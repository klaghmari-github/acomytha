"""Catalogue, stats et aperçu sans compte."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from acomytha.api.deps import get_db
from acomytha.catalog import page_stories, related_for, story_to_dict
from acomytha.commerce import num
from acomytha.models import Chunk, Lesson, Story, StoryIdea
from acomytha.preview import client_graph, ensure_preview_chk, preview_id

router = APIRouter(prefix="/api/public", tags=["public"])


class IdeaBody(BaseModel):
    email: str = ""
    text: str = Field(min_length=8, max_length=2000)


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return {
        "stories": db.query(Story).count(),
        "with_audio": db.query(Story).filter(Story.has_audio.is_(True)).count(),
        "themes": db.scalar(select(func.count(func.distinct(Story.domain)))) or 0,
        "ages": ["3–4 ans", "4–5 ans", "5–6 ans"],
        "preview_seconds": int(num(db, "preview_seconds") or 30),
        "price_story_acm": float(num(db, "price_story_a") or 1),
        "price_tree_acm": float(num(db, "price_tree_a") or 1),
        "home_catalog_page_size": max(1, min(int(num(db, "home_catalog_page_size") or 6), 48)),
    }


@router.get("/lessons")
def lessons(db: Session = Depends(get_db)):
    rows = list(db.scalars(select(Lesson).order_by(Lesson.domain_id, Lesson.lesson_id)))
    return [
        {"lesson_id": r.lesson_id, "title": r.title, "domain_id": r.domain_id, "domain": r.domain}
        for r in rows
    ]


@router.get("/stories")
def stories(
    q: str = "",
    domain: str = "",
    age_band: str = "",
    kind: str = "",
    limit: int | None = None,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    page = int(num(db, "home_catalog_page_size") or 6) if limit is None else limit
    rows, total = page_stories(
        db, q=q, domain=domain, age_band=age_band, kind=kind, limit=page, offset=offset
    )
    related = related_for(db, rows)
    items = []
    for s in rows:
        d = story_to_dict(s)
        if s.kind == "ramifiee" and s.lesson_id:
            d["related"] = [r for r in related.get(s.lesson_id, []) if r["story_id"] != s.story_id]
        items.append(d)
    return {"items": items, "total": total, "limit": max(1, min(int(page), 48)), "offset": max(0, offset)}


@router.get("/stories/{story_id}")
def story_one(story_id: str, db: Session = Depends(get_db)):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    d = story_to_dict(story)
    if story.kind == "ramifiee" and story.lesson_id:
        rel = related_for(db, [story])
        d["related"] = [r for r in rel.get(story.lesson_id, []) if r["story_id"] != story.story_id]
    return d


@router.get("/preview/{story_id}/graph")
def preview_graph(story_id: str, request: Request, db: Session = Depends(get_db)):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    seconds = int(num(db, "preview_seconds") or 30)
    key = request.app.state.vault.story_key_b64(story_id) if story.has_audio else ""
    return client_graph(story, seconds, key)


@router.get("/preview/{story_id}/chunk/{chunk_id}")
def preview_chunk(story_id: str, chunk_id: str, request: Request, db: Session = Depends(get_db)):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    seconds = int(num(db, "preview_seconds") or 30)
    if chunk_id != preview_id(seconds):
        raise HTTPException(403, "aperçu seulement")
    chunks = list(db.scalars(select(Chunk).where(Chunk.story_id == story_id)))
    try:
        path = ensure_preview_chk(
            request.app.state.vault, request.app.state.settings, story_id, chunks, seconds
        )
    except FileNotFoundError as exc:
        raise HTTPException(404, "audio encore absent") from exc
    return Response(content=path.read_bytes(), media_type="application/octet-stream", headers={"Cache-Control": "no-store"})


@router.post("/ideas")
def ideas(body: IdeaBody, db: Session = Depends(get_db)):
    db.add(StoryIdea(email=body.email.strip()[:180], text=body.text.strip()))
    db.commit()
    return {"ok": True}
