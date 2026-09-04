#!/usr/bin/env python3
"""TREE-AUT-020 / TREE-AUT-021 — récit implicite, graphe conservé, D16."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    ROOT,
    check,
    make_chunk,
    relecture,
    words,
)

# ---------------------------------------------------------------------------
# TREE-AUT-020  N1  Amir  AUT.AFF.003  chat à la fenêtre
# Sara → Amir. Pas une leçon de départ : le chat, le jardin, le seau oublié.
# L3 labels : manteau / chaussures / sac (plus Tom Léa Sami).
# ---------------------------------------------------------------------------

L1_020 = {
    1: {"lab": "le bac à sable", "ici": "au bac à sable", "ou": "vers le bac à sable"},
    2: {"lab": "le toboggan", "ici": "au toboggan", "ou": "vers le toboggan"},
    3: {"lab": "les balançoires", "ici": "aux balançoires", "ou": "vers les balançoires"},
}
L2_020 = {
    1: {"lab": "le ballon", "obj": "le ballon", "un": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau", "un": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou", "un": "le doudou"},
}
L3_020 = {
    1: {"lab": "le manteau", "fait": "pris le manteau bleu"},
    2: {"lab": "les chaussures", "fait": "mis les chaussures"},
    3: {"lab": "le sac", "fait": "pris le sac"},
}

ARRIVE_020 = {
    1: [
        "narrateur|Amir va vers le bac à sable.",
        "narrateur|Le bac est juste sous la fenêtre.",
        "narrateur|Le sable est encore un peu frais.",
        "narrateur|Le chat regarde depuis la vitre.",
        "enfant-m|Il me voit.",
        "papa|On joue un peu.",
        "maman|Le seau est près du bac.",
        "narrateur|Amir enfonce les mains.",
        "narrateur|Ça fait chh, tout doux.",
        "enfant-m|Ça chante, papa.",
        "papa|Oui.",
        "papa|Le sable chante.",
        "narrateur|Un grain reste sous son ongle.",
        "narrateur|Le manteau reste sur la chaise.",
        "enfant-m|Le chat tapote encore.",
        "maman|On le voit d'ici.",
    ],
    2: [
        "narrateur|Amir va vers le toboggan.",
        "narrateur|Il est dans le petit jardin.",
        "narrateur|Le bois est froid, un peu.",
        "narrateur|L'ombre de la fenêtre est dessus.",
        "enfant-m|Je glisse.",
        "papa|J'attends en bas.",
        "maman|Le seau est au pied.",
        "narrateur|Amir monte, tout doux.",
        "narrateur|Le bois fait toc, toc.",
        "enfant-m|Houuu.",
        "narrateur|Ses pieds retrouvent l'herbe.",
        "papa|Tu as les joues roses.",
        "narrateur|Une feuille colle sur la rampe.",
        "narrateur|Le manteau reste à la chaise.",
        "enfant-m|Encore une fois ?",
        "maman|Une fois, d'accord.",
    ],
    3: [
        "narrateur|Amir va vers les balançoires.",
        "narrateur|Les cordes bougent un peu.",
        "narrateur|Le siège de bois est lisse.",
        "narrateur|Le chat tapote encore la vitre.",
        "enfant-m|Pousse, maman.",
        "maman|Tout doux.",
        "papa|Le seau est sous le siège.",
        "narrateur|Amir avance, puis revient.",
        "narrateur|Le vent lui touche le nez.",
        "enfant-m|Je vois le chat.",
        "papa|Il tapote toujours.",
        "narrateur|Une corde fait cling, puis se tait.",
        "narrateur|Le manteau reste sur la chaise.",
        "enfant-m|Encore un peu.",
        "maman|Un peu, oui.",
    ],
}

Q_020 = {
    1: [
        "narrateur|Le seau est encore près du bac.",
        "papa|Amir, tu fais quoi ?",
    ],
    2: [
        "narrateur|Le seau est encore au pied.",
        "maman|Amir, tu fais quoi ?",
    ],
    3: [
        "narrateur|Le seau est encore sous le siège.",
        "papa|Amir, tu fais quoi ?",
    ],
}

C_020 = {
    1: [
        "narrateur|Amir revient vers le bac.",
        "narrateur|Il prend le seau jaune.",
        "enfant-m|Il était là.",
        "papa|Oui.",
        "papa|Il t'attendait.",
        "maman|Le manteau est encore à la chaise.",
        "narrateur|Un grain reste sur sa joue.",
        "papa|Merci, Amir.",
    ],
    2: [
        "narrateur|Amir s'arrête au bas du toboggan.",
        "narrateur|Il prend le seau jaune.",
        "enfant-m|Il sonne.",
        "maman|Oui.",
        "maman|Il était au pied.",
        "papa|Le manteau est encore à la chaise.",
        "narrateur|La feuille reste sur la rampe.",
        "maman|Merci, Amir.",
    ],
    3: [
        "narrateur|Amir pose un pied au sol.",
        "narrateur|Il prend le seau sous le siège.",
        "enfant-m|Je l'ai.",
        "papa|Oui.",
        "papa|Il t'attendait.",
        "maman|Le manteau est encore à la chaise.",
        "narrateur|La corde ne fait plus cling.",
        "papa|Merci, Amir.",
    ],
}

PLAY_020 = {
    (1, 1): [
        "narrateur|Amir a choisi le ballon.",
        "narrateur|Le ballon est bleu, un peu lisse.",
        "narrateur|Il roule une fois, puis s'arrête.",
        "papa|Le ballon reste près de nous.",
        "enfant-m|Il est bleu, papa.",
        "maman|Le chat le voit, depuis la vitre.",
        "narrateur|Un grain de sable colle au cuir.",
        "enfant-m|Il gratte un peu.",
        "papa|Tu le tiens ?",
        "enfant-m|Oui.",
        "narrateur|Le seau jaune reste à sa droite.",
    ],
    (1, 2): [
        "narrateur|Amir a choisi le seau.",
        "narrateur|Le seau jaune a du sable.",
        "narrateur|L'anse est un peu froide.",
        "maman|C'est ton seau, Amir.",
        "enfant-m|Il est jaune.",
        "papa|Tu verses encore ?",
        "narrateur|Il verse, tout doux.",
        "narrateur|Ça fait chh contre le bois.",
        "enfant-m|Encore un château.",
        "maman|Tout petit, dans le bac.",
        "narrateur|Le chat tapote une fois.",
    ],
    (1, 3): [
        "narrateur|Amir a choisi le doudou.",
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Un peu de sable est dessus.",
        "maman|Il t'attendait, près de la vitre.",
        "enfant-m|Il est doux.",
        "papa|Il a vu le chat, lui aussi.",
        "narrateur|Amir le serre contre sa joue.",
        "enfant-m|Il vient.",
        "maman|Oui.",
        "narrateur|L'oreille du doudou est chaude.",
        "narrateur|Le seau reste un peu plus loin.",
    ],
    (2, 1): [
        "narrateur|Amir a choisi le ballon.",
        "narrateur|Il est bleu, un peu froid.",
        "narrateur|Il fait un petit bond près de la rampe.",
        "papa|Le ballon reste avec nous.",
        "enfant-m|Il a glissé, comme moi.",
        "maman|La feuille reste sur la rampe.",
        "narrateur|Amir pose le ballon contre le seau.",
        "enfant-m|Ils se parlent.",
        "papa|Tout doux, oui.",
        "narrateur|Un brin d'herbe colle au cuir.",
        "narrateur|Le manteau reste à la chaise.",
    ],
    (2, 2): [
        "narrateur|Amir a choisi le seau.",
        "narrateur|Le seau sonne tout doux contre une marche.",
        "narrateur|L'anse est froide, près du bois.",
        "maman|Tu le poses au pied ?",
        "enfant-m|Non.",
        "enfant-m|Il vient.",
        "papa|Il a vu le toboggan.",
        "narrateur|Amir le serre à deux mains.",
        "narrateur|Du sable fin brille au fond.",
        "maman|Le bois du toboggan se tait.",
        "narrateur|Une feuille tourne sur l'herbe.",
    ],
    (2, 3): [
        "narrateur|Amir a choisi le doudou.",
        "narrateur|Le doudou a vu le toboggan, tout gris.",
        "narrateur|L'oreille molle a un peu d'herbe.",
        "maman|Il a glissé avec toi ?",
        "enfant-m|Dans la poche, un moment.",
        "papa|Il est au chaud, maintenant.",
        "narrateur|Amir le serre, puis souffle.",
        "enfant-m|Il a eu peur, un peu.",
        "maman|Il est avec toi.",
        "narrateur|La rampe brille encore, tout loin.",
        "narrateur|Le seau reste près des marches.",
    ],
    (3, 1): [
        "narrateur|Amir a choisi le ballon.",
        "narrateur|Un brin d'herbe colle au ballon.",
        "narrateur|La corde de la balançoire le frôle.",
        "papa|Le ballon reste près de nous.",
        "enfant-m|Il voyage.",
        "maman|Le chat le voit encore.",
        "narrateur|Amir le pose sur ses genoux.",
        "enfant-m|Il ne tombe pas.",
        "papa|Tu le tiens bien.",
        "narrateur|Un nuage passe au-dessus.",
        "narrateur|Le seau reste au pied de bois.",
    ],
    (3, 2): [
        "narrateur|Amir a choisi le seau.",
        "narrateur|L'anse du seau est froide, près de la corde.",
        "narrateur|Le seau jaune pose son ombre.",
        "maman|Tu le mets sous le siège ?",
        "enfant-m|Non.",
        "enfant-m|Il vient sur moi.",
        "papa|Il a senti le vent.",
        "narrateur|Amir le cale entre ses genoux.",
        "narrateur|Un cling lointain, puis plus rien.",
        "maman|La corde se tait.",
        "narrateur|Le chat tapote une dernière fois.",
    ],
    (3, 3): [
        "narrateur|Amir a choisi le doudou.",
        "narrateur|Le doudou a senti le vent, tout doux.",
        "narrateur|L'oreille grise dépasse de ses bras.",
        "maman|Il s'assoit avec toi ?",
        "enfant-m|Oui.",
        "enfant-m|Il voyage.",
        "papa|La corde ne le touche pas.",
        "narrateur|Amir le serre contre le seau.",
        "narrateur|Un fil gris pend, tout mince.",
        "maman|On rentrera tout à l'heure.",
        "narrateur|Le siège de bois est tiède, vide un peu.",
    ],
}

L3_BODY_020 = {
    1: [
        "narrateur|Le manteau bleu est encore sur la chaise.",
        "narrateur|Il est encore à l'envers.",
        "narrateur|Du sable est sur la manche.",
        "papa|Le manteau, Amir.",
        "enfant-m|Je le prends.",
        "narrateur|Amir prend le manteau.",
        "narrateur|Le tissu est un peu rêche.",
        "enfant-m|Je l'ai, papa.",
        "maman|On tourne la manche.",
        "narrateur|La manche retrouve sa place.",
    ],
    2: [
        "narrateur|Les chaussures attendent près de la porte.",
        "narrateur|Un petit caillou est dedans.",
        "papa|Tes chaussures, Amir.",
        "enfant-m|Il y a un caillou.",
        "maman|On le verse, tout doux.",
        "narrateur|Amir secoue la chaussure.",
        "narrateur|Le caillou tombe, tic.",
        "enfant-m|Elles sont vides.",
        "papa|Tu les mets ?",
        "narrateur|Amir glisse un pied, puis l'autre.",
    ],
    3: [
        "narrateur|Le sac est près de la fenêtre.",
        "narrateur|La sangle est un peu molle.",
        "maman|Le sac, Amir.",
        "enfant-m|Il est vide.",
        "papa|On le prend quand même.",
        "narrateur|Amir passe la sangle.",
        "narrateur|Le sac tape doucement sa hanche.",
        "enfant-m|Il vient.",
        "maman|Oui.",
        "narrateur|Le doudou peut s'y caler, plus tard.",
    ],
}

IMG_020 = {
    (1, 1, 1): "Un grain rouge colle à la manche bleue.",
    (1, 1, 2): "Le ballon laisse une trace près des chaussures.",
    (1, 1, 3): "Un brin d'herbe reste au fond du sac.",
    (1, 2, 1): "Du sable fin brille sur le col du manteau.",
    (1, 2, 2): "L'anse jaune touche une chaussure.",
    (1, 2, 3): "Un coquillage minuscule roule dans le sac.",
    (1, 3, 1): "L'oreille grise dépasse du manteau.",
    (1, 3, 2): "Le doudou sent encore le sable, près des chaussures.",
    (1, 3, 3): "Un fil gris pend du sac.",
    (2, 1, 1): "La feuille jaune colle au manteau.",
    (2, 1, 2): "Le ballon est un peu froid, près des chaussures.",
    (2, 1, 3): "Une goutte glisse vers le sac.",
    (2, 2, 1): "Le seau sonne tout doux contre le manteau.",
    (2, 2, 2): "Le métal du toboggan se tait, près des chaussures.",
    (2, 2, 3): "Un pas sur la rampe, puis le sac.",
    (2, 3, 1): "Le doudou a vu le toboggan, contre le manteau.",
    (2, 3, 2): "L'oreille molle dépasse près des chaussures.",
    (2, 3, 3): "La rampe brille encore, loin du sac.",
    (3, 1, 1): "La corde a fait cling, près du manteau.",
    (3, 1, 2): "Le ballon a touché l'herbe, près des chaussures.",
    (3, 1, 3): "Un nuage passe au-dessus du sac.",
    (3, 2, 1): "L'anse du seau est froide, contre le manteau.",
    (3, 2, 2): "Un cling lointain, et les chaussures.",
    (3, 2, 3): "Le seau jaune pose son ombre au sac.",
    (3, 3, 1): "Le doudou a senti le vent, dans le manteau.",
    (3, 3, 2): "La corde se tait, près des chaussures.",
    (3, 3, 3): "L'oreille grise dépasse du sac.",
}

FIN_IMG_020 = {
    (1, 1, 1): "Le chat se lèche la patte, tout calme.",
    (1, 1, 2): "Le carré de soleil a bougé, sur le bois.",
    (1, 1, 3): "Un grain de sable reste dans le seau.",
    (1, 2, 1): "Le seau jaune sèche sous la fenêtre.",
    (1, 2, 2): "Le chat cligne, puis s'endort.",
    (1, 2, 3): "La poussière ne danse plus, dans le carré.",
    (1, 3, 1): "Le doudou s'installe contre la vitre.",
    (1, 3, 2): "Le seau luit, tout seul, dans le carré.",
    (1, 3, 3): "La queue du chat ne fait plus tic.",
    (2, 1, 1): "Le manteau bleu retrouve la chaise.",
    (2, 1, 2): "Une feuille sèche près des chaussures.",
    (2, 1, 3): "Le ballon a encore l'odeur de l'herbe.",
    (2, 2, 1): "Le seau penche un peu, sous la fenêtre.",
    (2, 2, 2): "La rampe du toboggan reste loin, maintenant.",
    (2, 2, 3): "Le carré de soleil a glissé, sur le bois.",
    (2, 3, 1): "L'oreille du doudou dépasse de la chaise.",
    (2, 3, 2): "Le bois du toboggan est loin, tout froid.",
    (2, 3, 3): "Le rayon du soir a bougé, sur le tapis.",
    (3, 1, 1): "Le ballon s'endort près de la chaise.",
    (3, 1, 2): "Le siège de bois attend déjà demain.",
    (3, 1, 3): "Ça sent encore la poussière chaude, un peu.",
    (3, 2, 1): "Le seau pose son ombre sur le bois.",
    (3, 2, 2): "Les chaussures font un dernier clac.",
    (3, 2, 3): "Les cordes ne bougent plus, dehors.",
    (3, 3, 1): "Le doudou a l'odeur du vent, à la fenêtre.",
    (3, 3, 2): "Le chat rentre dans le carré de soleil.",
    (3, 3, 3): "La vitre ne tapote plus.",
}


def extras_t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def extras_q(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


def body_020(i: int, j: int, k: int) -> list[str]:
    loc = L1_020[i]
    jeu = L2_020[j]
    return (
        [
            f"narrateur|Amir quitte {loc['lab']}.",
            f"narrateur|Il a {jeu['obj']} avec lui.",
            "enfant-m|On rentre ?",
            "papa|Un moment, oui.",
        ]
        + L3_BODY_020[k]
        + [
            f"narrateur|{IMG_020[(i, j, k)]}",
            "papa|Merci, Amir.",
            "enfant-m|Le chat m'attend.",
            "maman|On le revoit à la fenêtre.",
        ]
    )


def fin_020(i: int, j: int, k: int) -> list[str]:
    loc = L1_020[i]
    jeu = L2_020[j]
    reste = L3_020[k]
    return [
        "narrateur|Amir est de nouveau près de la fenêtre.",
        f"narrateur|Il a joué {loc['ici']}.",
        f"narrateur|Il a pris {jeu['lab']}.",
        f"narrateur|Il a {reste['fait']}.",
        "enfant-m|Le chat est encore là.",
        "maman|Il se lèche la patte.",
        "papa|Le seau est avec nous.",
        f"narrateur|{IMG_020[(i, j, k)]}",
        f"narrateur|{FIN_IMG_020[(i, j, k)]}",
    ]


def build_020() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|Un chat tapote la vitre.",
        "narrateur|Sa queue fait tic, tic, tic.",
        "narrateur|Le soleil entre, tout bas.",
        "narrateur|Il fait un carré chaud sur le bois.",
        "narrateur|Dans le carré, un seau jaune brille.",
        "narrateur|Des grains de sable y dorment.",
        "narrateur|Un manteau bleu est sur la chaise.",
        "narrateur|Le manteau est à l'envers.",
        "narrateur|Un doudou gris regarde par la fenêtre.",
        "narrateur|Le doudou a une oreille pliée.",
        "narrateur|L'air sent la poussière chaude.",
        "papa|Amir, tu as vu le chat ?",
        "enfant-m|Oui, papa.",
        "enfant-m|Il tapote.",
        "maman|Le soleil est déjà bas.",
        "narrateur|En ce moment, Amir colle son nez.",
        "narrateur|Le verre est un peu tiède.",
        "enfant-m|Je veux le jardin.",
        "enfant-m|Le chat regarde dehors.",
        "papa|Le petit jardin est juste là.",
        "maman|On sort un moment ?",
        "enfant-m|Oui.",
        "narrateur|Amir glisse du carré de soleil.",
        "narrateur|Le seau reste dans le carré.",
        "narrateur|Le manteau reste sur la chaise.",
    ]
    sons["CHK_T0000_P0000"] = "chat,vitre"

    s["CHK_T0001_P0000"] = [
        "papa|On joue où, dans le jardin ?",
        "narrateur|Le bac à sable.",
        "narrateur|Le toboggan.",
        "narrateur|Ou les balançoires.",
    ]
    sons["CHK_T0001_P0000"] = ""
    extras["CHK_T0001_P0000"] = extras_t3("le bac à sable", "le toboggan", "les balançoires")

    for i, loc in L1_020.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_020[i]
        sons[p] = {1: "sable", 2: "enfants_parc", 3: "enfants_parc"}[i]
        s[f"{p}_Q0001"] = Q_020[i]
        sons[f"{p}_Q0001"] = ""
        extras[f"{p}_Q0001"] = extras_q(
            "reprendre",
            "reprendre | le seau | le manteau | ses affaires | il le prend | je le prends",
            "Il reprend le seau. Amir fait quoi ?",
        )
        s[f"{p}_C0001"] = C_020[i]
        sons[f"{p}_C0001"] = ""
        s[f"{p}_T0002_P0000"] = [
            "maman|Tu emportes quel jeu ?",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Ou le doudou.",
        ]
        sons[f"{p}_T0002_P0000"] = ""
        extras[f"{p}_T0002_P0000"] = extras_t3("le ballon", "le seau", "le doudou")

        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_020[(i, j)] + [
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[p2] = ""
            s[f"{p2}_T0003_P0000"] = [
                "papa|On emporte encore quoi ?",
                "narrateur|Le manteau.",
                "narrateur|Les chaussures.",
                "narrateur|Ou le sac.",
            ]
            sons[f"{p2}_T0003_P0000"] = ""
            extras[f"{p2}_T0003_P0000"] = extras_t3("le manteau", "les chaussures", "le sac")

            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_020(i, j, k)
                sons[p3] = ""
                s[f"{p3}_F0001"] = fin_020(i, j, k)
                sons[f"{p3}_F0001"] = ""
    return s, sons, extras


# ---------------------------------------------------------------------------
# TREE-AUT-021  N2  Mila  AUT.AFF.001  grain de sable dans la sangle
# Lina → Mila. Pas une liste de sac : elle veut la mer. La sangle pique.
# L3 labels : banc / cabine / galets (plus Tom Léa Sami).
# ---------------------------------------------------------------------------

L1_021 = {
    1: {"lab": "le bac à sable", "ici": "au bac à sable"},
    2: {"lab": "le toboggan", "ici": "au toboggan"},
    3: {"lab": "les balançoires", "ici": "aux balançoires"},
}
L2_021 = {
    1: {"lab": "le ballon", "obj": "le ballon", "un": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau", "un": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou", "un": "le doudou"},
}
L3_021 = {
    1: {"lab": "le banc", "ou": "vers le banc", "ici": "sur le banc"},
    2: {"lab": "la cabine", "ou": "vers la cabine", "ici": "près de la cabine"},
    3: {"lab": "les galets", "ou": "vers les galets", "ici": "près des galets"},
}

ARRIVE_021 = {
    1: [
        "narrateur|Mila s'agenouille au bac à sable.",
        "narrateur|Le sable est frais, un peu collant.",
        "narrateur|Ça fait chh sous la paume.",
        "narrateur|Le sac bleu reste près du bois.",
        "enfant-f|Un château, papa.",
        "papa|D'accord.",
        "papa|Le sac reste près de toi.",
        "narrateur|Mila verse le sable.",
        "narrateur|Un grain reste sous son ongle.",
        "narrateur|Ça sent le sel, tout près.",
        "maman|La sangle a encore un grain ?",
        "enfant-f|Un tout petit.",
        "narrateur|Mila secoue la sangle une fois.",
        "narrateur|Le grain tombe dans le bac.",
        "papa|Le château tient, tout rond.",
        "enfant-f|C'est mon château de mer.",
    ],
    2: [
        "narrateur|Mila va vers le toboggan.",
        "narrateur|Le métal est tiède sous la paume.",
        "narrateur|Les marches font toc, toc.",
        "narrateur|Le sac bleu est au pied du toboggan.",
        "papa|J'attends en bas.",
        "enfant-f|Je vais, papa.",
        "narrateur|Le vent touche ses cheveux.",
        "narrateur|Elle glisse.",
        "narrateur|Ça fait houuu, tout doux.",
        "enfant-f|Le sac m'a vue.",
        "maman|Il est encore au pied ?",
        "enfant-f|Oui.",
        "narrateur|Une feuille colle sur la rampe.",
        "narrateur|La sangle a pris un peu de sable.",
        "papa|Tu n'as plus le grain dans la main ?",
        "enfant-f|Non, je glisse encore.",
    ],
    3: [
        "narrateur|Mila va vers les balançoires.",
        "narrateur|La corde est un peu rêche.",
        "narrateur|Le siège est lisse, un peu chaud.",
        "narrateur|Le sac bleu est posé dans l'herbe.",
        "maman|Je pousse tout doux.",
        "enfant-f|Encore un peu ?",
        "maman|Encore.",
        "narrateur|Le vent passe dans ses cheveux.",
        "narrateur|Un oiseau passe au-dessus.",
        "papa|Tu le tiens bien, le siège.",
        "enfant-f|Il voyage.",
        "narrateur|La sangle a un brin d'herbe.",
        "narrateur|Mila la secoue du bout du pied.",
        "maman|Tu as les joues roses, Mila.",
        "enfant-f|Encore une fois.",
        "papa|Une dernière, d'accord.",
    ],
}

Q_021 = {
    1: [
        "narrateur|La sangle pique encore, contre le bac.",
        "maman|Mila prend quoi, pour la mer ?",
    ],
    2: [
        "narrateur|Le sac est encore au pied du toboggan.",
        "papa|Mila prend quoi, pour la mer ?",
    ],
    3: [
        "narrateur|Le sac est encore dans l'herbe.",
        "maman|Mila prend quoi, pour la mer ?",
    ],
}

C_021 = {
    1: [
        "narrateur|Mila reprend le sac bleu.",
        "narrateur|Elle secoue la sangle, tout fort.",
        "narrateur|Un grain tombe, tic, dans le sable.",
        "enfant-f|Il est parti.",
        "maman|Merci, Mila.",
        "papa|Le sac vient avec nous.",
        "enfant-f|Pour la mer.",
        "narrateur|Le château reste un moment, tout petit.",
    ],
    2: [
        "narrateur|Mila redescend vers le sac.",
        "narrateur|Elle passe la sangle à l'épaule.",
        "narrateur|Un grain glisse, puis plus rien.",
        "enfant-f|Il ne pique plus.",
        "papa|Merci, Mila.",
        "maman|On peut jouer un peu.",
        "narrateur|Mila pose la main sur le tissu.",
        "narrateur|L'herbe sent encore le sel.",
    ],
    3: [
        "narrateur|Mila pose un pied au sol.",
        "narrateur|Elle ramasse le sac dans l'herbe.",
        "narrateur|La sangle reste près de sa main.",
        "enfant-f|Il ne part pas.",
        "maman|Merci, Mila.",
        "papa|On reste ensemble.",
        "narrateur|Une chaîne fait cling, tout doux.",
        "narrateur|Le vent touche encore ses joues.",
    ],
}

PLAY_021 = {
    (1, 1): [
        "narrateur|Mila a choisi le ballon.",
        "narrateur|Il est rouge, un peu mou.",
        "narrateur|Un peu de sable colle dessus.",
        "papa|Le ballon reste près de nous.",
        "enfant-f|Il est trop gros pour le sac.",
        "maman|Tu le portes, alors.",
        "narrateur|Mila le serre sous le bras.",
        "narrateur|Le sac bleu tape sa hanche.",
        "enfant-f|Ils viennent tous les deux.",
        "papa|Tout doux, oui.",
        "narrateur|Un grain de sable colle au cuir.",
        "narrateur|Le château de sable reste un moment.",
    ],
    (1, 2): [
        "narrateur|Mila a choisi le seau.",
        "narrateur|Le seau jaune a du sable.",
        "narrateur|L'anse est un peu rêche.",
        "maman|C'est ton seau de mer.",
        "enfant-f|Il est jaune.",
        "papa|Tu le laisses au bac ?",
        "enfant-f|Non.",
        "enfant-f|Il vient.",
        "narrateur|Elle accroche l'anse au poignet.",
        "narrateur|Le sac reste à l'autre main.",
        "maman|L'anse dépasse un tout petit peu.",
        "narrateur|Du sable fin brille dans le seau.",
    ],
    (1, 3): [
        "narrateur|Mila a choisi le doudou.",
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Un peu de sable est dessus.",
        "maman|Il t'attendait, Mila.",
        "enfant-f|Il est doux.",
        "papa|Il peut s'asseoir dans le sac.",
        "narrateur|Elle l'enfonce tout doucement.",
        "narrateur|L'oreille dépasse de la sangle.",
        "enfant-f|Ils viennent.",
        "maman|Oui.",
        "narrateur|L'oreille du doudou est chaude.",
        "narrateur|Le château garde un creux, tout petit.",
    ],
    (2, 1): [
        "narrateur|Mila a choisi le ballon, près du toboggan.",
        "narrateur|Il rebondit une fois, tout mou.",
        "maman|Il va rouler sous la rampe ?",
        "enfant-f|Non.",
        "narrateur|Mila le prend à deux mains.",
        "narrateur|Le sac reste à l'épaule.",
        "papa|Il ne part plus.",
        "enfant-f|Le ballon voyage avec moi.",
        "narrateur|La feuille reste sur la rampe.",
        "maman|Le sac reste fermé, lui.",
        "narrateur|Le métal du toboggan se tait.",
    ],
    (2, 2): [
        "narrateur|Mila a choisi le seau, au pied du toboggan.",
        "narrateur|L'anse cliquette contre une marche.",
        "papa|Le seau va rester ici ?",
        "enfant-f|Non.",
        "narrateur|Mila le pose contre le sac.",
        "maman|Tu l'as mis avec nous ?",
        "enfant-f|Oui.",
        "enfant-f|Il est là.",
        "papa|L'anse cliquette encore.",
        "narrateur|Mila rit un peu.",
        "narrateur|Un pas sur la rampe, puis plus rien.",
    ],
    (2, 3): [
        "narrateur|Mila a choisi le doudou, près des marches.",
        "narrateur|Il a vu le toboggan, tout gris.",
        "maman|Il va rester sur la rampe ?",
        "enfant-f|Non.",
        "narrateur|Mila l'enfonce dans le sac, tout doux.",
        "papa|Il est au chaud, maintenant.",
        "enfant-f|Oui.",
        "narrateur|Mila souffle.",
        "narrateur|Le toboggan brille encore.",
        "maman|La sangle ne pique plus.",
        "narrateur|L'oreille molle dépasse du tissu bleu.",
    ],
    (3, 1): [
        "narrateur|Mila a choisi le ballon, près des chaînes.",
        "narrateur|Il fait un petit bond dans l'herbe.",
        "papa|Il va sous la balançoire ?",
        "enfant-f|Non.",
        "narrateur|Mila le rattrape.",
        "narrateur|Elle le serre, le sac à l'épaule.",
        "maman|Le vent ne l'emporte plus.",
        "enfant-f|Il est avec moi.",
        "narrateur|Une chaîne fait cling, tout près.",
        "papa|Le sac reste avec nous.",
        "narrateur|Un brin d'herbe colle au ballon.",
    ],
    (3, 2): [
        "narrateur|Mila a choisi le seau, sous le banc.",
        "narrateur|L'anse est froide, encore.",
        "maman|Il reste sous le banc ?",
        "enfant-f|Non.",
        "narrateur|Mila le pose contre le sac, tout droit.",
        "papa|L'anse dépasse un peu.",
        "enfant-f|Je la rentre.",
        "narrateur|Mila rentre l'anse.",
        "maman|Le sac tient mieux.",
        "narrateur|L'herbe est encore un peu mouillée.",
        "narrateur|Un cling lointain, puis le vent.",
    ],
    (3, 3): [
        "narrateur|Mila a choisi le doudou, sur le siège.",
        "narrateur|Il a pris un peu de vent.",
        "papa|Il reste sur la balançoire ?",
        "enfant-f|Non.",
        "narrateur|Mila le serre, puis le glisse dans le sac.",
        "maman|Il se réchauffe.",
        "enfant-f|Oui, contre moi.",
        "narrateur|Le bois du siège est chaud, vide maintenant.",
        "papa|Le sac est un peu plus lourd.",
        "narrateur|Le vent passe encore dans ses cheveux.",
        "narrateur|L'oreille grise dépasse de la sangle.",
    ],
}

L3_BODY_021 = {
    1: [
        "narrateur|Ils vont vers le banc.",
        "narrateur|Une vague lèche le bois du banc.",
        "narrateur|Le sac se cale sous le banc.",
        "enfant-f|Il y a encore un grain.",
        "papa|Dans la sangle ?",
        "narrateur|Mila secoue la sangle au-dessus du sable.",
        "narrateur|Le grain tombe, tic, sur le bois.",
        "maman|Le banc est à nous, un moment.",
        "enfant-f|Je m'assois.",
        "papa|Le sac reste sous tes pieds.",
    ],
    2: [
        "narrateur|Ils vont vers la cabine.",
        "narrateur|Le bois sent le sel, tout fort.",
        "narrateur|Un crochet attend, tout bas.",
        "enfant-f|Le sac, là.",
        "maman|Oui.",
        "maman|Au crochet.",
        "narrateur|Mila accroche la sangle.",
        "narrateur|Un grain brille encore, puis elle souffle.",
        "narrateur|Le grain tombe près du seuil.",
        "papa|La cabine fait de l'ombre.",
        "enfant-f|J'aime l'ombre.",
    ],
    3: [
        "narrateur|Ils vont vers les galets.",
        "narrateur|Les galets font clic, clic, sous le pied.",
        "narrateur|Le sac se pose sur le sable sec.",
        "enfant-f|Un galet pour moi.",
        "papa|Un seul, tout lisse.",
        "narrateur|Mila le serre, puis pose la sangle.",
        "narrateur|Un grain de sable pique encore.",
        "narrateur|Elle secoue, et le grain part vers l'eau.",
        "maman|L'eau chante, tout près.",
        "enfant-f|Le sac est avec nous.",
    ],
}

IMG_021 = {
    (1, 1, 1): "Un grain rouge colle au bois du banc.",
    (1, 1, 2): "Le ballon laisse une trace au seuil de la cabine.",
    (1, 1, 3): "Un brin d'herbe reste entre deux galets.",
    (1, 2, 1): "Du sable fin brille sous le banc.",
    (1, 2, 2): "L'anse jaune touche le bois de la cabine.",
    (1, 2, 3): "Un coquillage minuscule roule près des galets.",
    (1, 3, 1): "L'oreille grise dépasse sous le banc.",
    (1, 3, 2): "Le doudou sent encore le sable, dans la cabine.",
    (1, 3, 3): "Un fil gris pend près des galets.",
    (2, 1, 1): "La feuille jaune colle au bois du banc.",
    (2, 1, 2): "Le ballon est un peu froid, près de la cabine.",
    (2, 1, 3): "Une goutte glisse vers les galets.",
    (2, 2, 1): "Le seau sonne tout doux contre le banc.",
    (2, 2, 2): "Le métal du toboggan se tait, loin de la cabine.",
    (2, 2, 3): "Un pas sur la rampe, puis les galets.",
    (2, 3, 1): "Le doudou a vu le toboggan, sous le banc.",
    (2, 3, 2): "L'oreille molle dépasse dans la cabine.",
    (2, 3, 3): "La rampe brille encore, loin des galets.",
    (3, 1, 1): "La chaîne a fait cling, près du banc.",
    (3, 1, 2): "Le ballon a touché l'herbe, près de la cabine.",
    (3, 1, 3): "Un nuage passe au-dessus des galets.",
    (3, 2, 1): "L'anse du seau est froide, contre le banc.",
    (3, 2, 2): "Un cling lointain, et la cabine.",
    (3, 2, 3): "Le seau jaune pose son ombre aux galets.",
    (3, 3, 1): "Le doudou a senti le vent, sous le banc.",
    (3, 3, 2): "La chaîne se tait, près de la cabine.",
    (3, 3, 3): "L'oreille grise dépasse près des galets.",
}

FIN_IMG_021 = {
    (1, 1, 1): "La chaise de paille attend déjà le sac.",
    (1, 1, 2): "Une goutte de pêche sèche sur le bois.",
    (1, 1, 3): "Un grain de sable reste dans la sangle, tout petit.",
    (1, 2, 1): "Le seau jaune sèche près de la porte.",
    (1, 2, 2): "Le rideau blanc ne chatouille plus le carrelage.",
    (1, 2, 3): "Le bateau ne fait plus rum rum, dehors.",
    (1, 3, 1): "Le doudou s'installe dans le creux de la chaise.",
    (1, 3, 2): "Ça sent encore la pêche, un peu.",
    (1, 3, 3): "La sangle est lisse, maintenant.",
    (2, 1, 1): "Le ballon s'endort près de la chaise de paille.",
    (2, 1, 2): "Les sandales de papa sèchent, près de la porte.",
    (2, 1, 3): "Le ballon a encore l'odeur du vent.",
    (2, 2, 1): "Le seau penche un peu, sous la chaise.",
    (2, 2, 2): "La rampe du toboggan reste loin, maintenant.",
    (2, 2, 3): "Le carrelage est froid, sous les pieds.",
    (2, 3, 1): "L'oreille du doudou dépasse de la chaise.",
    (2, 3, 2): "Le bois de la cabine sent encore le sel.",
    (2, 3, 3): "Le rayon du soir a bougé, sur le rideau.",
    (3, 1, 1): "Le ballon s'endort près du sac bleu.",
    (3, 1, 2): "Le creux de la chaise attend Mila.",
    (3, 1, 3): "Ça sent encore le sel, un peu.",
    (3, 2, 1): "Le seau pose son ombre sur le carrelage.",
    (3, 2, 2): "Les sandales font un dernier clac.",
    (3, 2, 3): "Les galets ne font plus clic, dehors.",
    (3, 3, 1): "Le doudou a l'odeur de l'herbe, à la maison.",
    (3, 3, 2): "Le sac bleu retrouve la chaise de paille.",
    (3, 3, 3): "Le rideau blanc ne bouge plus.",
}


def body_021(i: int, j: int, k: int) -> list[str]:
    loc = L1_021[i]
    jeu = L2_021[j]
    lieu = L3_021[k]
    return (
        [
            "narrateur|C'est l'heure d'un autre coin.",
            f"narrateur|Mila quitte {loc['lab']}.",
            f"narrateur|Elle a {jeu['obj']} avec elle.",
            "enfant-f|Le sac vient.",
            "papa|Oui.",
            "papa|On l'emporte.",
        ]
        + L3_BODY_021[k]
        + [
            f"narrateur|{jeu['un'].capitalize()} reste {lieu['ici']}, un moment.",
            f"narrateur|{IMG_021[(i, j, k)]}",
            "maman|On rentre, tout à l'heure.",
            "enfant-f|Encore un peu.",
            "papa|Un peu, oui.",
        ]
    )


def fin_021(i: int, j: int, k: int) -> list[str]:
    loc = L1_021[i]
    jeu = L2_021[j]
    lieu = L3_021[k]
    return [
        "narrateur|La chaise de paille attend dans la maison.",
        f"narrateur|Mila a joué {loc['ici']}.",
        f"narrateur|Elle a choisi {jeu['lab']}.",
        f"narrateur|Elle est allée {lieu['ou']}.",
        "narrateur|Le sac bleu est avec elle.",
        "enfant-f|La sangle ne pique plus.",
        "maman|Le grain est resté à la mer.",
        "papa|Merci, Mila.",
        "narrateur|Elle pose le sac sur la chaise.",
        f"narrateur|{IMG_021[(i, j, k)]}",
        f"narrateur|{FIN_IMG_021[(i, j, k)]}",
    ]


def build_021() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|Le sac bleu attend sur la chaise de paille.",
        "narrateur|Un grain de sable brille dans la sangle.",
        "narrateur|Les sandales de papa sont encore mouillées.",
        "narrateur|Elles font clac, près de la porte.",
        "narrateur|Ça sent la pêche, toute mûre.",
        "narrateur|Maman coupe un quartier juteux.",
        "narrateur|Une goutte tombe sur le bois de la table.",
        "narrateur|Dehors, un bateau fait rum rum, tout loin.",
        "narrateur|Le vent pousse le rideau blanc.",
        "narrateur|Le rideau chatouille le carrelage froid.",
        "maman|Mila, tu as vu la mer ?",
        "papa|On y va, tout à l'heure.",
        "narrateur|En ce moment, Mila touche la sangle.",
        "narrateur|La sangle est un peu rêche.",
        "enfant-f|Il y a du sable, maman.",
        "enfant-f|Je veux la mer.",
        "maman|Le sac vient avec nous.",
        "narrateur|Mila soulève le sac bleu.",
        "narrateur|Le grain pique sa paume.",
        "enfant-f|Aïe, ça glisse.",
        "papa|Un grain, dans la sangle.",
        "narrateur|Mila secoue la sangle, tout fort.",
        "narrateur|Le grain tombe, tic, sur le carrelage.",
        "enfant-f|Il est parti.",
        "maman|On peut y aller, maintenant.",
        "enfant-f|On y va.",
    ]
    sons["CHK_T0000_P0000"] = "mer,sac"

    s["CHK_T0001_P0000"] = [
        "narrateur|Près de l'eau, trois coins attendent.",
        "papa|Le bac à sable, le toboggan, ou les balançoires ?",
        "maman|On emporte le sac.",
        "maman|Tu choisis.",
    ]
    sons["CHK_T0001_P0000"] = "mer"
    extras["CHK_T0001_P0000"] = extras_t3("le bac à sable", "le toboggan", "les balançoires")

    for i, loc in L1_021.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = ARRIVE_021[i]
        sons[p] = {1: "sable", 2: "enfants_parc", 3: "enfants_parc"}[i]
        s[f"{p}_Q0001"] = Q_021[i]
        sons[f"{p}_Q0001"] = ""
        extras[f"{p}_Q0001"] = extras_q(
            "sac",
            "sac | le sac | son sac | le sac bleu | elle le prend | je le prends",
            "Le sac bleu. Mila prend quoi ?",
        )
        s[f"{p}_C0001"] = C_021[i]
        sons[f"{p}_C0001"] = ""
        s[f"{p}_T0002_P0000"] = [
            "maman|Tu emportes quoi, avec toi ?",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Ou le doudou.",
        ]
        sons[f"{p}_T0002_P0000"] = ""
        extras[f"{p}_T0002_P0000"] = extras_t3("le ballon", "le seau", "le doudou")

        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = PLAY_021[(i, j)] + [
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[p2] = ""
            s[f"{p2}_T0003_P0000"] = [
                "papa|On va où, après, avec le sac ?",
                "narrateur|Le banc.",
                "narrateur|La cabine.",
                "narrateur|Les galets.",
            ]
            sons[f"{p2}_T0003_P0000"] = ""
            extras[f"{p2}_T0003_P0000"] = extras_t3("le banc", "la cabine", "les galets")

            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = body_021(i, j, k)
                sons[p3] = "mer" if k in (1, 3) else ""
                s[f"{p3}_F0001"] = fin_021(i, j, k)
                sons[f"{p3}_F0001"] = ""
    return s, sons, extras


def write_tree(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    extras: dict,
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} chunks missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            scale, rate = 1.28, "slow"
        elif src.get("age_band") == "N1":
            scale, rate = 1.22, "slow"
        else:
            scale, rate = 1.22, "medium"
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_lines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_lines[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} {c['chunk_id']} fin mécanique: {last}")
    nwords = sum(words(c["text"]) for c in out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {sid} {nwords} mots")


def main() -> None:
    s, sons, extras = build_020()
    write_tree(
        "TREE-AUT-020",
        (
            "Amir veut le petit jardin, parce que le chat tapote la vitre. "
            "Le seau reste dans le carré de soleil, le manteau sur la chaise. "
            "Il joue au bac, au toboggan ou aux balançoires. "
            "Il revient prendre le seau, puis un jeu, puis le manteau, "
            "les chaussures ou le sac. Le chat se lèche la patte."
        ),
        "Le chat à la fenêtre d'Amir",
        "Amir, papa, maman",
        "près de la fenêtre, petit jardin",
        s,
        sons,
        extras,
    )
    relecture(
        "TREE-AUT-020",
        "Le chat à la fenêtre d'Amir",
        "Amir veut le jardin vu par le chat. Carré de soleil, seau jaune, "
        "manteau à l'envers. Bac / toboggan / balançoires, puis ballon / "
        "seau / doudou, puis manteau / chaussures / sac. Il reprend le seau.",
        "D16 Amir (plus Sara). N1 ≤10. Leçon implicite AUT.AFF.003. "
        "Labels T3 = manteau/chaussures/sac. Pas Tom/Léa/Sami. "
        "Fin sensorielle (chat, vitre), pas « L'histoire est finie ».",
    )

    s, sons, extras = build_021()
    write_tree(
        "TREE-AUT-021",
        (
            "Mila veut la mer. Un grain de sable brille dans la sangle du sac. "
            "Ça pique. Elle secoue. Elle joue près de l'eau, avec le sac. "
            "Le grain revient un peu, elle le chasse. Banc, cabine ou galets. "
            "Le sac retrouve la chaise de paille. Ça sent encore la pêche."
        ),
        "Le grain de sable dans la sangle",
        "Mila, papa, maman",
        "maison près de la mer, chaise de paille, puis le bord de l'eau",
        s,
        sons,
        extras,
    )
    relecture(
        "TREE-AUT-021",
        "Le grain de sable dans la sangle",
        "Mila veut la mer. Pêche, sandales mouillées, bateau. "
        "Grain dans la sangle : ça pique, le sac glisse, elle secoue. "
        "Bac / toboggan / balançoires, puis ballon / seau / doudou, "
        "puis banc / cabine / galets. Pas une liste de sac.",
        "D16 Mila (plus Lina). N2 <16. Leçon implicite AUT.AFF.001. "
        "Labels T3 = banc/cabine/galets. Pas Tom/Léa/Sami. "
        "Fin = chaise de paille, sangle lisse.",
    )


if __name__ == "__main__":
    main()
