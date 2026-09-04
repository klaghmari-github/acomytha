#!/usr/bin/env python3
"""avis2 — polir TREE-AUT-001 : oral plus lié, morale vécue, T1 dans le voyage."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-AUT-001"
REPL = (
    ("enfant-m|Celle-ci, la coque.", "enfant-m|Celle-ci, c'est la coque."),
    ("enfant-m|Et ça, la cheminée.", "enfant-m|Et ça, c'est la cheminée."),
    ("maman|Le manteau, Amir.", "maman|Prends le manteau, Amir."),
    ("narrateur|Amir regarde.", "narrateur|Amir s'accroupit, et il regarde."),
    ("papa|À toi, capitaine.", "papa|C'est à toi, capitaine."),
    ("enfant-m|Quai Deux.", "enfant-m|Celui-ci, c'est le quai Deux."),
    ("narrateur|Amir raconte :", "narrateur|Amir raconte, tout doux."),
    ("papa|Nouveau départ.", "papa|On reprend plus loin, alors."),
    ("enfant-m|Mon chemin disparaît.", "enfant-m|Mon chemin s'en va dans le sable."),
    ("enfant-m|Celui-là, pour demain.", "enfant-m|Celui-là, on le fera demain."),
    (
        "papa|Changer de chemin, ce n'est pas perdre.",
        "papa|Tu as trouvé une autre rivière.",
    ),
    ("enfant-m|Aujourd'hui, mon bateau a marché.", "enfant-m|Mon bateau a marché sur le sable."),
    ("papa|Un bateau de terre, aujourd'hui.", "papa|Un bateau de terre, pour cette fois."),
    (
        "narrateur|Sur le tapis, Amir plie un coin de papier.",
        "narrateur|En ce moment, Amir plie un coin de papier.",
    ),
)

# Extra lived line on destination chunks so T1 accessory is in the adventure, not only the fin.
T1_BEAT = {
    "CHK_T0001_P0001": "narrateur|Le manteau tiède frotte le sac.",
    "CHK_T0001_P0002": "narrateur|Les bottes font clap, déjà, dans l'entrée.",
    "CHK_T0001_P0003": "narrateur|Le linge sent encore le radiateur.",
}
SPLIT_RE = re.compile(r"(?<=[.?!])\s+")


def _cut(role: str, p: str) -> list[str]:
    for sep in (", ", " et ", " puis ", " entre "):
        if sep in p:
            a, b = p.split(sep, 1)
            a = a.strip()
            if not a.endswith((".", "?", "!")):
                a = a + "."
            b = b.strip()
            if sep == " entre ":
                b = "Entre " + b
            if not b.endswith((".", "?", "!")):
                b = b + "."
            if b and b[0].islower() and sep != " entre ":
                b = b[0].upper() + b[1:]
            return [f"{role}|{a}", f"{role}|{b}"]
    toks = p.rstrip(".?!").split()
    mid = max(3, len(toks) // 2)
    a = " ".join(toks[:mid]) + "."
    b = " ".join(toks[mid:]) + ("." if not p.endswith("?") else "?")
    b = b[0].upper() + b[1:]
    return [f"{role}|{a}", f"{role}|{b}"]


def split_line(ln: str, lim: int) -> list[str]:
    role, ph = ln.split("|", 1)
    parts = [p.strip() for p in SPLIT_RE.split(ph.strip()) if p.strip()]
    out = []
    for p in parts:
        if not p.endswith((".", "?", "!")):
            p = p + "."
        if words(p) > lim:
            out.extend(_cut(role, p))
        else:
            out.append(f"{role}|{p}")
    return out or [ln]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    for c in src["chunks"]:
        script = c.get("script") or ""
        for old, new in REPL:
            script = script.replace(old, new)
        cid = c["chunk_id"]
        # destination arrivals: P0001_T0002_P0001 / P0002 / P0003 (after T2 choice)
        if cid.endswith("T0002_P0001") or cid.endswith("T0002_P0002") or cid.endswith("T0002_P0003"):
            if "T0003" not in cid:
                prefix = cid[: len("CHK_T0001_P0001")]
                beat = T1_BEAT.get(prefix)
                if beat and beat not in script:
                    script = script.rstrip() + "\n" + beat
        lim = LIMITS["N1"]
        lines = []
        for ln in script.splitlines():
            if "|" not in ln:
                continue
            lines.extend(split_line(ln, lim))
        script = "\n".join(lines)
        c["script"] = script
        text, _ = from_script(script.splitlines())
        c["text"] = text
        c["text_ssml"] = text
    src["fil_rouge"] = (
        "Amir veut faire voyager son bateau dans les chemins d'eau du jardin. "
        "Chaque lieu a son obstacle. L'accessoire change le voyage."
    )
    check(SID, src["age_band"], src["chunks"])
    (ROOT / SID / "merged.json").write_text(
        json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    relecture(
        SID,
        src.get("title") or "",
        "morale retirée, oral un peu plus lié, T1 dans le lieu",
        "avis2. Audio non cuit. Les 27 chemins non écoutés à voix haute.",
    )


if __name__ == "__main__":
    main()
