#!/usr/bin/env python3
"""TREE-DIF-008 — goutte du store, stand de Raphaël. DIF.BES.002 implicite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-008"
N3 = LIMITS["N3"]


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
        "Une goutte tombe du store. Raphaël veut tenir le stand et offrir un fruit. "
        "Le store colore l'étal. Il propose à Mila. Elle regarde, dit plus tard, ou prend. "
        "Il accepte. Le stand continue."
    )
    out["title"] = "La goutte du store et le stand de Raphaël"
    out["characters"] = "Raphaël, Mila, papa, maman"
    out["setting"] = "au marché, sous le store"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in ("kenzo", "tom ", "léa", "lea ", "sami"):
        if bad in blob:
            raise SystemExit(f"{SID} prénom hors troupe: {bad}")
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


STORE = {
    1: dict(
        lab="le store jaune",
        coul="jaune",
        fruit="le citron",
        fruits="les citrons",
        un="un citron",
        lum="une lumière dorée",
        goutte="une goutte jaune",
        odeur="le zeste",
        son="goutte",
    ),
    2: dict(
        lab="le store rouge",
        coul="rouge",
        fruit="la fraise",
        fruits="les fraises",
        un="une fraise",
        lum="une lumière rose",
        goutte="une goutte rouge",
        odeur="le sucre",
        son="goutte",
    ),
    3: dict(
        lab="le store vert",
        coul="vert",
        fruit="la poire",
        fruits="les poires",
        un="une poire",
        lum="une lumière verte",
        goutte="une goutte verte",
        odeur="le sucré",
        son="goutte",
    ),
}

GEST = {
    1: dict(lab="la balance", ou="sur la balance", de="de la balance", pres="près de la balance"),
    2: dict(lab="le sac", ou="dans le sac", de="du sac", pres="près du sac"),
    3: dict(lab="la caisse", ou="dans la caisse", de="de la caisse", pres="près de la caisse"),
}

REP = {
    1: dict(lab="je regarde", dit="Je regarde."),
    2: dict(lab="plus tard", dit="Plus tard."),
    3: dict(lab="je prends", dit="Je prends."),
}


def t1_pass(i: int) -> list[str]:
    st = STORE[i]
    if i == 1:
        return vet(
            [
                "narrateur|Raphaël glisse sous le store jaune.",
                "narrateur|La toile sent le soleil, un peu chaud.",
                f"narrateur|{st['lum'].capitalize()} pose des ronds sur les citrons.",
                "enfant-m|Ils sont tout jaunes.",
                "papa|Le zeste pique un peu le nez.",
                "narrateur|Une goutte jaune tremble au bord de la toile.",
                "narrateur|Puis elle tombe sur un citron.",
                "enfant-m|Il est mouillé.",
                "maman|Tu le poses, pour l'étal ?",
                "enfant-m|Oui.",
                "enfant-m|Je tiens le stand.",
                "narrateur|Mila arrive, les mains dans les poches.",
                "enfant-m|Tu viens au stand ?",
                "narrateur|Mila ne dit rien, encore.",
                "narrateur|Le citron brille, tout mouillé.",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Raphaël passe sous le store rouge.",
                "narrateur|La toile chauffe les joues, tout doux.",
                "narrateur|Une lumière rose colore les fraises.",
                "enfant-m|Elles sentent le sucre.",
                "maman|Une barquette est encore froide.",
                "narrateur|Une goutte rouge glisse le long de la toile.",
                "narrateur|Elle mouille une fraise, puis s'arrête.",
                "enfant-m|Elle brille.",
                "papa|Tu la ranges, sur l'étal ?",
                "enfant-m|Oui, papa.",
                "enfant-m|C'est mon stand.",
                "narrateur|Mila s'approche, un pas, puis deux.",
                "enfant-m|Tu veux une fraise ?",
                "narrateur|Mila garde les mains dans les poches.",
                "narrateur|La fraise reste au creux de sa paume.",
            ]
        )
    return vet(
        [
            "narrateur|Raphaël s'abrite sous le store vert.",
            "narrateur|La toile sent la feuille, un peu humide.",
            "narrateur|Une lumière verte pose des taches sur les poires.",
            "enfant-m|Elles sont lourdes.",
            "papa|Le sucré arrive jusqu'ici.",
            "narrateur|Une goutte verte pend, trop ronde.",
            "narrateur|Elle tombe sur une poire, tout bas.",
            "enfant-m|Elle a un point d'eau.",
            "maman|Tu la mets, pour le stand ?",
            "enfant-m|Oui.",
            "enfant-m|Je veux offrir une poire.",
            "narrateur|Mila s'arrête au bord de l'étal.",
            "enfant-m|Tu viens m'aider ?",
            "narrateur|Mila regarde la poire, sans bouger.",
            "narrateur|Le point d'eau glisse, tout lent.",
        ]
    )


def t1_q(i: int) -> list[str]:
    st = STORE[i]
    if i == 1:
        return vet(
            [
                "narrateur|Une goutte a coloré le citron.",
                "papa|De quelle couleur est le store ?",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|La lumière a teinté les fraises.",
                "maman|De quelle couleur est le store ?",
            ]
        )
    return vet(
        [
            f"narrateur|{st['goutte'].capitalize()} a touché la poire.",
            "papa|De quelle couleur est le store ?",
        ]
    )


def t1_c(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "enfant-m|Jaune.",
                "papa|Oui.",
                "narrateur|La toile jaune vibre un peu au vent.",
                "maman|Les citrons en ont plein le dos.",
                "enfant-m|Je tiens le stand.",
                "papa|Bravo, Raphaël.",
                "narrateur|Il pose le citron mouillé près des autres.",
            ]
        )
    if i == 2:
        return vet(
            [
                "enfant-m|Rouge.",
                "maman|Oui.",
                "narrateur|La toile rouge fait un peu d'ombre.",
                "papa|Les fraises ont pris la lumière.",
                "enfant-m|J'offre une fraise.",
                "maman|Merci, Raphaël.",
                "narrateur|La barquette reste froide, contre le bois.",
            ]
        )
    return vet(
        [
            "enfant-m|Vert.",
            "papa|Oui.",
            "narrateur|La toile verte bouge, tout calme.",
            "maman|Les poires ont un peu d'eau.",
            "enfant-m|Le stand est à moi, ce matin.",
            "papa|Merci.",
            "narrateur|La poire garde son point brillant.",
        ]
    )


def t2_pass(i: int, j: int) -> list[str]:
    st = STORE[i]
    if (i, j) == (1, 1):
        return vet(
            [
                "narrateur|Raphaël pose le citron sur la balance.",
                "narrateur|Le plateau est froid, tout lisse.",
                "narrateur|L'aiguille saute, puis tremble.",
                "enfant-m|Il est lourd.",
                "papa|Le zeste a laissé une trace.",
                "narrateur|Une goutte jaune rejoint le métal.",
                "enfant-m|Tu veux voir l'aiguille, Mila ?",
                "narrateur|Mila se tient au bord de l'étal.",
                "maman|Elle t'a entendu.",
            ]
        )
    if (i, j) == (1, 2):
        return vet(
            [
                "narrateur|Raphaël ouvre un sac en papier brun.",
                "narrateur|Le papier froisse, tout sec.",
                "narrateur|Il glisse le citron dedans.",
                "enfant-m|Ça sent le zeste.",
                "maman|Le sac tient chaud, déjà.",
                "enfant-m|Tu veux tenir le sac, Mila ?",
                "narrateur|Le sac reste ouvert, entre ses doigts.",
                "papa|Il froisse encore, tout sec.",
                "narrateur|Une ombre jaune traverse le papier.",
            ]
        )
    if (i, j) == (1, 3):
        return vet(
            [
                "narrateur|Raphaël soulève le citron vers la caisse.",
                "narrateur|Le bois des bords est rêche.",
                "narrateur|Les citrons font une petite tour.",
                "enfant-m|Il va tout en haut.",
                "papa|La caisse est un peu haute.",
                "enfant-m|Tu veux poser un citron, Mila ?",
                "narrateur|Mila lève les yeux vers le bord.",
                "maman|Il y en a aussi, plus bas.",
                "narrateur|Le citron mouillé attend dans sa main.",
            ]
        )
    if (i, j) == (2, 1):
        return vet(
            [
                "narrateur|Raphaël pose la fraise sur la balance.",
                "narrateur|Un jus rose tache le plateau.",
                "narrateur|L'aiguille bouge à peine.",
                "enfant-m|Elle est légère.",
                "maman|Le sucre colle un peu au métal.",
                "enfant-m|Tu veux voir le poids, Mila ?",
                "narrateur|Mila avance le menton, tout près.",
                "papa|L'aiguille fait un tout petit tic.",
                "narrateur|La goutte rouge a séché en rond.",
            ]
        )
    if (i, j) == (2, 2):
        return vet(
            [
                "narrateur|Raphaël glisse la barquette dans le sac.",
                "narrateur|Le papier sent encore le bois.",
                "narrateur|Les fraises roulent, tout doux.",
                "enfant-m|Elles sont au chaud.",
                "papa|Le sac est un peu trop grand.",
                "enfant-m|Tu veux le porter, Mila ?",
                "narrateur|Mila touche le bord du papier.",
                "maman|Il froisse sous les doigts.",
                "narrateur|Une lumière rose traverse le sac.",
            ]
        )
    if (i, j) == (2, 3):
        return vet(
            [
                "narrateur|Raphaël pose la fraise dans la caisse.",
                "narrateur|Les autres sont déjà alignées.",
                "narrateur|Une fraise roule vers le bord.",
                "enfant-m|Je la rattrape.",
                "papa|Doucement, le bois est lisse.",
                "enfant-m|Tu veux ranger une fraise, Mila ?",
                "narrateur|Mila suit la fraise des yeux.",
                "maman|Il reste une place, tout près.",
                "narrateur|La caisse sent le sucre, encore.",
            ]
        )
    if (i, j) == (3, 1):
        return vet(
            [
                "narrateur|Raphaël pose la poire sur la balance.",
                "narrateur|L'aiguille part loin, tout d'un coup.",
                "enfant-m|Elle est trop lourde.",
                "papa|Le plateau penche un peu.",
                "narrateur|Une goutte verte glisse sous le fruit.",
                "enfant-m|Tu veux voir le chiffre, Mila ?",
                "narrateur|Mila se hausse, pour mieux voir.",
                "maman|Le chiffre est grand, tout noir.",
                "narrateur|La poire ne bouge plus.",
            ]
        )
    if (i, j) == (3, 2):
        return vet(
            [
                "narrateur|Raphaël ouvre le sac, tout large.",
                "narrateur|La poire entre, presque entière.",
                "narrateur|Le papier prend la forme du fruit.",
                "enfant-m|Elle remplit tout.",
                "maman|Le sucré passe à travers.",
                "enfant-m|Tu veux porter le sac, Mila ?",
                "narrateur|Mila pose un doigt sur le papier.",
                "papa|Il est un peu lourd, déjà.",
                "narrateur|Une tache verte perce le brun.",
            ]
        )
    return vet(
        [
            "narrateur|Raphaël approche la poire de la caisse.",
            "narrateur|Les poires du haut dépassent le bord.",
            "enfant-m|Celles d'en bas sont plus près.",
            "papa|La caisse est haute, pour les petites mains.",
            "enfant-m|Tu veux une poire d'en bas, Mila ?",
            "narrateur|Mila regarde le rang du bas.",
            "maman|Il y en a une, juste à sa hauteur.",
            "narrateur|La goutte verte brille encore dessus.",
            "narrateur|Le bois sent le fruit, tout calme.",
        ]
    )


def t3_pass(i: int, j: int, k: int) -> list[str]:
    st = STORE[i]
    ge = GEST[j]
    if k == 1:
        # Mila looks
        if j == 1:
            suite = [
                "narrateur|Raphaël laisse l'aiguille se calmer.",
                f"narrateur|{st['fruit'].capitalize()} reste {ge['ou']}.",
                "enfant-m|Tu peux regarder.",
                "narrateur|Mila suit l'aiguille des yeux.",
                "papa|L'aiguille s'est arrêtée, tout seule.",
            ]
        elif j == 2:
            suite = [
                "narrateur|Raphaël tient le sac ouvert.",
                f"narrateur|{st['un'].capitalize()} reste dedans.",
                "enfant-m|Tu peux regarder.",
                "narrateur|Mila regarde le papier, tout près.",
                "maman|Ses yeux restent sur le papier.",
            ]
        else:
            suite = [
                "narrateur|Raphaël pose le fruit, tout doux.",
                f"narrateur|{st['fruit'].capitalize()} rejoint {ge['lab']}.",
                "enfant-m|Tu peux regarder.",
                "narrateur|Mila suit le geste, sans toucher.",
                "papa|Elle suit le stand, sans bouger.",
            ]
        return vet(
            [
                "enfant-f|Je regarde.",
                "enfant-m|D'accord.",
            ]
            + suite
        )
    if k == 2:
        if j == 1:
            suite = [
                "narrateur|Raphaël garde le fruit sur le plateau.",
                "enfant-m|Je te le garde.",
                "narrateur|Mila recule d'un pas, vers une autre odeur.",
                f"papa|{st['fruit'].capitalize()} ne bouge plus.",
                f"narrateur|{st['odeur'].capitalize()} reste sur le métal.",
            ]
        elif j == 2:
            suite = [
                "narrateur|Raphaël referme un peu le sac.",
                "enfant-m|Je te le garde.",
                "narrateur|Mila s'éloigne vers un autre étal.",
                "maman|Le sac sent encore le fruit.",
                f"narrateur|{st['un'].capitalize()} reste au fond du papier.",
            ]
        else:
            suite = [
                "narrateur|Raphaël laisse une place dans la caisse.",
                "enfant-m|Je te la garde.",
                "narrateur|Mila part un peu, puis se retourne.",
                "papa|La place reste vide, pour elle.",
                f"narrateur|{st['fruits'].capitalize()} attendent, tout calmes.",
            ]
        return vet(
            [
                "enfant-f|Plus tard.",
                "enfant-m|D'accord.",
            ]
            + suite
        )
    # k == 3 je prends
    if j == 1:
        suite = [
            "narrateur|Mila pose un doigt près de l'aiguille.",
            f"narrateur|{st['fruit'].capitalize()} penche un peu, puis tient.",
            "enfant-m|Merci.",
            "papa|Vous l'avez pesé, tous les deux.",
            "narrateur|Le plateau redevient calme.",
        ]
    elif j == 2:
        suite = [
            "narrateur|Mila prend le sac par le bord.",
            f"narrateur|{st['un'].capitalize()} roule au fond, tout doux.",
            "enfant-m|Merci.",
            "maman|Le papier tient, entre vous.",
            "narrateur|Le sac se ferme, presque.",
        ]
    else:
        suite = [
            "narrateur|Mila glisse le fruit dans la caisse.",
            f"narrateur|{st['un'].capitalize()} trouve sa place.",
            "enfant-m|Merci.",
            "papa|Le stand a deux paires de mains.",
            "narrateur|Le bois ne bouge plus.",
        ]
    return vet(
        [
            "enfant-f|Je prends.",
            "enfant-m|Oui.",
        ]
        + suite
    )


FIN_IMG = {
    (1, 1, 1): "L'aiguille ne bouge plus, sous le store jaune.",
    (1, 1, 2): "Le citron attend encore sur le plateau froid.",
    (1, 1, 3): "Deux doigts ont laissé une trace sur le métal.",
    (1, 2, 1): "Le sac brun garde une ombre de citron.",
    (1, 2, 2): "Le papier reste ouvert, pour plus tard.",
    (1, 2, 3): "Le sac penche entre deux petites mains.",
    (1, 3, 1): "Les citrons du haut brillent, tout jaunes.",
    (1, 3, 2): "Une place vide reste au bord de la caisse.",
    (1, 3, 3): "Le citron mouillé a rejoint la tour.",
    (2, 1, 1): "Un rond de jus rose sèche sur le plateau.",
    (2, 1, 2): "La fraise garde sa place, pour plus tard.",
    (2, 1, 3): "L'aiguille s'est tue, tout près des deux.",
    (2, 2, 1): "Le sac sent encore le sucre, tout bas.",
    (2, 2, 2): "La barquette attend au fond du papier.",
    (2, 2, 3): "Le sac froisse, porté à deux.",
    (2, 3, 1): "Les fraises sont alignées, sous le rouge.",
    (2, 3, 2): "Une place rose reste dans la caisse.",
    (2, 3, 3): "La fraise rattrapée ne roule plus.",
    (3, 1, 1): "Le chiffre noir reste grand, sous le vert.",
    (3, 1, 2): "La poire pèse encore, pour plus tard.",
    (3, 1, 3): "Le plateau s'est calmé, entre eux.",
    (3, 2, 1): "Le sac a pris la forme de la poire.",
    (3, 2, 2): "Le papier attend, un peu lourd.",
    (3, 2, 3): "Le sac vert-brun penche, puis tient.",
    (3, 3, 1): "Les poires d'en bas restent à hauteur.",
    (3, 3, 2): "Une poire du bas attend encore.",
    (3, 3, 3): "La poire d'en bas a trouvé sa place.",
}

FIN_DROP = {
    1: "La goutte jaune a séché sur le bois.",
    2: "La goutte rouge n'est plus qu'un rond.",
    3: "La goutte verte a disparu de la peau.",
}


def t3_fin(i: int, j: int, k: int) -> list[str]:
    st = STORE[i]
    ge = GEST[j]
    img = FIN_IMG[(i, j, k)]
    drop = FIN_DROP[i]
    if k == 1:
        return vet(
            [
                f"narrateur|{img}",
                "narrateur|Mila reste au bord, les yeux ouverts.",
                "enfant-m|Tu as regardé le stand.",
                "enfant-f|Oui.",
                f"narrateur|{st['fruits'].capitalize()} restent {ge['ou']}.",
                "maman|Le stand a tenu, ce matin.",
                "papa|Merci, Raphaël.",
                f"narrateur|{drop}",
                "narrateur|Le marché parle plus bas, maintenant.",
                "narrateur|La toile du store ne goutte plus.",
            ]
        )
    if k == 2:
        return vet(
            [
                f"narrateur|{img}",
                "narrateur|Mila revient, les joues un peu chaudes.",
                "enfant-f|Maintenant ?",
                "enfant-m|Oui.",
                "enfant-m|C'est encore pour toi.",
                f"narrateur|Elle s'approche {ge['de']}.",
                "papa|Vous avez pris le temps.",
                "maman|Merci, tous les deux.",
                f"narrateur|{drop}",
                "narrateur|Sous le store, l'étal est calme.",
            ]
        )
    return vet(
        [
            f"narrateur|{img}",
            "enfant-f|On l'a fait.",
            "enfant-m|Le stand est à nous.",
            f"narrateur|{st['un'].capitalize()} a quitté l'étal, tout doux.",
            "papa|Vous avez offert le fruit.",
            "maman|Merci, Raphaël.",
            "maman|Merci, Mila.",
            f"narrateur|{drop}",
            "narrateur|Le bois de l'étal redevient sec.",
            "narrateur|La toile ne bouge plus, ou presque.",
        ]
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        [
            "narrateur|Une goutte glisse le long du store, toute ronde.",
            "narrateur|Elle tombe sur le bois de l'étal.",
            "narrateur|Le marché sent le fruit, encore frais.",
            "narrateur|Des caisses claquent, tout près.",
            "narrateur|Le soleil perce la toile, un peu mouillée.",
            "papa|Tu as vu la goutte, Raphaël ?",
            "enfant-m|Elle a fait ploc.",
            "maman|Le bois est froid, ce matin.",
            "enfant-m|Je veux tenir le stand.",
            "papa|Tu offres un fruit, alors ?",
            "enfant-m|Oui.",
            "enfant-m|Un fruit, pour Mila.",
            "narrateur|En ce moment, Raphaël pose les deux mains sur l'étal.",
            "narrateur|La toile du store bouge un peu.",
            "maman|Le jaune, le rouge, ou le vert ?",
        ]
    )
    sons["CHK_T0000_P0000"] = "goutte"

    s["CHK_T0001_P0000"] = vet(
        [
            "narrateur|Trois toiles colorent l'étal.",
            "narrateur|Le store jaune, le store rouge, ou le store vert.",
            "papa|Lequel éclaire tes fruits, Raphaël ?",
        ]
    )
    extras["CHK_T0001_P0000"] = t3(
        "le store jaune", "le store rouge", "le store vert"
    )

    q_extra = {
        1: qf(
            "jaune",
            "jaune | store jaune | citron | dorée | doré",
            "Une goutte est tombée. De quelle couleur est le store ?",
        ),
        2: qf(
            "rouge",
            "rouge | store rouge | fraise | rose",
            "La lumière a teinté les fraises. De quelle couleur est le store ?",
        ),
        3: qf(
            "vert",
            "vert | store vert | poire | verte",
            "Une goutte a touché la poire. De quelle couleur est le store ?",
        ),
    }

    for i, st in STORE.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = t1_pass(i)
        sons[p] = st["son"]
        s[f"{p}_Q0001"] = t1_q(i)
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = t1_c(i)
        s[f"{p}_T0002_P0000"] = vet(
            [
                f"narrateur|Sous {st['lab']}, le stand attend un geste.",
                "maman|La balance, le sac, ou la caisse ?",
                f"papa|Tu fais quoi, avec {st['fruit']} ?",
            ]
        )
        extras[f"{p}_T0002_P0000"] = t3("la balance", "le sac", "la caisse")
        for j, ge in GEST.items():
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = t2_pass(i, j)
            s[f"{p2}_T0003_P0000"] = vet(
                [
                    f"narrateur|Mila est {ge['pres']}.",
                    "papa|Je regarde, plus tard, ou je prends ?",
                    "maman|On l'écoute, tout près.",
                ]
            )
            extras[f"{p2}_T0003_P0000"] = t3("je regarde", "plus tard", "je prends")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = t3_pass(i, j, k)
                s[f"{p3}_F0001"] = t3_fin(i, j, k)

    write_tree(s, sons, extras)
    relecture(
        SID,
        "La goutte du store et le stand de Raphaël",
        "goutte du store, 3 couleurs d'étal, balance/sac/caisse, Mila regarde/plus tard/prend, stand tenu",
        "avis2. Gabarit train/Tom/Léa jeté. Kenzo hors troupe. Audio non cuit. 27 chemins non écoutés à voix haute.",
    )


if __name__ == "__main__":
    main()
