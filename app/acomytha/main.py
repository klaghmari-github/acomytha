"""Usine FastAPI : câble services, API, fichiers statiques."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from acomytha.api import admin, auth, editor, play, public, shop, stories
from acomytha.crypto_audio import AudioVault
from acomytha.db import Database
from acomytha.devices import DeviceGuard
from acomytha.mail import MailService
from acomytha.security import SessionService
from acomytha.seed import Bootstrap
from acomytha.settings import Settings, get_settings
from acomytha.rate_limit import RateLimiter


def create_app(settings: Settings | None = None, import_limit: int | None = None) -> FastAPI:
    settings = settings or get_settings()
    database = Database(settings)
    database.create_all()
    with next(database.session()) as db:
        Bootstrap(settings).run(db, import_limit=import_limit)

    app = FastAPI(title="AcoMytha", version="0.1.0")
    app.state.settings = settings
    app.state.database = database
    app.state.sessions = SessionService(hours=settings.session_hours)
    app.state.devices = DeviceGuard()
    app.state.mailer = MailService(settings)
    app.state.rate_limiter = RateLimiter(settings.rate_limit_enabled)
    app.state.vault = AudioVault(settings)

    app.include_router(auth.router)
    app.include_router(public.router)
    app.include_router(shop.router)
    app.include_router(stories.router)
    app.include_router(play.router)
    app.include_router(admin.router)
    app.include_router(editor.router)
    try:
        from akomythatts.app import TtsApp

        app.state.tts = TtsApp.assemble()
    except Exception:
        logging.getLogger("acomytha").exception("Moteur TTS non chargé")
        app.state.tts = None

    @app.get("/api/health")
    def health():
        return {
            "ok": True,
            "name": "acomytha",
            "modes": ["accueil", "parent", "enfant", "admin", "editeur"],
            "tts": getattr(app.state, "tts", None) is not None,
        }

    frontend = settings.frontend_dir
    if frontend.exists():
        assets = frontend / "css"
        if assets.exists():
            app.mount("/css", StaticFiles(directory=frontend / "css"), name="css")
        app.mount("/js", StaticFiles(directory=frontend / "js"), name="js")
        if (frontend / "assets").exists():
            app.mount("/assets", StaticFiles(directory=frontend / "assets"), name="assets")

        @app.get("/")
        def index():
            return FileResponse(frontend / "index.html")

        @app.get("/manifest.webmanifest")
        def manifest():
            return FileResponse(frontend / "manifest.webmanifest", media_type="application/manifest+json")

    return app


def app() -> FastAPI:
    """Point d'entrée uvicorn `acomytha.main:app` — factory wrapping."""
    return create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("acomytha.main:create_app", factory=True, host="127.0.0.1", port=8787, reload=True)
