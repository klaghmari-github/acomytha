#!/usr/bin/env python3
"""TREE-DIF-064 — Le cerf-volant d'Amir, sur la dune (N3, DIF.BES.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-064"
N3 = 16
TITLE = "Le cerf-volant d'Amir, sur la dune"
FIL = (
    "Au bord de la mer, Amir veut que son cerf-volant rouge voie la mer, "
    "avant que le vent se couche. Il prend d'abord le cerf-volant, la ficelle "
    "ou le piquet ; les trois viennent. La crête souffle trop, l'herbe accroche "
    "trop, l'écume mouille trop. Neuf façons de laisser du temps. Le rouge vole."
)
CHARS = "Amir, papa, maman"
SETTING = "bord de mer : cabanes, dune, crête, herbe, écume"


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
        "hugo",
        "kenzo",
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
        "escargot",
        "balcon",
        "veau",
        "étable",
        "abreuvoir",
        "le four",
        "marché",
        "fort de coussins",
        "étoile",
        "bulle",
        "bronze",
        "tilleul",
        "moulinet",
        "carrousel",
        "marelle",
        "pain",
        "zoé",
        "zoe",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "cerf-volant" not in blob:
        raise SystemExit(f"{SID}: cerf-volant absent")
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
        "lab": "le cerf-volant",
        "ans": "cerf-volant",
        "acc": "cerf-volant | le cerf-volant | d'abord le cerf-volant | le tissu | le rouge",
        "retry": "Amir prend le cerf-volant d'abord.",
        "coda": "Le tissu rouge sèche près du seau, un pli encore salé.",
        "hip": "Entre ses doigts, le tissu rouge est déjà chaud.",
        "wait": "Pendant ce temps, le tissu reste plié, sage.",
        "use": "Un coin du tissu cherche encore l'air.",
    },
    2: {
        "lab": "la ficelle",
        "ans": "ficelle",
        "acc": "ficelle | la ficelle | d'abord la ficelle | le fil",
        "retry": "Amir prend la ficelle d'abord.",
        "coda": "La ficelle reste enroulée, un bout encore collant de sel.",
        "hip": "Au poignet, la ficelle colle un peu, de sel.",
        "wait": "Enroulée, la ficelle attend contre sa manche.",
        "use": "Un bout de ficelle brille, prêt à tenir.",
    },
    3: {
        "lab": "le piquet",
        "ans": "piquet",
        "acc": "piquet | le piquet | d'abord le piquet | le bois",
        "retry": "Amir prend le piquet d'abord.",
        "coda": "Le piquet garde un peu de sable, près du fil.",
        "hip": "Dans sa paume, le bois du piquet est tiède.",
        "wait": "Planté, le piquet reste droit, sans bouger.",
        "use": "La pointe du piquet attend le sable.",
    },
}

T3_LABS = {
    1: ("plus bas", "attendre", "de côté"),
    2: ("plus court", "à genoux", "le sable"),
    3: ("plus haut", "après la vague", "loin de l'eau"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir déplie d'abord le cerf-volant, encore tiède.",
            "enfant-m|Toi, tu vas voir la mer.",
            "maman|Tiens le nez, pas la queue.",
            "narrateur|La queue rouge claque une fois, puis se tait.",
            "papa|Ta queue me chatouille le cou.",
            "enfant-m|Elle est trop contente.",
            "narrateur|Maman glisse la ficelle contre son poignet.",
            "narrateur|Le piquet roule contre son genou, tout lourd.",
            "enfant-m|Nez en avant, queue derrière.",
            "papa|Le rouge est à toi, maintenant.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir enroule d'abord la ficelle, autour du poignet.",
            "enfant-m|Tu vas tenir le rouge.",
            "papa|Pas trop serré, laisse un peu d'air.",
            "narrateur|Un tour glisse, puis tient.",
            "maman|Tu m'as fait un anneau, tout doux.",
            "enfant-m|C'est pour tenir.",
            "narrateur|Papa pose le tissu plié contre le seau.",
            "narrateur|Le piquet attend, planté un peu, déjà.",
            "enfant-m|Fil, tu restes avec moi.",
            "maman|La ficelle est prête, tu peux y aller.",
        )
    return L(
        "narrateur|Amir lève d'abord le piquet, le bois encore chaud.",
        "enfant-m|Tu vas tenir le fil.",
        "maman|Pointe vers le bas, tout doux.",
        "narrateur|Le bois tape le sable, un toc.",
        "papa|Il a tracé une ligne, comme un serpent.",
        "enfant-m|C'est le chemin.",
        "narrateur|Maman glisse le tissu sous son autre bras.",
        "narrateur|La ficelle pend, déjà, contre sa manche.",
        "enfant-m|Piquet, je te porte.",
        "papa|Le piquet est prêt, on avance.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|Le tissu rouge reste contre sa poitrine, encore chaud.",
            "enfant-m|On va jusqu'à la dune.",
            "maman|Le vent n'attendra pas longtemps.",
            "papa|Tu tiens bien, Amir ?",
            "enfant-m|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|La ficelle fait un bracelet lâche, au poignet.",
            "enfant-m|Elle va tenir le rouge.",
            "papa|Ça sent encore le sel, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un tour se desserre, puis se tait.",
        )
    return L(
        "narrateur|Le piquet reste contre son bras, encore lourd.",
        "enfant-m|Il va tenir le fil.",
        "maman|Le bois sent encore le soleil.",
        "papa|On y va, tous les trois ?",
        "enfant-m|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le tissu tape sa poitrine, tout bas.",
        2: "La ficelle frotte son poignet, un peu serrée.",
        3: "Le piquet tape son bras, tout doux.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Devant, la crête soulève trop de vent.",
        "narrateur|L'herbe, elle, accroche encore les fils.",
        "narrateur|Plus bas, l'écume mouille déjà le sable.",
        "papa|Amir, vous partez où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le tissu se tord, trop vite, trop fort.",
            2: "La ficelle siffle, trop tendue, trop vive.",
            3: "Le piquet penche, trop léger dans l'air.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|La crête de la dune souffle trop fort.",
            f"narrateur|{extra}",
            "enfant-m|Il va se déchirer !",
            "narrateur|La queue claque trop, encore une fois.",
            "narrateur|Le nez rouge se plie, trop pris.",
            "papa|Ici, le vent est trop grand.",
            "maman|Le rouge a besoin d'un vent plus doux.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois comment, Amir ?",
        )
    if t2 == 2:
        extra = {
            1: "Un pli du tissu s'accroche, trop serré.",
            2: "La ficelle fait un nœud, trop vite.",
            3: "Le piquet disparaît dans l'herbe, trop caché.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|L'herbe de la dune tient trop, trop verte.",
            f"narrateur|{extra}",
            "enfant-m|Le fil est coincé !",
            "narrateur|Une tige tire, puis une autre.",
            "narrateur|Le rouge n'a plus d'air, trop bas.",
            "papa|Ici, ça s'accroche trop.",
            "maman|Le fil n'avance plus.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois comment, Amir ?",
        )
    extra = {
        1: "Le tissu pèse, trop lourd, trop salé.",
        2: "La ficelle goutte, trop mouillée, trop froide.",
        3: "Le piquet s'enfonce, trop mou dans le sable.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|L'écume lèche le sable, trop près.",
        f"narrateur|{extra}",
        "enfant-m|Il est tout mouillé !",
        "narrateur|Une vague revient, trop blanche.",
        "narrateur|Le rouge n'a plus de vent, trop lourd.",
        "papa|Ici, ça mouille trop.",
        "maman|Il lui faut du temps, et du sec.",
        "enfant-m|Alors on fait quoi ?",
        "papa|Tu vois comment, Amir ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La crête n'a pas fini de souffler.",
            "papa|Plus bas, attendre, ou de côté ?",
        )
    if t2 == 2:
        return L(
            "narrateur|L'herbe n'a pas fini d'accrocher.",
            "maman|Plus court, à genoux, ou le sable ?",
        )
    return L(
        "narrateur|L'écume n'a pas fini de lécher.",
        "papa|Plus haut, après la vague, ou loin de l'eau ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        low = {
            1: "Il baisse le tissu, loin de la crête.",
            2: "Il baisse la ficelle, loin de la crête.",
            3: "Il plante le piquet plus bas, loin de la crête.",
        }[t1]
        return L(
            "enfant-m|Plus bas, d'abord.",
            f"narrateur|{low}",
            "narrateur|Amir descend la pente, les genoux au sable.",
            "narrateur|L'air est plus doux, contre la dune.",
            f"narrateur|{o['use']}",
            "papa|Tu as regardé le vent, avant.",
            "enfant-m|Ici, tu ne te déchires plus.",
            "maman|Plus bas, ça tenait mieux.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "Il tient le tissu contre lui, sans le lancer.",
            2: "Il tient la ficelle, sans la dérouler encore.",
            3: "Il tient le piquet, sans le planter encore.",
        }[t1]
        return L(
            "enfant-m|On attend le vent.",
            f"narrateur|{wait}",
            "narrateur|Le souffle passe, une fois, puis plus.",
            "enfant-m|Tu peux partir, maintenant.",
            f"narrateur|{o['wait']}",
            "papa|Le vent s'est tu, maintenant.",
            "narrateur|Le rouge se lève, tout calme.",
            "maman|Le rouge a eu son calme.",
        )
    if t2 == 1 and t3 == 3:
        side = {
            1: "Il tourne le tissu de côté, tout doux.",
            2: "Il tourne la ficelle de côté, tout doux.",
            3: "Il plante le piquet de côté, tout doux.",
        }[t1]
        return L(
            "enfant-m|De côté, pas face au vent.",
            f"narrateur|{side}",
            "narrateur|Le nez rouge prend moins d'air, déjà.",
            "narrateur|Amir compte tout bas, un, deux.",
            f"narrateur|{o['wait']}",
            "papa|De côté, ça n'a pas trop tiré.",
            "enfant-m|Tu es à l'abri.",
            "maman|Le nez a moins tiré, comme ça.",
        )
    if t2 == 2 and t3 == 1:
        short = {
            1: "Il tient le tissu tout près, ficelle courte.",
            2: "Il déroule peu de ficelle, tout court.",
            3: "Il plante le piquet tout près, fil court.",
        }[t1]
        return L(
            "enfant-m|Plus court, d'abord.",
            f"narrateur|{short}",
            "narrateur|L'herbe n'atteint plus le fil, trop loin.",
            "narrateur|Le rouge se lève, tout petit, déjà.",
            f"narrateur|{o['wait']}",
            "maman|Le fil n'a plus accroché.",
            "enfant-m|Maintenant, tu me vois.",
            "papa|Tu as commencé tout près.",
        )
    if t2 == 2 and t3 == 2:
        knee = {
            1: "À genoux, il dénoue le tissu, tout doux.",
            2: "À genoux, il dénoue la ficelle, tout doux.",
            3: "À genoux, il dégage le piquet, tout doux.",
        }[t1]
        return L(
            "enfant-m|À genoux, on dénoue.",
            f"narrateur|{knee}",
            "narrateur|Un nœud lâche, puis un autre.",
            "narrateur|L'herbe se tait, plus loin, toute seule.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas tiré trop fort.",
            "enfant-m|C'est pour toi.",
            "maman|Le nœud a lâché tout seul.",
        )
    if t2 == 2 and t3 == 3:
        sand = {
            1: "Sur le sable nu, le tissu ne s'accroche plus.",
            2: "Sur le sable nu, la ficelle ne s'accroche plus.",
            3: "Sur le sable nu, le piquet trouve sa place.",
        }[t1]
        return L(
            "enfant-m|Le sable, pas l'herbe.",
            "narrateur|Amir recule vers le sable nu, tout doux.",
            f"narrateur|{sand}",
            "narrateur|Plus de tiges, plus de nœuds.",
            f"narrateur|{o['wait']}",
            "papa|Tu t'es mis où c'est vide.",
            "enfant-m|Le fil est libre.",
            "maman|Le sable nu était plus simple.",
        )
    if t2 == 3 and t3 == 1:
        high = {
            1: "Plus haut, le tissu n'a plus d'écume.",
            2: "Plus haut, la ficelle n'a plus d'écume.",
            3: "Plus haut, le piquet n'a plus d'eau.",
        }[t1]
        return L(
            "enfant-m|Plus haut, d'abord.",
            f"narrateur|{high}",
            "narrateur|Amir gravit la dune, le sable qui glisse.",
            "narrateur|L'écume reste en bas, trop loin pour lécher.",
            f"narrateur|{o['wait']}",
            "papa|La vague n'a plus touché.",
            "enfant-m|Maintenant, tu peux rester.",
            "maman|Le sable était plus sec, là-haut.",
        )
    if t2 == 3 and t3 == 2:
        wave = {
            1: "Il tient le tissu, puis attend la vague.",
            2: "Il tient la ficelle, puis attend la vague.",
            3: "Il tient le piquet, puis attend la vague.",
        }[t1]
        return L(
            "enfant-m|On attend la vague, d'abord.",
            f"narrateur|{wave}",
            "narrateur|L'eau va, revient, puis se tait.",
            "narrateur|Le sable redevient ferme, tout net.",
            f"narrateur|{o['use']}",
            "papa|Tu n'as pas couru dans l'eau.",
            "enfant-m|Tu es sec, maintenant.",
            "maman|Tu as laissé la vague finir.",
        )
    far = {
        1: "Loin de l'eau, le tissu reste sec, tout rouge.",
        2: "Loin de l'eau, la ficelle reste sèche, déjà.",
        3: "Loin de l'eau, le piquet tient, sans s'enfoncer.",
    }[t1]
    return L(
        "enfant-m|Loin de l'eau, tout sec.",
        f"narrateur|{far}",
        "narrateur|Amir recule vers les cabanes, tout doux.",
        "narrateur|L'écume se tait, plus loin, toute seule.",
        f"narrateur|{o['wait']}",
        "papa|Le sec était assez large.",
        "enfant-m|Tu restes, rouge.",
        "maman|Loin de l'eau, ça suffisait.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Plus bas, le cerf-volant voit la mer, tout calme.",
            "enfant-m|On s'est baissés, d'abord.",
            "papa|Tu as regardé le vent avant de lancer.",
            "maman|Essuie tes genoux, sur le maillot.",
            f"narrateur|{coda}",
            "narrateur|Un carré rouge reste dans le ciel, puis pâlit.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Quand le vent s'est tu, le rouge a vu la mer.",
            "enfant-m|On a attendu le souffle.",
            "papa|Merci d'avoir laissé le vent se taire.",
            "maman|Rentrez, le pin sent encore le chaud.",
            f"narrateur|{coda}",
            "narrateur|Une poussière de sable tourne, puis s'arrête.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|De côté, le cerf-volant tient, sans se tordre.",
            "enfant-m|Je n'ai pas fait face.",
            "papa|De côté, ça n'a pas trop tiré.",
            "maman|Le bois des cabanes est retombé, plus loin.",
            f"narrateur|{coda}",
            "narrateur|La mer se tait, derrière le tissu tiède.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Tout près, le rouge a repris l'air, déjà.",
            "enfant-m|On a commencé tout court.",
            "papa|Le silence vous a aidés.",
            "maman|L'herbe sent encore le sel, moins fort.",
            f"narrateur|{coda}",
            "narrateur|Un brin d'herbe se recouche, tout lent.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Quand le nœud s'est tu, le rouge a volé.",
            "enfant-m|On a dénoué, à genoux.",
            "papa|Tu n'as pas tiré trop fort.",
            "maman|Le fil a parlé tout seul.",
            f"narrateur|{coda}",
            "narrateur|Un carré net reste dans le ciel, puis pâlit.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sur le sable nu, le rouge touche déjà le bleu.",
            "enfant-m|Je me suis mis où c'est vide.",
            "papa|Tu t'es glissé, comme le vent.",
            "maman|Vous rentrez, les mains pleines de sable.",
            f"narrateur|{coda}",
            "narrateur|L'herbe reste derrière, sans accrocher.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Plus haut, le cerf-volant a tenu, tout sec.",
            "enfant-m|On a gravi la dune.",
            "papa|La vague n'a plus touché.",
            "maman|Vos manches sentent encore le sel.",
            f"narrateur|{coda}",
            "narrateur|Un grain de sable sèche sur le bois, puis plus.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Après la vague, le rouge a vu la mer, déjà.",
            "enfant-m|On a attendu que ça se taise.",
            "papa|Tu n'as pas couru dans l'eau.",
            "maman|Tes doigts sentent encore le sel.",
            f"narrateur|{coda}",
            "narrateur|La vague reste à sa place, plus loin.",
        )
    return L(
        "narrateur|Loin de l'eau, le rouge tient, tout calme.",
        "enfant-m|On a reculé vers les cabanes.",
        "papa|Le sec était assez large.",
        "maman|Rentrez, le maillot est déjà sec.",
        f"narrateur|{coda}",
        "narrateur|L'écume se tait, plus loin, toute seule.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Un grain de sel brille sur le bois de la cabane.",
        "narrateur|Le fil du linge tape, tout petit.",
        "narrateur|Ça sent le pin chaud, et la mer.",
        "papa|Tu as vu la queue, Amir ?",
        "enfant-m|Elle tape déjà la marche.",
        "maman|C'est le cerf-volant, encore rouge.",
        "narrateur|En ce moment, Amir déplie un coin du tissu.",
        "enfant-m|Je veux qu'il voie la mer.",
        "papa|Le vent va se coucher bientôt.",
        "maman|On prend les affaires, alors ?",
        "papa|Merci, tu as dénoué la ficelle.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du sable.",
        "narrateur|Le cerf-volant, la ficelle, et le piquet.",
        "maman|Tu prends quoi d'abord, Amir ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le cerf-volant", "la ficelle", "le piquet")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Amir a pris {o['lab']} d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la crête", "l'herbe", "l'écume")

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
        "Cabanes de bois, grain de sel, fil du linge, pin chaud. "
        "Amir veut que son cerf-volant rouge voie la mer, avant que le vent se couche. "
        "T1 = cerf-volant / ficelle / piquet (les trois viennent). "
        "T2 = crête trop venteuse / herbe trop accrochante / écume trop mouillée. "
        "T3 = neuf résolutions (plus bas, attendre, de côté ; plus court, à genoux, sable ; "
        "plus haut, après la vague, loin de l'eau). La leçon se vit : il attend, "
        "il compte, il lance quand le vent se tait. Fin : le rouge vole.",
        "N3 ≤ 16. Slogan « Plus de temps ou de calme », Hugo, Tom/Léa/Sami, "
        "bac/toboggan/balançoires, « bon travail », calque AUT-001 jetés. "
        "Récit autre que DIF-020 (escargot/balcon), DIF-030 (pain/four), "
        "DIF-040 (veau/ferme), DIF-048 (étoile/fenêtre), DIF-056 (bulle/bronze). "
        "Merci de papa (ficelle dénouée). Relecture : morales collées "
        "(« laissé le temps », « observé d'abord », « parlé lentement ») "
        "remplacées par des faits vus. chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-064.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
