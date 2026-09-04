#!/usr/bin/env python3
"""F-NAR-009 — merged.json TREE-AUT-006 (N2, AFF.003) et TREE-AUT-007 (N3, ROU.001)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    BAD_NAMES,
    FORBIDDEN,
    OPENING_BAD,
    ROLES,
    _listy_run,
    from_script,
    words,
)

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 16}


def L(*items: str) -> list[str]:
    return [it.strip() for it in items if it.strip()]


def path_ids(i: int, j: int, k: int) -> list[str]:
    return [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        f"CHK_T0001_P000{i}",
        f"CHK_T0001_P000{i}_Q0001",
        f"CHK_T0001_P000{i}_C0001",
        f"CHK_T0001_P000{i}_T0002_P0000",
        f"CHK_T0001_P000{i}_T0002_P000{j}",
        f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
        f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
        f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
    ]


def make_chunk(src: dict, lines: list[str], extra: dict | None = None) -> dict:
    text, script = from_script(lines)
    nc = deepcopy(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    if nc.get("sons") is None:
        nc["sons"] = ""
    kind = src.get("kind") or ""
    if kind in ("passage_question", "transition_question"):
        nc["length_scale_piper"] = 1.28
        nc["rate_label"] = "slow"
    else:
        nc["length_scale_piper"] = 1.22
        nc["rate_label"] = src.get("rate_label") or "medium"
    if extra:
        nc.update(extra)
    return nc


def write_merged(sid: str, meta: dict, scripts: dict[str, list[str]], q: dict[str, dict]) -> dict:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = sorted(set(scripts) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={extra[:8]}")
    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        chunks.append(make_chunk(c, scripts[cid], q.get(cid)))
    out = dict(src)
    out.update(meta)
    out["chunks"] = chunks
    check_tree(out)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return out


def check_tree(story: dict) -> None:
    sid = story["story_id"]
    age = story["age_band"]
    lim = LIMITS[age]
    chunks = story["chunks"]
    by = {c["chunk_id"]: c for c in chunks}
    if len(chunks) != 86:
        raise SystemExit(f"{sid} n={len(chunks)}")
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if name in low:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    if "papa|" not in joined or "maman|" not in joined:
        raise SystemExit(f"{sid}: besoin papa et maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        raise SystemExit(f"{sid}: pas de merci/bravo")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in OPENING_BAD:
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
    listed = _listy_run(joined)
    if listed:
        raise SystemExit(f"{sid}: puces « {listed} »")
    for c in chunks:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: text ≠ script")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                raise SystemExit(f"{sid} ligne sans | : {ln}")
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                raise SystemExit(f"{sid} rôle {role}")
            n = words(phrase)
            if n > lim:
                raise SystemExit(f"{sid} {c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    needles = {
        "TREE-AUT-006": ("nina", "manteau", "reprend", "affaires", "partir"),
        "TREE-AUT-007": ("victorina", "pain", "chose"),
    }[sid]
    t1 = {1: ("matin",), 2: ("sieste",), 3: ("soir",)} if sid == "TREE-AUT-006" else {
        1: ("chambre",),
        2: ("eau",),
        3: ("cuisine",),
    }
    t2 = {1: ("cuisine",), 2: ("jardin",), 3: ("chambre",)} if sid == "TREE-AUT-006" else {
        1: ("t-shirt", "t shirt"),
        2: ("chaussette",),
        3: ("gilet",),
    }
    t3 = {1: ("ballon",), 2: ("seau",), 3: ("doudou",)} if sid == "TREE-AUT-006" else {
        1: ("sac",),
        2: ("manteau",),
        3: ("doudou",),
    }
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                ids = path_ids(i, j, k)
                blob = " ".join(by[cid]["text"] for cid in ids)
                n = words(blob)
                if n < 350:
                    raise SystemExit(f"{sid} path {i}{j}{k} trop court ({n})")
                lowb = blob.lower()
                for nd in needles:
                    if nd not in lowb:
                        raise SystemExit(f"{sid} path {i}{j}{k} manque {nd}")
                if not any(x in lowb for x in t1[i]):
                    raise SystemExit(f"{sid} path {i}{j}{k} T1 absent")
                if not any(x in lowb for x in t2[j]):
                    raise SystemExit(f"{sid} path {i}{j}{k} T2 absent")
                if not any(x in lowb for x in t3[k]):
                    raise SystemExit(f"{sid} path {i}{j}{k} T3 absent")
                last = [ln for ln in by[ids[-1]]["script"].splitlines() if ln.startswith("narrateur|")]
                if not last:
                    raise SystemExit(f"{sid} {ids[-1]} sans narrateur")
                end = last[-1].split("|", 1)[1].lower()
                if "histoire" in end or "bon travail" in end:
                    raise SystemExit(f"{sid} fin mécanique: {end}")
    l1 = [by[f"CHK_T0001_P000{i}"]["text"] for i in (1, 2, 3)]
    if len(set(l1)) < 3:
        raise SystemExit(f"{sid} T1 ne change pas l'histoire")
    l2 = [by[f"CHK_T0001_P0001_T0002_P000{j}"]["text"] for j in (1, 2, 3)]
    if len(set(l2)) < 3:
        raise SystemExit(f"{sid} T2 ne change pas l'histoire")
    l3 = [
        by[f"CHK_T0001_P0001_T0002_P0001_T0003_P000{k}"]["text"] for k in (1, 2, 3)
    ]
    if len(set(l3)) < 3:
        raise SystemExit(f"{sid} T3 ne change pas l'histoire")
    print(f"OK {sid} 1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}")


# ---------------------------------------------------------------------------
# TREE-AUT-006 — Nina, manteau jaune, soupe, vitre embuée. N2 AUT.AFF.003
# T1 matin / sieste / soir   T2 cuisine / jardin / chambre   T3 ballon / seau / doudou
# ---------------------------------------------------------------------------

MOM = {1: "le matin", 2: "après la sieste", 3: "le soir"}
ROOM6 = {1: "la cuisine", 2: "le jardin", 3: "la chambre"}
OBJ6 = {1: "le ballon rouge", 2: "le seau bleu", 3: "le doudou"}


def debut_006() -> list[str]:
    return L(
        "narrateur|La vitre de la cuisine est toute blanche de buée.",
        "narrateur|Une goutte y glisse, toute lente.",
        "narrateur|Ça sent la soupe, tout doux.",
        "narrateur|Le couvercle fait un petit clic.",
        "narrateur|Un manteau jaune pend au crochet.",
        "narrateur|Un bouton brille, encore tiède.",
        "narrateur|Sous la table, un seau bleu attend.",
        "narrateur|Dehors, une flaque attend aussi.",
        "maman|Tu as vu la buée, Nina ?",
        "enfant-f|Je fais un rond.",
        "narrateur|Nina essuie un petit rond.",
        "narrateur|La flaque apparaît, toute ronde.",
        "enfant-f|Je veux la flaque.",
        "enfant-f|Avec mon seau.",
        "papa|Le manteau aussi.",
        "narrateur|En ce moment, Nina touche le manteau jaune.",
        "narrateur|Le tissu est un peu épais.",
        "maman|On sort quand tu as tes affaires.",
        "enfant-f|Où est mon seau ?",
        "papa|On le cherche ensemble.",
        "narrateur|Des miettes dorées sont sur la table.",
        "narrateur|Le robinet fait une goutte, puis s'arrête.",
        "papa|Tu es prête à chercher ?",
        "enfant-f|Oui, papa.",
    )


def tq1_006() -> list[str]:
    return L(
        "narrateur|C'est quel moment, pour la flaque ?",
        "papa|Le matin, après la sieste, ou le soir.",
    )


def l1_006(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|La lumière du matin est pâle, sur la buée.",
            "narrateur|La soupe commence à peine.",
            "narrateur|Le manteau jaune est froid, au crochet.",
            "narrateur|La flaque de la nuit est encore grande.",
            "enfant-f|J'y vais.",
            "narrateur|Nina court vers la porte.",
            "narrateur|Ses mains sont vides.",
            "papa|Nina.",
            "papa|Tes mains.",
            "enfant-f|Oh.",
            "maman|Le seau est resté sous la table.",
            "narrateur|Le manteau n'est pas sur elle.",
            "enfant-f|Je veux la grande flaque.",
            "papa|On reprend tes affaires.",
            "maman|Tu as vu le gant, près du bol ?",
            "narrateur|Nina pose le gant dans la poche.",
        )
    if i == 2:
        return L(
            "narrateur|Après la sieste, la cuisine fume encore.",
            "narrateur|La soupe est prête, toute chaude.",
            "narrateur|La buée cache presque le jardin.",
            "narrateur|Nina essuie un rond plus grand.",
            "narrateur|La flaque a déjà rétréci.",
            "enfant-f|Elle part.",
            "narrateur|Nina cherche le manteau dans la vapeur.",
            "narrateur|Le crochet est flou.",
            "maman|Il est là, tout jaune.",
            "papa|Le seau aussi, avant qu'elle sèche.",
            "enfant-f|Je le prends.",
            "narrateur|Elle avance trop vite vers la porte.",
            "narrateur|Un pied glisse sur une miette.",
            "maman|Tes affaires d'abord.",
            "papa|La flaque t'attend encore un peu.",
        )
    return L(
        "narrateur|Le soir, la lampe allume le manteau jaune.",
        "narrateur|Il brille comme une petite lanterne.",
        "narrateur|Les bols de soupe sont sur la table.",
        "narrateur|Dehors, un réverbère s'allume.",
        "enfant-f|Une dernière flaque.",
        "narrateur|Nina prend le manteau, tout de suite.",
        "narrateur|Le seau reste sous la table.",
        "papa|Tu as le jaune.",
        "papa|Et le bleu ?",
        "enfant-f|Il est où ?",
        "maman|Sous la table, près des miettes.",
        "narrateur|Nina se baisse.",
        "narrateur|Le seau est un peu frais.",
        "papa|On reprend tout, même le soir.",
        "maman|La flaque est encore là.",
    )


def q_006(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Nina va à la porte.",
            "narrateur|Que reprend-elle ?",
        )
    if i == 2:
        return L(
            "narrateur|La buée cache encore le crochet.",
            "narrateur|Que fait Nina avant de sortir ?",
        )
    return L(
        "narrateur|Le manteau est sur Nina.",
        "narrateur|Et le seau ?",
    )


def c_006(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Nina regarde ses mains vides.",
            "enfant-f|Mes affaires.",
            "maman|On reprend tes affaires.",
            "papa|Avant de partir.",
            "narrateur|Elle se tourne vers le crochet.",
            "enfant-f|Le manteau jaune.",
            "papa|Merci, Nina.",
            "maman|Le seau ensuite.",
        )
    if i == 2:
        return L(
            "narrateur|Nina essuie encore la vitre.",
            "narrateur|Le manteau réapparaît, tout jaune.",
            "enfant-f|Je le prends.",
            "papa|On reprend tes affaires.",
            "maman|Avant de partir, le seau aussi.",
            "narrateur|Nina hoche la tête.",
            "maman|Merci.",
            "enfant-f|La flaque m'attend.",
        )
    return L(
        "narrateur|Nina se baisse sous la table.",
        "narrateur|Le seau bleu touche son genou.",
        "enfant-f|Je l'ai.",
        "maman|On reprend tes affaires.",
        "papa|Avant de partir, même le soir.",
        "narrateur|Le bouton du manteau brille.",
        "papa|Bravo.",
        "enfant-f|On peut aller à la flaque.",
    )


def tq2_006() -> list[str]:
    return L(
        "narrateur|Où Nina cherche-t-elle encore ?",
        "maman|La cuisine, le jardin, ou la chambre.",
    )


def l2_006(i: int, j: int) -> list[str]:
    when = MOM[i]
    if j == 1:
        extra = {
            1: "La lumière du matin pose un rond sur le seau.",
            2: "La vapeur de la sieste mouille le bois.",
            3: "La lampe du soir touche les miettes.",
        }[i]
        return L(
            f"narrateur|Nina cherche dans la cuisine, {when}.",
            f"narrateur|{extra}",
            "narrateur|Elle ouvre le placard, tout doux.",
            "narrateur|Une tasse cliquette.",
            "narrateur|Le seau est bien sous la table.",
            "enfant-f|Le voilà.",
            "papa|Le manteau, au crochet.",
            "narrateur|Nina l'enfile.",
            "narrateur|Une manche reste un peu froide.",
            "maman|Tu as regardé près du bol ?",
            "enfant-f|Le gant est dans la poche.",
            "papa|Tes affaires sont là.",
            "narrateur|La soupe sent encore, tout près.",
        )
    if j == 2:
        extra = {
            1: "L'herbe du matin est mouillée, toute froide.",
            2: "Après la sieste, la pierre est tiède.",
            3: "Le réverbère allume une feuille, le soir.",
        }[i]
        return L(
            f"narrateur|Nina pousse la porte du jardin, {when}.",
            f"narrateur|{extra}",
            "narrateur|Le seau est près du romarin.",
            "narrateur|La flaque brille déjà.",
            "enfant-f|Elle est là.",
            "narrateur|Le vent passe dans les manches vides.",
            "enfant-f|J'ai froid.",
            "maman|Le manteau est resté au crochet.",
            "narrateur|Nina rentre, tout de suite.",
            "narrateur|Elle reprend le manteau jaune.",
            "papa|Avant de rester dehors.",
            "enfant-f|Maintenant j'ai chaud.",
            "narrateur|Le romarin sent fort, sur le chemin.",
        )
    extra = {
        1: "Un rayon du matin traverse le rideau.",
        2: "Le lit de la sieste est encore chaud.",
        3: "La petite lampe du soir est allumée.",
    }[i]
    return L(
        f"narrateur|Nina va dans la chambre, {when}.",
        f"narrateur|{extra}",
        "narrateur|Le manteau est sur la chaise.",
        "narrateur|Le seau a servi de tambour.",
        "enfant-f|Il était là.",
        "papa|Et le manteau.",
        "narrateur|Une manche est à l'envers.",
        "maman|On la remet, tout doux.",
        "narrateur|Nina passe le bras.",
        "narrateur|Le doudou dépasse de la couverture.",
        "enfant-f|Mes affaires.",
        "papa|Tu les as reprises.",
        "narrateur|La chambre sent encore le savon.",
    )


def tq3_006() -> list[str]:
    return L(
        "narrateur|Elle emporte aussi quoi ?",
        "papa|Le ballon rouge, le seau bleu, ou le doudou.",
    )


OPEN6 = {
    (1, 1, 1): (
        "Le ballon rouge tape une tasse, dans la cuisine.",
        "Un peu de buée du matin reste sur le rouge.",
    ),
    (1, 1, 2): (
        "Le seau bleu frotte une miette, sous la table.",
        "La lumière du matin entre dans le plastique.",
    ),
    (1, 1, 3): (
        "Le doudou a une oreille tiède, près de la soupe.",
        "Un rond de buée du matin s'efface tout doux.",
    ),
    (1, 2, 1): (
        "Au jardin, le ballon tire vers la grande flaque.",
        "L'herbe du matin colle au plastique rouge.",
    ),
    (1, 2, 2): (
        "Le seau bleu attend près du romarin mouillé.",
        "La flaque du matin est encore très ronde.",
    ),
    (1, 2, 3): (
        "Le doudou s'assoit sur le banc froid du matin.",
        "Une goutte d'herbe brille sur son oreille.",
    ),
    (1, 3, 1): (
        "Dans la chambre, le ballon était sous le lit.",
        "Un rayon du matin le rend tout rose.",
    ),
    (1, 3, 2): (
        "Le seau tambour redevient un seau, le matin.",
        "La chaise garde encore le pli du manteau.",
    ),
    (1, 3, 3): (
        "Le doudou sort de la couverture du matin.",
        "Il sent encore le lit, tout chaud.",
    ),
    (2, 1, 1): (
        "Après la sieste, le ballon nage dans la vapeur.",
        "La tasse cliquette encore, dans la cuisine.",
    ),
    (2, 1, 2): (
        "Le seau bleu est tiède, sous la table.",
        "La soupe de la sieste fume encore.",
    ),
    (2, 1, 3): (
        "Le doudou sent la soupe, près du bol.",
        "La buée de la sieste mouille un peu le tissu.",
    ),
    (2, 2, 1): (
        "Au jardin, le ballon flotte au-dessus de la pierre tiède.",
        "La flaque a déjà perdu un bout, après la sieste.",
    ),
    (2, 2, 2): (
        "Le seau bleu se pose près du romarin chaud.",
        "Après la sieste, l'eau de la flaque est tiède.",
    ),
    (2, 2, 3): (
        "Le doudou s'installe sur la pierre chaude du jardin.",
        "Une abeille passe, après la sieste.",
    ),
    (2, 3, 1): (
        "Dans la chambre, le ballon roule du lit de la sieste.",
        "Le rideau bouge encore, tout lent.",
    ),
    (2, 3, 2): (
        "Le seau tambour est resté près du lit chaud.",
        "Après la sieste, le bois de la chaise est doux.",
    ),
    (2, 3, 3): (
        "Le doudou a gardé le creux de la sieste.",
        "La couverture reste un peu pliée.",
    ),
    (3, 1, 1): (
        "Le soir, le ballon rouge prend la lumière de la lampe.",
        "Une miette dore encore, dans la cuisine.",
    ),
    (3, 1, 2): (
        "Le seau bleu brille sous la lampe du soir.",
        "Les bols de soupe sont vides, tout calmes.",
    ),
    (3, 1, 3): (
        "Le doudou a une oreille d'or, sous la lampe.",
        "Le soir, la soupe sent encore, tout bas.",
    ),
    (3, 2, 1): (
        "Au jardin, le ballon passe devant le réverbère.",
        "La flaque du soir est noire et ronde.",
    ),
    (3, 2, 2): (
        "Le seau bleu entre dans l'eau sombre du soir.",
        "Le manteau jaune fait une lanterne, au jardin.",
    ),
    (3, 2, 3): (
        "Le doudou regarde le réverbère, tout sage.",
        "Une feuille du soir tremble près du banc.",
    ),
    (3, 3, 1): (
        "Dans la chambre, le ballon roule vers la petite lampe.",
        "Le soir, le rideau est déjà fermé à demi.",
    ),
    (3, 3, 2): (
        "Le seau bleu attend au pied du lit, le soir.",
        "La petite lampe pose un rond sur le plastique.",
    ),
    (3, 3, 3): (
        "Le doudou et la petite lampe se touchent, le soir.",
        "La chambre est calme, avant la flaque.",
    ),
}

FIN6 = {
    (1, 1, 1): "Le ballon reste au-dessus du rond essuyé, le matin.",
    (1, 1, 2): "Une miette du matin flotte dans le seau plein.",
    (1, 1, 3): "L'oreille du doudou a séché, près du bol.",
    (1, 2, 1): "Le rouge du ballon se mêle à l'herbe mouillée.",
    (1, 2, 2): "Une goutte froide reste sur la manche jaune.",
    (1, 2, 3): "Le banc garde un rond d'eau, tout petit.",
    (1, 3, 1): "Le rayon du matin suit le ballon jusqu'à la porte.",
    (1, 3, 2): "Le seau ne fait plus tambour, seulement de l'eau.",
    (1, 3, 3): "La couverture reste ouverte, encore chaude.",
    (2, 1, 1): "Un nuage de vapeur entoure encore le ballon.",
    (2, 1, 2): "Le seau sent la soupe et la flaque, ensemble.",
    (2, 1, 3): "Le doudou a une mèche un peu humide de buée.",
    (2, 2, 1): "La pierre tiède a gardé une ombre de ballon.",
    (2, 2, 2): "Le romarin sent plus fort, après l'eau.",
    (2, 2, 3): "Une abeille a quitté le doudou, tout loin.",
    (2, 3, 1): "Le lit de la sieste a perdu son ballon.",
    (2, 3, 2): "Le bois de la chaise n'a plus le seau.",
    (2, 3, 3): "Le creux du doudou s'est un peu défait.",
    (3, 1, 1): "La lampe du soir se reflète dans le rouge.",
    (3, 1, 2): "Le seau bleu a un rond de lampe, tout calme.",
    (3, 1, 3): "L'oreille d'or du doudou s'est assombrie.",
    (3, 2, 1): "Le réverbère suit le ballon, tout bas.",
    (3, 2, 2): "L'eau sombre tremble dans le seau.",
    (3, 2, 3): "Le doudou a vu le réverbère s'éteindre un peu.",
    (3, 3, 1): "La petite lampe reste allumée, sans le ballon.",
    (3, 3, 2): "Le pied du lit n'a plus le seau bleu.",
    (3, 3, 3): "La petite lampe éclaire encore le doudou revenu.",
}


def l3_006(i: int, j: int, k: int) -> list[str]:
    a, b = OPEN6[(i, j, k)]
    when = MOM[i]
    where = ROOM6[j]
    if k == 1:
        act = L(
            "narrateur|Nina attache le ballon au seau.",
            "narrateur|Le ballon tire un peu vers la porte.",
            "enfant-f|Il veut la flaque.",
            "papa|Toi d'abord, avec tes affaires.",
        )
    elif k == 2:
        act = L(
            "narrateur|Nina prend le seau à deux mains.",
            "narrateur|Le plastique est un peu froid.",
            "enfant-f|Pour la flaque.",
            "maman|Tu as repris tes affaires.",
        )
    else:
        act = L(
            "narrateur|Nina glisse le doudou dans le manteau.",
            "narrateur|Une oreille dépasse, toute douce.",
            "enfant-f|Il vient.",
            "papa|Lui aussi.",
        )
    return L(
        f"narrateur|{a}",
        f"narrateur|{b}",
        *act,
        f"narrateur|Ils quittent {where}, {when}.",
        "narrateur|Le manteau jaune tape un peu sa jambe.",
        "maman|Avant de partir, tu avais tout ?",
        "enfant-f|Le manteau.",
        "enfant-f|Et ça.",
        "papa|La flaque est à vous.",
    )


def fin_006(i: int, j: int, k: int) -> list[str]:
    img = FIN6[(i, j, k)]
    obj = OBJ6[k]
    return L(
        "narrateur|La flaque fait un petit cercle.",
        f"narrateur|Nina pose {obj} tout près.",
        "enfant-f|On y est.",
        "maman|Tu as tes affaires.",
        "papa|Le manteau te tient chaud.",
        "enfant-f|Merci.",
        f"narrateur|{img}",
        "narrateur|Une goutte de soupe a séché, sur la vitre.",
    )


Q006 = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | avant de partir | elle reprend",
    "retry_prompt": "Elle reprend ses affaires. Que fait Nina ?",
}


def build_006() -> None:
    scripts: dict[str, list[str]] = {
        "CHK_T0000_P0000": debut_006(),
        "CHK_T0001_P0000": tq1_006(),
    }
    q: dict[str, dict] = {}
    for i in (1, 2, 3):
        scripts[f"CHK_T0001_P000{i}"] = l1_006(i)
        qid = f"CHK_T0001_P000{i}_Q0001"
        scripts[qid] = q_006(i)
        q[qid] = Q006
        scripts[f"CHK_T0001_P000{i}_C0001"] = c_006(i)
        scripts[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_006()
        for j in (1, 2, 3):
            scripts[f"CHK_T0001_P000{i}_T0002_P000{j}"] = l2_006(i, j)
            scripts[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"] = tq3_006()
            for k in (1, 2, 3):
                scripts[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"] = l3_006(i, j, k)
                scripts[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin_006(i, j, k)
    write_merged(
        "TREE-AUT-006",
        {
            "fil_rouge": (
                "Nina veut la flaque du jardin. La vitre est embuée, ça sent la soupe. "
                "Elle reprend le manteau jaune et ses affaires avant de partir."
            ),
            "title": "Le manteau jaune de Nina",
            "characters": "Nina, papa, maman",
            "setting": "cuisine embuée, manteau jaune, flaque du jardin",
        },
        scripts,
        q,
    )


# ---------------------------------------------------------------------------
# TREE-AUT-007 — Victorina, volets de bois, pain, séquence vécue. N3 AUT.ROU.001
# T1 chambre / salle d'eau / cuisine   T2 t-shirt / chaussettes / gilet   T3 sac / manteau / doudou
# ---------------------------------------------------------------------------

ROOM7 = {1: "la chambre", 2: "la salle d'eau", 3: "la cuisine"}
CLO7 = {1: "le t-shirt", 2: "les chaussettes", 3: "le gilet"}
OBJ7 = {1: "le sac", 2: "le manteau", 3: "le doudou"}


def debut_007() -> list[str]:
    return L(
        "narrateur|Un volet de bois claque contre le mur.",
        "narrateur|Le bois est encore froid.",
        "narrateur|Une bande de soleil tombe sur le parquet.",
        "narrateur|Le parquet est déjà tiède.",
        "narrateur|Une odeur de pain monte l'escalier.",
        "narrateur|Le pain est encore tout chaud.",
        "narrateur|Dehors, un moineau picore la gouttière.",
        "narrateur|La gouttière fait tic, tic.",
        "papa|Le pain est sous le linge.",
        "maman|Victorina, le volet a bougé.",
        "narrateur|La couverture pique un peu.",
        "narrateur|Elle sent le savon.",
        "narrateur|Le radiateur fait un petit clic.",
        "narrateur|En ce moment, Victorina ouvre les yeux.",
        "enfant-f|Le moineau.",
        "enfant-f|Et le pain.",
        "maman|Le pain t'attend en bas.",
        "papa|Le volet d'abord, si tu veux le voir.",
        "narrateur|Victorina pousse la couverture.",
        "narrateur|Un pied trouve le tapis.",
        "narrateur|L'autre pied cherche encore.",
        "enfant-f|J'y vais.",
        "narrateur|Elle se lève trop vite.",
        "narrateur|Une chaussette glisse du lit.",
        "maman|Une chose, puis la suivante.",
        "papa|Tu as dormi ?",
        "enfant-f|Oui, papa.",
    )


def tq1_007() -> list[str]:
    return L(
        "narrateur|Victorina va où d'abord ?",
        "maman|La chambre, la salle d'eau, ou la cuisine.",
    )


def l1_007(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Victorina pousse le volet de la chambre.",
            "narrateur|Le bois claque encore, tout fort.",
            "narrateur|Le moineau s'envole d'un coup.",
            "enfant-f|Reviens.",
            "narrateur|De l'autre main, elle prend le t-shirt.",
            "narrateur|La chaussette tombe dans la fente du volet.",
            "papa|Le volet d'abord.",
            "maman|Une chose, puis la suivante.",
            "narrateur|Victorina tient le bois, tout calme.",
            "narrateur|Le volet s'arrête.",
            "narrateur|Le moineau revient sur la gouttière.",
            "enfant-f|Il est là.",
            "papa|Maintenant le t-shirt.",
            "maman|Le pain attend encore, en bas.",
            "narrateur|Le parquet est tiède sous un pied nu.",
        )
    if i == 2:
        return L(
            "narrateur|Victorina entre dans la salle d'eau.",
            "narrateur|L'eau du robinet est trop froide.",
            "enfant-f|Aïe.",
            "narrateur|Elle se dépêche, les mains mouillées.",
            "narrateur|Elle attrape le sac, tout de suite.",
            "narrateur|La fermeture glisse et reste coincée.",
            "maman|Tes mains d'abord.",
            "papa|Une chose, puis la suivante.",
            "narrateur|Elle prend la serviette rêche.",
            "narrateur|Les mains deviennent sèches.",
            "narrateur|La fermeture part, tout doux.",
            "enfant-f|Ça y est.",
            "papa|Le pain n'a pas bougé.",
            "maman|Tu peux y aller après le t-shirt.",
            "narrateur|Une goutte reste sur le carrelage.",
        )
    return L(
        "narrateur|Victorina descend vers la cuisine.",
        "narrateur|Le carrelage est froid sous les pieds nus.",
        "narrateur|Le pain fume encore, sous le linge.",
        "enfant-f|Il est à moi.",
        "narrateur|Elle est encore en pyjama.",
        "narrateur|Un courant d'air passe dans le dos.",
        "papa|Le pain t'attend.",
        "maman|Les vêtements d'abord, sur le carrelage froid.",
        "narrateur|Victorina recule d'un pas.",
        "enfant-f|Mes pieds.",
        "papa|Une chose, puis la suivante.",
        "maman|Le gilet est sur la chaise.",
        "narrateur|Le linge du pain reste baissé.",
        "narrateur|Ça sent encore le four.",
        "enfant-f|J'y vais après.",
    )


def q_007(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Le volet claque.",
            "narrateur|Comment Victorina continue-t-elle ?",
        )
    if i == 2:
        return L(
            "narrateur|Ses mains sont mouillées.",
            "narrateur|Comment se prépare-t-elle ?",
        )
    return L(
        "narrateur|Le carrelage est froid.",
        "narrateur|Comment vient-elle au pain ?",
    )


def c_007(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Victorina a tenu le volet.",
            "narrateur|Le moineau est resté.",
            "maman|Une chose, puis la suivante.",
            "papa|Le t-shirt maintenant.",
            "enfant-f|Puis le pain.",
            "maman|Merci.",
            "narrateur|La chaussette attend encore près du bois.",
        )
    if i == 2:
        return L(
            "narrateur|Les mains sont sèches.",
            "narrateur|Le sac s'ouvre sans rien coincer.",
            "papa|Une chose, puis la suivante.",
            "maman|Tu as séché d'abord.",
            "enfant-f|Puis le zip.",
            "papa|Merci, Victorina.",
            "narrateur|L'eau du robinet s'est tue.",
        )
    return L(
        "narrateur|Victorina pose un pied sur le tapis de la cuisine.",
        "narrateur|L'autre pied suit.",
        "maman|Une chose, puis la suivante.",
        "papa|Les vêtements, puis le pain.",
        "enfant-f|Le pain attend.",
        "maman|Oui.",
        "narrateur|Le linge garde la chaleur.",
    )


def tq2_007() -> list[str]:
    return L(
        "narrateur|Ensuite, quel vêtement ?",
        "papa|Le t-shirt, les chaussettes, ou le gilet.",
    )


def l2_007(i: int, j: int) -> list[str]:
    where = ROOM7[i]
    if j == 1:
        place = {
            1: "Il est plié dans le tiroir de la chambre.",
            2: "Il pend à la patère de la salle d'eau.",
            3: "Il attend sur le dossier, dans la cuisine.",
        }[i]
        return L(
            f"narrateur|Dans {where}, Victorina prend le t-shirt.",
            f"narrateur|{place}",
            "narrateur|Le coton est doux et un peu froid.",
            "enfant-f|La tête.",
            "narrateur|Elle passe la tête, puis les manches.",
            "papa|Les manches sont bonnes ?",
            "enfant-f|Oui, papa.",
            "maman|Une chose, c'est faite.",
            "narrateur|Le pyjama tombe sur le bois.",
            "papa|Ensuite on verra la suite.",
            "enfant-f|Le pain après.",
            "narrateur|Le coton se réchauffe déjà.",
        )
    if j == 2:
        sock = {
            1: "Une chaussette était dans la fente du volet.",
            2: "Une chaussette était mouillée, près du carrelage.",
            3: "Une chaussette était sous la table, près du pain.",
        }[i]
        return L(
            f"narrateur|Dans {where}, Victorina cherche les chaussettes.",
            f"narrateur|{sock}",
            "enfant-f|Je l'ai.",
            "narrateur|Elle enfile une chaussette, puis l'autre.",
            "maman|Un pied, puis l'autre.",
            "papa|Elles sont paires ?",
            "enfant-f|Oui.",
            "narrateur|Les pieds ne glissent plus.",
            "maman|Une chose, puis la suivante.",
            "enfant-f|Mes pieds sont au chaud.",
            "papa|Le pain n'a pas bougé.",
            "narrateur|Le bois du sol sonne moins fort.",
        )
    vest = {
        1: "Le gilet coupe le courant d'air du volet.",
        2: "Le gilet réchauffe après l'eau froide.",
        3: "Le gilet pose une laine sur le carrelage froid.",
    }[i]
    return L(
        f"narrateur|Dans {where}, Victorina prend le gilet.",
        f"narrateur|{vest}",
        "narrateur|Un bouton résiste un peu.",
        "enfant-f|Il veut pas.",
        "papa|Ce bouton-ci, d'abord.",
        "narrateur|Le bouton passe.",
        "maman|Une chose, puis la suivante.",
        "enfant-f|J'ai chaud.",
        "papa|Le pain va goûter meilleur, comme ça.",
        "narrateur|La laine gratte un tout petit peu.",
        "maman|Tu es prête pour la suite ?",
        "enfant-f|Oui, maman.",
    )


def tq3_007() -> list[str]:
    return L(
        "narrateur|Ensuite, le sac, le manteau, ou le doudou ?",
    )


OPEN7 = {
    (1, 1, 1): (
        "Dans la chambre, le sac frotte le t-shirt encore froid.",
        "Au volet, le moineau reste, tout calme.",
    ),
    (1, 1, 2): (
        "Dans la chambre, le manteau sent le bois du volet.",
        "Sous le manteau, le t-shirt est déjà moins froid.",
    ),
    (1, 1, 3): (
        "Dans la chambre, le doudou a vu le moineau, lui aussi.",
        "Un pli du tiroir reste sur le t-shirt.",
    ),
    (1, 2, 1): (
        "Au pied du volet, le sac heurte une chaussette.",
        "Plus aucun claquement, dans le bois.",
    ),
    (1, 2, 2): (
        "Sur les chaussettes chaudes, le manteau tombe.",
        "Derrière le bois, le moineau picore encore.",
    ),
    (1, 2, 3): (
        "Sur la chaussette retrouvée, le doudou s'assoit.",
        "Sous les pieds, le parquet de la chambre est tiède.",
    ),
    (1, 3, 1): (
        "Contre le gilet boutonné, le sac de la chambre appuie.",
        "Un courant d'air du volet s'arrête là.",
    ),
    (1, 3, 2): (
        "Par-dessus le gilet de laine, le manteau passe.",
        "Plus de claquement, dans le bois du volet.",
    ),
    (1, 3, 3): (
        "Sous le gilet, le doudou se glisse, tout petit.",
        "Sur la gouttière, le moineau reste.",
    ),
    (2, 1, 1): (
        "Dans la salle d'eau, le sac s'ouvre avec des mains sèches.",
        "Près du col, le t-shirt a une goutte.",
    ),
    (2, 1, 2): (
        "Loin de l'eau, le manteau attend près du t-shirt.",
        "La serviette rêche est repliée.",
    ),
    (2, 1, 3): (
        "Loin du robinet, le doudou n'a pas touché l'eau.",
        "Sur le t-shirt, ça sent encore le savon.",
    ),
    (2, 2, 1): (
        "Dans la salle d'eau, le sac évite la chaussette mouillée.",
        "Victorina a pris la paire sèche.",
    ),
    (2, 2, 2): (
        "Loin de la flaque du carrelage, le manteau reste.",
        "Les chaussettes sèches tiennent chaud.",
    ),
    (2, 2, 3): (
        "Sur le tabouret, le doudou attend, loin de l'eau.",
        "Une chaussette sèche touche son pied.",
    ),
    (2, 3, 1): (
        "Dans la salle d'eau, le sac appuie sur le gilet chaud.",
        "L'eau du robinet est fermée.",
    ),
    (2, 3, 2): (
        "Loin du robinet, le manteau recouvre le gilet.",
        "Plus aucune goutte sur les mains.",
    ),
    (2, 3, 3): (
        "Dans le gilet, le doudou se cache, tout sec.",
        "La salle d'eau ne goutte plus.",
    ),
    (3, 1, 1): (
        "Dans la cuisine, le sac se pose loin du pain chaud.",
        "Près du four, le t-shirt a déjà moins froid.",
    ),
    (3, 1, 2): (
        "Dans la cuisine, le manteau sent le pain, tout de suite.",
        "Sur le dos, le t-shirt tient chaud.",
    ),
    (3, 1, 3): (
        "Près du t-shirt, le doudou s'assoit, face au linge.",
        "Sous le linge, le pain fume encore.",
    ),
    (3, 2, 1): (
        "Dans la cuisine, le sac évite les miettes.",
        "Sur le carrelage, les pieds ne glissent plus.",
    ),
    (3, 2, 2): (
        "Sur les chaussettes chaudes, le manteau de la cuisine tombe.",
        "Sous le linge, le pain bouge un peu.",
    ),
    (3, 2, 3): (
        "Près du four, le doudou a une chaussette contre lui.",
        "Sous les pieds, le carrelage n'est plus si froid.",
    ),
    (3, 3, 1): (
        "Contre le gilet de laine, le sac de la cuisine s'appuie.",
        "Sous le linge, le pain attend encore.",
    ),
    (3, 3, 2): (
        "Dans la cuisine, le manteau passe sur le gilet.",
        "Dans le dos, le courant d'air s'est tu.",
    ),
    (3, 3, 3): (
        "Face au pain, le doudou se loge dans le gilet.",
        "Une miette tinte dans le bol du chat.",
    ),
}

FIN7 = {
    (1, 1, 1): "Au pied du volet, le sac reste, le moineau picore.",
    (1, 1, 2): "Sous le manteau, ça sent le bois, le pain casse.",
    (1, 1, 3): "Une miette reste au doudou, le moineau est là.",
    (1, 2, 1): "Contre le sac, une chaussette, le pain est chaud.",
    (1, 2, 2): "Sous le manteau, les pieds restent au chaud.",
    (1, 2, 3): "Avec la chaussette, le doudou voit le volet calme.",
    (1, 3, 1): "Contre le gilet, le sac, le moineau fait tic.",
    (1, 3, 2): "Ensemble, le manteau et le gilet sentent le pain.",
    (1, 3, 3): "Une croûte tout petite reste au doudou du gilet.",
    (2, 1, 1): "Sur le carrelage, une goutte a séché, le sac est sec.",
    (2, 1, 2): "Loin de l'eau, le manteau, le pain casse.",
    (2, 1, 3): "Ça sent le savon et le pain, sur le doudou.",
    (2, 2, 1): "Loin de l'eau, le sac, la croûte craque.",
    (2, 2, 2): "Au sec, le manteau, les pieds, le pain fume.",
    (2, 2, 3): "Sur le tabouret, le doudou a une miette sèche.",
    (2, 3, 1): "Loin du robinet, le sac et le gilet sont chauds.",
    (2, 3, 2): "Plus de goutte, le manteau sur le gilet, le pain.",
    (2, 3, 3): "Sans eau, le doudou du gilet a seulement du pain.",
    (3, 1, 1): "Loin des miettes, le sac, le linge est relevé.",
    (3, 1, 2): "Près du four, le manteau, une croûte casse.",
    (3, 1, 3): "Face au linge, le doudou a la première miette.",
    (3, 2, 1): "Près des chaussettes, le sac, le bol du chat tinte.",
    (3, 2, 2): "Avec les chaussettes, le manteau, le pain est à elle.",
    (3, 2, 3): "Une chaussette et une miette restent au doudou.",
    (3, 3, 1): "Contre le gilet, le sac, le linge retombe vide.",
    (3, 3, 2): "Plus de froid, le manteau sur le gilet, le pain.",
    (3, 3, 3): "Dans le gilet, le doudou, le bol du chat est calme.",
}


def l3_007(i: int, j: int, k: int) -> list[str]:
    a, b = OPEN7[(i, j, k)]
    if k == 1:
        act = L(
            "narrateur|Victorina ouvre le sac.",
            "narrateur|Elle glisse la gourde, tout au fond.",
            "enfant-f|Le sac est prêt.",
            "papa|Cette chose-ci, c'est faite.",
        )
    elif k == 2:
        act = L(
            "narrateur|Victorina passe le manteau.",
            "narrateur|Une manche cherche encore la main.",
            "enfant-f|Pour le pas de la porte.",
            "maman|Cette chose-ci, c'est faite.",
        )
    else:
        act = L(
            "narrateur|Victorina prend le doudou contre la joue.",
            "narrateur|Le tissu est encore un peu chaud.",
            "enfant-f|Il vient au pain.",
            "papa|Cette chose-ci, c'est faite.",
        )
    return L(
        f"narrateur|{a}",
        f"narrateur|{b}",
        *act,
        "maman|Une chose, puis la suivante.",
        "narrateur|Ils descendent vers le pain.",
        "narrateur|Ça sent le four, tout près.",
        "enfant-f|Maintenant le pain.",
        "papa|Oui.",
        "narrateur|Le linge se soulève, tout doux.",
    )


def fin_007(i: int, j: int, k: int) -> list[str]:
    img = FIN7[(i, j, k)]
    obj = OBJ7[k]
    cloth = CLO7[j]
    return L(
        "narrateur|Papa coupe une tranche.",
        "narrateur|La croûte casse, tout net.",
        "enfant-f|Elle est chaude.",
        "maman|Tu as fait une chose, puis l'autre.",
        f"narrateur|Victorina pose {obj} près du bol.",
        f"narrateur|Elle a encore {cloth}.",
        "papa|Merci, Victorina.",
        f"narrateur|{img}",
        "narrateur|Derrière, un volet de bois se tait.",
    )


Q007 = {
    "expected_answer": "une chose",
    "accepted_examples": "une chose | puis l'autre | d'abord | doucement | puis la suivante | une chose puis l'autre",
    "retry_prompt": "Elle fait une chose, puis la suivante. Comment se prépare Victorina ?",
}


def build_007() -> None:
    scripts: dict[str, list[str]] = {
        "CHK_T0000_P0000": debut_007(),
        "CHK_T0001_P0000": tq1_007(),
    }
    q: dict[str, dict] = {}
    for i in (1, 2, 3):
        scripts[f"CHK_T0001_P000{i}"] = l1_007(i)
        qid = f"CHK_T0001_P000{i}_Q0001"
        scripts[qid] = q_007(i)
        q[qid] = Q007
        scripts[f"CHK_T0001_P000{i}_C0001"] = c_007(i)
        scripts[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_007()
        for j in (1, 2, 3):
            scripts[f"CHK_T0001_P000{i}_T0002_P000{j}"] = l2_007(i, j)
            scripts[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"] = tq3_007()
            for k in (1, 2, 3):
                scripts[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"] = l3_007(i, j, k)
                scripts[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin_007(i, j, k)
    write_merged(
        "TREE-AUT-007",
        {
            "fil_rouge": (
                "Victorina veut le pain chaud et le moineau du volet. "
                "Elle se lève trop vite. Une chose, puis la suivante : "
                "le volet, les vêtements, le pain."
            ),
            "title": "Le volet de Victorina",
            "characters": "Victorina, papa, maman",
            "setting": "maison, volets en bois, pain du matin",
        },
        scripts,
        q,
    )


if __name__ == "__main__":
    build_006()
    build_007()
