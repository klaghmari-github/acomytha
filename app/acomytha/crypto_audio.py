"""Coffre audio AES-256-GCM. Master local, clé d'histoire HKDF."""

from __future__ import annotations

import json
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from acomytha.settings import Settings

MAGIC = b"SNT01"


class AudioVault:
    """Un objet coffre : enveloppe les MP3 atelier en .chk jouables seulement par l'app."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.master = self._load_or_create_master()

    def _load_or_create_master(self) -> bytes:
        path = self.settings.master_key_path
        if path.exists():
            return path.read_bytes()
        key = AESGCM.generate_key(bit_length=256)
        path.write_bytes(key)
        path.chmod(0o600)
        return key

    def story_key(self, story_id: str) -> bytes:
        hkdf = HKDF(algorithm=SHA256(), length=32, salt=b"acomytha-story", info=story_id.encode("utf-8"))
        return hkdf.derive(self.master)

    def story_key_b64(self, story_id: str) -> str:
        import base64

        return base64.b64encode(self.story_key(story_id)).decode("ascii")

    def chk_path(self, story_id: str, chunk_id: str) -> Path:
        return self.settings.chk_dir / story_id / f"{chunk_id}.chk"

    def mp3_path(self, story_id: str, chunk_id: str) -> Path:
        return self.settings.audio_dir / story_id / f"{chunk_id}.mp3"

    def ensure_chk(self, story_id: str, chunk_id: str) -> Path:
        dest = self.chk_path(story_id, chunk_id)
        if dest.exists() and dest.stat().st_size > 32:
            return dest
        src = self.mp3_path(story_id, chunk_id)
        if not src.exists():
            raise FileNotFoundError(f"mp3 absent: {src}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(self.wrap(story_id, chunk_id, src.read_bytes()))
        return dest

    def wrap(self, story_id: str, chunk_id: str, mp3: bytes) -> bytes:
        header = json.dumps(
            {"v": 1, "story_id": story_id, "chunk_id": chunk_id, "codec": "mp3"},
            separators=(",", ":"),
        ).encode("utf-8")
        nonce = os.urandom(12)
        aes = AESGCM(self.story_key(story_id))
        ct = aes.encrypt(nonce, mp3, header)
        return MAGIC + len(header).to_bytes(2, "big") + header + nonce + ct

    def unwrap(self, blob: bytes, story_id: str) -> bytes:
        if blob[:5] != MAGIC:
            raise ValueError("magic")
        hlen = int.from_bytes(blob[5:7], "big")
        header = blob[7 : 7 + hlen]
        nonce = blob[7 + hlen : 19 + hlen]
        ct = blob[19 + hlen :]
        aes = AESGCM(self.story_key(story_id))
        return aes.decrypt(nonce, ct, header)
