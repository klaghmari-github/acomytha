"""Détecte les personnages d'une histoire et les relie au catalogue."""

from __future__ import annotations

import re

from .catalogue import TROUPE, CharacterCatalogue
from .models import CastMember, CharacterProfile, ParsedStory
from .utils import Utils


class CharacterDetector:
    """Relie les locuteurs d'une histoire aux profils du catalogue."""

    ROLE_DEFAULTS = {
        "narrator": ("Narratrice", "female", "adult", "narrator", "narrator"),
        "father": ("Papa", "male", "adult", "father", "father"),
        "mother": ("Maman", "female", "adult", "mother", "mother"),
        "child_boy": ("Enfant garçon", "male", "child", "child", "child_boy"),
        "child_girl": ("Enfant fille", "female", "child", "child", "child_girl"),
        "teacher": ("Maîtresse", "female", "adult", "character", "teacher"),
    }

    def __init__(self, catalogue: CharacterCatalogue) -> None:
        self.catalogue = catalogue

    def detect(self, story: ParsedStory) -> list[CastMember]:
        named = self._named_people(story.characters_hint)
        hero = self._hero_from_names(named)
        members: list[CastMember] = []
        seen: set[str] = set()
        for key in story.speaker_keys:
            member = self._resolve(key, named, hero)
            if member.speaker_key in seen:
                continue
            seen.add(member.speaker_key)
            members.append(member)
        return members

    def _resolve(self, key: str, named: list[str], hero: str | None) -> CastMember:
        raw = key.strip()
        lowered = raw.casefold()
        if lowered.startswith("character."):
            slug = lowered.split(".", 1)[1]
            return self._from_slug(raw, slug)
        if lowered in self.ROLE_DEFAULTS and lowered in {"father", "mother", "narrator", "child_boy", "child_girl", "teacher"}:
            if lowered == "child_boy" and hero:
                return self._from_given_name(hero, role="character", speaker_key=key)
            if lowered == "child_girl" and hero:
                girl = hero if self._gender_of(hero) == "female" else self._first_of_gender(named, "female")
                if girl:
                    return self._from_given_name(girl, role="character", speaker_key=key)
            return self._from_role(key, lowered)
        slug = self.slug(raw)
        if slug in TROUPE:
            return self._from_slug(raw, slug)
        by_name = self.catalogue.find_by_name(raw)
        if by_name:
            return self._member_from_profile(key, by_name)
        if lowered in {"papa", "père", "dad"}:
            named_father = self._named_parent(named, "father")
            if named_father:
                return self._from_given_name(named_father, role="father", speaker_key=key)
            return self._from_role(key, "father")
        if lowered in {"maman", "mère", "mom"}:
            named_mother = self._named_parent(named, "mother")
            if named_mother:
                return self._from_given_name(named_mother, role="mother", speaker_key=key)
            return self._from_role(key, "mother")
        return CastMember(
            speaker_key=key,
            given_name=raw,
            gender="female",
            age_group="adult",
            role="character",
            profile_id=None,
            has_fingerprint=False,
            suggested_profile_id=f"character.{slug or 'inconnu'}",
        )

    def _from_role(self, speaker_key: str, role_key: str) -> CastMember:
        name, gender, age, role, profile_id = self.ROLE_DEFAULTS[role_key]
        profile = self.catalogue.get(profile_id)
        return CastMember(
            speaker_key=speaker_key,
            given_name=name,
            gender=gender,
            age_group=age,
            role=role,
            profile_id=profile_id if profile else None,
            has_fingerprint=bool(profile and profile.has_audio(self.catalogue.settings.root)),
            suggested_profile_id=profile_id,
        )

    def _from_slug(self, speaker_key: str, slug: str) -> CastMember:
        info = TROUPE.get(slug)
        profile_id = f"character.{slug}"
        profile = self.catalogue.get(profile_id)
        if info:
            name, gender, age = info
        elif profile:
            name, gender, age = profile.display_name, profile.gender, profile.age_group
        else:
            name, gender, age = slug.capitalize(), "female", "child"
        return CastMember(
            speaker_key=speaker_key,
            given_name=name,
            gender=gender,
            age_group=age,
            role="character",
            profile_id=profile.id if profile else None,
            has_fingerprint=bool(profile and profile.has_audio(self.catalogue.settings.root)),
            suggested_profile_id=profile_id,
        )

    def _from_given_name(self, name: str, role: str, speaker_key: str) -> CastMember:
        profile = self.catalogue.find_by_name(name)
        slug = self.slug(name)
        profile_id = profile.id if profile else f"character.{slug}"
        gender = profile.gender if profile else self._gender_of(name) or "female"
        age = profile.age_group if profile else (TROUPE.get(slug, (None, None, "child"))[2])
        return CastMember(
            speaker_key=speaker_key,
            given_name=name,
            gender=gender,
            age_group=age,
            role=role,
            profile_id=profile.id if profile else None,
            has_fingerprint=bool(profile and profile.has_audio(self.catalogue.settings.root)),
            suggested_profile_id=profile_id,
        )

    def _member_from_profile(self, speaker_key: str, profile: CharacterProfile) -> CastMember:
        return CastMember(
            speaker_key=speaker_key,
            given_name=profile.display_name,
            gender=profile.gender,
            age_group=profile.age_group,
            role=profile.role,
            profile_id=profile.id,
            has_fingerprint=profile.has_audio(self.catalogue.settings.root),
            suggested_profile_id=profile.id,
        )

    def _named_people(self, hint: str) -> list[str]:
        parts = [part.strip() for part in re.split(r"[,;/]| et ", hint or "") if part.strip()]
        names = []
        for part in parts:
            if part.casefold() in {"papa", "maman", "père", "mère", "narrateur", "narratrice"}:
                continue
            names.append(part)
        return names

    def _hero_from_names(self, named: list[str]) -> str | None:
        for name in named:
            if self.slug(name) in TROUPE:
                return name
        return named[0] if named else None

    def _first_of_gender(self, named: list[str], gender: str) -> str | None:
        for name in named:
            if self._gender_of(name) == gender:
                return name
        return None

    def _named_parent(self, named: list[str], role: str) -> str | None:
        return None

    def _gender_of(self, name: str) -> str | None:
        info = TROUPE.get(self.slug(name))
        return info[1] if info else None

    @staticmethod
    def slug(value: str) -> str:
        return Utils.slug(value)
