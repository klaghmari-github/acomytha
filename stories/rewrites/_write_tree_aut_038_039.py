#!/usr/bin/env python3
"""TREE-AUT-038 (N1 AFF.003, Mila, seau sous la table) et TREE-AUT-039 (N3 RAN.001, Nino, osier)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402


def vet(lim: int, lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > lim:
            raise SystemExit(f"{n}>{lim}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def write_tree(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict[str, list[str]],
    sons: dict[str, str],
    extras: dict[str, dict],
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind in {"passage_question", "transition_question"}:
            scale, rate = 1.28, "slow"
        elif kind == "passage_fin":
            scale, rate = 1.26, "slow"
        elif src.get("age_band") == "N1":
            scale, rate = 1.22, "slow"
        else:
            scale, rate = 1.22, "medium"
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


N1 = LIMITS["N1"]
N3 = LIMITS["N3"]


# ---------------------------------------------------------------------------
# TREE-AUT-038  N1  Mila  AUT.AFF.003  table du square, pain, mouche
# ≠ 033 kiosque/zinc  ≠ 014 palier  ≠ 020 chat  ≠ 023 rampe  ≠ 048 flaque
# T3 Tom/Léa/Sami → manteau / seau / doudou
# ---------------------------------------------------------------------------

L1_038 = {
    1: {"lab": "le bac à sable", "ou": "près du bac", "son": "enfants_parc"},
    2: {"lab": "le toboggan", "ou": "près du toboggan", "son": "enfants_parc"},
    3: {"lab": "les balançoires", "ou": "près des balançoires", "son": "enfants_parc"},
}
L2_038 = {
    1: {"lab": "le ballon", "obj": "le ballon rouge"},
    2: {"lab": "le seau", "obj": "le seau jaune"},
    3: {"lab": "le doudou", "obj": "le doudou gris"},
}
L3_038 = {
    1: {"lab": "le manteau", "ou": "le manteau rouge", "lieu": "sur le dossier"},
    2: {"lab": "le seau", "ou": "le seau jaune", "lieu": "sous la table"},
    3: {"lab": "le doudou", "ou": "le doudou gris", "lieu": "sur le banc"},
}

ARRIVE_038 = {
    1: vet(
        N1,
        [
            "narrateur|Mila s'agenouille près du bac.",
            "narrateur|Le sable est frais, un peu fin.",
            "narrateur|Il coule entre ses doigts.",
            "narrateur|Chh.",
            "enfant-f|Un château, maman.",
            "maman|D'accord.",
            "maman|Le sable est doux.",
            "papa|Ton seau est où, Mila ?",
            "enfant-f|Pas dans mes mains.",
            "narrateur|Elle creuse avec la paume.",
            "narrateur|Un grain reste sous l'ongle.",
            "maman|Le manteau reste au dossier ?",
            "enfant-f|Oui, je le vois.",
            "narrateur|Le pain tiède sent encore, loin.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Mila va vers le toboggan.",
            "narrateur|Une marche est lisse, un peu froide.",
            "narrateur|Une miette de pain y colle.",
            "enfant-f|Il brille, papa.",
            "papa|Oui.",
            "papa|Le soleil le touche.",
            "maman|J'attends en bas.",
            "narrateur|Mila glisse.",
            "narrateur|Le plastique fait un petit frou.",
            "enfant-f|Encore !",
            "papa|Le seau n'est pas là.",
            "enfant-f|Il est sous la table.",
            "narrateur|Une miette reste sur la marche.",
            "maman|Le manteau reste au dossier.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Mila va vers les balançoires.",
            "narrateur|Une chaîne fait tic, tout doux.",
            "narrateur|Le siège rouge est encore tiède.",
            "enfant-f|Ça bouge, maman.",
            "maman|C'est le vent.",
            "maman|Je pousse tout doux.",
            "papa|Le seau est resté où ?",
            "enfant-f|Sous la table, je crois.",
            "narrateur|Mila avance, puis pose les pieds.",
            "narrateur|Le vent lui touche le nez.",
            "maman|Le manteau est au dossier.",
            "enfant-f|Je le vois.",
            "papa|Tu t'es arrêtée toute seule.",
            "narrateur|La chaîne ne fait plus tic.",
        ],
    ),
}

Q_038 = {
    1: vet(
        N1,
        [
            "narrateur|Mila a du sable aux doigts.",
            "papa|Le seau jaune est où ?",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Mila a une miette au genou.",
            "maman|Le seau jaune est où ?",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Mila a le vent dans les cheveux.",
            "papa|Le seau jaune est où ?",
        ],
    ),
}

C_038 = {
    1: vet(
        N1,
        [
            "narrateur|Mila regarde vers la table.",
            "enfant-f|Dessous.",
            "papa|Oui.",
            "papa|Sous la table.",
            "maman|Il ne roule plus, là.",
            "narrateur|Un grain brille sur son genou.",
            "papa|Merci, Mila.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Mila montre la table du doigt.",
            "enfant-f|Dessous.",
            "maman|Oui.",
            "maman|Sous la table.",
            "papa|On y retourne tout à l'heure.",
            "narrateur|La miette reste sur la marche.",
            "maman|Merci, Mila.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Mila se tourne vers la table.",
            "enfant-f|Dessous.",
            "papa|Oui.",
            "papa|Sous la table.",
            "maman|Le manteau est encore au dossier.",
            "narrateur|La chaîne reste calme, tout bas.",
            "papa|Merci, Mila.",
        ],
    ),
}

PLAY_038 = {
    (1, 1): vet(
        N1,
        [
            "narrateur|Près du bac, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, papa.",
            "papa|D'accord.",
            "narrateur|Mila pose les deux mains dessus.",
            "narrateur|Un peu de sable y colle.",
            "maman|Le seau reste sous la table.",
            "enfant-f|Je le prendrai.",
            "papa|Le manteau reste au dossier.",
            "narrateur|Le ballon prend un grain, tout fin.",
        ],
    ),
    (1, 2): vet(
        N1,
        [
            "narrateur|Mila revient vers la table.",
            "narrateur|Elle se penche, tout doux.",
            "enfant-f|Le seau, maman.",
            "maman|Il est dessous ?",
            "narrateur|L'anse est un peu rêche.",
            "narrateur|Mila tire le seau jaune.",
            "narrateur|Du sable reste au fond.",
            "papa|Tu l'as.",
            "enfant-f|Pour le château.",
            "narrateur|Un grain tombe sur le bois.",
        ],
    ),
    (1, 3): vet(
        N1,
        [
            "narrateur|Près du bac, le doudou gris attend.",
            "narrateur|Le tissu est doux, un peu chaud.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Mila le serre contre elle.",
            "narrateur|Le doudou sent encore le pain.",
            "maman|Le seau reste sous la table.",
            "enfant-f|Je le prendrai.",
            "papa|Le manteau aussi.",
            "narrateur|Un grain colle à l'oreille grise.",
        ],
    ),
    (2, 1): vet(
        N1,
        [
            "narrateur|Près du toboggan, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, papa.",
            "papa|D'accord.",
            "narrateur|Mila pose les deux mains dessus.",
            "narrateur|Le ballon s'appuie contre une marche.",
            "maman|Le seau reste sous la table.",
            "enfant-f|Je le vois, des yeux.",
            "papa|Le manteau reste au dossier.",
            "narrateur|Une miette colle au cuir rouge.",
        ],
    ),
    (2, 2): vet(
        N1,
        [
            "narrateur|Mila revient vers la table.",
            "narrateur|Elle se penche, tout doux.",
            "enfant-f|Le seau, papa.",
            "papa|Il est dessous ?",
            "narrateur|L'anse est un peu rêche.",
            "narrateur|Mila tire le seau jaune.",
            "narrateur|Le seau sonne, toc.",
            "maman|Tu l'as.",
            "enfant-f|Il vient glisser.",
            "narrateur|Du sable reste au fond, tout fin.",
        ],
    ),
    (2, 3): vet(
        N1,
        [
            "narrateur|Près du toboggan, le doudou gris attend.",
            "narrateur|Le tissu est doux, un peu chaud.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Mila le serre contre elle.",
            "narrateur|Le doudou regarde la marche lisse.",
            "maman|Le seau reste sous la table.",
            "enfant-f|Je le prendrai.",
            "papa|Le manteau aussi.",
            "narrateur|Une miette colle au ventre gris.",
        ],
    ),
    (3, 1): vet(
        N1,
        [
            "narrateur|Près des balançoires, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, papa.",
            "papa|D'accord.",
            "narrateur|Mila pose les deux mains dessus.",
            "narrateur|Le ballon rebondit une fois, tout mou.",
            "maman|Le seau reste sous la table.",
            "enfant-f|Je le vois.",
            "papa|Le manteau reste au dossier.",
            "narrateur|Un brin d'herbe colle au cuir.",
        ],
    ),
    (3, 2): vet(
        N1,
        [
            "narrateur|Mila revient vers la table.",
            "narrateur|Elle se penche, tout doux.",
            "enfant-f|Le seau, maman.",
            "maman|Il est dessous ?",
            "narrateur|L'anse est un peu rêche.",
            "narrateur|Mila tire le seau jaune.",
            "narrateur|Le seau tapote l'herbe, toc.",
            "papa|Tu l'as.",
            "enfant-f|Il a vu la chaîne.",
            "narrateur|Du sable reste au fond, tout fin.",
        ],
    ),
    (3, 3): vet(
        N1,
        [
            "narrateur|Près des balançoires, le doudou gris attend.",
            "narrateur|Le tissu est doux, un peu chaud.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Mila le serre contre elle.",
            "narrateur|Le doudou a senti le vent.",
            "maman|Le seau reste sous la table.",
            "enfant-f|Je le prendrai.",
            "papa|Le manteau aussi.",
            "narrateur|L'oreille du doudou est un peu froide.",
        ],
    ),
}

FIRST_038 = {
    1: vet(
        N1,
        [
            "narrateur|Mila va vers le dossier.",
            "narrateur|Le manteau rouge est encore là.",
            "narrateur|Elle le prend.",
            "enfant-f|Il est tiède.",
            "maman|Oui.",
            "maman|Il a pris le soleil.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Mila se penche sous la table.",
            "narrateur|L'ombre est un peu fraîche.",
            "narrateur|L'anse jaune attend, tout près.",
            "enfant-f|Le seau !",
            "papa|Oui.",
            "papa|Il ne roulait plus.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Mila va vers le banc de pierre.",
            "narrateur|Le doudou gris est encore là.",
            "narrateur|Elle le serre.",
            "enfant-f|Il sent le pain.",
            "maman|Oui.",
            "maman|Une miette est sur l'oreille.",
        ],
    ),
}

SEAU_038 = {
    True: vet(
        N1,
        [
            "narrateur|Le seau jaune est déjà dans sa main.",
            "papa|Tu l'as pris tout à l'heure.",
            "enfant-f|Il était sous la table.",
            "maman|Il est avec toi, maintenant.",
        ],
    ),
    False: vet(
        N1,
        [
            "narrateur|Mila se penche sous la table.",
            "narrateur|L'anse jaune brille, tout bas.",
            "narrateur|Elle tire le seau.",
            "enfant-f|Il était dessous.",
            "papa|Oui.",
            "papa|Il t'attendait.",
        ],
    ),
}

MANTEAU_038 = vet(
    N1,
    [
        "narrateur|Le manteau rouge est au dossier.",
        "narrateur|Mila le prend aussi.",
        "maman|Il est avec nous.",
    ],
)

DOUDOU_038 = vet(
    N1,
    [
        "narrateur|Le doudou gris est sur le banc.",
        "narrateur|Mila le prend aussi.",
        "papa|Il est avec nous.",
    ],
)

IMG_038 = {
    (1, 1, 1): "Un grain de sable reste sur le manteau.",
    (1, 1, 2): "Le ballon a un peu de sable au fond.",
    (1, 1, 3): "Le ballon frotte l'oreille du doudou.",
    (1, 2, 1): "Du sable du seau colle au manteau.",
    (1, 2, 2): "Un grain brille encore au fond du seau.",
    (1, 2, 3): "Le seau tapote le ventre du doudou.",
    (1, 3, 1): "L'oreille grise a un grain, tout fin.",
    (1, 3, 2): "Le doudou a senti le sable du seau.",
    (1, 3, 3): "Une miette de pain colle au doudou.",
    (2, 1, 1): "Une miette de marche colle au manteau.",
    (2, 1, 2): "Le ballon a touché l'anse du seau.",
    (2, 1, 3): "Le ballon s'appuie contre le doudou.",
    (2, 2, 1): "L'anse du seau frotte le manteau rouge.",
    (2, 2, 2): "Le seau sonne encore, tout bas.",
    (2, 2, 3): "Le seau a une miette sur le bord.",
    (2, 3, 1): "Le doudou a touché la marche lisse.",
    (2, 3, 2): "Une miette sèche sur le seau jaune.",
    (2, 3, 3): "Le doudou garde une miette au ventre.",
    (3, 1, 1): "Un brin d'herbe colle au manteau.",
    (3, 1, 2): "Le ballon a senti le vent de la chaîne.",
    (3, 1, 3): "Le ballon frotte la feuille du banc.",
    (3, 2, 1): "Du sable du seau reste dans l'herbe.",
    (3, 2, 2): "L'anse du seau est encore un peu froide.",
    (3, 2, 3): "Le seau tapote le banc de pierre.",
    (3, 3, 1): "L'oreille du doudou a pris le vent.",
    (3, 3, 2): "Le doudou sent un peu le sable.",
    (3, 3, 3): "Le doudou passe près de la chaîne calme.",
}

FIN_START_038 = {
    (1, 1, 1): "Mila a le manteau sur le bras.",
    (1, 1, 2): "Mila tient le seau par l'anse.",
    (1, 1, 3): "Mila serre le doudou contre elle.",
    (1, 2, 1): "Le seau tape doucement le manteau.",
    (1, 2, 2): "Le seau jaune est plein de sable.",
    (1, 2, 3): "Le seau et le doudou se touchent.",
    (1, 3, 1): "Le doudou frotte le manteau rouge.",
    (1, 3, 2): "Le doudou regarde au fond du seau.",
    (1, 3, 3): "Le doudou a une miette sur l'oreille.",
    (2, 1, 1): "Une miette reste collée au manteau.",
    (2, 1, 2): "Le ballon s'appuie contre le seau.",
    (2, 1, 3): "Le ballon et le doudou rentrent.",
    (2, 2, 1): "L'anse du seau tient le manteau.",
    (2, 2, 2): "Le seau sonne encore, tout près.",
    (2, 2, 3): "Une miette brille au bord du seau.",
    (2, 3, 1): "Le doudou a senti la marche froide.",
    (2, 3, 2): "Le doudou touche l'anse du seau.",
    (2, 3, 3): "Le doudou rentre, tout calme.",
    (3, 1, 1): "Un brin d'herbe reste au manteau.",
    (3, 1, 2): "Le ballon a gardé le vent.",
    (3, 1, 3): "Le ballon frotte le doudou, tout doux.",
    (3, 2, 1): "Le seau a un peu d'herbe au fond.",
    (3, 2, 2): "L'anse du seau reste froide, encore.",
    (3, 2, 3): "Le seau tapote le doudou, toc.",
    (3, 3, 1): "L'oreille du doudou a pris l'herbe.",
    (3, 3, 2): "Le doudou sent le sable du seau.",
    (3, 3, 3): "Le doudou a quitté la chaîne.",
}

FIN_LAST_038 = {
    (1, 1, 1): "Le carré de soleil a glissé.",
    (1, 1, 2): "La mouche a quitté le pain.",
    (1, 1, 3): "Une miette reste sur le bois.",
    (1, 2, 1): "Le dossier est vide, maintenant.",
    (1, 2, 2): "Sous la table, il n'y a plus rien.",
    (1, 2, 3): "Le banc de pierre est vide.",
    (1, 3, 1): "Le pain est froid, tout calme.",
    (1, 3, 2): "Un grain brille encore sur le bois.",
    (1, 3, 3): "L'ombre de la table est fraîche.",
    (2, 1, 1): "La marche du toboggan sèche.",
    (2, 1, 2): "Le pain n'a plus de mouche.",
    (2, 1, 3): "Le soleil a quitté la table.",
    (2, 2, 1): "Le manteau n'est plus au dossier.",
    (2, 2, 2): "L'anse jaune ne traîne plus.",
    (2, 2, 3): "Une miette sèche sur la pierre.",
    (2, 3, 1): "Le dossier reste vide, tout calme.",
    (2, 3, 2): "Sous la table, l'ombre est vide.",
    (2, 3, 3): "Le doudou n'est plus au banc.",
    (3, 1, 1): "La chaîne ne fait plus tic.",
    (3, 1, 2): "Le vent a quitté le pain.",
    (3, 1, 3): "Le siège rouge est vide.",
    (3, 2, 1): "L'herbe a un peu de sable.",
    (3, 2, 2): "La table n'a plus de seau.",
    (3, 2, 3): "Le banc de pierre est calme.",
    (3, 3, 1): "Le manteau a quitté le dossier.",
    (3, 3, 2): "Le seau a quitté l'ombre.",
    (3, 3, 3): "Plus rien n'attend sur le banc.",
}


def body_038(i: int, j: int, k: int) -> list[str]:
    loc = L1_038[i]
    has_seau = j == 2
    lines = [
        f"narrateur|Mila est encore {loc['ou']}.",
        "papa|C'est l'heure de rentrer.",
        "enfant-f|J'arrive.",
    ]
    if k == 2 and has_seau:
        lines.extend(
            [
                "narrateur|Mila se penche sous la table.",
                "narrateur|L'ombre est un peu fraîche.",
                "narrateur|Plus de seau, dessous.",
                "enfant-f|Il est dans ma main.",
                "papa|Oui.",
                "papa|Tu l'as pris tout à l'heure.",
            ]
        )
    else:
        lines.extend(FIRST_038[k])
        if k != 2:
            lines.extend(SEAU_038[has_seau])
    if k != 1:
        lines.extend(MANTEAU_038)
    if k != 3:
        lines.extend(DOUDOU_038)
    lines.append("enfant-f|J'ai le seau.")
    lines.append("enfant-f|J'ai le manteau.")
    lines.append("maman|Bravo, Mila.")
    lines.append(f"narrateur|{IMG_038[(i, j, k)]}")
    return vet(N1, lines)


def fin_038(i: int, j: int, k: int) -> list[str]:
    loc = L1_038[i]
    obj = L2_038[j]
    picked = L3_038[k]
    return vet(
        N1,
        [
            f"narrateur|{FIN_START_038[(i, j, k)]}",
            f"narrateur|Mila a joué {loc['ou']}.",
            f"narrateur|Elle avait {obj['lab']}.",
            f"narrateur|Puis {picked['lab']}.",
            "enfant-f|Le seau était dessous.",
            "papa|Oui.",
            "papa|Sous la table.",
            "maman|On rentre.",
            f"narrateur|{IMG_038[(i, j, k)]}",
            f"narrateur|{FIN_LAST_038[(i, j, k)]}",
        ],
    )


def build_038() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N1,
        [
            "narrateur|Un carré de soleil dort sur le bois.",
            "narrateur|La table du square est un peu rêche.",
            "narrateur|Une mouche marche sur le pain.",
            "narrateur|Le pain est encore tiède.",
            "narrateur|Ça sent bon, tout près.",
            "narrateur|Un manteau rouge est sur le dossier.",
            "narrateur|Le dossier est un peu creux.",
            "narrateur|Un seau jaune est sous la table.",
            "narrateur|Le seau a du sable au fond.",
            "narrateur|Un doudou montre une oreille.",
            "narrateur|Il est sur le banc de pierre.",
            "narrateur|Maman plie la serviette du pain.",
            "narrateur|Des miettes tombent, toutes petites.",
            "narrateur|Papa noue un lacet.",
            "narrateur|Le lacet fait un petit bruit.",
            "maman|Tu as vu le soleil, Mila ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Il est chaud.",
            "narrateur|En ce moment, Mila touche le seau.",
            "narrateur|L'anse est un peu rêche.",
            "enfant-f|Je veux le bac !",
            "papa|On y va.",
            "narrateur|Mila pousse le seau sous la table.",
            "narrateur|Il ne roule plus.",
            "maman|Il reste à l'ombre ?",
            "enfant-f|Oui.",
            "narrateur|Elle court déjà vers le sable.",
            "narrateur|Le seau reste sous la table.",
        ],
    )
    sons["CHK_T0000_P0000"] = "enfants_parc,pain"

    s["CHK_T0001_P0000"] = vet(
        N1,
        [
            "narrateur|Le square a trois coins.",
            "papa|Le bac à sable.",
            "papa|Le toboggan.",
            "maman|Ou les balançoires ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("le bac à sable", "le toboggan", "les balançoires")

    for i, loc in L1_038.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_038[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_038[i]
        extras[f"{p}_Q0001"] = qf(
            "table",
            "table | sous la table | dessous | le seau | seau | sous la table",
            "Le seau jaune. Il est où ?",
        )
        s[f"{p}_C0001"] = C_038[i]
        s[f"{p}_T0002_P0000"] = vet(
            N1,
            [
                f"narrateur|{loc['ou'].capitalize()}, Mila prend un objet.",
                "papa|Le ballon, le seau, ou le doudou ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_038[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N1,
                [
                    "narrateur|Il reste une chose à prendre.",
                    "maman|Le manteau, le seau, ou le doudou ?",
                    "papa|Tu choisis.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le manteau", "le seau", "le doudou")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_038(i, j, k)
                s[f"{p3}_F0001"] = fin_038(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-039  N3  Nino  AUT.RAN.001  caisse d'osier, lièvre de bois
# IMPLICIT: objet aimé perdu dans l'osier, trouvé seulement en remettant.
# NEVER « on va ranger » / « après le jeu ».
# ≠ 012 train/doudou  ≠ 018 étoile/gouttière  ≠ 004 moulin  ≠ 029 oiseau
# ---------------------------------------------------------------------------

L1_039 = {
    1: {"lab": "la cuisine", "ou": "dans la cuisine", "son": "casserole"},
    2: {"lab": "le jardin", "ou": "dans le jardin", "son": "pluie"},
    3: {"lab": "la chambre", "ou": "dans la chambre", "son": "rideau"},
}
L2_039 = {
    1: {"lab": "les cubes", "un": "un cube", "put": "Nino glisse un cube dans l'osier."},
    2: {"lab": "le livre", "un": "le livre", "put": "Nino glisse le livre dans l'osier."},
    3: {"lab": "la dînette", "un": "une tasse", "put": "Nino glisse une tasse dans l'osier."},
}
L3_039 = {
    1: {
        "lab": "le matin",
        "lum": "La lumière est pâle, un peu bleue.",
        "dehors": "Le réverbère s'est tu, enfin.",
        "fin": "La rosée sèche sur le banc de pierre.",
    },
    2: {
        "lab": "après la sieste",
        "lum": "La lumière est ronde, un peu chaude.",
        "dehors": "Le banc de pierre est tiède.",
        "fin": "Les joues de Nino sont encore un peu chaudes.",
    },
    3: {
        "lab": "le soir",
        "lum": "Le réverbère se rallume, tout jaune.",
        "dehors": "La grille de cave est déjà noire.",
        "fin": "Dehors, les lumières des maisons s'allument.",
    },
}

ARRIVE_039 = {
    1: vet(
        N3,
        [
            "narrateur|Nino pousse la porte de la cuisine.",
            "narrateur|Les carreaux sont froids sous les chaussettes.",
            "narrateur|Ça sent l'orange pelée, tout près.",
            "narrateur|Un zeste brille dans l'évier.",
            "narrateur|La casserole fait un tout petit tic.",
            "maman|Tu cherches ici un moment ?",
            "enfant-m|Le lièvre voulait l'orange.",
            "papa|La caisse d'osier est près de la porte.",
            "narrateur|Nino pose un doigt sur le zeste.",
            "narrateur|Il est un peu humide, un peu parfumé.",
            "enfant-m|Il n'est pas sur la table.",
            "maman|Sous les cubes, peut-être.",
            "narrateur|Un cube jaune a roulé près du zeste.",
            "papa|On peut voir dans l'osier, tout doux.",
            "narrateur|Une buée fine reste sur la vitre.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Nino ouvre la porte du jardin.",
            "narrateur|L'herbe est encore mouillée, tout bas.",
            "narrateur|La grille de cave est froide et noire.",
            "narrateur|Ça sent le foin de l'osier, dehors.",
            "enfant-m|Le lièvre voulait l'herbe.",
            "papa|La caisse est posée près du pas.",
            "maman|Une feuille jaune colle encore au bois.",
            "narrateur|Nino pose un doigt sur l'herbe.",
            "narrateur|Une goutte lui touche le poignet.",
            "enfant-m|Il n'est pas dans l'herbe.",
            "papa|Dans l'osier, peut-être.",
            "narrateur|Un cube a glissé près de la grille.",
            "maman|On peut voir dessous, tout doux.",
            "narrateur|Un moineau secoue une aile, sur le toit.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Nino pousse la porte de la chambre.",
            "narrateur|Le rideau jaune bouge, tout lent.",
            "narrateur|Le lit est encore un peu chaud.",
            "narrateur|Le cartable est posé contre la chaise.",
            "narrateur|La fermeture fait un petit zzz.",
            "enfant-m|Le lièvre voulait le lit.",
            "maman|La caisse d'osier est au pied du lit.",
            "papa|Le bonnet de laine est sur l'oreiller.",
            "narrateur|Nino soulève un coin de couverture.",
            "narrateur|Le tissu sent le savon propre.",
            "enfant-m|Il n'est pas dans le nid.",
            "maman|Dans l'osier, peut-être.",
            "narrateur|Une tasse de dînette a roulé sous la chaise.",
            "papa|On peut voir au fond, tout doux.",
            "narrateur|Le rideau se tait, enfin.",
        ],
    ),
}

Q_039 = {
    1: vet(
        N3,
        [
            "narrateur|Le zeste brille encore, près du cube.",
            "maman|Le petit lièvre est où ?",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|L'herbe a gardé une goutte, tout près.",
            "papa|Le petit lièvre est où ?",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Le rideau jaune ne bouge plus.",
            "maman|Le petit lièvre est où ?",
        ],
    ),
}

C_039 = {
    1: vet(
        N3,
        [
            "narrateur|Nino se penche vers l'osier.",
            "enfant-m|Au fond, peut-être.",
            "papa|Oui.",
            "papa|On peut voir dessous.",
            "maman|Un cube, puis un autre.",
            "narrateur|La casserole tic encore, tout petit.",
            "papa|Merci, Nino.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Nino se penche vers l'osier.",
            "enfant-m|Au fond, peut-être.",
            "maman|Oui.",
            "maman|On peut voir dessous.",
            "papa|Une feuille, puis un cube.",
            "narrateur|Le moineau est parti du toit.",
            "maman|Merci, Nino.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Nino se penche vers l'osier.",
            "enfant-m|Au fond, peut-être.",
            "papa|Oui.",
            "papa|On peut voir dessous.",
            "maman|Le bonnet attend encore.",
            "narrateur|La fermeture ne fait plus zzz.",
            "papa|Merci, Nino.",
        ],
    ),
}

PLAY_039 = {
    (1, 1): vet(
        N3,
        [
            "narrateur|Les cubes de bois sont près du zeste.",
            "narrateur|Ils tapent un peu, toc toc.",
            "papa|Les cubes, Nino.",
            "papa|Tu les prends ?",
            "enfant-m|Oui.",
            "enfant-m|Une tour, d'abord.",
            "narrateur|Il pose un cube jaune, puis un bleu.",
            "narrateur|Le jaune a un peu d'orange au coin.",
            "maman|Elle est haute, ta tour.",
            "enfant-m|Le lièvre voulait la voir.",
            "papa|Il est encore dans l'osier, peut-être.",
            "narrateur|Un cube attrape un reflet d'orange.",
        ],
    ),
    (1, 2): vet(
        N3,
        [
            "narrateur|Le livre est sous le torchon de la cuisine.",
            "narrateur|La couverture est lisse, un peu froide.",
            "maman|Le livre, Nino.",
            "maman|Tu le prends ?",
            "enfant-m|Oui.",
            "enfant-m|Le livre.",
            "narrateur|Il ouvre une page, tout doux.",
            "narrateur|Un lièvre dessiné regarde le vrai.",
            "papa|Il lui ressemble, un peu.",
            "enfant-m|Le mien est en bois.",
            "maman|Il est encore dans l'osier, peut-être.",
            "narrateur|Une miette d'orange reste sur la page.",
        ],
    ),
    (1, 3): vet(
        N3,
        [
            "narrateur|La dînette cliquette près de l'évier.",
            "narrateur|Une petite tasse est blanche.",
            "papa|La dînette, Nino.",
            "papa|Tu la prends ?",
            "enfant-m|Oui.",
            "enfant-m|Un thé d'orange.",
            "narrateur|Il pose la tasse près du zeste.",
            "narrateur|Ça fait ting, tout petit.",
            "maman|Le lièvre voulait une gorgée ?",
            "enfant-m|Oui, une toute petite.",
            "papa|Il est encore dans l'osier, peut-être.",
            "narrateur|La casserole tic encore, tout bas.",
        ],
    ),
    (2, 1): vet(
        N3,
        [
            "narrateur|Les cubes attendent près de la grille.",
            "narrateur|Un cube a une goutte d'herbe dessus.",
            "maman|Les cubes, Nino.",
            "maman|Tu les prends ?",
            "enfant-m|Oui.",
            "enfant-m|Un pont, pour le lièvre.",
            "narrateur|Il pose deux cubes sur une pierre.",
            "narrateur|L'osier sent le foin, tout près.",
            "papa|Le pont est petit, et droit.",
            "enfant-m|Il n'est pas encore dessus.",
            "maman|Dans la caisse, peut-être.",
            "narrateur|Une feuille jaune tremble sur le cube.",
        ],
    ),
    (2, 2): vet(
        N3,
        [
            "narrateur|Le livre est sur le pas de la porte.",
            "narrateur|Une page est un peu cornée, par le vent.",
            "papa|Le livre, Nino.",
            "papa|Tu le prends ?",
            "enfant-m|Oui.",
            "enfant-m|Le livre.",
            "narrateur|Il le serre contre le manteau.",
            "narrateur|Une goutte d'herbe y brille, un instant.",
            "maman|Le lièvre de la page regarde le jardin.",
            "enfant-m|Le mien voulait l'herbe.",
            "papa|Il est encore dans l'osier, peut-être.",
            "narrateur|Le moineau est revenu, tout loin.",
        ],
    ),
    (2, 3): vet(
        N3,
        [
            "narrateur|La dînette est dans l'herbe, près de l'osier.",
            "narrateur|L'osier pique un peu les doigts.",
            "maman|La dînette, Nino.",
            "maman|Tu la prends ?",
            "enfant-m|Oui.",
            "enfant-m|Un thé de goutte.",
            "narrateur|Il sert une feuille dans l'assiette.",
            "narrateur|La petite cuillère brille, toute froide.",
            "papa|Le lièvre voulait goûter l'herbe ?",
            "enfant-m|Oui, une toute petite gorgée.",
            "maman|Il est encore dans l'osier, peut-être.",
            "narrateur|La grille de cave reste noire, tout calme.",
        ],
    ),
    (3, 1): vet(
        N3,
        [
            "narrateur|Les cubes sont au pied du lit.",
            "narrateur|Un cube tapote le parquet, tout doux.",
            "papa|Les cubes, Nino.",
            "papa|Tu les prends ?",
            "enfant-m|Oui.",
            "enfant-m|Pour le lièvre.",
            "narrateur|Il les pose dans un petit chemin.",
            "narrateur|Le chemin mène vers l'osier.",
            "maman|Le bonnet de laine a glissé.",
            "enfant-m|Il n'est pas sous le bonnet.",
            "papa|Dans la caisse, peut-être.",
            "narrateur|Le rideau jaune touche son épaule.",
        ],
    ),
    (3, 2): vet(
        N3,
        [
            "narrateur|Sur la couverture, le livre est ouvert.",
            "narrateur|Le rideau jaune colore la page.",
            "maman|Le livre, Nino.",
            "maman|Tu le prends ?",
            "enfant-m|Oui.",
            "enfant-m|Le livre.",
            "narrateur|Il glisse l'ouvrage contre l'osier.",
            "narrateur|Une page se recourbe, tout doux.",
            "papa|Le lièvre de la page est calme.",
            "enfant-m|Le mien est en bois.",
            "maman|Il est encore dans l'osier, peut-être.",
            "narrateur|L'oreiller sent encore le savon.",
        ],
    ),
    (3, 3): vet(
        N3,
        [
            "narrateur|La dînette attend au pied du lit.",
            "narrateur|Une petite tasse est près du cartable.",
            "papa|La dînette, Nino.",
            "papa|Tu la prends ?",
            "enfant-m|Oui.",
            "enfant-m|Un thé de chambre.",
            "narrateur|Il pose la tasse sur l'osier.",
            "narrateur|Ça fait ting, tout bas.",
            "maman|Le lièvre voulait le lit chaud ?",
            "enfant-m|Oui, et la tasse.",
            "papa|Il est encore dans l'osier, peut-être.",
            "narrateur|La fermeture du cartable reste calme.",
        ],
    ),
}

IMG_039 = {
    (1, 1, 1): "Un cube a un peu d'orange au coin.",
    (1, 1, 2): "Le cube jaune est encore tiède, comme les joues.",
    (1, 1, 3): "L'ombre des cubes danse sous la lampe.",
    (1, 2, 1): "Une page du livre sent l'orange.",
    (1, 2, 2): "Une miette reste sous le livre, tout plate.",
    (1, 2, 3): "La page a un rond de lampe, tout jaune.",
    (1, 3, 1): "La petite tasse est encore tiède.",
    (1, 3, 2): "Une cuillère minuscule brille près du zeste.",
    (1, 3, 3): "La tasse a un reflet orange sur le bord.",
    (2, 1, 1): "Une goutte d'herbe sèche sur un cube.",
    (2, 1, 2): "Le cube a gardé la chaleur de la sieste.",
    (2, 1, 3): "Un cube bleu a un grain de nuit.",
    (2, 2, 1): "Le livre a une page un peu fraîche.",
    (2, 2, 2): "Une goutte a séché sur la couverture.",
    (2, 2, 3): "Le livre voit les lumières du village.",
    (2, 3, 1): "Une feuille vraie reste dans l'assiette.",
    (2, 3, 2): "L'osier sent encore le jardin tiède.",
    (2, 3, 3): "La petite assiette reflète le réverbère.",
    (3, 1, 1): "Un cube tapote le parquet, tout doux.",
    (3, 1, 2): "Un cube est contre l'oreiller, tout calme.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Une bande jaune colore encore la page.",
    (3, 2, 2): "Sur la couverture, le livre reste ouvert.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FIN_START_039 = [
    "Le lièvre a le nez contre la poche.",
    "Nino tient le bois lisse, tout chaud.",
    "Contre la joue, le lièvre est calme.",
    "Au chaud, le lièvre écoute les pas.",
    "Près de la caisse, Nino respire.",
    "Sous la lampe, le bois gris brille.",
    "Dans la poche, le lièvre est trouvé.",
    "Enfin le bois est là, tout doux.",
    "Voilà le lièvre, contre le cartable.",
    "Les oreilles de bois sont lisses, encore.",
    "Nino glisse le lièvre dans la poche.",
    "Le petit bois sent encore le foin.",
    "Contre le zeste, le lièvre a voyagé.",
    "Une goutte d'herbe sèche sur l'oreille.",
    "Le bonnet de laine touche le bois.",
    "La corde de l'osier est calme, maintenant.",
    "Nino sent le foin, tout près du bois.",
    "Le lièvre regarde déjà le chemin.",
    "Dans la paume, le bois est un peu frais.",
    "Nino souffle sur l'oreille du lièvre.",
    "Le cartable attend, tout sage, à côté.",
    "La poche est tiède, autour du bois.",
    "Le lièvre a un grain de lumière.",
    "Nino referme la main, tout doux.",
    "L'osier ne cache plus rien, maintenant.",
    "Le petit lièvre est prêt pour le chemin.",
    "Nino a le bois contre le cœur.",
]


def l3_body_039(i: int, j: int, k: int) -> list[str]:
    t = L3_039[k]
    p = L1_039[i]
    y = L2_039[j]
    img = IMG_039[(i, j, k)]
    return vet(
        N3,
        [
            f"narrateur|{t['lum']}",
            f"narrateur|La caisse d'osier est encore {p['ou']}.",
            f"narrateur|{y['put']}",
            "narrateur|Toc.",
            "narrateur|Un coin de bois gris reparaît.",
            "enfant-m|Une oreille !",
            "maman|Encore un, tout doux.",
            f"narrateur|{y['un'].capitalize()} glisse encore.",
            "narrateur|Au fond, le petit lièvre attend.",
            "enfant-m|Mon lièvre !",
            "papa|Te voilà, petit.",
            "papa|Merci, tu l'as trouvé.",
            f"narrateur|{img}",
            "narrateur|Nino le serre contre sa joue.",
            f"narrateur|{t['dehors']}",
        ],
    )


def l3_fin_039(i: int, j: int, k: int) -> list[str]:
    t = L3_039[k]
    p = L1_039[i]
    y = L2_039[j]
    img = IMG_039[(i, j, k)]
    first = FIN_START_039[(i - 1) * 9 + (j - 1) * 3 + (k - 1)]
    return vet(
        N3,
        [
            f"narrateur|{first}",
            f"narrateur|{y['un'].capitalize()} reste dans la caisse.",
            "enfant-m|Il vient dans la poche, papa.",
            "papa|Oui, il est bien là.",
            "maman|L'osier est calme, maintenant.",
            "papa|Bravo, Nino.",
            f"narrateur|Ils ont cherché {p['ou']}.",
            f"narrateur|{img}",
            f"narrateur|{t['fin']}",
            "narrateur|Le chemin reprend, tout bas.",
        ],
    )


def build_039() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N3,
        [
            "narrateur|Le réverbère est encore allumé.",
            "narrateur|Une goutte tombe du toit, toute ronde.",
            "narrateur|Elle éclate sur le banc de pierre.",
            "narrateur|Le banc est froid, un peu vert de mousse.",
            "narrateur|Un bonnet de laine attend sur le banc.",
            "narrateur|Une feuille jaune y colle, toute plate.",
            "narrateur|Le cartable de Nino est posé à côté.",
            "narrateur|La fermeture fait un petit zzz.",
            "narrateur|Papa tient une caisse d'osier par la corde.",
            "narrateur|L'osier sent le foin sec.",
            "narrateur|Maman boutonne son manteau, près de la grille.",
            "narrateur|La grille de cave est froide et noire.",
            "maman|Tu as mis ton bonnet, Nino ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Il y a une feuille dessus.",
            "papa|On la laisse.",
            "papa|Elle est jolie.",
            "narrateur|En ce moment, Nino touche la caisse.",
            "narrateur|Les jouets dorment dedans, tout calmes.",
            "enfant-m|Je veux mon lièvre !",
            "enfant-m|Il vient dans la poche.",
            "papa|D'accord.",
            "narrateur|Nino penche la caisse, tout doux.",
            "narrateur|Des cubes tombent sur la mousse.",
            "narrateur|Le livre glisse sous le bonnet.",
            "narrateur|Une tasse de dînette roule, toc.",
            "enfant-m|Mon lièvre ?",
            "maman|Il était dans l'osier.",
            "narrateur|Nino cherche sous le cartable.",
            "narrateur|Rien.",
            "papa|Tu as regardé au fond ?",
            "enfant-m|Le tas est trop haut.",
            "maman|On peut voir dessous, tout doux.",
            "narrateur|Le réverbère brûle encore, tout jaune.",
        ],
    )
    sons["CHK_T0000_P0000"] = "goutte,osier"

    s["CHK_T0001_P0000"] = vet(
        N3,
        [
            "papa|Nino cherche où, un moment ?",
            "maman|La cuisine, le jardin, ou la chambre ?",
            "narrateur|La cuisine.",
            "narrateur|Le jardin.",
            "narrateur|Ou la chambre.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("la cuisine", "le jardin", "la chambre")

    for i, loc in L1_039.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_039[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_039[i]
        extras[f"{p}_Q0001"] = qf(
            "lièvre",
            "lièvre | le lièvre | dans la caisse | au fond | l'osier | sous les jouets | dessous",
            "Il cherche dans l'osier. Où est le lièvre ?",
        )
        s[f"{p}_C0001"] = C_039[i]
        s[f"{p}_T0002_P0000"] = vet(
            N3,
            [
                "papa|Tu prends quel jeu ?",
                "narrateur|Les cubes.",
                "narrateur|Le livre.",
                "narrateur|Ou la dînette.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("les cubes", "le livre", "la dînette")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_039[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N3,
                [
                    "maman|C'est quel moment, pour le chemin ?",
                    "narrateur|Le matin.",
                    "narrateur|Après la sieste.",
                    "narrateur|Ou le soir.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le matin", "après la sieste", "le soir")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_039(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_039(i, j, k)
    return s, sons, extras


def main() -> None:
    s38, n38, e38 = build_038()
    write_tree(
        "TREE-AUT-038",
        "Mila veut le bac du square. Elle glisse le seau jaune sous la table "
        "pour qu'il ne roule pas, puis elle court. Le manteau reste au dossier. "
        "Quand c'est l'heure, elle se penche : le seau est encore dessous.",
        "Le seau sous la table",
        "Mila, papa, maman",
        "square du village, table de bois, pain tiède, seau sous la table",
        s38,
        n38,
        e38,
    )
    relecture(
        "TREE-AUT-038",
        "Le seau sous la table",
        "Square, table, pain, mouche. Désir: le bac. Imprévu: seau glissé "
        "sous la table, oublié. T1 bac / toboggan / balançoires. T2 ballon / "
        "seau / doudou. T3 manteau / seau / doudou (plus Tom/Léa/Sami). "
        "Elle se penche, l'anse est là. Fin: soleil glissé, pain froid.",
        "Lila→Mila (D16). N1 ≤10. AUT.AFF.003 implicite. "
        "Pas « on va apprendre » / « tes affaires » / « reprendre ». "
        "Q=table/seau. Monde ≠ 033 kiosque, ≠ 014 palier, ≠ 020 chat, "
        "≠ 023 rampe, ≠ 048 flaque. 86 ids. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins.",
    )

    s39, n39, e39 = build_039()
    write_tree(
        "TREE-AUT-039",
        "Nino veut son petit lièvre de bois dans la poche, pour le chemin. "
        "Il penche la caisse d'osier. Cubes, livre et tasse tombent. "
        "Le lièvre n'est plus dessus. Il ne le retrouve qu'en glissant "
        "les jouets dans l'osier, au fond.",
        "La caisse d'osier de Nino",
        "Nino, papa, maman",
        "chemin, réverbère, banc de mousse, caisse d'osier, grille de cave",
        s39,
        n39,
        e39,
    )
    relecture(
        "TREE-AUT-039",
        "La caisse d'osier de Nino",
        "Réverbère, banc de mousse, osier, foin. Désir: lièvre dans la poche. "
        "Imprévu: caisse penchée, tas, lièvre perdu au fond. "
        "T1 cuisine / jardin / chambre. T2 cubes / livre / dînette. "
        "T3 matin / sieste / soir. Résolution: jouet dans l'osier, lièvre au fond. "
        "Fin: lièvre dans la poche, chemin.",
        "Tom→Nino (D16). N3. AUT.RAN.001 implicite. "
        "Pas « on va ranger » / « après le jeu » / « ranger, c'est ». "
        "Q=lièvre. Monde ≠ 012 train, ≠ 018 étoile, ≠ 004 moulin, ≠ 029 oiseau. "
        "86 ids. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins (images uniques).",
    )


if __name__ == "__main__":
    main()
