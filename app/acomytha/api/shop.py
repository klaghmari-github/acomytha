"""Boutique : solde A, achats, commandes, voix, recharge Stripe."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from acomytha.api.deps import AuthContext, get_db, require_roles
from acomytha.commerce import (
    WalletBook,
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
from acomytha.payments import confirm_demo, create_recharge, fulfill_provider

router = APIRouter(prefix="/api/shop", tags=["shop"])


class BuyBody(BaseModel):
    story_id: str


class OrderBody(BaseModel):
    context: str = Field(min_length=8, max_length=4000)
    ramifications: int = Field(default=0, ge=0, le=3)


class RechargeBody(BaseModel):
    eur: float = Field(gt=0, le=500)


class ConfirmBody(BaseModel):
    ref: str = Field(min_length=6, max_length=80)


def _parent(auth: AuthContext) -> int:
    return auth.parent_id


def _wallet_payload(db: Session, parent_id: int) -> dict:
    return WalletBook(db, parent_id).payload()


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
def recharge(
    body: RechargeBody,
    request: Request,
    auth: AuthContext = Depends(require_roles("parent")),
    db: Session = Depends(get_db),
):
    try:
        return create_recharge(db, request.app.state.settings, _parent(auth), body.eur)
    except ValueError:
        raise HTTPException(400, "Choisissez 10, 20, 30, 40 ou 50 €.") from None


@router.post("/recharge/confirm")
def recharge_confirm(
    body: ConfirmBody,
    auth: AuthContext = Depends(require_roles("parent")),
    db: Session = Depends(get_db),
):
    try:
        confirm_demo(db, _parent(auth), body.ref)
    except LookupError:
        raise HTTPException(404, "paiement inconnu") from None
    return _wallet_payload(db, _parent(auth))


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    secret = (params(db).get("stripe_webhook_secret") or request.app.state.settings.stripe_webhook_secret or "").strip()
    if not secret:
        return {"ok": True, "ignored": True}
    try:
        import stripe

        event = stripe.Webhook.construct_event(payload, sig, secret)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(400, "signature") from exc
    if event["type"] == "checkout.session.completed":
        obj = event["data"]["object"]
        fulfill_provider(db, obj.get("id") or "", (obj.get("metadata") or {}).get("ref") or "")
    return {"ok": True}


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
