#!/usr/bin/env python3
"""TREE-AUT-008 / TREE-AUT-009 — N2, leçon implicite, 3 branches distinctes."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words

N2 = 15


def ln(*xs: str) -> list[str]:
    out = []
    for x in xs:
        role, ph = x.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def write_tree(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict[str, list[str]],
    qmap: dict[str, dict],
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={list(extra)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind == "passage_question":
            scale, rate = 1.28, "slow"
        else:
            scale, rate = 1.22, "medium"
        by[cid] = make_chunk(c, scripts[cid], c.get("sons") or "", scale, rate)
        if cid in qmap:
            by[cid].update(qmap[cid])
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in ("hugo", "sami", "tes affaires", "ce que l'adulte", "ce que j'ai dit"):
        if bad in blob:
            raise SystemExit(f"{sid} slogan/prénom: {bad}")
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def assemble(debut, t1q, l1, q, c, t2q, l2, t3q, l3, fin) -> dict[str, list[str]]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": debut,
        "CHK_T0001_P0000": t1q,
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = l1[i]
        s[f"{p}_Q0001"] = q[i]
        s[f"{p}_C0001"] = c[i]
        s[f"{p}_T0002_P0000"] = t2q
        for j in (1, 2, 3):
            s[f"{p}_T0002_P000{j}"] = l2[i][j]
            s[f"{p}_T0002_P000{j}_T0003_P0000"] = t3q
            for k in (1, 2, 3):
                s[f"{p}_T0002_P000{j}_T0003_P000{k}"] = l3(i, j, k)
                s[f"{p}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin(i, j, k)
    return s


# ---------------------------------------------------------------------------
# TREE-AUT-008 — Aniss, seau jaune, cour après la pluie (AUT.AFF.003)
# T1 cuisine / jardin / chambre : trois sorties vraiment différentes.
# ---------------------------------------------------------------------------

DEBUT_008 = ln(
    "narrateur|Une goutte tombe dans le seau jaune.",
    "narrateur|Ça sonne, comme une petite cloche.",
    "narrateur|La cour brille, toute mouillée.",
    "narrateur|Des feuilles collent aux dalles.",
    "narrateur|Ça sent la terre, après la pluie.",
    "narrateur|Un bol en terre tient les clés de papa.",
    "papa|Les clés sont au sec, Aniss.",
    "maman|La cour est encore une grande flaque.",
    "enfant-m|Je veux le seau, dans la cour.",
    "enfant-m|Je verse l'eau des flaques.",
    "maman|On y va, tout à l'heure.",
    "narrateur|En ce moment, Aniss touche le seau.",
    "narrateur|Le plastique est froid, un peu lisse.",
    "narrateur|Un manteau bleu pend au crochet.",
    "narrateur|Le doudou gris est sur le canapé.",
    "papa|Tu prends le seau avec toi ?",
    "enfant-m|Oui, papa.",
    "papa|Dehors, il fait encore frais.",
    "narrateur|Aniss lève le seau.",
    "narrateur|Une goutte roule sur le bord.",
    "maman|Où vas-tu d'abord ?",
)

T1Q_008 = ln(
    "narrateur|Aniss va où, d'abord ?",
    "papa|La cuisine, le jardin, ou la chambre.",
)

L1_008 = {
    1: ln(
        "narrateur|Aniss pousse la porte de la cuisine.",
        "narrateur|Le carrelage est froid, encore mouillé.",
        "narrateur|Une goutte a glissé de la fenêtre.",
        "narrateur|Ça sent le pain, tout tiède.",
        "narrateur|Le seau jaune est sous la table.",
        "narrateur|Un peu d'eau de pluie brille dedans.",
        "enfant-m|Il a déjà de l'eau, papa.",
        "papa|C'est la gouttière, par la fenêtre.",
        "maman|Tu le portes à deux mains ?",
        "narrateur|Aniss soulève le seau.",
        "narrateur|Il est plus lourd qu'il ne croyait.",
        "narrateur|Une goutte tombe sur son pied.",
        "enfant-m|Je fais une rivière, dans la cour.",
        "papa|On y va ?",
        "enfant-m|Oui.",
        "narrateur|Il marche vers la porte.",
        "narrateur|Le manteau reste sur la chaise.",
        "narrateur|Le doudou est près du radiateur.",
        "maman|Tu as le seau.",
        "maman|Et le manteau ?",
        "enfant-m|Oh.",
        "narrateur|Aniss s'arrête.",
    ),
    2: ln(
        "narrateur|Aniss ouvre la porte du jardin.",
        "narrateur|L'air sent l'herbe coupée, encore mouillée.",
        "narrateur|Une flaque ronde attend près du banc.",
        "narrateur|Le seau jaune est déjà dans l'eau.",
        "enfant-m|Il boit la flaque, maman.",
        "maman|Il est à moitié plein.",
        "papa|Tu verses vers l'autre flaque ?",
        "enfant-m|Oui, un chemin d'eau.",
        "narrateur|Aniss penche le seau.",
        "narrateur|L'eau fait un filet brillant.",
        "narrateur|Le manteau est resté sur le banc.",
        "narrateur|Le tissu boit la pluie, tout seul.",
        "narrateur|Le doudou est sous le banc, au sec.",
        "papa|Le banc est mouillé, Aniss.",
        "enfant-m|Mon manteau aussi ?",
        "papa|Un peu, oui.",
        "narrateur|Aniss pose le seau.",
        "narrateur|Il prend le manteau, tout doux.",
        "enfant-m|Il est froid.",
        "maman|On le met, alors ?",
        "enfant-m|Oui.",
    ),
    3: ln(
        "narrateur|Aniss court vers la chambre.",
        "narrateur|Le volet est encore un peu mouillé.",
        "narrateur|Par la fenêtre, la cour brille.",
        "enfant-m|Je la vois, papa.",
        "papa|Les flaques sont là, oui.",
        "narrateur|Le doudou gris est sur le lit.",
        "narrateur|Le seau jaune attend près de la porte.",
        "narrateur|Le manteau bleu est au pied du lit.",
        "enfant-m|J'y vais maintenant.",
        "maman|Avec le doudou ?",
        "narrateur|Aniss serre le doudou contre lui.",
        "narrateur|Il court vers la porte.",
        "narrateur|Le seau reste, tout seul.",
        "papa|Aniss.",
        "papa|Le seau est encore là.",
        "enfant-m|Oh.",
        "narrateur|Il revient sur ses pas.",
        "narrateur|L'anse du seau est froide.",
        "enfant-m|Je le prends.",
        "maman|Le manteau, aussi ?",
        "enfant-m|Oui, maman.",
    ),
}

Q_008 = {
    1: ln(
        "narrateur|Aniss tient le seau.",
        "maman|Il a oublié quoi, près de la chaise ?",
    ),
    2: ln(
        "narrateur|Le banc est mouillé.",
        "papa|Aniss reprend quoi, sur le banc ?",
    ),
    3: ln(
        "narrateur|Aniss court vers la porte.",
        "papa|Le seau est encore où ?",
    ),
}

C_008 = {
    1: ln(
        "narrateur|Aniss pose le seau un instant.",
        "narrateur|Il prend le manteau sur la chaise.",
        "enfant-m|Il était là.",
        "papa|Merci, Aniss.",
        "maman|Le doudou, tout à l'heure.",
        "narrateur|Le seau attend près du pied.",
        "enfant-m|On continue.",
    ),
    2: ln(
        "narrateur|Aniss essuie le manteau du plat de la main.",
        "enfant-m|Il est froid, encore.",
        "maman|Il va sécher, dehors.",
        "papa|Le doudou est sous le banc.",
        "narrateur|Aniss se baisse.",
        "narrateur|Le doudou est au sec.",
        "enfant-m|Toi aussi, tu viens.",
    ),
    3: ln(
        "narrateur|Aniss reprend le seau, près de la porte.",
        "narrateur|Il prend aussi le manteau.",
        "enfant-m|J'ai tout, maintenant.",
        "maman|Le doudou est contre toi.",
        "papa|On peut aller à la cour.",
        "enfant-m|Oui.",
    ),
}

T2Q_008 = ln(
    "narrateur|Près de quoi, Aniss ?",
    "maman|Les cubes, le livre, ou la dînette.",
)

L2_008 = {
    1: {
        1: ln(
            "narrateur|Sur le carrelage, une petite tour attend.",
            "narrateur|Un cube jaune est dans le seau.",
            "enfant-m|Il nage, papa.",
            "papa|Pêche-le, tout doux.",
            "narrateur|Aniss sort le cube.",
            "narrateur|Il le pose au bord de l'eau.",
            "enfant-m|C'est le barrage, pour la cour.",
            "maman|Le cube vient avec le seau ?",
            "enfant-m|Oui, un seul.",
            "papa|Les autres restent ici.",
            "narrateur|La tour penche un peu, puis tient.",
        ),
        2: ln(
            "narrateur|Un livre est ouvert sur la table.",
            "narrateur|Une barque est peinte, toute petite.",
            "enfant-m|Comme dans la cour, maman.",
            "maman|Une feuille peut faire bateau.",
            "narrateur|Une goutte du seau tremble au bord.",
            "papa|Le livre, on le recule.",
            "narrateur|Papa pousse le livre au sec.",
            "enfant-m|Il reste ici.",
            "maman|Oui, les pages n'aiment pas l'eau.",
            "narrateur|Aniss garde le seau contre lui.",
        ),
        3: ln(
            "narrateur|Deux tasses sont encore en rond.",
            "narrateur|Aniss verse une goutte dans une tasse.",
            "enfant-m|Soupe de pluie.",
            "papa|Tu goûtes, tout doux ?",
            "narrateur|Aniss touche l'eau du doigt.",
            "enfant-m|Elle est froide.",
            "maman|La tasse reste ici, alors ?",
            "enfant-m|Oui, le seau vient.",
            "narrateur|Il essuie le bord de la tasse.",
            "narrateur|La dînette reste sage, près du buffet.",
        ),
    },
    2: {
        1: ln(
            "narrateur|Dans l'herbe, des cubes sont mouillés.",
            "narrateur|Un cube glisse sous le doigt.",
            "enfant-m|Ils sont trop glissants.",
            "papa|Pour le barrage, un seul suffit.",
            "narrateur|Aniss pose un cube au bord de la flaque.",
            "narrateur|L'eau tourne autour, tout doux.",
            "maman|Les autres restent dans l'herbe ?",
            "enfant-m|Oui.",
            "papa|Le manteau, tu l'as ?",
            "enfant-m|Sur moi.",
            "narrateur|Le doudou est contre le seau, au sec.",
        ),
        2: ln(
            "narrateur|Le livre est sous le banc, au sec.",
            "narrateur|Aniss le tire un peu.",
            "enfant-m|Les pages sont sèches.",
            "maman|On le laisse sous le banc, alors.",
            "papa|Dehors, l'eau est partout.",
            "narrateur|Aniss referme le livre.",
            "narrateur|Il le glisse à sa place.",
            "enfant-m|Le bateau, c'est une feuille.",
            "maman|Oui, une feuille de la cour.",
            "narrateur|Une feuille collée à une dalle attend.",
        ),
        3: ln(
            "narrateur|Les tasses sont sur une planche.",
            "narrateur|Une tasse a déjà un fond d'eau.",
            "enfant-m|La pluie a servi, maman.",
            "maman|Tu verses encore un peu ?",
            "narrateur|Aniss penche le seau.",
            "narrateur|Une goutte tombe dans la tasse.",
            "papa|La dînette reste au jardin ?",
            "enfant-m|Oui, moi je verse.",
            "narrateur|La planche est un peu glissante.",
            "narrateur|Aniss tient le seau à deux mains.",
        ),
    },
    3: {
        1: ln(
            "narrateur|Près du lit, une tour de cubes tient.",
            "narrateur|Aniss passe trop vite.",
            "narrateur|Un cube tombe, tout doux.",
            "enfant-m|Oh.",
            "papa|On la recule, la tour.",
            "narrateur|Aniss pose le seau.",
            "narrateur|Il recule la tour du pied.",
            "maman|Maintenant tu peux passer.",
            "enfant-m|Le seau aussi.",
            "narrateur|L'anse tape un peu le bois.",
            "papa|Doucement, jusqu'à la cour.",
        ),
        2: ln(
            "narrateur|Le livre est sur le lit, ouvert.",
            "narrateur|Un rond de fenêtre touche la page.",
            "enfant-m|La cour est dans le livre aussi.",
            "maman|Une flaque est dessinée, oui.",
            "papa|On referme, pour le garder sec.",
            "narrateur|Aniss referme le livre.",
            "narrateur|Il le pose sur l'oreiller.",
            "enfant-m|Je prends le seau.",
            "maman|Et le doudou.",
            "narrateur|Le doudou est déjà contre lui.",
        ),
        3: ln(
            "narrateur|Deux tasses attendent sur le chevet.",
            "narrateur|Aniss avait servi le doudou.",
            "enfant-m|Il a déjà bu, maman.",
            "maman|Alors on laisse la dînette.",
            "papa|La cour attend, elle.",
            "narrateur|Aniss pose une tasse, tout droit.",
            "narrateur|Le seau est près de la porte.",
            "enfant-m|J'y vais.",
            "maman|Tu as tout contre toi ?",
            "enfant-m|Oui, avec moi.",
        ),
    },
}

T3Q_008 = ln(
    "narrateur|C'est quel moment ?",
    "papa|Le matin, après la sieste, ou le soir.",
)

TIME_008 = {
    1: ln(
        "narrateur|Le soleil est bas, tout pâle.",
        "narrateur|Les flaques dorent un peu.",
        "papa|On sort ce matin ?",
        "enfant-m|Oui, papa.",
    ),
    2: ln(
        "narrateur|La maison est calme, encore tiède.",
        "narrateur|Le store claque, tout doux.",
        "maman|Après la sieste, on y va ?",
        "enfant-m|Oui, maman.",
    ),
    3: ln(
        "narrateur|La lampe fait un rond jaune.",
        "narrateur|Un vélo passe, tout loin.",
        "papa|On sort un peu, ce soir ?",
        "enfant-m|Oui, un peu.",
    ),
}

GO_008 = {
    1: ln(
        "narrateur|Aniss porte le seau vers la porte.",
        "narrateur|Le manteau est sur son bras.",
        "narrateur|Le doudou est contre lui.",
    ),
    2: ln(
        "narrateur|Aniss est déjà dans la cour.",
        "narrateur|L'herbe mouille ses chaussures.",
        "narrateur|Le manteau n'est plus sur le banc.",
    ),
    3: ln(
        "narrateur|Aniss descend vers la cour.",
        "narrateur|Le seau tapote la marche.",
        "narrateur|Le doudou est dans le seau, au sec.",
    ),
}

PLAY_008 = {
    1: ln(
        "narrateur|Il pose un cube au bord de l'eau.",
        "enfant-m|C'est le barrage.",
        "papa|L'eau va tourner autour.",
        "narrateur|Aniss verse un filet brillant.",
    ),
    2: ln(
        "narrateur|Une feuille sert de bateau.",
        "enfant-m|Comme dans le livre.",
        "maman|Le livre reste au sec.",
        "narrateur|La feuille tourne dans la flaque.",
    ),
    3: ln(
        "narrateur|Il verse un peu dans la tasse.",
        "enfant-m|Soupe de pluie.",
        "papa|Elle est froide, hein ?",
        "narrateur|Aniss touche l'eau du doigt.",
    ),
}

IMG_008 = {
    (1, 1, 1): "Le cube jaune sèche au bord de la flaque.",
    (1, 1, 2): "La petite tour reste à l'ombre, près du seau.",
    (1, 1, 3): "Le cube brille encore, sous la lampe.",
    (1, 2, 1): "La feuille-bateau s'arrête contre une dalle.",
    (1, 2, 2): "Le livre reste sur la table, bien sec.",
    (1, 2, 3): "La feuille sombre dans l'eau, tout calme.",
    (1, 3, 1): "La tasse a un fond d'eau claire.",
    (1, 3, 2): "La dînette reste sage, près du buffet.",
    (1, 3, 3): "Une goutte tremble au bord de la tasse.",
    (2, 1, 1): "L'herbe ne tient plus le seau.",
    (2, 1, 2): "Les cubes mouillés restent dans l'herbe.",
    (2, 1, 3): "Le dessous du banc est vide, maintenant.",
    (2, 2, 1): "Les pots du jardin gardent le livre au sec.",
    (2, 2, 2): "La barrière n'a plus le manteau.",
    (2, 2, 3): "L'herbe haute est calme, sans le doudou.",
    (2, 3, 1): "Le cerisier n'a plus le seau à son pied.",
    (2, 3, 2): "Le paillasson du jardin est vide.",
    (2, 3, 3): "La brouette reste, toute seule.",
    (3, 1, 1): "La tour de la chambre tient encore.",
    (3, 1, 2): "Un cube a roulé sous le lit, et reste.",
    (3, 1, 3): "L'oreiller n'a plus le doudou.",
    (3, 2, 1): "Le livre de la chambre est refermé.",
    (3, 2, 2): "La fenêtre de la chambre est un peu floue.",
    (3, 2, 3): "Un signet dépasse encore, tout calme.",
    (3, 3, 1): "Les tasses restent au chevet.",
    (3, 3, 2): "Le lit est défait, tout doux.",
    (3, 3, 3): "Le crochet de la chambre est vide.",
}

CLOSE_008 = {
    1: "Un oiseau boit dans une petite flaque.",
    2: "La cour sent encore la terre mouillée.",
    3: "Les clés tintent dans le bol, au loin.",
}


def l3_008(i: int, j: int, k: int) -> list[str]:
    extra = {
        1: "enfant-m|J'ai le seau, et le manteau.",
        2: "enfant-m|Le manteau n'est plus mouillé, presque.",
        3: "enfant-m|Le seau est avec moi, maintenant.",
    }[i]
    return TIME_008[k] + GO_008[i] + PLAY_008[j] + ln(
        extra,
        "maman|La cour est à toi.",
    )


def fin_008(i: int, j: int, k: int) -> list[str]:
    return ln(
        f"narrateur|{IMG_008[(i, j, k)]}",
        "enfant-m|J'ai le seau.",
        "papa|La cour chante, sous l'eau.",
        "narrateur|Aniss verse encore une goutte.",
        f"narrateur|{CLOSE_008[k]}",
    )


QMAP_008 = {
    "CHK_T0001_P0001_Q0001": {
        "expected_answer": "manteau",
        "accepted_examples": "manteau | le manteau | doudou | la chaise | il revient",
        "retry_prompt": "Le manteau est sur la chaise. Aniss reprend quoi ?",
    },
    "CHK_T0001_P0002_Q0001": {
        "expected_answer": "manteau",
        "accepted_examples": "manteau | le manteau | doudou | le banc | il le prend",
        "retry_prompt": "Le manteau est sur le banc. Aniss reprend quoi ?",
    },
    "CHK_T0001_P0003_Q0001": {
        "expected_answer": "seau",
        "accepted_examples": "seau | le seau | près de la porte | il le prend | la porte",
        "retry_prompt": "Le seau est près de la porte. Il est où ?",
    },
}


# ---------------------------------------------------------------------------
# TREE-AUT-009 — Victorino, sac bleu au crochet (AUT.AFF.001)
# Désir = sortir. Pas une liste. Sangle coincée / doudou au fond. Ils partent.
# ---------------------------------------------------------------------------

DEBUT_009 = ln(
    "narrateur|Un rayon touche la sangle du sac bleu.",
    "narrateur|Le sac penche au crochet, d'un côté.",
    "narrateur|Les dents de la fermeture brillent un peu.",
    "narrateur|Le tapis est doux, rêche au bord.",
    "narrateur|Ça sent le pain, tout chaud.",
    "narrateur|Une cuillère tape un bol, tout près.",
    "maman|Victorino, tu as entendu le bol ?",
    "enfant-m|Oui, maman.",
    "enfant-m|Je veux sortir, maintenant.",
    "papa|On y va.",
    "papa|Le sac est au crochet.",
    "narrateur|En ce moment, Victorino tire le sac.",
    "narrateur|La sangle résiste un peu.",
    "enfant-m|Ça ne vient pas.",
    "maman|Doucement.",
    "narrateur|Le sac tombe dans ses bras.",
    "narrateur|Il est déjà un peu lourd.",
    "papa|On ouvre, pour voir.",
    "narrateur|Victorino ouvre le sac.",
    "narrateur|Au fond, quelque chose de gris.",
    "enfant-m|Mon doudou est déjà là ?",
    "papa|Au fond, oui.",
    "maman|Où vas-tu d'abord, avec le sac ?",
)

T1Q_009 = ln(
    "narrateur|Victorino va où, avec le sac ?",
    "papa|La cuisine, le jardin, ou la chambre.",
)

L1_009 = {
    1: ln(
        "narrateur|Victorino porte le sac vers la cuisine.",
        "narrateur|Le carrelage est frais sous les pieds.",
        "narrateur|Ça sent encore le pain, tout près.",
        "enfant-m|On va chercher le pain, papa ?",
        "papa|Oui, le four du village.",
        "narrateur|La sangle accroche le pied de la chaise.",
        "enfant-m|Ça tient.",
        "maman|Tire tout doucement.",
        "narrateur|Victorino tire.",
        "narrateur|La chaise bouge d'un tout petit cran.",
        "narrateur|La sangle se libère, lisse encore.",
        "enfant-m|Elle est libre.",
        "papa|Le sac vient avec nous.",
        "narrateur|Victorino plonge la main au fond.",
        "narrateur|Le doudou est chaud, tout en bas.",
        "enfant-m|Il était caché.",
        "maman|Au fond, oui.",
        "papa|On part, alors ?",
        "enfant-m|Oui, le pain.",
    ),
    2: ln(
        "narrateur|Victorino pousse la porte du jardin.",
        "narrateur|L'herbe est encore un peu humide.",
        "narrateur|Un oiseau chante une seule fois.",
        "enfant-m|Je veux voir dehors, maman.",
        "maman|Le sac vient, alors.",
        "narrateur|Le crochet du jardin a mouillé la sangle.",
        "enfant-m|Elle est froide.",
        "papa|Elle va sécher, au soleil.",
        "narrateur|Victorino cherche le doudou des yeux.",
        "enfant-m|Il n'est pas sur le banc.",
        "maman|Regarde dans le sac.",
        "narrateur|Il plonge la main, tout au fond.",
        "narrateur|Le tissu gris est là, un peu tassé.",
        "enfant-m|Au fond !",
        "papa|Il t'attendait.",
        "narrateur|Victorino le serre, puis le remet.",
        "enfant-m|On reste un peu ?",
        "maman|Avec le sac, oui.",
    ),
    3: ln(
        "narrateur|Victorino va vers la chambre.",
        "narrateur|Le sac bleu pendait au crochet, là aussi.",
        "narrateur|La couverture est douce sous la main.",
        "enfant-m|On sort, après ?",
        "papa|Oui, vers le village.",
        "narrateur|La sangle a glissé sous le lit.",
        "enfant-m|Elle est partie.",
        "maman|À genoux, tout doux.",
        "narrateur|Victorino se baisse.",
        "narrateur|Il tire la sangle, centimètre par centimètre.",
        "narrateur|Une poussière vole, tout bas.",
        "enfant-m|Je l'ai.",
        "papa|Le sac est à toi, maintenant.",
        "narrateur|Il ouvre encore un peu.",
        "narrateur|Le doudou est au fond, déjà chaud.",
        "enfant-m|Il vient au village.",
        "maman|Dans le sac, oui.",
        "papa|On met tes chaussures, après ?",
        "enfant-m|Oui, papa.",
    ),
}

Q_009 = {
    1: ln(
        "narrateur|La sangle tenait à la chaise.",
        "papa|Victorino a fait quoi ?",
    ),
    2: ln(
        "narrateur|Le doudou n'était pas sur le banc.",
        "maman|Il était où ?",
    ),
    3: ln(
        "narrateur|La sangle était sous le lit.",
        "papa|Victorino a fait quoi ?",
    ),
}

C_009 = {
    1: ln(
        "narrateur|Victorino a tiré, tout doux.",
        "narrateur|La sangle est libre.",
        "enfant-m|Le doudou est au fond.",
        "papa|Merci, Victorino.",
        "maman|Le pain nous attend.",
        "enfant-m|On y va.",
    ),
    2: ln(
        "narrateur|Victorino a cherché au fond du sac.",
        "enfant-m|Il était là.",
        "maman|Au fond, tout chaud.",
        "papa|Le jardin est à nous, maintenant.",
        "narrateur|La sangle sèche un peu au soleil.",
        "enfant-m|On reste.",
    ),
    3: ln(
        "narrateur|Victorino a tiré la sangle.",
        "narrateur|Le sac est dans ses bras.",
        "enfant-m|Le doudou est au fond.",
        "maman|On peut partir.",
        "papa|Les chaussures, puis la porte.",
        "enfant-m|Oui.",
    ),
}

T2Q_009 = ln(
    "narrateur|Près de quoi, Victorino ?",
    "maman|Les cubes, le livre, ou la dînette.",
)

L2_009 = {
    1: {
        1: ln(
            "narrateur|Un cube rouge est sous la chaise.",
            "narrateur|C'est lui qui tenait la sangle.",
            "enfant-m|Le cube, papa.",
            "papa|Pose-le, près des autres.",
            "narrateur|Victorino pose le cube.",
            "narrateur|Les cubes restent dans la cuisine.",
            "maman|Le sac, lui, vient.",
            "enfant-m|Pour le pain.",
            "papa|La sangle est libre, maintenant.",
            "narrateur|Victorino passe la sangle à l'épaule.",
        ),
        2: ln(
            "narrateur|Le petit livre est sur la table.",
            "narrateur|Une miette dort près de la couverture.",
            "enfant-m|Je le prends, pour attendre.",
            "maman|Près du four, oui.",
            "narrateur|Victorino essuie la miette du doigt.",
            "narrateur|Il glisse le livre contre le doudou.",
            "papa|Au fond, il y a de la place.",
            "enfant-m|Il est dedans.",
            "maman|Les pages sont à l'abri ?",
            "enfant-m|Oui, maman.",
        ),
        3: ln(
            "narrateur|Une petite tasse est dans le sac.",
            "narrateur|Elle a glissé, tout seule.",
            "enfant-m|Ce n'est pas pour le pain.",
            "papa|Sors-la, alors.",
            "narrateur|Victorino sort la tasse.",
            "narrateur|Sous la tasse, le doudou apparaît.",
            "maman|Il était dessous.",
            "enfant-m|Au fond.",
            "papa|La tasse reste près du bol.",
            "narrateur|Victorino pose la tasse, tout droit.",
        ),
    },
    2: {
        1: ln(
            "narrateur|Des cubes sont dans un panier, au soleil.",
            "narrateur|Un cube est coincé dans la fermeture.",
            "enfant-m|Ça ferme pas.",
            "maman|Enlève le cube, tout doux.",
            "narrateur|Victorino tire le cube.",
            "narrateur|La fermeture redevient lisse.",
            "papa|Les cubes restent dans le panier.",
            "enfant-m|Le sac vient avec moi.",
            "maman|Le doudou est au fond ?",
            "enfant-m|Oui.",
        ),
        2: ln(
            "narrateur|Le petit livre chauffe un peu au soleil.",
            "narrateur|Une feuille passe, toute légère.",
            "enfant-m|Je le mets, pour le banc.",
            "papa|Au sec, dans le sac.",
            "narrateur|Victorino glisse le livre à côté du doudou.",
            "enfant-m|Il est à l'abri.",
            "maman|Les pages restent sèches ?",
            "enfant-m|Oui, maman.",
            "papa|On s'assoit un moment, après.",
            "narrateur|Le sac bleu sent un peu l'herbe.",
        ),
        3: ln(
            "narrateur|La petite dînette est sur le banc.",
            "narrateur|Une tasse cliquette, tout bas.",
            "enfant-m|Je pose la tasse.",
            "maman|Puis le sac.",
            "narrateur|Victorino pose la tasse.",
            "narrateur|Il ouvre le sac encore un peu.",
            "papa|Le doudou est là ?",
            "enfant-m|Au fond, oui.",
            "maman|La tasse reste au jardin.",
            "narrateur|Le bois de la tasse reste au soleil.",
        ),
    },
    3: {
        1: ln(
            "narrateur|Des cubes sont sur le tapis.",
            "narrateur|Un cube a roulé près de la sangle.",
            "enfant-m|Il voulait venir.",
            "papa|Il reste ici, celui-là.",
            "narrateur|Victorino pose le cube sur le tapis.",
            "narrateur|La sangle n'accroche plus.",
            "maman|Le sac est libre.",
            "enfant-m|On part au village.",
            "papa|Le doudou est au fond.",
            "narrateur|Victorino passe la sangle à l'épaule.",
        ),
        2: ln(
            "narrateur|Le livre est sur l'oreiller.",
            "narrateur|La couverture est encore tiède.",
            "enfant-m|Je le prends, pour le chemin.",
            "maman|Glisse-le, près du doudou.",
            "narrateur|Victorino glisse le livre dans le sac.",
            "narrateur|Le doudou fait un creux, tout doux.",
            "papa|Tu fermes ?",
            "enfant-m|Un peu.",
            "narrateur|La fermeture fait zzz, tout bas.",
            "maman|Le sac est prêt, alors.",
        ),
        3: ln(
            "narrateur|Une tasse attend sur la commode.",
            "narrateur|Victorino l'avait servie, tout à l'heure.",
            "enfant-m|Elle reste, maman.",
            "maman|Oui, la dînette dort ici.",
            "papa|Le village, c'est le sac.",
            "narrateur|Victorino pose la tasse.",
            "narrateur|Il vérifie le fond du sac.",
            "enfant-m|Le doudou est là.",
            "papa|On peut y aller.",
            "narrateur|Le sac tape doucement sa hanche.",
        ),
    },
}

T3Q_009 = ln(
    "narrateur|C'est quel moment ?",
    "papa|Le matin, après la sieste, ou le soir.",
)

TIME_009 = {
    1: ln(
        "narrateur|Le matin, l'air est encore frais.",
        "narrateur|Une tache de soleil touche le sac.",
        "papa|On part ce matin ?",
        "enfant-m|Oui, papa.",
    ),
    2: ln(
        "narrateur|Après la sieste, la maison est calme.",
        "narrateur|Un petit ronron vient de loin.",
        "maman|On sort un peu ?",
        "enfant-m|Oui, maman.",
    ),
    3: ln(
        "narrateur|Le soir, la lampe est déjà allumée.",
        "narrateur|Le sac a une ombre longue.",
        "papa|On sort encore un peu ?",
        "enfant-m|Un peu, oui.",
    ),
}

LEAVE_009 = {
    1: ln(
        "narrateur|Victorino passe la sangle à l'épaule.",
        "narrateur|La porte de la cuisine s'ouvre.",
        "narrateur|L'odeur du pain devient plus forte.",
    ),
    2: ln(
        "narrateur|Victorino marche près de l'herbe.",
        "narrateur|Le sac tape sa hanche, tout doux.",
        "narrateur|Un oiseau reprend une note, puis se tait.",
    ),
    3: ln(
        "narrateur|Victorino enfile une chaussure.",
        "narrateur|L'autre semelle est encore froide.",
        "narrateur|Papa ouvre la porte du village.",
    ),
}

DO_009 = {
    1: ln(
        "enfant-m|Les cubes restent.",
        "papa|Oui, le sac vient.",
        "narrateur|Victorino pousse la fermeture.",
        "narrateur|Ça fait zzz, tout bas.",
    ),
    2: ln(
        "enfant-m|Le livre est à l'abri.",
        "maman|On le sort sur le banc, plus tard.",
        "narrateur|Victorino cale le sac contre lui.",
        "narrateur|Le tissu est un peu rêche.",
    ),
    3: ln(
        "enfant-m|La tasse reste.",
        "papa|Oui, le doudou vient.",
        "narrateur|Victorino pose la main sur le sac.",
        "narrateur|Le creux du fond est plein.",
    ),
}

IMG_009 = {
    (1, 1, 1): "Le cube rouge reste près de la chaise.",
    (1, 1, 2): "Les cubes sont en tas, sages, dans la cuisine.",
    (1, 1, 3): "Le sac bleu se pose près de la porte.",
    (1, 2, 1): "Le sac fait un petit ventre rond, près du pain.",
    (1, 2, 2): "L'eau fait un petit bruit dans le verre.",
    (1, 2, 3): "Le sac attend dans l'ombre douce.",
    (1, 3, 1): "Le bois de la tasse reste au soleil.",
    (1, 3, 2): "Le sac bleu fait un petit tas près du buffet.",
    (1, 3, 3): "Le sac attend près de la porte de la cuisine.",
    (2, 1, 1): "Un oiseau reprend une note, puis se tait.",
    (2, 1, 2): "Le sac bleu sent l'herbe coupée.",
    (2, 1, 3): "Le sac attend sur le banc de l'entrée.",
    (2, 2, 1): "La feuille vole vers l'herbe.",
    (2, 2, 2): "Le sac bleu repose entre papa et Victorino.",
    (2, 2, 3): "Les chaussures font toc toc sur les dalles.",
    (2, 3, 1): "Une abeille passe, tout haut, sans s'arrêter.",
    (2, 3, 2): "Le sac bleu a un goût d'herbe, presque.",
    (2, 3, 3): "La porte du jardin cliquette, tout bas.",
    (3, 1, 1): "Le tapis de la chambre reste plat.",
    (3, 1, 2): "Un cube dort encore sous le lit.",
    (3, 1, 3): "Les chaussures font toc toc, dans l'entrée.",
    (3, 2, 1): "Le sac tape doucement, sur le chemin.",
    (3, 2, 2): "L'oreiller n'a plus le livre.",
    (3, 2, 3): "Le village sent le four, de plus en plus.",
    (3, 3, 1): "La tasse reste sur la commode.",
    (3, 3, 2): "Le sac bleu penche un peu, sur l'épaule.",
    (3, 3, 3): "La porte du village cliquette, tout bas.",
}

CLOSE_009 = {
    1: "L'air sent le pain, de plus en plus.",
    2: "Victorino pose le sac un instant, puis le reprend.",
    3: "Une miette de soleil reste au sol.",
}


def l3_009(i: int, j: int, k: int) -> list[str]:
    extra = {
        1: "enfant-m|On va voir le pain.",
        2: "enfant-m|On reste un peu, dehors.",
        3: "enfant-m|On va au village.",
    }[i]
    return TIME_009[k] + LEAVE_009[i] + DO_009[j] + ln(
        extra,
        "maman|Le sac est avec toi.",
    )


def fin_009(i: int, j: int, k: int) -> list[str]:
    said = {
        1: "papa|Le pain est tout près.",
        2: "maman|L'herbe est encore fraîche.",
        3: "papa|Le village est tout près.",
    }[i]
    return ln(
        f"narrateur|{IMG_009[(i, j, k)]}",
        "enfant-m|On y va.",
        said,
        "narrateur|Le sac bleu tape, tout doux.",
        f"narrateur|{CLOSE_009[k]}",
    )


QMAP_009 = {
    "CHK_T0001_P0001_Q0001": {
        "expected_answer": "tiré",
        "accepted_examples": "tiré | il tire | sangle | la sangle | doucement | le sac",
        "retry_prompt": "La sangle tenait. Il a tiré. Il a fait quoi ?",
    },
    "CHK_T0001_P0002_Q0001": {
        "expected_answer": "au fond",
        "accepted_examples": "au fond | dans le sac | le sac | doudou | il était là",
        "retry_prompt": "Le doudou était au fond du sac. Il était où ?",
    },
    "CHK_T0001_P0003_Q0001": {
        "expected_answer": "tiré",
        "accepted_examples": "tiré | il tire | sangle | sous le lit | le sac",
        "retry_prompt": "La sangle était sous le lit. Il a tiré. Il a fait quoi ?",
    },
}


def main() -> None:
    s008 = assemble(
        DEBUT_008, T1Q_008, L1_008, Q_008, C_008, T2Q_008, L2_008, T3Q_008, l3_008, fin_008
    )
    write_tree(
        "TREE-AUT-008",
        "Aniss veut verser l'eau des flaques dans le seau jaune, dans la cour qui brille. "
        "Il part trop vite. Le manteau, le doudou ou le seau reste. Il revient les prendre. "
        "Puis la cour chante sous le seau.",
        "Le seau jaune d'Aniss",
        "Aniss, papa, maman",
        "cour après la pluie, maison",
        s008,
        QMAP_008,
    )
    relecture(
        "TREE-AUT-008",
        "Le seau jaune d'Aniss",
        "Aniss veut la cour et le seau jaune, après la pluie. "
        "Cuisine : seau sous la table, manteau sur la chaise. "
        "Jardin : manteau qui boit sur le banc. "
        "Chambre : il court, le seau reste près de la porte. "
        "Puis il verse, barrage / feuille-bateau / soupe de pluie.",
        "Hugo→Aniss. AUT.AFF.003 implicite (il revient chercher). "
        "Pas de liste seau-manteau-doudou. Pas « L'histoire est finie ». "
        "3 branches distinctes. Relu P0000 + 3 L1 + 9 L2 + 27 fins. "
        "Questions liées à la scène. Audio non cuit.",
    )

    s009 = assemble(
        DEBUT_009, T1Q_009, L1_009, Q_009, C_009, T2Q_009, L2_009, T3Q_009, l3_009, fin_009
    )
    write_tree(
        "TREE-AUT-009",
        "Victorino veut sortir. Le sac bleu pend au crochet. "
        "La sangle se coince, ou le doudou est déjà au fond. "
        "Il tire, il cherche, il trouve. Ils partent : pain, jardin, ou village.",
        "Le sac bleu de Victorino",
        "Victorino, papa, maman",
        "salon, sac bleu au crochet",
        s009,
        QMAP_009,
    )
    relecture(
        "TREE-AUT-009",
        "Le sac bleu de Victorino",
        "Victorino veut sortir. Pas une liste. "
        "Cuisine : sangle à la chaise, pain du village. "
        "Jardin : doudou au fond, sangle mouillée. "
        "Chambre : sangle sous le lit, village. "
        "Puis ils partent. Cube coincé / livre pour le banc / tasse sortie.",
        "Sami→Victorino. AUT.AFF.001 implicite (sac prêt pour sortir). "
        "Pas « ce que l'adulte a dit ». Pas de packing-list. "
        "3 branches distinctes. Relu P0000 + 3 L1 + 9 L2 + 27 fins. "
        "Audio non cuit.",
    )


if __name__ == "__main__":
    main()
