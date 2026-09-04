#!/usr/bin/env python3
"""TREE-AUT-032 / TREE-AUT-033 — récit implicite, graphe 86 nœuds, D16."""
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
N1 = LIMITS["N1"]


# ---------------------------------------------------------------------------
# TREE-AUT-032  N3  Mila  AUT.AFF.002  manteau vert, casserole, orange
# ≠ TREE-AUT-016 (Raphaël, laine, radiateur, flaque, bottes jaunes)
# ≠ TREE-COL-001 (pommes, train, voyage)
# ---------------------------------------------------------------------------

L1_032 = {
    1: {"lab": "la cuisine", "ou": "par la cuisine", "son": "casserole"},
    2: {"lab": "le jardin", "ou": "par le jardin", "son": "pluie"},
    3: {"lab": "la chambre", "ou": "par la chambre", "son": "rideau"},
}
L2_032 = {
    1: {"lab": "les cubes", "un": "un cube"},
    2: {"lab": "le livre", "un": "le livre"},
    3: {"lab": "la dînette", "un": "une tasse"},
}
L3_032 = {
    1: {"lab": "le matin", "quand": "le matin"},
    2: {"lab": "après la sieste", "quand": "après la sieste"},
    3: {"lab": "le soir", "quand": "le soir"},
}

ARRIVE_032 = {
    1: vet(
        N3,
        [
            "narrateur|Mila reste un moment dans la cuisine.",
            "narrateur|Une miette d'orange brille sur la planche.",
            "narrateur|Le couvercle fait encore un tout petit bruit.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Oui.",
            "papa|C'est l'orange.",
            "maman|Tu as froid aux bras, Mila ?",
            "enfant-f|Un peu.",
            "narrateur|Mila va vers le crochet bas.",
            "narrateur|Le manteau vert l'attend, tout près.",
            "narrateur|Elle glisse un bras.",
            "narrateur|L'autre manche est encore à l'envers.",
            "enfant-f|Oh.",
            "maman|On tourne le tissu.",
            "narrateur|Maman tourne la manche épaisse.",
            "narrateur|Mila glisse l'autre bras.",
            "narrateur|Les boutons de bois sont tièdes.",
            "papa|Il te va bien, ce vert.",
            "enfant-f|Il est chaud.",
            "narrateur|Le frigo ronronne encore.",
            "narrateur|La farine reste comme un petit nuage.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Mila s'approche de la vitre du jardin.",
            "narrateur|Une feuille collée tremble dehors.",
            "narrateur|La terre sent l'humidité, tout bas.",
            "enfant-f|Le jardin est là, maman.",
            "maman|Oui.",
            "maman|On y va.",
            "papa|L'air entre, tout froid.",
            "narrateur|Mila recule d'un pas.",
            "enfant-f|J'ai froid aux bras.",
            "papa|Ton manteau vert est au crochet.",
            "narrateur|Elle revient vers la porte.",
            "narrateur|Le manteau vert est à sa hauteur.",
            "narrateur|Elle glisse un bras, puis l'autre.",
            "narrateur|Le tissu est un peu rêche au col.",
            "maman|Tu as les boutons ?",
            "enfant-f|Oui.",
            "enfant-f|Ils sont ronds.",
            "narrateur|Derrière la vitre, la feuille attend.",
            "narrateur|La casserole chante encore, tout doux.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Mila passe par la chambre, un instant.",
            "narrateur|Le rideau jaune bouge.",
            "narrateur|Le lit est encore chaud.",
            "enfant-f|Je prends le bateau d'orange.",
            "papa|Il est sur l'oreiller ?",
            "enfant-f|Oui.",
            "narrateur|Elle glisse l'écorce dans sa main.",
            "narrateur|L'oreiller sent encore le savon.",
            "maman|On sort après, d'accord ?",
            "enfant-f|Vers la flaque.",
            "narrateur|Elle revient dans la cuisine.",
            "narrateur|Le carrelage est froid sous les chaussettes.",
            "narrateur|Le crochet bas l'attend près de la porte.",
            "papa|L'air est frais, dehors.",
            "narrateur|Mila prend le manteau vert.",
            "narrateur|Une manche frotte la farine, tout doux.",
            "enfant-f|Il sent l'orange, un peu.",
            "maman|Il te tient chaud.",
            "narrateur|Le frigo fait un nouveau petit ronron.",
        ],
    ),
}

Q_032 = {
    1: vet(
        N3,
        [
            "narrateur|Mila a les bras au chaud, dans la cuisine.",
            "papa|Elle a pris quoi, près du crochet ?",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Dehors, Mila n'a plus froid aux bras.",
            "maman|Elle a pris quoi, avant le jardin ?",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Le manteau frotte encore la farine.",
            "papa|Mila a pris quoi, près de la porte ?",
        ],
    ),
}

C_032 = {
    1: vet(
        N3,
        [
            "narrateur|Oui.",
            "narrateur|Elle a pris le manteau vert.",
            "papa|Merci, Mila.",
            "maman|Les boutons de bois sont à ta hauteur.",
            "enfant-f|Il est chaud.",
            "papa|On emporte un jeu ?",
            "narrateur|Le torchon rayé bouge un peu.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Oui.",
            "narrateur|Le manteau vert est sur elle.",
            "maman|Bravo.",
            "maman|Tu n'as plus froid.",
            "enfant-f|Il est chaud.",
            "papa|On emporte un jeu, pour le jardin ?",
            "narrateur|Une pelure d'orange reste sur la planche.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Oui.",
            "narrateur|Le manteau est sur Mila.",
            "papa|Le bateau d'orange est dans sa main.",
            "enfant-f|Pour la flaque.",
            "maman|On emporte un jeu aussi ?",
            "narrateur|Le rideau de la chambre se tait.",
            "narrateur|Le carrelage reste froid, tout calme.",
        ],
    ),
}

PLAY_032 = {
    (1, 1): vet(
        N3,
        [
            "narrateur|Les cubes de bois sont près de la farine.",
            "narrateur|Ils tapent un peu, toc toc.",
            "papa|Les cubes, Mila.",
            "papa|Tu les emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Les cubes.",
            "narrateur|Elle les met dans la petite boîte.",
            "narrateur|Le manteau vert frotte la table.",
            "maman|Un cube a un coin un peu rêche.",
            "enfant-f|Il gratte.",
            "papa|On fait un pont, pour la flaque ?",
            "enfant-f|Oui.",
            "narrateur|Un cube attrape un reflet d'orange.",
        ],
    ),
    (1, 2): vet(
        N3,
        [
            "narrateur|Le livre est sous le torchon rayé.",
            "narrateur|La couverture est lisse, un peu froide.",
            "maman|Le livre, Mila.",
            "maman|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Le livre.",
            "narrateur|Elle le serre contre le manteau.",
            "narrateur|Le tissu vert cache un coin de page.",
            "papa|On le met à l'abri, sous le vert.",
            "enfant-f|Il reste au sec.",
            "maman|Une miette d'orange reste sur la table.",
            "narrateur|Le frigo ronronne, tout content.",
        ],
    ),
    (1, 3): vet(
        N3,
        [
            "narrateur|La dînette cliquette dans son panier.",
            "narrateur|Une petite assiette est blanche.",
            "papa|La dînette, Mila.",
            "papa|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|La dînette.",
            "narrateur|Elle prend le panier d'une main.",
            "narrateur|L'autre main tient un bouton de bois.",
            "maman|On sert l'orange, tout petit ?",
            "enfant-f|Un thé d'écorce.",
            "narrateur|Une tasse minuscule fait ting.",
            "narrateur|La casserole chante encore.",
        ],
    ),
    (2, 1): vet(
        N3,
        [
            "narrateur|Les cubes attendent près de la vitre.",
            "narrateur|Un reflet de feuille passe dessus.",
            "maman|Les cubes, Mila.",
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
        N3,
        [
            "narrateur|Le livre est sur la marche, près de la vitre.",
            "narrateur|Une page est un peu cornée.",
            "papa|Le livre, Mila.",
            "papa|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Le livre.",
            "narrateur|Elle le glisse sous le bras, contre le vert.",
            "narrateur|Le col du manteau chatouille le menton.",
            "maman|Une goutte brille sur l'herbe, dehors.",
            "enfant-f|Je la montre au livre.",
            "papa|D'accord.",
            "narrateur|Le jardin attend derrière la porte.",
        ],
    ),
    (2, 3): vet(
        N3,
        [
            "narrateur|La dînette est dans le panier d'osier.",
            "narrateur|L'osier pique un peu les doigts.",
            "maman|La dînette, Mila.",
            "maman|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|La dînette.",
            "narrateur|Elle soulève le panier.",
            "narrateur|Le manteau vert fait un pli au coude.",
            "papa|Tu as ton manteau, pour dehors ?",
            "enfant-f|Oui.",
            "enfant-f|Je l'ai pris.",
            "narrateur|Une petite cuillère brille.",
            "narrateur|La terre du jardin sent la pluie d'hier.",
        ],
    ),
    (3, 1): vet(
        N3,
        [
            "narrateur|Les cubes sont au pied du lit.",
            "narrateur|Un cube tapote le parquet, tout doux.",
            "papa|Les cubes, Mila.",
            "papa|Tu les emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Pour le pont.",
            "narrateur|Elle les range dans la boîte.",
            "narrateur|Le manteau frotte la couverture.",
            "maman|Le bateau d'orange tient contre un cube ?",
            "enfant-f|Oui.",
            "papa|On les emporte.",
            "narrateur|Le rideau jaune touche son épaule.",
        ],
    ),
    (3, 2): vet(
        N3,
        [
            "narrateur|Sur la couverture, le livre est ouvert.",
            "narrateur|Le rideau jaune colore la page.",
            "maman|Le livre, Mila.",
            "maman|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Le livre.",
            "narrateur|Elle le glisse sous le manteau.",
            "narrateur|Il reste au chaud, contre le vert.",
            "papa|Le bateau d'orange peut servir de marque-page ?",
            "enfant-f|Oui.",
            "narrateur|Une page se recourbe, tout doux.",
            "narrateur|L'oreiller sent encore le savon.",
        ],
    ),
    (3, 3): vet(
        N3,
        [
            "narrateur|La dînette attend au pied du lit.",
            "narrateur|Une petite tasse est près du bateau.",
            "papa|La dînette, Mila.",
            "papa|Tu l'emportes ?",
            "enfant-f|Oui.",
            "enfant-f|Un thé de flaque.",
            "narrateur|Elle prend le panier.",
            "narrateur|Le manteau vert cache l'osier.",
            "maman|La tasse tient dans la poche ?",
            "enfant-f|À côté du bouton.",
            "narrateur|La petite assiette reste dans l'autre main.",
            "narrateur|Le tapis de la chambre est calme.",
        ],
    ),
}

MOMENT_032 = {
    1: vet(
        N3,
        [
            "narrateur|Le matin, la lumière est pâle, un peu bleue.",
            "narrateur|Un oiseau chante une fois.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Après la sieste, l'air de la maison est tiède.",
            "narrateur|Les joues de Mila sont encore chaudes.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Le soir, la lumière de la cuisine devient orange.",
            "narrateur|La casserole s'est tue, enfin.",
        ],
    ),
}

SORTIE_032 = {
    1: vet(
        N3,
        [
            "papa|La flaque est claire, ce matin.",
            "narrateur|Ils sortent un moment.",
            "narrateur|L'air touche le nez de Mila.",
            "enfant-f|Elle brille.",
            "maman|Tes bras, dans le manteau ?",
            "enfant-f|Ils sont au chaud.",
        ],
    ),
    2: vet(
        N3,
        [
            "papa|La flaque a rétréci, un peu.",
            "narrateur|Ils sortent un moment.",
            "narrateur|Le soleil est jaune et doux.",
            "enfant-f|Elle est tiède.",
            "maman|Le manteau est encore utile.",
            "enfant-f|Oui, un peu.",
        ],
    ),
    3: vet(
        N3,
        [
            "papa|La flaque est sombre, ce soir.",
            "narrateur|Ils sortent un moment.",
            "narrateur|La vitre de la maison est bleue.",
            "enfant-f|Je vois les lumières.",
            "maman|Le manteau te tient chaud.",
            "enfant-f|Oui, maman.",
        ],
    ),
}

JEU_DEHORS_032 = {
    (1, 1): "narrateur|Mila pose les cubes un moment sur le pas de la porte.",
    (1, 2): "narrateur|Mila ouvre le livre un instant, près de la porte.",
    (1, 3): "narrateur|Mila pose une tasse minuscule, puis la reprend.",
    (2, 1): "narrateur|Au jardin, Mila empile deux cubes sur une pierre.",
    (2, 2): "narrateur|Au jardin, Mila montre une image à la feuille.",
    (2, 3): "narrateur|Au jardin, Mila sert une feuille dans l'assiette.",
    (3, 1): "narrateur|Près du seuil, Mila pose le bateau sur un cube.",
    (3, 2): "narrateur|Près du seuil, Mila glisse l'écorce dans le livre.",
    (3, 3): "narrateur|Près du seuil, Mila sert l'écorce dans la tasse.",
}

RETOUR_032 = vet(
    N3,
    [
        "maman|C'est l'heure de rentrer.",
        "narrateur|Ils rentrent.",
        "narrateur|La maison est tiède.",
        "narrateur|Le manteau vert est un peu lourd.",
        "narrateur|Il goutte, tout doux.",
        "papa|Il sèche mieux, au crochet.",
        "narrateur|Mila retire le manteau vert.",
        "narrateur|Elle le raccroche au crochet bas.",
        "narrateur|Les boutons de bois pendent, calmes.",
        "enfant-f|Il est à sa place.",
        "maman|Oui.",
        "maman|Il sèche, là.",
        "papa|Merci, Mila.",
    ],
)

IMG_032 = {
    (1, 1, 1): "Un cube a un peu de farine au coin.",
    (1, 1, 2): "Le torchon rayé a glissé du dossier.",
    (1, 1, 3): "Le couvercle ne tremble plus.",
    (1, 2, 1): "Une page du livre sent l'orange.",
    (1, 2, 2): "Une miette reste sous le livre.",
    (1, 2, 3): "Le frigo fait un dernier ronron.",
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
    (3, 1, 1): "Le bateau d'orange repose sur un cube.",
    (3, 1, 2): "Un cube est contre l'oreiller, tout calme.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Une bande jaune colore encore la page.",
    (3, 2, 2): "Sur la couverture, le livre reste ouvert.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FIN_IMG_032 = {
    (1, 1, 1): "La casserole fait un tout petit pschitt.",
    (1, 1, 2): "Une miette reste sur la table.",
    (1, 1, 3): "Le bouton de bois brille, au crochet.",
    (1, 2, 1): "Un oiseau chante encore, tout loin.",
    (1, 2, 2): "La page se recourbe, près du bol.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "L'orange sent encore, tout bas.",
    (1, 3, 3): "Le manteau vert sèche, au crochet.",
    (2, 1, 1): "Les chaussettes sèchent près de la porte.",
    (2, 1, 2): "L'herbe colle encore à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau.",
    (2, 2, 1): "Une feuille vraie reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "La flaque ne brille plus, dehors.",
    (2, 3, 1): "La petite assiette a encore de l'herbe.",
    (2, 3, 2): "Le col vert sèche, au crochet.",
    (2, 3, 3): "Une odeur de terre reste au seuil.",
    (3, 1, 1): "Le bateau d'orange repose sur un cube.",
    (3, 1, 2): "L'oreiller sent encore le savon.",
    (3, 1, 3): "Plus rien ne bouge, au rideau jaune.",
    (3, 2, 1): "Le bateau sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près du bateau.",
    (3, 3, 2): "Le tapis de la chambre est calme.",
    (3, 3, 3): "Le frigo ronronne tout loin, tout doux.",
}


def body_032(i: int, j: int, k: int) -> list[str]:
    loc = L1_032[i]
    jeu = L2_032[j]
    lines = list(MOMENT_032[k])
    lines.extend(SORTIE_032[k])
    lines.append(JEU_DEHORS_032[(i, j)])
    lines.extend(RETOUR_032)
    lines.append(f"narrateur|{jeu['un'].capitalize()} rentre avec eux.")
    lines.append(f"narrateur|{IMG_032[(i, j, k)]}")
    return vet(N3, lines)


def fin_032(i: int, j: int, k: int) -> list[str]:
    loc = L1_032[i]
    jeu = L2_032[j]
    mom = L3_032[k]
    return vet(
        N3,
        [
            f"narrateur|{IMG_032[(i, j, k)]}",
            f"narrateur|Mila est passée {loc['ou']}.",
            f"narrateur|Elle a pris {jeu['lab']}.",
            f"narrateur|C'était {mom['quand']}.",
            "enfant-f|Le manteau est au crochet.",
            "maman|Oui.",
            "maman|Il sèche, là.",
            "papa|Merci, Mila.",
            f"narrateur|{FIN_IMG_032[(i, j, k)]}",
            "narrateur|Mila touche encore un bouton de bois.",
        ],
    )


def build_032() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N3,
        [
            "narrateur|Le couvercle de la casserole tremble.",
            "narrateur|Ça sent l'orange pelée.",
            "narrateur|De la farine blanche reste sur la table.",
            "narrateur|Le frigo fait un petit ronron.",
            "narrateur|Un torchon rayé sèche sur le dossier.",
            "narrateur|La lumière de la cuisine est jaune.",
            "narrateur|Elle touche le carrelage, un peu froid.",
            "narrateur|Près de la porte, un crochet bas attend.",
            "narrateur|Le manteau vert de Mila y pend.",
            "narrateur|Les boutons sont en bois, ronds et lisses.",
            "narrateur|Papa coupe encore une orange.",
            "narrateur|Maman essuie un coin de table.",
            "maman|Mila, tu as vu ton manteau ?",
            "enfant-f|Oui.",
            "enfant-f|Il est vert.",
            "papa|Il est à ta hauteur.",
            "narrateur|En ce moment, Mila pose la main dessus.",
            "narrateur|Le tissu est un peu épais.",
            "enfant-f|Je veux sortir !",
            "enfant-f|Le bateau d'orange, dans la flaque.",
            "papa|D'accord.",
            "narrateur|Mila tire la poignée, tout doux.",
            "narrateur|L'air froid entre.",
            "enfant-f|J'ai froid, papa.",
            "papa|Le manteau vert est là.",
            "papa|Il attend, au crochet.",
            "narrateur|Mila prend le manteau.",
            "narrateur|Une manche est à l'envers.",
            "enfant-f|Oh.",
            "enfant-f|Ça ne passe pas.",
            "maman|On tourne la manche.",
            "narrateur|Maman tourne le tissu épais.",
            "narrateur|Mila glisse un bras.",
            "narrateur|Elle glisse l'autre bras.",
            "enfant-f|Il est chaud.",
            "papa|Oui.",
            "maman|On peut aller à la flaque ?",
            "enfant-f|Oui.",
            "narrateur|La casserole chante encore, tout bas.",
        ],
    )
    sons["CHK_T0000_P0000"] = "casserole,orange"

    s["CHK_T0001_P0000"] = vet(
        N3,
        [
            "papa|On passe où, avant la flaque ?",
            "narrateur|La cuisine.",
            "narrateur|Le jardin.",
            "narrateur|Ou la chambre.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("la cuisine", "le jardin", "la chambre")

    for i, loc in L1_032.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_032[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_032[i]
        extras[f"{p}_Q0001"] = qf(
            "manteau",
            "manteau | le manteau | son manteau | le manteau vert",
            "Le manteau vert. Mila a pris quoi ?",
        )
        s[f"{p}_C0001"] = C_032[i]
        s[f"{p}_T0002_P0000"] = vet(
            N3,
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
            s[p2] = PLAY_032[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N3,
                [
                    "papa|C'est quel moment, pour sortir ?",
                    "narrateur|Le matin.",
                    "narrateur|Après la sieste.",
                    "narrateur|Ou le soir.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le matin", "après la sieste", "le soir")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_032(i, j, k)
                s[f"{p3}_F0001"] = fin_032(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-033  N1  Nino  AUT.AFF.003  gouttière du kiosque, manteau bleu
# ≠ maison/zinc/bottes (ROU), ≠ palier (014), ≠ cour/seau Aniss (008)
# ---------------------------------------------------------------------------

L1_033 = {
    1: {"lab": "le bac à sable", "ou": "près du bac", "son": "enfants_parc"},
    2: {"lab": "le toboggan", "ou": "près du toboggan", "son": "enfants_parc"},
    3: {"lab": "les balançoires", "ou": "près des balançoires", "son": "enfants_parc"},
}
L2_033 = {
    1: {"lab": "le ballon", "obj": "le ballon rouge"},
    2: {"lab": "le seau", "obj": "le seau jaune"},
    3: {"lab": "le doudou", "obj": "le doudou gris"},
}
L3_033 = {
    1: {"lab": "le filet", "ou": "vers le filet"},
    2: {"lab": "la fontaine", "ou": "vers la fontaine"},
    3: {"lab": "la grille", "ou": "vers la grille"},
}

ARRIVE_033 = {
    1: vet(
        N1,
        [
            "narrateur|Nino s'agenouille près du bac.",
            "narrateur|Le sable est frais, un peu humide.",
            "narrateur|Il coule entre ses doigts.",
            "narrateur|Chh.",
            "enfant-m|Le sable est doux, maman.",
            "maman|Oui.",
            "maman|Il est doux et frais.",
            "papa|Le seau reste près de toi ?",
            "enfant-m|Oui, tout près.",
            "maman|Le manteau est sur le banc.",
            "narrateur|Nino verse le sable.",
            "narrateur|Ça sent la terre propre.",
            "narrateur|Un grain reste sous son ongle.",
            "enfant-m|Il est froid.",
            "papa|Tes joues sont déjà roses.",
            "narrateur|Un grain de sable brille sur son genou.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Nino va vers le toboggan.",
            "narrateur|Le métal est un peu froid.",
            "narrateur|Une marche est lisse.",
            "narrateur|Une goutte y brille encore.",
            "enfant-m|Il est froid, papa.",
            "maman|Oui.",
            "maman|Le soleil va le tiédir.",
            "papa|On reste près des marches.",
            "narrateur|Le manteau bleu reste sur le banc.",
            "narrateur|Le seau jaune n'est pas loin.",
            "enfant-m|Je glisse !",
            "papa|J'attends en bas.",
            "narrateur|Nino glisse.",
            "narrateur|Le plastique fait un petit frou.",
            "narrateur|Une goutte a séché sur le métal.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Nino va vers les balançoires.",
            "narrateur|Une chaîne fait tic, tout doux.",
            "narrateur|Le siège rouge est encore humide.",
            "enfant-m|Ça bouge tout seul.",
            "maman|C'est le vent, Nino.",
            "maman|Je pousse tout doux.",
            "papa|Le manteau reste au banc ?",
            "enfant-m|Oui, je le vois.",
            "narrateur|Nino avance, puis revient.",
            "narrateur|Le vent lui touche le nez.",
            "maman|Le seau est sous le banc.",
            "narrateur|Nino pose les pieds par terre.",
            "enfant-m|Je vois le ciel.",
            "papa|Tu t'es arrêté tout seul.",
            "narrateur|La chaîne ne fait plus tic.",
        ],
    ),
}

Q_033 = {
    1: vet(
        N1,
        [
            "narrateur|Le seau est resté au bac.",
            "papa|Nino, tu prends quoi ?",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Le manteau est resté au banc.",
            "maman|Nino, tu prends quoi ?",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Le doudou est resté sous le banc.",
            "papa|Nino, tu prends quoi ?",
        ],
    ),
}

C_033 = {
    1: vet(
        N1,
        [
            "narrateur|Nino revient vers le bac.",
            "narrateur|Il prend le seau jaune.",
            "enfant-m|Il était là.",
            "papa|Oui.",
            "papa|Il t'attendait.",
            "maman|Le manteau est encore sur le banc.",
            "narrateur|Un grain de sable reste sur sa joue.",
            "papa|Merci, Nino.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Nino revient vers le banc.",
            "narrateur|Il prend le manteau bleu.",
            "enfant-m|Il fait toc.",
            "maman|Oui.",
            "maman|Il était encore là.",
            "papa|Le seau est près des bottes.",
            "narrateur|Une goutte glisse de la manche.",
            "maman|Merci, Nino.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Nino se penche sous le banc.",
            "narrateur|Il sort le doudou gris.",
            "enfant-m|Il sent le vent.",
            "papa|Oui.",
            "papa|Il t'attendait.",
            "maman|Le seau est encore là.",
            "narrateur|L'oreille du doudou est un peu humide.",
            "papa|Merci, Nino.",
        ],
    ),
}

PLAY_033 = {
    (1, 1): vet(
        N1,
        [
            "narrateur|Près du bac, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-m|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Nino pose les deux mains dessus.",
            "narrateur|Le ballon fait un petit bruit.",
            "maman|Le seau reste à ta droite.",
            "papa|Le manteau reste sur le banc.",
            "enfant-m|Je les vois.",
            "narrateur|Le ballon prend un peu de sable.",
        ],
    ),
    (1, 2): vet(
        N1,
        [
            "narrateur|Près du bac, le seau jaune est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-m|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Nino tient l'anse des deux mains.",
            "narrateur|Le seau racle un peu, toc.",
            "maman|Tu as déjà le seau.",
            "papa|Il restera le manteau.",
            "enfant-m|Je le vois, au banc.",
            "narrateur|Du sable reste au fond du seau.",
        ],
    ),
    (1, 3): vet(
        N1,
        [
            "narrateur|Près du bac, le doudou gris est là.",
            "narrateur|Le tissu est doux, un peu humide.",
            "enfant-m|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Nino le serre contre lui.",
            "narrateur|Le doudou sent encore le savon.",
            "maman|Le seau attend encore.",
            "papa|Le manteau aussi.",
            "enfant-m|Ils sont au banc.",
            "narrateur|Le doudou a un grain sur l'oreille.",
        ],
    ),
    (2, 1): vet(
        N1,
        [
            "narrateur|Près du toboggan, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-m|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Nino pose les deux mains dessus.",
            "narrateur|Le ballon s'appuie contre une marche.",
            "maman|Tes affaires restent près de papa.",
            "papa|Je vois le seau.",
            "papa|Je vois le manteau.",
            "enfant-m|Moi aussi, des yeux.",
        ],
    ),
    (2, 2): vet(
        N1,
        [
            "narrateur|Près du toboggan, le seau jaune est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-m|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Nino tient l'anse des deux mains.",
            "narrateur|Le seau attend au pied du toboggan.",
            "maman|Tu as déjà le seau.",
            "papa|Il restera le manteau.",
            "enfant-m|Au banc.",
            "narrateur|L'anse du seau a une goutte.",
        ],
    ),
    (2, 3): vet(
        N1,
        [
            "narrateur|Près du toboggan, le doudou gris est là.",
            "narrateur|Le tissu est doux, un peu humide.",
            "enfant-m|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Nino le serre contre lui.",
            "narrateur|Le doudou regarde le métal froid.",
            "maman|Le seau attend encore.",
            "papa|Le manteau aussi.",
            "enfant-m|Ils sont au banc.",
            "narrateur|Le doudou a touché la marche lisse.",
        ],
    ),
    (3, 1): vet(
        N1,
        [
            "narrateur|Près des balançoires, le ballon rouge attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-m|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Nino pose les deux mains dessus.",
            "narrateur|Le ballon rebondit une fois, tout mou.",
            "maman|Le seau est sous le banc.",
            "papa|Le manteau reste au banc.",
            "enfant-m|Je les vois.",
            "narrateur|Un brin d'herbe colle au cuir.",
        ],
    ),
    (3, 2): vet(
        N1,
        [
            "narrateur|Près des balançoires, le seau jaune est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-m|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Nino tient l'anse des deux mains.",
            "narrateur|Le seau tapote l'herbe, toc.",
            "maman|Tu as déjà le seau.",
            "papa|Il restera le manteau.",
            "enfant-m|Au banc.",
            "narrateur|L'anse du seau est froide, encore.",
        ],
    ),
    (3, 3): vet(
        N1,
        [
            "narrateur|Près des balançoires, le doudou gris est là.",
            "narrateur|Le tissu est doux, un peu humide.",
            "enfant-m|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Nino le serre contre lui.",
            "narrateur|Le doudou a senti le vent.",
            "maman|Le seau est sous le banc.",
            "papa|Le manteau aussi.",
            "enfant-m|Ils sont là.",
            "narrateur|L'oreille du doudou est un peu froide.",
        ],
    ),
}

FIND_033 = {
    1: vet(
        N1,
        [
            "narrateur|Le filet est accroché au banc.",
            "narrateur|Les mailles sont un peu rudes.",
            "narrateur|Ça sent le pain, tout près.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|La fontaine fait un tout petit bruit.",
            "narrateur|L'eau brille, toute claire.",
            "narrateur|La pierre est froide sous la main.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|La grille du parc est verte.",
            "narrateur|La barre est un peu froide.",
            "narrateur|Une feuille y est coincée.",
        ],
    ),
}

# j==2 : Nino a déjà le seau
TAKE_033 = {
    True: vet(
        N1,
        [
            "papa|C'est l'heure de partir.",
            "narrateur|Nino tient déjà le seau jaune.",
            "maman|Cherche le manteau, Nino.",
            "narrateur|Nino va vers le banc.",
            "narrateur|Le manteau bleu sèche encore.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai les deux.",
            "papa|Oui.",
            "papa|Le seau et le manteau.",
        ],
    ),
    False: vet(
        N1,
        [
            "papa|C'est l'heure de partir.",
            "maman|Cherche le seau, Nino.",
            "narrateur|Nino va vers le banc.",
            "narrateur|Le seau jaune est dessous.",
            "narrateur|Il le prend.",
            "papa|Cherche le manteau.",
            "narrateur|Le manteau bleu est dessus.",
            "narrateur|Il le prend.",
            "enfant-m|Le seau.",
            "enfant-m|Le manteau.",
            "maman|Oui.",
        ],
    ),
}

CLOSE_033 = {
    1: vet(
        N1,
        [
            "maman|On met les affaires dans le filet.",
            "papa|Le seau.",
            "papa|Le manteau.",
            "papa|Dans le filet.",
            "enfant-m|Dans le filet.",
            "narrateur|Le filet devient un peu lourd.",
        ],
    ),
    2: vet(
        N1,
        [
            "maman|D'abord les affaires.",
            "papa|Ensuite on rince les mains.",
            "papa|Les affaires sont avec nous.",
            "enfant-m|J'ai le seau.",
            "enfant-m|J'ai le manteau.",
            "narrateur|Une goutte tombe sur la pierre.",
        ],
    ),
    3: vet(
        N1,
        [
            "maman|Avant la grille, les affaires.",
            "papa|On a le seau.",
            "papa|On a le manteau.",
            "papa|On peut passer.",
            "enfant-m|J'ai tout.",
            "narrateur|La grille fait clic, tout doux.",
        ],
    ),
}

IMG_033 = {
    (1, 1, 1): "Une miette de pain reste dans une maille.",
    (1, 1, 2): "Une goutte d'eau roule sur le ballon.",
    (1, 1, 3): "Le ballon frotte la grille, tout doux.",
    (1, 2, 1): "Du sable reste au fond du seau.",
    (1, 2, 2): "Le seau sonne un peu sous l'eau.",
    (1, 2, 3): "Le seau tapote la barre verte.",
    (1, 3, 1): "Le doudou a un grain de sable.",
    (1, 3, 2): "Le doudou sent un peu l'eau.",
    (1, 3, 3): "Le doudou frotte la feuille coincée.",
    (2, 1, 1): "Le ballon a une trace de métal froid.",
    (2, 1, 2): "Une goutte du toboggan rejoint la fontaine.",
    (2, 1, 3): "Le ballon rebondit une fois, près de la grille.",
    (2, 2, 1): "L'anse du seau a une goutte du toboggan.",
    (2, 2, 2): "Le seau se rince un tout petit peu.",
    (2, 2, 3): "Le seau jaune brille près de la grille.",
    (2, 3, 1): "Le doudou a touché la marche lisse.",
    (2, 3, 2): "Une goutte du toboggan sèche sur le doudou.",
    (2, 3, 3): "Le doudou passe sous la barre verte.",
    (3, 1, 1): "Le filet frotte encore la chaîne froide.",
    (3, 1, 2): "Une goutte de la chaîne rejoint la pierre.",
    (3, 1, 3): "Le ballon frotte la feuille coincée.",
    (3, 2, 1): "Du sable du seau reste dans le filet.",
    (3, 2, 2): "L'anse du seau sonne sous l'eau.",
    (3, 2, 3): "Le seau tapote la barre verte, tout doux.",
    (3, 3, 1): "L'oreille du doudou a pris le filet.",
    (3, 3, 2): "Le doudou sent un peu l'eau froide.",
    (3, 3, 3): "Le doudou passe sous la barre verte.",
}

HOLD_033 = {
    1: "Le ballon reste rond, tout calme.",
    2: "Le seau reste dans ses mains.",
    3: "Le doudou reste contre sa joue.",
}


def body_033(i: int, j: int, k: int) -> list[str]:
    loc = L1_033[i]
    lines = list(FIND_033[k])
    lines.append(f"narrateur|Nino est encore {loc['ou']}.")
    lines.append(f"narrateur|{HOLD_033[j]}")
    lines.extend(TAKE_033[j == 2])
    lines.extend(CLOSE_033[k])
    lines.append("enfant-m|Merci, papa.")
    lines.append("enfant-m|Merci, maman.")
    lines.append(f"narrateur|{IMG_033[(i, j, k)]}")
    return vet(N1, lines)


def fin_033(i: int, j: int, k: int) -> list[str]:
    loc = L1_033[i]
    obj = L2_033[j]
    dest = L3_033[k]
    return vet(
        N1,
        [
            f"narrateur|{IMG_033[(i, j, k)]}",
            f"narrateur|Nino a joué {loc['ou']}.",
            f"narrateur|Il avait {obj['lab']}.",
            f"narrateur|Puis {dest['lab']}.",
            "enfant-m|J'ai le seau.",
            "enfant-m|J'ai le manteau.",
            "maman|On rentre.",
            "papa|Le kiosque s'est tu.",
            "narrateur|Une dernière goutte tombe du zinc.",
            "narrateur|Ploc.",
        ],
    )


def build_033() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N1,
        [
            "narrateur|Le zinc du kiosque fait ploc.",
            "narrateur|Une flaque ronde brille dessous.",
            "narrateur|Une feuille y tourne, toute lente.",
            "narrateur|Le banc du parc est encore mouillé.",
            "narrateur|Un manteau bleu sèche dessus.",
            "narrateur|Les boutons sont ronds, un peu froids.",
            "narrateur|Un seau jaune est sous le banc.",
            "narrateur|Il sent le sable mouillé.",
            "narrateur|Une affiche du kiosque claque.",
            "narrateur|Papa essuie le bois avec sa manche.",
            "narrateur|Maman ouvre un sac de pain.",
            "narrateur|Ça sent le pain, tout chaud.",
            "maman|Tu as vu la flaque, Nino ?",
            "enfant-m|Oui.",
            "enfant-m|Elle brille.",
            "papa|Le banc est encore humide.",
            "narrateur|En ce moment, Nino touche le seau.",
            "narrateur|L'anse est froide, un peu rêche.",
            "enfant-m|Je veux les gouttes !",
            "maman|D'accord.",
            "maman|On joue un peu.",
            "papa|Le seau reste avec toi ?",
            "enfant-m|Oui, papa.",
            "narrateur|Une goutte tombe encore.",
            "narrateur|Ploc.",
        ],
    )
    sons["CHK_T0000_P0000"] = "enfants_parc,gouttiere"

    s["CHK_T0001_P0000"] = vet(
        N1,
        [
            "narrateur|Au parc, Nino peut commencer à trois endroits.",
            "papa|Le bac à sable, le toboggan, ou les balançoires ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("le bac à sable", "le toboggan", "les balançoires")

    for i, loc in L1_033.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_033[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_033[i]
        extras[f"{p}_Q0001"] = qf(
            "seau",
            "seau | le seau | manteau | le manteau | doudou | le doudou | ses affaires",
            "Le seau jaune. Nino prend quoi ?",
        )
        s[f"{p}_C0001"] = C_033[i]
        s[f"{p}_T0002_P0000"] = vet(
            N1,
            [
                f"narrateur|{loc['ou'].capitalize()}, Nino prend un objet.",
                "papa|Le ballon, le seau, ou le doudou ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_033[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N1,
                [
                    f"narrateur|Nino a {L2_033[j]['lab']}, {loc['ou']}.",
                    "maman|Avant de partir, on passe où ?",
                    "papa|Le filet, la fontaine, ou la grille ?",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le filet", "la fontaine", "la grille")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_033(i, j, k)
                s[f"{p3}_F0001"] = fin_033(i, j, k)
    return s, sons, extras


def main() -> None:
    s32, n32, e32 = build_032()
    write_tree(
        "TREE-AUT-032",
        "Mila veut le bateau d'orange dans la flaque. "
        "L'air froid la ramène au manteau vert, près de la casserole. "
        "Une manche est à l'envers. En rentrant, le manteau goutte : "
        "elle le raccroche au crochet bas.",
        "Le manteau vert de Mila près de la casserole",
        "Mila, papa, maman",
        "cuisine, casserole, orange, crochet bas près de la porte",
        s32,
        n32,
        e32,
    )
    relecture(
        "TREE-AUT-032",
        "Le manteau vert de Mila près de la casserole",
        "Mila veut le bateau d'orange dans la flaque. Casserole, farine, "
        "crochet bas, manteau vert. Cuisine / jardin / chambre, puis "
        "cubes / livre / dînette, puis matin / sieste / soir. "
        "Elle prend le manteau (froid, manche à l'envers). "
        "En rentrant, il goutte : elle le raccroche.",
        "Adam→Mila (D16). N3. AUT.AFF.002 implicite. "
        "Monde ≠ TREE-AUT-016 (laine, radiateur, bottes). "
        "Monde ≠ TREE-COL-001 (pommes, train). "
        "Pas « on va apprendre ». Fin sensorielle.",
    )

    s33, n33, e33 = build_033()
    write_tree(
        "TREE-AUT-033",
        "Nino veut les gouttes du kiosque dans le seau jaune. "
        "Le zinc du kiosque fait ploc. Le manteau bleu sèche sur le banc. "
        "Au moment de partir, il reprend le seau et le manteau. "
        "Filet, fontaine ou grille : la suite change.",
        "La gouttière du kiosque et le manteau bleu",
        "Nino, papa, maman",
        "parc, kiosque à pain, zinc, banc mouillé",
        s33,
        n33,
        e33,
    )
    relecture(
        "TREE-AUT-033",
        "La gouttière du kiosque et le manteau bleu",
        "Nino veut les gouttes du kiosque. Zinc, affiche, pain, banc, "
        "manteau bleu, seau jaune. Bac / toboggan / balançoires, puis "
        "ballon / seau / doudou, puis filet / fontaine / grille. "
        "Il reprend seau et manteau pour une raison vécue.",
        "Nino déjà D16. N1 ≤10. AUT.AFF.003 implicite. "
        "Gouttière du kiosque ≠ maison/zinc/bottes, ≠ palier 014, "
        "≠ cour Aniss 008. T3 = filet/fontaine/grille (plus Tom/Léa/Sami). "
        "Fin = ploc du zinc, pas « L'histoire est finie ».",
    )


if __name__ == "__main__":
    main()
