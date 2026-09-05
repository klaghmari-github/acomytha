#!/usr/bin/env python3
"""TREE-DIF-026 — Le théâtre de draps de Mila (N3, DIF.COR.003)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-026"
N3 = 16
TITLE = "Le théâtre de draps de Mila"
FIL = (
    "Mila veut un vrai spectacle de marionnette avant la soupe. "
    "Nino arrive, lunettes encore floues du bain, cheveux mouillés, "
    "pull trop long. Ils emportent le drap à carreaux, les pinces "
    "et la marionnette rouge. Au salon la buée cache la scène, "
    "au couloir les pinces touchent les cheveux, dans la chambre "
    "les manches avalent le héros. Ils jouent ensemble. Le drap "
    "retombe sur le coffre."
)


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
    out["characters"] = "Mila, Nino, papa, maman"
    out["setting"] = "maison : salon, couloir, chambre, avant la soupe"
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
        "pas rire",
        "zoé",
        "zoe",
        "sami",
        "léa",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "escargot",
        "tarte",
        "aniss",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
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
        "lab": "le drap à carreaux",
        "cap": "Le drap à carreaux",
        "t1q": "dans le panier",
        "t1line": "Le drap à carreaux est dans le panier.",
        "t1acc": "panier | le panier | dans le panier | au panier",
        "t1retry": "Le drap est dans le panier.",
        "coda": "narrateur|Le drap à carreaux retombe sur le coffre.",
    },
    2: {
        "lab": "les pinces",
        "cap": "Les pinces",
        "t1q": "dans la poche",
        "t1line": "Les pinces sont dans la poche.",
        "t1acc": "poche | la poche | dans la poche | sa poche",
        "t1retry": "Les pinces sont dans la poche.",
        "coda": "narrateur|Les pinces rentrent dans la poche.",
    },
    3: {
        "lab": "la marionnette rouge",
        "cap": "La marionnette rouge",
        "t1q": "au poignet",
        "t1line": "La marionnette rouge est au poignet.",
        "t1acc": "poignet | au poignet | le poignet | son poignet",
        "t1retry": "La marionnette est au poignet.",
        "coda": "narrateur|La marionnette rouge veille au bord du lit.",
    },
}

T3_LABS = {
    1: ("le torchon de maman", "les mains de Nino", "la fenêtre ouverte"),
    2: ("la pince plus haut", "la serviette", "tenir le drap"),
    3: ("les manches retroussées", "Mila tient la marionnette", "l'élastique de maman"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila prend d'abord le drap à carreaux.",
            "enfant-f|Il sent encore le soleil de la fenêtre.",
            "maman|Glisse-le dans le panier, tout plié.",
            "narrateur|Le tissu fait un petit froissement.",
            "papa|Les pinces, ensuite, dans ta poche.",
            "narrateur|Maman noue la marionnette rouge au poignet.",
            "narrateur|Tout le théâtre se met en route.",
            "enfant-f|Nino, tu portes le panier ?",
            "copain|Je le tiens, même un peu flou.",
            "papa|Le drap d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila prend d'abord les pinces, toutes froides.",
            "enfant-f|Elles cliquettent dans ma paume.",
            "papa|Range-les dans ta poche, tout doux.",
            "narrateur|Le métal fait un petit toc contre le tissu.",
            "maman|Le drap, ensuite, dans le panier.",
            "narrateur|Elle glisse la marionnette rouge au poignet.",
            "narrateur|Ils avancent, les affaires avec eux.",
            "enfant-f|Nino, tu accroches le bord ?",
            "copain|J'essaie, mes lunettes glissent un peu.",
            "maman|Les pinces d'abord, elles sont prêtes.",
        )
    return L(
        "narrateur|Mila enfile d'abord la marionnette rouge.",
        "enfant-f|Elle marche déjà sur ma main.",
        "maman|Garde-la au poignet, comme un secret.",
        "narrateur|La laine rouge chatouille la peau.",
        "papa|Le drap et les pinces, avec vous.",
        "narrateur|Il les pose près du panier.",
        "narrateur|Le spectacle quitte le coffre, enfin.",
        "enfant-f|Nino, elle te salue !",
        "copain|Bonjour, petite laine.",
        "papa|La marionnette d'abord, elle est prête.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le panier porte le drap, tout contre le bois.",
            "copain|Je vois des carreaux, un peu flous.",
            "enfant-f|C'est pour notre scène.",
            "narrateur|Les lunettes de Nino gardent un rond de buée.",
            "maman|Le salon vous attend, plus loin.",
            "papa|On avance avec le panier ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La poche porte les pinces, tout contre le tissu.",
            "copain|Ça cliquette quand je marche.",
            "enfant-f|Ne les perds pas.",
            "narrateur|Une goutte tombe d'une mèche de Nino.",
            "papa|Ça sent encore le savon du bain.",
            "maman|Vos mains, au-dessus de la poche ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|Le poignet porte la marionnette, toute légère.",
        "copain|Elle a un œil brodé, tout petit.",
        "enfant-f|Tu le verras mieux, tout à l'heure.",
        "narrateur|Le pull de Nino cache encore ses poignets.",
        "maman|La chambre est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le radiateur du salon fait un air tout chaud.",
        "narrateur|Dans le couloir, les crochets attendent, tout hauts.",
        "narrateur|Le lit de la chambre ressemble déjà à une scène.",
        "papa|Vous jouez où, pour le spectacle ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Mila déplie le drap entre les deux chaises.",
            2: "narrateur|Mila attache le drap, pince après pince.",
            3: "narrateur|La marionnette grimpe le dossier d'une chaise.",
        }[t1]
        mishap = {
            1: "narrateur|Le drap retombe, Nino n'a pas vu le bord.",
            2: "narrateur|Une pince tombe : Nino visait à côté.",
            3: "narrateur|La marionnette salue, Nino la cherche trop bas.",
        }[t1]
        return L(
            lead,
            "narrateur|Le radiateur souffle un air tiède, tout proche.",
            "copain|Je vois un nuage sur mes lunettes !",
            "narrateur|Un rond de buée cache la scène.",
            mishap,
            f"enfant-f|{o['cap']} attend encore, tout prêt.",
            "maman|La chaleur a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, lui un peu flou.",
            "copain|On joue comment, alors ?",
            "papa|La scène est floue, vous faites quoi ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Mila jette le drap vers le crochet du manteau.",
            2: "narrateur|Mila tend une pince vers le crochet haut.",
            3: "narrateur|La marionnette tire le drap, vers le crochet.",
        }[t1]
        mishap = {
            1: "narrateur|Le drap glisse, accroché à une mèche mouillée.",
            2: "narrateur|La pince pince un cheveu, pas le tissu.",
            3: "narrateur|La laine rouge s'emmêle à une mèche encore humide.",
        }[t1]
        return L(
            lead,
            "enfant-f|Ici, le couloir fait un rideau, Nino.",
            "copain|Mes cheveux sont encore lourds du bain.",
            mishap,
            "narrateur|Une goutte tombe sur le carrelage, toc.",
            "maman|Ils sèchent, tout doux, ce n'est rien.",
            "papa|Toi tes cheveux tiennent, les siens gouttent.",
            "enfant-f|On peut jouer avec lui ?",
            "papa|Le rideau accroche, vous faites quoi ?",
        )
    lead = {
        1: "narrateur|Mila tend le drap au pied du lit.",
        2: "narrateur|Mila attache le drap au bois du lit.",
        3: "narrateur|La marionnette se cache sous l'oreiller.",
    }[t1]
    mishap = {
        1: "narrateur|Une manche trop longue emporte un coin du drap.",
        2: "narrateur|Une manche trop longue balaie les pinces.",
        3: "narrateur|Une manche trop longue avale la marionnette.",
    }[t1]
    return L(
        lead,
        "enfant-f|Le lit est notre château, Nino.",
        "copain|Mon pull me suit jusqu'aux genoux !",
        mishap,
        f"narrateur|{o['cap']} disparaît un instant, sous le tissu.",
        "maman|Le pull est un peu grand, c'est tout.",
        "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
        "copain|On joue comment, alors ?",
        "papa|Le pull et le roi, vous faites comment ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La buée reste sur les verres, tout douce.",
            "papa|Le torchon, les mains, ou la fenêtre ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Une mèche mouillée tient encore le drap.",
            "maman|La pince plus haut, la serviette, ou tenir ?",
        )
    return L(
        "narrateur|Les manches cachent encore le petit héros.",
        "papa|Manches, marionnette, ou l'élastique de maman ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wipe = {
            1: "narrateur|Nino essuie, puis reprend le bord du drap.",
            2: "narrateur|Nino essuie, puis reprend une pince.",
            3: "narrateur|Nino essuie, puis salue la marionnette.",
        }[t1]
        return L(
            "enfant-f|Maman, le torchon, s'il te plaît.",
            "maman|Tiens, tout doux, sur les verres.",
            "narrateur|Nino frotte un rond, puis un autre.",
            wipe,
            "copain|Je vois la scène !",
            "enfant-f|L'œil brodé est à toi, maintenant.",
            "narrateur|Les lunettes rendent le rouge tout net.",
            "papa|Vous jouez, chacun avec ce qu'il a.",
            "maman|Le torchon a rendu la scène.",
        )
    if t2 == 1 and t3 == 2:
        touch = {
            1: "narrateur|Nino palpe le drap, Mila parle.",
            2: "narrateur|Nino palpe les pinces, Mila parle.",
            3: "narrateur|Nino palpe la laine rouge, Mila parle.",
        }[t1]
        return L(
            "enfant-f|Tu joues avec tes mains, Nino.",
            "copain|Je touche, toi tu racontes.",
            touch,
            "narrateur|Sous le drap, deux silhouettes avancent.",
            "enfant-f|Le roi est à gauche, tout chaud.",
            "copain|Je le tiens !",
            f"narrateur|{o['cap']} guide encore le geste.",
            "papa|Les mains ont vu à la place des verres.",
            "maman|Le salon vous a gardés.",
        )
    if t2 == 1 and t3 == 3:
        air = {
            1: "narrateur|Le drap claque un peu, puis s'apaise.",
            2: "narrateur|Les pinces tintent, puis le métal se tait.",
            3: "narrateur|La marionnette se penche vers l'air frais.",
        }[t1]
        return L(
            "enfant-f|On ouvre un peu, papa ?",
            "papa|Un doigt de fenêtre, pas plus.",
            "narrateur|L'air froid chasse la buée, tout lent.",
            air,
            "copain|Ça redevient clair !",
            "enfant-f|Le spectacle peut commencer.",
            "narrateur|Nino ajuste ses lunettes, tout net.",
            "maman|La chaleur est partie, le jeu reste.",
            "papa|Vous avez attendu le verre clair.",
        )
    if t2 == 2 and t3 == 1:
        high = {
            1: "narrateur|Mila attache le drap plus haut, hors des mèches.",
            2: "narrateur|Mila pose la pince plus haut, hors des mèches.",
            3: "narrateur|La marionnette pousse le drap plus haut.",
        }[t1]
        return L(
            "enfant-f|On met la pince plus haut.",
            "copain|Mes cheveux restent en bas, alors.",
            high,
            "narrateur|Le rideau tient au crochet, tout droit.",
            "narrateur|Les mèches de Nino pendent, libres.",
            "enfant-f|Tu peux bouger, maintenant.",
            "copain|Le drap ne m'attrape plus.",
            "papa|Chacun a sa hauteur, sur le crochet.",
            "maman|Les cheveux ont eu leur place.",
        )
    if t2 == 2 and t3 == 2:
        dry = {
            1: "narrateur|Le drap attend, le temps d'un frottement.",
            2: "narrateur|Les pinces attendent, le temps d'un frottement.",
            3: "narrateur|La marionnette attend, le temps d'un frottement.",
        }[t1]
        return L(
            "enfant-f|La serviette, maman ?",
            "maman|Frotte, tout doux, pas trop fort.",
            "narrateur|Nino essuie une mèche, puis une autre.",
            dry,
            "copain|Elles sont plus légères !",
            "enfant-f|On accroche, maintenant.",
            "narrateur|Le drap monte, sans emporter de cheveu.",
            "papa|Vous avez laissé l'eau s'en aller.",
            "maman|Le couloir sent encore le savon.",
        )
    if t2 == 2 and t3 == 3:
        hold = {
            1: "narrateur|Nino tient le drap à deux mains, sans pince.",
            2: "narrateur|Nino tient le bord, Mila garde les pinces.",
            3: "narrateur|Nino tient le drap, la marionnette salue.",
        }[t1]
        return L(
            "enfant-f|Tu tiens le drap, moi j'attache à côté.",
            "copain|Mes mains font le crochet, alors.",
            hold,
            "narrateur|Le rideau s'ouvre quand Nino recule.",
            "narrateur|Il se ferme quand il avance.",
            "enfant-f|C'est toi le rideau vivant !",
            "copain|Et toi le spectacle.",
            "papa|Vous jouez avec ce que vous avez.",
            "maman|Les cheveux n'ont plus besoin d'être pris.",
        )
    if t2 == 3 and t3 == 1:
        roll = {
            1: "narrateur|Les manches remontent, le drap redevient libre.",
            2: "narrateur|Les manches remontent, les pinces redeviennent visibles.",
            3: "narrateur|Les manches remontent, la marionnette reparaît.",
        }[t1]
        return L(
            "enfant-f|On retrousse, Nino.",
            "copain|Jusqu'au coude, comme papa.",
            "narrateur|Deux rouleaux de laine tiennent, un peu épais.",
            roll,
            "enfant-f|Je te vois les mains, maintenant.",
            "copain|Le héros n'est plus dans le pull.",
            f"narrateur|{o['cap']} reprend sa place, au milieu.",
            "papa|Les manches ont laissé le jeu passer.",
            "maman|Le pull reste, plus court aux poignets.",
        )
    if t2 == 3 and t3 == 2:
        split = {
            1: "narrateur|Mila garde la marionnette, Nino lève le drap.",
            2: "narrateur|Mila attache, Nino lève le drap comme un rideau.",
            3: "narrateur|Mila parle avec la laine, Nino lève le drap.",
        }[t1]
        return L(
            "enfant-f|Moi je tiens la marionnette.",
            "copain|Moi je fais le rideau, avec le drap.",
            split,
            "narrateur|Les manches trop longues bougent le tissu, seulement.",
            "narrateur|La petite laine reste hors du pull.",
            "copain|Le château s'ouvre !",
            "enfant-f|Le roi sort, tout rouge.",
            "papa|Chacun a pris sa part, à sa taille.",
            "maman|Le lit a tenu le théâtre.",
        )
    bind = {
        1: "narrateur|L'élastique tient une manche, le drap l'autre bord.",
        2: "narrateur|L'élastique tient une manche, les pinces le drap.",
        3: "narrateur|L'élastique tient une manche, la marionnette salue.",
    }[t1]
    return L(
        "enfant-f|Maman, ton élastique, s'il te plaît.",
        "maman|Un pour chaque manche, tout doux.",
        "narrateur|Nino tend les poignets, maman noue.",
        bind,
        "copain|Mes mains sont nues, maintenant.",
        "enfant-f|Le héros peut marcher.",
        "narrateur|Le rouge avance sur la couette.",
        "papa|Vous avez demandé, et ça tient.",
        "maman|Mes élastiques ont gardé le pull.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Le salon sent encore le torchon tiède.",
            "copain|J'ai vu l'œil brodé, tout net.",
            "enfant-f|Tes lunettes ont trouvé le roi.",
            "papa|Vous avez joué, chacun avec sa vue.",
            "maman|La soupe appelle, tout doux.",
            coda,
            "narrateur|Un carreau de drap garde un rond de buée.",
            "enfant-f|On rentre, Nino.",
            "narrateur|Les chaises se font encore face, au calme.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous le drap, l'air est encore un peu chaud.",
            "enfant-f|Tu as touché, moi j'ai raconté.",
            "copain|Mes mains ont vu le roi.",
            "papa|Les verres flous n'ont pas arrêté le jeu.",
            "maman|Le radiateur se tait, enfin.",
            coda,
            "narrateur|Une ombre de marionnette reste au mur.",
            "enfant-f|À demain, la scène.",
            "narrateur|Le bois des chaises redevient froid.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Un filet d'air froid reste dans le salon.",
            "copain|La buée est partie, tout seule.",
            "enfant-f|On a attendu le verre clair.",
            "maman|La fenêtre a rendu la scène.",
            "papa|Vous avez laissé le temps aux lunettes.",
            f"narrateur|{o['cap']} pose une ombre nette, au sol.",
            "narrateur|Mila souffle sur l'œil brodé, tout léger.",
            "copain|Il brille encore.",
            "narrateur|Le radiateur reprend, plus loin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Le crochet du couloir garde encore le drap.",
            "enfant-f|La pince était trop bas, d'abord.",
            "copain|Mes cheveux sont restés libres.",
            "papa|Chacun a eu sa hauteur, sur le bois.",
            "maman|Le carrelage sèche déjà.",
            coda,
            "narrateur|Une mèche sèche contre le col, tout calme.",
            "enfant-f|On rentre, le rideau reste.",
            "narrateur|Le manteau du crochet reprend sa place.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La serviette sent encore le savon du bain.",
            "copain|Tu as frotté, tout doux.",
            "enfant-f|Puis on a accroché, sans emporter de cheveu.",
            "maman|L'eau s'en est allée, le jeu est resté.",
            "papa|Le couloir vous rend le silence.",
            f"narrateur|{o['cap']} garde une goutte, déjà tiède.",
            "narrateur|Mila souffle dessus, tout léger.",
            "copain|Elle part.",
            "narrateur|Le savon s'efface déjà du bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Les mains de Nino gardent encore le pli du drap.",
            "enfant-f|Tu étais le rideau vivant.",
            "copain|Toi le spectacle, moi l'ouverture.",
            "papa|Vous avez joué avec ce que vous aviez.",
            "maman|Les cheveux n'avaient plus besoin d'être pris.",
            coda,
            "narrateur|Un crochet vide attend, tout haut.",
            "enfant-f|On se dit au revoir, couloir.",
            "narrateur|Les chaussons glissent vers la soupe.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Deux rouleaux de manches tiennent encore.",
            "enfant-f|Tes mains sont sorties du pull.",
            "copain|Le héros n'était plus avalé.",
            "papa|Les manches ont laissé le jeu passer.",
            "maman|Le lit redevient un lit, tout simple.",
            coda,
            "narrateur|Un fil de laine rouge reste sur la couette.",
            "enfant-f|On rentre, Nino.",
            "narrateur|L'oreiller reprend sa forme, tout lent.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le drap-rideau retombe au pied du lit.",
            "copain|Tu tenais le roi, moi le château.",
            "enfant-f|Tes manches bougeaient seulement le tissu.",
            "maman|Chacun a pris sa part, à sa taille.",
            "papa|Le théâtre a tenu jusqu'à la soupe.",
            f"narrateur|{o['cap']} garde un pli de couette.",
            "narrateur|Mila lisse le rouge, tout doux.",
            "copain|Il a bien joué.",
            "narrateur|La chambre reprend son calme, déjà.",
        )
    return L(
        "narrateur|Deux élastiques veillent encore aux poignets.",
        "enfant-f|On a demandé, et ça tenait.",
        "copain|Mes mains étaient nues, pour le roi.",
        "papa|Vous avez demandé, rien de plus.",
        "maman|Mes élastiques rentrent dans le tiroir.",
        coda,
        "narrateur|Un peu de laine rouge reste au bois du lit.",
        "enfant-f|Le spectacle est à nous.",
        "narrateur|La soupe sent déjà, tout au bout du couloir.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le coffre de l'entrée sent la lavande.",
        "narrateur|Deux chaises se font face, dans le salon.",
        "narrateur|Un drap à carreaux dort sur le bois.",
        "narrateur|Une oreille rouge dépasse du panier.",
        "papa|Tu as vu le théâtre, Mila ?",
        "enfant-f|Il attend encore.",
        "maman|La soupe n'est pas prête.",
        "narrateur|En ce moment, Mila glisse sa main dans la marionnette.",
        "enfant-f|Je veux un vrai spectacle, avant de manger.",
        "narrateur|Des chaussons glissent dans le couloir.",
        "copain|Je viens jouer, Mila !",
        "narrateur|Les lunettes de Nino sont encore un peu floues.",
        "narrateur|Ses cheveux gouttent sur le pull trop long.",
        "papa|Merci, tu tiens déjà la marionnette.",
        "maman|On prépare le théâtre, alors ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Près du coffre, le drap sent encore le soleil.",
        "narrateur|Les pinces cliquettent, la marionnette attend.",
        "maman|Tu prends quoi d'abord, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le drap à carreaux", "les pinces", "la marionnette rouge")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        t1_ask = {
            1: "maman|Le drap est où ?",
            2: "maman|Les pinces sont où ?",
            3: "maman|La marionnette est où ?",
        }[t1]
        s[f"{p}_Q0001"] = L(
            f"narrateur|{o['t1line']}",
            t1_ask,
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("le salon", "le couloir", "la chambre")

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
        "Mila veut un vrai spectacle de marionnette avant la soupe. "
        "Nino arrive, lunettes encore floues du bain, cheveux mouillés, "
        "pull trop long. T1 = drap à carreaux / pinces / marionnette rouge "
        "(les trois partent). T2 = salon (buée sur les verres) / couloir "
        "(pinces et mèches) / chambre (manches trop longues). T3 = neuf "
        "résolutions (torchon, mains, fenêtre ; pince plus haut, serviette, "
        "tenir le drap ; manches, Mila tient, élastique). On joue ensemble, "
        "sans slogan. Fin : le drap retombe, la soupe appelle.",
        "N3 ≤ 16. Zoé / Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-003 "
        "(théâtre, pas l'escargot) et DIF-016 (pas la tarte). Un merci de "
        "papa lié au geste (tenir la marionnette). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
