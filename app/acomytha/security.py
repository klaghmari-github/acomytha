"""Mots de passe (scrypt) et jetons de session."""

from __future__ import annotations

import base64
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from acomytha.models import SessionToken, User


class PasswordHasher:
    _N = 2**14
    _R = 8
    _P = 1

    def hash(self, secret: str) -> str:
        salt = os.urandom(16)
        dk = hashlib.scrypt(secret.encode("utf-8"), salt=salt, n=self._N, r=self._R, p=self._P, dklen=32)
        return "scrypt$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(dk).decode()

    def verify(self, secret: str, stored: str | None) -> bool:
        if not stored or not stored.startswith("scrypt$"):
            return False
        try:
            _, salt_b64, dk_b64 = stored.split("$", 2)
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(dk_b64)
            dk = hashlib.scrypt(secret.encode("utf-8"), salt=salt, n=self._N, r=self._R, p=self._P, dklen=32)
        except (ValueError, TypeError):
            return False
        return secrets.compare_digest(dk, expected)


class SessionService:
    def __init__(self, hours: int = 72) -> None:
        self._hours = max(1, int(hours))
        self._hasher = PasswordHasher()

    @property
    def hours(self) -> int:
        return self._hours

    @property
    def hasher(self) -> PasswordHasher:
        return self._hasher

    def issue(
        self,
        db: Session,
        user: User,
        device_id: str,
        acting_role: str,
        child_profile_id: int | None = None,
    ) -> str:
        token = secrets.token_hex(32)
        db.add(
            SessionToken(
                token=token,
                user_id=user.id,
                device_id=device_id,
                acting_role=acting_role,
                child_profile_id=child_profile_id,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=self.hours),
            )
        )
        db.commit()
        return token

    def get(self, db: Session, token: str | None) -> SessionToken | None:
        if not token:
            return None
        row = db.get(SessionToken, token)
        if row is None:
            return None
        exp = row.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < datetime.now(timezone.utc):
            db.delete(row)
            db.commit()
            return None
        return row

    def revoke(self, db: Session, token: str | None) -> None:
        if not token:
            return
        row = db.get(SessionToken, token)
        if row is not None:
            db.delete(row)
            db.commit()
