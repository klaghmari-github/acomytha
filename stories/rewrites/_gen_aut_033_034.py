#!/usr/bin/env python3
"""F-NAR-009 — merged.json TREE-AUT-033 et TREE-AUT-034."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAXW = {"N1": 10, "N2": 15, "N3": 18}

FORBIDDEN_NAR = (
    "on va apprendre",
    "voici le geste",
    "papa sourit",
    "maman sourit",
    "papa est là",
    "maman est là",
)
FORBIDDEN_NAMES = (
    "kenzo", "lina", "nora", "maya", "inès", "ines", "léa ", " lea ",
    "zoé", "zoe", "sara ", "lila", "hugo", "jules", "noé", "noe",
    "adam", "sami", "tom ", " tom",
)


def from_lines(lines: list[str]) -> tuple[str, str]:
    out = []
    phrases = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        role, phrase = raw.split("|", 1)
        phrase = phrase.strip()
        out.append(f"{role}|{phrase}")
        phrases.append(phrase)
    return " ".join(phrases), "\n".join(out)


def wc(phrase: str) -> int:
    return len(phrase.replace("'", " ").replace("’", " ").replace("-", " ").split())


def apply_map(src: dict, fil: str, title: str, chars: str, setting: str, scripts: dict[str, list[str]], sons_over: dict[str, str] | None = None) -> dict:
    sons_over = sons_over or {}
    by = {}
    missing = []
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        if cid not in scripts:
            missing.append(cid)
            continue
        text, script = from_lines(scripts[cid])
        nc = dict(c)
        nc["text"] = text
        nc["script"] = script
        if cid in sons_over:
            nc["sons"] = sons_over[cid]
        elif nc.get("sons") in (None,):
            nc["sons"] = ""
        by[cid] = nc
    if missing:
        raise SystemExit(f"{src['story_id']} missing {missing[:8]}… ({len(missing)})")
    if extra:
        raise SystemExit(f"{src['story_id']} extra {sorted(extra)[:8]}")
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    return out


def check(story: dict) -> None:
    band = story["age_band"]
    mx = MAXW[band]
    sid = story["story_id"]
    all_script = []
    for c in story["chunks"]:
        all_script.append(c["script"])
        for line in c["script"].splitlines():
            role, phrase = line.split("|", 1)
            n = wc(phrase)
            if n > mx:
                raise SystemExit(f"{sid} {c['chunk_id']} {n}w>{mx} {role}|{phrase}")
            if "。" in phrase or len(phrase) > 1 and phrase[-1] not in ".!?":
                # allow short answers without punct? require end punct
                if not phrase.endswith((".", "?", "!")):
                    raise SystemExit(f"{sid} {c['chunk_id']} no punct: {phrase}")
        low = " ".join(
            ln.split("|", 1)[1] for ln in c["script"].splitlines() if ln.startswith("narrateur|")
        ).lower()
        for bad in FORBIDDEN_NAR:
            if bad in low:
                raise SystemExit(f"{sid} {c['chunk_id']} forbidden «{bad}»")
        joined = "\n".join(all_script).lower()
    joined = "\n".join(all_script)
    low = joined.lower()
    if "on va apprendre" in low:
        raise SystemExit(f"{sid} On va apprendre")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid} no adult")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "bon travail" not in aj:
        raise SystemExit(f"{sid} no bravo")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid} no adult question")
    if "papa|" not in joined or "maman|" not in joined:
        raise SystemExit(f"{sid} need papa and maman")
    # extra child names in narrative except allowed choice labels Tom/Léa/Sami on 033
    nar = " ".join(
        ln.split("|", 1)[1]
        for ln in joined.splitlines()
        if ln.startswith("narrateur|") or ln.startswith("papa|") or ln.startswith("maman|") or ln.startswith("enfant")
    )
    # ok to have Tom Léa Sami as bag labels
    blob = " " + nar.lower().replace("é", "e") + " "
    for name in ("kenzo", "lina", "nora", "maya", "hugo", "jules"):
        if name in blob:
            raise SystemExit(f"{sid} name {name}")
    print(sid, "ok", len(story["chunks"]), "chunks", "fil", story["fil_rouge"][:50])


# ---------------------------------------------------------------------------
# TREE-AUT-033  Nino  parc  N1  AUT.AFF.003
# ---------------------------------------------------------------------------

L1_033 = {
    1: {
        "label": "le bac à sable",
        "ou": "au bac à sable",
        "ici": "le bac à sable",
    },
    2: {
        "label": "le toboggan",
        "ou": "au toboggan",
        "ici": "le toboggan",
    },
    3: {
        "label": "les balançoires",
        "ou": "aux balançoires",
        "ici": "les balançoires",
    },
}
L2_033 = {
    1: {"label": "le ballon", "obj": "ballon"},
    2: {"label": "le seau", "obj": "seau"},
    3: {"label": "le doudou", "obj": "doudou"},
}
L3_033 = {
    1: {"label": "Tom", "sac": "le sac Tom", "coul": "bleu"},
    2: {"label": "Léa", "sac": "le sac Léa", "coul": "rouge"},
    3: {"label": "Sami", "sac": "le sac Sami", "coul": "vert"},
}

L1_ARRIVE_033 = {
    1: [
        "narrateur|Nino va vers le bac à sable.",
        "narrateur|Le sable est frais et fin.",
        "narrateur|Il colle un peu aux genoux.",
        "narrateur|Une pelle rouge attend.",
        "narrateur|Le bois du bac est rêche.",
        "maman|Tu fais un gâteau, Nino ?",
        "enfant-m|Un gâteau de sable.",
        "papa|Le banc garde tes affaires.",
        "papa|Le seau. Le manteau. Le doudou.",
        "maman|Avant de partir, on les reprend.",
        "enfant-m|Ils sont sur le banc.",
        "papa|Bravo. Tu t'en souviens.",
        "narrateur|Un grain brille sur le genou.",
        "narrateur|Ça sent l'écorce mouillée.",
    ],
    2: [
        "narrateur|Nino va vers le toboggan.",
        "narrateur|Le métal est un peu froid.",
        "narrateur|Une feuille colle sur la rampe.",
        "narrateur|La feuille est jaune et molle.",
        "papa|Tu montes, Nino. Doucement.",
        "enfant-m|Je monte, papa.",
        "narrateur|Les marches font tic, tic.",
        "maman|Tes affaires sont sur le banc.",
        "maman|Avant de partir, on les reprend.",
        "enfant-m|Le seau et le manteau.",
        "papa|Oui. Et le doudou gris.",
        "papa|Bravo. C'est du bon travail.",
        "narrateur|Un oiseau passe au-dessus.",
        "narrateur|Le toboggan brille un peu.",
    ],
    3: [
        "narrateur|Nino va vers les balançoires.",
        "narrateur|La chaîne fait encore cling.",
        "narrateur|Elle est froide dans la main.",
        "narrateur|Les pieds touchent le sable.",
        "maman|Tu te tiens bien, Nino ?",
        "enfant-m|Oui, maman. Cling.",
        "papa|Le banc est juste là.",
        "papa|Il garde tes affaires.",
        "maman|Avant de partir, on les reprend.",
        "enfant-m|Le manteau bleu.",
        "papa|Oui. Le seau. Le doudou.",
        "maman|Bravo. Tu as de la mémoire.",
        "narrateur|Un nuage passe, tout lent.",
        "narrateur|La chaîne se tait un peu.",
    ],
}

L2_PLAY_033 = {
    1: [  # ballon
        "narrateur|Nino a choisi le ballon.",
        "narrateur|Le ballon est rouge et lisse.",
        "narrateur|Il fait un petit bond.",
        "narrateur|Puis il s'arrête près de papa.",
        "papa|Le ballon reste près de nous.",
        "enfant-m|Il est rouge, papa.",
        "maman|Tes affaires sont encore au banc.",
        "maman|On les reprend avant de partir.",
        "enfant-m|Le seau. Le manteau.",
        "papa|Oui. Bravo, Nino.",
        "narrateur|Une goutte brille sur le cuir.",
    ],
    2: [  # seau — aussi une affaire
        "narrateur|Nino a choisi le seau.",
        "narrateur|Le seau jaune a du sable.",
        "narrateur|L'anse est un peu froide.",
        "maman|C'est ton seau, Nino.",
        "enfant-m|Il est jaune.",
        "papa|On joue avec. Puis on le reprend.",
        "papa|Avant de partir, on le prend.",
        "maman|Avec le manteau et le doudou.",
        "enfant-m|Je le tiens.",
        "papa|Bravo. Tu le gardes près de toi.",
        "narrateur|Un grain tombe, tout fin.",
    ],
    3: [  # doudou — aussi une affaire
        "narrateur|Nino a choisi le doudou.",
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Un peu de sable est dessus.",
        "maman|Il t'attendait, Nino.",
        "enfant-m|Il est doux.",
        "papa|On le reprend avant de partir.",
        "maman|Avec le seau et le manteau.",
        "enfant-m|Je le serre.",
        "papa|Bravo. Tu as fait du bon travail.",
        "narrateur|L'oreille du doudou est chaude.",
        "narrateur|Le banc reste tout près.",
    ],
}

# unique last image per (l1,l2,l3)
IMG_033 = {
    (1, 1, 1): "Un grain rouge colle au sac bleu.",
    (1, 1, 2): "Le ballon laisse une trace au sac rouge.",
    (1, 1, 3): "Un brin d'herbe reste au sac vert.",
    (1, 2, 1): "Du sable fin brille dans le sac bleu.",
    (1, 2, 2): "L'anse jaune touche le sac rouge.",
    (1, 2, 3): "Un coquillage minuscule roule au sac vert.",
    (1, 3, 1): "L'oreille grise dépasse du sac bleu.",
    (1, 3, 2): "Le doudou sent encore le sable, au sac rouge.",
    (1, 3, 3): "Un fil gris pend du sac vert.",
    (2, 1, 1): "La feuille jaune colle au sac bleu.",
    (2, 1, 2): "Le ballon est un peu froid, près du sac rouge.",
    (2, 1, 3): "Une goutte glisse vers le sac vert.",
    (2, 2, 1): "Le seau sonne tout doux contre le sac bleu.",
    (2, 2, 2): "Le métal du toboggan se tait, près du sac rouge.",
    (2, 2, 3): "Un pas sur la rampe, puis le sac vert.",
    (2, 3, 1): "Le doudou a vu le toboggan, dans le sac bleu.",
    (2, 3, 2): "L'oreille molle dépasse du sac rouge.",
    (2, 3, 3): "La rampe brille encore, loin du sac vert.",
    (3, 1, 1): "La chaîne a fait cling, près du sac bleu.",
    (3, 1, 2): "Le ballon a touché le sable, près du sac rouge.",
    (3, 1, 3): "Un nuage passe au-dessus du sac vert.",
    (3, 2, 1): "L'anse du seau est froide, contre le sac bleu.",
    (3, 2, 2): "Un cling lointain, et le sac rouge.",
    (3, 2, 3): "Le seau jaune pose son ombre au sac vert.",
    (3, 3, 1): "Le doudou a senti le vent, dans le sac bleu.",
    (3, 3, 2): "La chaîne se tait, près du sac rouge.",
    (3, 3, 3): "L'oreille grise dépasse du sac vert.",
}

Q_033 = ["narrateur|Avant de partir, on reprend quoi ?"]

C_033 = {
    1: [
        "narrateur|Oui.",
        "narrateur|On reprend les affaires.",
        "papa|Avant de partir, Nino.",
        "maman|On cherche le seau et le manteau.",
        "maman|On les prend.",
        "enfant-m|Le seau. Le manteau.",
        "papa|Et le doudou gris.",
        "papa|Bravo. Tu as fait du bon travail.",
        "narrateur|Le banc est encore là.",
    ],
    2: [
        "narrateur|Oui.",
        "narrateur|On reprend les affaires.",
        "maman|Avant de partir, on les cherche.",
        "papa|Le seau jaune. Le manteau bleu.",
        "enfant-m|On les prend.",
        "maman|Oui. Bravo, Nino.",
        "papa|C'est du bon travail.",
        "narrateur|La feuille reste sur la rampe.",
        "narrateur|Les affaires vont venir.",
    ],
    3: [
        "narrateur|Oui.",
        "narrateur|On reprend les affaires.",
        "papa|Avant de partir.",
        "maman|On cherche le seau et le manteau.",
        "enfant-m|Je les prends.",
        "papa|Bravo. Tu as compris.",
        "maman|Le doudou aussi.",
        "narrateur|La chaîne fait un tout petit cling.",
        "narrateur|Puis elle se tait.",
    ],
}


def l3_body_033(i: int, j: int, k: int) -> list[str]:
    loc = L1_033[i]
    obj = L2_033[j]
    sac = L3_033[k]
    img = IMG_033[(i, j, k)]
    return [
        f"narrateur|Nino va vers {sac['sac']}.",
        f"narrateur|Le sac est {sac['coul']}, accroché à la barrière.",
        "narrateur|Le nom est cousu, tout simple.",
        "maman|C'est l'heure, Nino.",
        "maman|On reprend tes affaires.",
        "papa|Avant de partir.",
        "enfant-m|Le seau. Le manteau.",
        "narrateur|Nino prend le seau jaune.",
        "narrateur|Il prend le manteau bleu.",
        "narrateur|Il prend le doudou gris.",
        f"papa|Tu mets ça près de {sac['sac']} ?",
        f"enfant-m|{sac['label']}.",
        "maman|Bravo. Tu as repris tes affaires.",
        "papa|C'est du bon travail.",
        f"narrateur|{img}",
        "narrateur|On rentre ensemble.",
    ]


def l3_fin_033(i: int, j: int, k: int) -> list[str]:
    loc = L1_033[i]
    obj = L2_033[j]
    sac = L3_033[k]
    img = IMG_033[(i, j, k)]
    return [
        f"narrateur|Nino est passé par {loc['ici']}.",
        f"narrateur|Il a pris {obj['label']}.",
        f"narrateur|Il a rejoint {sac['sac']}.",
        "narrateur|Avant de partir, il a repris ses affaires.",
        "enfant-m|Le seau. Le manteau. Le doudou.",
        "maman|Oui. Bravo, Nino.",
        "papa|Tu as fait du bon travail.",
        f"narrateur|{img}",
        "narrateur|L'histoire est finie.",
    ]


def trans_l1_033() -> list[str]:
    return [
        "narrateur|On peut aller au bac à sable.",
        "narrateur|On peut aller au toboggan.",
        "narrateur|Ou aux balançoires.",
    ]


def trans_l2_033() -> list[str]:
    return [
        "narrateur|On peut prendre le ballon.",
        "narrateur|On peut prendre le seau.",
        "narrateur|Ou le doudou.",
    ]


def trans_l3_033() -> list[str]:
    return [
        "narrateur|On peut aller vers Tom.",
        "narrateur|On peut aller vers Léa.",
        "narrateur|Ou vers Sami.",
    ]


def build_033() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|La chaîne du portique fait cling.",
        "narrateur|Elle est encore un peu froide.",
        "narrateur|Une flaque tient une feuille.",
        "narrateur|La feuille est jaune et molle.",
        "narrateur|Le sable colle dans une chaussette.",
        "narrateur|Ça sent l'écorce mouillée.",
        "narrateur|Au loin, le four sent le pain.",
        "narrateur|Un banc de bois attend.",
        "narrateur|Dessus, un manteau bleu est plié.",
        "narrateur|Un seau jaune est à l'envers.",
        "narrateur|Un doudou gris regarde les arbres.",
        "maman|Nino, tu as entendu la chaîne ?",
        "enfant-m|Oui, maman. Cling.",
        "papa|Le banc garde tes affaires.",
        "papa|Le seau, le manteau, le doudou.",
        "maman|Avant de partir, on les reprend.",
        "enfant-m|Je veux jouer !",
        "papa|On joue un peu, d'accord.",
        "narrateur|En ce moment, Nino touche le sable.",
        "narrateur|Le sable est frais et fin.",
    ]
    s["CHK_T0001_P0000"] = trans_l1_033()
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_ARRIVE_033[i]
        s[f"{p}_Q0001"] = Q_033
        s[f"{p}_C0001"] = C_033[i]
        s[f"{p}_T0002_P0000"] = trans_l2_033()
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            extra = {
                1: "narrateur|Le sable reste aux genoux.",
                2: "narrateur|La rampe est encore froide.",
                3: "narrateur|La chaîne fait un petit cling.",
            }[i]
            s[p2] = L2_PLAY_033[j] + [extra]
            s[f"{p2}_T0003_P0000"] = trans_l3_033()
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_033(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_033(i, j, k)
    return s


# ---------------------------------------------------------------------------
# TREE-AUT-034  Chouchou  jardin  N2  AUT.RAN.001
# ---------------------------------------------------------------------------

L1_034 = {
    1: {"label": "la cuisine", "ou": "dans la cuisine", "ici": "la cuisine"},
    2: {"label": "le jardin", "ou": "dans le jardin", "ici": "le jardin"},
    3: {"label": "la chambre", "ou": "dans la chambre", "ici": "la chambre"},
}
L2_034 = {
    1: {"label": "les cubes", "obj": "cubes"},
    2: {"label": "le livre", "obj": "livre"},
    3: {"label": "la dînette", "obj": "dînette"},
}
L3_034 = {
    1: {"label": "le matin", "quand": "le matin", "lum": "La lumière est pâle, un peu bleue."},
    2: {"label": "après la sieste", "quand": "après la sieste", "lum": "L'air est tiède, un peu lourd."},
    3: {"label": "le soir", "quand": "le soir", "lum": "La lumière devient orange, tout doux."},
}

L1_ARRIVE_034 = {
    1: [
        "narrateur|Chouchou va vers la cuisine.",
        "narrateur|Le carrelage est frais sous les pieds.",
        "narrateur|Une tomate coupe attend dans l'assiette.",
        "narrateur|Ça sent encore le jardin, par la fenêtre.",
        "narrateur|La caisse bleue est posée près du meuble.",
        "maman|Tu as vu la caisse, Chouchou ?",
        "enfant-m|Elle est bleue, maman.",
        "papa|On joue un peu ici.",
        "papa|Après le jeu, on range.",
        "maman|On met dans la caisse.",
        "enfant-m|Dans la caisse.",
        "papa|Bravo. Tu t'en souviens.",
        "narrateur|Une goutte d'arrosoir sèche sur le seuil.",
        "narrateur|Le frigo fait un petit ronron.",
    ],
    2: [
        "narrateur|Chouchou reste dans le jardin.",
        "narrateur|L'ombre du prunier est douce.",
        "narrateur|Une abeille va sur une fleur, puis s'en va.",
        "narrateur|La terre est un peu collante.",
        "narrateur|La caisse bleue est ouverte, sous l'arbre.",
        "papa|La caisse est à ta hauteur, Chouchou.",
        "enfant-m|Je la vois, papa.",
        "maman|Après le jeu, on range.",
        "maman|On met dans la caisse.",
        "enfant-m|Dans la caisse.",
        "papa|Bravo. C'est du bon travail.",
        "narrateur|L'arrosoir goutte encore, tout petit.",
        "narrateur|Une feuille de prunier tourne.",
    ],
    3: [
        "narrateur|Chouchou va vers la chambre.",
        "narrateur|Le tapis est épais et chaud.",
        "narrateur|Le rideau bouge un peu.",
        "narrateur|Ça sent encore la terre, sur les chaussettes.",
        "narrateur|La caisse bleue a suivi, près du lit.",
        "maman|La caisse est là, Chouchou.",
        "enfant-m|Près du lit.",
        "papa|On joue un peu sur le tapis.",
        "papa|Après le jeu, on range.",
        "maman|On met dans la caisse.",
        "enfant-m|Dans la caisse.",
        "maman|Bravo. Tu as entendu.",
        "narrateur|Un rayon touche le bois du lit.",
        "narrateur|La caisse attend, ouverte.",
    ],
}

L2_PLAY_034 = {
    1: [
        "narrateur|Chouchou a choisi les cubes.",
        "narrateur|Un cube est rouge.",
        "narrateur|Un cube est jaune.",
        "narrateur|Le rouge est un peu rêche.",
        "papa|Tu poses le rouge en bas ?",
        "enfant-m|Le rouge en bas.",
        "narrateur|La tour est petite et ferme.",
        "maman|Après le jeu, les cubes vont dans la caisse.",
        "enfant-m|Dans la caisse.",
        "papa|Oui. Bravo, Chouchou.",
        "narrateur|Un coin de cube a un peu de terre.",
    ],
    2: [
        "narrateur|Chouchou a choisi le livre.",
        "narrateur|La couverture est lisse, un peu froide.",
        "narrateur|Une page est pliée, tout doux.",
        "maman|Tu tournes la page, Chouchou ?",
        "enfant-m|Oui. Une page.",
        "papa|Après le jeu, le livre va dans la caisse.",
        "enfant-m|Dans la caisse.",
        "maman|Bravo. Tu t'en souviens.",
        "narrateur|Le livre sent un peu le jardin.",
        "narrateur|Une miette de terre reste au coin.",
    ],
    3: [
        "narrateur|Chouchou a choisi la dînette.",
        "narrateur|Une tasse est à l'envers.",
        "narrateur|Elle a un peu de terre au bord.",
        "papa|On fait le goûter, tout doux ?",
        "enfant-m|Le goûter.",
        "maman|Après le jeu, la dînette va dans la caisse.",
        "enfant-m|Dans la caisse.",
        "papa|Oui. Bravo. C'est du bon travail.",
        "narrateur|La tasse fait un tout petit bruit.",
        "narrateur|Puis elle se tait.",
    ],
}

IMG_034 = {
    (1, 1, 1): "Un cube rouge a une miette de tomate.",
    (1, 1, 2): "Le carrelage est tiède sous la caisse.",
    (1, 1, 3): "Le frigo ronronne, la caisse est fermée.",
    (1, 2, 1): "Une page du livre sent la tomate.",
    (1, 2, 2): "Le torchon de la cuisine a glissé.",
    (1, 2, 3): "La fenêtre de la cuisine est orange.",
    (1, 3, 1): "La tasse a une goutte sur le bord.",
    (1, 3, 2): "La dînette est calme, près du meuble.",
    (1, 3, 3): "L'assiette de tomate est vide.",
    (2, 1, 1): "Un cube a de la terre au coin.",
    (2, 1, 2): "Une feuille de prunier pose sur la caisse.",
    (2, 1, 3): "L'abeille est partie. La caisse est fermée.",
    (2, 2, 1): "Le livre a une goutte d'arrosoir au coin.",
    (2, 2, 2): "L'ombre du prunier a bougé.",
    (2, 2, 3): "Le jardin sent encore la tomate, plus doux.",
    (2, 3, 1): "La tasse a un peu de terre sèche.",
    (2, 3, 2): "L'arrosoir ne goutte plus.",
    (2, 3, 3): "Une prune tombe, loin, tout mou.",
    (3, 1, 1): "Un cube rouge reste au bord du tapis, puis entre.",
    (3, 1, 2): "Le rideau de la chambre est calme.",
    (3, 1, 3): "Le bois du lit est tiède.",
    (3, 2, 1): "Une page du livre touche le tapis, puis rentre.",
    (3, 2, 2): "Le rayon sur le lit a bougé.",
    (3, 2, 3): "La chambre écoute le soir.",
    (3, 3, 1): "La tasse est rentrée, propre assez.",
    (3, 3, 2): "Le tapis a un creux, puis plus.",
    (3, 3, 3): "Le rideau devient orange, tout lent.",
}

Q_034 = ["narrateur|Après le jeu, on range où ?"]

C_034 = {
    1: [
        "narrateur|Oui.",
        "narrateur|On range.",
        "papa|On met dans la caisse.",
        "enfant-m|Dans la caisse.",
        "maman|Bravo, Chouchou.",
        "maman|Tu as fait du bon travail.",
        "narrateur|La caisse bleue attend près du meuble.",
        "narrateur|Le carrelage est encore frais.",
    ],
    2: [
        "narrateur|Oui.",
        "narrateur|On range.",
        "maman|On met dans la caisse.",
        "enfant-m|Sous le prunier.",
        "papa|Dans la caisse, oui.",
        "papa|Bravo. C'est du bon travail.",
        "narrateur|L'ombre de l'arbre est ronde.",
        "narrateur|La caisse est ouverte, prête.",
    ],
    3: [
        "narrateur|Oui.",
        "narrateur|On range.",
        "papa|On met dans la caisse.",
        "enfant-m|Près du lit.",
        "maman|Dans la caisse. Bravo.",
        "papa|Tu as entendu. C'est bien.",
        "narrateur|Le tapis est chaud sous les genoux.",
        "narrateur|La caisse attend, tout près.",
    ],
}

L2_EXTRA_034 = {
    1: "narrateur|Une odeur de tomate entre encore.",
    2: "narrateur|Une goutte d'arrosoir sèche sur le bois.",
    3: "narrateur|Le rideau fait un tout petit bruit.",
}


def l3_body_034(i: int, j: int, k: int) -> list[str]:
    loc = L1_034[i]
    obj = L2_034[j]
    t = L3_034[k]
    img = IMG_034[(i, j, k)]
    what = {
        1: "Chouchou pose les cubes, un par un.",
        2: "Chouchou glisse le livre, tout plat.",
        3: "Chouchou pose la tasse, puis l'assiette.",
    }[j]
    return [
        f"narrateur|C'est {t['quand']}.",
        f"narrateur|{t['lum']}",
        f"papa|Le jeu est fini, Chouchou.",
        "papa|On range.",
        "maman|On met dans la caisse.",
        "enfant-m|Dans la caisse.",
        f"narrateur|{what}",
        "narrateur|La caisse bleue se remplit.",
        "maman|Tu as fini de ranger ?",
        "enfant-m|Oui, maman.",
        "papa|Bravo. Tu as fait du bon travail.",
        f"narrateur|{img}",
        "narrateur|On se tient la main un peu.",
    ]


def l3_fin_034(i: int, j: int, k: int) -> list[str]:
    loc = L1_034[i]
    obj = L2_034[j]
    t = L3_034[k]
    img = IMG_034[(i, j, k)]
    return [
        f"narrateur|Chouchou est passé par {loc['ici']}.",
        f"narrateur|Il a pris {obj['label']}.",
        f"narrateur|C'était {t['quand']}.",
        "narrateur|Après le jeu, il a rangé.",
        "enfant-m|Dans la caisse.",
        "maman|Oui. Bravo, Chouchou.",
        "papa|Tu as fait du bon travail.",
        f"narrateur|{img}",
        "narrateur|L'histoire est finie.",
    ]


def trans_l1_034() -> list[str]:
    return [
        "narrateur|On peut aller dans la cuisine.",
        "narrateur|On peut aller dans le jardin.",
        "narrateur|Ou dans la chambre.",
    ]


def trans_l2_034() -> list[str]:
    return [
        "narrateur|On peut prendre les cubes.",
        "narrateur|On peut prendre le livre.",
        "narrateur|Ou la dînette.",
    ]


def trans_l3_034() -> list[str]:
    return [
        "narrateur|C'est le matin ?",
        "narrateur|Après la sieste ?",
        "narrateur|Ou le soir ?",
    ]


def build_034() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|L'arrosoir goutte encore.",
        "narrateur|Une goutte tombe sur la terre.",
        "narrateur|Ça sent la tomate chaude.",
        "narrateur|Une abeille va sur une fleur.",
        "narrateur|Sous le prunier, l'ombre est douce.",
        "narrateur|Une caisse bleue est ouverte.",
        "narrateur|Des cubes dépassent du bord.",
        "narrateur|Un livre a une page pliée.",
        "narrateur|Une tasse de dînette a de la terre.",
        "narrateur|Les chaussettes de Chouchou sont un peu humides.",
        "papa|Tu as vu la caisse, Chouchou ?",
        "enfant-m|Elle est bleue, papa.",
        "maman|Après le jeu, on range.",
        "maman|On met dans la caisse.",
        "enfant-m|Dans la caisse.",
        "papa|Oui. Bravo. Tu t'en souviens.",
        "narrateur|En ce moment, Chouchou prend un cube.",
        "narrateur|Le cube est rouge et rêche.",
    ]
    s["CHK_T0001_P0000"] = trans_l1_034()
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_ARRIVE_034[i]
        s[f"{p}_Q0001"] = Q_034
        s[f"{p}_C0001"] = C_034[i]
        s[f"{p}_T0002_P0000"] = trans_l2_034()
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2_PLAY_034[j] + [L2_EXTRA_034[i]]
            s[f"{p2}_T0003_P0000"] = trans_l3_034()
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_034(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_034(i, j, k)
    return s


def write_story(sid: str, fil: str, title: str, chars: str, setting: str, scripts: dict[str, list[str]], sons_over: dict[str, str] | None = None) -> None:
    src = json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))
    merged = apply_map(src, fil, title, chars, setting, scripts, sons_over)
    check(merged)
    path = ROOT / sid / "merged.json"
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", path, "bytes", path.stat().st_size)


def main() -> None:
    write_story(
        "TREE-AUT-033",
        "Nino joue au parc. Le banc garde seau, manteau et doudou. Avant de partir, il les reprend.",
        "Le seau à l'envers sous le banc",
        "Nino, maman, papa",
        "au parc, banc de bois, seau jaune et manteau bleu",
        build_033(),
        {"CHK_T0000_P0000": "enfants_parc"},
    )
    write_story(
        "TREE-AUT-034",
        "Chouchou joue sous le prunier. Après le jeu, les jouets retournent dans la caisse bleue.",
        "La caisse bleue sous le prunier",
        "Chouchou, papa, maman",
        "jardin, prunier, puis cuisine ou chambre",
        build_034(),
        None,
    )


if __name__ == "__main__":
    main()
