#!/usr/bin/env python3
"""TREE-DIF-045 — Le galet peint d'Aniss et le poisson de la classe (N3, DIF.PAR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-045"
N3 = 16
TITLE = "Le galet peint d'Aniss et le poisson de la classe"
FIL = (
    "Aniss veut poser son galet peint dans le bac à poisson de la classe. "
    "Sarah arrive ; elle voudrait l'entendre crier plouf, "
    "mais Aniss répond avec les mains. "
    "T1 = galet / épuisette / torchon, les trois partent. "
    "T2 = bac (verre trop haut) / évier (eau trop vite) / "
    "bac à sable de la cour (bleu mêlé). "
    "T3 = neuf façons. Sarah attend, tend. Le galet est au fond, "
    "le poisson tourne, on rentre."
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
    out["characters"] = "Aniss, Sarah, papa, maman"
    out["setting"] = "école : classe, bac à poisson, évier, bac à sable de la cour"
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
        "noé",
        "noe ",
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
        "plic",
        "volet jaune",
        "locomotive",
        "gare en carton",
        "cuillère",
        "véranda",
        "petite roue",
        "coquillage",
        "soleil en papier",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
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
        "lab": "le galet",
        "cap": "Le galet",
        "t1q": "le galet",
        "t1ans": "galet",
        "t1acc": "galet | le galet | le bleu | tendre",
        "t1retry": "Il tend le galet. Il tend quoi ?",
        "coda": "Le bleu garde une goutte, tout au fond.",
        "voy": "Le galet voyage déjà contre le verre.",
    },
    2: {
        "lab": "l'épuisette",
        "cap": "L'épuisette",
        "t1q": "l'épuisette",
        "t1ans": "épuisette",
        "t1acc": "épuisette | l'épuisette | le filet | tendre",
        "t1retry": "Il tend l'épuisette. Il tend quoi ?",
        "coda": "L'épuisette sent encore l'eau tiède.",
        "voy": "L'épuisette voyage déjà vers le bac.",
    },
    3: {
        "lab": "le torchon",
        "cap": "Le torchon",
        "t1q": "le torchon",
        "t1ans": "torchon",
        "t1acc": "torchon | le torchon | les carreaux | tendre",
        "t1retry": "Il tend le torchon. Il tend quoi ?",
        "coda": "Un carreau de torchon reste un peu humide.",
        "voy": "Le torchon voyage déjà, plié sur le galet.",
    },
}

T3_LABS = {
    1: ("la chaise", "les mains de Sarah", "le marchepied"),
    2: ("l'eau", "l'épuisette", "le robinet"),
    3: ("le tamis", "les mains de Sarah", "le seau"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss prend d'abord le galet peint.",
            "enfant-m|Il est froid.",
            "papa|Le bleu tient encore un peu de craie.",
            "narrateur|Il le tend vers Sarah, tout près.",
            "copine|Dis plouf !",
            "narrateur|Aniss pose sa main sur la pierre.",
            "narrateur|Un grain de craie tombe, tout petit.",
            "maman|L'épuisette et le torchon viennent aussi.",
            "narrateur|Papa glisse le tout contre le bac.",
            "narrateur|Rien ne reste sur le papier.",
            "copine|Aniss, on part ?",
            "narrateur|Aniss hoche la tête, tout petit.",
            "papa|Le galet d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss prend d'abord l'épuisette ronde.",
            "enfant-m|Elle est mouillée.",
            "maman|Le filet sent encore le bac.",
            "narrateur|Il tend le manche vers Sarah.",
            "copine|Dis filet !",
            "narrateur|Aniss secoue une goutte, sans un mot.",
            "narrateur|La goutte tombe, puis s'arrête.",
            "papa|Le galet et le torchon viennent aussi.",
            "narrateur|Maman les pose contre le filet.",
            "narrateur|Tout part ensemble, déjà.",
            "copine|Aniss, tu viens ?",
            "narrateur|Aniss lève l'épuisette, tout bas.",
            "maman|L'épuisette d'abord, vous l'avez.",
        )
    return L(
        "narrateur|Aniss prend d'abord le torchon à carreaux.",
        "enfant-m|Il sent le savon.",
        "papa|Le tissu a séché près de l'évier.",
        "narrateur|Il tend le pliage vers Sarah.",
        "copine|Dis essuie !",
        "narrateur|Aniss enroule le galet, tout lent.",
        "narrateur|Le bleu se cache, sans un mot.",
        "maman|Le galet et l'épuisette viennent aussi.",
        "narrateur|Papa les glisse près des tables.",
        "narrateur|Le torchon les garde, tous les trois.",
        "copine|Aniss, c'est bon ?",
        "narrateur|Aniss appuie sur le tissu, tout calme.",
        "papa|Le torchon d'abord, il tient.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss garde le galet contre lui.",
            "copine|Il est à toi, un moment.",
            "narrateur|Sarah attend, les mains ouvertes.",
            "narrateur|Une bulle se fait, toute petite, dans le bac.",
            "maman|Le bleu est tiède, maintenant.",
            "papa|On pose le galet où ?",
            "copine|Vers le bac, peut-être.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss garde l'épuisette contre sa jambe.",
            "copine|Elle est à toi, un moment.",
            "narrateur|Sarah attend, sans répéter.",
            "narrateur|Le filet sent encore l'eau du bac.",
            "maman|Le poisson peut tourner, après.",
            "papa|On pose le galet où ?",
            "copine|Vers l'évier, peut-être.",
        )
    return L(
        "narrateur|Aniss tient encore le torchon, tout près.",
        "copine|Il est à toi, un moment.",
        "narrateur|Sarah attend, les lèvres fermées.",
        "narrateur|Un carreau bouge un peu, puis s'arrête.",
        "papa|Le sable de la cour attend, dehors.",
        "maman|On pose le galet où ?",
        "copine|Vers le sable, tout doux.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Le poisson peut attendre en trois coins.",
        "narrateur|Au bac, le verre est trop haut.",
        "narrateur|À l'évier, l'eau court trop vite.",
        "narrateur|Vers le bac à sable, le bleu se mélange.",
        "papa|On commence où, pour le poisson ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = {
            1: "narrateur|Le galet bute contre le verre trop haut.",
            2: "narrateur|L'épuisette n'atteint pas l'eau du bac.",
            3: "narrateur|Le torchon glisse sur le bord du bac.",
        }[t1]
        return L(
            lead,
            "narrateur|Le bac est trop haut, juste là.",
            "copine|Monte-le, Aniss !",
            "narrateur|Aniss montre le pied du bac, du doigt.",
            "narrateur|Le verre reste froid, trop loin.",
            "copine|Dis-moi où !",
            "maman|Il montre déjà, avec le doigt.",
            "papa|La chaise dort près des tables.",
            "narrateur|Aniss ouvre un peu les mains.",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le galet saute sous l'eau trop vite.",
            2: "narrateur|L'épuisette se remplit trop, d'un coup.",
            3: "narrateur|Le torchon se mouille trop, tout de suite.",
        }[t1]
        return L(
            lead,
            "copine|L'eau est trop grande.",
            "narrateur|Une bulle de savon tient encore.",
            "copine|Tourne fort, Aniss !",
            "narrateur|Aniss pose la pierre, tout calme.",
            "narrateur|L'eau court, puis rebondit.",
            "maman|Le robinet barre encore le calme.",
            "papa|On reste près de l'évier, tous les deux.",
            "narrateur|Une goutte brille aussi, plus bas.",
            "papa|Vous faites comment, tous les deux ?",
        )
    lead = {
        1: "narrateur|Le galet peint tombe dans le sable beige.",
        2: "narrateur|L'épuisette ramasse trop de grains, d'un coup.",
        3: "narrateur|Le torchon se charge de sable chaud.",
    }[t1]
    return L(
        lead,
        "copine|C'est trop mêlé, Aniss !",
        "narrateur|Sarah cherche, trop vite, trop fort.",
        "copine|Dis bleu !",
        "narrateur|Aniss pointe un grain plus foncé, du doigt.",
        "narrateur|Le bac à sable reste trop large.",
        "maman|Tes yeux vont plus loin, Aniss.",
        "papa|Le tamis dort près du seau.",
        "narrateur|Un caillou beige attend, trop clair.",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le verre reste trop haut, encore.",
            "papa|La chaise, les mains, ou le marchepied ?",
        )
    if t2 == 2:
        return L(
            "narrateur|L'eau tient encore le savon.",
            "maman|L'eau, l'épuisette, ou le robinet ?",
        )
    return L(
        "narrateur|Le sable reste trop mêlé, encore.",
        "papa|Le tamis, les mains, ou le seau ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le galet attend près du dossier.",
            2: "narrateur|L'épuisette attend près du dossier.",
            3: "narrateur|Le torchon attend près du dossier.",
        }[t1]
        return L(
            "copine|On attend.",
            "narrateur|Aniss tire la chaise, tout lent.",
            "narrateur|Sarah tient le dossier, enfin, un peu.",
            wait,
            "narrateur|Aniss monte vers le bac, sans un mot.",
            "narrateur|Ça fait toc, tout net, contre le verre.",
            "copine|Toc.",
            "papa|La chaise n'est plus trop basse.",
            "maman|Vous avez laissé le temps au verre.",
        )
    if t2 == 1 and t3 == 2:
        hold = {
            1: "narrateur|Le galet glisse vers les mains de Sarah.",
            2: "narrateur|L'épuisette guide la pierre vers Sarah.",
            3: "narrateur|Le torchon suit la pierre vers Sarah.",
        }[t1]
        return L(
            "copine|Pour toi.",
            "narrateur|Sarah tend les deux mains, tout près.",
            "narrateur|Aniss pose le bleu contre ses paumes.",
            hold,
            "narrateur|Le bac redevient facile, tout doux.",
            "copine|Il passe !",
            "maman|Le galet a pris le bord, tout seul.",
            "papa|Tes mains ont trouvé le bleu.",
        )
    if t2 == 1 and t3 == 3:
        step = {
            1: "narrateur|Le galet attend sur le marchepied.",
            2: "narrateur|L'épuisette attend sur le marchepied.",
            3: "narrateur|Le torchon attend sur le marchepied.",
        }[t1]
        return L(
            "copine|Le marchepied, Aniss.",
            "narrateur|Aniss pose le bleu dessus, sans un mot.",
            "narrateur|Sarah attend, puis suit sa main.",
            step,
            "narrateur|Ils le poussent, ensuite, vers le bac.",
            "copine|Merci.",
            "papa|Le bois a gardé le calme.",
            "maman|La chaise peut dormir, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        wind = {
            1: "narrateur|Le galet attend au calme, contre l'évier.",
            2: "narrateur|L'épuisette retombe, enfin, contre l'évier.",
            3: "narrateur|Le torchon retombe, enfin, contre l'évier.",
        }[t1]
        return L(
            "copine|On attend l'eau.",
            "narrateur|Aniss s'assoit près de l'évier, tout calme.",
            "narrateur|Sarah s'assoit aussi, les genoux contre lui.",
            wind,
            "narrateur|L'eau tombe, une bulle s'arrête.",
            "copine|Maintenant.",
            "papa|Le robinet ne chante plus.",
            "maman|Vous avez laissé l'eau finir.",
        )
    if t2 == 2 and t3 == 2:
        rope = {
            1: "narrateur|Le galet descend au bout du filet.",
            2: "narrateur|L'épuisette part au bout des mains de Sarah.",
            3: "narrateur|Le torchon guide le filet, tout droit.",
        }[t1]
        return L(
            "copine|Tes mains, Aniss.",
            "narrateur|Aniss tend l'épuisette, tout près.",
            "narrateur|Sarah tire avec lui, tout lent.",
            rope,
            "narrateur|Le filet traverse comme un pont.",
            "copine|On tient ensemble.",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|L'eau restera après.",
        )
    if t2 == 2 and t3 == 3:
        cloth = {
            1: "narrateur|Le galet passe, dès que l'eau se tait.",
            2: "narrateur|L'épuisette se libère, dès que l'eau se tait.",
            3: "narrateur|Le torchon se libère, dès que l'eau se tait.",
        }[t1]
        return L(
            "copine|Le robinet, d'abord.",
            "narrateur|Sarah tend la poignée vers Aniss.",
            "narrateur|Aniss tourne, tout doux, sans un mot.",
            cloth,
            "narrateur|Une goutte rejoint le fond, tout calme.",
            "copine|C'est doux.",
            "maman|L'eau garde son souffle, plus loin.",
            "papa|Le robinet a laissé le filet.",
        )
    if t2 == 3 and t3 == 1:
        bench = {
            1: "narrateur|Le galet monte avec le tamis.",
            2: "narrateur|L'épuisette monte avec le tamis.",
            3: "narrateur|Le torchon monte avec le tamis.",
        }[t1]
        return L(
            "copine|Le tamis, dessous.",
            "papa|Je vous le tends, à votre hauteur.",
            "narrateur|Aniss secoue, Sarah tend le bleu.",
            bench,
            "narrateur|Aniss souffle le sable, tout doux, sans parler.",
            "copine|Ça tient !",
            "papa|Le métal a tenu le tamis.",
            "maman|Aniss a poussé tout doux.",
        )
    if t2 == 3 and t3 == 2:
        hands = {
            1: "narrateur|Le galet part au bout des mains de Sarah.",
            2: "narrateur|L'épuisette part au bout des mains de Sarah.",
            3: "narrateur|Le torchon part au bout des mains de Sarah.",
        }[t1]
        return L(
            "enfant-m|Sarah.",
            "narrateur|Aniss pointe ses paumes, du doigt.",
            "narrateur|Sarah attend, puis ouvre les mains.",
            hands,
            "narrateur|Le bleu glisse, tout net, vers elle.",
            "copine|Je le tiens.",
            "maman|Le sable garde son ombre, plus loin.",
            "papa|Tes mains ont guidé le galet.",
        )
    beam = {
        1: "narrateur|Le galet suit le seau, grain après grain.",
        2: "narrateur|L'épuisette court le long du seau, au calme.",
        3: "narrateur|Le torchon tient derrière le seau, tout droit.",
    }[t1]
    return L(
        "copine|Le seau, Aniss.",
        "narrateur|Aniss pointe le fond, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        beam,
        "narrateur|Le bleu prend le chemin du calme.",
        "copine|Il évite le beige.",
        "papa|Le seau a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le galet pose une bulle sur le verre.",
            "enfant-m|Poisson.",
            "copine|Il est arrivé.",
            "papa|La chaise a laissé le passage.",
            "maman|Le bac est prêt, tout près.",
            "narrateur|Aniss pose encore une main sur le bord.",
            coda,
            "narrateur|Une écaille d'or tourne autour du bleu.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le bleu a contourné le verre, jusqu'au fond.",
            "copine|Aniss l'a tendu, tout seul.",
            "papa|Tu as tendu, d'abord.",
            "maman|Venez, le poisson est encore calme.",
            coda,
            "narrateur|Aniss s'assoit près du bac.",
            "enfant-m|Tiens.",
            "narrateur|La sandale de Sarah reste sous la table.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le bleu court jusqu'au fond, tout droit.",
            "copine|On a posé le galet.",
            "papa|Le marchepied a tenu, tout droit.",
            "maman|Essuyez vos mains, tout doux.",
            coda,
            "narrateur|Aniss descend, un pied après l'autre.",
            "narrateur|Le bois du marchepied reste un peu froid.",
            "narrateur|Le poisson pousse une bulle, tout près.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Une goutte glisse, puis s'arrête.",
            "copine|On a attendu l'eau.",
            "papa|Le savon n'a plus pris vos bras.",
            "maman|Rentrez le torchon, après le bac.",
            coda,
            "enfant-m|Toc.",
            "narrateur|Une bulle se tait, puis l'autre.",
            "narrateur|L'évier redevient calme, autour du bac.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le filet tient le galet, tout net.",
            "copine|On tenait, tous les deux.",
            "papa|Je remporte l'épuisette, tout à l'heure.",
            "maman|Le poisson vous attend.",
            coda,
            "narrateur|Aniss essuie une main sur son pantalon.",
            "narrateur|Un grain de craie reste sur le filet.",
            "narrateur|L'eau sent encore le savon tiède.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains d'Aniss laissent le bleu descendre.",
            "copine|C'était plus facile, là.",
            "papa|Tes bras ont guidé le galet.",
            "maman|Le fond gardera son ombre.",
            coda,
            "narrateur|Aniss pose un doigt sur le robinet.",
            "narrateur|Il bouge, tout petit.",
            "narrateur|Un rai de soleil barre encore l'évier.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le bleu rejoint le bac, tout propre.",
            "copine|On a trouvé, Aniss.",
            "papa|Le tamis n'a pas glissé.",
            "maman|Rentrez, le seuil est sec.",
            coda,
            "narrateur|Aniss pose un grain beige sur le seau.",
            "narrateur|Le grain ne bouge plus.",
            "narrateur|Une goutte sèche déjà sur le verre.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Les mains de Sarah laissent le bleu au fond.",
            "copine|On l'a tenu, tous les deux.",
            "papa|Le sable est resté à sa place.",
            "maman|Essuie tes chaussures, Aniss.",
            coda,
            "narrateur|Aniss souffle un peu sur le verre.",
            "narrateur|Un grain blanchit, puis s'arrête.",
            "narrateur|La craie colle encore, derrière la porte.",
        )
    return L(
        "narrateur|Le bleu suit le seau, jusqu'au bac.",
        "copine|L'ombre était douce.",
        "papa|Le seau a tenu, tout droit.",
        "maman|Le sable n'a plus rien à dire.",
        coda,
        "narrateur|Aniss touche le verre, un instant.",
        "narrateur|Une bulle revient contre le bleu.",
        "narrateur|Un oiseau passe, puis la classe se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "eau"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le bac à poisson bourdonne, tout bas.",
        "narrateur|Une bulle monte, puis une autre.",
        "narrateur|La classe sent la terre mouillée, encore.",
        "papa|Le poisson tourne, Aniss.",
        "maman|Ton galet peint sèche sur le papier.",
        "narrateur|En ce moment, Aniss serre le galet bleu.",
        "enfant-m|Pour lui.",
        "papa|Avec Sarah, tout à l'heure ?",
        "narrateur|Aniss hoche la tête, tout petit.",
        "narrateur|Les sandales de Sarah tapent le linoléum.",
        "copine|Dis plouf !",
        "narrateur|Aniss tend le galet, sans un mot.",
        "maman|Tu peux lui tendre le bleu.",
        "papa|Merci, tu as tenu le galet droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le galet reste froid, près des pieds.",
        "narrateur|Une épuisette brille, encore ronde.",
        "narrateur|Un torchon, puis le bleu, à côté.",
        "papa|Tu prends quoi d'abord, Aniss ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le galet", "l'épuisette", "le torchon")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Aniss a tendu {o['t1q']}, tout près.",
            "maman|Il tend quoi, à Sarah ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1ans"], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le bac", "l'évier", "le bac à sable")

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
        "Aniss veut poser son galet peint dans le bac à poisson de la classe. "
        "T1 = galet / épuisette / torchon (les trois partent). "
        "T2 = bac (verre trop haut) / évier (eau trop vite) / "
        "bac à sable de la cour (bleu mêlé). "
        "T3 = neuf résolutions (chaise, tendre le galet, marchepied ; "
        "eau, épuisette, robinet ; tamis, mains de Sarah, seau). "
        "Aniss répond avec les mains, sans étiquette. Sarah attend, tend. "
        "Fin : le galet est au fond, le poisson tourne, on rentre.",
        "Gabarit Noé / cuisine-jardin-chambre / slogan PAR jeté. "
        "Autre récit que DIF-017 (locomotive), DIF-027 (cuillères, véranda) "
        "et DIF-037 (panier, petite roue). "
        "Héros Aniss (peu de mots, vécu). Copine Sarah. Noé hors troupe. "
        "École, pas cloche ni soleil en papier (DIF-034). "
        "Désir ≠ leçon. N3 ≤ 16. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
