"""Adaptateur HTTP Flask autour de ``TtsApp``.

Aucune règle métier ici : lecture de la requête, appel de la façade,
réponse JSON ou fichier. L'éditeur AcoMytha n'a pas besoin de ce module.
"""

from __future__ import annotations

import json
import logging
import threading
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory

from .app import TtsApp
from .settings import Settings
from .utils import Utils


class WebApp:
    """Studio local : sert le HTML et expose TtsApp en HTTP."""

    def __init__(self, tts: TtsApp) -> None:
        self.tts = tts
        self.settings = tts.settings
        self.app = Flask(
            __name__,
            static_folder=str(tts.settings.static_dir),
            static_url_path="/static",
        )
        self._bind()

    def _bind(self) -> None:
        app = self.app
        app.after_request(self._no_store)
        app.add_url_rule("/", view_func=self.index)
        app.add_url_rule("/api/voices", view_func=self.list_voices, methods=["GET"])
        app.add_url_rule("/api/voices/presets", view_func=self.presets, methods=["GET"])
        app.add_url_rule("/api/voices/generate", view_func=self.generate_voice, methods=["POST"])
        app.add_url_rule("/api/voices/jobs/<job_id>", view_func=self.voice_job, methods=["GET"])
        app.add_url_rule("/api/voices/record", view_func=self.record_voice, methods=["POST"])
        app.add_url_rule("/api/roster", view_func=self.list_roster, methods=["GET"])
        app.add_url_rule("/api/stories", view_func=self.list_stories, methods=["GET"])
        app.add_url_rule("/api/stories/<story_id>", view_func=self.get_story, methods=["GET"])
        app.add_url_rule("/api/parse", view_func=self.parse_story, methods=["POST"])
        app.add_url_rule("/api/convert", view_func=self.convert_story, methods=["POST"])
        app.add_url_rule("/api/jobs/<job_id>", view_func=self.job_status, methods=["GET"])
        app.add_url_rule("/api/jobs/<job_id>/audio", view_func=self.job_audio, methods=["GET"])
        app.add_url_rule("/api/jobs/<job_id>/edit", view_func=self.job_edit, methods=["GET"])
        app.add_url_rule("/api/jobs/<job_id>/replicas/<int:index>/audio", view_func=self.replica_audio, methods=["GET"])
        app.add_url_rule("/api/jobs/<job_id>/replicas/regenerate", view_func=self.regenerate_replicas, methods=["POST"])
        app.add_url_rule("/api/jobs/<job_id>/replicas/<int:index>/record", view_func=self.record_replica, methods=["POST"])
        app.add_url_rule("/api/edits/<edit_id>", view_func=self.edit_status, methods=["GET"])

    def _no_store(self, response):
        if request.path.startswith("/static/") or request.path.startswith("/api/jobs/"):
            response.headers["Cache-Control"] = "no-store, max-age=0"
        return response

    def index(self):
        return send_from_directory(self.settings.static_dir, "index.html")

    def _fail(self, message: str, status: int = 400):
        return jsonify({"error": message}), status

    def _story_id_from_request(self) -> str:
        if request.form.get("story_id"):
            return str(request.form.get("story_id") or "").strip()
        if request.is_json:
            data = request.get_json(silent=True) or {}
            return str(data.get("story_id") or "").strip()
        return ""

    def _upload_pair(self):
        upload = request.files.get("file")
        if upload is None or not upload.filename:
            return None, None
        return upload.filename, upload.read()

    def list_voices(self):
        return jsonify(self.tts.voices_public())

    def list_roster(self):
        return jsonify(self.tts.roster_public())

    def list_stories(self):
        return jsonify(self.tts.list_stories())

    def get_story(self, story_id: str):
        try:
            return jsonify(self.tts.preview(story_id=story_id))
        except FileNotFoundError:
            return self._fail(f"Pas de JSON stories/json/{story_id}.json", 404)
        except Exception as exc:
            return self._fail(str(exc))

    def presets(self):
        return jsonify(self.tts.presets())

    def parse_story(self):
        story_id = self._story_id_from_request()
        try:
            if story_id:
                return jsonify(self.tts.preview(story_id=story_id))
            filename, payload = self._upload_pair()
            if not filename:
                return self._fail("Choisis un JSON dans stories/json/.")
            return jsonify(self.tts.preview(filename=filename, payload=payload))
        except FileNotFoundError:
            return self._fail(f"Pas de JSON stories/json/{story_id}.json", 404)
        except Exception as exc:
            return self._fail(str(exc))

    def generate_voice(self):
        data = request.get_json(force=True, silent=True) or {}
        profile_id = str(data.get("id") or "").strip()
        name = str(data.get("display_name") or "").strip()
        if not profile_id or not name:
            return self._fail("Nom et identifiant requis.")
        return jsonify(
            self.tts.generate_voice(
                profile_id=profile_id,
                display_name=name,
                gender=str(data.get("gender") or "female"),
                age_group=str(data.get("age_group") or "adult"),
                temperament=str(data.get("temperament") or "naturel"),
                role=str(data.get("role") or "character"),
            )
        )

    def voice_job(self, job_id: str):
        payload = self.tts.voice_job(job_id)
        if payload is None:
            return self._fail("Travail vocal introuvable.", 404)
        return jsonify(payload)

    def record_voice(self):
        upload = request.files.get("file")
        profile_id = str(request.form.get("id") or "").strip()
        name = str(request.form.get("display_name") or "").strip()
        if upload is None or not profile_id or not name:
            return self._fail("Fichier, nom et identifiant requis.")
        try:
            raw = self.tts.stash_upload(f"rec-{profile_id.replace('.', '_')}", upload)
        except ValueError as exc:
            return self._fail(str(exc))
        return jsonify(
            self.tts.record_voice(
                raw,
                profile_id=profile_id,
                display_name=name,
                gender=str(request.form.get("gender") or "female"),
                age_group=str(request.form.get("age_group") or "adult"),
                role=str(request.form.get("role") or "character"),
                temperament=str(request.form.get("temperament") or "naturel"),
            )
        )

    def convert_story(self):
        story_id = self._story_id_from_request()
        assignments_raw = request.form.get("assignments") or "{}"
        if request.is_json:
            body = request.get_json(silent=True) or {}
            if not request.form.get("assignments"):
                assignments_raw = json.dumps(body.get("assignments") or {})
        try:
            assignments = json.loads(assignments_raw)
            if not isinstance(assignments, dict):
                raise ValueError("assignments invalides")
            filename, payload = (None, None)
            if not story_id:
                filename, payload = self._upload_pair()
            return jsonify(self.tts.convert(story_id or None, assignments, filename=filename, payload=payload))
        except FileNotFoundError:
            return self._fail(f"Pas de JSON stories/json/{story_id}.json", 404)
        except Exception as exc:
            return self._fail(str(exc))

    def job_status(self, job_id: str):
        job = self.tts.job(job_id)
        if job is None:
            return self._fail("Travail introuvable.", 404)
        return jsonify(job.public())

    def job_audio(self, job_id: str):
        job = self.tts.job(job_id)
        if job is None:
            return self._fail("Travail introuvable.", 404)
        if job.status != "done" or job.wav is None:
            return self._fail("L'audio n'est pas encore prêt.", 409)
        safe = Utils.safe_filename(job.title)
        return send_file(job.wav, mimetype="audio/wav", as_attachment=False, download_name=f"{safe}.wav")

    def job_edit(self, job_id: str):
        try:
            return jsonify(self.tts.edit_public(job_id))
        except FileNotFoundError as exc:
            return self._fail(str(exc), 404)
        except RuntimeError as exc:
            return self._fail(str(exc), 409)

    def replica_audio(self, job_id: str, index: int):
        try:
            self.tts.edit_public(job_id)
        except FileNotFoundError as exc:
            return self._fail(str(exc), 404)
        except RuntimeError as exc:
            return self._fail(str(exc), 409)
        path = self.tts.replica_path(job_id, index)
        if not path.is_file():
            return self._fail(f"Réplique {index} introuvable.", 404)
        return send_file(path, mimetype="audio/wav", as_attachment=False, download_name=f"replique-{index:04d}.wav")

    def regenerate_replicas(self, job_id: str):
        data = request.get_json(silent=True) or {}
        try:
            indices = sorted({int(item) for item in (data.get("indices") or [])})
            return jsonify(self.tts.regenerate_replicas(job_id, indices))
        except FileNotFoundError as exc:
            return self._fail(str(exc), 404)
        except RuntimeError as exc:
            return self._fail(str(exc), 409)
        except (TypeError, ValueError) as exc:
            return self._fail(str(exc) if str(exc) else "Indices de répliques invalides.")

    def record_replica(self, job_id: str, index: int):
        upload = request.files.get("file")
        if upload is None:
            return self._fail("Fichier audio requis.")
        raw = None
        try:
            raw = self.tts.stash_upload(f"line-{job_id}-{index}", upload)
            return jsonify(self.tts.record_replica(job_id, index, raw))
        except FileNotFoundError as exc:
            return self._fail(str(exc), 404)
        except RuntimeError as exc:
            return self._fail(str(exc), 409)
        except ValueError as exc:
            return self._fail(str(exc))
        except Exception as exc:
            logging.exception("enregistrement de réplique")
            return self._fail(str(exc), 500)
        finally:
            Utils.unlink(raw)

    def edit_status(self, edit_id: str):
        payload = self.tts.edit_work(edit_id)
        if payload is None:
            return self._fail("Édition introuvable.", 404)
        return jsonify(payload)

    def run(self) -> None:
        self.settings.ensure_dirs()
        threading.Thread(target=self.tts.warmup, daemon=True).start()
        print(f"AcoMythaTTS → http://{self.settings.host}:{self.settings.port}")
        self.app.run(host=self.settings.host, port=self.settings.port, debug=False, threaded=True)


def create_app(settings: Settings | None = None) -> WebApp:
    """Point d'assemblage du studio web."""
    return WebApp(TtsApp.assemble(settings))
