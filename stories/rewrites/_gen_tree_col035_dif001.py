#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-035 et TREE-DIF-001 (texte seulement)."""
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
    "Jules",
    "Gabin",
    "Hugo",
    "Maya",
    "Nora",
    "Kenzo",
    "Zoé",
    "Zoe",
    "Noé",
    "Noe",
    "Corentin",
    "Barnabé",
    "Barnabe",
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
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:60]))


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
        raise SystemExit(f"{story_id} besoin papa et maman")
    adults = " ".join(p for lines in by.values() for r, p in lines if r in ("papa", "maman"))
    if "Bravo" not in adults and "bon travail" not in adults.lower():
        raise SystemExit(f"{story_id} pas de bravo")
    if "?" not in adults:
        raise SystemExit(f"{story_id} pas de question adulte")
    root = " ".join(p for r, p in by["CHK_T0000_P0000"])
    if "En ce moment" not in root:
        raise SystemExit(f"{story_id} root sans « En ce moment »")
    first = by["CHK_T0000_P0000"][0][1]
    if first.startswith(("Aujourd'hui", "C'est le matin", "On va")):
        raise SystemExit(f"{story_id} amorce brutale: {first}")


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


def story_col035() -> None:
    lieux = {"P0001": "boulangerie", "P0002": "etal", "P0003": "fromagerie"}
    gens = {"P0001": "boulangere", "P0002": "voisin", "P0003": "maitresse"}
    objs = {"P0001": "pain", "P0002": "pomme", "P0003": "fromage"}

    lieu_np = {
        "boulangerie": "la boulangerie",
        "etal": "l'étal",
        "fromagerie": "la fromagerie",
    }
    lieu_a = {
        "boulangerie": "à la boulangerie",
        "etal": "à l'étal",
        "fromagerie": "à la fromagerie",
    }
    gen_np = {
        "boulangere": "la boulangère",
        "voisin": "le voisin",
        "maitresse": "la maîtresse",
    }
    obj_np = {
        "pain": "le pain",
        "pomme": "une pomme",
        "fromage": "un fromage",
    }
    obj_le = {
        "pain": "le pain",
        "pomme": "la pomme",
        "fromage": "le fromage",
    }

    lieu_l1 = {
        "boulangerie": [
            ("narrateur", "Raphaël pousse la porte de la boulangerie."),
            ("narrateur", "Une petite cloche fait ding."),
            ("narrateur", "L'air chaud sent le beurre."),
            ("narrateur", "De la farine blanche reste sur le bois."),
            ("narrateur", "Les croûtes dorées sont alignées."),
            ("narrateur", "Papa pose le panier, tout près."),
            ("enfant-m", "Bonjour."),
            ("papa", "Bonjour."),
            ("maman", "On dit bonjour."),
            ("maman", "On dit s'il te plaît."),
            ("maman", "On dit merci."),
            ("narrateur", "Un petit pain attend derrière la vitre."),
            ("papa", "Tu veux celui-là ?"),
            ("enfant-m", "Oui."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le sachet papier fait un bruit doux."),
            ("enfant-m", "Merci."),
            ("maman", "Bravo, Raphaël."),
            ("maman", "Tu as dit les trois mots."),
            ("narrateur", "Le pain reste tiède contre le manteau."),
        ],
        "etal": [
            ("narrateur", "Raphaël s'arrête devant l'étal."),
            ("narrateur", "Les caisses sentent le bois mouillé."),
            ("narrateur", "Des pommes rouges brillent, tout près."),
            ("narrateur", "Un papier vert frissonne au vent."),
            ("narrateur", "Un pigeon picore encore une miette."),
            ("maman", "On dit bonjour, ici aussi."),
            ("enfant-m", "Bonjour."),
            ("papa", "Bonjour."),
            ("papa", "Tu veux une pomme ?"),
            ("enfant-m", "Oui."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Maman pose une pomme dans sa main."),
            ("narrateur", "La peau est lisse, un peu froide."),
            ("enfant-m", "Merci."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit s'il te plaît."),
            ("maman", "Tu as dit merci."),
            ("papa", "On dit les mots, à l'étal."),
            ("narrateur", "Une feuille verte colle à une caisse."),
        ],
        "fromagerie": [
            ("narrateur", "Raphaël entre dans la fromagerie."),
            ("narrateur", "L'air est frais, tout calme."),
            ("narrateur", "Le comptoir de marbre est froid."),
            ("narrateur", "Ça sent le lait, tout doux."),
            ("narrateur", "Un papier blanc attend, tout plié."),
            ("papa", "On dit bonjour."),
            ("enfant-m", "Bonjour."),
            ("maman", "Bonjour."),
            ("maman", "Tu veux goûter l'odeur ?"),
            ("enfant-m", "Oui."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Papa approche le papier, tout lentement."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "Tu as dit les mots."),
            ("maman", "On dit s'il te plaît."),
            ("maman", "On dit merci."),
            ("narrateur", "Une goutte d'eau brille sur le marbre."),
        ],
    }

    q = {
        "boulangerie": [
            ("narrateur", "Raphaël veut le petit pain."),
            ("maman", "Il dit quoi ?"),
        ],
        "etal": [
            ("narrateur", "À l'étal, Raphaël demande."),
            ("papa", "Quels mots ?"),
        ],
        "fromagerie": [
            ("narrateur", "Dans la fromagerie, on salue."),
            ("maman", "Raphaël dit merci ?"),
        ],
    }

    conf = {
        "boulangerie": [
            ("maman", "Oui."),
            ("maman", "On dit bonjour."),
            ("maman", "On dit s'il te plaît."),
            ("maman", "On dit merci."),
            ("narrateur", "Raphaël souffle un peu."),
            ("narrateur", "Le sachet reste tiède dans ses mains."),
            ("enfant-m", "Bonjour."),
            ("enfant-m", "Merci."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "La cloche reste silencieuse, un moment."),
        ],
        "etal": [
            ("papa", "Oui."),
            ("papa", "On dit s'il te plaît."),
            ("papa", "On dit merci."),
            ("narrateur", "Raphaël serre la pomme, tout doux."),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit les mots."),
            ("narrateur", "Le pigeon s'envole, tout près des caisses."),
        ],
        "fromagerie": [
            ("maman", "Oui."),
            ("maman", "On dit bonjour."),
            ("maman", "On dit merci."),
            ("narrateur", "Raphaël touche le papier, tout léger."),
            ("enfant-m", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as salué."),
            ("maman", "Et tu as demandé, tout doux."),
            ("narrateur", "Le marbre reste froid, tout calme."),
        ],
    }

    gen_scene = {
        "boulangere": [
            ("narrateur", "La boulangère a de la farine au tablier."),
            ("narrateur", "Elle tend un sachet, tout lentement."),
            ("enfant-m", "Bonjour."),
            ("maman", "On dit s'il te plaît."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le papier craque, tout doux."),
            ("enfant-m", "Merci."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "Tu as dit les trois mots."),
            ("maman", "On dit bonjour."),
            ("maman", "On dit merci."),
            ("narrateur", "Un peu de farine colle au sachet."),
        ],
        "voisin": [
            ("narrateur", "Le voisin tient un panier d'osier."),
            ("narrateur", "Le panier sent le bois, un peu."),
            ("papa", "On dit bonjour au voisin."),
            ("enfant-m", "Bonjour."),
            ("narrateur", "Le voisin incline un peu la tête."),
            ("maman", "Tu veux passer ?"),
            ("enfant-m", "Oui."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Raphaël recule, tout doux."),
            ("enfant-m", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les mots."),
            ("maman", "On dit s'il te plaît."),
            ("maman", "On dit merci."),
            ("narrateur", "Une anse du panier craque, tout petit."),
        ],
        "maitresse": [
            ("narrateur", "La maîtresse a un sac, tout simple."),
            ("maitresse", "Bonjour, Raphaël."),
            ("enfant-m", "Bonjour."),
            ("maman", "On dit s'il te plaît."),
            ("papa", "Tu veux saluer encore ?"),
            ("enfant-m", "Oui."),
            ("enfant-m", "S'il te plaît."),
            ("maitresse", "Merci, Raphaël."),
            ("enfant-m", "Merci."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit bonjour."),
            ("maman", "On dit les trois mots."),
            ("narrateur", "Le sac de la maîtresse sent le pain."),
        ],
    }

    extra_gen = {
        ("boulangerie", "boulangere"): "La cloche tinte encore, tout loin.",
        ("boulangerie", "voisin"): "Une croûte dore près du panier.",
        ("boulangerie", "maitresse"): "De la farine colle au sac d'école.",
        ("etal", "boulangere"): "Une pomme rouge roule près du tablier.",
        ("etal", "voisin"): "Le pigeon revient, près des caisses.",
        ("etal", "maitresse"): "Le papier vert frôle le sac.",
        ("fromagerie", "boulangere"): "Le marbre refroidit encore le sachet.",
        ("fromagerie", "voisin"): "Le panier d'osier sent le lait.",
        ("fromagerie", "maitresse"): "Le sac pose sur le marbre froid.",
    }

    obj_open = {
        "pain": [
            ("narrateur", "Le pain est encore tiède."),
            ("narrateur", "La croûte fait un petit bruit."),
            ("papa", "Tu veux le pain ?"),
            ("enfant-m", "Oui."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Papa pose le pain dans les mains."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Tu as demandé."),
            ("maman", "Puis tu as dit merci."),
        ],
        "pomme": [
            ("narrateur", "La pomme est rouge, toute lisse."),
            ("narrateur", "Un point jaune brille sur la peau."),
            ("maman", "Tu veux la pomme ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Maman la pose, tout doux."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "Tu as dit s'il te plaît."),
            ("maman", "Et merci, maintenant."),
            ("enfant-m", "Merci."),
        ],
        "fromage": [
            ("narrateur", "Le fromage est dans un papier blanc."),
            ("narrateur", "Le papier fait un bruit doux."),
            ("papa", "On prend le fromage ?"),
            ("enfant-m", "Oui."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Papa tend le paquet, tout lentement."),
            ("enfant-m", "Merci."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit les mots."),
            ("papa", "On dit merci, encore une fois."),
            ("enfant-m", "Merci, papa."),
        ],
    }

    extras = {
        ("boulangerie", "boulangere", "pain"): "La croûte du pain craque, tout doux.",
        ("boulangerie", "boulangere", "pomme"): "La pomme roule près du sachet de farine.",
        ("boulangerie", "boulangere", "fromage"): "Le fromage sent le lait, près du four.",
        ("boulangerie", "voisin", "pain"): "Le voisin tient aussi un pain chaud.",
        ("boulangerie", "voisin", "pomme"): "Une miette reste sur la pomme.",
        ("boulangerie", "voisin", "fromage"): "Le panier du voisin sent le fromage.",
        ("boulangerie", "maitresse", "pain"): "La maîtresse pose le pain dans son sac.",
        ("boulangerie", "maitresse", "pomme"): "La maîtresse essuie la pomme, tout doux.",
        ("boulangerie", "maitresse", "fromage"): "Le fromage glisse dans le sac.",
        ("etal", "boulangere", "pain"): "La boulangère a le pain, à l'étal.",
        ("etal", "boulangere", "pomme"): "La boulangère choisit une pomme rouge.",
        ("etal", "boulangere", "fromage"): "Un papier blanc entoure le fromage.",
        ("etal", "voisin", "pain"): "Le voisin pose le pain sur la caisse.",
        ("etal", "voisin", "pomme"): "Deux pommes se touchent, dans le panier.",
        ("etal", "voisin", "fromage"): "Le fromage pèse un peu, dans les mains.",
        ("etal", "maitresse", "pain"): "La maîtresse sent le pain, tout près.",
        ("etal", "maitresse", "pomme"): "Une feuille verte colle à la pomme.",
        ("etal", "maitresse", "fromage"): "Le fromage reste frais, sous le store.",
        ("fromagerie", "boulangere", "pain"): "Le pain attend près du comptoir froid.",
        ("fromagerie", "boulangere", "pomme"): "La pomme brille, sur le marbre froid.",
        ("fromagerie", "boulangere", "fromage"): "La boulangère touche le papier blanc.",
        ("fromagerie", "voisin", "pain"): "Le voisin pose le pain, tout près.",
        ("fromagerie", "voisin", "pomme"): "La pomme fait un bruit, sur le marbre.",
        ("fromagerie", "voisin", "fromage"): "Le voisin sent le fromage, tout doux.",
        ("fromagerie", "maitresse", "pain"): "La maîtresse range le pain, tout près.",
        ("fromagerie", "maitresse", "pomme"): "La pomme attend dans le sac.",
        ("fromagerie", "maitresse", "fromage"): "Le papier du fromage fait un bruit doux.",
    }

    fin_image = {
        "pain": "Le sachet reste tiède, contre le manteau.",
        "pomme": "La pomme garde un point jaune, tout petit.",
        "fromage": "Le papier blanc se tait, dans le panier.",
    }

    def l3(lieu: str, gen: str, obj: str) -> list[tuple[str, str]]:
        return (
            obj_open[obj]
            + extra_lines(extras[(lieu, gen, obj)])
            + [
                ("narrateur", f"On est encore {lieu_a[lieu]}."),
                ("narrateur", f"Près de {gen_np[gen]}."),
                ("papa", "Tu as dit les mots ?"),
                ("enfant-m", "Oui."),
                ("enfant-m", "Bonjour."),
                ("enfant-m", "S'il te plaît."),
                ("enfant-m", "Merci."),
                ("maman", "Bravo, Raphaël."),
                ("maman", "Tu as fait du bon travail."),
                ("narrateur", f"Raphaël range {obj_le[obj]}, tout doux."),
            ]
        )

    def fin(lieu: str, gen: str, obj: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "Bonjour."),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
            ("maman", "Bravo, Raphaël."),
            ("papa", "Tu as dit les trois mots."),
            ("narrateur", f"Raphaël a vécu {lieu_a[lieu]}."),
            ("narrateur", f"Il a salué {gen_np[gen]}."),
            ("narrateur", f"Il tient {obj_le[obj]}."),
            ("narrateur", fin_image[obj]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois visages attendent, tout proches."),
            ("maman", "La boulangère, le voisin, ou la maîtresse ?"),
            ("papa", "On dit bonjour."),
            ("papa", "On dit merci."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois choses brillent, dans le panier."),
            ("papa", "Le pain, une pomme, ou un fromage ?"),
            ("maman", "On dit encore les mots."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Un store rayé goutte encore, au-dessus des caisses."),
        ("narrateur", "Une goutte tombe sur le pavé."),
        ("narrateur", "Elle fait un petit cercle, tout brillant."),
        ("narrateur", "Un pigeon picore une miette, près d'une caisse."),
        ("narrateur", "La caisse sent le bois mouillé."),
        ("narrateur", "Ça sent le pain chaud, déjà."),
        ("narrateur", "Papa porte un panier d'osier."),
        ("narrateur", "Le panier a un trou, tout petit."),
        ("narrateur", "Maman noue l'écharpe de Raphaël."),
        ("narrateur", "L'écharpe est rouge, un peu rêche."),
        ("papa", "Tu as vu le pigeon ?"),
        ("enfant-m", "Il a une miette."),
        ("maman", "Le store est encore mouillé."),
        ("narrateur", "En ce moment, Raphaël touche le panier."),
        ("narrateur", "L'osier pique un peu, puis cède."),
        ("papa", "On marche vers les étals."),
        ("maman", "On dit les mots, au marché."),
        ("maman", "On dit bonjour."),
        ("maman", "On dit s'il te plaît."),
        ("maman", "On dit merci."),
        ("enfant-m", "Bonjour."),
        ("papa", "Bravo, Raphaël."),
        ("narrateur", "Une autre goutte tombe, sur la chaussure."),
        ("narrateur", "La chaussure fait un petit toc, sur le pavé."),
    ]
    sons["CHK_T0000_P0000"] = "goutte,oiseau"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Trois coins du marché attendent."),
        ("papa", "La boulangerie, l'étal, ou la fromagerie ?"),
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
            "boulangerie": "cloche",
            "etal": "oiseau",
            "fromagerie": "",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, gen in gens.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                gen_scene[gen]
                + extra_lines(extra_gen[(lieu, gen)])
                + [
                    ("narrateur", f"On est encore {lieu_a[lieu]}."),
                    ("maman", "On dit s'il te plaît."),
                    ("maman", "On dit merci."),
                ]
            )
            sons[cid_l2] = {
                "boulangere": "papier",
                "voisin": "",
                "maitresse": "",
            }[gen]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, obj in objs.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, gen, obj)
                by[f"{cid_l3}_F0001"] = fin(lieu, gen, obj)
                sons[cid_l3] = {"pain": "pain", "pomme": "", "fromage": "papier"}[obj]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-035",
        {
            "fil_rouge": (
                "Sous le store goutteux du marché, Raphaël tient le panier troué. "
                "Il dit bonjour, s'il te plaît, merci, à chaque étal, avec papa et maman."
            ),
            "title": "Le store goutteux et les trois mots",
            "characters": "Raphaël, papa, maman",
            "setting": "marché sous le store, boulangerie, étal, fromagerie",
        },
        by,
        sons,
        max_words=15,
    )


def story_dif001() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    souvenirs = {"P0001": "coquillage", "P0002": "galet", "P0003": "filet"}

    lieu_np = {
        "cuisine": "la cuisine",
        "jardin": "le jardin",
        "chambre": "la chambre",
    }
    lieu_dans = {
        "cuisine": "dans la cuisine",
        "jardin": "dans le jardin",
        "chambre": "dans la chambre",
    }
    jouet_np = {
        "ballon": "le ballon rouge",
        "seau": "le seau bleu",
        "doudou": "le doudou",
    }
    souv_np = {
        "coquillage": "le coquillage",
        "galet": "le galet",
        "filet": "le filet",
    }

    lieu_l1 = {
        "cuisine": [
            ("narrateur", "Après la mer, la cuisine est tiède."),
            ("narrateur", "L'eau coule, tout petit bruit."),
            ("narrateur", "Un coquillage attend près de l'évier."),
            ("narrateur", "Sarah est plus grande."),
            ("narrateur", "Aniss est plus petit."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "Tu viens ?"),
            ("enfant-f", "Oui."),
            ("maman", "On invite."),
            ("maman", "On joue ensemble."),
            ("narrateur", "Sarah lave le coquillage, tout haut."),
            ("narrateur", "Aniss tient l'anse, plus bas."),
            ("papa", "Vous jouez ensemble ?"),
            ("enfant-m", "Oui, papa."),
            ("papa", "Bravo, Aniss."),
            ("papa", "Tu as invité."),
            ("narrateur", "Une goutte brille sur le carrelage."),
        ],
        "jardin": [
            ("narrateur", "Après la mer, l'herbe est tiède."),
            ("narrateur", "Un linge sèche, tout blanc."),
            ("narrateur", "Sarah tient un arrosoir, plus haut."),
            ("narrateur", "Aniss tient une pelle, plus petite."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "On verse l'eau ?"),
            ("enfant-f", "Oui."),
            ("maman", "On invite."),
            ("maman", "On joue ensemble."),
            ("narrateur", "Ils versent, tout doux."),
            ("narrateur", "L'eau fait un petit cercle."),
            ("papa", "Bravo."),
            ("papa", "Vous jouez ensemble."),
            ("enfant-m", "Sarah est grande."),
            ("maman", "Et toi, plus petit."),
            ("maman", "On peut jouer ensemble."),
            ("narrateur", "Une feuille colle à la chaussette."),
        ],
        "chambre": [
            ("narrateur", "Après la mer, la chambre est calme."),
            ("narrateur", "La couverture est douce."),
            ("narrateur", "Un oreiller devient un bateau."),
            ("narrateur", "Sarah pose un galet, tout haut."),
            ("narrateur", "Aniss pose le coquillage, plus bas."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "Tu viens sur le bateau ?"),
            ("enfant-f", "Oui."),
            ("papa", "On invite."),
            ("papa", "On joue ensemble."),
            ("maman", "Bravo, Aniss."),
            ("maman", "Tu as invité Sarah."),
            ("narrateur", "Ils poussent l'oreiller, tout doux."),
            ("enfant-f", "La mer chante encore."),
            ("narrateur", "Un rayon pose sur le plaid."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Aniss invite Sarah."),
            ("maman", "Ils font quoi ?"),
        ],
        "jardin": [
            ("narrateur", "Les tailles sont différentes."),
            ("papa", "On fait quoi ?"),
        ],
        "chambre": [
            ("narrateur", "Aniss a invité Sarah."),
            ("maman", "On joue ensemble ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("maman", "Oui."),
            ("maman", "On joue ensemble."),
            ("narrateur", "Aniss souffle un peu."),
            ("narrateur", "Le coquillage reste mouillé."),
            ("enfant-m", "On joue."),
            ("papa", "Bravo."),
            ("papa", "Tu as invité."),
            ("maman", "Les tailles sont différentes."),
            ("maman", "On peut jouer ensemble."),
            ("narrateur", "L'eau coule encore, tout fin."),
        ],
        "jardin": [
            ("papa", "Oui."),
            ("papa", "On joue ensemble."),
            ("narrateur", "Aniss tient encore la pelle."),
            ("enfant-m", "On invite."),
            ("maman", "Bravo, Aniss."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Sarah verse une dernière goutte."),
            ("maman", "Les tailles sont différentes."),
            ("narrateur", "L'herbe brille, tout calme."),
        ],
        "chambre": [
            ("maman", "Oui."),
            ("maman", "On invite."),
            ("maman", "On joue ensemble."),
            ("narrateur", "Aniss hoche la tête."),
            ("enfant-m", "On joue."),
            ("papa", "Bravo."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", "Le bateau-oreiller s'arrête, tout doux."),
            ("narrateur", "Le rayon glisse encore."),
        ],
    }

    jouet_scene = {
        "ballon": [
            ("narrateur", "Aniss pose le ballon rouge."),
            ("narrateur", "Le ballon est un peu sablé."),
            ("enfant-m", "Tu veux jouer ?"),
            ("enfant-f", "Oui."),
            ("narrateur", "Sarah est plus grande."),
            ("narrateur", "Elle rattrape le ballon, tout haut."),
            ("narrateur", "Aniss le pousse, plus bas."),
            ("maman", "Les tailles sont différentes."),
            ("maman", "On joue ensemble."),
            ("papa", "Bravo, Aniss."),
            ("papa", "Tu as invité."),
            ("narrateur", "Le ballon roule, tout doux."),
        ],
        "seau": [
            ("narrateur", "Aniss prend le seau bleu."),
            ("narrateur", "L'anse est un peu rêche."),
            ("enfant-m", "On le tient ensemble ?"),
            ("enfant-f", "Oui."),
            ("narrateur", "Sarah tient l'anse, tout haut."),
            ("narrateur", "Aniss tient le bord, plus bas."),
            ("papa", "Les tailles sont différentes."),
            ("papa", "On peut jouer ensemble."),
            ("maman", "Bravo."),
            ("maman", "Vous jouez ensemble."),
            ("narrateur", "Un peu d'eau tremble, dans le seau."),
        ],
        "doudou": [
            ("narrateur", "Aniss pose le doudou."),
            ("narrateur", "Le tissu est encore sablé."),
            ("enfant-m", "Tu le caresses ?"),
            ("enfant-f", "Oui."),
            ("narrateur", "Sarah est plus grande."),
            ("narrateur", "Sa main couvre presque le doudou."),
            ("narrateur", "La main d'Aniss est plus petite."),
            ("maman", "On invite."),
            ("maman", "On joue ensemble."),
            ("papa", "Bravo, Aniss."),
            ("papa", "Tu as invité Sarah."),
            ("narrateur", "Le doudou a une oreille froissée."),
        ],
    }

    extra_jouet = {
        ("cuisine", "ballon"): "Le ballon frôle l'évier, tout doux.",
        ("cuisine", "seau"): "Le seau pose sous le robinet.",
        ("cuisine", "doudou"): "Le doudou s'assoit sur une chaise sèche.",
        ("jardin", "ballon"): "Le ballon roule dans l'herbe tiède.",
        ("jardin", "seau"): "Le seau attend sous le robinet du jardin.",
        ("jardin", "doudou"): "Le doudou s'abrite sous le linge.",
        ("chambre", "ballon"): "Le ballon rouge devient un phare.",
        ("chambre", "seau"): "Le seau bleu se cache derrière le lit.",
        ("chambre", "doudou"): "Le doudou se cale sous la couverture.",
    }

    souv_open = {
        "coquillage": [
            ("narrateur", "Le coquillage a encore un trou."),
            ("narrateur", "Aniss le tend à Sarah."),
            ("enfant-m", "Tu regardes ?"),
            ("enfant-f", "Oui."),
            ("narrateur", "Sarah le lève, tout haut."),
            ("narrateur", "Aniss le voit, plus bas."),
            ("maman", "Les tailles sont différentes."),
            ("maman", "On joue ensemble."),
            ("papa", "Bravo."),
            ("papa", "Tu as invité."),
        ],
        "galet": [
            ("narrateur", "Le galet est lisse, tout gris."),
            ("narrateur", "Il sent encore la mer."),
            ("enfant-m", "On le pose ensemble ?"),
            ("enfant-f", "Oui."),
            ("narrateur", "Sarah pose le galet, tout doux."),
            ("papa", "On invite."),
            ("papa", "On joue ensemble."),
            ("maman", "Bravo, Aniss."),
            ("maman", "C'est du bon travail."),
        ],
        "filet": [
            ("narrateur", "Le filet sent le sel, un peu."),
            ("narrateur", "Sarah le tient, tout haut."),
            ("narrateur", "Aniss tient un bout, plus bas."),
            ("enfant-m", "On tire doucement ?"),
            ("enfant-f", "Oui."),
            ("maman", "Les tailles sont différentes."),
            ("maman", "On peut jouer ensemble."),
            ("papa", "Bravo."),
            ("papa", "Vous jouez ensemble."),
        ],
    }

    extras = {
        ("cuisine", "ballon", "coquillage"): "Le coquillage sonne contre le ballon.",
        ("cuisine", "ballon", "galet"): "Le galet attend près de l'évier.",
        ("cuisine", "ballon", "filet"): "Le filet sèche près du ballon rouge.",
        ("cuisine", "seau", "coquillage"): "Le coquillage trempe dans le seau.",
        ("cuisine", "seau", "galet"): "Le galet pèse au fond du seau.",
        ("cuisine", "seau", "filet"): "Le filet goutte au-dessus du seau.",
        ("cuisine", "doudou", "coquillage"): "Le coquillage dort près du doudou.",
        ("cuisine", "doudou", "galet"): "Le galet chauffe contre le doudou.",
        ("cuisine", "doudou", "filet"): "Le filet couvre un peu le doudou.",
        ("jardin", "ballon", "coquillage"): "Le coquillage brille dans l'herbe.",
        ("jardin", "ballon", "galet"): "Le galet arrête le ballon, tout doux.",
        ("jardin", "ballon", "filet"): "Le filet sèche au vent, près du ballon.",
        ("jardin", "seau", "coquillage"): "Le coquillage flotte dans le seau.",
        ("jardin", "seau", "galet"): "Le galet tapote l'anse du seau.",
        ("jardin", "seau", "filet"): "Le filet s'égoutte dans le seau bleu.",
        ("jardin", "doudou", "coquillage"): "Le coquillage se cache sous le doudou.",
        ("jardin", "doudou", "galet"): "Le galet pèse sur le doudou, tout léger.",
        ("jardin", "doudou", "filet"): "Le filet abrite le doudou, au soleil.",
        ("chambre", "ballon", "coquillage"): "Le coquillage est le trésor du phare.",
        ("chambre", "ballon", "galet"): "Le galet ancre le bateau-oreiller.",
        ("chambre", "ballon", "filet"): "Le filet devient une voile, tout douce.",
        ("chambre", "seau", "coquillage"): "Le coquillage revient du seau caché.",
        ("chambre", "seau", "galet"): "Le galet roule derrière le lit.",
        ("chambre", "seau", "filet"): "Le filet sort du seau, tout salé.",
        ("chambre", "doudou", "coquillage"): "Le coquillage chuchote près du doudou.",
        ("chambre", "doudou", "galet"): "Le galet chauffe sous la couverture.",
        ("chambre", "doudou", "filet"): "Le filet couvre doudou et oreiller.",
    }

    fin_image = {
        "coquillage": "Le trou du coquillage laisse encore le ciel.",
        "galet": "Le galet reste lisse, tout calme.",
        "filet": "Le filet sent encore le sel, tout loin.",
    }

    def l3(lieu: str, jouet: str, souv: str) -> list[tuple[str, str]]:
        return (
            souv_open[souv]
            + extra_lines(extras[(lieu, jouet, souv)])
            + [
                ("narrateur", f"On est encore {lieu_dans[lieu]}."),
                ("narrateur", f"{jouet_np[jouet].capitalize()} est rangé, presque."),
                ("papa", "Vous jouez encore ensemble ?"),
                ("enfant-m", "Oui."),
                ("enfant-f", "Oui."),
                ("maman", "Bravo."),
                ("maman", "Les tailles sont différentes."),
                ("maman", "On joue ensemble."),
                ("narrateur", f"Aniss pose {souv_np[souv]}, tout doux."),
            ]
        )

    def fin(lieu: str, jouet: str, souv: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "On a joué ensemble."),
            ("enfant-f", "Oui."),
            ("maman", "Bravo, Aniss."),
            ("papa", "Tu as invité Sarah."),
            ("narrateur", f"Aniss a vécu {lieu_dans[lieu]}."),
            ("narrateur", f"Ils ont joué avec {jouet_np[jouet]}."),
            ("narrateur", f"Ils ont gardé {souv_np[souv]}."),
            ("narrateur", fin_image[souv]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout proches."),
            ("maman", "Le ballon rouge, le seau bleu, ou le doudou ?"),
            ("papa", "On invite."),
            ("papa", "On joue ensemble."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois souvenirs de mer attendent."),
            ("papa", "Le coquillage, le galet, ou le filet ?"),
            ("maman", "On joue encore ensemble."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le vent secoue une serviette, tout blanche."),
        ("narrateur", "Du sable tombe, en petite pluie."),
        ("narrateur", "Un coquillage a un trou, tout rond."),
        ("narrateur", "La mer chante, tout loin, tout bas."),
        ("narrateur", "Le sable mouillé colle aux orteils."),
        ("narrateur", "Papa a retroussé son pantalon."),
        ("narrateur", "Maman secoue encore la serviette."),
        ("narrateur", "Deux empreintes brillent, dans le sable."),
        ("narrateur", "Une petite."),
        ("narrateur", "Une plus grande."),
        ("papa", "Tu as vu les traces ?"),
        ("enfant-m", "Elles sont différentes."),
        ("maman", "Oui."),
        ("maman", "Les tailles sont différentes."),
        ("narrateur", "En ce moment, Aniss ramasse le coquillage."),
        ("narrateur", "Le trou laisse passer le ciel."),
        ("narrateur", "Sarah arrive, plus grande."),
        ("narrateur", "Ses pieds font des traces plus longues."),
        ("enfant-m", "Tu viens jouer ?"),
        ("enfant-f", "Oui."),
        ("maman", "On invite."),
        ("maman", "On joue ensemble."),
        ("papa", "Bravo, Aniss."),
        ("papa", "Tu as invité."),
        ("narrateur", "Ils posent le coquillage, tout doux."),
        ("narrateur", "Le vent pousse encore la serviette."),
    ]
    sons["CHK_T0000_P0000"] = "oiseau"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "La mer reste derrière, tout loin."),
        ("papa", "La cuisine, le jardin, ou la chambre ?"),
        ("maman", "On invite."),
        ("maman", "On joue ensemble."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "cuisine": "eau",
            "jardin": "oiseau",
            "chambre": "",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                jouet_scene[jouet]
                + extra_lines(extra_jouet[(lieu, jouet)])
                + [
                    ("narrateur", f"On est encore {lieu_dans[lieu]}."),
                    ("maman", "On invite."),
                    ("maman", "On joue ensemble."),
                ]
            )
            sons[cid_l2] = {
                "ballon": "ballon",
                "seau": "eau",
                "doudou": "",
            }[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, souv in souvenirs.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, souv)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, souv)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-DIF-001",
        {
            "fil_rouge": (
                "Sur le sable, deux empreintes : une petite, une plus grande. "
                "Aniss invite Sarah. Les tailles sont différentes. Ils jouent ensemble, "
                "jusque dans la maison, avec un souvenir de mer."
            ),
            "title": "Les empreintes et le coquillage d'Aniss",
            "characters": "Aniss, Sarah, papa, maman",
            "setting": "bord de mer, puis cuisine, jardin, chambre",
        },
        by,
        sons,
        max_words=10,
    )


if __name__ == "__main__":
    story_col035()
    story_dif001()
