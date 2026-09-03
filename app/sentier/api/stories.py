"""Catalogue, filtres, forêt parentale."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from sentier.api.deps import AuthContext, get_db, require_roles
from sentier.catalog import list_stories, story_to_dict
from sentier.graph import StoryGraph
from sentier.models import Chunk, ForestEntry, Lesson, Story

router = APIRouter(prefix="/api", tags=["stories"])


class ForestBody(BaseModel):
    story_ids: list[str]


@router.get("/lessons")
def lessons(_auth: AuthContext = Depends(require_roles("admin", "parent")), db: Session = Depends(get_db)):
    rows = list(db.scalars(select(Lesson).order_by(Lesson.domain_id, Lesson.lesson_id)))
    return [
        {
            "lesson_id": r.lesson_id,
            "title": r.title,
            "domain_id": r.domain_id,
            "domain": r.domain,
            "subdomain": r.subdomain,
            "framing": r.framing,
            "objective": r.objective,
        }
        for r in rows
    ]


@router.get("/stories")
def stories(
    q: str = "",
    domain: str = "",
    age_band: str = "",
    kind: str = "",
    _auth: AuthContext = Depends(require_roles("admin", "parent")),
    db: Session = Depends(get_db),
):
    return [story_to_dict(s) for s in list_stories(db, q=q, domain=domain, age_band=age_band, kind=kind)]


@router.get("/stories/{story_id}")
def story_detail(story_id: str, auth: AuthContext = Depends(require_roles("admin", "parent")), db: Session = Depends(get_db)):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    chunks = list(db.scalars(select(Chunk).where(Chunk.story_id == story_id)))
    graph = StoryGraph(chunks).as_client_dict(include_text=auth.role in {"admin", "parent"})
    payload = story_to_dict(story)
    payload["graph"] = graph
    return payload


@router.get("/parent/forest")
def get_forest(auth: AuthContext = Depends(require_roles("parent", "admin")), db: Session = Depends(get_db)):
    if auth.role == "admin":
        return [story_to_dict(s) for s in db.scalars(select(Story).where(Story.has_audio.is_(True)))]
    ids = list(db.scalars(select(ForestEntry.story_id).where(ForestEntry.parent_id == auth.parent_id)))
    if not ids:
        return []
    rows = list(db.scalars(select(Story).where(Story.story_id.in_(ids))))
    return [story_to_dict(s) for s in rows]


@router.put("/parent/forest")
def put_forest(body: ForestBody, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    db.query(ForestEntry).filter(ForestEntry.parent_id == auth.parent_id).delete()
    for sid in body.story_ids:
        if db.get(Story, sid) is None:
            raise HTTPException(404, f"histoire inconnue: {sid}")
        db.add(ForestEntry(parent_id=auth.parent_id, story_id=sid))
    db.commit()
    return {"ok": True, "count": len(body.story_ids)}


@router.get("/enfant/file")
def child_queue(auth: AuthContext = Depends(require_roles("child")), db: Session = Depends(get_db)):
    ids = list(db.scalars(select(ForestEntry.story_id).where(ForestEntry.parent_id == auth.parent_id)))
    if not ids:
        return []
    rows = list(db.scalars(select(Story).where(Story.story_id.in_(ids))))
    return [story_to_dict(s) for s in rows]
