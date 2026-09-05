#!/usr/bin/env python3
"""TREE-DIF-053 — Le nichoir de Nina et le merle du pommier (N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-053"
N2 = 15
TITLE = "Le nichoir de Nina et le merle du pommier"
FIL = (
    "Nina veut accrocher son nichoir de bois dans le pommier, "
    "pour qu'un merle vienne habiter. Aniss arrive ; Nina voudrait "
    "l'entendre crier merle, mais Aniss répond avec les mains. "
    "T1 = nichoir / ficelle / graines, les trois partent. "
    "T2 = branche basse (trop bas, ça tape) / fourche (trop haute) / "
    "tronc (ficelle qui glisse). T3 = neuf façons. Nina attend, tend. "
    "Le merle vient, on rentre."
)


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
    out["characters"] = "Nina, Aniss, papa, maman"
    out["setting"] = "sous le pommier, branche, fourche, tronc"
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
        "maya",
        " parlé peu",
        "parle peu",
        "camarade",
        "timide",
        "forcer la parole",
        "il faut attendre",
        "un camarade",
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
        "cerf-volant",
        "cerf volant",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
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
        "lab": "le nichoir",
        "cap": "Le nichoir",
        "t1q": "le nichoir",
        "t1ans": "nichoir",
        "t1acc": "nichoir | le nichoir | le bois | tendre",
        "t1retry": "Elle tend le nichoir. Elle tend quoi ?",
        "coda": "Un copeau de bois brille encore sur le toit.",
        "voy": "Le nichoir voyage déjà dans le panier.",
    },
    2: {
        "lab": "la ficelle",
        "cap": "La ficelle",
        "t1q": "la ficelle",
        "t1ans": "ficelle",
        "t1acc": "ficelle | la ficelle | le fil | tendre",
        "t1retry": "Elle tend la ficelle. Elle tend quoi ?",
        "coda": "Un bout de ficelle pend, tout calme.",
        "voy": "La ficelle voyage déjà dans le panier.",
    },
    3: {
        "lab": "les graines",
        "cap": "Les graines",
        "t1q": "les graines",
        "t1ans": "graines",
        "t1acc": "graines | les graines | le sachet | tendre",
        "t1retry": "Elle tend les graines. Elle tend quoi ?",
        "coda": "Une graine reste collée au bois, toute ronde.",
        "voy": "Les graines voyagent déjà dans le panier.",
    },
}

T3_LABS = {
    1: ("la branche", "le nichoir", "le tabouret"),
    2: ("le vent", "la ficelle", "les mains"),
    3: ("le nœud", "la pince", "la fourche"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina prend d'abord le nichoir de bois.",
            "enfant-f|Il sent la résine.",
            "papa|Le toit est un peu rêche, encore.",
            "narrateur|Elle le tend vers Aniss, tout près.",
            "enfant-f|Dis merle !",
            "narrateur|Aniss pose deux doigts sur le toit.",
            "narrateur|Un copeau tombe, tout petit.",
            "maman|La ficelle et les graines viennent aussi.",
            "narrateur|Papa glisse le tout dans le panier.",
            "narrateur|Le panier tient les trois, déjà.",
            "enfant-f|Aniss, on part ?",
            "narrateur|Aniss appuie le toit, tout petit.",
            "papa|Le nichoir d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina prend d'abord la ficelle beige.",
            "enfant-f|Elle gratte un peu.",
            "maman|Le fil sent encore le tiroir.",
            "narrateur|Elle tend la bobine vers Aniss.",
            "enfant-f|Dis nœud !",
            "narrateur|Aniss enroule un tour, sans un mot.",
            "narrateur|La bobine s'arrête, toute calme.",
            "papa|Le nichoir et les graines viennent aussi.",
            "narrateur|Maman les pose contre le bois.",
            "narrateur|Tout part ensemble, déjà.",
            "enfant-f|Aniss, tu viens ?",
            "narrateur|Aniss lève la ficelle, tout bas.",
            "maman|La ficelle d'abord, vous l'avez.",
        )
    return L(
        "narrateur|Nina prend d'abord le sachet de graines.",
        "enfant-f|Ça sent le tournesol.",
        "papa|Une graine brille encore, toute ronde.",
        "narrateur|Elle tend le sachet vers Aniss.",
        "enfant-f|Dis miam !",
        "narrateur|Aniss en prend une, tout lent.",
        "narrateur|Il la pose dans le nichoir, sans un mot.",
        "maman|Le nichoir et la ficelle viennent aussi.",
        "narrateur|Papa les glisse près du tronc.",
        "narrateur|Le sachet les garde, tous les trois.",
        "enfant-f|Aniss, c'est bon ?",
        "narrateur|Aniss appuie sur le papier, tout calme.",
        "papa|Les graines d'abord, elles tiennent.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss garde le nichoir contre lui.",
            "enfant-f|Il est à toi, un moment.",
            "narrateur|Nina attend, les mains ouvertes.",
            "narrateur|Un merle passe, tout petit, au-dessus.",
            "maman|Le bois est tiède, maintenant.",
            "papa|On pose le nichoir où ?",
            "enfant-f|Vers le pommier.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss garde la ficelle contre sa jambe.",
            "enfant-f|Elle est à toi, un moment.",
            "narrateur|Nina attend, sans répéter.",
            "narrateur|Le fil sent encore le tiroir.",
            "maman|Le merle peut venir, après.",
            "papa|On pose le nichoir où ?",
            "enfant-f|Vers la fourche, peut-être.",
        )
    return L(
        "narrateur|Aniss tient encore le sachet, tout près.",
        "enfant-f|Il est à toi, un moment.",
        "narrateur|Nina attend, les lèvres fermées.",
        "narrateur|Une graine bouge un peu, puis s'arrête.",
        "papa|Le tronc du pommier attend, dehors.",
        "maman|On pose le nichoir où ?",
        "enfant-f|Vers le tronc, tout doux.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Le pommier ouvre trois places.",
        "narrateur|La branche basse tape l'herbe.",
        "maman|La fourche est trop haute, encore.",
        "narrateur|Le tronc fait glisser la ficelle.",
        "papa|On commence où, pour le merle ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = {
            1: "narrateur|Le nichoir tape déjà l'herbe, trop bas.",
            2: "narrateur|La ficelle traîne dans l'herbe, trop bas.",
            3: "narrateur|Les graines tombent trop près de l'herbe.",
        }[t1]
        cry = {
            1: "enfant-f|Monte-le, Aniss !",
            2: "enfant-f|Tire-la, Aniss !",
            3: "enfant-f|Pose-les, Aniss !",
        }[t1]
        return L(
            lead,
            "narrateur|La branche basse penche trop, juste là.",
            cry,
            "narrateur|Aniss montre une branche plus haute, du doigt.",
            "narrateur|Le bois reste trop près de l'herbe.",
            "enfant-f|Dis-moi où !",
            "maman|Il montre déjà, avec le doigt.",
            "papa|Le tabouret dort près du tronc.",
            "narrateur|Aniss ouvre un peu les mains.",
            "papa|On le monte comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le nichoir n'atteint pas la fourche.",
            2: "narrateur|La ficelle n'atteint pas la fourche.",
            3: "narrateur|Les graines n'arrivent pas à la fourche.",
        }[t1]
        return L(
            lead,
            "enfant-f|C'est trop haut.",
            "narrateur|Une pomme cache encore le creux.",
            "enfant-f|Jette, Aniss !",
            "narrateur|Aniss lève les bras, tout calme.",
            "narrateur|La fourche reste loin, trop loin.",
            "maman|Le vent peut pencher un peu.",
            "papa|On reste sous la fourche, tous les deux.",
            "narrateur|Une feuille brille aussi, plus haut.",
            "papa|On l'accroche comment, tous les deux ?",
        )
    lead = {
        1: "narrateur|Le nichoir glisse le long du tronc.",
        2: "narrateur|La ficelle glisse le long du tronc.",
        3: "narrateur|Les graines tombent le long du tronc.",
    }[t1]
    return L(
        lead,
        "enfant-f|Ça glisse, Aniss !",
        "narrateur|Nina serre trop vite, trop fort.",
        "enfant-f|Dis nœud !",
        "narrateur|Aniss pointe l'écorce lisse, du doigt.",
        "narrateur|Le tronc reste trop lisse, encore.",
        "maman|Tes doigts vont plus lentement, Aniss.",
        "papa|La pince dort près du panier.",
        "narrateur|Un copeau attend, trop mince.",
        "papa|On le tient comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La branche reste trop basse, encore.",
            "papa|La branche, le nichoir, ou le tabouret ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La fourche reste trop haute, encore.",
            "maman|Le vent, la ficelle, ou les mains ?",
        )
    return L(
        "narrateur|La ficelle glisse encore sur le tronc.",
        "papa|Le nœud, la pince, ou la fourche ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le nichoir attend près de l'herbe.",
            2: "narrateur|La ficelle attend près de l'herbe.",
            3: "narrateur|Les graines attendent près de l'herbe.",
        }[t1]
        return L(
            "enfant-f|On attend.",
            "narrateur|Aniss cherche, tout lent, du doigt.",
            "narrateur|Nina suit le doigt, enfin, un peu.",
            wait,
            "narrateur|Aniss montre une branche plus haute.",
            "narrateur|Ça fait toc, tout net, contre le bois.",
            "copain|Toc.",
            "papa|La branche n'est plus trop basse.",
            "maman|Vous avez laissé le temps au merle.",
        )
    if t2 == 1 and t3 == 2:
        hold = {
            1: "narrateur|Le nichoir glisse vers les mains d'Aniss.",
            2: "narrateur|La ficelle guide le bois vers Aniss.",
            3: "narrateur|Les graines suivent le bois vers Aniss.",
        }[t1]
        return L(
            "enfant-f|Pour toi.",
            "narrateur|Nina tend les deux mains, tout près.",
            "narrateur|Aniss pose le bois contre ses paumes.",
            hold,
            "narrateur|La branche redevient facile, tout doux.",
            "enfant-f|Il passe !",
            "maman|Le nichoir a pris le bois, tout seul.",
            "papa|Tes mains ont trouvé la place.",
        )
    if t2 == 1 and t3 == 3:
        step = {
            1: "narrateur|Le nichoir attend sur le tabouret.",
            2: "narrateur|La ficelle attend sur le tabouret.",
            3: "narrateur|Les graines attendent sur le tabouret.",
        }[t1]
        return L(
            "enfant-f|Le tabouret, Aniss.",
            "narrateur|Aniss pose le bois dessus, sans un mot.",
            "narrateur|Nina attend, puis suit sa main.",
            step,
            "narrateur|Ils le poussent, ensuite, vers la branche.",
            "enfant-f|Merci.",
            "papa|Le bois a gardé le calme.",
            "maman|L'herbe peut dormir, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        wind = {
            1: "narrateur|Le nichoir attend au calme, sous la fourche.",
            2: "narrateur|La ficelle retombe, enfin, sous la fourche.",
            3: "narrateur|Les graines restent, enfin, sous la fourche.",
        }[t1]
        return L(
            "enfant-f|On attend le vent.",
            "narrateur|Aniss s'assoit dans l'herbe, tout calme.",
            "narrateur|Nina s'assoit aussi, les genoux contre lui.",
            wind,
            "narrateur|Le vent penche, une pomme s'arrête.",
            "enfant-f|Maintenant.",
            "papa|La fourche n'est plus trop loin.",
            "maman|Vous avez laissé le vent finir.",
        )
    if t2 == 2 and t3 == 2:
        rope = {
            1: "narrateur|Le nichoir monte au bout de la ficelle.",
            2: "narrateur|La ficelle part au bout des mains d'Aniss.",
            3: "narrateur|Les graines suivent le fil, tout droit.",
        }[t1]
        return L(
            "enfant-f|Tes mains, Aniss.",
            "narrateur|Aniss tend la ficelle, tout près.",
            "narrateur|Nina tire avec lui, tout lent.",
            rope,
            "narrateur|Le fil traverse comme un pont.",
            "enfant-f|On tient ensemble.",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|La fourche restera après.",
        )
    if t2 == 2 and t3 == 3:
        cloth = {
            1: "narrateur|Le nichoir passe, dès que les bras montent.",
            2: "narrateur|La ficelle se libère, dès que les bras montent.",
            3: "narrateur|Les graines se libèrent, dès que les bras montent.",
        }[t1]
        return L(
            "enfant-f|Tes bras, d'abord.",
            "narrateur|Nina tend le bois vers Aniss.",
            "narrateur|Aniss lève, tout doux, sans un mot.",
            cloth,
            "narrateur|Une pomme rejoint le creux, tout calme.",
            "enfant-f|C'est doux.",
            "maman|La fourche garde son souffle, plus loin.",
            "papa|Tes bras ont laissé le bois.",
        )
    if t2 == 3 and t3 == 1:
        bench = {
            1: "narrateur|Le nichoir tient avec le nœud.",
            2: "narrateur|La ficelle tient avec le nœud.",
            3: "narrateur|Les graines tiennent avec le nœud.",
        }[t1]
        return L(
            "enfant-f|Le nœud, dessous.",
            "papa|Je vous laisse le temps, tout près.",
            "narrateur|Aniss noue, Nina tend le bois.",
            bench,
            "narrateur|Aniss serre le fil, tout doux, sans parler.",
            "enfant-f|Ça tient !",
            "papa|Le nœud a tenu le bois.",
            "maman|Aniss a poussé tout doux.",
        )
    if t2 == 3 and t3 == 2:
        hands = {
            1: "narrateur|Le nichoir part au bout de la pince.",
            2: "narrateur|La ficelle part au bout de la pince.",
            3: "narrateur|Les graines partent au bout de la pince.",
        }[t1]
        return L(
            "copain|Pince.",
            "narrateur|Aniss pointe la pince, du doigt.",
            "narrateur|Nina attend, puis ouvre les mains.",
            hands,
            "narrateur|Le fil glisse, tout net, vers l'écorce.",
            "enfant-f|Je le tiens.",
            "maman|Le tronc garde son ombre, plus loin.",
            "papa|Tes mains ont guidé la pince.",
        )
    beam = {
        1: "narrateur|Le nichoir suit la fourche, pas à pas.",
        2: "narrateur|La ficelle court le long de la fourche.",
        3: "narrateur|Les graines tiennent derrière la fourche.",
    }[t1]
    return L(
        "enfant-f|La fourche, Aniss.",
        "narrateur|Aniss pointe le creux, du doigt.",
        "narrateur|Nina attend, puis suit le doigt.",
        beam,
        "narrateur|Le bois prend le chemin du calme.",
        "enfant-f|Il évite le tronc.",
        "papa|La fourche a montré la route.",
        "maman|Vos pieds restent dans l'herbe, aussi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le nichoir pose un toc sur la branche.",
            "copain|Toc.",
            "enfant-f|Il est arrivé.",
            "papa|La branche haute a laissé le passage.",
            "maman|Le merle peut venir, tout près.",
            "narrateur|Aniss pose encore une main sur le toit.",
            coda,
            "narrateur|Une pomme jaune tourne au-dessus du bois.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le bois a contourné l'herbe, jusqu'en haut.",
            "enfant-f|Aniss l'a posé, tout seul.",
            "papa|Tu as tendu le bois, d'abord.",
            "maman|Venez, le merle est encore calme.",
            coda,
            "narrateur|Aniss s'assoit près du tronc.",
            "copain|Merle.",
            "narrateur|L'herbe de la branche sèche déjà au soleil.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le bois court jusqu'à la branche, tout droit.",
            "enfant-f|On a posé le nichoir.",
            "papa|Le tabouret a tenu, tout droit.",
            "maman|Essuyez vos mains, tout doux.",
            coda,
            "narrateur|Aniss descend, un pied après l'autre.",
            "narrateur|Le bois du tabouret reste un peu froid.",
            "narrateur|Le merle pousse un cri, tout près.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le bois rejoint la fourche, encore léger.",
            "enfant-f|On a attendu le vent.",
            "papa|Le vent n'a plus pris vos bras.",
            "maman|Rentrez la ficelle, après le merle.",
            coda,
            "copain|Toc.",
            "narrateur|Une feuille se tait, puis l'autre.",
            "narrateur|La fourche reste calme, derrière eux.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le fil pose le nichoir dans la fourche.",
            "enfant-f|On tenait, tous les deux.",
            "papa|Je remporte la ficelle, tout à l'heure.",
            "maman|Le merle vous attend.",
            coda,
            "narrateur|Aniss essuie une main sur son pantalon.",
            "narrateur|Un copeau reste sur le fil.",
            "narrateur|Le bois sent encore la résine tiède.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains d'Aniss laissent le bois dans la fourche.",
            "enfant-f|C'était plus facile, là.",
            "papa|Tes bras ont guidé le nichoir.",
            "maman|Le creux gardera son ombre.",
            coda,
            "narrateur|Aniss pose un doigt sur le toit.",
            "narrateur|Une pomme bouge, toute petite.",
            "narrateur|Un rai de soleil barre encore le bois.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le bois tient au tronc, tout propre.",
            "enfant-f|On a noué, Aniss.",
            "papa|Le nœud n'a pas glissé.",
            "maman|Rentrez, l'herbe est sèche.",
            coda,
            "narrateur|Aniss pose une graine sur le toit.",
            "narrateur|La graine ne bouge plus.",
            "narrateur|Une goutte sèche déjà sur le bois.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La pince laisse le bois contre le tronc.",
            "enfant-f|On l'a tenu, tous les deux.",
            "papa|L'écorce est restée à sa place.",
            "maman|Essuie tes chaussures, Nina.",
            coda,
            "narrateur|Aniss souffle un peu sur le toit.",
            "narrateur|Un copeau blanchit, puis s'arrête.",
            "narrateur|La résine colle encore, derrière la haie.",
        )
    return L(
        "narrateur|Le bois suit la fourche, jusqu'au creux.",
        "enfant-f|L'ombre était douce.",
        "papa|La fourche a tenu, tout droit.",
        "maman|Le tronc n'a plus rien à dire.",
        coda,
        "narrateur|Aniss touche le bois, un instant.",
        "narrateur|Une pomme revient contre le toit.",
        "narrateur|Un merle passe, puis le pommier se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Derrière la haie, le pommier penche.",
        "narrateur|Une pomme jaune tape une autre, tout doux.",
        "narrateur|Ça sent le fruit chaud, un peu sucré.",
        "papa|Le merle a chanté, Nina.",
        "maman|Ton nichoir de bois attend dans l'herbe.",
        "narrateur|Le toit est rêche, encore neuf.",
        "narrateur|Une graine roule près du pied.",
        "narrateur|En ce moment, Nina pose la ficelle.",
        "enfant-f|Il va habiter là.",
        "papa|Le merle, tout en haut ?",
        "enfant-f|Oui.",
        "narrateur|Le portillon claque, une fois.",
        "narrateur|Aniss arrive, son sac frotte l'herbe.",
        "enfant-f|On y va, Aniss !",
        "narrateur|Aniss s'accroupit près du bois.",
        "narrateur|Il le touche, sans un mot.",
        "maman|Tu peux lui tendre quelque chose.",
        "papa|Merci, tu as tenu le nichoir droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le nichoir reste dans l'herbe, près des pieds.",
        "narrateur|La ficelle, les graines, et le toit de bois.",
        "papa|Tu prends quoi d'abord, Nina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le nichoir", "la ficelle", "les graines")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nina a tendu {o['t1q']}, tout près.",
            "maman|Elle tend quoi, à Aniss ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1ans"], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la branche", "la fourche", "le tronc")

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
        "Nina veut accrocher son nichoir de bois dans le pommier, pour un merle. "
        "T1 = nichoir / ficelle / graines (les trois partent). "
        "T2 = branche basse (trop bas) / fourche (trop haute) / tronc (ficelle qui glisse). "
        "T3 = neuf résolutions (branche plus haute, tendre le nichoir, tabouret ; "
        "vent, ficelle, mains d'Aniss ; nœud, pince, fourche). "
        "Aniss répond avec les mains, sans étiquette. Nina attend, tend. "
        "Fin : le nichoir tient, le merle vient, on rentre.",
        "Gabarit Maya / cuisine-jardin-chambre / slogan PAR jeté. "
        "Autre récit que DIF-017 (locomotive), DIF-027 (cuillères, véranda), "
        "DIF-037 (panier, petite roue) et DIF-045 (galet, poisson). "
        "Pommier ≠ cueillette (014) ni cerf-volant (024). "
        "Héroïne Nina. Copain Aniss (peu de mots, vécu). Maya hors troupe. "
        "Désir ≠ leçon. N2 ≤ 15. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
