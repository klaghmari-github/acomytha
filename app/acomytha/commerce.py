"""Solde A, taux €→A, paramètres admin."""

from __future__ import annotations

from sqlalchemy.orm import Session

from acomytha.models import AppSetting, LedgerEntry, Purchase, Story, Wallet

PARAM_SPECS: list[tuple[str, str, str]] = [
    ("welcome_credit_eur", "10", "Crédit offert à l’activation (€)"),
    ("preview_seconds", "10", "Aperçu sans achat (secondes)"),
    ("price_story_a", "1", "Prix d’une histoire (A)"),
    ("price_tree_a", "1", "Prix d’une série avec des choix (A)"),
    ("price_order_a", "1.5", "Commander une histoire (A)"),
    ("price_ramification_a", "0.5", "Branche supplémentaire à la commande (A)"),
    ("max_ramifications", "3", "Branches max par commande"),
    ("price_voice_record_a", "5", "Enregistrer une voix (A)"),
    ("price_voice_apply_all_a", "5", "Appliquer la voix à tout le déjà-acheté (A)"),
    ("fx_rate_start", "1", "Taux A par €, première tranche"),
    ("fx_rate_step", "0.25", "Hausse du taux toutes les N €"),
    ("fx_rate_every_eur", "10", "Largeur d’une tranche (€)"),
    ("fx_rate_max", "5", "Taux max A par €"),
    ("free_story_ids", "TREE-SEC-001", "Histoires offertes (ids, virgules)"),
    ("pack_trees_count", "10", "Nouvelles séries dans le pack"),
    ("pack_trees_eur", "10", "Prix du pack (€)"),
    ("default_child_pin", "2468", "PIN enfant à l’inscription"),
]


def seed_params(db: Session) -> None:
    existing = {r.key for r in db.query(AppSetting).all()}
    for key, value, label in PARAM_SPECS:
        if key not in existing:
            db.add(AppSetting(key=key, value=value, label=label))
    db.commit()


def params(db: Session) -> dict[str, str]:
    seed_params(db)
    return {r.key: r.value for r in db.query(AppSetting).all()}


def num(db: Session, key: str) -> float:
    raw = params(db).get(key, "0")
    try:
        return float(raw)
    except ValueError:
        return 0.0


def fx_rate(eur: float, p: dict[str, str] | None = None) -> float:
    start = float((p or {}).get("fx_rate_start", "1"))
    step = float((p or {}).get("fx_rate_step", "0.25"))
    every = float((p or {}).get("fx_rate_every_eur", "10")) or 10
    cap = float((p or {}).get("fx_rate_max", "5"))
    if eur <= 0:
        return start
    band = int((max(eur, 1) - 1) // every)
    return min(cap, start + step * band)


def eur_to_a(eur: float, p: dict[str, str] | None = None) -> float:
    return round(eur * fx_rate(eur, p), 2)


def price_for(story: Story, db: Session) -> float:
    if story.kind == "ramifiee":
        return num(db, "price_tree_a")
    return num(db, "price_story_a")


def free_ids(db: Session) -> set[str]:
    raw = params(db).get("free_story_ids", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def owned_ids(db: Session, parent_id: int) -> set[str]:
    bought = {
        r.item_id
        for r in db.query(Purchase).filter(Purchase.parent_id == parent_id)
    }
    return bought | free_ids(db)


def get_wallet(db: Session, parent_id: int) -> Wallet:
    row = db.get(Wallet, parent_id)
    if row is None:
        row = Wallet(parent_id=parent_id, balance_a=0, lifetime_eur=0)
        db.add(row)
        db.flush()
    return row


def credit(db: Session, parent_id: int, amount_a: float, *, kind: str, eur: float = 0, ref: str = "", note: str = "") -> Wallet:
    w = get_wallet(db, parent_id)
    w.balance_a = round(w.balance_a + amount_a, 2)
    if eur:
        w.lifetime_eur = round(w.lifetime_eur + eur, 2)
    db.add(LedgerEntry(parent_id=parent_id, kind=kind, amount_a=amount_a, amount_eur=eur, ref=ref, note=note))
    return w


def debit(db: Session, parent_id: int, amount_a: float, *, kind: str, ref: str = "", note: str = "") -> Wallet:
    w = get_wallet(db, parent_id)
    if w.balance_a + 1e-9 < amount_a:
        raise ValueError("solde insuffisant")
    w.balance_a = round(w.balance_a - amount_a, 2)
    db.add(LedgerEntry(parent_id=parent_id, kind=kind, amount_a=-amount_a, ref=ref, note=note))
    return w


def grant_welcome(db: Session, parent_id: int) -> Wallet:
    w = get_wallet(db, parent_id)
    if db.query(LedgerEntry).filter(LedgerEntry.parent_id == parent_id, LedgerEntry.kind == "welcome").first():
        return w
    eur = num(db, "welcome_credit_eur")
    a = eur_to_a(eur, params(db))
    return credit(db, parent_id, a, kind="welcome", eur=eur, note="activation")
