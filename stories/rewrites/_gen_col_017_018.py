#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-017 et TREE-COL-018 (texte seulement)."""
from __future__ import annotations

import json
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
    if sons is None:
        out["sons"] = src.get("sons") or ""
    else:
        out["sons"] = sons
    return out


def write_story(story_id: str, meta: dict, by_id: dict[str, list[tuple[str, str]]], sons_map: dict[str, str]) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:8]} extra={extra[:8]}")
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


def split_extra(extra: str) -> list[tuple[str, str]]:
    parts = [p.strip() for p in extra.replace("? ", "?|").split(". ") if p.strip()]
    out = []
    for p in parts:
        p = p.replace("|", " ")
        if not p.endswith((".", "?", "!")):
            p += "."
        out.append(("narrateur", p))
    return out


def story_017() -> None:
    L = {
        "sable": "le bac à sable",
        "toboggan": "le toboggan",
        "balancoires": "les balançoires",
    }
    LOC = {
        "sable": "près du bac à sable",
        "toboggan": "près du toboggan",
        "balancoires": "près des balançoires",
    }
    T = {
        "ballon": "le ballon",
        "seau": "le seau",
        "doudou": "le doudou",
    }
    O = {
        "galet": "le galet",
        "plume": "la plume",
        "escargot": "l'escargot",
    }

    l1 = {
        "sable": [
            ("narrateur", "Amir s'approche du bac à sable."),
            ("narrateur", "Le sable est frais, un peu gris."),
            ("narrateur", "Un râteau de bois attend, tout petit."),
            ("narrateur", "Des grains collent déjà au lacet."),
            ("papa", "On reste près du bac."),
            ("papa", "Ensuite, l'école."),
            ("enfant-m", "Je veux un château."),
            ("papa", "Oui."),
            ("papa", "Un tout petit château."),
            ("narrateur", "Papa s'assoit sur le bord de bois."),
            ("narrateur", "Le bois est lisse, un peu chaud."),
            ("papa", "À l'école, tu écoutes la maîtresse."),
            ("papa", "Si tu as un malaise, tu racontes à la maison."),
            ("enfant-m", "À maman ?"),
            ("papa", "À maman."),
            ("papa", "Ou à moi."),
            ("narrateur", "Amir pose une poignée de sable."),
            ("narrateur", "Ça sent la terre mouillée, tout doux."),
            ("enfant-m", "J'écoute."),
            ("enfant-m", "Puis je raconte."),
            ("papa", "Bravo, Amir."),
            ("narrateur", "Une miette de pain est là, près du râteau."),
        ],
        "toboggan": [
            ("narrateur", "Amir va vers le toboggan."),
            ("narrateur", "Le métal est un peu froid sous la main."),
            ("narrateur", "Une feuille jaune reste collée, tout haut."),
            ("narrateur", "Le vent la fait bouger, tout peu."),
            ("papa", "On y va doucement."),
            ("papa", "Je suis là."),
            ("enfant-m", "Je glisse ?"),
            ("papa", "Une fois."),
            ("papa", "Puis on parle un peu."),
            ("narrateur", "Amir pose les deux mains."),
            ("narrateur", "Il glisse."),
            ("narrateur", "Le pantalon fait un chuintement."),
            ("papa", "À l'école, tu écoutes la maîtresse."),
            ("papa", "Si tu as un malaise, tu racontes à papa ou maman."),
            ("enfant-m", "Même un tout petit malaise ?"),
            ("papa", "Oui."),
            ("papa", "Même un tout petit."),
            ("narrateur", "La feuille tombe, tout lentement."),
            ("enfant-m", "J'écoute."),
            ("enfant-m", "Ensuite je raconte."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Un chat miaule une fois, derrière le mur."),
        ],
        "balancoires": [
            ("narrateur", "Amir va vers les balançoires."),
            ("narrateur", "Les chaînes font un petit clic."),
            ("narrateur", "Le siège est lisse, un peu froid."),
            ("narrateur", "Une goutte brille encore dessus."),
            ("papa", "Tu t'assoies."),
            ("papa", "Moi, je pousse tout doux."),
            ("enfant-m", "Pas trop haut."),
            ("papa", "Pas trop haut."),
            ("narrateur", "Les chaussures d'Amir font toc toc, tout près du sol."),
            ("papa", "À l'école, tu écoutes la maîtresse."),
            ("papa", "Si tu as un malaise, tu viens raconter à la maison."),
            ("enfant-m", "Maman m'écoute aussi ?"),
            ("papa", "Oui."),
            ("papa", "Maman t'écoute."),
            ("papa", "Moi aussi."),
            ("narrateur", "Amir serre la chaîne, tout chaud dans la main."),
            ("enfant-m", "J'écoute la maîtresse."),
            ("enfant-m", "Puis je raconte."),
            ("papa", "Bravo."),
            ("narrateur", "Une flaque tremble, sous la balançoire."),
        ],
    }

    q = {
        "sable": [
            ("narrateur", "Amir a un malaise."),
            ("papa", "Il raconte à qui ?"),
        ],
        "toboggan": [
            ("narrateur", "À l'école, Amir écoute."),
            ("papa", "S'il a un malaise, il fait quoi ?"),
        ],
        "balancoires": [
            ("narrateur", "Amir sent un malaise."),
            ("maman", "Il vient raconter à la maison ?"),
        ],
    }

    conf = {
        "sable": [
            ("papa", "Oui."),
            ("papa", "Tu racontes à papa ou maman."),
            ("narrateur", "Amir souffle un peu."),
            ("narrateur", "Le sable retombe entre ses doigts."),
            ("enfant-m", "J'écoute la maîtresse."),
            ("enfant-m", "Puis je raconte."),
            ("papa", "Bravo, Amir."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Le râteau de bois reste calme."),
            ("maman", "On t'écoute, à la maison."),
        ],
        "toboggan": [
            ("papa", "Oui."),
            ("papa", "Tu racontes à la maison."),
            ("narrateur", "Amir essuie ses mains sur son manteau jaune."),
            ("narrateur", "Le tissu est encore un peu humide."),
            ("enfant-m", "Même un petit malaise."),
            ("papa", "Même un petit."),
            ("papa", "On t'écoute."),
            ("maman", "Bravo."),
            ("narrateur", "La feuille jaune est dans l'herbe, maintenant."),
            ("papa", "On continue un peu, ensemble."),
        ],
        "balancoires": [
            ("maman", "Oui."),
            ("maman", "Tu viens raconter à la maison."),
            ("narrateur", "La chaîne ne clic plus."),
            ("narrateur", "Amir pose un pied à terre."),
            ("enfant-m", "J'écoute."),
            ("enfant-m", "Ensuite je raconte."),
            ("papa", "Bravo, Amir."),
            ("papa", "Tu as bien retenu."),
            ("narrateur", "La goutte a glissé du siège."),
            ("papa", "On a encore un petit moment."),
        ],
    }

    toy_scene = {
        "ballon": [
            ("narrateur", "Amir prend le ballon."),
            ("narrateur", "Le ballon est un peu sablé."),
            ("narrateur", "Il fait poum contre le genou."),
            ("papa", "On joue ici."),
            ("papa", "Le ballon reste près de nous."),
            ("enfant-m", "À moi ?"),
            ("papa", "À toi."),
            ("papa", "Tout doux."),
            ("narrateur", "Amir tient le ballon contre son ventre."),
            ("papa", "À l'école, tu écoutes la maîtresse."),
            ("papa", "Si malaise, tu racontes à la maison."),
            ("enfant-m", "D'accord, papa."),
            ("papa", "Bravo."),
        ],
        "seau": [
            ("narrateur", "Amir prend le seau rouge."),
            ("narrateur", "Un peu d'eau tremble au fond."),
            ("narrateur", "Le plastique est tiède, au soleil."),
            ("papa", "On verse tout doucement."),
            ("enfant-m", "Ça fait ploc."),
            ("papa", "Oui."),
            ("papa", "Un petit ploc."),
            ("narrateur", "Papa tient le bord du seau."),
            ("papa", "Tu écoutes la maîtresse, à l'école."),
            ("papa", "Si tu as un malaise, tu racontes à papa ou maman."),
            ("enfant-m", "Je raconte."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Une goutte coule sur le pouce d'Amir."),
        ],
        "doudou": [
            ("narrateur", "Amir sort le doudou du sac."),
            ("narrateur", "Le doudou sent encore la maison."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("papa", "Il t'attendait."),
            ("enfant-m", "Il a chaud."),
            ("papa", "Oui."),
            ("papa", "Comme toi."),
            ("narrateur", "Amir le serre, tout près du manteau jaune."),
            ("papa", "À l'école, on écoute la maîtresse."),
            ("papa", "Si malaise, on raconte à la maison."),
            ("enfant-m", "Le doudou peut venir ?"),
            ("papa", "Le doudou reste dans le sac."),
            ("papa", "Toi, tu racontes, ce soir."),
            ("maman", "On t'écoute, tous les deux."),
        ],
    }

    extra_toy = {
        ("sable", "ballon"): "Des grains de sable collent au ballon.",
        ("sable", "seau"): "Le seau laisse un rond humide dans le sable.",
        ("sable", "doudou"): "Le doudou a un peu de sable sur le ventre.",
        ("toboggan", "ballon"): "Le ballon roule jusqu'au pied du toboggan.",
        ("toboggan", "seau"): "Le seau sonne creux, près du métal.",
        ("toboggan", "doudou"): "Le doudou regarde le toboggan, tout calme.",
        ("balancoires", "ballon"): "Le ballon fait poum, sous la balançoire.",
        ("balancoires", "seau"): "Le seau tremble un peu, quand la chaîne clic.",
        ("balancoires", "doudou"): "Le doudou est sur les genoux, pendant que ça balance.",
    }

    obj_open = {
        "galet": [
            ("narrateur", "Le galet est chaud, tout lisse."),
            ("narrateur", "Il a une tache jaune, comme le manteau."),
            ("narrateur", "Amir le pose dans sa paume."),
        ],
        "plume": [
            ("narrateur", "La plume est grise, tout légère."),
            ("narrateur", "Elle chatouille le doigt d'Amir."),
            ("narrateur", "Le vent veut l'emporter, tout doux."),
        ],
        "escargot": [
            ("narrateur", "L'escargot avance, tout lent."),
            ("narrateur", "Sa coquille est brune, un peu brillante."),
            ("narrateur", "Un fil d'argent reste sur la pierre."),
        ],
    }

    extras = {
        ("sable", "ballon", "galet"): "Le galet fait un petit creux, près du ballon.",
        ("sable", "ballon", "plume"): "La plume se pose sur le ballon, puis s'envole.",
        ("sable", "ballon", "escargot"): "L'escargot contourne le ballon, pas à pas.",
        ("sable", "seau", "galet"): "Amir glisse le galet au fond du seau.",
        ("sable", "seau", "plume"): "La plume flotte un instant, dans l'eau du seau.",
        ("sable", "seau", "escargot"): "L'escargot s'arrête loin du seau, tout sage.",
        ("sable", "doudou", "galet"): "Le galet chauffe, contre le doudou.",
        ("sable", "doudou", "plume"): "La plume colle un peu au doudou.",
        ("sable", "doudou", "escargot"): "L'escargot passe près du doudou, sans le toucher.",
        ("toboggan", "ballon", "galet"): "Le galet reste au pied du toboggan, près du ballon.",
        ("toboggan", "ballon", "plume"): "La plume glisse sur le métal, puis sur le ballon.",
        ("toboggan", "ballon", "escargot"): "L'escargot est sur la pierre, loin du ballon.",
        ("toboggan", "seau", "galet"): "Le galet fait toc, contre le seau.",
        ("toboggan", "seau", "plume"): "La plume tremble au bord du seau.",
        ("toboggan", "seau", "escargot"): "L'escargot boit une goutte, tout loin du seau.",
        ("toboggan", "doudou", "galet"): "Le doudou tient le galet, tout calme.",
        ("toboggan", "doudou", "plume"): "La plume est derrière l'oreille du doudou.",
        ("toboggan", "doudou", "escargot"): "L'escargot et le doudou se regardent, tout doux.",
        ("balancoires", "ballon", "galet"): "Le galet brille dans la flaque, près du ballon.",
        ("balancoires", "ballon", "plume"): "La plume tourne, sous la balançoire, près du ballon.",
        ("balancoires", "ballon", "escargot"): "L'escargot grimpe une pierre, loin du ballon.",
        ("balancoires", "seau", "galet"): "Le galet cloche au fond du seau, tout bas.",
        ("balancoires", "seau", "plume"): "La plume sèche au bord du seau.",
        ("balancoires", "seau", "escargot"): "L'escargot évite le seau, pas à pas.",
        ("balancoires", "doudou", "galet"): "Le doudou et le galet se tiennent, sur les genoux.",
        ("balancoires", "doudou", "plume"): "La plume chatouille le doudou, puis s'arrête.",
        ("balancoires", "doudou", "escargot"): "L'escargot s'est arrêté, près du doudou.",
    }

    fin_image = {
        "galet": "Le galet reste chaud, au fond de la poche.",
        "plume": "La plume s'envole un peu, puis se pose.",
        "escargot": "L'escargot reprend le mur, tout lent.",
    }

    def l3(lieu: str, toy: str, obj: str) -> list[tuple[str, str]]:
        return (
            obj_open[obj]
            + split_extra(extras[(lieu, toy, obj)])
            + [
                ("narrateur", f"Amir a encore {T[toy]}, {LOC[lieu]}."),
                ("papa", "On a joué un peu."),
                ("papa", "Maintenant, l'école."),
                ("enfant-m", "J'écoute la maîtresse."),
                ("enfant-m", "Si malaise, je raconte à la maison."),
                ("papa", "Oui."),
                ("papa", "À maman, ou à moi."),
                ("papa", "Bravo, Amir."),
                ("maman", "On t'écoute, ce soir."),
                ("enfant-m", "Merci, papa."),
                ("narrateur", "La poire attend dans le sac."),
                ("narrateur", "Les manches jaunes sont presque sèches."),
            ]
        )

    def fin(lieu: str, toy: str, obj: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "J'ai écouté papa."),
            ("enfant-m", "Ensuite, j'écoute la maîtresse."),
            ("papa", "Bravo, Amir."),
            ("papa", "C'est du bon travail."),
            ("maman", "Ce soir, on t'écoute."),
            ("narrateur", f"Amir a vu {L[lieu]}."),
            ("narrateur", f"Il a tenu {T[toy]}."),
            ("narrateur", f"Il a regardé {O[obj]}."),
            ("narrateur", fin_image[obj]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Dans le sac, trois choses attendent."),
            ("papa", "Le ballon, le seau, ou le doudou ?"),
            ("papa", "On joue un peu."),
            ("maman", "Ensuite, tu écoutes, à l'école."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Au bord du parc, trois petites choses."),
            ("papa", "Le galet, la plume, ou l'escargot ?"),
            ("papa", "On regarde."),
            ("papa", "Puis on va à l'école."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le volet de la boulangerie claque, tout doux."),
        ("narrateur", "Ça sent le pain chaud, dans la rue."),
        ("narrateur", "Une flaque tient un nuage, tout blanc."),
        ("narrateur", "Les manches jaunes d'Amir sont encore un peu humides."),
        ("narrateur", "Les clés de papa font un petit tintement."),
        ("narrateur", "Maman a glissé une poire dans le sac."),
        ("maman", "La poire est pour plus tard, Amir."),
        ("maman", "Tu écoutes la maîtresse, à l'école."),
        ("papa", "Si tu as un malaise, tu racontes à la maison."),
        ("enfant-m", "D'accord, maman."),
        ("narrateur", "Un escargot grimpe le mur, tout lent."),
        ("papa", "Regarde."),
        ("papa", "Il prend son temps."),
        ("narrateur", "En ce moment, Amir et papa s'arrêtent."),
        ("narrateur", "Le petit parc est là, avant l'école."),
        ("narrateur", "Le bac à sable, le toboggan, les balançoires."),
        ("papa", "On a un tout petit moment."),
        ("papa", "Ensuite, l'école."),
        ("enfant-m", "Je veux jouer un peu."),
        ("papa", "Oui."),
        ("papa", "Puis tu écoutes, à l'école."),
        ("narrateur", "Une miette de pain est tombée, près du bac."),
        ("narrateur", "Le vent sent encore le four."),
    ]
    sons["CHK_T0000_P0000"] = "pain,oiseau"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Le petit parc a trois coins."),
        ("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ("maman", "On joue un peu."),
        ("papa", "Ensuite, tu écoutes la maîtresse."),
    ]
    sons["CHK_T0001_P0000"] = ""

    lieux = {"P0001": "sable", "P0002": "toboggan", "P0003": "balancoires"}
    toys = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    objs = {"P0001": "galet", "P0002": "plume", "P0003": "escargot"}

    sons_l1 = {"sable": "", "toboggan": "chat", "balancoires": "chaussures"}
    sons_toy = {"ballon": "ballon", "seau": "goutte", "doudou": ""}
    sons_obj = {"galet": "", "plume": "oiseau", "escargot": ""}

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = sons_l1[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, toy in toys.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = toy_scene[toy] + split_extra(extra_toy[(lieu, toy)]) + [
                ("narrateur", f"On est encore {LOC[lieu]}."),
                ("papa", "On écoute la maîtresse, après."),
                ("papa", "Si malaise, on raconte à la maison."),
            ]
            sons[cid_l2] = sons_toy[toy]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, obj in objs.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, toy, obj)
                by[f"{cid_l3}_F0001"] = fin(lieu, toy, obj)
                sons[cid_l3] = sons_obj[obj]
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-017",
        {
            "fil_rouge": "Un escargot grimpe le mur de la boulangerie. Amir s'arrête au petit parc avec papa. Il joue un peu. À l'école, il écoutera la maîtresse. S'il a un malaise, il racontera à la maison.",
            "title": "L'escargot de la boulangerie",
            "characters": "Amir, papa, maman",
            "setting": "rue, boulangerie, petit parc avant l'école",
        },
        by,
        sons,
    )


def story_018() -> None:
    L = {
        "tapis": "le tapis",
        "table": "la table",
        "preau": "le préau",
    }
    SOUV_L = {
        "tapis": "du tapis",
        "table": "de la table",
        "preau": "du préau",
    }
    A = {
        "histoire": "l'histoire",
        "dessin": "le dessin",
        "chanson": "la chanson",
    }
    SOUV_A = {
        "histoire": "de l'histoire",
        "dessin": "du dessin",
        "chanson": "de la chanson",
    }
    Q = {
        "maman": "maman",
        "papa": "papa",
        "doudou": "le doudou",
    }

    l1 = {
        "tapis": [
            ("narrateur", "Nina s'assoit sur le tapis."),
            ("narrateur", "La laine est chaude, sous les genoux."),
            ("narrateur", "Le rond de soleil a bougé, un peu."),
            ("maitresse", "On écoute, sur le tapis."),
            ("narrateur", "Nina écoute."),
            ("narrateur", "Un camarade se penche."),
            ("narrateur", "Il chuchote, tout près."),
            ("narrateur", "Nina sent un malaise."),
            ("narrateur", "Son ventre se serre, tout petit."),
            ("narrateur", "Elle reste sur le tapis."),
            ("narrateur", "Elle écoute encore la maîtresse."),
            ("enfant-f", "Ce soir, je raconte."),
            ("maman", "Tu écoutes."),
            ("maman", "Si malaise, tu racontes à la maison."),
            ("maitresse", "Merci, Nina."),
            ("maitresse", "Tu as écouté."),
            ("narrateur", "Le tapis chatouille encore un genou."),
        ],
        "table": [
            ("narrateur", "Nina s'assoit à la table."),
            ("narrateur", "Le bois a des lignes, tout fines."),
            ("narrateur", "Un crayon jaune attend, tout lisse."),
            ("maitresse", "On écoute, à la table."),
            ("narrateur", "Nina écoute."),
            ("narrateur", "Un mot la gêne, tout bas."),
            ("narrateur", "C'est un chuchotement."),
            ("narrateur", "Nina a un malaise."),
            ("narrateur", "Ses mains deviennent chaudes."),
            ("narrateur", "Elle pose le crayon, tout droit."),
            ("narrateur", "Elle écoute la maîtresse, jusqu'au bout."),
            ("papa", "Si tu as un malaise, tu racontes à la maison."),
            ("enfant-f", "Je raconte à papa."),
            ("enfant-f", "Ou à maman."),
            ("maitresse", "Oui."),
            ("maitresse", "D'abord, on écoute ici."),
            ("narrateur", "Le crayon reste tiède, sous le doigt."),
        ],
        "preau": [
            ("narrateur", "Nina va au préau."),
            ("narrateur", "Les carreaux sont froids, un peu humides."),
            ("narrateur", "Une goutte tombe du toit, tout loin."),
            ("maitresse", "On écoute, au préau."),
            ("narrateur", "Nina écoute."),
            ("narrateur", "Un camarade parle tout bas."),
            ("narrateur", "Le ventre de Nina se serre."),
            ("narrateur", "Elle respire."),
            ("narrateur", "Elle reste près de la maîtresse."),
            ("maman", "Papa t'écoute, à la maison."),
            ("maman", "Moi aussi."),
            ("enfant-f", "Ce soir, je raconte."),
            ("maitresse", "Tu as bien écouté."),
            ("narrateur", "La goutte fait encore un ploc, tout petit."),
            ("narrateur", "Nina garde les mains dans ses poches."),
        ],
    }

    q = {
        "tapis": [
            ("narrateur", "Sur le tapis, Nina a un malaise."),
            ("maman", "Que fait-elle ?"),
        ],
        "table": [
            ("narrateur", "À la table, Nina a un malaise."),
            ("papa", "Que fait-elle ?"),
        ],
        "preau": [
            ("narrateur", "Au préau, Nina a un malaise."),
            ("maman", "Que fait-elle ?"),
        ],
    }

    conf = {
        "tapis": [
            ("maman", "Oui."),
            ("maman", "Elle raconte à la maison."),
            ("narrateur", "Nina souffle un peu."),
            ("narrateur", "Le rond de soleil a encore bougé."),
            ("enfant-f", "J'écoute."),
            ("enfant-f", "Puis je raconte."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "La laine du tapis redevient douce."),
        ],
        "table": [
            ("papa", "Oui."),
            ("papa", "On écoute."),
            ("papa", "Si malaise, on raconte à la maison."),
            ("narrateur", "Nina essuie ses mains sur sa robe."),
            ("narrateur", "Le tissu est un peu rêche."),
            ("enfant-f", "J'ai écouté."),
            ("maman", "Et tu nous racontes."),
            ("maman", "Bravo."),
            ("narrateur", "Le crayon jaune reste sur la table."),
        ],
        "preau": [
            ("maman", "Oui."),
            ("maman", "Nina a écouté."),
            ("maman", "Elle raconte à la maison."),
            ("narrateur", "Nina lève les yeux."),
            ("narrateur", "Le toit du préau est gris, tout calme."),
            ("enfant-f", "Je raconte ce soir."),
            ("papa", "On t'écoute."),
            ("papa", "Bravo, Nina."),
            ("narrateur", "La goutte s'est arrêtée."),
        ],
    }

    act_scene = {
        "histoire": [
            ("narrateur", "La maîtresse ouvre le livre."),
            ("narrateur", "Il y a un renard, tout roux."),
            ("narrateur", "Une page sent encore l'encre."),
            ("maitresse", "On écoute l'histoire."),
            ("narrateur", "Nina écoute."),
            ("narrateur", "Le malaise est encore là, tout petit."),
            ("narrateur", "Elle reste sage."),
            ("narrateur", "Elle écoute jusqu'au bout."),
            ("enfant-f", "Je raconte à la maison."),
            ("maman", "Oui."),
            ("maman", "On t'écoute."),
        ],
        "dessin": [
            ("narrateur", "Nina prend le crayon jaune."),
            ("narrateur", "Le bois est lisse, un peu chaud."),
            ("narrateur", "Elle dessine un rond, comme le soleil."),
            ("maitresse", "On écoute, pendant le dessin."),
            ("narrateur", "Nina écoute."),
            ("narrateur", "Le malaise serre encore un peu."),
            ("narrateur", "Elle pose le crayon, tout droit."),
            ("enfant-f", "Ce soir, je raconte."),
            ("papa", "Tu as écouté."),
            ("papa", "Ensuite, tu racontes."),
            ("narrateur", "Le rond jaune brille sur le papier."),
        ],
        "chanson": [
            ("narrateur", "La maîtresse tape deux fois dans les mains."),
            ("narrateur", "La chanson est douce, tout simple."),
            ("maitresse", "On écoute la chanson."),
            ("narrateur", "Nina écoute."),
            ("narrateur", "Elle ne chuchote pas."),
            ("narrateur", "Le malaise reste, tout petit."),
            ("enfant-f", "Je raconte à maman."),
            ("enfant-f", "Ou à papa."),
            ("maman", "Oui."),
            ("maman", "Si malaise, tu racontes à la maison."),
            ("narrateur", "Les mains de Nina se posent sur ses genoux."),
        ],
    }

    extra_act = {
        ("tapis", "histoire"): "Le renard du livre est assis, comme sur le tapis.",
        ("tapis", "dessin"): "Le rond jaune ressemble au soleil du tapis.",
        ("tapis", "chanson"): "La chanson fait un peu danser la laine.",
        ("table", "histoire"): "Le livre est ouvert, au milieu de la table.",
        ("table", "dessin"): "Le crayon roule d'un doigt, sur la table.",
        ("table", "chanson"): "La table vibre un peu, avec la chanson.",
        ("preau", "histoire"): "Le vent tourne une page, au préau.",
        ("preau", "dessin"): "Le papier claque un peu, au préau.",
        ("preau", "chanson"): "La chanson revient en écho, sous le toit.",
    }

    qui_open = {
        "maman": [
            ("narrateur", "Le soir, la cuisine sent la soupe."),
            ("narrateur", "La louche fait un petit bruit, contre la casserole."),
            ("narrateur", "Nina rejoint maman."),
            ("maman", "Te voilà, Nina."),
            ("maman", "Tu as faim ?"),
            ("enfant-f", "Un peu."),
        ],
        "papa": [
            ("narrateur", "Le soir, la lampe fait un rond jaune."),
            ("narrateur", "Papa est dans le fauteuil."),
            ("narrateur", "Nina rejoint papa."),
            ("papa", "Viens."),
            ("papa", "On a le temps."),
            ("enfant-f", "J'ai quelque chose."),
        ],
        "doudou": [
            ("narrateur", "Le soir, le doudou attend sur le lit."),
            ("narrateur", "Il est tiède, un peu froissé."),
            ("narrateur", "Nina le serre."),
            ("enfant-f", "Toi d'abord."),
            ("narrateur", "Puis elle va vers papa et maman."),
            ("maman", "On t'écoute."),
        ],
    }

    extras = {
        ("tapis", "histoire", "maman"): "Nina revoit le renard du livre, près de la soupe.",
        ("tapis", "histoire", "papa"): "Nina revoit le tapis, dans le rond de la lampe.",
        ("tapis", "histoire", "doudou"): "Le doudou a l'air d'écouter l'histoire, lui aussi.",
        ("tapis", "dessin", "maman"): "Le rond jaune est encore dans sa tête, près de la soupe.",
        ("tapis", "dessin", "papa"): "Nina a un peu de jaune au doigt, sous la lampe.",
        ("tapis", "dessin", "doudou"): "Le doudou a un trait jaune, tout petit, sur l'oreille.",
        ("tapis", "chanson", "maman"): "Nina chante un mot, tout bas, près de maman.",
        ("tapis", "chanson", "papa"): "Papa reconnaît la chanson, tout doux.",
        ("tapis", "chanson", "doudou"): "Le doudou balance un peu, comme la chanson.",
        ("table", "histoire", "maman"): "Nina pose le livre dans sa tête, près de l'assiette.",
        ("table", "histoire", "papa"): "Papa écoute l'histoire de Nina, jusqu'au bout.",
        ("table", "histoire", "doudou"): "Le doudou est sur la table de la cuisine, tout sage.",
        ("table", "dessin", "maman"): "Maman regarde le rond jaune, dans les mots de Nina.",
        ("table", "dessin", "papa"): "Papa dit que le rond est beau, tout simple.",
        ("table", "dessin", "doudou"): "Le doudou tient le crayon, dans le récit de Nina.",
        ("table", "chanson", "maman"): "Maman tapote la casserole, comme la chanson.",
        ("table", "chanson", "papa"): "Papa tapote le fauteuil, tout doux.",
        ("table", "chanson", "doudou"): "Le doudou a entendu la chanson, tout près.",
        ("preau", "histoire", "maman"): "Nina raconte le préau, et le renard du livre.",
        ("preau", "histoire", "papa"): "Papa entend encore le ploc, dans l'histoire.",
        ("preau", "histoire", "doudou"): "Le doudou a une goutte imaginaire, sur le nez.",
        ("preau", "dessin", "maman"): "Nina dessine le préau, avec des mots.",
        ("preau", "dessin", "papa"): "Papa voit le toit gris, dans le dessin raconté.",
        ("preau", "dessin", "doudou"): "Le doudou a froid, comme les carreaux du préau.",
        ("preau", "chanson", "maman"): "La chanson du préau revient, près de la soupe.",
        ("preau", "chanson", "papa"): "Papa écoute l'écho, dans la voix de Nina.",
        ("preau", "chanson", "doudou"): "Le doudou connaît le rythme, tout petit.",
    }

    fin_image = {
        "maman": "La soupe fume encore, tout doux.",
        "papa": "La lampe reste allumée, un moment.",
        "doudou": "Le doudou s'endort contre l'épaule.",
    }

    def l3(lieu: str, act: str, qui: str) -> list[tuple[str, str]]:
        return (
            qui_open[qui]
            + split_extra(extras[(lieu, act, qui)])
            + [
                ("narrateur", f"Nina se souvient {SOUV_L[lieu]}."),
                ("narrateur", f"Elle se souvient {SOUV_A[act]}."),
                ("enfant-f", "Papa."),
                ("enfant-f", "Maman."),
                ("enfant-f", "J'ai eu un malaise."),
                ("enfant-f", "Un camarade a chuchoté."),
                ("enfant-f", "J'ai écouté la maîtresse."),
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

    def fin(lieu: str, act: str, qui: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "J'ai écouté."),
            ("enfant-f", "Puis j'ai raconté."),
            ("maman", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Nina a écouté { { 'tapis': 'sur le tapis', 'table': 'à la table', 'preau': 'au préau' }[lieu] }."),
            ("narrateur", f"Elle a vécu {A[act]}."),
            ("narrateur", f"Le soir, elle a rejoint {Q[qui]}."),
            ("narrateur", fin_image[qui]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois choses encore, dans la classe."),
            ("maitresse", "L'histoire, le dessin, ou la chanson ?"),
            ("maman", "On écoute."),
            ("papa", "Ensuite, si malaise, on raconte à la maison."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Le soir, à la maison, trois chemins."),
            ("maman", "Maman, papa, ou le doudou ?"),
            ("papa", "On t'écoute."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Les patères font une rangée de bois."),
        ("narrateur", "Le manteau bleu de Nina est encore tiède."),
        ("narrateur", "Ça sent la colle d'hier, tout doux."),
        ("narrateur", "La fenêtre est un peu embuée."),
        ("narrateur", "Un rond de soleil dort sur le tapis."),
        ("narrateur", "Maman a serré la main de Nina, près de la porte."),
        ("maman", "Bonne journée, Nina."),
        ("maman", "Tu écoutes la maîtresse."),
        ("papa", "Si tu as un malaise, tu viens raconter à la maison."),
        ("enfant-f", "D'accord."),
        ("narrateur", "En ce moment, la maîtresse tapote la table."),
        ("narrateur", "Un petit toc, tout net."),
        ("maitresse", "On s'assoit."),
        ("maitresse", "On écoute."),
        ("narrateur", "Nina aime écouter."),
        ("narrateur", "Le tapis, la table, le préau attendent."),
        ("narrateur", "Un camarade se penche déjà, tout près."),
        ("narrateur", "Nina sent son ventre, tout calme encore."),
    ]
    sons["CHK_T0000_P0000"] = "porte"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "On peut s'asseoir à trois endroits."),
        ("maitresse", "Le tapis, la table, ou le préau ?"),
        ("maman", "Tu écoutes."),
        ("papa", "Si malaise, tu racontes à la maison."),
    ]
    sons["CHK_T0001_P0000"] = ""

    lieux = {"P0001": "tapis", "P0002": "table", "P0003": "preau"}
    acts = {"P0001": "histoire", "P0002": "dessin", "P0003": "chanson"}
    quis = {"P0001": "maman", "P0002": "papa", "P0003": "doudou"}

    sons_l1 = {"tapis": "", "table": "", "preau": "goutte"}
    sons_act = {"histoire": "", "dessin": "", "chanson": "chanson"}

    for p1, lieu in lieux.items():
        by[f"CHK_T0001_{p1}"] = l1[lieu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[lieu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[lieu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = sons_l1[lieu]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, act in acts.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = act_scene[act] + split_extra(extra_act[(lieu, act)]) + [
                ("narrateur", f"Nina garde {L[lieu]} dans sa tête."),
                ("maman", "On écoute la maîtresse."),
                ("maman", "Si malaise, raconter à la maison."),
            ]
            sons[cid_l2] = sons_act[act]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, qui in quis.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(lieu, act, qui)
                by[f"{cid_l3}_F0001"] = fin(lieu, act, qui)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-018",
        {
            "fil_rouge": "Un rond de soleil dort sur le tapis. Nina écoute la maîtresse. Un chuchotement serre son ventre. Le soir, elle raconte à papa et maman.",
            "title": "Le rond de soleil sur le tapis",
            "characters": "Nina, maman, papa",
            "setting": "école, puis la maison le soir",
        },
        by,
        sons,
    )


if __name__ == "__main__":
    story_017()
    story_018()
    print("ok")
