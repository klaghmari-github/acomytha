"""Dépendances FastAPI : session cookie, rôles."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from acomytha.models import SessionToken, User


@dataclass
class AuthContext:
    user: User
    session: SessionToken
    role: str

    @property
    def parent_id(self) -> int:
        if self.user.role == "parent":
            return self.user.id
        if self.user.role == "child" and self.user.parent_id:
            return self.user.parent_id
        raise HTTPException(403, "pas un foyer")


def get_db(request: Request):
    yield from request.app.state.database.session()


def get_auth(request: Request, db: Session = Depends(get_db)) -> AuthContext:
    token = request.cookies.get(request.app.state.settings.cookie_name)
    sessions = request.app.state.sessions
    row = sessions.get(db, token)
    if row is None:
        raise HTTPException(401, "session requise")
    user = db.get(User, row.user_id)
    if user is None or not user.is_active:
        raise HTTPException(401, "compte inactif")
    return AuthContext(user=user, session=row, role=row.acting_role)


def require_roles(*roles: str):
    def _inner(auth: AuthContext = Depends(get_auth)) -> AuthContext:
        if auth.role not in roles:
            raise HTTPException(403, "rôle insuffisant")
        return auth

    return _inner
