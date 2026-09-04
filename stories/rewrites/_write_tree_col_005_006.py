#!/usr/bin/env python3
"""TREE-COL-005 / TREE-COL-006 — récit implicite, graphe 86 nœuds, D16."""
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


N2 = LIMITS["N2"]


# ---------------------------------------------------------------------------
# TREE-COL-005  N2  Aniss  COL.POL.001
# Gouttière + stand de zinc. Politesse vécue (jamais « les trois mots »).
# ≠ TREE-COL-001 (pommes, train) ≠ TREE-COL-012 (bâche, fraises)
# ≠ TREE-COL-025 (gouttière Nina, main) ≠ TREE-COL-035 (store goutteux)
# ---------------------------------------------------------------------------

L1_005 = {
    1: {"lab": "la cuisine", "de": "de la cuisine", "ou": "dans la cuisine", "son": "soupe"},
    2: {"lab": "le jardin", "de": "du jardin", "ou": "dans le jardin", "son": "pluie"},
    3: {"lab": "la chambre", "de": "de la chambre", "ou": "dans la chambre", "son": "rideau"},
}
L2_005 = {
    1: {"lab": "le voisin", "ou": "près du banc du voisin", "qui": "le voisin"},
    2: {"lab": "la maîtresse", "ou": "sous l'auvent de l'école", "qui": "la maîtresse"},
    3: {"lab": "la boulangère", "ou": "au stand de pain", "qui": "la boulangère"},
}
L3_005 = {
    1: {"lab": "le pain", "un": "un pain", "le": "le pain"},
    2: {"lab": "une pomme", "un": "une pomme", "le": "la pomme"},
    3: {"lab": "un livre", "un": "un livre", "le": "le livre"},
}

ARRIVE_005 = {
    1: vet(
        N2,
        [
            "narrateur|Aniss pousse la porte de la cuisine.",
            "narrateur|La soupe fume encore, tout doux.",
            "narrateur|Une miette dorée attend près de l'assiette.",
            "enfant-m|Bonjour, maman.",
            "maman|Bonjour, Aniss.",
            "maman|Tu as vu la vapeur sur la vitre ?",
            "enfant-m|Oui.",
            "enfant-m|Elle fait un nuage.",
            "papa|Le panier est près du four.",
            "enfant-m|Je le prends pour le stand.",
            "narrateur|Il glisse l'anse dans sa main.",
            "narrateur|L'osier pique un peu les doigts.",
            "maman|Il est encore tiède, ce bois.",
            "enfant-m|Ça sent le thym.",
            "papa|On sort après, d'accord ?",
            "enfant-m|Vers le stand.",
            "narrateur|Une goutte glisse sur la vitre, tout lentement.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Aniss passe par le jardin mouillé.",
            "narrateur|La gouttière tombe dans l'herbe, plic.",
            "narrateur|Une feuille collée tremble sur le seau.",
            "enfant-m|Le panier, s'il te plaît.",
            "papa|Le voilà.",
            "narrateur|Papa tend l'osier, encore froid.",
            "enfant-m|Merci.",
            "maman|Tes chaussettes, dans les bottes ?",
            "enfant-m|Oui.",
            "enfant-m|Elles sont au sec.",
            "narrateur|L'air sent la terre, tout bas.",
            "narrateur|L'oiseau gris est encore sur la haie.",
            "papa|Le stand est au coin, sous le zinc.",
            "enfant-m|J'y vais avec le panier.",
            "maman|On reste près de toi.",
            "narrateur|Une goutte rebondit sur l'anse.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Aniss entre un moment dans la chambre.",
            "narrateur|Le rideau jaune bouge.",
            "narrateur|Le lit est encore chaud.",
            "papa|Ton manteau, Aniss.",
            "narrateur|Papa le tient à sa hauteur.",
            "enfant-m|Merci, papa.",
            "narrateur|Il glisse un bras, puis l'autre.",
            "narrateur|Le tissu sent encore la pluie.",
            "maman|Les boutons sont un peu froids.",
            "enfant-m|Ils sont ronds.",
            "enfant-m|Je veux le stand.",
            "papa|Le panier t'attend près de la porte.",
            "narrateur|Aniss revient vers le couloir.",
            "narrateur|Une rivière reste sur la vitre de la chambre.",
            "maman|On y va ?",
            "enfant-m|Oui, maman.",
        ],
    ),
}

Q_005 = {
    1: vet(
        N2,
        [
            "narrateur|Aniss arrive près de maman.",
            "papa|Il dit quoi ?",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Aniss veut le panier, dans le jardin.",
            "maman|Que dit-il ?",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Papa tend le manteau.",
            "maman|Aniss dit quoi ?",
        ],
    ),
}

C_005 = {
    1: vet(
        N2,
        [
            "narrateur|Aniss a dit bonjour.",
            "narrateur|Le panier est dans ses mains.",
            "papa|Merci, Aniss.",
            "enfant-m|On va au stand.",
            "maman|Oui.",
            "papa|Qui tient l'étal, ce matin ?",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Aniss a dit s'il te plaît.",
            "narrateur|Le panier est à sa main.",
            "maman|Merci, Aniss.",
            "enfant-m|On va au stand.",
            "papa|Oui.",
            "maman|Qui tient l'étal, sous le zinc ?",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Aniss a dit merci.",
            "narrateur|Le manteau est sur lui.",
            "papa|Merci, Aniss.",
            "enfant-m|On va au stand.",
            "maman|Oui.",
            "papa|Qui tient l'étal, près de la gouttière ?",
        ],
    ),
}

PLAY_005 = {
    (1, 1): vet(
        N2,
        [
            "narrateur|Ils sortent de la cuisine, le panier à la main.",
            "narrateur|Le banc du voisin est sous la haie.",
            "narrateur|La gouttière tombe dans une caisse, plic.",
            "narrateur|Le bois de la caisse est sombre, tout mouillé.",
            "enfant-m|Bonjour.",
            "papa|Le voisin range des pots de thym.",
            "maman|L'étal est petit, tout près.",
            "enfant-m|Ça sent la terre.",
            "narrateur|Une abeille passe, tout bas, le long de la haie.",
        ],
    ),
    (1, 2): vet(
        N2,
        [
            "narrateur|Ils quittent la cuisine, le panier à la main.",
            "narrateur|L'auvent de l'école goutte sur les dalles.",
            "narrateur|Une nappe de papier tremble.",
            "enfant-m|Bonjour.",
            "maitresse|Bonjour, Aniss.",
            "papa|La table est encore un peu froide.",
            "maman|Le zinc chante, tout doux.",
            "enfant-m|Ça sent la craie, un peu.",
            "narrateur|Une flaque ronde garde un morceau de ciel.",
        ],
    ),
    (1, 3): vet(
        N2,
        [
            "narrateur|Ils quittent la cuisine, le panier à la main.",
            "narrateur|Le stand de pain a un petit zinc.",
            "narrateur|Une goutte tombe sur le pavé, ploc.",
            "enfant-m|Bonjour.",
            "papa|La boulangère a de la farine au tablier.",
            "maman|Ça sent le beurre, tout chaud.",
            "enfant-m|Le pain fume un peu.",
            "narrateur|Le papier des sachets fait un bruit doux.",
            "narrateur|L'air du four touche les joues.",
        ],
    ),
    (2, 1): vet(
        N2,
        [
            "narrateur|Ils traversent le jardin, bottes dans l'herbe.",
            "narrateur|Le banc du voisin luit, encore mouillé.",
            "narrateur|La gouttière de la haie fait plic, plic.",
            "enfant-m|Bonjour.",
            "papa|Le voisin essuie le bois avec un torchon.",
            "maman|Les pots de thym sont alignés.",
            "enfant-m|Ça sent vert.",
            "narrateur|Une feuille reste collée à la caisse.",
            "narrateur|L'anse du panier est froide, un peu rêche.",
        ],
    ),
    (2, 2): vet(
        N2,
        [
            "narrateur|Ils quittent le jardin par le portail mouillé.",
            "narrateur|L'auvent de l'école goutte encore.",
            "narrateur|La nappe de papier a une tache d'eau.",
            "enfant-m|Bonjour.",
            "maitresse|Bonjour.",
            "papa|On s'abrite un peu, ici.",
            "maman|Le zinc chante au-dessus.",
            "enfant-m|J'entends les gouttes.",
            "narrateur|Une craie blanche repose près d'une pomme.",
        ],
    ),
    (2, 3): vet(
        N2,
        [
            "narrateur|Ils quittent le jardin, l'herbe aux bottes.",
            "narrateur|Le stand de pain fume sous le zinc.",
            "narrateur|Une goutte rebondit sur le pavé.",
            "enfant-m|Bonjour.",
            "papa|La boulangère tourne un sachet.",
            "maman|Ça sent le four, tout fort.",
            "enfant-m|J'ai les joues tièdes.",
            "narrateur|De la farine blanche reste sur le bois.",
            "narrateur|Le panier attend, tout calme.",
        ],
    ),
    (3, 1): vet(
        N2,
        [
            "narrateur|Aniss a le manteau, et le panier.",
            "narrateur|Ils rejoignent le banc du voisin.",
            "narrateur|Une goutte tombe du zinc sur la caisse.",
            "enfant-m|Bonjour.",
            "papa|Le voisin range encore un pot.",
            "maman|Le bois est froid, sous la haie.",
            "enfant-m|Mon manteau est chaud.",
            "narrateur|Le col frotte le thym, tout doux.",
            "narrateur|Une abeille passe, tout près du banc.",
        ],
    ),
    (3, 2): vet(
        N2,
        [
            "narrateur|Aniss a le manteau, et le panier.",
            "narrateur|Ils s'abritent sous l'auvent de l'école.",
            "narrateur|Le zinc goutte sur les dalles, plic.",
            "enfant-m|Bonjour.",
            "maitresse|Bonjour, Aniss.",
            "papa|La nappe tremble un peu.",
            "maman|Tes boutons sont froids, encore ?",
            "enfant-m|Un peu.",
            "narrateur|Une craie a roulé près du pied de table.",
        ],
    ),
    (3, 3): vet(
        N2,
        [
            "narrateur|Aniss a le manteau, et le panier.",
            "narrateur|Ils arrivent au stand de pain.",
            "narrateur|Le petit zinc chante au-dessus.",
            "enfant-m|Bonjour.",
            "papa|La boulangère a les mains farinées.",
            "maman|Ça sent le beurre, tout chaud.",
            "enfant-m|Le manteau prend l'odeur du four.",
            "narrateur|Un sachet attend, encore vide.",
            "narrateur|Une goutte sèche sur le pavé.",
        ],
    ),
}

ASK_005 = {
    1: vet(
        N2,
        [
            "enfant-m|Le pain, s'il te plaît.",
            "narrateur|Le sachet craque, un peu gras.",
            "narrateur|Le pain est encore tiède.",
            "enfant-m|Merci.",
        ],
    ),
    2: vet(
        N2,
        [
            "enfant-m|La pomme, s'il te plaît.",
            "narrateur|La peau est lisse, un peu mouillée.",
            "narrateur|Elle sent le sucre, tout doux.",
            "enfant-m|Merci.",
        ],
    ),
    3: vet(
        N2,
        [
            "enfant-m|Le livre, s'il te plaît.",
            "narrateur|La couverture est lisse, un peu froide.",
            "narrateur|Une page sent encore le bois.",
            "enfant-m|Merci.",
        ],
    ),
}

GIVE_005 = {
    1: "narrateur|Le voisin pose ça sur le banc.",
    2: "maitresse|Le voilà.",
    3: "narrateur|La boulangère glisse ça dans les mains.",
}

IMG_005 = {
    (1, 1, 1): "Une miette de pain reste sur le bois mouillé.",
    (1, 1, 2): "Une feuille colle à la pomme, tout plat.",
    (1, 1, 3): "Une goutte sèche sur la couverture.",
    (1, 2, 1): "La farine du pain brille sous l'auvent.",
    (1, 2, 2): "La pomme roule un peu sur la nappe.",
    (1, 2, 3): "Le livre sent encore la craie, tout bas.",
    (1, 3, 1): "Le sachet de pain craque, tout chaud.",
    (1, 3, 2): "La pomme a un point d'eau, tout rond.",
    (1, 3, 3): "Une page du livre sent le beurre.",
    (2, 1, 1): "De la terre reste au fond du panier.",
    (2, 1, 2): "L'herbe a laissé une odeur sur la pomme.",
    (2, 1, 3): "Une goutte d'herbe sèche sur le livre.",
    (2, 2, 1): "Le pain a une croûte brillante, sous l'auvent.",
    (2, 2, 2): "La pomme reflète un bout de ciel.",
    (2, 2, 3): "Le livre a une page un peu fraîche.",
    (2, 3, 1): "Une miette tombe près de la flaque.",
    (2, 3, 2): "La pomme sent le jardin, tout doux.",
    (2, 3, 3): "Le livre reste au sec, contre le manteau.",
    (3, 1, 1): "Le pain chauffe encore la poche du manteau.",
    (3, 1, 2): "La pomme frotte un bouton de bois.",
    (3, 1, 3): "Le livre glisse contre la manche, tout calme.",
    (3, 2, 1): "Une croûte reste dans la main, toute tiède.",
    (3, 2, 2): "La pomme a pris l'odeur du manteau.",
    (3, 2, 3): "Le livre touche l'écharpe, tout doux.",
    (3, 3, 1): "Le sachet fait encore un petit bruit.",
    (3, 3, 2): "La pomme brille près du four, tout bas.",
    (3, 3, 3): "Une page se recourbe, près du zinc.",
}

FIN_IMG_005 = {
    (1, 1, 1): "La gouttière fait un dernier tic, tout loin.",
    (1, 1, 2): "Une feuille de haie sèche sur le banc.",
    (1, 1, 3): "Le thym sent encore, tout bas.",
    (1, 2, 1): "L'auvent s'est tu, enfin.",
    (1, 2, 2): "La nappe de papier ne tremble plus.",
    (1, 2, 3): "Une craie reste au sec, sous l'auvent.",
    (1, 3, 1): "Le four chante encore, tout doux.",
    (1, 3, 2): "Une miette dorée dort sur le zinc.",
    (1, 3, 3): "Le pavé a séché, près du stand.",
    (2, 1, 1): "L'herbe ne goutte plus sur l'anse.",
    (2, 1, 2): "Le seau du jardin est calme.",
    (2, 1, 3): "L'oiseau gris a quitté la haie.",
    (2, 2, 1): "Une dalle brille encore, sous l'auvent.",
    (2, 2, 2): "Le portail ne claque plus.",
    (2, 2, 3): "La flaque a perdu son bout de ciel.",
    (2, 3, 1): "Une odeur de four reste aux bottes.",
    (2, 3, 2): "Le zinc du stand ne chante plus.",
    (2, 3, 3): "Le jardin sent encore la terre.",
    (3, 1, 1): "Le bouton de bois est tiède, maintenant.",
    (3, 1, 2): "Le rideau jaune ne bouge plus.",
    (3, 1, 3): "Le col du manteau sèche, tout calme.",
    (3, 2, 1): "Une goutte sèche sur un bouton.",
    (3, 2, 2): "L'auvent garde une petite tache d'eau.",
    (3, 2, 3): "Le manteau sent encore la craie.",
    (3, 3, 1): "Le sachet reste chaud, contre le tissu.",
    (3, 3, 2): "Une farine blanche dort sur le zinc.",
    (3, 3, 3): "Le petit zinc s'est tu.",
}


def body_005(i: int, j: int, k: int) -> list[str]:
    loc = L1_005[i]
    who = L2_005[j]
    obj = L3_005[k]
    ask = ASK_005[k]
    lines = [
        f"narrateur|Aniss est {who['ou']}.",
        f"narrateur|Il vient {loc['de']}.",
        ask[0],
        GIVE_005[j],
        *ask[1:],
        f"papa|Tu as {obj['le']} ?",
        "enfant-m|Oui.",
        "maman|Il tient, dans le panier.",
        "enfant-m|Il est à moi.",
        f"narrateur|{IMG_005[(i, j, k)]}",
    ]
    return vet(N2, lines)


def fin_005(i: int, j: int, k: int) -> list[str]:
    loc = L1_005[i]
    who = L2_005[j]
    obj = L3_005[k]
    return vet(
        N2,
        [
            f"narrateur|{IMG_005[(i, j, k)]}",
            f"narrateur|Aniss est passé {loc['ou']}.",
            f"narrateur|Il a vu {who['qui']}.",
            f"narrateur|Il tient {obj['le']}.",
            "enfant-m|Merci, papa.",
            "enfant-m|Merci, maman.",
            "papa|On rentre.",
            "maman|La soupe attend encore.",
            f"narrateur|{FIN_IMG_005[(i, j, k)]}",
            "narrateur|Une dernière goutte tombe du zinc.",
        ],
    )


def build_005() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N2,
        [
            "narrateur|La gouttière fait un petit tic, tic, tic.",
            "narrateur|Des rivières de pluie restent sur la vitre.",
            "narrateur|La vitre est tiède du côté de la maison.",
            "narrateur|Dehors, l'air sent l'herbe mouillée.",
            "narrateur|Les chaussures de papa sèchent près de la porte.",
            "narrateur|Une chaussette rouge pend encore.",
            "narrateur|Dans la cuisine, la soupe fume tout doux.",
            "narrateur|Ça sent la carotte et le thym.",
            "narrateur|Un oiseau gris secoue ses plumes sur la haie.",
            "maman|Tu entends la gouttière, Aniss ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Tic, tic.",
            "papa|Les chaussures sont encore mouillées.",
            "papa|On les laisse là.",
            "narrateur|En ce moment, Aniss trace une rivière sur la vitre.",
            "narrateur|Son doigt fait un chemin clair.",
            "enfant-m|Je vois l'oiseau.",
            "enfant-m|Je veux un pain au stand.",
            "maman|Le stand est ouvert, après la pluie.",
            "papa|On y va, quand tu es prêt ?",
            "enfant-m|Oui, papa.",
            "narrateur|Une goutte tombe encore, tout près.",
        ],
    )
    sons["CHK_T0000_P0000"] = "gouttiere,soupe"

    s["CHK_T0001_P0000"] = vet(
        N2,
        [
            "narrateur|Avant le stand, la maison a trois passages.",
            "papa|La cuisine, le jardin, ou la chambre ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("la cuisine", "le jardin", "la chambre")

    ans = {
        1: ("bonjour", "bonjour | s'il te plaît | merci", "Il dit bonjour. Aniss dit quoi ?"),
        2: (
            "s'il te plaît",
            "s'il te plaît | s'il te plait | merci | bonjour",
            "Il dit s'il te plaît. Que dit Aniss ?",
        ),
        3: ("merci", "merci | bonjour | s'il te plaît", "Il dit merci. Aniss dit quoi ?"),
    }

    for i, loc in L1_005.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_005[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_005[i]
        extras[f"{p}_Q0001"] = qf(*ans[i])
        s[f"{p}_C0001"] = C_005[i]
        s[f"{p}_T0002_P0000"] = vet(
            N2,
            [
                f"narrateur|{loc['ou'].capitalize()}, le panier est prêt.",
                "papa|Le voisin, la maîtresse, ou la boulangère ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le voisin", "la maîtresse", "la boulangère")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_005[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N2,
                [
                    f"narrateur|Aniss est {L2_005[j]['ou']}.",
                    "maman|Le pain, une pomme, ou un livre ?",
                    "papa|Tu choisis.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le pain", "une pomme", "un livre")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_005(i, j, k)
                s[f"{p3}_F0001"] = fin_005(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-COL-006  N2  Mila  COL.ECO.002
# Rayon du vestiaire. Tour de parole vécu (jamais « il faut attendre »).
# T3 Léa/Tom/Sami → crayon / coussin / grelot.
# ≠ TREE-COL-004 (cloche, crayon) ≠ TREE-COL-016 (craie, oiseau)
# ≠ TREE-COL-025 (gouttière, main Nina) ≠ TREE-COL-028 (cartable jaune)
# ---------------------------------------------------------------------------

L1_006 = {
    1: {"lab": "le tapis", "ou": "sur le tapis", "son": "tapis"},
    2: {"lab": "la table", "ou": "à la table", "son": "table"},
    3: {"lab": "la fenêtre", "ou": "près de la fenêtre", "son": "fenetre"},
}
L2_006 = {
    1: {"lab": "l'histoire", "quoi": "l'histoire", "dit": "Le loup est dans le bois."},
    2: {"lab": "la chanson", "quoi": "la chanson", "dit": "La chanson est douce."},
    3: {"lab": "le dessin", "quoi": "le dessin", "dit": "Le soleil est rond."},
}
L3_006 = {
    1: {"lab": "le crayon", "un": "le crayon jaune", "son": "crayon"},
    2: {"lab": "le coussin", "un": "le coussin bleu", "son": "coussin"},
    3: {"lab": "le grelot", "un": "le grelot", "son": "grelot"},
}

ARRIVE_006 = {
    1: vet(
        N2,
        [
            "narrateur|Le tapis de la classe est gris, un peu rêche.",
            "narrateur|Mila s'assoit.",
            "narrateur|Ses genoux font un bruit de laine.",
            "narrateur|Un rayon pose un carré jaune sur le tissu.",
            "enfant-f|La poussière dansait, au vestiaire.",
            "narrateur|Les mots tombent trop tôt.",
            "narrateur|La maîtresse parle encore, tout doux.",
            "narrateur|Personne ne se tourne.",
            "narrateur|Mila ferme la bouche.",
            "narrateur|Sa main se lève, tout droit.",
            "narrateur|Elle attend.",
            "maitresse|Mila, c'est toi.",
            "enfant-f|La poussière dansait.",
            "papa|Je t'entends, maintenant.",
            "maman|Merci, Mila.",
            "narrateur|Le carré de soleil a bougé, tout lent.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|La table de bois est lisse, un peu froide.",
            "narrateur|Mila pose les mains à plat.",
            "narrateur|Une miette de craie dort dans une rainure.",
            "enfant-f|Ma poire est dans le sachet.",
            "narrateur|Papa parle encore à maman, tout bas.",
            "narrateur|Les mots de Mila se perdent.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Sa main se lève, près du bois.",
            "narrateur|Elle attend.",
            "papa|Je t'écoute, Mila.",
            "enfant-f|La poire attend, dans le papier.",
            "maman|Je t'entends.",
            "maman|Merci.",
            "narrateur|Le sachet fait un tout petit bruit.",
            "narrateur|La rainure de craie reste blanche.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Mila s'approche de la fenêtre.",
            "narrateur|La flaque ronde garde encore un bout de ciel.",
            "narrateur|Le verre est froid sous ses doigts.",
            "enfant-f|Le ciel est dans l'eau.",
            "narrateur|La maîtresse parle vers le tableau.",
            "narrateur|La voix de Mila tombe dans l'air.",
            "narrateur|Personne ne se tourne.",
            "narrateur|Elle pose le doigt sur la vitre, puis s'arrête.",
            "narrateur|Sa main se lève.",
            "narrateur|Elle attend.",
            "maitresse|Mila, je t'écoute.",
            "enfant-f|Le ciel est dans l'eau.",
            "papa|Oui.",
            "maman|On t'a entendue.",
            "narrateur|Un nuage passe dans la flaque, tout lent.",
        ],
    ),
}

Q_006 = {
    1: vet(
        N2,
        [
            "narrateur|Mila est sur le tapis.",
            "maman|Que fait-elle avant de parler ?",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Mila est à la table.",
            "papa|Que fait-elle avant de parler ?",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Mila est près de la fenêtre.",
            "maman|Que fait-elle avant de parler ?",
        ],
    ),
}

C_006 = {
    1: vet(
        N2,
        [
            "narrateur|Elle a attendu.",
            "narrateur|Puis on l'a entendue.",
            "papa|Merci, Mila.",
            "enfant-f|Le tapis est chaud ici.",
            "maman|On continue, tout doux ?",
            "narrateur|Le carré jaune a glissé un peu.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Elle a attendu.",
            "narrateur|Puis papa l'a entendue.",
            "maman|Merci, Mila.",
            "enfant-f|La table est lisse.",
            "papa|On continue ?",
            "narrateur|La miette de craie reste dans la rainure.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Elle a attendu.",
            "narrateur|Puis la maîtresse l'a entendue.",
            "papa|Merci, Mila.",
            "enfant-f|La flaque brille encore.",
            "maman|On continue ?",
            "narrateur|Le verre de la fenêtre est calme.",
        ],
    ),
}

PLAY_006 = {
    (1, 1): vet(
        N2,
        [
            "narrateur|Le tapis gris garde encore un carré de soleil.",
            "narrateur|La maîtresse ouvre l'histoire.",
            "narrateur|Le loup marche dans le bois, sur l'image.",
            "narrateur|Les arbres sont verts, un peu sombres.",
            "maitresse|Qui veut dire un mot ?",
            "narrateur|Mila lève la main.",
            "narrateur|Elle attend.",
            "narrateur|Un autre mot est dit, tout bas.",
            "narrateur|Sa main reste en l'air.",
            "maitresse|Mila, à toi.",
            "enfant-f|Le loup est dans le bois.",
            "papa|Je t'ai entendue.",
            "maman|Merci.",
            "narrateur|La page du loup reste ouverte, un moment.",
        ],
    ),
    (1, 2): vet(
        N2,
        [
            "narrateur|Le tapis gris garde encore un carré de soleil.",
            "narrateur|Une chanson commence, tout bas.",
            "narrateur|Les mains tapent un rythme, tout doux.",
            "enfant-f|Moi aussi.",
            "narrateur|Sa voix se perd dans le chant.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Sa main se lève.",
            "narrateur|Elle attend.",
            "maitresse|Mila, c'est ton tour.",
            "enfant-f|La chanson est douce.",
            "papa|On t'entend.",
            "maman|Merci.",
            "narrateur|Le rythme s'arrête un peu, puis reprend.",
        ],
    ),
    (1, 3): vet(
        N2,
        [
            "narrateur|Le tapis gris garde encore un carré de soleil.",
            "narrateur|Un grand papier blanc attend au milieu.",
            "narrateur|Un soleil à moitié rond y dort déjà.",
            "enfant-f|Il est jaune.",
            "narrateur|La maîtresse parle encore du dessin.",
            "narrateur|Mila s'arrête.",
            "narrateur|Sa main se lève.",
            "narrateur|Elle attend.",
            "maitresse|Mila, à toi.",
            "enfant-f|Le soleil est rond.",
            "papa|Je t'écoute.",
            "maman|Merci.",
            "narrateur|Le papier fait un petit bruit, tout sec.",
        ],
    ),
    (2, 1): vet(
        N2,
        [
            "narrateur|À la table, un livre s'ouvre.",
            "narrateur|Le loup marche dans le bois, sur l'image.",
            "narrateur|Les arbres sont verts, un peu sombres.",
            "maitresse|Un mot, pour le loup ?",
            "narrateur|Mila a les mots tout prêts.",
            "narrateur|Elle les garde encore.",
            "narrateur|Sa main se lève, près du bois.",
            "narrateur|Elle attend.",
            "maitresse|Mila.",
            "enfant-f|Le loup est dans le bois.",
            "papa|Je t'ai entendue.",
            "maman|Merci.",
            "narrateur|Une page se recourbe, tout doux.",
        ],
    ),
    (2, 2): vet(
        N2,
        [
            "narrateur|À la table, une chanson commence.",
            "narrateur|Les mains tapent le bois, tout léger.",
            "narrateur|Ça fait toc, toc, tout bas.",
            "enfant-f|Moi.",
            "narrateur|Personne ne se tourne encore.",
            "narrateur|Mila lève la main.",
            "narrateur|Elle attend.",
            "maitresse|Mila, c'est toi.",
            "enfant-f|La chanson est douce.",
            "papa|On t'entend.",
            "maman|Merci.",
            "narrateur|Le toc toc s'arrête un moment.",
            "narrateur|La rainure de craie reste blanche.",
        ],
    ),
    (2, 3): vet(
        N2,
        [
            "narrateur|À la table, un papier blanc attend.",
            "narrateur|Un soleil à moitié rond y dort déjà.",
            "narrateur|La craie a laissé un trait, tout pâle.",
            "enfant-f|Je veux le finir.",
            "narrateur|Papa parle encore, tout bas.",
            "narrateur|Mila lève la main.",
            "narrateur|Elle attend.",
            "papa|Je t'écoute.",
            "enfant-f|Le soleil est rond.",
            "maman|Merci.",
            "narrateur|Le papier craque sous le doigt.",
            "narrateur|La miette de craie ne bouge plus.",
        ],
    ),
    (3, 1): vet(
        N2,
        [
            "narrateur|Près de la fenêtre, le livre s'ouvre.",
            "narrateur|Le loup marche dans le bois, sur l'image.",
            "narrateur|Un reflet de flaque passe sur la page.",
            "maitresse|Un mot, Mila ?",
            "narrateur|Elle a envie de parler tout de suite.",
            "narrateur|La maîtresse n'a pas fini.",
            "narrateur|Mila lève la main.",
            "narrateur|Elle attend.",
            "maitresse|Maintenant, Mila.",
            "enfant-f|Le loup est dans le bois.",
            "papa|Je t'ai entendue.",
            "maman|Merci.",
            "narrateur|Le ciel de la flaque a bougé.",
        ],
    ),
    (3, 2): vet(
        N2,
        [
            "narrateur|Près de la fenêtre, une chanson commence.",
            "narrateur|Elle est douce, comme la pluie d'hier.",
            "narrateur|Les vitres tremblent un peu.",
            "enfant-f|Moi aussi.",
            "narrateur|Sa voix se mêle à la chanson.",
            "narrateur|Mila s'arrête.",
            "narrateur|Sa main se lève.",
            "narrateur|Elle attend.",
            "maitresse|Mila, à toi.",
            "enfant-f|La chanson est douce.",
            "papa|On t'entend.",
            "maman|Merci.",
            "narrateur|Un oiseau passe dans la flaque, tout petit.",
        ],
    ),
    (3, 3): vet(
        N2,
        [
            "narrateur|Près de la fenêtre, un papier attend.",
            "narrateur|Un soleil à moitié rond y dort déjà.",
            "narrateur|Le verre jette un rond clair sur le blanc.",
            "enfant-f|Il est jaune.",
            "narrateur|La maîtresse parle encore du dessin.",
            "narrateur|Mila lève la main.",
            "narrateur|Elle attend.",
            "maitresse|Mila.",
            "enfant-f|Le soleil est rond.",
            "papa|Je t'écoute.",
            "maman|Merci.",
            "narrateur|Le rond clair a glissé sur le papier.",
        ],
    ),
}

OBJ_006 = {
    1: vet(
        N2,
        [
            "narrateur|Le crayon jaune sent un peu le bois.",
            "narrateur|La mine est douce, déjà un peu ronde.",
            "enfant-f|Le crayon.",
            "narrateur|Mila ne le prend pas encore.",
            "narrateur|Sa main reste en l'air.",
            "maitresse|Mila, tu peux le prendre.",
            "enfant-f|Merci.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le coussin bleu est mou, un peu lourd.",
            "narrateur|Il sent la classe, et un peu le savon.",
            "enfant-f|Le coussin.",
            "narrateur|Elle ne s'assoit pas encore dessus.",
            "narrateur|Sa main reste en l'air.",
            "maitresse|Mila, c'est toi.",
            "enfant-f|Merci.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Le grelot est petit, un peu froid.",
            "narrateur|Il fait un tintement, tout court.",
            "enfant-f|Le grelot.",
            "narrateur|Elle le laisse encore sur le tissu.",
            "narrateur|Sa main reste en l'air.",
            "maitresse|Mila, à toi.",
            "enfant-f|Merci.",
        ],
    ),
}

IMG_006 = {
    (1, 1, 1): "Un petit trait jaune reste près du loup.",
    (1, 1, 2): "Le coussin s'enfonce un peu, sous elle.",
    (1, 1, 3): "Le grelot s'est tu, sur le tapis.",
    (1, 2, 1): "Un trait jaune suit encore le rythme.",
    (1, 2, 2): "Le coussin garde le toc toc, tout mou.",
    (1, 2, 3): "Le grelot a fait ding, tout doux.",
    (1, 3, 1): "Un soleil jaune est fini, sur le papier.",
    (1, 3, 2): "Le coussin touche le bord du dessin.",
    (1, 3, 3): "Le grelot brille près du soleil rond.",
    (2, 1, 1): "Un trait jaune court sur la page du loup.",
    (2, 1, 2): "Le coussin est posé contre le livre.",
    (2, 1, 3): "Le grelot repose près de la rainure.",
    (2, 2, 1): "Un trait jaune tapote le bois, tout léger.",
    (2, 2, 2): "Le coussin s'assoit comme une note, tout mou.",
    (2, 2, 3): "Le grelot a répondu au toc toc.",
    (2, 3, 1): "Un trait jaune ferme le soleil, enfin.",
    (2, 3, 2): "Le coussin cache un coin du papier.",
    (2, 3, 3): "Le grelot fait ding, près du soleil.",
    (3, 1, 1): "Un trait jaune prend un peu de ciel.",
    (3, 1, 2): "Le coussin est chaud, contre la vitre.",
    (3, 1, 3): "Le grelot reflète un bout de flaque.",
    (3, 2, 1): "Un trait jaune tremble comme la chanson.",
    (3, 2, 2): "Le coussin écoute encore, tout mou.",
    (3, 2, 3): "Le grelot chante une fois, puis s'arrête.",
    (3, 3, 1): "Un trait jaune suit le rond de la vitre.",
    (3, 3, 2): "Le coussin a un carré de soleil.",
    (3, 3, 3): "Le grelot brille dans le rond clair.",
}

FIN_IMG_006 = {
    (1, 1, 1): "Le rayon du vestiaire s'est un peu déplacé.",
    (1, 1, 2): "Le tapis redevient calme, sous ses genoux.",
    (1, 1, 3): "Un crochet gris brille, tout loin.",
    (1, 2, 1): "La poussière ne danse plus, au vestiaire.",
    (1, 2, 2): "L'écharpe rouge attend encore au crochet.",
    (1, 2, 3): "Le cartable bleu ne penche plus.",
    (1, 3, 1): "Le papier blanc s'est tu.",
    (1, 3, 2): "Un carré de soleil dort sur le tapis.",
    (1, 3, 3): "La classe sent encore le savon.",
    (2, 1, 1): "La rainure de craie reste blanche.",
    (2, 1, 2): "La table de bois est calme.",
    (2, 1, 3): "Le sachet de la poire fait un bruit.",
    (2, 2, 1): "Les mains ne tapent plus le bois.",
    (2, 2, 2): "Une miette de craie ne bouge plus.",
    (2, 2, 3): "Le toc toc s'est perdu.",
    (2, 3, 1): "Le soleil du papier est fini.",
    (2, 3, 2): "La table garde un peu de chaleur.",
    (2, 3, 3): "Le bois sent encore le savon.",
    (3, 1, 1): "La flaque a perdu son bout de ciel.",
    (3, 1, 2): "Le verre de la fenêtre est froid.",
    (3, 1, 3): "Un nuage a quitté l'eau.",
    (3, 2, 1): "La vitre ne tremble plus.",
    (3, 2, 2): "Un oiseau a quitté la flaque.",
    (3, 2, 3): "La chanson s'est tue, près du verre.",
    (3, 3, 1): "Le rond clair a glissé, puis s'est arrêté.",
    (3, 3, 2): "La flaque est grise, maintenant.",
    (3, 3, 3): "Le vestiaire est calme, derrière la porte.",
}


def body_006(i: int, j: int, k: int) -> list[str]:
    loc = L1_006[i]
    act = L2_006[j]
    lines = list(OBJ_006[k])
    lines.append(f"narrateur|Mila est encore {loc['ou']}.")
    lines.append(f"enfant-f|{act['dit']}")
    lines.append("papa|Je t'ai entendue.")
    lines.append("maman|Merci, Mila.")
    lines.append(f"narrateur|{IMG_006[(i, j, k)]}")
    return vet(N2, lines)


def fin_006(i: int, j: int, k: int) -> list[str]:
    loc = L1_006[i]
    act = L2_006[j]
    obj = L3_006[k]
    return vet(
        N2,
        [
            f"narrateur|{IMG_006[(i, j, k)]}",
            f"narrateur|Mila était {loc['ou']}.",
            f"narrateur|C'était {act['quoi']}.",
            f"narrateur|Elle a pris {obj['lab']}.",
            "enfant-f|On m'a entendue.",
            "maman|Oui.",
            "papa|On rentre au vestiaire.",
            "narrateur|Le rayon passe encore entre deux manteaux.",
            f"narrateur|{FIN_IMG_006[(i, j, k)]}",
            "narrateur|Un peu de poussière reste, comme de la neige.",
        ],
    )


def build_006() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N2,
        [
            "narrateur|Un rayon passe entre deux manteaux, au vestiaire.",
            "narrateur|Il tient un peu de poussière, comme de la neige.",
            "narrateur|Les crochets sont froids, tout gris.",
            "narrateur|Un cartable bleu penche, un peu trop.",
            "narrateur|Dedans, une poire attend dans un sachet.",
            "narrateur|Le sachet fait un bruit de papier.",
            "narrateur|Dehors, une flaque ronde garde un morceau de ciel.",
            "narrateur|La cloche n'a pas encore sonné.",
            "narrateur|Maman plie l'écharpe rouge, tout doux.",
            "narrateur|Papa pose le cartable contre le mur.",
            "maman|Tu as vu la poussière dans la lumière, Mila ?",
            "enfant-f|Oui.",
            "enfant-f|Elle danse.",
            "papa|La poire est pour plus tard.",
            "narrateur|En ce moment, Mila accroche son manteau.",
            "narrateur|Le crochet fait un petit clic.",
            "enfant-f|Je veux le dire.",
            "enfant-f|La poussière danse.",
            "narrateur|Papa parle encore à maman, tout bas.",
            "narrateur|Les mots de Mila tombent trop tôt.",
            "narrateur|Personne ne se tourne.",
            "narrateur|Mila ferme la bouche.",
            "narrateur|Sa main se lève, tout doux.",
            "narrateur|Elle attend.",
            "papa|Je t'écoute, maintenant.",
            "enfant-f|Elle danse, la poussière.",
            "maman|Je t'entends, Mila.",
            "papa|Merci.",
            "narrateur|La classe sent encore le savon des lavabos.",
        ],
    )
    sons["CHK_T0000_P0000"] = "vestiaire,papier"

    s["CHK_T0001_P0000"] = vet(
        N2,
        [
            "narrateur|La classe a trois places, pour s'asseoir.",
            "papa|Le tapis, la table, ou la fenêtre ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("le tapis", "la table", "la fenêtre")

    for i, loc in L1_006.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_006[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_006[i]
        extras[f"{p}_Q0001"] = qf(
            "attendre",
            "attendre | elle attend | la main | lever la main",
            "Elle lève la main. Ensuite ?",
        )
        s[f"{p}_C0001"] = C_006[i]
        s[f"{p}_T0002_P0000"] = vet(
            N2,
            [
                f"narrateur|Mila est {loc['ou']}.",
                "papa|L'histoire, la chanson, ou le dessin ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("l'histoire", "la chanson", "le dessin")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_006[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N2,
                [
                    f"narrateur|C'est encore {L2_006[j]['quoi']}.",
                    "maman|Le crayon, le coussin, ou le grelot ?",
                    "papa|Tu choisis.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le crayon", "le coussin", "le grelot")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_006(i, j, k)
                sons[p3] = L3_006[k]["son"]
                s[f"{p3}_F0001"] = fin_006(i, j, k)
    return s, sons, extras


def main() -> None:
    s5, n5, e5 = build_005()
    write_tree(
        "TREE-COL-005",
        "Aniss veut un pain chaud au stand sous la gouttière. "
        "Il dit bonjour, s'il te plaît, merci, pour le demander. "
        "Cuisine, jardin ou chambre, puis le voisin, la maîtresse "
        "ou la boulangère, puis le pain, la pomme ou le livre.",
        "La gouttière et les trois mots d'Aniss",
        "Aniss, papa, maman",
        "maison sous la pluie, gouttière, stand de zinc",
        s5,
        n5,
        e5,
    )
    relecture(
        "TREE-COL-005",
        "La gouttière et les trois mots d'Aniss",
        "Aniss veut un pain au stand sous le zinc. Gouttière tic-tic, "
        "rivières sur la vitre, chaussette rouge, soupe thym, oiseau gris. "
        "Cuisine / jardin / chambre, puis voisin / maîtresse / boulangère, "
        "puis pain / pomme / livre. Bonjour, s'il te plaît, merci vécus "
        "à l'étal, jamais « on va apprendre les trois mots ».",
        "Jules→Aniss (D16). N2. COL.POL.001 implicite. "
        "Monde ≠ TREE-COL-001 (pommes, train), ≠ TREE-COL-012 (bâche), "
        "≠ TREE-COL-025 (gouttière Nina). Fin sensorielle, goutte du zinc.",
    )

    s6, n6, e6 = build_006()
    write_tree(
        "TREE-COL-006",
        "Mila veut dire que la poussière danse dans le rayon du vestiaire. "
        "Elle parle trop tôt. Personne ne se tourne. Elle lève la main, "
        "elle attend, puis on l'entend. Tapis, table ou fenêtre, puis "
        "histoire, chanson ou dessin, puis crayon, coussin ou grelot.",
        "Le rayon du vestiaire de Mila",
        "Mila, papa, maman",
        "vestiaire de l'école, rayon de poussière, flaque",
        s6,
        n6,
        e6,
    )
    relecture(
        "TREE-COL-006",
        "Le rayon du vestiaire de Mila",
        "Mila veut dire que la poussière danse. Crochets froids, cartable "
        "bleu, poire, flaque-ciel, écharpe rouge. Elle parle trop tôt, "
        "attend, puis on l'entend. Tapis / table / fenêtre, puis "
        "histoire / chanson / dessin, puis crayon / coussin / grelot.",
        "Iris→Mila (D16). N2. COL.ECO.002 implicite. "
        "T3 Léa/Tom/Sami → crayon/coussin/grelot. "
        "Pas « il faut attendre ». Pas « puis parler » en refrain. "
        "Monde ≠ TREE-COL-004, ≠ TREE-COL-016, ≠ TREE-COL-028. "
        "Fin = poussière comme de la neige.",
    )


if __name__ == "__main__":
    main()
