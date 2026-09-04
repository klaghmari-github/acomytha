#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-021 et TREE-COL-022 (texte seulement)."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FORBIDDEN_SUB = (
    "On va apprendre",
    "Voici le geste",
    "Il était une fois",
    "Ceci est l'histoire",
    "papa sourit",
    "maman sourit",
    "papa est là",
    "maman est là",
)
FORBIDDEN_NAMES = (
    "Adam", "Iris", "Léa", "Lea", "Tom", "Sami", "Lina", "Lucas",
    "Céline", "Celine", "Luca", "Jules", "Gabin", "Hugo", "Maya",
    "Nora", "Kenzo", "Zoé", "Zoe", "Sara ", "Inès", "Ines", "Noé",
    "Noe", "Marceau", "Maëlys", "Ninon", "Barnabé", "Corentin",
)


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    script = "\n".join(f"{role}|{phrase}" for role, phrase in lines)
    text = " ".join(phrase for _, phrase in lines)
    return text, script


def apply_chunk(src: dict, lines: list[tuple[str, str]], sons: str | None = None) -> dict:
    text, script = pack(lines)
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    if sons is None:
        out["sons"] = src.get("sons") or ""
    else:
        out["sons"] = sons
    return out


def wc(phrase: str) -> int:
    return len(phrase.replace("'", " ").replace("’", " ").replace("-", " ").split())


def check_phrases(story_id: str, by: dict[str, list[tuple[str, str]]], max_words: int) -> None:
    bad: list[str] = []
    allowed = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "maitresse"}
    for cid, lines in by.items():
        for role, ph in lines:
            if role not in allowed:
                bad.append(f"{cid} role {role}")
            if "|" in ph:
                bad.append(f"{cid} pipe in phrase: {ph}")
            n = wc(ph)
            if n > max_words:
                bad.append(f"{cid} {n}w {role}|{ph}")
            if not ph.endswith((".", "?", "!")):
                bad.append(f"{cid} no end punct {role}|{ph}")
            if ph.count(".") + ph.count("?") + ph.count("!") > 1:
                bad.append(f"{cid} two sentences {role}|{ph}")
    if bad:
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:50]))


def check_text(story_id: str, by: dict[str, list[tuple[str, str]]]) -> None:
    blob = " ".join(ph for lines in by.values() for _, ph in lines)
    for s in FORBIDDEN_SUB:
        if s.lower() in blob.lower():
            raise SystemExit(f"{story_id} interdit: {s}")
    for name in FORBIDDEN_NAMES:
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{story_id} nom interdit: {name}")
    joined = "\n".join(f"{r}|{p}" for lines in by.values() for r, p in lines)
    if "papa|" not in joined or "maman|" not in joined:
        raise SystemExit(f"{story_id} need papa and maman")
    adults = " ".join(p for lines in by.values() for r, p in lines if r in ("papa", "maman"))
    if "Bravo" not in adults and "bon travail" not in adults.lower():
        raise SystemExit(f"{story_id} no bravo")
    if "?" not in adults:
        raise SystemExit(f"{story_id} no adult question")
    root = " ".join(p for r, p in by["CHK_T0000_P0000"])
    if "En ce moment" not in root:
        raise SystemExit(f"{story_id} root sans « En ce moment »")


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str],
    max_words: int,
) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:8]} extra={extra[:8]}")
    check_phrases(story_id, by_id, max_words)
    check_text(story_id, by_id)
    chunks = []
    for c in source["chunks"]:
        cid = c["chunk_id"]
        chunks.append(apply_chunk(c, by_id[cid], sons_map.get(cid)))
    merged = dict(source)
    merged.update(meta)
    merged["chunks"] = chunks
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"ok {story_id} {len(chunks)} chunks")


def extra_lines(s: str) -> list[tuple[str, str]]:
    parts = [p.strip() for p in s.split(". ") if p.strip()]
    return [("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in parts]


def story_021() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}

    lieu_l1 = {
        "cuisine": [
            ("narrateur", "Victorino pousse la porte de la cuisine."),
            ("narrateur", "Le cacao fume encore, dans les tasses."),
            ("narrateur", "Une cuillère en bois est un peu collante."),
            ("narrateur", "Ça sent le pain grillé, tout doux."),
            ("papa", "Moi, je raconte le cacao."),
            ("narrateur", "Papa parle, près des tasses."),
            ("narrateur", "Victorino a une chose à dire."),
            ("narrateur", "Il lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "La flaque tient le ciel."),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "Tu as attendu."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Une goutte de cacao tombe dans la tasse."),
            ("narrateur", "Le bois de la table est tiède."),
        ],
        "jardin": [
            ("narrateur", "Victorino pose un pied dans l'herbe."),
            ("narrateur", "L'herbe est froide, encore brillante."),
            ("narrateur", "Une chaussette danse sur le fil."),
            ("narrateur", "La flaque sous la boîte tremble."),
            ("maman", "Moi, je raconte le moineau."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le ciel est dans l'eau."),
            ("papa", "Oui."),
            ("papa", "Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino se penche, tout doux."),
            ("narrateur", "Un moineau picore près du portail."),
            ("maman", "Bravo, Victorino."),
            ("maman", "Tu as levé la main."),
        ],
        "chambre": [
            ("narrateur", "Victorino entre dans la chambre."),
            ("narrateur", "La vitre est un peu embuée."),
            ("narrateur", "Le cartable repose au pied du lit."),
            ("narrateur", "Le doudou attend contre l'oreiller."),
            ("papa", "Moi, je raconte le chemin."),
            ("narrateur", "Papa parle, tout bas."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le chemin brille, derrière la vitre."),
            ("maman", "C'est ton tour."),
            ("maman", "On a attendu."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo."),
            ("papa", "Tu as levé la main."),
            ("narrateur", "Le radiateur fait un petit tic."),
            ("narrateur", "Un carré de ciel pose sur le parquet."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Victorino veut parler, près des tasses."),
            ("papa", "Il fait quoi d'abord ?"),
        ],
        "jardin": [
            ("narrateur", "Victorino lève la main, dans l'herbe."),
            ("maman", "Et après, on attend ?"),
        ],
        "chambre": [
            ("narrateur", "Chacun son tour, près du doudou."),
            ("papa", "On attend, puis on parle ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("papa", "Oui."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino souffle un peu."),
            ("narrateur", "Sa main redescend, tout doux."),
            ("enfant-m", "J'ai attendu."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("maman", "Tu as fini de souffler ?"),
            ("enfant-m", "Oui, maman."),
        ],
        "jardin": [
            ("maman", "Oui."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorino essuie une goutte sur son genou."),
            ("enfant-m", "J'attends mon tour."),
            ("papa", "Bravo, Victorino."),
            ("papa", "La flaque est à toi, et le tour aussi."),
            ("maman", "Tu as levé la main ?"),
            ("enfant-m", "Oui."),
        ],
        "chambre": [
            ("papa", "Oui."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino hoche la tête."),
            ("enfant-m", "Chacun son tour."),
            ("maman", "On continue, tout doux."),
            ("maman", "Tu as levé la main."),
            ("papa", "C'est du bon travail."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Victorino prend les cubes bleus."),
            ("narrateur", "Un nuage est collé sur un cube."),
            ("narrateur", "Le bois est froid, un peu lisse."),
            ("papa", "Moi, je raconte le ciel."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("papa", "C'est ton tour."),
            ("enfant-m", "Une tour pour la flaque."),
            ("maman", "Oui."),
            ("maman", "Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino pose le cube-nuage, tout droit."),
        ],
        "livre": [
            ("narrateur", "Victorino ouvre le livre cartonné."),
            ("narrateur", "La couverture est glacée, tout bleue."),
            ("narrateur", "Une flaque y tient un petit nuage."),
            ("maman", "Moi, je lis d'abord."),
            ("narrateur", "Maman lit jusqu'au bout."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le nuage est dans l'eau."),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino suit le nuage, du doigt."),
            ("maman", "Bravo, Victorino."),
        ],
        "dinette": [
            ("narrateur", "Victorino prend la dînette jaune."),
            ("narrateur", "Deux petites tasses copient les vraies."),
            ("narrateur", "Ça sent encore le cacao, tout près."),
            ("papa", "Moi, je sers le cacao imaginaire."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Une tasse pour le moineau ?"),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo."),
            ("papa", "Tu as attendu ton tour."),
            ("narrateur", "Victorino pose les deux tasses, tout doux."),
        ],
    }

    extra_jouet = {
        ("cuisine", "cubes"): "Un cube attrape un reflet de cacao.",
        ("cuisine", "livre"): "Une miette de pain reste au bord de la page.",
        ("cuisine", "dinette"): "La petite tasse est près des vraies tasses.",
        ("jardin", "cubes"): "L'herbe mouille un cube, tout vert.",
        ("jardin", "livre"): "Une vraie feuille sert de marque-page.",
        ("jardin", "dinette"): "Une goutte perle au bord de la tasse.",
        ("chambre", "cubes"): "Un cube tapote le parquet, tout doux.",
        ("chambre", "livre"): "La vitre embuée colore la page, tout pâle.",
        ("chambre", "dinette"): "La petite tasse est près du doudou.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, la lumière est claire."),
            ("narrateur", "Le cacao sent encore le chocolat."),
            ("narrateur", "Les oiseaux parlent déjà, tout loin."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, les joues sont chaudes."),
            ("narrateur", "La couverture a un pli, tout doux."),
            ("narrateur", "La maison est calme, encore un peu."),
        ],
        "soir": [
            ("narrateur", "Le soir, la lampe fait un rond."),
            ("narrateur", "Ça sent le pain, tout chaud."),
            ("narrateur", "Les chaussons font toc, sur le bois."),
        ],
    }

    extras = {
        ("cuisine", "cubes", "matin"): "Un cube jaune attrape le soleil sur la table.",
        ("cuisine", "cubes", "sieste"): "Un cube fait un clic, tout petit, près des tasses.",
        ("cuisine", "cubes", "soir"): "La lampe allonge l'ombre des cubes.",
        ("cuisine", "livre", "matin"): "Une miette reste collée sur la page.",
        ("cuisine", "livre", "sieste"): "Le livre est un peu chaud, comme la nappe.",
        ("cuisine", "livre", "soir"): "La flaque du livre brille sous la lampe.",
        ("cuisine", "dinette", "matin"): "La petite tasse sent encore le cacao.",
        ("cuisine", "dinette", "sieste"): "Une cuillère miniature tremble près du bol.",
        ("cuisine", "dinette", "soir"): "La dînette fait un tout petit ding.",
        ("jardin", "cubes", "matin"): "L'herbe mouille un cube, tout vert.",
        ("jardin", "cubes", "sieste"): "Un cube sèche au soleil, près de la flaque.",
        ("jardin", "cubes", "soir"): "Un cube garde une goutte, toute ronde.",
        ("jardin", "livre", "matin"): "Une feuille vraie marque encore la page.",
        ("jardin", "livre", "sieste"): "Le livre sent l'herbe, un peu.",
        ("jardin", "livre", "soir"): "Un oiseau chante.",
        ("jardin", "dinette", "matin"): "Une petite tasse a une goutte de rosée.",
        ("jardin", "dinette", "sieste"): "La dînette est tiède, au soleil.",
        ("jardin", "dinette", "soir"): "Loin de la dînette, la flaque tient encore le ciel.",
        ("chambre", "cubes", "matin"): "Un rayon pose sur la tour de cubes.",
        ("chambre", "cubes", "sieste"): "Un cube est contre l'oreiller, tout calme.",
        ("chambre", "cubes", "soir"): "L'ombre des cubes danse sur le mur.",
        ("chambre", "livre", "matin"): "La vitre filtre la page, tout pâle.",
        ("chambre", "livre", "sieste"): "Le livre est ouvert sur la couverture.",
        ("chambre", "livre", "soir"): "La page sent le doudou, un peu.",
        ("chambre", "dinette", "matin"): "Une tasse miniature est près du lit.",
        ("chambre", "dinette", "sieste"): "La dînette attend au pied du lit.",
        ("chambre", "dinette", "soir"): "Une petite tasse reflète la veilleuse.",
    }

    child_l3 = {
        ("cuisine", "cubes", "matin"): "Ma tour est jaune, comme le cacao.",
        ("cuisine", "cubes", "sieste"): "Le cube est chaud, près de moi.",
        ("cuisine", "cubes", "soir"): "L'ombre des cubes est longue.",
        ("cuisine", "livre", "matin"): "La flaque du livre a un nuage.",
        ("cuisine", "livre", "sieste"): "La page est tiède.",
        ("cuisine", "livre", "soir"): "La lampe lit avec nous.",
        ("cuisine", "dinette", "matin"): "Le cacao imaginaire est chaud.",
        ("cuisine", "dinette", "sieste"): "La petite tasse a dormi.",
        ("cuisine", "dinette", "soir"): "La dînette fait ding.",
        ("jardin", "cubes", "matin"): "Le cube a de l'herbe.",
        ("jardin", "cubes", "sieste"): "Le cube sèche, tout seul.",
        ("jardin", "cubes", "soir"): "Le cube a une goutte.",
        ("jardin", "livre", "matin"): "Une vraie feuille est dans le livre.",
        ("jardin", "livre", "sieste"): "Le livre sent l'herbe.",
        ("jardin", "livre", "soir"): "L'oiseau a fini sa phrase.",
        ("jardin", "dinette", "matin"): "La rosée est dans la tasse.",
        ("jardin", "dinette", "sieste"): "La tasse est tiède.",
        ("jardin", "dinette", "soir"): "La flaque tient encore le ciel.",
        ("chambre", "cubes", "matin"): "Le soleil est sur ma tour.",
        ("chambre", "cubes", "sieste"): "Le cube a dormi aussi.",
        ("chambre", "cubes", "soir"): "Les cubes dansent au mur.",
        ("chambre", "livre", "matin"): "La vitre a un nuage.",
        ("chambre", "livre", "sieste"): "Le livre est sur la couverture.",
        ("chambre", "livre", "soir"): "Le doudou écoute la page.",
        ("chambre", "dinette", "matin"): "La tasse est près du lit.",
        ("chambre", "dinette", "sieste"): "La dînette a attendu.",
        ("chambre", "dinette", "soir"): "La veilleuse est dans la tasse.",
    }

    fin_image = {
        "matin": "Un oiseau picore encore, tout loin.",
        "sieste": "La couverture redescend, tout calme.",
        "soir": "La lampe reste allumée, tout doux.",
    }

    jouet_np = {"cubes": "les cubes", "livre": "le livre", "dinette": "la dînette"}
    moment_np = {"matin": "le matin", "sieste": "après la sieste", "soir": "le soir"}
    lieu_np = {"cuisine": "la cuisine", "jardin": "le jardin", "chambre": "la chambre"}

    def l3(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return (
            moment_open[moment]
            + [
                ("narrateur", f"Victorino a encore {jouet_np[jouet]}, dans {lieu_np[lieu]}."),
            ]
            + extra_lines(extras[(lieu, jouet, moment)])
            + [
                ("papa", "J'écoute encore un peu."),
                ("narrateur", "Victorino lève la main."),
                ("narrateur", "Il attend."),
                ("enfant-m", child_l3[(lieu, jouet, moment)]),
                ("maman", "Bravo."),
                ("maman", "Tu as attendu."),
                ("maman", "Puis tu as parlé."),
                ("papa", "On peut lever la main, partout."),
                ("enfant-m", "Merci, papa."),
                ("enfant-m", "Merci, maman."),
                ("narrateur", "Victorino range " + jouet_np[jouet] + ", tout doux."),
            ]
        )

    def fin(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", f"Victorino a vécu {moment_np[moment]}, dans {lieu_np[lieu]}."),
            ("narrateur", f"Il a joué avec {jouet_np[jouet]}."),
            ("papa", "Bravo, Victorino."),
            ("papa", "C'est du bon travail."),
            ("maman", "Bonne journée, mon grand."),
            ("narrateur", fin_image[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout proches."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On joue."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Quel moment, maintenant ?"),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On lève la main."),
            ("maman", "Chacun son tour."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Une flaque tient le ciel, sous la boîte."),
        ("narrateur", "Le ciré jaune pend au crochet."),
        ("narrateur", "Le capuchon goutte, tout lourd."),
        ("narrateur", "Un gant de laine chauffe sur le radiateur."),
        ("narrateur", "Ça sent le cacao, tout chaud."),
        ("narrateur", "La vapeur embue la vitre de la porte."),
        ("narrateur", "Le cartable attend sur la première marche."),
        ("narrateur", "Dehors, le chemin de l'école brille."),
        ("narrateur", "Une feuille jaune colle au portail."),
        ("papa", "Ton gant est tout chaud, Victorino."),
        ("maman", "Tu as vu la flaque ?"),
        ("enfant-m", "Elle tient le ciel."),
        ("maman", "Oui."),
        ("maman", "Elle est ronde, comme un miroir."),
        ("narrateur", "Papa pose deux tasses près de la vitre."),
        ("narrateur", "Le cacao fait un petit nuage."),
        ("narrateur", "En ce moment, Victorino est dans l'entrée."),
        ("narrateur", "Il a une chose à dire."),
        ("enfant-m", "J'ai une chose."),
        ("papa", "On lève la main."),
        ("papa", "On attend."),
        ("papa", "Puis on parle."),
        ("maman", "Tu peux lever la main."),
        ("narrateur", "Papa parle déjà, tout doucement."),
        ("narrateur", "Victorino lève la main."),
        ("narrateur", "Il attend."),
        ("maman", "Bravo."),
        ("maman", "C'est ton tour."),
        ("enfant-m", "Le chemin brille, dehors."),
        ("papa", "Tu as attendu."),
        ("papa", "Puis tu as parlé."),
        ("narrateur", "Une goutte tombe encore du capuchon."),
        ("maman", "On reste un moment, à la maison."),
    ]
    sons["CHK_T0000_P0000"] = "goutte,cacao"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Où va Victorino, maintenant ?"),
        ("papa", "La cuisine, le jardin, ou la chambre ?"),
        ("maman", "On s'écoute."),
        ("maman", "On attend."),
        ("maman", "Puis on parle."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "cuisine": "cacao,pain",
            "jardin": "oiseau,herbe",
            "chambre": "radiateur",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_jouet[(lieu, jouet)]
            by[cid_l2] = jouet_scene[jouet] + extra_lines(extra) + [
                ("narrateur", f"On est encore dans {lieu_np[lieu]}."),
                ("maman", "On attend."),
                ("maman", "Puis on parle."),
            ]
            sons[cid_l2] = {"cubes": "cubes", "livre": "page", "dinette": "tasse"}[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, moment in moments.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, moment)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, moment)
                sons[cid_l3] = {"matin": "oiseau", "sieste": "", "soir": "pain"}[moment]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-021",
        {
            "fil_rouge": (
                "Une flaque tient le ciel, sous la boîte. "
                "Victorino rentre. Il lève la main, il attend, "
                "puis il parle, avec papa et maman."
            ),
            "title": "La flaque et le ciré de Victorino",
            "characters": "Victorino, papa, maman",
            "setting": "maison après la pluie, avant l'école",
        },
        by,
        sons,
        max_words=10,
    )


def story_022() -> None:
    lieux = {"P0001": "boulangerie", "P0002": "etal", "P0003": "fromagerie"}
    gens = {"P0001": "boulangere", "P0002": "voisin", "P0003": "maitresse"}
    choses = {"P0001": "pain", "P0002": "pomme", "P0003": "fromage"}

    lieu_np = {
        "boulangerie": "la boulangerie",
        "etal": "l'étal",
        "fromagerie": "la fromagerie",
    }
    gen_np = {
        "boulangere": "la boulangère",
        "voisin": "le voisin",
        "maitresse": "la maîtresse",
    }
    chose_np = {"pain": "le pain", "pomme": "une pomme", "fromage": "un fromage"}

    lieu_l1 = {
        "boulangerie": [
            ("narrateur", "Nina pousse la porte de la boulangerie."),
            ("narrateur", "Ça sent le beurre, tout chaud."),
            ("narrateur", "Un pain de seigle a une croûte sombre."),
            ("narrateur", "Des graines de pavot restent sur la planche."),
            ("narrateur", "Une pelle en bois est encore farinée."),
            ("maman", "On dit bonjour, Nina."),
            ("enfant-f", "Bonjour."),
            ("papa", "Bonjour."),
            ("narrateur", "Un petit pain au pavot attend dans le panier."),
            ("enfant-f", "Celui-là."),
            ("maman", "Tu demandes, Nina ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Le sachet craque, un peu gras."),
            ("narrateur", "Le seigle est encore tiède."),
            ("enfant-f", "Merci."),
            ("papa", "Merci."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as dit les trois mots."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Le sachet pèse un peu, dans le panier."),
        ],
        "etal": [
            ("narrateur", "Nina s'arrête devant l'étal."),
            ("narrateur", "Des pommes rouges brillent, tout rondes."),
            ("narrateur", "Une balance de fer fait clic."),
            ("narrateur", "Ça sent le thym, tout sec."),
            ("papa", "On dit bonjour, d'accord ?"),
            ("enfant-f", "Bonjour."),
            ("maman", "Bonjour."),
            ("narrateur", "Une pomme a une petite tache dorée."),
            ("enfant-f", "Celle-là."),
            ("maman", "Tu la demandes ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "La pomme tombe dans le panier, tout doux."),
            ("enfant-f", "Merci."),
            ("papa", "Merci."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit bonjour."),
            ("maman", "Tu as dit s'il te plaît."),
            ("maman", "Tu as dit merci."),
            ("narrateur", "Le cordon rouge tape contre la jambe."),
            ("papa", "Les mots gentils, à l'étal aussi."),
        ],
        "fromagerie": [
            ("narrateur", "Nina entre à la fromagerie."),
            ("narrateur", "Ça sent le lait, tout doux."),
            ("narrateur", "Un fromage rond repose sur une feuille."),
            ("narrateur", "Le marbre du comptoir est froid."),
            ("maman", "On salue, Nina."),
            ("enfant-f", "Bonjour."),
            ("papa", "Bonjour."),
            ("narrateur", "Un petit fromage blanc attend, tout lisse."),
            ("enfant-f", "Celui-là."),
            ("papa", "Tu demandes ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Le papier d'emballage fait un froissement."),
            ("enfant-f", "Merci."),
            ("maman", "Merci."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as dit les trois mots."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "Le fromage est frais, contre le pain."),
        ],
    }

    q = {
        "boulangerie": [
            ("narrateur", "À la boulangerie, Nina parle."),
            ("maman", "Quels mots ?"),
        ],
        "etal": [
            ("narrateur", "À l'étal, Nina demande."),
            ("papa", "Quels mots ?"),
        ],
        "fromagerie": [
            ("narrateur", "À la fromagerie, Nina salue."),
            ("maman", "Quels mots ?"),
        ],
    }

    conf = {
        "boulangerie": [
            ("narrateur", "Nina a dit bonjour."),
            ("narrateur", "Elle a dit s'il te plaît."),
            ("narrateur", "Elle a dit merci."),
            ("maman", "Tu as dit les trois mots."),
            ("maman", "Bravo."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("enfant-f", "Merci, papa."),
            ("maman", "On continue, tout doux."),
        ],
        "etal": [
            ("papa", "Oui."),
            ("papa", "Les trois mots."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "La pomme brille encore dans le panier."),
            ("enfant-f", "J'ai dit merci."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("maman", "Tu as fini de tenir le panier ?"),
            ("enfant-f", "Oui, maman."),
        ],
        "fromagerie": [
            ("narrateur", "Nina a salué."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les mots."),
            ("enfant-f", "Les trois mots."),
            ("narrateur", "Le marbre reste froid sous les doigts."),
            ("maman", "Même à la fromagerie."),
        ],
    }

    gen_scene = {
        "boulangere": [
            ("narrateur", "La boulangère a de la farine sur le tablier."),
            ("narrateur", "Elle incline la tête, tout doux."),
            ("enfant-f", "Bonjour."),
            ("papa", "Bonjour."),
            ("maman", "Tu demandes, Nina ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Le bois du comptoir est lisse, un peu fariné."),
            ("enfant-f", "Merci."),
            ("maman", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les trois mots."),
        ],
        "voisin": [
            ("narrateur", "Le voisin tient un filet de poireaux."),
            ("narrateur", "Les poireaux ont encore de la terre."),
            ("narrateur", "Il lève la main, tout amical."),
            ("enfant-f", "Bonjour."),
            ("maman", "Bonjour."),
            ("papa", "Tu parles au voisin, Nina ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Le panier, un peu."),
            ("narrateur", "Nina recule d'un pas, pour laisser passer."),
            ("enfant-f", "Merci."),
            ("papa", "Merci."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as dit les mots."),
        ],
        "maitresse": [
            ("narrateur", "La maîtresse a un panier en osier."),
            ("narrateur", "Un brin de thym dépasse, tout sec."),
            ("maitresse", "Bonjour, Nina."),
            ("enfant-f", "Bonjour."),
            ("papa", "Bonjour."),
            ("maman", "Tu demandes, Nina ?"),
            ("enfant-f", "S'il te plaît."),
            ("maitresse", "Oui."),
            ("narrateur", "Nina serre le cordon rouge du panier."),
            ("enfant-f", "Merci."),
            ("maman", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit bonjour."),
            ("papa", "Tu as dit s'il te plaît."),
            ("papa", "Tu as dit merci."),
        ],
    }

    extra_gen = {
        ("boulangerie", "boulangere"): "La farine poudre encore le tablier, tout blanc.",
        ("boulangerie", "voisin"): "Le voisin sent le pain chaud, lui aussi.",
        ("boulangerie", "maitresse"): "La maîtresse s'arrête près du seigle.",
        ("etal", "boulangere"): "La boulangère passe, un sachet encore tiède au bras.",
        ("etal", "voisin"): "Le voisin pèse un poireau, tout lentement.",
        ("etal", "maitresse"): "La maîtresse touche une pomme, tout léger.",
        ("fromagerie", "boulangere"): "La boulangère choisit un fromage, tout près.",
        ("fromagerie", "voisin"): "Le voisin pose son filet sur le marbre froid.",
        ("fromagerie", "maitresse"): "La maîtresse sent le lait, tout doux.",
    }

    chose_open = {
        "pain": [
            ("narrateur", "Le pain est encore chaud, dans le papier."),
            ("narrateur", "La croûte fait un petit craquant."),
            ("narrateur", "Ça sent le four, tout bon."),
        ],
        "pomme": [
            ("narrateur", "La pomme est lisse, un peu froide."),
            ("narrateur", "Elle a une tache dorée, toute petite."),
            ("narrateur", "Ça sent le sucré, tout léger."),
        ],
        "fromage": [
            ("narrateur", "Le fromage est frais, dans son papier."),
            ("narrateur", "Le papier fait un froissement, tout doux."),
            ("narrateur", "Ça sent le lait, tout près."),
        ],
    }

    extras = {
        ("boulangerie", "boulangere", "pain"): "Le sachet tiède reste près du tablier fariné.",
        ("boulangerie", "boulangere", "pomme"): "Une pomme brille à côté du pain, sur le bois.",
        ("boulangerie", "boulangere", "fromage"): "Le fromage est frais, contre le pain chaud.",
        ("boulangerie", "voisin", "pain"): "Le voisin lève son filet, pour laisser le pain.",
        ("boulangerie", "voisin", "pomme"): "Une pomme roule vers le filet de poireaux.",
        ("boulangerie", "voisin", "fromage"): "Le fromage sent le lait, près des poireaux.",
        ("boulangerie", "maitresse", "pain"): "La maîtresse sent le four, tout près du sachet.",
        ("boulangerie", "maitresse", "pomme"): "La pomme tape le panier d'osier, tout léger.",
        ("boulangerie", "maitresse", "fromage"): "Le fromage est frais, près du brin de thym.",
        ("etal", "boulangere", "pain"): "Le pain tiède croise les pommes, à l'étal.",
        ("etal", "boulangere", "pomme"): "La boulangère regarde la pomme, toute ronde.",
        ("etal", "boulangere", "fromage"): "Le fromage est posé près des pommes rouges.",
        ("etal", "voisin", "pain"): "Le voisin pose le pain près de la balance.",
        ("etal", "voisin", "pomme"): "La pomme fait clic, sur la balance de fer.",
        ("etal", "voisin", "fromage"): "Le fromage est frais, près du filet de poireaux.",
        ("etal", "maitresse", "pain"): "Le pain chauffe le panier d'osier, un peu.",
        ("etal", "maitresse", "pomme"): "La maîtresse pose la pomme, tout doux, dans le panier.",
        ("etal", "maitresse", "fromage"): "Le fromage rejoint le thym, dans l'osier.",
        ("fromagerie", "boulangere", "pain"): "Le pain chaud rencontre le marbre froid.",
        ("fromagerie", "boulangere", "pomme"): "Une pomme brille sur le marbre, près du lait.",
        ("fromagerie", "boulangere", "fromage"): "La boulangère incline la tête, près du fromage rond.",
        ("fromagerie", "voisin", "pain"): "Le voisin pose le pain sur le marbre, tout calme.",
        ("fromagerie", "voisin", "pomme"): "La pomme roule vers le filet, puis s'arrête.",
        ("fromagerie", "voisin", "fromage"): "Le fromage est frais, contre les poireaux.",
        ("fromagerie", "maitresse", "pain"): "Le pain sent le four, dans la fromagerie.",
        ("fromagerie", "maitresse", "pomme"): "La pomme est lisse, près du brin de thym.",
        ("fromagerie", "maitresse", "fromage"): "Le fromage rond rejoint le panier d'osier.",
    }

    child_l3 = {
        ("boulangerie", "boulangere", "pain"): "Un pain, s'il te plaît.",
        ("boulangerie", "boulangere", "pomme"): "Une pomme, s'il te plaît.",
        ("boulangerie", "boulangere", "fromage"): "Un fromage, s'il te plaît.",
        ("boulangerie", "voisin", "pain"): "Le pain est chaud.",
        ("boulangerie", "voisin", "pomme"): "La pomme est ronde.",
        ("boulangerie", "voisin", "fromage"): "Le fromage est frais.",
        ("boulangerie", "maitresse", "pain"): "Le pain, s'il te plaît.",
        ("boulangerie", "maitresse", "pomme"): "La pomme, s'il te plaît.",
        ("boulangerie", "maitresse", "fromage"): "Le fromage, s'il te plaît.",
        ("etal", "boulangere", "pain"): "Le pain, s'il te plaît.",
        ("etal", "boulangere", "pomme"): "Une pomme, s'il te plaît.",
        ("etal", "boulangere", "fromage"): "Un fromage, s'il te plaît.",
        ("etal", "voisin", "pain"): "Le pain est tiède.",
        ("etal", "voisin", "pomme"): "La pomme fait clic.",
        ("etal", "voisin", "fromage"): "Le fromage sent le lait.",
        ("etal", "maitresse", "pain"): "Le pain, s'il te plaît.",
        ("etal", "maitresse", "pomme"): "La pomme, s'il te plaît.",
        ("etal", "maitresse", "fromage"): "Le fromage, s'il te plaît.",
        ("fromagerie", "boulangere", "pain"): "Le pain, s'il te plaît.",
        ("fromagerie", "boulangere", "pomme"): "Une pomme, s'il te plaît.",
        ("fromagerie", "boulangere", "fromage"): "Un fromage, s'il te plaît.",
        ("fromagerie", "voisin", "pain"): "Le pain est chaud.",
        ("fromagerie", "voisin", "pomme"): "La pomme est lisse.",
        ("fromagerie", "voisin", "fromage"): "Le fromage est rond.",
        ("fromagerie", "maitresse", "pain"): "Le pain, s'il te plaît.",
        ("fromagerie", "maitresse", "pomme"): "La pomme, s'il te plaît.",
        ("fromagerie", "maitresse", "fromage"): "Le fromage, s'il te plaît.",
    }

    fin_image = {
        "pain": "Le sachet reste tiède, contre le panier.",
        "pomme": "La pomme brille encore, tout ronde.",
        "fromage": "Le papier du fromage fait un dernier froissement.",
    }

    def l3(lieu: str, gen: str, chose: str) -> list[tuple[str, str]]:
        lines = list(chose_open[chose])
        lines.append(
            ("narrateur", f"Nina est avec {gen_np[gen]}, à {lieu_np[lieu]}.")
        )
        lines.extend(extra_lines(extras[(lieu, gen, chose)]))
        lines.append(("enfant-f", "Bonjour."))
        if gen == "maitresse":
            lines.append(("maitresse", "Bonjour, Nina."))
        else:
            lines.append(("papa", "Bonjour."))
        lines.append(("enfant-f", child_l3[(lieu, gen, chose)]))
        lines.append(("maman", "Voilà."))
        lines.append(("enfant-f", "Merci."))
        lines.append(("maman", "Bravo, Nina."))
        lines.append(("maman", "Tu as dit les trois mots."))
        lines.append(("papa", "Bonjour."))
        lines.append(("papa", "S'il te plaît."))
        lines.append(("papa", "Merci."))
        lines.append(("enfant-f", "Merci, papa."))
        lines.append(("enfant-f", "Merci, maman."))
        lines.append(("narrateur", f"Nina range {chose_np[chose]} dans le panier."))
        return lines

    def fin(lieu: str, gen: str, chose: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as dit bonjour."),
            ("papa", "Tu as dit s'il te plaît."),
            ("enfant-f", "Et merci."),
            ("narrateur", f"Nina a vécu {lieu_np[lieu]}, avec {gen_np[gen]}."),
            ("narrateur", f"Elle a {chose_np[chose]}, dans le panier."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("maman", "Bonne journée, ma grande."),
            ("narrateur", fin_image[chose]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois personnes sont là, tout près."),
            ("maman", "La boulangère, le voisin, ou la maîtresse ?"),
            ("papa", "On dit bonjour."),
            ("papa", "On dit s'il te plaît."),
            ("papa", "On dit merci."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Le panier peut recevoir trois choses."),
            ("papa", "Le pain, une pomme, ou un fromage ?"),
            ("maman", "On demande, tout gentiment."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Un grain de sel reste sur une planche."),
        ("narrateur", "L'huile d'olive y fait un petit rond."),
        ("narrateur", "Un cordon rouge borde le panier."),
        ("narrateur", "Une clochette de vélo tinte, tout loin."),
        ("narrateur", "Ça sent le thym, tout sec."),
        ("narrateur", "Un pot de miel est tout doré."),
        ("narrateur", "Le store rayé claque une fois."),
        ("narrateur", "Des citrons jaunes dorment dans une caisse."),
        ("papa", "Tu as vu le miel, Nina ?"),
        ("enfant-f", "Il est tout doré."),
        ("maman", "On tient le panier, près de moi."),
        ("narrateur", "Papa range les pièces dans une petite bourse."),
        ("narrateur", "La bourse est douce, un peu lourde."),
        ("narrateur", "En ce moment, Nina pose le pied au marché."),
        ("narrateur", "Les planches sentent le bois et le sel."),
        ("maman", "On dit bonjour, d'accord ?"),
        ("enfant-f", "Bonjour."),
        ("papa", "Et si tu veux le miel ?"),
        ("enfant-f", "S'il te plaît."),
        ("maman", "Bravo."),
        ("maman", "Et après ?"),
        ("enfant-f", "Merci."),
        ("papa", "Bonjour."),
        ("papa", "S'il te plaît."),
        ("papa", "Merci."),
        ("narrateur", "Le cordon rouge tape contre la jambe."),
        ("maman", "Nina aime les mots gentils."),
        ("papa", "Toi aussi, tu les connais."),
        ("enfant-f", "Oui, papa."),
        ("narrateur", "Un citron roule, puis s'arrête."),
        ("maman", "Tu es prête ?"),
        ("enfant-f", "Oui, maman."),
    ]
    sons["CHK_T0000_P0000"] = "clochette,store"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Où va Nina, d'abord ?"),
        ("papa", "La boulangerie, l'étal, ou la fromagerie ?"),
        ("maman", "On dit les trois mots."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "boulangerie": "cloche,papier",
            "etal": "balance",
            "fromagerie": "papier",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, gen in gens.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_gen[(lieu, gen)]
            by[cid_l2] = gen_scene[gen] + extra_lines(extra) + [
                ("narrateur", f"On est encore à {lieu_np[lieu]}."),
                ("maman", "Bonjour."),
                ("maman", "S'il te plaît."),
                ("maman", "Merci."),
            ]
            sons[cid_l2] = ""
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, chose in choses.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, gen, chose)
                by[f"{cid_l3}_F0001"] = fin(lieu, gen, chose)
                sons[cid_l3] = {"pain": "papier", "pomme": "", "fromage": "papier"}[chose]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-022",
        {
            "fil_rouge": (
                "Un grain de sel reste sur une planche. "
                "Nina tient le panier au marché. "
                "Elle dit bonjour, s'il te plaît, merci."
            ),
            "title": "Le grain de sel et le panier de Nina",
            "characters": "Nina, maman, papa",
            "setting": "marché, planches et store rayé",
        },
        by,
        sons,
        max_words=16,
    )


if __name__ == "__main__":
    story_021()
    story_022()
