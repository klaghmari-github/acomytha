#!/usr/bin/env python3
"""TREE-DIF-044 — Les groseilles de Raphaël au treillis (N2, DIF.COR.003)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-044"
N2 = LIMITS["N2"]
TITLE = "Les groseilles de Raphaël au treillis"
FIL = (
    "Raphaël veut remplir un bol de groseilles rouges pour le goûter. "
    "Sarah arrive, lunettes encore floues, cheveux mouillés, ciré jaune "
    "trop long. Ils emportent le bol blanc, le panier d'osier et la nappe "
    "à carreaux. À la serre la buée cache les grains, sous le tilleul "
    "les mèches gouttent, au treillis les manches attrapent. Ils cueillent "
    "ensemble. Le bol rentre, tout rouge."
)
CHARS = "Raphaël, Sarah, papa, maman"
SETTING = "jardin après la pluie : serre, tilleul, treillis"


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
        "potager",
        "tomate",
        "biscuits",
        "lunettes, cheveux",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "raphaël" not in blob and "raphael" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "groseille" not in blob:
        raise SystemExit(f"{SID}: groseilles absentes")
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
        "lab": "le bol blanc",
        "cap": "Le bol blanc",
        "t1q": "dans les mains",
        "t1line": "Le bol blanc est dans les mains.",
        "t1acc": "mains | les mains | dans les mains | ses mains",
        "t1retry": "Le bol est dans les mains.",
        "coda": "narrateur|Le bol blanc rentre, tout rouge.",
    },
    2: {
        "lab": "le panier d'osier",
        "cap": "Le panier d'osier",
        "t1q": "au bras",
        "t1line": "Le panier d'osier est au bras.",
        "t1acc": "bras | le bras | au bras | son bras",
        "t1retry": "Le panier est au bras.",
        "coda": "narrateur|Le panier d'osier sèche près de la marche.",
    },
    3: {
        "lab": "la nappe à carreaux",
        "cap": "La nappe à carreaux",
        "t1q": "sous le bras",
        "t1line": "La nappe à carreaux est sous le bras.",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "La nappe est sous le bras.",
        "coda": "narrateur|La nappe à carreaux retrouve la table.",
    },
}

T3_LABS = {
    1: ("le torchon de maman", "les mains de Sarah", "un pas hors de la serre"),
    2: ("l'élastique de maman", "la serviette", "Sarah tient le bol"),
    3: ("les manches retroussées", "Raphaël tient le panier", "maman noue les poignets"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Raphaël glisse d'abord le bol dans ses mains.",
            "enfant-m|Il est encore un peu froid.",
            "maman|Garde-le droit, tout près de toi.",
            "narrateur|Le blanc du bol brille, tout net.",
            "papa|Le panier, ensuite, au bras.",
            "narrateur|Sarah prend la nappe, sous le bras.",
            "narrateur|Tout part avec eux, vers le jardin.",
            "enfant-m|Sarah, tu viens ?",
            "copine|J'arrive, même un peu floue.",
            "papa|Le bol d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Raphaël enroule d'abord le panier au bras.",
            "enfant-m|L'osier gratte un peu, contre le coude.",
            "papa|Garde-le au bras, tout doux.",
            "narrateur|Les tiges font un petit froissement.",
            "maman|Le bol, ensuite, dans les mains.",
            "narrateur|Sarah prend la nappe, sous le bras.",
            "narrateur|Ils avancent, les affaires avec eux.",
            "enfant-m|Sarah, tu portes la nappe ?",
            "copine|Je la tiens, mes lunettes glissent.",
            "maman|Le panier d'abord, il est prêt.",
        )
    return L(
        "narrateur|Raphaël plie d'abord la nappe, sous le bras.",
        "enfant-m|Les carreaux sentent encore le tiroir.",
        "maman|Serre-la sous le bras, tout droit.",
        "narrateur|Le tissu fait un petit froissement.",
        "papa|Le bol et le panier, avec vous.",
        "narrateur|Il les pose près de la marche.",
        "narrateur|Les groseilles les attendent, plus loin.",
        "enfant-m|Sarah, vite !",
        "narrateur|Le ciré jaune traîne sur l'herbe.",
        "copine|J'arrive près du treillis.",
        "enfant-m|Je te garde un coin de nappe.",
        "papa|La nappe d'abord, elle est prête.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Les mains portent le bol, tout contre le tissu.",
            "copine|Je vois le blanc, un peu flou.",
            "enfant-m|C'est pour les groseilles.",
            "narrateur|Les lunettes de Sarah gardent un rond de buée.",
            "maman|Les grains vous attendent, plus loin.",
            "papa|On avance avec le bol ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le bras porte le panier, tout contre la manche.",
            "copine|Ça gratte quand je marche.",
            "enfant-m|Ne le perds pas.",
            "narrateur|Une goutte tombe d'une mèche de Sarah.",
            "papa|Ça sent encore le savon, sur tes cheveux.",
            "maman|Vos mains, au-dessus du panier ?",
            "copine|Oui, maman.",
        )
    return L(
        "narrateur|Le bras porte la nappe, toute légère.",
        "copine|Elle a un pli, déjà.",
        "enfant-m|On va l'ouvrir.",
        "narrateur|Le ciré de Sarah cache encore ses poignets.",
        "maman|Le treillis est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|La serre fume un peu, tout bas.",
        "narrateur|Sous le tilleul, l'herbe goutte.",
        "narrateur|Le treillis attend, tout rouge.",
        "papa|Vous allez où, pour les groseilles ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Raphaël pose le bol au bord de la serre.",
            2: "narrateur|Raphaël pose le panier au bord de la serre.",
            3: "narrateur|Raphaël déplie la nappe au bord de la serre.",
        }[t1]
        mishap = {
            1: "narrateur|Le bol glisse, Sarah ne le voit plus.",
            2: "narrateur|Le panier vise à côté : Sarah visait trop bas.",
            3: "narrateur|La nappe se plie, Sarah cherche le bord trop bas.",
        }[t1]
        return L(
            lead,
            "narrateur|La vitre est chaude, encore un peu voilée.",
            "copine|Je vois un nuage sur mes lunettes !",
            "narrateur|Un rond de buée cache les grains.",
            mishap,
            f"enfant-m|{o['cap']} n'attendait pas ça.",
            "maman|La goutte a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, elle un peu flou.",
            "copine|On fait comment, alors ?",
            "papa|Les grains sont flous, vous faites quoi ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Raphaël pose le bol sous le tilleul.",
            2: "narrateur|Raphaël pose le panier sous le tilleul.",
            3: "narrateur|Raphaël déplie la nappe sous le tilleul.",
        }[t1]
        mishap = {
            1: "narrateur|Une mèche mouillée couvre le bol.",
            2: "narrateur|Le panier accroche une mèche, pas un grain.",
            3: "narrateur|Une goutte de cheveu tombe sur la nappe.",
        }[t1]
        return L(
            lead,
            "enfant-m|Ici, les feuilles gouttent, Sarah.",
            "copine|Mes cheveux sont encore lourds.",
            mishap,
            "narrateur|Une goutte tape l'herbe, toc.",
            "maman|Ils sèchent, tout doux, ce n'est rien.",
            "papa|Toi tes cheveux tiennent, les siens gouttent.",
            "enfant-m|On peut cueillir avec elle ?",
            "papa|Les mèches tombent, vous faites quoi ?",
        )
    lead = {
        1: "narrateur|Raphaël tend le bol vers le treillis.",
        2: "narrateur|Raphaël glisse le panier entre les tiges.",
        3: "narrateur|Raphaël pose la nappe sous le treillis.",
    }[t1]
    mishap = {
        1: "narrateur|Une manche trop longue emporte le bol.",
        2: "narrateur|Une manche trop longue balaie le panier.",
        3: "narrateur|Une manche trop longue froisse la nappe.",
    }[t1]
    return L(
        lead,
        "enfant-m|Les grains sont notre goûter, Sarah.",
        "copine|Mon ciré me suit jusqu'aux genoux !",
        mishap,
        f"narrateur|{o['cap']} disparaît un instant, sous le tissu.",
        "maman|Le ciré est un peu grand, c'est tout.",
        "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
        "copine|On fait comment, alors ?",
        "papa|Le ciré et les grains, vous faites comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La buée reste sur les verres, tout douce.",
            "papa|Le torchon, les mains, ou un pas hors de la serre ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Une mèche mouillée touche encore un grain.",
            "maman|L'élastique, la serviette, ou tenir le bol ?",
        )
    return L(
        "narrateur|Les manches cachent encore les grains rouges.",
        "papa|Les manches, le panier, ou nouer les poignets ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wipe = {
            1: "narrateur|Sarah essuie, puis reprend le bord du bol.",
            2: "narrateur|Sarah essuie, puis reprend l'anse du panier.",
            3: "narrateur|Sarah essuie, puis reprend le pli de la nappe.",
        }[t1]
        return L(
            "enfant-m|Maman, le torchon, s'il te plaît.",
            "maman|Tiens, tout doux, sur les verres.",
            "narrateur|Sarah frotte un rond, puis un autre.",
            wipe,
            "copine|Je vois les grains !",
            "enfant-m|Le rouge est à toi, maintenant.",
            "narrateur|Les lunettes rendent le treillis tout net.",
            "papa|Vous cueillez, chacun avec ce qu'il a.",
            "maman|Le torchon a rendu la serre.",
        )
    if t2 == 1 and t3 == 2:
        touch = {
            1: "narrateur|Sarah palpe le bol, Raphaël parle.",
            2: "narrateur|Sarah palpe le panier, Raphaël parle.",
            3: "narrateur|Sarah palpe la nappe, Raphaël parle.",
        }[t1]
        return L(
            "enfant-m|Tu cueilles avec tes mains, Sarah.",
            "copine|Je touche, toi tu dis où.",
            touch,
            "narrateur|Sous la vitre, deux silhouettes avancent.",
            "enfant-m|Le grain est à gauche, tout froid.",
            "copine|Je le tiens !",
            f"narrateur|{o['cap']} guide encore le geste.",
            "papa|Les mains ont vu à la place des verres.",
            "maman|La serre vous a gardés.",
        )
    if t2 == 1 and t3 == 3:
        air = {
            1: "narrateur|Le bol attend au bord, puis se pose.",
            2: "narrateur|Le panier craque un peu, puis s'apaise.",
            3: "narrateur|La nappe glisse, puis le tissu se tait.",
        }[t1]
        return L(
            "enfant-m|On recule un peu, papa ?",
            "papa|Un pas, hors de la buée, pas plus.",
            "narrateur|L'air sec chasse la buée, tout lent.",
            air,
            "copine|Ça redevient clair !",
            "enfant-m|Les groseilles peuvent tomber.",
            "narrateur|Sarah ajuste ses lunettes, tout net.",
            "maman|La goutte est partie, le jeu reste.",
            "papa|Vous avez attendu le verre clair.",
        )
    if t2 == 2 and t3 == 1:
        high = {
            1: "narrateur|Raphaël pose le bol, hors des mèches.",
            2: "narrateur|Raphaël tend le panier, hors des mèches.",
            3: "narrateur|Raphaël ouvre la nappe, hors des mèches.",
        }[t1]
        return L(
            "enfant-m|On met l'élastique, plus haut.",
            "copine|Mes cheveux restent en arrière, alors.",
            high,
            "narrateur|Maman noue l'élastique, tout doux.",
            "narrateur|Les mèches de Sarah tiennent, libres.",
            "enfant-m|Tu peux te pencher, maintenant.",
            "copine|La feuille ne m'attrape plus.",
            "papa|Chacun a sa hauteur, sous le tilleul.",
            "maman|Les cheveux ont eu leur place.",
        )
    if t2 == 2 and t3 == 2:
        dry = {
            1: "narrateur|Le bol attend, le temps d'un frottement.",
            2: "narrateur|Le panier attend, le temps d'un frottement.",
            3: "narrateur|La nappe attend, le temps d'un frottement.",
        }[t1]
        pose = {
            1: "enfant-m|On pose le bol, maintenant.",
            2: "enfant-m|On tend le panier, maintenant.",
            3: "enfant-m|On ouvre la nappe, maintenant.",
        }[t1]
        return L(
            "enfant-m|La serviette, maman ?",
            "maman|Frotte, tout doux, pas trop fort.",
            "narrateur|Sarah essuie une mèche, puis une autre.",
            dry,
            "copine|Elles sont plus légères !",
            pose,
            "narrateur|La feuille goutte, sans emporter de cheveu.",
            "papa|Vous avez laissé l'eau des cheveux.",
            "maman|Le tilleul sent encore le savon.",
        )
    if t2 == 2 and t3 == 3:
        hold = {
            1: "narrateur|Sarah tient le bol, Raphaël cueille.",
            2: "narrateur|Sarah tient le panier à deux mains, sans se pencher.",
            3: "narrateur|Sarah tient le bol, Raphaël ouvre la nappe.",
        }[t1]
        return L(
            "enfant-m|Tu tiens le bol, moi je cueille.",
            "copine|Mes mains font le bord, alors.",
            hold,
            "narrateur|Les grains tombent quand Sarah recule.",
            "narrateur|Ils s'arrêtent quand elle avance.",
            "enfant-m|C'est toi le bol vivant, Sarah !",
            "copine|Et toi les grains.",
            "papa|Vous cueillez avec ce que vous avez.",
            "maman|Les cheveux n'ont plus besoin d'être dans les feuilles.",
        )
    if t2 == 3 and t3 == 1:
        roll = {
            1: "narrateur|Les manches remontent, le bol redevient libre.",
            2: "narrateur|Les manches remontent, le panier redevient visible.",
            3: "narrateur|Les manches remontent, la nappe redevient visible.",
        }[t1]
        return L(
            "enfant-m|On retrousse, Sarah.",
            "copine|Jusqu'au coude, comme papa.",
            "narrateur|Deux rouleaux de tissu tiennent, un peu épais.",
            roll,
            "enfant-m|Je te vois les mains, maintenant.",
            "copine|Le grain n'est plus dans le ciré.",
            f"narrateur|{o['cap']} reprend sa place, au milieu.",
            "papa|Les manches ont laissé les grains passer.",
            "maman|Le ciré reste, plus court aux poignets.",
        )
    if t2 == 3 and t3 == 2:
        split = {
            1: "narrateur|Raphaël tient le panier, Sarah pose le bol.",
            2: "narrateur|Raphaël tient le panier, Sarah y glisse un grain.",
            3: "narrateur|Raphaël tient le panier, Sarah ouvre la nappe.",
        }[t1]
        return L(
            "enfant-m|Moi je tiens le panier.",
            "copine|Moi je guide, près des tiges.",
            split,
            "narrateur|Les manches trop longues bougent le tissu, seulement.",
            "narrateur|Les grains restent hors du ciré.",
            "copine|Le treillis s'ouvre !",
            "enfant-m|Le rouge sort, tout vif.",
            "papa|Chacun a pris sa part, à sa taille.",
            "maman|Les tiges ont tenu les grains.",
        )
    bind = {
        1: "narrateur|L'élastique tient une manche, le bol l'autre main.",
        2: "narrateur|L'élastique tient une manche, le panier l'autre main.",
        3: "narrateur|L'élastique tient une manche, la nappe reste droite.",
    }[t1]
    return L(
        "enfant-m|Maman, ton élastique, s'il te plaît.",
        "maman|Un pour chaque manche, tout doux.",
        "narrateur|Sarah tend les poignets, maman noue.",
        bind,
        "copine|Mes mains sont nues, maintenant.",
        "enfant-m|Les groseilles peuvent tomber.",
        "narrateur|Le rouge avance entre les tiges.",
        "papa|Vous avez demandé, et ça tient.",
        "maman|Mes élastiques ont gardé le ciré.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La serre sent encore le torchon tiède.",
            "copine|J'ai vu le grain, tout net.",
            "enfant-m|Tes lunettes ont trouvé le rouge.",
            "papa|Vous avez cueilli, chacun avec sa vue.",
            "maman|Les vitres sèchent déjà, tout doux.",
            coda,
            "narrateur|Une goutte reste sur un grain, ronde.",
            "enfant-m|On rentre, Sarah.",
            "narrateur|La serre redevient calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous la vitre, l'air est encore un peu chaud.",
            "enfant-m|Tu as touché, moi j'ai dit où.",
            "copine|Mes mains ont vu le rouge.",
            "papa|Les verres flous n'ont pas arrêté les grains.",
            "maman|La serre se tait, enfin.",
            coda,
            "narrateur|Une ombre de grain reste au fond.",
            "enfant-m|À demain, les groseilles.",
            "narrateur|Le rebord redevient tiède, déjà.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Un filet d'air sec reste près de la serre.",
            "copine|La buée est partie, tout seule.",
            "enfant-m|On a attendu le verre clair.",
            "maman|Le pas en arrière a rendu les grains.",
            "papa|Vous avez laissé le temps aux lunettes.",
            coda,
            "narrateur|Raphaël souffle sur un grain, tout léger.",
            "copine|Il brille encore.",
            "narrateur|La vitre reprend, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le tilleul garde encore un peu d'ombre.",
            "enfant-m|L'élastique était trop bas, d'abord.",
            "copine|Mes cheveux sont restés libres.",
            "papa|Chacun a eu sa hauteur, sous les feuilles.",
            "maman|L'herbe sèche déjà.",
            coda,
            "narrateur|Une mèche sèche contre le col, tout calme.",
            "enfant-m|On rentre, le tilleul reste.",
            "narrateur|Une feuille reprend sa place, tout bas.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La serviette sent encore le savon.",
            "copine|Tu as frotté, tout doux.",
            "enfant-m|Puis on a cueilli, sans emporter de cheveu.",
            "maman|L'eau des cheveux s'en est allée.",
            "papa|Le tilleul vous rend le silence.",
            coda,
            "narrateur|Raphaël souffle dessus, tout léger.",
            "copine|Elle part.",
            "narrateur|Le savon s'efface déjà de l'herbe.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains de Sarah gardent encore le pli du bol.",
            "enfant-m|Tu étais le bol vivant.",
            "copine|Toi les grains, moi le bord.",
            "papa|Vous avez cueilli avec ce que vous aviez.",
            "maman|Les cheveux n'avaient plus besoin d'être pris.",
            coda,
            "narrateur|Un rebord vide attend, tout bas.",
            "enfant-m|On se dit au revoir, tilleul.",
            "narrateur|Les chaussons glissent vers la maison.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Deux rouleaux de manches tiennent encore.",
            "enfant-m|Tes mains sont sorties du ciré.",
            "copine|Le grain n'était plus avalé.",
            "papa|Les manches ont laissé les grains passer.",
            "maman|Les tiges redeviennent des tiges, tout simples.",
            coda,
            "narrateur|Un grain rouge reste sur le bois.",
            "enfant-m|On rentre, Sarah.",
            "narrateur|Le treillis reprend sa forme, tout lent.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Une goutte tombe encore d'une feuille.",
            "copine|Tu tenais le panier, moi le bord.",
            "enfant-m|Tes manches bougeaient seulement le tissu.",
            "maman|Chacun a pris sa part, à sa taille.",
            "papa|Les tiges ont tenu jusqu'au bout.",
            coda,
            "narrateur|Raphaël lisse un grain, tout doux.",
            "copine|Il a bien roulé.",
            "narrateur|Le mur reprend son calme, déjà.",
        )
    return L(
        "narrateur|Deux élastiques veillent encore aux poignets.",
        "enfant-m|On a demandé, et ça tenait.",
        "copine|Mes mains étaient nues, pour les grains.",
        "papa|Vous avez demandé, rien de plus.",
        "maman|Mes élastiques rentrent dans la poche.",
        coda,
        "narrateur|Un peu de terre reste au rebord.",
        "enfant-m|Les groseilles sont à nous.",
        "narrateur|Le jardin sent encore la pluie d'hier.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Un merle saute dans l'herbe encore mouillée.",
        "narrateur|Des gouttes pendent aux feuilles du tilleul.",
        "narrateur|Ça sent la terre et la feuille froissée.",
        "narrateur|Le treillis du fond porte des groseilles.",
        "papa|Tu as vu les grains, Raphaël ?",
        "enfant-m|Ils brillent, tout petits.",
        "maman|Le bol blanc attend, près de la marche.",
        "narrateur|En ce moment, Raphaël le prend, tout doux.",
        "enfant-m|Je veux le remplir, pour le goûter.",
        "narrateur|La porte de la maison claque, tout bas.",
        "copine|J'arrive, Raphaël !",
        "narrateur|Les lunettes de Sarah gardent un rond de buée.",
        "narrateur|Ses cheveux gouttent sur le ciré trop long.",
        "papa|Merci, tu tiens déjà le bol.",
        "maman|On l'emmène aux grains, alors ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près de la marche, le bol blanc attend.",
        "narrateur|Le panier d'osier dort, vide.",
        "narrateur|La nappe à carreaux est pliée.",
        "maman|Tu prends quoi d'abord, Raphaël ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bol blanc", "le panier d'osier", "la nappe à carreaux")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        t1_ask = {
            1: "maman|Le bol est où ?",
            2: "maman|Le panier est où ?",
            3: "maman|La nappe est où ?",
        }[t1]
        s[f"{p}_Q0001"] = L(
            f"narrateur|{o['t1line']}",
            t1_ask,
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la serre", "le tilleul", "le treillis")

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
        "Raphaël veut remplir un bol de groseilles rouges pour le goûter. "
        "Sarah arrive, lunettes encore floues, cheveux mouillés, ciré jaune "
        "trop long. T1 = bol blanc / panier d'osier / nappe à carreaux (les trois "
        "partent). T2 = serre (buée sur les verres) / tilleul (mèches dans les "
        "feuilles) / treillis (manches trop longues). T3 = neuf résolutions "
        "(torchon, mains, pas hors de la serre ; élastique, serviette, tenir le "
        "bol ; manches, Raphaël tient, nouer les poignets). On cueille ensemble, "
        "sans slogan. Fin : le bol rentre, tout rouge.",
        "N2 ≤ 15. Jules / Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-016 "
        "(pas la tarte), DIF-026 (pas le théâtre) et DIF-036 (pas le poisson, "
        "pas le lavoir). Jardin : serre, tilleul, treillis. Un merci de papa "
        "lié au geste (tenir le bol). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
