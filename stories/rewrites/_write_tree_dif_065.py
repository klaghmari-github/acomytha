#!/usr/bin/env python3
"""TREE-DIF-065 — Les arrosoirs de Chouchou, dans la serre (N1, DIF.BES.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-065"
N1 = LIMITS["N1"]
TITLE = "Les arrosoirs de Chouchou, dans la serre"
FIL = (
    "Après la pluie, la serre derrière la maison reste embuée. "
    "Chouchou veut un défilé d'arrosoirs le long des planches, "
    "pour que Raphaël arrose avec elle. Elle prend d'abord l'arrosoir rouge, "
    "la graine de basilic ou le tablier à pois ; les trois partent. "
    "À l'allée la flaque retient Raphaël, à la table la terre colle, "
    "au bac les feuilles mouillent le visage. Il dit non, autre chose, "
    "ou plus tard. Elle accepte. Un seul arrosoir, une seule plante, on rentre."
)
CHARS = "Chouchou, Raphaël, papa, maman"
SETTING = "serre derrière la maison, après la pluie : allée, table, bac"


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
        "inviter sans forcer",
        "accepter plusieurs",
        "jules",
        "pommier",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
        "après la sieste",
        "panier rouge",
        "figuier",
        "poupée",
        "poisson",
        "stand",
        "biscuit",
        "fort de coussins",
        "wagon",
        "il faut attendre",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob or "raphaël" not in blob:
        raise SystemExit(f"{SID}: troupe Chouchou/Raphaël absente")
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
        "lab": "l'arrosoir rouge",
        "ans": "arrosoir",
        "acc": "arrosoir | l'arrosoir | l'arrosoir rouge | le rouge",
        "retry": "Chouchou a pris l'arrosoir.",
        "coda": "L'arrosoir rouge a encore une goutte.",
        "hip": "L'arrosoir rouge pèse contre son bras.",
        "wait": "L'arrosoir rouge attend, sans verser.",
        "use": "Une goutte tremble encore au bec.",
    },
    2: {
        "lab": "la graine",
        "ans": "graine",
        "acc": "graine | la graine | la graine de basilic | basilic",
        "retry": "Chouchou a pris la graine.",
        "coda": "La graine dort déjà dans la terre.",
        "hip": "La graine reste au chaud, dans sa poche.",
        "wait": "La graine attend, toute sèche.",
        "use": "La graine pique encore sa paume.",
    },
    3: {
        "lab": "le tablier à pois",
        "ans": "tablier",
        "acc": "tablier | le tablier | le tablier à pois | les pois",
        "retry": "Chouchou a mis le tablier.",
        "coda": "Le tablier à pois sent encore le basilic.",
        "hip": "Le tablier à pois colle un peu, déjà.",
        "wait": "Le tablier à pois attend, tout mouillé.",
        "use": "Un pois blanc brille, tout humide.",
    },
}

T3_LABS = {
    1: ("le bord", "la feuille", "les bottes"),
    2: ("le godet", "la terre", "le robinet"),
    3: ("le pas", "le basilic", "le torchon"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Chouchou prend d'abord l'arrosoir rouge.",
            "enfant-f|Il est encore un peu lourd.",
            "maman|Tiens le bec, tout doux.",
            "narrateur|Une goutte tombe sur sa botte.",
            "papa|La graine et le tablier viennent aussi.",
            "narrateur|Elle glisse le tablier sous son bras.",
            "narrateur|La graine reste au fond d'une poche.",
            "enfant-f|Raphaël va arroser avec moi.",
            "papa|Tu lui proposes, tout calme ?",
            "enfant-f|Oui, papa.",
            "maman|Les trois affaires partent, déjà.",
        )
    if t1 == 2:
        return L(
            "narrateur|Chouchou prend d'abord la graine.",
            "enfant-f|Elle est toute petite, toute sèche.",
            "papa|Garde-la dans ta paume, alors.",
            "narrateur|La graine sent déjà le basilic.",
            "maman|L'arrosoir t'attend, près du seau.",
            "narrateur|Elle enfile le tablier, tout de suite.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|On va la planter, avec Raphaël.",
            "maman|Tu lui proposes, tout calme ?",
            "enfant-f|Oui, maman.",
            "papa|La poche garde bien la graine.",
        )
    return L(
        "narrateur|Chouchou enfile d'abord le tablier à pois.",
        "enfant-f|Les pois sont tout ronds.",
        "maman|Les poches sont déjà un peu humides.",
        "narrateur|Elle glisse la graine dans une poche.",
        "papa|Voici l'arrosoir, accroche-le.",
        "narrateur|Le bec rouge tape contre son genou.",
        "narrateur|Rien ne reste près de la porte.",
        "enfant-f|Raphaël va aimer les pois.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-f|Oui.",
        "maman|Le tablier tient déjà, tout noué.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|L'arrosoir rouge pèse déjà.",
            "maman|Elle a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|La graine reste dans sa paume.",
            "papa|Elle a pris quoi, d'abord ?",
        )
    return L(
        "narrateur|Le tablier à pois tient déjà.",
        "maman|Elle a mis quoi, d'abord ?",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "enfant-f|L'arrosoir.",
            "maman|Oui.",
            "narrateur|Une goutte glisse encore du bec.",
            "enfant-f|On va jusqu'à Raphaël.",
            "papa|La serre est encore toute embuée.",
            "enfant-f|Oui, papa, j'y vais.",
            f"narrateur|{o['use']}",
            "maman|Les planches sentent la terre mouillée.",
        )
    if t1 == 2:
        return L(
            "enfant-f|La graine.",
            "papa|Oui.",
            "narrateur|Un peu de terre colle au pouce.",
            "enfant-f|On va la montrer à Raphaël.",
            "maman|Ça sent le basilic, déjà.",
            "enfant-f|Oui, maman.",
            f"narrateur|{o['use']}",
            "papa|La poche reste bien fermée.",
        )
    return L(
        "enfant-f|Le tablier.",
        "maman|Oui.",
        "narrateur|Un pois blanc brille, tout mouillé.",
        "enfant-f|Raphaël va voir les pois.",
        "papa|On avance, tous les trois ?",
        "enfant-f|Oui.",
        f"narrateur|{o['use']}",
        "maman|Les poches sentent encore l'eau.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Raphaël est déjà dans la serre.",
        "maman|L'allée a une flaque, au milieu.",
        "narrateur|La table à rempoter colle encore.",
        "papa|Le bac à tomates tremble, tout mouillé.",
        "papa|On va vers où, Chouchou ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Une goutte tombe dans la flaque, ploc.",
            2: "La graine reste au sec, dans la poche.",
            3: "Un pois blanc se mouille, déjà.",
        }[t1]
        ask = {
            1: "Raphaël, on fait un défilé ?",
            2: "Raphaël, on plante, puis on arrose ?",
            3: "Raphaël, tu prends un arrosoir ?",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Raphaël est accroupi, tout près de l'eau.",
            f"enfant-f|{ask}",
            "copain|Non, la flaque d'abord.",
            "enfant-f|On aligne tout, le long des planches.",
            "copain|Mes bottes restent ici.",
            f"narrateur|{extra}",
            "maman|Il ne bouge pas, encore.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute, d'abord.",
        )
    if t2 == 2:
        extra = {
            1: "Le bec rouge sonne contre le bois.",
            2: "La graine pique sa paume, tout sec.",
            3: "Un pois blanc se tache de brun.",
        }[t1]
        ask = {
            1: "Raphaël, tu arroses avec moi ?",
            2: "Raphaël, on plante la graine ?",
            3: "Raphaël, tu veux le tablier ?",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Raphaël a de la terre aux doigts.",
            f"enfant-f|{ask}",
            "copain|Mes mains collent trop.",
            "enfant-f|Le défilé commence ici, alors.",
            "copain|Le godet, d'abord.",
            f"narrateur|{extra}",
            "maman|Il ne lâche pas le godet.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute, d'abord.",
        )
    extra = {
        1: "Le bec rouge passe sous les feuilles.",
        2: "La poche frotte une feuille, tout mouillé.",
        3: "Un pois blanc se colle d'eau.",
    }[t1]
    ask = {
        1: "Raphaël, on arrose les feuilles ?",
        2: "Raphaël, on plante ici, tout près ?",
        3: "Raphaël, tu viens sous les feuilles ?",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Une feuille mouillée tape le visage.",
        "copain|Ça mouille, Chouchou !",
        f"enfant-f|{ask}",
        "copain|Pas là-dedans.",
        f"narrateur|{extra}",
        "enfant-f|Le défilé passe ici, tout près.",
        "papa|Les feuilles restent trop basses.",
        "maman|Tu fais quoi, alors ?",
        "enfant-f|J'écoute, d'abord.",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La flaque tient encore Raphaël.",
            "papa|Le bord, la feuille, ou les bottes ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La terre colle encore à ses doigts.",
            "maman|Le godet, la terre, ou le robinet ?",
        )
    return L(
        "narrateur|Les feuilles restent trop mouillées.",
        "papa|Le pas, le basilic, ou le torchon ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        pose = {
            1: "Elle pose l'arrosoir hors de la flaque.",
            2: "Elle pose la graine hors de la flaque.",
            3: "Elle pose le tablier hors de la flaque.",
        }[t1]
        return L(
            "enfant-f|D'accord, on reste au bord.",
            f"narrateur|{pose}",
            "copain|Je reste ici, moi.",
            "enfant-f|J'arrose une plante, alors.",
            f"narrateur|{o['wait']}",
            "narrateur|Un seul bec penche, tout doux.",
            "papa|La flaque lui reste, à lui.",
            "maman|Ton arrosoir est resté au sec.",
            "enfant-f|C'est bien, comme ça.",
        )
    if t2 == 1 and t3 == 2:
        near = {
            1: "Le bec rouge pousse la feuille, tout doux.",
            2: "La graine reste au sec, dans la poche.",
            3: "Un pois blanc se penche vers l'eau.",
        }[t1]
        return L(
            "copain|Une feuille bateau, plutôt.",
            "enfant-f|D'accord, on pousse la feuille.",
            f"narrateur|{near}",
            "narrateur|La feuille glisse, toute verte.",
            "copain|Elle va jusqu'au bord !",
            "enfant-f|Après, une plante, tout petit.",
            f"narrateur|{o['use']}",
            "papa|Vous avez fait un bateau, d'abord.",
            "maman|L'arrosoir attend, plus loin.",
        )
    if t2 == 1 and t3 == 3:
        leave = {
            1: "Elle laisse l'arrosoir, tout calme.",
            2: "Elle laisse la graine, tout calme.",
            3: "Elle laisse le tablier, tout calme.",
        }[t1]
        return L(
            "copain|Plus tard, quand les bottes sèchent.",
            "enfant-f|D'accord, plus tard.",
            f"narrateur|{leave}",
            "copain|Je reste encore un peu.",
            "enfant-f|Une plante m'attend, déjà.",
            f"narrateur|{o['wait']}",
            "narrateur|Un seul bec reste au bord.",
            "papa|Les bottes restent dans l'eau.",
            "maman|La flaque n'a plus de défilé.",
        )
    if t2 == 2 and t3 == 1:
        side = {
            1: "L'arrosoir rouge reste à côté du godet.",
            2: "La graine reste à côté du godet.",
            3: "Le tablier à pois reste à côté.",
        }[t1]
        return L(
            "enfant-f|D'accord, tu gardes le godet.",
            "copain|La terre, c'est à moi.",
            f"narrateur|{side}",
            "narrateur|Il presse la terre, tout brun.",
            "enfant-f|J'arrose une plante, à côté.",
            f"narrateur|{o['wait']}",
            "narrateur|Un seul bec penche, tout près.",
            "papa|Le godet est resté à lui.",
            "maman|L'arrosoir est resté à toi.",
        )
    if t2 == 2 and t3 == 2:
        press = {
            1: "Deux paumes collent près de l'arrosoir.",
            2: "Deux paumes collent autour de la graine.",
            3: "Deux paumes collent sur le tablier.",
        }[t1]
        return L(
            "copain|On presse la terre, plutôt.",
            "enfant-f|D'accord, on appuie ensemble.",
            f"narrateur|{press}",
            "narrateur|Un petit mont brun se tient.",
            "copain|C'est un nid de terre !",
            "enfant-f|Puis une plante, tout petit.",
            f"narrateur|{o['use']}",
            "papa|Vous avez pressé, d'abord.",
            "maman|L'eau viendra après, tout calme.",
        )
    if t2 == 2 and t3 == 3:
        wash = {
            1: "L'arrosoir rouge attend près du robinet.",
            2: "La graine attend près du robinet.",
            3: "Le tablier à pois attend, tout brun.",
        }[t1]
        return L(
            "copain|Plus tard, après le robinet.",
            "enfant-f|D'accord, va te laver.",
            f"narrateur|{wash}",
            "narrateur|L'eau du robinet chante, tout près.",
            "copain|Mes doigts sont encore bruns.",
            "enfant-f|Une plante m'attend, déjà.",
            f"narrateur|{o['wait']}",
            "papa|Le robinet chante pour lui.",
            "maman|La table garde encore sa terre.",
        )
    if t2 == 3 and t3 == 1:
        back = {
            1: "L'arrosoir rouge recule d'un pas.",
            2: "La graine recule d'un pas, dans la poche.",
            3: "Le tablier à pois recule d'un pas.",
        }[t1]
        return L(
            "enfant-f|D'accord, on reste dehors.",
            "copain|Les feuilles, j'aime pas.",
            f"narrateur|{back}",
            "narrateur|Ils reculent d'un pas, tout doux.",
            "enfant-f|J'arrose une plante, d'ici.",
            f"narrateur|{o['wait']}",
            "narrateur|Un seul bec penche, de loin.",
            "papa|Le bac lui reste trop mouillé.",
            "maman|Ton arrosoir n'est pas entré.",
        )
    if t2 == 3 and t3 == 2:
        smell = {
            1: "Le bec rouge s'arrête près du basilic.",
            2: "La graine sent le basilic, déjà.",
            3: "Un pois blanc frôle le basilic.",
        }[t1]
        return L(
            "copain|Le basilic, plutôt, il sent bon.",
            "enfant-f|D'accord, on sent, d'abord.",
            f"narrateur|{smell}",
            "narrateur|Une feuille de basilic, tout près.",
            "copain|Ça pique le nez, un peu.",
            "enfant-f|Puis une plante, tout petit.",
            f"narrateur|{o['use']}",
            "papa|Vous avez senti, d'abord.",
            "maman|Les feuilles restent derrière, mouillées.",
        )
    wipe = {
        1: "L'arrosoir rouge attend pendant le torchon.",
        2: "La graine attend pendant le torchon.",
        3: "Le tablier à pois attend, tout mouillé.",
    }[t1]
    return L(
        "copain|Plus tard, après le torchon.",
        "enfant-f|D'accord, essuie-toi.",
        f"narrateur|{wipe}",
        "narrateur|Maman tend le torchon, tout doux.",
        "copain|Mon nez n'est plus mouillé.",
        "enfant-f|Une plante m'attend, déjà.",
        f"narrateur|{o['wait']}",
        "papa|Son nez est sec, maintenant.",
        "maman|Les feuilles n'ont plus collé.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        last = {
            1: "Une goutte reste au bord de la flaque.",
            2: "Un peu de terre sèche au bord, déjà.",
            3: "Un pois blanc sèche au bord, déjà.",
        }[t1]
        return L(
            "narrateur|Un seul arrosoir, une seule plante.",
            "enfant-f|Le défilé n'est pas venu.",
            "copain|La flaque m'a gardé.",
            "papa|On rentre, les bottes sont lourdes.",
            "maman|Ça sent encore le basilic, dehors.",
            f"narrateur|{coda}",
            "enfant-f|La plante a bu, tout petit.",
            f"narrateur|{last}",
        )
    if t2 == 1 and t3 == 2:
        last = {
            1: "La feuille bateau sèche contre le bec.",
            2: "La feuille bateau sèche contre la poche.",
            3: "La feuille bateau sèche contre un pois.",
        }[t1]
        return L(
            "narrateur|Après le bateau, un seul arrosoir penche.",
            "copain|La feuille est arrivée au bord.",
            "enfant-f|Puis on a arrosé une plante.",
            "papa|Vous avez soufflé, d'abord.",
            "maman|La serre reste tiède, tout gris.",
            f"narrateur|{coda}",
            "enfant-f|On rentre, les pieds mouillés.",
            f"narrateur|{last}",
        )
    if t2 == 1 and t3 == 3:
        last = {
            1: "L'arrosoir rouge sèche près des bottes.",
            2: "La poche sèche près des bottes.",
            3: "Le tablier sèche près des bottes.",
        }[t1]
        return L(
            "narrateur|Plus tard n'est pas encore là.",
            "copain|Mes bottes sèchent encore.",
            "enfant-f|Une plante a bu, déjà.",
            "papa|On rentre, sans le défilé.",
            "maman|La flaque reste, toute ronde.",
            f"narrateur|{coda}",
            "enfant-f|Raphaël viendra, une autre fois.",
            f"narrateur|{last}",
        )
    if t2 == 2 and t3 == 1:
        last = {
            1: "Un peu de terre brune tache le bec.",
            2: "Un peu de terre brune tache la poche.",
            3: "Un peu de terre brune tache un pois.",
        }[t1]
        return L(
            "narrateur|Un seul arrosoir, une seule plante.",
            "copain|Mon godet est resté à moi.",
            "enfant-f|J'ai arrosé à côté, tout calme.",
            "papa|On rentre, les mains brunes.",
            "maman|La table garde encore sa terre.",
            f"narrateur|{coda}",
            "enfant-f|Le godet et l'arrosoir se parlent.",
            f"narrateur|{last}",
        )
    if t2 == 2 and t3 == 2:
        last = {
            1: "Le nid de terre garde une goutte.",
            2: "Le nid de terre garde la graine.",
            3: "Le nid de terre tache un pois.",
        }[t1]
        return L(
            "narrateur|Après le nid, un seul arrosoir penche.",
            "copain|On a pressé, d'abord.",
            "enfant-f|Puis une plante a bu.",
            "papa|Vos paumes sentent encore la terre.",
            "maman|On rentre, tout brun, tout calme.",
            f"narrateur|{coda}",
            "enfant-f|Le nid reste sur la table.",
            f"narrateur|{last}",
        )
    if t2 == 2 and t3 == 3:
        last = {
            1: "Une goutte du robinet sèche au bec.",
            2: "Une goutte du robinet sèche à la poche.",
            3: "Une goutte du robinet sèche sur un pois.",
        }[t1]
        return L(
            "narrateur|Plus tard n'est pas encore là.",
            "copain|Mes doigts sont encore bruns.",
            "enfant-f|Une plante a bu, déjà.",
            "papa|On rentre, le robinet se tait.",
            "maman|La terre reste sur la table.",
            f"narrateur|{coda}",
            "enfant-f|Raphaël lavera, une autre fois.",
            f"narrateur|{last}",
        )
    if t2 == 3 and t3 == 1:
        last = {
            1: "Une feuille mouillée sèche sur le bec.",
            2: "Une feuille mouillée sèche sur la poche.",
            3: "Une feuille mouillée sèche sur un pois.",
        }[t1]
        return L(
            "narrateur|Un seul arrosoir, une seule plante.",
            "copain|Je suis resté dehors, moi.",
            "enfant-f|J'ai arrosé de loin, tout doux.",
            "papa|On rentre, les visages secs.",
            "maman|Le bac reste trop mouillé, derrière.",
            f"narrateur|{coda}",
            "enfant-f|Les feuilles n'ont pas tapé.",
            f"narrateur|{last}",
        )
    if t2 == 3 and t3 == 2:
        last = {
            1: "Une feuille de basilic colle au bec.",
            2: "Une feuille de basilic colle à la poche.",
            3: "Une feuille de basilic colle à un pois.",
        }[t1]
        return L(
            "narrateur|Après le basilic, un seul arrosoir penche.",
            "copain|Ça piquait le nez, encore.",
            "enfant-f|Puis une plante a bu.",
            "papa|Vos manches sentent encore le vert.",
            "maman|On rentre, ça sent le basilic.",
            f"narrateur|{coda}",
            "enfant-f|Les feuilles restent derrière, mouillées.",
            f"narrateur|{last}",
        )
    last = {
        1: "Le torchon sèche encore contre le bec.",
        2: "Le torchon sèche encore contre la poche.",
        3: "Le torchon sèche encore contre un pois.",
    }[t1]
    return L(
        "narrateur|Plus tard n'est pas encore là.",
        "copain|Mon nez est sec, maintenant.",
        "enfant-f|Une plante a bu, déjà.",
        "papa|On rentre, le torchon sous le bras.",
        "maman|Les vitres restent embuées, tout gris.",
        f"narrateur|{coda}",
        "enfant-f|Raphaël essuiera, une autre fois.",
        f"narrateur|{last}",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Derrière la maison, la pluie vient de finir.",
        "narrateur|La serre garde encore toute l'eau.",
        "narrateur|Les vitres sont embuées, tout gris.",
        "papa|Ça sent le basilic, tu le sens ?",
        "enfant-f|Oui, et la terre mouillée.",
        "maman|Une goutte glisse à l'intérieur.",
        "narrateur|En ce moment, Chouchou frotte une vitre.",
        "enfant-f|Je veux un défilé d'arrosoirs.",
        "papa|Pour Raphaël, tout le long des planches ?",
        "enfant-f|Oui, il arrose avec moi.",
        "maman|L'arrosoir rouge est près de la porte.",
        "papa|Merci, tu as essuyé la vitre.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près de la porte, trois affaires attendent.",
        "narrateur|L'arrosoir, la graine, ou le tablier.",
        "papa|Par quoi tu commences, Chouchou ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("l'arrosoir rouge", "la graine", "le tablier à pois")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("l'allée", "la table", "le bac")

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
        "Serre derrière la maison, après la pluie : vitres embuées, terre mouillée, "
        "odeur de basilic. Chouchou veut un défilé d'arrosoirs le long des planches, "
        "pour Raphaël. T1 = arrosoir rouge / graine de basilic / tablier à pois "
        "(les trois partent, le premier change le voyage). "
        "T2 = allée (flaque) / table à rempoter (terre qui colle) / bac à tomates "
        "(feuilles mouillées au visage). "
        "T3 = neuf résolutions : bord (accepter le non), feuille bateau (autre chose), "
        "bottes (plus tard) ; godet (accepter le non), nid de terre (autre chose), "
        "robinet (plus tard) ; pas en reculant (accepter le non), basilic (autre chose), "
        "torchon (plus tard). La leçon se vit : elle propose, elle accepte oui, non, "
        "ou une autre idée, elle n'insiste pas. Fin : un seul arrosoir, une seule plante, "
        "on rentre.",
        "N1 ≤ 10. Jules, pommier et slogan « Inviter sans forcer » jetés. "
        "Autre récit que DIF-008 (stand), DIF-018 (biscuits jardin), DIF-031 "
        "(panier potager), DIF-035 (poupées), DIF-049 (poissons papier). "
        "Un merci de papa lié au geste (essuyer la vitre). chunk_id inchangés. "
        "check() OK. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
