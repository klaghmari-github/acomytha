#!/usr/bin/env python3
"""TREE-DIF-061 — Le moulin de papier d'Aniss et la grille de l'école (N3, DIF.PAR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-061"
N3 = 16
TITLE = "Le moulin de papier d'Aniss et la grille de l'école"
FIL = (
    "Aniss veut planter son moulin de papier dans la grille de l'école, "
    "pour le voir tourner pendant la classe. Mila arrive ; elle voudrait "
    "l'entendre crier tourne, mais Aniss répond avec les mains. "
    "T1 = moulin / fil / caillou, les trois partent. "
    "T2 = grille (barreaux trop serrés) / caniveau (eau trop vite) / "
    "porche (air trop calme). T3 = neuf façons. Mila attend, tend. "
    "Le moulin tourne, on entre."
)


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
    out["characters"] = "Aniss, Mila, papa, maman"
    out["setting"] = "chemin de l'école : grille, caniveau, porche"
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
        "lila",
        " parlé peu",
        "parle peu",
        "camarade",
        "timide",
        "forcer la parole",
        "il faut attendre",
        "un camarade",
        "la cuisine",
        "le jardin",
        "la chambre",
        "dînette",
        "dinette",
        "après la sieste",
        "capitaine",
        "locomotive",
        "gare en carton",
        "cuillère",
        "véranda",
        "petite roue",
        "galet",
        "épuisette",
        "nichoir",
        "merle",
        "pommier",
        "cerf-volant",
        "cerf volant",
        "soleil en papier",
        "cloche",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
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
        "lab": "le moulin",
        "cap": "Le moulin",
        "t1q": "le moulin",
        "t1ans": "moulin",
        "t1acc": "moulin | le moulin | le papier | tendre",
        "t1retry": "Il tend le moulin. Il tend quoi ?",
        "coda": "Une pale de papier tremble encore, toute jaune.",
        "voy": "Le moulin voyage déjà contre le sac.",
    },
    2: {
        "lab": "le fil",
        "cap": "Le fil",
        "t1q": "le fil",
        "t1ans": "fil",
        "t1acc": "fil | le fil | la bobine | tendre",
        "t1retry": "Il tend le fil. Il tend quoi ?",
        "coda": "Un bout de fil pend, tout calme, contre le fer.",
        "voy": "Le fil voyage déjà autour du bâton.",
    },
    3: {
        "lab": "le caillou",
        "cap": "Le caillou",
        "t1q": "le caillou",
        "t1ans": "caillou",
        "t1acc": "caillou | le caillou | la pierre | tendre",
        "t1retry": "Il tend le caillou. Il tend quoi ?",
        "coda": "Le caillou reste tiède, contre le barreau.",
        "voy": "Le caillou voyage déjà contre le papier.",
    },
}

T3_LABS = {
    1: ("le bas", "les mains de Mila", "le crochet"),
    2: ("la dalle", "le fil", "le bord"),
    3: ("le vent", "la marche", "le nœud"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss sort d'abord le moulin du sac.",
            "enfant-m|Il est froid.",
            "papa|Une pale a encore un peu de colle.",
            "narrateur|Il le tend vers Mila, tout près.",
            "copine|Dis tourne !",
            "narrateur|Aniss pose deux doigts sur le papier.",
            "narrateur|Le vent manque, puis revient, tout petit.",
            "maman|Le fil et le caillou viennent aussi.",
            "narrateur|Papa glisse le tout contre le sac.",
            "narrateur|Le bitume ne garde plus rien.",
            "copine|Aniss, on part ?",
            "narrateur|Aniss hoche la tête, tout petit.",
            "papa|Le moulin d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss sort d'abord le fil beige.",
            "enfant-m|Il gratte un peu.",
            "maman|La bobine sent encore le tiroir.",
            "narrateur|Il tend le fil vers Mila.",
            "copine|Dis nœud !",
            "narrateur|Aniss enroule un tour, sans un mot.",
            "narrateur|Le fil se tait, tout calme, autour du bâton.",
            "papa|Le moulin et le caillou viennent aussi.",
            "narrateur|Maman les pose contre le papier.",
            "narrateur|Tout part ensemble, déjà.",
            "copine|Aniss, tu viens ?",
            "narrateur|Aniss lève le fil, tout bas.",
            "maman|Le fil d'abord, vous l'avez.",
        )
    return L(
        "narrateur|Aniss sort d'abord le caillou rond.",
        "enfant-m|Il est tiède.",
        "papa|La pierre a séché près du muret.",
        "narrateur|Il tend le caillou vers Mila.",
        "copine|Dis pierre !",
        "narrateur|Aniss le cale contre le bâton, tout lent.",
        "narrateur|Le papier se tient, sans un mot.",
        "maman|Le moulin et le fil viennent aussi.",
        "narrateur|Papa les glisse près des bottes.",
        "narrateur|Le caillou les garde, tous les trois.",
        "copine|Aniss, c'est bon ?",
        "narrateur|Aniss appuie sur la pierre, tout calme.",
        "papa|Le caillou d'abord, il tient.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss garde le moulin contre lui.",
            "copine|Il est à toi, un moment.",
            "narrateur|Mila attend, les mains ouvertes.",
            "narrateur|Une pale tremble, toute petite, au vent.",
            "maman|Le papier est tiède, maintenant.",
            "papa|On pose le moulin où ?",
            "copine|Vers la grille, peut-être.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss garde le fil contre sa jambe.",
            "copine|Il est à toi, un moment.",
            "narrateur|Mila attend, sans répéter.",
            "narrateur|La bobine sent encore le tiroir.",
            "maman|Le moulin peut tourner, après.",
            "papa|On pose le moulin où ?",
            "copine|Vers le caniveau, peut-être.",
        )
    return L(
        "narrateur|Aniss tient encore le caillou, tout près.",
        "copine|Il est à toi, un moment.",
        "narrateur|Mila attend, les lèvres fermées.",
        "narrateur|Un grain de poussière tombe, puis s'arrête.",
        "papa|Le porche de l'école attend, plus loin.",
        "maman|On pose le moulin où ?",
        "copine|Vers le porche, tout doux.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Le chemin monte un peu, encore mouillé.",
        "narrateur|La grille serre trop les barreaux, déjà.",
        "maman|Le caniveau emporte trop d'eau, plus bas.",
        "narrateur|Sous le porche, l'air ne pousse plus.",
        "papa|On commence où, pour le moulin ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = {
            1: "narrateur|Le bâton du moulin bute contre deux barreaux.",
            2: "narrateur|Le fil se coince entre deux barreaux froids.",
            3: "narrateur|Le caillou reste coincé, trop large pour le fer.",
        }[t1]
        return L(
            lead,
            "narrateur|La grille serre trop, juste à hauteur d'Aniss.",
            "copine|Pousse-le, Aniss !",
            "narrateur|Aniss montre un écart plus bas, du doigt.",
            "narrateur|Le fer reste froid, trop près des pales.",
            "copine|Dis-moi où !",
            "maman|Il montre déjà, avec le doigt.",
            "papa|Le crochet du loquet brille un peu.",
            "narrateur|Aniss ouvre un peu les mains.",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Une pale du moulin touche l'eau trop vite.",
            2: "narrateur|Le fil traîne dans l'eau trop vite.",
            3: "narrateur|Le caillou glisse vers l'eau trop vite.",
        }[t1]
        return L(
            lead,
            "copine|L'eau est trop grande.",
            "narrateur|Une feuille jaune part déjà, plus bas.",
            "copine|Attrape, Aniss !",
            "narrateur|Aniss recule le papier, tout calme.",
            "narrateur|L'eau frappe la dalle, puis rebondit.",
            "maman|La dalle tient encore le courant.",
            "papa|On reste près du caniveau, tous les deux.",
            "narrateur|Une goutte brille aussi, plus bas.",
            "papa|Vous faites comment, tous les deux ?",
        )
    lead = {
        1: "narrateur|Les pales du moulin s'arrêtent sous le porche.",
        2: "narrateur|Le fil pend, trop lourd, sous le porche.",
        3: "narrateur|Le caillou reste sourd, sous le porche.",
    }[t1]
    return L(
        lead,
        "copine|Ça ne tourne plus, Aniss !",
        "narrateur|Mila souffle trop vite, trop fort.",
        "copine|Dis vent !",
        "narrateur|Aniss pointe la porte, du doigt.",
        "narrateur|Le porche garde l'air, trop fermé.",
        "maman|Tes yeux vont plus loin, Aniss.",
        "papa|La marche du seuil est encore sèche.",
        "narrateur|Un rai de soleil reste trop mince.",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Les barreaux restent trop serrés, encore.",
            "papa|Le bas, les mains, ou le crochet ?",
        )
    if t2 == 2:
        return L(
            "narrateur|L'eau tient encore la feuille jaune.",
            "maman|La dalle, le fil, ou le bord ?",
        )
    return L(
        "narrateur|L'air reste trop calme, encore.",
        "papa|Le vent, la marche, ou le nœud ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le moulin reste bas, près du bitume.",
            2: "narrateur|Le fil reste bas, près du bitume.",
            3: "narrateur|Le caillou reste bas, près du bitume.",
        }[t1]
        return L(
            "copine|On attend.",
            "narrateur|Aniss cherche l'écart du bas, tout lent.",
            "narrateur|Mila suit le doigt, enfin, un peu.",
            wait,
            "narrateur|Aniss glisse le bâton, sans un mot.",
            "narrateur|Le fer fait toc, tout net, plus large.",
            "copine|Toc.",
            "papa|Le bas laisse un vrai passage.",
            "maman|Vous avez laissé le temps au fer.",
        )
    if t2 == 1 and t3 == 2:
        hold = {
            1: "narrateur|Le moulin glisse vers les mains de Mila.",
            2: "narrateur|Le fil guide le papier vers Mila.",
            3: "narrateur|Le caillou suit le papier vers Mila.",
        }[t1]
        return L(
            "copine|Pour toi.",
            "narrateur|Mila ouvre les deux mains, tout près.",
            "narrateur|Aniss pose le jaune contre ses paumes.",
            hold,
            "narrateur|Mila vise l'écart, Aniss pousse le bâton.",
            "copine|Il passe !",
            "maman|Le papier a pris le barreau, tout seul.",
            "papa|Tes mains ont trouvé le fer.",
        )
    if t2 == 1 and t3 == 3:
        hook = {
            1: "narrateur|Le moulin pend déjà au crochet du loquet.",
            2: "narrateur|Le fil s'enroule déjà au crochet du loquet.",
            3: "narrateur|Le caillou cale déjà le crochet du loquet.",
        }[t1]
        return L(
            "copine|Le crochet, Aniss.",
            "narrateur|Aniss lève le jaune, sans un mot.",
            "narrateur|Mila attend, puis suit sa main.",
            hook,
            "narrateur|Une pale racle le fer, puis se libère.",
            "copine|Merci.",
            "papa|Le loquet a gardé le calme.",
            "maman|Les barreaux peuvent dormir, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        stone = {
            1: "narrateur|Le moulin sèche contre la dalle.",
            2: "narrateur|Le fil sèche contre la dalle.",
            3: "narrateur|Le caillou sèche contre la dalle.",
        }[t1]
        return L(
            "copine|On attend l'eau.",
            "narrateur|Aniss s'assoit près du caniveau, tout calme.",
            "narrateur|Mila s'assoit aussi, les genoux contre lui.",
            stone,
            "narrateur|L'eau frappe, puis la feuille s'arrête.",
            "copine|Maintenant.",
            "papa|La dalle a cassé le courant.",
            "maman|Vous avez laissé l'eau finir.",
        )
    if t2 == 2 and t3 == 2:
        rope = {
            1: "narrateur|Le moulin traverse au bout du fil.",
            2: "narrateur|Le fil part au bout des mains de Mila.",
            3: "narrateur|Le caillou guide le fil, tout droit.",
        }[t1]
        return L(
            "copine|Tes mains, Aniss.",
            "narrateur|Aniss tend le fil, tout près.",
            "narrateur|Mila tire avec lui, tout lent.",
            rope,
            "narrateur|Le papier passe au-dessus de l'eau.",
            "copine|On tient ensemble.",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|L'eau restera après.",
        )
    if t2 == 2 and t3 == 3:
        edge = {
            1: "narrateur|Le moulin suit le bord sec, déjà.",
            2: "narrateur|Le fil suit le bord sec, déjà.",
            3: "narrateur|Le caillou suit le bord sec, déjà.",
        }[t1]
        return L(
            "copine|Le bord, d'abord.",
            "narrateur|Mila tend la pierre sèche vers Aniss.",
            "narrateur|Aniss marche, tout doux, sans un mot.",
            edge,
            "narrateur|Une goutte rejoint le fond, tout calme.",
            "copine|C'est doux.",
            "maman|L'eau garde son souffle, plus loin.",
            "papa|Le bord a laissé le papier.",
        )
    if t2 == 3 and t3 == 1:
        draft = {
            1: "narrateur|Le moulin prend le vent de la porte.",
            2: "narrateur|Le fil prend le vent de la porte.",
            3: "narrateur|Le caillou prend le vent de la porte.",
        }[t1]
        return L(
            "copine|Le vent, d'abord.",
            "papa|J'ouvre un peu, à votre hauteur.",
            "narrateur|Aniss attend, Mila tient le jaune.",
            draft,
            "narrateur|Une pale part, tout doux, sans un mot.",
            "copine|Ça tient !",
            "papa|La porte a donné le courant.",
            "maman|Aniss a poussé tout doux.",
        )
    if t2 == 3 and t3 == 2:
        step = {
            1: "narrateur|Le moulin pose ses pales sur la marche.",
            2: "narrateur|Le fil pose le papier sur la marche.",
            3: "narrateur|Le caillou cale le papier sur la marche.",
        }[t1]
        return L(
            "enfant-m|Mila.",
            "narrateur|Aniss pointe la marche, du doigt.",
            "narrateur|Mila attend, puis ouvre les mains.",
            step,
            "narrateur|Le courant du seuil pousse, tout net.",
            "copine|Je le tiens.",
            "maman|Le porche garde son ombre, plus loin.",
            "papa|Tes mains ont guidé le moulin.",
        )
    knot = {
        1: "narrateur|Le moulin suit le nœud, tour après tour.",
        2: "narrateur|Le fil serre le nœud, tout calme.",
        3: "narrateur|Le caillou tient derrière le nœud, tout droit.",
    }[t1]
    return L(
        "copine|Le nœud, Aniss.",
        "narrateur|Aniss pointe le crochet du porche, du doigt.",
        "narrateur|Mila attend, puis suit le doigt.",
        knot,
        "narrateur|Le jaune se tient, hors du mur.",
        "copine|Il évite le mur.",
        "papa|Le nœud a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le moulin pose une pale sur le fer.",
            "enfant-m|Tourne.",
            "copine|Il est arrivé.",
            "papa|Le bas a laissé le passage.",
            "maman|La grille est prête, tout près.",
            "narrateur|Aniss pose encore une main sur le barreau.",
            coda,
            "narrateur|Une feuille jaune tourne autour du papier.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le jaune s'est glissé jusqu'au barreau.",
            "copine|Aniss l'a tendu, tout seul.",
            "papa|Tu as tendu, d'abord.",
            "maman|Venez, le moulin est encore calme.",
            coda,
            "narrateur|Aniss s'assoit près de la grille.",
            "enfant-m|Tiens.",
            "narrateur|La botte de Mila reste sous le fer.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le jaune pend au crochet, déjà droit.",
            "copine|On a posé le moulin.",
            "papa|Le crochet a tenu, tout droit.",
            "maman|Essuyez vos mains, tout doux.",
            coda,
            "narrateur|Aniss recule, un pied après l'autre.",
            "narrateur|Le loquet de fer reste un peu froid.",
            "narrateur|Une pale pousse l'air, tout près.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le jaune rejoint la grille, encore mouillé.",
            "copine|On a attendu l'eau.",
            "papa|Le caniveau n'a plus pris vos bras.",
            "maman|Rentrez le fil, après la grille.",
            coda,
            "enfant-m|Toc.",
            "narrateur|Une goutte se tait, puis l'autre.",
            "narrateur|Le caniveau reste calme, derrière eux.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le fil pose le moulin contre le fer.",
            "copine|On tenait, tous les deux.",
            "papa|Je remporte le fil, tout à l'heure.",
            "maman|La grille vous attend.",
            coda,
            "narrateur|Aniss essuie une main sur son pantalon.",
            "narrateur|Un grain de colle reste sur le fil.",
            "narrateur|Le fer sent encore l'eau tiède.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains d'Aniss laissent le jaune contre le fer.",
            "copine|C'était plus facile, là.",
            "papa|Tes bras ont guidé le moulin.",
            "maman|Le barreau gardera son ombre.",
            coda,
            "narrateur|Aniss pose un doigt sur le fer.",
            "narrateur|Une pale bouge, toute petite.",
            "narrateur|Un rai de soleil barre encore la grille.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le jaune rejoint la grille, tout sec.",
            "copine|On a trouvé, Aniss.",
            "papa|Le vent n'a pas glissé.",
            "maman|Entrez, le seuil est sec.",
            coda,
            "narrateur|Aniss pose un grain de poussière sur la marche.",
            "narrateur|Le grain ne bouge plus.",
            "narrateur|Une goutte sèche déjà sur le fer.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Les mains de Mila laissent le jaune au fer.",
            "copine|On l'a tenu, tous les deux.",
            "papa|Le porche est resté à sa place.",
            "maman|Essuie tes chaussures, Aniss.",
            coda,
            "narrateur|Aniss souffle un peu sur le papier.",
            "narrateur|Un grain blanchit, puis s'arrête.",
            "narrateur|Un peu de colle reste derrière la porte.",
        )
    return L(
        "narrateur|Le jaune suit le nœud, jusqu'à la grille.",
        "copine|L'ombre était douce.",
        "papa|Le nœud a tenu, tout droit.",
        "maman|Le porche n'a plus rien à dire.",
        coda,
        "narrateur|Aniss touche le fer, un instant.",
        "narrateur|Une pale revient contre le jaune.",
        "narrateur|Un oiseau passe, puis le chemin se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "vent"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une odeur de pain monte le long du muret.",
        "narrateur|Le bitume fume un peu, encore mouillé.",
        "narrateur|La grille de l'école brille, un peu froide.",
        "papa|Le boulanger a déjà ouvert, Aniss.",
        "maman|Ton moulin de papier dépasse du sac.",
        "narrateur|En ce moment, Aniss tient le bâton du moulin.",
        "enfant-m|Il tourne.",
        "papa|Mila arrive, tu lui montres ?",
        "narrateur|Aniss hoche la tête, tout petit.",
        "narrateur|Les bottes de Mila tapent le bitume, derrière.",
        "copine|Dis tourne !",
        "narrateur|Aniss tend le moulin, sans un mot.",
        "maman|Tu peux lui tendre le papier.",
        "papa|Merci, tu as tenu le moulin droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le moulin reste froid, près des pieds.",
        "narrateur|Un fil beige brille, encore roulé.",
        "narrateur|Un caillou, puis le papier, à côté.",
        "papa|Tu prends quoi d'abord, Aniss ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le moulin", "le fil", "le caillou")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Aniss a tendu {o['t1q']}, tout près.",
            "maman|Il tend quoi, à Mila ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1ans"], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la grille", "le caniveau", "le porche")

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
        "Aniss veut planter son moulin de papier dans la grille de l'école. "
        "T1 = moulin / fil / caillou (les trois partent). "
        "T2 = grille (barreaux trop serrés) / caniveau (eau trop vite) / "
        "porche (air trop calme). "
        "T3 = neuf résolutions (bas, tendre le moulin, crochet ; "
        "dalle, fil, bord ; vent, mains de Mila, nœud). "
        "Aniss répond avec les mains, sans étiquette. Mila attend, tend. "
        "Fin : le moulin tourne, on entre.",
        "Gabarit Lila / cuisine-jardin-chambre / slogan PAR jeté. "
        "Autre récit que DIF-017 (locomotive), DIF-027 (cuillères, véranda), "
        "DIF-037 (panier, petite roue), DIF-045 (galet, poisson) et "
        "DIF-053 (nichoir, merle). "
        "Chemin d'école, pas cloche ni soleil en papier (DIF-034). "
        "Héros Aniss (peu de mots, vécu). Copine Mila. Lila hors troupe. "
        "Fins caniveau et porche ramènent à la grille. "
        "Désir ≠ leçon. N3 ≤ 16. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
