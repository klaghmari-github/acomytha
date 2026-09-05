#!/usr/bin/env python3
"""TREE-DIF-069 — Le camion de carton de Raphaël, dans la cave (N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-069"
N2 = 15
TITLE = "Le camion de carton de Raphaël, dans la cave"
FIL = (
    "Dans la cave, Raphaël veut monter un camion en carton pour descendre "
    "une pomme, avec Chouchou. Elle répond avec les mains. "
    "T1 = grand carton / crayon gras / ficelle, les trois partent. "
    "T2 = râtelier (pommes qui roulent) / marche trop étroite / "
    "coin de l'ampoule (ombre, Chouchou s'arrête). "
    "T3 = neuf façons. Le camion glisse, une pomme dessus, on remonte."
)
CHARS = "Raphaël, Chouchou, papa, maman"
SETTING = "cave sous la maison : râtelier de pommes, marche, ampoule jaune"


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
        "parle peu",
        "parlé peu",
        "camarade",
        "timide",
        "forcer la parole",
        "un camarade",
        "dînette",
        "dinette",
        "après la sieste",
        "cuisine",
        "nichoir",
        "locomotive",
        "gare en carton",
        "cuillère",
        "véranda",
        "petite roue",
        "galet",
        "lina",
        "merle",
        "capitaine",
        "bac à sable",
        "toboggan",
        "balançoire",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
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
        "lab": "le carton",
        "ans": "carton",
        "acc": "carton | le carton | le grand carton | d'abord le carton",
        "retry": "Raphaël prend le carton d'abord.",
        "coda": "Le grand carton garde un peu de poussière.",
        "hip": "Le carton racle encore sous ses mains.",
        "wait": "Le carton reste plat, sans bouger.",
        "use": "Le carton attend, déjà en forme de camion.",
    },
    2: {
        "lab": "le crayon",
        "ans": "crayon",
        "acc": "crayon | le crayon | le crayon gras | d'abord le crayon",
        "retry": "Raphaël prend le crayon d'abord.",
        "coda": "Le crayon gras a laissé un trait jaune.",
        "hip": "Le crayon gras chauffe un peu dans sa main.",
        "wait": "Le crayon reste contre le carton, tout calme.",
        "use": "Un trait de crayon montre encore une roue.",
    },
    3: {
        "lab": "la ficelle",
        "ans": "ficelle",
        "acc": "ficelle | la ficelle | le fil | d'abord la ficelle",
        "retry": "Raphaël prend la ficelle d'abord.",
        "coda": "La ficelle pend encore, un peu tordue.",
        "hip": "La ficelle gratte un peu sa paume.",
        "wait": "La ficelle reste enroulée, tout calme.",
        "use": "Un bout de ficelle sert déjà de corde.",
    },
}

T3_LABS = {
    1: ("les pommes", "le bas", "son doigt"),
    2: ("le bord", "de côté", "sa main"),
    3: ("la lumière", "son ombre", "son mot"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Raphaël prend d'abord le grand carton.",
            "enfant-m|Il va devenir un camion.",
            "papa|Plie le bord, tout doux.",
            "narrateur|Le carton racle, puis se plie.",
            "enfant-m|Dis camion, Chouchou !",
            "narrateur|Chouchou tape deux fois le fond, tout net.",
            "narrateur|Le crayon et la ficelle glissent près d'elle.",
            "maman|Les trois viennent, déjà.",
            "narrateur|Papa pose le crayon contre le carton.",
            "narrateur|La ficelle s'enroule autour d'un coin.",
            "enfant-m|Chouchou, tu viens ?",
            "narrateur|Elle pousse le carton vers le râtelier.",
            "papa|Le carton d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Raphaël prend d'abord le crayon gras.",
            "enfant-m|Il va dessiner les roues.",
            "maman|Un trait, pas tout le crayon.",
            "narrateur|Un cercle jaune apparaît, un peu gras.",
            "enfant-m|Dis roue, Chouchou !",
            "narrateur|Chouchou trace un rond, avec le doigt.",
            "narrateur|Le carton et la ficelle glissent près d'eux.",
            "papa|Les trois viennent, déjà.",
            "narrateur|Maman glisse le carton sous le crayon.",
            "narrateur|La ficelle sert déjà de corde.",
            "enfant-m|Chouchou, c'est ta roue ?",
            "narrateur|Elle appuie le doigt au centre, tout calme.",
            "maman|Le crayon d'abord, vous l'avez.",
        )
    return L(
        "narrateur|Raphaël prend d'abord la ficelle beige.",
        "enfant-m|Elle va tirer le camion.",
        "papa|Un nœud, pas trop serré.",
        "narrateur|La ficelle gratte, puis tient.",
        "enfant-m|Dis corde, Chouchou !",
        "narrateur|Chouchou enroule un tour, sans un mot.",
        "narrateur|Le carton et le crayon glissent près d'elle.",
        "maman|Les trois viennent, déjà.",
        "narrateur|Papa pose le carton contre la marche.",
        "narrateur|Le crayon reste au bord, tout gras.",
        "enfant-m|Chouchou, tu tiens ?",
        "narrateur|Elle tend la ficelle, tout calme.",
        "papa|La ficelle d'abord, vous l'avez.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|Le carton reste contre eux, déjà plié.",
            "enfant-m|On va chercher une pomme.",
            "narrateur|Chouchou pose une main dessus, tout plat.",
            "maman|Le râtelier n'est pas loin.",
            "papa|Tu tiens bien, Raphaël ?",
            "enfant-m|Oui, papa.",
            f"narrateur|{o['use']}",
        )
    if t1 == 2:
        return L(
            "narrateur|Le crayon pend un peu, encore gras.",
            "enfant-m|Les roues sont là.",
            "narrateur|Chouchou garde le carton contre son genou.",
            "papa|Ça sent encore le bois, ici.",
            "maman|Tes mains sont prêtes ?",
            "enfant-m|Oui, maman.",
            f"narrateur|{o['use']}",
        )
    return L(
        "narrateur|La ficelle reste enroulée, contre sa paume.",
        "enfant-m|Elle va tirer.",
        "narrateur|Chouchou tient le bout, tout près.",
        "maman|Le nœud sent encore le tiroir.",
        "papa|On avance, tous les deux ?",
        "enfant-m|Oui.",
        f"narrateur|{o['use']}",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['hip']}",
        "narrateur|Devant, le râtelier laisse rouler des pommes.",
        "narrateur|La marche, elle, est trop étroite pour le carton.",
        "narrateur|Sous l'ampoule, une ombre arrête Chouchou.",
        "papa|Raphaël, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le carton tremble, trop vite, trop fort.",
            2: "Le crayon saute, trop sec, trop vite.",
            3: "La ficelle se tend, trop vite, trop fort.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Une pomme tombe du râtelier, puis une autre.",
            f"narrateur|{extra}",
            "enfant-m|Attrape, Chouchou !",
            "narrateur|Chouchou montre une pomme, du doigt.",
            "narrateur|Les pommes roulent encore, trop vite.",
            "papa|Ici, ça n'arrête pas.",
            "maman|Elle montre déjà, avec le doigt.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois comment, Raphaël ?",
        )
    if t2 == 2:
        extra = {
            1: "Le carton plie, trop large, trop raide.",
            2: "Le crayon tombe, trop près de la marche.",
            3: "La ficelle se coince, trop large encore.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|La marche de pierre pince le carton, trop large.",
            f"narrateur|{extra}",
            "enfant-m|Pousse, Chouchou !",
            "narrateur|Le carton reste coincé, trop large.",
            "narrateur|Chouchou s'arrête, les deux mains à plat.",
            "papa|Ici, c'est trop étroit.",
            "maman|Le camion n'arrive pas.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois comment, Raphaël ?",
        )
    extra = {
        1: "Le carton s'arrête, trop près de l'ombre.",
        2: "Le crayon glisse, trop pris par l'ombre.",
        3: "La ficelle se tait, trop près de l'ombre.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|L'ampoule jaune laisse un coin d'ombre.",
        f"narrateur|{extra}",
        "enfant-m|Viens, Chouchou !",
        "narrateur|Chouchou s'arrête, collée à la lumière.",
        "narrateur|L'ombre tremble un peu, trop noire.",
        "papa|Ici, ça fait trop d'ombre.",
        "maman|Elle reste près de la lumière.",
        "enfant-m|Alors on fait quoi ?",
        "papa|Tu vois comment, Raphaël ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Les pommes n'ont pas fini de rouler.",
            "papa|Les pommes, le bas, ou son doigt ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le carton n'a pas fini de coincer.",
            "maman|Le bord, de côté, ou sa main ?",
        )
    return L(
        "narrateur|L'ombre n'a pas fini de trembler.",
        "papa|La lumière, son ombre, ou son mot ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "Il tient le carton, sans le pousser encore.",
            2: "Il tient le crayon, sans tracer encore.",
            3: "Il tient la ficelle, sans tirer encore.",
        }[t1]
        return L(
            "enfant-m|On attend les pommes.",
            f"narrateur|{hold}",
            "narrateur|Les pommes se taisent, une, puis plus.",
            f"narrateur|{o['wait']}",
            "narrateur|Chouchou pose une pomme, tout doux.",
            "papa|Les pommes se sont tues, maintenant.",
            "enfant-m|Elle a posé, toute seule.",
            "maman|Tu as attendu, et elle a posé.",
        )
    if t2 == 1 and t3 == 2:
        low = {
            1: "Il baisse le carton, loin des pommes qui tombent.",
            2: "Il baisse le crayon, loin des pommes qui tombent.",
            3: "Il baisse la ficelle, loin des pommes qui tombent.",
        }[t1]
        return L(
            "enfant-m|En bas, d'abord.",
            f"narrateur|{low}",
            "narrateur|Chouchou s'accroupit aussi, sans un mot.",
            "narrateur|Raphaël s'accroupit, les genoux au sol froid.",
            f"narrateur|{o['use']}",
            "papa|Tu as vu le bas, avant.",
            "enfant-m|Ici, ça ne tombe plus.",
            "maman|Près du sol, ça tenait mieux.",
        )
    if t2 == 1 and t3 == 3:
        point = {
            1: "Elle glisse le carton sous la pomme choisie.",
            2: "Elle pose le crayon vers la pomme choisie.",
            3: "Elle tend la ficelle vers la pomme choisie.",
        }[t1]
        return L(
            "enfant-m|Ton doigt, Chouchou.",
            "narrateur|Elle montre une pomme, tout près du râtelier.",
            "narrateur|Raphaël attend, puis suit le doigt.",
            f"narrateur|{point}",
            f"narrateur|{o['wait']}",
            "papa|Le doigt n'a pas bougé.",
            "copine|Pomme.",
            "maman|Son doigt a choisi.",
        )
    if t2 == 2 and t3 == 1:
        edge = {
            1: "Le carton reste collé à la marche, tout calme.",
            2: "Le crayon reste collé à la marche, tout calme.",
            3: "La ficelle reste collée à la marche, tout calme.",
        }[t1]
        return L(
            "enfant-m|On attend au bord.",
            f"narrateur|{edge}",
            "narrateur|Chouchou s'assoit, tout calme, sans parler.",
            f"narrateur|{o['wait']}",
            "narrateur|Puis elle penche le carton, tout doux.",
            "papa|La marche n'a plus pincé.",
            "enfant-m|Maintenant, ça passe.",
            "maman|Tu as laissé le bord finir.",
        )
    if t2 == 2 and t3 == 2:
        side = {
            1: "De côté, le carton n'est plus trop large.",
            2: "De côté, le crayon n'accroche plus la pierre.",
            3: "De côté, la ficelle n'accroche plus la pierre.",
        }[t1]
        return L(
            "enfant-m|De côté, d'abord.",
            "narrateur|Chouchou tourne le carton, sans un mot.",
            "narrateur|Raphaël suit ses mains, tout lent.",
            f"narrateur|{side}",
            f"narrateur|{o['use']}",
            "papa|Tu as tourné, tout doux.",
            "enfant-m|Il passe de côté.",
            "maman|De côté, la marche était plus douce.",
        )
    if t2 == 2 and t3 == 3:
        push = {
            1: "Sa main pousse le carton, d'un seul coup.",
            2: "Sa main pousse près du crayon, d'un seul coup.",
            3: "Sa main pousse près de la ficelle, d'un seul coup.",
        }[t1]
        return L(
            "enfant-m|Ta main, Chouchou.",
            "narrateur|Elle pousse le carton, tout près de la marche.",
            "narrateur|Raphaël attend, puis pousse avec elle.",
            f"narrateur|{push}",
            f"narrateur|{o['use']}",
            "papa|Sa main a guidé le bord.",
            "copine|Pousse.",
            "maman|Vous avez poussé ensemble.",
        )
    if t2 == 3 and t3 == 1:
        light = {
            1: "Sous la lumière, le carton ne tremble plus.",
            2: "Sous la lumière, le crayon ne glisse plus.",
            3: "Sous la lumière, la ficelle ne se tait plus.",
        }[t1]
        return L(
            "enfant-m|On attend la lumière.",
            "narrateur|L'ampoule jaune tremble, puis se tient.",
            "narrateur|Chouchou reste collée au cercle jaune.",
            f"narrateur|{light}",
            f"narrateur|{o['wait']}",
            "papa|La lumière est revenue, maintenant.",
            "enfant-m|Tu peux venir, maintenant.",
            "maman|Tu as laissé la lumière arriver.",
        )
    if t2 == 3 and t3 == 2:
        shade = {
            1: "Dans le jaune, le carton n'a plus d'ombre.",
            2: "Dans le jaune, le crayon n'a plus d'ombre.",
            3: "Dans le jaune, la ficelle n'a plus d'ombre.",
        }[t1]
        return L(
            "enfant-m|Ton ombre, d'abord.",
            "narrateur|Raphaël se glisse près d'elle, dans le jaune.",
            "narrateur|Chouchou reste dans le jaune, tout calme.",
            f"narrateur|{shade}",
            f"narrateur|{o['use']}",
            "papa|Tu t'es mis tout près, avec elle.",
            "enfant-m|On reste ici.",
            "maman|Près d'elle, le jaune suffisait.",
        )
    tiny = {
        1: "Le carton avance d'un pas, dans le jaune.",
        2: "Le crayon avance d'un pas, dans le jaune.",
        3: "La ficelle avance d'un pas, dans le jaune.",
    }[t1]
    return L(
        "enfant-m|Ton mot, Chouchou.",
        "narrateur|Raphaël attend, les lèvres fermées.",
        "narrateur|Chouchou ouvre la bouche, tout petit.",
        "copine|Viens.",
        f"narrateur|{tiny}",
        f"narrateur|{o['use']}",
        "papa|Elle a dit le mot, toute seule.",
        "maman|Le mot était tout bas, à elle.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le camion glisse, une pomme dessus, tout calme.",
            "enfant-m|On a attendu les pommes.",
            "papa|Les pommes se sont tues, d'abord.",
            "maman|On remonte, la marche est froide.",
            f"narrateur|{coda}",
            "narrateur|Une odeur de pomme suit l'escalier.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Du bas du râtelier, le camion glisse, une pomme dessus.",
            "enfant-m|On s'est baissés, d'abord.",
            "papa|Tu as vu le sol avant de pousser.",
            "maman|Essuie tes genoux, on remonte.",
            f"narrateur|{coda}",
            "narrateur|Un grain de poussière retombe, puis plus rien.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La pomme du doigt reste sur le camion, déjà.",
            "enfant-m|Elle a montré, et j'ai suivi.",
            "papa|Le doigt n'a pas bougé.",
            "maman|On remonte, le râtelier se tait.",
            f"narrateur|{coda}",
            "narrateur|Le râtelier se tait, derrière eux.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Quand le bord a cédé, le camion a glissé.",
            "enfant-m|On a attendu la marche.",
            "papa|La marche n'a plus pincé.",
            "maman|Une pomme tient encore dessus, on remonte.",
            f"narrateur|{coda}",
            "narrateur|La marche garde une trace de carton.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|De côté, le camion passe, une pomme dessus.",
            "enfant-m|On a tourné, d'abord.",
            "papa|Tu as tourné, tout doux.",
            "maman|On remonte, la pierre est froide.",
            f"narrateur|{coda}",
            "narrateur|Un trait jaune reste sur la pierre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sa main a laissé le camion passer, une pomme dessus.",
            "enfant-m|On a poussé ensemble.",
            "papa|Sa main a guidé le bord.",
            "maman|On remonte, vos doigts sentent le carton.",
            f"narrateur|{coda}",
            "narrateur|La ficelle traîne un instant, puis monte.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Quand la lumière a tenu, le camion a glissé.",
            "enfant-m|On a attendu l'ampoule.",
            "papa|La lumière vous a aidés.",
            "maman|Une pomme brille encore dessus, on remonte.",
            f"narrateur|{coda}",
            "narrateur|L'ampoule jaune tremble encore, tout seul.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Dans le jaune, le camion glisse, une pomme dessus.",
            "enfant-m|On est restés près d'elle.",
            "papa|Tu t'es glissé, comme l'ombre.",
            "maman|On remonte, vos manches sentent la cave.",
            f"narrateur|{coda}",
            "narrateur|Un cercle de lumière reste au sol, puis pâlit.",
        )
    return L(
        "narrateur|Après son mot, le camion glisse, une pomme dessus.",
        "enfant-m|Elle a dit viens, tout bas.",
        "papa|Le mot était à elle.",
        "maman|On remonte, l'escalier sent encore la pomme.",
        f"narrateur|{coda}",
        "narrateur|L'ombre de la cave reste en bas, tout calme.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|L'odeur des pommes grimpe l'escalier de pierre.",
        "narrateur|Elle arrive jusque dans le couloir, tout froid.",
        "narrateur|En bas, l'ampoule jaune tremble.",
        "papa|Tu entends ce bruit, Raphaël ?",
        "enfant-m|Le carton racle contre le mur.",
        "maman|Chouchou est déjà près du râtelier.",
        "narrateur|Un râtelier de bois tient des pommes, tout haut.",
        "narrateur|Une pomme rouge brille, un peu poussiéreuse.",
        "narrateur|En ce moment, Raphaël pose un pied sur la marche.",
        "enfant-m|On fait un camion, pour une pomme.",
        "narrateur|Chouchou tape deux fois le carton, tout doux.",
        "papa|Elle pousse déjà, elle.",
        "enfant-m|Dis camion, Chouchou !",
        "narrateur|Chouchou pousse encore, sans un mot.",
        "papa|Merci, tu as tenu la rampe.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois choses attendent près de la marche.",
        "narrateur|Un grand carton, un crayon gras, une ficelle.",
        "papa|Tu prends quoi d'abord, Raphaël ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le carton", "le crayon", "la ficelle")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Raphaël a pris {o['lab']} d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le râtelier", "la marche", "l'ampoule")

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
        "Cave sous la maison, odeur de pommes, ampoule jaune, carton qui racle. "
        "Raphaël veut monter un camion en carton pour descendre une pomme, avec Chouchou. "
        "T1 = grand carton / crayon gras / ficelle (les trois partent). "
        "T2 = râtelier (pommes qui roulent) / marche trop étroite / "
        "coin de l'ampoule (ombre, Chouchou s'arrête). "
        "T3 = neuf résolutions (attendre les pommes, le bas, son doigt ; "
        "le bord, de côté, sa main ; la lumière, son ombre, son mot). "
        "Chouchou agit : elle tape, pousse, montre, dit un mot. "
        "Raphaël attend, lit le geste. Fin : le camion glisse, une pomme dessus, on remonte.",
        "N2 ≤ 15. Slogan « Un camarade qui parle peu — dans la cuisine » jeté. "
        "Lina hors troupe, héros Raphaël, copine Chouchou. "
        "Pas cuisine (016/028/055), pas nichoir (053), pas locomotive (017), "
        "pas galet (045), pas cuillères (027), pas panier roue (037). "
        "Merci de papa (rampe). chunk_id inchangés. check() OK. "
        "xlsx live : stories/arbres/TREE-DIF-069.xlsx. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
