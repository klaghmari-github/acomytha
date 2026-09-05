#!/usr/bin/env python3
"""TREE-DIF-019 — La petite boutique de Sarah et Nino (N2, DIF.ENE.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-019"
N2 = LIMITS["N2"]
TITLE = "La petite boutique de Sarah et Nino"
FIL = (
    "Au marché du village, Sarah tient une pêche chaude. "
    "Elle veut ouvrir une petite boutique avec Nino. "
    "Les pieds de Nino tapent, sautent, dansent. "
    "T1 = bac / toboggan / balançoires (trois voyages). "
    "T2 = ballon / seau / doudou (neuf aventures). "
    "T3 = jouer ensemble, attendre, ou demander à papa ou maman. "
    "La boutique ouvre. Ils goûtent la pêche."
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
    out["characters"] = "Sarah, Nino, papa, maman"
    out["setting"] = "le marché du village, puis l'aire de jeux"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "ce n'est pas une faute",
        "beaucoup d'énergie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "sami",
        "il ne faut pas",
        "hyperactif",
        "camarade qui bouge",
    ):
        if bad in blob:
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


LIEU = {
    1: {
        "lab": "le bac à sable",
        "sol": "Un grain de sable reste collé à la pêche.",
        "bruit": "Sous les pieds, le sable chuchote encore.",
        "coda": "Un trou rond reste au milieu du bac.",
        "q_lead": "Sarah a posé la pêche dans le bac.",
        "q_ask": "Elle l'a posée où ?",
        "q_ans": "dans le bac",
        "q_acc": "bac | le bac | dans le bac | dans le sable | sable | au bac",
        "q_retry": "La pêche est dans le bac.",
    },
    2: {
        "lab": "le toboggan",
        "sol": "Le métal reste chaud, un peu lisse.",
        "bruit": "Un petit toc dort encore dans le métal.",
        "coda": "Vide et chaud, le toboggan se tait.",
        "q_lead": "Nino attend la pêche, tout en bas.",
        "q_ask": "Nino attend où ?",
        "q_ans": "en bas",
        "q_acc": "en bas | bas | au bas | sous le toboggan | en bas du toboggan",
        "q_retry": "Nino attend en bas.",
    },
    3: {
        "lab": "les balançoires",
        "sol": "Un brin d'herbe reste au mollet de Sarah.",
        "bruit": "Puis la chaîne se tait, tout doux.",
        "coda": "Plus aucun cri sur la chaîne.",
        "q_lead": "Sarah a noué le linge à la chaîne.",
        "q_ask": "Le linge pend où ?",
        "q_ans": "à la chaîne",
        "q_acc": "chaîne | la chaîne | à la chaîne | sur la balançoire | balançoire",
        "q_retry": "Le linge pend à la chaîne.",
    },
}

OBJ = {
    1: {"lab": "le ballon", "cap": "Le ballon", "le": "le ballon"},
    2: {"lab": "le seau", "cap": "Le seau", "le": "le seau"},
    3: {"lab": "le doudou", "cap": "Le doudou", "le": "le doudou"},
}

T3_LABS = {
    1: ("on joue", "on attend", "papa le tient"),
    2: ("tout doux", "on s'assoit", "maman tient"),
    3: ("l'enseigne", "sur le banc", "maman l'attache"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah court vers le bac à sable.",
            "narrateur|Le sable est tiède, un peu rêche.",
            "enfant-f|Ici, on plante la boutique !",
            "copain|J'arrive !",
            "narrateur|Nino saute dans le bac, les deux pieds.",
            "narrateur|Un nuage de sable s'élève, tout fin.",
            "papa|Tes pieds dansent déjà, Nino.",
            "enfant-f|La pêche, elle, reste sage.",
            "narrateur|Sarah creuse un petit trou, au milieu.",
            "narrateur|Elle y pose la pêche, tout doux.",
            "copain|Encore plus profond !",
            "maman|On l'ouvre d'ici, alors ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah court vers le toboggan.",
            "narrateur|Le métal est chaud, un peu lisse.",
            "enfant-f|On livre la pêche, en glissant !",
            "copain|Moi je suis le client !",
            "narrateur|Nino dévale les marches, toc toc toc.",
            "papa|Doucement, les marches sont chaudes.",
            "narrateur|Il s'assoit en bas, puis se relève.",
            "narrateur|Ses pieds tapent encore le sol.",
            "enfant-f|Attends, je la glisse !",
            "copain|Plus vite, Sarah !",
            "maman|La pêche n'a pas encore glissé.",
            "papa|On reste un moment, ici ?",
        )
    return L(
        "narrateur|Sarah court vers les balançoires.",
        "narrateur|La chaîne est froide, un peu rêche.",
        "enfant-f|L'enseigne, c'est le linge !",
        "copain|Je la fais voler !",
        "narrateur|Nino pousse le siège, très fort.",
        "narrateur|La chaîne chante un petit cri.",
        "maman|Tes pieds donnent trop d'élan, Nino.",
        "narrateur|Sarah noue le linge à carreaux.",
        "narrateur|Il pend, et il claque au vent.",
        "enfant-f|Boutique ouverte !",
        "copain|Encore plus haut !",
        "papa|On accroche comment, alors ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Oui, la pêche dort dans le bac.",
            "copain|Mes pieds veulent encore sauter.",
            "enfant-f|La boutique, elle, reste sage.",
            "papa|Un objet du jeu, peut-être ?",
            "maman|Le ballon, le seau, ou le doudou.",
            "enfant-f|Pour ouvrir, avec Nino.",
        )
    if t1 == 2:
        return L(
            "narrateur|Oui, Nino attend tout en bas.",
            "copain|Mes pieds veulent déjà remonter.",
            "enfant-f|La pêche n'a pas encore glissé.",
            "maman|On prend un objet, alors ?",
            "papa|Le ballon, le seau, ou le doudou.",
            "enfant-f|Oui, pour la livraison.",
        )
    return L(
        "narrateur|Oui, le linge pend à la chaîne.",
        "copain|Je veux la faire danser encore.",
        "enfant-f|L'enseigne a besoin d'un objet.",
        "papa|Le ballon, le seau, ou le doudou.",
        "maman|Tu choisis, Sarah.",
        "enfant-f|On choisit ensemble.",
    )


def t2_question(t1: int) -> list[str]:
    if t1 == 1:
        lead = "narrateur|Au bac, la boutique n'est pas encore là."
    elif t1 == 2:
        lead = "narrateur|Sur le toboggan, rien n'a encore glissé."
    else:
        lead = "narrateur|À la balançoire, l'enseigne n'est pas prête."
    return L(
        lead,
        "narrateur|Près des caisses, le ballon attend.",
        "narrateur|Un seau goutte un peu, tout près.",
        "narrateur|Du sac de Nino, le doudou dépasse.",
        "papa|Tu prends quoi, pour ouvrir ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    key = (t1, t2)
    if key == (1, 1):
        return L(
            "narrateur|Nino voit le ballon dans le sable.",
            "copain|Moi je le fais rouler !",
            "narrateur|Son pied part, trop vite.",
            "narrateur|Le ballon rentre dans le petit trou.",
            "enfant-f|Il penche ma pêche !",
            "papa|Tes pieds l'ont trouvé, Nino.",
            "maman|La boutique penche, un peu.",
            "narrateur|Un grain colle déjà au cuir.",
            "copain|Encore un coup !",
            "enfant-f|Ma pêche va tomber.",
            "papa|Vous faites comment, tous les deux ?",
        )
    if key == (1, 2):
        return L(
            "narrateur|Nino tire le seau vers le bac.",
            "copain|Je verse, pour la boutique !",
            "narrateur|L'eau part d'un seul coup.",
            "narrateur|La pêche se retrouve dans une flaque.",
            "enfant-f|Elle nage, maintenant !",
            "maman|Le seau a tout donné, trop vite.",
            "papa|Tes mains ont versé d'un trait.",
            "narrateur|Le sable devient boue, tout autour.",
            "copain|C'est un lac, Sarah !",
            "enfant-f|Je ne vois plus le trou.",
            "maman|Vous versez comment, alors ?",
        )
    if key == (1, 3):
        return L(
            "narrateur|Nino plante le doudou dans le sable.",
            "copain|C'est le marchand !",
            "narrateur|Il saute autour, les deux pieds.",
            "narrateur|Le doudou bascule sur la pêche.",
            "enfant-f|Il la cache, tout entier !",
            "papa|Tes pieds ont trop bougé, Nino.",
            "maman|Le marchand s'est couché.",
            "narrateur|Un oreille de tissu dépasse encore.",
            "copain|Il s'est endormi !",
            "enfant-f|Ma pêche, je ne la vois plus.",
            "papa|Vous le remettez comment ?",
        )
    if key == (2, 1):
        return L(
            "narrateur|Nino pose le ballon en haut.",
            "copain|Lui, il glisse le premier !",
            "narrateur|Le ballon dévale, toc toc toc.",
            "narrateur|La pêche reste dans la main de Sarah.",
            "enfant-f|Ce n'est pas la livraison !",
            "papa|Le ballon a pris la place.",
            "maman|Tes pieds l'ont poussé, Nino.",
            "narrateur|En bas, le ballon rebondit, puis s'arrête.",
            "copain|Encore une fois !",
            "enfant-f|Ma pêche n'a pas glissé.",
            "papa|Vous livrez comment, alors ?",
        )
    if key == (2, 2):
        return L(
            "narrateur|Nino glisse la pêche dans le seau.",
            "copain|Elle voyage dans l'eau !",
            "narrateur|Il part trop vite sur le métal.",
            "narrateur|L'eau gicle, une ligne brillante.",
            "enfant-f|Le seau a tout perdu !",
            "maman|Tes pieds ont donné un coup.",
            "papa|La pêche tape le fond, toc.",
            "narrateur|Une goutte mouille le genou de Sarah.",
            "copain|On recommence, plus fort !",
            "enfant-f|Elle est toute mouillée.",
            "maman|Vous descendez comment, alors ?",
        )
    if key == (2, 3):
        return L(
            "narrateur|Nino pose le doudou tout en bas.",
            "copain|Toi tu es le client !",
            "narrateur|Il remonte en sautant les marches.",
            "narrateur|Le doudou glisse, puis tombe à côté.",
            "enfant-f|Le client n'est plus à sa place !",
            "papa|Tes pieds ont trop tapé, Nino.",
            "maman|Le doudou attend dans l'herbe.",
            "narrateur|Sarah tient encore la pêche, en haut.",
            "copain|Je le remets, et je saute !",
            "enfant-f|Il va retomber.",
            "papa|Vous le gardez comment, le client ?",
        )
    if key == (3, 1):
        return L(
            "narrateur|Nino lance le ballon vers le linge.",
            "copain|Je touche l'enseigne !",
            "narrateur|Le ballon tape le tissu, pan.",
            "narrateur|Le nœud se desserre, un peu.",
            "enfant-f|L'enseigne va tomber !",
            "maman|Tes pieds ont donné l'élan, Nino.",
            "papa|Le linge claque, trop fort.",
            "narrateur|Sarah rattrape un coin, tout juste.",
            "copain|Encore un pan !",
            "enfant-f|Elle ne tient plus.",
            "papa|Vous jouez comment, avec le ballon ?",
        )
    if key == (3, 2):
        return L(
            "narrateur|Nino accroche le seau à la chaîne.",
            "copain|C'est le panier de la boutique !",
            "narrateur|Il pousse, et le seau s'envole.",
            "narrateur|L'eau dessine un arc, tout court.",
            "enfant-f|Le panier verse partout !",
            "papa|La chaîne va trop vite, Nino.",
            "maman|Tes pieds ont trop poussé.",
            "narrateur|Une goutte touche le linge à carreaux.",
            "copain|C'est de la pluie !",
            "enfant-f|L'enseigne est mouillée.",
            "maman|Vous le tenez comment, le seau ?",
        )
    return L(
        "narrateur|Nino noue le doudou à l'autre chaîne.",
        "copain|Deux enseignes, encore plus belles !",
        "narrateur|Il se balance, très fort.",
        "narrateur|Le doudou s'envole, une seconde.",
        "enfant-f|Il va partir !",
        "maman|Tes pieds font trop de vent, Nino.",
        "papa|Le nœud glisse déjà.",
        "narrateur|Sarah rattrape une oreille, tout près.",
        "copain|Plus haut, doudou !",
        "enfant-f|Il n'est pas une enseigne, comme ça.",
        "papa|Vous l'attachez comment, alors ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le ballon n'a pas ouvert la boutique.",
            "papa|On joue, on attend, ou je le tiens ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le seau n'a pas encore aidé.",
            "maman|Tout doux, on s'assoit, ou je tiens ?",
        )
    return L(
        "narrateur|Le doudou n'est pas encore à sa place.",
        "papa|L'enseigne, le banc, ou maman l'attache ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    sol = f"narrateur|{LIEU[t1]['sol']}"
    if t2 == 1 and t3 == 1:
        play = {
            1: "narrateur|Ils se passent le ballon, dans le bac.",
            2: "narrateur|Ils se passent le ballon, près du métal.",
            3: "narrateur|Ils se passent le ballon, sous la chaîne.",
        }[t1]
        return L(
            "enfant-f|On joue avec, Nino.",
            "copain|À moi, puis à toi !",
            play,
            "narrateur|Les pieds de Nino dansent, pile avec le jeu.",
            "narrateur|Puis Sarah pose la pêche, tout calme.",
            "papa|Vous avez joué, et la boutique tient.",
            "maman|Le ballon a eu son tour.",
            sol,
            "enfant-f|Boutique ouverte !",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Nino s'assoit dans le sable, un moment.",
            2: "narrateur|Nino s'assoit au pied du métal.",
            3: "narrateur|Nino s'assoit dans l'herbe, sous la chaîne.",
        }[t1]
        return L(
            "enfant-f|On attend un peu, Nino.",
            "copain|J'attends, je souffle.",
            wait,
            "narrateur|Le ballon repose, tout rond, tout sage.",
            "narrateur|Sarah replace la pêche, tout doux.",
            "papa|Tes pieds ont su s'asseoir.",
            "maman|La boutique a eu la place.",
            sol,
            "enfant-f|Maintenant, c'est ouvert.",
        )
    if t2 == 1 and t3 == 3:
        hold = {
            1: "narrateur|Papa tient le ballon, hors du bac.",
            2: "narrateur|Papa tient le ballon, près du métal.",
            3: "narrateur|Papa tient le ballon, loin de la chaîne.",
        }[t1]
        return L(
            "enfant-f|Papa, tu le tiens ?",
            "papa|Je le tiens, Sarah.",
            hold,
            "narrateur|Les mains de Nino sont libres, maintenant.",
            "narrateur|Sarah pose la pêche, pile au milieu.",
            "copain|Je t'aide, sans le ballon.",
            "maman|Vous avez demandé, et ça tient.",
            sol,
            "enfant-f|La boutique est prête.",
        )
    if t2 == 2 and t3 == 1:
        slow = {
            1: "narrateur|Ils versent goutte à goutte, dans le bac.",
            2: "narrateur|Ils versent goutte à goutte, sur le métal.",
            3: "narrateur|Ils versent goutte à goutte, sous la chaîne.",
        }[t1]
        return L(
            "enfant-f|Tout doux, Nino, avec moi.",
            "copain|Goutte, puis goutte.",
            slow,
            "narrateur|Les mains de Nino suivent celles de Sarah.",
            "narrateur|La pêche a juste un peu d'eau, autour.",
            "papa|Vous avez versé ensemble.",
            "maman|Le seau a gardé le reste.",
            sol,
            "enfant-f|Boutique ouverte, tout propre.",
        )
    if t2 == 2 and t3 == 2:
        sit = {
            1: "narrateur|Ils s'assoient au bord du bac.",
            2: "narrateur|Ils s'assoient au pied du toboggan.",
            3: "narrateur|Ils s'assoient sous les balançoires.",
        }[t1]
        return L(
            "enfant-f|On s'assoit, Nino.",
            "copain|Mes pieds, restez là.",
            sit,
            "narrateur|Le seau repose entre eux, tout calme.",
            "narrateur|L'eau ne bouge plus, un miroir.",
            "maman|Vous avez laissé l'eau s'asseoir.",
            "papa|La pêche a séché un peu.",
            sol,
            "enfant-f|On ouvre, maintenant.",
        )
    if t2 == 2 and t3 == 3:
        mum = {
            1: "narrateur|Maman tient le seau, au bord du bac.",
            2: "narrateur|Maman tient le seau, au pied du métal.",
            3: "narrateur|Maman tient le seau, sous la chaîne.",
        }[t1]
        return L(
            "enfant-f|Maman, tu le tiens ?",
            "maman|Je le tiens, tout stable.",
            mum,
            "narrateur|Nino pose un doigt sur le bord, tout léger.",
            "narrateur|Sarah replace la pêche, au sec.",
            "copain|Je ne verse plus tout seul.",
            "papa|Vous avez demandé, et ça tient.",
            sol,
            "enfant-f|La boutique est prête.",
        )
    if t2 == 3 and t3 == 1:
        sign = {
            1: "narrateur|Ils plantent le doudou derrière la pêche.",
            2: "narrateur|Ils posent le doudou au bas du métal.",
            3: "narrateur|Ils nouent le doudou à côté du linge.",
        }[t1]
        return L(
            "enfant-f|Toi tu es l'enseigne, doudou.",
            "copain|Je le tiens, tu le places.",
            sign,
            "narrateur|Les pieds de Nino s'arrêtent, le temps du nœud.",
            "narrateur|Le doudou regarde la pêche, tout droit.",
            "papa|Vous l'avez mis à sa place.",
            "maman|L'enseigne tient, cette fois.",
            sol,
            "enfant-f|Boutique ouverte !",
        )
    if t2 == 3 and t3 == 2:
        bench = {
            1: "narrateur|Le doudou s'assoit au bord du bac.",
            2: "narrateur|Le doudou s'assoit au pied du toboggan.",
            3: "narrateur|Le doudou s'assoit sur le banc, près des chaînes.",
        }[t1]
        return L(
            "enfant-f|Sur le banc, Nino, un moment.",
            "copain|Toi tu regardes, doudou.",
            bench,
            "narrateur|Nino souffle, et ses pieds se taisent.",
            "narrateur|Sarah replace la pêche, tout net.",
            "maman|Le doudou a sa place, à côté.",
            "papa|Vous avez laissé la boutique libre.",
            sol,
            "enfant-f|C'est ouvert.",
        )
    pin = {
        1: "narrateur|Maman cale le doudou contre la caisse.",
        2: "narrateur|Maman cale le doudou au pied du métal.",
        3: "narrateur|Maman noue le doudou, un nœud court.",
    }[t1]
    return L(
        "enfant-f|Maman, tu l'attaches ?",
        "maman|Je l'attache, tout ferme.",
        pin,
        "narrateur|Nino tient le bout, sans sauter.",
        "narrateur|Sarah pose la pêche, pile devant.",
        "copain|Il ne part plus.",
        "papa|Vous avez demandé, et ça tient.",
        sol,
        "enfant-f|La boutique est prête.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{LIEU[t1]['coda']}"
    bruit = f"narrateur|{LIEU[t1]['bruit']}"
    outil = OBJ[t2]["cap"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils croquent la pêche, encore tiède.",
            "copain|On a joué, et elle est à nous !",
            "enfant-f|La boutique a tenu, Nino.",
            "papa|Tes pieds ont dansé dans le jeu.",
            "maman|Une bouchée pour chacun.",
            "narrateur|Le jus colle un peu au menton.",
            f"narrateur|{outil} repose, tout rond, à côté.",
            bruit,
            coda,
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sarah tend un quartier à Nino.",
            "copain|J'ai attendu, et elle est sucrée.",
            "enfant-f|Tes pieds se sont tus, un moment.",
            "maman|Le sucré valait l'attente.",
            "papa|Le jus, sur le pouce ?",
            "enfant-f|Oui, il brille.",
            f"narrateur|{outil} reste sage, tout près.",
            bruit,
            coda,
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Papa rend le ballon, après la bouchée.",
            "enfant-f|Tu l'as tenu, on a ouvert.",
            "copain|Maintenant je peux le reprendre.",
            "papa|Quand la boutique a fini, oui.",
            "maman|Essuie ton menton, tout doux.",
            "narrateur|Un filet sucré reste au coin.",
            f"narrateur|{outil} reprend un petit bond, plus tard.",
            bruit,
            coda,
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Ils goûtent au bord, les mains encore fraîches.",
            "enfant-f|On a versé goutte à goutte.",
            "copain|Mes mains ont suivi les tiennes.",
            "papa|Le seau a gardé le reste.",
            "maman|La pêche a juste un peu d'eau.",
            "narrateur|Nino souffle sur un quartier, puis croque.",
            f"narrateur|{outil} sonne creux, après.",
            bruit,
            coda,
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils croquent assis, tout lent.",
            "copain|On s'est assis, et l'eau s'est tue.",
            "enfant-f|Puis la boutique a ouvert.",
            "maman|Vos pieds ont su rester là.",
            "papa|Le sucré, ça valait l'assise.",
            "narrateur|Le jus coule, une perle, au poignet.",
            f"narrateur|{outil} garde une auréole, au fond.",
            bruit,
            coda,
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Maman pose le seau, après la part.",
            "enfant-f|Tu l'as tenu, on a ouvert.",
            "copain|Je n'ai plus tout versé.",
            "papa|Vous avez demandé, pile à temps.",
            "maman|Tes pieds pendent, tout sages.",
            "narrateur|Chaque bouchée sent encore le marché.",
            f"narrateur|{outil} repose, le bord vers le ciel.",
            bruit,
            coda,
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le doudou garde encore la boutique.",
            "copain|Il était l'enseigne, tout droit.",
            "enfant-f|On l'a mis ensemble.",
            "papa|Tes pieds ont attendu le nœud.",
            "maman|La pêche a vu son marchand.",
            "narrateur|Sarah croque, et un jus perle.",
            f"narrateur|{outil} a une tache ronde, au ventre.",
            bruit,
            coda,
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Ils s'allongent un peu, près du banc.",
            "copain|Le doudou a regardé, tout sage.",
            "enfant-f|La boutique avait de la place.",
            "maman|Vos pieds se sont tus, un moment.",
            "papa|Une bouchée, puis une autre.",
            "narrateur|Le sucré reste longtemps, en bouche.",
            f"narrateur|{outil} a une oreille encore chaude.",
            bruit,
            coda,
        )
    return L(
        "narrateur|Maman détache le doudou, plus tard.",
        "enfant-f|Tu l'avais attaché, pile.",
        "copain|Il n'est pas parti.",
        "papa|Vous avez demandé, et ça a tenu.",
        "maman|La pêche sent encore le soleil.",
        "narrateur|Trois bouches, un même sucré.",
        f"narrateur|{outil} reprend le sac, tout doux.",
        bruit,
        coda,
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0001_P0001": "sable",
        "CHK_T0001_P0001_C0001": "sable",
        "CHK_T0001_P0002": "metal",
        "CHK_T0001_P0003": "chaine",
        "CHK_T0001_P0001_T0002_P0002": "eau",
        "CHK_T0001_P0002_T0002_P0002": "eau",
        "CHK_T0001_P0003_T0002_P0002": "eau",
    }

    s["CHK_T0000_P0000"] = L(
        "narrateur|Sous les toiles du marché, l'air sent la pêche.",
        "narrateur|Une abeille tourne autour d'une caisse de bois.",
        "narrateur|Les caisses claquent, tout doux, sur les pavés chauds.",
        "narrateur|Un rai de soleil coupe le stand des cerises.",
        "narrateur|L'eau du robinet fait un filet, tout mince.",
        "papa|Tu entends les caisses, Sarah ?",
        "enfant-f|Elles font toc, papa.",
        "maman|Nino arrive, avec son sac rouge.",
        "narrateur|Le sac tape sa jambe, à chaque pas.",
        "narrateur|Un linge à carreaux dépasse du panier.",
        "narrateur|En ce moment, Sarah tient une pêche encore chaude.",
        "narrateur|La peau est un peu rêche, tout sucrée.",
        "enfant-f|Je veux une boutique, comme les stands.",
        "copain|Moi aussi !",
        "narrateur|Les pieds de Nino tapent déjà le pavé.",
        "narrateur|Ses pieds font tap, tap, tap.",
        "enfant-f|On l'ouvre ensemble, Nino.",
        "papa|On l'ouvre où, cette boutique ?",
        "maman|Merci, tu la tiens tout doux, la pêche.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Sous les toiles, le bac attend.",
        "narrateur|Le toboggan brille, un peu chaud.",
        "narrateur|Les balançoires bougent déjà.",
        "papa|Tu vas où, d'abord, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bac à sable", "le toboggan", "les balançoires")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        li = LIEU[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|{li['q_lead']}",
            f"maman|{li['q_ask']}",
        )
        extras[f"{p}_Q0001"] = qf(li["q_ans"], li["q_acc"], li["q_retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le ballon", "le seau", "le doudou")

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
        "Marché du village, pêche chaude, toiles, abeille. Sarah veut une boutique avec Nino. "
        "Les pieds de Nino tapent, sautent, dansent (vécu, pas d'étiquette). "
        "T1 = bac / toboggan / balançoires (trois voyages). "
        "T2 = ballon / seau / doudou (neuf aventures : le ballon penche la pêche, "
        "le seau verse, le doudou tombe). "
        "T3 = neuf résolutions : on joue / on attend / papa tient ; "
        "tout doux / on s'assoit / maman tient ; "
        "l'enseigne / le banc / maman attache. "
        "Fin : la boutique ouvre, ils goûtent la pêche. Leçon vécue, pas de slogan.",
        "N2 ≤ 15. Sara→Sarah. Tom / Léa / Sami jetés. Héros Sarah, copain Nino, papa, maman. "
        "Un merci de maman lié au geste (tenir la pêche). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
