"""Comptes de démo + import catalogue si base vide."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from acomytha.catalog import CatalogImporter, fill_durations, fill_interaction
from acomytha.commerce import grant_welcome, seed_params
from acomytha.models import ChildCatalogEntry, ChildProfile, ForestEntry, Purchase, Story, User
from acomytha.security import PasswordHasher
from acomytha.settings import Settings


class Bootstrap:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._hasher = PasswordHasher()
        self._importer = CatalogImporter(settings)

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def hasher(self) -> PasswordHasher:
        return self._hasher

    @property
    def importer(self) -> CatalogImporter:
        return self._importer

    def run(self, db: Session, import_limit: int | None = None) -> None:
        seed_params(db)
        self.ensure_users(db)
        n = db.scalar(select(func.count()).select_from(Story)) or 0
        if n == 0:
            self.importer.import_all(db, limit=import_limit)
        self.ensure_demo_forest(db)
        self.ensure_child_profiles(db)
        self.ensure_demo_wallet(db)
        fill_durations(db, self.settings)
        fill_interaction(db)

    def ensure_demo_forest(self, db: Session) -> None:
        parent = db.query(User).filter(User.email == self.settings.parent_email).one_or_none()
        if parent is None:
            return
        existing = db.query(ForestEntry).filter(ForestEntry.parent_id == parent.id).count()
        if existing:
            return
        for sid in ("ATOM-SAN.ALI.001-01", "TREE-SEC-001"):
            if db.get(Story, sid) is not None:
                db.add(ForestEntry(parent_id=parent.id, story_id=sid))
        db.commit()

    def ensure_users(self, db: Session) -> None:
        if not (self.settings.admin_email and self.settings.admin_password):
            return
        admin = db.query(User).filter(User.email == self.settings.admin_email).one_or_none()
        if admin is None:
            admin = User(
                email=self.settings.admin_email,
                display_name="Fondateur",
                role="admin",
                password_hash=self.hasher.hash(self.settings.admin_password),
            )
            db.add(admin)
            db.flush()
        parent = db.query(User).filter(User.email == self.settings.parent_email).one_or_none() if self.settings.parent_email else None
        if parent is None and self.settings.parent_email and self.settings.parent_password:
            parent = User(
                email=self.settings.parent_email,
                display_name="Parent démo",
                role="parent",
                password_hash=self.hasher.hash(self.settings.parent_password),
            )
            db.add(parent)
            db.flush()
        db.commit()

    def ensure_demo_wallet(self, db: Session) -> None:
        parent = db.query(User).filter(User.email == self.settings.parent_email).one_or_none()
        if parent is None:
            return
        grant_welcome(db, parent.id)
        for sid in ("ATOM-SAN.ALI.001-01", "TREE-SEC-001"):
            if db.get(Story, sid) is None:
                continue
            exists = (
                db.query(Purchase)
                .filter(Purchase.parent_id == parent.id, Purchase.item_id == sid)
                .one_or_none()
            )
            if exists is None:
                db.add(Purchase(parent_id=parent.id, item_type="story", item_id=sid, price_a=0))
        db.commit()

    def ensure_child_profiles(self, db: Session) -> None:
        parents = db.query(User).filter(User.role == "parent").all()
        for parent in parents:
            profile = db.query(ChildProfile).filter(ChildProfile.parent_id == parent.id).first()
            if profile is None:
                profile = ChildProfile(parent_id=parent.id, display_name="Mon enfant", age_band="N1")
                db.add(profile)
                db.flush()
            legacy_ids = [row.story_id for row in db.query(ForestEntry).filter(ForestEntry.parent_id == parent.id)]
            existing = {row.story_id for row in db.query(ChildCatalogEntry).filter(ChildCatalogEntry.profile_id == profile.id)}
            for story_id in legacy_ids:
                if story_id not in existing:
                    db.add(ChildCatalogEntry(profile_id=profile.id, story_id=story_id))
        db.commit()
