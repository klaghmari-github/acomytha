"""Solde acm (clés internes *_a), taux €→acm, paramètres admin."""

from __future__ import annotations

from sqlalchemy.orm import Session

from acomytha.models import AppSetting, LedgerEntry, Purchase, Story, Wallet

PARAM_SPECS: list[tuple[str, str, str]] = [
    ("welcome_credit_eur", "10", "Crédit offert à l’activation (€)"),
    ("preview_seconds", "30", "Aperçu visiteur vitrine (secondes)"),
    ("home_catalog_page_size", "6", "Accueil : histoires par lot (scroll)"),
    ("parent_preview_seconds", "30", "Aperçu parent, histoire non achetée (secondes)"),
    ("price_story_a", "1", "Prix d’une histoire (acm)"),
    ("price_tree_a", "1", "Prix d’une série avec des choix (acm)"),
    ("price_order_a", "1.5", "Commander une histoire (acm)"),
    ("price_ramification_a", "0.5", "Branche supplémentaire à la commande (acm)"),
    ("max_ramifications", "3", "Branches max par commande"),
    ("price_voice_record_a", "5", "Enregistrer une voix (acm)"),
    ("price_voice_apply_all_a", "5", "Appliquer la voix à tout le déjà-acheté (acm)"),
    ("fx_rate_start", "1", "Taux acm par €, première tranche"),
    ("fx_rate_step", "0.25", "Hausse du taux toutes les N €"),
    ("fx_rate_every_eur", "10", "Largeur d’une tranche (€)"),
    ("fx_rate_max", "5", "Taux max acm par €"),
    ("free_story_ids", "TREE-SEC-001", "Histoires offertes (ids, virgules)"),
    ("pack_trees_count", "10", "Nouvelles séries dans le pack"),
    ("pack_trees_eur", "10", "Prix du pack (€)"),
    ("max_child_profiles", "10", "Profils enfants maximum par foyer"),
]

LEGACY_SECRET_KEYS = ("stripe_secret", "stripe_publishable", "stripe_webhook_secret")


class ShopParams:
    """Paramètres boutique d’un foyer de données. Cache par requête."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._values: dict[str, str] | None = None

    def seed(self) -> None:
        # Les anciennes versions stockaient les secrets Stripe en base et les exposaient
        # dans l'admin. Ils vivent désormais exclusivement dans l'environnement du serveur.
        self._db.query(AppSetting).filter(AppSetting.key.in_(LEGACY_SECRET_KEYS)).delete(synchronize_session=False)
        existing = {r.key: r for r in self._db.query(AppSetting).all()}
        for key, value, label in PARAM_SPECS:
            row = existing.get(key)
            if row is None:
                self._db.add(AppSetting(key=key, value=value, label=label))
            else:
                if row.label != label:
                    row.label = label
                if key == "preview_seconds" and row.value == "10":
                    row.value = "30"
        self._db.commit()
        self._values = None

    def as_dict(self) -> dict[str, str]:
        if self._values is None:
            self.seed()
            self._values = {r.key: r.value for r in self._db.query(AppSetting).all()}
        return self._values

    def number(self, key: str) -> float:
        raw = self.as_dict().get(key, "0")
        try:
            return float(raw)
        except ValueError:
            return 0.0

    def free_ids(self) -> set[str]:
        raw = self.as_dict().get("free_story_ids", "")
        return {x.strip() for x in raw.split(",") if x.strip()}

    @staticmethod
    def fx_rate(eur: float, values: dict[str, str] | None = None) -> float:
        start = float((values or {}).get("fx_rate_start", "1"))
        step = float((values or {}).get("fx_rate_step", "0.25"))
        every = float((values or {}).get("fx_rate_every_eur", "10")) or 10
        cap = float((values or {}).get("fx_rate_max", "5"))
        if eur <= 0:
            return start
        band = int((max(eur, 1) - 1) // every)
        return min(cap, start + step * band)

    @staticmethod
    def eur_to_a(eur: float, values: dict[str, str] | None = None) -> float:
        return round(eur * ShopParams.fx_rate(eur, values), 2)


class WalletBook:
    """Livre de compte d’un parent : solde, crédit, débit, possessions."""

    def __init__(self, db: Session, parent_id: int) -> None:
        self._db = db
        self._parent_id = int(parent_id)

    @property
    def parent_id(self) -> int:
        return self._parent_id

    def row(self) -> Wallet:
        found = self._db.get(Wallet, self._parent_id)
        if found is None:
            found = Wallet(parent_id=self._parent_id, balance_a=0, lifetime_eur=0)
            self._db.add(found)
            self._db.flush()
        return found

    @property
    def balance_a(self) -> float:
        return float(self.row().balance_a)

    def owned_ids(self) -> set[str]:
        bought = {r.item_id for r in self._db.query(Purchase).filter(Purchase.parent_id == self._parent_id)}
        return bought | ShopParams(self._db).free_ids()

    def credit(self, amount_a: float, *, kind: str, eur: float = 0, ref: str = "", note: str = "") -> Wallet:
        w = self.row()
        w.balance_a = round(w.balance_a + amount_a, 2)
        if eur:
            w.lifetime_eur = round(w.lifetime_eur + eur, 2)
        self._db.add(
            LedgerEntry(parent_id=self._parent_id, kind=kind, amount_a=amount_a, amount_eur=eur, ref=ref, note=note)
        )
        return w

    def debit(self, amount_a: float, *, kind: str, ref: str = "", note: str = "") -> Wallet:
        w = self.row()
        if w.balance_a + 1e-9 < amount_a:
            raise ValueError("solde insuffisant")
        w.balance_a = round(w.balance_a - amount_a, 2)
        self._db.add(LedgerEntry(parent_id=self._parent_id, kind=kind, amount_a=-amount_a, ref=ref, note=note))
        return w

    def grant_welcome(self) -> Wallet:
        w = self.row()
        if self._db.query(LedgerEntry).filter(LedgerEntry.parent_id == self._parent_id, LedgerEntry.kind == "welcome").first():
            return w
        p = ShopParams(self._db)
        eur = p.number("welcome_credit_eur")
        a = ShopParams.eur_to_a(eur, p.as_dict())
        return self.credit(a, kind="welcome", eur=eur, note="activation")

    def price_for(self, story: Story) -> float:
        return price_of(story, self._db)

    def payload(self) -> dict:
        p = ShopParams(self._db)
        values = p.as_dict()
        w = self.row()
        return {
            "balance_a": w.balance_a,
            "lifetime_eur": w.lifetime_eur,
            "owned": sorted(self.owned_ids()),
            "free": sorted(p.free_ids()),
            "prices": {
                "story": p.number("price_story_a"),
                "tree": p.number("price_tree_a"),
                "order": p.number("price_order_a"),
                "ramification": p.number("price_ramification_a"),
                "voice": p.number("price_voice_record_a"),
                "voice_apply_all": p.number("price_voice_apply_all_a"),
            },
            "preview_seconds": int(p.number("preview_seconds") or 10),
            "parent_preview_seconds": int(p.number("parent_preview_seconds") or 30),
            "pack": {"count": int(p.number("pack_trees_count") or 10), "eur": p.number("pack_trees_eur")},
            "fx": {
                "start": float(values["fx_rate_start"]),
                "step": float(values["fx_rate_step"]),
                "every": float(values["fx_rate_every_eur"]),
                "max": float(values["fx_rate_max"]),
            },
        }


def seed_params(db: Session) -> None:
    ShopParams(db).seed()


def params(db: Session) -> dict[str, str]:
    return ShopParams(db).as_dict()


def num(db: Session, key: str) -> float:
    return ShopParams(db).number(key)


def fx_rate(eur: float, p: dict[str, str] | None = None) -> float:
    return ShopParams.fx_rate(eur, p)


def eur_to_a(eur: float, p: dict[str, str] | None = None) -> float:
    return ShopParams.eur_to_a(eur, p)


def price_of(story: Story, db: Session) -> float:
    p = ShopParams(db)
    if story.kind == "ramifiee":
        return p.number("price_tree_a")
    return p.number("price_story_a")


def price_for(story: Story, db: Session) -> float:
    return price_of(story, db)


def free_ids(db: Session) -> set[str]:
    return ShopParams(db).free_ids()


def owned_ids(db: Session, parent_id: int) -> set[str]:
    return WalletBook(db, parent_id).owned_ids()


def get_wallet(db: Session, parent_id: int) -> Wallet:
    return WalletBook(db, parent_id).row()


def credit(db: Session, parent_id: int, amount_a: float, *, kind: str, eur: float = 0, ref: str = "", note: str = "") -> Wallet:
    return WalletBook(db, parent_id).credit(amount_a, kind=kind, eur=eur, ref=ref, note=note)


def debit(db: Session, parent_id: int, amount_a: float, *, kind: str, ref: str = "", note: str = "") -> Wallet:
    return WalletBook(db, parent_id).debit(amount_a, kind=kind, ref=ref, note=note)


def grant_welcome(db: Session, parent_id: int) -> Wallet:
    return WalletBook(db, parent_id).grant_welcome()
