#!/usr/bin/env python3
"""TREE-AUT-048 / TREE-COL-002 — récit implicite, graphe 86, D16."""
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
        if kind in ("passage_question", "transition_question"):
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


N1 = LIMITS["N1"]
N2 = LIMITS["N2"]


# ---------------------------------------------------------------------------
# TREE-AUT-048  N1  Nina  AUT.AFF.003
# Seau rouge, anse en corde, ronds du lampadaire, banc de pierre.
# ≠ 008 Aniss seau jaune cour ; ≠ 011 Sarah seau jaune ferme
# ≠ 025 Nina fontaine bottes ; ≠ 028 Victorino seau vert
# ≠ 033 Nino kiosque zinc seau jaune ; ≠ 038 Mila seau sous la table
# ---------------------------------------------------------------------------

L1_048 = {
    1: {"lab": "le bac à sable", "ou": "près du bac", "son": "enfants_parc"},
    2: {"lab": "le toboggan", "ou": "près du toboggan", "son": "enfants_parc"},
    3: {"lab": "les balançoires", "ou": "près des balançoires", "son": "enfants_parc"},
}
L2_048 = {
    1: {"lab": "le ballon", "obj": "le ballon mouillé"},
    2: {"lab": "le seau", "obj": "le seau rouge"},
    3: {"lab": "le doudou", "obj": "le doudou beige"},
}
L3_048 = {
    1: {"lab": "le banc", "ou": "vers le banc de pierre"},
    2: {"lab": "le portail", "ou": "vers le portail"},
    3: {"lab": "la haie", "ou": "vers la haie"},
}

ARRIVE_048 = {
    1: vet(
        N1,
        [
            "narrateur|Nina s'agenouille près du bac.",
            "narrateur|Le sable est sombre, un peu froid.",
            "narrateur|Une trace ronde reste au milieu.",
            "enfant-f|Mon seau était là.",
            "maman|Oui.",
            "maman|La trace est encore nette.",
            "papa|Les ronds de la flaque t'attendent.",
            "narrateur|Nina fouille le sable mouillé.",
            "narrateur|L'anse en corde dépasse, toute rouge.",
            "enfant-f|Je le vois !",
            "narrateur|Elle tire le seau.",
            "narrateur|Du sable tombe, tout doux.",
            "papa|Tu le tiens bien ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un grain reste sur sa joue.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Nina va vers le toboggan.",
            "narrateur|Le métal est froid, encore luisant.",
            "narrateur|Une goutte brille sur une marche.",
            "enfant-f|Il est froid, maman.",
            "maman|Oui.",
            "maman|Le soleil va le tiédir.",
            "papa|Ton manteau sèche sur la marche.",
            "narrateur|Le tissu gris frotte le métal.",
            "narrateur|Nina le prend à deux mains.",
            "enfant-f|Il est un peu lourd.",
            "papa|Il était resté là.",
            "narrateur|Une goutte glisse de la manche.",
            "maman|Le seau reste près de la flaque.",
            "enfant-f|Je le vois, en bas.",
            "narrateur|Le plastique du toboggan fait frou.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Nina va vers les balançoires.",
            "narrateur|Une chaîne fait tic, tout doux.",
            "narrateur|Le siège rouge est encore humide.",
            "enfant-f|Ça bouge tout seul.",
            "maman|C'est le vent, Nina.",
            "papa|Le doudou est sous le siège.",
            "narrateur|Nina se penche.",
            "narrateur|Le doudou beige a une oreille mouillée.",
            "enfant-f|Il a de l'eau.",
            "maman|On le serre un moment.",
            "narrateur|Nina le presse contre elle.",
            "narrateur|Le tissu sent encore le savon.",
            "papa|Le seau rouge reste à la flaque.",
            "enfant-f|Je le vois.",
            "narrateur|La chaîne ne fait plus tic.",
        ],
    ),
}

Q_048 = {
    1: vet(
        N1,
        [
            "narrateur|L'anse rouge dépasse du sable.",
            "papa|Nina a pris quoi ?",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Le tissu gris était sur la marche.",
            "maman|Nina a pris quoi ?",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Le doudou était sous le siège.",
            "papa|Nina a pris quoi ?",
        ],
    ),
}

C_048 = {
    1: vet(
        N1,
        [
            "narrateur|Nina tient déjà le seau rouge.",
            "enfant-f|Pour les ronds.",
            "papa|Oui.",
            "papa|Merci, Nina.",
            "maman|Le manteau reste sur la pierre.",
            "narrateur|Du sable reste au fond du seau.",
            "papa|On joue encore un peu ?",
            "enfant-f|Oui.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Nina tient déjà le manteau gris.",
            "enfant-f|Il était froid.",
            "maman|Oui.",
            "maman|Merci, Nina.",
            "papa|Le seau rouge reste à la flaque.",
            "narrateur|Une goutte sèche sur la manche.",
            "maman|On joue encore un peu ?",
            "enfant-f|Oui.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|Nina tient déjà le doudou beige.",
            "enfant-f|Son oreille est mouillée.",
            "papa|Oui.",
            "papa|Merci, Nina.",
            "maman|Le seau rouge reste à la flaque.",
            "narrateur|L'oreille du doudou sèche un peu.",
            "papa|On joue encore un peu ?",
            "enfant-f|Oui.",
        ],
    ),
}

PLAY_048 = {
    (1, 1): vet(
        N1,
        [
            "narrateur|Près du bac, le ballon attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Nina pose les deux mains dessus.",
            "narrateur|Le ballon prend un peu de sable.",
            "maman|Tu as déjà le seau.",
            "papa|Le manteau reste sur la pierre.",
            "enfant-f|Je le vois.",
            "narrateur|Un grain colle au cuir mouillé.",
        ],
    ),
    (1, 2): vet(
        N1,
        [
            "narrateur|Près du bac, le seau rouge est là.",
            "narrateur|L'anse en corde est froide.",
            "enfant-f|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Nina tient l'anse des deux mains.",
            "narrateur|Le seau racle le sable, toc.",
            "maman|Tu l'as déjà, ce seau.",
            "papa|Il restera le manteau.",
            "enfant-f|Sur la pierre.",
            "narrateur|Du sable reste au fond, tout sombre.",
        ],
    ),
    (1, 3): vet(
        N1,
        [
            "narrateur|Près du bac, le doudou beige attend.",
            "narrateur|Le tissu est doux, un peu plat.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Nina le serre contre le seau.",
            "narrateur|L'oreille frotte l'anse en corde.",
            "maman|Tu as déjà le seau.",
            "papa|Le manteau reste sur la pierre.",
            "enfant-f|Je le vois.",
            "narrateur|Un grain reste sur l'oreille beige.",
        ],
    ),
    (2, 1): vet(
        N1,
        [
            "narrateur|Près du toboggan, le ballon attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Nina le presse contre le manteau.",
            "narrateur|Le cuir frotte le tissu gris.",
            "maman|Tu as déjà le manteau.",
            "papa|Le seau reste près de la flaque.",
            "enfant-f|Pour les ronds.",
            "narrateur|Une goutte du métal touche le ballon.",
        ],
    ),
    (2, 2): vet(
        N1,
        [
            "narrateur|Près du toboggan, le seau rouge attend.",
            "narrateur|L'anse en corde est froide.",
            "enfant-f|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Nina le tire vers elle.",
            "narrateur|Le seau tape sa jambe, tout doux.",
            "maman|Tu as le manteau.",
            "maman|Tu as le seau.",
            "enfant-f|Pour les ronds.",
            "narrateur|Une goutte du toboggan sonne dedans.",
        ],
    ),
    (2, 3): vet(
        N1,
        [
            "narrateur|Près du toboggan, le doudou beige attend.",
            "narrateur|Le tissu est doux, un peu plat.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Nina le glisse sous le manteau.",
            "narrateur|L'oreille dépasse, un peu froide.",
            "maman|Tu as déjà le manteau.",
            "papa|Le seau reste près de la flaque.",
            "enfant-f|Je le prendrai.",
            "narrateur|Le doudou a touché la marche lisse.",
        ],
    ),
    (3, 1): vet(
        N1,
        [
            "narrateur|Près des balançoires, le ballon attend.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, maman.",
            "papa|D'accord.",
            "narrateur|Nina le serre avec le doudou.",
            "narrateur|Le ballon rebondit une fois, tout mou.",
            "maman|Tu as déjà le doudou.",
            "papa|Le seau reste près de la flaque.",
            "enfant-f|Pour les ronds.",
            "narrateur|Un brin d'herbe colle au cuir.",
        ],
    ),
    (3, 2): vet(
        N1,
        [
            "narrateur|Près des balançoires, le seau rouge attend.",
            "narrateur|L'anse en corde est froide.",
            "enfant-f|Le seau, papa.",
            "papa|D'accord.",
            "narrateur|Nina tient l'anse et le doudou.",
            "narrateur|Le seau tapote l'herbe, toc.",
            "maman|Tu as le doudou.",
            "maman|Tu as le seau.",
            "enfant-f|Pour les ronds.",
            "narrateur|L'anse frotte l'oreille beige.",
        ],
    ),
    (3, 3): vet(
        N1,
        [
            "narrateur|Près des balançoires, le doudou beige attend.",
            "narrateur|Le tissu est doux, un peu plat.",
            "enfant-f|Le doudou, maman.",
            "papa|D'accord.",
            "narrateur|Nina le serre encore plus fort.",
            "narrateur|L'oreille sèche contre sa joue.",
            "maman|Tu l'as déjà, ce doudou.",
            "papa|Le seau reste près de la flaque.",
            "enfant-f|Je le prendrai.",
            "narrateur|La chaîne fait un tout petit tic.",
        ],
    ),
}

FIND_048 = {
    1: vet(
        N1,
        [
            "narrateur|Le banc de pierre est encore froid.",
            "narrateur|La mousse verte brille un peu.",
            "narrateur|Une feuille y reste collée.",
        ],
    ),
    2: vet(
        N1,
        [
            "narrateur|Le portail de fer est un peu froid.",
            "narrateur|La barre fait un petit clic.",
            "narrateur|Une goutte y tremble encore.",
        ],
    ),
    3: vet(
        N1,
        [
            "narrateur|La haie sent la terre mouillée.",
            "narrateur|Une branche touche l'épaule de Nina.",
            "narrateur|Une goutte glisse sur une feuille.",
        ],
    ),
}

TAKE_048 = {
    (True, True): vet(
        N1,
        [
            "papa|C'est l'heure de rentrer.",
            "narrateur|Nina tient déjà le seau rouge.",
            "narrateur|Elle tient déjà le manteau gris.",
            "enfant-f|J'ai les deux.",
            "maman|Oui.",
            "maman|On peut y aller.",
        ],
    ),
    (True, False): vet(
        N1,
        [
            "papa|C'est l'heure de rentrer.",
            "narrateur|Nina tient déjà le seau rouge.",
            "maman|Cherche le manteau, Nina.",
            "narrateur|Le manteau gris sèche encore.",
            "narrateur|Elle le prend.",
            "enfant-f|J'ai les deux.",
            "papa|Oui.",
        ],
    ),
    (False, True): vet(
        N1,
        [
            "papa|C'est l'heure de rentrer.",
            "narrateur|Nina tient déjà le manteau gris.",
            "maman|Cherche le seau, Nina.",
            "narrateur|Le seau rouge l'attend.",
            "narrateur|Elle prend l'anse en corde.",
            "enfant-f|Pour les ronds.",
            "papa|Oui.",
        ],
    ),
    (False, False): vet(
        N1,
        [
            "papa|C'est l'heure de rentrer.",
            "maman|Cherche le seau, Nina.",
            "narrateur|Le seau rouge l'attend.",
            "narrateur|Elle prend l'anse en corde.",
            "papa|Cherche le manteau.",
            "narrateur|Le manteau gris sèche encore.",
            "narrateur|Elle le prend aussi.",
            "enfant-f|J'ai les deux.",
        ],
    ),
}

CLOSE_048 = {
    1: vet(
        N1,
        [
            "maman|On passe près du banc.",
            "papa|Le seau.",
            "papa|Le manteau.",
            "enfant-f|Avec moi.",
            "narrateur|La mousse reste verte, toute calme.",
        ],
    ),
    2: vet(
        N1,
        [
            "maman|On passe le portail.",
            "papa|Le seau.",
            "papa|Le manteau.",
            "enfant-f|J'ai tout.",
            "narrateur|Le fer fait clic, tout doux.",
        ],
    ),
    3: vet(
        N1,
        [
            "maman|On longe la haie.",
            "papa|Le seau.",
            "papa|Le manteau.",
            "enfant-f|J'ai tout.",
            "narrateur|Une feuille de haie reste au seau.",
        ],
    ),
}

HOLD_048 = {
    1: "Le ballon reste rond, tout calme.",
    2: "Le seau rouge reste dans ses mains.",
    3: "Le doudou reste contre sa joue.",
}

IMG_048 = {
    (1, 1, 1): "Un grain de sable colle au ballon.",
    (1, 1, 2): "Le ballon frotte la barre du portail.",
    (1, 1, 3): "Le ballon a une feuille de haie.",
    (1, 2, 1): "Du sable reste au fond du seau.",
    (1, 2, 2): "L'anse en corde frotte le fer.",
    (1, 2, 3): "Une feuille de haie tombe dans le seau.",
    (1, 3, 1): "Le doudou a un grain sur l'oreille.",
    (1, 3, 2): "Le doudou frotte la barre froide.",
    (1, 3, 3): "L'oreille beige a une feuille de haie.",
    (2, 1, 1): "Le ballon a une goutte du toboggan.",
    (2, 1, 2): "Une goutte du métal sèche au portail.",
    (2, 1, 3): "Le ballon frotte une branche basse.",
    (2, 2, 1): "Une goutte du toboggan sonne au seau.",
    (2, 2, 2): "Le seau rouge tape le fer, toc.",
    (2, 2, 3): "L'anse en corde accroche une feuille.",
    (2, 3, 1): "L'oreille du doudou a une goutte.",
    (2, 3, 2): "Le doudou passe sous la barre.",
    (2, 3, 3): "Le doudou frotte la haie, tout doux.",
    (3, 1, 1): "Le ballon a senti la chaîne froide.",
    (3, 1, 2): "Le ballon rebondit une fois au portail.",
    (3, 1, 3): "Un brin d'herbe reste au ballon.",
    (3, 2, 1): "L'anse du seau a une goutte de chaîne.",
    (3, 2, 2): "Le seau rouge sonne contre le fer.",
    (3, 2, 3): "Le seau emporte une feuille de haie.",
    (3, 3, 1): "L'oreille du doudou sent encore le vent.",
    (3, 3, 2): "Le doudou passe sous le portail.",
    (3, 3, 3): "L'oreille beige frotte la haie.",
}

FIN_IMG_048 = {
    (1, 1, 1): "La mousse du banc ne brille plus.",
    (1, 1, 2): "Le portail reste un peu froid.",
    (1, 1, 3): "La haie sent encore la terre.",
    (1, 2, 1): "Du sable sèche au fond du seau.",
    (1, 2, 2): "L'anse en corde ne goutte plus.",
    (1, 2, 3): "Une feuille reste au bord du seau.",
    (1, 3, 1): "L'oreille du doudou est presque sèche.",
    (1, 3, 2): "Le doudou ne frotte plus le fer.",
    (1, 3, 3): "Une feuille de haie sèche sur l'oreille.",
    (2, 1, 1): "Le manteau gris ne goutte plus.",
    (2, 1, 2): "Une goutte sèche sur la barre.",
    (2, 1, 3): "Le manteau sent encore le métal.",
    (2, 2, 1): "Le seau et le manteau restent calmes.",
    (2, 2, 2): "Le fer du portail ne cliquète plus.",
    (2, 2, 3): "L'anse en corde sent la haie.",
    (2, 3, 1): "Le doudou sèche contre le manteau.",
    (2, 3, 2): "L'oreille beige a passé le fer.",
    (2, 3, 3): "Le manteau frotte encore une feuille.",
    (3, 1, 1): "La chaîne de la balançoire s'est tue.",
    (3, 1, 2): "Le ballon ne rebondit plus.",
    (3, 1, 3): "Un brin d'herbe sèche sur le cuir.",
    (3, 2, 1): "Le seau rouge ne sonne plus.",
    (3, 2, 2): "Le portail reste fermé, tout calme.",
    (3, 2, 3): "Une feuille de haie sèche au seau.",
    (3, 3, 1): "L'oreille beige ne sent plus le vent.",
    (3, 3, 2): "Le doudou a passé le fer.",
    (3, 3, 3): "La haie ne touche plus l'épaule.",
}


def body_048(i: int, j: int, k: int) -> list[str]:
    loc = L1_048[i]
    has_bucket = i == 1 or j == 2
    has_coat = i == 2
    lines = list(FIND_048[k])
    lines.append(f"narrateur|Nina est encore {loc['ou']}.")
    lines.append(f"narrateur|{HOLD_048[j]}")
    lines.extend(TAKE_048[(has_bucket, has_coat)])
    lines.extend(CLOSE_048[k])
    lines.append("enfant-f|Merci, papa.")
    lines.append("enfant-f|Merci, maman.")
    lines.append(f"narrateur|{IMG_048[(i, j, k)]}")
    return vet(N1, lines)


def fin_048(i: int, j: int, k: int) -> list[str]:
    loc = L1_048[i]
    obj = L2_048[j]
    dest = L3_048[k]
    return vet(
        N1,
        [
            f"narrateur|{IMG_048[(i, j, k)]}",
            f"narrateur|Nina a joué {loc['ou']}.",
            f"narrateur|Elle avait {obj['lab']}.",
            f"narrateur|Puis {dest['lab']}.",
            "enfant-f|J'ai le seau.",
            "enfant-f|J'ai le manteau.",
            "maman|On rentre.",
            "papa|Le lampadaire s'est tu.",
            "narrateur|Un dernier rond s'efface.",
            f"narrateur|{FIN_IMG_048[(i, j, k)]}",
        ],
    )


def build_048() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N1,
        [
            "narrateur|Le lampadaire goutte sur le chemin.",
            "narrateur|Une flaque fait des ronds.",
            "narrateur|Ploc.",
            "narrateur|Le seau rouge est près de l'eau.",
            "narrateur|L'anse est en corde, un peu rêche.",
            "narrateur|Un manteau gris sèche sur la pierre.",
            "narrateur|La mousse du banc est verte.",
            "narrateur|Une feuille y colle, toute plate.",
            "narrateur|La maison est juste derrière.",
            "narrateur|La fenêtre a un peu de buée.",
            "narrateur|Papa plie une serviette.",
            "papa|On rentre bientôt, Nina ?",
            "maman|Le seau est encore dehors.",
            "enfant-f|Je veux les ronds !",
            "enfant-f|Dans mon seau.",
            "narrateur|En ce moment, Nina touche l'anse.",
            "narrateur|La corde est froide, un peu mouillée.",
            "papa|Tu le prends, le seau ?",
            "enfant-f|Oui, papa.",
            "maman|Le manteau reste sur la pierre.",
            "narrateur|Une goutte fait encore un rond.",
        ],
    )
    sons["CHK_T0000_P0000"] = "enfants_parc"

    s["CHK_T0001_P0000"] = vet(
        N1,
        [
            "narrateur|Nina peut commencer à trois endroits.",
            "papa|Le bac à sable, le toboggan, ou les balançoires ?",
            "maman|Tu choisis.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("le bac à sable", "le toboggan", "les balançoires")

    q_extra = {
        1: qf("seau", "seau | le seau | seau rouge | le seau rouge", "Le seau rouge. Nina a pris quoi ?"),
        2: qf(
            "manteau",
            "manteau | le manteau | manteau gris | le manteau gris",
            "Le manteau. Nina a pris quoi ?",
        ),
        3: qf(
            "doudou",
            "doudou | le doudou | doudou beige | le doudou beige",
            "Le doudou. Nina a pris quoi ?",
        ),
    }

    for i, loc in L1_048.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_048[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_048[i]
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = C_048[i]
        s[f"{p}_T0002_P0000"] = vet(
            N1,
            [
                f"narrateur|{loc['ou'].capitalize()}, Nina prend un objet.",
                "papa|Le ballon, le seau, ou le doudou ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_048[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N1,
                [
                    f"narrateur|Nina a {L2_048[j]['lab']}, {loc['ou']}.",
                    "maman|Avant de rentrer, on passe où ?",
                    "papa|Le banc, le portail, ou la haie ?",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le banc", "le portail", "la haie")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_048(i, j, k)
                s[f"{p3}_F0001"] = fin_048(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-COL-002  N2  Amir  COL.ECO.001
# Banc de fer, feuille de platane, goûter. S'asseoir / partager / pas jeter.
# ≠ COL-001 pommes train ; ≠ COL-023 banc bois pommier Mila
# ≠ COL-033 chaîne galet malaise ; ≠ COL-014 gant rouge malaise
# ---------------------------------------------------------------------------

L1_002 = {
    1: {"lab": "une pomme", "reste": "la pelure", "son": "enfants_parc,pomme"},
    2: {"lab": "un yaourt", "reste": "le couvercle", "son": "enfants_parc"},
    3: {"lab": "un morceau de pain", "reste": "une miette", "son": "enfants_parc"},
}
L2_002 = {
    1: {"lab": "la cuisine", "ou": "dans la cuisine", "son": "cacao,porte"},
    2: {"lab": "le jardin", "ou": "dans le jardin", "son": "porte"},
    3: {"lab": "la chambre", "ou": "dans la chambre", "son": "porte"},
}
L3_002 = {
    1: {"lab": "les cubes", "un": "un cube"},
    2: {"lab": "le livre", "un": "le livre"},
    3: {"lab": "la dînette", "un": "une tasse"},
}

ARRIVE_002 = {
    1: vet(
        N2,
        [
            "narrateur|Amir sort une pomme du sac tiède.",
            "narrateur|Elle est lisse, un peu froide.",
            "narrateur|Il croque.",
            "narrateur|Ça fait un petit bruit clair.",
            "enfant-m|Elle est sucrée, maman.",
            "maman|Oui.",
            "maman|On est bien assis, maintenant.",
            "papa|La feuille est sous le platane.",
            "narrateur|Une pelure glisse vers le bois mouillé.",
            "enfant-m|Oh.",
            "maman|Tu veux encore de la place, sur le banc ?",
            "enfant-m|Oui.",
            "narrateur|Amir met la pelure dans le sac.",
            "narrateur|Le bois reste libre, tout calme.",
            "papa|Merci, Amir.",
            "narrateur|La pomme sent encore le sucré et la pluie.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Amir ouvre un yaourt.",
            "narrateur|La cuillère est petite, un peu froide.",
            "narrateur|Le yaourt est blanc, tout doux.",
            "enfant-m|Il est froid, papa.",
            "papa|Oui.",
            "papa|Le banc est à nous, tous les deux.",
            "maman|Le couvercle tremble dans le vent.",
            "narrateur|Le plastique blanc veut s'envoler.",
            "enfant-m|Il va tomber dans la flaque.",
            "maman|Tu le mets où, pour garder ta place ?",
            "enfant-m|Dans le sac.",
            "narrateur|Amir glisse le couvercle dans le sac.",
            "narrateur|Le banc reste libre, à côté de maman.",
            "papa|Merci, Amir.",
            "narrateur|Une cuillerée blanche reste au bord.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Amir mange un morceau de pain.",
            "narrateur|La croûte est un peu rêche.",
            "narrateur|La mie est encore tiède.",
            "enfant-m|Il est bon, maman.",
            "maman|Oui.",
            "maman|On a de la place, tous les deux.",
            "papa|Une miette tombe sur le bois mouillé.",
            "narrateur|L'oiseau picore trop près du banc.",
            "enfant-m|Il veut ma place.",
            "maman|Tu mets la miette où, pour l'oiseau ?",
            "enfant-m|Sur la terre, sous l'arbre.",
            "narrateur|Amir pose la miette près de la feuille.",
            "narrateur|L'oiseau saute vers la terre, pas vers le banc.",
            "papa|Merci, Amir.",
            "narrateur|Le pain sent encore le four, tout doux.",
        ],
    ),
}

Q_002 = {
    1: vet(
        N2,
        [
            "narrateur|La pelure allait sur le banc.",
            "papa|Amir l'a mise où ?",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le couvercle voulait s'envoler.",
            "maman|Amir l'a mis où ?",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|La miette était sur le bois.",
            "papa|Amir l'a mise où ?",
        ],
    ),
}

C_002 = {
    1: vet(
        N2,
        [
            "narrateur|La pelure est dans le sac.",
            "enfant-m|Le banc est pour s'asseoir.",
            "papa|Oui.",
            "papa|Merci, Amir.",
            "maman|La feuille reste sous le platane.",
            "narrateur|Une goutte glisse encore du fer.",
            "papa|On rentre tout à l'heure ?",
            "enfant-m|D'accord.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le couvercle est dans le sac.",
            "enfant-m|Le banc est pour s'asseoir.",
            "maman|Oui.",
            "maman|Merci, Amir.",
            "papa|La feuille reste sous le platane.",
            "narrateur|Le yaourt blanc ne tremble plus.",
            "maman|On rentre tout à l'heure ?",
            "enfant-m|D'accord.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|La miette est sur la terre.",
            "enfant-m|Le banc est pour s'asseoir.",
            "papa|Oui.",
            "papa|Merci, Amir.",
            "maman|L'oiseau mange sous le platane.",
            "narrateur|Le bois mouillé reste libre.",
            "papa|On rentre tout à l'heure ?",
            "enfant-m|D'accord.",
        ],
    ),
}

HOME_002 = {
    1: vet(
        N2,
        [
            "narrateur|Plus tard, ils rentrent.",
            "narrateur|La cuisine sent le cacao.",
            "narrateur|La tasse fume, tout doux.",
            "narrateur|Papa a posé son manteau.",
            "enfant-m|Le banc était mouillé.",
            "enfant-m|On a fait de la place.",
            "maman|Oui.",
            "maman|La feuille est sous l'arbre.",
            "papa|Le sac est encore un peu lourd.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Plus tard, ils vont au jardin.",
            "narrateur|L'herbe est encore un peu mouillée.",
            "narrateur|Une marche de pierre est presque sèche.",
            "narrateur|Papa ouvre la petite porte.",
            "enfant-m|Le banc du parc était mouillé.",
            "enfant-m|On a fait de la place.",
            "maman|Oui.",
            "maman|La feuille est sous l'arbre.",
            "papa|Ici, la marche est à nous.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Plus tard, ils vont dans la chambre.",
            "narrateur|La couverture est douce, un peu froissée.",
            "narrateur|Le tapis sent encore le savon.",
            "narrateur|Papa s'assoit sur le bord du lit.",
            "enfant-m|Le banc du parc était mouillé.",
            "enfant-m|On a fait de la place.",
            "maman|Oui.",
            "maman|La feuille est sous l'arbre.",
            "papa|Ici, le tapis est à nous.",
        ],
    ),
}

SNACK_REST_002 = {
    1: vet(
        N2,
        [
            "narrateur|La pelure reste dans le sac.",
            "narrateur|Ça sent encore la pomme, tout bas.",
            "enfant-m|Elle n'est pas sur le banc.",
            "maman|Oui.",
            "maman|Le banc est resté libre.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le couvercle reste dans le sac.",
            "narrateur|Le plastique blanc ne s'envole plus.",
            "enfant-m|Il n'est pas dans la flaque.",
            "papa|Oui.",
            "papa|Le banc est resté libre.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Une miette a voyagé, dans le sac.",
            "narrateur|L'autre est restée sous le platane.",
            "enfant-m|L'oiseau l'a, lui.",
            "maman|Oui.",
            "maman|Le banc est resté libre.",
        ],
    ),
}

PLAY_002 = {
    1: vet(
        N2,
        [
            "narrateur|Les cubes de bois attendent.",
            "narrateur|Ils sentent le sapin, tout doux.",
            "papa|Tu fais un banc, Amir ?",
            "enfant-m|Oui.",
            "enfant-m|Un banc sec, pour deux.",
            "narrateur|Il pose deux cubes, puis un troisième.",
            "maman|Il reste de la place, à côté ?",
            "enfant-m|Oui, pour toi.",
            "papa|Bravo.",
            "narrateur|Le cube du milieu est un peu rêche.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le livre est ouvert, tout calme.",
            "narrateur|Une grande feuille est dessinée.",
            "maman|On dirait le platane, Amir.",
            "enfant-m|Oui.",
            "enfant-m|On l'a posée sous l'arbre.",
            "narrateur|Il tourne la page, tout lentement.",
            "papa|Le banc de l'image est vide.",
            "enfant-m|On peut s'asseoir, dessus.",
            "maman|Merci.",
            "narrateur|La page sent encore le papier neuf.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|La dînette cliquette dans son panier.",
            "narrateur|Une petite assiette est blanche.",
            "papa|On sert le goûter, tout petit ?",
            "enfant-m|Oui.",
            "enfant-m|Puis on remet dans le sac.",
            "narrateur|Il pose une miette imaginaire.",
            "maman|Elle va sur l'assiette, ou par terre ?",
            "enfant-m|Sur l'assiette.",
            "papa|Merci.",
            "narrateur|La petite cuillère fait ting.",
        ],
    ),
}

IMG_002 = {
    (1, 1, 1): "Une miette de cacao reste près d'un cube.",
    (1, 1, 2): "La page du livre sent encore la pomme.",
    (1, 1, 3): "La petite assiette a une pelure dessinée.",
    (1, 2, 1): "Un cube a un peu d'herbe au coin.",
    (1, 2, 2): "Une goutte d'herbe sèche sur la page.",
    (1, 2, 3): "L'assiette miniature a une feuille dessinée.",
    (1, 3, 1): "Un cube repose contre l'oreiller, tout calme.",
    (1, 3, 2): "La page touche la couverture douce.",
    (1, 3, 3): "La petite tasse est près du doudou.",
    (2, 1, 1): "Le couvercle blanc brille près de la tasse.",
    (2, 1, 2): "Une page montre un banc vide.",
    (2, 1, 3): "La petite cuillère a encore du blanc.",
    (2, 2, 1): "Un cube a une goutte d'herbe.",
    (2, 2, 2): "Le livre a une page un peu fraîche.",
    (2, 2, 3): "L'osier du panier sent le jardin.",
    (2, 3, 1): "Un cube tapote le tapis, tout doux.",
    (2, 3, 2): "La page se recourbe sur le lit.",
    (2, 3, 3): "La petite assiette reflète la veilleuse.",
    (3, 1, 1): "Une miette de pain reste près du cacao.",
    (3, 1, 2): "Le livre a une miette au creux.",
    (3, 1, 3): "La petite assiette a une croûte minuscule.",
    (3, 2, 1): "Un cube a une miette collée, toute sèche.",
    (3, 2, 2): "Une page sent encore le pain tiède.",
    (3, 2, 3): "L'assiette a reçu une miette de jardin.",
    (3, 3, 1): "Un cube est contre l'oreiller, tout calme.",
    (3, 3, 2): "La page reste ouverte, sur le lit.",
    (3, 3, 3): "La petite tasse sèche près du doudou.",
}

FIN_IMG_002 = {
    (1, 1, 1): "Le cacao ne fume plus, dans la tasse.",
    (1, 1, 2): "La pelure reste au fond du sac.",
    (1, 1, 3): "La petite cuillère ne fait plus ting.",
    (1, 2, 1): "L'herbe du jardin ne brille plus.",
    (1, 2, 2): "Une goutte sèche sur la marche.",
    (1, 2, 3): "Le panier d'osier est posé droit.",
    (1, 3, 1): "L'oreiller ne bouge plus.",
    (1, 3, 2): "La veilleuse dore encore la page.",
    (1, 3, 3): "Le tapis de la chambre est calme.",
    (2, 1, 1): "Le couvercle blanc reste dans le sac.",
    (2, 1, 2): "Le livre se referme, tout doux.",
    (2, 1, 3): "La tasse de cacao devient tiède.",
    (2, 2, 1): "La marche de pierre ne goutte plus.",
    (2, 2, 2): "Une feuille vraie reste dans le livre.",
    (2, 2, 3): "L'herbe colle encore à l'osier.",
    (2, 3, 1): "Un cube reste au pied du lit.",
    (2, 3, 2): "La page ne se recourbe plus.",
    (2, 3, 3): "La petite assiette ne brille plus.",
    (3, 1, 1): "Une miette sèche près de la tasse.",
    (3, 1, 2): "Le livre garde une odeur de pain.",
    (3, 1, 3): "La petite assiette est vide, enfin.",
    (3, 2, 1): "Un cube a encore une miette sèche.",
    (3, 2, 2): "La marche garde une odeur de pain.",
    (3, 2, 3): "L'oiseau du jardin s'est tu.",
    (3, 3, 1): "Le doudou ne bouge plus, au lit.",
    (3, 3, 2): "La page reste ouverte, tout calme.",
    (3, 3, 3): "La petite tasse sèche, près du tapis.",
}


def body_002(i: int, j: int, k: int) -> list[str]:
    lines = list(HOME_002[j])
    lines.extend(SNACK_REST_002[i])
    lines.extend(PLAY_002[k])
    lines.append(f"narrateur|{IMG_002[(i, j, k)]}")
    return vet(N2, lines)


def fin_002(i: int, j: int, k: int) -> list[str]:
    snack = L1_002[i]
    lieu = L2_002[j]
    jeu = L3_002[k]
    return vet(
        N2,
        [
            f"narrateur|{IMG_002[(i, j, k)]}",
            f"narrateur|Amir a mangé {snack['lab']}, au parc.",
            f"narrateur|Puis il est allé {lieu['ou']}.",
            f"narrateur|Il a pris {jeu['lab']}.",
            "enfant-m|Le banc était pour s'asseoir.",
            "maman|Oui.",
            "maman|La feuille est sous le platane.",
            "papa|Merci, Amir.",
            f"narrateur|{FIN_IMG_002[(i, j, k)]}",
            "narrateur|Le sac de goûter ne pèse plus.",
        ],
    )


def build_002() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N2,
        [
            "narrateur|Le banc de fer est encore mouillé.",
            "narrateur|Une grande feuille de platane y colle.",
            "narrateur|Elle brille, toute plate.",
            "narrateur|Une flaque tremble au pied du banc.",
            "narrateur|Un oiseau picore près de l'eau.",
            "narrateur|Le sac de goûter est tiède contre la hanche.",
            "narrateur|Ça sent le pain, tout doux.",
            "narrateur|La peinture verte du banc s'écaille un peu.",
            "maman|Tu as tes mains au chaud, Amir ?",
            "enfant-m|Un peu.",
            "enfant-m|Je veux m'asseoir.",
            "enfant-m|Avec toi.",
            "maman|Le banc est mouillé, tu vois ?",
            "narrateur|En ce moment, Amir touche la feuille.",
            "narrateur|Elle est froide, un peu lourde.",
            "papa|On la pose sous l'arbre ?",
            "enfant-m|Oui.",
            "narrateur|Amir soulève la feuille.",
            "narrateur|Il la pose sur la terre, sous le platane.",
            "maman|Merci.",
            "maman|Il y a de la place, maintenant.",
            "narrateur|Papa essuie le bois avec le torchon du sac.",
            "enfant-m|On peut s'asseoir ?",
            "papa|Oui.",
            "papa|Viens.",
        ],
    )
    sons["CHK_T0000_P0000"] = "enfants_parc"

    s["CHK_T0001_P0000"] = vet(
        N2,
        [
            "maman|Amir, tu prends quoi, dans le sac ?",
            "narrateur|Une pomme.",
            "narrateur|Un yaourt.",
            "narrateur|Ou un morceau de pain.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("une pomme", "un yaourt", "un morceau de pain")

    q_extra = {
        1: qf("sac", "sac | le sac | dans le sac | pelure", "La pelure. Amir l'a mise où ?"),
        2: qf("sac", "sac | le sac | dans le sac | couvercle", "Le couvercle. Amir l'a mis où ?"),
        3: qf(
            "terre",
            "terre | la terre | sous l'arbre | sous le platane | oiseau",
            "La terre, sous l'arbre. Amir l'a mise où ?",
        ),
    }

    for i, snack in L1_002.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_002[i]
        sons[p] = snack["son"]
        s[f"{p}_Q0001"] = Q_002[i]
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = C_002[i]
        s[f"{p}_T0002_P0000"] = vet(
            N2,
            [
                "maman|On rentre où, après le banc ?",
                "narrateur|La cuisine.",
                "narrateur|Le jardin.",
                "narrateur|Ou la chambre.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("la cuisine", "le jardin", "la chambre")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = vet(
                N2,
                list(HOME_002[j])
                + list(SNACK_REST_002[i])
                + [
                    "papa|On joue avec quoi, un moment ?",
                ],
            )
            sons[p2] = L2_002[j]["son"]
            s[f"{p2}_T0003_P0000"] = vet(
                N2,
                [
                    f"narrateur|Amir est {L2_002[j]['ou']}, après {snack['lab']}.",
                    "papa|Les cubes, le livre, ou la dînette ?",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("les cubes", "le livre", "la dînette")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_002(i, j, k)
                s[f"{p3}_F0001"] = fin_002(i, j, k)
    return s, sons, extras


def main() -> None:
    s48, n48, e48 = build_048()
    write_tree(
        "TREE-AUT-048",
        "Nina veut les ronds de la flaque dans son seau rouge. "
        "Le lampadaire goutte sur le chemin. L'anse est en corde. "
        "Le manteau gris sèche sur la pierre. Au moment de rentrer, "
        "elle reprend le seau et le manteau. Banc, portail ou haie : la suite change.",
        "Le seau rouge de Nina près de la flaque",
        "Nina, papa, maman",
        "parc après la pluie, lampadaire, flaque du chemin, banc de pierre",
        s48,
        n48,
        e48,
    )
    relecture(
        "TREE-AUT-048",
        "Le seau rouge de Nina près de la flaque",
        "Nina veut les ronds du lampadaire dans le seau rouge. "
        "Anse en corde, banc de pierre, mousse, manteau gris. "
        "Bac / toboggan / balançoires, puis ballon / seau / doudou, "
        "puis banc / portail / haie. Elle reprend seau et manteau pour une raison vécue.",
        "Nina déjà D16. N1 ≤10. AUT.AFF.003 implicite. "
        "Seau rouge ≠ jaune 008/011/033, ≠ vert 028, ≠ sous la table 038, "
        "≠ fontaine 025, ≠ kiosque 033. T3 = banc/portail/haie. "
        "Questions = seau / manteau / doudou (branches distinctes). "
        "Fin = dernier rond, pas « L'histoire est finie ».",
    )

    s02, n02, e02 = build_002()
    write_tree(
        "TREE-COL-002",
        "Amir veut s'asseoir sur le banc de fer, avec maman, et manger. "
        "Une feuille de platane colle au bois mouillé. Il la pose sous l'arbre. "
        "Pelure, couvercle ou miette : il garde le banc libre. "
        "Cuisine, jardin ou chambre, puis cubes, livre ou dînette : la suite change.",
        "Le banc mouillé d'Amir",
        "Amir, papa, maman",
        "parc, banc de fer, platane, flaque, sac de goûter, puis la maison",
        s02,
        n02,
        e02,
    )
    relecture(
        "TREE-COL-002",
        "Le banc mouillé d'Amir",
        "Amir veut s'asseoir et manger. Feuille de platane, banc de fer, "
        "peinture écaillée, sac tiède. Pomme / yaourt / pain, puis "
        "cuisine / jardin / chambre, puis cubes / livre / dînette. "
        "La feuille va sous l'arbre. Le reste du goûter ne reste pas sur le banc.",
        "Hugo→Amir (D16). N2. COL.ECO.001 implicite (partage du banc, "
        "feuille à la terre, pas de lecture poubelle). "
        "Monde ≠ COL-001 pommes, ≠ COL-023 banc bois pommier, "
        "≠ COL-033 galet malaise, ≠ COL-014 gant. "
        "Questions = sac / sac / terre. Fin sensorielle, pas « L'histoire est finie ».",
    )


if __name__ == "__main__":
    main()
