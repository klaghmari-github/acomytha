"""Éditeur vocal : JSON, empreintes, conversion, répliques. Admin seulement."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from acomytha.api.deps import AuthContext, require_roles

router = APIRouter(prefix="/api/editor", tags=["editor"])
LOG = logging.getLogger("acomytha.editor")


def get_tts(request: Request):
    tts = getattr(request.app.state, "tts", None)
    if tts is None:
        raise HTTPException(503, "Moteur TTS indisponible.")
    return tts


def _http(exc: Exception, not_found: int = 404):
    if isinstance(exc, FileNotFoundError):
        raise HTTPException(not_found, str(exc))
    if isinstance(exc, RuntimeError):
        raise HTTPException(409, str(exc))
    if isinstance(exc, ValueError):
        raise HTTPException(400, str(exc))
    LOG.exception("éditeur TTS")
    raise HTTPException(400, str(exc))


@router.get("/roster")
def roster(_auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    return tts.roster_public()


@router.get("/stories")
def stories(_auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    return tts.list_stories()


@router.get("/stories/{story_id}")
def story(story_id: str, _auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    try:
        return tts.preview(story_id=story_id)
    except Exception as exc:
        _http(exc)


@router.post("/parse")
async def parse_story(
    request: Request,
    _auth: AuthContext = Depends(require_roles("admin", "editor")),
    tts=Depends(get_tts),
):
    story_id = ""
    filename = None
    payload = None
    ctype = request.headers.get("content-type") or ""
    if "application/json" in ctype:
        body = await request.json()
        story_id = str((body or {}).get("story_id") or "").strip()
    else:
        form = await request.form()
        story_id = str(form.get("story_id") or "").strip()
        upload = form.get("file")
        if upload is not None and getattr(upload, "filename", None):
            filename = upload.filename
            payload = await upload.read()
    try:
        if story_id:
            return tts.preview(story_id=story_id)
        return tts.preview(filename=filename, payload=payload)
    except Exception as exc:
        _http(exc)


@router.get("/voices")
def voices(_auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    return tts.voices_public()


@router.get("/voices/presets")
def presets(_auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    return tts.presets()


@router.post("/voices/generate")
async def generate_voice(
    request: Request,
    _auth: AuthContext = Depends(require_roles("admin", "editor")),
    tts=Depends(get_tts),
):
    data = await request.json()
    profile_id = str(data.get("id") or "").strip()
    name = str(data.get("display_name") or "").strip()
    if not profile_id or not name:
        raise HTTPException(400, "Nom et identifiant requis.")
    return tts.generate_voice(
        profile_id=profile_id,
        display_name=name,
        gender=str(data.get("gender") or "female"),
        age_group=str(data.get("age_group") or "adult"),
        temperament=str(data.get("temperament") or "naturel"),
        role=str(data.get("role") or "character"),
    )


@router.get("/voices/jobs/{job_id}")
def voice_job(job_id: str, _auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    payload = tts.voice_job(job_id)
    if payload is None:
        raise HTTPException(404, "Travail vocal introuvable.")
    return payload


@router.post("/voices/record")
async def record_voice(
    file: UploadFile = File(...),
    id: str = Form(...),
    display_name: str = Form(...),
    gender: str = Form("female"),
    age_group: str = Form("adult"),
    role: str = Form("character"),
    temperament: str = Form("naturel"),
    _auth: AuthContext = Depends(require_roles("admin", "editor")),
    tts=Depends(get_tts),
):
    class _Upload:
        filename = file.filename

        def save(self, path: Path) -> None:
            path.write_bytes(_Upload._data)

    _Upload._data = await file.read()
    try:
        raw = tts.stash_upload(f"rec-{id.replace('.', '_')}", _Upload())
        return tts.record_voice(
            raw,
            profile_id=id.strip(),
            display_name=display_name.strip(),
            gender=gender,
            age_group=age_group,
            role=role,
            temperament=temperament,
        )
    except Exception as exc:
        _http(exc)


@router.post("/convert")
async def convert_story(
    request: Request,
    _auth: AuthContext = Depends(require_roles("admin", "editor")),
    tts=Depends(get_tts),
):
    ctype = request.headers.get("content-type") or ""
    story_id = ""
    assignments: dict = {}
    filename = None
    payload = None
    try:
        if "application/json" in ctype:
            body = await request.json()
            story_id = str((body or {}).get("story_id") or "").strip()
            assignments = dict((body or {}).get("assignments") or {})
        else:
            form = await request.form()
            story_id = str(form.get("story_id") or "").strip()
            raw = form.get("assignments") or "{}"
            assignments = json.loads(str(raw))
            upload = form.get("file")
            if upload is not None and getattr(upload, "filename", None):
                filename = upload.filename
                payload = await upload.read()
        if not isinstance(assignments, dict):
            raise ValueError("assignments invalides")
        return tts.convert(story_id or None, assignments, filename=filename, payload=payload)
    except Exception as exc:
        _http(exc)


@router.post("/excel")
def convert_excel(_auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    try:
        return tts.convert_excel()
    except Exception as exc:
        _http(exc)


@router.get("/jobs/{job_id}")
def job_status(job_id: str, _auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    job = tts.job(job_id)
    if job is None:
        raise HTTPException(404, "Travail introuvable.")
    return job.public()


@router.get("/jobs/{job_id}/audio")
def job_audio(job_id: str, _auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    job = tts.job(job_id)
    if job is None:
        raise HTTPException(404, "Travail introuvable.")
    if job.status != "done" or job.wav is None:
        raise HTTPException(409, "L'audio n'est pas encore prêt.")
    return FileResponse(job.wav, media_type="audio/wav", filename="histoire.wav")


@router.get("/jobs/{job_id}/edit")
def job_edit(job_id: str, _auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    try:
        return tts.edit_public(job_id)
    except Exception as exc:
        _http(exc)


@router.get("/jobs/{job_id}/replicas/{index}/audio")
def replica_audio(
    job_id: str,
    index: int,
    _auth: AuthContext = Depends(require_roles("admin", "editor")),
    tts=Depends(get_tts),
):
    try:
        tts.edit_public(job_id)
    except Exception as exc:
        _http(exc)
    path = tts.replica_path(job_id, index)
    if not path.is_file():
        raise HTTPException(404, f"Réplique {index} introuvable.")
    return FileResponse(path, media_type="audio/wav", filename=f"replique-{index:04d}.wav")


@router.post("/jobs/{job_id}/replicas/regenerate")
async def regenerate_replicas(
    job_id: str,
    request: Request,
    _auth: AuthContext = Depends(require_roles("admin", "editor")),
    tts=Depends(get_tts),
):
    data = await request.json()
    try:
        indices = sorted({int(item) for item in (data.get("indices") or [])})
        return tts.regenerate_replicas(job_id, indices)
    except Exception as exc:
        _http(exc)


@router.post("/jobs/{job_id}/replicas/{index}/record")
async def record_replica(
    job_id: str,
    index: int,
    file: UploadFile = File(...),
    _auth: AuthContext = Depends(require_roles("admin", "editor")),
    tts=Depends(get_tts),
):
    class _Upload:
        filename = file.filename

        def save(self, path: Path) -> None:
            path.write_bytes(_Upload._data)

    _Upload._data = await file.read()
    try:
        raw = tts.stash_upload(f"line-{job_id}-{index}", _Upload())
        return tts.record_replica(job_id, index, raw)
    except Exception as exc:
        _http(exc)


@router.get("/edits/{edit_id}")
def edit_status(edit_id: str, _auth: AuthContext = Depends(require_roles("admin", "editor")), tts=Depends(get_tts)):
    payload = tts.edit_work(edit_id)
    if payload is None:
        raise HTTPException(404, "Édition introuvable.")
    return payload
