#!/usr/bin/env python3
"""TREE-DIF-024 — Le cerf-volant de Chouchou dans le pommier (N1, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-024"
N1 = 10


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
    out["fil_rouge"] = (
        "Après le vent, le cerf-volant de Chouchou dort dans le pommier. "
        "Elle le veut pour voler encore. Aniss est plus grand. "
        "Ils emportent ficelle, bâton et tabouret. "
        "Trois coins, neuf façons. Le papier rentre à la maison."
    )
    out["title"] = "Le cerf-volant de Chouchou dans le pommier"
    out["characters"] = "Chouchou, Aniss, papa, maman"
    out["setting"] = "jardin, pommier après le vent"
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
        "tailles sont différentes",
        "le corps n'est pas",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "inès",
        "ines",
        "sami",
        "léa",
        " toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
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


OBJ = {
    1: {
        "lab": "la ficelle",
        "cap": "La ficelle",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | dans ma poche",
        "t1retry": "Le papier est dans la poche.",
    },
    2: {
        "lab": "le bâton",
        "cap": "Le bâton",
        "t1q": "sur le bâton",
        "t1acc": "bâton | le bâton | sur le bâton | le bois",
        "t1retry": "Le papier est sur le bâton.",
    },
    3: {
        "lab": "le tabouret",
        "cap": "Le tabouret",
        "t1q": "sous le tabouret",
        "t1acc": "tabouret | le tabouret | sous le tabouret | le bois",
        "t1retry": "Le papier est sous le tabouret.",
    },
}

T3_LABS = {
    1: ("le passage de Chouchou", "la branche levée", "le vent qui défait"),
    2: ("les mains d'Aniss", "le bâton d'en bas", "tirer à deux"),
    3: ("le tabouret d'Aniss", "la ficelle lancée", "le geste d'en bas"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Chouchou enroule la ficelle, tout doux.",
            "enfant-f|Le papier va avec.",
            "maman|Glisse-le dans ta poche.",
            "narrateur|Le bout de papier fait un froissement.",
            "papa|Le bâton aussi, près du sac.",
            "narrateur|Maman pose le tabouret contre le tronc.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Aniss, viens sous le pommier.",
            "enfant-m|J'arrive, Chouchou.",
            "papa|La ficelle d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Chouchou prend le bâton, encore tiède.",
            "enfant-f|Je pique le papier dessus.",
            "papa|Enroule-le, comme un drapeau.",
            "narrateur|Le bois sent encore la sève.",
            "maman|La ficelle, ensuite, près des pieds.",
            "narrateur|Elle glisse le tabouret d'une main.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Aniss, on y va.",
            "enfant-m|Je suis là.",
            "maman|Le bâton d'abord, il est prêt.",
        )
    return L(
        "narrateur|Chouchou tire le tabouret, tout rêche.",
        "enfant-f|Le papier reste dessous.",
        "maman|Tiens-le droit, tout doux.",
        "narrateur|Le bois tape un petit toc.",
        "papa|La ficelle et le bâton, avec vous.",
        "narrateur|Il les pose près des sandales.",
        "narrateur|Les trois affaires partent ensemble.",
        "enfant-f|Aniss, vite !",
        "enfant-m|J'arrive sous l'arbre.",
        "papa|Le tabouret d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            f"narrateur|{o['cap']} porte le papier, dans la poche.",
            "enfant-m|Ça a fait un froissement.",
            "enfant-f|C'est pour retrouver le cerf-volant.",
            "maman|Le grand bleu vous attend, plus haut.",
            "papa|On avance sous les feuilles ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            f"narrateur|{o['cap']} tient le papier, comme un drapeau.",
            "enfant-m|Je vois un coin, tout bleu.",
            "enfant-f|Ne touche pas encore.",
            "papa|Ça sent déjà la sève, ici.",
            "maman|Vos pieds, dans l'herbe ?",
            "enfant-m|Oui, maman.",
        )
    return L(
        f"narrateur|{o['cap']} cache le papier, tout rêche.",
        "enfant-m|Il roule un peu.",
        "enfant-f|Je le rattrape.",
        "maman|Le pommier est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le pommier ouvre trois coins.",
        "narrateur|Sous les branches, l'ombre est basse.",
        "narrateur|Dans la fourche, le papier brille.",
        "narrateur|Tout en haut, une queue danse.",
        "papa|Où allez-vous, sous le pommier ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|La ficelle frotte une feuille basse.",
            2: "narrateur|Le bâton accroche une brindille.",
            3: "narrateur|Le tabouret bute contre une racine.",
        }[t1]
        return L(
            lead,
            "narrateur|Les branches basses font un tunnel vert.",
            "enfant-f|J'y vais.",
            "narrateur|Chouchou penche la tête, assez petite.",
            "enfant-f|Ça me touche à peine.",
            "enfant-m|Moi, je reste coincé.",
            "narrateur|Aniss bute du front, trop grand.",
            "papa|Tes épaules passent, Chouchou.",
            "narrateur|La queue du cerf-volant s'enroule là.",
            "enfant-f|Elle est mêlée, tout bas.",
            "maman|Vous la prenez comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: f"narrateur|{o['cap']} penche, trop vite, vers la fourche.",
            2: f"narrateur|{o['cap']} tape un peu l'écorce chaude.",
            3: f"narrateur|{o['cap']} s'enfonce un peu, près du tronc.",
        }[t1]
        return L(
            lead,
            "narrateur|La fourche du tronc est chaude, rêche.",
            "enfant-m|Je vois le papier, là-dedans.",
            "narrateur|Aniss a les yeux assez hauts.",
            "narrateur|Les bras de Chouchou restent trop courts.",
            "enfant-f|Moi, je vois que l'écorce.",
            "papa|Tes yeux sont plus hauts, Aniss.",
            "maman|Les mains de Chouchou sont plus près.",
            "enfant-f|On le sort comment ?",
        )
    lead = {
        1: f"narrateur|{o['cap']} pose un toc contre le tronc.",
        2: f"narrateur|{o['cap']} glisse sur l'herbe sèche.",
        3: f"narrateur|{o['cap']} cogne le pied du tronc.",
    }[t1]
    return L(
        lead,
        "narrateur|La branche haute tremble, tout légère.",
        "enfant-f|Je me hausse, pour le cerf-volant.",
        "narrateur|Chouchou lève les talons, trop petite.",
        "narrateur|Ses doigts frôlent l'air, pas plus.",
        "enfant-m|Mes bras vont plus loin.",
        "papa|Le tabouret n'est pas assez, tout seul.",
        "maman|Chouchou, tu restes en bas.",
        "enfant-f|Il brille, juste au-dessus.",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La queue reste coincée dans les feuilles.",
            "papa|Le passage de Chouchou, la branche, ou le vent ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le papier se cache dans la fourche.",
            "maman|Les mains d'Aniss, le bâton, ou tirer ?",
        )
    return L(
        "narrateur|Le cerf-volant reste trop loin, tout haut.",
        "papa|Tabouret, ficelle, ou geste d'en bas ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Chouchou pousse la ficelle sous les feuilles.",
            2: "narrateur|Chouchou glisse le bâton sous le tunnel.",
            3: "narrateur|Chouchou pousse le tabouret sous le vert.",
        }[t1]
        return L(
            "enfant-f|Je passe, Aniss.",
            "narrateur|Chouchou rampe, tout petite, sous le vert.",
            "enfant-m|Doucement.",
            use,
            "narrateur|Ses doigts dénouent la queue, tout lent.",
            "enfant-f|Je la tiens !",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Le cerf-volant glisse à leur hauteur.",
            "enfant-m|Regarde, Chouchou.",
            "enfant-f|Il est à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|La ficelle attend en bas, plein d'ombre.",
            2: "narrateur|Le bâton attend en bas, un peu vert.",
            3: "narrateur|Le tabouret attend en bas, un peu humide.",
        }[t1]
        return L(
            "enfant-m|Je soulève la branche.",
            "papa|Je te tiens, Aniss.",
            "narrateur|Aniss lève le bois, plus haut que Chouchou.",
            "enfant-f|Je vois la queue !",
            "narrateur|Chouchou tend les deux mains.",
            "narrateur|La queue glisse vers elle.",
            "enfant-m|Elle est à toi, un moment.",
            "maman|Vous la partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        catch = {
            1: "narrateur|La ficelle cueille la queue, tout doux.",
            2: "narrateur|Le bâton cueille la queue, tout rêche.",
            3: "narrateur|Le tabouret cueille la queue, toc.",
        }[t1]
        return L(
            "enfant-f|On attend un peu.",
            "enfant-m|Moi aussi, j'attends.",
            "narrateur|Un souffle passe dans les feuilles.",
            "narrateur|La queue se défait, toute seule.",
            catch,
            "papa|Elle est venue vers vous.",
            "enfant-m|On l'a reprise.",
            "enfant-f|Elle brille encore.",
            "maman|Vos cheveux sentent la feuille.",
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Aniss pose le papier contre la ficelle.",
            2: "narrateur|Aniss pose le papier contre le bâton.",
            3: "narrateur|Aniss pose le papier sur le tabouret.",
        }[t1]
        return L(
            "enfant-m|Je ramasse, tout près de la fourche.",
            "enfant-f|Je te guide, d'en bas.",
            "narrateur|Aniss écarte deux brindilles, tout doux.",
            "narrateur|Le papier bleu est là, collé.",
            "enfant-m|Je le tiens !",
            carry,
            "papa|Tes mains étaient à la bonne hauteur.",
            "enfant-f|Passe-le, un peu.",
            "enfant-m|Il est encore chaud.",
        )
    if t2 == 2 and t3 == 2:
        reach = {
            1: "narrateur|Chouchou tend la ficelle, bras tout courts.",
            2: "narrateur|Chouchou tend le bâton, bras tout courts.",
            3: "narrateur|Chouchou pousse le tabouret, tout près.",
        }[t1]
        return L(
            "enfant-f|Je reste ici, plus bas.",
            "enfant-m|Je vais où tu dis.",
            reach,
            "narrateur|Chouchou pousse, tout doux, d'en bas.",
            "narrateur|Aniss voit le bleu, dans la fourche.",
            "enfant-m|Je le tiens !",
            "maman|Tes yeux ont trouvé le chemin.",
            "enfant-f|Il sent l'écorce.",
            "papa|Soufflez dessus, tout léger.",
        )
    if t2 == 2 and t3 == 3:
        nest = {
            1: "narrateur|La ficelle devient un nid, contre l'écorce.",
            2: "narrateur|Le bâton devient un nid, contre l'écorce.",
            3: "narrateur|Le tabouret devient un nid, contre l'écorce.",
        }[t1]
        return L(
            "enfant-f|Papa, écarte un peu ?",
            "papa|Je fais un chemin, tout doux.",
            "narrateur|Les brindilles s'ouvrent, comme une porte.",
            "narrateur|Le papier bleu apparaît, collé.",
            nest,
            "enfant-m|On le prend ensemble.",
            "enfant-f|Oui.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux paires de mains tiennent le papier.",
        )
    if t2 == 3 and t3 == 1:
        hold = {
            1: "narrateur|Chouchou garde la ficelle au pied.",
            2: "narrateur|Chouchou garde le bâton au pied.",
            3: "narrateur|Chouchou garde le tabouret au pied.",
        }[t1]
        return L(
            "enfant-m|Je me hausse encore.",
            hold,
            "narrateur|Les doigts d'Aniss touchent le papier.",
            "enfant-m|Il bouge !",
            "narrateur|Le cerf-volant penche, puis se détache.",
            "enfant-f|Je le rattrape.",
            "papa|Tes doigts allaient assez loin.",
            "maman|Chouchou tenait bien le bas.",
            "enfant-m|Il est à nous.",
        )
    if t2 == 3 and t3 == 2:
        up = {
            1: "narrateur|Chouchou lance la ficelle, tout léger.",
            2: "narrateur|Chouchou tend le bâton, tout léger.",
            3: "narrateur|Chouchou pousse le tabouret, tout près.",
        }[t1]
        return L(
            "enfant-f|On lance la ficelle ?",
            "enfant-m|Oui, tout doux.",
            up,
            "narrateur|Papa tient le bois, tout ferme.",
            "narrateur|Chouchou et Aniss tendent ensemble.",
            "enfant-f|Elle accroche !",
            "enfant-m|Je la sens.",
            "maman|Vous avez tiré ensemble.",
            "papa|La ficelle est restée douce.",
        )
    two = {
        1: "narrateur|Aniss tend la ficelle, bras tout longs.",
        2: "narrateur|Aniss tend le bâton, bras tout longs.",
        3: "narrateur|Aniss pousse le tabouret, tout près.",
    }[t1]
    return L(
        "enfant-f|Reste en haut, Aniss.",
        "enfant-m|Je tends, d'ici.",
        two,
        "narrateur|Aniss fait basculer le papier, tout doux.",
        "narrateur|Le cerf-volant tombe dans les mains d'en bas.",
        "enfant-f|Je le tiens !",
        "papa|Chacun a fait sa part.",
        "enfant-m|Il sent le soleil.",
        "maman|Vos bras n'avaient pas la même longueur.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = {
        1: "narrateur|La ficelle sèche près des sandales.",
        2: "narrateur|Le bâton sèche près des sandales.",
        3: "narrateur|Le tabouret sèche près des sandales.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils rentrent, le papier au creux.",
            "enfant-m|Il sent encore la feuille.",
            "enfant-f|Tes épaules l'ont laissé passer.",
            "papa|Vous l'avez pris, enfin.",
            "maman|Posez-le sur la table, au calme.",
            "narrateur|Le tronc garde une ombre, tout petit.",
            coda,
            "narrateur|Un bourdon passe, plus loin.",
            "narrateur|Le bleu dort contre le bois.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous la branche, la maison paraît petite.",
            "enfant-f|Aniss, tu l'as vue glisser.",
            "enfant-m|Oui, tout près de tes mains.",
            "papa|Je t'ai tenu, pas trop longtemps.",
            "maman|Vos têtes, haute et basse, rentrent.",
            "narrateur|Le papier reste dans la paume de Chouchou.",
            coda,
            "narrateur|Une feuille reste collée aux cheveux.",
            "narrateur|La table sent encore le vent.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le souffle du pommier les suit jusqu'à la porte.",
            "enfant-m|Elle est tombée vers nous.",
            "enfant-f|On a attendu, tous les deux.",
            "maman|Elle n'était plus trop mêlée.",
            "papa|Le papier froisse encore, dans l'air.",
            f"narrateur|{o['cap']} pose une feuille, tout léger.",
            "narrateur|La porte claque, tout doux.",
            "narrateur|Une odeur de pomme reste dans l'entrée.",
            "narrateur|Le bleu veille près des souliers.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Ils rentrent avec de l'écorce aux genoux.",
            "enfant-m|Mes mains savaient le chemin.",
            "enfant-f|Moi, je voyais trop bas.",
            "papa|Vous avez suivi ce qui était à vous.",
            "maman|Soufflez le dernier brin, dehors.",
            "enfant-f|Il est pour voler, demain.",
            "enfant-m|Il est un peu chaud encore.",
            coda,
            "narrateur|L'écorce sèche déjà sur le palier.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils n'ont pas couru dans tout le pré.",
            "enfant-f|Je l'ai poussé d'en bas.",
            "enfant-m|Tes bras étaient assez courts.",
            "maman|L'écorce sent fort, sur vos mains.",
            "papa|Lavez-les, tout doux, au bac.",
            f"narrateur|{o['cap']} garde un brin d'écorce.",
            "enfant-m|Je le tiens, Chouchou.",
            "narrateur|Le bac goutte, puis se tait.",
            "narrateur|Le papier sèche près de la fenêtre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Leurs chaussettes portent encore de l'herbe.",
            "enfant-f|Papa a ouvert un chemin.",
            "enfant-m|On l'a pris ensemble.",
            "papa|L'écorce vous a laissé la place.",
            "maman|Changez le linge des pieds, d'abord.",
            coda,
            "narrateur|Un coin de papier marque le carreau.",
            "enfant-f|Regarde-le, Aniss, il brille.",
            "narrateur|Le bleu reste au chaud, sur la table.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les talons d'Aniss sont encore chauds.",
            "enfant-f|Tu l'as fait pencher pour moi.",
            "enfant-m|Tu tenais le bas.",
            "maman|Essuie tes pieds, sur le paillasson.",
            "papa|Le cerf-volant est à vous, maintenant.",
            "narrateur|Chouchou le pose contre la vitre.",
            coda,
            "narrateur|Un rai de soleil traverse le bleu.",
            "narrateur|Dehors, la branche redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Un peu de soleil les suit jusqu'à la porte.",
            "enfant-m|Tu l'as lancée, d'en bas.",
            "enfant-f|Tes bras l'ont fait descendre.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du tabouret sèche déjà.",
            f"narrateur|{o['cap']} pose une ombre au carrelage.",
            "enfant-m|Il brille trop, Chouchou.",
            "enfant-f|C'est pour ça.",
            "narrateur|La vitre garde le bleu, tout proche.",
        )
    return L(
        "narrateur|Un peu de poussière d'herbe reste au seuil.",
        "enfant-f|On a tiré ensemble.",
        "enfant-m|Sans trop monter.",
        "papa|Le tabouret est resté à sa place.",
        "maman|Vos mains sentent encore le vent.",
        coda,
        "narrateur|Chouchou pose le papier au rebord.",
        "enfant-m|Tu l'as eu, enfin.",
        "narrateur|Le bleu tremble un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "oiseau"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Un bout de papier tremble sur le carreau.",
        "narrateur|Le vent passe dans les pommes.",
        "narrateur|Une ficelle traîne dans l'herbe chaude.",
        "papa|Tu as vu l'ombre, Chouchou ?",
        "enfant-f|Elle court sur le mur.",
        "maman|Le papier sent encore le soleil.",
        "narrateur|En ce moment, Chouchou lève le nez.",
        "narrateur|Son cerf-volant dort dans le pommier.",
        "enfant-f|Je le veux, pour voler.",
        "papa|Aniss arrive, plus grand que toi.",
        "narrateur|Aniss a de l'ombre jusqu'aux épaules.",
        "enfant-m|On le prend ensemble ?",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu regardes bien le papier.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent sous l'arbre.",
        "narrateur|La ficelle, le bâton, et le tabouret.",
        "maman|Tu prends quoi d'abord, Chouchou ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la ficelle", "le bâton", "le tabouret")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Chouchou a glissé le papier {o['t1q']}.",
            "maman|Il est où, le bout de papier ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("les branches basses", "la fourche", "la branche haute")

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
        "Le cerf-volant de Chouchou dans le pommier",
        "Après le vent, le cerf-volant de Chouchou dort dans le pommier. "
        "Elle le veut pour voler encore. Aniss est plus grand. "
        "T1 = ficelle / bâton / tabouret (les trois partent). "
        "T2 = branches basses trop basses pour Aniss / fourche trop haute "
        "pour Chouchou / branche trop haute pour elle seule. "
        "T3 = neuf résolutions (passage de Chouchou, branche levée, vent qui "
        "défait ; mains d'Aniss, bâton d'en bas, tirer à deux ; tabouret "
        "d'Aniss, ficelle lancée, geste d'en bas). La leçon (tailles, jouer "
        "ensemble) se vit dans les gestes, sans slogan. Fin : le papier "
        "rentre à la maison.",
        "N1 ≤ 10. Inès / Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre leçon collée remplacé (objet + désir). Autre récit que "
        "DIF-014 (cerf-volant, pas la pomme du haut). Un merci de papa lié "
        "au geste (regarder le papier). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
