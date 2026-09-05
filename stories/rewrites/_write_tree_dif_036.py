#!/usr/bin/env python3
"""TREE-DIF-036 — Le poisson de bois de Raphaël au lavoir (N2, DIF.COR.003)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-036"
N2 = LIMITS["N2"]
TITLE = "Le poisson de bois de Raphaël au lavoir"
FIL = (
    "Raphaël veut que son poisson de bois nage dans l'eau du village. "
    "Aniss arrive, lunettes encore floues, cheveux mouillés, manteau jaune "
    "trop long. Ils emportent le poisson, le filet vert et le seau bleu. "
    "Au bassin la buée cache l'eau, au ruisseau les mèches tombent, "
    "aux géraniums les manches trempent. Ils jouent ensemble. "
    "Le poisson rentre dans la poche, encore mouillé."
)
CHARS = "Raphaël, Aniss, papa, maman"
SETTING = "lavoir du village après la pluie : bassin, ruisseau, géraniums"


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
    out["characters"] = CHARS
    out["setting"] = SETTING
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
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "pas rire",
        "hugo",
        "zoé",
        "zoe",
        "sami",
        "léa",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "tarte",
        "théâtre",
        "theatre",
        "marionnette",
        "chambre",
        "potager",
        "tomate",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "raphaël" not in blob and "raphael" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
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
        "lab": "le poisson de bois",
        "cap": "Le poisson de bois",
        "t1q": "dans la poche",
        "t1line": "Le poisson de bois est dans la poche.",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "Le poisson est dans la poche.",
        "coda": "narrateur|Le poisson de bois rentre dans la poche.",
    },
    2: {
        "lab": "le filet vert",
        "cap": "Le filet vert",
        "t1q": "au bras",
        "t1line": "Le filet vert est au bras.",
        "t1acc": "bras | le bras | au bras | son bras",
        "t1retry": "Le filet est au bras.",
        "coda": "narrateur|Le filet vert sèche sur le rebord.",
    },
    3: {
        "lab": "le seau bleu",
        "cap": "Le seau bleu",
        "t1q": "dans la main",
        "t1line": "Le seau bleu est dans la main.",
        "t1acc": "main | la main | dans la main | sa main",
        "t1retry": "Le seau est dans la main.",
        "coda": "narrateur|Le seau bleu garde une goutte, au fond.",
    },
}

T3_LABS = {
    1: ("le torchon de maman", "les mains d'Aniss", "un pas en arrière"),
    2: ("l'élastique de maman", "la serviette", "Aniss tient le filet"),
    3: ("les manches retroussées", "Raphaël tient le seau", "maman noue les poignets"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Raphaël glisse d'abord le poisson dans sa poche.",
            "enfant-m|Il sent encore le bois, tout doux.",
            "maman|Garde-le dans la poche, tout droit.",
            "narrateur|Un œil peint cligne sous le tissu.",
            "papa|Le filet, ensuite, au bras.",
            "narrateur|Aniss prend le seau bleu, par l'anse.",
            "narrateur|Tout part avec eux, vers l'eau.",
            "enfant-m|Aniss, tu viens ?",
            "copain|J'arrive, même un peu flou.",
            "papa|Le poisson d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Raphaël enroule d'abord le filet vert, au bras.",
            "enfant-m|Il gratte un peu, contre le coude.",
            "papa|Garde-le au bras, tout doux.",
            "narrateur|Les mailles font un petit froissement.",
            "maman|Le poisson, ensuite, dans la poche.",
            "narrateur|Aniss prend le seau bleu, par l'anse.",
            "narrateur|Ils avancent, les affaires avec eux.",
            "enfant-m|Aniss, tu portes le seau ?",
            "copain|Je le tiens, mes lunettes glissent.",
            "maman|Le filet d'abord, il est prêt.",
        )
    return L(
        "narrateur|Raphaël saisit d'abord le seau bleu, par l'anse.",
        "enfant-m|Il sonne un peu, tout vide.",
        "maman|Serre-le dans ta main, tout droit.",
        "narrateur|Le métal fait un petit toc.",
        "papa|Le poisson et le filet, avec vous.",
        "narrateur|Il les pose près des dalles.",
        "narrateur|L'eau du village les attend, plus loin.",
        "enfant-m|Aniss, vite !",
        "narrateur|Le manteau jaune traîne sur les dalles.",
        "copain|J'arrive près de la pierre.",
        "enfant-m|Je te garde un coin d'eau.",
        "papa|Le seau d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La poche porte le poisson, tout contre le tissu.",
            "copain|Je vois un œil, un peu flou.",
            "enfant-m|C'est pour qu'il nage.",
            "narrateur|Les lunettes d'Aniss gardent un rond de buée.",
            "maman|L'eau vous attend, plus loin.",
            "papa|On avance avec le poisson ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le bras porte le filet, tout contre la manche.",
            "copain|Ça gratte quand je marche.",
            "enfant-m|Ne le perds pas.",
            "narrateur|Une goutte tombe d'une mèche d'Aniss.",
            "papa|Ça sent encore le savon, sur tes cheveux.",
            "maman|Vos mains, au-dessus du filet ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|L'anse porte le seau, toute légère.",
        "copain|Il a une goutte, déjà.",
        "enfant-m|On va le remplir.",
        "narrateur|Le manteau d'Aniss cache encore ses poignets.",
        "maman|Les géraniums sont calmes, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le bassin fume un peu, tout bas.",
        "narrateur|Sous l'arche, le ruisseau file.",
        "narrateur|Les géraniums attendent, contre le mur.",
        "papa|Vous allez où, pour le poisson ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Raphaël pose le poisson au bord du bassin.",
            2: "narrateur|Raphaël plonge le filet dans le bassin.",
            3: "narrateur|Raphaël penche le seau vers le bassin.",
        }[t1]
        mishap = {
            1: "narrateur|Le poisson glisse, Aniss ne le voit plus.",
            2: "narrateur|Le filet vise à côté : Aniss visait trop bas.",
            3: "narrateur|Le seau éclabousse, Aniss cherche le jet trop bas.",
        }[t1]
        return L(
            lead,
            "narrateur|Le jet du bassin frappe la pierre, tout fin.",
            "copain|Je vois un nuage sur mes lunettes !",
            "narrateur|Un rond de buée cache l'eau.",
            mishap,
            f"enfant-m|{o['cap']} n'attendait pas ça.",
            "maman|La goutte a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, lui un peu flou.",
            "copain|On fait comment, alors ?",
            "papa|L'eau est floue, vous faites quoi ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Raphaël pose le poisson sous l'arche.",
            2: "narrateur|Raphaël tend le filet sous l'arche.",
            3: "narrateur|Raphaël penche le seau sous l'arche.",
        }[t1]
        mishap = {
            1: "narrateur|Une mèche mouillée couvre le poisson.",
            2: "narrateur|Le filet accroche une mèche, pas l'eau.",
            3: "narrateur|Une goutte de cheveu tombe dans le seau.",
        }[t1]
        return L(
            lead,
            "enfant-m|Ici, l'eau file, Aniss.",
            "copain|Mes cheveux sont encore lourds.",
            mishap,
            "narrateur|Une goutte tape la dalle, toc.",
            "maman|Ils sèchent, tout doux, ce n'est rien.",
            "papa|Toi tes cheveux tiennent, les siens gouttent.",
            "enfant-m|On peut jouer avec lui ?",
            "papa|Les mèches tombent, vous faites quoi ?",
        )
    lead = {
        1: "narrateur|Raphaël tend le poisson vers les fleurs.",
        2: "narrateur|Raphaël glisse le filet entre les pots.",
        3: "narrateur|Raphaël pose le seau près des pots.",
    }[t1]
    mishap = {
        1: "narrateur|Une manche trop longue emporte le poisson.",
        2: "narrateur|Une manche trop longue balaie le filet.",
        3: "narrateur|Une manche trop longue renverse un peu d'eau.",
    }[t1]
    return L(
        lead,
        "enfant-m|Les fleurs sont notre port, Aniss.",
        "copain|Mon manteau me suit jusqu'aux genoux !",
        mishap,
        f"narrateur|{o['cap']} disparaît un instant, sous le tissu.",
        "maman|Le manteau est un peu grand, c'est tout.",
        "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
        "copain|On fait comment, alors ?",
        "papa|Le manteau et l'eau, vous faites comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La buée reste sur les verres, tout douce.",
            "papa|Le torchon, les mains, ou un pas en arrière ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Une mèche mouillée touche encore l'eau.",
            "maman|L'élastique, la serviette, ou tenir le filet ?",
        )
    return L(
        "narrateur|Les manches cachent encore le bois peint.",
        "papa|Les manches, le seau, ou nouer les poignets ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wipe = {
            1: "narrateur|Aniss essuie, puis reprend le bord du poisson.",
            2: "narrateur|Aniss essuie, puis reprend le filet.",
            3: "narrateur|Aniss essuie, puis reprend l'anse du seau.",
        }[t1]
        return L(
            "enfant-m|Maman, le torchon, s'il te plaît.",
            "maman|Tiens, tout doux, sur les verres.",
            "narrateur|Aniss frotte un rond, puis un autre.",
            wipe,
            "copain|Je vois l'eau !",
            "enfant-m|L'œil peint est à toi, maintenant.",
            "narrateur|Les lunettes rendent le bleu tout net.",
            "papa|Vous jouez, chacun avec ce qu'il a.",
            "maman|Le torchon a rendu le bassin.",
        )
    if t2 == 1 and t3 == 2:
        touch = {
            1: "narrateur|Aniss palpe le poisson, Raphaël parle.",
            2: "narrateur|Aniss palpe le filet, Raphaël parle.",
            3: "narrateur|Aniss palpe l'anse, Raphaël parle.",
        }[t1]
        return L(
            "enfant-m|Tu joues avec tes mains, Aniss.",
            "copain|Je touche, toi tu dis où.",
            touch,
            "narrateur|Sous le jet, deux silhouettes avancent.",
            "enfant-m|Le poisson est à gauche, tout froid.",
            "copain|Je le tiens !",
            f"narrateur|{o['cap']} guide encore le geste.",
            "papa|Les mains ont vu à la place des verres.",
            "maman|Le bassin vous a gardés.",
        )
    if t2 == 1 and t3 == 3:
        air = {
            1: "narrateur|Le poisson attend au bord, puis glisse.",
            2: "narrateur|Le filet claque un peu, puis s'apaise.",
            3: "narrateur|Le seau sonne, puis le métal se tait.",
        }[t1]
        return L(
            "enfant-m|On recule un peu, papa ?",
            "papa|Un pas, hors du jet, pas plus.",
            "narrateur|L'air sec chasse la buée, tout lent.",
            air,
            "copain|Ça redevient clair !",
            "enfant-m|Le poisson peut nager.",
            "narrateur|Aniss ajuste ses lunettes, tout net.",
            "maman|La goutte est partie, le jeu reste.",
            "papa|Vous avez attendu le verre clair.",
        )
    if t2 == 2 and t3 == 1:
        high = {
            1: "narrateur|Raphaël pose le poisson, hors des mèches.",
            2: "narrateur|Raphaël tend le filet, hors des mèches.",
            3: "narrateur|Raphaël penche le seau, hors des mèches.",
        }[t1]
        return L(
            "enfant-m|On met l'élastique, plus haut.",
            "copain|Mes cheveux restent en arrière, alors.",
            high,
            "narrateur|Maman noue l'élastique, tout doux.",
            "narrateur|Les mèches d'Aniss tiennent, libres.",
            "enfant-m|Tu peux te pencher, maintenant.",
            "copain|L'eau ne m'attrape plus.",
            "papa|Chacun a sa hauteur, près de l'arche.",
            "maman|Les cheveux ont eu leur place.",
        )
    if t2 == 2 and t3 == 2:
        dry = {
            1: "narrateur|Le poisson attend, le temps d'un frottement.",
            2: "narrateur|Le filet attend, le temps d'un frottement.",
            3: "narrateur|Le seau attend, le temps d'un frottement.",
        }[t1]
        pose = {
            1: "enfant-m|On pose le poisson, maintenant.",
            2: "enfant-m|On tend le filet, maintenant.",
            3: "enfant-m|On penche le seau, maintenant.",
        }[t1]
        return L(
            "enfant-m|La serviette, maman ?",
            "maman|Frotte, tout doux, pas trop fort.",
            "narrateur|Aniss essuie une mèche, puis une autre.",
            dry,
            "copain|Elles sont plus légères !",
            pose,
            "narrateur|L'eau file, sans emporter de cheveu.",
            "papa|Vous avez laissé l'eau des cheveux.",
            "maman|L'arche sent encore le savon.",
        )
    if t2 == 2 and t3 == 3:
        hold = {
            1: "narrateur|Aniss tient le filet, Raphaël glisse le poisson.",
            2: "narrateur|Aniss tient le filet à deux mains, sans se pencher.",
            3: "narrateur|Aniss tient le filet, Raphaël penche le seau.",
        }[t1]
        return L(
            "enfant-m|Tu tiens le filet, moi je pose.",
            "copain|Mes mains font le bord, alors.",
            hold,
            "narrateur|L'eau s'ouvre quand Aniss recule.",
            "narrateur|Elle se ferme quand il avance.",
            "enfant-m|C'est toi le port, Aniss !",
            "copain|Et toi le poisson.",
            "papa|Vous jouez avec ce que vous avez.",
            "maman|Les cheveux n'ont plus besoin d'être dans l'eau.",
        )
    if t2 == 3 and t3 == 1:
        roll = {
            1: "narrateur|Les manches remontent, le poisson redevient libre.",
            2: "narrateur|Les manches remontent, le filet redevient visible.",
            3: "narrateur|Les manches remontent, le seau redevient visible.",
        }[t1]
        return L(
            "enfant-m|On retrousse, Aniss.",
            "copain|Jusqu'au coude, comme papa.",
            "narrateur|Deux rouleaux de tissu tiennent, un peu épais.",
            roll,
            "enfant-m|Je te vois les mains, maintenant.",
            "copain|Le poisson n'est plus dans le manteau.",
            f"narrateur|{o['cap']} reprend sa place, au milieu.",
            "papa|Les manches ont laissé l'eau passer.",
            "maman|Le manteau reste, plus court aux poignets.",
        )
    if t2 == 3 and t3 == 2:
        split = {
            1: "narrateur|Raphaël tient le seau, Aniss pose le poisson.",
            2: "narrateur|Raphaël tient le seau, Aniss tend le filet.",
            3: "narrateur|Raphaël tient le seau, Aniss verse tout doux.",
        }[t1]
        return L(
            "enfant-m|Moi je tiens le seau.",
            "copain|Moi je guide, près des fleurs.",
            split,
            "narrateur|Les manches trop longues bougent le tissu, seulement.",
            "narrateur|Le bois peint reste hors du manteau.",
            "copain|Le port s'ouvre !",
            "enfant-m|Le poisson sort, tout bleu.",
            "papa|Chacun a pris sa part, à sa taille.",
            "maman|Les fleurs ont tenu l'eau.",
        )
    bind = {
        1: "narrateur|L'élastique tient une manche, le poisson l'autre main.",
        2: "narrateur|L'élastique tient une manche, le filet l'autre main.",
        3: "narrateur|L'élastique tient une manche, le seau reste droit.",
    }[t1]
    return L(
        "enfant-m|Maman, ton élastique, s'il te plaît.",
        "maman|Un pour chaque manche, tout doux.",
        "narrateur|Aniss tend les poignets, maman noue.",
        bind,
        "copain|Mes mains sont nues, maintenant.",
        "enfant-m|Le poisson peut nager.",
        "narrateur|Le bleu avance entre les pots.",
        "papa|Vous avez demandé, et ça tient.",
        "maman|Mes élastiques ont gardé le manteau.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le bassin sent encore le torchon tiède.",
            "copain|J'ai vu l'œil peint, tout net.",
            "enfant-m|Tes lunettes ont trouvé le bleu.",
            "papa|Vous avez joué, chacun avec sa vue.",
            "maman|Les dalles sèchent déjà, tout doux.",
            coda,
            "narrateur|Une goutte reste sur le bois, ronde.",
            "enfant-m|On rentre, Aniss.",
            "narrateur|La pierre du lavoir redevient calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous le jet, l'air est encore un peu froid.",
            "enfant-m|Tu as touché, moi j'ai dit où.",
            "copain|Mes mains ont vu le bleu.",
            "papa|Les verres flous n'ont pas arrêté l'eau.",
            "maman|Le bassin se tait, enfin.",
            coda,
            "narrateur|Une ombre de poisson reste au fond.",
            "enfant-m|À demain, l'eau.",
            "narrateur|Le rebord redevient froid, déjà.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Un filet d'air sec reste près du bassin.",
            "copain|La buée est partie, tout seule.",
            "enfant-m|On a attendu le verre clair.",
            "maman|Le pas en arrière a rendu l'eau.",
            "papa|Vous avez laissé le temps aux lunettes.",
            coda,
            "narrateur|Raphaël souffle sur l'œil peint, tout léger.",
            "copain|Il brille encore.",
            "narrateur|Le jet reprend, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|L'arche garde encore un peu d'ombre.",
            "enfant-m|L'élastique était trop bas, d'abord.",
            "copain|Mes cheveux sont restés libres.",
            "papa|Chacun a eu sa hauteur, près de l'eau.",
            "maman|La dalle sèche déjà.",
            coda,
            "narrateur|Une mèche sèche contre le col, tout calme.",
            "enfant-m|On rentre, l'arche reste.",
            "narrateur|Le ruisseau reprend sa course, tout bas.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La serviette sent encore le savon.",
            "copain|Tu as frotté, tout doux.",
            "enfant-m|Puis on a posé, sans emporter de cheveu.",
            "maman|L'eau des cheveux s'en est allée.",
            "papa|L'arche vous rend le silence.",
            coda,
            "narrateur|Raphaël souffle dessus, tout léger.",
            "copain|Elle part.",
            "narrateur|Le savon s'efface déjà de la pierre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains d'Aniss gardent encore le pli du filet.",
            "enfant-m|Tu étais le port vivant.",
            "copain|Toi le poisson, moi l'ouverture.",
            "papa|Vous avez joué avec ce que vous aviez.",
            "maman|Les cheveux n'avaient plus besoin d'être pris.",
            coda,
            "narrateur|Un rebord vide attend, tout bas.",
            "enfant-m|On se dit au revoir, arche.",
            "narrateur|Les chaussons glissent vers la maison.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Deux rouleaux de manches tiennent encore.",
            "enfant-m|Tes mains sont sorties du manteau.",
            "copain|Le poisson n'était plus avalé.",
            "papa|Les manches ont laissé l'eau passer.",
            "maman|Les pots redeviennent des pots, tout simples.",
            coda,
            "narrateur|Un pétale rouge reste sur le bois.",
            "enfant-m|On rentre, Aniss.",
            "narrateur|Le géranium reprend sa forme, tout lent.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Une goutte tombe encore d'une feuille.",
            "copain|Tu tenais le seau, moi le bord.",
            "enfant-m|Tes manches bougeaient seulement le tissu.",
            "maman|Chacun a pris sa part, à sa taille.",
            "papa|Les fleurs ont tenu jusqu'au bout.",
            coda,
            "narrateur|Raphaël lisse le bois, tout doux.",
            "copain|Il a bien nagé.",
            "narrateur|Le mur reprend son calme, déjà.",
        )
    return L(
        "narrateur|Deux élastiques veillent encore aux poignets.",
        "enfant-m|On a demandé, et ça tenait.",
        "copain|Mes mains étaient nues, pour l'eau.",
        "papa|Vous avez demandé, rien de plus.",
        "maman|Mes élastiques rentrent dans la poche.",
        coda,
        "narrateur|Un peu de terre reste au rebord.",
        "enfant-m|L'eau est à nous.",
        "narrateur|Le village sent encore la pluie d'hier.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La pierre du lavoir reste froide, encore mouillée.",
        "narrateur|Un filet de mousse verte suit le rebord.",
        "narrateur|Ça sent le savon et la pluie d'hier.",
        "narrateur|Trois géraniums rouges pendent au mur.",
        "papa|Tu as vu l'eau, Raphaël ?",
        "enfant-m|Elle court encore, tout bas.",
        "maman|Le poisson de bois attend, dans la poche.",
        "narrateur|En ce moment, Raphaël le sort, tout doux.",
        "enfant-m|Je veux qu'il nage, pour de vrai.",
        "narrateur|Des pas claquent sur les dalles.",
        "copain|J'arrive, Raphaël !",
        "narrateur|Les lunettes d'Aniss gardent un rond de buée.",
        "narrateur|Ses cheveux gouttent sur le manteau trop long.",
        "papa|Merci, tu tiens déjà le poisson.",
        "maman|On l'emmène à l'eau, alors ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près de la pierre, le poisson attend.",
        "narrateur|Le filet vert dort, plié.",
        "narrateur|Le seau bleu penche, vide.",
        "maman|Tu prends quoi d'abord, Raphaël ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le poisson de bois", "le filet vert", "le seau bleu")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        t1_ask = {
            1: "maman|Le poisson est où ?",
            2: "maman|Le filet est où ?",
            3: "maman|Le seau est où ?",
        }[t1]
        s[f"{p}_Q0001"] = L(
            f"narrateur|{o['t1line']}",
            t1_ask,
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le bassin", "le ruisseau", "les géraniums")

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Raphaël veut que son poisson de bois nage dans l'eau du village. "
        "Aniss arrive, lunettes encore floues, cheveux mouillés, manteau jaune "
        "trop long. T1 = poisson de bois / filet vert / seau bleu (les trois "
        "partent). T2 = bassin (buée sur les verres) / ruisseau (mèches dans "
        "l'eau) / géraniums (manches trop longues). T3 = neuf résolutions "
        "(torchon, mains, pas en arrière ; élastique, serviette, tenir le "
        "filet ; manches, Raphaël tient, nouer les poignets). On joue ensemble, "
        "sans slogan. Fin : le poisson rentre, encore mouillé.",
        "N2 ≤ 15. Hugo / Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-016 "
        "(pas la tarte, pas la chambre) et DIF-026 (pas le théâtre). "
        "Un merci de papa lié au geste (tenir le poisson). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
