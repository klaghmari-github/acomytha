#!/usr/bin/env python3
"""TREE-DIF-063 — Le ticket rouge de Victorino, vers le lac (N2, DIF.ENE.001, train)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-063"
N2 = 15
TITLE = "Le ticket rouge de Victorino, vers le lac"
FIL = (
    "Victorino veut garder son ticket rouge jusqu'au lac. "
    "Il prend d'abord le ticket, le sac bleu ou la pomme ; les trois montent. "
    "Dans l'allée ses pieds courent, à la fenêtre le pré file, à la tablette ça saute. "
    "Il joue avec l'élan, il attend, il demande. "
    "Le tunnel passe. Le lac arrive. Le ticket reste dans sa main."
)
CHARS = "Victorino, papa, maman"
SETTING = "le quai, puis le wagon : allée, fenêtre, tablette"


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
        "sami",
        "citronnade",
        "grillon",
        "navire",
        "bateau",
        "camp de",
        "sous la lampe",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
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
        "lab": "le ticket rouge",
        "cap": "Le ticket rouge",
        "t1q": "dans la main",
        "t1acc": "main | la main | dans la main | sa main | les mains",
        "t1retry": "Le ticket est dans la main.",
        "coda": "narrateur|Le ticket rouge garde un pli chaud, tout petit.",
    },
    2: {
        "lab": "le sac bleu",
        "cap": "Le sac bleu",
        "t1q": "sous le bras",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "Le sac est sous le bras.",
        "coda": "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
    },
    3: {
        "lab": "la pomme",
        "cap": "La pomme",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "La pomme est dans la poche.",
        "coda": "narrateur|La pomme garde une peau lisse, un peu tiède.",
    },
}

T3_LABS = {
    1: ("les petits pas", "les roues", "papa tient"),
    2: ("les arbres", "le tunnel", "maman tient"),
    3: ("la pomme", "la tablette calme", "papa ouvre"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorino prend d'abord le ticket rouge.",
            "enfant-m|Il est tiède, déjà.",
            "maman|Garde-le dans la main, tout droit.",
            "narrateur|Le papier sent encore l'encre.",
            "papa|Le sac aussi, près de toi.",
            "narrateur|Maman glisse la pomme, tout près.",
            "narrateur|Les trois affaires montent avec lui.",
            "enfant-m|Le lac va arriver.",
            "narrateur|Ses pieds tapent déjà le quai, tout vite.",
            "papa|Le ticket d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorino passe d'abord le sac bleu, sous le bras.",
            "enfant-m|Il pèse un peu, à l'épaule.",
            "papa|Tiens-le, le voyage est long.",
            "narrateur|La boucle fait un petit clic.",
            "maman|Le ticket, ensuite, près de toi.",
            "narrateur|Il glisse la pomme d'une main.",
            "narrateur|Les trois affaires montent avec lui.",
            "enfant-m|Je vais voir le lac, tout près.",
            "narrateur|Un genou rebondit, puis l'autre.",
            "maman|Le sac d'abord, il est prêt.",
        )
    return L(
        "narrateur|Victorino prend d'abord la pomme.",
        "enfant-m|Elle est froide, contre la poche.",
        "maman|Garde-la là, tout près.",
        "narrateur|La peau sent encore le panier.",
        "papa|Le ticket et le sac, avec toi.",
        "narrateur|Il les pose près du banc.",
        "narrateur|Les trois affaires montent avec lui.",
        "enfant-m|Ma pomme va voyager aussi.",
        "narrateur|Ses talons frappent le quai, trop vite.",
        "papa|La pomme d'abord, elle est prise.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Dans la main.",
            "maman|Oui.",
            "narrateur|Un sifflet réveille le quai.",
            "enfant-m|C'est mon train, pour le lac.",
            "narrateur|Victorino plie un genou, puis l'autre, trop vite.",
            "narrateur|Le ticket dessine un pli, puis le perd.",
            "maman|Tes pieds veulent déjà le wagon.",
            "papa|On monte ici ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Sous le bras.",
            "papa|Oui.",
            "narrateur|La boucle du sac chatouille sa manche.",
            "enfant-m|C'est mon coin, pour le lac.",
            "narrateur|Victorino secoue le sac, un nuage de laine.",
            "narrateur|Un coin bleu traîne encore par terre.",
            "maman|Ça sent le quai tiède, déjà.",
            "papa|Tes mains, sur le sac ?",
            "enfant-m|Oui, papa.",
        )
    return L(
        "enfant-m|Dans la poche.",
        "maman|Oui.",
        "narrateur|La pomme roule un peu, puis s'arrête.",
        "enfant-m|Elle voyage contre moi.",
        "narrateur|Victorino la serre, la lâche, la reprend.",
        "narrateur|Un reflet rouge frotte sa poche, tout doux.",
        "maman|Le wagon est prêt, devant.",
        "papa|On y va, tous les trois ?",
        "enfant-m|Oui.",
    )


def t2_question(t1: int) -> list[str]:
    o = OBJ[t1]
    return L(
        f"narrateur|{o['cap']} voyage déjà, trop vite.",
        "narrateur|Dans l'allée, le caoutchouc garde un pli.",
        "narrateur|À la vitre, un pré file tout vert.",
        "narrateur|Près des genoux, la tablette attend.",
        "papa|On s'installe où, Victorino ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Victorino porte le ticket vers l'allée.",
            2: "narrateur|Victorino avance le sac vers l'allée.",
            3: "narrateur|Victorino avance, la pomme dans la poche.",
        }[t1]
        mishap = {
            1: "narrateur|Le ticket glisse, trop vite, tout seul.",
            2: "narrateur|Le sac cogne un siège, clic trop fort.",
            3: "narrateur|La pomme tape sa poche, trop haut.",
        }[t1]
        return L(
            lead,
            "narrateur|Ses talons tambourinent le caoutchouc.",
            "enfant-m|Le lac, c'est par là, papa !",
            mishap,
            f"enfant-m|{o['cap']} part trop vite.",
            "maman|Tes pieds dansent, dans le wagon.",
            "papa|L'allée n'est pas encore un chemin.",
            "enfant-m|On avance comment, alors ?",
            "papa|Tu fais comment, avec nous ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Victorino pose le ticket contre la vitre.",
            2: "narrateur|Victorino pose le sac sous la vitre.",
            3: "narrateur|Victorino pose la pomme contre la vitre.",
        }[t1]
        mishap = {
            1: "narrateur|Le ticket file, et le pli se perd.",
            2: "narrateur|Le sac glisse comme un wagon trop pressé.",
            3: "narrateur|La pomme file, une bosse après l'autre.",
        }[t1]
        return L(
            lead,
            "enfant-m|Ici, je vois le lac, maman.",
            "narrateur|Ses genoux font un petit trampoline.",
            mishap,
            "narrateur|Un pré passe, puis un autre.",
            "maman|Ton corps veut encore courir.",
            "papa|La vitre n'a pas encore le lac.",
            "enfant-m|On peut jouer avec, quand même ?",
            "papa|Vous trouvez, tous les trois ?",
        )
    lead = {
        1: "narrateur|Victorino glisse le ticket sur la tablette.",
        2: "narrateur|Victorino pousse le sac sur la tablette.",
        3: "narrateur|Victorino pose la pomme sur la tablette.",
    }[t1]
    mishap = {
        1: "narrateur|Le ticket grimpe au bord, trop haut, trop vite.",
        2: "narrateur|Le sac se faufile sous la tablette, tout seul.",
        3: "narrateur|La pomme disparaît vers le bord, trop loin.",
    }[t1]
    return L(
        lead,
        "enfant-m|Ici, c'est ma table, papa.",
        "narrateur|Le bois plié renvoie chaque secousse.",
        mishap,
        f"narrateur|{o['cap']} n'est plus à sa place.",
        "maman|Tes genoux font trop de vagues.",
        "papa|La tablette n'a pas encore de repas.",
        "enfant-m|On pose comment, alors ?",
        "papa|Vous trouvez, tous les trois ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'allée tremble encore un peu.",
            "papa|Les petits pas, les roues, ou papa ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le pré file encore trop vite.",
            "maman|Les arbres, le tunnel, ou maman ?",
        )
    return L(
        "narrateur|La tablette n'a pas encore de calme.",
        "papa|La pomme, la tablette, ou papa ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Victorino tape, le ticket dans la main.",
            2: "narrateur|Victorino tape, le sac sous le bras.",
            3: "narrateur|Victorino tape, la pomme dans la poche.",
        }[t1]
        return L(
            "enfant-m|On fait les petits pas.",
            "papa|Toi tu tapes, moi je compte.",
            hold,
            "narrateur|Les roues répondent, sous le plancher.",
            "narrateur|Il tape encore, puis s'arrête.",
            "enfant-m|Les petits pas sont fatigués.",
            "maman|Le banc a sa place, maintenant.",
            "papa|Vous avez dansé, puis posé.",
            "narrateur|L'allée redevient un chemin, tout étroit.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le ticket repose contre le dossier, sage.",
            2: "narrateur|Le sac repose contre le dossier, plié.",
            3: "narrateur|La pomme repose contre le dossier, sage.",
        }[t1]
        return L(
            "enfant-m|On attend les roues.",
            "narrateur|Victorino pose les genoux au banc.",
            wait,
            "narrateur|Les roues changent une fois, puis plus.",
            "enfant-m|Elles ne dansent plus ?",
            "maman|Le plancher est calme, oui.",
            "papa|Tes pieds ont trouvé le banc, eux aussi.",
            "narrateur|Victorino souffle, tout droit, tout petit.",
            "enfant-m|Le lac peut arriver.",
        )
    if t2 == 1 and t3 == 3:
        hand = {
            1: "narrateur|Papa prend la main, Victorino tient le ticket.",
            2: "narrateur|Papa prend la main, Victorino tient le sac.",
            3: "narrateur|Papa prend la main, Victorino tient la pomme.",
        }[t1]
        keep = {
            1: "narrateur|Le ticket reste sage, dans sa main.",
            2: "narrateur|Le sac reste sage, sous le bras.",
            3: "narrateur|La pomme reste sage, dans la poche.",
        }[t1]
        return L(
            "enfant-m|Papa, tu tiens, s'il te plaît ?",
            "papa|Je tiens, tu poses tes pieds.",
            hand,
            "narrateur|Victorino avance, un pas, puis l'autre.",
            keep,
            "enfant-m|Toi tu tiens, moi je marche.",
            "maman|Vous avez demandé, et ça tient.",
            "papa|Ma main fait le rail, ici.",
            "narrateur|L'allée garde un pli, tout mince.",
        )
    if t2 == 2 and t3 == 1:
        pair = {
            1: "narrateur|Victorino pose le ticket, papa montre un arbre.",
            2: "narrateur|Victorino pose le sac, papa montre un arbre.",
            3: "narrateur|Victorino pose la pomme, papa montre un arbre.",
        }[t1]
        return L(
            "enfant-m|On compte les arbres.",
            "papa|Toi tu pointes, moi je compte.",
            pair,
            "narrateur|Des ombres courent sur la vitre.",
            "narrateur|Victorino pointe une, papa une autre.",
            "enfant-m|Le lac est après.",
            "maman|Vous avez joué, puis posé les yeux.",
            "papa|La vitre est devenue un pré.",
            "narrateur|Un reflet vert reste, tout petit.",
        )
    if t2 == 2 and t3 == 2:
        line = {
            1: "narrateur|Victorino tient le ticket, le noir attend.",
            2: "narrateur|Victorino tient le sac, le noir attend.",
            3: "narrateur|Victorino tient la pomme, le noir attend.",
        }[t1]
        return L(
            "enfant-m|J'attends le tunnel.",
            "papa|Quand il est noir, tu restes.",
            line,
            "narrateur|La vitre devient sombre, bout après bout.",
            "narrateur|Victorino souffle, les épaules baissent.",
            "papa|C'est à toi, Victorino.",
            "enfant-m|Je colle mon nez.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le jour revient, enfin.",
        )
    if t2 == 2 and t3 == 3:
        hold = {
            1: "narrateur|Maman tient Victorino, près du ticket.",
            2: "narrateur|Maman tient Victorino, près du sac.",
            3: "narrateur|Maman tient Victorino, près de la pomme.",
        }[t1]
        return L(
            "enfant-m|Maman, tu tiens, s'il te plaît ?",
            "maman|Je tiens, tu regardes le pré.",
            hold,
            "narrateur|Victorino colle le nez, les genoux se posent.",
            "narrateur|L'autre pied suit, la vitre au calme.",
            "enfant-m|Toi tu tiens, moi je vois.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Mes bras font la rambarde, maintenant.",
            "narrateur|Un carré de ciel reste bleu, autour.",
        )
    if t2 == 3 and t3 == 1:
        roll = {
            1: "narrateur|La pomme voyage vers le ticket.",
            2: "narrateur|La pomme voyage vers le sac.",
            3: "narrateur|La pomme voyage d'un bord à l'autre.",
        }[t1]
        return L(
            "enfant-m|On fait rouler la pomme.",
            "papa|Tu la rattrapes, puis tu t'arrêtes.",
            roll,
            "narrateur|Le bois devient une pente, puis une rive.",
            "enfant-m|Doucement, la pomme tient.",
            "maman|Vous avez joué, puis calmé la table.",
            "papa|La tablette est une table, maintenant.",
            f"narrateur|{o['cap']} a trouvé son coin.",
            "enfant-m|Le goûter est là, tout bas.",
        )
    if t2 == 3 and t3 == 2:
        hush = {
            1: "narrateur|Le ticket reste sage, au creux de la table.",
            2: "narrateur|Le sac reste fermé, au creux de la table.",
            3: "narrateur|La pomme reste sage, au creux de la table.",
        }[t1]
        return L(
            "enfant-m|On attend la tablette.",
            "papa|Quand elle se tait, tu poses.",
            "narrateur|Une secousse, puis le bois reste calme.",
            hush,
            "narrateur|La tablette se tait, enfin.",
            "enfant-m|Maintenant !",
            "maman|Le bois a fini ses vagues.",
            "papa|Tes genoux ont trouvé le banc, eux aussi.",
            "narrateur|Un pli du bois retombe, tout lent.",
        )
    open_ = {
        1: "narrateur|Papa ouvre le sac, près du ticket.",
        2: "narrateur|Papa ouvre le sac, tout grand.",
        3: "narrateur|Papa ouvre le sac, près de la pomme.",
    }[t1]
    return L(
        "enfant-m|Papa, tu ouvres le goûter ?",
        "papa|Je l'ouvre, tout doux.",
        open_,
        "narrateur|Victorino écoute les mains, plus que ses pieds.",
        "papa|Tu poses, et ça tient.",
        "enfant-m|Moi aussi, j'écoute.",
        "narrateur|La tablette devient une table.",
        "papa|Vous avez demandé l'ouverture.",
        "maman|Mes mains ont tenu le bord.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Victorino s'assoit, le sac contre le banc.",
            "enfant-m|Les petits pas sont couchés, papa.",
            "papa|Toi tu tapais, moi je comptais.",
            "maman|Le wagon a sa place, maintenant.",
            "narrateur|Le quai a laissé le fer, derrière.",
            coda,
            "narrateur|Un reflet d'eau dort sur la vitre.",
            "enfant-m|Bonjour, lac.",
            "narrateur|Les pieds retrouvent le caoutchouc tiède.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Victorino s'assoit, les roues tout calmes.",
            "enfant-m|J'ai attendu le plancher, d'abord.",
            "papa|Puis les roues sont restées sages.",
            "maman|Tes pieds ont trouvé le banc, eux aussi.",
            "narrateur|L'allée ne danse plus.",
            coda,
            "narrateur|Une poussière reste coincée, tout près.",
            "enfant-m|À tout à l'heure, les rails.",
            "narrateur|Le dossier brille un peu, puis se tait.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Victorino s'assoit, la main de papa tout près.",
            "enfant-m|Tu tenais le rail.",
            "papa|Vous avez demandé, et ça tenait.",
            "maman|Sa main a fait le chemin.",
            "narrateur|Le wagon rend le silence, tout doux.",
            f"narrateur|{o['cap']} pose un grain de lumière.",
            "narrateur|Victorino touche la vitre, du bout.",
            "enfant-m|Le lac est à nous.",
            "narrateur|Un rai d'eau barre encore le verre.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Victorino s'assoit au bout des arbres.",
            "enfant-m|Toi tu comptais, moi je pointais.",
            "papa|Tes doigts ont fait le pré.",
            "maman|La vitre est devenue un lac.",
            "narrateur|Le verre redevient froid, et calme.",
            coda,
            "narrateur|Un peu de buée sèche déjà.",
            "enfant-m|Les arbres restent, maman.",
            "narrateur|Le siège garde une chaleur ronde.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Victorino s'assoit, le jour revenu.",
            "papa|J'ai compté le noir, puis c'était toi.",
            "enfant-m|J'ai attendu le tunnel.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le lac tient, enfin.",
            f"narrateur|{o['cap']} garde un grain de buée.",
            "narrateur|Victorino souffle dessus, tout doux.",
            "enfant-m|Bonjour, vitre.",
            "narrateur|Un fil d'eau sèche contre le bas.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Victorino s'assoit, tenu par maman.",
            "enfant-m|Tu tenais, tout près.",
            "papa|Les bras ont fait la rambarde.",
            "maman|La fenêtre est à vous.",
            "narrateur|Le verre a rendu le calme.",
            coda,
            "narrateur|Un rond de buée reste sur le froid.",
            "enfant-m|Regarde, papa, il brille.",
            "narrateur|Les pieds retrouvent le plancher, au frais.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Victorino s'assoit devant la tablette.",
            "enfant-m|La pomme est sage, papa.",
            "papa|Tu la rattrapais, puis tu t'arrêtais.",
            "maman|La table a son goûter, maintenant.",
            "narrateur|Le bois est redevenu plat.",
            coda,
            "narrateur|Une poussière tourne encore, puis tombe.",
            "enfant-m|La pomme se tait.",
            "narrateur|Dans le wagon, le lac tient.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Victorino s'assoit, la tablette tout calme.",
            "enfant-m|On a attendu le bois.",
            "papa|Quand il s'est tu, tu as posé.",
            "maman|La tablette a fait une table.",
            "narrateur|Tes genoux ont trouvé le banc.",
            f"narrateur|{o['cap']} ne fait plus aucun bruit.",
            "narrateur|Victorino pose la paume sur le bois tiède.",
            "enfant-m|Il est tiède.",
            "narrateur|Une vache passe sur le pré, sans crier.",
        )
    return L(
        "narrateur|Victorino s'assoit, le sac ouvert par papa.",
        "enfant-m|J'écoutais tes mains.",
        "papa|Moi aussi, j'ouvrais avec toi.",
        "maman|Tu as demandé, il a ouvert.",
        "narrateur|La tablette a rendu vos pas.",
        coda,
        "narrateur|Victorino touche la pomme, du bout des doigts.",
        "enfant-m|Elle est à nous, maman.",
        "narrateur|Le lac reste collé à la vitre, tout bleu.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le quai sent le fer tiède, déjà.",
        "narrateur|Un pigeon picore près du banc.",
        "narrateur|L'horloge jaune avance, tout lent.",
        "narrateur|Le wagon fait une ombre longue.",
        "papa|Tu entends le sifflet, Victorino ?",
        "enfant-m|Oui, papa, il est tout près.",
        "narrateur|Maman pose le sac bleu sur le banc.",
        "maman|Le ticket est là, tu le vois ?",
        "enfant-m|Il est tout rouge, papa.",
        "narrateur|En ce moment, Victorino touche le ticket rouge.",
        "enfant-m|Je le garde jusqu'au lac.",
        "papa|On prépare les affaires, alors ?",
        "maman|Le ticket, le sac, et la pomme.",
        "papa|Merci, tu le tiens tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près du banc.",
        "narrateur|Le ticket, le sac, et la pomme.",
        "maman|Tu prends quoi d'abord, Victorino ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le ticket rouge", "le sac bleu", "la pomme")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        if t1 == 1:
            s[f"{p}_Q0001"] = L(
                "narrateur|Victorino a mis le ticket rouge.",
                "maman|Il est où, maintenant ?",
            )
        elif t1 == 2:
            s[f"{p}_Q0001"] = L(
                "narrateur|Victorino a passé le sac bleu.",
                "maman|Il est où, maintenant ?",
            )
        else:
            s[f"{p}_Q0001"] = L(
                "narrateur|Victorino a pris la pomme.",
                "maman|Elle est où, maintenant ?",
            )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("l'allée", "la fenêtre", "la tablette")
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
        "Victorino veut garder son ticket rouge jusqu'au lac. "
        "T1 = ticket rouge / sac bleu / pomme (les trois montent). "
        "T2 = allée (talons, glisse) / fenêtre (pré, trampoline) / tablette (secousse, bord). "
        "T3 = neuf résolutions (petits pas, roues, papa tient ; "
        "arbres, tunnel, maman tient ; "
        "pomme, tablette calme, papa ouvre). "
        "L'élan de Victorino se vit, sans slogan. Fin : le lac est collé à la vitre.",
        "N2 ≤ 15. Héros Victorino, papa/maman, troupe D16, Sami hors troupe. "
        "Cuisine/jardin/chambre, cubes/livre/dînette, matin/sieste/soir jetés. "
        "Train (pas marché 019, marelle 023, papillon 029, carrousel 033, "
        "balle-portail 039, camp 047, citronnade 055). "
        "Titre slogan remplacé (objet + désir). Un merci de papa lié au geste "
        "(tenir le ticket). Pas de « bon travail ». Audio non cuit.",
    )


if __name__ == "__main__":
    main()
