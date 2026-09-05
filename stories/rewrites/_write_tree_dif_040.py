#!/usr/bin/env python3
"""TREE-DIF-040 — Le lait de Nino et le petit veau (N3, DIF.BES.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-040"
N3 = 16
TITLE = "Le lait de Nino et le petit veau"
FIL = (
    "À la ferme, Nino veut porter le lait tiède au petit veau. "
    "Il prépare d'abord le seau, la brosse ou le torchon ; les trois partent. "
    "L'étable claque trop, le pré souffle trop, l'abreuvoir éclabousse trop. "
    "Neuf façons de laisser du temps. Le veau boit."
)
CHARS = "Nino, papa, maman"
SETTING = "ferme du village : étable, pré, abreuvoir"


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
        "plus de temps ou de calme",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
        "chambre",
        "marché",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
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
        "lab": "le seau",
        "ans": "seau",
        "acc": "seau | le seau | d'abord le seau | le lait",
        "retry": "Nino prend le seau d'abord.",
        "coda": "Le seau sèche près des bottes, encore tiède.",
        "hip": "Contre sa jambe, le zinc du seau cliquette.",
        "wait": "Pendant ce temps, le lait se tait dans le seau.",
        "use": "Un peu de lait tremble encore au bord.",
    },
    2: {
        "lab": "la brosse",
        "ans": "brosse",
        "acc": "brosse | la brosse | d'abord la brosse | les poils",
        "retry": "Nino prend la brosse d'abord.",
        "coda": "La brosse garde un poil clair, près du savon.",
        "hip": "Dans sa paume, les poils de la brosse piquent.",
        "wait": "Au creux du bras, la brosse reste sage.",
        "use": "Les poils frôlent l'air, tout doux, tout lents.",
    },
    3: {
        "lab": "le torchon",
        "ans": "torchon",
        "acc": "torchon | le torchon | d'abord le torchon | le linge",
        "retry": "Nino prend le torchon d'abord.",
        "coda": "Le torchon sèche sur le loquet, un pli au milieu.",
        "hip": "Au poignet, le torchon humide colle un peu.",
        "wait": "Plié, le torchon attend contre sa manche.",
        "use": "Le linge sent encore le lait, tout tiède.",
    },
}

T3_LABS = {
    1: ("attendre à la porte", "la paille", "tout bas"),
    2: ("la barrière", "poser le seau", "dans l'herbe"),
    3: ("l'eau se tait", "essuyer", "au bord"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord le seau, encore tiède.",
            "enfant-m|Le lait va au veau.",
            "maman|Tiens-le droit, tout doux.",
            "narrateur|Un peu de lait tremble, puis se tait.",
            "papa|La brosse aussi, près du sac.",
            "narrateur|Maman glisse le torchon contre le seau.",
            "narrateur|Seau, brosse et torchon avancent avec lui.",
            "enfant-m|J'arrive, petit veau.",
            "narrateur|Le zinc sent le lait, tout chaud.",
            "papa|Le seau d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino prend d'abord la brosse, les poils rèches.",
            "enfant-m|Je le brosserai après le lait.",
            "papa|Pas trop vite, encore.",
            "narrateur|Un brin de paille reste coincé dedans.",
            "maman|Le seau, ensuite, près de toi.",
            "narrateur|Papa pose le torchon contre les bottes.",
            "narrateur|Il emporte les trois, contre lui.",
            "enfant-m|Tes poils, tout doux.",
            "narrateur|La brosse frotte sa manche, un peu.",
            "maman|La brosse d'abord, elle est prête.",
        )
    return L(
        "narrateur|Nino prend d'abord le torchon, encore humide.",
        "enfant-m|Pour son mufle, après.",
        "maman|Plie-le, tout petit.",
        "narrateur|Le linge sent le lait et le savon.",
        "papa|Le seau et la brosse, avec vous.",
        "narrateur|Il les pose près des bottes.",
        "narrateur|Rien ne reste près du portail.",
        "enfant-m|Je t'essuierai, tout doux.",
        "narrateur|Un coin du torchon dépasse, déjà tiède.",
        "papa|Le torchon d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|Le seau tient contre sa hanche, encore tiède.",
            "enfant-m|Le lait va au veau.",
            "maman|La ferme vous attend.",
            "papa|On avance par où ?",
            "enfant-m|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|La brosse reste au creux du bras, sage.",
            "enfant-m|Après le lait, je le brosse.",
            "papa|Les poils sentent encore le foin.",
            "maman|Vos pieds, dans les bottes ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un brin de paille tremble, puis tombe.",
        )
    return L(
        "narrateur|Le torchon fait un nœud lâche, au poignet.",
        "enfant-m|Son mufle sera propre.",
        "maman|Le linge sent encore le savon.",
        "papa|On y va, tous les trois ?",
        "enfant-m|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le seau cliquette à chaque pas, tout bas.",
        2: "La brosse frotte sa manche, un peu rêche.",
        3: "Le torchon tape le poignet, tout doux.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|L'étable reste sombre, trop bruyante.",
        "narrateur|Plus loin, le pré souffle déjà.",
        "narrateur|Près de la pierre, l'eau claque.",
        "papa|Nino, vous partez où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le zinc tape une barre, trop fort.",
            2: "Les poils frôlent le fer, un bruit trop sec.",
            3: "Le torchon accroche un clou, puis lâche.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|L'étable sent le foin, trop sombre.",
            f"narrateur|{extra}",
            "enfant-m|Petit veau, j'ai du lait.",
            "narrateur|Une barre de fer claque encore, trop fort.",
            "narrateur|Le veau recule, le mufle contre sa mère.",
            "papa|Ça claque trop, ici.",
            "maman|Il a besoin de calme.",
            "enfant-m|On fait comment, alors ?",
            "papa|Tu trouves, Nino ?",
        )
    if t2 == 2:
        extra = {
            1: "Le vent penche le seau, le lait tremble.",
            2: "Les poils s'envolent un peu, trop légers.",
            3: "Le torchon claque comme un drap, trop fort.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Le pré sent l'herbe coupée, encore chaude.",
            f"narrateur|{extra}",
            "enfant-m|Le veau est trop loin !",
            "narrateur|Une mouche tourne, puis une autre.",
            "narrateur|Le veau lève la tête, puis recule.",
            "papa|Le vent n'a pas fini.",
            "maman|Il n'avance plus.",
            "enfant-m|On fait comment, alors ?",
            "maman|Tu trouves, Nino ?",
        )
    extra = {
        1: "Une goutte du seau tombe, trop bruyante.",
        2: "La brosse glisse sur la pierre, trop rêche.",
        3: "Le torchon s'alourdit, déjà trop mouillé.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|L'abreuvoir claque, trop plein, trop vif.",
        f"narrateur|{extra}",
        "enfant-m|L'eau fait trop de bruit.",
        "narrateur|Une flaque brille, trop large, trop froide.",
        "narrateur|Le veau recule d'un pas, les oreilles hautes.",
        "papa|Ça éclabousse trop, ici.",
        "maman|Il a besoin de temps.",
        "enfant-m|On fait comment, alors ?",
        "papa|Tu trouves, Nino ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'étable claque encore, trop sombre.",
            "papa|Attendre à la porte, la paille, ou tout bas ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le pré souffle encore, trop fort.",
            "maman|La barrière, poser le seau, ou dans l'herbe ?",
        )
    return L(
        "narrateur|L'eau claque encore, trop vive.",
        "papa|L'eau se tait, essuyer, ou au bord ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "Il pose le seau près du seuil, sans entrer.",
            2: "Il pose la brosse près du seuil, sans entrer.",
            3: "Il pose le torchon près du seuil, sans entrer.",
        }[t1]
        return L(
            "enfant-m|On attend à la porte.",
            f"narrateur|{wait}",
            "narrateur|Le fer se tait, une fois, puis plus.",
            "narrateur|Le veau sort deux oreilles, tout lent.",
            f"narrateur|{o['wait']}",
            "papa|Le fer s'est tu, maintenant.",
            "enfant-m|Tu peux venir.",
            "maman|Tu lui as laissé le temps.",
        )
    if t2 == 1 and t3 == 2:
        straw = {
            1: "Il glisse le seau dans la paille, tout bas.",
            2: "Il pose la brosse dans la paille, tout bas.",
            3: "Il étale le torchon dans la paille, tout bas.",
        }[t1]
        return L(
            "enfant-m|Dans la paille, on s'assoit.",
            f"narrateur|{straw}",
            "narrateur|Nino s'assoit, les genoux dans le foin.",
            "narrateur|Le veau avance d'un pas, puis d'un autre.",
            f"narrateur|{o['use']}",
            "papa|Tu as regardé d'abord.",
            "enfant-m|Viens, tout doux.",
            "maman|La paille a fait le calme.",
        )
    if t2 == 1 and t3 == 3:
        soft = {
            1: "Il parle au seau, tout bas, puis au veau.",
            2: "Il parle à la brosse, tout bas, puis au veau.",
            3: "Il parle au torchon, tout bas, puis au veau.",
        }[t1]
        return L(
            "enfant-m|Tout bas, c'est moi.",
            f"narrateur|{soft}",
            "narrateur|Nino répète, encore plus bas.",
            "narrateur|Le veau dresse les oreilles, sans reculer.",
            f"narrateur|{o['wait']}",
            "papa|Ta voix n'a pas claqué.",
            "enfant-m|Tu m'entends, maintenant.",
            "maman|Tu as parlé lentement.",
        )
    if t2 == 2 and t3 == 1:
        fence = {
            1: "Derrière le bois, le seau attend, tout droit.",
            2: "Derrière le bois, la brosse reste contre lui.",
            3: "Derrière le bois, le torchon ne claque plus.",
        }[t1]
        return L(
            "enfant-m|Derrière la barrière, d'abord.",
            "narrateur|Nino s'arrête au bois, sans courir.",
            f"narrateur|{fence}",
            "narrateur|Le vent passe, puis s'apaise un peu.",
            f"narrateur|{o['wait']}",
            "maman|Le pré retombe, comme un mur calme.",
            "enfant-m|Maintenant, tu me vois.",
            "papa|Tu as attendu le silence.",
        )
    if t2 == 2 and t3 == 2:
        down = {
            1: "Il pose le seau dans l'herbe, tout droit.",
            2: "Il pose la brosse, puis le seau, tout droit.",
            3: "Il pose le torchon sous le seau, tout droit.",
        }[t1]
        return L(
            "enfant-m|Je pose le seau, d'abord.",
            f"narrateur|{down}",
            "narrateur|Le lait fume, tout seul, dans l'herbe.",
            "narrateur|Le veau avance le mufle, tout lent.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas couru vers lui.",
            "enfant-m|C'est pour toi.",
            "maman|Tu as laissé le seau parler.",
        )
    if t2 == 2 and t3 == 3:
        grass = {
            1: "Dans l'herbe, le seau reste bas, près de lui.",
            2: "Dans l'herbe, la brosse reste contre son genou.",
            3: "Dans l'herbe, le torchon ne vole plus.",
        }[t1]
        return L(
            "enfant-m|Dans l'herbe, tout petit.",
            "narrateur|Nino s'accroupit, les mains dans l'herbe.",
            f"narrateur|{grass}",
            "narrateur|Le veau le voit plus bas, moins grand.",
            f"narrateur|{o['wait']}",
            "papa|Tu t'es fait petit, comme lui.",
            "enfant-m|Viens, je t'attends.",
            "maman|Tu as observé d'abord.",
        )
    if t2 == 3 and t3 == 1:
        hush = {
            1: "Il tient le seau, sans verser, jusqu'au silence.",
            2: "Il tient la brosse, sans bouger, jusqu'au silence.",
            3: "Il tient le torchon, sans essuyer, jusqu'au silence.",
        }[t1]
        return L(
            "enfant-m|On attend que l'eau se taise.",
            f"narrateur|{hush}",
            "narrateur|Les gouttes se calment, une, puis une autre.",
            "narrateur|Le veau baisse les oreilles, tout doux.",
            f"narrateur|{o['wait']}",
            "papa|L'eau n'éclabousse plus.",
            "enfant-m|Maintenant, tu peux boire.",
            "maman|Tu as attendu le calme.",
        )
    if t2 == 3 and t3 == 2:
        wipe = {
            1: "Il pose le seau, puis pousse l'eau du pied.",
            2: "Les poils de la brosse chassent un peu d'eau.",
            3: "Le torchon boit la flaque, tout large.",
        }[t1]
        return L(
            "enfant-m|J'essuie, d'abord.",
            f"narrateur|{wipe}",
            "narrateur|La pierre redevient mate, moins froide.",
            "narrateur|Le veau pose un sabot, puis l'autre.",
            f"narrateur|{o['use']}",
            "papa|La flaque n'a plus claqué.",
            "enfant-m|C'est sec, viens.",
            "maman|Tu as préparé le chemin.",
        )
    edge = {
        1: "Au bord, le seau reste droit, loin de l'eau.",
        2: "Au bord, la brosse reste sèche, loin de l'eau.",
        3: "Au bord, le torchon reste plié, loin de l'eau.",
    }[t1]
    return L(
        "enfant-m|Au bord, pas trop près.",
        f"narrateur|{edge}",
        "narrateur|Nino s'arrête sur la pierre sèche.",
        "narrateur|Le veau s'approche du lait, pas de l'eau.",
        f"narrateur|{o['wait']}",
        "papa|Tu n'as pas penché.",
        "enfant-m|Bois, tout doux.",
        "maman|Le bord était assez large.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le veau boit, le mufle dans le lait tiède.",
            "enfant-m|On a attendu à la porte.",
            "papa|Merci d'avoir laissé le fer se taire.",
            "maman|Rentrez, le pain est prêt.",
            f"narrateur|{coda}",
            "narrateur|Une paille blonde reste coincée au seuil.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Dans la paille, le veau finit le lait.",
            "enfant-m|On s'est assis, d'abord.",
            "papa|Tu as regardé avant d'appeler.",
            "maman|Essuie tes genoux, sur le paillasson.",
            f"narrateur|{coda}",
            "narrateur|Un brin de foin reste au pli du pantalon.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Tout bas, le veau a suivi la voix.",
            "enfant-m|Je n'ai pas parlé fort.",
            "papa|Ta voix n'a pas claqué.",
            "maman|Le fer est retombé, plus loin.",
            f"narrateur|{coda}",
            "narrateur|L'étable redevient sombre, tout calme.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Derrière la barrière, le veau a bu.",
            "enfant-m|On a attendu le vent.",
            "papa|Le silence vous a aidés.",
            "maman|L'herbe sent encore le soleil.",
            f"narrateur|{coda}",
            "narrateur|Une tige se recouche, tout lentement.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le seau vide fume encore, dans l'herbe.",
            "enfant-m|Je l'ai posé, d'abord.",
            "papa|Tu n'as pas couru vers lui.",
            "maman|Le lait a parlé tout seul.",
            f"narrateur|{coda}",
            "narrateur|Un cercle clair reste dans l'herbe couchée.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Dans l'herbe, le veau a trouvé Nino.",
            "enfant-m|Je me suis fait petit.",
            "papa|Tu t'es baissé, comme lui.",
            "maman|Vous rentrez, les bottes pleines d'herbe.",
            f"narrateur|{coda}",
            "narrateur|Une mouche s'en va, puis plus.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Quand l'eau s'est tue, le veau a bu.",
            "enfant-m|On a attendu les gouttes.",
            "papa|L'eau n'éclaboussait plus.",
            "maman|Vos manches sont encore fraîches.",
            f"narrateur|{coda}",
            "narrateur|Une dernière perle sèche sur la pierre.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La pierre mate a gardé deux sabots.",
            "enfant-m|J'ai essuyé, d'abord.",
            "papa|La flaque n'a plus claqué.",
            "maman|Tes mains sentent encore l'eau.",
            f"narrateur|{coda}",
            "narrateur|Un coin de pierre redevient clair, puis sèche.",
        )
    return L(
        "narrateur|Au bord, le veau a tout bu, tout calme.",
        "enfant-m|On n'est pas allés trop près.",
        "papa|Le bord était assez large.",
        "maman|Rentrez, le lait de la maison fume.",
        f"narrateur|{coda}",
        "narrateur|L'abreuvoir se tait, plus loin, tout seul.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le portail de bois sent encore la rosée.",
        "narrateur|Une paille blonde brille entre deux planches.",
        "narrateur|Ça sent le foin, tout chaud, tout sec.",
        "papa|Tu as vu la buée, Nino ?",
        "enfant-m|Le lait fume dans le seau.",
        "maman|Il est encore tiède, tout doux.",
        "narrateur|Derrière l'étable, un mufle rose cherche déjà.",
        "narrateur|En ce moment, Nino touche le bord du seau.",
        "enfant-m|Je veux le porter au petit veau.",
        "papa|Il recule si on va trop vite.",
        "maman|On prend les affaires, alors ?",
        "papa|Merci, tu as fermé le loquet.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des bottes.",
        "narrateur|Le seau, la brosse, et le torchon.",
        "maman|Tu prends quoi d'abord, Nino ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le seau", "la brosse", "le torchon")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nino a pris {o['lab']} d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'étable", "le pré", "l'abreuvoir")

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
        "Ferme, rosée, seau qui fume. Nino veut porter le lait tiède au petit veau. "
        "T1 = seau / brosse / torchon (les trois partent). "
        "T2 = étable trop bruyante / pré trop venteux / abreuvoir trop vif. "
        "T3 = neuf résolutions (porte, paille, tout bas ; barrière, poser le seau, "
        "dans l'herbe ; l'eau se tait, essuyer, au bord). "
        "La leçon (plus de temps, plus de calme) se vit : il attend, il observe, "
        "il répète tout bas. Fin : le veau boit.",
        "N3 ≤ 16. Slogan « Plus de temps ou de calme », Tom/Léa/Sami, "
        "bac/toboggan/balançoires, « bon travail », calque AUT-001 jetés. "
        "Un merci de papa (loquet fermé). chunk_id inchangés. "
        "Pas chambre, pas marché. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-040.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
