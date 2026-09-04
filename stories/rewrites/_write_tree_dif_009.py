#!/usr/bin/env python3
"""TREE-DIF-009 — petit train d'Amir, rails qui chantent. DIF.COR.001 implicite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-009"
N2 = LIMITS["N2"]


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


def write_tree(
    scripts: dict[str, list[str]],
    sons: dict[str, str],
    extras: dict[str, dict],
) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind == "passage_question" else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = (
        "Les rails du grand train chantent sous le wagon. Amir veut faire voyager "
        "son petit train de bois, avec Nina. Jaune, bleu ou rouge colore la voie. "
        "Un pont, une gare ou un tunnel change le trajet. Un grelot, une plume ou "
        "un galet part avec eux. Nina atteint le haut, Amir le bas. Le petit train arrive."
    )
    out["title"] = "Le petit train d'Amir, sous les rails qui chantent"
    out["characters"] = "Amir, Nina, papa, maman"
    out["setting"] = "dans le wagon, rails de bois près du plancher"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID} en ce moment: {blob.count('en ce moment')}")
    for bad in (
        "kenzo",
        "tom ",
        "léa",
        "lea ",
        "sami",
        "tailles sont différentes",
        "on va apprendre",
        "bon travail",
        "l'histoire est finie",
        "jouer ensemble ?",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan/prénom: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


RAIL = {
    1: dict(
        lab="les rails jaunes",
        coul="jaunes",
        adj="jaune",
        ou="sous les sièges",
        lum="l'or de l'allée",
        lieu="le tunnel bas",
        sol="le plancher",
    ),
    2: dict(
        lab="les rails bleus",
        coul="bleus",
        adj="bleu",
        ou="le long de la vitre",
        lum="le ciel pâle",
        lieu="la tablette",
        sol="la tablette",
    ),
    3: dict(
        lab="les rails rouges",
        coul="rouges",
        adj="rouge",
        ou="sur la valise",
        lum="le tissu rêche",
        lieu="la pente de tissu",
        sol="le tapis",
    ),
}

PIECE = {
    1: dict(lab="le pont", ou="sur le pont", de="du pont"),
    2: dict(lab="la gare", ou="à la gare", de="de la gare"),
    3: dict(lab="le tunnel", ou="dans le tunnel", de="du tunnel"),
}

CARGO = {
    1: dict(lab="le grelot", un="un grelot", de="du grelot"),
    2: dict(lab="la plume", un="une plume", de="de la plume"),
    3: dict(lab="le galet", un="un galet", de="du galet"),
}


def t1_pass(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "narrateur|Amir glisse les rails jaunes sous les sièges.",
                "narrateur|L'ombre sent encore le tissu chaud.",
                "narrateur|Une lumière dorée arrive de l'allée.",
                "enfant-m|C'est un tunnel, tout bas.",
                "papa|Tes mains passent, tout près du plancher.",
                "narrateur|Nina plie un genou, plus haut que lui.",
                "enfant-f|Moi, je tiens le bout, ici.",
                "narrateur|Le bois jaune claque, pièce après pièce.",
                "enfant-m|Le petit train va dessous.",
                "maman|Il va loin, comme le grand.",
                "narrateur|Un grain de poussière brille, tout or.",
                "enfant-m|Les rails sont jaunes.",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Amir aligne les rails bleus contre la vitre.",
                "narrateur|Le ciel colle au verre, tout pâle.",
                "narrateur|Une goutte de pluie glisse dehors, lente.",
                "enfant-m|On va vers les nuages.",
                "maman|La tablette vibre encore, tout doux.",
                "narrateur|Nina pose un rail plus haut, au rebord.",
                "enfant-f|Ma main arrive jusqu'ici.",
                "enfant-m|La mienne reste plus bas.",
                "papa|Vous faites la voie, tous les deux.",
                "narrateur|Le bois bleu sent la cire, un peu.",
                "enfant-m|Les rails sont bleus.",
            ]
        )
    return vet(
        [
            "narrateur|Amir monte les rails rouges sur la valise.",
            "narrateur|Le tissu est rêche, encore un peu chaud.",
            "narrateur|La fermeture fait un petit zzz.",
            "enfant-m|C'est une montagne.",
            "papa|Le petit train grimpe, alors ?",
            "enfant-m|Oui.",
            "narrateur|Nina tient le haut, près de la poignée.",
            "enfant-f|Je pose le dernier rail.",
            "narrateur|Amir cale le bas, contre le tapis.",
            "maman|Il va monter, puis redescendre.",
            "enfant-m|Les rails sont rouges.",
        ]
    )


def t1_q(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "narrateur|Le bois a pris la lumière dorée.",
                "papa|De quelle couleur sont les rails ?",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Le bois a pris le ciel de la vitre.",
                "maman|De quelle couleur sont les rails ?",
            ]
        )
    return vet(
        [
            "narrateur|Le bois a pris le rouge du tissu.",
            "papa|De quelle couleur sont les rails ?",
        ]
    )


def t1_c(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "enfant-m|Jaune.",
                "papa|Oui.",
                "narrateur|L'or de l'allée reste sur le bois.",
                "maman|Le tunnel est prêt, sous les sièges.",
                "enfant-f|J'ai le bout, encore.",
                "papa|Merci, Amir.",
                "narrateur|La locomotive attend au bord de l'ombre.",
            ]
        )
    if i == 2:
        return vet(
            [
                "enfant-m|Bleu.",
                "maman|Oui.",
                "narrateur|Le ciel pâle reste collé au verre.",
                "papa|La voie suit la vitre, tout droit.",
                "enfant-f|Je garde le rebord.",
                "maman|Merci, Amir.",
                "narrateur|La locomotive attend contre la goutte.",
            ]
        )
    return vet(
        [
            "enfant-m|Rouge.",
            "papa|Oui.",
            "narrateur|Le tissu rêche garde sa pente.",
            "maman|La montagne de valise est prête.",
            "enfant-f|Je tiens la poignée.",
            "papa|Merci, Amir.",
            "narrateur|La locomotive attend au pied du tapis.",
        ]
    )


def t2_pass(i: int, j: int) -> list[str]:
    if (i, j) == (1, 1):
        return vet(
            [
                "narrateur|Amir pose un pont de bois au-dessus de l'ombre.",
                "narrateur|Les pieds du pont touchent le plancher jaune.",
                "enfant-m|Le haut est trop loin.",
                "papa|La planche est un peu haute.",
                "narrateur|Nina tend les siens, jusqu'à la planche.",
                "enfant-f|Je tiens le milieu, moi.",
                "enfant-m|Moi, les pieds.",
                "maman|Vous le tenez, chacun un bout.",
                "narrateur|Le pont tremble un peu, puis tient.",
            ]
        )
    if (i, j) == (1, 2):
        return vet(
            [
                "narrateur|Amir pose une petite gare, à la sortie de l'ombre.",
                "narrateur|Le toit arrive trop haut, pour ses doigts.",
                "enfant-m|Je n'accroche pas le toit.",
                "maman|Nina est plus près du haut.",
                "narrateur|Elle pose le toit, tout doux, dans l'or.",
                "enfant-f|Toi, tu ouvres la porte.",
                "enfant-m|La porte est plus bas.",
                "papa|Chacun sa hauteur, et la gare tient.",
                "narrateur|Un rectangle de lumière dorée entre dedans.",
            ]
        )
    if (i, j) == (1, 3):
        return vet(
            [
                "narrateur|Amir glisse un carton sous les sièges, en tunnel.",
                "narrateur|L'intérieur est sombre, un peu poussiéreux.",
                "enfant-m|Je vois dessous, moi.",
                "papa|Tes yeux sont tout près du plancher.",
                "narrateur|Le bras de Nina traverse le carton, plus loin.",
                "enfant-f|Je sors de l'autre côté.",
                "enfant-m|Pousse, je regarde.",
                "maman|Vous tenez les deux bouts du noir.",
                "narrateur|Un rond jaune attend à la sortie.",
            ]
        )
    if (i, j) == (2, 1):
        return vet(
            [
                "narrateur|Amir dresse un pont vers la vitre bleue.",
                "narrateur|Le haut frôle le rebord, trop haut pour lui.",
                "enfant-m|Ça penche.",
                "maman|Nina peut caler le haut, contre le verre.",
                "narrateur|Elle appuie la planche, tout près du ciel.",
                "enfant-f|Tiens le bas, sur la tablette.",
                "enfant-m|Je le cale.",
                "papa|Le pont relie le bois et la vitre.",
                "narrateur|Une goutte, dehors, suit la pente.",
            ]
        )
    if (i, j) == (2, 2):
        return vet(
            [
                "narrateur|Amir pose une gare sur la tablette, face aux champs.",
                "narrateur|Le petit drapeau refuse de tenir, trop haut.",
                "enfant-m|Il retombe.",
                "papa|Le toit est à la hauteur de Nina.",
                "narrateur|Elle pique le bâton, au faîte bleu.",
                "enfant-f|Ouvre la porte, Amir.",
                "enfant-m|Elle coulisse, tout bas.",
                "maman|La gare regarde les champs, maintenant.",
                "narrateur|Un arbre défile, tout lent, derrière le verre.",
            ]
        )
    if (i, j) == (2, 3):
        return vet(
            [
                "narrateur|Amir plie un magazine, en tunnel, le long du verre.",
                "narrateur|L'ombre bleue traverse les pages, tout pâle.",
                "enfant-m|Je regarde par le trou.",
                "maman|Nina tient le haut, pour qu'il ne tombe pas.",
                "narrateur|Ses doigts pincent le papier, plus haut.",
                "enfant-f|Pousse, je garde l'arche.",
                "enfant-m|J'envoie la loco.",
                "papa|Vous tenez le passage, tous les deux.",
                "narrateur|Le ciel pâle allume la sortie.",
            ]
        )
    if (i, j) == (3, 1):
        return vet(
            [
                "narrateur|Amir pose un pont sur la pente de la valise.",
                "narrateur|Le haut touche presque la poignée rouge.",
                "enfant-m|Je n'y arrive pas.",
                "papa|Nina est déjà près de la poignée.",
                "narrateur|Elle cale le haut, contre le métal.",
                "enfant-f|Toi, le pied, sur le tapis.",
                "enfant-m|Je le sers.",
                "maman|La montagne a un pont, maintenant.",
                "narrateur|Le tissu rêche ne glisse plus.",
            ]
        )
    if (i, j) == (3, 2):
        return vet(
            [
                "narrateur|Amir installe une gare tout en haut de la valise.",
                "narrateur|Le toit glisse vers la fermeture, trop loin.",
                "enfant-m|Il part.",
                "maman|Nina rattrape le toit, près du zzz.",
                "narrateur|Elle l'assoit, contre la poignée rouge.",
                "enfant-f|La porte, c'est pour toi.",
                "enfant-m|Je l'ouvre, plus bas.",
                "papa|Le quai regarde la descente.",
                "narrateur|Le tapis attend, au pied de la pente.",
            ]
        )
    return vet(
        [
            "narrateur|Amir enfile une chaussette en tunnel, sur la valise.",
            "narrateur|Le tissu rouge avale la locomotive, tout doux.",
            "enfant-m|Je ne vois plus le bout.",
            "papa|Le bras de Nina est plus long, lui.",
            "narrateur|Elle ouvre la sortie, près de la poignée.",
            "enfant-f|Pousse, je l'attends.",
            "enfant-m|J'envoie.",
            "maman|Vous tenez l'entrée et la sortie.",
            "narrateur|Un bout de chaussette reste ouvert, tout rouge.",
        ]
    )


def t3_pass(i: int, j: int, k: int) -> list[str]:
    r = RAIL[i]
    if (j, k) == (1, 1):
        return vet(
            [
                "enfant-m|Le grelot va sous le pont.",
                "narrateur|Nina l'accroche, plus haut, à la planche.",
                "enfant-f|Écoute, en bas.",
                "narrateur|Amir colle l'oreille près du bois.",
                f"papa|Il va tinter, {r['ou']}.",
                "narrateur|La locomotive passe, et le grelot répond.",
                "enfant-m|Il chante, comme les rails.",
            ]
        )
    if (j, k) == (1, 2):
        return vet(
            [
                "enfant-m|La plume, sur le pont.",
                "narrateur|Le wagon secoue, tout doux, et elle vole.",
                "enfant-f|Je l'attrape, en haut.",
                "narrateur|Amir retient les pieds du pont, tout bas.",
                f"maman|Vous l'avez, {r['ou']}.",
                "narrateur|Nina la pose à nouveau, au milieu.",
                "enfant-m|Elle reste, cette fois.",
            ]
        )
    if (j, k) == (1, 3):
        return vet(
            [
                "enfant-m|Le galet cale le pont.",
                "narrateur|Amir le pousse au pied, contre le bois.",
                "enfant-f|Il est lourd.",
                "narrateur|Nina appuie encore le haut, pour aider.",
                f"papa|Le pont ne saute plus, {r['ou']}.",
                "narrateur|Un toc, puis plus rien.",
                "enfant-m|On peut passer.",
            ]
        )
    if (j, k) == (2, 1):
        return vet(
            [
                "enfant-m|Le grelot, à la gare.",
                "narrateur|Nina le pose sur le toit, tout près.",
                "enfant-f|Toi, tu sonnes, quand ça arrive.",
                "narrateur|Amir tend la main vers la porte, plus bas.",
                f"maman|{r['lum'].capitalize()} touche le grelot.",
                "narrateur|La locomotive entre, et ça tinte.",
                "enfant-m|La gare a parlé.",
            ]
        )
    if (j, k) == (2, 2):
        return vet(
            [
                "enfant-m|La plume, c'est le drapeau.",
                "narrateur|Nina la pique au faîte, là où il n'atteint pas.",
                "enfant-f|Elle flotte.",
                "narrateur|Amir ouvre la porte, pour le quai.",
                f"papa|Le vent {r['adj']} la fait trembler.",
                "narrateur|La locomotive s'arrête dessous, tout fière.",
                "enfant-m|On est arrivés.",
            ]
        )
    if (j, k) == (2, 3):
        return vet(
            [
                "enfant-m|Le galet, pour arrêter.",
                "narrateur|Amir le pose au quai, tout près du sol.",
                "enfant-f|Moi, je garde le toit.",
                "narrateur|La locomotive roule, puis touche la pierre.",
                f"maman|Elle s'arrête {r['ou']}.",
                "papa|Le galet l'a retenue.",
                "enfant-m|Elle est à la gare.",
            ]
        )
    if (j, k) == (3, 1):
        return vet(
            [
                "enfant-m|Le grelot, dans le noir.",
                "narrateur|Amir le glisse à l'entrée, tout bas.",
                "enfant-f|Je l'écoute, de l'autre côté.",
                "narrateur|Le tintement traverse, sans qu'on voie.",
                f"papa|Il chante {r['ou']}, au milieu.",
                "narrateur|Puis la locomotive sort, et le grelot aussi.",
                "enfant-m|Je l'ai entendu avant.",
            ]
        )
    if (j, k) == (3, 2):
        return vet(
            [
                "enfant-m|La plume passe d'abord.",
                "narrateur|Amir la pousse à l'entrée, tout doux.",
                "enfant-f|Une pointe blanche, chez moi.",
                "narrateur|Nina la tire, de l'autre bout, plus haut.",
                f"maman|{r['lum'].capitalize()} la rend toute claire.",
                "narrateur|La locomotive suit, juste derrière.",
                "enfant-m|Elle a montré le chemin.",
            ]
        )
    return vet(
        [
            "enfant-m|Le galet, tout lent.",
            "narrateur|Amir le pousse, il roule à peine.",
            "enfant-f|J'attends la sortie.",
            "narrateur|Nina reste à genoux, du côté clair.",
            f"papa|Il met du temps, {r['ou']}.",
            "narrateur|Un bruit sourd, puis la pierre paraît.",
            "enfant-m|On a attendu ensemble.",
        ]
    )


FIN_IMG = {
    (1, 1, 1): "Le grelot tinte encore, sous le pont d'or.",
    (1, 1, 2): "La plume repose au milieu du pont jaune.",
    (1, 1, 3): "Le galet cale encore les pieds du pont.",
    (1, 2, 1): "Le grelot de la gare s'est tu, dans l'or.",
    (1, 2, 2): "La plume-drapeau ne bouge plus, sur le toit.",
    (1, 2, 3): "Le galet reste au quai, près de la porte basse.",
    (1, 3, 1): "Le grelot s'est tu, au fond du carton.",
    (1, 3, 2): "La plume blanche repose à la sortie jaune.",
    (1, 3, 3): "Le galet a fini le noir, tout lent.",
    (2, 1, 1): "Le grelot répond encore à la vitre bleue.",
    (2, 1, 2): "La plume ne vole plus, sur le pont de verre.",
    (2, 1, 3): "Le galet tient le bas, contre la tablette.",
    (2, 2, 1): "Le grelot de gare s'est tu, face aux champs.",
    (2, 2, 2): "La plume flotte encore, tout bleu, au faîte.",
    (2, 2, 3): "Le galet garde le quai, près de la porte.",
    (2, 3, 1): "Le grelot s'est tu, dans le papier plié.",
    (2, 3, 2): "La plume blanche a montré la sortie pâle.",
    (2, 3, 3): "Le galet a traversé les pages, tout lent.",
    (3, 1, 1): "Le grelot tinte encore, sous le pont rouge.",
    (3, 1, 2): "La plume repose, au milieu de la pente.",
    (3, 1, 3): "Le galet cale le pont, contre le tissu.",
    (3, 2, 1): "Le grelot de la gare s'est tu, en haut.",
    (3, 2, 2): "La plume-drapeau ne bouge plus, près du zzz.",
    (3, 2, 3): "Le galet reste au quai, avant la descente.",
    (3, 3, 1): "Le grelot s'est tu, dans la chaussette.",
    (3, 3, 2): "La plume blanche a trouvé la poignée.",
    (3, 3, 3): "Le galet a fini le tissu, tout rouge.",
}

FIN_CODA = {
    (1, 1, 1): "Sous le plancher, le grand train répond, tout bas.",
    (1, 1, 2): "L'ombre sous les sièges redevient calme.",
    (1, 1, 3): "Le bois jaune ne claque plus, ou presque.",
    (1, 2, 1): "L'or de l'allée reste sur le petit toit.",
    (1, 2, 2): "Un rectangle de lumière dort dans la gare.",
    (1, 2, 3): "La porte basse reste ouverte, tout doux.",
    (1, 3, 1): "Le carton garde encore un peu de noir.",
    (1, 3, 2): "Le rond jaune de la sortie ne bouge plus.",
    (1, 3, 3): "Le plancher reprend son tic, tout loin.",
    (2, 1, 1): "Une goutte, dehors, a fini sa pente.",
    (2, 1, 2): "Le ciel pâle reste collé au verre.",
    (2, 1, 3): "La tablette vibre moins, maintenant.",
    (2, 2, 1): "Un arbre a fini de défiler, derrière.",
    (2, 2, 2): "Le champ reste vert, tout calme, au loin.",
    (2, 2, 3): "La porte coulisse encore, puis s'arrête.",
    (2, 3, 1): "Les pages du magazine ne tremblent plus.",
    (2, 3, 2): "Le ciel allume encore un peu la sortie.",
    (2, 3, 3): "Le papier plié garde sa forme d'arche.",
    (3, 1, 1): "La poignée froide ne bouge plus, en haut.",
    (3, 1, 2): "Le tissu rêche a fini de glisser.",
    (3, 1, 3): "Le tapis reprend les pieds du pont.",
    (3, 2, 1): "La fermeture ne fait plus zzz.",
    (3, 2, 2): "Le toit rouge reste contre la poignée.",
    (3, 2, 3): "La descente vers le tapis est vide, maintenant.",
    (3, 3, 1): "Un bout de chaussette reste ouvert, tout doux.",
    (3, 3, 2): "La poignée garde encore un fil blanc.",
    (3, 3, 3): "Le tissu rouge n'avale plus rien.",
}


def t3_fin(i: int, j: int, k: int) -> list[str]:
    r = RAIL[i]
    p = PIECE[j]
    img = FIN_IMG[(i, j, k)]
    coda = FIN_CODA[(i, j, k)]
    if k == 1:
        return vet(
            [
                f"narrateur|{img}",
                "enfant-m|Il a chanté avec le grand.",
                "enfant-f|On l'a fait, tous les deux.",
                f"narrateur|La locomotive repose {p['ou']}.",
                f"maman|{r['lab'].capitalize()} ont tenu.",
                "papa|Vous avez mené le voyage.",
                f"narrateur|{coda}",
            ]
        )
    if k == 2:
        return vet(
            [
                f"narrateur|{img}",
                "enfant-f|Elle est restée, cette fois.",
                "enfant-m|Le petit train est arrivé.",
                f"narrateur|Nina souffle, tout près {p['de']}.",
                "papa|Tu as tenu le haut, Nina.",
                "maman|Et toi le bas, Amir.",
                f"narrateur|{coda}",
            ]
        )
    return vet(
        [
            f"narrateur|{img}",
            "enfant-m|Il était lourd, pour moi.",
            "enfant-f|Pour moi aussi, un peu.",
            f"narrateur|Le galet reste {p['ou']}, tout rond.",
            "papa|Vous l'avez calé, chacun votre place.",
            "maman|Le petit train a fini sa route.",
            f"narrateur|{coda}",
        ]
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        [
            "narrateur|Sous le plancher, les joints font tic, puis tac.",
            "papa|Tu entends les rails, Amir ?",
            "enfant-m|Ils chantent.",
            "narrateur|Le wagon sent l'orange, encore un peu.",
            "narrateur|Un ticket dépasse de la poche de papa, sous le filet.",
            "maman|Le grand train va loin, ce matin.",
            "narrateur|Dehors, un champ passe, tout vert, derrière la vitre.",
            "narrateur|Nina pose un sac de toile, près des genoux.",
            "narrateur|Dedans, des rails de bois s'entrechoquent.",
            "enfant-m|Je veux un petit train, comme le grand.",
            "papa|Tu le poses où, alors ?",
            "enfant-m|Près des rails, avec Nina.",
            "maman|Les pièces sont dans le sac.",
            "narrateur|En ce moment, Amir sort une locomotive en bois.",
            "narrateur|Elle est petite, toute lisse.",
            "enfant-f|J'ai les rails.",
            "enfant-m|On fait une longue voie.",
            "papa|Jaune, bleu, ou rouge ?",
        ]
    )
    sons["CHK_T0000_P0000"] = ""

    s["CHK_T0001_P0000"] = vet(
        [
            "narrateur|Trois paquets de rails attendent dans le sac.",
            "narrateur|Les jaunes, les bleus, ou les rouges.",
            "maman|Lequel pose-t-on d'abord ?",
        ]
    )
    extras["CHK_T0001_P0000"] = t3(
        "les rails jaunes", "les rails bleus", "les rails rouges"
    )

    q_extra = {
        1: qf(
            "jaune",
            "jaune | jaunes | rails jaunes | or | dorée | doré",
            "Les rails sous les sièges sont jaunes.",
        ),
        2: qf(
            "bleu",
            "bleu | bleus | rails bleus | vitre | ciel",
            "Les rails le long de la vitre sont bleus.",
        ),
        3: qf(
            "rouge",
            "rouge | rouges | rails rouges | valise",
            "Les rails sur la valise sont rouges.",
        ),
    }

    for i, st in RAIL.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = t1_pass(i)
        sons[p] = ""
        s[f"{p}_Q0001"] = t1_q(i)
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = t1_c(i)
        s[f"{p}_T0002_P0000"] = vet(
            [
                f"narrateur|{st['lab'].capitalize()} attendent encore une pièce.",
                "maman|Le pont, la gare, ou le tunnel ?",
                "papa|Qu'est-ce qu'on ajoute ?",
            ]
        )
        extras[f"{p}_T0002_P0000"] = t3("le pont", "la gare", "le tunnel")
        for j, ge in PIECE.items():
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = t2_pass(i, j)
            s[f"{p2}_T0003_P0000"] = vet(
                [
                    f"narrateur|Près {ge['de']}, le sac a encore un objet.",
                    "papa|Le grelot, la plume, ou le galet ?",
                    "maman|Qu'est-ce qui part avec le train ?",
                ]
            )
            extras[f"{p2}_T0003_P0000"] = t3("le grelot", "la plume", "le galet")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = t3_pass(i, j, k)
                s[f"{p3}_F0001"] = t3_fin(i, j, k)

    write_tree(s, sons, extras)
    relecture(
        SID,
        "Le petit train d'Amir, sous les rails qui chantent",
        "rails du grand train, petit train de bois, T1 jaune/bleu/rouge, "
        "pont/gare/tunnel, grelot/plume/galet, Nina le haut Amir le bas",
        "avis2. Gabarit cuisine/jardin/chambre + Tom/Léa/Sami jeté. "
        "Kenzo hors troupe. Désir: jouer près des rails jouet, pas la leçon. "
        "Audio non cuit. 27 chemins non écoutés à voix haute.",
    )


if __name__ == "__main__":
    main()
