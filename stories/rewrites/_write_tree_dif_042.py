#!/usr/bin/env python3
"""TREE-DIF-042 — Le cacao de Nina, trop haut sur l'étagère (N3, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-042"
N3 = 16
TITLE = "Le cacao de Nina, trop haut sur l'étagère"
FIL = (
    "Dans la cuisine, après la pluie. Nina veut un chocolat chaud, pour deux. "
    "Victorino est plus grand. Ils emportent le bidon de cacao, le fouet et "
    "les deux tasses. À l'étagère, au frigo, sous la table : trois lieux, "
    "neuf façons. Le cacao fume pour eux."
)
CHARS = "Nina, Victorino, papa, maman"
SETTING = "cuisine : étagère, frigo, sous la table"


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
        "soleil en papier",
        "bac à sable",
        "toboggan",
        "balançoire",
        "sami",
        " léa",
        " lea",
        "tom ",
        "doudou",
        "ballon",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
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
        "lab": "le bidon de cacao",
        "cap": "Le bidon",
        "t1q": "contre la hanche",
        "t1acc": "hanche | la hanche | contre la hanche | sa hanche",
        "t1retry": "Le bidon est contre la hanche.",
    },
    2: {
        "lab": "le fouet",
        "cap": "Le fouet",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "Le fouet est dans la poche.",
    },
    3: {
        "lab": "les deux tasses",
        "cap": "Les tasses",
        "t1q": "sur le plateau",
        "t1acc": "plateau | le plateau | sur le plateau | le bois",
        "t1retry": "Les tasses sont sur le plateau.",
    },
}

T3_LABS = {
    1: ("les bras de Victorino", "le tabouret de Nina", "le torchon ensemble"),
    2: ("la poignée haute", "le bac du bas", "le tabouret à deux"),
    3: ("le passage de Nina", "écarter la chaise", "un dessous un dessus"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina serre le bidon de cacao, encore froid.",
            "enfant-f|Il sent le chocolat, tout près.",
            "maman|Garde-le contre ta hanche, tout droit.",
            "narrateur|Le métal glisse un peu, puis tient.",
            "papa|Le fouet, ensuite, dans la poche.",
            "narrateur|Victorino pose les deux tasses sur le plateau.",
            "narrateur|Tout voyage avec eux, vers l'évier.",
            "enfant-f|Victorino, tu viens près de l'eau ?",
            "copain|J'arrive, Nina.",
            "papa|Le bidon d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina prend le fouet, encore un peu rêche.",
            "enfant-f|Il gratte ma paume, tout doux.",
            "papa|Glisse-le dans ta poche, tout droit.",
            "narrateur|Un clic de métal, tout petit.",
            "maman|Le bidon, ensuite, contre la hanche.",
            "narrateur|Victorino pose les deux tasses sur le plateau.",
            "narrateur|Tout voyage avec eux, vers l'évier.",
            "enfant-f|Victorino va tout voir.",
            "narrateur|Ses épaules passent déjà au-dessus du bois.",
            "copain|Me voilà, Nina.",
            "enfant-f|On mélange le cacao, tous les deux ?",
            "maman|Le fouet d'abord, il est prêt.",
        )
    return L(
        "narrateur|Nina soulève les deux tasses, l'une petite.",
        "enfant-f|La grande est pour toi.",
        "maman|Pose-les sur le plateau, tout droit.",
        "narrateur|La porcelaine fait un petit choc.",
        "papa|Le bidon et le fouet, avec vous.",
        "narrateur|Elle les pose près de l'évier.",
        "narrateur|Rien ne reste près de la fenêtre.",
        "enfant-f|Victorino, vite !",
        "narrateur|Une ombre trop longue passe au frigo.",
        "copain|J'arrive près des tasses.",
        "enfant-f|Je te garde la grande.",
        "papa|Les tasses d'abord, elles sont prêtes.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La hanche porte le bidon, tout contre la robe.",
            "copain|Il est tout froid !",
            "enfant-f|Il va chauffer dans le lait.",
            "narrateur|Victorino a les genoux plus hauts que Nina.",
            "narrateur|Ses mains touchent déjà le bord du plan.",
            "maman|Il est plus grand, c'est tout.",
            "papa|On reste dans la cuisine ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La poche veille près du fouet.",
            "copain|J'entends le clic !",
            "enfant-f|Ne le sors pas encore.",
            "narrateur|Victorino se baisse, trop long, trop vite.",
            "narrateur|Une mèche saute au-dessus du pichet.",
            "papa|Ça sent déjà le cacao, sur le métal.",
            "maman|Vos mains, au-dessus du plateau ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|Le plateau cache encore les deux tasses.",
        "copain|La grande est à moi ?",
        "enfant-f|Oui, la petite est à moi.",
        "narrateur|Le pull de Victorino laisse ses poignets nus.",
        "narrateur|Nina, plus courte, tient le plateau des deux mains.",
        "maman|La cuisine est tiède, autour.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le bidon tape la hanche, tout bas.",
        2: "Le fouet frotte la poche, un peu rêche.",
        3: "Les tasses s'entrechoquent, tout doux.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|L'étagère reste trop haute, trop loin.",
        "narrateur|Le frigo garde son lait, trop froid.",
        "narrateur|Sous la table, l'ombre est basse.",
        "papa|Nina, vous mélangez où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Nina pose le bidon sur le plan, trop haut.",
            2: "narrateur|Nina pose le fouet sur le plan, trop haut.",
            3: "narrateur|Nina pose le plateau sur le plan, trop haut.",
        }[t1]
        mishap = {
            1: "narrateur|Un peu de poudre tombe, trop loin de ses yeux.",
            2: "narrateur|Les fils du fouet disparaissent derrière le bol.",
            3: "narrateur|Les tasses n'arrivent plus, trop basses.",
        }[t1]
        return L(
            lead,
            "narrateur|Le grand bol attend, trop loin pour Nina.",
            "enfant-f|Je ne vois plus le fond.",
            "copain|Moi si, il est tout brun.",
            "narrateur|Victorino se hausse, le menton au rebord.",
            mishap,
            f"narrateur|{o['cap']} reste au-dessus d'elle, trop loin.",
            "maman|Ses bras vont jusqu'au bol.",
            "papa|Toi tu vois le bois, lui la poudre.",
            "enfant-f|On mélange comment, alors ?",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Nina tape le bidon contre la porte, toc.",
            2: "narrateur|Nina tape le fouet contre la porte, toc.",
            3: "narrateur|Nina tape le plateau contre la porte, toc.",
        }[t1]
        mishap = {
            1: "narrateur|Le cacao reste trop bas, sous la poignée.",
            2: "narrateur|Le fouet n'accroche pas encore le loquet.",
            3: "narrateur|Les tasses n'ouvrent rien, trop basses.",
        }[t1]
        return L(
            lead,
            "enfant-f|Le lait est dedans, Victorino.",
            "copain|Je vois déjà le beurre, tout haut !",
            "narrateur|La poignée reste trop loin pour Nina.",
            mishap,
            "narrateur|Un souffle froid lève, puis retombe.",
            "maman|Ses bras vont jusqu'à la poignée.",
            "papa|Toi tu vois le bac, lui le beurre.",
            "enfant-f|On ouvre comment, alors ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: "narrateur|Nina glisse le bidon sous la table, tout bas.",
        2: "narrateur|Nina glisse le fouet sous la table, tout bas.",
        3: "narrateur|Nina glisse le plateau sous la table, tout bas.",
    }[t1]
    mishap = {
        1: "narrateur|Le cacao prend une miette, sur les carreaux.",
        2: "narrateur|Le fouet roule, puis s'arrête contre un pied.",
        3: "narrateur|Une tasse cliquette, trop près d'une chaise.",
    }[t1]
    return L(
        lead,
        "enfant-f|On goûte ici, comme une grotte.",
        "copain|J'entre, trop large !",
        "narrateur|Ses épaules butent contre le bois de la table.",
        mishap,
        f"narrateur|{o['cap']} attend au bord, un peu seul.",
        "maman|Il a les épaules trop larges, c'est tout.",
        "papa|Toi tu passes, lui pas encore.",
        "copain|On goûte comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'étagère attend encore, trop haute.",
            "papa|Les bras, le tabouret, ou le torchon ensemble ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La poignée attend encore, trop loin.",
            "maman|La poignée, le bac, ou le tabouret ?",
        )
    return L(
        "narrateur|L'ombre sous la table attend encore.",
        "papa|Le passage, écarter, ou un dessous un dessus ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Nina tend le bidon, bras tout courts.",
            2: "narrateur|Nina tend le fouet, bras tout courts.",
            3: "narrateur|Nina pousse le plateau, tout près.",
        }[t1]
        return L(
            "enfant-f|Tu mélanges, toi, tu vois le fond.",
            "narrateur|Victorino tourne dans le bol, assez haut.",
            "copain|Ça devient brun, tout doux.",
            use,
            "narrateur|Nina verse le lait, d'en bas, tout lent.",
            "enfant-f|Je tiens le pichet !",
            "papa|Tes bras allaient assez loin.",
            "narrateur|La poudre s'ouvre, à leur hauteur.",
            "copain|Goûte, Nina.",
            "enfant-f|Il est à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le bidon attend au bord, plein d'ombre.",
            2: "narrateur|Le fouet attend au bord, un peu rêche.",
            3: "narrateur|Le plateau attend au bord, un peu chaud.",
        }[t1]
        return L(
            "enfant-f|Je monte, tout doux.",
            "papa|Tiens le bois, Nina.",
            "narrateur|Nina se hausse, le nez au bord du bol.",
            "copain|Moi je verse le lait, tout près.",
            "narrateur|Victorino tient le pichet, au-dessus.",
            "narrateur|La poudre glisse vers le fond.",
            "copain|Tu vois, maintenant.",
            "maman|Vous le partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        catch = {
            1: "narrateur|Le bidon glisse avec le torchon, tout doux.",
            2: "narrateur|Le fouet glisse avec le torchon, clic.",
            3: "narrateur|Le plateau glisse avec le linge, toc.",
        }[t1]
        return L(
            "enfant-f|On tire le bol, tout doux.",
            "copain|Moi aussi, je tire.",
            "narrateur|Victorino enroule un torchon, tout haut.",
            "narrateur|Nina tire l'autre bout, plus bas.",
            catch,
            "papa|Le bol est venu vers vous.",
            "copain|On le tient.",
            "enfant-f|Il fume encore.",
            "maman|Vos cheveux sentent le linge chaud.",
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Victorino pose le bidon contre la porte.",
            2: "narrateur|Victorino pose le fouet contre la porte.",
            3: "narrateur|Victorino pose le plateau contre le joint.",
        }[t1]
        return L(
            "copain|Je me hausse encore.",
            "enfant-f|Je tiens les tasses, d'en bas.",
            "narrateur|Les doigts de Victorino touchent la poignée.",
            "copain|Elle bouge !",
            "narrateur|La bouteille de lait penche, puis avance.",
            carry,
            "papa|Tes doigts allaient assez loin.",
            "maman|Nina tenait bien le bas.",
            "copain|Le lait est à nous.",
        )
    if t2 == 2 and t3 == 2:
        up = {
            1: "narrateur|Nina pose le bidon près du bac.",
            2: "narrateur|Nina pose le fouet près du bac.",
            3: "narrateur|Nina pousse le plateau, tout près.",
        }[t1]
        return L(
            "enfant-f|J'ouvre le bac du bas ?",
            "copain|Oui, tout doux.",
            up,
            "narrateur|Papa tient la porte, tout ferme.",
            "narrateur|Nina tire le bac, Victorino veille.",
            "enfant-f|Le lait est là !",
            "copain|Il est tout froid.",
            "maman|Vous avez regardé ensemble.",
            "papa|Le bac est resté doux.",
        )
    if t2 == 2 and t3 == 3:
        two = {
            1: "narrateur|Victorino tend le bidon, bras tout longs.",
            2: "narrateur|Victorino tend le fouet, bras tout longs.",
            3: "narrateur|Victorino pousse le plateau, tout près.",
        }[t1]
        return L(
            "enfant-f|Reste en haut, Victorino.",
            "copain|Je tends, d'ici.",
            two,
            "narrateur|Victorino fait basculer le loquet, tout doux.",
            "narrateur|Le tabouret prend Nina, puis lui.",
            "enfant-f|Je tiens la bouteille !",
            "papa|Chacun a fait sa part.",
            "copain|Elle sent le froid.",
            "maman|Vos bras n'avaient pas la même longueur.",
        )
    if t2 == 3 and t3 == 1:
        use = {
            1: "narrateur|Nina pousse le bidon sous la table.",
            2: "narrateur|Nina glisse le fouet sous le bois.",
            3: "narrateur|Nina pousse le plateau sous le bord.",
        }[t1]
        return L(
            "enfant-f|Je passe, toi tu restes.",
            "narrateur|Nina rampe, tout petite, sous la table.",
            "copain|Je fouette ici, dehors.",
            use,
            "narrateur|Ses doigts trouvent la petite tasse.",
            "enfant-f|Je la tiens !",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Une grotte de vapeur s'ouvre, à eux.",
            "copain|Je te verse, d'ici.",
            "enfant-f|Elle est à nous.",
        )
    if t2 == 3 and t3 == 2:
        catch = {
            1: "narrateur|Le bidon avance, tout doux, vers le jour.",
            2: "narrateur|Le fouet avance, un clic, vers le jour.",
            3: "narrateur|Le plateau avance, toc, vers le jour.",
        }[t1]
        return L(
            "enfant-f|On écarte la chaise.",
            "copain|Moi aussi, j'écarte.",
            "narrateur|Victorino tire la chaise, tout haut.",
            "narrateur|Nina se glisse, pendant l'ouverture.",
            catch,
            "papa|La place est venue vers vous.",
            "copain|Je rentre, de côté.",
            "enfant-f|On y est, tous les deux.",
            "maman|Vos cheveux sentent le bois chaud.",
        )
    nest = {
        1: "narrateur|Le bidon devient un nid, contre le bois.",
        2: "narrateur|Le fouet devient un nid, contre le bois.",
        3: "narrateur|Le plateau devient un nid, contre le bois.",
    }[t1]
    return L(
        "enfant-f|Papa, écarte un peu ?",
        "papa|Je fais un chemin, tout doux.",
        "narrateur|Une chaise s'ouvre, comme une aile.",
        "narrateur|Nina rentre, Victorino reste dehors.",
        nest,
        "copain|On trinque à travers ?",
        "enfant-f|Oui, petite tasse, grande tasse.",
        "maman|Vous y arrivez, tous les deux.",
        "narrateur|Deux voix tiennent le même secret.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        keep = {
            1: "narrateur|Le bidon de cacao pèse encore sur le rebord.",
            2: "narrateur|Le fouet veille encore au bas, un peu brun.",
            3: "narrateur|Le plateau veille encore au bas, deux tasses.",
        }[t1]
        return L(
            "narrateur|À l'étagère, le cacao sent le citron.",
            "copain|Tu versais, moi je tournais.",
            "enfant-f|Tes bras ont vu le fond.",
            "papa|Vous l'avez, enfin.",
            "maman|Le bol dort sur le bois, au calme.",
            keep,
            "enfant-f|On reste un peu, Victorino.",
            "narrateur|Un rai brun s'endort sur les carreaux.",
            "narrateur|La buée redevient douce, dans l'air.",
        )
    if t2 == 1 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} reste dans la paume de Nina.",
            2: f"narrateur|{o['cap']} reste dans la paume de Nina.",
            3: f"narrateur|{o['cap']} reste dans la paume de Nina.",
        }[t1]
        return L(
            "narrateur|Sur le tabouret, deux têtes se calment.",
            "enfant-f|J'ai vu le fond, moi aussi.",
            "copain|Oui, tu étais assez haute.",
            "papa|Toi en bas, lui au-dessus, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            keep,
            "copain|Je reste encore un peu.",
            "narrateur|Une goutte reste collée au bol.",
            "narrateur|L'évier sent encore le cacao.",
        )
    if t2 == 1 and t3 == 3:
        keep = {
            1: "narrateur|Le bidon de cacao retombe, tout léger.",
            2: "narrateur|Le fouet retombe, tout léger.",
            3: "narrateur|Le plateau retombe, tout léger.",
        }[t1]
        return L(
            "narrateur|Le torchon redescend, tout doux.",
            "copain|Le bol est venu vers nous.",
            "enfant-f|On a tiré, tous les deux.",
            "maman|Il n'était plus trop haut.",
            "papa|La poudre danse encore, dans l'air.",
            keep,
            "enfant-f|On souffle dessus, tout calme.",
            "narrateur|Un rayon veille près des bols.",
            "narrateur|Le radiateur se tait, au fond.",
        )
    if t2 == 2 and t3 == 1:
        keep = {
            1: "narrateur|Le bidon de cacao garde un brin de froid.",
            2: "narrateur|Le fouet garde un brin de froid.",
            3: "narrateur|Le plateau garde un brin de froid.",
        }[t1]
        return L(
            "narrateur|Au frigo, le cacao sent le lait.",
            "enfant-f|Tu as ouvert, tout haut.",
            "copain|Tu tenais les tasses.",
            "maman|Le verre sent encore le matin.",
            "papa|Le cacao est à vous, maintenant.",
            keep,
            "narrateur|Nina verse dans la tasse petite.",
            "narrateur|Un rai traverse la vapeur, tout chaud.",
            "narrateur|Le loquet redevient calme, tout seul.",
        )
    if t2 == 2 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} pose une ombre au bac.",
            2: f"narrateur|{o['cap']} pose une ombre au bac.",
            3: f"narrateur|{o['cap']} pose une ombre au bac.",
        }[t1]
        return L(
            "narrateur|Près du bac, deux paires de pieds se touchent.",
            "copain|Tu l'as trouvé, d'en bas.",
            "enfant-f|Tes yeux gardaient la porte.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du bac sèche déjà.",
            keep,
            "copain|Il fume trop, Nina.",
            "enfant-f|C'est pour ça.",
            "narrateur|La porte garde le froid, tout proche.",
        )
    if t2 == 2 and t3 == 3:
        keep = {
            1: "narrateur|Nina pose le bidon au rebord.",
            2: "narrateur|Nina pose le fouet au rebord.",
            3: "narrateur|Nina pose le plateau au rebord.",
        }[t1]
        return L(
            "narrateur|Un peu de buée reste au frigo.",
            "enfant-f|On a ouvert ensemble.",
            "copain|Sans trop monter.",
            "papa|Le tabouret est resté à sa place.",
            "maman|Vos mains sentent encore le lait.",
            keep,
            "copain|Tu l'as eu, enfin.",
            "enfant-f|Il est à nous.",
            "narrateur|La vapeur tremble un peu, puis s'endort.",
        )
    if t2 == 3 and t3 == 1:
        keep = {
            1: "narrateur|Le bidon de cacao couvre encore leurs genoux.",
            2: "narrateur|Le fouet fait un clic, tout bas.",
            3: "narrateur|Le plateau tient encore leurs coudes.",
        }[t1]
        return L(
            "narrateur|Sous la table, la grotte sent le bois.",
            "copain|Tu es passée, moi je fouettais.",
            "enfant-f|Tes épaules l'ont laissé ouvert.",
            "papa|Vous l'avez, enfin.",
            "maman|La petite tasse dort sur le bord, au calme.",
            keep,
            "enfant-f|On reste un peu, Victorino.",
            "narrateur|Un rai brun s'endort sous le bois.",
            "narrateur|La miette redevient douce, autour.",
        )
    if t2 == 3 and t3 == 2:
        keep = {
            1: "narrateur|Le bidon de cacao retombe, tout léger.",
            2: "narrateur|Le fouet retombe, tout léger.",
            3: "narrateur|Le plateau retombe, tout léger.",
        }[t1]
        return L(
            "narrateur|Le bord de table redescend, tout doux.",
            "copain|Je suis rentré de côté.",
            "enfant-f|On a écarté, tous les deux.",
            "maman|Il n'était plus trop coincé.",
            "papa|La poudre danse encore, dans l'air.",
            keep,
            "enfant-f|On souffle dessus, tout calme.",
            "narrateur|Un rayon veille près des chaises.",
            "narrateur|Le radiateur se tait, contre le mur.",
        )
    keep = {
        1: "narrateur|Le bidon de cacao garde un brin de lait.",
        2: "narrateur|Le fouet garde un brin de lait.",
        3: "narrateur|Le plateau garde un brin de lait.",
    }[t1]
    return L(
        "narrateur|Deux tasses se parlent encore, à travers le bois.",
        "copain|On a trinqué à travers.",
        "papa|La table vous a laissé la place.",
        "maman|Le secret tient encore, tout chaud.",
        keep,
        "enfant-f|Regarde-le, Victorino, il fume.",
        "copain|Je le vois, d'ici.",
        "narrateur|Le brun reste au chaud, sous le bois.",
        "narrateur|Une chaise redevient calme, tout seule.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La fenêtre de la cuisine a encore de la buée.",
        "narrateur|Un citron jaune dort sur le rebord.",
        "narrateur|Le radiateur fait tic, tout doux.",
        "papa|Tu as vu le pichet, Nina ?",
        "enfant-f|Il est déjà tiède.",
        "maman|Le lait attend près de l'évier.",
        "narrateur|En ce moment, Nina touche le bois de la table.",
        "narrateur|Ses doigts sentent encore la pluie, dehors.",
        "enfant-f|Je veux du cacao, pour deux.",
        "papa|Victorino arrive, plus grand que toi.",
        "narrateur|Ses épaules montent déjà jusqu'au frigo.",
        "copain|On le mélange ensemble ?",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu as posé le pichet tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près de l'évier.",
        "narrateur|Le bidon, le fouet, et les tasses.",
        "maman|Tu prends quoi d'abord, Nina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bidon de cacao", "le fouet", "les deux tasses")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nina a mis {o['lab']} {o['t1q']}.",
            "maman|C'est où, maintenant ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'étagère", "le frigo", "sous la table")
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
        "Dans la cuisine, après la pluie. Nina veut un chocolat chaud, "
        "pour deux. Victorino est plus grand. "
        "T1 = bidon de cacao / fouet / deux tasses (les trois partent). "
        "T2 = étagère (trop haute pour Nina) / frigo (poignée trop loin) / "
        "sous la table (trop bas pour Victorino). "
        "T3 = neuf résolutions (bras de Victorino, tabouret de Nina, torchon ; "
        "poignée haute, bac du bas, tabouret à deux ; passage de Nina, "
        "écarter la chaise, un dessous un dessus). "
        "La leçon (tailles, jouer) se vit dans les gestes, sans slogan. "
        "Fin : le cacao fume pour eux.",
        "N3 ≤ 16. Tom / Léa / Sami hors troupe → Nina + Victorino (D16). "
        "Bac/toboggan/balançoires et ballon/seau/doudou jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-014 "
        "(pomme), DIF-022 (marelle), DIF-032 (cabane), DIF-034 (soleil). "
        "Un merci de papa lié au geste (poser le pichet). Pas de « bon travail ». "
        "Audio non cuit.",
    )


if __name__ == "__main__":
    main()
