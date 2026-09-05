#!/usr/bin/env python3
"""TREE-DIF-070 — L'album de Nina, à l'arrêt du bus (N1, DIF.PAR.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-070"
N1 = 10
TITLE = "L'album de Nina, à l'arrêt du bus"
FIL = (
    "À l'arrêt du bus, Nina veut lire la dernière page de l'album du loup, "
    "avant que le bus arrive. Victorino parle trop vite, et coupe. "
    "T1 = album rouge / ticket carton / petit coussin ; les trois partent. "
    "T2 = banc (gouttière) / vitre (buée) / bord du trottoir (bus au loin). "
    "Neuf façons de laisser Victorino finir. La dernière page, le bus, on monte."
)
CHARS = "Nina, Victorino, papa, maman"
SETTING = "arrêt du bus du village : banc mouillé, abri de verre, bord du trottoir"


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
        "il faut attendre",
        "laisser le temps",
        "attendre la fin",
        "nora",
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
        "escargot",
        "balcon",
        "veau",
        "étable",
        "abreuvoir",
        "le four",
        "marché",
        "moulinet",
        "carrousel",
        "marelle",
        "fort de coussins",
        "nez de bronze",
        "loup de carton",
        "au parc",
        "joue au salon",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
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
        "lab": "l'album",
        "ans": "album",
        "acc": "album | l'album | le rouge | l'album rouge | le livre",
        "retry": "Nina prend l'album d'abord.",
        "coda": "L'album rouge reste chaud, sur ses genoux.",
        "hip": "Sur ses genoux, l'album est tiède.",
        "wait": "L'album reste ouvert, sans bouger.",
        "use": "La dernière page attend encore, tout près.",
        "voy": "L'album penche déjà vers l'abri.",
        "cap": "L'album",
    },
    2: {
        "lab": "le ticket",
        "ans": "ticket",
        "acc": "ticket | le ticket | le carton | ticket carton",
        "retry": "Nina prend le ticket d'abord.",
        "coda": "Le ticket carton dort dans la poche.",
        "hip": "Dans sa poche, le ticket est tiède.",
        "wait": "Le ticket reste plat, sans bouger.",
        "use": "Le carton attend encore, tout plat.",
        "voy": "Le ticket penche déjà vers l'abri.",
        "cap": "Le ticket",
    },
    3: {
        "lab": "le coussin",
        "ans": "coussin",
        "acc": "coussin | le coussin | le petit coussin | le tissu",
        "retry": "Nina prend le coussin d'abord.",
        "coda": "Le petit coussin reste sous le rouge.",
        "hip": "Sous l'album, le coussin est tiède.",
        "wait": "Le coussin reste plat, sans bouger.",
        "use": "Le tissu attend encore, tout doux.",
        "voy": "Le coussin penche déjà vers l'abri.",
        "cap": "Le coussin",
    },
}

T3_LABS = {
    1: ("la goutte", "le manteau", "tout près"),
    2: ("le doigt", "le souffle", "le loup"),
    3: ("le pas", "la page", "le phare"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina prend d'abord l'album rouge.",
            "enfant-f|La dernière page, après.",
            "papa|Garde le rouge contre toi.",
            "narrateur|Le carton sent encore la pluie, un peu.",
            "maman|Le ticket, ensuite, dans la poche.",
            "narrateur|Papa glisse le coussin sous le rouge.",
            "narrateur|Les trois partent, collés à Nina.",
            "enfant-m|Le loup, il va manger !",
            "enfant-f|C'est trop tôt, Victorino.",
            "papa|L'album d'abord, tu l'as.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina prend d'abord le ticket carton.",
            "enfant-f|Pour le bus, après.",
            "maman|Garde le carton dans ta poche.",
            "narrateur|Le ticket sent encore les doigts, un peu.",
            "papa|L'album, ensuite, sur tes genoux.",
            "narrateur|Maman glisse le coussin sous le rouge.",
            "narrateur|Les trois partent, collés à Nina.",
            "enfant-m|Le loup, il va sauter !",
            "enfant-f|Pas encore, Victorino.",
            "maman|Le ticket d'abord, tu l'as.",
        )
    return L(
        "narrateur|Nina prend d'abord le petit coussin.",
        "enfant-f|Pour le banc mouillé.",
        "papa|Mets le tissu sous le rouge.",
        "narrateur|Le coussin sent encore le tiroir, un peu.",
        "maman|L'album, ensuite, et le ticket.",
        "narrateur|Papa les pose contre elle, tout près.",
        "narrateur|Les trois partent, collés à Nina.",
        "enfant-m|Le loup, il va crier !",
        "enfant-f|Laisse, je lis encore.",
        "papa|Le coussin d'abord, tu l'as.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|L'album reste sur ses genoux.",
            "enfant-f|On va jusqu'à la fin.",
            "maman|Le bus n'est pas là.",
            "papa|Tu tiens bien, Nina ?",
            "enfant-f|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|Le ticket pend à sa poche, un peu.",
            "enfant-f|Il va servir, après.",
            "papa|Ça sent encore le carton, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le carton se tait, puis plus rien.",
        )
    return L(
        "narrateur|Le coussin reste plat, sous le rouge.",
        "enfant-f|Le banc ne mouille plus.",
        "maman|Le tissu sent encore le tiroir.",
        "papa|On avance, tous les quatre ?",
        "enfant-f|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Le banc goutte encore, trop fort.",
        "narrateur|La vitre a trop de buée.",
        "narrateur|Le bord voit le bus, trop loin.",
        "papa|Nina, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Une goutte tombe sur le rouge, déjà.",
            2: "Une goutte mouille le ticket, déjà.",
            3: "Une goutte pèse sur le coussin, déjà.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|La gouttière tape trop, trop fort.",
            f"narrateur|{extra}",
            "enfant-m|Le loup, il va !",
            "narrateur|Une goutte couvre le mot, déjà.",
            "enfant-f|Il va quoi ?",
            "narrateur|Victorino reprend trop vite, trop fort.",
            "papa|On n'entend plus le mot.",
            "maman|La goutte a pris sa phrase.",
            "enfant-f|Alors on fait quoi ?",
            "papa|Tu vois comment, Nina ?",
        )
    if t2 == 2:
        extra = {
            1: "Le rouge se colle à la buée.",
            2: "Le carton se colle à la buée.",
            3: "Le tissu se colle à la buée.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|La buée cache trop le verre.",
            f"narrateur|{extra}",
            "enfant-m|Le loup, il va !",
            "enfant-f|Il court, c'est ça ?",
            "narrateur|Victorino secoue la tête, trop vite.",
            "papa|On n'a pas vu sa bouche.",
            "maman|La buée a pris le mot.",
            "enfant-f|Alors on fait quoi ?",
            "maman|Tu vois comment, Nina ?",
        )
    extra = {
        1: "L'album penche trop vers la rue.",
        2: "Le ticket penche trop vers la rue.",
        3: "Le coussin penche trop vers la rue.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Un phare brille trop loin, déjà.",
        f"narrateur|{extra}",
        "enfant-m|Le loup, il va !",
        "enfant-f|Dépêche, le bus arrive !",
        "narrateur|Le mot de Victorino s'arrête net.",
        "papa|Le bus est encore loin.",
        "maman|Sa phrase n'est pas finie.",
        "enfant-f|Alors on fait quoi ?",
        "papa|Tu vois comment, Nina ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La gouttière n'a pas fini.",
            "papa|La goutte, le manteau, ou tout près ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La buée n'a pas fini.",
            "maman|Le doigt, le souffle, ou le loup ?",
        )
    return L(
        "narrateur|Le phare n'a pas fini.",
        "papa|Le pas, la page, ou le phare ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "Nina tient l'album, sans tourner.",
            2: "Nina tient le ticket, sans parler.",
            3: "Nina tient le coussin, sans bouger.",
        }[t1]
        return L(
            "enfant-f|On attend la goutte.",
            f"narrateur|{hold}",
            "narrateur|La gouttière se tait, une fois.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['wait']}",
            "papa|Le mot est arrivé, tout entier.",
            "enfant-f|Il s'endort.",
            "maman|La page peut venir, maintenant.",
        )
    if t2 == 1 and t3 == 2:
        cover = {
            1: "Maman pose le manteau sur le rouge.",
            2: "Maman pose le manteau sur le ticket.",
            3: "Maman pose le manteau sur le coussin.",
        }[t1]
        return L(
            "enfant-f|Le manteau, dessus.",
            f"narrateur|{cover}",
            "narrateur|La goutte tombe à côté, tout doux.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['use']}",
            "papa|On a entendu, sous le tissu.",
            "enfant-f|Il s'endort.",
            "maman|Le manteau a gardé la page.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-f|Tout près, j'écoute.",
            "narrateur|Nina se glisse contre Victorino, tout doux.",
            "narrateur|La goutte reste loin, déjà.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['wait']}",
            "papa|Tu t'es mise tout près.",
            "enfant-f|Il s'endort.",
            "maman|Ses mots sont arrivés.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-f|Le doigt, sur la buée.",
            "narrateur|Nina trace un rond, tout net.",
            "narrateur|La bouche de Victorino se voit, enfin.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['use']}",
            "papa|On a vu le mot, sur ses lèvres.",
            "enfant-f|Il s'endort.",
            "maman|Le rond a laissé la suite.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-f|On souffle ensemble.",
            "narrateur|Nina et Victorino respirent, tout calmes.",
            "narrateur|Personne ne devine trop tôt.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['wait']}",
            "papa|Vous avez respiré, puis parlé.",
            "enfant-f|Il s'endort.",
            "maman|Le souffle a laissé sa place.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-f|Le loup, sur le dessin.",
            "narrateur|Nina pose le doigt sur le loup.",
            "narrateur|Victorino regarde aussi, sans parler.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['use']}",
            "papa|Le dessin a tenu le mot.",
            "enfant-f|Il s'endort.",
            "maman|Vous avez regardé ensemble.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-f|On reste, un pas.",
            "narrateur|Nina ne court pas vers le phare.",
            "narrateur|Victorino reprend, tout calme.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['wait']}",
            "papa|Le bus est encore loin.",
            "enfant-f|Il s'endort.",
            "maman|Vous n'avez pas couru.",
        )
    if t2 == 3 and t3 == 2:
        keep = {
            1: "Nina garde l'album ouvert, tout près.",
            2: "Nina garde le ticket plat, tout près.",
            3: "Nina garde le coussin plat, tout près.",
        }[t1]
        return L(
            "enfant-f|La page, encore ouverte.",
            f"narrateur|{keep}",
            "narrateur|Victorino pose un doigt, puis parle.",
            "enfant-m|Le loup, il s'endort.",
            f"narrateur|{o['use']}",
            "papa|La page a gardé le mot.",
            "enfant-f|Il s'endort.",
            "maman|Vous avez lu ensemble.",
        )
    count = {
        1: "L'album reste ouvert pendant le compte.",
        2: "Le ticket reste plat pendant le compte.",
        3: "Le coussin reste plat pendant le compte.",
    }[t1]
    return L(
        "enfant-f|Le phare, on le compte.",
        "narrateur|Le rond jaune grandit, tout lent.",
        f"narrateur|{count}",
        "enfant-m|Le loup, il s'endort.",
        f"narrateur|{o['wait']}",
        "papa|Le phare n'a pas coupé le mot.",
        "enfant-f|Il s'endort.",
        "maman|Le compte a laissé sa phrase.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Nina tourne la dernière page, tout doux.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, l'album fermé.",
            f"narrateur|{coda}",
            "narrateur|Une goutte sèche sur le banc, derrière.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous le manteau, la dernière page s'ouvre.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, le manteau sur le rouge.",
            f"narrateur|{coda}",
            "narrateur|Le tissu reste un peu mouillé, derrière.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Tout près, la dernière page s'ouvre.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, les deux têtes ensemble.",
            f"narrateur|{coda}",
            "narrateur|Le banc reste vide, tout mouillé.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Dans le rond, la dernière page s'ouvre.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, l'album fermé.",
            f"narrateur|{coda}",
            "narrateur|Un rond clair reste sur la vitre.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Après le souffle, la dernière page s'ouvre.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, l'album fermé.",
            f"narrateur|{coda}",
            "narrateur|La buée revient, tout doux, derrière.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sous le doigt, la dernière page s'ouvre.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, le loup caché.",
            f"narrateur|{coda}",
            "narrateur|Le dessin reste au chaud, fermé.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Sans courir, la dernière page s'ouvre.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, sans se presser.",
            f"narrateur|{coda}",
            "narrateur|Le bord du trottoir reste vide, derrière.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La page ouverte se ferme, tout doux.",
            "enfant-f|Le loup dort, enfin.",
            "papa|Le bus s'arrête, tout calme.",
            "maman|On monte, le rouge contre elle.",
            f"narrateur|{coda}",
            "narrateur|Le ticket passe près de la porte.",
        )
    return L(
        "narrateur|Sous le phare, la dernière page s'ouvre.",
        "enfant-f|Le loup dort, enfin.",
        "papa|Le bus s'arrête, tout calme.",
        "maman|On monte, le phare tout près.",
        f"narrateur|{coda}",
        "narrateur|Le rond jaune s'éteint, déjà parti.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une gouttière tape encore, tout lent.",
        "narrateur|L'abri de verre garde la pluie.",
        "narrateur|Ça sent le bitume mouillé, un peu.",
        "papa|Le banc est encore tout froid.",
        "enfant-f|Mon album, il est resté sec.",
        "maman|Le loup attend sa dernière page.",
        "narrateur|En ce moment, Nina ouvre le rouge.",
        "enfant-f|Avant le bus, je finis.",
        "narrateur|Victorino parle déjà trop vite.",
        "enfant-m|Le loup, il va manger !",
        "papa|Merci, tu as essuyé le banc.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près des genoux, trois affaires attendent.",
        "narrateur|L'album, le ticket, le coussin.",
        "maman|Par quoi tu commences, Nina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("l'album", "le ticket", "le coussin")

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
        extras[f"{p}_T0002_P0000"] = t3lab("le banc", "la vitre", "le bord")

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
        "Arrêt du bus du village, banc mouillé, abri de verre, bitume. "
        "Nina veut lire la dernière page de l'album du loup, avant le bus. "
        "Victorino parle trop vite, coupe. "
        "T1 = album rouge / ticket carton / petit coussin (les trois viennent). "
        "T2 = banc trop goutte / vitre trop buée / bord trop pressé. "
        "T3 = neuf résolutions (goutte, manteau, tout près ; doigt, souffle, loup ; "
        "pas, page, phare). La leçon se vit : on laisse Victorino finir, "
        "on relit ensemble. Fin : dernière page, le loup dort, on monte.",
        "N1 ≤ 10. Slogan « Laisser le temps à l'autre de finir sa phrase — au parc », "
        "Nora, Tom/Léa/Sami, bac/toboggan/balançoires, « bon travail », "
        "« voici le geste » jetés. Monde autre que DIF-005/056 (parc), "
        "DIF-040/062 (ferme), DIF-046 (marché/moulinet), DIF-054 (loup de carton). "
        "Merci de papa (banc essuyé). chunk_id inchangés. check() OK. "
        "xlsx : stories/archive/arbres/TREE-DIF-070.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
