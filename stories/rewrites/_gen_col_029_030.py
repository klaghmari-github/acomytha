#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-029 et TREE-COL-030 (texte seulement)."""
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
    "maman sourit",
)
FORBIDDEN_NAMES = (
    "Adam",
    "Iris",
    "Léa",
    "Lea",
    "Tom",
    "Sami",
    "Lina",
    "Lila",
    "Lucas",
    "Céline",
    "Celine",
    "Luca",
    "Sara",
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
            if role not in ("narrateur", "papa", "maman", "enfant-m", "enfant-f", "maitresse"):
                bad.append(f"{cid} role {role}")
    if bad:
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:50]))


def check_text(story_id: str, by: dict[str, list[tuple[str, str]]]) -> None:
    blob = " ".join(ph for lines in by.values() for _, ph in lines)
    for s in FORBIDDEN_SUB:
        if s.lower() in blob.lower():
            raise SystemExit(f"{story_id} interdit: {s}")
    for name in FORBIDDEN_NAMES:
        if re.search(rf"\b{re.escape(name)}\b", blob):
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


def story_029() -> None:
    lieux = {"P0001": "sable", "P0002": "toboggan", "P0003": "balancoires"}
    jouets = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    animaux = {"P0001": "poule", "P0002": "chevre", "P0003": "poulain"}

    lieu_np = {
        "sable": "le bac à sable",
        "toboggan": "le toboggan",
        "balancoires": "les balançoires",
    }
    jouet_np = {"ballon": "le ballon", "seau": "le seau", "doudou": "le doudou"}
    animal_np = {"poule": "la poule", "chevre": "la chèvre", "poulain": "le poulain"}

    lieu_l1 = {
        "sable": [
            ("narrateur", "Sarah va vers le bac à sable."),
            ("narrateur", "Le sable est frais, un peu humide."),
            ("narrateur", "Le bois du rebord est gris, tout lisse."),
            ("narrateur", "Une petite pelle rouge attend dedans."),
            ("maman", "Viens, Sarah."),
            ("maman", "Le sable est doux, aujourd'hui."),
            ("narrateur", "Sarah s'assoit au bord."),
            ("narrateur", "Le gilet d'école touche le bois."),
            ("enfant-f", "Maman, la maîtresse a parlé."),
            ("maman", "Tu as écouté ?"),
            ("enfant-f", "Oui."),
            ("enfant-f", "J'ai écouté jusqu'au bout."),
            ("narrateur", "Sarah prend la pelle."),
            ("narrateur", "Le manche est un peu rêche."),
            ("narrateur", "Un souvenir revient, tout près."),
            ("narrateur", "Un camarade a chuchoté, ce matin."),
            ("narrateur", "Le ventre de Sarah se serre."),
            ("enfant-f", "Maman."),
            ("enfant-f", "J'ai eu un malaise."),
            ("enfant-f", "Il a parlé tout bas, d'un secret."),
            ("maman", "Tu as bien fait de raconter."),
            ("maman", "On écoute la maîtresse."),
            ("maman", "Si malaise, tu viens nous le dire."),
            ("papa", "Je t'écoute, moi aussi."),
            ("papa", "Bravo, Sarah."),
            ("narrateur", "Le sable coule entre les doigts."),
            ("narrateur", "Le ventre se desserre, tout doux."),
            ("enfant-f", "Je raconte à la maison."),
            ("maman", "À la ferme aussi, on raconte."),
        ],
        "toboggan": [
            ("narrateur", "Sarah va vers le toboggan."),
            ("narrateur", "Le métal est tiède, un peu pâle."),
            ("narrateur", "Une feuille sèche est sur la marche."),
            ("narrateur", "Les marches sentent le bois et la poussière."),
            ("papa", "Je tiens le côté, Sarah."),
            ("papa", "Tu montes, tout doux."),
            ("narrateur", "Sarah pose un pied, puis l'autre."),
            ("narrateur", "Le gilet d'école frotte la rampe."),
            ("enfant-f", "Papa, j'ai écouté la maîtresse."),
            ("papa", "Oui."),
            ("papa", "On écoute d'abord."),
            ("narrateur", "Sarah s'arrête, en haut."),
            ("narrateur", "Le pré est vert, tout plat."),
            ("narrateur", "Le souvenir du chuchotement revient."),
            ("narrateur", "Son ventre se serre, tout petit."),
            ("enfant-f", "Papa, j'ai eu un malaise."),
            ("enfant-f", "Un camarade a parlé tout bas."),
            ("papa", "Tu as bien fait de le dire."),
            ("papa", "Si malaise, tu racontes à papa ou maman."),
            ("maman", "Je t'écoute, Sarah."),
            ("maman", "On écoute la maîtresse."),
            ("maman", "Ensuite, tu nous racontes."),
            ("narrateur", "Sarah glisse, tout lentement."),
            ("narrateur", "Le sable de l'arrivée est tiède."),
            ("enfant-f", "Je raconte à la maison."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
        ],
        "balancoires": [
            ("narrateur", "Sarah va vers les balançoires."),
            ("narrateur", "La corde est rêche, un peu tiède."),
            ("narrateur", "L'herbe sous les pieds est plate."),
            ("narrateur", "Un oiseau passe, tout loin."),
            ("maman", "Je suis près de toi."),
            ("maman", "On pousse tout doux."),
            ("narrateur", "Sarah s'assoit."),
            ("narrateur", "Le bois de l'assise est lisse."),
            ("enfant-f", "Maman, la maîtresse a dit d'écouter."),
            ("maman", "Tu as écouté ?"),
            ("enfant-f", "Oui, jusqu'au bout."),
            ("narrateur", "La balançoire avance, tout petit."),
            ("narrateur", "Sarah pense à la cour, ce matin."),
            ("narrateur", "Un camarade a chuchoté, trop près."),
            ("narrateur", "Son ventre se serre encore."),
            ("enfant-f", "Maman, j'ai eu un malaise."),
            ("enfant-f", "Il a parlé d'un secret."),
            ("maman", "Tu viens me le dire."),
            ("maman", "C'est bien."),
            ("papa", "On écoute la maîtresse."),
            ("papa", "Si malaise, on raconte à la maison."),
            ("narrateur", "La corde se tait un peu."),
            ("narrateur", "Le ventre de Sarah se desserre."),
            ("enfant-f", "Je raconte à papa et maman."),
            ("maman", "Bravo, Sarah."),
            ("maman", "On t'écoute."),
        ],
    }

    q = {
        "sable": [
            ("narrateur", "Sarah a un malaise, dans le sable."),
            ("maman", "Elle raconte à qui ?"),
        ],
        "toboggan": [
            ("narrateur", "Sarah a écouté la maîtresse."),
            ("papa", "Et si le ventre se serre ?"),
        ],
        "balancoires": [
            ("narrateur", "Sarah écoute, puis elle raconte."),
            ("maman", "On raconte à la maison ?"),
        ],
    }

    conf = {
        "sable": [
            ("maman", "Oui."),
            ("maman", "On raconte à papa ou maman."),
            ("papa", "Si malaise, tu viens le dire."),
            ("narrateur", "Sarah souffle un peu."),
            ("narrateur", "Le sable est encore frais, sous la paume."),
            ("enfant-f", "J'ai raconté."),
            ("maman", "Bravo."),
            ("maman", "Tu as écouté, puis tu as raconté."),
            ("papa", "C'est du bon travail, Sarah."),
            ("narrateur", "La petite pelle rouge reste dans le sable."),
        ],
        "toboggan": [
            ("papa", "Oui."),
            ("papa", "On raconte à la maison."),
            ("maman", "On écoute la maîtresse."),
            ("maman", "Si malaise, tu nous le dis."),
            ("narrateur", "Sarah pose les deux pieds dans le sable."),
            ("enfant-f", "Je raconte à papa."),
            ("papa", "Bravo."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", "La feuille sèche vole un peu, tout loin."),
        ],
        "balancoires": [
            ("maman", "Oui."),
            ("maman", "On raconte à la maison."),
            ("papa", "On t'écoute, Sarah."),
            ("narrateur", "La corde ne bouge plus."),
            ("enfant-f", "J'ai écouté."),
            ("enfant-f", "Puis j'ai raconté."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "L'herbe sous les pieds est encore plate."),
        ],
    }

    jouet_scene = {
        "ballon": [
            ("narrateur", "Sarah prend le ballon rouge."),
            ("narrateur", "Le ballon est un peu sablé, tout doux."),
            ("narrateur", "Il fait poum contre le bois."),
            ("papa", "Moi, je raconte le pré."),
            ("narrateur", "Papa parle jusqu'au bout."),
            ("narrateur", "Sarah écoute."),
            ("enfant-f", "Le ballon est chaud."),
            ("maman", "Tu as écouté."),
            ("maman", "Si le ventre se serre, tu racontes."),
            ("enfant-f", "Oui, maman."),
            ("papa", "Bravo."),
            ("narrateur", "Le ballon reste près du gilet."),
        ],
        "seau": [
            ("narrateur", "Sarah prend le seau bleu."),
            ("narrateur", "Un peu de sable tremble au fond."),
            ("narrateur", "Le seau sonne, tout creux."),
            ("maman", "Moi, je raconte le puits."),
            ("narrateur", "Maman parle, tout près."),
            ("narrateur", "Sarah écoute jusqu'au bout."),
            ("enfant-f", "Le seau est lourd."),
            ("papa", "Tu as écouté."),
            ("papa", "Si malaise, tu viens nous le dire."),
            ("enfant-f", "Je raconte à la maison."),
            ("maman", "Bravo, Sarah."),
            ("narrateur", "Sarah pose le seau, tout droit."),
        ],
        "doudou": [
            ("narrateur", "Sarah prend le doudou gris."),
            ("narrateur", "Une oreille est encore chaude."),
            ("narrateur", "Le doudou sent le foin, un peu."),
            ("papa", "Le doudou écoute, lui aussi."),
            ("narrateur", "Papa parle tout bas."),
            ("narrateur", "Sarah serre le doudou."),
            ("enfant-f", "J'ai encore un peu le ventre serré."),
            ("maman", "Tu peux raconter."),
            ("maman", "On t'écoute."),
            ("enfant-f", "Un camarade a chuchoté."),
            ("papa", "Tu as bien fait de le dire."),
            ("papa", "On écoute la maîtresse."),
            ("narrateur", "Le doudou reste sur les genoux."),
        ],
    }

    extra_jouet = {
        ("sable", "ballon"): "Le ballon laisse une trace ronde dans le sable.",
        ("sable", "seau"): "Le seau fait un creux, tout propre.",
        ("sable", "doudou"): "Le doudou a un grain de sable sur l'oreille.",
        ("toboggan", "ballon"): "Le ballon attend au pied du toboggan.",
        ("toboggan", "seau"): "Le seau sonne contre la rampe, tout doux.",
        ("toboggan", "doudou"): "Le doudou voyage sur les genoux, en haut.",
        ("balancoires", "ballon"): "Le ballon repose dans l'herbe, sous la corde.",
        ("balancoires", "seau"): "Le seau penche un peu, près de l'herbe.",
        ("balancoires", "doudou"): "Le doudou s'assoit sur l'assise, tout calme.",
    }

    animal_open = {
        "poule": [
            ("narrateur", "La poule picore près de la haie."),
            ("narrateur", "Elle fait cot cot, tout petit."),
            ("narrateur", "Une plume blonde reste dans l'herbe."),
        ],
        "chevre": [
            ("narrateur", "La chèvre sonne sa clochette, tout léger."),
            ("narrateur", "Elle mâche une feuille, tout lentement."),
            ("narrateur", "Son poil est rêche, un peu chaud."),
        ],
        "poulain": [
            ("narrateur", "Le poulain souffle par le nez, tout chaud."),
            ("narrateur", "Sa crinière est douce, un peu en bataille."),
            ("narrateur", "Le foin sent bon, tout près."),
        ],
    }

    extras = {
        ("sable", "ballon", "poule"): "Un grain de mil colle au ballon, près de la poule.",
        ("sable", "ballon", "chevre"): "La chèvre pose le nez sur le ballon sablé.",
        ("sable", "ballon", "poulain"): "Le poulain recule. Le ballon reste dans le sable.",
        ("sable", "seau", "poule"): "La poule regarde le seau, puis picore ailleurs.",
        ("sable", "seau", "chevre"): "La clochette sonne. Le seau tremble un peu.",
        ("sable", "seau", "poulain"): "Le poulain renifle le seau, tout doux.",
        ("sable", "doudou", "poule"): "Une petite plume blonde colle au doudou.",
        ("sable", "doudou", "chevre"): "Le doudou sent la chèvre, un peu.",
        ("sable", "doudou", "poulain"): "Le poulain cligne. Le doudou reste sur les genoux.",
        ("toboggan", "ballon", "poule"): "La poule contourne le ballon, au pied du toboggan.",
        ("toboggan", "ballon", "chevre"): "La chèvre lève la tête. Le ballon attend en bas.",
        ("toboggan", "ballon", "poulain"): "Le poulain fait un pas. Le ballon reste calme.",
        ("toboggan", "seau", "poule"): "Un grain tombe près du seau, au pied du toboggan.",
        ("toboggan", "seau", "chevre"): "La chèvre mâche. Le seau sonne, tout creux.",
        ("toboggan", "seau", "poulain"): "Le foin touche le seau, près du poulain.",
        ("toboggan", "doudou", "poule"): "La poule picore loin du doudou, en bas.",
        ("toboggan", "doudou", "chevre"): "La clochette sonne. Sarah serre le doudou.",
        ("toboggan", "doudou", "poulain"): "Le poulain souffle. Le doudou est encore chaud.",
        ("balancoires", "ballon", "poule"): "La poule passe sous la corde, loin du ballon.",
        ("balancoires", "ballon", "chevre"): "La chèvre broute. Le ballon dort dans l'herbe.",
        ("balancoires", "ballon", "poulain"): "Le poulain secoue la crinière, près du ballon.",
        ("balancoires", "seau", "poule"): "La poule saute un peu, près du seau.",
        ("balancoires", "seau", "chevre"): "La chèvre s'approche. Sarah pose le seau.",
        ("balancoires", "seau", "poulain"): "Le poulain écoute. Le seau reste dans l'herbe.",
        ("balancoires", "doudou", "poule"): "Une plume blonde tombe près du doudou.",
        ("balancoires", "doudou", "chevre"): "La chèvre cligne. Le doudou reste sur l'assise.",
        ("balancoires", "doudou", "poulain"): "Le poulain souffle chaud, loin du doudou.",
    }

    fin_image = {
        "poule": "La poule picore encore un grain, tout loin.",
        "chevre": "La clochette sonne encore, tout léger.",
        "poulain": "Le poulain pose le nez dans le foin.",
    }

    def l3(lieu: str, jouet: str, animal: str) -> list[tuple[str, str]]:
        extra = extras[(lieu, jouet, animal)]
        extra_parts = [p.strip() for p in extra.split(". ") if p.strip()]
        extra_lines = [
            ("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in extra_parts
        ]
        return (
            animal_open[animal]
            + [
                ("narrateur", f"Sarah a encore {jouet_np[jouet]}, près de {lieu_np[lieu]}."),
            ]
            + extra_lines
            + [
                ("papa", f"On dit bonjour à {animal_np[animal]}."),
                ("narrateur", "Sarah écoute d'abord."),
                ("enfant-f", "Bonjour."),
                ("maman", "Tu as écouté."),
                ("maman", "Si malaise, tu racontes."),
                ("enfant-f", "Je raconte à la maison."),
                ("papa", "Bravo, Sarah."),
                ("papa", "On t'écoute."),
                ("narrateur", "Sarah pose " + jouet_np[jouet] + ", tout doux."),
                ("narrateur", "Le foin sent encore le soleil."),
            ]
        )

    def fin(lieu: str, jouet: str, animal: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as écouté la maîtresse."),
            ("maman", "Puis tu as raconté."),
            ("narrateur", f"Sarah a vu {animal_np[animal]}, près de {lieu_np[lieu]}."),
            ("narrateur", f"Elle avait {jouet_np[jouet]}."),
            ("papa", "Bravo, Sarah."),
            ("papa", "C'est du bon travail."),
            ("enfant-f", "Merci, papa."),
            ("enfant-f", "Merci, maman."),
            ("narrateur", fin_image[animal]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jouets attendent, tout proches."),
            ("maman", "Le ballon, le seau, ou le doudou ?"),
            ("papa", "On joue."),
            ("papa", "On écoute."),
            ("papa", "Et on raconte, si malaise."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Au fond du pré, trois animaux sont là."),
            ("papa", "La poule, la chèvre, ou le poulain ?"),
            ("maman", "On écoute d'abord."),
            ("maman", "Puis on raconte."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Une paille d'or colle encore au bois de la barrière."),
        ("narrateur", "Le coq a chanté, tout loin, derrière le hangar."),
        ("narrateur", "Ça sent le foin tiède et le lait."),
        ("narrateur", "Une botte de Sarah est encore mouillée, près du seau."),
        ("narrateur", "Le seau a une goutte qui tremble."),
        ("narrateur", "Dehors, le pré est vert, tout plat."),
        ("narrateur", "Une mouche tourne près de la porte de l'étable."),
        ("narrateur", "Maman étend un linge rayé sur la corde."),
        ("narrateur", "Le linge claque une fois, tout doux."),
        ("narrateur", "Papa rentre avec un panier d'œufs."),
        ("narrateur", "Les œufs sont chauds, tout blancs."),
        ("maman", "Sarah, tu as encore ton gilet d'école."),
        ("maman", "Il sent la craie, un peu."),
        ("papa", "La ferme est calme, ce soir-là."),
        ("narrateur", "En ce moment, Sarah pose la main sur la barrière."),
        ("narrateur", "Le bois est rêche, puis chaud."),
        ("narrateur", "La maîtresse a parlé, ce matin."),
        ("narrateur", "Sarah écoute encore, dans sa tête."),
        ("enfant-f", "J'ai écouté, maman."),
        ("maman", "Oui."),
        ("maman", "On écoute la maîtresse."),
        ("papa", "Et si le ventre se serre ?"),
        ("maman", "On raconte à papa ou maman, à la maison."),
        ("papa", "À la ferme aussi, on raconte."),
        ("narrateur", "Le bac à sable attend, près du pré."),
        ("narrateur", "Le toboggan brille un peu."),
        ("narrateur", "Les balançoires bougent, tout doux."),
        ("enfant-f", "Papa, on va là-bas ?"),
        ("papa", "On y va."),
        ("maman", "On t'écoute, Sarah."),
    ]
    sons["CHK_T0000_P0000"] = "coq,foin"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Où va Sarah, près du pré ?"),
        ("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ("maman", "On écoute."),
        ("maman", "Et on raconte, si malaise."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "sable": "sable",
            "toboggan": "toboggan",
            "balancoires": "balancoire,oiseau",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_jouet[(lieu, jouet)]
            by[cid_l2] = jouet_scene[jouet] + [
                ("narrateur", extra),
                ("narrateur", f"On est encore près de {lieu_np[lieu]}."),
                ("maman", "On écoute."),
                ("maman", "Si malaise, on raconte."),
            ]
            sons[cid_l2] = {"ballon": "ballon", "seau": "seau", "doudou": ""}[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, animal in animaux.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, animal)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, animal)
                sons[cid_l3] = {
                    "poule": "poule",
                    "chevre": "clochette",
                    "poulain": "poulain,foin",
                }[animal]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-029",
        {
            "fil_rouge": "À la ferme, Sarah a encore son gilet d'école. Elle écoute la maîtresse. Si le ventre se serre, elle raconte à papa ou maman.",
            "title": "Le foin et le gilet d'école",
            "characters": "Sarah, papa, maman",
            "setting": "à la ferme, près du pré",
        },
        by,
        sons,
        max_words=16,
    )


def story_030() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}

    lieu_np = {
        "cuisine": "la table",
        "jardin": "la vitre",
        "chambre": "le plaid",
    }
    jouet_np = {"cubes": "les cubes", "livre": "le livre", "dinette": "la dînette"}
    moment_np = {"matin": "le matin", "sieste": "après la sieste", "soir": "le soir"}

    lieu_l1 = {
        "cuisine": [
            ("narrateur", "Nina va vers la table."),
            ("narrateur", "La table se déplie, tout petit."),
            ("narrateur", "Des miettes y sont collées."),
            ("narrateur", "Ça sent le pain."),
            ("papa", "Moi, je raconte le goûter."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Nina a une chose à dire."),
            ("narrateur", "Elle lève la main."),
            ("narrateur", "Elle attend."),
            ("papa", "Oui, Nina."),
            ("papa", "C'est ton tour."),
            ("enfant-f", "Le pain est doux."),
            ("maman", "Bravo."),
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", "Maman pose une serviette."),
            ("narrateur", "La serviette est à carreaux."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ],
        "jardin": [
            ("narrateur", "Nina va vers la vitre."),
            ("narrateur", "Les champs filent, tout verts."),
            ("narrateur", "Une vache passe, tout loin."),
            ("narrateur", "Le verre est un peu froid."),
            ("maman", "Moi, je raconte les champs."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Une vache !"),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", "Le petit rond reste sur la vitre."),
            ("narrateur", "Les rails font tchouk, tchouk."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as levé la main."),
        ],
        "chambre": [
            ("narrateur", "Nina va vers le plaid."),
            ("narrateur", "Le plaid est gris, tout doux."),
            ("narrateur", "Il sent encore la maison."),
            ("narrateur", "Le siège est un peu rêche."),
            ("papa", "Moi, je raconte le plaid."),
            ("narrateur", "Papa parle, tout bas."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Le plaid est chaud."),
            ("maman", "C'est ton tour."),
            ("maman", "On a attendu."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo."),
            ("papa", "Tu as levé la main."),
            ("narrateur", "Nina pose la joue sur le plaid."),
            ("narrateur", "Les rails bercent un peu."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Nina veut parler, à la table."),
            ("papa", "Elle fait quoi d'abord ?"),
        ],
        "jardin": [
            ("narrateur", "Nina lève la main, à la vitre."),
            ("maman", "Et après, on attend ?"),
        ],
        "chambre": [
            ("narrateur", "Chacun son tour, sur le plaid."),
            ("papa", "On attend, puis on parle ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("papa", "Oui."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina souffle un peu."),
            ("narrateur", "Sa main redescend, tout doux."),
            ("enfant-f", "J'ai attendu."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Une miette reste sur la table."),
        ],
        "jardin": [
            ("maman", "Oui."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Nina pose le doigt sur le rond."),
            ("enfant-f", "J'attends mon tour."),
            ("papa", "Bravo, Nina."),
            ("papa", "La vitre est à toi, et le tour aussi."),
            ("narrateur", "La vache a disparu, tout loin."),
        ],
        "chambre": [
            ("papa", "Oui."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina hoche la tête."),
            ("enfant-f", "Chacun son tour."),
            ("maman", "On continue, tout doux."),
            ("maman", "Tu as levé la main."),
            ("narrateur", "Le plaid reste chaud, sous la joue."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Nina prend les cubes en bois."),
            ("narrateur", "Un cube rouge fait clic."),
            ("narrateur", "Un cube bleu sent le pin."),
            ("papa", "Moi, je raconte la tour."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("papa", "C'est ton tour."),
            ("enfant-f", "Une tour pour le train."),
            ("maman", "Oui."),
            ("maman", "Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina pose un cube, tout droit."),
        ],
        "livre": [
            ("narrateur", "Nina ouvre le livre."),
            ("narrateur", "La page sent le papier, un peu sec."),
            ("narrateur", "Un dessin de train est là."),
            ("maman", "Moi, je lis d'abord."),
            ("narrateur", "Maman lit jusqu'au bout."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Le train est rouge."),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina caresse la page, tout léger."),
            ("maman", "Bravo, Nina."),
        ],
        "dinette": [
            ("narrateur", "Nina prend la dînette."),
            ("narrateur", "Une petite tasse sonne, tout creux."),
            ("narrateur", "Une cuillère miniature est tiède."),
            ("papa", "Moi, je sers le goûter imaginaire."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Du pain pour maman ?"),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo."),
            ("papa", "Tu as attendu ton tour."),
            ("narrateur", "Nina pose la petite tasse, tout doux."),
        ],
    }

    extra_jouet = {
        ("cuisine", "cubes"): "Un cube attrape une miette, sur la table.",
        ("cuisine", "livre"): "Une miette reste au bord de la page.",
        ("cuisine", "dinette"): "La petite tasse est près du vrai pain.",
        ("jardin", "cubes"): "Un cube bleu colle à la vitre froide.",
        ("jardin", "livre"): "Le champ du livre ressemble au vrai champ.",
        ("jardin", "dinette"): "La petite tasse tremble, avec les rails.",
        ("chambre", "cubes"): "Un cube tapote le plaid, tout doux.",
        ("chambre", "livre"): "Le plaid tient le livre ouvert.",
        ("chambre", "dinette"): "La petite tasse est près du plaid.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, la lumière est pâle."),
            ("narrateur", "La rosée brille, dans les champs."),
            ("narrateur", "Les rails chantent, tout clairs."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, les joues sont chaudes."),
            ("narrateur", "Le plaid a un pli, tout doux."),
            ("narrateur", "Le wagon est calme, encore un peu."),
        ],
        "soir": [
            ("narrateur", "Le soir, la vitre devient orange."),
            ("narrateur", "Ça sent encore le pain."),
            ("narrateur", "Les lampes du wagon sont petites."),
        ],
    }

    extras = {
        ("cuisine", "cubes", "matin"): "Un cube jaune attrape le soleil, sur la table.",
        ("cuisine", "cubes", "sieste"): "Un cube fait un clic, tout petit, près du pain.",
        ("cuisine", "cubes", "soir"): "La lampe allonge l'ombre des cubes.",
        ("cuisine", "livre", "matin"): "Une miette reste collée sur la page.",
        ("cuisine", "livre", "sieste"): "Le livre est un peu chaud, comme le pain.",
        ("cuisine", "livre", "soir"): "Le train du livre brille sous la lampe.",
        ("cuisine", "dinette", "matin"): "La petite tasse sent encore le pain.",
        ("cuisine", "dinette", "sieste"): "Une cuillère miniature tremble près du sac.",
        ("cuisine", "dinette", "soir"): "La dînette fait un tout petit ding.",
        ("jardin", "cubes", "matin"): "Un cube bleu colle à la rosée de la vitre.",
        ("jardin", "cubes", "sieste"): "Un cube sèche au soleil, contre la vitre.",
        ("jardin", "cubes", "soir"): "Un cube garde un reflet orange.",
        ("jardin", "livre", "matin"): "La page montre un champ, comme dehors.",
        ("jardin", "livre", "sieste"): "Le livre sent le verre froid, un peu.",
        ("jardin", "livre", "soir"): "Un oiseau passe. Le livre reste ouvert.",
        ("jardin", "dinette", "matin"): "Une petite tasse a un rond de lumière.",
        ("jardin", "dinette", "sieste"): "La dînette est tiède, au soleil de la vitre.",
        ("jardin", "dinette", "soir"): "Loin de la dînette, les champs s'assombrissent.",
        ("chambre", "cubes", "matin"): "Un rayon pose sur la tour, sur le plaid.",
        ("chambre", "cubes", "sieste"): "Un cube est contre le plaid, tout calme.",
        ("chambre", "cubes", "soir"): "L'ombre des cubes danse sur le siège.",
        ("chambre", "livre", "matin"): "Le plaid tient la page, tout doux.",
        ("chambre", "livre", "sieste"): "Le livre est ouvert sur le plaid.",
        ("chambre", "livre", "soir"): "La page sent le plaid, un peu.",
        ("chambre", "dinette", "matin"): "Une tasse miniature est près du plaid.",
        ("chambre", "dinette", "sieste"): "La dînette attend au creux du plaid.",
        ("chambre", "dinette", "soir"): "Une petite tasse reflète la lampe.",
    }

    fin_image = {
        "matin": "Un champ passe encore, tout clair.",
        "sieste": "Le plaid redescend, tout calme.",
        "soir": "La lampe du wagon reste allumée, tout doux.",
    }

    def l3(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        extra = extras[(lieu, jouet, moment)]
        extra_parts = [p.strip() for p in extra.split(". ") if p.strip()]
        extra_lines = [
            ("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in extra_parts
        ]
        return (
            moment_open[moment]
            + [
                ("narrateur", f"Nina a encore {jouet_np[jouet]}."),
                ("narrateur", f"Elle est près de {lieu_np[lieu]}."),
            ]
            + extra_lines
            + [
                ("papa", "J'écoute encore un peu."),
                ("narrateur", "Nina lève la main."),
                ("narrateur", "Elle attend."),
                ("enfant-f", "Les rails font tchouk."),
                ("maman", "Bravo."),
                ("maman", "Tu as attendu."),
                ("maman", "Puis tu as parlé."),
                ("papa", "On lève la main, dans le train aussi."),
                ("enfant-f", "Merci, papa."),
                ("enfant-f", "Merci, maman."),
                ("narrateur", "Nina range " + jouet_np[jouet] + ", tout doux."),
            ]
        )

    def fin(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", f"Nina a vécu {moment_np[moment]}."),
            ("narrateur", f"Elle était près de {lieu_np[lieu]}."),
            ("narrateur", f"Elle a joué avec {jouet_np[jouet]}."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("narrateur", fin_image[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, dans le sac."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On joue."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Quel moment, dans le train ?"),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On lève la main."),
            ("maman", "Chacun son tour."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "La vitre du train est un peu embuée."),
        ("narrateur", "Un doigt de Nina y dessine un rond."),
        ("narrateur", "Derrière le rond, les champs filent."),
        ("narrateur", "Les rails font tchouk, tchouk."),
        ("narrateur", "Le siège est en tissu bleu."),
        ("narrateur", "Le tissu est un peu rêche."),
        ("narrateur", "Un ticket dépasse de la poche de papa."),
        ("narrateur", "Ça sent le pain du goûter."),
        ("narrateur", "Maman pose le sac sur les genoux."),
        ("narrateur", "Le sac est souple, un peu lourd."),
        ("papa", "Nina, tu as vu le petit rond ?"),
        ("enfant-f", "Oui, papa."),
        ("maman", "Le wagon est à nous, un moment."),
        ("narrateur", "En ce moment, Nina est sur le siège."),
        ("narrateur", "Elle a une chose à dire."),
        ("narrateur", "Papa parle encore du ticket."),
        ("narrateur", "Nina lève la main."),
        ("narrateur", "Elle attend."),
        ("papa", "C'est ton tour."),
        ("enfant-f", "Les champs, c'est tout vert."),
        ("maman", "Bravo."),
        ("maman", "Tu as attendu."),
        ("maman", "Puis tu as parlé."),
        ("papa", "On lève la main."),
        ("papa", "On attend."),
        ("papa", "Puis on parle."),
        ("narrateur", "Dans le wagon, trois coins attendent."),
        ("narrateur", "La table du goûter, comme une cuisine."),
        ("narrateur", "La vitre des champs, comme un jardin."),
        ("narrateur", "Le plaid, comme une chambre."),
    ]
    sons["CHK_T0000_P0000"] = "train,rails"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "On va où, dans le wagon ?"),
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
            "cuisine": "table,pain",
            "jardin": "train,vache",
            "chambre": "plaid",
        }[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_jouet[(lieu, jouet)]
            by[cid_l2] = jouet_scene[jouet] + [
                ("narrateur", extra),
                ("narrateur", f"On est encore près de {lieu_np[lieu]}."),
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
                sons[cid_l3] = {"matin": "rails", "sieste": "plaid", "soir": "train"}[moment]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-030",
        {
            "fil_rouge": "Dans le train, Nina dessine un rond sur la vitre. Elle a une chose à dire. Elle lève la main, elle attend, puis elle parle.",
            "title": "Le petit rond sur la vitre",
            "characters": "Nina, papa, maman",
            "setting": "dans le train avec papa et maman",
        },
        by,
        sons,
        max_words=10,
    )


if __name__ == "__main__":
    story_029()
    story_030()
    print("ok TREE-COL-029 TREE-COL-030")
