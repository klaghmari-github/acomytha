#!/usr/bin/env python3
"""TREE-DIF-072 — Le sac bleu de Sarah, au vestiaire (N2, DIF.BES.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-072"
N2 = 15
TITLE = "Le sac bleu de Sarah, au vestiaire"
FIL = (
    "Au vestiaire, Sarah veut fermer son sac bleu à la dernière maille, "
    "avant la cloche, sans qu'on la presse. Elle prend d'abord le sac, "
    "le goûter enveloppé ou le petit grelot ; les trois viennent. "
    "Sous les manteaux ça goutte, près de la porte ça pousse, "
    "au banc du fond c'est trop sombre. Neuf façons de prendre le temps. "
    "Le sac clique, la cloche, la main de papa."
)
CHARS = "Sarah, papa, maman"
SETTING = "vestiaire de l'école : manteaux, crochets, banc du fond"


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
        "inès",
        "ines",
        "kenzo",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "il faut attendre",
        "marelle",
        "soleil en papier",
        "galet",
        "fort de",
        "étoile",
        "citronnade",
        "poisson",
        "tapis",
        "escargot",
        "balcon",
        "veau",
        "étable",
        "le four",
        "marché",
        "moulinet",
        "carrousel",
        "bulle",
        "bronze",
        "tilleul",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    if aj.count("merci") + aj.count("bravo") != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{aj.count('merci') + aj.count('bravo')}")
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
        "lab": "le sac",
        "ans": "sac",
        "acc": "sac | le sac | d'abord le sac | le sac bleu | sac bleu",
        "retry": "Sarah prend le sac d'abord.",
        "coda": "Le sac bleu reste fermé, une maille encore brillante.",
        "hip": "Contre son ventre, le sac bleu est encore ouvert.",
        "wait": "Le sac reste posé, sans bouger.",
        "use": "Une maille cherche encore le curseur.",
    },
    2: {
        "lab": "le goûter",
        "ans": "goûter",
        "acc": "goûter | le goûter | d'abord le goûter | le papier | gouter | le gouter",
        "retry": "Sarah prend le goûter d'abord.",
        "coda": "Le papier du goûter reste plié, une miette au pli.",
        "hip": "Dans sa paume, le goûter enveloppé est tiède.",
        "wait": "Enveloppé, le goûter reste contre son pouce.",
        "use": "Le papier du goûter tient, tout calme.",
    },
    3: {
        "lab": "le grelot",
        "ans": "grelot",
        "acc": "grelot | le grelot | d'abord le grelot | le petit grelot",
        "retry": "Sarah prend le grelot d'abord.",
        "coda": "Le grelot se tait, accroché à la fermeture.",
        "hip": "Entre ses doigts, le petit grelot est froid.",
        "wait": "Le grelot reste muet, sans bouger.",
        "use": "Le grelot tinte une fois, tout bas.",
    },
}

T3_LABS = {
    1: ("poser le sac", "compter", "recommencer"),
    2: ("plus loin", "les mailles", "un instant"),
    3: ("la lumière", "les genoux", "tout doux"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah attrape d'abord le sac bleu, encore ouvert.",
            "enfant-f|La dernière maille est à moi.",
            "maman|Garde la fermeture tout droit.",
            "narrateur|Le curseur tremble un peu, puis tient.",
            "papa|Prends le goûter, il est à tes pieds.",
            "narrateur|Le grelot glisse sous son autre bras.",
            "narrateur|Les trois partent, collés à Sarah.",
            "enfant-f|Maille, j'arrive.",
            "narrateur|Le sac sent la laine, un peu.",
            "papa|Le sac est à toi, maintenant.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah prend d'abord le goûter, tout enveloppé.",
            "enfant-f|Il va dans le sac.",
            "papa|Le papier reste fermé, pas trop serré.",
            "narrateur|Le pli tient, puis se tait.",
            "maman|Le sac est là, près du crochet.",
            "narrateur|Papa pose le grelot contre sa manche.",
            "narrateur|Sarah serre les trois contre son ventre.",
            "enfant-f|Goûter, tu restes avec moi.",
            "narrateur|Le papier colle un peu sa manche.",
            "maman|Le goûter est prêt, tu peux y aller.",
        )
    return L(
        "narrateur|Sarah lève d'abord le grelot, tout petit.",
        "enfant-f|Il va sur le sac.",
        "maman|Tout doux, il tinte vite.",
        "narrateur|Le grelot tinte, puis se tait.",
        "papa|Voici le sac, et le goûter.",
        "narrateur|Il les glisse contre son genou.",
        "narrateur|Le crochet reste vide, derrière eux.",
        "enfant-f|Grelot, je te porte.",
        "narrateur|Un tout petit son reste encore.",
        "papa|Le grelot est prêt, on avance.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|Le sac reste contre elle, encore ouvert.",
            "enfant-f|On va jusqu'à la maille.",
            "maman|La cloche n'est pas loin.",
            "papa|Tu tiens bien, Sarah ?",
            "enfant-f|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|Le goûter pend au poignet, un peu lâche.",
            "enfant-f|Il va dans le sac.",
            "papa|Ça sent encore le biscuit, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le papier se tait, puis plus rien.",
        )
    return L(
        "narrateur|Le grelot reste froid, contre son pouce.",
        "enfant-f|Il ne tinte plus.",
        "maman|Le métal sent encore la pluie.",
        "papa|On avance, tous les trois ?",
        "enfant-f|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le sac penche vers les crochets, déjà.",
        2: "Le goûter colle encore à sa manche.",
        3: "Le grelot appuie contre son pouce.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Sous les manteaux, des gouttes tombent encore.",
        "narrateur|Près de la porte, l'air pousse trop.",
        "narrateur|Au banc du fond, c'est trop sombre.",
        "papa|Sarah, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "La maille glisse, trop mouillée, trop vite.",
            2: "Le papier se mouille, trop vite, trop froid.",
            3: "Le grelot tinte, trop mouillé, trop fort.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Les manteaux gouttent dans son cou, trop fort.",
            f"narrateur|{extra}",
            "enfant-f|Ma maille a glissé !",
            "narrateur|Encore une goutte, encore dans le cou.",
            "narrateur|La fermeture reste trop mouillée, trop loin.",
            "papa|Ici, ça n'arrête pas.",
            "maman|Le sac a besoin de calme.",
            "enfant-f|Alors on fait quoi ?",
            "papa|Tu vois comment, Sarah ?",
        )
    if t2 == 2:
        extra = {
            1: "La maille saute, trop poussée par l'air.",
            2: "Le papier s'envole, trop pris par le courant.",
            3: "Le grelot tinte trop, trop pris par le bruit.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|La porte laisse un courant, trop fort.",
            f"narrateur|{extra}",
            "enfant-f|Ça saute trop !",
            "narrateur|Un pas dehors, encore du bruit.",
            "narrateur|La fermeture n'arrive pas, trop vite.",
            "papa|Ici, ça souffle trop.",
            "maman|Le sac n'arrive pas.",
            "enfant-f|Alors on fait quoi ?",
            "maman|Tu vois comment, Sarah ?",
        )
    extra = {
        1: "La maille se cache, trop noire, trop basse.",
        2: "Le papier se perd, trop sombre, trop tard.",
        3: "Le grelot se tait, trop sombre pour le voir.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Le banc du fond reste trop sombre, trop bas.",
        f"narrateur|{extra}",
        "enfant-f|Je ne vois plus la maille !",
        "narrateur|La cloche n'est plus si loin, déjà.",
        "narrateur|La fermeture cherche, trop tard, trop noir.",
        "papa|Ici, c'est trop calme, trop tard.",
        "maman|Le sac n'arrive pas.",
        "enfant-f|Alors on fait quoi ?",
        "papa|Tu vois comment, Sarah ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Les manteaux n'ont pas fini de goutter.",
            "papa|Poser le sac, compter, ou recommencer ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La porte n'a pas fini de pousser.",
            "maman|Plus loin, les mailles, ou un instant ?",
        )
    return L(
        "narrateur|Le banc n'a pas fini d'être sombre.",
        "papa|La lumière, les genoux, ou tout doux ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        pose = {
            1: "Le sac ne prend plus les gouttes.",
            2: "Le goûter ne prend plus les gouttes.",
            3: "Le grelot ne prend plus les gouttes.",
        }[t1]
        return L(
            "enfant-f|Je pose le sac, d'abord.",
            "narrateur|Sarah pose le sac sur le carrelage sec.",
            f"narrateur|{pose}",
            "enfant-f|Toi, tu restes au sec.",
            f"narrateur|{o['wait']}",
            "papa|Tu as posé ça, hors des gouttes.",
            "narrateur|La fermeture avance, maille après maille.",
            "maman|Tu as pris ce moment, tout calme.",
        )
    if t2 == 1 and t3 == 2:
        cnt = {
            1: "Elle tient le sac, et compte tout bas.",
            2: "Elle tient le goûter, et compte tout bas.",
            3: "Elle tient le grelot, et compte tout bas.",
        }[t1]
        return L(
            "enfant-f|Je compte les gouttes.",
            f"narrateur|{cnt}",
            "narrateur|Une goutte, deux gouttes, puis plus.",
            "enfant-f|Maintenant, tu peux fermer.",
            f"narrateur|{o['wait']}",
            "papa|Tu as compté, sans te presser.",
            "narrateur|La fermeture glisse, tout droit.",
            "maman|Les gouttes t'ont laissée faire.",
        )
    if t2 == 1 and t3 == 3:
        re = {
            1: "Elle ramène le curseur du sac, tout en bas.",
            2: "Elle ramène le curseur, goûter déjà dedans.",
            3: "Elle ramène le curseur, grelot au bord.",
        }[t1]
        return L(
            "enfant-f|Je recommence, depuis le bas.",
            f"narrateur|{re}",
            "narrateur|Elle reprend la maille du bas, tout doux.",
            f"narrateur|{o['use']}",
            "papa|Tu as repris depuis le début.",
            "enfant-f|Cette fois, tu tiens.",
            "maman|Tu n'as pas tiré trop fort.",
        )
    if t2 == 2 and t3 == 1:
        loin = {
            1: "Elle recule le sac, loin de la porte.",
            2: "Elle recule le goûter, loin de la porte.",
            3: "Elle recule le grelot, loin de la porte.",
        }[t1]
        return L(
            "enfant-f|Plus loin, loin du courant.",
            f"narrateur|{loin}",
            "narrateur|Sarah recule d'un pas, vers les crochets.",
            f"narrateur|{o['use']}",
            "papa|Tu t'es mise hors du vent.",
            "enfant-f|Ici, tu ne sautes plus.",
            "maman|Loin de la porte, ça tenait mieux.",
        )
    if t2 == 2 and t3 == 2:
        mail = {
            1: "Elle touche chaque maille du sac, tout lentement.",
            2: "Elle touche chaque maille, goûter déjà dedans.",
            3: "Elle touche chaque maille, grelot au bord.",
        }[t1]
        return L(
            "enfant-f|Les mailles, une par une.",
            f"narrateur|{mail}",
            "narrateur|Le courant n'attrape plus le curseur.",
            f"narrateur|{o['wait']}",
            "papa|Tu as compté les mailles, une à une.",
            "enfant-f|Tu es fermé, maintenant.",
            "maman|Chaque maille a eu son temps.",
        )
    if t2 == 2 and t3 == 3:
        inst = {
            1: "Sarah respire, le sac contre le ventre.",
            2: "Sarah respire, le goûter contre la paume.",
            3: "Sarah respire, le grelot entre les doigts.",
        }[t1]
        return L(
            "enfant-f|Un instant, papa.",
            "papa|Je reste, je ne te presse pas.",
            f"narrateur|{inst}",
            f"narrateur|{o['wait']}",
            "narrateur|Le courant passe, puis s'en va.",
            "enfant-f|Maintenant, j'y vais.",
            "maman|Tu as demandé cet instant.",
            "papa|Le sac peut fermer, maintenant.",
        )
    if t2 == 3 and t3 == 1:
        lum = {
            1: "Un carré de jour tombe sur le sac.",
            2: "Un carré de jour tombe sur le goûter.",
            3: "Un carré de jour tombe sur le grelot.",
        }[t1]
        return L(
            "enfant-f|La lumière, d'abord.",
            "narrateur|Sarah glisse le sac vers la porte, un peu.",
            f"narrateur|{lum}",
            f"narrateur|{o['use']}",
            "maman|La fermeture se voit, maintenant.",
            "enfant-f|Je vois la dernière maille.",
            "papa|Tu as pris le jour, tout doux.",
        )
    if t2 == 3 and t3 == 2:
        gen = {
            1: "Le sac s'installe sur ses genoux.",
            2: "Le goûter s'installe sur ses genoux.",
            3: "Le grelot s'installe sur ses genoux.",
        }[t1]
        return L(
            "enfant-f|Sur les genoux, je vois mieux.",
            "narrateur|Sarah pose le sac sur ses genoux.",
            f"narrateur|{gen}",
            f"narrateur|{o['wait']}",
            "papa|Tes genoux tiennent le sac, bien droit.",
            "enfant-f|La maille est là.",
            "maman|Tu as posé le sac, tout près.",
        )
    doux = {
        1: "Elle ferme le sac tout bas, sans tirer.",
        2: "Elle ferme, goûter déjà calme dedans.",
        3: "Elle ferme, grelot tout muet au bord.",
    }[t1]
    return L(
        "enfant-f|Tout doux, sans me presser.",
        f"narrateur|{doux}",
        "narrateur|Le banc reste sombre, mais ça avance.",
        f"narrateur|{o['use']}",
        "papa|Tu n'as pas tiré trop vite.",
        "enfant-f|Tu cliques, sac.",
        "maman|Le petit geste a suffi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le sac clique, net, hors des gouttes.",
            "enfant-f|On a posé le sac.",
            "papa|Tes doigts sont secs, maintenant.",
            "maman|La cloche n'a pas encore sonné.",
            f"narrateur|{coda}",
            "narrateur|Sarah prend la main de papa, vers la porte.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le sac clique, après les gouttes tues.",
            "enfant-f|On a compté, d'abord.",
            "papa|Tu n'as pas tiré trop tôt.",
            "maman|La cloche sonne, essuie ton cou.",
            f"narrateur|{coda}",
            "narrateur|Sarah glisse sa main dans celle de papa.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le sac clique, repris depuis le bas.",
            "enfant-f|J'ai recommencé, tout doux.",
            "papa|Tu as repris la maille du bas.",
            "maman|La cloche peut sonner, on part.",
            f"narrateur|{coda}",
            "narrateur|La main de Sarah reste dans celle de papa.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Plus loin, le sac clique, hors du vent.",
            "enfant-f|On s'est reculées, d'abord.",
            "papa|Tu t'es mise hors du courant.",
            "maman|La cloche sonne, près de la porte.",
            f"narrateur|{coda}",
            "narrateur|Sarah prend la main de papa, déjà dehors.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Maille après maille, le sac clique enfin.",
            "enfant-f|On a compté les mailles.",
            "papa|Chaque maille a eu son temps.",
            "maman|La cloche sonne, on y va.",
            f"narrateur|{coda}",
            "narrateur|Sa main reste dans celle de papa.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Après l'instant, le sac clique, net.",
            "enfant-f|J'ai demandé un instant.",
            "papa|Je ne t'ai pas pressée.",
            "maman|La cloche peut sonner, maintenant.",
            f"narrateur|{coda}",
            "narrateur|La main de Sarah reste dans celle de papa.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Sous le jour, le sac clique, net.",
            "enfant-f|On a pris la lumière.",
            "papa|La fermeture s'est vue, alors elle a tenu.",
            "maman|La cloche sonne, le banc reste derrière.",
            f"narrateur|{coda}",
            "narrateur|Ils passent la porte, la main dans la main.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sur les genoux, le sac clique, tout près.",
            "enfant-f|On a posé le sac.",
            "papa|Tes genoux ont tenu la fermeture.",
            "maman|La cloche sonne, on y va.",
            f"narrateur|{coda}",
            "narrateur|Sarah serre la main de papa, déjà dehors.",
        )
    return L(
        "narrateur|Tout doux, le sac clique, puis se tait.",
        "enfant-f|On n'a pas tiré trop vite.",
        "papa|Le petit geste a suffi.",
        "maman|La cloche sonne, tes doigts sentent la laine.",
        f"narrateur|{coda}",
        "narrateur|Ils partent par la porte, main dans la main.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Derrière la porte vitrée, le vestiaire sent encore la pluie.",
        "narrateur|Les crochets tiennent des manteaux lourds, tout mouillés.",
        "narrateur|Une goutte glisse du col rouge jusqu'au carrelage.",
        "papa|Ton crochet a un grelot, Sarah.",
        "enfant-f|Il tinte quand je le touche.",
        "maman|Le carrelage est froid, sous tes chaussures.",
        "narrateur|En ce moment, Sarah ouvre son sac bleu, trop vite.",
        "enfant-f|Je veux la dernière maille, sans qu'on me presse.",
        "papa|La cloche n'a pas encore sonné.",
        "maman|Le goûter est encore dans le papier.",
        "papa|Merci, tu as essuyé le crochet.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près du crochet, trois affaires restent.",
        "narrateur|Un sac bleu, un goûter, un petit grelot.",
        "maman|Par quoi tu commences, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le sac bleu", "le goûter", "le grelot")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Sarah a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab(
            "sous les manteaux", "près de la porte", "le banc du fond"
        )

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
        "Vestiaire de l'école, fin de jour, manteaux qui gouttent, crochets, "
        "carrelage froid, cloche au loin. Sarah veut fermer son sac bleu à la "
        "dernière maille, avant la cloche, sans qu'on la presse. "
        "T1 = sac bleu / goûter enveloppé / petit grelot (les trois viennent). "
        "T2 = sous les manteaux (gouttes dans le cou) / près de la porte "
        "(courant, bruit) / banc du fond (trop sombre, trop calme trop tard). "
        "T3 = neuf façons de prendre le temps (poser, compter, recommencer ; "
        "plus loin, mailles, un instant ; lumière, genoux, tout doux). "
        "La leçon se vit : elle pose, elle compte, elle demande, elle reprend. "
        "Fin : le sac clique, la cloche, la main dans celle de papa.",
        "N2 ≤ 15. Slogan « Plus de temps ou de calme — à l'école », Inès, "
        "Tom/Léa/Sami, bac/toboggan/balançoires, « il faut attendre », "
        "« bon travail » jetés. Récit autre que DIF-022/023 (marelle), "
        "DIF-034 (soleil papier), DIF-045 (galet), DIF-021 (fort fenêtre), "
        "DIF-048 (étoile), DIF-055 (citronnade), DIF-049 (poissons tapis), "
        "DIF-056 (bulle/bronze). Merci de papa (crochet essuyé), une fois. "
        "chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-072.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
