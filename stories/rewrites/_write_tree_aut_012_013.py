#!/usr/bin/env python3
"""TREE-AUT-012 (N2 RAN implicite, train) et TREE-AUT-013 (N3 ROU vécue, mer)."""
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
) -> None:
    preview(sid, json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))["age_band"], scripts)
    src = json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={list(extra)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind in {"passage_question", "transition_question"}:
            scale, rate = 1.28, "slow"
        elif kind == "passage_fin":
            scale, rate = 1.26, "slow"
        else:
            scale, rate = 1.22, "medium"
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if kind == "passage_question" and q:
            by[cid].update(q)
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
# TREE-AUT-012 — Amir, train, caisse, doudou perdu sous le tas
# T1 temps  T2 lieu du wagon  T3 jouet qui cache
# ---------------------------------------------------------------------------

TIME_012 = {
    1: {
        "label": "le matin",
        "lum": "La lumière est pâle, un peu bleue.",
        "dehors": "Les champs ont encore de la rosée.",
        "extra": "Une goutte glisse tout droit sur la vitre.",
        "fin": "La rosée sèche, tout doux, sur l'herbe.",
    },
    2: {
        "label": "après la sieste",
        "lum": "La lumière est ronde, un peu chaude.",
        "dehors": "Les champs sont tièdes, tout calmes.",
        "extra": "La couverture de la sieste reste pliée.",
        "fin": "Les joues d'Amir sont encore un peu chaudes.",
    },
    3: {
        "label": "le soir",
        "lum": "Les lampes du wagon sont petites et jaunes.",
        "dehors": "Le ciel devient orange, tout lent.",
        "extra": "Un village passe, tout petit, tout loin.",
        "fin": "Dehors, les lumières des maisons s'allument.",
    },
}

PLACE_012 = {
    1: {
        "label": "la cuisine",
        "ou": "près de la table",
        "arrive": "La petite table du wagon devient une cuisine.",
        "detail": "Deux gobelets attendent, tout sages.",
        "tas": "Le tas de jouets est sur la table.",
        "geste": "Amir pose un gobelet, tout doux.",
        "fin": "Les gobelets restent vides, bien droits.",
    },
    2: {
        "label": "le jardin",
        "ou": "près de la fenêtre",
        "arrive": "Par la fenêtre, le wagon a un jardin de champs.",
        "detail": "L'herbe défile, puis une haie, puis un arbre.",
        "tas": "Les jouets sont collés contre la vitre froide.",
        "geste": "Amir pose un doigt sur la vitre.",
        "fin": "Une haie verte passe encore, tout près.",
    },
    3: {
        "label": "la chambre",
        "ou": "sur le siège",
        "arrive": "Le siège bleu devient une petite chambre.",
        "detail": "Amir tire la couverture sur ses genoux.",
        "tas": "Les jouets sont dans le nid du siège.",
        "geste": "Le tissu sent le savon propre.",
        "fin": "Le nid du siège est vide, maintenant.",
    },
}

TOY_012 = {
    1: {
        "label": "le ballon",
        "take": "Amir prend le ballon à deux mains.",
        "feel": "Il est souple, un peu rouge.",
        "child": "Il va dans la caisse.",
        "put": "Le ballon tombe dans la caisse.",
        "find": "Sous sa place, un coin de tissu gris.",
        "fin": "Le ballon ne roule plus, dans la caisse.",
    },
    2: {
        "label": "le seau",
        "take": "Amir soulève le seau bleu.",
        "feel": "Des crayons restent collés au fond.",
        "child": "Le seau, dans la caisse.",
        "put": "Le seau glisse, tout droit.",
        "find": "Sous le seau, le tissu gris attend.",
        "fin": "Les crayons restent sages, dans le seau.",
    },
    3: {
        "label": "le doudou",
        "take": "Amir écarte encore un jouet.",
        "feel": "Un trou s'ouvre au milieu du tas.",
        "child": "Il reste un trou.",
        "put": "Au fond du trou, le doudou gris.",
        "find": "Il sent encore la maison.",
        "fin": "Le doudou est au chaud, contre Amir.",
    },
}

IMG_012 = {
    (1, 1, 1): "Une miette de goûter colle au ballon, puis part.",
    (1, 1, 2): "Un crayon jaune roule vers le gobelet, tout lent.",
    (1, 1, 3): "Le doudou a une miette sur l'oreille, toute petite.",
    (1, 2, 1): "Le ballon a un reflet de champ, tout vert.",
    (1, 2, 2): "Le seau a une goutte de rosée sur le bord.",
    (1, 2, 3): "Le doudou voit une vache, tout contre la vitre.",
    (1, 3, 1): "Le ballon s'enfonce un peu dans la couverture.",
    (1, 3, 2): "Un crayon a glissé sous le pli du nid.",
    (1, 3, 3): "Le doudou était dans le pli chaud, tout gris.",
    (2, 1, 1): "Le ballon est tiède, comme les joues d'Amir.",
    (2, 1, 2): "Le seau a senti la couverture, un moment.",
    (2, 1, 3): "Le doudou a une joue un peu marquée.",
    (2, 2, 1): "Le ballon touche la vitre, puis rentre.",
    (2, 2, 2): "Le seau a un grain de lumière ronde.",
    (2, 2, 3): "Le doudou regarde un arbre qui s'éloigne.",
    (2, 3, 1): "Le ballon quitte le nid encore chaud.",
    (2, 3, 2): "Le seau rentre, près de la couverture pliée.",
    (2, 3, 3): "Le doudou quitte le nid pour les bras d'Amir.",
    (3, 1, 1): "Le ballon a un rond de lampe, tout jaune.",
    (3, 1, 2): "Le seau cliquette, tout bas, sous la lampe.",
    (3, 1, 3): "Le doudou a un reflet orange sur le ventre.",
    (3, 2, 1): "Le ballon voit les lumières du village.",
    (3, 2, 2): "Le seau a le ciel orange dedans, un instant.",
    (3, 2, 3): "Le doudou colle son nez à la vitre orange.",
    (3, 3, 1): "Le ballon s'endort dans la caisse, sous la lampe.",
    (3, 3, 2): "Le seau rentre, près du nid du soir.",
    (3, 3, 3): "Le doudou s'endort contre la vitre orange.",
}

L1_012 = {
    1: [
        "narrateur|La lumière est pâle sur la vitre.",
        "narrateur|Des gouttes glissent tout droit.",
        "enfant-m|Le ciel est tout blanc, papa.",
        "papa|Oui, les champs ont de la rosée.",
        "narrateur|Le tas de jouets cache le siège bleu.",
        "enfant-m|Je ne vois plus le doudou.",
        "maman|Il est sous quelque chose ?",
        "narrateur|Amir soulève le ballon.",
        "narrateur|Pas de tissu gris.",
        "papa|Et sous le seau ?",
        "narrateur|Des crayons seulement.",
        "narrateur|Un champ mouillé passe, tout lent.",
        "enfant-m|Il est perdu.",
        "maman|On peut voir dessous, tout doux.",
    ],
    2: [
        "narrateur|Amir a les joues un peu chaudes.",
        "narrateur|La couverture est pliée sur le siège.",
        "maman|Tu as bien dormi, Amir ?",
        "enfant-m|Un peu, les rails ont chanté.",
        "papa|Le train a roulé tout le temps.",
        "narrateur|Le tas de jouets est encore là.",
        "enfant-m|Mon doudou n'est plus dessus.",
        "maman|Il s'est caché pendant la sieste ?",
        "narrateur|Amir cherche près du sac.",
        "narrateur|L'odeur du goûter est encore là.",
        "papa|Sous la couverture, peut-être.",
        "narrateur|Un coin de tissu bleu seulement.",
        "enfant-m|Pas lui.",
        "maman|Le tas est encore haut, tu vois.",
    ],
    3: [
        "narrateur|Les lampes du wagon sont petites et jaunes.",
        "narrateur|Dehors, le ciel devient orange.",
        "enfant-m|Ça brille, maman.",
        "maman|Oui, le soir arrive doucement.",
        "narrateur|Les jouets font des ombres sur le siège.",
        "enfant-m|Je ne vois plus le gris.",
        "papa|Le doudou aime les cachettes, parfois.",
        "narrateur|Amir colle le nez à la vitre.",
        "narrateur|Un village passe, tout petit.",
        "maman|Tu as regardé sous la table ?",
        "enfant-m|Le ballon est là, pas lui.",
        "narrateur|Le seau a roulé contre le sac.",
        "papa|Le tas cache encore le fond.",
        "enfant-m|Je le veux pour la fenêtre.",
    ],
}

C_012 = {
    1: [
        "narrateur|Amir glisse un crayon dans la caisse.",
        "narrateur|Toc.",
        "maman|Tu regardes dessous ?",
        "enfant-m|Pas encore, maman.",
        "papa|Encore un, tout doux.",
        "narrateur|Un bout de siège reparaît, tout bleu.",
        "narrateur|La rosée brille encore dehors.",
    ],
    2: [
        "narrateur|Amir pose une tasse jouet dans la caisse.",
        "narrateur|Toc.",
        "papa|Le tas devient plus petit.",
        "enfant-m|Toujours pas.",
        "maman|Tu continues, tout calme ?",
        "narrateur|La lumière ronde touche le bois.",
        "narrateur|La couverture reste pliée, à côté.",
    ],
    3: [
        "narrateur|Amir pousse un cube vers la caisse.",
        "narrateur|Ça fait un petit bruit.",
        "maman|Les ombres bougent, tu vois ?",
        "enfant-m|Un peu, maman.",
        "papa|Encore un, près de la lampe.",
        "narrateur|Le fond du siège reparaît, tout lent.",
        "narrateur|Dehors, le ciel reste orange.",
    ],
}

L2_012 = {
    1: [
        "narrateur|La petite table du wagon devient une cuisine.",
        "narrateur|Deux gobelets attendent, tout sages.",
        "maman|On fait semblant de goûter ?",
        "enfant-m|Oui, le doudou aussi.",
        "narrateur|Le doudou n'est pas sur la table.",
        "papa|Il est sous le tas, peut-être.",
        "narrateur|Amir se penche vers le bois.",
        "narrateur|Le ballon et le seau sont en tas.",
        "enfant-m|Je verse le jus, d'abord.",
        "maman|Merci, c'est tiède, ce jus.",
        "papa|Tu sers, puis tu cherches ?",
        "enfant-m|Oui, papa.",
    ],
    2: [
        "narrateur|Par la fenêtre, le wagon a un jardin de champs.",
        "narrateur|L'herbe défile, puis une haie.",
        "papa|Tu vois les haies, Amir ?",
        "enfant-m|Oui, il y a un arbre.",
        "narrateur|Amir pose un doigt sur la vitre froide.",
        "maman|On joue au jardin, ici, tout près.",
        "narrateur|Les jouets sont collés contre la vitre.",
        "enfant-m|Le doudou voulait voir les vaches.",
        "papa|Il est sous le tas, contre la vitre ?",
        "narrateur|Une vache passe, loin, dans l'herbe.",
        "enfant-m|Elle est blanche et noire.",
        "maman|On cherche encore, tout doux.",
    ],
    3: [
        "narrateur|Le siège bleu devient une petite chambre.",
        "maman|On fait un nid avec la couverture ?",
        "enfant-m|Oui, c'est doux.",
        "narrateur|Amir tire la couverture sur ses genoux.",
        "papa|La chambre du train est prête.",
        "narrateur|Le tissu sent le savon propre.",
        "narrateur|Les jouets sont dans le nid du siège.",
        "enfant-m|Le doudou aime le nid.",
        "maman|Il est dessous, peut-être.",
        "narrateur|Amir soulève un coin chaud.",
        "narrateur|Le ballon et le seau bougent.",
        "papa|Tu es bien installé ?",
        "enfant-m|Oui, je cherche encore.",
    ],
}


def l3_body_012(i: int, j: int, k: int) -> list[str]:
    t = TIME_012[i]
    p = PLACE_012[j]
    y = TOY_012[k]
    img = IMG_012[(i, j, k)]
    return [
        f"narrateur|{t['lum']}",
        f"narrateur|{p['tas']}",
        f"narrateur|{y['take']}",
        f"narrateur|{y['feel']}",
        f"enfant-m|{y['child']}",
        f"narrateur|{y['put']}",
        "narrateur|Toc.",
        f"narrateur|{y['find']}",
        "enfant-m|Mon doudou !",
        "maman|Te voilà, petit.",
        "papa|Merci, tu l'as trouvé.",
        f"narrateur|{img}",
        "narrateur|Amir le serre contre sa joue.",
        f"narrateur|{t['dehors']}",
    ]


def l3_fin_012(i: int, j: int, k: int) -> list[str]:
    t = TIME_012[i]
    p = PLACE_012[j]
    y = TOY_012[k]
    img = IMG_012[(i, j, k)]
    starts = [
        "Le doudou a le nez sur la vitre.",
        "Amir tient le tissu gris, tout chaud.",
        "Contre la joue, le doudou est calme.",
        "Au chaud, le doudou écoute les rails.",
        "Près de la caisse, Amir respire.",
        "Sous la lampe, le tissu gris brille.",
        "Dans ses bras, le doudou est trouvé.",
        "Enfin le gris est là, tout doux.",
        "Voilà le doudou, contre la vitre.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return [
        f"narrateur|{first}",
        f"narrateur|{y['fin']}",
        f"enfant-m|Il voit les champs, papa.",
        "papa|Oui, il est bien là.",
        "maman|La caisse est calme, maintenant.",
        f"papa|Bravo, Amir.",
        f"narrateur|{p['fin']}",
        f"narrateur|{img}",
        f"narrateur|{t['fin']}",
        "narrateur|Les rails chantent encore, tout bas.",
    ]


def build_012() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|Un champ de blé se penche, tout entier.",
        "narrateur|Il passe, puis un autre.",
        "narrateur|La vitre est froide sous le nez d'Amir.",
        "narrateur|Le siège bleu est un peu rêche.",
        "narrateur|Une odeur de goûter sort du sac.",
        "papa|On est bien, ici.",
        "maman|Ta caisse est près de tes pieds.",
        "enfant-m|Je veux mon doudou, maman.",
        "enfant-m|Il va voir les champs avec moi.",
        "narrateur|La petite table se déplie.",
        "narrateur|Ça fait clic.",
        "narrateur|En ce moment, Amir ouvre la caisse.",
        "narrateur|Le ballon saute sur le siège.",
        "narrateur|Le seau bleu verse des crayons.",
        "narrateur|Le train donne un petit à-coup.",
        "narrateur|Les jouets glissent partout.",
        "enfant-m|Mon doudou ?",
        "papa|Il était dans la caisse.",
        "narrateur|Amir cherche sous la table.",
        "narrateur|Rien.",
        "maman|Tu as regardé près de la vitre ?",
        "enfant-m|Le tas est trop haut.",
        "papa|On peut voir dessous, tout doux.",
        "narrateur|Les champs défilent encore, tout verts.",
    ]
    s["CHK_T0001_P0000"] = [
        "papa|On cherche quand, Amir ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ]
    q = [
        "narrateur|Amir cherche son doudou.",
        "maman|Il est où ?",
    ]
    t2 = [
        "maman|Où cherches-tu, dans le wagon ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|La chambre.",
    ]
    t3 = [
        "papa|Quel jouet tu prends ?",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
    ]
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_012[i]
        s[f"{p}_Q0001"] = q
        s[f"{p}_C0001"] = C_012[i]
        s[f"{p}_T0002_P0000"] = t2
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2_012[j] + [
                f"narrateur|{TIME_012[i]['extra']}",
                f"narrateur|{PLACE_012[j]['geste']}",
            ]
            s[f"{p2}_T0003_P0000"] = t3
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_012(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_012(i, j, k)
    return s


Q_012 = {
    "expected_answer": "doudou",
    "accepted_examples": "doudou | le doudou | sous les jouets | sous le tas | dans la caisse | dessous",
    "retry_prompt": "Il cherche sous le tas. Où est le doudou ?",
}


# ---------------------------------------------------------------------------
# TREE-AUT-013 — Raphaël, maison de mer, carré d'or, séquence vécue
# T1 lieu  T2 jeu-étape  T3 moment de lumière
# ---------------------------------------------------------------------------

PLACE_013 = {
    1: {
        "label": "la cuisine",
        "sol": "Le carrelage est frais sous ses pieds.",
        "carre": "Le carré d'or est sur les carreaux.",
        "odeur": "Ça sent le pain chaud, tout près.",
        "fin": "Une miette reste sur la table, comme un grain.",
    },
    2: {
        "label": "le jardin",
        "sol": "Le sable du chemin colle un peu.",
        "carre": "Le carré d'or est sur la pierre du banc.",
        "odeur": "Le vent sent le thym et le sel.",
        "fin": "Une feuille de figuier bouge encore.",
    },
    3: {
        "label": "la chambre",
        "sol": "Le tapis est doux sous les orteils.",
        "carre": "Le carré d'or est sur le tapis rêche.",
        "odeur": "Le drap sent encore le savon de la mer.",
        "fin": "La coquille du rebord brille encore.",
    },
}

GAME_013 = {
    1: {
        "label": "les cubes",
        "obj": "les cubes",
        "do": "Raphaël pose un cube, puis un autre.",
        "feel": "Le bois sent le sapin, tout doux.",
        "child": "Une petite allée, papa.",
        "next": "L'allée de cubes mène vers le carré.",
        "fin": "La petite allée reste droite, vers la porte.",
    },
    2: {
        "label": "le livre",
        "obj": "le livre",
        "do": "Raphaël tourne une page, puis l'autre.",
        "feel": "Le papier est lisse, un peu froid.",
        "child": "Un bateau, maman !",
        "next": "Le bateau du livre regarde vers la mer.",
        "fin": "Le bateau reste sur la page, tout calme.",
    },
    3: {
        "label": "la dînette",
        "obj": "la dînette",
        "do": "Raphaël pose la tasse, puis il verse.",
        "feel": "La petite tasse est blanche, un peu froide.",
        "child": "Une gorgée, puis la porte.",
        "next": "La tasse vide attend, sage, sur la serviette.",
        "fin": "La petite tasse reste à sa place.",
    },
}

WHEN_013 = {
    1: {
        "label": "le matin",
        "lum": "La lumière est blanche, comme le sel.",
        "carre": "Le carré d'or est net, tout neuf.",
        "mer": "La mer brille, tout près, tout claire.",
        "fin": "Le sel pique un peu les lèvres de Raphaël.",
    },
    2: {
        "label": "après la sieste",
        "lum": "Les volets ont laissé une bande d'ombre.",
        "carre": "Le carré d'or a glissé vers la porte.",
        "mer": "La mer est tiède, on l'entend plus fort.",
        "fin": "L'ombre du figuier a bougé, tout lent.",
    },
    3: {
        "label": "le soir",
        "lum": "La mer parle plus bas, tout orange.",
        "carre": "Le carré d'or devient un rond de lampe.",
        "mer": "Un phare clignote, tout petit, tout loin.",
        "fin": "Le bois du seuil est frais, maintenant.",
    },
}

IMG_013 = {
    (1, 1, 1): "Un cube rouge a une miette de pain au coin.",
    (1, 1, 2): "Les cubes sont tièdes, près du bol vide.",
    (1, 1, 3): "La tour de cubes garde l'ombre de la lampe.",
    (1, 2, 1): "La tartine a une marque de dent, tout petite.",
    (1, 2, 2): "Le livre sent encore le fruit de la sieste.",
    (1, 2, 3): "La dernière page fait un bruit de papier.",
    (1, 3, 1): "Une goutte de lait brille près de la tasse.",
    (1, 3, 2): "La nappe de dînette est pliée, tout calme.",
    (1, 3, 3): "Les assiettes jouets montent sur l'étagère.",
    (2, 1, 1): "Les cubes du banc ont du soleil dessus.",
    (2, 1, 2): "Le vent pousse le cube léger, on le remet.",
    (2, 1, 3): "Papa rentre les cubes dans la boîte, tout bas.",
    (2, 2, 1): "Le poisson jaune du livre regarde le ciel.",
    (2, 2, 2): "La page a une petite ride, à cause du vent.",
    (2, 2, 3): "Raphaël tient le livre sous le bras, dehors.",
    (2, 3, 1): "Une fourmi change de chemin, près des assiettes.",
    (2, 3, 2): "La nappe a un pli de vent, on la secoue.",
    (2, 3, 3): "Le panier rentre, et la dînette cliquette tout bas.",
    (3, 1, 1): "Un cube bleu touche le carré, puis s'écarte.",
    (3, 1, 2): "Les cubes sont un peu chauds, sur le tapis.",
    (3, 1, 3): "La boîte de cubes se ferme, près du lit.",
    (3, 2, 1): "Le pull bleu a gardé une page, un moment.",
    (3, 2, 2): "Le livre sent le drap, encore un peu.",
    (3, 2, 3): "Raphaël pose le livre sur la chaise, tout doux.",
    (3, 3, 1): "La petite tasse a un reflet de coquille.",
    (3, 3, 2): "Une chaussette a glissé près de la dînette.",
    (3, 3, 3): "La dînette rentre, et la coquille reste au rebord.",
}

L1_013 = {
    1: [
        "narrateur|Raphaël pousse la porte de la cuisine.",
        "narrateur|Le carrelage est frais sous ses pieds.",
        "narrateur|Le pain fume encore un peu.",
        "maman|Viens, le bol t'attend.",
        "enfant-m|Je veux le carré, tout de suite.",
        "papa|Le bol d'abord, tout doux.",
        "narrateur|Raphaël tire sa chaise.",
        "narrateur|Il pose les pieds par terre.",
        "enfant-m|Ça sent le pain chaud.",
        "maman|Oui, une bouchée, puis le carré.",
        "narrateur|Il prend une bouchée.",
        "narrateur|Le lait est tiède contre sa lèvre.",
        "papa|Merci, tu t'es assis.",
        "narrateur|Dehors, la mer continue son chhh.",
        "narrateur|Le carré d'or attend sur les carreaux.",
    ],
    2: [
        "narrateur|Raphaël ouvre la porte du jardin.",
        "narrateur|Le vent sent le thym et le sel.",
        "narrateur|Le sable du chemin colle un peu.",
        "enfant-m|Je cours au carré !",
        "papa|Les chaussures, d'abord.",
        "narrateur|Raphaël enfile la gauche.",
        "narrateur|Puis la droite.",
        "narrateur|Ça fait toc toc sur la pierre.",
        "enfant-m|J'entends une mouette.",
        "maman|Moi aussi, on reste sur le chemin.",
        "narrateur|Il marche jusqu'au petit banc.",
        "papa|Tu as mis les deux chaussures.",
        "maman|Bravo, Raphaël.",
        "narrateur|Le soleil chauffe le bois du banc.",
        "narrateur|Le carré d'or est sur la pierre.",
    ],
    3: [
        "narrateur|Raphaël revient vers la chambre.",
        "narrateur|Le drap est encore chaud.",
        "narrateur|Le pull bleu attend sur la chaise.",
        "enfant-m|Le carré, et la mer !",
        "maman|Le pull, d'abord.",
        "narrateur|Il passe la tête dans le pull.",
        "narrateur|Le tricot gratte un tout petit peu.",
        "enfant-m|Il est doux, maman.",
        "papa|Ensuite les chaussettes.",
        "narrateur|Il les enfile, une puis l'autre.",
        "maman|Tu es habillé, maintenant.",
        "papa|Merci, le carré t'attend.",
        "narrateur|La coquille sur le rebord brille encore.",
        "narrateur|Le carré d'or est sur le tapis.",
        "narrateur|La mer reste tout près, derrière la vitre.",
    ],
}

C_013 = {
    1: [
        "narrateur|Raphaël avale une gorgée de lait.",
        "maman|Une chose, puis la suivante.",
        "enfant-m|Ensuite le carré.",
        "papa|Oui, on continue, avec nous.",
        "narrateur|Une miette brille sur la table.",
        "narrateur|Le carré d'or touche déjà un pied.",
    ],
    2: [
        "narrateur|Raphaël souffle, et le vent lui touche les cheveux.",
        "papa|Une chose, puis la suivante.",
        "enfant-m|Les chaussures sont mises.",
        "maman|Oui, ensuite le pas, tout doux.",
        "narrateur|Une feuille de figuier bouge.",
        "narrateur|Le carré d'or chauffe la pierre.",
    ],
    3: [
        "narrateur|Raphaël lisse une manche du pull.",
        "maman|Une chose, puis la suivante.",
        "enfant-m|Ensuite le carré, sur le tapis.",
        "papa|Oui, tes pieds sont prêts.",
        "narrateur|Le drap retombe, tout calme.",
        "narrateur|Le carré d'or attend près de la porte.",
    ],
}

L2_013 = {
    1: [
        "narrateur|Les cubes attendent, en bois clair.",
        "narrateur|Ils sentent le sapin.",
        "enfant-m|Une allée, papa.",
        "papa|Un cube, ensuite un autre.",
        "narrateur|Raphaël pose le cube rouge.",
        "narrateur|Puis le cube bleu.",
        "maman|Tu as fini ta petite allée ?",
        "enfant-m|Elle va vers le carré.",
        "papa|Oui, une chose, puis la suivante.",
        "narrateur|L'allée est petite et droite.",
    ],
    2: [
        "narrateur|Le livre a une couverture bleue, comme l'eau.",
        "maman|On ouvre, une page, puis l'autre.",
        "enfant-m|Un bateau !",
        "papa|Oui, tu as bien regardé.",
        "narrateur|Raphaël touche le papier lisse.",
        "maman|Tu as fini la page du bateau ?",
        "enfant-m|Ensuite la mer vraie.",
        "papa|Oui, le livre, puis le seuil.",
        "narrateur|Le bateau reste sur la page.",
        "narrateur|La mer vraie chante encore, dehors.",
    ],
    3: [
        "narrateur|La dînette est sur une serviette.",
        "narrateur|La petite tasse est blanche.",
        "enfant-m|Du thé, maman ?",
        "maman|D'abord la tasse, ensuite on verse.",
        "narrateur|Raphaël pose la tasse près du vrai bol.",
        "papa|Une gorgée du vrai bol, tout doux.",
        "narrateur|Il boit une gorgée.",
        "maman|Merci, la tasse jouet reste à sa place.",
        "enfant-m|Ensuite le carré.",
        "narrateur|Ça sent le pain et le sel, ensemble.",
    ],
}


def l3_body_013(i: int, j: int, k: int) -> list[str]:
    p = PLACE_013[i]
    g = GAME_013[j]
    w = WHEN_013[k]
    img = IMG_013[(i, j, k)]
    return [
        f"narrateur|{w['lum']}",
        f"narrateur|{p['carre']}",
        f"narrateur|{g['do']}",
        f"enfant-m|{g['child']}",
        f"papa|{g['next']}",
        f"narrateur|{w['carre']}",
        "narrateur|Raphaël pose un pied dans la lumière.",
        "narrateur|Puis l'autre pied.",
        "enfant-m|Je suis dans le carré !",
        "maman|Oui, ensuite la porte, tout doux.",
        "papa|Merci, tu as avancé sans te presser.",
        f"narrateur|{img}",
        f"narrateur|{w['mer']}",
    ]


def l3_fin_013(i: int, j: int, k: int) -> list[str]:
    p = PLACE_013[i]
    g = GAME_013[j]
    w = WHEN_013[k]
    img = IMG_013[(i, j, k)]
    starts = [
        "Raphaël a les pieds dans la lumière.",
        "Le carré d'or tient encore sous les orteils.",
        "Contre le seuil, le sel arrive déjà.",
        "Au bout du chemin, la mer dit chhh.",
        "Près de la porte, le carré glisse dehors.",
        "Sous ses pieds, le plancher est chaud.",
        "Dans le vent, une mouette passe, très haut.",
        "Enfin le sable mouillé, tout proche.",
        "Voilà l'eau, tout près de la maison.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return [
        f"narrateur|{first}",
        f"narrateur|{g['fin']}",
        "enfant-m|La mer, maman.",
        "maman|Oui, on y va, maintenant.",
        "papa|Bravo, Raphaël.",
        f"narrateur|{p['fin']}",
        f"narrateur|{img}",
        f"narrateur|{w['fin']}",
        "narrateur|La mer respire encore, tout près.",
    ]


def build_013() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|Un grain de sable brille sur le plancher.",
        "narrateur|Puis un autre, près du tapis.",
        "narrateur|Le soleil en fait un carré d'or.",
        "narrateur|Le carré touche un tapis rêche, couleur de coquille.",
        "narrateur|Sur le rebord, une coquille blanche attend.",
        "narrateur|Elle est encore un peu humide.",
        "narrateur|Ça sent le sel.",
        "narrateur|Ça sent aussi le pain, tout chaud.",
        "papa|Les volets, Raphaël.",
        "narrateur|Papa pousse les volets, tout doucement.",
        "narrateur|Les volets font clic.",
        "maman|L'eau de la casserole chante déjà.",
        "narrateur|En ce moment, Raphaël ouvre les yeux.",
        "narrateur|Ses pieds cherchent le tapis.",
        "enfant-m|Je veux le carré d'or.",
        "enfant-m|Après, je veux la mer.",
        "papa|Le carré d'abord, tout doux.",
        "narrateur|Raphaël attrape le pull et une chaussure.",
        "narrateur|Le carré glisse vers la porte.",
        "narrateur|La chaussure tombe, toc.",
        "enfant-m|Il part !",
        "maman|Une chose, puis la suivante.",
        "narrateur|La mer dit chhh, contre le sable mouillé.",
    ]
    s["CHK_T0001_P0000"] = [
        "papa|On commence où, Raphaël ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|La chambre.",
    ]
    q = [
        "narrateur|Raphaël veut le carré, puis la mer.",
        "maman|Il fait comment ?",
    ]
    t2 = [
        "papa|Quel jeu t'aide, ce matin ?",
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
        s[p] = L1_013[i]
        s[f"{p}_Q0001"] = q
        s[f"{p}_C0001"] = C_013[i]
        s[f"{p}_T0002_P0000"] = t2
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            extra = {
                1: "Une miette reste sur la table, à côté.",
                2: "Une mouette passe, très haut.",
                3: "La coquille du rebord brille encore.",
            }[i]
            s[p2] = L2_013[j] + [
                f"narrateur|{extra}",
                f"narrateur|{PLACE_013[i]['odeur']}",
            ]
            s[f"{p2}_T0003_P0000"] = t3
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_013(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_013(i, j, k)
    return s


Q_013 = {
    "expected_answer": "une chose",
    "accepted_examples": "une chose | puis l'autre | d'abord | une chose puis l'autre | puis la suivante",
    "retry_prompt": "Il fait une chose, puis la suivante. Comment ?",
}


def main() -> None:
    s012 = build_012()
    write_tree(
        "TREE-AUT-012",
        "Amir veut son doudou pour regarder les champs par la fenêtre du train. "
        "La caisse se renverse. Le doudou disparaît sous le tas. "
        "Il ne le retrouve qu'en remettant ballon, seau et jouets dans la caisse.",
        "Le doudou sous la caisse du train",
        "Amir, papa, maman",
        "wagon, fenêtre sur les champs, caisse de jouets",
        s012,
        {"CHK_T0000_P0000": "train"},
        Q_012,
    )
    relecture(
        "TREE-AUT-012",
        "Le doudou sous la caisse du train",
        "Train, champs, caisse. Désir: doudou à la vitre. À-coup, tas. "
        "Question: où est le doudou. Résolution: jouet dans la caisse, doudou dessous. "
        "T1 matin/sieste/soir. T2 table-cuisine / fenêtre-jardin / siège-chambre. "
        "T3 ballon / seau / doudou. Fin: doudou et champs.",
        "Pas « on va ranger » / « après le jeu ». Noé→Amir. 86 ids. "
        "Q=doudou. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins (images uniques).",
    )

    s013 = build_013()
    write_tree(
        "TREE-AUT-013",
        "Raphaël veut mettre ses pieds dans le carré d'or, puis aller voir la mer. "
        "S'il prend pull et chaussure ensemble, le carré glisse. "
        "Une chose puis la suivante, le carré le mène jusqu'au sable.",
        "Le carré d'or sur le plancher",
        "Raphaël, papa, maman",
        "petite maison au bord de la mer, carré de soleil",
        s013,
        {"CHK_T0000_P0000": "mer,volet"},
        Q_013,
    )
    relecture(
        "TREE-AUT-013",
        "Le carré d'or sur le plancher",
        "Maison de mer, coquille, carré d'or. Désir: carré puis mer. "
        "Imprévu: pull et chaussure à la fois, carré qui part. "
        "T1 cuisine (bol) / jardin (chaussures) / chambre (pull). "
        "T2 cubes-allée / livre-bateau / dînette-gorgée. "
        "T3 matin / sieste / soir. Fin: pieds dans la lumière, mer.",
        "Pas « une étape après l'autre ». Adam→Raphaël (Amir déjà en 012). "
        "Q=une chose. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins.",
    )


if __name__ == "__main__":
    main()
