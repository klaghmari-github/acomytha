"""Dépendances FastAPI : session cookie, rôles."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from acomytha.models import AccountRole, SessionToken, User

ADULT_ROLES = frozenset({"parent", "editor", "admin"})


def roles_for(db: Session, user: User) -> frozenset[str]:
    if user.role == "child":
        return frozenset({"child"})
    granted = set(db.scalars(select(AccountRole.role).where(AccountRole.user_id == user.id)))
    granted.add("parent")
    if user.role in ADULT_ROLES:
        granted.add(user.role)
    return frozenset(granted)


@dataclass
class AuthContext:
    user: User
    session: SessionToken
    role: str
    roles: frozenset[str]

    @property
    def parent_id(self) -> int:
        if self.user.role == "parent" or self.role == "child":
            return self.user.id
        if self.user.role == "child" and self.user.parent_id:
            return self.user.parent_id
        raise HTTPException(403, "pas un foyer")

    @property
    def child_profile_id(self) -> int:
        if self.role != "child" or not self.session.child_profile_id:
            raise HTTPException(403, "profil enfant requis")
        return self.session.child_profile_id


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
    return AuthContext(user=user, session=row, role=row.acting_role, roles=roles_for(db, user))


def require_roles(*roles: str):
    def _inner(auth: AuthContext = Depends(get_auth)) -> AuthContext:
        if auth.role == "child" and "child" not in roles:
            raise HTTPException(403, "rôle insuffisant")
        if auth.role != "child" and not auth.roles.intersection(roles):
            raise HTTPException(403, "rôle insuffisant")
        return auth

    return _inner
