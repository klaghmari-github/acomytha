#!/usr/bin/env python3
"""TREE-AUT-014 / TREE-AUT-015 — implicit, D16, 86 chunks, 3 branches vécues."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture

L1_014 = {
    1: {"label": "le bac à sable", "ou": "au bac à sable", "ici": "le bac à sable", "quit": "le bac à sable"},
    2: {"label": "le toboggan", "ou": "au toboggan", "ici": "le toboggan", "quit": "le toboggan"},
    3: {"label": "les balançoires", "ou": "aux balançoires", "ici": "les balançoires", "quit": "les balançoires"},
}
L2_014 = {
    1: {"label": "les cubes", "obj": "les cubes"},
    2: {"label": "le livre", "obj": "le livre"},
    3: {"label": "la dînette", "obj": "la dînette"},
}
L3_014 = {
    1: {"label": "le manteau", "obj": "manteau", "det": "le manteau bleu"},
    2: {"label": "le seau", "obj": "seau", "det": "le seau jaune"},
    3: {"label": "le doudou", "obj": "doudou", "det": "le doudou gris"},
}

L1_015 = {
    1: {"label": "le bac à sable", "ou": "au bac à sable", "ici": "le bac à sable"},
    2: {"label": "le toboggan", "ou": "au toboggan", "ici": "le toboggan"},
    3: {"label": "les balançoires", "ou": "aux balançoires", "ici": "les balançoires"},
}
L2_015 = {
    1: {"label": "le ballon", "obj": "ballon", "det": "le ballon rouge"},
    2: {"label": "le seau", "obj": "seau", "det": "le seau jaune"},
    3: {"label": "le doudou", "obj": "doudou", "det": "le doudou"},
}
L3_015 = {
    1: {"label": "la gourde", "obj": "gourde", "det": "la gourde bleue"},
    2: {"label": "le goûter", "obj": "goûter", "det": "le goûter dans le linge"},
    3: {"label": "la casquette", "obj": "casquette", "det": "la casquette à visière"},
}


def write_tree(sid: str, fil: str, title: str, chars: str, setting: str, scripts: dict, sons: dict, extras: dict) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} chunks missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind == "passage_question":
            scale, rate = 1.28, "slow"
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
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# TREE-AUT-014  Nino  palier / cour  N3  AUT.AFF.003
# Monde unique ≠ TREE-AUT-003 (salon, cacao, tapis).
# ---------------------------------------------------------------------------

ARRIVE_014 = {
    1: [
        "narrateur|Nino s'agenouille au bord du bac.",
        "narrateur|Le sable est frais, encore un peu mouillé.",
        "narrateur|Ça fait chh quand la main entre.",
        "narrateur|Le seau jaune sonne contre le bois.",
        "enfant-m|Un château, papa.",
        "papa|D'accord.",
        "papa|Le seau reste près de toi ?",
        "enfant-m|Oui, tout près.",
        "maman|Le manteau est sur le banc.",
        "narrateur|Nino verse le sable.",
        "narrateur|Ça sent la terre propre.",
        "narrateur|Un grain reste sous son ongle.",
        "enfant-m|Il est froid.",
        "papa|Tes joues sont déjà roses.",
        "narrateur|Nino appuie le château avec la paume.",
        "maman|Le doudou regarde depuis la chaise.",
    ],
    2: [
        "narrateur|Le toboggan brille encore de pluie.",
        "narrateur|Les marches sont froides sous la main.",
        "narrateur|Nino pose le pied, tout doux.",
        "enfant-m|Je glisse !",
        "papa|J'attends en bas.",
        "papa|Ton manteau est au crochet ?",
        "enfant-m|Je le vois.",
        "maman|Le seau est près des bottes.",
        "narrateur|Nino glisse.",
        "narrateur|Le plastique fait un petit frou.",
        "narrateur|Ses pieds retrouvent l'herbe mouillée.",
        "enfant-m|Encore une fois.",
        "papa|Une fois, oui.",
        "narrateur|Nino souffle.",
        "narrateur|Il a les joues tièdes.",
        "maman|Tes mains sont mouillées.",
    ],
    3: [
        "narrateur|Les chaînes des balançoires sont froides.",
        "narrateur|Elles font un bruit de goutte, tout léger.",
        "narrateur|Nino s'assoit.",
        "narrateur|Le siège est encore humide.",
        "enfant-m|Un peu, maman.",
        "maman|Je pousse tout doux.",
        "papa|Le manteau reste au poteau ?",
        "enfant-m|Oui, au crochet.",
        "narrateur|Nino avance, puis revient.",
        "narrateur|Le vent lui touche le nez.",
        "maman|Le seau est sous le banc.",
        "narrateur|Nino pose les pieds par terre.",
        "papa|Tu t'es arrêté tout seul.",
        "narrateur|Une flaque reflète le ciel, tout près.",
        "enfant-m|Je vois le ciel.",
        "maman|Le doudou est sous le banc, lui aussi.",
    ],
}

Q_014 = {
    1: [
        "narrateur|Le seau est resté au bac.",
        "papa|Nino, tu fais quoi ?",
    ],
    2: [
        "narrateur|Le manteau est resté au crochet.",
        "maman|Nino, tu fais quoi ?",
    ],
    3: [
        "narrateur|Le doudou est resté sous le banc.",
        "papa|Nino, tu fais quoi ?",
    ],
}

C_014 = {
    1: [
        "narrateur|Nino revient vers le bac.",
        "narrateur|Il prend le seau jaune à deux mains.",
        "enfant-m|Il était là.",
        "papa|Oui.",
        "papa|Il t'attendait.",
        "maman|Le manteau est encore sur le banc.",
        "narrateur|Un grain de sable reste sur sa joue.",
        "papa|Bravo.",
        "papa|Merci, Nino.",
    ],
    2: [
        "narrateur|Nino revient vers le crochet.",
        "narrateur|Il décroche le manteau bleu.",
        "enfant-m|Il fait toc.",
        "maman|Oui.",
        "maman|Il était encore là.",
        "papa|Le seau est près des bottes.",
        "narrateur|Une goutte glisse de la manche.",
        "maman|Merci, Nino.",
    ],
    3: [
        "narrateur|Nino se penche sous le banc.",
        "narrateur|Il sort le doudou gris.",
        "enfant-m|Il sent le vent.",
        "papa|Oui.",
        "papa|Il t'attendait.",
        "maman|Le seau est encore là, juste à côté.",
        "narrateur|L'oreille du doudou est un peu humide.",
        "papa|Merci, Nino.",
    ],
}

PLAY_014 = {
    (1, 1): [
        "narrateur|Près du bac, les cubes sont un peu sableux.",
        "narrateur|Nino en pose un, puis un autre.",
        "enfant-m|Un mur pour le château.",
        "papa|Le seau reste à ta droite.",
        "maman|Le manteau reste sur le banc.",
        "narrateur|Le cube rouge a un grain de sable dessus.",
        "enfant-m|Il gratte un peu.",
        "papa|Tu finis le mur ?",
        "narrateur|Nino finit le mur.",
        "maman|Le doudou a vu le château.",
    ],
    (1, 2): [
        "narrateur|Près du bac, le livre a un coin un peu rêche.",
        "narrateur|Nino l'ouvre sur ses genoux.",
        "enfant-m|Un crabe !",
        "maman|Oui.",
        "maman|Ton seau est juste là, jaune.",
        "papa|Ton manteau est sur le banc, bleu.",
        "narrateur|Nino referme le livre.",
        "enfant-m|On garde le livre.",
        "maman|Oui, dans les mains.",
        "narrateur|Le sable fait un petit tas contre le seau.",
    ],
    (1, 3): [
        "narrateur|Près du bac, la dînette est dans un panier.",
        "narrateur|Nino pose une tasse sur le rebord.",
        "enfant-m|Du sable-thé.",
        "papa|La tasse jouet, oui.",
        "papa|Le seau, c'est autre chose.",
        "maman|Ce n'est pas la même tasse.",
        "narrateur|Nino range la tasse.",
        "enfant-m|Le château reste.",
        "maman|Tout petit, dans le bac.",
        "narrateur|Le panier sent encore le plastique chaud.",
    ],
    (2, 1): [
        "narrateur|Au pied du toboggan, les cubes attendent sur un linge.",
        "narrateur|Le linge est encore humide.",
        "enfant-m|Une tour basse.",
        "maman|D'accord.",
        "maman|Tes affaires restent près de papa.",
        "narrateur|Nino empile deux cubes.",
        "papa|Je vois le seau.",
        "papa|Je vois le manteau.",
        "enfant-m|Moi aussi, des yeux.",
        "narrateur|Nino montre le crochet, sans se lever trop vite.",
    ],
    (2, 2): [
        "narrateur|Au toboggan, le livre reste dans le sac de papa.",
        "narrateur|Nino le sort.",
        "narrateur|Les pages sentent le tissu.",
        "enfant-m|Une page, puis l'autre.",
        "papa|Comme tes affaires, une puis l'autre.",
        "maman|Le seau, le manteau, le doudou.",
        "narrateur|Nino pose le livre sur le sac.",
        "papa|Tu as fini la page ?",
        "enfant-m|Oui.",
        "narrateur|Le toboggan sèche au soleil, tout lentement.",
    ],
    (2, 3): [
        "narrateur|Au toboggan, la dînette cliquette dans le sac.",
        "narrateur|Nino sort une assiette ronde.",
        "enfant-m|Pour le goûter plus tard.",
        "maman|Oui.",
        "maman|D'abord tes affaires de cour.",
        "papa|Le manteau, le seau, le doudou.",
        "narrateur|Nino remet l'assiette dans le sac.",
        "enfant-m|Elle rentre.",
        "maman|L'herbe mouillée brille encore.",
        "narrateur|Une feuille colle à la rampe.",
    ],
    (3, 1): [
        "narrateur|Près des balançoires, les cubes sont dans l'herbe.",
        "narrateur|L'herbe est encore mouillée.",
        "enfant-m|Une tour qui penche.",
        "papa|Elle penche vers le seau.",
        "maman|Le seau est sous le banc.",
        "narrateur|Nino redresse un cube.",
        "enfant-m|Il est froid.",
        "papa|Comme la chaîne.",
        "narrateur|La chaîne fait un petit cling.",
        "maman|Le manteau reste au poteau.",
    ],
    (3, 2): [
        "narrateur|Nino ouvre le livre sur ses genoux.",
        "narrateur|Le siège de la balançoire bouge un peu.",
        "enfant-m|Le crabe encore.",
        "maman|Oui.",
        "maman|Les pages sont un peu froides.",
        "papa|Le doudou est sous le banc.",
        "narrateur|Nino referme le livre.",
        "enfant-m|Il rentre dans le sac.",
        "papa|Oui, avec nous.",
        "narrateur|Une flaque tremble quand il pose le pied.",
    ],
    (3, 3): [
        "narrateur|Près des balançoires, la dînette est dans l'herbe.",
        "narrateur|Nino pose une assiette sur le banc.",
        "enfant-m|Un pique-nique, tout petit.",
        "papa|L'assiette jouet, oui.",
        "maman|Le seau n'est pas une assiette.",
        "narrateur|Nino range l'assiette.",
        "enfant-m|Le doudou a faim ?",
        "maman|Il a surtout envie de rentrer au chaud.",
        "papa|Il est sous le banc.",
        "narrateur|Une chaîne sèche au soleil, tout lentement.",
    ],
}

FIND_014 = {
    (1, 1, 1): [
        "narrateur|Le manteau bleu a un grain de sable à la manche.",
        "narrateur|Nino le prend au banc.",
        "papa|Tu as le manteau.",
        "maman|Le seau est encore à droite.",
        "narrateur|Nino prend le seau, puis le doudou.",
    ],
    (1, 1, 2): [
        "narrateur|Le seau jaune sonne contre le mur de cubes.",
        "narrateur|Nino le soulève à deux mains.",
        "maman|Oui.",
        "maman|Ensuite le manteau.",
        "narrateur|Nino prend le manteau, puis le doudou.",
    ],
    (1, 1, 3): [
        "narrateur|Le doudou gris a une odeur de vent.",
        "narrateur|Nino le serre, puis prend le seau.",
        "maman|Le manteau aussi.",
        "enfant-m|J'ai tout.",
        "narrateur|Un cube rouge reste près du château.",
    ],
    (1, 2, 1): [
        "narrateur|Le manteau est un peu humide, encore.",
        "narrateur|Nino le boutonne, une boutonnière après l'autre.",
        "papa|Tu as le manteau.",
        "papa|Cherche le seau.",
        "maman|Il est près du livre.",
        "narrateur|Nino prend le seau, puis le doudou.",
    ],
    (1, 2, 2): [
        "narrateur|Le seau attend contre le livre fermé.",
        "narrateur|Nino le prend.",
        "narrateur|Le livre rentre dans le sac.",
        "maman|Le manteau, maintenant.",
        "papa|Il est sur le banc.",
        "narrateur|Nino prend le manteau, puis le doudou.",
    ],
    (1, 2, 3): [
        "narrateur|Le doudou était sous le livre.",
        "narrateur|Nino le sort, tout doux.",
        "papa|Puis le seau.",
        "papa|Puis le manteau.",
        "enfant-m|Je les prends.",
        "narrateur|Le crabe du livre reste dans le sac.",
    ],
    (1, 3, 1): [
        "narrateur|Le manteau glisse du banc.",
        "narrateur|Nino le rattrape.",
        "narrateur|La dînette est déjà dans le panier.",
        "maman|Le seau, maintenant.",
        "papa|On les prend tous.",
        "narrateur|Nino prend le seau, puis le doudou.",
    ],
    (1, 3, 2): [
        "narrateur|Le seau a servi de couvercle un moment.",
        "narrateur|Nino le vide.",
        "narrateur|Le sable retombe dans le bac.",
        "papa|Le seau est à toi.",
        "maman|Le manteau t'attend.",
        "narrateur|Nino prend le manteau, puis le doudou.",
    ],
    (1, 3, 3): [
        "narrateur|Le doudou était dans le panier, sous une tasse.",
        "narrateur|Nino le sort.",
        "narrateur|La tasse reste.",
        "maman|Tes affaires, pas la dînette du parc.",
        "papa|Seau, manteau, doudou.",
        "narrateur|Nino les prend, un par un.",
    ],
    (2, 1, 1): [
        "narrateur|Au crochet du toboggan, le manteau fait toc.",
        "narrateur|Nino le décroche.",
        "papa|Bien.",
        "papa|Le seau est près des bottes.",
        "enfant-m|Je le prends aussi.",
        "narrateur|Nino prend le doudou dans le sac.",
    ],
    (2, 1, 2): [
        "narrateur|Le seau a reçu une goutte du toboggan.",
        "narrateur|Nino l'essuie sur l'herbe, tout doux.",
        "maman|On le prend.",
        "maman|Ensuite le manteau.",
        "papa|Au crochet.",
        "narrateur|Nino prend le manteau, puis le doudou.",
    ],
    (2, 1, 3): [
        "narrateur|Le doudou était dans le sac, au pied de la rampe.",
        "narrateur|Nino le retrouve au premier regard.",
        "maman|Tu as cherché.",
        "papa|Le seau et le manteau aussi.",
        "enfant-m|Je les prends.",
        "narrateur|Les cubes restent sur le linge humide.",
    ],
    (2, 2, 1): [
        "narrateur|Le manteau couvre un instant le livre, puis Nino le met.",
        "narrateur|Le tissu est frais sur les bras.",
        "papa|Le seau pend au sac.",
        "maman|Le doudou aussi.",
        "enfant-m|Je les prends.",
        "narrateur|Les pages sentent encore le tissu.",
    ],
    (2, 2, 2): [
        "narrateur|Le seau pend au sac, à côté du livre.",
        "narrateur|Nino le décroche.",
        "maman|Tu as le seau.",
        "maman|Cherche le manteau.",
        "enfant-m|Au crochet.",
        "narrateur|Nino prend le manteau, puis le doudou.",
    ],
    (2, 2, 3): [
        "narrateur|Le doudou sent encore le tissu du sac.",
        "narrateur|Nino le serre.",
        "narrateur|Le livre est déjà rangé.",
        "papa|Manteau, seau, doudou.",
        "maman|Tu les as.",
        "narrateur|La rampe brille encore, derrière eux.",
    ],
    (2, 3, 1): [
        "narrateur|Le manteau était sous le sac de dînette.",
        "narrateur|Nino le tire, tout droit.",
        "papa|Tu as cherché.",
        "maman|Le seau, ensuite.",
        "enfant-m|Près des bottes.",
        "narrateur|Nino prend le seau, puis le doudou.",
    ],
    (2, 3, 2): [
        "narrateur|Le seau a servi de siège un moment.",
        "narrateur|Nino se lève et le prend.",
        "maman|Oui.",
        "maman|C'est le tien.",
        "papa|Le manteau est au crochet.",
        "narrateur|Nino prend le manteau, puis le doudou.",
    ],
    (2, 3, 3): [
        "narrateur|Le doudou était assis dans une assiette jouet.",
        "narrateur|Nino rit un peu, puis le prend.",
        "papa|L'assiette rentre.",
        "papa|Le doudou aussi.",
        "maman|Et le manteau, et le seau.",
        "narrateur|Nino les prend, les uns après les autres.",
    ],
    (3, 1, 1): [
        "narrateur|Au poteau, le manteau fait toc.",
        "narrateur|Nino le décroche.",
        "papa|Le seau est sous le banc.",
        "maman|Le doudou aussi.",
        "enfant-m|Je me penche.",
        "narrateur|Nino les sort, l'un puis l'autre.",
    ],
    (3, 1, 2): [
        "narrateur|Le seau est sous le banc, près des cubes.",
        "narrateur|Nino le tire par l'anse.",
        "maman|Il est froid.",
        "papa|Le manteau est au poteau.",
        "enfant-m|Je le prends.",
        "narrateur|Nino prend le manteau, puis le doudou.",
    ],
    (3, 1, 3): [
        "narrateur|Le doudou est sous le banc, un peu humide.",
        "narrateur|Nino le secoue, tout doux.",
        "papa|Le seau est juste à côté.",
        "maman|Le manteau au poteau.",
        "enfant-m|J'ai tout.",
        "narrateur|Un cube reste dans l'herbe mouillée.",
    ],
    (3, 2, 1): [
        "narrateur|Le manteau au poteau a une goutte à la manche.",
        "narrateur|Nino l'essuie, puis le met.",
        "papa|Le livre est déjà dans le sac.",
        "maman|Le seau est sous le banc.",
        "enfant-m|Je le prends.",
        "narrateur|Nino prend le doudou ensuite.",
    ],
    (3, 2, 2): [
        "narrateur|Le seau a pris un peu d'eau de la flaque.",
        "narrateur|Nino le verse dans l'herbe.",
        "maman|Maintenant le manteau.",
        "papa|Au poteau.",
        "enfant-m|Et le doudou.",
        "narrateur|Le livre reste au chaud, dans le sac.",
    ],
    (3, 2, 3): [
        "narrateur|Le doudou a vu le crabe du livre.",
        "narrateur|Nino le serre contre la page fermée.",
        "papa|Le seau, maintenant.",
        "maman|Le manteau aussi.",
        "enfant-m|Je les prends.",
        "narrateur|La flaque redevient calme.",
    ],
    (3, 3, 1): [
        "narrateur|Le manteau glisse du poteau.",
        "narrateur|Nino le rattrape avant l'herbe.",
        "papa|L'assiette est déjà rangée.",
        "maman|Le seau est sous le banc.",
        "enfant-m|Je le prends.",
        "narrateur|Nino prend le doudou ensuite.",
    ],
    (3, 3, 2): [
        "narrateur|Le seau a servi de table, un moment.",
        "narrateur|Nino le vide, puis le prend.",
        "maman|C'est le tien.",
        "papa|Le manteau est au poteau.",
        "enfant-m|Le doudou aussi.",
        "narrateur|L'assiette rentre dans le panier.",
    ],
    (3, 3, 3): [
        "narrateur|Le doudou était assis à la dînette.",
        "narrateur|Nino le prend, tout doux.",
        "papa|L'assiette rentre.",
        "maman|Le manteau, et le seau.",
        "enfant-m|Je les prends.",
        "narrateur|La chaîne se tait, tout à fait.",
    ],
}

IMG_014 = {
    (1, 1, 1): "Un grain de sable colle à la manche bleue.",
    (1, 1, 2): "Le seau jaune sonne, tout près du château.",
    (1, 1, 3): "L'oreille grise a un grain de sable.",
    (1, 2, 1): "Le manteau couvre encore le livre du crabe.",
    (1, 2, 2): "Le seau attend contre le livre fermé.",
    (1, 2, 3): "Le doudou sent encore la page.",
    (1, 3, 1): "Une tasse de dînette reste dans le bac.",
    (1, 3, 2): "Le sable retombe, tout fin, dans le bac.",
    (1, 3, 3): "Une tasse reste dans le panier.",
    (2, 1, 1): "Le crochet du toboggan fait encore toc.",
    (2, 1, 2): "Une goutte sèche sur l'herbe, près du seau.",
    (2, 1, 3): "Le doudou a vu la rampe, dans les bras.",
    (2, 2, 1): "Le tissu du manteau est frais sur les bras.",
    (2, 2, 2): "Le seau pendait au sac, à côté du livre.",
    (2, 2, 3): "Les pages sentent encore le sac.",
    (2, 3, 1): "L'assiette ronde est déjà rentrée.",
    (2, 3, 2): "Le seau n'est plus un siège.",
    (2, 3, 3): "L'assiette est vide, et le doudou aussi.",
    (3, 1, 1): "La chaîne a fait cling, près du manteau.",
    (3, 1, 2): "L'anse du seau est froide, encore.",
    (3, 1, 3): "Un cube reste dans l'herbe mouillée.",
    (3, 2, 1): "Une goutte sèche sur la manche bleue.",
    (3, 2, 2): "La flaque redevient calme.",
    (3, 2, 3): "Le crabe du livre rentre avec eux.",
    (3, 3, 1): "Le manteau a évité l'herbe mouillée.",
    (3, 3, 2): "L'assiette rentre dans le panier.",
    (3, 3, 3): "La chaîne se tait, tout à fait.",
}


def body_014(i: int, j: int, k: int) -> list[str]:
    loc = L1_014[i]
    first = L3_014[k]
    lines = [
        f"narrateur|Nino quitte {loc['quit']}.",
        f"narrateur|Il cherche d'abord {first['label']}.",
    ]
    lines.extend(FIND_014[(i, j, k)])
    if not any(ln.startswith("enfant-m|") and "tout" in ln for ln in lines):
        lines.append("enfant-m|J'ai tout.")
    lines.append("narrateur|Nino a le seau, le manteau, le doudou.")
    lines.append(f"narrateur|{IMG_014[(i, j, k)]}")
    lines.append("enfant-m|On rentre.")
    lines.append("papa|Oui.")
    return lines


def fin_014(i: int, j: int, k: int) -> list[str]:
    loc = L1_014[i]
    obj = L2_014[j]
    first = L3_014[k]
    return [
        f"narrateur|{IMG_014[(i, j, k)]}",
        f"narrateur|Nino a joué {loc['ou']}.",
        f"narrateur|Il a pris {obj['label']}.",
        f"narrateur|Il a d'abord pris {first['label']}.",
        "enfant-m|J'ai le seau.",
        "enfant-m|J'ai le manteau.",
        "enfant-m|J'ai le doudou.",
        "maman|On remonte le palier.",
        "papa|La goutte n'est plus sur la vitre.",
        "narrateur|La cour brille encore, derrière eux.",
        "narrateur|Le radiateur du palier est tiède.",
    ]


def trans_l2_014(i: int) -> list[str]:
    loc = L1_014[i]
    return [
        f"narrateur|Nino peut encore jouer un peu, {loc['ou']}.",
        "maman|Les cubes, le livre, ou la dînette ?",
        "papa|On joue encore un peu.",
    ]


def trans_l3_014(i: int) -> list[str]:
    loc = L1_014[i]
    return [
        f"narrateur|Il manque encore une affaire, {loc['ou']}.",
        "maman|Le manteau, le seau, ou le doudou ?",
        "papa|On cherche, puis on prend.",
    ]


def extras_t3(label1: str, label2: str, label3: str) -> dict:
    return {
        "option_1_label": label1,
        "option_2_label": label2,
        "option_3_label": label3,
    }


def extras_q(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


def build_014() -> tuple[dict, dict]:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|La pluie vient juste de s'arrêter.",
        "narrateur|Sur la vitre du palier, une goutte glisse.",
        "narrateur|Elle laisse un trait brillant, tout mince.",
        "narrateur|Derrière le verre, la cour est encore mouillée.",
        "narrateur|Les balançoires luisent, comme de l'eau.",
        "narrateur|Le bac à sable est sombre, comme du chocolat.",
        "narrateur|Près du radiateur, l'air est tiède.",
        "narrateur|Un manteau bleu pend au crochet du palier.",
        "narrateur|Le crochet fait un petit toc.",
        "narrateur|Un seau jaune attend près des bottes mouillées.",
        "narrateur|Le seau a encore un peu de sable au fond.",
        "narrateur|Un doudou gris est posé sur la chaise.",
        "maman|Regarde, Nino.",
        "maman|La goutte.",
        "papa|La cour est à nous, tout à l'heure.",
        "narrateur|En ce moment, Nino pose le nez sur le verre.",
        "narrateur|Le verre est froid.",
        "enfant-m|Je veux jouer.",
        "enfant-m|La pluie est partie.",
        "maman|On y va.",
        "papa|Ton seau est encore là ?",
        "narrateur|Nino hoche la tête.",
        "narrateur|Le seau l'attend.",
        "narrateur|Le manteau aussi.",
    ]
    s["CHK_T0001_P0000"] = [
        "narrateur|La cour a trois coins tout proches.",
        "papa|Le bac à sable, le toboggan, ou les balançoires ?",
        "maman|On joue un peu.",
    ]
    extras["CHK_T0001_P0000"] = extras_t3("le bac à sable", "le toboggan", "les balançoires")
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_014[i]
        s[f"{p}_Q0001"] = Q_014[i]
        extras[f"{p}_Q0001"] = extras_q(
            "reprendre",
            "reprendre | le seau | le manteau | le doudou | ses affaires | il le prend",
            "Il reprend le seau. Que fait Nino ?",
        )
        s[f"{p}_C0001"] = C_014[i]
        s[f"{p}_T0002_P0000"] = trans_l2_014(i)
        extras[f"{p}_T0002_P0000"] = extras_t3("les cubes", "le livre", "la dînette")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_014[(i, j)]
            s[f"{p2}_T0003_P0000"] = trans_l3_014(i)
            extras[f"{p2}_T0003_P0000"] = extras_t3("le manteau", "le seau", "le doudou")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_014(i, j, k)
                s[f"{p3}_F0001"] = fin_014(i, j, k)
    return s, extras


# ---------------------------------------------------------------------------
# TREE-AUT-015  Nina  cuisine / parc  N3  AUT.AFF.001
# Pas une liste de sac. Le sac trop léger, le moineau, la buée.
# ---------------------------------------------------------------------------

ARRIVE_015 = {
    1: [
        "narrateur|Nina marche vers le bac à sable.",
        "narrateur|Le sable est un peu froid, tout fin.",
        "narrateur|Il glisse entre les doigts.",
        "narrateur|Le bois du rebord sent le soleil.",
        "narrateur|Le sac bleu est posé contre le rebord.",
        "maman|On pose le sac ici, près de nous.",
        "papa|Il est encore un peu léger, tu sens ?",
        "enfant-f|Oui.",
        "enfant-f|Il y a un creux.",
        "narrateur|Nina ouvre un peu le sac.",
        "narrateur|Le doudou est déjà dedans, un peu humide.",
        "enfant-f|Il a pris la buée.",
        "maman|Il va sécher.",
        "narrateur|Un oiseau chante tout près.",
        "narrateur|Le vent soulève un peu de sable clair.",
    ],
    2: [
        "narrateur|Nina marche vers le toboggan.",
        "narrateur|Le plastique lisse brille au soleil.",
        "narrateur|Les marches métalliques sont tièdes.",
        "narrateur|Nina pose la main dessus, tout doucement.",
        "narrateur|Le sac bleu est au pied du toboggan.",
        "papa|On garde le sac près de nous.",
        "maman|Il est encore léger.",
        "narrateur|Nina ouvre le sac.",
        "narrateur|Elle sent le doudou à travers le tissu.",
        "enfant-f|Il est au chaud.",
        "papa|Il a quitté la vitre.",
        "narrateur|Une feuille sèche tourne sur le sol.",
        "narrateur|Ça sent l'herbe coupée.",
        "enfant-f|Je glisse après.",
        "maman|D'accord.",
    ],
    3: [
        "narrateur|Nina marche vers les balançoires.",
        "narrateur|Les chaînes font un petit clin clin.",
        "narrateur|Le siège en bois est lisse et chaud.",
        "narrateur|Le vent passe dans les cheveux de Nina.",
        "narrateur|Le sac bleu est posé dans l'herbe.",
        "maman|On met le sac ici, à côté.",
        "papa|Il pèse encore trop peu.",
        "narrateur|Nina touche la sangle lisse.",
        "narrateur|Elle sent le doudou à travers le tissu.",
        "enfant-f|Le sac est avec nous.",
        "maman|Oui.",
        "maman|On reste ensemble.",
        "narrateur|Au loin, un vélo passe tout doux.",
        "narrateur|L'air est frais sur les joues.",
        "enfant-f|Je m'assois.",
    ],
}

Q_015 = {
    1: [
        "narrateur|Le sac est trop léger, contre le bac.",
        "maman|Nina met où le doudou ?",
    ],
    2: [
        "narrateur|Le sac est au pied du toboggan.",
        "papa|Nina met où les affaires ?",
    ],
    3: [
        "narrateur|Le sac est dans l'herbe.",
        "maman|Nina met où les affaires ?",
    ],
}

C_015 = {
    1: [
        "narrateur|Nina glisse le doudou au fond.",
        "narrateur|Le sac devient un peu plus lourd.",
        "enfant-f|Il n'est plus vide.",
        "maman|Merci, Nina.",
        "papa|On continue.",
        "papa|Le sac reste avec nous.",
        "narrateur|Nina respire.",
        "narrateur|Le sable est froid sous ses mains.",
    ],
    2: [
        "narrateur|Nina appuie sur la fermeture.",
        "narrateur|Ça fait zzz, tout petit.",
        "enfant-f|Le sac est avec nous.",
        "papa|Merci, Nina.",
        "maman|On peut jouer un peu.",
        "narrateur|Nina pose la main sur la sangle lisse.",
        "narrateur|L'herbe sent encore la pluie.",
    ],
    3: [
        "narrateur|Nina pose le sac dans l'herbe sèche.",
        "narrateur|La sangle reste près de sa main.",
        "enfant-f|Il ne part pas.",
        "maman|Merci, Nina.",
        "papa|On reste ensemble.",
        "narrateur|Une chaîne fait clin, tout doux.",
        "narrateur|Le vent touche encore ses joues.",
    ],
}

PLAY_015 = {
    (1, 1): [
        "narrateur|Nina a choisi le ballon.",
        "narrateur|Il est rouge, un peu poussiéreux.",
        "narrateur|Il sent le caoutchouc chaud.",
        "maman|Il va rester dans le sable ?",
        "enfant-f|Non.",
        "enfant-f|Il rentre.",
        "narrateur|Nina pousse le ballon dans l'ouverture.",
        "narrateur|Le sac devient tout rond.",
        "papa|Il est au chaud, maintenant.",
        "narrateur|Un peu d'eau goutte d'un robinet, tout près.",
    ],
    (1, 2): [
        "narrateur|Nina a choisi le seau.",
        "narrateur|Il est jaune.",
        "narrateur|L'anse est un peu rêche.",
        "narrateur|Il y a du sable au fond, tout fin.",
        "papa|Tu le laisses au bac ?",
        "enfant-f|Non.",
        "enfant-f|Il vient.",
        "narrateur|Nina le glisse à côté du doudou.",
        "maman|L'anse dépasse un tout petit peu.",
        "narrateur|Un vélo passe au loin, tout léger.",
    ],
    (1, 3): [
        "narrateur|Nina a choisi le doudou.",
        "narrateur|Il est déjà un peu dans le sac.",
        "narrateur|Nina le pousse bien au fond, tout doux.",
        "maman|Il a pris la buée, tout à l'heure.",
        "enfant-f|Il sèche dedans.",
        "papa|Le tissu sent la maison.",
        "enfant-f|Mon doudou est prêt.",
        "narrateur|La lumière est claire sur le tissu bleu.",
        "maman|On souffle un peu.",
        "narrateur|Puis le sac attend, contre le bois.",
    ],
    (2, 1): [
        "narrateur|Nina a choisi le ballon, près du toboggan.",
        "narrateur|Il rebondit une fois, tout mou.",
        "maman|Il va rouler sous la rampe ?",
        "enfant-f|Non.",
        "narrateur|Nina le prend à deux mains.",
        "narrateur|Elle le glisse dans le sac bleu.",
        "papa|Il ne part plus.",
        "enfant-f|Le ballon est avec le doudou.",
        "narrateur|Il y a des miettes sur une table basse.",
        "maman|Le sac reste fermé.",
    ],
    (2, 2): [
        "narrateur|Nina a choisi le seau, au pied du toboggan.",
        "narrateur|Un chat miaule une fois, tout près.",
        "papa|Le seau va rester ici ?",
        "enfant-f|Non.",
        "narrateur|Nina le pose sur le doudou.",
        "maman|Tu l'as mis avec nous ?",
        "enfant-f|Oui.",
        "enfant-f|Il est dedans.",
        "papa|L'anse cliquette.",
        "narrateur|Nina rit un peu.",
    ],
    (2, 3): [
        "narrateur|Nina a choisi le doudou, près des marches.",
        "narrateur|Les chaussures font toc toc sur le métal.",
        "maman|Il va rester sur la rampe ?",
        "enfant-f|Non.",
        "narrateur|Nina l'enfonce tout doucement.",
        "papa|Il est au chaud dans le sac.",
        "enfant-f|Oui.",
        "narrateur|Nina souffle.",
        "narrateur|Le toboggan brille encore.",
        "maman|Il reste une chose, plus tard.",
    ],
    (3, 1): [
        "narrateur|Nina a choisi le ballon, près des chaînes.",
        "narrateur|Il fait un petit bond dans l'herbe.",
        "papa|Il va sous la balançoire ?",
        "enfant-f|Non.",
        "narrateur|Nina le rattrape.",
        "narrateur|Elle le glisse dans le sac.",
        "maman|Le sac devient rond.",
        "enfant-f|Il est avec moi.",
        "narrateur|Une chaîne fait clin, tout près.",
        "papa|Le vent ne l'emporte plus.",
    ],
    (3, 2): [
        "narrateur|Nina a choisi le seau, sous le banc.",
        "narrateur|L'anse est froide, encore.",
        "maman|Il reste sous le banc ?",
        "enfant-f|Non.",
        "narrateur|Nina le pose dans le sac, tout droit.",
        "papa|L'anse dépasse un peu.",
        "enfant-f|Je la rentre.",
        "narrateur|Nina rentre l'anse.",
        "maman|Le sac tient mieux.",
        "narrateur|L'herbe est encore un peu mouillée.",
    ],
    (3, 3): [
        "narrateur|Nina a choisi le doudou, sur le siège.",
        "narrateur|Il a pris un peu de vent.",
        "papa|Il reste sur la balançoire ?",
        "enfant-f|Non.",
        "narrateur|Nina le serre, puis le glisse dans le sac.",
        "maman|Il se réchauffe.",
        "enfant-f|Oui, contre moi.",
        "narrateur|Le bois du siège est chaud, vide maintenant.",
        "papa|Le sac est un peu plus lourd.",
        "narrateur|Le vent passe encore dans ses cheveux.",
    ],
}

NEED_015 = {
    1: [
        "narrateur|Nina prend la gourde.",
        "narrateur|Elle est bleue.",
        "narrateur|L'eau chante un peu dedans.",
        "enfant-f|J'ai soif.",
        "maman|Elle rentre dans le sac.",
        "narrateur|Nina l'écoute, puis la glisse au fond.",
        "papa|L'eau va avec nous.",
        "enfant-f|Le sac est prêt.",
    ],
    2: [
        "narrateur|Nina prend le goûter.",
        "narrateur|Il est dans un linge.",
        "narrateur|Ça sent la pomme douce.",
        "enfant-f|J'ai faim, un peu.",
        "papa|Le goûter rentre dans le sac.",
        "narrateur|Nina le pose à côté du doudou.",
        "maman|La pomme va avec nous.",
        "enfant-f|Le sac est prêt.",
    ],
    3: [
        "narrateur|Nina prend la casquette.",
        "narrateur|Elle est à visière.",
        "narrateur|Le tissu est un peu rêche.",
        "enfant-f|Le soleil est chaud.",
        "maman|La casquette rentre dans le sac.",
        "narrateur|Nina la plie, puis la glisse.",
        "papa|L'ombre va avec nous.",
        "enfant-f|Le sac est prêt.",
    ],
}

PLACE_015 = {
    1: [
        "narrateur|Un grain de sable reste collé au sac.",
        "narrateur|Le sable reste froid sous les chaussures.",
    ],
    2: [
        "narrateur|Le toboggan brille encore derrière eux.",
        "narrateur|Ça sent l'herbe coupée.",
    ],
    3: [
        "narrateur|Une chaîne se tait, tout doux.",
        "narrateur|L'herbe est chaude sous le sac.",
    ],
}

OBJ_MARK_015 = {
    1: "narrateur|Le ballon fait une bosse dans le sac.",
    2: "narrateur|L'anse du seau dépasse un tout petit peu.",
    3: "narrateur|Le doudou chauffe le fond du sac.",
}

IMG_015 = {
    (1, 1, 1): "Un grain de sable reste collé au sac.",
    (1, 1, 2): "Une fourmi traverse le rebord de bois.",
    (1, 1, 3): "Le vent pousse un peu de poussière claire.",
    (1, 2, 1): "Une feuille sèche tourne près des pieds.",
    (1, 2, 2): "Un oiseau saute sur le grillage.",
    (1, 2, 3): "Le soleil chauffe la sangle bleue.",
    (1, 3, 1): "Une flaque reflète le sac ouvert.",
    (1, 3, 2): "Le bois du banc est tout strié.",
    (1, 3, 3): "Un papillon passe, tout jaune.",
    (2, 1, 1): "La terre sent l'eau de la nuit.",
    (2, 1, 2): "Un caillou tapote le seau.",
    (2, 1, 3): "Le toboggan claque tout doux au vent.",
    (2, 2, 1): "Une corde de balançoire craque.",
    (2, 2, 2): "Le sac fait une bosse ronde.",
    (2, 2, 3): "Nina essuie ses mains à l'herbe.",
    (2, 3, 1): "Papa porte le sac un moment.",
    (2, 3, 2): "Maman ferme la fermeture. Ça fait zzz.",
    (2, 3, 3): "Le chemin du parc sent les pins.",
    (3, 1, 1): "Le ballon a cessé de rebondir.",
    (3, 1, 2): "Une pomme sent encore dans le linge.",
    (3, 1, 3): "La visière fait une petite ombre.",
    (3, 2, 1): "L'eau chante encore dans la gourde.",
    (3, 2, 2): "Le linge du goûter est un peu tiède.",
    (3, 2, 3): "Le soleil touche la visière, dans le sac.",
    (3, 3, 1): "Le doudou a quitté le siège de bois.",
    (3, 3, 2): "Le goûter sent la pomme, contre le doudou.",
    (3, 3, 3): "Le vent n'emporte plus la casquette.",
}


def split_img(s: str) -> list[str]:
    parts = [p.strip() for p in s.split(". ") if p.strip()]
    out = []
    for p in parts:
        if not p.endswith((".", "?", "!")):
            p = p + "."
        out.append(f"narrateur|{p}")
    return out


def body_015(i: int, j: int, k: int) -> list[str]:
    lines = list(NEED_015[k])
    lines.append(OBJ_MARK_015[j])
    lines.extend(PLACE_015[i])
    lines.extend(split_img(IMG_015[(i, j, k)]))
    lines.append("maman|On rentre ?")
    lines.append("papa|Oui.")
    lines.append("papa|Le sac vient avec nous.")
    lines.append("narrateur|Nina dit merci.")
    lines.append("narrateur|Les chaussures font toc toc.")
    return lines


def fin_015(i: int, j: int, k: int) -> list[str]:
    loc = L1_015[i]
    obj = L2_015[j]
    need = L3_015[k]
    return [
        *split_img(IMG_015[(i, j, k)]),
        f"narrateur|Nina a joué {loc['ou']}.",
        f"narrateur|Elle a mis {obj['label']} dans le sac.",
        f"narrateur|Elle a mis {need['label']} aussi.",
        "narrateur|Le sac est sur le dos, lourd et doux.",
        "maman|Merci, Nina.",
        "papa|On rentre à la maison.",
        "narrateur|La fenêtre les attend, encore un peu embuée.",
        "narrateur|Le moineau n'est plus sur le rebord.",
    ]


def trans_l2_015(i: int) -> list[str]:
    loc = L1_015[i]
    return [
        f"papa|Nina joue encore un peu, {loc['ou']}.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le sac reste près de nous.",
    ]


def trans_l3_015(i: int) -> list[str]:
    loc = L1_015[i]
    return [
        f"maman|Le sac est encore un peu vide, {loc['ou']}.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "papa|Qu'est-ce qui manque, Nina ?",
    ]


def build_015() -> tuple[dict, dict]:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|La vitre de la cuisine est toute embuée.",
        "narrateur|Un moineau tapote le rebord mouillé.",
        "narrateur|Le soleil revient sur le plancher de bois.",
        "narrateur|Il dessine des carrés chauds, tout jaunes.",
        "narrateur|Ça sent le cacao dans la petite casserole.",
        "narrateur|Un sac bleu est ouvert sur la chaise.",
        "narrateur|Les sangles pendent, molles et lisses.",
        "narrateur|Les chaussettes rouges de Nina sèchent près du radiateur.",
        "papa|Nina, tu as vu le moineau ?",
        "enfant-f|Oui, papa.",
        "enfant-f|Il tapote.",
        "maman|Le parc va sécher, tout à l'heure.",
        "narrateur|En ce moment, Nina est près de la fenêtre.",
        "narrateur|Le sac a un creux tout vide.",
        "enfant-f|Je veux le parc.",
        "maman|Le sac est trop léger, tu sens ?",
        "narrateur|Nina glisse la main dedans.",
        "narrateur|Il n'y a presque rien.",
        "papa|Le doudou chauffe encore près de la vitre.",
        "enfant-f|Je le prends.",
        "narrateur|Elle le pose dans le sac.",
        "narrateur|Le tissu est un peu humide, à cause de la buée.",
        "maman|Merci, Nina.",
        "papa|On y va ?",
        "enfant-f|Oui.",
    ]
    s["CHK_T0001_P0000"] = [
        "maman|On va au parc.",
        "maman|Où va-t-on d'abord ?",
        "narrateur|On peut aller au bac à sable, au toboggan, ou aux balançoires.",
    ]
    extras["CHK_T0001_P0000"] = extras_t3("le bac à sable", "le toboggan", "les balançoires")
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_015[i]
        s[f"{p}_Q0001"] = Q_015[i]
        extras[f"{p}_Q0001"] = extras_q(
            "sac",
            "sac | le sac | dans le sac | elle met | mettre",
            "Elle les met dans le sac. Où les met Nina ?",
        )
        s[f"{p}_C0001"] = C_015[i]
        s[f"{p}_T0002_P0000"] = trans_l2_015(i)
        extras[f"{p}_T0002_P0000"] = extras_t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_015[(i, j)]
            s[f"{p2}_T0003_P0000"] = trans_l3_015(i)
            extras[f"{p2}_T0003_P0000"] = extras_t3("la gourde", "le goûter", "la casquette")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_015(i, j, k)
                s[f"{p3}_F0001"] = fin_015(i, j, k)
    return s, extras


def main() -> None:
    s14, e14 = build_014()
    write_tree(
        "TREE-AUT-014",
        "Nino veut jouer dans la cour, maintenant que la pluie s'est arrêtée. "
        "Une goutte glisse encore sur la vitre du palier. "
        "Il oublie le seau, le manteau ou le doudou. Il revient les prendre. "
        "Ils remontent avec tout. La goutte n'est plus là.",
        "La goutte du palier",
        "Nino, papa, maman",
        "palier d'immeuble, vitre sur la cour, après la pluie",
        s14,
        {
            "CHK_T0000_P0000": "goutte,radiateur",
            "CHK_T0001_P0001": "sable",
            "CHK_T0001_P0002": "enfants_parc",
            "CHK_T0001_P0003": "enfants_parc",
        },
        e14,
    )
    relecture(
        "TREE-AUT-014",
        "La goutte du palier",
        "Nino veut la cour mouillée. Goutte sur la vitre du palier. "
        "Bac / toboggan / balançoires, puis cubes / livre / dînette, "
        "puis manteau / seau / doudou d'abord. Il revient les prendre.",
        "D16 Nino. Monde palier ≠ TREE-AUT-003 (salon, cacao, tapis). "
        "Leçon implicite. Labels T3 = manteau/seau/doudou. Pas Sami. "
        "Fin sensorielle, pas « L'histoire est finie ».",
    )

    s15, e15 = build_015()
    write_tree(
        "TREE-AUT-015",
        "Nina veut le parc. Un moineau tapote la vitre embuée de la cuisine. "
        "Le sac bleu est trop léger. Elle y glisse ce qui manque, pour une raison vécue. "
        "Le sac est chaud contre son dos. La fenêtre les attend.",
        "Le sac près de la buée",
        "Nina, papa, maman",
        "cuisine embuée, sac sur la chaise, puis le parc",
        s15,
        {
            "CHK_T0000_P0000": "enfants_parc",
            "CHK_T0001_P0001": "enfants_parc",
            "CHK_T0001_P0002": "enfants_parc",
            "CHK_T0001_P0003": "enfants_parc",
            "CHK_T0001_P0001_T0002_P0002": "voiture_passe",
        },
        e15,
    )
    relecture(
        "TREE-AUT-015",
        "Le sac près de la buée",
        "Nina veut le parc. Moineau, buée, cacao, sac trop léger. "
        "Bac / toboggan / balançoires, puis ballon / seau / doudou, "
        "puis gourde (soif) / goûter (pomme) / casquette (soleil).",
        "D16 Nina (plus Jules). Pas une liste de sac. Labels T3 = "
        "gourde/goûter/casquette. Pas Tom/Léa/Sami. Fin = fenêtre embuée.",
    )


if __name__ == "__main__":
    main()
