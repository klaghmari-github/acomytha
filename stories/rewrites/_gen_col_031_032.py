#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-031 et TREE-COL-032 (texte seulement)."""
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
    "Barnabé",
    "Barnabe",
    "Lila",
    "Sara",
    "Kenzo",
    "Hugo",
    "Jules",
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


def story_031() -> None:
    lieux = {"P0001": "tapis", "P0002": "table", "P0003": "fenetre"}
    acts = {"P0001": "histoire", "P0002": "chanson", "P0003": "dessin"}
    objets = {"P0001": "doudou", "P0002": "camion", "P0003": "gobelet"}

    lieu_np = {
        "tapis": "le tapis",
        "table": "la table",
        "fenetre": "la fenêtre",
    }
    lieu_ou = {
        "tapis": "sur le tapis",
        "table": "à la table",
        "fenetre": "près de la fenêtre",
    }
    act_np = {
        "histoire": "l'histoire",
        "chanson": "la chanson",
        "dessin": "le dessin",
    }
    obj_np = {
        "doudou": "le doudou",
        "camion": "le camion",
        "gobelet": "le gobelet",
    }

    lieu_l1 = {
        "tapis": [
            ("narrateur", "Victorino pose un genou sur le tapis."),
            ("narrateur", "Le tapis est gris, un peu rêche."),
            ("narrateur", "Un bouton bleu s'est perdu dans les poils."),
            ("narrateur", "Le radiateur chauffe encore, tout près."),
            ("maman", "Moi, je raconte le bouton d'abord."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Victorino a une chose à dire."),
            ("narrateur", "Il lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le bouton est tout rond."),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "Tu as attendu."),
            ("maman", "On lève la main."),
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorino touche le bouton, tout doux."),
            ("narrateur", "Le tapis chatouille encore le genou."),
        ],
        "table": [
            ("narrateur", "Victorino s'assoit à la table."),
            ("narrateur", "Le bois sent l'orange, un peu."),
            ("narrateur", "Un crayon bleu a roulé, tout seul."),
            ("narrateur", "Une petite tache luisante reste sur le bois."),
            ("papa", "Moi, je raconte le crayon."),
            ("narrateur", "Papa parle, tout calme."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le crayon a une mine cassée."),
            ("maman", "Oui."),
            ("maman", "Merci d'avoir attendu."),
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorino pose un doigt sur la tache."),
            ("narrateur", "Elle est un peu collante."),
            ("papa", "Bravo, Victorino."),
            ("papa", "Tu as levé la main."),
        ],
        "fenetre": [
            ("narrateur", "Victorino s'approche de la fenêtre."),
            ("narrateur", "La vitre est embuée, toute douce au doigt."),
            ("narrateur", "Le bateau en papier attend sur le rebord."),
            ("narrateur", "Dehors, la gouttière chante, tout fin."),
            ("maman", "Moi, je raconte le bateau."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le bateau a une voile pliée."),
            ("papa", "C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
            ("narrateur", "Un trait d'eau glisse sur la vitre."),
            ("narrateur", "Le bateau ne bouge pas."),
        ],
    }

    q = {
        "tapis": [
            ("narrateur", "Sur le tapis, Victorino veut parler."),
            ("maman", "Que fait-il d'abord ?"),
        ],
        "table": [
            ("narrateur", "À la table, Victorino lève la main."),
            ("papa", "Et après, on peut attendre ?"),
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
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorino souffle un peu."),
            ("narrateur", "Sa main redescend, tout doux."),
            ("enfant-m", "J'ai attendu."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Le bouton bleu reste dans les poils."),
        ],
        "table": [
            ("papa", "Oui."),
            ("papa", "On peut attendre."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino pose le crayon, tout droit."),
            ("enfant-m", "J'attends mon tour."),
            ("maman", "Bravo, Victorino."),
            ("maman", "La table est à toi, et le tour aussi."),
            ("narrateur", "La petite tache brille encore."),
        ],
        "fenetre": [
            ("maman", "Oui."),
            ("maman", "On lève la main."),
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorino hoche la tête."),
            ("enfant-m", "Chacun son tour."),
            ("papa", "On continue, tout doux."),
            ("papa", "Tu as levé la main."),
            ("narrateur", "La gouttière chante encore, dehors."),
        ],
    }

    act_scene = {
        "histoire": [
            ("narrateur", "Maman ouvre un livre d'images."),
            ("narrateur", "Une page sent le papier, un peu sec."),
            ("narrateur", "Un bateau y flotte, tout blanc."),
            ("maman", "Moi, je lis l'histoire d'abord."),
            ("narrateur", "Maman lit jusqu'au bout."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le bateau a une voile."),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "On peut attendre."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino touche le papier, tout léger."),
            ("maman", "Bravo."),
            ("maman", "Tu as attendu."),
        ],
        "chanson": [
            ("narrateur", "Papa tapote la table, tout doux."),
            ("narrateur", "Ça fait un petit toc, comme la pluie."),
            ("papa", "Moi, je chante la gouttière d'abord."),
            ("narrateur", "Papa chante jusqu'au bout."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Je peux chanter ?"),
            ("maman", "Oui."),
            ("maman", "Tu as attendu."),
            ("maman", "Puis on parle."),
            ("narrateur", "Victorino chante tout bas, une petite pluie."),
            ("papa", "Bravo, Victorino."),
            ("papa", "On lève la main, même pour chanter."),
            ("narrateur", "Les moufles bleues bougent un peu, au radiateur."),
        ],
        "dessin": [
            ("narrateur", "Un papier blanc attend, tout lisse."),
            ("narrateur", "Le crayon bleu a encore sa mine cassée."),
            ("maman", "Moi, je dessine le bateau d'abord."),
            ("narrateur", "Maman trace une voile, tout lentement."),
            ("narrateur", "Victorino lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Je peux un trait ?"),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "On peut attendre."),
            ("papa", "Puis on parle."),
            ("narrateur", "Victorino pose un trait bleu, tout court."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
        ],
    }

    extra_act = {
        ("tapis", "histoire"): "Le livre repose sur le tapis gris.",
        ("tapis", "chanson"): "Le tapis étouffe un peu le toc de papa.",
        ("tapis", "dessin"): "Le papier blanc plisse, sur le tapis.",
        ("table", "histoire"): "Le livre glisse un peu, sur le bois.",
        ("table", "chanson"): "La table rend le toc plus clair.",
        ("table", "dessin"): "Le trait bleu brille, sur le bois.",
        ("fenetre", "histoire"): "Le bateau du livre regarde le bateau du rebord.",
        ("fenetre", "chanson"): "La gouttière chante avec papa, dehors.",
        ("fenetre", "dessin"): "La vitre embuée garde un petit trait de doigt.",
    }

    obj_open = {
        "doudou": [
            ("narrateur", "Le doudou est gris, un peu râpé."),
            ("narrateur", "Une oreille est encore chaude."),
            ("narrateur", "Il sent l'orange, tout doux."),
        ],
        "camion": [
            ("narrateur", "Le camion est rouge, tout petit."),
            ("narrateur", "Une roue crisse, tout fin."),
            ("narrateur", "Une goutte de pluie brille sur le toit."),
        ],
        "gobelet": [
            ("narrateur", "Le gobelet est jaune, un peu froid."),
            ("narrateur", "L'eau tremble au fond, tout calme."),
            ("narrateur", "Un reflet de fenêtre y danse."),
        ],
    }

    extra_obj = {
        ("tapis", "histoire", "doudou"): "Le doudou écoute le livre, sur le tapis.",
        ("tapis", "histoire", "camion"): "Le camion se gare près du livre.",
        ("tapis", "histoire", "gobelet"): "Le gobelet jaunit une page, tout doux.",
        ("tapis", "chanson", "doudou"): "Le doudou se berce, avec la chanson.",
        ("tapis", "chanson", "camion"): "La roue du camion crisse, en rythme.",
        ("tapis", "chanson", "gobelet"): "L'eau du gobelet tremble, avec le toc.",
        ("tapis", "dessin", "doudou"): "Le doudou pose l'oreille sur le papier.",
        ("tapis", "dessin", "camion"): "Le camion roule le long du trait bleu.",
        ("tapis", "dessin", "gobelet"): "Une goutte du gobelet manque le papier.",
        ("table", "histoire", "doudou"): "Le doudou s'assoit contre le livre, à table.",
        ("table", "histoire", "camion"): "Le camion attend au bord du bois.",
        ("table", "histoire", "gobelet"): "Le gobelet fait un rond humide, sur la table.",
        ("table", "chanson", "doudou"): "Le doudou tapote le bois, tout léger.",
        ("table", "chanson", "camion"): "Le camion avance d'une roue, puis s'arrête.",
        ("table", "chanson", "gobelet"): "Le gobelet sonne un tout petit ding.",
        ("table", "dessin", "doudou"): "Le doudou garde le papier, à table.",
        ("table", "dessin", "camion"): "Le camion laisse une trace, à côté du trait.",
        ("table", "dessin", "gobelet"): "Le gobelet jaune éclaire le dessin.",
        ("fenetre", "histoire", "doudou"): "Le doudou regarde le bateau du rebord.",
        ("fenetre", "histoire", "camion"): "Le camion se gare sous le bateau en papier.",
        ("fenetre", "histoire", "gobelet"): "Le gobelet reflète la vitre embuée.",
        ("fenetre", "chanson", "doudou"): "Le doudou écoute la gouttière, tout près.",
        ("fenetre", "chanson", "camion"): "Le camion rouge brille, contre la lumière.",
        ("fenetre", "chanson", "gobelet"): "L'eau du gobelet tremble, comme la pluie.",
        ("fenetre", "dessin", "doudou"): "Le doudou tient le papier, près de la vitre.",
        ("fenetre", "dessin", "camion"): "Le camion suit le trait, vers le rebord.",
        ("fenetre", "dessin", "gobelet"): "Le gobelet pose une ombre ronde, sur le dessin.",
    }

    obj_fin_img = {
        "doudou": "Le doudou garde l'oreille chaude, tout calme.",
        "camion": "Le camion s'endort, une roue encore tiède.",
        "gobelet": "L'eau du gobelet ne tremble plus.",
    }

    def l3(lieu: str, act: str, obj: str) -> list[tuple[str, str]]:
        extra = extra_obj[(lieu, act, obj)]
        return (
            obj_open[obj]
            + [
                ("narrateur", f"Victorino a encore {obj_np[obj]}, {lieu_ou[lieu]}."),
                ("narrateur", extra),
                ("narrateur", f"C'était {act_np[act]}."),
                ("papa", "On peut attendre."),
                ("papa", "Puis on parle."),
                ("narrateur", "Victorino lève la main."),
                ("narrateur", "Il attend."),
                ("enfant-m", "Merci, papa."),
                ("maman", "Bravo."),
                ("maman", "Tu as attendu."),
                ("maman", "Puis tu as parlé."),
                ("papa", "C'est du bon travail, Victorino."),
                ("narrateur", f"{obj_np[obj].capitalize()} reste {lieu_ou[lieu]}."),
            ]
        )

    def fin(lieu: str, act: str, obj: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", f"Victorino a choisi {lieu_np[lieu]}, {act_np[act]}, et {obj_np[obj]}."),
            ("papa", "Bravo, Victorino."),
            ("papa", "C'est du bon travail."),
            ("narrateur", obj_fin_img[obj]),
            ("narrateur", "Les moufles bleues sont sèches, maintenant."),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois choses attendent, dans la classe."),
            ("maman", "L'histoire, la chanson, ou le dessin ?"),
            ("papa", "On lève la main."),
            ("papa", "On peut attendre."),
            ("papa", "Puis on parle."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois objets sont là, tout près."),
            ("papa", "Le doudou, le camion, ou le gobelet ?"),
            ("maman", "On peut attendre."),
            ("maman", "Puis on parle."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le radiateur fait tic, tout petit."),
        ("narrateur", "Les moufles bleues sèchent dessus."),
        ("narrateur", "Elles sentent encore la pluie."),
        ("narrateur", "La vitre de la classe est embuée."),
        ("narrateur", "Un bateau en papier attend sur le rebord."),
        ("narrateur", "Dehors, la gouttière chante."),
        ("narrateur", "Ça sent l'orange, dans la poche."),
        ("narrateur", "Papa a glissé le fruit, ce matin."),
        ("papa", "L'orange est pour plus tard, Victorino."),
        ("maman", "Le manteau goutte encore, au portemanteau."),
        ("maman", "Tu as les pieds au sec ?"),
        ("enfant-m", "Oui, maman."),
        ("narrateur", "Le lino a un carré de lumière."),
        ("narrateur", "Un crayon bleu a roulé près d'une table."),
        ("papa", "Tu lèves la main, d'accord ?"),
        ("enfant-m", "D'accord, papa."),
        ("maman", "On peut attendre."),
        ("maman", "Puis on parle."),
        ("narrateur", "En ce moment, Victorino entre dans la classe."),
        ("narrateur", "Le tapis est gris, un peu rêche."),
        ("narrateur", "La table sent le bois."),
        ("narrateur", "La fenêtre tremble un peu, sous la pluie."),
        ("enfant-m", "J'ai une chose à dire."),
        ("papa", "Moi aussi."),
        ("papa", "On peut attendre d'abord."),
        ("narrateur", "Victorino lève la main."),
        ("narrateur", "Il attend."),
        ("narrateur", "Le bateau en papier ne bouge pas."),
    ]
    sons["CHK_T0000_P0000"] = "pluie,radiateur"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Dans la classe, trois endroits attendent."),
        ("maman", "Le tapis, la table, ou la fenêtre ?"),
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
        sons[f"CHK_T0001_{p1}"] = "pluie" if lieu == "fenetre" else ""
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, act in acts.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_act[(lieu, act)]
            by[cid_l2] = act_scene[act] + [
                ("narrateur", extra),
                ("narrateur", f"On est encore {lieu_ou[lieu]}."),
                ("maman", "On peut attendre."),
                ("maman", "Puis on parle."),
            ]
            sons[cid_l2] = {"histoire": "page", "chanson": "", "dessin": "crayon"}[act]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, obj in objets.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, act, obj)
                by[f"{cid_l3}_F0001"] = fin(lieu, act, obj)
                sons[cid_l3] = "camion" if obj == "camion" else ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-031",
        {
            "fil_rouge": (
                "Les moufles sèchent sur le radiateur. Un bateau en papier "
                "attend sur le rebord. Victorino lève la main, il attend, "
                "puis il parle, avec papa et maman."
            ),
            "title": "Les moufles et le bateau en papier",
            "characters": "Victorino, papa, maman",
            "setting": "classe, un matin de pluie",
        },
        by,
        sons,
        max_words=16,
    )


def story_032() -> None:
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    jouets = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}

    lieu_np = {
        "cuisine": "la cuisine",
        "jardin": "le jardin",
        "chambre": "la chambre",
    }
    lieu_vers = {
        "cuisine": "vers la cuisine",
        "jardin": "vers le jardin",
        "chambre": "vers la chambre",
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
            ("narrateur", "Nina pousse la porte de la cuisine."),
            ("narrateur", "Le presse-agrumes brille encore, tout collant."),
            ("narrateur", "Une pelure d'orange fait un petit croissant."),
            ("narrateur", "Le torchon à pois essuie le bois."),
            ("papa", "Bonjour, Nina."),
            ("enfant-f", "Bonjour, papa."),
            ("maman", "Tu veux un coin de pain ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Papa tend un morceau, tout tiède."),
            ("enfant-f", "Merci."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit les mots."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Le pichet d'orange tremble, un peu."),
            ("narrateur", "Ça sent le zeste, tout vif."),
        ],
        "jardin": [
            ("narrateur", "Nina pose un pied sur la dalle mouillée."),
            ("narrateur", "L'étendoir tient un torchon encore humide."),
            ("narrateur", "Une caisse en bois sent l'orange."),
            ("narrateur", "Une pelure flotte dans une flaque."),
            ("maman", "Bonjour, jardin."),
            ("enfant-f", "Bonjour."),
            ("papa", "Tu veux la petite pelle ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Papa tend le manche, tout lisse."),
            ("enfant-f", "Merci, papa."),
            ("maman", "Bravo, Nina."),
            ("maman", "Les mots gentils, dehors aussi."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Une goutte tombe de l'étendoir."),
            ("narrateur", "La dalle est froide sous le pied."),
        ],
        "chambre": [
            ("narrateur", "Nina entre dans la chambre."),
            ("narrateur", "L'abat-jour a des étoiles, tout pâles."),
            ("narrateur", "L'horloge fait tic, tout lent."),
            ("narrateur", "Le dessus de lit sent encore le zeste."),
            ("papa", "Bonjour, petite chambre."),
            ("enfant-f", "Bonjour, papa."),
            ("maman", "Tu veux le coussin ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Maman pose le coussin, tout doux."),
            ("enfant-f", "Merci, maman."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les trois mots."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "Un carré de pluie danse au plafond."),
            ("narrateur", "Nina essuie un doigt encore collant."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Nina veut le pain, dans la cuisine."),
            ("maman", "Que dit-elle ?"),
        ],
        "jardin": [
            ("narrateur", "Nina veut la pelle, dehors."),
            ("papa", "On dit s'il te plaît, merci ?"),
        ],
        "chambre": [
            ("narrateur", "Dans la chambre, Nina a dit bonjour."),
            ("maman", "Et après, on dit merci ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("maman", "Oui."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "Nina croque le pain, tout calme."),
            ("enfant-f", "Merci, maman."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", "La pelure d'orange reste en croissant."),
        ],
        "jardin": [
            ("papa", "Oui."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Nina tient la pelle contre le manteau."),
            ("enfant-f", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Les mots gentils, dans la flaque aussi."),
            ("narrateur", "La pelure tourne, tout lentement."),
        ],
        "chambre": [
            ("maman", "Oui."),
            ("maman", "Bonjour."),
            ("maman", "S'il te plaît."),
            ("maman", "Merci."),
            ("narrateur", "Nina pose la joue sur le coussin."),
            ("enfant-f", "Merci."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "L'horloge fait tic, encore."),
        ],
    }

    jouet_scene = {
        "cubes": [
            ("narrateur", "Nina prend les cubes en bois."),
            ("narrateur", "Ils font clic, l'un contre l'autre."),
            ("narrateur", "Un cube est orange, tout vif."),
            ("papa", "Tu veux le cube orange ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Papa le tend, tout léger."),
            ("enfant-f", "Merci."),
            ("maman", "Bonjour, petit cube."),
            ("enfant-f", "Bonjour."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit les mots."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Le cube orange reste dans la paume."),
        ],
        "livre": [
            ("narrateur", "Nina ouvre le livre."),
            ("narrateur", "Une page sent le papier, un peu sec."),
            ("narrateur", "Un oranger y est dessiné, tout rond."),
            ("maman", "Tu veux que je tourne la page ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Maman tourne, tout doux."),
            ("enfant-f", "Merci, maman."),
            ("papa", "On dit bonjour à l'oranger."),
            ("enfant-f", "Bonjour."),
            ("maman", "Bravo, Nina."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "Une feuille du livre tremble, un peu."),
        ],
        "dinette": [
            ("narrateur", "Nina prend la dînette."),
            ("narrateur", "La petite tasse est froide, tout lisse."),
            ("narrateur", "On dirait du jus, tout orange."),
            ("papa", "Tu veux la tasse ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Papa la pose près d'elle."),
            ("enfant-f", "Merci."),
            ("maman", "On dit bonjour à la tasse."),
            ("enfant-f", "Bonjour."),
            ("maman", "Bravo."),
            ("maman", "Tu as demandé."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", "La petite tasse sonne, tout fin."),
        ],
    }

    extra_jouet = {
        ("cuisine", "cubes"): "Un cube colle un peu, à cause du zeste.",
        ("cuisine", "livre"): "Le livre s'éloigne du pichet, tout prudent.",
        ("cuisine", "dinette"): "La petite tasse imite le pichet, sur le bois.",
        ("jardin", "cubes"): "Un cube se mouille, près de la flaque.",
        ("jardin", "livre"): "Le livre reste à l'abri, sous l'étendoir.",
        ("jardin", "dinette"): "La tasse se pose près de la caisse en bois.",
        ("chambre", "cubes"): "Les cubes clic-cliquent, sous l'abat-jour.",
        ("chambre", "livre"): "Le livre s'ouvre sur le coussin, tout calme.",
        ("chambre", "dinette"): "La tasse attend sur le dessus de lit.",
    }

    moment_open = {
        "matin": [
            ("narrateur", "Le matin, la lumière est pâle."),
            ("narrateur", "Le plancher est un peu froid."),
            ("narrateur", "Un oiseau parle, tout loin."),
            ("narrateur", "Une miette d'orange brille encore, au bord."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, l'air est tiède."),
            ("narrateur", "Un rideau bouge, tout lent."),
            ("narrateur", "La maison est calme, tout douce."),
            ("narrateur", "Nina a une joue un peu chaude."),
        ],
        "soir": [
            ("narrateur", "Le soir, la lampe fait un rond chaud."),
            ("narrateur", "Dehors, un vélo passe, tout loin."),
            ("narrateur", "Ça sent encore l'orange, un peu."),
            ("narrateur", "Le torchon à pois est sec, maintenant."),
        ],
    }

    extra_m = {
        ("cuisine", "cubes", "matin"): "Les cubes brillent, près du pichet du matin.",
        ("cuisine", "cubes", "sieste"): "Un cube orange dort, près du torchon.",
        ("cuisine", "cubes", "soir"): "Les cubes se rangent, sous la lampe.",
        ("cuisine", "livre", "matin"): "L'oranger du livre voit le jus du matin.",
        ("cuisine", "livre", "sieste"): "La page reste ouverte, pendant la sieste.",
        ("cuisine", "livre", "soir"): "Le livre se ferme, près du pain du soir.",
        ("cuisine", "dinette", "matin"): "La petite tasse imite le petit déjeuner.",
        ("cuisine", "dinette", "sieste"): "La tasse attend, pendant que la maison dort.",
        ("cuisine", "dinette", "soir"): "On range la tasse, près du pichet.",
        ("jardin", "cubes", "matin"): "Un cube a une perle de rosée, ce matin.",
        ("jardin", "cubes", "sieste"): "Les cubes sèchent, après la sieste.",
        ("jardin", "cubes", "soir"): "Les cubes rentrent, quand le vélo passe.",
        ("jardin", "livre", "matin"): "Le livre sent l'herbe mouillée, ce matin.",
        ("jardin", "livre", "sieste"): "Le livre reste à l'ombre, après la sieste.",
        ("jardin", "livre", "soir"): "On rentre le livre, sous la lampe du soir.",
        ("jardin", "dinette", "matin"): "La tasse boit la lumière pâle du matin.",
        ("jardin", "dinette", "sieste"): "La tasse se repose, près de la caisse.",
        ("jardin", "dinette", "soir"): "La tasse rentre, avant la nuit.",
        ("chambre", "cubes", "matin"): "Les cubes clic-cliquent, dans la lumière pâle.",
        ("chambre", "cubes", "sieste"): "Les cubes se taisent, après la sieste.",
        ("chambre", "cubes", "soir"): "On range les cubes, sous l'abat-jour.",
        ("chambre", "livre", "matin"): "Le livre s'ouvre, avec l'horloge du matin.",
        ("chambre", "livre", "sieste"): "Le livre reste sur le coussin, tout calme.",
        ("chambre", "livre", "soir"): "On ferme le livre, sous les étoiles de l'abat-jour.",
        ("chambre", "dinette", "matin"): "La tasse dit bonjour, dans la chambre du matin.",
        ("chambre", "dinette", "sieste"): "La tasse attend, tout près du lit.",
        ("chambre", "dinette", "soir"): "On pose la tasse, avant de dormir.",
    }

    moment_img = {
        "matin": "L'oiseau se tait, tout loin.",
        "sieste": "Le rideau ne bouge plus.",
        "soir": "La lampe garde son rond chaud.",
    }

    def l3(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        extra = extra_m[(lieu, jouet, moment)]
        return (
            moment_open[moment]
            + [
                ("narrateur", f"Nina a encore {jouet_np[jouet]}, dans {lieu_np[lieu]}."),
                ("narrateur", extra),
                ("papa", "On dit encore les mots ?"),
                ("enfant-f", "Bonjour."),
                ("enfant-f", "S'il te plaît."),
                ("enfant-f", "Merci."),
                ("maman", "Bravo, Nina."),
                ("maman", "Tu as dit bonjour, s'il te plaît, merci."),
                ("papa", "C'est du bon travail."),
                (
                    "narrateur",
                    "Les cubes restent près d'elle."
                    if jouet == "cubes"
                    else f"{jouet_np[jouet].capitalize()} reste près d'elle.",
                ),
                ("enfant-f", "Merci, papa."),
                ("enfant-f", "Merci, maman."),
            ]
        )

    def fin(lieu: str, jouet: str, moment: str) -> list[tuple[str, str]]:
        return [
            ("maman", "Tu as dit les mots gentils."),
            ("papa", "Bonjour."),
            ("papa", "S'il te plaît."),
            ("papa", "Merci."),
            ("narrateur", f"Nina a choisi {lieu_np[lieu]}, {jouet_np[jouet]}, et {moment_np[moment]}."),
            ("maman", "Bravo, Nina."),
            ("maman", "C'est du bon travail."),
            ("narrateur", moment_img[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout près."),
            ("papa", "Les cubes, le livre, ou la dînette ?"),
            ("maman", "On dit s'il te plaît."),
            ("maman", "Puis merci."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Le jour a trois moments, tout doux."),
            ("maman", "Le matin, après la sieste, ou le soir ?"),
            ("papa", "On dit bonjour, encore."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le presse-agrumes crisse contre l'orange."),
        ("narrateur", "Une goutte de jus glisse sur le bois."),
        ("narrateur", "La table est un peu collante."),
        ("narrateur", "Ça sent le zeste, tout vif."),
        ("narrateur", "Dehors, la pluie tapote le rebord."),
        ("narrateur", "Les chaussures mouillées font un tas, près de la porte."),
        ("narrateur", "Un torchon à pois essuie une flaque."),
        ("papa", "La pulpe est encore chaude, Nina."),
        ("maman", "Tu as vu le torchon à pois ?"),
        ("enfant-f", "Il est bleu et blanc."),
        ("maman", "Oui."),
        ("narrateur", "Papa tourne la manivelle."),
        ("narrateur", "Le jus tombe dans le pichet, tout orange."),
        ("maman", "On dit les mots gentils, ici."),
        ("papa", "Bonjour."),
        ("enfant-f", "Bonjour."),
        ("narrateur", "En ce moment, Nina est dans la cuisine."),
        ("narrateur", "Elle a les doigts un peu collants."),
        ("enfant-f", "Je peux jouer ?"),
        ("maman", "On dit s'il te plaît."),
        ("enfant-f", "S'il te plaît."),
        ("papa", "Voilà."),
        ("enfant-f", "Merci."),
        ("maman", "Bravo, Nina."),
        ("papa", "Bonjour."),
        ("papa", "S'il te plaît."),
        ("papa", "Merci."),
        ("narrateur", "Le pichet brille, près de la fenêtre."),
    ]
    sons["CHK_T0000_P0000"] = "pluie,presse"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "La maison a trois endroits, tout proches."),
        ("maman", "La cuisine, le jardin, ou la chambre ?"),
        ("papa", "On dit bonjour, en arrivant."),
    ]
    sons["CHK_T0001_P0000"] = ""

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = lieu_l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = {"cuisine": "presse", "jardin": "pluie", "chambre": "horloge"}[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, jouet in jouets.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_jouet[(lieu, jouet)]
            by[cid_l2] = [
                ("narrateur", f"Nina reste dans {lieu_np[lieu]}."),
                ("narrateur", f"Elle a choisi {jouet_np[jouet]}."),
            ] + jouet_scene[jouet] + [
                ("narrateur", extra),
                ("maman", "Bonjour."),
                ("maman", "S'il te plaît."),
                ("maman", "Merci."),
            ]
            sons[cid_l2] = {"cubes": "cubes", "livre": "page", "dinette": "tasse"}[jouet]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, moment in moments.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, jouet, moment)
                by[f"{cid_l3}_F0001"] = fin(lieu, jouet, moment)
                sons[cid_l3] = {"matin": "oiseau", "sieste": "", "soir": "velo"}[moment]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-032",
        {
            "fil_rouge": (
                "Le presse-agrumes crisse. Nina a les doigts collants. "
                "Elle dit bonjour, s'il te plaît, merci, avec papa et maman."
            ),
            "title": "Le presse-agrumes de Nina",
            "characters": "Nina, papa, maman",
            "setting": "maison, un jour de pluie, jus d'orange",
        },
        by,
        sons,
        max_words=16,
    )


if __name__ == "__main__":
    story_031()
    story_032()
    print("ok TREE-COL-031 TREE-COL-032")
