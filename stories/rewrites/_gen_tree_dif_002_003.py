#!/usr/bin/env python3
"""Génère merged.json pour TREE-DIF-002 et TREE-DIF-003 (texte seulement)."""
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
    "Hugo",
    "Sami",
    "Tom",
    "Léa",
    "Lea",
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


def story_002() -> None:
    lieux = {"P0001": "sable", "P0002": "toboggan", "P0003": "balancoires"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    couleurs = {"P0001": "rouge", "P0002": "bleu", "P0003": "vert"}
    lieu_np = {
        "sable": "le bac à sable",
        "toboggan": "le toboggan",
        "balancoires": "les balançoires",
    }
    jouet_np = {"cubes": "les cubes", "livre": "le livre", "dinette": "la dînette"}
    couleur_np = {"rouge": "le rouge", "bleu": "le bleu", "vert": "le vert"}

    lieu_l1 = {
        "sable": [
            ("narrateur", "Amir s'agenouille près du bac à sable."),
            ("narrateur", "Le sable est frais, un peu rêche."),
            ("narrateur", "Un grain colle à son genou."),
            ("narrateur", "Nino s'assoit à côté, tout calme."),
            ("narrateur", "Nino a un corps plus rond."),
            ("narrateur", "Amir a des bras plus minces."),
            ("papa", "On joue ensemble."),
            ("papa", "Le corps n'est pas une blague."),
            ("enfant-m", "On joue."),
            ("copain", "On joue."),
            ("narrateur", "Ils remplissent un moule, chacun."),
            ("narrateur", "Le sable sent la terre mouillée."),
            ("maman", "Bravo, Amir."),
            ("maman", "Tu as invité Nino."),
            ("papa", "L'amitié ne dépend pas de la forme."),
            ("narrateur", "Un gâteau de sable tient, tout doux."),
            ("enfant-m", "Il est beau."),
            ("copain", "Le mien aussi."),
            ("maman", "Vous jouez."),
            ("maman", "C'est ça."),
            ("narrateur", "Une fourmi passe au bord du bac."),
        ],
        "toboggan": [
            ("narrateur", "Amir pose la main sur le toboggan."),
            ("narrateur", "Le métal est un peu froid."),
            ("narrateur", "Une marche sonne, tout creux."),
            ("narrateur", "Nino attend en bas, tout sage."),
            ("narrateur", "Nino a un corps plus mince."),
            ("narrateur", "Amir s'assoit à côté, un moment."),
            ("papa", "On joue, chacun son tour."),
            ("papa", "Le corps n'est pas une blague."),
            ("enfant-m", "Tu glisses ?"),
            ("copain", "Oui."),
            ("narrateur", "Nino glisse, tout doux."),
            ("narrateur", "Puis Amir glisse, tout doux."),
            ("maman", "Bravo."),
            ("maman", "Vous avez attendu."),
            ("papa", "On joue ensemble."),
            ("papa", "On ne commente pas le corps."),
            ("enfant-m", "Encore ?"),
            ("copain", "Encore."),
            ("narrateur", "Le métal reste froid sous les mains."),
            ("maman", "C'est du bon travail."),
        ],
        "balancoires": [
            ("narrateur", "Amir s'assoit sur la balançoire."),
            ("narrateur", "La chaîne est froide, un peu rêche."),
            ("narrateur", "Elle fait un tout petit criiiii."),
            ("narrateur", "Une feuille tombe du pommier."),
            ("narrateur", "Nino pousse tout doux, tout près."),
            ("narrateur", "Nino a une autre forme, tout simplement."),
            ("papa", "On joue ensemble."),
            ("papa", "Le corps n'est pas une blague."),
            ("enfant-m", "Merci, Nino."),
            ("copain", "À moi ?"),
            ("maman", "Oui."),
            ("maman", "Chacun son tour."),
            ("narrateur", "Ils échangent la place, tout calme."),
            ("narrateur", "L'herbe sent encore la rosée."),
            ("papa", "Bravo, Amir."),
            ("papa", "Tu as joué avec Nino."),
            ("maman", "L'amitié ne dépend pas de la forme."),
            ("enfant-m", "On joue."),
            ("copain", "On joue."),
            ("narrateur", "La chaîne s'arrête, tout doucement."),
        ],
    }

    q = {
        "sable": [
            ("narrateur", "Nino a un corps plus rond."),
            ("papa", "On joue ensemble ?"),
        ],
        "toboggan": [
            ("narrateur", "Ils ont glissé, chacun son tour."),
            ("maman", "On joue ensemble ?"),
        ],
        "balancoires": [
            ("narrateur", "Amir a joué avec Nino."),
            ("papa", "On joue ensemble ?"),
        ],
    }

    conf = {
        "sable": [
            ("papa", "Oui."),
            ("papa", "On joue."),
            ("papa", "Le corps n'est pas une blague."),
            ("narrateur", "Amir souffle un peu."),
            ("narrateur", "Un grain de sable reste sur son genou."),
            ("enfant-m", "On joue."),
            ("maman", "Bravo, Amir."),
            ("maman", "Tu as fait du bon travail."),
            ("narrateur", "Le moule garde encore la forme du gâteau."),
        ],
        "toboggan": [
            ("maman", "Oui."),
            ("maman", "On joue."),
            ("maman", "Le corps n'est pas une blague."),
            ("narrateur", "Amir essuie ses mains sur son pull."),
            ("narrateur", "Le tissu est un peu rêche."),
            ("enfant-m", "Chacun son tour."),
            ("papa", "Bravo."),
            ("papa", "Vous avez attendu."),
            ("narrateur", "Le métal du toboggan reste froid, tout calme."),
        ],
        "balancoires": [
            ("papa", "Oui."),
            ("papa", "On joue ensemble."),
            ("papa", "Le corps n'est pas une blague."),
            ("narrateur", "Amir hoche la tête."),
            ("narrateur", "La chaîne ne crie plus."),
            ("enfant-m", "On joue."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "La feuille reste dans l'herbe, toute plate."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Amir prend les cubes en bois."),
            ("narrateur", "Un cube rouge sent le pin."),
            ("narrateur", "Un cube vert fait clic."),
            ("narrateur", "Nino pose un cube, tout droit."),
            ("papa", "Vous construisez ensemble ?"),
            ("enfant-m", "Oui."),
            ("copain", "Oui."),
            ("maman", "Le corps n'est pas une blague."),
            ("maman", "On joue."),
            ("papa", "Nino tient la base."),
            ("papa", "Amir pose le petit cube."),
            ("narrateur", "La tour tient."),
            ("enfant-m", "Elle est haute."),
            ("copain", "Encore un."),
            ("maman", "Bravo."),
            ("maman", "Vous jouez ensemble."),
        ],
        "livre": [
            ("narrateur", "Amir ouvre le livre."),
            ("narrateur", "La page sent le papier, un peu sec."),
            ("narrateur", "Une pomme est dessinée, toute rouge."),
            ("narrateur", "Nino montre la pomme du doigt."),
            ("papa", "On lit ensemble ?"),
            ("enfant-m", "Oui."),
            ("copain", "La pomme."),
            ("maman", "On joue."),
            ("maman", "Le corps n'est pas une blague."),
            ("papa", "L'amitié ne dépend pas de la forme."),
            ("narrateur", "Amir tourne la page, tout doux."),
            ("narrateur", "Une feuille collée sert de marque-page."),
            ("enfant-m", "Encore."),
            ("maman", "Bravo, Amir."),
            ("maman", "Tu as partagé le livre."),
        ],
        "dinette": [
            ("narrateur", "Amir sort la dînette."),
            ("narrateur", "Une petite assiette sonne, tout creux."),
            ("narrateur", "Une cuillère miniature est encore tiède."),
            ("narrateur", "Nino sert le sable, tout doux."),
            ("maman", "Tu sers Nino ?"),
            ("enfant-m", "Oui."),
            ("copain", "Merci."),
            ("papa", "On joue ensemble."),
            ("papa", "Le corps n'est pas une blague."),
            ("narrateur", "Ils posent deux tasses, côte à côte."),
            ("enfant-m", "C'est du goûter."),
            ("maman", "Bravo."),
            ("maman", "Vous avez partagé."),
            ("papa", "On ne commente pas le corps."),
            ("narrateur", "Une goutte perle au bord de l'assiette."),
        ],
    }

    extra_jouet = {
        ("sable", "cubes"): "Un cube attrape un grain de sable, tout fin.",
        ("sable", "livre"): "Le livre a une tache de sable, toute petite.",
        ("sable", "dinette"): "La petite casserole laisse un rond dans le sable.",
        ("toboggan", "cubes"): "Un cube tapote la première marche, tout doux.",
        ("toboggan", "livre"): "Le livre s'ouvre au pied du toboggan.",
        ("toboggan", "dinette"): "La petite tasse sonne contre le métal.",
        ("balancoires", "cubes"): "Un cube attend sous la balançoire, tout sage.",
        ("balancoires", "livre"): "Le livre est ouvert sur l'herbe, près de la chaîne.",
        ("balancoires", "dinette"): "La dînette a une place, sur les genoux.",
    }

    couleur_open = {
        "rouge": [
            ("narrateur", "Le rouge arrive, tout vif."),
            ("narrateur", "Une pomme rouge brille dans l'herbe."),
            ("narrateur", "Un seau rouge attend, tout près."),
            ("papa", "Tu vois le rouge, Amir ?"),
            ("enfant-m", "Oui, papa."),
        ],
        "bleu": [
            ("narrateur", "Le bleu s'installe, tout calme."),
            ("narrateur", "Le ciel est bleu, tout haut."),
            ("narrateur", "Une pelle bleue repose dans l'herbe."),
            ("maman", "Tu vois le bleu, Amir ?"),
            ("enfant-m", "Oui, maman."),
        ],
        "vert": [
            ("narrateur", "Le vert est partout, tout doux."),
            ("narrateur", "L'herbe est verte, encore un peu mouillée."),
            ("narrateur", "Une feuille verte colle à la chaussette."),
            ("papa", "Tu vois le vert, Amir ?"),
            ("enfant-m", "Oui, papa."),
        ],
    }

    extras = {
        ("sable", "cubes", "rouge"): "Un cube rouge a du sable sur une arête.",
        ("sable", "cubes", "bleu"): "Un cube bleu sèche au soleil, près du bac.",
        ("sable", "cubes", "vert"): "Un cube vert garde une tache d'herbe.",
        ("sable", "livre", "rouge"): "La pomme du livre est rouge, comme celle de l'herbe.",
        ("sable", "livre", "bleu"): "Une tache bleue du ciel passe sur la page.",
        ("sable", "livre", "vert"): "Une vraie feuille verte marque encore la page.",
        ("sable", "dinette", "rouge"): "La petite assiette a un rond de sable rouge.",
        ("sable", "dinette", "bleu"): "La petite tasse bleue tremble près du bac.",
        ("sable", "dinette", "vert"): "Un brin d'herbe verte reste dans la casserole.",
        ("toboggan", "cubes", "rouge"): "Un cube rouge tapote la rampe, tout petit.",
        ("toboggan", "cubes", "bleu"): "L'ombre bleue du toboggan couvre deux cubes.",
        ("toboggan", "cubes", "vert"): "Un cube vert attend en bas, dans l'herbe.",
        ("toboggan", "livre", "rouge"): "La page rouge se plie un peu, près du métal.",
        ("toboggan", "livre", "bleu"): "Le ciel bleu se reflète sur la page lisse.",
        ("toboggan", "livre", "vert"): "Une feuille verte sert de marque-page, encore.",
        ("toboggan", "dinette", "rouge"): "La petite tasse rouge sonne contre une marche.",
        ("toboggan", "dinette", "bleu"): "La casserole bleue refroidit au pied du toboggan.",
        ("toboggan", "dinette", "vert"): "Un brin vert reste collé à la cuillère.",
        ("balancoires", "cubes", "rouge"): "Un cube rouge se balance un peu, sur les genoux.",
        ("balancoires", "cubes", "bleu"): "Un cube bleu attend sous la chaîne froide.",
        ("balancoires", "cubes", "vert"): "L'herbe verte cache un cube, tout petit.",
        ("balancoires", "livre", "rouge"): "La pomme rouge du livre tremble, tout doux.",
        ("balancoires", "livre", "bleu"): "La page bleue claque un peu, dans l'air.",
        ("balancoires", "livre", "vert"): "Une feuille verte s'envole du livre, tout loin.",
        ("balancoires", "dinette", "rouge"): "La tasse rouge a une place, sur les genoux.",
        ("balancoires", "dinette", "bleu"): "La petite assiette bleue reflète le ciel.",
        ("balancoires", "dinette", "vert"): "Un brin vert reste au fond de l'assiette.",
    }

    fin_image = {
        "rouge": "La pomme rouge reste dans le panier, tout calme.",
        "bleu": "La pelle bleue sèche dans l'herbe, tout sage.",
        "vert": "La feuille verte ne bouge plus, sur le pull.",
    }

    def l3(lieu: str, jouet: str, couleur: str) -> list[tuple[str, str]]:
        return (
            couleur_open[couleur]
            + [
                ("narrateur", f"Amir a encore {jouet_np[jouet]}, près de {lieu_np[lieu]}."),
                ("narrateur", "Nino est encore là, tout près."),
            ]
            + sent(extras[(lieu, jouet, couleur)])
            + [
                ("papa", "On joue encore ?"),
                ("enfant-m", "Oui."),
                ("copain", "Oui."),
                ("maman", "Le corps n'est pas une blague."),
                ("maman", "On joue ensemble."),
                ("papa", "On ne commente pas le corps."),
                ("enfant-m", "Merci, Nino."),
                ("copain", "Merci, Amir."),
                ("maman", "Bravo."),
                ("maman", "C'est du bon travail."),
                ("narrateur", "Amir range " + jouet_np[jouet] + ", tout doux."),
                ("papa", "Tu as fini de ranger un peu ?"),
                ("enfant-m", "Oui, papa."),
            ]
        )

    def fin(lieu: str, jouet: str, couleur: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "On a joué."),
            ("copain", "On a joué."),
            ("papa", "Le corps n'est pas une blague."),
            ("maman", "Bravo, Amir."),
            ("maman", "Tu as fait du bon travail."),
            ("narrateur", f"Amir a vécu {couleur_np[couleur]}, près de {lieu_np[lieu]}."),
            ("narrateur", f"Il a joué avec {jouet_np[jouet]}, et avec Nino."),
            ("narrateur", fin_image[couleur]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l1() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois coins du jardin attendent."),
            ("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
            ("maman", "On joue ensemble."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout proches."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On joue."),
            ("papa", "Le corps n'est pas une blague."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Quelle couleur, maintenant ?"),
            ("papa", "Rouge, bleu, ou vert ?"),
            ("maman", "On joue encore ensemble."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le soleil perce les feuilles du pommier."),
        ("narrateur", "Des ronds de lumière dansent sur l'herbe."),
        ("narrateur", "Une pomme verte a une joue rouge."),
        ("narrateur", "Une autre est toute ronde, toute jaune."),
        ("narrateur", "Un pull bleu pend à la branche basse."),
        ("narrateur", "Il sent encore le savon."),
        ("narrateur", "Papa range deux pommes dans le panier."),
        ("narrateur", "Elles n'ont pas la même forme."),
        ("narrateur", "Maman essuie une feuille sur la nappe."),
        ("narrateur", "Ça sent l'herbe coupée."),
        ("papa", "Tu sens, Amir ?"),
        ("papa", "Ça sent la pomme."),
        ("enfant-m", "Elle est froide."),
        ("maman", "Le pull sèche, tout doux."),
        ("narrateur", "En ce moment, Amir pose sa main sur l'écorce."),
        ("narrateur", "L'écorce est rêche, un peu chaude."),
        ("narrateur", "Nino arrive près du panier."),
        ("narrateur", "Ses chaussettes sont jaunes."),
        ("narrateur", "Nino a un corps plus rond."),
        ("narrateur", "Amir a des bras plus minces."),
        ("papa", "On joue ensemble."),
        ("papa", "Le corps n'est pas une blague."),
        ("enfant-m", "On joue."),
        ("copain", "On joue."),
        ("maman", "L'amitié ne dépend pas de la forme."),
        ("maman", "On peut jouer."),
        ("narrateur", "Une coccinelle marche sur une feuille, tout lentement."),
        ("narrateur", "Le pull bleu bouge un peu, sur la branche."),
    ]
    sons["CHK_T0000_P0000"] = "oiseau,feuille"

    by["CHK_T0001_P0000"] = trans_l1()
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "sable": "sable",
            "toboggan": "",
            "balancoires": "",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                jouet_scene[jouet]
                + sent(extra_jouet[(lieu, jouet)])
                + [
                    ("narrateur", f"On est encore près de {lieu_np[lieu]}."),
                    ("papa", "On joue ensemble."),
                    ("maman", "Le corps n'est pas une blague."),
                ]
            )
            sons[cid_l2] = {"cubes": "cubes", "livre": "page", "dinette": "assiette"}[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, couleur in couleurs.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, couleur)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, couleur)
                sons[cid_l3] = {"rouge": "oiseau", "bleu": "", "vert": "feuille"}[couleur]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-DIF-002",
        {
            "fil_rouge": (
                "Sous le pommier, deux pommes n'ont pas la même forme. "
                "Amir et Nino jouent. Le corps n'est pas une blague."
            ),
            "title": "Le pull bleu et les deux pommes",
            "characters": "Amir, Nino, papa, maman",
            "setting": "jardin sous le pommier",
        },
        by,
        sons,
        max_words=15,
        extra_forbid=("Nina", "Mila", "Sarah", "Chouchou", "Victorino", "Victorina", "Raphaël", "Aniss"),
    )


def story_003() -> None:
    objets = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    coins = {"P0001": "tapis", "P0002": "canape", "P0003": "carton"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}
    objet_np = {"ballon": "le ballon rouge", "seau": "le seau bleu", "doudou": "le doudou"}
    coin_np = {"tapis": "le tapis", "canape": "le canapé", "carton": "le carton"}
    moment_np = {"matin": "le matin", "sieste": "après la sieste", "soir": "le soir"}

    objet_l1 = {
        "ballon": [
            ("narrateur", "Nina prend le ballon rouge."),
            ("narrateur", "Le ballon est un peu tiède, tout lisse."),
            ("narrateur", "Il fait poum contre le sol."),
            ("narrateur", "Mila a des lunettes rondes."),
            ("narrateur", "Elles brillent un peu."),
            ("enfant-f", "Tu veux le ballon ?"),
            ("copine", "Oui."),
            ("narrateur", "Nina passe le ballon, tout doux."),
            ("maman", "Les lunettes aident à voir."),
            ("maman", "On ne rit pas de l'apparence."),
            ("papa", "On joue ensemble."),
            ("enfant-f", "On joue."),
            ("copine", "On joue."),
            ("narrateur", "Le ballon va, puis revient."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as invité Mila."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Une perle de lumière glisse sur une lunette."),
        ],
        "seau": [
            ("narrateur", "Nina prend le seau bleu."),
            ("narrateur", "Un peu d'eau tremble au fond."),
            ("narrateur", "Le seau sonne, tout creux."),
            ("narrateur", "Mila a les cheveux très courts."),
            ("narrateur", "Ils sont doux, tout près des oreilles."),
            ("enfant-f", "On met des pinces ?"),
            ("copine", "Oui."),
            ("narrateur", "Elles mettent des pinces dans le seau."),
            ("maman", "Les cheveux sont les cheveux."),
            ("maman", "On ne rit pas de l'apparence."),
            ("papa", "On joue ensemble."),
            ("papa", "Maman apporte un peu d'eau."),
            ("enfant-f", "Merci, maman."),
            ("maman", "Bravo."),
            ("maman", "Vous jouez."),
            ("narrateur", "Une pince rouge flotte, tout légère."),
            ("copine", "Elle brille."),
            ("papa", "On joue."),
        ],
        "doudou": [
            ("narrateur", "Nina prend le doudou."),
            ("narrateur", "Le doudou est gris, un peu chaud."),
            ("narrateur", "Une oreille est froissée."),
            ("narrateur", "Mila porte un habit à pois, tout neuf."),
            ("narrateur", "Les pois sont blancs, sur le bleu."),
            ("enfant-f", "On assied le doudou ?"),
            ("copine", "Oui."),
            ("narrateur", "Elles asseyent le doudou contre un coussin."),
            ("papa", "L'habit tient chaud."),
            ("papa", "On ne rit pas de l'apparence."),
            ("maman", "On joue ensemble."),
            ("papa", "Je plie une manche, tout doux."),
            ("enfant-f", "Merci, papa."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as partagé le doudou."),
            ("narrateur", "Le doudou a une place, tout calme."),
            ("copine", "Il dort."),
            ("papa", "On joue."),
        ],
    }

    q = {
        "ballon": [
            ("narrateur", "Mila a des lunettes."),
            ("maman", "On joue ensemble ?"),
        ],
        "seau": [
            ("narrateur", "Mila a les cheveux courts."),
            ("papa", "On joue ensemble ?"),
        ],
        "doudou": [
            ("narrateur", "Mila a un habit à pois."),
            ("maman", "On joue ensemble ?"),
        ],
    }

    conf = {
        "ballon": [
            ("maman", "Oui."),
            ("maman", "On joue."),
            ("maman", "On ne rit pas de l'apparence."),
            ("narrateur", "Nina souffle un peu."),
            ("narrateur", "Le ballon reste chaud contre son ventre."),
            ("enfant-f", "On joue."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", "Les lunettes restent bien sur le nez."),
        ],
        "seau": [
            ("papa", "Oui."),
            ("papa", "On joue."),
            ("papa", "On ne rit pas de l'apparence."),
            ("narrateur", "Nina essuie une goutte sur le seau."),
            ("narrateur", "Le plastique est un peu froid."),
            ("enfant-f", "On joue."),
            ("maman", "Bravo."),
            ("maman", "Les cheveux sont les cheveux."),
            ("narrateur", "Une pince rouge reste au fond, tout sage."),
        ],
        "doudou": [
            ("maman", "Oui."),
            ("maman", "On joue."),
            ("maman", "On ne rit pas de l'apparence."),
            ("narrateur", "Nina hoche la tête."),
            ("narrateur", "Le doudou a encore l'oreille froissée."),
            ("enfant-f", "On joue."),
            ("papa", "Bravo."),
            ("papa", "L'habit tient chaud."),
            ("narrateur", "Un pois blanc attrape la lumière."),
        ],
    }

    coin_scene = {
        "tapis": [
            ("narrateur", "Nina s'assoit sur le tapis."),
            ("narrateur", "Le tapis est épais, un peu rêche."),
            ("narrateur", "Un fil rouge dépasse, tout petit."),
            ("narrateur", "Mila s'assoit en face, tout près."),
            ("enfant-f", "On joue ici ?"),
            ("copine", "Oui."),
            ("maman", "On joue ensemble."),
            ("maman", "On ne rit pas de l'apparence."),
            ("papa", "Les lunettes aident à voir."),
            ("papa", "Les cheveux sont les cheveux."),
            ("narrateur", "Elles posent le jeu au milieu du tapis."),
            ("enfant-f", "C'est doux."),
            ("maman", "Bravo."),
            ("maman", "Vous êtes bien, là."),
        ],
        "canape": [
            ("narrateur", "Nina grimpe sur le canapé."),
            ("narrateur", "Le tissu est chaud, un peu lourd."),
            ("narrateur", "Un coussin a une tache de lumière."),
            ("narrateur", "Mila s'assoit à côté, tout calme."),
            ("papa", "Vous avez de la place ?"),
            ("enfant-f", "Oui."),
            ("copine", "Oui."),
            ("maman", "On joue ensemble."),
            ("maman", "On ne rit pas de l'apparence."),
            ("papa", "L'habit tient chaud."),
            ("narrateur", "Elles posent le jeu entre les genoux."),
            ("enfant-f", "On est bien."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as fait une place à Mila."),
        ],
        "carton": [
            ("narrateur", "Nina ouvre le carton."),
            ("narrateur", "Le carton sent le papier, un peu sec."),
            ("narrateur", "Un rabat fait un bruit tout creux."),
            ("narrateur", "Mila tient l'autre rabat, tout doux."),
            ("enfant-f", "C'est une maison ?"),
            ("copine", "Oui."),
            ("papa", "On joue ensemble."),
            ("papa", "On ne rit pas de l'apparence."),
            ("maman", "Les lunettes restent bien en place."),
            ("maman", "L'habit à pois brille un peu."),
            ("narrateur", "Elles mettent le jeu dans le carton."),
            ("enfant-f", "On rentre."),
            ("papa", "Bravo."),
            ("papa", "Vous jouez."),
        ],
    }

    extra_coin = {
        ("ballon", "tapis"): "Le ballon fait un creux, au milieu du tapis.",
        ("ballon", "canape"): "Le ballon roule jusqu'au coussin, tout lentement.",
        ("ballon", "carton"): "Le ballon rentre dans le carton, trop juste.",
        ("seau", "tapis"): "Le seau laisse un rond mouillé, sur le tapis.",
        ("seau", "canape"): "Le seau attend au pied du canapé, tout sage.",
        ("seau", "carton"): "Le seau sonne contre le carton, tout creux.",
        ("doudou", "tapis"): "Le doudou s'allonge sur le tapis, l'oreille à plat.",
        ("doudou", "canape"): "Le doudou a une place, contre le coussin.",
        ("doudou", "carton"): "Le doudou s'assoit dans le carton, tout calme.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, le bol de cacao fume encore."),
            ("narrateur", "Un rai de soleil traverse le rideau."),
            ("narrateur", "Les chaussons sont encore un peu froids."),
            ("papa", "Bonjour, Nina."),
            ("enfant-f", "Bonjour, papa."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, un oreiller a un creux."),
            ("narrateur", "Le radiateur fait encore tic, tout petit."),
            ("narrateur", "Ça sent le linge chaud."),
            ("maman", "Tu es réveillée ?"),
            ("enfant-f", "Oui, maman."),
        ],
        "soir": [
            ("narrateur", "Le soir, la lampe fait un rond jaune."),
            ("narrateur", "Le pain craque, tout loin, dans la cuisine."),
            ("narrateur", "Un chausson attend sous la table."),
            ("papa", "Te voilà, Nina."),
            ("enfant-f", "Bonjour, papa."),
        ],
    }

    extras = {
        ("ballon", "tapis", "matin"): "Le ballon rouge attrape le soleil, sur le tapis.",
        ("ballon", "tapis", "sieste"): "Le ballon est tiède, comme les joues, sur le tapis.",
        ("ballon", "tapis", "soir"): "L'ombre du ballon danse sur le tapis, sous la lampe.",
        ("ballon", "canape", "matin"): "Le ballon rouge brille contre le coussin clair.",
        ("ballon", "canape", "sieste"): "Le ballon s'enfonce un peu, dans le canapé chaud.",
        ("ballon", "canape", "soir"): "La lampe allonge l'ombre du ballon, sur le canapé.",
        ("ballon", "carton", "matin"): "Un rabat du carton a un rond de soleil, tout jaune.",
        ("ballon", "carton", "sieste"): "Le ballon est calme, dans le carton un peu sombre.",
        ("ballon", "carton", "soir"): "La lampe éclaire l'intérieur du carton, tout doux.",
        ("seau", "tapis", "matin"): "Une goutte du seau brille, sur le fil rouge du tapis.",
        ("seau", "tapis", "sieste"): "Le seau bleu est tiède, posé sur le tapis calme.",
        ("seau", "tapis", "soir"): "Le seau bleu reflète la lampe, sur le tapis.",
        ("seau", "canape", "matin"): "Le seau attend au pied du canapé, dans le soleil.",
        ("seau", "canape", "sieste"): "Une pince tremble encore, près du canapé tiède.",
        ("seau", "canape", "soir"): "Le seau sonne un tout petit ding, sous la lampe.",
        ("seau", "carton", "matin"): "Le seau bleu a un reflet de matin, dans le carton.",
        ("seau", "carton", "sieste"): "Une goutte sèche au bord du carton, tout calme.",
        ("seau", "carton", "soir"): "Le carton sent encore l'eau, près de la lampe.",
        ("doudou", "tapis", "matin"): "L'oreille du doudou a un rond de soleil, sur le tapis.",
        ("doudou", "tapis", "sieste"): "Le doudou est chaud, comme la couverture, sur le tapis.",
        ("doudou", "tapis", "soir"): "Le doudou a une ombre longue, sur le tapis.",
        ("doudou", "canape", "matin"): "Le doudou s'adosse au coussin, dans la lumière.",
        ("doudou", "canape", "sieste"): "Le doudou garde le pli de la sieste, sur le canapé.",
        ("doudou", "canape", "soir"): "Le doudou reflète la lampe, contre le coussin.",
        ("doudou", "carton", "matin"): "Le doudou cligne, dans le carton clair du matin.",
        ("doudou", "carton", "sieste"): "Le doudou s'endort encore un peu, dans le carton.",
        ("doudou", "carton", "soir"): "Le carton devient une maison, sous la lampe.",
    }

    fin_image = {
        "matin": "Le bol de cacao ne fume plus, près du rideau.",
        "sieste": "L'oreiller garde encore son creux, tout calme.",
        "soir": "Le chausson sous la table n'attend plus.",
    }

    def l3(objet: str, coin: str, moment: str) -> list[tuple[str, str]]:
        return (
            moment_open[moment]
            + [
                ("narrateur", f"Nina a encore {objet_np[objet]}, près de {coin_np[coin]}."),
                ("narrateur", "Mila est encore là, tout près."),
            ]
            + sent(extras[(objet, coin, moment)])
            + [
                ("maman", "On joue encore ?"),
                ("enfant-f", "Oui."),
                ("copine", "Oui."),
                ("papa", "On ne rit pas de l'apparence."),
                ("papa", "On joue ensemble."),
                ("maman", "Les lunettes aident à voir."),
                ("maman", "Les cheveux sont les cheveux."),
                ("enfant-f", "Merci, Mila."),
                ("copine", "Merci, Nina."),
                ("papa", "Bravo."),
                ("papa", "C'est du bon travail."),
                ("narrateur", "Nina range " + objet_np[objet] + ", tout doux."),
                ("maman", "Tu as fini de ranger un peu ?"),
                ("enfant-f", "Oui, maman."),
            ]
        )

    def fin(objet: str, coin: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "On a joué."),
            ("copine", "On a joué."),
            ("maman", "On ne rit pas de l'apparence."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Nina a vécu {moment_np[moment]}, près de {coin_np[coin]}."),
            ("narrateur", f"Elle a joué avec {objet_np[objet]}, et avec Mila."),
            ("narrateur", fin_image[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l1() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout proches."),
            ("papa", "Le ballon rouge, le seau bleu, ou le doudou ?"),
            ("maman", "On joue ensemble."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois coins de la maison attendent."),
            ("maman", "Le tapis, le canapé, ou le carton ?"),
            ("papa", "On joue."),
            ("papa", "On ne rit pas de l'apparence."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Quel moment, maintenant ?"),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On joue encore ensemble."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Les chaussons de Nina font chut sur le carrelage."),
        ("narrateur", "Un manteau à pois brille au crochet."),
        ("narrateur", "Une goutte tombe du bas, sur le paillasson."),
        ("narrateur", "Elle fait ploc, tout petit."),
        ("narrateur", "Maman tourne la cuillère dans le bol."),
        ("narrateur", "Ça sent le pain grillé."),
        ("narrateur", "Papa plie un torchon, près de l'évier."),
        ("narrateur", "Le radiateur fait un tic doux."),
        ("maman", "Tu as entendu le ploc, Nina ?"),
        ("enfant-f", "Oui."),
        ("enfant-f", "C'est le manteau."),
        ("papa", "Il sèche, tout doux."),
        ("narrateur", "En ce moment, Nina est dans le salon."),
        ("narrateur", "Le tapis a un fil rouge qui dépasse."),
        ("narrateur", "Mila arrive avec son sac."),
        ("narrateur", "Mila a des lunettes rondes."),
        ("narrateur", "Elles brillent un peu."),
        ("narrateur", "Mila a les cheveux courts."),
        ("narrateur", "Son habit à pois est neuf."),
        ("maman", "On joue ensemble."),
        ("maman", "On ne rit pas de l'apparence."),
        ("enfant-f", "On joue."),
        ("copine", "On joue."),
        ("papa", "Les lunettes aident à voir."),
        ("papa", "Les cheveux sont les cheveux."),
        ("papa", "L'habit tient chaud."),
        ("narrateur", "Le crochet cliquette un peu, tout seul."),
        ("narrateur", "Le bol de maman fume encore, tout loin."),
    ]
    sons["CHK_T0000_P0000"] = "goutte,assiette"

    by["CHK_T0001_P0000"] = trans_l1()
    sons["CHK_T0001_P0000"] = ""

    for p1, objet in objets.items():
        by[f"CHK_T0001_{p1}"] = objet_l1[objet]
        by[f"CHK_T0001_{p1}_Q0001"] = q[objet]
        by[f"CHK_T0001_{p1}_C0001"] = conf[objet]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "ballon": "ballon",
            "seau": "eau",
            "doudou": "",
        }[objet]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, coin in coins.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                coin_scene[coin]
                + sent(extra_coin[(objet, coin)])
                + [
                    ("narrateur", f"On a encore {objet_np[objet]}."),
                    ("maman", "On joue ensemble."),
                    ("papa", "On ne rit pas de l'apparence."),
                ]
            )
            sons[cid_l2] = {"tapis": "", "canape": "", "carton": "carton"}[coin]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, moment in moments.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(objet, coin, moment)
                by[f"{cid_l3}_F0001"] = fin(objet, coin, moment)
                sons[cid_l3] = {"matin": "oiseau", "sieste": "", "soir": "pain"}[moment]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-DIF-003",
        {
            "fil_rouge": (
                "Une goutte tombe du manteau à pois. Nina invite Mila. "
                "On joue. On ne rit pas de l'apparence."
            ),
            "title": "Le manteau à pois et les lunettes de Mila",
            "characters": "Nina, Mila, papa, maman",
            "setting": "à la maison",
        },
        by,
        sons,
        max_words=15,
        extra_forbid=("Amir", "Nino", "Aniss", "Sarah", "Chouchou", "Victorino", "Victorina", "Raphaël"),
    )


if __name__ == "__main__":
    story_002()
    story_003()
    print("ok TREE-DIF-002 TREE-DIF-003")
