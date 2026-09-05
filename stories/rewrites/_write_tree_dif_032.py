#!/usr/bin/env python3
"""TREE-DIF-032 — La cabane de Victorina, sous le drap à pois (N3, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-032"
N3 = 16
TITLE = "La cabane de Victorina, sous le drap à pois"
FIL = (
    "La pluie tapote la chambre. Victorina veut une cabane, ici. "
    "Raphaël est plus grand. Ils emportent le drap à pois, la lampe "
    "et le coussin rond. Sous le lit, entre l'armoire, près de la fenêtre : "
    "trois coins, neuf façons. La cabane est à eux."
)


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            scale, rate = 1.28, "slow"
        else:
            scale, rate = 1.22, "medium"
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Victorina, Raphaël, papa, maman"
    out["setting"] = "chambre sous la pluie : lit, armoire, fenêtre"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tailles différentes",
        "plus petit ou plus grand",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "zoé",
        "zoe",
        "capitaine",
        "plic",
        "volet jaune",
        "pommier",
        "la cuisine",
        "dînette",
        "dinette",
        "après la sieste",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "victorina" not in blob:
        raise SystemExit(f"{SID}: Victorina absente")
    if "raphaël" not in blob and "raphael" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


OBJ = {
    1: {
        "lab": "le drap à pois",
        "cap": "Le drap à pois",
        "t1q": "autour des épaules",
        "t1acc": "épaules | les épaules | autour des épaules | sur les épaules",
        "t1retry": "Le drap est autour des épaules.",
    },
    2: {
        "lab": "la lampe de poche",
        "cap": "La lampe de poche",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "La lampe est dans la poche.",
    },
    3: {
        "lab": "le coussin rond",
        "cap": "Le coussin rond",
        "t1q": "sous le bras",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "Le coussin est sous le bras.",
    },
}

T3_LABS = {
    1: ("le passage de Victorina", "le bord du lit", "soulever le drap"),
    2: ("Victorina devant", "les deux chaises", "un dedans un dehors"),
    3: ("les bras de Raphaël", "le coussin levé", "le rebord ensemble"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorina enroule le drap à pois, tout doux.",
            "enfant-f|Il sent encore le savon.",
            "maman|Glisse-le autour de tes épaules.",
            "narrateur|Les pois froissent contre le pull.",
            "papa|La lampe, ensuite, dans la poche.",
            "narrateur|Raphaël prend le coussin rond.",
            "narrateur|Tout voyage avec eux, dans la pièce.",
            "enfant-f|Raphaël, viens près du lit.",
            "copain|J'arrive, Victorina.",
            "papa|Le drap d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorina prend la lampe de poche, encore tiède.",
            "enfant-f|Elle fait un rond sur le mur.",
            "papa|Glisse-la dans ta poche, tout droit.",
            "narrateur|Un clic, puis une petite lumière.",
            "maman|Le drap, ensuite, autour des épaules.",
            "narrateur|Raphaël prend le coussin rond.",
            "narrateur|Tout voyage avec eux, dans la pièce.",
            "enfant-f|Raphaël va tout voir.",
            "narrateur|Des genoux trop hauts arrivent au tapis.",
            "copain|Me voilà, Victorina.",
            "enfant-f|On fait la cabane, tous les deux ?",
            "maman|La lampe d'abord, elle est prête.",
        )
    return L(
        "narrateur|Victorina tire le coussin rond, tout doux.",
        "enfant-f|Il est tiède, un peu rêche.",
        "maman|Serre-le sous ton bras, tout droit.",
        "narrateur|Le tissu fait un petit pouf.",
        "papa|Le drap et la lampe, avec vous.",
        "narrateur|Il les pose près des chaussettes.",
        "narrateur|Tout voyage avec eux, dans la pièce.",
        "enfant-f|Raphaël, vite !",
        "narrateur|Une ombre trop longue passe au seuil.",
        "copain|J'arrive près du lit.",
        "enfant-f|Je te garde un coin.",
        "papa|Le coussin d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Les épaules portent le drap, tout contre le pull.",
            "copain|Il a trop de pois !",
            "enfant-f|C'est pour notre cabane.",
            "narrateur|Raphaël a les genoux plus hauts que Victorina.",
            "narrateur|Ses pieds touchent déjà le bas du lit.",
            "maman|Il est plus grand, c'est tout.",
            "papa|On reste dans la chambre ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La poche veille près de la lampe.",
            "copain|Je vois le rond !",
            "enfant-f|Ne l'allume pas encore.",
            "narrateur|Raphaël a les cheveux tout courts.",
            "narrateur|Une mèche saute quand il se baisse.",
            "papa|Ça sent déjà le savon, sur le drap.",
            "maman|Vos mains, au-dessus du coussin ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|Le coussin rond cache encore le coude.",
        "copain|Ça sent le savon.",
        "enfant-f|Le coin de départ est là.",
        "narrateur|Le pull de Raphaël s'arrête trop haut.",
        "narrateur|Les manches laissent ses poignets libres.",
        "maman|La chambre est tiède, autour.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Raphaël tapote déjà le tapis, tout léger.",
        "narrateur|Sous le lit, l'ombre est basse.",
        "narrateur|Entre l'armoire et le mur, c'est étroit.",
        "narrateur|Près de la fenêtre, le carreau clignote.",
        "papa|On commence où, pour la cabane ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le drap accroche une latte, tout bas.",
            2: "narrateur|La lampe tape une latte, toc.",
            3: "narrateur|Le coussin bute contre une latte.",
        }[t1]
        mishap = {
            1: "narrateur|Un pois reste coincé dans le bois.",
            2: "narrateur|Le rond de lumière danse sous le sommier.",
            3: "narrateur|Le tissu du coussin prend la poussière.",
        }[t1]
        return L(
            lead,
            "narrateur|Le dessous du lit sent la poussière chaude.",
            "copain|Moi je rentre, Victorina !",
            "narrateur|Raphaël se baisse, trop vite.",
            "narrateur|Ses épaules butent contre le bois.",
            mishap,
            f"enfant-f|{o['cap']} n'attendait pas ça.",
            "maman|Il est trop grand, pour là-dessous.",
            "papa|Toi tu passes, lui pas encore.",
            "copain|On joue comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le drap se coince entre le bois et le mur.",
            2: "narrateur|La lampe glisse, trop vite, dans le passage.",
            3: "narrateur|Le coussin se plie, coincé, contre l'armoire.",
        }[t1]
        mishap = {
            1: "narrateur|Les pois froissent, puis s'arrêtent.",
            2: "narrateur|Le clic de la lampe se perd, au fond.",
            3: "narrateur|Un peu de laine reste collée au bois.",
        }[t1]
        return L(
            lead,
            "enfant-f|Le couloir est à nous, Raphaël.",
            "copain|Je me glisse, trop large !",
            "narrateur|Ses coudes frottent le bois, des deux côtés.",
            mishap,
            "narrateur|Un peu de poussière lève, puis retombe.",
            "maman|Il a les épaules trop larges, c'est tout.",
            "papa|Toi tu es plus mince, lui plus haut.",
            "enfant-f|On peut jouer avec lui ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Le drap pèse trop, vers le carreau mouillé.",
        2: "narrateur|La lampe dessine un rond sur le rideau.",
        3: "narrateur|Le coussin roule vers le rebord froid.",
    }[t1]
    mishap = {
        1: "narrateur|Les pois restent trop bas, sous la tringle.",
        2: "narrateur|Le rond n'atteint pas encore le ciel.",
        3: "narrateur|Le coussin n'aide pas, tout seul, trop bas.",
    }[t1]
    return L(
        lead,
        "enfant-f|Ici, ça clignote, Raphaël.",
        "copain|Je touche le rideau, tout haut !",
        "narrateur|La tringle reste trop loin pour Victorina.",
        mishap,
        f"narrateur|{o['cap']} attend au bord, un peu seule.",
        "maman|Ses bras vont jusqu'à la tringle.",
        "papa|Toi tu vois le carreau, lui le ciel.",
        "copain|On accroche comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le dessous du lit attend encore.",
            "papa|Le passage, le bord, ou soulever le drap ?",
        )
    if t2 == 2:
        return L(
            "narrateur|L'espace étroit attend encore.",
            "maman|Devant, les chaises, ou un dedans un dehors ?",
        )
    return L(
        "narrateur|La tringle attend encore, trop haut.",
        "papa|Les bras, le coussin, ou le rebord ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Victorina pousse le drap sous les lattes.",
            2: "narrateur|Victorina glisse la lampe sous le sommier.",
            3: "narrateur|Victorina pousse le coussin sous le bois.",
        }[t1]
        return L(
            "enfant-f|Je passe, Raphaël.",
            "narrateur|Victorina rampe, tout petite, sous le lit.",
            "copain|Doucement.",
            use,
            "narrateur|Ses doigts trouvent une chaussette perdue.",
            "enfant-f|Je la tiens !",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|La cabane s'ouvre, à leur hauteur.",
            "copain|Regarde, Victorina.",
            "enfant-f|Elle est à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le drap attend au bord, plein d'ombre.",
            2: "narrateur|La lampe attend au bord, un peu ronde.",
            3: "narrateur|Le coussin attend au bord, un peu chaud.",
        }[t1]
        return L(
            "copain|Je reste au bord, moi.",
            "papa|Assieds-toi, Raphaël.",
            "narrateur|Raphaël s'assoit, plus haut que le sommier.",
            "enfant-f|Moi je suis dessous, tout près.",
            "narrateur|Victorina tend les deux mains.",
            "narrateur|La chaussette glisse vers lui.",
            "copain|Elle est à toi, un moment.",
            "maman|Vous la partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        catch = {
            1: "narrateur|Le drap soulève la poussière, tout doux.",
            2: "narrateur|La lampe soulève un rond, tout bas.",
            3: "narrateur|Le coussin soulève un coin, toc.",
        }[t1]
        return L(
            "enfant-f|On soulève un peu.",
            "copain|Moi aussi, je soulève.",
            "narrateur|Raphaël lève le drap du lit, tout haut.",
            "narrateur|Victorina se glisse, pendant l'ouverture.",
            catch,
            "papa|Elle est venue vers vous.",
            "copain|On l'a reprise.",
            "enfant-f|Elle brille encore.",
            "maman|Vos cheveux sentent la poussière.",
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Raphaël pose le drap contre le bois.",
            2: "narrateur|Raphaël pose la lampe contre le bois.",
            3: "narrateur|Raphaël pose le coussin contre le bois.",
        }[t1]
        return L(
            "enfant-f|Je passe devant, tout mince.",
            "copain|Je te tends les affaires.",
            "narrateur|Victorina se glisse, assez étroite.",
            "narrateur|Le couloir de laine s'ouvre, un peu.",
            "enfant-f|Je le tiens !",
            carry,
            "papa|Tes hanches étaient à la bonne largeur.",
            "copain|Passe-le, un peu.",
            "enfant-f|Il sent encore le savon.",
        )
    if t2 == 2 and t3 == 2:
        reach = {
            1: "narrateur|Victorina tend le drap, bras tout courts.",
            2: "narrateur|Victorina tend la lampe, bras tout courts.",
            3: "narrateur|Victorina pousse le coussin, tout près.",
        }[t1]
        return L(
            "enfant-f|On met les chaises, ici.",
            "copain|Une pour toi, une pour moi.",
            reach,
            "narrateur|Deux dossiers font un mur, tout doux.",
            "narrateur|Raphaël voit le fond, Victorina le seuil.",
            "copain|Je le tiens !",
            "maman|Vos chaises ont trouvé le chemin.",
            "enfant-f|Ça sent la laine.",
            "papa|La cabane a deux murs, maintenant.",
        )
    if t2 == 2 and t3 == 3:
        nest = {
            1: "narrateur|Le drap devient un nid, contre l'armoire.",
            2: "narrateur|La lampe devient un nid, contre l'armoire.",
            3: "narrateur|Le coussin devient un nid, contre l'armoire.",
        }[t1]
        return L(
            "enfant-f|Papa, écarte un peu ?",
            "papa|Je fais un chemin, tout doux.",
            "narrateur|La porte de l'armoire s'ouvre, comme une aile.",
            "narrateur|Victorina rentre, Raphaël reste dehors.",
            nest,
            "copain|On se parle à travers.",
            "enfant-f|Oui.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux voix tiennent le même secret.",
        )
    if t2 == 3 and t3 == 1:
        hold = {
            1: "narrateur|Victorina garde le drap au pied.",
            2: "narrateur|Victorina garde la lampe au pied.",
            3: "narrateur|Victorina garde le coussin au pied.",
        }[t1]
        return L(
            "copain|Je me hausse encore.",
            hold,
            "narrateur|Les doigts de Raphaël touchent la tringle.",
            "copain|Elle bouge !",
            "narrateur|Le drap penche, puis s'accroche.",
            "enfant-f|Je tiens le bas.",
            "papa|Tes doigts allaient assez loin.",
            "maman|Victorina tenait bien le bas.",
            "copain|Elle est à nous.",
        )
    if t2 == 3 and t3 == 2:
        up = {
            1: "narrateur|Victorina pose le drap sur le coussin.",
            2: "narrateur|Victorina pose la lampe sur le coussin.",
            3: "narrateur|Victorina pousse le coussin, tout près.",
        }[t1]
        return L(
            "enfant-f|On monte sur le coussin ?",
            "copain|Oui, tout doux.",
            up,
            "narrateur|Papa tient le bois, tout ferme.",
            "narrateur|Victorina et Raphaël se haussent ensemble.",
            "enfant-f|Je vois le ciel !",
            "copain|Je le sens.",
            "maman|Vous avez regardé ensemble.",
            "papa|Le coussin est resté doux.",
        )
    two = {
        1: "narrateur|Raphaël tend le drap, bras tout longs.",
        2: "narrateur|Raphaël tend la lampe, bras tout longs.",
        3: "narrateur|Raphaël pousse le coussin, tout près.",
    }[t1]
    return L(
        "enfant-f|Reste en haut, Raphaël.",
        "copain|Je tends, d'ici.",
        two,
        "narrateur|Raphaël fait basculer le rideau, tout doux.",
        "narrateur|Le rebord prend Victorina, puis lui.",
        "enfant-f|Je le tiens !",
        "papa|Chacun a fait sa part.",
        "copain|Il sent la pluie.",
        "maman|Vos bras n'avaient pas la même longueur.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        keep = {
            1: "narrateur|Le drap à pois couvre encore leurs genoux.",
            2: "narrateur|La lampe de poche fait un rond, tout bas.",
            3: "narrateur|Le coussin rond tient encore leurs coudes.",
        }[t1]
        return L(
            "narrateur|Sous le sommier, la cabane sent le bois.",
            "copain|Tu es passée, moi je gardais.",
            "enfant-f|Tes épaules l'ont laissé ouvert.",
            "papa|Vous l'avez, enfin.",
            "maman|La chaussette dort sur le lit, au calme.",
            keep,
            "enfant-f|On reste un peu, Raphaël.",
            "narrateur|Un rai orange s'endort sur le plafond.",
            "narrateur|La poussière redevient douce, autour.",
        )
    if t2 == 1 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} reste dans la paume de Victorina.",
            2: f"narrateur|{o['cap']} reste dans la paume de Victorina.",
            3: f"narrateur|{o['cap']} reste dans la paume de Victorina.",
        }[t1]
        return L(
            "narrateur|Au bord du lit, deux têtes se calment.",
            "enfant-f|Raphaël, tu l'as vue glisser.",
            "copain|Oui, tout près de tes mains.",
            "papa|Toi assis, elle dessous, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            keep,
            "copain|Je reste encore un peu.",
            "narrateur|Une poussière reste collée aux cheveux.",
            "narrateur|Le tapis sent encore la pluie.",
        )
    if t2 == 1 and t3 == 3:
        keep = {
            1: "narrateur|Le drap à pois retombe, tout léger.",
            2: "narrateur|La lampe de poche retombe, tout léger.",
            3: "narrateur|Le coussin rond retombe, tout léger.",
        }[t1]
        return L(
            "narrateur|Le sommier redescend, tout doux.",
            "copain|Elle est tombée vers nous.",
            "enfant-f|On a soulevé, tous les deux.",
            "maman|Elle n'était plus trop coincée.",
            "papa|Le tissu froisse encore, dans l'air.",
            keep,
            "enfant-f|On souffle dessus, tout calme.",
            "narrateur|Un pois veille près des oreillers.",
            "narrateur|La pluie se tait, contre le carreau.",
        )
    if t2 == 2 and t3 == 1:
        keep = {
            1: "narrateur|Le drap à pois garde un brin de laine.",
            2: "narrateur|La lampe de poche garde un brin de laine.",
            3: "narrateur|Le coussin rond garde un brin de laine.",
        }[t1]
        return L(
            "narrateur|Entre l'armoire et le mur, ça sent le bois.",
            "copain|Mes mains savaient le chemin.",
            "enfant-f|Moi, je passais trop mince.",
            "papa|Vous avez suivi ce qui était à vous.",
            "maman|Un brin de laine reste au pull.",
            keep,
            "enfant-f|Elle est pour demain, la cabane.",
            "copain|Elle est un peu chaude encore.",
            "narrateur|L'ombre de l'armoire s'allonge, puis s'arrête.",
        )
    if t2 == 2 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} garde un brin de laine.",
            2: f"narrateur|{o['cap']} garde un brin de laine.",
            3: f"narrateur|{o['cap']} garde un brin de laine.",
        }[t1]
        return L(
            "narrateur|Les deux chaises restent, comme deux murs.",
            "enfant-f|J'ai poussé d'en bas.",
            "copain|Tes bras étaient assez courts.",
            "maman|La laine sent fort, sur vos mains.",
            "papa|Frottez-les sur le tapis, tout doux.",
            keep,
            "copain|Je le tiens, Victorina.",
            "narrateur|Un dossier grince, puis se tait.",
            "narrateur|Le pois sèche près de la fenêtre.",
        )
    if t2 == 2 and t3 == 3:
        keep = {
            1: "narrateur|Le drap à pois marque encore le carreau.",
            2: "narrateur|La lampe de poche marque encore le carreau.",
            3: "narrateur|Le coussin rond marque encore le carreau.",
        }[t1]
        return L(
            "narrateur|Une voix dedans, une voix dehors, puis plus.",
            "enfant-f|Papa a ouvert un chemin.",
            "copain|On s'est parlé à travers.",
            "papa|L'armoire vous a laissé la place.",
            "maman|Le secret tient encore, tout chaud.",
            keep,
            "enfant-f|Regarde-le, Raphaël, il brille.",
            "copain|Je le vois, d'ici.",
            "narrateur|Le pois reste au chaud, sur le lit.",
        )
    if t2 == 3 and t3 == 1:
        keep = {
            1: "narrateur|Le drap à pois pèse encore sur la tringle.",
            2: "narrateur|La lampe de poche veille encore au pied.",
            3: "narrateur|Le coussin rond veille encore au pied.",
        }[t1]
        return L(
            "narrateur|Les talons de Raphaël sont encore chauds.",
            "enfant-f|Tu l'as fait pencher pour moi.",
            "copain|Tu tenais le bas.",
            "maman|Le rideau sent la pluie, tout près.",
            "papa|La cabane est à vous, maintenant.",
            "narrateur|Victorina la pose contre la vitre.",
            keep,
            "narrateur|Un rai de pluie traverse le pois.",
            "narrateur|Le rideau redevient calme, tout seul.",
        )
    if t2 == 3 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} pose une ombre au carrelage.",
            2: f"narrateur|{o['cap']} pose une ombre au carrelage.",
            3: f"narrateur|{o['cap']} pose une ombre au carrelage.",
        }[t1]
        return L(
            "narrateur|Sur le coussin, deux paires de pieds se touchent.",
            "copain|Tu l'as posée, d'en bas.",
            "enfant-f|Tes bras l'ont fait descendre.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le tissu du coussin sèche déjà.",
            keep,
            "copain|Il brille trop, Victorina.",
            "enfant-f|C'est pour ça.",
            "narrateur|La vitre garde le pois, tout proche.",
        )
    keep = {
        1: "narrateur|Victorina pose le drap au rebord.",
        2: "narrateur|Victorina pose la lampe au rebord.",
        3: "narrateur|Victorina pose le coussin au rebord.",
    }[t1]
    return L(
        "narrateur|Un peu de buée reste au carreau.",
        "enfant-f|On a tiré ensemble.",
        "copain|Sans trop monter.",
        "papa|Le rebord est resté à sa place.",
        "maman|Vos mains sentent encore la pluie.",
        keep,
        "copain|Tu l'as eue, enfin.",
        "enfant-f|Elle est à nous.",
        "narrateur|Le pois tremble un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La pluie tapote le carreau de la chambre.",
        "narrateur|Un rai orange court sur le plafond.",
        "narrateur|Le tapis sent encore le savon du matin.",
        "papa|Tu as vu le halo, Victorina ?",
        "enfant-f|Il tremble, un peu.",
        "maman|Le drap à pois attend sur le lit.",
        "narrateur|En ce moment, Victorina touche le tissu.",
        "enfant-f|Je veux une cabane, ici.",
        "papa|Raphaël arrive, plus grand que toi.",
        "narrateur|Raphaël a les épaules jusqu'à la poignée.",
        "copain|On la fait ensemble ?",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu tiens le drap tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du lit.",
        "narrateur|Le drap, la lampe, et le coussin.",
        "maman|Tu prends quoi d'abord, Victorina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le drap à pois", "la lampe de poche", "le coussin rond")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Victorina a mis {o['lab']} {o['t1q']}.",
            "maman|C'est où, maintenant ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("sous le lit", "entre l'armoire", "près de la fenêtre")
        sons[p] = ""
        sons[f"{p}_T0002_P0000"] = ""

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            sons[sp] = ""
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Victorina veut une cabane dans la chambre, sous la pluie. "
        "Raphaël est plus grand. "
        "T1 = drap à pois / lampe de poche / coussin rond (les trois partent). "
        "T2 = sous le lit (trop bas pour Raphaël) / entre l'armoire "
        "(trop étroit pour ses épaules) / près de la fenêtre "
        "(tringle trop haute pour Victorina). "
        "T3 = neuf résolutions (passage de Victorina, bord du lit, soulever ; "
        "Victorina devant, deux chaises, un dedans un dehors ; "
        "bras de Raphaël, coussin levé, rebord ensemble). "
        "La leçon (tailles, jouer) se vit dans les gestes, sans slogan. "
        "Fin : la cabane est à eux.",
        "N3 ≤ 16. Zoé hors troupe → Victorina + Raphaël (D16). "
        "Cuisine/jardin/chambre et cubes/livre/dînette et matin/sieste/soir jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-024 "
        "(chambre, pas pommier). Un merci de papa lié au geste (tenir le drap). "
        "Pas de « bon travail ». Audio non cuit.",
    )


if __name__ == "__main__":
    main()
