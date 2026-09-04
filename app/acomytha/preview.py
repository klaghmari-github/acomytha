"""Aperçu audio : N premières secondes du chemin par défaut, tous passages."""

from __future__ import annotations

import wave
from pathlib import Path

import lameenc
import numpy as np

from acomytha.crypto_audio import AudioVault
from acomytha.graph import StoryGraph
from acomytha.models import Chunk
from acomytha.settings import Settings

PREVIEW_CHUNK = "CHK_PREVIEW"
TARGET_SR = 44100
CHANNELS = 2
GAP_S = 0.12


class PreviewStudio:
    """Assemble le clip d’aperçu (chemin par défaut) et son graphe client."""

    def __init__(self, settings: Settings, vault: AudioVault) -> None:
        self._settings = settings
        self._vault = vault

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def vault(self) -> AudioVault:
        return self._vault

    @staticmethod
    def clip_id(seconds: int) -> str:
        return f"{PREVIEW_CHUNK}_{int(seconds)}"

    def client_graph(self, story, seconds: int, key: str) -> dict:
        return client_graph(story, seconds, key)

    def ensure_chk(self, story_id: str, chunks: list[Chunk], seconds: int) -> Path:
        return ensure_preview_chk(self._vault, self._settings, story_id, chunks, seconds)


def preview_id(seconds: int) -> str:
    return PreviewStudio.clip_id(seconds)


def client_graph(story, seconds: int, key: str) -> dict:
    cid = preview_id(seconds)
    return {
        "story_id": story.story_id,
        "title": story.title,
        "root": cid,
        "preview_seconds": int(seconds),
        "has_audio": story.has_audio,
        "key": key,
        "chunks": {
            cid: {
                "chunk_id": cid,
                "kind": "passage",
                "wait_ms": 0,
                "night_policy": "play",
                "default_next": None,
                "options": [],
            }
        },
    }


def _read_stereo(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        nch = w.getnchannels()
        sw = w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if sw != 2:
        raise ValueError("wav 16-bit requis")
    samples = np.frombuffer(raw, dtype="<i2").astype(np.float32)
    if nch == 1:
        stereo = np.column_stack((samples, samples))
    else:
        stereo = samples.reshape(-1, nch)[:, :2]
    return stereo, sr


def _encode_mp3(stereo: np.ndarray) -> bytes:
    pcm = np.clip(stereo, -32768, 32767).astype("<i2")
    enc = lameenc.Encoder()
    enc.set_bit_rate(128)
    enc.set_in_sample_rate(TARGET_SR)
    enc.set_channels(CHANNELS)
    enc.set_quality(2)
    return bytes(enc.encode(pcm.tobytes()) + enc.flush())


def stitch_default_path(settings: Settings, story_id: str, chunks: list[Chunk], seconds: float) -> bytes:
    graph = StoryGraph(chunks)
    budget = int(max(1.0, seconds) * TARGET_SR)
    parts: list[np.ndarray] = []
    used = 0
    gap = np.zeros((int(GAP_S * TARGET_SR), 2), dtype=np.float32)
    audio_dir = settings.audio_dir / story_id
    for cid in graph.default_path():
        wav = audio_dir / f"{cid}.wav"
        if not wav.exists():
            continue
        samples, sr = _read_stereo(wav)
        if sr != TARGET_SR and len(samples):
            # ratio entier habituel 22050→44100
            from math import gcd

            from scipy.signal import resample_poly

            g = gcd(sr, TARGET_SR)
            left = resample_poly(samples[:, 0], TARGET_SR // g, sr // g)
            right = resample_poly(samples[:, 1], TARGET_SR // g, sr // g)
            n = min(len(left), len(right))
            samples = np.column_stack((left[:n], right[:n]))
        take = min(len(samples), budget - used)
        if take <= 0:
            break
        parts.append(samples[:take])
        used += take
        if used >= budget:
            break
        if used + len(gap) < budget:
            parts.append(gap)
            used += len(gap)
    if not parts:
        raise FileNotFoundError(f"aucun wav pour aperçu {story_id}")
    mix = np.concatenate(parts, axis=0)
    return _encode_mp3(mix)


def ensure_preview_chk(
    vault: AudioVault,
    settings: Settings,
    story_id: str,
    chunks: list[Chunk],
    seconds: int,
) -> Path:
    cid = preview_id(seconds)
    dest = vault.chk_path(story_id, cid)
    audio_dir = settings.audio_dir / story_id
    sources = list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3"))
    newest = max((p.stat().st_mtime for p in sources), default=0)
    if dest.exists() and dest.stat().st_size > 32 and dest.stat().st_mtime >= newest:
        return dest
    mp3 = stitch_default_path(settings, story_id, chunks, seconds)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(vault.wrap(story_id, cid, mp3))
    return dest
