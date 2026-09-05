#!/usr/bin/env python3
"""TREE-DIF-059 — Les deux plantes de Nina, à la fenêtre. DIF.COR.002, N1."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-059"
N1 = LIMITS["N1"]
TITLE = "Les deux plantes de Nina, à la fenêtre"
FIL = (
    "Derrière la vitre nuageuse, Nina veut que son cactus tout rond "
    "et sa tige toute mince boivent la lumière ensemble. "
    "Elle prend d'abord l'arrosoir, la cuillère ou le linge ; les trois partent. "
    "Au rebord trop étroit, sur la chaise trop haute, près du radiateur trop chaud. "
    "Neuf façons de les garder ensemble. Les deux plantes boivent."
)
CHARS = "Nina, papa, maman"
SETTING = "près de la fenêtre : rebord, chaise, radiateur"


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
        "zoé",
        "zoe",
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
        "poupée",
        "canard",
        "hérisson",
        "dînette",
        "dinette",
        "après la sieste",
        "bac à sable",
        "toboggan",
        "balançoire",
        "nichoir",
        "merle",
        "chambre",
        "marché",
        "cuisine",
        "jardin",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
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
        "lab": "l'arrosoir",
        "ans": "arrosoir",
        "acc": "arrosoir | l'arrosoir | d'abord l'arrosoir | le métal",
        "retry": "Nina a pris l'arrosoir, d'abord.",
        "hip": "L'arrosoir tape sa jambe, à chaque pas.",
        "wait": "Dans sa main, l'arrosoir attend.",
        "use": "Un peu d'eau tremble au bec.",
        "coda": "Une goutte sèche au fond de l'arrosoir.",
    },
    2: {
        "lab": "la cuillère",
        "ans": "cuillère",
        "acc": "cuillère | la cuillère | d'abord la cuillère | le métal",
        "retry": "Nina a pris la cuillère, d'abord.",
        "hip": "La cuillère cliquette, tout doux.",
        "wait": "Contre elle, la cuillère chauffe déjà.",
        "use": "Une goutte reste dans la cuillère.",
        "coda": "La cuillère brille encore, déjà sèche.",
    },
    3: {
        "lab": "le linge",
        "ans": "linge",
        "acc": "linge | le linge | d'abord le linge | le tissu",
        "retry": "Nina a pris le linge, d'abord.",
        "hip": "Un coin de linge frotte le carreau.",
        "wait": "Contre elle, le linge chauffe déjà.",
        "use": "Le linge garde une trace d'eau.",
        "coda": "Un pli de linge reste, encore tiède.",
    },
}

T3_LABS = {
    1: ("la planche", "deux places", "la caisse"),
    2: ("le sol", "le banc", "les mains"),
    3: ("le coin", "le linge", "plus tard"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina prend d'abord l'arrosoir, encore froid.",
            "narrateur|Le métal pique un peu, entre ses doigts.",
            "enfant-f|Il est lourd.",
            "maman|Tiens-le tout doux, pour elles.",
            "narrateur|Elle verse un peu d'eau, tout doux.",
            "narrateur|Puis elle glisse la cuillère sous le bras.",
            "enfant-f|Un cactus rond, une tige mince.",
            "papa|Deux plantes, une lumière.",
            "narrateur|Près du tabouret, le linge attend.",
            "maman|Le linge aussi, avec toi.",
            "enfant-f|On les prend.",
            "narrateur|Arrosoir, cuillère et linge avancent avec elle.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina prend d'abord la cuillère, encore froide.",
            "narrateur|Le métal cliquette une fois, tout sec.",
            "enfant-f|Elle est petite.",
            "papa|C'est pour la tige, goutte à goutte.",
            "narrateur|Elle la pose un instant sur le tabouret.",
            "narrateur|L'arrosoir attend, déjà un peu plein.",
            "enfant-f|Un rond, et une ligne.",
            "maman|Tu as vu les deux formes.",
            "narrateur|Sous son bras, le linge pend.",
            "papa|L'arrosoir aussi, pour plus tard.",
            "enfant-f|Je garde la cuillère.",
            "narrateur|Les trois affaires partent avec elle.",
        )
    return L(
        "narrateur|Nina saisit d'abord le linge, encore tiède.",
        "narrateur|Le tissu sent le savon, un peu.",
        "enfant-f|Il est doux.",
        "maman|Essuie le carreau, tout doux.",
        "narrateur|Elle frotte un nuage, puis un autre.",
        "narrateur|La lumière passe, plus claire.",
        "enfant-f|Elles vont voir, toutes les deux.",
        "papa|Oui, les deux.",
        "narrateur|Près du tabouret, l'arrosoir attend.",
        "maman|La cuillère aussi.",
        "enfant-f|Je garde le linge.",
        "narrateur|Rien ne reste près du tabouret.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|L'arrosoir.",
            "papa|Oui.",
            "narrateur|Nina glisse la cuillère sous le bras.",
            "maman|Le linge, je te le tends.",
            "enfant-f|Merci.",
            "narrateur|Les deux plantes attendent déjà.",
            "papa|Les deux vont boire.",
            "enfant-f|On cherche l'endroit.",
        )
    if t1 == 2:
        return L(
            "enfant-f|La cuillère.",
            "maman|Oui.",
            "narrateur|Elle ramasse l'arrosoir, tout petit.",
            "papa|Le linge, dans l'autre main ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les deux plantes tournent déjà.",
            "maman|Merci d'avoir pris les deux.",
            "enfant-f|On va où, maintenant ?",
        )
    return L(
        "enfant-f|Le linge.",
        "papa|Oui.",
        "narrateur|Maman lui passe l'arrosoir, déjà froid.",
        "maman|La cuillère, sous le bras.",
        "enfant-f|Elle est là.",
        "narrateur|Les deux plantes attendent la lumière.",
        "papa|Merci, Nina.",
        "enfant-f|On va à la vitre ?",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['hip']}",
        "narrateur|Les deux plantes veulent boire.",
        "papa|Le rebord, la chaise, ou le radiateur ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    hip = OBJ[t1]["hip"]
    if t2 == 1:
        extra = {
            1: "Un filet d'eau tombe, trop loin.",
            2: "La cuillère accroche le bois, puis lâche.",
            3: "Le linge accroche un clou, trop mince.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Elles s'approchent du rebord, trop étroit.",
            "enfant-f|La lumière est là.",
            f"narrateur|{extra}",
            "narrateur|Le bois fait une ligne, trop fine.",
            "enfant-f|Vous venez.",
            "narrateur|Le cactus large bute contre le bois.",
            "narrateur|La tige légère glisse vers le sol.",
            "enfant-f|L'une reste, l'autre part.",
            "maman|Elles n'ont pas la même forme.",
            "papa|Tu fais quoi, avec les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "L'eau rate le pot, trop haut.",
            2: "La cuillère tremble, trop haute.",
            3: "Le linge glisse du dossier, trop mince.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Sur la chaise, le bois penche un peu.",
            "enfant-f|La lumière, ici.",
            f"narrateur|{extra}",
            "narrateur|Nina pose un pied, trop haut pour elles.",
            "papa|Tu es trop haute, pour elles.",
            "narrateur|Le cactus pèse, et la chaise penche.",
            "narrateur|La tige légère penche, elle aussi.",
            "enfant-f|Elle va tomber.",
            "papa|La chaise penche, voilà tout.",
            "maman|Tu les gardes comment, ensemble ?",
        )
    extra = {
        1: "L'eau tiédit déjà, trop près du fer.",
        2: "La cuillère chauffe, trop vite.",
        3: "Le linge sèche trop vite, trop chaud.",
    }[t1]
    return L(
        f"narrateur|{hip}",
        "narrateur|Près du radiateur, le fer est trop chaud.",
        "enfant-f|La lumière, là-bas.",
        f"narrateur|{extra}",
        "narrateur|Un air passe, tout sec.",
        "maman|Trop chaud, trop près.",
        "narrateur|Le cactus tient, le fer est chaud.",
        "narrateur|La tige baisse une feuille, trop près.",
        "enfant-f|Elle n'aime pas.",
        "maman|Le fer est trop chaud pour elle.",
        "papa|Tu les rassembles comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Sur le rebord, l'une reste, l'autre glisse.",
            "papa|Tu fais quoi, Nina ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Sur la chaise, l'eau rate encore.",
            "maman|Tu fais quoi, avec elles ?",
        )
    return L(
        "narrateur|Près du fer, la tige baisse une feuille.",
        "papa|Tu fais quoi, maintenant ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wall = {
            1: "Elle pose l'arrosoir sur la planche, tout bas.",
            2: "Elle pose la cuillère sur la planche, tout bas.",
            3: "Elle pose le linge sur la planche, tout bas.",
        }[t1]
        return L(
            "enfant-f|La planche, plus large.",
            f"narrateur|{wall}",
            "narrateur|Le cactus large trouve sa place.",
            "narrateur|La tige légère revient, tout doux.",
            "enfant-f|Vous avez chacune votre place.",
            "papa|Deux places, deux formes.",
            f"narrateur|{o['use']}",
            "maman|Elles boivent, quand même.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-f|Deux places, pour elles.",
            "narrateur|Elle écarte les deux pots, tout doux.",
            "narrateur|Un pot près du rond, trop large.",
            "narrateur|Un pot près du mince, trop fin.",
            "enfant-f|Vous tenez, toutes les deux.",
            "maman|Elles n'ont pas besoin d'être pareilles.",
            f"narrateur|{o['use']}",
            "papa|Le rebord les tient, maintenant.",
        )
    if t2 == 1 and t3 == 3:
        cover = {
            1: "Elle pose l'arrosoir dans la caisse, tout bas.",
            2: "Elle pose la cuillère dans la caisse, tout bas.",
            3: "Elle pose le linge dans la caisse, tout bas.",
        }[t1]
        return L(
            "enfant-f|La caisse, pour toutes.",
            f"narrateur|{cover}",
            "narrateur|Le cactus large tient dans la caisse.",
            "narrateur|La tige légère tient, tout près.",
            "enfant-f|Une lumière, plus large.",
            "papa|Le vide reste en dessous, tout seul.",
            "maman|Elles se touchent, les deux.",
            f"narrateur|{o['use']}",
        )
    if t2 == 2 and t3 == 1:
        down = {
            1: "Elle pose l'arrosoir au sol, tout bas.",
            2: "Elle pose la cuillère au sol, tout bas.",
            3: "Elle pose le linge au sol, tout bas.",
        }[t1]
        return L(
            "enfant-f|Le sol, comme une table.",
            f"narrateur|{down}",
            "narrateur|Nina s'assoit, les pieds au parquet.",
            "papa|Tout doux, au sol.",
            "narrateur|Le cactus large tient au parquet.",
            "narrateur|La tige légère s'allonge contre lui.",
            "enfant-f|Vous avez le sol, toutes les deux.",
            "papa|Chacune a sa place.",
            f"narrateur|{o['use']}",
            "maman|L'eau reste, plus calme.",
        )
    if t2 == 2 and t3 == 2:
        foot = {
            1: "Elle pose l'arrosoir sur le banc, tout bas.",
            2: "Elle glisse la cuillère sur le banc, tout bas.",
            3: "Elle pose le linge sur le banc, tout bas.",
        }[t1]
        return L(
            "enfant-f|Le banc, plus bas.",
            f"narrateur|{foot}",
            "narrateur|Le cactus large reste sur le banc.",
            "narrateur|La tige légère reste, tout près.",
            "enfant-f|Vous tenez, sans tomber.",
            "papa|Le banc était assez large.",
            "maman|Et la tige reste près, tout doux.",
            f"narrateur|{o['use']}",
        )
    if t2 == 2 and t3 == 3:
        spread = {
            1: "Elle tient la tige, l'arrosoir tout près.",
            2: "Elle tient la tige, la cuillère tout près.",
            3: "Elle tient la tige, le linge tout près.",
        }[t1]
        return L(
            "enfant-f|Les mains, pour la mince.",
            f"narrateur|{spread}",
            "narrateur|Une goutte tombe, tout petite.",
            "enfant-f|Vous avez l'eau, toutes les deux.",
            "papa|Plus besoin de monter.",
            "maman|Tes mains ont tenu la tige.",
            f"narrateur|{o['wait']}",
            "enfant-f|Le cactus aussi, je le vois.",
        )
    if t2 == 3 and t3 == 1:
        step = {
            1: "Elle pose l'arrosoir au coin, tout bas.",
            2: "Elle pose la cuillère au coin, tout bas.",
            3: "Elle pose le linge au coin, tout bas.",
        }[t1]
        return L(
            "enfant-f|Le coin, plus frais.",
            f"narrateur|{step}",
            "narrateur|Le cactus large tient au coin, tout calme.",
            "narrateur|La tige légère tient, une feuille plus haute.",
            "enfant-f|Vous buvez ici, tout doux.",
            "papa|Le coin a deux places, maintenant.",
            "maman|Plus besoin du fer.",
            f"narrateur|{o['wait']}",
        )
    if t2 == 3 and t3 == 2:
        near = {
            1: "Elle pose le linge, l'arrosoir tout près.",
            2: "Elle pose le linge, la cuillère tout près.",
            3: "Elle pose le linge, comme une ombre.",
        }[t1]
        return L(
            "enfant-f|Le linge, pour l'ombre.",
            f"narrateur|{near}",
            "narrateur|Les deux plantes avancent, tout lent.",
            "enfant-f|Vous avez l'eau, plus douce.",
            "papa|L'ombre était plus douce.",
            "maman|L'une près de l'autre.",
            f"narrateur|{o['use']}",
        )
    shade = {
        1: "Elle pose l'arrosoir plus loin, tout bas.",
        2: "Elle pose la cuillère plus loin, tout bas.",
        3: "Elle pose le linge plus loin, tout bas.",
    }[t1]
    return L(
        "enfant-f|Plus tard, plus calme.",
        f"narrateur|{shade}",
        "narrateur|Le fer reste derrière, déjà moins chaud.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Le fer a moins chaud, maintenant.",
        "maman|La vitre sent encore, plus loin.",
        f"narrateur|{o['wait']}",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Deux ronds d'eau restent sur la planche.",
            "enfant-f|Vous avez eu votre lumière.",
            "narrateur|Le cactus large brille, encore tout rond.",
            "narrateur|La tige brille, encore toute mince.",
            "papa|Tes mains ont fait les deux places.",
            "maman|Elles sont ensemble, quand même.",
            f"narrateur|{coda}",
            "narrateur|La vitre redevient claire, tout calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Les deux pots sentent encore la terre.",
            "enfant-f|Vous teniez, toutes les deux.",
            "narrateur|Nina souffle sur une feuille, tout doux.",
            "papa|Le rebord les a tenues.",
            "maman|Bravo, elles ont bu.",
            f"narrateur|{coda}",
            "enfant-f|On reste un peu.",
            "narrateur|Le bois n'a plus qu'une trace, tout bas.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Dans la caisse, la terre tremble encore.",
            "enfant-f|Une lumière, plus large.",
            "narrateur|Elle pose une goutte, puis une autre.",
            "papa|Le vide n'a plus gagné.",
            "maman|Tes mains ont mis la caisse.",
            f"narrateur|{coda}",
            "enfant-f|Encore une goutte, pour rire.",
            "narrateur|Une poussière s'arrête sur le bois, puis plus.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Au sol, deux traces restent, trop différentes.",
            "enfant-f|On a bu ici, sans tomber.",
            "narrateur|La mince pointe encore le ciel, tout doux.",
            "papa|Le sol avait deux places.",
            "maman|Plus besoin de la chaise.",
            f"narrateur|{coda}",
            "enfant-f|On reste un peu.",
            "narrateur|Le parquet se tait, tout lentement.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Sur le banc, ça sent encore le bois.",
            "enfant-f|Vous teniez, sans tomber.",
            "narrateur|La mince a une goutte sur la feuille.",
            "papa|Le banc était assez large.",
            "maman|Deux formes, une même lumière.",
            f"narrateur|{coda}",
            "enfant-f|La soupe, après ?",
            "narrateur|Un peu de soleil reste sur le bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Dans ses mains, une feuille reste, tout petite.",
            "enfant-f|Vous avez eu l'eau.",
            "narrateur|Elle les regarde, l'une contre l'autre.",
            "papa|Plus besoin de monter.",
            "maman|Tes mains ont tenu la tige.",
            f"narrateur|{coda}",
            "enfant-f|On est là.",
            "narrateur|La chaise redevient vide, tout calme.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Au coin, deux gouttes restent encore.",
            "enfant-f|Vous aviez le coin.",
            "narrateur|Nina lisse une feuille, un dernier coup.",
            "papa|Le coin avait deux places.",
            "maman|Plus besoin du fer.",
            f"narrateur|{coda}",
            "enfant-f|On reste un peu.",
            "narrateur|Le fer se tait, tout lentement.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sous le linge, l'air est déjà doux.",
            "enfant-f|Vous aviez l'eau, plus douce.",
            "narrateur|Le rond et le mince se touchent, encore.",
            "papa|L'ombre était plus douce.",
            "maman|La vitre sent encore, plus loin.",
            f"narrateur|{coda}",
            "enfant-f|Elles ont bu, pour de vrai.",
            "narrateur|Un pli de tissu s'arrête contre le pot.",
        )
    return L(
        "narrateur|Plus tard, l'air est déjà plus doux.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|Un cactus rond, une tige mince, tout près.",
        "papa|Le fer a moins chaud, maintenant.",
        "maman|La vitre sent encore, plus loin.",
        f"narrateur|{coda}",
        "enfant-f|On reste, maintenant.",
        "narrateur|Le fer du radiateur retombe, tout doux.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"": ""}
    sons.pop("", None)

    s["CHK_T0000_P0000"] = L(
        "narrateur|Sur le carreau, un nuage tout bas.",
        "narrateur|Une goutte glisse, puis s'arrête.",
        "papa|Tu vois le toit, Nina ?",
        "enfant-f|Il est encore mouillé.",
        "narrateur|La soupe sent déjà, tout près.",
        "maman|Le bol est chaud, encore.",
        "narrateur|Papa plie une serviette, près de l'évier.",
        "narrateur|Deux plantes attendent sur le tabouret.",
        "papa|Le cactus a le ventre tout rond.",
        "maman|La tige verte est toute mince.",
        "enfant-f|Je veux qu'elles boivent, toutes les deux.",
        "papa|Les deux, Nina ?",
        "enfant-f|Les deux.",
        "narrateur|En ce moment, Nina touche l'arrosoir.",
        "narrateur|Le métal est un peu froid, encore.",
        "enfant-f|Elles ne se ressemblent pas.",
        "papa|On les emmène toutes les deux.",
        "maman|L'arrosoir, la cuillère, et le linge.",
        "papa|Merci, tu as sorti les deux.",
        "enfant-f|On prépare, d'abord.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du tabouret.",
        "narrateur|L'arrosoir, la cuillère, et le linge.",
        "maman|Tu commences par laquelle ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("l'arrosoir", "la cuillère", "le linge")

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
        extras[f"{p}_T0002_P0000"] = t3lab("le rebord", "la chaise", "le radiateur")

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
        "Vitre nuageuse, goutte, toit mouillé, soupe, tabouret. Nina veut que "
        "le cactus tout rond et la tige toute mince boivent la lumière ensemble. "
        "T1 = arrosoir / cuillère / linge (les trois partent). "
        "T2 = rebord trop étroit / chaise trop haute / radiateur trop chaud. "
        "T3 = neuf résolutions (planche, deux places, caisse ; sol, banc, mains ; "
        "coin, linge, plus tard). La leçon se vit : les formes ne sont pas "
        "une blague, on arrose les deux. Fin : les deux plantes boivent.",
        "N1 ≤ 10. Zoé hors troupe → Nina, papa/maman. Slogan « Plus rond ou "
        "plus mince », « bon travail », calque AUT-001 jetés. Autre récit que "
        "DIF-015/025/035/043/051 (tente, défilé, bain, canards, train). "
        "Fenêtre tenue. Un merci de papa (les deux sorties). "
        "chunk_id inchangés. check() OK. "
        "xlsx live : `stories/arbres/TREE-DIF-059.xlsx`. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
