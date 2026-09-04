"""Configuration objet : chemins, comptes démo, secrets locaux."""

from __future__ import annotations

import os
from pathlib import Path


class Settings:
    """Un objet de config par processus. Surcharge via ACOMYTHA_*."""

    def __init__(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[2]
        self.data_dir = Path(os.environ.get("ACOMYTHA_DATA", self.repo_root / "app" / "data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.frontend_dir = Path(os.environ.get("ACOMYTHA_FRONTEND", self.repo_root / "app" / "frontend"))
        self.arbres_dir = Path(os.environ.get("ACOMYTHA_ARBRES", self.repo_root / "stories" / "arbres"))
        self.audio_dir = Path(os.environ.get("ACOMYTHA_AUDIO", self.repo_root / "stories" / "audio"))
        self.lecons_xlsx = Path(
            os.environ.get("ACOMYTHA_LECONS", self.repo_root / "stories" / "referentiel" / "lecons.xlsx")
        )
        self.chk_dir = self.data_dir / "chk"
        self.chk_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "acomytha.sqlite"
        self.master_key_path = self.data_dir / "master.key"
        self.session_hours = int(os.environ.get("ACOMYTHA_SESSION_HOURS", "72"))
        self.admin_email = os.environ.get("ACOMYTHA_ADMIN_EMAIL", "admin@acomytha.local")
        self.admin_password = os.environ.get("ACOMYTHA_ADMIN_PASSWORD", "acomytha-admin")
        self.parent_email = os.environ.get("ACOMYTHA_PARENT_EMAIL", "parent@acomytha.local")
        self.parent_password = os.environ.get("ACOMYTHA_PARENT_PASSWORD", "acomytha-parent")
        self.child_pin = os.environ.get("ACOMYTHA_CHILD_PIN", "2468")
        self.cookie_name = "acomytha_session"
        self.cookie_secure = os.environ.get("ACOMYTHA_COOKIE_SECURE", "0") == "1"
        self.public_url = os.environ.get("ACOMYTHA_PUBLIC_URL", "http://127.0.0.1:8787")
        self.stripe_secret = os.environ.get("STRIPE_SECRET_KEY") or os.environ.get("ACOMYTHA_STRIPE_SECRET", "")
        self.stripe_publishable = os.environ.get("STRIPE_PUBLISHABLE_KEY") or os.environ.get(
            "ACOMYTHA_STRIPE_PUBLISHABLE", ""
        )
        self.stripe_webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET") or os.environ.get(
            "ACOMYTHA_STRIPE_WEBHOOK_SECRET", ""
        )

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.db_path}"


def get_settings() -> Settings:
    return Settings()
