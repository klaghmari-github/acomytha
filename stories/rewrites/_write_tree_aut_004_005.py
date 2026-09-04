#!/usr/bin/env python3
"""F-NAR-008 — TREE-AUT-004 (Nina, caisse) et TREE-AUT-005 (Raphaël, bottes)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, relecture, words, write_story


def preview(sid: str, age: str, scripts: dict) -> None:
    lim = LIMITS.get(age) or 12
    bad: list[str] = []
    n = 0
    for cid, lines in scripts.items():
        for raw in lines:
            phrase = raw.split("|", 1)[1]
            w = words(phrase)
            n += w
            if w > lim:
                bad.append(f"{cid} {w}>{lim}: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                bad.append(f"{cid} multi: {phrase}")
    if bad:
        raise SystemExit(f"{sid} preview:\n" + "\n".join(bad[:40]))
    print(f"preview {sid} {n} mots  chunks={len(scripts)}")


def patch_merged(sid: str, q: dict, relabel: dict[str, tuple[str, str, str]] | None = None) -> None:
    path = ROOT / sid / "merged.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for c in data["chunks"]:
        if c.get("kind") == "passage_question":
            c.update(q)
        if relabel and c.get("option_1_label") in relabel:
            a, b, d = relabel[c["option_1_label"]]
            c["option_1_label"] = a
            c["option_2_label"] = b
            c["option_3_label"] = d
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# TREE-AUT-004 N3 — Nina, petit moulin perdu sous les jouets
# 3 lieux de cachette / 3 façons de ramasser / 3 couleurs de caisse
# ---------------------------------------------------------------------------
Q004 = {
    "expected_answer": "sous les jouets",
    "accepted_examples": (
        "sous les jouets | sous le tas | dessous | dans le tas | sous | "
        "dans la caisse | caisse | le moulin | moulin"
    ),
    "retry_prompt": "Il est sous les jouets. Nina cherche où ?",
}


def story_004() -> dict:
    scripts: dict[str, list[str]] = {}
    scripts["CHK_T0000_P0000"] = [
        "narrateur|Les tilleuls laissent tomber des gouttes.",
        "narrateur|L'écorce sent le bois mouillé.",
        "narrateur|Une coque de châtaigne craque sous un pas.",
        "narrateur|Le banc du square brille, encore humide.",
        "narrateur|Un moineau secoue une aile grise.",
        "narrateur|Papa porte une caisse de bois clair.",
        "narrateur|La poignée de cuir frotte sa paume.",
        "maman|J'ai mis une poire dans le sac.",
        "papa|Elle est encore un peu fraîche.",
        "narrateur|En ce moment, Nina marche entre eux.",
        "narrateur|Ses chaussures font un petit clac.",
        "enfant-f|Mon moulin veut le vent.",
        "maman|Il est dans la caisse, avec les jouets ?",
        "enfant-f|Oui, tout au fond.",
        "papa|Le square est juste là.",
        "narrateur|Une flaque ronde attend près du banc.",
        "narrateur|Le vent bouge déjà une feuille.",
        "enfant-f|Je le sors, pour qu'il tourne.",
        "narrateur|Nina soulève un peu le couvercle.",
        "narrateur|Des cubes, un livre, une tasse.",
        "narrateur|Le moulin n'est pas sur le dessus.",
        "enfant-f|Il est dessous, je crois.",
        "maman|Tu le cherches où ?",
        "papa|Le bac, le toboggan, ou les balançoires.",
    ]
    scripts["CHK_T0001_P0000"] = [
        "narrateur|Nina cherche son moulin où ?",
        "papa|Le bac à sable, le toboggan, ou les balançoires ?",
        "maman|Tu choisis.",
    ]

    l1 = {
        1: [
            "narrateur|Nina s'agenouille près du bac.",
            "narrateur|Le sable est froid, un peu collant.",
            "narrateur|Il coule entre ses doigts.",
            "narrateur|Chh.",
            "narrateur|Papa pose la caisse à côté.",
            "enfant-f|Je sors les jouets.",
            "narrateur|Les cubes tombent dans le sable.",
            "narrateur|Le livre glisse, tout plat.",
            "narrateur|La petite tasse se couche.",
            "enfant-f|Où est mon moulin ?",
            "maman|Sur le banc, peut-être ?",
            "narrateur|Nina va vers le banc mouillé.",
            "narrateur|Le bois est vide, seulement une feuille.",
            "papa|Dans le sac ?",
            "narrateur|Maman ouvre le sac en toile.",
            "narrateur|La poire est là, toute seule.",
            "enfant-f|Il est perdu.",
            "narrateur|Le tas cache tout le milieu du bac.",
            "enfant-f|Je veux voir dessous.",
            "maman|Tu commences par un jouet ?",
        ],
        2: [
            "narrateur|Nina pose la main sur le toboggan.",
            "narrateur|Le métal est frais, un peu lisse.",
            "narrateur|Deux marches sonnent, tout creux.",
            "narrateur|Papa pose la caisse au pied.",
            "enfant-f|Les jouets glissent avec moi.",
            "narrateur|Les cubes dévalent, clic clic.",
            "narrateur|Le livre tape la dernière marche.",
            "narrateur|La tasse roule dans l'herbe.",
            "enfant-f|Mon moulin est parti aussi ?",
            "papa|Sous le toboggan, peut-être ?",
            "narrateur|Nina se penche, tout bas.",
            "narrateur|De l'ombre, pas de pales.",
            "maman|Près du sac ?",
            "narrateur|Le sac tient encore la poire.",
            "enfant-f|Il n'est pas là.",
            "narrateur|Un tas s'est fait en bas.",
            "narrateur|Cubes, livre, tasse, tout mêlé.",
            "enfant-f|Je veux voir sous le tas.",
            "papa|Tu prends un jouet, tout doux ?",
        ],
        3: [
            "narrateur|Nina s'assoit sur une balançoire.",
            "narrateur|La chaîne est froide, un peu rêche.",
            "narrateur|Elle fait un tout petit cri.",
            "narrateur|Papa pose la caisse dans l'herbe.",
            "enfant-f|Les jouets viennent au vent.",
            "narrateur|Les cubes s'éparpillent sous le siège.",
            "narrateur|Le livre s'ouvre sur l'herbe.",
            "narrateur|La tasse se cache dans les brins.",
            "enfant-f|Mon moulin ?",
            "maman|Sous la balançoire ?",
            "narrateur|Nina descend, les pieds à plat.",
            "narrateur|L'herbe est haute, un peu mouillée.",
            "papa|Derrière le sac ?",
            "narrateur|Le sac est fermé, la poire dedans.",
            "enfant-f|Je ne le vois pas.",
            "narrateur|Les jouets font un petit mont.",
            "enfant-f|Il est sous le mont, je crois.",
            "maman|Tu ramasses par quoi ?",
        ],
    }
    q_l1 = {
        1: [
            "narrateur|Nina cherche son moulin.",
            "narrateur|Il est où ?",
        ],
        2: [
            "narrateur|Le tas est au pied du toboggan.",
            "narrateur|Le moulin est où ?",
        ],
        3: [
            "narrateur|L'herbe cache les jouets.",
            "narrateur|Le moulin est où ?",
        ],
    }
    c_l1 = {
        1: [
            "narrateur|Nina prend un cube du tas.",
            "narrateur|Elle le glisse dans la caisse.",
            "narrateur|Toc.",
            "narrateur|Un rond de sable reparaît.",
            "enfant-f|Pas encore le moulin.",
            "maman|Tu regardes bien dessous ?",
            "enfant-f|Oui, maman.",
            "papa|Il reste des jouets, tout autour.",
            "narrateur|Le tas est encore haut.",
            "enfant-f|Je continue.",
            "maman|Quel jouet, maintenant ?",
        ],
        2: [
            "narrateur|Nina ramasse un cube au pied.",
            "narrateur|Elle le pose dans la caisse.",
            "narrateur|Toc.",
            "narrateur|Une marche grise reparaît.",
            "enfant-f|Toujours pas.",
            "papa|Tu regardes sous le tas ?",
            "enfant-f|Oui, papa.",
            "maman|D'autres jouets attendent encore.",
            "narrateur|Le métal sonne un peu vide.",
            "enfant-f|Je prends encore.",
            "papa|Lequel, d'abord ?",
        ],
        3: [
            "narrateur|Nina prend un cube dans l'herbe.",
            "narrateur|Elle le met dans la caisse.",
            "narrateur|Toc.",
            "narrateur|Un brin d'herbe se redresse.",
            "enfant-f|Ce n'est pas lui.",
            "maman|Tu regardes sous le mont ?",
            "enfant-f|Oui.",
            "papa|Il reste le livre, et la tasse.",
            "narrateur|La chaîne ne crie plus.",
            "enfant-f|Je ramasse encore.",
            "maman|Tu prends quoi, dans l'herbe ?",
        ],
    }
    t2q = {
        1: [
            "narrateur|Nina ramasse quoi, près du bac ?",
            "maman|Les cubes, le livre, ou la dînette ?",
        ],
        2: [
            "narrateur|Nina ramasse quoi, au pied ?",
            "papa|Les cubes, le livre, ou la dînette ?",
        ],
        3: [
            "narrateur|Nina ramasse quoi, dans l'herbe ?",
            "maman|Les cubes, le livre, ou la dînette ?",
        ],
    }

    l2 = {
        (1, 1): [
            "narrateur|Les cubes sont sablés, un peu rudes.",
            "enfant-f|Un par un, dans la caisse.",
            "narrateur|Nina empile deux cubes, puis s'arrête.",
            "narrateur|Clic.",
            "narrateur|Elle glisse le premier dans la caisse.",
            "narrateur|Toc.",
            "narrateur|Le second suit, tout sablé.",
            "papa|Tu vois le sable, maintenant ?",
            "enfant-f|Un peu, papa.",
            "maman|Les pales, pas encore ?",
            "enfant-f|Non.",
            "narrateur|Un troisième cube reste au milieu.",
            "narrateur|Nina le soulève, tout doux.",
            "narrateur|Rien que du sable froid.",
            "enfant-f|Il est plus bas.",
            "papa|La caisse peut encore s'ouvrir.",
        ],
        (1, 2): [
            "narrateur|Le livre a du sable sur la couverture.",
            "enfant-f|Je l'essuie un peu.",
            "narrateur|Nina passe la main, tout plat.",
            "narrateur|Des grains tombent, chh.",
            "maman|Tu le mets où ?",
            "enfant-f|Dans la caisse.",
            "narrateur|Elle ferme le livre.",
            "narrateur|Une image de lune reste un instant.",
            "narrateur|Le livre glisse dans la caisse.",
            "narrateur|Toc, tout sourd.",
            "papa|Le bac est plus vide ?",
            "enfant-f|Un coin, oui.",
            "narrateur|Sous le livre, du sable plat.",
            "enfant-f|Pas de pales.",
            "maman|D'autres choses restent encore.",
        ],
        (1, 3): [
            "narrateur|La tasse est froide, posée de travers.",
            "narrateur|Une soucoupe est à côté, sablée.",
            "enfant-f|La dînette, tout doux.",
            "narrateur|Nina pose la tasse sur la soucoupe.",
            "narrateur|Ça cliquette.",
            "papa|Tu les mets dans la caisse ?",
            "enfant-f|Oui, la tasse d'abord.",
            "narrateur|Toc.",
            "narrateur|La soucoupe suit, un peu de sable.",
            "maman|Tu as regardé dessous ?",
            "enfant-f|Sous la tasse, rien.",
            "narrateur|Un rond de bac reparaît.",
            "enfant-f|Le moulin est plus loin.",
            "papa|La caisse n'est pas pleine.",
        ],
        (2, 1): [
            "narrateur|Les cubes attendent au pied du métal.",
            "enfant-f|Ils ont glissé, les uns sur les autres.",
            "narrateur|Nina les sépare, un par un.",
            "narrateur|Clic.",
            "narrateur|Un cube va dans la caisse.",
            "narrateur|Toc.",
            "papa|La marche reparaît ?",
            "enfant-f|La dernière, un peu.",
            "maman|Les pales ?",
            "enfant-f|Pas encore.",
            "narrateur|Deux cubes restent coincés ensemble.",
            "narrateur|Nina les décroche, tout calme.",
            "narrateur|Elle les pose dans la caisse.",
            "enfant-f|Il est sous le reste.",
            "papa|On garde la caisse ouverte.",
        ],
        (2, 2): [
            "narrateur|Le livre est contre la dernière marche.",
            "narrateur|Une page a un peu d'herbe.",
            "enfant-f|Je ferme, puis la caisse.",
            "narrateur|Nina chasse la feuille du bout des doigts.",
            "narrateur|Elle referme le livre.",
            "maman|Il rentre ?",
            "enfant-f|Oui, tout plat.",
            "narrateur|Le livre glisse dans la caisse.",
            "narrateur|Toc.",
            "papa|Sous le livre, tu vois ?",
            "enfant-f|L'herbe, et l'ombre.",
            "narrateur|Pas de bois, pas de pales.",
            "enfant-f|Il est encore dessous.",
            "maman|D'autres jouets ont glissé aussi.",
        ],
        (2, 3): [
            "narrateur|La tasse a roulé dans l'herbe basse.",
            "narrateur|La soucoupe est plus loin, un peu tordue.",
            "enfant-f|Je les rattrape.",
            "narrateur|Nina pose la tasse dans la soucoupe.",
            "narrateur|Ça cliquette, tout fin.",
            "papa|Dans la caisse, les deux ?",
            "enfant-f|Oui, papa.",
            "narrateur|Toc.",
            "narrateur|Toc encore.",
            "maman|Tu as regardé sous la tasse ?",
            "enfant-f|De l'herbe mouillée.",
            "narrateur|Le pied du toboggan est plus net.",
            "enfant-f|Le moulin n'est pas là.",
            "papa|Il reste un fond, dans le tas.",
        ],
        (3, 1): [
            "narrateur|Les cubes sont dans l'herbe, sous le siège.",
            "enfant-f|Je les prends, un par un.",
            "narrateur|Nina cherche avec les doigts.",
            "narrateur|Un cube, puis un autre.",
            "narrateur|Clic, contre le bois de la caisse.",
            "papa|L'herbe se redresse ?",
            "enfant-f|Un peu, papa.",
            "maman|Les pales, dans les brins ?",
            "enfant-f|Je ne les vois pas.",
            "narrateur|Un cube reste coincé contre un pied.",
            "narrateur|Nina le dégage, tout doux.",
            "narrateur|Elle le met dans la caisse.",
            "enfant-f|Encore dessous.",
            "papa|La caisse attend le reste.",
        ],
        (3, 2): [
            "narrateur|Le livre est ouvert sur l'herbe.",
            "narrateur|Une page boit une goutte.",
            "enfant-f|Je le sèche un peu.",
            "narrateur|Nina souffle sur la page.",
            "narrateur|Ffff.",
            "maman|Tu le fermes ?",
            "enfant-f|Oui, puis la caisse.",
            "narrateur|Le livre rentre, tout plat.",
            "narrateur|Toc.",
            "papa|Sous le livre ?",
            "enfant-f|Des brins, pas de bois.",
            "narrateur|La chaîne bouge un tout petit peu.",
            "enfant-f|Il est plus bas, dans l'herbe.",
            "maman|D'autres jouets sont encore là.",
        ],
        (3, 3): [
            "narrateur|La tasse s'est cachée dans les brins.",
            "narrateur|La soucoupe est froide, un peu verte.",
            "enfant-f|La dînette, je la sors de l'herbe.",
            "narrateur|Nina pose la tasse, ça cliquette.",
            "papa|Dans la caisse ?",
            "enfant-f|Oui, les deux.",
            "narrateur|Toc.",
            "narrateur|Un trou d'herbe reste, tout rond.",
            "maman|Tu as regardé dans le trou ?",
            "enfant-f|Pas de pales.",
            "narrateur|Le siège de la balançoire est vide.",
            "enfant-f|Le moulin est encore dessous.",
            "papa|Il reste un fond, tout près.",
        ],
    }

    t3q = [
        "narrateur|Nina prend quelle caisse ?",
        "papa|Rouge, bleu, ou vert ?",
        "maman|Tu choisis la couleur.",
    ]

    hide = {
        (1, 1): "narrateur|Sous le dernier cube, un bout de bois.",
        (1, 2): "narrateur|Sous le livre, les pales sont plates.",
        (1, 3): "narrateur|Sous la tasse, le moulin est sablé.",
        (2, 1): "narrateur|Sous les cubes du pied, le bois.",
        (2, 2): "narrateur|Entre la marche et le livre, les pales.",
        (2, 3): "narrateur|Dans l'herbe de la tasse, le moulin.",
        (3, 1): "narrateur|Sous le cube de l'herbe, le bois.",
        (3, 2): "narrateur|Sous le livre mouillé, les pales.",
        (3, 3): "narrateur|Sous la soucoupe, le petit moulin.",
    }
    place_bit = {
        1: "narrateur|Le bac redevient un rond de sable.",
        2: "narrateur|Le toboggan sonne, tout vide.",
        3: "narrateur|La chaîne de la balançoire se tait.",
    }
    toy_put = {
        1: ("narrateur|Nina glisse le dernier cube.", "enfant-f|Clic, puis toc."),
        2: ("narrateur|Nina glisse le livre, tout plat.", "enfant-f|Toc, tout sourd."),
        3: ("narrateur|Nina glisse la dernière tasse.", "enfant-f|Ça cliquette, puis toc."),
    }
    color_open = {
        1: "narrateur|Le couvercle rouge attend, un peu luisant.",
        2: "narrateur|Une caisse bleue est là, près du pied.",
        3: "narrateur|Papa tend la caisse verte, ouverte.",
    }
    color_see = {
        1: "narrateur|Une feuille rouge colle près du pied.",
        2: "narrateur|Un galet bleu brille dans la flaque.",
        3: "narrateur|Une feuille verte tremble au bord.",
    }
    color_lid = {
        1: "narrateur|Elle pousse le couvercle rouge.",
        2: "narrateur|Elle pousse le couvercle bleu.",
        3: "narrateur|Elle pousse le couvercle vert.",
    }
    spin = {
        1: "narrateur|Les pales prennent le vent, contre le rouge.",
        2: "narrateur|Les pales tournent, au-dessus du bleu.",
        3: "narrateur|Les pales tournent, tout contre le vert.",
    }

    def l3(t1: int, t2: int, t3: int) -> list[str]:
        a, b = toy_put[t2]
        return [
            color_open[t3],
            color_see[t3],
            place_bit[t1],
            a,
            b,
            hide[(t1, t2)],
            "enfant-f|Mon moulin !",
            "narrateur|Nina le soulève, tout doux.",
            "narrateur|Le bois sent encore le square.",
            "maman|Te voilà, petit.",
            "papa|Merci, tu l'as trouvé.",
            "enfant-f|Il était dessous.",
            color_lid[t3],
            "narrateur|Toc.",
            "enfant-f|Tourne.",
            spin[t3],
        ]

    fin_walk = {
        1: "narrateur|Ils quittent le bac, tout calme.",
        2: "narrateur|Ils quittent le toboggan, tout calme.",
        3: "narrateur|Ils quittent les balançoires, tout calme.",
    }
    fin_obj = {
        1: "narrateur|Les cubes dorment dans la caisse.",
        2: "narrateur|Le livre dort dans la caisse.",
        3: "narrateur|La tasse dort dans la caisse.",
    }
    fin_col = {
        1: "narrateur|Le couvercle rouge reste fermé.",
        2: "narrateur|Le couvercle bleu reste fermé.",
        3: "narrateur|Le couvercle vert reste fermé.",
    }
    fin_img = {
        (1, 1, 1): "narrateur|Le moineau reprend une miette, plus loin.",
        (1, 1, 2): "narrateur|La flaque tremble, toute ronde.",
        (1, 1, 3): "narrateur|Une goutte tombe d'un tilleul.",
        (1, 2, 1): "narrateur|Le banc sèche par petites plaques.",
        (1, 2, 2): "narrateur|Le sac tape le dos, toc toc.",
        (1, 2, 3): "narrateur|La poire roule un peu, dans le sac.",
        (1, 3, 1): "narrateur|Le sable ne coule plus.",
        (1, 3, 2): "narrateur|Un vélo sonne, tout loin.",
        (1, 3, 3): "narrateur|L'école montre son portail, tout loin.",
        (2, 1, 1): "narrateur|Le métal du toboggan sèche.",
        (2, 1, 2): "narrateur|Une voiture passe, tout bas.",
        (2, 1, 3): "narrateur|Les marches restent vides, grises.",
        (2, 2, 1): "narrateur|Une page ne boit plus de goutte.",
        (2, 2, 2): "narrateur|Le trottoir sèche par plaques.",
        (2, 2, 3): "narrateur|Le vent pousse une feuille verte.",
        (2, 3, 1): "narrateur|La tasse ne cliquette plus.",
        (2, 3, 2): "narrateur|Le square reste derrière, calme.",
        (2, 3, 3): "narrateur|Les chaussures font clac, à nouveau.",
        (3, 1, 1): "narrateur|La chaîne ne crie plus du tout.",
        (3, 1, 2): "narrateur|L'herbe se redresse, brin par brin.",
        (3, 1, 3): "narrateur|Papa et maman marchent au même pas.",
        (3, 2, 1): "narrateur|Le zip du sac est fermé.",
        (3, 2, 2): "narrateur|Nina a les mains propres, maintenant.",
        (3, 2, 3): "narrateur|L'école sent déjà le savon, tout loin.",
        (3, 3, 1): "narrateur|Une miette reste sur le banc.",
        (3, 3, 2): "narrateur|Le vent est doux, dans les cheveux.",
        (3, 3, 3): "narrateur|Le vent tourne encore les pales.",
    }
    fin_spin = {
        1: "narrateur|Le moulin tourne contre le rouge.",
        2: "narrateur|Le moulin tourne contre le bleu.",
        3: "narrateur|Le moulin tourne contre le vert.",
    }

    def fin(t1: int, t2: int, t3: int) -> list[str]:
        lines = [
            fin_walk[t1],
            fin_obj[t2],
            fin_col[t3],
            "enfant-f|Il a du vent, maintenant.",
            "maman|Tu l'as vu dessous.",
            "papa|Bravo, tu l'as retrouvé.",
            fin_spin[t3],
            "narrateur|La poire sent encore, dans le sac.",
            fin_img[(t1, t2, t3)],
        ]
        if (t1, t2, t3) == (3, 3, 3):
            lines[-1] = "narrateur|Le vent tourne encore les pales."
        return lines

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        scripts[p] = l1[t1]
        scripts[f"{p}_Q0001"] = q_l1[t1]
        scripts[f"{p}_C0001"] = c_l1[t1]
        scripts[f"{p}_T0002_P0000"] = t2q[t1]
        for t2 in (1, 2, 3):
            scripts[f"{p}_T0002_P000{t2}"] = l2[(t1, t2)]
            scripts[f"{p}_T0002_P000{t2}_T0003_P0000"] = t3q
            for t3 in (1, 2, 3):
                scripts[f"{p}_T0002_P000{t2}_T0003_P000{t3}"] = l3(t1, t2, t3)
                scripts[f"{p}_T0002_P000{t2}_T0003_P000{t3}_F0001"] = fin(t1, t2, t3)
    return scripts


# ---------------------------------------------------------------------------
# TREE-AUT-005 N1 — Raphaël, coq, bottes puis chemin (pas une liste d'étapes)
# ---------------------------------------------------------------------------
Q005 = {
    "expected_answer": "les bottes",
    "accepted_examples": "les bottes | bottes | ses bottes | les bottes d'abord | mettre les bottes",
    "retry_prompt": "Il met les bottes. Raphaël met quoi ?",
}


def story_005() -> dict:
    scripts: dict[str, list[str]] = {}
    scripts["CHK_T0000_P0000"] = [
        "narrateur|La paille craque sous le volet.",
        "narrateur|Un volet bleu bouge tout doux.",
        "narrateur|Ça sent le foin chaud.",
        "narrateur|Le lait fume dans le bol.",
        "maman|Le lait est prêt, Raphaël.",
        "papa|Tu as entendu le coq ?",
        "enfant-m|Oui, papa.",
        "narrateur|Le coq chante derrière la grange.",
        "narrateur|L'herbe brille, encore mouillée.",
        "narrateur|Les bottes attendent près de la porte.",
        "narrateur|Une paille dépasse d'une botte.",
        "narrateur|En ce moment, Raphaël se lève.",
        "narrateur|Le plancher est froid sous ses pieds.",
        "enfant-m|Je veux voir le coq.",
        "maman|Le chemin est mouillé.",
        "papa|Tes pieds sont déjà froids ?",
        "enfant-m|Un peu.",
        "narrateur|Raphaël va vers la porte.",
        "narrateur|La pierre du seuil est froide.",
        "enfant-m|Je prends quelque chose.",
        "papa|Quoi, pour le chemin ?",
    ]
    scripts["CHK_T0001_P0000"] = [
        "narrateur|Qu'est-ce que Raphaël prend ?",
        "maman|Le ballon rouge, le seau bleu, ou le doudou.",
    ]

    l1 = {
        1: [
            "narrateur|Raphaël prend le ballon rouge.",
            "narrateur|Le ballon est lisse, un peu tiède.",
            "enfant-m|Il vient avec moi.",
            "narrateur|Il marche vers la porte.",
            "narrateur|Le ballon tape le bois.",
            "narrateur|Toc.",
            "narrateur|La porte s'ouvre un peu.",
            "narrateur|L'air sent l'herbe mouillée.",
            "narrateur|Le ballon glisse sur la pierre.",
            "narrateur|Il roule vers le chemin.",
            "enfant-m|Attends !",
            "narrateur|Raphaël avance un pied.",
            "narrateur|Le chausson touche l'eau.",
            "narrateur|L'eau est froide, toute fine.",
            "enfant-m|Aïe, c'est froid.",
            "papa|Tes pieds n'aiment pas ça.",
            "maman|Les bottes sont là, près de toi.",
            "narrateur|Les bottes attendent, bouche ouverte.",
            "enfant-m|Le ballon est dehors.",
            "papa|On le reprend avec les bottes ?",
        ],
        2: [
            "narrateur|Raphaël prend le seau bleu.",
            "narrateur|Le seau fait un petit bruit de fer.",
            "enfant-m|Il y a du grain, pour le coq.",
            "maman|Un peu, tout au fond.",
            "narrateur|Il marche vers la porte.",
            "narrateur|Le seau tape sa jambe.",
            "narrateur|La porte s'ouvre.",
            "narrateur|L'air sent le fumier doux.",
            "narrateur|Raphaël pose un pied dehors.",
            "narrateur|Le chausson glisse sur la pierre.",
            "narrateur|Le seau penche.",
            "narrateur|Deux grains tombent.",
            "enfant-m|Oh.",
            "papa|La pierre est mouillée.",
            "maman|Tes pieds sont tout froids.",
            "enfant-m|Je veux le chemin.",
            "papa|Les bottes tiennent mieux, sur l'eau.",
            "narrateur|Les bottes sont là, près du seau.",
            "enfant-m|Je les mets ?",
            "maman|Tu les mets, pour le chemin ?",
        ],
        3: [
            "narrateur|Raphaël prend le doudou.",
            "narrateur|Le doudou est doux contre sa joue.",
            "enfant-m|Il veut voir le coq aussi.",
            "maman|Il vient, tout contre toi.",
            "narrateur|Raphaël va vers la porte.",
            "narrateur|Le doudou frotte le bois.",
            "narrateur|La porte s'ouvre.",
            "narrateur|Un filet d'air froid entre.",
            "narrateur|Raphaël pose un orteil dehors.",
            "narrateur|La pierre pique, toute froide.",
            "enfant-m|Aïe.",
            "papa|Le chemin n'aime pas les orteils.",
            "maman|Les bottes sont près du sac.",
            "narrateur|Une paille dépasse encore.",
            "enfant-m|Le doudou a froid aussi.",
            "papa|Toi d'abord, les pieds au chaud.",
            "narrateur|Raphaël serre le doudou.",
            "enfant-m|Je mets les bottes ?",
            "maman|Tu mets les bottes, pour le chemin ?",
        ],
    }
    q_l1 = {
        1: [
            "narrateur|Le ballon est sur le chemin.",
            "narrateur|Raphaël met quoi ?",
        ],
        2: [
            "narrateur|Le seau penche, dehors.",
            "narrateur|Raphaël met quoi ?",
        ],
        3: [
            "narrateur|La pierre est froide.",
            "narrateur|Raphaël met quoi ?",
        ],
    }
    c_l1 = {
        1: [
            "narrateur|Raphaël prend la botte gauche.",
            "narrateur|Il pousse le pied dedans.",
            "narrateur|Le caoutchouc est un peu froid.",
            "narrateur|Puis la botte droite.",
            "narrateur|Les deux pieds sont au chaud.",
            "enfant-m|C'est mieux.",
            "maman|Tu es prêt pour le chemin ?",
            "enfant-m|Oui, maman.",
            "papa|Le ballon t'attend, là-bas.",
            "narrateur|Raphaël marche sur la pierre.",
            "narrateur|L'eau ne passe plus.",
            "enfant-m|On va voir qui ?",
        ],
        2: [
            "narrateur|Raphaël pose le seau un instant.",
            "narrateur|Il prend la botte gauche.",
            "narrateur|Le pied glisse dedans, tout doux.",
            "narrateur|Puis la botte droite.",
            "narrateur|Les pieds sont au chaud.",
            "enfant-m|Le seau, maintenant.",
            "papa|Il tient droit, cette fois ?",
            "enfant-m|Oui, papa.",
            "maman|Tu marches sur la pierre ?",
            "narrateur|Raphaël avance, le seau stable.",
            "narrateur|L'eau reste sous les bottes.",
            "enfant-m|On va voir qui ?",
        ],
        3: [
            "narrateur|Raphaël pose le doudou sur le banc.",
            "narrateur|Il prend la botte gauche.",
            "narrateur|Le pied entre, tout au fond.",
            "narrateur|Puis la botte droite.",
            "maman|Les pieds sont au chaud ?",
            "enfant-m|Oui, maman.",
            "narrateur|Il reprend le doudou.",
            "papa|Tu marches sur la pierre ?",
            "narrateur|Raphaël avance, tout calme.",
            "narrateur|La pierre ne pique plus.",
            "enfant-m|Le doudou vient.",
            "maman|On va voir qui ?",
        ],
    }
    t2q = [
        "narrateur|On va voir qui ?",
        "papa|Le chat, le chien, ou la poule.",
    ]

    obj_hold = {
        1: "narrateur|Son ballon rouge tape sa jambe, tout doux.",
        2: "narrateur|Son seau bleu tient droit, dans sa main.",
        3: "narrateur|Son doudou reste contre sa joue.",
    }

    l2 = {
        1: [
            "narrateur|Dans la paille, le chat dort.",
            "narrateur|Raphaël marche vers lui.",
            "narrateur|Les bottes font un petit bruit.",
            "narrateur|Floc, sur le chemin.",
            "enfant-m|Bonjour, chat.",
            "narrateur|Le poil est chaud, tout doux.",
            "narrateur|Le chat ronronne.",
            "papa|Tu as les pieds au chaud ?",
            "enfant-m|Oui, papa.",
            "maman|Le chat aime la paille sèche.",
            "narrateur|Une paille colle à une botte.",
            "enfant-m|Le coq est plus loin.",
            "papa|On continue, sur le chemin ?",
        ],
        2: [
            "narrateur|Près de l'étable, le chien attend.",
            "narrateur|Raphaël marche vers lui.",
            "narrateur|Les bottes tiennent sur la boue.",
            "narrateur|Floc.",
            "enfant-m|Bonjour, chien.",
            "narrateur|Le chien remue la queue.",
            "narrateur|Wouaf, tout doux.",
            "maman|Tu as les pieds au chaud ?",
            "enfant-m|Oui, maman.",
            "papa|Le chien a les pattes mouillées.",
            "narrateur|Raphaël reste sur le chemin.",
            "enfant-m|Le coq est plus loin.",
            "papa|On continue, avec les bottes ?",
        ],
        3: [
            "narrateur|Dans la cour, la poule picore.",
            "narrateur|Raphaël marche vers elle.",
            "narrateur|Les bottes font toc, sur les cailloux.",
            "enfant-m|Bonjour, poule.",
            "narrateur|La poule fait cot-cot.",
            "narrateur|Cot-cot.",
            "papa|Tu as les pieds au chaud ?",
            "enfant-m|Oui, papa.",
            "maman|La poule a les plumes sèches.",
            "narrateur|Un caillou sonne sous une botte.",
            "enfant-m|Le coq est plus loin.",
            "maman|On continue, sur le chemin ?",
        ],
    }

    t3q = [
        "narrateur|C'est quel moment ?",
        "maman|Le matin, après la sieste, ou le soir.",
    ]

    time_air = {
        1: [
            "narrateur|Le soleil est bas, tout pâle.",
            "narrateur|La rosée brille sur l'herbe.",
            "narrateur|Le coq chante fort, derrière.",
        ],
        2: [
            "narrateur|La maison est calme, tout tiède.",
            "narrateur|La paille sent le soleil.",
            "narrateur|Le coq fait un petit cri.",
        ],
        3: [
            "narrateur|Une lampe est allumée, tout bas.",
            "narrateur|L'air devient un peu bleu.",
            "narrateur|Le coq se tait, sur son perchoir.",
        ],
    }
    time_do = {
        1: {
            1: "narrateur|Raphaël pose le ballon près du coq.",
            2: "narrateur|Raphaël verse un peu de grain.",
            3: "narrateur|Raphaël montre le doudou au coq.",
        },
        2: {
            1: "narrateur|Raphaël pose le ballon dans l'herbe tiède.",
            2: "narrateur|Raphaël pose le seau, tout calme.",
            3: "narrateur|Raphaël assied le doudou dans la paille.",
        },
        3: {
            1: "narrateur|Raphaël tient le ballon, sans le jeter.",
            2: "narrateur|Raphaël pose le seau près de la porte.",
            3: "narrateur|Raphaël serre le doudou, tout contre.",
        },
    }
    animal_bit = {
        1: "narrateur|Un chat se frotte contre une botte.",
        2: "narrateur|Un chien s'assoit près des bottes.",
        3: "narrateur|Une poule picore près des bottes.",
    }
    animal_say = {
        1: "enfant-m|Il ronronne.",
        2: "enfant-m|Il fait wouaf.",
        3: "enfant-m|Elle fait cot-cot.",
    }

    def l3(t1: int, t2: int, t3: int) -> list[str]:
        return [
            *time_air[t3],
            obj_hold[t1],
            animal_bit[t2],
            time_do[t3][t1],
            "narrateur|Le chemin tient sous les bottes.",
            "papa|Tes pieds sont bien ?",
            "enfant-m|Au chaud.",
            animal_say[t2],
            "maman|Le coq t'a vu.",
            "enfant-m|Moi aussi.",
            "papa|Merci, tu as mis les bottes.",
            "narrateur|Une paille reste sur une botte.",
        ]

    fin_time = {
        1: "narrateur|Le lait sent encore, dans la maison.",
        2: "narrateur|La paille reste tiède, tout calme.",
        3: "narrateur|La lampe fait un rond jaune.",
    }
    fin_obj = {
        1: "narrateur|Le ballon rouge est un peu humide.",
        2: "narrateur|Le seau bleu a encore deux grains.",
        3: "narrateur|Le doudou sent le foin, maintenant.",
    }
    fin_ani = {
        1: "narrateur|Le chat se recouche dans la paille.",
        2: "narrateur|Le chien remue encore la queue.",
        3: "narrateur|La poule picore un dernier grain.",
    }
    fin_img = {
        (1, 1, 1): "narrateur|Le coq chante encore, tout près.",
        (1, 1, 2): "narrateur|Une mouche tourne au-dessus du foin.",
        (1, 1, 3): "narrateur|Le perchoir craque, tout doux.",
        (1, 2, 1): "narrateur|L'étable sent le bois mouillé.",
        (1, 2, 2): "narrateur|La queue du chien fait de l'ombre.",
        (1, 2, 3): "narrateur|Un volet bleu se ferme un peu.",
        (1, 3, 1): "narrateur|Un caillou brille sous la rosée.",
        (1, 3, 2): "narrateur|La cour est chaude, tout calme.",
        (1, 3, 3): "narrateur|Les plumes de la poule sont sombres.",
        (2, 1, 1): "narrateur|Deux grains restent dans l'herbe.",
        (2, 1, 2): "narrateur|Le seau fait un petit bruit de fer.",
        (2, 1, 3): "narrateur|La porte de la grange reste ouverte.",
        (2, 2, 1): "narrateur|La boue tient sous les semelles.",
        (2, 2, 2): "narrateur|L'étable est calme, tout tiède.",
        (2, 2, 3): "narrateur|Le chien bâille, tout près.",
        (2, 3, 1): "narrateur|Le grain sent encore le sac.",
        (2, 3, 2): "narrateur|Une poule gratte, plus loin.",
        (2, 3, 3): "narrateur|Le fer du seau est froid, le soir.",
        (3, 1, 1): "narrateur|Le doudou a une paille sur l'oreille.",
        (3, 1, 2): "narrateur|Le chat ferme un œil, puis l'autre.",
        (3, 1, 3): "narrateur|Le poil du chat est tiède encore.",
        (3, 2, 1): "narrateur|Le doudou a vu le chien.",
        (3, 2, 2): "narrateur|Les pattes du chien sèchent.",
        (3, 2, 3): "narrateur|L'étable devient toute douce.",
        (3, 3, 1): "narrateur|Le doudou a vu la poule.",
        (3, 3, 2): "narrateur|Un cot-cot part, tout loin.",
        (3, 3, 3): "narrateur|La paille sent encore le soir.",
    }

    def fin(t1: int, t2: int, t3: int) -> list[str]:
        return [
            fin_time[t3],
            fin_obj[t1],
            fin_ani[t2],
            "enfant-m|Mes bottes sont un peu sales.",
            "maman|Elles ont fait le chemin.",
            "papa|Bravo, tes pieds sont restés au chaud.",
            "narrateur|Voilà le coq, de l'autre côté.",
            fin_img[(t1, t2, t3)],
        ]

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        scripts[p] = l1[t1]
        scripts[f"{p}_Q0001"] = q_l1[t1]
        scripts[f"{p}_C0001"] = c_l1[t1]
        scripts[f"{p}_T0002_P0000"] = list(t2q)
        for t2 in (1, 2, 3):
            head = [obj_hold[t1]]
            # avoid 4x same start: obj_hold starts with Le/Le/Le — mix by t1
            body = l2[t2]
            scripts[f"{p}_T0002_P000{t2}"] = head + body
            scripts[f"{p}_T0002_P000{t2}_T0003_P0000"] = list(t3q)
            for t3 in (1, 2, 3):
                scripts[f"{p}_T0002_P000{t2}_T0003_P000{t3}"] = l3(t1, t2, t3)
                scripts[f"{p}_T0002_P000{t2}_T0003_P000{t3}_F0001"] = fin(t1, t2, t3)
    return scripts


def main() -> None:
    s004 = story_004()
    preview("TREE-AUT-004", "N3", s004)
    write_story(
        "TREE-AUT-004",
        "Nina veut faire tourner son petit moulin au square. "
        "Le moulin disparaît sous les jouets, au bac, au toboggan ou sous les balançoires. "
        "Elle le retrouve seulement quand cubes, livre ou dînette vont dans la caisse. "
        "Le vent fait tourner les pales.",
        "Le petit moulin de Nina",
        "Nina, papa, maman",
        "rue des tilleuls après la pluie, square, caisse de bois, chemin de l'école",
        s004,
        {},
    )
    patch_merged("TREE-AUT-004", Q004)
    relecture(
        "TREE-AUT-004",
        "Le petit moulin de Nina",
        "Nina veut le vent pour son moulin. Jouets sortis au square, moulin perdu. "
        "Banc, sac, poire : pas lui. Cubes / livre / dînette dans la caisse. "
        "Dessous, les pales. Le moulin tourne. Ils reprennent le chemin.",
        "Inès/Mila → Nina. Pas « on va ranger » ni « après le jeu ». "
        "T1 = 3 cachettes (bac, toboggan, balançoires). "
        "T2 = 3 façons de ramasser (cubes, livre, dînette). "
        "T3 = 3 couleurs de caisse. Question = où est le moulin. "
        "Graphe 86 chunks. Audio non cuit.",
    )

    s005 = story_005()
    preview("TREE-AUT-005", "N1", s005)
    write_story(
        "TREE-AUT-005",
        "Raphaël veut voir le coq sur le chemin mouillé. "
        "Il prend le ballon, le seau ou le doudou. La pierre est froide. "
        "Il met les bottes, puis il marche. Le chat, le chien ou la poule l'attendent. "
        "Le coq est de l'autre côté.",
        "Le coq et les bottes de Raphaël",
        "Raphaël, papa, maman",
        "ferme, volet bleu, paille, grange, chemin de terre mouillé",
        s005,
        {},
    )
    patch_merged(
        "TREE-AUT-005",
        Q005,
        relabel={"Tom": ("le chat", "le chien", "la poule")},
    )
    relecture(
        "TREE-AUT-005",
        "Le coq et les bottes de Raphaël",
        "Raphaël veut le coq. Objet à la main, pierre froide, chausson mouillé. "
        "Bottes gauche puis droite. Chemin. Chat / chien / poule. "
        "Matin, sieste ou soir. Coq de l'autre côté. Pieds au chaud.",
        "Léa/Tom/Sami hors troupe. Pas « une étape après l'autre ». "
        "Séquence vécue : bottes puis chemin. N1 ≤10 mots. "
        "T2 libellés → chat, chien, poule. Graphe 86. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
