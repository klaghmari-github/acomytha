"""Connexion, bascule enfant, déconnexion."""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from acomytha.api.deps import AuthContext, get_auth, get_db, roles_for
from acomytha.devices import DeviceConflict, DeviceGuard
from acomytha.commerce import grant_welcome, num
from acomytha.models import ChildProfile, EmailVerification, User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginBody(BaseModel):
    email: str
    password: str
    device_id: str = Field(min_length=8, max_length=64)
    device_label: str = ""


class ChildBody(BaseModel):
    profile_id: int
    pin: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$")
    device_id: str = Field(min_length=8, max_length=64)


class SignupBody(BaseModel):
    email: str
    password: str = Field(min_length=8)
    display_name: str = ""
    device_id: str = Field(min_length=8, max_length=64)
    device_label: str = ""


class VerifyEmailBody(BaseModel):
    token: str = Field(min_length=32, max_length=256)
    device_id: str = Field(min_length=8, max_length=64)
    device_label: str = ""


class ResendVerificationBody(BaseModel):
    email: str


class PinChangeBody(BaseModel):
    current_pin: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$")
    new_pin: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$")


class ParentBackBody(BaseModel):
    pin: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$")


def _profile_of(db: Session, parent_id: int, profile_id: int) -> ChildProfile | None:
    return db.query(ChildProfile).filter(
        ChildProfile.id == profile_id,
        ChildProfile.parent_id == parent_id,
    ).one_or_none()


def _valid_pin(pin: str) -> bool:
    return bool(pin) and pin.isdigit() and len(pin) == 4


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


def _verification_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _send_verification(db: Session, request: Request, user: User) -> None:
    now = datetime.now(timezone.utc)
    db.query(EmailVerification).filter(
        EmailVerification.user_id == user.id,
        EmailVerification.used_at.is_(None),
    ).delete()
    token = secrets.token_urlsafe(32)
    db.add(
        EmailVerification(
            user_id=user.id,
            token_hash=_verification_hash(token),
            expires_at=now + timedelta(hours=request.app.state.settings.email_verification_hours),
        )
    )
    db.commit()
    url = f"{request.app.state.settings.public_url.rstrip('/')}/#/verification?token={token}"
    request.app.state.mailer.send_verification(user.email, url)


def _user_payload(user: User, role: str, db: Session) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "role": role,
        "home_role": user.role,
        "roles": sorted(roles_for(db, user)),
    }


@router.post("/signup")
def signup(body: SignupBody, request: Request, response: Response, db: Session = Depends(get_db)):
    email = body.email.strip().lower()
    if db.query(User).filter(User.email == email).one_or_none():
        raise HTTPException(409, "cette adresse a déjà un compte")
    hasher = request.app.state.sessions.hasher
    name = (body.display_name or "").strip() or email.split("@")[0]
    parent = User(email=email, display_name=name, role="parent", password_hash=hasher.hash(body.password), is_active=False)
    db.add(parent)
    db.flush()
    db.commit()
    _send_verification(db, request, parent)
    return {"verification_required": True, "email": parent.email}


@router.post("/verify-email")
def verify_email(body: VerifyEmailBody, request: Request, response: Response, db: Session = Depends(get_db)):
    row = db.query(EmailVerification).filter(
        EmailVerification.token_hash == _verification_hash(body.token),
        EmailVerification.used_at.is_(None),
    ).one_or_none()
    now = datetime.now(timezone.utc)
    if row is None:
        raise HTTPException(400, "lien de validation inconnu ou déjà utilisé")
    expires = row.expires_at if row.expires_at.tzinfo else row.expires_at.replace(tzinfo=timezone.utc)
    if expires < now:
        raise HTTPException(410, "ce lien de validation a expiré")
    user = db.get(User, row.user_id)
    if user is None:
        raise HTTPException(400, "compte inconnu")
    first_activation = not user.is_active
    user.is_active = True
    row.used_at = now
    if first_activation:
        db.add(ChildProfile(parent_id=user.id, display_name="Mon enfant", age_band="N1"))
        grant_welcome(db, user.id)
    db.commit()
    ua = request.headers.get("user-agent", "")
    request.app.state.devices.assert_or_bind(db, user, body.device_id, ua, body.device_label)
    session_token = request.app.state.sessions.issue(db, user, body.device_id, "parent")
    _set_cookie(response, request, session_token)
    return _user_payload(user, "parent", db)


@router.post("/resend-verification")
def resend_verification(body: ResendVerificationBody, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.strip().lower()).one_or_none()
    if user is not None and not user.is_active:
        _send_verification(db, request, user)
    return {"ok": True}


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
                "message": "Ce compte est déjà ouvert sur un autre appareil. Écrivez-nous si vous avez changé de téléphone.",
                "alert_id": exc.alert.id,
            },
        ) from exc
    token = request.app.state.sessions.issue(db, user, body.device_id, user.role)
    _set_cookie(response, request, token)
    return _user_payload(user, user.role, db)


@router.post("/enfant")
def enter_child(body: ChildBody, request: Request, response: Response, auth: AuthContext = Depends(get_auth), db: Session = Depends(get_db)):
    if auth.user.role != "parent":
        raise HTTPException(403, "seul un parent ouvre le mode enfant")
    if auth.session.device_id != body.device_id:
        raise HTTPException(409, "appareil différent de la session")
    if not _valid_pin(body.pin):
        raise HTTPException(400, "le code a 4 chiffres")
    profile = _profile_of(db, auth.user.id, body.profile_id)
    if profile is None:
        raise HTTPException(404, "profil enfant introuvable")
    profile.unlock_pin_hash = request.app.state.sessions.hasher.hash(body.pin)
    db.commit()
    request.app.state.sessions.revoke(db, auth.session.token)
    token = request.app.state.sessions.issue(db, auth.user, body.device_id, "child", profile.id)
    _set_cookie(response, request, token)
    payload = _user_payload(auth.user, "child", db)
    payload["child_profile"] = {"id": profile.id, "display_name": profile.display_name}
    return payload


@router.post("/parent")
def back_to_parent(
    body: ParentBackBody,
    request: Request,
    response: Response,
    auth: AuthContext = Depends(get_auth),
    db: Session = Depends(get_db),
):
    if auth.role != "child":
        raise HTTPException(403, "pas en mode enfant")
    profile = _profile_of(db, auth.user.id, auth.child_profile_id)
    if profile is None or not _valid_pin(body.pin) or not request.app.state.sessions.hasher.verify(body.pin, profile.unlock_pin_hash):
        raise HTTPException(401, "ce n'est pas le bon code")
    request.app.state.sessions.revoke(db, auth.session.token)
    profile.unlock_pin_hash = None
    db.commit()
    token = request.app.state.sessions.issue(db, auth.user, auth.session.device_id, "parent")
    _set_cookie(response, request, token)
    return _user_payload(auth.user, "parent", db)


@router.put("/pin")
def change_pin(body: PinChangeBody, request: Request, auth: AuthContext = Depends(get_auth), db: Session = Depends(get_db)):
    if auth.role != "parent":
        raise HTTPException(403, "seul le parent change le code")
    raise HTTPException(410, "le code est désormais créé à chaque activation du mode enfant")


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(request.app.state.settings.cookie_name)
    request.app.state.sessions.revoke(db, token)
    response.delete_cookie(request.app.state.settings.cookie_name, path="/")
    return {"ok": True}


@router.get("/me")
def me(auth: AuthContext = Depends(get_auth), db: Session = Depends(get_db)):
    payload = _user_payload(auth.user, auth.role, db)
    if auth.role == "child" and auth.session.child_profile_id:
        payload["child_profile_id"] = auth.session.child_profile_id
    return payload
