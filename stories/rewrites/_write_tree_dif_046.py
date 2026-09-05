#!/usr/bin/env python3
"""TREE-DIF-046 — Le moulinet rouge de Victorino, au marché (N1, DIF.PAR.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-046"
N1 = 10
TITLE = "Le moulinet rouge de Victorino, au marché"
FIL = (
    "Au marché du village, Victorino veut le moulinet rouge "
    "qui tourne tout seul dans le vent. "
    "Papa sait l'étal, mais il cherche ses mots. "
    "T1 = panier / ficelle / bourse ; les trois partent. "
    "T2 = étal de papier (trop mêlé) / fontaine (l'eau couvre) / "
    "auvent bleu (trop haut). "
    "Victorino laisse la phrase arriver. Le rouge tourne jusqu'à la maison."
)


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
    out["characters"] = "Victorino, papa, maman"
    out["setting"] = "marché du village : étal de papier, fontaine, auvent bleu"
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
        "adam",
        " toboggan",
        "balançoire",
        "bac à sable",
        "capitaine",
        "plic",
        "volet jaune",
        "biscuit",
        "gâteau",
        "cheval",
        "dans le salon",
        "joue au salon",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
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
        "lab": "le panier",
        "cap": "Le panier",
        "t1q": "le panier",
        "t1acc": "panier | le panier | l'osier | panier d'osier",
        "t1retry": "Victorino tient le panier. Il tient quoi ?",
        "coda": "Le panier tient le bâton, tout droit.",
        "voy": "Le panier penche déjà vers l'allée.",
    },
    2: {
        "lab": "la ficelle",
        "cap": "La ficelle",
        "t1q": "la ficelle",
        "t1acc": "ficelle | la ficelle | le fil | la corde",
        "t1retry": "Victorino tient la ficelle. Il tient quoi ?",
        "coda": "La ficelle serre le bois, tout net.",
        "voy": "La ficelle tape un peu sa hanche.",
    },
    3: {
        "lab": "la bourse",
        "cap": "La bourse",
        "t1q": "la bourse",
        "t1acc": "bourse | la bourse | les pièces | la monnaie",
        "t1retry": "Victorino tient la bourse. Il tient quoi ?",
        "coda": "La bourse cliquette une fois, puis se tait.",
        "voy": "La bourse pèse déjà contre sa poche.",
    },
}

T3_LABS = {
    1: ("le clou bas", "le souffle", "le papier jaune"),
    2: ("le pas en arrière", "le creux des mains", "le banc"),
    3: ("le petit en bas", "le tabouret", "les bras de papa"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorino prend d'abord le panier d'osier.",
            "enfant-m|Il gratte un peu, déjà.",
            "papa|L'osier a gardé une paille.",
            "narrateur|Elle pique sa paume, puis s'arrête.",
            "maman|La ficelle, ensuite, autour du bord.",
            "narrateur|Papa glisse la bourse dans la poche.",
            "narrateur|Plus rien n'attend près des caisses.",
            "enfant-m|Où est le rouge ?",
            "narrateur|Papa ouvre la bouche, puis s'arrête.",
            "enfant-m|À quel étal ?",
            "maman|Le mot n'est pas là, encore.",
            "papa|On marche, il va venir.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorino enroule d'abord la ficelle beige.",
            "enfant-m|Elle sent le lin, un peu.",
            "maman|Un nœud dort déjà au bout.",
            "narrateur|Le fil serre son poignet, tout doux.",
            "papa|Le panier, ensuite, contre lui.",
            "narrateur|Maman glisse la bourse dans la poche.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Alors dis-moi où.",
            "narrateur|Papa inspire, les lèvres déjà rondes.",
            "narrateur|Rien ne sort, encore.",
            "maman|Il cherche la suite.",
            "enfant-m|J'écoute.",
        )
    return L(
        "narrateur|Victorino prend d'abord la bourse ronde.",
        "enfant-m|Pour payer, après.",
        "papa|Elle cliquette un peu, déjà.",
        "narrateur|Deux pièces roulent, puis se taisent.",
        "maman|Le panier, ensuite, et la ficelle.",
        "narrateur|Papa les pose contre lui, l'un après l'autre.",
        "narrateur|Près des caisses, plus rien n'attend.",
        "enfant-m|Maintenant, tu dis où.",
        "narrateur|Papa ouvre la bouche, puis la referme.",
        "papa|Le mot va arriver.",
        "enfant-m|D'accord.",
        "maman|On avance, tout doux.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le panier.",
            "papa|Oui.",
            "narrateur|La ficelle et la bourse voyagent avec.",
            "maman|Le rouge va se dire, plus loin.",
            "enfant-m|Je suis prêt.",
            "papa|On marche, alors ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La ficelle.",
            "maman|Oui.",
            "narrateur|Le panier penche déjà sous le bras.",
            "narrateur|La bourse dort dans la poche.",
            "papa|Le lin a un peu serré.",
            "enfant-m|J'écoute la suite.",
            "maman|On reste ensemble.",
        )
    return L(
        "enfant-m|La bourse.",
        "papa|Oui.",
        "narrateur|Le panier et la ficelle pèsent contre lui.",
        "maman|Les pièces vont parler, en marchant.",
        "enfant-m|J'attends le mot.",
        "papa|Il va venir, tout seul.",
        "maman|On avance, alors ?",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Le marché a trois coins, encore.",
        "papa|L'étal, la fontaine, ou l'auvent ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Il bute contre une caisse de papier.",
            2: "Elle s'accroche à un clou, déjà.",
            3: "Elle tape le bois, un petit toc.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près de l'étal de papier.",
            f"narrateur|{extra}",
            "narrateur|Des moulinets pendent, tous mêlés.",
            "enfant-m|C'est ici ?",
            "papa|C'est le rouge, près du.",
            "narrateur|Le mot s'arrête au milieu.",
            "enfant-m|Près du quoi ?",
            "narrateur|Victorino referme sa bouche, tout net.",
            "maman|Ils se ressemblent tous, là-haut.",
            "papa|On fait comment, Victorino ?",
        )
    if t2 == 2:
        extra = {
            1: "Il se mouille un peu, au bord.",
            2: "Elle boit une goutte, tout net.",
            3: "Elle cliquette sous l'eau qui vole.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près de la fontaine.",
            f"narrateur|{extra}",
            "enfant-m|Il est là, le rouge ?",
            "maman|Il est près de l'.",
            "narrateur|L'eau couvre le mot, tout fort.",
            "narrateur|Des gouttes tapent le bord, déjà.",
            "enfant-m|Près de l'eau ?",
            "narrateur|Victorino recule d'un pas, puis attend.",
            "papa|On n'entend plus la fin.",
            "maman|Tu trouves comment ?",
        )
    extra = {
        1: "Il reste trop bas, encore.",
        2: "Elle pend, trop courte, sous le bleu.",
        3: "Elle n'atteint pas le bord, trop haute.",
    }[t1]
    return L(
        f"narrateur|{o['cap']} arrive sous l'auvent bleu.",
        f"narrateur|{extra}",
        "enfant-m|Tout en haut ?",
        "papa|Tout en haut, près du.",
        "narrateur|Papa s'arrête, les lèvres encore rondes.",
        "enfant-m|Près du bord ?",
        "narrateur|Victorino garde sa bouche fermée, après.",
        "maman|Le haut est trop loin, pour lui.",
        "papa|Un tabouret dort près du mur.",
        "papa|Tu fais quoi, alors ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Sur l'étal, la suite manque encore.",
            "papa|Le clou, le souffle, ou le papier ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Près de l'eau, le mot n'est pas fini.",
            "maman|Le pas, les mains, ou le banc ?",
        )
    return L(
        "narrateur|Sous l'auvent, le haut attend encore.",
        "papa|Le petit, le tabouret, ou mes bras ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "Le panier reste contre la jambe, tout sage.",
        2: "La ficelle attend un dernier nœud.",
        3: "La bourse dort contre sa paume.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-m|On reste.",
            "narrateur|Ils s'arrêtent sous les papiers, tout calmes.",
            "papa|Le clou.",
            "enfant-m|Le clou bas.",
            "narrateur|Victorino attend, sans crier.",
            "narrateur|Un moulinet rouge penche, enfin.",
            f"narrateur|{col}",
            "maman|La phrase est arrivée, toute seule.",
            "papa|Merci, Victorino.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-m|Je souffle.",
            "narrateur|Un moulinet part, puis un autre.",
            "papa|Le.",
            "narrateur|Victorino ne dit rien.",
            "papa|Le rouge qui tourne.",
            "enfant-m|Je le vois, maintenant.",
            f"narrateur|{col}",
            "maman|Le vent a aidé le mot.",
            "papa|Tu as écouté jusqu'au bout.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-m|On se baisse.",
            "narrateur|Ils regardent le papier jaune, tout près.",
            "papa|Pas le haut.",
            "narrateur|Victorino garde sa bouche fermée.",
            "papa|Contre le jaune.",
            "enfant-m|Celui-là, tout contre la feuille.",
            f"narrateur|{col}",
            "maman|Tu n'as pas deviné trop tôt.",
            "papa|Le rouge est là, tout net.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-m|On recule.",
            "narrateur|Les deux s'éloignent de l'eau, tout calmes.",
            "papa|Près de l'.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "papa|Près de l'eau, le rouge.",
            "enfant-m|Je l'entends, maintenant.",
            f"narrateur|{col}",
            "maman|Le mot est venu, tout seul.",
            "papa|Tu as laissé la fin arriver.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-m|Mes mains, ici.",
            "papa|En creux, tout près des oreilles.",
            "narrateur|L'eau devient un peu plus loin.",
            "maman|Près de.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "maman|Près de la pierre.",
            f"narrateur|{col}",
            "papa|On a écouté ensemble.",
            "maman|La suite a eu sa place.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-m|Le banc, là.",
            "papa|On s'assoit, tout doux.",
            "narrateur|La pierre est froide, encore.",
            "maman|Le rouge.",
            "narrateur|Victorino tourne la tête, sans parler.",
            "enfant-m|Je le vois, contre la pierre.",
            f"narrateur|{col}",
            "papa|Le banc a tenu le mot.",
            "maman|On a regardé ensemble.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-m|Je dis rien.",
            "narrateur|Victorino baisse les yeux, tout calme.",
            "papa|Pas le grand.",
            "enfant-m|Le petit.",
            "narrateur|Papa tend le bras, tout bas.",
            "narrateur|Un moulinet rouge penche, tout bas.",
            f"narrateur|{col}",
            "maman|Le mot a fini sa route.",
            "papa|Merci d'avoir écouté jusque-là.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-m|Le tabouret, dessous.",
            "papa|Je le tiens, à ta hauteur.",
            "narrateur|Victorino monte, tout doux, sans crier.",
            "papa|Près du.",
            "narrateur|Victorino attend, un pied en l'air.",
            "papa|Près du bord.",
            f"narrateur|{col}",
            "maman|Tu as laissé le mot monter.",
            "papa|Le bois a tenu tes pieds.",
        )
    return L(
        "enfant-m|Tes bras, papa.",
        "papa|Viens, tout contre moi.",
        "narrateur|Victorino s'élève, le nez au bleu.",
        "papa|Le rouge, tout près du bord.",
        "enfant-m|Je le vois !",
        "narrateur|Un moulinet brille entre deux toiles.",
        f"narrateur|{col}",
        "maman|Tes bras ont fini la phrase.",
        "papa|Chacun a fait sa part.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le bâton rentre dans le poing, un petit clic.",
            "enfant-m|Il tourne !",
            "papa|Sur le chemin, tout droit.",
            "maman|Bravo.",
            coda,
            "narrateur|Une paille sèche déjà sur l'osier.",
            "narrateur|L'étal redevient calme, autour des papiers.",
            "narrateur|La soupe sent, déjà, vers la maison.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le moulinet part, enfin, tout rouge.",
            "enfant-m|J'ai soufflé, d'abord.",
            "papa|Puis le mot est venu.",
            "maman|Venez, le pain est chaud.",
            coda,
            "narrateur|Victorino pose le bâton contre l'épaule.",
            "narrateur|Un papier reste collé à sa chaussure.",
            "narrateur|Le marché laisse un rai, tout doux.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Contre le jaune, le rouge tient, tout net.",
            "enfant-m|On s'est baissés, papa.",
            "papa|Le haut gardera son ombre.",
            "maman|Tiens bien le bâton, tout doux.",
            coda,
            "narrateur|Victorino tapote le papier, tout léger.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Une abeille passe, puis l'étal se tait.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Loin de l'eau, le rouge était là.",
            "enfant-m|Tu as fini, papa.",
            "papa|Oui, le mot était long.",
            "maman|Tu as reculé, tout doux.",
            coda,
            "narrateur|Une goutte sèche déjà sur le bâton.",
            "narrateur|Victorino fait tourner le rouge, tout près.",
            "narrateur|La fontaine redevient une fontaine, tout simple.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Dans le creux, le mot a parlé, enfin.",
            "enfant-m|J'ai écouté, tout contre.",
            "papa|Tes mains étaient à la bonne place.",
            "maman|Le pain t'attend.",
            coda,
            "narrateur|Victorino essuie une main sur son pantalon.",
            "narrateur|Une goutte reste sur le papier.",
            "narrateur|Le moulinet avance, tour après tour.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sur le banc, le rouge penche encore.",
            "enfant-m|Je l'ai vu, contre la pierre.",
            "papa|La pierre a gardé l'ombre.",
            "maman|Rentre le bâton, après le tour.",
            coda,
            "narrateur|Victorino souffle un peu sur les pales.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Le banc garde son ombre, tout seul.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Tout en bas, le rouge brille.",
            "enfant-m|Tu as dit petit, à la fin.",
            "papa|Merci d'avoir écouté jusque-là.",
            "maman|Un peu de soupe, après le vent.",
            coda,
            "narrateur|Victorino pose le bâton contre le mur.",
            "narrateur|L'auvent bleu reprend sa place, tout sage.",
            "narrateur|Le haut n'a plus de secret, ce matin.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sur le tabouret, Victorino a vu le bord.",
            "enfant-m|Le mot est monté avec moi.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Essuie tes chaussures, Victorino.",
            coda,
            "narrateur|Le moulinet tourne jusqu'au seuil, tout net.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|L'auvent redevient calme, une toile encore.",
        )
    return L(
        "narrateur|Dans les bras de papa, le rouge était là.",
        "enfant-m|On l'a pris, tout haut.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        coda,
        "narrateur|Victorino pose le bâton près des pavés.",
        "narrateur|Les pales touchent l'air, enfin.",
        "narrateur|Une toile claque, puis le vent se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Les toiles claquent au-dessus des pavés.",
        "narrateur|Le marché du village est déjà ouvert.",
        "narrateur|Un rayon tombe sur une caisse, tout chaud.",
        "narrateur|Ça sent le thym et le savon tiède.",
        "papa|Tu as vu le rouge, là-haut ?",
        "enfant-m|Il tourne tout seul.",
        "maman|Le vent le pousse, déjà.",
        "narrateur|En ce moment, Victorino lève le nez.",
        "enfant-m|Je le veux, pour rentrer.",
        "papa|Il est à l'étal du.",
        "narrateur|Papa cherche, la bouche ouverte.",
        "enfant-m|Du quoi ?",
        "narrateur|Victorino referme sa bouche, tout net.",
        "maman|La suite va arriver.",
        "papa|Prenez vos affaires, avant le vent.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des caisses.",
        "narrateur|Le panier, la ficelle, et la bourse.",
        "papa|Tu prends quoi, d'abord ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le panier", "la ficelle", "la bourse")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Victorino a pris {o['t1q']}, tout près.",
            "maman|Victorino a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'étal de papier", "la fontaine", "l'auvent bleu")

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
        "Victorino veut le moulinet rouge qui tourne au vent du marché. "
        "Papa sait l'étal, cherche ses mots. "
        "T1 = panier / ficelle / bourse (les trois partent). "
        "T2 = étal de papier (mêlé, clou) / fontaine (eau qui couvre) / "
        "auvent bleu (trop haut). "
        "T3 = neuf résolutions (clou bas, souffle, papier jaune ; "
        "pas en arrière, creux des mains, banc ; "
        "petit en bas, tabouret, bras de papa). "
        "Victorino referme sa bouche. Le rouge tourne jusqu'à la maison. "
        "Fin : pavés, soupe, toiles calmes.",
        "Slogan salon / Adam / bac-toboggan-balançoires / Tom-Léa-Sami jetés. "
        "Autre récit que DIF-018 (biscuits jardin), DIF-028 (gâteau) "
        "et DIF-038 (cheval sous l'auvent). "
        "Héros Victorino, papa/maman, pas de copain. Désir ≠ leçon. "
        "N1 ≤ 10. Oral lié. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
