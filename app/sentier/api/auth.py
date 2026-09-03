"""Connexion, bascule enfant, déconnexion."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from sentier.api.deps import AuthContext, get_auth, get_db
from sentier.devices import DeviceConflict, DeviceGuard
from sentier.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginBody(BaseModel):
    email: str
    password: str
    device_id: str = Field(min_length=8, max_length=64)
    device_label: str = ""


class ChildBody(BaseModel):
    pin: str
    device_id: str = Field(min_length=8, max_length=64)


def _set_cookie(response: Response, request: Request, token: str) -> None:
    settings = request.app.state.settings
    response.set_cookie(
        settings.cookie_name,
        token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=settings.session_hours * 3600,
        path="/",
    )


def _user_payload(user: User, role: str) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "role": role,
        "home_role": user.role,
    }


@router.post("/login")
def login(body: LoginBody, request: Request, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.strip().lower()).one_or_none()
    hasher = request.app.state.sessions.hasher
    if user is None or user.role == "child" or not hasher.verify(body.password, user.password_hash):
        raise HTTPException(401, "identifiants inconnus")
    if not user.is_active:
        raise HTTPException(403, "compte désactivé")
    ua = request.headers.get("user-agent", "")
    try:
        request.app.state.devices.assert_or_bind(db, user, body.device_id, ua, body.device_label)
    except DeviceConflict as exc:
        raise HTTPException(
            409,
            {
                "code": "device_bound",
                "message": "Cette clé est déjà liée à un autre appareil. L'admin a été alerté.",
                "alert_id": exc.alert.id,
            },
        ) from exc
    token = request.app.state.sessions.issue(db, user, body.device_id, user.role)
    _set_cookie(response, request, token)
    return _user_payload(user, user.role)


@router.post("/enfant")
def enter_child(body: ChildBody, request: Request, response: Response, auth: AuthContext = Depends(get_auth), db: Session = Depends(get_db)):
    if auth.user.role != "parent":
        raise HTTPException(403, "seul un parent ouvre le mode enfant")
    if auth.session.device_id != body.device_id:
        raise HTTPException(409, "appareil différent de la session")
    child = db.query(User).filter(User.parent_id == auth.user.id, User.role == "child").one_or_none()
    if child is None or not request.app.state.sessions.hasher.verify(body.pin, child.pin_hash):
        raise HTTPException(401, "code enfant incorrect")
    request.app.state.sessions.revoke(db, auth.session.token)
    token = request.app.state.sessions.issue(db, child, body.device_id, "child")
    _set_cookie(response, request, token)
    return _user_payload(child, "child")


@router.post("/parent")
def back_to_parent(request: Request, response: Response, auth: AuthContext = Depends(get_auth), db: Session = Depends(get_db)):
    if auth.user.role != "child" or not auth.user.parent_id:
        raise HTTPException(403, "pas en mode enfant")
    parent = db.get(User, auth.user.parent_id)
    if parent is None:
        raise HTTPException(404, "parent introuvable")
    request.app.state.sessions.revoke(db, auth.session.token)
    token = request.app.state.sessions.issue(db, parent, auth.session.device_id, "parent")
    _set_cookie(response, request, token)
    return _user_payload(parent, "parent")


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(request.app.state.settings.cookie_name)
    request.app.state.sessions.revoke(db, token)
    response.delete_cookie(request.app.state.settings.cookie_name, path="/")
    return {"ok": True}


@router.get("/me")
def me(auth: AuthContext = Depends(get_auth)):
    return _user_payload(auth.user, auth.role)
