#!/usr/bin/env python3
"""TREE-AUT-016 / TREE-AUT-017 — récit implicite, graphe conservé, D16."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    FORBIDDEN,
    OPENING_BAD,
    ROLES,
    ROOT,
    from_script,
    words,
)

LIMITS = {"N1": 10, "N2": 15}
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "lina", "iris", "aïcha", "aicha",
    "clément", "clement", "léonie", "leonie", "clarisse",
    "éléonore", "eleonore", "dominique", "zoé", "zoe", "adam",
    "ariane", "benoît", "benoit", "delphine", "erwan", "kenzo",
    "alban", "agathe", "barnabé", "barnabe", "nora", "constentin",
    "constantin", "lucas", "luca", "céline", "celine", "alice",
    "noé", "noe", "victorina", "léa", "lea ", "tom ", "sami",
)


def check_story(sid: str, age: str, chunks: list[dict], allow_sac: bool) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    blob = low
    if allow_sac:
        blob = re.sub(r"\bsac (tom|léa|lea|sami)\b", "sac X", blob)
        blob = re.sub(r"\b(tom|léa|lea|sami)\.", "X.", blob)
        blob = blob.replace("tom ", "X ").replace("léa", "x").replace("lea ", "x ")
        blob = blob.replace("sami", "x")
    for name in BAD_NAMES:
        if name in blob:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
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
    allow_sac: bool = False,
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
    check_story(sid, out["age_band"], out["chunks"], allow_sac)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# TREE-AUT-016  N1  Raphaël  AUT.AFF.002  manteau de laine
# ---------------------------------------------------------------------------

L1_016 = {
    1: {
        "lab": "la cuisine",
        "ou": "vers la cuisine",
        "ici": "dans la cuisine",
        "son": "soupe",
    },
    2: {
        "lab": "le jardin",
        "ou": "vers le jardin",
        "ici": "dans le jardin",
        "son": "pluie",
    },
    3: {
        "lab": "la chambre",
        "ou": "vers la chambre",
        "ici": "dans la chambre",
        "son": "rideau",
    },
}
L2_016 = {
    1: {"lab": "les cubes", "obj": "les cubes", "un": "un cube"},
    2: {"lab": "le livre", "obj": "le livre", "un": "le livre"},
    3: {"lab": "la dînette", "obj": "la dînette", "un": "une tasse"},
}
L3_016 = {
    1: {"lab": "le matin", "quand": "le matin"},
    2: {"lab": "après la sieste", "quand": "après la sieste"},
    3: {"lab": "le soir", "quand": "le soir"},
}

L1_BODY_016 = {
    1: [
        "narrateur|Raphaël pousse la porte de la cuisine.",
        "narrateur|Les carreaux sont un peu tièdes.",
        "narrateur|Ça sent la soupe dans la casserole.",
        "narrateur|La vitre de la cuisine est embuée.",
        "narrateur|Le manteau de laine fume un peu.",
        "papa|La soupe est chaude, hein ?",
        "enfant-m|Oui, papa.",
        "enfant-m|Mon manteau aussi.",
        "maman|Une feuille de laurier tombe.",
        "narrateur|Elle glisse près de l'évier.",
        "narrateur|Raphaël la ramasse, tout doux.",
        "papa|Tu la mets dans la poche ?",
        "enfant-m|Oui.",
        "narrateur|La poche de laine est rêche.",
        "narrateur|La feuille sent le bois.",
        "maman|On sort par la porte de derrière ?",
        "enfant-m|Vers la flaque.",
        "papa|Le manteau est déjà sur toi.",
        "narrateur|Raphaël touche le bouton chaud.",
    ],
    2: [
        "narrateur|Raphaël va vers le jardin.",
        "narrateur|L'herbe est mouillée, toute brillante.",
        "narrateur|L'air est frais sur le nez.",
        "narrateur|Le manteau sent la laine.",
        "papa|Tu as tes bottes jaunes ?",
        "enfant-m|Oui.",
        "enfant-m|Elles font ploc.",
        "maman|La flaque est près du potager.",
        "narrateur|Une goutte tombe d'une feuille.",
        "narrateur|Elle fait un tout petit bruit.",
        "narrateur|Raphaël serre le col contre sa joue.",
        "papa|Tu n'as pas froid ?",
        "enfant-m|Non.",
        "enfant-m|Le manteau est chaud.",
        "maman|L'herbe mouille le bas, un peu.",
        "narrateur|Le bas de laine devient sombre.",
        "papa|On rentrera le sécher.",
        "narrateur|Raphaël avance dans l'herbe.",
    ],
    3: [
        "narrateur|Raphaël va vers la chambre.",
        "narrateur|La couverture est douce, toute pliée.",
        "narrateur|Le rideau jaune bouge un peu.",
        "narrateur|Le manteau frotte la porte.",
        "maman|Ton petit bateau est sur le lit.",
        "enfant-m|Je le prends.",
        "enfant-m|Pour la flaque.",
        "papa|Il tient dans la poche ?",
        "narrateur|Raphaël glisse le bateau.",
        "narrateur|La poche de laine est épaisse.",
        "narrateur|L'oreiller sent encore le savon.",
        "maman|Le rideau touche tes épaules.",
        "enfant-m|C'est doux.",
        "papa|On sort après, d'accord ?",
        "enfant-m|Avec le bateau.",
        "narrateur|Raphaël marche tout doux sur le tapis.",
        "narrateur|Le manteau fait un bruit de laine.",
    ],
}

Q_016 = {
    1: [
        "narrateur|Le manteau est chaud, dans la cuisine.",
        "papa|Raphaël a pris quoi, pour sortir ?",
    ],
    2: [
        "narrateur|Dehors, Raphaël n'a pas froid.",
        "maman|Il a pris quoi, avant ?",
    ],
    3: [
        "narrateur|Le manteau frotte la porte.",
        "papa|Raphaël a pris quoi ?",
    ],
}

C_016 = {
    1: [
        "narrateur|Oui.",
        "narrateur|Il a pris le manteau de laine.",
        "papa|Merci, Raphaël.",
        "maman|La feuille est dans la poche.",
        "enfant-m|Elle sent le bois.",
        "papa|On emporte un jeu ?",
        "narrateur|La casserole chante tout bas.",
    ],
    2: [
        "narrateur|Oui.",
        "narrateur|Le manteau de laine est sur lui.",
        "maman|Bravo.",
        "maman|Tu n'as pas froid.",
        "enfant-m|Il est chaud.",
        "papa|On emporte un jeu, dans le jardin ?",
        "narrateur|Une goutte brille encore sur l'herbe.",
    ],
    3: [
        "narrateur|Oui.",
        "narrateur|Le manteau est sur Raphaël.",
        "papa|Le bateau est dans la poche.",
        "enfant-m|Pour la flaque.",
        "maman|On emporte un jeu aussi ?",
        "narrateur|Le rideau se tait.",
        "narrateur|La chambre est calme.",
    ],
}

L2_BODY_016 = {
    1: [
        "narrateur|Raphaël a choisi les cubes.",
        "narrateur|Ils sont en bois, un peu lourds.",
        "narrateur|Ils cliquent dans la boîte.",
        "papa|On fait un pont, pour la flaque ?",
        "enfant-m|Oui.",
        "enfant-m|Un pont de cubes.",
        "maman|Le manteau garde tes bras au chaud.",
        "narrateur|Un cube sent le pin.",
        "narrateur|Raphaël le serre contre la laine.",
        "papa|On les emporte.",
        "narrateur|La boîte tape doucement sa hanche.",
    ],
    2: [
        "narrateur|Raphaël a choisi le livre.",
        "narrateur|La couverture est un peu froissée.",
        "narrateur|Une page montre de la pluie.",
        "maman|Comme dehors, hein ?",
        "enfant-m|Oui.",
        "enfant-m|La vraie pluie.",
        "papa|On le met sous le manteau.",
        "narrateur|Le livre glisse contre la laine.",
        "narrateur|Il reste au sec.",
        "maman|On le regardera près de la flaque.",
        "narrateur|Une page se recourbe, tout doux.",
    ],
    3: [
        "narrateur|Raphaël a choisi la dînette.",
        "narrateur|Une petite tasse sonne, tout creux.",
        "narrateur|Une cuillère miniature est tiède.",
        "papa|On sert la flaque ?",
        "enfant-m|Oui.",
        "enfant-m|Un thé de pluie.",
        "maman|La tasse tient dans la poche.",
        "narrateur|Raphaël la glisse à côté du bouton.",
        "narrateur|La laine la tient.",
        "papa|On y va, alors.",
        "narrateur|La petite assiette reste dans l'autre main.",
    ],
}

L2_EXTRA_016 = {
    (1, 1): "Un cube attrape un reflet de soupe.",
    (1, 2): "Une miette reste au bord de la page.",
    (1, 3): "La petite casserole est près du vrai bol.",
    (2, 1): "L'herbe tache un cube, tout vert.",
    (2, 2): "Une vraie feuille sert de marque-page.",
    (2, 3): "Une goutte perle au bord de l'assiette.",
    (3, 1): "Un cube tapote le parquet, tout doux.",
    (3, 2): "Le rideau jaune colore la page.",
    (3, 3): "La petite tasse est près du bateau.",
}

MOMENT_016 = {
    1: [
        "narrateur|C'est le matin.",
        "narrateur|La lumière est pâle, tout douce.",
        "narrateur|Un oiseau chante une fois.",
    ],
    2: [
        "narrateur|C'est après la sieste.",
        "narrateur|Les joues de Raphaël sont chaudes.",
        "narrateur|La maison est encore calme.",
    ],
    3: [
        "narrateur|C'est le soir.",
        "narrateur|La lampe fait un rond jaune.",
        "narrateur|Le radiateur reprend son tic tic.",
    ],
}

L3_SORTIE_016 = {
    1: [
        "papa|La flaque est claire, ce matin.",
        "narrateur|Ils sortent un moment.",
        "narrateur|L'air touche le nez de Raphaël.",
        "enfant-m|Elle brille.",
        "maman|Tes pieds, dans les bottes ?",
        "enfant-m|Ils sont au chaud.",
    ],
    2: [
        "papa|La flaque a rétréci, un peu.",
        "narrateur|Ils sortent un moment.",
        "narrateur|Le soleil est jaune et doux.",
        "enfant-m|Elle est tiède.",
        "maman|Le manteau est encore utile.",
        "enfant-m|Oui, un peu.",
    ],
    3: [
        "papa|La flaque est sombre, ce soir.",
        "narrateur|Ils sortent un moment.",
        "narrateur|La vitre de la maison est bleue.",
        "enfant-m|Je vois les lumières.",
        "maman|Le manteau te tient chaud.",
        "enfant-m|Oui, maman.",
    ],
}

L3_RETOUR_016 = [
    "papa|C'est l'heure de rentrer.",
    "narrateur|Ils rentrent.",
    "narrateur|Le manteau de laine est un peu lourd.",
    "narrateur|Raphaël le retire.",
    "narrateur|Il le raccroche au petit crochet.",
    "maman|Il goutte, tout doux.",
    "enfant-m|Il sèche, là.",
    "papa|Oui.",
    "papa|Le crochet est à ta hauteur.",
]

IMG_016 = {
    (1, 1, 1): "Une miette de soupe sèche sur un cube.",
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
    (3, 2, 1): "Le rideau jaune colore la page.",
    (3, 2, 2): "Le livre est ouvert sur la couverture.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FIN_016 = {
    (1, 1, 1): "Le radiateur reprend son tic tic.",
    (1, 1, 2): "La casserole fait un tout petit pschitt.",
    (1, 1, 3): "Une miette reste sur la table.",
    (1, 2, 1): "Un oiseau chante encore, tout loin.",
    (1, 2, 2): "La page se recourbe, près du bol.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "La soupe sent encore, tout bas.",
    (1, 3, 3): "Le bouton du manteau brille, au crochet.",
    (2, 1, 1): "Les bottes jaunes sèchent près de la porte.",
    (2, 1, 2): "L'herbe colle encore à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau.",
    (2, 2, 1): "Une feuille vraie reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "La flaque ne brille plus, dehors.",
    (2, 3, 1): "La petite assiette a encore de l'herbe.",
    (2, 3, 2): "Les bottes font un dernier ploc.",
    (2, 3, 3): "Le col de laine sèche, au crochet.",
    (3, 1, 1): "Le bateau de papier repose sur un cube.",
    (3, 1, 2): "L'oreiller sent encore le savon.",
    (3, 1, 3): "Le rideau jaune ne bouge plus.",
    (3, 2, 1): "Le bateau sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près du bateau.",
    (3, 3, 2): "Le tapis de la chambre est calme.",
    (3, 3, 3): "Le radiateur fait tic tic, tout loin.",
}


def build_016() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    qf: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|Le radiateur du salon fait tic tic.",
        "narrateur|Un manteau de laine attend.",
        "narrateur|Il est sur le petit crochet.",
        "narrateur|Le crochet est bas, tout près.",
        "narrateur|La pluie trace des lignes.",
        "narrateur|Elles glissent sur la grande vitre.",
        "narrateur|Le tapis beige est tout épais.",
        "narrateur|Une chaussette dépasse sous le canapé.",
        "narrateur|L'air sent la terre mouillée.",
        "narrateur|La fenêtre est un peu ouverte.",
        "narrateur|Les bottes jaunes sont là.",
        "narrateur|Elles sont dans une flaque de lumière.",
        "papa|Raphaël, tu as vu la flaque ?",
        "enfant-m|Oui, papa.",
        "enfant-m|Je veux la flaque.",
        "maman|Dehors, le vent est froid.",
        "narrateur|En ce moment, Raphaël va vers la porte.",
        "narrateur|Il tire la poignée, tout doux.",
        "narrateur|L'air froid entre.",
        "enfant-m|J'ai froid, papa.",
        "papa|Le manteau de laine est là.",
        "papa|Il attend, au crochet.",
        "narrateur|Raphaël prend le manteau.",
        "narrateur|Une manche est à l'envers.",
        "enfant-m|Oh.",
        "enfant-m|Ça ne passe pas.",
        "maman|On tourne la manche.",
        "narrateur|Maman tourne le tissu rêche.",
        "narrateur|Raphaël glisse un bras.",
        "narrateur|Il glisse l'autre bras.",
        "enfant-m|Il est chaud.",
        "papa|Oui.",
        "papa|Il te tiendra chaud.",
        "maman|On peut aller à la flaque ?",
        "enfant-m|Oui.",
        "narrateur|Le radiateur fait encore tic tic.",
    ]
    sons["CHK_T0000_P0000"] = "pluie"

    s["CHK_T0001_P0000"] = [
        "papa|On passe où, avant de sortir ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|Ou la chambre.",
    ]
    sons["CHK_T0001_P0000"] = ""

    for i, loc in L1_016.items():
        s[f"CHK_T0001_P000{i}"] = L1_BODY_016[i]
        sons[f"CHK_T0001_P000{i}"] = loc["son"]
        s[f"CHK_T0001_P000{i}_Q0001"] = Q_016[i]
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        qf[f"CHK_T0001_P000{i}_Q0001"] = {
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | son manteau | le manteau de laine",
            "retry_prompt": "Le manteau de laine. Raphaël a pris quoi ?",
        }
        s[f"CHK_T0001_P000{i}_C0001"] = C_016[i]
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        s[f"CHK_T0001_P000{i}_T0002_P0000"] = [
            "maman|Tu emportes quel jeu ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|Ou la dînette.",
        ]
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""

        for j, jeu in L2_016.items():
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            extra = L2_EXTRA_016[(i, j)]
            s[cid2] = L2_BODY_016[j] + [
                f"narrateur|{extra}",
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[cid2] = "voiture_passe" if (i, j) == (1, 1) else ""
            s[f"{cid2}_T0003_P0000"] = [
                "papa|C'est quel moment, pour sortir ?",
                "narrateur|Le matin.",
                "narrateur|Après la sieste.",
                "narrateur|Ou le soir.",
            ]
            sons[f"{cid2}_T0003_P0000"] = ""

            for k, mom in L3_016.items():
                cid3 = f"{cid2}_T0003_P000{k}"
                img = IMG_016[(i, j, k)]
                fin = FIN_016[(i, j, k)]
                s[cid3] = (
                    MOMENT_016[k]
                    + [
                        f"narrateur|Raphaël a {jeu['obj']} avec lui.",
                        f"narrateur|Il est encore {loc['ici']}.",
                    ]
                    + L3_SORTIE_016[k]
                    + [
                        f"narrateur|Il pose {jeu['un']}, près de la flaque.",
                        "enfant-m|La flaque est à moi.",
                        "papa|Un moment, oui.",
                    ]
                    + L3_RETOUR_016
                    + [
                        f"narrateur|{img}",
                        "papa|Merci, Raphaël.",
                    ]
                )
                sons[cid3] = {1: "oiseau", 2: "", 3: "radiateur"}.get(k, "")
                s[f"{cid3}_F0001"] = [
                    f"narrateur|Raphaël est passé par {loc['lab']}.",
                    f"narrateur|Il a emporté {jeu['lab']}.",
                    f"narrateur|C'était {mom['quand']}.",
                    "narrateur|Il a mis le manteau de laine.",
                    "narrateur|En rentrant, il l'a raccroché.",
                    f"narrateur|{img}",
                    "maman|Le crochet attend déjà demain.",
                    "enfant-m|La flaque aussi.",
                    f"narrateur|{fin}",
                ]
                sons[f"{cid3}_F0001"] = ""
    return s, sons, qf


# ---------------------------------------------------------------------------
# TREE-AUT-017  N2  Mila  AUT.AFF.003  citron / parc / sacs
# ---------------------------------------------------------------------------

L1_017 = {
    1: {"lab": "le bac à sable", "ou": "vers le bac à sable", "ici": "au bac à sable"},
    2: {"lab": "le toboggan", "ou": "vers le toboggan", "ici": "au toboggan"},
    3: {"lab": "les balançoires", "ou": "vers les balançoires", "ici": "aux balançoires"},
}
L2_017 = {
    1: {"lab": "le ballon", "obj": "le ballon", "un": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau", "un": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou", "un": "le doudou"},
}
L3_017 = {
    1: {"lab": "Tom", "sac": "le sac Tom", "coul": "bleu"},
    2: {"lab": "Léa", "sac": "le sac Léa", "coul": "rouge"},
    3: {"lab": "Sami", "sac": "le sac Sami", "coul": "vert"},
}

L1_BODY_017 = {
    1: [
        "narrateur|Mila va vers le bac à sable.",
        "narrateur|Le sable est frais, un peu sombre.",
        "narrateur|Ça fait chh sous les doigts.",
        "narrateur|Le bord en bois est tiède.",
        "papa|Tu verses, Mila ?",
        "enfant-f|Oui, ça chante.",
        "narrateur|Elle pose le citron sur le château.",
        "narrateur|On dirait un petit soleil.",
        "maman|Il est jaune, comme le seau.",
        "narrateur|Le seau jaune reste près du bac.",
        "narrateur|Le manteau rouge est sur le banc.",
        "enfant-f|J'ai chaud, maman.",
        "papa|Le manteau peut attendre, alors.",
        "narrateur|Mila appuie un château.",
        "narrateur|Un grain reste sous son ongle.",
        "maman|Le citron tient, tout rond.",
        "enfant-f|C'est mon soleil.",
    ],
    2: [
        "narrateur|Mila va vers le toboggan.",
        "narrateur|Le métal est tiède sous la paume.",
        "narrateur|Les marches font toc, toc.",
        "narrateur|Elle glisse le citron dans la poche.",
        "papa|J'attends en bas.",
        "enfant-f|Je vais, papa.",
        "narrateur|Le vent touche ses cheveux.",
        "narrateur|Elle glisse.",
        "narrateur|Ça fait houuu, tout doux.",
        "enfant-f|Le citron a glissé avec moi.",
        "maman|Il est encore dans la poche ?",
        "enfant-f|Oui.",
        "narrateur|Le seau reste près des marches.",
        "narrateur|Le manteau rouge est sur le banc.",
        "papa|Tu n'as plus froid, hein ?",
        "enfant-f|Non, je glisse encore.",
        "narrateur|Une feuille colle sur la rampe.",
    ],
    3: [
        "narrateur|Mila va vers les balançoires.",
        "narrateur|La corde est un peu rêche.",
        "narrateur|Le siège est lisse, un peu chaud.",
        "maman|Je pousse tout doux.",
        "enfant-f|Encore un peu ?",
        "maman|Encore.",
        "narrateur|Le citron est sur ses genoux.",
        "narrateur|Il ne tombe pas.",
        "papa|Tu le tiens bien.",
        "enfant-f|Il voyage.",
        "narrateur|Un oiseau passe au-dessus.",
        "narrateur|Le seau est près du pied de bois.",
        "narrateur|Le manteau rouge attend sur le banc.",
        "maman|Tu as les joues roses, Mila.",
        "enfant-f|Encore une fois.",
        "papa|Une dernière, d'accord.",
        "narrateur|La corde fait cling, puis se tait.",
    ],
}

Q_017 = {
    1: [
        "narrateur|Le seau est encore près du bac.",
        "papa|Avant de partir, Mila fait quoi ?",
    ],
    2: [
        "narrateur|Le manteau est encore sur le banc.",
        "maman|Avant de partir, Mila fait quoi ?",
    ],
    3: [
        "narrateur|Le seau est encore au pied de bois.",
        "papa|Avant de partir, Mila fait quoi ?",
    ],
}

C_017 = {
    1: [
        "narrateur|Mila regarde derrière elle.",
        "narrateur|Le seau jaune est encore là.",
        "enfant-f|Je reviens.",
        "maman|Oui.",
        "maman|On reprend le seau.",
        "papa|Et le manteau, sur le banc.",
        "enfant-f|Je les prends.",
        "papa|Bravo, Mila.",
        "narrateur|Un grain de sable reste au fond du seau.",
    ],
    2: [
        "narrateur|Mila s'arrête au bas du toboggan.",
        "narrateur|Le manteau rouge est encore sur le banc.",
        "enfant-f|J'y vais.",
        "papa|Oui.",
        "papa|On reprend le manteau.",
        "maman|Et le seau, près des marches.",
        "enfant-f|Je les prends.",
        "maman|Merci, Mila.",
        "narrateur|La feuille reste sur la rampe.",
    ],
    3: [
        "narrateur|Mila pose un pied au sol.",
        "narrateur|Le seau est encore au pied de bois.",
        "enfant-f|Je le prends.",
        "maman|Oui.",
        "maman|On reprend le seau.",
        "papa|Et le manteau, sur le banc.",
        "enfant-f|Ils viennent.",
        "papa|Bravo.",
        "narrateur|La corde ne fait plus cling.",
    ],
}

L2_BODY_017 = {
    1: [
        "narrateur|Mila a choisi le ballon.",
        "narrateur|Il est rouge et lisse.",
        "narrateur|Il fait un petit bond.",
        "papa|Le ballon reste près de nous.",
        "enfant-f|Il est rouge, papa.",
        "maman|Le citron est jaune, lui.",
        "narrateur|Mila pose le citron contre le ballon.",
        "enfant-f|Ils se parlent.",
        "papa|Tout doux, oui.",
        "narrateur|Un brin d'herbe colle au cuir.",
        "narrateur|Le seau et le manteau restent un peu plus loin.",
    ],
    2: [
        "narrateur|Mila a choisi le seau.",
        "narrateur|Le seau jaune a du sable.",
        "narrateur|L'anse est un peu froide.",
        "maman|C'est ton seau, Mila.",
        "enfant-f|Il est jaune.",
        "enfant-f|Comme le citron.",
        "papa|Tu mets le citron dedans ?",
        "narrateur|Elle le pose au fond.",
        "narrateur|Le citron fait un petit toc.",
        "maman|Il voyage dans le seau.",
        "narrateur|Le manteau rouge reste encore sur le banc.",
    ],
    3: [
        "narrateur|Mila a choisi le doudou.",
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Un peu de sable est dessus.",
        "maman|Il t'attendait, Mila.",
        "enfant-f|Il est doux.",
        "papa|Le citron peut s'asseoir contre lui.",
        "narrateur|Elle les serre tous les deux.",
        "enfant-f|Ils viennent.",
        "maman|Oui.",
        "narrateur|L'oreille du doudou est chaude.",
        "narrateur|Le seau reste un peu plus loin.",
    ],
}

L2_EXTRA_017 = {
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

IMG_017 = {
    (1, 1, 1): "Un grain rouge colle au sac bleu.",
    (1, 1, 2): "Le ballon laisse une trace au sac rouge.",
    (1, 1, 3): "Un brin d'herbe reste au sac vert.",
    (1, 2, 1): "Du sable fin brille dans le sac bleu.",
    (1, 2, 2): "L'anse jaune touche le sac rouge.",
    (1, 2, 3): "Un coquillage minuscule roule au sac vert.",
    (1, 3, 1): "L'oreille grise dépasse du sac bleu.",
    (1, 3, 2): "Le doudou sent encore le sable, au sac rouge.",
    (1, 3, 3): "Un fil gris pend du sac vert.",
    (2, 1, 1): "La feuille jaune colle au sac bleu.",
    (2, 1, 2): "Le ballon est un peu froid, près du sac rouge.",
    (2, 1, 3): "Une goutte glisse vers le sac vert.",
    (2, 2, 1): "Le seau sonne tout doux contre le sac bleu.",
    (2, 2, 2): "Le métal du toboggan se tait, près du sac rouge.",
    (2, 2, 3): "Un pas sur la rampe, puis le sac vert.",
    (2, 3, 1): "Le doudou a vu le toboggan, dans le sac bleu.",
    (2, 3, 2): "L'oreille molle dépasse du sac rouge.",
    (2, 3, 3): "La rampe brille encore, loin du sac vert.",
    (3, 1, 1): "La chaîne a fait cling, près du sac bleu.",
    (3, 1, 2): "Le ballon a touché le sable, près du sac rouge.",
    (3, 1, 3): "Un nuage passe au-dessus du sac vert.",
    (3, 2, 1): "L'anse du seau est froide, contre le sac bleu.",
    (3, 2, 2): "Un cling lointain, et le sac rouge.",
    (3, 2, 3): "Le seau jaune pose son ombre au sac vert.",
    (3, 3, 1): "Le doudou a senti le vent, dans le sac bleu.",
    (3, 3, 2): "La chaîne se tait, près du sac rouge.",
    (3, 3, 3): "L'oreille grise dépasse du sac vert.",
}

FIN_017 = {
    (1, 1, 1): "Le citron reprend sa place dans le bol bleu.",
    (1, 1, 2): "Le plaid tricoté retrouve le creux du canapé.",
    (1, 1, 3): "Un grain de sable reste dans la coupelle.",
    (1, 2, 1): "Le seau jaune sèche sous le portemanteau.",
    (1, 2, 2): "Le bol bleu attend encore le citron.",
    (1, 2, 3): "La poussière ne danse plus, dans le salon.",
    (1, 3, 1): "Le doudou s'installe dans le creux du canapé.",
    (1, 3, 2): "Le citron luit, tout seul, dans le bol.",
    (1, 3, 3): "L'horloge fait toc, puis toc, tout calme.",
    (2, 1, 1): "Le manteau rouge retrouve le fauteuil.",
    (2, 1, 2): "Une feuille sèche près des clés de papa.",
    (2, 1, 3): "Le citron a encore l'odeur du vent.",
    (2, 2, 1): "Le seau penche un peu, sous le portemanteau.",
    (2, 2, 2): "Le plaid a glissé, puis Mila le remet.",
    (2, 2, 3): "La rampe du toboggan reste loin, maintenant.",
    (2, 3, 1): "L'oreille du doudou dépasse du fauteuil.",
    (2, 3, 2): "Le citron est lisse, un peu froid encore.",
    (2, 3, 3): "Le rayon d'après-midi a bougé, sur le tapis.",
    (3, 1, 1): "Le ballon s'endort près du canapé.",
    (3, 1, 2): "Le creux du canapé attend Mila.",
    (3, 1, 3): "Ça sent encore le citron, un peu.",
    (3, 2, 1): "Le seau pose son ombre sur le tapis.",
    (3, 2, 2): "Le plaid tricoté est chaud, sur les genoux.",
    (3, 2, 3): "Les clés de papa restent dans la coupelle.",
    (3, 3, 1): "Le doudou a l'odeur de l'herbe, au salon.",
    (3, 3, 2): "Le citron rentre dans le bol bleu.",
    (3, 3, 3): "Le canapé a de nouveau son creux.",
}


def build_017() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    qf: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|Le canapé du salon a encore un creux.",
        "narrateur|Le plaid tricoté a glissé par terre.",
        "narrateur|Un bol bleu tient un citron, tout rond.",
        "narrateur|L'horloge fait toc, puis toc.",
        "narrateur|Un rayon d'après-midi traverse la pièce.",
        "narrateur|La poussière danse, toute lente.",
        "narrateur|Ça sent le citron, un peu.",
        "narrateur|Sous le portemanteau, un seau jaune attend.",
        "narrateur|Un manteau rouge est plié sur le fauteuil.",
        "narrateur|Les clés de papa sont dans une coupelle.",
        "maman|Mila, le parc est tout calme.",
        "maman|On peut y aller un moment.",
        "enfant-f|Je veux le citron.",
        "enfant-f|Je l'emmène au parc.",
        "papa|Le citron est dans le bol bleu.",
        "papa|Tu le prends ?",
        "narrateur|En ce moment, Mila se lève.",
        "narrateur|Ses pieds touchent le tapis épais.",
        "narrateur|Elle prend le citron, tout rond.",
        "narrateur|Il est lisse, un peu froid.",
        "enfant-f|Il est jaune, comme le seau.",
        "maman|Le seau est sous le portemanteau.",
        "papa|Le manteau est sur le fauteuil.",
        "narrateur|Mila pose le citron un instant.",
        "narrateur|Elle prend le seau jaune.",
        "narrateur|Elle prend le manteau rouge.",
        "enfant-f|J'ai le citron.",
        "maman|On y va ?",
        "enfant-f|Oui.",
        "narrateur|Le plaid reste par terre, un moment.",
    ]
    sons["CHK_T0000_P0000"] = ""

    s["CHK_T0001_P0000"] = [
        "papa|Le parc a trois coins.",
        "maman|Où va-t-on d'abord ?",
        "narrateur|Le bac à sable.",
        "narrateur|Le toboggan.",
        "narrateur|Ou les balançoires.",
    ]
    sons["CHK_T0001_P0000"] = "enfants_parc"

    for i, loc in L1_017.items():
        s[f"CHK_T0001_P000{i}"] = L1_BODY_017[i]
        sons[f"CHK_T0001_P000{i}"] = "enfants_parc"
        s[f"CHK_T0001_P000{i}_Q0001"] = Q_017[i]
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        qf[f"CHK_T0001_P000{i}_Q0001"] = {
            "expected_answer": "reprendre",
            "accepted_examples": "reprendre | ses affaires | elle reprend | avant de partir | le seau | le manteau",
            "retry_prompt": "Elle reprend le seau. Mila fait quoi ?",
        }
        s[f"CHK_T0001_P000{i}_C0001"] = C_017[i]
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        s[f"CHK_T0001_P000{i}_T0002_P0000"] = [
            "maman|Tu emportes quel jeu ?",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Ou le doudou.",
        ]
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""

        for j, jeu in L2_017.items():
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            extra = L2_EXTRA_017[(i, j)]
            s[cid2] = L2_BODY_017[j] + [
                f"narrateur|{extra}",
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[cid2] = ""
            s[f"{cid2}_T0003_P0000"] = [
                "papa|Quel sac, pour les affaires ?",
                "narrateur|Le sac Tom.",
                "narrateur|Le sac Léa.",
                "narrateur|Ou le sac Sami.",
            ]
            sons[f"{cid2}_T0003_P0000"] = ""

            for k, sac in L3_017.items():
                cid3 = f"{cid2}_T0003_P000{k}"
                img = IMG_017[(i, j, k)]
                fin = FIN_017[(i, j, k)]
                oublie = {
                    1: [
                        "narrateur|Le ballon est dans ses bras.",
                        "narrateur|Le seau est encore là.",
                    ],
                    2: [
                        "narrateur|Le seau est dans ses mains.",
                        "narrateur|Le manteau est encore là.",
                    ],
                    3: [
                        "narrateur|Le doudou est contre elle.",
                        "narrateur|Le seau est encore là.",
                    ],
                }[j]
                s[cid3] = [
                    "narrateur|C'est l'heure de rentrer.",
                    f"narrateur|Mila quitte {loc['lab']}.",
                    *oublie,
                    "enfant-f|J'ai le citron.",
                    "papa|Attends, Mila.",
                    "papa|On cherche encore un peu.",
                    f"narrateur|Ils vont vers {sac['sac']}.",
                    f"narrateur|Le sac est {sac['coul']}, accroché à la barrière.",
                    "maman|On met le manteau.",
                    "maman|On met le seau.",
                    "narrateur|Mila cherche le manteau rouge.",
                    "narrateur|Elle le met dans le sac.",
                    "papa|Et le seau, ma grande.",
                    "narrateur|Elle cherche le seau jaune.",
                    "narrateur|Elle le prend à deux mains.",
                    f"enfant-f|{sac['lab']}.",
                    "maman|Oui, il tient.",
                    f"narrateur|{jeu['un'].capitalize()} vient aussi.",
                    "narrateur|Le citron glisse tout contre.",
                    "papa|Merci, Mila.",
                    f"narrateur|{img}",
                    "enfant-f|On rentre.",
                    "maman|Oui.",
                    "maman|On rentre ensemble.",
                ]
                sons[cid3] = ""
                s[f"{cid3}_F0001"] = [
                    "narrateur|Le canapé du salon a encore un creux.",
                    f"narrateur|Mila a joué {loc['ici']}.",
                    f"narrateur|Elle a choisi {jeu['lab']}.",
                    f"narrateur|Elle a repris ses affaires dans {sac['sac']}.",
                    "narrateur|Le seau et le manteau sont avec elle.",
                    "narrateur|Elle pose le citron dans le bol bleu.",
                    "enfant-f|Il est rentré.",
                    "maman|Oui.",
                    "papa|Le plaid, Mila ?",
                    "narrateur|Elle ramasse le plaid tricoté.",
                    "narrateur|Elle le pose dans le creux.",
                    f"narrateur|{img}",
                    f"narrateur|{fin}",
                ]
                sons[f"{cid3}_F0001"] = ""
    return s, sons, qf


def main() -> None:
    s, sons, qf = build_016()
    write_story(
        "TREE-AUT-016",
        (
            "Raphaël veut la flaque. Le vent est froid. Une manche du manteau "
            "de laine est à l'envers. Il le met. Ils passent par la cuisine, "
            "le jardin ou la chambre, avec un jeu. Ils rentrent. Le manteau "
            "goutte au crochet. Le radiateur fait tic tic."
        ),
        "Le manteau de laine de Raphaël",
        "Raphaël, papa, maman",
        "salon sous la pluie, puis cuisine, jardin ou chambre",
        s,
        sons,
        qf,
        allow_sac=False,
    )

    s, sons, qf = build_017()
    write_story(
        "TREE-AUT-017",
        (
            "Mila veut emmener le citron du bol bleu au parc. Elle joue. "
            "Au moment de rentrer, le seau et le manteau sont encore là. "
            "Elle les reprend dans un sac. Le citron rentre dans le bol. "
            "Le plaid retrouve le creux du canapé."
        ),
        "Le citron dans le bol bleu",
        "Mila, papa, maman",
        "salon, puis parc",
        s,
        sons,
        qf,
        allow_sac=True,
    )


if __name__ == "__main__":
    main()
