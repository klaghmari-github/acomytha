#!/usr/bin/env python3
"""TREE-DIF-049 — Les poissons de papier de Sarah, sur le tapis (N1, DIF.BES.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-049"
N1 = LIMITS["N1"]
TITLE = "Les poissons de papier de Sarah, sur le tapis"
FIL = (
    "Dehors la mare a trop de vent. Sarah veut une pêche sur le tapis du salon, "
    "pour Nino. Elle prend d'abord le bâton, le seau bleu ou le poisson jaune ; "
    "les trois viennent, et le voyage change : canapé, table, tapis tiède. "
    "Nino tourne la boîte à musique, conduit son camion, ou cherche un chausson. "
    "Elle propose, et elle accepte oui, non, ou une autre idée. "
    "Les poissons jaunes finissent dans le seau."
)
CHARS = "Sarah, Nino, papa, maman"
SETTING = "salon : canapé, table, tapis près du radiateur"


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
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "inviter sans forcer",
        "accepter plusieurs",
        "kenzo",
        "lina",
        "coussin",
        "le fort",
        "tomate",
        "panier rouge",
        "figuier",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
        "wagon",
        "sifflet",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob or "nino" not in blob:
        raise SystemExit(f"{SID}: troupe Sarah/Nino absente")
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


T1 = {
    1: {
        "lab": "le bâton",
        "ans": "bâton",
        "acc": "bâton | le bâton | d'abord le bâton | le bois",
        "retry": "Sarah a pris le bâton.",
        "coda": "La ficelle garde encore un peu de savon.",
    },
    2: {
        "lab": "le seau bleu",
        "ans": "seau",
        "acc": "seau | le seau | le seau bleu | d'abord le seau",
        "retry": "Sarah a pris le seau.",
        "coda": "Le seau bleu garde un poisson plat.",
    },
    3: {
        "lab": "le poisson jaune",
        "ans": "poisson",
        "acc": "poisson | le poisson | un poisson | le papier",
        "retry": "Sarah a coupé un poisson.",
        "coda": "Le tapis garde un fil, tout calme.",
    },
}

T3_LABS = {
    1: ("attendre la chanson", "parler tout bas", "s'asseoir à côté"),
    2: ("laisser garer", "un poisson dedans", "garder le seau"),
    3: ("aider un peu", "un tout petit regard", "proposer plus tard"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah prend d'abord le bâton.",
            "enfant-f|Il est un peu rêche.",
            "maman|Tiens-le, tout doux.",
            "narrateur|Puis elle grimpe sur le canapé.",
            "papa|La ficelle descend, comme un pont.",
            "narrateur|Le seau attend en bas, déjà.",
            "narrateur|Le poisson jaune reste près d'elle.",
            "enfant-f|Nino va pêcher, d'en haut.",
            "papa|Tu l'invites, quand tu le trouves ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah prend d'abord le seau bleu.",
            "enfant-f|Il sent encore l'eau.",
            "papa|Pose-le sur la table, tout doux.",
            "narrateur|Un petit toc sonne contre le bois.",
            "maman|Le bâton aussi, près de toi.",
            "narrateur|Elle pose le poisson à côté.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Nino va vider le seau.",
            "maman|Tu lui proposes, tout calme ?",
            "enfant-f|Oui, maman.",
        )
    return L(
        "narrateur|Sarah prend d'abord le poisson jaune.",
        "enfant-f|Il a un œil rond.",
        "maman|Tiens-le à plat, tout doux.",
        "narrateur|Puis elle s'allonge sur le tapis.",
        "papa|Le radiateur chante, tout près.",
        "narrateur|Le bâton et le seau la suivent.",
        "narrateur|Rien ne reste sur la table.",
        "enfant-f|Nino va voir ma mare.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-f|Oui.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah tient le bois, déjà.",
            "maman|Elle a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le plastique bleu est dans ses mains.",
            "papa|Elle a pris quoi, d'abord ?",
        )
    return L(
        "narrateur|Le papier jaune tremble encore.",
        "maman|Elle a coupé quoi ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|Le bâton.",
            "maman|Oui.",
            "narrateur|La ficelle pend, tout calme.",
            "narrateur|Le canapé fait une rive haute.",
            "enfant-f|Nino est dans le salon.",
            "papa|Je l'entends, plus loin.",
            "maman|Vous allez le trouver.",
            "enfant-f|Je lui propose la mare.",
        )
    if t1 == 2:
        return L(
            "enfant-f|Le seau.",
            "papa|Oui.",
            "narrateur|Le plastique bleu tient le bois.",
            "narrateur|Une ombre ronde dort dessus.",
            "enfant-f|Nino est dans le salon.",
            "maman|Je l'entends, plus loin.",
            "papa|Le bois tient bien, maintenant.",
            "enfant-f|Je lui propose le seau.",
        )
    return L(
        "enfant-f|Le poisson.",
        "maman|Oui.",
        "narrateur|Un peu d'air lève le papier.",
        "narrateur|Le radiateur chante, tout près.",
        "enfant-f|Nino est dans le salon.",
        "papa|Je l'entends, plus loin.",
        "maman|Le tapis reste sous toi.",
        "enfant-f|Je lui propose la mare.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Nino est dans le salon, déjà.",
        "narrateur|La boîte à musique tourne, tout près.",
        "narrateur|Un camion roule, plus loin.",
        "narrateur|Des chaussons attendent, au bord.",
        "papa|On va vers quoi, Sarah ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        if t1 == 1:
            return L(
                "narrateur|Sarah redescend du canapé, tout doux.",
                "narrateur|Nino tourne la boîte, tout absorbé.",
                "enfant-f|Nino, la mare est prête.",
                "narrateur|Il ne lève pas encore les yeux.",
                "copain|Ma chanson n'est pas finie.",
                "enfant-f|Tu viens pêcher, d'en haut ?",
                "copain|J'ai pas fini.",
                "maman|Il écoute encore, tout concentré.",
                "papa|Tu proposes comment, Sarah ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Sarah pose le seau près de la boîte.",
                "narrateur|Nino tient encore la clé.",
                "enfant-f|Nino, le seau est bleu.",
                "narrateur|Une note tinte, puis une autre.",
                "copain|Ma chanson n'est pas finie.",
                "enfant-f|Tu viens à la table ?",
                "copain|J'ai pas fini.",
                "papa|Il reste dans sa chanson.",
                "maman|Tu proposes comment, Sarah ?",
            )
        return L(
            "narrateur|Le poisson jaune tremble près du tapis.",
            "narrateur|Nino tourne la clé, tout bas.",
            "enfant-f|Nino, ma mare est tiède.",
            "narrateur|Le radiateur chante avec la boîte.",
            "copain|Ma chanson n'est pas finie.",
            "enfant-f|Tu viens t'allonger ?",
            "copain|J'ai pas fini.",
            "maman|La boîte tient encore sa note.",
            "papa|Tu proposes comment, Sarah ?",
        )
    if t2 == 2:
        if t1 == 1:
            return L(
                "narrateur|Un camion jaune passe sous le canapé.",
                "narrateur|Nino le pousse, tout concentré.",
                "enfant-f|Nino, on pêche d'en haut.",
                "copain|Mon camion n'est pas garé.",
                "enfant-f|Tu viens sur le canapé ?",
                "copain|Après, peut-être.",
                "narrateur|Les roues font un petit rrr.",
                "maman|Il conduit encore, tout calme.",
                "papa|Tu proposes comment, Sarah ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Nino a déjà son camion, à la table.",
                "narrateur|Le seau bleu attend, tout près.",
                "enfant-f|Nino, tu veux un poisson ?",
                "copain|Mon camion n'est pas garé.",
                "enfant-f|On charge le seau ?",
                "copain|Pas maintenant.",
                "narrateur|Deux jeux, trop loin l'un de l'autre.",
                "papa|Il n'a pas fini, Sarah.",
                "maman|Tu proposes comment, alors ?",
            )
        return L(
            "narrateur|Nino pousse le camion sur le tapis.",
            "narrateur|Une roue passe sur la ficelle.",
            "enfant-f|Nino, la mare est tiède.",
            "copain|Mon camion n'est pas garé.",
            "enfant-f|Tu t'allonges avec moi ?",
            "copain|Après, peut-être.",
            "narrateur|Le poisson tremble, tout plat.",
            "maman|Il conduit encore, tout concentré.",
            "papa|Tu proposes comment, Sarah ?",
        )
    if t1 == 1:
        return L(
            "narrateur|Nino s'assoit au bord du tapis.",
            "copain|J'ai un chausson, Sarah.",
            "enfant-f|On pêche d'en haut, après.",
            "narrateur|Il cherche l'autre, sous le canapé.",
            "enfant-f|Tu viens sur le canapé ?",
            "copain|Quand j'ai mes chaussons, d'abord.",
            "papa|Il enfile encore, tout calme.",
            "maman|L'autre chausson n'est pas là.",
            "papa|Tu proposes comment, Sarah ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino quitte la table, un pied nu.",
            "copain|J'ai un chausson, Sarah.",
            "enfant-f|Le seau est encore vide.",
            "narrateur|Il ne s'assoit plus.",
            "enfant-f|Tu reviens au seau ?",
            "copain|Quand j'ai mes chaussons, d'abord.",
            "maman|Il cherche encore, tout tendu.",
            "papa|L'autre chausson n'est pas là.",
            "maman|Tu proposes comment, Sarah ?",
        )
    return L(
        "narrateur|Nino se tient près du radiateur.",
        "copain|J'ai un chausson, Sarah.",
        "enfant-f|Ma mare est déjà tiède.",
        "narrateur|Il serre le chausson, tout calme.",
        "enfant-f|Tu t'allonges avec moi ?",
        "copain|Quand j'ai mes chaussons, d'abord.",
        "papa|Il cherche encore, tout près.",
        "maman|L'autre chausson n'est pas là.",
        "papa|Tu proposes comment, Sarah ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La boîte à musique tourne encore.",
            "papa|Attendre, parler tout bas, ou s'asseoir ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le camion n'est pas rangé.",
            "maman|Laisser garer, un poisson, ou garder ?",
        )
    return L(
        "narrateur|Un chausson n'est pas chaussé.",
        "papa|Aider, un petit regard, ou plus tard ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|La ficelle pend, sans bouger.",
            2: "narrateur|Le seau bleu attend, sans bouger.",
            3: "narrateur|Le poisson jaune attend, tout plat.",
        }[t1]
        return L(
            "enfant-f|J'attends un peu.",
            "copain|Merci, Sarah.",
            "narrateur|La boîte tourne sa dernière note.",
            wait,
            "narrateur|Nino pose la clé, enfin.",
            "copain|Ma chanson est finie, maintenant.",
            "enfant-f|Tu viens, alors ?",
            "copain|Oui.",
            "papa|Tu as laissé sa chanson finir.",
        )
    if t2 == 1 and t3 == 2:
        near = {
            1: "narrateur|Elle parle tout contre le canapé.",
            2: "narrateur|Elle parle tout contre la table.",
            3: "narrateur|Elle parle tout contre le tapis.",
        }[t1]
        return L(
            "enfant-f|Nino, je te propose la mare.",
            near,
            "narrateur|Sa voix reste tout bas, près de lui.",
            "copain|J'ai entendu, Sarah.",
            "enfant-f|Tu peux dire non.",
            "copain|Oui, je viens.",
            "narrateur|Il ferme la boîte, tout doux.",
            "papa|Ta voix est restée tout bas.",
            "maman|Il a choisi de lui-même.",
        )
    if t2 == 1 and t3 == 3:
        sit = {
            1: "narrateur|Sarah s'assoit au pied du canapé.",
            2: "narrateur|Sarah s'assoit près de la table.",
            3: "narrateur|Sarah s'assoit près du radiateur.",
        }[t1]
        return L(
            "enfant-f|Je m'assois à côté.",
            sit,
            "narrateur|Elle ne touche pas la clé.",
            "copain|Tu écoutes, toi aussi ?",
            "enfant-f|Oui, avec toi.",
            "narrateur|Deux oreilles, maintenant, sur la boîte.",
            "copain|Après, on va pêcher.",
            "papa|Tu es restée près de lui.",
            "maman|Il a proposé la suite.",
        )
    if t2 == 2 and t3 == 1:
        wait = {
            1: "narrateur|Le canapé garde sa rive, encore.",
            2: "narrateur|Le seau bleu garde son bois.",
            3: "narrateur|Le poisson jaune garde le tapis.",
        }[t1]
        return L(
            "enfant-f|J'attends qu'il gare.",
            "copain|Merci, Sarah.",
            wait,
            "narrateur|Le camion s'arrête, pile.",
            "copain|C'est garé, maintenant.",
            "enfant-f|Tu viens, alors ?",
            "copain|Oui.",
            "papa|Tu as laissé son camion finir.",
            "maman|Il a dit oui, à son heure.",
        )
    if t2 == 2 and t3 == 2:
        offer = {
            1: "narrateur|Elle tend le poisson, sous le canapé.",
            2: "narrateur|Elle tend le poisson, sur la table.",
            3: "narrateur|Elle tend le poisson, sur le tapis.",
        }[t1]
        return L(
            "enfant-f|Nino, un poisson dans le camion ?",
            offer,
            "copain|Un tout petit, alors.",
            "enfant-f|D'accord.",
            "narrateur|Le papier glisse, tout doux.",
            "copain|Il est tout plat, dedans.",
            "enfant-f|On est deux, maintenant.",
            "papa|Le poisson est resté dans sa main.",
            "maman|Il a pris ce qu'il voulait.",
        )
    if t2 == 2 and t3 == 3:
        side = {
            1: "narrateur|Le seau reste au pied du canapé.",
            2: "narrateur|Le seau reste sur la table.",
            3: "narrateur|Le seau reste près du radiateur.",
        }[t1]
        return L(
            "copain|Pas de poisson, Sarah.",
            "enfant-f|D'accord.",
            "enfant-f|Je garde le seau, alors.",
            side,
            "narrateur|Elle pêche de son côté, tout calme.",
            "copain|Tu peux parler, d'ici.",
            "enfant-f|Je reste près de toi.",
            "papa|Tu as gardé ton seau.",
            "maman|Vous êtes encore ensemble.",
        )
    if t2 == 3 and t3 == 1:
        help_ = {
            1: "narrateur|Elle cherche sous le canapé, tout doux.",
            2: "narrateur|Elle cherche sous la table, tout doux.",
            3: "narrateur|Elle cherche près du radiateur, tout doux.",
        }[t1]
        return L(
            "enfant-f|J'aide un peu.",
            help_,
            "narrateur|Le second chausson apparaît, enfin.",
            "copain|Tu l'as vu, toi aussi ?",
            "enfant-f|Oui, sous le bord.",
            "narrateur|Deux pieds, maintenant, tout chauds.",
            "copain|Il était là !",
            "papa|Tu as aidé à son heure.",
            "maman|Vous l'avez eu, tous les deux.",
        )
    if t2 == 3 and t3 == 2:
        look = {
            1: "narrateur|Ils regardent la rive du canapé.",
            2: "narrateur|Ils regardent le seau, une seconde.",
            3: "narrateur|Ils regardent la mare du tapis.",
        }[t1]
        return L(
            "enfant-f|Un tout petit regard, Nino ?",
            "copain|Très petit, alors.",
            "enfant-f|D'accord.",
            look,
            "narrateur|Un poisson jaune brille, une seconde.",
            "copain|Il est joli, Sarah.",
            "narrateur|Puis Nino reprend le chausson.",
            "papa|Tu as proposé court, juste assez.",
            "maman|Il a vu, puis choisi.",
        )
    later = {
        1: "narrateur|Le canapé garde sa place, tout calme.",
        2: "narrateur|La table garde sa place, tout calme.",
        3: "narrateur|Le tapis garde sa place, tout calme.",
    }[t1]
    return L(
        "enfant-f|On pêche plus tard, alors ?",
        "copain|Oui, plus tard.",
        "enfant-f|D'accord.",
        later,
        "narrateur|Nino serre encore le chausson.",
        "copain|Garde un poisson pour moi.",
        "enfant-f|Il t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Il a dit oui, pour plus tard.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{T1[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Une nageoire jaune tremble dans le seau.",
            "copain|C'est une prise, Sarah ?",
            "enfant-f|Oui, elle est là.",
            "papa|Vous avez attendu le bon moment.",
            "maman|Le papier est encore un peu chaud.",
            coda,
            "narrateur|Nino souffle sur le poisson, tout petit.",
            "enfant-f|C'est notre mare, maintenant.",
            "narrateur|Un peu de savon reste sur le papier.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|La boîte est fermée, contre le genou.",
            "enfant-f|Tu as dit oui, tout bas.",
            "copain|J'avais entendu, près de toi.",
            "papa|Ta voix est restée tout bas.",
            "maman|Pêchez un peu, tout doux.",
            coda,
            "narrateur|Nino pose sa joue, tout calme.",
            "enfant-f|Reste autant que tu veux.",
            "narrateur|La clé de la boîte dort, enfin.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Après la chanson, la ficelle descend.",
            "copain|On a écouté ensemble, d'abord.",
            "enfant-f|Puis tu as dit : on y va.",
            "maman|Deux oreilles, puis un poisson.",
            "papa|Le salon redevient calme.",
            coda,
            "narrateur|Nino rit, tout petit.",
            "enfant-f|La mare t'a attendu.",
            "narrateur|Deux mains tiennent le bâton, déjà.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le camion dort, près du seau.",
            "copain|J'ai fini, Sarah.",
            "enfant-f|Tu as dit oui.",
            "papa|Vous tenez tous les deux, maintenant.",
            "maman|Le poisson descend jusqu'à vous.",
            coda,
            "narrateur|Nino tape deux fois, tout doux.",
            "enfant-f|C'est le signal.",
            "narrateur|Une roue jaune sent encore le tapis.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le camion a un poisson, maintenant.",
            "enfant-f|Le tien, et le mien.",
            "copain|Il était plat, Sarah.",
            "papa|Vous avez partagé sans tout casser.",
            "maman|La mare, au fond, pour deux.",
            coda,
            "narrateur|Nino souffle, puis Sarah souffle.",
            "enfant-f|On reste encore un peu.",
            "narrateur|Un poisson plat dort sur le bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Deux jeux restent côte à côte.",
            "copain|Tu n'as pas pris mon camion.",
            "enfant-f|Tu avais dit non.",
            "papa|Son camion est resté à lui.",
            "maman|Vous vous parlez encore, d'ici.",
            coda,
            "narrateur|Nino tend une roue, alors.",
            "enfant-f|Je la prends, d'à côté.",
            "narrateur|Deux jeux se parlent, tout calme.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les deux chaussons sont chauds, enfin.",
            "copain|On l'a eu, ensemble.",
            "enfant-f|Puis la mare est arrivée.",
            "papa|Vous avez aidé à son heure.",
            "maman|Le seau attend encore, tout doux.",
            coda,
            "narrateur|Nino fait un signe vers le tapis.",
            "enfant-f|La mare t'a vu, une minute.",
            "narrateur|Un fil jaune passe, tout loin.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le petit regard est déjà fini.",
            "copain|Le poisson a brillé, une fois.",
            "enfant-f|Merci d'avoir regardé.",
            "papa|Vous avez vu juste assez.",
            "maman|La mare entre, maintenant.",
            coda,
            "narrateur|Nino fait un signe vers le seau.",
            "enfant-f|On l'a vue, une minute.",
            "narrateur|Le radiateur reprend, tout doux.",
        )
    return L(
        "narrateur|Nino enfile encore, un instant.",
        "enfant-f|Plus tard, il a dit.",
        "enfant-f|Le poisson t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le seau attend, tout doux.",
        coda,
        "narrateur|Sarah garde une place, tout calme.",
        "enfant-f|La mare t'attend, Nino.",
        "narrateur|La ficelle fait un pont, encore.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Dehors, la mare a trop de vent.",
        "narrateur|Le salon est tiède, tout calme.",
        "narrateur|Le tapis sent encore le savon.",
        "papa|Les manteaux sèchent, près du radiateur.",
        "maman|Le seau bleu est vide, Sarah.",
        "narrateur|Des ciseaux brillent sur la table.",
        "enfant-f|Je fais un étang, pour Nino.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-f|Oui, papa.",
        "narrateur|En ce moment, Sarah coupe un poisson.",
        "maman|Le papier jaune craque, tout doux.",
        "papa|Merci, tu tiens le seau bien.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le tapis attend, tout calme.",
        "narrateur|Le bâton, le seau, ou le poisson.",
        "papa|On commence par quoi, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bâton", "le seau bleu", "le poisson jaune")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = T1[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la boîte à musique", "le camion jaune", "les chaussons")

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
        "Sarah veut une pêche sur le tapis du salon, pour Nino. "
        "T1 = bâton (canapé, rive haute) / seau bleu (table, port) / poisson jaune "
        "(tapis tiède) : le voyage change. "
        "T2 = boîte à musique (chanson à finir) / camion jaune (pas garé) / "
        "chaussons (un pied nu). "
        "T3 = neuf résolutions : attendre la chanson, proposer tout bas, s'asseoir ; "
        "laisser garer, un poisson dans le camion, garder le seau (accepter le non) ; "
        "aider le chausson, un tout petit regard, plus tard. "
        "La leçon se vit : elle propose, elle accepte oui, non, ou une autre idée. "
        "Fin : poissons jaunes, seau, ficelle.",
        "N1 ≤ 10. Lina et le slogan « Inviter sans forcer » jetés. "
        "Autre récit que DIF-021 (pas de fort, pas de coussins), DIF-031 "
        "(pas de potager, pas de tomates) et DIF-041 (pas de wagon, pas de mer). "
        "Un merci de papa lié au geste (tenir le seau). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
