#!/usr/bin/env python3
"""TREE-DIF-025 — Le défilé de Nina et les deux chapeaux. DIF.COR.002, N2."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-025"
N2 = LIMITS["N2"]
TITLE = "Le défilé de Nina et les deux chapeaux"
FIL = (
    "Nina veut un vrai défilé pour ses deux doudous, chacun son chapeau. "
    "L'ours porte le béret tout rond, la girafe le cône tout mince. "
    "Elle prépare d'abord le tambour, le ruban ou le panier ; les trois partent. "
    "Dans le couloir, le jardin ou l'escalier, chaque lieu a son obstacle. "
    "Les deux chapeaux restent dans le défilé."
)
CHARS = "Nina, papa, maman"
SETTING = "hall de la maison, couloir, jardin, escalier"


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
    for bad in (
        "léa",
        "lea ",
        "tom ",
        "sami",
        "plus rond ou plus mince",
        "le corps n'est pas",
        "tailles différentes",
        "tu as fait du bon travail",
        "bon travail",
        "l'histoire est finie",
        "capitaine",
        "plic",
        "volet jaune",
        "on va apprendre",
        "voici le geste",
        "la première",
        "la deuxième",
        "la troisième",
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
        "lab": "le tambour",
        "cap": "Le tambour",
        "ans": "tambour",
        "acc": "tambour | le tambour | d'abord le tambour | la casserole",
        "retry": "Nina prend le tambour d'abord.",
    },
    2: {
        "lab": "le ruban",
        "cap": "Le ruban",
        "ans": "ruban",
        "acc": "ruban | le ruban | d'abord le ruban | le lien",
        "retry": "Nina prend le ruban d'abord.",
    },
    3: {
        "lab": "le panier",
        "cap": "Le panier",
        "ans": "panier",
        "acc": "panier | le panier | d'abord le panier | le panier d'abord",
        "retry": "Nina prend le panier d'abord.",
    },
}

T3_LABS = {
    1: ("les chaussettes", "le tapis", "les petits pas"),
    2: ("le nœud", "le mur", "le panier-tête"),
    3: ("la même marche", "descendre", "la rampe"),
}


def t1_lead(t1: int) -> dict[str, str]:
    return {
        1: {
            "hip": "Contre sa hanche, le tambour tape un toc.",
            "wait": "Pendant ce temps, le tambour se tait.",
            "use": "Un petit toc donne le rythme.",
            "coda": "Près des chaussons, le tambour reste tiède.",
        },
        2: {
            "hip": "Sa paume sent le ruban, tout soyeux.",
            "wait": "Au poignet, le ruban reste enroulé.",
            "use": "Entre eux deux, le ruban tient, tout doux.",
            "coda": "Près du béret, le ruban garde un pli.",
        },
        3: {
            "hip": "Contre le genou, l'osier du panier penche.",
            "wait": "Au fond du panier, un peu de laine attend.",
            "use": "Avec eux, le panier avance, tout bas.",
            "coda": "Un fil de laine reste dans l'osier.",
        },
    }[t1]


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina prend d'abord le tambour, encore tiède.",
            "enfant-f|Ça va faire la musique.",
            "maman|Doucement, c'est une casserole.",
            "narrateur|La cuillère donne un toc, tout court.",
            "papa|Le ruban aussi, près du sac.",
            "narrateur|Maman glisse le panier contre le mur.",
            "narrateur|Tambour, ruban et panier avancent avec elle.",
            "enfant-f|L'ours, le béret.",
            "narrateur|Elle enfonce la laine, un peu trop large.",
            "enfant-f|La girafe, le cône.",
            "narrateur|Le papier penche déjà vers l'oreille.",
            "papa|Le tambour d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina déroule d'abord le ruban, trop long.",
            "enfant-f|Il va tenir les chapeaux.",
            "papa|Pas trop serré, encore.",
            "narrateur|La soie sent le tiroir, un peu sec.",
            "maman|Le tambour, ensuite, près du sac.",
            "narrateur|Papa pose le panier contre les chaussons.",
            "narrateur|Elle emporte les trois, contre elle.",
            "enfant-f|Le béret sur l'ours.",
            "narrateur|La laine mange un peu ses oreilles.",
            "enfant-f|Le cône sur la girafe.",
            "narrateur|Le papier tremble, trop mince, trop léger.",
            "maman|Le ruban d'abord, il est prêt.",
        )
    return L(
        "narrateur|Nina tire d'abord le panier, l'osier rêche.",
        "enfant-f|Ils voyageront là-dedans.",
        "maman|Tiens-le droit, tout doux.",
        "narrateur|Un brin pique un doigt, puis plus.",
        "papa|Tambour et ruban, avec vous.",
        "narrateur|Il les glisse près des chaussons.",
        "narrateur|Rien ne reste près de la commode.",
        "enfant-f|L'ours dans le panier.",
        "narrateur|Le béret dépasse, tout rond, trop large.",
        "enfant-f|La girafe aussi.",
        "narrateur|Le cône dépasse de l'autre bord, tout mince.",
        "papa|Le panier d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le tambour tient contre sa hanche.",
            "enfant-f|Les deux chapeaux vont marcher.",
            "maman|Le hall vous attend.",
            "papa|On avance par où ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un toc, tout petit, dans le métal.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le ruban fait un nœud lâche, au poignet.",
            "enfant-f|Il va garder les chapeaux.",
            "papa|La soie brille un peu.",
            "maman|Vos pieds, dans les chaussons ?",
            "enfant-f|Oui, maman.",
            "narrateur|Les deux doudous se touchent déjà.",
        )
    return L(
        "narrateur|Le panier penche, deux têtes dehors.",
        "enfant-f|On défile avec eux.",
        "maman|L'osier sent encore le grenier.",
        "papa|On y va, tous les trois ?",
        "enfant-f|Oui.",
        "narrateur|Le béret et le cône ne se ressemblent pas.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le tambour cliquette à chaque pas.",
        2: "Le ruban frotte le poignet, tout doux.",
        3: "Le panier tape le genou, un peu.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Le couloir brille, trop lisse.",
        "narrateur|Dehors, le jardin souffle déjà.",
        "narrateur|Plus loin, l'escalier monte, étroit.",
        "papa|Nina, vous partez où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    lead = t1_lead(t1)
    if t2 == 1:
        extra = {
            1: "Un toc résonne trop fort, sur le carrelage.",
            2: "Contre le mur, le ruban glisse, trop soyeux.",
            3: "Sur les carreaux, le panier part tout seul.",
        }[t1]
        return L(
            f"narrateur|{lead['hip']}",
            "narrateur|Le couloir sent le savon, encore humide.",
            f"narrateur|{extra}",
            "enfant-f|On défile ici.",
            "narrateur|L'ours avance, le béret trop rond glisse.",
            "narrateur|La girafe avance, ses pieds partent de travers.",
            "enfant-f|Ils n'ont pas les mêmes pas !",
            "papa|Le carrelage est trop lisse, voilà tout.",
            "maman|Tu fais comment, avec les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "D'un bord, le tambour s'envole presque.",
            2: "Comme un drapeau, le ruban claque.",
            3: "Le vent prend le papier, le panier penche.",
        }[t1]
        return L(
            f"narrateur|{lead['hip']}",
            "narrateur|Le jardin sent l'herbe coupée, encore chaude.",
            f"narrateur|{extra}",
            "enfant-f|Le défilé, dehors !",
            "narrateur|Le béret tient, trop lourd, trop rond.",
            "narrateur|Le cône s'envole, trop mince, trop léger.",
            "enfant-f|Elle n'a plus son chapeau !",
            "papa|Le vent a choisi, pas toi.",
            "maman|Tu les gardes comment, ensemble ?",
        )
    extra = {
        1: "Sur une marche, le tambour cogne, toc trop fort.",
        2: "À la rampe, le ruban s'accroche, puis lâche.",
        3: "Trop large pour la marche, le panier bute.",
    }[t1]
    return L(
        f"narrateur|{lead['hip']}",
        "narrateur|L'escalier sent le bois ciré, un peu froid.",
        f"narrateur|{extra}",
        "enfant-f|On monte, tous les deux.",
        "narrateur|L'ours est trop large, une patte dehors.",
        "narrateur|Le cône tape le plafond, trop haut.",
        "enfant-f|Ils ne passent pas pareil !",
        "papa|Les marches n'ont pas leur taille.",
        "maman|Tu défiles comment, alors ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le couloir reste trop lisse, trop savonné.",
            "papa|Les chaussettes, le tapis, ou les petits pas ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le jardin souffle encore, trop fort.",
            "maman|Le nœud, le mur, ou le panier-tête ?",
        )
    return L(
        "narrateur|L'escalier reste trop étroit, trop haut.",
        "papa|La même marche, descendre, ou la rampe ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    lead = t1_lead(t1)
    if t2 == 1 and t3 == 1:
        sock = {
            1: "Elle pose le tambour, le temps des chaussettes.",
            2: "Elle noue une chaussette, avec le ruban.",
            3: "Elle sort les chaussettes du panier, toutes chaudes.",
        }[t1]
        return L(
            "enfant-f|Des chaussettes, aux pattes.",
            f"narrateur|{sock}",
            "narrateur|L'ours a deux chaussons de laine, trop grands.",
            "narrateur|La girafe a deux bouts, trop étroits.",
            f"narrateur|{lead['use']}",
            "enfant-f|Vous glissez plus.",
            "papa|Chacun a sa laine, maintenant.",
            "maman|Ils marchent ensemble, quand même.",
        )
    if t2 == 1 and t3 == 2:
        rug = {
            1: "Au bord du tapis, le tambour marque un toc.",
            2: "Tout le long, le ruban sert de bord.",
            3: "Au bout, elle pose le panier, comme une arrivée.",
        }[t1]
        return L(
            "enfant-f|Le tapis, comme une route.",
            "narrateur|Elle tire le tapis du salon, tout rêche.",
            "narrateur|Sur la laine du chemin, le béret tient.",
            "narrateur|Trop mince encore, le cône ne glisse plus.",
            f"narrateur|{rug}",
            "enfant-f|Vous avez une route, tous les deux.",
            "papa|Le savon reste sous le tapis.",
            "maman|Deux silhouettes, une même allée.",
        )
    if t2 == 1 and t3 == 3:
        step = {
            1: "Un toc, puis un pas, puis un autre.",
            2: "Le ruban les relie, un pas chacun.",
            3: "Elle pose le panier, avance, le reprend.",
        }[t1]
        return L(
            "enfant-f|Tout petit, le pas.",
            f"narrateur|{step}",
            "narrateur|Nina tient l'ours d'une main.",
            "narrateur|L'autre main tient la girafe, plus haute.",
            f"narrateur|{lead['use']}",
            "enfant-f|On va au même rythme.",
            "papa|Tes mains ont fait le couloir.",
            "maman|Le carrelage n'a plus gagné.",
        )
    if t2 == 2 and t3 == 1:
        knot = {
            1: "Dans l'herbe, le tambour attend le nœud.",
            2: "Avec le ruban, elle noue le cône, tout doux.",
            3: "Dans l'osier, elle passe le cône, puis le noue.",
        }[t1]
        return L(
            "enfant-f|Un nœud, pour le cône.",
            f"narrateur|{knot}",
            "narrateur|Trop mince, le papier tient, maintenant lié.",
            "narrateur|Trop rond, trop lourd, le béret n'a pas bougé.",
            f"narrateur|{lead['wait']}",
            "enfant-f|Tu as ton chapeau, toi aussi.",
            "papa|Le vent n'a plus le papier.",
            "maman|Deux têtes, deux chapeaux, le même vent.",
        )
    if t2 == 2 and t3 == 2:
        wall = {
            1: "Le tambour donne le pas, le long du mur.",
            2: "Le ruban glisse contre la pierre, tout bas.",
            3: "Le panier racle un peu le crépi, puis avance.",
        }[t1]
        return L(
            "enfant-f|Le mur, sans le vent.",
            "narrateur|Ils longent la maison, l'ombre déjà fraîche.",
            f"narrateur|{wall}",
            "narrateur|Le cône ne s'envole plus, trop près du mur.",
            "narrateur|Le béret frotte la pierre, tout rond.",
            "enfant-f|Vous marchez, tous les deux.",
            "papa|L'abri était là, contre la maison.",
            "maman|Le jardin reste à côté, plus calme.",
        )
    if t2 == 2 and t3 == 3:
        hat = {
            1: "Le tambour pose sur le bord, un toc dans l'osier.",
            2: "Le ruban attache les deux bords, comme un toit.",
            3: "Elle rentre les chapeaux, les têtes restent dehors.",
        }[t1]
        return L(
            "enfant-f|Les chapeaux dans le panier.",
            f"narrateur|{hat}",
            "narrateur|L'ours a le béret sur le ventre, trop rond.",
            "narrateur|La girafe a le cône collé, trop mince.",
            "enfant-f|Vos têtes regardent, quand même.",
            "papa|Le vent prend l'osier, pas le papier.",
            "maman|Ils défilent, tête contre tête.",
            f"narrateur|{lead['use']}",
        )
    if t2 == 3 and t3 == 1:
        same = {
            1: "Un toc sur la marche, le défilé sur place.",
            2: "Le ruban fait un cercle, autour d'eux.",
            3: "Le panier s'assoit sur la marche, trop juste.",
        }[t1]
        return L(
            "enfant-f|La même marche, pour tous.",
            f"narrateur|{same}",
            "narrateur|L'ours s'assoit, trop large, trop rond.",
            "narrateur|La girafe s'assoit, le cône sous le ciel.",
            "enfant-f|On défile ici, sans monter.",
            "papa|La marche a deux places, maintenant.",
            "maman|Plus besoin du plafond.",
            f"narrateur|{lead['wait']}",
        )
    if t2 == 3 and t3 == 2:
        down = {
            1: "D'une marche, le tambour descend, toc plus doux.",
            2: "Vers le bas, le ruban les guide.",
            3: "D'une marche, le panier glisse, puis s'arrête.",
        }[t1]
        return L(
            "enfant-f|On descend, plus simple.",
            f"narrateur|{down}",
            "narrateur|L'ours passe, trop large encore, mais ça tient.",
            "narrateur|Le cône ne tape plus, le plafond s'éloigne.",
            "enfant-f|Vous avez la place, en bas.",
            "papa|Descendre, c'était votre largeur.",
            "maman|Le bois ciré sent encore, plus bas.",
            f"narrateur|{lead['use']}",
        )
    rail = {
        1: "Le tambour voyage sur la rampe, un toc de bois.",
        2: "Le ruban les tient, le long de la rampe.",
        3: "Le panier glisse sur le bois, tout étroit.",
    }[t1]
    return L(
        "enfant-f|La rampe, comme un chemin.",
        f"narrateur|{rail}",
        "narrateur|L'ours glisse, le béret bien enfoncé.",
        "narrateur|La girafe glisse, le cône vers l'avant.",
        "enfant-f|Vous partez côte à côte.",
        "papa|Le bois a fait le pont.",
        "maman|Les marches restent en dessous.",
        f"narrateur|{lead['wait']}",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = t1_lead(t1)["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Les chaussettes de laine sentent encore le tiroir.",
            "enfant-f|Vous avez fini le couloir.",
            "narrateur|De travers, le béret reste tout rond.",
            "narrateur|Un peu froissé, le cône tient, tout mince.",
            "papa|Tes mains ont mis la laine.",
            "maman|Ils sont arrivés ensemble.",
            f"narrateur|{coda}",
            "narrateur|Le carrelage redevient froid, sous les chaussons.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le tapis garde deux traces, l'une ronde.",
            "enfant-f|La route était à nous.",
            "narrateur|Nina souffle sur le cône, tout doux.",
            "enfant-f|Il fait un froissement.",
            "papa|Le savon est resté dessous.",
            "maman|Deux silhouettes, une allée.",
            f"narrateur|{coda}",
            "narrateur|Le salon parle plus bas, maintenant.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Leurs pas ont marqué le savon, tout petits.",
            "enfant-f|On allait au même rythme.",
            "narrateur|Elle pose l'ours, puis la girafe, tout près.",
            "papa|Tes mains ont fait le couloir.",
            "maman|Le carrelage n'a plus gagné.",
            f"narrateur|{coda}",
            "enfant-f|Encore un pas, pour rire.",
            "narrateur|Un dernier glissement, puis plus.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le nœud tient encore, un peu de vent dedans.",
            "enfant-f|Tu as ton chapeau, toi aussi.",
            "narrateur|Elle lisse le béret, trop rond, trop chaud.",
            "papa|Le vent n'a plus le papier.",
            "maman|Deux têtes, le même air.",
            f"narrateur|{coda}",
            "enfant-f|On rentre, maintenant.",
            "narrateur|Une feuille s'arrête contre le pas de la porte.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|L'ombre du mur sent encore la pierre.",
            "enfant-f|Vous avez marché, tous les deux.",
            "narrateur|Le cône a un peu de crépi, tout mince.",
            "papa|L'abri était là.",
            "maman|Le jardin reste à côté.",
            f"narrateur|{coda}",
            "enfant-f|Le vent, je l'entends encore.",
            "narrateur|L'herbe se recouche, tout lentement.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Deux têtes dépassent encore de l'osier.",
            "enfant-f|Tête contre tête.",
            "narrateur|Le béret chauffe le ventre de l'ours.",
            "papa|Le vent a pris l'osier, pas eux.",
            "maman|Ils ont défilé quand même.",
            f"narrateur|{coda}",
            "enfant-f|On les sort, tout doux.",
            "narrateur|Le jardin n'a plus qu'un souffle, tout bas.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|La marche garde deux ronds, l'un plus large.",
            "enfant-f|On a défilé ici, sans monter.",
            "narrateur|Le cône pointe encore le ciel, trop mince.",
            "papa|La marche avait deux places.",
            "maman|Plus besoin du plafond.",
            f"narrateur|{coda}",
            "enfant-f|On reste un peu.",
            "narrateur|Le bois ciré redevient froid, sous eux.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|En bas, le hall sent encore les manteaux.",
            "enfant-f|Vous aviez la place, plus bas.",
            "narrateur|Elle enfonce le béret, un dernier coup.",
            "papa|Descendre, c'était votre largeur.",
            "maman|Le bois sent encore, plus bas.",
            f"narrateur|{coda}",
            "enfant-f|On est arrivés.",
            "narrateur|Une marche craque, puis se tait.",
        )
    return L(
        "narrateur|La rampe garde un fil de laine, tout petit.",
        "enfant-f|Vous êtes partis côte à côte.",
        "narrateur|L'ours et la girafe se touchent, encore.",
        "papa|Le bois a fait le pont.",
        "maman|Les marches sont restées en dessous.",
        f"narrateur|{coda}",
        "enfant-f|Le défilé est fini, pour de vrai.",
        "narrateur|La rampe redevient lisse, sous la main.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le hall sent encore les manteaux mouillés.",
        "narrateur|Une patère jaune tient deux chapeaux, tout près.",
        "narrateur|Le béret de laine a gardé une goutte.",
        "narrateur|Le cône de papier penche, trop léger.",
        "maman|Tu les as vus, Nina ?",
        "enfant-f|Ils ne se ressemblent pas.",
        "papa|Ils peuvent marcher ensemble, quand même.",
        "narrateur|L'ours attend sur la commode, ventre chaud.",
        "narrateur|La girafe dépasse, trop haute, une oreille pliée.",
        "narrateur|En ce moment, Nina touche les deux chapeaux.",
        "enfant-f|Je veux un vrai défilé.",
        "enfant-f|Avec de la musique, et eux deux.",
        "maman|Le tambour, le ruban, et le panier.",
        "papa|Merci, tu as fermé le tiroir.",
        "enfant-f|On prépare, d'abord.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des chaussons.",
        "narrateur|Le tambour, le ruban, et le panier.",
        "maman|Tu prends quoi d'abord, Nina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le tambour", "le ruban", "le panier")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nina a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le couloir", "le jardin", "l'escalier")

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
        "Hall mouillé, patère jaune, deux chapeaux. Nina veut un vrai défilé "
        "pour l'ours au béret rond et la girafe au cône mince. "
        "T1 = tambour / ruban / panier (les trois partent). "
        "T2 = couloir trop lisse / jardin trop venteux / escalier trop étroit. "
        "T3 = neuf résolutions (chaussettes, tapis, petits pas ; nœud, mur, "
        "panier-tête ; même marche, descendre, rampe). "
        "La leçon (pas les mêmes formes, on défile quand même) se vit dans "
        "les glissades, le vent et les marches. Fin : les deux chapeaux restent.",
        "N2 ≤ 15. Léa hors troupe → Nina, papa/maman. Slogan « Plus rond ou "
        "plus mince », « bon travail », calque AUT-001 jetés. Un merci de papa "
        "(tiroir fermé). chunk_id inchangés. check() N2. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
