#!/usr/bin/env python3
"""TREE-DIF-066 — La petite valise d'Amir, dans le grenier (N2, DIF.COR.001)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-066"
N2 = 15
TITLE = "La petite valise d'Amir, dans le grenier"
FIL = (
    "Au grenier, Amir veut descendre la petite valise à pois, "
    "pour le pique-nique, pas la grande trop lourde. "
    "Il prend d'abord la valise à pois, la valise en carton ou la cordelette ; "
    "les trois viennent. Sous la lucarne c'est trop bas, entre les caisses "
    "c'est trop large, près de l'escalier la marche est trop haute. "
    "Neuf façons de choisir la bonne taille, porter à deux, glisser, attendre. "
    "La petite valise descend. On sent le pain, dans la cuisine."
)
CHARS = "Amir, papa, maman"
SETTING = "grenier de la maison du village : lucarne, caisses, escalier, malle"


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
        "plus petit ou plus grand",
        "tailles différentes",
        "jouer ensemble",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "kenzo",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
        "nina",
        "adam",
        "la mer",
        "plage",
        "vague",
        "cacao",
        "cerf-volant",
        "cerf volant",
        "soleil en papier",
        "le four",
        "pomme",
        "rails",
        "wagon",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if re.search(r"\bmer\b", whole):
        raise SystemExit(f"{SID} slogan/calque: mer")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
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
        "lab": "la valise à pois",
        "ans": "pois",
        "acc": "pois | valise à pois | la valise à pois | petite valise | la petite",
        "retry": "Amir a pris la valise à pois.",
        "coda": "Les pois gardent un grain de poussière.",
        "hip": "Les pois frottent sa paume, tout doux.",
        "wait": "La petite valise attend, sans bouger.",
        "use": "Les pois brillent encore, un peu poussiéreux.",
    },
    2: {
        "lab": "la valise en carton",
        "ans": "carton",
        "acc": "carton | valise en carton | la valise en carton | grande valise | la grande",
        "retry": "Amir a pris la valise en carton.",
        "coda": "Le carton reste au grenier, trop lourd.",
        "hip": "Le carton râpe ses doigts, trop lourd.",
        "wait": "La grande reste, trop large, trop lourde.",
        "use": "Le carton reste trop grand, trop loin.",
    },
    3: {
        "lab": "la cordelette",
        "ans": "cordelette",
        "acc": "cordelette | la cordelette | corde | la corde | le fil",
        "retry": "Amir a pris la cordelette.",
        "coda": "La cordelette reste nouée, tout bas.",
        "hip": "La cordelette pique un peu, contre le poignet.",
        "wait": "La cordelette pend, toute calme.",
        "use": "La cordelette tire tout doux, sans casser.",
    },
}

T3_LABS = {
    1: ("la petite valise", "le plancher", "la cordelette"),
    2: ("le passage", "les poignées", "la poussière"),
    3: ("la rampe", "le palier", "la petite valise"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir attrape d'abord la valise à pois.",
            "enfant-m|Elle est légère, celle-là.",
            "maman|Les pois sont un peu poussiéreux.",
            "narrateur|Un grain tombe, tout fin, dans le rai.",
            "papa|Prends la cordelette, elle est là.",
            "narrateur|Maman glisse aussi la valise en carton.",
            "narrateur|Les trois partent, collés à Amir.",
            "enfant-m|Petite valise, tu viens.",
            "narrateur|Les pois sentent le bois chaud, un peu.",
            "papa|La petite est à toi, maintenant.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir tire d'abord la valise en carton.",
            "enfant-m|Elle est trop lourde, déjà.",
            "papa|Le carton râpe, tout sec.",
            "narrateur|La grande avance d'un pas, puis s'arrête.",
            "maman|La petite t'attend, près de la malle.",
            "narrateur|Papa noue la cordelette au poignet.",
            "narrateur|Amir serre les trois contre son ventre.",
            "enfant-m|Carton, tu restes avec moi.",
            "narrateur|Le carton colle un peu sa manche.",
            "maman|La grande est partie, on avance.",
        )
    return L(
        "narrateur|Amir lève d'abord la cordelette, toute fine.",
        "enfant-m|Elle va tirer la valise.",
        "maman|Pas trop fort, juste un fil.",
        "narrateur|Le fil pique, puis se tait.",
        "papa|Voici la petite, et la grande.",
        "narrateur|Il les glisse contre son genou.",
        "narrateur|La malle reste ouverte, derrière eux.",
        "enfant-m|Cordelette, je te porte.",
        "narrateur|Un nœud simple brille au poignet.",
        "papa|La cordelette est prête, on avance.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|La valise à pois reste contre lui, légère.",
            "enfant-m|On va jusqu'à la trappe.",
            "maman|Le pique-nique n'est pas loin.",
            "papa|Tu tiens bien, Amir ?",
            "enfant-m|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|La valise en carton pèse au poignet, trop.",
            "enfant-m|Elle va descendre, peut-être.",
            "papa|Ça sent encore le bois, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le carton se tait, puis plus rien.",
        )
    return L(
        "narrateur|La cordelette reste nouée, contre son poignet.",
        "enfant-m|Elle ne lâche pas.",
        "maman|Le fil sent encore le tiroir.",
        "papa|On avance, tous les trois ?",
        "enfant-m|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "La valise à pois penche vers la trappe, déjà.",
        2: "La valise en carton colle encore à sa manche.",
        3: "La cordelette appuie contre son poignet.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Devant, la lucarne est trop basse, trop petite.",
        "narrateur|Au milieu, les caisses laissent un trou trop étroit.",
        "narrateur|Près de l'escalier, la marche est trop haute.",
        "papa|Amir, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Les pois passent, mais le carton bute.",
            2: "Le carton bute, trop large, trop haut.",
            3: "La cordelette tire, mais le carton reste.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Sous la lucarne, le toit est trop bas.",
            f"narrateur|{extra}",
            "enfant-m|Elle ne passe pas !",
            "narrateur|Le bois touche, trop serré, trop bas.",
            "narrateur|La grande reste coincée, trop large.",
            "papa|Ici, c'est trop petit.",
            "maman|Regarde les deux, Amir.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois comment, Amir ?",
        )
    if t2 == 2:
        extra = {
            1: "Les pois glissent, mais le carton se coince.",
            2: "Le carton se coince, trop large, trop sec.",
            3: "La cordelette passe, mais le carton reste.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Entre les caisses, le trou est trop étroit.",
            f"narrateur|{extra}",
            "enfant-m|Elle est trop large !",
            "narrateur|Une caisse racle, puis une autre.",
            "narrateur|La grande n'avance plus, trop sèche.",
            "papa|Ici, ça ne passe pas.",
            "maman|Le carton est trop grand pour le trou.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois comment, Amir ?",
        )
    extra = {
        1: "Les pois sont légers, mais le carton pèse trop.",
        2: "Le carton pèse, trop lourd, trop haut.",
        3: "La cordelette tire, mais le carton ne monte pas.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Près de l'escalier, la marche est trop haute.",
        f"narrateur|{extra}",
        "enfant-m|Elle est trop lourde !",
        "narrateur|Un pied cherche, trop bas, trop court.",
        "narrateur|La grande ne descend pas, trop haute.",
        "papa|Ici, c'est trop haut.",
        "maman|La grande pèse trop, pour la marche.",
        "enfant-m|Alors on fait quoi ?",
        "papa|Tu vois comment, Amir ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La lucarne n'a pas fini d'être trop basse.",
            "papa|La petite valise, le plancher, ou la cordelette ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les caisses n'ont pas fini d'être trop étroites.",
            "maman|Le passage, les poignées, ou la poussière ?",
        )
    return L(
        "narrateur|La marche n'a pas fini d'être trop haute.",
        "papa|La rampe, le palier, ou la petite valise ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        choose = {
            1: "Il garde la petite, et pose la grande.",
            2: "Il pose la grande, trop large, trop lourde.",
            3: "Il noue le fil, puis pose la grande.",
        }[t1]
        return L(
            "enfant-m|La petite valise, elle passe.",
            f"narrateur|{choose}",
            "narrateur|Sous la lucarne, les pois glissent, tout bas.",
            "enfant-m|Toi, tu rentres.",
            f"narrateur|{o['wait']}",
            "papa|La petite passait sous le toit.",
            "enfant-m|Celle-ci passe, l'autre non.",
            "maman|La petite allait sous le bois.",
        )
    if t2 == 1 and t3 == 2:
        low = {
            1: "Il couche la petite valise, à plat.",
            2: "Il laisse le carton debout, trop haut.",
            3: "Il glisse le fil le long du plancher.",
        }[t1]
        return L(
            "enfant-m|Sur le plancher, tout bas.",
            f"narrateur|{low}",
            "narrateur|Amir pousse la petite sous la poutre.",
            "narrateur|Le carton reste debout, trop haut.",
            f"narrateur|{o['use']}",
            "papa|Tu as glissé, sans la lever.",
            "enfant-m|Ici, tu ne butes plus.",
            "maman|Au sol, ça passait mieux.",
        )
    if t2 == 1 and t3 == 3:
        cord = {
            1: "Il noue le fil à la petite valise.",
            2: "Il noue le fil, pas au carton trop large.",
            3: "Il serre le nœud sur la petite valise.",
        }[t1]
        return L(
            "enfant-m|La cordelette, tout petit.",
            f"narrateur|{cord}",
            "narrateur|Le carton reste, trop large pour le rai.",
            "narrateur|Amir tire, tout bas, encore une fois.",
            f"narrateur|{o['wait']}",
            "papa|Le fil a tiré la petite.",
            "enfant-m|Tu es de l'autre côté.",
            "maman|Tu as tiré tout doux.",
        )
    if t2 == 2 and t3 == 1:
        gap = {
            1: "Il mesure le trou, puis la petite valise.",
            2: "Il compare le carton, trop large, au trou.",
            3: "Il passe le fil, puis la petite valise.",
        }[t1]
        return L(
            "enfant-m|Le passage, d'abord.",
            f"narrateur|{gap}",
            "narrateur|Le carton est trop large, trop sec.",
            "narrateur|Les pois passent entre les caisses, juste.",
            f"narrateur|{o['wait']}",
            "maman|Le trou était de sa taille.",
            "enfant-m|Maintenant, tu me suis.",
            "papa|Le trou était juste, pour elle.",
        )
    if t2 == 2 and t3 == 2:
        two = {
            1: "Papa prend une poignée, Amir l'autre.",
            2: "Ils laissent le carton, trop large, trop lourd.",
            3: "Le fil relie les deux poignées, tout doux.",
        }[t1]
        return L(
            "enfant-m|Les poignées, à deux.",
            f"narrateur|{two}",
            "narrateur|Ils lèvent la petite, pas la grande.",
            "narrateur|Le carton reste entre les caisses, trop large.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas tiré tout seul.",
            "enfant-m|C'est pour le pique-nique.",
            "maman|À deux, la petite avançait.",
        )
    if t2 == 2 and t3 == 3:
        dust = {
            1: "Amir s'arrête, les pois encore gris.",
            2: "Amir s'arrête, le carton encore gris.",
            3: "Amir s'arrête, le fil encore gris.",
        }[t1]
        return L(
            "enfant-m|La poussière, d'abord.",
            f"narrateur|{dust}",
            "narrateur|La poussière retombe, une fois, puis plus.",
            "narrateur|Il voit le trou, et la petite valise.",
            f"narrateur|{o['wait']}",
            "papa|Le rai est redevenu net.",
            "enfant-m|Je vois, maintenant.",
            "maman|Le trou était de sa taille.",
        )
    if t2 == 3 and t3 == 1:
        rail = {
            1: "Il pose la petite valise contre la rampe.",
            2: "Il pose le carton, trop lourd, trop haut.",
            3: "Il glisse le fil le long de la rampe.",
        }[t1]
        return L(
            "enfant-m|La rampe, d'abord.",
            f"narrateur|{rail}",
            "narrateur|Le carton reste en haut, trop lourd.",
            "narrateur|La petite glisse, marche après marche.",
            f"narrateur|{o['wait']}",
            "papa|La rampe a tenu la petite.",
            "enfant-m|Maintenant, tu peux rester.",
            "maman|Tu as glissé, sans la jeter.",
        )
    if t2 == 3 and t3 == 2:
        land = {
            1: "Ils posent la petite sur le palier, un moment.",
            2: "Ils posent le carton, trop lourd, un moment.",
            3: "Ils posent le fil sur le palier, un moment.",
        }[t1]
        return L(
            "enfant-m|Le palier, on s'arrête.",
            f"narrateur|{land}",
            "narrateur|Papa se met plus bas, une marche.",
            "narrateur|Amir tend la petite, pas la grande.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas sauté la marche.",
            "enfant-m|Tu es en bas, maintenant.",
            "maman|Le palier vous a aidés.",
        )
    tiny = {
        1: "Il descend la petite, une marche, puis l'autre.",
        2: "Il laisse le carton, trop lourd pour la marche.",
        3: "Il descend le fil, puis la petite valise.",
    }[t1]
    return L(
        "enfant-m|La petite valise, elle est légère.",
        f"narrateur|{tiny}",
        "narrateur|La grande reste au grenier, trop haute.",
        "narrateur|Amir tient la petite, marche après marche.",
        f"narrateur|{o['use']}",
        "papa|La petite tenait dans tes mains.",
        "enfant-m|Tu restes avec moi.",
        "maman|La petite a suffi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La petite valise descend, sous la lucarne.",
            "enfant-m|On a pris celle qui passe.",
            "papa|La petite passait sous le toit.",
            "maman|On sent le pain, déjà, dans la cuisine.",
            f"narrateur|{coda}",
            "narrateur|Un grain de poussière retombe, puis plus rien.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sur le plancher, la petite valise rejoint la trappe.",
            "enfant-m|On a glissé, d'abord.",
            "papa|Tu as poussé, sans la lever.",
            "maman|Le pain sent déjà, en bas.",
            f"narrateur|{coda}",
            "narrateur|Un rai d'ombre reste au bas de la lucarne.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Au bout du fil, la petite valise a passé.",
            "enfant-m|J'ai tiré tout doux.",
            "papa|Le fil a tenu.",
            "maman|La cuisine sent déjà le pain.",
            f"narrateur|{coda}",
            "narrateur|La lucarne se tait, derrière le bois tiède.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Dans le passage, la petite valise a tenu.",
            "enfant-m|On a regardé le trou.",
            "papa|Le trou était juste, pour elle.",
            "maman|Le pain chauffe encore, en bas.",
            f"narrateur|{coda}",
            "narrateur|Une caisse reste à sa place, plus loin.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|À deux, la petite valise a quitté les caisses.",
            "enfant-m|On a porté les poignées.",
            "papa|Tu n'as pas tiré tout seul.",
            "maman|On sent le pain, dans la cuisine.",
            f"narrateur|{coda}",
            "narrateur|Un pois de poussière reste sur une caisse.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Quand la poussière s'est tue, la petite a passé.",
            "enfant-m|J'ai vu le trou, après.",
            "papa|Le rai est redevenu net.",
            "maman|Le pain attend, tout chaud.",
            f"narrateur|{coda}",
            "narrateur|Les caisses restent derrière, sans bouger.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le long de la rampe, la petite valise est en bas.",
            "enfant-m|On a glissé, marche après marche.",
            "papa|La rampe a tenu.",
            "maman|Le pain sent déjà, dans la cuisine.",
            f"narrateur|{coda}",
            "narrateur|Une marche sèche, puis plus.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Du palier, la petite valise a rejoint le bas.",
            "enfant-m|On s'est arrêtés, d'abord.",
            "papa|Tu n'as pas sauté la marche.",
            "maman|On sent le pain, tout près.",
            f"narrateur|{coda}",
            "narrateur|Le palier reste à sa place, plus haut.",
        )
    return L(
        "narrateur|Tout légère, la petite valise est en bas, tout calme.",
        "enfant-m|On a pris celle qu'on porte.",
        "papa|La petite tenait dans tes mains.",
        "maman|Le pain est déjà chaud, on descend.",
        f"narrateur|{coda}",
        "narrateur|L'escalier se tait, plus loin, tout seul.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La trappe du grenier reste ouverte, toute chaude.",
        "narrateur|Un rai de soleil tient la poussière, toute fine.",
        "narrateur|Ça sent le bois chaud, et la malle.",
        "papa|La malle grince, tu as entendu ?",
        "enfant-m|Elle a bougé toute seule.",
        "maman|C'est le bois, il travaille.",
        "narrateur|En ce moment, Amir touche deux valises, l'une contre l'autre.",
        "enfant-m|Je veux la petite, pour le pique-nique.",
        "papa|La grande est trop lourde, toi.",
        "maman|Le panier attend, déjà, en bas.",
        "papa|Merci, tu as tenu la trappe.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près de la malle, trois affaires attendent.",
        "narrateur|La valise à pois, la valise en carton, la cordelette.",
        "maman|Tu prends quoi d'abord, Amir ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la valise à pois", "la valise en carton", "la cordelette")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Amir a pris {o['lab']} d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la lucarne", "les caisses", "l'escalier")

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
        "Grenier de la maison du village, rai de soleil, poussière, malle qui grince, "
        "bois chaud. Amir veut descendre la petite valise à pois pour le pique-nique, "
        "pas la grande trop lourde. "
        "T1 = valise à pois / valise en carton / cordelette (les trois viennent). "
        "T2 = lucarne trop basse / caisses trop étroites / marche trop haute. "
        "T3 = neuf résolutions (petite valise, plancher, cordelette ; passage, "
        "poignées, poussière ; rampe, palier, petite valise). La leçon se vit : "
        "il compare les deux tailles pour un geste. Fin : la petite descend, "
        "on sent le pain dans la cuisine.",
        "N2 ≤ 15. Slogan « Plus petit ou plus grand — au bord de la mer », Adam, "
        "Tom/Léa/Sami, bac/toboggan/balançoires, mer, « bon travail » jetés. "
        "Récit autre que DIF-009 (train), DIF-012 (pomme), DIF-013/041/052 (mer), "
        "DIF-030/041 (pain comme objet), DIF-034 (soleil papier), DIF-042 (cacao). "
        "Pain seulement en odeur de cuisine, à la fin. Amir seul + papa/maman. "
        "Merci de papa (trappe tenue). chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-066.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
