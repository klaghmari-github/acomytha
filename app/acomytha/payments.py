"""Stripe Checkout : création des recharges et traitement idempotent des webhooks."""

from __future__ import annotations

import logging
import secrets
from decimal import Decimal, InvalidOperation
from typing import Any

from sqlalchemy import update
from sqlalchemy.orm import Session

from acomytha.commerce import WalletBook, eur_to_a, params
from acomytha.models import StripeSession, User
from acomytha.settings import Settings

ALLOWED_EUR_CENTS = (1000, 2000, 3000, 4000, 5000)
HANDLED_SUCCESS_EVENTS = {"checkout.session.completed", "checkout.session.async_payment_succeeded"}
HANDLED_FAILURE_EVENTS = {"checkout.session.async_payment_failed", "checkout.session.expired"}

logger = logging.getLogger(__name__)


class StripeNotConfigured(RuntimeError):
    """La clé Stripe ou le SDK manque sur le serveur."""


class StripeCheckoutError(RuntimeError):
    """Stripe n'a pas pu créer la session de paiement."""


class StripeVerificationError(ValueError):
    """Le contenu signé ne correspond pas à la commande locale."""


def stripe_status(settings: Settings) -> str:
    """Expose l'état de configuration sans divulguer les secrets."""
    if not settings.stripe_secret:
        return "unconfigured"
    if not settings.stripe_webhook_secret:
        return "webhook_missing"
    if settings.stripe_secret.startswith("sk_test_"):
        return "test"
    if settings.stripe_secret.startswith("sk_live_") and settings.public_url.startswith("https://"):
        return "live"
    return "invalid"


def _stripe_module():
    try:
        import stripe
    except ImportError as exc:
        raise StripeNotConfigured("Le paquet Python stripe n'est pas installé sur le serveur.") from exc
    return stripe


def _eur_cents(eur: float) -> int:
    try:
        cents_value = Decimal(str(eur)) * 100
    except InvalidOperation as exc:
        raise ValueError("montant") from exc
    if cents_value != cents_value.to_integral_value():
        raise ValueError("montant")
    cents = int(cents_value)
    if cents not in ALLOWED_EUR_CENTS:
        raise ValueError("montant")
    return cents


def create_recharge(db: Session, settings: Settings, parent_id: int, eur: float) -> dict[str, Any]:
    """Crée une Checkout Session ; aucun crédit n'est accordé ici."""
    cents = _eur_cents(eur)
    status = stripe_status(settings)
    if status == "unconfigured":
        raise StripeNotConfigured("Stripe n'est pas encore configuré sur ce serveur.")
    if status == "webhook_missing":
        raise StripeNotConfigured("Webhook Stripe non configuré")
    if status not in {"test", "live"}:
        raise StripeNotConfigured("Configuration Stripe invalide, ou clé live utilisée sans URL HTTPS.")

    stripe = _stripe_module()
    values = params(db)
    amount_a = eur_to_a(cents / 100, values)
    ref = secrets.token_urlsafe(24)
    row = StripeSession(parent_id=parent_id, ref=ref, eur=cents / 100, amount_a=amount_a, status="pending")
    db.add(row)
    db.commit()

    user = db.get(User, parent_id)
    try:
        checkout = stripe.checkout.Session.create(
            api_key=settings.stripe_secret,
            idempotency_key=f"acomytha-recharge-{ref}",
            mode="payment",
            client_reference_id=ref,
            customer_email=user.email if user and user.email else None,
            success_url=f"{settings.public_url.rstrip('/')}/#/parent?checkout=success",
            cancel_url=f"{settings.public_url.rstrip('/')}/#/parent?checkout=cancelled",
            metadata={"ref": ref, "parent_id": str(parent_id), "amount_a": str(amount_a)},
            line_items=[
                {
                    "quantity": 1,
                    "price_data": {
                        "currency": "eur",
                        "unit_amount": cents,
                        "product_data": {"name": f"AcoMytha · {amount_a:g} acm"},
                    },
                }
            ],
        )
    except Exception as exc:  # Le SDK expose plusieurs sous-classes selon sa version.
        row.status = "failed"
        db.commit()
        logger.exception("Échec de création d'une Checkout Session Stripe")
        raise StripeCheckoutError("Stripe n'a pas pu initialiser le paiement. Réessayez plus tard.") from exc

    if not getattr(checkout, "id", None) or not getattr(checkout, "url", None):
        row.status = "failed"
        db.commit()
        raise StripeCheckoutError("Stripe a renvoyé une session de paiement incomplète.")

    row.provider_id = checkout.id
    db.commit()
    return {"checkout_url": checkout.url, "ref": ref, "eur": cents / 100, "would_credit_a": amount_a}


def _find_and_verify(db: Session, obj: Any) -> StripeSession:
    provider_id = str(obj.get("id") or "")
    metadata = obj.get("metadata") or {}
    ref = str(metadata.get("ref") or "")
    row = db.query(StripeSession).filter(StripeSession.provider_id == provider_id).one_or_none()
    if row is None or not provider_id:
        raise StripeVerificationError("session Stripe inconnue")
    expected_cents = int(round(row.eur * 100))
    checks = (
        ref == row.ref,
        str(metadata.get("parent_id") or "") == str(row.parent_id),
        obj.get("mode") == "payment",
        str(obj.get("currency") or "").lower() == "eur",
        int(obj.get("amount_total") or 0) == expected_cents,
    )
    if not all(checks):
        raise StripeVerificationError("la session Stripe ne correspond pas à la recharge")
    return row


def process_checkout_event(db: Session, event: Any) -> StripeSession | None:
    """Vérifie puis crédite une recharge une seule fois, même après un nouvel envoi du webhook."""
    event_type = str(event.get("type") or "")
    if event_type not in HANDLED_SUCCESS_EVENTS | HANDLED_FAILURE_EVENTS:
        return None
    obj = event["data"]["object"]
    row = _find_and_verify(db, obj)

    if event_type in HANDLED_FAILURE_EVENTS:
        if row.status != "paid":
            row.status = "expired" if event_type.endswith("expired") else "failed"
            db.commit()
        return row

    if obj.get("payment_status") != "paid" or row.status == "paid":
        return row

    claimed = db.execute(
        update(StripeSession)
        .where(StripeSession.id == row.id, StripeSession.status != "paid")
        .values(status="paid")
        .execution_options(synchronize_session=False)
    )
    if claimed.rowcount != 1:
        db.rollback()
        return db.get(StripeSession, row.id)

    WalletBook(db, row.parent_id).credit(
        row.amount_a,
        kind="recharge",
        eur=row.eur,
        ref=row.ref,
        note=f"{row.eur:g} € via Stripe",
    )
    db.commit()
    db.refresh(row)
    return row
