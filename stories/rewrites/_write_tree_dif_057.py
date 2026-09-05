#!/usr/bin/env python3
"""TREE-DIF-057 — Le carillon de Sarah, au prunier (N3, DIF.BES.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-057"
N3 = LIMITS["N3"]
TITLE = "Le carillon de Sarah, au prunier"
FIL = (
    "Sarah veut accrocher un carillon au prunier, pour que Nino entende "
    "le jardin chanter avec elle, avant le vent du soir. Elle prend d'abord "
    "le bocal, le grelot ou le ruban bleu ; les trois viennent. À la table "
    "le verre tinte, sur la marche le grelot court, à la branche le ruban "
    "attend vide. Nino dessine un soleil de craie, suit une coccinelle, "
    "ou cherche une sandale. Elle propose, et elle accepte oui, plus tard, "
    "ou une autre idée. Le carillon sonne."
)
CHARS = "Sarah, Nino, papa, maman"
SETTING = "jardin : table, terrasse, prunier, rose, herbe"


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
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "inviter sans forcer",
        "accepter plusieurs",
        "kenzo",
        "sara ",
        "coussin",
        "le fort",
        "tomate",
        "panier rouge",
        "figuier",
        "les cubes",
        "dînette",
        "dinette",
        "wagon",
        "sifflet",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
        "poissons de papier",
        "nichoir",
        "citronnade",
        "cerf-volant",
        "bac à sable",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    for bad in ("la cuisine", "le jardin", "la chambre", "les cubes", "le livre", "le matin"):
        if bad in labels:
            raise SystemExit(f"{SID} label calque: {bad}")
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
        "lab": "le bocal",
        "ans": "bocal",
        "acc": "bocal | le bocal | d'abord le bocal | le verre",
        "retry": "Sarah a pris le bocal.",
        "coda": "Le bocal garde un toc, encore tiède.",
    },
    2: {
        "lab": "le grelot",
        "ans": "grelot",
        "acc": "grelot | le grelot | d'abord le grelot | la clochette",
        "retry": "Sarah a pris le grelot.",
        "coda": "Le grelot dort contre le verre, tout petit.",
    },
    3: {
        "lab": "le ruban bleu",
        "ans": "ruban",
        "acc": "ruban | le ruban | le ruban bleu | d'abord le ruban",
        "retry": "Sarah a pris le ruban.",
        "coda": "Le ruban bleu tient un nœud, tout calme.",
    },
}

T3_LABS = {
    1: ("attendre le soleil", "parler tout bas", "s'asseoir à côté"),
    2: ("attendre l'envol", "un grelot tout près", "garder le carillon"),
    3: ("aider un peu", "un tout petit regard", "proposer plus tard"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah prend d'abord le bocal, encore tiède.",
            "enfant-f|Il va chanter, tout creux.",
            "maman|Tiens-le à deux mains, tout doux.",
            "narrateur|Elle le pose sur la table du jardin, encore chaude.",
            "papa|Le verre fait un toc, contre le bois.",
            "narrateur|Le grelot glisse à côté, déjà.",
            "narrateur|Maman noue le ruban autour du col.",
            "enfant-f|Nino va l'entendre, d'ici.",
            "papa|Tu lui proposes, quand tu le trouves ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah prend d'abord le grelot, tout froid.",
            "enfant-f|Il va courir jusqu'au prunier.",
            "papa|Secoue-le tout bas, pas trop fort.",
            "narrateur|Elle le fait tinter sur la marche de pierre.",
            "maman|Le bocal aussi, près de toi.",
            "narrateur|Le ruban s'enroule autour de son poignet.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Nino va suivre le son.",
            "maman|Tu lui proposes, tout calme ?",
            "enfant-f|Oui, maman.",
        )
    return L(
        "narrateur|Sarah prend d'abord le ruban bleu.",
        "enfant-f|Il va tenir le carillon.",
        "maman|Noue une boucle, tout doux.",
        "narrateur|Puis elle rejoint la branche basse du prunier.",
        "papa|Le prunier penche, tout près.",
        "narrateur|Le bocal et le grelot la suivent.",
        "narrateur|Rien ne reste près de la porte.",
        "enfant-f|Nino va voir ma boucle.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-f|Oui.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le verre est déjà dans ses mains.",
            "maman|Elle a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le petit fer tinte encore.",
            "papa|Elle a pris quoi, d'abord ?",
        )
    return L(
        "narrateur|Le bleu tremble entre ses doigts.",
        "maman|Elle a noué quoi ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|Le bocal.",
            "maman|Oui.",
            "narrateur|Le verre garde un toc, tout creux.",
            "narrateur|La table du jardin sent le bois chaud.",
            "enfant-f|Nino est dehors, déjà.",
            "papa|Je l'entends, plus loin.",
            "maman|Vous allez le trouver.",
            "enfant-f|Je lui propose le carillon.",
        )
    if t1 == 2:
        return L(
            "enfant-f|Le grelot.",
            "papa|Oui.",
            "narrateur|Le petit fer dort dans sa paume.",
            "narrateur|La marche garde encore un tintement.",
            "enfant-f|Nino est dehors, déjà.",
            "maman|Je l'entends, plus loin.",
            "papa|Le son a couru vers le prunier.",
            "enfant-f|Je lui propose le grelot.",
        )
    return L(
        "enfant-f|Le ruban.",
        "maman|Oui.",
        "narrateur|Une boucle bleue pend à la branche.",
        "narrateur|Le prunier sent encore les prunes chaudes.",
        "enfant-f|Nino est dehors, déjà.",
        "papa|Je l'entends, plus loin.",
        "maman|La boucle attend, vide.",
        "enfant-f|Je lui propose la branche.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "narrateur|Le bocal tinte encore, tout bas.",
        2: "narrateur|Le grelot dort dans sa paume.",
        3: "narrateur|Le ruban pend déjà, à la branche.",
    }[t1]
    return L(
        head,
        "narrateur|Une craie jaune traîne sur la terrasse.",
        "narrateur|Une rose penche, tout près.",
        "narrateur|Une sandale attend, dans l'herbe.",
        "papa|On va vers quoi, Sarah ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        if t1 == 1:
            return L(
                "narrateur|Sarah quitte la table, le bocal contre elle.",
                "narrateur|Nino dessine un soleil, absorbé.",
                "enfant-f|Nino, le carillon est prêt.",
                "narrateur|Un rayon de craie manque encore.",
                "copain|Mon soleil n'est pas fini.",
                "enfant-f|Tu viens l'entendre, après ?",
                "copain|Ce soleil, d'abord.",
                "maman|La craie tient encore sa poussière.",
                "papa|Tu restes près de lui ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Sarah pose le grelot près de la craie.",
                "narrateur|Nino penche l'oreille, puis reprend.",
                "enfant-f|Nino, ça tinte, tout petit.",
                "narrateur|Le dernier rayon n'est pas tiré.",
                "copain|Mon soleil n'est pas fini.",
                "enfant-f|Tu viens sur la marche ?",
                "copain|Ce soleil, d'abord.",
                "papa|Il suit encore la poussière jaune.",
                "maman|Tu restes près de lui ?",
            )
        return L(
            "narrateur|Le ruban attend à la branche, déjà noué.",
            "narrateur|Sarah revient vers la terrasse, tout doux.",
            "enfant-f|Nino, ma boucle est bleue.",
            "narrateur|Un rayon de craie manque encore.",
            "copain|Il n'a pas son dernier trait.",
            "enfant-f|Tu viens sous le prunier ?",
            "copain|Ce soleil, d'abord.",
            "maman|La craie n'a pas dit au revoir.",
            "papa|Tu restes près de lui ?",
        )
    if t2 == 2:
        if t1 == 1:
            return L(
                "narrateur|Sarah laisse le bocal sur la table.",
                "narrateur|Nino suit une coccinelle, sur la rose.",
                "enfant-f|Nino, le verre va chanter.",
                "copain|Elle n'a pas encore volé.",
                "enfant-f|Tu viens au prunier ?",
                "copain|La coccinelle, d'abord.",
                "narrateur|Une patte rouge hésite, tout bas.",
                "maman|Il écoute encore la rose.",
                "papa|Tu fais quoi, alors ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Le grelot se tait dans son poing.",
                "narrateur|Nino est collé à la rose, déjà.",
                "enfant-f|Nino, tu veux un son tout doux ?",
                "copain|Elle n'a pas encore volé.",
                "enfant-f|On l'écoute, puis on part ?",
                "copain|La coccinelle, d'abord.",
                "narrateur|Une aile tremble, puis se rassoit.",
                "papa|La rose n'a pas fini.",
                "maman|Tu fais quoi, alors ?",
            )
        return L(
            "narrateur|Sarah quitte la branche, le ruban en place.",
            "narrateur|Nino respire tout contre la rose.",
            "enfant-f|Nino, ma boucle t'attend.",
            "copain|Elle n'a pas encore volé.",
            "enfant-f|Tu viens sous le prunier ?",
            "copain|La coccinelle, d'abord.",
            "narrateur|Une patte rouge reste collée, tout calme.",
            "maman|Il ne veut pas bouger.",
            "papa|Tu fais quoi, alors ?",
        )
    if t1 == 1:
        return L(
            "narrateur|Nino s'arrête au bord de l'herbe.",
            "copain|J'ai un pied nu, Sarah.",
            "enfant-f|Le bocal est déjà sur la table.",
            "narrateur|Une sandale manque, sous les tiges.",
            "enfant-f|Tu viens au verre, après ?",
            "copain|L'autre sandale, d'abord.",
            "papa|Il fouille encore, tout calme.",
            "maman|Le second n'est pas là.",
            "papa|Tu l'aides, ou tu attends ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino quitte la marche, un pied nu.",
            "copain|J'ai un pied nu, Sarah.",
            "enfant-f|Le grelot peut t'aider à chercher.",
            "narrateur|La sandale droite est déjà chaude.",
            "enfant-f|Tu reviens au son ?",
            "copain|L'autre sandale, d'abord.",
            "maman|Il cherche encore, tout tendu.",
            "papa|Le second n'est pas là.",
            "maman|Tu l'aides, ou tu attends ?",
        )
    return L(
        "narrateur|Nino se tient sous le prunier, un pied nu.",
        "copain|J'ai un pied nu, Sarah.",
        "enfant-f|Ma boucle est déjà nouée.",
        "narrateur|Il serre une sandale, tout calme.",
        "enfant-f|Tu regardes la branche ?",
        "copain|L'autre sandale, d'abord.",
        "papa|Il cherche encore, tout près.",
        "maman|Le second n'est pas là.",
        "papa|Tu l'aides, ou tu attends ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le soleil de craie n'est pas fini.",
            "papa|Attendre, parler tout bas, ou s'asseoir ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La coccinelle n'est pas partie.",
            "maman|Attendre l'envol, un grelot, ou garder ?",
        )
    return L(
        "narrateur|Une sandale n'est pas chaussée.",
        "papa|Aider, un petit regard, ou plus tard ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le bocal attend sur la table, sans bouger.",
            2: "narrateur|Le grelot attend sur la marche, sans bouger.",
            3: "narrateur|Le ruban attend à la branche, tout calme.",
        }[t1]
        return L(
            "enfant-f|J'attends le dernier trait.",
            "copain|Merci, Sarah.",
            "narrateur|Elle compte les rayons, sur ses doigts.",
            wait,
            "narrateur|La craie s'arrête, pile.",
            "copain|Il a son soleil, maintenant.",
            "enfant-f|Tu viens, alors ?",
            "copain|Oui, j'apporte la craie.",
            "papa|Tu as laissé le soleil finir.",
        )
    if t2 == 1 and t3 == 2:
        near = {
            1: "narrateur|Elle glisse le bocal contre la craie.",
            2: "narrateur|Elle glisse le grelot contre le soleil.",
            3: "narrateur|Elle montre la boucle, tout bas.",
        }[t1]
        return L(
            "enfant-f|Nino, un carillon t'écoute.",
            near,
            "narrateur|Sa voix reste tout bas, près de lui.",
            "copain|Il a une oreille, lui aussi ?",
            "enfant-f|Oui, tout calme.",
            "copain|Je viens, alors.",
            "narrateur|Il pose la craie, sans la perdre.",
            "papa|Tu as parlé tout contre lui.",
            "maman|Il a dit oui, tout seul.",
        )
    if t2 == 1 and t3 == 3:
        sit = {
            1: "narrateur|Sarah s'assoit au pied de la table.",
            2: "narrateur|Sarah s'assoit sur la marche, tout doux.",
            3: "narrateur|Sarah s'assoit dans l'herbe, sous la branche.",
        }[t1]
        return L(
            "enfant-f|Je m'assois à côté.",
            sit,
            "narrateur|Elle ne touche pas la craie.",
            "copain|Tu vois le rayon, toi aussi ?",
            "enfant-f|Oui, il pique un peu.",
            "narrateur|Un dernier trait les fait souffler.",
            "copain|On accroche, après ça.",
            "papa|Tu as écouté son soleil.",
            "maman|C'est lui qui a dit après.",
        )
    if t2 == 2 and t3 == 1:
        wait = {
            1: "narrateur|La table garde le bocal, encore.",
            2: "narrateur|Le grelot dort dans sa paume.",
            3: "narrateur|La branche garde sa boucle, vide.",
        }[t1]
        return L(
            "enfant-f|J'attends l'envol.",
            "copain|Merci, Sarah.",
            wait,
            "narrateur|La coccinelle ouvre une aile, puis part.",
            "copain|Elle a volé, maintenant.",
            "enfant-f|Tu viens, alors ?",
            "copain|Oui, je laisse la rose.",
            "papa|Tu as laissé la rose finir.",
            "maman|Il a dit oui, après.",
        )
    if t2 == 2 and t3 == 2:
        offer = {
            1: "narrateur|Elle fait tinter le verre, tout près.",
            2: "narrateur|Elle ouvre le poing, un tout petit son.",
            3: "narrateur|Elle agite le ruban, une seconde.",
        }[t1]
        return L(
            "enfant-f|Nino, un grelot tout près ?",
            offer,
            "copain|Elle l'entend, la petite ?",
            "enfant-f|Tout doux, oui.",
            "narrateur|Une aile se lève, puis se rassoit.",
            "copain|On va jusqu'au prunier, alors.",
            "enfant-f|D'accord.",
            "papa|Le son n'a pas chassé la rose.",
            "maman|Il a choisi le voyage.",
        )
    if t2 == 2 and t3 == 3:
        side = {
            1: "narrateur|Le bocal reste sur la table, à elle.",
            2: "narrateur|Le grelot reste dans sa paume, à elle.",
            3: "narrateur|Le ruban reste à la branche, à elle.",
        }[t1]
        return L(
            "copain|Pas maintenant, Sarah.",
            "enfant-f|D'accord.",
            "enfant-f|J'accroche ici, alors.",
            side,
            "narrateur|Un toc part vers la rose, tout loin.",
            "copain|Je l'entends, d'ici !",
            "enfant-f|Toi la rose, moi le prunier.",
            "papa|Tu as gardé ton carillon.",
            "maman|La rose est restée à lui.",
        )
    if t2 == 3 and t3 == 1:
        help_ = {
            1: "narrateur|Elle fouille sous la table, tout doux.",
            2: "narrateur|Elle fouille près de la marche, tout doux.",
            3: "narrateur|Elle fouille sous le prunier, tout doux.",
        }[t1]
        return L(
            "enfant-f|J'aide un peu.",
            help_,
            "narrateur|Une sandale chaude apparaît, enfin.",
            "copain|Elle s'était cachée !",
            "enfant-f|Près du bord, oui.",
            "narrateur|Deux pieds, maintenant, tout chauds.",
            "copain|On peut accrocher, là.",
            "papa|Tu as cherché avec lui.",
            "maman|Le pied nu n'a plus froid.",
        )
    if t2 == 3 and t3 == 2:
        look = {
            1: "narrateur|Ils se penchent vers le bocal, une seconde.",
            2: "narrateur|Ils se penchent vers le grelot, une seconde.",
            3: "narrateur|Ils se penchent vers la boucle, une seconde.",
        }[t1]
        return L(
            "enfant-f|Un tout petit regard, Nino ?",
            "copain|Très petit, alors.",
            "enfant-f|D'accord.",
            look,
            "narrateur|Un toc brille, une seconde.",
            "copain|Il chante, presque.",
            "narrateur|Puis Nino reprend la sandale.",
            "papa|Tu as montré juste un peu.",
            "maman|Il a vu, puis choisi.",
        )
    later = {
        1: "narrateur|La table garde le bocal, tout calme.",
        2: "narrateur|La marche garde le grelot, tout calme.",
        3: "narrateur|Le prunier garde sa boucle, tout calme.",
    }[t1]
    return L(
        "enfant-f|On accroche plus tard, alors ?",
        "copain|Oui, plus tard.",
        "enfant-f|D'accord.",
        later,
        "narrateur|Nino serre encore la sandale.",
        "copain|Garde un son pour moi.",
        "enfant-f|Il t'attend à la branche.",
        "papa|Tu as dit une autre heure.",
        "maman|Le pied nu cherche encore.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{T1[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le soleil de craie reste sur la pierre.",
            "copain|Il a son dernier trait, Sarah.",
            "enfant-f|Oui, tout jaune.",
            "papa|La craie a laissé la place.",
            "maman|Le prunier fait un petit toc.",
            coda,
            "narrateur|Nino noue le grelot, tout calme.",
            "enfant-f|Le jardin chante, maintenant.",
            "narrateur|Une prune penche, puis se tait.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le carillon collé écoute encore, un peu.",
            "enfant-f|Il t'a attendu, tout bas.",
            "copain|J'ai dit oui, près de toi.",
            "papa|Ta voix n'a pas cassé le trait.",
            "maman|Accrochez, maintenant, tout doux.",
            coda,
            "narrateur|Nino tient le ruban, tout calme.",
            "enfant-f|On tire ensemble, tout lent.",
            "narrateur|La craie jaune dort, enfin.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Après le dernier trait, le ruban descend.",
            "copain|On a soufflé, d'abord.",
            "enfant-f|Puis tu as dit : on accroche.",
            "maman|Un trait, puis un toc.",
            "papa|Le jardin redevient tiède.",
            coda,
            "narrateur|Nino rit encore, tout petit.",
            "enfant-f|Le prunier a attendu le soleil.",
            "narrateur|Deux mains tiennent le nœud, déjà.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|La rose est vide, maintenant.",
            "copain|Elle a volé, Sarah.",
            "enfant-f|Tu as dit oui, après.",
            "papa|Les ailes se sont tues.",
            "maman|Le grelot glisse vers la branche.",
            coda,
            "narrateur|Nino souffle sur le verre, tout petit.",
            "enfant-f|Il chante, dans le bleu.",
            "narrateur|Une feuille rouge sent encore la rose.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le petit son les mène jusqu'au prunier.",
            "enfant-f|Le grelot descend, tout doux.",
            "copain|Il a tenu près de la rose.",
            "papa|Vous avez fait un chemin, ensemble.",
            "maman|La branche devient une cloche, maintenant.",
            coda,
            "narrateur|Nino pousse le verre, une dernière fois.",
            "enfant-f|On reste encore un peu.",
            "narrateur|Un toc plat dort sur le bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|La rose reste à sa place.",
            "copain|Tu n'as pas pris ma rose.",
            "enfant-f|Tu avais dit non.",
            "papa|Sa rose est restée à lui.",
            "maman|Le prunier a eu son toc, quand même.",
            coda,
            "narrateur|Nino écoute, puis reprend la rose.",
            "enfant-f|Je sonne, tu regardes.",
            "narrateur|Deux jeux se parlent, tout calme.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les deux sandales sont chaudes, enfin.",
            "copain|Le pied nu n'a plus froid.",
            "enfant-f|On peut accrocher, là.",
            "papa|Vous avez cherché ensemble.",
            "maman|La branche attend encore, tout doux.",
            coda,
            "narrateur|Nino s'assoit, le pied au chaud.",
            "enfant-f|Le carillon est prêt, pour deux.",
            "narrateur|Un fil bleu passe, tout loin.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le petit regard est déjà fini.",
            "copain|Il chantait, presque.",
            "enfant-f|Tu as vu, une seconde.",
            "papa|Un œil a suffi, ce soir.",
            "maman|La sandale est chaussée, maintenant.",
            coda,
            "narrateur|Nino s'assoit au bord de l'herbe.",
            "enfant-f|On noue, tout doux.",
            "narrateur|Le prunier reprend, tout bas.",
        )
    return L(
        "narrateur|Nino enfile encore, un instant.",
        "enfant-f|Plus tard, il a dit.",
        "enfant-f|Le son t'attend à la branche.",
        "papa|Tu as dit une autre heure.",
        "maman|Le pied nu cherche encore.",
        coda,
        "narrateur|Sarah laisse un toc à part.",
        "enfant-f|Le prunier t'attend, Nino.",
        "narrateur|Le ruban fait un pont, encore.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une feuille sèche claque encore contre le vieux prunier.",
        "narrateur|Le jardin derrière la maison sent la terre chaude.",
        "narrateur|Les mains de Sarah sont déjà collantes de prune.",
        "papa|Le vent du soir arrive, tout doux.",
        "maman|Le fil à linge s'endort, déjà.",
        "narrateur|Un bocal vide brille près de la porte.",
        "narrateur|Les dernières prunes pendent, toutes chaudes.",
        "enfant-f|Je fais un carillon, pour Nino.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-f|Oui, papa.",
        "narrateur|Nino est déjà dehors, quelque part.",
        "narrateur|En ce moment, Sarah tourne le bocal.",
        "maman|Il fait un petit toc, contre son pouce.",
        "papa|Merci, tu le tiens bien.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le prunier attend, tout calme.",
        "narrateur|Le bocal, le grelot, ou le ruban.",
        "papa|On commence par quoi, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bocal", "le grelot", "le ruban bleu")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = T1[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab(
            "le soleil de craie", "la coccinelle", "la sandale"
        )

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
        "Sarah veut un carillon au prunier, pour Nino, avant le vent du soir. "
        "T1 = bocal (table, verre qui tinte) / grelot (marche, son qui court) / "
        "ruban bleu (branche basse, boucle vide) : le voyage change. "
        "T2 = soleil de craie (trait à finir) / coccinelle (pas encore volée) / "
        "sandale (un pied nu). "
        "T3 = neuf résolutions : attendre le soleil, proposer tout bas, s'asseoir ; "
        "attendre l'envol, un grelot tout près, garder le carillon (accepter le non) ; "
        "aider la sandale, un tout petit regard, plus tard. "
        "La leçon se vit : elle propose, elle accepte oui, non, ou une autre idée. "
        "Fin : toc du verre, nœud bleu, prunier.",
        "N3 ≤ 16. Sara et le slogan « Inviter sans forcer » jetés. "
        "Autre récit que DIF-021 (pas de fort, pas de coussins), DIF-031 "
        "(pas de potager, pas de tomates), DIF-041 (pas de wagon, pas de mer) "
        "et DIF-049 (pas de poissons de papier, pas de tapis). "
        "Un merci de papa lié au geste (tenir le bocal). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
