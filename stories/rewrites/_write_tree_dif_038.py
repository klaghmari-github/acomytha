#!/usr/bin/env python3
"""TREE-DIF-038 — Le cheval de bois de Nino, sous l'auvent (N1, DIF.PAR.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-038"
N1 = 10
TITLE = "Le cheval de bois de Nino, sous l'auvent"
FIL = (
    "Après la pluie, Nino veut que son cheval galope sur les carreaux secs. "
    "Une roue manque. Papa sait où, mais il cherche ses mots. "
    "T1 = cheval / boîte ronde / chiffon ; les trois partent. "
    "T2 = établi (copeaux) / coffre (couvercle) / étagère (trop haute). "
    "Nino laisse la phrase arriver. La roue rentre. Le cheval galope."
)


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
    out["characters"] = "Nino, papa, maman"
    out["setting"] = "sous l'auvent, après la pluie : établi, coffre, étagère"
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
        "il faut attendre",
        "laisser le temps",
        "attendre la fin",
        "noé",
        "noe ",
        "sami",
        "léa",
        " toboggan",
        "balançoire",
        "bac à sable",
        "capitaine",
        "plic",
        "volet jaune",
        "biscuit",
        "gâteau",
        "dans le salon",
        "joue au salon",
    ):
        if bad in whole:
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


OBJ = {
    1: {
        "lab": "le cheval",
        "cap": "Le cheval",
        "t1q": "le cheval",
        "t1acc": "cheval | le cheval | le bois | cheval de bois",
        "t1retry": "Nino tient le cheval. Il tient quoi ?",
        "coda": "Le bois du cheval reste un peu tiède.",
        "voy": "Le cheval penche déjà vers la porte.",
    },
    2: {
        "lab": "la boîte",
        "cap": "La boîte",
        "t1q": "la boîte",
        "t1acc": "boîte | la boîte | boite | la boite | la ronde",
        "t1retry": "Nino tient la boîte. Il tient quoi ?",
        "coda": "La boîte ronde garde une poussière, tout fine.",
        "voy": "La boîte ronde tape un peu sa hanche.",
    },
    3: {
        "lab": "le chiffon",
        "cap": "Le chiffon",
        "t1q": "le chiffon",
        "t1acc": "chiffon | le chiffon | le tissu | le linge",
        "t1retry": "Nino tient le chiffon. Il tient quoi ?",
        "coda": "Le chiffon sent encore le savon du bois.",
        "voy": "Le chiffon pend déjà contre sa poche.",
    },
}

T3_LABS = {
    1: ("le petit tiroir", "les copeaux", "le tiroir bas"),
    2: ("le coin gauche", "les deux mains", "la cale"),
    3: ("le pot bleu", "le tabouret", "les bras de papa"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord le cheval, tout rêche.",
            "enfant-m|Il sent encore la pluie.",
            "papa|Le bois a gardé une goutte.",
            "narrateur|Elle glisse sur le dos, puis s'arrête.",
            "maman|La boîte, ensuite, contre lui.",
            "narrateur|Papa pose le chiffon sur l'encolure.",
            "narrateur|Rien ne reste sous l'auvent.",
            "enfant-m|Où est la roue ?",
            "narrateur|Papa ouvre la bouche, puis s'arrête.",
            "enfant-m|Dans lequel ?",
            "maman|Le mot n'est pas là, encore.",
            "papa|On marche, il va venir.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino ouvre d'abord la boîte ronde.",
            "enfant-m|Elle sent le métal froid.",
            "maman|Une poussière brille au fond.",
            "narrateur|Le couvercle fait un petit toc.",
            "papa|Le cheval, ensuite, sous le bras.",
            "narrateur|Maman glisse le chiffon dans la poche.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Alors dis-moi où.",
            "narrateur|Papa inspire, les lèvres déjà rondes.",
            "narrateur|Rien ne sort, encore.",
            "maman|Il cherche la suite.",
            "enfant-m|J'écoute.",
        )
    return L(
        "narrateur|Nino prend d'abord le chiffon doux.",
        "enfant-m|Pour sécher le bois.",
        "papa|Il sent encore le savon.",
        "narrateur|Le tissu frotte l'encolure, tout léger.",
        "maman|La boîte, ensuite, et le cheval.",
        "narrateur|Papa les pose contre lui, l'un après l'autre.",
        "narrateur|Sous l'auvent, plus rien n'attend.",
        "enfant-m|Maintenant, tu dis où.",
        "narrateur|Papa ouvre la bouche, puis la referme.",
        "papa|Le mot va arriver.",
        "enfant-m|D'accord.",
        "maman|On avance, tout doux.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le cheval.",
            "papa|Oui.",
            "narrateur|La boîte et le chiffon voyagent avec.",
            "maman|La roue va se dire, plus loin.",
            "enfant-m|Je suis prêt.",
            "papa|On marche, alors ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La boîte.",
            "maman|Oui.",
            "narrateur|Le cheval penche déjà sous le bras.",
            "narrateur|Le chiffon dort dans la poche.",
            "papa|Le métal a un peu sonné.",
            "enfant-m|J'écoute la suite.",
            "maman|On reste ensemble.",
        )
    return L(
        "enfant-m|Le chiffon.",
        "papa|Oui.",
        "narrateur|Le cheval et la boîte pèsent contre lui.",
        "maman|Le bois va sécher, en marchant.",
        "enfant-m|J'attends le mot.",
        "papa|Il va venir, tout seul.",
        "maman|On avance, alors ?",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Sous l'auvent, trois coins restent secs.",
        "papa|L'établi, le coffre, ou l'étagère ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Le cheval bute contre un tas de copeaux.",
            2: "La boîte glisse sur une planche, tout fin.",
            3: "Le chiffon s'accroche à une écharde.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près de l'établi.",
            f"narrateur|{extra}",
            "narrateur|Des copeaux cachent les tiroirs, tout jaunes.",
            "enfant-m|C'est ici ?",
            "papa|C'est le tiroir.",
            "narrateur|Le mot s'arrête au milieu.",
            "enfant-m|Lequel ?",
            "narrateur|Nino referme sa bouche, tout net.",
            "maman|Les tiroirs se ressemblent tous.",
            "papa|On fait comment, Nino ?",
        )
    if t2 == 2:
        extra = {
            1: "Le cheval penche contre le couvercle lourd.",
            2: "La boîte tape le bois, un petit toc.",
            3: "Le chiffon glisse sous le bord, déjà.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près du coffre.",
            f"narrateur|{extra}",
            "enfant-m|Elle est là-dedans ?",
            "maman|Elle est dans le.",
            "narrateur|Maman cherche, un doigt en l'air.",
            "narrateur|Le couvercle ne bouge pas, encore.",
            "enfant-m|Ouvre !",
            "narrateur|Nino recule d'un pas, puis attend.",
            "papa|Le bois est trop lourd, tout seul.",
            "maman|Tu trouves comment ?",
        )
    extra = {
        1: "Le cheval lève le nez, trop bas encore.",
        2: "La boîte n'atteint pas le bord, trop haute.",
        3: "Le chiffon pend, trop court, sous le bois.",
    }[t1]
    return L(
        f"narrateur|{o['cap']} arrive sous l'étagère.",
        f"narrateur|{extra}",
        "enfant-m|Tout en haut ?",
        "papa|Tout en haut, près du.",
        "narrateur|Papa s'arrête, les lèvres encore rondes.",
        "enfant-m|Près du pot ?",
        "narrateur|Nino garde sa bouche fermée, après.",
        "maman|Le haut est trop loin, pour lui.",
        "papa|Un tabouret dort près du mur.",
        "papa|Tu fais quoi, alors ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Sur l'établi, la suite manque encore.",
            "papa|Le petit, les copeaux, ou le bas ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Sur le coffre, le mot n'est pas fini.",
            "maman|Le coin, les mains, ou la cale ?",
        )
    return L(
        "narrateur|Sous l'étagère, le haut attend encore.",
        "papa|Le pot, le tabouret, ou mes bras ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "Le cheval reste contre la jambe, tout sage.",
        2: "La boîte attend un dernier toc.",
        3: "Le chiffon dort contre sa paume.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-m|On reste.",
            "narrateur|Ils s'assoient près des copeaux, tout calmes.",
            "papa|Le petit.",
            "enfant-m|Le petit tiroir.",
            "narrateur|Nino tire, tout doux, sans crier.",
            "narrateur|Une roue brille au fond, enfin.",
            f"narrateur|{col}",
            "maman|La phrase est arrivée, toute seule.",
            "papa|Merci, Nino.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-m|Je souffle.",
            "narrateur|Les copeaux s'envolent, un par un.",
            "papa|Le.",
            "narrateur|Nino ne dit rien.",
            "papa|Le petit.",
            "enfant-m|Je vois l'étiquette, maintenant.",
            f"narrateur|{col}",
            "maman|Le vent a aidé le mot.",
            "papa|Tu as écouté jusqu'au bout.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-m|On se baisse.",
            "narrateur|Ils s'accroupissent près du tiroir bas.",
            "papa|Pas le haut.",
            "narrateur|Nino garde sa bouche fermée.",
            "papa|Le bas.",
            "enfant-m|Celui-là, tout près du sol.",
            f"narrateur|{col}",
            "maman|Tu n'as pas deviné trop tôt.",
            "papa|La roue est là, tout ronde.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-m|On ne touche pas encore.",
            "narrateur|Les deux restent debout, tout calmes.",
            "maman|Le coin gauche.",
            "enfant-m|Celui près de la fenêtre.",
            "narrateur|Papa lève un peu, Nino regarde.",
            f"narrateur|{col}",
            "papa|Le mot est venu, tout seul.",
            "maman|Tu as laissé la fin arriver.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-m|À deux.",
            "papa|Tes mains ici, les miennes là.",
            "narrateur|Le couvercle s'ouvre, tout lent.",
            "maman|Dans le.",
            "narrateur|Nino attend, les lèvres fermées.",
            "maman|Dans le coin.",
            f"narrateur|{col}",
            "papa|On a porté ensemble.",
            "maman|La suite a eu sa place.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-m|La cale, dessous.",
            "papa|Je glisse le bois, tout doux.",
            "narrateur|Le couvercle reste ouvert, un peu.",
            "maman|À gauche.",
            "narrateur|Nino tourne la tête, sans parler.",
            "enfant-m|Je la vois, au fond.",
            f"narrateur|{col}",
            "papa|La cale a tenu le mot.",
            "maman|On a regardé ensemble.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-m|Je dis rien.",
            "narrateur|Nino baisse les yeux, tout calme.",
            "papa|Près du pot bleu.",
            "enfant-m|Celui qui brille.",
            "narrateur|Papa tend la boîte, tout haut.",
            f"narrateur|{col}",
            "maman|Le mot a fini sa route.",
            "papa|Merci d'avoir écouté jusque-là.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-m|Le tabouret, dessous.",
            "papa|Je le tiens, à ta hauteur.",
            "narrateur|Nino monte, tout doux, sans crier.",
            "papa|Près du.",
            "narrateur|Nino attend, un pied en l'air.",
            "papa|Près du pot.",
            f"narrateur|{col}",
            "maman|Tu as laissé le mot monter.",
            "papa|Le bois a tenu tes pieds.",
        )
    return L(
        "enfant-m|Tes bras, papa.",
        "papa|Viens, tout contre moi.",
        "narrateur|Nino s'élève, le nez au bois.",
        "papa|Près du pot bleu.",
        "enfant-m|Je la vois !",
        "narrateur|La roue brille entre deux pots.",
        f"narrateur|{col}",
        "maman|Tes bras ont fini la phrase.",
        "papa|Chacun a fait sa part.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La roue rentre, un petit clic.",
            "enfant-m|Il galope !",
            "papa|Sur les carreaux secs, tout droit.",
            "maman|Bravo.",
            coda,
            "narrateur|Une goutte sèche déjà sur l'encolure.",
            "narrateur|L'établi redevient calme, autour des copeaux.",
            "narrateur|La soupe sent, derrière la porte.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|La roue tourne, enfin, tout ronde.",
            "enfant-m|Les copeaux ont volé, d'abord.",
            "papa|Puis le mot est venu.",
            "maman|Venez, le pain est chaud.",
            coda,
            "narrateur|Nino pose le cheval près du seuil.",
            "narrateur|Un copeau reste collé à sa chaussure.",
            "narrateur|L'auvent laisse passer un rai, tout doux.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La roue du bas tient, tout nette.",
            "enfant-m|On s'est baissés, papa.",
            "papa|Le haut gardera son ombre.",
            "maman|Lave-toi les mains, tout doux.",
            coda,
            "narrateur|Nino tapote le dos, tout léger.",
            "narrateur|Le bois a un peu de poussière.",
            "narrateur|Une abeille passe, puis l'auvent se tait.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Au coin gauche, la roue était là.",
            "enfant-m|Tu as fini, maman.",
            "maman|Oui, le mot était long.",
            "papa|Merci d'avoir regardé sans crier.",
            coda,
            "narrateur|Le couvercle retombe, un petit toc.",
            "narrateur|Nino fait galoper le cheval, tout près.",
            "narrateur|Le coffre redevient un coffre, tout simple.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|À deux, le coffre a parlé, enfin.",
            "enfant-m|On a porté, tous les deux.",
            "papa|Tes mains étaient à la bonne place.",
            "maman|Le pain t'attend.",
            coda,
            "narrateur|Nino essuie une main sur son pantalon.",
            "narrateur|Un grain de savon reste sur le bois.",
            "narrateur|Le cheval avance, roue après roue.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|La cale tient encore le bord, tout calme.",
            "enfant-m|Je l'ai vue, au fond.",
            "papa|Le bois a gardé l'ouverture.",
            "maman|Rentrez la cale, après le galop.",
            coda,
            "narrateur|Nino souffle un peu sur la roue.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Le coffre garde son ombre, tout seul.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Près du pot bleu, la roue brille.",
            "enfant-m|Tu as dit bleu, à la fin.",
            "papa|Merci d'avoir écouté jusque-là.",
            "maman|Un peu de soupe, après le galop.",
            coda,
            "narrateur|Nino pose le cheval contre le mur.",
            "narrateur|Le pot bleu reprend sa place, tout sage.",
            "narrateur|L'étagère n'a plus de secret, ce soir.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sur le tabouret, Nino a vu le bleu.",
            "enfant-m|Le mot est monté avec moi.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Essuie tes chaussures, Nino.",
            coda,
            "narrateur|Le cheval galope jusqu'au seuil, tout net.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|L'auvent redevient calme, une goutte encore.",
        )
    return L(
        "narrateur|Dans les bras de papa, la roue était là.",
        "enfant-m|On l'a prise, tout haut.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        coda,
        "narrateur|Nino pose le cheval près des carreaux.",
        "narrateur|Quatre roues touchent le sol, enfin.",
        "narrateur|Une goutte sèche, puis le bois se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une goutte tombe encore, sous l'auvent.",
        "narrateur|Le bois sent la pluie, tout chaud.",
        "narrateur|Les carreaux sèchent, un par un.",
        "papa|Tu as vu le cheval, Nino ?",
        "enfant-m|Il manque une roue.",
        "maman|Papa la connaît, quelque part.",
        "narrateur|En ce moment, Nino touche le bois.",
        "enfant-m|Je veux qu'il galope.",
        "papa|La roue est dans le.",
        "narrateur|Papa cherche, la bouche ouverte.",
        "enfant-m|Dans le quoi ?",
        "narrateur|Nino referme sa bouche, tout net.",
        "maman|La suite va arriver.",
        "papa|Prenez vos affaires, avant le vent.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du seuil.",
        "narrateur|Le cheval, la boîte, et le chiffon.",
        "papa|Tu prends quoi, d'abord ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le cheval", "la boîte ronde", "le chiffon")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nino a pris {o['t1q']}, tout près.",
            "maman|Nino a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'établi", "le coffre", "l'étagère")

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
        "Nino veut que son cheval de bois galope sur les carreaux secs, sous l'auvent. "
        "Une roue manque. Papa sait où, cherche ses mots. "
        "T1 = cheval / boîte ronde / chiffon (les trois partent). "
        "T2 = établi (copeaux, tiroir) / coffre (couvercle lourd) / étagère (trop haute). "
        "T3 = neuf résolutions (petit tiroir, souffler, tiroir bas ; "
        "coin gauche, à deux, cale ; pot bleu, tabouret, bras de papa). "
        "Nino referme sa bouche. La roue rentre. Le cheval galope. "
        "Fin : carreaux, soupe, auvent calme.",
        "Slogan salon / Noé / bac-toboggan-balançoires / Tom-Léa-Sami jetés. "
        "Autre récit que DIF-018 (biscuits jardin) et DIF-028 (gâteau). "
        "Héros Nino, papa/maman, pas de copain. Désir ≠ leçon. "
        "N1 ≤ 10. Oral lié. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
