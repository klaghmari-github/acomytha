"""Console admin : comptes et alertes appareil."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from sentier.api.deps import AuthContext, get_db, require_roles
from sentier.models import DeviceAlert, DeviceBinding, User

router = APIRouter(prefix="/api/admin", tags=["admin"])


class NewParent(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)
    display_name: str
    child_pin: str = Field(min_length=4, max_length=8)


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
            "parent_id": u.parent_id,
            "is_active": u.is_active,
            "device_id": bindings[u.id].device_id if u.id in bindings else None,
            "device_bound_at": bindings[u.id].bound_at.isoformat() if u.id in bindings else None,
        }
        for u in rows
    ]


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
    from sentier.models import Chunk, Story

    return {
        "users": db.query(User).count(),
        "stories": db.query(Story).count(),
        "chunks": db.query(Chunk).count(),
        "alerts_open": db.query(DeviceAlert).filter(DeviceAlert.acknowledged.is_(False)).count(),
        "with_audio": db.query(Story).filter(Story.has_audio.is_(True)).count(),
    }
