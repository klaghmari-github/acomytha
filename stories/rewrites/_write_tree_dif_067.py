#!/usr/bin/env python3
"""TREE-DIF-067 — Le seau rond de Nino, au puits (N1, DIF.COR.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-067"
N1 = LIMITS["N1"]
TITLE = "Le seau rond de Nino, au puits"
FIL = (
    "Au puits du village, Nino veut remonter de l'eau pour la bassine de maman. "
    "Il prend d'abord le seau rond de bois, le seau mince en zinc ou la corde rêche ; "
    "les trois partent. La margelle glisse trop, l'auge est trop basse, "
    "la treille accroche la corde. Neuf façons de sentir le rond qui tient "
    "et le mince qui penche. L'eau tremble dans la bassine, on rentre."
)
CHARS = "Nino, papa, maman"
SETTING = "puits du village : mousse, margelle, auge, treille"


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
        "il faut attendre",
        "pommier",
        "pomme",
        "canard",
        "pain chaud",
        "le pain",
        "cheval",
        "auvent",
        "veau",
        "étable",
        "abreuvoir",
        "lampe",
        "capitaine",
        "plic",
        "volet jaune",
        "dînette",
        "dinette",
        "après la sieste",
        "sami",
        "cuisine",
        "chambre",
        "pull",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "puits" not in blob:
        raise SystemExit(f"{SID}: puits absent")
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
        "lab": "le seau rond",
        "ans": "seau rond",
        "acc": "seau rond | le seau rond | d'abord le seau rond | le bois | rond",
        "retry": "Nino a pris le seau rond, d'abord.",
        "hip": "L'anse de bois marque encore sa paume.",
        "wait": "Pendant ce temps, le bois reste droit.",
        "use": "Une goutte de bois tremble encore.",
        "coda": "Le seau rond sèche, une goutte au fond.",
    },
    2: {
        "lab": "le seau mince",
        "ans": "seau mince",
        "acc": "seau mince | le seau mince | d'abord le seau mince | le zinc | mince",
        "retry": "Nino a pris le seau mince, d'abord.",
        "hip": "Le zinc cliquette encore, contre sa jambe.",
        "wait": "Fermé, le zinc ne penche plus.",
        "use": "Une ligne de zinc brille, prête.",
        "coda": "Le zinc reste froid, une ligne d'eau.",
    },
    3: {
        "lab": "la corde",
        "ans": "corde",
        "acc": "corde | la corde | d'abord la corde | la corde rêche | rêche",
        "retry": "Nino a pris la corde, d'abord.",
        "hip": "La corde rêche gratte encore ses doigts.",
        "wait": "Lâche, la corde ne tire plus.",
        "use": "Un brin de corde reste mouillé.",
        "coda": "La corde pend, encore rêche, encore mouillée.",
    },
}

T3_LABS = {
    1: ("le seau rond", "tenir le mince", "attendre"),
    2: ("à deux", "la corde", "poser le rond"),
    3: ("décrocher", "attendre", "à deux"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord le seau rond.",
            "narrateur|Le bois est lourd, encore humide.",
            "enfant-m|Il tient bien, tout rond.",
            "maman|Le fond est large, tout calme.",
            "narrateur|Il pose le seau contre sa jambe.",
            "papa|Le mince de zinc attend, tout près.",
            "narrateur|La corde rêche pend, déjà froide.",
            "enfant-m|On les prend, tous.",
            "maman|Les trois partent, avec toi.",
            "narrateur|Rien ne reste près de la pierre.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino prend d'abord le seau mince.",
            "narrateur|Le zinc est froid, déjà cliquetant.",
            "enfant-m|Il penche un peu.",
            "papa|Le fond est étroit, tout léger.",
            "narrateur|Il le serre contre son ventre.",
            "maman|Le rond de bois attend, tout près.",
            "narrateur|La corde rêche pend, déjà froide.",
            "enfant-m|On les prend, tous.",
            "papa|Les trois partent, avec toi.",
            "narrateur|Rien ne reste près de la pierre.",
        )
    return L(
        "narrateur|Nino prend d'abord la corde rêche.",
        "narrateur|Elle gratte un peu, encore froide.",
        "enfant-m|Elle pique les doigts.",
        "maman|C'est pour descendre le seau.",
        "narrateur|Il enroule un tour, tout lent.",
        "papa|Le rond et le mince viennent aussi.",
        "narrateur|Maman les pose contre la pierre.",
        "enfant-m|Je garde la corde.",
        "maman|La corde d'abord, tu l'as.",
        "narrateur|Les trois affaires avancent avec lui.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le seau rond.",
            "papa|Oui.",
            "narrateur|Nino glisse le zinc sous le bras.",
            "maman|La corde, je te la tends.",
            "enfant-m|Elle gratte encore.",
            "narrateur|Les trois affaires tapent sa jambe.",
            "papa|On cherche l'endroit.",
            "enfant-m|Pour l'eau de maman.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Le seau mince.",
            "maman|Oui.",
            "narrateur|Il ramasse le bois, tout lourd.",
            "papa|La corde, dans l'autre main ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux seaux voyagent contre lui.",
            "maman|On cherche l'endroit.",
            "enfant-m|Pour l'eau de maman.",
        )
    return L(
        "enfant-m|La corde.",
        "papa|Oui.",
        "narrateur|Maman lui passe le seau rond.",
        "maman|Le mince, sous le bras.",
        "enfant-m|Il est là.",
        "narrateur|Le bois et le zinc avancent avec lui.",
        "papa|On cherche l'endroit.",
        "enfant-m|Pour l'eau de maman.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['hip']}",
        "narrateur|Devant, la margelle est trop glissante.",
        "narrateur|L'auge, elle, est trop basse.",
        "narrateur|Près de la treille, la corde s'accroche.",
        "papa|Nino, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    hip = OBJ[t1]["hip"]
    if t2 == 1:
        extra = {
            1: "L'anse de bois glisse déjà sur la mousse.",
            2: "Le zinc cliquette, trop léger, trop vite.",
            3: "La corde rêche frotte la pierre, trop mouillée.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|La margelle est trop glissante, trop verte.",
            f"narrateur|{extra}",
            "enfant-m|Le seau part de travers !",
            "narrateur|Le seau rond glisse, puis tient un peu.",
            "narrateur|Le mince de zinc penche, trop vite.",
            "enfant-m|L'eau ne monte pas.",
            "papa|Ici, la pierre n'arrête pas.",
            "maman|La mousse est trop mouillée.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois comment, Nino ?",
        )
    if t2 == 2:
        extra = {
            1: "Le bois bute le bord, trop large.",
            2: "Une goutte de zinc part déjà, trop vite.",
            3: "La corde traîne dans l'auge, trop longue.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|L'auge est trop basse, trop étroite.",
            f"narrateur|{extra}",
            "enfant-m|Je n'arrive pas à verser !",
            "narrateur|Le seau rond bute, trop large.",
            "narrateur|Le mince penche, et l'eau fuit.",
            "enfant-m|Ça va à côté.",
            "papa|Ici, c'est trop bas.",
            "maman|La bassine n'atteint pas.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois comment, Nino ?",
        )
    extra = {
        1: "L'anse de bois tape la vigne, trop large.",
        2: "Le zinc s'accroche, trop mince, trop vif.",
        3: "La corde rêche s'enroule autour d'une vrille.",
    }[t1]
    return L(
        f"narrateur|{hip}",
        "narrateur|Près de la treille, la corde s'accroche.",
        f"narrateur|{extra}",
        "enfant-m|La corde ne descend plus !",
        "narrateur|Une vrille de vigne tient le nœud.",
        "narrateur|Le seau rond pend, trop lourd.",
        "narrateur|Le mince tape la pierre, trop mince.",
        "enfant-m|L'eau reste en bas.",
        "papa|Ici, ça s'accroche trop.",
        "maman|La vigne tient trop.",
        "enfant-m|Alors on fait quoi ?",
        "papa|Tu vois comment, Nino ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La margelle n'a pas fini de glisser.",
            "papa|Le seau rond, tenir le mince, ou attendre ?",
        )
    if t2 == 2:
        return L(
            "narrateur|L'auge n'a pas fini d'être basse.",
            "maman|À deux, la corde, ou poser le rond ?",
        )
    return L(
        "narrateur|La corde n'a pas fini de s'accrocher.",
        "papa|Décrocher, attendre, ou à deux ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        pose = {
            1: "Nino pose le bois sur la pierre.",
            2: "Nino pose le zinc contre le bois.",
            3: "Nino pose la corde sur l'anse.",
        }[t1]
        return L(
            "enfant-m|Le seau rond, d'abord.",
            f"narrateur|{pose}",
            "narrateur|Le seau rond tient, tout calme.",
            "narrateur|Le mince de zinc attend, contre lui.",
            "enfant-m|Toi, tu restes droit.",
            "papa|Le rond a une assise, voilà.",
            "maman|Le mince, on le tiendra après.",
            f"narrateur|{o['use']}",
        )
    if t2 == 1 and t3 == 2:
        hold = {
            1: "Ses deux mains serrent le bois aussi.",
            2: "Ses deux mains serrent le zinc.",
            3: "La corde l'aide à serrer le zinc.",
        }[t1]
        return L(
            "enfant-m|Je tiens le mince.",
            f"narrateur|{hold}",
            "narrateur|Le mince penche, puis se redresse.",
            "narrateur|Le seau rond reste, tout seul, tout large.",
            "enfant-m|Tu ne glisses plus.",
            "papa|Tu l'as tenu, tout près.",
            "maman|Deux formes, une même eau.",
            f"narrateur|{o['use']}",
        )
    if t2 == 1 and t3 == 3:
        wait = {
            1: "Nino tient le bois, sans bouger encore.",
            2: "Nino tient le zinc, sans verser encore.",
            3: "Nino tient la corde, sans tirer encore.",
        }[t1]
        return L(
            "enfant-m|On attend un peu.",
            f"narrateur|{wait}",
            "narrateur|Une goutte quitte la mousse, puis plus.",
            "narrateur|La pierre redevient un peu moins glissante.",
            "enfant-m|Maintenant, ça tient.",
            "papa|La mousse s'est tue, maintenant.",
            "maman|Tu as laissé la pierre se calmer.",
            f"narrateur|{o['wait']}",
        )
    if t2 == 2 and t3 == 1:
        two = {
            1: "Papa tient le seau rond, tout large.",
            2: "Papa tient le zinc, trop mince.",
            3: "Papa tient la corde, Nino le bois.",
        }[t1]
        return L(
            "enfant-m|À deux, on verse.",
            f"narrateur|{two}",
            "narrateur|Nino guide le mince, qui penche.",
            "narrateur|L'eau tombe dans l'auge, tout droit.",
            "enfant-m|Les deux, ensemble.",
            "papa|Tes mains ont aidé les miennes.",
            "maman|Le rond tient, le mince verse.",
            f"narrateur|{o['use']}",
        )
    if t2 == 2 and t3 == 2:
        knot = {
            1: "Nino noue la corde au seau rond.",
            2: "Nino noue la corde au zinc mince.",
            3: "Nino noue la corde, déjà dans ses mains.",
        }[t1]
        return L(
            "enfant-m|La corde, pour descendre.",
            f"narrateur|{knot}",
            "narrateur|Le bois descend, sans pencher.",
            "narrateur|Le mince suit, tenu par le nœud.",
            "enfant-m|Tu vas jusqu'en bas.",
            "papa|La corde a gardé les deux.",
            "maman|Le rond ne se couche pas.",
            f"narrateur|{o['use']}",
        )
    if t2 == 2 and t3 == 3:
        sit = {
            1: "Le seau rond s'assoit dans l'auge.",
            2: "Le zinc attend, le bois s'assoit.",
            3: "La corde lâche, le bois s'assoit.",
        }[t1]
        return L(
            "enfant-m|On pose le rond, d'abord.",
            f"narrateur|{sit}",
            "narrateur|Il tient, tout large, tout calme.",
            "narrateur|Nino y verse le mince, tout doux.",
            "enfant-m|Toi, tu reçois.",
            "papa|Le rond fait bassine, un moment.",
            "maman|Le mince a pu pencher, sans perdre.",
            f"narrateur|{o['use']}",
        )
    if t2 == 3 and t3 == 1:
        free = {
            1: "Nino glisse la corde hors de la vrille.",
            2: "Le zinc se libère, puis la corde.",
            3: "Nino glisse la corde, doigt par doigt.",
        }[t1]
        return L(
            "enfant-m|On décroche, d'abord.",
            f"narrateur|{free}",
            "narrateur|Le seau rond redescend, tout lourd.",
            "narrateur|Le mince penche, puis se calme.",
            "enfant-m|Tu es libre, corde.",
            "papa|Tu n'as pas tiré trop fort.",
            "maman|La vigne a lâché, toute seule.",
            f"narrateur|{o['use']}",
        )
    if t2 == 3 and t3 == 2:
        still = {
            1: "Nino tient le bois, sans tirer.",
            2: "Nino tient le zinc, sans tirer.",
            3: "Nino tient la corde, sans tirer.",
        }[t1]
        return L(
            "enfant-m|On attend la vigne.",
            f"narrateur|{still}",
            "narrateur|La vrille va, revient, puis lâche.",
            "narrateur|Le seau rond pend, enfin droit.",
            "enfant-m|Maintenant, tu descends.",
            "papa|La treille n'a plus accroché.",
            "maman|Tu as laissé la vigne finir.",
            f"narrateur|{o['wait']}",
        )
    lift = {
        1: "Papa lève la vrille, Nino le bois.",
        2: "Papa lève la vrille, Nino le zinc.",
        3: "Papa lève la vrille, Nino la corde.",
    }[t1]
    return L(
        "enfant-m|À deux, on libère.",
        f"narrateur|{lift}",
        "narrateur|Nino tire la corde, tout calme.",
        "narrateur|Le seau rond passe, puis le mince.",
        "enfant-m|Vous deux, vous descendez.",
        "papa|Tes mains ont tiré, les miennes ont levé.",
        "maman|Le rond et le mince, ensemble.",
        f"narrateur|{o['use']}",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|L'eau tremble dans la bassine, tout ronde.",
            "enfant-m|On a posé le seau rond.",
            "papa|Le rond a tenu, sur la pierre.",
            "maman|On rentre, maintenant.",
            f"narrateur|{coda}",
            "narrateur|Une mousse verte reste, plus loin.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Dans la bassine, l'eau fait un rond.",
            "enfant-m|J'ai tenu le mince.",
            "papa|Tu l'as tenu, tout près.",
            "maman|Essuie tes mains, on rentre.",
            f"narrateur|{coda}",
            "narrateur|La margelle se tait, encore humide.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|L'eau est arrivée, toute calme, toute froide.",
            "enfant-m|On a attendu la pierre.",
            "papa|La mousse s'est tue.",
            "maman|La bassine est pleine, on rentre.",
            f"narrateur|{coda}",
            "narrateur|Une goutte quitte encore la margelle.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|La bassine reçoit l'eau, un peu froide.",
            "enfant-m|On a versé à deux.",
            "papa|Tes mains ont aidé.",
            "maman|Le rond et le mince, tous les deux.",
            f"narrateur|{coda}",
            "narrateur|L'auge garde une flaque, tout bas.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|De l'auge, l'eau rejoint la bassine.",
            "enfant-m|La corde a descendu les deux.",
            "papa|La corde a gardé les deux.",
            "maman|On rentre, tes doigts sont froids.",
            f"narrateur|{coda}",
            "narrateur|Un nœud reste mouillé, contre le zinc.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Le seau rond a versé, tout doux.",
            "enfant-m|Il a reçu le mince.",
            "papa|Le rond a fait bassine.",
            "maman|Vos manches sentent encore l'eau.",
            f"narrateur|{coda}",
            "narrateur|L'auge se tait, plus loin, tout basse.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Quand la corde a lâché, l'eau a monté.",
            "enfant-m|On a décroché la vrille.",
            "papa|Tu n'as pas tiré trop fort.",
            "maman|La bassine tremble, on rentre.",
            f"narrateur|{coda}",
            "narrateur|Une feuille de vigne reste, trop verte.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Quand la vigne s'est tue, l'eau a monté.",
            "enfant-m|On a attendu la treille.",
            "papa|La treille n'a plus accroché.",
            "maman|Tes doigts sentent encore la corde.",
            f"narrateur|{coda}",
            "narrateur|La vrille se recouche, tout lentement.",
        )
    return L(
        "narrateur|À deux, l'eau a rejoint la bassine.",
        "enfant-m|Papa a levé, j'ai tiré.",
        "papa|Tes mains ont tiré.",
        "maman|On rentre, la bassine est froide.",
        f"narrateur|{coda}",
        "narrateur|La treille se tait, plus loin, toute seule.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Au milieu du village, le puits garde l'ombre.",
        "narrateur|La mousse est froide, sur la pierre.",
        "narrateur|Un seau cliquette, tout bas.",
        "papa|Tu entends le seau, Nino ?",
        "enfant-m|Oui, il cliquette.",
        "narrateur|L'ombre du puits sent l'eau.",
        "maman|La bassine est vide, à la maison.",
        "enfant-m|Je veux remonter de l'eau.",
        "papa|Pour la bassine de maman ?",
        "enfant-m|Oui, avec le bon seau.",
        "narrateur|En ce moment, Nino touche la pierre.",
        "narrateur|La mousse colle un peu, toute verte.",
        "enfant-m|Elle est froide.",
        "maman|Deux seaux attendent, près de la corde.",
        "papa|Un rond de bois, un mince de zinc.",
        "papa|Merci, tu as vu les deux.",
        "enfant-m|On prépare, d'abord.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du puits.",
        "narrateur|Le seau rond, le seau mince, la corde.",
        "maman|Tu commences par laquelle ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le seau rond", "le seau mince", "la corde")

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
        extras[f"{p}_T0002_P0000"] = t3lab("la margelle", "l'auge", "la treille")

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
        "Puits du village, mousse froide, seau qui cliquette, ombre d'eau. "
        "Nino veut remonter de l'eau pour la bassine de maman, avec le bon seau. "
        "T1 = seau rond de bois / seau mince en zinc / corde rêche (les trois partent). "
        "T2 = margelle trop glissante / auge trop basse / treille qui accroche. "
        "T3 = neuf gestes (seau rond, tenir le mince, attendre ; "
        "à deux, la corde, poser le rond ; décrocher, attendre, à deux). "
        "La leçon se vit : le rond tient, le mince penche, l'eau arrive quand même. "
        "Fin : l'eau tremble dans la bassine, on rentre.",
        "N1 ≤ 10. Slogan « Plus rond ou plus mince — sous le pommier » jeté. "
        "Monde unique : puits, pas pommier (014/024/053), pas pain (040/043), "
        "pas pull/pommes (002), pas cheval/auvent (038), pas lait/veau (040), "
        "pas camp/lampe (047). Merci de papa (les deux seaux vus). "
        "chunk_id inchangés. check() N1. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
