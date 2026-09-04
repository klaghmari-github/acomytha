#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-033 et TREE-COL-034 (texte seulement)."""
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
    "Kenzo",
    "Hugo",
    "Jules",
    "Nora",
    "Noé",
    "Noe",
    "Barnabé",
    "Barnabe",
    "Lila",
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
    low = blob.lower()
    for s in FORBIDDEN_SUB:
        if s.lower() in low:
            raise SystemExit(f"{story_id} interdit: {s}")
    for name in FORBIDDEN_NAMES:
        if re.search(rf"\b{re.escape(name)}\b", blob):
            raise SystemExit(f"{story_id} nom interdit: {name}")
    joined = "\n".join(f"{r}|{p}" for lines in by.values() for r, p in lines)
    if "papa|" not in joined or "maman|" not in joined:
        raise SystemExit(f"{story_id} besoin papa et maman")
    adults = " ".join(p for lines in by.values() for r, p in lines if r in ("papa", "maman"))
    if "Bravo" not in adults and "bon travail" not in adults.lower():
        raise SystemExit(f"{story_id} pas de bravo")
    if "?" not in adults:
        raise SystemExit(f"{story_id} pas de question adulte")


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


def story_033() -> None:
    lieux = {"P0001": "sable", "P0002": "toboggan", "P0003": "balancoires"}
    jouets = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    coins = {"P0001": "banc", "P0002": "marelle", "P0003": "cerceau"}

    lieu_np = {
        "sable": "le bac à sable",
        "toboggan": "le toboggan",
        "balancoires": "les balançoires",
    }
    jouet_np = {"ballon": "le ballon", "seau": "le seau", "doudou": "le doudou"}
    coin_np = {"banc": "le banc", "marelle": "la marelle", "cerceau": "le cerceau"}

    lieu_l1 = {
        "sable": [
            ("narrateur", "Nino s'assoit au bord du bac."),
            ("narrateur", "Le sable est frais, un peu blond."),
            ("narrateur", "Le bois du rebord est lisse, tout gris."),
            ("narrateur", "Une petite pelle rouge attend dedans."),
            ("narrateur", "L'ombre du manteau jaune tombe ici."),
            ("maman", "Le sable est doux, Nino."),
            ("maman", "Tu veux la pelle ?"),
            ("enfant-m", "Oui, maman."),
            ("narrateur", "Nino prend le manche."),
            ("narrateur", "Il est un peu rêche."),
            ("narrateur", "Le galet reste froid, dans la poche."),
            ("narrateur", "Un souvenir revient, tout près."),
            ("narrateur", "Quelqu'un a parlé tout bas, à l'école."),
            ("narrateur", "Le ventre de Nino se serre."),
            ("enfant-m", "Maman."),
            ("enfant-m", "J'ai eu un malaise."),
            ("enfant-m", "C'était un secret, tout bas."),
            ("maman", "Tu as bien fait de raconter."),
            ("maman", "On écoute la maîtresse."),
            ("maman", "Si malaise, tu viens nous le dire."),
            ("papa", "Je t'écoute, moi aussi."),
            ("papa", "Bravo, Nino."),
            ("narrateur", "Le sable coule entre les doigts."),
            ("narrateur", "Le ventre se desserre, tout doux."),
            ("enfant-m", "Je raconte à la maison."),
            ("maman", "Au parc aussi, on raconte."),
        ],
        "toboggan": [
            ("narrateur", "Nino pose un pied sur la marche."),
            ("narrateur", "Le métal du toboggan est tiède."),
            ("narrateur", "Une feuille verte colle à la rampe."),
            ("narrateur", "Ça sent l'herbe coupée, encore."),
            ("papa", "Tu montes tout doux, Nino ?"),
            ("enfant-m", "Oui, papa."),
            ("narrateur", "Nino s'assoit en haut."),
            ("narrateur", "Le galet appuie dans la poche."),
            ("narrateur", "La maîtresse a parlé, ce matin."),
            ("narrateur", "Nino a écouté jusqu'au bout."),
            ("narrateur", "Puis quelqu'un a chuchoté, trop près."),
            ("narrateur", "Le ventre se serre, tout petit."),
            ("enfant-m", "Papa."),
            ("enfant-m", "J'ai eu un malaise."),
            ("enfant-m", "Un secret, tout bas."),
            ("papa", "Tu as bien fait de le dire."),
            ("papa", "On écoute la maîtresse."),
            ("papa", "Si malaise, on raconte à la maison."),
            ("maman", "Je t'écoute, Nino."),
            ("maman", "Bravo."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Nino glisse, tout lent."),
            ("narrateur", "Le métal chante un tout petit ffft."),
            ("enfant-m", "Je raconte à papa et maman."),
            ("papa", "Au parc aussi, on raconte."),
        ],
        "balancoires": [
            ("narrateur", "Nino touche la chaîne tiède."),
            ("narrateur", "Elle fait tic, contre le poteau."),
            ("narrateur", "Le siège est en bois, un peu rêche."),
            ("narrateur", "Un pigeon recule, tout près."),
            ("maman", "Tu t'assoies, Nino ?"),
            ("enfant-m", "Oui, maman."),
            ("narrateur", "Nino pose les pieds dans l'herbe."),
            ("narrateur", "L'herbe coupée colle aux chaussures."),
            ("narrateur", "La craie de l'école reste au genou."),
            ("narrateur", "Nino a écouté la maîtresse."),
            ("narrateur", "Puis un chuchotement a serré le ventre."),
            ("enfant-m", "Maman."),
            ("enfant-m", "Papa."),
            ("enfant-m", "J'ai eu un malaise."),
            ("maman", "Tu as bien fait de raconter."),
            ("papa", "On écoute la maîtresse."),
            ("papa", "Si malaise, tu viens nous le dire."),
            ("maman", "Bravo, Nino."),
            ("maman", "On t'écoute, toujours."),
            ("narrateur", "La chaîne fait tic, plus doux."),
            ("narrateur", "Le ventre se desserre."),
            ("enfant-m", "Je raconte à la maison."),
            ("papa", "Ici aussi, Nino."),
        ],
    }

    q = {
        "sable": [
            ("narrateur", "Nino a un malaise, au bac."),
            ("maman", "Que fait-il ?"),
        ],
        "toboggan": [
            ("narrateur", "Nino a un malaise, en haut."),
            ("papa", "Il raconte à qui ?"),
        ],
        "balancoires": [
            ("narrateur", "Le ventre de Nino s'est serré."),
            ("maman", "On raconte à la maison ?"),
        ],
    }

    conf = {
        "sable": [
            ("maman", "Oui."),
            ("maman", "On écoute la maîtresse."),
            ("maman", "Si malaise, on raconte."),
            ("narrateur", "Nino souffle un peu."),
            ("enfant-m", "Je raconte à papa et maman."),
            ("papa", "Bravo, Nino."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "La pelle rouge reste dans le sable."),
        ],
        "toboggan": [
            ("papa", "Oui."),
            ("papa", "À papa."),
            ("papa", "À maman."),
            ("papa", "À la maison."),
            ("narrateur", "Nino pose les deux pieds dans l'herbe."),
            ("enfant-m", "J'ai raconté."),
            ("maman", "Bravo."),
            ("maman", "Tu as écouté, puis raconté."),
            ("narrateur", "La feuille verte reste sur la rampe."),
        ],
        "balancoires": [
            ("maman", "Oui."),
            ("maman", "On raconte à papa ou maman."),
            ("maman", "À la maison."),
            ("narrateur", "Nino serre la chaîne, tout doux."),
            ("enfant-m", "Je raconte."),
            ("papa", "Bravo, Nino."),
            ("papa", "On t'écoute."),
            ("narrateur", "Le pigeon picore encore, plus loin."),
        ],
    }

    jouet_scene = {
        "ballon": [
            ("narrateur", "Nino prend le ballon rouge."),
            ("narrateur", "Il sent le caoutchouc, un peu chaud."),
            ("narrateur", "Une miette colle encore dessus."),
            ("papa", "Tu veux le lancer, tout doux ?"),
            ("enfant-m", "Oui, papa."),
            ("narrateur", "Papa parle d'abord, tout calme."),
            ("narrateur", "Nino écoute jusqu'au bout."),
            ("enfant-m", "Le ballon est chaud."),
            ("maman", "Tu as écouté."),
            ("maman", "Bravo."),
            ("narrateur", "Le ballon fait un petit poum, dans l'herbe."),
        ],
        "seau": [
            ("narrateur", "Nino prend le seau bleu."),
            ("narrateur", "Le plastique est un peu froid."),
            ("narrateur", "Un peu de sable reste au fond."),
            ("maman", "Tu veux remplir le seau ?"),
            ("enfant-m", "Oui, maman."),
            ("narrateur", "Maman parle d'abord."),
            ("narrateur", "Nino écoute."),
            ("enfant-m", "Le seau est froid."),
            ("papa", "Tu as écouté."),
            ("papa", "Bravo, Nino."),
            ("narrateur", "Le seau tapote le bois, tout fin."),
        ],
        "doudou": [
            ("narrateur", "Nino prend le doudou gris."),
            ("narrateur", "Une oreille est encore tiède."),
            ("narrateur", "Il sent le cartable, un peu."),
            ("maman", "Tu le serres, Nino ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Maman parle tout doux."),
            ("narrateur", "Nino écoute jusqu'au bout."),
            ("enfant-m", "Le doudou est tiède."),
            ("papa", "Bravo."),
            ("papa", "Tu as écouté."),
            ("narrateur", "Le doudou pose l'oreille sur le genou."),
        ],
    }

    extra_jouet = {
        ("sable", "ballon"): "Le ballon laisse un rond, dans le sable.",
        ("sable", "seau"): "Le seau prend du sable blond, tout frais.",
        ("sable", "doudou"): "Le doudou a un grain de sable, à l'oreille.",
        ("toboggan", "ballon"): "Le ballon attend au pied du toboggan.",
        ("toboggan", "seau"): "Le seau sonne un ding, contre le métal.",
        ("toboggan", "doudou"): "Le doudou glisse un peu, sur la rampe.",
        ("balancoires", "ballon"): "Le ballon roule sous la balançoire.",
        ("balancoires", "seau"): "Le seau tremble, quand la chaîne fait tic.",
        ("balancoires", "doudou"): "Le doudou s'assoit sur le siège, tout calme.",
    }

    coin_open = {
        "banc": [
            ("narrateur", "Le banc de bois est encore tiède."),
            ("narrateur", "Le manteau jaune y fait un tas."),
            ("narrateur", "Une flaque tient le ciel, tout bas."),
        ],
        "marelle": [
            ("narrateur", "La marelle a des cases, à la craie."),
            ("narrateur", "Une case est un peu effacée."),
            ("narrateur", "La craie sent l'école, encore."),
        ],
        "cerceau": [
            ("narrateur", "Le cerceau jaune est dans l'herbe."),
            ("narrateur", "Il est un peu chaud, au soleil."),
            ("narrateur", "Une tige d'herbe passe au milieu."),
        ],
    }

    extras = {
        ("sable", "ballon", "banc"): "Le ballon s'appuie contre le banc.",
        ("sable", "ballon", "marelle"): "Le ballon roule sur une case, tout doux.",
        ("sable", "ballon", "cerceau"): "Le ballon entre dans le cerceau, tout juste.",
        ("sable", "seau", "banc"): "Le seau bleu pose au pied du banc.",
        ("sable", "seau", "marelle"): "Un peu de sable tombe sur la marelle.",
        ("sable", "seau", "cerceau"): "Le seau sonne, contre le cerceau.",
        ("sable", "doudou", "banc"): "Le doudou s'assoit sur le manteau jaune.",
        ("sable", "doudou", "marelle"): "Le doudou pose l'oreille sur une case.",
        ("sable", "doudou", "cerceau"): "Le doudou regarde le cerceau, tout calme.",
        ("toboggan", "ballon", "banc"): "Le ballon roule du toboggan jusqu'au banc.",
        ("toboggan", "ballon", "marelle"): "Le ballon s'arrête sur la première case.",
        ("toboggan", "ballon", "cerceau"): "Le ballon traverse le cerceau, tout lent.",
        ("toboggan", "seau", "banc"): "Le seau attend au pied du banc, tout bleu.",
        ("toboggan", "seau", "marelle"): "Le seau pose sur la case du milieu.",
        ("toboggan", "seau", "cerceau"): "Le seau tient le cerceau, tout droit.",
        ("toboggan", "doudou", "banc"): "Le doudou rejoint le manteau, sur le banc.",
        ("toboggan", "doudou", "marelle"): "Le doudou saute une case, tout doux.",
        ("toboggan", "doudou", "cerceau"): "Le doudou passe la tête dans le cerceau.",
        ("balancoires", "ballon", "banc"): "Le ballon se gare sous le banc.",
        ("balancoires", "ballon", "marelle"): "Le ballon fait poum, sur une case.",
        ("balancoires", "ballon", "cerceau"): "Le ballon et le cerceau se touchent.",
        ("balancoires", "seau", "banc"): "Le seau sonne un ding, contre le banc.",
        ("balancoires", "seau", "marelle"): "Un grain de sable reste sur la marelle.",
        ("balancoires", "seau", "cerceau"): "Le seau tremble dans le cerceau.",
        ("balancoires", "doudou", "banc"): "Le doudou s'endort sur le manteau jaune.",
        ("balancoires", "doudou", "marelle"): "Le doudou garde la case du ciel.",
        ("balancoires", "doudou", "cerceau"): "Le doudou tient le cerceau, tout léger.",
    }

    fin_image = {
        "banc": "Le manteau jaune reste plié, tout calme.",
        "marelle": "La craie de la marelle sèche, tout pâle.",
        "cerceau": "Le cerceau jaune dort dans l'herbe.",
    }

    def l3(lieu: str, jouet: str, coin: str) -> list[tuple[str, str]]:
        extra = extras[(lieu, jouet, coin)]
        return (
            coin_open[coin]
            + [
                ("narrateur", f"Nino a encore {jouet_np[jouet]}."),
                ("narrateur", f"Il est près de {lieu_np[lieu]}."),
                ("narrateur", extra),
                ("papa", "Tu as encore un mot, Nino ?"),
                ("narrateur", "Nino respire."),
                ("enfant-m", "J'ai écouté la maîtresse."),
                ("enfant-m", "Si malaise, je raconte."),
                ("maman", "Bravo."),
                ("maman", "Tu as écouté."),
                ("maman", "Puis tu as raconté."),
                ("papa", "C'est du bon travail, Nino."),
                ("enfant-m", "Merci, papa."),
                ("enfant-m", "Merci, maman."),
                ("narrateur", f"{coin_np[coin].capitalize()} reste tout près."),
            ]
        )

    def fin(lieu: str, jouet: str, coin: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as écouté la maîtresse."),
            ("maman", "Puis tu as raconté."),
            ("narrateur", f"Nino a choisi {lieu_np[lieu]}."),
            ("narrateur", f"Il avait {jouet_np[jouet]}."),
            ("narrateur", f"Il est allé vers {coin_np[coin]}."),
            ("papa", "Bravo, Nino."),
            ("papa", "C'est du bon travail."),
            ("narrateur", fin_image[coin]),
            ("narrateur", "La chaîne de la balançoire se tait."),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jouets attendent, dans l'herbe."),
            ("maman", "Le ballon, le seau, ou le doudou ?"),
            ("papa", "On joue."),
            ("papa", "On écoute."),
            ("papa", "Et on raconte, si malaise."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois coins du parc attendent."),
            ("papa", "Le banc, la marelle, ou le cerceau ?"),
            ("maman", "On écoute d'abord."),
            ("maman", "Puis on raconte."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "La chaîne de la balançoire est tiède."),
        ("narrateur", "Elle fait tic, tout petit, contre le poteau."),
        ("narrateur", "Un manteau jaune est plié sur le banc."),
        ("narrateur", "Une flaque tient le ciel, tout bas."),
        ("narrateur", "Ça sent l'herbe coupée, encore."),
        ("narrateur", "Un pigeon picore une miette, tout près."),
        ("narrateur", "Le cartable de Nino s'appuie contre le banc."),
        ("narrateur", "Il sent encore la craie de l'école."),
        ("narrateur", "Un galet froid reste dans la poche."),
        ("maman", "Nino, tu as encore tes chaussures d'école."),
        ("maman", "Elles sont un peu poussiéreuses."),
        ("papa", "Le parc est calme, ce soir-là."),
        ("narrateur", "En ce moment, Nino pose la main sur la chaîne."),
        ("narrateur", "Le métal est tiède, un peu rugueux."),
        ("narrateur", "La maîtresse a parlé, ce matin."),
        ("narrateur", "Nino écoute encore, dans sa tête."),
        ("enfant-m", "J'ai écouté, maman."),
        ("maman", "Oui."),
        ("maman", "On écoute la maîtresse."),
        ("papa", "Et si le ventre se serre ?"),
        ("maman", "On raconte à papa ou maman, à la maison."),
        ("papa", "Au parc aussi, on raconte."),
        ("narrateur", "Le bac à sable attend, tout blond."),
        ("narrateur", "Le toboggan tient encore le soleil."),
        ("narrateur", "Les balançoires bougent, tout doux."),
        ("enfant-m", "Papa, on va là-bas ?"),
        ("papa", "On y va."),
        ("maman", "On t'écoute, Nino."),
    ]
    sons["CHK_T0000_P0000"] = "enfants_parc,chaine"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Où va Nino, dans le parc ?"),
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

            for p3, coin in coins.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, coin)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, coin)
                sons[cid_l3] = {
                    "banc": "banc",
                    "marelle": "craie",
                    "cerceau": "cerceau",
                }[coin]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-033",
        {
            "fil_rouge": (
                "La chaîne de la balançoire est tiède. Un galet reste "
                "dans la poche. Nino a écouté la maîtresse. Si le ventre "
                "se serre, il raconte à papa ou maman."
            ),
            "title": "La chaîne tiède et le galet",
            "characters": "Nino, papa, maman",
            "setting": "au parc, après l'école",
        },
        by,
        sons,
        max_words=15,
    )


def story_034() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}

    lieu_np = {
        "cuisine": "la cuisine",
        "jardin": "le jardin",
        "chambre": "la chambre",
    }
    jouet_np = {
        "cubes": "les cubes",
        "livre": "le livre",
        "dinette": "la dînette",
    }
    moment_np = {
        "matin": "le matin",
        "sieste": "après la sieste",
        "soir": "le soir",
    }

    lieu_l1 = {
        "cuisine": [
            ("narrateur", "Mila pousse la porte de la cuisine."),
            ("narrateur", "Le carrelage est un peu froid."),
            ("narrateur", "L'arrosoir sonne, près du seuil."),
            ("narrateur", "Ça sent la menthe, encore."),
            ("narrateur", "Une tomate verte attend au saladier."),
            ("papa", "Bonjour, Mila."),
            ("enfant-f", "Bonjour, papa."),
            ("papa", "Moi, je parle d'abord."),
            ("narrateur", "Papa parle jusqu'au bout."),
            ("narrateur", "Mila lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "La tomate est encore petite."),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "Tu as attendu."),
            ("papa", "On lève la main."),
            ("papa", "On peut attendre."),
            ("papa", "Puis on parle."),
            ("narrateur", "Mila touche la tomate, tout doux."),
            ("narrateur", "La peau est lisse, un peu froide."),
        ],
        "jardin": [
            ("narrateur", "Mila revient sous la menthe."),
            ("narrateur", "L'herbe colle aux chaussettes."),
            ("narrateur", "L'arrosoir penche encore, tout lent."),
            ("narrateur", "Le ver rose glisse entre deux cailloux."),
            ("maman", "Tu as vu le ver, Mila ?"),
            ("enfant-f", "Oui, maman."),
            ("maman", "Moi, je raconte le ver d'abord."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Mila lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Le ver est tout rose."),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "Tu as attendu."),
            ("maman", "On lève la main."),
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
            ("narrateur", "Une goutte tombe sur la terre."),
            ("narrateur", "Le ver se cache, tout calme."),
        ],
        "chambre": [
            ("narrateur", "Mila entre dans la chambre."),
            ("narrateur", "Le parquet craque, tout petit."),
            ("narrateur", "Un rayon pose sur le plaid."),
            ("narrateur", "Ça sent encore la menthe, aux doigts."),
            ("papa", "Bonjour, petite chambre."),
            ("enfant-f", "Bonjour, papa."),
            ("maman", "Moi, je raconte le plaid."),
            ("narrateur", "Maman parle, tout calme."),
            ("narrateur", "Mila lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Le plaid est tout doux."),
            ("papa", "C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("maman", "Bravo, Mila."),
            ("maman", "Tu as levé la main."),
            ("narrateur", "Mila pose la joue sur le plaid."),
            ("narrateur", "Le tissu est chaud, un peu lourd."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Dans la cuisine, Mila veut parler."),
            ("maman", "Que fait-elle d'abord ?"),
        ],
        "jardin": [
            ("narrateur", "Mila a une chose à dire."),
            ("papa", "Elle lève la main ?"),
        ],
        "chambre": [
            ("narrateur", "Dans la chambre, chacun son tour."),
            ("maman", "On attend, puis on parle ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("maman", "Oui."),
            ("maman", "On lève la main."),
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
            ("narrateur", "Mila souffle un peu."),
            ("enfant-f", "J'ai attendu."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "La tomate verte reste froide."),
        ],
        "jardin": [
            ("papa", "Oui."),
            ("papa", "On lève la main."),
            ("papa", "On peut attendre."),
            ("papa", "Puis on parle."),
            ("narrateur", "Mila hoche la tête."),
            ("enfant-f", "J'attends mon tour."),
            ("maman", "Bravo, Mila."),
            ("maman", "Tu as levé la main."),
            ("narrateur", "L'arrosoir reste penché, tout calme."),
        ],
        "chambre": [
            ("maman", "Oui."),
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
            ("narrateur", "Mila caresse le plaid."),
            ("enfant-f", "Chacun son tour."),
            ("papa", "Bravo, Mila."),
            ("papa", "Tu as attendu."),
            ("narrateur", "Le rayon glisse sur l'oreiller."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Mila prend les cubes en bois."),
            ("narrateur", "Un cube vert sent le pin."),
            ("narrateur", "Un cube rouge fait clic."),
            ("papa", "Moi, je pose le cube vert."),
            ("narrateur", "Papa pose le cube."),
            ("narrateur", "Mila lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Je peux le rouge ?"),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "Puis on parle."),
            ("narrateur", "Mila pose le cube rouge."),
            ("papa", "Bravo, Mila."),
            ("papa", "Tu as attendu."),
        ],
        "livre": [
            ("narrateur", "Maman ouvre un livre d'images."),
            ("narrateur", "Une page sent le papier, un peu sec."),
            ("narrateur", "Un ver rose y glisse, tout petit."),
            ("maman", "Moi, je lis d'abord."),
            ("narrateur", "Maman lit jusqu'au bout."),
            ("narrateur", "Mila lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Le ver a une feuille."),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "On peut attendre."),
            ("papa", "Puis on parle."),
            ("narrateur", "Mila touche le papier, tout léger."),
            ("maman", "Bravo."),
            ("maman", "Tu as attendu."),
        ],
        "dinette": [
            ("narrateur", "Mila pose la petite tasse."),
            ("narrateur", "Elle sonne un ding, tout fin."),
            ("narrateur", "Ça sent encore la menthe."),
            ("papa", "Moi, je sers le goûter imaginaire."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Mila lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "Du thym pour maman ?"),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo."),
            ("papa", "Tu as attendu ton tour."),
            ("narrateur", "La petite tasse reste tiède."),
        ],
    }

    extra_jouet = {
        ("cuisine", "cubes"): "Un cube attrape une goutte, sur le bois.",
        ("cuisine", "livre"): "Une feuille de menthe marque la page.",
        ("cuisine", "dinette"): "La petite tasse est près du saladier.",
        ("jardin", "cubes"): "Un cube vert colle à l'herbe humide.",
        ("jardin", "livre"): "Le ver du livre ressemble au vrai ver.",
        ("jardin", "dinette"): "La petite tasse tremble, près de l'arrosoir.",
        ("chambre", "cubes"): "Un cube tapote le plaid, tout doux.",
        ("chambre", "livre"): "Le plaid tient le livre ouvert.",
        ("chambre", "dinette"): "La petite tasse est près du plaid.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, la rosée brille."),
            ("narrateur", "L'herbe est froide, tout nette."),
            ("narrateur", "Un oiseau chante, tout près."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, les joues sont chaudes."),
            ("narrateur", "L'ombre de la menthe est ronde."),
            ("narrateur", "L'arrosoir est tiède, au soleil."),
        ],
        "soir": [
            ("narrateur", "Le soir, la lampe est petite."),
            ("narrateur", "Ça sent encore la terre."),
            ("narrateur", "Un grillon chante, tout loin."),
        ],
    }

    extras = {
        ("cuisine", "cubes", "matin"): "Un cube jaune attrape le soleil, sur la table.",
        ("cuisine", "cubes", "sieste"): "Un cube fait un clic, tout petit, près du saladier.",
        ("cuisine", "cubes", "soir"): "La lampe allonge l'ombre des cubes.",
        ("cuisine", "livre", "matin"): "Une goutte de rosée manque la page.",
        ("cuisine", "livre", "sieste"): "Le livre est un peu chaud, comme le carrelage.",
        ("cuisine", "livre", "soir"): "Le ver du livre brille sous la lampe.",
        ("cuisine", "dinette", "matin"): "La petite tasse sent encore la menthe.",
        ("cuisine", "dinette", "sieste"): "Une cuillère miniature tremble près du saladier.",
        ("cuisine", "dinette", "soir"): "La dînette fait un tout petit ding.",
        ("jardin", "cubes", "matin"): "Un cube vert colle à la rosée.",
        ("jardin", "cubes", "sieste"): "Un cube sèche au soleil, contre l'arrosoir.",
        ("jardin", "cubes", "soir"): "Un cube garde un reflet orange.",
        ("jardin", "livre", "matin"): "La page montre un ver, comme dehors.",
        ("jardin", "livre", "sieste"): "Le livre sent l'herbe tiède, un peu.",
        ("jardin", "livre", "soir"): "Un grillon chante. Le livre reste ouvert.",
        ("jardin", "dinette", "matin"): "Une petite tasse a un rond de rosée.",
        ("jardin", "dinette", "sieste"): "La dînette est tiède, au soleil.",
        ("jardin", "dinette", "soir"): "Loin de la dînette, le jardin s'assombrit.",
        ("chambre", "cubes", "matin"): "Un rayon pose sur la tour, sur le plaid.",
        ("chambre", "cubes", "sieste"): "Un cube est contre le plaid, tout calme.",
        ("chambre", "cubes", "soir"): "L'ombre des cubes danse sur le parquet.",
        ("chambre", "livre", "matin"): "Le plaid tient la page, tout doux.",
        ("chambre", "livre", "sieste"): "Le livre est ouvert sur le plaid.",
        ("chambre", "livre", "soir"): "La page sent le plaid, un peu.",
        ("chambre", "dinette", "matin"): "Une tasse miniature est près du plaid.",
        ("chambre", "dinette", "sieste"): "La dînette attend au creux du plaid.",
        ("chambre", "dinette", "soir"): "Une petite tasse reflète la lampe.",
    }

    fin_image = {
        "matin": "La rosée sèche, tout doux, sur l'herbe.",
        "sieste": "L'ombre de la menthe redescend, tout calme.",
        "soir": "La petite lampe reste allumée, tout doux.",
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
                ("narrateur", f"Mila a encore {jouet_np[jouet]}."),
                ("narrateur", f"Elle est près de {lieu_np[lieu]}."),
            ]
            + extra_lines
            + [
                ("papa", "J'écoute encore un peu."),
                ("narrateur", "Mila lève la main."),
                ("narrateur", "Elle attend."),
                ("enfant-f", "L'arrosoir penche encore."),
                ("maman", "Bravo."),
                ("maman", "Tu as attendu."),
                ("maman", "Puis tu as parlé."),
                ("papa", "On lève la main, au jardin aussi."),
                ("enfant-f", "Merci, papa."),
                ("enfant-f", "Merci, maman."),
                ("narrateur", "Mila range " + jouet_np[jouet] + ", tout doux."),
            ]
        )

    def fin(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", f"Mila a vécu {moment_np[moment]}."),
            ("narrateur", f"Elle était près de {lieu_np[lieu]}."),
            ("narrateur", f"Elle a joué avec {jouet_np[jouet]}."),
            ("papa", "Bravo, Mila."),
            ("papa", "C'est du bon travail."),
            ("narrateur", fin_image[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout près."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On joue."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Quel moment, près de l'arrosoir ?"),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On lève la main."),
            ("maman", "Chacun son tour."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "L'arrosoir penche, tout lent."),
        ("narrateur", "Une goutte tombe sur la terre."),
        ("narrateur", "Ça sent la menthe, près du mur."),
        ("narrateur", "Un ver rose glisse entre deux cailloux."),
        ("narrateur", "Les chaussettes de Mila ont de l'herbe."),
        ("narrateur", "Une tomate verte brille, encore petite."),
        ("narrateur", "Le banc de bois reste un peu chaud."),
        ("narrateur", "Une abeille passe, tout loin."),
        ("maman", "Tu as vu le ver rose, Mila ?"),
        ("enfant-f", "Oui, maman."),
        ("papa", "L'eau de l'arrosoir est tiède."),
        ("narrateur", "Maman essuie une feuille, tout doux."),
        ("narrateur", "Le soleil pose un carré sur l'herbe."),
        ("papa", "Tu as une chose à dire ?"),
        ("enfant-f", "Oui, papa."),
        ("maman", "On lève la main."),
        ("maman", "On peut attendre."),
        ("maman", "Puis on parle."),
        ("narrateur", "En ce moment, Mila est dans le jardin."),
        ("narrateur", "Elle a de la terre aux doigts."),
        ("enfant-f", "J'ai une chose à dire."),
        ("papa", "Moi aussi."),
        ("papa", "On peut attendre d'abord."),
        ("narrateur", "Mila lève la main."),
        ("narrateur", "Elle attend."),
        ("papa", "C'est ton tour."),
        ("enfant-f", "Le ver est tout rose."),
        ("maman", "Bravo, Mila."),
        ("maman", "Tu as attendu."),
        ("maman", "Puis tu as parlé."),
        ("narrateur", "L'arrosoir reste penché, tout calme."),
    ]
    sons["CHK_T0000_P0000"] = "arrosoir,oiseau"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "La maison a trois endroits, tout proches."),
        ("maman", "La cuisine, le jardin, ou la chambre ?"),
        ("papa", "On lève la main."),
        ("papa", "On peut attendre."),
        ("papa", "Puis on parle."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {
            "cuisine": "porte,tomate",
            "jardin": "arrosoir,oiseau",
            "chambre": "parquet",
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
                sons[cid_l3] = {
                    "matin": "oiseau",
                    "sieste": "arrosoir",
                    "soir": "grillon",
                }[moment]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-034",
        {
            "fil_rouge": (
                "L'arrosoir penche. Un ver rose glisse. Mila lève la main, "
                "elle attend, puis elle parle, avec papa et maman."
            ),
            "title": "L'arrosoir et le ver rose",
            "characters": "Mila, papa, maman",
            "setting": "dans le jardin, près de la menthe",
        },
        by,
        sons,
        max_words=10,
    )


if __name__ == "__main__":
    story_033()
    story_034()
    print("ok TREE-COL-033 TREE-COL-034")
