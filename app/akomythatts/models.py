"""Objets métier : histoire, personnage, empreinte vocale."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class VoiceFingerprint:
    speed: float = 1.0
    pitch_semitones: float = 0.0
    gain_db: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any] | None) -> VoiceFingerprint:
        data = raw or {}
        return cls(
            speed=float(data.get("speed", 1.0)),
            pitch_semitones=float(data.get("pitch_semitones", 0.0)),
            gain_db=float(data.get("gain_db", 0.0)),
        )


@dataclass
class CharacterProfile:
    id: str
    display_name: str
    gender: str
    age_group: str
    role: str = "character"
    kokoro_voice: str = "ff_siwis"
    reference_audio: str | None = None
    fingerprint: VoiceFingerprint = field(default_factory=VoiceFingerprint)
    direction: str = ""

    def has_audio(self, root: Path) -> bool:
        if not self.reference_audio:
            return False
        path = Path(self.reference_audio)
        if not path.is_absolute():
            path = root / path
        return path.is_file()

    def audio_path(self, root: Path) -> Path | None:
        if not self.reference_audio:
            return None
        path = Path(self.reference_audio)
        return path if path.is_absolute() else (root / path)

    def to_dict(self) -> dict[str, Any]:
        return {
            "display_name": self.display_name,
            "gender": self.gender,
            "age_group": self.age_group,
            "role": self.role,
            "kokoro_voice": self.kokoro_voice,
            "reference_audio": self.reference_audio,
            "voice_fingerprint": self.fingerprint.to_dict(),
            "direction": self.direction,
        }

    @classmethod
    def from_dict(cls, profile_id: str, raw: dict[str, Any]) -> CharacterProfile:
        return cls(
            id=profile_id,
            display_name=str(raw.get("display_name") or profile_id),
            gender=str(raw.get("gender") or "female"),
            age_group=str(raw.get("age_group") or "adult"),
            role=str(raw.get("role") or "character"),
            kokoro_voice=str(raw.get("kokoro_voice") or "ff_siwis"),
            reference_audio=raw.get("reference_audio"),
            fingerprint=VoiceFingerprint.from_dict(raw.get("voice_fingerprint")),
            direction=str(raw.get("direction") or ""),
        )


@dataclass
class CastMember:
    speaker_key: str
    given_name: str
    gender: str
    age_group: str
    role: str
    profile_id: str | None
    has_fingerprint: bool
    suggested_profile_id: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ParsedStory:
    title: str
    format: str
    speaker_keys: list[str]
    segments: list[dict[str, Any]]
    characters_hint: str = ""
    excerpt: str = ""
    chunks: int = 0

    def to_preview(self, cast: list[CastMember]) -> dict[str, Any]:
        return {
            "title": self.title,
            "format": self.format,
            "chunks": self.chunks,
            "segments": len(self.segments),
            "excerpt": self.excerpt,
            "characters_hint": self.characters_hint,
            "cast": [member.to_dict() for member in cast],
        }
