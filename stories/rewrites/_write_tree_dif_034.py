#!/usr/bin/env python3
"""TREE-DIF-034 — Le soleil en papier d'Amir, à l'école (N3, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-034"
N3 = 16
TITLE = "Le soleil en papier d'Amir, à l'école"
FIL = (
    "À l'école, le matin de la fête. Amir a collé un soleil en papier. "
    "Il veut le voir briller, haut. Nino est plus grand. Ils emportent "
    "le ruban jaune, la pince à linge et le petit tabouret. Aux patères, "
    "à la fenêtre, sous les tables : trois lieux, neuf façons. "
    "Le soleil brille pour eux."
)


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
    out["characters"] = "Amir, Nino, papa, maman"
    out["setting"] = "école : vestiaire, classe, tables"
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
        "tailles différentes",
        "plus petit ou plus grand",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "capitaine",
        "plic",
        "volet jaune",
        "pommier",
        "chambre",
        "marelle",
        "bac à sable",
        "toboggan",
        "balançoire",
        "sami",
        " léa",
        " lea",
        "tom ",
        "doudou",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
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
        "lab": "le ruban jaune",
        "cap": "Le ruban jaune",
        "t1q": "autour du poignet",
        "t1acc": "poignet | le poignet | autour du poignet | son poignet",
        "t1retry": "Le ruban est autour du poignet.",
    },
    2: {
        "lab": "la pince à linge",
        "cap": "La pince à linge",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "La pince est dans la poche.",
    },
    3: {
        "lab": "le petit tabouret",
        "cap": "Le petit tabouret",
        "t1q": "derrière les pieds",
        "t1acc": "pieds | les pieds | derrière les pieds | ses pieds",
        "t1retry": "Le tabouret est derrière les pieds.",
    },
}

T3_LABS = {
    1: ("les bras de Nino", "le tabouret d'Amir", "la pince ensemble"),
    2: ("la poignée de Nino", "le tabouret du radiateur", "le rebord ensemble"),
    3: ("le passage d'Amir", "soulever la table", "un dessous un dessus"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir enroule le ruban jaune, encore collant.",
            "enfant-m|Il sent la colle, tout près.",
            "maman|Glisse-le autour de ton poignet.",
            "narrateur|Le jaune froisse contre la manche.",
            "papa|La pince, ensuite, dans la poche.",
            "narrateur|Nino tire le petit tabouret, toc.",
            "narrateur|Tout voyage avec eux, dans le couloir.",
            "enfant-m|Nino, tu viens près des patères ?",
            "copain|J'arrive, Amir.",
            "papa|Le ruban d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir prend la pince à linge, encore tiède.",
            "enfant-m|Elle pince un peu, sur le doigt.",
            "papa|Glisse-la dans ta poche, tout droit.",
            "narrateur|Un clic de bois, tout petit.",
            "maman|Le ruban, ensuite, autour du poignet.",
            "narrateur|Nino tire le petit tabouret, toc.",
            "narrateur|Tout voyage avec eux, dans le couloir.",
            "enfant-m|Nino va tout voir.",
            "narrateur|Des épaules trop hautes passent au casier.",
            "copain|Me voilà, Amir.",
            "enfant-m|On accroche le soleil, tous les deux ?",
            "maman|La pince d'abord, elle est prête.",
        )
    return L(
        "narrateur|Amir tire le petit tabouret, un peu rêche.",
        "enfant-m|Il gratte le linoléum, tic.",
        "maman|Garde-le derrière tes pieds, tout droit.",
        "narrateur|Les pieds du bois font un petit choc.",
        "papa|Le ruban et la pince, avec vous.",
        "narrateur|Il les pose près des casiers.",
        "narrateur|Tout voyage avec eux, dans le couloir.",
        "enfant-m|Nino, vite !",
        "narrateur|Une ombre trop longue passe au casier.",
        "copain|J'arrive près des patères.",
        "enfant-m|Je te garde un bout de soleil.",
        "papa|Le tabouret d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le poignet porte le ruban, tout contre la manche.",
            "copain|Il a trop de jaune !",
            "enfant-m|C'est pour notre soleil.",
            "narrateur|Nino a les genoux plus hauts qu'Amir.",
            "narrateur|Ses mains touchent déjà le crochet du bas.",
            "maman|Il est plus grand, c'est tout.",
            "papa|On reste dans l'école ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La poche veille près de la pince.",
            "copain|J'entends le clic !",
            "enfant-m|Ne la sors pas encore.",
            "narrateur|Nino a les cheveux tout courts.",
            "narrateur|Une mèche saute quand il se baisse.",
            "papa|Ça sent déjà la colle, sur le papier.",
            "maman|Vos mains, au-dessus du tabouret ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|Le tabouret cache encore les talons.",
        "copain|Ça sent la colle.",
        "enfant-m|Le coin de départ est là.",
        "narrateur|Le pull de Nino s'arrête trop haut.",
        "narrateur|Les manches laissent ses poignets libres.",
        "maman|Le couloir est tiède, autour.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Nino tapote déjà le linoléum, tout léger.",
        "narrateur|Aux patères, les crochets brillent trop haut.",
        "narrateur|À la fenêtre, le carreau clignote.",
        "narrateur|Sous les tables, l'ombre est basse.",
        "papa|On accroche où, pour le soleil ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le ruban accroche un crochet, trop haut.",
            2: "narrateur|La pince tape un crochet, toc.",
            3: "narrateur|Le tabouret bute contre un casier.",
        }[t1]
        mishap = {
            1: "narrateur|Un bout de jaune reste coincé dans le métal.",
            2: "narrateur|Le clic de bois se perd entre les manteaux.",
            3: "narrateur|Le bois du tabouret prend une goutte froide.",
        }[t1]
        return L(
            lead,
            "narrateur|Le vestiaire sent les manteaux encore mouillés.",
            "copain|Moi je touche, Amir !",
            "narrateur|Nino se hausse, trop vite.",
            "narrateur|Ses doigts trouvent le crochet du haut.",
            mishap,
            f"enfant-m|{o['cap']} n'attendait pas ça.",
            "maman|Toi tu n'y arrives pas, tout seul.",
            "papa|Lui touche le haut, toi le bas.",
            "copain|On accroche comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Le ruban se colle au carreau, trop haut.",
            2: "narrateur|La pince glisse vers la poignée, trop vite.",
            3: "narrateur|Le tabouret se coince sous le radiateur.",
        }[t1]
        mishap = {
            1: "narrateur|Le jaune reste trop bas, sous la poignée.",
            2: "narrateur|Le clic n'atteint pas encore le loquet.",
            3: "narrateur|Le tabouret n'aide pas, tout seul, trop court.",
        }[t1]
        return L(
            lead,
            "enfant-m|Le carreau est à nous, Nino.",
            "copain|Je vois la cour, tout haut !",
            "narrateur|La poignée reste trop loin pour Amir.",
            mishap,
            "narrateur|Un peu de craie lève, puis retombe.",
            "maman|Ses bras vont jusqu'à la poignée.",
            "papa|Toi tu vois le radiateur, lui la cour.",
            "enfant-m|On peut jouer avec lui ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Le ruban rampe sous une table, trop bas.",
        2: "narrateur|La pince roule sous une chaise, toc.",
        3: "narrateur|Le tabouret bute contre un pied de table.",
    }[t1]
    mishap = {
        1: "narrateur|Le jaune prend la poussière du linoléum.",
        2: "narrateur|Le clic se perd entre les pieds de chaise.",
        3: "narrateur|Le bois gratte, puis s'arrête, coincé.",
    }[t1]
    return L(
        lead,
        "enfant-m|Ici, ça sent la craie, Nino.",
        "copain|Je me glisse, trop large !",
        "narrateur|Ses épaules butent contre le bois des tables.",
        mishap,
        f"narrateur|{o['cap']} attend au bord, un peu seul.",
        "maman|Il a les épaules trop larges, c'est tout.",
        "papa|Toi tu passes, lui pas encore.",
        "copain|On joue comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Les patères attendent encore, trop haut.",
            "papa|Les bras, le tabouret, ou la pince ensemble ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La poignée attend encore, trop loin.",
            "maman|La poignée, le tabouret, ou le rebord ?",
        )
    return L(
        "narrateur|L'ombre sous les tables attend encore.",
        "papa|Le passage, soulever, ou un dessous un dessus ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Amir tend le ruban, bras tout courts.",
            2: "narrateur|Amir tend la pince, bras tout courts.",
            3: "narrateur|Amir pousse le tabouret, tout près.",
        }[t1]
        return L(
            "enfant-m|Tu accroches, Nino.",
            "narrateur|Nino lève le soleil, assez haut.",
            "copain|Doucement.",
            use,
            "narrateur|Ses doigts trouvent un crochet froid.",
            "enfant-m|Je tiens le bas !",
            "papa|Tes bras allaient assez loin.",
            "narrateur|Le papier s'ouvre, à leur hauteur.",
            "copain|Regarde, Amir.",
            "enfant-m|Il est à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le ruban attend au bord, plein d'ombre.",
            2: "narrateur|La pince attend au bord, un peu ronde.",
            3: "narrateur|Le tabouret attend au bord, un peu chaud.",
        }[t1]
        return L(
            "enfant-m|Je monte, tout doux.",
            "papa|Tiens le bois, Amir.",
            "narrateur|Amir se hausse, plus petit que le crochet.",
            "copain|Moi je guide, tout près.",
            "narrateur|Nino tient le soleil, au-dessus.",
            "narrateur|Le papier glisse vers le métal.",
            "copain|Il est à toi, un moment.",
            "maman|Vous le partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        catch = {
            1: "narrateur|Le ruban pince le manteau, tout doux.",
            2: "narrateur|La pince attrape le papier, clic.",
            3: "narrateur|Le tabouret serre le bas, toc.",
        }[t1]
        return L(
            "enfant-m|On pince un peu.",
            "copain|Moi aussi, je pince.",
            "narrateur|Nino lève un manteau, tout haut.",
            "narrateur|Amir glisse le soleil, pendant l'ouverture.",
            catch,
            "papa|Il est venu vers vous.",
            "copain|On l'a repris.",
            "enfant-m|Il brille encore.",
            "maman|Vos cheveux sentent le manteau mouillé.",
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Nino pose le ruban contre le carreau.",
            2: "narrateur|Nino pose la pince contre le carreau.",
            3: "narrateur|Nino pose le tabouret contre le mur.",
        }[t1]
        return L(
            "copain|Je me hausse encore.",
            "enfant-m|Je tiens le papier, d'en bas.",
            "narrateur|Les doigts de Nino touchent la poignée.",
            "copain|Elle bouge !",
            "narrateur|Le soleil penche, puis s'accroche.",
            carry,
            "papa|Tes doigts allaient assez loin.",
            "maman|Amir tenait bien le bas.",
            "copain|Il est à nous.",
        )
    if t2 == 2 and t3 == 2:
        up = {
            1: "narrateur|Amir pose le ruban sur le tabouret.",
            2: "narrateur|Amir pose la pince sur le tabouret.",
            3: "narrateur|Amir pousse le tabouret, tout près.",
        }[t1]
        return L(
            "enfant-m|On monte sur le tabouret ?",
            "copain|Oui, tout doux.",
            up,
            "narrateur|Papa tient le radiateur, tout ferme.",
            "narrateur|Amir et Nino se haussent ensemble.",
            "enfant-m|Je vois la cour !",
            "copain|Je la sens.",
            "maman|Vous avez regardé ensemble.",
            "papa|Le tabouret est resté doux.",
        )
    if t2 == 2 and t3 == 3:
        two = {
            1: "narrateur|Nino tend le ruban, bras tout longs.",
            2: "narrateur|Nino tend la pince, bras tout longs.",
            3: "narrateur|Nino pousse le tabouret, tout près.",
        }[t1]
        return L(
            "enfant-m|Reste en haut, Nino.",
            "copain|Je tends, d'ici.",
            two,
            "narrateur|Nino fait basculer le loquet, tout doux.",
            "narrateur|Le rebord prend Amir, puis lui.",
            "enfant-m|Je le tiens !",
            "papa|Chacun a fait sa part.",
            "copain|Il sent la craie.",
            "maman|Vos bras n'avaient pas la même longueur.",
        )
    if t2 == 3 and t3 == 1:
        use = {
            1: "narrateur|Amir pousse le ruban sous les tables.",
            2: "narrateur|Amir glisse la pince sous le bois.",
            3: "narrateur|Amir pousse le tabouret sous le bord.",
        }[t1]
        return L(
            "enfant-m|Je passe, Nino.",
            "narrateur|Amir rampe, tout petit, sous la table.",
            "copain|Doucement.",
            use,
            "narrateur|Ses doigts trouvent une craie perdue.",
            "enfant-m|Je la tiens !",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Une grotte de lumière s'ouvre, à eux.",
            "copain|Regarde, Amir.",
            "enfant-m|Elle est à nous.",
        )
    if t2 == 3 and t3 == 2:
        catch = {
            1: "narrateur|Le ruban soulève la poussière, tout doux.",
            2: "narrateur|La pince soulève un clic, tout bas.",
            3: "narrateur|Le tabouret soulève un coin, toc.",
        }[t1]
        return L(
            "enfant-m|On soulève un peu.",
            "copain|Moi aussi, je soulève.",
            "narrateur|Nino lève le bord de la table, tout haut.",
            "narrateur|Amir se glisse, pendant l'ouverture.",
            catch,
            "papa|Il est venu vers vous.",
            "copain|On l'a repris.",
            "enfant-m|Il brille encore.",
            "maman|Vos cheveux sentent la craie.",
        )
    nest = {
        1: "narrateur|Le ruban devient un nid, contre le bois.",
        2: "narrateur|La pince devient un nid, contre le bois.",
        3: "narrateur|Le tabouret devient un nid, contre le bois.",
    }[t1]
    return L(
        "enfant-m|Papa, écarte un peu ?",
        "papa|Je fais un chemin, tout doux.",
        "narrateur|Une chaise s'ouvre, comme une aile.",
        "narrateur|Amir rentre, Nino reste dehors.",
        nest,
        "copain|On se parle à travers.",
        "enfant-m|Oui.",
        "maman|Vous y arrivez, tous les deux.",
        "narrateur|Deux voix tiennent le même secret.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        keep = {
            1: "narrateur|Le ruban jaune pèse encore sur le crochet.",
            2: "narrateur|La pince à linge veille encore au bas.",
            3: "narrateur|Le petit tabouret veille encore au bas.",
        }[t1]
        return L(
            "narrateur|Aux patères, le soleil sent la laine mouillée.",
            "copain|Tu tenais le bas, moi j'accrochais.",
            "enfant-m|Tes bras l'ont fait monter.",
            "papa|Vous l'avez, enfin.",
            "maman|Le manteau dort sur le crochet, au calme.",
            keep,
            "enfant-m|On reste un peu, Nino.",
            "narrateur|Un rai jaune s'endort sur le linoléum.",
            "narrateur|La craie redevient douce, dans l'air.",
        )
    if t2 == 1 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} reste dans la paume d'Amir.",
            2: f"narrateur|{o['cap']} reste dans la paume d'Amir.",
            3: f"narrateur|{o['cap']} reste dans la paume d'Amir.",
        }[t1]
        return L(
            "narrateur|Sur le tabouret, deux têtes se calment.",
            "enfant-m|Nino, tu l'as vue glisser.",
            "copain|Oui, tout près de tes mains.",
            "papa|Toi en bas, lui au-dessus, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            keep,
            "copain|Je reste encore un peu.",
            "narrateur|Une goutte reste collée au manteau.",
            "narrateur|Le couloir sent encore la colle.",
        )
    if t2 == 1 and t3 == 3:
        keep = {
            1: "narrateur|Le ruban jaune retombe, tout léger.",
            2: "narrateur|La pince à linge retombe, tout léger.",
            3: "narrateur|Le petit tabouret retombe, tout léger.",
        }[t1]
        return L(
            "narrateur|Le manteau redescend, tout doux.",
            "copain|Il est tombé vers nous.",
            "enfant-m|On a pincé, tous les deux.",
            "maman|Il n'était plus trop coincé.",
            "papa|Le papier froisse encore, dans l'air.",
            keep,
            "enfant-m|On souffle dessus, tout calme.",
            "narrateur|Un rayon veille près des casiers.",
            "narrateur|La cloche se tait, au fond du préau.",
        )
    if t2 == 2 and t3 == 1:
        keep = {
            1: "narrateur|Le ruban jaune garde un brin de craie.",
            2: "narrateur|La pince à linge garde un brin de craie.",
            3: "narrateur|Le petit tabouret garde un brin de craie.",
        }[t1]
        return L(
            "narrateur|À la fenêtre, le soleil sent le carreau.",
            "enfant-m|Tu l'as fait pencher pour moi.",
            "copain|Tu tenais le bas.",
            "maman|Le verre sent encore le matin.",
            "papa|Le soleil est à vous, maintenant.",
            keep,
            "narrateur|Amir le pose contre la vitre.",
            "narrateur|Un rai traverse le papier, tout chaud.",
            "narrateur|Le loquet redevient calme, tout seul.",
        )
    if t2 == 2 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} pose une ombre au radiateur.",
            2: f"narrateur|{o['cap']} pose une ombre au radiateur.",
            3: f"narrateur|{o['cap']} pose une ombre au radiateur.",
        }[t1]
        return L(
            "narrateur|Sur le tabouret, deux paires de pieds se touchent.",
            "copain|Tu l'as posé, d'en bas.",
            "enfant-m|Tes bras l'ont fait descendre.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du tabouret sèche déjà.",
            keep,
            "copain|Il brille trop, Amir.",
            "enfant-m|C'est pour ça.",
            "narrateur|La vitre garde le jaune, tout proche.",
        )
    if t2 == 2 and t3 == 3:
        keep = {
            1: "narrateur|Amir pose le ruban au rebord.",
            2: "narrateur|Amir pose la pince au rebord.",
            3: "narrateur|Amir pose le tabouret au rebord.",
        }[t1]
        return L(
            "narrateur|Un peu de buée reste au carreau.",
            "enfant-m|On a tiré ensemble.",
            "copain|Sans trop monter.",
            "papa|Le rebord est resté à sa place.",
            "maman|Vos mains sentent encore la craie.",
            keep,
            "copain|Tu l'as eu, enfin.",
            "enfant-m|Il est à nous.",
            "narrateur|Le papier tremble un peu, puis s'endort.",
        )
    if t2 == 3 and t3 == 1:
        keep = {
            1: "narrateur|Le ruban jaune couvre encore leurs genoux.",
            2: "narrateur|La pince à linge fait un clic, tout bas.",
            3: "narrateur|Le petit tabouret tient encore leurs coudes.",
        }[t1]
        return L(
            "narrateur|Sous la table, la grotte sent le bois.",
            "copain|Tu es passé, moi je gardais.",
            "enfant-m|Tes épaules l'ont laissé ouvert.",
            "papa|Vous l'avez, enfin.",
            "maman|La craie dort sur le bord, au calme.",
            keep,
            "enfant-m|On reste un peu, Nino.",
            "narrateur|Un rai orange s'endort sous le bois.",
            "narrateur|La poussière redevient douce, autour.",
        )
    if t2 == 3 and t3 == 2:
        keep = {
            1: "narrateur|Le ruban jaune retombe, tout léger.",
            2: "narrateur|La pince à linge retombe, tout léger.",
            3: "narrateur|Le petit tabouret retombe, tout léger.",
        }[t1]
        return L(
            "narrateur|Le bord de table redescend, tout doux.",
            "copain|Il est tombé vers nous.",
            "enfant-m|On a soulevé, tous les deux.",
            "maman|Il n'était plus trop coincé.",
            "papa|Le papier froisse encore, dans l'air.",
            keep,
            "enfant-m|On souffle dessus, tout calme.",
            "narrateur|Un rayon veille près des chaises.",
            "narrateur|La cloche se tait, contre le préau.",
        )
    keep = {
        1: "narrateur|Le ruban jaune garde un brin de craie.",
        2: "narrateur|La pince à linge garde un brin de craie.",
        3: "narrateur|Le petit tabouret garde un brin de craie.",
    }[t1]
    return L(
        "narrateur|Deux têtes se parlent encore, à travers le bois.",
        "copain|On s'est parlé à travers.",
        "papa|La table vous a laissé la place.",
        "maman|Le secret tient encore, tout chaud.",
        keep,
        "enfant-m|Regarde-le, Nino, il brille.",
        "copain|Je le vois, d'ici.",
        "narrateur|Le jaune reste au chaud, sous le bois.",
        "narrateur|Une chaise redevient calme, tout seule.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La cloche de l'école tinte encore, toute légère.",
        "narrateur|Le couloir sent la craie et les manteaux mouillés.",
        "narrateur|Un rai jaune court sur le linoléum.",
        "papa|Tu as vu le soleil, Amir ?",
        "enfant-m|Il brille déjà, un peu.",
        "maman|Le papier attend près des casiers.",
        "narrateur|En ce moment, Amir tient son soleil en papier.",
        "narrateur|La colle est encore un peu froide, au milieu.",
        "enfant-m|Je veux le voir haut, ici.",
        "papa|Nino arrive, plus grand que toi.",
        "narrateur|Nino a les épaules jusqu'à la poignée.",
        "copain|On l'accroche ensemble ?",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu tiens le papier tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des casiers.",
        "narrateur|Le ruban, la pince, et le tabouret.",
        "maman|Tu prends quoi d'abord, Amir ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le ruban jaune", "la pince à linge", "le petit tabouret")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Amir a mis {o['lab']} {o['t1q']}.",
            "maman|C'est où, maintenant ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("les patères", "la fenêtre", "sous les tables")
        sons[p] = ""
        sons[f"{p}_T0002_P0000"] = ""

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            sons[sp] = ""
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "À l'école, le matin de la fête. Amir veut accrocher son soleil "
        "en papier, haut. Nino est plus grand. "
        "T1 = ruban jaune / pince à linge / petit tabouret (les trois partent). "
        "T2 = patères (trop hautes pour Amir) / fenêtre (poignée trop loin) / "
        "sous les tables (trop bas pour Nino). "
        "T3 = neuf résolutions (bras de Nino, tabouret d'Amir, pince ensemble ; "
        "poignée de Nino, tabouret du radiateur, rebord ; passage d'Amir, "
        "soulever la table, un dessous un dessus). "
        "La leçon (tailles, jouer) se vit dans les gestes, sans slogan. "
        "Fin : le soleil brille pour eux.",
        "N3 ≤ 16. Tom / Léa / Sami hors troupe → Amir + Nino (D16). "
        "Bac/toboggan/balançoires et ballon/seau/doudou jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-032 "
        "(école, pas chambre) et DIF-024 (pas pommier). Un merci de papa "
        "lié au geste (tenir le papier). Pas de « bon travail ». Audio non cuit.",
    )


if __name__ == "__main__":
    main()
