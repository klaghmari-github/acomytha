"""Boutique : solde A, achats, commandes, voix. Stripe plus tard."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from acomytha.api.deps import AuthContext, get_db, require_roles
from acomytha.commerce import (
    debit,
    eur_to_a,
    free_ids,
    fx_rate,
    get_wallet,
    num,
    owned_ids,
    params,
    price_for,
)
from acomytha.models import ForestEntry, Purchase, Story, StoryOrder, VoiceProfile

router = APIRouter(prefix="/api/shop", tags=["shop"])


class BuyBody(BaseModel):
    story_id: str


class OrderBody(BaseModel):
    context: str = Field(min_length=8, max_length=4000)
    ramifications: int = Field(default=0, ge=0, le=3)


class RechargeBody(BaseModel):
    eur: float = Field(gt=0, le=500)


def _parent(auth: AuthContext) -> int:
    return auth.parent_id


def _wallet_payload(db: Session, parent_id: int) -> dict:
    p = params(db)
    w = get_wallet(db, parent_id)
    return {
        "balance_a": w.balance_a,
        "lifetime_eur": w.lifetime_eur,
        "owned": sorted(owned_ids(db, parent_id)),
        "free": sorted(free_ids(db)),
        "prices": {
            "story": num(db, "price_story_a"),
            "tree": num(db, "price_tree_a"),
            "order": num(db, "price_order_a"),
            "ramification": num(db, "price_ramification_a"),
            "voice": num(db, "price_voice_record_a"),
            "voice_apply_all": num(db, "price_voice_apply_all_a"),
        },
        "preview_seconds": int(num(db, "preview_seconds") or 10),
        "pack": {"count": int(num(db, "pack_trees_count") or 10), "eur": num(db, "pack_trees_eur")},
        "fx": {
            "start": float(p["fx_rate_start"]),
            "step": float(p["fx_rate_step"]),
            "every": float(p["fx_rate_every_eur"]),
            "max": float(p["fx_rate_max"]),
        },
        "stripe": "planned",
    }


@router.get("/wallet")
def wallet(auth: AuthContext = Depends(require_roles("parent", "admin")), db: Session = Depends(get_db)):
    if auth.role == "admin":
        return {"balance_a": 0, "owned": [], "free": sorted(free_ids(db)), "prices": {}, "stripe": "planned"}
    return _wallet_payload(db, _parent(auth))


@router.post("/buy")
def buy(body: BuyBody, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    pid = _parent(auth)
    story = db.get(Story, body.story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    if body.story_id in owned_ids(db, pid):
        return _wallet_payload(db, pid)
    price = price_for(story, db)
    kind = "tree" if story.kind == "ramifiee" else "story"
    try:
        debit(db, pid, price, kind="buy", ref=story.story_id, note=story.title)
    except ValueError:
        raise HTTPException(402, "solde insuffisant") from None
    db.add(Purchase(parent_id=pid, item_type=kind, item_id=story.story_id, price_a=price))
    if not db.query(ForestEntry).filter(ForestEntry.parent_id == pid, ForestEntry.story_id == story.story_id).one_or_none():
        db.add(ForestEntry(parent_id=pid, story_id=story.story_id))
    db.commit()
    return _wallet_payload(db, pid)


@router.post("/order")
def order(body: OrderBody, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    pid = _parent(auth)
    max_r = int(num(db, "max_ramifications") or 3)
    ram = min(max(body.ramifications, 0), max_r)
    price = num(db, "price_order_a") + ram * num(db, "price_ramification_a")
    try:
        debit(db, pid, price, kind="order", note=body.context[:80])
    except ValueError:
        raise HTTPException(402, "solde insuffisant") from None
    row = StoryOrder(parent_id=pid, context=body.context.strip(), ramifications=ram, price_a=price)
    db.add(row)
    db.commit()
    out = _wallet_payload(db, pid)
    out["order_id"] = row.id
    return out


@router.post("/recharge")
def recharge(body: RechargeBody, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    p = params(db)
    a = eur_to_a(body.eur, p)
    return {
        "stripe": "planned",
        "eur": body.eur,
        "rate": fx_rate(body.eur, p),
        "would_credit_a": a,
        "message": "Le paiement arrivera bientôt.",
    }


@router.post("/voice")
async def voice(
    request: Request,
    role: str = Form("narrateur"),
    file: UploadFile | None = File(None),
    auth: AuthContext = Depends(require_roles("parent")),
    db: Session = Depends(get_db),
):
    pid = _parent(auth)
    price = num(db, "price_voice_record_a")
    try:
        debit(db, pid, price, kind="voice", note=role)
    except ValueError:
        raise HTTPException(402, "solde insuffisant") from None
    dest = ""
    if file is not None:
        folder = Path(request.app.state.settings.data_dir) / "voices" / str(pid)
        folder.mkdir(parents=True, exist_ok=True)
        dest = str(folder / f"{role}-{file.filename or 'voix.webm'}")
        Path(dest).write_bytes(await file.read())
    row = VoiceProfile(parent_id=pid, role=role.strip()[:32], path=dest)
    db.add(row)
    db.commit()
    out = _wallet_payload(db, pid)
    out["voice_id"] = row.id
    return out


@router.post("/voice/{voice_id}/apply-all")
def apply_all(voice_id: int, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    pid = _parent(auth)
    row = db.get(VoiceProfile, voice_id)
    if row is None or row.parent_id != pid:
        raise HTTPException(404, "voix inconnue")
    if not row.applied_all:
        try:
            debit(db, pid, num(db, "price_voice_apply_all_a"), kind="voice_all", ref=str(voice_id))
        except ValueError:
            raise HTTPException(402, "solde insuffisant") from None
        row.applied_all = True
        db.commit()
    return _wallet_payload(db, pid)


@router.get("/voices")
def voices(auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    rows = db.query(VoiceProfile).filter(VoiceProfile.parent_id == _parent(auth)).all()
    return [{"id": r.id, "role": r.role, "applied_all": r.applied_all} for r in rows]


@router.get("/orders")
def orders(auth: AuthContext = Depends(require_roles("parent", "admin")), db: Session = Depends(get_db)):
    q = db.query(StoryOrder)
    if auth.role == "parent":
        q = q.filter(StoryOrder.parent_id == _parent(auth))
    rows = q.order_by(StoryOrder.created_at.desc()).limit(50).all()
    return [
        {"id": r.id, "context": r.context, "ramifications": r.ramifications, "price_a": r.price_a, "status": r.status}
        for r in rows
    ]
