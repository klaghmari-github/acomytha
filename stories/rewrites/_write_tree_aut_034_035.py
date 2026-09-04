#!/usr/bin/env python3
"""TREE-AUT-034 (N2 RAN implicite, prunier) et TREE-AUT-035 (N3 ROU vécue, radiateur)."""
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
        if kind in {"passage_question", "transition_question"}:
            scale, rate = 1.28, "slow"
        elif kind == "passage_fin":
            scale, rate = 1.26, "slow"
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
N3 = LIMITS["N3"]


# ---------------------------------------------------------------------------
# TREE-AUT-034 — Amir, prunier, escargot perdu sous feuilles et jouets
# T1 lieu  T2 jouet qui cache  T3 lumière
# ---------------------------------------------------------------------------

PLACE_034 = {
    1: {
        "lab": "la cuisine",
        "ou": "dans la cuisine",
        "tas": "Les jouets sont en tas, près du buffet.",
        "geste": "Amir touche une cuillère collante.",
        "fin": "Une goutte de confiture brille encore.",
        "son": "confiture",
    },
    2: {
        "lab": "le jardin",
        "ou": "sous le prunier",
        "tas": "Les jouets sont sous les feuilles mouillées.",
        "geste": "Amir écarte une feuille, tout doux.",
        "fin": "Le prunier penche, tout calme.",
        "son": "pluie",
    },
    3: {
        "lab": "la chambre",
        "ou": "dans la chambre",
        "tas": "Les jouets sont près des chaussons.",
        "geste": "Amir touche le rideau aux feuilles.",
        "fin": "Un pli du rideau bouge un peu.",
        "son": "rideau",
    },
}

TOY_034 = {
    1: {
        "lab": "les cubes",
        "take": "Amir soulève un cube jaune.",
        "feel": "Il est lisse, un peu froid.",
        "child": "Encore un cube.",
        "put": "La petite tour s'ouvre.",
        "find": "Sous le cube, l'escargot avance.",
        "fin": "Les cubes restent plus bas, tout sages.",
    },
    2: {
        "lab": "le livre",
        "take": "Amir soulève le livre, tout doux.",
        "feel": "La couverture est lisse, un peu froide.",
        "child": "Une page, maman.",
        "put": "Le livre s'écarte du tas.",
        "find": "Sous la page, l'escargot attend.",
        "fin": "Le livre reste ouvert, à côté.",
    },
    3: {
        "lab": "la dînette",
        "take": "Amir soulève la petite tasse.",
        "feel": "Elle est tiède, un peu collante.",
        "child": "La tasse, papa.",
        "put": "La tasse quitte le tas.",
        "find": "Sous l'assiette, l'escargot est là.",
        "fin": "La petite tasse reste vide, sage.",
    },
}

WHEN_034 = {
    1: {
        "lab": "le matin",
        "lum": "La lumière est pâle, un peu bleue.",
        "dehors": "Dehors, un oiseau chante une fois.",
        "extra": "L'air touche le nez, tout frais.",
        "fin": "La rosée brille encore sur la feuille.",
    },
    2: {
        "lab": "après la sieste",
        "lum": "Une bande d'ombre traverse le sol.",
        "dehors": "L'air de la maison est tiède.",
        "extra": "Amir a une joue un peu marquée.",
        "fin": "L'ombre a bougé d'un tout petit pas.",
    },
    3: {
        "lab": "le soir",
        "lum": "La lumière devient orange, toute douce.",
        "dehors": "Une première lampe s'allume au loin.",
        "extra": "L'air est plus frais sur les joues.",
        "fin": "La lampe fait un rond jaune au sol.",
    },
}

IMG_034 = {
    (1, 1, 1): "Un cube jaune a une miette de prune.",
    (1, 1, 2): "Les cubes sont tièdes, côté soleil.",
    (1, 1, 3): "Un cube a un peu de confiture au coin.",
    (1, 2, 1): "Une page du livre sent la prune.",
    (1, 2, 2): "Le bateau rouge dort près du buffet.",
    (1, 2, 3): "Une page du livre sent la confiture.",
    (1, 3, 1): "La petite tasse est encore un peu collante.",
    (1, 3, 2): "Une cuillère minuscule brille près du buffet.",
    (1, 3, 3): "La casserole de confiture ne chante plus.",
    (2, 1, 1): "Un cube a un grain de terre au coin.",
    (2, 1, 2): "L'escargot a avancé d'encore une feuille.",
    (2, 1, 3): "La pomme d'arrosoir s'est tue.",
    (2, 2, 1): "Une page sent l'herbe mouillée.",
    (2, 2, 2): "Le bateau rouge a une ombre de feuille.",
    (2, 2, 3): "Une pince à linge claque une fois, sur le fil.",
    (2, 3, 1): "La petite assiette a une goutte de rosée.",
    (2, 3, 2): "La tasse a pris un peu de soleil.",
    (2, 3, 3): "Le prunier penche au-dessus du chemin libre.",
    (3, 1, 1): "Un cube bleu touche le rayon du rideau.",
    (3, 1, 2): "Les cubes sont un peu chauds, sur le tapis.",
    (3, 1, 3): "La boîte de cubes se tait, près du lit.",
    (3, 2, 1): "Le livre a un pli du rideau dessus.",
    (3, 2, 2): "Une page sent l'oreiller, encore un peu.",
    (3, 2, 3): "Le livre reste sur la chaise, tout doux.",
    (3, 3, 1): "La petite tasse a un reflet de bouton.",
    (3, 3, 2): "Une chaussette a glissé près de la dînette.",
    (3, 3, 3): "La dînette rentre, et le rideau se tait.",
}

L1_034 = {
    1: vet(
        N2,
        [
            "narrateur|Amir pousse la porte de la cuisine.",
            "narrateur|Les carreaux sont froids sous les pieds.",
            "narrateur|Ça sent la confiture de prunes.",
            "narrateur|Une cuillère de bois est un peu collante.",
            "enfant-m|Ça sent les prunes, papa.",
            "papa|C'est la confiture.",
            "maman|L'escargot a suivi l'odeur ?",
            "narrateur|Amir cherche près du buffet.",
            "narrateur|Les jouets sont en tas, par terre.",
            "enfant-m|Il n'est plus là.",
            "papa|Sous le tas, peut-être.",
            "narrateur|Une mouche se pose sur la vitre.",
            "maman|On peut regarder dessous, tout doux.",
            "narrateur|Une goutte de confiture brille sur la cuillère.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Amir revient sous le prunier.",
            "narrateur|La terre est encore un peu molle.",
            "narrateur|La pomme d'arrosoir goutte encore.",
            "narrateur|Ploc, sur une pierre chaude.",
            "enfant-m|L'escargot est tout petit.",
            "papa|Il va tout lentement.",
            "maman|Tu le vois encore ?",
            "enfant-m|Non.",
            "narrateur|Les jouets sont sous les feuilles.",
            "narrateur|Une feuille mouillée cache le chemin.",
            "papa|Sous les feuilles, peut-être.",
            "narrateur|Une pince à linge claque une fois.",
            "maman|On peut regarder dessous, tout doux.",
            "narrateur|Le prunier penche encore, tout calme.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Amir entre dans la chambre.",
            "narrateur|Le rideau a des feuilles imprimées.",
            "narrateur|Un rayon passe entre deux plis.",
            "enfant-m|Comme le prunier, maman.",
            "maman|Oui, ce sont des dessins.",
            "papa|L'escargot est venu ici ?",
            "narrateur|Amir cherche près des chaussons.",
            "narrateur|Les jouets sont en tas, au sol.",
            "enfant-m|Pas lui.",
            "maman|Sous le tas, tout doux ?",
            "narrateur|L'oreiller est encore un peu tiède.",
            "papa|On regarde dessous, ensemble.",
            "narrateur|Un pli du rideau bouge un peu.",
        ],
    ),
}

C_034 = {
    1: vet(
        N2,
        [
            "narrateur|Amir écarte un cube, tout doux.",
            "narrateur|Toc.",
            "maman|Tu regardes dessous ?",
            "enfant-m|Pas encore, maman.",
            "papa|Encore un, tout doux.",
            "narrateur|Un bout de carreau reparaît.",
            "narrateur|La confiture brille encore.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Amir soulève une feuille mouillée.",
            "maman|Le chemin s'ouvre un peu.",
            "enfant-m|Toujours pas.",
            "papa|Sous une autre, peut-être.",
            "narrateur|La terre sombre reparaît.",
            "narrateur|L'arrosoir goutte encore, ploc.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|Amir pousse un cube vers le tapis.",
            "narrateur|Ça fait un petit bruit.",
            "maman|Le rayon bouge, tu vois ?",
            "enfant-m|Un peu, maman.",
            "papa|Encore un, près des chaussons.",
            "narrateur|Le fond du tapis reparaît, tout lent.",
            "narrateur|Le rideau reste calme.",
        ],
    ),
}

L2_034 = {
    1: vet(
        N2,
        [
            "narrateur|Les cubes de bois sont en tas.",
            "narrateur|Un cube jaune est lisse.",
            "narrateur|Un cube vert est un peu rêche.",
            "enfant-m|Les cubes, papa.",
            "papa|D'accord.",
            "narrateur|Amir pose une petite tour.",
            "narrateur|Clic.",
            "narrateur|Encore clic.",
            "maman|Tu joues un moment ?",
            "narrateur|La tour est petite, toute fière.",
            "papa|L'escargot est dessous, peut-être.",
            "enfant-m|Je vais voir.",
        ],
    ),
    2: vet(
        N2,
        [
            "narrateur|Le livre est ouvert, tout plat.",
            "narrateur|La couverture est lisse, un peu froide.",
            "narrateur|Les pages sentent le papier.",
            "enfant-m|Le livre, maman.",
            "papa|D'accord.",
            "narrateur|Amir tourne une page, tout doux.",
            "narrateur|Le papier chuchote.",
            "maman|Tu joues un moment ?",
            "narrateur|Sur la page, il y a un bateau rouge.",
            "papa|L'escargot est sous le livre ?",
            "enfant-m|Peut-être, papa.",
        ],
    ),
    3: vet(
        N2,
        [
            "narrateur|La dînette cliquette dans son panier.",
            "narrateur|Une petite assiette est blanche.",
            "narrateur|Une tasse est tiède.",
            "enfant-m|La dînette, papa.",
            "papa|D'accord.",
            "narrateur|Amir pose la tasse près de l'assiette.",
            "narrateur|Ting.",
            "maman|Tu joues un moment ?",
            "narrateur|Une cuillère minuscule brille.",
            "papa|L'escargot est sous l'assiette ?",
            "enfant-m|Je soulève, tout doux.",
        ],
    ),
}


def l3_body_034(i: int, j: int, k: int) -> list[str]:
    t = WHEN_034[k]
    p = PLACE_034[i]
    y = TOY_034[j]
    img = IMG_034[(i, j, k)]
    return vet(
        N2,
        [
            f"narrateur|{t['lum']}",
            f"narrateur|{p['tas']}",
            f"narrateur|{y['take']}",
            f"narrateur|{y['feel']}",
            f"enfant-m|{y['child']}",
            f"narrateur|{y['put']}",
            "narrateur|Le chemin s'ouvre, tout petit.",
            f"narrateur|{y['find']}",
            "enfant-m|L'escargot !",
            "maman|Te voilà, petit.",
            "papa|Merci, tu l'as trouvé.",
            f"narrateur|{img}",
            "narrateur|Amir se penche, tout calme.",
            f"narrateur|{t['dehors']}",
        ],
    )


def l3_fin_034(i: int, j: int, k: int) -> list[str]:
    t = WHEN_034[k]
    p = PLACE_034[i]
    y = TOY_034[j]
    img = IMG_034[(i, j, k)]
    starts = [
        "L'escargot a le nez sur la feuille.",
        "Amir tient la feuille, tout calme.",
        "Contre la terre, l'escargot avance.",
        "Au chaud, la coquille brille un peu.",
        "Près du tas, Amir respire.",
        "Sous la lampe, la coquille brille.",
        "Dans l'herbe, l'escargot est trouvé.",
        "Enfin la coquille est là, tout douce.",
        "Voilà l'escargot, sur la feuille.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return vet(
        N2,
        [
            f"narrateur|{first}",
            f"narrateur|{y['fin']}",
            "enfant-m|Il avance encore, papa.",
            "papa|Oui, il est bien là.",
            "maman|Le chemin est libre, maintenant.",
            "papa|Bravo, Amir.",
            f"narrateur|{p['fin']}",
            f"narrateur|{img}",
            f"narrateur|{t['fin']}",
            "narrateur|La feuille brille encore, tout doux.",
        ],
    )


def build_034() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N2,
        [
            "narrateur|Un prunier penche au fond du jardin.",
            "narrateur|Une feuille brille, encore mouillée.",
            "narrateur|Un escargot avance dessus, tout lent.",
            "narrateur|La pomme d'arrosoir goutte.",
            "narrateur|Ploc, sur la terre sombre.",
            "narrateur|Des pinces à linge dansent sur le fil.",
            "narrateur|Un torchon rayé sèche, tout léger.",
            "narrateur|Papa pose les bottes près de la porte.",
            "narrateur|Maman accroche encore une pince.",
            "maman|Tu as vu l'escargot, Amir ?",
            "enfant-m|Oui.",
            "enfant-m|Il est tout petit.",
            "papa|Il va vers l'herbe, tout doux.",
            "narrateur|En ce moment, Amir se penche.",
            "narrateur|La feuille est froide, un peu rêche.",
            "enfant-m|Je veux le suivre !",
            "maman|D'accord.",
            "maman|On reste près de lui.",
            "narrateur|Amir sort les jouets de la caisse.",
            "narrateur|Les cubes, le livre, la dînette.",
            "narrateur|Une feuille tombe dessus.",
            "narrateur|Puis une autre.",
            "enfant-m|Il a disparu !",
            "papa|Sous les feuilles, peut-être.",
            "narrateur|Le prunier cache encore un bout de ciel.",
        ],
    )
    sons["CHK_T0000_P0000"] = "pluie,arrosoir"

    s["CHK_T0001_P0000"] = vet(
        N2,
        [
            "papa|Où le cherche-t-on, Amir ?",
            "narrateur|La cuisine.",
            "narrateur|Le jardin.",
            "narrateur|La chambre.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("la cuisine", "le jardin", "la chambre")

    q_lines = vet(
        N2,
        [
            "narrateur|Amir cherche l'escargot.",
            "maman|Il est où ?",
        ],
    )
    t2_lines = vet(
        N2,
        [
            "papa|Quel jouet tu soulèves, Amir ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|La dînette.",
        ],
    )
    t3_lines = vet(
        N2,
        [
            "maman|On cherche à quelle heure ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ],
    )

    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1_034[i]
        sons[p] = PLACE_034[i]["son"]
        s[f"{p}_Q0001"] = q_lines
        extras[f"{p}_Q0001"] = qf(
            "escargot",
            "escargot | l'escargot | sous les feuilles | sous les jouets | dessous | sous le tas",
            "Il cherche sous les feuilles. Où est l'escargot ?",
        )
        s[f"{p}_C0001"] = C_034[i]
        s[f"{p}_T0002_P0000"] = t2_lines
        extras[f"{p}_T0002_P0000"] = t3("les cubes", "le livre", "la dînette")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2_034[j] + vet(
                N2,
                [
                    f"narrateur|{PLACE_034[i]['geste']}",
                    f"narrateur|{PLACE_034[i]['tas']}",
                ],
            )
            s[f"{p2}_T0003_P0000"] = t3_lines
            extras[f"{p2}_T0003_P0000"] = t3("le matin", "après la sieste", "le soir")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = l3_body_034(i, j, k)
                s[f"{p3}_F0001"] = l3_fin_034(i, j, k)
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-035 — Nina, fil d'argent, radiateur, séquence vécue
# T1 jeu de cour  T2 objet  T3 suite du matin (plus Tom/Léa/Sami)
# ---------------------------------------------------------------------------

L1_035 = {
    1: {"lab": "le bac à sable", "ou": "près du bac à sable", "son": "sable"},
    2: {"lab": "le toboggan", "ou": "près du toboggan", "son": "toboggan"},
    3: {"lab": "les balançoires", "ou": "près des balançoires", "son": "balancoire"},
}

L2_035 = {
    1: {"lab": "le ballon", "un": "le ballon rouge"},
    2: {"lab": "le seau", "un": "le seau bleu"},
    3: {"lab": "le doudou", "un": "le doudou beige"},
}

L3_035 = {
    1: {"lab": "le préau", "ou": "sous le préau"},
    2: {"lab": "la fontaine", "ou": "près de la fontaine"},
    3: {"lab": "le cartable", "ou": "près du cartable"},
}

ARRIVE_035 = {
    1: vet(
        N3,
        [
            "narrateur|Nina revient vers le vestiaire.",
            "narrateur|Les crochets sont froids.",
            "narrateur|Le radiateur fait tic, tout bas.",
            "enfant-f|J'ai froid aux doigts.",
            "maman|Pose les mains, un moment.",
            "narrateur|Nina pose les paumes sur le métal.",
            "narrateur|Ses doigts deviennent roses.",
            "papa|Ton gant rouge est tombé ici.",
            "narrateur|Elle le ramasse, tout près.",
            "narrateur|Elle accroche le manteau.",
            "enfant-f|Maintenant la cour.",
            "maman|Oui, tes mains sont tièdes.",
            "narrateur|Nina s'agenouille près du bac.",
            "narrateur|Le sable est frais, un peu humide.",
            "narrateur|Une petite pelle jaune attend.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Nina s'arrête au vestiaire, un instant.",
            "narrateur|Le radiateur ronronne, tout bas.",
            "enfant-f|Mes doigts sont froids, papa.",
            "papa|Le métal est tiède, tu sens ?",
            "narrateur|Elle pose les mains dessus.",
            "narrateur|Le gant rouge attend contre le mur.",
            "maman|Tu l'as retrouvé ?",
            "enfant-f|Oui.",
            "narrateur|Elle accroche le manteau, tout lourd.",
            "narrateur|Les boutons tapent le crochet.",
            "papa|Tu es prête, maintenant ?",
            "enfant-f|Le toboggan !",
            "narrateur|Nina pose un pied sur la première marche.",
            "narrateur|Le plastique jaune brille, encore mouillé.",
            "narrateur|Une goutte pend sous le rebord.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Nina passe d'abord près du radiateur.",
            "narrateur|Il fait tic, contre le mur.",
            "maman|Tes mains, un moment.",
            "narrateur|Les paumes se réchauffent, tout doux.",
            "papa|L'autre gant rouge est là.",
            "narrateur|La paire se retrouve, enfin.",
            "enfant-f|Ils sont chauds.",
            "maman|Le manteau au crochet ?",
            "narrateur|Nina l'accroche, tout calme.",
            "papa|On peut aller aux balançoires.",
            "narrateur|Les chaînes font un petit cling.",
            "narrateur|Le siège en bois est encore frais.",
            "enfant-f|Je m'assois.",
            "narrateur|Elle pose les deux mains dessus.",
            "narrateur|La cour sent l'herbe mouillée.",
        ],
    ),
}

Q_035 = {
    1: vet(
        N3,
        [
            "narrateur|Nina a les doigts froids, près du bac.",
            "maman|Elle a posé les mains où ?",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|Nina a les doigts froids, près du toboggan.",
            "papa|Elle a posé les mains où ?",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Nina a les doigts froids, près des chaînes.",
            "maman|Elle a posé les mains où ?",
        ],
    ),
}

C_035 = {
    1: vet(
        N3,
        [
            "papa|Oui.",
            "papa|Sur le radiateur, tout doux.",
            "maman|Ton gant est retrouvé.",
            "enfant-f|Mes doigts sont roses.",
            "papa|On peut jouer, maintenant.",
            "narrateur|Un grain de sable brille sur son genou.",
            "narrateur|La pelle jaune attend encore.",
        ],
    ),
    2: vet(
        N3,
        [
            "maman|Oui.",
            "maman|Sur le radiateur, tout tiède.",
            "papa|Le manteau est au crochet.",
            "enfant-f|Je n'ai plus froid.",
            "maman|On continue, avec nous.",
            "narrateur|La goutte sous le rebord tombe, plic.",
            "narrateur|Le plastique jaune est un peu tiède.",
        ],
    ),
    3: vet(
        N3,
        [
            "papa|Oui.",
            "papa|Les mains sur le radiateur.",
            "maman|La paire de gants est complète.",
            "enfant-f|Ils sont chauds.",
            "papa|Les chaînes peuvent bouger, tout doux.",
            "narrateur|Une ombre d'oiseau passe dessus.",
            "narrateur|Le bois du siège reste frais.",
        ],
    ),
}

PLAY_035 = {
    (1, 1): vet(
        N3,
        [
            "narrateur|Nina est encore près du bac à sable.",
            "narrateur|Le ballon rouge attend dans l'herbe courte.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, papa.",
            "papa|D'accord.",
            "narrateur|Nina pose les deux mains dessus.",
            "narrateur|Le ballon fait un petit bruit de peau.",
            "maman|Tu le tiens bien ?",
            "enfant-f|Oui.",
            "narrateur|Un grain de sable colle au ballon.",
            "papa|Il reste avec toi ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    (1, 2): vet(
        N3,
        [
            "narrateur|Nina est encore près du bac à sable.",
            "narrateur|Le seau bleu a une anse qui brille.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau, maman.",
            "maman|D'accord.",
            "narrateur|Nina prend l'anse.",
            "narrateur|Ting.",
            "papa|Le seau est vide, léger.",
            "narrateur|Elle le pose tout doux, près du sable.",
            "maman|Tu remplis un peu ?",
            "enfant-f|Oui, un peu.",
            "narrateur|Le sable coule, chh.",
        ],
    ),
    (1, 3): vet(
        N3,
        [
            "narrateur|Nina est encore près du bac à sable.",
            "narrateur|Le doudou beige attend sur le banc.",
            "narrateur|Une oreille est un peu pliée.",
            "enfant-f|Le doudou, maman.",
            "maman|D'accord.",
            "narrateur|Nina prend le doudou.",
            "narrateur|Il sent le lit.",
            "papa|Tu le poses près de nous ?",
            "enfant-f|Oui.",
            "enfant-f|Il attend.",
            "narrateur|Le tissu est doux, un peu chaud.",
            "narrateur|Un grain de sable reste sur l'oreille.",
        ],
    ),
    (2, 1): vet(
        N3,
        [
            "narrateur|Nina est encore près du toboggan.",
            "narrateur|Le ballon rouge attend dans l'herbe courte.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, papa.",
            "papa|D'accord.",
            "narrateur|Nina le tient contre son manteau.",
            "narrateur|Le ballon fait un petit bruit de peau.",
            "maman|Tu as fini de le tenir ?",
            "enfant-f|Oui.",
            "narrateur|Le ballon reste au pied de la rampe.",
            "papa|Il ne roule pas trop ?",
            "enfant-f|Non, papa.",
        ],
    ),
    (2, 2): vet(
        N3,
        [
            "narrateur|Nina est encore près du toboggan.",
            "narrateur|Le seau bleu a une anse qui brille.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau, maman.",
            "maman|D'accord.",
            "narrateur|Nina prend l'anse.",
            "narrateur|Ting.",
            "papa|Le seau est à sa place ?",
            "enfant-f|Oui, papa.",
            "narrateur|Elle le pose au pied des marches.",
            "maman|Il attend, tout calme.",
            "narrateur|Un oiseau crie une fois, tout haut.",
        ],
    ),
    (2, 3): vet(
        N3,
        [
            "narrateur|Nina est encore près du toboggan.",
            "narrateur|Le doudou beige attend sur le banc du préau.",
            "narrateur|Une oreille est un peu pliée.",
            "enfant-f|Le doudou, maman.",
            "maman|D'accord.",
            "narrateur|Nina le pose près de la rampe.",
            "narrateur|Le tissu est doux, un peu chaud.",
            "papa|Il est bien, là ?",
            "enfant-f|Oui.",
            "enfant-f|Il attend.",
            "narrateur|Le doudou garde l'oreille pliée.",
            "narrateur|Le plastique jaune reste un peu mouillé.",
        ],
    ),
    (3, 1): vet(
        N3,
        [
            "narrateur|Nina est encore près des balançoires.",
            "narrateur|Le ballon rouge attend dans l'herbe courte.",
            "narrateur|Il est lisse, un peu frais.",
            "enfant-f|Le ballon, papa.",
            "papa|D'accord.",
            "narrateur|Nina le pose entre deux chaînes.",
            "narrateur|Le ballon fait un petit bruit de peau.",
            "maman|Il reste là ?",
            "enfant-f|Oui.",
            "narrateur|Les chaînes font cling, tout doux.",
            "papa|Tu le regardes, en te balançant ?",
            "enfant-f|Un peu, papa.",
        ],
    ),
    (3, 2): vet(
        N3,
        [
            "narrateur|Nina est encore près des balançoires.",
            "narrateur|Le seau bleu a une anse qui brille.",
            "narrateur|L'anse est un peu froide.",
            "enfant-f|Le seau, maman.",
            "maman|D'accord.",
            "narrateur|Nina pose le seau sous le siège.",
            "narrateur|Ting.",
            "papa|Il est à sa place ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le seau reste vide, tout sage.",
            "maman|On se balance, tout doux.",
            "narrateur|Une ombre d'oiseau passe encore.",
        ],
    ),
    (3, 3): vet(
        N3,
        [
            "narrateur|Nina est encore près des balançoires.",
            "narrateur|Le doudou beige attend sur le banc.",
            "narrateur|Une oreille est un peu pliée.",
            "enfant-f|Le doudou, maman.",
            "maman|D'accord.",
            "narrateur|Nina l'assoit sur le bois frais.",
            "narrateur|Le tissu est doux, un peu chaud.",
            "papa|Il est bien, là ?",
            "enfant-f|Oui.",
            "enfant-f|Il attend.",
            "narrateur|Le doudou garde l'oreille pliée.",
            "narrateur|Les chaînes se taisent un moment.",
        ],
    ),
}

HOLD_035 = {
    1: "Le ballon rouge vient avec elle.",
    2: "Le seau bleu vient avec elle.",
    3: "Le doudou beige vient avec elle.",
}

DEST_035 = {
    1: vet(
        N3,
        [
            "narrateur|Sous le préau, des piliers en bois clair attendent.",
            "narrateur|Le sol dessous est sec, enfin.",
            "papa|On s'assoit, un moment.",
            "enfant-f|J'y vais.",
            "narrateur|Nina marche jusqu'au pilier.",
            "narrateur|Ses bottes font toc toc, plus sourd.",
            "narrateur|Elle s'assoit.",
            "narrateur|Le bois est lisse.",
            "maman|Tu as faim, un peu ?",
            "enfant-f|Oui.",
            "enfant-f|Un petit bout.",
            "narrateur|Maman sort un morceau de pomme.",
            "narrateur|La pomme est froide, un peu sucrée.",
        ],
    ),
    2: vet(
        N3,
        [
            "narrateur|La fontaine de la cour est en pierre grise.",
            "narrateur|Une goutte pend, puis tombe.",
            "narrateur|Plic.",
            "maman|Les mains, tout doux.",
            "enfant-f|J'y vais.",
            "narrateur|Nina va jusqu'à la pierre.",
            "narrateur|L'eau est froide sur ses doigts.",
            "narrateur|Elle essuie ses mains sur son manteau.",
            "papa|Tes mains sont propres ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Elles sont froides.",
            "narrateur|Papa tend un coin de mouchoir.",
            "narrateur|Le mouchoir sent le savon.",
        ],
    ),
    3: vet(
        N3,
        [
            "narrateur|Le cartable bleu attend près du vestiaire.",
            "narrateur|La boucle est un peu froide.",
            "papa|On ouvre, tout doux.",
            "enfant-f|J'ouvre.",
            "narrateur|Nina ouvre la boucle.",
            "narrateur|Clic.",
            "narrateur|Un dessin à la craie est plié dedans.",
            "narrateur|Elle le pousse tout doux, au fond.",
            "maman|Tu refermes ?",
            "enfant-f|Oui.",
            "narrateur|Clic.",
            "narrateur|Le cartable est fermé, un peu lourd.",
            "narrateur|Le gant rouge a retrouvé sa paire.",
        ],
    ),
}

OBJ_MARK_035 = {
    (1, 1): "Un grain de sable colle au ballon, sous le préau.",
    (1, 2): "Le ballon a une goutte de fontaine dessus.",
    (1, 3): "Le ballon appuie contre le cartable bleu.",
    (2, 1): "Le seau résonne un peu, sous le préau.",
    (2, 2): "Une goutte de fontaine tombe dans le seau.",
    (2, 3): "Le seau se pose à côté du cartable.",
    (3, 1): "Le doudou sent le bois sec du préau.",
    (3, 2): "Le doudou a une goutte sur l'oreille.",
    (3, 3): "Le doudou glisse contre le cartable.",
}

IMG_035 = {
    (1, 1, 1): "Le préau sent encore le bois mouillé.",
    (1, 1, 2): "Une autre goutte tombe, toute seule.",
    (1, 1, 3): "Le vestiaire sent la laine mouillée.",
    (1, 2, 1): "Le seau garde une ombre de pilier.",
    (1, 2, 2): "Le seau a pris une goutte, plic.",
    (1, 2, 3): "Le seau veille près de la boucle.",
    (1, 3, 1): "Le doudou s'adosse au bois clair.",
    (1, 3, 2): "L'oreille du doudou reste un peu mouillée.",
    (1, 3, 3): "Le doudou veille près du dessin plié.",
    (2, 1, 1): "Le ballon roule jusqu'au pilier du préau.",
    (2, 1, 2): "Le ballon tremble un peu, près de l'eau.",
    (2, 1, 3): "Le ballon attend contre le cartable fermé.",
    (2, 2, 1): "Le seau fait ting, sous le bois du préau.",
    (2, 2, 2): "Le seau reçoit une goutte, plic.",
    (2, 2, 3): "Le seau bleu garde le dessin au chaud.",
    (2, 3, 1): "Le doudou s'adosse au pilier, tout calme.",
    (2, 3, 2): "Le doudou écoute la goutte, plic.",
    (2, 3, 3): "Le doudou veille près de la boucle.",
    (3, 1, 1): "Le ballon se pose au sec, sous le bois.",
    (3, 1, 2): "Le ballon a une goutte sur le flanc.",
    (3, 1, 3): "Le ballon attend près du crochet.",
    (3, 2, 1): "Le seau sonne plus sourd, sous le préau.",
    (3, 2, 2): "L'anse du seau est froide, près de l'eau.",
    (3, 2, 3): "Le seau tapote la boucle, tout doux.",
    (3, 3, 1): "Le doudou sent le bois sec, enfin.",
    (3, 3, 2): "Le doudou a une goutte sur le ventre.",
    (3, 3, 3): "Le doudou glisse contre la laine du manteau.",
}

CLOSE_035 = {
    1: "Le préau sent encore le bois mouillé.",
    2: "Une goutte tombe encore, toute seule.",
    3: "Le cartable bleu est fermé, calme.",
}


def body_035(i: int, j: int, k: int) -> list[str]:
    loc = L1_035[i]
    lines = [
        f"narrateur|Nina est encore {loc['ou']}.",
        f"narrateur|{HOLD_035[j]}",
        f"narrateur|{OBJ_MARK_035[(j, k)]}",
    ]
    lines.extend(DEST_035[k])
    lines.append("papa|Merci, Nina.")
    lines.append(f"narrateur|{IMG_035[(i, j, k)]}")
    return vet(N3, lines)


def fin_035(i: int, j: int, k: int) -> list[str]:
    loc = L1_035[i]
    obj = L2_035[j]
    dest = L3_035[k]
    starts = [
        "Nina a les doigts encore un peu roses.",
        "Le fil d'argent brille encore sur la vitre.",
        "Contre le mur, le radiateur fait tic.",
        "Au vestiaire, le manteau pèse, tout calme.",
        "Près de la flaque, le ciel est tout petit.",
        "Sous le préau, le bois reste sec.",
        "Dans la cour, l'herbe sent encore la pluie.",
        "Enfin le gant rouge a sa paire.",
        "Voilà les mains tièdes, contre le métal.",
    ]
    first = starts[(i * 9 + j * 3 + k) % len(starts)]
    return vet(
        N3,
        [
            f"narrateur|{first}",
            f"narrateur|Nina est passée {loc['ou']}.",
            f"narrateur|Elle a pris {obj['lab']}.",
            f"narrateur|Puis {dest['lab']}.",
            "enfant-f|J'ai le gant.",
            "enfant-f|J'ai les mains tièdes.",
            "maman|On peut rentrer, tout doux.",
            "papa|Bravo, Nina.",
            f"narrateur|{CLOSE_035[k]}",
            f"narrateur|{IMG_035[(i, j, k)]}",
            "narrateur|Le radiateur fait encore tic, tout bas.",
        ],
    )


def build_035() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        N3,
        [
            "narrateur|Un fil d'argent traverse la vitre de l'école.",
            "narrateur|Il brille, tout mince, tout lent.",
            "narrateur|La vitre est encore un peu grise.",
            "narrateur|Dans la cour, une flaque ronde attend.",
            "narrateur|Elle tient un morceau de ciel.",
            "narrateur|Le préau goutte, tout doux, sur le bois.",
            "narrateur|Les manteaux pendent, lourds, au vestiaire.",
            "narrateur|Un gant rouge a perdu sa paire.",
            "narrateur|Le radiateur fait tic, contre le mur.",
            "narrateur|Il est tiède, tout bas.",
            "narrateur|Papa essuie une botte, sans bruit.",
            "narrateur|Maman ouvre le petit cartable bleu.",
            "maman|Tu as vu le fil, Nina ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Il brille.",
            "papa|Le radiateur est tiède.",
            "papa|Tu le sens ?",
            "narrateur|En ce moment, Nina pose les mains dessus.",
            "narrateur|Ses doigts deviennent un peu roses.",
            "enfant-f|Je veux déjà la cour !",
            "maman|D'accord.",
            "narrateur|Nina court vers la porte.",
            "narrateur|Son manteau reste ouvert.",
            "narrateur|Un gant tombe près du radiateur.",
            "enfant-f|J'ai froid aux doigts.",
            "papa|Le gant est resté derrière.",
            "narrateur|Le fil d'argent attend encore sur la vitre.",
        ],
    )
    sons["CHK_T0000_P0000"] = "radiateur,goutte"

    s["CHK_T0001_P0000"] = vet(
        N3,
        [
            "narrateur|Ils arrivent dans la cour.",
            "papa|On commence où, Nina ?",
            "narrateur|Le bac à sable.",
            "narrateur|Le toboggan.",
            "narrateur|Les balançoires.",
        ],
    )
    extras["CHK_T0001_P0000"] = t3("le bac à sable", "le toboggan", "les balançoires")

    q_extra = qf(
        "radiateur",
        "radiateur | le radiateur | vestiaire | le vestiaire | le gant | manteau | le manteau | les mains",
        "Le métal est tiède. Elle a posé les mains où ?",
    )

    for i, loc in L1_035.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_035[i]
        sons[p] = loc["son"]
        s[f"{p}_Q0001"] = Q_035[i]
        extras[f"{p}_Q0001"] = q_extra
        s[f"{p}_C0001"] = C_035[i]
        s[f"{p}_T0002_P0000"] = vet(
            N3,
            [
                f"narrateur|{loc['ou'].capitalize()}, Nina prend un objet.",
                "papa|Le ballon, le seau, ou le doudou ?",
                "maman|Tu choisis.",
            ],
        )
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_035[(i, j)]
            s[f"{p2}_T0003_P0000"] = vet(
                N3,
                [
                    f"narrateur|Nina a {L2_035[j]['lab']}, {loc['ou']}.",
                    "maman|Le matin continue où ?",
                    "papa|Le préau, la fontaine, ou le cartable ?",
                ],
            )
            extras[f"{p2}_T0003_P0000"] = t3("le préau", "la fontaine", "le cartable")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_035(i, j, k)
                s[f"{p3}_F0001"] = fin_035(i, j, k)
    return s, sons, extras


def main() -> None:
    s34, n34, e34 = build_034()
    write_tree(
        "TREE-AUT-034",
        "Amir veut suivre l'escargot sous le prunier. "
        "Les jouets et les feuilles cachent le chemin. "
        "Il ne le retrouve qu'en soulevant cubes, livre ou dînette.",
        "L'escargot sous le prunier",
        "Amir, papa, maman",
        "jardin, prunier, arrosoir, pinces à linge",
        s34,
        n34,
        e34,
    )
    relecture(
        "TREE-AUT-034",
        "L'escargot sous le prunier",
        "Prunier, feuille mouillée, escargot, arrosoir. "
        "Désir: suivre l'escargot. Imprévu: jouets et feuilles sur le chemin. "
        "T1 cuisine / jardin / chambre. T2 cubes / livre / dînette. "
        "T3 matin / sieste / soir. Il soulève, le chemin s'ouvre, l'escargot est là.",
        "Kenzo→Amir (D16). N2. AUT.RAN.001 implicite. "
        "Pas « on va ranger » / « après le jeu ». Q=escargot. "
        "86 ids. Relu ouverture + 3 L1 + 3 L2 + 27 L3/fins (images uniques). "
        "Monde ≠ TREE-AUT-012 (train, doudou).",
    )

    s35, n35, e35 = build_035()
    write_tree(
        "TREE-AUT-035",
        "Nina veut déjà la cour. Un fil d'argent traverse la vitre. "
        "Elle court, le manteau ouvert, un gant tombe près du radiateur. "
        "Les mains se réchauffent, le gant revient, puis la cour. "
        "Préau, fontaine ou cartable : la suite change.",
        "Le fil d'argent et le radiateur de Nina",
        "Nina, papa, maman",
        "école, vitre, vestiaire, radiateur, cour",
        s35,
        n35,
        e35,
    )
    relecture(
        "TREE-AUT-035",
        "Le fil d'argent et le radiateur de Nina",
        "École, fil d'argent, flaque, gant rouge, radiateur tic. "
        "Désir: la cour. Imprévu: manteau ouvert, gant tombé, doigts froids. "
        "T1 bac / toboggan / balançoires. T2 ballon / seau / doudou. "
        "T3 préau / fontaine / cartable (plus Tom/Léa/Sami). "
        "Séquence vécue: vestiaire et radiateur, puis le jeu.",
        "Lina→Nina (D16). N3. AUT.ROU.001 implicite. "
        "Pas « une étape après l'autre ». Q=radiateur. "
        "86 ids. Relu ouverture + 3 L1 + 9 L2 + 27 L3/fins. "
        "Monde ≠ TREE-AUT-013 (mer, carré d'or), ≠ TREE-AUT-016 (laine, bottes).",
    )


if __name__ == "__main__":
    main()
