#!/usr/bin/env python3
"""TREE-DIF-037 — Le panier d'Aniss et la petite roue de la cour (N3, DIF.PAR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-037"
N3 = 16
TITLE = "Le panier d'Aniss et la petite roue de la cour"
FIL = (
    "Aniss veut envoyer le goûter en haut, avec la petite roue de la cour. "
    "Mila arrive ; elle voudrait l'entendre crier tire, "
    "mais Aniss répond avec les mains. "
    "T1 = panier / corde / nappe, les trois partent. "
    "T2 = palier (paillasson, trop étroit) / balcon (linge, vent) / "
    "appentis (poutre trop haute). "
    "T3 = neuf façons. Mila attend, tend. Le panier arrive, on goûte, on rentre."
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
    out["setting"] = "cour, palier, balcon, appentis"
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
        "jules",
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
        "plic",
        "volet jaune",
        "locomotive",
        "gare en carton",
        "cuillère",
        "véranda",
        "fenêtre",
        "fenetre",
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
        "lab": "le panier",
        "cap": "Le panier",
        "t1q": "le panier",
        "t1acc": "panier | le panier | l'osier | osier | tendre",
        "t1retry": "Il tend le panier. Il tend quoi ?",
        "coda": "L'osier sent encore le pain tiède.",
        "voy": "Le panier voyage déjà contre la corde.",
    },
    2: {
        "lab": "la corde",
        "cap": "La corde",
        "t1q": "la corde",
        "t1acc": "corde | la corde | la roue | tendre",
        "t1retry": "Il tend la corde. Il tend quoi ?",
        "coda": "La corde garde un peu de poussière chaude.",
        "voy": "La corde voyage déjà vers la petite roue.",
    },
    3: {
        "lab": "la nappe",
        "cap": "La nappe",
        "t1q": "la nappe",
        "t1acc": "nappe | la nappe | les carreaux | tendre",
        "t1retry": "Il tend la nappe. Il tend quoi ?",
        "coda": "Un carreau de nappe garde une miette.",
        "voy": "La nappe voyage déjà, pliée dans l'osier.",
    },
}

T3_LABS = {
    1: ("le paillasson", "le panier", "la marche"),
    2: ("le vent", "la corde", "le linge"),
    3: ("le banc", "les mains de Mila", "la poutre"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss prend d'abord le panier d'osier.",
            "enfant-m|Il sent le pain.",
            "papa|L'osier est encore un peu rêche.",
            "narrateur|Il le tend vers Mila, tout près.",
            "copine|Dis goûter !",
            "narrateur|Aniss pose sa main sur le bord.",
            "narrateur|Les miettes bougent, tout petit.",
            "maman|La corde et la nappe viennent aussi.",
            "narrateur|Papa glisse le tout contre l'osier.",
            "narrateur|Rien ne reste sur les dalles.",
            "copine|Aniss, on part ?",
            "narrateur|Aniss hoche la tête, tout petit.",
            "papa|Le panier d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss prend d'abord la corde rêche.",
            "enfant-m|Elle gratte un peu.",
            "maman|La petite roue attend, tout en haut.",
            "narrateur|Il tend le bout vers Mila.",
            "copine|Dis tire !",
            "narrateur|Aniss tire une fois, sans un mot.",
            "narrateur|La roue fait tic, puis s'arrête.",
            "papa|Le panier et la nappe viennent aussi.",
            "narrateur|Maman les pose contre l'osier.",
            "narrateur|Tout part ensemble, déjà.",
            "copine|Aniss, tu viens ?",
            "narrateur|Aniss lève la corde, tout bas.",
            "maman|La corde d'abord, vous l'avez.",
        )
    return L(
        "narrateur|Aniss prend d'abord la nappe à carreaux.",
        "enfant-m|Elle a des miettes.",
        "papa|Le tissu sent encore le tiroir.",
        "narrateur|Il tend le pliage vers Mila.",
        "copine|Dis nappe !",
        "narrateur|Aniss enroule le pain, tout lent.",
        "narrateur|Le goûter se fait, sans un mot.",
        "maman|Le panier et la corde viennent aussi.",
        "narrateur|Papa les glisse près des dalles.",
        "narrateur|L'osier les garde, tous les trois.",
        "copine|Aniss, c'est bon ?",
        "narrateur|Aniss appuie sur le tissu, tout calme.",
        "papa|La nappe d'abord, elle tient.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss garde le panier contre lui.",
            "copine|Il est à toi, un moment.",
            "narrateur|Mila attend, les mains ouvertes.",
            "narrateur|Un tic se fait, tout petit, en haut.",
            "maman|L'osier est tiède, maintenant.",
            "papa|On envoie le goûter où ?",
            "copine|Vers le palier, peut-être.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss garde la corde contre sa jambe.",
            "copine|Elle est à toi, un moment.",
            "narrateur|Mila attend, sans répéter.",
            "narrateur|La poussière sent encore le mur chaud.",
            "maman|La petite roue peut tourner, après.",
            "papa|On envoie le goûter où ?",
            "copine|Vers le balcon, peut-être.",
        )
    return L(
        "narrateur|Aniss tient encore la nappe, tout près.",
        "copine|Elle est à toi, un moment.",
        "narrateur|Mila attend, les lèvres fermées.",
        "narrateur|Un carreau bouge un peu, puis s'arrête.",
        "papa|L'ombre de l'appentis va le voir.",
        "maman|On envoie le goûter où ?",
        "copine|Vers l'appentis, tout doux.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|La petite roue peut aller en trois coins.",
        "narrateur|Au palier, un paillasson barre le passage.",
        "narrateur|Au balcon, le linge claque déjà.",
        "narrateur|Vers l'appentis, une poutre attend trop haut.",
        "papa|On commence où, pour le goûter ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = {
            1: "narrateur|Le panier bute contre le paillasson.",
            2: "narrateur|La corde s'accroche au paillasson rêche.",
            3: "narrateur|La nappe froisse contre le paillasson.",
        }[t1]
        return L(
            lead,
            "narrateur|Le palier est trop étroit, juste là.",
            "copine|Pousse-le, Aniss !",
            "narrateur|Aniss montre le nœud du tapis, du doigt.",
            "narrateur|Le paillasson est coincé, sous l'osier.",
            "copine|Dis-moi où !",
            "maman|Il montre déjà, avec le doigt.",
            "papa|Le tapis reste lourd, au milieu.",
            "narrateur|Aniss ouvre un peu le panier.",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le panier penche, trop loin, vers le linge.",
            2: "narrateur|La corde se coince dans une pince.",
            3: "narrateur|La nappe claque au vent, trop fort.",
        }[t1]
        return L(
            lead,
            "copine|Le vent est trop grand.",
            "narrateur|Une pince tient encore une chaussette.",
            "copine|Tire fort, Aniss !",
            "narrateur|Aniss serre la corde, tout calme.",
            "narrateur|La petite roue grince, puis s'arrête.",
            "maman|Le linge barre encore le chemin.",
            "papa|On reste près du mur, tous les deux.",
            "narrateur|Une pince brille aussi, plus bas.",
            "papa|Vous faites comment, tous les deux ?",
        )
    lead = {
        1: "narrateur|Le panier accroche la gouttière de l'appentis.",
        2: "narrateur|La corde frotte la poutre, trop haut.",
        3: "narrateur|La nappe se prend dans le bois sec.",
    }[t1]
    return L(
        lead,
        "copine|C'est trop haut, Aniss !",
        "narrateur|Mila lève les talons, trop petite.",
        "copine|Dis monte !",
        "narrateur|Aniss pointe le banc, du doigt.",
        "narrateur|Le bois de l'appentis reste trop loin.",
        "maman|Tes bras vont plus loin, Aniss.",
        "papa|Le banc dort près du mur.",
        "narrateur|Une feuille sèche attend sur la poutre.",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le paillasson reste fermé, trop lourd.",
            "papa|Le paillasson, le panier, ou la marche ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le vent tient encore le linge.",
            "maman|Le vent, la corde, ou le linge ?",
        )
    return L(
        "narrateur|La poutre reste trop haute, encore.",
        "papa|Le banc, les mains, ou la poutre ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le panier attend près du nœud.",
            2: "narrateur|La corde attend près du nœud.",
            3: "narrateur|La nappe attend près du nœud.",
        }[t1]
        return L(
            "copine|On attend.",
            "narrateur|Aniss tire le paillasson, tout lent.",
            "narrateur|Le nœud s'ouvre, enfin, un peu.",
            wait,
            "narrateur|Aniss pousse l'osier vers le palier.",
            "narrateur|Ça fait tic, tout net, en haut.",
            "copine|Tic.",
            "papa|Le tapis n'est plus un bouchon.",
            "maman|Vous avez laissé le temps au tapis.",
        )
    if t2 == 1 and t3 == 2:
        hold = {
            1: "narrateur|Le panier glisse vers les mains de Mila.",
            2: "narrateur|La corde guide l'osier vers Mila.",
            3: "narrateur|La nappe suit l'osier vers Mila.",
        }[t1]
        return L(
            "copine|Pour toi.",
            "narrateur|Mila tend les deux mains, tout près.",
            "narrateur|Aniss pose l'osier contre ses paumes.",
            hold,
            "narrateur|Le palier redevient libre, tout doux.",
            "copine|Il passe !",
            "maman|Le goûter a pris le bord, tout seul.",
            "papa|Tes mains ont trouvé l'osier.",
        )
    if t2 == 1 and t3 == 3:
        step = {
            1: "narrateur|Le panier attend sur la marche.",
            2: "narrateur|La corde attend sur la marche.",
            3: "narrateur|La nappe attend sur la marche.",
        }[t1]
        return L(
            "copine|La marche, Aniss.",
            "narrateur|Aniss pose l'osier dessus, sans un mot.",
            "narrateur|Mila attend, puis suit sa main.",
            step,
            "narrateur|Ils le poussent, ensuite, vers le palier.",
            "copine|Merci.",
            "papa|La marche a gardé le calme.",
            "maman|Le paillasson peut dormir, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        wind = {
            1: "narrateur|Le panier attend au calme, contre le mur.",
            2: "narrateur|La corde retombe, enfin, contre le mur.",
            3: "narrateur|La nappe retombe, enfin, contre le mur.",
        }[t1]
        return L(
            "copine|On attend le vent.",
            "narrateur|Aniss s'assoit près du mur, tout calme.",
            "narrateur|Mila s'assoit aussi, les genoux contre lui.",
            wind,
            "narrateur|Le vent tombe, une chaussette s'arrête.",
            "copine|Maintenant.",
            "papa|La petite roue ne grince plus.",
            "maman|Vous avez laissé le vent finir.",
        )
    if t2 == 2 and t3 == 2:
        rope = {
            1: "narrateur|Le panier monte au bout de la corde.",
            2: "narrateur|La corde part au bout des mains de Mila.",
            3: "narrateur|La nappe monte au bout de la corde.",
        }[t1]
        return L(
            "copine|Tes mains, Aniss.",
            "narrateur|Aniss tend la corde, tout près.",
            "narrateur|Mila tire avec lui, tout lent.",
            rope,
            "narrateur|La petite roue traverse comme un pont.",
            "copine|On tient ensemble.",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|Le linge restera après.",
        )
    if t2 == 2 and t3 == 3:
        cloth = {
            1: "narrateur|Le panier passe, dès que le linge part.",
            2: "narrateur|La corde se libère, dès que le linge part.",
            3: "narrateur|La nappe se libère, dès que le linge part.",
        }[t1]
        return L(
            "copine|Le linge, d'abord.",
            "narrateur|Mila tend la pince vers Aniss.",
            "narrateur|Aniss l'ouvre, tout lent, sans un mot.",
            cloth,
            "narrateur|La chaussette rejoint le panier à linge.",
            "copine|C'est doux.",
            "maman|Le vent garde son souffle, plus loin.",
            "papa|Le linge a laissé la corde.",
        )
    if t2 == 3 and t3 == 1:
        bench = {
            1: "narrateur|Le panier monte avec le banc.",
            2: "narrateur|La corde monte avec le banc.",
            3: "narrateur|La nappe monte avec le banc.",
        }[t1]
        return L(
            "copine|Le banc, dessous.",
            "papa|Je vous le tends, à votre hauteur.",
            "narrateur|Aniss monte, Mila tend l'osier.",
            bench,
            "narrateur|Aniss accroche, tout doux, sans parler.",
            "copine|Ça tient !",
            "papa|Le bois a tenu le banc.",
            "maman|Aniss a poussé tout doux.",
        )
    if t2 == 3 and t3 == 2:
        hands = {
            1: "narrateur|Le panier part au bout des mains de Mila.",
            2: "narrateur|La corde part au bout des mains de Mila.",
            3: "narrateur|La nappe part au bout des mains de Mila.",
        }[t1]
        return L(
            "enfant-m|Mila.",
            "narrateur|Aniss pointe ses paumes, du doigt.",
            "narrateur|Mila attend, puis ouvre les mains.",
            hands,
            "narrateur|L'osier glisse, tout net, vers elle.",
            "copine|Je le tiens.",
            "maman|Le haut garde son ombre, plus loin.",
            "papa|Tes mains ont guidé le goûter.",
        )
    beam = {
        1: "narrateur|Le panier suit la poutre, bois après bois.",
        2: "narrateur|La corde court le long de la poutre, au calme.",
        3: "narrateur|La nappe tient derrière la poutre, tout droit.",
    }[t1]
    return L(
        "copine|La poutre, Aniss.",
        "narrateur|Aniss pointe l'ombre, du doigt.",
        "narrateur|Mila attend, puis suit le doigt.",
        beam,
        "narrateur|L'osier prend le chemin du calme.",
        "copine|Il évite la gouttière.",
        "papa|Le bois a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le panier pose une miette sur le palier.",
            "enfant-m|Pain.",
            "copine|Il est arrivé.",
            "papa|Le paillasson a laissé le passage.",
            "maman|Le goûter est prêt, tout près.",
            "narrateur|Aniss pose encore une main sur l'osier.",
            coda,
            "narrateur|Une miette dorée attend sur le tapis.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|L'osier a contourné le tapis, jusqu'au bout.",
            "copine|Aniss l'a tendu, tout seul.",
            "papa|Tu as tendu, d'abord.",
            "maman|Venez, le pain est encore tiède.",
            coda,
            "narrateur|Aniss s'assoit près du panier.",
            "enfant-m|Tiens.",
            "narrateur|La sandale de Mila reste sur la marche.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|L'osier court jusqu'au palier, tout droit.",
            "copine|On a posé le panier.",
            "papa|Le calme est rentré à sa place.",
            "maman|Essuyez vos mains, tout doux.",
            coda,
            "narrateur|Aniss tapote l'osier, tout léger.",
            "narrateur|Le bois a un peu de poussière.",
            "narrateur|Le pain fume encore, tout près.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|La petite roue glisse, puis s'arrête.",
            "copine|On a attendu le vent.",
            "papa|Le linge n'a plus pris vos bras.",
            "maman|Rentrez la pince, après le goûter.",
            coda,
            "enfant-m|Tic.",
            "narrateur|Une chaussette se tait, puis l'autre.",
            "narrateur|Le balcon redevient calme, autour du mur.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La petite roue tient la corde, tout net.",
            "copine|On tenait, tous les deux.",
            "papa|Je remporte la pince, tout à l'heure.",
            "maman|Le pain vous attend.",
            coda,
            "narrateur|Aniss essuie une main sur son pantalon.",
            "narrateur|Un grain de poussière reste sur l'osier.",
            "narrateur|La corde sent encore le vent chaud.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains d'Aniss laissent la corde monter.",
            "copine|C'était plus facile, là.",
            "papa|Tes bras ont guidé l'osier.",
            "maman|Le haut gardera son ombre.",
            coda,
            "narrateur|Aniss pose un doigt sur une pince.",
            "narrateur|Elle bouge, tout petit.",
            "narrateur|Un rai de soleil barre encore le mur.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|L'osier pose une feuille sèche sur le banc.",
            "copine|On a monté, Aniss.",
            "papa|Le bois n'a pas glissé.",
            "maman|Rentrez, le seuil est sec.",
            coda,
            "narrateur|Aniss pose une feuille sur le banc.",
            "narrateur|La feuille ne bouge plus.",
            "narrateur|Une goutte sèche déjà sur l'osier.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Les mains de Mila laissent l'osier poser.",
            "copine|On l'a tenu, tous les deux.",
            "papa|Le haut est resté à sa place.",
            "maman|Essuie tes chaussures, Aniss.",
            coda,
            "narrateur|Aniss souffle un peu sur le pain.",
            "narrateur|Une miette blanchit, puis s'arrête.",
            "narrateur|La résine colle encore, derrière la porte.",
        )
    return L(
        "narrateur|L'osier suit la poutre, jusqu'au calme.",
        "copine|L'ombre était douce.",
        "papa|Le bois a tenu, tout droit.",
        "maman|Le vent n'a plus rien à dire.",
        coda,
        "narrateur|Aniss touche la corde, un instant.",
        "narrateur|Une miette revient contre le bois.",
        "narrateur|Une abeille passe, puis la cour se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "oiseau"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Les dalles de la cour sont encore chaudes.",
        "narrateur|Une petite roue grince, tout en haut.",
        "narrateur|La corde pend, un peu rêche, contre le mur.",
        "papa|Ça sent le pain, Aniss.",
        "maman|Le goûter attend, dans le panier.",
        "narrateur|Des miettes dorment déjà sur la nappe.",
        "narrateur|En ce moment, Aniss serre l'osier.",
        "enfant-m|Il va monter.",
        "papa|Avec Mila, tout à l'heure ?",
        "narrateur|Aniss hoche la tête, tout petit.",
        "narrateur|Les sandales de Mila tapent l'escalier.",
        "copine|Dis tire !",
        "narrateur|Aniss tend la corde, sans un mot.",
        "maman|Tu peux lui tendre le panier.",
        "papa|Merci, tu as tenu l'osier droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le panier reste ouvert, près des pieds.",
        "narrateur|Une corde y brille, encore rêche.",
        "narrateur|Une nappe, puis l'osier, à côté.",
        "papa|Tu prends quoi d'abord, Aniss ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le panier", "la corde", "la nappe")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Aniss a tendu {o['t1q']}, tout près.",
            "maman|Il tend quoi, à Mila ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le palier", "le balcon", "l'appentis")

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
        "Aniss veut envoyer le goûter en haut, avec la petite roue de la cour. "
        "T1 = panier / corde / nappe (les trois partent). "
        "T2 = palier (paillasson, trop étroit) / balcon (linge, vent) / "
        "appentis (poutre trop haute). "
        "T3 = neuf résolutions (paillasson, tendre le panier, marche ; "
        "vent, corde, linge ; banc, mains de Mila, poutre). "
        "Aniss répond avec les mains, sans étiquette. Mila attend, tend. "
        "Fin : le panier arrive, on goûte, on rentre.",
        "Gabarit Jules / fenêtre / cuisine-jardin-chambre / slogan PAR jeté. "
        "Autre récit que DIF-017 (locomotive) et DIF-027 (cuillères, véranda). "
        "Héros Aniss (peu de mots, vécu). Copine Mila. Jules hors troupe. "
        "Désir ≠ leçon. N3 ≤ 16. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
