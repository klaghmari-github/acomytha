#!/usr/bin/env python3
"""TREE-DIF-062 — Le seau rouge de Nino, à la pompe (N1, DIF.PAR.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-062"
N1 = 10
TITLE = "Le seau rouge de Nino, à la pompe"
FIL = (
    "Dans la cour, Nino veut remplir son seau rouge "
    "et donner à boire au basilic de la fenêtre. "
    "Papa sait le geste de la pompe, mais il cherche ses mots. "
    "T1 = seau / arrosoir / torchon ; les trois partent. "
    "T2 = pompe (le fer couvre) / muret (les abeilles couvrent) / "
    "fenêtre (trop haute). "
    "Nino laisse la phrase arriver. L'eau tombe. Le basilic boit."
)
CHARS = "Nino, papa, maman"
SETTING = "la cour : pompe, muret au thym, fenêtre du basilic"


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
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    check(SID, out["age_band"], out["chunks"])
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
        "noé",
        "noe ",
        "sami",
        "léa",
        " toboggan",
        "balançoire",
        "bac à sable",
        "capitaine",
        "plic",
        "volet jaune",
        "biscuit",
        "gâteau",
        "cheval",
        "moulinet",
        "loup de carton",
        "dans le salon",
        "joue au salon",
        "à la ferme",
        "veau",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
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
        "lab": "le seau",
        "cap": "Le seau",
        "t1q": "le seau",
        "t1acc": "seau | le seau | rouge | le rouge | seau rouge",
        "t1retry": "Nino tient le seau. Il tient quoi ?",
        "coda": "Le seau rouge tient l'eau, tout droit.",
        "voy": "Le seau penche déjà vers la pompe.",
    },
    2: {
        "lab": "l'arrosoir",
        "cap": "L'arrosoir",
        "t1q": "l'arrosoir",
        "t1acc": "arrosoir | l'arrosoir | le vert | arrosoir vert | le bec",
        "t1retry": "Nino tient l'arrosoir. Il tient quoi ?",
        "coda": "L'arrosoir serre le bec, tout net.",
        "voy": "L'arrosoir tape un peu sa hanche.",
    },
    3: {
        "lab": "le torchon",
        "cap": "Le torchon",
        "t1q": "le torchon",
        "t1acc": "torchon | le torchon | le tissu | le linge",
        "t1retry": "Nino tient le torchon. Il tient quoi ?",
        "coda": "Le torchon sent encore le savon du fer.",
        "voy": "Le torchon pend déjà contre sa poche.",
    },
}

T3_LABS = {
    1: ("le crochet", "le torchon", "le petit bois"),
    2: ("le pas de côté", "les deux mains", "le banc"),
    3: ("le pot du bas", "le tabouret", "les bras de papa"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord le seau rouge.",
            "enfant-m|Il sent encore le fer.",
            "papa|Une goutte dort au fond.",
            "narrateur|Elle roule, puis s'arrête.",
            "maman|L'arrosoir, ensuite, contre lui.",
            "narrateur|Papa glisse le torchon dans la poche.",
            "narrateur|Plus rien n'attend près de la pierre.",
            "enfant-m|On met le seau sous quoi ?",
            "narrateur|Papa ouvre la bouche, puis s'arrête.",
            "enfant-m|Sous la pompe ?",
            "maman|Le mot n'est pas là, encore.",
            "papa|On marche, il va venir.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino prend d'abord l'arrosoir vert.",
            "enfant-m|Le bec est froid, déjà.",
            "maman|Une poussière brille au fond.",
            "narrateur|Le métal fait un petit toc.",
            "papa|Le seau, ensuite, sous le bras.",
            "narrateur|Maman glisse le torchon dans la poche.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Alors dis-moi sous quoi ?",
            "narrateur|Papa inspire, les lèvres déjà rondes.",
            "narrateur|Rien ne sort, encore.",
            "maman|Il cherche la suite.",
            "enfant-m|J'écoute.",
        )
    return L(
        "narrateur|Nino prend d'abord le torchon doux.",
        "enfant-m|Pour essuyer le fer.",
        "papa|Il sent encore le savon.",
        "narrateur|Le tissu frotte la pompe, tout léger.",
        "maman|Le seau, ensuite, et l'arrosoir.",
        "narrateur|Papa les pose contre lui, l'un après l'autre.",
        "narrateur|Près de la pierre, plus rien n'attend.",
        "enfant-m|Maintenant, tu dis sous quoi ?",
        "narrateur|Papa ouvre la bouche, puis la referme.",
        "papa|Le mot va arriver.",
        "enfant-m|D'accord.",
        "maman|On avance, tout doux.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le seau.",
            "papa|Oui.",
            "narrateur|L'arrosoir et le torchon voyagent avec.",
            "maman|L'eau va se dire, plus loin.",
            "enfant-m|Je suis prêt.",
            "papa|On marche, alors ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-m|L'arrosoir.",
            "maman|Oui.",
            "narrateur|Le seau penche déjà sous le bras.",
            "narrateur|Le torchon dort dans la poche.",
            "papa|Le bec a un peu sonné.",
            "enfant-m|J'écoute la suite.",
            "maman|On reste ensemble.",
        )
    return L(
        "enfant-m|Le torchon.",
        "papa|Oui.",
        "narrateur|Le seau et l'arrosoir pèsent contre lui.",
        "maman|Le fer va sécher, en marchant.",
        "enfant-m|J'attends le mot.",
        "papa|Il va venir, tout seul.",
        "maman|On avance, alors ?",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|La cour a trois coins, encore.",
        "papa|La pompe, le muret, ou la fenêtre ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Il tape le fer, un petit toc.",
            2: "Le bec s'accroche au bras, déjà.",
            3: "Il s'enroule autour du manche.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près de la pompe.",
            f"narrateur|{extra}",
            "narrateur|Le manche grince, tout fort.",
            "enfant-m|C'est ici ?",
            "papa|On met le seau sous le.",
            "narrateur|Le mot s'arrête au milieu.",
            "enfant-m|Sous le quoi ?",
            "narrateur|Nino referme sa bouche, tout net.",
            "maman|Le fer a couvert la fin.",
            "papa|On fait comment, Nino ?",
        )
    if t2 == 2:
        extra = {
            1: "Il se pose dans la terre, un peu.",
            2: "Le bec touche une feuille, tout net.",
            3: "Il prend une poussière, déjà.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près du muret.",
            f"narrateur|{extra}",
            "enfant-m|Le pot a soif, ici ?",
            "maman|Il est près des.",
            "narrateur|Les abeilles couvrent le mot, tout fort.",
            "narrateur|Un thym sent, déjà, tout chaud.",
            "enfant-m|Près des fleurs ?",
            "narrateur|Nino recule d'un pas, puis attend.",
            "papa|On n'entend plus la fin.",
            "maman|Tu trouves comment ?",
        )
    extra = {
        1: "Il reste trop bas, encore.",
        2: "Le bec n'atteint pas le bord.",
        3: "Il pend, trop court, sous le pot.",
    }[t1]
    return L(
        f"narrateur|{o['cap']} arrive sous la fenêtre.",
        f"narrateur|{extra}",
        "narrateur|Le basilic sent le poivre, tout près.",
        "enfant-m|Je le vois, les feuilles ?",
        "papa|À gauche du.",
        "narrateur|Papa s'arrête, un doigt en l'air.",
        "enfant-m|Du bord ?",
        "narrateur|Nino garde sa bouche fermée, après.",
        "maman|Tes pieds n'arrivent pas, encore.",
        "papa|La caisse dort près du mur.",
        "papa|Tu fais quoi, alors ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Sur la pompe, la suite manque encore.",
            "papa|Le crochet, le torchon, ou le bois ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Près du thym, le mot n'est pas fini.",
            "maman|Le pas, les mains, ou le banc ?",
        )
    return L(
        "narrateur|Sous la fenêtre, le haut attend encore.",
        "papa|Le pot du bas, le tabouret, ou mes bras ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "Le seau rouge reste contre la jambe, tout sage.",
        2: "L'arrosoir attend une dernière goutte.",
        3: "Le torchon dort contre sa poche.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-m|Le crochet, là.",
            "narrateur|Ils pendent le seau, tout calmes.",
            "papa|Sous le.",
            "narrateur|Nino attend, sans crier.",
            "papa|Sous le bec.",
            "enfant-m|Je vois l'eau, déjà.",
            f"narrateur|{col}",
            "maman|La phrase est arrivée, toute seule.",
            "papa|Merci, Nino.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-m|Le torchon, autour.",
            "papa|Sur le manche, tout doux.",
            "narrateur|Le grincement tombe, puis se tait.",
            "papa|Sous le.",
            "narrateur|Nino ne dit rien.",
            "papa|Sous le bec, maintenant.",
            f"narrateur|{col}",
            "maman|Le fer a laissé le mot.",
            "papa|Tu as écouté jusqu'au bout.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-m|Le petit bois, dessous.",
            "papa|Sous le bras de la pompe.",
            "narrateur|Le bois cale le fer, tout net.",
            "papa|La goutte.",
            "narrateur|Nino garde sa bouche fermée.",
            "papa|La goutte va venir.",
            "enfant-m|Elle vient !",
            f"narrateur|{col}",
            "maman|Tu n'as pas deviné trop tôt.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-m|On recule.",
            "narrateur|Ils s'éloignent des abeilles, tout calmes.",
            "papa|Près des.",
            "narrateur|Nino attend, les lèvres fermées.",
            "papa|Près des pots, le petit.",
            "enfant-m|Je l'entends, maintenant.",
            f"narrateur|{col}",
            "maman|Le mot est venu, tout seul.",
            "papa|Tu as laissé la fin arriver.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-m|Mes mains, ici.",
            "papa|En creux, tout près des oreilles.",
            "narrateur|Le bourdonnement devient un peu loin.",
            "maman|Près des.",
            "narrateur|Nino attend, les lèvres fermées.",
            "maman|Près des feuilles.",
            f"narrateur|{col}",
            "papa|On a écouté ensemble.",
            "maman|La suite a eu sa place.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-m|Le banc, là.",
            "papa|On s'assoit, tout doux.",
            "narrateur|La pierre est chaude, encore.",
            "maman|Le petit pot.",
            "narrateur|Nino tourne la tête, sans parler.",
            "enfant-m|Je le vois, contre le thym.",
            f"narrateur|{col}",
            "papa|Le banc a tenu le mot.",
            "maman|On a regardé ensemble.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-m|Je dis rien.",
            "narrateur|Nino baisse les yeux, tout calme.",
            "papa|Pas le grand.",
            "enfant-m|Le petit.",
            "narrateur|Papa tend le bras, tout bas.",
            "narrateur|Un pot de basilic penche, tout bas.",
            f"narrateur|{col}",
            "maman|Le mot a fini sa route.",
            "papa|Merci d'avoir écouté jusque-là.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-m|Le tabouret, dessous.",
            "papa|Je le tiens, à ta hauteur.",
            "narrateur|Nino monte, tout doux, sans crier.",
            "papa|À gauche du.",
            "narrateur|Nino attend, un pied en l'air.",
            "papa|À gauche du bord.",
            f"narrateur|{col}",
            "maman|Tu as laissé le mot monter.",
            "papa|Le bois a tenu tes pieds.",
        )
    return L(
        "enfant-m|Tes bras, papa.",
        "papa|Viens, tout contre moi.",
        "narrateur|Nino s'élève, le nez au basilic.",
        "papa|Le petit pot, tout près du bord.",
        "enfant-m|Je le vois !",
        "narrateur|Les feuilles touchent sa joue, déjà.",
        f"narrateur|{col}",
        "maman|Tes bras ont fini la phrase.",
        "papa|Chacun a fait sa part.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|L'eau tombe dans le seau, un petit clic.",
            "enfant-m|Elle est là !",
            "papa|Vers la fenêtre, tout droit.",
            "maman|Bravo.",
            coda,
            "narrateur|Une goutte sèche déjà sur le fer.",
            "narrateur|La pompe redevient calme, autour de la pierre.",
            "narrateur|Le thym sent, déjà, vers la maison.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le seau se remplit, enfin, tout net.",
            "enfant-m|J'ai tenu le manche, d'abord.",
            "papa|Puis le mot est venu.",
            "maman|Venez, la soupe sent.",
            coda,
            "narrateur|Nino pose le seau contre sa jambe.",
            "narrateur|Un fil de fer reste tiède, encore.",
            "narrateur|La cour laisse un rai, tout doux.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Sous le bois, l'eau tient, tout net.",
            "enfant-m|On a calé, papa.",
            "papa|Le bras gardera son ombre.",
            "maman|Tiens bien le seau, tout doux.",
            coda,
            "narrateur|Nino tapote le fer, tout léger.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Une abeille passe, puis la pompe se tait.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Loin des abeilles, le pot était là.",
            "enfant-m|Tu as fini, papa.",
            "papa|Oui, le mot était long.",
            "maman|Tu as reculé, tout doux.",
            coda,
            "narrateur|Une terre sèche déjà sur le seau.",
            "narrateur|Nino verse une goutte, tout près.",
            "narrateur|Le muret redevient un muret, tout simple.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Dans le creux, le mot a parlé, enfin.",
            "enfant-m|J'ai écouté, tout contre.",
            "papa|Tes mains étaient à la bonne place.",
            "maman|La soupe t'attend.",
            coda,
            "narrateur|Nino essuie une main sur son pantalon.",
            "narrateur|Une poussière reste sur le thym.",
            "narrateur|Le seau avance, goutte après goutte.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sur le banc, le pot penche encore.",
            "enfant-m|Je l'ai vu, contre le thym.",
            "papa|La pierre a gardé l'ombre.",
            "maman|Verse tout doux, après le mot.",
            coda,
            "narrateur|Nino souffle un peu sur les feuilles.",
            "narrateur|Une terre s'envole, puis retombe.",
            "narrateur|Le banc garde son ombre, tout seul.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Tout en bas, le basilic brille.",
            "enfant-m|Tu as dit petit, à la fin.",
            "papa|Merci d'avoir écouté jusque-là.",
            "maman|Un peu de soupe, après l'eau.",
            coda,
            "narrateur|Nino pose le seau contre le mur.",
            "narrateur|La fenêtre reprend sa place, tout sage.",
            "narrateur|Le haut n'a plus de secret, ce soir.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sur le tabouret, Nino a vu le bord.",
            "enfant-m|Le mot est monté avec moi.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Essuie tes chaussures, Nino.",
            coda,
            "narrateur|L'eau monte jusqu'au seuil, tout net.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|La fenêtre redevient calme, un carreau encore.",
        )
    return L(
        "narrateur|Dans les bras de papa, le pot était là.",
        "enfant-m|On a versé, tout haut.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        coda,
        "narrateur|Nino pose le seau près des pavés.",
        "narrateur|Les feuilles boivent l'air, enfin.",
        "narrateur|Une goutte claque, puis le fer se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une goutte pend encore à la pompe.",
        "narrateur|Elle tombe sur la pierre chaude, tic.",
        "narrateur|La cour sent le fer et le thym.",
        "papa|Le basilic a soif, là-haut.",
        "enfant-m|Je veux lui donner à boire.",
        "maman|Le soleil part déjà du mur.",
        "narrateur|En ce moment, Nino tient le seau.",
        "enfant-m|Il est rouge, tout neuf.",
        "papa|On met d'abord le seau sous.",
        "narrateur|Papa cherche, la bouche ouverte.",
        "enfant-m|Sous quoi ?",
        "narrateur|Nino referme sa bouche, tout net.",
        "maman|La suite va arriver.",
        "papa|Prenez vos affaires, avant le soleil.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près de la pompe.",
        "narrateur|Le seau, l'arrosoir, et le torchon.",
        "papa|Tu prends quoi, d'abord ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le seau", "l'arrosoir", "le torchon")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nino a pris {o['t1q']}, tout près.",
            "maman|Nino a pris quoi, d'abord ?",
        )
        ans = o["t1q"].split()[-1].replace("l'", "").replace("d'", "")
        extras[f"{p}_Q0001"] = qf(ans, o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la pompe", "le muret", "la fenêtre")

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
        "Nino veut remplir son seau rouge et donner à boire au basilic. "
        "Papa sait le geste de la pompe, cherche ses mots. "
        "T1 = seau / arrosoir / torchon (les trois partent). "
        "T2 = pompe (fer qui couvre) / muret (abeilles) / fenêtre (trop haute). "
        "T3 = neuf résolutions (crochet, torchon, petit bois ; "
        "pas de côté, deux mains, banc ; "
        "pot du bas, tabouret, bras de papa). "
        "Nino referme sa bouche. L'eau tombe. Le basilic boit. "
        "Fin : pierre, thym, goutte, cour calme.",
        "Slogan ferme / Tom / bac-toboggan-balançoires / Tom-Léa-Sami jetés. "
        "Autre récit que DIF-018 (biscuits jardin), DIF-028 (gâteau), "
        "DIF-038 (cheval sous l'auvent), DIF-046 (moulinet marché), "
        "DIF-054 (loup de carton). "
        "Héros Nino, papa/maman, pas de copain. Désir ≠ leçon. "
        "N1 ≤ 10. Oral lié. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
