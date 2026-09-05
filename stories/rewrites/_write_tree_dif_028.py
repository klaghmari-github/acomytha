#!/usr/bin/env python3
"""TREE-DIF-028 — Le gâteau aux fraises de Chouchou. DIF.PAR.002, N2."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N2 = LIMITS["N2"]
SID = "TREE-DIF-028"
TITLE = "Le gâteau aux fraises de Chouchou"
FIL = (
    "Chouchou veut un gâteau aux fraises pour le goûter. "
    "Maman a la recette dans la tête, mais elle cherche ses mots, "
    "les mains déjà blanches. "
    "T1 = saladier / cuillère / tablier ; les trois partent. "
    "T2 = placard / tiroir / garde-manger, chaque lieu a son obstacle. "
    "Chouchou laisse maman finir. Le gâteau sent le beurre."
)


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


PREP = {
    1: dict(
        label="le saladier",
        coda="Le bois du saladier reste tiède, un peu blanc.",
        touch="Le bois du saladier est lisse, déjà farineux.",
    ),
    2: dict(
        label="la cuillère",
        coda="La cuillère de bois tape une dernière fois, tout doux.",
        touch="Le manche de la cuillère est rêche, encore.",
    ),
    3: dict(
        label="le tablier",
        coda="Le tablier garde une tache de farine, tout petite.",
        touch="Le tissu du tablier est un peu rêche, déjà.",
    ),
}


def t1_pass(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Chouchou saisit d'abord le saladier de bois.",
            "enfant-f|Pour le gâteau, après.",
            "papa|Il sent encore le lait.",
            "narrateur|Le bois est lisse, déjà un peu blanc.",
            "maman|La cuillère, ensuite, contre le bord.",
            "narrateur|Papa glisse le tablier sur ses épaules.",
            "enfant-f|Et la farine ?",
            "narrateur|Maman ouvre la bouche, les mains blanches.",
            "maman|Elle est.",
            "narrateur|Le mot n'arrive pas, encore.",
            "papa|On marche, elle va finir.",
            "enfant-f|D'accord.",
        )
    if t1 == 2:
        return L(
            "narrateur|Chouchou prend d'abord la cuillère de bois.",
            "enfant-f|Pour mélanger, après.",
            "maman|Elle tape trop tôt, parfois.",
            "narrateur|Le manche est rêche, encore un peu.",
            "papa|Le saladier, ensuite, et le tablier.",
            "narrateur|Maman les pose contre elle, l'un après l'autre.",
            "enfant-f|Alors dis-moi où.",
            "narrateur|Maman inspire, les lèvres déjà rondes.",
            "narrateur|Elle ne dit rien, encore.",
            "papa|Elle cherche la suite.",
            "enfant-f|J'attends.",
            "maman|Oui.",
        )
    return L(
        "narrateur|Chouchou enfile d'abord le tablier, tout large.",
        "enfant-f|Pour ne pas tacher, après.",
        "papa|Le nœud, dans le dos.",
        "narrateur|Le tissu est un peu rêche, déjà chaud.",
        "maman|Le saladier, ensuite, et la cuillère.",
        "narrateur|Papa les pose dans ses mains, tout doux.",
        "enfant-f|Maintenant, tu dis où.",
        "narrateur|Maman ouvre la bouche, puis s'arrête.",
        "papa|On avance, elle va finir.",
        "enfant-f|D'accord, maman.",
        "maman|Le mot va arriver.",
        "enfant-f|J'écoute.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le saladier de bois est déjà dans ses mains.",
            "maman|Chouchou a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|La cuillère de bois brille un peu, encore.",
            "papa|Chouchou a pris quoi ?",
        )
    return L(
        "narrateur|Le tablier fait un pli, contre son ventre.",
        "maman|Chouchou a enfilé quoi, d'abord ?",
    )


def t1_c(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|Le saladier.",
            "papa|Oui.",
            "narrateur|La cuillère et le tablier voyagent avec.",
            "maman|On marche, tout doux.",
            "enfant-f|Je suis prête.",
            "papa|Maman, tu nous guides ?",
            "maman|Oui.",
            "enfant-f|J'écoute la fin.",
        )
    if t1 == 2:
        return L(
            "enfant-f|La cuillère.",
            "maman|Oui.",
            "narrateur|Le saladier pèse déjà contre son bras.",
            "narrateur|Le tablier dort sur ses épaules.",
            "papa|On avance, le mot suivra.",
            "enfant-f|D'accord, maman.",
            "maman|Vous restez près de moi.",
            "enfant-f|Oui.",
        )
    return L(
        "enfant-f|Le tablier.",
        "papa|Oui.",
        "narrateur|Le saladier et la cuillère pèsent contre elle.",
        "maman|Elle va dire la suite.",
        "enfant-f|J'écoute.",
        "papa|On avance, alors ?",
        "maman|Oui, papa.",
        "enfant-f|Je suis prête.",
    )


def t2_q(t1: int) -> list[str]:
    head = {
        1: "Le saladier tape un peu sa hanche, à chaque pas.",
        2: "La cuillère claque une fois, contre le bois.",
        3: "Le tablier fait un pli, à chaque pas.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Le placard, le tiroir, et le garde-manger attendent.",
        "papa|On cherche où, d'abord ?",
    )


def t2_pass(t1: int, t2: int) -> list[str]:
    head = {
        1: "Le saladier de bois pose un rond d'ombre.",
        2: "La cuillère s'arrête, contre sa paume.",
        3: "Le tablier reste sage, contre son ventre.",
    }[t1]
    if t2 == 1:
        extra = {
            1: "Le saladier glisse vers le bas, tout lourd.",
            2: "La cuillère pointe une boîte, trop tôt.",
            3: "Chouchou serre le tablier, sans bouger.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|Ils s'arrêtent devant le placard haut.",
            "enfant-f|C'est trop haut.",
            f"narrateur|{extra}",
            "narrateur|Les boîtes se ressemblent, toutes blanches.",
            "enfant-f|C'est ici ?",
            "maman|La farine est sur.",
            "narrateur|Maman lève un doigt, encore.",
            "narrateur|Chouchou ouvre la bouche, puis la referme.",
            "papa|Il y a trop d'étagères.",
            "papa|Vous faites comment, toutes les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "Le saladier bute contre la poignée, puis lâche.",
            2: "La cuillère glisse dans le tiroir, trop vite.",
            3: "Un coin du tablier frôle le bois.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|Devant le tiroir, le bois sent le citron.",
            f"narrateur|{extra}",
            "enfant-f|Il y a trop de choses.",
            "maman|La recette est sous les.",
            "narrateur|Maman s'arrête, les lèvres encore rondes.",
            "narrateur|Chouchou avance un doigt, puis recule.",
            "papa|Le tiroir est trop plein.",
            "maman|La suite n'est pas dite.",
            "papa|Vous trouvez comment ?",
        )
    extra = {
        1: "Le saladier penche contre le seuil, tout sage.",
        2: "La cuillère cogne un bocal, un petit toc.",
        3: "Le tablier accroche une anse, puis lâche.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Dans le garde-manger, l'air est frais, un peu sombre.",
        f"narrateur|{extra}",
        "enfant-f|Les fraises, elles sont où ?",
        "maman|Les belles sont dans le.",
        "narrateur|Maman cherche, un doigt en l'air.",
        "narrateur|Un panier et un bol attendent, tous les deux.",
        "papa|L'ombre mélange les formes.",
        "maman|Je n'ai pas fini ma phrase.",
        "papa|Vous faites quoi, alors ?",
    )


def t3_q(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Devant le placard, maman n'a pas fini.",
            "papa|Attendre, le tabouret, ou je te porte ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Devant le tiroir, la suite manque encore.",
            "maman|S'asseoir, la lampe, ou le linge ?",
        )
    return L(
        "narrateur|Dans le garde-manger, l'ombre tient encore les fraises.",
        "papa|Compter, le panier, ou le bol ?",
    )


def t3_pass(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "Le saladier reste au sol, tout sage.",
        2: "La cuillère attend un dernier tour.",
        3: "Le tablier dort contre son ventre.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-f|On attend.",
            "maman|Oui.",
            "narrateur|Elles restent debout, l'une contre l'autre.",
            "narrateur|Une mouche tapote la vitre, puis plus rien.",
            "maman|Celle du milieu.",
            "enfant-f|L'étagère du milieu.",
            f"narrateur|{col}",
            "papa|Tu as laissé la fin arriver.",
            "maman|Elle est là, maintenant.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "papa|Je pose le petit tabouret.",
            "narrateur|Le bois craque, un tout petit cri.",
            "maman|Derrière le.",
            "narrateur|Chouchou ne dit rien.",
            "maman|Derrière le sucre.",
            "enfant-f|Je vois le sac, maintenant.",
            f"narrateur|{col}",
            "maman|Le tabouret a aidé le mot.",
            "papa|Vous avez écouté jusqu'au bout.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-f|Tu me portes, papa ?",
            "papa|Oui, tout doux.",
            "narrateur|Sa joue touche la chemise, encore chaude.",
            "maman|À côté du.",
            "narrateur|Chouchou garde sa bouche fermée.",
            "maman|À côté du sel.",
            "enfant-f|Celle-là, tout près du sel.",
            f"narrateur|{col}",
            "papa|Tu n'as pas deviné trop tôt.",
            "maman|La phrase est complète, enfin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-f|On s'assoit, d'abord.",
            "narrateur|Le carrelage est froid, un peu lisse.",
            "maman|Les serviettes.",
            "enfant-f|Sous les serviettes.",
            "narrateur|Elles soulèvent le papier, ensemble.",
            f"narrateur|{col}",
            "maman|Le mot est venu, tout seul.",
            "papa|Vous l'avez laissée finir.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "papa|J'allume la petite lampe.",
            "narrateur|Un rond jaune court dans le tiroir.",
            "maman|Sous les.",
            "narrateur|Le crayon gratte, puis s'arrête.",
            "maman|Sous les cuillères.",
            "enfant-f|Comme le rond jaune.",
            f"narrateur|{col}",
            "papa|La lumière a tenu le mot.",
            "maman|Vous avez lu ensemble.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-f|On lève le linge.",
            "narrateur|Le tissu sent encore le savon.",
            "maman|En dessous.",
            "narrateur|Chouchou tourne la tête, sans parler.",
            "maman|En dessous, le papier jaune.",
            "enfant-f|Je vois le coin, maintenant.",
            f"narrateur|{col}",
            "maman|Le linge a gardé le secret.",
            "papa|Tu as écouté la fin.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-f|On compte les bocaux.",
            "maman|Moi aussi.",
            "narrateur|Un, deux, trois, jusqu'à sept.",
            "maman|Le panier.",
            "enfant-f|Dans le panier.",
            f"narrateur|{col}",
            "papa|Les bocaux se sont tus, le mot aussi.",
            "maman|Vous l'avez entendue jusqu'au bout.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-f|On se baisse, d'abord.",
            "narrateur|L'air du bas est plus frais, encore.",
            "maman|Le panier bas.",
            "enfant-f|Pas le bol.",
            "narrateur|Elles se relèvent, tout calmes, ensemble.",
            f"narrateur|{col}",
            "papa|Se baisser a ralenti les mots.",
            "maman|La phrase a eu sa place.",
        )
    return L(
        "narrateur|Le bol rouge brille, plus proche que le panier.",
        "enfant-f|Le bol ?",
        "narrateur|Chouchou referme sa bouche, tout de suite.",
        "maman|Le bol rouge.",
        "enfant-f|Dans le bol rouge, d'accord.",
        f"narrateur|{col}",
        "maman|Tu as laissé la vraie fin.",
        "papa|Le panier peut attendre.",
    )


def t3_fin(t1: int, t2: int, t3: int) -> list[str]:
    cd = PREP[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le sac de farine est bien au milieu.",
            "narrateur|Un nuage blanc tombe dans le saladier.",
            "enfant-f|On l'a.",
            "maman|Parce que tu as attendu.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa pose les fraises, tout près.",
            "maman|Le four est déjà tiède.",
            f"narrateur|{cd}",
            "narrateur|La cuisine sent le beurre, tout doux.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Derrière le sucre, le sac attendait.",
            "enfant-f|Le tabouret l'a montrée.",
            "maman|Et le mot, après.",
            "maman|Bravo.",
            "papa|Merci d'avoir écouté.",
            "narrateur|Ils mélangent, tout doux, près de l'évier.",
            f"narrateur|{cd}",
            "narrateur|La farine se repose, enfin, dans le bois.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|À côté du sel, le sac se penche.",
            "enfant-f|Il était trop près, tout en haut.",
            "maman|Le sel a gardé sa place.",
            "papa|Merci de ne pas avoir deviné.",
            "narrateur|Une fraise laisse un jus rouge sur son doigt.",
            "maman|Le four est déjà tiède.",
            f"narrateur|{cd}",
            "narrateur|Ils s'assoient, le beurre déjà chaud.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Sous les serviettes, le papier est jaune.",
            "enfant-f|Comme tu avais dit, à la fin.",
            "maman|Oui.",
            "papa|Merci d'avoir attendu le mot.",
            "maman|On suit la recette, tout doux.",
            f"narrateur|{cd}",
            "narrateur|Le beurre fond, déjà, dans le saladier.",
            "narrateur|Le tiroir se referme, un petit clic.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le rond jaune colle encore aux cuillères.",
            "maman|Le papier était le bon.",
            "enfant-f|On a lu ensemble.",
            "maman|Bravo, toi.",
            "papa|Merci, Chouchou.",
            "narrateur|Une fraise casse, tout net, entre les dents.",
            f"narrateur|{cd}",
            "narrateur|Le tiroir redevient silencieux, près du four.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sous le linge, le papier attend.",
            "enfant-f|Tu as dit en dessous, à la fin.",
            "maman|Oui, à la fin.",
            "papa|Merci d'avoir écouté jusque-là.",
            "narrateur|Ils cassent un œuf, tout petit, dans le bois.",
            f"narrateur|{cd}",
            "narrateur|Le linge reprend sa place, tout rêche.",
            "narrateur|La cuisine n'a plus de secret, ce soir.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Dans le panier, les fraises sentent le soleil.",
            "enfant-f|Sept bocaux, puis le mot.",
            "maman|Puis j'ai fini.",
            "papa|Merci d'avoir compté.",
            "maman|Une fraise chacun, avant le four.",
            f"narrateur|{cd}",
            "narrateur|L'ombre du garde-manger passe ailleurs.",
            "narrateur|La cuisine redevient une cuisine, tout simple.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Dans le panier bas, ça sent le rouge.",
            "enfant-f|Le bol n'avait rien.",
            "maman|Se baisser nous a aidées.",
            "maman|Bravo.",
            "papa|Merci de vous être baissées.",
            f"narrateur|{cd}",
            "narrateur|Ils croquent, les pieds sous la table.",
            "narrateur|Le four ronronne, et reste.",
        )
    return L(
        "narrateur|Dans le bol rouge, pas dans le panier.",
        "enfant-f|J'ai failli dire le panier.",
        "maman|Tu as attendu ma fin.",
        "papa|Merci, Chouchou.",
        "narrateur|Une fraise casse, tout doux, entre les dents.",
        f"narrateur|{cd}",
        "narrateur|Le panier garde son ombre, tout seul.",
        "narrateur|Le four sent le beurre, enfin.",
    )


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
        scale, rate = (1.28, "slow") if kind in ("passage_question", "transition_question") else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Chouchou, papa, maman"
    out["setting"] = "cuisine, dimanche, goûter aux fraises"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "il faut attendre",
        "lila",
        "jules",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "cabanon",
        "cerisier",
        "biscuit",
        "capitaine",
        "plic",
        "volet jaune",
        "bac à sable",
        "toboggan",
        "balançoire",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
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


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Un carré de soleil tient sur le plancher de la cuisine.",
        "narrateur|La farine a laissé un nuage, tout blanc.",
        "narrateur|Le saladier de bois sent encore le lait.",
        "maman|J'ai sorti le beurre, il ramollit.",
        "papa|Les fraises du marché attendent dans l'évier.",
        "narrateur|En ce moment, Chouchou pousse une chaise, tout doux.",
        "enfant-f|On fait le gâteau, maman ?",
        "maman|Oui, le gâteau aux fraises.",
        "enfant-f|Où est la farine ?",
        "narrateur|Maman ouvre la bouche, puis s'arrête.",
        "papa|Elle cherche encore le mot.",
        "maman|Prends tes affaires, d'abord.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près de l'évier.",
        "narrateur|Le saladier, la cuillère, et le tablier.",
        "papa|Tu prends quoi, d'abord ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le saladier", "la cuillère", "le tablier")

    t3_by_t2 = {
        1: t3lab("attendre", "le tabouret", "papa porte"),
        2: t3lab("s'asseoir", "la lampe", "le linge"),
        3: t3lab("compter", "le panier", "le bol"),
    }
    q_by_t1 = {
        1: qf(
            "le saladier",
            "saladier | le saladier | un saladier | le bol | bol | le bois",
            "Chouchou a pris le saladier en premier. Elle a pris quoi ?",
        ),
        2: qf(
            "la cuillère",
            "cuillère | la cuillère | une cuillère | la cuiller | cuiller | le bois",
            "La cuillère de bois brillait. Chouchou a pris quoi ?",
        ),
        3: qf(
            "le tablier",
            "tablier | le tablier | un tablier | le tissu",
            "Le tablier faisait un pli. Elle a enfilé quoi ?",
        ),
    }

    for t1 in (1, 2, 3):
        p = pre(t1)
        s[p] = t1_pass(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = q_by_t1[t1]
        s[f"{p}_C0001"] = t1_c(t1)
        s[f"{p}_T0002_P0000"] = t2_q(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le placard", "le tiroir", "le garde-manger")
        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_pass(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_q(t2)
            extras[f"{sp}_T0003_P0000"] = t3_by_t2[t2]
            for t3 in (1, 2, 3):
                tp = f"{sp}_T0003_P000{t3}"
                s[tp] = t3_pass(t1, t2, t3)
                s[f"{tp}_F0001"] = t3_fin(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Chouchou veut un gâteau aux fraises. "
        "T1 = saladier / cuillère / tablier, les trois partent. "
        "T2×T3 = 9 aventures : placard (attendre, tabouret, papa porte), "
        "tiroir (s'asseoir, lampe, linge), garde-manger (compter, panier, bol). "
        "Maman cherche ses mots ; Chouchou laisse la phrase aller jusqu'au bout. "
        "Le gâteau sent le beurre.",
        "Gabarit Lila/Tom/slogan jeté. Autre récit que DIF-018 (cuisine, pas jardin). "
        "Désir ≠ leçon. chunk_id inchangés. check() N2. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
