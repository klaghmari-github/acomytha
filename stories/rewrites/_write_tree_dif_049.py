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
                "narrateur|Nino tourne la petite clé, absorbé.",
                "enfant-f|Nino, la mare est prête.",
                "narrateur|Une note tinte, encore la même.",
                "copain|Elle n'a pas dit au revoir.",
                "enfant-f|On pêche après la note ?",
                "copain|Cette chanson, d'abord.",
                "maman|La boîte tient encore sa voix.",
                "papa|Tu restes près de lui ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Sarah pose le seau près de la boîte.",
                "narrateur|Nino penche l'oreille, tout près.",
                "enfant-f|Nino, le seau est bleu.",
                "narrateur|La clé glisse, puis reprend.",
                "copain|Elle n'a pas dit au revoir.",
                "enfant-f|Tu viens à la table ?",
                "copain|Cette chanson, d'abord.",
                "papa|Il suit encore la note.",
                "maman|Tu restes près de lui ?",
            )
        return L(
            "narrateur|Le poisson jaune tremble près du tapis.",
            "narrateur|Nino tourne la clé, tout bas.",
            "enfant-f|Nino, ma mare est tiède.",
            "narrateur|Le radiateur chante avec la boîte.",
            "copain|Elle n'a pas dit au revoir.",
            "enfant-f|Tu viens t'allonger ?",
            "copain|Cette chanson, d'abord.",
            "maman|La note n'est pas partie.",
            "papa|Tu restes près de lui ?",
        )
    if t2 == 2:
        if t1 == 1:
            return L(
                "narrateur|Un camion jaune passe sous le canapé.",
                "narrateur|Nino le pousse entre deux livres.",
                "enfant-f|Nino, on pêche d'en haut.",
                "copain|Il va au garage, encore.",
                "enfant-f|Tu viens sur le canapé ?",
                "copain|Le garage, d'abord.",
                "narrateur|Les roues font un petit rrr.",
                "maman|Il range encore sa route.",
                "papa|Tu fais quoi, alors ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Nino a déjà son camion, à la table.",
                "narrateur|Le seau bleu attend, tout près.",
                "enfant-f|Nino, tu veux un poisson ?",
                "copain|Il va au garage, encore.",
                "enfant-f|On le met dans le seau ?",
                "copain|Le garage, d'abord.",
                "narrateur|Une roue frotte le bois, tout sec.",
                "papa|Le camion n'est pas rentré.",
                "maman|Tu fais quoi, alors ?",
            )
        return L(
            "narrateur|Nino pousse le camion sur le tapis.",
            "narrateur|Une roue passe sur la ficelle.",
            "enfant-f|Nino, la mare est tiède.",
            "copain|Il va au garage, encore.",
            "enfant-f|Tu t'allonges avec moi ?",
            "copain|Le garage, d'abord.",
            "narrateur|Le poisson tremble, tout plat.",
            "maman|Il cherche encore sa place.",
            "papa|Tu fais quoi, alors ?",
        )
    if t1 == 1:
        return L(
            "narrateur|Nino s'assoit au bord du tapis.",
            "copain|J'ai un pied froid, Sarah.",
            "enfant-f|On pêche d'en haut, après.",
            "narrateur|Un chausson manque, sous le canapé.",
            "enfant-f|Tu viens sur le canapé ?",
            "copain|L'autre chausson, d'abord.",
            "papa|Il fouille encore, tout calme.",
            "maman|Le second n'est pas là.",
            "papa|Tu l'aides, ou tu attends ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino quitte la table, un pied nu.",
            "copain|J'ai un pied froid, Sarah.",
            "enfant-f|Le seau est encore vide.",
            "narrateur|Le chausson droit est déjà chaud.",
            "enfant-f|Tu reviens au seau ?",
            "copain|L'autre chausson, d'abord.",
            "maman|Il cherche encore, tout tendu.",
            "papa|Le second n'est pas là.",
            "maman|Tu l'aides, ou tu attends ?",
        )
    return L(
        "narrateur|Nino se tient près du radiateur.",
        "copain|J'ai un pied froid, Sarah.",
        "enfant-f|Ma mare est déjà tiède.",
        "narrateur|Il serre un chausson, tout calme.",
        "enfant-f|Tu t'allonges avec moi ?",
        "copain|L'autre chausson, d'abord.",
        "papa|Il cherche encore, tout près.",
        "maman|Le second n'est pas là.",
        "papa|Tu l'aides, ou tu attends ?",
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
            "enfant-f|J'attends la dernière note.",
            "copain|Merci, Sarah.",
            "narrateur|Elle compte les tintes, sur ses doigts.",
            wait,
            "narrateur|La boîte s'arrête, pile.",
            "copain|Elle a dit au revoir.",
            "enfant-f|Tu viens, alors ?",
            "copain|Oui, j'apporte la clé.",
            "papa|Tu as laissé la chanson finir.",
        )
    if t2 == 1 and t3 == 2:
        near = {
            1: "narrateur|Elle glisse un poisson contre le canapé.",
            2: "narrateur|Elle glisse un poisson contre la table.",
            3: "narrateur|Elle glisse un poisson contre le tapis.",
        }[t1]
        return L(
            "enfant-f|Nino, un poisson t'écoute.",
            near,
            "narrateur|Sa voix reste tout bas, près de lui.",
            "copain|Il a une oreille, lui aussi ?",
            "enfant-f|Oui, tout calme.",
            "copain|Je viens, alors.",
            "narrateur|Il pose la clé, sans la perdre.",
            "papa|Tu as parlé tout contre lui.",
            "maman|Il a dit oui, tout seul.",
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
            "copain|Tu entends le ding, toi aussi ?",
            "enfant-f|Oui, dans le ventre.",
            "narrateur|Un dernier ding les fait sauter.",
            "copain|On pêche, après ça.",
            "papa|Tu as écouté sa boîte.",
            "maman|C'est lui qui a dit après.",
        )
    if t2 == 2 and t3 == 1:
        wait = {
            1: "narrateur|Le canapé garde sa rive, encore.",
            2: "narrateur|Le seau bleu garde son bois.",
            3: "narrateur|Le poisson jaune garde le tapis.",
        }[t1]
        return L(
            "enfant-f|J'attends le garage.",
            "copain|Merci, Sarah.",
            wait,
            "narrateur|Le camion se glisse entre deux livres.",
            "copain|Il est rentré, maintenant.",
            "enfant-f|Tu viens, alors ?",
            "copain|Oui, je laisse les roues.",
            "papa|Tu as laissé le garage finir.",
            "maman|Il a dit oui, après.",
        )
    if t2 == 2 and t3 == 2:
        offer = {
            1: "narrateur|Elle pose le poisson sur le capot.",
            2: "narrateur|Elle pose le poisson sur le bois.",
            3: "narrateur|Elle pose le poisson sur une roue.",
        }[t1]
        return L(
            "enfant-f|Nino, un poisson voyageur ?",
            offer,
            "copain|Il tient, sur le camion ?",
            "enfant-f|Tout plat, oui.",
            "narrateur|Le papier colle un peu, puis tient.",
            "copain|On va jusqu'au seau, alors.",
            "enfant-f|D'accord.",
            "papa|Le poisson a pris la route.",
            "maman|Il a choisi le voyage.",
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
            "enfant-f|Je pêche ici, alors.",
            side,
            "narrateur|Un poisson se colle à sa chaussette.",
            "copain|Il t'a pêchée, toi !",
            "enfant-f|Je ris, d'à côté.",
            "papa|Tu as gardé ton seau.",
            "maman|Le camion est resté à lui.",
        )
    if t2 == 3 and t3 == 1:
        help_ = {
            1: "narrateur|Elle fouille sous le canapé, tout doux.",
            2: "narrateur|Elle fouille sous la table, tout doux.",
            3: "narrateur|Elle fouille près du radiateur, tout doux.",
        }[t1]
        return L(
            "enfant-f|J'aide un peu.",
            help_,
            "narrateur|Un chausson chaud apparaît, enfin.",
            "copain|Il s'était caché !",
            "enfant-f|Près du bord, oui.",
            "narrateur|Deux pieds, maintenant, tout chauds.",
            "copain|On peut pêcher, là.",
            "papa|Tu as cherché avec lui.",
            "maman|Le pied froid n'a plus froid.",
        )
    if t2 == 3 and t3 == 2:
        look = {
            1: "narrateur|Ils se penchent vers la rive du canapé.",
            2: "narrateur|Ils se penchent vers le seau, une seconde.",
            3: "narrateur|Ils se penchent vers la mare du tapis.",
        }[t1]
        return L(
            "enfant-f|Un tout petit regard, Nino ?",
            "copain|Très petit, alors.",
            "enfant-f|D'accord.",
            look,
            "narrateur|Un poisson jaune brille, une seconde.",
            "copain|Il nage, presque.",
            "narrateur|Puis Nino reprend le chausson.",
            "papa|Tu as montré juste un peu.",
            "maman|Il a vu, puis choisi.",
        )
    later = {
        1: "narrateur|Le canapé garde sa rive, tout calme.",
        2: "narrateur|La table garde le seau, tout calme.",
        3: "narrateur|Le tapis garde sa mare, tout calme.",
    }[t1]
    return L(
        "enfant-f|On pêche plus tard, alors ?",
        "copain|Oui, plus tard.",
        "enfant-f|D'accord.",
        later,
        "narrateur|Nino serre encore le chausson.",
        "copain|Garde un poisson pour moi.",
        "enfant-f|Il t'attend dans le seau.",
        "papa|Tu as dit une autre heure.",
        "maman|Le pied froid cherche encore.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{T1[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La ficelle tremble, puis un papier vient.",
            "copain|Il a mordu, Sarah ?",
            "enfant-f|Oui, tout plat.",
            "papa|La chanson a laissé la place.",
            "maman|Le seau fait un petit ploc.",
            coda,
            "narrateur|Nino pose la clé à côté du seau.",
            "enfant-f|La mare chante, maintenant.",
            "narrateur|Un peu de savon reste sur le papier.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le poisson collé écoute encore, un peu.",
            "enfant-f|Il t'a attendu, tout bas.",
            "copain|J'ai dit oui, près de toi.",
            "papa|Ta voix n'a pas cassé la note.",
            "maman|Pêchez, maintenant, tout doux.",
            coda,
            "narrateur|Nino tient le bâton, tout calme.",
            "enfant-f|On tire ensemble, tout lent.",
            "narrateur|La clé de la boîte dort, enfin.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Après le ding, la ficelle descend.",
            "copain|On a sauté, d'abord.",
            "enfant-f|Puis tu as dit : on pêche.",
            "maman|Un ding, puis un poisson.",
            "papa|Le salon redevient tiède.",
            coda,
            "narrateur|Nino rit encore, tout petit.",
            "enfant-f|La mare a attendu le ding.",
            "narrateur|Deux mains tiennent le bâton, déjà.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le camion dort entre les livres.",
            "copain|Le garage est fermé, Sarah.",
            "enfant-f|Tu as dit oui, après.",
            "papa|Les roues se sont tues.",
            "maman|Le poisson glisse vers le seau.",
            coda,
            "narrateur|Nino souffle sur la nageoire, tout petit.",
            "enfant-f|Il nage, dans le bleu.",
            "narrateur|Une roue jaune sent encore le tapis.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le camion roule jusqu'au seau.",
            "enfant-f|Le voyageur descend, tout plat.",
            "copain|Il a tenu sur le capot.",
            "papa|Vous avez fait une route, ensemble.",
            "maman|Le seau devient un port, maintenant.",
            coda,
            "narrateur|Nino pousse une dernière fois, tout doux.",
            "enfant-f|On reste encore un peu.",
            "narrateur|Un poisson plat dort sur le bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Le camion reste à sa place.",
            "copain|Tu n'as pas pris mes roues.",
            "enfant-f|Tu avais dit non.",
            "papa|Son garage est resté à lui.",
            "maman|La chaussette a eu un poisson.",
            coda,
            "narrateur|Nino rit, puis pousse encore.",
            "enfant-f|Je pêche, tu roules.",
            "narrateur|Deux jeux se parlent, tout calme.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les deux chaussons sont chauds, enfin.",
            "copain|Le pied froid n'a plus froid.",
            "enfant-f|On peut pêcher, là.",
            "papa|Vous avez cherché ensemble.",
            "maman|Le seau attend encore, tout doux.",
            coda,
            "narrateur|Nino s'allonge, le pied au chaud.",
            "enfant-f|La mare est tiède, pour deux.",
            "narrateur|Un fil jaune passe, tout loin.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le petit regard est déjà fini.",
            "copain|Il nageait, presque.",
            "enfant-f|Tu as vu, une seconde.",
            "papa|Un œil a suffi, déjà.",
            "maman|Le chausson est chaussé, maintenant.",
            coda,
            "narrateur|Nino s'assoit au bord du seau.",
            "enfant-f|On tire, tout doux.",
            "narrateur|Le radiateur reprend, tout bas.",
        )
    return L(
        "narrateur|Nino enfile encore, un instant.",
        "enfant-f|Plus tard, il a dit.",
        "enfant-f|Le poisson t'attend dans le seau.",
        "papa|Tu as dit une autre heure.",
        "maman|Le pied froid cherche encore.",
        coda,
        "narrateur|Sarah laisse un poisson à part.",
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
        "enfant-f|Je fais une mare, pour Nino.",
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
