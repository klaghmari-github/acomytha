#!/usr/bin/env python3
"""TREE-DIF-013 — Le sel sur les lèvres de Sarah. DIF.COR.001 implicite, N2."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-013"
N2 = LIMITS["N2"]


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"sans fin: {ph}")
    return list(rows)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
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
    out["fil_rouge"] = (
        "Sarah veut le sel des vagues sur les lèvres, avec un vrai jeu. "
        "Victorino arrive, le seau contre le genou. Ils prennent gobelet, "
        "pelle et moulin. Une dune trop pentue, des algues trop hautes ou "
        "un ruisseau trop large arrête l'écume. Ils trouvent à leur pas. "
        "Le grain pique enfin, sur leurs lèvres."
    )
    out["title"] = "Le sel sur les lèvres de Sarah"
    out["characters"] = "Sarah, Victorino, papa, maman"
    out["setting"] = "cabane au bord de la mer, dune et écume"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    if re.search(r"\bsara\b", whole):
        raise SystemExit(f"{SID}: Sara (hors Sarah)")
    for bad in (
        "tom ",
        "léa",
        "lea ",
        "sami",
        "tailles différentes",
        "le corps n'est pas",
        "tu as fait du bon travail",
        "l'histoire est finie",
        "capitaine",
        "plic",
        "volet jaune",
        "on va apprendre",
        "voici le geste",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


OBJ = {
    1: {
        "lab": "le gobelet",
        "cap": "Le gobelet",
        "ans": "gobelet",
        "acc": "gobelet | le gobelet | d'abord le gobelet | le gobelet d'abord",
        "retry": "Sarah prend le gobelet d'abord.",
    },
    2: {
        "lab": "la pelle",
        "cap": "La pelle",
        "ans": "pelle",
        "acc": "pelle | la pelle | d'abord la pelle | la pelle d'abord",
        "retry": "Sarah prend la pelle d'abord.",
    },
    3: {
        "lab": "le moulin",
        "cap": "Le moulin",
        "ans": "moulin",
        "acc": "moulin | le moulin | d'abord le moulin | le moulin d'abord",
        "retry": "Sarah prend le moulin d'abord.",
    },
}

T3_LABS = {
    1: ("la main de Sarah", "le sentier bas", "la serviette"),
    2: ("le trou bas", "un bord d'algues", "le sable sec"),
    3: ("le gobelet tendu", "le bord étroit", "le pont de pelle"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah prend le gobelet, tout froid.",
            "enfant-f|L'écume ira là-dedans.",
            "maman|Tiens-le près du seau.",
            "narrateur|Le plastique sent encore le sable.",
            "papa|La pelle aussi, dans le sac.",
            "narrateur|Maman glisse le moulin à côté.",
            "narrateur|Le sac est prêt, maintenant.",
            "enfant-f|Victorino, on va au sel.",
            "narrateur|Le seau tape contre son genou.",
            "enfant-m|J'arrive, Sarah.",
            "enfant-f|On attrape l'écume, d'accord ?",
            "papa|Le gobelet d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah soulève la pelle, un peu lourde.",
            "enfant-f|On lève l'écume avec.",
            "papa|Le bord est encore humide.",
            "narrateur|Un grain tombe, toc, sur le bois.",
            "maman|Le gobelet, ensuite, près du sac.",
            "narrateur|Papa pose le moulin sur le linge.",
            "narrateur|Le sac se ferme, tout doux.",
            "enfant-f|Victorino, viens jouer.",
            "narrateur|Ses pas sont courts, sur les lames.",
            "enfant-m|J'apporte le seau.",
            "enfant-f|On prend le sel des vagues.",
            "maman|La pelle d'abord, elle est prête.",
        )
    return L(
        "narrateur|Sarah tourne le moulin, un cran.",
        "enfant-f|Il va cracher le sel.",
        "maman|Pas trop vite, encore.",
        "narrateur|Les pales sentent l'eau séchée.",
        "papa|Gobelet et pelle, avec vous.",
        "narrateur|Il les glisse près des tongs.",
        "narrateur|Le sac cliquette, puis se tait.",
        "enfant-f|Victorino, on y va.",
        "narrateur|Le seau frotte encore son genou.",
        "enfant-m|Moi, je tiens l'anse.",
        "enfant-f|Le moulin va nous asperger.",
        "papa|Le moulin d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le gobelet tient au fond du seau.",
            "enfant-m|On va le remplir d'écume.",
            "enfant-f|Le sel ira sur nos lèvres.",
            "maman|Le sable vous attend.",
            "papa|On sort par les dunes ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La pelle repose contre le sac.",
            "enfant-f|On soulèvera le ruban blanc.",
            "enfant-m|Puis on goûte, d'accord ?",
            "papa|Le vent sent déjà l'eau.",
            "maman|Vos pieds, dans les tongs ?",
            "enfant-m|Oui, maman.",
        )
    return L(
        "narrateur|Le moulin dépasse du sac, tout croche.",
        "enfant-f|Il va nous souffler le sel.",
        "enfant-m|Sur le nez, peut-être.",
        "maman|La mer claque, tout près.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le sable chaud tremble un peu.",
        "narrateur|À gauche, une dune ronde.",
        "narrateur|Devant, une barrière d'algues.",
        "narrateur|À droite, un ruisseau salé.",
        "papa|Vous jouez où, tous les deux ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = {
            1: "narrateur|Le gobelet cliquette contre le seau.",
            2: "narrateur|La pelle trace une ligne dans le sable.",
            3: "narrateur|Le moulin tourne, un cran, dans l'air.",
        }[t1]
        return L(
            lead,
            "narrateur|La dune sent le thym et le sel.",
            "enfant-f|L'écume est derrière, je l'entends.",
            "enfant-m|Je veux y aller.",
            "narrateur|Victorino lève le genou, tout haut.",
            "narrateur|Le sable redescend sous son pied.",
            "enfant-m|Mes jambes n'y arrivent pas.",
            "papa|Le sable recule sous toi.",
            "narrateur|Sarah pose le pied, plus haut.",
            "enfant-f|On y va à tes pas ?",
            "maman|Vous trouvez comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Sarah pose le gobelet, le temps d'un regard.",
            2: "narrateur|Sarah plante la pelle, le temps d'un regard.",
            3: "narrateur|Sarah pose le moulin, le temps d'un regard.",
        }[t1]
        return L(
            lead,
            "narrateur|Les algues sentent fort, tout mouillé.",
            "enfant-f|Je passe par-dessus.",
            "narrateur|Sarah enjambe, un pied, puis l'autre.",
            "narrateur|Victorino lève la jambe.",
            "enfant-m|Je n'y arrive pas.",
            "papa|Le tapis vert est trop épais.",
            "narrateur|Une crevette saute, tout petit.",
            "enfant-f|On passe comment, alors ?",
            "maman|Vous cherchez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Le gobelet penche vers l'eau claire.",
        2: "narrateur|La pelle frôle le filet d'eau.",
        3: "narrateur|Le moulin tremble au-dessus du filet.",
    }[t1]
    return L(
        lead,
        "narrateur|Le ruisseau salé coupe le sable.",
        "enfant-f|L'écume est de l'autre côté.",
        "narrateur|Sarah enjambe, sans se presser.",
        "narrateur|Victorino recule, l'eau trop large.",
        "enfant-m|Mes pas sont trop courts.",
        "papa|Une feuille-bateau passe, toute seule.",
        "enfant-f|On reste ensemble, d'accord ?",
        "maman|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La dune reste trop pentue.",
            "papa|La main de Sarah, le sentier, ou la serviette ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les algues barrent encore le sable.",
            "maman|Le trou, un bord, ou le sable sec ?",
        )
    return L(
        "narrateur|Le ruisseau salé reste trop large.",
        "papa|Le gobelet, le bord étroit, ou le pont ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        hip = {
            1: "narrateur|Le gobelet tape contre sa hanche.",
            2: "narrateur|La pelle tape contre sa hanche.",
            3: "narrateur|Le moulin tape contre sa hanche.",
        }[t1]
        return L(
            "enfant-f|Prends ma main.",
            "enfant-m|Oui, fort.",
            "narrateur|Sarah marche un petit pas.",
            "narrateur|Victorino pose le même pas.",
            hip,
            "narrateur|Le sommet arrive sous leurs genoux.",
            "enfant-f|L'écume est blanche.",
            "enfant-m|On y est.",
            "papa|Vous avez gravi à son rythme.",
            "narrateur|Un grain salé brille sur le pouce.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le gobelet attend au creux du seau.",
            2: "narrateur|La pelle attend, un peu sablée.",
            3: "narrateur|Le moulin attend, un cran figé.",
        }[t1]
        return L(
            "enfant-m|On tourne, tout bas.",
            "enfant-f|Oui, le petit chemin.",
            "narrateur|Des traces étroites longent la dune.",
            "narrateur|Sarah se baisse pour passer.",
            "narrateur|Victorino marche droit, à sa hauteur.",
            wait,
            "enfant-m|L'écume, je la vois.",
            "enfant-f|Elle nous a attendus.",
            "maman|Le long chemin était à vos pieds.",
            "papa|Vous n'avez pas forcé la pente.",
        )
    if t2 == 1 and t3 == 3:
        drag = {
            1: "narrateur|Le seau et le gobelet glissent derrière.",
            2: "narrateur|La pelle glisse à côté, tout plat.",
            3: "narrateur|Le moulin glisse, pales vers le ciel.",
        }[t1]
        return L(
            "enfant-f|On met la serviette.",
            "enfant-m|Comme un tapis.",
            "narrateur|Ils tirent le tissu sur le sable.",
            "narrateur|Ça tient, un peu mou.",
            "narrateur|Ils montent à quatre pattes, tout doux.",
            drag,
            "enfant-f|On est au même endroit.",
            "enfant-m|Moi aussi, j'arrive.",
            "papa|Vos genoux ont fait le chemin.",
            "narrateur|L'écume claque, juste derrière.",
        )
    if t2 == 2 and t3 == 1:
        scoop = {
            1: "narrateur|Sarah glisse le gobelet dans le trou.",
            2: "narrateur|Sarah glisse la pelle dans le trou.",
            3: "narrateur|Sarah glisse le moulin près du trou.",
        }[t1]
        return L(
            "enfant-m|Là, un trou, tout bas.",
            "narrateur|Il est à hauteur de ses genoux.",
            "enfant-f|Toi tu vois mieux, plus près.",
            "narrateur|Victorino écarte les brins, tout doux.",
            scoop,
            "narrateur|L'écume attend, de l'autre côté.",
            "enfant-m|Passe, Sarah.",
            "enfant-f|Toi d'abord, c'est ton trou.",
            "papa|Tu as trouvé le passage.",
            "maman|Sarah s'est baissée, comme toi.",
        )
    if t2 == 2 and t3 == 2:
        lift = {
            1: "narrateur|Le gobelet reste au sec, contre le seau.",
            2: "narrateur|La pelle soulève encore un brin.",
            3: "narrateur|Le moulin sert de coin, tout léger.",
        }[t1]
        return L(
            "enfant-f|On lève un bord, tous les deux.",
            "enfant-m|Moi le bas, toi le haut.",
            "narrateur|Sarah prend les algues lourdes.",
            "narrateur|Victorino tient le bord, près du sable.",
            lift,
            "narrateur|Un couloir s'ouvre, assez bas.",
            "enfant-m|Je passe !",
            "enfant-f|Moi aussi, je me baisse.",
            "papa|Chacun a tenu sa part.",
            "narrateur|L'écume cliquette, tout près.",
        )
    if t2 == 2 and t3 == 3:
        dry = {
            1: "narrateur|Le gobelet penche, déjà plein d'air.",
            2: "narrateur|La pelle porte un peu de sable sec.",
            3: "narrateur|Le moulin tourne dans l'air chaud.",
        }[t1]
        return L(
            "enfant-f|On tourne par le sable sec.",
            "enfant-m|Sans enjamber.",
            "narrateur|Ils longent la barrière, pieds chauds.",
            "narrateur|Sarah ralentit pour ses pas.",
            dry,
            "narrateur|Au bout, l'écume les rejoint.",
            "enfant-m|Elle est venue.",
            "enfant-f|On n'a pas forcé les algues.",
            "maman|Le tour était plus long, plus simple.",
            "papa|Vos tongs sont pleines de soleil.",
        )
    if t2 == 3 and t3 == 1:
        hold = {
            1: "narrateur|Sarah tend le gobelet, bras longs.",
            2: "narrateur|Sarah tend la pelle, le gobelet au bout.",
            3: "narrateur|Sarah tend le moulin, le gobelet au bout.",
        }[t1]
        return L(
            "enfant-f|On reste ici.",
            "enfant-m|Tu prends l'écume, de l'autre bord ?",
            hold,
            "narrateur|Victorino tient le seau, prêt.",
            "narrateur|Le blanc glisse, glouglou, dans le plastique.",
            "enfant-m|Je la vois, dans le fond.",
            "enfant-f|On n'a pas traversé.",
            "papa|Vos bras ont fait le pont.",
            "maman|L'eau est restée à sa place.",
            "narrateur|Un grain tremble au bord du gobelet.",
        )
    if t2 == 3 and t3 == 2:
        walk = {
            1: "narrateur|Le gobelet pend, au rythme des pas.",
            2: "narrateur|La pelle sert de bâton, tout léger.",
            3: "narrateur|Le moulin se tait, le long du filet.",
        }[t1]
        return L(
            "enfant-m|On marche jusqu'au bord étroit.",
            "enfant-f|Oui, où tes pieds passent.",
            "narrateur|Le ruisseau se fait mince, plus loin.",
            "narrateur|Sarah compte les pas de Victorino.",
            walk,
            "narrateur|Ils enjambent, l'un après l'autre.",
            "enfant-m|Mes pieds suffisent, ici.",
            "enfant-f|Les miens aussi, tout près.",
            "papa|Vous avez cherché votre largeur.",
            "narrateur|L'écume les attend, déjà là.",
        )
    bridge = {
        1: "narrateur|Le gobelet traverse, posé sur le bois.",
        2: "narrateur|La pelle fait pont, le gobelet dessus.",
        3: "narrateur|Le moulin attend, le temps du pont.",
    }[t1]
    return L(
        "enfant-f|On pose la pelle, en pont.",
        "papa|J'attends au bord.",
        "narrateur|Le métal pose une bande étroite.",
        "narrateur|Victorino passe, un pied, puis l'autre.",
        "narrateur|Sarah passe après, tout léger.",
        bridge,
        "enfant-m|On est de l'autre côté.",
        "enfant-f|L'écume, elle est à nous.",
        "maman|Vous avez marché l'un après l'autre.",
        "papa|Le filet d'eau reste en dessous.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = {
        1: "narrateur|Le gobelet sèche près des tongs.",
        2: "narrateur|La pelle repose, un peu de sable au bord.",
        3: "narrateur|Le moulin garde un grain dans une pale.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils redescendent, la main encore chaude.",
            "enfant-f|Le sel, il est là.",
            "narrateur|Sarah passe la langue, tout lentement.",
            "enfant-f|Ça pique, pour de vrai.",
            "enfant-m|Moi aussi !",
            "papa|Vous avez gravi à ses pas.",
            "maman|La dune a gardé vos traces, collées.",
            coda,
            "narrateur|Un crabe rentre dans son trou.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le long chemin a rempli leurs tongs.",
            "enfant-m|On a tourné, et l'écume était là.",
            "enfant-f|Je goûte.",
            "narrateur|Le grain pique le milieu de sa lèvre.",
            "papa|Le sentier bas vous a suffi.",
            "maman|Secouez le sable, tout doux.",
            coda,
            "enfant-m|Ça pique moi aussi.",
            "narrateur|La cabane sent encore le thym.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La serviette est pleine de dune.",
            "enfant-f|On a monté à genoux.",
            "enfant-m|Au même endroit, tous les deux.",
            "narrateur|Sarah lèche un trait blanc, sur le pouce.",
            "enfant-f|Le sel est chaud, presque.",
            "papa|Vos genoux ont fait le travail.",
            "maman|On étend le tissu, au soleil.",
            coda,
            "narrateur|L'écume sèche déjà sur le bois.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Leurs genoux sentent encore l'algue.",
            "enfant-m|C'était mon trou.",
            "enfant-f|Tu l'as vu, plus près du sable.",
            "narrateur|Elle goûte, les yeux un peu plissés.",
            "enfant-f|Ça pique, et ça sent la mer.",
            "papa|Tu as trouvé le passage.",
            "maman|Lavez les mains, tout doux.",
            coda,
            "narrateur|Une crevette n'est plus là.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Leurs bras sentent le tapis vert.",
            "enfant-f|Toi le bas, moi le haut.",
            "enfant-m|On a ouvert le couloir.",
            "narrateur|Sarah pose l'écume sur sa lèvre.",
            "enfant-m|Et moi, un peu, s'il te plaît.",
            "papa|Chacun a tenu sa part.",
            "maman|L'iode reste dans vos cheveux.",
            coda,
            "narrateur|Les algues se recouchent, tout lentement.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les tongs rendent le sable chaud.",
            "enfant-f|On n'a pas forcé les algues.",
            "enfant-m|Le tour était long, facile.",
            "narrateur|Elle lèche un grain, déjà sec.",
            "enfant-f|Il colle, puis il fond.",
            "papa|Vos tongs sont pleines de soleil.",
            "maman|Buvez un peu d'eau, maintenant.",
            coda,
            "narrateur|La barrière verte reste derrière eux.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le gobelet a encore une goutte blanche.",
            "enfant-f|On n'a pas traversé.",
            "enfant-m|Tes bras ont fait le pont.",
            "narrateur|Sarah boit un tout petit trait.",
            "enfant-f|Ça pique les lèvres, fort.",
            "papa|Vos bras ont suffi.",
            "maman|Le ruisseau n'a pas bougé.",
            coda,
            "narrateur|La feuille-bateau a disparu, plus loin.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Leurs pieds sont mouillés, juste assez.",
            "enfant-m|Mes pas suffisaient, au bord étroit.",
            "enfant-f|J'ai compté tes pas.",
            "narrateur|Elle goûte, puis elle rit, tout petit.",
            "enfant-f|Le sel est là, promis.",
            "papa|Vous avez cherché votre largeur.",
            "maman|Essuie tes orteils, sur le paillasson.",
            coda,
            "narrateur|Le filet d'eau redevient calme.",
        )
    return L(
        "narrateur|Un peu d'eau reste sous la pelle.",
        "enfant-m|On a marché l'un après l'autre.",
        "enfant-f|L'écume est à nous.",
        "narrateur|Sarah pose le grain sur sa lèvre.",
        "enfant-m|Moi aussi, un peu.",
        "papa|Le filet d'eau est resté en dessous.",
        "maman|Rangez la pelle, elle goutte.",
        coda,
        "narrateur|Le sel brille, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "mer"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La vitre de la cabane a des grains blancs.",
        "narrateur|Un chapeau de paille goutte sur le clou.",
        "maman|Tu sens l'air, Sarah ?",
        "enfant-f|Ça pique, un peu.",
        "papa|C'est le sel de la mer.",
        "narrateur|Un trou de crabe tient du sable mouillé.",
        "narrateur|La serviette rayée attend près des tongs.",
        "narrateur|En ce moment, Sarah passe la langue.",
        "enfant-f|Il reste un grain, d'hier.",
        "enfant-f|Je veux le sel des vagues.",
        "enfant-f|Avec un vrai jeu, au bord.",
        "narrateur|Des petits pas sonnent sur le bois.",
        "narrateur|Victorino arrive, le seau contre le genou.",
        "enfant-m|On attrape l'écume ?",
        "enfant-f|Oui, sur nos lèvres.",
        "papa|Merci, tu as fermé la porte.",
        "maman|On prépare les affaires, alors ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le sac attend près des tongs.",
        "narrateur|Le gobelet, la pelle, et le moulin.",
        "maman|Tu prends quoi d'abord, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le gobelet", "la pelle", "le moulin")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        sons[p] = "mer"
        s[f"{p}_Q0001"] = L(
            f"narrateur|Sarah a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la dune", "les algues", "le ruisseau")

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            sons[sp] = "mer"
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                sons[f"{sp}_T0003_P000{t3}"] = "mer"
                fin_id = f"{sp}_T0003_P000{t3}_F0001"
                s[fin_id] = fin_scene(t1, t2, t3)
                sons[fin_id] = "mer,oiseau"

    write_tree(s, extras, sons)
    relecture(
        SID,
        "Le sel sur les lèvres de Sarah",
        "Cabane salée, chapeau qui goutte. Sarah veut le sel des vagues "
        "sur les lèvres, avec un jeu. Victorino arrive, seau contre le genou. "
        "T1 = gobelet / pelle / moulin (les trois partent). "
        "T2 = dune trop pentue / algues trop hautes / ruisseau trop large. "
        "T3 = neuf résolutions (main, sentier, serviette ; trou, bord levé, "
        "sable sec ; gobelet tendu, bord étroit, pont de pelle). "
        "La leçon (pas les mêmes pas, on joue quand même) se vit dans les "
        "genoux, les enjambées et le rythme. Fin : le grain pique.",
        "N2 ≤ 15. Sara, Tom/Léa/Sami, slogans tailles/corps, « bon travail » "
        "jetés. Un merci de papa (porte fermée). Pas de calque AUT-001 "
        "(capitaine, plic, volet jaune). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
