#!/usr/bin/env python3
"""TREE-AUT-046 / TREE-AUT-047 — récit implicite, graphe 86, D16, N2."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

N2 = 15


def ln(*xs: str) -> list[str]:
    out = []
    for x in xs:
        role, ph = x.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


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
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "ce que l'adulte",
        "ce que maman a dit",
        "ce que papa a dit",
        "tes affaires",
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
    ):
        if bad in blob:
            raise SystemExit(f"{sid} slogan: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} {c['chunk_id']} fin mécanique: {last}")
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def assemble(debut, t1q, l1, q, c, t2q, l2, t3q, l3, fin) -> dict[str, list[str]]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": debut,
        "CHK_T0001_P0000": t1q,
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = l1[i]
        s[f"{p}_Q0001"] = q[i]
        s[f"{p}_C0001"] = c[i]
        s[f"{p}_T0002_P0000"] = t2q[i] if isinstance(t2q, dict) else t2q
        for j in (1, 2, 3):
            s[f"{p}_T0002_P000{j}"] = l2[i][j]
            s[f"{p}_T0002_P000{j}_T0003_P0000"] = (
                t3q[j] if isinstance(t3q, dict) else t3q
            )
            for k in (1, 2, 3):
                s[f"{p}_T0002_P000{j}_T0003_P000{k}"] = l3(i, j, k)
                s[f"{p}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin(i, j, k)
    return s


# ---------------------------------------------------------------------------
# TREE-AUT-046  N2  Victorino  AUT.AFF.001
# Sac jaune sur le banc. Camp près de l'escargot. Pas une packing-list.
# ≠ TREE-AUT-009 (sac bleu, crochet, doudou, four).
# ≠ TREE-COL-001 (pommes, train, voyage).
# T1 pomme / yaourt / pain : le goûter du camp, choisi par lui.
# ---------------------------------------------------------------------------

FOOD_046 = {
    1: {"lab": "une pomme", "le": "la pomme", "son": "pomme"},
    2: {"lab": "un yaourt", "le": "le yaourt", "son": "pot"},
    3: {"lab": "un morceau de pain", "le": "le pain", "son": "pain"},
}
LIEU_046 = {
    1: {"lab": "la cuisine", "ou": "dans la cuisine", "son": "evier"},
    2: {"lab": "le jardin", "ou": "dans le jardin", "son": "arrosoir"},
    3: {"lab": "la chambre", "ou": "dans la chambre", "son": "rideau"},
}
JEU_046 = {
    1: {"lab": "les cubes", "un": "un cube"},
    2: {"lab": "le livre", "un": "le livre"},
    3: {"lab": "la dînette", "un": "une tasse"},
}

DEBUT_046 = ln(
    "narrateur|Une goutte tombe de l'arrosoir.",
    "narrateur|Elle brille sur une feuille de laitue.",
    "narrateur|Un escargot avance, tout doux.",
    "narrateur|Sa coquille est brune et lisse.",
    "narrateur|Le banc du jardin est en bois clair.",
    "narrateur|Le sac jaune de Victorino est posé dessus.",
    "narrateur|La sangle est un peu rêche.",
    "narrateur|Papa râcle une petite allée.",
    "narrateur|Ça fait un bruit de graviers.",
    "narrateur|Maman pose des pinces à linge.",
    "maman|Tu as vu l'escargot, Victorino ?",
    "enfant-m|Oui, maman.",
    "enfant-m|Il avance.",
    "papa|Il va vers la laitue.",
    "narrateur|En ce moment, Victorino touche le sac.",
    "narrateur|Le sac est encore vide.",
    "narrateur|Le tissu est un peu froid du matin.",
    "enfant-m|Je veux un camp, près de lui !",
    "enfant-m|Pour le regarder.",
    "maman|D'accord.",
    "narrateur|Victorino soulève le sac.",
    "narrateur|Il retombe, tout mou.",
    "enfant-m|Il n'y a rien dedans.",
    "papa|Tu auras faim, après ?",
    "enfant-m|Oui.",
    "papa|On glisse un goûter, alors ?",
)

T1Q_046 = ln(
    "papa|Tu glisses quoi, pour le camp ?",
    "narrateur|Une pomme.",
    "narrateur|Un yaourt.",
    "narrateur|Ou un morceau de pain.",
)

L1_046 = {
    1: ln(
        "narrateur|Victorino prend une pomme sur le banc.",
        "narrateur|Un reflet vert danse dessus.",
        "narrateur|Elle est lisse, un peu froide de la rosée.",
        "enfant-m|Elle brille, maman.",
        "maman|Oui.",
        "maman|Elle est encore fraîche.",
        "papa|Tu la portes à la main ?",
        "narrateur|La pomme glisse entre ses doigts.",
        "enfant-m|Oh.",
        "enfant-m|Elle va tomber.",
        "maman|Le sac est juste là.",
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Il glisse la pomme au fond.",
        "narrateur|Elle fait un petit choc.",
        "enfant-m|Elle est dedans.",
        "papa|Le sac a un rond, maintenant.",
        "narrateur|La sangle tient mieux, un peu lourde.",
        "narrateur|L'escargot n'a presque pas bougé.",
    ),
    2: ln(
        "narrateur|Victorino prend un yaourt près des pinces.",
        "narrateur|Le couvercle blanc brille au soleil.",
        "narrateur|Le pot est froid et un peu humide.",
        "enfant-m|Il glisse, papa.",
        "papa|Oui.",
        "papa|Le couvercle est mouillé.",
        "maman|Tu le serres fort ?",
        "narrateur|Le pot fait un petit toc sur le bois.",
        "enfant-m|Il va rouler.",
        "papa|Le sac l'attend, sur le banc.",
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Il glisse le pot au fond.",
        "narrateur|Le tissu se tend un peu.",
        "enfant-m|Il est dedans.",
        "maman|Le sac a un rond froid, maintenant.",
        "narrateur|Un peu d'eau reste sur le bois.",
        "narrateur|L'abeille passe, puis s'en va.",
    ),
    3: ln(
        "narrateur|Victorino prend un morceau de pain.",
        "narrateur|Ça sent le four, même dans le jardin.",
        "narrateur|Le pain est encore un peu tiède.",
        "enfant-m|Il est chaud, maman.",
        "maman|Oui.",
        "maman|Il vient du village.",
        "papa|Le papier veut s'envoler.",
        "narrateur|Le vent soulève un coin blanc.",
        "enfant-m|Oh.",
        "enfant-m|Il part.",
        "maman|Glisse-le, dans le sac.",
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Le papier froisse, tout doux.",
        "narrateur|Le pain disparaît au fond.",
        "enfant-m|Il est à l'abri.",
        "papa|Le sac sent le four, maintenant.",
        "narrateur|La sangle est un peu plus lourde.",
        "narrateur|L'arrosoir goutte encore, tout bas.",
    ),
}

Q_046 = {
    1: ln(
        "narrateur|La pomme n'est plus sur le banc.",
        "papa|Victorino l'a mise où ?",
    ),
    2: ln(
        "narrateur|Le pot froid n'est plus sur le bois.",
        "maman|Victorino l'a mis où ?",
    ),
    3: ln(
        "narrateur|Le pain n'est plus près de l'arrosoir.",
        "papa|Victorino l'a mis où ?",
    ),
}

C_046 = {
    1: ln(
        "narrateur|Oui.",
        "narrateur|La pomme est dans le sac jaune.",
        "papa|Merci, Victorino.",
        "enfant-m|Le camp, maintenant.",
        "maman|On choisit l'endroit ?",
        "narrateur|La sangle frotte un peu l'épaule.",
        "narrateur|L'escargot avance d'un cran.",
    ),
    2: ln(
        "narrateur|Oui.",
        "narrateur|Le yaourt est dans le sac jaune.",
        "maman|Merci, Victorino.",
        "enfant-m|Le camp, maintenant.",
        "papa|On choisit l'endroit ?",
        "narrateur|Le pot laisse un rond d'eau, au fond.",
        "narrateur|Une pince à linge brille encore.",
    ),
    3: ln(
        "narrateur|Oui.",
        "narrateur|Le pain est dans le sac jaune.",
        "papa|Merci, Victorino.",
        "enfant-m|Le camp, maintenant.",
        "maman|On choisit l'endroit ?",
        "narrateur|Le papier ne s'envole plus.",
        "narrateur|Ça sent encore le four, tout bas.",
    ),
}

T2Q_046 = ln(
    "maman|Le camp, c'est où ?",
    "narrateur|La cuisine.",
    "narrateur|Le jardin.",
    "narrateur|Ou la chambre.",
)

L2_046 = {
    1: {
        1: ln(
            "narrateur|Victorino porte le sac vers la cuisine.",
            "narrateur|Le carrelage est un peu froid.",
            "narrateur|Un bol bleu attend sur la table.",
            "enfant-m|Le camp, sous la table.",
            "papa|D'accord.",
            "papa|On se glisse là.",
            "narrateur|Il pose le sac jaune à côté du bol.",
            "narrateur|La pomme fait un petit choc, au fond.",
            "maman|Tu as ton goûter avec toi.",
            "enfant-m|Oui.",
            "enfant-m|Elle est au chaud.",
            "narrateur|Un robinet goutte, tout loin.",
            "narrateur|Le torchon de l'évier ne bouge plus.",
        ),
        2: ln(
            "narrateur|Victorino repose le sac sur le banc.",
            "narrateur|L'herbe est encore humide sous les chaussures.",
            "narrateur|L'escargot est tout près de la laitue.",
            "enfant-m|Le camp, sous le banc.",
            "maman|D'accord.",
            "maman|On se glisse là.",
            "narrateur|Il pousse le sac jaune sous le bois.",
            "narrateur|La pomme roule d'un cran, puis tient.",
            "papa|L'escargot te voit, un peu.",
            "enfant-m|Je le regarde.",
            "narrateur|L'arrosoir fait une dernière goutte.",
            "narrateur|Elle brille sur la feuille.",
        ),
        3: ln(
            "narrateur|Victorino monte le sac vers la chambre.",
            "narrateur|Un rayon entre par le rideau.",
            "narrateur|Le tapis de la chambre est doux et beige.",
            "enfant-m|Le camp, près du lit.",
            "maman|D'accord.",
            "maman|Le doudou peut venir.",
            "narrateur|Il pose le sac jaune près de l'oreiller.",
            "narrateur|La pomme appuie un peu le tissu.",
            "papa|Tu as ton goûter, ici aussi.",
            "enfant-m|Oui.",
            "enfant-m|Près du doudou.",
            "narrateur|Le rideau bouge un tout petit peu.",
            "narrateur|Le plancher fait un petit cri.",
        ),
    },
    2: {
        1: ln(
            "narrateur|Victorino porte le sac vers la cuisine.",
            "narrateur|Le carrelage est un peu froid.",
            "narrateur|Un bol bleu attend sur la table.",
            "enfant-m|Le camp, sous la table.",
            "papa|D'accord.",
            "papa|On se glisse là.",
            "narrateur|Il pose le sac jaune à côté du bol.",
            "narrateur|Le pot fait un petit toc, au fond.",
            "maman|Le yaourt reste au frais, là.",
            "enfant-m|Oui.",
            "enfant-m|Il est froid.",
            "narrateur|Un robinet goutte, tout loin.",
            "narrateur|Le torchon de l'évier ne bouge plus.",
        ),
        2: ln(
            "narrateur|Victorino repose le sac sur le banc.",
            "narrateur|L'herbe est encore humide sous les chaussures.",
            "narrateur|L'escargot est tout près de la laitue.",
            "enfant-m|Le camp, sous le banc.",
            "maman|D'accord.",
            "maman|On se glisse là.",
            "narrateur|Il pousse le sac jaune sous le bois.",
            "narrateur|Le pot froid touche le tissu.",
            "papa|L'escargot te voit, un peu.",
            "enfant-m|Je le regarde.",
            "narrateur|L'arrosoir fait une dernière goutte.",
            "narrateur|Elle brille sur la feuille.",
        ),
        3: ln(
            "narrateur|Victorino monte le sac vers la chambre.",
            "narrateur|Un rayon entre par le rideau.",
            "narrateur|Le tapis de la chambre est doux et beige.",
            "enfant-m|Le camp, près du lit.",
            "maman|D'accord.",
            "maman|Le doudou peut venir.",
            "narrateur|Il pose le sac jaune près de l'oreiller.",
            "narrateur|Le pot laisse un rond froid, au fond.",
            "papa|Tu as ton goûter, ici aussi.",
            "enfant-m|Oui.",
            "enfant-m|Près du doudou.",
            "narrateur|Le rideau bouge un tout petit peu.",
            "narrateur|Le plancher fait un petit cri.",
        ),
    },
    3: {
        1: ln(
            "narrateur|Victorino porte le sac vers la cuisine.",
            "narrateur|Le carrelage est un peu froid.",
            "narrateur|Un bol bleu attend sur la table.",
            "enfant-m|Le camp, sous la table.",
            "papa|D'accord.",
            "papa|On se glisse là.",
            "narrateur|Il pose le sac jaune à côté du bol.",
            "narrateur|Le papier du pain froisse, tout doux.",
            "maman|Ça sent encore le four, ici.",
            "enfant-m|Oui.",
            "enfant-m|Il est tiède.",
            "narrateur|Un robinet goutte, tout loin.",
            "narrateur|Le torchon de l'évier ne bouge plus.",
        ),
        2: ln(
            "narrateur|Victorino repose le sac sur le banc.",
            "narrateur|L'herbe est encore humide sous les chaussures.",
            "narrateur|L'escargot est tout près de la laitue.",
            "enfant-m|Le camp, sous le banc.",
            "maman|D'accord.",
            "maman|On se glisse là.",
            "narrateur|Il pousse le sac jaune sous le bois.",
            "narrateur|Le pain reste au chaud, au fond.",
            "papa|L'escargot te voit, un peu.",
            "enfant-m|Je le regarde.",
            "narrateur|L'arrosoir fait une dernière goutte.",
            "narrateur|Elle brille sur la feuille.",
        ),
        3: ln(
            "narrateur|Victorino monte le sac vers la chambre.",
            "narrateur|Un rayon entre par le rideau.",
            "narrateur|Le tapis de la chambre est doux et beige.",
            "enfant-m|Le camp, près du lit.",
            "maman|D'accord.",
            "maman|Le doudou peut venir.",
            "narrateur|Il pose le sac jaune près de l'oreiller.",
            "narrateur|Le pain sent encore le village.",
            "papa|Tu as ton goûter, ici aussi.",
            "enfant-m|Oui.",
            "enfant-m|Près du doudou.",
            "narrateur|Le rideau bouge un tout petit peu.",
            "narrateur|Le plancher fait un petit cri.",
        ),
    },
}

T3Q_046 = ln(
    "papa|Tu prends quel jeu, pour le camp ?",
    "narrateur|Les cubes.",
    "narrateur|Le livre.",
    "narrateur|Ou la dînette.",
)

PLAY_046 = {
    (1, 1): ln(
        "narrateur|Les cubes de bois sont près du bol bleu.",
        "narrateur|Un cube rouge, un cube bleu.",
        "enfant-m|Un mur, pour le camp.",
        "papa|Tout doux, sur le carrelage.",
        "narrateur|Les cubes font toc toc.",
        "narrateur|Un cube jaune roule, puis s'arrête.",
    ),
    (1, 2): ln(
        "narrateur|Le livre a une image d'arbre, devant.",
        "narrateur|La couverture est lisse, un peu froide.",
        "enfant-m|Je montre l'arbre au camp.",
        "maman|Sous la table, oui.",
        "narrateur|Une page fait un petit chh.",
        "narrateur|Un coin se plie, tout doux.",
    ),
    (1, 3): ln(
        "narrateur|La dînette a une tasse minuscule.",
        "narrateur|Une petite assiette est blanche et lisse.",
        "enfant-m|On sert le goûter, ici.",
        "papa|Dans la tasse, tout petit.",
        "narrateur|La tasse fait ting.",
        "narrateur|Une cuillère minuscule reste au fond.",
    ),
    (2, 1): ln(
        "narrateur|Les cubes de bois sont près du banc.",
        "narrateur|Un cube rouge, un cube bleu.",
        "enfant-m|Un mur, pour l'escargot.",
        "maman|Pas trop près de lui.",
        "narrateur|Les cubes font toc toc.",
        "narrateur|Un cube jaune roule dans l'herbe.",
    ),
    (2, 2): ln(
        "narrateur|Le livre a une image d'arbre, devant.",
        "narrateur|La couverture est lisse, un peu froide.",
        "enfant-m|Je montre l'arbre à l'escargot.",
        "papa|Il avance encore, tout doux.",
        "narrateur|Une page fait un petit chh.",
        "narrateur|Un coin se plie, tout doux.",
    ),
    (2, 3): ln(
        "narrateur|La dînette a une tasse minuscule.",
        "narrateur|Une petite assiette est blanche et lisse.",
        "enfant-m|Un thé de laitue, pour lui.",
        "maman|Tout petit, d'accord.",
        "narrateur|La tasse fait ting.",
        "narrateur|Une cuillère minuscule reste au fond.",
    ),
    (3, 1): ln(
        "narrateur|Les cubes de bois sont au pied du lit.",
        "narrateur|Un cube rouge, un cube bleu.",
        "enfant-m|Un mur, près du doudou.",
        "papa|Sur le tapis, tout doux.",
        "narrateur|Les cubes font toc toc.",
        "narrateur|Un cube jaune roule, puis s'arrête.",
    ),
    (3, 2): ln(
        "narrateur|Le livre a une image d'arbre, devant.",
        "narrateur|La couverture est lisse, un peu froide.",
        "enfant-m|Je lis au doudou.",
        "maman|Tout bas, près du lit.",
        "narrateur|Une page fait un petit chh.",
        "narrateur|Un coin se plie, tout doux.",
    ),
    (3, 3): ln(
        "narrateur|La dînette a une tasse minuscule.",
        "narrateur|Une petite assiette est blanche et lisse.",
        "enfant-m|On sert le doudou, aussi.",
        "papa|Une goutte, tout petit.",
        "narrateur|La tasse fait ting.",
        "narrateur|Une cuillère minuscule reste au fond.",
    ),
}

GOUT_046 = {
    1: ln(
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|La pomme est encore froide, au fond.",
        "enfant-m|On croque un peu ?",
        "maman|Oui.",
        "maman|Un petit bout.",
        "narrateur|Ça croque, tout doux.",
        "papa|Merci, Victorino.",
    ),
    2: ln(
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Le pot est encore froid, au fond.",
        "enfant-m|On goûte un peu ?",
        "papa|Oui.",
        "papa|Le couvercle, d'abord.",
        "narrateur|Le couvercle fait un petit clic.",
        "maman|Merci, Victorino.",
    ),
    3: ln(
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Le pain est encore tiède, au fond.",
        "enfant-m|On rompt un peu ?",
        "maman|Oui.",
        "maman|Un petit morceau.",
        "narrateur|Le pain sent encore le village.",
        "papa|Merci, Victorino.",
    ),
}

IMG_046 = {
    (1, 1, 1): "Un cube a un reflet vert, tout petit.",
    (1, 1, 2): "Une page sent encore la pomme, un peu.",
    (1, 1, 3): "La petite tasse a un bout de peau.",
    (1, 2, 1): "Un cube a une feuille collée, au coin.",
    (1, 2, 2): "Une page a une goutte de rosée.",
    (1, 2, 3): "La petite assiette a une miette verte.",
    (1, 3, 1): "Un cube touche le doudou, tout calme.",
    (1, 3, 2): "Une page reste ouverte près de l'oreiller.",
    (1, 3, 3): "La petite tasse brille sur le tapis.",
    (2, 1, 1): "Un cube a un rond d'eau, au coin.",
    (2, 1, 2): "Une page a un peu de blanc, au bord.",
    (2, 1, 3): "La petite cuillère est encore froide.",
    (2, 2, 1): "Un cube a une goutte d'herbe.",
    (2, 2, 2): "Une page sent le jardin, tout bas.",
    (2, 2, 3): "La petite assiette a un rond d'eau.",
    (2, 3, 1): "Un cube sèche près du doudou.",
    (2, 3, 2): "Une page reste froide, sur le lit.",
    (2, 3, 3): "La petite tasse a un voile blanc.",
    (3, 1, 1): "Un cube a une miette de pain.",
    (3, 1, 2): "Une page sent encore le four.",
    (3, 1, 3): "La petite tasse a une miette tiède.",
    (3, 2, 1): "Un cube a une miette dans l'herbe.",
    (3, 2, 2): "Une page sent le pain, tout bas.",
    (3, 2, 3): "La petite assiette a une miette blonde.",
    (3, 3, 1): "Un cube a une miette sur le tapis.",
    (3, 3, 2): "Une page reste ouverte près du pain.",
    (3, 3, 3): "La petite tasse sent encore le village.",
}

FIN_IMG_046 = {
    (1, 1, 1): "Le bol bleu ne bouge plus, sur la table.",
    (1, 1, 2): "Le robinet fait une dernière goutte.",
    (1, 1, 3): "Le torchon de l'évier est calme.",
    (1, 2, 1): "L'escargot n'a presque pas bougé.",
    (1, 2, 2): "L'arrosoir reste penché, tout doux.",
    (1, 2, 3): "Une goutte sèche sur la laitue.",
    (1, 3, 1): "Le doudou du lit attend, tout calme.",
    (1, 3, 2): "Le rideau ne bouge plus.",
    (1, 3, 3): "Un rayon reste sur le tapis beige.",
    (2, 1, 1): "Le bol bleu a un petit rond d'eau.",
    (2, 1, 2): "Le carrelage sèche, tout doux.",
    (2, 1, 3): "Le couvercle blanc brille encore.",
    (2, 2, 1): "L'herbe brille encore, sous le banc.",
    (2, 2, 2): "L'abeille s'en est allée.",
    (2, 2, 3): "Le bois du banc est tiède.",
    (2, 3, 1): "Le plancher ne crie plus.",
    (2, 3, 2): "Le doudou est un peu froid, au bord.",
    (2, 3, 3): "Le clic de la sangle s'arrête.",
    (3, 1, 1): "Une miette reste près du bol bleu.",
    (3, 1, 2): "Ça sent encore le four, tout bas.",
    (3, 1, 3): "Le papier du pain ne bouge plus.",
    (3, 2, 1): "Une miette reste dans l'herbe.",
    (3, 2, 2): "L'escargot avance d'un cran.",
    (3, 2, 3): "Le banc sent encore le pain.",
    (3, 3, 1): "Une miette reste sur le tapis.",
    (3, 3, 2): "L'oreiller sent encore le village.",
    (3, 3, 3): "Le sac jaune est un peu tiède.",
}


def l3_046(i: int, j: int, k: int) -> list[str]:
    lines = list(PLAY_046[(j, k)])
    lines.extend(GOUT_046[i])
    lines.append(f"narrateur|{IMG_046[(i, j, k)]}")
    return ln(*lines)


def fin_046(i: int, j: int, k: int) -> list[str]:
    food = FOOD_046[i]
    lieu = LIEU_046[j]
    jeu = JEU_046[k]
    return ln(
        f"narrateur|{IMG_046[(i, j, k)]}",
        f"narrateur|Victorino a fait le camp {lieu['ou']}.",
        f"narrateur|Il a pris {jeu['lab']}.",
        f"enfant-m|{food['le'].capitalize()} était dans le sac.",
        "maman|Oui.",
        "papa|Merci, Victorino.",
        "narrateur|Le sac jaune tient, un peu lourd.",
        f"narrateur|{FIN_IMG_046[(i, j, k)]}",
        "narrateur|Victorino pose une main sur le tissu.",
        "narrateur|Le jaune est un peu tiède, maintenant.",
    )


def build_046() -> tuple[dict, dict, dict]:
    s = assemble(
        DEBUT_046,
        T1Q_046,
        L1_046,
        Q_046,
        C_046,
        T2Q_046,
        L2_046,
        T3Q_046,
        l3_046,
        fin_046,
    )
    sons: dict[str, str] = {"CHK_T0000_P0000": "arrosoir,escargot"}
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": extras_opts("une pomme", "un yaourt", "un morceau de pain"),
    }
    for i, food in FOOD_046.items():
        p = f"CHK_T0001_P000{i}"
        sons[p] = food["son"]
        extras[f"{p}_Q0001"] = extras_q(
            "sac",
            "sac | le sac | dans le sac | le sac jaune",
            "Dans le sac jaune. Il l'a mis où ?",
        )
        extras[f"{p}_T0002_P0000"] = extras_opts(
            "la cuisine", "le jardin", "la chambre"
        )
        for j, lieu in LIEU_046.items():
            p2 = f"{p}_T0002_P000{j}"
            sons[p2] = lieu["son"]
            extras[f"{p2}_T0003_P0000"] = extras_opts(
                "les cubes", "le livre", "la dînette"
            )
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-047  N2  Raphaël  AUT.AFF.002
# Manteau bleu près des bottes. Froid sans manteau. Pas une consigne.
# ≠ TREE-AUT-016 (laine, radiateur, flaque, manche à l'envers).
# ≠ TREE-COL-001 (pommes, train).
# ---------------------------------------------------------------------------

LIEU_047 = {
    1: {"lab": "la cuisine", "ou": "par la cuisine", "son": "porte"},
    2: {"lab": "le jardin", "ou": "par le jardin", "son": "herbe"},
    3: {"lab": "la chambre", "ou": "par la chambre", "son": "rideau"},
}
JEU_047 = {
    1: {"lab": "les cubes", "un": "un cube"},
    2: {"lab": "le livre", "un": "le livre"},
    3: {"lab": "la dînette", "un": "une tasse"},
}
MOM_047 = {
    1: {"lab": "le matin", "quand": "le matin"},
    2: {"lab": "après la sieste", "quand": "après la sieste"},
    3: {"lab": "le soir", "quand": "le soir"},
}

DEBUT_047 = ln(
    "narrateur|Le paillasson de l'entrée est encore mouillé.",
    "narrateur|Deux bottes jaunes brillent dessus.",
    "narrateur|Une goutte tombe d'une botte.",
    "narrateur|Elle fait un petit rond sombre.",
    "narrateur|Dehors, le marché sent le pain chaud.",
    "narrateur|Une cloche de vélo tinte, tout loin.",
    "narrateur|Le portemanteau de bois est bas.",
    "narrateur|Un manteau bleu attend, près des bottes.",
    "narrateur|Le tissu est un peu froid.",
    "narrateur|Papa essuie le bord d'une botte.",
    "papa|Les bottes sont prêtes, Raphaël.",
    "narrateur|Maman ouvre un peu la porte.",
    "maman|Tu as senti le pain, dehors ?",
    "enfant-m|Oui, maman.",
    "enfant-m|Ça sent bon.",
    "enfant-m|Je veux sortir !",
    "papa|D'accord.",
    "narrateur|En ce moment, Raphaël enfile une botte.",
    "narrateur|Il ouvre la porte, tout grand.",
    "narrateur|L'air froid lui prend les bras.",
    "enfant-m|J'ai froid, papa.",
    "maman|Le manteau bleu est près des bottes.",
    "narrateur|Raphaël recule d'un pas.",
    "narrateur|Il touche le manteau.",
)

T1Q_047 = ln(
    "papa|On passe où, d'abord ?",
    "narrateur|La cuisine.",
    "narrateur|Le jardin.",
    "narrateur|Ou la chambre.",
)

L1_047 = {
    1: ln(
        "narrateur|Raphaël pousse la porte de la cuisine.",
        "narrateur|Le carrelage est un peu froid.",
        "narrateur|Ça sent le pain, tout près.",
        "enfant-m|La porte du fond, papa.",
        "papa|Elle donne sur le jardin.",
        "narrateur|Papa ouvre un tout petit peu.",
        "narrateur|Un courant d'air glisse sur les bras.",
        "enfant-m|J'ai encore froid.",
        "maman|Le manteau est resté près des bottes.",
        "narrateur|Raphaël revient vers l'entrée.",
        "narrateur|Il prend le manteau bleu.",
        "narrateur|Il glisse un bras, puis l'autre.",
        "narrateur|Le tissu se réchauffe contre lui.",
        "enfant-m|Il est chaud.",
        "papa|Oui.",
        "papa|Tes bras aussi.",
        "narrateur|La fermeture fait un petit bruit.",
        "narrateur|Le carrelage reste froid, tout calme.",
    ),
    2: ln(
        "narrateur|Raphaël va vers le jardin.",
        "narrateur|L'herbe est encore mouillée.",
        "narrateur|Une feuille colle à une botte.",
        "enfant-m|Je sors, maman.",
        "maman|L'air est frais, là.",
        "narrateur|Il pose un pied dans l'herbe.",
        "narrateur|L'air sent la terre mouillée.",
        "enfant-m|Mes bras sont froids.",
        "papa|Le manteau bleu est près des bottes.",
        "narrateur|Raphaël rentre d'un pas.",
        "narrateur|Il prend le manteau bleu.",
        "narrateur|Il glisse un bras, puis l'autre.",
        "narrateur|Le col chatouille le menton.",
        "enfant-m|Il est chaud.",
        "maman|Oui.",
        "maman|L'herbe peut attendre.",
        "narrateur|Une goutte glisse encore d'une botte.",
        "narrateur|Le paillasson reste sombre, au milieu.",
    ),
    3: ln(
        "narrateur|Raphaël monte vers la chambre.",
        "narrateur|Le plancher fait un petit cri.",
        "narrateur|Un rayon touche le lit.",
        "enfant-m|J'ouvre la fenêtre, un peu.",
        "papa|Tout doux, d'accord.",
        "narrateur|Le rideau se soulève.",
        "narrateur|L'air froid entre, tout net.",
        "enfant-m|J'ai froid aux bras.",
        "maman|Le manteau est resté en bas.",
        "narrateur|Raphaël redescend l'escalier.",
        "narrateur|Les bottes font toc toc.",
        "narrateur|Il prend le manteau bleu.",
        "narrateur|Il glisse un bras, puis l'autre.",
        "enfant-m|Il est chaud.",
        "papa|Oui.",
        "papa|Près des bottes, il t'attendait.",
        "narrateur|Le tissu sent encore le savon.",
        "narrateur|Le portemanteau de bois est vide, maintenant.",
    ),
}

Q_047 = {
    1: ln(
        "narrateur|Raphaël n'a plus froid aux bras.",
        "papa|Il a pris quoi, près des bottes ?",
    ),
    2: ln(
        "narrateur|L'air ne pique plus les bras.",
        "maman|Raphaël a pris quoi ?",
    ),
    3: ln(
        "narrateur|Les bras sont au chaud, maintenant.",
        "papa|Raphaël a pris quoi, en bas ?",
    ),
}

C_047 = {
    1: ln(
        "narrateur|Oui.",
        "narrateur|Le manteau bleu est sur lui.",
        "papa|Merci, Raphaël.",
        "enfant-m|Je n'ai plus froid.",
        "maman|On emporte un jeu ?",
        "narrateur|La porte du fond reste un peu ouverte.",
        "narrateur|Un courant d'air tiédit, déjà.",
    ),
    2: ln(
        "narrateur|Oui.",
        "narrateur|Le manteau bleu est sur lui.",
        "maman|Merci, Raphaël.",
        "enfant-m|Je n'ai plus froid.",
        "papa|On emporte un jeu, pour le jardin ?",
        "narrateur|La feuille reste collée à la botte.",
        "narrateur|L'herbe attend encore.",
    ),
    3: ln(
        "narrateur|Oui.",
        "narrateur|Le manteau bleu est sur lui.",
        "papa|Merci, Raphaël.",
        "enfant-m|Je n'ai plus froid.",
        "maman|On emporte un jeu, de la chambre ?",
        "narrateur|Le rideau se tait, en haut.",
        "narrateur|Le portemanteau reste vide, un moment.",
    ),
}

T2Q_047 = ln(
    "maman|Tu emportes quel jeu ?",
    "narrateur|Les cubes.",
    "narrateur|Le livre.",
    "narrateur|Ou la dînette.",
)

L2_047 = {
    1: {
        1: ln(
            "narrateur|Les cubes de bois sont près du bol.",
            "narrateur|Un cube claque contre un autre.",
            "papa|Les cubes, Raphaël.",
            "papa|Tu les emportes ?",
            "enfant-m|Oui.",
            "enfant-m|Les cubes.",
            "narrateur|Il les met dans une petite boîte.",
            "narrateur|Le manteau bleu frotte la table.",
            "maman|Un cube a un coin un peu rêche.",
            "enfant-m|Il gratte.",
            "papa|On les sort, un moment.",
            "narrateur|Le carrelage reste froid sous les bottes.",
        ),
        2: ln(
            "narrateur|Le livre a une couverture lisse.",
            "narrateur|Une page est un peu cornée.",
            "maman|Le livre, Raphaël.",
            "maman|Tu l'emportes ?",
            "enfant-m|Oui.",
            "enfant-m|Le livre.",
            "narrateur|Il le serre contre le manteau.",
            "narrateur|Le bleu cache un coin de page.",
            "papa|Il reste au chaud, là.",
            "enfant-m|Oui.",
            "narrateur|Une page tourne, tout doux.",
            "narrateur|Ça sent encore le pain, tout près.",
        ),
        3: ln(
            "narrateur|La dînette cliquette dans son panier.",
            "narrateur|Une petite assiette est blanche.",
            "papa|La dînette, Raphaël.",
            "papa|Tu l'emportes ?",
            "enfant-m|Oui.",
            "enfant-m|La dînette.",
            "narrateur|Il prend le panier d'une main.",
            "narrateur|L'autre main tient un bouton.",
            "maman|On sert le pain, tout petit ?",
            "enfant-m|Un thé de mie.",
            "narrateur|Une tasse minuscule fait ting.",
            "narrateur|Le manteau bleu fait un pli au coude.",
        ),
    },
    2: {
        1: ln(
            "narrateur|Les cubes attendent près de la porte.",
            "narrateur|Un reflet d'herbe passe dessus.",
            "maman|Les cubes, Raphaël.",
            "maman|Tu les emportes ?",
            "enfant-m|Oui.",
            "enfant-m|Les cubes.",
            "narrateur|Il les empile, tout lentement.",
            "narrateur|Le manteau frotte le rebord froid.",
            "papa|Tu as ton manteau, pour le jardin ?",
            "enfant-m|Oui.",
            "enfant-m|Je l'ai pris.",
            "narrateur|La feuille collée tremble encore.",
            "narrateur|Ça sent la terre, tout bas.",
        ),
        2: ln(
            "narrateur|Le livre est sur la marche, près de la porte.",
            "narrateur|Une page est un peu cornée.",
            "papa|Le livre, Raphaël.",
            "papa|Tu l'emportes ?",
            "enfant-m|Oui.",
            "enfant-m|Le livre.",
            "narrateur|Il le glisse sous le bras, contre le bleu.",
            "narrateur|Le col du manteau chatouille le menton.",
            "maman|Une goutte brille sur l'herbe, dehors.",
            "enfant-m|Je la montre au livre.",
            "papa|D'accord.",
            "narrateur|Le jardin attend derrière la porte.",
        ),
        3: ln(
            "narrateur|La dînette est dans le panier d'osier.",
            "narrateur|L'osier pique un peu les doigts.",
            "maman|La dînette, Raphaël.",
            "maman|Tu l'emportes ?",
            "enfant-m|Oui.",
            "enfant-m|La dînette.",
            "narrateur|Il soulève le panier.",
            "narrateur|Le manteau bleu fait un pli au coude.",
            "papa|Tu as ton manteau, pour dehors ?",
            "enfant-m|Oui.",
            "enfant-m|Je l'ai pris.",
            "narrateur|Une petite cuillère brille.",
            "narrateur|La terre du jardin sent la pluie d'hier.",
        ),
    },
    3: {
        1: ln(
            "narrateur|Les cubes sont au pied du lit.",
            "narrateur|Un cube tapote le parquet, tout doux.",
            "papa|Les cubes, Raphaël.",
            "papa|Tu les emportes ?",
            "enfant-m|Oui.",
            "enfant-m|Pour dehors.",
            "narrateur|Il les range dans la boîte.",
            "narrateur|Le manteau frotte la couverture.",
            "maman|Le doudou reste ici ?",
            "enfant-m|Oui.",
            "papa|On emporte les cubes.",
            "narrateur|Le rideau touche son épaule, un instant.",
        ),
        2: ln(
            "narrateur|Sur la couverture, le livre est ouvert.",
            "narrateur|Le rideau colore un peu la page.",
            "maman|Le livre, Raphaël.",
            "maman|Tu l'emportes ?",
            "enfant-m|Oui.",
            "enfant-m|Le livre.",
            "narrateur|Il le glisse sous le manteau.",
            "narrateur|Il reste au chaud, contre le bleu.",
            "papa|Une page peut servir dehors ?",
            "enfant-m|Oui.",
            "narrateur|Une page se recourbe, tout doux.",
            "narrateur|L'oreiller sent encore le savon.",
        ),
        3: ln(
            "narrateur|La dînette attend au pied du lit.",
            "narrateur|Une petite tasse est près du doudou.",
            "papa|La dînette, Raphaël.",
            "papa|Tu l'emportes ?",
            "enfant-m|Oui.",
            "enfant-m|Un thé dehors.",
            "narrateur|Il prend le panier.",
            "narrateur|Le manteau bleu cache l'osier.",
            "maman|La tasse tient dans la poche ?",
            "enfant-m|À côté du bouton.",
            "narrateur|La petite assiette reste dans l'autre main.",
            "narrateur|Le tapis de la chambre est calme.",
        ),
    },
}

T3Q_047 = ln(
    "papa|C'est quel moment, dehors ?",
    "narrateur|Le matin.",
    "narrateur|Après la sieste.",
    "narrateur|Ou le soir.",
)

MOMENT_047 = {
    1: ln(
        "narrateur|Le matin, la lumière est pâle, un peu bleue.",
        "narrateur|Un oiseau chante une fois.",
    ),
    2: ln(
        "narrateur|Après la sieste, l'air de la maison est tiède.",
        "narrateur|Les joues de Raphaël sont encore chaudes.",
    ),
    3: ln(
        "narrateur|Le soir, la lampe de l'entrée est douce.",
        "narrateur|L'horloge fait tic tac, tout loin.",
    ),
}

SORTIE_047 = {
    1: ln(
        "papa|L'air du matin est clair.",
        "narrateur|Ils sortent un moment.",
        "narrateur|L'air touche le nez de Raphaël.",
        "enfant-m|Ça sent le pain.",
        "maman|Tes bras, dans le manteau ?",
        "enfant-m|Ils sont au chaud.",
    ),
    2: ln(
        "papa|L'air a réchauffé, un peu.",
        "narrateur|Ils sortent un moment.",
        "narrateur|Le soleil est jaune et doux.",
        "enfant-m|C'est tiède.",
        "maman|Le manteau est encore utile.",
        "enfant-m|Oui, un peu.",
    ),
    3: ln(
        "papa|L'air du soir est plus frais.",
        "narrateur|Ils sortent un moment.",
        "narrateur|Les fenêtres de la maison sont bleues.",
        "enfant-m|Je vois les lumières.",
        "maman|Le manteau te tient chaud.",
        "enfant-m|Oui, maman.",
    ),
}

JEU_DEHORS_047 = {
    (1, 1): "narrateur|Raphaël pose les cubes un moment sur le pas.",
    (1, 2): "narrateur|Raphaël ouvre le livre un instant, près de la porte.",
    (1, 3): "narrateur|Raphaël pose une tasse minuscule, puis la reprend.",
    (2, 1): "narrateur|Au jardin, Raphaël empile deux cubes sur une pierre.",
    (2, 2): "narrateur|Au jardin, Raphaël montre une image à la feuille.",
    (2, 3): "narrateur|Au jardin, Raphaël sert une feuille dans l'assiette.",
    (3, 1): "narrateur|Près du seuil, Raphaël pose un cube sur la marche.",
    (3, 2): "narrateur|Près du seuil, Raphaël glisse une feuille dans le livre.",
    (3, 3): "narrateur|Près du seuil, Raphaël sert une goutte dans la tasse.",
}

RETOUR_047 = ln(
    "maman|C'est l'heure de rentrer.",
    "narrateur|Ils rentrent.",
    "narrateur|La maison est tiède.",
    "narrateur|Le manteau bleu est un peu lourd.",
    "narrateur|Il goutte, tout doux.",
    "papa|Il sèche mieux, près des bottes.",
    "narrateur|Raphaël retire le manteau bleu.",
    "narrateur|Il le raccroche au portemanteau.",
    "narrateur|Les boutons pendent, calmes.",
    "enfant-m|Il est à sa place.",
    "maman|Oui.",
    "maman|Près des bottes.",
    "papa|Merci, Raphaël.",
)

IMG_047 = {
    (1, 1, 1): "Un cube a une miette de pain, au coin.",
    (1, 1, 2): "Le bol de la cuisine a glissé d'un cran.",
    (1, 1, 3): "La porte du fond ne tremble plus.",
    (1, 2, 1): "Une page du livre sent le pain.",
    (1, 2, 2): "Une miette reste sous le livre.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse est encore tiède.",
    (1, 3, 2): "Une cuillère minuscule brille.",
    (1, 3, 3): "Le panier d'osier est posé droit.",
    (2, 1, 1): "Une goutte d'herbe sèche sur un cube.",
    (2, 1, 2): "La feuille collée ne tremble plus.",
    (2, 1, 3): "Un peu de terre reste au seuil.",
    (2, 2, 1): "Le livre a une page un peu fraîche.",
    (2, 2, 2): "Une goutte a séché sur la vitre.",
    (2, 2, 3): "L'herbe a laissé une odeur verte.",
    (2, 3, 1): "Une feuille a voyagé dans l'assiette.",
    (2, 3, 2): "L'osier sent encore le jardin.",
    (2, 3, 3): "Le panier a une petite tache d'eau.",
    (3, 1, 1): "Un cube repose près de l'oreiller.",
    (3, 1, 2): "Un cube est contre le doudou, tout calme.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Une bande de rideau colore encore la page.",
    (3, 2, 2): "Sur la couverture, le livre reste ouvert.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FIN_IMG_047 = {
    (1, 1, 1): "Les bottes jaunes brillent encore, au paillasson.",
    (1, 1, 2): "Une miette reste près de la porte.",
    (1, 1, 3): "Un bouton du manteau brille, au bois.",
    (1, 2, 1): "Un oiseau chante encore, tout loin.",
    (1, 2, 2): "La page se recourbe, près des bottes.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "Le pain sent encore, tout bas.",
    (1, 3, 3): "Le manteau bleu sèche, près des bottes.",
    (2, 1, 1): "Les chaussettes sèchent près de la porte.",
    (2, 1, 2): "L'herbe colle encore à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau.",
    (2, 2, 1): "Une feuille vraie reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "La cloche de vélo ne tinte plus.",
    (2, 3, 1): "La petite assiette a encore de l'herbe.",
    (2, 3, 2): "Le col bleu sèche, au portemanteau.",
    (2, 3, 3): "Une odeur de terre reste au seuil.",
    (3, 1, 1): "Le doudou repose sur un cube.",
    (3, 1, 2): "L'oreiller sent encore le savon.",
    (3, 1, 3): "Plus rien ne bouge, au rideau.",
    (3, 2, 1): "Une feuille sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près du doudou.",
    (3, 3, 2): "Le tapis de la chambre est calme.",
    (3, 3, 3): "Le paillasson n'a plus de rond sombre.",
}


def l3_047(i: int, j: int, k: int) -> list[str]:
    jeu = JEU_047[j]
    lines = list(MOMENT_047[k])
    lines.extend(SORTIE_047[k])
    lines.append(JEU_DEHORS_047[(i, j)])
    lines.extend(RETOUR_047)
    lines.append(f"narrateur|{jeu['un'].capitalize()} rentre avec eux.")
    lines.append(f"narrateur|{IMG_047[(i, j, k)]}")
    return ln(*lines)


def fin_047(i: int, j: int, k: int) -> list[str]:
    lieu = LIEU_047[i]
    jeu = JEU_047[j]
    mom = MOM_047[k]
    return ln(
        f"narrateur|{IMG_047[(i, j, k)]}",
        f"narrateur|Raphaël est passé {lieu['ou']}.",
        f"narrateur|Il a pris {jeu['lab']}.",
        f"narrateur|C'était {mom['quand']}.",
        "enfant-m|Le manteau est près des bottes.",
        "maman|Oui.",
        "maman|Il sèche, là.",
        "papa|Merci, Raphaël.",
        f"narrateur|{FIN_IMG_047[(i, j, k)]}",
        "narrateur|Raphaël touche encore un bouton.",
    )


def build_047() -> tuple[dict, dict, dict]:
    s = assemble(
        DEBUT_047,
        T1Q_047,
        L1_047,
        Q_047,
        C_047,
        T2Q_047,
        L2_047,
        T3Q_047,
        l3_047,
        fin_047,
    )
    sons: dict[str, str] = {"CHK_T0000_P0000": "bottes,porte"}
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": extras_opts("la cuisine", "le jardin", "la chambre"),
    }
    for i, lieu in LIEU_047.items():
        p = f"CHK_T0001_P000{i}"
        sons[p] = lieu["son"]
        extras[f"{p}_Q0001"] = extras_q(
            "manteau",
            "manteau | le manteau | son manteau | le manteau bleu",
            "Le manteau bleu. Il a pris quoi ?",
        )
        extras[f"{p}_T0002_P0000"] = extras_opts(
            "les cubes", "le livre", "la dînette"
        )
        for j in (1, 2, 3):
            extras[f"{p}_T0002_P000{j}_T0003_P0000"] = extras_opts(
                "le matin", "après la sieste", "le soir"
            )
    return s, sons, extras


def main() -> None:
    s46, n46, e46 = build_046()
    write_tree(
        "TREE-AUT-046",
        "Victorino veut un camp près de l'escargot. "
        "Le sac jaune sur le banc est vide, tout mou. "
        "Il y glisse un goûter, puis il installe le camp. "
        "Cuisine, jardin ou chambre : la suite change.",
        "Le sac jaune de Victorino sur le banc",
        "Victorino, papa, maman",
        "jardin, arrosoir, laitue, escargot, banc de bois",
        s46,
        n46,
        e46,
    )
    relecture(
        "TREE-AUT-046",
        "Le sac jaune de Victorino sur le banc",
        "Victorino veut un camp près de l'escargot. Arrosoir, laitue, "
        "banc, sac jaune vide. Pomme / yaourt / pain, puis cuisine / "
        "jardin / chambre, puis cubes / livre / dînette. Le sac floppe "
        "vide ; le goûter tient quand il est dedans.",
        "Victorino déjà D16. N2. AUT.AFF.001 implicite. "
        "Pas une packing-list. Pas « ce que l'adulte a dit ». "
        "Monde ≠ TREE-AUT-009 (sac bleu, crochet). "
        "Monde ≠ TREE-COL-001 (pommes, train). Fin sensorielle.",
    )

    s47, n47, e47 = build_047()
    write_tree(
        "TREE-AUT-047",
        "Raphaël veut sortir. L'air froid lui prend les bras. "
        "Le manteau bleu attend près des bottes. "
        "Il le met. En rentrant, le manteau goutte : "
        "il le raccroche au portemanteau.",
        "Le manteau de Raphaël près des bottes",
        "Raphaël, papa, maman",
        "entrée, paillasson mouillé, bottes jaunes, portemanteau",
        s47,
        n47,
        e47,
    )
    relecture(
        "TREE-AUT-047",
        "Le manteau de Raphaël près des bottes",
        "Raphaël veut sortir. Paillasson, bottes jaunes, cloche de vélo, "
        "manteau bleu près des bottes. Cuisine / jardin / chambre, puis "
        "cubes / livre / dînette, puis matin / sieste / soir. "
        "Froid sans manteau. En rentrant, il le raccroche.",
        "Raphaël déjà D16. N2. AUT.AFF.002 implicite. "
        "Monde ≠ TREE-AUT-016 (laine, radiateur, flaque). "
        "Monde ≠ TREE-COL-001 (pommes, train). "
        "Pas « on va apprendre ». Fin sensorielle.",
    )


if __name__ == "__main__":
    main()
