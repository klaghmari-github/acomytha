#!/usr/bin/env python3
"""Génère merged.json pour TREE-DIF-010 et TREE-DIF-011 (texte seulement)."""
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
    "Maya",
    "Léa",
    "Lea",
    "Tom",
    "Sami",
)


SENT_SPLIT = re.compile(r"(?<=[.?!])\s+")


def flatten(lines: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for role, ph in lines:
        parts = [p.strip() for p in SENT_SPLIT.split(ph) if p.strip()]
        for p in parts:
            if not p.endswith((".", "?", "!")):
                p += "."
            out.append((role, p))
    return out


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    lines = flatten(lines)
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
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:60]))


def check_text(story_id: str, by: dict[str, list[tuple[str, str]]], extra_forbid: tuple[str, ...] = ()) -> None:
    blob = " ".join(ph for lines in by.values() for _, ph in lines)
    for s in FORBIDDEN_SUB:
        if s.lower() in blob.lower():
            raise SystemExit(f"{story_id} interdit: {s}")
    for name in FORBIDDEN_NAMES + extra_forbid:
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{story_id} nom interdit: {name}")


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str],
    max_words: int,
    extra_forbid: tuple[str, ...] = (),
    required: tuple[str, ...] = (),
) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    src_ids = [c["chunk_id"] for c in source["chunks"]]
    missing = [cid for cid in src_ids if cid not in by_id]
    extra = [k for k in by_id if k not in set(src_ids)]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:8]} extra={extra[:8]}")
    by_id = {cid: flatten(lines) for cid, lines in by_id.items()}
    check_phrases(story_id, by_id, max_words)
    check_text(story_id, by_id, extra_forbid)
    blob = " ".join(ph for lines in by_id.values() for _, ph in lines).lower()
    for req in required:
        if req.lower() not in blob:
            raise SystemExit(f"{story_id} leçon absente: {req}")
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


def story_010() -> None:
    lieux = {"P0001": "bac", "P0002": "toboggan", "P0003": "balancoires"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    couleurs = {"P0001": "rouge", "P0002": "bleu", "P0003": "vert"}
    lieu_np = {
        "bac": "le bac à sable",
        "toboggan": "le toboggan",
        "balancoires": "les balançoires",
    }
    jouet_np = {
        "cubes": "les cubes",
        "livre": "le livre",
        "dinette": "la dînette",
    }
    coul_np = {"rouge": "le rouge", "bleu": "le bleu", "vert": "le vert"}

    lecon = [
        ("maman", "Cette énergie n'est pas une faute."),
        ("papa", "On peut jouer ou attendre."),
        ("papa", "On peut demander à un adulte."),
    ]

    lieu_l1 = {
        "bac": [
            ("narrateur", "Sarah s'agenouille près du bac à sable."),
            ("narrateur", "Le sable est tiède, un peu rêche."),
            ("narrateur", "Un grain colle à son genou."),
            ("narrateur", "Raphaël court, saute, creuse."),
            ("narrateur", "Le sable vole, tout léger."),
            ("narrateur", "Il a beaucoup d'énergie."),
            ("enfant-f", "Il saute, maman."),
            ("maman", "Cette énergie n'est pas une faute."),
            ("papa", "On peut jouer ou attendre."),
            ("narrateur", "Sarah souffle un peu."),
            ("enfant-f", "On creuse ensemble ?"),
            ("copain", "Oui !"),
            ("copain", "Un grand trou !"),
            ("narrateur", "Raphaël creuse très vite."),
            ("narrateur", "Sarah attend une seconde."),
            ("narrateur", "Puis elle pose sa pelle, tout doux."),
            ("maman", "Bravo, Sarah."),
            ("maman", "Tu as pu attendre."),
            ("papa", "On peut demander, aussi."),
            ("enfant-f", "Papa, on joue ?"),
            ("papa", "Oui."),
            ("papa", "Chacun son tour."),
            ("narrateur", "Le trou devient rond, tout petit."),
            ("narrateur", "Une coquille blanche brille au fond."),
        ],
        "toboggan": [
            ("narrateur", "Sarah pose la main sur le toboggan."),
            ("narrateur", "Le bois est chaud, un peu lisse."),
            ("narrateur", "Une marche sonne, tout creux."),
            ("narrateur", "Raphaël monte, descend, recommence."),
            ("narrateur", "Il a beaucoup d'énergie."),
            ("enfant-f", "Encore, papa."),
            ("papa", "Cette énergie n'est pas une faute."),
            ("maman", "On peut jouer ou attendre."),
            ("narrateur", "Sarah reste en bas, un moment."),
            ("enfant-f", "J'attends mon tour."),
            ("maman", "Bravo."),
            ("maman", "Tu as attendu."),
            ("narrateur", "Raphaël arrive, tout vite."),
            ("narrateur", "Il souffle. Il rit."),
            ("copain", "À toi !"),
            ("narrateur", "Sarah monte, tout doux."),
            ("narrateur", "Le vent sent le sel, sur la joue."),
            ("papa", "On peut demander à un adulte."),
            ("enfant-f", "Tu me regardes, papa ?"),
            ("papa", "Oui."),
            ("papa", "Je te vois."),
            ("narrateur", "Sarah glisse. Le bois est tiède."),
            ("narrateur", "Raphaël attend, un tout petit peu."),
        ],
        "balancoires": [
            ("narrateur", "Sarah s'approche des balançoires."),
            ("narrateur", "La chaîne est froide, un peu sablée."),
            ("narrateur", "Elle fait un tout petit criiii."),
            ("narrateur", "Raphaël pousse fort, puis rit."),
            ("narrateur", "Il a beaucoup d'énergie."),
            ("enfant-f", "Il va haut, maman."),
            ("maman", "Cette énergie n'est pas une faute."),
            ("papa", "On peut jouer ou attendre."),
            ("papa", "On peut demander à un adulte."),
            ("narrateur", "Sarah pose les deux pieds au sol."),
            ("enfant-f", "Papa, je m'assois à côté ?"),
            ("papa", "Oui."),
            ("papa", "Doucement, comme ça."),
            ("narrateur", "Sarah s'assoit. La planche est chaude."),
            ("copain", "On se balance !"),
            ("narrateur", "Raphaël va vite. Sarah va lentement."),
            ("maman", "Chacun son rythme."),
            ("maman", "On peut jouer ensemble."),
            ("enfant-f", "D'accord."),
            ("papa", "Bravo, Sarah."),
            ("papa", "Tu as demandé."),
            ("narrateur", "Une mouette passe, tout loin."),
            ("narrateur", "La chaîne chante encore, tout bas."),
        ],
    }

    q = {
        "bac": [
            ("narrateur", "Raphaël a de l'énergie."),
            ("maman", "C'est une faute ?"),
        ],
        "toboggan": [
            ("narrateur", "Raphaël recommence."),
            ("papa", "On joue, ou on attend ?"),
        ],
        "balancoires": [
            ("narrateur", "Sarah veut s'asseoir."),
            ("maman", "On demande à un adulte ?"),
        ],
    }

    conf = {
        "bac": [
            ("papa", "Oui."),
            ("papa", "Cette énergie n'est pas une faute."),
            ("maman", "On peut jouer ou attendre."),
            ("narrateur", "Sarah respire. Le sable est tiède."),
            ("enfant-f", "On creuse, un peu."),
            ("copain", "Oui."),
            ("papa", "Bravo, Sarah."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", "La coquille blanche reste au fond."),
        ],
        "toboggan": [
            ("maman", "Oui."),
            ("maman", "On peut jouer ou attendre."),
            ("papa", "Cette énergie n'est pas une faute."),
            ("narrateur", "Sarah retient le geste, tout doux."),
            ("enfant-f", "J'attends."),
            ("copain", "Après, c'est toi."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Le bois du toboggan reste chaud."),
        ],
        "balancoires": [
            ("papa", "Oui."),
            ("papa", "On peut demander à un adulte."),
            ("maman", "Cette énergie n'est pas une faute."),
            ("maman", "On peut jouer ou attendre."),
            ("narrateur", "Sarah hoche la tête."),
            ("enfant-f", "Merci, papa."),
            ("papa", "Bravo."),
            ("papa", "Tu as demandé."),
            ("narrateur", "La chaîne se tait, un moment."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Sarah sort les cubes de bois."),
            ("narrateur", "Un cube sent le pin, un peu."),
            ("narrateur", "Raphaël pose trois cubes, très vite."),
            ("narrateur", "La tour penche. Il recommence."),
            ("enfant-f", "On attend, un peu ?"),
            ("copain", "Encore !"),
            ("maman", "Cette énergie n'est pas une faute."),
            ("papa", "On peut jouer ou attendre."),
            ("narrateur", "Sarah pose un cube, tout droit."),
            ("narrateur", "Raphaël souffle. Il attend."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "Tu as attendu."),
            ("enfant-f", "C'est ton tour."),
        ],
        "livre": [
            ("narrateur", "Sarah ouvre le livre."),
            ("narrateur", "La page sent le papier, un peu sec."),
            ("narrateur", "Raphaël tourne deux pages, trop vite."),
            ("narrateur", "Puis il s'assoit. Il regarde."),
            ("enfant-f", "On lit ensemble ?"),
            ("copain", "Oui."),
            ("maman", "Cette énergie n'est pas une faute."),
            ("papa", "On peut jouer ou attendre."),
            ("narrateur", "Sarah montre un bateau, tout bleu."),
            ("maman", "On tourne une page, puis on attend."),
            ("enfant-f", "D'accord."),
            ("papa", "Bravo."),
            ("papa", "Vous lisez, chacun son tour."),
        ],
        "dinette": [
            ("narrateur", "Sarah sort la dînette."),
            ("narrateur", "Une petite assiette sonne, tout creux."),
            ("narrateur", "Raphaël sert très vite, trop vite."),
            ("narrateur", "L'eau imaginaire déborde, un peu."),
            ("enfant-f", "Maman, on fait comment ?"),
            ("maman", "On peut jouer ou attendre."),
            ("papa", "Cette énergie n'est pas une faute."),
            ("narrateur", "Sarah pose la tasse, tout doux."),
            ("copain", "Encore du thé ?"),
            ("enfant-f", "Après toi."),
            ("papa", "Bravo, Sarah."),
            ("papa", "Tu as attendu."),
            ("narrateur", "Une petite cuillère brille au soleil."),
        ],
    }

    extra_l2 = {
        ("bac", "cubes"): "Un cube rouge garde un grain de sable.",
        ("bac", "livre"): "Le sable poudre un coin de la page.",
        ("bac", "dinette"): "Une tasse miniature a du sable au bord.",
        ("toboggan", "cubes"): "Un cube tapote la marche du toboggan.",
        ("toboggan", "livre"): "Le vent tourne une page, tout seul.",
        ("toboggan", "dinette"): "La petite casserole est au pied du toboggan.",
        ("balancoires", "cubes"): "Un cube repose près de la chaîne.",
        ("balancoires", "livre"): "Le livre est ouvert, sous la balançoire.",
        ("balancoires", "dinette"): "Une cuillère miniature tinte près du pied.",
    }

    extra_l3 = {
        ("bac", "cubes", "rouge"): "Sarah pose le cube rouge dans le trou. Il reste droit.",
        ("bac", "cubes", "bleu"): "Le cube bleu a une goutte. Sarah attend. Raphaël pose le sien.",
        ("bac", "cubes", "vert"): "Un brin d'algue colle au cube vert. Ils rient, tout doux.",
        ("bac", "livre", "rouge"): "Sur la page, un crabe rouge. Raphaël montre, puis attend.",
        ("bac", "livre", "bleu"): "La mer du livre est bleue. Sarah tourne, tout lentement.",
        ("bac", "livre", "vert"): "Un bateau vert est dessiné. Ils le regardent, ensemble.",
        ("bac", "dinette", "rouge"): "Sarah sert dans la tasse rouge. Raphaël attend sa gorgée.",
        ("bac", "dinette", "bleu"): "L'assiette bleue sent le sel. Ils font un pique-nique.",
        ("bac", "dinette", "vert"): "La cuillère verte a du sable. Sarah l'essuie, tout doux.",
        ("toboggan", "cubes", "rouge"): "Le cube rouge attend en bas. Raphaël glisse, puis le pose.",
        ("toboggan", "cubes", "bleu"): "Sarah garde le cube bleu. Elle attend son tour, en haut.",
        ("toboggan", "cubes", "vert"): "Le cube vert roule d'une marche. Ils le ramassent, ensemble.",
        ("toboggan", "livre", "rouge"): "La couverture rouge est chaude. Ils lisent après la glissade.",
        ("toboggan", "livre", "bleu"): "Une vague bleue est sur la page. Sarah montre. Raphaël écoute.",
        ("toboggan", "livre", "vert"): "Une île verte est dessinée. Ils soufflent, puis lisent.",
        ("toboggan", "dinette", "rouge"): "La tasse rouge est au pied. Après la glissade, on sert.",
        ("toboggan", "dinette", "bleu"): "L'assiette bleue est tiède. Sarah attend. Raphaël s'assoit.",
        ("toboggan", "dinette", "vert"): "La cuillère verte tinte. Ils font la soupe, tout calmes.",
        ("balancoires", "cubes", "rouge"): "Sarah tient le cube rouge. La balançoire s'arrête. On pose.",
        ("balancoires", "cubes", "bleu"): "Le cube bleu est dans sa poche. Raphaël attend, les pieds au sol.",
        ("balancoires", "cubes", "vert"): "Le cube vert brille. Ils le posent entre les deux sièges.",
        ("balancoires", "livre", "rouge"): "Le livre rouge est sur les genoux. On se balance, tout lent.",
        ("balancoires", "livre", "bleu"): "La page bleue claque un peu. Sarah attend. Raphaël écoute.",
        ("balancoires", "livre", "vert"): "Une feuille verte est collée. Ils la gardent, comme un secret.",
        ("balancoires", "dinette", "rouge"): "La tasse rouge est dans l'herbe. Après, on sert, tout doux.",
        ("balancoires", "dinette", "bleu"): "L'assiette bleue reste près des pieds. Raphaël souffle, puis attend.",
        ("balancoires", "dinette", "vert"): "La cuillère verte est tiède. Sarah demande. Papa dit oui.",
    }

    coul_obj = {
        ("cubes", "rouge"): "le cube rouge",
        ("cubes", "bleu"): "le cube bleu",
        ("cubes", "vert"): "le cube vert",
        ("livre", "rouge"): "la page rouge",
        ("livre", "bleu"): "la page bleue",
        ("livre", "vert"): "la page verte",
        ("dinette", "rouge"): "la tasse rouge",
        ("dinette", "bleu"): "l'assiette bleue",
        ("dinette", "vert"): "la cuillère verte",
    }

    fin_image = {
        "bac": "La coquille blanche brille encore, au fond du trou.",
        "toboggan": "Le bois du toboggan reste chaud, tout calme.",
        "balancoires": "La chaîne des balançoires se tait, tout loin.",
    }

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout proches."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On peut jouer ou attendre."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Une couleur attend, maintenant."),
            ("papa", "Rouge, bleu, ou vert ?"),
            ("maman", "Cette énergie n'est pas une faute."),
        ]

    def l2(lieu: str, jouet: str) -> list[tuple[str, str]]:
        extra = extra_l2[(lieu, jouet)]
        extra_ph = extra if extra.endswith((".", "?", "!")) else extra + "."
        return jouet_scene[jouet] + [
            ("narrateur", extra_ph),
            ("narrateur", f"On est encore près de {lieu_np[lieu]}."),
            ("maman", "On peut jouer ensemble."),
        ]

    def l3(lieu: str, jouet: str, coul: str) -> list[tuple[str, str]]:
        extra = extra_l3[(lieu, jouet, coul)]
        extra_ph = extra if extra.endswith((".", "?", "!")) else extra + "."
        obj = coul_obj[(jouet, coul)]
        return [
            ("narrateur", f"Sarah a choisi {coul}."),
            ("narrateur", f"Elle a encore {jouet_np[jouet]}."),
            ("narrateur", f"On est près de {lieu_np[lieu]}."),
            ("narrateur", extra_ph),
            ("narrateur", f"Elle pose {obj}, tout doux."),
            ("narrateur", "Raphaël a encore de l'énergie."),
            ("enfant-f", "On attend, un peu ?"),
            ("copain", "D'accord."),
            ("maman", "Cette énergie n'est pas une faute."),
            ("papa", "On peut jouer ou attendre."),
            ("papa", "On peut demander à un adulte."),
            ("enfant-f", "Merci, maman."),
            ("maman", "Bravo, Sarah."),
            ("maman", "Tu as su attendre."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Ils jouent encore, un tout petit peu."),
        ]

    def fin(lieu: str, jouet: str, coul: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "On a joué."),
            ("enfant-f", "On a attendu."),
            ("maman", "Bravo, Sarah."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Sarah a vécu {lieu_np[lieu]}, avec {jouet_np[jouet]}."),
            ("narrateur", f"Elle a choisi {coul_np[coul]}."),
            ("narrateur", "Raphaël a eu de l'énergie. Ce n'était pas une faute."),
            ("narrateur", fin_image[lieu]),
            ("narrateur", "L'histoire est finie."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le chapeau de paille sèche sur la rampe."),
        ("narrateur", "Une goutte de sel glisse, toute lente."),
        ("narrateur", "Elle fait ploc sur le bois."),
        ("narrateur", "Loin, une mouette crie, tout bas."),
        ("narrateur", "La maison sent le linge chaud."),
        ("narrateur", "Papa déplie une serviette rayée."),
        ("narrateur", "Du sable colle déjà dans les chaussures."),
        ("narrateur", "Maman verse de l'eau, dans une bouteille bleue."),
        ("papa", "Tu sens le sel, Sarah ?"),
        ("enfant-f", "Oui."),
        ("enfant-f", "Ça pique un peu."),
        ("maman", "Les chaussures sont encore mouillées."),
        ("narrateur", "Raphaël saute sur le chemin de sable."),
        ("narrateur", "Ses pieds font toc, toc, toc."),
        ("narrateur", "En ce moment, Sarah regarde le jeu, près de la mer."),
        ("narrateur", "Un bac à sable. Un toboggan. Des balançoires."),
        ("enfant-f", "Il court, papa."),
        ("papa", "Raphaël a beaucoup d'énergie."),
        ("maman", "Cette énergie n'est pas une faute."),
        ("papa", "On peut jouer ou attendre."),
        ("papa", "On peut demander à un adulte."),
        ("enfant-f", "On va où ?"),
        ("maman", "Tu choisis, Sarah."),
        ("narrateur", "La serviette rayée claque un peu, au vent."),
        ("narrateur", "Le chapeau de paille sèche encore."),
    ]
    sons["CHK_T0000_P0000"] = "oiseau,vague"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Trois coins du jeu attendent, près de la mer."),
        ("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ("maman", "On peut jouer ou attendre."),
    ]
    sons["CHK_T0001_P0000"] = ""

    sons_l1 = {"bac": "sable", "toboggan": "", "balancoires": ""}
    sons_j = {"cubes": "cubes", "livre": "page", "dinette": "assiette"}

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = sons_l1[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = l2(lieu, jouet)
            sons[cid_l2] = sons_j[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, coul in couleurs.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, coul)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, coul)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-DIF-010",
        {
            "fil_rouge": (
                "Le chapeau de paille sèche sur la rampe. Sarah voit Raphaël "
                "sauter près de la mer. Cette énergie n'est pas une faute. "
                "On peut jouer ou attendre. On peut demander à papa ou maman."
            ),
            "title": "Le chapeau de paille et Raphaël qui saute",
            "characters": "Sarah, Raphaël, papa, maman",
            "setting": "maison de bois au bord de la mer, puis le jeu sur le sable",
        },
        by,
        sons,
        max_words=18,
        extra_forbid=("Nina", "Mila", "Amir", "Nino", "Victorina", "Victorino", "Chouchou", "Aniss"),
        required=("énergie", "pas une faute", "jouer ou attendre"),
    )


def story_011() -> None:
    lieux = {"P0001": "sable", "P0002": "galets", "P0003": "ombre"}
    jouets = {"P0001": "seau", "P0002": "filet", "P0003": "livre"}
    reponses = {"P0001": "regarder", "P0002": "plus_tard", "P0003": "non"}
    lieu_np = {
        "sable": "le sable",
        "galets": "les galets",
        "ombre": "l'ombre",
    }
    jouet_np = {
        "seau": "le seau",
        "filet": "le filet",
        "livre": "le livre",
    }
    rep_np = {
        "regarder": "regarder",
        "plus_tard": "plus tard",
        "non": "un non",
    }

    lieu_l1 = {
        "sable": [
            ("narrateur", "Nina s'agenouille sur le sable chaud."),
            ("narrateur", "Le sable colle aux genoux, tout fin."),
            ("narrateur", "Une petite colline attend sa main."),
            ("narrateur", "Amir est là, un peu plus loin."),
            ("narrateur", "Il regarde l'eau, tout calme."),
            ("enfant-f", "Tu viens, Amir ?"),
            ("enfant-f", "On fait un château ?"),
            ("copain", "Je regarde."),
            ("narrateur", "Nina tourne les yeux vers maman."),
            ("maman", "On peut proposer."),
            ("maman", "On propose."),
            ("maman", "On accepte plusieurs réponses."),
            ("papa", "Oui."),
            ("papa", "Regarder."),
            ("papa", "Plus tard."),
            ("papa", "Ou non."),
            ("enfant-f", "D'accord."),
            ("narrateur", "Nina laisse une place, tout près."),
            ("narrateur", "Elle pousse le sable, tout doux."),
            ("maman", "Regarder, c'est une réponse."),
            ("papa", "Un non est possible, aussi."),
            ("narrateur", "Amir s'assoit. Il regarde encore."),
            ("narrateur", "Le château a une tour, toute petite."),
        ],
        "galets": [
            ("narrateur", "Nina s'approche des galets."),
            ("narrateur", "Ils sont lisses, un peu froids."),
            ("narrateur", "Un galet gris a une ligne blanche."),
            ("narrateur", "Amir touche un galet, tout seul."),
            ("enfant-f", "On fait une file, Amir ?"),
            ("copain", "Plus tard."),
            ("narrateur", "Nina hoche la tête."),
            ("maman", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("maman", "Plus tard, c'est une réponse."),
            ("enfant-f", "D'accord."),
            ("enfant-f", "Je commence, toute seule."),
            ("narrateur", "Elle pose le galet gris, tout droit."),
            ("narrateur", "Amir reste près de l'eau."),
            ("papa", "Tu as accepté, Nina."),
            ("papa", "C'est bien."),
            ("narrateur", "La file de galets grandit, tout lentement."),
            ("narrateur", "L'eau vient, puis recule."),
            ("maman", "Un non est possible."),
            ("enfant-f", "Oui, maman."),
        ],
        "ombre": [
            ("narrateur", "Nina rejoint l'ombre du parasol."),
            ("narrateur", "Le rond est frais, tout calme."),
            ("narrateur", "La toile jaune bouge un peu."),
            ("narrateur", "Amir est au bord de l'ombre."),
            ("enfant-f", "Tu viens t'asseoir, Amir ?"),
            ("copain", "Non."),
            ("narrateur", "Nina reste un moment, sans bouger."),
            ("maman", "On peut proposer."),
            ("maman", "On propose."),
            ("maman", "On accepte plusieurs réponses."),
            ("papa", "Un non est possible."),
            ("enfant-f", "D'accord, Amir."),
            ("narrateur", "Elle s'assoit dans le rond frais."),
            ("narrateur", "Amir reste au soleil, tout près."),
            ("papa", "Tu as accepté le non."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as fait du bon travail."),
            ("narrateur", "Une mouche passe, tout bas."),
            ("narrateur", "La toile jaune fait un petit bruit."),
        ],
    }

    q = {
        "sable": [
            ("narrateur", "Nina invite Amir."),
            ("papa", "S'il dit non ?"),
        ],
        "galets": [
            ("narrateur", "Nina a proposé."),
            ("maman", "Si Amir dit non ?"),
        ],
        "ombre": [
            ("narrateur", "Amir a dit non."),
            ("papa", "Nina fait quoi ?"),
        ],
    }

    conf = {
        "sable": [
            ("maman", "Oui."),
            ("maman", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("papa", "Un non est possible."),
            ("narrateur", "Nina souffle. Le sable est chaud."),
            ("enfant-f", "D'accord."),
            ("maman", "Bravo, Nina."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "La petite tour reste droite."),
        ],
        "galets": [
            ("papa", "Oui."),
            ("papa", "On accepte plusieurs réponses."),
            ("maman", "Plus tard, ou non, c'est possible."),
            ("narrateur", "Nina respire. Le galet est froid."),
            ("enfant-f", "J'ai accepté."),
            ("maman", "Bravo."),
            ("papa", "Tu as proposé, tout doux."),
            ("narrateur", "La ligne blanche brille encore."),
        ],
        "ombre": [
            ("maman", "Oui."),
            ("maman", "Nina accepte le non."),
            ("papa", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("narrateur", "Nina donne la main à maman, un instant."),
            ("enfant-f", "D'accord."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Le rond d'ombre reste frais."),
        ],
    }

    jouet_scene = {
        "seau": [
            ("narrateur", "Nina prend le seau rouge."),
            ("narrateur", "Le plastique est chaud, un peu rêche."),
            ("narrateur", "Du sable tombe, tout fin."),
            ("enfant-f", "Tu veux le seau, Amir ?"),
            ("maman", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("narrateur", "Nina attend la réponse, tout calme."),
            ("narrateur", "Elle remplit le seau, tout doux."),
            ("maman", "Un non est possible."),
            ("enfant-f", "D'accord."),
            ("papa", "Bravo."),
            ("papa", "Tu as attendu la réponse."),
        ],
        "filet": [
            ("narrateur", "Nina prend le filet souple."),
            ("narrateur", "Les mailles sentent le sel, un peu."),
            ("narrateur", "Le vent le fait bouger."),
            ("enfant-f", "On cherche un crabe, Amir ?"),
            ("maman", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("narrateur", "Nina tient le filet, sans forcer."),
            ("maman", "Regarder, c'est une réponse."),
            ("enfant-f", "Oui."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as proposé, tout doux."),
            ("narrateur", "Une goutte perle au bout du filet."),
        ],
        "livre": [
            ("narrateur", "Nina ouvre le livre."),
            ("narrateur", "Un coin de page est encore mouillé."),
            ("narrateur", "Un crabe est dessiné, tout rouge."),
            ("enfant-f", "On lit, Amir ?"),
            ("maman", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("narrateur", "Nina laisse le livre ouvert, entre eux."),
            ("maman", "Plus tard, c'est une réponse."),
            ("papa", "Un non est possible."),
            ("enfant-f", "D'accord."),
            ("papa", "Bravo."),
            ("narrateur", "La page claque un peu, au vent."),
        ],
    }

    extra_l2 = {
        ("sable", "seau"): "Le seau laisse un rond, dans le sable chaud.",
        ("sable", "filet"): "Le filet traîne une ligne, sur le sable.",
        ("sable", "livre"): "Le livre a du sable, dans le pli.",
        ("galets", "seau"): "Un galet sonne, contre le seau.",
        ("galets", "filet"): "Le filet accroche un galet lisse.",
        ("galets", "livre"): "Un galet plat sert de marque-page.",
        ("ombre", "seau"): "Le seau est à l'ombre, tout frais.",
        ("ombre", "filet"): "Le filet sèche dans le rond jaune.",
        ("ombre", "livre"): "La page reste à l'ombre, tout calme.",
    }

    extra_l3 = {
        ("sable", "seau", "regarder"): "Amir regarde le seau. Nina continue le château.",
        ("sable", "seau", "plus_tard"): "Amir dit plus tard. Nina pose le seau, et attend.",
        ("sable", "seau", "non"): "Amir dit non. Nina garde le seau. Elle accepte.",
        ("sable", "filet", "regarder"): "Amir regarde le filet. Nina le traîne, tout doux.",
        ("sable", "filet", "plus_tard"): "Amir dit plus tard. Nina range le filet, un moment.",
        ("sable", "filet", "non"): "Amir dit non. Nina pose le filet. C'est d'accord.",
        ("sable", "livre", "regarder"): "Amir regarde la page. Nina lit tout bas, pour elle.",
        ("sable", "livre", "plus_tard"): "Amir dit plus tard. Nina ferme le livre, tout calme.",
        ("sable", "livre", "non"): "Amir dit non. Nina accepte. Le livre reste ouvert.",
        ("galets", "seau", "regarder"): "Amir regarde le seau, près des galets. Nina verse.",
        ("galets", "seau", "plus_tard"): "Amir dit plus tard. Nina pose le seau sur un galet.",
        ("galets", "seau", "non"): "Amir dit non. Nina sourit un peu. Elle accepte.",
        ("galets", "filet", "regarder"): "Amir regarde le filet. Un galet brille dedans.",
        ("galets", "filet", "plus_tard"): "Amir dit plus tard. Nina laisse le filet au sec.",
        ("galets", "filet", "non"): "Amir dit non. Nina pose le filet. Les galets restent.",
        ("galets", "livre", "regarder"): "Amir regarde le livre. Nina montre le galet dessiné.",
        ("galets", "livre", "plus_tard"): "Amir dit plus tard. Nina pose le livre sur un galet.",
        ("galets", "livre", "non"): "Amir dit non. Nina accepte. La page reste au vent.",
        ("ombre", "seau", "regarder"): "Amir regarde le seau, depuis le soleil. Nina reste à l'ombre.",
        ("ombre", "seau", "plus_tard"): "Amir dit plus tard. Nina pose le seau dans le rond frais.",
        ("ombre", "seau", "non"): "Amir dit non. Nina accepte, sous le parasol jaune.",
        ("ombre", "filet", "regarder"): "Amir regarde le filet sécher. Nina le laisse.",
        ("ombre", "filet", "plus_tard"): "Amir dit plus tard. Nina plie le filet, tout doux.",
        ("ombre", "filet", "non"): "Amir dit non. Nina pose le filet. L'ombre reste fraîche.",
        ("ombre", "livre", "regarder"): "Amir regarde la page, de loin. Nina lit dans l'ombre.",
        ("ombre", "livre", "plus_tard"): "Amir dit plus tard. Nina garde le livre sur les genoux.",
        ("ombre", "livre", "non"): "Amir dit non. Nina accepte. Le livre reste à l'ombre.",
    }

    par_amir = {
        "regarder": ("copain", "Je regarde."),
        "plus_tard": ("copain", "Plus tard."),
        "non": ("copain", "Non."),
    }

    acc_nina = {
        "regarder": ("enfant-f", "D'accord. Tu regardes."),
        "plus_tard": ("enfant-f", "D'accord. Plus tard."),
        "non": ("enfant-f", "D'accord. C'est non."),
    }

    fin_image = {
        "sable": "La petite tour de sable reste chaude, au soleil.",
        "galets": "Le galet gris garde sa ligne blanche.",
        "ombre": "Le parasol jaune fait encore un rond frais.",
    }

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois objets attendent, tout proches."),
            ("maman", "Le seau, le filet, ou le livre ?"),
            ("papa", "On propose."),
            ("papa", "On accepte."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Amir peut répondre, maintenant."),
            ("papa", "Regarder, plus tard, ou un non ?"),
            ("maman", "On accepte plusieurs réponses."),
        ]

    def l2(lieu: str, jouet: str) -> list[tuple[str, str]]:
        extra = extra_l2[(lieu, jouet)]
        extra_ph = extra if extra.endswith((".", "?", "!")) else extra + "."
        return jouet_scene[jouet] + [
            ("narrateur", extra_ph),
            ("narrateur", f"On est encore près de {lieu_np[lieu]}."),
            ("maman", "Un non est possible."),
        ]

    def l3(lieu: str, jouet: str, rep: str) -> list[tuple[str, str]]:
        extra = extra_l3[(lieu, jouet, rep)]
        extra_ph = extra if extra.endswith((".", "?", "!")) else extra + "."
        return [
            ("narrateur", f"Nina a encore {jouet_np[jouet]}."),
            ("narrateur", f"On est près de {lieu_np[lieu]}."),
            ("enfant-f", "Tu viens, Amir ?"),
            par_amir[rep],
            ("narrateur", extra_ph),
            acc_nina[rep],
            ("maman", "On propose."),
            ("papa", "On accepte plusieurs réponses."),
            ("maman", "Un non est possible."),
            ("papa", "Regarder, c'est une réponse."),
            ("papa", "Plus tard, aussi."),
            ("enfant-f", "Merci, maman."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as accepté."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Nina continue, tout doux, sans forcer."),
        ]

    def fin(lieu: str, jouet: str, rep: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "J'ai proposé."),
            ("enfant-f", "J'ai accepté."),
            ("maman", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Nina a vécu {lieu_np[lieu]}, avec {jouet_np[jouet]}."),
            ("narrateur", f"Amir a choisi {rep_np[rep]}."),
            ("narrateur", "Nina a accepté plusieurs réponses."),
            ("narrateur", fin_image[lieu]),
            ("narrateur", "L'histoire est finie."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le parasol jaune fait un rond d'ombre."),
        ("narrateur", "Une coquille de crabe attend dans une flaque."),
        ("narrateur", "L'eau de la flaque est tiède, tout calme."),
        ("narrateur", "La mer chuchote, tout bas."),
        ("narrateur", "Un coin du livre est encore mouillé."),
        ("narrateur", "Papa s'assoit sur une chaise pliante."),
        ("narrateur", "La toile craque, un tout petit peu."),
        ("narrateur", "Maman déplie une serviette à carreaux."),
        ("papa", "Tu entends la mer, Nina ?"),
        ("enfant-f", "Oui."),
        ("enfant-f", "Elle chuchote."),
        ("maman", "La flaque est tiède, aujourd'hui."),
        ("narrateur", "Amir est près de l'eau, tout calme."),
        ("narrateur", "Ses pieds laissent des ronds, dans le sable."),
        ("narrateur", "En ce moment, Nina a envie de jouer avec lui."),
        ("enfant-f", "Je peux proposer, maman ?"),
        ("maman", "Oui."),
        ("maman", "On peut proposer."),
        ("maman", "On propose."),
        ("papa", "On peut accepter plusieurs réponses."),
        ("papa", "On accepte plusieurs réponses."),
        ("papa", "Oui."),
        ("papa", "Regarder."),
        ("papa", "Plus tard."),
        ("papa", "Ou non."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Le parasol jaune bouge un peu, au vent."),
        ("narrateur", "La coquille reste dans la flaque tiède."),
    ]
    sons["CHK_T0000_P0000"] = "vague,oiseau"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Trois coins de la plage attendent."),
        ("papa", "Le sable, les galets, ou l'ombre ?"),
        ("maman", "On propose."),
        ("maman", "On accepte."),
    ]
    sons["CHK_T0001_P0000"] = ""

    sons_l1 = {"sable": "sable", "galets": "", "ombre": "toile"}
    sons_j = {"seau": "seau", "filet": "", "livre": "page"}

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = sons_l1[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = l2(lieu, jouet)
            sons[cid_l2] = sons_j[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, rep in reponses.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, rep)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, rep)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-DIF-011",
        {
            "fil_rouge": (
                "Sous le parasol jaune, Nina veut jouer avec Amir. "
                "Elle propose. Amir peut dire oui, regarder, plus tard, ou non. "
                "Nina accepte plusieurs réponses."
            ),
            "title": "Le parasol jaune et la réponse d'Amir",
            "characters": "Nina, Amir, papa, maman",
            "setting": "plage sous un parasol jaune, sable, galets, ombre",
        },
        by,
        sons,
        max_words=15,
        extra_forbid=("Sarah", "Raphaël", "Mila", "Nino", "Victorina", "Victorino", "Chouchou", "Aniss"),
        required=("proposer", "accepte plusieurs réponses"),
    )


if __name__ == "__main__":
    story_010()
    story_011()
    print("ok TREE-DIF-010 TREE-DIF-011")
