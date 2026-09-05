#!/usr/bin/env python3
"""TREE-DIF-054 — Le loup de carton de Victorina, sur le mur (N3, DIF.PAR.002, maison)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-054"
N3 = 16
TITLE = "Le loup de carton de Victorina, sur le mur"
FIL = (
    "Le soir, dans la maison, Victorina veut faire marcher son loup de carton "
    "sur le mur, tout grand, avec le drap et la lampe ronde. "
    "La lune de papier manque. Papa sait où, mais il cherche ses mots. "
    "T1 = drap blanc / loup de carton / lampe ronde ; les trois partent. "
    "T2 = buffet (assiettes qui couvrent) / placard sous l'escalier (écho) / "
    "étagère du palier (trop haute). "
    "Victorina laisse la phrase arriver. La lune rentre. Le loup marche."
)
CHARS = "Victorina, papa, maman"
SETTING = "la maison, le soir : couloir, buffet, placard sous l'escalier, palier"


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
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    check(SID, out["age_band"], out["chunks"])
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
        "inès",
        "ines",
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
        "cheval",
        "moulinet",
        "marché",
        "joue au salon",
        "dans le salon",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "victorina" not in blob:
        raise SystemExit(f"{SID}: Victorina absente")
    if "inès" in blob or "ines" in blob:
        raise SystemExit(f"{SID}: Inès encore là")
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
        "lab": "le drap blanc",
        "cap": "Le drap blanc",
        "t1q": "le drap",
        "t1acc": "drap | le drap | drap blanc | le drap blanc | le coton",
        "t1retry": "Victorina tient le drap. Elle tient quoi ?",
        "coda": "Le drap blanc tient le carton, tout droit.",
        "voy": "Le drap blanc penche déjà vers le couloir.",
    },
    2: {
        "lab": "le loup de carton",
        "cap": "Le loup de carton",
        "t1q": "le loup",
        "t1acc": "loup | le loup | carton | le carton | loup de carton",
        "t1retry": "Victorina tient le loup. Elle tient quoi ?",
        "coda": "Le loup de carton serre le bois, tout net.",
        "voy": "Le loup de carton tape un peu sa hanche.",
    },
    3: {
        "lab": "la lampe ronde",
        "cap": "La lampe ronde",
        "t1q": "la lampe",
        "t1acc": "lampe | la lampe | lampe ronde | la lampe ronde | le rond",
        "t1retry": "Victorina tient la lampe. Elle tient quoi ?",
        "coda": "La lampe ronde cliquette une fois, puis se tait.",
        "voy": "La lampe ronde pèse déjà contre sa hanche.",
    },
}

T3_LABS = {
    1: ("le tiroir du bas", "la serviette", "la chaise"),
    2: ("la porte tenue", "le chuchotement", "la marche"),
    3: ("le tabouret", "le regard d'en bas", "les bras de papa"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorina prend d'abord le drap blanc.",
            "enfant-f|Il glisse un peu, déjà.",
            "maman|Garde-le contre toi, tout droit.",
            "narrateur|Le coton sent encore le savon tiède de ce soir.",
            "papa|Le loup ensuite, près de toi.",
            "narrateur|Maman glisse la lampe ronde, tout près de l'épaule.",
            "narrateur|Les trois affaires avancent avec elle, vers le couloir.",
            "enfant-f|La lune, papa, elle est où ?",
            "narrateur|Papa ouvre la bouche, puis s'arrête au milieu.",
            "enfant-f|Où donc ?",
            "maman|Le mot n'est pas là, encore.",
            "papa|On marche, il va venir.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorina prend d'abord le loup de carton.",
            "enfant-f|Il gratte un peu, déjà.",
            "papa|Tiens-le contre toi, les oreilles hautes.",
            "narrateur|Le carton sent encore la colle, tout fin.",
            "maman|Le drap ensuite, autour du bras.",
            "narrateur|Papa glisse la lampe ronde dans sa main libre.",
            "narrateur|Les trois affaires avancent avec elle, pas après pas.",
            "enfant-f|Alors dis-moi où.",
            "narrateur|Papa inspire, les lèvres déjà rondes.",
            "narrateur|Rien ne sort, encore.",
            "maman|Il cherche la suite.",
            "enfant-f|J'écoute.",
        )
    return L(
        "narrateur|Victorina prend d'abord la lampe ronde.",
        "enfant-f|Pour le loup, après.",
        "papa|Elle est tiède, déjà.",
        "narrateur|Un clic réveille un petit rond, au plafond du couloir.",
        "maman|Le drap ensuite, et le loup.",
        "narrateur|Papa les pose contre elle, l'un après l'autre.",
        "narrateur|Près de la marche, plus rien n'attend.",
        "enfant-f|Maintenant, tu dis où.",
        "narrateur|Papa ouvre la bouche, puis la referme sans un mot.",
        "papa|Le mot va arriver.",
        "enfant-f|D'accord.",
        "maman|On avance, tout doux.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|Le drap.",
            "papa|Oui.",
            "narrateur|Le loup et la lampe voyagent avec, contre le coton.",
            "maman|La lune va se dire, plus loin.",
            "enfant-f|Je suis prête.",
            "papa|On marche, alors ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-f|Le loup.",
            "maman|Oui.",
            "narrateur|Le drap penche déjà sous le bras.",
            "narrateur|La lampe dort contre sa hanche, tout ronde.",
            "papa|Le carton a un peu piqué.",
            "enfant-f|J'écoute la suite.",
            "maman|On reste ensemble.",
        )
    return L(
        "enfant-f|La lampe.",
        "papa|Oui.",
        "narrateur|Le drap et le loup pèsent contre elle, déjà chauds.",
        "maman|Le rond va parler, en marchant.",
        "enfant-f|J'attends le mot.",
        "papa|Il va venir, tout seul.",
        "maman|On avance, alors ?",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|La maison a trois coins, encore, tout calmes.",
        "papa|Le buffet, le placard, ou l'étagère ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        extra = {
            1: "Il bute contre une pile d'assiettes, tout bas.",
            2: "Il s'accroche à une anse, déjà.",
            3: "Elle tape le bois, un petit toc.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près du buffet.",
            f"narrateur|{extra}",
            "narrateur|Des assiettes s'entrechoquent, toutes mêlées sur le bois.",
            "enfant-f|C'est ici ?",
            "papa|C'est la lune, près du.",
            "narrateur|Le mot s'arrête au milieu, couvert par le bruit.",
            "enfant-f|Près du quoi ?",
            "narrateur|Victorina referme sa bouche, tout net.",
            "maman|Elles se ressemblent toutes, là-haut.",
            "papa|On fait comment, Victorina ?",
        )
    if t2 == 2:
        extra = {
            1: "Il se froisse un peu, au bord sombre.",
            2: "Il rentre de travers, tout net.",
            3: "Elle éclaire un coin, trop vite.",
        }[t1]
        return L(
            f"narrateur|{o['cap']} arrive près du placard, sous l'escalier.",
            f"narrateur|{extra}",
            "enfant-f|Elle est là, la lune ?",
            "maman|Elle est derrière le.",
            "narrateur|L'écho couvre le mot, tout fort, entre les cartons.",
            "narrateur|Un fond de boîte tape déjà, tout loin.",
            "enfant-f|Derrière le bois ?",
            "narrateur|Victorina recule d'un pas, puis attend.",
            "papa|On n'entend plus la fin.",
            "maman|Tu trouves comment ?",
        )
    extra = {
        1: "Il reste trop bas, encore, sous le bois.",
        2: "Il pend, trop court, sous la planche.",
        3: "Elle n'atteint pas le bord, trop haute.",
    }[t1]
    return L(
        f"narrateur|{o['cap']} arrive sous l'étagère du palier.",
        f"narrateur|{extra}",
        "enfant-f|Tout en haut ?",
        "papa|Tout en haut, près du.",
        "narrateur|Papa s'arrête, les lèvres encore rondes, sans la suite.",
        "enfant-f|Près du cadre ?",
        "narrateur|Victorina garde sa bouche fermée, après.",
        "maman|Le haut est trop loin, pour elle.",
        "papa|Un tabouret dort près du mur.",
        "papa|Tu fais quoi, alors ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Sur le buffet, la suite manque encore.",
            "papa|Le tiroir, la serviette, ou la chaise ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Près du placard, le mot n'est pas fini.",
            "maman|La porte, le chuchotement, ou la marche ?",
        )
    return L(
        "narrateur|Sous l'étagère, le haut attend encore.",
        "papa|Le tabouret, le regard, ou mes bras ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "Le drap blanc reste contre la jambe, tout sage.",
        2: "Le loup de carton attend un dernier pas.",
        3: "La lampe ronde dort contre sa paume.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-f|On reste.",
            "narrateur|Elles s'arrêtent sous les assiettes, tout calmes.",
            "papa|Le tiroir.",
            "enfant-f|Le tiroir du bas.",
            "narrateur|Victorina attend, sans crier, les lèvres fermées.",
            "narrateur|Une lune de papier penche, enfin, contre le bois.",
            f"narrateur|{col}",
            "maman|La phrase est arrivée, toute seule.",
            "papa|Merci, Victorina.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-f|La serviette, dessus.",
            "narrateur|Les assiettes se taisent un peu, sous le linge.",
            "papa|Le.",
            "narrateur|Victorina ne dit rien.",
            "papa|Le bas, sous le linge.",
            "enfant-f|Je la vois, maintenant.",
            f"narrateur|{col}",
            "maman|Le linge a aidé le mot.",
            "papa|Tu as écouté jusqu'au bout.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-f|On s'assoit.",
            "narrateur|Elles regardent le bois, tout près du pied.",
            "papa|Pas le haut.",
            "narrateur|Victorina garde sa bouche fermée.",
            "papa|Contre la chaise.",
            "enfant-f|Celle-là, tout contre le pied.",
            f"narrateur|{col}",
            "maman|Tu n'as pas deviné trop tôt.",
            "papa|La lune est là, tout net.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-f|On tient.",
            "narrateur|Les deux retiennent la porte, tout calmes, sans l'écho.",
            "papa|Derrière le.",
            "narrateur|Victorina attend, les lèvres fermées.",
            "papa|Derrière le carton, la lune.",
            "enfant-f|Je l'entends, maintenant.",
            f"narrateur|{col}",
            "maman|Le mot est venu, tout seul.",
            "papa|Tu as laissé le mot aller jusqu'au bout.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-f|Tout bas, ici.",
            "papa|Tout près des oreilles.",
            "narrateur|L'écho devient un peu plus loin, déjà.",
            "maman|Derrière.",
            "narrateur|Victorina attend, les lèvres fermées.",
            "maman|Derrière la boîte.",
            f"narrateur|{col}",
            "papa|On a écouté ensemble.",
            "maman|La suite a eu sa place.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-f|La marche, là.",
            "papa|On s'assoit, tout doux.",
            "narrateur|Le bois est froid, encore, sous les chaussettes.",
            "maman|La lune.",
            "narrateur|Victorina tourne la tête, sans parler.",
            "enfant-f|Je la vois, contre le fond.",
            f"narrateur|{col}",
            "papa|La marche a tenu le mot.",
            "maman|On a regardé ensemble.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-f|Le tabouret, dessous.",
            "papa|Je le tiens, à ta hauteur.",
            "narrateur|Victorina monte, tout doux, sans crier.",
            "papa|Près du.",
            "narrateur|Victorina attend, un pied en l'air.",
            "papa|Près du cadre.",
            f"narrateur|{col}",
            "maman|Tu as laissé le mot monter.",
            "papa|Le bois a tenu tes pieds.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-f|Je regarde en bas.",
            "narrateur|Victorina baisse les yeux, tout calme, vers la plinthe.",
            "papa|Pas le grand.",
            "enfant-f|Le petit, contre le bois.",
            "narrateur|Une lune de papier penche, tout bas, déjà tombée.",
            "narrateur|Elle attendait près de la plinthe, sans un bruit.",
            f"narrateur|{col}",
            "maman|Le mot a fini sa route.",
            "papa|Merci d'avoir écouté jusque-là.",
        )
    return L(
        "enfant-f|Tes bras, papa.",
        "papa|Viens, tout contre moi.",
        "narrateur|Victorina s'élève, le nez au cadre, tout près des livres.",
        "papa|La lune, tout près du bord.",
        "enfant-f|Je la vois !",
        "narrateur|Un rond blanc brille entre deux livres, enfin.",
        f"narrateur|{col}",
        "maman|Tes bras ont fini la phrase.",
        "papa|Chacun a fait sa part.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La lune rentre dans le poing, un petit clic.",
            "enfant-f|Il marche !",
            "papa|Sur le mur du buffet, tout droit.",
            "maman|Bravo.",
            coda,
            "narrateur|Une miette sèche déjà sur le bois.",
            "narrateur|Le buffet redevient calme, autour des assiettes.",
            "narrateur|Le lait tiède sent encore, vers la cuisine.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le loup part, enfin, tout gris, entre les ombres.",
            "enfant-f|J'ai posé la serviette, d'abord.",
            "papa|Puis le mot est venu.",
            "maman|Venez, le mur est prêt.",
            coda,
            "narrateur|Victorina pose le carton contre l'épaule.",
            "narrateur|Une assiette tinte, puis se tait.",
            "narrateur|Le couloir laisse un rai, tout doux.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Contre la chaise, le loup tient, tout net.",
            "enfant-f|On s'est assises, papa.",
            "papa|Le haut gardera son ombre.",
            "maman|Tiens bien le carton, tout doux.",
            coda,
            "narrateur|Victorina tapote le bois, tout léger.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Une horloge tape, puis le buffet se tait.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Loin de l'écho, la lune était là, contre le carton.",
            "enfant-f|Tu as fini, papa.",
            "papa|Oui, le mot était long.",
            "maman|Tu as tenu la porte, tout doux.",
            coda,
            "narrateur|Une poussière sèche déjà sur le carton.",
            "narrateur|Victorina fait marcher le loup, tout près du bois.",
            "narrateur|Le placard redevient un placard, tout simple.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Dans le chuchotement, le mot a parlé, enfin.",
            "enfant-f|J'ai écouté, tout contre.",
            "papa|Tes oreilles étaient à la bonne place.",
            "maman|Le mur t'attend.",
            coda,
            "narrateur|Victorina essuie une main sur son pantalon.",
            "narrateur|Une ombre reste sur le bois.",
            "narrateur|Le loup avance, pas après pas.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sur la marche, la lune penche encore.",
            "enfant-f|Je l'ai vue, contre le fond.",
            "papa|Le bois a gardé l'ombre.",
            "maman|Rentre le carton, après le pas.",
            coda,
            "narrateur|Victorina souffle un peu sur les oreilles.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|La marche garde son ombre, tout seule.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Sur le tabouret, Victorina a vu le cadre.",
            "enfant-f|Le mot est monté avec moi.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Essuie tes chaussettes, Victorina.",
            coda,
            "narrateur|Le loup marche jusqu'au palier, tout net.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|L'étagère redevient calme, une planche encore.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Tout en bas, la lune brille, près de la plinthe.",
            "enfant-f|Tu as dit petit, à la fin.",
            "papa|Merci d'avoir écouté jusque-là.",
            "maman|Un peu de lait, après le mur.",
            coda,
            "narrateur|Victorina pose le carton contre le mur du palier.",
            "narrateur|L'étagère reprend sa place, tout sage.",
            "narrateur|Le haut n'a plus de secret, ce soir.",
        )
    return L(
        "narrateur|Dans les bras de papa, la lune était là.",
        "enfant-f|On l'a prise, tout haut.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        coda,
        "narrateur|Victorina pose le carton près des carreaux.",
        "narrateur|Les oreilles touchent l'air, enfin.",
        "narrateur|Une bande jaune s'allonge, puis la lampe se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Sur les carreaux du couloir, une bande jaune s'allonge.",
        "narrateur|La lampe du portemanteau est déjà allumée.",
        "narrateur|Ça sent encore le savon de la salle d'eau.",
        "narrateur|Une horloge tape, derrière la porte de la cuisine.",
        "narrateur|Papa plie le torchon, tout près de la marche du couloir.",
        "maman|La serviette reste un peu humide, encore.",
        "enfant-f|Mon loup va marcher, ce soir.",
        "narrateur|En ce moment, Victorina pose le carton contre le mur.",
        "narrateur|Deux oreilles pointues attendent déjà la lumière.",
        "papa|Il veut le grand mur, c'est ça ?",
        "enfant-f|Le grand, tout grand, papa.",
        "papa|Le grand est dans le.",
        "narrateur|Le mot s'arrête au milieu, tout net.",
        "enfant-f|Dans le quoi ?",
        "narrateur|Victorina referme sa bouche, et le loup aussi.",
        "maman|La suite va arriver.",
        "papa|Prenez vos affaires, avant que la bande s'éteigne.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près de la marche du couloir.",
        "narrateur|Le drap, le loup, et la lampe.",
        "papa|Tu prends quoi, d'abord ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le drap blanc", "le loup de carton", "la lampe ronde")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Victorina a pris {o['t1q']}, tout près.",
            "maman|Victorina a pris quoi, d'abord ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le buffet", "le placard", "l'étagère")

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
        "Victorina veut faire marcher son loup de carton sur le mur, "
        "le soir, dans la maison. La lune de papier manque. "
        "Papa sait où, cherche ses mots. "
        "T1 = drap blanc / loup de carton / lampe ronde (les trois partent). "
        "T2 = buffet (assiettes, bruit) / placard sous l'escalier (écho) / "
        "étagère du palier (trop haute). "
        "T3 = neuf résolutions (tiroir du bas, serviette, chaise ; "
        "porte tenue, chuchotement, marche ; "
        "tabouret, regard d'en bas, bras de papa). "
        "Victorina referme sa bouche. La lune rentre. Le loup marche. "
        "Fin : carreaux, bande jaune, lait, horloge.",
        "Slogan salon / Inès / bac-toboggan-balançoires / Tom-Léa-Sami jetés. "
        "Autre récit que DIF-018 (biscuits jardin), DIF-028 (gâteau), "
        "DIF-038 (cheval sous l'auvent), DIF-046 (moulinet marché). "
        "Héroïne Victorina, papa/maman, pas de copine. Désir ≠ leçon. "
        "N3 ≤ 16. Oral lié. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
