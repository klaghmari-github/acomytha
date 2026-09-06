"""Livre des répliques : chaque ligne a son WAV, l'histoire se réassemble."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from .catalogue import CharacterCatalogue
from .settings import Settings
from .utils import Utils

SAMPLE_RATE = 24_000

FALLBACK_NAMES = {
    "narrator": ("Narratrice", "narrator"),
    "father": ("Papa", "father"),
    "mother": ("Maman", "mother"),
    "child_boy": ("Enfant garçon", "child"),
    "child_girl": ("Enfant fille", "child"),
}


class ReplicaBook:
    """Une WAV par réplique ; assemble l'histoire après chaque édition."""

    def __init__(self, settings: Settings, catalogue: CharacterCatalogue) -> None:
        self.settings = settings
        self.catalogue = catalogue

    def folder(self, job_id: str) -> Path:
        return self.settings.jobs_dir / job_id

    def replica_path(self, job_id: str, index: int) -> Path:
        return self.folder(job_id) / "replicas" / f"{int(index):04d}.wav"

    def edit_path(self, job_id: str) -> Path:
        return self.folder(job_id) / "edit.json"

    def scenario_path(self, job_id: str) -> Path:
        return self.folder(job_id) / "scenario.json"

    def write_replica(self, job_id: str, index: int, audio: np.ndarray) -> Path:
        return Utils.write_pcm16(self.replica_path(job_id, index), audio, SAMPLE_RATE)

    def duration_ms(self, path: Path) -> int:
        return Utils.duration_ms(path)

    def speaker_meta(self, key: str, assignments: dict[str, str]) -> dict[str, str]:
        profile_id = assignments.get(key) or key
        profile = self.catalogue.get(profile_id) or self.catalogue.get(key)
        if profile:
            return {
                "key": key,
                "profile_id": profile.id,
                "display_name": profile.display_name,
                "role": profile.role,
            }
        name, role = FALLBACK_NAMES.get(key, (key, "character"))
        return {"key": key, "profile_id": profile_id, "display_name": name, "role": role}

    def capture(self, job_id: str, story: Any, assignments: dict[str, str], sources: dict[int, str] | None = None) -> dict[str, Any]:
        previous = self.load(job_id)
        old_sources = {int(row["index"]): row.get("source") or "tts" for row in (previous or {}).get("replicas") or []}
        speakers: dict[str, dict[str, str]] = {}
        replicas: list[dict[str, Any]] = []
        for index, segment in enumerate(story.segments, start=1):
            meta = self.speaker_meta(segment.speaker, assignments)
            speakers[segment.speaker] = meta
            path = self.replica_path(job_id, index)
            source = (sources or {}).get(index) or old_sources.get(index) or "tts"
            replicas.append(
                {
                    "index": index,
                    "speaker": segment.speaker,
                    "display_name": meta["display_name"],
                    "role": meta["role"],
                    "text": segment.text,
                    "pause_before_ms": int(segment.prosody.pause_before_ms or 0),
                    "pause_after_ms": int(segment.prosody.pause_after_ms or 0),
                    "duration_ms": self.duration_ms(path),
                    "source": source,
                    "file": f"replicas/{index:04d}.wav",
                }
            )
        payload = {
            "title": story.title,
            "assignments": assignments,
            "speakers": speakers,
            "replicas": replicas,
        }
        self.save(job_id, payload)
        return payload

    def save(self, job_id: str, payload: dict[str, Any]) -> None:
        Utils.dump_json(self.edit_path(job_id), payload)

    def load(self, job_id: str) -> dict[str, Any] | None:
        return Utils.load_json(self.edit_path(job_id))

    def save_scenario(self, job_id: str, title: str, speaker_keys: list[str], segments: list[dict[str, Any]], assignments: dict[str, str]) -> None:
        Utils.dump_json(
            self.scenario_path(job_id),
            {
                "title": title,
                "speaker_keys": speaker_keys,
                "segments": segments,
                "assignments": assignments,
            },
        )

    def load_scenario(self, job_id: str) -> dict[str, Any] | None:
        return Utils.load_json(self.scenario_path(job_id))

    def mark_source(self, job_id: str, index: int, source: str) -> dict[str, Any]:
        edit = self.load(job_id)
        if not edit:
            raise FileNotFoundError("Livre de répliques introuvable.")
        path = self.replica_path(job_id, index)
        for row in edit.get("replicas") or []:
            if int(row.get("index") or 0) == int(index):
                row["source"] = source
                row["duration_ms"] = self.duration_ms(path)
                break
        else:
            raise KeyError(f"Réplique {index} introuvable.")
        self.save(job_id, edit)
        return edit

    def assemble(self, job_id: str) -> Path:
        edit = self.load(job_id)
        if not edit:
            raise FileNotFoundError("Livre de répliques introuvable.")
        parts: list[np.ndarray] = []
        for row in edit.get("replicas") or []:
            before = int(row.get("pause_before_ms") or 0)
            after = int(row.get("pause_after_ms") or 0)
            if before > 0:
                parts.append(Utils.silence(before, SAMPLE_RATE))
            path = self.folder(job_id) / str(row.get("file") or "")
            if not path.is_file():
                raise FileNotFoundError(f"Audio de la réplique {row.get('index')} manquant.")
            parts.append(Utils.read_mono(path, SAMPLE_RATE))
            if after > 0:
                parts.append(Utils.silence(after, SAMPLE_RATE))
        audio = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
        output = self.folder(job_id) / "histoire.wav"
        Utils.write_pcm16(output, audio, SAMPLE_RATE)
        return output

    def transcode(self, source: Path, dest: Path) -> None:
        Utils.transcode(source, dest, SAMPLE_RATE)
