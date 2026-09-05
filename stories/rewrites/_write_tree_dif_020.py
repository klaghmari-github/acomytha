#!/usr/bin/env python3
"""TREE-DIF-020 — L'escargot de Mila et la feuille du balcon (N3, F-NAR-018)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N3 = LIMITS["N3"]
SID = "TREE-DIF-020"
TITLE = "L'escargot de Mila et la feuille du balcon"
FIL = (
    "Après la pluie, Mila veut que son escargot arrive à une feuille mouillée "
    "avant que le soleil sèche le bois. Elle prépare d'abord la boîte, "
    "le compte-gouttes ou la feuille ; les trois partent. Nina reste au seuil, "
    "elle a besoin de calme. Gouttière trop vite, linge trop agité, carreaux trop chauds. "
    "Neuf façons de laisser du temps. L'escargot arrive."
)


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"sans fin: {ph}")
    return list(rows)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def pre(t1: int) -> str:
    return f"CHK_T0001_P000{t1}"


PREP = {
    1: dict(
        label="la boîte",
        coda="La boîte sèche près de la fenêtre, le couvercle entrouvert.",
        son="",
    ),
    2: dict(
        label="le compte-gouttes",
        coda="Une goutte reste au bout du compte-gouttes, près du savon.",
        son="goutte",
    ),
    3: dict(
        label="la feuille",
        coda="La feuille sèche sur le rebord, un peu recroquevillée.",
        son="",
    ),
}

T3_BY_T2 = {
    1: t3lab("attendre un peu", "regarder d'abord", "le petit filet"),
    2: t3lab("attendre le vent", "tenir le drap", "derrière"),
    3: t3lab("l'ombre", "goutte à goutte", "sous le pot"),
}

Q_BY_T1 = {
    1: qf(
        "répéter",
        "répéter | répète | observer | observer d'abord | attendre | attendre un peu",
        "On peut répéter. Que fait-on ?",
    ),
    2: qf(
        "répéter",
        "répéter | répète | observer | observer d'abord | attendre | attendre un peu",
        "On peut répéter. Que fait-on ?",
    ),
    3: qf(
        "répéter",
        "répéter | répète | observer | observer d'abord | attendre | attendre un peu",
        "On peut répéter. Que fait-on ?",
    ),
}


def t1_pass(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila glisse l'escargot dans la boîte, tout doux.",
            "enfant-f|Tu voyages ici.",
            "maman|Ferme le couvercle, pas trop fort.",
            "narrateur|Un petit toc sonne contre le carton.",
            "papa|Le compte-gouttes aussi, pour le chemin.",
            "narrateur|Maman pose la feuille mouillée près de la boîte.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Nina va le voir marcher.",
            "narrateur|Des pas légers s'arrêtent près de la porte.",
            "copine|Mila, je suis là.",
            "enfant-f|Viens, on va au balcon.",
            "narrateur|Nina reste sur le seuil, les mains sur le cadre.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila prend le compte-gouttes, encore plein.",
            "enfant-f|Je fais un chemin mouillé.",
            "papa|Une goutte, puis une autre, tout lent.",
            "narrateur|L'eau trace une ligne sur le bois.",
            "maman|La boîte, ensuite, près de toi.",
            "narrateur|Elle glisse la feuille par-dessus.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Nina va tout voir.",
            "narrateur|La porte du balcon s'ouvre, tout léger.",
            "copine|Me voilà, Mila.",
            "enfant-f|On suit les gouttes ?",
            "narrateur|Nina s'arrête au seuil, sans avancer.",
        )
    return L(
        "narrateur|Mila prend la feuille, encore froide de pluie.",
        "enfant-f|C'est ta maison, tout au bout.",
        "maman|Tiens-la comme un toit, tout doux.",
        "narrateur|La feuille sent l'herbe et l'eau.",
        "papa|La boîte et le compte-gouttes, avec vous.",
        "narrateur|Il les pose près des sandales.",
        "narrateur|Les trois affaires partent ensemble.",
        "enfant-f|Nina, vite !",
        "narrateur|Des pas frais sonnent sur le carreau.",
        "copine|J'arrive, Mila.",
        "enfant-f|Je te montre l'escargot.",
        "narrateur|Nina reste près du cadre, tout calme.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina regarde la boîte, sans bouger.",
            "maman|Que peut-on faire ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina regarde les gouttes, sans bouger.",
            "papa|Que peut-on faire ?",
        )
    return L(
        "narrateur|Nina regarde la feuille, sans bouger.",
        "maman|Que peut-on faire ?",
    )


def t1_c(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|On répète, tout doux.",
            "enfant-f|On regarde d'abord.",
            "copine|Je reste ici, un peu.",
            "papa|Elle a le temps.",
            "narrateur|Nina écoute, les mains sur le bois.",
            "maman|Vous partez quand elle est prête.",
            "enfant-f|Oui, maman.",
            "narrateur|La boîte reste tiède, contre sa paume.",
        )
    if t1 == 2:
        return L(
            "enfant-f|On répète le chemin, goutte après goutte.",
            "enfant-f|On observe d'abord.",
            "copine|Je te vois, d'ici.",
            "maman|Elle a le temps.",
            "narrateur|Une goutte tremble au bout du verre.",
            "papa|Vous partez quand elle est prête.",
            "enfant-f|Oui, papa.",
            "narrateur|Le bois garde encore la ligne d'eau.",
        )
    return L(
        "enfant-f|On répète, tout bas.",
        "enfant-f|La feuille attend, on regarde.",
        "copine|Je viens après.",
        "papa|Elle a le temps.",
        "narrateur|Nina suit des yeux la nervure verte.",
        "maman|Vous partez quand elle est prête.",
        "enfant-f|Oui.",
        "narrateur|La feuille perle encore, une goutte au bord.",
    )


def t2_q(t1: int) -> list[str]:
    head = {
        1: "La boîte tape un peu le bois, à chaque pas.",
        2: "Une goutte tombe devant elles, puis une autre.",
        3: "La feuille tremble entre les doigts de Mila.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Le balcon fume encore, tout mouillé.",
        "papa|La gouttière, le linge, ou les carreaux ?",
    )


def t2_pass(t1: int, t2: int) -> list[str]:
    head = {
        1: "Un coin de la boîte frotte encore le bois.",
        2: "Une perle tombe du compte-gouttes, sur le seuil.",
        3: "La feuille mouillée colle un peu à sa paume.",
    }[t1]
    if t2 == 1:
        extra = {
            1: "Mila pose la boîte au bord, le couvercle ouvert.",
            2: "Une goutte du verre se perd dans le courant.",
            3: "La feuille frôle le zinc, trop vite emportée.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|La gouttière chante trop fort, trop vite.",
            f"narrateur|{extra}",
            "enfant-f|L'eau emporte tout.",
            "narrateur|L'escargot rentre dans sa coquille, tout petit.",
            "copine|Il a peur.",
            "papa|Le filet est trop fort, ici.",
            "maman|Il a besoin de calme.",
            "enfant-f|On fait comment, alors ?",
            "papa|Vous trouvez, toutes les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "La boîte penche quand le drap claque.",
            2: "Les gouttes du linge brouillent le chemin d'eau.",
            3: "La feuille s'envole un peu, puis retombe.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|Un drap mouillé claque, encore et encore.",
            f"narrateur|{extra}",
            "enfant-f|Ça bouge trop.",
            "narrateur|Nina recule d'un pas, les mains aux oreilles.",
            "copine|C'est trop fort.",
            "maman|Le vent n'a pas fini.",
            "papa|L'escargot n'avance plus.",
            "enfant-f|On fait comment, Nina ?",
            "maman|Vous trouvez, toutes les deux ?",
        )
    extra = {
        1: "Le carton de la boîte chauffe déjà, un peu.",
        2: "Les gouttes sèchent avant d'arriver au bout.",
        3: "La feuille se recroqueville, trop vite.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Les carreaux du jardin brillent, trop chauds.",
        f"narrateur|{extra}",
        "enfant-f|La trace d'argent s'arrête.",
        "narrateur|L'escargot reste collé, sans bouger.",
        "copine|Il n'aime pas le chaud.",
        "papa|Le soleil a déjà trop séché.",
        "maman|Il a besoin de temps.",
        "enfant-f|On fait comment, alors ?",
        "papa|Vous trouvez, toutes les deux ?",
    )


def t3_q(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'eau de la gouttière chante encore trop vite.",
            "papa|Attendre, regarder, ou le petit filet ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le drap claque encore, trop fort.",
            "maman|Attendre le vent, tenir, ou derrière ?",
        )
    return L(
        "narrateur|Les carreaux restent trop chauds, trop secs.",
        "papa|L'ombre, goutte à goutte, ou sous le pot ?",
    )


def t3_pass(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "La boîte attend au bord, le couvercle ouvert.",
        2: "Une perle tremble encore au bout du compte-gouttes.",
        3: "La feuille reste dans sa main, un peu froide.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-f|On attend un peu.",
            "copine|Moi aussi, j'attends.",
            "narrateur|Les gouttes se calment, une, puis une autre.",
            "narrateur|L'escargot sort deux cornes, tout lent.",
            f"narrateur|{col}",
            "papa|Le filet a baissé, maintenant.",
            "enfant-f|Tu peux marcher.",
            "maman|Vous lui avez laissé le temps.",
            "copine|Il avance, Mila.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-f|On regarde d'abord.",
            "copine|Le bord du zinc, là.",
            "narrateur|Elles observent le courant, sans toucher.",
            "narrateur|Un filet plus calme longe le bois.",
            f"narrateur|{col}",
            "papa|Vous avez vu avant de poser.",
            "enfant-f|Par ici, tout doux.",
            "maman|Observer d'abord, ça a aidé.",
            "copine|Il suit le calme.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-f|Le petit filet, le long du bois.",
            "copine|Pas la gouttière, plus bas.",
            "narrateur|Mila pose l'escargot sur la planche humide.",
            "narrateur|L'eau y glisse, toute mince, toute lente.",
            f"narrateur|{col}",
            "papa|Ce chemin-là n'emporte rien.",
            "enfant-f|Tu y vas.",
            "maman|Vous avez changé de filet.",
            "copine|Il avance, enfin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-f|On attend que le vent se taise.",
            "copine|Je reste près de toi.",
            "narrateur|Le drap claque encore, puis s'apaise.",
            "narrateur|Nina baisse les mains, tout doux.",
            f"narrateur|{col}",
            "maman|Le linge retombe, comme un mur calme.",
            "enfant-f|Maintenant, on pose.",
            "papa|Vous avez attendu le silence.",
            "copine|Il sort, Mila.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-f|On tient le drap, toutes les deux.",
            "copine|Je prends ce coin.",
            "narrateur|Les deux filles tendent le tissu, tout large.",
            "narrateur|Le vent pousse, mais le drap ne claque plus.",
            f"narrateur|{col}",
            "papa|Vos mains font un abri.",
            "enfant-f|Pose-toi, tout doux.",
            "maman|Vous l'avez tenu ensemble.",
            "copine|Il avance dessous.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-f|Derrière le drap, c'est plus calme.",
            "copine|Je viens, tout près.",
            "narrateur|Elles glissent derrière le linge, à l'abri.",
            "narrateur|Le vent reste de l'autre côté.",
            f"narrateur|{col}",
            "maman|Ici, ça ne claque plus.",
            "enfant-f|Ta feuille est là.",
            "papa|Vous avez trouvé le coin tranquille.",
            "copine|Il marche, Mila.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-f|L'ombre du bac, Nina.",
            "copine|Là, le carreau est plus frais.",
            "narrateur|Elles se mettent à l'ombre, tout contre le bac.",
            "narrateur|Le bois y reste sombre, encore mouillé.",
            f"narrateur|{col}",
            "papa|Le soleil n'atteint plus le chemin.",
            "enfant-f|Tu peux sortir.",
            "maman|Vous avez cherché le frais.",
            "copine|La trace reprend, argentée.",
        )
    if t2 == 3 and t3 == 2:
        wet = {
            1: "Mila mouille le bord de la boîte, goutte à goutte.",
            2: "Mila reprend le compte-gouttes, goutte à goutte.",
            3: "Mila mouille la nervure de la feuille, goutte à goutte.",
        }[t1]
        return L(
            "enfant-f|Goutte à goutte, tout lent.",
            "copine|Je compte avec toi.",
            f"narrateur|{wet}",
            "narrateur|Une perle, puis une autre, sur le carreau chaud.",
            f"narrateur|{col}",
            "papa|Le chemin redevient mouillé.",
            "enfant-f|Tu suis l'eau.",
            "maman|Vous n'avez pas pressé.",
            "copine|Il avance, enfin.",
        )
    under = {
        1: "Mila glisse la boîte sous le rebord du pot.",
        2: "Une goutte tombe sous le pot, puis l'escargot.",
        3: "Mila glisse la feuille sous le rebord du pot.",
    }[t1]
    return L(
        "enfant-f|Sous le pot, c'est encore mouillé.",
        "copine|Je me baisse, moi aussi.",
        f"narrateur|{under}",
        "narrateur|La terre y sent la pluie, encore fraîche.",
        f"narrateur|{col}",
        "papa|Le soleil n'entre pas, là.",
        "enfant-f|Ta maison est au bout.",
        "maman|Vous avez trouvé l'endroit lent.",
        "copine|Il arrive, Mila.",
    )


def t3_fin(t1: int, t2: int, t3: int) -> list[str]:
    cd = PREP[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|L'escargot atteint la feuille, deux cornes dressées.",
            "copine|On a attendu, et il est venu.",
            "enfant-f|Il est arrivé.",
            "papa|Merci d'avoir laissé le temps.",
            "maman|La soupe est prête, dedans.",
            f"narrateur|{cd}",
            "narrateur|La bassine fait un dernier toc, puis se tait.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|La feuille brille au bout du filet calme.",
            "enfant-f|On a regardé d'abord.",
            "copine|Le zinc n'emportait plus rien.",
            "papa|Vous avez vu avant de poser.",
            "maman|Rentrez, le bois refroidit.",
            f"narrateur|{cd}",
            "narrateur|Une trace d'argent sèche déjà sur le zinc.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le petit filet mène jusqu'à la feuille, tout mince.",
            "copine|Ce chemin-là était le bon.",
            "enfant-f|Il n'a pas été emporté.",
            "maman|Vous avez changé de courant.",
            "papa|La gouttière chante encore, plus loin.",
            f"narrateur|{cd}",
            "narrateur|Au balcon, le bois redevient sombre, tout calme.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le drap pend, enfin immobile, au-dessus d'eux.",
            "enfant-f|On a attendu le vent.",
            "copine|Mes oreilles n'entendent plus le claquement.",
            "papa|Le silence vous a aidées.",
            "maman|Le linge sent encore le savon.",
            f"narrateur|{cd}",
            "narrateur|Une goutte glisse le long du tissu, puis plus.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le drap reste tendu, un abri de toile.",
            "copine|On l'a tenu, toutes les deux.",
            "enfant-f|L'escargot est sur la feuille.",
            "papa|Vos mains ont fait le calme.",
            "maman|Rentrez, je sèche vos poignets.",
            f"narrateur|{cd}",
            "narrateur|De l'autre côté, le vent passe sans les toucher.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Derrière le drap, l'air est frais et sombre.",
            "enfant-f|C'était plus calme, ici.",
            "copine|Il a marché jusqu'à la feuille.",
            "maman|Vous avez trouvé le coin tranquille.",
            "papa|Le salon vous attend, tout tiède.",
            f"narrateur|{cd}",
            "narrateur|Dehors, le linge claque encore, plus loin.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|À l'ombre du bac, la feuille reste mouillée.",
            "copine|Le carreau n'était plus trop chaud.",
            "enfant-f|Il est arrivé.",
            "papa|Vous avez cherché le frais.",
            "maman|Essuie tes pieds, sur le paillasson.",
            f"narrateur|{cd}",
            "narrateur|Au milieu, le soleil reste sur les carreaux, tout seul.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Goutte après goutte, la feuille a repris l'eau.",
            "enfant-f|On n'a pas pressé.",
            "copine|J'ai compté avec toi.",
            "papa|Le chemin est resté mouillé.",
            "maman|Vos doigts sentent encore la pluie.",
            f"narrateur|{cd}",
            "narrateur|Une perle sèche au milieu d'un carreau, puis s'en va.",
        )
    return L(
        "narrateur|Sous le pot, la terre garde encore la pluie.",
        "enfant-f|Il a trouvé sa feuille, au frais.",
        "copine|On s'est baissées, toutes les deux.",
        "papa|L'endroit lent était là.",
        "maman|Rentrez, la soupe fume.",
        f"narrateur|{cd}",
        "narrateur|Une petite ombre ronde reste sous le rebord du pot.",
    )


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
        scale, rate = (1.28, "slow") if kind in ("passage_question", "transition_question") else (1.22, "medium")
        raw_son = sons.get(cid)
        if raw_son is None:
            raw_son = c.get("sons") or ""
            if raw_son == "chien_bonjour":
                raw_son = ""
        nc = make_chunk(c, scripts[cid], raw_son, scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Mila, Nina, papa, maman"
    out["setting"] = "balcon de bois après la pluie, gouttière, linge, carreaux"
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
        "lila",
        "il ne faut pas",
        "plus de temps ou de calme",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "goutte"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le bois du balcon est encore sombre, tout mouillé.",
        "narrateur|Une trace d'argent brille, fine comme un fil.",
        "narrateur|Le linge goutte dans une bassine, une fois, puis encore.",
        "narrateur|La bassine fait toc, puis se tait.",
        "papa|Tu as vu la trace, Mila ?",
        "enfant-f|Elle va vers la feuille.",
        "maman|Nina arrive pour la voir.",
        "narrateur|En ce moment, Mila tient un escargot au creux de la main.",
        "narrateur|Il est frais, et il avance à peine.",
        "enfant-f|Je veux qu'il arrive à la feuille.",
        "papa|Le soleil sèche déjà le bois.",
        "maman|On prend les affaires, alors ?",
        "papa|Merci, tu le tiens tout doux.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des sandales.",
        "narrateur|La boîte, le compte-gouttes, et la feuille.",
        "maman|Tu prends quoi d'abord, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la boîte", "le compte-gouttes", "la feuille")

    for t1 in (1, 2, 3):
        p = pre(t1)
        s[p] = t1_pass(t1)
        sons[p] = PREP[t1]["son"]
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = Q_BY_T1[t1]
        s[f"{p}_C0001"] = t1_c(t1)
        s[f"{p}_T0002_P0000"] = t2_q(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la gouttière", "le linge", "les carreaux")
        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_pass(t1, t2)
            sons[sp] = {1: "goutte", 2: "tissu", 3: ""}[t2]
            s[f"{sp}_T0003_P0000"] = t3_q(t2)
            extras[f"{sp}_T0003_P0000"] = T3_BY_T2[t2]
            for t3 in (1, 2, 3):
                tp = f"{sp}_T0003_P000{t3}"
                s[tp] = t3_pass(t1, t2, t3)
                s[f"{tp}_F0001"] = t3_fin(t1, t2, t3)
                if t2 == 1:
                    sons[tp] = "goutte"
                elif t2 == 2:
                    sons[tp] = "tissu"
                else:
                    sons[tp] = ""

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Mila veut que son escargot arrive à une feuille mouillée, avant le soleil. "
        "T1 = boîte / compte-gouttes / feuille, les trois partent. Nina reste au seuil. "
        "T2×T3 = 9 aventures : gouttière (attendre, regarder, petit filet), "
        "linge (vent, tenir, derrière), carreaux (ombre, goutte à goutte, sous le pot). "
        "La leçon se vit : répéter, attendre, observer. Fin : l'escargot arrive.",
        "Slogan chambre / Lila jetés. Désir ≠ leçon. chunk_id inchangés. "
        "check() N3. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
