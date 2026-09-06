"""Référentiel persistant des personnages et de leurs empreintes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import CharacterProfile, VoiceFingerprint
from .settings import Settings

DEFAULT_PROFILES: dict[str, dict[str, Any]] = {
    "narrator": {
        "display_name": "Narratrice",
        "gender": "female",
        "age_group": "adult",
        "role": "narrator",
        "kokoro_voice": "ff_siwis",
        "voice_fingerprint": {"speed": 0.94, "pitch_semitones": 0.0, "gain_db": 0.0},
        "direction": "chaleureuse, joueuse, complice",
    },
    "father": {
        "display_name": "Papa",
        "gender": "male",
        "age_group": "adult",
        "role": "father",
        "kokoro_voice": "ff_siwis",
        "voice_fingerprint": {"speed": 0.96, "pitch_semitones": -2.2, "gain_db": 0.3},
        "direction": "rassurante, naturelle",
    },
    "mother": {
        "display_name": "Maman",
        "gender": "female",
        "age_group": "adult",
        "role": "mother",
        "kokoro_voice": "ff_siwis",
        "voice_fingerprint": {"speed": 0.97, "pitch_semitones": -0.3, "gain_db": 0.1},
        "direction": "tendre, claire",
    },
    "child_boy": {
        "display_name": "Enfant garçon",
        "gender": "male",
        "age_group": "child",
        "role": "child",
        "kokoro_voice": "ff_siwis",
        "voice_fingerprint": {"speed": 1.04, "pitch_semitones": 0.5, "gain_db": 0.0},
        "direction": "enfantine, spontanée",
    },
    "child_girl": {
        "display_name": "Enfant fille",
        "gender": "female",
        "age_group": "child",
        "role": "child",
        "kokoro_voice": "ff_siwis",
        "voice_fingerprint": {"speed": 1.03, "pitch_semitones": 1.2, "gain_db": 0.0},
        "direction": "enfantine, spontanée",
    },
}

TROUPE: dict[str, tuple[str, str, str]] = {
    "amir": ("Amir", "male", "child"),
    "aniss": ("Aniss", "male", "child"),
    "sarah": ("Sarah", "female", "child"),
    "chouchou": ("Chouchou", "female", "child"),
    "mila": ("Mila", "female", "child"),
    "nino": ("Nino", "male", "child"),
    "nina": ("Nina", "female", "child"),
    "raphael": ("Raphaël", "male", "child"),
    "victorino": ("Victorino", "male", "child"),
    "victorina": ("Victorina", "female", "child"),
}


class CharacterCatalogue:
    """Registre persistant ``catalogue/voice_registry.json`` : une empreinte par personnage."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.path = settings.catalogue_path
        self.profiles: dict[str, CharacterProfile] = {}
        self.load()

    def load(self) -> None:
        self.settings.ensure_dirs()
        if self.path.is_file():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            stored = raw.get("profiles") or {}
            self.profiles = {
                key: CharacterProfile.from_dict(key, value)
                for key, value in stored.items()
                if isinstance(value, dict)
            }
        for key, spec in DEFAULT_PROFILES.items():
            self.profiles.setdefault(key, CharacterProfile.from_dict(key, spec))
        for slug, (name, gender, age) in TROUPE.items():
            profile_id = f"character.{slug}"
            self.profiles.setdefault(
                profile_id,
                CharacterProfile(
                    id=profile_id,
                    display_name=name,
                    gender=gender,
                    age_group=age,
                    role="character",
                    fingerprint=VoiceFingerprint(
                        speed=1.02 if age == "child" else 0.96,
                        pitch_semitones=1.1 if gender == "female" and age == "child" else 0.4 if age == "child" else -2.0 if gender == "male" else 0.0,
                    ),
                    direction="identité stable entre toutes les histoires",
                ),
            )
        self.save()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": "2.0",
            "profiles": {key: profile.to_dict() for key, profile in sorted(self.profiles.items())},
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def get(self, profile_id: str) -> CharacterProfile | None:
        return self.profiles.get(profile_id)

    def find_by_name(self, name: str) -> CharacterProfile | None:
        needle = name.strip().casefold()
        for profile in self.profiles.values():
            if profile.display_name.casefold() == needle:
                return profile
        return None

    def upsert(self, profile: CharacterProfile) -> CharacterProfile:
        self.profiles[profile.id] = profile
        self.save()
        return profile

    def list_public(self) -> list[dict[str, Any]]:
        root = self.settings.root
        rows = []
        for profile in self.profiles.values():
            item = profile.to_dict()
            item["id"] = profile.id
            item["has_fingerprint"] = profile.has_audio(root)
            rows.append(item)
        rows.sort(key=lambda row: (row["role"], row["display_name"]))
        return rows
