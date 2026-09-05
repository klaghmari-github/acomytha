#!/usr/bin/env python3
"""TREE-DIF-030 — Le pain chaud d'Amir et le four du marché (N1, DIF.BES.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-030"
N1 = 10
TITLE = "Le pain chaud d'Amir et le four du marché"
FIL = (
    "Au marché, Amir veut le pain rond qui sort du four, encore chaud, "
    "pour le partager avec Chouchou. Ils emportent sac, serviette et pièce ; "
    "les trois partent. Le four est trop fort, la file trop vite, le banc trop "
    "agité. Neuf façons de laisser du temps. Le pain rentre, encore tiède."
)


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
    out["characters"] = "Amir, Chouchou, papa, maman"
    out["setting"] = "marché du village, four du boulanger"
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
        "plus de temps ou de calme",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
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
        "lab": "le sac",
        "cap": "Le sac",
        "t1q": "dans le sac",
        "t1acc": "sac | le sac | dans le sac | là-dedans",
        "t1retry": "Le pain ira dans le sac.",
        "coda": "Le sac sèche près des souliers.",
    },
    2: {
        "lab": "la serviette",
        "cap": "La serviette",
        "t1q": "dans la serviette",
        "t1acc": "serviette | la serviette | dans la serviette | le linge",
        "t1retry": "Le pain ira dans la serviette.",
        "coda": "La serviette sèche près des souliers.",
    },
    3: {
        "lab": "la pièce",
        "cap": "La pièce",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | la pièce",
        "t1retry": "La pièce est dans la poche.",
        "coda": "La pièce repose près du pain.",
    },
}

T3_LABS = {
    1: ("attendre un peu", "reculer", "derrière la farine"),
    2: ("son tour", "le bord", "répéter"),
    3: ("le pigeon", "s'asseoir", "l'ombre"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir glisse la main dans le sac.",
            "enfant-m|Le pain ira là-dedans.",
            "maman|Tiens-le ouvert, tout doux.",
            "narrateur|Le tissu sent encore la farine.",
            "papa|La serviette aussi, près de toi.",
            "narrateur|Maman y pose la pièce, tout léger.",
            "narrateur|Le sac emmène tout, maintenant.",
            "enfant-m|Chouchou, on va au four.",
            "enfant-f|J'arrive, tout doux.",
            "papa|Le sac d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir prend la serviette, encore tiède.",
            "enfant-m|J'enveloppe le pain avec.",
            "papa|Plie-la, comme un nid.",
            "narrateur|Le linge sent le soleil séché.",
            "maman|Le sac, ensuite, près des pieds.",
            "narrateur|Elle glisse la pièce dans le tissu.",
            "narrateur|La serviette emmène tout, maintenant.",
            "enfant-m|Chouchou, on y va.",
            "enfant-f|Je suis là.",
            "maman|La serviette d'abord, elle est prête.",
        )
    return L(
        "narrateur|Amir prend la pièce, toute ronde.",
        "enfant-m|C'est pour le pain chaud.",
        "maman|Glisse-la dans ta poche.",
        "narrateur|Un petit tintement sonne contre le tissu.",
        "papa|Le sac et la serviette, avec vous.",
        "narrateur|Il les pose près des sandales.",
        "narrateur|La pièce part avec le reste.",
        "enfant-m|Chouchou, viens !",
        "enfant-f|J'arrive près des caisses.",
        "papa|La pièce d'abord, elle est prête.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            f"narrateur|{o['cap']} reste ouvert, contre sa hanche.",
            "enfant-f|Ça sent déjà le chaud.",
            "enfant-m|On le mettra dedans.",
            "maman|Chouchou, tu viens avec nous ?",
            "enfant-f|Oui, tout lent.",
            "papa|On avance vers le four ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            f"narrateur|{o['cap']} pend, comme un nid.",
            "enfant-m|Le pain va dormir là.",
            "enfant-f|Pas trop vite, d'accord ?",
            "papa|Le four fume déjà, là-bas.",
            "maman|Vos pieds, dans les sandales ?",
            "enfant-m|Oui, maman.",
        )
    return L(
        f"narrateur|{o['cap']} tinte encore, dans la poche.",
        "enfant-m|Je la tiens, tout fort.",
        "enfant-f|Moi, je marche lentement.",
        "maman|Le four vous attend, tout blanc.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le marché s'ouvre, tout large.",
        "narrateur|Le four fume devant, tout blanc.",
        "narrateur|Puis la file avance, trop vite.",
        "narrateur|Plus loin, un banc attend.",
        "papa|Vous allez où, tous les deux ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le sac tape un peu sa hanche.",
            2: "narrateur|La serviette frôle sa joue, tiède.",
            3: "narrateur|La pièce tinte au fond du sac.",
        }[t1]
        return L(
            lead,
            "narrateur|Le four souffle, trop fort, trop chaud.",
            "enfant-f|Mes oreilles n'aiment pas.",
            "narrateur|Chouchou met les mains, tout contre.",
            "enfant-m|Le pain est là, tout rond.",
            "papa|Le four chante trop fort, ici.",
            "maman|Elle a besoin de calme.",
            f"narrateur|{o['cap']} reste collé, sans bouger.",
            "enfant-m|On fait comment, alors ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le sac se serre, trop près des genoux.",
            2: "narrateur|La serviette se plie, trop vite.",
            3: "narrateur|La pièce se perd un instant.",
        }[t1]
        return L(
            lead,
            "narrateur|La file pousse, trop vite, trop près.",
            "enfant-f|Mes pieds n'y arrivent pas.",
            "narrateur|Chouchou s'arrête, collée au sac.",
            "enfant-m|Le pain va partir sans nous.",
            "papa|Les pas sont trop pressés, ici.",
            "maman|Elle a besoin de temps.",
            f"narrateur|{o['cap']} attend, tout bas.",
            "enfant-m|On fait comment, Chouchou ?",
            "maman|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Le sac bute contre le pied du banc.",
        2: "narrateur|La serviette glisse vers le bois chaud.",
        3: "narrateur|La pièce tinte contre le banc.",
    }[t1]
    return L(
        lead,
        "narrateur|Autour du banc, ça parle trop fort.",
        "enfant-f|Le pigeon a trop bougé.",
        "narrateur|Chouchou recule, les mains aux oreilles.",
        "enfant-m|On s'assoit pour le pain ?",
        "papa|Ici, ce n'est pas calme.",
        "maman|Elle veut un coin calme.",
        f"narrateur|{o['cap']} reste sur ses genoux.",
        "enfant-m|On fait comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le four souffle encore, trop fort.",
            "papa|Attendre, reculer, ou derrière la farine ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La file avance encore, trop vite.",
            "maman|Son tour, le bord, ou répéter ?",
        )
    return L(
        "narrateur|Le banc reste trop agité, trop bruyant.",
        "papa|Le pigeon, s'asseoir, ou l'ombre ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Le sac reste ouvert, contre sa hanche.",
            2: "narrateur|La serviette reste pliée, comme un nid.",
            3: "narrateur|La pièce reste au fond, tout calme.",
        }[t1]
        return L(
            "enfant-m|On attend un peu.",
            "enfant-f|Moi aussi, j'attends.",
            "narrateur|Le souffle du four baisse, tout lent.",
            "narrateur|Chouchou baisse les mains, tout doux.",
            hold,
            "papa|Il chante moins, maintenant.",
            "enfant-m|Tu peux regarder.",
            "maman|Vous lui avez laissé le temps.",
            "enfant-f|Je vois le pain rond.",
        )
    if t2 == 1 and t3 == 2:
        step = {
            1: "narrateur|Amir recule avec le sac, un pas.",
            2: "narrateur|Amir recule avec la serviette, un pas.",
            3: "narrateur|Amir recule, la pièce dans la poche.",
        }[t1]
        return L(
            "enfant-m|On recule, tout doux.",
            "enfant-f|Plus loin du chaud.",
            step,
            "narrateur|Le bruit devient petit, comme un chuchotement.",
            "narrateur|Chouchou lève un peu les yeux.",
            "papa|Vous avez regardé d'abord.",
            "enfant-m|On avance, maintenant ?",
            "maman|Quand elle est prête.",
            "enfant-f|Le pain est encore là.",
        )
    if t2 == 1 and t3 == 3:
        hide = {
            1: "narrateur|Amir glisse le sac derrière la farine.",
            2: "narrateur|Amir glisse la serviette derrière la farine.",
            3: "narrateur|La pièce tinte, derrière le sac de farine.",
        }[t1]
        return L(
            "enfant-m|Derrière la farine, c'est plus calme.",
            "enfant-f|Je viens, tout près.",
            hide,
            "narrateur|Le sac de farine fait un mur blanc.",
            "narrateur|Le four reste de l'autre côté.",
            "papa|Ici, ça ne souffle plus.",
            "enfant-m|On observe d'abord.",
            "maman|Vous avez trouvé le coin tranquille.",
            "enfant-f|Je vois le pain, par ici.",
        )
    if t2 == 2 and t3 == 1:
        wait = {
            1: "narrateur|Le sac pend, sans se presser.",
            2: "narrateur|La serviette pend, sans se presser.",
            3: "narrateur|La pièce reste au fond, sans tinter.",
        }[t1]
        return L(
            "enfant-m|On attend notre tour.",
            "enfant-f|Je compte les pieds, tout lent.",
            "narrateur|Un pas, puis un autre, puis le silence.",
            wait,
            "narrateur|Chouchou avance quand le dos bouge.",
            "papa|Vous n'avez pas poussé.",
            "enfant-m|C'est à nous, maintenant.",
            "maman|Elle a eu le temps.",
            "enfant-f|Le pain est encore chaud.",
        )
    if t2 == 2 and t3 == 2:
        edge = {
            1: "narrateur|Amir glisse le sac le long du bord.",
            2: "narrateur|Amir glisse la serviette le long du bord.",
            3: "narrateur|La pièce tinte, tout au bord.",
        }[t1]
        return L(
            "enfant-m|On prend le bord, Chouchou.",
            "enfant-f|Pas au milieu, d'accord.",
            edge,
            "narrateur|Ils longent les caisses, sans se bousculer.",
            "narrateur|Chouchou pose un pied, puis l'autre.",
            "papa|Vous avez vu le chemin, d'abord.",
            "enfant-m|On y est.",
            "maman|Le bord était assez large.",
            "enfant-f|Je n'ai pas couru.",
        )
    if t2 == 2 and t3 == 3:
        again = {
            1: "narrateur|Amir reprend le sac, tout au début.",
            2: "narrateur|Amir reprend la serviette, tout au début.",
            3: "narrateur|Amir reprend la pièce, tout au début.",
        }[t1]
        return L(
            "enfant-m|On recommence, plus lent.",
            "enfant-f|Je te suis, cette fois.",
            again,
            "narrateur|Ils refont le chemin, pas après pas.",
            "narrateur|Chouchou répète chaque pas, tout doux.",
            "papa|Vous avez repris le même sentier.",
            "enfant-m|Tu peux, maintenant.",
            "maman|Le même chemin a aidé.",
            "enfant-f|J'y suis arrivée.",
        )
    if t2 == 3 and t3 == 1:
        bird = {
            1: "narrateur|Le sac reste sur les genoux, tout calme.",
            2: "narrateur|La serviette reste sur les genoux, tout calme.",
            3: "narrateur|La pièce reste dans la poche, tout calme.",
        }[t1]
        return L(
            "enfant-m|On attend le pigeon.",
            "enfant-f|Il va se poser, je crois.",
            "narrateur|L'oiseau se tait, une patte, puis l'autre.",
            bird,
            "narrateur|Chouchou baisse les mains, tout lent.",
            "papa|Il n'a plus bougé trop fort.",
            "enfant-m|On peut s'asseoir.",
            "maman|Vous avez regardé, d'abord.",
            "enfant-f|Il est calme, maintenant.",
        )
    if t2 == 3 and t3 == 2:
        sit = {
            1: "narrateur|Amir pose le sac sur le bois.",
            2: "narrateur|Amir pose la serviette sur le bois.",
            3: "narrateur|Amir pose la pièce sur le bois.",
        }[t1]
        return L(
            "enfant-m|On s'assoit, d'abord.",
            "enfant-f|Moi aussi, je m'assois.",
            sit,
            "narrateur|Le bois du banc est tiède, un peu rêche.",
            "narrateur|Chouchou pose les mains, sans les coller.",
            "papa|Ici, on ne court plus.",
            "enfant-m|Après, on prend le pain.",
            "maman|Vous vous êtes arrêtés, ensemble.",
            "enfant-f|Mes oreilles vont mieux.",
        )
    shade = {
        1: "narrateur|Amir glisse le sac vers l'ombre.",
        2: "narrateur|Amir glisse la serviette vers l'ombre.",
        3: "narrateur|La pièce tinte, vers l'ombre du banc.",
    }[t1]
    return L(
        "enfant-m|L'ombre, au bout du banc.",
        "enfant-f|Là, ça parle moins.",
        shade,
        "narrateur|Un bout de toile fait un toit gris.",
        "narrateur|Chouchou s'y glisse, tout contre le bois.",
        "papa|Le soleil n'entre pas, là.",
        "enfant-m|On reste un peu.",
        "maman|Vous avez trouvé le coin lent.",
        "enfant-f|Je suis prête, après.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le pain rond entre dans le sac, encore tiède.",
            "enfant-f|On a attendu, et il est venu.",
            "enfant-m|Il sent la croûte, tout chaud.",
            "papa|Merci, vous avez attendu ensemble.",
            "maman|La soupe est prête, dedans.",
            f"narrateur|{coda}",
            "narrateur|Une miette reste sur le bois du banc.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Ils rentrent, le pain contre la serviette.",
            "enfant-m|On a reculé, d'abord.",
            "enfant-f|Le four n'était plus trop fort.",
            "papa|Vous avez vu avant d'avancer.",
            "maman|Rentrez, le pain refroidit.",
            f"narrateur|{coda}",
            "narrateur|La croûte craque encore, tout petit.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Derrière la farine, le pain les suit.",
            "enfant-f|Ce coin-là était le bon.",
            "enfant-m|Il n'a pas trop chanté.",
            "maman|Vous avez changé de place.",
            "papa|Le four souffle encore, plus loin.",
            f"narrateur|{coda}",
            "narrateur|Au seuil, ça sent encore le chaud.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le pain tiède pose une ombre sur la table.",
            "enfant-m|On a attendu notre tour.",
            "enfant-f|J'ai compté les pieds.",
            "papa|Vous n'avez pas poussé.",
            "maman|Lavez les mains, tout doux.",
            f"narrateur|{coda}",
            "narrateur|Une odeur de farine reste dans l'entrée.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils n'ont pas couru dans toute la file.",
            "enfant-f|Le bord était assez large.",
            "enfant-m|Tes pas y allaient, Chouchou.",
            "maman|Le pain est encore chaud, sur la table.",
            "papa|Chacun a marché à son rythme.",
            f"narrateur|{coda}",
            "narrateur|Une miette brille près de la fenêtre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Le même chemin les ramène, plus lent.",
            "enfant-m|On a recommencé, tous les deux.",
            "enfant-f|Cette fois, j'ai suivi.",
            "papa|Le chemin repris a ouvert la file.",
            "maman|Coupez-le, tout doux, en deux.",
            f"narrateur|{coda}",
            "narrateur|Deux parts tièdes attendent dans l'assiette.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le pigeon reste sur la caisse, tout calme.",
            "enfant-f|On l'a regardé, d'abord.",
            "enfant-m|Puis le pain est venu.",
            "maman|Essuie tes pieds, sur le paillasson.",
            "papa|Le pain est à vous, maintenant.",
            f"narrateur|{coda}",
            "narrateur|Dehors, le banc redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Un peu de soleil les suit jusqu'à la porte.",
            "enfant-m|On s'est assis, d'abord.",
            "enfant-f|Mes oreilles ont eu le temps.",
            "papa|Le banc vous a gardés un moment.",
            "maman|Le pain sèche déjà, sur le linge.",
            f"narrateur|{coda}",
            "narrateur|La vitre garde une odeur de croûte.",
        )
    return L(
        "narrateur|Un peu de poussière de farine reste au seuil.",
        "enfant-f|L'ombre était plus douce.",
        "enfant-m|On y est resté un peu.",
        "papa|Le coin du banc était le bon.",
        "maman|Vos mains sentent encore le pain.",
        f"narrateur|{coda}",
        "narrateur|Le pain rond s'endort sur la table.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une toile claque au-dessus des caisses.",
        "narrateur|Ça sent le pain, tout chaud.",
        "narrateur|Un pigeon marche sur une caisse.",
        "papa|Tu as vu le four, Amir ?",
        "enfant-m|Il fume, tout blanc.",
        "maman|La croûte craque déjà, là-bas.",
        "narrateur|En ce moment, Amir lève le nez.",
        "enfant-m|Je veux le pain rond.",
        "narrateur|Chouchou arrive, les pas tout petits.",
        "enfant-f|Le four fait trop de bruit.",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu regardes bien Chouchou.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des caisses.",
        "narrateur|Le sac, la serviette, et la pièce.",
        "maman|Tu prends quoi d'abord, Amir ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le sac", "la serviette", "la pièce")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        if t1 == 3:
            s[f"{p}_Q0001"] = L(
                "narrateur|Amir a glissé la pièce dans la poche.",
                "maman|Elle est où, la pièce ?",
            )
        else:
            s[f"{p}_Q0001"] = L(
                f"narrateur|Amir a préparé le pain {o['t1q']}.",
                "maman|Le pain ira où ?",
            )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le four", "la file", "le banc")

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
        "Au marché, Amir veut le pain rond qui sort du four, encore chaud, "
        "pour le partager avec Chouchou. T1 = sac / serviette / pièce "
        "(les trois partent). T2 = four trop fort / file trop vite / banc trop "
        "agité. T3 = neuf résolutions (attendre, reculer, derrière la farine ; "
        "son tour, le bord, répéter ; pigeon, s'asseoir, l'ombre). La leçon "
        "(plus de temps, plus de calme) se vit dans les gestes, sans slogan. "
        "Fin : le pain rentre, encore tiède.",
        "N1 ≤ 10. Sami / Tom / Léa et bac/toboggan/balançoires jetés. "
        "Titre leçon collée remplacé (objet + désir). Pas de calque AUT-001 "
        "(capitaine, plic, volet jaune). Un merci de papa lié au geste "
        "(regarder Chouchou). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
