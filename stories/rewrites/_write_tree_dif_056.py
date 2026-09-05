#!/usr/bin/env python3
"""TREE-DIF-056 — La bulle de Nina, sur le nez de bronze (N2, DIF.BES.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-056"
N2 = 15
TITLE = "La bulle de Nina, sur le nez de bronze"
FIL = (
    "Au parc, Nina veut poser une bulle ronde sur le nez de bronze, "
    "avant la cloche. Elle prend d'abord le bâton, le savon ou la coupelle ; "
    "les trois viennent. L'allée soulève trop, le socle brûle trop, "
    "le tilleul claque trop. Neuf façons de laisser du temps. La bulle reste."
)
CHARS = "Nina, papa, maman"
SETTING = "parc du village : allée, statue de bronze, tilleul"


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
        "plus de temps ou de calme",
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
        "escargot",
        "balcon",
        "veau",
        "étable",
        "abreuvoir",
        "le four",
        "marché",
        "fort de coussins",
        "étoile",
        "moulinet",
        "carrousel",
        "marelle",
        "zoé",
        "zoe",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
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
        "lab": "le bâton",
        "ans": "bâton",
        "acc": "bâton | le bâton | d'abord le bâton | le bois",
        "retry": "Nina prend le bâton d'abord.",
        "coda": "Le bâton sèche près du savon, un fil encore collant.",
        "hip": "Entre ses doigts, le bois du bâton est tiède.",
        "wait": "Pendant ce temps, le bâton reste droit, sans bouger.",
        "use": "Un fil de savon cherche encore l'air.",
    },
    2: {
        "lab": "le savon",
        "ans": "savon",
        "acc": "savon | le savon | d'abord le savon | le flacon",
        "retry": "Nina prend le savon d'abord.",
        "coda": "Le flacon reste fermé, une goutte au bouchon.",
        "hip": "Dans sa paume, le flacon de savon est tiède.",
        "wait": "Fermé, le savon attend contre son pouce.",
        "use": "Une goutte de savon brille, prête à filer.",
    },
    3: {
        "lab": "la coupelle",
        "ans": "coupelle",
        "acc": "coupelle | la coupelle | d'abord la coupelle | le bol",
        "retry": "Nina prend la coupelle d'abord.",
        "coda": "La coupelle sèche près du gravier, un cercle de savon.",
        "hip": "Contre son ventre, la coupelle reste bien plate.",
        "wait": "Plate, la coupelle attend, sans verser.",
        "use": "Le rond de savon attend, tout calme.",
    },
}

T3_LABS = {
    1: ("attendre les pas", "plus bas", "le bord"),
    2: ("attendre l'ombre", "l'oiseau", "tout près"),
    3: ("attendre les feuilles", "derrière", "tout petit"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina attrape d'abord le bâton, encore mouillé.",
            "enfant-f|La bulle va s'y accrocher.",
            "maman|Garde le cercle en l'air.",
            "narrateur|Un film tremble au bout, puis tient.",
            "papa|Prends le savon, il est à tes pieds.",
            "narrateur|La coupelle glisse sous son autre bras.",
            "narrateur|Les trois partent, collés à Nina.",
            "enfant-f|Nez, j'arrive.",
            "narrateur|Le bois sent le sucre, un peu.",
            "papa|Le bâton est à toi, maintenant.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina dévisse d'abord le savon, tout lentement.",
            "enfant-f|Il va donner la bulle.",
            "papa|Une goutte, pas tout le flacon.",
            "narrateur|La goutte reste au pouce, puis tombe.",
            "maman|Le bâton t'attend, près du lacet.",
            "narrateur|Papa pose la coupelle contre le gravier chaud.",
            "narrateur|Nina serre les trois contre son ventre.",
            "enfant-f|Savon, tu restes avec moi.",
            "narrateur|Le flacon colle un peu sa manche.",
            "maman|Le savon est ouvert, tu peux y aller.",
        )
    return L(
        "narrateur|Nina lève d'abord la coupelle, bien à plat.",
        "enfant-f|Le savon va dormir dedans.",
        "maman|Pas trop d'eau, juste un miroir.",
        "narrateur|Le rond tremble, puis s'arrête.",
        "papa|Voici le bâton, et le savon.",
        "narrateur|Il les glisse contre son genou.",
        "narrateur|Le gravier reste vide, derrière eux.",
        "enfant-f|Coupelle, je te porte.",
        "narrateur|Un cercle de savon brille au fond.",
        "papa|La coupelle est prête, on avance.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|Le bâton reste contre elle, encore mouillé.",
            "enfant-f|On va jusqu'au bronze.",
            "maman|La cloche n'est pas loin.",
            "papa|Tu tiens bien, Nina ?",
            "enfant-f|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|Le savon pend au poignet, un peu lâche.",
            "enfant-f|Il va filer la bulle.",
            "papa|Ça sent encore le sucre, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Une goutte se tait, puis plus rien.",
        )
    return L(
        "narrateur|La coupelle reste plate, contre son ventre.",
        "enfant-f|Le savon ne verse pas.",
        "maman|Le rond sent encore le miel.",
        "papa|On avance, tous les trois ?",
        "enfant-f|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le bâton penche vers le bronze, déjà.",
        2: "Le savon colle encore à sa manche.",
        3: "La coupelle appuie contre son ventre.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Devant, l'allée soulève trop de poussière.",
        "narrateur|Le socle, lui, brûle encore au soleil.",
        "narrateur|Sous le tilleul, les feuilles claquent.",
        "papa|Nina, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le fil se casse, trop vite, trop fort.",
            2: "La goutte saute, trop sèche, trop vite.",
            3: "Le rond se plisse, trop agité, trop gris.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Le gravier de l'allée saute sous les pas.",
            f"narrateur|{extra}",
            "enfant-f|Ma bulle a crevé !",
            "narrateur|Encore un pas, encore de la poussière.",
            "narrateur|Le nez reste trop loin, trop gris.",
            "papa|Ici, ça n'arrête pas.",
            "maman|La bulle a besoin de calme.",
            "enfant-f|Alors on fait quoi ?",
            "papa|Tu vois comment, Nina ?",
        )
    if t2 == 2:
        extra = {
            1: "Le fil fond, trop chaud, trop mince.",
            2: "La goutte sèche, trop vite, trop chaude.",
            3: "Le rond tremble, trop chaud, trop mince.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Le bronze tient encore tout le soleil.",
            f"narrateur|{extra}",
            "enfant-f|Le nez brûle trop !",
            "narrateur|La bulle touche, puis crève tout de suite.",
            "narrateur|Il ne reste rien sur le bronze.",
            "papa|Ici, c'est trop chaud.",
            "maman|La bulle n'arrive pas.",
            "enfant-f|Alors on fait quoi ?",
            "maman|Tu vois comment, Nina ?",
        )
    extra = {
        1: "Le fil claque, trop léger dans l'air.",
        2: "La goutte s'envole, trop prise par le vent.",
        3: "Le rond se plie, trop poussé par les feuilles.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Le tilleul agite ses feuilles, trop vite.",
        f"narrateur|{extra}",
        "enfant-f|Le vent prend tout !",
        "narrateur|Une feuille claque, puis une autre.",
        "narrateur|La bulle part de travers, trop loin.",
        "papa|Ici, ça souffle trop.",
        "maman|Il lui faut du temps.",
        "enfant-f|Alors on fait quoi ?",
        "papa|Tu vois comment, Nina ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'allée n'a pas fini de soulever.",
            "papa|Attendre les pas, plus bas, ou le bord ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le bronze n'a pas fini de brûler.",
            "maman|Attendre l'ombre, l'oiseau, ou tout près ?",
        )
    return L(
        "narrateur|Les feuilles n'ont pas fini de claquer.",
        "papa|Attendre les feuilles, derrière, ou tout petit ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "Elle tient le bâton, sans souffler encore.",
            2: "Elle tient le savon, sans ouvrir encore.",
            3: "Elle tient la coupelle, sans verser encore.",
        }[t1]
        return L(
            "enfant-f|On attend les pas.",
            f"narrateur|{wait}",
            "narrateur|Le gravier se tait, une fois, puis plus.",
            "enfant-f|Tu peux partir, maintenant.",
            f"narrateur|{o['wait']}",
            "papa|Les pas se sont tus, maintenant.",
            "narrateur|La bulle part, ronde, tout calme.",
            "maman|Tu as attendu, et elle est partie.",
        )
    if t2 == 1 and t3 == 2:
        low = {
            1: "Elle baisse le bâton, loin de la poussière.",
            2: "Elle baisse le savon, loin de la poussière.",
            3: "Elle baisse la coupelle, loin de la poussière.",
        }[t1]
        return L(
            "enfant-f|Plus bas, d'abord.",
            f"narrateur|{low}",
            "narrateur|Nina s'accroupit, les genoux au gravier.",
            "narrateur|L'air est plus doux, près de l'herbe.",
            f"narrateur|{o['use']}",
            "papa|Tu as vu l'herbe, avant.",
            "enfant-f|Ici, tu ne crèves plus.",
            "maman|Près du sol, ça tenait mieux.",
        )
    if t2 == 1 and t3 == 3:
        edge = {
            1: "Elle glisse le bâton vers le bord d'herbe.",
            2: "Elle glisse le savon vers le bord d'herbe.",
            3: "Elle glisse la coupelle vers le bord d'herbe.",
        }[t1]
        return L(
            "enfant-f|Au bord, tout petit.",
            f"narrateur|{edge}",
            "narrateur|L'herbe tient, sans laisser la poussière.",
            "narrateur|Nina répète, tout bas, encore une fois.",
            f"narrateur|{o['wait']}",
            "papa|Le bord n'a pas soulevé.",
            "enfant-f|Tu es à l'abri.",
            "maman|Tu as dit ça tout bas.",
        )
    if t2 == 2 and t3 == 1:
        shade = {
            1: "Sous l'ombre, le bâton ne fond plus.",
            2: "Sous l'ombre, le savon ne sèche plus.",
            3: "Sous l'ombre, la coupelle ne fume plus.",
        }[t1]
        return L(
            "enfant-f|On attend l'ombre.",
            "narrateur|Une ombre de tilleul glisse sur le nez.",
            f"narrateur|{shade}",
            "narrateur|Le bronze se tait, puis se refroidit.",
            f"narrateur|{o['wait']}",
            "maman|Le nez est redevenu doux.",
            "enfant-f|Maintenant, tu me vois.",
            "papa|Tu as laissé l'ombre arriver.",
        )
    if t2 == 2 and t3 == 2:
        bird = {
            1: "Elle pose d'abord le fil sur l'oiseau.",
            2: "Elle pose d'abord la goutte sur l'oiseau.",
            3: "Elle pose d'abord le rond sur l'oiseau.",
        }[t1]
        return L(
            "enfant-f|L'oiseau, d'abord, il est plus frais.",
            f"narrateur|{bird}",
            "narrateur|L'oiseau de bronze est à l'ombre, déjà.",
            "narrateur|Le nez reçoit ensuite un rond tout calme.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas soufflé trop fort.",
            "enfant-f|C'est pour toi.",
            "maman|L'oiseau était plus frais, tu as vu.",
        )
    if t2 == 2 and t3 == 3:
        close = {
            1: "Tout près, le bâton n'a plus d'air chaud.",
            2: "Tout près, le savon n'a plus d'air chaud.",
            3: "Tout près, la coupelle n'a plus d'air chaud.",
        }[t1]
        return L(
            "enfant-f|Tout près, contre le bronze.",
            "narrateur|Nina se glisse contre le socle, tout doux.",
            f"narrateur|{close}",
            "narrateur|La bulle n'a plus à voyager trop loin.",
            f"narrateur|{o['wait']}",
            "papa|Tu t'es mise tout près, contre le nez.",
            "enfant-f|Le nez est là.",
            "maman|Tu t'es mise tout contre.",
        )
    if t2 == 3 and t3 == 1:
        leaves = {
            1: "Elle tient le bâton, puis attend les feuilles.",
            2: "Elle tient le savon, puis attend les feuilles.",
            3: "Elle tient la coupelle, puis attend les feuilles.",
        }[t1]
        return L(
            "enfant-f|On attend les feuilles, d'abord.",
            f"narrateur|{leaves}",
            "narrateur|Les feuilles vont, reviennent, puis se taisent.",
            "narrateur|L'air redevient un seul souffle, net.",
            f"narrateur|{o['wait']}",
            "papa|Le tilleul n'a plus claqué.",
            "enfant-f|Maintenant, tu peux rester.",
            "maman|Tu as laissé les feuilles finir.",
        )
    if t2 == 3 and t3 == 2:
        behind = {
            1: "Derrière le tronc, le bâton ne claque plus.",
            2: "Derrière le tronc, le savon ne s'envole plus.",
            3: "Derrière le tronc, la coupelle ne se plie plus.",
        }[t1]
        return L(
            "enfant-f|Derrière, pas trop près du vent.",
            f"narrateur|{behind}",
            "narrateur|Nina se glisse derrière le tronc, tout bas.",
            "narrateur|Rien ne claque, rien ne pousse plus.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas couru.",
            "enfant-f|Tu es ronde, maintenant.",
            "maman|Derrière, l'air était plus doux.",
        )
    tiny = {
        1: "Une toute petite bulle quitte le bâton.",
        2: "Une toute petite bulle quitte le savon.",
        3: "Une toute petite bulle quitte la coupelle.",
    }[t1]
    return L(
        "enfant-f|Tout petit, tout serré.",
        f"narrateur|{tiny}",
        "narrateur|Nina souffle à peine, sans prendre le vent.",
        "narrateur|Le tilleul se tait, plus loin, tout seul.",
        f"narrateur|{o['use']}",
        "papa|Le petit rond n'a pas volé.",
        "enfant-f|Tu restes, bulle.",
        "maman|Le petit rond a suffi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La bulle se pose, ronde, sur le nez de bronze.",
            "enfant-f|On a attendu les pas.",
            "papa|Merci d'avoir laissé le gravier se taire.",
            "maman|La cloche n'a pas encore sonné.",
            f"narrateur|{coda}",
            "narrateur|Un grain de poussière retombe, puis plus rien.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Plus bas, la bulle monte jusqu'au nez.",
            "enfant-f|On s'est baissées, d'abord.",
            "papa|Tu as vu l'herbe avant de souffler.",
            "maman|Essuie tes genoux, on rentre.",
            f"narrateur|{coda}",
            "narrateur|Un rond d'ombre reste au bas du bronze.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Du bord d'herbe, la bulle rejoint le nez.",
            "enfant-f|Je suis restée sur l'herbe.",
            "papa|Le bord n'a pas soulevé.",
            "maman|L'herbe est retombée, plus loin.",
            f"narrateur|{coda}",
            "narrateur|L'allée se tait, derrière le bronze tiède.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Quand l'ombre a touché, la bulle a tenu.",
            "enfant-f|On a attendu le tilleul.",
            "papa|L'ombre vous a aidées.",
            "maman|Le bronze sent encore le soleil, moins fort.",
            f"narrateur|{coda}",
            "narrateur|L'ombre reste un moment, puis glisse.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|De l'oiseau au nez, la bulle a glissé.",
            "enfant-f|On a commencé par l'oiseau.",
            "papa|Tu n'as pas soufflé trop fort.",
            "maman|L'oiseau était plus frais, d'abord.",
            f"narrateur|{coda}",
            "narrateur|Un rond net reste sur le nez, puis pâlit.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Tout près, la bulle touche le nez, déjà.",
            "enfant-f|Je me suis mise tout près.",
            "papa|Tu t'es glissée, comme l'ombre.",
            "maman|Vos mains sentent encore le savon.",
            f"narrateur|{coda}",
            "narrateur|Le socle reste derrière, sans brûler.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Quand les feuilles se sont tues, la bulle a tenu.",
            "enfant-f|On a attendu le tilleul.",
            "papa|Le tilleul n'a plus claqué.",
            "maman|Vos manches sentent encore le miel.",
            f"narrateur|{coda}",
            "narrateur|Une feuille sèche sur le bronze, puis plus.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Derrière le tronc, la bulle rejoint le nez.",
            "enfant-f|On n'est pas allées trop au vent.",
            "papa|Tu n'as pas couru.",
            "maman|Tes doigts sentent encore le savon.",
            f"narrateur|{coda}",
            "narrateur|Le tronc reste à sa place, plus loin.",
        )
    return L(
        "narrateur|Tout petit, le rond tient sur le nez, tout calme.",
        "enfant-f|On a soufflé à peine.",
        "papa|Le petit rond n'a pas volé.",
        "maman|Le savon est déjà sec, on rentre.",
        f"narrateur|{coda}",
        "narrateur|Le tilleul se tait, plus loin, tout seul.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "enfants_parc"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Sous les tilleuls, le parc retient encore la chaleur.",
        "narrateur|Un pétale jaune se colle au lacet de Nina.",
        "narrateur|Ça sent le miel chaud, et le gravier.",
        "papa|Tu as vu le petit bronze, Nina ?",
        "enfant-f|Il tient un oiseau, tout près du nez.",
        "maman|Le nez est lisse, encore chaud.",
        "narrateur|En ce moment, Nina souffle dans ses mains, vides.",
        "enfant-f|Je veux une bulle, collée là.",
        "papa|La cloche va fermer le parc.",
        "maman|On emporte le savon, alors ?",
        "papa|Merci, tu as essuyé le bâton.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près du lacet, trois affaires attendent.",
        "narrateur|Un bâton, un savon, une coupelle.",
        "maman|Par quoi tu commences, Nina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bâton", "le savon", "la coupelle")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nina a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'allée", "le socle", "le tilleul")

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
        "Parc du village, gravier chaud, pétale de tilleul, bronze. "
        "Nina veut poser une bulle ronde sur le nez de la statue, avant la cloche. "
        "T1 = bâton / savon / coupelle (les trois viennent). "
        "T2 = allée trop poussiéreuse / socle trop chaud / tilleul trop venteux. "
        "T3 = neuf résolutions (pas, plus bas, bord ; ombre, oiseau, tout près ; "
        "feuilles, derrière, tout petit). La leçon se vit : elle attend, "
        "elle observe, elle répète tout bas. Fin : la bulle reste sur le nez.",
        "N2 ≤ 15. Slogan « Plus de temps ou de calme », Zoé, Tom/Léa/Sami, "
        "bac/toboggan/balançoires, « bon travail », calque AUT-001 jetés. "
        "Récit autre que DIF-020 (escargot/balcon), DIF-030 (pain/four), "
        "DIF-040 (veau/ferme), DIF-048 (étoile/fenêtre). "
        "Répliques 048 (avancer avec elle, tape sa paume, tu trouves) réécrites. "
        "Merci de papa (bâton essuyé). chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-056.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
