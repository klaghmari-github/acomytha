"""File de conversion et d'édition des répliques."""

from __future__ import annotations

import tempfile
import threading
import uuid
from pathlib import Path
from typing import Any

from .catalogue import CharacterCatalogue
from .edit import ReplicaBook
from .models import ParsedStory
from .settings import Settings


class ConversionJob:
    def __init__(self, job_id: str, title: str, segments: int) -> None:
        self.id = job_id
        self.status = "queued"
        self.message = "En file d'attente…"
        self.title = title
        self.segments = segments
        self.progress = 0
        self.wav: Path | None = None
        self.edit: dict[str, Any] | None = None
        self.assignments: dict[str, str] = {}

    def public(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "job_id": self.id,
            "status": self.status,
            "message": self.message,
            "title": self.title,
            "segments": self.segments,
            "progress": self.progress,
        }
        if self.edit:
            replicas = self.edit.get("replicas") or []
            payload["replica_count"] = len(replicas)
            payload["speakers"] = [
                {
                    "key": key,
                    "display_name": meta.get("display_name") or key,
                    "role": meta.get("role") or "character",
                    "count": sum(1 for row in replicas if row.get("speaker") == key),
                }
                for key, meta in (self.edit.get("speakers") or {}).items()
            ]
        return payload


class EditWork:
    def __init__(self, kind: str, job_id: str, label: str) -> None:
        self.id = uuid.uuid4().hex[:12]
        self.kind = kind
        self.job_id = job_id
        self.label = label
        self.status = "queued"
        self.progress = 0
        self.message = "En file d'attente…"

    def public(self) -> dict[str, Any]:
        return {
            "edit_id": self.id,
            "job_id": self.job_id,
            "kind": self.kind,
            "label": self.label,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
        }


class ConversionQueue:
    """File unique : rendu d'histoire, régénération de répliques, Kokoro partagé."""

    def __init__(self, settings: Settings, catalogue: CharacterCatalogue) -> None:
        self.settings = settings
        self.catalogue = catalogue
        self.book = ReplicaBook(settings, catalogue)
        self._jobs: dict[str, ConversionJob] = {}
        self._edits: dict[str, EditWork] = {}
        self._lock = threading.Lock()
        self._engine_lock = threading.Lock()
        self._kokoro = None
        self._cloner = None

    def kokoro(self):
        from acomytha_tts import KokoroSynthesizer

        if self._kokoro is None:
            self._kokoro = KokoroSynthesizer()
        return self._kokoro

    def cloner(self):
        from acomytha_tts import OpenVoiceCloner

        if self._cloner is None:
            self._cloner = OpenVoiceCloner(self.settings.checkpoints, "cpu")
        return self._cloner

    def get(self, job_id: str) -> ConversionJob | None:
        job = self._jobs.get(job_id)
        if job is not None:
            return job
        return self._load_job(job_id)

    def get_edit(self, edit_id: str) -> EditWork | None:
        return self._edits.get(edit_id)

    def _load_job(self, job_id: str) -> ConversionJob | None:
        edit = self.book.load(job_id)
        wav = self.book.folder(job_id) / "histoire.wav"
        if not edit or not wav.is_file():
            return None
        job = ConversionJob(job_id, str(edit.get("title") or "Histoire"), len(edit.get("replicas") or []))
        job.status = "done"
        job.progress = 100
        job.message = "Audio prêt."
        job.wav = wav
        job.edit = edit
        job.assignments = {str(k): str(v) for k, v in (edit.get("assignments") or {}).items()}
        self._jobs[job_id] = job
        return job

    def submit(self, story: ParsedStory, assignments: dict[str, str]) -> ConversionJob:
        job = ConversionJob(uuid.uuid4().hex[:12], story.title, len(story.segments))
        self._jobs[job.id] = job
        thread = threading.Thread(target=self._run, args=(job, story, assignments), daemon=True)
        thread.start()
        return job

    def _build_story(self, parsed: ParsedStory, assignments: dict[str, str]):
        from acomytha_tts import Speaker, Story, StoryLoader

        speakers: dict[str, Speaker] = {}
        needs_clone = False
        for key in parsed.speaker_keys:
            profile_id = assignments.get(key) or key
            profile = self.catalogue.get(profile_id)
            if profile is None:
                speakers[key] = Speaker(key)
                continue
            audio = profile.audio_path(self.settings.root)
            if audio and audio.is_file():
                needs_clone = True
            else:
                audio = None
            speakers[key] = Speaker(
                name=key,
                kokoro_voice=profile.kokoro_voice,
                reference_audio=audio,
                fingerprint_speed=profile.fingerprint.speed,
                fingerprint_pitch=profile.fingerprint.pitch_semitones,
                fingerprint_gain=profile.fingerprint.gain_db,
            )
        scenario = {"title": parsed.title, "speakers": {k: {} for k in speakers}, "segments": parsed.segments}
        loaded = StoryLoader().load_dict(scenario, self.settings.root, parsed.title)
        merged = dict(loaded.speakers)
        merged.update(speakers)
        return Story(loaded.title, merged, loaded.segments), needs_clone

    def _parsed_from_disk(self, job_id: str) -> tuple[ParsedStory, dict[str, str]]:
        raw = self.book.load_scenario(job_id)
        if not raw:
            raise FileNotFoundError("Scénario de répliques introuvable.")
        assignments = {str(k): str(v) for k, v in (raw.get("assignments") or {}).items()}
        segments = list(raw.get("segments") or [])
        parsed = ParsedStory(
            title=str(raw.get("title") or "Histoire"),
            format="edit",
            speaker_keys=list(raw.get("speaker_keys") or []),
            segments=segments,
        )
        return parsed, assignments

    def _run(self, job: ConversionJob, parsed: ParsedStory, assignments: dict[str, str]) -> None:
        try:
            job.status = "running"
            job.message = "Préparation des voix…"
            job.assignments = assignments
            self.book.save_scenario(job.id, parsed.title, parsed.speaker_keys, parsed.segments, assignments)
            story, needs_clone = self._build_story(parsed, assignments)
            job.progress = 8
            job.message = f"Synthèse de {len(story.segments)} réplique(s)…"
            wav_path = self.settings.jobs_dir / job.id / "histoire.wav"

            def on_progress(index: int, total: int, name: str) -> None:
                job.progress = 8 + int(90 * index / max(total, 1))
                job.message = f"Réplique {index}/{total} — {name}"

            def on_replica(index: int, _segment, audio) -> None:
                self.book.write_replica(job.id, index, audio)

            with self._engine_lock:
                from acomytha_tts import ProsodyProcessor, StoryRenderer

                cloner = self.cloner() if needs_clone else None
                StoryRenderer(self.kokoro(), ProsodyProcessor(), cloner).render(
                    story, wav_path, on_progress=on_progress, on_replica=on_replica
                )
            job.edit = self.book.capture(job.id, story, assignments)
            job.wav = self.book.assemble(job.id)
            job.progress = 100
            job.status = "done"
            job.message = "Audio prêt."
        except Exception as exc:
            job.status = "error"
            job.message = str(exc)

    def edit_public(self, job: ConversionJob) -> dict[str, Any]:
        edit = job.edit or self.book.load(job.id)
        if not edit:
            raise FileNotFoundError("Livre de répliques introuvable.")
        replicas = []
        for row in edit.get("replicas") or []:
            item = dict(row)
            index = int(item.get("index") or 0)
            item["audio_url"] = f"{self.settings.api_prefix}/jobs/{job.id}/replicas/{index}/audio"
            replicas.append(item)
        speakers = []
        for key, meta in (edit.get("speakers") or {}).items():
            speakers.append(
                {
                    "key": key,
                    "profile_id": meta.get("profile_id") or key,
                    "display_name": meta.get("display_name") or key,
                    "role": meta.get("role") or "character",
                    "count": sum(1 for row in replicas if row.get("speaker") == key),
                }
            )
        return {
            "job_id": job.id,
            "title": job.title,
            "status": job.status,
            "audio_url": f"{self.settings.api_prefix}/jobs/{job.id}/audio",
            "speakers": speakers,
            "replicas": replicas,
        }

    def submit_regenerate(self, job: ConversionJob, indices: list[int]) -> EditWork:
        work = EditWork("regenerate", job.id, f"{len(indices)} réplique(s)")
        self._edits[work.id] = work
        threading.Thread(target=self._run_regenerate, args=(work, job, indices), daemon=True).start()
        return work

    def _run_regenerate(self, work: EditWork, job: ConversionJob, indices: list[int]) -> None:
        try:
            work.status = "running"
            parsed, assignments = self._parsed_from_disk(job.id)
            story, needs_clone = self._build_story(parsed, assignments)
            total = max(len(indices), 1)
            work.message = f"Régénération de {len(indices)} réplique(s)…"
            with self._engine_lock:
                from acomytha_tts import ProsodyProcessor, StoryRenderer

                cloner = self.cloner() if needs_clone else None
                renderer = StoryRenderer(self.kokoro(), ProsodyProcessor(), cloner)
                with tempfile.TemporaryDirectory(prefix="acomytha_edit_") as tmp:
                    temp_dir = Path(tmp)
                    for step, index in enumerate(indices, start=1):
                        if index < 1 or index > len(story.segments):
                            raise ValueError(f"Réplique {index} hors limites.")
                        segment = story.segments[index - 1]
                        work.progress = int(90 * step / total)
                        work.message = f"Réplique {index} — {segment.speaker} ({step}/{len(indices)})"
                        audio = renderer.synthesize_segment(story, segment, index, temp_dir)
                        self.book.write_replica(job.id, index, audio)
                        self.book.mark_source(job.id, index, "tts")
            job.edit = self.book.capture(job.id, story, assignments)
            job.wav = self.book.assemble(job.id)
            work.progress = 100
            work.status = "done"
            work.message = "Répliques mises à jour."
        except Exception as exc:
            work.status = "error"
            work.message = str(exc)

    def replace_recorded(self, job: ConversionJob, index: int, upload: Path) -> dict[str, Any]:
        dest = self.book.replica_path(job.id, index)
        self.book.transcode(upload, dest)
        job.edit = self.book.mark_source(job.id, index, "record")
        job.wav = self.book.assemble(job.id)
        return self.edit_public(job)
