#!/usr/bin/env python3
"""TREE-DIF-050 — Les deux cerceaux d'Aniss, jusqu'à la porte jaune (N2, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-050"
N2 = 15
TITLE = "Les deux cerceaux d'Aniss, jusqu'à la porte jaune"
FIL = (
    "Une porte jaune attend au bout du chemin. Aniss veut y faire arriver "
    "deux cerceaux, avec Mila. Le grand orange est à lui, le petit bleu à elle, "
    "plus petite. Ils prennent d'abord le grand, le petit ou le bâton ; les trois "
    "partent. Le chemin avale, l'herbe arrête, le perron est trop haut. "
    "Neuf façons. Les deux cerceaux tapent la porte."
)
CHARS = "Aniss, Mila, papa, maman"
SETTING = "chemin du village : terre, herbe du tilleul, perron"


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


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
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tailles différentes",
        "plus petit ou plus grand",
        "jouer ensemble",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "capitaine",
        "plic",
        "volet jaune",
        "veau",
        "le lait",
        "étable",
        "abreuvoir",
        "cacao",
        "étagère",
        "bac à sable",
        "toboggan",
        "balançoire",
        "kenzo",
        "sami",
        " léa",
        " lea",
        "tom ",
        "doudou",
        "ballon",
        "pommier",
        "marelle",
        "soleil en papier",
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
        "lab": "le grand cerceau",
        "cap": "Le grand cerceau",
        "t1q": "contre la hanche",
        "t1acc": "hanche | la hanche | contre la hanche | sa hanche",
        "t1retry": "Le grand cerceau est contre la hanche.",
        "coda": "narrateur|Le grand cerceau sèche contre le seuil, tout calme.",
    },
    2: {
        "lab": "le petit cerceau",
        "cap": "Le petit cerceau",
        "t1q": "dans la main",
        "t1acc": "main | la main | dans la main | sa main",
        "t1retry": "Le petit cerceau est dans la main.",
        "coda": "narrateur|Le petit cerceau sèche contre le seuil, tout calme.",
    },
    3: {
        "lab": "le bâton",
        "cap": "Le bâton",
        "t1q": "sous le bras",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "Le bâton est sous le bras.",
        "coda": "narrateur|Le bâton sèche contre le seuil, tout calme.",
    },
}

T3_LABS = {
    1: ("les mains de Mila", "le pont du grand", "rouler à deux"),
    2: ("le couloir de Mila", "les mains d'Aniss", "écarter ensemble"),
    3: ("Aniss porte", "Mila reçoit", "la dernière marche"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss serre le grand cerceau, encore chaud.",
            "enfant-m|Il sent le soleil, tout près.",
            "maman|Garde-le contre ta hanche, tout droit.",
            "narrateur|Le bois glisse un peu, puis tient.",
            "papa|Le petit, ensuite, pour Mila.",
            "narrateur|Mila serre le petit bleu, tout près.",
            "narrateur|Papa glisse le bâton contre le grand.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Mila, tu viens jusqu'à la porte ?",
            "enfant-f|J'arrive, Aniss.",
            "papa|Le grand d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss tend le petit cerceau, tout bleu.",
            "enfant-m|Celui-là, c'est pour toi.",
            "papa|Tiens-le dans ta main, tout droit.",
            "narrateur|Le bois tape un petit toc.",
            "maman|Le grand, ensuite, contre la hanche.",
            "narrateur|Mila glisse le bâton sous son bras.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Mila, on y va.",
            "enfant-f|Je suis là.",
            "maman|Le petit d'abord, il est prêt.",
        )
    return L(
        "narrateur|Aniss attrape le bâton, un peu rêche.",
        "enfant-m|Il va pousser les deux cerceaux.",
        "maman|Glisse-le sous ton bras, tout doux.",
        "narrateur|Le bois sent la poussière chaude.",
        "papa|Les deux cerceaux, avec vous.",
        "narrateur|Mila porte le petit, Aniss le grand.",
        "narrateur|Les trois affaires partent ensemble.",
        "enfant-m|Mila, vite !",
        "enfant-f|J'arrive près du bâton.",
        "papa|Le bâton d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La hanche porte le grand cerceau, tout orange.",
            "enfant-f|Il me monte trop, moi.",
            "enfant-m|Moi, il me va.",
            "maman|Mila est plus petite, c'est tout.",
            "papa|On avance vers la porte ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La main de Mila tient le petit, tout bleu.",
            "enfant-m|Le mien est trop large pour toi.",
            "enfant-f|Le bleu, je le tiens bien.",
            "papa|Ça sent la poussière, sur le bois.",
            "maman|Vos pieds, sur le chemin ?",
            "enfant-f|Oui, maman.",
        )
    return L(
        "narrateur|Le bâton reste sous le bras, tout rêche.",
        "enfant-f|Il dépasse encore, un peu.",
        "enfant-m|Je le baisse pour toi.",
        "maman|Le chemin est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le grand cerceau tape la hanche, tout bas.",
        2: "Le petit cerceau frotte la main, un peu rêche.",
        3: "Le bâton frotte le bras, tout doux.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Le chemin de terre a des trous.",
        "narrateur|L'herbe du tilleul est trop haute.",
        "narrateur|Le perron de pierre est trop haut.",
        "papa|Vous roulez où, vers la porte ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le grand cerceau bute contre une ornière.",
            2: "narrateur|Le petit cerceau tombe dans une ornière.",
            3: "narrateur|Le bâton bute contre une ornière.",
        }[t1]
        return L(
            lead,
            "narrateur|Le chemin de terre avale le petit bleu.",
            "enfant-f|Je ne le vois plus !",
            "enfant-m|Moi, je vois le trou, d'en haut.",
            "narrateur|Mila se penche, le nez tout près.",
            "narrateur|Ses mains passent dans le creux.",
            f"narrateur|{o['cap']} attend au bord, tout calme.",
            "papa|Tes épaules passent, Mila.",
            "maman|Toi tu vois le haut, elle le fond.",
            "enfant-m|On le sort comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le grand cerceau passe au-dessus de l'herbe.",
            2: "narrateur|Le petit cerceau s'arrête dans l'herbe.",
            3: "narrateur|Le bâton accroche un brin, tout vert.",
        }[t1]
        return L(
            lead,
            "narrateur|L'herbe du tilleul arrive à la poitrine de Mila.",
            "enfant-f|Je ne vois que le vert !",
            "enfant-m|Moi, je vois le bleu, par-dessus.",
            "narrateur|Aniss a les yeux plus hauts.",
            "narrateur|Mila a les genoux plus près du sol.",
            f"narrateur|{o['cap']} reste coincé, tout près.",
            "papa|Tes yeux sont plus hauts, Aniss.",
            "maman|Les mains de Mila sont plus près.",
            "enfant-m|On le trouve comment ?",
        )
    lead = {
        1: "narrateur|Le grand cerceau tape la marche du bas, toc.",
        2: "narrateur|Le petit cerceau refuse la marche du bas.",
        3: "narrateur|Le bâton tape la marche du bas, toc.",
    }[t1]
    return L(
        lead,
        "narrateur|Le perron de pierre est trop haut pour le bleu.",
        "enfant-m|Je peux le soulever, moi.",
        "enfant-f|Moi, je n'arrive pas.",
        "narrateur|Aniss a les bras plus longs.",
        "narrateur|Mila a les pieds sur la marche du bas.",
        f"narrateur|{o['cap']} attend au bas, tout rêche.",
        "papa|La marche est trop haute, pour le bleu.",
        "maman|Mila, tu restes en bas ?",
        "enfant-f|On monte comment, tous les deux ?",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le petit bleu reste dans le trou.",
            "papa|Les mains de Mila, le pont, ou rouler à deux ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le petit bleu se cache dans l'herbe.",
            "maman|Le couloir, les mains d'Aniss, ou écarter ?",
        )
    return L(
        "narrateur|Le petit bleu reste trop bas, trop loin.",
        "papa|Aniss porte, Mila reçoit, ou la dernière marche ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Aniss tient le grand, comme un abri.",
            2: "narrateur|Aniss attend le petit, tout près.",
            3: "narrateur|Aniss pose le bâton en travers du trou.",
        }[t1]
        return L(
            "enfant-f|Je passe les mains, Aniss.",
            "narrateur|Mila rampe, tout petite, vers le creux.",
            "enfant-m|Doucement.",
            use,
            "narrateur|Les doigts de Mila trouvent le bleu, tout lent.",
            "enfant-f|Je le tiens !",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Le petit cerceau remonte à leur hauteur.",
            "enfant-m|Regarde, Mila.",
            "enfant-f|Il est à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le grand cerceau fait un pont, au-dessus.",
            2: "narrateur|Le petit attend, un moment, sous le bois.",
            3: "narrateur|Le bâton fait un pont, au-dessus.",
        }[t1]
        return L(
            "enfant-m|Je pose le grand, comme un pont.",
            "papa|Je te tiens, Aniss.",
            "narrateur|Aniss couche le bois, plus haut que Mila.",
            "enfant-f|Je vois le bleu !",
            "narrateur|Mila pousse, d'en bas.",
            "narrateur|Le petit glisse vers elle.",
            "enfant-m|Il est à toi, un moment.",
            "maman|Vous le partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        catch = {
            1: "narrateur|Le grand cerceau guide le petit, tout doux.",
            2: "narrateur|Le petit cerceau reprend la terre plate.",
            3: "narrateur|Le bâton guide les deux, tout doux.",
        }[t1]
        return L(
            "enfant-m|On attend un peu.",
            "enfant-f|Moi aussi, j'attends.",
            "narrateur|Un souffle passe sur la poussière.",
            "narrateur|Le petit bleu se dégage, tout seul.",
            catch,
            "papa|Il est venu vers vous.",
            "enfant-f|On l'a repris.",
            "enfant-m|Il brille encore.",
            "maman|Vos cheveux sentent la terre.",
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Mila pousse le bleu vers le grand.",
            2: "narrateur|Mila ramène le petit, tout près.",
            3: "narrateur|Mila pousse le bleu vers le bâton.",
        }[t1]
        return L(
            "enfant-f|Je rampe, tout près du sol.",
            "enfant-m|Je te guide, d'en haut.",
            "narrateur|Mila écarte deux brins, tout doux.",
            "narrateur|Le petit bleu est là, collé.",
            "enfant-f|Je le tiens !",
            carry,
            "papa|Tes mains étaient à la bonne hauteur.",
            "enfant-m|Passe-le, un peu.",
            "enfant-f|Il est encore froid.",
        )
    if t2 == 2 and t3 == 2:
        reach = {
            1: "narrateur|Aniss tend le grand, bras tout longs.",
            2: "narrateur|Aniss tend la main, bras tout longs.",
            3: "narrateur|Aniss tend le bâton, bras tout longs.",
        }[t1]
        return L(
            "enfant-m|Je reste ici, plus haut.",
            "enfant-f|Je vais où tu dis.",
            reach,
            "narrateur|Aniss voit le rond bleu, par-dessus.",
            "narrateur|Mila avance vers le point d'ombre.",
            "enfant-f|Je le tiens !",
            "maman|Tes yeux ont trouvé le chemin.",
            "enfant-m|Il sent l'herbe.",
            "papa|Soufflez dessus, tout léger.",
        )
    if t2 == 2 and t3 == 3:
        nest = {
            1: "narrateur|Le grand cerceau devient un nid, dans l'herbe.",
            2: "narrateur|Le petit cerceau devient un nid, dans l'herbe.",
            3: "narrateur|Le bâton devient un nid, dans l'herbe.",
        }[t1]
        return L(
            "enfant-m|Papa, écarte un peu ?",
            "papa|Je fais un chemin, tout doux.",
            "narrateur|L'herbe s'ouvre, comme une porte.",
            "narrateur|Le petit bleu apparaît, collé.",
            nest,
            "enfant-f|On le prend ensemble.",
            "enfant-m|Oui.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux paires de mains tiennent le bois.",
        )
    if t2 == 3 and t3 == 1:
        hold = {
            1: "narrateur|Mila garde le grand au pied du perron.",
            2: "narrateur|Mila garde le petit, un moment, en bas.",
            3: "narrateur|Mila garde le bâton au pied du perron.",
        }[t1]
        return L(
            "enfant-m|Je le soulève, moi.",
            hold,
            "narrateur|Les bras d'Aniss portent le bleu, tout haut.",
            "enfant-m|Il monte !",
            "narrateur|Le petit cerceau pose un toc, en haut.",
            "enfant-f|Je le vois arriver.",
            "papa|Tes bras allaient assez loin.",
            "maman|Mila tenait bien le bas.",
            "enfant-m|Il est à nous.",
        )
    if t2 == 3 and t3 == 2:
        up = {
            1: "narrateur|Aniss tend le grand, depuis la marche.",
            2: "narrateur|Aniss tend le petit, depuis la marche.",
            3: "narrateur|Aniss tend le bâton, depuis la marche.",
        }[t1]
        return L(
            "enfant-m|Reste en bas, Mila.",
            "enfant-f|Je tends, d'ici.",
            up,
            "narrateur|Aniss fait basculer le bleu, tout doux.",
            "narrateur|Le bois tombe dans les mains d'en bas.",
            "enfant-f|Je le tiens !",
            "papa|Chacun a fait sa part.",
            "enfant-m|Il sent le soleil.",
            "maman|Vos bras n'avaient pas la même longueur.",
        )
    two = {
        1: "narrateur|Papa pose le grand sur la dernière marche.",
        2: "narrateur|Papa pose le petit sur la dernière marche.",
        3: "narrateur|Papa pose le bâton sur la dernière marche.",
    }[t1]
    return L(
        "enfant-m|On monte à deux ?",
        "enfant-f|Oui, tout doux.",
        two,
        "narrateur|Papa tient la pierre, tout ferme.",
        "narrateur|Aniss et Mila poussent ensemble.",
        "enfant-m|Il vient !",
        "enfant-f|Je le sens.",
        "maman|Vous avez poussé ensemble.",
        "papa|La marche est restée à sa place.",
        "narrateur|Les deux cerceaux tapent la porte, un toc.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils rentrent, les deux cerceaux au creux.",
            "enfant-f|Il sent encore la terre.",
            "enfant-m|Tes épaules l'ont fait monter.",
            "papa|Vous l'avez repris, enfin.",
            "maman|Posez-les près de la porte jaune.",
            "narrateur|Le tilleul garde une ombre, tout petit.",
            coda,
            "narrateur|Une abeille passe, plus loin.",
            "narrateur|Le bleu dort contre l'orange.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous le pont de bois, la maison paraît petite.",
            "enfant-m|Mila, tu l'as vu glisser.",
            "enfant-f|Oui, tout près de mes mains.",
            "papa|Je t'ai tenu, pas trop longtemps.",
            "maman|Vos têtes, haute et basse, rentrent.",
            "narrateur|Le petit reste dans la paume de Mila.",
            coda,
            "narrateur|Un brin de terre reste collé aux cheveux.",
            "narrateur|La porte jaune sent encore le soleil.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le souffle du chemin les suit jusqu'à la porte.",
            "enfant-f|Il est venu vers nous.",
            "enfant-m|On a attendu, tous les deux.",
            "maman|Il n'était plus trop coincé.",
            "papa|La poussière perle encore, sur le bois.",
            f"narrateur|{o['cap']} pose une feuille, tout léger.",
            "narrateur|La porte claque, tout doux.",
            "narrateur|Une odeur de terre reste dans l'entrée.",
            "narrateur|Le bleu veille près des souliers.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Ils rentrent avec de l'herbe aux genoux.",
            "enfant-f|Mes mains savaient le chemin.",
            "enfant-m|Moi, je voyais trop haut.",
            "papa|Vous avez suivi ce qui était à vous.",
            "maman|Soufflez le dernier brin, dehors.",
            "enfant-m|Ils sont pour la porte, maintenant.",
            "enfant-f|Il est un peu froid encore.",
            coda,
            "narrateur|L'herbe sèche déjà sur le palier.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils n'ont pas couru dans toute l'herbe.",
            "enfant-m|Je l'ai vu par-dessus.",
            "enfant-f|Tes yeux étaient assez hauts.",
            "maman|L'herbe sent fort, sur vos mains.",
            "papa|Lavez-les, tout doux, au bac.",
            f"narrateur|{o['cap']} garde un brin d'herbe.",
            "enfant-f|Je le tiens, Aniss.",
            "narrateur|Le bac goutte, puis se tait.",
            "narrateur|Les deux cerceaux sèchent près de la fenêtre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Leurs chaussettes portent encore de l'herbe.",
            "enfant-m|Papa a ouvert un chemin.",
            "enfant-f|On l'a pris ensemble.",
            "papa|L'herbe vous a laissé la place.",
            "maman|Changez le linge des pieds, d'abord.",
            coda,
            "narrateur|Une poussière jaune marque le carreau.",
            "enfant-m|Regarde-le, Mila, il brille.",
            "narrateur|Le bleu reste au chaud, près de l'orange.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les bras d'Aniss sont encore chauds.",
            "enfant-f|Tu l'as fait monter pour moi.",
            "enfant-m|Tu tenais le bas.",
            "maman|Essuie tes pieds, sur le paillasson.",
            "papa|Les deux cerceaux sont à vous, maintenant.",
            "narrateur|Mila les pose contre la vitre.",
            coda,
            "narrateur|Un rai de soleil traverse le bleu.",
            "narrateur|Dehors, le perron redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Un peu de soleil les suit jusqu'à la porte.",
            "enfant-m|Tu l'as reçu, d'en bas.",
            "enfant-f|Tes bras l'ont fait tomber.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du perron sèche déjà.",
            f"narrateur|{o['cap']} pose une auréole au carrelage.",
            "enfant-f|Il brille trop, Aniss.",
            "enfant-m|C'est pour ça.",
            "narrateur|La vitre garde le bleu, tout proche.",
        )
    return L(
        "narrateur|Un peu de poussière de pierre reste au seuil.",
        "enfant-m|On a poussé ensemble.",
        "enfant-f|Sans trop monter.",
        "papa|La marche est restée à sa place.",
        "maman|Vos mains sentent encore le soleil.",
        coda,
        "narrateur|Aniss pose les deux cerceaux au rebord.",
        "enfant-f|Tu les as eus, enfin.",
        "narrateur|Le toc de la porte s'endort, tout doux.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "oiseau"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une porte jaune attend au bout du chemin.",
        "narrateur|Le tilleul jette une ombre ronde, toute tiède.",
        "narrateur|La poussière sent le soleil, encore chaud.",
        "narrateur|Un cerceau orange s'appuie contre le mur.",
        "narrateur|Un plus petit dort dans l'herbe.",
        "papa|Tu as vu les deux cerceaux, Aniss ?",
        "enfant-m|Ils veulent aller à la porte.",
        "maman|Mila arrive, plus petite que toi.",
        "narrateur|En ce moment, Aniss touche le bois.",
        "enfant-m|On les emmène tous les deux.",
        "papa|On prépare d'abord, alors ?",
        "maman|Merci, tu les as bien regardés.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du mur.",
        "narrateur|Le grand cerceau, le petit, et le bâton.",
        "maman|Tu prends quoi d'abord, Aniss ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le grand cerceau", "le petit cerceau", "le bâton")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Aniss a mis {o['lab']} {o['t1q']}.",
            "maman|Il est où, ce bois-là ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le chemin de terre", "l'herbe du tilleul", "le perron")

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Une porte jaune attend. Aniss veut y faire arriver deux cerceaux, "
        "avec Mila plus petite. T1 = grand cerceau / petit cerceau / bâton "
        "(les trois partent). T2 = chemin de terre (ornière trop creuse pour "
        "le bleu, Aniss voit d'en haut, Mila d'en bas) / herbe du tilleul "
        "(trop haute pour Mila) / perron trop haut pour le petit. T3 = neuf "
        "résolutions (mains de Mila, pont du grand, rouler à deux ; couloir "
        "de Mila, mains d'Aniss, écarter ensemble ; Aniss porte, Mila reçoit, "
        "dernière marche). La leçon (tailles, jouer ensemble) se vit dans les "
        "gestes, sans slogan. Fin : les deux cerceaux tapent la porte jaune.",
        "N2 ≤ 15. Kenzo / Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre leçon collée remplacé (objet + désir). Autre récit que DIF-040 "
        "(veau/lait/ferme) et DIF-042 (cacao/étagère). Un merci de maman lié "
        "au geste (regarder les cerceaux). Pas de « bon travail ». Audio non cuit.",
    )


if __name__ == "__main__":
    main()
