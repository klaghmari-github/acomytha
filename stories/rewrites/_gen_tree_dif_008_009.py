#!/usr/bin/env python3
"""Génère merged.json pour TREE-DIF-008 et TREE-DIF-009 (texte seulement)."""
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
    "Kenzo",
    "Hugo",
    "Jules",
    "Maya",
    "Zoé",
    "Zoe",
    "Sara",
    "Inès",
    "Ines",
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
            if not ph.strip():
                bad.append(f"{cid} empty {role}")
    if bad:
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:50]))


def check_text(story_id: str, by: dict[str, list[tuple[str, str]]]) -> None:
    blob = " ".join(ph for lines in by.values() for _, ph in lines)
    low = blob.lower()
    for s in FORBIDDEN_SUB:
        if s.lower() in low:
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


def sent(extra: str) -> list[tuple[str, str]]:
    parts = [p.strip() for p in extra.split(". ") if p.strip()]
    return [("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in parts]


def path_text(by: dict[str, list[tuple[str, str]]], ids: list[str]) -> str:
    return " ".join(ph for cid in ids for _, ph in by[cid]).lower()


def _stem_ok(blob: str, needle: str) -> bool:
    words = [
        w
        for w in re.findall(r"[a-zàâäéèêëïîôùûüçœ-]{3,}", needle.lower())
        if w not in ("une", "des", "les", "est", "avec", "pour", "dans")
    ]

    def stem(w: str) -> str:
        for suf in ("er", "ir", "ez", "ent", "ons", "ait"):
            if w.endswith(suf) and len(w) > len(suf) + 2:
                return w[: -len(suf)]
        return w

    if needle.lower() in blob:
        return True
    if words and all(stem(w) in blob or w in blob for w in words[:2]):
        return True
    return False


def check_cover(story_id: str, by: dict[str, list[tuple[str, str]]], needles: tuple[str, ...]) -> None:
    p1s = ("P0001", "P0002", "P0003")
    for a in p1s:
        for b in p1s:
            for c in p1s:
                ids = [
                    "CHK_T0000_P0000",
                    "CHK_T0001_P0000",
                    f"CHK_T0001_{a}",
                    f"CHK_T0001_{a}_Q0001",
                    f"CHK_T0001_{a}_C0001",
                    f"CHK_T0001_{a}_T0002_P0000",
                    f"CHK_T0001_{a}_T0002_{b}",
                    f"CHK_T0001_{a}_T0002_{b}_T0003_P0000",
                    f"CHK_T0001_{a}_T0002_{b}_T0003_{c}",
                    f"CHK_T0001_{a}_T0002_{b}_T0003_{c}_F0001",
                ]
                blob = path_text(by, ids)
                miss = [n for n in needles if not _stem_ok(blob, n)]
                if miss:
                    raise SystemExit(f"{story_id} cover {a}/{b}/{c}: {miss}")


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str],
    max_words: int,
    needles: tuple[str, ...],
) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:8]} extra={extra[:8]}")
    check_phrases(story_id, by_id, max_words)
    check_text(story_id, by_id)
    check_cover(story_id, by_id, needles)
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


def story_008() -> None:
    transports = {"P0001": "train", "P0002": "bus", "P0003": "voiture"}
    peluches = {"P0001": "Tom", "P0002": "Léa", "P0003": "Sami"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}
    tr_np = {
        "train": "le train en bois",
        "bus": "le bus jaune",
        "voiture": "la voiture verte",
    }
    pel_np = {
        "Tom": "l'ours Tom",
        "Léa": "la poupée Léa",
        "Sami": "le canard Sami",
    }
    moment_np = {
        "matin": "le matin",
        "sieste": "après la sieste",
        "soir": "le soir",
    }
    reponse = {"Tom": "Non.", "Léa": "Je regarde.", "Sami": "Plus tard."}

    lieu_l1 = {
        "train": [
            ("narrateur", "Raphaël prend le train en bois."),
            ("narrateur", "Les roues sont rouges, un peu rêches."),
            ("narrateur", "Ça sent le pin, tout doux."),
            ("narrateur", "Un wagon minuscule a une fenêtre peinte."),
            ("enfant-m", "Mila, tu viens ?"),
            ("copine", "Non."),
            ("narrateur", "Raphaël garde le train dans ses mains."),
            ("enfant-m", "D'accord."),
            ("papa", "Tu as proposé."),
            ("papa", "On peut accepter plusieurs réponses."),
            ("maman", "Non, c'est une réponse."),
            ("maman", "Bravo, Raphaël."),
            ("maman", "Tu as fait du bon travail."),
            ("papa", "Plus tard, c'est possible."),
            ("narrateur", "Le train reste sur la caisse, tout calme."),
            ("narrateur", "Une orange roule, tout près."),
        ],
        "bus": [
            ("narrateur", "Raphaël pousse le bus jaune."),
            ("narrateur", "Les fenêtres sont peintes en bleu."),
            ("narrateur", "Une roue fait un petit clic."),
            ("narrateur", "Le pavé est froid sous les genoux."),
            ("enfant-m", "Tu viens voir le bus ?"),
            ("copine", "Je regarde."),
            ("narrateur", "Mila reste près du panier."),
            ("enfant-m", "D'accord."),
            ("maman", "Regarder, c'est une réponse."),
            ("papa", "On peut proposer."),
            ("papa", "On peut accepter plusieurs réponses."),
            ("maman", "Bravo, Raphaël."),
            ("papa", "Tu as su attendre."),
            ("narrateur", "Le bus s'arrête près d'une fraise."),
            ("narrateur", "Le papier tache un peu le jaune."),
        ],
        "voiture": [
            ("narrateur", "Raphaël prend la petite voiture verte."),
            ("narrateur", "Le capot est lisse, un peu froid."),
            ("narrateur", "Une portière peinte a un point blanc."),
            ("narrateur", "Ça sent encore la fraise, tout près."),
            ("enfant-m", "On joue ?"),
            ("copine", "Plus tard."),
            ("enfant-m", "D'accord."),
            ("papa", "Plus tard, c'est une réponse."),
            ("maman", "On peut proposer."),
            ("maman", "On peut accepter plusieurs réponses."),
            ("papa", "Bravo, Raphaël."),
            ("maman", "Tu as accepté."),
            ("narrateur", "La voiture verte attend sur le stand."),
            ("narrateur", "Une feuille de chou tremble au vent."),
        ],
    }

    q = {
        "train": [
            ("narrateur", "Raphaël a proposé le train."),
            ("papa", "On propose sans forcer ?"),
        ],
        "bus": [
            ("narrateur", "Mila regarde le bus."),
            ("maman", "On accepte plusieurs réponses ?"),
        ],
        "voiture": [
            ("narrateur", "Raphaël a invité Mila."),
            ("papa", "On invite, et après ?"),
        ],
    }

    conf = {
        "train": [
            ("papa", "Oui."),
            ("papa", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("narrateur", "Raphaël souffle un peu."),
            ("narrateur", "Le bois du train reste froid."),
            ("enfant-m", "D'accord, Mila."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Une goutte tombe encore du store."),
        ],
        "bus": [
            ("maman", "Oui."),
            ("maman", "On propose."),
            ("maman", "On accepte plusieurs réponses."),
            ("narrateur", "Raphaël laisse une place, tout près."),
            ("enfant-m", "Tu regardes."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Le bus jaune reste immobile."),
        ],
        "voiture": [
            ("papa", "Oui."),
            ("papa", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("narrateur", "Raphaël hoche la tête."),
            ("enfant-m", "Plus tard, d'accord."),
            ("maman", "Bravo."),
            ("maman", "Tu as fait du bon travail."),
            ("narrateur", "Le sac de papa penche un peu."),
        ],
    }

    pel_scene = {
        "Tom": [
            ("narrateur", "Raphaël prend l'ours Tom."),
            ("narrateur", "Le ventre a une tache de fraise."),
            ("narrateur", "Une oreille est un peu froissée."),
            ("enfant-m", "Tu viens avec Tom ?"),
            ("copine", "Non."),
            ("enfant-m", "D'accord."),
            ("papa", "Tu as proposé."),
            ("maman", "On peut accepter plusieurs réponses."),
            ("papa", "Bravo."),
            ("narrateur", "L'ours Tom reste contre le panier."),
        ],
        "Léa": [
            ("narrateur", "Raphaël prend la poupée Léa."),
            ("narrateur", "Elle a un chapeau de paille, tout petit."),
            ("narrateur", "Un bouton brille, tout rond."),
            ("enfant-m", "Tu joues avec Léa ?"),
            ("copine", "Je regarde."),
            ("enfant-m", "D'accord."),
            ("maman", "Regarder, c'est une réponse."),
            ("papa", "On peut proposer."),
            ("papa", "On accepte plusieurs réponses."),
            ("narrateur", "La poupée Léa s'assoit près des oranges."),
        ],
        "Sami": [
            ("narrateur", "Raphaël prend le canard Sami."),
            ("narrateur", "Le bec est en bois, tout lisse."),
            ("narrateur", "Le jaune a une poussière de marché."),
            ("enfant-m", "Plus tard, avec Sami ?"),
            ("copine", "Plus tard."),
            ("enfant-m", "D'accord."),
            ("papa", "Plus tard, c'est possible."),
            ("maman", "On peut accepter plusieurs réponses."),
            ("narrateur", "Le canard Sami penche la tête."),
        ],
    }

    extra_pel = {
        ("train", "Tom"): "Une roue rouge touche l'oreille de Tom.",
        ("train", "Léa"): "La poupée Léa a le chapeau dans le wagon.",
        ("train", "Sami"): "Le canard Sami penche vers le train.",
        ("bus", "Tom"): "L'ours Tom a le museau contre le bus.",
        ("bus", "Léa"): "La poupée Léa regarde une fenêtre peinte.",
        ("bus", "Sami"): "Le canard Sami a une poussière jaune.",
        ("voiture", "Tom"): "L'ours Tom est trop grand pour la voiture.",
        ("voiture", "Léa"): "La poupée Léa a le chapeau sur le capot.",
        ("voiture", "Sami"): "Le canard Sami glisse près de la portière.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, le soleil pose sur les oranges."),
            ("narrateur", "Une goutte brille encore, sur le store."),
            ("narrateur", "Ça sent le cacao, au stand du pain."),
            ("papa", "Bonjour, Raphaël."),
            ("enfant-m", "Bonjour, papa."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, les pavés sont chauds."),
            ("narrateur", "Le panier a un pli, tout doux."),
            ("narrateur", "La place est plus calme, un peu."),
            ("maman", "Tu es réveillé ?"),
            ("enfant-m", "Oui, maman."),
        ],
        "soir": [
            ("narrateur", "Le soir, une lanterne fait un rond."),
            ("narrateur", "Ça sent le pain, tout chaud."),
            ("narrateur", "Les caisses claquent, tout loin."),
            ("papa", "Te voilà, Raphaël."),
            ("enfant-m", "Bonjour, papa."),
        ],
    }

    extras = {
        ("train", "Tom", "matin"): "L'ours Tom a du soleil sur le museau.",
        ("train", "Tom", "sieste"): "L'ours Tom chauffe contre le wagon.",
        ("train", "Tom", "soir"): "L'ours Tom a une ombre de lanterne.",
        ("train", "Léa", "matin"): "La poupée Léa a le chapeau tout clair.",
        ("train", "Léa", "sieste"): "La poupée Léa s'adosse au train, tout calme.",
        ("train", "Léa", "soir"): "La poupée Léa brille sous la lanterne.",
        ("train", "Sami", "matin"): "Le canard Sami a une goutte sur le bec.",
        ("train", "Sami", "sieste"): "Le canard Sami est tiède, près du wagon.",
        ("train", "Sami", "soir"): "Le canard Sami écoute les caisses, tout loin.",
        ("bus", "Tom", "matin"): "L'ours Tom regarde le bus jaune, tout calme.",
        ("bus", "Tom", "sieste"): "L'ours Tom a une poussière de pavé.",
        ("bus", "Tom", "soir"): "L'ours Tom penche vers le bus, tout doux.",
        ("bus", "Léa", "matin"): "La poupée Léa a le chapeau contre le bus.",
        ("bus", "Léa", "sieste"): "La poupée Léa a chaud, près du pavé.",
        ("bus", "Léa", "soir"): "La poupée Léa a une ombre de roue.",
        ("bus", "Sami", "matin"): "Le canard Sami glisse près d'une roue jaune.",
        ("bus", "Sami", "sieste"): "Le canard Sami a le bec sur le bus.",
        ("bus", "Sami", "soir"): "Le canard Sami écoute un clic, tout petit.",
        ("voiture", "Tom", "matin"): "L'ours Tom tient le capot vert, trop grand.",
        ("voiture", "Tom", "sieste"): "L'ours Tom a le ventre tiède, près de la voiture.",
        ("voiture", "Tom", "soir"): "L'ours Tom a une ombre verte, tout longue.",
        ("voiture", "Léa", "matin"): "La poupée Léa a le bouton contre le capot.",
        ("voiture", "Léa", "sieste"): "La poupée Léa s'assoit près de la portière.",
        ("voiture", "Léa", "soir"): "La poupée Léa brille, près du point blanc.",
        ("voiture", "Sami", "matin"): "Le canard Sami a le bec sur le capot.",
        ("voiture", "Sami", "sieste"): "Le canard Sami est tiède, comme le pavé.",
        ("voiture", "Sami", "soir"): "Le canard Sami écoute la lanterne, tout bas.",
    }

    fin_image = {
        "matin": "Une orange garde encore le soleil.",
        "sieste": "Le pavé redevient calme, tout chaud.",
        "soir": "La lanterne reste allumée, tout doux.",
    }

    def l3(tr: str, pel: str, moment: str) -> list[tuple[str, str]]:
        return (
            moment_open[moment]
            + [
                ("narrateur", f"Raphaël a encore {tr_np[tr]}."),
                ("narrateur", f"Il tient {pel_np[pel]}."),
            ]
            + sent(extras[(tr, pel, moment)])
            + [
                ("enfant-m", "Mila, tu viens ?"),
                ("copine", reponse[pel]),
                ("enfant-m", "D'accord."),
                ("papa", "On propose."),
                ("maman", "On accepte plusieurs réponses."),
                ("maman", "Non, regarder, ou plus tard."),
                ("papa", "Bravo, Raphaël."),
                ("papa", "Tu as fait du bon travail."),
                ("enfant-m", "Merci, papa."),
                ("enfant-m", "Merci, maman."),
                ("narrateur", f"Raphaël range {pel_np[pel]}, tout doux."),
            ]
        )

    def fin(tr: str, pel: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "J'ai proposé."),
            ("enfant-m", "J'ai accepté."),
            ("maman", "Bravo, Raphaël."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Raphaël a vécu {moment_np[moment]}, près du stand."),
            ("narrateur", f"Il a joué avec {tr_np[tr]}."),
            ("narrateur", f"Il a tenu {pel_np[pel]}."),
            ("narrateur", fin_image[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois peluches attendent sur le stand."),
            ("narrateur", "Un ours, une poupée, un canard."),
            ("maman", "Tom, Léa, ou Sami ?"),
            ("papa", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Quel moment, maintenant ?"),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On propose encore."),
            ("maman", "On accepte plusieurs réponses."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Une caisse d'oranges tremble, tout bas."),
        ("narrateur", "Une goutte glisse du store rayé."),
        ("narrateur", "Elle fait ploc sur le pavé."),
        ("narrateur", "Le pavé est encore mouillé, tout gris."),
        ("narrateur", "Une feuille de chou colle à la chaussure de Raphaël."),
        ("narrateur", "Le panier de maman a une anse rêche."),
        ("narrateur", "Papa plie un sac en toile, un peu lourd."),
        ("narrateur", "Ça sent la fraise écrasée, sur le papier."),
        ("narrateur", "Une poule glousse, tout loin, derrière le stand."),
        ("narrateur", "Mila a un manteau rouge, trop long."),
        ("narrateur", "Les manches cachent un peu ses mains."),
        ("papa", "Tu entends la poule, Raphaël ?"),
        ("enfant-m", "Oui, papa."),
        ("enfant-m", "Les fraises sont froides."),
        ("maman", "Le panier pique un peu."),
        ("maman", "L'anse est en osier."),
        ("narrateur", "En ce moment, Raphaël touche le bois du stand."),
        ("narrateur", "Le bois est rêche, puis lisse."),
        ("narrateur", "Un train en bois attend sur le stand."),
        ("narrateur", "Un bus jaune est à côté."),
        ("narrateur", "Une petite voiture verte brille."),
        ("narrateur", "Mila regarde les roues, tout calme."),
        ("maman", "On peut proposer un jeu, Raphaël."),
        ("enfant-m", "Oui, maman."),
        ("papa", "Mila peut dire non."),
        ("papa", "Ou regarder."),
        ("papa", "Ou plus tard."),
    ]
    sons["CHK_T0000_P0000"] = "goutte"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Trois jouets en bois attendent."),
        ("papa", "Le train, le bus, ou la voiture ?"),
        ("maman", "On propose."),
        ("maman", "On accepte plusieurs réponses."),
        ("papa", "On joue ensemble si l'autre veut."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, tr in transports.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[tr]
        by[f"CHK_T0001_{p1}_Q0001"] = q[tr]
        by[f"CHK_T0001_{p1}_C0001"] = conf[tr]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = ""
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, pel in peluches.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                pel_scene[pel]
                + sent(extra_pel[(tr, pel)])
                + [
                    ("narrateur", f"On est encore près de {tr_np[tr]}."),
                    ("maman", "On propose."),
                    ("maman", "On accepte plusieurs réponses."),
                ]
            )
            sons[cid_l2] = ""
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, moment in moments.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(tr, pel, moment)
                by[f"{cid_l3}_F0001"] = fin(tr, pel, moment)
                sons[cid_l3] = {"matin": "oiseau", "sieste": "", "soir": "pain"}[moment]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-DIF-008",
        {
            "fil_rouge": (
                "Au marché, une goutte tombe du store. Raphaël veut jouer "
                "avec Mila près des jouets en bois. Il propose. Mila dit non, "
                "je regarde, ou plus tard. Il accepte plusieurs réponses."
            ),
            "title": "La goutte du store et le stand de Raphaël",
            "characters": "Raphaël, Mila, papa, maman",
            "setting": "marché du village, store rayé, stand de bois",
            "secondary_lessons": "DIF.COR.001",
        },
        by,
        sons,
        max_words=18,
        needles=("proposer", "accepter plusieurs réponses"),
    )


def story_009() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    pels = {"P0001": "Tom", "P0002": "Léa", "P0003": "Sami"}
    lieu_np = {
        "cuisine": "la cuisine du wagon",
        "jardin": "le jardin derrière la vitre",
        "chambre": "la petite chambre du siège",
    }
    jouet_np = {
        "ballon": "le ballon rouge",
        "seau": "le seau bleu",
        "doudou": "le doudou",
    }
    pel_np = {
        "Tom": "l'ours Tom",
        "Léa": "la poupée Léa",
        "Sami": "le lion Sami",
    }

    lieu_l1 = {
        "cuisine": [
            ("narrateur", "Amir ouvre la tablette, tout doux."),
            ("narrateur", "C'est la cuisine du wagon, tout petite."),
            ("narrateur", "Une brioche sent encore le beurre."),
            ("narrateur", "Nina est plus grande."),
            ("narrateur", "Elle tient le sac."),
            ("narrateur", "Amir est plus petit."),
            ("narrateur", "Il tient une miette."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "Viens jouer."),
            ("copine", "Oui."),
            ("papa", "Vous jouez ensemble."),
            ("maman", "Les tailles sont différentes."),
            ("maman", "On joue ensemble."),
            ("papa", "Bravo, Amir."),
            ("papa", "Tu as invité."),
            ("narrateur", "Nina casse la brioche, tout doux."),
            ("narrateur", "Amir prend un morceau, tout petit."),
            ("enfant-m", "Merci, Nina."),
            ("copine", "Merci, Amir."),
            ("narrateur", "Une miette brille sur la tablette."),
        ],
        "jardin": [
            ("narrateur", "Amir colle le nez à la vitre."),
            ("narrateur", "Derrière, un jardin défile, tout vert."),
            ("narrateur", "Un arbre passe."),
            ("narrateur", "Puis un autre."),
            ("narrateur", "Nina montre un champ, plus haut."),
            ("narrateur", "Amir montre une vache, plus bas."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "On joue au jardin ?"),
            ("copine", "Oui."),
            ("maman", "On joue ensemble."),
            ("papa", "Bravo."),
            ("papa", "Vous avez des tailles différentes."),
            ("papa", "Et vous jouez ensemble."),
            ("narrateur", "La vitre est tiède, un peu embuée."),
            ("narrateur", "Nina souffle un rond, tout petit."),
            ("enfant-m", "J'en fais un aussi."),
            ("maman", "Le corps n'est pas une blague."),
            ("maman", "On joue."),
        ],
        "chambre": [
            ("narrateur", "Amir plie le manteau bleu, sur le siège."),
            ("narrateur", "C'est une chambre, tout minuscule."),
            ("narrateur", "Nina pose le sac comme un oreiller."),
            ("narrateur", "Nina est plus grande."),
            ("narrateur", "Le sac est grand."),
            ("narrateur", "Amir est plus petit."),
            ("narrateur", "Il a le doudou."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "On joue à la chambre ?"),
            ("copine", "Oui."),
            ("papa", "On invite."),
            ("maman", "On joue ensemble."),
            ("papa", "Bravo, Amir."),
            ("narrateur", "Le manteau sent encore la pluie."),
            ("narrateur", "Nina baisse un peu le col."),
            ("enfant-m", "C'est doux."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Amir invite Nina."),
            ("papa", "On joue ensemble ?"),
        ],
        "jardin": [
            ("narrateur", "Les tailles sont différentes."),
            ("maman", "On fait quoi ?"),
        ],
        "chambre": [
            ("narrateur", "Amir a invité Nina."),
            ("papa", "On invite, et on joue ensemble ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("papa", "Oui."),
            ("papa", "On joue ensemble."),
            ("maman", "Les tailles sont différentes."),
            ("narrateur", "Amir souffle une miette."),
            ("enfant-m", "On joue."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "La brioche sent encore le beurre."),
        ],
        "jardin": [
            ("maman", "Oui."),
            ("maman", "On joue ensemble."),
            ("papa", "Les tailles sont différentes."),
            ("narrateur", "Amir touche le rond sur la vitre."),
            ("enfant-m", "Ensemble."),
            ("papa", "Bravo."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", "Une vache passe encore, tout loin."),
        ],
        "chambre": [
            ("papa", "Oui."),
            ("papa", "On invite."),
            ("papa", "On joue ensemble."),
            ("maman", "Les tailles sont différentes."),
            ("narrateur", "Amir caresse le manteau, tout doux."),
            ("enfant-m", "On joue."),
            ("maman", "Bravo, Amir."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Le sac fait un petit creux."),
        ],
    }

    jouet_scene = {
        "ballon": [
            ("narrateur", "Amir pose le ballon rouge sur la tablette."),
            ("narrateur", "Il est un peu trop grand, pour lui."),
            ("narrateur", "Nina le tient, tout doux."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "On le fait rouler ?"),
            ("copine", "Oui."),
            ("papa", "On joue ensemble."),
            ("maman", "Bravo."),
            ("narrateur", "Le ballon roule, tout lentement."),
        ],
        "seau": [
            ("narrateur", "Amir pose le seau bleu entre les sièges."),
            ("narrateur", "Nina tient l'anse, plus haut."),
            ("narrateur", "Amir tient le bord, plus bas."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "On range les miettes ?"),
            ("copine", "Oui."),
            ("maman", "Vous jouez ensemble."),
            ("papa", "On joue ensemble."),
            ("narrateur", "Le seau sonne, tout creux."),
        ],
        "doudou": [
            ("narrateur", "Amir pose le doudou sur les genoux."),
            ("narrateur", "Nina le caresse, tout doux."),
            ("narrateur", "Une oreille est froissée, un peu."),
            ("narrateur", "Les tailles sont différentes."),
            ("enfant-m", "Il vient avec nous."),
            ("copine", "Oui."),
            ("papa", "On joue ensemble."),
            ("maman", "On joue."),
            ("narrateur", "Le doudou sent encore la maison."),
        ],
    }

    extra_jouet = {
        ("cuisine", "ballon"): "Le ballon frôle la brioche, tout doux.",
        ("cuisine", "seau"): "Une miette tombe dans le seau bleu.",
        ("cuisine", "doudou"): "Le doudou a une miette sur l'oreille.",
        ("jardin", "ballon"): "Le ballon attrape un reflet de champ.",
        ("jardin", "seau"): "Le seau bleu se colle à la vitre tiède.",
        ("jardin", "doudou"): "Le doudou regarde les vaches, tout calme.",
        ("chambre", "ballon"): "Le ballon s'adosse au manteau bleu.",
        ("chambre", "seau"): "Le seau bleu sert de table, tout petit.",
        ("chambre", "doudou"): "Le doudou s'endort sur le sac.",
    }

    pel_scene = {
        "Tom": [
            ("narrateur", "Amir prend l'ours Tom."),
            ("narrateur", "Un ticket est glissé dans la poche."),
            ("narrateur", "L'oreille est rêche, puis douce."),
            ("enfant-m", "Tom vient jouer."),
            ("copine", "Oui."),
            ("papa", "Vous jouez ensemble."),
            ("maman", "Les tailles sont différentes."),
            ("papa", "Bravo, Amir."),
            ("narrateur", "L'ours Tom s'assoit contre le genou."),
        ],
        "Léa": [
            ("narrateur", "Amir prend la poupée Léa."),
            ("narrateur", "Elle a un foulard, tout minuscule."),
            ("narrateur", "Un bouton brille, comme la vitre."),
            ("enfant-m", "Léa vient avec nous."),
            ("copine", "Oui."),
            ("maman", "On joue ensemble."),
            ("papa", "Les tailles sont différentes."),
            ("maman", "Bravo."),
            ("narrateur", "La poupée Léa penche la tête."),
        ],
        "Sami": [
            ("narrateur", "Amir prend le lion Sami."),
            ("narrateur", "La crinière est en laine, un peu mêlée."),
            ("narrateur", "Un œil de bouton regarde les champs."),
            ("enfant-m", "Sami joue aussi."),
            ("copine", "Oui."),
            ("papa", "On joue ensemble."),
            ("maman", "Le corps n'est pas une blague."),
            ("maman", "On joue."),
            ("narrateur", "Le lion Sami chauffe contre la vitre."),
        ],
    }

    extras = {
        ("cuisine", "ballon", "Tom"): "L'ours Tom a le ballon trop grand.",
        ("cuisine", "ballon", "Léa"): "La poupée Léa tient le ballon, tout lourd.",
        ("cuisine", "ballon", "Sami"): "Le lion Sami garde le ballon entre les pattes.",
        ("cuisine", "seau", "Tom"): "L'ours Tom regarde une miette dans le seau.",
        ("cuisine", "seau", "Léa"): "La poupée Léa a une miette au foulard.",
        ("cuisine", "seau", "Sami"): "Le lion Sami lape une miette, tout doux.",
        ("cuisine", "doudou", "Tom"): "L'ours Tom se colle au doudou, près de la brioche.",
        ("cuisine", "doudou", "Léa"): "La poupée Léa s'assoit près du doudou.",
        ("cuisine", "doudou", "Sami"): "Le lion Sami pose la crinière sur le doudou.",
        ("jardin", "ballon", "Tom"): "L'ours Tom suit le champ, près du ballon.",
        ("jardin", "ballon", "Léa"): "La poupée Léa a le ballon contre la vitre.",
        ("jardin", "ballon", "Sami"): "Le lion Sami roule un peu, comme le ballon.",
        ("jardin", "seau", "Tom"): "L'ours Tom a l'oreille froide, près du seau.",
        ("jardin", "seau", "Léa"): "La poupée Léa voit une vache dans le seau.",
        ("jardin", "seau", "Sami"): "Le lion Sami écoute le seau, tout creux.",
        ("jardin", "doudou", "Tom"): "L'ours Tom et le doudou regardent le jardin.",
        ("jardin", "doudou", "Léa"): "La poupée Léa a le foulard comme le doudou.",
        ("jardin", "doudou", "Sami"): "Le lion Sami chauffe contre le doudou.",
        ("chambre", "ballon", "Tom"): "L'ours Tom s'adosse au manteau, près du ballon.",
        ("chambre", "ballon", "Léa"): "La poupée Léa a le ballon sur le sac.",
        ("chambre", "ballon", "Sami"): "Le lion Sami garde le ballon, tout calme.",
        ("chambre", "seau", "Tom"): "L'ours Tom a un ticket dans le seau.",
        ("chambre", "seau", "Léa"): "La poupée Léa tient le seau, trop lourd.",
        ("chambre", "seau", "Sami"): "Le lion Sami a la crinière dans le seau.",
        ("chambre", "doudou", "Tom"): "L'ours Tom et le doudou partagent le manteau.",
        ("chambre", "doudou", "Léa"): "La poupée Léa s'endort presque, près du doudou.",
        ("chambre", "doudou", "Sami"): "Le lion Sami écoute le wagon, près du doudou.",
    }

    fin_image = {
        "Tom": "L'ours Tom garde le ticket, tout calme.",
        "Léa": "La poupée Léa garde son foulard droit.",
        "Sami": "Le lion Sami a la crinière un peu plus sage.",
    }

    def l3(lieu: str, jouet: str, pel: str) -> list[tuple[str, str]]:
        return (
            pel_scene[pel]
            + sent(extras[(lieu, jouet, pel)])
            + [
                ("narrateur", f"Amir a encore {jouet_np[jouet]}."),
                ("narrateur", f"On est encore dans {lieu_np[lieu]}."),
                ("enfant-m", "On joue encore ?"),
                ("copine", "Oui."),
                ("papa", "On joue ensemble."),
                ("maman", "Les tailles sont différentes."),
                ("maman", "Le corps n'est pas une blague."),
                ("papa", "Bravo, Amir."),
                ("papa", "Tu as fait du bon travail."),
                ("enfant-m", "Merci, papa."),
                ("enfant-m", "Merci, maman."),
                ("narrateur", f"Amir range {pel_np[pel]}, tout doux."),
            ]
        )

    def fin(lieu: str, jouet: str, pel: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "On a joué ensemble."),
            ("copine", "Oui."),
            ("maman", "Bravo, Amir."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Amir a joué dans {lieu_np[lieu]}."),
            ("narrateur", f"Il a tenu {jouet_np[jouet]}."),
            ("narrateur", f"Il a parlé près de {pel_np[pel]}."),
            ("narrateur", fin_image[pel]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, dans le sac."),
            ("maman", "Le ballon rouge, le seau bleu, ou le doudou ?"),
            ("papa", "On invite."),
            ("papa", "On joue ensemble."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois peluches écoutent, sur le siège."),
            ("maman", "Tom, Léa, ou Sami ?"),
            ("papa", "Les tailles sont différentes."),
            ("papa", "On joue ensemble."),
            ("maman", "Le corps n'est pas une blague."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Les rails chantent sous le wagon."),
        ("narrateur", "Un tunnel avale la lumière."),
        ("narrateur", "Puis elle revient, toute claire."),
        ("narrateur", "Le filet à bagages tremble, tout bas."),
        ("narrateur", "Un manteau bleu pend, près de la porte."),
        ("narrateur", "Ça sent l'orange, tout doux."),
        ("narrateur", "Une peau repose sur la tablette."),
        ("narrateur", "Le siège pique un peu les genoux."),
        ("narrateur", "Un ticket dépasse de la poche de papa."),
        ("narrateur", "Dehors, des vaches passent, toutes lentes."),
        ("narrateur", "Maman plie un foulard bleu, sur ses genoux."),
        ("narrateur", "Nina a un sac, tout près."),
        ("narrateur", "Nina est plus grande."),
        ("narrateur", "Amir est plus petit."),
        ("narrateur", "Les tailles sont différentes."),
        ("papa", "Tu as vu les vaches, Amir ?"),
        ("enfant-m", "Oui, papa."),
        ("maman", "Le foulard est pour la gare."),
        ("narrateur", "En ce moment, Amir pose un doigt sur la tablette."),
        ("narrateur", "La tablette vibre, tout doux."),
        ("enfant-m", "Viens jouer."),
        ("copine", "Oui."),
        ("papa", "On joue ensemble, d'accord ?"),
        ("enfant-m", "D'accord."),
        ("maman", "Les tailles sont différentes."),
        ("maman", "Et on joue ensemble."),
    ]
    sons["CHK_T0000_P0000"] = ""

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Trois coins du wagon attendent."),
        ("papa", "La cuisine, le jardin, ou la chambre ?"),
        ("maman", "On invite."),
        ("maman", "On peut jouer ensemble."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = ""
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                jouet_scene[jouet]
                + sent(extra_jouet[(lieu, jouet)])
                + [
                    ("narrateur", f"On est encore dans {lieu_np[lieu]}."),
                    ("maman", "Les tailles sont différentes."),
                    ("maman", "On joue ensemble."),
                ]
            )
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
        "TREE-DIF-009",
        {
            "fil_rouge": (
                "Les rails chantent. Amir voyage avec papa et maman. "
                "Nina est plus grande. Ils jouent ensemble dans le wagon, "
                "malgré des tailles différentes."
            ),
            "title": "Les rails chantent, Amir et Nina jouent",
            "characters": "Amir, Nina, papa, maman",
            "setting": "wagon de train, champs et gare au loin",
            "secondary_lessons": "DIF.COR.002",
        },
        by,
        sons,
        max_words=16,
        needles=("tailles différentes", "jouer ensemble"),
    )


if __name__ == "__main__":
    story_008()
    story_009()
    print("ok TREE-DIF-008 TREE-DIF-009")
