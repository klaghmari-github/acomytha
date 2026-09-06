"""Helpers transverses : texte, fichiers JSON, audio.

Les objets métier (catalogue, parser, studio, répliques) passent par
``Utils`` plutôt que de recopier slug / ffmpeg / lecture WAV.
"""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path
from typing import Any


class Utils:
    """Boîte à outils globale du moteur TTS."""

    SKIP_JSON = frozenset({"conversion_report.json", "voice_registry.json", "manifest.json"})
    ROLE_ALIASES = {
        "narrateur": "narrator",
        "narratrice": "narrator",
        "papa": "father",
        "père": "father",
        "dad": "father",
        "maman": "mother",
        "mère": "mother",
        "mom": "mother",
        "copain": "friend_boy",
        "copine": "friend_girl",
        "maitresse": "teacher",
        "maîtresse": "teacher",
        "enfant-m": "child_boy",
        "enfant-f": "child_girl",
        "garçon": "child_boy",
        "fille": "child_girl",
    }

    @staticmethod
    def slug(value: str) -> str:
        """Identité compacte d'un nom (Amir → amir, Raphaël → raphael)."""
        stripped = unicodedata.normalize("NFKD", value or "")
        ascii_name = "".join(ch for ch in stripped if not unicodedata.combining(ch))
        return re.sub(r"[^a-z0-9]+", "", ascii_name.casefold()) or "inconnu"

    @staticmethod
    def file_slug(value: str) -> str:
        """Identifiant fichier, tirets bas (Le jardin → le_jardin)."""
        plain = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode().lower()
        return re.sub(r"[^a-z0-9]+", "_", plain).strip("_") or "item"

    @staticmethod
    def speaker_key(role: str) -> str:
        """Alias de rôle Excel/script → clé locuteur (papa → father)."""
        raw = (role or "").strip()
        return Utils.ROLE_ALIASES.get(raw.casefold(), raw)

    @staticmethod
    def is_story_json(path: Path) -> bool:
        return path.suffix.lower() == ".json" and path.name not in Utils.SKIP_JSON

    @staticmethod
    def story_json_paths(folder: Path) -> list[Path]:
        if not folder.is_dir():
            return []
        return [path for path in sorted(folder.glob("*.json")) if Utils.is_story_json(path)]

    @staticmethod
    def load_json(path: Path) -> dict[str, Any] | None:
        if not path.is_file():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return data if isinstance(data, dict) else None

    @staticmethod
    def dump_json(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def safe_filename(title: str, fallback: str = "histoire") -> str:
        cleaned = "".join(ch if ch.isalnum() or ch in "-_ " else "_" for ch in title).strip()
        return cleaned or fallback

    @staticmethod
    def unlink(path: Path | None) -> None:
        if path is None:
            return
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass

    @staticmethod
    def write_pcm16(path: Path, audio, sample_rate: int) -> Path:
        import numpy as np
        import soundfile as sf

        path.parent.mkdir(parents=True, exist_ok=True)
        sf.write(path, np.asarray(audio, dtype=np.float32), sample_rate, subtype="PCM_16")
        return path

    @staticmethod
    def duration_ms(path: Path) -> int:
        import soundfile as sf

        if not path.is_file():
            return 0
        info = sf.info(str(path))
        return int(1000 * info.frames / max(info.samplerate, 1))

    @staticmethod
    def silence(ms: int, sample_rate: int):
        import numpy as np

        if ms <= 0:
            return np.zeros(0, dtype=np.float32)
        return np.zeros(int(sample_rate * ms / 1000), dtype=np.float32)

    @staticmethod
    def read_mono(path: Path, sample_rate: int):
        import numpy as np
        import soundfile as sf

        data, sr = sf.read(path, dtype="float32")
        if getattr(data, "ndim", 1) > 1:
            data = np.mean(data, axis=1)
        if sr != sample_rate:
            import librosa

            data = librosa.resample(data, orig_sr=sr, target_sr=sample_rate)
        return np.asarray(data, dtype=np.float32)

    @staticmethod
    def transcode(source: Path, dest: Path, sample_rate: int) -> Path:
        """WebM/WAV → WAV mono à ``sample_rate``. ffmpeg d'abord, soundfile sinon."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-y", "-i", str(source), "-ac", "1", "-ar", str(sample_rate), str(dest)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return dest
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            detail = ""
            if isinstance(exc, subprocess.CalledProcessError):
                detail = (exc.stderr or exc.stdout or "").strip()
            try:
                audio = Utils.read_mono(source, sample_rate)
            except Exception as read_exc:
                raise RuntimeError(detail or f"Impossible de lire l'enregistrement ({read_exc}).") from read_exc
            Utils.write_pcm16(dest, audio, sample_rate)
            return dest
