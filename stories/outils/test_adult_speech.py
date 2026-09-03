"""D20 — papa et maman parlent, ils ne sont pas un sourire du narrateur."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REWRITES = ROOT / "rewrites"

STORIES = (
    "ATOM-SAN.ALI.001-01",
    "ATOM-SAN.ALI.001-02",
    "ATOM-SAN.ALI.002-01",
)

FILLER = (
    "papa sourit",
    "maman sourit",
    "lina sourit",
    "noé sourit",
    "tom sourit",
    "papa est là.",
    "maman est là.",
)


def _scripts(story_id: str) -> str:
    data = json.loads((REWRITES / story_id / "merged.json").read_text(encoding="utf-8"))
    return "\n".join(str(c.get("script") or "") for c in data["chunks"])


def _adult_lines(script: str) -> list[str]:
    out = []
    for line in script.splitlines():
        if line.startswith("papa|") or line.startswith("maman|"):
            out.append(line.split("|", 1)[1])
    return out


def test_pas_de_sourire_narrateur():
    for sid in STORIES:
        nar = "\n".join(
            ln.split("|", 1)[1]
            for ln in _scripts(sid).splitlines()
            if ln.startswith("narrateur|")
        ).lower()
        for bad in FILLER:
            assert bad not in nar, f"{sid}: narrateur dit « {bad} »"


def test_adultes_felicite_et_demandent():
    for sid in STORIES:
        adults = _adult_lines(_scripts(sid))
        joined = " ".join(adults).lower()
        assert adults, f"{sid}: aucun papa/maman"
        assert "bravo" in joined or "bon travail" in joined, f"{sid}: pas de félicitation"
        assert any("?" in line for line in adults), f"{sid}: aucune question d'adulte"


def test_lina_maman_adapte_la_tomate():
    adults = " ".join(_adult_lines(_scripts("ATOM-SAN.ALI.001-01"))).lower()
    assert "bouchée" in adults or "goûter" in adults or "gouter" in adults
    assert "assis" in adults


def test_noe_papa_range_et_rattrape():
    adults = " ".join(_adult_lines(_scripts("ATOM-SAN.ALI.001-02"))).lower()
    assert "attrap" in adults
    assert "ranger le panier" in adults or "poses près de l'évier" in adults


def test_tom_papa_maman_parlent_tous_les_deux():
    script = _scripts("ATOM-SAN.ALI.002-01")
    papa = [ln for ln in script.splitlines() if ln.startswith("papa|")]
    maman = [ln for ln in script.splitlines() if ln.startswith("maman|")]
    assert papa and maman
    joined = " ".join(_adult_lines(script)).lower()
    assert "bateau" in joined
    assert "est là" not in joined
