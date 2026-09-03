"""Comptes de démo + import catalogue si base vide."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from sentier.catalog import CatalogImporter
from sentier.models import ForestEntry, Story, User
from sentier.security import PasswordHasher
from sentier.settings import Settings


class Bootstrap:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.hasher = PasswordHasher()
        self.importer = CatalogImporter(settings)

    def run(self, db: Session, import_limit: int | None = None) -> None:
        self.ensure_users(db)
        n = db.scalar(select(func.count()).select_from(Story)) or 0
        if n == 0:
            self.importer.import_all(db, limit=import_limit)
        self.ensure_demo_forest(db)

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
        parent = db.query(User).filter(User.email == self.settings.parent_email).one_or_none()
        if parent is None:
            parent = User(
                email=self.settings.parent_email,
                display_name="Parent démo",
                role="parent",
                password_hash=self.hasher.hash(self.settings.parent_password),
            )
            db.add(parent)
            db.flush()
        child = db.query(User).filter(User.parent_id == parent.id, User.role == "child").one_or_none()
        if child is None:
            db.add(
                User(
                    email=None,
                    display_name="Enfant",
                    role="child",
                    parent_id=parent.id,
                    pin_hash=self.hasher.hash(self.settings.child_pin),
                )
            )
        db.commit()
