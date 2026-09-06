"""Index des personnages et des histoires sur tout le catalogue JSON."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .catalogue import CharacterCatalogue
from .detector import CharacterDetector
from .parser import StoryParser
from .settings import Settings
from .utils import Utils

LOG = logging.getLogger("akomythatts.roster")


class Roster:
    """Index du catalogue JSON : vue personnages et vue histoires."""

    def __init__(
        self,
        settings: Settings,
        catalogue: CharacterCatalogue,
        parser: StoryParser,
        detector: CharacterDetector,
    ) -> None:
        self.settings = settings
        self.catalogue = catalogue
        self.parser = parser
        self.detector = detector

    def public(self) -> dict[str, Any]:
        characters, stories = self.build()
        return {
            "folder": "stories/json",
            "stories": len(stories),
            "characters": len(characters),
            "missing": sum(1 for item in characters if not item["has_fingerprint"]),
            "items": characters,
            "by_story": stories,
        }

    def build(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        grouped: dict[str, dict[str, Any]] = {}
        stories: list[dict[str, Any]] = []
        for path in self._story_paths():
            try:
                parsed = self.parser.parse_path(path)
            except Exception as exc:
                LOG.warning("Roster : %s illisible (%s)", path.name, exc)
                continue
            story_id = path.stem
            title = parsed.title or story_id
            story_ref = {"story_id": story_id, "title": title}
            cast_rows: list[dict[str, Any]] = []
            seen: set[str] = set()
            for member in self.detector.detect(parsed):
                profile_id = member.suggested_profile_id or member.speaker_key
                person = {
                    "id": profile_id,
                    "display_name": member.given_name,
                    "role": member.role,
                    "gender": member.gender,
                    "age_group": member.age_group,
                }
                if profile_id not in seen:
                    cast_rows.append(person)
                    seen.add(profile_id)
                entry = grouped.get(profile_id)
                if entry is None:
                    grouped[profile_id] = {**person, "stories": [story_ref]}
                    continue
                if not any(row["story_id"] == story_id for row in entry["stories"]):
                    entry["stories"].append(story_ref)
            stories.append({"story_id": story_id, "title": title, "characters": cast_rows})
        root = self.settings.root
        characters: list[dict[str, Any]] = []
        fingerprints: dict[str, dict[str, Any]] = {}
        for profile_id, entry in grouped.items():
            profile = self.catalogue.get(profile_id)
            if profile:
                entry["display_name"] = profile.display_name
                entry["role"] = profile.role
                entry["gender"] = profile.gender
                entry["age_group"] = profile.age_group
                entry["has_fingerprint"] = profile.has_audio(root)
            else:
                entry["has_fingerprint"] = False
            entry["story_count"] = len(entry["stories"])
            fingerprints[profile_id] = entry
            characters.append(entry)
        for story in stories:
            for person in story["characters"]:
                ready = fingerprints.get(person["id"])
                if ready:
                    person["display_name"] = ready["display_name"]
                    person["role"] = ready["role"]
                    person["gender"] = ready["gender"]
                    person["age_group"] = ready["age_group"]
                    person["has_fingerprint"] = ready["has_fingerprint"]
                else:
                    person["has_fingerprint"] = False
            story["character_count"] = len(story["characters"])
            story["missing"] = sum(1 for person in story["characters"] if not person["has_fingerprint"])
        characters.sort(
            key=lambda row: (
                row["has_fingerprint"],
                {"character": 0, "child": 1, "narrator": 2, "father": 3, "mother": 4}.get(row["role"], 9),
                row["display_name"].casefold(),
            )
        )
        stories.sort(key=lambda row: row["title"].casefold())
        return characters, stories

    def _story_paths(self) -> list[Path]:
        folder = self.settings.stories_json_dir
        if not folder.is_dir():
            return []
        return Utils.story_json_paths(folder)
