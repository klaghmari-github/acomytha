#!/usr/bin/env python3
"""TREE-DIF-071 — L'avion de papier de Mila, dans le hangar (N3, DIF.ENE.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-071"
N3 = 16
TITLE = "L'avion de papier de Mila, dans le hangar"
FIL = (
    "Dans le hangar à vélos, Mila veut faire voler un avion de papier "
    "d'un bout à l'autre, tout droit, avant la pluie. Victorino n'arrête pas "
    "de bouger. Elle prend d'abord la feuille, le trombone ou la craie ; "
    "les trois partent. Près des guidons la roue tourne trop, au milieu "
    "la flaque saute trop, près de la porte le vent pousse trop. "
    "Neuf façons de jouer avec son élan : il tient, il compte, il s'assoit. "
    "L'avion glisse jusqu'à la porte. On rentre."
)
CHARS = "Mila, Victorino, papa, maman"
SETTING = "hangar à vélos derrière la maison : guidons, flaque, porte"


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
        "maya",
        "camarade qui bouge",
        "un camarade",
        "hyperactif",
        "ce n'est pas une faute",
        "beaucoup d'énergie",
        "il faut attendre",
        "jardin",
        "carrousel",
        "papillon",
        "portail",
        "citronnade",
        "cuisine",
        "chambre",
        "dînette",
        "dinette",
        "les cubes",
        "après la sieste",
        "capitaine",
        "plic",
        "volet jaune",
        "balle rouge",
        "pichet",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
    if "hangar" not in blob:
        raise SystemExit(f"{SID}: hangar absent")
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
        "lab": "la feuille",
        "cap": "La feuille",
        "ans": "feuille",
        "acc": "feuille | la feuille | d'abord la feuille | le papier",
        "retry": "Mila prend la feuille d'abord.",
        "coda": "La feuille garde un pli tiède, tout petit.",
        "hip": "Entre ses doigts, le papier est encore froid.",
        "use": "Un pli blanc cherche encore l'air.",
    },
    2: {
        "lab": "le trombone",
        "cap": "Le trombone",
        "ans": "trombone",
        "acc": "trombone | le trombone | d'abord le trombone | le métal",
        "retry": "Mila prend le trombone d'abord.",
        "coda": "Le trombone reste froid, contre le nez.",
        "hip": "Dans sa paume, le trombone pique un peu.",
        "use": "Le métal pèse encore le nez plié.",
    },
    3: {
        "lab": "la craie",
        "cap": "La craie",
        "ans": "craie",
        "acc": "craie | la craie | d'abord la craie | le trait",
        "retry": "Mila prend la craie d'abord.",
        "coda": "Un trait de craie sèche déjà sur le ciment.",
        "hip": "Contre sa poche, la craie reste un peu chaude.",
        "use": "Un trait blanc attend, tout droit, au sol.",
    },
}

T3_LABS = {
    1: ("le guidon", "les tours", "le seau"),
    2: ("l'avion", "les gouttes", "le bord"),
    3: ("la porte", "jusqu'à trois", "le banc"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila prend d'abord la feuille blanche.",
            "enfant-f|Elle est froide, encore.",
            "papa|Le pli du nez tient déjà.",
            "narrateur|Elle la tend vers Victorino, tout près.",
            "copain|Moi je la lance, trop vite !",
            "narrateur|Mila replie le coin, tout doux.",
            "narrateur|Un grain de graisse tache le bord.",
            "maman|Le trombone et la craie viennent aussi.",
            "narrateur|Papa glisse le tout contre sa poche.",
            "narrateur|Rien ne reste sur le ciment.",
            "copain|Mila, on part ?",
            "enfant-f|Jusqu'à la porte, tout droit.",
            "papa|La feuille d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila prend d'abord le trombone, tout petit.",
            "enfant-f|Il pique un peu, au pouce.",
            "maman|Il va tenir le nez, tout droit.",
            "narrateur|Elle le glisse sur le pli, déjà.",
            "copain|Moi je le lance avec, trop fort !",
            "narrateur|Le métal cliquette contre le papier.",
            "narrateur|Une goutte de graisse brille au bout.",
            "papa|La feuille et la craie viennent aussi.",
            "narrateur|Maman les pose contre le sac.",
            "narrateur|Le ciment reste vide, derrière eux.",
            "copain|On y va, Mila ?",
            "enfant-f|Le nez d'abord, il pèse.",
            "maman|Le trombone d'abord, il est pris.",
        )
    return L(
        "narrateur|Mila prend d'abord la craie, encore rêche.",
        "enfant-f|Elle va faire la piste.",
        "papa|Un trait, pas tout le ciment.",
        "narrateur|Un blanc court déjà sous son doigt.",
        "copain|Moi je cours sur la piste !",
        "narrateur|Mila tient la craie, tout serré.",
        "narrateur|Un peu de poussière blanche tombe.",
        "maman|La feuille et le trombone viennent aussi.",
        "narrateur|Papa les glisse contre son genou.",
        "narrateur|La pompe reste seule, plus loin.",
        "copain|La piste, c'est pour l'avion ?",
        "enfant-f|Oui, tout droit, jusqu'à la porte.",
        "papa|La craie d'abord, elle est à toi.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            "narrateur|La feuille reste contre elle, encore froide.",
            "enfant-f|On va jusqu'à la porte.",
            "maman|La pluie n'est pas loin.",
            "papa|Tu tiens bien, Mila ?",
            "enfant-f|Oui, papa.",
            f"narrateur|{o['use']}",
            "copain|Moi je tiens la sonnette, déjà.",
            "narrateur|Un tintement court, puis se tait.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le trombone pend au pli, un peu lâche.",
            "enfant-f|Il va garder le nez.",
            "papa|Ça sent encore la graisse, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le métal se tait, puis plus rien.",
            "copain|Moi je fais tinter, encore.",
            "narrateur|La sonnette cliquette, trop vite, trop fort.",
        )
    return L(
        "narrateur|La craie reste chaude, contre sa poche.",
        "enfant-f|Le trait ne verse pas.",
        "maman|Le blanc sent encore la poussière.",
        "papa|On avance, tous les quatre ?",
        "enfant-f|Oui.",
        f"narrateur|{o['use']}",
        "copain|Moi je cours déjà, Mila !",
        "narrateur|Ses talons tapent le ciment, trop vite.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "La feuille penche déjà vers le hangar.",
        2: "Le trombone colle encore au pli.",
        3: "La craie appuie contre sa poche.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Près des guidons, une roue tourne encore.",
        "narrateur|Au milieu, une flaque coupe le ciment.",
        "narrateur|Près de la porte, le vent pousse.",
        "papa|Mila, tu vas où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le papier tape les rayons, trop vite.",
            2: "Le trombone accroche un rayon, trop fort.",
            3: "Le trait de craie se brouille sous le pneu.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Près des guidons, une roue tourne toute seule.",
            f"narrateur|{extra}",
            "copain|Je la fais tourner, trop fort !",
            "enfant-f|Mon avion a touché !",
            "narrateur|Les rayons claquent, trop près, trop vite.",
            "narrateur|Le papier se plie, de travers.",
            "papa|Ici, la roue n'arrête pas.",
            "maman|L'avion a besoin d'un couloir.",
            "enfant-f|Alors on fait comment ?",
            "papa|Tu vois comment, avec lui ?",
        )
    if t2 == 2:
        extra = {
            1: "Le papier boit l'eau, trop vite, trop gris.",
            2: "Le trombone gicle, trop mouillé, trop lourd.",
            3: "Le trait de craie fond, trop mou, trop pâle.",
        }[t1]
        return L(
            f"narrateur|{o['hip']}",
            "narrateur|Au milieu, la flaque brille sous le rayon.",
            f"narrateur|{extra}",
            "copain|Je saute dedans, trop fort !",
            "enfant-f|Mon avion est mouillé !",
            "narrateur|Des ronds d'eau courent, trop larges.",
            "narrateur|Le papier s'alourdit, trop bas.",
            "papa|Ici, ça saute trop.",
            "maman|L'avion n'arrive pas à glisser.",
            "enfant-f|Alors on fait comment ?",
            "maman|Tu vois comment, avec lui ?",
        )
    extra = {
        1: "Le papier part de travers, trop pris.",
        2: "Le nez trop lourd plonge, trop vite.",
        3: "Le trait s'envole en poussière, trop loin.",
    }[t1]
    return L(
        f"narrateur|{o['hip']}",
        "narrateur|Près de la porte, le vent pousse déjà.",
        f"narrateur|{extra}",
        "copain|J'ouvre, trop vite !",
        "enfant-f|Le vent l'a pris !",
        "narrateur|Le battant claque, trop fort, trop large.",
        "narrateur|L'avion file de côté, trop loin.",
        "papa|Ici, ça souffle trop.",
        "maman|Il lui faut un air plus calme.",
        "enfant-f|Alors on fait comment ?",
        "papa|Tu vois comment, avec lui ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La roue n'a pas fini de tourner.",
            "papa|Le guidon, les tours, ou le seau ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La flaque n'a pas fini de sauter.",
            "maman|L'avion, les gouttes, ou le bord ?",
        )
    return L(
        "narrateur|Le vent n'a pas fini de pousser.",
        "papa|La porte, jusqu'à trois, ou le banc ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "Elle tient la feuille, lui le guidon.",
            2: "Elle tient le trombone, lui le guidon.",
            3: "Elle tient la craie, lui le guidon.",
        }[t1]
        return L(
            "enfant-f|Tu tiens le guidon, Victorino.",
            "copain|Je le serre, tout fort.",
            f"narrateur|{hold}",
            "narrateur|La roue ralentit, un tour, puis plus.",
            f"narrateur|{o['use']}",
            "papa|Tes mains ont tenu la roue.",
            "enfant-f|Le couloir est libre, maintenant.",
            "maman|L'élan a trouvé le guidon.",
        )
    if t2 == 1 and t3 == 2:
        count = {
            1: "Il compte, la feuille reste contre elle.",
            2: "Il compte, le trombone reste au pli.",
            3: "Il compte, la craie reste dans sa main.",
        }[t1]
        return L(
            "enfant-f|Tu comptes les tours, d'abord.",
            "copain|Un, deux, trois, quatre.",
            f"narrateur|{count}",
            "narrateur|La roue s'essouffle, puis s'arrête.",
            f"narrateur|{o['wait'] if False else o['use']}",
            "papa|Tu as compté jusqu'au silence.",
            "copain|Elle ne tourne plus, Mila.",
            "maman|Les tours ont pris son élan.",
        )
    if t2 == 1 and t3 == 3:
        sit = {
            1: "Sur le seau, la feuille ne tremble plus.",
            2: "Sur le seau, le trombone ne cliquette plus.",
            3: "Sur le seau, la craie ne tombe plus.",
        }[t1]
        return L(
            "enfant-f|Tu t'assoies un moment, là.",
            "copain|Je m'assoie, les pieds encore vifs.",
            "narrateur|Victorino pose le seau, puis s'assoit.",
            f"narrateur|{sit}",
            "narrateur|Ses genoux dansent un peu, puis se posent.",
            f"narrateur|{o['use']}",
            "papa|Le seau a reçu tes jambes.",
            "maman|Un moment assis, et la roue s'est tue.",
        )
    if t2 == 2 and t3 == 1:
        plane = {
            1: "Il tient la feuille, au-dessus de l'eau.",
            2: "Il tient le trombone, au-dessus de l'eau.",
            3: "Il tient la craie, au-dessus de l'eau.",
        }[t1]
        return L(
            "enfant-f|Tu tiens l'avion, tout haut.",
            "copain|Je le serre, il ne tombe pas.",
            f"narrateur|{plane}",
            "narrateur|Mila trace un trait, au sec.",
            f"narrateur|{o['use']}",
            "papa|Tes mains ont porté l'avion.",
            "enfant-f|La piste est sèche, maintenant.",
            "maman|L'élan a tenu le papier.",
        )
    if t2 == 2 and t3 == 2:
        drops = {
            1: "Il compte, la feuille sèche un peu.",
            2: "Il compte, le trombone sèche un peu.",
            3: "Il compte, le trait redevient blanc.",
        }[t1]
        return L(
            "enfant-f|Tu comptes les gouttes, sur le toit.",
            "copain|Une, deux, trois, encore une.",
            f"narrateur|{drops}",
            "narrateur|Ses pieds restent au bord, sans sauter.",
            "narrateur|La flaque se tait, une fois, puis plus.",
            f"narrateur|{o['use']}",
            "papa|Tu as compté le toit, pas l'eau.",
            "maman|Les gouttes ont pris son élan.",
        )
    if t2 == 2 and t3 == 3:
        edge = {
            1: "Au bord, la feuille n'a plus d'eau.",
            2: "Au bord, le trombone n'a plus d'eau.",
            3: "Au bord, la craie n'a plus d'eau.",
        }[t1]
        return L(
            "enfant-f|Tu t'assoies au bord, tout petit.",
            "copain|Je m'assoie, les pieds dansent encore.",
            "narrateur|Victorino s'assoit, juste hors de l'eau.",
            f"narrateur|{edge}",
            "narrateur|Ses talons tapotent, puis se calment.",
            f"narrateur|{o['use']}",
            "papa|Le bord t'a gardé au sec.",
            "maman|Un moment assis, et la flaque s'est tue.",
        )
    if t2 == 3 and t3 == 1:
        door = {
            1: "Il tient la porte, la feuille ne file plus.",
            2: "Il tient la porte, le trombone ne plonge plus.",
            3: "Il tient la porte, le trait ne s'envole plus.",
        }[t1]
        return L(
            "enfant-f|Tu tiens la porte, tout fort.",
            "copain|Je la serre, elle ne claque plus.",
            f"narrateur|{door}",
            "narrateur|Le vent reste dehors, tout seul.",
            f"narrateur|{o['use']}",
            "papa|Tes mains ont tenu le battant.",
            "enfant-f|Le couloir est droit, maintenant.",
            "maman|L'élan a trouvé la porte.",
        )
    if t2 == 3 and t3 == 2:
        three = {
            1: "À trois, la feuille quitte ses doigts.",
            2: "À trois, le trombone quitte le pli.",
            3: "À trois, le trait guide le papier.",
        }[t1]
        return L(
            "enfant-f|Tu comptes jusqu'à trois, d'abord.",
            "copain|Un, deux, trois.",
            f"narrateur|{three}",
            "narrateur|Victorino souffle avec, tout droit.",
            "narrateur|Le battant reste fermé, derrière eux.",
            f"narrateur|{o['use']}",
            "papa|Tu as compté, puis vous avez lancé.",
            "maman|Jusqu'à trois, l'élan a suivi.",
        )
    bench = {
        1: "Sur le banc, la feuille ne tremble plus.",
        2: "Sur le banc, le trombone ne pique plus.",
        3: "Sur le banc, la craie ne tombe plus.",
    }[t1]
    return L(
        "enfant-f|Tu t'assoies un moment, sur le banc.",
        "copain|Je m'assoie, les mains encore vives.",
        "narrateur|Victorino s'assoit, près du battant.",
        f"narrateur|{bench}",
        "narrateur|Ses genoux dansent, puis se posent.",
        f"narrateur|{o['use']}",
        "papa|Le banc a reçu tes jambes.",
        "maman|Un moment assis, et le vent s'est tu.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu as tenu le guidon.",
            "copain|La roue s'est tue, alors il a volé.",
            "papa|Tes mains ont laissé le couloir.",
            "maman|On rentre, la pluie n'est pas loin.",
            f"narrateur|{coda}",
            "narrateur|Un grain de graisse sèche déjà sur le ciment.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu as compté les tours.",
            "copain|Quatre, puis plus rien, puis il a volé.",
            "papa|Les tours ont pris ton élan.",
            "maman|Essuie tes mains, on rentre.",
            f"narrateur|{coda}",
            "narrateur|La sonnette se tait, plus loin, toute seule.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu t'es assis un moment.",
            "copain|Le seau était froid, puis ça allait.",
            "papa|Le seau a reçu tes jambes.",
            "maman|On rentre, le hangar sent encore la graisse.",
            f"narrateur|{coda}",
            "narrateur|Une chaîne de vélo cliquette, puis plus rien.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu as tenu l'avion, tout haut.",
            "copain|Il n'est pas tombé dans l'eau.",
            "papa|Tes mains ont porté le papier.",
            "maman|On rentre, vos chaussures sont un peu mouillées.",
            f"narrateur|{coda}",
            "narrateur|Un rond d'eau sèche déjà sur le ciment.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu as compté les gouttes.",
            "copain|Le toit parlait, pas la flaque.",
            "papa|Tu as compté le toit, pas l'eau.",
            "maman|On rentre, ça sent encore le caoutchouc.",
            f"narrateur|{coda}",
            "narrateur|Une goutte sèche sur le guidon, tout petit.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu t'es assis au bord.",
            "copain|Mes pieds dansaient, puis ils se sont tus.",
            "papa|Le bord t'a gardé au sec.",
            "maman|On rentre, la flaque redevient calme.",
            f"narrateur|{coda}",
            "narrateur|Le rayon de pluie pâlit, puis s'efface.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu as tenu le battant.",
            "copain|Le vent est resté dehors.",
            "papa|Tes mains ont tenu la porte.",
            "maman|On rentre, le seuil est encore sec.",
            f"narrateur|{coda}",
            "narrateur|Un reflet jaune tremble au seuil, puis s'arrête.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
            "enfant-f|Tu as compté jusqu'à trois.",
            "copain|Un, deux, trois, et il a volé.",
            "papa|Vous avez lancé ensemble, tout droit.",
            "maman|On rentre, la pluie tapote déjà le toit.",
            f"narrateur|{coda}",
            "narrateur|Le battant reste fermé, derrière eux, tout calme.",
        )
    return L(
        "narrateur|L'avion glisse, tout droit, jusqu'à la porte.",
        "enfant-f|Tu t'es assis un moment.",
        "copain|Le banc était froid, puis ça allait.",
        "papa|Le banc a reçu tes jambes.",
        "maman|On rentre, le hangar se tait déjà.",
        f"narrateur|{coda}",
        "narrateur|Une sonnette oubliée tinte, puis le silence.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "pluie"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Derrière la maison, le hangar à vélos sent la graisse.",
        "narrateur|Un rayon de pluie coupe le ciment, tout étroit.",
        "narrateur|Une sonnette de vélo tinte, toute seule.",
        "papa|Tu as vu le trait d'eau, Mila ?",
        "enfant-f|Il barre le sol, jusqu'à la porte.",
        "maman|Ça sent le caoutchouc mouillé, déjà.",
        "narrateur|En ce moment, Mila plie un coin de papier.",
        "enfant-f|Je veux qu'il vole, tout droit.",
        "papa|Avant la pluie, d'un bout à l'autre.",
        "narrateur|Les pieds de Victorino tapent déjà le ciment.",
        "copain|On le fait voler, Mila !",
        "narrateur|Il fait tinter la sonnette, trop fort.",
        "maman|Le papier, le trombone, et la craie.",
        "papa|Merci, tu as plié le nez.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près de la pompe, trois affaires attendent.",
        "narrateur|Une feuille blanche, un trombone, une craie.",
        "papa|Tu prends quoi d'abord, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la feuille", "le trombone", "la craie")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Mila a pris {o['lab']} d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["ans"], o["acc"], o["retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("les guidons", "la flaque", "la porte")

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
        "Hangar à vélos derrière la maison : graisse, rayon de pluie, sonnette. "
        "Mila veut faire voler un avion de papier d'un bout à l'autre, "
        "tout droit, avant la pluie. Victorino n'arrête pas de bouger. "
        "T1 = feuille / trombone / craie (les trois partent). "
        "T2 = guidons (roue trop vite) / flaque (saut trop fort) / "
        "porte (vent trop fort). "
        "T3 = neuf façons de jouer avec son élan sans le gronder "
        "(il tient, il compte, il s'assoit un moment). "
        "Fin : l'avion glisse jusqu'à la porte, on rentre.",
        "N3 ≤ 16. Slogan « Un camarade qui bouge beaucoup — dans le jardin » "
        "jeté. Maya hors troupe → Mila. Copain Victorino. "
        "Pas jardin (008/018/031), pas carrousel (033), pas papillon (029), "
        "pas balle portail (039), pas citronnade (055). "
        "Pas « il faut attendre » : l'élan se vit. "
        "Merci de papa (nez plié), une fois. chunk_id inchangés. "
        "check() OK. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
