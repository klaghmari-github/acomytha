#!/usr/bin/env python3
"""TREE-DIF-041 — Le pain tiède d'Amir, jusqu'à la mer (N1, DIF.BES.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-041"
N1 = LIMITS["N1"]
TITLE = "Le pain tiède d'Amir, jusqu'à la mer"
FIL = (
    "Amir veut montrer la mer à Nina, depuis le wagon. "
    "Il s'installe d'abord à la vitre, à la tablette ou près de la porte ; "
    "le voyage change. Nina dessine une vache, croque sa pomme, ou attend "
    "le sifflet. Il propose, et il accepte oui, plus tard, ou une autre idée. "
    "Le pain tiède, puis le sel."
)
CHARS = "Amir, Nina, papa, maman"
SETTING = "gare du village, wagon : vitre, tablette, porte"


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
        "inviter sans forcer",
        "accepter plusieurs",
        "kenzo",
        "coussin",
        "le fort",
        "tomate",
        "panier rouge",
        "figuier",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
        "capitaine",
        "plic",
        "volet jaune",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob or "nina" not in blob:
        raise SystemExit(f"{SID}: troupe Amir/Nina absente")
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


T1 = {
    1: {
        "lab": "la vitre",
        "cap": "La vitre",
        "ans": "champs",
        "acc": "champs | les champs | dehors | les arbres | un arbre",
        "retry": "Il regarde les champs.",
        "coda": "La vitre garde encore un peu de sel.",
    },
    2: {
        "lab": "la tablette",
        "cap": "La tablette",
        "ans": "tablette",
        "acc": "tablette | la tablette | le bois | le pain",
        "retry": "Il a déplié la tablette.",
        "coda": "La tablette garde une miette tiède.",
    },
    3: {
        "lab": "la porte",
        "cap": "La porte",
        "ans": "porte",
        "acc": "porte | la porte | près de la porte | la barre",
        "retry": "Il se tient près de la porte.",
        "coda": "La porte garde encore un peu de vent.",
    },
}

T3_LABS = {
    1: ("attendre un peu", "parler tout bas", "dessiner à côté"),
    2: ("attendre la fin", "proposer le pain", "garder le sien"),
    3: ("écouter ensemble", "un tout petit jeu", "proposer plus tard"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir se colle d'abord à la vitre.",
            "enfant-m|Les champs courent, tout vite.",
            "maman|Pose ton sac, tout doux.",
            "narrateur|Un arbre passe, puis un autre.",
            "papa|Tu vois déjà la mer ?",
            "enfant-m|Pas encore, papa.",
            "narrateur|Le clic des rails rentre dans le ventre.",
            "enfant-m|Nina va tout voir, avec moi.",
            "papa|Tu l'invites, quand tu la trouves ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir déplie d'abord la tablette.",
            "enfant-m|Elle fait un petit toc.",
            "papa|Tiens-la, elle tremble un peu.",
            "narrateur|Le pain tiède pose son papier.",
            "maman|Les miettes vont dans le sac.",
            "narrateur|Le bois sent encore le savon.",
            "enfant-m|Nina va aimer le pain.",
            "maman|Tu lui proposes, tout calme ?",
            "enfant-m|Oui, maman.",
            "papa|On est bien, ici.",
        )
    return L(
        "narrateur|Amir s'approche d'abord de la porte.",
        "enfant-m|Ça souffle un peu, ici.",
        "maman|Tiens la barre, tout doux.",
        "narrateur|Le wagon penche, puis se redresse.",
        "papa|Les rails passent, tout près.",
        "narrateur|Un sifflet lointain, déjà.",
        "enfant-m|Nina va aimer le vent.",
        "papa|Tu l'invites, tout calme ?",
        "enfant-m|Oui.",
        "maman|La barre est froide, encore.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir a collé son nez.",
            "maman|Il regarde quoi, Amir ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le petit toc est déjà fait.",
            "papa|Il a déplié quoi ?",
        )
    return L(
        "narrateur|La barre reste froide, sous la main.",
        "maman|Il se tient près de quoi ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Les champs.",
            "maman|Oui.",
            "narrateur|La vitre tremble un peu, tout doux.",
            "narrateur|Un toit rouge passe, déjà loin.",
            "enfant-m|Nina est dans le wagon.",
            "papa|Je l'entends, plus loin.",
            "maman|Vous allez la trouver.",
            "enfant-m|Je lui propose la mer.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La tablette.",
            "papa|Oui.",
            "narrateur|Le pain tiède chauffe encore le papier.",
            "narrateur|Une miette roule, puis s'arrête.",
            "enfant-m|Nina est dans le wagon.",
            "maman|Je l'entends, plus loin.",
            "papa|Le bois tient bien, maintenant.",
            "enfant-m|Je lui propose le pain.",
        )
    return L(
        "enfant-m|La porte.",
        "maman|Oui.",
        "narrateur|Un peu d'air entre, tout frais.",
        "narrateur|Les rails claquent, tout près.",
        "enfant-m|Nina est dans le wagon.",
        "papa|Je l'entends, plus loin.",
        "maman|La barre reste sous ta main.",
        "enfant-m|Je lui propose le vent.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Nina est dans le wagon, déjà.",
        "narrateur|Son carnet est ouvert, tout près.",
        "narrateur|Une pomme croque, plus loin.",
        "narrateur|Le sifflet peut encore arriver.",
        "papa|On va vers quoi, Amir ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        if t1 == 1:
            return L(
                "narrateur|Amir revient vers la vitre, tout doux.",
                "narrateur|Nina dessine une vache, tout absorbée.",
                "enfant-m|Nina, la mer arrive bientôt.",
                "narrateur|Elle ne lève pas encore les yeux.",
                "copine|Ma vache n'est pas finie.",
                "enfant-m|Tu viens voir les champs ?",
                "copine|Je n'ai pas fini.",
                "maman|Elle dessine encore, tout concentrée.",
                "papa|Tu proposes comment, Amir ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Amir pose le pain près du carnet.",
                "narrateur|Nina tient encore son crayon.",
                "enfant-m|Nina, le pain est tiède.",
                "narrateur|Une tache bleue sèche sur le papier.",
                "copine|Ma vache n'est pas finie.",
                "enfant-m|Tu viens à la tablette ?",
                "copine|Je n'ai pas fini.",
                "papa|Elle reste dans son dessin.",
                "maman|Tu proposes comment, Amir ?",
            )
        return L(
            "narrateur|Le papier claque un peu, près de la porte.",
            "narrateur|Nina dessine sur ses genoux.",
            "enfant-m|Nina, le vent est bon.",
            "narrateur|Le crayon glisse, puis reprend.",
            "copine|Ma vache n'est pas finie.",
            "enfant-m|Tu viens à la barre ?",
            "copine|Je n'ai pas fini.",
            "maman|Le vent agite encore la feuille.",
            "papa|Tu proposes comment, Amir ?",
        )
    if t2 == 2:
        if t1 == 1:
            return L(
                "narrateur|Une pomme croque, tout contre la vitre.",
                "narrateur|Nina mange lentement, les yeux dehors.",
                "enfant-m|Nina, les champs courent.",
                "copine|J'ai pas fini ma pomme.",
                "enfant-m|Tu viens coller ton nez ?",
                "copine|Après, peut-être.",
                "narrateur|Le jus brille un peu, au coin.",
                "maman|Elle croque encore, tout calme.",
                "papa|Tu proposes comment, Amir ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Nina a déjà sa pomme, à la tablette.",
                "narrateur|Le pain tiède attend, tout près.",
                "enfant-m|Nina, tu veux du pain ?",
                "copine|J'ai ma pomme, encore.",
                "enfant-m|On partage ?",
                "copine|Pas maintenant.",
                "narrateur|Deux goûters, trop loin l'un de l'autre.",
                "papa|Elle n'a pas fini, Amir.",
                "maman|Tu proposes comment, alors ?",
            )
        return L(
            "narrateur|Nina croque près de la porte, debout.",
            "narrateur|Le jus coule un peu, sur le pouce.",
            "enfant-m|Nina, le vent est bon.",
            "copine|J'ai pas fini ma pomme.",
            "enfant-m|Tu viens à la barre ?",
            "copine|Après, peut-être.",
            "narrateur|La pomme avance, tout lente.",
            "maman|Elle mange encore, tout concentrée.",
            "papa|Tu proposes comment, Amir ?",
        )
    if t1 == 1:
        return L(
            "narrateur|Nina colle l'oreille, tout contre la vitre.",
            "copine|J'attends le sifflet, Amir.",
            "enfant-m|La mer arrive, après.",
            "narrateur|Elle ne bouge pas encore.",
            "enfant-m|Tu viens voir les champs ?",
            "copine|Quand ça siffle, d'abord.",
            "papa|Elle écoute le rail, tout dur.",
            "maman|Le sifflet n'est pas là.",
            "papa|Tu proposes comment, Amir ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina quitte la tablette, l'oreille tendue.",
            "copine|J'attends le sifflet, Amir.",
            "enfant-m|Le pain est encore tiède.",
            "narrateur|Elle ne s'assoit plus.",
            "enfant-m|Tu reviens manger ?",
            "copine|Quand ça siffle, d'abord.",
            "maman|Elle écoute le wagon, tout tendue.",
            "papa|Le sifflet n'est pas là.",
            "maman|Tu proposes comment, Amir ?",
        )
    return L(
        "narrateur|Nina se tient près de la porte, déjà.",
        "copine|J'attends le sifflet, Amir.",
        "enfant-m|Ça souffle trop, ici.",
        "narrateur|Elle serre la barre, tout calme.",
        "enfant-m|Tu restes avec moi ?",
        "copine|Quand ça siffle, d'abord.",
        "papa|Elle écoute le rail, tout près.",
        "maman|Le sifflet n'est pas là.",
        "papa|Tu proposes comment, Amir ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le crayon de Nina reste en l'air.",
            "papa|Attendre, parler tout bas, ou dessiner ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La pomme n'est pas finie.",
            "maman|Attendre, proposer le pain, ou garder ?",
        )
    return L(
        "narrateur|Le sifflet n'est pas encore là.",
        "papa|Écouter, un petit jeu, ou plus tard ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Les champs courent encore, tout seuls.",
            2: "narrateur|Le pain tiède attend, sans bouger.",
            3: "narrateur|Le vent de la porte passe, déjà.",
        }[t1]
        return L(
            "enfant-m|J'attends un peu.",
            "copine|Merci, Amir.",
            "narrateur|Le crayon reprend la tache bleue.",
            wait,
            "narrateur|Nina pose le crayon, enfin.",
            "copine|Ma vache est finie, maintenant.",
            "enfant-m|Tu viens, alors ?",
            "copine|Oui.",
            "papa|Tu as laissé sa vache finir.",
        )
    if t2 == 1 and t3 == 2:
        near = {
            1: "narrateur|Il parle tout contre la vitre.",
            2: "narrateur|Il parle tout contre la tablette.",
            3: "narrateur|Il parle tout contre la barre.",
        }[t1]
        return L(
            "enfant-m|Nina, je te propose la mer.",
            near,
            "narrateur|Sa voix reste tout bas, près d'elle.",
            "copine|J'ai entendu, Amir.",
            "enfant-m|Tu peux dire non.",
            "copine|Oui, je viens.",
            "narrateur|Elle ferme le carnet, tout doux.",
            "papa|Ta voix est restée tout bas.",
            "maman|Elle a choisi d'elle-même.",
        )
    if t2 == 1 and t3 == 3:
        sit = {
            1: "narrateur|Amir s'assoit près de la vitre.",
            2: "narrateur|Amir s'assoit près de la tablette.",
            3: "narrateur|Amir s'assoit près de la barre.",
        }[t1]
        return L(
            "enfant-m|Je dessine à côté.",
            sit,
            "narrateur|Il ne prend pas le crayon.",
            "copine|Tu fais un pré, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Deux vaches, maintenant, sur le papier.",
            "copine|Après, on va voir la mer.",
            "papa|Tu es resté près d'elle.",
            "maman|Elle a proposé la suite.",
        )
    if t2 == 2 and t3 == 1:
        wait = {
            1: "narrateur|La vitre garde les champs, encore.",
            2: "narrateur|Le pain tiède garde son papier.",
            3: "narrateur|La barre reste froide, sous la main.",
        }[t1]
        return L(
            "enfant-m|J'attends la fin.",
            "copine|Merci, Amir.",
            wait,
            "narrateur|La pomme devient un petit trognon.",
            "copine|C'est fini, maintenant.",
            "enfant-m|Tu viens, alors ?",
            "copine|Oui.",
            "papa|Tu as laissé sa pomme finir.",
            "maman|Elle a dit oui, à son heure.",
        )
    if t2 == 2 and t3 == 2:
        offer = {
            1: "narrateur|Il tend le pain, près de la vitre.",
            2: "narrateur|Il tend le pain, sur la tablette.",
            3: "narrateur|Il tend le pain, près de la porte.",
        }[t1]
        return L(
            "enfant-m|Nina, tu veux du pain ?",
            offer,
            "copine|Un tout petit bout, alors.",
            "enfant-m|D'accord.",
            "narrateur|Le papier craque, tout doux.",
            "copine|Il est encore tiède.",
            "enfant-m|On est deux, maintenant.",
            "papa|Le pain est resté dans sa main.",
            "maman|Elle a pris ce qu'elle voulait.",
        )
    if t2 == 2 and t3 == 3:
        side = {
            1: "narrateur|Le pain reste près de la vitre.",
            2: "narrateur|Le pain reste sur la tablette.",
            3: "narrateur|Le pain reste près de la porte.",
        }[t1]
        return L(
            "copine|Pas de pain, Amir.",
            "enfant-m|D'accord.",
            "enfant-m|Je garde le mien, alors.",
            side,
            "narrateur|Il croque de son côté, tout calme.",
            "copine|Tu peux parler, d'ici.",
            "enfant-m|Je reste près de toi.",
            "papa|Tu as gardé ton pain.",
            "maman|Vous êtes encore ensemble.",
        )
    if t2 == 3 and t3 == 1:
        listen = {
            1: "narrateur|Deux oreilles, maintenant, contre la vitre.",
            2: "narrateur|Deux oreilles, maintenant, près de la tablette.",
            3: "narrateur|Deux oreilles, maintenant, près de la porte.",
        }[t1]
        return L(
            "enfant-m|J'écoute avec toi.",
            listen,
            "narrateur|Le rail chante, tout bas.",
            "copine|Tu entends, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Un sifflet arrive, enfin, tout long.",
            "copine|C'est lui !",
            "papa|Tu as écouté à son heure.",
            "maman|Vous l'avez eu, tous les deux.",
        )
    if t2 == 3 and t3 == 2:
        game = {
            1: "narrateur|Ils comptent les arbres, à la vitre.",
            2: "narrateur|Ils comptent les miettes, à la tablette.",
            3: "narrateur|Ils comptent les clics, à la porte.",
        }[t1]
        return L(
            "enfant-m|Un tout petit jeu, Nina ?",
            "copine|Très petit, alors.",
            "enfant-m|D'accord.",
            game,
            "narrateur|Ils comptent jusqu'à trois, tout bas.",
            "narrateur|Le sifflet coupe le trois, pile.",
            "copine|C'est lui !",
            "papa|Tu as proposé court, juste assez.",
            "maman|Le sifflet a dit la fin.",
        )
    later = {
        1: "narrateur|La vitre garde sa place, tout calme.",
        2: "narrateur|La tablette garde sa place, tout calme.",
        3: "narrateur|La porte garde sa place, tout calme.",
    }[t1]
    return L(
        "enfant-m|On regarde plus tard, alors ?",
        "copine|Oui, plus tard.",
        "enfant-m|D'accord.",
        later,
        "narrateur|Nina serre encore l'oreille.",
        "copine|Garde la mer pour moi.",
        "enfant-m|Elle t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Elle a dit oui, pour plus tard.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{T1[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Une ligne bleue arrive, tout au fond.",
            "copine|C'est la mer, Amir ?",
            "enfant-m|Oui, elle est là.",
            "papa|Vous avez attendu le bon moment.",
            "maman|Le pain est encore un peu tiède.",
            coda,
            "narrateur|Nina souffle sur le sel, tout petit.",
            "enfant-m|C'est notre mer, maintenant.",
            "narrateur|Un peu de sel reste sur le dessin.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le carnet est fermé, contre le genou.",
            "enfant-m|Tu as dit oui, tout bas.",
            "copine|J'avais entendu, près de toi.",
            "papa|Ta voix est restée tout bas.",
            "maman|Mangez un peu, tout doux.",
            coda,
            "narrateur|Nina pose sa joue, tout calme.",
            "enfant-m|Reste autant que tu veux.",
            "narrateur|La vache du carnet regarde la mer.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Après le pré, la mer entre au crayon.",
            "copine|On a dessiné ensemble, d'abord.",
            "enfant-m|Puis tu as dit : on y va.",
            "maman|Deux vaches, puis une ligne bleue.",
            "papa|Le wagon redevient calme.",
            coda,
            "narrateur|Nina rit, tout petit.",
            "enfant-m|La mer t'a attendue.",
            "narrateur|Deux crayons se touchent, tout calme.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le trognon part dans le sac.",
            "copine|J'ai fini, Amir.",
            "enfant-m|Tu as dit oui.",
            "papa|Vous tenez tous les deux, maintenant.",
            "maman|Le pain descend jusqu'à vous.",
            coda,
            "narrateur|Nina tape deux fois, tout doux.",
            "enfant-m|C'est le signal.",
            "narrateur|Le trognon de pomme sent encore le sucre.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le pain a deux bouts, maintenant.",
            "enfant-m|Le tien, et le mien.",
            "copine|Il était tiède, Amir.",
            "papa|Vous avez partagé sans tout casser.",
            "maman|La mer, au fond, pour deux.",
            coda,
            "narrateur|Nina souffle, puis Amir souffle.",
            "enfant-m|On reste encore un peu.",
            "narrateur|Une miette tiède dort sur le bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Deux goûters restent côte à côte.",
            "copine|Tu n'as pas pris ma pomme.",
            "enfant-m|Tu avais dit non.",
            "papa|Sa pomme est restée à elle.",
            "maman|Vous vous parlez encore, d'ici.",
            coda,
            "narrateur|Nina tend un bout de pomme, alors.",
            "enfant-m|Je le prends, d'à côté.",
            "narrateur|Deux goûters se parlent, tout calme.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le sifflet s'en va, tout loin.",
            "copine|On l'a eu, ensemble.",
            "enfant-m|Puis la mer est arrivée.",
            "papa|Vous avez écouté à son heure.",
            "maman|Le pain attend encore, tout doux.",
            coda,
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|La mer t'a vue, une minute.",
            "narrateur|Un oiseau blanc passe, tout loin.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le petit jeu est déjà fini.",
            "copine|Le sifflet a coupé le trois.",
            "enfant-m|Merci d'avoir joué.",
            "papa|Vous avez compté juste assez.",
            "maman|La mer entre, maintenant.",
            coda,
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|On l'a vue, une minute.",
            "narrateur|Le clic des rails reprend, tout doux.",
        )
    return L(
        "narrateur|Nina écoute encore, un instant.",
        "enfant-m|Plus tard, elle a dit.",
        "enfant-m|Garde la mer pour moi.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le pain attend, tout doux.",
        coda,
        "narrateur|Amir garde une place, tout calme.",
        "enfant-m|Elle t'attend, Nina.",
        "narrateur|Le vent de la mer entre, déjà.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La gare sent le café, tout chaud.",
        "narrateur|Les pierres du quai sont encore mouillées.",
        "narrateur|Un train long attend, tout calme.",
        "papa|Les billets sont dans ma poche.",
        "maman|Le pain est encore tiède, Amir.",
        "narrateur|Les rails brillent un peu, au soleil.",
        "papa|Nina est déjà dans le wagon.",
        "enfant-m|Je veux lui montrer la mer.",
        "narrateur|En ce moment, Amir monte la marche.",
        "maman|Le marchepied est haut, tout doux.",
        "papa|Merci, tu tiens le sac bien.",
        "enfant-m|On va jusqu'à la mer.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le wagon sent le pain, déjà.",
        "narrateur|La vitre, la tablette, ou la porte.",
        "papa|On s'assoit où, Amir ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la vitre", "la tablette", "la porte")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = T1[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le carnet", "la pomme", "le sifflet")

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
        "Amir veut montrer la mer à Nina depuis le wagon. "
        "T1 = vitre (champs) / tablette (pain) / porte (vent) : le voyage change. "
        "T2 = carnet (vache à finir) / pomme (pas prête) / sifflet (elle écoute). "
        "T3 = neuf résolutions : attendre, proposer tout bas, dessiner à côté ; "
        "attendre la pomme, proposer le pain, garder le sien (accepter le non) ; "
        "écouter ensemble, petit jeu, plus tard. "
        "La leçon se vit : il propose, il accepte oui, non, ou une autre idée. "
        "Fin : mer, pain tiède, sel.",
        "N1 ≤ 10. Kenzo et le slogan « Inviter sans forcer » jetés. "
        "Autre récit que DIF-021 (pas de fort, pas de coussins) et DIF-031 "
        "(pas de potager, pas de tomates). Un merci de papa lié au geste "
        "(tenir le sac). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
