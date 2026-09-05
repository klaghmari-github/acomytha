#!/usr/bin/env python3
"""TREE-DIF-047 — Le camp de Nino, sous la lampe (N2, DIF.ENE.001, chambre)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-047"
N2 = 15
TITLE = "Le camp de Nino, sous la lampe"
FIL = (
    "Nino veut camper dans sa chambre, toute la nuit. "
    "Il prend d'abord la lampe torche, le sac vert ou l'oreiller rayé ; les trois partent. "
    "À la fenêtre le faisceau court, sur le tapis le sac glisse, au pied du lit les genoux dansent. "
    "Il joue avec l'élan, il attend, il demande. "
    "Le camp tient. Nino s'allonge. La lampe fait un rond."
)
CHARS = "Nino, papa, maman"
SETTING = "la chambre de Nino : fenêtre, tapis, pied du lit"


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
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "hyperactif",
        "ce n'est pas une faute",
        "camarade qui bouge",
        "beaucoup d'énergie",
        "cuisine",
        "jardin",
        "dînette",
        "dinette",
        "les cubes",
        "après la sieste",
        "capitaine",
        "plic",
        "volet jaune",
        "boutique",
        "marelle",
        "carrousel",
        "papillon",
        "portail",
        "il faut attendre",
        "on doit demander",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
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
        "lab": "la lampe torche",
        "cap": "La lampe torche",
        "t1q": "dans les mains",
        "t1acc": "mains | les mains | dans les mains | ses mains",
        "t1retry": "La lampe est dans les mains.",
        "coda": "narrateur|La lampe torche garde un rond tiède, tout petit.",
    },
    2: {
        "lab": "le sac vert",
        "cap": "Le sac vert",
        "t1q": "sous le bras",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "Le sac est sous le bras.",
        "coda": "narrateur|Le sac vert garde un pli chaud, près de la fermeture.",
    },
    3: {
        "lab": "l'oreiller rayé",
        "cap": "L'oreiller rayé",
        "t1q": "contre le ventre",
        "t1acc": "ventre | le ventre | contre le ventre | son ventre",
        "t1retry": "L'oreiller est contre le ventre.",
        "coda": "narrateur|L'oreiller rayé garde une chaleur ronde, au creux.",
    },
}

T3_LABS = {
    1: ("les lucioles", "le rideau calme", "maman tient"),
    2: ("le sentier", "la fermeture", "papa ouvre"),
    3: ("les vagues", "le matelas", "maman borde"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord la lampe torche.",
            "enfant-m|Elle est tiède, déjà.",
            "maman|Garde-la dans les mains, tout droit.",
            "narrateur|Le plastique sent encore le savon.",
            "papa|Le sac aussi, près de toi.",
            "narrateur|Maman glisse l'oreiller, tout près.",
            "narrateur|Les trois affaires avancent avec lui.",
            "enfant-m|Le camp va s'ouvrir.",
            "narrateur|Ses pieds tapent déjà le parquet, tout vite.",
            "papa|La lampe d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino passe d'abord le sac vert, sous le bras.",
            "enfant-m|Il gratte un peu, à la manche.",
            "papa|Tiens-le, la nuit est longue.",
            "narrateur|La fermeture fait un petit clic.",
            "maman|La lampe, ensuite, près de toi.",
            "narrateur|Il glisse l'oreiller d'une main.",
            "narrateur|Les trois affaires avancent avec lui.",
            "enfant-m|Je vais dormir là, tout près.",
            "narrateur|Un genou rebondit, puis l'autre.",
            "maman|Le sac d'abord, il est prêt.",
        )
    return L(
        "narrateur|Nino prend d'abord l'oreiller rayé.",
        "enfant-m|Il est doux, contre le ventre.",
        "maman|Garde-le là, tout chaud.",
        "narrateur|Le coton sent encore le linge.",
        "papa|La lampe et le sac, avec toi.",
        "narrateur|Il les pose près des chaussettes.",
        "narrateur|Les trois affaires avancent avec lui.",
        "enfant-m|Ma tête va camper aussi.",
        "narrateur|Ses talons frappent le tapis, trop vite.",
        "papa|L'oreiller d'abord, il est pris.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Dans les mains.",
            "maman|Oui.",
            "narrateur|Un clic de lampe réveille le plafond.",
            "enfant-m|C'est mon soleil de camp.",
            "narrateur|Nino plie un genou, puis l'autre, trop vite.",
            "narrateur|Le faisceau dessine un lapin, puis le perd.",
            "maman|Tes pieds veulent déjà la nuit.",
            "papa|On pose le camp ici ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Sous le bras.",
            "papa|Oui.",
            "narrateur|La fermeture du sac chatouille sa manche.",
            "enfant-m|C'est ma tente, pour ce soir.",
            "narrateur|Nino secoue le sac, un nuage de coton.",
            "narrateur|Un coin vert traîne encore par terre.",
            "maman|Ça sent le linge tiède, déjà.",
            "papa|Tes mains, sur le sac ?",
            "enfant-m|Oui, papa.",
        )
    return L(
        "enfant-m|Contre le ventre.",
        "maman|Oui.",
        "narrateur|Les rayures de l'oreiller dansent un peu.",
        "enfant-m|Ma tête campe dessus.",
        "narrateur|Nino le serre, le lâche, le reprend.",
        "narrateur|Un coin rayé frotte sa joue, tout doux.",
        "maman|La chambre est prête, devant.",
        "papa|On y va, tous les trois ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Nino tapote déjà le parquet, tout léger.",
        "narrateur|Sous la fenêtre, le rideau garde un rai de rue.",
        "narrateur|Au milieu, le tapis fait un carré chaud.",
        "narrateur|Près du bois, le pied du lit attend.",
        "papa|On campe où, Nino ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Nino porte la lampe vers le rideau.",
            2: "narrateur|Nino traîne le sac vers le rideau.",
            3: "narrateur|Nino pousse l'oreiller vers le rideau.",
        }[t1]
        mishap = {
            1: "narrateur|Le faisceau devient un lapin, puis s'enfuit.",
            2: "narrateur|Le sac cogne le rebord, clic trop fort.",
            3: "narrateur|L'oreiller tape le bois, rebondit trop haut.",
        }[t1]
        return L(
            lead,
            "narrateur|Ses talons tambourinent le parquet.",
            "enfant-m|Le camp, c'est là, papa !",
            mishap,
            f"enfant-m|{o['cap']} part trop vite.",
            "maman|Tes pieds dansent, ce soir.",
            "papa|Le rideau n'est pas encore une tente.",
            "enfant-m|On campe comment, alors ?",
            "papa|Tu fais comment, avec nous ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Nino pose la lampe au milieu du tapis.",
            2: "narrateur|Nino déroule le sac au milieu du tapis.",
            3: "narrateur|Nino jette l'oreiller au milieu du tapis.",
        }[t1]
        mishap = {
            1: "narrateur|Le faisceau roule, et le rond se perd.",
            2: "narrateur|Le sac glisse comme un escargot trop pressé.",
            3: "narrateur|L'oreiller file, une rayure après l'autre.",
        }[t1]
        return L(
            lead,
            "enfant-m|Ici, c'est la clairière, maman.",
            "narrateur|Ses genoux font un petit trampoline.",
            mishap,
            "narrateur|Un fil de laine se lève, puis retombe.",
            "maman|Ton corps veut encore courir.",
            "papa|Le tapis n'a pas encore de tente.",
            "enfant-m|On peut jouer avec, quand même ?",
            "papa|Vous trouvez, tous les trois ?",
        )
    lead = {
        1: "narrateur|Nino glisse la lampe au pied du lit.",
        2: "narrateur|Nino pousse le sac au pied du lit.",
        3: "narrateur|Nino pose l'oreiller au pied du lit.",
    }[t1]
    mishap = {
        1: "narrateur|Le rond grimpe au bois, trop haut, trop vite.",
        2: "narrateur|Le sac se faufile sous le bois, tout seul.",
        3: "narrateur|L'oreiller disparaît sous le drap, trop loin.",
    }[t1]
    return L(
        lead,
        "enfant-m|Ici, c'est la grotte, papa.",
        "narrateur|Le bois du lit renvoie chaque pas.",
        mishap,
        f"narrateur|{o['cap']} n'est plus à sa place.",
        "maman|Tes genoux font trop de vagues.",
        "papa|Le camp n'a pas encore de toit.",
        "enfant-m|On s'allonge comment, alors ?",
        "papa|Vous trouvez, tous les trois ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le lapin de lumière court encore.",
            "papa|Les lucioles, le rideau, ou maman ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le sac n'a pas encore de forme.",
            "maman|Le sentier, la fermeture, ou papa ?",
        )
    return L(
        "narrateur|Le bois du lit tremble encore un peu.",
        "papa|Les vagues, le matelas, ou maman ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Nino cligne la lampe, un, deux, trois.",
            2: "narrateur|Nino cligne, le sac devient une colline.",
            3: "narrateur|Nino cligne, l'oreiller devient un nuage.",
        }[t1]
        return L(
            "enfant-m|On joue aux lucioles.",
            "papa|Toi tu clignes, moi je compte.",
            hold,
            "narrateur|Des points d'or s'allument sur le rideau.",
            "narrateur|Nino cligne encore, puis s'arrête.",
            "enfant-m|Les lucioles sont fatiguées.",
            "maman|Le camp a sa lumière, maintenant.",
            "papa|Vous avez dansé, puis posé.",
            "narrateur|Le tissu redevient un mur, tout doux.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|La lampe repose contre le rebord, éteinte.",
            2: "narrateur|Le sac repose contre le rebord, plié.",
            3: "narrateur|L'oreiller repose contre le rebord, sage.",
        }[t1]
        return L(
            "enfant-m|On attend le rideau.",
            "narrateur|Nino pose les genoux au parquet.",
            wait,
            "narrateur|Le volet tape une fois, puis plus.",
            "enfant-m|Il ne bouge plus ?",
            "maman|Le tissu est calme, oui.",
            "papa|Tes pieds se sont assis, eux aussi.",
            "narrateur|Nino rallume, tout droit, tout petit.",
            "enfant-m|Le camp peut s'ouvrir.",
        )
    if t2 == 1 and t3 == 3:
        hand = {
            1: "narrateur|Maman prend la lampe, Nino tend le sac.",
            2: "narrateur|Maman tient le sac, Nino tend la lampe.",
            3: "narrateur|Maman tient l'oreiller, Nino tend la lampe.",
        }[t1]
        return L(
            "enfant-m|Maman, tu tiens, s'il te plaît ?",
            "maman|Je tiens, tu poses le camp.",
            hand,
            "narrateur|Nino étale le sac sous le rai de rue.",
            "narrateur|Le faisceau reste sage, dans sa main.",
            "enfant-m|Toi tu tiens, moi je range.",
            "papa|Vous avez demandé, et ça tient.",
            "maman|Ma main fait le piquet, ce soir.",
            "narrateur|La fenêtre garde un rai, tout mince.",
        )
    if t2 == 2 and t3 == 1:
        pair = {
            1: "narrateur|Nino pose la lampe, papa marque le sentier.",
            2: "narrateur|Nino pose le sac, papa marque le sentier.",
            3: "narrateur|Nino pose l'oreiller, papa marque le sentier.",
        }[t1]
        return L(
            "enfant-m|On fait un sentier.",
            "papa|Toi tu sautes, moi je suis derrière.",
            pair,
            "narrateur|Des pas dessinent un chemin sur le tapis.",
            "narrateur|Nino saute une case, papa une autre.",
            "enfant-m|La clairière est au bout.",
            "maman|Vous avez joué, puis posé le sac.",
            "papa|Le tapis est devenu un chemin.",
            "narrateur|Un fil de laine reste, tout petit.",
        )
    if t2 == 2 and t3 == 2:
        line = {
            1: "narrateur|Nino tient la lampe, le sac attend.",
            2: "narrateur|Nino tient le sac, la fermeture attend.",
            3: "narrateur|Nino tient l'oreiller, le sac attend.",
        }[t1]
        return L(
            "enfant-m|J'attends la fermeture.",
            "papa|Moi je l'ouvre, puis c'est toi.",
            line,
            "narrateur|Le zip avance, dent après dent.",
            "narrateur|Nino souffle, les épaules baissent.",
            "papa|C'est à toi, Nino.",
            "enfant-m|J'y glisse un pied.",
            "maman|Chacun son tour, sur le tapis.",
            "narrateur|La tente verte s'ouvre, enfin.",
        )
    if t2 == 2 and t3 == 3:
        open_ = {
            1: "narrateur|Papa ouvre le sac près de la lampe.",
            2: "narrateur|Papa ouvre le sac, tout grand.",
            3: "narrateur|Papa ouvre le sac près de l'oreiller.",
        }[t1]
        return L(
            "enfant-m|Papa, tu ouvres le sac ?",
            "papa|Je l'ouvre, tout doux.",
            open_,
            "narrateur|Nino glisse un pied, les genoux se posent.",
            "narrateur|L'autre pied suit, la lampe au calme.",
            "enfant-m|Toi tu ouvres, moi j'entre.",
            "maman|Vous avez demandé, et ça marche.",
            "papa|Le sac tient tout seul, maintenant.",
            "narrateur|Un carré de tapis reste tiède, autour.",
        )
    if t2 == 3 and t3 == 1:
        train = {
            1: "narrateur|La lampe voyage d'un genou à l'autre.",
            2: "narrateur|Le sac voyage d'un genou à l'autre.",
            3: "narrateur|L'oreiller voyage d'un genou à l'autre.",
        }[t1]
        return L(
            "enfant-m|On fait des vagues.",
            "papa|Tu rebondis, puis tu t'arrêtes.",
            train,
            "narrateur|Le bois devient une mer, puis une rive.",
            "enfant-m|Doucement, les vagues tiennent.",
            "maman|Vous avez joué, puis calmé le lit.",
            "papa|Le pied du lit est une grotte.",
            f"narrateur|{o['cap']} a trouvé son coin.",
            "enfant-m|Le camp est là, tout bas.",
        )
    if t2 == 3 and t3 == 2:
        hush = {
            1: "narrateur|La lampe reste éteinte, au creux du sac.",
            2: "narrateur|Le sac reste fermé, au creux du bois.",
            3: "narrateur|L'oreiller reste sage, au creux du bois.",
        }[t1]
        return L(
            "enfant-m|On attend le matelas.",
            "papa|Quand il se tait, tu t'allonges.",
            "narrateur|Un saut, puis le bois reste calme.",
            hush,
            "narrateur|Le matelas se tait, enfin.",
            "enfant-m|Maintenant !",
            "maman|Le lit a fini ses vagues.",
            "papa|Tes genoux se sont assis, eux aussi.",
            "narrateur|Un pli du drap retombe, tout lent.",
        )
    tuck = {
        1: "narrateur|Maman borde le sac, Nino tient la lampe.",
        2: "narrateur|Maman borde le sac, tout près du bois.",
        3: "narrateur|Maman borde le sac autour de l'oreiller.",
    }[t1]
    return L(
        "enfant-m|Maman, tu bordes le sac ?",
        "maman|Je le borde, tout chaud.",
        tuck,
        "narrateur|Nino écoute les mains, plus que ses pieds.",
        "papa|Tu t'allonges, et ça tient.",
        "enfant-m|Moi aussi, j'écoute.",
        "narrateur|Le pied du lit devient un toit.",
        "papa|Vous avez demandé le bord.",
        "maman|Mes mains ont tenu le camp.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le dernier rond du rideau est à eux.",
            "enfant-m|On a joué, chacun son tour.",
            "papa|Toi tu bougais, moi je suivais.",
            "maman|Vous avez laissé l'élan dessiner.",
            "narrateur|La chambre sent encore le savon.",
            coda,
            "narrateur|Un trait clair dort sur le bois.",
            "enfant-m|On s'allonge, papa.",
            "narrateur|Les chaussettes retrouvent le tapis tiède.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le rebord de la fenêtre garde encore la chaleur.",
            "enfant-m|Je me suis arrêté, d'abord.",
            "papa|Puis le faisceau est resté droit.",
            "maman|L'élan s'est assis, puis il a campé.",
            "narrateur|Le rideau redevient calme.",
            coda,
            "narrateur|Une poussière reste coincée, tout près.",
            "enfant-m|À demain, les ronds.",
            "narrateur|Le volet brille un peu, puis se tait.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|La main de maman reste dans l'air, tout légère.",
            "enfant-m|J'ai attendu le pas.",
            "papa|On a demandé, et ça allait.",
            "maman|Sa main a tenu vos pieds.",
            "narrateur|La chambre vous rend le silence.",
            f"narrateur|{o['cap']} pose un grain de lumière sur le bois.",
            "narrateur|Nino touche le rideau, du bout.",
            "enfant-m|Il est à nous.",
            "narrateur|Un rai de rue barre encore le tissu.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Deux paires de chaussettes marquent le bout du tapis.",
            "enfant-m|Toi devant, moi derrière.",
            "papa|Tes jambes allaient plus loin.",
            "maman|Vous avez sauté avec l'élan, pas contre.",
            "narrateur|Le tapis redevient chaud, et calme.",
            coda,
            "narrateur|Un peu de laine sèche déjà sur le tissu.",
            "enfant-m|On s'allonge, le sentier reste.",
            "narrateur|Le lit fait une ombre longue.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Le bout du tapis attend encore, tout lisse.",
            "papa|J'ai ouvert, puis c'était toi.",
            "enfant-m|J'ai attendu ta place.",
            "maman|Chacun son tour, sur le tissu.",
            "narrateur|L'élan a laissé la place.",
            f"narrateur|{o['cap']} garde un grain de poussière.",
            "narrateur|Nino souffle dessus, tout doux.",
            "enfant-m|On se dit au revoir, tapis.",
            "narrateur|Un fil oublié sèche contre le pied.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Le sac de papa repose sur le tapis.",
            "enfant-m|Tu l'ouvrais, tout grand.",
            "papa|On a demandé, et ça allait juste.",
            "maman|L'ouverture a fait le tour, rien de plus.",
            "narrateur|Le tapis a rendu le calme.",
            coda,
            "narrateur|Un rond de chaleur reste sur le tissu.",
            "enfant-m|Regarde, papa, il brille.",
            "narrateur|Les chaussettes retrouvent le parquet, au frais.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les vagues s'arrêtent contre le pied du lit.",
            "enfant-m|On est arrivés, tous les deux.",
            "papa|Tu rebondissais, puis tu t'arrêtais.",
            "maman|Le bois est redevenu un lit, simplement.",
            "narrateur|L'élan s'est couché.",
            coda,
            "narrateur|Une poussière tourne encore, puis tombe.",
            "enfant-m|On s'allonge, les vagues se taisent.",
            "narrateur|Dans la chambre, le camp redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le matelas s'est tu, enfin, tout à fait.",
            "enfant-m|On a attendu le bois.",
            "papa|Quand il était calme, on s'allongeait.",
            "maman|Le pied vous a laissé le sac.",
            "narrateur|L'élan a écouté le bois.",
            f"narrateur|{o['cap']} ne fait plus aucun bruit.",
            "narrateur|Nino pose la paume sur le bois tiède.",
            "enfant-m|Il est tiède.",
            "narrateur|Un grillon passe derrière le volet, sans crier.",
        )
    return L(
        "narrateur|Les mains de maman s'éteignent, un à un.",
        "enfant-m|J'écoutais tes mains.",
        "papa|Moi aussi, je bordais avec toi.",
        "maman|Vous avez demandé le bord.",
        "narrateur|Le lit a rendu vos pas.",
        coda,
        "narrateur|Nino touche le sac, du bout des doigts.",
        "enfant-m|Il est à nous, maman.",
        "narrateur|Le coton garde une poussière, puis plus rien.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Un grillon chante, tout bas, derrière le volet.",
        "narrateur|Ça sent encore le savon, dans le couloir.",
        "narrateur|La chambre de Nino garde une lampe ronde.",
        "narrateur|Elle fait un cercle pâle, au plafond.",
        "papa|Tes chaussettes sont trop chaudes, Nino ?",
        "enfant-m|Un peu, papa.",
        "narrateur|Maman pose l'oreiller rayé sur le tapis.",
        "maman|Il attend le camp, tu le vois ?",
        "enfant-m|Il veut dormir, tout grand.",
        "narrateur|En ce moment, Nino touche la lampe torche.",
        "enfant-m|Je veux camper ici, toute la nuit.",
        "papa|On prépare les affaires, alors ?",
        "maman|La lampe, le sac, et l'oreiller.",
        "papa|Merci, tu tiens la lampe tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près des chaussettes.",
        "narrateur|La lampe, le sac, et l'oreiller.",
        "maman|Tu prends quoi d'abord, Nino ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la lampe torche", "le sac vert", "l'oreiller rayé")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        if t1 == 1:
            s[f"{p}_Q0001"] = L(
                "narrateur|Nino a mis la lampe torche.",
                "maman|Elle est où, maintenant ?",
            )
        elif t1 == 2:
            s[f"{p}_Q0001"] = L(
                "narrateur|Nino a passé le sac vert.",
                "maman|Il est où, maintenant ?",
            )
        else:
            s[f"{p}_Q0001"] = L(
                "narrateur|Nino a pris l'oreiller rayé.",
                "maman|Il est où, maintenant ?",
            )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la fenêtre", "le tapis", "le pied du lit")
        sons[p] = ""
        sons[f"{p}_T0002_P0000"] = ""

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            sons[sp] = ""
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Nino veut camper dans sa chambre toute la nuit. "
        "T1 = lampe torche / sac vert / oreiller rayé (les trois partent). "
        "T2 = fenêtre (faisceau, rideau) / tapis (glisse, genoux) / pied du lit (rebonds). "
        "T3 = neuf résolutions (lucioles, rideau calme, maman tient ; "
        "sentier, fermeture, papa ouvre ; "
        "vagues, matelas, maman borde). "
        "L'élan de Nino se vit, sans slogan. Fin : le camp tient, il s'allonge.",
        "N2 ≤ 15. Héros Nino, papa/maman, troupe D16. "
        "Cuisine/jardin/chambre, cubes/livre/dînette, matin/sieste/soir jetés. "
        "Chambre (pas marché, pas marelle, pas carrousel, pas papillon, pas portail). "
        "Titre slogan remplacé (objet + désir). Un merci de papa lié au geste "
        "(tenir la lampe). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
