#!/usr/bin/env python3
"""F-NAR-008 — helpers communs pour écrire merged.json (vraie histoire, pas des puces)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 16}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "copain", "copine", "maitresse"}
TROUPE_M = ("Amir", "Aniss", "Nino", "Raphaël", "Victorino")
TROUPE_F = ("Sarah", "Chouchou", "Mila", "Nina", "Victorina")
FORBIDDEN = (
    "on va apprendre",
    "voici le geste",
    "on va ranger",
    "après le jeu",
    "c'est la règle",
    "tu as suivi la règle",
    "même leçon",
    "tu as repris le geste",
    "tu ranges",
    "papa sourit",
    "maman sourit",
    "papa est là",
    "maman est là",
    "il était une fois",
    "ceci est l'histoire",
    "aujourd'hui,",
    "tu as fait du bon travail",
    "c'est du bon travail",
    "un chuchotement serre",
    "une étape après l'autre",
    "tu as mis ce que l'adulte a dit",
    "on met ce que l'adulte a dit",
    "l'histoire est finie",
    "bravo. tu as",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "il faut attendre",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom ", "léa", "lea ", "lina", "iris",
    "aïcha", "aicha", "clément", "clement", "léonie", "leonie",
    "clarisse", "éléonore", "eleonore", "dominique", "zoé", "zoe",
    "adam", "ariane", "benoît", "benoit", "delphine", "erwan",
    "kenzo", "alban", "agathe", "barnabé", "barnabe",
    "nora", "constentin", "constantin", "lucas", "luca", "céline",
    "celine", "alice",
)
OPENING_BAD = ("joue au salon", "est dans l'entrée", "c'est le matin", "va à l'école")


def words(s: str) -> int:
    return len(s.replace("'", " ").replace("’", " ").replace("-", " ").split())


def from_script(lines: list[str]) -> tuple[str, str]:
    phrases, out = [], []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        role, phrase = raw.split("|", 1)
        phrase = phrase.strip()
        out.append(f"{role}|{phrase}")
        phrases.append(phrase)
    return " ".join(phrases), "\n".join(out)


def make_chunk(src: dict, lines: list[str], sons, scale: float, rate: str) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["length_scale_piper"] = scale
    nc["rate_label"] = rate
    return nc


def _listy_run(script: str) -> str | None:
    """Quatre phrases d'affilée qui commencent par le même mot = puces, pas un récit."""
    starts: list[str] = []
    for ln in script.splitlines():
        if "|" not in ln:
            continue
        role, phrase = ln.split("|", 1)
        if role != "narrateur":
            starts.append("")
            continue
        tok = phrase.strip().split()
        starts.append(tok[0].lower() if tok else "")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                return starts[i]
        else:
            run = 1
    return None


def check(sid: str, age: str, chunks: list[dict]) -> None:
    lim = LIMITS.get(age) or 12
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        token = name.strip()
        if not re.search(rf"\b{re.escape(token)}\b", low):
            continue
        raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation vécue (merci/bravo une fois, dans la scène)")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in OPENING_BAD:
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    listed = _listy_run(joined)
    if listed:
        raise SystemExit(f"{sid}: puces (4 narrations d'affilée commencent par « {listed} »)")
    last_lines = [ln for ln in chunks[-1]["script"].splitlines() if ln.startswith("narrateur|")]
    if not last_lines:
        raise SystemExit(f"{sid}: la fin n'a pas de narrateur")
    last = last_lines[-1].split("|", 1)[1].lower()
    if "histoire" in last or "bravo" in last or "bon travail" in last:
        raise SystemExit(f"{sid}: fin mécanique: {last}")
    for c in chunks:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: text ≠ script")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                raise SystemExit(f"{sid} ligne sans | : {ln}")
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                raise SystemExit(f"{sid} rôle {role}")
            n = words(phrase)
            if n > lim:
                raise SystemExit(f"{sid} {c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    print(f"OK {sid} {nwords} mots  1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}")


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    q: dict | None = None,
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind == "passage_question":
            scale, rate = 1.28, "slow"
        else:
            scale, rate = 1.22, "medium"
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
    if q:
        qc = by.get("CHK_T0000_P0000_Q0001")
        if qc:
            for k, v in q.items():
                qc[k] = v
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def relecture(sid: str, title: str, vecu: str, notes: str) -> None:
    path = ROOT / sid / "RELECTURE.md"
    path.write_text(
        f"# {sid} — {title}\n\n"
        f"Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        f"`chunk_id` / `kind` inchangés.\n\n"
        f"## Vécu\n{vecu}\n\n"
        f"## Vu et corrigé\n{notes}\n\n"
        f"## Non vérifié\n"
        f"Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
