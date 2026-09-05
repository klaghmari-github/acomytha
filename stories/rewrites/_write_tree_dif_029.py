#!/usr/bin/env python3
"""TREE-DIF-029 — Le papillon jaune de Victorino (N3, DIF.ENE.001, pré)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-029"
N3 = 16
TITLE = "Le papillon jaune de Victorino"
FIL = (
    "Victorino veut que le papillon jaune se pose sur la fleur de papier, "
    "avec Aniss. Ils emportent le filet vert, le chapeau bleu et la fleur. "
    "Aniss a trop d'élan : dans le pré l'herbe s'envole, aux lavandes le parfum "
    "saute, au muret les pierres cliquent. Ils jouent avec lui, ils attendent, "
    "ils demandent. Le jaune se pose."
)
CHARS = "Victorino, Aniss, papa, maman"
SETTING = "village au bord des champs : pré, lavandes, muret"


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
        "sami",
        "il ne faut pas",
        "hyperactif",
        "ce n'est pas une faute",
        "camarade qui bouge",
        "à l'école",
        "l'école",
        "marelle",
        "dînette",
        "dinette",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if re.search(r"\btom\b", whole):
        raise SystemExit(f"{SID} slogan: tom")
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
        "lab": "le filet vert",
        "cap": "Le filet vert",
        "t1q": "dans le sac",
        "t1ans": "sac",
        "t1acc": "sac | le sac | dans le sac | son sac",
        "t1retry": "Le filet est dans le sac.",
        "coda": "narrateur|Le filet vert rentre dans le sac.",
    },
    2: {
        "lab": "le chapeau bleu",
        "cap": "Le chapeau bleu",
        "t1q": "sur la tête",
        "t1ans": "tête",
        "t1acc": "tête | tete | la tête | sur la tête | sa tête",
        "t1retry": "Le chapeau est sur la tête.",
        "coda": "narrateur|Le chapeau bleu reste sur les cheveux.",
    },
    3: {
        "lab": "la fleur de papier",
        "cap": "La fleur de papier",
        "t1q": "dans la poche",
        "t1ans": "poche",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "La fleur est dans la poche.",
        "coda": "narrateur|La fleur de papier rentre dans la poche.",
    },
}

T3_LABS = {
    1: ("marcher comme lui", "s'asseoir dans l'herbe", "le silence de maman"),
    2: ("souffler tout doux", "attendre le parfum", "la fleur de papa"),
    3: ("le rythme sur la pierre", "attendre en bas", "la main de maman"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorino prend d'abord le filet vert.",
            "enfant-m|Les mailles laissent passer le soleil.",
            "maman|Glisse-le dans le sac, tout droit.",
            "narrateur|Un peu d'ombre reste au creux de la main.",
            "papa|Le chapeau bleu va sur ta tête, juste après.",
            "narrateur|Maman glisse la fleur de papier dans la poche.",
            "narrateur|Les trois affaires restent avec eux.",
            "enfant-m|Aniss va guetter avec moi.",
            "narrateur|Des pas tapent déjà le gravier, tout vite.",
            "copain|Victorino, je suis là !",
            "enfant-m|Viens, on cherche le papillon jaune.",
            "papa|Le filet d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorino pose d'abord le chapeau bleu.",
            "enfant-m|Il sent encore le savon du linge.",
            "papa|Calé sur tes cheveux, tout doux.",
            "narrateur|L'ombre descend jusqu'aux sourcils.",
            "maman|Le filet vert, ensuite, dans le sac.",
            "narrateur|Elle glisse la fleur de papier dans la poche.",
            "narrateur|Les trois affaires restent avec eux.",
            "enfant-m|Aniss va tout voir.",
            "narrateur|Un genou tout petit apparaît au seuil.",
            "copain|Me voilà, Victorino.",
            "enfant-m|On guette le jaune, tous les deux ?",
            "maman|Le chapeau d'abord, il est prêt.",
        )
    return L(
        "narrateur|Victorino glisse la fleur de papier dans la poche.",
        "enfant-m|C'est pour attirer le jaune.",
        "maman|Serre-la, comme un secret.",
        "narrateur|Le papier sent encore un peu la colle.",
        "papa|Le filet et le chapeau, avec vous.",
        "narrateur|Il les pose près du sac.",
        "narrateur|Les trois affaires restent avec eux.",
        "enfant-m|Aniss, vite !",
        "narrateur|Des manches trop courtes arrivent en sautant.",
        "copain|J'arrive, Victorino.",
        "enfant-m|Je te garde une place au pré.",
        "papa|La fleur d'abord, elle est cachée.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le sac porte le filet, tout contre le tissu.",
            "copain|Il est trop vert !",
            "enfant-m|C'est pour faire de l'ombre.",
            "narrateur|Aniss a les genoux plus bas que Victorino.",
            "narrateur|Ses pieds n'arrêtent pas de bouger.",
            "maman|Il a beaucoup d'élan, ce n'est rien.",
            "papa|On reste près des champs ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le chapeau veille déjà sur les sourcils.",
            "copain|Je vois l'ombre !",
            "enfant-m|Ne cours pas encore.",
            "narrateur|Aniss a les cheveux tout courts.",
            "narrateur|Une mèche saute quand il respire.",
            "papa|Ça sent déjà le foin, derrière le portail.",
            "maman|Vos mains, au-dessus du sac ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|La poche cache encore le papier plié.",
        "copain|Ça sent la colle.",
        "enfant-m|La fleur attend le jaune.",
        "narrateur|Le manteau d'Aniss s'arrête trop haut.",
        "narrateur|Les manches laissent ses poignets libres.",
        "maman|Le pré est tiède, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Aniss tapote déjà le sol, tout léger.",
        "narrateur|Le pré a l'herbe haute, encore tiède.",
        "narrateur|Les lavandes sentent fort, tout bas.",
        "narrateur|Le muret garde une pierre chaude.",
        "papa|On commence où, pour le papillon ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Victorino lève le filet, comme un toit.",
            2: "narrateur|Victorino baisse le chapeau, pour l'ombre.",
            3: "narrateur|Victorino pose la fleur sur une tige.",
        }[t1]
        mishap = {
            1: "narrateur|Le filet racle l'herbe, trop vite.",
            2: "narrateur|Le chapeau s'envole, puis retombe.",
            3: "narrateur|La fleur se plie contre un genou.",
        }[t1]
        return L(
            lead,
            "narrateur|L'herbe du pré sent le foin chaud.",
            "copain|Moi je cours, Victorino !",
            "narrateur|Aniss fend l'herbe, trop vite.",
            "narrateur|Un nuage de graines s'envole, tout haut.",
            mishap,
            f"enfant-m|{o['cap']} n'attendait pas ça.",
            "maman|Il a envie de bouger, c'est tout.",
            "papa|Ses jambes sont plus courtes, plus vives.",
            "copain|On guette comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Victorino glisse le filet entre les tiges.",
            2: "narrateur|Victorino avance, le chapeau tout bas.",
            3: "narrateur|Victorino tend la fleur vers le violet.",
        }[t1]
        mishap = {
            1: "narrateur|La poussière violette emplit les mailles.",
            2: "narrateur|Des brins collent à l'aile du chapeau.",
            3: "narrateur|Un coude plie le papier, trop fort.",
        }[t1]
        return L(
            lead,
            "enfant-m|Les lavandes sentent partout, Aniss.",
            "copain|Je vais jusqu'au bout, trop vite !",
            "narrateur|Ses pieds tapent les tiges, puis reviennent.",
            mishap,
            "narrateur|Un parfum lève, puis retombe.",
            "maman|Il a de l'élan, comme un petit vent.",
            "papa|Toi tu vas plus loin, lui plus vite.",
            "enfant-m|On peut guetter avec lui ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Victorino pose le filet contre la pierre.",
        2: "narrateur|Le chapeau bleu frôle le muret chaud.",
        3: "narrateur|La fleur de papier attend sur la pierre.",
    }[t1]
    mishap = {
        1: "narrateur|Les pas d'Aniss font trembler le filet.",
        2: "narrateur|Le bord du chapeau tape la pierre.",
        3: "narrateur|La fleur glisse dans une fente.",
    }[t1]
    return L(
        lead,
        "enfant-m|Ici, la pierre est chaude, Aniss.",
        "copain|J'entends mes pieds deux fois !",
        "narrateur|Le muret renvoie chaque pas, tout fort.",
        mishap,
        f"narrateur|{o['cap']} attend au bord, un peu seule.",
        "maman|Son élan remplit toute la pierre.",
        "papa|Toi tu vas plus loin, lui plus vite.",
        "copain|On guette comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Aniss fend encore l'herbe, tout léger.",
            "papa|Marcher comme lui, s'asseoir, ou maman ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les lavandes bougent encore, un peu.",
            "maman|Souffler, attendre, ou la fleur de papa ?",
        )
    return L(
        "narrateur|Les clics remplissent encore le muret.",
        "papa|Le rythme, en bas, ou la main de maman ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Aniss tient le sac, Victorino lève le filet.",
            2: "narrateur|Aniss tient le sac, Victorino baisse le chapeau.",
            3: "narrateur|Aniss tient le sac, Victorino lève la fleur.",
        }[t1]
        return L(
            "enfant-m|On marche comme lui.",
            "copain|Moi je bats des bras, tout lent.",
            hold,
            "narrateur|Deux ombres avancent dans l'herbe, sans courir.",
            "narrateur|Aniss lève un pied, puis s'arrête.",
            "enfant-m|Maintenant c'est moi.",
            "copain|Puis c'est moi encore.",
            "papa|Vous jouez à son pas.",
            "maman|L'élan a trouvé sa place.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le filet vert attend près des genoux.",
            2: "narrateur|Le chapeau bleu attend près des genoux.",
            3: "narrateur|La fleur de papier attend près des genoux.",
        }[t1]
        return L(
            "enfant-m|On s'assoit un peu.",
            "copain|Je m'assois, alors.",
            "narrateur|Aniss pose les genoux dans l'herbe.",
            wait,
            "narrateur|Sa respiration redevient calme, tout doux.",
            "enfant-m|Tu es prêt ?",
            "copain|Je ne cours plus.",
            "papa|Vous avez laissé l'élan s'asseoir.",
            "maman|Le pré vous a gardés.",
        )
    if t2 == 1 and t3 == 3:
        count = {
            1: "narrateur|Victorino lève le filet à chaque chiffre.",
            2: "narrateur|Victorino touche le chapeau à chaque chiffre.",
            3: "narrateur|Victorino lève la fleur à chaque chiffre.",
        }[t1]
        return L(
            "enfant-m|Maman, tu restes avec nous ?",
            "maman|Un, deux, trois, on ne bouge plus.",
            "narrateur|Aniss s'arrête seulement quand elle dit trois.",
            count,
            "copain|Je peux attendre le trois !",
            "enfant-m|Moi aussi, j'attends.",
            "narrateur|L'herbe redevient droite, autour.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Mes chiffres ont tenu l'élan.",
        )
    if t2 == 2 and t3 == 1:
        pair = {
            1: "narrateur|Victorino garde le filet, Aniss souffle devant.",
            2: "narrateur|Victorino garde le chapeau, Aniss souffle devant.",
            3: "narrateur|Victorino garde la fleur, Aniss souffle devant.",
        }[t1]
        return L(
            "enfant-m|On souffle tout doux.",
            "copain|Toi derrière, moi devant !",
            pair,
            "narrateur|Deux souffles passent sur la même tige.",
            "narrateur|Aniss va plus vite, Victorino plus loin.",
            "enfant-m|On arrive au violet, tous les deux.",
            "copain|J'ai attendu ton souffle, un peu.",
            "papa|Vous avez joué avec l'élan.",
            "maman|Les lavandes vous ont laissés passer.",
        )
    if t2 == 2 and t3 == 2:
        line = {
            1: "narrateur|Victorino tient le filet, sans le bouger.",
            2: "narrateur|Victorino tient le chapeau, sans le bouger.",
            3: "narrateur|Victorino tient la fleur, sans la bouger.",
        }[t1]
        return L(
            "enfant-m|J'attends le parfum.",
            "copain|Moi je finis, puis c'est toi.",
            line,
            "narrateur|Aniss tapote une tige, tout seul d'abord.",
            "narrateur|Il souffle, puis il recule.",
            "copain|C'est à toi, Victorino.",
            "enfant-m|Merci, j'y vais.",
            "papa|Chacun son tour, entre les tiges.",
            "maman|L'élan a attendu le parfum.",
        )
    if t2 == 2 and t3 == 3:
        hand = {
            1: "narrateur|Papa pose la fleur près du filet.",
            2: "narrateur|Papa pose la fleur près du chapeau.",
            3: "narrateur|Papa pose la fleur dans sa paume.",
        }[t1]
        return L(
            "enfant-m|Papa, tu gardes la fleur ?",
            "papa|Je la tends, un pas chacun.",
            hand,
            "narrateur|Aniss s'approche, tout petit pas.",
            "narrateur|Victorino s'approche, encore plus lent.",
            "copain|On demande, et ça va !",
            "enfant-m|Le violet est à nous.",
            "maman|Vous avez demandé, tout calme.",
            "papa|Ma main a juste attendu.",
        )
    if t2 == 3 and t3 == 1:
        train = {
            1: "narrateur|Le filet vert voyage contre la pierre, entre deux taps.",
            2: "narrateur|Le chapeau bleu voyage sur les cheveux, entre deux taps.",
            3: "narrateur|La fleur de papier voyage sur la pierre, entre deux taps.",
        }[t1]
        return L(
            "enfant-m|On fait un rythme sur la pierre.",
            "copain|Toc toc, j'avance !",
            "narrateur|Victorino pose une main sur l'épaule d'Aniss.",
            train,
            "narrateur|Ils tapent la même pierre, l'un après l'autre.",
            "enfant-m|Doucement, le rythme tient.",
            "copain|Le clic suit le rythme, puis se tait.",
            "papa|Vous jouez avec le bruit, ensemble.",
            "maman|Le muret est devenu un tambour.",
        )
    if t2 == 3 and t3 == 2:
        hush = {
            1: "narrateur|Le filet vert reste muet, au creux.",
            2: "narrateur|Le chapeau bleu reste muet, au creux.",
            3: "narrateur|La fleur de papier reste muette, au creux.",
        }[t1]
        return L(
            "enfant-m|On attend en bas.",
            "copain|Quand la pierre se tait, je m'approche.",
            "narrateur|Un pas dans l'herbe, puis plus rien.",
            hush,
            "narrateur|Le muret se tait, enfin.",
            "copain|Maintenant !",
            "enfant-m|À toi, puis à moi.",
            "papa|Vous avez laissé le bruit s'asseoir.",
            "maman|L'élan a attendu le silence.",
        )
    clap = {
        1: "narrateur|Victorino lève le filet quand maman ouvre la paume.",
        2: "narrateur|Victorino touche le chapeau quand maman ouvre la paume.",
        3: "narrateur|Victorino lève la fleur quand maman ouvre la paume.",
    }[t1]
    return L(
        "enfant-m|Maman, tu tends la main ?",
        "maman|Je reste, et vous venez tout doux.",
        "narrateur|Aniss écoute la paume, plus que ses pieds.",
        clap,
        "copain|Je m'arrête sur ta main !",
        "enfant-m|Moi aussi, j'écoute.",
        "narrateur|Le clic se range derrière le silence.",
        "papa|Vous avez demandé la main.",
        "maman|Ma paume a tenu l'élan.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le papillon jaune se pose, au bout d'une tige.",
            "copain|On a marché, chacun son tour.",
            "enfant-m|Tu battais des bras, moi j'avançais.",
            "papa|Vous avez laissé l'élan dessiner.",
            "maman|Le pré sent encore le foin.",
            coda,
            "narrateur|Une poudre jaune dort sur l'herbe.",
            "enfant-m|On rentre, Aniss.",
            "narrateur|Le portail de bois cliquette, tout seul.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|L'herbe garde encore la chaleur des genoux.",
            "enfant-m|Tu t'es assis, d'abord.",
            "copain|Puis le jaune est venu, tout droit.",
            "papa|L'élan s'est assis, puis il a guetté.",
            "maman|Le pré redevient calme.",
            coda,
            "narrateur|Une graine reste coincée au tissu.",
            "enfant-m|À demain, les tiges.",
            "narrateur|Le gravier du chemin brille un peu.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le trois de maman reste dans l'air, tout léger.",
            "copain|J'ai attendu le chiffre.",
            "enfant-m|On a demandé, et ça allait.",
            "maman|Mes mots ont tenu vos pieds.",
            "papa|Le pré vous rend le silence.",
            f"narrateur|{o['cap']} pose un grain de jaune sur le bois.",
            "narrateur|Victorino touche la tige, du bout.",
            "copain|Il s'est posé.",
            "narrateur|Une ombre de peuplier barre encore l'herbe.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Deux souffles marquent la même tige violette.",
            "enfant-m|Toi devant, moi derrière.",
            "copain|Tes pas allaient plus loin.",
            "papa|Vous avez soufflé avec l'élan, pas contre.",
            "maman|Les lavandes redeviennent tièdes, et calmes.",
            coda,
            "narrateur|Un brin violet sèche déjà sur le tissu.",
            "enfant-m|On rentre, le parfum reste.",
            "narrateur|Le puits fait une ombre ronde.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le parfum attend encore, tout bas.",
            "copain|J'ai fini, puis c'était toi.",
            "enfant-m|J'ai attendu ta tige.",
            "maman|Chacun son tour, entre les tiges.",
            "papa|L'élan a laissé la place.",
            f"narrateur|{o['cap']} garde un grain de parfum.",
            "narrateur|Victorino souffle dessus, tout doux.",
            "copain|On se dit au revoir, lavandes.",
            "narrateur|Une abeille passe, sans se presser.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|La fleur de papa repose près du violet.",
            "enfant-m|Tu la tendais, un pas chacun.",
            "copain|On a demandé, et ça venait juste.",
            "papa|Ma main a fait le tour, rien de plus.",
            "maman|Les lavandes ont rendu le jaune.",
            coda,
            "narrateur|Un rond clair reste sur une feuille.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|Le chat reprend la pierre, au frais.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le rythme s'arrête, et le jaune se pose.",
            "copain|Toc toc, on est arrivés.",
            "enfant-m|J'avais la main sur ton épaule.",
            "papa|Le muret est redevenu une pierre, simplement.",
            "maman|Le clic s'est couché.",
            coda,
            "narrateur|Une poussière tourne encore, puis tombe.",
            "enfant-m|On rentre, le tambour se tait.",
            "narrateur|Dehors, le pré redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La pierre s'est tue, enfin, tout à fait.",
            "enfant-m|On a attendu en bas.",
            "copain|Quand elle était partie, on s'approchait.",
            "papa|Le silence vous a laissé le jaune.",
            "maman|L'élan a écouté la pierre.",
            f"narrateur|{o['cap']} ne fait plus aucun bruit.",
            "narrateur|Victorino pose la paume sur la pierre chaude.",
            "copain|Elle est tiède.",
            "narrateur|Un oiseau passe au-dessus du muret, sans crier.",
        )
    return L(
        "narrateur|La paume de maman s'ouvre, puis se referme.",
        "enfant-m|J'écoutais ta main.",
        "copain|Moi aussi, je m'arrêtais dessus.",
        "maman|Vous avez demandé le calme.",
        "papa|Le muret a rendu vos pas.",
        coda,
        "narrateur|Victorino touche la pierre, du bout des doigts.",
        "enfant-m|Il s'est posé, Aniss.",
        "narrateur|La pierre garde une poussière, puis plus rien.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une ombre de peuplier barre la cour.",
        "narrateur|Le seau du puits goutte encore.",
        "narrateur|Victorino vit là, avec papa et maman.",
        "narrateur|Le chat a choisi la pierre la plus chaude.",
        "papa|Tu entends le pré, Victorino ?",
        "enfant-m|Ça chante, tout petit.",
        "narrateur|Maman pose un filet vert près du sac.",
        "maman|Il est léger, tu l'as senti ?",
        "enfant-m|Les mailles chatouillent la paume.",
        "narrateur|En ce moment, Victorino touche le chapeau bleu.",
        "enfant-m|Je veux que le papillon jaune se pose.",
        "papa|Avec Aniss, vous le guettez ?",
        "enfant-m|Oui, sur la fleur de papier.",
        "maman|Le filet, le chapeau, et la fleur.",
        "papa|Merci, tu tiens le filet tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près du sac.",
        "narrateur|Le filet, le chapeau, et la fleur.",
        "maman|Tu prends quoi d'abord, Victorino ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le filet vert", "le chapeau bleu", "la fleur de papier")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Victorino a mis {o['lab']} {o['t1q']}.",
            "maman|C'est où, maintenant ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1ans"], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le pré", "les lavandes", "le muret")
        sons[p] = ""
        sons[f"{p}_T0002_P0000"] = ""

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            sons[sp] = "oiseaux" if t2 in (1, 2) else ""
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Victorino veut que le papillon jaune se pose, avec Aniss. "
        "T1 = filet vert / chapeau bleu / fleur de papier (les trois partent). "
        "T2 = pré (herbe, course) / lavandes (parfum, tiges) / muret (clic, pierre). "
        "T3 = neuf résolutions (marcher comme lui, s'asseoir, silence de maman ; "
        "souffler, attendre le parfum, fleur de papa ; "
        "rythme sur la pierre, attendre en bas, main de maman). "
        "L'élan d'Aniss se vit, sans slogan. Fin : le jaune se pose.",
        "N3 ≤ 16. Tom jeté. Titre slogan remplacé (objet + désir). "
        "Autre récit que DIF-023 (pré/lavandes/muret, pas école). "
        "Cuisine/jardin/chambre et cubes/livre/dînette jetés. "
        "Un merci de papa lié au geste (tenir le filet). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
