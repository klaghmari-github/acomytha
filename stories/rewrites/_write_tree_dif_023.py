#!/usr/bin/env python3
"""TREE-DIF-023 — La marelle de Sarah et Nino (N3, DIF.ENE.001, école)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-023"
N3 = 16
TITLE = "La marelle de Sarah et Nino"
FIL = (
    "Sarah veut finir une marelle à l'école avec Nino. "
    "Ils emportent la craie bleue, le galet plat et le ruban rouge. "
    "Nino a beaucoup d'élan : en classe le tapis tremble, "
    "dans la cour le galet file, sous le préau l'écho court. "
    "Ils jouent avec lui, ils attendent, ils demandent. "
    "La dernière case est à eux."
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
    out["characters"] = "Sarah, Nino, papa, maman"
    out["setting"] = "école : classe, cour, préau"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
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
        "sami",
        "il ne faut pas",
        "hyperactif",
        "ce n'est pas une faute",
        "camarade qui bouge",
        "sara ",
        "au marché",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
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
        "lab": "la craie bleue",
        "cap": "La craie bleue",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "La craie est dans la poche.",
        "coda": "narrateur|La craie bleue rentre dans la poche.",
    },
    2: {
        "lab": "le galet plat",
        "cap": "Le galet plat",
        "t1q": "dans la boîte",
        "t1acc": "boîte | boite | la boîte | dans la boîte | la boite",
        "t1retry": "Le galet est dans la boîte.",
        "coda": "narrateur|Le galet plat rentre dans la boîte.",
    },
    3: {
        "lab": "le ruban rouge",
        "cap": "Le ruban rouge",
        "t1q": "au poignet",
        "t1acc": "poignet | au poignet | le poignet | son poignet",
        "t1retry": "Le ruban est au poignet.",
        "coda": "narrateur|Le ruban rouge reste au poignet.",
    },
}

T3_LABS = {
    1: ("jouer sur le tapis", "attendre le coussin", "compter avec maman"),
    2: ("sauter ensemble", "attendre la case", "le galet de papa"),
    3: ("le train de sauts", "attendre l'écho", "le rythme de maman"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah prend d'abord la craie bleue.",
            "enfant-f|Elle laisse un trait sur ma paume.",
            "maman|Glisse-la dans ta poche, tout droit.",
            "narrateur|Un peu de bleu reste au creux de la main.",
            "papa|Le galet va dans la boîte, juste après.",
            "narrateur|Maman noue le ruban rouge au poignet.",
            "narrateur|Les trois affaires restent avec eux.",
            "enfant-f|Nino va sauter avec moi.",
            "narrateur|Des pas tapent déjà le carrelage, tout vite.",
            "copain|Sarah, je suis là !",
            "enfant-f|Viens, on finit la marelle.",
            "papa|La craie d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah prend d'abord le galet plat.",
            "enfant-f|Il est tiède, un peu rugueux.",
            "papa|Pose-le dans la boîte, tout doux.",
            "narrateur|La pierre fait un petit toc contre le bois.",
            "maman|La craie bleue, ensuite, dans la poche.",
            "narrateur|Elle glisse le ruban rouge au poignet.",
            "narrateur|Les trois affaires restent avec eux.",
            "enfant-f|Nino va tout voir.",
            "narrateur|Un manteau trop court apparaît au seuil.",
            "copain|Me voilà, Sarah.",
            "enfant-f|On joue la marelle, tous les deux ?",
            "maman|Le galet d'abord, il est prêt.",
        )
    return L(
        "narrateur|Sarah passe le ruban rouge autour du poignet.",
        "enfant-f|C'est la ligne de départ.",
        "maman|Serre-le, comme un secret.",
        "narrateur|Le tissu sent encore le savon de la classe.",
        "papa|La craie et le galet, avec vous.",
        "narrateur|Il les pose près de la boîte.",
        "narrateur|Les trois affaires restent avec eux.",
        "enfant-f|Nino, vite !",
        "narrateur|Des genoux tout petits arrivent en sautant.",
        "copain|J'arrive, Sarah.",
        "enfant-f|Je te garde une case.",
        "papa|Le ruban d'abord, il est noué.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La poche porte la craie, tout contre le tissu.",
            "copain|Elle est trop bleue !",
            "enfant-f|C'est pour nos cases.",
            "narrateur|Nino a les genoux plus bas que Sarah.",
            "narrateur|Ses pieds n'arrêtent pas de bouger.",
            "maman|Il a beaucoup d'élan, ce n'est rien.",
            "papa|On reste à l'école ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La boîte veille près du galet plat.",
            "copain|Je vois la pierre !",
            "enfant-f|Ne la lance pas encore.",
            "narrateur|Nino a les cheveux tout courts.",
            "narrateur|Une mèche saute quand il respire.",
            "papa|Ça sent déjà la craie, dans le couloir.",
            "maman|Vos mains, au-dessus de la boîte ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|Le ruban rouge cache encore le pouls.",
        "copain|Ça sent le savon.",
        "enfant-f|La ligne de départ est là.",
        "narrateur|Le manteau de Nino s'arrête trop haut.",
        "narrateur|Les manches laissent ses poignets libres.",
        "maman|L'école est tiède, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Nino tapote déjà le sol, tout léger.",
        "narrateur|La classe a un tapis à cases.",
        "narrateur|La cour a le bitume encore chaud.",
        "narrateur|Le préau renvoie chaque bruit.",
        "papa|On commence où, pour la marelle ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Sarah trace une case sur le grand papier.",
            2: "narrateur|Sarah pose le galet sur une case dessinée.",
            3: "narrateur|Sarah noue le ruban à la jambe d'une chaise.",
        }[t1]
        mishap = {
            1: "narrateur|Le trait bleu tremble, puis s'élargit.",
            2: "narrateur|Le galet glisse, roule sous une chaise.",
            3: "narrateur|La chaise recule, le ruban se défait.",
        }[t1]
        return L(
            lead,
            "narrateur|Le tapis de la classe sent la laine chaude.",
            "copain|Moi je saute, Sarah !",
            "narrateur|Nino saute entre les tables, trop vite.",
            "narrateur|Une boîte de crayons cliquette, tout haut.",
            mishap,
            f"enfant-f|{o['cap']} n'attendait pas ça.",
            "maman|Il a envie de bouger, c'est tout.",
            "papa|Ses jambes sont plus courtes, plus vives.",
            "copain|On joue comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Sarah dessine une case sur le bitume chaud.",
            2: "narrateur|Sarah lance le galet vers la case huit.",
            3: "narrateur|Sarah pose le ruban, pile sur la ligne.",
        }[t1]
        mishap = {
            1: "narrateur|Les chaussures de Nino prennent le bleu frais.",
            2: "narrateur|Le galet file trop loin, vers le grillage.",
            3: "narrateur|Nino saute par-dessus le ruban, sans s'arrêter.",
        }[t1]
        return L(
            lead,
            "enfant-f|La cour est à nous, Nino.",
            "copain|Je vais jusqu'au bout, trop vite !",
            "narrateur|Ses pieds quittent les cases, puis reviennent.",
            mishap,
            "narrateur|Un peu de poussière lève, puis retombe.",
            "maman|Il a de l'élan, comme un petit vent.",
            "papa|Toi tu as les jambes plus longues.",
            "enfant-f|On peut jouer avec lui ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Sarah trace une case pâle sous le préau.",
        2: "narrateur|Le galet claque, et l'écho répond.",
        3: "narrateur|Le ruban flotte un peu, sous le toit.",
    }[t1]
    mishap = {
        1: "narrateur|Les sauts de Nino effacent le trait pâle.",
        2: "narrateur|Nino court après le bruit, plus loin.",
        3: "narrateur|Nino chasse le ruban, l'écho le suit.",
    }[t1]
    return L(
        lead,
        "enfant-f|Ici, ça résonne, Nino.",
        "copain|J'entends mes pieds deux fois !",
        "narrateur|Le préau renvoie chaque pas, tout fort.",
        mishap,
        f"narrateur|{o['cap']} attend au bord, un peu seule.",
        "maman|Son élan remplit tout le toit.",
        "papa|Toi tu vas plus loin, lui plus vite.",
        "copain|On saute comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Nino saute encore entre les tables.",
            "papa|Le tapis, le coussin, ou compter avec maman ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les cases de la cour attendent encore.",
            "maman|Sauter ensemble, attendre, ou le galet de papa ?",
        )
    return L(
        "narrateur|L'écho remplit encore le préau.",
        "papa|Le train, l'écho, ou le rythme de maman ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Nino tient la boîte, Sarah trace.",
            2: "narrateur|Nino tient le galet, Sarah trace.",
            3: "narrateur|Nino tient le ruban, Sarah trace.",
        }[t1]
        return L(
            "enfant-f|On joue sur le tapis.",
            "copain|Moi je tiens, toi tu dessines.",
            hold,
            "narrateur|Les cases du tapis redeviennent nettes.",
            "narrateur|Nino saute une case, puis s'arrête.",
            "enfant-f|Maintenant c'est moi.",
            "copain|Puis c'est moi encore.",
            "papa|Vous jouez à tour de rôle.",
            "maman|L'élan a trouvé sa place.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|La craie bleue attend près du coussin.",
            2: "narrateur|Le galet plat attend près du coussin.",
            3: "narrateur|Le ruban rouge attend près du coussin.",
        }[t1]
        return L(
            "enfant-f|On attend un peu.",
            "copain|Je m'assois, alors.",
            "narrateur|Nino pose les genoux sur le coussin.",
            wait,
            "narrateur|Sa respiration redevient calme, tout doux.",
            "enfant-f|Tu es prêt ?",
            "copain|Je saute la case un.",
            "papa|Vous avez laissé l'élan s'asseoir.",
            "maman|Le tapis vous a gardés.",
        )
    if t2 == 1 and t3 == 3:
        count = {
            1: "narrateur|Sarah lève la craie à chaque chiffre.",
            2: "narrateur|Sarah lève le galet à chaque chiffre.",
            3: "narrateur|Sarah lève le ruban à chaque chiffre.",
        }[t1]
        return L(
            "enfant-f|Maman, tu comptes avec nous ?",
            "maman|Un, deux, trois.",
            "narrateur|Nino saute seulement quand elle dit trois.",
            count,
            "copain|Je peux attendre le trois !",
            "enfant-f|Moi aussi, j'attends.",
            "narrateur|Les tables restent tranquilles, autour.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Mes chiffres ont tenu l'élan.",
        )
    if t2 == 2 and t3 == 1:
        pair = {
            1: "narrateur|Sarah garde la craie, Nino saute devant.",
            2: "narrateur|Sarah garde le galet, Nino saute devant.",
            3: "narrateur|Sarah garde le ruban, Nino saute devant.",
        }[t1]
        return L(
            "enfant-f|On saute ensemble.",
            "copain|Toi derrière, moi devant !",
            pair,
            "narrateur|Deux ombres passent sur la même case.",
            "narrateur|Nino va plus vite, Sarah plus loin.",
            "enfant-f|On arrive à huit, tous les deux.",
            "copain|J'ai attendu ta jambe, un peu.",
            "papa|Vous avez joué avec l'élan.",
            "maman|La cour vous a laissés passer.",
        )
    if t2 == 2 and t3 == 2:
        line = {
            1: "narrateur|Sarah tient la craie, sur la ligne.",
            2: "narrateur|Sarah tient le galet, sur la ligne.",
            3: "narrateur|Sarah tient le ruban, sur la ligne.",
        }[t1]
        return L(
            "enfant-f|J'attends la case.",
            "copain|Moi je finis, puis c'est toi.",
            line,
            "narrateur|Nino saute jusqu'à huit, tout seul d'abord.",
            "narrateur|Il souffle, puis il recule.",
            "copain|C'est à toi, Sarah.",
            "enfant-f|Merci, j'y vais.",
            "papa|Chacun son tour, sur le bitume.",
            "maman|L'élan a attendu la ligne.",
        )
    if t2 == 2 and t3 == 3:
        hand = {
            1: "narrateur|Papa pose le galet près de la craie.",
            2: "narrateur|Papa pose le galet dans sa paume.",
            3: "narrateur|Papa pose le galet près du ruban.",
        }[t1]
        return L(
            "enfant-f|Papa, tu gardes le galet ?",
            "papa|Je le donne, un coup chacun.",
            hand,
            "narrateur|Nino le reçoit, le pose sur une case.",
            "narrateur|Sarah le reçoit, le pose plus loin.",
            "copain|On demande, et ça va !",
            "enfant-f|La huit est à nous.",
            "maman|Vous avez demandé, tout calme.",
            "papa|Ma main a juste attendu.",
        )
    if t2 == 3 and t3 == 1:
        train = {
            1: "narrateur|La craie bleue voyage dans la poche, entre deux sauts.",
            2: "narrateur|Le galet plat voyage dans la boîte, entre deux sauts.",
            3: "narrateur|Le ruban rouge voyage au poignet, entre deux sauts.",
        }[t1]
        return L(
            "enfant-f|On fait un train de sauts.",
            "copain|Tchou tchou, j'avance !",
            "narrateur|Sarah pose une main sur l'épaule de Nino.",
            train,
            "narrateur|Ils sautent la même case, l'un derrière l'autre.",
            "enfant-f|Doucement, le wagon tient.",
            "copain|L'écho suit le train, puis se tait.",
            "papa|Vous jouez avec le bruit, ensemble.",
            "maman|Le préau est devenu une voie.",
        )
    if t2 == 3 and t3 == 2:
        hush = {
            1: "narrateur|La craie bleue reste muette, au creux.",
            2: "narrateur|Le galet plat reste muet, au creux.",
            3: "narrateur|Le ruban rouge reste muet, au poignet.",
        }[t1]
        return L(
            "enfant-f|On attend l'écho.",
            "copain|Quand il est parti, je saute.",
            "narrateur|Un pas, puis le toit répond.",
            hush,
            "narrateur|Le toit se tait, enfin.",
            "copain|Maintenant !",
            "enfant-f|À toi, puis à moi.",
            "papa|Vous avez laissé le bruit s'asseoir.",
            "maman|L'élan a attendu le silence.",
        )
    clap = {
        1: "narrateur|Sarah lève la craie quand maman frappe.",
        2: "narrateur|Sarah lève le galet quand maman frappe.",
        3: "narrateur|Sarah lève le ruban quand maman frappe.",
    }[t1]
    return L(
        "enfant-f|Maman, tu frappes le rythme ?",
        "maman|Tape, tape, et tu sautes.",
        "narrateur|Nino écoute les mains, plus que ses pieds.",
        clap,
        "copain|Je saute sur tes mains !",
        "enfant-f|Moi aussi, j'écoute.",
        "narrateur|L'écho se range derrière les claps.",
        "papa|Vous avez demandé le rythme.",
        "maman|Mes mains ont tenu l'élan.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La dernière case du tapis est à eux.",
            "copain|On a joué, chacun son tour.",
            "enfant-f|Tu tenais, moi je traçais.",
            "papa|Vous avez laissé l'élan dessiner.",
            "maman|Le couloir sent encore la laine.",
            coda,
            "narrateur|Un trait bleu dort sur le papier.",
            "enfant-f|On rentre, Nino.",
            "narrateur|Les crochets reprennent les manteaux trop longs.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le coussin garde encore la chaleur des genoux.",
            "enfant-f|Tu t'es assis, d'abord.",
            "copain|Puis j'ai sauté, tout droit.",
            "papa|L'élan s'est assis, puis il a joué.",
            "maman|Le tapis redevient calme.",
            coda,
            "narrateur|Une mèche de laine reste coincée.",
            "enfant-f|À demain, les cases.",
            "narrateur|Le carrelage du couloir brille un peu.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le trois de maman reste dans l'air, tout léger.",
            "copain|J'ai attendu le chiffre.",
            "enfant-f|On a demandé, et ça allait.",
            "maman|Mes mots ont tenu vos pieds.",
            "papa|La classe vous rend le silence.",
            f"narrateur|{o['cap']} pose un grain de bleu sur le bois.",
            "narrateur|Sarah touche la dernière case, du bout.",
            "copain|Elle est à nous.",
            "narrateur|Un rai de soleil barre encore le tapis.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Deux paires de chaussures marquent la case huit.",
            "enfant-f|Toi devant, moi derrière.",
            "copain|Tes jambes allaient plus loin.",
            "papa|Vous avez sauté avec l'élan, pas contre.",
            "maman|La cour redevient chaude, et calme.",
            coda,
            "narrateur|Un peu de bleu sèche déjà sur le bitume.",
            "enfant-f|On rentre, les cases restent.",
            "narrateur|Le grillage fait une ombre longue.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La ligne de départ attend encore, toute blanche.",
            "copain|J'ai fini, puis c'était toi.",
            "enfant-f|J'ai attendu ta case.",
            "maman|Chacun son tour, sur le bitume.",
            "papa|L'élan a laissé la place.",
            f"narrateur|{o['cap']} garde un grain de poussière.",
            "narrateur|Sarah souffle dessus, tout doux.",
            "copain|On se dit au revoir, cour.",
            "narrateur|Une craie oubliée sèche contre le mur.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Le galet de papa repose sur la huit.",
            "enfant-f|Tu le donnais, un coup chacun.",
            "copain|On a demandé, et ça roulait juste.",
            "papa|Ma main a fait le tour, rien de plus.",
            "maman|La cour a rendu le galet.",
            coda,
            "narrateur|Un rond clair reste sur le bitume.",
            "enfant-f|Regarde, Nino, il brille.",
            "narrateur|Les manteaux retrouvent les crochets, au frais.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le train de sauts s'arrête à la dernière case.",
            "copain|Tchou tchou, on est arrivés.",
            "enfant-f|J'avais la main sur ton épaule.",
            "papa|Le préau est redevenu un toit, simplement.",
            "maman|L'écho s'est couché.",
            coda,
            "narrateur|Une poussière tourne encore, puis tombe.",
            "enfant-f|On rentre, le wagon se tait.",
            "narrateur|Dehors, la cour redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le toit s'est tu, enfin, tout à fait.",
            "enfant-f|On a attendu l'écho.",
            "copain|Quand il était parti, on sautait.",
            "papa|Le silence vous a laissé la case.",
            "maman|L'élan a écouté le toit.",
            f"narrateur|{o['cap']} ne fait plus aucun bruit.",
            "narrateur|Sarah pose la paume sur la dernière case.",
            "copain|Elle est tiède.",
            "narrateur|Un oiseau passe au-dessus du préau, sans crier.",
        )
    return L(
        "narrateur|Les claps de maman s'éteignent, un à un.",
        "enfant-f|J'écoutais tes mains.",
        "copain|Moi aussi, je sautais dessus.",
        "maman|Vous avez demandé le rythme.",
        "papa|Le préau a rendu vos pas.",
        coda,
        "narrateur|Sarah touche la dernière case, du bout des doigts.",
        "enfant-f|Elle est à nous, Nino.",
        "narrateur|Le toit garde une poussière, puis plus rien.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Des étoiles de papier collent aux vitres.",
        "narrateur|Le couloir sent encore la craie fraîche.",
        "narrateur|Les crochets portent des manteaux trop longs.",
        "narrateur|Un rai de soleil barre le carrelage.",
        "narrateur|Papa noue le lacet de Sarah, tout doux.",
        "papa|Il tient bien, maintenant ?",
        "enfant-f|Oui, papa.",
        "narrateur|Maman pose un galet plat dans la boîte.",
        "maman|Pour la marelle, tu l'as senti ?",
        "enfant-f|Il est tiède, un peu rugueux.",
        "narrateur|En ce moment, Sarah touche la craie bleue.",
        "enfant-f|Je veux finir la marelle avec Nino.",
        "papa|On prépare les affaires, alors ?",
        "maman|La craie, le galet, et le ruban.",
        "papa|Merci, tu tiens la craie tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près de la boîte.",
        "narrateur|La craie, le galet, et le ruban.",
        "maman|Tu prends quoi d'abord, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la craie bleue", "le galet plat", "le ruban rouge")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Sarah a mis {o['lab']} {o['t1q']}.",
            "maman|C'est où, maintenant ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la classe", "la cour", "le préau")
        sons[p] = ""
        sons[f"{p}_T0002_P0000"] = ""

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            sons[sp] = "enfants_parc" if t2 in (2, 3) else ""
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Sarah veut finir une marelle à l'école avec Nino. "
        "T1 = craie bleue / galet plat / ruban rouge (les trois partent). "
        "T2 = classe (tapis, tables) / cour (bitume, cases) / préau (écho). "
        "T3 = neuf résolutions (tapis à tour, coussin, compter avec maman ; "
        "sauter ensemble, attendre la case, galet de papa ; "
        "train de sauts, attendre l'écho, rythme de maman). "
        "L'élan de Nino se vit, sans slogan. Fin : la dernière case.",
        "N3 ≤ 16. Sara→Sarah. Cuisine/jardin/chambre et ballon/seau/doudou jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-019 (école, pas marché). "
        "Un merci de papa lié au geste (tenir la craie). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
