#!/usr/bin/env python3
"""TREE-AUT-036 / TREE-AUT-037 — récit implicite, graphe 86 nœuds, D16."""
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
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} {c['chunk_id']} fin mécanique: {last}")
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


N3 = LIMITS["N3"]
N2 = LIMITS["N2"]


# ---------------------------------------------------------------------------
# TREE-AUT-036  N3  Sarah  AUT.AFF.001
# Oiseau de papier, sac rouge. Pas une liste de sac.
# ≠ TREE-AUT-029 (Nino, toit rouge, vitre, ranger)
# ≠ TREE-AUT-031 (Aniss, sac vert, casquette/gourde/goûter)
# ≠ TREE-COL-001 (pommes, train)
# T3 : le banc / la grille / le cerisier (plus Tom Léa Sami)
# ---------------------------------------------------------------------------

L1_036 = {
    1: {"lab": "le bac à sable", "ou": "du bac à sable", "son": "enfants_parc"},
    2: {"lab": "le toboggan", "ou": "du toboggan", "son": "enfants_parc"},
    3: {"lab": "les balançoires", "ou": "des balançoires", "son": "enfants_parc"},
}
L2_036 = {
    1: {"lab": "le ballon", "obj": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou"},
}
L3_036 = {
    1: {"lab": "le banc", "où": "sur le banc"},
    2: {"lab": "la grille", "où": "contre la grille"},
    3: {"lab": "le cerisier", "où": "sous le cerisier"},
}

ARRIVE_036 = {
    1: vet(
        N3,
        [
            "narrateur|Sarah s'agenouille près du bac.",
            "narrateur|Le sable est frais, un peu humide.",
            "narrateur|Il coule entre ses doigts.",
            "enfant-f|Il est doux, papa.",
            "papa|Oui.",
            "papa|Il est doux et frais.",
            "narrateur|Le sac rouge pose son ombre ronde.",
            "narrateur|Sarah l'ouvre un tout petit peu.",
            "narrateur|L'oiseau de papier regarde le sable.",
            "maman|Le vent tire déjà une aile.",
            "enfant-f|Oh.",
            "enfant-f|Il va s'envoler.",
            "narrateur|Sarah referme le sac, tout doux.",
            "narrateur|Le papier se calme, à l'abri.",
            "papa|Il voyage mieux, là.",
            "enfant-f|Il est au chaud.",
            "narrateur|Une petite pelle jaune attend encore.",
            "narrateur|Un grain de sable brille sur la sangle.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Sarah va vers le toboggan.",
            "narrateur|Le métal est un peu froid.",
            "narrateur|Une marche lisse tient une goutte.",
            "enfant-f|Il est froid, maman.",
            "maman|Oui.",
            "maman|Le soleil va le tiédir.",
            "narrateur|Le sac rouge reste au pied des marches.",
            "narrateur|Sarah l'ouvre un instant.",
            "narrateur|L'oiseau penche vers le plastique.",
            "papa|Une aile touche déjà le vent.",
            "enfant-f|Je le rentre.",
            "narrateur|Elle glisse l'oiseau au fond.",
            "narrateur|Le tissu rouge se referme.",
            "maman|Il est à l'abri, maintenant.",
            "enfant-f|Il verra le ciel plus tard.",
            "narrateur|Une feuille sèche tourne sur une marche.",
            "narrateur|Le sac ne bouge plus.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Sarah va vers les balançoires.",
            "narrateur|Une chaîne fait tic, tout doux.",
            "narrateur|Le siège rouge est encore un peu humide.",
            "enfant-f|Ça bouge tout seul.",
            "maman|C'est le vent, Sarah.",
            "papa|Le sac reste dans l'herbe.",
            "narrateur|Sarah ouvre le sac, tout près d'elle.",
            "narrateur|L'oiseau de papier tremble un peu.",
            "enfant-f|Le vent le tire.",
            "maman|Rentre-le, tout doux.",
            "narrateur|Sarah rentre l'aile pliée.",
            "narrateur|Elle appuie sur le tissu rouge.",
            "papa|Il voyage avec nous, là.",
            "enfant-f|Il est dedans.",
            "narrateur|Un brin d'herbe colle à la sangle.",
            "narrateur|La chaîne ne fait plus tic.",
        ],
    ),
}

Q_036 = {
    1: vet(
        N3,
        [
            "narrateur|L'oiseau de papier s'est calmé, près du bac.",
            "papa|Sarah l'a mis où ?",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|L'aile ne penche plus, au pied du toboggan.",
            "maman|Sarah a mis l'oiseau où ?",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Le vent n'emporte plus le papier.",
            "papa|Sarah a mis l'oiseau où ?",
        ],
    ),
}

C_036 = {
    1: vet(
        N3,
        [
            "narrateur|Oui.",
            "narrateur|L'oiseau est dans le sac rouge.",
            "papa|Merci, Sarah.",
            "maman|Le papier se repose, à l'abri.",
            "enfant-f|Il verra le sable plus tard.",
            "papa|On emporte un jeu, avec lui ?",
            "narrateur|Un grain reste collé à la sangle.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Oui.",
            "narrateur|L'oiseau est dans le sac.",
            "maman|Merci, Sarah.",
            "maman|L'aile ne se plie plus.",
            "enfant-f|Il est au fond.",
            "papa|On emporte un jeu, près des marches ?",
            "narrateur|Une goutte sèche encore sur le métal.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Oui.",
            "narrateur|L'oiseau reste dans le sac rouge.",
            "papa|Merci, Sarah.",
            "enfant-f|Le vent ne le prend plus.",
            "maman|On emporte un jeu, dans l'herbe ?",
            "narrateur|La chaîne se tait, tout à fait.",
            "narrateur|Un brin d'herbe reste sur le tissu.",
        ],
    ),
}

PLAY_036 = {
    (1, 1): vet(
        N3,
        [
            "narrateur|Près du bac, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Sarah pose les deux mains dessus.",
            "narrateur|Le ballon fait un petit bruit.",
            "maman|Le sac reste à ta droite.",
            "papa|L'oiseau est dedans, lui.",
            "enfant-f|Je les vois.",
            "narrateur|Un grain de sable colle au cuir.",
        ],
    ),
    (1, 2): vet(
        N3,
        [
            "narrateur|Près du bac, le seau jaune est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Sarah tient l'anse des deux mains.",
            "narrateur|Le seau racle un peu, toc.",
            "maman|Le sac rouge reste contre le bois.",
            "papa|L'oiseau voyage encore, au fond.",
            "enfant-f|Il ne sort pas.",
            "narrateur|Du sable reste au fond du seau.",
        ],
    ),
    (1, 3): vet(
        N3,
        [
            "narrateur|Près du bac, le doudou gris est là.",
            "narrateur|Le tissu est doux, un peu humide.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Sarah le serre contre elle.",
            "narrateur|Le doudou sent encore le savon.",
            "maman|Le sac attend, tout près.",
            "papa|L'oiseau est à l'abri.",
            "enfant-f|Tous les deux.",
            "narrateur|Le doudou a un grain sur l'oreille.",
        ],
    ),
    (2, 1): vet(
        N3,
        [
            "narrateur|Près du toboggan, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Sarah pose les deux mains dessus.",
            "narrateur|Le ballon s'appuie contre une marche.",
            "maman|Le sac reste au pied, avec l'oiseau.",
            "papa|Je vois le tissu rouge.",
            "enfant-f|Moi aussi.",
            "narrateur|Une goutte a séché sur le cuir.",
        ],
    ),
    (2, 2): vet(
        N3,
        [
            "narrateur|Près du toboggan, le seau jaune est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Sarah tient l'anse des deux mains.",
            "narrateur|Le seau attend au pied du toboggan.",
            "maman|Le sac rouge ne bouge pas.",
            "papa|L'oiseau reste au fond.",
            "enfant-f|Près du seau.",
            "narrateur|L'anse du seau a une goutte.",
        ],
    ),
    (2, 3): vet(
        N3,
        [
            "narrateur|Près du toboggan, le doudou gris est là.",
            "narrateur|Le tissu est doux, un peu humide.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Sarah le serre contre elle.",
            "narrateur|Le doudou regarde le métal froid.",
            "maman|Le sac attend encore, tout bas.",
            "papa|L'oiseau est dedans.",
            "enfant-f|Il se repose.",
            "narrateur|Le doudou a touché la marche lisse.",
        ],
    ),
    (3, 1): vet(
        N3,
        [
            "narrateur|Près des balançoires, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Sarah pose les deux mains dessus.",
            "narrateur|Le ballon rebondit une fois, tout mou.",
            "maman|Le sac est dans l'herbe.",
            "papa|L'oiseau reste à l'abri.",
            "enfant-f|Je les vois.",
            "narrateur|Un brin d'herbe colle au cuir.",
        ],
    ),
    (3, 2): vet(
        N3,
        [
            "narrateur|Près des balançoires, le seau jaune est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Sarah tient l'anse des deux mains.",
            "narrateur|Le seau tapote l'herbe, toc.",
            "maman|Le sac rouge reste à côté.",
            "papa|L'oiseau ne s'envole pas.",
            "enfant-f|Il est au fond.",
            "narrateur|L'anse du seau est froide, encore.",
        ],
    ),
    (3, 3): vet(
        N3,
        [
            "narrateur|Près des balançoires, le doudou gris est là.",
            "narrateur|Le tissu est doux, un peu humide.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Sarah le serre contre elle.",
            "narrateur|Le doudou a senti le vent.",
            "maman|Le sac est dans l'herbe.",
            "papa|L'oiseau se tient tranquille.",
            "enfant-f|Ils sont là.",
            "narrateur|L'oreille du doudou est un peu froide.",
        ],
    ),
}

DEST_036 = {
    1: vet(
        N3,
        [
            "narrateur|Le banc du parc est encore un peu frais.",
            "narrateur|Le bois est lisse, strié.",
            "narrateur|Une miette de pain y brille.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|La grille du parc est verte.",
            "narrateur|Une barre est un peu froide.",
            "narrateur|Une feuille y est coincée.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Le cerisier penche au bord du parc.",
            "narrateur|Une pétale rose tourne, toute lente.",
            "narrateur|L'ombre est tiède, par terre.",
        ],
    ),
}

OPEN_036 = {
    1: vet(
        N3,
        [
            "maman|On peut ouvrir le sac, ici.",
            "narrateur|Sarah pose le sac sur le banc.",
            "narrateur|Elle sort l'oiseau, tout doux.",
            "enfant-f|Il voit le bois.",
            "papa|Une aile attrape le jour.",
            "narrateur|Le papier se déplie un peu.",
        ],
    ),
    2: vet(
        N3,
        [
            "maman|On peut ouvrir le sac, ici.",
            "narrateur|Sarah pose le sac contre la grille.",
            "narrateur|Elle sort l'oiseau, tout doux.",
            "enfant-f|Il voit le ciel.",
            "papa|Une barre tient l'aile, tout calme.",
            "narrateur|Le papier tremble, puis s'arrête.",
        ],
    ),
    3: vet(
        N3,
        [
            "maman|On peut ouvrir le sac, ici.",
            "narrateur|Sarah pose le sac sous le cerisier.",
            "narrateur|Elle sort l'oiseau, tout doux.",
            "enfant-f|Il voit les feuilles.",
            "papa|Une pétale se pose sur l'aile.",
            "narrateur|Le papier sent l'arbre, un peu.",
        ],
    ),
}

HOLD_036 = {
    1: "narrateur|Le ballon reste rond, contre sa jambe.",
    2: "narrateur|Le seau reste dans son autre main.",
    3: "narrateur|Le doudou reste contre sa joue.",
}

IMG_036 = {
    (1, 1, 1): "Un grain de sable reste sur l'aile.",
    (1, 1, 2): "Le ballon frotte la barre verte, tout doux.",
    (1, 1, 3): "Une pétale rose colle au cuir du ballon.",
    (1, 2, 1): "Du sable reste au fond du seau, sur le banc.",
    (1, 2, 2): "Le seau tapote la grille, toc.",
    (1, 2, 3): "Une pétale tombe dans le seau jaune.",
    (1, 3, 1): "Le doudou a un grain de sable, sur le bois.",
    (1, 3, 2): "L'oreille du doudou frotte la feuille coincée.",
    (1, 3, 3): "Le doudou sent la pétale, tout doux.",
    (2, 1, 1): "Le ballon a une trace de métal froid.",
    (2, 1, 2): "Une goutte du toboggan sèche sur la grille.",
    (2, 1, 3): "Le ballon rebondit une fois, sous l'arbre.",
    (2, 2, 1): "L'anse du seau a une goutte, sur le banc.",
    (2, 2, 2): "Le seau jaune brille près de la barre.",
    (2, 2, 3): "L'anse du seau tient une pétale.",
    (2, 3, 1): "Le doudou a touché la marche, puis le bois.",
    (2, 3, 2): "Une goutte du toboggan sèche sur le doudou.",
    (2, 3, 3): "Le doudou passe sous une branche basse.",
    (3, 1, 1): "Le ballon a pris le tic de la chaîne.",
    (3, 1, 2): "Le ballon frotte la feuille coincée.",
    (3, 1, 3): "Un brin d'herbe colle au ballon, sous l'arbre.",
    (3, 2, 1): "Du sable du seau reste sur le banc.",
    (3, 2, 2): "Le seau tapote la barre verte, tout doux.",
    (3, 2, 3): "Le seau jaune brille sous le cerisier.",
    (3, 3, 1): "L'oreille du doudou a pris le bois du banc.",
    (3, 3, 2): "Le doudou passe sous la barre verte.",
    (3, 3, 3): "L'oreille du doudou a une pétale rose.",
}

FIN_IMG_036 = {
    (1, 1, 1): "La chaussette jaune dort encore sur la lampe.",
    (1, 1, 2): "Un rayon passe encore entre deux lunes.",
    (1, 1, 3): "Le fil du plafond ne tourne plus.",
    (1, 2, 1): "Le sac rouge sèche au pied du lit.",
    (1, 2, 2): "Une aile blanche regarde le rideau.",
    (1, 2, 3): "Ça sent encore le savon de la lessive.",
    (1, 3, 1): "L'oreille du doudou dépasse du sac.",
    (1, 3, 2): "Le pull à étoile reste plié.",
    (1, 3, 3): "Une pétale sèche sur le rebord.",
    (2, 1, 1): "Le ballon s'endort près des sangles.",
    (2, 1, 2): "La goutte du toboggan a disparu.",
    (2, 1, 3): "Le cerisier reste loin, derrière la vitre.",
    (2, 2, 1): "L'anse du seau est tiède, maintenant.",
    (2, 2, 2): "La grille du parc ne se voit plus.",
    (2, 2, 3): "Une pétale reste au fond du seau.",
    (2, 3, 1): "Le doudou chauffe le fond du sac.",
    (2, 3, 2): "Le métal du toboggan s'est tu.",
    (2, 3, 3): "L'ombre du cerisier a quitté le tapis.",
    (3, 1, 1): "Le ballon a cessé de rebondir.",
    (3, 1, 2): "La chaîne des balançoires s'est tue.",
    (3, 1, 3): "Une pétale rose sèche sur l'aile.",
    (3, 2, 1): "Le seau pose son ombre sur le tapis.",
    (3, 2, 2): "Un brin d'herbe sèche sur la sangle.",
    (3, 2, 3): "Le cerisier ne penche plus, d'ici.",
    (3, 3, 1): "Le doudou a l'odeur de l'herbe, au lit.",
    (3, 3, 2): "La feuille coincée reste au parc.",
    (3, 3, 3): "L'oiseau de papier se tient tout calme.",
}


def body_036(i: int, j: int, k: int) -> list[str]:
    loc = L1_036[i]
    lines = list(DEST_036[k])
    lines.append(f"narrateur|Sarah vient {loc['ou']}.")
    lines.append(HOLD_036[j])
    lines.extend(OPEN_036[k])
    lines.append(f"narrateur|{IMG_036[(i, j, k)]}")
    return vet(N3, lines)


def fin_036(i: int, j: int, k: int) -> list[str]:
    loc = L1_036[i]
    jeu = L2_036[j]
    dest = L3_036[k]
    return vet(
        N3,
        [
            f"narrateur|{IMG_036[(i, j, k)]}",
            f"narrateur|Sarah a joué {loc['ou']}.",
            f"narrateur|Elle avait {jeu['lab']}.",
            f"narrateur|Puis {dest['lab']}.",
            "enfant-f|L'oiseau est dans le sac.",
            "maman|Oui.",
            "maman|Il rentre à l'abri.",
            "papa|Merci, Sarah.",
            "narrateur|Ils rentrent.",
            f"narrateur|{FIN_IMG_036[(i, j, k)]}",
        ],
    )


def build_036() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N3,
        [
            "narrateur|Un oiseau en papier tourne sous le plafond.",
            "narrateur|Il est blanc, un peu froissé.",
            "narrateur|Le fil fait un petit cercle lent.",
            "narrateur|Les rideaux ont des lunes bleues.",
            "narrateur|Un rayon passe entre deux lunes.",
            "narrateur|La poussière danse, toute fine.",
            "narrateur|Une chaussette jaune dort sur la lampe.",
            "narrateur|Le lit est encore chaud, un peu en vrac.",
            "narrateur|Ça sent le savon de la lessive.",
            "narrateur|Le sac rouge attend au pied du lit.",
            "narrateur|Les sangles pendent, toutes molles.",
            "narrateur|Papa plie un pull à étoile.",
            "narrateur|Maman cherche un petit livre.",
            "maman|Tu as vu l'oiseau, Sarah ?",
            "enfant-f|Oui.",
            "enfant-f|Il tourne.",
            "papa|Il voudra le ciel, plus tard.",
            "narrateur|En ce moment, Sarah tend la main.",
            "narrateur|Le papier est un peu rêche.",
            "enfant-f|Je veux qu'il vole !",
            "maman|D'accord.",
            "narrateur|Sarah décroche le fil, tout doux.",
            "narrateur|L'oiseau penche.",
            "narrateur|Une aile se plie.",
            "enfant-f|Oh.",
            "papa|Le vent de la fenêtre le froisse.",
            "narrateur|Le sac rouge est tout près.",
            "narrateur|Sarah glisse l'oiseau dedans.",
            "narrateur|Le papier se calme, à l'abri.",
            "enfant-f|Il est au chaud.",
            "maman|Oui.",
            "maman|Le sac le porte.",
            "papa|On peut aller le montrer au parc ?",
            "enfant-f|Oui.",
            "narrateur|La chaussette jaune ne bouge pas.",
        ],
    )
    sons["CHK_T0000_P0000"] = "rideau"

    s["CHK_T0001_P0000"] = vet(
        N3,
        [
            "narrateur|Au parc, l'oiseau peut voir trois endroits.",
            "papa|Le bac à sable, le toboggan, ou les balançoires ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("le bac à sable", "le toboggan", "les balançoires")

    for i, loc in L1_036.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_036[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_036[i]
        extras[f"{p}_Q0001"] = qf(
            "sac",
            "sac | le sac | dans le sac | le sac rouge | dedans",
            "Le sac rouge. Sarah a mis l'oiseau où ?",
        )
        s[f"{p}_C0001"] = C_036[i]
        s[f"{p}_T0002_P0000"] = vet(
            N3,
            [
                f"narrateur|{loc['lab'].capitalize()}, Sarah prend un jeu.",
                "papa|Le ballon, le seau, ou le doudou ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_036[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N3,
                [
                    f"narrateur|Sarah a {L2_036[j]['lab']}, et le sac.",
                    "maman|On ouvre le sac où ?",
                    "papa|Le banc, la grille, ou le cerisier ?",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le banc", "la grille", "le cerisier")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_036(i, j, k)
                s[f"{p3}_F0001"] = fin_036(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-037  N2  Chouchou  AUT.AFF.002
# Manteau jaune, gouttière de la maison, limaçon sur le zinc, pain grillé.
# ≠ TREE-AUT-033 (kiosque, manteau bleu, seau)
# ≠ TREE-AUT-014 (palier)
# ≠ TREE-AUT-018 (immeuble, étoile, caisse)
# ≠ TREE-AUT-001 (bateau, rivière de gouttière)
# ≠ TREE-AUT-032 (manteau vert, casserole, orange)
# ≠ TREE-AUT-047 (bottes jaunes, manteau bleu)
# ≠ TREE-AUT-035 (école, fil d'argent, radiateur)
# T3 : le perron / le tonneau / le lilas (plus matin/sieste/soir)
# ---------------------------------------------------------------------------

L1_037 = {
    1: {"lab": "la cuisine", "de": "de la cuisine", "son": "casserole"},
    2: {"lab": "le jardin", "de": "du jardin", "son": "pluie"},
    3: {"lab": "la chambre", "de": "de la chambre", "son": "rideau"},
}
L2_037 = {
    1: {"lab": "les cubes", "obj": "les cubes"},
    2: {"lab": "le livre", "obj": "le livre"},
    3: {"lab": "la dînette", "obj": "une tasse"},
}
L3_037 = {
    1: {"lab": "le perron", "où": "sur le perron"},
    2: {"lab": "le tonneau", "où": "près du tonneau"},
    3: {"lab": "le lilas", "où": "sous le lilas"},
}

ARRIVE_037 = {
    1: vet(
        N2,
        [
            "narrateur|Chouchou reste un moment dans la cuisine.",
            "narrateur|Une miette brille encore sur la table.",
            "narrateur|Le carrelage est un peu froid.",
            "enfant-f|Ça sent le pain, papa.",
            "papa|Oui.",
            "papa|C'est la croûte.",
            "maman|Tu as froid aux bras, Chouchou ?",
            "enfant-f|Un peu.",
            "narrateur|Le manteau jaune frotte la chaise.",
            "narrateur|Le bouton argenté est tiède, déjà.",
            "narrateur|Elle glisse la miette dans sa poche.",
            "narrateur|Le tissu épais la cache.",
            "enfant-f|Pour le limaçon.",
            "papa|Il attend sur le zinc.",
            "maman|Le manteau te tient au chaud.",
            "enfant-f|Il est chaud.",
            "narrateur|La gouttière chante encore, tout bas.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Chouchou s'approche de la vitre du jardin.",
            "narrateur|Une feuille collée tremble dehors.",
            "narrateur|La terre sent l'humidité, tout bas.",
            "enfant-f|Le jardin est là, maman.",
            "maman|Oui.",
            "maman|On y va.",
            "papa|L'air entre, tout froid.",
            "narrateur|Chouchou recule d'un pas.",
            "enfant-f|J'ai froid aux bras.",
            "papa|Ton manteau jaune est sur toi.",
            "narrateur|Elle touche le bouton argenté.",
            "narrateur|Le tissu est un peu rêche au col.",
            "maman|Tu as les boutons ?",
            "enfant-f|Oui.",
            "enfant-f|Ils sont ronds.",
            "narrateur|Derrière la vitre, la feuille attend.",
            "narrateur|La gouttière fait glou, encore.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Chouchou passe par la chambre, un instant.",
            "narrateur|Le rideau gris bouge.",
            "narrateur|Le lit est encore chaud.",
            "enfant-f|Je prends une feuille, pour le limaçon.",
            "papa|Elle est sur l'oreiller ?",
            "enfant-f|Oui.",
            "narrateur|Elle glisse le papier dans sa poche.",
            "narrateur|L'oreiller sent encore le savon.",
            "maman|On sort après, d'accord ?",
            "enfant-f|Vers le zinc.",
            "narrateur|Elle revient dans la cuisine.",
            "narrateur|Le carrelage est froid sous les chaussettes.",
            "narrateur|Le manteau jaune frotte le seuil.",
            "papa|L'air est frais, dehors.",
            "enfant-f|Le manteau est chaud.",
            "maman|Il te tient.",
            "narrateur|La gouttière répond, tout doux.",
        ],
    ),
}

Q_037 = {
    1: vet(
        N2,
        [
            "narrateur|Chouchou a les bras au chaud, dans la cuisine.",
            "papa|Elle a pris quoi, près du crochet ?",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Dehors, Chouchou n'a plus froid aux bras.",
            "maman|Elle a pris quoi, avant le jardin ?",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Le manteau frotte encore le seuil.",
            "papa|Chouchou a pris quoi, près de la porte ?",
        ],
    ),
}

C_037 = {
    1: vet(
        N2,
        [
            "narrateur|Oui.",
            "narrateur|Elle a pris le manteau jaune.",
            "papa|Merci, Chouchou.",
            "maman|Le bouton argenté est à ta hauteur.",
            "enfant-f|Il est chaud.",
            "papa|On emporte un jeu ?",
            "narrateur|La miette reste dans la poche.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Oui.",
            "narrateur|Le manteau jaune est sur elle.",
            "maman|Merci, Chouchou.",
            "maman|Tu n'as plus froid.",
            "enfant-f|Il est chaud.",
            "papa|On emporte un jeu, pour le jardin ?",
            "narrateur|Une feuille collée tremble encore.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Oui.",
            "narrateur|Le manteau est sur Chouchou.",
            "papa|La feuille est dans sa poche.",
            "enfant-f|Pour le limaçon.",
            "maman|On emporte un jeu aussi ?",
            "narrateur|Le rideau de la chambre se tait.",
            "narrateur|Le carrelage reste froid, tout calme.",
        ],
    ),
}

PLAY_037 = {
    (1, 1): vet(
        N2,
        [
            "narrateur|Les cubes de bois sont près de la miette.",
            "narrateur|Ils tapent un peu, toc toc.",
            "papa|Les cubes, Chouchou.",
            "papa|Tu les emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Les cubes.",
            "narrateur|Elle les met dans la petite boîte.",
            "narrateur|Le manteau jaune frotte la table.",
            "maman|Un cube a un coin un peu rêche.",
            "enfant-f|Il gratte.",
            "papa|On fait un pont, pour le limaçon ?",
            "enfant-f|Oui.",
            "narrateur|Un cube attrape un reflet de pain.",
        ],
    ),
    (1, 2): vet(
        N2,
        [
            "narrateur|Le livre est sous le torchon bleu.",
            "narrateur|La couverture est lisse, un peu froide.",
            "maman|Le livre, Chouchou.",
            "maman|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Le livre.",
            "narrateur|Elle le serre contre le manteau.",
            "narrateur|Le tissu jaune cache un coin de page.",
            "papa|On le met à l'abri, sous le jaune.",
            "enfant-f|Il reste au sec.",
            "maman|Une miette reste sur la table.",
            "narrateur|La gouttière chante, tout content.",
        ],
    ),
    (1, 3): vet(
        N2,
        [
            "narrateur|La dînette cliquette dans son panier.",
            "narrateur|Une petite assiette est blanche.",
            "papa|La dînette, Chouchou.",
            "papa|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|La dînette.",
            "narrateur|Elle prend le panier d'une main.",
            "narrateur|L'autre main tient le bouton argenté.",
            "maman|On sert le pain, tout petit ?",
            "enfant-f|Un thé de miette.",
            "narrateur|Une tasse minuscule fait ting.",
            "narrateur|La gouttière chante encore.",
        ],
    ),
    (2, 1): vet(
        N2,
        [
            "narrateur|Les cubes attendent près de la vitre.",
            "narrateur|Un reflet de feuille passe dessus.",
            "maman|Les cubes, Chouchou.",
            "maman|Tu les emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Les cubes.",
            "narrateur|Elle les empile, tout lentement.",
            "narrateur|Le manteau frotte le rebord froid.",
            "papa|Tu as ton manteau, pour le jardin ?",
            "enfant-f|Oui.",
            "enfant-f|Je l'ai pris.",
            "narrateur|La feuille collée tremble encore.",
            "narrateur|Ça sent la terre, tout bas.",
        ],
    ),
    (2, 2): vet(
        N2,
        [
            "narrateur|Le livre est sur la marche, près de la vitre.",
            "narrateur|Une page est un peu cornée.",
            "papa|Le livre, Chouchou.",
            "papa|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Le livre.",
            "narrateur|Elle le glisse sous le bras, contre le jaune.",
            "narrateur|Le col du manteau chatouille le menton.",
            "maman|Une goutte brille sur l'herbe, dehors.",
            "enfant-f|Je la montre au livre.",
            "papa|D'accord.",
            "narrateur|Le jardin attend derrière la porte.",
        ],
    ),
    (2, 3): vet(
        N2,
        [
            "narrateur|La dînette est dans le panier d'osier.",
            "narrateur|L'osier pique un peu les doigts.",
            "maman|La dînette, Chouchou.",
            "maman|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|La dînette.",
            "narrateur|Elle soulève le panier.",
            "narrateur|Le manteau jaune fait un pli au coude.",
            "papa|Tu as ton manteau, pour dehors ?",
            "enfant-f|Oui.",
            "enfant-f|Je l'ai pris.",
            "narrateur|Une petite cuillère brille.",
            "narrateur|La terre du jardin sent la pluie d'hier.",
        ],
    ),
    (3, 1): vet(
        N2,
        [
            "narrateur|Les cubes sont au pied du lit.",
            "narrateur|Un cube tapote le parquet, tout doux.",
            "papa|Les cubes, Chouchou.",
            "papa|Tu les emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Pour le pont.",
            "narrateur|Elle les range dans la boîte.",
            "narrateur|Le manteau frotte la couverture.",
            "maman|La feuille tient contre un cube ?",
            "enfant-f|Oui.",
            "papa|On les emporte.",
            "narrateur|Le rideau gris touche son épaule.",
        ],
    ),
    (3, 2): vet(
        N2,
        [
            "narrateur|Sur la couverture, le livre est ouvert.",
            "narrateur|Le rideau gris colore la page.",
            "maman|Le livre, Chouchou.",
            "maman|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Le livre.",
            "narrateur|Elle le glisse sous le manteau.",
            "narrateur|Il reste au chaud, contre le jaune.",
            "papa|La feuille peut servir de marque-page ?",
            "enfant-f|Oui.",
            "narrateur|Une page se recourbe, tout doux.",
            "narrateur|L'oreiller sent encore le savon.",
        ],
    ),
    (3, 3): vet(
        N2,
        [
            "narrateur|La dînette attend au pied du lit.",
            "narrateur|Une petite tasse est près de la feuille.",
            "papa|La dînette, Chouchou.",
            "papa|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Un thé de gouttière.",
            "narrateur|Elle prend le panier.",
            "narrateur|Le manteau jaune cache l'osier.",
            "maman|La tasse tient dans la poche ?",
            "enfant-f|À côté du bouton.",
            "narrateur|La petite assiette reste dans l'autre main.",
            "narrateur|Le tapis de la chambre est calme.",
        ],
    ),
}

DEST_037 = {
    1: vet(
        N2,
        [
            "narrateur|Le perron est encore mouillé.",
            "narrateur|Une goutte y fait un rond sombre.",
            "narrateur|Le zinc chante juste au-dessus.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le tonneau récupère l'eau de la gouttière.",
            "narrateur|Le bois est sombre, un peu rêche.",
            "narrateur|Une feuille y tourne, toute lente.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Le lilas penche, encore mouillé.",
            "narrateur|Une grappe violette sent le jardin.",
            "narrateur|Une goutte y tremble, puis tombe.",
        ],
    ),
}

SORTIE_037 = {
    1: vet(
        N2,
        [
            "papa|Le limaçon est sur le zinc, au-dessus.",
            "narrateur|Ils sortent un moment.",
            "narrateur|L'air touche le nez de Chouchou.",
            "enfant-f|La miette est pour lui.",
            "maman|Tes bras, dans le manteau ?",
            "enfant-f|Ils sont au chaud.",
        ],
    ),
    2: vet(
        N2,
        [
            "papa|Le limaçon a glissé vers le tonneau.",
            "narrateur|Ils sortent un moment.",
            "narrateur|L'eau du tonneau est sombre.",
            "enfant-f|Je vois le trait d'argent.",
            "maman|Le manteau te tient.",
            "enfant-f|Oui, un peu.",
        ],
    ),
    3: vet(
        N2,
        [
            "papa|Le limaçon a gagné la feuille du lilas.",
            "narrateur|Ils sortent un moment.",
            "narrateur|La grappe violette est lourde d'eau.",
            "enfant-f|Je vois les lumières.",
            "maman|Le manteau te tient chaud.",
            "enfant-f|Oui, maman.",
        ],
    ),
}

JEU_DEHORS_037 = {
    (1, 1): "narrateur|Chouchou pose les cubes un moment sur le perron.",
    (1, 2): "narrateur|Chouchou ouvre le livre un instant, près de la porte.",
    (1, 3): "narrateur|Chouchou pose une tasse minuscule, puis la reprend.",
    (2, 1): "narrateur|Au jardin, Chouchou empile deux cubes sur une pierre.",
    (2, 2): "narrateur|Au jardin, Chouchou montre une image à la feuille.",
    (2, 3): "narrateur|Au jardin, Chouchou sert une feuille dans l'assiette.",
    (3, 1): "narrateur|Près du seuil, Chouchou pose la feuille sur un cube.",
    (3, 2): "narrateur|Près du seuil, Chouchou glisse la feuille dans le livre.",
    (3, 3): "narrateur|Près du seuil, Chouchou sert la feuille dans la tasse.",
}

RETOUR_037 = vet(
    N2,
    [
        "maman|C'est l'heure de rentrer.",
        "narrateur|Ils rentrent.",
        "narrateur|La maison est tiède.",
        "narrateur|Le manteau jaune est un peu lourd.",
        "narrateur|Il goutte, tout doux.",
        "papa|Il sèche mieux, au crochet.",
        "narrateur|Chouchou retire le manteau jaune.",
        "narrateur|Elle le raccroche au crochet froid.",
        "narrateur|Le bouton argenté pend, calme.",
        "enfant-f|Il est à sa place.",
        "maman|Oui.",
        "maman|Il sèche, là.",
        "papa|Merci, Chouchou.",
    ],
)

IMG_037 = {
    (1, 1, 1): "Un cube a un peu de miette au coin.",
    (1, 1, 2): "Le torchon bleu a glissé du dossier.",
    (1, 1, 3): "La gouttière ne tremble plus.",
    (1, 2, 1): "Une page du livre sent le pain.",
    (1, 2, 2): "Une miette reste sous le livre.",
    (1, 2, 3): "Le zinc fait un dernier glou.",
    (1, 3, 1): "La petite tasse est encore tiède.",
    (1, 3, 2): "Une cuillère minuscule brille.",
    (1, 3, 3): "Le panier d'osier est posé droit.",
    (2, 1, 1): "Une goutte d'herbe sèche sur un cube.",
    (2, 1, 2): "La feuille collée ne tremble plus.",
    (2, 1, 3): "Un peu de terre reste au seuil.",
    (2, 2, 1): "Le livre a une page un peu fraîche.",
    (2, 2, 2): "Une goutte a séché sur la vitre.",
    (2, 2, 3): "L'herbe a laissé une odeur verte.",
    (2, 3, 1): "Une feuille a voyagé dans l'assiette.",
    (2, 3, 2): "L'osier sent encore le jardin.",
    (2, 3, 3): "Le panier a une petite tache d'eau.",
    (3, 1, 1): "La feuille repose sur un cube.",
    (3, 1, 2): "Un cube est contre l'oreiller, tout calme.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Une bande grise colore encore la page.",
    (3, 2, 2): "Sur la couverture, le livre reste ouvert.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FIN_IMG_037 = {
    (1, 1, 1): "La gouttière fait un tout petit glou.",
    (1, 1, 2): "Une miette reste sur la table.",
    (1, 1, 3): "Le bouton argenté brille, au crochet.",
    (1, 2, 1): "Un oiseau chante encore, tout loin.",
    (1, 2, 2): "La page se recourbe, près du bol.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "Le pain sent encore, tout bas.",
    (1, 3, 3): "Le manteau jaune sèche, au crochet.",
    (2, 1, 1): "Les chaussettes sèchent près de la porte.",
    (2, 1, 2): "L'herbe colle encore à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau.",
    (2, 2, 1): "Une feuille vraie reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "Le limaçon ne brille plus, dehors.",
    (2, 3, 1): "La petite assiette a encore de l'herbe.",
    (2, 3, 2): "Le col jaune sèche, au crochet.",
    (2, 3, 3): "Une odeur de terre reste au seuil.",
    (3, 1, 1): "La feuille repose sur un cube.",
    (3, 1, 2): "L'oreiller sent encore le savon.",
    (3, 1, 3): "Plus rien ne bouge, au rideau gris.",
    (3, 2, 1): "La feuille sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près de la feuille.",
    (3, 3, 2): "Le tapis de la chambre est calme.",
    (3, 3, 3): "Le zinc se tait tout loin, tout doux.",
}


def body_037(i: int, j: int, k: int) -> list[str]:
    loc = L1_037[i]
    jeu = L2_037[j]
    lines = list(DEST_037[k])
    lines.extend(SORTIE_037[k])
    lines.append(JEU_DEHORS_037[(i, j)])
    lines.extend(RETOUR_037)
    lines.append(f"narrateur|{jeu['obj'].capitalize()} rentre avec eux.")
    lines.append(f"narrateur|{IMG_037[(i, j, k)]}")
    return vet(N2, lines)


def fin_037(i: int, j: int, k: int) -> list[str]:
    loc = L1_037[i]
    jeu = L2_037[j]
    dest = L3_037[k]
    return vet(
        N2,
        [
            f"narrateur|{IMG_037[(i, j, k)]}",
            f"narrateur|Chouchou est passée {loc['de']}.",
            f"narrateur|Elle a pris {jeu['lab']}.",
            f"narrateur|C'était {dest['où']}.",
            "enfant-f|Le manteau est au crochet.",
            "maman|Oui.",
            "maman|Il sèche, là.",
            "papa|Merci, Chouchou.",
            f"narrateur|{FIN_IMG_037[(i, j, k)]}",
            "narrateur|Chouchou touche encore le bouton argenté.",
        ],
    )


def build_037() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N2,
        [
            "narrateur|La buée du pain grillé colle à la vitre.",
            "narrateur|Un trait d'argent la traverse, tout mince.",
            "narrateur|Le limaçon est déjà dehors, sur le zinc.",
            "narrateur|La gouttière répond, glou, tout bas.",
            "narrateur|Une goutte tombe sur le carreau.",
            "narrateur|Elle fait un rond brillant.",
            "narrateur|Ça sent encore la croûte chaude.",
            "narrateur|Une miette reste sur la table.",
            "narrateur|Le manteau jaune attend au crochet.",
            "narrateur|Le crochet est froid, tout près.",
            "narrateur|Un bouton argenté brille.",
            "narrateur|Papa essuie la goutte.",
            "narrateur|Il a un torchon bleu.",
            "narrateur|Maman plie une écharpe de laine.",
            "papa|Tu as vu le limaçon, Chouchou ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il est sur le zinc.",
            "narrateur|En ce moment, Chouchou prend la miette.",
            "narrateur|Elle est un peu sèche.",
            "enfant-f|Je la lui donne !",
            "maman|D'accord.",
            "narrateur|Chouchou ouvre la porte, tout doux.",
            "narrateur|Une goutte de la gouttière saute.",
            "narrateur|Elle touche son bras.",
            "enfant-f|Oh.",
            "enfant-f|C'est froid.",
            "papa|Le manteau jaune est là.",
            "narrateur|Chouchou glisse un bras, puis l'autre.",
            "narrateur|Le tissu est un peu épais.",
            "enfant-f|Il est chaud.",
            "maman|Le bouton est lisse, tu sens ?",
            "enfant-f|Oui.",
            "papa|On peut aller au zinc ?",
            "enfant-f|Avec la miette.",
            "narrateur|La gouttière chante encore, tout bas.",
        ],
    )
    sons["CHK_T0000_P0000"] = "gouttiere,pain"

    s["CHK_T0001_P0000"] = vet(
        N2,
        [
            "papa|On passe où, avant le zinc ?",
            "narrateur|La cuisine.",
            "narrateur|Le jardin.",
            "narrateur|Ou la chambre.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("la cuisine", "le jardin", "la chambre")

    for i, loc in L1_037.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_037[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_037[i]
        extras[f"{p}_Q0001"] = qf(
            "manteau",
            "manteau | le manteau | son manteau | le manteau jaune",
            "Le manteau jaune. Chouchou a pris quoi ?",
        )
        s[f"{p}_C0001"] = C_037[i]
        s[f"{p}_T0002_P0000"] = vet(
            N2,
            [
                "maman|Tu emportes quel jeu ?",
                "narrateur|Les cubes.",
                "narrateur|Le livre.",
                "narrateur|Ou la dînette.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("les cubes", "le livre", "la dînette")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_037[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N2,
                [
                    "papa|On va jusqu'où, avec le manteau ?",
                    "narrateur|Le perron.",
                    "narrateur|Le tonneau.",
                    "narrateur|Ou le lilas.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le perron", "le tonneau", "le lilas")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_037(i, j, k)
                s[f"{p3}_F0001"] = fin_037(i, j, k)
    return s, sons, extras


def main() -> None:
    s36, n36, e36 = build_036()
    write_tree(
        "TREE-AUT-036",
        "Sarah veut que l'oiseau de papier voie le ciel du parc. "
        "Le vent de la fenêtre plie une aile. Elle glisse l'oiseau "
        "dans le sac rouge, à l'abri. Bac, toboggan ou balançoires, "
        "puis un jeu, puis le banc, la grille ou le cerisier : "
        "elle ouvre le sac. Pas une liste.",
        "L'oiseau de papier et le sac rouge de Sarah",
        "Sarah, papa, maman",
        "chambre, oiseau de papier au plafond, rideaux à lunes, sac rouge",
        s36,
        n36,
        e36,
    )
    relecture(
        "TREE-AUT-036",
        "L'oiseau de papier et le sac rouge de Sarah",
        "Sarah veut que l'oiseau vole au parc. Fil, lunes bleues, "
        "chaussette jaune, sac rouge. Le vent plie une aile : "
        "l'oiseau va dans le sac. Bac / toboggan / balançoires, "
        "puis ballon / seau / doudou, puis banc / grille / cerisier. "
        "Elle ouvre le sac. Fin sensorielle.",
        "Zoé→Sarah (D16). N3. AUT.AFF.001 implicite. "
        "Pas une liste de sac. Monde ≠ TREE-AUT-029 (toit rouge, ranger). "
        "Monde ≠ TREE-AUT-031 (sac vert, casquette). "
        "Monde ≠ TREE-COL-001 (pommes, train). "
        "T3 = banc/grille/cerisier (plus Tom/Léa/Sami). "
        "Pas « on va apprendre ». Fin sensorielle.",
    )

    s37, n37, e37 = build_037()
    write_tree(
        "TREE-AUT-037",
        "Chouchou veut porter une miette au limaçon, sur le zinc. "
        "La gouttière de la maison fait glou. Une goutte lui touche "
        "le bras : elle prend le manteau jaune. En rentrant, il goutte : "
        "elle le raccroche. Perron, tonneau ou lilas : la suite change.",
        "Le manteau jaune près de la gouttière",
        "Chouchou, papa, maman",
        "cuisine, pain grillé, vitre, zinc, gouttière, crochet",
        s37,
        n37,
        e37,
    )
    relecture(
        "TREE-AUT-037",
        "Le manteau jaune près de la gouttière",
        "Chouchou veut la miette pour le limaçon du zinc. "
        "Buée du pain, trait d'argent, manteau jaune, bouton argenté. "
        "Cuisine / jardin / chambre, puis cubes / livre / dînette, "
        "puis perron / tonneau / lilas. Goutte froide, manteau, "
        "retour : elle le raccroche.",
        "Sara→Chouchou (D16). N2. AUT.AFF.002 implicite. "
        "Gouttière de la maison ≠ kiosque 033, ≠ palier 014, "
        "≠ immeuble 018, ≠ bateau 001, ≠ casserole 032, "
        "≠ bottes 047, ≠ école 035. T3 = perron/tonneau/lilas. "
        "Fin = bouton au crochet, pas « L'histoire est finie ».",
    )


if __name__ == "__main__":
    main()
