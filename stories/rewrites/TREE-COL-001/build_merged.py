#!/usr/bin/env python3
"""TREE-COL-001 — voyage des pommes (avis 88534be). N2."""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = json.loads((HERE / "source.json").read_text(encoding="utf-8"))
BY = {c["chunk_id"]: c for c in SRC["chunks"]}


def pack(cid: str, lines: list[tuple[str, str]]) -> dict:
    src = BY[cid]
    script = "\n".join(f"{r}|{p}" for r, p in lines)
    text = " ".join(p for _, p in lines)
    return {
        "chunk_id": cid,
        "kind": src["kind"],
        "text": text,
        "script": script,
        "sons": src.get("sons") or "",
        "length_scale_piper": src.get("length_scale_piper") or 1.22,
        "rate_label": src.get("rate_label") or "slow",
        "pause_after_ms": src.get("pause_after_ms"),
    }


CHUNKS: list[dict] = []

CHUNKS.append(
    pack(
        "CHK_T0000_P0000",
        [
            ("narrateur", "Une goutte glisse le long de la casserole."),
            ("narrateur", "Ça sent la pomme, toute douce."),
            ("narrateur", "Le torchon rayé pend près de l'évier."),
            ("narrateur", "Dehors, le marché parle tout bas."),
            ("narrateur", "Un rond de soleil se pose sur le carrelage."),
            ("narrateur", "Papa a mis des rondelles dans un bol jaune."),
            ("narrateur", "En ce moment, Raphaël tient une cuillère en bois."),
            ("enfant-m", "Je veux donner des pommes à Mila."),
            ("enfant-m", "On fait le voyage des pommes."),
            ("maman", "Elle arrive tout à l'heure."),
            ("papa", "Tu prends un véhicule, en attendant ?"),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0000",
        [
            ("narrateur", "Qu'est-ce que Raphaël prend ?"),
            ("narrateur", "Le train, le bus, ou la voiture."),
        ],
    )
)

# train
CHUNKS.append(
    pack(
        "CHK_T0001_P0001",
        [
            ("narrateur", "Raphaël prend le train en bois."),
            ("narrateur", "Les roues font un petit clic sur le carrelage."),
            ("narrateur", "La porte s'ouvre. Mila entre, les joues roses."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour, Raphaël."),
            ("narrateur", "Le train s'arrête près de ses pieds."),
            ("enfant-m", "C'est le voyage des pommes."),
            ("enfant-f", "J'apporte le bol ?"),
            ("papa", "Il est un peu lourd."),
            ("enfant-m", "On le met sur le train."),
            ("narrateur", "Ils glissent le bol jaune entre deux wagons."),
            ("enfant-f", "Merci. Il tient."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0001_Q0001", [("narrateur", "Mila arrive. Raphaël dit quoi ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_C0001",
        [
            ("narrateur", "Raphaël a dit bonjour."),
            ("narrateur", "Le bol est sur le train."),
            ("enfant-m", "On cherche l'arrêt."),
            ("maman", "Choisissez l'endroit."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0000",
        [
            ("narrateur", "L'arrêt, c'est où ?"),
            ("narrateur", "La table, la fenêtre, ou le tabouret."),
        ],
    )
)

# bus
CHUNKS.append(
    pack(
        "CHK_T0001_P0002",
        [
            ("narrateur", "Raphaël prend le bus rouge."),
            ("narrateur", "Dehors, un vrai bus passe, tout bas."),
            ("narrateur", "Mila pousse la porte."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour."),
            ("narrateur", "Une miette colle au rebord du bol."),
            ("enfant-m", "Le torchon, s'il te plaît."),
            ("maman", "Le voilà."),
            ("enfant-m", "Merci."),
            ("narrateur", "Il essuie. Le bol est propre."),
            ("enfant-f", "Les pommes montent dans le bus."),
            ("narrateur", "Ils posent deux rondelles sur les sièges."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0002_Q0001", [("narrateur", "Raphaël veut le torchon. Que dit-il ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_C0001",
        [
            ("narrateur", "Raphaël a dit s'il te plaît."),
            ("narrateur", "Le torchon a servi. Le bus est chargé."),
            ("enfant-f", "On cherche l'arrêt."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0000",
        [
            ("narrateur", "L'arrêt, c'est où ?"),
            ("narrateur", "La table, la fenêtre, ou le tabouret."),
        ],
    )
)

# voiture
CHUNKS.append(
    pack(
        "CHK_T0001_P0003",
        [
            ("narrateur", "Raphaël prend la petite voiture."),
            ("narrateur", "Elle est lisse, un peu froide."),
            ("narrateur", "Mila arrive. Son manteau sent la pluie."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour."),
            ("enfant-f", "Tu accroches mon manteau, s'il te plaît ?"),
            ("maman", "Oui."),
            ("narrateur", "Maman accroche le manteau."),
            ("enfant-f", "Merci."),
            ("papa", "Une rondelle pour la route ?"),
            ("enfant-m", "Oui, merci."),
            ("narrateur", "Il pose la rondelle sur le capot, pour de faux."),
            ("enfant-m", "Cargaison prête."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0003_Q0001", [("narrateur", "Papa donne une rondelle. Que dit Raphaël ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_C0001",
        [
            ("narrateur", "Raphaël a dit merci."),
            ("narrateur", "La voiture a sa cargaison."),
            ("enfant-m", "On cherche l'arrêt."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0000",
        [
            ("narrateur", "L'arrêt, c'est où ?"),
            ("narrateur", "La table, la fenêtre, ou le tabouret."),
        ],
    )
)


def pre(t1: int) -> str:
    return {1: "CHK_T0001_P0001", 2: "CHK_T0001_P0002", 3: "CHK_T0001_P0003"}[t1]


VEH = {1: "le train", 2: "le bus", 3: "la voiture"}

T2_ARRIVE = {
    1: {  # table
        1: [
            ("narrateur", "Ils poussent le train jusqu'à la table."),
            ("narrateur", "Le bol jaune glisse un peu. Raphaël le rattrape."),
            ("enfant-m", "Arrêt table."),
            ("enfant-f", "On décharge ici."),
            ("narrateur", "Mila tire une chaise. Raphaël pose deux assiettes."),
            ("maman", "Vous avez besoin d'aide ?"),
            ("enfant-m", "On fait le voyage."),
        ],
        2: [
            ("narrateur", "Le bus rouge arrive contre la table."),
            ("enfant-m", "Arrêt table. Portes."),
            ("narrateur", "Mila ouvre la petite porte. Les rondelles descendent."),
            ("narrateur", "Raphaël pose une assiette. Mila l'autre."),
            ("enfant-f", "Ticket pomme."),
        ],
        3: [
            ("narrateur", "La voiture tourne autour de la table."),
            ("narrateur", "Une goutte du manteau a séché."),
            ("enfant-m", "Parking table."),
            ("narrateur", "Ils glissent la rondelle du capot dans une assiette."),
            ("enfant-f", "Livraison faite. Presque."),
        ],
    },
    2: {  # fenêtre
        1: [
            ("narrateur", "Le train va près de la fenêtre."),
            ("narrateur", "La vitre est un peu floue."),
            ("enfant-f", "Je dessine l'arrêt, dans la buée."),
            ("narrateur", "Mila trace un petit rond."),
            ("enfant-m", "J'essuie juste à côté. Le rond reste."),
            ("narrateur", "Le marché apparaît autour du rond."),
            ("enfant-m", "Arrêt fenêtre."),
        ],
        2: [
            ("narrateur", "Le bus va près de la fenêtre."),
            ("narrateur", "Un vrai bus passe dans la rue."),
            ("enfant-m", "On suit le grand."),
            ("narrateur", "Mila essuie un coin. Raphaël garde un trait de buée."),
            ("enfant-f", "C'est notre ligne."),
            ("enfant-m", "Arrêt fenêtre."),
        ],
        3: [
            ("narrateur", "La voiture va près de la fenêtre."),
            ("narrateur", "Mila dessine une route dans la buée."),
            ("enfant-m", "J'essuie le bas. La route du haut reste."),
            ("narrateur", "La petite voiture suit le trait."),
            ("enfant-f", "Arrêt fenêtre."),
        ],
    },
    3: {  # tabouret
        1: [
            ("narrateur", "Le train glisse jusqu'au tabouret."),
            ("narrateur", "Le tabouret est bas, en bois clair."),
            ("enfant-f", "Je m'assois. C'est la gare haute."),
            ("enfant-m", "Je peux après ?"),
            ("enfant-f", "Oui. Quand le bol est arrivé."),
            ("narrateur", "Raphaël pose le bol sur le bois, près d'elle."),
            ("narrateur", "Le tabouret fait un petit craquement."),
        ],
        2: [
            ("narrateur", "Le bus s'arrête au pied du tabouret."),
            ("enfant-m", "Arrêt tabouret. On monte la cargaison."),
            ("narrateur", "Mila s'assoit. Les pieds balancent."),
            ("narrateur", "Raphaël hisse le bol à côté d'elle."),
            ("enfant-f", "Gare haute. Les pommes voient tout."),
        ],
        3: [
            ("narrateur", "La voiture arrive au tabouret."),
            ("enfant-m", "Je monte la voiture, tout doux ?"),
            ("enfant-f", "Oui. Sur le bois."),
            ("narrateur", "Il pose la voiture près d'elle. Le bol suit."),
            ("enfant-f", "Parking haut."),
        ],
    },
}

T3_Q = [
    ("narrateur", "Qui pousse pour livrer ?"),
    ("narrateur", "Mila, Raphaël, ou tous les deux."),
]


def t3_play(t1: int, t2: int, t3: int) -> list[tuple[str, str]]:
    v = VEH[t1]
    if t3 == 1:  # Mila
        who = [
            ("enfant-f", "Je pousse."),
            ("enfant-m", "Moi, je garde les pommes."),
            ("narrateur", "Mila pousse " + v + ", tout autour de l'arrêt."),
        ]
    elif t3 == 2:  # Raphaël
        who = [
            ("enfant-m", "Je pousse."),
            ("enfant-f", "Moi, je dis les arrêts."),
            ("narrateur", "Raphaël pousse " + v + ". Mila annonce."),
            ("enfant-f", "Prochain : les assiettes."),
        ]
    else:
        who = [
            ("enfant-m", "Ensemble."),
            ("enfant-f", "Toi devant. Moi derrière."),
            ("narrateur", "Ils poussent " + v + " avec quatre mains."),
        ]
    # deliver
    deliver = [
        ("narrateur", "Le bol avance. Une rondelle tremble, puis tient."),
        ("enfant-m", "Terminus, les pommes."),
        ("narrateur", "Ils posent une rondelle chacun."),
        ("enfant-f", "On croque."),
        ("narrateur", "Ça croque, tout doux. Ça sent encore le fruit."),
    ]
    return who + deliver


def t3_fin(t1: int, t2: int, t3: int) -> list[tuple[str, str]]:
    park = {
        (1, 1): "Le train s'arrête contre le bol jaune.",
        (1, 2): "Le train rentre sous le rebord.",
        (1, 3): "Le train dort sous le tabouret.",
        (2, 1): "Le bus reste collé à l'assiette.",
        (2, 2): "Le petit bus s'endort contre la vitre.",
        (2, 3): "Le bus dort sous le tabouret.",
        (3, 1): "La voiture se gare contre le bol.",
        (3, 2): "La voiture s'arrête au bas de la vitre.",
        (3, 3): "La voiture descend du tabouret.",
    }[(t1, t2)]
    gag = {
        1: ("enfant-m", "Terminus, les pommes."),
        2: ("enfant-f", "Ticket utilisé."),
        3: ("enfant-m", "Cargaison livrée."),
    }[t1]
    lines = [
        ("narrateur", park),
        gag,
        ("papa", "Vous avez fait le voyage."),
        ("narrateur", "Les assiettes sont vides, maintenant."),
        ("narrateur", "L'histoire est finie."),
    ]
    return lines


for t1 in (1, 2, 3):
    p = pre(t1)
    for t2 in (1, 2, 3):
        CHUNKS.append(pack(f"{p}_T0002_P000{t2}", T2_ARRIVE[t2][t1]))
        CHUNKS.append(pack(f"{p}_T0002_P000{t2}_T0003_P0000", T3_Q))
        for t3 in (1, 2, 3):
            CHUNKS.append(pack(f"{p}_T0002_P000{t2}_T0003_P000{t3}", t3_play(t1, t2, t3)))
            CHUNKS.append(pack(f"{p}_T0002_P000{t2}_T0003_P000{t3}_F0001", t3_fin(t1, t2, t3)))


def word_count(s: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9']+", s))


def main() -> None:
    ids_src = [c["chunk_id"] for c in SRC["chunks"]]
    by = {c["chunk_id"]: c for c in CHUNKS}
    missing = [i for i in ids_src if i not in by]
    if missing:
        raise SystemExit(f"missing {missing[:10]} n={len(by)}")
    long_lines = []
    bravo = stp = merci = 0
    for c in CHUNKS:
        t = (c["text"] or "").lower()
        bravo += t.count("bravo")
        stp += t.count("s'il te plaît")
        merci += t.count("merci")
        for line in c["script"].splitlines():
            phrase = line.split("|", 1)[1] if "|" in line else line
            n = word_count(phrase)
            if n > 16:
                long_lines.append((c["chunk_id"], n, phrase))
    payload = {
        "story_id": "TREE-COL-001",
        "fil_rouge": (
            "Raphaël veut donner des pommes à Mila. Ils font le voyage des pommes "
            "avec un train, un bus ou une voiture, jusqu'à un arrêt. "
            "Ils poussent, ils livrent, ils croquent."
        ),
        "title": "Le voyage des pommes de Raphaël",
        "lesson_id": "COL.POL.001",
        "age_band": "N2",
        "kind": "ramifiee",
        "characters": "Raphaël, Mila, maman, papa",
        "setting": "dans la cuisine",
        "chunks": [by[i] for i in ids_src],
    }
    out = HERE / "merged.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} n=86 bravo={bravo} stp={stp} merci={merci} long>16={len(long_lines)}")
    for x in long_lines[:10]:
        print(" ", x)


if __name__ == "__main__":
    main()
