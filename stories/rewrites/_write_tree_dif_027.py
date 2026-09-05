#!/usr/bin/env python3
"""TREE-DIF-027 — Les cuillères de Sarah sous la véranda (N1, DIF.PAR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-027"
N1 = 10
TITLE = "Les cuillères de Sarah sous la véranda"
FIL = (
    "Sarah veut que ses cuillères chantent sous la véranda, quand le vent du soir arrive. "
    "Aniss vient jouer ; elle voudrait l'entendre dire ding, "
    "mais Aniss répond avec les mains. "
    "T1 = cuillère / clochette / ficelle, les trois partent. "
    "T2 = étendoir (linge mêlé) / poutre (clou trop haut) / marche (vent trop fort). "
    "T3 = neuf façons d'accrocher. Sarah attend, tend le jouet. Le fil chante, on rentre."
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
    out["characters"] = "Sarah, Aniss, papa, maman"
    out["setting"] = "cuisine, véranda, étendoir, poutre, marche du jardin"
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
        "sara ",
        "hugo",
        "parle peu",
        "camarade",
        "timide",
        "forcer la parole",
        "il faut attendre",
        "un camarade",
        "parc",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "locomotive",
        "gare en carton",
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
        "lab": "la cuillère",
        "cap": "La cuillère",
        "t1q": "la cuillère",
        "t1acc": "cuillère | la cuillère | le métal | tendre",
        "t1retry": "Elle tend la cuillère. Elle tend quoi ?",
        "coda": "Un peu de savon brille encore dans le creux.",
        "voy": "La cuillère voyage déjà dans le panier.",
    },
    2: {
        "lab": "la clochette",
        "cap": "La clochette",
        "t1q": "la clochette",
        "t1acc": "clochette | la clochette | la cloche | tendre",
        "t1retry": "Elle tend la clochette. Elle tend quoi ?",
        "coda": "La clochette penche sur le fil, tout calme.",
        "voy": "La clochette voyage déjà dans le panier.",
    },
    3: {
        "lab": "la ficelle",
        "cap": "La ficelle",
        "t1q": "la ficelle",
        "t1acc": "ficelle | la ficelle | le fil | tendre",
        "t1retry": "Elle tend la ficelle. Elle tend quoi ?",
        "coda": "La ficelle reste contre le bois, tout droite.",
        "voy": "La ficelle voyage déjà dans le panier.",
    },
}

T3_LABS = {
    1: ("le linge", "la cuillère", "le panier"),
    2: ("le tabouret", "le clou plus bas", "les mains d'Aniss"),
    3: ("le vent", "le linge", "le pilier"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah prend d'abord la cuillère chaude.",
            "enfant-f|Elle sent le savon.",
            "papa|Le métal est encore un peu mouillé.",
            "narrateur|Elle la tend vers Aniss, tout près.",
            "enfant-f|Dis ding !",
            "narrateur|Aniss pose un doigt sur le creux.",
            "narrateur|Ça fait un tout petit tic.",
            "maman|La clochette et la ficelle viennent aussi.",
            "narrateur|Papa glisse le tout dans le panier.",
            "narrateur|Rien ne reste sur la table.",
            "enfant-f|Aniss, on part ?",
            "narrateur|Aniss hoche la tête, tout petit.",
            "papa|La cuillère d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah prend d'abord la clochette froide.",
            "enfant-f|Elle va tinter.",
            "maman|Le métal est un peu rêche.",
            "narrateur|Elle la tend vers Aniss.",
            "enfant-f|Dis ding !",
            "narrateur|Aniss la tient à deux mains.",
            "narrateur|Ça tinte une fois, puis s'arrête.",
            "papa|La cuillère et la ficelle viennent aussi.",
            "narrateur|Maman les pose près du panier.",
            "narrateur|Tout part ensemble, déjà.",
            "enfant-f|Aniss, tu viens ?",
            "narrateur|Aniss lève la clochette, tout bas.",
            "maman|La clochette d'abord, vous l'avez.",
        )
    return L(
        "narrateur|Sarah prend d'abord la ficelle douce.",
        "enfant-f|C'est pour le fil.",
        "papa|Elle sent encore le tiroir.",
        "narrateur|Elle tend le peloton vers Aniss.",
        "enfant-f|Dis fil !",
        "narrateur|Aniss enroule un bout, tout lent.",
        "narrateur|Le fil se fait, sans un mot.",
        "maman|La cuillère et la clochette viennent aussi.",
        "narrateur|Papa les glisse près du sac.",
        "narrateur|Le panier les garde, toutes les trois.",
        "enfant-f|Aniss, c'est bon ?",
        "narrateur|Aniss appuie sur le fil, tout calme.",
        "papa|La ficelle d'abord, elle tient.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss prend la cuillère contre lui.",
            "enfant-f|Elle est à toi, un moment.",
            "narrateur|Sarah attend, les mains ouvertes.",
            "narrateur|Un tic se fait, tout petit.",
            "maman|Le métal est tiède, maintenant.",
            "papa|On accroche le fil où ?",
            "enfant-f|Sous la véranda.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss garde la clochette contre sa jambe.",
            "enfant-f|Elle est à toi, un moment.",
            "narrateur|Sarah attend, sans répéter.",
            "narrateur|Le métal sent encore le tiroir.",
            "maman|Le fil peut grandir, après.",
            "papa|On accroche le fil où ?",
            "enfant-f|Sous la véranda.",
        )
    return L(
        "narrateur|Aniss tient encore la ficelle, tout près.",
        "enfant-f|Elle est à toi, un moment.",
        "narrateur|Sarah attend, les lèvres fermées.",
        "narrateur|Le fil bouge un peu, puis s'arrête.",
        "papa|La véranda va le voir, plus tard.",
        "maman|On accroche le fil où ?",
        "enfant-f|Dehors, au bois.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Dehors, le fil peut aller en trois coins.",
        "narrateur|Un linge mouillé barre encore l'étendoir.",
        "narrateur|Plus haut, un clou attend sur la poutre.",
        "narrateur|Plus bas, le vent pousse la marche.",
        "papa|On commence où, pour le fil ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = {
            1: "narrateur|La cuillère frotte le linge mouillé.",
            2: "narrateur|La clochette s'accroche au linge.",
            3: "narrateur|La ficelle s'enroule dans le linge.",
        }[t1]
        return L(
            lead,
            "narrateur|Un torchon barre encore le bois de l'étendoir.",
            "enfant-f|Pousse-le, Aniss !",
            "narrateur|Aniss montre le nœud, du doigt.",
            "narrateur|La ficelle est mêlée, juste là.",
            "enfant-f|Dis-moi où !",
            "maman|Il montre déjà, avec le doigt.",
            "papa|Le linge reste lourd, au milieu.",
            "narrateur|Aniss ouvre un peu le panier.",
            "papa|Vous faites comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|La cuillère n'atteint pas le clou.",
            2: "narrateur|La clochette tinte trop bas, sous le bois.",
            3: "narrateur|La ficelle pend, trop courte, sous la poutre.",
        }[t1]
        return L(
            lead,
            "enfant-f|Le clou est trop haut.",
            "narrateur|Sarah lève les talons, trop petite.",
            "enfant-f|Pousse, Aniss !",
            "narrateur|Aniss lève les bras, tout long.",
            "narrateur|Ses doigts frôlent le bois, pas plus.",
            "maman|Tes bras vont plus loin, Aniss.",
            "papa|Le tabouret dort près du seuil.",
            "narrateur|Un clou plus bas brille aussi.",
            "papa|Vous faites comment, tous les deux ?",
        )
    lead = {
        1: "narrateur|La cuillère claque au vent, trop fort.",
        2: "narrateur|La clochette chante trop vite, déjà.",
        3: "narrateur|La ficelle fouette la marche, tout sec.",
    }[t1]
    return L(
        lead,
        "enfant-f|Le vent est trop grand.",
        "narrateur|Les cuillères se cognent, trop fort.",
        "enfant-f|Aniss, on court ?",
        "narrateur|Aniss recule d'un pas, près du pilier.",
        "narrateur|Il serre le métal contre lui.",
        "maman|Le fil n'aime pas ce vent.",
        "papa|Un linge sec attend sur la marche.",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le nœud du linge reste fermé.",
            "papa|Le linge, la cuillère, ou le panier ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le clou reste trop haut, encore.",
            "maman|Le tabouret, le clou, ou les mains ?",
        )
    return L(
        "narrateur|Le vent tient encore les cuillères.",
        "papa|Le vent, le linge, ou le pilier ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|La cuillère attend près du nœud.",
            2: "narrateur|La clochette attend près du nœud.",
            3: "narrateur|La ficelle attend près du nœud.",
        }[t1]
        return L(
            "enfant-f|On attend.",
            "narrateur|Aniss tire le linge, tout lent.",
            "narrateur|Le nœud s'ouvre, enfin, un peu.",
            wait,
            "narrateur|Aniss accroche le fil au bois libre.",
            "narrateur|Ça fait tic, tout net.",
            "enfant-f|Tic.",
            "papa|Le nœud n'est plus un nœud.",
            "maman|Vous avez laissé le temps au linge.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|La cuillère attend près du bois, déjà.",
            2: "narrateur|La clochette attend près du bois, déjà.",
            3: "narrateur|La ficelle attend près du bois, déjà.",
        }[t1]
        return L(
            "enfant-f|Pour toi.",
            "narrateur|Sarah tend la cuillère vers Aniss.",
            "narrateur|Aniss lève le torchon avec la cuillère.",
            wait,
            "narrateur|Le bois redevient libre, tout doux.",
            "enfant-f|Il passe !",
            "maman|Le fil a pris le bord, tout seul.",
            "papa|Le métal a trouvé le linge.",
        )
    if t2 == 1 and t3 == 3:
        basket = {
            1: "narrateur|La cuillère attend dans le panier.",
            2: "narrateur|La clochette attend dans le panier.",
            3: "narrateur|La ficelle attend dans le panier.",
        }[t1]
        return L(
            "enfant-f|Le panier, Aniss.",
            "narrateur|Aniss pose le fil dedans, sans un mot.",
            "narrateur|Sarah attend, puis suit sa main.",
            basket,
            "narrateur|Ils accrochent, ensuite, au bois libre.",
            "enfant-f|Merci.",
            "papa|Le panier a gardé le calme.",
            "maman|Le linge peut sécher, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        stool = {
            1: "narrateur|La cuillère monte avec le tabouret.",
            2: "narrateur|La clochette monte avec le tabouret.",
            3: "narrateur|La ficelle monte avec le tabouret.",
        }[t1]
        return L(
            "enfant-f|Le tabouret, dessous.",
            "papa|Je vous le tends, à votre hauteur.",
            "narrateur|Aniss monte, Sarah tend le fil.",
            stool,
            "narrateur|Aniss accroche, tout doux, sans parler.",
            "enfant-f|Ça tient !",
            "papa|Le bois a tenu le tabouret.",
            "maman|Aniss a poussé tout doux.",
        )
    if t2 == 2 and t3 == 2:
        nail = {
            1: "narrateur|La cuillère trouve le clou plus bas.",
            2: "narrateur|La clochette trouve le clou plus bas.",
            3: "narrateur|La ficelle trouve le clou plus bas.",
        }[t1]
        return L(
            "enfant-f|On recommence plus bas.",
            "narrateur|Aniss pointe le petit clou, du doigt.",
            "narrateur|Sarah attend, puis suit le doigt.",
            nail,
            "narrateur|Le fil glisse, tout net, sur le fer.",
            "enfant-f|Il glisse.",
            "maman|Le haut garde son ombre, plus loin.",
            "papa|Le bas est plus facile, ici.",
        )
    if t2 == 2 and t3 == 3:
        hands = {
            1: "narrateur|La cuillère part au bout des mains d'Aniss.",
            2: "narrateur|La clochette part au bout des mains d'Aniss.",
            3: "narrateur|La ficelle part au bout des mains d'Aniss.",
        }[t1]
        return L(
            "enfant-f|Tes mains, Aniss.",
            "narrateur|Sarah tend le fil, tout près.",
            "narrateur|Aniss lève les bras, tout long.",
            hands,
            "narrateur|Le fil traverse comme un pont.",
            "enfant-f|On tient ensemble.",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|Le tabouret restera après.",
        )
    if t2 == 3 and t3 == 1:
        wind = {
            1: "narrateur|La cuillère attend sur le seuil, tout calme.",
            2: "narrateur|La clochette attend sur le seuil, tout calme.",
            3: "narrateur|La ficelle retombe, enfin, contre le bois.",
        }[t1]
        return L(
            "enfant-f|On attend le vent.",
            "narrateur|Aniss s'assoit sur la marche, tout calme.",
            "narrateur|Sarah s'assoit aussi, les genoux contre lui.",
            wind,
            "narrateur|Le vent tombe, une feuille s'arrête.",
            "enfant-f|Maintenant.",
            "papa|Le fil ne fouette plus.",
            "maman|Vous avez laissé le vent finir.",
        )
    if t2 == 3 and t3 == 2:
        cloth = {
            1: "narrateur|La cuillère se cache un peu dans le linge.",
            2: "narrateur|La clochette se cache un peu dans le linge.",
            3: "narrateur|La ficelle se cache un peu dans le linge.",
        }[t1]
        return L(
            "enfant-f|Le linge, autour.",
            "narrateur|Sarah tend le linge vers Aniss.",
            "narrateur|Aniss l'enroule, tout lent, sans un mot.",
            cloth,
            "narrateur|Les cuillères ne claquent plus.",
            "enfant-f|C'est doux.",
            "maman|Le vent garde son souffle, plus loin.",
            "papa|Le linge a tenu le métal.",
        )
    pillar = {
        1: "narrateur|La cuillère suit le pilier, pierre après pierre.",
        2: "narrateur|La clochette court le long du pilier, au calme.",
        3: "narrateur|La ficelle tient derrière le pilier, tout droit.",
    }[t1]
    return L(
        "enfant-f|Le pilier, Aniss.",
        "narrateur|Aniss pointe l'ombre, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        pillar,
        "narrateur|Le fil prend le chemin du calme.",
        "enfant-f|Il évite le vent.",
        "papa|Le bois a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = f"narrateur|{OBJ[t1]['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le fil chante une fois, un petit tic.",
            "enfant-m|Tic.",
            "enfant-f|Il est accroché.",
            "papa|Le linge a laissé le bois.",
            "maman|La soupe est prête, dans la cuisine.",
            "narrateur|Aniss pose encore une main sur le fil.",
            coda,
            "narrateur|Une miette de pain attend sur la table.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le fil a contourné le linge, jusqu'au bout.",
            "enfant-f|Aniss l'a levé, tout seul.",
            "papa|Tu as tendu, d'abord.",
            "maman|Venez, le pain est chaud.",
            coda,
            "narrateur|Aniss s'assoit près du panier.",
            "enfant-m|Ding.",
            "narrateur|Le torchon sèche déjà au vent.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le fil court jusqu'au bois, tout droit.",
            "enfant-f|On a posé le panier.",
            "papa|Le calme est rentré à sa place.",
            "maman|Lavez-vous les mains, tout doux.",
            coda,
            "narrateur|Aniss tapote une cuillère, tout léger.",
            "narrateur|Le métal a un peu de poussière.",
            "narrateur|La soupe fume, tout loin, dans la cuisine.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le fil glisse sur le clou, puis tinte.",
            "enfant-f|Le tabouret était juste assez.",
            "papa|Le haut n'a plus pris vos bras.",
            "maman|Rentrez le tabouret, après le chant.",
            coda,
            "enfant-m|Tic.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|La véranda redevient calme, autour du bois.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le petit clou tient le fil, tout net.",
            "enfant-f|On tenait, tous les deux.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Le pain vous attend.",
            coda,
            "narrateur|Aniss essuie une main sur son pantalon.",
            "narrateur|Un grain de savon reste sur le bois.",
            "narrateur|Le fil sent encore le vent chaud.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains d'Aniss laissent le fil chanter.",
            "enfant-f|C'était plus facile, là.",
            "papa|Tes bras ont guidé le fil.",
            "maman|Le haut gardera son ombre.",
            coda,
            "narrateur|Aniss pose un doigt sur une cuillère.",
            "narrateur|Elle bouge, tout petit.",
            "narrateur|Un rai de soleil barre encore le bois.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le fil chante, maintenant que le vent s'est tu.",
            "enfant-f|On a attendu, Aniss.",
            "papa|Le métal n'a pas volé.",
            "maman|Rentrez, le seuil est sec.",
            coda,
            "narrateur|Aniss pose une feuille sur la marche.",
            "narrateur|La feuille ne bouge plus.",
            "narrateur|Une goutte sèche déjà sur le métal.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le linge, tout près, laisse le fil tinter.",
            "enfant-f|On l'a enroulé, tous les deux.",
            "papa|Le vent est resté à sa place.",
            "maman|Essuie tes chaussures, Sarah.",
            coda,
            "narrateur|Aniss souffle un peu sur le métal.",
            "narrateur|Le savon blanchit, puis s'arrête.",
            "narrateur|Le pain grillé sent encore, derrière la porte.",
        )
    return L(
        "narrateur|Le fil suit le pilier, jusqu'au calme.",
        "enfant-f|L'ombre était douce.",
        "papa|Le bois a tenu, tout droit.",
        "maman|Le vent n'a plus rien à dire.",
        coda,
        "narrateur|Aniss touche le fil, un instant.",
        "narrateur|Une cuillère revient contre le bois.",
        "narrateur|Une abeille passe, puis le jardin se tait.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "oiseau"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une cuillère tape le verre, tout léger.",
        "narrateur|Le rideau de la véranda souffle.",
        "narrateur|La soupe sent déjà, dans la cuisine.",
        "papa|Ça tinte, Sarah.",
        "maman|Le fil attend, dehors, encore chaud.",
        "narrateur|Les carreaux de la véranda restent tièdes.",
        "narrateur|En ce moment, Sarah prend la cuillère.",
        "enfant-f|Elle va chanter, dehors.",
        "papa|Avec Aniss, tout à l'heure ?",
        "enfant-f|Oui.",
        "narrateur|Le sac d'Aniss frotte le seuil.",
        "enfant-f|Dis ding !",
        "narrateur|Aniss touche le métal, tout calme.",
        "maman|Tu peux lui tendre quelque chose.",
        "papa|Merci, tu as écouté le tic.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le panier reste ouvert, près des pieds.",
        "narrateur|Une cuillère y brille, encore tiède.",
        "narrateur|Une clochette, puis une ficelle, à côté.",
        "papa|Tu prends quoi d'abord, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la cuillère", "la clochette", "la ficelle")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Sarah a tendu {o['t1q']}, tout près.",
            "maman|Elle tend quoi, à Aniss ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'étendoir", "la poutre", "la marche")

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
        "Sarah veut que ses cuillères chantent sous la véranda. "
        "T1 = cuillère / clochette / ficelle (les trois partent). "
        "T2 = étendoir (linge mêlé) / poutre (clou trop haut) / marche (vent trop fort). "
        "T3 = neuf résolutions (attendre le nœud, tendre la cuillère, panier ; "
        "tabouret, clou plus bas, mains d'Aniss ; vent, linge, pilier). "
        "Aniss répond avec les mains, sans étiquette. Sarah attend, tend le jouet. "
        "Fin : le fil chante, on rentre à la soupe.",
        "Gabarit Sara / parc / cuisine-jardin-chambre / slogan PAR jeté. "
        "Autre récit que DIF-017 (parc d'origine, puis locomotive). "
        "Désir ≠ leçon. N1 ≤ 10. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
