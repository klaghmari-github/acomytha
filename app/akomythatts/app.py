"""Façade unique du moteur.

AcoMytha (site officiel) branchera l'éditeur d'histoires / texte / voix
sur ``TtsApp`` : pas de Flask, pas d'HTML. Le studio local ``WebApp``
n'est qu'un adaptateur HTTP autour de cet objet.
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any

from .catalogue import CharacterCatalogue
from .converter import CatalogueConverter
from .detector import CharacterDetector
from .jobs import ConversionQueue
from .parser import StoryParser
from .roster import Roster
from .settings import Settings
from .studio import GENERATE_PRESETS, TEMPERAMENTS, VoiceStudio
from .utils import Utils


class TtsApp:
    """Assemble catalogue, parser, studio vocal et file de conversion.

    Toutes les opérations utiles à un éditeur (lister, parser, empreintes,
    convertir, éditer des répliques) passent par les méthodes publiques.
    """

    def __init__(
        self,
        settings: Settings,
        catalogue: CharacterCatalogue,
        parser: StoryParser,
        detector: CharacterDetector,
        roster: Roster,
        studio: VoiceStudio,
        queue: ConversionQueue,
    ) -> None:
        self.settings = settings
        self.catalogue = catalogue
        self.parser = parser
        self.detector = detector
        self.roster = roster
        self.studio = studio
        self.queue = queue

    @classmethod
    def assemble(cls, settings: Settings | None = None) -> TtsApp:
        """Construit le graphe d'objets (un exemplaire par processus)."""
        settings = settings or Settings()
        settings.ensure_dirs()
        catalogue = CharacterCatalogue(settings)
        parser = StoryParser()
        detector = CharacterDetector(catalogue)
        queue = ConversionQueue(settings, catalogue)
        studio = VoiceStudio(settings, catalogue, queue)
        roster = Roster(settings, catalogue, parser, detector)
        return cls(settings, catalogue, parser, detector, roster, studio, queue)

    def list_stories(self) -> dict[str, Any]:
        """JSON du dossier stories/json/ (hors rapports)."""
        items = []
        for path in Utils.story_json_paths(self.settings.stories_json_dir):
            data = Utils.load_json(path) or {}
            story_id = str(data.get("story_id") or path.stem)
            title = str(data.get("title") or path.stem)
            items.append({"story_id": story_id, "title": title, "filename": path.name})
        return {"folder": "stories/json", "stories": items}

    def parse_catalog(self, story_id: str):
        path = self.settings.resolve_story_json(story_id)
        if not path.is_file():
            raise FileNotFoundError(path.name)
        return self.parser.parse_path(path)

    def preview(self, story_id: str | None = None, filename: str | None = None, payload: bytes | None = None) -> dict[str, Any]:
        """Parse une histoire et attache le casting détecté."""
        if story_id:
            parsed = self.parse_catalog(story_id)
        elif filename and payload is not None:
            parsed = self.parser.parse_bytes(filename, payload)
        else:
            raise ValueError("Choisis un JSON dans stories/json/.")
        preview = parsed.to_preview(self.detector.detect(parsed))
        if story_id:
            preview["story_id"] = story_id
        return preview

    def roster_public(self) -> dict[str, Any]:
        return self.roster.public()

    def voices_public(self) -> dict[str, Any]:
        return {"voices": self.catalogue.list_public()}

    def presets(self) -> dict[str, Any]:
        return {
            "genders": ["female", "male"],
            "ages": ["child", "adult", "senior"],
            "temperaments": list(TEMPERAMENTS),
            "generate": [{"gender": gender, "age_group": age} for gender, age in GENERATE_PRESETS],
        }

    def generate_voice(self, **kwargs: Any) -> dict[str, Any]:
        work = self.studio.submit_generate(**kwargs)
        return work.public()

    def voice_job(self, job_id: str) -> dict[str, Any] | None:
        work = self.studio.get_work(job_id)
        return None if work is None else work.public()

    def stash_upload(self, prefix: str, upload) -> Path:
        """Enregistre un fichier micro/webm dans le dossier jobs."""
        suffix = Path(getattr(upload, "filename", None) or "rec.webm").suffix or ".webm"
        path = self.settings.jobs_dir / f"{prefix}-{uuid.uuid4().hex[:8]}{suffix}"
        path.parent.mkdir(parents=True, exist_ok=True)
        upload.save(path)
        if not path.is_file() or path.stat().st_size < 200:
            Utils.unlink(path)
            raise ValueError("Enregistrement trop court.")
        return path

    def record_voice(self, upload_path: Path, **kwargs: Any) -> dict[str, Any]:
        work = self.studio.submit_record(upload_path=upload_path, **kwargs)
        return work.public()

    def convert(self, story_id: str | None, assignments: dict[str, str], filename: str | None = None, payload: bytes | None = None) -> dict[str, Any]:
        if story_id:
            parsed = self.parse_catalog(story_id)
        elif filename and payload is not None:
            parsed = self.parser.parse_bytes(filename, payload)
        else:
            raise ValueError("Choisis un JSON dans stories/json/.")
        job = self.queue.submit(parsed, {str(k): str(v) for k, v in assignments.items()})
        return job.public()

    def job(self, job_id: str):
        return self.queue.get(job_id)

    def edit_public(self, job_id: str) -> dict[str, Any]:
        job = self.queue.get(job_id)
        if job is None:
            raise FileNotFoundError("Travail introuvable.")
        if job.status != "done":
            raise RuntimeError("L'audio n'est pas encore prêt.")
        return self.queue.edit_public(job)

    def replica_path(self, job_id: str, index: int) -> Path:
        return self.queue.book.replica_path(job_id, index)

    def regenerate_replicas(self, job_id: str, indices: list[int]) -> dict[str, Any]:
        job = self.queue.get(job_id)
        if job is None:
            raise FileNotFoundError("Travail introuvable.")
        if job.status != "done":
            raise RuntimeError("L'audio n'est pas encore prêt.")
        total = job.segments or len((job.edit or {}).get("replicas") or [])
        if not indices:
            raise ValueError("Coche au moins une réplique.")
        if any(index < 1 or (total and index > total) for index in indices):
            raise ValueError("Une réplique est hors limites.")
        return self.queue.submit_regenerate(job, indices).public()

    def record_replica(self, job_id: str, index: int, upload_path: Path) -> dict[str, Any]:
        job = self.queue.get(job_id)
        if job is None:
            raise FileNotFoundError("Travail introuvable.")
        if job.status != "done":
            raise RuntimeError("L'audio n'est pas encore prêt.")
        return self.queue.replace_recorded(job, index, upload_path)

    def edit_work(self, edit_id: str) -> dict[str, Any] | None:
        work = self.queue.get_edit(edit_id)
        return None if work is None else work.public()

    def convert_excel(self, source: Path | None = None, output: Path | None = None) -> dict[str, Any]:
        converter = CatalogueConverter(self.settings, self.catalogue)
        source = source or (self.settings.root / "stories" / "arbres")
        output = output or self.settings.stories_json_dir
        return converter.convert_directory(source, output)

    def warmup(self) -> None:
        """Précharge Kokoro (premier rendu plus court)."""
        try:
            logging.info("Préchargement de Kokoro…")
            with self.queue._engine_lock:
                self.queue.kokoro()
            logging.info("Kokoro prêt.")
        except Exception:
            logging.exception("Préchargement Kokoro impossible")
