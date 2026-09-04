"""Graphe de lecture + blobs chiffrés."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from acomytha.api.deps import AuthContext, get_db, require_roles
from acomytha.graph import StoryGraph
from acomytha.commerce import num, owned_ids
from acomytha.models import Chunk, ForestEntry, Story
from acomytha.preview import client_graph, ensure_preview_chk, preview_id

router = APIRouter(prefix="/api/play", tags=["play"])


def _can_play(db: Session, auth: AuthContext, story_id: str) -> Story:
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    if auth.role == "admin":
        return story
    parent_id = auth.parent_id
    in_forest = (
        db.query(ForestEntry)
        .filter(ForestEntry.parent_id == parent_id, ForestEntry.story_id == story_id)
        .one_or_none()
        is not None
    )
    if auth.role == "child" and not in_forest:
        raise HTTPException(403, "cette histoire n'est pas proposée à l'enfant")
    if auth.role in {"parent", "child"} and story_id not in owned_ids(db, parent_id):
        raise HTTPException(402, "aperçu seulement — débloquez l'histoire")
    return story


@router.get("/{story_id}/graph")
def graph(
    story_id: str,
    request: Request,
    auth: AuthContext = Depends(require_roles("admin", "parent", "child")),
    db: Session = Depends(get_db),
):
    story = _can_play(db, auth, story_id)
    chunks = list(db.scalars(select(Chunk).where(Chunk.story_id == story_id)))
    payload = StoryGraph(chunks).as_client_dict(include_text=auth.role in {"admin", "parent"})
    payload["story_id"] = story.story_id
    payload["title"] = story.title
    payload["wait_default_ms"] = story.wait_default_ms
    payload["has_audio"] = story.has_audio
    payload["key"] = request.app.state.vault.story_key_b64(story_id)
    return payload


@router.get("/{story_id}/chunk/{chunk_id}")
def chunk_blob(
    story_id: str,
    chunk_id: str,
    request: Request,
    auth: AuthContext = Depends(require_roles("admin", "parent", "child")),
    db: Session = Depends(get_db),
):
    _can_play(db, auth, story_id)
    chunk = db.query(Chunk).filter(Chunk.story_id == story_id, Chunk.chunk_id == chunk_id).one_or_none()
    if chunk is None:
        raise HTTPException(404, "chunk inconnu")
    try:
        path = request.app.state.vault.ensure_chk(story_id, chunk_id)
    except FileNotFoundError as exc:
        raise HTTPException(404, "audio encore absent pour ce chunk") from exc
    data = path.read_bytes()
    return Response(content=data, media_type="application/octet-stream", headers={"Cache-Control": "no-store"})


@router.get("/{story_id}/preview/graph")
def parent_preview_graph(
    story_id: str,
    request: Request,
    auth: AuthContext = Depends(require_roles("admin", "parent")),
    db: Session = Depends(get_db),
):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    seconds = int(num(db, "parent_preview_seconds") or 30)
    key = request.app.state.vault.story_key_b64(story_id) if story.has_audio else ""
    return client_graph(story, seconds, key)


@router.get("/{story_id}/preview/chunk/{chunk_id}")
def parent_preview_chunk(
    story_id: str,
    chunk_id: str,
    request: Request,
    auth: AuthContext = Depends(require_roles("admin", "parent")),
    db: Session = Depends(get_db),
):
    story = db.get(Story, story_id)
    if story is None:
        raise HTTPException(404, "histoire inconnue")
    seconds = int(num(db, "parent_preview_seconds") or 30)
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
