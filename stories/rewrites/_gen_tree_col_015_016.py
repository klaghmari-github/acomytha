#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-015 et TREE-COL-016 (texte seulement)."""
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
    "maman est là",
)
FORBIDDEN_NAMES = (
    "Adam",
    "Iris",
    "Léa",
    "Lea",
    "Tom",
    "Sami",
    "Lina",
    "Lucas",
    "Céline",
    "Celine",
    "Luca",
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
    return len(phrase.replace("'", " ").replace("’", " ").split())


def check_phrases(story_id: str, by: dict[str, list[tuple[str, str]]], max_words: int) -> None:
    bad: list[str] = []
    for cid, lines in by.items():
        for role, ph in lines:
            if "|" in ph:
                bad.append(f"{cid} pipe in phrase: {ph}")
            n = wc(ph)
            if n > max_words:
                bad.append(f"{cid} {n}w {role}|{ph}")
            if not ph.endswith((".", "?", "!")):
                bad.append(f"{cid} no end punct {role}|{ph}")
    if bad:
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:40]))


def check_text(story_id: str, by: dict[str, list[tuple[str, str]]]) -> None:
    blob = " ".join(ph for lines in by.values() for _, ph in lines)
    for s in FORBIDDEN_SUB:
        if s.lower() in blob.lower():
            raise SystemExit(f"{story_id} interdit: {s}")
    for name in FORBIDDEN_NAMES:
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{story_id} nom interdit: {name}")


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


def story_015() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}

    lieu_l1 = {
        "cuisine": [
            ("narrateur", "Aniss pousse la porte de la cuisine."),
            ("narrateur", "La vapeur de la soupe chatouille le nez."),
            ("narrateur", "Un verre d'eau tient des tiges de menthe."),
            ("narrateur", "La nappe à carreaux est un peu froissée."),
            ("papa", "Moi, je raconte la soupe."),
            ("narrateur", "Papa parle, tout près du bol."),
            ("narrateur", "Aniss a une chose à dire."),
            ("narrateur", "Il lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "L'escargot a brillé, dehors."),
            ("maman", "Oui. C'est ton tour."),
            ("maman", "Tu as attendu."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Une goutte de menthe tombe dans l'eau."),
            ("narrateur", "Le bois de la table est lisse, un peu chaud."),
        ],
        "jardin": [
            ("narrateur", "Aniss pose un pied dans l'herbe."),
            ("narrateur", "L'herbe est froide, encore mouillée."),
            ("narrateur", "La pierre garde une trace d'argent."),
            ("narrateur", "Une abeille passe, tout bas."),
            ("maman", "Moi, je raconte l'abeille."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "L'escargot est sur la pierre."),
            ("papa", "Oui. Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss se penche, tout doux."),
            ("narrateur", "La trace d'argent brille encore."),
            ("maman", "Bravo, Aniss."),
            ("maman", "Tu as levé la main."),
        ],
        "chambre": [
            ("narrateur", "Aniss entre dans la chambre."),
            ("narrateur", "Le rideau jaune filtre le soleil."),
            ("narrateur", "Le doudou attend sur l'oreiller."),
            ("narrateur", "L'oreiller sent encore le savon."),
            ("papa", "Moi, je raconte le rideau."),
            ("narrateur", "Papa parle, tout bas."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "J'ai vu l'escargot, à la fenêtre."),
            ("maman", "C'est ton tour."),
            ("maman", "On a attendu."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo."),
            ("papa", "Tu as levé la main."),
            ("narrateur", "Le doudou a une oreille un peu froissée."),
            ("narrateur", "Un carré de soleil pose sur le parquet."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Aniss veut parler, dans la cuisine."),
            ("papa", "Il fait quoi d'abord ?"),
        ],
        "jardin": [
            ("narrateur", "Aniss lève la main, dans l'herbe."),
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
            ("narrateur", "Aniss souffle un peu."),
            ("narrateur", "Sa main redescend, tout doux."),
            ("enfant-m", "J'ai attendu."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
        ],
        "jardin": [
            ("maman", "Oui."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Aniss essuie une goutte sur son genou."),
            ("enfant-m", "J'attends mon tour."),
            ("papa", "Bravo, Aniss."),
            ("papa", "La pierre est à toi, et le tour aussi."),
        ],
        "chambre": [
            ("papa", "Oui."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss hoche la tête."),
            ("enfant-m", "Chacun son tour."),
            ("maman", "On continue, tout doux."),
            ("maman", "Tu as levé la main."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Aniss prend les cubes en bois."),
            ("narrateur", "Un cube rouge fait clic."),
            ("narrateur", "Un cube jaune sent le pin."),
            ("papa", "Moi, je raconte la tour."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("papa", "C'est ton tour."),
            ("enfant-m", "Une maison pour l'escargot."),
            ("maman", "Oui. Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss pose un cube, tout droit."),
        ],
        "livre": [
            ("narrateur", "Aniss ouvre le livre."),
            ("narrateur", "La page sent le papier, un peu sec."),
            ("narrateur", "Un dessin d'escargot est là, tout gris."),
            ("maman", "Moi, je lis d'abord."),
            ("narrateur", "Maman lit jusqu'au bout."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Il a une coquille ronde."),
            ("papa", "Oui. C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss caresse la page, tout léger."),
            ("maman", "Bravo, Aniss."),
        ],
        "dinette": [
            ("narrateur", "Aniss prend la dînette."),
            ("narrateur", "Une petite assiette sonne, tout creux."),
            ("narrateur", "Une cuillère miniature est encore tiède."),
            ("papa", "Moi, je sers la soupe imaginaire."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Une feuille pour l'escargot ?"),
            ("maman", "Oui. C'est ton tour."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo."),
            ("papa", "Tu as attendu ton tour."),
            ("narrateur", "Aniss pose la petite assiette, tout doux."),
        ],
    }

    extra_jouet = {
        ("cuisine", "cubes"): "Un cube attrape un reflet de menthe.",
        ("cuisine", "livre"): "Une miette reste au bord de la page.",
        ("cuisine", "dinette"): "La petite casserole est près du vrai bol.",
        ("jardin", "cubes"): "L'herbe tache un cube, tout vert.",
        ("jardin", "livre"): "Une vraie feuille sert de marque-page.",
        ("jardin", "dinette"): "Une goutte perle au bord de l'assiette.",
        ("chambre", "cubes"): "Un cube tapote le parquet, tout doux.",
        ("chambre", "livre"): "Le rideau jaune colore la page.",
        ("chambre", "dinette"): "La petite tasse est près du doudou.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, la lumière est claire."),
            ("narrateur", "Des miettes dorées restent sur la table."),
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
        ("cuisine", "cubes", "sieste"): "Un cube fait un clic, tout petit, près du bol.",
        ("cuisine", "cubes", "soir"): "La lampe allonge l'ombre des cubes.",
        ("cuisine", "livre", "matin"): "Une miette reste collée sur la page.",
        ("cuisine", "livre", "sieste"): "Le livre est un peu chaud, comme la nappe.",
        ("cuisine", "livre", "soir"): "L'escargot du livre brille sous la lampe.",
        ("cuisine", "dinette", "matin"): "La petite casserole sent encore la menthe.",
        ("cuisine", "dinette", "sieste"): "Une cuillère miniature tremble près du bol.",
        ("cuisine", "dinette", "soir"): "La dînette fait un tout petit ding.",
        ("jardin", "cubes", "matin"): "L'herbe mouille un cube, tout vert.",
        ("jardin", "cubes", "sieste"): "Un cube sèche au soleil, près de la pierre.",
        ("jardin", "cubes", "soir"): "Un cube garde une goutte, toute ronde.",
        ("jardin", "livre", "matin"): "Une feuille vraie marque encore la page.",
        ("jardin", "livre", "sieste"): "Le livre sent l'herbe, un peu.",
        ("jardin", "livre", "soir"): "Un oiseau chante. Le livre reste ouvert.",
        ("jardin", "dinette", "matin"): "Une petite assiette a une goutte de rosée.",
        ("jardin", "dinette", "sieste"): "La dînette est tiède, au soleil.",
        ("jardin", "dinette", "soir"): "Loin de la dînette, la pierre brille encore.",
        ("chambre", "cubes", "matin"): "Un rayon pose sur la tour de cubes.",
        ("chambre", "cubes", "sieste"): "Un cube est contre l'oreiller, tout calme.",
        ("chambre", "cubes", "soir"): "L'ombre des cubes danse sur le mur.",
        ("chambre", "livre", "matin"): "Le rideau filtre la page, tout jaune.",
        ("chambre", "livre", "sieste"): "Le livre est ouvert sur la couverture.",
        ("chambre", "livre", "soir"): "La page sent le doudou, un peu.",
        ("chambre", "dinette", "matin"): "Une tasse miniature est près du lit.",
        ("chambre", "dinette", "sieste"): "La dînette attend au pied du lit.",
        ("chambre", "dinette", "soir"): "Une petite assiette reflète la veilleuse.",
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
        extra = extras[(lieu, jouet, moment)]
        extra_parts = [p.strip() for p in extra.split(". ") if p.strip()]
        extra_lines = [
            ("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in extra_parts
        ]
        return (
            moment_open[moment]
            + [
                ("narrateur", f"Aniss a encore {jouet_np[jouet]}, dans {lieu_np[lieu]}."),
            ]
            + extra_lines
            + [
                ("papa", "J'écoute encore un peu."),
                ("narrateur", "Aniss lève la main."),
                ("narrateur", "Il attend."),
                ("enfant-m", "L'escargot a une trace d'argent."),
                ("maman", "Bravo."),
                ("maman", "Tu as attendu."),
                ("maman", "Puis tu as parlé."),
                ("papa", "On peut lever la main, partout."),
                ("enfant-m", "Merci, papa."),
                ("enfant-m", "Merci, maman."),
                ("narrateur", "Aniss range " + jouet_np[jouet] + ", tout doux."),
            ]
        )

    def fin(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", f"Aniss a vécu {moment_np[moment]}, dans {lieu_np[lieu]}."),
            ("narrateur", f"Il a joué avec {jouet_np[jouet]}."),
            ("papa", "Bravo, Aniss."),
            ("papa", "C'est du bon travail."),
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
        ("narrateur", "Le volet du salon claque une fois."),
        ("narrateur", "Une odeur de menthe entre."),
        ("narrateur", "Les bottes jaunes d'Aniss gouttent dans l'entrée."),
        ("narrateur", "Une petite flaque brille, tout ronde."),
        ("narrateur", "Dehors, une pierre est encore mouillée."),
        ("narrateur", "Une trace d'argent y brille, toute fine."),
        ("narrateur", "C'est un escargot, tout lent."),
        ("narrateur", "La soupe sent bon, dans la cuisine."),
        ("narrateur", "Papa coupe la menthe, tout près."),
        ("maman", "Tu as vu tes bottes, Aniss ?"),
        ("enfant-m", "Elles sont mouillées."),
        ("papa", "La pierre brille, dehors."),
        ("narrateur", "En ce moment, Aniss est à la fenêtre."),
        ("narrateur", "Il a une chose à dire."),
        ("narrateur", "Papa parle encore de la soupe."),
        ("narrateur", "Aniss lève la main."),
        ("narrateur", "Il attend."),
        ("maman", "On lève la main."),
        ("maman", "On attend."),
        ("maman", "Puis on parle."),
        ("papa", "C'est bientôt ton tour."),
        ("enfant-m", "L'escargot a une trace."),
        ("papa", "Bravo."),
        ("papa", "Tu as attendu."),
        ("narrateur", "Le volet ne claque plus."),
        ("narrateur", "La trace d'argent reste sur la pierre."),
    ]
    sons["CHK_T0000_P0000"] = "volet,menthe"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Où va Aniss, maintenant ?"),
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
            "cuisine": "soupe,menthe",
            "jardin": "oiseau,herbe",
            "chambre": "rideau",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_jouet[(lieu, jouet)]
            by[cid_l2] = jouet_scene[jouet] + [
                ("narrateur", extra),
                ("narrateur", f"On est encore dans {lieu_np[lieu]}."),
                ("maman", "On attend."),
                ("maman", "Puis on parle."),
            ]
            sons[cid_l2] = {"cubes": "cubes", "livre": "page", "dinette": "assiette"}[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, moment in moments.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, moment)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, moment)
                sons[cid_l3] = {"matin": "oiseau", "sieste": "", "soir": "pain"}[moment]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-015",
        {
            "fil_rouge": (
                "Après la pluie, une trace d'argent brille sur la pierre. "
                "Aniss veut raconter l'escargot. Il lève la main, il attend, "
                "puis il parle, avec papa et maman."
            ),
            "title": "La trace d'argent d'Aniss",
            "characters": "Aniss, papa, maman",
            "setting": "maison et jardin, après la pluie",
        },
        by,
        sons,
        max_words=15,
    )


def story_016() -> None:
    lieux = {"P0001": "tapis", "P0002": "table", "P0003": "fenetre"}
    activites = {"P0001": "histoire", "P0002": "chanson", "P0003": "dessin"}
    doudous = {"P0001": "poupee", "P0002": "ours", "P0003": "lion"}

    lieu_l1 = {
        "tapis": [
            ("narrateur", "Victorina s'assoit sur le tapis."),
            ("narrateur", "Le tapis est épais, un peu rêche."),
            ("narrateur", "Un fil rouge dépasse, tout doux."),
            ("narrateur", "La poussière de craie brille un peu."),
            ("maman", "Moi, je raconte le tapis d'abord."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Victorina a une chose à dire."),
            ("narrateur", "Elle lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "L'oiseau est jaune, dehors."),
            ("papa", "Oui. C'est ton tour."),
            ("papa", "Tu as attendu."),
            ("maman", "On lève la main."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorina pose la paume sur le tapis."),
            ("narrateur", "Le fil rouge chatouille le poignet."),
        ],
        "table": [
            ("narrateur", "Victorina s'assoit à la table."),
            ("narrateur", "Le bois est lisse, un peu froid."),
            ("narrateur", "Le carton-tableau est collé tout près."),
            ("narrateur", "Un trait de craie jaune y tremble."),
            ("papa", "Moi, je raconte le carton."),
            ("narrateur", "Papa parle, tout calme."),
            ("narrateur", "Victorina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "La craie fait un oiseau."),
            ("maman", "Oui. Merci d'avoir attendu."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorina pose un doigt sur le bois."),
            ("narrateur", "La lampe fait un rond chaud."),
            ("papa", "Bravo, Victorina."),
            ("papa", "Tu as levé la main."),
        ],
        "fenetre": [
            ("narrateur", "Victorina s'approche de la fenêtre."),
            ("narrateur", "La pluie tapote la vitre, tout fin."),
            ("narrateur", "Un oiseau jaune tient le rebord."),
            ("narrateur", "Ses plumes sont mouillées, tout collées."),
            ("maman", "Moi, je raconte la pluie."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Victorina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Il penche la tête."),
            ("papa", "C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
            ("narrateur", "Une goutte glisse, toute lente."),
            ("narrateur", "L'oiseau reste, tout calme."),
        ],
    }

    q = {
        "tapis": [
            ("narrateur", "Sur le tapis, Victorina veut parler."),
            ("maman", "Que fait-elle d'abord ?"),
        ],
        "table": [
            ("narrateur", "À la table, Victorina lève la main."),
            ("papa", "Et après, on attend ?"),
        ],
        "fenetre": [
            ("narrateur", "Près de la fenêtre, chacun son tour."),
            ("maman", "On attend, puis on parle ?"),
        ],
    }

    conf = {
        "tapis": [
            ("maman", "Oui."),
            ("maman", "On lève la main."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorina souffle un peu."),
            ("narrateur", "Sa main redescend, tout doux."),
            ("enfant-f", "J'ai attendu."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
        ],
        "table": [
            ("papa", "Oui."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorina essuie un peu de craie."),
            ("enfant-f", "J'attends mon tour."),
            ("maman", "Bravo, Victorina."),
            ("maman", "La table est à toi, et le tour aussi."),
        ],
        "fenetre": [
            ("maman", "Oui."),
            ("maman", "On lève la main."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorina hoche la tête."),
            ("enfant-f", "Chacun son tour."),
            ("papa", "On continue, tout doux."),
            ("papa", "Tu as levé la main."),
        ],
    }

    act_scene = {
        "histoire": [
            ("narrateur", "Maman ouvre un livre d'images."),
            ("narrateur", "Une page sent le papier, un peu sec."),
            ("narrateur", "Un oiseau y est dessiné, tout jaune."),
            ("maman", "Moi, je lis l'histoire d'abord."),
            ("narrateur", "Maman lit jusqu'au bout."),
            ("narrateur", "Victorina lève la main."),
            ("narrateur", "Elle attend."),
            ("papa", "C'est ton tour."),
            ("enfant-f", "Le mien est dehors, sur le rebord."),
            ("maman", "Oui. Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorina pose un doigt sur l'image."),
        ],
        "chanson": [
            ("narrateur", "Papa tapote la table, tout léger."),
            ("narrateur", "Une chanson de pluie commence."),
            ("narrateur", "Les gouttes suivent le rythme, dehors."),
            ("papa", "Moi, je chante d'abord."),
            ("narrateur", "Papa chante jusqu'au bout."),
            ("narrateur", "Victorina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Je peux chanter l'oiseau ?"),
            ("maman", "Oui. C'est ton tour."),
            ("maman", "On a attendu."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorina chante tout bas, tout doux."),
            ("papa", "Bravo, Victorina."),
        ],
        "dessin": [
            ("narrateur", "Victorina prend un morceau de craie."),
            ("narrateur", "La craie est jaune, un peu cassée."),
            ("narrateur", "Elle fait un bruit rêche sur le carton."),
            ("maman", "Moi, je dessine d'abord un nuage."),
            ("narrateur", "Maman dessine jusqu'au bout."),
            ("narrateur", "Victorina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Un bec, et deux pattes ?"),
            ("papa", "Oui. C'est ton tour."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("maman", "Bravo."),
            ("maman", "Tu as attendu ton tour."),
            ("narrateur", "Un petit oiseau jaune apparaît."),
        ],
    }

    extra_act = {
        ("tapis", "histoire"): "Le livre repose sur le tapis, tout ouvert.",
        ("tapis", "chanson"): "Le fil rouge du tapis suit la chanson.",
        ("tapis", "dessin"): "Un peu de craie tombe sur le tapis.",
        ("table", "histoire"): "Le livre est collé contre le carton.",
        ("table", "chanson"): "La table vibre un peu, sous les doigts.",
        ("table", "dessin"): "La craie laisse une poussière sur le bois.",
        ("fenetre", "histoire"): "L'oiseau vrai regarde l'oiseau du livre.",
        ("fenetre", "chanson"): "La pluie tapote, comme un refrain.",
        ("fenetre", "dessin"): "Le trait jaune copie l'oiseau du rebord.",
    }

    doudou_open = {
        "poupee": [
            ("narrateur", "La poupée est assise, tout droite."),
            ("narrateur", "Sa robe de toile est un peu froissée."),
            ("narrateur", "Un bouton brille, tout petit."),
        ],
        "ours": [
            ("narrateur", "L'ours est brun, un peu râpé."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("narrateur", "Il sent encore le placard."),
        ],
        "lion": [
            ("narrateur", "Le lion a une crinière en laine."),
            ("narrateur", "La laine est mêlée, tout douce."),
            ("narrateur", "Un œil de bouton regarde, tout calme."),
        ],
    }

    extras = {
        ("tapis", "histoire", "poupee"): "La poupée a le livre contre les genoux.",
        ("tapis", "histoire", "ours"): "L'ours pose le nez sur une page.",
        ("tapis", "histoire", "lion"): "Le lion écoute l'histoire, tout sage.",
        ("tapis", "chanson", "poupee"): "La poupée balance un peu, au rythme.",
        ("tapis", "chanson", "ours"): "L'ours tape l'oreille, tout doux.",
        ("tapis", "chanson", "lion"): "La crinière tremble, comme un refrain.",
        ("tapis", "dessin", "poupee"): "Un point de craie tache la robe.",
        ("tapis", "dessin", "ours"): "L'ours a un trait jaune sur le ventre.",
        ("tapis", "dessin", "lion"): "Une mèche de laine a un peu de craie.",
        ("table", "histoire", "poupee"): "La poupée est assise contre le carton.",
        ("table", "histoire", "ours"): "L'ours tient le livre, tout maladroit.",
        ("table", "histoire", "lion"): "Le lion garde la page avec la patte.",
        ("table", "chanson", "poupee"): "La poupée a un ticket de papier, tout plié.",
        ("table", "chanson", "ours"): "L'ours tapote le bois, avec papa.",
        ("table", "chanson", "lion"): "Le lion fait un tout petit rrr, au refrain.",
        ("table", "dessin", "poupee"): "La poupée a un nuage dessiné au dos.",
        ("table", "dessin", "ours"): "L'ours a de la poussière jaune au museau.",
        ("table", "dessin", "lion"): "Le lion regarde l'oiseau du carton.",
        ("fenetre", "histoire", "poupee"): "La poupée regarde l'oiseau, tout près.",
        ("fenetre", "histoire", "ours"): "L'ours est chaud contre la vitre froide.",
        ("fenetre", "histoire", "lion"): "Le lion suit l'oiseau des yeux.",
        ("fenetre", "chanson", "poupee"): "La poupée écoute la pluie, et la chanson.",
        ("fenetre", "chanson", "ours"): "L'ours a une goutte sur le nez, tout petite.",
        ("fenetre", "chanson", "lion"): "La crinière frôle la vitre, tout léger.",
        ("fenetre", "dessin", "poupee"): "La poupée a un oiseau jaune sur la robe.",
        ("fenetre", "dessin", "ours"): "L'ours compare le dessin et l'oiseau vrai.",
        ("fenetre", "dessin", "lion"): "Le lion a un bec jaune, en craie, au museau.",
    }

    fin_image = {
        "poupee": "La poupée reste assise, tout calme.",
        "ours": "L'ours referme une oreille, tout lentement.",
        "lion": "Le lion garde sa crinière, tout douce.",
    }

    lieu_np = {"tapis": "le tapis", "table": "la table", "fenetre": "la fenêtre"}
    act_np = {"histoire": "l'histoire", "chanson": "la chanson", "dessin": "le dessin"}
    doudou_np = {"poupee": "la poupée", "ours": "l'ours", "lion": "le lion"}
    lieu_prep = {"tapis": "sur le tapis", "table": "à la table", "fenetre": "près de la fenêtre"}

    def l3(lieu: str, act: str, doudou: str) -> list[tuple[str, str]]:
        extra = extras[(lieu, act, doudou)]
        extra_parts = [p.strip() for p in extra.split(". ") if p.strip()]
        extra_lines = [
            ("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in extra_parts
        ]
        return (
            doudou_open[doudou]
            + [
                ("narrateur", f"Victorina a encore {doudou_np[doudou]}, {lieu_prep[lieu]}."),
            ]
            + extra_lines
            + [
                ("papa", "On dit bonjour, chacun son tour."),
                ("narrateur", "Victorina lève la main."),
                ("narrateur", "Elle attend."),
                ("enfant-f", "Bonjour. J'ai vu l'oiseau."),
                ("maman", "Bravo."),
                ("maman", "Tu as attendu."),
                ("maman", "Puis tu as parlé."),
                ("papa", "On peut lever la main, dans la petite classe."),
                ("enfant-f", "Merci, papa."),
                ("enfant-f", "Merci, maman."),
                ("narrateur", "Victorina pose " + doudou_np[doudou] + " tout près."),
            ]
        )

    def fin(lieu: str, act: str, doudou: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", f"Victorina a vécu {act_np[act]}, {lieu_prep[lieu]}."),
            ("narrateur", f"Elle a parlé avec {doudou_np[doudou]}."),
            ("papa", "Bravo, Victorina."),
            ("papa", "C'est du bon travail."),
            ("narrateur", fin_image[doudou]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "La petite classe a trois jeux."),
            ("maman", "L'histoire, la chanson, ou le dessin ?"),
            ("papa", "On écoute."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Qui écoute, tout près ?"),
            ("papa", "La poupée, l'ours, ou le lion ?"),
            ("maman", "On dit bonjour."),
            ("maman", "Chacun son tour."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Un carton est collé contre le buffet."),
        ("narrateur", "Un trait de craie jaune y reste."),
        ("narrateur", "La lampe fait un rond chaud."),
        ("narrateur", "La pluie tape la vitre, tout doux."),
        ("narrateur", "Un oiseau jaune s'est posé dehors."),
        ("narrateur", "Ses pattes tiennent le rebord."),
        ("narrateur", "La soupe mijote, tout loin, dans la cuisine."),
        ("narrateur", "Maman a mis trois coussins par terre."),
        ("papa", "C'est notre petite classe, Victorina."),
        ("maman", "Tu as vu l'oiseau ?"),
        ("enfant-f", "Il est jaune."),
        ("narrateur", "En ce moment, Victorina s'assoit."),
        ("narrateur", "Le carton est un tableau, tout simple."),
        ("narrateur", "Elle a une chose à dire."),
        ("narrateur", "Maman parle encore de la pluie."),
        ("narrateur", "Victorina lève la main."),
        ("narrateur", "Elle attend."),
        ("papa", "On lève la main."),
        ("papa", "On attend."),
        ("papa", "Puis on parle."),
        ("maman", "C'est bientôt ton tour."),
        ("enfant-f", "L'oiseau est sur le rebord."),
        ("maman", "Bravo."),
        ("maman", "Tu as attendu."),
        ("narrateur", "La craie jaune laisse un peu de poussière."),
        ("narrateur", "L'oiseau penche la tête."),
    ]
    sons["CHK_T0000_P0000"] = "pluie,craie"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Où s'assoit Victorina ?"),
        ("maman", "Le tapis, la table, ou la fenêtre ?"),
        ("papa", "On s'écoute."),
        ("papa", "On attend."),
        ("papa", "Puis on parle."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "tapis": "tapis",
            "table": "craie",
            "fenetre": "pluie,oiseau",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, act in activites.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_act[(lieu, act)]
            by[cid_l2] = act_scene[act] + [
                ("narrateur", extra),
                ("narrateur", f"On est encore {lieu_prep[lieu]}."),
                ("maman", "On attend."),
                ("maman", "Puis on parle."),
            ]
            sons[cid_l2] = {"histoire": "page", "chanson": "", "dessin": "craie"}[act]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, doudou in doudous.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, act, doudou)
                by[f"{cid_l3}_F0001"] = fin(lieu, act, doudou)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-016",
        {
            "fil_rouge": (
                "Sur le carton, une craie jaune. Dehors, un oiseau sous la pluie. "
                "Victorina veut le dire, dans la petite classe. Elle lève la main, "
                "elle attend, puis elle parle, avec papa et maman."
            ),
            "title": "La craie et l'oiseau de Victorina",
            "characters": "Victorina, papa, maman",
            "setting": "petite classe à la maison, jour de pluie",
        },
        by,
        sons,
        max_words=16,
    )


if __name__ == "__main__":
    story_015()
    story_016()
    print("ok TREE-COL-015 TREE-COL-016")
