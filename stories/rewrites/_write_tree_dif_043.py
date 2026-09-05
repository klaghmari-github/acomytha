#!/usr/bin/env python3
"""TREE-DIF-043 — Le pain de Nino et les deux canards. DIF.COR.002, N1."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-043"
N1 = LIMITS["N1"]
TITLE = "Le pain de Nino et les deux canards"
FIL = (
    "Au parc, Nino veut un vrai goûter pour deux canards. "
    "L'un a le ventre tout rond, l'autre le cou tout mince. "
    "Il prépare d'abord le pain, la nappe ou le seau ; les trois partent. "
    "À la mare trop haute, au banc trop fendu, au kiosque trop loin. "
    "Neuf façons de les garder ensemble. Les deux canards goûtent."
)
CHARS = "Nino, papa, maman"
SETTING = "parc du village : mare, banc, kiosque"


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
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"sans fin: {ph}")
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
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "hugo",
        "plus rond ou plus mince",
        "le corps n'est pas",
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "bon travail",
        "bravo tu as",
        "la première",
        "la deuxième",
        "la troisième",
        "capitaine",
        "plic",
        "volet jaune",
        "peluche",
        "défilé",
        "poupée",
        "cuisine",
        "dînette",
        "dinette",
        "après la sieste",
        "bac à sable",
        "toboggan",
        "balançoire",
        "chambre",
        "marché",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    check(SID, out["age_band"], out["chunks"])
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
        "lab": "le pain",
        "ans": "pain",
        "acc": "pain | le pain | d'abord le pain | la croûte",
        "retry": "Nino a pris le pain, d'abord.",
        "hip": "Le pain sent encore le four, tout chaud.",
        "wait": "Dans sa main, le pain attend.",
        "use": "Un peu de croûte reste, tout rêche.",
        "coda": "Une miette sèche sur l'herbe, déjà froide.",
    },
    2: {
        "lab": "la nappe",
        "ans": "nappe",
        "acc": "nappe | la nappe | d'abord la nappe | le tissu",
        "retry": "Nino a pris la nappe, d'abord.",
        "hip": "Un coin de nappe frotte l'herbe.",
        "wait": "Contre lui, la nappe chauffe déjà.",
        "use": "La nappe les abrite, tout doux.",
        "coda": "Un pli de nappe reste, encore tiède.",
    },
    3: {
        "lab": "le seau",
        "ans": "seau",
        "acc": "seau | le seau | d'abord le seau | le métal",
        "retry": "Nino a pris le seau, d'abord.",
        "hip": "Le seau tape sa jambe, à chaque pas.",
        "wait": "Sur l'herbe, le seau attend.",
        "use": "Un peu d'eau tremble au bord du seau.",
        "coda": "Une goutte sèche au fond du seau.",
    },
}

T3_LABS = {
    1: ("le bord", "deux tas", "le pont"),
    2: ("l'herbe", "le pied", "la nappe"),
    3: ("les marches", "plus près", "l'ombre"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord le pain, encore chaud.",
            "narrateur|La croûte casse un peu, entre ses doigts.",
            "enfant-m|Il sent le four.",
            "maman|Casse-le tout doux, pour eux.",
            "narrateur|Il en met un morceau dans le seau.",
            "narrateur|Puis il glisse la nappe sous le bras.",
            "enfant-m|Un ventre rond, un cou mince.",
            "papa|Deux canards, un goûter.",
            "narrateur|Près du sac, rien ne reste.",
            "maman|La nappe aussi, avec toi.",
            "enfant-m|On les prend.",
            "narrateur|Pain, nappe et seau avancent avec lui.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino prend d'abord la nappe, encore pliée.",
            "narrateur|Le tissu sent l'herbe, un peu.",
            "enfant-m|Elle est douce.",
            "papa|Déplie-la tout doux, pour eux.",
            "narrateur|Il la pose un instant sur le sac.",
            "narrateur|Le pain attend, déjà cassé.",
            "enfant-m|Un rond, et une ligne.",
            "maman|Tu as vu les deux formes.",
            "narrateur|Dans le seau, le pain attend.",
            "papa|Le seau aussi, pour plus tard.",
            "enfant-m|Je garde la nappe.",
            "narrateur|Les trois affaires partent avec lui.",
        )
    return L(
        "narrateur|Nino saisit d'abord le seau, encore vide.",
        "narrateur|Le seau cliquette une fois, tout sec.",
        "enfant-m|Il tient le pain.",
        "maman|C'est pour porter, tout doux.",
        "narrateur|Il y glisse un morceau de pain.",
        "narrateur|La nappe reste pliée, contre lui.",
        "enfant-m|Le seau va aux deux.",
        "papa|Oui, aux deux.",
        "narrateur|Près du sac, la nappe attend.",
        "maman|Le pain aussi.",
        "enfant-m|Je garde le seau.",
        "narrateur|Rien ne reste près du sac.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le pain.",
            "papa|Oui.",
            "narrateur|Nino glisse la nappe sous le bras.",
            "maman|Le seau, je te le tends.",
            "enfant-m|Merci.",
            "narrateur|Les deux canards avancent déjà.",
            "papa|Les deux viennent goûter.",
            "enfant-m|On cherche l'endroit.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La nappe.",
            "maman|Oui.",
            "narrateur|Il ramasse le pain, tout petit.",
            "papa|Le seau, dans l'autre main ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux canards tournent déjà.",
            "maman|Merci d'avoir pris les deux.",
            "enfant-m|On va où, maintenant ?",
        )
    return L(
        "enfant-m|Le seau.",
        "papa|Oui.",
        "narrateur|Maman lui passe le pain, déjà froid.",
        "maman|La nappe, sous le bras.",
        "enfant-m|Elle est là.",
        "narrateur|Les deux canards attendent l'eau.",
        "papa|Merci, Nino.",
        "enfant-m|On va à l'eau ?",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['hip']}",
        "narrateur|Les deux canards veulent manger.",
        "papa|La mare, le banc, ou le kiosque ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    hip = OBJ[t1]["hip"]
    if t2 == 1:
        extra = {
            1: "Un morceau de pain tombe, trop loin.",
            2: "La nappe accroche l'herbe, puis lâche.",
            3: "Le seau penche, une miette tombe.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Ils s'approchent de la mare, trop haute.",
            f"narrateur|{extra}",
            "narrateur|L'eau fait un pli, trop vif.",
            "enfant-m|Vous venez.",
            "narrateur|Le canard rond reste au bord.",
            "narrateur|Le mince part, trop léger, trop loin.",
            "enfant-m|L'un reste, l'autre part.",
            "maman|Ils n'ont pas la même forme.",
            "papa|Tu fais quoi, avec les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "Des miettes tombent entre les planches.",
            2: "La nappe glisse dans le vide, trop mince.",
            3: "Le seau cogne le bois, un toc.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Sur le banc, les planches ont des fentes.",
            f"narrateur|{extra}",
            "enfant-m|Le goûter, ici.",
            "narrateur|Nino s'assoit, trop haut pour eux.",
            "narrateur|Le canard rond bute, trop large.",
            "narrateur|Le mince glisse entre les planches.",
            "enfant-m|Ce n'est pas juste.",
            "papa|Le banc a des trous, voilà tout.",
            "maman|Tu les gardes comment, ensemble ?",
        )
    extra = {
        1: "Le pain sent encore, trop loin de l'eau.",
        2: "La nappe claque sur les marches, trop haut.",
        3: "Le seau tape une marche, trop haute.",
    }[t1]
    return L(
        f"narrateur|{hip}",
        "narrateur|Au kiosque, les marches sont trop hautes.",
        f"narrateur|{extra}",
        "enfant-m|Le goûter, là-haut.",
        "narrateur|Un vent passe, tout froid.",
        "narrateur|Le canard rond ne monte pas.",
        "narrateur|Le mince commence, puis recule.",
        "enfant-m|Ils ne viennent pas.",
        "maman|Le kiosque est trop loin de l'eau.",
        "papa|Tu les rassembles comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Dans la mare, l'un reste, l'autre part.",
            "papa|Tu fais quoi, Nino ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Sur le banc, les miettes tombent.",
            "maman|Tu fais quoi, avec eux ?",
        )
    return L(
        "narrateur|Au kiosque, ils ne montent pas.",
        "papa|Tu fais quoi, maintenant ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wall = {
            1: "Il pose le pain au bord, tout bas.",
            2: "Il pose la nappe au bord, tout bas.",
            3: "Il pose le seau au bord, tout bas.",
        }[t1]
        return L(
            "enfant-m|Le bord, pas l'eau.",
            f"narrateur|{wall}",
            "narrateur|Le canard rond s'approche, trop rond.",
            "narrateur|Le mince revient, trop mince.",
            "enfant-m|Vous avez chacun votre pain.",
            "papa|Deux places, deux formes.",
            f"narrateur|{o['use']}",
            "maman|Ils goûtent, quand même.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-m|Deux tas, pour eux.",
            "narrateur|Il casse le pain en deux tas.",
            "narrateur|Un tas près du rond, trop large.",
            "narrateur|Un tas près du mince, trop fin.",
            "enfant-m|Vous tenez, tous les deux.",
            "maman|Ils n'ont pas besoin d'être pareils.",
            f"narrateur|{o['use']}",
            "papa|La mare les tient, maintenant.",
        )
    if t2 == 1 and t3 == 3:
        cover = {
            1: "Il pose le pain sur le pont, tout bas.",
            2: "Il étale la nappe sur le pont, tout bas.",
            3: "Il pose le seau sur le pont, tout bas.",
        }[t1]
        return L(
            "enfant-m|Le pont, pour tous.",
            f"narrateur|{cover}",
            "narrateur|Le canard rond monte, trop large.",
            "narrateur|Le mince monte, trop léger.",
            "enfant-m|Un goûter, plus large.",
            "papa|L'eau reste en dessous, tout seule.",
            "maman|Ils se touchent, les deux.",
            f"narrateur|{o['use']}",
        )
    if t2 == 2 and t3 == 1:
        down = {
            1: "Il pose le pain dans l'herbe, tout bas.",
            2: "Il étale la nappe dans l'herbe, tout bas.",
            3: "Il pose le seau dans l'herbe, tout bas.",
        }[t1]
        return L(
            "enfant-m|L'herbe, comme une table.",
            f"narrateur|{down}",
            "narrateur|Nino s'assoit, les pieds dans l'herbe.",
            "narrateur|Le canard rond s'assoit, trop rond.",
            "narrateur|Le mince s'allonge contre lui, trop mince.",
            "enfant-m|Vous avez le sol, tous les deux.",
            "papa|Chacun a sa place.",
            f"narrateur|{o['use']}",
            "maman|Les miettes restent, plus calmes.",
        )
    if t2 == 2 and t3 == 2:
        foot = {
            1: "Il pose le pain au pied, tout bas.",
            2: "Il glisse la nappe au pied, tout bas.",
            3: "Il pose le seau au pied, tout bas.",
        }[t1]
        return L(
            "enfant-m|Le pied du banc.",
            f"narrateur|{foot}",
            "narrateur|Le canard rond reste, trop large.",
            "narrateur|Le mince reste, trop mince.",
            "enfant-m|Vous tenez, sans tomber.",
            "papa|Le pied était assez large.",
            "maman|Et lui, tout mince, reste près.",
            f"narrateur|{o['use']}",
        )
    if t2 == 2 and t3 == 3:
        spread = {
            1: "Il étale la nappe, le pain dessus.",
            2: "Il étale la nappe, trop large, trop douce.",
            3: "Il étale la nappe, le seau dessus.",
        }[t1]
        return L(
            "enfant-m|La nappe, sur les fentes.",
            f"narrateur|{spread}",
            "enfant-m|Vous avez le pain, tous les deux.",
            "papa|Plus besoin des trous.",
            "maman|Tes mains ont tenu le tissu.",
            f"narrateur|{o['wait']}",
        )
    if t2 == 3 and t3 == 1:
        step = {
            1: "Il pose le pain sur la marche, tout bas.",
            2: "Il pose la nappe sur la marche, tout bas.",
            3: "Il pose le seau sur la marche, tout bas.",
        }[t1]
        return L(
            "enfant-m|Les marches, pour tous.",
            f"narrateur|{step}",
            "narrateur|Le canard rond tient, trop large, trop rond.",
            "narrateur|Le mince tient, une patte dans le vide.",
            "enfant-m|Vous goûtez ici, sans tomber.",
            "papa|La marche a deux places, maintenant.",
            "maman|Plus besoin de monter.",
            f"narrateur|{o['wait']}",
        )
    if t2 == 3 and t3 == 2:
        near = {
            1: "Il porte le pain, tout près de l'eau.",
            2: "Il porte la nappe, tout près de l'eau.",
            3: "Il porte le seau, tout près de l'eau.",
        }[t1]
        return L(
            "enfant-m|Plus près, vers l'eau.",
            f"narrateur|{near}",
            "narrateur|Les deux canards avancent, tout lent.",
            "enfant-m|Vous avez le goûter, plus près.",
            "papa|Rentrer vers l'eau, c'était plus doux.",
            "maman|L'un près de l'autre.",
            f"narrateur|{o['use']}",
        )
    shade = {
        1: "Il pose le pain à l'ombre, tout bas.",
        2: "Il étale la nappe à l'ombre, tout bas.",
        3: "Il pose le seau à l'ombre, tout bas.",
    }[t1]
    return L(
        "enfant-m|Sous l'ombre, plus calme.",
        f"narrateur|{shade}",
        "narrateur|Le vent reste dehors, sur les marches.",
        "enfant-m|Vous avez la place, à l'abri.",
        "papa|L'ombre était plus douce.",
        "maman|L'herbe sent encore, plus loin.",
        f"narrateur|{o['wait']}",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Deux ronds d'eau restent au bord.",
            "enfant-m|Vous avez eu votre pain.",
            "narrateur|Le canard rond brille, encore tout rond.",
            "narrateur|Le mince brille, le cou encore mince.",
            "papa|Tes mains ont fait les deux places.",
            "maman|Ils sont ensemble, quand même.",
            f"narrateur|{coda}",
            "narrateur|La mare redevient plate, tout calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Les deux tas sentent encore le four.",
            "enfant-m|Vous teniez, tous les deux.",
            "narrateur|Nino souffle sur une miette, tout doux.",
            "papa|La mare les a tenus.",
            "maman|Bravo, ils ont mangé.",
            f"narrateur|{coda}",
            "enfant-m|On rentre, maintenant.",
            "narrateur|L'eau n'a plus qu'un pli, tout bas.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Sur le pont, l'eau tremble encore.",
            "enfant-m|Un goûter, plus large.",
            "narrateur|Il pose une miette, puis une autre.",
            "papa|L'eau n'a plus gagné.",
            "maman|Tes mains ont mis le pont.",
            f"narrateur|{coda}",
            "enfant-m|Encore une miette, pour rire.",
            "narrateur|Une feuille s'arrête sur le bois, puis plus.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Dans l'herbe, deux traces restent, trop différentes.",
            "enfant-m|On a goûté ici, sans tomber.",
            "narrateur|Le mince pointe encore le ciel, trop mince.",
            "papa|L'herbe avait deux places.",
            "maman|Plus besoin des fentes.",
            f"narrateur|{coda}",
            "enfant-m|On reste un peu.",
            "narrateur|L'herbe se recouche, tout lentement.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Au pied, ça sent encore l'herbe.",
            "enfant-m|Vous teniez, sans tomber.",
            "narrateur|Le mince a une miette sur le bec, trop mince.",
            "papa|Le pied était assez large.",
            "maman|Deux silhouettes, un même pain.",
            f"narrateur|{coda}",
            "enfant-m|Le dîner, après ?",
            "narrateur|Un rai de lumière reste sur le bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sur la nappe, une miette reste, tout petite.",
            "enfant-m|Vous avez eu le pain.",
            "narrateur|Il les regarde, l'un contre l'autre.",
            "papa|Plus besoin des trous.",
            "maman|Tes mains ont tenu le tissu.",
            f"narrateur|{coda}",
            "enfant-m|On est arrivés.",
            "narrateur|Le banc redevient vide, tout calme.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Sur la marche, deux miettes restent encore.",
            "enfant-m|Vous aviez les marches.",
            "narrateur|Nino lisse une miette, un dernier coup.",
            "papa|La marche avait deux places.",
            "maman|Plus besoin de monter.",
            f"narrateur|{coda}",
            "enfant-m|On reste un peu.",
            "narrateur|Les marches se taisent, tout lentement.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Plus près de l'eau, l'air est déjà doux.",
            "enfant-m|Vous aviez le goûter, plus près.",
            "narrateur|Le rond et le mince se touchent, encore.",
            "papa|Rentrer vers l'eau, c'était plus doux.",
            "maman|L'herbe sent encore, plus loin.",
            f"narrateur|{coda}",
            "enfant-m|Le goûter est fini, pour de vrai.",
            "narrateur|Une feuille s'arrête contre le pas.",
        )
    return L(
        "narrateur|Sous l'ombre, l'air est déjà plus doux.",
        "enfant-m|Vous aviez la place, à l'abri.",
        "narrateur|Un bec rond, un bec mince, tout près.",
        "papa|L'ombre était plus douce.",
        "maman|L'herbe sent encore, plus loin.",
        f"narrateur|{coda}",
        "enfant-m|On rentre, maintenant.",
        "narrateur|L'ombre du kiosque retombe, tout douce.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "enfants_parc"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Sous les tilleuls, le parc sent l'herbe.",
        "narrateur|Une mare brille, toute plate.",
        "narrateur|Des feuilles sèches font un bruit, tout sec.",
        "narrateur|Papa pose le sac, près du banc.",
        "narrateur|Maman tient le seau, encore vide.",
        "narrateur|Deux canards avancent, l'un derrière l'autre.",
        "narrateur|Le premier a le ventre tout rond.",
        "narrateur|Le second a le cou tout mince.",
        "papa|Tu les as vus, Nino ?",
        "enfant-m|Oui, les deux.",
        "enfant-m|Je veux leur donner à manger.",
        "papa|Les deux, Nino ?",
        "enfant-m|Les deux.",
        "narrateur|En ce moment, Nino touche le pain.",
        "narrateur|La croûte est un peu rêche, encore.",
        "enfant-m|Ils ne se ressemblent pas.",
        "papa|On donne aux deux.",
        "maman|Le pain, la nappe, et le seau.",
        "papa|Merci, tu as vu les deux.",
        "enfant-m|On prépare, d'abord.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du sac.",
        "narrateur|Le pain, la nappe, et le seau.",
        "maman|Tu commences par laquelle ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le pain", "la nappe", "le seau")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nino a pris {o['lab']} d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la mare", "le banc", "le kiosque")

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            sons[sp] = "enfants_parc"
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Parc, tilleuls, mare plate, feuilles sèches. Nino veut un vrai goûter "
        "pour le canard au ventre rond et le canard au cou mince. "
        "T1 = pain / nappe / seau (les trois partent). "
        "T2 = mare trop haute / banc trop fendu / kiosque trop loin. "
        "T3 = neuf résolutions (bord, deux tas, pont ; herbe, pied, nappe ; "
        "marches, plus près, ombre). La leçon se vit : les formes ne sont pas "
        "une blague, on donne aux deux. Fin : les deux canards goûtent.",
        "N1 ≤ 10. Hugo hors troupe → Nino, papa/maman. Slogan « Plus rond ou "
        "plus mince », « bon travail », calque AUT-001 jetés. Autre récit que "
        "DIF-015/025/035 (tente, défilé, bain). Un merci de papa (les deux vus). "
        "chunk_id inchangés. check() N1. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
