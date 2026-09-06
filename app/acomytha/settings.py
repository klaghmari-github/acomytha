"""Configuration objet : chemins, comptes démo, secrets locaux."""

from __future__ import annotations

import os
from pathlib import Path


class Settings:
    """Un objet de config par processus. Surcharge via ACOMYTHA_*. Champs privés, accès par propriétés."""

    def __init__(self) -> None:
        self._repo_root = Path(__file__).resolve().parents[2]
        self._data_dir = Path(os.environ.get("ACOMYTHA_DATA", self._repo_root / "app" / "data"))
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._frontend_dir = Path(os.environ.get("ACOMYTHA_FRONTEND", self._repo_root / "app" / "frontend"))
        self._arbres_dir = Path(os.environ.get("ACOMYTHA_ARBRES", self._repo_root / "stories" / "arbres"))
        self._audio_dir = Path(os.environ.get("ACOMYTHA_AUDIO", self._repo_root / "stories" / "audio"))
        self._lecons_xlsx = Path(
            os.environ.get("ACOMYTHA_LECONS", self._repo_root / "stories" / "referentiel" / "lecons.xlsx")
        )
        self._chk_dir = self._data_dir / "chk"
        self._chk_dir.mkdir(parents=True, exist_ok=True)
        self._db_path = self._data_dir / "acomytha.sqlite"
        self._master_key_path = self._data_dir / "master.key"
        self._session_hours = int(os.environ.get("ACOMYTHA_SESSION_HOURS", "72"))
        self._admin_email = os.environ.get("ACOMYTHA_ADMIN_EMAIL", "admin@acomytha.local")
        self._admin_password = os.environ.get("ACOMYTHA_ADMIN_PASSWORD", "acomytha-admin")
        self._parent_email = os.environ.get("ACOMYTHA_PARENT_EMAIL", "parent@acomytha.local")
        self._parent_password = os.environ.get("ACOMYTHA_PARENT_PASSWORD", "acomytha-parent")
        self._child_pin = os.environ.get("ACOMYTHA_CHILD_PIN", "2468")
        self._cookie_name = "acomytha_session"
        self._cookie_secure = os.environ.get("ACOMYTHA_COOKIE_SECURE", "0") == "1"
        self._public_url = os.environ.get("ACOMYTHA_PUBLIC_URL", "http://127.0.0.1:8787")
        self._stripe_secret = os.environ.get("STRIPE_SECRET_KEY", "").strip()
        self._stripe_webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "").strip()

    def _as_path(self, value: Path | str) -> Path:
        return value if isinstance(value, Path) else Path(value)

    @property
    def repo_root(self) -> Path:
        return self._repo_root

    @property
    def data_dir(self) -> Path:
        return self._data_dir

    @data_dir.setter
    def data_dir(self, value: Path | str) -> None:
        self._data_dir = self._as_path(value)

    @property
    def frontend_dir(self) -> Path:
        return self._frontend_dir

    @frontend_dir.setter
    def frontend_dir(self, value: Path | str) -> None:
        self._frontend_dir = self._as_path(value)

    @property
    def arbres_dir(self) -> Path:
        return self._arbres_dir

    @arbres_dir.setter
    def arbres_dir(self, value: Path | str) -> None:
        self._arbres_dir = self._as_path(value)

    @property
    def audio_dir(self) -> Path:
        return self._audio_dir

    @audio_dir.setter
    def audio_dir(self, value: Path | str) -> None:
        self._audio_dir = self._as_path(value)

    @property
    def lecons_xlsx(self) -> Path:
        return self._lecons_xlsx

    @lecons_xlsx.setter
    def lecons_xlsx(self, value: Path | str) -> None:
        self._lecons_xlsx = self._as_path(value)

    @property
    def chk_dir(self) -> Path:
        return self._chk_dir

    @chk_dir.setter
    def chk_dir(self, value: Path | str) -> None:
        self._chk_dir = self._as_path(value)

    @property
    def db_path(self) -> Path:
        return self._db_path

    @db_path.setter
    def db_path(self, value: Path | str) -> None:
        self._db_path = self._as_path(value)

    @property
    def master_key_path(self) -> Path:
        return self._master_key_path

    @master_key_path.setter
    def master_key_path(self, value: Path | str) -> None:
        self._master_key_path = self._as_path(value)

    @property
    def session_hours(self) -> int:
        return self._session_hours

    @session_hours.setter
    def session_hours(self, value: int) -> None:
        self._session_hours = max(1, int(value))

    @property
    def admin_email(self) -> str:
        return self._admin_email

    @property
    def admin_password(self) -> str:
        return self._admin_password

    @property
    def parent_email(self) -> str:
        return self._parent_email

    @property
    def parent_password(self) -> str:
        return self._parent_password

    @property
    def child_pin(self) -> str:
        return self._child_pin

    @property
    def cookie_name(self) -> str:
        return self._cookie_name

    @property
    def cookie_secure(self) -> bool:
        return self._cookie_secure

    @property
    def public_url(self) -> str:
        return self._public_url

    @property
    def stripe_secret(self) -> str:
        return self._stripe_secret

    @stripe_secret.setter
    def stripe_secret(self, value: str) -> None:
        self._stripe_secret = str(value).strip()

    @property
    def stripe_webhook_secret(self) -> str:
        return self._stripe_webhook_secret

    @stripe_webhook_secret.setter
    def stripe_webhook_secret(self, value: str) -> None:
        self._stripe_webhook_secret = str(value).strip()

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self._db_path}"


def get_settings() -> Settings:
    return Settings()
