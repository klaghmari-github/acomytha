#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-023 et TREE-COL-024 (texte seulement)."""
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
    "maman est là",
    "papa est là",
)
FORBIDDEN_NAMES = (
    "Adam",
    "Iris",
    "Lina",
    "Nora",
    "Lucas",
    "Céline",
    "Celine",
    "Luca",
    "Noé",
    "Noe",
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
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:50]))


def check_text(story_id: str, by: dict[str, list[tuple[str, str]]], extra_forbid: tuple[str, ...] = ()) -> None:
    blob = " ".join(ph for lines in by.values() for _, ph in lines)
    for s in FORBIDDEN_SUB:
        if s.lower() in blob.lower():
            raise SystemExit(f"{story_id} interdit: {s}")
    for name in FORBIDDEN_NAMES + extra_forbid:
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{story_id} nom interdit: {name}")


def sent(extra: str) -> list[tuple[str, str]]:
    parts = [p.strip() for p in extra.split(". ") if p.strip()]
    return [("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in parts]


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str],
    max_words: int,
    extra_forbid: tuple[str, ...] = (),
) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:8]} extra={extra[:8]}")
    check_phrases(story_id, by_id, max_words)
    check_text(story_id, by_id, extra_forbid)
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


def story_023() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}
    lieu_np = {"cuisine": "la cuisine", "jardin": "le jardin", "chambre": "la chambre"}
    jouet_np = {"cubes": "les cubes", "livre": "le livre", "dinette": "la dînette"}
    moment_np = {"matin": "le matin", "sieste": "après la sieste", "soir": "le soir"}

    lieu_l1 = {
        "cuisine": [
            ("narrateur", "Mila pousse la porte de la cuisine."),
            ("narrateur", "Le carrelage est un peu froid."),
            ("narrateur", "Une pomme jaune attend dans le saladier."),
            ("narrateur", "Ça sent le sucre et le bois."),
            ("narrateur", "Papa essuie encore sa manche."),
            ("enfant-f", "Bonjour, papa."),
            ("papa", "Bonjour, Mila."),
            ("papa", "Tu veux la pomme jaune ?"),
            ("enfant-f", "Oui."),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Papa pose la pomme dans sa main."),
            ("narrateur", "La peau est lisse, un peu froide."),
            ("enfant-f", "Merci, papa."),
            ("maman", "Bravo, Mila."),
            ("maman", "Tu as dit les mots."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Une goutte de jus brille sur la table."),
        ],
        "jardin": [
            ("narrateur", "Mila revient sous le pommier."),
            ("narrateur", "L'herbe colle encore à ses chaussettes."),
            ("narrateur", "Le banc de bois reste mouillé."),
            ("narrateur", "Une pomme rouge brille dans l'herbe."),
            ("enfant-f", "Bonjour, maman."),
            ("maman", "Bonjour, ma grande."),
            ("maman", "Tu veux le panier ?"),
            ("enfant-f", "Oui."),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Maman tend le panier troué."),
            ("narrateur", "L'anse est rêche, tout douce ensuite."),
            ("enfant-f", "Merci, maman."),
            ("papa", "Bravo, Mila."),
            ("papa", "Tu as dit merci."),
            ("maman", "On dit bonjour."),
            ("maman", "On dit s'il te plaît."),
            ("maman", "On dit merci."),
            ("narrateur", "Une feuille tourne, tout lentement."),
        ],
        "chambre": [
            ("narrateur", "Mila entre dans la chambre."),
            ("narrateur", "Le parquet craque, tout petit."),
            ("narrateur", "Le doudou attend sur l'oreiller."),
            ("narrateur", "Un rayon pose sur le plaid."),
            ("enfant-f", "Bonjour, doudou."),
            ("maman", "Bonjour, Mila."),
            ("maman", "Tu veux le plaid doux ?"),
            ("enfant-f", "Oui."),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Maman pose le plaid sur ses genoux."),
            ("narrateur", "Le tissu est chaud, un peu lourd."),
            ("enfant-f", "Merci, maman."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les trois mots."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "Le doudou a une oreille froissée."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Papa arrive, dans la cuisine."),
            ("maman", "Mila dit quoi ?"),
        ],
        "jardin": [
            ("narrateur", "Mila veut le panier."),
            ("papa", "Elle dit quoi ?"),
        ],
        "chambre": [
            ("narrateur", "Maman donne le plaid."),
            ("papa", "Mila dit quoi ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("papa", "Oui."),
            ("papa", "On dit bonjour."),
            ("papa", "On dit s'il te plaît."),
            ("papa", "On dit merci."),
            ("narrateur", "Mila souffle un peu."),
            ("narrateur", "La pomme jaune reste froide dans sa main."),
            ("enfant-f", "Bonjour."),
            ("enfant-f", "Merci."),
            ("maman", "Bravo, Mila."),
            ("maman", "C'est du bon travail."),
        ],
        "jardin": [
            ("maman", "Oui."),
            ("maman", "On dit s'il te plaît."),
            ("maman", "On dit merci."),
            ("narrateur", "Mila serre l'anse du panier."),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les mots."),
            ("narrateur", "Une pomme rouge roule, tout près."),
        ],
        "chambre": [
            ("papa", "Oui."),
            ("papa", "On dit merci."),
            ("papa", "On dit bonjour aussi."),
            ("narrateur", "Mila caresse le plaid, tout doux."),
            ("enfant-f", "Merci, maman."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit merci."),
            ("narrateur", "Le rayon glisse encore sur l'oreiller."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Mila prend les cubes en bois."),
            ("narrateur", "Un cube rouge sent le pin."),
            ("narrateur", "Un cube vert fait clic."),
            ("papa", "Tu veux le cube rouge ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Papa tend le cube, tout lentement."),
            ("enfant-f", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Tu as demandé."),
            ("maman", "Puis tu as dit merci."),
            ("papa", "On dit s'il te plaît."),
            ("papa", "On dit merci."),
            ("narrateur", "Mila pose le cube, tout droit."),
        ],
        "livre": [
            ("narrateur", "Mila ouvre le livre."),
            ("narrateur", "La page sent le papier, un peu sec."),
            ("narrateur", "Une pomme est dessinée, toute rouge."),
            ("maman", "On lit ensemble ?"),
            ("enfant-f", "Oui."),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Maman tourne la page, tout doux."),
            ("enfant-f", "Merci, maman."),
            ("papa", "Bravo, Mila."),
            ("papa", "Tu as dit s'il te plaît."),
            ("maman", "Et merci, maintenant."),
            ("enfant-f", "Merci."),
            ("narrateur", "Mila caresse la pomme du livre."),
        ],
        "dinette": [
            ("narrateur", "Mila prend la dînette."),
            ("narrateur", "Une petite assiette sonne, tout creux."),
            ("narrateur", "Une cuillère miniature est encore tiède."),
            ("papa", "Tu sers la soupe ?"),
            ("enfant-f", "S'il te plaît, la casserole."),
            ("maman", "Oui."),
            ("maman", "Tiens."),
            ("enfant-f", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les mots."),
            ("maman", "Bonjour, petite casserole."),
            ("enfant-f", "Bonjour."),
            ("narrateur", "Mila pose l'assiette, tout doux."),
        ],
    }

    extra_jouet = {
        ("cuisine", "cubes"): "Un cube attrape un reflet de pomme.",
        ("cuisine", "livre"): "Une goutte de jus reste au bord de la page.",
        ("cuisine", "dinette"): "La petite casserole est près du saladier.",
        ("jardin", "cubes"): "L'herbe tache un cube, tout vert.",
        ("jardin", "livre"): "Une vraie feuille sert de marque-page.",
        ("jardin", "dinette"): "Une goutte perle au bord de l'assiette.",
        ("chambre", "cubes"): "Un cube tapote le parquet, tout doux.",
        ("chambre", "livre"): "Le rayon colore la page, tout jaune.",
        ("chambre", "dinette"): "La petite tasse est près du doudou.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, la lumière est claire."),
            ("narrateur", "La rosée brille encore, tout loin."),
            ("narrateur", "Ça sent le cacao, un peu."),
            ("papa", "Bonjour, Mila."),
            ("enfant-f", "Bonjour, papa."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, les joues sont chaudes."),
            ("narrateur", "La couverture a un pli, tout doux."),
            ("narrateur", "La maison est calme, encore un peu."),
            ("maman", "Tu es réveillée ?"),
            ("enfant-f", "Oui, maman."),
        ],
        "soir": [
            ("narrateur", "Le soir, la lampe fait un rond."),
            ("narrateur", "Ça sent le pain, tout chaud."),
            ("narrateur", "Les chaussons font toc, sur le bois."),
            ("papa", "Te voilà, Mila."),
            ("enfant-f", "Bonjour, papa."),
        ],
    }

    extras = {
        ("cuisine", "cubes", "matin"): "Un cube jaune attrape le soleil sur la table.",
        ("cuisine", "cubes", "sieste"): "Un cube fait un clic, tout petit, près du bol.",
        ("cuisine", "cubes", "soir"): "La lampe allonge l'ombre des cubes.",
        ("cuisine", "livre", "matin"): "Une miette reste collée sur la page.",
        ("cuisine", "livre", "sieste"): "Le livre est un peu chaud, comme la nappe.",
        ("cuisine", "livre", "soir"): "La pomme du livre brille sous la lampe.",
        ("cuisine", "dinette", "matin"): "La petite casserole sent encore la pomme.",
        ("cuisine", "dinette", "sieste"): "Une cuillère miniature tremble près du bol.",
        ("cuisine", "dinette", "soir"): "La dînette fait un tout petit ding.",
        ("jardin", "cubes", "matin"): "L'herbe mouille un cube, tout vert.",
        ("jardin", "cubes", "sieste"): "Un cube sèche au soleil, près du banc.",
        ("jardin", "cubes", "soir"): "Un cube garde une goutte, toute ronde.",
        ("jardin", "livre", "matin"): "Une feuille vraie marque encore la page.",
        ("jardin", "livre", "sieste"): "Le livre sent l'herbe, un peu.",
        ("jardin", "livre", "soir"): "Un oiseau chante. Le livre reste ouvert.",
        ("jardin", "dinette", "matin"): "Une petite assiette a une goutte de rosée.",
        ("jardin", "dinette", "sieste"): "La dînette est tiède, au soleil.",
        ("jardin", "dinette", "soir"): "Loin de la dînette, le banc brille encore.",
        ("chambre", "cubes", "matin"): "Un rayon pose sur la tour de cubes.",
        ("chambre", "cubes", "sieste"): "Un cube est contre l'oreiller, tout calme.",
        ("chambre", "cubes", "soir"): "L'ombre des cubes danse sur le mur.",
        ("chambre", "livre", "matin"): "Le plaid filtre la page, tout jaune.",
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

    def l3(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return (
            moment_open[moment]
            + [
                ("narrateur", f"Mila a encore {jouet_np[jouet]}, dans {lieu_np[lieu]}."),
            ]
            + sent(extras[(lieu, jouet, moment)])
            + [
                ("papa", "Tu veux encore jouer ?"),
                ("enfant-f", "Oui."),
                ("enfant-f", "S'il te plaît."),
                ("maman", "Oui."),
                ("maman", "Tiens."),
                ("enfant-f", "Merci, maman."),
                ("papa", "Bravo, Mila."),
                ("papa", "Tu as dit les mots."),
                ("maman", "Bonjour."),
                ("maman", "S'il te plaît."),
                ("maman", "Merci."),
                ("enfant-f", "Merci, papa."),
                ("narrateur", "Mila range " + jouet_np[jouet] + ", tout doux."),
            ]
        )

    def fin(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "Bonjour."),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
            ("maman", "Bravo, Mila."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Mila a vécu {moment_np[moment]}, dans {lieu_np[lieu]}."),
            ("narrateur", f"Elle a joué avec {jouet_np[jouet]}."),
            ("narrateur", fin_image[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout proches."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On demande."),
            ("papa", "On dit merci."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Quel moment, maintenant ?"),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On dit encore les mots."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le banc de bois reste mouillé, sous le pommier."),
        ("narrateur", "Une goutte glisse sur le dossier."),
        ("narrateur", "Elle fait ploc dans l'herbe."),
        ("narrateur", "Une pomme jaune a une tache brune."),
        ("narrateur", "Une feuille colle à la chaussette de Mila."),
        ("narrateur", "La porte de la maison est ouverte."),
        ("narrateur", "Ça sent la soupe, tout doux."),
        ("narrateur", "Un panier a un trou, tout petit."),
        ("narrateur", "Papa essuie une pomme sur sa manche."),
        ("narrateur", "Maman pose un torchon sur la branche."),
        ("papa", "Tu sens, Mila ?"),
        ("papa", "Ça sent la pomme."),
        ("enfant-f", "Elle est froide."),
        ("maman", "Le banc est encore mouillé."),
        ("narrateur", "En ce moment, Mila touche le bois."),
        ("narrateur", "Le bois est rêche, puis lisse."),
        ("enfant-f", "Bonjour, pommier."),
        ("papa", "Bonjour, Mila."),
        ("maman", "On dit les mots, ici aussi."),
        ("maman", "Bonjour."),
        ("maman", "S'il te plaît."),
        ("maman", "Merci."),
        ("narrateur", "Une abeille passe, tout loin, tout bas."),
        ("narrateur", "Le torchon bouge un peu, sur la branche."),
    ]
    sons["CHK_T0000_P0000"] = "goutte,oiseau"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Trois coins de la maison attendent."),
        ("papa", "La cuisine, le jardin, ou la chambre ?"),
        ("maman", "On dit bonjour."),
        ("maman", "On dit merci."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "cuisine": "assiette",
            "jardin": "oiseau",
            "chambre": "",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = jouet_scene[jouet] + sent(extra_jouet[(lieu, jouet)]) + [
                ("narrateur", f"On est encore dans {lieu_np[lieu]}."),
                ("maman", "On dit s'il te plaît."),
                ("maman", "On dit merci."),
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
        "TREE-COL-023",
        {
            "fil_rouge": (
                "Sous le pommier, le banc est encore mouillé. Mila veut une pomme, "
                "un panier, un jeu. Elle dit bonjour, s'il te plaît, merci, "
                "avec papa et maman."
            ),
            "title": "Le banc mouillé et la pomme de Mila",
            "characters": "Mila, papa, maman",
            "setting": "jardin sous le pommier, puis la maison",
            "secondary_lessons": "COL.ECO.001",
        },
        by,
        sons,
        max_words=12,
        extra_forbid=("Tom", "Léa", "Lea", "Sami", "Aniss", "Sarah", "Nina"),
    )


def story_024() -> None:
    lieux = {"P0001": "sable", "P0002": "toboggan", "P0003": "balancoires"}
    jouets = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    pels = {"P0001": "Tom", "P0002": "Léa", "P0003": "Sami"}
    lieu_np = {
        "sable": "le bac à sable",
        "toboggan": "le toboggan",
        "balancoires": "les balançoires",
    }
    lieu_prep = {
        "sable": "près du bac à sable",
        "toboggan": "près du toboggan",
        "balancoires": "près des balançoires",
    }
    jouet_np = {"ballon": "le ballon", "seau": "le seau", "doudou": "le doudou"}
    pel_np = {
        "Tom": "l'ours Tom",
        "Léa": "la poupée Léa",
        "Sami": "le lion Sami",
    }

    lieu_l1 = {
        "sable": [
            ("narrateur", "Nina s'agenouille près du bac à sable."),
            ("narrateur", "Le sable est tiède, un peu rêche."),
            ("narrateur", "Un grain colle à son genou."),
            ("narrateur", "Elle se souvient de la classe."),
            ("narrateur", "La maîtresse parlait, tout près du tableau."),
            ("maitresse", "On écoute, ensemble."),
            ("narrateur", "Nina a écouté."),
            ("narrateur", "Un camarade a chuchoté, tout près."),
            ("narrateur", "Son ventre s'est serré, tout petit."),
            ("narrateur", "Elle est restée près du sable, maintenant."),
            ("enfant-f", "J'ai écouté la maîtresse."),
            ("enfant-f", "J'ai un malaise."),
            ("maman", "On aime écouter la maîtresse."),
            ("maman", "Si malaise, raconter à la maison."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as écouté."),
            ("papa", "Ensuite, tu racontes."),
            ("narrateur", "Nina laisse le sable glisser entre ses doigts."),
        ],
        "toboggan": [
            ("narrateur", "Nina pose la main sur le toboggan."),
            ("narrateur", "Le métal est un peu froid."),
            ("narrateur", "Une marche sonne, tout creux."),
            ("narrateur", "Elle revoit la classe, tout nette."),
            ("narrateur", "La maîtresse ouvrait un livre."),
            ("maitresse", "On écoute d'abord."),
            ("narrateur", "Nina a écouté jusqu'au bout."),
            ("narrateur", "Un camarade a parlé tout bas."),
            ("narrateur", "Nina a senti un malaise."),
            ("narrateur", "Ses mains sont devenues chaudes."),
            ("enfant-f", "Mon ventre s'est serré."),
            ("maman", "On aime écouter la maîtresse."),
            ("maman", "Si malaise, raconter à la maison."),
            ("papa", "On t'écoute, Nina."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Nina reste en bas du toboggan, tout calme."),
            ("enfant-f", "Je raconte à papa, ou à maman."),
        ],
        "balancoires": [
            ("narrateur", "Nina s'assoit sur la balançoire."),
            ("narrateur", "La chaîne est froide, un peu rêche."),
            ("narrateur", "Elle fait un tout petit criiiii."),
            ("narrateur", "Nina pense à l'école, encore."),
            ("narrateur", "La maîtresse disait les mots, tout doux."),
            ("maitresse", "Merci d'avoir écouté."),
            ("narrateur", "Nina a écouté."),
            ("narrateur", "Le malaise est resté, tout petit."),
            ("narrateur", "Un camarade a chuchoté près de l'oreille."),
            ("enfant-f", "J'ai un malaise, maman."),
            ("maman", "Tu as bien fait de le dire."),
            ("maman", "On aime écouter la maîtresse."),
            ("maman", "Si malaise, raconter à la maison."),
            ("papa", "Je t'écoute, Nina."),
            ("papa", "Bravo."),
            ("narrateur", "La balançoire s'arrête, tout doucement."),
        ],
    }

    q = {
        "sable": [
            ("narrateur", "Nina a un malaise."),
            ("maman", "Que fait-elle ?"),
        ],
        "toboggan": [
            ("narrateur", "À l'école, Nina écoute."),
            ("papa", "Et si malaise, on raconte à la maison ?"),
        ],
        "balancoires": [
            ("narrateur", "Nina a écouté la maîtresse."),
            ("maman", "On raconte à la maison ?"),
        ],
    }

    conf = {
        "sable": [
            ("maman", "Oui."),
            ("maman", "On aime écouter la maîtresse."),
            ("maman", "Si malaise, raconter à la maison."),
            ("narrateur", "Nina souffle."),
            ("narrateur", "Un grain de sable reste sur son genou."),
            ("enfant-f", "Je raconte à papa, ou à maman."),
            ("papa", "On t'écoute."),
            ("papa", "Bravo, Nina."),
            ("narrateur", "Le ventre se desserre un tout petit peu."),
        ],
        "toboggan": [
            ("papa", "Oui."),
            ("papa", "On aime écouter."),
            ("papa", "Si malaise, raconter à la maison."),
            ("narrateur", "Nina essuie ses mains sur son manteau."),
            ("narrateur", "Le tissu est un peu rêche."),
            ("enfant-f", "J'ai écouté."),
            ("maman", "Et tu nous racontes."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Le métal du toboggan reste froid, tout calme."),
        ],
        "balancoires": [
            ("maman", "Oui."),
            ("maman", "On aime écouter la maîtresse."),
            ("maman", "Si malaise, raconter à papa ou maman."),
            ("narrateur", "Nina hoche la tête."),
            ("narrateur", "La chaîne ne crie plus."),
            ("enfant-f", "J'écoute."),
            ("enfant-f", "Puis je raconte."),
            ("papa", "Bravo."),
            ("papa", "On continue ensemble."),
        ],
    }

    jouet_scene = {
        "ballon": [
            ("narrateur", "Nina prend le ballon."),
            ("narrateur", "Le ballon est un peu sablé."),
            ("narrateur", "Il fait poum contre le sol."),
            ("papa", "Tu veux le ballon ?"),
            ("enfant-f", "Oui."),
            ("enfant-f", "S'il te plaît."),
            ("papa", "Tiens."),
            ("enfant-f", "Merci, papa."),
            ("maman", "On aime écouter, à l'école."),
            ("maman", "Si malaise, raconter à la maison."),
            ("narrateur", "Nina serre le ballon contre son ventre."),
            ("enfant-f", "Mon ventre est encore un peu serré."),
            ("papa", "On t'écoute."),
        ],
        "seau": [
            ("narrateur", "Nina prend le seau bleu."),
            ("narrateur", "Un peu d'eau tremble au fond."),
            ("narrateur", "Le seau sonne, tout creux."),
            ("maman", "Tu verses, tout doux ?"),
            ("enfant-f", "S'il te plaît."),
            ("maman", "Oui."),
            ("enfant-f", "Merci, maman."),
            ("papa", "À l'école, on aime écouter la maîtresse."),
            ("papa", "Ensuite, si malaise, raconter à la maison."),
            ("narrateur", "Nina pose le seau près de ses genoux."),
            ("enfant-f", "J'ai écouté."),
            ("maman", "Bravo."),
            ("maman", "Tu nous racontes."),
        ],
        "doudou": [
            ("narrateur", "Nina prend le doudou."),
            ("narrateur", "Le doudou est gris, un peu sablé."),
            ("narrateur", "Une oreille est encore chaude."),
            ("enfant-f", "Doudou, j'ai un malaise."),
            ("maman", "Tu peux le dire à la maison."),
            ("maman", "Papa et maman t'écoutent."),
            ("papa", "On aime écouter la maîtresse."),
            ("papa", "Ensuite, tu racontes à la maison."),
            ("enfant-f", "Merci, papa."),
            ("enfant-f", "Merci, maman."),
            ("narrateur", "Nina serre le doudou, tout doux."),
            ("maman", "Bravo, Nina."),
        ],
    }

    extra_jouet = {
        ("sable", "ballon"): "Le ballon a une tache de sable, toute fine.",
        ("sable", "seau"): "Le seau laisse un rond mouillé dans le sable.",
        ("sable", "doudou"): "Un grain de sable colle à l'oreille du doudou.",
        ("toboggan", "ballon"): "Le ballon roule jusqu'à la première marche.",
        ("toboggan", "seau"): "Le seau sonne contre le métal, tout creux.",
        ("toboggan", "doudou"): "Le doudou s'assoit en bas du toboggan.",
        ("balancoires", "ballon"): "Le ballon attend sous la balançoire, tout sage.",
        ("balancoires", "seau"): "Le seau tremble un peu, près de la chaîne.",
        ("balancoires", "doudou"): "Le doudou a une place, sur les genoux.",
    }

    peluche = {
        "Tom": [
            ("narrateur", "Nina rejoint l'ours Tom."),
            ("narrateur", "L'ours est brun, un peu râpé."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("narrateur", "Nina l'assoit contre son genou."),
            ("enfant-f", "Tom, j'ai écouté."),
            ("enfant-f", "J'ai un malaise."),
            ("maman", "Tu peux le dire à la maison."),
            ("maman", "Papa et maman t'écoutent."),
            ("papa", "On aime écouter la maîtresse."),
            ("papa", "Si malaise, raconter à la maison."),
            ("narrateur", "Nina caresse l'oreille de l'ours."),
        ],
        "Léa": [
            ("narrateur", "Nina rejoint la poupée Léa."),
            ("narrateur", "La robe est bleue, un peu froissée."),
            ("narrateur", "Un bouton brille, tout petit."),
            ("narrateur", "Nina pose Léa sur ses genoux."),
            ("enfant-f", "Léa, j'ai écouté la maîtresse."),
            ("enfant-f", "Mon ventre est serré."),
            ("maman", "Ce n'est pas un secret pour nous."),
            ("maman", "On aime écouter la maîtresse."),
            ("maman", "Si malaise, raconter à la maison."),
            ("papa", "On t'écoute."),
            ("narrateur", "Nina lisse la robe bleue."),
            ("narrateur", "Le malaise est encore là, tout petit."),
        ],
        "Sami": [
            ("narrateur", "Nina rejoint le lion Sami."),
            ("narrateur", "La crinière est en laine, un peu mêlée."),
            ("narrateur", "Un œil de bouton regarde, tout calme."),
            ("narrateur", "Nina tient Sami contre son manteau."),
            ("enfant-f", "Sami, j'ai un malaise."),
            ("maman", "On aime écouter la maîtresse."),
            ("maman", "Ensuite, tu racontes à papa ou maman."),
            ("papa", "Je t'écoute."),
            ("papa", "Bravo, Nina."),
            ("narrateur", "Nina range une mèche de laine."),
        ],
    }

    extra_peluche = {
        ("sable", "ballon", "Tom"): "L'ours Tom a du sable sur le ventre.",
        ("sable", "ballon", "Léa"): "La poupée Léa a un grain de sable au bouton.",
        ("sable", "ballon", "Sami"): "Le lion Sami a du sable dans la crinière.",
        ("sable", "seau", "Tom"): "L'ours Tom regarde l'eau du seau, tout calme.",
        ("sable", "seau", "Léa"): "La poupée Léa a une goutte sur la robe.",
        ("sable", "seau", "Sami"): "Le lion Sami lape une goutte, tout doux.",
        ("sable", "doudou", "Tom"): "L'ours Tom se colle au doudou gris.",
        ("sable", "doudou", "Léa"): "La poupée Léa s'assoit près du doudou.",
        ("sable", "doudou", "Sami"): "Le lion Sami pose la tête sur le doudou.",
        ("toboggan", "ballon", "Tom"): "L'ours Tom roule un peu, comme le ballon.",
        ("toboggan", "ballon", "Léa"): "La poupée Léa tient le ballon, trop grand.",
        ("toboggan", "ballon", "Sami"): "Le lion Sami garde le ballon entre les pattes.",
        ("toboggan", "seau", "Tom"): "L'ours Tom a l'oreille mouillée, près du seau.",
        ("toboggan", "seau", "Léa"): "La poupée Léa a un ticket de papier dans le seau.",
        ("toboggan", "seau", "Sami"): "Le lion Sami écoute le seau, tout creux.",
        ("toboggan", "doudou", "Tom"): "L'ours Tom s'assoit en bas, près du doudou.",
        ("toboggan", "doudou", "Léa"): "La poupée Léa a la robe froissée, comme le doudou.",
        ("toboggan", "doudou", "Sami"): "Le lion Sami chauffe contre le doudou.",
        ("balancoires", "ballon", "Tom"): "L'ours Tom attend sous la balançoire, près du ballon.",
        ("balancoires", "ballon", "Léa"): "La poupée Léa a le ballon sur les genoux.",
        ("balancoires", "ballon", "Sami"): "Le lion Sami suit le ballon des yeux.",
        ("balancoires", "seau", "Tom"): "L'ours Tom a une goutte sur le nez, près du seau.",
        ("balancoires", "seau", "Léa"): "La poupée Léa tient le seau, trop lourd.",
        ("balancoires", "seau", "Sami"): "Le lion Sami a la crinière mouillée, un peu.",
        ("balancoires", "doudou", "Tom"): "L'ours Tom et le doudou partagent les genoux.",
        ("balancoires", "doudou", "Léa"): "La poupée Léa s'endort presque, près du doudou.",
        ("balancoires", "doudou", "Sami"): "Le lion Sami écoute la chaîne, tout calme, près du doudou.",
    }

    fin_image = {
        "Tom": "L'ours Tom s'endort contre le genou.",
        "Léa": "La poupée Léa garde son bouton brillant.",
        "Sami": "Le lion Sami a la crinière un peu plus sage.",
    }

    def l3(lieu: str, jouet: str, pel: str) -> list[tuple[str, str]]:
        return (
            peluche[pel]
            + sent(extra_peluche[(lieu, jouet, pel)])
            + [
                ("narrateur", f"Nina a encore {jouet_np[jouet]}, {lieu_prep[lieu]}."),
                ("enfant-f", "Papa."),
                ("enfant-f", "Maman."),
                ("enfant-f", "J'ai eu un malaise."),
                ("enfant-f", "Un camarade a chuchoté."),
                ("enfant-f", "J'ai écouté la maîtresse."),
                ("papa", "Tu as bien fait de raconter."),
                ("maman", "On aime écouter la maîtresse."),
                ("maman", "Si malaise, raconter à la maison."),
                ("papa", "Bravo, Nina."),
                ("papa", "C'est du bon travail."),
                ("enfant-f", "Merci, maman."),
                ("enfant-f", "Merci, papa."),
                ("narrateur", "Le ventre de Nina se desserre, tout doucement."),
            ]
        )

    def fin(lieu: str, jouet: str, pel: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "J'ai écouté."),
            ("enfant-f", "Puis j'ai raconté."),
            ("maman", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Nina a joué {lieu_prep[lieu]}."),
            ("narrateur", f"Elle a tenu {jouet_np[jouet]}."),
            ("narrateur", f"Elle a parlé près de {pel_np[pel]}."),
            ("narrateur", fin_image[pel]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jouets attendent, tout proches."),
            ("maman", "Le ballon, le seau, ou le doudou ?"),
            ("papa", "On joue."),
            ("papa", "Ensuite, on raconte à la maison."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois peluches écoutent, tout calmes."),
            ("maman", "Tom, Léa, ou Sami ?"),
            ("papa", "Tu t'assoies un peu."),
            ("papa", "Ensuite, tu racontes à la maison."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "La vitre de la cuisine est toute embuée."),
        ("narrateur", "La soupe fume encore, près du four."),
        ("narrateur", "Nina dessine un rond avec le doigt."),
        ("narrateur", "À travers le rond, le parc brille."),
        ("narrateur", "Un toboggan gris luit, tout loin."),
        ("narrateur", "Le manteau goutte encore, sur le crochet."),
        ("narrateur", "Le cartable est sur la chaise, un peu lourd."),
        ("narrateur", "Un crayon jaune dépasse, tout lisse."),
        ("narrateur", "Les chaussures ont encore du sable."),
        ("narrateur", "Maman essuie la table, tout lentement."),
        ("narrateur", "Papa range une cuillère dans le tiroir."),
        ("maman", "L'école est finie, Nina."),
        ("maman", "Tu as écouté la maîtresse ?"),
        ("enfant-f", "Oui, maman."),
        ("papa", "On t'écoute, ce soir."),
        ("narrateur", "En ce moment, Nina a le ventre un peu serré."),
        ("narrateur", "Elle revoit la classe, tout nette."),
        ("narrateur", "Un camarade a chuchoté, tout près."),
        ("enfant-f", "J'ai un malaise."),
        ("maman", "Tu nous racontes, d'accord ?"),
        ("enfant-f", "D'accord."),
        ("papa", "D'abord, on peut aller au parc."),
        ("papa", "Le parc est derrière la haie."),
        ("narrateur", "Le rond sur la vitre sèche, tout doux."),
    ]
    sons["CHK_T0000_P0000"] = "porte"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Le parc est tout près, derrière la haie."),
        ("maman", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ("papa", "On aime écouter la maîtresse."),
        ("papa", "Ensuite, si malaise, raconter à la maison."),
    ]
    sons["CHK_T0001_P0000"] = "enfants_parc"

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = "enfants_parc"
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = jouet_scene[jouet] + sent(extra_jouet[(lieu, jouet)]) + [
                ("narrateur", f"On est encore {lieu_prep[lieu]}."),
                ("maman", "On aime écouter la maîtresse."),
                ("maman", "Si malaise, raconter à la maison."),
            ]
            sons[cid_l2] = {"ballon": "ballon", "seau": "seau", "doudou": ""}[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, pel in pels.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, pel)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, pel)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-024",
        {
            "fil_rouge": (
                "La vitre est embuée. Nina voit le parc. À l'école, elle a écouté "
                "la maîtresse. Un camarade a chuchoté. Son ventre s'est serré. "
                "Au parc, puis à la maison, elle raconte à papa et maman."
            ),
            "title": "Le rond sur la vitre de Nina",
            "characters": "Nina, maman, papa",
            "setting": "cuisine embuée, puis le parc derrière la haie",
            "secondary_lessons": "COL.POL.001",
        },
        by,
        sons,
        max_words=16,
    )


if __name__ == "__main__":
    story_023()
    story_024()
    print("ok TREE-COL-023 TREE-COL-024")
