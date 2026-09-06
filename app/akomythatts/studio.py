"""Enregistrement et génération d'empreintes vocales."""

from __future__ import annotations

import threading
import uuid
from pathlib import Path
from typing import Any, Callable

import numpy as np

from .catalogue import CharacterCatalogue
from .models import CharacterProfile, VoiceFingerprint
from .settings import Settings
from .utils import Utils

GENERATE_PRESETS = {
    ("female", "adult"): VoiceFingerprint(0.96, 0.0, 0.0),
    ("female", "child"): VoiceFingerprint(1.03, 1.2, 0.0),
    ("female", "senior"): VoiceFingerprint(0.90, -1.1, 0.1),
    ("male", "adult"): VoiceFingerprint(0.96, -2.2, 0.3),
    ("male", "child"): VoiceFingerprint(1.02, 0.45, 0.0),
    ("male", "senior"): VoiceFingerprint(0.88, -3.0, 0.2),
}

TEMPERAMENTS = {
    "calme": VoiceFingerprint(0.92, -0.2, -0.4),
    "naturel": VoiceFingerprint(1.0, 0.0, 0.0),
    "vif": VoiceFingerprint(1.08, 0.35, 0.2),
}


class VoiceWork:
    def __init__(self, kind: str, label: str) -> None:
        self.id = uuid.uuid4().hex[:12]
        self.kind = kind
        self.label = label
        self.status = "queued"
        self.progress = 0
        self.message = "En file d'attente…"
        self.profile: CharacterProfile | None = None

    def public(self) -> dict[str, Any]:
        item: dict[str, Any] = {
            "job_id": self.id,
            "kind": self.kind,
            "label": self.label,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
        }
        if self.profile is not None:
            data = self.profile.to_dict()
            data["id"] = self.profile.id
            data["has_fingerprint"] = True
            item["profile"] = data
        return item


class VoiceStudio:
    """Crée une empreinte : synthèse Kokoro ou enregistrement micro."""

    def __init__(self, settings: Settings, catalogue: CharacterCatalogue, queue) -> None:
        self.settings = settings
        self.catalogue = catalogue
        self.queue = queue
        self._works: dict[str, VoiceWork] = {}

    def get_work(self, job_id: str) -> VoiceWork | None:
        return self._works.get(job_id)

    def submit_generate(self, **kwargs: Any) -> VoiceWork:
        return self._submit("generate", self._run_generate, kwargs)

    def submit_record(self, **kwargs: Any) -> VoiceWork:
        return self._submit("record", self._run_record, kwargs)

    def _submit(self, kind: str, runner, kwargs: dict[str, Any]) -> VoiceWork:
        work = VoiceWork(kind, str(kwargs.get("display_name") or "voix"))
        self._works[work.id] = work
        threading.Thread(target=runner, args=(work, kwargs), daemon=True).start()
        return work

    def _run_generate(self, work: VoiceWork, kwargs: dict[str, Any]) -> None:
        self._finish(work, lambda: self.generate(progress=self._reporter(work), **kwargs), "Empreinte prête.")

    def _run_record(self, work: VoiceWork, kwargs: dict[str, Any]) -> None:
        upload = kwargs.get("upload_path")
        try:
            self._finish(work, lambda: self.record(progress=self._reporter(work), **kwargs), "Empreinte enregistrée.")
        finally:
            if isinstance(upload, Path):
                try:
                    upload.unlink(missing_ok=True)
                except OSError:
                    pass

    def _finish(self, work: VoiceWork, factory, done_message: str) -> None:
        try:
            work.status = "running"
            work.profile = factory()
            work.progress = 100
            work.status = "done"
            work.message = done_message
        except Exception as exc:
            work.status = "error"
            work.message = str(exc)

    def _reporter(self, work: VoiceWork) -> Callable[[int, str], None]:
        def report(progress: int, message: str) -> None:
            work.progress = max(0, min(100, int(progress)))
            work.message = message
            work.status = "running"

        return report

    def generate(
        self,
        profile_id: str,
        display_name: str,
        gender: str,
        age_group: str,
        temperament: str = "naturel",
        role: str = "character",
        progress: Callable[[int, str], None] | None = None,
    ) -> CharacterProfile:
        def report(value: int, message: str) -> None:
            if progress:
                progress(value, message)

        base = GENERATE_PRESETS.get((gender, age_group), VoiceFingerprint())
        mood = TEMPERAMENTS.get(temperament, VoiceFingerprint())
        fingerprint = VoiceFingerprint(
            speed=float(np.clip(base.speed * mood.speed, 0.5, 1.6)),
            pitch_semitones=float(np.clip(base.pitch_semitones + mood.pitch_semitones, -5, 5)),
            gain_db=float(np.clip(base.gain_db + mood.gain_db, -12, 8)),
        )
        text = f"Bonjour, je m'appelle {display_name}. J'aime raconter des histoires, tout doucement."
        report(8, "Préparation de l'empreinte…")
        stop_pulse = threading.Event()

        def pulse() -> None:
            value = 22
            while not stop_pulse.wait(0.45):
                value = min(42, value + 2)
                report(value, "Chargement de Kokoro…")

        report(22, "Chargement de Kokoro…")
        threading.Thread(target=pulse, daemon=True).start()
        try:
            with self.queue._engine_lock:
                kokoro = self.queue.kokoro()
                stop_pulse.set()
                report(48, "Synthèse de la voix…")
                audio = kokoro.synthesize(text, "ff_siwis", fingerprint.speed)
        finally:
            stop_pulse.set()
        if abs(fingerprint.pitch_semitones) > 0.01:
            import librosa

            report(72, "Ajustement du timbre…")
            audio = librosa.effects.pitch_shift(audio, sr=self.settings.sample_rate, n_steps=fingerprint.pitch_semitones)
        report(88, "Enregistrement au catalogue…")
        rel = self._write_wav(profile_id, audio)
        profile = CharacterProfile(
            id=profile_id,
            display_name=display_name,
            gender=gender,
            age_group=age_group,
            role=role,
            kokoro_voice="ff_siwis",
            reference_audio=rel,
            fingerprint=fingerprint,
            direction=f"empreinte générée ({gender}, {age_group}, {temperament})",
        )
        saved = self.catalogue.upsert(profile)
        report(100, "Empreinte prête.")
        return saved

    def record(
        self,
        profile_id: str,
        display_name: str,
        gender: str,
        age_group: str,
        upload_path: Path,
        role: str = "character",
        temperament: str = "naturel",
        progress: Callable[[int, str], None] | None = None,
    ) -> CharacterProfile:
        def report(value: int, message: str) -> None:
            if progress:
                progress(value, message)

        report(18, "Réception de l'enregistrement…")
        report(42, "Conversion en WAV 24 kHz…")
        wav_rel = self._transcode(profile_id, upload_path)
        report(78, "Enregistrement au catalogue…")
        base = GENERATE_PRESETS.get((gender, age_group), VoiceFingerprint())
        mood = TEMPERAMENTS.get(temperament, VoiceFingerprint())
        fingerprint = VoiceFingerprint(
            speed=float(np.clip(base.speed * mood.speed, 0.5, 1.6)),
            pitch_semitones=float(np.clip(base.pitch_semitones + mood.pitch_semitones, -5, 5)),
            gain_db=float(np.clip(base.gain_db + mood.gain_db, -12, 8)),
        )
        profile = CharacterProfile(
            id=profile_id,
            display_name=display_name,
            gender=gender,
            age_group=age_group,
            role=role,
            kokoro_voice="ff_siwis",
            reference_audio=wav_rel,
            fingerprint=fingerprint,
            direction=f"empreinte enregistrée ({gender}, {age_group})",
        )
        saved = self.catalogue.upsert(profile)
        report(100, "Empreinte enregistrée.")
        return saved

    def _voice_path(self, profile_id: str) -> Path:
        folder = self.settings.characters_dir if profile_id.startswith("character.") else self.settings.defaults_dir
        return folder / (profile_id.replace(".", "_") + ".wav")

    def _write_wav(self, profile_id: str, audio: np.ndarray) -> str:
        path = Utils.write_pcm16(self._voice_path(profile_id), audio, self.settings.sample_rate)
        return str(path.relative_to(self.settings.root))

    def _transcode(self, profile_id: str, source: Path) -> str:
        dest = self._voice_path(profile_id)
        Utils.transcode(source, dest, self.settings.sample_rate)
        return str(dest.relative_to(self.settings.root))
