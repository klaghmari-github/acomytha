#!/usr/bin/env python3
"""Réécrit le CHILD_AUDIO des arbres SAN (graphe inchangé). Fichier temporaire."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAN = ROOT / "ramifiees" / "SAN"
LECONS = json.loads((ROOT / "referentiel" / "lecons.json").read_text(encoding="utf-8"))
BY_ID = {l["lesson_id"]: l for l in LECONS["lessons"]}

KEYS = list("ABC")
SUBS = "123"
ENDS = "XYZ"


def apply_spec(data: dict, spec: dict) -> None:
    n = data["nodes"]
    n["root"]["text"] = spec["root"]
    n["ch1"]["prompt"] = spec["ch1_prompt"]
    for i, lab in enumerate(spec["ch1_labels"]):
        n["ch1"]["options"][i]["label"] = lab
    for key, br in zip(KEYS, spec["branches"]):
        n[f"br{key}"]["text"] = br["audio"]
        q = n[f"q{key}"]
        q["prompt"] = br["q_prompt"]
        q["retry_prompt"] = br["retry"]
        q["positive_feedback"] = br["pos"]
        q["wrong_feedback"] = br["wrong"]
        if br.get("examples"):
            q["accepted_examples"] = br["examples"]
        n[f"fb{key}"]["text"] = br["fb"]
        n[f"ch2{key}"]["prompt"] = br["ch2_prompt"]
        for i, lab in enumerate(br["ch2_labels"]):
            n[f"ch2{key}"]["options"][i]["label"] = lab
        for j, sub in zip(SUBS, br["subs"]):
            n[f"br{key}{j}"]["text"] = sub["audio"]
            n[f"ch3{key}{j}"]["prompt"] = sub["ch3_prompt"]
            for i, lab in enumerate(sub["ch3_labels"]):
                n[f"ch3{key}{j}"]["options"][i]["label"] = lab
            for e, text in zip(ENDS, sub["ends"]):
                n[f"end{key}{j}{e}"]["text"] = text
    data["validation"] = {
        "status": "PENDING",
        "blocking_findings": 0,
        "major_findings": 0,
        "paths_tested": 27,
    }


def cover_ok(data: dict) -> list[str]:
    lesson = BY_ID[data["lesson_id"]]
    req = lesson.get("required_messages") or []
    nodes = data["nodes"]

    def collect(node):
        parts = [
            node.get("text") or "",
            node.get("prompt") or "",
            node.get("retry_prompt") or "",
            node.get("positive_feedback") or "",
            node.get("wrong_feedback") or "",
        ]
        for opt in node.get("options") or []:
            parts.append(opt.get("label") or "")
        return " ".join(parts)

    def norm(s):
        return (s or "").lower().replace("’", "'")

    def path_ok(ids):
        ptxt = norm(" ".join(collect(nodes[i]) for i in ids if i in nodes))
        missing = []
        for m in req:
            tokens = [t for t in re.split(r"[;/]", m) if t.strip()]
            ok = False
            for t in tokens:
                t = t.strip().lower()
                if len(t) < 3:
                    continue
                words = [
                    w
                    for w in re.findall(r"[a-zàâäéèêëïîôùûüçœ-]{3,}", t)
                    if w not in ("une", "des", "les", "est", "avec", "pour", "dans")
                ]

                def stem(w):
                    for suf in ("er", "ir", "ez", "ent", "ons", "ait", "é", "ée", "és", "ées"):
                        if w.endswith(suf) and len(w) > len(suf) + 2:
                            return w[: -len(suf)]
                    return w

                if words and all(stem(w) in ptxt or w in ptxt for w in words[:2]):
                    ok = True
                    break
                if t in ptxt:
                    ok = True
                    break
            if tokens and not ok:
                missing.append(m)
        return missing

    # enumerate 27 choice paths
    misses = []
    for a, ka in enumerate(KEYS):
        for b, jb in enumerate(SUBS):
            for c, ec in enumerate(ENDS):
                ids = [
                    "root",
                    "ch1",
                    f"br{ka}",
                    f"q{ka}",
                    f"fb{ka}",
                    f"ch2{ka}",
                    f"br{ka}{jb}",
                    f"ch3{ka}{jb}",
                    f"end{ka}{jb}{ec}",
                ]
                missing = path_ok(ids)
                if missing:
                    misses.append(f"{ka}{jb}{ec}: {missing}")
    return misses


def n1_long(data: dict) -> list[str]:
    if data.get("age_band") != "N1":
        return []
    hits = []
    for v in data["nodes"].values():
        if v.get("type") in ("audio", "feedback", "ending", "transition"):
            for sent in re.split(r"[.!?]+", v.get("text") or ""):
                sent = sent.strip()
                if not sent:
                    continue
                wc = len(sent.split())
                if wc > 14:
                    hits.append(f"{v.get('id')} ({wc}): {sent[:80]}")
    return hits


SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# TREE-SAN-001 N1 Lina — goûter un légume à la maison
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-001"] = {
    "root": (
        "C'est l'heure de manger. Lina a faim. "
        "Maman est dans la cuisine. Papa est là aussi. "
        "Dans l'assiette, il y a un légume. "
        "Maman dit : tu peux goûter. Une petite portion. "
        "Puis tu nommes le goût. Lina écoute."
    ),
    "ch1_prompt": "Lina goûte où ? La cuisine, le jardin, ou la chambre ?",
    "ch1_labels": ["la cuisine", "le jardin", "la chambre"],
    "branches": [
        {
            "audio": (
                "Lina entre dans la cuisine. Ça sent la soupe. "
                "Elle s'assoit à table, près de maman. "
                "Une carotte orange est dans l'assiette. "
                "Maman dit : goûte une petite portion. "
                "Lina prend une petite bouchée. C'est un peu sucré. "
                "Lina nomme le goût : c'est sucré, maman."
            ),
            "q_prompt": "Lina prend une petite bouchée. Que fait-elle ?",
            "retry": "Elle goûte. Une petite portion. Que fait Lina ?",
            "pos": "Oui. Elle goûte une petite portion. Elle nomme le goût.",
            "wrong": "On goûte une petite portion. On nomme le goût à papa ou maman.",
            "examples": ["goûter", "une bouchée", "petite bouchée", "le goût", "elle goûte"],
            "fb": (
                "Lina a goûté. Elle a nommé le goût. "
                "Une petite portion, c'est bien. Maman sourit."
            ),
            "ch2_prompt": "Quel légume maintenant ? La carotte, le petit pois, ou la courgette ?",
            "ch2_labels": ["la carotte", "le petit pois", "la courgette"],
            "subs": [
                {
                    "audio": (
                        "Maman coupe un tout petit bout de carotte. "
                        "Lina goûte une petite portion. C'est croquant. "
                        "Elle nomme le goût : sucré. Papa dit : merci d'avoir goûté."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom s'assoit près de Lina. Lina dit : la carotte est sucrée. Elle a goûté une petite portion. Elle a nommé le goût. Tom tapote la table. Ils rient. L'histoire est finie.",
                        "Léa écoute. Lina dit : c'est sucré. Elle a goûté une petite portion. Elle nomme le goût. Léa sourit. Maman verse de l'eau. L'histoire est finie.",
                        "Sami regarde la carotte orange. Lina dit : j'ai goûté. C'est sucré. Une petite portion. Elle nomme le goût. Sami dit merci à maman. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa pose un petit pois vert. Il est tout rond. "
                        "Lina goûte une petite portion. C'est doux. "
                        "Elle nomme le goût : doux. Maman dit : une petite bouchée, c'est assez."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom compte : un petit pois. Lina goûte. Elle nomme le goût : doux. Une petite portion. Tom applaudit tout doux. L'histoire est finie.",
                        "Léa chuchote : c'est petit. Lina goûte une petite portion. Elle nomme le goût. Léa goûte aussi, si elle veut. Maman est là. L'histoire est finie.",
                        "Sami rit : c'est rond. Lina a goûté. Elle a nommé le goût. Une petite portion. Sami range sa cuillère. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman donne un cube de courgette. Il est tendre. "
                        "Lina goûte une petite portion. C'est doux, un peu tiède. "
                        "Elle nomme le goût à maman. Papa hoche la tête."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom dit : c'est vert. Lina dit : c'est doux. Elle a goûté une petite portion. Elle a nommé le goût. Ils restent à table. L'histoire est finie.",
                        "Léa touche l'assiette, tout doux. Lina goûte. Elle nomme le goût. Une petite portion. Léa dit : merci maman. L'histoire est finie.",
                        "Sami souffle sur le cube. Lina goûte une petite portion. Elle nomme le goût : doux. Sami pose sa serviette. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Lina va au jardin avec maman. Le soleil est chaud. "
                "Une petite tomate rouge brille. Maman la lave. "
                "Maman dit : goûte une petite portion. "
                "Lina croque un tout petit bout. C'est juteux. "
                "Elle nomme le goût : c'est juteux, maman."
            ),
            "q_prompt": "Lina goûte la tomate. Que fait-elle ?",
            "retry": "Une petite portion. Puis elle nomme le goût. Que fait Lina ?",
            "pos": "Oui. Elle goûte une petite portion. Elle nomme le goût.",
            "wrong": "On goûte une petite portion. On nomme le goût à papa ou maman.",
            "examples": ["goûter", "une bouchée", "petite bouchée", "le goût", "elle goûte"],
            "fb": (
                "Lina a goûté au jardin. Elle a nommé le goût. "
                "Une petite portion, c'est déjà bien."
            ),
            "ch2_prompt": "Que cueille Lina ? La tomate, le radis, ou la salade ?",
            "ch2_labels": ["la tomate", "le radis", "la salade"],
            "subs": [
                {
                    "audio": (
                        "Lina cueille une tomate cerise. Papa est près du bac. "
                        "Elle goûte une petite portion. C'est chaud du soleil. "
                        "Elle nomme le goût : sucré et juteux."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom sent la tomate. Lina dit : c'est sucré. Elle a goûté une petite portion. Elle nomme le goût. Une abeille passe loin. L'histoire est finie.",
                        "Léa s'assoit dans l'herbe. Lina goûte. Elle nomme le goût. Une petite portion. Léa dit : c'est rouge. L'histoire est finie.",
                        "Sami tient l'arrosoir. Lina a goûté. Elle a nommé le goût. Une petite portion. Ils rentrent avec maman. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman tire un petit radis. Il pique un peu le nez. "
                        "Lina goûte une petite portion. C'est vif. "
                        "Elle nomme le goût : un peu piquant. Papa rit doucement."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom ouvre les yeux grand. Lina dit : ça pique un peu. Elle a goûté une petite portion. Elle nomme le goût. Tom dit : merci. L'histoire est finie.",
                        "Léa boit une gorgée d'eau. Lina a goûté. Elle a nommé le goût. Une petite portion. Léa s'essuie la bouche. L'histoire est finie.",
                        "Sami sent le radis. Lina goûte une petite portion. Elle nomme le goût. Sami range le panier. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa cueille une feuille de salade. Elle est fraîche. "
                        "Lina goûte une petite portion. C'est croquant. "
                        "Elle nomme le goût : frais. Maman dit : bien dit."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom touche la feuille. Lina dit : c'est frais. Elle a goûté une petite portion. Elle nomme le goût. Le vent est doux. L'histoire est finie.",
                        "Léa met la feuille dans le panier. Lina a goûté. Elle a nommé le goût. Une petite portion. Elles marchent vers la maison. L'histoire est finie.",
                        "Sami écoute. Lina goûte une petite portion. Elle nomme le goût : croquant. Sami dit : moi aussi, une petite bouchée. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Lina est dans sa chambre. Maman apporte un petit plateau. "
                "Il y a un bâtonnet de concombre. "
                "Maman dit : tu peux goûter une petite portion. "
                "Lina croque. C'est froid et frais. "
                "Elle nomme le goût : c'est frais, maman."
            ),
            "q_prompt": "Lina nomme le goût. Que fait-elle ?",
            "retry": "Elle goûte une petite portion. Que fait Lina ?",
            "pos": "Oui. Elle goûte une petite portion. Elle nomme le goût.",
            "wrong": "On goûte une petite portion. On nomme le goût à papa ou maman.",
            "examples": ["goûter", "une bouchée", "petite bouchée", "le goût", "nommer"],
            "fb": (
                "Même dans la chambre, Lina a goûté. "
                "Elle a nommé le goût. Une petite portion suffit."
            ),
            "ch2_prompt": "Que goûte Lina ? Le concombre, le poivron, ou le maïs ?",
            "ch2_labels": ["le concombre", "le poivron", "le maïs"],
            "subs": [
                {
                    "audio": (
                        "Le concombre est froid. Lina goûte une petite portion. "
                        "Ça croque. Elle nomme le goût : frais. "
                        "Papa pose le doudou à côté, tout sage."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom s'assoit sur le tapis. Lina dit : c'est frais. Elle a goûté une petite portion. Elle nomme le goût. Tom pose le plateau. L'histoire est finie.",
                        "Léa tient le doudou. Lina goûte. Elle nomme le goût. Une petite portion. Léa dit : c'est vert. L'histoire est finie.",
                        "Sami écoute près de la fenêtre. Lina a goûté. Elle a nommé le goût. Une petite portion. Ils rangent le plateau. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman offre un tout petit morceau de poivron. Il est rouge. "
                        "Lina goûte une petite portion. C'est un peu sucré. "
                        "Elle nomme le goût. Papa dit : tu as dit le goût. Merci."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom dit : c'est rouge. Lina dit : c'est sucré. Elle a goûté une petite portion. Elle nomme le goût. Ils sourient. L'histoire est finie.",
                        "Léa sent le poivron. Lina goûte une petite portion. Elle nomme le goût. Léa tapote le doudou. L'histoire est finie.",
                        "Sami chuchote. Lina a goûté. Elle a nommé le goût. Une petite portion. Sami dit merci à papa. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa montre un grain de maïs. Il est jaune. "
                        "Lina goûte une petite portion. C'est doux. "
                        "Elle nomme le goût : doux. Maman dit : une petite bouchée, c'est bien."
                    ),
                    "ch3_prompt": "Lina dit le goût à qui ? Tom, Léa, ou Sami ?",
                    "ch3_labels": ["Tom", "Léa", "Sami"],
                    "ends": [
                        "Tom rit : c'est jaune. Lina goûte. Elle nomme le goût. Une petite portion. Tom range le grain. L'histoire est finie.",
                        "Léa s'allonge un peu. Lina a goûté une petite portion. Elle a nommé le goût. Léa dit : c'est doux. L'histoire est finie.",
                        "Sami pose le plateau. Lina a goûté. Elle nomme le goût. Une petite portion. Maman baisse le store. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-002 N2 Nora — s'asseoir pour manger dans la cuisine
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-002"] = {
    "root": (
        "C'est l'heure du déjeuner. Nora a faim. "
        "Papa pose les assiettes. Maman apporte le pain. "
        "On mange assis à table, ensemble. "
        "Nora va choisir sa place. Les fesses sur la chaise."
    ),
    "ch1_prompt": "Nora s'assoit où ? Près de papa, près de maman, ou à sa petite chaise ?",
    "ch1_labels": ["près de papa", "près de maman", "sa petite chaise"],
    "branches": [
        {
            "audio": (
                "Nora tire la chaise près de papa. La chaise fait un petit bruit. "
                "Elle pose les fesses sur la chaise. Elle est assise. "
                "Papa s'assoit aussi. Maman s'assoit en face. "
                "Ils sont ensemble à table. Nora prend sa cuillère. Elle reste assise."
            ),
            "q_prompt": "Nora va manger. Que fait-elle ?",
            "retry": "Elle pose les fesses sur la chaise. À table. Que fait Nora ?",
            "pos": "Oui. Elle s'assoit à table. Ils mangent ensemble.",
            "wrong": "On s'assoit à table. On pose les fesses sur la chaise. On mange ensemble.",
            "examples": ["assise", "s'asseoir", "à table", "ensemble", "sur la chaise"],
            "fb": (
                "Nora est assise. La table est stable. "
                "Papa, maman et Nora mangent ensemble."
            ),
            "ch2_prompt": "Que mange Nora, assise ? La soupe, le pain, ou le fromage ?",
            "ch2_labels": ["la soupe", "le pain", "le fromage"],
            "subs": [
                {
                    "audio": (
                        "Papa souffle un peu sur la soupe. Nora reste assise. "
                        "Elle mange à table, ensemble. La cuillère va, la cuillère vient. "
                        "Maman dit : on est assis. C'est calme."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "L'assiette bleue est devant Nora. Elle est assise à table. Ils mangent la soupe ensemble. Nora dit merci. L'histoire est finie.",
                        "L'assiette rouge brille. Nora reste assise. À table, ensemble, la soupe est tiède. Papa sourit. L'histoire est finie.",
                        "L'assiette verte est ronde. Nora est assise. Ils mangent ensemble à table. Maman essuie une goutte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman casse le pain. Nora est assise. "
                        "Elle attend, les fesses sur la chaise. "
                        "Puis elle mange le pain à table, ensemble. Ça sent bon."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "Nora pose le pain dans l'assiette bleue. Elle est assise à table, ensemble. Le pain croque. L'histoire est finie.",
                        "L'assiette rouge attend le pain. Nora reste assise. Ils mangent ensemble à table. Papa dit : bravo. L'histoire est finie.",
                        "L'assiette verte est près de maman. Nora est assise. À table, ensemble, elle mange son morceau. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa coupe un petit bout de fromage. Nora est assise. "
                        "Elle mange à table, ensemble. Le fromage est doux. "
                        "Maman dit : on reste assis jusqu'à la fin."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "Le fromage est dans l'assiette bleue. Nora est assise à table. Ils mangent ensemble. Puis ils rangent. L'histoire est finie.",
                        "L'assiette rouge sent le fromage. Nora reste assise. Ensemble, à table, c'est calme. L'histoire est finie.",
                        "L'assiette verte attend. Nora est assise. Ils mangent ensemble à table. Nora dit : j'étais assise. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Nora choisit la chaise près de maman. La nappe est douce. "
                "Elle s'assoit. Les fesses sur la chaise. "
                "Maman s'assoit à côté. Papa en face. "
                "Ils mangent ensemble à table. Nora tient sa fourchette. Elle reste assise."
            ),
            "q_prompt": "Nora est près de maman. Que fait-elle pour manger ?",
            "retry": "Assise, à table, ensemble. Que fait Nora ?",
            "pos": "Oui. Elle s'assoit à table. Ils mangent ensemble.",
            "wrong": "On s'assoit à table. On pose les fesses sur la chaise. On mange ensemble.",
            "examples": ["assise", "s'asseoir", "à table", "ensemble", "sur la chaise"],
            "fb": (
                "Près de maman, Nora est assise. "
                "La table les tient ensemble."
            ),
            "ch2_prompt": "Que mange Nora, assise ? La soupe, le pain, ou le fromage ?",
            "ch2_labels": ["la soupe", "le pain", "le fromage"],
            "subs": [
                {
                    "audio": (
                        "Maman goûte la soupe. Nora est assise à côté. "
                        "Elle mange à table, ensemble. Une goutte tombe. Maman l'essuie. "
                        "Nora reste sur sa chaise."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "L'assiette bleue fume un peu. Nora est assise à table, ensemble. Elle souffle. L'histoire est finie.",
                        "L'assiette rouge est près de maman. Nora reste assise. Ils mangent ensemble à table. L'histoire est finie.",
                        "L'assiette verte attend la cuillère. Nora est assise. Ensemble, à table, c'est bon. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa passe le panier. Nora, assise, prend un morceau. "
                        "Elle mange le pain à table, ensemble. "
                        "Maman dit : les fesses sur la chaise."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "Le pain est sur l'assiette bleue. Nora est assise à table. Ils mangent ensemble. Des miettes. On les ramasse. L'histoire est finie.",
                        "L'assiette rouge a des miettes. Nora reste assise. Ensemble, à table, elle mange. L'histoire est finie.",
                        "L'assiette verte est propre. Nora est assise. Ils mangent le pain ensemble à table. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman pose le fromage. Nora est assise. "
                        "Elle attend son tour, à table, ensemble. "
                        "Puis elle mange. Papa dit : on est tous assis."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "L'assiette bleue a un petit bout. Nora est assise à table, ensemble. Elle dit merci. L'histoire est finie.",
                        "L'assiette rouge sent bon. Nora reste assise. Ils mangent ensemble à table. L'histoire est finie.",
                        "L'assiette verte est au milieu. Nora est assise. À table, ensemble, le repas se termine. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Nora a sa petite chaise, juste à sa taille. "
                "Elle s'assoit. Les fesses bien posées. "
                "Papa et maman s'assoient aussi. "
                "Ils mangent ensemble à table. Nora dit : je suis assise. Maman sourit."
            ),
            "q_prompt": "Nora a sa petite chaise. Que fait-elle ?",
            "retry": "Les fesses sur la chaise. À table. Ensemble. Que fait Nora ?",
            "pos": "Oui. Elle s'assoit à table. Ils mangent ensemble.",
            "wrong": "On s'assoit à table. On pose les fesses sur la chaise. On mange ensemble.",
            "examples": ["assise", "s'asseoir", "à table", "ensemble", "petite chaise"],
            "fb": (
                "La petite chaise est stable. Nora est assise. "
                "Toute la famille est ensemble à table."
            ),
            "ch2_prompt": "Que mange Nora, assise ? La soupe, le pain, ou le fromage ?",
            "ch2_labels": ["la soupe", "le pain", "le fromage"],
            "subs": [
                {
                    "audio": (
                        "La soupe arrive. Nora, sur sa petite chaise, reste assise. "
                        "Elle mange à table, ensemble. La cuillère est à sa taille."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "L'assiette bleue est petite aussi. Nora est assise à table. Ils mangent ensemble. L'histoire est finie.",
                        "L'assiette rouge va bien avec la chaise. Nora reste assise. Ensemble, à table, elle finit sa cuillère. L'histoire est finie.",
                        "L'assiette verte est ronde. Nora est assise. Ils mangent ensemble à table. Papa range. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Nora, assise, rompt un peu de pain. "
                        "Elle mange à table, ensemble. "
                        "Sa petite chaise ne bouge pas. Maman dit : bien."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "Le pain rejoint l'assiette bleue. Nora est assise à table, ensemble. Une miette tombe. Elle la pose. L'histoire est finie.",
                        "L'assiette rouge attend. Nora reste assise. Ils mangent le pain ensemble à table. L'histoire est finie.",
                        "L'assiette verte a une miette. Nora est assise. À table, ensemble, c'est fini. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa glisse un bout de fromage. Nora est assise. "
                        "Elle mange à table, ensemble. "
                        "Elle reste jusqu'au bout, sur sa petite chaise."
                    ),
                    "ch3_prompt": "Quelle assiette ? Bleue, rouge, ou verte ?",
                    "ch3_labels": ["bleue", "rouge", "verte"],
                    "ends": [
                        "L'assiette bleue est vide, presque. Nora est assise à table. Ils étaient ensemble. L'histoire est finie.",
                        "L'assiette rouge a encore une odeur. Nora reste assise. Ensemble, à table, elle dit merci. L'histoire est finie.",
                        "L'assiette verte rentre dans le placard. Nora était assise. Ils ont mangé ensemble à table. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-003 N2 Maya — boire de l'eau au parc
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-003"] = {
    "root": (
        "Maya joue au parc avec maman. Papa arrive aussi. "
        "Le soleil tape. Maya a soif. Sa bouche est sèche. "
        "Maman a un verre. Dedans, il y a de l'eau. "
        "Quand on a soif, on boit de l'eau dans un verre."
    ),
    "ch1_prompt": "Maya a soif où ? Au bac à sable, au toboggan, ou aux balançoires ?",
    "ch1_labels": ["le bac à sable", "le toboggan", "les balançoires"],
    "branches": [
        {
            "audio": (
                "Maya creuse au bac à sable. Le sable est chaud. "
                "Elle a soif. Maman tend un verre. "
                "Maya boit de l'eau dans le verre. L'eau est fraîche. "
                "Papa dit : quand on a soif, on boit de l'eau."
            ),
            "q_prompt": "Maya a soif. Que boit-elle ?",
            "retry": "Dans un verre. De l'eau. Que prend Maya ?",
            "pos": "Oui. Elle boit de l'eau dans un verre. Elle n'avait plus soif.",
            "wrong": "Quand on a soif, on boit de l'eau dans un verre.",
            "examples": ["eau", "de l'eau", "un verre", "le verre", "j'ai soif"],
            "fb": (
                "Maya a bu. L'eau était dans le verre. "
                "La soif est partie. Elle peut rejouer."
            ),
            "ch2_prompt": "Qui a soif aussi ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom a le sable aux mains. Il a soif aussi. "
                        "Maman verse de l'eau dans un verre. Tom boit. "
                        "Maya dit : l'eau, dans le verre. Quand on a soif."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, le parc est calme. Maya a soif. Elle boit de l'eau dans un verre. Tom aussi. L'histoire est finie.",
                        "Après la sieste, Maya a soif. Elle prend le verre. Elle boit de l'eau. Tom dit : encore un peu. L'histoire est finie.",
                        "Le soir, l'air est plus doux. Maya a soif. Elle boit de l'eau dans un verre. Tom range le seau. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa s'assoit au bord du bac. Elle a soif. "
                        "Papa donne un verre d'eau. Léa boit. "
                        "Maya boit aussi. L'eau coule, fraîche."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa a soif. Maya lui passe le verre. Elles boivent de l'eau. La soif s'en va. L'histoire est finie.",
                        "Après la sieste, Léa bâille. Elle a soif. Maya boit de l'eau dans un verre. Léa aussi. L'histoire est finie.",
                        "Le soir, Léa a encore soif. Maya prend le verre. Elles boivent de l'eau. Maman range. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami a bâti un château. Il a soif. "
                        "Maya lui montre le verre. Sami boit de l'eau. "
                        "Maya dit : j'avais soif. L'eau m'a aidée."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Sami a soif. Maya boit de l'eau dans un verre. Sami aussi. Le château reste. L'histoire est finie.",
                        "Après la sieste, Sami a chaud. Maya a soif. Elle boit de l'eau dans un verre. L'histoire est finie.",
                        "Le soir, Sami range. Maya a soif. Elle boit de l'eau dans un verre. Papa dit : bien. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Maya gravit le petit toboggan. En haut, elle a soif. "
                "Elle redescend. Maman l'attend avec un verre. "
                "Maya boit de l'eau. L'eau glisse, fraîche. "
                "Papa dit : soif, alors un verre d'eau."
            ),
            "q_prompt": "Maya redescend. Que boit-elle ?",
            "retry": "Elle a soif. De l'eau, dans un verre. Que fait Maya ?",
            "pos": "Oui. Elle boit de l'eau dans un verre.",
            "wrong": "Quand on a soif, on boit de l'eau dans un verre.",
            "examples": ["eau", "de l'eau", "un verre", "le verre", "j'ai soif"],
            "fb": (
                "Après le toboggan, Maya a bu. "
                "L'eau était dans le verre. La soif est partie."
            ),
            "ch2_prompt": "Qui boit après Maya ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom glisse aussi. Il a soif. "
                        "Maman remplit le verre d'eau. Tom boit. "
                        "Maya dit : quand on a soif, un verre d'eau."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, le toboggan est frais. Maya a soif. Elle boit de l'eau dans un verre. Tom aussi. L'histoire est finie.",
                        "Après la sieste, Tom a chaud. Maya boit de l'eau dans un verre. La soif s'en va. L'histoire est finie.",
                        "Le soir, ils glissent une dernière fois. Maya a soif. Elle boit de l'eau dans un verre. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa attend en bas. Elle a soif. "
                        "Papa tend le verre d'eau. Léa boit. Maya boit. "
                        "Elles soufflent. Plus soif."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa a soif. Maya lui donne le verre. Elles boivent de l'eau. L'histoire est finie.",
                        "Après la sieste, Léa a les joues chaudes. Maya boit de l'eau dans un verre. Léa aussi. L'histoire est finie.",
                        "Le soir, Léa dit : encore un peu. Maya a soif. Elle boit de l'eau dans un verre. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami tient les montants. Il a soif. "
                        "Maya passe le verre. Sami boit de l'eau. "
                        "Maya dit : l'eau, c'est pour la soif."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Sami a soif. Maya boit de l'eau dans un verre. Ils se tapent dans les mains. L'histoire est finie.",
                        "Après la sieste, Sami a la bouche sèche. Maya a soif. Elle boit de l'eau dans un verre. L'histoire est finie.",
                        "Le soir, Sami range ses chaussures. Maya boit de l'eau dans un verre. La soif est partie. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Maya se balance. L'air bouge. Elle a soif. "
                "Elle s'arrête. Maman est là, avec un verre d'eau. "
                "Maya boit. L'eau est froide. Papa dit : bien. "
                "Quand on a soif, on boit de l'eau dans un verre."
            ),
            "q_prompt": "Maya s'arrête. Que boit-elle ?",
            "retry": "Un verre. De l'eau. Elle avait soif. Que fait Maya ?",
            "pos": "Oui. Elle boit de l'eau dans un verre.",
            "wrong": "Quand on a soif, on boit de l'eau dans un verre.",
            "examples": ["eau", "de l'eau", "un verre", "le verre", "j'ai soif"],
            "fb": (
                "Maya a bu à la balançoire. "
                "L'eau dans le verre a calmé la soif."
            ),
            "ch2_prompt": "Qui se balance et boit ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom se balance tout doux. Il a soif. "
                        "Maman verse de l'eau dans le verre. Tom boit. "
                        "Maya dit : j'avais soif. L'eau, c'est bien."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, la balançoire craque. Maya a soif. Elle boit de l'eau dans un verre. Tom aussi. L'histoire est finie.",
                        "Après la sieste, Tom a soif. Maya boit de l'eau dans un verre. Ils se reposent. L'histoire est finie.",
                        "Le soir, Tom dit : encore. Maya a soif. Elle boit de l'eau dans un verre. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa se balance en face. Elle a soif. "
                        "Papa donne le verre d'eau. Léa boit. Maya boit. "
                        "Elles sourient. Plus de soif."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa a soif. Maya prend le verre. Elles boivent de l'eau. L'histoire est finie.",
                        "Après la sieste, Léa a chaud. Maya a soif. Elle boit de l'eau dans un verre. L'histoire est finie.",
                        "Le soir, Léa range son manteau. Maya boit de l'eau dans un verre. La soif s'en va. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami pousse tout doux. Il a soif. "
                        "Maya lui offre le verre. Sami boit de l'eau. "
                        "Maya dit : soif, alors de l'eau."
                    ),
                    "ch3_prompt": "On boit quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Sami a soif. Maya boit de l'eau dans un verre. Sami aussi. L'histoire est finie.",
                        "Après la sieste, Sami a les lèvres sèches. Maya a soif. Elle boit de l'eau dans un verre. L'histoire est finie.",
                        "Le soir, Sami dit merci. Maya a soif. Elle boit de l'eau dans un verre. Papa range le verre. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-004 N3 Inès — se laver les mains dans le jardin
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-004"] = {
    "root": (
        "Inès joue dans le jardin. Papa est là. Maman arrive avec un panier. "
        "Les mains d'Inès ont de la terre. Bientôt on goûte. "
        "Avant de manger, on lave les mains. Savon et eau. "
        "Après les toilettes, c'est pareil. Savon, puis rincer, puis essuyer."
    ),
    "ch1_prompt": "Inès a joué avec quoi ? Les cubes, le livre, ou la dînette ?",
    "ch1_labels": ["les cubes", "le livre", "la dînette"],
    "branches": [
        {
            "audio": (
                "Inès a construit une tour de cubes, dans l'herbe. "
                "Les cubes ont un peu de terre. Papa dit : on va manger. "
                "Avant de manger, Inès va au robinet du jardin. "
                "Elle ouvre l'eau. Elle prend le savon. Elle frotte. Elle rince. Elle essuie. "
                "Après les toilettes, tout à l'heure, elle avait déjà lavé avec du savon."
            ),
            "q_prompt": "Inès se lave les mains. Avec quoi ?",
            "retry": "Avant de manger. Après les toilettes. Avec du savon. Quoi ?",
            "pos": "Oui. Elle prend le savon. Avant de manger, et après les toilettes.",
            "wrong": "On ouvre l'eau. On prend le savon. Avant de manger, et après les toilettes.",
            "examples": ["savon", "du savon", "les mains", "avant de manger", "après les toilettes"],
            "fb": (
                "Les mains d'Inès sentent le savon. "
                "Avant de manger, c'est fait. Après les toilettes, c'était fait aussi."
            ),
            "ch2_prompt": "On mange quoi, mains propres ? Une pomme, un yaourt, ou du pain ?",
            "ch2_labels": ["une pomme", "un yaourt", "un morceau de pain"],
            "subs": [
                {
                    "audio": (
                        "Maman sort une pomme. Inès a les mains propres. "
                        "Avant de manger, elle a pris le savon. "
                        "Après les toilettes, elle avait fait pareil. "
                        "Elle croque. La pomme est croquante."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat frotte sa tête. Inès a les mains propres. Avant de manger, savon. Après les toilettes, savon. Elle mange sa pomme. L'histoire est finie.",
                        "Le chien s'assoit dans l'herbe. Inès a pris le savon avant de manger. Après les toilettes aussi. La pomme craque. L'histoire est finie.",
                        "La poule picore loin. Inès a les mains savonnées. Avant de manger. Après les toilettes. Elle finit sa pomme. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa ouvre un yaourt. Inès a lavé. "
                        "Savon, avant de manger. Savon, après les toilettes. "
                        "Elle prend sa cuillère. Le yaourt est frais."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat miaule. Inès a les mains propres grâce au savon. Avant de manger. Après les toilettes. Elle mange son yaourt. L'histoire est finie.",
                        "Le chien respire fort. Inès a pris le savon. Avant de manger, après les toilettes. Le yaourt est doux. L'histoire est finie.",
                        "La poule fait cot cot. Inès a lavé au savon. Avant de manger. Après les toilettes. Elle range la cuillère. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman casse le pain. Inès a les mains propres. "
                        "Avant de manger, savon. Après les toilettes, savon. "
                        "Elle mange un morceau. Ça sent le four."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat s'enroule. Inès a pris le savon avant de manger. Après les toilettes aussi. Le pain est bon. L'histoire est finie.",
                        "Le chien pose la tête. Inès a les mains savonnées. Avant de manger. Après les toilettes. Elle dit merci. L'histoire est finie.",
                        "La poule s'éloigne. Inès a lavé. Savon avant de manger. Savon après les toilettes. Elle range le pain. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Inès a lu un livre sur la couverture, au jardin. "
                "Elle va aux toilettes de la maison. Après les toilettes, elle prend le savon. "
                "Eau, savon, rincer, essuyer. "
                "Puis maman dit : avant de manger, on lave encore. Inès reprend le savon."
            ),
            "q_prompt": "Après les toilettes, Inès prend quoi ?",
            "retry": "Savon. Avant de manger aussi. Qu'est-ce qu'elle prend ?",
            "pos": "Oui. Elle prend le savon. Après les toilettes, et avant de manger.",
            "wrong": "Après les toilettes, on prend le savon. Avant de manger, aussi.",
            "examples": ["savon", "du savon", "les mains", "après les toilettes", "avant de manger"],
            "fb": (
                "Le livre attend. Les mains d'Inès sentent le savon. "
                "Après les toilettes, c'est fait. Avant de manger, c'est fait."
            ),
            "ch2_prompt": "On mange quoi, mains propres ? Une pomme, un yaourt, ou du pain ?",
            "ch2_labels": ["une pomme", "un yaourt", "un morceau de pain"],
            "subs": [
                {
                    "audio": (
                        "Inès a fermé le livre. Elle a pris le savon après les toilettes. "
                        "Avant de manger la pomme, elle lave encore. Savon. "
                        "Puis elle croque."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat se couche sur le livre. Inès a le savon sur les mains. Après les toilettes. Avant de manger. La pomme est rouge. L'histoire est finie.",
                        "Le chien écoute l'histoire. Inès a lavé au savon. Après les toilettes, avant de manger. Elle mange sa pomme. L'histoire est finie.",
                        "La poule s'approche du panier. Inès a pris le savon. Après les toilettes. Avant de manger. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Papa pose le yaourt près du livre. "
                        "Inès a le savon après les toilettes. "
                        "Avant de manger, elle frotte encore. Puis elle mange."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat lèche sa patte. Inès a pris le savon. Après les toilettes. Avant de manger. Le yaourt est frais. L'histoire est finie.",
                        "Le chien bâille. Inès a les mains savonnées. Après les toilettes, avant de manger. Elle range le pot. L'histoire est finie.",
                        "La poule picore une miette loin. Inès a lavé au savon. Après les toilettes. Avant de manger. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman pose le pain sur la couverture. "
                        "Inès a lavé après les toilettes, avec du savon. "
                        "Avant de manger, elle lave encore. Puis elle croque."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat s'étire. Inès a le savon. Après les toilettes. Avant de manger. Le pain sent bon. L'histoire est finie.",
                        "Le chien garde le livre. Inès a pris le savon. Après les toilettes, avant de manger. Elle dit merci. L'histoire est finie.",
                        "La poule fait un petit bruit. Inès a lavé. Savon après les toilettes. Savon avant de manger. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Inès a fait la dînette dans le jardin. Petites assiettes. "
                "Maman dit : maintenant, le vrai goûter. "
                "Avant de manger, Inès ouvre l'eau. Elle prend le savon. "
                "Elle se souvient : après les toilettes, le savon aussi. Elle rince. Elle essuie."
            ),
            "q_prompt": "Avant le vrai goûter, Inès prend quoi ?",
            "retry": "Savon. Avant de manger. Après les toilettes aussi. Quoi ?",
            "pos": "Oui. Elle prend le savon. Avant de manger, et après les toilettes.",
            "wrong": "On prend le savon. Avant de manger, et après les toilettes.",
            "examples": ["savon", "du savon", "les mains", "avant de manger", "dînette"],
            "fb": (
                "La dînette est rangée. Les vraies mains sont propres. "
                "Savon avant de manger. Savon après les toilettes."
            ),
            "ch2_prompt": "Le vrai goûter, c'est quoi ? Une pomme, un yaourt, ou du pain ?",
            "ch2_labels": ["une pomme", "un yaourt", "un morceau de pain"],
            "subs": [
                {
                    "audio": (
                        "Inès pose les petites assiettes. Puis elle lave. "
                        "Savon, avant de manger la pomme. "
                        "Après les toilettes, elle savait déjà : savon. Elle croque."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat joue avec une cuillère en bois. Inès a pris le savon. Avant de manger. Après les toilettes. La pomme craque. L'histoire est finie.",
                        "Le chien reste près de papa. Inès a le savon. Avant de manger, après les toilettes. Elle mange sa pomme. L'histoire est finie.",
                        "La poule regarde la dînette. Inès a lavé au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Le yaourt n'est pas en plastique. C'est le vrai. "
                        "Inès a le savon avant de manger. "
                        "Après les toilettes, savon aussi. Elle prend sa cuillère."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat s'assoit droit. Inès a les mains savonnées. Avant de manger. Après les toilettes. Le yaourt est bon. L'histoire est finie.",
                        "Le chien cligne. Inès a pris le savon. Avant de manger, après les toilettes. Elle range. L'histoire est finie.",
                        "La poule s'éloigne. Inès a lavé. Savon avant de manger. Savon après les toilettes. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman donne le vrai pain. Inès a lavé. "
                        "Savon avant de manger. Savon après les toilettes. "
                        "Elle mange. La dînette attend dans la caisse."
                    ),
                    "ch3_prompt": "Qui passe près d'elle ? Le chat, le chien, ou la poule ?",
                    "ch3_labels": ["le chat", "le chien", "la poule"],
                    "ends": [
                        "Le chat ferme les yeux. Inès a pris le savon. Avant de manger. Après les toilettes. Le pain est doux. L'histoire est finie.",
                        "Le chien suit maman. Inès a le savon. Avant de manger, après les toilettes. Elle dit merci. L'histoire est finie.",
                        "La poule retourne au fond. Inès a lavé au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-005 N1 Léa — se brosser les dents (journée d'école)
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-005"] = {
    "root": (
        "Léa a école aujourd'hui. Maman est là. Papa aussi. "
        "Le matin, on prend la brosse. Le soir, on prend la brosse. "
        "Un adulte est avec Léa. C'est maman, ou papa. "
        "Les dents aiment la brosse."
    ),
    "ch1_prompt": "Léa se brosse quand ? Le matin, après la sieste, ou le soir ?",
    "ch1_labels": ["le matin", "après la sieste", "le soir"],
    "branches": [
        {
            "audio": (
                "C'est le matin. Léa se lève. "
                "Maman est dans la salle de bain. Un adulte est là. "
                "Léa prend sa brosse. Elles brossent. En haut. En bas. "
                "Le soir, ce sera pareil. Brosse, avec un adulte."
            ),
            "q_prompt": "Léa se brosse. Avec quoi ?",
            "retry": "Le matin et le soir. Elle prend la brosse. Avec un adulte. Quoi ?",
            "pos": "Oui. Elle prend la brosse. Matin et soir, avec un adulte.",
            "wrong": "On prend la brosse. Matin et soir, avec un adulte.",
            "examples": ["brosse", "la brosse", "matin", "soir", "avec maman"],
            "fb": (
                "Léa a pris la brosse. Le matin, c'est fait. "
                "Le soir, elle la reprendra. Un adulte sera là."
            ),
            "ch2_prompt": "Léa brosse où ? À la cuisine, au jardin, ou à la chambre ?",
            "ch2_labels": ["la cuisine", "le jardin", "la chambre"],
            "subs": [
                {
                    "audio": (
                        "Léa passe par la cuisine. Elle boit une gorgée. "
                        "Puis elle prend la brosse. Maman, l'adulte, brosse avec elle. "
                        "Le matin. Et ce soir, encore la brosse."
                    ),
                    "ch3_prompt": "Léa prend quoi après ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Léa prend le ballon rouge. Ses dents sont brossées. Le matin, la brosse. Le soir, la brosse. Un adulte était là. L'histoire est finie.",
                        "Léa pose le seau bleu. Elle a pris la brosse le matin. Le soir, ce sera pareil, avec un adulte. L'histoire est finie.",
                        "Léa serre le doudou. La brosse est rangée. Matin et soir, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa ouvre la porte du jardin. L'air est frais. "
                        "Puis elle rentre. Elle prend la brosse. "
                        "Maman, l'adulte, est là. Le matin. Le soir aussi."
                    ),
                    "ch3_prompt": "Léa prend quoi après ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Dehors, le ballon rouge attend. Léa a brossé. Matin, brosse. Soir, brosse. Un adulte. L'histoire est finie.",
                        "Léa pose le seau bleu près des fleurs. Elle a pris la brosse. Le matin et le soir, avec un adulte. L'histoire est finie.",
                        "Le doudou reste à la fenêtre. Léa a la brosse. Matin et soir, un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa revient dans la chambre. Elle s'habille. "
                        "Puis elle prend la brosse. Papa, l'adulte, l'aide. "
                        "C'est le matin. Le soir, la brosse reviendra."
                    ),
                    "ch3_prompt": "Léa prend quoi après ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Le ballon rouge est sous le lit. Léa a brossé. Le matin, la brosse. Le soir, la brosse. Un adulte. L'histoire est finie.",
                        "Le seau bleu sert aux crayons. Léa a pris la brosse. Matin et soir, avec un adulte. L'histoire est finie.",
                        "Le doudou l'attend. Léa range la brosse. Matin et soir, un adulte est là. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Après la sieste, Léa se réveille. L'école est calme. "
                "Maman est venue. Un adulte est là. "
                "Léa prend sa brosse. Elles brossent un peu. "
                "Le matin, c'était déjà fait. Le soir, on brossera encore."
            ),
            "q_prompt": "Léa prend quoi, après la sieste ?",
            "retry": "La brosse. Avec un adulte. Matin et soir aussi. Quoi ?",
            "pos": "Oui. Elle prend la brosse. Avec un adulte. Matin et soir.",
            "wrong": "On prend la brosse. Matin et soir, avec un adulte.",
            "examples": ["brosse", "la brosse", "matin", "soir", "adulte"],
            "fb": (
                "Après la sieste, Léa a brossé. "
                "Le matin déjà. Le soir encore. Un adulte avec elle."
            ),
            "ch2_prompt": "Léa va où ensuite ? La cuisine, le jardin, ou la chambre ?",
            "ch2_labels": ["la cuisine", "le jardin", "la chambre"],
            "subs": [
                {
                    "audio": (
                        "Léa va à la cuisine. Un verre d'eau. "
                        "Elle a pris la brosse. Maman, l'adulte, sourit. "
                        "Le matin. Après la sieste. Le soir."
                    ),
                    "ch3_prompt": "Léa prend quoi ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Léa roule le ballon rouge. La brosse a fait son travail. Matin et soir, avec un adulte. L'histoire est finie.",
                        "Léa pose le seau bleu. Elle a la brosse. Le matin, le soir, un adulte. L'histoire est finie.",
                        "Léa câline le doudou. Elle a brossé. Matin et soir, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa va au jardin un moment. "
                        "Ses dents sont brossées. Un adulte l'a aidée. "
                        "Le matin. Le soir, la brosse reviendra."
                    ),
                    "ch3_prompt": "Léa prend quoi ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Le ballon rouge rebondit. Léa a pris la brosse. Matin et soir, un adulte. L'histoire est finie.",
                        "Le seau bleu a de l'eau pour les fleurs. Léa a brossé. Le matin, le soir, avec un adulte. L'histoire est finie.",
                        "Le doudou s'assoit dehors un peu. Léa a la brosse. Matin et soir. Un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa rentre dans la chambre. Le lit est défait. "
                        "Elle a pris la brosse. Papa, l'adulte, range. "
                        "Le matin c'était fait. Le soir, encore."
                    ),
                    "ch3_prompt": "Léa prend quoi ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Le ballon rouge attend. Léa a brossé. Matin et soir, avec un adulte. L'histoire est finie.",
                        "Le seau bleu est sous la table. Léa a pris la brosse. Le matin, le soir. Un adulte. L'histoire est finie.",
                        "Le doudou retrouve l'oreiller. Léa a la brosse. Matin et soir, un adulte. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "C'est le soir. Léa rentre d'école. "
                "Papa dit : la brosse. Un adulte est là. "
                "Léa prend sa brosse. Ils brossent. "
                "Le matin, c'était déjà fait. Matin et soir."
            ),
            "q_prompt": "Le soir, Léa prend quoi ?",
            "retry": "La brosse. Avec un adulte. Le matin aussi. Quoi ?",
            "pos": "Oui. Elle prend la brosse. Matin et soir, avec un adulte.",
            "wrong": "On prend la brosse. Matin et soir, avec un adulte.",
            "examples": ["brosse", "la brosse", "soir", "matin", "avec papa"],
            "fb": (
                "Léa a brossé le soir. "
                "Le matin aussi. Un adulte était avec elle."
            ),
            "ch2_prompt": "Avant le lit, Léa passe où ? La cuisine, le jardin, ou la chambre ?",
            "ch2_labels": ["la cuisine", "le jardin", "la chambre"],
            "subs": [
                {
                    "audio": (
                        "Léa boit un peu à la cuisine. "
                        "Puis elle prend la brosse. Papa, l'adulte, brosse aussi. "
                        "Le soir. Comme le matin."
                    ),
                    "ch3_prompt": "Léa emmène quoi au lit ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Le ballon rouge reste au salon. Léa a brossé. Le soir et le matin, avec un adulte. L'histoire est finie.",
                        "Le seau bleu reste à sa place. Léa a pris la brosse. Matin et soir, un adulte. L'histoire est finie.",
                        "Le doudou va au lit. Léa a la brosse. Le matin, le soir, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa ferme la porte du jardin. Il fait nuit. "
                        "Elle a pris la brosse. Maman, l'adulte, l'aide. "
                        "Le soir. Le matin, ce sera pareil."
                    ),
                    "ch3_prompt": "Léa emmène quoi au lit ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Le ballon rouge dort au panier. Léa a brossé. Matin et soir, un adulte. L'histoire est finie.",
                        "Le seau bleu reste dehors. Léa a pris la brosse. Le soir, le matin, avec un adulte. L'histoire est finie.",
                        "Le doudou sent bon. Léa a la brosse. Matin et soir, un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa est dans la chambre. Pyjama. "
                        "Elle a déjà pris la brosse. Un adulte était là. "
                        "Le soir. Le matin aussi."
                    ),
                    "ch3_prompt": "Léa emmène quoi au lit ? Le ballon, le seau, ou le doudou ?",
                    "ch3_labels": ["le ballon rouge", "le seau bleu", "le doudou"],
                    "ends": [
                        "Le ballon rouge reste au pied du lit. Léa a brossé. Le matin, le soir, avec un adulte. L'histoire est finie.",
                        "Le seau bleu sert de table de nuit. Léa a pris la brosse. Matin et soir, un adulte. L'histoire est finie.",
                        "Le doudou est sous le coude. Léa a la brosse. Matin et soir, avec un adulte. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-006 N2 Zoé — se moucher au marché
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-006"] = {
    "root": (
        "Zoé va au marché avec papa. Maman les rejoint. "
        "Le nez de Zoé chatouille. Atchoum, tout doux. "
        "Papa dit : on prend un mouchoir. Puis on le met à la poubelle."
    ),
    "ch1_prompt": "Zoé se mouche près de qui ? Tom, Léa, ou Sami ?",
    "ch1_labels": ["Tom", "Léa", "Sami"],
    "branches": [
        {
            "audio": (
                "Tom est près de l'étal des fruits. Zoé a le nez plein. "
                "Papa tend un mouchoir. Zoé prend le mouchoir. Elle se mouche. "
                "Puis elle va à la poubelle. Elle jette le mouchoir. Tom dit : bien."
            ),
            "q_prompt": "Zoé se mouche. Que prend-elle ?",
            "retry": "Un mouchoir. Puis la poubelle. Que prend Zoé ?",
            "pos": "Oui. Elle prend un mouchoir. Puis elle le jette à la poubelle.",
            "wrong": "On prend un mouchoir. Puis on le met à la poubelle.",
            "examples": ["mouchoir", "un mouchoir", "poubelle", "elle se mouche"],
            "fb": (
                "Zoé a le nez plus libre. Le mouchoir est à la poubelle. "
                "Tom est encore là."
            ),
            "ch2_prompt": "Zoé attend où, nez propre ? Aux cubes, au livre, ou à la dînette ?",
            "ch2_labels": ["les cubes", "le livre", "la dînette"],
            "subs": [
                {
                    "audio": (
                        "Au stand des jouets, il y a des cubes. "
                        "Zoé a déjà pris un mouchoir. Elle l'a jeté à la poubelle. "
                        "Elle peut empiler. Tom l'aide."
                    ),
                    "ch3_prompt": "On regarde quoi ensuite ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Papa achète une pomme. Zoé a le mouchoir à la poubelle. Son nez respire. Tom tient le sac. L'histoire est finie.",
                        "Maman prend un yaourt. Zoé a jeté le mouchoir à la poubelle. Tom sourit. L'histoire est finie.",
                        "Le pain est chaud. Zoé a pris un mouchoir. Puis la poubelle. Tom dit merci. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa... non, Tom montre un petit livre. "
                        "Zoé a le nez propre. Mouchoir, puis poubelle. "
                        "Elle tourne une page. Papa est là."
                    ),
                    "ch3_prompt": "On regarde quoi ensuite ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Une pomme rouge. Zoé a mis le mouchoir à la poubelle. Tom ferme le livre. L'histoire est finie.",
                        "Un yaourt frais. Zoé a pris un mouchoir. Poubelle. Tom range. L'histoire est finie.",
                        "Un morceau de pain. Zoé a le nez libre. Mouchoir à la poubelle. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Il y a une petite dînette en bois. Tom s'assoit. "
                        "Zoé a déjà jeté le mouchoir à la poubelle. "
                        "Elle joue un peu. Maman dit : nez propre."
                    ),
                    "ch3_prompt": "On regarde quoi ensuite ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Papa montre une pomme. Zoé a le mouchoir à la poubelle. Tom pose une assiette. L'histoire est finie.",
                        "Maman a un yaourt. Zoé a pris un mouchoir. Puis la poubelle. L'histoire est finie.",
                        "Le pain craque. Zoé a jeté le mouchoir. Poubelle. Tom dit : on rentre. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Léa est près des fleurs. Zoé sent un chatouillement. "
                "Maman sort un mouchoir. Zoé prend le mouchoir. Elle se mouche. "
                "Elle trouve la poubelle. Elle jette. Léa dit : ton nez respire."
            ),
            "q_prompt": "Zoé a pris quoi, près des fleurs ?",
            "retry": "Un mouchoir. Puis la poubelle. Quoi ?",
            "pos": "Oui. Un mouchoir. Puis la poubelle.",
            "wrong": "On prend un mouchoir. Puis on le met à la poubelle.",
            "examples": ["mouchoir", "un mouchoir", "poubelle", "fleurs"],
            "fb": (
                "Les fleurs sentent bon. Zoé aussi respire. "
                "Le mouchoir est à la poubelle."
            ),
            "ch2_prompt": "Zoé s'assoit où ? Aux cubes, au livre, ou à la dînette ?",
            "ch2_labels": ["les cubes", "le livre", "la dînette"],
            "subs": [
                {
                    "audio": (
                        "Léa empile des cubes. Zoé a le nez propre. "
                        "Mouchoir, poubelle. Elle pose un cube bleu."
                    ),
                    "ch3_prompt": "On achète quoi ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Une pomme dans le sac. Zoé a jeté le mouchoir à la poubelle. Léa applaudit. L'histoire est finie.",
                        "Un yaourt. Zoé a pris un mouchoir. Poubelle. Léa tient la main. L'histoire est finie.",
                        "Du pain chaud. Zoé a le mouchoir à la poubelle. Léa dit : on y va. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa ouvre un livre d'images. "
                        "Zoé a déjà mis le mouchoir à la poubelle. "
                        "Elle écoute. Papa tourne la page."
                    ),
                    "ch3_prompt": "On achète quoi ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Papa prend une pomme. Zoé a le mouchoir à la poubelle. Léa ferme le livre. L'histoire est finie.",
                        "Maman prend un yaourt. Zoé a pris un mouchoir. Puis la poubelle. L'histoire est finie.",
                        "Le pain est dans le filet. Zoé a jeté le mouchoir. Poubelle. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Une dînette miniature. Léa sert du thé imaginaire. "
                        "Zoé a le nez libre. Mouchoir à la poubelle. "
                        "Elle dit : à table."
                    ),
                    "ch3_prompt": "On achète quoi ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Une vraie pomme. Zoé a mis le mouchoir à la poubelle. Léa range. L'histoire est finie.",
                        "Un vrai yaourt. Zoé a pris un mouchoir. Poubelle. L'histoire est finie.",
                        "Un vrai morceau de pain. Zoé a le mouchoir à la poubelle. Léa dit merci. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Sami est près du stand de pain. Zoé a le nez qui coule. "
                "Papa dit : mouchoir. Zoé prend un mouchoir. Elle se mouche. "
                "Sami montre la poubelle. Zoé jette. Son nez est plus libre."
            ),
            "q_prompt": "Sami montre la poubelle. Zoé a pris quoi avant ?",
            "retry": "Un mouchoir. Puis la poubelle. Quoi ?",
            "pos": "Oui. Un mouchoir. Puis la poubelle.",
            "wrong": "On prend un mouchoir. Puis on le met à la poubelle.",
            "examples": ["mouchoir", "un mouchoir", "poubelle", "Sami"],
            "fb": (
                "Le pain sent bon. Zoé respire mieux. "
                "Le mouchoir est à la poubelle."
            ),
            "ch2_prompt": "Sami et Zoé jouent à quoi ? Cubes, livre, ou dînette ?",
            "ch2_labels": ["les cubes", "le livre", "la dînette"],
            "subs": [
                {
                    "audio": (
                        "Sami construit. Zoé a déjà jeté le mouchoir à la poubelle. "
                        "Elle pose un cube. Papa surveille."
                    ),
                    "ch3_prompt": "On prend quoi ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Une pomme pour plus tard. Zoé a le mouchoir à la poubelle. Sami range les cubes. L'histoire est finie.",
                        "Un yaourt. Zoé a pris un mouchoir. Poubelle. Sami dit : on rentre. L'histoire est finie.",
                        "Le pain de Sami. Zoé a jeté le mouchoir à la poubelle. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami a un petit livre. "
                        "Zoé écoute, nez propre. Mouchoir, puis poubelle. "
                        "Maman dit : bien."
                    ),
                    "ch3_prompt": "On prend quoi ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Papa choisit une pomme. Zoé a le mouchoir à la poubelle. Sami ferme le livre. L'histoire est finie.",
                        "Maman choisit un yaourt. Zoé a pris un mouchoir. Poubelle. L'histoire est finie.",
                        "Sami sent le pain. Zoé a jeté le mouchoir. Poubelle. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami fait la dînette. Zoé a le nez libre. "
                        "Le mouchoir est déjà à la poubelle. "
                        "Elle sert une tasse imaginaire."
                    ),
                    "ch3_prompt": "On prend quoi ? Une pomme, un yaourt, ou du pain ?",
                    "ch3_labels": ["une pomme", "un yaourt", "un morceau de pain"],
                    "ends": [
                        "Une pomme vraie. Zoé a mis le mouchoir à la poubelle. Sami range. L'histoire est finie.",
                        "Un yaourt vrai. Zoé a pris un mouchoir. Puis la poubelle. L'histoire est finie.",
                        "Un morceau de pain vrai. Zoé a le mouchoir à la poubelle. Sami dit : au revoir marché. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-007 N2 Sara — aller se coucher dans la chambre
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-007"] = {
    "root": (
        "Le soir, la maison devient calme. Sara bâille. "
        "Maman dit : c'est l'heure. Papa ouvre le lit. "
        "On met le pyjama. Puis c'est le dodo. "
        "Le corps a besoin de dormir."
    ),
    "ch1_prompt": "Qui va au lit avec Sara ? Le chat, le chien, ou la poule ?",
    "ch1_labels": ["le chat", "le chien", "la poule"],
    "branches": [
        {
            "audio": (
                "Le chat en peluche attend sur l'oreiller. "
                "Le soir, Sara met son pyjama. Il est doux. "
                "Maman dit : au lit. Sara se couche. C'est le dodo. "
                "Papa baisse la lumière."
            ),
            "q_prompt": "Sara va dormir. Que met-elle ?",
            "retry": "Le soir. Le pyjama. Puis le dodo. Que met Sara ?",
            "pos": "Oui. Elle met le pyjama. Le soir, c'est le dodo.",
            "wrong": "Le soir, on met le pyjama. Puis on va au dodo.",
            "examples": ["pyjama", "le pyjama", "dodo", "au lit", "soir"],
            "fb": (
                "Sara a le pyjama. Le soir, elle est au lit. "
                "C'est le dodo. Le chat peluche est là."
            ),
            "ch2_prompt": "Avant le dodo, un souvenir ? Le bac, le toboggan, ou les balançoires ?",
            "ch2_labels": ["le bac à sable", "le toboggan", "les balançoires"],
            "subs": [
                {
                    "audio": (
                        "Sara pense au bac à sable. Les mains sont lavées. "
                        "Le soir, elle a le pyjama. Elle se couche. Dodo. "
                        "Le chat peluche ronronne, tout doux."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Le pyjama rouge est chaud. Le soir, Sara est au dodo. Le chat peluche aussi. L'histoire est finie.",
                        "Le pyjama bleu est doux. Sara a mis le pyjama. Le soir, dodo. L'histoire est finie.",
                        "Le pyjama vert a des étoiles. Sara se couche. Le soir, dodo. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sara se souvient du toboggan. Les jambes sont fatiguées. "
                        "Le soir, pyjama. Au lit. Dodo. "
                        "Maman pose le chat peluche."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Sara est au dodo. Le soir. Le chat peluche veille. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, dodo. Papa chuchote. L'histoire est finie.",
                        "Pyjama vert. Sara ferme les yeux. Le soir, dodo. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sara pense aux balançoires. Ça va, ça vient. "
                        "Maintenant, le soir. Pyjama. Dodo. "
                        "Le chat peluche est sous le bras."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Sara respire. Le soir, dodo. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, au lit. Dodo. L'histoire est finie.",
                        "Pyjama vert. Le chat peluche est là. Sara, dodo. Le soir. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Le chien en peluche a de grandes oreilles. "
                "Le soir, Sara met son pyjama. Papa l'aide. "
                "Elle se couche. C'est le dodo. Maman dit : le corps a besoin de dormir."
            ),
            "q_prompt": "Sara met le pyjama. Puis elle va où ?",
            "retry": "Le soir. Pyjama. Dodo. Où va Sara ?",
            "pos": "Oui. Elle met le pyjama. Puis c'est le dodo.",
            "wrong": "Le soir, on met le pyjama. Puis on va au dodo.",
            "examples": ["pyjama", "dodo", "au lit", "soir", "se coucher"],
            "fb": (
                "Le chien peluche est au pied du lit. "
                "Sara a le pyjama. Le soir, dodo."
            ),
            "ch2_prompt": "Sara a joué où, avant ? Le bac, le toboggan, ou les balançoires ?",
            "ch2_labels": ["le bac à sable", "le toboggan", "les balançoires"],
            "subs": [
                {
                    "audio": (
                        "Au bac, Sara a creusé. Maintenant les mains sont propres. "
                        "Le soir, pyjama. Dodo. Le chien peluche garde."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Sara est au dodo. Le soir. Le chien peluche aussi. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, dodo. L'histoire est finie.",
                        "Pyjama vert. Sara se couche. Le soir, dodo. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sara a glissé au toboggan. Les jambes sont lourdes. "
                        "Le soir, elle a le pyjama. Au lit. Dodo."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Dodo. Le soir. Le chien peluche est chaud. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, dodo. Papa baisse le store. L'histoire est finie.",
                        "Pyjama vert. Sara ferme les yeux. Le soir, dodo. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Les balançoires sont loin, maintenant. "
                        "Le soir, pyjama. Sara se couche. Dodo. "
                        "Le chien peluche a une oreille sur l'oreiller."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Sara, dodo. Le soir. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, au lit. Dodo. L'histoire est finie.",
                        "Pyjama vert. Le chien peluche veille. Sara, dodo. Le soir. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "La poule en peluche est ronde et douce. "
                "Le soir, Sara met son pyjama. Maman boutonnes. "
                "Sara se couche. C'est le dodo. Papa raconte deux phrases. Puis silence."
            ),
            "q_prompt": "Sara a la poule peluche. Que met-elle pour dormir ?",
            "retry": "Le soir. Le pyjama. Puis le dodo. Que met-elle ?",
            "pos": "Oui. Elle met le pyjama. Le soir, c'est le dodo.",
            "wrong": "Le soir, on met le pyjama. Puis on va au dodo.",
            "examples": ["pyjama", "le pyjama", "dodo", "soir"],
            "fb": (
                "La poule peluche est sous le coude. "
                "Sara a le pyjama. Le soir, dodo."
            ),
            "ch2_prompt": "Sara a joué où, avant ? Le bac, le toboggan, ou les balançoires ?",
            "ch2_labels": ["le bac à sable", "le toboggan", "les balançoires"],
            "subs": [
                {
                    "audio": (
                        "Le bac à sable est fermé. "
                        "Le soir, Sara a le pyjama. Elle se couche. Dodo. "
                        "La poule peluche est là."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Sara, dodo. Le soir. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, dodo. L'histoire est finie.",
                        "Pyjama vert. La poule peluche est ronde. Sara, dodo. Le soir. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Plus de toboggan. Les pieds sont au lit. "
                        "Le soir, pyjama. Dodo. Maman pose un baiser."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Sara est au dodo. Le soir. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, dodo. L'histoire est finie.",
                        "Pyjama vert. Sara ferme les yeux. Le soir, dodo. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Les balançoires se taisent dans sa tête. "
                        "Le soir, Sara a le pyjama. Au lit. Dodo. "
                        "La poule peluche reste."
                    ),
                    "ch3_prompt": "Le pyjama est de quelle couleur ? Rouge, bleu, ou vert ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Pyjama rouge. Dodo. Le soir. L'histoire est finie.",
                        "Pyjama bleu. Sara a mis le pyjama. Le soir, au lit. Dodo. L'histoire est finie.",
                        "Pyjama vert. La poule peluche est là. Sara, dodo. Le soir. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-008 N3 Lila — jouer dehors un moment (près de la fenêtre)
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-008"] = {
    "root": (
        "Lila est près de la fenêtre. Ses jambes ont envie de bouger. "
        "Papa dit : on va dehors. Maman prend les chaussures. "
        "On joue dehors, avec un adulte. Un moment. Puis on rentre."
    ),
    "ch1_prompt": "Lila va dehors comment ? En train, en bus, ou en voiture ?",
    "ch1_labels": ["le train", "le bus", "la voiture"],
    "branches": [
        {
            "audio": (
                "Ils prennent le petit train, tout près. Papa tient la main. "
                "À la gare-jardin, ils descendent. "
                "Lila court sur l'herbe. Elle joue dehors, avec un adulte. "
                "Papa reste près d'elle. Maman arrive."
            ),
            "q_prompt": "Lila veut bouger. Où joue-t-elle ?",
            "retry": "Dehors. Avec un adulte. Où ?",
            "pos": "Oui. Elle joue dehors, avec un adulte.",
            "wrong": "On joue dehors, avec un adulte. Papa ou maman.",
            "examples": ["dehors", "avec papa", "avec un adulte", "au jardin", "avec maman"],
            "fb": (
                "Lila a bougé dehors. Un adulte était là. "
                "Le train attendra pour rentrer."
            ),
            "ch2_prompt": "Qui joue avec Lila dehors ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom lance un ballon. Lila court. "
                        "Ils jouent dehors. Papa, l'adulte, les voit. "
                        "Maman dit : encore un moment."
                    ),
                    "ch3_prompt": "Ils jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, l'herbe est fraîche. Lila joue dehors, avec un adulte. Tom aussi. Puis le train. L'histoire est finie.",
                        "Après la sieste, Lila a de l'énergie. Elle joue dehors, avec un adulte. Tom lance. L'histoire est finie.",
                        "Le soir, le ciel est rose. Lila joue dehors, avec un adulte. Tom dit : on rentre. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa ramasse des feuilles. Lila l'aide. "
                        "Elles jouent dehors, avec un adulte. Papa marche à côté."
                    ),
                    "ch3_prompt": "Elles jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa et Lila jouent dehors, avec un adulte. Une feuille vole. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Léa chante. L'histoire est finie.",
                        "Le soir, elles rangent. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami suit un petit chemin. Lila aussi. "
                        "Ils jouent dehors. Maman, l'adulte, est là. "
                        "Le train sifflera plus tard."
                    ),
                    "ch3_prompt": "Ils jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Sami et Lila jouent dehors, avec un adulte. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Sami saute à cloche-pied. L'histoire est finie.",
                        "Le soir, le train les reprend. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Ils prennent le bus. Maman est à côté. Un adulte. "
                "Ils descendent au parc. Lila respire l'air. "
                "Elle joue dehors, avec un adulte. Papa les rejoint."
            ),
            "q_prompt": "Après le bus, Lila joue où ?",
            "retry": "Dehors. Avec un adulte. Où ?",
            "pos": "Oui. Elle joue dehors, avec un adulte.",
            "wrong": "On joue dehors, avec un adulte. Papa ou maman.",
            "examples": ["dehors", "au parc", "avec un adulte", "avec maman"],
            "fb": (
                "Le bus les a menées au parc. "
                "Lila joue dehors, avec un adulte."
            ),
            "ch2_prompt": "Qui court avec Lila ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom a un cerceau. Lila le fait rouler. "
                        "Ils jouent dehors. Maman, l'adulte, les voit."
                    ),
                    "ch3_prompt": "Ils jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, le cerceau roule. Lila joue dehors, avec un adulte. Tom rit. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Tom souffle. L'histoire est finie.",
                        "Le soir, le bus revient. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa grimpe sur la petite butte. Lila aussi. "
                        "Elles jouent dehors, avec un adulte. Papa dit : je vous vois."
                    ),
                    "ch3_prompt": "Elles jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, la butte est douce. Lila joue dehors, avec un adulte. Léa aussi. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Léa s'assoit. L'histoire est finie.",
                        "Le soir, elles redescendent. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami a une corde à sauter. Lila essaie. "
                        "Ils jouent dehors. Un adulte compte. C'est maman."
                    ),
                    "ch3_prompt": "Ils jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, la corde tape. Lila joue dehors, avec un adulte. Sami compte. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Sami pose la corde. L'histoire est finie.",
                        "Le soir, le bus les attend. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Papa prend la voiture. Lila s'assoit. Maman aussi. "
                "Ils arrivent à la cour de la ferme. "
                "Lila court. Elle joue dehors, avec un adulte. L'air sent le foin."
            ),
            "q_prompt": "À la ferme, Lila joue où ?",
            "retry": "Dehors. Avec un adulte. Où ?",
            "pos": "Oui. Elle joue dehors, avec un adulte.",
            "wrong": "On joue dehors, avec un adulte. Papa ou maman.",
            "examples": ["dehors", "avec un adulte", "à la ferme", "avec papa"],
            "fb": (
                "La voiture est rangée. Lila a bougé. "
                "Dehors, avec un adulte."
            ),
            "ch2_prompt": "Qui court dans la cour ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom a un seau. Ils portent de l'herbe. "
                        "Ils jouent dehors. Papa, l'adulte, marche avec eux."
                    ),
                    "ch3_prompt": "Ils jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, la cour est calme. Lila joue dehors, avec un adulte. Tom aussi. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Tom pose le seau. L'histoire est finie.",
                        "Le soir, la voiture rentre. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa écoute une poule, loin. Lila aussi. "
                        "Elles jouent dehors, avec un adulte. Maman reste près."
                    ),
                    "ch3_prompt": "Elles jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa et Lila jouent dehors, avec un adulte. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Léa bâille. L'histoire est finie.",
                        "Le soir, elles saluent la poule. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami marche sur une planche. Lila l'imite, tout doux. "
                        "Ils jouent dehors. Un adulte les voit. C'est papa."
                    ),
                    "ch3_prompt": "Ils jouent dehors quand ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, la planche est sèche. Lila joue dehors, avec un adulte. Sami aussi. L'histoire est finie.",
                        "Après la sieste, Lila joue dehors, avec un adulte. Sami s'assoit. L'histoire est finie.",
                        "Le soir, la voiture part. Lila a joué dehors, avec un adulte. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-009 N1 Tom — éteindre l'écran dans le salon
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-009"] = {
    "root": (
        "Tom est dans le salon. Un dessin danse à l'écran. "
        "Maman s'assoit près de lui. Papa est là aussi. "
        "L'adulte dit fini. Tom va éteindre. "
        "Puis il prend un autre jeu."
    ),
    "ch1_prompt": "Tom a goûté quoi, avant l'écran ? Une pomme, un yaourt, ou du pain ?",
    "ch1_labels": ["une pomme", "un yaourt", "un morceau de pain"],
    "branches": [
        {
            "audio": (
                "Tom a croqué une pomme. Puis le dessin. "
                "Maman dit : fini. L'adulte dit fini. "
                "Tom éteint l'écran. L'écran devient noir. "
                "Maman dit : un autre jeu. Tom cherche."
            ),
            "q_prompt": "Maman dit fini. Que fait Tom ?",
            "retry": "L'adulte dit fini. Il éteint. Puis un autre jeu. Que fait-il ?",
            "pos": "Oui. Il éteint. Puis il prend un autre jeu.",
            "wrong": "Quand l'adulte dit fini, on éteint. Puis on prend un autre jeu.",
            "examples": ["éteindre", "il éteint", "autre jeu", "fini", "les cubes"],
            "fb": (
                "Tom a éteint. L'adulte a dit fini. "
                "Un autre jeu commence."
            ),
            "ch2_prompt": "L'autre jeu, c'est où ? La cuisine, le jardin, ou la chambre ?",
            "ch2_labels": ["la cuisine", "le jardin", "la chambre"],
            "subs": [
                {
                    "audio": (
                        "Tom va à la cuisine. L'écran est éteint. "
                        "L'adulte a dit fini. Il prend un autre jeu. "
                        "Des cuillères en bois. Papa joue aussi."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Tom empile les cubes. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Tom ouvre le livre. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Tom fait la dînette. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Tom va au jardin. L'écran est éteint. "
                        "L'adulte a dit fini. Un autre jeu dehors. "
                        "Le ballon. Maman lance."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Tom pose des cubes sur la table du jardin. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Tom lit un livre sur l'herbe. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Tom sort la dînette. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Tom va dans la chambre. L'écran est éteint. "
                        "L'adulte a dit fini. Un autre jeu sur le tapis. "
                        "Papa s'assoit."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Tom bâtit une tour de cubes. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Tom écoute le livre. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Tom sert le doudou à la dînette. Il a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Tom a mangé un yaourt. Puis l'écran. "
                "Papa dit : fini. L'adulte dit fini. "
                "Tom éteint. Il pose la télécommande. "
                "Papa dit : un autre jeu."
            ),
            "q_prompt": "Papa dit fini. Que fait Tom ?",
            "retry": "L'adulte dit fini. Éteindre. Puis un autre jeu. Que fait-il ?",
            "pos": "Oui. Il éteint. Puis il prend un autre jeu.",
            "wrong": "Quand l'adulte dit fini, on éteint. Puis on prend un autre jeu.",
            "examples": ["éteindre", "il éteint", "autre jeu", "fini"],
            "fb": (
                "Tom a éteint. L'adulte a dit fini. "
                "Le yaourt est fini aussi. Un autre jeu."
            ),
            "ch2_prompt": "L'autre jeu, c'est où ? La cuisine, le jardin, ou la chambre ?",
            "ch2_labels": ["la cuisine", "le jardin", "la chambre"],
            "subs": [
                {
                    "audio": (
                        "À la cuisine, Tom range le pot. "
                        "L'écran est éteint. L'adulte a dit fini. "
                        "Un autre jeu : trier les cuillères."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Cubes sur la table. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Un livre de recettes imagées. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "La dînette près du buffet. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Au jardin, Tom court un peu. "
                        "Il a éteint. L'adulte a dit fini. "
                        "Un autre jeu, dehors."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Cubes au soleil. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Un livre sous le cerisier. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Dînette sur la nappe. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Dans la chambre, Tom s'étire. "
                        "L'écran est éteint. L'adulte a dit fini. "
                        "Un autre jeu sur le tapis."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Une tour de cubes. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Le livre des animaux. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "La dînette des peluches. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Tom a mangé un morceau de pain. Puis l'écran. "
                "Maman dit : fini. L'adulte dit fini. "
                "Tom éteint. Il sourit un peu. "
                "Maman dit : un autre jeu, maintenant."
            ),
            "q_prompt": "L'adulte dit fini. Que fait Tom ?",
            "retry": "Il éteint. Puis un autre jeu. Que fait-il ?",
            "pos": "Oui. Il éteint. Puis il prend un autre jeu.",
            "wrong": "Quand l'adulte dit fini, on éteint. Puis on prend un autre jeu.",
            "examples": ["éteindre", "il éteint", "autre jeu", "fini", "pain"],
            "fb": (
                "Le pain est fini. L'écran aussi. "
                "Tom a éteint. L'adulte a dit fini. Un autre jeu."
            ),
            "ch2_prompt": "L'autre jeu, c'est où ? La cuisine, le jardin, ou la chambre ?",
            "ch2_labels": ["la cuisine", "le jardin", "la chambre"],
            "subs": [
                {
                    "audio": (
                        "À la cuisine, Tom essuie des miettes. "
                        "L'écran est éteint. L'adulte a dit fini. "
                        "Un autre jeu avec papa."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Cubes et miettes rangées. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Un livre sur la table. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Dînette après le pain. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Au jardin, Tom cherche un caillou rond. "
                        "Il a éteint. L'adulte a dit fini. "
                        "Un autre jeu."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Cubes près des cailloux. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Un livre sur le banc. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Dînette sous le tilleul. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Dans la chambre, Tom range une chaussette. "
                        "L'écran est éteint. L'adulte a dit fini. "
                        "Un autre jeu, tout calme."
                    ),
                    "ch3_prompt": "Quel autre jeu ? Les cubes, le livre, ou la dînette ?",
                    "ch3_labels": ["les cubes", "le livre", "la dînette"],
                    "ends": [
                        "Cubes au pied du lit. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "Le livre sous la lampe. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                        "La dînette des doudous. Tom a éteint. L'adulte a dit fini. Un autre jeu. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-010 N2 Zoé — goûter un légume dans la cuisine (dîner avec copains)
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-010"] = {
    "root": (
        "Le soir, Zoé est dans la cuisine. Papa cuisine. Maman dresse la table. "
        "Il y a des copains. Dans la poêle, des légumes. "
        "Papa dit : on peut goûter une petite portion. Puis nommer le goût."
    ),
    "ch1_prompt": "Zoé goûte avec qui ? Tom, Léa, ou Sami ?",
    "ch1_labels": ["Tom", "Léa", "Sami"],
    "branches": [
        {
            "audio": (
                "Tom s'assoit près de Zoé. Papa sert des brocolis. "
                "Zoé goûte une petite portion. C'est un peu croquant. "
                "Elle nomme le goût : c'est doux, papa. Tom écoute."
            ),
            "q_prompt": "Zoé goûte le brocoli. Que fait-elle ?",
            "retry": "Une petite portion. Elle nomme le goût. Que fait Zoé ?",
            "pos": "Oui. Elle goûte une petite portion. Elle nomme le goût.",
            "wrong": "On goûte une petite portion. On nomme le goût à papa ou maman.",
            "examples": ["goûter", "petite portion", "le goût", "une bouchée", "brocoli"],
            "fb": (
                "Zoé a goûté. Elle a nommé le goût. "
                "Une petite portion, c'est assez. Tom applaudit."
            ),
            "ch2_prompt": "Après, Zoé joue à quoi ? Les cubes, le livre, ou la dînette ?",
            "ch2_labels": ["les cubes", "le livre", "la dînette"],
            "subs": [
                {
                    "audio": (
                        "Zoé et Tom empilent des cubes. "
                        "Zoé dit : j'ai goûté une petite portion. J'ai nommé le goût. "
                        "Tom pose un cube vert, comme le brocoli."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Zoé dit : c'est doux. Elle a goûté une petite portion. Elle a nommé le goût. Tom sourit. L'histoire est finie.",
                        "Zoé dit : un peu salé. Elle a goûté une petite portion. Elle nomme le goût. Tom hoche. L'histoire est finie.",
                        "Zoé dit : c'est croquant. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Maman ouvre un livre de légumes. "
                        "Zoé montre le brocoli. Elle a goûté une petite portion. "
                        "Elle nomme le goût. Tom tourne la page."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Dans le livre, Zoé dit : doux. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : salé, un peu. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : croquant. Elle a goûté une petite portion. Elle nomme le goût. Tom rit. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Ils font la dînette. Zoé sert un tout petit brocoli. "
                        "Elle a goûté une petite portion, pour de vrai. "
                        "Elle nomme le goût. Tom sert de l'eau."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "À la dînette, Zoé dit : doux. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : salé. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : croquant. Elle a goûté une petite portion. Elle nomme le goût. Tom tapote. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Léa a une assiette de betterave. Elle est rose. "
                "Zoé goûte une petite portion. C'est terreux et doux. "
                "Elle nomme le goût : c'est doux, maman. Léa ouvre les yeux."
            ),
            "q_prompt": "Zoé goûte la betterave. Que fait-elle ?",
            "retry": "Une petite portion. Nommer le goût. Que fait Zoé ?",
            "pos": "Oui. Elle goûte une petite portion. Elle nomme le goût.",
            "wrong": "On goûte une petite portion. On nomme le goût à papa ou maman.",
            "examples": ["goûter", "petite portion", "le goût", "betterave"],
            "fb": (
                "Les lèvres de Zoé sont un peu roses. "
                "Elle a goûté. Elle a nommé le goût. Une petite portion."
            ),
            "ch2_prompt": "Après, Zoé joue à quoi ? Les cubes, le livre, ou la dînette ?",
            "ch2_labels": ["les cubes", "le livre", "la dînette"],
            "subs": [
                {
                    "audio": (
                        "Léa choisit un cube rose. Zoé aussi. "
                        "Zoé dit : j'ai goûté une petite portion. J'ai nommé le goût."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Zoé dit : doux et rose. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : un peu salé. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : pas trop croquant. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Dans le livre, une betterave. Léa montre. "
                        "Zoé a goûté une petite portion. Elle nomme le goût."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Zoé dit : doux. Elle a goûté une petite portion. Elle nomme le goût. Léa sourit. L'histoire est finie.",
                        "Zoé dit : salé. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : tendre, pas croquant. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "À la dînette, Léa sert du rose. "
                        "Zoé a goûté une petite portion pour de vrai. "
                        "Elle nomme le goût. Maman rit."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Zoé dit : doux. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : salé, un tout petit peu. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : mou, pas croquant. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Sami a des épinards. Ils sont verts et chauds. "
                "Zoé goûte une petite portion. C'est fondant. "
                "Elle nomme le goût : c'est doux, papa. Sami hoche."
            ),
            "q_prompt": "Zoé goûte les épinards. Que fait-elle ?",
            "retry": "Petite portion. Nommer le goût. Que fait Zoé ?",
            "pos": "Oui. Elle goûte une petite portion. Elle nomme le goût.",
            "wrong": "On goûte une petite portion. On nomme le goût à papa ou maman.",
            "examples": ["goûter", "petite portion", "le goût", "épinards"],
            "fb": (
                "Zoé a goûté les épinards. "
                "Elle a nommé le goût. Une petite portion."
            ),
            "ch2_prompt": "Après, Zoé joue à quoi ? Les cubes, le livre, ou la dînette ?",
            "ch2_labels": ["les cubes", "le livre", "la dînette"],
            "subs": [
                {
                    "audio": (
                        "Sami bâtit une tour verte. "
                        "Zoé dit : j'ai goûté une petite portion. J'ai nommé le goût."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Zoé dit : doux. Elle a goûté une petite portion. Elle nomme le goût. Sami pose un cube. L'histoire est finie.",
                        "Zoé dit : un peu salé. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : fondant, pas croquant. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami trouve les épinards dans le livre. "
                        "Zoé a goûté une petite portion. Elle nomme le goût."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Zoé dit : doux. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : salé. Elle a goûté une petite portion. Elle nomme le goût. Sami ferme le livre. L'histoire est finie.",
                        "Zoé dit : pas croquant. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "À la dînette, Sami sert du vert. "
                        "Zoé a goûté une petite portion. Elle nomme le goût. "
                        "Papa dit : merci d'avoir dit le goût."
                    ),
                    "ch3_prompt": "Zoé dit le goût comment ? Doux, salé, ou croquant ?",
                    "ch3_labels": ["doux", "salé", "croquant"],
                    "ends": [
                        "Zoé dit : doux. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : salé. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                        "Zoé dit : tout mou, pas croquant. Elle a goûté une petite portion. Elle nomme le goût. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-011 N2 Sara — s'asseoir pour manger au parc (pique-nique)
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-011"] = {
    "root": (
        "Sara va au parc avec maman. Papa porte le panier. "
        "C'est l'heure de manger. On s'assoit. "
        "Assis à table, ensemble. Ici, la table est une nappe sur l'herbe. "
        "Sara pose les fesses. Elle reste assise."
    ),
    "ch1_prompt": "Qui vient près de la nappe ? Le chat, le chien, ou la poule ?",
    "ch1_labels": ["le chat", "le chien", "la poule"],
    "branches": [
        {
            "audio": (
                "Un chat passe au loin. Sara s'assoit sur la nappe. "
                "Les fesses posées. Papa s'assoit. Maman s'assoit. "
                "Ils mangent ensemble, à table, sur la nappe. Sara reste assise."
            ),
            "q_prompt": "Sara va manger au parc. Que fait-elle ?",
            "retry": "Elle s'assoit. À table. Ensemble. Que fait Sara ?",
            "pos": "Oui. Elle s'assoit à table. Ils mangent ensemble.",
            "wrong": "On s'assoit à table. On pose les fesses. On mange ensemble.",
            "examples": ["assise", "s'asseoir", "à table", "ensemble", "nappe"],
            "fb": (
                "Sara est assise. La nappe est leur table. "
                "Ensemble, c'est calme. Le chat s'éloigne."
            ),
            "ch2_prompt": "Après manger, Sara joue où ? Le bac, le toboggan, ou les balançoires ?",
            "ch2_labels": ["le bac à sable", "le toboggan", "les balançoires"],
            "subs": [
                {
                    "audio": (
                        "Sara a mangé assise, à table, ensemble. "
                        "Puis elle va au bac. Elle reste calme. "
                        "Maman dit : on a bien mangé assis."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "La nappe rouge est pliée. Sara a mangé assise à table, ensemble. Le bac l'attend. L'histoire est finie.",
                        "La nappe bleue sent l'herbe. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "La nappe verte a une miette. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Après le repas, assise, Sara va au toboggan. "
                        "Elle a mangé à table, ensemble. "
                        "Papa dit : d'abord assis. Puis on glisse."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. Puis le toboggan. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sara se balance après. Elle a d'abord mangé assise. "
                        "À table, ensemble. Maman plie un coin de nappe."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. La balançoire craque. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Le chien du parc reste avec son maître, loin. "
                "Sara s'assoit. Fesses sur la nappe. "
                "Papa et maman s'assoient. Ils mangent ensemble à table. "
                "Sara tient son sandwich. Elle reste assise."
            ),
            "q_prompt": "Le chien est loin. Sara, elle, que fait-elle pour manger ?",
            "retry": "Assise. À table. Ensemble. Que fait Sara ?",
            "pos": "Oui. Elle s'assoit à table. Ils mangent ensemble.",
            "wrong": "On s'assoit à table. On pose les fesses. On mange ensemble.",
            "examples": ["assise", "s'asseoir", "à table", "ensemble"],
            "fb": (
                "Sara est assise. Le chien ne vient pas. "
                "À table, ensemble, c'est le pique-nique."
            ),
            "ch2_prompt": "Après, Sara joue où ? Le bac, le toboggan, ou les balançoires ?",
            "ch2_labels": ["le bac à sable", "le toboggan", "les balançoires"],
            "subs": [
                {
                    "audio": (
                        "Sara a mangé assise, ensemble, à table. "
                        "Au bac, elle creuse. Papa dit : d'abord on était assis."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Au toboggan, Sara attend son tour. "
                        "Elle a mangé assise à table, ensemble. "
                        "Maman range le panier."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sara se balance. Elle a d'abord été assise. "
                        "À table, ensemble. Papa pousse tout doux."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Une poule du jardin d'à côté picore loin. "
                "Sara s'assoit à table, sur la nappe. Ensemble. "
                "Papa verse de l'eau. Maman ouvre la boîte. "
                "Sara mange assise. Les fesses bien posées."
            ),
            "q_prompt": "La poule picore. Sara, elle, que fait-elle ?",
            "retry": "Elle s'assoit. À table. Ensemble. Que fait Sara ?",
            "pos": "Oui. Elle s'assoit à table. Ils mangent ensemble.",
            "wrong": "On s'assoit à table. On pose les fesses. On mange ensemble.",
            "examples": ["assise", "s'asseoir", "à table", "ensemble", "poule"],
            "fb": (
                "Sara est assise. La poule reste loin. "
                "Ensemble, à table, le pique-nique est calme."
            ),
            "ch2_prompt": "Après, Sara joue où ? Le bac, le toboggan, ou les balançoires ?",
            "ch2_labels": ["le bac à sable", "le toboggan", "les balançoires"],
            "subs": [
                {
                    "audio": (
                        "Au bac, Sara a les mains occupées. "
                        "Elle a mangé assise, à table, ensemble. "
                        "Maman dit : bravo d'être restée assise."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sara gravit le toboggan. "
                        "Avant, elle était assise à table, ensemble. "
                        "Papa la voit."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Aux balançoires, Sara chante. "
                        "Elle a mangé assise, ensemble, à table. "
                        "Maman plie la nappe."
                    ),
                    "ch3_prompt": "La nappe est de quelle couleur ? Rouge, bleue, ou verte ?",
                    "ch3_labels": ["rouge", "bleu", "vert"],
                    "ends": [
                        "Nappe rouge. Sara a mangé assise à table, ensemble. L'histoire est finie.",
                        "Nappe bleue. Sara était assise. Ensemble, à table. L'histoire est finie.",
                        "Nappe verte. Sara a mangé assise, ensemble, à table. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# TREE-SAN-012 N3 Lila — se laver les mains (retour de trajet, jardin)
# ---------------------------------------------------------------------------
SPECS["TREE-SAN-012"] = {
    "root": (
        "Lila rentre au jardin. Papa ouvre le portail. Maman porte le sac. "
        "Les mains ont voyagé. Bientôt on mange. "
        "Avant de manger, savon. Après les toilettes, savon aussi. "
        "Eau, savon, rincer, essuyer."
    ),
    "ch1_prompt": "Lila rentre d'où ? Du train, du bus, ou de la voiture ?",
    "ch1_labels": ["le train", "le bus", "la voiture"],
    "branches": [
        {
            "audio": (
                "Ils ont pris le train. Lila a touché la barre. "
                "Au jardin, papa dit : avant de manger, on lave. "
                "Lila ouvre l'eau. Elle prend le savon. Elle frotte. Elle rince. "
                "Après les toilettes du quai, elle avait déjà pris le savon."
            ),
            "q_prompt": "Lila se lave. Avec quoi ?",
            "retry": "Savon. Avant de manger. Après les toilettes aussi. Quoi ?",
            "pos": "Oui. Elle prend le savon. Avant de manger, et après les toilettes.",
            "wrong": "On prend le savon. Avant de manger, et après les toilettes.",
            "examples": ["savon", "du savon", "les mains", "avant de manger", "après les toilettes"],
            "fb": (
                "Les mains de Lila sentent le savon. "
                "Avant de manger, c'est fait. Après les toilettes, c'était fait."
            ),
            "ch2_prompt": "Qui se lave avec Lila ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom frotte aussi. Savon. "
                        "Lila dit : avant de manger. Après les toilettes, pareil. "
                        "Ils essuient. Maman pose le goûter."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Lila a pris le savon. Avant de manger. Après les toilettes. Tom aussi. L'histoire est finie.",
                        "Après la sieste, Lila lave au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a le savon. Avant de manger. Après les toilettes. Tom dit merci. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa chante : savon, savon. "
                        "Lila lave avant de manger. "
                        "Après les toilettes, elle savait déjà. Elles rincen."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa et Lila ont le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Après la sieste, Lila prend le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a lavé au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami ouvre le robinet. Lila prend le savon. "
                        "Avant de manger. Après les toilettes, déjà fait. "
                        "Papa dit : bien."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Sami et Lila ont le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Après la sieste, Lila lave au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a pris le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Ils ont pris le bus. Lila a tenu le ticket. "
                "Au jardin, maman dit : avant de manger, savon. "
                "Lila lave. Après les toilettes de la gare routière, savon aussi. "
                "Elle rince. Elle essuie. Les mains sont propres."
            ),
            "q_prompt": "Après le bus, Lila prend quoi ?",
            "retry": "Savon. Avant de manger. Après les toilettes. Quoi ?",
            "pos": "Oui. Elle prend le savon. Avant de manger, et après les toilettes.",
            "wrong": "On prend le savon. Avant de manger, et après les toilettes.",
            "examples": ["savon", "du savon", "les mains", "avant de manger"],
            "fb": (
                "Le bus est loin. Les mains sentent le savon. "
                "Avant de manger. Après les toilettes."
            ),
            "ch2_prompt": "Qui se lave avec Lila ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom attend son tour. Lila a le savon. "
                        "Avant de manger. Après les toilettes. "
                        "Tom frotte ensuite."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Lila a le savon. Avant de manger. Après les toilettes. Tom aussi. L'histoire est finie.",
                        "Après la sieste, Lila lave au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a pris le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa tend la serviette. Lila a frotté au savon. "
                        "Avant de manger. Après les toilettes, pareil."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa et Lila ont le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Après la sieste, Lila prend le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a lavé au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami compte jusqu'à cinq. Lila frotte au savon. "
                        "Avant de manger. Après les toilettes. "
                        "Ils essuient ensemble."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Sami compte. Lila a le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Après la sieste, Lila lave au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a pris le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
            ],
        },
        {
            "audio": (
                "Ils ont pris la voiture. Lila a touché la ceinture. "
                "Au jardin, papa ouvre le robinet. "
                "Avant de manger, Lila prend le savon. "
                "Après les toilettes de l'aire, elle avait déjà lavé. Elle rince."
            ),
            "q_prompt": "Après la voiture, Lila prend quoi ?",
            "retry": "Savon. Avant de manger. Après les toilettes. Quoi ?",
            "pos": "Oui. Elle prend le savon. Avant de manger, et après les toilettes.",
            "wrong": "On prend le savon. Avant de manger, et après les toilettes.",
            "examples": ["savon", "du savon", "les mains", "voiture"],
            "fb": (
                "La voiture est au garage. Les mains sont propres. "
                "Savon avant de manger. Savon après les toilettes."
            ),
            "ch2_prompt": "Qui se lave avec Lila ? Tom, Léa, ou Sami ?",
            "ch2_labels": ["Tom", "Léa", "Sami"],
            "subs": [
                {
                    "audio": (
                        "Tom tient le savon. Lila frotte. "
                        "Avant de manger. Après les toilettes. "
                        "Maman dit : on peut s'asseoir."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Tom et Lila ont le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Après la sieste, Lila lave au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a pris le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Léa ouvre l'eau. Lila prend le savon. "
                        "Avant de manger. Après les toilettes. "
                        "Elles essuient sur la même serviette."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Léa et Lila ont le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Après la sieste, Lila prend le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a lavé au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
                {
                    "audio": (
                        "Sami ferme le robinet. Lila a frotté au savon. "
                        "Avant de manger. Après les toilettes. "
                        "Papa pose le panier."
                    ),
                    "ch3_prompt": "On mange quand, mains propres ? Le matin, après la sieste, ou le soir ?",
                    "ch3_labels": ["le matin", "après la sieste", "le soir"],
                    "ends": [
                        "Le matin, Sami et Lila ont le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Après la sieste, Lila lave au savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                        "Le soir, Lila a pris le savon. Avant de manger. Après les toilettes. L'histoire est finie.",
                    ],
                },
            ],
        },
    ],
}












