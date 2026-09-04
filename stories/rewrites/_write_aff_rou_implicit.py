#!/usr/bin/env python3
"""F-NAR-008 — bulletin « Bravo, tu as… » / « Tu as mis ce qu'il faut ? » → ligne vécue."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, relecture, write_story

NEVER = (
    "bravo, tu as",
    "bravo tu as",
    "tu as mis ce qu'il faut",
    "tu as mis ce qu’il faut",
    "on va apprendre",
    "on va ranger",
)

# Surgical: keep the arc, swap the recap. Not a packing list.
PATCH = {
    "ATOM-AUT.AFF.001-02": {
        "maman|Bravo, tu as préparé tout ça.": "maman|Le doudou est chaud, dans le sac.",
    },
    "ATOM-AUT.AFF.001-03": {
        "maman|Bravo, tu as préparé le pique-nique.": "maman|Le biscuit est encore tout chaud.",
    },
    "ATOM-AUT.AFF.001-04": {
        "maman|Bravo, tu as préparé la sortie.": "maman|Merci pour le sac, Mila.",
    },
    "ATOM-AUT.AFF.001-05": {
        "papa|Bravo, tu as préparé le jardin.": "papa|Le livre est au chaud, dedans.",
    },
    "ATOM-AUT.AFF.001-06": {
        "maman|Bravo, tu as préparé la sortie.": "maman|Merci pour le sac, Nina.",
    },
    "ATOM-AUT.AFF.001-07": {
        "papa|Bravo, tu as préparé le chemin.": "papa|Le doudou est chaud, contre toi.",
    },
    "ATOM-AUT.AFF.001-08": {
        "maman|Bravo, tu as préparé le seau.": "maman|Merci pour le seau, Victorina.",
    },
    "ATOM-AUT.ROU.001-01": {
        "papa|Bravo, tu as avancé tout doux.": "papa|Le wagon est chaud, sous tes doigts.",
    },
    "ATOM-AUT.ROU.001-03": {
        "narrateur|Nino met la gourde.": "narrateur|Nino glisse le doudou.",
        "narrateur|Il met le doudou.": "narrateur|Le tissu est encore chaud.",
        "papa|Tu as mis ce qu'il faut ?": "papa|Le pain est tout près ?",
    },
    "ATOM-AUT.ROU.001-04": {
        "narrateur|Elle met la gourde.": "narrateur|Le cabas sent encore le linge.",
        "narrateur|Elle met le petit sac aussi.": "narrateur|La gourde est fraîche, tout au fond.",
        "maman|Tu as mis ce qu'il faut ?": "maman|Les fraises sont tout près ?",
    },
}

NOTES = {
    "ATOM-AUT.AFF.001-02": (
        "La cour de Sarah",
        "Sarah veut Chouchou. Chapeau sous la chaise, zip coincé. Cour, linge, main.",
        "Bulletin « Bravo, tu as préparé » → doudou chaud dans le sac.",
    ),
    "ATOM-AUT.AFF.001-03": (
        "Le pique-nique de la pente",
        "Nino veut le biscuit dehors. Gourde trop froide, chapeau trop haut. Croûte, pierre.",
        "Bulletin « Bravo, tu as préparé » → biscuit encore chaud.",
    ),
    "ATOM-AUT.AFF.001-04": (
        "Le bateau de Mila",
        "Mila veut le bateau. Doudou caché, loquet coincé. Sel, bois, flot.",
        "Bulletin « Bravo, tu as préparé » → merci pour le sac.",
    ),
    "ATOM-AUT.AFF.001-05": (
        "L'escargot du jardin",
        "Raphaël veut l'escargot. Zip coincé. Coquille, flaque, terre.",
        "Bulletin « Bravo, tu as préparé » → livre au chaud.",
    ),
    "ATOM-AUT.AFF.001-06": (
        "La pomme du marché",
        "Nina veut la pomme. Cuillère en trop, chapeau sous la chaise. Peau lisse.",
        "Bulletin « Bravo, tu as préparé » → merci pour le sac.",
    ),
    "ATOM-AUT.AFF.001-07": (
        "La plume d'Aniss",
        "Aniss veut l'oiseau. Chapeau tombé, doudou oublié. Plume, cri, pin.",
        "Bulletin « Bravo, tu as préparé » → doudou chaud contre lui.",
    ),
    "ATOM-AUT.AFF.001-08": (
        "Le château de la rive",
        "Victorina veut le château. Seau mouillé. Mur, fleuve, sable.",
        "Bulletin « Bravo, tu as préparé » → merci pour le seau.",
    ),
    "ATOM-AUT.ROU.001-01": (
        "Le train de l'allée",
        "Chouchou veut l'allée. Roue perdue. Wagon sur les dalles tièdes.",
        "Bulletin « Bravo, tu as avancé » → wagon chaud sous les doigts.",
    ),
    "ATOM-AUT.ROU.001-03": (
        "Le pain chaud de Nino",
        "Nino veut le pain. Pyjama, marche trop tôt. Pull, marches, croûte.",
        "« Tu as mis ce qu'il faut » → le pain est tout près. Pas de liste.",
    ),
    "ATOM-AUT.ROU.001-04": (
        "Les fraises de Sarah",
        "Sarah veut les fraises. Cabas vide. Miel, marché, jus rouge.",
        "« Tu as mis ce qu'il faut » → les fraises sont tout près. Pas de liste.",
    ),
}


def load_merged(sid: str) -> dict:
    path = ROOT / sid / "merged.json"
    return json.loads(path.read_text(encoding="utf-8"))


def scripts_of(merged: dict, mapping: dict[str, str]) -> tuple[dict, dict, dict | None]:
    scripts: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    q = None
    pending = dict(mapping)
    for c in merged["chunks"]:
        cid = c["chunk_id"]
        lines = [ln for ln in c["script"].strip().splitlines() if ln.strip()]
        out = []
        for ln in lines:
            if ln in pending:
                out.append(pending.pop(ln))
            else:
                out.append(ln)
        scripts[cid] = out
        sons[cid] = c.get("sons") or ""
        if cid.endswith("_Q0001"):
            q = {
                "expected_answer": c.get("expected_answer"),
                "accepted_examples": c.get("accepted_examples"),
                "retry_prompt": c.get("retry_prompt"),
            }
    if pending:
        raise SystemExit(f"{merged['story_id']} lignes introuvables: {list(pending)}")
    return scripts, sons, q


def assert_lived(sid: str, scripts: dict) -> None:
    joined = "\n".join("\n".join(v) for v in scripts.values()).lower()
    for bad in NEVER:
        if bad in joined:
            raise SystemExit(f"{sid} encore interdit: {bad}")


def run_one(sid: str) -> None:
    merged = load_merged(sid)
    scripts, sons, q = scripts_of(merged, PATCH[sid])
    assert_lived(sid, scripts)
    write_story(
        sid,
        merged["fil_rouge"],
        merged["title"],
        merged["characters"],
        merged["setting"],
        scripts,
        sons,
        q,
    )
    title, vecu, notes = NOTES[sid]
    relecture(sid, title, vecu, notes)


def main() -> None:
    for sid in PATCH:
        run_one(sid)


if __name__ == "__main__":
    main()
