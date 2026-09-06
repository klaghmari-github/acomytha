"""Console admin : comptes et alertes appareil."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from acomytha.api.deps import ADULT_ROLES, AuthContext, get_db, require_roles, roles_for
from acomytha.commerce import PARAM_SPECS, params, seed_params
from acomytha.models import AccountRole, AppSetting, DeviceAlert, DeviceBinding, StoryOrder, User

router = APIRouter(prefix="/api/admin", tags=["admin"])


class NewParent(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)
    display_name: str
    child_pin: str = Field(min_length=4, max_length=8)


class SettingsBody(BaseModel):
    values: dict[str, str]


class RolesBody(BaseModel):
    roles: list[str]


@router.get("/alerts")
def alerts(_auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    rows = list(db.scalars(select(DeviceAlert).order_by(DeviceAlert.created_at.desc()).limit(200)))
    users = {u.id: u for u in db.scalars(select(User).where(User.id.in_({r.user_id for r in rows} or {0})))}
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "email": users.get(r.user_id).email if users.get(r.user_id) else None,
            "display_name": users.get(r.user_id).display_name if users.get(r.user_id) else "",
            "attempted_device_id": r.attempted_device_id,
            "bound_device_id": r.bound_device_id,
            "user_agent": r.user_agent,
            "created_at": r.created_at.isoformat(),
            "acknowledged": r.acknowledged,
        }
        for r in rows
    ]


@router.post("/alerts/{alert_id}/ack")
def ack_alert(alert_id: int, _auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    row = db.get(DeviceAlert, alert_id)
    if row is None:
        raise HTTPException(404, "alerte inconnue")
    row.acknowledged = True
    db.commit()
    return {"ok": True}


@router.get("/users")
def users(_auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    rows = list(db.scalars(select(User).order_by(User.role, User.id)))
    bindings = {b.user_id: b for b in db.scalars(select(DeviceBinding))}
    return [
        {
            "id": u.id,
            "email": u.email,
            "display_name": u.display_name,
            "role": u.role,
            "roles": sorted(roles_for(db, u)),
            "parent_id": u.parent_id,
            "is_active": u.is_active,
            "device_id": bindings[u.id].device_id if u.id in bindings else None,
            "device_bound_at": bindings[u.id].bound_at.isoformat() if u.id in bindings else None,
        }
        for u in rows
    ]


@router.put("/users/{user_id}/roles")
def update_roles(
    user_id: int,
    body: RolesBody,
    auth: AuthContext = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if user is None or user.role == "child":
        raise HTTPException(404, "compte adulte inconnu")
    requested = set(body.roles)
    if not requested.issubset(ADULT_ROLES):
        raise HTTPException(400, "rôle inconnu")
    requested.add("parent")
    if user.id == auth.user.id and "admin" not in requested:
        raise HTTPException(409, "vous ne pouvez pas retirer votre propre rôle administrateur")
    db.query(AccountRole).filter(AccountRole.user_id == user.id).delete()
    for role in sorted(requested):
        db.add(AccountRole(user_id=user.id, role=role))
    db.commit()
    return {"id": user.id, "roles": sorted(roles_for(db, user))}


@router.post("/users")
def create_parent(body: NewParent, request: Request, _auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    email = str(body.email).lower()
    if db.query(User).filter(User.email == email).one_or_none():
        raise HTTPException(409, "email déjà pris")
    hasher = request.app.state.sessions.hasher
    parent = User(
        email=email,
        display_name=body.display_name,
        role="parent",
        password_hash=hasher.hash(body.password),
    )
    db.add(parent)
    db.flush()
    db.add(
        User(
            email=None,
            display_name="Enfant",
            role="child",
            parent_id=parent.id,
            pin_hash=hasher.hash(body.child_pin),
        )
    )
    db.commit()
    return {"id": parent.id, "email": parent.email}


@router.post("/users/{user_id}/reset-device")
def reset_device(user_id: int, request: Request, _auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(404, "compte inconnu")
    holder = user.parent_id or user.id
    request.app.state.devices.reset(db, holder)
    return {"ok": True}


@router.get("/stats")
def stats(_auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    from acomytha.models import Chunk, Story

    return {
        "users": db.query(User).count(),
        "stories": db.query(Story).count(),
        "chunks": db.query(Chunk).count(),
        "alerts_open": db.query(DeviceAlert).filter(DeviceAlert.acknowledged.is_(False)).count(),
        "with_audio": db.query(Story).filter(Story.has_audio.is_(True)).count(),
        "orders_pending": db.query(StoryOrder).filter(StoryOrder.status == "pending").count(),
    }


@router.get("/settings")
def get_settings(_auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    seed_params(db)
    current = params(db)
    return [{"key": k, "value": current.get(k, d), "label": lab} for k, d, lab in PARAM_SPECS]


@router.put("/settings")
def put_settings(body: SettingsBody, _auth: AuthContext = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    seed_params(db)
    allowed = {k for k, _d, _l in PARAM_SPECS}
    for key, value in body.values.items():
        if key not in allowed:
            continue
        row = db.get(AppSetting, key)
        if row:
            row.value = str(value)[:400]
    db.commit()
    return get_settings(_auth, db)
