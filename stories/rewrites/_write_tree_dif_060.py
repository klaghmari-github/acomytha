#!/usr/bin/env python3
"""TREE-DIF-060 — Le train de boîtes de Sarah (N2, DIF.COR.003, salon)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-060"
N2 = LIMITS["N2"]
TITLE = "Le train de boîtes de Sarah"
FIL = (
    "Sarah veut un train de boîtes pour son cheval de bois, jusqu'à la fenêtre, "
    "avant que papa n'éteigne la lampe. Nino arrive du palier, lunettes voilées "
    "par le radiateur, cheveux encore mouillés, gilet trop long. Ils emportent "
    "le cheval, la boîte à chaussures et le foulard à pois. Au canapé la buée "
    "cache le bord, sur le tapis les mèches gouttent, à la fenêtre les manches "
    "attrapent le rideau. Ils font voyager le cheval ensemble. La gare s'allume "
    "sur le rebord. Le cacao fume encore."
)
CHARS = "Sarah, Nino, papa, maman"
SETTING = "salon après la pluie : canapé, tapis, fenêtre"


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
        "jules",
        "sami",
        "léa",
        "tom ",
        "nora",
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
        "poisson",
        "lavoir",
        "groseille",
        "phare",
        "coquillage",
        "galet",
        "lunettes, cheveux",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if re.search(r"\bsara\b", blob):
        raise SystemExit(f"{SID}: Sara (sans h) encore présente")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "train" not in blob and "boîte" not in blob and "boite" not in blob:
        raise SystemExit(f"{SID}: train/boîtes absents")
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
        "lab": "le cheval de bois",
        "cap": "Le cheval de bois",
        "short": "le cheval",
        "t1q": "dans les mains",
        "t1line": "Le cheval de bois est dans les mains.",
        "t1acc": "mains | les mains | dans les mains | ses mains",
        "t1retry": "Le cheval est dans les mains.",
        "coda": "narrateur|Le cheval de bois garde un fil de tapis au pied.",
    },
    2: {
        "lab": "la boîte à chaussures",
        "cap": "La boîte à chaussures",
        "short": "la boîte",
        "t1q": "au bras",
        "t1line": "La boîte à chaussures est au bras.",
        "t1acc": "bras | le bras | au bras | son bras",
        "t1retry": "La boîte est au bras.",
        "coda": "narrateur|La boîte à chaussures sèche près de la porte.",
    },
    3: {
        "lab": "le foulard à pois",
        "cap": "Le foulard à pois",
        "short": "le foulard",
        "t1q": "sous le bras",
        "t1line": "Le foulard à pois est sous le bras.",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "Le foulard est sous le bras.",
        "coda": "narrateur|Le foulard à pois retrouve le dossier du canapé.",
    },
}

T3_LABS = {
    1: ("le torchon de maman", "les mains de Sarah", "un pas hors du canapé"),
    2: ("la pince de maman", "la serviette", "Sarah tient le cheval"),
    3: ("les manches retroussées", "Sarah tient la boîte", "maman noue les poignets"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah glisse d'abord le cheval dans ses mains.",
            "enfant-f|Son dos est encore un peu froid.",
            "maman|Garde-le droit, tout près de toi.",
            "narrateur|Le bois lisse brille, sous le rond de lampe.",
            "papa|La boîte, ensuite, au bras.",
            "narrateur|Nino prend le foulard, sous le bras.",
            "narrateur|Tout part avec eux, vers le tapis.",
            "enfant-f|Nino, tu viens ?",
            "copain|Je suis là, même un peu flou.",
            "papa|Le cheval d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah cale d'abord la boîte contre son bras.",
            "enfant-f|Le carton gratte un peu, contre le coude.",
            "papa|Garde-la au bras, tout doux.",
            "narrateur|Un coin de carton fait un petit froissement.",
            "maman|Le cheval, ensuite, dans les mains.",
            "narrateur|Nino prend le foulard, sous le bras.",
            "narrateur|Ils avancent, les affaires avec eux.",
            "enfant-f|Nino, tu portes le foulard ?",
            "copain|Je le tiens, mes lunettes glissent.",
            "maman|La boîte d'abord, elle est prête.",
        )
    return L(
        "narrateur|Sarah plie d'abord le foulard, sous le bras.",
        "enfant-f|Les pois sentent encore le tiroir.",
        "maman|Serre-le sous le bras, tout droit.",
        "narrateur|Le tissu glisse, puis tient.",
        "papa|Le cheval et la boîte, avec vous.",
        "narrateur|Elle les pose près du tapis usé.",
        "narrateur|La fenêtre les attend, toute rayée.",
        "enfant-f|Nino, vite !",
        "narrateur|Le gilet trop long traîne sur le tapis.",
        "copain|J'arrive près du canapé.",
        "enfant-f|Je te garde un coin de foulard.",
        "papa|Le foulard d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Les mains portent le cheval, tout contre le bois.",
            "copain|Je vois le dos, un peu flou.",
            "enfant-f|C'est pour le train.",
            "narrateur|Les lunettes de Nino gardent un rond de buée.",
            "maman|La fenêtre vous attend, plus loin.",
            "papa|On avance avec le cheval ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le bras porte la boîte, tout contre la manche.",
            "copain|Ça gratte quand je marche.",
            "enfant-f|Ne la perds pas.",
            "narrateur|Une goutte tombe d'une mèche de Nino.",
            "papa|Ça sent encore la pluie, sur tes cheveux.",
            "maman|Vos mains, au-dessus de la boîte ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|Le bras porte le foulard, tout léger.",
        "copain|Il a un pli, déjà.",
        "enfant-f|On va le dérouler, pour les rails.",
        "narrateur|Le gilet de Nino cache encore ses poignets.",
        "maman|Le rebord est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le canapé est tiède, près du radiateur.",
        "narrateur|Le tapis garde un coin usé.",
        "narrateur|La fenêtre attend, toute rayée de pluie.",
        "papa|Vous allez où, pour le train ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Sarah pose le cheval sur le dossier du canapé.",
            2: "narrateur|Sarah cale la boîte contre le coussin tiède.",
            3: "narrateur|Sarah déroule le foulard le long du canapé.",
        }[t1]
        mishap = {
            1: "narrateur|Le cheval glisse : Nino visait trop bas.",
            2: "narrateur|La boîte vise à côté du coussin.",
            3: "narrateur|Le foulard se plie, Nino cherche le bord trop bas.",
        }[t1]
        return L(
            lead,
            "narrateur|Le radiateur souffle, tout proche.",
            "copain|Je vois un nuage sur mes lunettes !",
            "narrateur|Un rond de buée cache le bord du canapé.",
            mishap,
            f"enfant-f|{o['cap']} n'attendait pas ça.",
            "maman|La chaleur a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, lui un peu flou.",
            "copain|On fait comment, alors ?",
            "papa|Le bord est flou, vous faites quoi ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Sarah pose le cheval au milieu du tapis.",
            2: "narrateur|Sarah pose la boîte au milieu du tapis.",
            3: "narrateur|Sarah déroule le foulard sur le tapis usé.",
        }[t1]
        mishap = {
            1: "narrateur|Une mèche mouillée couvre le dos du cheval.",
            2: "narrateur|Une goutte tombe dans la boîte, toc.",
            3: "narrateur|Une goutte de cheveu tache un pois du foulard.",
        }[t1]
        return L(
            lead,
            "enfant-f|Ici, le tapis est doux, Nino.",
            "copain|Mes cheveux sont encore lourds.",
            mishap,
            "narrateur|Une autre goutte tape le fil, tout petit.",
            "maman|Ils sèchent, tout doux, ce n'est rien.",
            "papa|Toi tes cheveux tiennent, les siens gouttent.",
            "enfant-f|On peut faire le train avec lui ?",
            "papa|Les mèches tombent, vous faites quoi ?",
        )
    lead = {
        1: "narrateur|Sarah tend le cheval vers le rebord de la fenêtre.",
        2: "narrateur|Sarah glisse la boîte vers le rebord.",
        3: "narrateur|Sarah pose le foulard sous la fenêtre.",
    }[t1]
    mishap = {
        1: "narrateur|Une manche trop longue emporte le cheval.",
        2: "narrateur|Une manche trop longue balaie la boîte.",
        3: "narrateur|Une manche trop longue froisse le foulard.",
    }[t1]
    return L(
        lead,
        "enfant-f|La gare, c'est le rebord, Nino.",
        "copain|Mon gilet me suit jusqu'aux genoux !",
        mishap,
        f"narrateur|{o['cap']} disparaît un instant, sous le tissu.",
        "maman|Le gilet est un peu grand, c'est tout.",
        "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
        "copain|On fait comment, alors ?",
        "papa|Le gilet et le train, vous faites comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La buée reste sur les verres, tout douce.",
            "papa|Le torchon, les mains, ou un pas hors du canapé ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Une mèche mouillée touche encore le carton.",
            "maman|La pince, la serviette, ou tenir le cheval ?",
        )
    return L(
        "narrateur|Les manches cachent encore le rebord de la fenêtre.",
        "papa|Les manches, la boîte, ou nouer les poignets ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wipe = {
            1: "narrateur|Nino essuie, puis reprend le dos du cheval.",
            2: "narrateur|Nino essuie, puis reprend le coin de la boîte.",
            3: "narrateur|Nino essuie, puis reprend le pli du foulard.",
        }[t1]
        return L(
            "enfant-f|Maman, le torchon, s'il te plaît.",
            "maman|Tiens, tout doux, sur les verres.",
            "narrateur|Nino frotte un rond, puis un autre.",
            wipe,
            "copain|Je vois le coussin !",
            "enfant-f|Le train est à toi, maintenant.",
            "narrateur|Les lunettes rendent le canapé tout net.",
            "papa|Vous avancez, chacun avec ce qu'il a.",
            "maman|Le torchon a rendu le bord.",
        )
    if t2 == 1 and t3 == 2:
        touch = {
            1: "narrateur|Nino palpe le cheval, Sarah parle.",
            2: "narrateur|Nino palpe la boîte, Sarah parle.",
            3: "narrateur|Nino palpe le foulard, Sarah parle.",
        }[t1]
        return L(
            "enfant-f|Tu guides avec tes mains, Nino.",
            "copain|Je touche, toi tu dis où.",
            touch,
            "narrateur|Sous la lampe, deux silhouettes avancent.",
            "enfant-f|Le coussin est à gauche, tout tiède.",
            "copain|Je le tiens !",
            f"narrateur|{o['cap']} guide encore le geste.",
            "papa|Les mains ont vu à la place des verres.",
            "maman|Le canapé vous a gardés.",
        )
    if t2 == 1 and t3 == 3:
        air = {
            1: "narrateur|Le cheval attend au bord, puis se pose.",
            2: "narrateur|La boîte craque un peu, puis s'apaise.",
            3: "narrateur|Le foulard glisse, puis le tissu se tait.",
        }[t1]
        return L(
            "enfant-f|On recule un peu, papa ?",
            "papa|Un pas, hors de la buée, pas plus.",
            "narrateur|L'air plus frais chasse la buée, tout lent.",
            air,
            "copain|Ça redevient clair !",
            "enfant-f|Le train peut partir.",
            "narrateur|Nino ajuste ses lunettes, tout net.",
            "maman|La buée est partie, le jeu reste.",
            "papa|Vous avez attendu le verre clair.",
        )
    if t2 == 2 and t3 == 1:
        high = {
            1: "narrateur|Sarah pose le cheval, hors des mèches.",
            2: "narrateur|Sarah tend la boîte, hors des mèches.",
            3: "narrateur|Sarah ouvre le foulard, hors des mèches.",
        }[t1]
        return L(
            "enfant-f|On met la pince, plus haut.",
            "copain|Mes cheveux restent en arrière, alors.",
            high,
            "narrateur|Maman glisse la pince, tout doux.",
            "narrateur|Les mèches de Nino tiennent, libres.",
            "enfant-f|Tu peux te pencher, maintenant.",
            "copain|Le tapis ne m'attrape plus.",
            "papa|Chacun a sa hauteur, sur le tapis.",
            "maman|Les cheveux ont eu leur place.",
        )
    if t2 == 2 and t3 == 2:
        dry = {
            1: "narrateur|Le cheval attend, le temps d'un frottement.",
            2: "narrateur|La boîte attend, le temps d'un frottement.",
            3: "narrateur|Le foulard attend, le temps d'un frottement.",
        }[t1]
        pose = {
            1: "enfant-f|On pose le cheval, maintenant.",
            2: "enfant-f|On pose la boîte, maintenant.",
            3: "enfant-f|On ouvre le foulard, maintenant.",
        }[t1]
        return L(
            "enfant-f|La serviette, maman ?",
            "maman|Frotte, tout doux, pas trop fort.",
            "narrateur|Nino essuie une mèche, puis une autre.",
            dry,
            "copain|Elles sont plus légères !",
            pose,
            "narrateur|Le tapis reste sec, sous le carton.",
            "papa|Vous avez laissé l'eau des cheveux.",
            "maman|Le tapis sent encore un peu la pluie.",
        )
    if t2 == 2 and t3 == 3:
        hold = {
            1: "narrateur|Sarah tient le cheval, Nino pose la boîte.",
            2: "narrateur|Sarah tient le cheval, Nino pousse la boîte.",
            3: "narrateur|Sarah tient le cheval, Nino ouvre le foulard.",
        }[t1]
        return L(
            "enfant-f|Tu poses les rails, moi je tiens le cheval.",
            "copain|Mes mains font le carton, alors.",
            hold,
            "narrateur|Les gouttes tombent quand Nino recule.",
            "narrateur|Elles s'arrêtent quand il avance.",
            "enfant-f|C'est toi la gare, Nino !",
            "copain|Et toi le cheval.",
            "papa|Vous avancez avec ce que vous avez.",
            "maman|Les cheveux n'ont plus besoin d'être dans la boîte.",
        )
    if t2 == 3 and t3 == 1:
        roll = {
            1: "narrateur|Les manches remontent, le cheval redevient libre.",
            2: "narrateur|Les manches remontent, la boîte redevient visible.",
            3: "narrateur|Les manches remontent, le foulard redevient visible.",
        }[t1]
        return L(
            "enfant-f|On retrousse, Nino.",
            "copain|Jusqu'au coude, comme papa.",
            "narrateur|Deux rouleaux de tissu tiennent, un peu épais.",
            roll,
            "enfant-f|Je te vois les mains, maintenant.",
            "copain|Le rebord n'est plus dans le gilet.",
            f"narrateur|{o['cap']} reprend sa place, au milieu.",
            "papa|Les manches ont laissé le train passer.",
            "maman|Le gilet reste, plus court aux poignets.",
        )
    if t2 == 3 and t3 == 2:
        split = {
            1: "narrateur|Sarah tient la boîte, Nino pose le cheval.",
            2: "narrateur|Sarah tient la boîte, Nino y glisse le cheval.",
            3: "narrateur|Sarah tient la boîte, Nino ouvre le foulard.",
        }[t1]
        return L(
            "enfant-f|Moi je tiens la boîte.",
            "copain|Moi je guide, près du rideau.",
            split,
            "narrateur|Les manches trop longues bougent le tissu, seulement.",
            "narrateur|Le cheval reste hors du gilet.",
            "copain|Le rebord s'ouvre !",
            "enfant-f|La gare est là, tout nette.",
            "papa|Chacun a pris sa part, à sa taille.",
            "maman|Le rideau a laissé le rebord.",
        )
    bind = {
        1: "narrateur|L'élastique tient une manche, le cheval l'autre main.",
        2: "narrateur|L'élastique tient une manche, la boîte l'autre main.",
        3: "narrateur|L'élastique tient une manche, le foulard reste droit.",
    }[t1]
    return L(
        "enfant-f|Maman, ton élastique, s'il te plaît.",
        "maman|Un pour chaque manche, tout doux.",
        "narrateur|Nino tend les poignets, maman noue.",
        bind,
        "copain|Mes mains sont nues, maintenant.",
        "enfant-f|Le train peut arriver.",
        "narrateur|Le cheval avance entre les pois.",
        "papa|Vous avez demandé, et ça tient.",
        "maman|Mes élastiques ont gardé le gilet.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le cheval s'arrête sur le dossier, gare du canapé.",
            "copain|J'ai vu le bord, tout net.",
            "enfant-f|Tes lunettes ont trouvé la gare.",
            "papa|Vous avez avancé, chacun avec sa vue.",
            "maman|Les verres sèchent déjà, tout doux.",
            coda,
            "narrateur|Le rond de lampe tient encore sur le coussin.",
            "enfant-f|On souffle sur le cacao, Nino.",
            "narrateur|Le radiateur reprend son tic, tout seul.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous la lampe, le cheval touche enfin le coussin.",
            "enfant-f|Tu as touché, moi j'ai dit où.",
            "copain|Mes mains ont vu la gare.",
            "papa|Les verres flous n'ont pas arrêté le train.",
            "maman|Le canapé se tait, enfin.",
            coda,
            "narrateur|Une ombre de cheval reste au fond du carton.",
            "enfant-f|À demain, le dossier.",
            "narrateur|Le cacao fume encore, près de la lampe.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Un filet d'air plus frais reste près du canapé.",
            "copain|La buée est partie, tout seule.",
            "enfant-f|On a attendu, puis le cheval est arrivé.",
            "maman|Le pas en arrière a rendu le bord.",
            "papa|Vous avez laissé le temps aux lunettes.",
            coda,
            "narrateur|Sarah souffle sur le cheval, tout léger.",
            "copain|Il brille encore, sur le dossier.",
            "narrateur|Le radiateur reprend, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le cheval s'arrête au coin usé, gare du tapis.",
            "enfant-f|La pince était trop bas, d'abord.",
            "copain|Mes cheveux sont restés libres.",
            "papa|Chacun a eu sa hauteur, sur le fil.",
            "maman|Le tapis sèche déjà.",
            coda,
            "narrateur|Une mèche sèche contre le col, tout calme.",
            "enfant-f|On reste un peu, le tapis reste.",
            "narrateur|Un pois reprend sa place, tout bas.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La serviette sent encore un peu la pluie.",
            "copain|Tu as frotté, tout doux.",
            "enfant-f|Puis le cheval a roulé, sans goutte.",
            "maman|L'eau des cheveux s'en est allée.",
            "papa|Le tapis vous rend le silence.",
            coda,
            "narrateur|Sarah souffle sur le dos du cheval.",
            "copain|Il est à la gare.",
            "narrateur|La pluie s'efface déjà du carton.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains de Sarah posent le cheval au coin usé.",
            "enfant-f|Tu étais la gare.",
            "copain|Toi le cheval, moi le carton.",
            "papa|Vous avez avancé avec ce que vous aviez.",
            "maman|Les cheveux n'avaient plus besoin d'être pris.",
            coda,
            "narrateur|Un coin de tapis usé attend, tout bas.",
            "enfant-f|On se dit au revoir, tapis.",
            "narrateur|Les chaussons glissent vers le cacao.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le cheval s'arrête sur le rebord, gare de la fenêtre.",
            "enfant-f|Tes mains sont sorties du gilet.",
            "copain|Le rebord n'était plus avalé.",
            "papa|Les manches ont laissé le train passer.",
            "maman|Les rideaux redeviennent des rideaux, tout simples.",
            coda,
            "narrateur|Un pois rouge reste sur le bois.",
            "enfant-f|On souffle, Nino.",
            "narrateur|La fenêtre reprend ses traits de pluie.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Une goutte glisse encore sur la vitre.",
            "copain|Tu tenais la boîte, moi le bord.",
            "enfant-f|Le cheval est arrivé, malgré le rideau.",
            "maman|Chacun a pris sa part, à sa taille.",
            "papa|Le rebord a tenu jusqu'au bout.",
            coda,
            "narrateur|Sarah lisse le dos du cheval, tout doux.",
            "copain|Il a bien roulé jusqu'ici.",
            "narrateur|Le salon reprend son calme, déjà.",
        )
    return L(
        "narrateur|Deux élastiques veillent encore aux poignets.",
        "enfant-f|On a demandé, et le cheval est là.",
        "copain|Mes mains étaient nues, pour le rebord.",
        "papa|Vous avez demandé, rien de plus.",
        "maman|Mes élastiques rentrent dans la poche.",
        coda,
        "narrateur|Le cheval garde la vitre, tout petit.",
        "enfant-f|Le train est à nous.",
        "narrateur|Le cacao fume encore, tout bas.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Au rez-de-chaussée, le salon garde la pluie dehors.",
        "narrateur|La grande vitre est rayée de gouttes.",
        "narrateur|Le radiateur chante un petit tic.",
        "narrateur|Ça sent le cacao, tout chaud.",
        "narrateur|L'abat-jour de papier pose un rond jaune.",
        "papa|Tu as vu le cheval, Sarah ?",
        "enfant-f|Il veut sa gare, près de la fenêtre.",
        "maman|La boîte à chaussures attend, sous la table.",
        "narrateur|En ce moment, Sarah la tire vers le tapis.",
        "enfant-f|Je veux un train, avant la lampe éteinte.",
        "narrateur|Des pas sonnent sur le palier mouillé.",
        "copain|J'arrive, Sarah !",
        "narrateur|Les lunettes de Nino gardent un rond de buée.",
        "narrateur|Ses cheveux gouttent sur le gilet trop long.",
        "papa|Merci, tu tiens déjà le cheval.",
        "maman|On le fait voyager, alors ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près de la table, le cheval de bois attend.",
        "narrateur|La boîte à chaussures dort, vide.",
        "narrateur|Le foulard à pois est plié.",
        "maman|Tu prends quoi d'abord, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le cheval de bois", "la boîte à chaussures", "le foulard à pois")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        t1_ask = {
            1: "maman|Le cheval est où ?",
            2: "maman|La boîte est où ?",
            3: "maman|Le foulard est où ?",
        }[t1]
        s[f"{p}_Q0001"] = L(
            f"narrateur|{o['t1line']}",
            t1_ask,
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le canapé", "le tapis", "la fenêtre")

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
        "Sarah veut un train de boîtes pour son cheval de bois, jusqu'à la fenêtre, "
        "avant que papa n'éteigne la lampe. Nino arrive du palier, lunettes voilées "
        "par le radiateur, cheveux mouillés, gilet trop long. T1 = cheval de bois / "
        "boîte à chaussures / foulard à pois (les trois partent). T2 = canapé (buée "
        "sur les verres) / tapis (mèches qui gouttent) / fenêtre (manches trop "
        "longues au rideau). T3 = neuf résolutions (torchon, mains, pas hors du "
        "canapé ; pince, serviette, Sarah tient le cheval ; manches, Sarah tient "
        "la boîte, nouer les poignets). On fait voyager le cheval ensemble, sans "
        "slogan. Fin : la gare s'allume sur le rebord, le cacao fume.",
        "N2 ≤ 15. Sara → Sarah. Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-016 (pas la "
        "tarte), DIF-026 (pas le théâtre), DIF-036 (pas le poisson, pas le lavoir), "
        "DIF-044 (pas les groseilles) et DIF-052 (pas le phare). Salon : canapé, "
        "tapis, fenêtre. Un merci de papa lié au geste (tenir le cheval). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
