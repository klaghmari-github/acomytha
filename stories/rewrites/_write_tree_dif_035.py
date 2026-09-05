#!/usr/bin/env python3
"""TREE-DIF-035 — Les deux poupées de Chouchou dans le bain. DIF.COR.002, N1."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-035"
N1 = LIMITS["N1"]
TITLE = "Les deux poupées de Chouchou dans le bain"
FIL = (
    "Après la pluie, Chouchou veut un vrai bain pour ses deux poupées. "
    "La poupée de coton est toute ronde, celle de bois toute mince. "
    "Elle prépare d'abord le savon, le gobelet ou la serviette ; les trois partent. "
    "À l'évier, dans la baignoire ou dans le bac du jardin, chaque lieu a son obstacle. "
    "Les deux poupées se baignent ensemble."
)
CHARS = "Chouchou, papa, maman"
SETTING = "salle de bain après la pluie, puis le bac du jardin"


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"sans fin: {ph}")
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
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "sami",
        "marché",
        "plus rond ou plus mince",
        "le corps n'est pas",
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "bon travail",
        "bravo tu as",
        "la première",
        "la deuxième",
        "la troisième",
        "capitaine",
        "plic",
        "volet jaune",
        "peluche",
        "défilé",
        "cuisine",
        "dînette",
        "dinette",
        "après la sieste",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    check(SID, out["age_band"], out["chunks"])
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
        "lab": "le savon",
        "ans": "savon",
        "acc": "savon | le savon | d'abord le savon | la lavande",
        "retry": "Chouchou a pris le savon, d'abord.",
        "hip": "Le savon glisse encore, entre ses doigts.",
        "wait": "Sur le rebord, le savon attend.",
        "use": "Un peu de savon reste sur le coton.",
        "coda": "Un rond de savon sèche sur le carrelage.",
    },
    2: {
        "lab": "le gobelet",
        "ans": "gobelet",
        "acc": "gobelet | le gobelet | d'abord le gobelet | le plastique",
        "retry": "Chouchou a pris le gobelet, d'abord.",
        "hip": "Le gobelet tape sa hanche, à chaque pas.",
        "wait": "Dans sa main, le gobelet reste.",
        "use": "Le gobelet verse un filet, tout fin.",
        "coda": "Une goutte reste au fond du gobelet.",
    },
    3: {
        "lab": "la serviette",
        "ans": "serviette",
        "acc": "serviette | la serviette | d'abord la serviette | le linge",
        "retry": "Chouchou a pris la serviette, d'abord.",
        "hip": "Un coin de serviette frotte le carrelage.",
        "wait": "Contre elle, la serviette chauffe déjà.",
        "use": "La serviette les enveloppe, tout doux.",
        "coda": "La serviette garde un pli, encore tiède.",
    },
}

T3_LABS = {
    1: ("deux places", "moins d'eau", "la bassine"),
    2: ("le tapis", "le bord", "verser"),
    3: ("le rebord", "la serviette", "l'auvent"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Chouchou prend d'abord le savon, encore froid.",
            "narrateur|Il glisse un peu, entre ses doigts.",
            "enfant-f|Il sent la lavande.",
            "maman|Il est un peu dur, encore.",
            "narrateur|Elle le frotte sur le ventre de coton.",
            "narrateur|Puis elle le glisse sur le bois mince.",
            "enfant-f|Un rond, et une ligne.",
            "papa|Deux formes, un bain.",
            "narrateur|Près du robinet, le gobelet attend.",
            "maman|La serviette aussi.",
            "enfant-f|On les prend.",
            "narrateur|Savon, gobelet et serviette avancent avec elle.",
        )
    if t1 == 2:
        return L(
            "narrateur|Chouchou saisit d'abord le gobelet, tout bleu.",
            "narrateur|Le plastique claque une fois, tout sec.",
            "enfant-f|Il tient l'eau.",
            "papa|C'est pour verser, tout doux.",
            "narrateur|Elle l'essaie près du ventre de coton.",
            "narrateur|Puis il glisse le long du bois mince.",
            "enfant-f|Il tape, et il glisse.",
            "maman|Tu as vu les deux formes.",
            "narrateur|Sur le rebord, le savon attend.",
            "papa|La serviette aussi, pour plus tard.",
            "enfant-f|Je garde le gobelet.",
            "narrateur|Les trois affaires partent avec elle.",
        )
    return L(
        "narrateur|Chouchou déplie d'abord la serviette, encore tiède.",
        "narrateur|Le tissu tombe, trop large, jusqu'au carrelage.",
        "enfant-f|Elle sent le linge.",
        "maman|Elle est un peu rêche, encore.",
        "narrateur|Elle la pose sur le ventre de coton.",
        "narrateur|Le bois dépasse, une jambe dehors.",
        "enfant-f|Une colline, et une ligne.",
        "papa|On les emmène toutes les deux.",
        "narrateur|Près du robinet, le savon attend.",
        "maman|Le gobelet aussi.",
        "enfant-f|Je garde la serviette.",
        "narrateur|Rien ne reste près du rebord.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|Le savon.",
            "papa|Oui.",
            "narrateur|Chouchou glisse le gobelet sous le bras.",
            "maman|La serviette, je te la tends.",
            "enfant-f|Merci.",
            "narrateur|Elle prend le coton, puis le bois.",
            "papa|Les deux viennent.",
            "enfant-f|On cherche l'endroit.",
        )
    if t1 == 2:
        return L(
            "enfant-f|Le gobelet.",
            "maman|Oui.",
            "narrateur|Elle ramasse le savon, tout petit.",
            "papa|La serviette, dans l'autre main ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les deux poupées voyagent contre elle.",
            "maman|Merci d'avoir pris les deux.",
            "enfant-f|On va où, maintenant ?",
        )
    return L(
        "enfant-f|La serviette.",
        "papa|Oui.",
        "narrateur|Maman lui passe le savon, déjà froid.",
        "maman|Le gobelet, dans la poche.",
        "enfant-f|Il est là.",
        "narrateur|Le coton et le bois avancent avec elle.",
        "papa|Merci, Chouchou.",
        "enfant-f|Il me faut de l'eau.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['hip']}",
        "narrateur|Les deux poupées attendent de l'eau.",
        "papa|L'évier, la baignoire, ou le bac ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    hip = OBJ[t1]["hip"]
    if t2 == 1:
        extra = {
            1: "Le savon glisse déjà sur le chrome.",
            2: "Le gobelet cogne le métal, un toc.",
            3: "La serviette accroche le robinet, puis lâche.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Ils s'approchent de l'évier, trop étroit.",
            f"narrateur|{extra}",
            "narrateur|L'eau fait un rond, tout petit.",
            "enfant-f|Vous entrez.",
            "narrateur|Le coton bute contre le rebord, trop rond.",
            "narrateur|Le bois glisse vers le trou, trop mince.",
            "enfant-f|L'une reste, l'autre part.",
            "maman|Elles n'ont pas la même forme.",
            "papa|Tu fais quoi, avec les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "Un peu de savon perle déjà sur l'eau.",
            2: "Le gobelet flotte un instant, trop léger.",
            3: "La serviette tombe, trop large, trop lourde.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Dans la baignoire, l'eau est déjà haute.",
            f"narrateur|{extra}",
            "enfant-f|C'est une mer, ici.",
            "narrateur|Chouchou pousse le coton vers l'eau.",
            "narrateur|Le ventre rond flotte, trop loin.",
            "narrateur|Le bois, lui, glisse au fond.",
            "enfant-f|Ce n'est pas juste.",
            "papa|L'eau est profonde, voilà tout.",
            "maman|Tu les gardes comment, ensemble ?",
        )
    extra = {
        1: "Dehors, le savon sent encore la lavande.",
        2: "Une goutte tombe du gobelet, trop penché.",
        3: "La serviette se gonfle, comme un nuage.",
    }[t1]
    return L(
        f"narrateur|{hip}",
        "narrateur|Dehors, le bac du jardin sent la terre.",
        f"narrateur|{extra}",
        "enfant-f|Le bain, ici.",
        "narrateur|Un vent passe, tout froid.",
        "narrateur|Le bois tombe, trop léger.",
        "narrateur|Le coton reste, tout lourd, tout rond.",
        "enfant-f|Elle est tombée !",
        "maman|Le vent a choisi, pas toi.",
        "papa|Tu les rassembles comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Dans l'évier, le coton bute, le bois glisse.",
            "papa|Tu fais quoi, Chouchou ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Dans la baignoire, l'eau est trop haute.",
            "maman|Tu fais quoi, avec elles ?",
        )
    return L(
        "narrateur|Dans le bac, le bois est tombé.",
        "papa|Tu fais quoi, maintenant ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wall = {
            1: "Elle pose le savon au milieu, comme un mur.",
            2: "Elle pose le gobelet au milieu, comme un mur.",
            3: "Elle pose la serviette au milieu, comme un pli.",
        }[t1]
        return L(
            "enfant-f|Deux places, dans l'évier.",
            f"narrateur|{wall}",
            "narrateur|Le coton s'assoit d'un côté, trop rond.",
            "narrateur|Le bois s'assoit de l'autre, trop mince.",
            "enfant-f|Vous avez chacun votre eau.",
            "papa|Deux places, deux formes.",
            f"narrateur|{o['use']}",
            "maman|Elles se baignent, quand même.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-f|Moins d'eau.",
            "narrateur|Elle ferme un peu le robinet.",
            "narrateur|Le rond devient une flaque, toute basse.",
            "narrateur|Le coton pose le ventre, sans coincer.",
            "narrateur|Le bois reste, sans glisser.",
            "enfant-f|Vous tenez, toutes les deux.",
            "maman|Elles n'ont pas besoin d'être pareilles.",
            f"narrateur|{o['use']}",
            "papa|L'évier les tient, maintenant.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-f|La bassine, dedans.",
            "narrateur|Maman glisse une bassine dans l'évier.",
            "narrateur|Le coton et le bois montent ensemble.",
            "enfant-f|Un bain, plus large.",
            "papa|Le trou reste en dessous, tout seul.",
            "maman|Elles se touchent, les deux.",
            f"narrateur|{o['use']}",
            "narrateur|Un filet tombe encore, puis s'arrête.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-f|Le tapis, comme une île.",
            "narrateur|Elle pose le tapis de bain, encore rêche.",
            "narrateur|Le coton s'assoit dessus, trop rond.",
            "narrateur|Le bois s'allonge contre lui, trop mince.",
            "enfant-f|Vous avez le fond, toutes les deux.",
            "papa|Chacun a sa place.",
            f"narrateur|{o['use']}",
            "maman|L'eau passe autour, plus calme.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-f|Le bord, pas le fond.",
            "narrateur|Elle les pose au bout, où l'eau est basse.",
            "narrateur|Le coton reste, le bois aussi.",
            "enfant-f|Vous tenez, sans couler.",
            "papa|Le bord était assez large.",
            "maman|Et lui, tout mince, reste près.",
            f"narrateur|{o['use']}",
            "narrateur|Une vague tout petite, puis plus.",
        )
    if t2 == 2 and t3 == 3:
        pour = {
            1: "Elle arrose le coton, puis le bois.",
            2: "Le gobelet arrose le coton, puis le bois.",
            3: "Sous la serviette, elle arrose les deux.",
        }[t1]
        return L(
            "enfant-f|Verser, juste un peu.",
            f"narrateur|{pour}",
            "enfant-f|Vous avez de l'eau, toutes les deux.",
            "papa|Pas besoin du grand bain.",
            "maman|Tes mains ont fait la pluie.",
            f"narrateur|{o['wait']}",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-f|Le rebord, pour tous.",
            "narrateur|Elle les assied sur le bord du bac.",
            "narrateur|Le coton tient, trop large, trop rond.",
            "narrateur|Le bois tient, une jambe dans le vide.",
            "enfant-f|Vous vous baignez ici, sans tomber.",
            "papa|Le bord a deux places, maintenant.",
            "maman|Plus besoin du vent.",
            f"narrateur|{o['wait']}",
        )
    if t2 == 3 and t3 == 2:
        wrap = {
            1: "Elle les enveloppe, savon contre le linge.",
            2: "Elle les enveloppe, gobelet contre le linge.",
            3: "Elle les enveloppe, coton contre bois.",
        }[t1]
        return L(
            "enfant-f|La serviette, contre le vent.",
            f"narrateur|{wrap}",
            "narrateur|Le tissu tient, même si ça souffle.",
            "enfant-f|Vous avez chaud, toutes les deux.",
            "papa|Le vent prend le linge, pas elles.",
            "maman|Tête contre tête.",
            f"narrateur|{o['use']}",
        )
    cover = {
        1: "Elle porte les deux, le savon contre elle.",
        2: "Elle porte les deux, le gobelet contre elle.",
        3: "Elle porte les deux, la serviette autour.",
    }[t1]
    return L(
        "enfant-f|Sous l'auvent, plus calme.",
        f"narrateur|{cover}",
        "narrateur|Le vent reste dehors, dans le bac.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Rentrer un peu, c'était plus doux.",
        "maman|La terre sent encore, plus loin.",
        f"narrateur|{o['wait']}",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Deux ronds d'eau restent dans l'évier.",
            "enfant-f|Vous avez eu votre bain.",
            "narrateur|Le coton brille, encore tout rond.",
            "narrateur|Le bois brille, une jambe encore mince.",
            "papa|Tes mains ont fait les deux places.",
            "maman|Elles sont ensemble, quand même.",
            f"narrateur|{coda}",
            "narrateur|Le chrome redevient froid, tout calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|La flaque basse sent encore la lavande.",
            "enfant-f|Vous teniez, toutes les deux.",
            "narrateur|Chouchou souffle sur le bois, tout doux.",
            "papa|L'évier les a tenues.",
            "maman|Bravo, elles sont propres.",
            f"narrateur|{coda}",
            "enfant-f|On rentre, maintenant.",
            "narrateur|L'évier n'a plus qu'un filet, tout bas.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Dans la bassine, l'eau tremble encore.",
            "enfant-f|Un bain, plus large.",
            "narrateur|Elle pose le coton, puis le bois, tout près.",
            "papa|Le trou n'a plus gagné.",
            "maman|Tes mains ont mis la bassine.",
            f"narrateur|{coda}",
            "enfant-f|Encore une goutte, pour rire.",
            "narrateur|Une goutte s'arrête sur le chrome, puis plus.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le tapis de bain garde deux traces, l'une ronde.",
            "enfant-f|Vous aviez votre île.",
            "narrateur|Elle lisse le ventre de coton, trop chaud.",
            "papa|Chacun avait sa place.",
            "maman|L'eau passait autour, plus calme.",
            f"narrateur|{coda}",
            "enfant-f|On les essuie, tout doux.",
            "narrateur|La baignoire se tait, l'eau trop calme.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Au bout, le bord reste un peu mouillé.",
            "enfant-f|Vous teniez, sans couler.",
            "narrateur|Le bois a une goutte sur la jambe, trop mince.",
            "papa|Le bord était assez large.",
            "maman|Deux silhouettes, une même eau.",
            f"narrateur|{coda}",
            "enfant-f|Le dîner, après ?",
            "narrateur|Un rai de lumière reste sur l'eau.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Un filet d'eau a marqué le coton, tout petit.",
            "enfant-f|Vous avez eu la pluie.",
            "narrateur|Elle pose les deux, l'une contre l'autre.",
            "papa|Pas besoin du grand bain.",
            "maman|Tes mains ont versé, tout doux.",
            f"narrateur|{coda}",
            "enfant-f|On est arrivés.",
            "narrateur|Le tapis de bain redevient plat, tout rêche.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Sur le bac, deux ronds restent, trop différents.",
            "enfant-f|On s'est baignées ici, sans tomber.",
            "narrateur|Le bois pointe encore le ciel, trop mince.",
            "papa|Le bord avait deux places.",
            "maman|Plus besoin du vent.",
            f"narrateur|{coda}",
            "enfant-f|On reste un peu.",
            "narrateur|L'herbe se recouche, tout lentement.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sous le linge, ça sent encore la terre.",
            "enfant-f|Vous aviez chaud, toutes les deux.",
            "narrateur|Elle lisse le coton, un dernier coup.",
            "papa|Le vent a pris le linge, pas elles.",
            "maman|Tête contre tête.",
            f"narrateur|{coda}",
            "enfant-f|On rentre, maintenant.",
            "narrateur|Une feuille s'arrête contre le pas.",
        )
    return L(
        "narrateur|Sous l'auvent, l'air est déjà plus doux.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|Le coton et le bois se touchent, encore.",
        "papa|Rentrer un peu, c'était plus doux.",
        "maman|La terre sent encore, plus loin.",
        f"narrateur|{coda}",
        "enfant-f|Le bain est fini, pour de vrai.",
        "narrateur|L'auvent goutte encore, puis se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Après la pluie, la maison sent le savon.",
        "narrateur|Dans la salle de bain, le carrelage brille.",
        "narrateur|Une goutte tombe encore du robinet.",
        "narrateur|Deux poupées attendent sur le rebord tiède.",
        "narrateur|La poupée de coton a le ventre tout rond.",
        "narrateur|La poupée de bois a les jambes toutes minces.",
        "maman|Tu les as sorties du panier ?",
        "enfant-f|Oui.",
        "enfant-f|Je veux leur donner un bain.",
        "papa|Les deux, Chouchou ?",
        "enfant-f|Les deux.",
        "narrateur|En ce moment, Chouchou touche le savon.",
        "narrateur|Il sent la lavande, encore un peu froid.",
        "enfant-f|Elles ne se ressemblent pas.",
        "papa|On les emmène toutes les deux.",
        "maman|Le savon, le gobelet, et la serviette.",
        "papa|Merci, tu as ouvert le robinet.",
        "enfant-f|On prépare, d'abord.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du rebord.",
        "narrateur|Le savon, le gobelet, et la serviette.",
        "maman|Tu commences par laquelle ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le savon", "le gobelet", "la serviette")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Chouchou a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'évier", "la baignoire", "le bac")

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
        "Après la pluie, salle de bain, carrelage brillant, lavande. "
        "Chouchou veut un vrai bain pour la poupée de coton, toute ronde, "
        "et la poupée de bois, toute mince. "
        "T1 = savon / gobelet / serviette (les trois partent). "
        "T2 = évier trop étroit / baignoire trop haute / bac du jardin trop venteux. "
        "T3 = neuf résolutions (deux places, moins d'eau, bassine ; "
        "tapis, bord, verser ; rebord, serviette, auvent). "
        "La leçon se vit : les formes ne sont pas une blague, on joue avec les deux. "
        "Fin : les deux poupées se baignent ensemble.",
        "N1 ≤ 10. Sami hors troupe → Chouchou, papa/maman. Slogan marché "
        "« Plus rond ou plus mince », « bon travail », calque AUT-001 jetés. "
        "Un merci de papa (robinet ouvert). chunk_id inchangés. check() N1. "
        "Audio non cuit.",
    )


if __name__ == "__main__":
    main()
