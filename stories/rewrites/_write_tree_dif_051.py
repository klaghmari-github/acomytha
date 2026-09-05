#!/usr/bin/env python3
"""TREE-DIF-051 — Les deux voyageurs de Chouchou, jusqu'au tunnel (N3, DIF.COR.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-051"
N3 = LIMITS["N3"]
TITLE = "Les deux voyageurs de Chouchou, jusqu'au tunnel"
FIL = (
    "Le soir, le train de montagne. Chouchou veut que son hérisson tout rond "
    "et son renard de bois tout mince voient le tunnel ensemble. Elle prépare "
    "d'abord le châle bleu, la boîte à biscuits ou la ficelle de laine ; les "
    "trois partent. Au filet, sur la banquette chaude, ou dans le passage : "
    "neuf façons de les garder ensemble. Le noir, puis la neige."
)
CHARS = "Chouchou, papa, maman"
SETTING = "gare de colline, train de montagne : filet, banquette, passage"


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
        "plus rond ou plus mince",
        "corps pas une blague",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "capitaine",
        "plic",
        "volet jaune",
        "poupée",
        "canard",
        "la mer",
        "pain tiède",
        "savon",
        "lavande",
        "la mare",
        "lina",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    if "hérisson" not in blob or "renard" not in blob:
        raise SystemExit(f"{SID}: voyageurs absents")
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
        "lab": "le châle bleu",
        "cap": "Le châle bleu",
        "ans": "autour",
        "acc": "autour | autour d'eux | autour des deux | sur eux | le châle",
        "retry": "Le châle est autour des deux.",
        "coda": "Un brin de laine bleue reste au chaud.",
    },
    2: {
        "lab": "la boîte à biscuits",
        "cap": "La boîte à biscuits",
        "ans": "genoux",
        "acc": "genoux | les genoux | sur les genoux | la boîte",
        "retry": "La boîte est sur les genoux.",
        "coda": "Une miette de biscuit dort encore.",
    },
    3: {
        "lab": "la ficelle de laine",
        "cap": "La ficelle de laine",
        "ans": "nœud",
        "acc": "nœud | le nœud | un nœud | autour | la ficelle",
        "retry": "La ficelle fait un nœud, tout doux.",
        "coda": "Le nœud de laine reste un peu tiède.",
    },
}

T3_LABS = {
    1: ("le nid de laine", "la boîte dans le filet", "contre soi"),
    2: ("la vallée du châle", "la maison-boîte", "la ficelle au dossier"),
    3: ("contre la poitrine", "sur la marche", "attendre le calme"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Chouchou prend d'abord le châle bleu, encore tiède.",
            "enfant-f|Il sent la maison.",
            "maman|Enroule-les tous les deux, tout doux.",
            "narrateur|Le hérisson rond disparaît dans la laine.",
            "narrateur|Le museau mince du renard dépasse encore.",
            "enfant-f|Je vois deux têtes.",
            "papa|La boîte viendra aussi, dans le sac.",
            "narrateur|La ficelle attend près de la fermeture.",
            "enfant-f|On prend tout.",
            "narrateur|Châle, boîte et ficelle montent avec elle.",
        )
    if t1 == 2:
        return L(
            "narrateur|Chouchou ouvre d'abord la boîte à biscuits, clic.",
            "enfant-f|Ça sent le beurre, encore.",
            "papa|Pose-les dedans, tous les deux.",
            "narrateur|Le hérisson rond prend presque toute la place.",
            "narrateur|Le renard mince se glisse le long du bord.",
            "enfant-f|Ils tiennent, côte à côte.",
            "maman|Le châle viendra aussi, par-dessus.",
            "narrateur|La ficelle attend près de la fermeture.",
            "enfant-f|Je garde la boîte.",
            "narrateur|Les trois affaires montent avec elle.",
        )
    return L(
        "narrateur|Chouchou saisit d'abord la ficelle de laine, un peu rêche.",
        "enfant-f|Elle chatouille le poignet.",
        "maman|Un nœud doux, autour des deux.",
        "narrateur|Le hérisson rond se laisse lier, tout calme.",
        "narrateur|Le renard mince reste collé contre lui.",
        "enfant-f|Ils tiennent ensemble.",
        "papa|Le châle et la boîte viennent aussi.",
        "narrateur|Elle les glisse dans le sac, tout près.",
        "enfant-f|La ficelle d'abord.",
        "narrateur|Les trois affaires montent avec elle.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le châle bleu est autour des deux voyageurs.",
            "maman|Il est où, maintenant ?",
        )
    if t1 == 2:
        return L(
            "narrateur|La boîte à biscuits repose sur les genoux.",
            "papa|Elle est où, maintenant ?",
        )
    return L(
        "narrateur|La ficelle de laine fait un nœud, tout doux.",
        "maman|Elle fait quoi, autour d'eux ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Deux têtes dépassent encore, l'une ronde, l'autre mince.",
            "enfant-f|Ils sont au chaud.",
            "papa|La marche du wagon est haute.",
            "maman|Tu tiens le paquet, tout contre toi ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le cacao sent encore, dans le thermos.",
        )
    if t1 == 2:
        return L(
            "narrateur|La boîte cliquette une fois, contre le genou.",
            "enfant-f|Ils sont dans leur cabine.",
            "maman|Le hérisson touche déjà le renard.",
            "papa|Tu montes avec les deux mains ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un peu de beurre reste au couvercle.",
        )
    return L(
        "narrateur|La ficelle tire un peu, puis se tait.",
        "enfant-f|Ils marchent ensemble, presque.",
        "papa|Le nœud tient, tout doux.",
        "maman|Tu gardes le sac à l'épaule ?",
        "enfant-f|Oui.",
        "narrateur|La laine frotte encore le poignet.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le wagon sent le cacao, déjà.",
        "narrateur|Le filet, la banquette, ou le passage.",
        "papa|On les pose où, pour attendre le tunnel ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le châle bleu accroche une maille, trop lâche.",
            2: "narrateur|La boîte à biscuits penche dans le filet.",
            3: "narrateur|La ficelle de laine passe déjà entre les mailles.",
        }[t1]
        return L(
            lead,
            "narrateur|Le filet sent le fer froid, tout haut.",
            "enfant-f|Vous voyez le plafond, tous les deux ?",
            "narrateur|Le hérisson rond roule vers un trou.",
            "narrateur|Le museau mince du renard glisse entre les fils.",
            f"narrateur|{o['cap']} n'attendait pas ça.",
            "enfant-f|Lui il roule, lui il glisse !",
            "papa|Alors on les garde ensemble.",
            "maman|Le tunnel n'est pas encore là.",
            "papa|Tu les gardes comment, dans le filet ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le châle bleu glisse sur le vinyle, trop chaud.",
            2: "narrateur|La boîte à biscuits part vers l'allée, toc.",
            3: "narrateur|La ficelle de laine fuit sous le dossier.",
        }[t1]
        return L(
            lead,
            "narrateur|La banquette sent le chauffage, tout près.",
            "enfant-f|C'est trop lisse, ici.",
            "narrateur|Le hérisson rond part vers le couloir.",
            "narrateur|Le renard mince se faufile sous le siège.",
            f"enfant-f|{o['cap']} ne les tient plus.",
            "maman|Ils ne jouent plus au même endroit.",
            "papa|On les reprend, tous les deux.",
            "enfant-f|Je ne veux pas choisir.",
            "papa|Tu les poses comment, sur le siège ?",
        )
    lead = {
        1: "narrateur|Le châle bleu tremble, entre les deux voitures.",
        2: "narrateur|La boîte à biscuits tape le plancher, toc.",
        3: "narrateur|La ficelle de laine saute à chaque joint.",
    }[t1]
    return L(
        lead,
        "narrateur|Le passage sent le vent froid, tout sec.",
        "enfant-f|Ça bouge trop, papa.",
        "narrateur|Le hérisson rond rebondit contre le genou.",
        "narrateur|Le renard mince glisse vers le soufflet noir.",
        f"narrateur|{o['cap']} n'arrête plus rien, tout seul.",
        "maman|On les tient, on ne les laisse pas.",
        "papa|Le tunnel va passer, déjà.",
        "enfant-f|Ils doivent le voir, tous les deux.",
        "maman|Tu les tiens comment, ici ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le filet attend encore, trop lâche.",
            "papa|Le nid, la boîte, ou contre toi ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La banquette chauffe encore, trop lisse.",
            "maman|La vallée, la maison, ou la ficelle ?",
        )
    return L(
        "narrateur|Le passage tremble encore, tout près.",
        "papa|La poitrine, la marche, ou le calme ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        nest = {
            1: "narrateur|Elle pousse le châle en nid, dans les mailles.",
            2: "narrateur|Elle pose un coin de châle sous la boîte.",
            3: "narrateur|Elle noue la ficelle autour du nid de laine.",
        }[t1]
        return L(
            "enfant-f|Un nid, pour vous deux.",
            nest,
            "narrateur|Le hérisson rond s'enfonce, tout calme.",
            "narrateur|Le renard mince se couche contre lui.",
            "enfant-f|Vous vous touchez, là.",
            "papa|Ils tiennent, l'un contre l'autre.",
            "maman|Le filet devient un hamac, un peu mou.",
            f"narrateur|{o['cap']} garde le bord.",
            "enfant-f|On verra le tunnel, d'en haut.",
        )
    if t2 == 1 and t3 == 2:
        box = {
            1: "narrateur|Elle glisse le châle dans la boîte, par-dessus.",
            2: "narrateur|Elle cale la boîte dans une maille plus serrée.",
            3: "narrateur|Elle attache la ficelle au bord de la boîte.",
        }[t1]
        return L(
            "enfant-f|Votre cabine, dans le filet.",
            box,
            "narrateur|Le hérisson rond prend le fond, tout chaud.",
            "narrateur|Le renard mince garde le rebord, tout droit.",
            "enfant-f|La fenêtre, c'est le couvercle.",
            "papa|Deux places, une seule boîte.",
            "maman|Ils voyagent encore ensemble.",
            f"narrateur|{o['cap']} cliquette une fois, puis se tait.",
            "enfant-f|On verra le tunnel, par le trou.",
        )
    if t2 == 1 and t3 == 3:
        hold = {
            1: "narrateur|Elle ramène le châle contre sa poitrine.",
            2: "narrateur|Elle reprend la boîte, tout contre elle.",
            3: "narrateur|Elle enroule la ficelle autour de son poignet.",
        }[t1]
        return L(
            "enfant-f|Le filet est trop grand.",
            hold,
            "narrateur|Le hérisson rond chauffe déjà sa manche.",
            "narrateur|Le renard mince frotte le bouton du manteau.",
            "enfant-f|Vous restez ici, tous les deux.",
            "papa|Plus bas, on les voit mieux.",
            "maman|Tes bras font le nid, maintenant.",
            f"narrateur|{o['cap']} pèse un peu, tout près.",
            "enfant-f|Le tunnel, on le verra d'ici.",
        )
    if t2 == 2 and t3 == 1:
        valley = {
            1: "narrateur|Elle plie le châle en vallée, entre deux coussins.",
            2: "narrateur|Elle glisse la boîte au fond de la vallée.",
            3: "narrateur|Elle tend la ficelle d'un coussin à l'autre.",
        }[t1]
        return L(
            "enfant-f|Une vallée, pour ne plus rouler.",
            valley,
            "narrateur|Le hérisson rond s'arrête au milieu, enfin.",
            "narrateur|Le renard mince reste sur le pli, tout droit.",
            "enfant-f|Plus de glissade.",
            "papa|Ils ont la même pente, maintenant.",
            "maman|Le vinyle ne les emporte plus.",
            f"narrateur|{o['cap']} tient le creux.",
            "enfant-f|La vitre est à vous, tous les deux.",
        )
    if t2 == 2 and t3 == 2:
        house = {
            1: "narrateur|Elle tapisse la boîte avec le châle, tout doux.",
            2: "narrateur|Elle ouvre la boîte, face à la vitre.",
            3: "narrateur|Elle noue la ficelle à l'anse de la boîte.",
        }[t1]
        return L(
            "enfant-f|Votre maison, sur la banquette.",
            house,
            "narrateur|Le hérisson rond garde le coin gauche.",
            "narrateur|Le renard mince garde le coin droit.",
            "enfant-f|Chacun sa fenêtre, dans la même maison.",
            "papa|Deux chambres, une seule porte.",
            "maman|Ils se parlent encore, tout près.",
            f"narrateur|{o['cap']} sent le beurre, un peu.",
            "enfant-f|Le tunnel va frapper le verre.",
        )
    if t2 == 2 and t3 == 3:
        belt = {
            1: "narrateur|Elle passe le châle derrière le dossier, en boucle.",
            2: "narrateur|Elle cale la boîte sous la boucle, tout bas.",
            3: "narrateur|Elle noue la ficelle autour du dossier, deux fois.",
        }[t1]
        return L(
            "enfant-f|Une ceinture, pour vous deux.",
            belt,
            "narrateur|Le hérisson rond reste collé au tissu.",
            "narrateur|Le renard mince reste collé à lui.",
            "enfant-f|Vous ne partez plus sous le siège.",
            "papa|Ils tiennent le dossier, ensemble.",
            "maman|Plus de chasse sous la banquette.",
            f"narrateur|{o['cap']} serre un peu, puis s'arrête.",
            "enfant-f|On attend le noir, tout calmes.",
        )
    if t2 == 3 and t3 == 1:
        chest = {
            1: "narrateur|Elle serre le châle contre sa poitrine, tout fort.",
            2: "narrateur|Elle plaque la boîte sous le menton, tout doux.",
            3: "narrateur|Elle enroule la ficelle autour de son pouce.",
        }[t1]
        return L(
            "enfant-f|Contre moi, tous les deux.",
            chest,
            "narrateur|Le hérisson rond entend son cœur, tout près.",
            "narrateur|Le renard mince sent le bouton, tout froid.",
            "enfant-f|Vous entendez le train, comme moi.",
            "papa|Tes bras font le wagon, maintenant.",
            "maman|Le soufflet peut gémir, ils restent.",
            f"narrateur|{o['cap']} chauffe déjà le manteau.",
            "enfant-f|Le tunnel, on le sentira ici.",
        )
    if t2 == 3 and t3 == 2:
        step = {
            1: "narrateur|Elle s'assoit sur la marche, le châle sur les genoux.",
            2: "narrateur|Elle pose la boîte sur ses genoux, couvercle ouvert.",
            3: "narrateur|Elle attache la ficelle à sa cheville, tout doux.",
        }[t1]
        return L(
            "enfant-f|Sur la marche, votre quai.",
            step,
            "narrateur|Le hérisson rond regarde le joint noir.",
            "narrateur|Le renard mince regarde le même joint.",
            "enfant-f|On est des voyageurs, là.",
            "papa|La marche est à toi, un moment.",
            "maman|Le plancher tremble moins, d'ici.",
            f"narrateur|{o['cap']} tient encore le poids.",
            "enfant-f|Le tunnel va passer sous nous.",
        )
    wait = {
        1: "narrateur|Elle attend, le châle serré, jusqu'au silence.",
        2: "narrateur|Elle attend, la boîte fermée, jusqu'au silence.",
        3: "narrateur|Elle attend, la ficelle au poignet, jusqu'au silence.",
    }[t1]
    return L(
        "enfant-f|On attend que ça se taise.",
        wait,
        "narrateur|Le hérisson rond ne rebondit plus.",
        "narrateur|Le renard mince ne glisse plus.",
        "enfant-f|Maintenant, contre la vitre du passage.",
        "papa|Le plancher a dit oui, enfin.",
        "maman|Ils peuvent voir, sans danser.",
        f"narrateur|{o['cap']} redevient calme, contre le verre.",
        "enfant-f|Le tunnel, on l'écoute d'ici.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le filet penche vers le noir, tout haut.",
            "enfant-f|Le tunnel, il arrive.",
            "papa|Ils l'ont vu, tous les deux.",
            "maman|Deux têtes dans le même nid.",
            coda,
            "narrateur|Les lampes du tunnel défilent, orange.",
            "enfant-f|Puis c'est blanc.",
            "narrateur|La neige colle au carreau, tout calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le couvercle tremble, puis s'ouvre un peu.",
            "enfant-f|Vous voyez le trou, tous les deux ?",
            "papa|Deux places, une seule cabine.",
            "maman|Le filet les a gardés.",
            coda,
            "narrateur|Le noir entre, puis s'en va.",
            "enfant-f|De la neige, déjà.",
            "narrateur|Un flocon reste au métal du filet.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Ses bras baissent un peu, vers la vitre.",
            "enfant-f|Vous êtes plus près, maintenant.",
            "papa|Tu les as repris tous les deux.",
            "maman|Le filet peut attendre, tout seul.",
            coda,
            "narrateur|Le noir frappe le verre, tout court.",
            "enfant-f|On l'a vu, ensemble.",
            "narrateur|La neige éclaire déjà le manteau.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|La vallée de laine s'arrête, face au verre.",
            "enfant-f|Plus personne ne roule.",
            "papa|Ils ont la même pente, jusqu'au bout.",
            "maman|Le chauffage ronronne encore, tout bas.",
            coda,
            "narrateur|Le souffle de Chouchou dessine le noir.",
            "enfant-f|Puis le blanc.",
            "narrateur|Deux silhouettes restent dans la buée.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La maison-boîte regarde la vitre, tout droit.",
            "enfant-f|Chacun sa fenêtre, même noir.",
            "papa|Deux chambres, un seul tunnel.",
            "maman|Ça sent encore le beurre, un peu.",
            coda,
            "narrateur|Le verre devient noir, puis blanc.",
            "enfant-f|On est arrivés, presque.",
            "narrateur|Un flocon se pose au couvercle.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|La ceinture de laine tient encore le dossier.",
            "enfant-f|Vous n'êtes plus sous le siège.",
            "papa|Ils ont voyagé à la même hauteur.",
            "maman|La banquette redevient un lit, tout calme.",
            coda,
            "narrateur|Le tunnel avale le wagon, une minute.",
            "enfant-f|Je vous ai gardés.",
            "narrateur|La neige frappe déjà le vinyle, tout doux.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Son cœur et le train parlent ensemble.",
            "enfant-f|Vous l'avez entendu, tous les deux.",
            "papa|Tes bras ont fait le wagon.",
            "maman|Le soufflet se tait, enfin.",
            coda,
            "narrateur|Le noir presse un peu les oreilles.",
            "enfant-f|Puis la lumière revient.",
            "narrateur|La neige entre par la fente, toute fine.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La marche vibre encore, puis s'endort.",
            "enfant-f|Votre quai a vu le noir.",
            "papa|La marche était à toi, un moment.",
            "maman|Le joint ne les a pas pris.",
            coda,
            "narrateur|Le tunnel passe sous leurs pattes.",
            "enfant-f|On est des voyageurs, vraiment.",
            "narrateur|Un peu de neige reste sur le fer.",
        )
    return L(
        "narrateur|Le plancher s'est tu, juste à temps.",
        "enfant-f|On a attendu, puis on a vu.",
        "papa|Le calme t'a laissé la place.",
        "maman|La vitre du passage tient encore.",
        coda,
        "narrateur|Le noir arrive sans danser, cette fois.",
        "enfant-f|Vous l'avez, tous les deux.",
        "narrateur|La neige allume déjà le couloir.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Sous le pont, la rivière parle encore.",
        "narrateur|La petite gare sent le fer et les feuilles.",
        "narrateur|Une lampe jaune tremble déjà, sur le quai.",
        "narrateur|La colline a mangé le dernier soleil.",
        "maman|Le cacao du thermos est encore chaud.",
        "papa|Le train de montagne arrive, tout lent.",
        "enfant-f|Ils viennent, mes deux voyageurs.",
        "narrateur|En ce moment, Chouchou ouvre le sac de laine.",
        "narrateur|Le hérisson est tout rond, tout doux.",
        "narrateur|Le renard de bois est tout mince, tout lisse.",
        "enfant-f|Ils doivent voir le tunnel ensemble.",
        "papa|Merci, tu les sors sans les bousculer.",
        "maman|On prend les affaires, avant la marche.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du sac.",
        "narrateur|Le châle, la boîte, et la ficelle.",
        "maman|Tu prends quoi d'abord, Chouchou ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le châle bleu", "la boîte à biscuits", "la ficelle de laine")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le filet", "la banquette", "le passage")
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
        "Le soir, gare de colline, train de montagne. Chouchou veut que "
        "le hérisson tout rond et le renard de bois tout mince voient le "
        "tunnel ensemble. "
        "T1 = châle bleu / boîte à biscuits / ficelle de laine (les trois partent). "
        "T2 = filet (mailles trop lâches) / banquette chaude (vinyle trop lisse) / "
        "passage entre les voitures (plancher qui tremble). "
        "T3 = neuf résolutions (nid de laine, boîte dans le filet, contre soi ; "
        "vallée du châle, maison-boîte, ficelle au dossier ; poitrine, marche, "
        "attendre le calme). "
        "La leçon se vit : on les garde tous les deux, sans blague sur le corps. "
        "Fin : le noir du tunnel, puis la neige.",
        "N3 ≤ 16. Lina hors troupe → Chouchou, papa/maman. Slogan "
        "« Plus rond ou plus mince » jeté. Autre récit que DIF-041 "
        "(pas mer, pas pain, pas Nina), DIF-043 (pas canards, pas parc) "
        "et DIF-035 (pas poupées, pas bain). Un merci de papa lié au geste "
        "(sortir les deux sans les bousculer). Pas de « bon travail ». "
        "Audio non cuit.",
    )


if __name__ == "__main__":
    main()
