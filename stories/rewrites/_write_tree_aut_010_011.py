#!/usr/bin/env python3
"""TREE-AUT-010 / TREE-AUT-011 — récit implicite, graphe 86 nœuds conservé."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    BAD_NAMES,
    FORBIDDEN,
    LIMITS,
    OPENING_BAD,
    ROLES,
    ROOT,
    _listy_run,
    from_script,
    words,
)

TROUPE = {
    "Amir",
    "Aniss",
    "Sarah",
    "Chouchou",
    "Mila",
    "Nino",
    "Nina",
    "Raphaël",
    "Victorino",
    "Victorina",
}
# Libellés du graphe (sacs / boutons), pas des enfants extra.
GRAPH_LABELS = {"Tom", "Léa", "Sami"}
SKIP_NAMES = GRAPH_LABELS | {
    "Papa",
    "Maman",
    "Oui",
    "Non",
    "Bravo",
    "Merci",
    "Bonjour",
    "Dehors",
    "Ou",
    "Ma",
    "Ta",
    "Loin",
    "Voilà",
    "Voila",
    "Comme",
    "Ainsi",
    "Alors",
    "Donc",
    "Puis",
    "Ensuite",
    "Après",
    "Avant",
    "Avec",
    "Sans",
    "Sous",
    "Sur",
    "Dans",
    "Chez",
    "Vers",
    "Près",
    "Pres",
    "Entre",
    "Pendant",
    "Depuis",
    "Parmi",
    "Selon",
    "Malgré",
    "Sauf",
    "Hormis",
    "Voici",
    "Voilà",
    "Tiens",
    "Attends",
    "Regarde",
    "Écoute",
    "Ecoute",
    "Donne",
    "Prends",
    "Viens",
    "Vas",
    "Va",
    "Allez",
    "Allons",
    "Reste",
    "Restons",
    "Là",
    "La",
    "Ici",
    "Maintenant",
    "Bientôt",
    "Toujours",
    "Jamais",
    "Encore",
    "Déjà",
    "Deja",
    "Souvent",
    "Parfois",
    "Soudain",
    "Enfin",
    "Puisque",
    "Lorsque",
    "Quand",
    "Comme",
    "Si",
    "Mais",
    "Car",
    "Or",
    "Ni",
    "Et",
    "Ou",
    "Donc",
    "Au",
    "Aux",
    "Du",
    "Des",
    "Le",
    "La",
    "Les",
    "Un",
    "Une",
    "Ce",
    "Cet",
    "Cette",
    "Ces",
    "Mon",
    "Ma",
    "Mes",
    "Ton",
    "Ta",
    "Tes",
    "Son",
    "Sa",
    "Ses",
    "Notre",
    "Nos",
    "Votre",
    "Vos",
    "Leur",
    "Leurs",
    "Je",
    "Tu",
    "Il",
    "Elle",
    "On",
    "Nous",
    "Vous",
    "Ils",
    "Elles",
    "Moi",
    "Toi",
    "Lui",
    "Eux",
    "Ça",
    "Ca",
    "Cela",
    "Celui",
    "Celle",
    "Ceux",
    "Celles",
    "Tout",
    "Toute",
    "Tous",
    "Toutes",
    "Rien",
    "Personne",
    "Quelque",
    "Quelques",
    "Plusieurs",
    "Chaque",
    "Autre",
    "Autres",
    "Même",
    "Meme",
    "Tel",
    "Telle",
    "Plus",
    "Moins",
    "Très",
    "Tres",
    "Bien",
    "Mal",
    "Bon",
    "Bonne",
    "Beau",
    "Belle",
    "Petit",
    "Petite",
    "Grand",
    "Grande",
    "Gros",
    "Grosse",
    "Long",
    "Longue",
    "Court",
    "Courte",
    "Haut",
    "Haute",
    "Bas",
    "Basse",
    "Nouveau",
    "Nouvelle",
    "Vieux",
    "Vieille",
    "Jeune",
    "Premier",
    "Première",
    "Dernier",
    "Dernière",
    "Seul",
    "Seule",
    "Seul",
    "Deux",
    "Trois",
    "Quatre",
    "Cinq",
    "Six",
    "Sept",
    "Huit",
    "Neuf",
    "Dix",
    "Midi",
    "Soir",
    "Matin",
    "Minuit",
    "Aujourd",
    "Demain",
    "Hier",
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Aout",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
    "Printemps",
    "Été",
    "Ete",
    "Automne",
    "Hiver",
    "Nord",
    "Sud",
    "Est",
    "Ouest",
    "France",
    "Paris",
    "Doudou",
    "Arrêt",
    "Terminus",
    "Cargaison",
    "Maîtresse",
    "Maitresse",
    "Malaise",
    "Daccord",
    "Sarah",
    "Chouchou",
    "L",
    "D",
    "C",
    "S",
    "N",
    "Qu",
    "Que",
    "Qui",
    "Quoi",
    "Dont",
    "Où",
    "Ou",
    "Comment",
    "Pourquoi",
    "Combien",
    "Quel",
    "Quelle",
    "Quels",
    "Quelles",
    "Lequel",
    "Laquelle",
    "Alors",
    "Comme",
    "Ainsi",
    "Pour",
    "Parce",
    "Aussi",
    "En",
    "De",
}


def apply_chunk(src: dict, lines: list[str]) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    if nc.get("sons") is None:
        nc["sons"] = ""
    return nc


def write_story(sid: str, meta: dict, scripts: dict[str, list[str]]) -> dict:
    folder = ROOT / sid
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in scripts]
    extra = sorted(set(scripts) - {c["chunk_id"] for c in source["chunks"]})
    if missing or extra:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={extra[:8]}")
    chunks = [apply_chunk(c, scripts[c["chunk_id"]]) for c in source["chunks"]]
    merged = dict(source)
    merged.update(meta)
    merged["chunks"] = chunks
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return merged


def path_ids(i: int, j: int, k: int) -> list[str]:
    return [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        f"CHK_T0001_P000{i}",
        f"CHK_T0001_P000{i}_Q0001",
        f"CHK_T0001_P000{i}_C0001",
        f"CHK_T0001_P000{i}_T0002_P0000",
        f"CHK_T0001_P000{i}_T0002_P000{j}",
        f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
        f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
        f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
    ]


def check_story(data: dict, needles: list[str], labels: tuple[dict, dict, dict]) -> None:
    sid = data["story_id"]
    lim = LIMITS[data["age_band"]]
    errors: list[str] = []
    by = {c["chunk_id"]: c for c in data["chunks"]}
    if len(data["chunks"]) != 86:
        errors.append(f"n_chunks={len(data['chunks'])}")
    joined = "\n".join(c["script"] for c in data["chunks"])
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            errors.append(f"interdit: {bad}")
    skip_bad = set(BAD_NAMES) - {"tom ", "léa", "lea "}
    for name in skip_bad:
        if name in low:
            errors.append(f"prénom hors troupe: {name}")
    if "hugo" in low or "jules" in low:
        errors.append("prénom source non remplacé")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        errors.append("aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        errors.append("pas de merci/bravo adulte")
    if not any("?" in a for a in adults):
        errors.append("aucune question d'adulte")
    if "papa|" not in joined or "maman|" not in joined:
        errors.append("il faut papa et maman")
    if "en ce moment" not in low:
        errors.append("manque en ce moment")
    first = data["chunks"][0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in OPENING_BAD:
        if bad in first:
            errors.append(f"ouverture brutale: {first}")
    listed = _listy_run(joined)
    if listed:
        errors.append(f"puces « {listed} »")
    for c in data["chunks"]:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            errors.append(f"{c['chunk_id']} text≠script")
        if (c.get("text_ssml") or "") != c["text"]:
            errors.append(f"{c['chunk_id']} ssml≠text")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                errors.append(f"{c['chunk_id']} sans |")
                continue
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                errors.append(f"{c['chunk_id']} rôle {role}")
            n = words(phrase)
            if n > lim:
                errors.append(f"{c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                errors.append(f"{c['chunk_id']} vide")
            if not phrase.endswith((".", "?", "!")):
                errors.append(f"{c['chunk_id']} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                errors.append(f"{c['chunk_id']} plusieurs phrases: {phrase}")
        blob = c["text"]
        for name in re.findall(r"\b([A-ZÉÈÊÀÂÎÔÙÛÇ][a-zéèêàâîôùûçëïü]+)\b", blob):
            if name in SKIP_NAMES or name in TROUPE:
                continue
            errors.append(f"{c['chunk_id']} nom hors troupe: {name}")
        if c["kind"] == "passage_fin":
            last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
            if not last_n:
                errors.append(f"{c['chunk_id']} fin sans narrateur")
            else:
                last = last_n[-1].split("|", 1)[1].lower()
                if "histoire" in last or "bravo" in last or "bon travail" in last:
                    errors.append(f"{c['chunk_id']} fin mécanique: {last}")
    l1, l2, l3 = labels
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                pth = path_ids(i, j, k)
                blob = " ".join(by[cid]["text"] for cid in pth)
                n = words(blob)
                if n < 350:
                    errors.append(f"path {i}{j}{k} trop court {n}")
                for needle in needles + [l1[i], l2[j], l3[k]]:
                    if needle.lower() not in blob.lower():
                        errors.append(f"path {i}{j}{k} manque {needle}")
    src = json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))
    for a, b in zip(src["chunks"], data["chunks"]):
        if a["chunk_id"] != b["chunk_id"] or a["kind"] != b["kind"]:
            errors.append(f"graphe cassé {a['chunk_id']}")
        for k in ("option_1_label", "option_2_label", "option_3_label"):
            if a.get(k) != b.get(k):
                errors.append(f"{a['chunk_id']} {k} changé")
        if a.get("expected_answer") != b.get("expected_answer"):
            errors.append(f"{a['chunk_id']} expected_answer changé")
    if errors:
        raise SystemExit(f"{sid} {len(errors)} erreurs:\n- " + "\n- ".join(errors[:40]))
    debut = data["chunks"][0]["script"].splitlines()[0].split("|", 1)[1]
    print(f"OK {sid} 1re: {debut}")


# ---------------------------------------------------------------------------
# TREE-AUT-010  N3  AUT.AFF.002  Chouchou, manteau jaune, gouttière
# L1 bac / toboggan / balançoires
# L2 ballon / seau / doudou
# L3 Tom / Léa / Sami  (sacs cousus, graphe inchangé)
# ---------------------------------------------------------------------------

L1_010 = {1: "le bac à sable", 2: "le toboggan", 3: "les balançoires"}
L2_010 = {1: "le ballon", 2: "le seau", 3: "le doudou"}
L3_010 = {1: "Tom", 2: "Léa", 3: "Sami"}
L3_SAC_010 = {
    1: {"qui": "Tom", "sac": "le sac Tom", "coul": "bleu"},
    2: {"qui": "Léa", "sac": "le sac Léa", "coul": "rouge"},
    3: {"qui": "Sami", "sac": "le sac Sami", "coul": "vert"},
}

IMG_010 = {
    (1, 1, 1): "La feuille brille sur le sac bleu, près du sable.",
    (1, 1, 2): "Une goutte du ballon glisse vers le sac rouge.",
    (1, 1, 3): "Un grain de sable colle au sac vert.",
    (1, 2, 1): "L'anse du seau touche le sac bleu.",
    (1, 2, 2): "Du sable fin brille dans le sac rouge.",
    (1, 2, 3): "Le seau pose son ombre sur le sac vert.",
    (1, 3, 1): "L'oreille du doudou dépasse du sac bleu.",
    (1, 3, 2): "Un fil gris pend du sac rouge.",
    (1, 3, 3): "Le doudou sent encore le sable, au sac vert.",
    (2, 1, 1): "La feuille jaune colle au sac bleu, sous la rampe.",
    (2, 1, 2): "Le ballon est un peu froid, près du sac rouge.",
    (2, 1, 3): "Une goutte de la rampe va vers le sac vert.",
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


def debut_010() -> list[str]:
    return [
        "narrateur|Dehors, la gouttière fait tic, tic, tic.",
        "narrateur|Une feuille mouillée colle au seuil.",
        "narrateur|Elle brille, toute plate.",
        "narrateur|L'air frais passe sous la porte.",
        "narrateur|Ça sent la terre humide.",
        "narrateur|Sur le crochet, un manteau jaune attend.",
        "narrateur|Une goutte tremble sur le capuchon.",
        "maman|Tu as vu la feuille, Chouchou ?",
        "enfant-f|Elle brille, maman.",
        "papa|On peut l'emmener au parc.",
        "enfant-f|Je veux la feuille au parc.",
        "narrateur|Papa noue une chaussure, lentement.",
        "narrateur|La goutte tombe sur le poignet de Chouchou.",
        "enfant-f|Elle est froide !",
        "maman|Le manteau jaune est tout prêt.",
        "narrateur|En ce moment, Chouchou prend le manteau.",
        "narrateur|Un bras, puis l'autre bras.",
        "narrateur|Le tissu est chaud, un peu lourd.",
        "papa|La feuille rentre dans la poche ?",
        "enfant-f|Oui, papa.",
        "narrateur|La feuille glisse, tout mouillée.",
        "maman|On ouvre la porte ?",
        "enfant-f|Oui, on va au parc.",
        "papa|Le chemin de l'école est encore frais.",
        "narrateur|La gouttière fait tic, encore.",
        "maman|Merci, Chouchou.",
        "maman|Tu as pris la feuille.",
        "narrateur|Le manteau jaune touche ses genoux.",
    ]


def l1_010(i: int) -> list[str]:
    if i == 1:
        return [
            "narrateur|Chouchou marche vers le bac à sable.",
            "narrateur|Le manteau jaune est sur ses épaules.",
            "narrateur|Le sable est froid, un peu rugueux.",
            "narrateur|Une flaque brille au milieu.",
            "enfant-f|Ma feuille peut flotter.",
            "papa|Tout doux, près de nous.",
            "narrateur|Chouchou sort la feuille de la poche.",
            "narrateur|Elle la pose sur l'eau, plate.",
            "narrateur|La feuille part, tout lentement.",
            "maman|Elle avance, tu vois ?",
            "enfant-f|Oui, elle est brillante.",
            "narrateur|Un peu de sable colle à la manche.",
            "papa|Le manteau te tient chaud ?",
            "enfant-f|Oui, papa, il est lourd.",
            "narrateur|Chouchou reprend la feuille, mouillée.",
            "narrateur|Elle la glisse dans la poche.",
            "maman|La poche fait un petit bruit.",
        ]
    if i == 2:
        return [
            "narrateur|Chouchou va vers le toboggan.",
            "narrateur|Le manteau jaune fait un bruit de tissu.",
            "narrateur|L'échelle est fraîche sous les mains.",
            "narrateur|Une feuille d'arbre colle à la rampe.",
            "papa|Tu montes, Chouchou, doucement.",
            "enfant-f|Je monte, papa.",
            "narrateur|Les marches font tic, tic.",
            "maman|Ta feuille est encore dans la poche ?",
            "enfant-f|Oui, elle est molle.",
            "narrateur|Chouchou glisse, le manteau gonfle.",
            "narrateur|Le vent est doux, un peu humide.",
            "papa|Tu as chaud, là-dedans ?",
            "enfant-f|Oui, le tissu est chaud.",
            "narrateur|Au bas, elle touche le capuchon.",
            "maman|Une goutte a suivi la rampe.",
            "narrateur|La goutte roule sur le jaune.",
        ]
    return [
        "narrateur|Chouchou va vers les balançoires.",
        "narrateur|Le sol est froid sous les chaussures.",
        "narrateur|Une chaîne fait un petit cling.",
        "narrateur|Elle est froide dans la main.",
        "maman|Tu te tiens bien, Chouchou ?",
        "enfant-f|Oui, maman, cling.",
        "narrateur|Chouchou s'assoit, le bois est lisse.",
        "papa|La feuille reste dans la poche ?",
        "enfant-f|Elle bouge, papa.",
        "narrateur|La poche tape, tout doux, contre la hanche.",
        "maman|Le manteau te tient au chaud ?",
        "enfant-f|Oui, il est jaune et chaud.",
        "narrateur|Un nuage passe, tout lent.",
        "narrateur|La chaîne se tait un peu.",
        "papa|On reste près de toi.",
        "narrateur|Le capuchon tapote le dos.",
    ]


def q_010(i: int) -> list[str]:
    ou = {1: "au bac à sable", 2: "au toboggan", 3: "aux balançoires"}[i]
    return [
        f"narrateur|Chouchou est {ou}.",
        "narrateur|Que porte-t-elle, dehors ?",
    ]


def c_010(i: int) -> list[str]:
    echo = {
        1: "La feuille a flotté, tout plat.",
        2: "La rampe est encore froide.",
        3: "La chaîne a fait cling.",
    }[i]
    return [
        "narrateur|Chouchou touche le col du manteau.",
        "enfant-f|Il est jaune et chaud.",
        "maman|Oui, tu l'as enfilé près de la gouttière.",
        "papa|La feuille est dans la poche ?",
        "enfant-f|Oui, papa, elle est molle.",
        f"narrateur|{echo}",
        "maman|On continue un peu ?",
        "enfant-f|Oui, maman.",
        "narrateur|Le manteau reste sur ses épaules.",
    ]


def l2_010(i: int, j: int) -> list[str]:
    echo = {
        1: "Le sable reste aux genoux.",
        2: "La rampe est encore froide.",
        3: "La chaîne fait un petit cling.",
    }[i]
    if j == 1:
        return [
            "narrateur|Chouchou a choisi le ballon.",
            "narrateur|Un ballon rouge attend, tout lisse.",
            "narrateur|Il est un peu froid, un peu mouillé.",
            "enfant-f|Le ballon, papa !",
            "papa|On le garde près de nous.",
            "narrateur|Chouchou pousse le ballon du pied.",
            "narrateur|La feuille sort un peu de la poche.",
            "narrateur|Elle colle au ballon, toute plate.",
            "maman|C'est ta feuille, tu vois ?",
            "enfant-f|Elle a voyagé !",
            "narrateur|Chouchou la décolle, tout doux.",
            "narrateur|Elle la remet dans la poche.",
            "papa|Le manteau a une manche mouillée.",
            "enfant-f|C'est le ballon.",
            f"narrateur|{echo}",
        ]
    if j == 2:
        return [
            "narrateur|Chouchou a choisi le seau.",
            "narrateur|Un seau jaune attend, l'anse froide.",
            "narrateur|Un peu d'eau tremble au fond.",
            "enfant-f|Je mets la feuille dedans.",
            "maman|Comme un bateau, Chouchou ?",
            "enfant-f|Oui, un tout petit bateau.",
            "narrateur|La feuille tourne dans le seau.",
            "narrateur|L'eau touche le bord, tout fin.",
            "papa|Tu la reprends après ?",
            "enfant-f|Oui, elle est à moi.",
            "narrateur|Chouchou sort la feuille, goutte à goutte.",
            "narrateur|Une goutte tombe sur le manteau jaune.",
            "maman|Le tissu devient plus foncé, juste là.",
            "enfant-f|C'est rien, il me tient chaud.",
            f"narrateur|{echo}",
        ]
    return [
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Il était dans l'autre poche.",
        "maman|Il t'attendait, Chouchou.",
        "enfant-f|Il est doux.",
        "narrateur|Chouchou sort la feuille, et le doudou.",
        "narrateur|La feuille colle à l'oreille grise.",
        "papa|Ils voyagent ensemble ?",
        "enfant-f|Oui, tous les deux.",
        "narrateur|Elle les serre contre le manteau.",
        "narrateur|Le jaune devient un nid, tout chaud.",
        "maman|L'oreille est un peu humide.",
        "enfant-f|C'est la feuille.",
        "papa|On les garde près de toi.",
        f"narrateur|{echo}",
    ]


def l3_010(i: int, j: int, k: int) -> list[str]:
    loc = L1_010[i]
    obj = L2_010[j]
    sac = L3_SAC_010[k]
    img = IMG_010[(i, j, k)]
    return [
        f"narrateur|Chouchou va vers {sac['sac']}.",
        f"narrateur|Le sac est {sac['coul']}, accroché à la barrière.",
        "narrateur|Le nom est cousu, tout simple.",
        f"enfant-f|{sac['qui']}.",
        "papa|C'est l'heure, Chouchou.",
        "maman|Le chemin rentre vers la maison.",
        f"narrateur|Elle a joué, vers {loc}.",
        f"narrateur|Elle a pris {obj}.",
        "narrateur|Le manteau jaune est lourd de pluie.",
        "enfant-f|Il est mouillé, maman.",
        "maman|On le raccroche, à la maison.",
        f"papa|Tu poses la feuille près du sac {sac['qui']} ?",
        "enfant-f|Une seconde, pour montrer.",
        f"narrateur|{img}",
        "narrateur|Puis la feuille rentre dans la poche.",
    ]


def fin_010(i: int, j: int, k: int) -> list[str]:
    loc = L1_010[i]
    obj = L2_010[j]
    sac = L3_SAC_010[k]
    img = IMG_010[(i, j, k)]
    return [
        "narrateur|La gouttière fait tic, encore, près de la porte.",
        "narrateur|Chouchou pousse la porte.",
        "narrateur|Le carrelage est froid sous les pieds.",
        "narrateur|Elle glisse le manteau jaune hors des bras.",
        "narrateur|Elle le raccroche au crochet.",
        "narrateur|Une goutte tombe du capuchon.",
        "enfant-f|Il sèche, maintenant.",
        "maman|Oui, tout doux.",
        "papa|La feuille ?",
        "narrateur|Chouchou la pose sur le rebord.",
        "narrateur|Elle brille encore, moins mouillée.",
        f"narrateur|Au parc, il y avait {loc}.",
        f"narrateur|Elle revoit {obj}, tout doux.",
        f"narrateur|{img}",
        f"narrateur|Loin, {sac['sac']} reste à la barrière.",
        "narrateur|Le crochet tient le jaune, tout calme.",
    ]


def build_010() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = debut_010()
    s["CHK_T0001_P0000"] = [
        "narrateur|On peut aller au bac à sable.",
        "narrateur|On peut aller au toboggan.",
        "narrateur|Ou aux balançoires.",
    ]
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = l1_010(i)
        s[f"{p}_Q0001"] = q_010(i)
        s[f"{p}_C0001"] = c_010(i)
        s[f"{p}_T0002_P0000"] = [
            "narrateur|On peut prendre le ballon.",
            "narrateur|On peut prendre le seau.",
            "narrateur|Ou le doudou.",
        ]
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = l2_010(i, j)
            s[f"{p2}_T0003_P0000"] = [
                "narrateur|On peut aller vers Tom.",
                "narrateur|On peut aller vers Léa.",
                "narrateur|Ou vers Sami.",
            ]
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_010(i, j, k)
                s[f"{p3}_F0001"] = fin_010(i, j, k)
    return s


# ---------------------------------------------------------------------------
# TREE-AUT-011  N1  AUT.AFF.003  Sarah, seau jaune, ferme toit rouge
# L1 cubes / livre / dînette
# L2 pomme / yaourt / pain
# L3 chat / chien / poule
# ---------------------------------------------------------------------------

L1_011 = {1: "les cubes", 2: "le livre", 3: "la dînette"}
L2_011 = {1: "une pomme", 2: "un yaourt", 3: "un morceau de pain"}
L3_011 = {1: "le chat", 2: "le chien", 3: "la poule"}

TROUVE_011 = {
    1: "près des cubes, sur le banc",
    2: "sous la paille, près du livre",
    3: "près des tasses, à l'étable",
}

IMG_011 = {
    (1, 1, 1): "Un cube jaune reste près du chat.",
    (1, 1, 2): "Le trognon sent la pomme, près du chien.",
    (1, 1, 3): "Un cube rouge brille près de la poule.",
    (1, 2, 1): "Une cuillère de yaourt sèche près du chat.",
    (1, 2, 2): "Le pot vide penche vers le chien.",
    (1, 2, 3): "Un peu de yaourt, près de la poule.",
    (1, 3, 1): "Une miette colle au cube, près du chat.",
    (1, 3, 2): "Le pain tiède sent, près du chien.",
    (1, 3, 3): "Une miette attend la poule.",
    (2, 1, 1): "La page de la pomme reste près du chat.",
    (2, 1, 2): "Le livre sent la pomme, près du chien.",
    (2, 1, 3): "Une image de poule, et la vraie poule.",
    (2, 2, 1): "Une page un peu collante, près du chat.",
    (2, 2, 2): "Le yaourt a taché le livre, près du chien.",
    (2, 2, 3): "La page blanche, et la poule.",
    (2, 3, 1): "Une miette sur la page, près du chat.",
    (2, 3, 2): "Le livre sent le pain, près du chien.",
    (2, 3, 3): "La poule du livre, et la poule du toit.",
    (3, 1, 1): "La tasse a un jus de pomme, près du chat.",
    (3, 1, 2): "Sarah a servi le chien, pour de rire.",
    (3, 1, 3): "La tasse attend la poule.",
    (3, 2, 1): "Le yaourt a fait le lait, près du chat.",
    (3, 2, 2): "La petite cuillère, près du chien.",
    (3, 2, 3): "Un pot vide, et la poule.",
    (3, 3, 1): "Une miette dans la tasse, près du chat.",
    (3, 3, 2): "Le pain a servi, près du chien.",
    (3, 3, 3): "La tasse sent le foin, près de la poule.",
}


def debut_011() -> list[str]:
    return [
        "narrateur|La paille sent le soleil.",
        "narrateur|Elle craque sous les bottes.",
        "narrateur|La ferme a un toit rouge.",
        "narrateur|Des gouttes brillent sur l'herbe.",
        "papa|On pousse le portail, Sarah.",
        "narrateur|Le portail fait criiic.",
        "maman|Tu as entendu le coq ?",
        "enfant-f|Oui, maman.",
        "narrateur|Le coq chante tout près.",
        "narrateur|Ça sent le foin chaud.",
        "narrateur|Maman tient un panier.",
        "narrateur|Papa pose la main sur le bois.",
        "narrateur|Le bois du banc est rêche.",
        "narrateur|En ce moment, Sarah arrive.",
        "narrateur|Elle porte un manteau bleu.",
        "narrateur|Elle tient un seau jaune.",
        "enfant-f|Je veux porter de l'eau.",
        "enfant-f|Avec le seau, papa.",
        "papa|On joue un peu, d'accord ?",
        "enfant-f|Oui, papa.",
        "enfant-f|Puis l'eau aux bêtes.",
        "narrateur|Sarah pose le seau près du banc.",
        "narrateur|Elle pose le manteau sur le bois.",
        "maman|Ils restent ici ?",
        "enfant-f|Oui, maman.",
        "narrateur|Une poule picore au loin.",
        "narrateur|Le vent passe dans l'herbe.",
        "narrateur|Le toit rouge brille un peu.",
        "papa|Tu as vu le seau ?",
        "enfant-f|Il est jaune, papa.",
        "maman|Le manteau est au chaud.",
        "maman|Merci, Sarah.",
    ]


def l1_011(i: int) -> list[str]:
    if i == 1:
        return [
            "narrateur|Sarah va vers les cubes.",
            "narrateur|Ils sont sur le banc de bois.",
            "narrateur|Un cube est rouge.",
            "narrateur|Un cube est bleu.",
            "narrateur|Un cube est jaune, comme le seau.",
            "enfant-f|Je les empile, papa.",
            "papa|Tu poses le rouge en bas.",
            "narrateur|Sarah pose le cube rouge.",
            "narrateur|Le bois sent le sapin.",
            "maman|Le bleu va dessus ?",
            "enfant-f|Oui, maman.",
            "narrateur|La tour est petite et ferme.",
            "papa|Le seau est encore là.",
            "maman|Le manteau aussi, sur le bois.",
            "enfant-f|Après, je prends l'eau.",
            "narrateur|Sarah touche le cube jaune.",
        ]
    if i == 2:
        return [
            "narrateur|Sarah va vers le livre.",
            "narrateur|Il est sur une botte de paille.",
            "narrateur|La paille pique un peu.",
            "narrateur|Sarah s'assoit près de papa.",
            "papa|On ouvre le livre ?",
            "enfant-f|Oui, il y a une poule.",
            "narrateur|Les pages font chh, chh.",
            "maman|Tu vois le toit rouge ?",
            "enfant-f|Comme la ferme.",
            "narrateur|Une image montre un seau.",
            "papa|Comme ton seau jaune.",
            "maman|Et un manteau, sur un banc.",
            "enfant-f|Le mien est sur le bois.",
            "narrateur|Sarah pose la main sur la page.",
            "narrateur|Le livre sent le papier chaud.",
            "papa|Le seau attend, tout près.",
        ]
    return [
        "narrateur|Sarah va vers la dînette.",
        "narrateur|De petites tasses en bois.",
        "narrateur|Elles sont près de l'étable.",
        "enfant-f|Je sers le lait, maman.",
        "maman|Tu sers papa d'abord ?",
        "papa|Merci, Sarah.",
        "papa|C'est tiède.",
        "narrateur|Sarah fait mine de verser.",
        "narrateur|Ça sent encore le foin.",
        "enfant-f|Après, le seau pour de vrai.",
        "maman|Oui, il est sur le banc.",
        "papa|Le manteau bleu aussi.",
        "narrateur|Sarah pose une tasse près d'elle.",
        "narrateur|Le bois de la tasse est lisse.",
        "maman|Les bêtes attendent un peu.",
        "enfant-f|Je vais y aller.",
    ]


def q_011(i: int) -> list[str]:
    jeu = {1: "les cubes", 2: "le livre", 3: "la dînette"}[i]
    return [
        f"narrateur|Sarah a joué avec {jeu}.",
        "narrateur|Avant de partir, que reprend-on ?",
    ]


def c_011(i: int) -> list[str]:
    ou = TROUVE_011[i]
    return [
        "narrateur|Sarah regarde vers le banc.",
        "papa|Le seau jaune est encore là.",
        "maman|Le manteau bleu aussi.",
        f"narrateur|Ils attendent {ou}.",
        "enfant-f|Après, je les prends.",
        "papa|Oui, pour l'eau des bêtes.",
        "maman|On goûte un peu, d'abord ?",
        "enfant-f|Oui, maman.",
        "narrateur|Le toit rouge reste au-dessus.",
    ]


def l2_011(i: int, j: int) -> list[str]:
    echo = {
        1: "Un cube jaune brille près d'elle.",
        2: "Le livre reste sur la paille.",
        3: "Une tasse attend près de l'étable.",
    }[i]
    if j == 1:
        return [
            "narrateur|Sarah a choisi une pomme.",
            "narrateur|Elle est rouge, bien ronde.",
            "maman|Tu la prends dans le panier ?",
            "enfant-f|Oui, elle est froide.",
            "narrateur|Sarah croque un tout petit bout.",
            "narrateur|Ça fait croque.",
            "papa|C'est juteux, hein ?",
            "enfant-f|Oui, papa.",
            "enfant-f|C'est doux.",
            "maman|Tu as fini ta bouchée ?",
            "narrateur|Sarah essuie ses doigts.",
            "papa|Le seau est encore au banc.",
            f"narrateur|{echo}",
            "narrateur|Le jus brille sur sa lèvre.",
        ]
    if j == 2:
        return [
            "narrateur|Sarah a choisi un yaourt.",
            "narrateur|Le pot est frais dans la main.",
            "papa|Une petite cuillère, voilà.",
            "enfant-f|Il est blanc, maman.",
            "narrateur|Sarah prend une cuillerée.",
            "narrateur|Ça sent le lait froid.",
            "maman|C'est bon ?",
            "enfant-f|Oui, c'est doux.",
            "narrateur|Une goutte reste au bord.",
            "papa|Tu essuies, tout doux.",
            "narrateur|Sarah passe le doigt.",
            "maman|Le manteau bleu attend.",
            f"narrateur|{echo}",
            "narrateur|Le pot vide penche un peu.",
        ]
    return [
        "narrateur|Sarah a choisi un morceau de pain.",
        "narrateur|Il est encore un peu tiède.",
        "maman|Il sent le four, tu vois ?",
        "enfant-f|Oui, il est doux.",
        "narrateur|Sarah croque, ça fait croûte.",
        "papa|Une miette tombe sur la paille.",
        "enfant-f|Pour les bêtes, après.",
        "maman|Avec le seau jaune ?",
        "enfant-f|Oui, l'eau et le pain.",
        "narrateur|Sarah garde une miette.",
        "narrateur|Elle la serre dans la main.",
        "papa|Le seau est au banc, encore.",
        f"narrateur|{echo}",
        "narrateur|Le pain tiède sent le blé.",
    ]


def animal_011(k: int) -> list[str]:
    if k == 1:
        return [
            "narrateur|Sarah rejoint le chat.",
            "narrateur|Il est gris, près du foin.",
            "narrateur|Il ronronne, tout bas.",
            "enfant-f|Il est chaud, maman.",
            "maman|Tu le caresses doucement ?",
            "narrateur|Le chat se frotte au banc.",
        ]
    if k == 2:
        return [
            "narrateur|Sarah rejoint le chien.",
            "narrateur|Il a le poil un peu rêche.",
            "narrateur|Sa queue tapote l'herbe.",
            "enfant-f|Il est grand, papa.",
            "papa|Tu dis bonjour, tout doux.",
            "narrateur|Le chien souffle, tout chaud.",
        ]
    return [
        "narrateur|Sarah rejoint la poule.",
        "narrateur|Elle picore près du toit rouge.",
        "narrateur|Ses plumes sont sèches.",
        "enfant-f|Elle fait cot cot.",
        "maman|Tout doux, près d'elle.",
        "narrateur|La poule penche la tête.",
    ]


def l3_011(i: int, j: int, k: int) -> list[str]:
    ou = TROUVE_011[i]
    snack = {1: "la pomme", 2: "le yaourt", 3: "le pain"}[j]
    bête = {1: "le chat", 2: "le chien", 3: "la poule"}[k]
    img = IMG_011[(i, j, k)]
    eau = {
        1: "un peu d'eau pour le chat",
        2: "un peu d'eau pour le chien",
        3: "un peu d'eau pour la poule",
    }[k]
    return animal_011(k) + [
        f"enfant-f|Je veux {eau}.",
        "papa|Le seau, alors.",
        "narrateur|Sarah cherche, les mains vides.",
        f"maman|Il est {ou}.",
        "narrateur|Sarah va, et elle cherche.",
        "narrateur|Elle trouve le seau jaune.",
        "enfant-f|Je le prends.",
        "maman|Le manteau bleu aussi.",
        "narrateur|Sarah le prend et le serre.",
        f"narrateur|{snack.capitalize()} reste au panier.",
        f"narrateur|{img}",
        f"papa|{bête.capitalize()} t'attend.",
    ]


def fin_011(i: int, j: int, k: int) -> list[str]:
    jeu = L1_011[i]
    snack = L2_011[j]
    bête = L3_011[k]
    img = IMG_011[(i, j, k)]
    return [
        "narrateur|Sarah tient le seau jaune.",
        "narrateur|Un peu d'eau tremble au fond.",
        f"narrateur|Elle pose l'eau { {1: 'près du chat', 2: 'près du chien', 3: 'près de la poule'}[k] }.",
        "enfant-f|Voilà, c'est pour toi.",
        "maman|Merci, Sarah.",
        "narrateur|Elle tient le manteau bleu.",
        "papa|On rentre, tu as tes affaires.",
        f"narrateur|Elle a joué avec {jeu}.",
        f"narrateur|Elle a goûté {snack}.",
        f"narrateur|{img}",
        "narrateur|Le portail fait criiic encore.",
        "narrateur|La paille colle à une botte.",
        "narrateur|Le toit rouge reste derrière.",
        "enfant-f|Le seau est avec moi.",
        "narrateur|Le manteau bleu aussi, contre elle.",
    ]


def build_011() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = debut_011()
    s["CHK_T0001_P0000"] = [
        "narrateur|Sarah peut prendre les cubes.",
        "narrateur|Elle peut prendre le livre.",
        "narrateur|Elle peut prendre la dînette.",
    ]
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = l1_011(i)
        s[f"{p}_Q0001"] = q_011(i)
        s[f"{p}_C0001"] = c_011(i)
        s[f"{p}_T0002_P0000"] = [
            "narrateur|On goûte un peu ?",
            "narrateur|Sarah peut prendre une pomme.",
            "narrateur|Elle peut prendre un yaourt.",
            "narrateur|Elle peut prendre un morceau de pain.",
        ]
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = l2_011(i, j)
            s[f"{p2}_T0003_P0000"] = [
                "narrateur|On dit bonjour à un animal ?",
                "narrateur|Sarah peut aller vers le chat.",
                "narrateur|Elle peut aller vers le chien.",
                "narrateur|Elle peut aller vers la poule.",
            ]
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_011(i, j, k)
                s[f"{p3}_F0001"] = fin_011(i, j, k)
    return s


def main() -> None:
    m010 = write_story(
        "TREE-AUT-010",
        {
            "fil_rouge": (
                "Chouchou veut emmener la feuille brillante au parc. "
                "Une goutte froide tombe. Elle enfile le manteau jaune. "
                "Elle joue, puis elle raccroche le manteau mouillé."
            ),
            "title": "Le manteau jaune de Chouchou",
            "characters": "Chouchou, papa, maman",
            "setting": "chemin de l'école, parc après la pluie",
        },
        build_010(),
    )
    check_story(
        m010,
        ["Chouchou", "manteau", "feuille", "gouttière"],
        (L1_010, L2_010, L3_010),
    )

    m011 = write_story(
        "TREE-AUT-011",
        {
            "fil_rouge": (
                "Sarah veut porter de l'eau aux bêtes avec le seau jaune. "
                "Elle pose le seau et le manteau. "
                "Avant de rentrer, elle les reprend."
            ),
            "title": "Le seau jaune de Sarah",
            "characters": "Sarah, papa, maman",
            "setting": "à la ferme, toit rouge, paille",
        },
        build_011(),
    )
    check_story(
        m011,
        ["Sarah", "seau", "paille", "toit"],
        (L1_011, L2_011, L3_011),
    )

    for data, l1, l2, l3 in (
        (m010, L1_010, L2_010, L3_010),
        (m011, L1_011, L2_011, L3_011),
    ):
        print(f"\n== {data['story_id']}  {data['title']}")
        print("opening:", data["chunks"][0]["script"].splitlines()[0].split("|", 1)[1])
        print("L1:", ", ".join(l1[i] for i in (1, 2, 3)))
        print("L2:", ", ".join(l2[i] for i in (1, 2, 3)))
        print("L3:", ", ".join(l3[i] for i in (1, 2, 3)))


if __name__ == "__main__":
    main()
