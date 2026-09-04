#!/usr/bin/env python3
"""TREE-COL-003 / TREE-COL-004 — récit implicite, graphe 86, D16."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402


def vet(lim: int, lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > lim:
            raise SystemExit(f"{n}>{lim}: {ph}")
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
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind == "passage_question":
            scale, rate = 1.28, "slow"
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
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in ("jules", "tom ", "léa", "sami", "sara "):
        if bad in blob:
            raise SystemExit(f"{sid} prénom hors troupe: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} {c['chunk_id']} fin mécanique: {last}")
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


N3 = LIMITS["N3"]


# ---------------------------------------------------------------------------
# TREE-COL-003  N3  Raphaël  COL.ECO.002
# Arrosoir, tapis, cerisier. Parler trop tôt → personne n'entend → silence.
# Jamais « il faut attendre » en slogan.
# T1 sous le cerisier / près de l'arrosoir / sur le tapis
# T2 le seau / la carafe / le coussin
# T3 le merle / le chat / la poule
# ≠ TREE-COL-001 (pommes, train)
# ---------------------------------------------------------------------------

L1_003 = {
    1: {"lab": "sous le cerisier", "ou": "sous le cerisier", "son": "oiseau"},
    2: {"lab": "près de l'arrosoir", "ou": "près de l'arrosoir", "son": "goutte"},
    3: {"lab": "sur le tapis", "ou": "sur le tapis", "son": "tapis"},
}
L2_003 = {
    1: {"lab": "le seau", "un": "le seau"},
    2: {"lab": "la carafe", "un": "la carafe"},
    3: {"lab": "le coussin", "un": "le coussin"},
}
L3_003 = {
    1: {"lab": "le merle", "qui": "le merle"},
    2: {"lab": "le chat", "qui": "le chat"},
    3: {"lab": "la poule", "qui": "la poule"},
}

ARRIVE_003 = {
    1: vet(
        N3,
        [
            "narrateur|Raphaël s'assoit sous le cerisier.",
            "narrateur|L'ombre est ronde, un peu fraîche.",
            "narrateur|Une cerise pend, trop lourde.",
            "enfant-m|La terre a soif, papa !",
            "enfant-f|Le merle est là !",
            "narrateur|Les deux voix partent en même temps.",
            "narrateur|Le merle chante par-dessus, tout fort.",
            "narrateur|Papa ne tourne pas la tête.",
            "papa|J'entends le merle.",
            "papa|Pas vos mots.",
            "narrateur|Raphaël ferme la bouche.",
            "narrateur|Sa main se lève, tout droit.",
            "narrateur|Mila lève la sienne aussi.",
            "narrateur|Le merle picore, puis se tait.",
            "narrateur|Le silence est chaud, tout soudain.",
            "papa|Je t'entends, maintenant.",
            "enfant-m|La terre a soif.",
            "maman|Oui.",
            "maman|On a entendu.",
            "narrateur|Une cerise tache encore la terre.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Raphaël s'approche de l'arrosoir.",
            "narrateur|Le bec est mouillé, un peu froid.",
            "narrateur|Une goutte tremble, puis tombe.",
            "enfant-m|Je veux l'arrosoir !",
            "enfant-f|L'eau, pour le merle !",
            "narrateur|Les mots tombent dans le ploc.",
            "narrateur|Personne ne se tourne.",
            "maman|J'ai entendu la goutte.",
            "narrateur|Raphaël ferme la bouche.",
            "narrateur|Il pose la main sur le bec.",
            "narrateur|La goutte suivante n'arrive pas.",
            "narrateur|Un petit silence s'installe.",
            "maman|Je t'entends, maintenant.",
            "enfant-m|Je veux l'arrosoir.",
            "papa|Oui.",
            "papa|Il est encore lourd.",
            "narrateur|L'herbe brille, tout verte.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Raphaël revient sur le tapis.",
            "narrateur|Le tissu chatouille le genou.",
            "narrateur|Maman plie un coin de nappe.",
            "enfant-m|La cerise est trop mûre !",
            "enfant-f|Le tapis est doux !",
            "narrateur|Les voix se croisent, tout près.",
            "narrateur|La nappe claque un peu.",
            "papa|J'ai entendu la nappe.",
            "narrateur|Raphaël se tait.",
            "narrateur|Mila met un doigt sur sa bouche.",
            "narrateur|Le clac de la nappe s'arrête.",
            "papa|Je t'entends, maintenant.",
            "enfant-m|La cerise est trop mûre.",
            "maman|Oui.",
            "maman|On a compris.",
            "narrateur|Un fil du tapis reste sous le genou.",
        ],
    ),
}

Q_003 = {
    1: vet(
        N3,
        [
            "narrateur|Les voix se mélangent sous l'arbre.",
            "papa|On a entendu quoi ?",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Le ploc a couvert les mots.",
            "maman|Raphaël veut quoi, près de l'eau ?",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|La nappe a fait du bruit.",
            "maman|Après le silence, on a entendu qui ?",
        ],
    ),
}

C_003 = {
    1: vet(
        N3,
        [
            "papa|Oui.",
            "papa|On n'avait rien entendu.",
            "maman|Le merle était trop fort.",
            "enfant-m|Maintenant, vous m'entendez.",
            "papa|Oui, Raphaël.",
            "papa|Merci.",
            "narrateur|L'ombre du cerisier reste ronde.",
        ],
    ),
    2: vet(
        N3,
        [
            "maman|Oui.",
            "maman|Il veut l'arrosoir.",
            "papa|On t'entend, maintenant.",
            "enfant-m|L'eau est pour le cerisier.",
            "papa|Merci, Raphaël.",
            "narrateur|Une goutte reste au bec, toute ronde.",
        ],
    ),
    3: vet(
        N3,
        [
            "maman|Oui.",
            "maman|On a entendu Raphaël.",
            "papa|Mila aussi, juste après.",
            "enfant-m|La terre a soif.",
            "papa|Merci.",
            "narrateur|Le tapis redevient calme.",
        ],
    ),
}

TAKE_003 = {
    1: vet(
        N3,
        [
            "narrateur|Raphaël prend le seau.",
            "narrateur|Un peu d'eau tremble au fond.",
            "narrateur|Le seau sonne, tout creux.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Raphaël prend la carafe.",
            "narrateur|L'eau brille, un peu froide.",
            "narrateur|Le verre est lisse sous les doigts.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Raphaël tire le coussin.",
            "narrateur|Le tissu est rêche, puis doux.",
            "narrateur|Un fil dépasse, tout calme.",
        ],
    ),
}

MIX_003 = {
    1: vet(
        N3,
        [
            "enfant-m|Je verse !",
            "enfant-f|Moi aussi !",
            "narrateur|Les voix tombent dans l'eau.",
            "narrateur|Le seau fait floc, trop fort.",
            "papa|J'entends l'eau.",
            "papa|Pas vos mots.",
            "narrateur|Raphaël ferme la bouche.",
            "narrateur|Mila aussi.",
            "narrateur|Le floc s'arrête.",
            "maman|Je t'entends, maintenant.",
            "enfant-m|Pour le cerisier.",
        ],
    ),
    2: vet(
        N3,
        [
            "enfant-m|J'ai soif !",
            "enfant-f|La carafe, s'il te plaît !",
            "narrateur|Les mots se cognent au verre.",
            "narrateur|L'eau cloche, trop forte.",
            "maman|J'entends la carafe.",
            "narrateur|Raphaël se tait.",
            "narrateur|Il tient la carafe contre lui.",
            "narrateur|Le cloc s'arrête.",
            "papa|Je t'entends, maintenant.",
            "enfant-m|Un peu d'eau, pour l'arbre.",
        ],
    ),
    3: vet(
        N3,
        [
            "enfant-m|Le coussin est à moi !",
            "enfant-f|Il est doux !",
            "narrateur|Les voix s'enfoncent dans le tissu.",
            "papa|J'entends le coussin.",
            "papa|Un bruit sourd.",
            "narrateur|Raphaël ferme la bouche.",
            "narrateur|Mila pose un doigt sur ses lèvres.",
            "narrateur|Plus rien ne bouge.",
            "maman|Je t'entends, maintenant.",
            "enfant-m|On s'assoit, puis on arrose.",
        ],
    ),
}

LOC_PLAY_003 = {
    (1, 1): "narrateur|Le seau est à l'ombre du cerisier.",
    (1, 2): "narrateur|La carafe prend un rond d'ombre.",
    (1, 3): "narrateur|Le coussin est sous la cerise trop mûre.",
    (2, 1): "narrateur|Le seau sonne contre le bec.",
    (2, 2): "narrateur|La carafe est près de l'arrosoir.",
    (2, 3): "narrateur|Le coussin frotte l'herbe mouillée.",
    (3, 1): "narrateur|Le seau pose un rond sur le tapis.",
    (3, 2): "narrateur|La carafe tient sur un carreau.",
    (3, 3): "narrateur|Le coussin rejoint le tapis, tout doux.",
}

HOLD_003 = {
    1: "Le seau reste dans ses mains.",
    2: "La carafe reste près de lui.",
    3: "Le coussin reste sous son genou.",
}

ANI_003 = {
    1: vet(
        N3,
        [
            "narrateur|Le merle revient, tout près.",
            "narrateur|Il chante une note, trop forte.",
            "enfant-m|J'arrose !",
            "enfant-f|Le merle !",
            "narrateur|Les mots se perdent dans le chant.",
            "papa|J'entends le merle.",
            "narrateur|Raphaël se tait.",
            "narrateur|Le merle picore, puis s'envole.",
            "maman|Je t'entends, maintenant.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Le chat s'étire sur la pierre chaude.",
            "narrateur|Il fait un petit rrr, tout grave.",
            "enfant-m|J'arrose !",
            "enfant-f|Le chat ronronne !",
            "narrateur|Les mots glissent sous le rrr.",
            "papa|J'entends le chat.",
            "narrateur|Raphaël ferme la bouche.",
            "narrateur|Le chat se tait, les yeux mi-clos.",
            "maman|Je t'entends, maintenant.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|La poule picore près de la nappe.",
            "narrateur|Elle fait cot cot, tout sec.",
            "enfant-m|J'arrose !",
            "enfant-f|La poule !",
            "narrateur|Les mots cassent dans le cot cot.",
            "papa|J'entends la poule.",
            "narrateur|Raphaël se tait.",
            "narrateur|La poule s'éloigne, tout calme.",
            "maman|Je t'entends, maintenant.",
        ],
    ),
}

WATER_003 = {
    1: vet(
        N3,
        [
            "enfant-m|La terre a soif.",
            "narrateur|Raphaël penche le seau.",
            "narrateur|L'eau rejoint la terre, tout doux.",
            "maman|Le cerisier boit.",
            "papa|Merci, Raphaël.",
            "enfant-f|Moi, je tiens le bec.",
        ],
    ),
    2: vet(
        N3,
        [
            "enfant-m|Un peu d'eau, pour l'arbre.",
            "narrateur|Raphaël verse un filet de carafe.",
            "narrateur|La terre devient sombre, tout près.",
            "maman|C'est assez.",
            "papa|Merci, Raphaël.",
            "enfant-f|La terre brille.",
        ],
    ),
    3: vet(
        N3,
        [
            "enfant-m|On s'assoit, puis on arrose.",
            "narrateur|Raphaël pose le coussin, puis l'arrosoir.",
            "narrateur|Une goutte tombe sur la terre.",
            "maman|Le cerisier a eu sa goutte.",
            "papa|Merci, Raphaël.",
            "enfant-f|La terre est sombre, maintenant.",
        ],
    ),
}

IMG_003 = {
    (1, 1, 1): "Une plume du merle reste sur le seau.",
    (1, 1, 2): "Une goutte du seau brille sous l'arbre.",
    (1, 1, 3): "Le seau a un peu de terre au fond.",
    (1, 2, 1): "La carafe a pris l'ombre du cerisier.",
    (1, 2, 2): "Un reflet d'eau danse sur la nappe.",
    (1, 2, 3): "La carafe est tiède, maintenant.",
    (1, 3, 1): "Une cerise a roulé contre le coussin.",
    (1, 3, 2): "Le coussin sent l'herbe, tout bas.",
    (1, 3, 3): "Un fil du coussin reste à l'ombre.",
    (2, 1, 1): "Le seau sonne encore, près du bec.",
    (2, 1, 2): "Une goutte du seau a rejoint l'arrosoir.",
    (2, 1, 3): "Le seau est mouillé, tout autour.",
    (2, 2, 1): "La carafe a un peu de terre au pied.",
    (2, 2, 2): "L'eau de la carafe sent l'herbe.",
    (2, 2, 3): "Un cercle d'eau sèche près du bec.",
    (2, 3, 1): "Le coussin a une tache d'eau ronde.",
    (2, 3, 2): "Le bec touche le coussin, tout doux.",
    (2, 3, 3): "Un fil du coussin est mouillé.",
    (3, 1, 1): "Le seau repose sur le tapis, droit.",
    (3, 1, 2): "Une goutte sèche sur un carreau du tapis.",
    (3, 1, 3): "Le seau a marqué un rond sur le tissu.",
    (3, 2, 1): "La carafe tient contre un coin du tapis.",
    (3, 2, 2): "Un carreau de nappe brille encore.",
    (3, 2, 3): "La carafe a réchauffé le tissu.",
    (3, 3, 1): "Le coussin est calme, au milieu du tapis.",
    (3, 3, 2): "Un fil du coussin chatouille encore.",
    (3, 3, 3): "L'ombre du tapis a reculé un peu.",
}

FIN_IMG_003 = {
    (1, 1, 1): "Le merle reprend une note, tout loin.",
    (1, 1, 2): "Une cerise balance, puis tient.",
    (1, 1, 3): "L'ombre du cerisier a grandi.",
    (1, 2, 1): "La carafe a un rond de soleil.",
    (1, 2, 2): "Un merle picore plus loin, tout calme.",
    (1, 2, 3): "La terre sombre sent le vert.",
    (1, 3, 1): "Le coussin garde un peu d'ombre.",
    (1, 3, 2): "Une plume reste sur le tissu.",
    (1, 3, 3): "Le jus de cerise a séché.",
    (2, 1, 1): "Le bec de l'arrosoir ne goutte plus.",
    (2, 1, 2): "Une dernière goutte brille, puis s'en va.",
    (2, 1, 3): "L'herbe autour du bec est sombre.",
    (2, 2, 1): "La carafe sèche au soleil.",
    (2, 2, 2): "Le chat cligne, sur la pierre.",
    (2, 2, 3): "Un cercle d'eau s'est tu.",
    (2, 3, 1): "Le coussin sèche près du bec.",
    (2, 3, 2): "L'arrosoir penche encore, tout léger.",
    (2, 3, 3): "Une poule picore plus loin.",
    (3, 1, 1): "Le tapis a un petit rond d'eau.",
    (3, 1, 2): "Un carreau de nappe ne bouge plus.",
    (3, 1, 3): "Le seau fait un tout petit ting.",
    (3, 2, 1): "La carafe tient, au milieu des carreaux.",
    (3, 2, 2): "Maman plie la nappe, tout doux.",
    (3, 2, 3): "Un fil de tapis reste au soleil.",
    (3, 3, 1): "Le coussin est tiède, maintenant.",
    (3, 3, 2): "Le tapis sent encore l'herbe.",
    (3, 3, 3): "Une ombre ronde recouvre le tapis.",
}


def play_003(i: int, j: int) -> list[str]:
    lines = list(TAKE_003[j])
    lines.append(LOC_PLAY_003[(i, j)])
    lines.extend(MIX_003[j])
    return vet(N3, lines)


def body_003(i: int, j: int, k: int) -> list[str]:
    loc = L1_003[i]
    lines = list(ANI_003[k])
    lines.append(f"narrateur|Raphaël est encore {loc['ou']}.")
    lines.append(f"narrateur|{HOLD_003[j]}")
    lines.extend(WATER_003[j])
    lines.append(f"narrateur|{IMG_003[(i, j, k)]}")
    return vet(N3, lines)


def fin_003(i: int, j: int, k: int) -> list[str]:
    loc = L1_003[i]
    obj = L2_003[j]
    ani = L3_003[k]
    return vet(
        N3,
        [
            f"narrateur|{FIN_IMG_003[(i, j, k)]}",
            f"narrateur|Raphaël a arrosé {loc['ou']}.",
            f"narrateur|Il tenait {obj['lab']}.",
            f"narrateur|{ani['qui'].capitalize()} s'est tu.",
            "enfant-m|La terre a bu.",
            "enfant-f|Oui.",
            "maman|On t'a entendu.",
            "papa|Merci, Raphaël.",
            "narrateur|Une dernière goutte brille, puis s'en va.",
            f"narrateur|{IMG_003[(i, j, k)]}",
        ],
    )


def build_003() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N3,
        [
            "narrateur|L'arrosoir penche encore, près du cerisier.",
            "narrateur|Une goutte tombe.",
            "narrateur|Elle fait ploc dans l'herbe.",
            "narrateur|L'herbe sent le vert, tout chaud.",
            "narrateur|Un merle picore une cerise trop mûre.",
            "narrateur|Le jus tache la terre, tout rouge.",
            "narrateur|Une nappe à carreaux attend sous l'arbre.",
            "narrateur|Papa pose une carafe.",
            "narrateur|L'eau brille, un peu froide.",
            "narrateur|Maman secoue le tapis.",
            "narrateur|Le tapis est rêche, puis doux.",
            "papa|Raphaël, viens.",
            "papa|Le jardin est à nous.",
            "maman|Le tapis est prêt.",
            "enfant-m|Je veux arroser le cerisier.",
            "enfant-m|La terre a soif.",
            "maman|L'arrosoir est encore lourd ?",
            "narrateur|En ce moment, Raphaël pose un genou sur le tapis.",
            "narrateur|Mila arrive, les joues chaudes.",
            "enfant-f|J'ai vu le merle !",
            "enfant-m|La cerise est trop mûre !",
            "narrateur|Les deux voix partent ensemble.",
            "narrateur|Les mots se mélangent, tout fort.",
            "narrateur|Personne ne se tourne.",
            "papa|J'ai entendu un mélange.",
            "maman|On n'a rien compris.",
            "narrateur|Raphaël ferme la bouche.",
            "narrateur|Mila aussi.",
            "narrateur|Le merle picore encore.",
        ],
    )
    sons["CHK_T0000_P0000"] = "goutte,oiseau"

    s["CHK_T0001_P0000"] = vet(
        N3,
        [
            "narrateur|Raphaël veut arroser, mais où ?",
            "papa|Sous le cerisier, près de l'arrosoir, ou sur le tapis ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3(
        "sous le cerisier", "près de l'arrosoir", "sur le tapis"
    )

    q_extra = {
        1: qf(
            "rien",
            "rien | le merle | un mélange | personne | pas les mots",
            "Les mots se mélangent. On a entendu quoi ?",
        ),
        2: qf(
            "arrosoir",
            "arrosoir | l'arrosoir | l eau | l'eau | arroser",
            "Près du bec. Raphaël veut quoi ?",
        ),
        3: qf(
            "Raphaël",
            "Raphaël | raphael | mila | les enfants",
            "Le silence est venu. On a entendu qui ?",
        ),
    }

    for i, loc in L1_003.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_003[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_003[i]
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = C_003[i]
        s[f"{p}_T0002_P0000"] = vet(
            N3,
            [
                f"narrateur|{loc['ou'].capitalize()}, Raphaël prend un objet.",
                "papa|Le seau, la carafe, ou le coussin ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le seau", "la carafe", "le coussin")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = play_003(i, j)
            s[f"{p2}_T0003_P0000"] = vet(
                N3,
                [
                    f"narrateur|Un animal fait du bruit, {loc['ou']}.",
                    "maman|Le merle, le chat, ou la poule ?",
                    "papa|On écoute un moment.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le merle", "le chat", "la poule")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_003(i, j, k)
                s[f"{p3}_F0001"] = fin_003(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-COL-004  N3  Sarah  COL.ECO.001
# Cloche, crayon jaune. Le jaune est à toute la classe.
# Implicit : le crayon manque, elle le remet.
# T1 la table / le casier / le rebord
# T2 le taille-crayon / la gomme / le cahier
# T3 la cloche / le soleil / la fleur
# ≠ TREE-COL-002 (banc, malaise) ≠ TREE-COL-001 (pommes)
# ---------------------------------------------------------------------------

L1_004 = {
    1: {"lab": "la table", "ou": "à la table", "son": "craie"},
    2: {"lab": "le casier", "ou": "près du casier", "son": "casier"},
    3: {"lab": "le rebord", "ou": "au rebord", "son": "vitre"},
}
L2_004 = {
    1: {"lab": "le taille-crayon", "un": "le taille-crayon"},
    2: {"lab": "la gomme", "un": "la gomme"},
    3: {"lab": "le cahier", "un": "le cahier"},
}
L3_004 = {
    1: {"lab": "la cloche", "dessin": "la cloche"},
    2: {"lab": "le soleil", "dessin": "le soleil"},
    3: {"lab": "la fleur", "dessin": "la fleur"},
}

ARRIVE_004 = {
    1: vet(
        N3,
        [
            "narrateur|Sarah pose les coudes à la table.",
            "narrateur|Le bois est lisse, un peu froid.",
            "narrateur|La boîte des crayons est au milieu.",
            "narrateur|Elle est un peu vide.",
            "narrateur|Le jaune reste dans sa main.",
            "enfant-f|Je dessine la cloche.",
            "maitresse|Le jaune est à toute la classe.",
            "narrateur|Nina regarde le crayon, tout doux.",
            "narrateur|Sarah serre encore le bois.",
            "narrateur|La pointe brille, trop longtemps.",
            "maman|La boîte attend, tu as vu ?",
            "narrateur|Sarah glisse le crayon dans la boîte.",
            "narrateur|Le bois tape un tout petit coup.",
            "enfant-f|Il est là.",
            "maitresse|Merci, Sarah.",
            "narrateur|Nina peut le prendre, maintenant.",
            "narrateur|Un copeau jaune reste sur la table.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Sarah s'arrête près du casier.",
            "narrateur|La porte de métal est froide.",
            "narrateur|Le crayon jaune dépasse du cartable.",
            "narrateur|Il pourrait tomber, tout bas.",
            "enfant-f|Il est à moi, dans le sac.",
            "maitresse|La boîte est au milieu.",
            "narrateur|Nina n'a plus de jaune, à sa place.",
            "narrateur|Sarah retire le crayon du cartable.",
            "narrateur|Le bois est encore chaud de sa main.",
            "papa|Tu le poses où, ce jaune ?",
            "narrateur|Sarah traverse jusqu'à la table.",
            "narrateur|Elle glisse le crayon dans la boîte.",
            "narrateur|Le casier se ferme, tout doux.",
            "enfant-f|Il n'est plus dans le sac.",
            "maitresse|Merci, Sarah.",
            "narrateur|Un rayon reste sur le métal.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Sarah s'approche du rebord.",
            "narrateur|La vitre est froide, un peu embuée.",
            "narrateur|Le crayon glisse vers la fenêtre.",
            "narrateur|Il va trop loin, trop vite.",
            "enfant-f|Oh.",
            "narrateur|Sarah le rattrape, tout près du vide.",
            "maman|Il est lisse, ce bois.",
            "narrateur|Nina tend la main, tout doux.",
            "narrateur|Sarah le garde un instant contre elle.",
            "narrateur|Puis elle revient vers la table.",
            "narrateur|Elle pose le jaune dans la boîte.",
            "narrateur|La boîte ne penche plus.",
            "enfant-f|Il ne tombe plus.",
            "maitresse|Merci, Sarah.",
            "narrateur|Un rond de buée reste sur la vitre.",
        ],
    ),
}

Q_004 = {
    1: vet(
        N3,
        [
            "narrateur|Le jaune manque dans la boîte.",
            "maman|Sarah le pose où ?",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Le jaune dépasse du cartable.",
            "papa|Sarah le met où ?",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Le crayon glisse vers la vitre.",
            "maman|Sarah le met où, à la fin ?",
        ],
    ),
}

C_004 = {
    1: vet(
        N3,
        [
            "maman|Oui.",
            "maman|Dans la boîte.",
            "maitresse|Le jaune est au milieu.",
            "enfant-f|Nina peut le prendre.",
            "papa|Merci, Sarah.",
            "narrateur|Un copeau reste sur le bois.",
        ],
    ),
    2: vet(
        N3,
        [
            "papa|Oui.",
            "papa|Dans la boîte, plus dans le sac.",
            "maitresse|Le casier est fermé.",
            "enfant-f|Le jaune est au milieu.",
            "maman|Merci, Sarah.",
            "narrateur|Le métal du casier ne bouge plus.",
        ],
    ),
    3: vet(
        N3,
        [
            "maman|Oui.",
            "maman|Dans la boîte.",
            "papa|Il ne tombe plus.",
            "enfant-f|Nina l'a vu.",
            "maitresse|Merci, Sarah.",
            "narrateur|La buée sèche un peu, sur la vitre.",
        ],
    ),
}

TAKE_004 = {
    1: vet(
        N3,
        [
            "narrateur|Sarah prend le taille-crayon.",
            "narrateur|Le bois du jaune est un peu émoussé.",
            "narrateur|Elle tourne, tout lentement.",
            "narrateur|Un copeau jaune tombe, tout fin.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Sarah prend la gomme.",
            "narrateur|Elle est blanche, un peu rêche.",
            "narrateur|Un trait jaune s'efface, tout doux.",
            "narrateur|La gomme sent le caoutchouc.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Sarah ouvre le cahier.",
            "narrateur|La page est blanche, un peu froide.",
            "narrateur|Le crayon jaune repose sur la reliure.",
            "narrateur|Le papier sent encore la colle.",
        ],
    ),
}

MIX_004 = {
    1: vet(
        N3,
        [
            "enfant-f|Il est trop beau, ce jaune.",
            "narrateur|Elle le garde dans le taille-crayon.",
            "narrateur|La boîte est encore un peu vide.",
            "narrateur|Nina regarde le copeau, puis la main.",
            "maitresse|Le taille-crayon est à toute la classe.",
            "narrateur|Sarah retire le crayon.",
            "narrateur|Elle le pose dans la boîte, tout droit.",
            "enfant-f|Il est prêt.",
            "maman|Merci.",
        ],
    ),
    2: vet(
        N3,
        [
            "enfant-f|La gomme, encore un peu.",
            "narrateur|Le crayon reste collé à sa paume.",
            "narrateur|Nina n'a plus de jaune.",
            "maitresse|La gomme revient au milieu, aussi.",
            "narrateur|Sarah pose la gomme.",
            "narrateur|Puis le crayon, dans la boîte.",
            "enfant-f|Voilà.",
            "papa|Merci, Sarah.",
        ],
    ),
    3: vet(
        N3,
        [
            "enfant-f|Il reste sur ma page.",
            "narrateur|Le jaune dort dans le pli du cahier.",
            "narrateur|Nina cherche le jaune, des yeux.",
            "maitresse|Le cahier est à toi.",
            "maitresse|Le crayon, à la classe.",
            "narrateur|Sarah le glisse hors du pli.",
            "narrateur|Elle le pose dans la boîte.",
            "enfant-f|Ma page est prête.",
            "maman|Merci.",
        ],
    ),
}

LOC_PLAY_004 = {
    (1, 1): "narrateur|Le taille-crayon tapote la table.",
    (1, 2): "narrateur|La gomme laisse un grain sur la table.",
    (1, 3): "narrateur|Le cahier est ouvert, à la table.",
    (2, 1): "narrateur|Un copeau glisse vers le casier.",
    (2, 2): "narrateur|La gomme frotte près du métal.",
    (2, 3): "narrateur|Le cahier s'appuie contre le casier.",
    (3, 1): "narrateur|Un copeau colle au rebord froid.",
    (3, 2): "narrateur|La gomme est tiède, près de la vitre.",
    (3, 3): "narrateur|Le cahier prend un peu de buée.",
}

HOLD_004 = {
    1: "Le taille-crayon reste près d'elle.",
    2: "La gomme reste au milieu.",
    3: "Le cahier reste ouvert.",
}

DRAW_004 = {
    1: vet(
        N3,
        [
            "narrateur|Sarah reprend le jaune, un moment.",
            "narrateur|Elle trace la cloche, toute ronde.",
            "enfant-f|Elle sonne, sur le papier.",
            "maitresse|Je l'entends presque.",
            "narrateur|Nina attend, tout calme.",
            "narrateur|Sarah pose le crayon dans la boîte.",
            "narrateur|Nina le prend, tout doux.",
            "enfant-f|C'est le nôtre.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Sarah reprend le jaune, un moment.",
            "narrateur|Elle trace un soleil, tout chaud.",
            "enfant-f|Il est jaune, comme le crayon.",
            "papa|Il éclaire la page.",
            "narrateur|Nina attend, les mains à plat.",
            "narrateur|Sarah pose le crayon dans la boîte.",
            "narrateur|Nina le prend, tout doux.",
            "enfant-f|C'est le nôtre.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Sarah reprend le jaune, un moment.",
            "narrateur|Elle trace une fleur, tout doux.",
            "enfant-f|Elle a cinq pétales.",
            "maman|Elle est belle, cette fleur.",
            "narrateur|Nina attend, tout calme.",
            "narrateur|Sarah pose le crayon dans la boîte.",
            "narrateur|Nina le prend, tout doux.",
            "enfant-f|C'est le nôtre.",
        ],
    ),
}

IMG_004 = {
    (1, 1, 1): "Un copeau jaune reste près de la cloche.",
    (1, 1, 2): "Le soleil a un copeau au milieu.",
    (1, 1, 3): "Un copeau colle à un pétale.",
    (1, 2, 1): "La gomme a un peu de jaune, sous la cloche.",
    (1, 2, 2): "Un grain de gomme brille sur le soleil.",
    (1, 2, 3): "La fleur a un trait un peu pâle.",
    (1, 3, 1): "La cloche sonne sur la page du cahier.",
    (1, 3, 2): "Le soleil chauffe le pli du cahier.",
    (1, 3, 3): "La fleur ouvre le cahier, tout doux.",
    (2, 1, 1): "Un copeau a glissé vers le casier.",
    (2, 1, 2): "Le soleil dore le métal, un peu.",
    (2, 1, 3): "Une fleur jaune touche le casier.",
    (2, 2, 1): "La cloche est nette, près du métal.",
    (2, 2, 2): "La gomme a laissé le soleil rond.",
    (2, 2, 3): "Un grain de gomme reste sur la fleur.",
    (2, 3, 1): "Le cahier s'appuie, la cloche au milieu.",
    (2, 3, 2): "Le soleil tient contre le casier.",
    (2, 3, 3): "La fleur du cahier ne bouge plus.",
    (3, 1, 1): "La cloche a un peu de buée au bord.",
    (3, 1, 2): "Le soleil éclaire le rebord froid.",
    (3, 1, 3): "Une fleur se colle à la vitre.",
    (3, 2, 1): "La cloche reste nette, malgré la buée.",
    (3, 2, 2): "Le soleil sèche un rond sur la vitre.",
    (3, 2, 3): "La gomme a éclairci un pétale.",
    (3, 3, 1): "La cloche du cahier voit le couloir.",
    (3, 3, 2): "Le soleil du cahier chauffe la buée.",
    (3, 3, 3): "La fleur du cahier touche le rebord.",
}

FIN_IMG_004 = {
    (1, 1, 1): "La vraie cloche sonne, toute ronde.",
    (1, 1, 2): "Un copeau dore encore la table.",
    (1, 1, 3): "Le taille-crayon se tait.",
    (1, 2, 1): "La boîte est pleine, au milieu.",
    (1, 2, 2): "La gomme est ronde, tout calme.",
    (1, 2, 3): "Un grain blanc reste sur le bois.",
    (1, 3, 1): "Le cahier se ferme, tout doux.",
    (1, 3, 2): "Une page garde le soleil.",
    (1, 3, 3): "La reliure sent encore la colle.",
    (2, 1, 1): "Le casier ne claque plus.",
    (2, 1, 2): "Un copeau sèche sur le métal.",
    (2, 1, 3): "Le cartable est fermé.",
    (2, 2, 1): "La gomme tient près du casier.",
    (2, 2, 2): "Le métal est froid, tout calme.",
    (2, 2, 3): "Un rayon quitte le casier.",
    (2, 3, 1): "Le cahier rentre dans le casier.",
    (2, 3, 2): "Une page jaune reste entrevue.",
    (2, 3, 3): "Le loquet du casier tient.",
    (3, 1, 1): "La buée a séché, sur la vitre.",
    (3, 1, 2): "Un copeau colle encore au rebord.",
    (3, 1, 3): "Le rebord est froid, tout nu.",
    (3, 2, 1): "La gomme sèche près de la fenêtre.",
    (3, 2, 2): "Un rond de soleil reste au carreau.",
    (3, 2, 3): "La vitre ne fume plus.",
    (3, 3, 1): "Le cahier voit encore le couloir.",
    (3, 3, 2): "Une page se recourbe, tout doux.",
    (3, 3, 3): "Le rebord garde une poussière jaune.",
}


def play_004(i: int, j: int) -> list[str]:
    lines = list(TAKE_004[j])
    lines.append(LOC_PLAY_004[(i, j)])
    lines.extend(MIX_004[j])
    return vet(N3, lines)


def body_004(i: int, j: int, k: int) -> list[str]:
    loc = L1_004[i]
    lines = list(DRAW_004[k])
    lines.append(f"narrateur|Sarah est encore {loc['ou']}.")
    lines.append(f"narrateur|{HOLD_004[j]}")
    lines.append("papa|Je suis là, à la porte.")
    lines.append("enfant-f|Regarde mon dessin.")
    lines.append("maman|Le jaune est dans la boîte.")
    lines.append("papa|Merci, Sarah.")
    lines.append(f"narrateur|{IMG_004[(i, j, k)]}")
    return vet(N3, lines)


def fin_004(i: int, j: int, k: int) -> list[str]:
    loc = L1_004[i]
    obj = L2_004[j]
    dess = L3_004[k]
    return vet(
        N3,
        [
            f"narrateur|{FIN_IMG_004[(i, j, k)]}",
            f"narrateur|Sarah a dessiné {loc['ou']}.",
            f"narrateur|Elle a pris {obj['lab']}.",
            f"narrateur|{dess['dessin'].capitalize()} est sur la page.",
            "enfant-f|Le jaune est dans la boîte.",
            "maitresse|Oui.",
            "maman|Nina a pu s'en servir.",
            "papa|Merci, Sarah.",
            "narrateur|La cloche sonne encore, plus loin.",
            f"narrateur|{IMG_004[(i, j, k)]}",
        ],
    )


def build_004() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N3,
        [
            "narrateur|La cloche de l'école sonne une fois, toute ronde.",
            "narrateur|Les carreaux du couloir sont froids sous les chaussures.",
            "narrateur|Ça sent la craie et le savon des mains.",
            "narrateur|Un rayon glisse sur le casier de Sarah.",
            "narrateur|Le cartable est un peu lourd.",
            "narrateur|Un crayon jaune dépasse, tout lisse.",
            "maman|Bonne journée, Sarah.",
            "enfant-f|Je veux dessiner la cloche.",
            "enfant-f|Avec le crayon jaune.",
            "maman|La boîte est au milieu, tu as vu ?",
            "enfant-f|Oui.",
            "papa|Je passe te chercher, ce soir.",
            "narrateur|En ce moment, Sarah s'assoit.",
            "narrateur|La chaise fait un petit toc.",
            "narrateur|La boîte des crayons est au milieu.",
            "narrateur|Elle est un peu vide.",
            "narrateur|Le jaune de Sarah est encore dans sa main.",
            "maitresse|Bonjour les enfants.",
            "narrateur|Nina regarde le jaune, tout doux.",
            "enfant-f|Il est lisse.",
            "narrateur|Sarah serre le crayon un moment.",
            "narrateur|La boîte attend, ouverte.",
        ],
    )
    sons["CHK_T0000_P0000"] = "cloche"

    s["CHK_T0001_P0000"] = vet(
        N3,
        [
            "narrateur|Sarah s'installe où, avec le jaune ?",
            "papa|La table, le casier, ou le rebord ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("la table", "le casier", "le rebord")

    q_extra = {
        1: qf(
            "la boîte",
            "la boîte | boite | la boite | au milieu | dans la boîte",
            "La boîte est vide, au milieu. Le crayon va où ?",
        ),
        2: qf(
            "la boîte",
            "la boîte | boite | la boite | au milieu | plus dans le sac",
            "Il dépasse du cartable. Sarah le met où ?",
        ),
        3: qf(
            "la boîte",
            "la boîte | boite | la boite | au milieu | elle le pose",
            "Il glissait vers la vitre. Sarah le met où ?",
        ),
    }

    for i, loc in L1_004.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_004[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_004[i]
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = C_004[i]
        s[f"{p}_T0002_P0000"] = vet(
            N3,
            [
                f"narrateur|{loc['ou'].capitalize()}, Sarah prend un objet.",
                "papa|Le taille-crayon, la gomme, ou le cahier ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le taille-crayon", "la gomme", "le cahier")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = play_004(i, j)
            s[f"{p2}_T0003_P0000"] = vet(
                N3,
                [
                    f"narrateur|Sarah dessine {loc['ou']}.",
                    "maman|La cloche, le soleil, ou la fleur ?",
                    "papa|Tu choisis.",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("la cloche", "le soleil", "la fleur")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_004(i, j, k)
                s[f"{p3}_F0001"] = fin_004(i, j, k)
    return s, sons, extras


def main() -> None:
    s03, n03, e03 = build_003()
    write_tree(
        "TREE-COL-003",
        "Raphaël veut arroser le cerisier. Il parle trop tôt, avec Mila. "
        "Personne n'entend. Ils se taisent. Puis on les entend. "
        "L'eau rejoint la terre.",
        "L'arrosoir et le tapis de Raphaël",
        "Raphaël, Mila, papa, maman",
        "jardin, cerisier, arrosoir, tapis",
        s03,
        n03,
        e03,
    )
    relecture(
        "TREE-COL-003",
        "L'arrosoir et le tapis de Raphaël",
        "Raphaël veut arroser le cerisier. Goutte, merle, nappe, tapis. "
        "Il parle trop tôt avec Mila : mélange, ploc, nappe. "
        "Personne n'entend. Silence. Je t'entends, maintenant. "
        "Cerisier / arrosoir / tapis, puis seau / carafe / coussin, "
        "puis merle / chat / poule. L'eau rejoint la terre.",
        "Jules→Raphaël (D16), Mila. N3. COL.ECO.002 implicite "
        "(parler trop tôt, personne n'entend). "
        "Jamais « il faut attendre ». T3 plus Tom/Léa/Sami. "
        "Monde ≠ TREE-COL-001 (pommes, train). Fin sensorielle.",
    )

    s04, n04, e04 = build_004()
    write_tree(
        "TREE-COL-004",
        "Sarah veut dessiner la cloche avec le crayon jaune. "
        "Le jaune est à toute la classe. Il manque dans la boîte. "
        "Elle le remet. Nina peut s'en servir. Le dessin reste.",
        "La cloche et le crayon jaune de Sarah",
        "Sarah, Nina, papa, maman, maîtresse",
        "école, cloche, couloir, crayon jaune",
        s04,
        n04,
        e04,
    )
    relecture(
        "TREE-COL-004",
        "La cloche et le crayon jaune de Sarah",
        "Sarah veut dessiner la cloche. Crayon jaune, boîte vide, Nina. "
        "Table / casier / rebord, puis taille-crayon / gomme / cahier, "
        "puis cloche / soleil / fleur. Elle remet le jaune. "
        "Nina s'en sert. La cloche sonne.",
        "Sara→Sarah (D16), Nina. N3. COL.ECO.001 implicite "
        "(soin d'un objet partagé). Pas « on écoute la maîtresse ». "
        "T2 plus Tom/Léa/Sami. T3 plus matin/sieste/soir. "
        "Monde ≠ TREE-COL-002 (banc, malaise). Fin sensorielle.",
    )


if __name__ == "__main__":
    main()
