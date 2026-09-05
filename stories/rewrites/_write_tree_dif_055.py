#!/usr/bin/env python3
"""TREE-DIF-055 — La citronnade de Sarah, dans le pichet (N1, DIF.ENE.001, cuisine)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-055"
N1 = 10
TITLE = "La citronnade de Sarah, dans le pichet"
FIL = (
    "Sarah veut un pichet de citronnade jaune, à boire près de la vitre. "
    "Elle prend d'abord le citron, le sucrier ou le pichet bleu ; les trois viennent. "
    "À la table le citron file, à l'évier le jus court, sur le tabouret ses pieds dansent. "
    "Elle joue avec l'élan, elle attend, elle demande. "
    "Le pichet se remplit. Ils goûtent. Ça pique, puis c'est doux."
)
CHARS = "Sarah, papa, maman"
SETTING = "la cuisine : table, évier, tabouret"


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
        "le jardin",
        "la chambre",
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
        "léa",
        "lea ",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "citronnade" not in blob:
        raise SystemExit(f"{SID}: citronnade absente")
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
        "lab": "le citron jaune",
        "cap": "Le citron jaune",
        "t1q": "dans les mains",
        "t1acc": "mains | les mains | dans les mains | ses mains",
        "t1retry": "Le citron est dans les mains.",
        "coda": "narrateur|Le citron jaune garde une peau froide, tout près.",
    },
    2: {
        "lab": "le sucrier blanc",
        "cap": "Le sucrier blanc",
        "t1q": "contre le ventre",
        "t1acc": "ventre | le ventre | contre le ventre | son ventre",
        "t1retry": "Le sucrier est contre le ventre.",
        "coda": "narrateur|Le sucrier blanc garde un grain, au fond.",
    },
    3: {
        "lab": "le pichet bleu",
        "cap": "Le pichet bleu",
        "t1q": "par le bord",
        "t1acc": "bord | le bord | par le bord | le pichet",
        "t1retry": "Le pichet est pris par le bord.",
        "coda": "narrateur|Le pichet bleu garde une goutte, tout au fond.",
    },
}

T3_LABS = {
    1: ("la balle jaune", "le grain", "maman tient"),
    2: ("les gouttes", "le filet", "papa presse"),
    3: ("les sauts", "le compte", "papa porte"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah prend d'abord le citron jaune.",
            "enfant-f|Il est froid, tout rond.",
            "maman|Garde-le dans les mains, tout droit.",
            "narrateur|La peau sent déjà le soleil.",
            "papa|Le sucrier aussi, près de toi.",
            "narrateur|Maman glisse le pichet, tout près.",
            "narrateur|Les trois affaires avancent avec elle.",
            "enfant-f|La citronnade va venir.",
            "narrateur|Ses pieds tapent déjà le carreau, trop vite.",
            "papa|Le citron d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah serre d'abord le sucrier blanc.",
            "enfant-f|Il gratte un peu, contre moi.",
            "papa|Tiens-le contre le ventre, tout chaud.",
            "narrateur|Un grain tombe, tout petit.",
            "maman|Le citron, ensuite, près de toi.",
            "narrateur|Elle glisse le pichet d'une main.",
            "narrateur|Les trois affaires avancent avec elle.",
            "enfant-f|Je veux le jus, tout jaune.",
            "narrateur|Un genou rebondit, puis l'autre.",
            "maman|Le sucrier d'abord, il est prêt.",
        )
    return L(
        "narrateur|Sarah prend d'abord le pichet bleu.",
        "enfant-f|Il est lourd, par le bord.",
        "maman|Garde-le là, tout droit.",
        "narrateur|L'eau chante un peu, déjà.",
        "papa|Le citron et le sucrier, avec toi.",
        "narrateur|Elle les pose près des carreaux.",
        "narrateur|Les trois affaires avancent avec elle.",
        "enfant-f|Le pichet veut son jaune.",
        "narrateur|Ses talons frappent le carreau, trop vite.",
        "papa|Le pichet d'abord, il est pris.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|Dans les mains.",
            "maman|Oui.",
            "narrateur|Le citron roule un peu, puis s'arrête.",
            "enfant-f|C'est mon soleil de cuisine.",
            "narrateur|Sarah le serre, le lâche, le reprend.",
            "narrateur|Un pied tape, puis l'autre, trop vite.",
            "maman|Tes pieds veulent déjà le jus.",
            "papa|On pose tout ici ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-f|Contre le ventre.",
            "papa|Oui.",
            "narrateur|Le couvercle du sucrier chatouille sa manche.",
            "enfant-f|C'est ma neige, pour le jus.",
            "narrateur|Sarah secoue, un nuage de grains.",
            "narrateur|Un grain blanc traîne encore par terre.",
            "maman|Ça sent déjà le sucré, tout près.",
            "papa|Tes mains, sur le sucrier ?",
            "enfant-f|Oui, papa.",
        )
    return L(
        "enfant-f|Par le bord.",
        "maman|Oui.",
        "narrateur|L'eau du pichet danse un peu.",
        "enfant-f|Ma citronnade habite dedans.",
        "narrateur|Sarah le penche, le redresse, trop vite.",
        "narrateur|Une goutte frappe le carreau, toute ronde.",
        "maman|La cuisine est prête, devant.",
        "papa|On y va, tous les trois ?",
        "enfant-f|Oui.",
    )


def t2_question(t1: int) -> list[str]:
    if t1 == 1:
        first = "narrateur|Sarah roule déjà le citron, trop vite."
    elif t1 == 2:
        first = "narrateur|Un grain de sucre saute encore."
    else:
        first = "narrateur|L'eau du pichet clapote, tout léger."
    return L(
        first,
        "narrateur|Sur la table, la toile cirée brille.",
        "narrateur|À l'évier, une goutte tombe, encore.",
        "narrateur|Près du bois, le tabouret attend.",
        "papa|On presse où, Sarah ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Sarah pose le citron sur la toile cirée.",
            2: "narrateur|Sarah pose le sucrier sur la toile cirée.",
            3: "narrateur|Sarah pose le pichet sur la toile cirée.",
        }[t1]
        mishap = {
            1: "narrateur|Le citron part, comme une petite balle.",
            2: "narrateur|Un grain de sucre saute, trop loin.",
            3: "narrateur|Le pichet penche, l'eau tremble.",
        }[t1]
        return L(
            lead,
            "narrateur|Ses talons tambourinent le carreau.",
            "enfant-f|La citronnade, c'est là, papa !",
            mishap,
            f"enfant-f|{o['cap']} part trop vite.",
            "maman|Tes pieds dansent, déjà.",
            "papa|La table n'a pas encore de jus.",
            "enfant-f|On presse comment, alors ?",
            "papa|Tu fais comment, avec nous ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Sarah porte le citron vers l'eau.",
            2: "narrateur|Sarah porte le sucrier vers l'eau.",
            3: "narrateur|Sarah porte le pichet vers l'eau.",
        }[t1]
        mishap = {
            1: "narrateur|Le citron glisse, trop mouillé, trop vite.",
            2: "narrateur|Le sucrier penche, un grain file.",
            3: "narrateur|Le pichet claque le rebord, trop fort.",
        }[t1]
        return L(
            lead,
            "enfant-f|Ici, le jus va tomber, maman.",
            "narrateur|Ses genoux font un petit trampoline.",
            mishap,
            "narrateur|Une goutte rebondit, puis s'en va.",
            "maman|Ton corps veut encore courir.",
            "papa|L'évier n'a pas encore de pichet.",
            "enfant-f|On peut jouer avec, quand même ?",
            "papa|Vous trouvez, tous les trois ?",
        )
    lead = {
        1: "narrateur|Sarah grimpe, le citron contre elle.",
        2: "narrateur|Sarah grimpe, le sucrier contre elle.",
        3: "narrateur|Sarah grimpe, le pichet contre elle.",
    }[t1]
    mishap = {
        1: "narrateur|Le citron saute d'un genou, trop haut.",
        2: "narrateur|Le sucrier vacille, un grain s'envole.",
        3: "narrateur|Le pichet penche, l'eau fait une vague.",
    }[t1]
    return L(
        lead,
        "enfant-f|Ici, je suis grande, papa.",
        "narrateur|Le bois du tabouret rend chaque pas.",
        mishap,
        f"narrateur|{o['cap']} n'est plus à sa place.",
        "maman|Tes genoux font trop de vagues.",
        "papa|Le tabouret n'a pas encore de table.",
        "enfant-f|On verse comment, alors ?",
        "papa|Vous trouvez, tous les trois ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le jaune veut encore courir.",
            "papa|La balle, le grain, ou maman ?",
        )
    if t2 == 2:
        return L(
            "narrateur|L'eau file encore un peu.",
            "maman|Les gouttes, le filet, ou papa ?",
        )
    return L(
        "narrateur|Le bois tremble encore un peu.",
        "papa|Les sauts, le compte, ou je porte ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Sarah roule le citron, un, deux, trois.",
            2: "narrateur|Sarah roule, le sucrier devient une colline.",
            3: "narrateur|Sarah roule, le pichet devient un lac.",
        }[t1]
        return L(
            "enfant-f|On joue à la balle jaune.",
            "papa|Toi tu roules, moi je rattrape.",
            hold,
            "narrateur|Le jaune va, revient, sent plus fort.",
            "narrateur|Sarah roule encore, puis s'arrête.",
            "enfant-f|La balle est fatiguée.",
            "maman|On peut presser, maintenant.",
            "papa|Vous avez joué, puis posé.",
            "narrateur|La toile redevient une table, tout douce.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le citron repose, enfin sage.",
            2: "narrateur|Le sucrier repose, un grain arrêté.",
            3: "narrateur|Le pichet repose, l'eau calme.",
        }[t1]
        return L(
            "enfant-f|On attend le grain.",
            "narrateur|Sarah pose les genoux au carreau.",
            wait,
            "narrateur|Un grain glisse, puis plus.",
            "enfant-f|Il ne bouge plus ?",
            "maman|La toile est calme, oui.",
            "papa|Tes pieds se sont assis, eux aussi.",
            "narrateur|Sarah presse, tout droit, tout petit.",
            "enfant-f|La citronnade peut venir.",
        )
    if t2 == 1 and t3 == 3:
        hand = {
            1: "narrateur|Maman tient le citron, Sarah verse.",
            2: "narrateur|Maman tient le sucrier, Sarah verse.",
            3: "narrateur|Maman tient le pichet, Sarah verse.",
        }[t1]
        return L(
            "enfant-f|Maman, tu tiens, s'il te plaît ?",
            "maman|Je tiens, tu verses le sucre.",
            hand,
            "narrateur|Sarah verse un grain, puis un autre.",
            "narrateur|Le jaune reste sage, dans sa main.",
            "enfant-f|Toi tu tiens, moi je verse.",
            "papa|Vous avez demandé, et ça tient.",
            "maman|Ma main fait le bol, ici.",
            "narrateur|La table garde un grain, tout mince.",
        )
    if t2 == 2 and t3 == 1:
        pair = {
            1: "narrateur|Sarah presse, papa compte les gouttes.",
            2: "narrateur|Sarah penche le sucrier, papa compte.",
            3: "narrateur|Sarah penche le pichet, papa compte.",
        }[t1]
        return L(
            "enfant-f|On fait des gouttes.",
            "papa|Toi tu presses, moi je compte.",
            pair,
            "narrateur|Des perles tombent, une après l'autre.",
            "enfant-f|La dernière est au bout.",
            "maman|Vous avez joué, puis posé le fruit.",
            "papa|L'évier est devenu un ruisseau.",
            f"narrateur|{o['cap']} a trouvé son coin.",
            "enfant-f|Le jus est là, tout bas.",
        )
    if t2 == 2 and t3 == 2:
        line = {
            1: "narrateur|Sarah tient le citron, le filet attend.",
            2: "narrateur|Sarah tient le sucrier, le filet attend.",
            3: "narrateur|Sarah tient le pichet, le filet attend.",
        }[t1]
        return L(
            "enfant-f|J'attends le filet.",
            "papa|Moi je l'ouvre, puis c'est toi.",
            line,
            "narrateur|L'eau avance, goutte après goutte.",
            "narrateur|Sarah souffle, les épaules baissent.",
            "papa|C'est à toi, Sarah.",
            "enfant-f|J'y glisse le citron.",
            "maman|Chacun son tour, sur l'évier.",
            "narrateur|Le filet se tait, enfin.",
        )
    if t2 == 2 and t3 == 3:
        open_ = {
            1: "narrateur|Papa presse le citron, tout doux.",
            2: "narrateur|Papa presse, près du sucrier.",
            3: "narrateur|Papa presse, au-dessus du pichet.",
        }[t1]
        return L(
            "enfant-f|Papa, tu presses le citron ?",
            "papa|Je le presse, tout doux.",
            open_,
            "narrateur|Sarah glisse un grain, les mains calmes.",
            "narrateur|L'autre main suit, le pichet au calme.",
            "enfant-f|Toi tu presses, moi je verse.",
            "maman|Vous avez demandé, et ça marche.",
            "papa|Le jus tient tout seul, maintenant.",
            "narrateur|Un carré de carreau reste tiède, autour.",
        )
    if t2 == 3 and t3 == 1:
        train = {
            1: "narrateur|Le citron voyage d'un genou à l'autre.",
            2: "narrateur|Le sucrier voyage d'un genou à l'autre.",
            3: "narrateur|Le pichet voyage d'un genou à l'autre.",
        }[t1]
        return L(
            "enfant-f|On fait des sauts.",
            "papa|Tu rebondis, puis tu verses.",
            train,
            "narrateur|Le bois penche, puis se tient droit.",
            "enfant-f|Doucement, les sauts tiennent.",
            "maman|Vous avez joué, puis versé.",
            "papa|Le tabouret est une table, maintenant.",
            f"narrateur|{o['cap']} a trouvé son coin.",
            "enfant-f|La citronnade est là, tout haut.",
        )
    if t2 == 3 and t3 == 2:
        hush = {
            1: "narrateur|Le citron reste sage, au creux des mains.",
            2: "narrateur|Le sucrier reste sage, au creux des mains.",
            3: "narrateur|Le pichet reste sage, au creux des genoux.",
        }[t1]
        return L(
            "enfant-f|On attend le compte.",
            "papa|Un, deux, trois, tu verses.",
            "narrateur|Un saut, puis le bois reste calme.",
            hush,
            "narrateur|Le compte se tait, enfin.",
            "enfant-f|Maintenant !",
            "maman|Le tabouret a fini ses vagues.",
            "papa|Tes genoux se sont assis, eux aussi.",
            "narrateur|Un pli du torchon retombe, tout lent.",
        )
    tuck = {
        1: "narrateur|Papa porte le pichet, Sarah tient le citron.",
        2: "narrateur|Papa porte le pichet, près du sucrier.",
        3: "narrateur|Papa porte le pichet, tout droit.",
    }[t1]
    return L(
        "enfant-f|Papa, tu portes le pichet ?",
        "papa|Je le porte, tout chaud.",
        tuck,
        "narrateur|Sarah écoute les mains, plus que ses pieds.",
        "maman|Tu verses, et ça tient.",
        "enfant-f|Moi aussi, j'écoute.",
        "narrateur|Le tabouret devient une table, tout haut.",
        "papa|Vous avez demandé le bord.",
        "maman|Ses mains ont tenu le jaune.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Sarah boit près de la table, tout petit.",
            "enfant-f|La balle est devenue du jus.",
            "papa|Tu roulais, moi je rattrapais.",
            "maman|Le pichet a son jaune, maintenant.",
            "narrateur|La toile cirée garde un grain sucré.",
            coda,
            "narrateur|Un grain sucré dort sur la toile.",
            "enfant-f|Encore une gorgée, papa.",
            "narrateur|La vitre tient encore le soleil.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sarah boit, la toile tout calme.",
            "enfant-f|J'ai attendu le grain, d'abord.",
            "papa|Puis le citron est resté droit.",
            "maman|Tes pieds se sont assis, eux aussi.",
            "narrateur|Le sucre ne danse plus.",
            coda,
            "narrateur|Une poussière reste coincée, tout près.",
            "enfant-f|C'est sucré, tout au fond.",
            "narrateur|La vitre brille un peu, puis se tait.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Sarah boit, la main de maman tout près.",
            "enfant-f|Tu tenais le fruit.",
            "papa|Vous avez demandé, et ça tenait.",
            "maman|Ma main a fait le bol.",
            "narrateur|La cuisine rend le silence, tout doux.",
            f"narrateur|{o['cap']} pose un grain de lumière.",
            "narrateur|Sarah touche la toile, du bout.",
            "enfant-f|Il est à nous.",
            "narrateur|Un rai de soleil barre encore la toile.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Sarah boit au bout des gouttes.",
            "enfant-f|Toi tu comptais, moi je pressais.",
            "papa|Tes gouttes ont fait le jus.",
            "maman|L'évier est devenu un ruisseau.",
            "narrateur|Le carreau redevient froid, et calme.",
            coda,
            "narrateur|Un peu d'eau sèche déjà.",
            "enfant-f|Les gouttes restent, maman.",
            "narrateur|Le robinet fait une ombre longue.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Sarah boit, le filet tout calme.",
            "papa|J'ai ouvert, puis c'était toi.",
            "enfant-f|J'ai attendu l'eau.",
            "maman|Chacun son tour, sur l'évier.",
            "narrateur|Le pichet bleu tient, enfin.",
            f"narrateur|{o['cap']} garde un grain de lumière.",
            "narrateur|Sarah souffle dessus, tout doux.",
            "enfant-f|Ça pique, puis c'est doux.",
            "narrateur|Un fil d'eau sèche contre le rebord.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sarah boit, le citron pressé par papa.",
            "enfant-f|Tu pressais, tout doux.",
            "papa|Le jus est tombé, juste assez.",
            "maman|L'entrée du pichet est à vous.",
            "narrateur|L'évier a rendu le calme.",
            coda,
            "narrateur|Un rond de chaleur reste sur le carreau.",
            "enfant-f|Regarde, papa, il brille.",
            "narrateur|Une odeur de citron reste, au frais.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Sarah boit, perchée sur le tabouret.",
            "enfant-f|Les sauts sont finis, papa.",
            "papa|Tu rebondissais, puis tu versais.",
            "maman|La table haute a son jus, ici.",
            "narrateur|Le bois est redevenu un siège.",
            coda,
            "narrateur|Une poussière tourne encore, puis tombe.",
            "enfant-f|Les sauts se taisent.",
            "narrateur|Dans la cuisine, le pichet tient.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Sarah boit, après le compte.",
            "enfant-f|On a attendu le bois.",
            "papa|Quand il s'est tu, tu as versé.",
            "maman|Le tabouret a fait une table.",
            "narrateur|Tes genoux se sont assis.",
            f"narrateur|{o['cap']} ne fait plus aucun bruit.",
            "narrateur|Sarah pose la paume sur le bois tiède.",
            "enfant-f|Il est tiède.",
            "narrateur|Une mouche passe sur la vitre, sans crier.",
        )
    return L(
        "narrateur|Sarah boit, le pichet porté par papa.",
        "enfant-f|J'écoutais tes mains.",
        "papa|Moi aussi, je portais avec toi.",
        "maman|Vous avez demandé le bord.",
        "narrateur|Le tabouret a rendu vos pas.",
        coda,
        "narrateur|Sarah touche le verre, du bout des doigts.",
        "enfant-f|Il est à nous, maman.",
        "narrateur|Le bleu garde une poussière, puis plus rien.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La casserole a laissé un nuage sur la vitre.",
        "narrateur|Les carreaux sont encore un peu froids.",
        "narrateur|Ça sent le toast d'avant, tout tiède.",
        "narrateur|Une goutte glisse, lente, sur le carreau.",
        "papa|Le citron est là, Sarah, tu le vois ?",
        "enfant-f|Il est tout jaune, papa.",
        "narrateur|Maman pose le pichet bleu près de l'eau.",
        "maman|On fait une citronnade, tu veux ?",
        "enfant-f|Oui, tout un pichet !",
        "narrateur|En ce moment, Sarah touche le citron.",
        "enfant-f|Je le roule, il est froid.",
        "papa|Merci, tu le tiens tout droit.",
        "maman|Le sucrier aussi, tout près.",
        "papa|On prépare, alors ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près de l'eau.",
        "narrateur|Le citron, le sucrier, et le pichet.",
        "maman|Tu prends quoi d'abord, Sarah ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le citron jaune", "le sucrier blanc", "le pichet bleu")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        if t1 == 1:
            s[f"{p}_Q0001"] = L(
                "narrateur|Sarah a pris le citron jaune.",
                "maman|Il est où, maintenant ?",
            )
        elif t1 == 2:
            s[f"{p}_Q0001"] = L(
                "narrateur|Sarah a serré le sucrier blanc.",
                "maman|Il est où, maintenant ?",
            )
        else:
            s[f"{p}_Q0001"] = L(
                "narrateur|Sarah a pris le pichet bleu.",
                "maman|Il est où, maintenant ?",
            )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la table", "l'évier", "le tabouret")
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
        "Sarah veut un pichet de citronnade jaune, à boire près de la vitre. "
        "T1 = citron jaune / sucrier blanc / pichet bleu (les trois viennent). "
        "T2 = table (citron-balle, grains) / évier (gouttes, filet) / tabouret (sauts, compte). "
        "T3 = neuf résolutions (balle jaune, grain, maman tient ; "
        "gouttes, filet, papa presse ; "
        "sauts, compte, papa porte). "
        "L'élan de Sarah se vit, sans slogan. Fin : ils goûtent, ça pique puis c'est doux.",
        "N1 ≤ 10. Héroïne Sarah, papa/maman, troupe D16, Léa hors troupe. "
        "Cuisine/jardin/chambre, cubes/livre/dînette, matin/sieste/soir jetés. "
        "Cuisine (pas marché, pas marelle, pas carrousel, pas papillon, pas portail, pas camp). "
        "Titre slogan remplacé (objet + désir). Un merci de papa lié au geste "
        "(tenir le citron). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
