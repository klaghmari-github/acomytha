#!/usr/bin/env python3
"""TREE-DIF-018 — Les biscuits de Mila au fond du jardin. DIF.PAR.002, N3."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N3 = LIMITS["N3"]
SID = "TREE-DIF-018"
TITLE = "Les biscuits de Mila au fond du jardin"
FIL = (
    "Raphaël veut les biscuits que Mila a cachés dans le jardin. "
    "Mila connaît l'endroit, mais elle cherche ses mots, phrase après phrase. "
    "Il prépare d'abord le sac, le carnet ou la clochette ; les trois partent. "
    "Au cabanon, sous le cerisier ou près de la table, chaque lieu a son obstacle. "
    "Il laisse Mila finir. Les biscuits arrivent."
)


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
        label="le sac",
        coda="Le sac en toile pèse un peu, enfin.",
        touch="La toile du sac est rêche, déjà chaude.",
    ),
    2: dict(
        label="le carnet",
        coda="Le carnet garde le dernier mot, tout net.",
        touch="Le papier du carnet est un peu gondolé.",
    ),
    3: dict(
        label="la clochette",
        coda="La clochette tinte une fois, puis se tait.",
        touch="Le métal de la clochette est froid, encore.",
    ),
}


def t1_pass(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Raphaël saisit d'abord le sac en toile.",
            "enfant-m|Pour les biscuits, après.",
            "papa|Il sent encore le pain.",
            "narrateur|La toile est rêche, déjà chaude au soleil.",
            "maman|Le carnet, ensuite, contre le sac.",
            "narrateur|Mila le glisse, tout doux, à l'intérieur.",
            "copine|La clochette aussi.",
            "narrateur|Elle tinte une fois, tout court.",
            "enfant-m|Maintenant, tu dis où.",
            "narrateur|Mila ouvre la bouche, puis s'arrête.",
            "papa|On marche, elle va finir.",
            "enfant-m|D'accord.",
        )
    if t1 == 2:
        return L(
            "narrateur|Raphaël ouvre d'abord le carnet de Mila.",
            "enfant-m|Il y a un mot, à moitié.",
            "maman|Le crayon a laissé un trait.",
            "narrateur|Le papier est un peu gondolé, encore.",
            "papa|Le sac, ensuite, pour porter.",
            "narrateur|Mila passe la lanière à Raphaël.",
            "copine|La clochette, dans ta poche.",
            "narrateur|Le métal reste froid contre le tissu.",
            "enfant-m|Lis-moi l'endroit.",
            "narrateur|Mila pose un doigt sous le trait.",
            "copine|Pas encore.",
            "papa|Le mot va arriver.",
        )
    return L(
        "narrateur|Raphaël prend d'abord la clochette, au bord.",
        "enfant-m|Pour crier quand on trouve.",
        "papa|Elle tinte trop tôt, parfois.",
        "narrateur|Le métal est froid, encore à l'ombre.",
        "maman|Le sac, ensuite, et le carnet.",
        "narrateur|Mila les pose contre lui, l'un après l'autre.",
        "copine|Pas de tintement, pas encore.",
        "enfant-m|Alors dis-moi où.",
        "narrateur|Mila inspire, les lèvres déjà rondes.",
        "narrateur|Elle ne dit rien, encore.",
        "maman|Elle cherche la suite.",
        "enfant-m|J'attends.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le sac en toile est déjà dans sa main.",
            "maman|Raphaël a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le carnet est ouvert, sur un trait.",
            "papa|Raphaël a ouvert quoi ?",
        )
    return L(
        "narrateur|Un petit tintement vient de sa main.",
        "maman|Raphaël a pris quoi, au bord ?",
    )


def t1_c(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le sac.",
            "papa|Oui.",
            "narrateur|Le carnet et la clochette voyagent avec.",
            "copine|Je vais dire l'endroit.",
            "maman|On marche, tout doux.",
            "enfant-m|Je suis prêt.",
            "papa|Mila, tu nous guides ?",
            "copine|Oui.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Le carnet.",
            "maman|Oui.",
            "narrateur|Le sac pend à son épaule, déjà.",
            "narrateur|La clochette dort dans la poche.",
            "copine|Le trait n'est pas fini.",
            "papa|On marche, le mot suivra.",
            "enfant-m|D'accord, Mila.",
            "maman|Vous restez ensemble.",
        )
    return L(
        "enfant-m|La clochette.",
        "papa|Oui.",
        "narrateur|Le sac et le carnet pèsent contre lui.",
        "copine|Pas de tintement, avant le goûter.",
        "maman|Elle va dire la suite.",
        "enfant-m|J'écoute.",
        "papa|On avance, alors ?",
        "copine|Oui, papa.",
    )


def t2_q(t1: int) -> list[str]:
    head = {
        1: "Le sac tape un peu sa hanche, à chaque pas.",
        2: "Le carnet claque une fois, contre le sac.",
        3: "La clochette reste muette, dans la poche.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Le cabanon, le cerisier, et la table attendent.",
        "papa|On cherche où, d'abord ?",
    )


def t2_pass(t1: int, t2: int) -> list[str]:
    head = {
        1: "Le sac en toile pose un carré d'ombre.",
        2: "Le carnet s'ouvre sur un mot inachevé.",
        3: "La clochette reste silencieuse, dans sa main.",
    }[t1]
    if t2 == 1:
        extra = {
            1: "Le sac glisse vers le seuil, tout lourd.",
            2: "Un trait du carnet s'arrête au milieu.",
            3: "Raphaël serre la clochette, sans la bouger.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|Ils s'arrêtent devant le cabanon.",
            f"narrateur|{extra}",
            "narrateur|L'ombre sent le bois chaud, et la poussière.",
            "enfant-m|C'est ici ?",
            "copine|C'est dans la caisse.",
            "narrateur|Mila lève un doigt, encore.",
            "narrateur|Raphaël ouvre la bouche, puis la referme.",
            "maman|Les caisses sont trop nombreuses.",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "Le sac s'accroche à une racine, puis lâche.",
            2: "Mila pose le carnet sur une pierre plate.",
            3: "Un oiseau fait tinter presque la clochette.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|Sous le cerisier, l'herbe est tachetée.",
            f"narrateur|{extra}",
            "enfant-m|Les pierres se ressemblent toutes.",
            "copine|Sous la pierre.",
            "narrateur|Mila s'arrête, les lèvres encore rondes.",
            "narrateur|Raphaël avance un pied, puis recule.",
            "papa|Il y en a trop, des pierres.",
            "maman|La suite n'est pas dite.",
            "papa|Vous trouvez comment ?",
        )
    extra = {
        1: "Le sac penche contre un pied de table.",
        2: "Le carnet frôle la nappe, qui vole déjà.",
        3: "La clochette cogne le bois, un petit toc.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Près de la table, le vent prend la nappe.",
        f"narrateur|{extra}",
        "enfant-m|Derrière quoi ?",
        "copine|Derrière le.",
        "narrateur|Mila cherche, un doigt en l'air.",
        "narrateur|Un seau et un vase attendent, tous les deux.",
        "papa|Le vent mélange les choses.",
        "maman|Elle n'a pas fini sa phrase.",
        "papa|Vous faites quoi, alors ?",
    )


def t3_q(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Dans le cabanon, Mila n'a pas fini.",
            "papa|Attendre, la lampe, ou la caisse basse ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Sous le cerisier, la suite manque encore.",
            "maman|La pierre, le dessin, ou les racines ?",
        )
    return L(
        "narrateur|Près de la table, le vent tient encore la nappe.",
        "papa|La nappe, s'asseoir, ou le vase ?",
    )


def t3_pass(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "Le sac reste au seuil, tout sage.",
        2: "Le carnet attend un dernier trait.",
        3: "La clochette dort contre sa paume.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-m|On attend.",
            "copine|Oui.",
            "narrateur|Ils s'assoient sur le seuil, l'un contre l'autre.",
            "narrateur|Une abeille passe, puis plus rien.",
            "copine|La bleue.",
            "enfant-m|La caisse bleue.",
            f"narrateur|{col}",
            "papa|Tu as laissé la fin arriver.",
            "maman|Elle est là, maintenant.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "papa|J'allume la petite lampe.",
            "narrateur|Un rond jaune court sur les caisses.",
            "copine|Près de la.",
            "narrateur|Raphaël ne dit rien.",
            "copine|Près de la fenêtre.",
            "enfant-m|Je vois le bleu, maintenant.",
            f"narrateur|{col}",
            "maman|La lumière a aidé le mot.",
            "papa|Vous avez écouté jusqu'au bout.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-m|On se baisse.",
            "narrateur|Ils s'accroupissent près des caisses.",
            "copine|Pas la haute.",
            "narrateur|Raphaël garde sa bouche fermée.",
            "copine|La basse.",
            "enfant-m|Celle-là, tout près du sol.",
            f"narrateur|{col}",
            "papa|Tu n'as pas deviné trop tôt.",
            "maman|La phrase est complète, enfin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-m|On ne touche pas encore.",
            "narrateur|Les deux restent debout, tout calmes.",
            "copine|La ronde.",
            "enfant-m|Celle qui ressemble à une lune.",
            "narrateur|Ils soulèvent la pierre ronde, ensemble.",
            f"narrateur|{col}",
            "maman|Le mot est venu, tout seul.",
            "papa|Vous l'avez laissée finir.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "copine|Je dessine.",
            "narrateur|Mila trace un rond, dans le carnet.",
            "narrateur|Le crayon gratte, puis s'arrête.",
            "copine|Ronde.",
            "enfant-m|Comme ton dessin.",
            "narrateur|Ils posent le carnet contre la pierre ronde.",
            f"narrateur|{col}",
            "papa|Le dessin a tenu le mot.",
            "maman|Vous avez lu ensemble.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-m|On s'assoit dans les racines.",
            "narrateur|L'écorce est rêche, un peu fraîche.",
            "copine|À gauche.",
            "narrateur|Raphaël tourne la tête, sans parler.",
            "copine|Sous les racines, à gauche.",
            "enfant-m|Je vois le coin, maintenant.",
            f"narrateur|{col}",
            "maman|Les racines ont gardé le secret.",
            "papa|Tu as écouté la fin.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-m|On tient la nappe.",
            "copine|Moi aussi.",
            "narrateur|Le vent lâche le tissu, tout doux.",
            "copine|Le vase.",
            "enfant-m|Derrière le vase.",
            f"narrateur|{col}",
            "papa|La nappe s'est tue, le mot aussi.",
            "maman|Vous l'avez entendue jusqu'au bout.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-m|On s'assoit, d'abord.",
            "narrateur|Le banc de bois est tiède, encore.",
            "copine|Derrière le vase blanc.",
            "enfant-m|Pas le seau.",
            "narrateur|Ils se lèvent, tout calmes, ensemble.",
            f"narrateur|{col}",
            "papa|S'asseoir a ralenti les mots.",
            "maman|La phrase a eu sa place.",
        )
    return L(
        "narrateur|Le seau brille, plus proche que le vase.",
        "enfant-m|Le seau ?",
        "narrateur|Raphaël referme sa bouche, tout de suite.",
        "copine|Le vase.",
        "enfant-m|Derrière le vase, d'accord.",
        f"narrateur|{col}",
        "maman|Tu as laissé la vraie fin.",
        "papa|Le seau peut attendre.",
    )


def t3_fin(t1: int, t2: int, t3: int) -> list[str]:
    cd = PREP[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La caisse bleue s'ouvre, un petit clic.",
            "narrateur|Une boîte de biscuits sent le beurre.",
            "enfant-m|On les a.",
            "copine|Parce que tu as attendu.",
            "papa|Merci, Raphaël.",
            "maman|Un pour Mila, un pour toi.",
            f"narrateur|{cd}",
            "narrateur|Le seuil du cabanon redevient tiède, tout calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Près de la fenêtre, la caisse bleue attend.",
            "enfant-m|Le rond jaune l'a montrée.",
            "copine|Et le mot, après.",
            "maman|Bravo.",
            "papa|Merci d'avoir écouté.",
            "narrateur|Ils croquent, tout petit, à l'ombre.",
            f"narrateur|{cd}",
            "narrateur|La poussière du cabanon se repose, enfin.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La caisse basse livre la boîte, tout de suite.",
            "enfant-m|Elle était trop près du sol.",
            "copine|La haute était vide.",
            "papa|Merci de ne pas avoir deviné.",
            "maman|Le beurre sent encore, tout chaud.",
            f"narrateur|{cd}",
            "narrateur|Ils s'assoient sur le seuil, les miettes aux doigts.",
            "narrateur|Le cabanon garde son ombre, plus rien d'autre.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Sous la pierre ronde, la boîte est fraîche.",
            "enfant-m|Comme une lune, tu avais dit.",
            "copine|Oui.",
            "papa|Merci d'avoir attendu le mot.",
            "maman|Goûtez, tout doux.",
            f"narrateur|{cd}",
            "narrateur|Une cerise tombe, trop loin, dans l'herbe.",
            "narrateur|Le cerisier redevient silencieux.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le dessin du carnet colle encore à la pierre.",
            "copine|Le rond était le bon.",
            "enfant-m|On a lu ensemble.",
            "maman|Bravo, vous deux.",
            "papa|Merci, Raphaël.",
            "narrateur|Un biscuit casse, tout net, entre les dents.",
            f"narrateur|{cd}",
            "narrateur|L'herbe tachetée se calme, sous les branches.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|À gauche, sous les racines, la boîte attend.",
            "enfant-m|Tu as dit à gauche, à la fin.",
            "copine|Oui, à la fin.",
            "papa|Merci d'avoir écouté jusque-là.",
            "maman|Les miettes, dans l'herbe, tout petit.",
            f"narrateur|{cd}",
            "narrateur|Une racine reprend sa place, tout rêche.",
            "narrateur|Le cerisier n'a plus de secret, ce soir.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Derrière le vase, la boîte touche le bois.",
            "enfant-m|La nappe s'est tue, d'abord.",
            "copine|Puis j'ai fini.",
            "papa|Merci d'avoir tenu le tissu.",
            "maman|Un biscuit chacun, sur la nappe.",
            f"narrateur|{cd}",
            "narrateur|Le vent passe ailleurs, plus loin.",
            "narrateur|La table redevient une table, tout simple.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Derrière le vase blanc, ça sent le beurre.",
            "enfant-m|Le seau n'avait rien.",
            "copine|Le banc nous a aidés.",
            "maman|Bravo.",
            "papa|Merci de vous être assis.",
            f"narrateur|{cd}",
            "narrateur|Ils croquent, les pieds sous la table.",
            "narrateur|La nappe bleue retombe, et reste.",
        )
    return L(
        "narrateur|Derrière le vase, pas derrière le seau.",
        "enfant-m|J'ai failli dire le seau.",
        "copine|Tu as attendu ma fin.",
        "papa|Merci, Raphaël.",
        "maman|Le biscuit casse, tout doux.",
        f"narrateur|{cd}",
        "narrateur|Le seau garde son ombre, tout seul.",
        "narrateur|La nappe bleue retombe, tout calme.",
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
    out["characters"] = "Raphaël, Mila, papa, maman"
    out["setting"] = "jardin, fin d'après-midi, terrasse tiède"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
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
        "jules",
        "sami",
    ):
        if bad in blob:
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
        "narrateur|Le romarin le long du mur sent encore le soleil.",
        "narrateur|Les carreaux de la terrasse sont tièdes sous les pieds.",
        "narrateur|Une nappe bleue se soulève un peu, puis retombe.",
        "narrateur|Les tomates brillent, encore mouillées d'eau.",
        "papa|J'ai arrosé, tout doux.",
        "maman|La menthe est prête, pour la carafe.",
        "narrateur|En ce moment, le portail grince, tout léger.",
        "narrateur|Mila entre, un doigt contre ses lèvres.",
        "copine|J'ai caché le goûter.",
        "enfant-m|Des biscuits ?",
        "copine|Oui.",
        "enfant-m|Où ?",
        "narrateur|Mila ouvre la bouche, puis s'arrête.",
        "maman|Elle cherche encore la suite.",
        "papa|Prenez vos affaires, avant le vent.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près de la nappe.",
        "narrateur|Le sac, le carnet, et la clochette.",
        "papa|Tu prends quoi, d'abord ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le sac", "le carnet", "la clochette")

    t3_by_t2 = {
        1: t3lab("attendre", "la lampe", "la caisse basse"),
        2: t3lab("la pierre", "le dessin", "les racines"),
        3: t3lab("la nappe", "s'asseoir", "le vase"),
    }
    q_by_t1 = {
        1: qf(
            "le sac",
            "sac | le sac | un sac | sac en toile | la toile",
            "Raphaël a pris le sac en premier. Il a pris quoi ?",
        ),
        2: qf(
            "le carnet",
            "carnet | le carnet | un carnet | le papier",
            "Le carnet était ouvert. Raphaël a ouvert quoi ?",
        ),
        3: qf(
            "la clochette",
            "clochette | la clochette | une clochette | la cloche",
            "Un tintement est venu de sa main. Il a pris quoi ?",
        ),
    }

    for t1 in (1, 2, 3):
        p = pre(t1)
        s[p] = t1_pass(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = q_by_t1[t1]
        s[f"{p}_C0001"] = t1_c(t1)
        s[f"{p}_T0002_P0000"] = t2_q(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le cabanon", "le cerisier", "la table")
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
        "Raphaël veut les biscuits que Mila a cachés. "
        "T1 = sac / carnet / clochette, les trois partent. "
        "T2×T3 = 9 aventures : cabanon (attendre, lampe, caisse basse), "
        "cerisier (pierre, dessin, racines), table (nappe, s'asseoir, vase). "
        "Mila cherche ses mots ; Raphaël laisse la phrase aller jusqu'au bout. "
        "Les biscuits arrivent.",
        "Gabarit Jules/Tom/slogan jeté. Désir ≠ leçon. chunk_id inchangés. "
        "check() N3. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
