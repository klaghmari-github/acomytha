#!/usr/bin/env python3
"""Moteur narratif local Kokoro + clonage de timbre OpenVoice V2."""

from __future__ import annotations

import argparse
import json
import logging
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import librosa
import numpy as np
import soundfile as sf

SAMPLE_RATE = 24_000
LOG = logging.getLogger("acomytha_tts")


@dataclass(frozen=True)
class Prosody:
    speed: float = 1.0
    gain_db: float = 0.0
    pitch_semitones: float = 0.0
    pause_before_ms: int = 0
    pause_after_ms: int = 250
    emotion: str = "neutral"
    intonation: str = "neutral"
    emphasis_words: tuple[str, ...] = ()


@dataclass(frozen=True)
class Speaker:
    name: str
    kokoro_voice: str = "ff_siwis"
    reference_audio: Path | None = None
    fingerprint_speed: float = 1.0
    fingerprint_pitch: float = 0.0
    fingerprint_gain: float = 0.0


@dataclass(frozen=True)
class Segment:
    text: str
    speaker: str
    prosody: Prosody = field(default_factory=Prosody)


@dataclass(frozen=True)
class Story:
    title: str
    speakers: dict[str, Speaker]
    segments: list[Segment]


class StoryLoader:
    """Charge le JSON, applique les valeurs par défaut et valide les bornes."""

    EMOTIONS = {
        "neutral", "calm", "warm", "joy", "excited", "focused", "suspense",
        "storytelling", "sadness", "anger", "surprise", "fear", "whisper",
    }
    INTONATIONS = {"neutral", "rising", "falling", "dramatic", "storytelling"}
    PROSODY_FIELDS = {f.name for f in Prosody.__dataclass_fields__.values()}

    def load(self, path: Path) -> Story:
        data = json.loads(path.read_text(encoding="utf-8"))
        return self.load_dict(data, path.parent, path.stem)

    def load_dict(self, data: dict[str, Any], base_dir: Path, fallback_title: str = "histoire") -> Story:
        speakers: dict[str, Speaker] = {}
        for name, raw in (data.get("speakers") or {}).items():
            if not isinstance(raw, dict):
                raw = {}
            speakers[name] = Speaker(
                name,
                raw.get("kokoro_voice", "ff_siwis"),
                self._resolve_reference(raw.get("reference_audio"), base_dir, name),
            )

        segments: list[Segment] = []
        defaults = data.get("defaults", {}).get("prosody", {}) if isinstance(data.get("defaults"), dict) else {}
        for index, raw in enumerate(data.get("segments") or [], start=1):
            speaker = str(raw.get("speaker") or "narrator")
            if speaker not in speakers:
                speakers[speaker] = Speaker(speaker)
            text = str(raw.get("text", "")).strip()
            if not text:
                raise ValueError(f"Segment {index}: texte vide")
            merged = {**defaults, **(raw.get("prosody") or {})}
            if "emphasis_words" in merged:
                merged["emphasis_words"] = tuple(merged.get("emphasis_words") or ())
            merged = {key: value for key, value in merged.items() if key in self.PROSODY_FIELDS}
            prosody = Prosody(**merged)
            self._validate_prosody(prosody, index)
            segments.append(Segment(text, speaker, prosody))

        if not segments:
            raise ValueError("Le scénario ne contient aucun segment.")
        return Story(str(data.get("title") or fallback_title), speakers, segments)

    def _resolve_reference(self, ref: Any, base_dir: Path, speaker: str) -> Path | None:
        if not ref:
            return None
        raw = Path(str(ref))
        candidates = [raw if raw.is_absolute() else (base_dir / raw)]
        project = Path(__file__).resolve().parent
        candidates.append(project / raw)
        candidates.append(project / "voices" / raw.name)
        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved.is_file():
                return resolved
        LOG.warning("Échantillon introuvable pour %s (%s) : clonage ignoré pour ce locuteur.", speaker, ref)
        return None

    def _validate_prosody(self, value: Prosody, index: int) -> None:
        if not 0.5 <= value.speed <= 1.6:
            raise ValueError(f"Segment {index}: speed doit être compris entre 0.5 et 1.6")
        if not -12 <= value.gain_db <= 8:
            raise ValueError(f"Segment {index}: gain_db doit être compris entre -12 et 8")
        if not -5 <= value.pitch_semitones <= 5:
            raise ValueError(f"Segment {index}: pitch_semitones doit être compris entre -5 et 5")
        if not 0 <= value.pause_before_ms <= 5000:
            raise ValueError(f"Segment {index}: pause_before_ms doit être compris entre 0 et 5000")
        if not 0 <= value.pause_after_ms <= 5000:
            raise ValueError(f"Segment {index}: pause_after_ms doit être compris entre 0 et 5000")
        if value.emotion not in self.EMOTIONS:
            raise ValueError(f"Segment {index}: émotion non reconnue: {value.emotion}")
        if value.intonation not in self.INTONATIONS:
            raise ValueError(f"Segment {index}: intonation non reconnue: {value.intonation}")


class ProsodyProcessor:
    """Transforme les métadonnées en réglages acoustiques reproductibles."""

    EMOTION_PRESETS: dict[str, tuple[float, float, float]] = {
        # speed multiplier, pitch addition, gain addition
        "neutral": (1.00, 0.0, 0.0),
        "calm": (0.92, -0.4, -1.0),
        "warm": (0.96, -0.1, -0.2),
        "joy": (1.06, 0.8, 1.0),
        "excited": (1.10, 1.0, 1.2),
        "focused": (0.97, -0.1, 0.0),
        "suspense": (0.90, -0.5, -1.0),
        "storytelling": (0.96, 0.15, 0.0),
        "sadness": (0.86, -1.0, -2.0),
        "anger": (1.08, 0.4, 2.5),
        "surprise": (1.10, 1.4, 1.2),
        "fear": (1.12, 1.0, -0.5),
        "whisper": (0.94, 0.2, -5.0),
    }
    INTONATION_PITCH = {
        "neutral": 0.0,
        "rising": 0.7,
        "falling": -0.6,
        "dramatic": 0.9,
        "storytelling": 0.2,
    }

    def resolved(self, p: Prosody) -> tuple[float, float, float]:
        speed_mul, pitch_add, gain_add = self.EMOTION_PRESETS[p.emotion]
        speed = float(np.clip(p.speed * speed_mul, 0.5, 1.6))
        pitch = float(np.clip(p.pitch_semitones + pitch_add + self.INTONATION_PITCH[p.intonation], -5, 5))
        gain = float(np.clip(p.gain_db + gain_add, -12, 8))
        return speed, pitch, gain

    def postprocess(self, audio: np.ndarray, pitch: float, gain_db: float) -> np.ndarray:
        result = np.asarray(audio, dtype=np.float32)
        if abs(pitch) > 0.01:
            result = librosa.effects.pitch_shift(result, sr=SAMPLE_RATE, n_steps=pitch)
        result *= 10 ** (gain_db / 20.0)
        peak = float(np.max(np.abs(result))) if result.size else 0.0
        if peak > 0.98:
            result *= 0.98 / peak
        return result.astype(np.float32)


class KokoroSynthesizer:
    """Génère la parole française de base. Kokoro ne clone pas de voix."""

    def __init__(self, lang_code: str = "f") -> None:
        from kokoro import KPipeline
        self.pipeline = KPipeline(lang_code=lang_code)

    def synthesize(self, text: str, voice: str, speed: float) -> np.ndarray:
        chunks = [np.asarray(audio, dtype=np.float32) for _, _, audio in self.pipeline(
            text, voice=voice, speed=speed, split_pattern=r"\n+"
        )]
        if not chunks:
            raise RuntimeError("Kokoro n'a produit aucun son.")
        silence = np.zeros(int(SAMPLE_RATE * 0.08), dtype=np.float32)
        joined: list[np.ndarray] = []
        for chunk in chunks:
            if joined:
                joined.append(silence)
            joined.append(chunk)
        return np.concatenate(joined)


class OpenVoiceCloner:
    """Extrait puis applique le timbre d'un échantillon avec OpenVoice V2."""

    def __init__(self, checkpoint_root: Path, device: str = "cpu") -> None:
        import torch
        from openvoice.api import OpenVoiceBaseClass, ToneColorConverter
        config = checkpoint_root / "converter" / "config.json"
        checkpoint = checkpoint_root / "converter" / "checkpoint.pth"
        if not config.is_file() or not checkpoint.is_file():
            raise FileNotFoundError(f"Checkpoints OpenVoice V2 absents dans {checkpoint_root}")
        if device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("--device cuda demandé, mais CUDA n'est pas disponible.")
        # OpenVoice transmet enable_watermark au parent, qui ne l'accepte pas.
        # On initialise sans wavmark (hors périmètre enfant).
        converter = ToneColorConverter.__new__(ToneColorConverter)
        OpenVoiceBaseClass.__init__(converter, str(config), device=device)
        converter.watermark_model = None
        converter.version = getattr(converter.hps, "_version_", "v1")
        converter.load_ckpt(str(checkpoint))
        self.converter = converter
        self.cache: dict[Path, Any] = {}

    def _embedding(self, audio_path: Path) -> Any:
        key = audio_path.resolve()
        if key not in self.cache:
            # extract_se direct : pas de se_extractor (faster-whisper / av / VAD).
            self.cache[key] = self.converter.extract_se([str(key)])
        return self.cache[key]

    def convert(self, source_wav: Path, reference_wav: Path, output_wav: Path) -> None:
        source_se = self._embedding(source_wav)
        target_se = self._embedding(reference_wav)
        self.converter.convert(
            audio_src_path=str(source_wav),
            src_se=source_se,
            tgt_se=target_se,
            output_path=str(output_wav),
            message="Acomytha",
        )


class StoryRenderer:
    """Orchestre synthèse, prosodie, clonage autorisé et assemblage final."""

    def __init__(self, kokoro: KokoroSynthesizer, prosody: ProsodyProcessor, cloner: OpenVoiceCloner | None) -> None:
        self.kokoro = kokoro
        self.prosody = prosody
        self.cloner = cloner

    def synthesize_segment(self, story: Story, segment: Segment, index: int, temp_dir: Path) -> np.ndarray:
        speaker = story.speakers[segment.speaker]
        speed, pitch, gain = self.prosody.resolved(segment.prosody)
        speed = float(np.clip(speed * speaker.fingerprint_speed, 0.5, 1.6))
        pitch = float(np.clip(pitch + speaker.fingerprint_pitch, -5, 5))
        gain = float(np.clip(gain + speaker.fingerprint_gain, -12, 8))
        audio = self.kokoro.synthesize(segment.text, speaker.kokoro_voice, speed)
        audio = self.prosody.postprocess(audio, pitch, gain)
        if speaker.reference_audio:
            if self.cloner is None:
                raise RuntimeError("Un échantillon vocal est déclaré, mais OpenVoice est désactivé.")
            source = temp_dir / f"{index:04d}_source.wav"
            cloned = temp_dir / f"{index:04d}_cloned.wav"
            sf.write(source, audio, SAMPLE_RATE)
            self.cloner.convert(source, speaker.reference_audio, cloned)
            audio, sr = sf.read(cloned, dtype="float32")
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
            if sr != SAMPLE_RATE:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=SAMPLE_RATE)
        return np.asarray(audio, dtype=np.float32)

    def render(self, story: Story, output: Path, on_progress=None, on_replica=None) -> None:
        rendered: list[np.ndarray] = []
        total = max(len(story.segments), 1)
        with tempfile.TemporaryDirectory(prefix="acomytha_tts_") as tmp:
            temp_dir = Path(tmp)
            for index, segment in enumerate(story.segments, start=1):
                speaker = story.speakers[segment.speaker]
                if on_progress:
                    on_progress(index, total, speaker.name)
                LOG.info("Segment %d/%d — %s", index, len(story.segments), speaker.name)
                if segment.prosody.pause_before_ms:
                    rendered.append(np.zeros(int(SAMPLE_RATE * segment.prosody.pause_before_ms / 1000), dtype=np.float32))
                audio = self.synthesize_segment(story, segment, index, temp_dir)
                if on_replica:
                    on_replica(index, segment, audio)
                rendered.append(audio)
                pause = np.zeros(int(SAMPLE_RATE * segment.prosody.pause_after_ms / 1000), dtype=np.float32)
                rendered.append(pause)

        output.parent.mkdir(parents=True, exist_ok=True)
        sf.write(output, np.concatenate(rendered), SAMPLE_RATE, subtype="PCM_16")
        LOG.info("Audio écrit dans %s", output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Génère une histoire audio Acomytha depuis un scénario JSON.")
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/histoire.wav"))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--checkpoints", type=Path, default=Path("vendor/OpenVoice/checkpoints_v2"))
    parser.add_argument("--without-cloning", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    story = StoryLoader().load(args.scenario)
    needs_cloning = any(s.reference_audio for s in story.speakers.values())
    cloner = None
    if needs_cloning and not args.without_cloning:
        cloner = OpenVoiceCloner(args.checkpoints.resolve(), args.device)
    StoryRenderer(KokoroSynthesizer(), ProsodyProcessor(), cloner).render(story, args.output)


if __name__ == "__main__":
    main()
