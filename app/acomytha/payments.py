"""Recharge € → A. Stripe Checkout si les clés sont là, sinon paiement démo."""

from __future__ import annotations

import secrets
from typing import Any

from sqlalchemy.orm import Session

from acomytha.commerce import credit, eur_to_a, params
from acomytha.models import StripeSession
from acomytha.settings import Settings


ALLOWED_EUR = (10, 20, 30, 40, 50)


def stripe_secret(settings: Settings, db: Session) -> str:
    p = params(db)
    return (p.get("stripe_secret") or settings.stripe_secret or "").strip()


def stripe_publishable(settings: Settings, db: Session) -> str:
    p = params(db)
    return (p.get("stripe_publishable") or settings.stripe_publishable or "").strip()


def fulfill(db: Session, row: StripeSession) -> StripeSession:
    if row.status == "paid":
        return row
    credit(db, row.parent_id, row.amount_a, kind="recharge", eur=row.eur, ref=row.ref, note=f"{row.eur} €")
    row.status = "paid"
    db.commit()
    return row


def create_recharge(db: Session, settings: Settings, parent_id: int, eur: float) -> dict[str, Any]:
    if int(eur) not in ALLOWED_EUR:
        raise ValueError("montant")
    p = params(db)
    a = eur_to_a(eur, p)
    ref = secrets.token_urlsafe(16)
    row = StripeSession(parent_id=parent_id, ref=ref, eur=eur, amount_a=a, status="pending")
    db.add(row)
    db.commit()
    secret = stripe_secret(settings, db)
    pub = stripe_publishable(settings, db)
    if secret:
        try:
            import stripe

            stripe.api_key = secret
            session = stripe.checkout.Session.create(
                mode="payment",
                success_url=f"{settings.public_url}/#/parent?paid=1",
                cancel_url=f"{settings.public_url}/#/parent?paid=0",
                metadata={"ref": ref, "parent_id": str(parent_id)},
                line_items=[
                    {
                        "quantity": 1,
                        "price_data": {
                            "currency": "eur",
                            "unit_amount": int(round(eur * 100)),
                            "product_data": {"name": f"AcoMytha · {a} acm"},
                        },
                    }
                ],
            )
            row.provider_id = session.id or ""
            db.commit()
            return {
                "mode": "stripe",
                "checkout_url": session.url,
                "publishable": pub,
                "ref": ref,
                "eur": eur,
                "would_credit_a": a,
                "stripe": "ready",
            }
        except Exception as exc:  # noqa: BLE001
            return {
                "mode": "demo",
                "ref": ref,
                "eur": eur,
                "would_credit_a": a,
                "stripe": "error",
                "message": str(exc)[:180],
            }
    return {
        "mode": "demo",
        "ref": ref,
        "eur": eur,
        "would_credit_a": a,
        "stripe": "demo",
        "message": "Paiement démo — Stripe se branche avec les clés admin.",
    }


def confirm_demo(db: Session, parent_id: int, ref: str) -> StripeSession:
    row = db.query(StripeSession).filter(StripeSession.ref == ref, StripeSession.parent_id == parent_id).one_or_none()
    if row is None:
        raise LookupError("paiement inconnu")
    return fulfill(db, row)


def fulfill_provider(db: Session, provider_id: str, ref: str = "") -> StripeSession | None:
    row = None
    if provider_id:
        row = db.query(StripeSession).filter(StripeSession.provider_id == provider_id).one_or_none()
    if row is None and ref:
        row = db.query(StripeSession).filter(StripeSession.ref == ref).one_or_none()
    if row is None:
        return None
    return fulfill(db, row)
