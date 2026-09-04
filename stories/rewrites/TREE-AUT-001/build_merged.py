#!/usr/bin/env python3
"""TREE-AUT-001 — Le bateau d'Amir et la flaque (exemple2 + avis 88534be)."""

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
        "length_scale_piper": src.get("length_scale_piper") or 1.28,
        "rate_label": src.get("rate_label") or "slow",
        "pause_after_ms": src.get("pause_after_ms"),
    }


CHUNKS: list[dict] = []

CHUNKS.append(
    pack(
        "CHK_T0000_P0000",
        [
            ("narrateur", "Sur le toit, la gouttière fait encore plic ploc."),
            ("narrateur", "La pluie vient de s'arrêter."),
            ("narrateur", "Le volet jaune claque tout doux."),
            ("narrateur", "Dans la rue, les pavés brillent."),
            ("narrateur", "En ce moment, Amir a un bateau en papier."),
            ("narrateur", "Une voile pliée. Un peu froissée."),
            ("enfant-m", "Papa, la flaque est là, dans le jardin."),
            ("papa", "Oui. On y va quand le sac est prêt."),
            ("narrateur", "Le sac attend sur le tapis rayé."),
            ("narrateur", "Amir tire la fermeture. Zzz."),
            ("narrateur", "Le sac est vide."),
            ("narrateur", "Le bateau est sur la commode."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0000",
        [
            ("narrateur", "Pour aller à la flaque, on prend aussi…"),
            ("narrateur", "Le manteau, les bottes, ou un linge."),
        ],
    )
)

# --- manteau : bateau d'abord, puis le manteau chaud --------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0001",
        [
            ("narrateur", "Amir prend le bateau sur la commode."),
            ("maman", "Le bateau, dans le sac d'abord."),
            ("narrateur", "Il le glisse au fond."),
            ("narrateur", "Toc."),
            ("narrateur", "La voile dépasse un tout petit peu."),
            ("narrateur", "Il la rentre avec le doigt."),
            ("narrateur", "Le manteau est sur la chaise."),
            ("narrateur", "Il est encore un peu chaud."),
            ("papa", "Pour la flaque. Il est encore frais dehors."),
            ("narrateur", "Amir le plie."),
            ("narrateur", "Il le met à côté du bateau."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0001_Q0001", [("narrateur", "Où Amir met-il le bateau ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_C0001",
        [
            ("narrateur", "Le bateau est dans le sac."),
            ("narrateur", "La voile est rentrée."),
            ("narrateur", "Le manteau est à côté."),
            ("enfant-m", "C'est bon ?"),
            ("papa", "Presque. On va à la flaque."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0000",
        [
            ("narrateur", "Quelle flaque ?"),
            ("narrateur", "Sous la gouttière, près du potager, ou près du bac."),
        ],
    )
)

# --- bottes : bateau dans le sac, bottes à côté (pas dedans) ------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0002",
        [
            ("narrateur", "Amir glisse le bateau au fond du sac."),
            ("narrateur", "Toc."),
            ("narrateur", "La voile dépasse. Il la rentre."),
            ("narrateur", "Les bottes sont près de la porte."),
            ("narrateur", "Elles sont encore mouillées dehors."),
            ("maman", "Attends. Je les essuie."),
            ("narrateur", "Maman frotte le bout, tout doux."),
            ("enfant-m", "Merci, maman."),
            ("narrateur", "Amir les pose à côté du sac."),
            ("maman", "Au pied, juste avant de sortir."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0002_Q0001", [("narrateur", "Qui essuie les bottes ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_C0001",
        [
            ("narrateur", "Maman a essuyé les bottes."),
            ("narrateur", "Le bateau est dans le sac."),
            ("narrateur", "Les bottes attendent près de la porte."),
            ("papa", "On va à la flaque."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0000",
        [
            ("narrateur", "Quelle flaque ?"),
            ("narrateur", "Sous la gouttière, près du potager, ou près du bac."),
        ],
    )
)

# --- linge -------------------------------------------------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0003",
        [
            ("narrateur", "Amir met le bateau dans le sac."),
            ("narrateur", "Toc. La voile rentre sous son doigt."),
            ("narrateur", "Le linge est sur le radiateur."),
            ("narrateur", "Il sent le propre."),
            ("maman", "Pour tes mains, après la flaque."),
            ("narrateur", "Amir le roule."),
            ("narrateur", "Il le glisse près du bateau."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0003_Q0001", [("narrateur", "On met le linge où ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_C0001",
        [
            ("narrateur", "Le linge est dans le sac."),
            ("narrateur", "Le bateau aussi."),
            ("enfant-m", "On y va ?"),
            ("papa", "Oui. Vers la flaque."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0000",
        [
            ("narrateur", "Quelle flaque ?"),
            ("narrateur", "Sous la gouttière, près du potager, ou près du bac."),
        ],
    )
)


def t1_prefix(t1: int) -> str:
    return {1: "CHK_T0001_P0001", 2: "CHK_T0001_P0002", 3: "CHK_T0001_P0003"}[t1]


# T2 : trois flaques. L'objet T1 sert vraiment.
T2 = {
    1: {
        "ou": "sous la gouttière",
        "go": {
            1: [
                ("narrateur", "Amir met le manteau. Il est tiède."),
                ("narrateur", "Ils sortent. Le sac tape contre sa hanche."),
                ("narrateur", "Sous la gouttière, une flaque ronde."),
                ("narrateur", "Une goutte tombe. Plic."),
                ("narrateur", "L'eau tremble."),
                ("papa", "Le bateau, maintenant."),
            ],
            2: [
                ("narrateur", "Amir enfile les bottes près de la porte."),
                ("narrateur", "Elles sont un peu froides, plus mouillées."),
                ("narrateur", "Sous la gouttière, une flaque ronde."),
                ("narrateur", "Ses bottes font un petit clap dans l'herbe."),
                ("narrateur", "Une goutte tombe. Plic."),
                ("papa", "Le bateau, maintenant."),
            ],
            3: [
                ("narrateur", "Amir porte le sac. Le linge est dedans."),
                ("narrateur", "Sous la gouttière, une flaque ronde."),
                ("narrateur", "Une goutte tombe. Plic."),
                ("narrateur", "L'eau tremble."),
                ("papa", "Le bateau, maintenant."),
            ],
        },
    },
    2: {
        "ou": "près du potager",
        "go": {
            1: [
                ("narrateur", "Amir met le manteau."),
                ("narrateur", "Ils vont près du potager."),
                ("narrateur", "La flaque est ronde, entre deux choux."),
                ("narrateur", "Une feuille y trempe le bout."),
                ("narrateur", "L'eau tremble un peu."),
                ("maman", "Le bateau, Amir."),
            ],
            2: [
                ("narrateur", "Amir enfile les bottes."),
                ("narrateur", "Ils vont près du potager."),
                ("narrateur", "La terre est molle. Les bottes tiennent."),
                ("narrateur", "La flaque est ronde, entre deux choux."),
                ("maman", "Le bateau, Amir."),
            ],
            3: [
                ("narrateur", "Amir porte le sac avec le linge."),
                ("narrateur", "Ils vont près du potager."),
                ("narrateur", "La flaque est ronde, entre deux choux."),
                ("narrateur", "L'eau tremble un peu."),
                ("maman", "Le bateau, Amir."),
            ],
        },
    },
    3: {
        "ou": "près du bac",
        "go": {
            1: [
                ("narrateur", "Amir met le manteau."),
                ("narrateur", "Ils vont près du bac à sable."),
                ("narrateur", "Une flaque borde le bois du bac."),
                ("narrateur", "Un peu de sable brille au fond."),
                ("papa", "Le bateau, Amir."),
            ],
            2: [
                ("narrateur", "Amir enfile les bottes."),
                ("narrateur", "Ils vont près du bac à sable."),
                ("narrateur", "Une flaque borde le bois du bac."),
                ("narrateur", "Les bottes s'arrêtent au bord, pile."),
                ("papa", "Le bateau, Amir."),
            ],
            3: [
                ("narrateur", "Amir porte le sac avec le linge."),
                ("narrateur", "Ils vont près du bac à sable."),
                ("narrateur", "Une flaque borde le bois du bac."),
                ("narrateur", "Un peu de sable brille au fond."),
                ("papa", "Le bateau, Amir."),
            ],
        },
    },
}

T3_Q = [
    ("narrateur", "On pose le bateau…"),
    ("narrateur", "Au milieu de l'eau, près du bord, ou d'abord sur le sac."),
]


def launch(t1: int, t2: int, t3: int) -> list[tuple[str, str]]:
    """T3 : milieu / bord / sur le sac — le bateau flotte vraiment."""
    if t3 == 1:
        lines = [
            ("narrateur", "Amir sort le bateau du sac."),
            ("narrateur", "Il le pose au milieu de l'eau."),
            ("narrateur", "La voile se tient."),
            ("narrateur", "Un peu d'eau touche le papier."),
            ("papa", "Il avance."),
            ("narrateur", "Amir souffle. Ffff."),
            ("narrateur", "Le bateau part tout doux."),
        ]
    elif t3 == 2:
        lines = [
            ("narrateur", "Amir sort le bateau."),
            ("narrateur", "Il le donne à papa."),
            ("papa", "Près du bord, ensemble."),
            ("narrateur", "Papa le pose. Amir tient le sac."),
            ("narrateur", "Le bateau part."),
            ("narrateur", "Amir marche le long de l'eau."),
            ("narrateur", "Le sac est à l'épaule."),
        ]
    else:
        lines = [
            ("narrateur", "Amir pose d'abord le sac."),
            ("narrateur", "Il pose le bateau sur le sac."),
            ("narrateur", "Il regarde la flaque."),
            ("narrateur", "Puis il met le bateau dans l'eau."),
            ("papa", "Tu as préparé. Maintenant il flotte."),
        ]
    return lines


def extra_back(t1: int) -> list[tuple[str, str]]:
    if t1 == 1:
        return [
            ("narrateur", "Le papier est un peu mouillé."),
            ("narrateur", "Amir reprend le bateau."),
            ("narrateur", "Il le remet dans le sac."),
            ("narrateur", "Le manteau rentre aussi."),
            ("narrateur", "On referme. Zzz."),
        ]
    if t1 == 2:
        return [
            ("narrateur", "Le papier est un peu mouillé."),
            ("narrateur", "Amir reprend le bateau."),
            ("narrateur", "Il le remet dans le sac."),
            ("narrateur", "Les bottes restent aux pieds, jusqu'à la porte."),
            ("narrateur", "On referme. Zzz."),
        ]
    return [
        ("narrateur", "Le papier est un peu mouillé."),
        ("narrateur", "Amir sèche ses doigts avec le linge."),
        ("narrateur", "Il remet le bateau dans le sac."),
        ("narrateur", "Le linge rentre aussi."),
        ("narrateur", "On referme. Zzz."),
    ]


def last_image(t2: int) -> tuple[str, str]:
    if t2 == 1:
        return ("narrateur", "La gouttière fait un dernier plic.")
    if t2 == 2:
        return ("narrateur", "Une feuille lâche la flaque.")
    return ("narrateur", "Un grain de sable reste sur le bois.")


for t1 in (1, 2, 3):
    pre = t1_prefix(t1)
    for t2 in (1, 2, 3):
        CHUNKS.append(pack(f"{pre}_T0002_P000{t2}", T2[t2]["go"][t1]))
        CHUNKS.append(pack(f"{pre}_T0002_P000{t2}_T0003_P0000", T3_Q))
        for t3 in (1, 2, 3):
            body = launch(t1, t2, t3)
            CHUNKS.append(pack(f"{pre}_T0002_P000{t2}_T0003_P000{t3}", body))
            fin = extra_back(t1) + [last_image(t2), ("narrateur", "L'histoire est finie.")]
            CHUNKS.append(pack(f"{pre}_T0002_P000{t2}_T0003_P000{t3}_F0001", fin))


def word_count(s: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9']+", s))


def main() -> None:
    ids_src = [c["chunk_id"] for c in SRC["chunks"]]
    ids_new = [c["chunk_id"] for c in CHUNKS]
    missing = [i for i in ids_src if i not in ids_new]
    extra = [i for i in ids_new if i not in ids_src]
    if missing or extra or len(ids_new) != len(set(ids_new)):
        raise SystemExit(f"ids mismatch missing={missing[:8]} extra={extra[:8]} n={len(ids_new)}")
    long_lines = []
    bravo = 0
    for c in CHUNKS:
        if "bravo" in (c["text"] or "").lower():
            bravo += 1
        for line in c["script"].splitlines():
            phrase = line.split("|", 1)[1] if "|" in line else line
            n = word_count(phrase)
            if n > 12:
                long_lines.append((c["chunk_id"], n, phrase))
    by_new = {c["chunk_id"]: c for c in CHUNKS}
    payload = {
        "story_id": "TREE-AUT-001",
        "fil_rouge": (
            "Amir veut faire flotter son bateau en papier dans la flaque. "
            "Le sac doit être prêt. Il y met le bateau, puis le manteau, les bottes ou le linge. "
            "À la flaque, le bateau part. Il le remet dans le sac."
        ),
        "title": "Le bateau d'Amir et la flaque",
        "lesson_id": "AUT.AFF.001",
        "age_band": "N1",
        "kind": "ramifiee",
        "characters": "Amir, maman, papa",
        "setting": "dans la chambre, puis le jardin",
        "chunks": [by_new[i] for i in ids_src],
    }
    out = HERE / "merged.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} n={len(ids_src)} bravo={bravo} long>12={len(long_lines)}")
    for cid, n, p in long_lines[:12]:
        print(f"  {n:2} {cid} {p}")


if __name__ == "__main__":
    main()
