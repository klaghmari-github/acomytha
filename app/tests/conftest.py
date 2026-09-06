from __future__ import annotations

import shutil
import secrets
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from acomytha.main import create_app
from acomytha.settings import Settings

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    arbres = tmp_path / "arbres"
    audio = tmp_path / "audio" / "ATOM-SAN.ALI.001-01"
    arbres.mkdir()
    audio.mkdir(parents=True)
    shutil.copy(REPO / "stories" / "arbres" / "ATOM-SAN.ALI.001-01.xlsx", arbres / "ATOM-SAN.ALI.001-01.xlsx")
    src_dir = REPO / "stories" / "audio" / "ATOM-SAN.ALI.001-01"
    if src_dir.exists():
        for src in src_dir.iterdir():
            if src.suffix in {".mp3", ".wav"}:
                shutil.copy(src, audio / src.name)
    s = Settings()
    s._admin_email = "admin@acomytha.local"
    s._admin_password = secrets.token_urlsafe(24)
    s._parent_email = "parent@acomytha.local"
    s._parent_password = secrets.token_urlsafe(24)
    s._child_pin = ""
    s.data_dir = tmp_path / "data"
    s.data_dir.mkdir()
    s.chk_dir = s.data_dir / "chk"
    s.chk_dir.mkdir()
    s.db_path = s.data_dir / "acomytha.sqlite"
    s.master_key_path = s.data_dir / "master.key"
    s.arbres_dir = arbres
    s.audio_dir = tmp_path / "audio"
    s.lecons_xlsx = REPO / "stories" / "referentiel" / "lecons.xlsx"
    s.frontend_dir = REPO / "app" / "frontend"
    return s


@pytest.fixture()
def client(settings: Settings) -> TestClient:
    app = create_app(settings)
    return TestClient(app)
