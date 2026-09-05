#!/usr/bin/env python3
"""TREE-DIF-068 — Le portrait de Victorina, sur le palier (N3, DIF.COR.003)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-068"
N3 = 16
TITLE = "Le portrait de Victorina, sur le palier"
FIL = (
    "Sur le palier, Victorina veut accrocher le portrait de famille au clou, "
    "avant que Mila parte. Elle prend d'abord le cadre, le chiffon de cire "
    "ou le petit tabouret ; les trois viennent. Sous la fenêtre ronde le soleil "
    "pique les lunettes, contre la rampe les cheveux vont dans la bouche, "
    "près de la porte la manche trop longue cache le clou. Neuf façons. "
    "Le portrait tient. On descend."
)
CHARS = "Victorina, Mila, papa, maman"
SETTING = "le palier : fenêtre ronde, rampe, porte des chambres, odeur de cire"


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
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "pas rire",
        "apparence",
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
        "lunettes, cheveux",
        "lunettes, cheveux, habit",
        "cabane",
        "drap à pois",
        "cacao",
        "étagère",
        "coquillage",
        "phare",
        "jetée",
        "manteau à pois",
        "escargot",
        "ciré",
        "marée",
        "il faut attendre",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorina" not in blob:
        raise SystemExit(f"{SID}: Victorina absente")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "palier" not in blob:
        raise SystemExit(f"{SID}: palier absent")
    if "portrait" not in blob:
        raise SystemExit(f"{SID}: portrait absent")
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
        "lab": "le cadre",
        "ans": "cadre",
        "acc": "cadre | le cadre | d'abord le cadre | le bois",
        "retry": "Victorina prend le cadre d'abord.",
        "coda": "Le cadre reste droit, un grain de cire au coin.",
        "hip": "Entre ses doigts, le bois du cadre est tiède.",
        "wait": "Pendant ce temps, le cadre reste droit, sans bouger.",
        "use": "Le verre du cadre cherche encore le clou.",
    },
    2: {
        "lab": "le chiffon",
        "ans": "chiffon",
        "acc": "chiffon | le chiffon | d'abord le chiffon | la cire",
        "retry": "Victorina prend le chiffon d'abord.",
        "coda": "Le chiffon reste plié, une odeur de cire encore.",
        "hip": "Dans sa paume, le chiffon de cire est gras.",
        "wait": "Plié, le chiffon attend contre son pouce.",
        "use": "Une odeur de cire brille, prête à lustrer.",
    },
    3: {
        "lab": "le tabouret",
        "ans": "tabouret",
        "acc": "tabouret | le tabouret | d'abord le tabouret | le petit",
        "retry": "Victorina prend le tabouret d'abord.",
        "coda": "Le tabouret reste bas, un rond de cire dessus.",
        "hip": "Contre son genou, le petit tabouret reste bien plat.",
        "wait": "Plat, le tabouret attend, sans glisser.",
        "use": "Le bois du tabouret attend, tout calme.",
    },
}

T3_LABS = {
    1: ("les lunettes", "Mila tient", "le nuage"),
    2: ("le nœud", "l'oreille", "Mila souffle"),
    3: ("la manche", "le bouton", "le clou"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorina prend d'abord le cadre en bois.",
            "enfant-f|Il sent encore la cire.",
            "papa|Le verre est propre, maintenant.",
            "narrateur|Mila pose une main sous le bas.",
            "copine|Je le porte avec toi.",
            "maman|Le chiffon et le tabouret viennent aussi.",
            "narrateur|Papa glisse le chiffon contre le cadre.",
            "narrateur|Le petit tabouret suit, tout près des pieds.",
            "enfant-f|On a tout, Mila.",
            "copine|On va jusqu'au clou.",
            "papa|Le cadre d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorina prend d'abord le chiffon de cire.",
            "enfant-f|Il sent le bois chaud.",
            "maman|Un peu, pas tout le pot.",
            "narrateur|Le chiffon brille, encore gras, entre ses doigts.",
            "papa|Le cadre et le tabouret viennent aussi.",
            "narrateur|Mila glisse le cadre contre son ventre.",
            "narrateur|Le petit tabouret tape une marche, tout doux.",
            "copine|Le palier sent la cire, partout.",
            "enfant-f|On a tout, maintenant.",
            "papa|Le chiffon d'abord, vous l'avez.",
        )
    return L(
        "narrateur|Victorina tire d'abord le petit tabouret.",
        "enfant-f|Il va me porter, près du clou.",
        "papa|Deux pieds, bien à plat.",
        "narrateur|Le bois du tabouret racle le palier, tout bas.",
        "maman|Le cadre et le chiffon viennent aussi.",
        "narrateur|Mila pose le cadre contre le tabouret.",
        "narrateur|Le chiffon reste sur le bois, tout plat.",
        "copine|On monte tous, alors.",
        "enfant-f|Le clou m'attend.",
        "papa|Le tabouret d'abord, il est à toi.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|Le cadre reste contre elle, encore tiède.",
            "enfant-f|On va jusqu'au clou.",
            "copine|Je tiens le bas, moi.",
            "maman|Mila n'a plus beaucoup de temps.",
            "papa|Tu tiens bien, Victorina ?",
            "enfant-f|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|Le chiffon pend à son poignet, un peu gras.",
            "enfant-f|Il va lustrer le verre.",
            "copine|Ça sent encore le bois chaud.",
            "papa|Tes mains sont prêtes ?",
            "enfant-f|Oui.",
            "narrateur|Une goutte de cire se tait, puis plus rien.",
        )
    return L(
        "narrateur|Le petit tabouret reste collé à ses genoux.",
        "enfant-f|Je vais monter, tout près.",
        "copine|Je le pousse, moi.",
        "maman|On avance, toutes les deux ?",
        "enfant-f|Oui, maman.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le cadre penche vers le clou, déjà.",
        2: "Le chiffon colle encore à sa manche.",
        3: "Le tabouret appuie contre son genou.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Devant, le soleil pique trop, dans les lunettes.",
        "narrateur|La rampe, elle, prend les cheveux dans la bouche.",
        "narrateur|Près de la porte, la manche trop longue cache le clou.",
        "papa|Victorina, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le verre du cadre devient trop blanc.",
            2: "Le chiffon tombe, trop ébloui, trop vite.",
            3: "Le tabouret penche, trop dans le soleil.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Le rond de soleil tape trop fort, dans les lunettes.",
            f"narrateur|{extra}",
            "enfant-f|Je ne vois plus le clou !",
            "narrateur|Les lunettes glissent, trop chaudes, trop basses.",
            "copine|Tes verres sont tout blancs.",
            "papa|Ici, ça pique trop.",
            "maman|Le clou se cache dans la lumière.",
            "enfant-f|Alors on fait quoi ?",
            "papa|Tu vois comment, Victorina ?",
        )
    if t2 == 2:
        extra = {
            1: "Le cadre penche, trop tenu d'une main.",
            2: "Le chiffon se coince dans les cheveux.",
            3: "Le tabouret avance, trop près de la rampe.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Victorina se penche contre la rampe, trop près.",
            f"narrateur|{extra}",
            "enfant-f|Mes cheveux vont dans ma bouche !",
            "narrateur|Une mèche colle, trop longue, trop sèche.",
            "copine|Tu parles avec les cheveux.",
            "papa|Ici, ça gêne trop.",
            "maman|Le clou attend, plus haut.",
            "enfant-f|Alors on fait quoi ?",
            "maman|Tu vois comment, Victorina ?",
        )
    extra = {
        1: "Le cadre bute contre la manche trop large.",
        2: "Le chiffon disparaît dans le tissu.",
        3: "Le tabouret reste coincé sous la manche.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Le manteau trop grand laisse la manche trop longue.",
        f"narrateur|{extra}",
        "enfant-f|Je n'attrape plus rien !",
        "narrateur|Le tissu glisse sur le bois, trop large.",
        "copine|Ta manche mange ta main.",
        "papa|Ici, ça cache trop.",
        "maman|Le clou est derrière le tissu.",
        "enfant-f|Alors on fait quoi ?",
        "papa|Tu vois comment, Victorina ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le soleil n'a pas fini de piquer.",
            "papa|Les lunettes, Mila tient, ou le nuage ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les cheveux n'ont pas fini de coller.",
            "maman|Le nœud, l'oreille, ou Mila souffle ?",
        )
    return L(
        "narrateur|La manche n'a pas fini de cacher.",
        "papa|La manche, le bouton, ou le clou ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-f|Je relève les lunettes.",
            "narrateur|Elle pousse les verres, tout haut, sur le nez.",
            "narrateur|Le clou redevient un petit point, net.",
            "copine|Je vois le clou, moi aussi.",
            f"narrateur|{o['wait']}",
            "papa|Tes lunettes tiennent, maintenant.",
            "enfant-f|Le cadre peut monter.",
            "maman|Tu as relevé, tout doux.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-f|Mila, tu tiens le cadre.",
            "narrateur|Mila ouvre les deux mains, tout près du verre.",
            "narrateur|Victorina relève les lunettes, sans le poids.",
            "copine|Je le garde, droit.",
            f"narrateur|{o['use']}",
            "papa|Tes mains ont laissé le cadre.",
            "enfant-f|Je vois le clou, enfin.",
            "maman|Mila a tenu, tout calme.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-f|On attend le nuage.",
            "narrateur|Un nuage passe sur la fenêtre ronde, tout lent.",
            "narrateur|Le rond de soleil s'en va, puis les lunettes se taisent.",
            "copine|C'est plus doux, là.",
            f"narrateur|{o['wait']}",
            "papa|Le nuage vous a aidées.",
            "enfant-f|Le clou est là.",
            "maman|Tu as laissé la lumière finir.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-f|On noue les cheveux.",
            "narrateur|Victorina rassemble les mèches, tout haut.",
            "narrateur|Mila tient le nœud, un instant.",
            "copine|Il tient, maintenant.",
            f"narrateur|{o['wait']}",
            "papa|Tes cheveux restent derrière.",
            "enfant-f|Je peux parler, et tenir.",
            "maman|Tu as noué, tout serré.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-f|Derrière l'oreille, d'abord.",
            "narrateur|Elle glisse la mèche, loin de la bouche.",
            "narrateur|L'oreille garde les cheveux, tout calme.",
            "copine|Tu n'as plus de cheveux, là.",
            f"narrateur|{o['use']}",
            "papa|L'oreille a suffi.",
            "enfant-f|Le cadre ne tremble plus.",
            "maman|Tu as glissé la mèche.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-f|Mila, souffle un peu.",
            "narrateur|Mila souffle, tout doux, sur la mèche.",
            "narrateur|Les cheveux quittent la bouche, puis restent.",
            "copine|Ils sont partis.",
            f"narrateur|{o['wait']}",
            "papa|Mila a soufflé, tout près.",
            "enfant-f|Je tiens le cadre, des deux mains.",
            "maman|La mèche n'est plus dans le chemin.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-f|Je retrousse la manche.",
            "narrateur|Elle plie le tissu, deux fois, jusqu'au coude.",
            "narrateur|La main redevient petite, nette, près du clou.",
            "copine|Ta main est sortie.",
            f"narrateur|{o['wait']}",
            "papa|La manche reste en haut.",
            "enfant-f|J'attrape le clou, maintenant.",
            "maman|Tu as retroussé, tout court.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-f|Le bouton, d'abord.",
            "narrateur|Elle passe le bouton dans la fente, tout lent.",
            "narrateur|La manche reste courte, collée au poignet.",
            "copine|Elle ne retombe plus.",
            f"narrateur|{o['use']}",
            "papa|Le bouton a tenu le tissu.",
            "enfant-f|Ma main est libre.",
            "maman|Tu as fermé, tout près du poignet.",
        )
    return L(
        "enfant-f|Papa, tu poses le clou.",
        "narrateur|Papa pose le clou, à leur hauteur, tout calme.",
        "narrateur|Victorina tient le cadre, la manche retroussée.",
        "copine|Je pousse le bas, moi.",
        f"narrateur|{o['wait']}",
        "papa|Le clou est prêt, maintenant.",
        "enfant-f|On accroche.",
        "maman|Vous avez laissé la manche, plus haut.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le portrait se pose, droit, sur le clou du palier.",
            "enfant-f|On a relevé les lunettes.",
            "papa|Tes verres ont laissé le clou.",
            "maman|Mila peut descendre, maintenant.",
            f"narrateur|{coda}",
            "narrateur|Un rond de soleil reste sur le verre, puis glisse.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Mila lâche le cadre, déjà accroché.",
            "enfant-f|Tu as tenu, Mila.",
            "papa|Tes mains ont laissé le portrait.",
            "maman|Le palier sent encore la cire.",
            f"narrateur|{coda}",
            "narrateur|On descend, une marche après l'autre.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Quand le nuage a passé, le portrait a tenu.",
            "enfant-f|On a attendu la lumière.",
            "papa|Le nuage vous a laissées.",
            "maman|La fenêtre ronde est plus douce, maintenant.",
            f"narrateur|{coda}",
            "narrateur|On descend, le portrait reste en haut.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le portrait tient, les cheveux noués derrière.",
            "enfant-f|On a noué, d'abord.",
            "papa|Tes cheveux n'ont plus gêné.",
            "maman|Le nœud tient encore, tout haut.",
            f"narrateur|{coda}",
            "narrateur|La rampe reste vide, on descend.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Derrière l'oreille, le portrait a trouvé le clou.",
            "enfant-f|La mèche est restée là.",
            "papa|L'oreille a suffi, tout doux.",
            "maman|Vos mains sentent encore la cire.",
            f"narrateur|{coda}",
            "narrateur|On descend, la rampe sous les doigts.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Après le souffle, le portrait tient, tout calme.",
            "enfant-f|Mila a soufflé, d'abord.",
            "papa|La mèche n'est plus dans le chemin.",
            "maman|Le palier redevient un palier.",
            f"narrateur|{coda}",
            "narrateur|On descend, sans les cheveux dans la bouche.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|La manche retroussée, le portrait accroche, déjà.",
            "enfant-f|Ma main a trouvé le clou.",
            "papa|La manche est restée en haut.",
            "maman|Essuie tes manches, on descend.",
            f"narrateur|{coda}",
            "narrateur|La porte des chambres se tait, derrière.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le bouton a tenu, le portrait aussi.",
            "enfant-f|Ma main était libre.",
            "papa|Le tissu n'a plus caché le clou.",
            "maman|Le bouton reste fermé, encore.",
            f"narrateur|{coda}",
            "narrateur|On descend, la manche courte, le portrait haut.",
        )
    return L(
        "narrateur|Papa a posé le clou, le portrait tient.",
        "enfant-f|On a accroché, toutes les deux.",
        "papa|Le clou était à votre hauteur.",
        "maman|Mila, tu peux partir, maintenant.",
        f"narrateur|{coda}",
        "narrateur|On descend, le portrait reste au palier.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Sur le palier, la cire sent encore le bois chaud.",
        "narrateur|Une fenêtre ronde pose un rond de soleil au mur.",
        "narrateur|Un reflet passe sur les lunettes de Victorina.",
        "narrateur|Le portrait de famille penche contre la rampe, trop bas.",
        "papa|Tu as vu le clou, Victorina ?",
        "enfant-f|Il est trop haut, encore.",
        "maman|Mila va partir, bientôt.",
        "narrateur|En ce moment, Victorina touche le cadre, tout près.",
        "enfant-f|Je veux l'accrocher, avant qu'elle parte.",
        "copine|Je reste un peu, alors.",
        "papa|Merci, tu as essuyé le verre, déjà.",
        "maman|Le tabouret attend, près des chambres.",
        "narrateur|Une marche craque, plus bas, puis plus rien.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent au haut de l'escalier.",
        "narrateur|Un cadre en bois, un chiffon de cire, un petit tabouret.",
        "maman|Par quoi tu commences, Victorina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le cadre", "le chiffon", "le tabouret")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Victorina a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la fenêtre", "la rampe", "la porte")

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
        "Palier au haut de l'escalier, fenêtre ronde, odeur de cire, cadre trop bas. "
        "Victorina veut accrocher le portrait de famille au clou, avant que Mila parte. "
        "T1 = cadre / chiffon de cire / petit tabouret (les trois viennent). "
        "T2 = fenêtre (soleil dans les lunettes) / rampe (cheveux dans la bouche) / "
        "porte des chambres (manche trop longue). "
        "T3 = neuf résolutions (relever les lunettes, Mila tient, nuage ; "
        "nœud, oreille, Mila souffle ; retrousser, bouton, papa pose le clou). "
        "La leçon se vit : lunettes, cheveux, manche gênent le geste, on les arrange. "
        "Fin : le portrait tient, on descend.",
        "N3 ≤ 16. Slogan « Lunettes, cheveux, habit — à la maison », Kenzo, "
        "Tom/Léa/Sami, bac/toboggan, « pas rire », « apparence » jetés. "
        "Récit autre que DIF-032 (cabane/drap), DIF-042 (cacao/étagère), "
        "DIF-003 (manteau pois/lunettes de Mila), DIF-052 (lunettes de mer). "
        "Merci de papa (verre essuyé). chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-068.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
