#!/usr/bin/env python3
"""TREE-AUT-022 / TREE-AUT-023 — récit implicite, graphe 86, D16, mondes uniques."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    BAD_NAMES,
    FORBIDDEN,
    LIMITS,
    OPENING_BAD,
    ROLES,
    ROOT,
    from_script,
    relecture,
    words,
)


def check_story(sid: str, age: str, chunks: list[dict]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if name in low:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [
        ln
        for ln in joined.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation vécue")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in OPENING_BAD:
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    longp: list[str] = []
    for c in chunks:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: text ≠ script")
        if c.get("text_ssml") != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: ssml ≠ text")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                raise SystemExit(f"{sid} ligne sans | : {ln}")
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                raise SystemExit(f"{sid} rôle {role}")
            n = words(phrase)
            if n > lim:
                longp.append(f"{c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    if longp:
        raise SystemExit(f"{sid} phrases trop longues:\n" + "\n".join(longp[:40]))
    for c in chunks:
        if c.get("kind") != "passage_fin":
            continue
        last_lines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        if not last_lines:
            raise SystemExit(f"{sid} {c['chunk_id']}: fin sans narrateur")
        last = last_lines[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} fin mécanique: {last}")
    print(f"OK {sid} {nwords} mots  1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}")


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict[str, list[str]],
    sons: dict[str, str],
    qfields: dict[str, dict],
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={sorted(extra)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        text, script = from_script(scripts[cid])
        nc = deepcopy(c)
        nc["text"] = text
        nc["script"] = script
        nc["text_ssml"] = text
        nc["sons"] = sons.get(cid, c.get("sons") or "") or ""
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            nc["length_scale_piper"] = 1.28
            nc["rate_label"] = "slow"
        elif src.get("age_band") == "N1":
            nc["length_scale_piper"] = 1.22
            nc["rate_label"] = "slow"
        else:
            nc["length_scale_piper"] = 1.22
            nc["rate_label"] = "medium"
        if cid in qfields:
            nc.update(qfields[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check_story(sid, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# TREE-AUT-022  N3  Aniss  AUT.AFF.002  pomme dans l'herbe
# Monde unique ≠ TREE-AUT-016 (radiateur, flaque).
# ---------------------------------------------------------------------------

L1_022 = {
    1: {"lab": "la cuisine", "ici": "dans la cuisine", "son": "soupe"},
    2: {"lab": "le jardin", "ici": "dans le jardin", "son": "oiseau"},
    3: {"lab": "la chambre", "ici": "dans la chambre", "son": "rideau"},
}
L2_022 = {
    1: {"lab": "les cubes", "obj": "les cubes", "un": "un cube"},
    2: {"lab": "le livre", "obj": "le livre", "un": "le livre"},
    3: {"lab": "la dînette", "obj": "la dînette", "un": "une tasse"},
}
L3_022 = {
    1: {"lab": "le matin", "quand": "le matin"},
    2: {"lab": "après la sieste", "quand": "après la sieste"},
    3: {"lab": "le soir", "quand": "le soir"},
}

L1_BODY_022 = {
    1: [
        "narrateur|Aniss pousse la porte de la cuisine.",
        "narrateur|Les carreaux sont tièdes sous les chaussons.",
        "narrateur|La casserole chante un tout petit pschitt.",
        "narrateur|Ça sent la soupe et la pomme, ensemble.",
        "narrateur|La vitre de la cuisine est embuée.",
        "narrateur|Le manteau de laine fume un peu.",
        "papa|La soupe est chaude, hein ?",
        "enfant-m|Oui, papa.",
        "enfant-m|Mon manteau aussi.",
        "maman|Une feuille de laurier tombe.",
        "narrateur|Elle glisse près de l'évier.",
        "narrateur|Aniss la ramasse, tout doux.",
        "papa|Tu la mets dans la poche ?",
        "enfant-m|Oui.",
        "narrateur|La poche de laine est rêche.",
        "narrateur|La feuille sent le bois.",
        "maman|La pomme nous attend, sous l'arbre ?",
        "enfant-m|Par la porte de derrière.",
        "papa|Le manteau est déjà sur toi.",
        "narrateur|Aniss touche le bouton, encore frais.",
    ],
    2: [
        "narrateur|Aniss va vers le jardin.",
        "narrateur|L'herbe est mouillée, toute brillante.",
        "narrateur|L'air est frais sur le nez.",
        "narrateur|Le manteau sent la laine mouillée.",
        "papa|Tes chevilles sont au chaud ?",
        "enfant-m|Oui.",
        "enfant-m|Le manteau les couvre.",
        "maman|La pomme est encore sous le pommier.",
        "narrateur|Une abeille passe, puis s'en va.",
        "narrateur|Une goutte tombe d'une feuille.",
        "narrateur|Elle fait un tout petit bruit.",
        "narrateur|Aniss serre le col contre sa joue.",
        "papa|Tu n'as pas froid ?",
        "enfant-m|Non.",
        "enfant-m|Le manteau est chaud.",
        "maman|L'herbe mouille le bas, un peu.",
        "narrateur|Le bas de laine devient sombre.",
        "papa|On le séchera, au crochet.",
        "narrateur|Aniss avance vers la pomme rouge.",
    ],
    3: [
        "narrateur|Aniss va vers la chambre.",
        "narrateur|La couverture est pliée, toute douce.",
        "narrateur|Le rideau vert bouge un peu.",
        "narrateur|Le manteau frotte le bois de la porte.",
        "maman|Le pommier se voit, par la fenêtre.",
        "enfant-m|La pomme brille, dans l'herbe.",
        "enfant-m|Je la prends après.",
        "papa|Elle attend, oui.",
        "narrateur|Aniss pose un genou sur le tapis.",
        "narrateur|L'oreiller sent encore le savon.",
        "narrateur|Un panier vide attend près du lit.",
        "maman|Le panier pourra porter la pomme.",
        "enfant-m|Il est léger.",
        "papa|On sort après, d'accord ?",
        "enfant-m|Avec le panier.",
        "narrateur|Aniss marche tout doux sur le tapis.",
        "narrateur|Le manteau fait un bruit de laine.",
    ],
}

Q_022 = {
    1: [
        "narrateur|Aniss n'a plus froid, dans la cuisine.",
        "papa|Il a mis quoi, pour l'herbe ?",
    ],
    2: [
        "narrateur|Dehors, Aniss n'a pas froid.",
        "maman|Il a mis quoi, avant ?",
    ],
    3: [
        "narrateur|Le manteau frotte encore la porte.",
        "papa|Aniss a mis quoi ?",
    ],
}

C_022 = {
    1: [
        "narrateur|Oui.",
        "narrateur|Le manteau de laine est sur lui.",
        "papa|Merci, Aniss.",
        "maman|La feuille est dans la poche.",
        "enfant-m|Elle sent le bois.",
        "papa|On emporte un jeu, pour la pomme ?",
        "narrateur|La casserole chante tout bas.",
    ],
    2: [
        "narrateur|Oui.",
        "narrateur|Le manteau de laine est sur lui.",
        "maman|Merci.",
        "maman|Tu n'as pas froid.",
        "enfant-m|Il est chaud.",
        "papa|On emporte un jeu, sous le pommier ?",
        "narrateur|Une goutte brille encore sur l'herbe.",
    ],
    3: [
        "narrateur|Oui.",
        "narrateur|Le manteau est sur Aniss.",
        "papa|Le panier est près de la porte.",
        "enfant-m|Pour la pomme.",
        "maman|On emporte un jeu aussi ?",
        "narrateur|Le rideau vert se tait.",
        "narrateur|La chambre est calme.",
    ],
}

L2_BODY_022 = {
    1: [
        "narrateur|Aniss a choisi les cubes.",
        "narrateur|Ils sont en bois, un peu lourds.",
        "narrateur|Ils cliquent dans la boîte.",
        "papa|On fait un petit socle, pour la pomme ?",
        "enfant-m|Oui.",
        "enfant-m|Un socle de cubes.",
        "maman|Le manteau garde tes bras au chaud.",
        "narrateur|Un cube sent le pin.",
        "narrateur|Aniss le serre contre la laine.",
        "papa|On les emporte.",
        "narrateur|La boîte tape doucement sa hanche.",
    ],
    2: [
        "narrateur|Aniss a choisi le livre.",
        "narrateur|La couverture est un peu froissée.",
        "narrateur|Une page montre un arbre rouge.",
        "maman|Comme le pommier, hein ?",
        "enfant-m|Oui.",
        "enfant-m|Et la vraie pomme.",
        "papa|On le met sous le manteau.",
        "narrateur|Le livre glisse contre la laine.",
        "narrateur|Il reste au sec.",
        "maman|On le regardera près de l'arbre.",
        "narrateur|Une page se recourbe, tout doux.",
    ],
    3: [
        "narrateur|Aniss a choisi la dînette.",
        "narrateur|Une petite tasse sonne, tout creux.",
        "narrateur|Une assiette miniature est tiède.",
        "papa|On sert la pomme ?",
        "enfant-m|Oui.",
        "enfant-m|Un goûter de fruit.",
        "maman|L'assiette tient dans la poche.",
        "narrateur|Aniss la glisse à côté du bouton.",
        "narrateur|La laine la tient.",
        "papa|On y va, alors.",
        "narrateur|La petite cuillère reste dans l'autre main.",
    ],
}

L2_EXTRA_022 = {
    (1, 1): "Un cube attrape un reflet de soupe.",
    (1, 2): "Une miette reste au bord de la page.",
    (1, 3): "La petite casserole est près du vrai bol.",
    (2, 1): "L'herbe tache un cube, tout vert.",
    (2, 2): "Une vraie feuille sert de marque-page.",
    (2, 3): "Une goutte perle au bord de l'assiette.",
    (3, 1): "Un cube tapote le parquet, tout doux.",
    (3, 2): "Le rideau vert colore la page.",
    (3, 3): "La petite tasse est près de la fenêtre.",
}

MOMENT_022 = {
    1: [
        "narrateur|C'est le matin.",
        "narrateur|La lumière est pâle, tout douce.",
        "narrateur|Un oiseau chante une fois.",
    ],
    2: [
        "narrateur|C'est après la sieste.",
        "narrateur|Les joues d'Aniss sont chaudes.",
        "narrateur|La maison est encore calme.",
    ],
    3: [
        "narrateur|C'est le soir.",
        "narrateur|La lampe fait un rond jaune.",
        "narrateur|Le pommier est plus sombre.",
    ],
}

L3_SORTIE_022 = {
    1: [
        "papa|La pomme est claire, ce matin.",
        "narrateur|Ils passent sous le pommier.",
        "narrateur|L'air touche le nez d'Aniss.",
        "enfant-m|Elle brille.",
        "maman|Tes mains, dans les manches ?",
        "enfant-m|Elles sont au chaud.",
    ],
    2: [
        "papa|La pomme a un peu séché, au soleil.",
        "narrateur|Ils passent sous le pommier.",
        "narrateur|Le soleil est jaune et doux.",
        "enfant-m|Elle est tiède.",
        "maman|Le manteau est encore utile.",
        "enfant-m|Oui, un peu.",
    ],
    3: [
        "papa|La pomme est sombre, ce soir.",
        "narrateur|Ils passent sous le pommier.",
        "narrateur|La vitre de la maison est bleue.",
        "enfant-m|Je vois les lumières.",
        "maman|Le manteau te tient chaud.",
        "enfant-m|Oui, maman.",
    ],
}

L3_RETOUR_022 = [
    "papa|On rentre avec la pomme.",
    "narrateur|Aniss la prend à deux mains.",
    "narrateur|Elle est lisse, un peu froide.",
    "narrateur|Ils rentrent.",
    "narrateur|Le manteau de laine est un peu lourd.",
    "narrateur|Aniss le retire.",
    "narrateur|Il le raccroche au petit crochet.",
    "maman|Il goutte, tout doux.",
    "enfant-m|Il sèche, là.",
    "papa|Oui.",
    "papa|Le crochet est à ta hauteur.",
]

IMG_022 = {
    (1, 1, 1): "Une miette de pomme sèche sur un cube.",
    (1, 1, 2): "Le cube sent encore la casserole.",
    (1, 1, 3): "L'ombre d'un cube danse sur le carrelage.",
    (1, 2, 1): "Une page sent le laurier, tout doux.",
    (1, 2, 2): "Le livre est tiède, près de la vitre.",
    (1, 2, 3): "La lampe dore le bord d'une page.",
    (1, 3, 1): "Une petite tasse a une goutte de soupe.",
    (1, 3, 2): "La dînette est chaude, comme la casserole.",
    (1, 3, 3): "La petite cuillère brille sous la lampe.",
    (2, 1, 1): "Un cube a une goutte d'herbe.",
    (2, 1, 2): "Le cube sèche au soleil, tout vert.",
    (2, 1, 3): "Un cube garde une goutte, toute ronde.",
    (2, 2, 1): "Une vraie feuille marque la page.",
    (2, 2, 2): "Le livre sent l'herbe mouillée.",
    (2, 2, 3): "Un oiseau se tait près du livre.",
    (2, 3, 1): "Une petite assiette a de la rosée.",
    (2, 3, 2): "La dînette est tiède, au soleil.",
    (2, 3, 3): "Loin de la dînette, une goutte tombe.",
    (3, 1, 1): "Un rayon pose sur la tour de cubes.",
    (3, 1, 2): "Un cube est contre l'oreiller, tout calme.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Le rideau vert colore la page.",
    (3, 2, 2): "Le livre est ouvert sur la couverture.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FIN_022 = {
    (1, 1, 1): "Le bol de pomme reste au milieu de la table.",
    (1, 1, 2): "La casserole fait un tout petit pschitt.",
    (1, 1, 3): "La lampe dore la pomme, dans le bol.",
    (1, 2, 1): "Un oiseau chante encore, tout loin.",
    (1, 2, 2): "La page se recourbe, près du bol.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "La soupe sent encore, tout bas.",
    (1, 3, 3): "Le bouton du manteau brille, au crochet.",
    (2, 1, 1): "Une feuille reste collée à un cube.",
    (2, 1, 2): "L'herbe colle encore à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau.",
    (2, 2, 1): "Une feuille vraie reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "La pomme ne brille plus, dehors.",
    (2, 3, 1): "La petite assiette a encore de l'herbe.",
    (2, 3, 2): "Une abeille s'en va, tout loin.",
    (2, 3, 3): "Le col de laine sèche, au crochet.",
    (3, 1, 1): "Le panier repose près d'un cube.",
    (3, 1, 2): "L'oreiller sent encore le savon.",
    (3, 1, 3): "Le rideau vert ne bouge plus.",
    (3, 2, 1): "Le panier sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près du panier.",
    (3, 3, 2): "Le tapis de la chambre est calme.",
    (3, 3, 3): "La pomme attend, dans le panier vide.",
}


def build_022() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    qf: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|Le pommier du jardin penche un peu.",
        "narrateur|Son ombre est ronde, sur l'herbe.",
        "narrateur|Une abeille fait un tour, puis s'en va.",
        "narrateur|Ça sent le fruit mûr, tout fort.",
        "narrateur|Par la porte ouverte, ça sent la soupe aussi.",
        "narrateur|Sur le banc de bois, un manteau de laine attend.",
        "narrateur|Le col a une goutte de rosée.",
        "narrateur|Dans l'herbe, une pomme rouge brille.",
        "narrateur|Une feuille reste collée dessus.",
        "papa|Aniss, tu as vu la pomme ?",
        "enfant-m|Oui, papa.",
        "enfant-m|Je la veux.",
        "maman|Elle est dans l'herbe froide.",
        "narrateur|En ce moment, Aniss court vers le banc.",
        "narrateur|Le manteau glisse et tombe dans l'herbe.",
        "enfant-m|Oh.",
        "enfant-m|Il est mouillé.",
        "papa|On le secoue, tout doux.",
        "narrateur|Aniss secoue le manteau.",
        "narrateur|Des gouttes tombent.",
        "narrateur|Une manche reste un peu tordue.",
        "maman|On tourne la manche ?",
        "narrateur|Aniss tourne le tissu rêche.",
        "narrateur|Il glisse un bras, puis l'autre.",
        "enfant-m|Il est frais, papa.",
        "papa|Oui.",
        "papa|Il te tiendra chaud, sous le pommier.",
        "maman|On va chercher la pomme ?",
        "enfant-m|Oui.",
        "narrateur|Le col touche sa joue, tout doux.",
    ]
    sons["CHK_T0000_P0000"] = "pommier,manteau"

    s["CHK_T0001_P0000"] = [
        "papa|On passe où, avant la pomme ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|Ou la chambre.",
    ]
    sons["CHK_T0001_P0000"] = ""

    for i, loc in L1_022.items():
        s[f"CHK_T0001_P000{i}"] = L1_BODY_022[i]
        sons[f"CHK_T0001_P000{i}"] = loc["son"]
        s[f"CHK_T0001_P000{i}_Q0001"] = Q_022[i]
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        qf[f"CHK_T0001_P000{i}_Q0001"] = {
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | son manteau | le manteau de laine",
            "retry_prompt": "Le manteau de laine. Aniss a mis quoi ?",
        }
        s[f"CHK_T0001_P000{i}_C0001"] = C_022[i]
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        s[f"CHK_T0001_P000{i}_T0002_P0000"] = [
            "maman|Tu emportes quel jeu ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|Ou la dînette.",
        ]
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""

        for j, jeu in L2_022.items():
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            extra = L2_EXTRA_022[(i, j)]
            s[cid2] = L2_BODY_022[j] + [
                f"narrateur|{extra}",
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[cid2] = ""
            s[f"{cid2}_T0003_P0000"] = [
                "papa|C'est quel moment, pour la pomme ?",
                "narrateur|Le matin.",
                "narrateur|Après la sieste.",
                "narrateur|Ou le soir.",
            ]
            sons[f"{cid2}_T0003_P0000"] = ""

            for k, mom in L3_022.items():
                cid3 = f"{cid2}_T0003_P000{k}"
                img = IMG_022[(i, j, k)]
                fin = FIN_022[(i, j, k)]
                s[cid3] = (
                    MOMENT_022[k]
                    + [
                        f"narrateur|Aniss a {jeu['obj']} avec lui.",
                        f"narrateur|Il est encore {loc['ici']}.",
                    ]
                    + L3_SORTIE_022[k]
                    + [
                        f"narrateur|Il pose {jeu['un']}, près de la pomme.",
                        "enfant-m|La pomme est à moi.",
                        "papa|Un moment, oui.",
                    ]
                    + L3_RETOUR_022
                    + [
                        f"narrateur|{img}",
                        "papa|Merci, Aniss.",
                    ]
                )
                sons[cid3] = {1: "oiseau", 2: "", 3: ""}.get(k, "")
                s[f"{cid3}_F0001"] = [
                    f"narrateur|Aniss est passé par {loc['lab']}.",
                    f"narrateur|Il a emporté {jeu['lab']}.",
                    f"narrateur|C'était {mom['quand']}.",
                    "narrateur|Il a mis le manteau de laine.",
                    "narrateur|En rentrant, il l'a raccroché.",
                    "narrateur|La pomme est dans le bol, maintenant.",
                    f"narrateur|{img}",
                    "maman|Le crochet attend déjà demain.",
                    "enfant-m|La pomme aussi.",
                    f"narrateur|{fin}",
                ]
                sons[f"{cid3}_F0001"] = ""
    return s, sons, qf


# ---------------------------------------------------------------------------
# TREE-AUT-023  N1  Chouchou  AUT.AFF.003  manteau sur la rampe
# Monde unique ≠ TREE-AUT-017 (citron, parc) et ≠ TREE-AUT-020 (chat fenêtre).
# T3 : banc / portail / paillasson (plus Tom / Léa / Sami).
# ---------------------------------------------------------------------------

L1_023 = {
    1: {"lab": "le bac à sable", "ici": "au bac à sable"},
    2: {"lab": "le toboggan", "ici": "au toboggan"},
    3: {"lab": "les balançoires", "ici": "aux balançoires"},
}
L2_023 = {
    1: {"lab": "le ballon", "obj": "le ballon", "un": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau", "un": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou", "un": "le doudou"},
}
L3_023 = {
    1: {"lab": "le banc", "ou": "vers le banc", "ici": "le banc"},
    2: {"lab": "le portail", "ou": "vers le portail", "ici": "le portail"},
    3: {"lab": "le paillasson", "ou": "vers le paillasson", "ici": "le paillasson"},
}

L1_BODY_023 = {
    1: [
        "narrateur|Chouchou pousse la porte du jardin.",
        "narrateur|Le bois est un peu rêche.",
        "narrateur|Le bac à sable est encore frais.",
        "narrateur|Des grains collent à la planche.",
        "narrateur|Une petite pelle dort dans le sable.",
        "maman|Tu vas au bac, Chouchou ?",
        "enfant-f|Oui.",
        "enfant-f|Je veux le sable.",
        "papa|On joue un peu.",
        "narrateur|Chouchou pose les genoux dans le bac.",
        "narrateur|Le sable est froid et doux.",
        "narrateur|Le manteau rouge reste près du bac.",
        "narrateur|Le seau jaune est à côté.",
        "enfant-f|Mon seau est là.",
        "maman|Tu le verras, tout à l'heure.",
        "narrateur|Un oiseau picore près du banc.",
        "papa|Tes joues sont déjà roses.",
    ],
    2: [
        "narrateur|Chouchou va vers le toboggan.",
        "narrateur|Le métal est tiède sous la paume.",
        "narrateur|Les marches font toc, toc.",
        "papa|J'attends en bas.",
        "enfant-f|Je vais, papa.",
        "narrateur|Le vent touche ses cheveux.",
        "narrateur|Elle glisse.",
        "narrateur|Ça fait houuu, tout doux.",
        "enfant-f|Encore un peu ?",
        "maman|Une fois, oui.",
        "narrateur|Le seau reste près des marches.",
        "narrateur|Le manteau rouge est sur le banc.",
        "papa|Tu n'as plus froid, hein ?",
        "enfant-f|Non, je glisse encore.",
        "narrateur|Une feuille colle sur la rampe.",
        "maman|Tes mains sont tièdes.",
    ],
    3: [
        "narrateur|Chouchou va vers les balançoires.",
        "narrateur|La corde est un peu rêche.",
        "narrateur|Le siège est lisse, un peu chaud.",
        "maman|Je pousse tout doux.",
        "enfant-f|Encore un peu ?",
        "maman|Encore.",
        "narrateur|Un oiseau passe au-dessus.",
        "papa|Tu le tiens bien.",
        "enfant-f|Je voyage.",
        "narrateur|Le seau est près du pied de bois.",
        "narrateur|Le manteau rouge attend sur le banc.",
        "maman|Tu as les joues roses, Chouchou.",
        "enfant-f|Encore une fois.",
        "papa|Une dernière, d'accord.",
        "narrateur|La corde fait cling, puis se tait.",
        "papa|Tes pieds retrouvent l'herbe.",
    ],
}

Q_023 = {
    1: [
        "narrateur|Le seau est encore près du bac.",
        "papa|Chouchou, tu fais quoi ?",
    ],
    2: [
        "narrateur|Le manteau est encore sur le banc.",
        "maman|Chouchou, tu fais quoi ?",
    ],
    3: [
        "narrateur|Le seau est encore au pied de bois.",
        "papa|Chouchou, tu fais quoi ?",
    ],
}

C_023 = {
    1: [
        "narrateur|Chouchou regarde derrière elle.",
        "narrateur|Le seau jaune est encore là.",
        "enfant-f|Je reviens.",
        "maman|Oui.",
        "maman|On reprend le seau.",
        "papa|Et le manteau, sur le banc.",
        "enfant-f|Je les prends.",
        "papa|Merci, Chouchou.",
        "narrateur|Un grain reste au fond du seau.",
    ],
    2: [
        "narrateur|Chouchou s'arrête au bas du toboggan.",
        "narrateur|Le manteau rouge est encore là.",
        "enfant-f|J'y vais.",
        "papa|Oui.",
        "papa|On reprend le manteau.",
        "maman|Et le seau, près des marches.",
        "enfant-f|Je les prends.",
        "maman|Merci, Chouchou.",
        "narrateur|La feuille reste sur la rampe.",
    ],
    3: [
        "narrateur|Chouchou pose un pied au sol.",
        "narrateur|Le seau est encore au pied de bois.",
        "enfant-f|Je le prends.",
        "maman|Oui.",
        "maman|On reprend le seau.",
        "papa|Et le manteau, sur le banc.",
        "enfant-f|Ils viennent.",
        "papa|Merci.",
        "narrateur|La corde ne fait plus cling.",
    ],
}

L2_BODY_023 = {
    1: [
        "narrateur|Chouchou a choisi le ballon.",
        "narrateur|Il est rouge et lisse.",
        "narrateur|Il fait un petit bond.",
        "papa|Le ballon reste près de nous.",
        "enfant-f|Il est rouge, papa.",
        "maman|Comme le manteau, lui.",
        "narrateur|Chouchou pose le ballon contre le seau.",
        "enfant-f|Ils se parlent.",
        "papa|Tout doux, oui.",
        "narrateur|Un brin d'herbe colle au cuir.",
        "narrateur|Le seau et le manteau restent près.",
    ],
    2: [
        "narrateur|Chouchou a choisi le seau.",
        "narrateur|Le seau jaune a du sable.",
        "narrateur|L'anse est un peu froide.",
        "maman|C'est ton seau, Chouchou.",
        "enfant-f|Il est jaune.",
        "enfant-f|Il chante un peu.",
        "papa|Tu le tiens à deux mains ?",
        "narrateur|Elle le pose, puis le reprend.",
        "narrateur|Le seau fait un petit toc.",
        "maman|Il voyage avec toi.",
        "narrateur|Le manteau rouge reste encore près.",
    ],
    3: [
        "narrateur|Chouchou a choisi le doudou.",
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Un peu de sable est dessus.",
        "maman|Il t'attendait, Chouchou.",
        "enfant-f|Il est doux.",
        "papa|Tu le serres contre toi ?",
        "narrateur|Elle le serre, tout chaud.",
        "enfant-f|Il vient.",
        "maman|Oui.",
        "narrateur|L'oreille du doudou est chaude.",
        "narrateur|Le seau reste un peu plus loin.",
    ],
}

L2_EXTRA_023 = {
    (1, 1): "Un grain de sable colle au ballon.",
    (1, 2): "Du sable fin brille dans le seau.",
    (1, 3): "L'oreille grise a un peu de sable.",
    (2, 1): "Le ballon est un peu froid, près de la rampe.",
    (2, 2): "Le seau sonne tout doux contre une marche.",
    (2, 3): "Le doudou a vu le toboggan, tout gris.",
    (3, 1): "Un brin d'herbe colle au ballon.",
    (3, 2): "L'anse du seau est froide, près de la corde.",
    (3, 3): "Le doudou a senti le vent, tout doux.",
}

L3_BODY_023 = {
    1: [
        "narrateur|Chouchou va vers le banc.",
        "narrateur|Le bois des lattes est chaud.",
        "narrateur|Une fourmi marche sur le bord.",
        "enfant-f|Le banc est chaud, maman.",
        "maman|Oui.",
        "maman|On s'assoit un peu.",
        "narrateur|Sous le banc, le manteau rouge attend.",
        "narrateur|Chouchou le tire, tout doucement.",
        "enfant-f|J'ai le manteau.",
        "papa|Tu le prends.",
        "narrateur|Le seau est près de ses pieds.",
        "narrateur|Chouchou le prend aussi.",
        "enfant-f|J'ai tout.",
        "maman|Les fraises nous attendent.",
        "narrateur|On rentre.",
        "narrateur|Le chat lève la tête.",
    ],
    2: [
        "narrateur|Chouchou va vers le portail.",
        "narrateur|Le loquet est un peu froid.",
        "narrateur|Le portail fait criiic.",
        "enfant-f|J'entends le criiic, papa.",
        "papa|Oui.",
        "papa|On pousse tout doux.",
        "narrateur|Près du loquet, le seau jaune attend.",
        "narrateur|Chouchou le saisit par l'anse.",
        "enfant-f|J'ai le seau.",
        "maman|Tu le prends.",
        "narrateur|Le manteau est accroché au bois.",
        "narrateur|Chouchou le décroche.",
        "enfant-f|J'ai tout.",
        "maman|Les fraises nous attendent.",
        "narrateur|On rentre.",
        "narrateur|Le chat lève la tête.",
    ],
    3: [
        "narrateur|Chouchou va vers le paillasson.",
        "narrateur|Il est rêche, couleur paille.",
        "narrateur|Les chaussures attendent dessus.",
        "enfant-f|Ça pique un peu, maman.",
        "maman|Oui.",
        "maman|C'est le paillasson.",
        "narrateur|Sur le paillasson, le manteau est plié.",
        "narrateur|Chouchou le soulève.",
        "enfant-f|J'ai le manteau.",
        "papa|Tu le prends.",
        "narrateur|Le seau est contre le seuil.",
        "narrateur|Chouchou le prend aussi.",
        "enfant-f|J'ai tout.",
        "maman|Les fraises nous attendent.",
        "narrateur|On rentre.",
        "narrateur|Le chat lève la tête.",
    ],
}

IMG_023 = {
    (1, 1, 1): "Un grain de sable colle au banc.",
    (1, 1, 2): "Le ballon laisse une trace au loquet.",
    (1, 1, 3): "Un brin d'herbe reste au paillasson.",
    (1, 2, 1): "Du sable fin brille sous le banc.",
    (1, 2, 2): "L'anse jaune touche le bois du portail.",
    (1, 2, 3): "Un coquillage minuscule roule au seuil.",
    (1, 3, 1): "L'oreille grise dépasse du banc.",
    (1, 3, 2): "Le doudou sent encore le sable, au loquet.",
    (1, 3, 3): "Un fil gris pend du paillasson.",
    (2, 1, 1): "La feuille jaune colle au banc.",
    (2, 1, 2): "Le ballon est un peu froid, près du loquet.",
    (2, 1, 3): "Une goutte glisse vers le paillasson.",
    (2, 2, 1): "Le seau sonne tout doux contre le banc.",
    (2, 2, 2): "Le métal du toboggan se tait, près du portail.",
    (2, 2, 3): "Un pas sur la rampe, puis le paillasson.",
    (2, 3, 1): "Le doudou a vu le toboggan, depuis le banc.",
    (2, 3, 2): "L'oreille molle dépasse près du loquet.",
    (2, 3, 3): "La rampe brille encore, loin du paillasson.",
    (3, 1, 1): "La chaîne a fait cling, près du banc.",
    (3, 1, 2): "Le ballon a touché l'herbe, près du portail.",
    (3, 1, 3): "Un nuage passe au-dessus du paillasson.",
    (3, 2, 1): "L'anse du seau est froide, contre le banc.",
    (3, 2, 2): "Un cling lointain, et le portail.",
    (3, 2, 3): "Le seau jaune pose son ombre au seuil.",
    (3, 3, 1): "Le doudou a senti le vent, sur le banc.",
    (3, 3, 2): "La chaîne se tait, près du portail.",
    (3, 3, 3): "L'oreille grise dépasse du paillasson.",
}

FIN_023 = {
    (1, 1, 1): "Le chat se recouche près du panier.",
    (1, 1, 2): "Une fraise roule, tout près du pain.",
    (1, 1, 3): "L'escalier ne fait plus cric.",
    (1, 2, 1): "Le seau jaune sèche sous la rampe.",
    (1, 2, 2): "Le panier de fraises sent encore.",
    (1, 2, 3): "Une graine reste sur le paillasson.",
    (1, 3, 1): "Le doudou s'installe dans le couloir.",
    (1, 3, 2): "Une fraise luit, toute seule, au panier.",
    (1, 3, 3): "Le chat lèche encore sa patte.",
    (2, 1, 1): "Le manteau rouge retrouve la rampe.",
    (2, 1, 2): "Une feuille sèche près des clés de papa.",
    (2, 1, 3): "Le pain est encore tiède, sur la table.",
    (2, 2, 1): "Le seau penche un peu, sous la rampe.",
    (2, 2, 2): "Le loquet du portail se tait.",
    (2, 2, 3): "La rampe du toboggan reste loin, maintenant.",
    (2, 3, 1): "L'oreille du doudou dépasse du couloir.",
    (2, 3, 2): "Une fraise est sucrée, un peu froide encore.",
    (2, 3, 3): "Le rayon d'après-midi a bougé, sur le bois.",
    (3, 1, 1): "Le ballon s'endort près de l'escalier.",
    (3, 1, 2): "Le panier attend encore Chouchou.",
    (3, 3, 3): "Le couloir a de nouveau son calme.",
    (3, 2, 1): "Le seau pose son ombre sur la marche.",
    (3, 2, 2): "Le pain tiède est chaud, sur la table.",
    (3, 2, 3): "Les clés de papa restent dans la coupelle.",
    (3, 3, 1): "Le doudou a l'odeur de l'herbe, au couloir.",
    (3, 3, 2): "Une fraise rentre dans le panier.",
    (3, 1, 3): "L'escalier de bois se tait.",
}


def build_023() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    qf: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|L'escalier de bois fait cric, cric.",
        "narrateur|Un panier de fraises attend.",
        "narrateur|Il est dans le couloir.",
        "narrateur|Ça sent le sucré, tout près.",
        "narrateur|Le chat lèche sa patte.",
        "narrateur|Sur la rampe, un manteau rouge est posé.",
        "narrateur|Le manteau est encore un peu chaud.",
        "narrateur|Un seau jaune est sur une marche.",
        "narrateur|Il y a du sable au fond.",
        "papa|Les fraises sont belles, Chouchou.",
        "maman|On les goûtera tout à l'heure.",
        "narrateur|En ce moment, Chouchou est dans le couloir.",
        "narrateur|Elle a les mains un peu collantes.",
        "enfant-f|Je veux jouer dehors.",
        "papa|D'accord.",
        "papa|On va au jardin.",
        "narrateur|Chouchou touche le manteau.",
        "narrateur|Le tissu est doux sous les doigts.",
        "maman|Tu as fini tes doigts ?",
        "enfant-f|Oui, maman.",
        "papa|Alors on ouvre le jardin.",
        "narrateur|Le seau tape doucement une marche.",
    ]
    sons["CHK_T0000_P0000"] = ""

    s["CHK_T0001_P0000"] = [
        "narrateur|Le jardin de la maison est calme.",
        "papa|Tu veux le bac à sable, Chouchou ?",
        "maman|Le toboggan, ou les balançoires ?",
        "papa|Choisis.",
    ]
    sons["CHK_T0001_P0000"] = "oiseau"

    for i, loc in L1_023.items():
        s[f"CHK_T0001_P000{i}"] = L1_BODY_023[i]
        sons[f"CHK_T0001_P000{i}"] = "oiseau"
        s[f"CHK_T0001_P000{i}_Q0001"] = Q_023[i]
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        qf[f"CHK_T0001_P000{i}_Q0001"] = {
            "expected_answer": "reprendre",
            "accepted_examples": "reprendre | ses affaires | elle reprend | le seau | le manteau",
            "retry_prompt": "Elle reprend le seau. Chouchou fait quoi ?",
        }
        s[f"CHK_T0001_P000{i}_C0001"] = C_023[i]
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        s[f"CHK_T0001_P000{i}_T0002_P0000"] = [
            "maman|Tu emportes quel jeu ?",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Ou le doudou.",
        ]
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""

        for j, jeu in L2_023.items():
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            extra = L2_EXTRA_023[(i, j)]
            s[cid2] = L2_BODY_023[j] + [
                f"narrateur|{extra}",
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[cid2] = ""
            t3 = f"{cid2}_T0003_P0000"
            s[t3] = [
                "papa|On va vers où, pour rentrer ?",
                "narrateur|Le banc.",
                "narrateur|Le portail.",
                "narrateur|Ou le paillasson.",
            ]
            sons[t3] = ""
            qf[t3] = {
                "option_1_label": "le banc",
                "option_2_label": "le portail",
                "option_3_label": "le paillasson",
            }

            for k, lieu in L3_023.items():
                cid3 = f"{cid2}_T0003_P000{k}"
                img = IMG_023[(i, j, k)]
                fin = FIN_023[(i, j, k)]
                s[cid3] = [
                    "narrateur|C'est l'heure des fraises.",
                    f"narrateur|Chouchou quitte {loc['lab']}.",
                    f"narrateur|Elle a encore {jeu['un']} avec elle.",
                    *L3_BODY_023[k],
                    f"narrateur|{jeu['un'].capitalize()} vient aussi.",
                    f"narrateur|{img}",
                    "enfant-f|On rentre.",
                    "maman|Oui.",
                    "maman|On rentre ensemble.",
                ]
                sons[cid3] = ""
                s[f"{cid3}_F0001"] = [
                    "narrateur|L'escalier de bois est calme.",
                    f"narrateur|Chouchou a joué {loc['ici']}.",
                    f"narrateur|Elle a choisi {jeu['lab']}.",
                    f"narrateur|Elle est passée par {lieu['ici']}.",
                    "narrateur|Le seau et le manteau sont avec elle.",
                    "narrateur|Elle croque une fraise, tout sucrée.",
                    "enfant-f|Elle est bonne.",
                    "maman|Oui.",
                    "papa|Le chat, Chouchou ?",
                    "narrateur|Le chat se recouche, tout calme.",
                    f"narrateur|{img}",
                    f"narrateur|{fin}",
                ]
                sons[f"{cid3}_F0001"] = ""
    return s, sons, qf


def main() -> None:
    s, sons, qf = build_022()
    write_story(
        "TREE-AUT-022",
        (
            "Aniss veut la pomme rouge sous le pommier. Le manteau glisse "
            "dans l'herbe mouillée. Une manche est tordue. Il le met. Ils "
            "passent par la cuisine, le jardin ou la chambre, avec un jeu. "
            "Ils prennent la pomme. Le manteau goutte au crochet. La pomme "
            "est dans le bol."
        ),
        "La pomme dans l'herbe",
        "Aniss, papa, maman",
        "jardin du pommier, puis cuisine, jardin ou chambre",
        s,
        sons,
        qf,
    )
    relecture(
        "TREE-AUT-022",
        "La pomme dans l'herbe",
        (
            "Monde : pommier, abeille, soupe par la porte, banc de bois. "
            "Désir : la pomme rouge. Imprévu : manteau qui tombe, manche "
            "tordue. Résolution : Aniss le met, raccroche au retour. "
            "Question manteau. 27 fins distinctes."
        ),
        (
            "Nora→Aniss. Leçon AUT.AFF.002 vécue, pas dite. Branches "
            "cuisine/jardin/chambre × cubes/livre/dînette × matin/sieste/soir. "
            "SSML = texte. Pas d'audio."
        ),
    )

    s, sons, qf = build_023()
    write_story(
        "TREE-AUT-023",
        (
            "Chouchou veut jouer dehors, puis les fraises du panier. Le "
            "manteau est sur la rampe, le seau sur une marche. Elle joue. "
            "Au moment des fraises, le seau et le manteau sont encore là. "
            "Elle les reprend, au banc, au portail ou au paillasson. Une "
            "fraise, le chat se recouche, l'escalier se tait."
        ),
        "Le manteau sur la rampe",
        "Chouchou, papa, maman",
        "couloir, rampe de bois, jardin de la maison",
        s,
        sons,
        qf,
    )
    relecture(
        "TREE-AUT-023",
        "Le manteau sur la rampe",
        (
            "Monde : escalier cric, fraises, chat, rampe. Désir : jouer "
            "dehors puis fraises. Imprévu : seau et manteau restés. "
            "Résolution : Chouchou les reprend. Question reprendre. "
            "T3 = banc / portail / paillasson."
        ),
        (
            "Maya→Chouchou. N1 ≤10 mots. Leçon AUT.AFF.003 implicite. "
            "Plus Tom/Léa/Sami. SSML = texte. Pas d'audio."
        ),
    )


if __name__ == "__main__":
    main()
