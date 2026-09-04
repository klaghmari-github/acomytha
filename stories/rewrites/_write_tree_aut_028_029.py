#!/usr/bin/env python3
"""TREE-AUT-028 / TREE-AUT-029 — 86 ids, D16, 3 branches vécues, leçon implicite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

EXTRA_BAD = (
    "sami", "hugo", "tom ", "léa", "lea ", "sarah",
    "on va ranger", "tu ranges", "après le jeu",
    "l'histoire est finie", "c'est du bon travail",
)


def extras_t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def extras_q(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


def preview(sid: str, age: str, scripts: dict) -> None:
    lim = {"N1": 10, "N2": 15, "N3": 16}[age]
    n = 0
    for cid, lines in scripts.items():
        prev = ""
        run = 1
        for raw in lines:
            role, phrase = raw.split("|", 1)
            w = words(phrase)
            n += w
            if w > lim:
                raise SystemExit(f"LONG {sid} {cid} {w}>{lim}: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"MULTI {sid} {cid}: {phrase}")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"PUNCT {sid} {cid}: {phrase}")
            tok = phrase.split()[0].lower() if role == "narrateur" else ""
            if tok and tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"PUCES {sid} {cid}: {tok}")
            else:
                run = 1
            prev = tok
    print(f"preview {sid} {n} mots  chunks={len(scripts)}")


def write_tree(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    extras: dict,
    extra_ban: tuple[str, ...] = (),
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    preview(sid, src["age_band"], scripts)
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
        elif src.get("age_band") == "N1":
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
    for bad in EXTRA_BAD + extra_ban:
        if bad in joined:
            raise SystemExit(f"{sid} extra interdit: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_lines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        if not last_lines:
            raise SystemExit(f"{sid} {c['chunk_id']}: fin sans narrateur")
        last = last_lines[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} fin mécanique: {last}")
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")


# ---------------------------------------------------------------------------
# TREE-AUT-028  N3  AUT.AFF.003  Victorino  seau vert
# T1 parc  T2 jeu  T3 banc / sac / portail  (plus Tom/Léa/Sami)
# ---------------------------------------------------------------------------

L1_028 = {
    1: {
        "label": "le bac à sable",
        "ou": "au bac à sable",
        "quit": "le bac à sable",
        "leave": "Un grain de sable reste sur l'anse.",
    },
    2: {
        "label": "le toboggan",
        "ou": "au toboggan",
        "quit": "le toboggan",
        "leave": "Une goutte glisse encore sur la rampe.",
    },
    3: {
        "label": "les balançoires",
        "ou": "aux balançoires",
        "quit": "les balançoires",
        "leave": "Une chaîne fait cling, tout léger.",
    },
}
L2_028 = {
    1: {"label": "le ballon", "en": "le ballon sous le bras"},
    2: {"label": "le seau", "en": "le seau vert dans les mains"},
    3: {"label": "le doudou", "en": "le doudou contre la poitrine"},
}
L3_028 = {
    1: {
        "label": "le banc",
        "arrive": "Le banc de bois est un peu chaud.",
        "obj": "Le manteau gris est plié dessus.",
        "first": "le manteau",
    },
    2: {
        "label": "le sac",
        "arrive": "Le sac d'osier attend dans l'herbe.",
        "obj": "Le seau vert est juste à côté.",
        "first": "le seau",
    },
    3: {
        "label": "le portail",
        "arrive": "Le portail du parc est un peu frais.",
        "obj": "Le doudou est assis contre le barreau.",
        "first": "le doudou",
    },
}

ARRIVE_028 = {
    1: [
        "narrateur|Victorino s'agenouille au bord du bac.",
        "narrateur|Le sable est frais, un peu lourd.",
        "narrateur|Ça fait chh quand il verse.",
        "papa|Ça fait chh, tu as entendu ?",
        "enfant-m|Oui.",
        "enfant-m|Le sable chante.",
        "narrateur|Le seau vert se remplit, puis se vide.",
        "maman|Le manteau gris est sur le banc.",
        "papa|Le doudou aussi, tout près.",
        "narrateur|Victorino enfonce les mains.",
        "narrateur|Le fond du bac est froid.",
        "enfant-m|Un château, tout petit.",
        "papa|Le seau reste à ta droite ?",
        "enfant-m|Oui, tout près.",
        "maman|Tes joues sont déjà roses.",
        "narrateur|Un grain reste sous son ongle.",
    ],
    2: [
        "narrateur|Le toboggan brille encore un peu.",
        "narrateur|Les marches sont froides sous la main.",
        "narrateur|Victorino pose le pied, tout doux.",
        "enfant-m|Je glisse !",
        "papa|J'attends en bas.",
        "narrateur|Le seau vert est près des bottes.",
        "maman|Le manteau est au crochet, gris.",
        "papa|Le doudou est dans le sac, lui.",
        "narrateur|Victorino glisse.",
        "narrateur|Le plastique fait un petit frou.",
        "narrateur|Ses pieds retrouvent l'herbe.",
        "enfant-m|Encore une fois.",
        "papa|Une fois, oui.",
        "maman|Tes mains sont mouillées.",
        "narrateur|Une feuille colle à la rampe.",
    ],
    3: [
        "narrateur|Les chaînes des balançoires sont froides.",
        "narrateur|Elles font un bruit de goutte.",
        "narrateur|Victorino s'assoit.",
        "narrateur|Le siège est encore un peu humide.",
        "enfant-m|Un peu, maman.",
        "maman|Je pousse tout doux.",
        "papa|Le manteau reste au poteau ?",
        "enfant-m|Oui, au crochet.",
        "narrateur|Le seau vert est sous le banc.",
        "maman|Le doudou aussi, juste à côté.",
        "narrateur|Victorino avance, puis revient.",
        "narrateur|Le vent lui touche le nez.",
        "enfant-m|Je vois le ciel.",
        "papa|Tu t'es arrêté tout seul.",
        "narrateur|Une flaque reflète le ciel, tout près.",
    ],
}

Q_028 = {
    1: [
        "narrateur|Le seau vert est encore au bac.",
        "papa|Victorino, tu prends quoi ?",
    ],
    2: [
        "narrateur|Le manteau gris est encore au crochet.",
        "maman|Victorino, tu prends quoi ?",
    ],
    3: [
        "narrateur|Le doudou est encore sous le banc.",
        "papa|Victorino, tu cherches quoi ?",
    ],
}

C_028 = {
    1: [
        "narrateur|Victorino revient vers le bac.",
        "narrateur|Il prend le seau vert à deux mains.",
        "enfant-m|Il était là.",
        "papa|Oui.",
        "papa|Il t'attendait.",
        "maman|Le manteau est encore sur le banc.",
        "narrateur|Un grain de sable reste sur sa joue.",
        "papa|Merci, Victorino.",
    ],
    2: [
        "narrateur|Victorino revient vers le crochet.",
        "narrateur|Il décroche le manteau gris.",
        "enfant-m|Il fait toc.",
        "maman|Oui.",
        "maman|Il était encore là.",
        "papa|Le seau vert est près des bottes.",
        "narrateur|Une goutte glisse de la manche.",
        "maman|Merci, Victorino.",
    ],
    3: [
        "narrateur|Victorino se penche sous le banc.",
        "narrateur|Il sort le doudou, tout doux.",
        "enfant-m|Il sent le vent.",
        "papa|Oui.",
        "papa|Il t'attendait.",
        "maman|Le seau vert est juste à côté.",
        "narrateur|L'oreille du doudou est un peu humide.",
        "papa|Merci, Victorino.",
    ],
}

PLAY_028 = {
    (1, 1): [
        "narrateur|Près du bac, le ballon est un peu sablé.",
        "narrateur|Victorino le fait rouler.",
        "narrateur|Ça fait poum contre le bois.",
        "enfant-m|Le ballon, papa.",
        "papa|Oui.",
        "papa|Le seau vert reste à ta droite.",
        "maman|Le manteau reste sur le banc.",
        "narrateur|Le ballon s'arrête contre le seau.",
        "enfant-m|Ils se parlent.",
        "maman|Tout doux, oui.",
        "narrateur|Un grain colle au cuir, tout fin.",
    ],
    (1, 2): [
        "narrateur|Près du bac, le seau vert attend.",
        "narrateur|Victorino le remplit encore une fois.",
        "enfant-m|Pour le château.",
        "papa|D'accord.",
        "papa|Puis on le garde avec nous.",
        "maman|Le manteau est encore sur le banc.",
        "narrateur|Le sable retombe, tout fin.",
        "enfant-m|L'anse est un peu froide.",
        "maman|Le doudou regarde depuis la chaise.",
        "narrateur|Un grain brille au fond du seau.",
    ],
    (1, 3): [
        "narrateur|Près du bac, le doudou a du sable.",
        "narrateur|Victorino le secoue, tout doux.",
        "enfant-m|Il a une oreille pliée.",
        "maman|Comme tout à l'heure, sur l'oreiller.",
        "papa|Le seau vert est encore à droite.",
        "narrateur|Victorino pose le doudou sur le rebord.",
        "enfant-m|Il voit le château.",
        "maman|Le manteau, lui, reste sur le banc.",
        "narrateur|L'oreille grise a un grain, tout petit.",
    ],
    (2, 1): [
        "narrateur|Au pied du toboggan, le ballon rebondit une fois.",
        "narrateur|Il est un peu froid, près de la rampe.",
        "enfant-m|Il est rond, papa.",
        "papa|Comme une goutte, presque.",
        "maman|Le seau vert est près des bottes.",
        "narrateur|Victorino le serre sous le bras.",
        "enfant-m|Il vient avec moi.",
        "papa|Le manteau est encore au crochet.",
        "narrateur|Une feuille sèche tourne sur le sol.",
        "maman|Le doudou est dans le sac, au chaud.",
    ],
    (2, 2): [
        "narrateur|Au toboggan, le seau vert sonne contre une marche.",
        "narrateur|L'anse est un peu froide.",
        "enfant-m|C'est le mien.",
        "maman|Oui.",
        "maman|On le garde.",
        "papa|Le manteau est au crochet, gris.",
        "narrateur|Victorino le pose près des bottes.",
        "enfant-m|Il attend.",
        "maman|Le doudou aussi, dans le sac.",
        "narrateur|Une goutte sèche sur l'herbe, près de l'anse.",
    ],
    (2, 3): [
        "narrateur|Au toboggan, le doudou est dans le sac.",
        "narrateur|Victorino le sort, tout doux.",
        "enfant-m|Il a vu la rampe.",
        "papa|Oui.",
        "papa|Il revient avec nous.",
        "maman|Le seau vert est près des bottes.",
        "narrateur|Victorino le serre contre sa joue.",
        "enfant-m|Il est un peu froid.",
        "maman|Le manteau est encore au crochet.",
        "narrateur|Le tissu gris sent encore le sac.",
    ],
    (3, 1): [
        "narrateur|Près des balançoires, le ballon est dans l'herbe.",
        "narrateur|Un brin d'herbe colle au cuir.",
        "enfant-m|Il a de l'herbe, papa.",
        "papa|On le prend quand même.",
        "maman|Le seau vert est sous le banc.",
        "narrateur|Victorino rattrape le ballon.",
        "enfant-m|Il ne part pas sous la chaîne.",
        "papa|Le manteau reste au poteau.",
        "narrateur|Une flaque tremble quand il pose le pied.",
        "maman|Le doudou est sous le banc, lui aussi.",
    ],
    (3, 2): [
        "narrateur|Près des balançoires, le seau vert est sous le banc.",
        "narrateur|Victorino le tire par l'anse.",
        "enfant-m|Il est froid.",
        "maman|Comme la chaîne.",
        "papa|Le manteau est au poteau, gris.",
        "narrateur|Victorino le pose à côté de ses pieds.",
        "enfant-m|Il reste avec moi.",
        "maman|Le doudou est juste à côté, encore.",
        "narrateur|L'anse a un peu d'eau de la flaque.",
        "papa|On le verse dans l'herbe, tout doux.",
    ],
    (3, 3): [
        "narrateur|Près des balançoires, le doudou est sous le banc.",
        "narrateur|Victorino le sort, un peu humide.",
        "enfant-m|Il a senti le vent.",
        "papa|Oui.",
        "papa|Il revient.",
        "maman|Le seau vert est juste à côté.",
        "narrateur|Victorino le secoue, tout doux.",
        "enfant-m|L'oreille est froide.",
        "maman|Le manteau est encore au poteau.",
        "narrateur|La chaîne se tait un moment.",
    ],
}

FIND_028 = {
    (1, 1, 1): [
        "narrateur|Victorino prend le manteau sur le banc.",
        "papa|Tu as le manteau.",
        "maman|Le seau vert est encore à droite.",
        "narrateur|Il prend le seau, puis le doudou.",
        "narrateur|Le ballon reste sous son bras.",
    ],
    (1, 1, 2): [
        "narrateur|Victorino pose le seau vert dans le sac.",
        "maman|Oui.",
        "maman|Ensuite le manteau.",
        "papa|Il est sur le banc.",
        "narrateur|Il prend le manteau, puis le doudou.",
        "narrateur|Le ballon tapote le bord du sac.",
    ],
    (1, 1, 3): [
        "narrateur|Victorino serre le doudou près du portail.",
        "papa|Puis le seau vert.",
        "maman|Puis le manteau, sur le banc.",
        "enfant-m|Je les prends.",
        "narrateur|Le ballon reste sous son bras.",
    ],
    (1, 2, 1): [
        "narrateur|Le seau vert est déjà dans ses mains.",
        "narrateur|Victorino prend le manteau sur le banc.",
        "papa|Tu as le manteau.",
        "maman|Cherche le doudou, maintenant.",
        "narrateur|Il le prend sur la chaise du bac.",
        "narrateur|Un grain colle à la manche grise.",
    ],
    (1, 2, 2): [
        "narrateur|Victorino glisse le seau vert dans le sac.",
        "enfant-m|Il rentre.",
        "maman|Le manteau, maintenant.",
        "papa|Il est sur le banc.",
        "narrateur|Il prend le manteau, puis le doudou.",
        "narrateur|Le sable retombe un peu, dans l'herbe.",
    ],
    (1, 2, 3): [
        "narrateur|Le seau vert pèse déjà dans ses mains.",
        "narrateur|Victorino prend le doudou au portail.",
        "papa|Puis le manteau.",
        "maman|Il est resté au banc.",
        "enfant-m|Je le prends.",
        "narrateur|L'anse sonne tout doux contre le barreau.",
    ],
    (1, 3, 1): [
        "narrateur|Le doudou est déjà contre lui.",
        "narrateur|Victorino prend le manteau sur le banc.",
        "maman|Le seau vert, maintenant.",
        "papa|Il est encore au bac.",
        "enfant-m|Je le prends.",
        "narrateur|L'oreille grise dépasse du manteau.",
    ],
    (1, 3, 2): [
        "narrateur|Le doudou voyage déjà contre lui.",
        "narrateur|Victorino pose le seau vert dans le sac.",
        "papa|Le manteau, ensuite.",
        "maman|Sur le banc, gris.",
        "enfant-m|Je le prends.",
        "narrateur|Un grain de sable roule au fond du sac.",
    ],
    (1, 3, 3): [
        "narrateur|Le doudou était déjà près du barreau.",
        "narrateur|Victorino le serre, puis prend le seau.",
        "papa|Le manteau aussi.",
        "maman|Il est au banc.",
        "enfant-m|J'ai tout.",
        "narrateur|Le portail est froid sous sa main libre.",
    ],
    (2, 1, 1): [
        "narrateur|Au banc près du toboggan, le manteau fait toc.",
        "narrateur|Victorino le décroche du bois.",
        "papa|Le seau vert est près des bottes.",
        "enfant-m|Je le prends aussi.",
        "maman|Le doudou est dans le sac.",
        "narrateur|Le ballon reste sous son bras, un peu froid.",
    ],
    (2, 1, 2): [
        "narrateur|Victorino pose le seau vert dans le sac d'osier.",
        "maman|Tu as le seau.",
        "maman|Cherche le manteau.",
        "enfant-m|Au crochet.",
        "papa|Le doudou aussi.",
        "narrateur|Le ballon tapote le sac, tout mou.",
    ],
    (2, 1, 3): [
        "narrateur|Près du portail, Victorino a le ballon.",
        "narrateur|Il prend le doudou contre le barreau.",
        "papa|Le seau vert, près des bottes.",
        "maman|Le manteau, au crochet.",
        "enfant-m|Je les prends.",
        "narrateur|Une goutte sèche sur l'herbe, derrière eux.",
    ],
    (2, 2, 1): [
        "narrateur|Le seau vert sonne encore, près du banc.",
        "narrateur|Victorino prend le manteau au bois.",
        "papa|Tu as le manteau.",
        "maman|Le doudou est dans le sac, au chaud.",
        "enfant-m|Je le sors, puis il vient.",
        "narrateur|La rampe brille encore, derrière eux.",
    ],
    (2, 2, 2): [
        "narrateur|Victorino glisse le seau vert dans le sac.",
        "enfant-m|Il rentre, maman.",
        "maman|Le manteau, au crochet.",
        "papa|Le doudou aussi.",
        "narrateur|Il les prend, l'un puis l'autre.",
        "narrateur|L'anse jaune touche le bord d'osier.",
    ],
    (2, 2, 3): [
        "narrateur|Le seau vert est déjà avec lui.",
        "narrateur|Victorino prend le doudou au portail.",
        "papa|Le manteau, ensuite.",
        "maman|Au crochet du toboggan.",
        "enfant-m|Je le décroche.",
        "narrateur|Le métal de la rampe se tait.",
    ],
    (2, 3, 1): [
        "narrateur|Le doudou est déjà contre sa joue.",
        "narrateur|Victorino prend le manteau au banc.",
        "papa|Le seau vert, près des bottes.",
        "maman|On le prend.",
        "enfant-m|Je le prends.",
        "narrateur|Une feuille reste collée à la rampe.",
    ],
    (2, 3, 2): [
        "narrateur|Le doudou voyage déjà, tout gris.",
        "narrateur|Victorino pose le seau vert dans le sac.",
        "maman|Le manteau, au crochet.",
        "papa|Il vient aussi.",
        "enfant-m|Je le prends.",
        "narrateur|Le sac d'osier devient un peu lourd.",
    ],
    (2, 3, 3): [
        "narrateur|Le doudou retrouve le barreau un instant.",
        "narrateur|Victorino le reprend, puis le seau.",
        "papa|Le manteau, au crochet.",
        "maman|On n'oublie rien.",
        "enfant-m|J'ai tout.",
        "narrateur|Le portail cliquette, tout bas.",
    ],
    (3, 1, 1): [
        "narrateur|Au poteau, le manteau gris fait toc.",
        "narrateur|Victorino le décroche.",
        "papa|Le seau vert est sous le banc.",
        "maman|Le doudou aussi.",
        "enfant-m|Je me penche.",
        "narrateur|Le ballon reste dans l'herbe un instant, puis il le prend.",
    ],
    (3, 1, 2): [
        "narrateur|Victorino pose le seau vert dans le sac.",
        "maman|Il est froid, encore.",
        "papa|Le manteau est au poteau.",
        "enfant-m|Je le prends.",
        "maman|Le doudou, sous le banc.",
        "narrateur|Le ballon a un brin d'herbe, sous le bras.",
    ],
    (3, 1, 3): [
        "narrateur|Près du portail, le ballon tapote le barreau.",
        "narrateur|Victorino prend le doudou.",
        "papa|Le seau vert, sous le banc.",
        "maman|Le manteau, au poteau.",
        "enfant-m|Je les prends.",
        "narrateur|La flaque redevient calme, derrière eux.",
    ],
    (3, 2, 1): [
        "narrateur|Le seau vert a un peu d'eau, encore.",
        "narrateur|Victorino le verse, puis prend le manteau.",
        "papa|Au poteau.",
        "maman|Le doudou est sous le banc.",
        "enfant-m|Je le sors.",
        "narrateur|L'anse reste froide, dans sa main.",
    ],
    (3, 2, 2): [
        "narrateur|Victorino glisse le seau vert dans le sac.",
        "enfant-m|Il rentre.",
        "maman|Le manteau, au poteau.",
        "papa|Le doudou, sous le banc.",
        "narrateur|Il les prend, l'un puis l'autre.",
        "narrateur|Un cling lointain, puis plus rien.",
    ],
    (3, 2, 3): [
        "narrateur|Le seau vert pèse déjà, près du portail.",
        "narrateur|Victorino prend le doudou au barreau.",
        "papa|Le manteau, au poteau.",
        "maman|Il vient.",
        "enfant-m|Je le prends.",
        "narrateur|Le seau pose son ombre sur l'herbe.",
    ],
    (3, 3, 1): [
        "narrateur|Le doudou est déjà un peu humide, contre lui.",
        "narrateur|Victorino prend le manteau au poteau.",
        "papa|Le seau vert, sous le banc.",
        "maman|On le tire par l'anse.",
        "enfant-m|Je le prends.",
        "narrateur|La chaîne se tait, tout à fait.",
    ],
    (3, 3, 2): [
        "narrateur|Le doudou voyage déjà, l'oreille molle.",
        "narrateur|Victorino pose le seau vert dans le sac.",
        "maman|C'est le tien.",
        "papa|Le manteau est au poteau.",
        "enfant-m|Je le prends.",
        "narrateur|L'oreille grise dépasse du sac d'osier.",
    ],
    (3, 3, 3): [
        "narrateur|Le doudou retrouve le barreau, puis les bras.",
        "narrateur|Victorino prend le seau, puis le manteau.",
        "papa|Tu as cherché.",
        "maman|Le banc est vide, maintenant.",
        "enfant-m|J'ai tout.",
        "narrateur|Le portail est frais, encore, sous la main.",
    ],
}

IMG_028 = {
    (1, 1, 1): "Un grain de sable colle à la manche grise.",
    (1, 1, 2): "Le ballon tapote le bord du sac d'osier.",
    (1, 1, 3): "Un brin d'herbe reste au ballon, près du barreau.",
    (1, 2, 1): "Du sable fin brille encore dans le seau vert.",
    (1, 2, 2): "L'anse du seau touche le sac d'osier.",
    (1, 2, 3): "Un coquillage minuscule roule au fond du seau.",
    (1, 3, 1): "L'oreille grise dépasse du manteau, sur le banc.",
    (1, 3, 2): "Le doudou sent encore le sable, dans le sac.",
    (1, 3, 3): "Un fil gris pend près du portail.",
    (2, 1, 1): "La feuille jaune colle au manteau, au banc.",
    (2, 1, 2): "Le ballon est un peu froid, près du sac.",
    (2, 1, 3): "Une goutte glisse vers le barreau du portail.",
    (2, 2, 1): "Le seau sonne tout doux contre le banc.",
    (2, 2, 2): "Le métal du toboggan se tait, près du sac.",
    (2, 2, 3): "Un pas sur la rampe, puis le portail.",
    (2, 3, 1): "Le doudou a vu le toboggan, contre le banc.",
    (2, 3, 2): "L'oreille molle dépasse du sac d'osier.",
    (2, 3, 3): "La rampe brille encore, loin du portail.",
    (3, 1, 1): "La chaîne a fait cling, près du manteau.",
    (3, 1, 2): "Le ballon a touché le sable, près du sac.",
    (3, 1, 3): "Un nuage passe au-dessus du portail.",
    (3, 2, 1): "L'anse du seau est froide, contre le banc.",
    (3, 2, 2): "Un cling lointain, et le sac d'osier.",
    (3, 2, 3): "Le seau vert pose son ombre au portail.",
    (3, 3, 1): "Le doudou a senti le vent, contre le banc.",
    (3, 3, 2): "La chaîne se tait, près du sac.",
    (3, 3, 3): "L'oreille grise dépasse, près du barreau.",
}

FIN_028 = {
    (1, 1, 1): "Le grain de sable reste sur le rebord, tout seul.",
    (1, 1, 2): "Le sac d'osier sèche sous le portemanteau.",
    (1, 1, 3): "Le ballon s'endort près de la porte.",
    (1, 2, 1): "Le seau vert sèche près des chaussettes.",
    (1, 2, 2): "Un peu de sable reste au fond du seau.",
    (1, 2, 3): "L'anse du seau est tiède, maintenant.",
    (1, 3, 1): "Le doudou retrouve l'oreiller, l'oreille pliée.",
    (1, 3, 2): "Le doudou sent encore le parc, un peu.",
    (1, 3, 3): "L'oreille grise est sèche, sur l'oreiller.",
    (2, 1, 1): "Le manteau gris retrouve le crochet de la chambre.",
    (2, 1, 2): "Une feuille sèche près des clés de papa.",
    (2, 1, 3): "Le ballon a encore l'odeur du plastique froid.",
    (2, 2, 1): "Le seau penche un peu, sous le lit.",
    (2, 2, 2): "Le manteau a glissé, puis Victorino le remet.",
    (2, 2, 3): "La rampe du toboggan reste loin, maintenant.",
    (2, 3, 1): "L'oreille du doudou dépasse de l'oreiller.",
    (2, 3, 2): "Le seau vert est lisse, un peu froid encore.",
    (2, 3, 3): "Le rayon d'après-midi a bougé, sur le plancher.",
    (3, 1, 1): "Le ballon s'endort près du seau vert.",
    (3, 1, 2): "Le creux de l'oreiller attend le doudou.",
    (3, 1, 3): "Ça sent encore l'herbe, un peu.",
    (3, 2, 1): "Le seau pose son ombre sur le plancher.",
    (3, 2, 2): "Le manteau gris est chaud, sur la chaise.",
    (3, 2, 3): "Les clés de papa restent dans la coupelle.",
    (3, 3, 1): "Le doudou a l'odeur de l'herbe, au lit.",
    (3, 3, 2): "Le seau vert rentre sous le lit, tout doux.",
    (3, 3, 3): "La chaîne du parc ne s'entend plus.",
}


def body_028(i: int, j: int, k: int) -> list[str]:
    loc = L1_028[i]
    lieu = L3_028[k]
    lines = [
        f"narrateur|Victorino quitte {loc['quit']}.",
        f"narrateur|{loc['leave']}",
        "maman|C'est l'heure.",
        f"narrateur|{lieu['arrive']}",
        f"narrateur|{lieu['obj']}",
    ]
    lines.extend(FIND_028[(i, j, k)])
    if not any("J'ai tout" in ln for ln in lines):
        lines.append("enfant-m|J'ai tout.")
    lines.append("narrateur|Victorino a le seau, le manteau, le doudou.")
    lines.append(f"narrateur|{IMG_028[(i, j, k)]}")
    lines.append("enfant-m|On rentre.")
    lines.append("papa|Oui.")
    return lines


def fin_028(i: int, j: int, k: int) -> list[str]:
    loc = L1_028[i]
    jeu = L2_028[j]
    lieu = L3_028[k]
    return [
        f"narrateur|{IMG_028[(i, j, k)]}",
        f"narrateur|Victorino a joué {loc['ou']}.",
        f"narrateur|Il a pris {jeu['label']}.",
        f"narrateur|Ils sont passés par {lieu['label']}.",
        "enfant-m|J'ai le seau vert.",
        "enfant-m|J'ai le manteau.",
        "enfant-m|J'ai le doudou.",
        "maman|On rentre dans la chambre.",
        "papa|Le grain de sable est encore au rebord.",
        f"narrateur|{FIN_028[(i, j, k)]}",
        "narrateur|La fenêtre est entrouverte, tout calme.",
    ]


def build_028() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|Un grain de sable brille sur le rebord.",
        "narrateur|La fenêtre de la chambre est entrouverte.",
        "narrateur|L'air sent l'herbe chaude, tout doux.",
        "narrateur|Au loin, une chaîne de balançoire tinte.",
        "narrateur|Ting, ting.",
        "narrateur|Le doudou de Victorino est assis sur l'oreiller.",
        "narrateur|Il a une oreille un peu pliée.",
        "narrateur|Sous le lit, un seau vert dépasse.",
        "narrateur|Le seau a du sable au fond.",
        "narrateur|Papa plie un manteau gris, tout lentement.",
        "narrateur|Le manteau est encore un peu chaud.",
        "papa|Le manteau est prêt, Victorino.",
        "narrateur|Maman souffle sur le grain de sable.",
        "maman|Tu as vu le parc, par la fenêtre ?",
        "enfant-m|Oui, maman.",
        "enfant-m|Le toboggan brille.",
        "narrateur|En ce moment, Victorino enfile une chaussette.",
        "enfant-m|Je veux mon seau vert.",
        "enfant-m|On va au parc.",
        "papa|D'accord.",
        "papa|Le seau est encore sous le lit.",
        "narrateur|Victorino le tire par l'anse.",
        "narrateur|Le plancher est tiède sous son pied.",
    ]
    sons["CHK_T0000_P0000"] = "enfants_parc"
    s["CHK_T0001_P0000"] = [
        "narrateur|Le parc a trois coins tout proches.",
        "papa|Le bac à sable, le toboggan, ou les balançoires ?",
        "maman|On joue un peu.",
    ]
    extras["CHK_T0001_P0000"] = extras_t3("le bac à sable", "le toboggan", "les balançoires")
    sons["CHK_T0001_P0000"] = "enfants_parc"
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_028[i]
        sons[p] = "enfants_parc"
        s[f"{p}_Q0001"] = Q_028[i]
        extras[f"{p}_Q0001"] = extras_q(
            "le seau",
            "le seau | seau | le manteau | le doudou | ses affaires | il le prend",
            "Le seau vert est encore là. Victorino prend quoi ?",
        )
        s[f"{p}_C0001"] = C_028[i]
        s[f"{p}_T0002_P0000"] = [
            f"narrateur|Victorino peut encore jouer un peu, {L1_028[i]['ou']}.",
            "maman|Le ballon, le seau, ou le doudou ?",
            "papa|On joue encore un peu.",
        ]
        extras[f"{p}_T0002_P0000"] = extras_t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_028[(i, j)]
            s[f"{p2}_T0003_P0000"] = [
                f"narrateur|Il manque encore une affaire, {L1_028[i]['ou']}.",
                "maman|Le banc, le sac, ou le portail ?",
                "papa|On cherche, puis on prend.",
            ]
            extras[f"{p2}_T0003_P0000"] = extras_t3("le banc", "le sac", "le portail")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_028(i, j, k)
                sons[p3] = "enfants_parc"
                s[f"{p3}_F0001"] = fin_028(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-029  N1  AUT.RAN.001  Nino  oiseau de papier
# T1 cuisine / jardin / chambre  T2 cubes / livre / dînette  T3 moment
# Leçon implicite : l'oiseau perdu sous les jouets, retrouvé dans la caisse.
# ---------------------------------------------------------------------------

L1_029 = {
    1: {
        "label": "la cuisine",
        "ou": "dans la cuisine",
        "caisse": "La caisse est près du buffet.",
    },
    2: {
        "label": "le jardin",
        "ou": "dans le jardin",
        "caisse": "La caisse est près de la marche.",
    },
    3: {
        "label": "la chambre",
        "ou": "dans la chambre",
        "caisse": "La caisse est sous le rebord.",
    },
}
L2_029 = {
    1: {"label": "les cubes", "un": "un cube", "put": "Nino glisse un cube."},
    2: {"label": "le livre", "un": "le livre", "put": "Nino glisse le livre."},
    3: {"label": "la dînette", "un": "une tasse", "put": "Nino glisse une tasse."},
}
L3_029 = {
    1: {
        "label": "le matin",
        "lum": "La lumière est blanche, tout neuve.",
        "dehors": "Le toit rouge est tout net.",
    },
    2: {
        "label": "après la sieste",
        "lum": "Une bande d'ombre traverse le tapis.",
        "dehors": "Le toit est un peu tiède.",
    },
    3: {
        "label": "le soir",
        "lum": "La lampe fait un rond jaune.",
        "dehors": "Le toit devient sombre, dehors.",
    },
}

ARRIVE_029 = {
    1: [
        "narrateur|Nino va vers la cuisine.",
        "narrateur|Le carrelage est un peu froid.",
        "narrateur|Une casserole chante tout bas.",
        "narrateur|Ça sent encore l'orange.",
        "narrateur|Une miette brille sur la table.",
        "papa|La caisse est près du buffet.",
        "narrateur|Des cubes sont par terre.",
        "enfant-m|L'oiseau n'est plus à la vitre.",
        "maman|Il est venu avec les jouets ?",
        "narrateur|Nino se penche.",
        "narrateur|Le papier n'est pas sur la table.",
        "enfant-m|Je ne le vois pas.",
        "papa|Sous un cube, peut-être.",
    ],
    2: [
        "narrateur|Nino va vers le jardin.",
        "narrateur|L'herbe est un peu mouillée.",
        "narrateur|L'air touche son nez.",
        "narrateur|Un vrai oiseau chante, tout loin.",
        "papa|La caisse est près de la marche.",
        "narrateur|Des cubes sont dans l'herbe.",
        "enfant-m|Mon papier n'est pas là.",
        "maman|Le vent l'a bougé ?",
        "narrateur|Nino cherche près d'une feuille.",
        "narrateur|Rien, seulement l'herbe.",
        "enfant-m|Il est perdu.",
        "papa|Sous les jouets, tout doux.",
    ],
    3: [
        "narrateur|Nino va vers la chambre.",
        "narrateur|La couverture est douce, pliée.",
        "narrateur|Le tapis bleu est encore là.",
        "narrateur|La vitre a toujours son rond.",
        "enfant-m|Le toit est rouge, dehors.",
        "maman|Et l'oiseau de papier ?",
        "narrateur|Le rebord est vide.",
        "papa|La caisse est sous le rebord.",
        "narrateur|Des cubes couvrent le tapis.",
        "enfant-m|Il est dessous.",
        "papa|On peut voir, tout doux.",
        "narrateur|Nino écarte un cube.",
        "narrateur|Pas encore de papier.",
    ],
}

Q_029 = {
    1: [
        "narrateur|Nino cherche l'oiseau, en cuisine.",
        "maman|Il est où ?",
    ],
    2: [
        "narrateur|Nino cherche l'oiseau, au jardin.",
        "papa|Il est où ?",
    ],
    3: [
        "narrateur|Nino cherche l'oiseau, dans la chambre.",
        "maman|Il est où ?",
    ],
}

C_029 = {
    1: [
        "narrateur|Nino prend un cube jaune.",
        "narrateur|Il le pose dans la caisse.",
        "narrateur|Toc.",
        "maman|Tu regardes dessous ?",
        "enfant-m|Un peu, maman.",
        "papa|Encore un, tout doux.",
        "narrateur|Un bout de carrelage reparaît.",
        "narrateur|La miette attend encore.",
    ],
    2: [
        "narrateur|Nino prend un cube dans l'herbe.",
        "narrateur|Il le pose dans la caisse.",
        "narrateur|Toc.",
        "papa|Le tas devient plus petit.",
        "enfant-m|Toujours pas.",
        "maman|Tu continues, tout calme ?",
        "narrateur|Un bout d'herbe reparaît.",
        "narrateur|Le vrai oiseau chante encore.",
    ],
    3: [
        "narrateur|Nino pousse un cube vers la caisse.",
        "narrateur|Ça fait un petit bruit.",
        "maman|Le tapis reparaît, tu vois ?",
        "enfant-m|Un peu, maman.",
        "papa|Encore un, près de la vitre.",
        "narrateur|Un coin de tapis bleu revient.",
        "narrateur|Le rebord reste vide.",
    ],
}

PLAY_029 = {
    1: [
        "narrateur|Nino a choisi les cubes.",
        "narrateur|Ils sont en bois, un peu lourds.",
        "narrateur|Ils cliquent dans la caisse.",
        "papa|Un, puis un autre.",
        "enfant-m|Je cherche dessous.",
        "maman|Tout doux, oui.",
        "narrateur|Un cube sent le pin.",
        "narrateur|Nino le serre, puis le pose.",
        "narrateur|Toc.",
        "enfant-m|Pas encore lui.",
        "papa|Le tas baisse, tu vois.",
    ],
    2: [
        "narrateur|Nino a choisi le livre.",
        "narrateur|La couverture est un peu froissée.",
        "narrateur|Une page montre un oiseau.",
        "maman|Comme le tien, hein ?",
        "enfant-m|Le mien est en papier.",
        "papa|On le met dans la caisse ?",
        "narrateur|Le livre glisse, tout plat.",
        "narrateur|Toc.",
        "enfant-m|Sous le livre ?",
        "maman|On peut voir, maintenant.",
        "narrateur|Un coin blanc apparaît, tout petit.",
    ],
    3: [
        "narrateur|Nino a choisi la dînette.",
        "narrateur|Une petite tasse sonne, tout creux.",
        "papa|On sert l'oiseau ?",
        "enfant-m|S'il est là.",
        "maman|La tasse va dans la caisse.",
        "narrateur|Nino la glisse, tout doux.",
        "narrateur|Toc.",
        "enfant-m|L'assiette aussi.",
        "papa|Oui, à côté.",
        "narrateur|Un trou s'ouvre au milieu.",
        "narrateur|Pas encore d'aile.",
    ],
}

L2_EXTRA_029 = {
    (1, 1): "Un cube attrape un reflet d'orange.",
    (1, 2): "Une miette reste au bord de la page.",
    (1, 3): "La petite casserole est près du vrai bol.",
    (2, 1): "L'herbe tache un cube, tout vert.",
    (2, 2): "Une vraie feuille sert de marque-page.",
    (2, 3): "Une goutte perle au bord de l'assiette.",
    (3, 1): "Un cube tapote le parquet, tout doux.",
    (3, 2): "Le rond de la vitre colore la page.",
    (3, 3): "La petite tasse est près du radiateur.",
}

FIND_029 = {
    1: [
        "narrateur|Nino prend le dernier cube.",
        "narrateur|Il le met dans la caisse.",
        "narrateur|Toc.",
        "narrateur|Sous sa place, un coin de papier.",
    ],
    2: [
        "narrateur|Nino soulève le livre.",
        "narrateur|Il le met dans la caisse.",
        "narrateur|Toc.",
        "narrateur|Sous la page, un coin de papier.",
    ],
    3: [
        "narrateur|Nino soulève la petite tasse.",
        "narrateur|Il la met dans la caisse.",
        "narrateur|Toc.",
        "narrateur|Sous la tasse, un coin de papier.",
    ],
}

IMG_029 = {
    (1, 1, 1): "Une miette colle à l'aile, puis part.",
    (1, 1, 2): "L'aile a un reflet de casserole, tout doux.",
    (1, 1, 3): "L'oiseau a une odeur d'orange, tout près.",
    (1, 2, 1): "Une page a un pli, comme l'aile.",
    (1, 2, 2): "Le livre reste sage, dans la caisse.",
    (1, 2, 3): "L'oiseau a vu le bol bleu, un instant.",
    (1, 3, 1): "La petite tasse sonne encore, tout bas.",
    (1, 3, 2): "Une goutte sèche sur l'aile de papier.",
    (1, 3, 3): "L'assiette rentre, et l'oiseau aussi.",
    (2, 1, 1): "Un brin d'herbe colle à l'aile blanche.",
    (2, 1, 2): "Le cube a un peu de terre, au coin.",
    (2, 1, 3): "Le vrai oiseau se tait, tout loin.",
    (2, 2, 1): "Une feuille verte reste dans le livre.",
    (2, 2, 2): "L'aile a un peu de vent, encore.",
    (2, 2, 3): "Le papier sent l'herbe, tout doux.",
    (2, 3, 1): "La tasse a une goutte d'herbe au bord.",
    (2, 3, 2): "L'assiette est froide, près de la marche.",
    (2, 3, 3): "L'aile tremble un peu, puis s'arrête.",
    (3, 1, 1): "Un cube a un rond de lumière, tout blanc.",
    (3, 1, 2): "Le tapis bleu reparaît, tout calme.",
    (3, 1, 3): "Le radiateur fait tic, près de l'aile.",
    (3, 2, 1): "La page a le toit rouge, tout petit.",
    (3, 2, 2): "Le livre est tiède, comme la joue.",
    (3, 2, 3): "Le rond de la vitre touche l'aile.",
    (3, 3, 1): "La tasse a un rond de lampe, tout jaune.",
    (3, 3, 2): "L'assiette rentre sous le rebord, tout sage.",
    (3, 3, 3): "L'aile a un reflet de lampe, tout doux.",
}

FIN_029 = {
    (1, 1, 1): "Le bol bleu a encore l'odeur d'orange.",
    (1, 1, 2): "La casserole se tait, tout à fait.",
    (1, 1, 3): "La miette n'est plus sur la table.",
    (1, 2, 1): "Le livre garde un pli, dans la caisse.",
    (1, 2, 2): "Le carrelage est libre, au milieu.",
    (1, 2, 3): "Le buffet a la caisse, tout calme.",
    (1, 3, 1): "La petite tasse ne sonne plus.",
    (1, 3, 2): "Le vrai bol attend, tout rond.",
    (1, 3, 3): "L'orange sent encore, tout bas.",
    (2, 1, 1): "L'herbe redevient calme, près de la marche.",
    (2, 1, 2): "Un vrai oiseau reprend une note.",
    (2, 1, 3): "La terre sèche sur le cube, déjà.",
    (2, 2, 1): "La feuille verte reste dans le livre.",
    (2, 2, 2): "Le vent ne bouge plus le papier.",
    (2, 2, 3): "La marche a la caisse, tout sage.",
    (2, 3, 1): "L'assiette a encore une goutte, toute petite.",
    (2, 3, 2): "L'herbe ne cache plus rien.",
    (2, 3, 3): "Le jardin est calme, maintenant.",
    (3, 1, 1): "Le tapis bleu est libre, sous la vitre.",
    (3, 1, 2): "Le radiateur fait tic, tout doux.",
    (3, 1, 3): "Le rebord a de nouveau son oiseau.",
    (3, 2, 1): "Le livre s'endort dans la caisse.",
    (3, 2, 2): "La couverture reste pliée, à côté.",
    (3, 2, 3): "Le rond sur la vitre est encore là.",
    (3, 3, 1): "La tasse rentre, près des cubes.",
    (3, 3, 2): "La lampe fait un rond, sur l'aile.",
    (3, 3, 3): "Le toit rouge n'est plus visible, dehors.",
}


def body_029(i: int, j: int, k: int) -> list[str]:
    loc = L1_029[i]
    t = L3_029[k]
    img = IMG_029[(i, j, k)]
    lines = [
        f"narrateur|{t['lum']}",
        f"narrateur|Nino est encore {loc['ou']}.",
        f"narrateur|{loc['caisse']}",
    ]
    lines.extend(FIND_029[j])
    lines.extend(
        [
            "enfant-m|Mon oiseau !",
            "maman|Te voilà, petit.",
            "papa|Merci, tu l'as trouvé.",
            "narrateur|Nino le serre, tout doux.",
            "narrateur|L'aile est un peu pliée.",
            "enfant-m|Je la déplie.",
            "maman|Tout doux, oui.",
            f"narrateur|{img}",
            f"narrateur|{t['dehors']}",
        ]
    )
    return lines


def fin_029(i: int, j: int, k: int) -> list[str]:
    loc = L1_029[i]
    jeu = L2_029[j]
    t = L3_029[k]
    img = IMG_029[(i, j, k)]
    return [
        "narrateur|Nino revient vers la vitre.",
        "narrateur|Il recolle l'oiseau de papier.",
        "enfant-m|Il voit le toit, papa.",
        "papa|Oui, il est bien là.",
        "maman|La caisse est calme, maintenant.",
        "papa|Bravo, Nino.",
        f"narrateur|Il a cherché {loc['ou']}.",
        f"narrateur|Il a pris {jeu['label']}.",
        f"narrateur|{t['lum']}",
        f"narrateur|{img}",
        f"narrateur|{FIN_029[(i, j, k)]}",
        "narrateur|L'aile est lisse, contre le verre.",
    ]


def build_029() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|La vitre est un peu embuée.",
        "narrateur|Un doigt a dessiné un rond.",
        "narrateur|Dans le rond, on voit un toit.",
        "narrateur|Le toit est rouge, tout petit.",
        "narrateur|Un oiseau en papier est collé.",
        "narrateur|Il a une aile un peu pliée.",
        "narrateur|Le papier est rêche sous le doigt.",
        "narrateur|Le radiateur fait tic, tic.",
        "narrateur|Ça sent l'orange, tout près.",
        "narrateur|Les peaux sont dans un bol bleu.",
        "papa|Tu as senti l'orange, Nino ?",
        "enfant-m|Oui, papa.",
        "narrateur|Le tapis sous la fenêtre est bleu.",
        "narrateur|Des cubes sont dessus.",
        "narrateur|Un livre est ouvert, tout plat.",
        "narrateur|Une petite tasse attend.",
        "enfant-m|Je veux que l'oiseau voie le toit.",
        "maman|L'aile est encore un peu pliée.",
        "narrateur|En ce moment, Nino touche le papier.",
        "narrateur|Un cube glisse contre l'aile.",
        "narrateur|L'oiseau tombe entre les jouets.",
        "enfant-m|Où est-il ?",
        "papa|Sous les cubes, peut-être.",
    ]
    sons["CHK_T0000_P0000"] = ""
    s["CHK_T0001_P0000"] = [
        "papa|On cherche où, Nino ?",
        "maman|La cuisine, le jardin, ou la chambre ?",
        "narrateur|Tu choisis.",
    ]
    extras["CHK_T0001_P0000"] = extras_t3("la cuisine", "le jardin", "la chambre")
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_029[i]
        s[f"{p}_Q0001"] = Q_029[i]
        extras[f"{p}_Q0001"] = extras_q(
            "l'oiseau",
            "l'oiseau | oiseau | sous les jouets | sous les cubes | dans la caisse | dessous | le papier",
            "Il cherche sous les jouets. Où est l'oiseau ?",
        )
        s[f"{p}_C0001"] = C_029[i]
        s[f"{p}_T0002_P0000"] = [
            "maman|Quel jouet tu prends ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|Ou la dînette.",
        ]
        extras[f"{p}_T0002_P0000"] = extras_t3("les cubes", "le livre", "la dînette")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            extra = L2_EXTRA_029[(i, j)]
            s[p2] = PLAY_029[j] + [
                f"narrateur|{extra}",
                f"narrateur|On est encore {L1_029[i]['ou']}.",
            ]
            s[f"{p2}_T0003_P0000"] = [
                "papa|On cherche quand ?",
                "narrateur|Le matin.",
                "narrateur|Après la sieste.",
                "narrateur|Ou le soir.",
            ]
            extras[f"{p2}_T0003_P0000"] = extras_t3(
                "le matin", "après la sieste", "le soir"
            )
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_029(i, j, k)
                s[f"{p3}_F0001"] = fin_029(i, j, k)
    return s, sons, extras


def main() -> None:
    s, sons, extras = build_028()
    write_tree(
        "TREE-AUT-028",
        (
            "Victorino veut le parc avec son seau vert. La chambre sent l'herbe. "
            "Une chaîne tinte au loin. Il joue au bac, au toboggan ou aux "
            "balançoires. Au moment de rentrer, le seau, le manteau ou le doudou "
            "sont encore là. Il les reprend au banc, au sac ou au portail. "
            "Le grain de sable reste sur le rebord."
        ),
        "Le seau vert de Victorino",
        "Victorino, papa, maman",
        "chambre entrouverte, puis le parc",
        s,
        sons,
        extras,
        extra_ban=("sami",),
    )
    relecture(
        "TREE-AUT-028",
        "Le seau vert de Victorino",
        "Victorino veut le parc et le seau vert. Grain de sable, chaîne, "
        "manteau gris. Bac / toboggan / balançoires, puis ballon / seau / "
        "doudou, puis banc / sac / portail. Il reprend ce qui reste. "
        "Retour chambre, rebord.",
        "D16 Victorino (plus Sami). T3 = banc/sac/portail, plus Tom/Léa/Sami. "
        "Leçon implicite AUT.AFF.003. Fin sensorielle.",
    )

    s, sons, extras = build_029()
    write_tree(
        "TREE-AUT-029",
        (
            "Nino veut que l'oiseau de papier voie le toit rouge. Un cube "
            "glisse. L'oiseau tombe entre les jouets. Il cherche dans la "
            "cuisine, le jardin ou la chambre. Les cubes, le livre ou la "
            "dînette vont dans la caisse. L'aile reparaît. L'oiseau revient "
            "contre la vitre."
        ),
        "L'oiseau de papier près de la fenêtre",
        "Nino, papa, maman",
        "près de la fenêtre, tapis bleu, caisse sous le rebord",
        s,
        sons,
        extras,
        extra_ban=("ranger", "hugo", "sarah"),
    )
    relecture(
        "TREE-AUT-029",
        "L'oiseau de papier près de la fenêtre",
        "Nino veut l'oiseau contre le toit rouge. Cube contre l'aile, oiseau "
        "sous les jouets. Cuisine / jardin / chambre, puis cubes / livre / "
        "dînette, puis matin / sieste / soir. Caisse. Aile lisse sur la vitre.",
        "D16 Nino (plus Hugo, plus Sarah). N1 ≤10. Pas « on va ranger ». "
        "Question = où est l'oiseau. Fin = aile contre le verre.",
    )


if __name__ == "__main__":
    main()
