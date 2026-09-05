#!/usr/bin/env python3
"""TREE-DIF-039 — La balle rouge de Victorino, jusqu'au portail (N2, DIF.ENE.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-039"
N2 = LIMITS["N2"]
TITLE = "La balle rouge de Victorino, jusqu'au portail"
FIL = (
    "Victorino veut faire rebondir sa balle rouge jusqu'au portail, avec Aniss. "
    "Il prend d'abord la balle, le sac à pois ou la gourde ; les trois partent. "
    "À la flaque Aniss saute trop fort, au banc du tilleul il rebondit, "
    "au muret il court. Ils jouent avec lui, ils attendent, ils demandent. "
    "La balle arrive au portail."
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
    out["characters"] = "Victorino, Aniss, papa, maman"
    out["setting"] = "chemin de l'école : flaque, banc du tilleul, muret du portail"
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
        "hyperactif",
        "ce n'est pas une faute",
        "camarade qui bouge",
        "beaucoup d'énergie",
        "adam",
        "jardin",
        "marché",
        "classe",
        "cuisine",
        "chambre",
        "dînette",
        "dinette",
        "sieste",
        "les cubes",
        "capitaine",
        "plic",
        "volet jaune",
        "pommier",
        "après la sieste",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
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
        "lab": "la balle rouge",
        "cap": "La balle rouge",
        "t1q": "contre le ventre",
        "t1acc": "ventre | le ventre | contre le ventre | son ventre",
        "t1retry": "La balle est contre le ventre.",
        "coda": "narrateur|La balle rouge garde une goutte, encore tiède.",
    },
    2: {
        "lab": "le sac à pois",
        "cap": "Le sac à pois",
        "t1q": "sur le dos",
        "t1acc": "dos | le dos | sur le dos | son dos",
        "t1retry": "Le sac est sur le dos.",
        "coda": "narrateur|Le sac à pois sèche une feuille de tilleul.",
    },
    3: {
        "lab": "la gourde bleue",
        "cap": "La gourde bleue",
        "t1q": "à la main",
        "t1acc": "main | la main | à la main | sa main",
        "t1retry": "La gourde est à la main.",
        "coda": "narrateur|La gourde bleue garde une perle d'eau.",
    },
}

T3_LABS = {
    1: ("jouer dans l'eau", "attendre la goutte", "la main de papa"),
    2: ("sauter ensemble", "attendre le tour", "le goûter de maman"),
    3: ("le relais de balles", "attendre le portail", "le rythme de papa"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorino prend d'abord la balle rouge.",
            "enfant-m|Elle est un peu rêche, encore.",
            "maman|Tiens-la contre le ventre, tout doux.",
            "narrateur|Le caoutchouc sent le soleil, déjà.",
            "papa|Le sac aussi, près de toi.",
            "narrateur|Maman glisse la gourde, tout près.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Aniss va tout voir.",
            "narrateur|Des pieds tapent déjà le trottoir, tout vite.",
            "copain|Victorino, je suis là !",
            "enfant-m|Viens, on va jusqu'au portail.",
            "papa|La balle d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorino passe d'abord le sac à pois.",
            "enfant-m|Il gratte un peu, aux épaules.",
            "papa|Mets-le, le chemin est long.",
            "narrateur|Les pois font une ombre ronde.",
            "maman|La balle, ensuite, près de toi.",
            "narrateur|Il glisse la gourde d'une main.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Aniss va aimer le sac.",
            "narrateur|Un manteau trop court apparaît au seuil.",
            "copain|Me voilà, Victorino.",
            "enfant-m|On rebondit jusqu'au portail ?",
            "maman|Le sac d'abord, il est prêt.",
        )
    return L(
        "narrateur|Victorino prend d'abord la gourde bleue.",
        "enfant-m|Elle est froide, contre la paume.",
        "maman|Garde-la à la main, tout droit.",
        "narrateur|Le plastique sent encore l'eau.",
        "papa|La balle et le sac, avec toi.",
        "narrateur|Il les pose près des chaussures.",
        "narrateur|Les trois affaires partent ensemble.",
        "enfant-m|Aniss, vite !",
        "narrateur|Des genoux tout petits arrivent en sautant.",
        "copain|J'arrive, Victorino.",
        "enfant-m|Je te garde la balle.",
        "papa|La gourde d'abord, elle est prise.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Contre le ventre.",
            "maman|Oui.",
            "narrateur|La balle rouge tient, déjà un peu chaude.",
            "copain|Elle est trop rouge !",
            "enfant-m|C'est pour le portail.",
            "narrateur|Aniss a les genoux plus bas que Victorino.",
            "narrateur|Ses pieds n'arrêtent pas de bouger.",
            "maman|Il a beaucoup d'élan, ce n'est rien.",
            "papa|On reste sur le chemin ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Sur le dos.",
            "papa|Oui.",
            "narrateur|Le sac à pois tient une ombre ronde.",
            "copain|Je vois les pois !",
            "enfant-m|On le garde pour le portail.",
            "narrateur|Aniss a les cheveux tout courts.",
            "narrateur|Une mèche saute quand il respire.",
            "maman|Ça sent déjà le trottoir chaud.",
            "papa|Vos mains, sur le sac ?",
            "copain|Oui, papa.",
        )
    return L(
        "enfant-m|À la main.",
        "maman|Oui.",
        "narrateur|La gourde bleue avance, un pas après l'autre.",
        "copain|Ça sent l'eau.",
        "enfant-m|Le départ est là.",
        "narrateur|Le manteau d'Aniss s'arrête trop haut.",
        "narrateur|Les manches laissent ses poignets libres.",
        "maman|Le chemin est tiède, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Aniss tapote déjà le sol, tout léger.",
        "narrateur|La flaque brille encore un peu.",
        "narrateur|Le banc du tilleul fait une ombre.",
        "narrateur|Le muret garde le portail, tout près.",
        "papa|On le rejoint où, Victorino ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|La balle rouge voyage vers la flaque.",
            2: "narrateur|Le sac à pois penche vers la flaque.",
            3: "narrateur|La gourde bleue avance vers la flaque.",
        }[t1]
        mishap = {
            1: "narrateur|La balle manque un rebond, touche l'eau.",
            2: "narrateur|Les pois du sac se mouillent, tout bas.",
            3: "narrateur|La gourde tape l'eau, un petit choc.",
        }[t1]
        return L(
            lead,
            "narrateur|Aniss tape l'eau, trop vite.",
            "copain|Moi je saute, Victorino !",
            "narrateur|Ses pieds font des ronds, trop larges.",
            mishap,
            f"enfant-m|{o['cap']} n'attendait pas ça.",
            "maman|Il a envie de bouger, c'est tout.",
            "papa|Ses jambes sont plus courtes, plus vives.",
            "copain|On joue comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|La balle rouge s'arrête sous le tilleul.",
            2: "narrateur|Le sac à pois glisse sous le tilleul.",
            3: "narrateur|La gourde bleue bute sous le tilleul.",
        }[t1]
        mishap = {
            1: "narrateur|Les chaussures d'Aniss prennent le bois du banc.",
            2: "narrateur|Le sac penche, Aniss rebondit trop haut.",
            3: "narrateur|Aniss saute par-dessus la gourde, sans s'arrêter.",
        }[t1]
        return L(
            lead,
            "enfant-m|Le banc est à nous, Aniss.",
            "copain|Je vais jusqu'au bout, trop vite !",
            "narrateur|Ses pieds quittent le bois, puis reviennent.",
            mishap,
            "narrateur|Un peu de poussière lève, puis retombe.",
            "maman|Il a de l'élan, comme un petit vent.",
            "papa|Toi tu as les jambes plus longues.",
            "enfant-m|On peut jouer avec lui ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|La balle rouge pose son ombre sur le muret.",
        2: "narrateur|Le sac à pois s'appuie contre le muret.",
        3: "narrateur|La gourde bleue s'arrête près du muret.",
    }[t1]
    mishap = {
        1: "narrateur|Les sauts d'Aniss chassent la balle, trop loin.",
        2: "narrateur|Aniss court après le sac, plus loin.",
        3: "narrateur|Aniss court, la gourde reste contre la pierre.",
    }[t1]
    return L(
        lead,
        "enfant-m|Ici, ça mène au portail, Aniss.",
        "copain|Je vais plus loin, encore !",
        "narrateur|Le muret renvoie chaque pas, tout fort.",
        mishap,
        f"narrateur|{o['cap']} attend au bord, un peu seule.",
        "maman|Son élan remplit tout le mur.",
        "papa|Toi tu vas plus loin, lui plus vite.",
        "copain|On rebondit comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Aniss tape encore l'eau, tout fort.",
            "papa|Dans l'eau, la goutte, ou ma main ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Aniss rebondit encore sur le banc.",
            "maman|Ensemble, le tour, ou le goûter ?",
        )
    return L(
        "narrateur|Aniss court encore le long du muret.",
        "papa|Le relais, le portail, ou mon rythme ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Aniss tient l'eau, Victorino rebondit.",
            2: "narrateur|Aniss tient le sac, Victorino rebondit.",
            3: "narrateur|Aniss tient la gourde, Victorino rebondit.",
        }[t1]
        return L(
            "enfant-m|On joue dans l'eau.",
            "copain|Moi je saute, toi tu rebondis.",
            hold,
            "narrateur|Deux ronds se croisent, puis s'éloignent.",
            "narrateur|Aniss saute une fois, puis s'arrête.",
            "enfant-m|Maintenant c'est moi.",
            "copain|Puis c'est moi encore.",
            "papa|Vous jouez à tour, dans l'eau.",
            "maman|L'élan a trouvé sa flaque.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|La balle rouge attend près du bord.",
            2: "narrateur|Le sac à pois attend près du bord.",
            3: "narrateur|La gourde bleue attend près du bord.",
        }[t1]
        return L(
            "enfant-m|On attend un peu.",
            "copain|Je m'arrête, alors.",
            "narrateur|Aniss pose les genoux au bord.",
            wait,
            "narrateur|Sa respiration redevient calme, tout doux.",
            "enfant-m|Tu es prêt ?",
            "copain|Je rebondis avec toi.",
            "papa|Vous avez laissé l'élan s'asseoir.",
            "maman|La flaque vous a gardés.",
        )
    if t2 == 1 and t3 == 3:
        hand = {
            1: "narrateur|Papa pose la balle près de sa main.",
            2: "narrateur|Papa pose le sac près de sa main.",
            3: "narrateur|Papa pose la gourde près de sa main.",
        }[t1]
        return L(
            "enfant-m|Papa, tu tiens Aniss ?",
            "papa|Je donne la main, un pas chacun.",
            hand,
            "narrateur|Aniss pose un pied, puis l'autre.",
            "narrateur|Victorino rebondit, juste à côté.",
            "copain|On demande, et ça va !",
            "enfant-m|La flaque est à nous.",
            "maman|Vous avez demandé, tout calme.",
            "papa|Ma main a juste attendu.",
        )
    if t2 == 2 and t3 == 1:
        pair = {
            1: "narrateur|Victorino garde la balle, Aniss saute devant.",
            2: "narrateur|Victorino garde le sac, Aniss saute devant.",
            3: "narrateur|Victorino garde la gourde, Aniss saute devant.",
        }[t1]
        return L(
            "enfant-m|On saute ensemble.",
            "copain|Toi derrière, moi devant !",
            pair,
            "narrateur|Deux ombres passent sur le même banc.",
            "narrateur|Aniss va plus vite, Victorino plus loin.",
            "enfant-m|On arrive au bout, tous les deux.",
            "copain|J'ai attendu ta jambe, un peu.",
            "papa|Vous avez joué avec l'élan.",
            "maman|Le banc vous a laissés passer.",
        )
    if t2 == 2 and t3 == 2:
        line = {
            1: "narrateur|Victorino tient la balle, sur le bois.",
            2: "narrateur|Victorino tient le sac, sur le bois.",
            3: "narrateur|Victorino tient la gourde, sur le bois.",
        }[t1]
        return L(
            "enfant-m|J'attends le tour.",
            "copain|Moi je finis, puis c'est toi.",
            line,
            "narrateur|Aniss saute jusqu'au bout, tout seul d'abord.",
            "narrateur|Il souffle, puis il recule.",
            "copain|C'est à toi, Victorino.",
            "enfant-m|Merci, j'y vais.",
            "papa|Chacun son tour, sur le banc.",
            "maman|L'élan a attendu la place.",
        )
    if t2 == 2 and t3 == 3:
        snack = {
            1: "narrateur|Maman pose le pain près de la balle.",
            2: "narrateur|Maman pose le pain dans le sac.",
            3: "narrateur|Maman pose le pain près de la gourde.",
        }[t1]
        return L(
            "enfant-m|Maman, tu ouvres le goûter ?",
            "maman|Un morceau chacun, tout doux.",
            snack,
            "narrateur|Aniss mâche, et ses pieds se posent.",
            "narrateur|Victorino mâche, la balle au calme.",
            "copain|On rebondit après, d'accord ?",
            "enfant-m|Après le goûter, oui.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Le pain a tenu l'élan.",
        )
    if t2 == 3 and t3 == 1:
        train = {
            1: "narrateur|La balle rouge voyage d'une main à l'autre.",
            2: "narrateur|Le sac à pois voyage d'une épaule à l'autre.",
            3: "narrateur|La gourde bleue voyage d'une paume à l'autre.",
        }[t1]
        return L(
            "enfant-m|On fait un relais de balles.",
            "copain|Je te la passe, tu me la rends !",
            train,
            "narrateur|Ils avancent le long du muret, l'un après l'autre.",
            "enfant-m|Doucement, le relais tient.",
            "copain|Le portail est tout près.",
            "papa|Vous jouez avec l'élan, ensemble.",
            "maman|Le muret est devenu une voie.",
            f"narrateur|{o['cap']} a fait le tour, sans se taire.",
        )
    if t2 == 3 and t3 == 2:
        hush = {
            1: "narrateur|La balle rouge reste muette, au creux.",
            2: "narrateur|Le sac à pois reste muet, au creux.",
            3: "narrateur|La gourde bleue reste muette, à la main.",
        }[t1]
        return L(
            "enfant-m|On attend le portail.",
            "copain|Quand il s'ouvre, je rebondis.",
            "narrateur|Un pas, puis le battant reste fermé.",
            hush,
            "narrateur|Le battant bouge, enfin.",
            "copain|Maintenant !",
            "enfant-m|À toi, puis à moi.",
            "papa|Vous avez laissé le battant s'ouvrir.",
            "maman|L'élan a attendu le seuil.",
        )
    clap = {
        1: "narrateur|Victorino lève la balle quand papa frappe.",
        2: "narrateur|Victorino lève le sac quand papa frappe.",
        3: "narrateur|Victorino lève la gourde quand papa frappe.",
    }[t1]
    return L(
        "enfant-m|Papa, tu frappes le rythme ?",
        "papa|Tape, tape, et tu rebondis.",
        "narrateur|Aniss écoute les mains, plus que ses pieds.",
        clap,
        "copain|Je saute sur tes mains !",
        "enfant-m|Moi aussi, j'écoute.",
        "narrateur|Le muret se range derrière les claps.",
        "papa|Vous avez demandé le rythme.",
        "maman|Ses mains ont tenu l'élan.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le dernier rond de la flaque est à eux.",
            "copain|On a joué, chacun son tour.",
            "enfant-m|Tu sautais, moi je rebondissais.",
            "papa|Vous avez laissé l'élan dessiner.",
            "maman|Le chemin sent encore l'eau.",
            coda,
            "narrateur|Un trait clair dort sur la pierre.",
            "enfant-m|On rentre, Aniss.",
            "narrateur|Les chaussures reprennent le trottoir sec.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le bord de la flaque garde encore la chaleur.",
            "enfant-m|Tu t'es arrêté, d'abord.",
            "copain|Puis j'ai rebondi, tout droit.",
            "papa|L'élan s'est assis, puis il a joué.",
            "maman|La flaque redevient calme.",
            coda,
            "narrateur|Une feuille reste coincée, tout près.",
            "enfant-m|À demain, les ronds.",
            "narrateur|Le caniveau brille un peu, puis se tait.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La main de papa reste dans l'air, tout légère.",
            "copain|J'ai attendu le pas.",
            "enfant-m|On a demandé, et ça allait.",
            "maman|Sa main a tenu vos pieds.",
            "papa|Le chemin vous rend le silence.",
            f"narrateur|{o['cap']} pose un grain d'eau sur le bois.",
            "narrateur|Victorino touche le portail, du bout.",
            "copain|Il est à nous.",
            "narrateur|Un rai de soleil barre encore la flaque.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Deux paires de chaussures marquent le bout du banc.",
            "enfant-m|Toi devant, moi derrière.",
            "copain|Tes jambes allaient plus loin.",
            "papa|Vous avez sauté avec l'élan, pas contre.",
            "maman|Le tilleul redevient chaud, et calme.",
            coda,
            "narrateur|Un peu de poussière sèche déjà sur le bois.",
            "enfant-m|On rentre, le banc reste.",
            "narrateur|Le portail fait une ombre longue.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le bout du banc attend encore, tout lisse.",
            "copain|J'ai fini, puis c'était toi.",
            "enfant-m|J'ai attendu ta place.",
            "maman|Chacun son tour, sur le bois.",
            "papa|L'élan a laissé la place.",
            f"narrateur|{o['cap']} garde un grain de poussière.",
            "narrateur|Victorino souffle dessus, tout doux.",
            "copain|On se dit au revoir, banc.",
            "narrateur|Une feuille oubliée sèche contre le pied.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Le pain de maman repose sur le banc.",
            "enfant-m|Tu le donnais, un morceau chacun.",
            "copain|On a demandé, et ça allait juste.",
            "papa|Le goûter a fait le tour, rien de plus.",
            "maman|Le tilleul a rendu le calme.",
            coda,
            "narrateur|Un rond de mie reste sur le bois.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|Les manteaux retrouvent le chemin, au frais.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le relais s'arrête contre le portail.",
            "copain|On est arrivés, tous les deux.",
            "enfant-m|Je te la passais, tu me la rendais.",
            "papa|Le muret est redevenu un mur, simplement.",
            "maman|L'élan s'est couché.",
            coda,
            "narrateur|Une poussière tourne encore, puis tombe.",
            "enfant-m|On rentre, le relais se tait.",
            "narrateur|Dehors, le chemin redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le battant s'est ouvert, enfin, tout à fait.",
            "enfant-m|On a attendu le portail.",
            "copain|Quand il était ouvert, on rebondissait.",
            "papa|Le seuil vous a laissé la balle.",
            "maman|L'élan a écouté le battant.",
            f"narrateur|{o['cap']} ne fait plus aucun bruit.",
            "narrateur|Victorino pose la paume sur le fer tiède.",
            "copain|Il est tiède.",
            "narrateur|Un oiseau passe au-dessus du muret, sans crier.",
        )
    return L(
        "narrateur|Les claps de papa s'éteignent, un à un.",
        "enfant-m|J'écoutais tes mains.",
        "copain|Moi aussi, je sautais dessus.",
        "maman|Vous avez demandé le rythme.",
        "papa|Le muret a rendu vos pas.",
        coda,
        "narrateur|Victorino touche le portail, du bout des doigts.",
        "enfant-m|Il est à nous, Aniss.",
        "narrateur|Le fer garde une poussière, puis plus rien.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La boîte aux lettres claque une fois, tout près.",
        "narrateur|Un vélo sonne, au bout de la rue.",
        "narrateur|Le trottoir garde encore une goutte.",
        "narrateur|Ça sent le pain chaud, sous la fenêtre.",
        "papa|Tes lacets tiennent, Victorino ?",
        "enfant-m|Oui, papa.",
        "narrateur|Maman glisse la gourde bleue dans le sac.",
        "maman|Pour le chemin, tu l'as sentie ?",
        "enfant-m|Elle est froide, un peu.",
        "narrateur|En ce moment, Victorino touche la balle rouge.",
        "enfant-m|Je veux la faire rebondir jusqu'au portail.",
        "papa|On prépare les affaires, alors ?",
        "maman|La balle, le sac, et la gourde.",
        "papa|Merci, tu tiens la balle tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près des chaussures.",
        "narrateur|La balle, le sac, et la gourde.",
        "maman|Tu prends quoi d'abord, Victorino ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la balle rouge", "le sac à pois", "la gourde bleue")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        if t1 == 1:
            s[f"{p}_Q0001"] = L(
                "narrateur|Victorino a mis la balle rouge.",
                "maman|Elle est où, maintenant ?",
            )
        elif t1 == 2:
            s[f"{p}_Q0001"] = L(
                "narrateur|Victorino a passé le sac à pois.",
                "maman|Il est où, maintenant ?",
            )
        else:
            s[f"{p}_Q0001"] = L(
                "narrateur|Victorino a pris la gourde bleue.",
                "maman|Elle est où, maintenant ?",
            )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la flaque", "le banc du tilleul", "le muret du portail")
        sons[p] = ""
        sons[f"{p}_T0002_P0000"] = ""

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            sons[sp] = ""
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Victorino veut faire rebondir sa balle rouge jusqu'au portail avec Aniss. "
        "T1 = balle rouge / sac à pois / gourde bleue (les trois partent). "
        "T2 = flaque (eau, ronds) / banc du tilleul (rebonds) / muret du portail (course). "
        "T3 = neuf résolutions (jouer dans l'eau, attendre la goutte, main de papa ; "
        "sauter ensemble, attendre le tour, goûter de maman ; "
        "relais de balles, attendre le portail, rythme de papa). "
        "L'élan d'Aniss se vit, sans slogan. Fin : le portail.",
        "N2 ≤ 15. Adam hors troupe → Victorino + Aniss. "
        "Cuisine/jardin/chambre, cubes/livre/dînette, matin/sieste/soir jetés. "
        "Chemin de l'école (pas jardin, pas marché, pas classe). "
        "Titre slogan remplacé (objet + désir). Un merci de papa lié au geste "
        "(tenir la balle). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
