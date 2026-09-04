#!/usr/bin/env python3
"""TREE-AUT-040 / TREE-AUT-045 — récit implicite, graphe 86, D16, AUT.ROU.001."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

EXTRA_BAD = ("sami", "tom ", "léa", "lea ")


def vet(lim: int, lines: list[str]) -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > lim:
            raise SystemExit(f"{n}>{lim}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        if tok and tok == prev:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces « {tok} »: {ph}")
        else:
            run = 1
        prev = tok
    return out


def write_tree(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict[str, list[str]],
    sons: dict[str, str],
    extras: dict[str, dict],
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    n1 = src.get("age_band") == "N1"
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            scale, rate = 1.28, "slow"
        elif n1:
            scale, rate = 1.22, "slow"
        else:
            scale, rate = 1.22, "medium"
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    joined = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in EXTRA_BAD:
        if bad in joined:
            raise SystemExit(f"{sid} extra interdit: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        if not last_n:
            raise SystemExit(f"{sid} {c['chunk_id']}: fin sans narrateur")
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} {c['chunk_id']} fin mécanique: {last}")
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


N2 = LIMITS["N2"]
N1 = LIMITS["N1"]


# ---------------------------------------------------------------------------
# TREE-AUT-040  N2  Amir  AUT.ROU.001  toile, pompe, lanterne
# Sami→Amir. Séquence vécue (pull puis bottes), pas de refrain d'étapes.
# T3 : la pompe / le poulailler / le pré (plus Tom/Léa/Sami).
# ≠ TREE-AUT-005 (coq, bottes, volet bleu) ≠ TREE-AUT-019 (bidon, lait)
# ---------------------------------------------------------------------------

L1_040 = {
    1: {"lab": "le bac à sable", "ou": "au bac à sable", "quit": "le bac à sable", "son": "poule"},
    2: {"lab": "le toboggan", "ou": "au toboggan", "quit": "le toboggan", "son": "bois"},
    3: {"lab": "les balançoires", "ou": "aux balançoires", "quit": "les balançoires", "son": "vent"},
}
L2_040 = {
    1: {"lab": "le ballon", "obj": "le ballon rouge"},
    2: {"lab": "le seau", "obj": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou"},
}
L3_040 = {
    1: {"lab": "la pompe", "ou": "vers la pompe", "son": "pompe"},
    2: {"lab": "le poulailler", "ou": "vers le poulailler", "son": "poule"},
    3: {"lab": "le pré", "ou": "vers le pré", "son": "vent"},
}

ARRIVE_040 = {
    1: vet(
        N2,
        [
            "narrateur|Amir s'agenouille près du bac.",
            "narrateur|Le sable est pâle, un peu frais.",
            "narrateur|Il glisse entre les doigts.",
            "narrateur|Chh.",
            "narrateur|Une poule passe près du bac.",
            "narrateur|Elle picore un grain, tout sec.",
            "enfant-m|Il est frais, maman.",
            "maman|Oui.",
            "maman|Le sable a dormi dehors.",
            "papa|Tes bottes tiennent bien ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir pose les genoux.",
            "narrateur|Le pull frotte le sable, tout doux.",
            "papa|La pompe attend encore, dans l'ombre.",
            "enfant-m|Après, j'y vais.",
            "narrateur|Un grain reste collé au pouce.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le toboggan est contre la grange.",
            "narrateur|Le métal est encore un peu froid.",
            "narrateur|Les marches font toc sous la main.",
            "enfant-m|Je glisse !",
            "papa|J'attends en bas.",
            "narrateur|Amir glisse.",
            "narrateur|Une paille colle sur la rampe.",
            "maman|Tes bottes ont tenu.",
            "enfant-m|Elles sont chaudes, dedans.",
            "papa|Le pull aussi, sous le vent.",
            "narrateur|Amir reprend son souffle.",
            "narrateur|Ça sent le foin, tout près.",
            "enfant-m|La pompe, après ?",
            "maman|Oui, tout doux.",
            "narrateur|La rampe se tait, un moment.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Les balançoires sont près de la haie.",
            "narrateur|Une corde est un peu rêche.",
            "narrateur|Le siège de bois est lisse, encore humide.",
            "maman|Je pousse tout doux.",
            "enfant-m|Je vois la cour.",
            "papa|La pompe est là-bas, dans l'ombre.",
            "narrateur|Amir avance, puis revient.",
            "narrateur|Le vent lui touche le nez.",
            "enfant-m|Mes bottes tiennent.",
            "maman|Le pull aussi, au col.",
            "papa|Une dernière poussée ?",
            "enfant-m|Encore.",
            "narrateur|La corde fait cling, puis se tait.",
            "narrateur|Une goutte de rosée brille sur la haie.",
        ],
    ),
}

Q_040 = {
    1: vet(
        N2,
        [
            "narrateur|Amir a du sable sur le pull.",
            "papa|Il s'est préparé comment, ce matin ?",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Les bottes ont tenu, sur la rampe.",
            "maman|Amir s'est préparé comment ?",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Le pull tient chaud, près de la haie.",
            "papa|Il s'est préparé comment, Amir ?",
        ],
    ),
}

C_040 = {
    1: vet(
        N2,
        [
            "narrateur|Oui.",
            "narrateur|D'abord le pull, sur la chaise.",
            "narrateur|Ensuite les bottes, près de la porte.",
            "papa|Merci, Amir.",
            "maman|La botte n'est plus tombée.",
            "enfant-m|On continue ?",
            "papa|On prend un jeu, près du bac ?",
            "narrateur|Un grain brille encore sur son pouce.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Oui.",
            "narrateur|D'abord le pull.",
            "narrateur|Ensuite les bottes.",
            "maman|Merci, Amir.",
            "papa|La manche n'est plus à l'envers.",
            "enfant-m|On continue ?",
            "maman|On prend un jeu, près de la rampe ?",
            "narrateur|La paille reste sur le métal.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Oui.",
            "narrateur|Le pull d'abord.",
            "narrateur|Les bottes ensuite.",
            "papa|Merci, Amir.",
            "maman|Tes pieds sont au chaud, maintenant.",
            "enfant-m|On continue ?",
            "papa|On prend un jeu, près de la haie ?",
            "narrateur|La corde ne fait plus cling.",
        ],
    ),
}

PLAY_040 = {
    (1, 1): vet(
        N2,
        [
            "narrateur|Près du bac, le ballon rouge attend.",
            "narrateur|Il est un peu rêche, tout rond.",
            "enfant-m|Le ballon, papa.",
            "papa|D'abord le tenir.",
            "narrateur|Amir pose les deux mains dessus.",
            "narrateur|Le ballon fait toc contre le sable.",
            "maman|Un grain reste collé dessus.",
            "enfant-m|Il vient avec moi.",
            "papa|Oui, tout près.",
            "narrateur|La poule picore encore, tout loin.",
        ],
    ),
    (1, 2): vet(
        N2,
        [
            "narrateur|Près du bac, le seau sonne.",
            "narrateur|L'anse est un peu froide.",
            "enfant-m|Un vrai puits, maman.",
            "maman|Le seau, d'abord.",
            "narrateur|Amir pose le seau près du creux.",
            "narrateur|Du sable pâle rentre au fond.",
            "papa|La pompe a de la vraie eau, plus tard.",
            "enfant-m|Je verse, chh.",
            "maman|Tout doux, oui.",
            "narrateur|Un grain reste sous son ongle.",
        ],
    ),
    (1, 3): vet(
        N2,
        [
            "narrateur|Près du bac, le doudou a du sable.",
            "narrateur|Une oreille est un peu pâle.",
            "enfant-m|Il garde le bac.",
            "papa|D'abord le doudou, contre toi.",
            "narrateur|Amir le serre.",
            "maman|Ensuite on le pose, tout près.",
            "narrateur|Le tissu frotte le pull.",
            "enfant-m|Il est chaud.",
            "papa|Oui.",
            "narrateur|La poule s'éloigne, un pas.",
        ],
    ),
    (2, 1): vet(
        N2,
        [
            "narrateur|Au pied du toboggan, le ballon attend.",
            "narrateur|Il est un peu froid, près de la rampe.",
            "enfant-m|Il glisse aussi ?",
            "papa|D'abord tes mains dessus.",
            "narrateur|Amir le tient.",
            "maman|Ensuite un tout petit bond.",
            "narrateur|Le ballon fait un bond mou.",
            "enfant-m|Mes bottes l'ont vu.",
            "papa|Elles restent au sol.",
            "narrateur|Une paille tourne près des pieds.",
        ],
    ),
    (2, 2): vet(
        N2,
        [
            "narrateur|Au toboggan, le seau sonne contre une marche.",
            "narrateur|L'anse est froide, encore.",
            "enfant-m|C'est sa gare.",
            "maman|D'abord le seau, droit.",
            "narrateur|Amir le pose au pied.",
            "papa|Ensuite on le laisse, un moment.",
            "narrateur|Le seau fait toc, tout creux.",
            "enfant-m|Il attend la pompe.",
            "maman|La rampe sèche au soleil.",
            "narrateur|Une goutte glisse encore, tout lente.",
        ],
    ),
    (2, 3): vet(
        N2,
        [
            "narrateur|Au toboggan, le doudou a vu la rampe.",
            "narrateur|L'oreille grise est un peu froide.",
            "enfant-m|Il a glissé des yeux.",
            "papa|D'abord le doudou, dans tes bras.",
            "narrateur|Amir le serre.",
            "maman|Ensuite contre le pull, au chaud.",
            "narrateur|Le tissu frotte le col.",
            "enfant-m|Ils sont ensemble.",
            "papa|Oui.",
            "narrateur|Le métal se tait, tout doux.",
        ],
    ),
    (3, 1): vet(
        N2,
        [
            "narrateur|Près des chaînes, le ballon a de l'herbe.",
            "narrateur|Un brin colle au cuir.",
            "enfant-m|On roule tout près.",
            "maman|D'abord le tenir.",
            "narrateur|Amir pose le ballon au sol.",
            "papa|Ensuite un tout petit coup.",
            "narrateur|Le ballon avance, puis s'arrête.",
            "enfant-m|Mes bottes n'ont pas bougé.",
            "maman|Elles tiennent, dans l'herbe.",
            "narrateur|La corde fait un cling lointain.",
        ],
    ),
    (3, 2): vet(
        N2,
        [
            "narrateur|Près des balançoires, le seau est dans l'herbe.",
            "narrateur|L'anse est froide, près de la corde.",
            "enfant-m|Il va à la pompe.",
            "papa|D'abord le seau, droit.",
            "narrateur|Amir le pose sous le siège.",
            "maman|Ensuite on le reprend, plus tard.",
            "narrateur|L'herbe mouille le bord, un peu.",
            "enfant-m|Il est à l'abri.",
            "papa|Oui.",
            "narrateur|Une flaque tremble près du pied.",
        ],
    ),
    (3, 3): vet(
        N2,
        [
            "narrateur|Près des balançoires, le doudou a du vent.",
            "narrateur|L'oreille molle clignote.",
            "enfant-m|Il s'assoit avec moi.",
            "maman|D'abord le doudou, sur tes genoux.",
            "narrateur|Amir l'installe.",
            "papa|Ensuite contre le pull.",
            "narrateur|Le tissu gris ne tombe pas.",
            "enfant-m|Il voyage encore.",
            "maman|Une dernière poussée, tout douce.",
            "narrateur|La corde se tait.",
        ],
    ),
}

STEP_040 = {
    1: vet(
        N2,
        [
            "narrateur|Ils vont vers la pompe de la cour.",
            "narrateur|La poignée est rêche, encore froide.",
            "enfant-m|Je pousse ?",
            "papa|D'abord tes deux mains.",
            "narrateur|Amir tient la poignée.",
            "narrateur|L'eau fait glou, tout froid.",
            "enfant-m|Ça coule !",
            "maman|Ensuite on s'arrête, tout doux.",
            "papa|Merci, Amir.",
            "narrateur|Une goutte brille sur sa manche.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Ils marchent vers le poulailler.",
            "narrateur|La porte de bois sent le foin.",
            "enfant-m|Un grain, pour elle ?",
            "maman|D'abord le grain, dans ta main.",
            "narrateur|Amir pose un grain près du seuil.",
            "narrateur|Une poule picore.",
            "narrateur|Toc toc, le bec.",
            "enfant-m|Elle mange.",
            "papa|Ensuite on recule, un pas.",
            "narrateur|Une paille colle à sa botte.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Ils vont vers le pré.",
            "narrateur|La clôture est un peu humide.",
            "enfant-m|C'est grand.",
            "papa|D'abord les mains sur le bois.",
            "narrateur|Amir pose les mains sur la clôture.",
            "narrateur|L'herbe haute brille, encore mouillée.",
            "maman|Ensuite on reste de ce côté.",
            "enfant-m|Ça sent l'herbe.",
            "papa|Oui.",
            "narrateur|Une goutte glisse le long d'un brin.",
        ],
    ),
}

IMG_040 = {
    (1, 1, 1): "Une goutte de la pompe brille sur le ballon.",
    (1, 1, 2): "Un grain de sable reste sur le ballon rouge.",
    (1, 1, 3): "Le ballon a une herbe collée dessus.",
    (1, 2, 1): "L'eau de la pompe sonne dans le seau.",
    (1, 2, 2): "Un grain de sable reste au fond du seau.",
    (1, 2, 3): "L'anse du seau a un brin d'herbe.",
    (1, 3, 1): "L'oreille du doudou a une goutte.",
    (1, 3, 2): "Un grain de sable reste sur le doudou.",
    (1, 3, 3): "Le doudou a senti l'herbe mouillée.",
    (2, 1, 1): "Le ballon a une goutte de la pompe.",
    (2, 1, 2): "Une paille de la rampe colle au ballon.",
    (2, 1, 3): "Le ballon a vu le pré, tout rouge.",
    (2, 2, 1): "Le seau sonne sous l'eau froide.",
    (2, 2, 2): "L'anse cliquette près du poulailler.",
    (2, 2, 3): "Une goutte de rampe brille dans le seau.",
    (2, 3, 1): "Le doudou a une goutte au bout de l'oreille.",
    (2, 3, 2): "Une paille reste sur le doudou gris.",
    (2, 3, 3): "Le doudou a senti le vent du pré.",
    (3, 1, 1): "Le ballon frotte la poignée rêche.",
    (3, 1, 2): "Un bout de paille colle au ballon.",
    (3, 1, 3): "Le ballon a de l'herbe, près de la clôture.",
    (3, 2, 1): "L'anse froide a pris une goutte.",
    (3, 2, 2): "Le seau pose son ombre près des poules.",
    (3, 2, 3): "L'herbe mouille le bord du seau.",
    (3, 3, 1): "Le doudou a senti l'eau de la pompe.",
    (3, 3, 2): "L'oreille grise a un peu de paille.",
    (3, 3, 3): "Le doudou a l'odeur de l'herbe haute.",
}

FIN_040 = {
    (1, 1, 1): "La toile brille encore, entre les lattes.",
    (1, 1, 2): "Le bol bleu attend, tout calme.",
    (1, 1, 3): "La lanterne ne fume plus.",
    (1, 2, 1): "Une goutte sèche sur la poignée rêche.",
    (1, 2, 2): "Le seau repose près du seuil.",
    (1, 2, 3): "Une paille colle encore au bois.",
    (1, 3, 1): "Le doudou sèche près du bol bleu.",
    (1, 3, 2): "Le lait n'a plus de rond blanc.",
    (1, 3, 3): "La botte penche encore, tout doux.",
    (2, 1, 1): "Le ballon s'endort près des bottes.",
    (2, 1, 2): "La rampe de la grange reste loin.",
    (2, 1, 3): "Une paille sèche près des clés.",
    (2, 2, 1): "Le seau penche un peu, sous le crochet.",
    (2, 2, 2): "Le foin ne sent plus, dans la cuisine.",
    (2, 2, 3): "La pompe est retournée dans l'ombre.",
    (2, 3, 1): "L'oreille du doudou dépasse du fauteuil.",
    (2, 3, 2): "Le pull sèche sur la chaise.",
    (2, 3, 3): "La lanterne est froide, tout à fait.",
    (3, 1, 1): "Le ballon a cessé de rouler, au seuil.",
    (3, 1, 2): "Une goutte de la toile ne brille plus.",
    (3, 1, 3): "Le crochet de la botte fait un petit toc.",
    (3, 2, 1): "Le seau pose son ombre sur le carrelage.",
    (3, 2, 2): "Le poulailler reste loin, fermé.",
    (3, 2, 3): "Ça sent encore le foin, tout bas.",
    (3, 3, 1): "Le doudou a l'odeur de l'herbe, au salon.",
    (3, 3, 2): "Les deux bottes se touchent, près de la porte.",
    (3, 3, 3): "La toile ne tremble plus.",
}


def body_040(i: int, j: int, k: int) -> list[str]:
    loc = L1_040[i]
    jeu = L2_040[j]
    lines = [
        f"narrateur|Amir quitte {loc['quit']}.",
        f"narrateur|Il a {jeu['obj']} avec lui.",
        "narrateur|Les bottes font toc, dans la cour.",
    ]
    lines.extend(STEP_040[k])
    lines.append(f"narrateur|{IMG_040[(i, j, k)]}")
    return vet(N2, lines)


def fin_040(i: int, j: int, k: int) -> list[str]:
    loc = L1_040[i]
    jeu = L2_040[j]
    dest = L3_040[k]
    return vet(
        N2,
        [
            f"narrateur|{IMG_040[(i, j, k)]}",
            f"narrateur|Amir a joué {loc['ou']}.",
            f"narrateur|Il a pris {jeu['lab']}.",
            f"narrateur|Puis {dest['lab']}.",
            "narrateur|Ils rentrent.",
            "enfant-m|La pompe s'est tue.",
            "maman|Oui.",
            "papa|Merci, Amir.",
            "narrateur|Le bol bleu attend sur la table.",
            f"narrateur|{FIN_040[(i, j, k)]}",
        ],
    )


def build_040() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = vet(
        N2,
        [
            "narrateur|Une toile d'araignée tient entre deux lattes.",
            "narrateur|Des gouttes d'eau y brillent, toutes petites.",
            "narrateur|La pompe de la cour est encore dans l'ombre.",
            "narrateur|Sa poignée est froide, un peu rêche.",
            "narrateur|Une lanterne fume tout bas, près du mur.",
            "narrateur|Ça sent le foin et le bois mouillé.",
            "narrateur|Une paille colle au seuil de la cuisine.",
            "narrateur|Le bol bleu d'Amir attend sur la table.",
            "narrateur|Le lait y fait un rond blanc.",
            "narrateur|Les bottes d'Amir sont près de la porte.",
            "narrateur|Une botte penche, comme fatiguée.",
            "maman|Amir, tu as vu les gouttes ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Elles brillent.",
            "papa|La pompe est encore dans l'ombre.",
            "narrateur|En ce moment, Amir frotte ses yeux.",
            "narrateur|Il a le doudou contre la joue.",
            "enfant-m|Je veux aller dehors !",
            "enfant-m|Je veux la pompe !",
            "maman|D'accord.",
            "narrateur|Amir prend le pull sur la chaise.",
            "narrateur|Il attrape aussi une botte.",
            "narrateur|La botte tombe, toc.",
            "enfant-m|Oh.",
            "papa|Le pull, d'abord, tout doux.",
            "narrateur|Amir pose la botte.",
            "narrateur|Une manche du pull est à l'envers.",
            "maman|On tourne le tissu.",
            "narrateur|Amir glisse un bras, puis l'autre.",
            "enfant-m|Il est chaud.",
            "papa|Les bottes, ensuite.",
            "narrateur|Amir enfile la botte gauche.",
            "narrateur|Puis la botte droite.",
            "enfant-m|On y va ?",
            "maman|Oui.",
            "narrateur|La lanterne fume encore, tout bas.",
        ],
    )
    sons["CHK_T0000_P0000"] = "pompe,lanterne"
    s["CHK_T0001_P0000"] = vet(
        N2,
        [
            "narrateur|Ils arrivent dans la cour.",
            "papa|Le bac à sable, le toboggan, ou les balançoires ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("le bac à sable", "le toboggan", "les balançoires")
    sons["CHK_T0001_P0000"] = "cour"
    qfields = qf(
        "une chose",
        "une chose | puis l'autre | d'abord | ensuite | le pull | les bottes | une chose puis l'autre | puis la suivante",
        "Il a mis le pull, puis les bottes. Comment s'est préparé Amir ?",
    )
    for i, loc in L1_040.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_040[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_040[i]
        extras[f"{p}_Q0001"] = qfields
        s[f"{p}_C0001"] = C_040[i]
        s[f"{p}_T0002_P0000"] = vet(
            N2,
            [
                f"narrateur|Amir peut encore jouer, {loc['ou']}.",
                "maman|Le ballon, le seau, ou le doudou ?",
                "papa|On prend un jeu.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_040[(i, j)]
            sons[p2] = loc["son"]
            s[f"{p2}_T0003_P0000"] = vet(
                N2,
                [
                    f"narrateur|La cour peut encore avancer, {loc['ou']}.",
                    "maman|La pompe, le poulailler, ou le pré ?",
                    "papa|On va vers la suivante.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("la pompe", "le poulailler", "le pré")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_040(i, j, k)
                sons[p3] = L3_040[k]["son"]
                s[f"{p3}_F0001"] = fin_040(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-045  N1  Nina  AUT.ROU.001  panier d'osier, marché
# Nina déjà D16. N1 ≤10. Séquence vécue (lever, pull, panier).
# T3 : le rouge / le bleu / le vert.
# ≠ TREE-AUT-027 (manteau bleu, bâche, oranges, menthe)
# ---------------------------------------------------------------------------

L1_045 = {
    1: {"lab": "une pomme", "ou": "près des pommes", "son": "marche"},
    2: {"lab": "un yaourt", "ou": "près des yaourts", "son": "marche"},
    3: {"lab": "un morceau de pain", "ou": "près du pain", "son": "pain"},
}
L2_045 = {
    1: {"lab": "le ballon", "obj": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou"},
}
L3_045 = {
    1: {"lab": "le rouge", "ou": "vers le rouge", "quoi": "la nappe rouge"},
    2: {"lab": "le bleu", "ou": "vers le bleu", "quoi": "le torchon bleu"},
    3: {"lab": "le vert", "ou": "vers le vert", "quoi": "le tablier vert"},
}

ARRIVE_045 = {
    1: vet(
        N1,
        [
            "narrateur|Nina va vers une pomme.",
            "narrateur|Un reflet vert brille dessus.",
            "narrateur|Elle est lisse et froide.",
            "maman|Tu prends la pomme ?",
            "enfant-f|La pomme.",
            "narrateur|Nina la pose dans le panier.",
            "narrateur|La pomme fait un petit choc.",
            "papa|L'osier la tient.",
            "enfant-f|Elle est froide.",
            "maman|Tes mains aussi, un peu.",
            "papa|Le pull te tient chaud.",
            "enfant-f|Oui, papa.",
            "narrateur|Nina tient le panier.",
            "narrateur|L'osier gratte un peu.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Nina va vers un yaourt.",
            "narrateur|Le pot blanc est un peu frais.",
            "narrateur|Le couvercle est lisse.",
            "papa|Tu prends le yaourt ?",
            "enfant-f|Le yaourt.",
            "narrateur|Nina le glisse au panier.",
            "narrateur|Le pot fait un petit toc.",
            "maman|Il reste droit.",
            "enfant-f|Il est froid.",
            "papa|Le pain est plus loin.",
            "enfant-f|Après, maman.",
            "maman|Oui.",
            "narrateur|Nina serre l'osier.",
            "narrateur|Ça sent encore le lait.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Nina va vers le pain.",
            "narrateur|La croûte est encore chaude.",
            "narrateur|Ça sent le four.",
            "maman|Un morceau, pour nous ?",
            "enfant-f|Le pain.",
            "narrateur|Nina le pose au panier.",
            "narrateur|Le pain fait un petit frou.",
            "papa|Il chauffe l'osier.",
            "enfant-f|Il est chaud.",
            "maman|Le pull aussi, au col.",
            "papa|Tu l'as mis, ce matin.",
            "enfant-f|Oui, d'abord.",
            "narrateur|Une miette tombe.",
            "narrateur|Un pigeon la picore.",
        ],
    ),
}

Q_045 = {
    1: vet(
        N1,
        [
            "narrateur|La pomme est dans le panier.",
            "maman|Nina s'est préparée comment ?",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Le yaourt est dans le panier.",
            "papa|Nina s'est préparée comment ?",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Le pain est dans le panier.",
            "maman|Nina s'est préparée comment ?",
        ],
    ),
}

C_045 = {
    1: vet(
        N1,
        [
            "narrateur|D'abord le pull.",
            "narrateur|Ensuite le panier.",
            "papa|Merci, Nina.",
            "maman|Le panier n'a plus penché.",
            "enfant-f|On continue ?",
            "papa|Oui.",
            "narrateur|La pomme reste au fond.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|D'abord le pull.",
            "narrateur|Ensuite le panier, au clou.",
            "maman|Merci, Nina.",
            "papa|Tes pieds ont quitté le tapis.",
            "enfant-f|On continue ?",
            "maman|Oui.",
            "narrateur|Le pot blanc reste droit.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Le pull, d'abord.",
            "narrateur|Le panier, ensuite.",
            "papa|Merci, Nina.",
            "maman|Le volet a claqué, tout à l'heure.",
            "enfant-f|On continue ?",
            "papa|Oui.",
            "narrateur|Une miette reste au pavé.",
        ],
    ),
}

PLAY_045 = {
    (1, 1): vet(
        N1,
        [
            "narrateur|Près des pommes, un ballon attend.",
            "narrateur|Il a des points jaunes.",
            "enfant-f|Le ballon.",
            "papa|D'accord.",
            "narrateur|Nina le tient contre le panier.",
            "narrateur|Le ballon fait un petit poum.",
            "maman|La pomme est déjà dedans.",
            "enfant-f|Ils se touchent.",
            "papa|Tout doux.",
            "narrateur|Ça sent encore le pain.",
        ],
    ),
    (1, 2): vet(
        N1,
        [
            "narrateur|Près des pommes, un seau est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau.",
            "maman|D'accord.",
            "narrateur|Nina le pose près du panier.",
            "narrateur|Le seau fait toc.",
            "papa|La pomme reste au fond.",
            "enfant-f|Le seau attend.",
            "maman|Oui.",
            "narrateur|Un reflet vert passe dessus.",
        ],
    ),
    (1, 3): vet(
        N1,
        [
            "narrateur|Près des pommes, le doudou est là.",
            "narrateur|Le tissu sent le savon.",
            "enfant-f|Le doudou.",
            "papa|D'accord.",
            "narrateur|Nina le serre.",
            "narrateur|Puis elle le pose au panier.",
            "maman|À côté de la pomme.",
            "enfant-f|Il est au chaud.",
            "papa|Oui.",
            "narrateur|L'oreille touche l'osier.",
        ],
    ),
    (2, 1): vet(
        N1,
        [
            "narrateur|Près des yaourts, un ballon attend.",
            "narrateur|Il a des points jaunes.",
            "enfant-f|Le ballon.",
            "maman|D'accord.",
            "narrateur|Nina le tient à deux mains.",
            "narrateur|Le ballon fait poum, tout mou.",
            "papa|Le yaourt reste droit.",
            "enfant-f|Je le vois.",
            "maman|Dans le panier.",
            "narrateur|Le pot blanc est calme.",
        ],
    ),
    (2, 2): vet(
        N1,
        [
            "narrateur|Près des yaourts, un seau est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau.",
            "papa|D'accord.",
            "narrateur|Nina tient l'anse.",
            "narrateur|Le seau racle un peu, toc.",
            "maman|Le yaourt est déjà au panier.",
            "enfant-f|Le seau aussi ?",
            "papa|Près de nous.",
            "narrateur|Ça sent encore le lait.",
        ],
    ),
    (2, 3): vet(
        N1,
        [
            "narrateur|Près des yaourts, le doudou est là.",
            "narrateur|Le tissu est doux, un peu frais.",
            "enfant-f|Le doudou.",
            "maman|D'accord.",
            "narrateur|Nina le serre contre elle.",
            "narrateur|Le doudou sent le savon.",
            "papa|Le yaourt reste au panier.",
            "enfant-f|Ils voyagent.",
            "maman|Oui.",
            "narrateur|L'oreille touche le pull bleu.",
        ],
    ),
    (3, 1): vet(
        N1,
        [
            "narrateur|Près du pain, un ballon attend.",
            "narrateur|Il a des points jaunes.",
            "enfant-f|Le ballon.",
            "papa|D'accord.",
            "narrateur|Nina le tient contre le panier.",
            "narrateur|Le ballon fait poum.",
            "maman|Le pain chauffe encore.",
            "enfant-f|Il est chaud.",
            "papa|Le ballon, lui, est frais.",
            "narrateur|Une miette colle au cuir.",
        ],
    ),
    (3, 2): vet(
        N1,
        [
            "narrateur|Près du pain, un seau est là.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau.",
            "maman|D'accord.",
            "narrateur|Nina pose le seau droit.",
            "narrateur|Le seau tapote le pavé, toc.",
            "papa|Le pain est déjà au panier.",
            "enfant-f|Le seau attend.",
            "maman|Oui.",
            "narrateur|Une miette roule près de l'anse.",
        ],
    ),
    (3, 3): vet(
        N1,
        [
            "narrateur|Près du pain, le doudou est là.",
            "narrateur|Le tissu est doux, un peu tiède.",
            "enfant-f|Le doudou.",
            "papa|D'accord.",
            "narrateur|Nina le serre.",
            "narrateur|Puis elle le pose au panier.",
            "maman|Près du pain chaud.",
            "enfant-f|Il sent le four.",
            "papa|Un peu, oui.",
            "narrateur|L'oreille a une miette.",
        ],
    ),
}

COLOR_045 = {
    1: vet(
        N1,
        [
            "narrateur|Nina rejoint la nappe rouge.",
            "narrateur|Les fraises sont rouges aussi.",
            "narrateur|Le tissu rouge est un peu rêche.",
            "maman|Tu vois le rouge ?",
            "enfant-f|Le rouge.",
            "narrateur|Nina pose la main.",
            "narrateur|La nappe claque une fois.",
            "papa|Une miette roule sous l'étal.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Nina rejoint le torchon bleu.",
            "narrateur|Le ciel est un peu bleu.",
            "narrateur|Le torchon bleu est encore humide.",
            "maman|Tu vois le bleu ?",
            "enfant-f|Le bleu.",
            "narrateur|Nina touche le tissu.",
            "narrateur|Le torchon claque tout doux.",
            "papa|Un pigeon s'envole d'un coup.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Nina rejoint le tablier vert.",
            "narrateur|Les choux sont verts, tout ronds.",
            "narrateur|Le tablier vert est un peu rêche.",
            "maman|Tu vois le vert ?",
            "enfant-f|Le vert.",
            "narrateur|Nina regarde le tablier.",
            "narrateur|Une feuille de chou froisse.",
            "papa|Une cloche de vélo sonne une fois.",
        ],
    ),
}

IMG_045 = {
    (1, 1, 1): "Une fraise a touché le ballon.",
    (1, 1, 2): "Le ballon a pris un peu de bleu.",
    (1, 1, 3): "Un point jaune touche une feuille.",
    (1, 2, 1): "L'anse du seau a une tache rouge.",
    (1, 2, 2): "Une goutte bleue brille sur l'anse.",
    (1, 2, 3): "Une feuille de chou touche le seau.",
    (1, 3, 1): "L'oreille du doudou a du rouge.",
    (1, 3, 2): "Le doudou a senti le torchon humide.",
    (1, 3, 3): "Une feuille verte reste au doudou.",
    (2, 1, 1): "Le ballon frotte la nappe rouge.",
    (2, 1, 2): "Un point jaune a vu le ciel.",
    (2, 1, 3): "Le ballon a touché le tablier.",
    (2, 2, 1): "Le seau pose son ombre au rouge.",
    (2, 2, 2): "L'anse froide a pris le bleu.",
    (2, 2, 3): "Le seau tapote près des choux.",
    (2, 3, 1): "Le doudou a senti les fraises.",
    (2, 3, 2): "L'oreille molle a du bleu.",
    (2, 3, 3): "Le doudou a l'odeur du chou.",
    (3, 1, 1): "Une miette de pain reste au rouge.",
    (3, 1, 2): "Le pain a vu le torchon bleu.",
    (3, 1, 3): "Une miette colle au tablier vert.",
    (3, 2, 1): "Le seau a une miette, au rouge.",
    (3, 2, 2): "L'anse a pris une goutte bleue.",
    (3, 2, 3): "Une feuille tombe près du seau.",
    (3, 3, 1): "Le doudou a une miette rouge.",
    (3, 3, 2): "L'oreille a senti le torchon.",
    (3, 3, 3): "Le doudou a une feuille verte.",
}

FIN_045 = {
    (1, 1, 1): "La pomme reste au fond du panier.",
    (1, 1, 2): "Le ballon sèche près de la porte.",
    (1, 1, 3): "Une feuille verte reste au seuil.",
    (1, 2, 1): "L'anse du seau est tiède, maintenant.",
    (1, 2, 2): "Le torchon bleu reprend le clou.",
    (1, 2, 3): "Le seau pose son ombre au tapis.",
    (1, 3, 1): "Le doudou s'endort près de la pomme.",
    (1, 3, 2): "L'osier sent encore le savon.",
    (1, 3, 3): "Une feuille de chou sèche au panier.",
    (2, 1, 1): "Le pot blanc reste droit, au panier.",
    (2, 1, 2): "Le ballon a cessé de faire poum.",
    (2, 1, 3): "Le tablier vert reste loin, maintenant.",
    (2, 2, 1): "Le seau repose près du yaourt.",
    (2, 2, 2): "Le ciel n'est plus dans le torchon.",
    (2, 2, 3): "L'anse ne cliquette plus.",
    (2, 3, 1): "Le doudou a l'odeur du lait, un peu.",
    (2, 3, 2): "L'oreille grise dépasse du panier.",
    (2, 3, 3): "Le pull bleu reprend la chaise.",
    (3, 1, 1): "Une miette de pain reste au panier.",
    (3, 1, 2): "Le pain n'est plus chaud, tout à fait.",
    (3, 1, 3): "Le volet du boulanger s'est tu.",
    (3, 2, 1): "Le seau a une miette, au fond.",
    (3, 2, 2): "Les pavés n'ont plus de goutte rouge.",
    (3, 2, 3): "Le seau sèche près de la porte.",
    (3, 3, 1): "Le doudou a une miette, à l'oreille.",
    (3, 3, 2): "Le pain sent encore, tout bas.",
    (3, 3, 3): "Le panier d'osier repose au clou.",
}


def body_045(i: int, j: int, k: int) -> list[str]:
    jeu = L2_045[j]
    lines = list(COLOR_045[k])
    lines.append(f"narrateur|Nina a encore {jeu['lab']}.")
    lines.append("enfant-f|J'ai fini, maman.")
    lines.append("maman|On rentre.")
    lines.append("papa|Le panier vient avec nous.")
    lines.append("narrateur|Les pavés sont encore mouillés.")
    lines.append(f"narrateur|{IMG_045[(i, j, k)]}")
    return vet(N1, lines)


def fin_045(i: int, j: int, k: int) -> list[str]:
    loc = L1_045[i]
    jeu = L2_045[j]
    col = L3_045[k]
    return vet(
        N1,
        [
            f"narrateur|{IMG_045[(i, j, k)]}",
            f"narrateur|Nina a choisi {loc['lab']}.",
            f"narrateur|Puis {jeu['lab']}.",
            f"narrateur|Puis {col['lab']}.",
            "narrateur|Ils rentrent.",
            "narrateur|La maison sent le pain.",
            "enfant-f|Le panier est là.",
            "maman|Oui.",
            "papa|Merci, Nina.",
            "narrateur|Nina pose le panier près de la porte.",
            f"narrateur|{FIN_045[(i, j, k)]}",
        ],
    )


def build_045() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = vet(
        N1,
        [
            "narrateur|Une goutte rouge tombe sur les pavés.",
            "narrateur|Elle vient de la caisse de fraises.",
            "narrateur|Les pavés sont encore mouillés.",
            "narrateur|Ça sent le pain chaud.",
            "narrateur|Le volet du boulanger claque une fois.",
            "narrateur|Deux pigeons picorent une miette.",
            "narrateur|Le panier d'osier pend au clou.",
            "narrateur|L'osier est un peu rêche.",
            "narrateur|Papa noue son foulard gris.",
            "narrateur|Maman plie un torchon à carreaux.",
            "maman|Nina, tu entends le marché ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Ça sent le pain.",
            "papa|Le panier t'attend, au clou.",
            "narrateur|En ce moment, Nina est sous la couverture.",
            "narrateur|La couverture a des petits pois.",
            "narrateur|Elle sent le savon.",
            "enfant-f|Je veux le marché !",
            "enfant-f|Avec le panier.",
            "narrateur|Nina tend le bras, encore couchée.",
            "narrateur|Le panier penche, tout seul.",
            "narrateur|L'osier gratte le mur.",
            "enfant-f|Oh.",
            "maman|On se lève, d'abord.",
            "narrateur|Nina pousse la couverture.",
            "narrateur|Ses pieds touchent le tapis.",
            "narrateur|Le tapis est un peu froid.",
            "papa|Le pull, ensuite.",
            "narrateur|Le pull bleu attend sur la chaise.",
            "narrateur|Nina met le pull.",
            "enfant-f|Il est chaud.",
            "maman|Le panier, maintenant.",
            "narrateur|Nina prend le panier au clou.",
            "narrateur|L'osier gratte un peu.",
            "papa|On y va ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une miette reste sur les pavés.",
        ],
    )
    sons["CHK_T0000_P0000"] = "marche,pain"
    s["CHK_T0001_P0000"] = vet(
        N1,
        [
            "maman|Au marché, on prend quoi d'abord ?",
            "narrateur|Une pomme.",
            "narrateur|Un yaourt.",
            "narrateur|Ou un morceau de pain.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("une pomme", "un yaourt", "un morceau de pain")
    sons["CHK_T0001_P0000"] = "marche"
    qfields = qf(
        "une chose",
        "une chose | puis l'autre | d'abord | ensuite | le pull | le panier | une chose puis l'autre | puis la suivante",
        "Elle a mis le pull, puis le panier. Comment ?",
    )
    for i, loc in L1_045.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_045[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_045[i]
        extras[f"{p}_Q0001"] = qfields
        s[f"{p}_C0001"] = C_045[i]
        s[f"{p}_T0002_P0000"] = vet(
            N1,
            [
                f"papa|Nina prend un jeu, {loc['ou']}.",
                "papa|Le ballon, le seau, ou le doudou ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_045[(i, j)]
            sons[p2] = loc["son"]
            s[f"{p2}_T0003_P0000"] = vet(
                N1,
                [
                    "maman|On va vers quelle couleur ?",
                    "narrateur|Le rouge.",
                    "narrateur|Le bleu.",
                    "narrateur|Ou le vert.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le rouge", "le bleu", "le vert")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_045(i, j, k)
                sons[p3] = "marche"
                s[f"{p3}_F0001"] = fin_045(i, j, k)
    return s, sons, extras


def main() -> None:
    s40, n40, e40 = build_040()
    write_tree(
        "TREE-AUT-040",
        "Amir veut la pompe de la cour. La toile brille entre les lattes. "
        "Il prend le pull et une botte ensemble : la botte tombe, une manche "
        "est à l'envers. Le pull d'abord, les bottes ensuite. Ils jouent, "
        "puis la pompe, le poulailler ou le pré. La lanterne s'est tue.",
        "La toile et la pompe d'Amir",
        "Amir, papa, maman",
        "ferme, cour, toile d'araignée, pompe, lanterne",
        s40,
        n40,
        e40,
    )
    relecture(
        "TREE-AUT-040",
        "La toile et la pompe d'Amir",
        "Amir veut la pompe. Toile, gouttes, lanterne, foin, bol bleu. "
        "Pull et botte ensemble : la botte tombe. Séquence vécue. "
        "Bac / toboggan / balançoires, puis ballon / seau / doudou, "
        "puis pompe / poulailler / pré.",
        "Sami→Amir (D16). N2. AUT.ROU.001 implicite, pas de refrain d'étapes. "
        "Monde ≠ TREE-AUT-005 (coq, volet bleu) ≠ TREE-AUT-019 (bidon). "
        "T3 = pompe/poulailler/pré (plus Tom/Léa/Sami). Fin = toile, pas "
        "« L'histoire est finie ».",
    )

    s45, n45, e45 = build_045()
    write_tree(
        "TREE-AUT-045",
        "Nina veut le marché avec le panier d'osier. Une goutte de fraise "
        "tombe sur les pavés. Encore sous la couverture, elle tire le panier : "
        "il penche. Se lever, le pull, puis le panier. Pomme, yaourt ou pain, "
        "puis un jeu, puis le rouge, le bleu ou le vert. Le panier retrouve le clou.",
        "Le panier d'osier de Nina au marché",
        "Nina, papa, maman",
        "maison puis marché, pavés, fraises, volet du boulanger, panier au clou",
        s45,
        n45,
        e45,
    )
    relecture(
        "TREE-AUT-045",
        "Le panier d'osier de Nina au marché",
        "Nina veut le marché. Goutte de fraise, volet, pigeons, panier au clou. "
        "Encore couchée, le panier penche. Séquence vécue. "
        "Pomme / yaourt / pain, puis ballon / seau / doudou, "
        "puis rouge / bleu / vert.",
        "Nina déjà D16. N1 ≤10. AUT.ROU.001 implicite. "
        "Monde ≠ TREE-AUT-027 (manteau bleu, bâche, oranges). "
        "T3 = le rouge/le bleu/le vert. Fin = panier près de la porte, "
        "pas « L'histoire est finie ».",
    )


if __name__ == "__main__":
    main()
