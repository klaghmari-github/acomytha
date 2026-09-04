#!/usr/bin/env python3
"""TREE-AUT-030 / TREE-AUT-031 — récit implicite, graphe 86, D16."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture

# ---------------------------------------------------------------------------
# Commun
# ---------------------------------------------------------------------------


def extras_opts(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def extras_q(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


def write_tree(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    extras: dict,
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} chunks missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
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
        for bad in ("tom", "léa", "lea", "sami", "jules", "noé", "noe"):
            blob = c["script"].lower()
            if bad in blob:
                raise SystemExit(f"{sid} prénom hors troupe dans fin: {bad}")
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# TREE-AUT-030  N2  Raphaël  AUT.ROU.001
# Bouilloire, rideau à bateaux. Séquence vécue, pas de refrain d'étapes.
# T3 : le banc / le portail / le manteau (plus Tom Léa Sami).
# ---------------------------------------------------------------------------

L1_030 = {
    1: {"lab": "le bac à sable", "ici": "le bac à sable", "ou": "au bac à sable"},
    2: {"lab": "le toboggan", "ici": "le toboggan", "ou": "au toboggan"},
    3: {"lab": "les balançoires", "ici": "les balançoires", "ou": "aux balançoires"},
}
L2_030 = {
    1: {"lab": "le ballon", "obj": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou"},
}
L3_030 = {
    1: {"lab": "le banc", "quoi": "le banc"},
    2: {"lab": "le portail", "quoi": "le portail"},
    3: {"lab": "le manteau", "quoi": "le manteau"},
}

ARRIVE_030 = {
    1: [
        "narrateur|Raphaël s'agenouille près du bac.",
        "narrateur|Le sable est frais, un peu humide.",
        "narrateur|Il coule entre ses doigts.",
        "narrateur|Une petite pelle attend, toute jaune.",
        "enfant-m|Un port, papa.",
        "papa|D'abord le sable, tout doux.",
        "narrateur|Raphaël creuse un creux rond.",
        "narrateur|Il pose un bateau bleu dedans.",
        "maman|Le jaune, ensuite ?",
        "enfant-m|Il attend dans la poche.",
        "narrateur|Le tas a une ombre, toute courte.",
        "papa|Tu as les deux bateaux ?",
        "enfant-m|Un ici.",
        "enfant-m|Un dans la poche.",
        "narrateur|Loin, un vélo de boulanger passe.",
        "narrateur|On entend un petit grelot.",
    ],
    2: [
        "narrateur|Le toboggan brille, encore un peu froid.",
        "narrateur|Les marches font toc sous la main.",
        "enfant-m|Le bateau glisse avec moi.",
        "papa|J'attends en bas.",
        "narrateur|Raphaël glisse le bateau bleu.",
        "narrateur|Sur la rampe, le papier fait frou.",
        "maman|Ensuite toi.",
        "narrateur|Raphaël glisse.",
        "narrateur|Ça fait houuu, tout doux.",
        "enfant-m|Il est arrivé.",
        "papa|Le jaune est encore dans la poche ?",
        "enfant-m|Oui.",
        "narrateur|Une feuille colle sur la rampe.",
        "maman|Tes joues sont déjà roses.",
        "narrateur|Raphaël reprend le bateau bleu.",
        "narrateur|Il le glisse contre l'autre.",
    ],
    3: [
        "narrateur|Les chaînes des balançoires sont froides.",
        "narrateur|Elles font un bruit de goutte.",
        "narrateur|Raphaël s'assoit.",
        "narrateur|Le siège est lisse, un peu froid.",
        "maman|Je pousse tout doux.",
        "enfant-m|Les bateaux voyagent.",
        "narrateur|Le bleu est sur ses genoux.",
        "narrateur|Le jaune reste dans la poche.",
        "papa|Ils ne tombent pas.",
        "enfant-m|Je les tiens.",
        "narrateur|Un oiseau passe au-dessus.",
        "maman|Encore une fois ?",
        "enfant-m|Encore.",
        "papa|Une dernière, d'accord.",
        "narrateur|La chaîne fait cling, puis se tait.",
        "narrateur|Raphaël pose un pied au sol.",
    ],
}

Q_030 = {
    1: [
        "narrateur|Raphaël a un bateau dans le sable.",
        "papa|Il s'est préparé comment, ce matin ?",
    ],
    2: [
        "narrateur|Le bateau a glissé sur la rampe.",
        "maman|Raphaël s'est préparé comment ?",
    ],
    3: [
        "narrateur|Les bateaux tiennent sur ses genoux.",
        "papa|Il s'est préparé comment, Raphaël ?",
    ],
}

C_030 = {
    1: [
        "narrateur|Oui.",
        "narrateur|D'abord la chaussette chaude.",
        "narrateur|Ensuite les bateaux dans la poche.",
        "papa|Merci, Raphaël.",
        "maman|La bouilloire a attendu, elle aussi.",
        "enfant-m|On continue ?",
        "papa|On prend un jeu, près du bac ?",
        "narrateur|Un grain de sable brille sur son genou.",
    ],
    2: [
        "narrateur|Oui.",
        "narrateur|D'abord la chaussette.",
        "narrateur|Ensuite les bateaux.",
        "maman|Merci, Raphaël.",
        "papa|Le sifflet s'est tu, à la maison.",
        "enfant-m|On continue ?",
        "maman|On prend un jeu, près de la rampe ?",
        "narrateur|La feuille reste sur le métal.",
    ],
    3: [
        "narrateur|Oui.",
        "narrateur|La chaussette d'abord.",
        "narrateur|Les bateaux ensuite.",
        "papa|Merci, Raphaël.",
        "maman|Une chose, puis la suivante.",
        "enfant-m|On continue ?",
        "papa|On prend un jeu, près des chaînes ?",
        "narrateur|La chaîne ne fait plus cling.",
    ],
}

PLAY_030 = {
    (1, 1): [
        "narrateur|Près du bac, le ballon rouge attend.",
        "narrateur|Il est lisse, un peu frais.",
        "enfant-m|Le ballon, papa.",
        "papa|D'abord le tenir.",
        "papa|Ensuite rouler, tout près.",
        "narrateur|Raphaël pose les deux mains dessus.",
        "narrateur|Le ballon fait un petit bruit de peau.",
        "maman|Le bateau reste au port ?",
        "enfant-m|Oui, dans le creux.",
        "narrateur|Le sable colle un peu aux chaussures.",
    ],
    (1, 2): [
        "narrateur|Près du bac, le seau jaune sonne.",
        "narrateur|L'anse est un peu froide.",
        "enfant-m|Un vrai port, maman.",
        "maman|Le seau, d'abord.",
        "narrateur|Raphaël pose le seau près du creux.",
        "narrateur|Il glisse le bateau bleu au fond.",
        "papa|Le jaune, ensuite ?",
        "enfant-m|Il rentre aussi.",
        "narrateur|Les deux bateaux se touchent, tout doux.",
        "maman|L'eau de sable fait chh.",
    ],
    (1, 3): [
        "narrateur|Près du bac, le doudou gris attend.",
        "narrateur|Une oreille a un peu de sable.",
        "enfant-m|Il garde le port.",
        "papa|D'abord le doudou, contre toi.",
        "narrateur|Raphaël le serre.",
        "maman|Ensuite le bateau, contre lui.",
        "narrateur|Le papier bleu frotte le tissu.",
        "enfant-m|Ils se parlent.",
        "papa|Tout doux, oui.",
        "narrateur|Un grain reste sous son ongle.",
    ],
    (2, 1): [
        "narrateur|Au pied du toboggan, le ballon attend.",
        "narrateur|Il est un peu froid, près de la rampe.",
        "enfant-m|Il glisse aussi ?",
        "papa|D'abord tes mains dessus.",
        "narrateur|Raphaël le tient.",
        "maman|Ensuite un tout petit bond.",
        "narrateur|Le ballon fait un bond mou.",
        "enfant-m|Les bateaux regardent.",
        "papa|Ils restent dans la poche.",
        "narrateur|Une feuille tourne près des pieds.",
    ],
    (2, 2): [
        "narrateur|Au toboggan, le seau sonne contre une marche.",
        "narrateur|L'anse est froide, encore.",
        "enfant-m|Le bateau rentre là.",
        "maman|D'abord le seau, droit.",
        "narrateur|Raphaël le pose au pied.",
        "papa|Ensuite le bateau, au fond.",
        "narrateur|Le papier fait toc, tout creux.",
        "enfant-m|C'est sa gare.",
        "maman|La rampe sèche au soleil.",
        "narrateur|Une goutte glisse encore, tout lente.",
    ],
    (2, 3): [
        "narrateur|Au toboggan, le doudou a vu la rampe.",
        "narrateur|L'oreille grise est un peu froide.",
        "enfant-m|Il a glissé des yeux.",
        "papa|D'abord le doudou, dans tes bras.",
        "narrateur|Raphaël le serre.",
        "maman|Ensuite le bateau, contre lui.",
        "narrateur|Le papier jaune dépasse de la poche.",
        "enfant-m|Ils sont ensemble.",
        "papa|Oui.",
        "narrateur|Le métal se tait, tout doux.",
    ],
    (3, 1): [
        "narrateur|Près des chaînes, le ballon a de l'herbe.",
        "narrateur|Un brin colle au cuir.",
        "enfant-m|On roule tout près.",
        "maman|D'abord le tenir.",
        "narrateur|Raphaël pose le ballon au sol.",
        "papa|Ensuite un tout petit coup.",
        "narrateur|Le ballon avance, puis s'arrête.",
        "enfant-m|Les bateaux n'ont pas bougé.",
        "maman|Ils sont sur tes genoux, encore.",
        "narrateur|La chaîne fait un cling lointain.",
    ],
    (3, 2): [
        "narrateur|Près des balançoires, le seau est dans l'herbe.",
        "narrateur|L'anse est froide, près de la corde.",
        "enfant-m|Le bateau va au port.",
        "papa|D'abord le seau, droit.",
        "narrateur|Raphaël le pose sous le banc.",
        "maman|Ensuite le bateau, au fond.",
        "narrateur|Le papier bleu disparaît.",
        "enfant-m|Il est à l'abri.",
        "papa|L'herbe mouille le bord, un peu.",
        "narrateur|Une flaque tremble près du pied.",
    ],
    (3, 3): [
        "narrateur|Près des balançoires, le doudou a du vent.",
        "narrateur|L'oreille molle clignote.",
        "enfant-m|Il s'assoit avec moi.",
        "maman|D'abord le doudou, sur tes genoux.",
        "narrateur|Raphaël l'installe.",
        "papa|Ensuite le bateau, contre lui.",
        "narrateur|Le papier jaune ne tombe pas.",
        "enfant-m|Ils voyagent encore.",
        "maman|Une dernière poussée, tout douce.",
        "narrateur|La corde se tait.",
    ],
}

STEP_030 = {
    1: [
        "narrateur|Ils vont vers le banc de bois.",
        "narrateur|Le bois est un peu froid.",
        "enfant-m|Je m'assois.",
        "maman|D'abord le banc.",
        "papa|Le gobelet est encore tiède.",
        "narrateur|C'est l'eau de la bouilloire.",
        "narrateur|Raphaël pose un bateau sur le bois.",
        "enfant-m|Il attend.",
        "maman|Ensuite on rentre.",
        "papa|Oui, tout doux.",
    ],
    2: [
        "narrateur|Ils marchent vers le portail.",
        "narrateur|Le métal est froid sous la main.",
        "enfant-m|J'ouvre ?",
        "papa|On attend une seconde.",
        "narrateur|Un vélo passe, tout loin.",
        "maman|Maintenant, tu pousses.",
        "narrateur|Raphaël pousse le portail.",
        "narrateur|Les bateaux restent dans sa poche.",
        "enfant-m|On rentre.",
        "papa|Oui.",
    ],
    3: [
        "narrateur|Le manteau attend sur le crochet du parc.",
        "narrateur|Il est un peu frais.",
        "enfant-m|Je le mets.",
        "maman|Une manche, puis l'autre.",
        "narrateur|Raphaël glisse un bras.",
        "narrateur|Puis l'autre bras.",
        "papa|Les bateaux restent dans la poche.",
        "enfant-m|Ils sont au chaud.",
        "maman|On rentre, maintenant.",
        "papa|Oui.",
    ],
}

EXTRA_030 = {
    (1, 1, 1): "Un grain de sable colle au bateau, sur le banc.",
    (1, 1, 2): "Le ballon reste rond, près du portail.",
    (1, 1, 3): "Le sable brille encore sur la manche.",
    (1, 2, 1): "L'anse du seau touche le bois du banc.",
    (1, 2, 2): "Le seau sonne tout doux, près du portail.",
    (1, 2, 3): "Un peu d'eau de sable tache le manteau.",
    (1, 3, 1): "L'oreille grise dépasse sur le banc.",
    (1, 3, 2): "Le doudou sent le sable, près du portail.",
    (1, 3, 3): "Un fil gris pend de la poche du manteau.",
    (2, 1, 1): "Le ballon est un peu froid, contre le banc.",
    (2, 1, 2): "Une feuille de la rampe va vers le portail.",
    (2, 1, 3): "La rampe se tait, loin du manteau.",
    (2, 2, 1): "Le seau pose son ombre sur le banc.",
    (2, 2, 2): "L'anse cliquette près du portail.",
    (2, 2, 3): "Une goutte de la rampe touche le manteau.",
    (2, 3, 1): "Le doudou a vu le toboggan, sur le banc.",
    (2, 3, 2): "L'oreille molle dépasse, près du portail.",
    (2, 3, 3): "Le papier jaune chauffe dans la poche.",
    (3, 1, 1): "Un cling lointain, et le banc.",
    (3, 1, 2): "Le ballon a de l'herbe, près du portail.",
    (3, 1, 3): "Un nuage passe au-dessus du manteau.",
    (3, 2, 1): "L'anse froide repose sur le banc.",
    (3, 2, 2): "La flaque tremble encore, près du portail.",
    (3, 2, 3): "Le seau laisse une ombre sur le manteau.",
    (3, 3, 1): "Le doudou a senti le vent, sur le banc.",
    (3, 3, 2): "La chaîne se tait, près du portail.",
    (3, 3, 3): "L'oreille grise dépasse du manteau.",
}

FIN_030 = {
    (1, 1, 1): "Le gobelet sèche près de la bouilloire.",
    (1, 1, 2): "Le rideau à bateaux ne bouge plus.",
    (1, 1, 3): "La chaussette reprend la chaise, toute tiède.",
    (1, 2, 1): "Un bateau bleu repose dans le seau, à la maison.",
    (1, 2, 2): "Le sifflet de la bouilloire reste muet.",
    (1, 2, 3): "Le savon du couloir sent encore.",
    (1, 3, 1): "Le doudou s'endort près des bateaux.",
    (1, 3, 2): "Un pois rouge du tapis redevient calme.",
    (1, 3, 3): "Le manteau goutte, tout doux, au crochet.",
    (2, 1, 1): "Le ballon s'endort près du tapis à pois.",
    (2, 1, 2): "La rampe du toboggan reste loin, maintenant.",
    (2, 1, 3): "Une feuille sèche près des clés de papa.",
    (2, 2, 1): "Le seau penche un peu, sous le portemanteau.",
    (2, 2, 2): "Les bateaux sèchent sur le rebord.",
    (2, 2, 3): "Le gobelet attend encore près du lavabo.",
    (2, 3, 1): "L'oreille du doudou dépasse du fauteuil.",
    (2, 3, 2): "Le papier jaune n'est plus froissé.",
    (2, 3, 3): "La bouilloire est froide, tout à fait.",
    (3, 1, 1): "Le ballon a cessé de rouler, au salon.",
    (3, 1, 2): "Un bateau bleu regarde le bateau du rideau.",
    (3, 1, 3): "Le crochet du manteau fait un petit toc.",
    (3, 2, 1): "Le seau pose son ombre sur le tapis.",
    (3, 2, 2): "Le portail du parc reste loin, fermé.",
    (3, 2, 3): "Ça sent encore le savon, dans le couloir.",
    (3, 3, 1): "Le doudou a l'odeur de l'herbe, au salon.",
    (3, 3, 2): "Les deux bateaux se touchent, sur la chaise.",
    (3, 3, 3): "La bouilloire ne chante plus.",
}


def trans_l2_030(i: int) -> list[str]:
    loc = L1_030[i]
    return [
        f"narrateur|Raphaël peut encore jouer, {loc['ou']}.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|On prend un jeu.",
    ]


def trans_l3_030(i: int) -> list[str]:
    loc = L1_030[i]
    return [
        f"narrateur|Le matin peut encore avancer, {loc['ou']}.",
        "maman|Le banc, le portail, ou le manteau ?",
        "papa|On fait la suivante.",
    ]


def body_030(i: int, j: int, k: int) -> list[str]:
    loc = L1_030[i]
    jeu = L2_030[j]
    lines = [
        f"narrateur|Raphaël quitte {loc['ici']}.",
        f"narrateur|Il a {jeu['obj']} avec lui.",
        "narrateur|Les bateaux voyagent encore.",
    ]
    lines.extend(STEP_030[k])
    lines.append(f"narrateur|{EXTRA_030[(i, j, k)]}")
    return lines


def fin_030(i: int, j: int, k: int) -> list[str]:
    loc = L1_030[i]
    jeu = L2_030[j]
    step = L3_030[k]
    return [
        f"narrateur|{EXTRA_030[(i, j, k)]}",
        f"narrateur|Raphaël a joué {loc['ou']}.",
        f"narrateur|Il a pris {jeu['lab']}.",
        f"narrateur|Puis {step['lab']}.",
        "narrateur|Les bateaux rentrent dans la poche.",
        "enfant-m|La bouilloire s'est tue.",
        "maman|Oui.",
        "papa|Merci, Raphaël.",
        "narrateur|Le rideau à bateaux ne bouge plus.",
        f"narrateur|{FIN_030[(i, j, k)]}",
    ]


def build_030() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|La bouilloire chante dans le salon.",
        "narrateur|Elle fait siff, tout aigu.",
        "narrateur|Un rideau à petits bateaux bouge.",
        "narrateur|Un bateau est bleu.",
        "narrateur|Un bateau est jaune.",
        "narrateur|Sur la chaise, une chaussette pend.",
        "narrateur|Elle est encore un peu chaude.",
        "narrateur|Le couloir sent le savon.",
        "narrateur|Un gobelet attend près du lavabo.",
        "papa|L'eau n'est pas prête, Raphaël.",
        "maman|Le sifflet va s'arrêter.",
        "narrateur|Le tapis du salon a des pois.",
        "narrateur|Un pois rouge.",
        "narrateur|Un pois vert.",
        "narrateur|Deux bateaux de papier attendent.",
        "narrateur|Ils sont sur le rebord, un peu froissés.",
        "narrateur|En ce moment, Raphaël a les pieds sur le tapis.",
        "enfant-m|Je veux les bateaux au parc.",
        "papa|D'accord.",
        "narrateur|Raphaël prend les bateaux.",
        "narrateur|Il prend aussi une chaussure.",
        "narrateur|Un bateau glisse sous la chaise.",
        "enfant-m|Oh.",
        "maman|Pose la chaussure, d'abord.",
        "narrateur|Raphaël pose la chaussure.",
        "narrateur|Il cherche le bateau du bout des doigts.",
        "narrateur|Le papier est un peu froissé.",
        "enfant-m|Je l'ai.",
        "papa|La bouilloire s'arrête.",
        "narrateur|Le sifflet se tait.",
        "maman|L'eau est prête, maintenant.",
        "narrateur|Raphaël enfile la chaussette chaude.",
        "narrateur|Il glisse les bateaux dans sa poche.",
        "enfant-m|On y va ?",
        "papa|Oui.",
        "narrateur|Le manteau attend sur le crochet.",
    ]
    sons["CHK_T0000_P0000"] = "bouilloire"
    s["CHK_T0001_P0000"] = [
        "narrateur|Ils arrivent au parc.",
        "papa|Le bac à sable, le toboggan, ou les balançoires ?",
        "maman|Tu choisis.",
    ]
    extras["CHK_T0001_P0000"] = extras_opts("le bac à sable", "le toboggan", "les balançoires")
    sons["CHK_T0001_P0000"] = "enfants_parc"
    qf = extras_q(
        "une chose",
        "une chose | puis l'autre | d'abord | ensuite | une chose puis l'autre | puis la suivante | la chaussette | les bateaux",
        "Il a fait une chose, puis la suivante. Comment s'est préparé Raphaël ?",
    )
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_030[i]
        sons[p] = "enfants_parc"
        s[f"{p}_Q0001"] = Q_030[i]
        extras[f"{p}_Q0001"] = qf
        s[f"{p}_C0001"] = C_030[i]
        s[f"{p}_T0002_P0000"] = trans_l2_030(i)
        extras[f"{p}_T0002_P0000"] = extras_opts("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_030[(i, j)]
            sons[p2] = "enfants_parc"
            s[f"{p2}_T0003_P0000"] = trans_l3_030(i)
            extras[f"{p2}_T0003_P0000"] = extras_opts("le banc", "le portail", "le manteau")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_030(i, j, k)
                s[f"{p3}_F0001"] = fin_030(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-031  N2  Aniss  AUT.AFF.001
# Sac vert sur le banc. Désir d'y aller. Un creux dans le sac, pas une liste.
# T3 : la casquette / la gourde / le goûter (plus Tom Léa Sami).
# ---------------------------------------------------------------------------

L1_031 = {
    1: {"lab": "le bac à sable", "ici": "le bac à sable", "ou": "au bac à sable"},
    2: {"lab": "le toboggan", "ici": "le toboggan", "ou": "au toboggan"},
    3: {"lab": "les balançoires", "ici": "les balançoires", "ou": "aux balançoires"},
}
L2_031 = {
    1: {"lab": "le ballon", "obj": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou"},
}
L3_031 = {
    1: {"lab": "la casquette", "quoi": "la casquette"},
    2: {"lab": "la gourde", "quoi": "la gourde"},
    3: {"lab": "le goûter", "quoi": "le goûter"},
}

ARRIVE_031 = {
    1: [
        "narrateur|Aniss marche vers le bac à sable.",
        "narrateur|Le sable est jaune, tout fin.",
        "narrateur|Il colle un peu aux doigts.",
        "enfant-m|Maman, le sable est doux ?",
        "maman|Oui.",
        "maman|Il est doux et un peu frais.",
        "narrateur|Le sac vert est posé contre le bois.",
        "papa|Il est encore un peu léger, tu sens ?",
        "enfant-m|Oui.",
        "enfant-m|Il y a un creux.",
        "narrateur|Aniss ouvre un peu le sac.",
        "narrateur|Le doudou est déjà dedans, tiède.",
        "enfant-m|Il sent le savon.",
        "maman|Il a quitté le panier.",
        "narrateur|Un grain de sable brille sur la sangle.",
        "papa|Le sac reste près de nous.",
    ],
    2: [
        "narrateur|Aniss marche vers le toboggan.",
        "narrateur|Le plastique lisse brille un peu.",
        "narrateur|Les marches sont tièdes sous la main.",
        "narrateur|Le sac vert est au pied du toboggan.",
        "papa|On garde le sac près de nous.",
        "maman|Il pèse encore trop peu.",
        "narrateur|Aniss ouvre le sac.",
        "narrateur|Il sent le doudou à travers le tissu.",
        "enfant-m|Il est au chaud.",
        "papa|Il a quitté le linge.",
        "narrateur|Une feuille sèche tourne sur le sol.",
        "enfant-m|Je glisse après.",
        "maman|D'accord.",
        "narrateur|La boucle jaune fait un petit clic.",
        "papa|Le sac ne part pas.",
        "narrateur|Ça sent l'herbe coupée.",
    ],
    3: [
        "narrateur|Aniss marche vers les balançoires.",
        "narrateur|Les chaînes font un petit clin clin.",
        "narrateur|Le siège en bois est lisse.",
        "narrateur|Le sac vert est posé dans l'herbe.",
        "maman|On met le sac ici, à côté.",
        "papa|Il est encore léger.",
        "narrateur|Aniss touche la sangle lisse.",
        "narrateur|Il sent le doudou à travers le tissu.",
        "enfant-m|Le sac est avec nous.",
        "maman|Oui.",
        "maman|On reste ensemble.",
        "narrateur|Au loin, un vélo passe tout doux.",
        "narrateur|L'air est frais sur les joues.",
        "enfant-m|Je m'assois.",
        "papa|Le creux du sac attend encore.",
        "narrateur|Une goutte d'une botte a séché, déjà.",
    ],
}

Q_031 = {
    1: [
        "narrateur|Le sac vert est trop léger, contre le bac.",
        "maman|Aniss met où le doudou ?",
    ],
    2: [
        "narrateur|Le sac est au pied du toboggan.",
        "papa|Aniss met où les affaires ?",
    ],
    3: [
        "narrateur|Le sac est dans l'herbe.",
        "maman|Aniss met où le doudou ?",
    ],
}

C_031 = {
    1: [
        "narrateur|Aniss glisse le doudou au fond.",
        "narrateur|Le sac devient un peu plus lourd.",
        "enfant-m|Il n'est plus vide.",
        "maman|Merci, Aniss.",
        "papa|On continue.",
        "papa|Le sac reste avec nous.",
        "narrateur|Aniss respire.",
        "narrateur|Le sable est froid sous ses mains.",
    ],
    2: [
        "narrateur|Aniss appuie sur la boucle.",
        "narrateur|Ça fait clic, tout petit.",
        "enfant-m|Le sac est avec nous.",
        "papa|Merci, Aniss.",
        "maman|On peut jouer un peu.",
        "narrateur|Aniss pose la main sur la sangle.",
        "narrateur|L'herbe sent encore la pluie.",
    ],
    3: [
        "narrateur|Aniss pose le sac dans l'herbe sèche.",
        "narrateur|La sangle reste près de sa main.",
        "enfant-m|Il ne part pas.",
        "maman|Merci, Aniss.",
        "papa|On reste ensemble.",
        "narrateur|Une chaîne fait clin, tout doux.",
        "narrateur|Le vent touche encore ses joues.",
    ],
}

PLAY_031 = {
    (1, 1): [
        "narrateur|Aniss a choisi le ballon.",
        "narrateur|Il est rouge, un peu poussiéreux.",
        "narrateur|Il sent le caoutchouc chaud.",
        "papa|Il reste près du sac ?",
        "enfant-m|Oui.",
        "enfant-m|Il rebondit tout doux.",
        "narrateur|Le sac vert reste contre le bois.",
        "maman|Le doudou est dedans, lui.",
        "enfant-m|Il attend.",
        "narrateur|Un grain de sable colle au cuir.",
    ],
    (1, 2): [
        "narrateur|Aniss a choisi le seau.",
        "narrateur|Il est jaune.",
        "narrateur|L'anse est un peu rêche.",
        "narrateur|Il y a du sable au fond, tout fin.",
        "papa|Tu le laisses au bac ?",
        "enfant-m|Il reste près du sac.",
        "maman|L'anse dépasse un tout petit peu.",
        "narrateur|Aniss verse, puis s'arrête.",
        "enfant-m|Le château est petit.",
        "narrateur|Un vélo passe au loin, tout léger.",
    ],
    (1, 3): [
        "narrateur|Aniss a choisi le doudou.",
        "narrateur|Il le sort du sac, tout doux.",
        "narrateur|Le tissu sent encore le savon.",
        "maman|Il a pris le linge, tout à l'heure.",
        "enfant-m|Il sèche dehors.",
        "papa|Le tissu sent la maison.",
        "enfant-m|Mon doudou est avec moi.",
        "narrateur|La lumière est claire sur le tissu vert.",
        "maman|On souffle un peu.",
        "narrateur|Puis le sac attend, contre le bois.",
    ],
    (2, 1): [
        "narrateur|Aniss a choisi le ballon, près du toboggan.",
        "narrateur|Il rebondit une fois, tout mou.",
        "maman|Il va rouler sous la rampe ?",
        "enfant-m|Non.",
        "narrateur|Aniss le prend à deux mains.",
        "papa|Il reste près du sac.",
        "enfant-m|Le ballon est avec nous.",
        "narrateur|Le sac vert ne bouge pas.",
        "narrateur|Il y a des miettes sur une table basse.",
        "maman|On joue ici, tout près.",
    ],
    (2, 2): [
        "narrateur|Aniss a choisi le seau, au pied du toboggan.",
        "narrateur|Un oiseau chante une fois, tout près.",
        "papa|Le seau va rester ici ?",
        "enfant-m|Près du sac.",
        "narrateur|Aniss le pose droit.",
        "maman|L'anse cliquette.",
        "enfant-m|J'ai un château plus tard.",
        "papa|D'accord.",
        "narrateur|Aniss rit un peu.",
        "narrateur|Le toboggan brille encore.",
    ],
    (2, 3): [
        "narrateur|Aniss a choisi le doudou, près des marches.",
        "narrateur|Les chaussures font toc toc sur le métal.",
        "maman|Il va rester sur la rampe ?",
        "enfant-m|Non.",
        "narrateur|Aniss le serre, puis le repose.",
        "papa|Il est au chaud, près du sac.",
        "enfant-m|Oui.",
        "narrateur|Aniss souffle.",
        "narrateur|Le toboggan brille encore.",
        "maman|Il manque encore une chose, plus tard.",
    ],
    (3, 1): [
        "narrateur|Aniss a choisi le ballon, près des chaînes.",
        "narrateur|Il fait un petit bond dans l'herbe.",
        "papa|Il va sous la balançoire ?",
        "enfant-m|Non.",
        "narrateur|Aniss le rattrape.",
        "maman|Le sac reste dans l'herbe.",
        "enfant-m|Il est avec moi.",
        "narrateur|Une chaîne fait clin, tout près.",
        "papa|Le vent ne l'emporte plus.",
        "narrateur|Un brin d'herbe colle au cuir.",
    ],
    (3, 2): [
        "narrateur|Aniss a choisi le seau, sous le banc.",
        "narrateur|L'anse est froide, encore.",
        "maman|Il reste sous le banc ?",
        "enfant-m|Non.",
        "narrateur|Aniss le pose près du sac, tout droit.",
        "papa|L'anse dépasse un peu.",
        "enfant-m|Je la rentre.",
        "narrateur|Aniss rentre l'anse.",
        "maman|Le sac tient mieux, à côté.",
        "narrateur|L'herbe est encore un peu mouillée.",
    ],
    (3, 3): [
        "narrateur|Aniss a choisi le doudou, sur le siège.",
        "narrateur|Il a pris un peu de vent.",
        "papa|Il reste sur la balançoire ?",
        "enfant-m|Non.",
        "narrateur|Aniss le serre, puis le pose au sac.",
        "maman|Il se réchauffe.",
        "enfant-m|Oui, contre moi.",
        "narrateur|Le bois du siège est chaud, vide maintenant.",
        "papa|Le sac est un peu plus lourd.",
        "narrateur|Le vent passe encore dans ses cheveux.",
    ],
}

NEED_031 = {
    1: [
        "narrateur|Le soleil tape sur les yeux d'Aniss.",
        "enfant-m|Ça pique.",
        "narrateur|Il fouille le sac vert.",
        "narrateur|La casquette n'est pas là.",
        "papa|Elle était sur le banc.",
        "narrateur|Papa la sort de sa poche.",
        "narrateur|Elle sent encore le savon.",
        "enfant-m|Je la mets dans le sac.",
        "narrateur|Aniss la glisse, puis la met.",
        "maman|L'ombre vient avec nous.",
    ],
    2: [
        "narrateur|Aniss a la bouche sèche.",
        "enfant-m|J'ai soif.",
        "narrateur|Il ouvre le sac vert.",
        "narrateur|La gourde n'est pas là.",
        "maman|Elle était près des bottes.",
        "narrateur|Papa la sort de sa poche.",
        "narrateur|L'eau chante un peu dedans.",
        "enfant-m|Je la mets dans le sac.",
        "narrateur|Aniss la glisse au fond.",
        "papa|L'eau va avec nous.",
    ],
    3: [
        "narrateur|Le vent apporte une odeur de pomme.",
        "enfant-m|J'ai faim, un peu.",
        "narrateur|Il cherche dans le sac vert.",
        "narrateur|Le goûter n'est pas là.",
        "papa|Il était dans le torchon.",
        "narrateur|Maman tend le linge.",
        "narrateur|Ça sent la pomme douce.",
        "enfant-m|Je le mets dans le sac.",
        "narrateur|Aniss le pose près du doudou.",
        "maman|La pomme va avec nous.",
    ],
}

MARK_031 = {
    1: "narrateur|Le ballon fait une bosse, tout près.",
    2: "narrateur|L'anse du seau dépasse un tout petit peu.",
    3: "narrateur|Le doudou chauffe le fond du sac.",
}

PLACE_031 = {
    1: [
        "narrateur|Un grain de sable reste collé au sac.",
        "narrateur|Le sable reste froid sous les chaussures.",
    ],
    2: [
        "narrateur|Le toboggan brille encore derrière eux.",
        "narrateur|Ça sent l'herbe coupée.",
    ],
    3: [
        "narrateur|Une chaîne se tait, tout doux.",
        "narrateur|L'herbe est chaude sous le sac.",
    ],
}

IMG_031 = {
    (1, 1, 1): "Un grain de sable reste collé à la visière.",
    (1, 1, 2): "Une fourmi traverse le rebord de bois.",
    (1, 1, 3): "Le vent pousse un peu de poussière claire.",
    (1, 2, 1): "Une feuille sèche tourne près des pieds.",
    (1, 2, 2): "Un oiseau saute sur le grillage.",
    (1, 2, 3): "Le soleil chauffe la sangle verte.",
    (1, 3, 1): "Une flaque reflète le sac ouvert.",
    (1, 3, 2): "Le bois du banc est tout strié.",
    (1, 3, 3): "Un papillon passe, tout jaune.",
    (2, 1, 1): "La terre sent l'eau de la nuit.",
    (2, 1, 2): "Un caillou tapote le seau.",
    (2, 1, 3): "Le toboggan claque tout doux au vent.",
    (2, 2, 1): "Une corde de balançoire craque.",
    (2, 2, 2): "Le sac fait une bosse ronde.",
    (2, 2, 3): "Aniss essuie ses mains à l'herbe.",
    (2, 3, 1): "Papa porte le sac un moment.",
    (2, 3, 2): "Maman ferme la boucle, ça fait clic.",
    (2, 3, 3): "Le chemin du parc sent les pins.",
    (3, 1, 1): "Le ballon a cessé de rebondir.",
    (3, 1, 2): "Une pomme sent encore dans le linge.",
    (3, 1, 3): "La visière fait une petite ombre.",
    (3, 2, 1): "L'eau chante encore dans la gourde.",
    (3, 2, 2): "Le linge du goûter est un peu tiède.",
    (3, 2, 3): "Le soleil touche la visière, dans le sac.",
    (3, 3, 1): "Le doudou a quitté le siège de bois.",
    (3, 3, 2): "Le goûter sent la pomme, contre le doudou.",
    (3, 3, 3): "Le vent n'emporte plus la casquette.",
}

FIN_031 = {
    (1, 1, 1): "La visière sèche près du panier à linge.",
    (1, 1, 2): "Une miette de savon reste sur le banc.",
    (1, 1, 3): "Le bouton de la chemise ne brille plus.",
    (1, 2, 1): "Le seau sèche sous le portemanteau.",
    (1, 2, 2): "Les bottes ont cessé de goutter.",
    (1, 2, 3): "Le marché, dehors, s'est tu.",
    (1, 3, 1): "Le doudou s'installe contre le sac vert.",
    (1, 3, 2): "Le torchon à carreaux reprend l'évier.",
    (1, 3, 3): "La boucle jaune ne fait plus clic.",
    (2, 1, 1): "Le ballon s'endort près des bottes.",
    (2, 1, 2): "La flaque de l'entrée a séché.",
    (2, 1, 3): "Le sac vert retrouve le banc.",
    (2, 2, 1): "L'anse du seau est tiède, maintenant.",
    (2, 2, 2): "Le linge du panier n'est plus chaud.",
    (2, 2, 3): "Une cloche de vélo sonne encore, tout loin.",
    (2, 3, 1): "L'oreille du doudou dépasse du sac.",
    (2, 3, 2): "Ça sent encore le savon, un peu.",
    (2, 3, 3): "La fenêtre de l'entrée est calme.",
    (3, 1, 1): "Le ballon a l'odeur de l'herbe, au banc.",
    (3, 1, 2): "La gourde repose près des bottes.",
    (3, 1, 3): "La casquette reprend le crochet.",
    (3, 2, 1): "L'eau de la gourde est encore fraîche.",
    (3, 2, 2): "Le goûter a une miette sur le banc.",
    (3, 2, 3): "Le bois clair du banc est vide, un moment.",
    (3, 3, 1): "Le doudou a l'odeur du vent, au sac.",
    (3, 3, 2): "La pomme n'est plus dans le torchon.",
    (3, 3, 3): "Le sac vert est fermé, sur le banc.",
}


def trans_l2_031(i: int) -> list[str]:
    loc = L1_031[i]
    return [
        f"papa|Aniss joue encore un peu, {loc['ou']}.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le sac reste près de nous.",
    ]


def trans_l3_031(i: int) -> list[str]:
    loc = L1_031[i]
    return [
        f"maman|Le sac est encore un peu vide, {loc['ou']}.",
        "narrateur|La casquette, la gourde, ou le goûter.",
        "papa|Qu'est-ce qui manque, Aniss ?",
    ]


def body_031(i: int, j: int, k: int) -> list[str]:
    lines = list(NEED_031[k])
    lines.append(MARK_031[j])
    lines.extend(PLACE_031[i])
    lines.append(f"narrateur|{IMG_031[(i, j, k)]}")
    lines.append("maman|On rentre ?")
    lines.append("papa|Oui.")
    lines.append("papa|Le sac vient avec nous.")
    return lines


def fin_031(i: int, j: int, k: int) -> list[str]:
    loc = L1_031[i]
    obj = L2_031[j]
    need = L3_031[k]
    return [
        f"narrateur|{IMG_031[(i, j, k)]}",
        f"narrateur|Aniss a joué {loc['ou']}.",
        f"narrateur|Il a choisi {obj['lab']}.",
        f"narrateur|Il a mis {need['lab']} dans le sac.",
        "narrateur|Le sac vert est sur le dos, un peu lourd.",
        "enfant-m|Il n'est plus vide.",
        "maman|Merci, Aniss.",
        "papa|On rentre à la maison.",
        "narrateur|Les bottes font toc toc, dans l'entrée.",
        f"narrateur|{FIN_031[(i, j, k)]}",
    ]


def build_031() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|Le panier à linge est encore tiède.",
        "narrateur|Les chaussettes sentent le savon.",
        "narrateur|Un petit bouton brille sur une chemise.",
        "narrateur|Dehors, le marché parle tout bas.",
        "narrateur|Une cloche de vélo sonne une fois.",
        "narrateur|Dans l'entrée, les bottes gouttent.",
        "narrateur|Une flaque ronde brille au sol.",
        "narrateur|Le banc du couloir est en bois clair.",
        "narrateur|Le sac vert d'Aniss est posé dessus.",
        "narrateur|La boucle jaune fait un petit clic.",
        "narrateur|Papa plie un torchon à carreaux.",
        "maman|Tu as senti le savon, Aniss ?",
        "enfant-m|Oui, maman.",
        "enfant-m|Ça sent le linge propre.",
        "papa|Le sac t'attend sur le banc.",
        "narrateur|En ce moment, Aniss touche le sac.",
        "narrateur|La sangle est lisse.",
        "enfant-m|Je veux aller au parc.",
        "maman|D'accord.",
        "narrateur|Aniss soulève le sac.",
        "narrateur|Le sac est trop léger.",
        "enfant-m|Il est vide, presque.",
        "papa|Ton doudou est dans le panier ?",
        "narrateur|Aniss fouille le linge tiède.",
        "narrateur|Le doudou sent le savon.",
        "enfant-m|Te voilà.",
        "narrateur|Il le glisse dans le sac vert.",
        "maman|Merci, Aniss.",
        "papa|On y va ?",
        "enfant-m|Oui.",
        "narrateur|Une goutte tombe encore d'une botte.",
    ]
    sons["CHK_T0000_P0000"] = "linge"
    s["CHK_T0001_P0000"] = [
        "maman|On va au parc.",
        "maman|Où va-t-on d'abord ?",
        "narrateur|Le bac à sable, le toboggan, ou les balançoires.",
    ]
    extras["CHK_T0001_P0000"] = extras_opts("le bac à sable", "le toboggan", "les balançoires")
    sons["CHK_T0001_P0000"] = "enfants_parc"
    qf = extras_q(
        "sac",
        "sac | le sac | dans le sac | il met | mettre | le doudou",
        "Il les met dans le sac. Où les met Aniss ?",
    )
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_031[i]
        sons[p] = "enfants_parc"
        s[f"{p}_Q0001"] = Q_031[i]
        extras[f"{p}_Q0001"] = qf
        s[f"{p}_C0001"] = C_031[i]
        s[f"{p}_T0002_P0000"] = trans_l2_031(i)
        extras[f"{p}_T0002_P0000"] = extras_opts("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_031[(i, j)]
            s[f"{p2}_T0003_P0000"] = trans_l3_031(i)
            extras[f"{p2}_T0003_P0000"] = extras_opts("la casquette", "la gourde", "le goûter")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_031(i, j, k)
                s[f"{p3}_F0001"] = fin_031(i, j, k)
    return s, sons, extras


def main() -> None:
    s, sons, extras = build_030()
    write_tree(
        "TREE-AUT-030",
        (
            "Raphaël veut emmener ses petits bateaux au parc. La bouilloire chante. "
            "Il prend tout à la fois, un bateau glisse. Une chose puis la suivante : "
            "la chaussette, les bateaux, le parc. Ils jouent, puis rentrent. "
            "La bouilloire s'est tue."
        ),
        "La bouilloire et les petits bateaux",
        "Raphaël, papa, maman",
        "salon le matin, rideau à bateaux, puis parc",
        s,
        sons,
        extras,
    )
    relecture(
        "TREE-AUT-030",
        "La bouilloire et les petits bateaux",
        "Raphaël veut les bateaux au parc. Bouilloire, rideau bleu et jaune, "
        "chaussette chaude. Un bateau glisse. Séquence vécue. Bac / toboggan / "
        "balançoires, puis ballon / seau / doudou, puis banc / portail / manteau.",
        "D16 Raphaël (plus Jules). AUT.ROU.001 implicite, pas de refrain d'étapes. "
        "Labels T3 = banc/portail/manteau. Pas Tom/Léa/Sami. Fin = bouilloire tue.",
    )

    s, sons, extras = build_031()
    write_tree(
        "TREE-AUT-031",
        (
            "Aniss veut aller au parc. Le sac vert sur le banc est trop léger. "
            "Le doudou est dans le linge tiède. Il le glisse dans le sac. "
            "Au parc, il manque encore la casquette, la gourde ou le goûter. "
            "Il les met dans le sac. Une miette de savon reste sur le banc."
        ),
        "Le sac vert d'Aniss sur le banc",
        "Aniss, papa, maman",
        "entrée, banc, panier à linge, puis parc",
        s,
        sons,
        extras,
    )
    relecture(
        "TREE-AUT-031",
        "Le sac vert d'Aniss sur le banc",
        "Aniss veut le parc. Sac vert trop léger, doudou dans le linge. "
        "Bac / toboggan / balançoires, jeu ballon / seau / doudou, puis "
        "casquette (soleil) / gourde (soif) / goûter (faim) manquants.",
        "D16 Aniss (plus Noé). AUT.AFF.001 implicite. Pas une liste de sac. "
        "Labels T3 = casquette/gourde/goûter. Pas Tom/Léa/Sami. Fin = banc.",
    )


if __name__ == "__main__":
    main()
