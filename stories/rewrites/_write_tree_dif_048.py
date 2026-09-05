#!/usr/bin/env python3
"""TREE-DIF-048 — L'étoile de papier de Mila, à la fenêtre (N3, DIF.BES.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-048"
N3 = 16
TITLE = "L'étoile de papier de Mila, à la fenêtre"
FIL = (
    "Le soir descend. Mila veut coller son étoile jaune dans le dernier soleil "
    "de la fenêtre, pour qu'elle brille avant la nuit. Elle prépare d'abord "
    "l'étoile, le ruban ou la pince ; les trois viennent. La vitre ouverte "
    "emporte trop, le rideau cache trop, le rebord trop plein fait tout tomber. "
    "Neuf façons de laisser du temps. L'étoile reste, jaune."
)
CHARS = "Mila, papa, maman"
SETTING = "près de la fenêtre, cuisine au soleil bas"


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
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
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
        "lab": "l'étoile",
        "ans": "étoile",
        "acc": "étoile | l'étoile | d'abord l'étoile | le papier",
        "retry": "Mila prend l'étoile d'abord.",
        "coda": "L'étoile sèche près du savon, un pli au coin.",
        "hip": "Entre ses doigts, le papier jaune craque un peu.",
        "wait": "Pendant ce temps, l'étoile reste plate, sage.",
        "use": "Un coin du papier cherche encore le soleil.",
    },
    2: {
        "lab": "le ruban",
        "ans": "ruban",
        "acc": "ruban | le ruban | d'abord le ruban | le collant",
        "retry": "Mila prend le ruban d'abord.",
        "coda": "Le ruban reste enroulé, un bout encore collant.",
        "hip": "Au poignet, le ruban colle un peu, tout doux.",
        "wait": "Enroulé, le ruban attend contre sa manche.",
        "use": "Un bout du ruban brille, prêt à tenir.",
    },
    3: {
        "lab": "la pince",
        "ans": "pince",
        "acc": "pince | la pince | d'abord la pince | le bois",
        "retry": "Mila prend la pince d'abord.",
        "coda": "La pince garde un fil jaune, près du rebord.",
        "hip": "Dans sa paume, le bois de la pince est tiède.",
        "wait": "Fermée, la pince reste contre son pouce.",
        "use": "Les deux branches de la pince attendent le bois.",
    },
}

T3_LABS = {
    1: ("attendre le vent", "plus bas", "la fente"),
    2: ("écarter", "attendre", "devant"),
    3: ("de la place", "au milieu", "contre le bois"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila prend d'abord l'étoile, encore chaude de soleil.",
            "enfant-f|Elle va briller à la vitre.",
            "maman|Tiens-la à plat, tout doux.",
            "narrateur|Un coin du papier se relève, puis retombe.",
            "papa|Le ruban aussi, près de toi.",
            "narrateur|Maman glisse la pince contre l'étoile.",
            "narrateur|Étoile, ruban et pince avancent avec elle.",
            "enfant-f|J'arrive, petit soleil.",
            "narrateur|Le papier sent l'orange et la colle.",
            "papa|L'étoile d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila prend d'abord le ruban, encore collant.",
            "enfant-f|Il va tenir l'étoile.",
            "papa|Déroule un peu, pas trop vite.",
            "narrateur|Un bout se colle à son pouce, puis lâche.",
            "maman|L'étoile, ensuite, près de toi.",
            "narrateur|Papa pose la pince contre le rebord.",
            "narrateur|Elle emporte les trois, contre elle.",
            "enfant-f|Tu vas la garder, ruban.",
            "narrateur|Le collant frotte sa manche, un peu.",
            "maman|Le ruban d'abord, il est prêt.",
        )
    return L(
        "narrateur|Mila prend d'abord la pince, le bois tiède.",
        "enfant-f|Elle va pincer le cadre.",
        "maman|Ouvre-la, tout doux.",
        "narrateur|Les deux branches claquent, puis se taisent.",
        "papa|L'étoile et le ruban, avec vous.",
        "narrateur|Il les pose près de l'évier.",
        "narrateur|Rien ne reste près de la table.",
        "enfant-f|Je te mets au bois.",
        "narrateur|Un fil jaune reste coincé dedans.",
        "papa|La pince d'abord, elle est prête.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|L'étoile tient contre sa poitrine, encore chaude.",
            "enfant-f|Elle va à la vitre.",
            "maman|Le soleil n'attendra pas longtemps.",
            "papa|On y va, Mila ?",
            "enfant-f|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|Le ruban fait un bracelet lâche, au poignet.",
            "enfant-f|Il va coller l'étoile.",
            "papa|Le collant sent encore le papier.",
            "maman|Vos mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un bout se décolle, puis se tait.",
        )
    return L(
        "narrateur|La pince reste fermée, contre son pouce.",
        "enfant-f|Elle va tenir le cadre.",
        "maman|Le bois sent encore le soleil.",
        "papa|On y va, tous les trois ?",
        "enfant-f|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "L'étoile tape sa poitrine, tout bas.",
        2: "Le ruban frotte sa manche, un peu collant.",
        3: "La pince tape le pouce, tout doux.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|La vitre ouverte souffle déjà, trop fort.",
        "narrateur|Plus loin, le rideau claque encore.",
        "narrateur|Sur le rebord, trop d'objets se touchent.",
        "papa|Mila, vous partez où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le papier se plie, trop vite, trop fort.",
            2: "Le ruban claque comme un fil, trop vif.",
            3: "La pince glisse, trop légère dans l'air.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|La vitre ouverte sent la rue, trop vive.",
            f"narrateur|{extra}",
            "enfant-f|Mon étoile s'envole !",
            "narrateur|Un souffle pousse le carreau, encore.",
            "narrateur|Le soleil saute, puis revient, trop vite.",
            "papa|Ça souffle trop, ici.",
            "maman|Elle a besoin de calme.",
            "enfant-f|On fait comment, alors ?",
            "papa|Tu trouves, Mila ?",
        )
    if t2 == 2:
        extra = {
            1: "Le papier disparaît un instant, trop caché.",
            2: "Le ruban s'accroche au tissu, trop serré.",
            3: "La pince tire le rideau, trop fort.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Le rideau sent la poussière, encore chaude.",
            f"narrateur|{extra}",
            "enfant-f|Le soleil est parti !",
            "narrateur|Le tissu va, puis revient, trop agité.",
            "narrateur|L'étoile n'a plus de lumière, trop sombre.",
            "papa|Le rideau n'a pas fini.",
            "maman|Elle n'avance plus.",
            "enfant-f|On fait comment, alors ?",
            "maman|Tu trouves, Mila ?",
        )
    extra = {
        1: "L'étoile glisse entre une cuillère et le savon.",
        2: "Le ruban colle une miette, trop sale.",
        3: "La pince n'a plus de bois libre, trop plein.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Le rebord est trop plein, trop étroit.",
        f"narrateur|{extra}",
        "enfant-f|Ça tombe tout le temps.",
        "narrateur|Une cuillère tinte, trop bruyante.",
        "narrateur|Le soleil se casse en petits bouts.",
        "papa|Ça tape trop, ici.",
        "maman|Elle a besoin de temps.",
        "enfant-f|On fait comment, alors ?",
        "papa|Tu trouves, Mila ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La vitre souffle encore, trop vive.",
            "papa|Attendre le vent, plus bas, ou la fente ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le rideau claque encore, trop fort.",
            "maman|Écarter, attendre, ou devant ?",
        )
    return L(
        "narrateur|Le rebord tape encore, trop plein.",
        "papa|De la place, au milieu, ou contre le bois ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "Elle tient l'étoile contre elle, sans coller.",
            2: "Elle tient le ruban, sans le dérouler encore.",
            3: "Elle tient la pince fermée, sans pincer.",
        }[t1]
        return L(
            "enfant-f|On attend le vent.",
            f"narrateur|{wait}",
            "narrateur|Le souffle passe, une fois, puis plus.",
            "enfant-f|Tu peux rester.",
            f"narrateur|{o['wait']}",
            "papa|Le vent s'est tu, maintenant.",
            "narrateur|Le papier redevient plat, tout calme.",
            "maman|Tu lui as laissé le temps.",
        )
    if t2 == 1 and t3 == 2:
        low = {
            1: "Elle pose l'étoile plus bas, loin du souffle.",
            2: "Elle colle le ruban plus bas, loin du souffle.",
            3: "Elle pince plus bas, loin du souffle.",
        }[t1]
        return L(
            "enfant-f|Plus bas, d'abord.",
            f"narrateur|{low}",
            "narrateur|Mila s'accroupit, les genoux au carreau.",
            "narrateur|L'air est plus doux, près du bois.",
            f"narrateur|{o['use']}",
            "papa|Tu as regardé d'abord.",
            "enfant-f|Ici, tu ne voles plus.",
            "maman|Le bas était plus calme.",
        )
    if t2 == 1 and t3 == 3:
        crack = {
            1: "Elle glisse l'étoile dans la fente du cadre.",
            2: "Elle pousse le ruban dans la fente du cadre.",
            3: "Elle pince la fente du cadre, tout doux.",
        }[t1]
        return L(
            "enfant-f|Dans la fente, tout petit.",
            f"narrateur|{crack}",
            "narrateur|Le bois tient, sans laisser le vent.",
            "narrateur|Mila répète, tout bas, encore une fois.",
            f"narrateur|{o['wait']}",
            "papa|La fente n'a pas soufflé.",
            "enfant-f|Tu es à l'abri.",
            "maman|Tu as parlé lentement.",
        )
    if t2 == 2 and t3 == 1:
        draw = {
            1: "Derrière le tissu, l'étoile revoit le soleil.",
            2: "Derrière le tissu, le ruban ne s'accroche plus.",
            3: "Derrière le tissu, la pince ne tire plus.",
        }[t1]
        return L(
            "enfant-f|J'écarte, tout doux.",
            "narrateur|Mila tire le rideau, un doigt seulement.",
            f"narrateur|{draw}",
            "narrateur|Le tissu s'arrête, puis se tait.",
            f"narrateur|{o['wait']}",
            "maman|Le soleil est revenu, comme un carré.",
            "enfant-f|Maintenant, tu me vois.",
            "papa|Tu as attendu le silence.",
        )
    if t2 == 2 and t3 == 2:
        still = {
            1: "Elle pose l'étoile, puis attend le tissu.",
            2: "Elle pose le ruban, puis attend le tissu.",
            3: "Elle pose la pince, puis attend le tissu.",
        }[t1]
        return L(
            "enfant-f|On attend qu'il retombe.",
            f"narrateur|{still}",
            "narrateur|Le rideau va, revient, puis s'arrête.",
            "narrateur|Le soleil redevient un seul carré, net.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas tiré trop fort.",
            "enfant-f|C'est pour toi.",
            "maman|Tu as laissé le tissu parler.",
        )
    if t2 == 2 and t3 == 3:
        front = {
            1: "Devant le tissu, l'étoile touche déjà le verre.",
            2: "Devant le tissu, le ruban colle le verre.",
            3: "Devant le tissu, la pince prend le cadre.",
        }[t1]
        return L(
            "enfant-f|Devant, tout contre la vitre.",
            "narrateur|Mila se glisse entre le rideau et le carreau.",
            f"narrateur|{front}",
            "narrateur|Le tissu reste derrière, sans cacher.",
            f"narrateur|{o['wait']}",
            "papa|Tu t'es mise devant, contre le verre.",
            "enfant-f|Le soleil est là.",
            "maman|Tu as observé d'abord.",
        )
    if t2 == 3 and t3 == 1:
        room = {
            1: "Elle pose l'étoile, puis pousse la cuillère.",
            2: "Elle pose le ruban, puis pousse la cuillère.",
            3: "Elle pose la pince, puis pousse la cuillère.",
        }[t1]
        return L(
            "enfant-f|On fait de la place, d'abord.",
            f"narrateur|{room}",
            "narrateur|La cuillère glisse, puis se tait.",
            "narrateur|Le savon recule, le bois redevient large.",
            f"narrateur|{o['wait']}",
            "papa|Le rebord n'a plus tapé.",
            "enfant-f|Maintenant, tu peux rester.",
            "maman|Tu as attendu le calme.",
        )
    if t2 == 3 and t3 == 2:
        mid = {
            1: "Au milieu, l'étoile tient, loin des bords.",
            2: "Au milieu, le ruban colle, loin des miettes.",
            3: "Au milieu, la pince trouve un bois libre.",
        }[t1]
        return L(
            "enfant-f|Au milieu, pas trop près.",
            f"narrateur|{mid}",
            "narrateur|Mila pose, puis compte un peu, tout bas.",
            "narrateur|Rien ne tinte, rien ne glisse plus.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas empilé.",
            "enfant-f|Tu es droite, maintenant.",
            "maman|Tu as préparé le chemin.",
        )
    wood = {
        1: "Contre le bois, l'étoile ne glisse plus.",
        2: "Contre le bois, le ruban tient le cadre.",
        3: "Contre le bois, la pince ferme tout doux.",
    }[t1]
    return L(
        "enfant-f|Contre le bois, tout serré.",
        f"narrateur|{wood}",
        "narrateur|Mila pince le cadre, sans toucher le savon.",
        "narrateur|Le rebord se tait, plus loin, tout seul.",
        f"narrateur|{o['wait']}",
        "papa|Le bois était assez large.",
        "enfant-f|Tu restes, étoile.",
        "maman|Le bord tenait assez.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|L'étoile brille, plate, dans le dernier soleil.",
            "enfant-f|On a attendu le vent.",
            "papa|Merci d'avoir laissé le souffle se taire.",
            "maman|Rentrez, la tarte sent l'orange.",
            f"narrateur|{coda}",
            "narrateur|Une poussière tourne encore, puis s'arrête.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Plus bas, l'étoile garde tout le jaune.",
            "enfant-f|On s'est baissées, d'abord.",
            "papa|Tu as regardé avant de coller.",
            "maman|Essuie tes genoux, sur le paillasson.",
            f"narrateur|{coda}",
            "narrateur|Un carré de soleil reste au bas du carreau.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Dans la fente, l'étoile ne tremble plus.",
            "enfant-f|Je n'ai pas ouvert trop grand.",
            "papa|La fente n'a pas soufflé.",
            "maman|Le bois est retombé, plus loin.",
            f"narrateur|{coda}",
            "narrateur|La rue se tait, derrière le verre tiède.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Derrière le rideau, l'étoile a repris le soleil.",
            "enfant-f|On a écarté, tout doux.",
            "papa|Le silence vous a aidées.",
            "maman|Le tissu sent encore la poussière chaude.",
            f"narrateur|{coda}",
            "narrateur|Un pli du rideau se recouche, tout lent.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Quand le tissu s'est tu, l'étoile a brillé.",
            "enfant-f|On a attendu qu'il retombe.",
            "papa|Tu n'as pas tiré trop fort.",
            "maman|Le soleil a parlé tout seul.",
            f"narrateur|{coda}",
            "narrateur|Un carré net reste sur le mur, puis pâlit.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Devant le tissu, l'étoile touche le verre chaud.",
            "enfant-f|Je me suis mise devant.",
            "papa|Tu t'es glissée, comme la lumière.",
            "maman|Vous rentrez, les mains pleines de soleil.",
            f"narrateur|{coda}",
            "narrateur|Le rideau reste derrière, sans cacher.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Quand la cuillère s'est tue, l'étoile a tenu.",
            "enfant-f|On a fait de la place.",
            "papa|Le rebord n'a plus tapé.",
            "maman|Vos manches sentent encore le savon.",
            f"narrateur|{coda}",
            "narrateur|Une miette sèche sur le bois, puis plus.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Au milieu, l'étoile reste droite, tout calme.",
            "enfant-f|On n'est pas allées trop près.",
            "papa|Tu n'as pas empilé.",
            "maman|Tes doigts sentent encore le papier.",
            f"narrateur|{coda}",
            "narrateur|Le savon reste à sa place, plus loin.",
        )
    return L(
        "narrateur|Contre le bois, l'étoile tient, jaune, tout calme.",
        "enfant-f|On a pincé le cadre.",
        "papa|Le bois était assez large.",
        "maman|Rentrez, l'orange est déjà coupée.",
        f"narrateur|{coda}",
        "narrateur|Le rebord se tait, plus loin, tout seul.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le carreau de la cuisine tient encore le soleil.",
        "narrateur|Une poussière tourne, lente, dans le rayon.",
        "narrateur|Ça sent l'orange, la peau un peu amère.",
        "papa|Tu as vu la tache, Mila ?",
        "enfant-f|Elle tremble sur le mur.",
        "maman|C'est l'étoile, encore jaune.",
        "narrateur|En ce moment, Mila pose deux doigts sur l'étoile.",
        "enfant-f|Je veux la coller à la vitre.",
        "papa|Le soleil s'en va déjà.",
        "maman|On prend les affaires, alors ?",
        "papa|Merci, tu as essuyé le bois.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du rebord.",
        "narrateur|L'étoile, le ruban, et la pince.",
        "maman|Tu prends quoi d'abord, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("l'étoile", "le ruban", "la pince")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Mila a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la vitre", "le rideau", "le rebord")

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
        "Cuisine, soleil bas, peau d'orange. Mila veut coller son étoile jaune "
        "dans le dernier soleil de la fenêtre, avant la nuit. "
        "T1 = étoile / ruban / pince (les trois viennent). "
        "T2 = vitre trop venteuse / rideau trop agité / rebord trop plein. "
        "T3 = neuf résolutions (vent, plus bas, fente ; écarter, attendre, devant ; "
        "place, milieu, bois). La leçon (plus de temps, plus de calme) se vit : "
        "elle attend, elle observe, elle répète tout bas. Fin : l'étoile brille.",
        "N3 ≤ 16. Slogan « Plus de temps ou de calme », Kenzo, Tom/Léa/Sami, "
        "bac/toboggan/balançoires, « bon travail », calque AUT-001 jetés. "
        "Récit autre que DIF-020 (escargot/balcon), DIF-030 (pain/four), "
        "DIF-040 (veau/ferme). Merci de papa (bois essuyé). "
        "Relecture : maman nomme l'étoile ; « On y va » au lieu d'un oui orphelin ; "
        "« contre le verre » au lieu de « comme lui » ; T3 vent moins empilé. "
        "chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-048.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
