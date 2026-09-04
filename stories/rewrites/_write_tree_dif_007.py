#!/usr/bin/env python3
"""TREE-DIF-007 — Le rayon sur le casier. Désir: retrouver le dessin. Besoin implicite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N2 = LIMITS["N2"]
SID = "TREE-DIF-007"


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
    return list(rows)


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind == "passage_question" else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = (
        "Un rayon touche le casier de Nino. Il veut retrouver son dessin "
        "pour le coller où le soleil arrive. Les feuilles glissent. "
        "Nino cherche trop vite. Un camarade reste au calme sur le banc. "
        "Tout doux, Nino retrouve le papier."
    )
    out["title"] = "Le rayon sur le casier"
    out["characters"] = "Nino, papa, maman"
    out["setting"] = "couloir de l'école, casiers"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


T1 = {
    1: dict(
        nom="le manteau",
        rest="Le manteau pend au crochet, une manche un peu froide.",
        trace="Une goutte sèche encore au col.",
        lift="le pan du manteau",
        q_ans="crayon",
        q_acc="crayon | un crayon | le crayon | poche | de la poche",
        q_retry="Un crayon tombe de la poche. Que tombe ?",
    ),
    2: dict(
        nom="le cartable",
        rest="Le cartable reste ouvert, la fermeture un peu tordue.",
        trace="Une feuille d'exercice dépasse encore.",
        lift="le rabat du cartable",
        q_ans="cartable",
        q_acc="cartable | le cartable | sac | le sac | fermeture",
        q_retry="Nino a ouvert le cartable. Qu'a-t-il ouvert ?",
    ),
    3: dict(
        nom="la boîte",
        rest="La boîte reste ouverte, ça sent encore la banane.",
        trace="La serviette a une tache ronde.",
        lift="le couvercle de la boîte",
        q_ans="boîte",
        q_acc="boîte | boite | la boîte | la boite | serviette",
        q_retry="Nino a ouvert la boîte. Qu'a-t-il ouvert ?",
    ),
}

T2 = {
    1: dict(
        nom="le banc",
        hide="sous le banc",
        sol="Le bois du banc est lisse, un peu froid.",
        bruit="Un pied du banc fait un tout petit toc.",
        reste="Le banc garde une ombre étroite.",
    ),
    2: dict(
        nom="la vitre",
        hide="contre la vitre",
        sol="Le rayon chauffe la vitre, tout doux.",
        bruit="La vitre fait un fil de lumière, tout mince.",
        reste="La vitre garde un carré de soleil.",
    ),
    3: dict(
        nom="les chaussures",
        hide="près des chaussures",
        sol="Une lacette traîne, encore un peu humide.",
        bruit="Une semelle sent le caoutchouc, tout bas.",
        reste="Les chaussures restent paires, tout sages.",
    ),
}


def t1_body(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Nino prend le manteau d'abord.",
            "narrateur|Le tissu est un peu froid, encore mouillé au col.",
            "enfant-m|Il sent le dehors.",
            "maman|Accroche-le, on verra mieux.",
            "narrateur|Le crochet fait clic, tout net.",
            "narrateur|Une manche reste retournée.",
            "enfant-m|Je la sors.",
            "narrateur|Un crayon tombe de la poche, tic.",
            "papa|Le crayon, d'accord.",
            "papa|Et le dessin ?",
            "enfant-m|Pas dans la poche.",
            "narrateur|Le camarade tourne à peine la tête.",
            "narrateur|Nino souffle, puis il regarde le sol.",
        )
    if i == 2:
        return L(
            "narrateur|Nino pose le cartable d'abord.",
            "narrateur|La fermeture résiste, un peu de travers.",
            "enfant-m|Elle est coincée.",
            "papa|Tire tout doux, pas trop fort.",
            "narrateur|La fermeture cède, zzzit, tout long.",
            "narrateur|Des feuilles s'éventent, une, puis une autre.",
            "enfant-m|Mon dessin ?",
            "maman|Regarde le dessus, sans tout vider.",
            "narrateur|Un livre pèse encore au fond.",
            "narrateur|Le dessin n'est pas sur le dessus.",
            "enfant-m|Il a glissé.",
            "narrateur|Le camarade serre un peu les genoux.",
            "narrateur|Nino referme à moitié, tout calme.",
        )
    return L(
        "narrateur|Nino ouvre la boîte d'abord.",
        "narrateur|Le couvercle claque, puis reste en l'air.",
        "enfant-m|Ça sent la banane.",
        "maman|La serviette est collée, tout au fond.",
        "narrateur|Nino soulève la serviette, tout lentement.",
        "narrateur|Une tache ronde brille, un peu collante.",
        "enfant-m|Pas le dessin.",
        "papa|Il n'est pas dans la boîte, alors.",
        "narrateur|Le couvercle attend, tout ouvert.",
        "narrateur|Le camarade ne bouge toujours pas.",
        "enfant-m|Il est parti où ?",
        "maman|On suit le papier, sans se presser.",
        "narrateur|Nino repose la serviette, tout plat.",
    )


def t1_q(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Le dessin n'est pas dans la poche.",
            "maman|Que tombe de la poche ?",
        )
    if i == 2:
        return L(
            "narrateur|Le dessin n'est pas sur le dessus.",
            "papa|Qu'est-ce que Nino a ouvert ?",
        )
    return L(
        "narrateur|Le dessin n'est pas sous la serviette.",
        "maman|Qu'est-ce que Nino a ouvert ?",
    )


def t1_c(i: int) -> list[str]:
    v = T1[i]
    return L(
        f"narrateur|{v['rest']}",
        "narrateur|Un coin jaune a disparu, trop vite.",
        "enfant-m|Je le veux encore.",
        "papa|On cherche, sans tout mélanger.",
        "narrateur|Nino pose les mains à plat, un moment.",
        "maman|Le papier a pu glisser, tout près.",
    )


def t2_body(t1: int, t2: int) -> list[str]:
    a, b = T1[t1], T2[t2]
    head = {
        (1, 1): L(
            "narrateur|Le manteau pend, et un coin jaune file.",
            "narrateur|Il glisse vers le banc, tout bas.",
            "narrateur|Le camarade garde les mains sur les genoux.",
            "enfant-m|Il est sous le banc, je crois.",
            "maman|On s'approche, sans faire de bruit.",
            "narrateur|Le bois du banc est lisse, un peu froid.",
            "narrateur|Un pied du banc fait un tout petit toc.",
            "papa|Tu le vois, Nino ?",
            "enfant-m|Un bout, tout jaune.",
            "narrateur|Le camarade respire, tout calme.",
        ),
        (1, 2): L(
            "narrateur|La porte laisse un peu d'air.",
            "narrateur|Le coin jaune vole vers la vitre.",
            "narrateur|Le rayon le rattrape, tout chaud.",
            "enfant-m|Il est contre la vitre !",
            "papa|Regarde, sans courir.",
            "narrateur|La vitre fait un fil de lumière, tout mince.",
            "narrateur|Le manteau bouge encore un peu au crochet.",
            "maman|Le papier colle, à cause du soleil.",
            "enfant-m|Je le vois, il brille.",
            "narrateur|Le camarade lève à peine les yeux.",
        ),
        (1, 3): L(
            "narrateur|Une goutte tombe du col du manteau.",
            "narrateur|Le papier suit, vers les chaussures.",
            "narrateur|Une lacette traîne, encore un peu humide.",
            "enfant-m|Il est près des chaussures.",
            "maman|Baisse-toi, tout doux.",
            "narrateur|Une semelle sent le caoutchouc, tout bas.",
            "narrateur|L'ombre est un peu sombre, sous le bord.",
            "papa|Tu cherches avec les yeux d'abord.",
            "enfant-m|Un coin, près du lacet.",
            "narrateur|Le camarade n'a pas bougé.",
        ),
        (2, 1): L(
            "narrateur|Une feuille quitte le cartable, tout plat.",
            "narrateur|Elle glisse jusqu'au banc.",
            "narrateur|Le camarade serre un peu les genoux.",
            "enfant-m|Mon dessin va sous le banc.",
            "papa|On marche lentement, d'accord ?",
            "enfant-m|D'accord.",
            "narrateur|Le bois du banc est lisse, un peu froid.",
            "narrateur|Un pied du banc fait un tout petit toc.",
            "maman|Le rabat du cartable reste ouvert, derrière.",
            "enfant-m|Je vois un bout jaune.",
        ),
        (2, 2): L(
            "narrateur|Le courant prend une feuille du cartable.",
            "narrateur|Elle va se coller contre la vitre.",
            "narrateur|Le rayon la tient, tout chaud.",
            "enfant-m|C'est lui, sur la vitre !",
            "maman|On y va, sans se bousculer.",
            "narrateur|La vitre fait un fil de lumière, tout mince.",
            "narrateur|Le cartable reste au milieu du couloir.",
            "papa|Tu le reconnais ?",
            "enfant-m|Le soleil que j'ai dessiné.",
            "narrateur|Le camarade écoute, sans se lever.",
        ),
        (2, 3): L(
            "narrateur|Une feuille échappe au cartable, tout bas.",
            "narrateur|Elle file vers les chaussures.",
            "narrateur|Une lacette traîne, encore un peu humide.",
            "enfant-m|Il se cache près des chaussures.",
            "papa|On se baisse, chacun son temps.",
            "narrateur|Une semelle sent le caoutchouc, tout bas.",
            "narrateur|L'ombre est un peu sombre, sous le bord.",
            "maman|Le cartable attend derrière, encore ouvert.",
            "enfant-m|Un coin, près du lacet.",
            "narrateur|Le camarade reste assis, tout sage.",
        ),
        (3, 1): L(
            "narrateur|Un coin de papier quitte la boîte.",
            "narrateur|Il glisse sous le banc, collé un peu.",
            "narrateur|Ça sent encore la banane, tout près.",
            "enfant-m|Il est sous le banc.",
            "maman|On s'approche, tout calme.",
            "narrateur|Le bois du banc est lisse, un peu froid.",
            "narrateur|Un pied du banc fait un tout petit toc.",
            "papa|La serviette a laissé une tache ronde.",
            "enfant-m|Je vois le jaune.",
            "narrateur|Le camarade garde les mains sur les genoux.",
        ),
        (3, 2): L(
            "narrateur|Le papier s'échappe de la boîte, tout léger.",
            "narrateur|Il va se poser contre la vitre.",
            "narrateur|Le rayon le réchauffe, et la tache brille.",
            "enfant-m|Il est à la vitre !",
            "papa|On marche, sans courir.",
            "narrateur|La vitre fait un fil de lumière, tout mince.",
            "narrateur|La boîte reste ouverte, au casier.",
            "maman|Tu le vois, malgré la tache ?",
            "enfant-m|Oui, le soleil est là.",
            "narrateur|Le camarade regarde la lumière, tout doux.",
        ),
        (3, 3): L(
            "narrateur|Le papier quitte la boîte, tout bas.",
            "narrateur|Il s'arrête près des chaussures.",
            "narrateur|Une lacette traîne, encore un peu humide.",
            "enfant-m|Il est près des chaussures.",
            "maman|On se baisse, sans se presser.",
            "narrateur|Une semelle sent le caoutchouc, tout bas.",
            "narrateur|L'ombre est un peu sombre, sous le bord.",
            "papa|La boîte reste ouverte, derrière nous.",
            "enfant-m|Un coin, près du lacet.",
            "narrateur|Le camarade n'a pas bougé d'un pied.",
        ),
    }
    return head[(t1, t2)]


def t3_body(t1: int, t2: int, t3: int) -> list[str]:
    a, b = T1[t1], T2[t2]
    if t3 == 1:
        return L(
            "enfant-m|On attend.",
            f"narrateur|Le papier reste {b['hide']}, sans bouger.",
            "narrateur|Nino pose les mains sur ses genoux, lui aussi.",
            "papa|On laisse le temps, juste un peu.",
            "narrateur|Le camarade relâche les épaules, tout doux.",
            f"narrateur|{b['sol']}",
            "enfant-m|Maintenant, je le vois.",
            "maman|Merci d'avoir attendu.",
            "narrateur|Nino avance deux doigts, tout lentement.",
            "narrateur|Le papier est un peu froid, un peu plié.",
        )
    if t3 == 2:
        return L(
            "enfant-m|Je souffle.",
            "narrateur|Nino souffle une fois, tout long.",
            f"narrateur|Le papier tremble {b['hide']}.",
            "papa|Encore une fois, tout calme.",
            "narrateur|La poussière danse, puis s'en va.",
            f"narrateur|{b['bruit']}",
            "enfant-m|Il avance vers moi.",
            "maman|Bravo, Nino.",
            "narrateur|Le camarade sourit à peine, sans parler.",
            "narrateur|Nino prend le dessin, tout plat.",
        )
    return L(
        "enfant-m|Tu lèves, papa ?",
        f"papa|{a['lift'].capitalize()}, c'est ça ?",
        "enfant-m|Oui, s'il te plaît.",
        f"narrateur|Papa lève {a['lift']}, tout doux.",
        f"narrateur|Le dessin apparaît {b['hide']}.",
        "maman|Tu le prends, Nino.",
        "enfant-m|Merci, papa.",
        "papa|Merci d'avoir demandé tout doux.",
        "narrateur|Le camarade n'a pas sursauté.",
        "narrateur|Le papier sent encore un peu le savon.",
    )


def fin(t1: int, t2: int, t3: int) -> list[str]:
    a, b = T1[t1], T2[t2]
    geste = {
        1: "Nino a attendu, et le papier est venu.",
        2: "Nino a soufflé, et le papier a bougé.",
        3: "Papa a levé, et le papier était là.",
    }[t3]
    return L(
        "narrateur|Nino tient son dessin des deux mains.",
        "enfant-m|C'est mon soleil.",
        "maman|On le met où le rayon arrive ?",
        "enfant-m|Oui, sur le casier.",
        "narrateur|Le papier se colle, tout chaud, sous le bouton.",
        f"narrateur|{a['rest']}",
        f"narrateur|{b['reste']}",
        f"narrateur|{geste}",
        "papa|Le camarade peut rester encore un peu.",
        "enfant-m|Mon soleil a retrouvé le rayon.",
        f"narrateur|{a['trace']}",
        "narrateur|Le bouton du casier brille, tout petit.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {
        "CHK_T0000_P0000": "porte_classe",
        "CHK_T0001_P0000": "",
    }

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une poussière danse dans le soleil.",
        "narrateur|Le rayon tombe sur le casier de Nino.",
        "narrateur|Un coin de papier jaunit, tout chaud.",
        "narrateur|Le couloir sent le savon, et la banane.",
        "narrateur|Les crochets font un petit clic.",
        "papa|Tu as vu ce papier, Nino ?",
        "enfant-m|C'est mon dessin.",
        "enfant-m|Je le veux pour la vitre.",
        "maman|Il est dans le casier, quelque part.",
        "narrateur|En ce moment, Nino ouvre trop vite.",
        "narrateur|Les feuilles glissent, une par une.",
        "narrateur|Un camarade s'assoit sur le banc.",
        "narrateur|Ses mains restent sur ses genoux.",
        "narrateur|Il ne bouge pas.",
        "enfant-m|Où es-tu, dessin ?",
        "papa|On cherche tout doux, d'accord ?",
        "enfant-m|D'accord, papa.",
        "maman|Tu commences par quoi ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le casier est encore un peu sombre.",
        "maman|Le manteau, le cartable, ou la boîte ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le manteau", "le cartable", "la boîte")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        s[p] = t1_body(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = qf(T1[t1]["q_ans"], T1[t1]["q_acc"], T1[t1]["q_retry"])
        s[f"{p}_C0001"] = t1_c(t1)
        s[f"{p}_T0002_P0000"] = L(
            "narrateur|Le coin jaune a glissé, tout près.",
            "papa|Le banc, la vitre, ou les chaussures ?",
        )
        extras[f"{p}_T0002_P0000"] = t3lab("le banc", "la vitre", "les chaussures")

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_body(t1, t2)
            s[f"{sp}_T0003_P0000"] = L(
                f"narrateur|Le dessin attend {T2[t2]['hide']}.",
                "maman|On attend, on souffle, ou on lève ?",
            )
            extras[f"{sp}_T0003_P0000"] = t3lab("on attend", "on souffle", "on lève")

            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_body(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        "Le rayon sur le casier",
        "Nino veut son dessin dans le casier. T1 manteau/cartable/boîte colore "
        "la recherche. T2 banc/vitre/chaussures. T3 attendre/souffler/lever. "
        "Le camarade reste au calme. Fin: le soleil collé sous le rayon.",
        "Gabarit chat/chien/poule et slogans « répéter la règle » jetés. "
        "Leçon besoin vécue, non dite. Audio non cuit. 27 chemins non écoutés.",
    )


if __name__ == "__main__":
    main()
