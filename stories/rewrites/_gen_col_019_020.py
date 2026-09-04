#!/usr/bin/env python3
"""merged.json pour TREE-COL-019 et TREE-COL-020 (texte seulement)."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    script = "\n".join(f"{role}|{phrase}" for role, phrase in lines)
    text = " ".join(phrase for _, phrase in lines)
    return text, script


def apply_chunk(src: dict, lines: list[tuple[str, str]], sons: str | None = None) -> dict:
    text, script = pack(lines)
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    out["sons"] = "" if sons is None else sons
    return out


def nwords(s: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9']+", s))


def check_lines(story_id: str, cid: str, lines: list[tuple[str, str]], max_w: int) -> None:
    for role, phrase in lines:
        if "|" in phrase:
            raise SystemExit(f"{story_id} {cid}: pipe in phrase: {phrase!r}")
        if "\n" in phrase:
            raise SystemExit(f"{story_id} {cid}: newline in phrase")
        w = nwords(phrase)
        if w > max_w:
            raise SystemExit(f"{story_id} {cid}: {w} mots ({max_w}): {phrase!r}")
        if not phrase.endswith((".", "?", "!")):
            raise SystemExit(f"{story_id} {cid}: pas de point: {phrase!r}")


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str],
    max_w: int,
) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    src_ids = [c["chunk_id"] for c in source["chunks"]]
    missing = [cid for cid in src_ids if cid not in by_id]
    extra = [k for k in by_id if k not in set(src_ids)]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:8]} extra={extra[:8]}")
    chunks = []
    for c in source["chunks"]:
        cid = c["chunk_id"]
        check_lines(story_id, cid, by_id[cid], max_w)
        chunks.append(apply_chunk(c, by_id[cid], sons_map.get(cid, "")))
    merged = dict(source)
    merged.update(meta)
    merged["chunks"] = chunks
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def story_019() -> None:
    places = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    toys = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    times = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}

    l1 = {
        "cuisine": [
            ("narrateur", "Victorino pousse la porte de la cuisine."),
            ("narrateur", "Le carrelage est froid sous les chaussons."),
            ("narrateur", "La vitre est encore embuée, tout bas."),
            ("narrateur", "Ça sent le beurre et le pain grillé."),
            ("narrateur", "Une miette reste près du bol jaune."),
            ("papa", "Bonjour, la cuisine."),
            ("enfant-m", "Bonjour, papa."),
            ("maman", "Tu veux le bol jaune ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le bol est lisse, un peu tiède."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo, Victorino."),
            ("papa", "Tu as dit les trois mots."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "Une goutte glisse encore, sur la vitre."),
            ("papa", "Les mots gentils, ici aussi."),
        ],
        "jardin": [
            ("narrateur", "Victorino ouvre la porte du jardin."),
            ("narrateur", "L'air est frais, un peu humide."),
            ("narrateur", "L'herbe brille, toute courte."),
            ("narrateur", "Un arrosoir penche près du bac."),
            ("narrateur", "Une petite feuille colle à la semelle."),
            ("maman", "Bonjour, jardin."),
            ("enfant-m", "Bonjour, maman."),
            ("papa", "Tu veux l'arrosoir ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "L'arrosoir est froid, un peu lourd."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Tu as demandé, tout doux."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Un oiseau picore près de la haie."),
            ("maman", "On reste près de la porte."),
        ],
        "chambre": [
            ("narrateur", "Victorino entre dans la chambre."),
            ("narrateur", "Le tapis est doux, tout épais."),
            ("narrateur", "L'oreiller a encore le creux de la nuit."),
            ("narrateur", "Un doudou gris attend au bord du lit."),
            ("narrateur", "Un rayon glisse sur le parquet."),
            ("papa", "Bonjour, la chambre."),
            ("enfant-m", "Bonjour, doudou."),
            ("maman", "Tu veux le doudou ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le doudou est tiède, un peu râpé."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo, Victorino."),
            ("papa", "Les trois mots, ici aussi."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "Le rideau jaune bouge, tout peu."),
            ("papa", "On parle doucement, dans la chambre."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Victorino veut le bol."),
            ("maman", "Que dit-il ?"),
        ],
        "jardin": [
            ("narrateur", "Victorino veut l'arrosoir."),
            ("papa", "On dit s'il te plaît ?"),
        ],
        "chambre": [
            ("narrateur", "On dit les trois mots."),
            ("maman", "Bonjour, s'il te plaît, merci ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("papa", "Oui."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Victorino souffle un peu."),
            ("narrateur", "Le bol jaune reste près de la miette."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Tu as fait du bon travail."),
            ("narrateur", "La vitre a encore un trait clair."),
        ],
        "jardin": [
            ("maman", "Oui."),
            ("maman", "On dit s'il te plaît."),
            ("maman", "Puis on dit merci."),
            ("narrateur", "Victorino tient l'arrosoir des deux mains."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo, Victorino."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "L'herbe brille encore, toute courte."),
            ("maman", "Les mots gentils, au jardin aussi."),
        ],
        "chambre": [
            ("papa", "Oui."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Victorino serre le doudou gris."),
            ("enfant-m", "J'ai dit les mots."),
            ("maman", "Bravo."),
            ("maman", "On continue, tout doux."),
            ("narrateur", "Le tapis chatouille encore les orteils."),
        ],
    }

    toy_scene = {
        "cubes": [
            ("narrateur", "Victorino prend les cubes de bois."),
            ("narrateur", "Ils sentent le sapin, tout léger."),
            ("narrateur", "Un cube rouge, un cube bleu."),
            ("papa", "Tu veux le cube rouge ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le cube est lisse, un peu froid."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bonjour, les cubes."),
            ("enfant-m", "Bonjour."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les mots."),
            ("narrateur", "Victorino pose le cube, tout droit."),
        ],
        "livre": [
            ("narrateur", "Victorino ouvre le livre."),
            ("narrateur", "Les pages sont épaisses, un peu rèches."),
            ("narrateur", "Un bateau jaune est dessiné."),
            ("maman", "Tu veux la page du bateau ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Maman tourne la page, tout doux."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bonjour, le bateau."),
            ("enfant-m", "Bonjour."),
            ("maman", "Bravo, Victorino."),
            ("maman", "Tu as demandé."),
            ("narrateur", "Le papier sent un peu le bois."),
        ],
        "dinette": [
            ("narrateur", "Victorino prend la dînette."),
            ("narrateur", "La petite tasse sonne, tout creux."),
            ("narrateur", "Une cuillère miniature brille."),
            ("papa", "Tu veux la tasse ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "La tasse est froide, toute ronde."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bonjour, la dînette."),
            ("enfant-m", "Bonjour."),
            ("papa", "Bravo."),
            ("papa", "Les trois mots, encore."),
            ("narrateur", "Victorino fait mine de verser, tout lent."),
        ],
    }

    extra_toy = {
        ("cuisine", "cubes"): "Une miette reste collée au cube bleu.",
        ("cuisine", "livre"): "Le livre est ouvert près du bol jaune.",
        ("cuisine", "dinette"): "La petite tasse sent encore le pain.",
        ("jardin", "cubes"): "Un brin d'herbe colle au cube vert.",
        ("jardin", "livre"): "Une petite feuille sert de marque-page.",
        ("jardin", "dinette"): "La cuillère miniature a un peu de rosée.",
        ("chambre", "cubes"): "Un cube tapote l'oreiller, tout léger.",
        ("chambre", "livre"): "Le livre est posé sur le doudou gris.",
        ("chambre", "dinette"): "La petite assiette est sur le tapis épais.",
    }

    time_open = {
        "matin": [
            ("narrateur", "C'est le matin."),
            ("narrateur", "La lumière est claire, un peu pâle."),
            ("narrateur", "Un oiseau tape encore le rebord."),
        ],
        "sieste": [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "Les joues de Victorino sont tièdes."),
            ("narrateur", "La maison est calme, tout douce."),
        ],
        "soir": [
            ("narrateur", "C'est le soir."),
            ("narrateur", "La lampe fait un rond jaune."),
            ("narrateur", "Ça sent la soupe, tout près."),
        ],
    }

    extras = {
        ("cuisine", "cubes", "matin"): "Le soleil touche le cube rouge, près de la miette.",
        ("cuisine", "cubes", "sieste"): "Le cube bleu a chaud, après la sieste.",
        ("cuisine", "cubes", "soir"): "La lampe fait un carré sur les cubes.",
        ("cuisine", "livre", "matin"): "Une page sent encore le pain grillé.",
        ("cuisine", "livre", "sieste"): "Le livre reste ouvert près du bol.",
        ("cuisine", "livre", "soir"): "Le bateau jaune brille sous la lampe.",
        ("cuisine", "dinette", "matin"): "La petite tasse a une goutte de lait.",
        ("cuisine", "dinette", "sieste"): "La casserole miniature est encore tiède.",
        ("cuisine", "dinette", "soir"): "Un grain de sel reste dans l'assiette.",
        ("jardin", "cubes", "matin"): "Une goutte d'herbe mouille le cube vert.",
        ("jardin", "cubes", "sieste"): "Les cubes chauffent sur la pierre.",
        ("jardin", "cubes", "soir"): "Un cube garde encore la chaleur du jour.",
        ("jardin", "livre", "matin"): "Une fourmi passe au bord de la page.",
        ("jardin", "livre", "sieste"): "Le livre a une ombre ronde, sous l'arbre.",
        ("jardin", "livre", "soir"): "Une page claque, tout doux, dans le vent.",
        ("jardin", "dinette", "matin"): "La petite cuillère a un peu de rosée.",
        ("jardin", "dinette", "sieste"): "La dînette sent l'herbe coupée.",
        ("jardin", "dinette", "soir"): "Un bol miniature reflète la fenêtre allumée.",
        ("chambre", "cubes", "matin"): "Un cube rouge reste près de l'oreiller.",
        ("chambre", "cubes", "sieste"): "Les cubes dorment au pied du lit.",
        ("chambre", "cubes", "soir"): "Un cube veille près de la veilleuse.",
        ("chambre", "livre", "matin"): "Le livre est ouvert sur le doudou gris.",
        ("chambre", "livre", "sieste"): "Une page a le creux de la sieste.",
        ("chambre", "livre", "soir"): "Maman lit tout bas, près de la veilleuse.",
        ("chambre", "dinette", "matin"): "La petite assiette attend sur le tapis.",
        ("chambre", "dinette", "sieste"): "La tasse miniature a glissé sous l'oreiller.",
        ("chambre", "dinette", "soir"): "La dînette range, près des chaussons.",
    }

    fin_image = {
        "matin": "L'oiseau a quitté le rebord, tout calme.",
        "sieste": "Les joues de Victorino restent tièdes.",
        "soir": "La lampe reste allumée, un moment.",
    }

    place_np = {"cuisine": "la cuisine", "jardin": "le jardin", "chambre": "la chambre"}
    toy_np = {"cubes": "les cubes", "livre": "le livre", "dinette": "la dînette"}
    time_np = {"matin": "le matin", "sieste": "après la sieste", "soir": "le soir"}

    place_sit = {
        "cuisine": "Victorino est encore dans la cuisine.",
        "jardin": "Victorino est encore dans l'herbe.",
        "chambre": "Victorino est encore sur le tapis de la chambre.",
    }

    def l3(place: str, toy: str, time: str) -> list[tuple[str, str]]:
        extra = extras[(place, toy, time)]
        extra_line = extra if extra.endswith((".", "?", "!")) else extra + "."
        return [
            time_open[time][0],
            ("narrateur", extra_line),
        ] + time_open[time][1:] + [
            ("narrateur", place_sit[place]),
            ("narrateur", f"Il a encore {toy_np[toy]} tout près."),
            ("enfant-m", "Bonjour."),
            ("papa", "Bonjour, Victorino."),
            ("maman", "Tu veux encore un peu ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Papa tend la main, tout doux."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit les trois mots."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("enfant-m", "Merci, maman."),
            ("narrateur", "La vitre a encore un petit trait clair."),
        ]

    def fin(place: str, toy: str, time: str) -> list[tuple[str, str]]:
        return [
            ("narrateur", f"Victorino a vécu {time_np[time]}, dans {place_np[place]}."),
            ("narrateur", f"Il a joué avec {toy_np[toy]}."),
            ("narrateur", fin_image[time]),
            ("maman", "Tu as dit bonjour."),
            ("papa", "Tu as dit s'il te plaît."),
            ("enfant-m", "Et merci."),
            ("maman", "Bravo, Victorino."),
            ("maman", "Tu as fait du bon travail."),
            ("papa", "Bonne journée, mon grand."),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout près."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On dit les mots gentils."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Le jour a trois moments, dans la maison."),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On reste ensemble."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "La vitre de la cuisine est toute embuée."),
        ("narrateur", "Une goutte descend, toute lente."),
        ("narrateur", "Elle laisse un trait clair, comme un chemin."),
        ("narrateur", "Le rideau jaune a des petits bateaux."),
        ("narrateur", "Il bouge, tout doux, près du radiateur."),
        ("narrateur", "Ça sent le pain grillé."),
        ("narrateur", "Une miette reste sur la table ronde."),
        ("narrateur", "Dehors, un oiseau tape le rebord, une fois."),
        ("narrateur", "Les chaussons de Victorino attendent sous la chaise."),
        ("papa", "Tu as vu la goutte, Victorino ?"),
        ("enfant-m", "Elle glisse."),
        ("maman", "Elle fait un chemin, sur la vitre."),
        ("papa", "Le pain est encore chaud."),
        ("maman", "Tu veux un bout ?"),
        ("enfant-m", "S'il te plaît."),
        ("narrateur", "Maman tend un coin de pain."),
        ("narrateur", "Il est tiède, un peu croustillant."),
        ("enfant-m", "Merci, maman."),
        ("papa", "Bravo."),
        ("papa", "Tu as dit s'il te plaît."),
        ("papa", "Tu as dit merci."),
        ("narrateur", "En ce moment, Victorino pose un doigt sur la vitre."),
        ("narrateur", "La vitre est froide, un peu mouillée."),
        ("enfant-m", "Bonjour, oiseau."),
        ("maman", "Bonjour, c'est un mot gentil."),
        ("papa", "Bonjour."),
        ("papa", "S'il te plaît."),
        ("papa", "Merci."),
        ("narrateur", "L'oiseau picore, puis s'en va."),
        ("maman", "On peut jouer, dans la maison."),
        ("enfant-m", "Oui, maman."),
        ("narrateur", "Le radiateur fait un petit tic, tout bas."),
    ]
    sons["CHK_T0000_P0000"] = "goutte,oiseau"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "La maison a trois coins, tout proches."),
        ("maman", "La cuisine, le jardin, ou la chambre ?"),
        ("papa", "On dit bonjour."),
        ("papa", "S'il te plaît."),
        ("papa", "Merci."),
    ]
    sons["CHK_T0001_P0000"] = ""

    toy_sons = {"cubes": "", "livre": "", "dinette": "assiette"}
    place_sons = {"cuisine": "casserole", "jardin": "oiseau", "chambre": ""}
    time_sons = {"matin": "oiseau", "sieste": "", "soir": ""}

    for p1, place in places.items():
        by[f"CHK_T0001_{p1}"] = l1[place]
        by[f"CHK_T0001_{p1}_Q0001"] = q[place]
        by[f"CHK_T0001_{p1}_C0001"] = conf[place]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = place_sons[place]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, toy in toys.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_toy[(place, toy)]
            extra_line = extra if extra.endswith((".", "?", "!")) else extra + "."
            by[cid_l2] = toy_scene[toy] + [
                ("narrateur", extra_line),
                ("narrateur", f"Victorino est encore dans {place_np[place]}."),
                ("maman", "Bonjour."),
                ("maman", "S'il te plaît."),
                ("maman", "Merci."),
            ]
            sons[cid_l2] = toy_sons[toy]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, time in times.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(place, toy, time)
                by[f"{cid_l3}_F0001"] = fin(place, toy, time)
                sons[cid_l3] = time_sons[time]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-019",
        {
            "fil_rouge": (
                "La vitre est embuée. Victorino suit une goutte. "
                "Il dit bonjour, s'il te plaît, merci, dans la maison."
            ),
            "title": "La vitre embuée de Victorino",
            "characters": "Victorino, papa, maman",
            "setting": "près de la fenêtre, puis la maison",
        },
        by,
        sons,
        max_w=15,
    )


def story_020() -> None:
    parks = {"P0001": "sable", "P0002": "toboggan", "P0003": "balancoire"}
    toys = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    pels = {"P0001": "Tom", "P0002": "Léa", "P0003": "Sami"}

    park_np = {
        "sable": "le bac à sable",
        "toboggan": "le toboggan",
        "balancoire": "les balançoires",
    }
    toy_np = {"ballon": "le ballon", "seau": "le seau", "doudou": "le doudou"}
    pel_np = {
        "Tom": "l'ours Tom",
        "Léa": "la poupée Léa",
        "Sami": "le lion Sami",
    }

    l1 = {
        "sable": [
            ("narrateur", "Nina va vers le bac à sable."),
            ("narrateur", "Le sable est frais, un peu gris."),
            ("narrateur", "Un grain colle à son doigt."),
            ("narrateur", "Une petite pelle attend, toute rouge."),
            ("maman", "Tu as tes mains, Nina ?"),
            ("enfant-f", "Elles sont froides."),
            ("papa", "Ce matin, tu as écouté la maîtresse."),
            ("enfant-f", "Oui."),
            ("enfant-f", "Puis j'ai raconté, au salon."),
            ("maman", "Bravo."),
            ("maman", "Si malaise, tu racontes à la maison."),
            ("narrateur", "Nina creuse un petit trou."),
            ("narrateur", "Le sable fait un bruit sec."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Un grain brille, tout plat."),
        ],
        "toboggan": [
            ("narrateur", "Nina va vers le toboggan."),
            ("narrateur", "Le métal est un peu froid."),
            ("narrateur", "Les marches sont lisses, toutes étroites."),
            ("narrateur", "Une feuille colle en haut, toute plate."),
            ("papa", "Tu montes, Nina ?"),
            ("enfant-f", "Oui, papa."),
            ("maman", "Tu as écouté, à l'école."),
            ("enfant-f", "La maîtresse a parlé."),
            ("enfant-f", "Un camarade a chuchoté."),
            ("papa", "Tu as raconté, au salon."),
            ("enfant-f", "Mon ventre est plus calme."),
            ("maman", "On écoute la maîtresse."),
            ("maman", "Si malaise, on raconte à la maison."),
            ("narrateur", "Nina glisse, tout doux."),
            ("narrateur", "Le vent lui chatouille les joues."),
        ],
        "balancoire": [
            ("narrateur", "Nina va vers les balançoires."),
            ("narrateur", "La chaîne fait tic, tout léger."),
            ("narrateur", "Le siège est un peu humide."),
            ("narrateur", "Ça sent l'herbe coupée, tout près."),
            ("maman", "Tu t'assoies, Nina ?"),
            ("enfant-f", "Oui, maman."),
            ("papa", "On t'a écoutée, au salon."),
            ("enfant-f", "J'ai eu un malaise."),
            ("enfant-f", "Puis j'ai raconté."),
            ("maman", "Tu as bien fait."),
            ("maman", "Papa et maman t'écoutent."),
            ("narrateur", "Nina se balance, tout peu."),
            ("narrateur", "Ses chaussures font un petit aller-retour."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as écouté, puis raconté."),
        ],
    }

    q = {
        "sable": [
            ("narrateur", "Nina a eu un malaise."),
            ("maman", "Que fait-elle, à la maison ?"),
        ],
        "toboggan": [
            ("narrateur", "On écoute la maîtresse."),
            ("papa", "Et si malaise, on raconte ?"),
        ],
        "balancoire": [
            ("narrateur", "Nina a écouté, puis raconté."),
            ("maman", "On raconte à papa ou maman ?"),
        ],
    }

    conf = {
        "sable": [
            ("maman", "Oui."),
            ("maman", "On écoute la maîtresse."),
            ("maman", "Si malaise, on raconte à la maison."),
            ("narrateur", "Nina essuie un grain de sable."),
            ("enfant-f", "Je raconte à papa, ou à maman."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Le ventre se desserre, tout doucement."),
            ("maman", "On t'écoute."),
        ],
        "toboggan": [
            ("papa", "Oui."),
            ("papa", "On écoute."),
            ("papa", "Si malaise, raconter à la maison."),
            ("narrateur", "Nina pose les pieds dans l'herbe."),
            ("enfant-f", "J'ai raconté, au salon."),
            ("maman", "Bravo."),
            ("maman", "Tu as fait du bon travail."),
            ("narrateur", "La feuille reste en haut, toute plate."),
            ("papa", "On continue, tout calme."),
        ],
        "balancoire": [
            ("maman", "Oui."),
            ("maman", "On raconte à papa ou maman."),
            ("narrateur", "La chaîne fait encore tic, tout bas."),
            ("enfant-f", "Je raconte."),
            ("papa", "On t'écoute."),
            ("papa", "Bravo, Nina."),
            ("maman", "Tu as écouté la maîtresse."),
            ("maman", "Ensuite tu as parlé, à la maison."),
            ("narrateur", "Nina pose une main sur la chaîne froide."),
        ],
    }

    toy_scene = {
        "ballon": [
            ("narrateur", "Nina prend le ballon."),
            ("narrateur", "Il est un peu sablé, tout rond."),
            ("narrateur", "Il fait poum contre l'herbe."),
            ("papa", "Tu te souviens de la classe ?"),
            ("enfant-f", "J'ai écouté la maîtresse."),
            ("enfant-f", "Un camarade a parlé tout bas."),
            ("maman", "Tu as raconté, au salon."),
            ("maman", "C'est bien."),
            ("narrateur", "Nina tient le ballon contre son ventre."),
            ("papa", "Si malaise, tu reviens nous le dire."),
            ("enfant-f", "Oui, papa."),
            ("maman", "Bravo."),
        ],
        "seau": [
            ("narrateur", "Nina prend le seau."),
            ("narrateur", "Un peu de sable tremble au fond."),
            ("narrateur", "Le seau sonne, tout creux."),
            ("maman", "Tu as écouté, ce matin."),
            ("enfant-f", "Oui."),
            ("enfant-f", "Puis j'ai raconté mon malaise."),
            ("papa", "On écoute la maîtresse."),
            ("papa", "Ensuite, si malaise, on raconte."),
            ("narrateur", "Nina pose le seau près de ses genoux."),
            ("maman", "Bravo, Nina."),
            ("maman", "On t'écoute, à la maison."),
            ("narrateur", "Un grain glisse le long du seau."),
        ],
        "doudou": [
            ("narrateur", "Nina prend le doudou."),
            ("narrateur", "Une oreille est encore chaude."),
            ("narrateur", "Le tissu est râpé, tout doux."),
            ("papa", "Le doudou t'écoute, lui aussi."),
            ("enfant-f", "Doudou, j'ai eu un malaise."),
            ("enfant-f", "J'ai raconté à maman."),
            ("maman", "Tu as bien fait."),
            ("maman", "Papa t'écoute aussi."),
            ("narrateur", "Nina serre le doudou, tout près."),
            ("papa", "On écoute la maîtresse."),
            ("papa", "Si malaise, raconter à la maison."),
            ("maman", "C'est du bon travail."),
        ],
    }

    extra_toy = {
        ("sable", "ballon"): "Le ballon a une tache de sable, toute plate.",
        ("sable", "seau"): "Le seau est à moitié plein, tout gris.",
        ("sable", "doudou"): "Un grain de sable colle à l'oreille du doudou.",
        ("toboggan", "ballon"): "Le ballon attend en bas, tout rond.",
        ("toboggan", "seau"): "Le seau est posé près de la dernière marche.",
        ("toboggan", "doudou"): "Le doudou glisse un peu, sur les genoux.",
        ("balancoire", "ballon"): "Le ballon reste coincé sous le siège.",
        ("balancoire", "seau"): "Le seau penche, près de la chaîne.",
        ("balancoire", "doudou"): "Le doudou se balance, tout peu.",
    }

    peluche = {
        "Tom": [
            ("narrateur", "Nina rejoint l'ours Tom."),
            ("narrateur", "L'ours est brun, un peu râpé."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("enfant-f", "Tom, j'ai écouté la maîtresse."),
            ("enfant-f", "J'ai eu un malaise."),
            ("maman", "Tu l'as dit, à la maison."),
            ("maman", "Papa et maman t'écoutent."),
            ("narrateur", "Nina caresse l'oreille de l'ours."),
        ],
        "Léa": [
            ("narrateur", "Nina rejoint la poupée Léa."),
            ("narrateur", "La robe est bleue, un peu froissée."),
            ("narrateur", "Un bouton brille, tout petit."),
            ("enfant-f", "Léa, j'ai écouté."),
            ("enfant-f", "Mon ventre était serré."),
            ("papa", "Ce n'est pas un secret pour nous."),
            ("papa", "Tu racontes à la maison."),
            ("narrateur", "Nina lisse la robe bleue."),
        ],
        "Sami": [
            ("narrateur", "Nina rejoint le lion Sami."),
            ("narrateur", "La crinière est en laine, un peu mêlée."),
            ("narrateur", "Un œil de bouton regarde, tout calme."),
            ("enfant-f", "Sami, j'ai raconté."),
            ("enfant-f", "Un camarade a chuchoté."),
            ("maman", "Tu as écouté la maîtresse."),
            ("maman", "Ensuite tu as parlé, au salon."),
            ("narrateur", "Nina range une mèche de laine."),
        ],
    }

    extras = {
        ("sable", "ballon", "Tom"): "L'ours a du sable sur le ventre, près du ballon.",
        ("sable", "ballon", "Léa"): "La poupée tient le ballon, tout droit.",
        ("sable", "ballon", "Sami"): "Le lion a un grain dans la crinière.",
        ("sable", "seau", "Tom"): "L'ours regarde le seau, tout calme.",
        ("sable", "seau", "Léa"): "La poupée a du sable dans la robe.",
        ("sable", "seau", "Sami"): "Le lion a une patte dans le seau.",
        ("sable", "doudou", "Tom"): "L'ours et le doudou se touchent, tout doux.",
        ("sable", "doudou", "Léa"): "La poupée caresse le doudou, tout sableux.",
        ("sable", "doudou", "Sami"): "Le lion pose la tête sur le doudou.",
        ("toboggan", "ballon", "Tom"): "L'ours attend en bas, le ballon contre lui.",
        ("toboggan", "ballon", "Léa"): "La poupée a le ballon sur les genoux.",
        ("toboggan", "ballon", "Sami"): "Le lion suit le ballon des yeux.",
        ("toboggan", "seau", "Tom"): "L'ours est assis dans le seau, trop grand.",
        ("toboggan", "seau", "Léa"): "La poupée a le seau comme un chapeau.",
        ("toboggan", "seau", "Sami"): "Le lion écoute le son creux du seau.",
        ("toboggan", "doudou", "Tom"): "L'ours tient le doudou, en bas du toboggan.",
        ("toboggan", "doudou", "Léa"): "La poupée a le doudou autour du cou.",
        ("toboggan", "doudou", "Sami"): "Le lion réchauffe le doudou, tout brun.",
        ("balancoire", "ballon", "Tom"): "L'ours a le ballon coincé sous le bras.",
        ("balancoire", "ballon", "Léa"): "La poupée regarde le ballon, tout rond.",
        ("balancoire", "ballon", "Sami"): "Le lion souffle, tout doux, près du ballon.",
        ("balancoire", "seau", "Tom"): "L'ours a le seau entre les pieds.",
        ("balancoire", "seau", "Léa"): "La poupée tape le seau, tout léger.",
        ("balancoire", "seau", "Sami"): "Le seau sonne. Le lion dresse l'oreille.",
        ("balancoire", "doudou", "Tom"): "L'ours berce le doudou, tout lentement.",
        ("balancoire", "doudou", "Léa"): "La poupée et le doudou se balancent un peu.",
        ("balancoire", "doudou", "Sami"): "Le lion retient le doudou, tout sage.",
    }

    fin_image = {
        "Tom": "L'ours Tom s'endort contre le cartable.",
        "Léa": "La poupée Léa reste sur le coussin tiède.",
        "Sami": "Le lion Sami garde la crinière un peu mêlée.",
    }

    def split_extra(extra: str) -> list[tuple[str, str]]:
        parts = [p.strip() for p in extra.split(". ") if p.strip()]
        out = []
        for p in parts:
            if not p.endswith((".", "?", "!")):
                p = p + "."
            out.append(("narrateur", p))
        return out

    park_sit = {
        "sable": "Près du bac à sable, Nina s'assoit.",
        "toboggan": "Au pied du toboggan, Nina s'assoit.",
        "balancoire": "Sous les balançoires, Nina s'assoit.",
    }

    def l3(park: str, toy: str, pel: str) -> list[tuple[str, str]]:
        return (
            [
                ("narrateur", park_sit[park]),
                ("narrateur", f"{toy_np[toy].capitalize()} est encore là."),
            ]
            + peluche[pel]
            + split_extra(extras[(park, toy, pel)])
            + [
                ("narrateur", f"Nina reste près de {park_np[park]}."),
                ("enfant-f", "Papa."),
                ("enfant-f", "Maman."),
                ("enfant-f", "J'ai écouté."),
                ("enfant-f", "Puis j'ai raconté."),
                ("papa", "Tu as bien fait de raconter."),
                ("maman", "On écoute la maîtresse."),
                ("maman", "Si malaise, on raconte à la maison."),
                ("papa", "Bravo, Nina."),
                ("papa", "C'est du bon travail."),
                ("enfant-f", "Merci, maman."),
                ("enfant-f", "Merci, papa."),
                ("narrateur", "Le ventre de Nina se desserre, tout doucement."),
            ]
        )

    def fin(park: str, toy: str, pel: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "J'ai écouté."),
            ("enfant-f", "Puis j'ai raconté."),
            ("maman", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Nina a joué à {park_np[park]}."),
            ("narrateur", f"Elle a tenu {toy_np[toy]}."),
            ("narrateur", f"Elle a parlé à {pel_np[pel]}."),
            ("narrateur", "Plus tard, le salon est calme."),
            ("narrateur", fin_image[pel]),
            ("maman", "On t'écoute, à la maison."),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jouets attendent, dans l'herbe."),
            ("maman", "Le ballon, le seau, ou le doudou ?"),
            ("papa", "On joue."),
            ("papa", "Ensuite on raconte, si besoin."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois peluches attendent, tout sages."),
            ("maman", "Tom, Léa, ou Sami ?"),
            ("papa", "On peut leur parler."),
            ("papa", "Puis on rentre."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le coussin du canapé est encore tiède."),
        ("narrateur", "Une chaussette pend au bras du fauteuil."),
        ("narrateur", "La lampe fait un rond jaune sur le tapis."),
        ("narrateur", "Le cartable de Nina est contre la table basse."),
        ("narrateur", "Il sent le crayon et le papier."),
        ("narrateur", "Dehors, la pluie tape le volet, tout petit."),
        ("narrateur", "Ça sent le cacao, dans la cuisine d'à côté."),
        ("maman", "Tes chaussettes, Nina."),
        ("maman", "Une est déjà au chaud."),
        ("papa", "Le cartable est rentré."),
        ("papa", "Toi aussi."),
        ("enfant-f", "J'ai écouté la maîtresse."),
        ("enfant-f", "Un camarade a parlé tout bas."),
        ("narrateur", "Nina pose les mains sur le tapis."),
        ("narrateur", "Le tapis est rêche, puis doux."),
        ("narrateur", "Son ventre se serre, tout petit."),
        ("maman", "C'est un malaise."),
        ("maman", "Tu as bien fait de raconter."),
        ("papa", "On écoute la maîtresse, à l'école."),
        ("papa", "Si malaise, on raconte à la maison."),
        ("enfant-f", "Je raconte à papa, ou à maman."),
        ("narrateur", "En ce moment, Nina enfile sa botte."),
        ("narrateur", "La botte est un peu froide, un peu lisse."),
        ("maman", "L'autre maintenant."),
        ("enfant-f", "Elle colle un peu."),
        ("papa", "Tire doucement."),
        ("papa", "Bravo."),
        ("maman", "Le parc nous attend, tout près."),
        ("enfant-f", "On y va ?"),
        ("maman", "Oui."),
        ("maman", "On t'écoute, aussi dehors."),
        ("narrateur", "La pluie a presque fini, sur le volet."),
    ]
    sons["CHK_T0000_P0000"] = "pluie,porte"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Le parc a trois coins, tout proches."),
        ("maman", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ("papa", "On joue."),
        ("papa", "On a déjà raconté, au salon."),
    ]
    sons["CHK_T0001_P0000"] = "enfants_parc"

    toy_sons = {"ballon": "enfants_parc", "seau": "enfants_parc", "doudou": ""}
    park_sons = {"sable": "enfants_parc", "toboggan": "enfants_parc", "balancoire": "enfants_parc"}

    for p1, park in parks.items():
        by[f"CHK_T0001_{p1}"] = l1[park]
        by[f"CHK_T0001_{p1}_Q0001"] = q[park]
        by[f"CHK_T0001_{p1}_C0001"] = conf[park]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = park_sons[park]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, toy in toys.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_toy[(park, toy)]
            extra_line = extra if extra.endswith((".", "?", "!")) else extra + "."
            by[cid_l2] = toy_scene[toy] + [
                ("narrateur", extra_line),
                ("narrateur", f"Nina est encore près de {park_np[park]}."),
                ("maman", "On écoute la maîtresse."),
                ("maman", "Si malaise, raconter à la maison."),
            ]
            sons[cid_l2] = toy_sons[toy]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, pel in pels.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(park, toy, pel)
                by[f"{cid_l3}_F0001"] = fin(park, toy, pel)
                sons[cid_l3] = "enfants_parc"
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-020",
        {
            "fil_rouge": (
                "Le coussin du salon est tiède. Nina raconte son malaise. "
                "Puis elle joue au parc, avec papa et maman."
            ),
            "title": "Le coussin tiède de Nina",
            "characters": "Nina, papa, maman",
            "setting": "salon, puis parc",
        },
        by,
        sons,
        max_w=18,
    )


if __name__ == "__main__":
    story_019()
    story_020()
    print("ok TREE-COL-019 TREE-COL-020")
