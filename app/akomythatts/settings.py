"""Chemins du moteur TTS, dans AkoMythaTTS autonome ou dans AcoMytha."""

from __future__ import annotations

from pathlib import Path


class Settings:
    """Chemins JSON, voix, jobs et checkpoints OpenVoice."""

    def __init__(self, root: Path | None = None, **overrides) -> None:
        package_dir = Path(__file__).resolve().parent
        default_root = package_dir.parent
        # Paquet copié dans app/akomythatts → racine = dépôt AcoMytha.
        if (default_root / "akomythatts").is_dir() and (default_root.parent / "stories").is_dir():
            default_root = default_root.parent
        self.root = (root or default_root).resolve()
        json_dir = self.root / "stories" / "json"
        self.stories_json_dir = json_dir
        if (self.root / "app" / "acomytha").is_dir():
            self.web_dir = self.root / "app" / "frontend"
            self.static_dir = self.web_dir
            self.jobs_dir = self.root / "app" / "data" / "tts_jobs"
            self.catalogue_path = json_dir / "voice_registry.json"
            voices = self.root / "stories" / "voices"
            self.voices_dir = voices if voices.exists() else (self.root / "app" / "data" / "voices")
            self.api_prefix = "/api/editor"
        else:
            self.web_dir = self.root / "web"
            self.static_dir = self.web_dir / "static"
            self.jobs_dir = self.web_dir / "jobs"
            self.api_prefix = "/api"
            classic = self.root / "catalogue" / "voice_registry.json"
            self.catalogue_path = json_dir / "voice_registry.json" if (json_dir / "voice_registry.json").exists() or not classic.parent.exists() else classic
            self.voices_dir = self.root / "voices"
        self.characters_dir = self.voices_dir / "characters"
        self.defaults_dir = self.voices_dir / "defaults"
        local_ckpt = self.root / "vendor" / "OpenVoice" / "checkpoints_v2"
        sibling_ckpt = Path("/media/laghmari/ssd-data/dev/AkoMythaTTS/vendor/OpenVoice/checkpoints_v2")
        self.checkpoints = local_ckpt if local_ckpt.is_dir() else sibling_ckpt
        self.host = "127.0.0.1"
        self.port = 8765
        self.sample_rate = 24_000
        for key, value in overrides.items():
            setattr(self, key, value)

    def ensure_dirs(self) -> None:
        for path in (
            self.jobs_dir,
            self.characters_dir,
            self.defaults_dir,
            self.catalogue_path.parent,
            self.stories_json_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)

    def resolve_story_json(self, story_id: str) -> Path:
        """Fichier plat stories/json/<story_id>.json — pas de sous-dossier."""
        name = Path(str(story_id or "").strip()).name
        if not name:
            raise ValueError("Identifiant d'histoire manquant.")
        if not name.endswith(".json"):
            name = f"{name}.json"
        root = self.stories_json_dir.resolve()
        path = (root / name).resolve()
        if path.parent != root:
            raise ValueError("Chemin d'histoire invalide.")
        return path
