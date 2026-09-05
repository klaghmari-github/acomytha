#!/usr/bin/env python3
"""TREE-DIF-031 — Le panier rouge de Raphaël dans le potager (N2, DIF.BES.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-031"
N2 = LIMITS["N2"]
TITLE = "Le panier rouge de Raphaël dans le potager"
FIL = (
    "Raphaël veut cueillir les dernières tomates avec Nina, puis manger "
    "la salade sur la marche. Il prend d'abord le panier, le chapeau ou "
    "le tabouret ; les trois partent. Au robinet Nina lave un caillou, "
    "sous le figuier elle a trop chaud, au bac elle finit un gâteau de sable. "
    "Il propose, et il accepte oui, plus tard, ou une autre idée."
)


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
    out["characters"] = "Raphaël, Nina, papa, maman"
    out["setting"] = "potager, robinet, figuier, bac à sable"
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
        "inviter sans forcer",
        "accepter plusieurs",
        "hugo",
        "coussin",
        "le fort",
        "capitaine",
        "plic",
        "volet jaune",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
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
        "lab": "le panier rouge",
        "cap": "Le panier rouge",
        "t1q": "au bras",
        "t1acc": "bras | au bras | le bras | mon bras | à son bras",
        "t1retry": "Le panier pend au bras.",
        "coda": "Le panier rouge garde une feuille, encore chaude.",
    },
    2: {
        "lab": "le chapeau de paille",
        "cap": "Le chapeau de paille",
        "t1q": "sur sa tête",
        "t1acc": "tête | sa tête | sur sa tête | le chapeau | chapeau",
        "t1retry": "Le chapeau est sur sa tête.",
        "coda": "Le chapeau de paille sèche sur la marche.",
    },
    3: {
        "lab": "le petit tabouret",
        "cap": "Le petit tabouret",
        "t1q": "près des pieds",
        "t1acc": "pieds | les pieds | près des pieds | au sol | tabouret",
        "t1retry": "Le tabouret est près des pieds.",
        "coda": "Le petit tabouret reste près du pain.",
    },
}

T3_LABS = {
    1: ("attendre un peu", "prendre le caillou", "laver une tomate"),
    2: ("apporter de l'eau", "l'ombre des plants", "garder une tomate"),
    3: ("attendre le gâteau", "déplacer le gâteau", "proposer plus tard"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Raphaël prend d'abord le panier rouge.",
            "enfant-m|Il sent encore la terre.",
            "maman|Passe-le à ton bras, tout doux.",
            "narrateur|L'osier gratte un peu le coude.",
            "papa|Le chapeau aussi, près de toi.",
            "narrateur|Maman glisse le tabouret, tout près.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Nina va tout voir.",
            "papa|Tu l'invites, quand tu la trouves ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Raphaël prend d'abord le chapeau de paille.",
            "enfant-m|Il gratte un peu, aux tempes.",
            "papa|Mets-le, le soleil tape encore.",
            "narrateur|La paille fait une ombre ronde.",
            "maman|Le panier, ensuite, près de toi.",
            "narrateur|Il glisse le tabouret d'une main.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Nina va aimer l'ombre.",
            "maman|Tu lui proposes les tomates ?",
            "enfant-m|Oui, maman.",
        )
    return L(
        "narrateur|Raphaël tire d'abord le petit tabouret.",
        "enfant-m|Les tomates du haut, avec ça.",
        "maman|Tiens-le droit, tout doux.",
        "narrateur|Le bois tape un petit toc.",
        "papa|Le panier et le chapeau, avec toi.",
        "narrateur|Il les pose près des sandales.",
        "narrateur|Les trois affaires partent ensemble.",
        "enfant-m|Nina va tout atteindre.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-m|Oui.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Au bras.",
            "maman|Oui.",
            "narrateur|Le panier rouge pend, déjà un peu lourd.",
            "narrateur|Le gravier craque sous les sandales.",
            "enfant-m|Nina est déjà dehors.",
            "papa|Je l'entends, dans le jardin.",
            "maman|Vous allez la trouver.",
            "enfant-m|Je lui propose les tomates.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Sur sa tête.",
            "papa|Oui.",
            "narrateur|Le chapeau de paille tient une ombre ronde.",
            "narrateur|Un grillon reprend, plus loin.",
            "enfant-m|Nina est déjà dehors.",
            "maman|Je l'entends, dans le jardin.",
            "papa|Le soleil tape encore, entre les plants.",
            "enfant-m|Je lui propose les tomates.",
        )
    return L(
        "enfant-m|Près des pieds.",
        "maman|Oui.",
        "narrateur|Le petit tabouret avance, un toc après l'autre.",
        "narrateur|La terre tiède colle aux sandales.",
        "enfant-m|Nina est déjà dehors.",
        "papa|Je l'entends, dans le jardin.",
        "maman|Les plants laissent un sentier étroit.",
        "enfant-m|Je lui propose les tomates.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Nina est dans le jardin, quelque part.",
        "narrateur|Le robinet chante encore un filet.",
        "narrateur|Le figuier fait une ombre ronde.",
        "narrateur|Le bac à sable garde des miettes.",
        "papa|On l'invite où, Raphaël ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le panier rouge voyage vers le robinet.",
            2: "narrateur|Le chapeau de paille penche vers le robinet.",
            3: "narrateur|Le petit tabouret avance vers le robinet.",
        }[t1]
        return L(
            lead,
            "narrateur|Nina frotte un caillou blanc, tout absorbée.",
            "enfant-m|Nina, les tomates sont prêtes.",
            "narrateur|Elle ne lève pas encore les yeux.",
            "copine|Il est encore sale, mon caillou.",
            "enfant-m|Tu viens cueillir ?",
            "copine|Je n'ai pas fini.",
            "maman|Elle lave encore, tout concentrée.",
            "papa|Tu proposes comment, Raphaël ?",
        )
    if t2 == 2:
        lead = {
            1: f"narrateur|{o['cap']} s'arrête sous le figuier.",
            2: f"narrateur|{o['cap']} glisse sous le figuier.",
            3: f"narrateur|{o['cap']} bute sous le figuier.",
        }[t1]
        return L(
            lead,
            "narrateur|Nina est allongée sous les grandes feuilles.",
            "copine|J'ai trop chaud, Raphaël.",
            "enfant-m|Les tomates sont là-bas.",
            "narrateur|Une feuille de figue tapote son front.",
            "enfant-m|Tu viens ?",
            "copine|Je ne veux pas bouger.",
            "maman|Elle a trop chaud, encore.",
            "papa|Tu fais comment, Raphaël ?",
        )
    lead = {
        1: f"narrateur|{o['cap']} pose son ombre sur le bac.",
        2: f"narrateur|{o['cap']} fait un rond sur le bac.",
        3: f"narrateur|{o['cap']} pose un pied près du bac.",
    }[t1]
    return L(
        lead,
        "narrateur|Nina patouille un gâteau de sable.",
        "copine|Il n'est pas cuit, encore.",
        "enfant-m|Les tomates m'attendent.",
        "narrateur|Le gâteau penche, tout mouillé.",
        "enfant-m|Tu viens cueillir ?",
        "copine|Après, peut-être.",
        "maman|Son gâteau n'est pas fini.",
        "papa|Tu proposes quoi, Raphaël ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Nina frotte encore son caillou blanc.",
            "papa|Attendre, prendre le caillou, ou laver ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Nina reste collée à l'ombre du figuier.",
            "maman|L'eau, l'ombre des plants, ou garder une tomate ?",
        )
    return L(
        "narrateur|Le gâteau de sable penche encore.",
        "papa|Attendre, déplacer, ou plus tard ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le panier rouge attend derrière elle.",
            2: "narrateur|Le chapeau de paille attend derrière elle.",
            3: "narrateur|Le petit tabouret attend derrière elle.",
        }[t1]
        return L(
            "enfant-m|J'attends un peu.",
            "copine|Merci, Raphaël.",
            "narrateur|L'eau coule, puis se tait.",
            wait,
            "narrateur|Nina lève le caillou, enfin propre.",
            "copine|Je viens, maintenant.",
            "enfant-m|Les tomates sont encore chaudes.",
            "papa|Tu as laissé son caillou finir.",
            "maman|Elle a dit oui, à son heure.",
        )
    if t2 == 1 and t3 == 2:
        take = {
            1: "narrateur|Le caillou blanc entre dans le panier.",
            2: "narrateur|Le caillou blanc se pose dans le chapeau.",
            3: "narrateur|Le caillou blanc s'assoit sur le tabouret.",
        }[t1]
        return L(
            "enfant-m|Ton caillou peut venir, avec nous.",
            "copine|Avec les tomates ?",
            "enfant-m|Si tu veux.",
            take,
            "narrateur|Nina pose le caillou, tout blanc.",
            "copine|Il va nous regarder.",
            "enfant-m|On cueille ensemble, alors.",
            "papa|Tu as pris son jeu avec toi.",
            "maman|Le caillou a sa place.",
        )
    if t2 == 1 and t3 == 3:
        wash = {
            1: "narrateur|Il pose une tomate dans le panier, sous l'eau.",
            2: "narrateur|Le chapeau fait de l'ombre sur leurs mains.",
            3: "narrateur|Il s'assoit sur le tabouret, tout près.",
        }[t1]
        return L(
            "enfant-m|Je lave une tomate, avec toi.",
            wash,
            "narrateur|Ils frottent sous le filet d'eau.",
            "copine|Elle est propre, maintenant.",
            "enfant-m|On va en chercher d'autres ?",
            "copine|Oui, après celle-là.",
            "papa|Tu t'es assis à son jeu.",
            "maman|Elle a proposé la suite.",
            f"narrateur|{o['cap']} reste mouillé, tout calme.",
        )
    if t2 == 2 and t3 == 1:
        water = {
            1: "narrateur|Il penche le panier, une gorgée au fond.",
            2: "narrateur|Il lui tend le chapeau, pour faire de l'ombre.",
            3: "narrateur|Il pose le tabouret, une tasse dessus.",
        }[t1]
        return L(
            "enfant-m|Je t'apporte de l'eau, d'abord.",
            water,
            "narrateur|Nina boit, tout doux, à petites gorgées.",
            "copine|C'est mieux.",
            "enfant-m|Tu viens, si tu veux.",
            "copine|Oui, j'arrive.",
            "papa|Tu as attendu qu'elle ait moins chaud.",
            "maman|Elle a dit oui, après l'eau.",
            "narrateur|Une feuille de figue retombe, plus légère.",
        )
    if t2 == 2 and t3 == 2:
        shade = {
            1: "narrateur|Le panier rouge glisse vers l'ombre des plants.",
            2: "narrateur|Le chapeau de paille avance vers les plants.",
            3: "narrateur|Le petit tabouret avance vers les plants.",
        }[t1]
        return L(
            "enfant-m|L'ombre des plants est fraîche, aussi.",
            "copine|Moins que le figuier.",
            "enfant-m|On cueille là, si tu veux.",
            "copine|D'accord, à l'ombre.",
            shade,
            "narrateur|Ils glissent entre les feuilles, tout calmes.",
            "papa|Vous restez au frais, tous les deux.",
            "maman|Les tomates pendent, juste là.",
            "enfant-m|Celle-ci, pour toi.",
        )
    if t2 == 2 and t3 == 3:
        keep = {
            1: "narrateur|Une tomate rouge attend dans le panier, à part.",
            2: "narrateur|Une tomate rouge attend sous le chapeau.",
            3: "narrateur|Une tomate rouge attend sur le tabouret.",
        }[t1]
        return L(
            "copine|Plus tard, Raphaël.",
            "enfant-m|D'accord.",
            "enfant-m|Je t'en garde une, alors.",
            keep,
            "narrateur|Nina ferme les yeux, un moment.",
            "copine|Merci.",
            "papa|Sa tomate reste avec elle.",
            "maman|Vous vous retrouvez, tout à l'heure.",
            "narrateur|Le figuier garde son ombre ronde.",
        )
    if t2 == 3 and t3 == 1:
        cake = {
            1: "narrateur|Le panier rouge fait un four, tout calme.",
            2: "narrateur|Le chapeau de paille fait un toit, tout calme.",
            3: "narrateur|Le petit tabouret fait une table, tout calme.",
        }[t1]
        return L(
            "enfant-m|Je reste jusqu'au gâteau.",
            "copine|Il manque le soleil, dessus.",
            cake,
            "narrateur|Ils soufflent une fois, tout bas.",
            "copine|Il est cuit, maintenant.",
            "enfant-m|On cueille, alors ?",
            "copine|Oui.",
            "papa|Tu as attendu la fin.",
            "maman|Le gâteau a eu son temps.",
        )
    if t2 == 3 and t3 == 2:
        move = {
            1: "narrateur|Le gâteau voyage dans le panier, tout fragile.",
            2: "narrateur|Le gâteau voyage sous le chapeau, tout fragile.",
            3: "narrateur|Le gâteau voyage sur le tabouret, tout fragile.",
        }[t1]
        return L(
            "enfant-m|Le gâteau peut voyager, près des plants.",
            "copine|Sans le casser ?",
            "enfant-m|Tout doux.",
            move,
            "narrateur|Le sable tient, à peine.",
            "copine|Il est venu avec nous.",
            "enfant-m|On cueille, et il nous regarde.",
            "papa|Tu as mêlé les deux jeux.",
            "maman|Rien n'a été laissé derrière.",
        )
    later = {
        1: "narrateur|Le panier rouge reste au bord du bac.",
        2: "narrateur|Le chapeau de paille reste au bord du bac.",
        3: "narrateur|Le petit tabouret reste au bord du bac.",
    }[t1]
    return L(
        "enfant-m|On cueille plus tard, alors ?",
        "copine|Oui, plus tard.",
        "enfant-m|D'accord.",
        later,
        "narrateur|Nina lisse encore un bord.",
        "copine|Garde-moi une tomate rouge.",
        "enfant-m|Elle t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le gâteau continue, tout calme.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = f"narrateur|{o['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils rentrent les tomates, enfin chaudes.",
            "copine|Mon caillou est propre, maintenant.",
            "enfant-m|Toi aussi, tu es venue.",
            "papa|La salade attend sur la marche.",
            "maman|Le pain a encore une croûte.",
            coda,
            "narrateur|Nina pose le caillou près du sel.",
            "enfant-m|C'est notre salade, maintenant.",
            "narrateur|Un grillon reprend, plus loin.",
        )
    if t2 == 1 and t3 == 2:
        vu = {
            1: "copine|Il a tout vu, du panier.",
            2: "copine|Il a tout vu, du chapeau.",
            3: "copine|Il a tout vu, du tabouret.",
        }[t1]
        return L(
            "narrateur|Le caillou blanc veille entre les tomates.",
            "enfant-m|Tu as dit oui, avec lui.",
            vu,
            "papa|Vous avez cueilli sans tirer.",
            "maman|Goûtez un peu, tout doux.",
            coda,
            "narrateur|Nina croque, le jus lui tache le menton.",
            "enfant-m|Reste autant que tu veux.",
            "narrateur|Le sel brille déjà sur la marche.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Après l'eau, ils glissent entre les plants.",
            "copine|On a lavé ensemble, d'abord.",
            "enfant-m|Puis tu as dit : on y va.",
            "maman|Deux mains mouillées, puis deux tomates.",
            "papa|Le jardin redevient calme.",
            coda,
            "narrateur|Nina rit, tout petit.",
            "enfant-m|La salade t'a attendue.",
            "narrateur|L'arrosoir sèche déjà, près du mur.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Après l'eau, le figuier les laisse partir.",
            "copine|J'avais moins chaud, alors j'ai dit oui.",
            "enfant-m|Ta tomate est celle-là.",
            "papa|Vous tenez tous les deux, entre les plants.",
            "maman|Le pain descend jusqu'à la marche.",
            coda,
            "narrateur|Nina souffle sur une graine, tout doux.",
            "enfant-m|C'est le signal.",
            "narrateur|Une feuille de figue reste au seuil.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|L'ombre des plants a deux places, maintenant.",
            "enfant-m|La tienne, et la mienne.",
            "copine|C'est la nôtre, Raphaël.",
            "papa|Vous avez changé d'ombre, pas de jeu.",
            "maman|La salade, au milieu, pour deux.",
            coda,
            "narrateur|Nina souffle, puis Raphaël souffle.",
            "enfant-m|On reste encore un peu.",
            "narrateur|Une tomate garde encore sa chaleur.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Plus tard, Nina rejoint la marche.",
            "copine|Ma tomate m'a attendue.",
            "enfant-m|Tu avais dit plus tard.",
            "papa|Le plus tard a eu sa place.",
            "maman|Vous mangez encore ensemble, d'ici.",
            coda,
            "narrateur|Nina tend une main, vers le sel.",
            "enfant-m|Je te la passe, d'à côté.",
            "narrateur|Le figuier laisse une ombre ronde.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le gâteau de sable est déjà fini.",
            "copine|J'ai eu le temps, juste assez.",
            "enfant-m|Merci d'être venue.",
            "papa|Vous avez soufflé une fois, tout bas.",
            "maman|Les tomates sont dans l'assiette, maintenant.",
            coda,
            "narrateur|Nina fait un signe vers le bac.",
            "enfant-m|Le gâteau t'a vue, une minute.",
            "narrateur|Le sable du bac redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le gâteau de sable veille près des plants.",
            "enfant-m|Il a voyagé avec nous.",
            "copine|Sans se casser.",
            "papa|Vous avez mêlé les deux envies.",
            "maman|Le pain sent encore le four.",
            coda,
            "narrateur|Nina pose un grain de sable, tout loin.",
            "enfant-m|La salade est à nous.",
            "narrateur|Une fourmi croise une graine, puis s'en va.",
        )
    return L(
        "narrateur|Nina arrive, le gâteau enfin lisse.",
        "copine|Plus tard, j'avais dit.",
        "enfant-m|Ta tomate t'a attendue.",
        "papa|Vous vous retrouvez sur la marche.",
        "maman|Goûtez, tout doux, avant le soir.",
        coda,
        "narrateur|Raphaël souffle sur une graine chaude.",
        "enfant-m|Elle t'attendait, Nina.",
        "narrateur|La marche garde une tache rouge, toute petite.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Les feuilles de tomate sentent le soleil.",
        "narrateur|Elles collent un peu, toutes chaudes.",
        "narrateur|Un grillon frotte dans l'herbe sèche.",
        "narrateur|La terre du potager reste encore tiède.",
        "papa|L'arrosoir goutte encore, Raphaël.",
        "maman|Le pain attend, dans la cuisine.",
        "narrateur|En ce moment, Raphaël touche une tomate.",
        "enfant-m|Elle est lourde, trop rouge.",
        "narrateur|Le jus tache déjà son pouce.",
        "enfant-m|Je la veux avec Nina.",
        "maman|On cueille, alors ?",
        "papa|Merci, tu la tiens tout doux.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des plants.",
        "narrateur|Le panier, le chapeau, et le tabouret.",
        "maman|Tu prends quoi d'abord, Raphaël ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le panier rouge", "le chapeau de paille", "le petit tabouret")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        if t1 == 1:
            s[f"{p}_Q0001"] = L(
                "narrateur|Raphaël a passé le panier rouge.",
                "maman|Il est où, maintenant ?",
            )
        elif t1 == 2:
            s[f"{p}_Q0001"] = L(
                "narrateur|Raphaël a mis le chapeau de paille.",
                "maman|Il est où, maintenant ?",
            )
        else:
            s[f"{p}_Q0001"] = L(
                "narrateur|Raphaël a tiré le petit tabouret.",
                "maman|Il est où, maintenant ?",
            )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le robinet", "le figuier", "le bac à sable")

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
        "Raphaël veut cueillir les dernières tomates avec Nina, puis la salade "
        "sur la marche. T1 = panier rouge / chapeau de paille / petit tabouret "
        "(les trois partent). T2 = robinet (caillou) / figuier (trop chaud) / "
        "bac à sable (gâteau). T3 = neuf résolutions : attendre, prendre le caillou, "
        "laver ; apporter l'eau, changer d'ombre, garder une tomate ; attendre le "
        "gâteau, le déplacer, plus tard. La leçon se vit : il propose, il accepte "
        "oui, non, ou une autre idée. Fin : salade, pain, marche, grillon.",
        "N2 ≤ 15. Hugo et le slogan « Inviter sans forcer » jetés. Autre récit "
        "que DIF-021 (pas de fort, pas de fenêtre, pas de coussins). Un merci "
        "de papa lié au geste (tenir la tomate). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
