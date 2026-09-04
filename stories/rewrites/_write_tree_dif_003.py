#!/usr/bin/env python3
"""TREE-DIF-003 — Mila retrouve l'escargot rayé. Manteau et lunettes = outils."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N2 = LIMITS["N2"]
SID = "TREE-DIF-003"


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if role not in {
            "narrateur",
            "papa",
            "maman",
            "enfant-m",
            "enfant-f",
            "copain",
            "copine",
        }:
            raise SystemExit(f"rôle {role}")
    return list(rows)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:12]} extra={sorted(extra_ids)[:12]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind in ("passage_question", "transition_question") else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = (
        "Mila a vu un escargot rayé sur la vitre. Elle veut le retrouver "
        "et lui faire une maison de feuille. Aniss l'aide. Le manteau à pois, "
        "les lunettes et le seau portent le voyage."
    )
    out["title"] = "Le manteau à pois et les lunettes de Mila"
    out["characters"] = "Mila, Aniss, papa, maman"
    out["setting"] = "cuisine puis seuil, après la pluie"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# T1 colore : manteau (poche-maison) / lunettes (voir la trace) / seau (hôtel).
TOOL = {
    1: dict(
        nom="le manteau à pois",
        q_ans="poche",
        q_acc="poche | la poche | dans la poche | manteau | le manteau | feuille",
        q_retry="Mila glisse la feuille où ?",
        q_ask="Où Mila met-elle la feuille ?",
    ),
    2: dict(
        nom="les lunettes",
        q_ans="trace",
        q_acc="trace | la trace | Mila | Aniss | lunettes | les lunettes | vitre",
        q_retry="Avec les lunettes, on voit quoi ?",
        q_ask="Mila voit quoi, avec les lunettes ?",
    ),
    3: dict(
        nom="le seau",
        q_ans="feuille",
        q_acc="feuille | une feuille | la feuille | eau | une goutte | seau",
        q_retry="Qu'est-ce qu'il y a dans le seau ?",
        q_ask="Qu'est-ce qu'il y a dans le seau ?",
    ),
}

# T2 = trois lieux d'aventure.
PLACE = {
    1: dict(nom="le paillasson", secret="Le paillasson garde encore un secret."),
    2: dict(nom="les pots", secret="Les pots gardent encore un secret."),
    3: dict(nom="la gouttière", secret="La gouttière garde encore un secret."),
}


def pre(t1: int) -> str:
    return f"CHK_T0001_P000{t1}"


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila tire le manteau à pois du crochet.",
            "narrateur|Une manche est encore retournée, toute molle.",
            "enfant-f|J'ai la manche !",
            "enfant-m|Je la tiens.",
            "narrateur|Aniss tend le tissu, tout doux.",
            "maman|Glisse un bras, puis l'autre.",
            "narrateur|Les pois brillent, encore un peu mouillés.",
            "enfant-m|On dirait des coquilles.",
            "enfant-f|C'est pour l'escargot.",
            "papa|La poche est assez grande ?",
            "enfant-f|Oui.",
            "enfant-f|J'y mets une feuille.",
            "narrateur|La feuille sent l'herbe, encore froide.",
            "narrateur|Mila la glisse au fond de la poche.",
            "enfant-f|C'est sa maison.",
            "papa|Vous sortez ensemble ?",
            "enfant-m|Oui.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila prend les lunettes près du bol.",
            "narrateur|Un peu de buée les rend encore floues.",
            "papa|Souffle, puis j'essuie.",
            "enfant-f|Je souffle.",
            "narrateur|Papa passe le torchon, tout lent.",
            "narrateur|Les verres redeviennent clairs.",
            "enfant-f|Je vois la trace d'argent !",
            "enfant-m|Moi aussi, si je me penche.",
            "narrateur|Aniss colle sa joue près de la sienne.",
            "maman|Elle part vers la porte ?",
            "enfant-f|Oui, toute fine.",
            "papa|Les lunettes tiennent bien ?",
            "enfant-f|Oui, sur mon nez.",
            "narrateur|Un fil brillant descend vers le seuil.",
            "enfant-m|On le suit.",
            "enfant-f|Avant qu'il sèche.",
        )
    return L(
        "narrateur|Mila attrape le seau bleu sous l'évier.",
        "narrateur|Il sonne creux, comme un petit tambour.",
        "enfant-f|C'est l'hôtel.",
        "enfant-m|Il est vide.",
        "maman|Une feuille, et une goutte ?",
        "narrateur|Mila pose une feuille au fond.",
        "narrateur|Papa incline le robinet, tout petit.",
        "enfant-f|Une goutte, pas un bain.",
        "papa|Voilà.",
        "narrateur|L'eau fait un rond sur la feuille.",
        "enfant-m|Je porte l'anse.",
        "enfant-f|Doucement, Aniss.",
        "narrateur|Le seau se balance, puis se calme.",
        "maman|L'hôtel est prêt ?",
        "enfant-f|Oui.",
        "enfant-m|On cherche.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La feuille reste au fond de la poche.",
            "narrateur|Le bas du manteau touche encore le paillasson.",
            "maman|Le paillasson est mouillé.",
            "enfant-f|On suit la trace.",
            "papa|Doucement, le carrelage est froid.",
            "enfant-m|J'ouvre un peu.",
            "narrateur|L'air entre, frais comme de l'eau.",
        )
    if t1 == 2:
        return L(
            "narrateur|La trace d'argent reste nette, tout près.",
            "narrateur|Les lunettes ne bougent plus sur le nez.",
            "papa|Vous voyez le fil jusqu'au seuil ?",
            "enfant-f|Oui.",
            "enfant-m|Il brille encore.",
            "maman|L'air va embuer, un peu.",
            "narrateur|Aniss pousse la porte, tout doux.",
        )
    return L(
        "narrateur|La feuille nage dans sa goutte, au fond.",
        "narrateur|Le seau penche, puis se tient droit.",
        "papa|Deux mains sur l'anse, Aniss.",
        "enfant-m|J'ai.",
        "enfant-f|On suit la trace.",
        "maman|Le seuil est encore mouillé.",
        "narrateur|Ils passent, sans faire sonner le seau.",
    )


def color_t2(t1: int, t2: int) -> list[str]:
    """Deux ou trois phrases qui font voyager l'outil T1 dans le lieu T2."""
    if t1 == 1 and t2 == 1:
        return L(
            "narrateur|Le manteau à pois frotte le paillasson.",
            "narrateur|Un pois laisse une goutte ronde.",
            "enfant-f|La poche est prête.",
        )
    if t1 == 1 and t2 == 2:
        return L(
            "narrateur|Un pois du manteau accroche une feuille de géranium.",
            "enfant-f|Je la mets avec l'autre, dans la poche.",
            "enfant-m|Deux toits, alors.",
        )
    if t1 == 1 and t2 == 3:
        return L(
            "narrateur|Une goutte tombe du tuyau, sur un pois.",
            "enfant-f|Il brille, celui-là.",
            "enfant-m|Comme une coquille.",
        )
    if t1 == 2 and t2 == 1:
        return L(
            "enfant-f|Je mets les lunettes.",
            "narrateur|Les fibres deviennent nettes, une par une.",
            "enfant-m|Là, une petite bosse.",
        )
    if t1 == 2 and t2 == 2:
        return L(
            "narrateur|Mila penche les lunettes entre les pots.",
            "enfant-f|Je vois un fil, sur la terre.",
            "enfant-m|Il va sous la feuille.",
        )
    if t1 == 2 and t2 == 3:
        return L(
            "narrateur|Les lunettes attrapent un éclat, tout haut.",
            "enfant-f|Une coquille, sur le tuyau !",
            "enfant-m|Elle brille, puis non.",
        )
    if t1 == 3 and t2 == 1:
        return L(
            "narrateur|Le seau pose un rond d'eau sur le paillasson.",
            "enfant-m|Je tiens l'anse.",
            "enfant-f|La feuille est encore dedans.",
        )
    if t1 == 3 and t2 == 2:
        return L(
            "narrateur|Le seau se cale entre deux pots, sans tomber.",
            "enfant-f|L'hôtel attend ici.",
            "enfant-m|La terre sent le mouillé.",
        )
    return L(
        "narrateur|Le seau s'arrête sous la gouttière, tout droit.",
        "enfant-m|Encore une goutte, dedans ?",
        "enfant-f|Non.",
        "enfant-f|Juste la feuille.",
    )


def t2_core(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Ils s'arrêtent sur le paillasson mouillé.",
            "narrateur|La trace d'argent s'y perd dans les fibres.",
            "enfant-f|Il est dessous ?",
            "papa|Le paillasson est lourd.",
            "maman|Tout doux, d'accord ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les pots de géranium luisent, encore mouillés.",
            "narrateur|Une feuille large fait un toit, tout bas.",
            "enfant-m|Ça gratte, en dessous.",
            "papa|La terre colle aux bords.",
            "maman|Vous regardez la tige, tout doux ?",
        )
    return L(
        "narrateur|La gouttière laisse encore une goutte, puis une autre.",
        "narrateur|Le tuyau est froid, un peu vert.",
        "enfant-f|C'est trop haut, Aniss.",
        "papa|Les pieds restent au sol.",
        "maman|Une feuille peut aider, plus bas.",
    )


def color_t3(t1: int, t3: int) -> list[str]:
    if t3 == 1:  # pose
        if t1 == 1:
            return L(
                "narrateur|Mila ouvre la poche à pois, tout large.",
                "narrateur|L'escargot glisse sur la feuille, dans le tissu.",
                "enfant-f|Sa maison est tiède.",
            )
        if t1 == 2:
            return L(
                "narrateur|Avec les lunettes, les rayures sont nettes.",
                "enfant-f|Cinq, six, sept.",
                "enfant-m|Je les vois aussi.",
            )
        return L(
            "narrateur|Ils posent la feuille du seau tout contre.",
            "narrateur|L'escargot passe, sans se presser.",
            "enfant-m|L'hôtel a un voyageur.",
        )
    if t3 == 2:  # attend
        if t1 == 1:
            return L(
                "narrateur|Mila ouvre un peu la poche, sans bouger.",
                "enfant-f|S'il veut, il entre.",
                "enfant-m|Les pois restent sages.",
            )
        if t1 == 2:
            return L(
                "narrateur|Les lunettes restent sur le nez, immobiles.",
                "enfant-f|Je le vois avancer, tout lent.",
                "enfant-m|Une corne, puis l'autre.",
            )
        return L(
            "narrateur|Aniss tient le seau, sans le pencher.",
            "enfant-m|L'eau ne bouge plus.",
            "enfant-f|Il peut venir.",
        )
    # dessine
    if t1 == 1:
        return L(
            "narrateur|Mila pose un pois contre le papier, comme un modèle.",
            "enfant-f|La coquille, c'est ça.",
            "enfant-m|Je fais les cornes.",
        )
    if t1 == 2:
        return L(
            "narrateur|Les lunettes gardent le fil d'argent, tout net.",
            "enfant-f|Je le recopie, tout doux.",
            "enfant-m|Il part vers la porte, sur le papier.",
        )
    return L(
        "narrateur|Une goutte du seau mouille le doigt d'Aniss.",
        "enfant-m|Ça fait le brillant.",
        "enfant-f|Et moi, la spirale.",
    )


def t3_body(t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-f|On soulève le coin.",
            "narrateur|Aniss tient le paillasson, tout fort.",
            "narrateur|Une coquille rayée brille entre les fibres.",
            "enfant-m|Il est là !",
            "narrateur|Mila approche la feuille, tout contre.",
            "narrateur|L'escargot avance, tout lent.",
            "papa|Merci d'avoir été doux.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-f|On reste là.",
            "narrateur|Ils s'accroupissent, genoux mouillés.",
            "narrateur|Une corne sort des fibres, puis l'autre.",
            "enfant-m|Il nous a vus.",
            "maman|Vous avez laissé le temps.",
            "narrateur|L'escargot mange un brin, tout petit.",
            "papa|Il est calme, maintenant.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-f|Il a filé.",
            "enfant-m|La trace est encore brillante.",
            "narrateur|Mila suit le fil d'argent du doigt.",
            "narrateur|Le carrelage garde un dessin mouillé.",
            "maman|On peut le garder sur le papier.",
            "papa|Le torchon est dans la cuisine.",
            "enfant-f|J'apporte le papier.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-f|Je soulève le toit de feuille.",
            "narrateur|Sous le géranium, la terre est noire et douce.",
            "narrateur|L'escargot est là, collé à un tesson.",
            "enfant-m|Il a un chapeau de terre.",
            "narrateur|Mila glisse la feuille sous lui, tout lent.",
            "papa|La tige reste entière.",
            "papa|Merci.",
            "maman|Vos doigts sont un peu noirs.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-m|Il grimpe tout seul.",
            "narrateur|La coquille monte sur la terre cuite, anneau après anneau.",
            "enfant-f|On compte.",
            "enfant-m|Un, deux, trois.",
            "maman|Vous restez en bas, les deux.",
            "narrateur|Une goutte tombe du pot, puis plus rien.",
            "papa|Il a choisi son mur.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-f|Les pots sont vides.",
            "narrateur|Il reste un fil sur la terre, déjà pâle.",
            "enfant-m|Je fais la spirale, avec la boue.",
            "narrateur|Aniss dessine sur le bord du pot, un tour.",
            "maman|Et ensuite, sur le papier ?",
            "enfant-f|Oui.",
            "enfant-f|Deux pots, et le fil.",
            "papa|On rince les doigts, après.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-f|Une rampe, avec la feuille.",
            "narrateur|Aniss tient la feuille contre le tuyau froid.",
            "narrateur|L'escargot quitte le métal, pas après pas.",
            "enfant-m|Il descend !",
            "papa|Vous l'avez aidé, sans le tirer.",
            "maman|Une goutte encore, sur le nez de Mila.",
            "enfant-f|Elle est froide !",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-f|On compte les gouttes.",
            "enfant-m|Plic, plic.",
            "narrateur|Ils attendent sous la gouttière, sans bouger.",
            "narrateur|À la quatrième, une coquille apparaît.",
            "maman|Il vient tout seul.",
            "papa|Vous avez écouté l'eau.",
            "enfant-f|Encore une, et il est là.",
        )
    return L(
        "enfant-f|Il a suivi l'eau.",
        "narrateur|Le tuyau est vide, juste mouillé.",
        "enfant-m|On dessine la gouttière, sur la vitre.",
        "narrateur|Mila trace le tuyau dans la buée.",
        "maman|Et les gouttes, Aniss ?",
        "enfant-m|Des ronds, tout le long.",
        "papa|On recopie au chaud, sur le papier.",
    )


def fin_body(t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils rentrent.",
            "narrateur|Le paillasson garde un creux mouillé.",
            "enfant-f|Il a sa maison, dehors.",
            "enfant-m|Près des fibres, tout doux.",
            "maman|La soupe est encore chaude.",
            "papa|Vos chaussettes sont un peu froides.",
            "narrateur|Un fil d'argent sèche déjà, sur le seuil.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Ils se relèvent.",
            "narrateur|Les genoux ont deux ronds mouillés.",
            "enfant-m|Il mange encore, je crois.",
            "enfant-f|On l'a regardé longtemps.",
            "papa|Le bol est encore tiède.",
            "maman|Une serviette pour les mains.",
            "narrateur|Le paillasson redevient plat, tout seul.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le papier rejoint la table, près du bol.",
            "enfant-f|Le fil, et deux cornes.",
            "enfant-m|C'est notre carte.",
            "maman|Elle sèche, à côté de la soupe.",
            "papa|Demain, on regardera le paillasson.",
            "narrateur|Le carrelage a perdu son dessin mouillé.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Ils laissent l'escargot sous le géranium, à l'abri.",
            "enfant-f|Sa feuille est là, comme un lit.",
            "enfant-m|La terre sent encore nos mains.",
            "maman|L'eau du robinet, tout doux.",
            "papa|Les ongles redeviennent propres.",
            "narrateur|Un pétale rouge tremble, puis s'arrête.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le pot garde un voyageur, collé tout haut.",
            "enfant-m|On a seulement regardé.",
            "enfant-f|Il a choisi.",
            "papa|Vous avez compté, et attendu.",
            "maman|La soupe vous attend, les deux.",
            "narrateur|La terre cuite sèche, un anneau après l'autre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Deux pots et une spirale tiennent sur le papier.",
            "enfant-f|Un peu de boue, un peu de crayon.",
            "enfant-m|C'est presque pareil.",
            "maman|Les mains, sous l'eau tiède.",
            "papa|Le papier sèche près du bol.",
            "narrateur|Le géranium penche, comme s'il regardait.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|La rampe de feuille reste au pied du tuyau.",
            "enfant-f|Il est redescendu tout seul.",
            "enfant-m|J'ai encore l'eau sur les doigts.",
            "maman|Un torchon, pour le nez.",
            "papa|La gouttière a fini ses gouttes.",
            "narrateur|Le métal redevient silencieux, tout gris.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Ils rentrent en comptant encore, tout bas.",
            "enfant-m|Plic.",
            "enfant-m|On s'arrête.",
            "enfant-f|Il est resté près de l'eau.",
            "papa|Vous avez bien écouté.",
            "maman|La soupe fait le même plic, dans les bols.",
            "narrateur|Une dernière goutte tombe, trop loin pour eux.",
        )
    return L(
        "narrateur|Sur le papier, le tuyau a des ronds tout le long.",
        "enfant-f|C'est la gouttière, en petit.",
        "enfant-m|Et la buée, on l'a laissée.",
        "maman|Le papier sèche.",
        "maman|La vitre aussi.",
        "papa|La soupe a fait un nouveau nuage.",
        "narrateur|Le rond essuyé s'est refermé, tout doux.",
    )


def color_fin(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila raccroche le manteau à pois.",
            "narrateur|Le bas laisse une goutte, puis plus rien.",
            "enfant-f|Les pois sont un peu froids.",
            "papa|Ils sécheront, près de la soupe.",
            "narrateur|Le crochet cliquette, une fois.",
        )
    if t1 == 2:
        return L(
            "narrateur|La soupe embue encore les lunettes.",
            "enfant-f|Je les pose près du bol.",
            "enfant-m|Elles ont bien vu.",
            "maman|Le torchon est là, si tu veux.",
            "narrateur|Un rond de buée s'installe sur un verre.",
        )
    return L(
        "narrateur|Aniss pose le seau sous l'évier, tout droit.",
        "enfant-m|Il sonne vide, maintenant.",
        "enfant-f|L'hôtel a fini son voyage.",
        "papa|La feuille, on la met au compost.",
        "narrateur|Le seau garde une odeur d'herbe, un peu.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "goutte"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La soupe laisse un nuage sur la vitre.",
        "narrateur|Ça sent le poireau, tout chaud.",
        "narrateur|Une trace d'argent traverse le verre, toute fine.",
        "narrateur|Le manteau à pois goutte encore au crochet.",
        "narrateur|Une goutte fait ploc, sur le paillasson.",
        "maman|Tu as entendu, Mila ?",
        "enfant-f|C'est le manteau.",
        "papa|Il sèche, tout doux.",
        "narrateur|Les lunettes de Mila sont près du bol.",
        "narrateur|Un peu de buée les rend floues.",
        "narrateur|En ce moment, papa essuie un rond sur la vitre.",
        "enfant-f|Il y avait un escargot rayé !",
        "papa|Il est parti ?",
        "enfant-f|Je veux le retrouver.",
        "enfant-f|Je lui fais une maison de feuille.",
        "maman|Aniss arrive, juste derrière la porte.",
        "narrateur|La porte fait toc toc, tout petit.",
        "enfant-m|On joue ?",
        "enfant-f|On cherche l'escargot.",
        "papa|Tu prends quoi, d'abord ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près du seuil, le manteau goutte encore.",
        "narrateur|Les lunettes reposent près du bol.",
        "narrateur|Le seau attend sous l'évier.",
        "maman|Qu'est-ce que tu prends d'abord, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le manteau à pois", "les lunettes", "le seau")

    for t1, tool in TOOL.items():
        p = pre(t1)
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|{tool['q_ask']}",
        )
        extras[f"{p}_Q0001"] = qf(tool["q_ans"], tool["q_acc"], tool["q_retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        if t1 == 1:
            s[f"{p}_T0002_P0000"] = L(
                "narrateur|La poche à pois est fermée, au seuil.",
                "narrateur|Le paillasson est tout près, encore mouillé.",
                "narrateur|Les pots luisent un peu plus loin.",
                "narrateur|La gouttière laisse une goutte.",
                "papa|La trace va où, d'après vous ?",
            )
        elif t1 == 2:
            s[f"{p}_T0002_P0000"] = L(
                "narrateur|Les lunettes gardent le fil d'argent, au seuil.",
                "narrateur|Le paillasson est tout près, encore mouillé.",
                "narrateur|Les pots luisent un peu plus loin.",
                "narrateur|La gouttière laisse une goutte.",
                "papa|La trace va où, d'après vous ?",
            )
        else:
            s[f"{p}_T0002_P0000"] = L(
                "narrateur|Le seau attend près du seuil, tout droit.",
                "narrateur|Le paillasson est tout près, encore mouillé.",
                "narrateur|Les pots luisent un peu plus loin.",
                "narrateur|La gouttière laisse une goutte.",
                "papa|La trace va où, d'après vous ?",
            )
        extras[f"{p}_T0002_P0000"] = t3lab("le paillasson", "les pots", "la gouttière")

        for t2, pl in PLACE.items():
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_core(t2) + color_t2(t1, t2)
            if t2 == 1:
                s[f"{sp}_T0003_P0000"] = L(
                    f"narrateur|{pl['secret']}",
                    "narrateur|On peut soulever le coin, attendre, ou dessiner.",
                    "maman|Vous faites quoi, tous les deux ?",
                )
            elif t2 == 2:
                s[f"{sp}_T0003_P0000"] = L(
                    f"narrateur|{pl['secret']}",
                    "narrateur|On peut poser la feuille, attendre, ou dessiner.",
                    "maman|Vous faites quoi, tous les deux ?",
                )
            else:
                s[f"{sp}_T0003_P0000"] = L(
                    f"narrateur|{pl['secret']}",
                    "narrateur|On peut faire une rampe, attendre, ou dessiner.",
                    "maman|Vous faites quoi, tous les deux ?",
                )
            extras[f"{sp}_T0003_P0000"] = t3lab("on le pose", "on attend", "on dessine")

            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_body(t2, t3) + color_t3(t1, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_body(t2, t3) + color_fin(t1)

    write_tree(s, extras, sons)
    relecture(
        SID,
        "Le manteau à pois et les lunettes de Mila",
        "Mila veut retrouver l'escargot rayé vu sur la vitre et lui faire une maison de feuille. "
        "Aniss l'aide. T1 = manteau (poche), lunettes (voir), seau (hôtel) : ça colore tout le voyage. "
        "T2×T3 = 9 aventures : paillasson / pots / gouttière × poser / attendre / dessiner. "
        "Les lunettes et le manteau à pois sont des outils, pas une leçon collée.",
        "Hugo hors troupe. Désir ≠ « on ne rit pas ». Questions factuelles (poche / trace / feuille). "
        "Fins vécues (soupe, buée, crochet). Audio non cuit. 27 chemins non écoutés à voix haute.",
    )


if __name__ == "__main__":
    main()
