#!/usr/bin/env python3
"""Génère ~100 arbres ramifiés 3×3×3, uniques par leçon / héros / lieu / choix."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from make_ramifiee import BY_ID, CHARACTERS, CHOICE_SETS, build_tree  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ramifiees"

SETTINGS = [
    "à la maison", "dans la cuisine", "au parc", "dans le jardin",
    "à l'école", "au marché", "dans la chambre", "près de la fenêtre",
    "dans le salon", "sur le chemin de l'école", "à la ferme",
    "dans le train avec papa", "au bord de la mer", "sous le pommier",
]

CHOICE_TRIPLES = [
    ("lieux_maison", "objets", "camarades"),
    ("lieux_parc", "jeux", "couleurs"),
    ("objets", "camarades", "moments"),
    ("jeux", "goûter", "animaux"),
    ("moments", "lieux_maison", "objets"),
    ("camarades", "jeux", "goûter"),
    ("animaux", "lieux_parc", "couleurs"),
    ("transports", "camarades", "moments"),
    ("goûter", "lieux_maison", "jeux"),
    ("couleurs", "objets", "animaux"),
]

AGE_CYCLE = ["N1", "N2", "N2", "N3"]


def main():
    lessons = list(BY_ID.values())
    # 100 trees: at least one per lesson, extras cycling popular V1
    plan = []
    for i, les in enumerate(lessons):
        plan.append((les["lesson_id"], i))
    extra_ids = [l["lesson_id"] for l in lessons if l.get("wave") in ("V1-pilote", "V1")]
    k = 0
    while len(plan) < 100:
        plan.append((extra_ids[k % len(extra_ids)], 1000 + k))
        k += 1

    written = []
    counts = {}
    for n, (lid, seed) in enumerate(plan, start=1):
        les = BY_ID[lid]
        dom = les["domain_id"]
        counts[dom] = counts.get(dom, 0) + 1
        seq = counts[dom]
        tree_id = f"TREE-{dom}-{seq:03d}"
        hero, pronoun = CHARACTERS[(n - 1) % len(CHARACTERS)]
        setting = SETTINGS[(n - 1) % len(SETTINGS)]
        choices = CHOICE_TRIPLES[(n - 1) % len(CHOICE_TRIPLES)]
        age = AGE_CYCLE[(n - 1) % len(AGE_CYCLE)]
        # N1 ramifié reste 3 options (consigne utilisateur) mais phrases courtes via age_band
        compat = [x for x in (les.get("compatible_lessons") or []) if x != lid]
        secondary = compat[0] if compat else None
        tree = build_tree(
            tree_id, lid, age, setting, hero, pronoun, choices, secondary, n
        )
        dest = OUT / dom / f"{tree_id}.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(tree, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(str(dest.relative_to(ROOT)))
    print(json.dumps({"count": len(written), "by_domain": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
