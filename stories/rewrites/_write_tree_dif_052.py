#!/usr/bin/env python3
"""TREE-DIF-052 — Le phare de coquillages de Mila (N1, DIF.COR.003)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-052"
N1 = LIMITS["N1"]
TITLE = "Le phare de coquillages de Mila"
FIL = (
    "Mila veut un phare de coquillages sur le rocher, avant la marée. "
    "Sarah arrive, lunettes voilées d'eau, cheveux collés de sel, ciré trop long. "
    "Elles emportent la clochette, le seau bleu et la pelle jaune. "
    "À la jetée les verres se voilent, à la dune les mèches collent, "
    "dans l'écume les manches trempent. Elles bâtissent ensemble. "
    "Le phare tient. On rentre, le sel aux doigts."
)
CHARS = "Mila, Sarah, papa, maman"
SETTING = "bord de mer : jetée, dune, écume, avant la marée"


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
        "galet",
        "lunettes, cheveux",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "phare" not in blob and "coquillage" not in blob:
        raise SystemExit(f"{SID}: phare/coquillages absents")
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
        "lab": "la clochette",
        "cap": "La clochette",
        "short": "la cloche",
        "t1q": "dans la main",
        "t1line": "La clochette est dans la main.",
        "t1acc": "main | la main | dans la main | sa main",
        "t1retry": "La cloche est dans la main.",
        "coda": "narrateur|La clochette rentre, encore salée.",
    },
    2: {
        "lab": "le seau bleu",
        "cap": "Le seau bleu",
        "short": "le seau",
        "t1q": "au bras",
        "t1line": "Le seau bleu est au bras.",
        "t1acc": "bras | le bras | au bras | son bras",
        "t1retry": "Le seau est au bras.",
        "coda": "narrateur|Le seau bleu sèche près de la porte.",
    },
    3: {
        "lab": "la pelle jaune",
        "cap": "La pelle jaune",
        "short": "la pelle",
        "t1q": "sous le bras",
        "t1line": "La pelle jaune est sous le bras.",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "La pelle est sous le bras.",
        "coda": "narrateur|La pelle jaune retrouve le sac.",
    },
}

T3_LABS = {
    1: ("le torchon de maman", "les mains de Sarah", "un pas hors des gouttes"),
    2: ("le bandeau de maman", "la serviette", "Sarah tient le seau"),
    3: ("les manches retroussées", "Mila tient la pelle", "maman noue les poignets"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila glisse d'abord la cloche dans sa main.",
            "enfant-f|Elle est encore un peu froide.",
            "maman|Garde-la près de toi, tout doux.",
            "narrateur|Le métal brille, tout net.",
            "papa|Le seau, ensuite, au bras.",
            "narrateur|Sarah prend la pelle, sous le bras.",
            "narrateur|Tout part avec elles, vers la mer.",
            "enfant-f|Sarah, tu viens ?",
            "copine|Je suis là, même un peu floue.",
            "papa|La cloche d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila enroule d'abord le seau au bras.",
            "enfant-f|Le bleu gratte un peu, contre le coude.",
            "papa|Garde-le au bras, tout doux.",
            "narrateur|Le plastique fait un petit froissement.",
            "maman|La cloche, ensuite, dans la main.",
            "narrateur|Sarah prend la pelle, sous le bras.",
            "narrateur|Elles avancent, les affaires avec elles.",
            "enfant-f|Sarah, tu portes la pelle ?",
            "copine|Je la tiens, mes lunettes glissent.",
            "maman|Le seau d'abord, il est prêt.",
        )
    return L(
        "narrateur|Mila glisse d'abord la pelle, sous le bras.",
        "enfant-f|Le bois sent encore le sac.",
        "maman|Serre-la sous le bras, tout droit.",
        "narrateur|Le bois fait un petit froissement.",
        "papa|La cloche et le seau, avec vous.",
        "narrateur|Il les pose près du sac.",
        "narrateur|Les trois affaires restent ensemble.",
        "enfant-f|Sarah, vite !",
        "narrateur|Le ciré jaune traîne sur le sable.",
        "copine|Je suis près du rocher.",
        "enfant-f|Je te garde un coin de seau.",
        "papa|La pelle d'abord, elle est prête.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La main porte la cloche, tout contre le tissu.",
            "copine|Je vois le métal, un peu flou.",
            "enfant-f|C'est pour le phare.",
            "narrateur|Les lunettes de Sarah gardent un rond d'eau.",
            "maman|Les coquillages vous attendent, plus loin.",
            "papa|On avance avec la cloche ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le bras porte le seau, tout contre la manche.",
            "copine|Ça gratte quand je marche.",
            "enfant-f|Ne le perds pas.",
            "narrateur|Une goutte tombe d'une mèche de Sarah.",
            "papa|Ça sent encore le sel, sur tes cheveux.",
            "maman|Vos mains, au-dessus du seau ?",
            "copine|Oui, maman.",
        )
    return L(
        "narrateur|Le bras porte la pelle, toute légère.",
        "copine|Elle a un grain de sable, déjà.",
        "enfant-f|On va creuser.",
        "narrateur|Le ciré de Sarah cache encore ses poignets.",
        "maman|Le rocher est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Dehors, l'eau brille encore un peu.",
        "narrateur|Un chemin part sur la jetée, un autre grimpe.",
        "narrateur|L'écume fait comme une petite île.",
        "papa|Quelle route, pour le phare ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Mila pose la cloche au bord de la jetée.",
            2: "narrateur|Mila pose le seau au bord de la jetée.",
            3: "narrateur|Mila pose la pelle au bord de la jetée.",
        }[t1]
        mishap = {
            1: "narrateur|La cloche glisse, Sarah ne la voit plus.",
            2: "narrateur|Le seau vise trop bas, tout flou.",
            3: "narrateur|La pelle part trop bas, tout flou.",
        }[t1]
        return L(
            lead,
            "narrateur|Le bois est mouillé, encore un peu voilé.",
            "copine|Je vois un nuage sur mes lunettes !",
            "narrateur|Un rond d'eau cache les coquillages.",
            mishap,
            f"enfant-f|{o['cap']} n'attendait pas ça.",
            "maman|La goutte a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, elle un peu flou.",
            "copine|On fait comment, alors ?",
            "papa|Les coquillages sont flous, vous faites quoi ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Mila pose la cloche sur la dune.",
            2: "narrateur|Mila pose le seau sur la dune.",
            3: "narrateur|Mila pose la pelle sur la dune.",
        }[t1]
        mishap = {
            1: "narrateur|Une mèche collée couvre la cloche.",
            2: "narrateur|Le seau accroche une mèche, pas un coquillage.",
            3: "narrateur|Une goutte de cheveu tombe sur la pelle.",
        }[t1]
        return L(
            lead,
            "enfant-f|Ici, le vent pousse, Sarah.",
            "copine|Mes cheveux sont encore lourds.",
            mishap,
            "narrateur|Une goutte de sel tape le sable.",
            "maman|Ils sèchent, tout doux, ce n'est rien.",
            "papa|Toi tes cheveux tiennent, les siens collent.",
            "enfant-f|On peut bâtir avec elle ?",
            "papa|Les mèches tombent, vous faites quoi ?",
        )
    lead = {
        1: "narrateur|Mila tend la cloche vers l'écume.",
        2: "narrateur|Mila glisse le seau vers l'écume.",
        3: "narrateur|Mila pose la pelle près de l'écume.",
    }[t1]
    mishap = {
        1: "narrateur|Une manche trop longue emporte la cloche.",
        2: "narrateur|Une manche trop longue balaie le seau.",
        3: "narrateur|Une manche trop longue cache la pelle.",
    }[t1]
    return L(
        lead,
        "enfant-f|Les coquillages sont notre phare, Sarah.",
        "copine|Mon ciré me suit jusqu'aux genoux !",
        mishap,
        f"narrateur|{o['cap']} disparaît un instant, sous le tissu.",
        "maman|Le ciré est un peu grand, c'est tout.",
        "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
        "copine|On fait comment, alors ?",
        "papa|Le ciré et les coquillages, vous faites comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'eau reste sur les verres, tout douce.",
            "papa|Le torchon, les mains, ou un pas dehors ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Une mèche collée touche encore un coquillage.",
            "maman|Le bandeau, la serviette, ou tenir le seau ?",
        )
    return L(
        "narrateur|Les manches cachent encore les coquillages.",
        "papa|Les manches, la pelle, ou nouer les poignets ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wipe = {
            1: "narrateur|Sarah essuie, puis reprend le bord de la cloche.",
            2: "narrateur|Sarah essuie, puis reprend l'anse du seau.",
            3: "narrateur|Sarah essuie, puis reprend le manche de la pelle.",
        }[t1]
        return L(
            "enfant-f|Maman, le torchon, s'il te plaît.",
            "maman|Tiens, tout doux, sur les verres.",
            "narrateur|Sarah frotte un rond, puis un autre.",
            wipe,
            "copine|Je vois les coquillages !",
            "enfant-f|Le rose est à toi, maintenant.",
            "narrateur|Les lunettes rendent le rocher tout net.",
            "papa|Vous bâtissez, chacune avec ce qu'elle a.",
            "maman|Le torchon a rendu la jetée.",
        )
    if t2 == 1 and t3 == 2:
        touch = {
            1: "narrateur|Sarah palpe la cloche, Mila parle.",
            2: "narrateur|Sarah palpe le seau, Mila parle.",
            3: "narrateur|Sarah palpe la pelle, Mila parle.",
        }[t1]
        return L(
            "enfant-f|Tu bâtis avec tes mains, Sarah.",
            "copine|Je touche, toi tu dis où.",
            touch,
            "narrateur|Sur le bois, deux silhouettes avancent.",
            "enfant-f|Le coquillage est à gauche, tout froid.",
            "copine|Je le tiens !",
            f"narrateur|{o['cap']} guide encore le geste.",
            "papa|Les mains ont vu à la place des verres.",
            "maman|La jetée vous a gardées.",
        )
    if t2 == 1 and t3 == 3:
        air = {
            1: "narrateur|La cloche attend au bord, puis se pose.",
            2: "narrateur|Le seau craque un peu, puis s'apaise.",
            3: "narrateur|La pelle glisse, puis le bois se tait.",
        }[t1]
        return L(
            "enfant-f|On recule un peu, papa ?",
            "papa|Un pas, hors des gouttes, pas plus.",
            "narrateur|L'air sec chasse l'eau, tout lent.",
            air,
            "copine|Ça redevient clair !",
            "enfant-f|Les coquillages peuvent s'empiler.",
            "narrateur|Sarah ajuste ses lunettes, tout net.",
            "maman|La goutte est partie, le jeu reste.",
            "papa|Vous avez attendu le verre clair.",
        )
    if t2 == 2 and t3 == 1:
        high = {
            1: "narrateur|Mila pose la cloche, hors des mèches.",
            2: "narrateur|Mila tend le seau, hors des mèches.",
            3: "narrateur|Mila ouvre la pelle, hors des mèches.",
        }[t1]
        return L(
            "enfant-f|On met le bandeau, plus haut.",
            "copine|Mes cheveux restent en arrière, alors.",
            high,
            "narrateur|Maman noue le bandeau, tout doux.",
            "narrateur|Les mèches de Sarah tiennent, libres.",
            "enfant-f|Tu peux te pencher, maintenant.",
            "copine|Le vent ne m'attrape plus.",
            "papa|Chacune a sa hauteur, sur la dune.",
            "maman|Les cheveux ont eu leur place.",
        )
    if t2 == 2 and t3 == 2:
        dry = {
            1: "narrateur|La cloche attend, le temps d'un frottement.",
            2: "narrateur|Le seau attend, le temps d'un frottement.",
            3: "narrateur|La pelle attend, le temps d'un frottement.",
        }[t1]
        pose = {
            1: "enfant-f|On pose la cloche, maintenant.",
            2: "enfant-f|On tend le seau, maintenant.",
            3: "enfant-f|On ouvre la pelle, maintenant.",
        }[t1]
        return L(
            "enfant-f|La serviette, maman ?",
            "maman|Frotte, tout doux, pas trop fort.",
            "narrateur|Sarah essuie une mèche, puis une autre.",
            dry,
            "copine|Elles sont plus légères !",
            pose,
            "narrateur|Le vent pousse, sans emporter de cheveu.",
            "papa|Vous avez laissé l'eau des cheveux.",
            "maman|La dune sent encore le sel.",
        )
    if t2 == 2 and t3 == 3:
        hold = {
            1: "narrateur|Sarah tient le seau, Mila pose la cloche.",
            2: "narrateur|Sarah tient le seau à deux mains, sans se pencher.",
            3: "narrateur|Sarah tient le seau, Mila ouvre la pelle.",
        }[t1]
        return L(
            "enfant-f|Tu tiens le seau, moi je pose.",
            "copine|Mes mains font le bord, alors.",
            hold,
            "narrateur|Les coquillages tombent quand Sarah recule.",
            "narrateur|Ils s'arrêtent quand elle avance.",
            "enfant-f|C'est toi le seau vivant, Sarah !",
            "copine|Et toi les coquillages.",
            "papa|Vous bâtissez avec ce que vous avez.",
            "maman|Les cheveux n'ont plus besoin du vent.",
        )
    if t2 == 3 and t3 == 1:
        roll = {
            1: "narrateur|Les manches remontent, la cloche redevient libre.",
            2: "narrateur|Les manches remontent, le seau redevient visible.",
            3: "narrateur|Les manches remontent, la pelle redevient visible.",
        }[t1]
        return L(
            "enfant-f|On retrousse, Sarah.",
            "copine|Jusqu'au coude, comme papa.",
            "narrateur|Deux rouleaux de tissu tiennent, un peu épais.",
            roll,
            "enfant-f|Je te vois les mains, maintenant.",
            "copine|Le coquillage n'est plus dans le ciré.",
            f"narrateur|{o['cap']} reprend sa place, au milieu.",
            "papa|Les manches ont laissé les coquillages passer.",
            "maman|Le ciré reste, plus court aux poignets.",
        )
    if t2 == 3 and t3 == 2:
        split = {
            1: "narrateur|Mila tient la pelle, Sarah pose la cloche.",
            2: "narrateur|Mila tient la pelle, Sarah y glisse un coquillage.",
            3: "narrateur|Mila tient la pelle, Sarah ouvre le seau.",
        }[t1]
        return L(
            "enfant-f|Moi je tiens la pelle.",
            "copine|Moi je guide, près de l'eau.",
            split,
            "narrateur|Les manches trop longues bougent le tissu, seulement.",
            "narrateur|Les coquillages restent hors du ciré.",
            "copine|L'écume s'ouvre !",
            "enfant-f|Le rose sort, tout vif.",
            "papa|Chacune a pris sa part, à sa taille.",
            "maman|L'eau a tenu les coquillages.",
        )
    bind = {
        1: "narrateur|L'élastique tient une manche, la cloche l'autre main.",
        2: "narrateur|L'élastique tient une manche, le seau l'autre main.",
        3: "narrateur|L'élastique tient une manche, la pelle reste droite.",
    }[t1]
    return L(
        "enfant-f|Maman, ton élastique, s'il te plaît.",
        "maman|Un pour chaque manche, tout doux.",
        "narrateur|Sarah tend les poignets, maman noue.",
        bind,
        "copine|Mes mains sont nues, maintenant.",
        "enfant-f|Les coquillages peuvent s'empiler.",
        "narrateur|Le rose avance dans l'écume.",
        "papa|Vous avez demandé, et ça tient.",
        "maman|Mes élastiques ont gardé le ciré.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La jetée sent encore le torchon tiède.",
            "copine|J'ai vu le coquillage, tout net.",
            "enfant-f|Tes lunettes ont trouvé le rose.",
            "papa|Vous avez bâti, chacune avec sa vue.",
            "maman|Le bois sèche déjà, tout doux.",
            coda,
            "narrateur|Une goutte reste sur un coquillage, ronde.",
            "enfant-f|On rentre, Sarah.",
            "narrateur|La jetée redevient calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sur le bois, l'air est encore un peu chaud.",
            "enfant-f|Tu as touché, moi j'ai dit où.",
            "copine|Mes mains ont vu le rose.",
            "papa|Les verres flous n'ont pas arrêté le phare.",
            "maman|La jetée se tait, enfin.",
            coda,
            "narrateur|Une ombre de coquillage reste au fond.",
            "enfant-f|À demain, le rocher.",
            "narrateur|Le rebord redevient tiède, déjà.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Un filet d'air sec reste près de la jetée.",
            "copine|L'eau est partie, tout seule.",
            "enfant-f|On a attendu le verre clair.",
            "maman|Le pas en arrière a rendu les coquillages.",
            "papa|Vous avez laissé le temps aux lunettes.",
            coda,
            "narrateur|Mila souffle sur un coquillage, tout léger.",
            "copine|Il brille encore.",
            "narrateur|Le bois reprend, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|La dune garde encore un peu d'ombre.",
            "enfant-f|Le bandeau était trop bas, d'abord.",
            "copine|Mes cheveux sont restés libres.",
            "papa|Chacune a eu sa hauteur, sous le vent.",
            "maman|Le sable sèche déjà.",
            coda,
            "narrateur|Une mèche sèche contre le col, tout calme.",
            "enfant-f|On rentre, la dune reste.",
            "narrateur|Un brin d'herbe reprend sa place, tout bas.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La serviette sent encore le sel.",
            "copine|Tu as frotté, tout doux.",
            "enfant-f|Puis on a bâti, sans emporter de cheveu.",
            "maman|L'eau des cheveux s'en est allée.",
            "papa|La dune vous rend le silence.",
            coda,
            "narrateur|Mila souffle dessus, tout léger.",
            "copine|Elle part.",
            "narrateur|Le sel s'efface déjà du sable.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains de Sarah gardent encore le pli du seau.",
            "enfant-f|Tu étais le seau vivant.",
            "copine|Toi les coquillages, moi le bord.",
            "papa|Vous avez bâti avec ce que vous aviez.",
            "maman|Les cheveux n'avaient plus besoin d'être pris.",
            coda,
            "narrateur|Un rebord vide attend, tout bas.",
            "enfant-f|On se dit au revoir, dune.",
            "narrateur|Les chaussons glissent vers la maison.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Deux rouleaux de manches tiennent encore.",
            "enfant-f|Tes mains sont sorties du ciré.",
            "copine|Le coquillage n'était plus avalé.",
            "papa|Les manches ont laissé les coquillages passer.",
            "maman|L'écume redevient de l'eau, tout simple.",
            coda,
            "narrateur|Un coquillage rose reste sur le bois.",
            "enfant-f|On rentre, Sarah.",
            "narrateur|L'écume reprend sa forme, tout lente.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Une goutte tombe encore d'une manche.",
            "copine|Tu tenais la pelle, moi le bord.",
            "enfant-f|Tes manches bougeaient seulement le tissu.",
            "maman|Chacune a pris sa part, à sa taille.",
            "papa|L'eau a tenu jusqu'au bout.",
            coda,
            "narrateur|Mila lisse un coquillage, tout doux.",
            "copine|Il a bien roulé.",
            "narrateur|La vague reprend son calme, déjà.",
        )
    return L(
        "narrateur|Deux élastiques veillent encore aux poignets.",
        "enfant-f|On a demandé, et ça tenait.",
        "copine|Mes mains étaient nues, pour les coquillages.",
        "papa|Vous avez demandé, rien de plus.",
        "maman|Mes élastiques rentrent dans la poche.",
        coda,
        "narrateur|Un peu de sable reste au rebord.",
        "enfant-f|Les coquillages sont à nous.",
        "narrateur|La mer sent encore le vent d'hier.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La maison tient au-dessus de la mer.",
        "narrateur|Les volets claquent, tout salés.",
        "narrateur|Ça sent le sel et le bois mouillé.",
        "narrateur|Le rocher gris attend, tout bas.",
        "papa|Tu as vu les coquillages, Mila ?",
        "enfant-f|Ils brillent, tout petits.",
        "maman|La clochette dort, près du sac.",
        "narrateur|En ce moment, Mila la prend, tout doux.",
        "enfant-f|Je veux un phare, avant la mer.",
        "narrateur|Des pas sonnent sur le chemin.",
        "copine|J'arrive, Mila !",
        "narrateur|Les lunettes de Sarah gardent un rond d'eau.",
        "narrateur|Ses cheveux collent au ciré trop long.",
        "papa|Merci, tu tiens déjà la cloche.",
        "maman|On l'emmène au rocher, alors ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près du sac, la clochette attend.",
        "narrateur|Le seau bleu dort, vide.",
        "narrateur|La pelle jaune est posée.",
        "maman|Tu prends quoi d'abord, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la clochette", "le seau bleu", "la pelle jaune")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        t1_ask = {
            1: "maman|La cloche est où ?",
            2: "maman|Le seau est où ?",
            3: "maman|La pelle est où ?",
        }[t1]
        s[f"{p}_Q0001"] = L(
            f"narrateur|{o['t1line']}",
            t1_ask,
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la jetée", "la dune", "l'écume")

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
        "Mila veut un phare de coquillages sur le rocher, avant la marée. "
        "Sarah arrive, lunettes voilées d'eau, cheveux collés de sel, ciré trop long. "
        "T1 = clochette / seau bleu / pelle jaune (les trois partent). "
        "T2 = jetée (eau sur les verres) / dune (mèches dans le vent) / "
        "écume (manches trop longues). T3 = neuf résolutions "
        "(torchon, mains, pas hors des gouttes ; bandeau, serviette, tenir le seau ; "
        "manches, Mila tient la pelle, nouer les poignets). On bâtit ensemble, "
        "sans slogan. Fin : le phare tient, on rentre le sel aux doigts.",
        "N1 ≤ 10. Nora / Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-016 "
        "(pas la tarte), DIF-026 (pas le théâtre), DIF-036 (pas le poisson, "
        "pas le lavoir) et DIF-044 (pas les groseilles). Bord de mer : jetée, "
        "dune, écume. Un merci de papa lié au geste (tenir la cloche). "
        "Audio non cuit.",
    )


if __name__ == "__main__":
    main()
