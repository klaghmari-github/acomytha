#!/usr/bin/env python3
"""TREE-AUT-024 (N2 RAN implicite, caisse) et TREE-AUT-025 (N3 ROU vécue, flaques)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words


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
    extras = extras or {}
    src = json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))
    preview(sid, src["age_band"], scripts)
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={list(extra_ids)[:8]}")
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


def extras_labels(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


# ---------------------------------------------------------------------------
# TREE-AUT-024 — Sarah, cuisine, caisse sous la table, canard perdu
# T1 lieu  T2 jouet qui cache  T3 moment
# ---------------------------------------------------------------------------

TIME_024 = {
    1: {
        "label": "le matin",
        "lum": "La lumière est pâle, un peu bleue.",
        "dehors": "L'auvent du boulanger est encore mouillé.",
        "extra": "Une bicyclette sonne, tout loin, dans la rue.",
        "fin": "Une miette de pomme brille sur la nappe.",
    },
    2: {
        "label": "après la sieste",
        "lum": "La lumière est ronde, un peu chaude.",
        "dehors": "Le zinc du toit s'est tu, tout calme.",
        "extra": "Le plat de tarte fume encore un peu.",
        "fin": "Les joues de Sarah sont un peu chaudes.",
    },
    3: {
        "label": "le soir",
        "lum": "La lampe fait un rond jaune sur le bois.",
        "dehors": "Les lumières de la rue s'allument, tout lent.",
        "extra": "La tarte sent encore, toute douce.",
        "fin": "La fenêtre a un carré orange, tout calme.",
    },
}

PLACE_024 = {
    1: {
        "label": "la cuisine",
        "arrive": "Sarah se glisse sous la table.",
        "detail": "La nappe à carreaux lui frôle les cheveux.",
        "tas": "Le tas de jouets cache le carrelage.",
        "geste": "Sarah pose une paume sur le bois froid.",
        "fin": "Le bol d'eau attend encore, tout sage.",
    },
    2: {
        "label": "le jardin",
        "arrive": "Sarah pousse la caisse sur la marche mouillée.",
        "detail": "Une dalle luisante colle à ses genoux.",
        "tas": "Les jouets sont en tas, près du zinc.",
        "geste": "Sarah touche une goutte sur le zinc.",
        "fin": "Le zinc fait encore un tic, tout loin.",
    },
    3: {
        "label": "la chambre",
        "arrive": "Sarah pose la caisse sur le tapis rêche.",
        "detail": "L'oreiller sent encore le savon doux.",
        "tas": "Les jouets font un nid près du lit.",
        "geste": "Sarah soulève un coin de couverture.",
        "fin": "L'odeur de tarte arrive jusqu'au tapis.",
    },
}

TOY_024 = {
    1: {
        "label": "les cubes",
        "take": "Sarah prend le cube rouge à deux mains.",
        "feel": "Il est rêche, un peu farineux.",
        "child": "Il va dans la caisse.",
        "put": "Le cube tombe dans la caisse.",
        "find": "Sous sa place, un bec jaune.",
        "fin": "Les cubes ne bougent plus, dans la caisse.",
    },
    2: {
        "label": "le livre",
        "take": "Sarah soulève le livre, tout plat.",
        "feel": "Une page a un grain de farine.",
        "child": "Le livre, dans la caisse.",
        "put": "Le livre glisse, tout droit.",
        "find": "Sous le livre, le canard jaune.",
        "fin": "Les pages restent sages, dans la caisse.",
    },
    3: {
        "label": "la dînette",
        "take": "Sarah écarte encore une tasse.",
        "feel": "Un trou s'ouvre au milieu du tas.",
        "child": "La tasse, dans la caisse.",
        "put": "La tasse glisse, tout doux.",
        "find": "Au fond du trou, le canard jaune.",
        "fin": "La tasse est au chaud, dans la caisse.",
    },
}

IMG_024 = {
    (1, 1, 1): "Un cube rouge a une miette de pomme au coin.",
    (1, 1, 2): "Les cubes sont tièdes, près du plat qui fume.",
    (1, 1, 3): "La petite tour a un rond de lampe, tout jaune.",
    (1, 2, 1): "Une page a une tache de farine, toute petite.",
    (1, 2, 2): "Le livre sent encore la tarte, tout chaud.",
    (1, 2, 3): "La dernière page a un reflet orange.",
    (1, 3, 1): "Une tasse jouet a un grain de sucre au bord.",
    (1, 3, 2): "La nappe de dînette est pliée, tout calme.",
    (1, 3, 3): "Les assiettes jouets brillent sous la lampe.",
    (2, 1, 1): "Les cubes de la marche ont de la rosée dessus.",
    (2, 1, 2): "Une goutte du zinc roule sur le cube bleu.",
    (2, 1, 3): "Papa rentre les cubes, tout bas, près du zinc.",
    (2, 2, 1): "Le bateau du livre regarde l'auvent mouillé.",
    (2, 2, 2): "La page a une petite ride, à cause du vent.",
    (2, 2, 3): "Sarah tient le livre sous le bras, dehors.",
    (2, 3, 1): "Une feuille mouillée tombe dans l'assiette jouet.",
    (2, 3, 2): "La nappe a un pli de vent, on la secoue.",
    (2, 3, 3): "La dînette cliquette, tout bas, sur la marche.",
    (3, 1, 1): "Un cube bleu touche l'oreiller, puis s'écarte.",
    (3, 1, 2): "Les cubes sont un peu chauds, sur le tapis.",
    (3, 1, 3): "La caisse se ferme, près du lit, tout doux.",
    (3, 2, 1): "Le livre a gardé un pli de couverture.",
    (3, 2, 2): "Le livre sent le drap, encore un peu.",
    (3, 2, 3): "Sarah pose le livre sur la chaise, tout doux.",
    (3, 3, 1): "La petite tasse a un reflet d'oreiller.",
    (3, 3, 2): "Une chaussette a glissé près de la dînette.",
    (3, 3, 3): "La dînette rentre, et le tapis redevient plat.",
}

L1_024 = {
    1: [
        "narrateur|Sarah se glisse sous la table.",
        "narrateur|La nappe à carreaux lui frôle les cheveux.",
        "narrateur|Ça sent les pommes chaudes, tout près.",
        "enfant-f|Je ne vois plus le canard.",
        "maman|Il est sous quelque chose ?",
        "narrateur|Sarah soulève le cube rouge.",
        "narrateur|Pas de bec jaune.",
        "papa|Et sous le livre ?",
        "narrateur|Un grain de farine seulement.",
        "narrateur|Le bol d'eau fume encore, tout sage.",
        "enfant-f|Il est perdu.",
        "maman|On peut voir dessous, tout doux.",
        "papa|Le tas est encore haut, tu vois ?",
        "narrateur|Le frigo fait un petit ronron.",
    ],
    2: [
        "narrateur|Sarah pousse la caisse sur la marche.",
        "narrateur|Une dalle luisante colle à ses genoux.",
        "papa|Le zinc goutte encore, tu entends ?",
        "enfant-f|Tic, tic.",
        "narrateur|Les jouets sont en tas, près du zinc.",
        "enfant-f|Mon canard n'est plus dessus.",
        "maman|Il s'est caché sous le tas ?",
        "narrateur|Sarah cherche près de la dalle.",
        "narrateur|L'odeur de tarte arrive jusqu'ici.",
        "papa|Sous la feuille, peut-être.",
        "narrateur|Une feuille mouillée seulement.",
        "enfant-f|Pas lui.",
        "maman|Le tas cache encore le fond.",
        "narrateur|Une goutte tombe du zinc, ploc.",
    ],
    3: [
        "narrateur|Sarah pose la caisse sur le tapis.",
        "narrateur|L'oreiller sent encore le savon doux.",
        "enfant-f|Le canard voulait le nid.",
        "maman|Il est dessous, peut-être ?",
        "narrateur|Les jouets font un nid près du lit.",
        "papa|Tu as regardé sous la couverture ?",
        "enfant-f|Le cube est là, pas lui.",
        "narrateur|Sarah soulève un coin chaud.",
        "narrateur|Le livre et la tasse bougent.",
        "maman|Le tas est encore haut.",
        "enfant-f|Je le veux pour l'eau tiède.",
        "papa|On peut voir dessous, tout doux.",
        "narrateur|L'odeur de tarte entre par la porte.",
        "narrateur|Un rayon pâle touche le tapis.",
    ],
}

C_024 = {
    1: [
        "narrateur|Sarah glisse un crayon dans la caisse.",
        "narrateur|Ça fait un petit bruit.",
        "maman|Tu regardes dessous ?",
        "enfant-f|Pas encore, maman.",
        "papa|Encore un, tout doux.",
        "narrateur|Un bout de carrelage reparaît, tout froid.",
        "narrateur|Les pommes brillent encore dans le plat.",
    ],
    2: [
        "narrateur|Sarah pose une feuille à côté de la caisse.",
        "narrateur|La dalle reparaît, un peu.",
        "papa|Le tas devient plus petit.",
        "enfant-f|Toujours pas.",
        "maman|Tu continues, tout calme ?",
        "narrateur|Une goutte du zinc touche le bois.",
        "narrateur|La caisse est rêche, sous la paume.",
    ],
    3: [
        "narrateur|Sarah pousse un cube vers la caisse.",
        "narrateur|Ça fait un petit bruit.",
        "maman|Le tapis reparaît, tu vois ?",
        "enfant-f|Un peu, maman.",
        "papa|Encore un, près de l'oreiller.",
        "narrateur|Le fond du nid reparaît, tout lent.",
        "narrateur|La tarte sent encore, tout près.",
    ],
}

L2_024 = {
    1: [
        "narrateur|Les cubes sentent le bois, un peu farine.",
        "narrateur|Sarah pose le rouge, puis le bleu.",
        "enfant-f|Une petite tour, papa.",
        "papa|Elle est un peu penchée, tu vois ?",
        "narrateur|La tour cache encore le fond.",
        "maman|Le canard n'est pas dessus.",
        "enfant-f|Il est dessous, je crois.",
        "papa|On soulèvera, tout doux.",
        "narrateur|Sarah touche le cube du sommet.",
        "narrateur|Un grain de farine reste au coin.",
    ],
    2: [
        "narrateur|Le livre a une couverture lisse.",
        "narrateur|Il y a un bateau sur la page.",
        "enfant-f|Un bateau, maman.",
        "maman|Tu tournes, tout doux ?",
        "narrateur|Le papier fait frou, tout bas.",
        "papa|Le canard n'est pas sur la page.",
        "enfant-f|Il voulait voir le bateau.",
        "maman|Il est sous le tas, peut-être.",
        "narrateur|Sarah pose la main sur le papier.",
        "narrateur|Un grain de farine colle au bord.",
    ],
    3: [
        "narrateur|La dînette est prête, près du tas.",
        "narrateur|Sarah pose une tasse.",
        "narrateur|Ça fait tic.",
        "enfant-f|Je sers le thé, papa.",
        "papa|Tu sers maman d'abord ?",
        "maman|Merci, c'est tiède, ce thé.",
        "narrateur|La cuillère tape le bord.",
        "enfant-f|Le canard aussi, une gorgée.",
        "papa|Il n'est pas dans la tasse.",
        "maman|Sous le tas, peut-être ?",
        "narrateur|Sarah se penche vers le trou.",
    ],
}


def l3_body_024(i: int, j: int, k: int) -> list[str]:
    t = TIME_024[k]
    p = PLACE_024[i]
    y = TOY_024[j]
    img = IMG_024[(i, j, k)]
    return [
        f"narrateur|{t['lum']}",
        f"narrateur|{p['tas']}",
        f"narrateur|{y['take']}",
        f"narrateur|{y['feel']}",
        f"enfant-f|{y['child']}",
        f"narrateur|{y['put']}",
        "narrateur|Ça fait un petit bruit.",
        f"narrateur|{y['find']}",
        "enfant-f|Mon canard !",
        "maman|Te voilà, petit.",
        "papa|Merci, tu l'as trouvé.",
        f"narrateur|{img}",
        "narrateur|Sarah le serre contre sa joue.",
        f"narrateur|{t['dehors']}",
    ]


def l3_fin_024(i: int, j: int, k: int) -> list[str]:
    t = TIME_024[k]
    p = PLACE_024[i]
    y = TOY_024[j]
    img = IMG_024[(i, j, k)]
    starts = [
        "Le canard a de l'eau sur le bec.",
        "Sarah tient le bois jaune, tout chaud.",
        "Contre la joue, le canard est calme.",
        "Au chaud, le canard écoute le zinc.",
        "Près de la caisse, Sarah respire.",
        "Sous la lampe, le bec jaune brille.",
        "Dans ses mains, le canard est trouvé.",
        "Enfin le jaune est là, tout doux.",
        "Voilà le canard, près du bol.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return [
        f"narrateur|{first}",
        f"narrateur|{y['fin']}",
        "enfant-f|Il va dans l'eau, papa.",
        "papa|Oui, il est bien là.",
        "maman|La caisse est calme, maintenant.",
        "papa|Bravo, Sarah.",
        f"narrateur|{p['fin']}",
        f"narrateur|{img}",
        f"narrateur|{t['fin']}",
        "narrateur|Le zinc du toit fait encore tic, tout bas.",
    ]


def build_024() -> dict[str, list[str]]:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|Le zinc du toit fait tic, tout lent.",
        "narrateur|Une goutte, puis une autre.",
        "narrateur|Dans la cuisine, la pâte aux pommes sent chaud.",
        "narrateur|La nappe à carreaux est un peu rêche.",
        "narrateur|Sous la table, une caisse en bois attend.",
        "papa|Les pommes sont tièdes, Sarah.",
        "maman|On fait la tarte, tout doux.",
        "enfant-f|Je veux le canard, maman.",
        "enfant-f|Il va dans l'eau tiède.",
        "narrateur|Le bol d'eau fume un peu.",
        "narrateur|En ce moment, Sarah tire la caisse.",
        "narrateur|Les cubes tombent sur le carrelage.",
        "narrateur|Le livre glisse, tout plat.",
        "narrateur|Une tasse de dînette roule.",
        "enfant-f|Mon canard ?",
        "papa|Il était dans la caisse.",
        "narrateur|Sarah cherche sous la table.",
        "narrateur|Rien.",
        "maman|Tu as regardé sous le tas ?",
        "enfant-f|Le tas est trop haut.",
        "papa|On peut voir dessous, tout doux.",
        "narrateur|Les pommes brillent encore, dans le plat.",
    ]
    s["CHK_T0001_P0000"] = [
        "papa|Où cherches-tu, Sarah ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|La chambre.",
    ]
    q = [
        "narrateur|Sarah cherche son canard.",
        "maman|Il est où ?",
    ]
    t2 = [
        "papa|Quel jouet tu prends ?",
        "narrateur|Les cubes.",
        "narrateur|Le livre.",
        "narrateur|La dînette.",
    ]
    t3 = [
        "maman|On cherche quand ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ]
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_024[i]
        s[f"{p}_Q0001"] = q
        s[f"{p}_C0001"] = C_024[i]
        s[f"{p}_T0002_P0000"] = t2
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2_024[j] + [
                f"narrateur|{PLACE_024[i]['geste']}",
                f"narrateur|{PLACE_024[i]['detail']}",
            ]
            s[f"{p2}_T0003_P0000"] = t3
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_024(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_024(i, j, k)
    return s


Q_024 = {
    "expected_answer": "canard",
    "accepted_examples": "canard | le canard | sous le tas | dessous | sous la table | dans la caisse",
    "retry_prompt": "Elle cherche sous le tas. Où est le canard ?",
}


# ---------------------------------------------------------------------------
# TREE-AUT-025 — Nina, parc de la fontaine, bottes puis une flaque, puis l'autre
# T1 lieu du parc  T2 objet  T3 quelle flaque d'abord
# ---------------------------------------------------------------------------

PLACE_025 = {
    1: {
        "label": "le bac à sable",
        "sol": "Le sable est froid, un peu collant.",
        "eau": "Une flaque tient au milieu du bac.",
        "odeur": "Ça sent le sable mouillé, tout près.",
        "fin": "Un grain de sable reste sur la botte.",
    },
    2: {
        "label": "le toboggan",
        "sol": "Les marches du toboggan sont froides.",
        "eau": "Une flaque attend tout en bas.",
        "odeur": "Le plastique mouillé sent un peu.",
        "fin": "Une goutte glisse encore sur la rampe.",
    },
    3: {
        "label": "les balançoires",
        "sol": "Le siège de la balançoire est encore humide.",
        "eau": "Une flaque tremble sous les chaînes.",
        "odeur": "Le vent sent le buis coupé.",
        "fin": "Une chaîne goutte encore, tout léger.",
    },
}

OBJ_025 = {
    1: {
        "label": "le ballon",
        "take": "Nina prend le ballon à deux mains.",
        "feel": "Il est souple, un peu mouillé.",
        "child": "Il vient aux flaques.",
        "fin": "Le ballon ne roule plus, contre elle.",
    },
    2: {
        "label": "le seau",
        "take": "Nina soulève le seau par l'anse.",
        "feel": "L'anse est lisse, un peu froide.",
        "child": "Pour l'eau, papa.",
        "fin": "Le seau a un peu d'eau, au fond.",
    },
    3: {
        "label": "le doudou",
        "take": "Nina serre le doudou contre sa veste.",
        "feel": "Le tissu est doux, un peu plat.",
        "child": "Il regarde l'eau, lui aussi.",
        "fin": "Le doudou a une goutte sur l'oreille.",
    },
}

PUDDLE_025 = {
    1: {
        "label": "la petite flaque",
        "eau": "L'eau est mince, comme une assiette.",
        "pied": "Nina pose le pied gauche dedans.",
        "next": "La flaque du banc attend, plus loin.",
        "next_do": "Nina marche jusqu'au banc, tout lent.",
        "fin": "La petite flaque redevient calme.",
    },
    2: {
        "label": "la flaque du banc",
        "eau": "L'eau du banc tient le ciel, tout gris.",
        "pied": "Nina pose le pied près du pied du banc.",
        "next": "La grande flaque brille, vers la fontaine.",
        "next_do": "Nina marche vers la fontaine, tout doux.",
        "fin": "Le banc vert goutte encore, tout doux.",
    },
    3: {
        "label": "la grande flaque",
        "eau": "L'eau est large, près du bassin.",
        "pied": "Nina entre par le bord, d'abord.",
        "next": "Une petite flaque reste près de la grille.",
        "next_do": "Nina revient vers la grille, tout lent.",
        "fin": "La grande flaque a des ronds, encore.",
    },
}

IMG_025 = {
    (1, 1, 1): "Le ballon a un grain de sable collé.",
    (1, 1, 2): "Le ballon touche l'eau du banc, un instant.",
    (1, 1, 3): "Le ballon fait un rond dans la grande flaque.",
    (1, 2, 1): "Le seau prend un peu de sable mouillé.",
    (1, 2, 2): "Le seau sonne, tout bas, contre le banc.",
    (1, 2, 3): "Le seau a de l'eau du bassin, au fond.",
    (1, 3, 1): "L'oreille du doudou a un grain de sable.",
    (1, 3, 2): "Le doudou voit le ciel dans l'eau du banc.",
    (1, 3, 3): "Le doudou a une goutte du bassin sur le ventre.",
    (2, 1, 1): "Le ballon glisse un peu sur la rampe mouillée.",
    (2, 1, 2): "Le ballon s'assoit un moment sur le banc vert.",
    (2, 1, 3): "Le ballon fait plouf, tout près du bassin.",
    (2, 2, 1): "Le seau a reçu une goutte du toboggan.",
    (2, 2, 2): "Le seau pend, près du banc encore mouillé.",
    (2, 2, 3): "Le seau verse un filet, puis s'arrête.",
    (2, 3, 1): "Le doudou a vu la rampe, depuis les bras.",
    (2, 3, 2): "Le doudou s'appuie au banc, tout doux.",
    (2, 3, 3): "Le doudou écoute la fontaine, tout contre Nina.",
    (3, 1, 1): "Le ballon passe sous la chaîne, tout lent.",
    (3, 1, 2): "Le ballon roule jusqu'au pied du banc.",
    (3, 1, 3): "Le ballon s'arrête au bord de la grande flaque.",
    (3, 2, 1): "Le seau est froid, sous la balançoire.",
    (3, 2, 2): "Le seau a pris un peu d'eau du banc.",
    (3, 2, 3): "Le seau reflète la fontaine, un instant.",
    (3, 3, 1): "Le doudou a une goutte de chaîne sur l'oreille.",
    (3, 3, 2): "Le doudou regarde le banc, tout calme.",
    (3, 3, 3): "Le doudou sent le buis, et l'eau froide.",
}

L1_025 = {
    1: [
        "narrateur|Nina s'assoit au bord du bac.",
        "narrateur|Le sable est froid, un peu collant.",
        "enfant-f|La flaque du bac brille.",
        "papa|Tes pieds sont encore nus.",
        "narrateur|Nina enfile la botte gauche.",
        "narrateur|Le caoutchouc est froid, tout près.",
        "enfant-f|Elle pince un peu.",
        "maman|Et l'autre, tout doux ?",
        "narrateur|La droite attend dans l'herbe mouillée.",
        "papa|Tu la vois ?",
        "enfant-f|Oui, papa.",
        "narrateur|Un grain de sable colle à la chaussette.",
        "maman|L'eau est déjà là, dans le bac.",
        "narrateur|Nina regarde l'eau, sans bouger.",
    ],
    2: [
        "narrateur|Nina pose la main sur la rampe.",
        "narrateur|Le plastique est froid, encore mouillé.",
        "enfant-f|Je glisse dans l'eau !",
        "papa|Les bottes, d'abord.",
        "narrateur|Nina s'assoit sur la marche du bas.",
        "narrateur|Elle pousse le pied gauche.",
        "enfant-f|Ça fait flouc.",
        "maman|L'autre est près de toi ?",
        "narrateur|La botte droite brille dans l'herbe.",
        "papa|Tu la prends ?",
        "enfant-f|Oui, je la vois.",
        "narrateur|Une goutte tombe de la rampe, ploc.",
        "maman|La flaque du bas attend.",
        "narrateur|Nina souffle, les joues un peu roses.",
    ],
    3: [
        "narrateur|Nina s'assoit sur le banc vert.",
        "narrateur|Le bois est encore mouillé.",
        "enfant-f|Je veux l'eau sous les chaînes.",
        "maman|Tes pieds sont encore nus.",
        "narrateur|Nina enfile la botte gauche.",
        "narrateur|Le caoutchouc colle un peu.",
        "papa|L'autre, près du pied du banc ?",
        "enfant-f|Elle est là.",
        "narrateur|La chaîne fait un bruit de goutte.",
        "maman|Tu as froid aux orteils ?",
        "enfant-f|Un peu, maman.",
        "papa|La botte droite est prête.",
        "narrateur|Nina la regarde, sans la mettre.",
        "narrateur|Une flaque tremble sous les chaînes.",
    ],
}

C_025 = {
    1: [
        "narrateur|Nina prend la botte droite.",
        "narrateur|Elle pousse le pied dedans.",
        "enfant-f|Les deux, maintenant.",
        "papa|Merci, Nina.",
        "narrateur|Elle se lève.",
        "narrateur|Le sable fait crac, sous les bottes.",
        "maman|Tu es prête pour l'eau ?",
    ],
    2: [
        "narrateur|Nina attrape la botte droite.",
        "narrateur|Elle pousse, tout doux.",
        "enfant-f|Ça y est.",
        "maman|Merci, ma grande.",
        "narrateur|Nina se lève près de la rampe.",
        "narrateur|Le gravier fait crac, sous les semelles.",
        "papa|La flaque du bas est là.",
    ],
    3: [
        "narrateur|Nina enfile la botte droite, sur le banc.",
        "narrateur|Le bois goutte encore, tout lent.",
        "enfant-f|Mes pieds sont au chaud.",
        "papa|Merci, Nina.",
        "narrateur|Elle pose les deux pieds par terre.",
        "narrateur|Le gravier chante sous le caoutchouc.",
        "maman|L'eau sous les chaînes t'attend.",
    ],
}

L2_025 = {
    1: [
        "narrateur|Près des bottes, le ballon attend.",
        "narrateur|Il est souple, un peu mouillé.",
        "enfant-f|Il vient avec moi.",
        "papa|Tu le prends à deux mains ?",
        "narrateur|Nina le serre contre sa veste.",
        "maman|Tes bottes tiennent bien ?",
        "enfant-f|Oui, elles font flouc.",
        "papa|L'eau est plus loin, tu vois ?",
        "narrateur|Nina avance d'un pas.",
        "narrateur|Elle ne saute pas encore.",
    ],
    2: [
        "narrateur|Près de la grille, le seau bleu attend.",
        "narrateur|L'anse est lisse, un peu froide.",
        "enfant-f|Pour l'eau, maman.",
        "maman|Tu le prends par l'anse ?",
        "narrateur|Nina soulève le seau.",
        "papa|Tes bottes sont mises, toutes les deux.",
        "enfant-f|Oui, papa.",
        "maman|L'eau brille, juste là.",
        "narrateur|Nina marche, tout lent.",
        "narrateur|Le seau tape un peu sa jambe.",
    ],
    3: [
        "narrateur|Sur le banc mouillé, le doudou attend.",
        "narrateur|Le tissu est doux, un peu plat.",
        "enfant-f|Il va voir l'eau.",
        "papa|Tu le sers contre toi ?",
        "narrateur|Nina le prend à deux mains.",
        "maman|Tes bottes font flouc, tu entends ?",
        "enfant-f|Oui, maman.",
        "papa|L'eau brille encore, plus loin.",
        "narrateur|Nina avance, sans sauter encore.",
        "narrateur|Le doudou a le nez vers l'eau.",
    ],
}


def l3_body_025(i: int, j: int, k: int) -> list[str]:
    p = PLACE_025[i]
    o = OBJ_025[j]
    u = PUDDLE_025[k]
    img = IMG_025[(i, j, k)]
    return [
        f"narrateur|{u['eau']}",
        f"narrateur|{p['eau']}",
        f"narrateur|{o['take']}",
        f"enfant-f|{o['child']}",
        f"narrateur|{u['pied']}",
        "narrateur|L'eau est froide autour de la botte.",
        "enfant-f|Elle pique un peu !",
        "papa|Oui, tout doux.",
        "narrateur|Puis l'autre pied, dans la même eau.",
        f"maman|{u['next']}",
        f"narrateur|{u['next_do']}",
        "enfant-f|Encore celle-là !",
        "narrateur|Nina pose un pied, puis l'autre.",
        f"narrateur|{img}",
    ]


def l3_fin_025(i: int, j: int, k: int) -> list[str]:
    p = PLACE_025[i]
    o = OBJ_025[j]
    u = PUDDLE_025[k]
    img = IMG_025[(i, j, k)]
    starts = [
        "Nina a les bottes dans l'eau.",
        "La flaque tient encore sous les semelles.",
        "Contre le gravier, l'eau fait des ronds.",
        "Au bout du chemin, la fontaine dit chhh.",
        "Près du banc, une goutte tombe encore.",
        "Sous ses pieds, le caoutchouc est froid.",
        "Dans le buis, un oiseau secoue une aile.",
        "Enfin l'eau froide, autour des bottes.",
        "Voilà le bassin, tout proche, tout calme.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return [
        f"narrateur|{first}",
        f"narrateur|{u['fin']}",
        "enfant-f|Les flaques, maman.",
        "maman|Oui, tes bottes sont toutes mouillées.",
        "papa|Bravo, Nina.",
        f"narrateur|{o['fin']}",
        f"narrateur|{p['fin']}",
        f"narrateur|{img}",
        f"narrateur|{p['odeur']}",
        "narrateur|La fontaine tousse encore, tout près.",
    ]


def build_025() -> tuple[dict[str, list[str]], dict[str, dict]]:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = [
        "narrateur|La fontaine du parc tousse encore.",
        "narrateur|Un filet d'eau tombe dans le bassin.",
        "narrateur|Le gravier est sombre, tout mouillé.",
        "narrateur|Ça sent le buis, et la terre.",
        "narrateur|Un banc vert brille, encore mouillé.",
        "narrateur|Près de la grille, deux bottes attendent.",
        "narrateur|Elles ont des grenouilles dessus, toutes vertes.",
        "papa|La pluie est partie, Nina.",
        "maman|Le parc est à nous, maintenant.",
        "enfant-f|Je veux les flaques !",
        "narrateur|En ce moment, Nina court vers la grille.",
        "narrateur|Elle a encore un pied nu.",
        "narrateur|Une goutte froide lui touche l'orteil.",
        "maman|Les bottes, d'abord.",
        "papa|Une, puis l'autre.",
        "narrateur|Nina s'arrête, tout près des semelles.",
        "enfant-f|Elles sont froides, papa.",
        "maman|Oui, et l'eau aussi.",
        "narrateur|La fontaine continue son petit chhh.",
    ]
    s["CHK_T0001_P0000"] = [
        "papa|On va où, Nina ?",
        "narrateur|Le bac à sable.",
        "narrateur|Le toboggan.",
        "narrateur|Les balançoires.",
    ]
    extras["CHK_T0001_P0000"] = extras_labels("le bac à sable", "le toboggan", "les balançoires")
    q = [
        "narrateur|Nina veut les flaques.",
        "maman|Elle met quoi, d'abord ?",
    ]
    t2 = [
        "papa|Tu prends quoi ?",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
    ]
    t3 = [
        "maman|Quelle flaque, d'abord ?",
        "narrateur|La petite flaque.",
        "narrateur|La flaque du banc.",
        "narrateur|La grande flaque.",
    ]
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_025[i]
        s[f"{p}_Q0001"] = q
        s[f"{p}_C0001"] = C_025[i]
        s[f"{p}_T0002_P0000"] = t2
        extras[f"{p}_T0002_P0000"] = extras_labels("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2_025[j] + [
                f"narrateur|{PLACE_025[i]['sol']}",
                f"narrateur|{PLACE_025[i]['odeur']}",
            ]
            s[f"{p2}_T0003_P0000"] = t3
            extras[f"{p2}_T0003_P0000"] = extras_labels(
                "la petite flaque", "la flaque du banc", "la grande flaque"
            )
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_025(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_025(i, j, k)
    return s, extras


Q_025 = {
    "expected_answer": "bottes",
    "accepted_examples": "bottes | les bottes | d'abord les bottes | une puis l'autre | la botte | les deux bottes",
    "retry_prompt": "Elle enfile les bottes, puis une flaque. D'abord ?",
}


def main() -> None:
    s024 = build_024()
    write_tree(
        "TREE-AUT-024",
        "Sarah veut son canard jaune dans l'eau tiède, pendant la tarte aux pommes. "
        "Elle tire la caisse sous la table. Les jouets tombent. Le canard disparaît sous le tas. "
        "Elle ne le retrouve qu'en remettant cubes, livre et tasses dans la caisse.",
        "Le canard sous la caisse de Sarah",
        "Sarah, papa, maman",
        "cuisine de village, nappe à carreaux, caisse sous la table, tarte aux pommes",
        s024,
        {"CHK_T0000_P0000": "pluie,caisse"},
        Q_024,
    )
    relecture(
        "TREE-AUT-024",
        "Le canard sous la caisse de Sarah",
        "Cuisine, zinc, tarte. Désir: canard dans l'eau tiède. Caisse tirée, tas. "
        "Question: où est le canard. Résolution: jouet dans la caisse, canard dessous. "
        "T1 cuisine / jardin / chambre. T2 cubes / livre / dînette. "
        "T3 matin / sieste / soir. Fin: canard et bol.",
        "Pas « on va ranger » / « après le jeu ». Inès→Sarah. 86 ids. "
        "Q=canard. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins (images uniques).",
    )

    s025, extras025 = build_025()
    write_tree(
        "TREE-AUT-025",
        "Nina veut les flaques du parc de la fontaine. Elle court avec un pied nu. "
        "Une goutte lui touche l'orteil. Elle enfile une botte, puis l'autre. "
        "Ensuite une flaque, puis la suivante. Les bottes font flouc jusqu'au bassin.",
        "Les flaques de Nina près de la fontaine",
        "Nina, papa, maman",
        "parc de la fontaine après la pluie, gravier, banc vert, bottes à grenouilles",
        s025,
        {"CHK_T0000_P0000": "fontaine,gravier,bottes"},
        Q_025,
        extras025,
    )
    relecture(
        "TREE-AUT-025",
        "Les flaques de Nina près de la fontaine",
        "Fontaine, buis, bottes. Désir: flaques. Imprévu: pied nu, goutte sur l'orteil. "
        "T1 bac / toboggan / balançoires. T2 ballon / seau / doudou. "
        "T3 petite flaque / flaque du banc / grande flaque. "
        "Séquence vécue: botte, botte, une flaque, puis l'autre. Fin: bassin.",
        "Pas « une étape après l'autre ». Léa→Nina. T3 Tom/Léa/Sami → flaques. "
        "86 ids. Q=bottes. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins.",
    )


if __name__ == "__main__":
    main()
