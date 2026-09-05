#!/usr/bin/env python3
"""TREE-DIF-017 — La locomotive de Nino et la gare en carton (N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-017"
N2 = 15
TITLE = "La locomotive de Nino et la gare en carton"
FIL = (
    "Nino veut que son train de bois arrive à la gare en carton. "
    "Aniss vient jouer ; Nino voudrait l'entendre crier go, "
    "mais Aniss répond avec les mains. "
    "T1 = locomotive / rails / drapeau, les trois partent. "
    "T2 = couloir (chaussure, rail manquant) / salon (tapis) / terrasse (flaque, vent). "
    "T3 = neuf façons d'arriver. Nino attend, tend le jouet. La gare reçoit le train."
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
    out["characters"] = "Nino, Aniss, papa, maman"
    out["setting"] = "couloir, salon, terrasse, gare en carton"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "hugo",
        "parle peu",
        "camarade",
        "timide",
        "forcer la parole",
        "il faut attendre",
        "un camarade",
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


OBJ = {
    1: {
        "lab": "la locomotive",
        "cap": "La locomotive",
        "t1q": "la locomotive",
        "t1acc": "locomotive | la locomotive | le train | le jouet | tendre",
        "t1retry": "Il tend la locomotive. Il tend quoi ?",
        "coda": "Un peu de cire brille encore sur le toit.",
        "voy": "La locomotive voyage déjà dans le panier.",
    },
    2: {
        "lab": "les rails",
        "cap": "Les rails",
        "t1q": "un rail",
        "t1acc": "rail | un rail | les rails | le bois | tendre",
        "t1retry": "Il tend un rail. Il tend quoi ?",
        "coda": "Un rail reste contre le carton, tout droit.",
        "voy": "Les rails voyagent déjà dans le panier.",
    },
    3: {
        "lab": "le drapeau",
        "cap": "Le drapeau",
        "t1q": "le drapeau",
        "t1acc": "drapeau | le drapeau | le rouge | le bâton | tendre",
        "t1retry": "Il tend le drapeau. Il tend quoi ?",
        "coda": "Le drapeau penche sur le toit, tout calme.",
        "voy": "Le drapeau voyage déjà dans le panier.",
    },
}

T3_LABS = {
    1: ("le rail", "la locomotive", "la chaussure"),
    2: ("le livre", "la planche", "le parquet"),
    3: ("le vent", "la gare", "le drapeau"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord la locomotive de bois.",
            "enfant-m|Elle sent la cire.",
            "papa|Le toit est un peu rêche, encore.",
            "narrateur|Il la tend vers Aniss, tout près.",
            "enfant-m|Dis vroom !",
            "narrateur|Aniss pose deux doigts sur une roue.",
            "narrateur|La roue tourne, petite, puis s'arrête.",
            "maman|Les rails et le drapeau viennent aussi.",
            "narrateur|Papa glisse le tout dans le panier.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-m|Aniss, on part ?",
            "narrateur|Aniss hoche la tête, tout petit.",
            "papa|La locomotive d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino prend d'abord deux rails de bois.",
            "enfant-m|Ça fait clic.",
            "papa|Un clic, puis un autre clic.",
            "narrateur|Il tend un rail vers Aniss.",
            "enfant-m|Dis encore !",
            "narrateur|Aniss aligne les deux bouts, tout droit.",
            "narrateur|Le clic se fait, sans un mot.",
            "maman|La locomotive et le drapeau viennent aussi.",
            "narrateur|Papa les pose près du panier.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-m|Aniss, c'est bon ?",
            "narrateur|Aniss appuie sur le rail, tout calme.",
            "papa|Les rails d'abord, ils tiennent.",
        )
    return L(
        "narrateur|Nino prend d'abord le drapeau rouge.",
        "enfant-m|C'est pour la gare.",
        "maman|Le tissu est un peu rêche.",
        "narrateur|Il tend le bâton vers Aniss.",
        "enfant-m|Dis gare !",
        "narrateur|Aniss tient le bâton à deux mains.",
        "narrateur|Le rouge tombe un peu sur ses genoux.",
        "papa|La locomotive et les rails viennent aussi.",
        "narrateur|Maman les glisse près du sac.",
        "narrateur|Les trois affaires restent ensemble.",
        "enfant-m|Aniss, tu viens ?",
        "narrateur|Aniss lève le drapeau, tout bas.",
        "maman|Le drapeau d'abord, vous l'avez.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss prend la locomotive contre lui.",
            "enfant-m|Elle est à toi, un moment.",
            "narrateur|Nino attend, les mains ouvertes.",
            "narrateur|Une roue fait un tout petit clic.",
            "maman|Le bois est tiède, maintenant.",
            "papa|On pose la ligne où ?",
            "enfant-m|On va jusqu'à la gare.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss garde le rail contre sa jambe.",
            "enfant-m|Il est à toi, un moment.",
            "narrateur|Nino attend, sans répéter.",
            "narrateur|Le bois sent encore le grenier.",
            "maman|La ligne peut grandir, après.",
            "papa|On pose la ligne où ?",
            "enfant-m|Jusqu'à la gare.",
        )
    return L(
        "narrateur|Aniss tient encore le drapeau, tout près.",
        "enfant-m|Il est à toi, un moment.",
        "narrateur|Nino attend, les lèvres fermées.",
        "narrateur|Le rouge bouge un peu, puis s'arrête.",
        "papa|La gare va le voir, plus tard.",
        "maman|On pose la ligne où ?",
        "enfant-m|Jusqu'à la boîte.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Le couloir a des carreaux tièdes.",
        "narrateur|Le salon a un tapis épais.",
        "narrateur|La terrasse a une flaque ronde.",
        "papa|On commence où, pour la gare ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = {
            1: "narrateur|La locomotive tape un peu le carreau.",
            2: "narrateur|Un rail frotte le carreau, tout sec.",
            3: "narrateur|Le drapeau frôle le mur du couloir.",
        }[t1]
        return L(
            lead,
            "narrateur|Une chaussure de papa barre le passage.",
            "enfant-m|Pousse-la, Aniss !",
            "narrateur|Aniss pointe un trou, entre deux rails.",
            "narrateur|Un bout de ligne manque, juste là.",
            "enfant-m|Dis-moi où !",
            "maman|Il montre déjà, avec le doigt.",
            "papa|La chaussure reste lourde, au milieu.",
            "narrateur|Aniss ouvre un peu son sac.",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|La locomotive s'enfonce dans le tapis.",
            2: "narrateur|Un rail disparaît un peu dans le tapis.",
            3: "narrateur|Le drapeau traîne sur le tapis, trop mou.",
        }[t1]
        return L(
            lead,
            "enfant-m|Le tapis est trop mou.",
            "narrateur|Les roues s'enfoncent, puis s'arrêtent.",
            "enfant-m|Pousse, Aniss !",
            "narrateur|Aniss pose la paume sur le toit.",
            "narrateur|Le train ne bouge presque plus.",
            "maman|Le tapis avale les petites roues.",
            "papa|Le parquet, plus loin, est lisse.",
            "narrateur|Un livre épais dort sous la table.",
            "papa|Vous faites comment, tous les deux ?",
        )
    lead = {
        1: "narrateur|La locomotive sent le vent, tout de suite.",
        2: "narrateur|Les rails cliquent au vent, sur la pierre.",
        3: "narrateur|Le drapeau claque une fois, trop fort.",
    }[t1]
    return L(
        lead,
        "enfant-m|La flaque est trop grande.",
        "narrateur|Le vent secoue le carton de la gare.",
        "enfant-m|Aniss, on court ?",
        "narrateur|Aniss recule d'un pas, près du seuil.",
        "narrateur|Une goutte brille déjà sur le toit.",
        "maman|Le carton n'aime pas l'eau.",
        "papa|Le vent tient encore le drapeau.",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le trou entre les rails reste ouvert.",
            "papa|Le rail, la locomotive, ou la chaussure ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les roues restent prises dans le tapis.",
            "maman|Le livre, la planche, ou le parquet ?",
        )
    return L(
        "narrateur|La flaque tient encore le chemin.",
        "papa|Le vent, la gare, ou le drapeau ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|La locomotive attend près du trou.",
            2: "narrateur|Les rails attendent près du trou.",
            3: "narrateur|Le drapeau attend près du trou.",
        }[t1]
        return L(
            "enfant-m|On attend.",
            "narrateur|Aniss fouille son sac, tout lent.",
            "narrateur|Un rail de bois en sort, le dernier.",
            wait,
            "narrateur|Aniss le pose dans le trou.",
            "narrateur|Ça fait clic, tout net.",
            "enfant-m|Clic.",
            "papa|Le trou n'est plus un trou.",
            "maman|Vous avez laissé le temps au sac.",
        )
    if t2 == 1 and t3 == 2:
        hold = {
            1: "narrateur|Aniss pose la locomotive avant la chaussure.",
            2: "narrateur|Aniss pose le rail avant la chaussure.",
            3: "narrateur|Aniss pose le drapeau avant la chaussure.",
        }[t1]
        return L(
            "enfant-m|Pour toi.",
            "narrateur|Nino tend la locomotive vers Aniss.",
            hold,
            "narrateur|Le train contourne le cuir, tout doux.",
            "enfant-m|Il passe !",
            "maman|Le train a pris le bord, tout seul.",
            "papa|Les roues ont trouvé le cuir.",
            f"narrateur|{o['cap']} reste un instant sur le bord.",
        )
    if t2 == 1 and t3 == 3:
        shoe = {
            1: "narrateur|La locomotive attend pendant qu'ils poussent.",
            2: "narrateur|Les rails attendent pendant qu'ils poussent.",
            3: "narrateur|Le drapeau attend pendant qu'ils poussent.",
        }[t1]
        return L(
            "enfant-m|La chaussure, Aniss.",
            "narrateur|Aniss tire le lacet, sans un mot.",
            "narrateur|Nino pousse le talon vers le mur.",
            shoe,
            "narrateur|Le passage redevient droit.",
            "enfant-m|Merci.",
            "papa|La chaussure a sa place, maintenant.",
            "maman|La ligne peut courir, tout long.",
        )
    if t2 == 2 and t3 == 1:
        book = {
            1: "narrateur|La locomotive monte sur la couverture.",
            2: "narrateur|Un rail guide la couverture, tout droit.",
            3: "narrateur|Le drapeau repose au bord du livre.",
        }[t1]
        return L(
            "enfant-m|Le livre, dessous.",
            "narrateur|Aniss glisse le livre sous les roues.",
            "narrateur|La couverture fait une piste, un peu dure.",
            book,
            "narrateur|Le train avance, tout droit, sans s'enfoncer.",
            "enfant-m|Ça roule !",
            "papa|Le livre a tenu le tapis.",
            "maman|Aniss a poussé tout doux.",
        )
    if t2 == 2 and t3 == 3:
        wood = {
            1: "narrateur|La locomotive chante déjà sur le bois.",
            2: "narrateur|Les rails cliquent sur le bois, tout net.",
            3: "narrateur|Le drapeau suit la bande près de la vitre.",
        }[t1]
        return L(
            "enfant-m|On recommence au parquet.",
            "narrateur|Aniss pointe la bande lisse, près de la vitre.",
            "narrateur|Nino attend, puis suit le doigt.",
            wood,
            "narrateur|Les roues glissent sur le bois, tout net.",
            "enfant-m|Elles glissent.",
            "maman|Le tapis garde son creux, plus loin.",
            "papa|Le bois est plus facile, ici.",
        )
    if t2 == 2 and t3 == 2:
        board = {
            1: "narrateur|La locomotive part au milieu de la planche.",
            2: "narrateur|Les rails tiennent au milieu de la planche.",
            3: "narrateur|Le drapeau veille au bout de la planche.",
        }[t1]
        return L(
            "enfant-m|La planche de la cuisine.",
            "papa|Je vous la tends, à votre hauteur.",
            "narrateur|Aniss tient un bout, Nino l'autre.",
            board,
            "narrateur|Le train traverse comme un pont.",
            "enfant-m|On tient ensemble.",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|La planche redescendra après.",
        )
    if t2 == 3 and t3 == 1:
        wind = {
            1: "narrateur|La locomotive attend sur le seuil, tout calme.",
            2: "narrateur|Les rails attendent sur le seuil, tout calmes.",
            3: "narrateur|Le drapeau retombe, enfin, contre le bois.",
        }[t1]
        return L(
            "enfant-m|On attend le vent.",
            "narrateur|Aniss s'assoit sur le seuil, tout calme.",
            "narrateur|Nino s'assoit aussi, les genoux contre lui.",
            wind,
            "narrateur|Le vent tombe, une feuille s'arrête.",
            "enfant-m|Maintenant.",
            "papa|Le carton ne tremble plus.",
            "maman|Vous avez laissé le vent finir.",
        )
    if t2 == 3 and t3 == 2:
        close = {
            1: "narrateur|La locomotive roule jusqu'à la boîte rapprochée.",
            2: "narrateur|Les rails s'arrêtent juste avant la flaque.",
            3: "narrateur|Le drapeau marque le nouveau bord de la gare.",
        }[t1]
        return L(
            "enfant-m|On rapproche la gare.",
            "narrateur|Aniss prend un côté de la boîte.",
            "narrateur|Nino prend l'autre, avant la flaque.",
            close,
            "narrateur|La gare s'assoit sur les carreaux secs.",
            "enfant-m|Elle est tout près.",
            "maman|Le carton reste au sec.",
            "papa|La flaque garde son rond, plus loin.",
        )
    flag = {
        1: "narrateur|La locomotive suit le rouge, pierre après pierre.",
        2: "narrateur|Les rails courent le long du rouge, au sec.",
        3: "narrateur|Le drapeau tient dans le sec, tout droit.",
    }[t1]
    return L(
        "enfant-m|Le drapeau, sur les pierres.",
        "narrateur|Nino plante le bâton dans le sec.",
        "narrateur|Aniss suit le rouge, pas à pas.",
        flag,
        "narrateur|Le train prend le chemin des pierres.",
        "enfant-m|Il évite l'eau.",
        "papa|Le rouge a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le train entre dans la boîte, un petit toc.",
            "copain|Toc.",
            "enfant-m|Il est arrivé.",
            "papa|Le rail du sac a fermé le trou.",
            "maman|Le toast est prêt, dans la cuisine.",
            "narrateur|Aniss pose encore une main sur le toit.",
            coda,
            "narrateur|Une miette de pain attend sur la table.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le train a contourné le cuir, jusqu'au bout.",
            "enfant-m|Aniss l'a posé, tout seul.",
            "papa|Tu as tendu, d'abord.",
            "maman|Venez, le pain est chaud.",
            coda,
            "narrateur|Aniss s'assoit près de la boîte.",
            "copain|Gare.",
            "narrateur|Le cuir de la chaussure sèche déjà au mur.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La ligne court jusqu'à la gare, tout droit.",
            "enfant-m|On a poussé la chaussure.",
            "papa|Le lacet est rentré à sa place.",
            "maman|Lavez-vous les mains, tout doux.",
            coda,
            "narrateur|Aniss tapote le toit de carton.",
            "narrateur|Le feutre noir a un peu de poussière.",
            "narrateur|Le toast craque, tout loin, dans la cuisine.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le train glisse sur le livre, puis dans la boîte.",
            "enfant-m|La couverture était dure, juste assez.",
            "papa|Le tapis n'a plus pris les roues.",
            "maman|Refermez le livre, après le voyage.",
            coda,
            "copain|Vroom.",
            "narrateur|Une page se soulève, puis se tait.",
            "narrateur|Le salon redevient calme, autour du tapis.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le pont de planche mène jusqu'à la gare.",
            "enfant-m|On tenait, tous les deux.",
            "papa|Je remporte la planche, tout à l'heure.",
            "maman|Le pain vous attend.",
            coda,
            "narrateur|Aniss essuie une main sur son pantalon.",
            "narrateur|Un grain de farine reste sur le bois.",
            "narrateur|La boîte sent encore le carton chaud.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les roues chantent jusqu'au carton, sur le parquet.",
            "enfant-m|C'était plus facile, là.",
            "papa|La vitre a guidé la ligne.",
            "maman|Le tapis gardera son creux.",
            coda,
            "narrateur|Aniss pose un doigt sur la porte de la gare.",
            "narrateur|Elle s'ouvre, tout petit.",
            "narrateur|Un rai de soleil barre encore le bois.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le train arrive, maintenant que le vent s'est tu.",
            "enfant-m|On a attendu, Aniss.",
            "papa|Le carton n'a pas volé.",
            "maman|Rentrez, le seuil est sec.",
            coda,
            "narrateur|Aniss pose une feuille dans la boîte.",
            "narrateur|La feuille ne bouge plus.",
            "narrateur|Une goutte sèche déjà sur la pierre.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La gare, tout près, reçoit le train.",
            "enfant-m|On l'a portée, tous les deux.",
            "papa|La flaque est restée à sa place.",
            "maman|Essuie tes chaussures, Nino.",
            coda,
            "narrateur|Aniss souffle un peu sur le toit.",
            "narrateur|Le feutre noircit, puis s'arrête.",
            "narrateur|Le pain grillé sent encore, derrière la porte.",
        )
    return L(
        "narrateur|Le train suit le rouge, jusqu'à la boîte.",
        "enfant-m|Les pierres étaient sèches.",
        "papa|Le drapeau a tenu, tout droit.",
        "maman|Le vent n'a plus rien à dire.",
        coda,
        "narrateur|Aniss touche le tissu, un instant.",
        "narrateur|Le rouge revient contre le carton.",
        "narrateur|Une abeille passe, puis le jardin se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La porte vitrée jette une barre jaune sur les carreaux.",
        "narrateur|Les carreaux sont tièdes sous les pieds.",
        "narrateur|Dans la cuisine, le pain grille, tout doux.",
        "papa|Ça sent le toast, Nino.",
        "maman|La gare en carton attend au bout.",
        "narrateur|Une boîte, un toit noir au feutre.",
        "narrateur|Le train de bois dort dans le panier.",
        "narrateur|En ce moment, Nino pose un rail.",
        "enfant-m|Il va jusqu'à la gare.",
        "papa|Toute la ligne, jusqu'au bout ?",
        "enfant-m|Oui.",
        "narrateur|La sonnette tinte, une fois.",
        "narrateur|Aniss entre, son sac frotte le sol.",
        "enfant-m|On y va, Aniss !",
        "narrateur|Aniss s'accroupit près des roues.",
        "narrateur|Il les touche, sans un mot.",
        "maman|Tu peux lui tendre quelque chose.",
        "papa|Merci, tu as posé le rail tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le panier reste ouvert, près des pieds.",
        "narrateur|La locomotive, les rails, et le drapeau rouge.",
        "papa|Tu prends quoi d'abord, Nino ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la locomotive", "les rails", "le drapeau")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nino a tendu {o['t1q']}, tout près.",
            "maman|Il tend quoi, à Aniss ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("le couloir", "le salon", "la terrasse")

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
        "Nino veut que son train de bois arrive à la gare en carton. "
        "T1 = locomotive / rails / drapeau (les trois partent). "
        "T2 = couloir (chaussure, rail manquant) / salon (tapis) / terrasse (flaque, vent). "
        "T3 = neuf résolutions (rail du sac, tendre la locomotive, chaussure ; "
        "livre, planche, parquet ; vent, rapprocher la gare, drapeau). "
        "Aniss répond avec les mains, sans étiquette. Nino attend, tend le jouet. "
        "Fin : le train entre dans la boîte.",
        "Gabarit Hugo / cuisine-jardin-chambre / slogan PAR jeté. "
        "Désir ≠ leçon. N2 ≤ 15. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
