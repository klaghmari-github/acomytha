#!/usr/bin/env python3
"""TREE-AUT-018 (N3 RAN implicite, étoile) et TREE-AUT-019 (N1 ROU vécue, bidon)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, check, make_chunk, relecture, words, ROOT


def preview(sid: str, age: str, scripts: dict) -> None:
    lim = LIMITS.get(age) or 12
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
    q: dict | None = None,
    extras: dict | None = None,
) -> None:
    preview(sid, json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))["age_band"], scripts)
    src = json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={list(extra)[:8]}")
    by = {}
    extras = extras or {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind in {"passage_question", "transition_question"}:
            scale, rate = 1.28, "slow"
        elif kind == "passage_fin":
            scale, rate = 1.26, "slow"
        elif src.get("age_band") == "N1":
            scale, rate = 1.22, "slow"
        else:
            scale, rate = 1.22, "medium"
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if kind == "passage_question" and q:
            by[cid].update(q)
        if cid in extras:
            by[cid].update(extras[cid])
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    path = ROOT / sid / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")


# ---------------------------------------------------------------------------
# TREE-AUT-018 — Nina, immeuble, caisse près des chaussures, étoile perdue
# T1 lieu  T2 jouet qui cache  T3 moment
# ---------------------------------------------------------------------------

TIME_018 = {
    1: {
        "label": "le matin",
        "lum": "La lumière est pâle, un peu bleue.",
        "dehors": "La gouttière chante encore, tout bas.",
        "extra": "Un pigeon secoue une aile mouillée.",
        "fin": "Le sac d'école attend, déjà un peu lourd.",
        "sortie": "On descend pour l'école, tout doux.",
    },
    2: {
        "label": "après la sieste",
        "lum": "La lumière est ronde, un peu chaude.",
        "dehors": "La cour de l'immeuble est calme.",
        "extra": "La couverture de la sieste reste pliée.",
        "fin": "Les joues de Nina sont encore un peu chaudes.",
        "sortie": "On descend pour la cour, tout calme.",
    },
    3: {
        "label": "le soir",
        "lum": "Les lampes de l'entrée sont petites et jaunes.",
        "dehors": "Les lumières de la rue s'allument.",
        "extra": "Une odeur de pain chaud monte de la rue.",
        "fin": "Le pigeon s'est endormi, sur le rebord.",
        "sortie": "On descend pour le pain, tout près.",
    },
}

PLACE_018 = {
    1: {
        "label": "la cuisine",
        "arrive": "Nina pousse la porte de la cuisine.",
        "detail": "Les carreaux sont un peu tièdes.",
        "tas": "Les jouets sont près de la table.",
        "geste": "Nina pose un doigt sur une miette sèche.",
        "fin": "Une miette reste sur la table, toute petite.",
    },
    2: {
        "label": "le jardin",
        "arrive": "Nina va vers le petit jardin de l'immeuble.",
        "detail": "L'herbe est mouillée, toute brillante.",
        "tas": "Près des bottes, les jouets font un tas.",
        "geste": "Nina touche une feuille collée au seau.",
        "fin": "Une feuille reste collée au paillasson.",
    },
    3: {
        "label": "la chambre",
        "arrive": "Nina revient vers la chambre.",
        "detail": "Le rideau jaune bouge un peu.",
        "tas": "Sur le tapis, les jouets cachent les chaussons.",
        "geste": "Nina lisse un pli de la couverture.",
        "fin": "Le rideau jaune ne bouge plus.",
    },
}

TOY_018 = {
    1: {
        "label": "les cubes",
        "take": "Nina prend un cube à deux mains.",
        "feel": "Il est lourd, un peu lisse.",
        "child": "Il va dans la caisse.",
        "put": "Le cube tombe dans la caisse.",
        "find": "Sous sa place, un coin de bois clair.",
        "fin": "Les cubes ne glissent plus, dans la caisse.",
    },
    2: {
        "label": "le livre",
        "take": "Nina soulève le livre aux pages froides.",
        "feel": "Une page sent encore le pain grillé.",
        "child": "Le livre, dans la caisse.",
        "put": "Le livre glisse, tout droit.",
        "find": "Sous le livre, le bois clair attend.",
        "fin": "Les pages restent sages, dans la caisse.",
    },
    3: {
        "label": "la dînette",
        "take": "Nina écarte encore une petite tasse.",
        "feel": "La tasse est blanche, un peu froide.",
        "child": "La tasse, dans la caisse.",
        "put": "La tasse sonne, tout creux.",
        "find": "Au fond, l'étoile de bois brille.",
        "fin": "La petite tasse reste à sa place, dans la caisse.",
    },
}

IMG_018 = {
    (1, 1, 1): "Une miette de pain colle au cube, puis part.",
    (1, 1, 2): "Le cube est tiède, comme les joues de Nina.",
    (1, 1, 3): "L'ombre d'un cube danse sous la lampe.",
    (1, 2, 1): "Une miette reste au bord d'une page.",
    (1, 2, 2): "Le livre est tiède, près de l'assiette ronde.",
    (1, 2, 3): "La lampe dore le bord d'une page.",
    (1, 3, 1): "Une petite tasse a une miette au fond.",
    (1, 3, 2): "La dînette est chaude, près de la casserole.",
    (1, 3, 3): "La petite cuillère brille sous la lampe.",
    (2, 1, 1): "Un cube a une goutte d'herbe, toute ronde.",
    (2, 1, 2): "Le cube sèche au soleil, tout vert.",
    (2, 1, 3): "Un cube garde une goutte, près des bottes.",
    (2, 2, 1): "Une vraie feuille sert de marque-page.",
    (2, 2, 2): "Le livre sent l'herbe mouillée.",
    (2, 2, 3): "Un pigeon se tait près du livre.",
    (2, 3, 1): "Une petite assiette a de la rosée.",
    (2, 3, 2): "La dînette est tiède, au soleil du jardin.",
    (2, 3, 3): "Loin de la dînette, une goutte tombe.",
    (3, 1, 1): "Un rayon pose sur la tour de cubes.",
    (3, 1, 2): "Un cube est contre l'oreiller, tout calme.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Le rideau jaune colore la page.",
    (3, 2, 2): "Le livre est ouvert sur la couverture.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

L1_018 = {
    1: [
        "narrateur|Nina pousse la porte de la cuisine.",
        "narrateur|Les carreaux sont un peu tièdes.",
        "narrateur|Ça sent encore le pain grillé.",
        "narrateur|Une miette brille sur la table.",
        "papa|Tu cherches ici un moment ?",
        "enfant-f|Mon étoile était près du bol.",
        "maman|Elle est sous quelque chose ?",
        "narrateur|Nina soulève le torchon rayé.",
        "narrateur|Pas de bois clair.",
        "papa|Et sous l'assiette ?",
        "narrateur|Une miette seulement.",
        "enfant-f|Elle est perdue.",
        "maman|Le tas est encore haut, tu vois.",
        "narrateur|La casserole fait un tout petit tic.",
    ],
    2: [
        "narrateur|Nina va vers le petit jardin.",
        "narrateur|L'herbe est mouillée, toute brillante.",
        "narrateur|L'air est frais sur le nez.",
        "papa|Tes bottes sont sur le paillasson ?",
        "enfant-f|Oui, elles font ploc.",
        "maman|L'étoile aimait le rebord, parfois.",
        "narrateur|Nina cherche près des bottes.",
        "narrateur|Un cube est collé à l'herbe.",
        "enfant-f|Je ne vois plus le bois clair.",
        "papa|Sous la feuille, peut-être.",
        "narrateur|Une feuille seulement, toute mouillée.",
        "enfant-f|Pas elle.",
        "maman|On peut voir dessous, tout doux.",
        "narrateur|La gouttière chante encore, tout bas.",
    ],
    3: [
        "narrateur|Nina revient vers la chambre.",
        "narrateur|Le drap est encore un peu chaud.",
        "narrateur|Le rideau jaune bouge un peu.",
        "enfant-f|Elle dormait près de l'oreiller.",
        "maman|L'étoile de bois ?",
        "narrateur|Nina soulève un coin du drap.",
        "narrateur|Les chaussons sont en tas.",
        "papa|Tu as regardé sous le livre ?",
        "enfant-f|Le tas cache le tapis.",
        "maman|Les jouets sont encore hauts.",
        "narrateur|Nina lisse un pli de la couverture.",
        "enfant-f|Je la veux pour le sac.",
        "papa|On peut voir dessous, tout calme.",
        "narrateur|Le rideau touche ses épaules, tout doux.",
    ],
}

C_018 = {
    1: [
        "narrateur|Nina glisse un cube vers la caisse.",
        "narrateur|Toc.",
        "maman|Tu regardes dessous ?",
        "enfant-f|Pas encore, maman.",
        "papa|Encore un, tout doux.",
        "narrateur|Un bout de carreau reparaît, tout clair.",
        "narrateur|La miette brille encore sur la table.",
    ],
    2: [
        "narrateur|Nina pose une tasse jouet dans la caisse.",
        "narrateur|Toc.",
        "papa|Le tas devient plus petit.",
        "enfant-f|Toujours pas.",
        "maman|Tu continues, tout calme ?",
        "narrateur|L'herbe mouillée brille encore dehors.",
        "narrateur|Les bottes restent sur le paillasson.",
    ],
    3: [
        "narrateur|Nina pousse un cube vers la caisse.",
        "narrateur|Ça fait un petit bruit.",
        "maman|Les ombres bougent, tu vois ?",
        "enfant-f|Un peu, maman.",
        "papa|Encore un, près du tapis.",
        "narrateur|Le fond du tapis reparaît, tout lent.",
        "narrateur|Le rideau jaune reste calme.",
    ],
}

L2_018 = {
    1: [
        "narrateur|Les cubes attendent, en bois clair.",
        "narrateur|Ils sentent le pin, tout doux.",
        "enfant-f|Une petite tour, papa.",
        "papa|Un cube, ensuite un autre.",
        "narrateur|Nina pose le cube rouge.",
        "narrateur|Puis le cube bleu.",
        "maman|L'étoile n'est pas dans la tour.",
        "enfant-f|Elle est dessous, peut-être.",
        "papa|On pourra voir, tout à l'heure.",
        "narrateur|La petite tour penche vers la caisse.",
    ],
    2: [
        "narrateur|Le livre a une couverture jaune, comme le rideau.",
        "maman|On ouvre, une page, puis l'autre.",
        "enfant-f|Une étoile dessinée !",
        "papa|Oui, tu as bien regardé.",
        "narrateur|Nina touche le papier lisse.",
        "maman|Ce n'est pas la vraie, hein ?",
        "enfant-f|La vraie est en bois.",
        "papa|Elle est sous le tas, peut-être.",
        "narrateur|Nina referme le livre, tout doux.",
        "narrateur|Les pages sentent encore le pain.",
    ],
    3: [
        "narrateur|La dînette est sur une serviette.",
        "narrateur|La petite tasse est blanche.",
        "enfant-f|Du thé, maman ?",
        "maman|D'abord la tasse, ensuite on verse.",
        "narrateur|Nina pose la tasse près du vrai bol.",
        "papa|Une gorgée du vrai bol, tout doux.",
        "narrateur|Elle boit une gorgée.",
        "maman|L'étoile n'est pas dans la tasse.",
        "enfant-f|Je cherche encore.",
        "narrateur|Ça sent le pain grillé, encore un peu.",
    ],
}


def l3_body_018(i: int, j: int, k: int) -> list[str]:
    t = TIME_018[i]
    p = PLACE_018[j]
    y = TOY_018[k]
    img = IMG_018[(i, j, k)]
    return [
        f"narrateur|{t['lum']}",
        f"narrateur|{p['tas']}",
        f"narrateur|{y['take']}",
        f"narrateur|{y['feel']}",
        f"enfant-f|{y['child']}",
        f"narrateur|{y['put']}",
        "narrateur|Toc.",
        f"narrateur|{y['find']}",
        "enfant-f|Mon étoile !",
        "maman|Te voilà, petite.",
        "papa|Merci, tu l'as trouvée.",
        f"narrateur|{img}",
        "narrateur|Nina la serre contre sa joue.",
        f"narrateur|{t['dehors']}",
    ]


def l3_fin_018(i: int, j: int, k: int) -> list[str]:
    t = TIME_018[i]
    p = PLACE_018[j]
    y = TOY_018[k]
    img = IMG_018[(i, j, k)]
    starts = [
        "L'étoile a le nez sur le sac.",
        "Nina tient le bois clair, tout chaud.",
        "Contre la joue, l'étoile est calme.",
        "Au chaud, l'étoile écoute la gouttière.",
        "Près de la caisse, Nina respire.",
        "Sous la lampe, le bois clair brille.",
        "Dans ses mains, l'étoile est trouvée.",
        "Enfin le bois est là, tout doux.",
        "Voilà l'étoile, contre le sac.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return [
        f"narrateur|{first}",
        f"narrateur|{y['fin']}",
        "enfant-f|Elle va sur le sac, papa.",
        "papa|Oui, elle est bien là.",
        "maman|La caisse est calme, maintenant.",
        "papa|Bravo, Nina.",
        f"narrateur|{p['fin']}",
        f"narrateur|{img}",
        f"narrateur|{t['fin']}",
        f"narrateur|{t['sortie']}",
        "narrateur|La gouttière chante encore, tout bas.",
    ]


def build_018() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|La gouttière de l'immeuble chante, tout bas.",
        "narrateur|Un pigeon secoue une aile, sur le rebord.",
        "narrateur|Les carreaux de l'entrée sont froids.",
        "narrateur|Un sac d'école s'appuie contre le mur.",
        "narrateur|Près des chaussures, une caisse en bois attend.",
        "narrateur|Sa corde est usée, toute douce.",
        "narrateur|Ça sent le pain grillé, encore un peu.",
        "narrateur|Une miette reste sur l'assiette ronde.",
        "papa|Le pigeon est revenu, Nina.",
        "maman|Il se sèche, tout calme.",
        "enfant-f|Je veux mon étoile, maman.",
        "enfant-f|Elle va sur le sac.",
        "narrateur|En ce moment, Nina ouvre la caisse.",
        "narrateur|Des cubes tombent près des chaussures.",
        "narrateur|Le livre glisse sous une botte.",
        "narrateur|Une tasse de dînette roule, toc.",
        "enfant-f|Mon étoile ?",
        "papa|Elle était dans la caisse.",
        "narrateur|Nina cherche sous le sac.",
        "narrateur|Rien.",
        "maman|Tu as regardé près des chaussures ?",
        "enfant-f|Le tas est trop haut.",
        "papa|On peut voir dessous, tout doux.",
        "narrateur|La gouttière chante encore, tout bas.",
    ]
    s["CHK_T0001_P0000"] = [
        "papa|Nina cherche où, d'abord ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|La chambre.",
    ]
    q = [
        "narrateur|Nina cherche son étoile.",
        "maman|Elle est où ?",
    ]
    t2 = [
        "papa|Quel jouet tu prends ?",
        "narrateur|Les cubes.",
        "narrateur|Le livre.",
        "narrateur|La dînette.",
    ]
    t3 = [
        "maman|On y va à quelle heure ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ]
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_018[i]
        s[f"{p}_Q0001"] = q
        s[f"{p}_C0001"] = C_018[i]
        s[f"{p}_T0002_P0000"] = t2
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2_018[j] + [
                f"narrateur|{PLACE_018[i]['geste']}",
                f"narrateur|{TIME_018[1]['extra'] if i == 1 else PLACE_018[i]['detail']}",
            ]
            s[f"{p2}_T0003_P0000"] = t3
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_018(k, i, j)
                s[f"{p3}_F0001"] = l3_fin_018(k, i, j)
    return s


Q_018 = {
    "expected_answer": "étoile",
    "accepted_examples": "étoile | l'étoile | sous les chaussures | sous les jouets | dans la caisse | dessous | sous une chaussure",
    "retry_prompt": "Elle cherche sous le tas. Où est l'étoile ?",
}


# ---------------------------------------------------------------------------
# TREE-AUT-019 — Sarah, ferme, bidon de lait, séquence vécue
# T1 lieu de jeu  T2 jouet  T3 animal (labels T3 changés : plus Tom/Léa/Sami)
# ---------------------------------------------------------------------------

PLACE_019 = {
    1: {
        "label": "le bac à sable",
        "sol": "Du sable pâle, un peu frais.",
        "son": "Ça fait chh, tout doux.",
        "fin": "Un grain reste sous l'ongle de Sarah.",
    },
    2: {
        "label": "le toboggan",
        "sol": "Sous la paume, le métal est froid.",
        "son": "Les marches font toc, toc.",
        "fin": "Une feuille colle encore sur la rampe.",
    },
    3: {
        "label": "les balançoires",
        "sol": "La corde est un peu rêche.",
        "son": "Le siège bouge, tout lent.",
        "fin": "La corde ne fait plus cling.",
    },
}

TOY_019 = {
    1: {
        "label": "le ballon",
        "take": "Sarah prend le ballon à deux mains.",
        "feel": "Il est souple, un peu rouge.",
        "child": "Il vient avec moi.",
        "fin": "Voilà le ballon, près d'elle.",
    },
    2: {
        "label": "le seau",
        "take": "Sarah soulève le seau bleu.",
        "feel": "L'anse est un peu froide.",
        "child": "Le seau vient.",
        "fin": "Voilà le seau, près des bottes.",
    },
    3: {
        "label": "le doudou",
        "take": "Sarah serre le doudou gris.",
        "feel": "Il sent encore la couverture.",
        "child": "Il vient, lui aussi.",
        "fin": "Contre Sarah, le doudou est au chaud.",
    },
}

ANIMAL_019 = {
    1: {
        "label": "le veau",
        "voir": "Le veau attend près de la porte.",
        "feel": "Son souffle est chaud, tout doux.",
        "child": "Il a faim, papa ?",
        "fin": "Le veau referme les yeux, tout calme.",
    },
    2: {
        "label": "la poule",
        "voir": "La poule picore près de la pierre.",
        "feel": "Ses pas font tic, tout secs.",
        "child": "Elle veut un grain.",
        "fin": "La poule picore encore, tout loin.",
    },
    3: {
        "label": "le chat",
        "voir": "Le chat est sur la pierre froide.",
        "feel": "Sa gorge fait ronron, tout bas.",
        "child": "Il a chaud, maman.",
        "fin": "Le chat s'endort, près du bidon vide.",
    },
}

IMG_019 = {
    (1, 1, 1): "Un grain de sable colle au ballon rouge.",
    (1, 1, 2): "Une miette de pain reste au bord du ballon.",
    (1, 1, 3): "Un poil de chat reste sur le ballon.",
    (1, 2, 1): "Du sable fin brille dans le seau.",
    (1, 2, 2): "L'anse jaune touche le bidon, un instant.",
    (1, 2, 3): "Un grain minuscule roule au fond du seau.",
    (1, 3, 1): "L'oreille grise a un peu de sable.",
    (1, 3, 2): "Du lait chaud a touché le doudou.",
    (1, 3, 3): "Un fil gris pend près du bol.",
    (2, 1, 1): "Près de la rampe, le ballon est un peu froid.",
    (2, 1, 2): "Une feuille jaune colle au ballon.",
    (2, 1, 3): "Tout rouge, le ballon a vu le veau.",
    (2, 2, 1): "Contre une marche, le seau sonne tout doux.",
    (2, 2, 2): "Près du seau, le métal du toboggan se tait.",
    (2, 2, 3): "Une goutte de lait brille dans le seau.",
    (2, 3, 1): "Tout gris, le doudou a vu le toboggan.",
    (2, 3, 2): "L'oreille molle dépasse près de la rampe.",
    (2, 3, 3): "La rampe brille encore, loin du doudou.",
    (3, 1, 1): "Un brin d'herbe colle au ballon.",
    (3, 1, 2): "La chaîne a fait cling, près du ballon.",
    (3, 1, 3): "Tout doux, le chat a touché le ballon.",
    (3, 2, 1): "L'anse du seau est froide, près de la corde.",
    (3, 2, 2): "Un cling lointain, et le seau.",
    (3, 2, 3): "Près du chat, le seau pose son ombre.",
    (3, 3, 1): "Tout doux, le doudou a senti le vent.",
    (3, 3, 2): "La corde se tait, près du doudou.",
    (3, 3, 3): "L'oreille grise dépasse près du chat.",
}

L1_019 = {
    1: [
        "narrateur|Sarah va vers le bac à sable.",
        "narrateur|Le sable est pâle, un peu frais.",
        "narrateur|Il glisse entre les doigts.",
        "narrateur|Ça fait chh, tout doux.",
        "enfant-f|Je joue, maman.",
        "maman|Tes lèvres sont sèches, hein ?",
        "papa|Le lait est encore au bidon.",
        "narrateur|Sarah pose les genoux.",
        "narrateur|Le sable est un peu froid.",
        "enfant-f|Il est frais, papa.",
        "maman|On reprend le bol, d'abord ?",
        "enfant-f|Oui, le lait chaud.",
        "papa|Une chose, puis l'autre.",
        "narrateur|Une poule passe près du bac.",
    ],
    2: [
        "narrateur|Sarah va vers le toboggan.",
        "narrateur|Le métal est froid sous la paume.",
        "narrateur|Les marches font toc, toc.",
        "enfant-f|Je glisse !",
        "papa|J'attends en bas.",
        "maman|Tes pieds sont froids, Sarah.",
        "narrateur|Sarah pose le pied, tout doux.",
        "narrateur|Le métal pique un peu.",
        "enfant-f|J'ai froid, maman.",
        "papa|Le lait est encore chaud, là-bas.",
        "maman|Les bottes, d'abord ?",
        "enfant-f|Puis le lait.",
        "papa|Une chose, puis l'autre.",
        "narrateur|Une feuille colle sur la rampe.",
    ],
    3: [
        "narrateur|Sarah va vers les balançoires.",
        "narrateur|La corde est un peu rêche.",
        "narrateur|Le siège est lisse, un peu froid.",
        "maman|Je pousse tout doux.",
        "enfant-f|Encore un peu ?",
        "papa|Tu as soif, Sarah ?",
        "narrateur|Sarah avance, puis revient.",
        "narrateur|Le vent lui touche le nez.",
        "enfant-f|J'ai soif, papa.",
        "maman|Le bidon fait ding, à la cuisine.",
        "papa|Le bol, d'abord, d'accord ?",
        "enfant-f|Oui, puis je reviens.",
        "maman|Une chose, puis l'autre.",
        "narrateur|La corde fait cling, puis se tait.",
    ],
}

C_019 = {
    1: [
        "narrateur|Sarah se relève du sable.",
        "maman|Une chose, puis la suivante.",
        "enfant-f|Ensuite le lait.",
        "papa|Oui, on rentre, avec nous.",
        "narrateur|Un grain reste sur sa joue.",
        "narrateur|Le bidon attend près de l'évier.",
    ],
    2: [
        "narrateur|Sarah pose les deux pieds par terre.",
        "papa|Une chose, puis la suivante.",
        "enfant-f|Les bottes, d'abord.",
        "maman|Oui, ensuite le bol, tout doux.",
        "narrateur|Une feuille de rampe bouge.",
        "narrateur|Le bidon brille, à la cuisine.",
    ],
    3: [
        "narrateur|Sarah pose un pied au sol.",
        "maman|Une chose, puis la suivante.",
        "enfant-f|Ensuite le lait, dans le bol.",
        "papa|Oui, tes pieds sont prêts.",
        "narrateur|La corde retombe, tout calme.",
        "narrateur|Le bidon attend près de la pierre.",
    ],
}

L2_019 = {
    1: [
        "narrateur|Sarah a choisi le ballon.",
        "narrateur|Il est rouge et lisse.",
        "narrateur|Il fait un petit bond.",
        "papa|Le ballon reste près de nous.",
        "enfant-f|Il est rouge, papa.",
        "maman|Le bol, ensuite, d'accord ?",
        "narrateur|Sarah pose le ballon près des bottes.",
        "enfant-f|Il attend.",
        "papa|Oui, une chose, puis l'autre.",
        "narrateur|Un brin d'herbe colle au cuir.",
    ],
    2: [
        "narrateur|Sarah a choisi le seau.",
        "narrateur|Le seau bleu a du sable.",
        "narrateur|L'anse est un peu froide.",
        "maman|C'est ton seau, Sarah.",
        "enfant-f|Il est bleu.",
        "papa|Tu le poses, d'abord ?",
        "narrateur|Elle le pose près de la porte.",
        "narrateur|Le seau fait un petit toc.",
        "maman|Ensuite le bidon, tout doux.",
        "enfant-f|Oui, maman.",
    ],
    3: [
        "narrateur|Sarah a choisi le doudou.",
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Un peu de paille est dessus.",
        "maman|Il t'attendait, Sarah.",
        "enfant-f|Il est doux.",
        "papa|Tu le poses, puis le bol ?",
        "narrateur|Elle le pose sur la chaise.",
        "enfant-f|Il reste.",
        "maman|Oui, une chose, puis l'autre.",
        "narrateur|L'oreille du doudou est chaude.",
    ],
}


def l3_body_019(i: int, j: int, k: int) -> list[str]:
    p = PLACE_019[i]
    y = TOY_019[j]
    a = ANIMAL_019[k]
    img = IMG_019[(i, j, k)]
    return [
        f"narrateur|{a['voir']}",
        f"narrateur|{a['feel']}",
        f"enfant-f|{a['child']}",
        "papa|Le bidon, d'abord.",
        "narrateur|Sarah ouvre le couvercle.",
        "narrateur|Elle verse, tout doux.",
        "enfant-f|C'est chaud.",
        "maman|Ensuite le bol, près de toi.",
        "narrateur|Elle boit une gorgée.",
        "papa|Merci, Sarah.",
        f"narrateur|{y['take']}",
        f"narrateur|{p['sol']}",
        f"narrateur|{img}",
    ]


def l3_fin_019(i: int, j: int, k: int) -> list[str]:
    p = PLACE_019[i]
    y = TOY_019[j]
    a = ANIMAL_019[k]
    img = IMG_019[(i, j, k)]
    starts = [
        "Sarah a le lait chaud dans le ventre.",
        "Voilà le bol vide, tout calme.",
        "Contre la pierre, le bidon ne fait plus ding.",
        "Au chaud, Sarah respire, tout doux.",
        "Près de la porte, le lait est fini.",
        "Sous la lampe, le bol brille encore.",
        "Dans ses mains, le jouet est prêt.",
        "Enfin le lait est là, tout bu.",
        "Voilà le bol vide, près du bidon.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return [
        f"narrateur|{first}",
        f"narrateur|{y['fin']}",
        f"enfant-f|{p['label'].capitalize()}, maman.",
        "maman|Oui, on y va, maintenant.",
        "papa|Bravo, Sarah.",
        f"narrateur|{p['fin']}",
        f"narrateur|{img}",
        f"narrateur|{a['fin']}",
        "narrateur|Le pain du four sent encore, tout près.",
    ]


def build_019() -> tuple[dict[str, list[str]], dict]:
    s: dict[str, list[str]] = {}
    extras: dict = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|Une poule picore près de la porte grise.",
        "narrateur|Ses petits pas font tic, sur la pierre.",
        "narrateur|La cuisine de la ferme est sombre.",
        "narrateur|Une petite lampe fait un rond jaune.",
        "narrateur|Ça sent le lait chaud.",
        "narrateur|Ça sent le pain du four.",
        "narrateur|Le sol de pierre est froid.",
        "narrateur|Les bottes de Sarah attendent.",
        "papa|Le bidon est là, Sarah.",
        "narrateur|Papa pose le bidon près de l'évier.",
        "narrateur|Ça fait ding.",
        "enfant-f|Je veux le lait chaud.",
        "enfant-f|Puis je joue dehors.",
        "maman|Le bol est sur la table.",
        "narrateur|En ce moment, Sarah attrape les bottes.",
        "narrateur|Elle prend aussi le bol.",
        "narrateur|Le bidon penche, un peu.",
        "narrateur|Une goutte tombe sur la pierre.",
        "enfant-f|Oh.",
        "papa|Le bol, d'abord, tout doux ?",
        "maman|Les bottes, ensuite.",
        "narrateur|La poule picore encore, dehors.",
    ]
    s["CHK_T0001_P0000"] = [
        "maman|Sarah va jouer où, après le lait ?",
        "narrateur|Le bac à sable.",
        "narrateur|Le toboggan.",
        "narrateur|Les balançoires.",
    ]
    q = [
        "narrateur|Sarah veut le lait, puis jouer.",
        "maman|Elle fait comment ?",
    ]
    t2 = [
        "papa|Tu prends quel jeu ?",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
    ]
    t3 = [
        "papa|Qui attend Sarah, près du lait ?",
        "narrateur|Le veau.",
        "narrateur|La poule.",
        "narrateur|Ou le chat.",
    ]
    t3_opt = {
        "option_1_label": "le veau",
        "option_2_label": "la poule",
        "option_3_label": "le chat",
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_019[i]
        s[f"{p}_Q0001"] = q
        s[f"{p}_C0001"] = C_019[i]
        s[f"{p}_T0002_P0000"] = t2
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            extra = {
                1: "Une poule passe près du bac.",
                2: "Une feuille colle sur la rampe.",
                3: "La corde fait cling, tout bas.",
            }[i]
            s[p2] = L2_019[j] + [
                f"narrateur|{extra}",
                f"narrateur|{PLACE_019[i]['son']}",
            ]
            s[f"{p2}_T0003_P0000"] = t3
            extras[f"{p2}_T0003_P0000"] = t3_opt
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_019(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_019(i, j, k)
    return s, extras


Q_019 = {
    "expected_answer": "une chose",
    "accepted_examples": "une chose | puis l'autre | d'abord | une chose puis l'autre | puis la suivante | les bottes | le bol",
    "retry_prompt": "Elle fait une chose, puis l'autre. Comment ?",
}


def main() -> None:
    s018 = build_018()
    write_tree(
        "TREE-AUT-018",
        "Nina veut son étoile de bois pour la mettre sur le sac. "
        "La caisse se renverse près des chaussures. L'étoile disparaît sous le tas. "
        "Elle ne la retrouve qu'en remettant cubes, livre et tasses dans la caisse.",
        "L'étoile sous la caisse de Nina",
        "Nina, papa, maman",
        "entrée d'immeuble, gouttière, caisse près des chaussures",
        s018,
        {"CHK_T0000_P0000": "gouttiere,pigeon"},
        Q_018,
    )
    relecture(
        "TREE-AUT-018",
        "L'étoile sous la caisse de Nina",
        "Immeuble, gouttière, caisse près des chaussures. Désir: étoile sur le sac. "
        "Tas de jouets et bottes. Question: où est l'étoile. "
        "Résolution: jouet dans la caisse, étoile dessous. "
        "T1 cuisine / jardin / chambre. T2 cubes / livre / dînette. "
        "T3 matin / sieste / soir. Fin: étoile sur le sac.",
        "Pas « on va ranger » / « après le jeu ». Zoé→Nina. 86 ids. "
        "Q=étoile. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins (images uniques).",
    )

    s019, extras019 = build_019()
    write_tree(
        "TREE-AUT-019",
        "Sarah veut le lait chaud du bidon, puis jouer dehors. "
        "Si elle prend bottes et bol ensemble, une goutte tombe. "
        "Une chose puis l'autre, le lait est bu, et elle peut jouer.",
        "Le bidon de lait de Sarah",
        "Sarah, papa, maman",
        "ferme, cuisine de pierre, bidon de lait",
        s019,
        {"CHK_T0000_P0000": "poule,lait"},
        Q_019,
        extras019,
    )
    relecture(
        "TREE-AUT-019",
        "Le bidon de lait de Sarah",
        "Ferme, poule, bidon. Désir: lait chaud puis jeu. "
        "Imprévu: bottes et bol à la fois, goutte. "
        "T1 bac / toboggan / balançoires. T2 ballon / seau / doudou. "
        "T3 veau / poule / chat. Fin: bol vide, jeu, animal.",
        "Pas « une étape après l'autre ». Sara→Sarah. N1 ≤10. "
        "Labels T3 = veau/poule/chat (plus Tom/Léa/Sami). "
        "Q=une chose. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins.",
    )


if __name__ == "__main__":
    main()
