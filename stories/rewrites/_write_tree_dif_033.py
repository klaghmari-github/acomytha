#!/usr/bin/env python3
"""TREE-DIF-033 — Le cheval doré de Sarah, au carrousel (N2, DIF.ENE.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-033"
N2 = LIMITS["N2"]
TITLE = "Le cheval doré de Sarah, au carrousel"
FIL = (
    "À la fête du village, Sarah veut tourner une fois sur le cheval doré, "
    "avec Aniss. Ils emportent le ticket bleu, l'écharpe à pois et la clochette. "
    "Aniss a trop d'élan : dans la file il saute, au marchepied il bondit, "
    "sur le cheval il veut galoper. Ils jouent avec lui, ils attendent, "
    "ils demandent. Le tour se fait. La crinière d'or se tait."
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
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"sans fin: {ph}")
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
    out["characters"] = "Sarah, Aniss, papa, maman"
    out["setting"] = "fête du village : file, marchepied, cheval doré"
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
        "ce n'est pas une faute",
        "beaucoup d'énergie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "sami",
        "il ne faut pas",
        "hyperactif",
        "camarade qui bouge",
        "lina",
        "capitaine",
        "plic",
        "volet jaune",
        "bac à sable",
        "toboggan",
        "balançoires",
        "marelle",
        "papillon",
        "dans le jardin",
        "la boutique",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
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
        "lab": "le ticket bleu",
        "cap": "Le ticket bleu",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "Le ticket est dans la poche.",
        "coda": "narrateur|Le ticket bleu rentre dans la poche.",
    },
    2: {
        "lab": "l'écharpe à pois",
        "cap": "L'écharpe à pois",
        "t1q": "autour du cou",
        "t1acc": "cou | le cou | autour du cou | son cou",
        "t1retry": "L'écharpe est autour du cou.",
        "coda": "narrateur|L'écharpe à pois rentre autour du cou.",
    },
    3: {
        "lab": "la clochette",
        "cap": "La clochette",
        "t1q": "au poignet",
        "t1acc": "poignet | le poignet | au poignet | son poignet",
        "t1retry": "La clochette est au poignet.",
        "coda": "narrateur|La clochette rentre au poignet.",
    },
}

T3_LABS = {
    1: ("on saute avec lui", "on attend", "papa tient le ticket"),
    2: ("tout doux", "on s'assoit", "maman tient l'écharpe"),
    3: ("on chante", "on attend l'arrêt", "papa tient la barre"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah glisse le ticket bleu, tout droit.",
            "enfant-f|Il sent encore l'encre.",
            "maman|Dans ta poche, près du cœur.",
            "narrateur|Le papier froisse contre le pull.",
            "papa|L'écharpe, ensuite, autour du cou.",
            "narrateur|Aniss prend la clochette, déjà.",
            "narrateur|Tout voyage avec eux, vers la file.",
            "enfant-f|Aniss, viens près des chevaux.",
            "copain|J'arrive, Sarah.",
            "papa|Le ticket d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah enroule l'écharpe à pois, tout doux.",
            "enfant-f|Elle chatouille le cou.",
            "papa|Autour du cou, tout droit.",
            "narrateur|Un pois reste collé au pull.",
            "maman|Le ticket, ensuite, dans la poche.",
            "narrateur|Aniss prend la clochette, déjà.",
            "narrateur|Tout voyage avec eux, vers la file.",
            "enfant-f|Aniss va tout voir.",
            "narrateur|Ses genoux sautent déjà, tout seuls.",
            "copain|Me voilà, Sarah.",
            "enfant-f|On tourne, tous les deux ?",
            "maman|L'écharpe d'abord, elle est prête.",
        )
    return L(
        "narrateur|Sarah noue la clochette au poignet, toc.",
        "enfant-f|Elle est froide, un peu ronde.",
        "maman|Au poignet, tout droit.",
        "narrateur|Un tintement court, puis s'arrête.",
        "papa|Le ticket et l'écharpe, avec vous.",
        "narrateur|Il les pose près des gaufres.",
        "narrateur|Tout voyage avec eux, vers la file.",
        "enfant-f|Aniss, vite !",
        "narrateur|Une ombre trop vive passe au kiosque.",
        "copain|J'arrive près des chevaux.",
        "enfant-f|Je te garde une place.",
        "papa|La clochette d'abord, elle est prête.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La poche veille près du ticket bleu.",
            "copain|Je vois l'encre !",
            "enfant-f|Ne le plie pas encore.",
            "narrateur|Aniss a les cheveux tout courts.",
            "narrateur|Une mèche saute quand il respire.",
            "papa|Ça sent déjà la gaufre, tout près.",
            "maman|Vos mains, au-dessus de la poche ?",
            "copain|Oui, maman.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le cou porte l'écharpe, tout contre le pull.",
            "copain|Elle a trop de pois !",
            "enfant-f|C'est pour le vent du tour.",
            "narrateur|Aniss a les genoux plus vifs que Sarah.",
            "narrateur|Ses pieds tapent déjà le sol peint.",
            "maman|Il a envie de bouger, c'est tout.",
            "papa|On reste près des chevaux ?",
            "enfant-f|Oui, papa.",
        )
    return L(
        "narrateur|La clochette cache encore le pouls.",
        "copain|Ça sent le sucre.",
        "enfant-f|La file de départ est là.",
        "narrateur|Le manteau d'Aniss s'arrête trop haut.",
        "narrateur|Les manches laissent ses poignets libres.",
        "maman|La fête est tiède, autour.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Aniss tapote déjà le sol, tout léger.",
        "narrateur|La file serpente vers les chevaux.",
        "narrateur|Le marchepied brille, un peu haut.",
        "narrateur|Le cheval doré attend, crinière d'or.",
        "papa|On commence où, pour le tour ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Sarah serre le ticket, dans la file.",
            2: "narrateur|Sarah serre l'écharpe, dans la file.",
            3: "narrateur|Sarah serre la clochette, dans la file.",
        }[t1]
        mishap = {
            1: "narrateur|Le ticket bleu tremble, puis glisse.",
            2: "narrateur|Un pois de l'écharpe se défait, un peu.",
            3: "narrateur|La clochette tinte trop fort, trop vite.",
        }[t1]
        return L(
            lead,
            "narrateur|La file sent le sucre et le cuivre.",
            "copain|Moi je saute, Sarah !",
            "narrateur|Aniss saute entre les pieds, trop vite.",
            "narrateur|Un chapeau penche, puis se redresse.",
            mishap,
            f"enfant-f|{o['cap']} n'attendait pas ça.",
            "maman|Il a envie de bouger, c'est tout.",
            "papa|Ses jambes sont plus courtes, plus vives.",
            "copain|On joue comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Sarah pose le ticket près du marchepied.",
            2: "narrateur|Sarah pose l'écharpe près du marchepied.",
            3: "narrateur|Sarah pose la clochette près du marchepied.",
        }[t1]
        mishap = {
            1: "narrateur|Le ticket frôle le bois, trop bas.",
            2: "narrateur|L'écharpe accroche une vis, un instant.",
            3: "narrateur|La clochette tape le fer, toc.",
        }[t1]
        return L(
            lead,
            "enfant-f|Le marchepied est à nous, Aniss.",
            "copain|Je monte le premier, trop vite !",
            "narrateur|Ses pieds quittent le sol, puis reviennent.",
            mishap,
            "narrateur|Un peu de poussière lève, puis retombe.",
            "maman|Il a de l'élan, comme un petit vent.",
            "papa|Toi tu as les jambes plus longues.",
            "enfant-f|On peut jouer avec lui ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Sarah glisse le ticket près de la crinière.",
        2: "narrateur|Sarah noue l'écharpe près de la crinière.",
        3: "narrateur|Sarah pose la clochette près de la crinière.",
    }[t1]
    mishap = {
        1: "narrateur|Le ticket frôle l'or, trop vite.",
        2: "narrateur|L'écharpe claque contre le cou du cheval.",
        3: "narrateur|La clochette tinte trop près de l'oreille.",
    }[t1]
    return L(
        lead,
        "enfant-f|Ici, ça brille, Aniss.",
        "copain|Je galope, trop fort !",
        "narrateur|Le cheval doré penche, un tout petit peu.",
        mishap,
        f"narrateur|{o['cap']} attend au bord, un peu seule.",
        "maman|Son élan remplit tout le tour.",
        "papa|Toi tu vas plus loin, lui plus vite.",
        "copain|On tourne comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Aniss saute encore entre les pieds.",
            "papa|On saute, on attend, ou je tiens le ticket ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le marchepied attend encore, trop vif.",
            "maman|Tout doux, on s'assoit, ou je tiens l'écharpe ?",
        )
    return L(
        "narrateur|La crinière d'or attend encore.",
        "papa|On chante, on attend l'arrêt, ou je tiens la barre ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        play = {
            1: "narrateur|Ils se passent le ticket, dans la file.",
            2: "narrateur|Ils se passent un pois, dans la file.",
            3: "narrateur|Ils se passent la clochette, dans la file.",
        }[t1]
        return L(
            "enfant-f|On saute avec toi, Aniss.",
            "copain|À moi, puis à toi !",
            play,
            "narrateur|Les pieds d'Aniss dansent, pile avec le jeu.",
            "narrateur|Puis Sarah avance d'un pas, tout calme.",
            "papa|Vous avez joué, et la file tient.",
            "maman|L'élan a eu son tour.",
            f"narrateur|{o['cap']} reste dans la paume.",
            "enfant-f|On avance, maintenant.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Aniss s'assoit près du kiosque, un moment.",
            2: "narrateur|Aniss s'assoit près du kiosque, un moment.",
            3: "narrateur|Aniss s'assoit près du kiosque, un moment.",
        }[t1]
        return L(
            "enfant-f|On attend un peu, Aniss.",
            "copain|J'attends, je souffle.",
            wait,
            "narrateur|La file repose, toute ronde, toute sage.",
            "narrateur|Sarah replace le pas, tout doux.",
            "papa|Tes pieds ont su s'asseoir.",
            "maman|Le tour a eu la place.",
            f"narrateur|{o['cap']} ne bouge plus.",
            "enfant-f|Maintenant, c'est à nous.",
        )
    if t2 == 1 and t3 == 3:
        hold = {
            1: "narrateur|Papa tient le ticket, hors de la file.",
            2: "narrateur|Papa tient le ticket, près de l'écharpe.",
            3: "narrateur|Papa tient le ticket, loin de la clochette.",
        }[t1]
        return L(
            "enfant-f|Papa, tu le tiens ?",
            "papa|Je le tiens, Sarah.",
            hold,
            "narrateur|Les mains d'Aniss sont libres, maintenant.",
            "narrateur|Sarah avance d'un pas, pile au milieu.",
            "copain|Je t'aide, sans le ticket.",
            "maman|Vous avez demandé, et ça tient.",
            f"narrateur|{o['cap']} reste près d'eux.",
            "enfant-f|La file est prête.",
        )
    if t2 == 2 and t3 == 1:
        soft = {
            1: "narrateur|Sarah pose le ticket, tout doux, sur le bois.",
            2: "narrateur|Sarah pose l'écharpe, tout doux, sur le bois.",
            3: "narrateur|Sarah pose la clochette, tout doux, sur le bois.",
        }[t1]
        return L(
            "enfant-f|On monte tout doux.",
            "copain|Toi derrière, moi devant !",
            soft,
            "narrateur|Deux ombres montent sur la même marche.",
            "narrateur|Aniss va plus vite, Sarah plus loin.",
            "enfant-f|On arrive en haut, tous les deux.",
            "copain|J'ai attendu ta jambe, un peu.",
            "papa|Vous avez joué avec l'élan.",
            "maman|Le marchepied vous a laissés passer.",
        )
    if t2 == 2 and t3 == 2:
        sit = {
            1: "narrateur|Sarah tient le ticket, sur la marche.",
            2: "narrateur|Sarah tient l'écharpe, sur la marche.",
            3: "narrateur|Sarah tient la clochette, sur la marche.",
        }[t1]
        return L(
            "enfant-f|On s'assoit un peu.",
            "copain|Moi je m'assois, puis c'est toi.",
            sit,
            "narrateur|Aniss pose les genoux sur le bois.",
            "narrateur|Il souffle, puis il se lève.",
            "copain|C'est à toi, Sarah.",
            "enfant-f|Merci, j'y vais.",
            "papa|Chacun son tour, sur la marche.",
            "maman|L'élan a attendu le bois.",
        )
    if t2 == 2 and t3 == 3:
        scarf = {
            1: "narrateur|Maman tient l'écharpe, près du ticket.",
            2: "narrateur|Maman tient l'écharpe, dans sa paume.",
            3: "narrateur|Maman tient l'écharpe, près de la clochette.",
        }[t1]
        return L(
            "enfant-f|Maman, tu tiens l'écharpe ?",
            "maman|Je la donne, un coup chacun.",
            scarf,
            "narrateur|Aniss la reçoit, monte un pas.",
            "narrateur|Sarah la reçoit, monte plus loin.",
            "copain|On demande, et ça va !",
            "enfant-f|Le haut est à nous.",
            "papa|Vous avez demandé, tout calme.",
            "maman|Ma main a juste attendu.",
        )
    if t2 == 3 and t3 == 1:
        song = {
            1: "narrateur|Le ticket bleu voyage dans la poche, entre deux notes.",
            2: "narrateur|L'écharpe à pois voyage au cou, entre deux notes.",
            3: "narrateur|La clochette voyage au poignet, entre deux notes.",
        }[t1]
        return L(
            "enfant-f|On chante, Aniss.",
            "copain|La la la, j'avance !",
            "narrateur|Sarah pose une main sur l'épaule d'Aniss.",
            song,
            "narrateur|Ils chantent la même valse, l'un près de l'autre.",
            "enfant-f|Doucement, le cheval tient.",
            "copain|La musique suit, puis se tait.",
            "papa|Vous jouez avec le bruit, ensemble.",
            "maman|Le tour est devenu une chanson.",
        )
    if t2 == 3 and t3 == 2:
        hush = {
            1: "narrateur|Le ticket bleu reste muet, au creux.",
            2: "narrateur|L'écharpe à pois reste muette, au creux.",
            3: "narrateur|La clochette reste muette, au creux.",
        }[t1]
        return L(
            "enfant-f|On attend l'arrêt.",
            "copain|Quand il s'arrête, on galope un peu.",
            hush,
            "narrateur|Le cheval doré ralentit, tout seul.",
            "narrateur|Aniss souffle, puis il sourit.",
            "copain|C'est à nous, maintenant.",
            "enfant-f|Un tour, tout calme.",
            "papa|Vous avez attendu la musique.",
            "maman|L'élan a écouté le bois.",
        )
    bar = {
        1: "narrateur|Papa tient la barre, près du ticket.",
        2: "narrateur|Papa tient la barre, près de l'écharpe.",
        3: "narrateur|Papa tient la barre, près de la clochette.",
    }[t1]
    return L(
        "enfant-f|Papa, tu tiens la barre ?",
        "papa|Je la tiens, tout ferme.",
        bar,
        "narrateur|Aniss pose les deux mains, tout près.",
        "narrateur|Sarah pose les siennes, plus loin.",
        "copain|On demande, et ça tient !",
        "enfant-f|La crinière est à nous.",
        "maman|Vous avez demandé, tout calme.",
        "papa|Ma barre a juste attendu.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        keep = {
            1: "narrateur|Le ticket bleu garde un grain de sucre.",
            2: "narrateur|L'écharpe à pois garde un grain de sucre.",
            3: "narrateur|La clochette garde un grain de sucre.",
        }[t1]
        return L(
            "narrateur|La file s'ouvre, enfin, vers le bois peint.",
            "copain|On a sauté, puis on a avancé.",
            "enfant-f|Tes pieds ont dansé avec le jeu.",
            "papa|Vous l'avez, le tour.",
            "maman|La gaufre attend encore, au kiosque.",
            keep,
            "enfant-f|On reste un peu, Aniss.",
            "narrateur|Un rai orange s'endort sur la crinière.",
            "narrateur|Le cuivre redevient doux, autour.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Au bord de la file, deux têtes se calment.",
            "enfant-f|Aniss, tu as su t'asseoir.",
            "copain|Oui, tout près de tes mains.",
            "papa|Toi debout, lui assis, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            f"narrateur|{o['cap']} reste dans la paume de Sarah.",
            "copain|Je reste encore un peu.",
            "narrateur|Un pois de sucre colle aux cheveux.",
            "narrateur|Le kiosque sent encore la gaufre.",
        )
    if t2 == 1 and t3 == 3:
        keep = {
            1: "narrateur|Le ticket bleu retombe, tout léger.",
            2: "narrateur|L'écharpe à pois retombe, toute légère.",
            3: "narrateur|La clochette retombe, toute légère.",
        }[t1]
        return L(
            "narrateur|Papa rend le ticket, tout doux.",
            "copain|Il est tombé vers nous.",
            "enfant-f|On a demandé, tous les deux.",
            "maman|Il n'était plus trop loin.",
            "papa|Le papier froisse encore, dans l'air.",
            keep,
            "enfant-f|On souffle dessus, tout calme.",
            "narrateur|Un pois d'or veille près des chevaux.",
            "narrateur|La valse se tait, contre le bois.",
        )
    if t2 == 2 and t3 == 1:
        keep = {
            1: "narrateur|Le ticket bleu garde un brin de poussière.",
            2: "narrateur|L'écharpe à pois garde un brin de poussière.",
            3: "narrateur|La clochette garde un brin de poussière.",
        }[t1]
        return L(
            "narrateur|Sur le marchepied, ça sent le bois chaud.",
            "copain|Mes pieds savaient le chemin.",
            "enfant-f|Moi, je montais plus loin.",
            "papa|Vous avez suivi ce qui était à vous.",
            "maman|Un brin de poussière reste au pull.",
            keep,
            "enfant-f|Il est pour demain, le tour.",
            "copain|Il est un peu chaud encore.",
            "narrateur|L'ombre du cheval s'allonge, puis s'arrête.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Deux genoux restent, comme deux murs.",
            "enfant-f|J'ai poussé d'en bas.",
            "copain|Tes bras étaient assez longs.",
            "maman|Le bois sent fort, sur vos mains.",
            "papa|Frottez-les sur le pantalon, tout doux.",
            f"narrateur|{o['cap']} garde un brin de poussière.",
            "copain|Je le tiens, Sarah.",
            "narrateur|Une vis grince, puis se tait.",
            "narrateur|Le pois sèche près du kiosque.",
        )
    if t2 == 2 and t3 == 3:
        keep = {
            1: "narrateur|Le ticket bleu marque encore le bois.",
            2: "narrateur|L'écharpe à pois marque encore le bois.",
            3: "narrateur|La clochette marque encore le bois.",
        }[t1]
        return L(
            "narrateur|Une voix en haut, une voix en bas, puis plus.",
            "enfant-f|Maman a tendu l'écharpe.",
            "copain|On s'est parlé à travers.",
            "papa|Le marchepied vous a laissé la place.",
            "maman|Le secret tient encore, tout chaud.",
            keep,
            "enfant-f|Regarde-le, Aniss, il brille.",
            "copain|Je le vois, d'ici.",
            "narrateur|Le pois reste au chaud, sur la marche.",
        )
    if t2 == 3 and t3 == 1:
        keep = {
            1: "narrateur|Le ticket bleu pèse encore dans la poche.",
            2: "narrateur|L'écharpe à pois pèse encore au cou.",
            3: "narrateur|La clochette pèse encore au poignet.",
        }[t1]
        return L(
            "narrateur|Les talons d'Aniss sont encore chauds.",
            "enfant-f|Tu as chanté pour moi.",
            "copain|Tu tenais mon épaule.",
            "maman|La crinière sent le vernis, tout près.",
            "papa|Le tour est à vous, maintenant.",
            keep,
            "narrateur|Sarah la pose contre le bois peint.",
            "narrateur|Un rai d'or traverse le pois.",
            "narrateur|La valse redevient calme, toute seule.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sur le cheval, deux paires de pieds se touchent.",
            "copain|Tu as attendu l'arrêt.",
            "enfant-f|Tes mains ont su ralentir.",
            "papa|Chacun a fait sa part, à son rythme.",
            "maman|Le tissu de l'écharpe sèche déjà.",
            f"narrateur|{o['cap']} pose une ombre au bois.",
            "copain|Il brille trop, Sarah.",
            "enfant-f|C'est pour ça.",
            "narrateur|La crinière garde le pois, tout proche.",
        )
    return L(
        "narrateur|Un peu de vernis reste aux paumes.",
        "enfant-f|On a tenu ensemble.",
        "copain|Sans trop galoper.",
        "papa|La barre est restée à sa place.",
        "maman|Vos mains sentent encore le bois.",
        coda,
        "copain|Tu l'as eue, enfin.",
        "enfant-f|Elle est à nous.",
        "narrateur|L'or tremble un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le kiosque sent encore la gaufre sucrée.",
        "narrateur|Un cuivre joue une valse, tout près.",
        "narrateur|Les chevaux peints brillent, or et rouge.",
        "papa|Tu as vu la crinière, Sarah ?",
        "enfant-f|Elle est toute en or.",
        "maman|Le ticket bleu attend dans ma poche.",
        "narrateur|En ce moment, Sarah touche le bois du cheval.",
        "enfant-f|Je veux tourner, une fois, avec Aniss.",
        "papa|Aniss arrive, les pieds déjà en danse.",
        "narrateur|Aniss a les genoux qui sautent, tout seuls.",
        "copain|On y va, Sarah ?",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu tiens le ticket tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du kiosque.",
        "narrateur|Le ticket, l'écharpe, et la clochette.",
        "maman|Tu prends quoi d'abord, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le ticket bleu", "l'écharpe à pois", "la clochette")

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
        extras[f"{p}_T0002_P0000"] = t3lab("la file", "le marchepied", "le cheval doré")
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
        "À la fête du village, Sarah veut tourner une fois sur le cheval doré, "
        "avec Aniss. T1 = ticket bleu / écharpe à pois / clochette "
        "(les trois partent). T2 = file (sauts, ticket qui glisse) / "
        "marchepied (bond, vis) / cheval doré (galop, crinière). "
        "T3 = neuf résolutions (sauter avec lui, attendre, papa tient le ticket ; "
        "tout doux, s'asseoir, maman tient l'écharpe ; "
        "chanter, attendre l'arrêt, papa tient la barre). "
        "L'élan d'Aniss se vit, sans slogan. Fin : le tour, l'or se tait.",
        "N2 ≤ 15. Lina hors troupe → Sarah + Aniss (D16). "
        "Jardin / bac / toboggan / balançoires jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-019/023/029 "
        "(carrousel, pas marché, pas école, pas papillon). "
        "Un merci de papa lié au geste (tenir le ticket). Pas de « bon travail ». "
        "Audio non cuit.",
    )


if __name__ == "__main__":
    main()
