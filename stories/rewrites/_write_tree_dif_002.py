#!/usr/bin/env python3
"""TREE-DIF-002 — Nino, goûter dans la cabane, pull trop grand, deux pommes."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N2 = LIMITS["N2"]
SID = "TREE-DIF-002"


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


def pre(t1: int) -> str:
    return f"CHK_T0001_P000{t1}"


def color(t1: int, i: int) -> str:
    bag = {
        1: (
            "Sous le bleu, les épaules sont déjà tièdes.",
            "Une manche trop longue frotte encore.",
            "Le savon du pull reste dans l'air.",
        ),
        2: (
            "L'anse marque encore la paume de Nino.",
            "Le panier penche vers l'herbe.",
            "Un brin d'osier pique un doigt.",
        ),
        3: (
            "Un coin de nappe dépasse, tout blanc.",
            "La nappe sent l'herbe coupée.",
            "Le paquet se défait un peu.",
        ),
    }
    return bag[t1][i % 3]


def coda(t1: int) -> str:
    return {
        1: "Une manche touche encore l'herbe, trop longue.",
        2: "L'anse du panier repose contre le genou.",
        3: "Un carré de nappe garde une miette.",
    }[t1]


def t1_pass(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino tire d'abord le pull bleu, à la branche.",
            "narrateur|Une manche tombe, trop longue, dans l'herbe.",
            "enfant-m|Mes mains ont disparu !",
            "maman|Les manches mangent tes doigts.",
            "narrateur|Il souffle dans le tissu, qui sent le savon.",
            "papa|C'est trop grand, et ça tient chaud.",
            "enfant-m|Je le garde.",
            "narrateur|Le panier attend, et la nappe aussi.",
            "maman|On les prend, après le pull.",
            "enfant-m|D'accord.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino saisit d'abord l'anse du panier.",
            "narrateur|L'osier gratte un peu, encore froid.",
            "enfant-m|Il est vide.",
            "papa|Les pommes vont dedans, tout à l'heure.",
            "narrateur|Deux pommes brillent encore sous les feuilles.",
            "enfant-m|Je les veux, pour la cabane.",
            "maman|Le pull et la nappe viennent avec.",
            "narrateur|Il pose le panier contre sa hanche.",
            "papa|Il tient ?",
            "enfant-m|Oui, papa.",
        )
    return L(
        "narrateur|Nino déplie d'abord la nappe, près de l'herbe.",
        "narrateur|Un carré rouge et blanc sent l'extérieur.",
        "enfant-m|C'est pour le goûter.",
        "maman|On la pose dans la cabane, plus tard.",
        "narrateur|Un coin reste collé à une feuille.",
        "enfant-m|Je l'enlève.",
        "papa|Le panier et le pull attendent.",
        "narrateur|Il plie la nappe, tout petit paquet.",
        "maman|Tu la portes ?",
        "enfant-m|Contre moi.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino a enfilé le pull de papa.",
            "maman|Le pull, il est comment ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le panier est encore vide.",
            "papa|Nino veut mettre quoi dedans ?",
        )
    return L(
        "narrateur|Un carré rouge et blanc sent l'herbe.",
        "maman|Nino a déplié quoi, d'abord ?",
    )


def t1_c(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Les manches traînent, et Nino avance quand même.",
            "papa|Le panier, tu le tiens ?",
            "enfant-m|Avec le bout des manches.",
            "narrateur|Il glisse la ronde, puis la mince.",
            "maman|La nappe, je la glisse sous ton bras.",
            "narrateur|Ils quittent la branche, tout doux.",
            "enfant-m|La cabane, après.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le panier penche, déjà moins vide.",
            "narrateur|La ronde, puis la mince, tombent dedans.",
            "papa|Le pull, par-dessus ?",
            "enfant-m|Oui, il tient chaud.",
            "maman|La nappe va avec, pliée.",
            "narrateur|Ils avancent dans l'herbe, sans courir.",
            "enfant-m|On goûte, après.",
        )
    return L(
        "narrateur|La nappe pliée tape le ventre, à chaque pas.",
        "maman|Le pull, tu le veux sur toi ?",
        "enfant-m|Oui, j'ai encore froid.",
        "narrateur|La ronde et la mince rejoignent le panier.",
        "papa|Le panier, je le porte un moment.",
        "enfant-m|Non, moi.",
        "narrateur|Ils marchent vers le fond du jardin.",
    )


def t2_q(t1: int) -> list[str]:
    head = {
        1: "Le pull bleu frotte encore les genoux.",
        2: "Le panier tape un peu la cuisse.",
        3: "La nappe fait un paquet contre le ventre.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Le jardin s'ouvre, encore frais.",
        "narrateur|Le pommier, la cabane, ou le banc.",
        "papa|On pose le goûter où ?",
    )


def t2_pass(t1: int, t2: int) -> list[str]:
    head = {
        1: "Le pull bleu descend trop bas.",
        2: "L'anse du panier marque la paume.",
        3: "La nappe pliée chauffe un peu.",
    }[t1]
    if t2 == 1:
        return L(
            f"narrateur|{head}",
            "narrateur|Sous le pommier, l'herbe est froide.",
            "enfant-m|Je les regarde encore.",
            "narrateur|Il sort la ronde, toute jaune.",
            "narrateur|Puis la mince, avec sa joue verte.",
            "enfant-m|Elles ne se ressemblent pas.",
            "papa|Tu les veux quand même ?",
            "enfant-m|Je voulais deux pareilles.",
            "maman|Elles sentent pareil, tu sais.",
            "narrateur|La ronde pèse plus, dans sa main.",
        )
    if t2 == 2:
        return L(
            f"narrateur|{head}",
            "narrateur|La cabane sent le bois sec.",
            "enfant-m|On goûte ici.",
            "narrateur|Les deux pommes voyagent, serrées contre lui.",
            "narrateur|Le pull accroche le bord de la porte.",
            "enfant-m|Je ne passe pas bien.",
            "papa|Les manches traînent par terre.",
            "maman|Tu tiens les pommes comment, là ?",
            "enfant-m|Mal.",
            "narrateur|Une manche a recouvert une pomme.",
        )
    return L(
        f"narrateur|{head}",
        "narrateur|Le banc de bois est encore un peu humide.",
        "enfant-m|La nappe, ici.",
        "narrateur|Ils posent les deux pommes au milieu.",
        "narrateur|La mince roule, et tombe dans l'herbe.",
        "enfant-m|Elle part !",
        "papa|La ronde, elle, reste.",
        "maman|Elles ne tiennent pas pareil.",
        "narrateur|Nino se baisse, l'herbe lui pique les mains.",
    )


def t3_q(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Deux pommes, deux formes.",
            "papa|Tu fais quoi, Nino ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le pull gêne un peu la porte.",
            "maman|Tu fais quoi, avec ?",
        )
    return L(
        "narrateur|La mince a roulé.",
        "papa|Tu fais quoi, maintenant ?",
    )


def t3_pass(t1: int, t2: int, t3: int) -> list[str]:
    col = color(t1, t2 + t3)
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-m|Les deux, dans le panier.",
            "narrateur|La ronde tombe au fond, lourde.",
            "narrateur|La mince se couche à côté, tout en long.",
            "enfant-m|Ça fait tic.",
            "papa|Deux pommes, deux places.",
            "maman|Tu les as, pour le goûter.",
            f"narrateur|{col}",
            "narrateur|Le panier sent déjà le fruit.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-m|J'attends une autre, pareille.",
            "narrateur|Le vent secoue une branche.",
            "narrateur|Une feuille tombe, pas une pomme.",
            "papa|Il n'en tombe plus.",
            "enfant-m|Bon.",
            "enfant-m|Je prends ces deux-là.",
            "maman|Elles iront très bien.",
            f"narrateur|{col}",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-m|Je les essuie, d'abord.",
            "narrateur|Il frotte la mince sur son genou.",
            "narrateur|La ronde, il la tourne, encore.",
            "enfant-m|Toujours pas pareilles.",
            "papa|Elles restent comme elles sont.",
            "maman|Le froid, lui, est le même.",
            f"narrateur|{col}",
            "narrateur|Un peu de jus brille sur le pouce.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-m|On roule les manches.",
            "maman|Un tour, puis un autre.",
            "narrateur|Les mains de Nino reparaissent, toutes petites.",
            "papa|Tu tiens les pommes, maintenant ?",
            "enfant-m|Oui !",
            f"narrateur|{col}",
            "narrateur|Il passe la porte, sans accrocher.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-m|Le pull, par terre.",
            "narrateur|Il l'enlève, et le pose au sol.",
            "narrateur|Le tissu fait un carré tiède.",
            "maman|C'est votre tapis de goûter.",
            "papa|Les pommes au milieu ?",
            "enfant-m|Oui, les deux.",
            f"narrateur|{col}",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-m|Comme une cape.",
            "papa|Sur les épaules, alors.",
            "narrateur|Le bleu tombe dans le dos, trop long.",
            "enfant-m|Je passe !",
            "narrateur|Il entre, la cape derrière lui.",
            "maman|Tu as chaud, comme ça ?",
            "enfant-m|Oui, maman.",
            f"narrateur|{col}",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-m|On les coupe.",
            "papa|La ronde d'abord, puis la mince.",
            "narrateur|Dedans, les deux sont blanches.",
            "enfant-m|Elles se ressemblent, là.",
            "maman|Le jus est le même.",
            f"narrateur|{col}",
            "narrateur|Deux moitiés attendent sur le bois.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-m|La ronde va l'arrêter.",
            "narrateur|Il pose la jaune contre la mince.",
            "narrateur|Plus rien ne roule.",
            "papa|L'une tient l'autre.",
            "maman|Deux formes, un goûter.",
            "enfant-m|Elles restent.",
            f"narrateur|{col}",
        )
    return L(
        "enfant-m|Une pour moi, une pour papa.",
        "narrateur|Nino croque la ronde, tout fort.",
        "narrateur|Papa croque la mince, plus doux.",
        "enfant-m|Ça goûte pareil !",
        "maman|Le jus te colle au menton.",
        f"narrateur|{col}",
        "papa|On partage, alors.",
    )


def t3_fin(t1: int, t2: int, t3: int) -> list[str]:
    cd = coda(t1)
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Dans la cabane, le panier s'ouvre.",
            "narrateur|Les deux pommes se touchent, différentes.",
            "enfant-m|On goûte.",
            "maman|La ronde, ou la mince, comme tu veux.",
            f"narrateur|{cd}",
            "narrateur|Dehors, une feuille tourne encore.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Ils s'assoient près du tronc.",
            "narrateur|Les deux pommes, enfin, dans les mains.",
            "enfant-m|Pas de troisième.",
            "papa|Ces deux-là suffisent.",
            f"narrateur|{cd}",
            "narrateur|Le bois de la cabane sent le soleil.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le pouce de Nino reste un peu collant.",
            "enfant-m|On entre.",
            "narrateur|Ils posent les pommes sur le plancher.",
            "maman|Le goûter est là.",
            f"narrateur|{cd}",
            "narrateur|Une abeille passe, puis s'en va.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|À l'intérieur, les manches tiennent, roulées.",
            "enfant-m|Mes mains sont libres.",
            "papa|Les pommes aussi.",
            f"narrateur|{cd}",
            "narrateur|Un rond de lumière entre par la fente.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils s'assoient sur le bleu, tout doux.",
            "enfant-m|C'est chaud, en dessous.",
            "maman|Le goûter a un tapis.",
            f"narrateur|{cd}",
            "narrateur|Le bois craque, une seule fois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|La cape bleue glisse encore un peu.",
            "enfant-m|J'ai les pommes.",
            "papa|On les pose, et on croque.",
            f"narrateur|{cd}",
            "narrateur|L'ombre de la cabane est fraîche.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Nino croque une moitié blanche.",
            "enfant-m|C'est sucré.",
            "maman|L'autre moitié attend papa.",
            f"narrateur|{cd}",
            "narrateur|Le banc garde une petite tache de jus.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Les deux pommes tiennent, l'une contre l'autre.",
            "enfant-m|On peut croquer, maintenant.",
            "papa|Doucement, le banc penche un peu.",
            f"narrateur|{cd}",
            "narrateur|Un oiseau se tait, dans le pommier.",
        )
    return L(
        "narrateur|Le jus mélange deux formes, sur le bois.",
        "enfant-m|Encore un morceau.",
        "maman|Il en reste, dans ta main.",
        f"narrateur|{cd}",
        "narrateur|Le jardin redevient calme, tout autour.",
    )


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
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
        "Nino veut deux pommes pour le goûter dans la cabane. "
        "Le pull de papa est trop grand. Les pommes n'ont pas la même forme. "
        "Il les emporte, et le tissu tient chaud."
    )
    out["title"] = "Le pull bleu et les deux pommes"
    out["characters"] = "Nino, papa, maman"
    out["setting"] = "jardin d'automne, pommier, cabane de planches"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {
        "CHK_T0000_P0000": "feuille",
        "CHK_T0001_P0001": "tissu",
        "CHK_T0001_P0002": "",
        "CHK_T0001_P0003": "tissu",
    }

    s["CHK_T0000_P0000"] = L(
        "narrateur|Derrière la maison, le jardin sent la pomme.",
        "narrateur|Une feuille jaune tourne, puis se pose.",
        "narrateur|Le pommier penche vers la cabane de planches.",
        "narrateur|Un pull bleu pend à la branche basse.",
        "narrateur|Il sent encore le savon, un peu froid.",
        "narrateur|Deux pommes brillent dans l'herbe.",
        "narrateur|L'une est ronde, toute jaune.",
        "narrateur|L'autre est plus mince, avec une joue verte.",
        "papa|Tu les veux pour le goûter, Nino ?",
        "enfant-m|Oui.",
        "enfant-m|Dans la cabane.",
        "maman|Il commence à faire frais.",
        "narrateur|En ce moment, Nino touche le pull.",
        "narrateur|Le tissu tombe trop bas, jusqu'aux genoux.",
        "enfant-m|Il est trop grand.",
        "papa|C'est le mien.",
        "papa|Tu le prends quand même ?",
        "enfant-m|Oui, j'ai froid.",
        "maman|Le panier et la nappe viennent aussi.",
        "papa|Merci d'avoir dit le froid.",
        "papa|Tu prépares quoi d'abord ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois choses attendent près de l'herbe.",
        "narrateur|Le pull bleu, le panier, et la nappe.",
        "maman|Tu commences par laquelle ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le pull bleu", "le panier", "la nappe")

    t3_by_t2 = {
        1: t3lab("les deux pommes", "attendre", "essuyer"),
        2: t3lab("rouler les manches", "la couverture", "la cape"),
        3: t3lab("couper", "caler", "partager"),
    }
    q_by_t1 = {
        1: qf(
            "trop grand",
            "trop grand | grand | trop large | large | énorme | trop long",
            "Le pull de papa tombe trop bas.",
        ),
        2: qf(
            "des pommes",
            "pommes | des pommes | deux pommes | les pommes | une pomme",
            "Nino veut des pommes dans le panier.",
        ),
        3: qf(
            "la nappe",
            "nappe | la nappe | une nappe",
            "Nino a déplié la nappe.",
        ),
    }

    for t1 in (1, 2, 3):
        p = pre(t1)
        s[p] = t1_pass(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = q_by_t1[t1]
        s[f"{p}_C0001"] = t1_c(t1)
        s[f"{p}_T0002_P0000"] = t2_q(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le pommier", "la cabane", "le banc")
        sons[p] = {1: "tissu", 2: "", 3: "tissu"}[t1]
        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_pass(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_q(t2)
            extras[f"{sp}_T0003_P0000"] = t3_by_t2[t2]
            sons[sp] = {1: "feuille", 2: "bois", 3: ""}[t2]
            for t3 in (1, 2, 3):
                tp = f"{sp}_T0003_P000{t3}"
                s[tp] = t3_pass(t1, t2, t3)
                s[f"{tp}_F0001"] = t3_fin(t1, t2, t3)
                if t2 == 1:
                    sons[tp] = "pomme"
                elif t2 == 2:
                    sons[tp] = "tissu"
                else:
                    sons[tp] = ""

    write_tree(s, extras, sons)
    relecture(
        SID,
        "Le pull bleu et les deux pommes",
        "Nino veut deux pommes pour le goûter dans la cabane. "
        "T1 colore : pull / panier / nappe, les trois partent. "
        "T2×T3 = 9 aventures : pommier (deux formes), cabane (pull trop grand), "
        "banc (pomme qui roule). Imprévu vécu, pas de morale dite.",
        "Sami hors troupe → Nino seul, papa/maman. Pas Mila. "
        "Brouillon merged.json non repris (leçon dite, Amir+Nino, T3 couleurs). "
        "check() N2. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
