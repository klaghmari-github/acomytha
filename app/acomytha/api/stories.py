"""Catalogue, filtres, forêt parentale."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone

from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from acomytha.api.deps import AuthContext, get_db, require_roles
from acomytha.catalog import list_stories, story_to_dict
from acomytha.commerce import num, owned_ids
from acomytha.graph import StoryGraph
from acomytha.models import ChildCatalogEntry, ChildProfile, Chunk, ForestEntry, Lesson, ListeningSession, SessionToken, Story

router = APIRouter(prefix="/api", tags=["stories"])


class ForestBody(BaseModel):
    story_ids: list[str]


class ChildProfileBody(BaseModel):
    display_name: str = Field(min_length=1, max_length=80)
    age_band: str = Field(default="N1", pattern=r"^N[123]$")
    color: str = Field(default="violet", max_length=16)


class ListeningEndBody(BaseModel):
    listened_seconds: float = Field(default=0, ge=0, le=86400)


def _profile_payload(profile: ChildProfile, db: Session) -> dict:
    count = db.query(ChildCatalogEntry).filter(ChildCatalogEntry.profile_id == profile.id).count()
    return {
        "id": profile.id,
        "display_name": profile.display_name,
        "age_band": profile.age_band,
        "color": profile.color,
        "story_count": count,
    }


def _owned_story_ids(db: Session, parent_id: int, story_ids: list[str]) -> list[str]:
    owned = owned_ids(db, parent_id)
    unique = list(dict.fromkeys(story_ids))
    missing = [story_id for story_id in unique if story_id not in owned]
    if missing:
        raise HTTPException(403, f"histoire non acquise: {missing[0]}")
    return unique


@router.get("/parent/profiles")
def child_profiles(auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    rows = db.query(ChildProfile).filter(ChildProfile.parent_id == auth.parent_id).order_by(ChildProfile.created_at).all()
    return {
        "items": [_profile_payload(profile, db) for profile in rows],
        "limit": max(1, min(int(num(db, "max_child_profiles") or 10), 20)),
    }


@router.post("/parent/profiles")
def create_child_profile(body: ChildProfileBody, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    limit = max(1, min(int(num(db, "max_child_profiles") or 10), 20))
    count = db.query(ChildProfile).filter(ChildProfile.parent_id == auth.parent_id).count()
    if count >= limit:
        raise HTTPException(409, f"limite de {limit} profils atteinte")
    profile = ChildProfile(
        parent_id=auth.parent_id,
        display_name=body.display_name.strip(),
        age_band=body.age_band,
        color=body.color,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return _profile_payload(profile, db)


@router.put("/parent/profiles/{profile_id}")
def update_child_profile(profile_id: int, body: ChildProfileBody, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    profile = db.query(ChildProfile).filter(ChildProfile.id == profile_id, ChildProfile.parent_id == auth.parent_id).one_or_none()
    if profile is None:
        raise HTTPException(404, "profil enfant introuvable")
    profile.display_name = body.display_name.strip()
    profile.age_band = body.age_band
    profile.color = body.color
    db.commit()
    return _profile_payload(profile, db)


@router.delete("/parent/profiles/{profile_id}")
def delete_child_profile(profile_id: int, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    profiles = db.query(ChildProfile).filter(ChildProfile.parent_id == auth.parent_id).all()
    profile = next((item for item in profiles if item.id == profile_id), None)
    if profile is None:
        raise HTTPException(404, "profil enfant introuvable")
    if len(profiles) <= 1:
        raise HTTPException(409, "un foyer doit conserver au moins un profil enfant")
    db.query(SessionToken).filter(SessionToken.child_profile_id == profile.id).delete()
    db.delete(profile)
    db.commit()
    return {"ok": True}


@router.get("/parent/profiles/{profile_id}/catalog")
def profile_catalog(profile_id: int, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    profile = db.query(ChildProfile).filter(ChildProfile.id == profile_id, ChildProfile.parent_id == auth.parent_id).one_or_none()
    if profile is None:
        raise HTTPException(404, "profil enfant introuvable")
    ids = list(db.scalars(select(ChildCatalogEntry.story_id).where(ChildCatalogEntry.profile_id == profile.id)))
    return {"profile": _profile_payload(profile, db), "story_ids": ids}


@router.put("/parent/profiles/{profile_id}/catalog")
def put_profile_catalog(profile_id: int, body: ForestBody, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    profile = db.query(ChildProfile).filter(ChildProfile.id == profile_id, ChildProfile.parent_id == auth.parent_id).one_or_none()
    if profile is None:
        raise HTTPException(404, "profil enfant introuvable")
    story_ids = _owned_story_ids(db, auth.parent_id, body.story_ids)
    db.query(ChildCatalogEntry).filter(ChildCatalogEntry.profile_id == profile.id).delete()
    for story_id in story_ids:
        db.add(ChildCatalogEntry(profile_id=profile.id, story_id=story_id))
    db.commit()
    return {"ok": True, "count": len(story_ids)}


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
    ids = list(db.scalars(select(ChildCatalogEntry.story_id).where(ChildCatalogEntry.profile_id == auth.child_profile_id)))
    allowed = owned_ids(db, auth.parent_id)
    ids = [i for i in ids if i in allowed]
    if not ids:
        return []
    counts = dict(db.execute(
        select(ListeningSession.story_id, func.count(ListeningSession.id))
        .where(ListeningSession.profile_id == auth.child_profile_id)
        .group_by(ListeningSession.story_id)
    ).all())
    rows = list(db.scalars(select(Story).where(Story.story_id.in_(ids))))
    rows.sort(key=lambda story: (counts.get(story.story_id, 0), story.title.casefold()))
    return [story_to_dict(s) for s in rows]


@router.post("/enfant/ecoutes/{story_id}")
def start_listening(story_id: str, auth: AuthContext = Depends(require_roles("child")), db: Session = Depends(get_db)):
    allowed = db.query(ChildCatalogEntry).filter(
        ChildCatalogEntry.profile_id == auth.child_profile_id,
        ChildCatalogEntry.story_id == story_id,
    ).one_or_none()
    if allowed is None:
        raise HTTPException(403, "histoire absente du catalogue enfant")
    row = ListeningSession(profile_id=auth.child_profile_id, story_id=story_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"listening_id": row.id, "started_at": row.started_at.isoformat()}


@router.put("/enfant/ecoutes/{listening_id}")
def finish_listening(listening_id: int, body: ListeningEndBody, auth: AuthContext = Depends(require_roles("child")), db: Session = Depends(get_db)):
    row = db.query(ListeningSession).filter(
        ListeningSession.id == listening_id,
        ListeningSession.profile_id == auth.child_profile_id,
    ).one_or_none()
    if row is None:
        raise HTTPException(404, "écoute inconnue")
    story = db.get(Story, row.story_id)
    duration = max(0, int(story.duration_s if story else 0))
    heard = max(0.0, float(body.listened_seconds))
    percent = min(100.0, heard / duration * 100) if duration else 0.0
    row.ended_at = datetime.now(timezone.utc)
    row.listened_seconds = heard
    row.completion_percent = round(percent, 2)
    row.completed = percent >= 95
    db.commit()
    return {"ok": True, "completion_percent": row.completion_percent, "completed": row.completed}


@router.get("/parent/profiles/{profile_id}/ecoutes")
def listening_history(profile_id: int, auth: AuthContext = Depends(require_roles("parent")), db: Session = Depends(get_db)):
    profile = db.query(ChildProfile).filter(ChildProfile.id == profile_id, ChildProfile.parent_id == auth.parent_id).one_or_none()
    if profile is None:
        raise HTTPException(404, "profil enfant introuvable")
    rows = db.query(ListeningSession).filter(ListeningSession.profile_id == profile_id).order_by(ListeningSession.started_at.desc()).limit(500).all()
    return [{"id": row.id, "story_id": row.story_id, "started_at": row.started_at.isoformat(), "ended_at": row.ended_at.isoformat() if row.ended_at else None, "listened_seconds": row.listened_seconds, "completion_percent": row.completion_percent, "completed": row.completed} for row in rows]
