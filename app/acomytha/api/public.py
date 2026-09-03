"""Catalogue, stats et aperçu sans compte."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from acomytha.api.deps import get_db
from acomytha.catalog import list_stories, story_to_dict
from acomytha.commerce import num
from acomytha.graph import StoryGraph
from acomytha.models import Chunk, Lesson, Story, StoryIdea

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
        "preview_seconds": int(num(db, "preview_seconds") or 10),
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
    db: Session = Depends(get_db),
):
    return [story_to_dict(s) for s in list_stories(db, q=q, domain=domain, age_band=age_band, kind=kind)]


@router.get("/preview/{story_id}/graph")
def preview_graph(story_id: str, request: Request, db: Session = Depends(get_db)):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    chunks = list(db.scalars(select(Chunk).where(Chunk.story_id == story_id)))
    graph = StoryGraph(chunks).as_client_dict(include_text=False)
    root = graph["root"]
    node = dict(graph["chunks"].get(root) or {})
    node["default_next"] = None
    node["options"] = []
    return {
        "story_id": story.story_id,
        "title": story.title,
        "root": root,
        "preview_seconds": int(num(db, "preview_seconds") or 10),
        "has_audio": story.has_audio,
        "key": request.app.state.vault.story_key_b64(story_id) if story.has_audio else "",
        "chunks": {root: node} if root else {},
    }


@router.get("/preview/{story_id}/chunk/{chunk_id}")
def preview_chunk(story_id: str, chunk_id: str, request: Request, db: Session = Depends(get_db)):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    chunks = list(db.scalars(select(Chunk).where(Chunk.story_id == story_id)))
    root = StoryGraph(chunks).root
    if chunk_id != root:
        raise HTTPException(403, "aperçu : premier passage seulement")
    try:
        path = request.app.state.vault.ensure_chk(story_id, chunk_id)
    except FileNotFoundError as exc:
        raise HTTPException(404, "audio encore absent") from exc
    return Response(content=path.read_bytes(), media_type="application/octet-stream", headers={"Cache-Control": "no-store"})


@router.post("/ideas")
def ideas(body: IdeaBody, db: Session = Depends(get_db)):
    db.add(StoryIdea(email=body.email.strip()[:180], text=body.text.strip()))
    db.commit()
    return {"ok": True}
