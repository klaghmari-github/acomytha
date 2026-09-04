#!/usr/bin/env python3
"""F-NAR-008 — merged.json TREE-AUT-002 (manteau) et TREE-AUT-003 (cacao / vitre)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, relecture, words, write_story


def L(*rows: str) -> list[str]:
    return list(rows)


def pre(t1: int) -> str:
    return f"CHK_T0001_P000{t1}"


def vet(sid: str, scripts: dict) -> None:
    lim = 15
    joined_starts: list[str] = []
    for cid, lines in scripts.items():
        for raw in lines:
            role, phrase = raw.split("|", 1)
            n = words(phrase)
            if n > lim:
                raise SystemExit(f"{sid} {cid} {n}>15: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") != 1:
                raise SystemExit(f"{sid} {cid} ponctuation: {phrase}")
            if role == "narrateur":
                tok = phrase.strip().split()
                joined_starts.append(tok[0].lower() if tok else "")
            else:
                joined_starts.append("")
    run = 1
    for i in range(1, len(joined_starts)):
        if joined_starts[i] and joined_starts[i] == joined_starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"{sid}: puces « {joined_starts[i]} »")
        else:
            run = 1


def patch_t3_labels(sid: str, a: str, b: str, c: str) -> None:
    path = ROOT / sid / "merged.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for ch in data["chunks"]:
        if ch["kind"] == "transition_question" and "T0003_P0000" in ch["chunk_id"]:
            ch["option_1_label"] = a
            ch["option_2_label"] = b
            ch["option_3_label"] = c
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check(sid, data["age_band"], data["chunks"])


# ---------------------------------------------------------------------------
# TREE-AUT-002 — Sarah, jardin gris, manteau au crochet
# ---------------------------------------------------------------------------
COAT = {1: "rouge", 2: "bleu", 3: "vert"}
OBJ = {1: "le ballon rouge", 2: "le seau bleu", 3: "le doudou"}
ANI = {1: "le chat", 2: "le chien", 3: "la poule"}


def t1_002(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Sarah tire le manteau rouge du crochet.",
            "narrateur|Une manche est à l'envers, toute molle.",
            "enfant-f|Je n'ai pas le temps !",
            "narrateur|Elle pose le rouge sur la chaise.",
            "narrateur|Papa ouvre un peu la porte.",
            "narrateur|L'air entre, froid comme de l'eau.",
            "enfant-f|Aïe, mes bras !",
            "papa|Tu veux le rouge, Sarah ?",
            "enfant-f|Oui.",
            "enfant-f|Il est chaud.",
            "maman|Glisse un bras, puis l'autre.",
            "narrateur|Maman tourne la manche, tout doux.",
            "narrateur|Sarah enfile le rouge jusqu'en haut.",
            "enfant-f|Mes mains sont au chaud.",
            "papa|On va au banc gris ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah passe devant le manteau bleu.",
            "narrateur|Les boutons sont gros, ronds, un peu froids.",
            "enfant-f|Le banc m'attend !",
            "narrateur|Elle pousse la porte, sans le bleu.",
            "narrateur|L'air pique les joues, puis les mains.",
            "enfant-f|Il fait froid.",
            "maman|Tu reviens, ma puce ?",
            "narrateur|Sarah revient vers le crochet.",
            "narrateur|Elle prend le bleu, bouton après bouton.",
            "papa|Le troisième est un peu dur.",
            "enfant-f|Je l'ai.",
            "papa|Merci, Sarah.",
            "narrateur|Le bleu tient chaud, tout de suite.",
            "enfant-f|On va au jardin gris.",
        )
    return L(
        "narrateur|Sarah prend le manteau vert, trop long.",
        "narrateur|Une feuille sèche colle encore au tissu.",
        "enfant-f|J'enlève la feuille.",
        "narrateur|Elle pose le vert sur la marche.",
        "narrateur|Puis elle court vers le banc gris.",
        "narrateur|L'air froid lui serre les épaules.",
        "enfant-f|Mon dos a froid.",
        "papa|Le vert est resté sur la marche.",
        "narrateur|Sarah revient, puis glisse les manches.",
        "maman|Le capuchon, si tu veux.",
        "narrateur|Sarah met le capuchon, tout doux.",
        "enfant-f|Il sent la pluie, un peu.",
        "papa|On y va, au jardin ?",
        "enfant-f|Oui.",
        "enfant-f|Avec le vert.",
    )


def q_002(t1: int) -> list[str]:
    return L("narrateur|L'air était froid, Sarah est revenue chercher quoi ?")


def c_002(t1: int) -> list[str]:
    color = COAT[t1]
    if t1 == 1:
        return L(
            "narrateur|Le manteau rouge est fermé, bien chaud.",
            "narrateur|Sarah touche la poche, sèche et tiède.",
            "enfant-f|Je peux aller au banc, maintenant ?",
            "papa|Oui.",
            "papa|Tes bras sont au chaud ?",
            "enfant-f|Oui, papa.",
            "maman|Tu prends un jeu, pour le jardin ?",
            "enfant-f|Oui.",
        )
    if t1 == 2:
        return L(
            "narrateur|Les boutons du bleu tiennent, un par un.",
            "narrateur|Sarah souffle dans ses mains, dans les poches.",
            "enfant-f|Je n'ai plus froid.",
            "maman|Le jardin t'attend.",
            "papa|Tu emportes un jeu ?",
            "enfant-f|Oui.",
            "enfant-f|Pour le banc gris.",
        )
    return L(
        "narrateur|Le capuchon vert tient chaud aux oreilles.",
        "narrateur|Sarah frotte le tissu, sans la feuille.",
        "enfant-f|Je suis prête.",
        "papa|Tu prends quelque chose, pour jouer ?",
        "maman|Le banc est encore mouillé.",
        "enfant-f|J'emporte un jeu.",
    )
    # color used in speech above; keep name live in other branches
    _ = color


def t2q_002() -> list[str]:
    return L(
        "narrateur|Sarah choisit pour le jardin gris.",
        "narrateur|Le ballon rouge, le seau bleu, ou le doudou.",
    )


def t2_002(t1: int, t2: int) -> list[str]:
    color = COAT[t1]
    key = (t1, t2)
    table = {
        (1, 1): L(
            "narrateur|Sarah a le manteau rouge, bien fermé.",
            "narrateur|Le ballon rouge attend près du banc gris.",
            "enfant-f|Il glisse !",
            "papa|Regarde au sec, près du pied.",
            "narrateur|Sarah se baisse, et le rouge touche l'herbe.",
            "narrateur|Elle attrape le ballon, un peu froid.",
            "enfant-f|Je l'ai !",
            "maman|Tes mains rentrent dans les poches, après ?",
            "enfant-f|Oui.",
            "enfant-f|Elles sont chaudes.",
            "narrateur|Elle souffle, et le ballon part vers le banc.",
        ),
        (1, 2): L(
            "narrateur|Sarah porte le seau bleu, manteau rouge fermé.",
            "narrateur|Des feuilles mouillées collent au fond.",
            "enfant-f|Il est lourd.",
            "papa|On le pose près du banc, ensemble.",
            "narrateur|Ils posent le seau, l'anse encore froide.",
            "maman|Tu ramasses encore deux feuilles ?",
            "enfant-f|Oui.",
            "narrateur|Sarah glisse deux feuilles, tout doux.",
            "narrateur|Le seau sent la terre, comme le jardin.",
            "papa|Tes poignets restent dans les manches ?",
            "enfant-f|Oui, papa.",
        ),
        (1, 3): L(
            "narrateur|Sarah tient le doudou contre le manteau rouge.",
            "narrateur|Une goutte du banc mouille une oreille.",
            "enfant-f|Il est froid, là.",
            "maman|Glisse-le dans la poche, un moment.",
            "narrateur|Sarah pousse le doudou dans la poche chaude.",
            "narrateur|Le tissu rouge le recouvre, tout doux.",
            "enfant-f|Il redevient chaud.",
            "papa|Tu le sors sur le banc sec ?",
            "enfant-f|Oui.",
            "narrateur|Elle s'assoit, et le doudou reprend l'air.",
        ),
        (2, 1): L(
            "narrateur|Sarah court, le capuchon bleu saute un peu.",
            "narrateur|Le ballon rouge roule vers la flaque.",
            "enfant-f|J'y vais !",
            "papa|Le capuchon, d'abord.",
            "narrateur|Sarah recule le capuchon, et voit clair.",
            "narrateur|Elle rattrape le ballon avant l'eau.",
            "enfant-f|Il est sec.",
            "maman|Bravo, Sarah.",
            "maman|Tes boutons tiennent encore ?",
            "enfant-f|Oui, tous.",
            "narrateur|Elle tape le ballon contre le banc gris.",
        ),
        (2, 2): L(
            "narrateur|Sarah pose le seau bleu près des boutons.",
            "narrateur|Une feuille tombe dedans, toute plate.",
            "enfant-f|C'est un bateau.",
            "papa|Un bateau de feuille, dans le seau.",
            "narrateur|Sarah souffle, et la feuille avance un peu.",
            "maman|Le bleu te tient chaud, pendant le voyage ?",
            "enfant-f|Oui.",
            "enfant-f|Les boutons sont fermés.",
            "narrateur|Une autre feuille rejoint le bateau.",
            "papa|On reste près du banc, d'accord ?",
            "enfant-f|D'accord.",
        ),
        (2, 3): L(
            "narrateur|Le doudou voyage dans la manche du bleu.",
            "narrateur|Sarah arrive au banc, une oreille dépasse.",
            "enfant-f|Il veut voir le jardin.",
            "maman|Sors-le maintenant, il est chaud.",
            "narrateur|Sarah sort le doudou, qui sent le tissu.",
            "papa|Tu le poses sur le bois un peu sec ?",
            "enfant-f|Oui.",
            "narrateur|Le doudou s'assoit, et Sarah boutonne encore.",
            "narrateur|Le troisième bouton était un peu ouvert.",
            "enfant-f|Voilà, il tient.",
        ),
        (3, 1): L(
            "narrateur|Le manteau vert frotte les feuilles, trop long.",
            "narrateur|Le ballon rouge part trop loin, trop vite.",
            "enfant-f|J'arrive pas.",
            "papa|On relève un peu le bas, ensemble.",
            "narrateur|Papa plie le bas, et Sarah court mieux.",
            "narrateur|Elle rattrape le ballon près de l'herbe.",
            "maman|Le capuchon reste, s'il te tient chaud ?",
            "enfant-f|Il reste.",
            "enfant-f|J'ai le ballon.",
            "narrateur|Elle le serre, lisse et froid.",
        ),
        (3, 2): L(
            "narrateur|Sarah traîne le seau, et le vert touche la terre.",
            "narrateur|Des feuilles dépassent, comme un chapeau.",
            "enfant-f|On fait une montagne.",
            "maman|Une montagne de feuilles, dans le seau.",
            "narrateur|Sarah ajoute une feuille, puis une autre.",
            "papa|Le seau est plein, on le pose ?",
            "enfant-f|Près du banc.",
            "narrateur|Ils posent le seau sur l'herbe froide.",
            "narrateur|Sarah rentre les mains dans le vert.",
            "maman|Tu as les poignets au chaud ?",
            "enfant-f|Oui, maman.",
        ),
        (3, 3): L(
            "narrateur|Le doudou voyage sous le capuchon vert.",
            "narrateur|Sarah arrive au banc, une oreille sort.",
            "enfant-f|Il a vu le jardin gris.",
            "papa|Il était au chaud, lui.",
            "narrateur|Sarah s'assoit, le bas du vert dans l'herbe.",
            "maman|On le plie un peu, pour le bois sec.",
            "narrateur|Sarah plie le bas, puis pose le doudou.",
            "enfant-f|Il est bien, là.",
            "papa|Toi aussi, avec le capuchon ?",
            "enfant-f|Moi aussi.",
        ),
    }
    lines = table[key]
    _ = color
    return lines


def t3q_002() -> list[str]:
    return L(
        "narrateur|Qui vient près de Sarah ?",
        "narrateur|Le chat, le chien, ou la poule.",
    )


def t3_002(t1: int, t2: int, t3: int) -> list[str]:
    color = COAT[t1]
    obj = OBJ[t2]
    if t3 == 1:
        head = L(
            "narrateur|Un chat gris pose une patte sur le bois.",
            "narrateur|Ses yeux sont deux petites fentes.",
            "enfant-f|Il est là.",
            "maman|On reste tout doux.",
        )
        mid = {
            1: L(
                "narrateur|Le ballon s'arrête près de ses pattes.",
                "enfant-f|Il le sent, tout bas.",
                f"papa|Toi, tu as le manteau {color}.",
                "narrateur|Sarah reste près du chat, sans le toucher.",
            ),
            2: L(
                "narrateur|Le chat regarde le seau, puis se recule.",
                "enfant-f|Les feuilles bougent.",
                f"papa|Toi, tu as le manteau {color}.",
                "narrateur|Sarah laisse le seau, et le chat cligne.",
            ),
            3: L(
                "narrateur|Le chat s'assoit près du doudou, pas dessus.",
                "enfant-f|Il a choisi le coin sec.",
                f"maman|Toi, tu as le manteau {color}.",
                "narrateur|Sarah tient le doudou, et le chat ronronne.",
            ),
        }[t2]
    elif t3 == 2:
        head = L(
            "narrateur|Un chien brun arrive près de la flaque.",
            "narrateur|Sa queue tape l'air, tout content.",
            "enfant-f|Il secoue les oreilles !",
            "papa|On le regarde, il est gentil.",
        )
        mid = {
            1: L(
                "narrateur|Sarah tient le ballon contre elle.",
                "enfant-f|Je le garde.",
                f"maman|Le manteau {color} te tient chaud.",
                "narrateur|Le chien flaire l'herbe, puis s'assoit.",
            ),
            2: L(
                "narrateur|Une feuille s'échappe du seau.",
                "enfant-f|Il la suit du nez.",
                f"maman|Le manteau {color} te tient chaud.",
                "narrateur|Sarah rit, le seau reste près d'elle.",
            ),
            3: L(
                "narrateur|Sarah serre le doudou, tout contre.",
                "enfant-f|Il reste avec moi.",
                f"papa|Le manteau {color} te tient chaud.",
                "narrateur|Le chien pose le museau, puis recule.",
            ),
        }[t2]
    else:
        head = L(
            "narrateur|Une poule picore près des feuilles.",
            "narrateur|Son cou avance, tout précis.",
            "enfant-f|Elle cherche un grain.",
            "maman|On la laisse faire.",
        )
        mid = {
            1: L(
                "narrateur|Le ballon reste loin de son bec.",
                "enfant-f|Je le tiens.",
                f"papa|Le manteau {color} te tient chaud.",
                "narrateur|La poule trouve un grain, puis s'éloigne.",
            ),
            2: L(
                "narrateur|La poule picore près du seau, pas dedans.",
                "enfant-f|Mes feuilles sont à moi.",
                f"papa|Le manteau {color} te tient chaud.",
                "narrateur|Sarah recule le seau, la poule picore ailleurs.",
            ),
            3: L(
                "narrateur|Sarah pose le doudou sur ses genoux.",
                "enfant-f|Il regarde la poule.",
                f"maman|Le manteau {color} te tient chaud.",
                "narrateur|La poule picore, et un grain saute.",
            ),
        }[t2]
    _ = obj
    return head + mid


def fin_002(t1: int, t2: int, t3: int) -> list[str]:
    color = COAT[t1]
    obj_line = {
        1: "narrateur|Le ballon rouge attend près des chaussures.",
        2: "narrateur|Le seau bleu reste près du paillasson.",
        3: "narrateur|Le doudou rentre, encore un peu froid.",
    }[t2]
    hang = f"narrateur|Sarah raccroche le manteau {color} au crochet."
    animal_last = {
        1: "narrateur|Le chat cligne encore, sur le banc gris.",
        2: "narrateur|Le chien secoue une dernière feuille.",
        3: "narrateur|La poule picore loin, tout calme.",
    }[t3]
    garden = {
        (1, 1): "narrateur|Le bois mouillé brille, sans personne.",
        (1, 2): "narrateur|Une feuille reste collée au pied du banc.",
        (1, 3): "narrateur|Le capuchon n'est plus là, le banc oui.",
        (2, 1): "narrateur|La flaque tremble encore, toute ronde.",
        (2, 2): "narrateur|Le bateau de feuille s'est arrêté.",
        (2, 3): "narrateur|Le bois sec garde une petite chaleur.",
        (3, 1): "narrateur|L'herbe pliée se relève, tout doux.",
        (3, 2): "narrateur|La montagne de feuilles s'est calmée.",
        (3, 3): "narrateur|Le jardin gris reste là, tout calme.",
    }[(t2, t3)]
    ask = {
        1: "papa|Tes mains sont chaudes, maintenant ?",
        2: "maman|Tu n'as plus froid aux joues ?",
        3: "papa|Le capuchon t'a tenu chaud ?",
    }[t1]
    return L(
        obj_line,
        hang,
        ask,
        "enfant-f|Oui.",
        animal_last,
        garden,
    )


def build_002() -> dict:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = L(
        "narrateur|Le banc du jardin est gris, tout mouillé.",
        "narrateur|Des feuilles collent au bois, comme des timbres.",
        "narrateur|L'air sent la terre froide.",
        "narrateur|Dans l'entrée, un crochet bas attend.",
        "narrateur|Trois manteaux pendent, rouge, bleu, vert.",
        "narrateur|L'horloge de la cuisine fait tic tac.",
        "narrateur|Papa lace une chaussure, puis l'autre.",
        "papa|Les chaussures sont prêtes, Sarah.",
        "narrateur|Maman soulève un peu le store.",
        "maman|Tu as vu le banc, tout mouillé ?",
        "enfant-f|Oui, maman.",
        "enfant-f|Je veux y aller.",
        "enfant-f|Je veux le jardin gris.",
        "narrateur|En ce moment, Sarah court vers la porte.",
        "narrateur|Le crochet reste derrière elle, plein.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Quel manteau, Sarah ?",
        "narrateur|Le rouge, le bleu, ou le vert.",
    )
    for t1 in (1, 2, 3):
        p = pre(t1)
        s[p] = t1_002(t1)
        s[f"{p}_Q0001"] = q_002(t1)
        s[f"{p}_C0001"] = c_002(t1)
        s[f"{p}_T0002_P0000"] = t2q_002()
        for t2 in (1, 2, 3):
            s[f"{p}_T0002_P000{t2}"] = t2_002(t1, t2)
            s[f"{p}_T0002_P000{t2}_T0003_P0000"] = t3q_002()
            for t3 in (1, 2, 3):
                s[f"{p}_T0002_P000{t2}_T0003_P000{t3}"] = t3_002(t1, t2, t3)
                s[f"{p}_T0002_P000{t2}_T0003_P000{t3}_F0001"] = fin_002(t1, t2, t3)
    return s


def sons_002(scripts: dict) -> dict:
    out = {cid: "" for cid in scripts}
    out["CHK_T0000_P0000"] = "porte"
    for t1 in (1, 2, 3):
        out[pre(t1)] = "porte"
        for t2 in (1, 2, 3):
            cid = f"{pre(t1)}_T0002_P000{t2}_T0003_P0002"
            out[cid] = "chien_bonjour"
    return out


# ---------------------------------------------------------------------------
# TREE-AUT-003 — Mila, cacao, buée, goutte sur la vitre
# T1 cuisine / jardin / chambre
# T2 ballon / seau / doudou
# T3 crayon / tasse / écharpe (labels source Tom/Léa/Sami → objets vécus)
# ---------------------------------------------------------------------------
PLACE = {1: "la cuisine", 2: "le jardin", 3: "la chambre"}
THING = {1: "le ballon rouge", 2: "le seau bleu", 3: "le doudou"}
LEFT = {1: "le crayon", 2: "la tasse", 3: "l'écharpe"}
DRAW = {1: "un soleil", 2: "une maison", 3: "un bateau"}


def t1_003(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila pousse la porte de la cuisine.",
            "narrateur|Ça sent le cacao, plus fort, tout chaud.",
            "narrateur|La vitre au-dessus de l'évier est embuée.",
            "enfant-f|Je dessine un soleil.",
            "narrateur|Son doigt trace un rond dans la buée.",
            "narrateur|La tasse fume encore, trop près du bord.",
            "maman|Elle est encore trop chaude, Mila.",
            "enfant-f|Je reviens après.",
            "narrateur|Mila part vers le salon, les mains vides.",
            "papa|Ta tasse est restée.",
            "enfant-f|Je la reprends !",
            "narrateur|Elle revient, puis souffle sur le cacao.",
            "maman|Tu la poses près de toi, maintenant ?",
            "enfant-f|Oui.",
            "enfant-f|Près de la vitre.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila ouvre la porte du jardin.",
            "narrateur|La vitre de la porte est toute embuée.",
            "narrateur|Une goutte glisse, comme un crayon lent.",
            "enfant-f|Je dessine une maison.",
            "narrateur|Elle trace un toit, puis une fenêtre.",
            "narrateur|Le crayon reste sur le rebord mouillé.",
            "papa|Tu rentres, Mila ?",
            "enfant-f|Oui, le cacao m'attend.",
            "narrateur|Elle fait un pas, le crayon reste dehors.",
            "maman|Il est resté sur le rebord.",
            "enfant-f|Je le reprends !",
            "narrateur|Mila revient, le bois du rebord est froid.",
            "narrateur|Elle essuie le crayon sur sa manche.",
            "papa|Tu l'as ?",
            "enfant-f|Oui, papa.",
        )
    return L(
        "narrateur|Mila entre dans la chambre, tout doux.",
        "narrateur|Le rideau laisse un carré de buée.",
        "enfant-f|Je dessine un bateau.",
        "narrateur|Son doigt fait une voile, puis une coque.",
        "narrateur|L'écharpe est restée sur le lit, pliée.",
        "maman|Tu as les épaules nues, près de la vitre.",
        "enfant-f|J'ai chaud du cacao.",
        "narrateur|Elle part vers le salon, trop vite.",
        "papa|L'écharpe est sur le lit.",
        "enfant-f|Je la reprends !",
        "narrateur|Mila revient, puis met l'écharpe.",
        "narrateur|Le tissu est doux, un peu froid d'abord.",
        "maman|Ça va mieux ?",
        "enfant-f|Oui.",
        "enfant-f|Je peux dessiner.",
    )


def q_003(t1: int) -> list[str]:
    left = {1: "la tasse", 2: "le crayon", 3: "l'écharpe"}[t1]
    return L(f"narrateur|Mila est revenue chercher {left}, elle a fait quoi ?")


def c_003(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La tasse est près de la vitre, maintenant.",
            "narrateur|Le soleil de buée brille encore un peu.",
            "enfant-f|Je peux continuer ?",
            "maman|Oui.",
            "maman|Tu as repris la tasse.",
            "papa|Tu prends aussi un jeu ?",
            "enfant-f|Oui.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le crayon est sec, dans sa main.",
            "narrateur|La maison de buée attend sur la porte.",
            "enfant-f|Je peux finir le toit ?",
            "papa|Oui.",
            "papa|Tu as repris le crayon.",
            "maman|Tu prends aussi un jeu ?",
            "enfant-f|Oui.",
        )
    return L(
        "narrateur|L'écharpe tient chaud aux épaules.",
        "narrateur|Le bateau de buée attend sur la vitre.",
        "enfant-f|Je peux finir la voile ?",
        "maman|Oui.",
        "maman|Tu as repris l'écharpe.",
        "papa|Tu prends aussi un jeu ?",
        "enfant-f|Oui.",
    )


def t2q_003(t1: int) -> list[str]:
    ou = {1: "dans la cuisine", 2: "près de la porte", 3: "dans la chambre"}[t1]
    return L(
        f"narrateur|Il reste un jeu, {ou}.",
        "narrateur|Le ballon rouge, le seau bleu, ou le doudou.",
    )


def t2_003(t1: int, t2: int) -> list[str]:
    table = {
        (1, 1): L(
            "narrateur|Le ballon rouge est sous la table, collé.",
            "narrateur|Une miette de cacao brille dessus.",
            "enfant-f|Il est là.",
            "papa|Tu le reprends, Mila ?",
            "enfant-f|Oui.",
            "narrateur|Mila le fait rouler jusqu'à elle.",
            "narrateur|Elle essuie la miette d'un doigt.",
            "maman|Tu le poses près de la tasse ?",
            "enfant-f|Près de la vitre.",
            "narrateur|Le ballon attend, et le soleil de buée aussi.",
        ),
        (1, 2): L(
            "narrateur|Le seau bleu sert de cache, près du four.",
            "narrateur|Un torchon dépasse, tout mou.",
            "enfant-f|Je mets la tasse dedans ?",
            "maman|Elle est encore chaude, tout doux.",
            "narrateur|Mila pose la tasse dans le seau, sans verser.",
            "papa|Tu portes le seau jusqu'à la vitre ?",
            "enfant-f|Oui.",
            "narrateur|Le seau tapote sa jambe, tout léger.",
            "narrateur|Elle pose tout près du soleil de buée.",
            "enfant-f|C'est mon plateau.",
        ),
        (1, 3): L(
            "narrateur|Le doudou est sur une chaise, près du cacao.",
            "narrateur|Il a une odeur de chocolat, tout douce.",
            "enfant-f|Il a vu le soleil.",
            "papa|Tu le reprends, avant d'oublier ?",
            "enfant-f|Oui.",
            "narrateur|Mila serre le doudou, un peu chaud.",
            "maman|Il reste avec toi, près de la vitre ?",
            "enfant-f|Avec moi.",
            "narrateur|Elle dessine encore un rayon, du doigt.",
            "narrateur|Le doudou regarde, et la tasse fume moins.",
        ),
        (2, 1): L(
            "narrateur|Le ballon rouge a roulé dans l'herbe froide.",
            "enfant-f|Il est tout mouillé.",
            "papa|Tu le reprends, puis tu l'essuies.",
            "narrateur|Mila le prend, une goutte tombe du caoutchouc.",
            "narrateur|Elle l'essuie sur le paillasson, tout doux.",
            "maman|Tu le poses près de la porte ?",
            "enfant-f|Oui.",
            "enfant-f|Pour la maison de buée.",
            "narrateur|Le ballon fait un rond, comme une fenêtre.",
            "papa|Ta maison a une fenêtre, maintenant.",
        ),
        (2, 2): L(
            "narrateur|Le seau bleu est sous le banc du jardin.",
            "narrateur|Deux feuilles mouillées dorment dedans.",
            "enfant-f|Je mets le crayon dedans.",
            "maman|Oui, il ne glissera plus.",
            "narrateur|Mila pose le crayon au fond, au sec.",
            "papa|Tu ramènes le seau près de la porte ?",
            "enfant-f|Oui.",
            "narrateur|Le seau tapote, et la maison de buée attend.",
            "narrateur|Elle pose le seau, le crayon est là.",
            "enfant-f|Je peux finir le toit.",
        ),
        (2, 3): L(
            "narrateur|Le doudou est resté sur le paillasson.",
            "narrateur|Une feuille sèche colle à son oreille.",
            "enfant-f|Je le reprends.",
            "papa|Oui, il rentre avec toi.",
            "narrateur|Mila enlève la feuille, tout doux.",
            "maman|Il était presque dehors, tout seul.",
            "enfant-f|Plus maintenant.",
            "narrateur|Elle le serre, la porte encore embuée.",
            "narrateur|La maison de buée a besoin d'une porte.",
            "enfant-f|Je la dessine.",
        ),
        (3, 1): L(
            "narrateur|Le ballon rouge est sous le lit, un peu plat.",
            "enfant-f|Je le vois.",
            "maman|Tu le reprends, Mila ?",
            "narrateur|Mila se baisse, et le tapis sent le savon.",
            "narrateur|Elle tire le ballon, qui reprend sa ronde.",
            "papa|Tu le poses près de la vitre ?",
            "enfant-f|Oui.",
            "enfant-f|C'est une bouée, pour le bateau.",
            "narrateur|Le ballon attend, et la voile de buée aussi.",
            "maman|L'écharpe te tient chaud, pendant le voyage ?",
            "enfant-f|Oui, maman.",
        ),
        (3, 2): L(
            "narrateur|Le seau bleu sert de coffre, près de l'armoire.",
            "narrateur|Un crayon de couleur dépasse déjà.",
            "enfant-f|Je mets le mien aussi.",
            "papa|Oui, tous les crayons voyagent.",
            "narrateur|Mila glisse son crayon dans le seau.",
            "maman|Tu portes le seau jusqu'à la vitre ?",
            "enfant-f|Oui.",
            "narrateur|Le seau est léger, l'écharpe frotte le bord.",
            "narrateur|Elle pose tout, et le bateau de buée attend.",
            "enfant-f|C'est ma cale.",
        ),
        (3, 3): L(
            "narrateur|Le doudou est sous la couverture, caché.",
            "enfant-f|Je te cherche.",
            "maman|Tu le reprends, avant de dessiner ?",
            "narrateur|Mila soulève la couverture, il est là.",
            "narrateur|Elle le sort, il sent encore le lit.",
            "papa|Il monte sur le bateau, avec toi ?",
            "enfant-f|Oui.",
            "enfant-f|Il tient la voile.",
            "narrateur|Mila pose le doudou sur le rebord.",
            "narrateur|L'écharpe et lui regardent la buée.",
        ),
    }
    return table[(t1, t2)]


def t3q_003() -> list[str]:
    return L(
        "narrateur|Il reste une chose, près de Mila.",
        "narrateur|Le crayon, la tasse, ou l'écharpe.",
    )


def t3_003(t1: int, t2: int, t3: int) -> list[str]:
    draw = DRAW[t1]
    if t3 == 1:
        head = L(
            "narrateur|Le crayon attend, encore un peu froid.",
            "enfant-f|Je finis le dessin.",
            "papa|Tu le reprends, Mila ?",
            "enfant-f|Oui.",
        )
        tail = {
            1: L(
                "narrateur|Mila trace un rayon, puis un autre.",
                "narrateur|Le soleil de buée devient plus net.",
                "maman|Il brille, maintenant.",
                "enfant-f|Il chauffe la tasse, pour de faux.",
            ),
            2: L(
                "narrateur|Mila trace une cheminée sur le toit.",
                "narrateur|La maison de buée a de la fumée.",
                "maman|Comme le cacao.",
                "enfant-f|Oui, une petite fumée.",
            ),
            3: L(
                "narrateur|Mila trace une vague sous la coque.",
                "narrateur|Le bateau de buée avance un peu.",
                "maman|Il part.",
                "enfant-f|Tout doux, sur la vitre.",
            ),
        }[t1]
    elif t3 == 2:
        head = L(
            "narrateur|La tasse n'est plus trop chaude.",
            "enfant-f|Je la reprends.",
            "maman|Tu souffles encore un peu ?",
            "enfant-f|Oui.",
        )
        tail = {
            1: L(
                "narrateur|Mila boit, ça sent le chocolat tout près.",
                "narrateur|Son doigt est chaud, pour la buée.",
                "papa|Tu ajoutes un rayon ?",
                "enfant-f|Un petit, avec le doigt.",
            ),
            2: L(
                "narrateur|Mila boit, une goutte reste au bord.",
                "narrateur|Elle essuie, puis touche la vitre.",
                "papa|Ta maison a une lumière, maintenant.",
                "enfant-f|C'est le cacao.",
            ),
            3: L(
                "narrateur|Mila boit, le cacao descend tout doux.",
                "narrateur|Elle pose la tasse, et la voile attend.",
                "papa|Le bateau a son goûter.",
                "enfant-f|Il peut partir.",
            ),
        }[t1]
    else:
        head = L(
            "narrateur|L'écharpe a glissé d'une épaule.",
            "enfant-f|Je la reprends.",
            "maman|Autour de toi, près de la vitre froide.",
            "enfant-f|Voilà.",
        )
        tail = {
            1: L(
                "narrateur|Mila est au chaud, et finit un rayon.",
                "narrateur|Le soleil de buée touche presque le cadre.",
                "papa|Tu as les épaules couvertes ?",
                "enfant-f|Oui, papa.",
            ),
            2: L(
                "narrateur|Mila est au chaud, et finit une fenêtre.",
                "narrateur|La maison de buée a deux yeux, maintenant.",
                "papa|Tu as les épaules couvertes ?",
                "enfant-f|Oui, papa.",
            ),
            3: L(
                "narrateur|Mila est au chaud, et finit la voile.",
                "narrateur|Le bateau de buée tient tout seul.",
                "papa|Tu as les épaules couvertes ?",
                "enfant-f|Oui, papa.",
            ),
        }[t1]
    extra = {
        1: "narrateur|Près du dessin, le ballon rouge reste.",
        2: "narrateur|Dans le seau bleu, un crayon attend encore.",
        3: "narrateur|Tout contre Mila, le doudou regarde.",
    }[t2]
    _ = draw
    return head + tail + [extra]


def fin_003(t1: int, t2: int, t3: int) -> list[str]:
    draw_done = {
        1: "narrateur|Le soleil de buée reste, tout rond.",
        2: "narrateur|La maison de buée garde son toit.",
        3: "narrateur|Le bateau de buée garde sa voile.",
    }[t1]
    obj = {
        1: "narrateur|Puis le ballon rouge s'endort contre le mur.",
        2: "narrateur|Puis le seau bleu reste près de la porte.",
        3: "narrateur|Puis le doudou rentre contre l'épaule de Mila.",
    }[t2]
    left = {
        1: "narrateur|Enfin, le crayon rejoint le pot, tout sec.",
        2: "narrateur|Enfin, la tasse est vide, encore un peu tiède.",
        3: "narrateur|Enfin, l'écharpe reste autour du cou.",
    }[t3]
    place = {
        1: "narrateur|La cuisine sent encore le cacao, tout calme.",
        2: "narrateur|La porte du jardin n'a plus de goutte.",
        3: "narrateur|Le rideau de la chambre retombe, tout doux.",
    }[t1]
    ask = {
        1: "maman|Tu as repris la tasse, Mila ?",
        2: "papa|Tu as repris le crayon ?",
        3: "maman|Tu as repris l'écharpe ?",
    }[t3]
    return L(
        draw_done,
        obj,
        left,
        ask,
        "enfant-f|Oui.",
        "papa|Merci, Mila.",
        place,
    )


def build_003() -> dict:
    s: dict[str, list[str]] = {}
    s["CHK_T0000_P0000"] = L(
        "narrateur|La tasse de cacao fume encore, toute ronde.",
        "narrateur|Ça sent le chocolat chaud, tout près.",
        "narrateur|Une goutte glisse sur la vitre du salon.",
        "narrateur|Elle laisse un trait brillant, comme un crayon.",
        "narrateur|Le tapis est chaud, juste là.",
        "narrateur|Un carré de buée attend le doigt de Mila.",
        "enfant-f|Je veux dessiner, maman.",
        "enfant-f|Et boire le cacao.",
        "maman|Le cacao est encore trop chaud.",
        "papa|Tu as vu la goutte ?",
        "enfant-f|Elle descend.",
        "narrateur|En ce moment, Mila pose le doigt sur le verre.",
        "narrateur|Le verre est froid, le cacao est chaud.",
        "enfant-f|Je commence où ?",
        "maman|Où tu veux, Mila.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Mila va où, d'abord ?",
        "narrateur|La cuisine, le jardin, ou la chambre.",
    )
    for t1 in (1, 2, 3):
        p = pre(t1)
        s[p] = t1_003(t1)
        s[f"{p}_Q0001"] = q_003(t1)
        s[f"{p}_C0001"] = c_003(t1)
        s[f"{p}_T0002_P0000"] = t2q_003(t1)
        for t2 in (1, 2, 3):
            s[f"{p}_T0002_P000{t2}"] = t2_003(t1, t2)
            s[f"{p}_T0002_P000{t2}_T0003_P0000"] = t3q_003()
            for t3 in (1, 2, 3):
                s[f"{p}_T0002_P000{t2}_T0003_P000{t3}"] = t3_003(t1, t2, t3)
                s[f"{p}_T0002_P000{t2}_T0003_P000{t3}_F0001"] = fin_003(t1, t2, t3)
    return s


def sons_003(scripts: dict) -> dict:
    return {cid: "" for cid in scripts}


def patch_questions_002() -> None:
    path = ROOT / "TREE-AUT-002" / "merged.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for ch in data["chunks"]:
        if ch["kind"] == "passage_question":
            ch["expected_answer"] = "manteau"
            ch["accepted_examples"] = "manteau | le manteau | son manteau | prendre manteau"
            ch["retry_prompt"] = "Elle a pris le manteau. Sarah a pris quoi ?"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check("TREE-AUT-002", data["age_band"], data["chunks"])


def patch_questions_003() -> None:
    path = ROOT / "TREE-AUT-003" / "merged.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for ch in data["chunks"]:
        if ch["kind"] == "passage_question":
            ch["expected_answer"] = "reprendre"
            ch["accepted_examples"] = "reprendre | elle reprend | ses affaires | la tasse | le crayon | l'écharpe"
            ch["retry_prompt"] = "Elle revient la reprendre. Mila fait quoi ?"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check("TREE-AUT-003", data["age_band"], data["chunks"])


def main() -> None:
    s002 = build_002()
    vet("TREE-AUT-002", s002)
    write_story(
        "TREE-AUT-002",
        "Sarah veut le banc gris du jardin. Le manteau attend au crochet. "
        "Elle sort trop vite, l'air pique, elle revient le prendre, puis le jardin s'ouvre.",
        "Le manteau du jardin gris",
        "Sarah, papa, maman",
        "entrée, crochet, jardin gris d'automne",
        s002,
        sons_002(s002),
    )
    patch_questions_002()
    relecture(
        "TREE-AUT-002",
        "Le manteau du jardin gris",
        "Sarah veut le banc gris. Trois manteaux, trois imprévus (manche, oubli, marche). "
        "Ballon, seau ou doudou au jardin, puis chat, chien ou poule. Elle raccroche.",
        "Prénom Nora retiré. Leçon implicite (froid → retour au crochet). "
        "T1 rouge/bleu/vert changent l'imprévu. Fin sans « L'histoire est finie ».",
    )

    s003 = build_003()
    vet("TREE-AUT-003", s003)
    write_story(
        "TREE-AUT-003",
        "Mila veut du cacao et dessiner dans la buée. Une goutte glisse. "
        "Elle part trop vite, la tasse, le crayon ou l'écharpe reste. Elle revient, puis le dessin se termine.",
        "La tasse de cacao et la vitre",
        "Mila, papa, maman",
        "salon, cuisine, jardin, chambre, vitre embuée",
        s003,
        sons_003(s003),
    )
    patch_t3_labels("TREE-AUT-003", "le crayon", "la tasse", "l'écharpe")
    patch_questions_003()
    relecture(
        "TREE-AUT-003",
        "La tasse de cacao et la vitre",
        "Mila veut cacao et dessin dans la buée. Cuisine, jardin ou chambre. "
        "Elle oublie, elle reprend. Ballon, seau ou doudou, puis crayon, tasse ou écharpe.",
        "Maya/Nino → Mila. T3 Tom/Léa/Sami → objets. Leçon implicite (revenir chercher). "
        "Fin vécue, sans slogan.",
    )


if __name__ == "__main__":
    main()
