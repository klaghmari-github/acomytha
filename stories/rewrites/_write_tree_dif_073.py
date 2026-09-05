#!/usr/bin/env python3
"""TREE-DIF-073 — La marguerite de Raphaël, à l'étal (N1, DIF.BES.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-073"
N1 = LIMITS["N1"]
TITLE = "La marguerite de Raphaël, à l'étal"
FIL = (
    "Sous la bâche, Raphaël veut offrir une marguerite à Nina. "
    "Il prend d'abord la marguerite, le petit seau ou le papier ; "
    "les trois viennent. Devant les roses, Nina recule. "
    "Près des seaux du bord, l'eau clabousse. Au bout de la bâche, "
    "elle choisit autre chose. Neuf façons de tendre, d'entendre non, "
    "ou de prendre sa fleur. Une tige reste dans sa main. On rentre."
)
CHARS = "Raphaël, Nina, papa, maman"
SETTING = "étal de fleurs du marché : seaux, tiges, abeille, bâche"


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
        "léa",
        "lea ",
        "kenzo",
        "moulinet",
        "le four",
        "pain",
        "wagon",
        "la mer",
        "la serre",
        "arrosoir",
        "le tapis",
        "poisson",
        "canapé",
        "le store",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
        "fort de coussins",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob or "nina" not in blob:
        raise SystemExit(f"{SID}: troupe Raphaël/Nina absente")
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
        "lab": "la marguerite",
        "ans": "marguerite",
        "acc": "marguerite | la marguerite | d'abord la marguerite | la fleur blanche",
        "retry": "Raphaël a pris la marguerite.",
        "coda": "Une goutte sèche encore sur le blanc.",
        "hip": "La tige blanche reste un peu mouillée.",
        "use": "Le cœur jaune tremble, tout petit.",
    },
    2: {
        "lab": "le petit seau",
        "ans": "seau",
        "acc": "seau | le seau | le petit seau | d'abord le seau",
        "retry": "Raphaël a pris le petit seau.",
        "coda": "Le petit seau garde une tige, tout calme.",
        "hip": "Le petit seau cloche encore un peu.",
        "use": "Une goutte pend encore au bord.",
    },
    3: {
        "lab": "le papier",
        "ans": "papier",
        "acc": "papier | le papier | d'abord le papier | l'enveloppe",
        "retry": "Raphaël a pris le papier.",
        "coda": "Le papier tient encore un peu d'eau.",
        "hip": "Le papier craque contre son poignet.",
        "use": "Un coin blanc dépasse, déjà.",
    },
}

T3_LABS = {
    1: ("deux pas", "le bord", "la tulipe"),
    2: ("après l'eau", "le pas de côté", "le bleu"),
    3: ("sous la bâche", "l'autre tige", "le tournesol"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Raphaël prend d'abord la marguerite.",
            "enfant-m|Elle a un cœur jaune.",
            "maman|Tiens-la par la tige.",
            "narrateur|Une goutte glisse sur le blanc.",
            "papa|Le seau et le papier aussi.",
            "narrateur|Il tient les trois contre lui.",
            "narrateur|Rien ne reste dans l'eau.",
            "enfant-m|Nina, je te la tends.",
            "papa|Tu lui proposes, tout calme ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Raphaël prend d'abord le petit seau.",
            "enfant-m|L'eau tremble un peu.",
            "papa|Pas trop plein, tout doux.",
            "narrateur|Une goutte clabousse sur la pierre.",
            "maman|La marguerite et le papier aussi.",
            "narrateur|Il pose les trois près de Nina.",
            "narrateur|Le zinc sent encore les tiges.",
            "enfant-m|Nina, je te tends ça.",
            "maman|Tu lui proposes, tout calme ?",
            "enfant-m|Oui, maman.",
        )
    return L(
        "narrateur|Raphaël prend d'abord le papier.",
        "enfant-m|Il craque un peu.",
        "maman|Enroule-le sans trop serrer.",
        "narrateur|Le papier sent encore le bois.",
        "papa|La marguerite et le seau aussi.",
        "narrateur|Il porte les trois sous la bâche.",
        "narrateur|Un coin blanc dépasse, déjà.",
        "enfant-m|Nina, je t'enveloppe ça.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-m|Oui.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Raphaël tient le blanc, déjà.",
            "maman|Il a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le petit seau est dans ses mains.",
            "papa|Il a pris quoi, d'abord ?",
        )
    return L(
        "narrateur|Le papier craque encore.",
        "maman|Il a pris quoi, d'abord ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|La marguerite.",
            "maman|Oui.",
            "narrateur|Le cœur jaune reste un peu mouillé.",
            "narrateur|Le papier attend contre son poignet.",
            "enfant-m|Nina est devant l'étal.",
            "papa|Je la vois, tout près.",
            "maman|Vous allez lui tendre ça.",
            "enfant-m|Je lui tends la tige.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Le seau.",
            "papa|Oui.",
            "narrateur|Une goutte pend encore au bord.",
            "narrateur|La marguerite voyage contre le zinc.",
            "enfant-m|Nina est devant l'étal.",
            "maman|Je la vois, tout près.",
            "papa|Le seau tient bien, maintenant.",
            "enfant-m|Je lui tends ça, après.",
        )
    return L(
        "enfant-m|Le papier.",
        "maman|Oui.",
        "narrateur|Un coin blanc dépasse, déjà.",
        "narrateur|La marguerite glisse dans le pli.",
        "enfant-m|Nina est devant l'étal.",
        "papa|Je la vois, tout près.",
        "maman|Le papier est prêt, maintenant.",
        "enfant-m|Je l'enveloppe pour elle.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "La marguerite penche déjà vers Nina.",
        2: "Le petit seau penche déjà vers Nina.",
        3: "Le papier penche déjà vers Nina.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Nina est déjà devant l'étal.",
        "narrateur|Les roses ont des épines, là.",
        "narrateur|Les seaux du bord claboussent.",
        "narrateur|Le bout de la bâche fait de l'ombre.",
        "papa|On va vers où, Raphaël ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        offer = {
            1: "Nina, cette marguerite est pour toi.",
            2: "Nina, je te tends la fleur.",
            3: "Nina, je t'enveloppe ça.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Une épine brille, trop près des roses.",
            f"enfant-m|{offer}",
            "copine|Les épines, non.",
            "narrateur|Nina recule d'un pas, déjà.",
            f"narrateur|{o['use']}",
            "papa|Elle a reculé, tout calme.",
            "maman|Tu as vu son pas ?",
            "enfant-m|Alors on fait quoi ?",
        )
    if t2 == 2:
        offer = {
            1: "Nina, je te tends la fleur.",
            2: "Nina, le seau est là.",
            3: "Nina, le papier est prêt.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|L'eau clabousse sur la pierre.",
            f"enfant-m|{offer}",
            "copine|Mes pieds, l'eau.",
            "narrateur|Une goutte saute sur sa chaussure.",
            "narrateur|Nina recule, les orteils mouillés.",
            "papa|Ici, ça clabousse trop.",
            "maman|Tu as vu ses pieds ?",
            "enfant-m|Alors on fait quoi ?",
        )
    offer = {
        1: "Nina, la marguerite est pour toi.",
        2: "Nina, je te tends ça.",
        3: "Nina, je t'enveloppe ça.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|L'ombre est fraîche, tout calme.",
        f"enfant-m|{offer}",
        "copine|Une autre, plutôt.",
        "narrateur|Nina pointe une autre tige, déjà.",
        f"narrateur|{o['use']}",
        "papa|Elle a choisi autre chose.",
        "maman|Tu as entendu sa voix ?",
        "enfant-m|Alors on fait quoi ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Les roses n'ont pas fini d'épiner.",
            "papa|Deux pas, le bord, ou la tulipe ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les seaux n'ont pas fini de clabousser.",
            "maman|Après l'eau, le pas, ou le bleu ?",
        )
    return L(
        "narrateur|La bâche n'a pas fini son ombre.",
        "papa|Sous la bâche, l'autre tige, ou le tournesol ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        far = {
            1: "Il recule, la marguerite encore tendue.",
            2: "Il recule, le seau contre la hanche.",
            3: "Il recule, le papier encore ouvert.",
        }[t1]
        return L(
            "enfant-m|Deux pas, plus loin des épines.",
            f"narrateur|{far}",
            "narrateur|Nina ne recule plus, maintenant.",
            "copine|Là, je vois le blanc.",
            "enfant-m|Elle est pour toi, alors ?",
            "copine|Oui, tout doux.",
            f"narrateur|{o['use']}",
            "papa|Tu as tendu de plus loin.",
            "maman|Elle a dit oui, toute seule.",
        )
    if t2 == 1 and t3 == 2:
        edge = {
            1: "Il baisse la marguerite, tout calme.",
            2: "Il pose le seau au bord, tout calme.",
            3: "Il plie le papier, tout calme.",
        }[t1]
        return L(
            "enfant-m|On reste au bord, d'accord.",
            "copine|Oui, loin des épines.",
            f"narrateur|{edge}",
            "narrateur|Nina respire, les épaules plus basses.",
            "copine|Pas celle-là, Raphaël.",
            "enfant-m|D'accord.",
            f"narrateur|{o['hip']}",
            "papa|Tu as gardé son recul.",
            "maman|Le bord n'a pas d'épines.",
        )
    if t2 == 1 and t3 == 3:
        tulip = {
            1: "Il pose la marguerite, tout doux.",
            2: "Il pose le seau, tout doux.",
            3: "Il pose le papier, tout doux.",
        }[t1]
        return L(
            "copine|La tulipe, plutôt.",
            "enfant-m|D'accord, la tulipe.",
            f"narrateur|{tulip}",
            "narrateur|La tulipe a une tige lisse.",
            "copine|Celle-là, oui.",
            "enfant-m|Je te la tends.",
            f"narrateur|{o['use']}",
            "papa|Tu as pris sa fleur.",
            "maman|La tulipe n'a pas d'épine, ici.",
        )
    if t2 == 2 and t3 == 1:
        wait = {
            1: "La marguerite attend, sans bouger.",
            2: "Le petit seau attend, sans bouger.",
            3: "Le papier attend, sans bouger.",
        }[t1]
        return L(
            "enfant-m|Après l'eau, je te la tends.",
            f"narrateur|{wait}",
            "narrateur|Le seau du bord se calme, enfin.",
            "copine|Mes pieds sont secs, maintenant.",
            "enfant-m|La marguerite, alors ?",
            "copine|Oui, tout doux.",
            f"narrateur|{o['use']}",
            "papa|Tu as tendu après l'eau.",
            "maman|Elle a dit oui, pieds secs.",
        )
    if t2 == 2 and t3 == 2:
        side = {
            1: "Il ne tend plus, tout de suite.",
            2: "Le seau reste à l'écart, déjà.",
            3: "Le papier reste plié, déjà.",
        }[t1]
        return L(
            "enfant-m|Un pas de côté, alors.",
            "copine|Oui, loin de l'eau.",
            f"narrateur|{side}",
            "narrateur|Nina essuie sa chaussure, tout calme.",
            "copine|Pas maintenant, Raphaël.",
            "enfant-m|D'accord.",
            f"narrateur|{o['hip']}",
            "papa|Tu as gardé ses pieds secs.",
            "maman|Le pas de côté a suffi.",
        )
    if t2 == 2 and t3 == 3:
        blue = {
            1: "Il pose la marguerite près du seau.",
            2: "Il pose le petit seau plus loin.",
            3: "Il pose le papier près du zinc.",
        }[t1]
        return L(
            "copine|Le bleu, là-bas.",
            "enfant-m|D'accord, le bleu.",
            f"narrateur|{blue}",
            "narrateur|Une fleur bleue a la tige sèche.",
            "copine|Celle-là, loin de l'eau.",
            "enfant-m|Je te la tends.",
            f"narrateur|{o['use']}",
            "papa|Tu as pris sa fleur.",
            "maman|Le bleu n'a pas claboussé.",
        )
    if t2 == 3 and t3 == 1:
        shade = {
            1: "Il tend la marguerite, à l'ombre.",
            2: "Il tend le seau, à l'ombre.",
            3: "Il tend le papier, à l'ombre.",
        }[t1]
        return L(
            "enfant-m|Sous la bâche, encore une fois.",
            f"narrateur|{shade}",
            "narrateur|Nina regarde le blanc, plus longtemps.",
            "copine|Là, le cœur jaune est doux.",
            "enfant-m|Elle est pour toi, alors ?",
            "copine|Oui, tout calme.",
            f"narrateur|{o['use']}",
            "papa|Tu as tendu sous l'ombre.",
            "maman|Elle a dit oui, à l'ombre.",
        )
    if t2 == 3 and t3 == 2:
        other = {
            1: "Il baisse la marguerite, tout doux.",
            2: "Il baisse le seau, tout doux.",
            3: "Il baisse le papier, tout doux.",
        }[t1]
        return L(
            "copine|Une autre tige, Raphaël.",
            "enfant-m|D'accord, pas celle-là.",
            f"narrateur|{other}",
            "narrateur|Nina cherche déjà, sous la bâche.",
            "copine|Celle-ci, plus ronde.",
            "enfant-m|Je te la prends, alors.",
            f"narrateur|{o['hip']}",
            "papa|Tu as entendu son autre voix.",
            "maman|L'autre tige était à elle.",
        )
    sun = {
        1: "Il pose la marguerite, tout calme.",
        2: "Il pose le seau, tout calme.",
        3: "Il pose le papier, tout calme.",
    }[t1]
    return L(
        "copine|Le tournesol, plutôt.",
        "enfant-m|D'accord, le tournesol.",
        f"narrateur|{sun}",
        "narrateur|Le tournesol chauffe encore un peu.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|Je te le tends.",
        f"narrateur|{o['use']}",
        "papa|Tu as pris sa fleur.",
        "maman|Le jaune tient dans sa main.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La marguerite voyage, serrée dans sa main.",
            "copine|Le blanc est à moi, maintenant.",
            "enfant-m|Deux pas, et tu as dit oui.",
            "papa|Les épines sont restées loin.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|Une abeille s'éloigne, déjà.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Une petite tige sans épine, déjà.",
            "copine|Celle du bord, je la prends.",
            "enfant-m|Tu as dit non, d'abord.",
            "papa|Son recul a gardé sa place.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|Les épines restent loin, déjà.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La tulipe rose dort dans sa main.",
            "copine|Elle n'a pas piqué.",
            "enfant-m|C'était ta fleur, Nina.",
            "papa|La tige lisse a suffi.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|Un pétale rose suit le pas, tout bas.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|La marguerite voyage, serrée dans sa main.",
            "copine|Mes pieds sont secs, maintenant.",
            "enfant-m|Après l'eau, tu as dit oui.",
            "papa|L'eau s'est tue, d'abord.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|Un seau du bord se tait, derrière.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Une tige sèche reste dans sa main.",
            "copine|Loin de l'eau, celle-là.",
            "enfant-m|Tu as dit pas maintenant.",
            "papa|Ses pieds sont restés secs.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|La pierre de l'étal sèche, enfin.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Le bleu reste contre sa paume chaude.",
            "copine|Il n'a pas claboussé.",
            "enfant-m|C'était ta fleur, Nina.",
            "papa|La tige sèche a suffi.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|Une goutte retombe, plus loin, déjà.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|La marguerite voyage, serrée dans sa main.",
            "copine|Sous la bâche, le blanc est doux.",
            "enfant-m|Tu as dit oui, à l'ombre.",
            "papa|L'ombre a laissé le temps.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|L'ombre de la bâche reste derrière.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La fleur ronde penche vers son pouce.",
            "copine|Celle-ci, plus ronde, c'est la mienne.",
            "enfant-m|Tu as choisi l'autre tige.",
            "papa|Sa voix a dit une autre.",
            "maman|On rentre, la fleur avec vous.",
            coda,
            "narrateur|Un coin de bâche claque, tout loin.",
        )
    return L(
        "narrateur|Le tournesol penche vers son nez.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|Le jaune tient dans sa main.",
        "maman|On rentre, la fleur avec vous.",
        coda,
        "narrateur|Un grain de pollen suit le pas.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La bâche du marché claque, tout doux.",
        "narrateur|Ça sent l'eau des seaux, déjà.",
        "narrateur|Une abeille tourne autour des tiges.",
        "papa|Les pétales tiennent encore des gouttes.",
        "maman|Nina te rejoint, Raphaël.",
        "copine|Je regarde les fleurs, tout calme.",
        "narrateur|En ce moment, Raphaël cherche une marguerite.",
        "enfant-m|Je veux t'en offrir une.",
        "papa|Tu lui proposes, tout doux ?",
        "enfant-m|Oui, papa.",
        "maman|Merci, tu as essuyé tes mains.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois choses attendent, sous la bâche.",
        "narrateur|La marguerite, le seau, le papier.",
        "papa|Par quoi tu commences, Raphaël ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la marguerite", "le petit seau", "le papier")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("les roses", "les seaux", "la bâche")

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
        "Étal de fleurs sous la bâche : seaux d'eau, tiges, abeille, ombre. "
        "Raphaël veut offrir une marguerite à Nina. "
        "T1 = marguerite / petit seau / papier (les trois viennent). "
        "T2 = roses (épines, Nina recule) / seaux du bord (eau qui clabousse) / "
        "bout de la bâche (ombre, Nina choisit autre chose). "
        "T3 = neuf façons : deux pas, le bord, la tulipe ; après l'eau, "
        "le pas de côté, le bleu ; sous la bâche, l'autre tige, le tournesol. "
        "La leçon se vit : il tend, il entend non, il prend sa fleur. "
        "Fin : une fleur dans la main de Nina, on rentre.",
        "N1 ≤ 10. Slogan « Inviter sans forcer — au marché », Léa, "
        "« voici le geste », « bon travail » jetés. "
        "Autre récit que DIF-046 (pas de moulinet), DIF-030 (pas de four), "
        "DIF-041 (pas de pain/mer), DIF-065 (pas de serre), DIF-049 "
        "(pas de salon, pas de poissons). Merci de maman (mains essuyées). "
        "chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-073.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
