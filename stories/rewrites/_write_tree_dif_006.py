#!/usr/bin/env python3
"""TREE-DIF-006 — Les gouttes de l'arrosoir. Raphaël, jardin, N2. DIF.ENE.001 implicite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-006"
N2 = LIMITS["N2"]


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
    return list(rows)


def t3opts(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


FLEUR = {
    1: {
        "lab": "la jaune",
        "nom": "la marguerite",
        "ou": "près du bac",
        "can": "l'arrosoir jaune",
        "tete": "La tête jaune",
        "sol": "la dalle",
        "lieu": "le bac",
        "insecte": "une abeille",
        "couleur": "jaune",
    },
    2: {
        "lab": "la rouge",
        "nom": "le coquelicot",
        "ou": "près des tomates",
        "can": "l'arrosoir rouge",
        "tete": "La tête rouge",
        "sol": "la terre",
        "lieu": "les tomates",
        "insecte": "une coccinelle",
        "couleur": "rouge",
    },
    3: {
        "lab": "la bleue",
        "nom": "la fleur bleue",
        "ou": "près du banc",
        "can": "l'arrosoir bleu",
        "tete": "La tête bleue",
        "sol": "le banc",
        "lieu": "le banc",
        "insecte": "un papillon",
        "couleur": "bleue",
    },
}

EAU = {
    1: {"lab": "le robinet", "de": "du robinet"},
    2: {"lab": "le seau", "de": "du seau"},
    3: {"lab": "l'arrosoir", "de": "de l'arrosoir de maman"},
}

FIN_AIR = {
    (1, 1): "Le bac garde un rond d'ombre.",
    (1, 2): "La petite tasse se tait.",
    (1, 3): "Papa s'essuie les mains sur le linge rose.",
    (2, 1): "Une tomate encore chaude brille à côté.",
    (2, 2): "La terre a un petit sourire mouillé.",
    (2, 3): "Les plants de tomates ne bougent plus.",
    (3, 1): "Une perle d'eau reste dans l'ombre.",
    (3, 2): "Le bois sent encore la pluie d'hier.",
    (3, 3): "L'ombre du banc a reculé d'un pas.",
}

FIN_IMG = {
    (1, 1, 1): "Un grain de sable sèche sur le pétale jaune.",
    (1, 1, 2): "La tasse garde un rond de soleil.",
    (1, 1, 3): "L'ombre de papa reste un moment sur le bac.",
    (1, 2, 1): "Le seau a un fond de sable, tout calme.",
    (1, 2, 2): "Une miette de sable brille dans la tasse.",
    (1, 2, 3): "Les orteils de Raphaël ont séché.",
    (1, 3, 1): "L'abeille est revenue, tout près.",
    (1, 3, 2): "La dernière goutte de maman a voyagé.",
    (1, 3, 3): "Le bec de l'arrosoir ne gicle plus.",
    (2, 1, 1): "Une coccinelle s'est posée sur le bouton rouge.",
    (2, 1, 2): "Une tomate a une goutte, pour de rire.",
    (2, 1, 3): "Le filet du robinet s'est tu.",
    (2, 2, 1): "La terre a cessé de faire des bulles.",
    (2, 2, 2): "La tasse a une auréole de terre.",
    (2, 2, 3): "Le seau repose entre les tomates.",
    (2, 3, 1): "Un pétale rouge a gardé une goutte ronde.",
    (2, 3, 2): "La coccinelle a repris le bec, tout doux.",
    (2, 3, 3): "L'arrosoir de maman s'est assis dans l'herbe.",
    (3, 1, 1): "Le zinc du robinet a une perle froide.",
    (3, 1, 2): "Le bois du banc a un petit nuage mouillé.",
    (3, 1, 3): "Un papillon est resté sur l'anse bleue.",
    (3, 2, 1): "L'ombre du seau a reculé, tout lent.",
    (3, 2, 2): "La tasse cliquette une dernière fois.",
    (3, 2, 3): "Le seau d'ombre est rentré sous le banc.",
    (3, 3, 1): "Une feuille d'ombre a bu, elle aussi.",
    (3, 3, 2): "Le papillon a suivi la tasse, puis parti.",
    (3, 3, 3): "Le bois du banc a séché, tout doux.",
}


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind == "passage_question" else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = (
        "Raphaël veut porter les gouttes de l'arrosoir jusqu'à une fleur qui penche. "
        "Il choisit une couleur. S'il va trop vite, l'eau saute. "
        "Il attend, joue avec une tasse, ou demande à papa. La fleur se redresse."
    )
    out["title"] = "Les gouttes de l'arrosoir"
    out["characters"] = "Raphaël, papa, maman"
    out["setting"] = "le jardin derrière la maison, après l'arrosage"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def t1_pass(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Raphaël file vers le bac.",
            "narrateur|Le sable colle déjà à ses orteils.",
            "narrateur|La marguerite jaune penche au bord.",
            "enfant-m|Toi d'abord !",
            "narrateur|Il court avec l'arrosoir.",
            "narrateur|Le métal tape sa jambe, toc.",
            "narrateur|Il veut tout verser, d'un coup.",
            "narrateur|L'eau saute sur la dalle chaude.",
            "papa|Elle a soif, pas un bain !",
            "enfant-m|Elle est partie trop vite.",
            "maman|La dalle a tout pris.",
            "narrateur|La marguerite attend encore, toute sèche.",
            "narrateur|Une abeille tourne autour du cœur jaune.",
            "papa|On lui en rapporte, plus lentement ?",
            "enfant-m|Oui.",
            "enfant-m|Sans courir.",
        )
    if i == 2:
        return L(
            "narrateur|Raphaël saute vers les tomates.",
            "narrateur|La terre sombre colle à ses genoux.",
            "narrateur|Le coquelicot rouge penche, tout mince.",
            "enfant-m|Bois, tout de suite !",
            "narrateur|Il verse trop, d'un seul élan.",
            "narrateur|L'eau fait une flaque dans la terre.",
            "narrateur|Le coquelicot se tord, trop lourd.",
            "maman|Sa tige n'aime pas le fleuve.",
            "papa|La flaque est à son pied, trop large.",
            "enfant-m|J'ai versé trop vite.",
            "narrateur|Une coccinelle grimpe, puis s'arrête.",
            "maman|Il lui faut une gorgée, pas un bain.",
            "papa|On va chercher de l'eau, tout doux ?",
            "enfant-m|Tout doux.",
        )
    return L(
        "narrateur|Raphaël tourne jusqu'au banc.",
        "narrateur|Le bois est tiède, un peu lisse.",
        "narrateur|La fleur bleue penche dans l'ombre.",
        "enfant-m|Je t'apporte la mer !",
        "narrateur|Il tourne encore, l'arrosoir au ventre.",
        "narrateur|L'eau gicle et mouille le banc.",
        "papa|Le bois n'a pas soif.",
        "maman|La fleur bleue, elle, attend.",
        "enfant-m|J'ai trop tourné.",
        "narrateur|Un papillon quitte le pétale mouillé.",
        "narrateur|La tête bleue reste basse.",
        "papa|On reprend de l'eau, sans danser ?",
        "enfant-m|Sans danser.",
        "maman|Le banc sèche déjà, un peu.",
    )


def t1_q(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|L'eau a sauté.",
            "maman|Où est-elle allée ?",
        )
    if i == 2:
        return L(
            "narrateur|Le trop d'eau a fait une flaque.",
            "maman|Elle est où, cette flaque ?",
        )
    return L(
        "narrateur|L'eau a mouillé le bois.",
        "maman|Elle a mouillé quoi ?",
    )


def t1_c(i: int) -> list[str]:
    if i == 1:
        return L(
            "narrateur|Oui, sur la dalle chaude.",
            "narrateur|Un rond mouillé brille déjà.",
            "enfant-m|La marguerite n'a rien eu.",
            "maman|Il nous faut d'autre eau.",
            "papa|Le jardin a encore des réserves.",
            "narrateur|L'arrosoir jaune est trop léger, maintenant.",
        )
    if i == 2:
        return L(
            "narrateur|Oui, la flaque est dans la terre.",
            "narrateur|Elle brille au pied du coquelicot.",
            "enfant-m|Il a trop bu, d'un coup.",
            "papa|La prochaine fois, une gorgée.",
            "maman|On va chercher de l'eau ailleurs.",
            "narrateur|L'arrosoir rouge pèse à peine.",
        )
    return L(
        "narrateur|Oui, le banc a pris l'eau.",
        "narrateur|Un nuage mouillé reste sur le bois.",
        "enfant-m|La fleur bleue a encore soif.",
        "maman|On lui en rapporte, tout calme.",
        "papa|Le jardin n'a pas dit son dernier mot.",
        "narrateur|L'arrosoir bleu sonne creux.",
    )


def t2_q(i: int) -> list[str]:
    f = FLEUR[i]
    return L(
        f"narrateur|{f['nom'].capitalize()} a encore soif.",
        "narrateur|Le robinet, le seau, ou l'arrosoir de maman.",
        "papa|On prend l'eau où ?",
    )


def t2_pass(i: int, j: int) -> list[str]:
    key = (i, j)
    if key == (1, 1):
        return L(
            "narrateur|Raphaël court vers le robinet, sable aux pieds.",
            "narrateur|Il ouvre trop grand.",
            "narrateur|L'eau part comme une fusée.",
            "narrateur|Il saute de joie sous le jet.",
            "narrateur|L'arrosoir jaune déborde sur le bac.",
            "papa|Le robinet va trop vite.",
            "maman|Ferme un tout petit peu.",
            "narrateur|Il ferme, puis rouvre un filet.",
            "narrateur|Le métal se remplit, tout calme.",
            "enfant-m|Je peux courir, maintenant ?",
            "papa|On marche, cette fois ?",
            "enfant-m|On marche.",
        )
    if key == (1, 2):
        return L(
            "narrateur|Près du bac, le seau est trop lourd.",
            "narrateur|Raphaël tire, il saute, ça avance mal.",
            "narrateur|L'eau cliquette et lui mouille les orteils.",
            "narrateur|Du sable nage au fond.",
            "papa|On le glisse, sans le lever.",
            "narrateur|Ils traînent le seau vers la marguerite.",
            "narrateur|Raphaël plonge l'arrosoir jaune.",
            "narrateur|Une feuille de sable vient avec.",
            "maman|On laisse le sable se poser.",
            "narrateur|Il attend deux ploc.",
            "enfant-m|Ensuite je puise.",
            "papa|Voilà, tout doux.",
        )
    if key == (1, 3):
        return L(
            "narrateur|L'arrosoir de maman goutte encore dans les fleurs.",
            "narrateur|Presque vide.",
            "narrateur|Raphaël le secoue, trop content.",
            "narrateur|Des gouttes volent.",
            "narrateur|Une abeille s'en va.",
            "maman|Il reste les dernières.",
            "papa|Elles tombent toutes seules.",
            "narrateur|Raphaël se met à genoux.",
            "narrateur|Il tend l'arrosoir jaune sous le bec.",
            "narrateur|Plic, puis rien, puis plic.",
            "enfant-m|J'attends la suivante.",
            "maman|Elle vient.",
        )
    if key == (2, 1):
        return L(
            "narrateur|Vers les tomates, le robinet du potager.",
            "narrateur|Raphaël ouvre, trop content.",
            "narrateur|Le jet brille dans le soleil.",
            "narrateur|Il tape des pieds.",
            "narrateur|L'eau inonde la terre du coquelicot.",
            "papa|Trop fort, le pied va pourrir.",
            "maman|Un filet, comme un fil.",
            "narrateur|Il referme, puis ouvre un peu.",
            "narrateur|L'arrosoir rouge se remplit sans vague.",
            "narrateur|Une coccinelle grimpe sur le bord.",
            "enfant-m|Je reste près du filet.",
            "papa|Bien, le coquelicot attend.",
        )
    if key == (2, 2):
        return L(
            "narrateur|Le seau près des tomates sent la terre.",
            "narrateur|Raphaël veut le porter comme papa.",
            "narrateur|Il le soulève, ça penche.",
            "narrateur|L'eau lui mouille le ventre.",
            "papa|Laisse, on le traîne à deux.",
            "narrateur|Ils glissent le seau entre les plants.",
            "narrateur|Le coquelicot tremble au passage.",
            "narrateur|Raphaël puise avec l'arrosoir rouge.",
            "maman|Doucement, la terre est déjà sombre.",
            "enfant-m|Je ne verse pas encore.",
            "papa|On avance jusqu'à lui.",
        )
    if key == (2, 3):
        return L(
            "narrateur|L'arrosoir de maman est coincé entre les tomates.",
            "narrateur|Raphaël tire, il saute, ça vient.",
            "narrateur|Une coccinelle était sur le bec.",
            "narrateur|Il souffle pour la faire partir.",
            "narrateur|Les dernières gouttes sont roses de terre.",
            "maman|Celles-là, on les garde.",
            "papa|Le coquelicot n'a pas besoin d'un fleuve.",
            "narrateur|Raphaël pose l'arrosoir rouge dessous.",
            "narrateur|Il attend le ploc.",
            "narrateur|Son genou gigote, puis s'arrête.",
            "enfant-m|Encore une.",
            "maman|Elle tombe.",
        )
    if key == (3, 1):
        return L(
            "narrateur|Près du banc, un petit robinet de zinc.",
            "narrateur|L'eau est froide.",
            "narrateur|Raphaël ouvre en tournant trop.",
            "narrateur|Le jet mouille le bois du banc.",
            "narrateur|Il rit, il tourne encore.",
            "papa|Le banc n'a pas soif.",
            "maman|La fleur bleue, elle, oui.",
            "narrateur|Il réduit le filet.",
            "narrateur|L'arrosoir bleu se remplit, tout froid.",
            "narrateur|Un papillon se pose sur l'anse, puis part.",
            "enfant-m|Je tiens le filet.",
            "papa|Petit, comme ça.",
        )
    if key == (3, 2):
        return L(
            "narrateur|Le seau d'ombre est sous le banc.",
            "narrateur|Raphaël s'assoit, veut le tirer d'un coup.",
            "narrateur|Ça résiste.",
            "narrateur|Il recule, il avance, il souffle.",
            "papa|On le sort ensemble.",
            "narrateur|Le bois est tiède.",
            "narrateur|L'eau est froide.",
            "narrateur|Ils posent le seau au soleil du banc.",
            "narrateur|Raphaël plonge l'arrosoir bleu.",
            "maman|Pas trop, le bois glisse.",
            "enfant-m|Juste une gorgée.",
            "papa|Voilà.",
        )
    return L(
        "narrateur|L'arrosoir de maman dort contre le banc.",
        "narrateur|Presque vide, à l'ombre.",
        "narrateur|Raphaël le soulève et le secoue.",
        "narrateur|L'eau gicle sur le bois.",
        "papa|Les dernières gouttes n'aiment pas danser.",
        "maman|Tends le tien dessous.",
        "narrateur|Il s'immobilise, l'arrosoir bleu ouvert.",
        "narrateur|Une goutte.",
        "narrateur|Un papillon passe.",
        "narrateur|Une autre goutte.",
        "enfant-m|Je reste encore un peu.",
        "maman|Elle arrive.",
    )


def t3_q(i: int, j: int) -> list[str]:
    f = FLEUR[i]
    w = EAU[j]
    return L(
        f"narrateur|L'eau {w['de']} est près de {f['nom']}.",
        "narrateur|On attend, on joue, ou on demande.",
        "maman|Tu fais comment, tout doux ?",
    )


def t3_pass(i: int, j: int, k: int) -> list[str]:
    f = FLEUR[i]
    w = EAU[j]
    if k == 1:
        return L(
            "enfant-m|On attend les gouttes.",
            f"narrateur|Raphaël s'accroupit {f['ou']}.",
            f"narrateur|Il penche {f['can']}, un tout petit peu.",
            "narrateur|Une goutte tombe, puis une autre.",
            "papa|Elle boit, tu vois ?",
            f"narrateur|{f['tete']} se redresse un peu.",
            "narrateur|Raphaël gigote, puis il se tient.",
            "maman|Bravo, elle boit.",
            f"narrateur|{w['lab'].capitalize()} fait à peine plic.",
            f"enfant-m|{f['insecte'].capitalize()} peut revenir.",
        )
    if k == 2:
        return L(
            "enfant-m|La tasse fait les voyages.",
            "narrateur|Maman tend une petite tasse.",
            f"narrateur|Raphaël court vers {w['lab']}, puis revient.",
            f"narrateur|Chaque fois, une gorgée pour {f['nom']}.",
            "papa|Tes jambes vont vite.",
            "papa|L'eau, elle, non.",
            "maman|Encore une tasse, tout doux.",
            f"narrateur|{f['tete']} se redresse, goutte après goutte.",
            "enfant-m|J'ai encore envie de courir.",
            "papa|La tasse t'attend, pas le fleuve.",
        )
    return L(
        "enfant-m|Papa, tu le tiens ?",
        "papa|Je le tiens.",
        f"narrateur|Papa tient {f['can']}, tout stable.",
        "narrateur|Raphaël pose deux doigts sur le bec.",
        "narrateur|Ils penchent ensemble, très peu.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais tout seul, très vite.",
        f"papa|Maintenant, on vise {f['sol']}, tout près.",
        f"narrateur|{f['nom'].capitalize()} boit sans se tordre.",
        "papa|Merci de m'avoir appelé.",
    )


def t3_fin(i: int, j: int, k: int) -> list[str]:
    f = FLEUR[i]
    img = FIN_IMG[(i, j, k)]
    if k == 1:
        extra = (
            f"narrateur|Ils restent {f['ou']}, sans bouger beaucoup.",
            f"maman|{f['nom'].capitalize()} a pris le temps.",
            "papa|Tes gouttes sont arrivées.",
        )
    elif k == 2:
        extra = (
            f"narrateur|La petite tasse repose {f['ou']}.",
            "maman|Ta tasse a fait le voyage.",
            "papa|Tu as couru, l'eau non.",
        )
    else:
        extra = (
            f"narrateur|Papa repose {f['can']} {f['ou']}.",
            "maman|Vous avez visé juste.",
            "papa|À deux, c'était plus calme.",
        )
    return L(
        f"narrateur|{f['tete']} ne penche plus.",
        extra[0],
        extra[1],
        extra[2],
        f"narrateur|{FIN_AIR[(i, k)]}",
        f"narrateur|{img}",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "goutte"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une goutte quitte l'arrosoir.",
        "narrateur|Elle fait ploc sur la dalle chaude.",
        "narrateur|Derrière la maison, le jardin est minuscule.",
        "narrateur|Ça sent la terre, et un peu la menthe.",
        "narrateur|Un linge rose sèche près du cerisier.",
        "narrateur|Les bottes de papa cuisent au soleil.",
        "narrateur|Maman a laissé l'arrosoir dans les fleurs.",
        "narrateur|En ce moment, Raphaël s'accroupit.",
        "narrateur|Une petite tête penche, trop sèche.",
        "enfant-m|Elle a soif !",
        "maman|Je n'ai pas vu celle-là.",
        "papa|Il reste des gouttes, tu crois ?",
        "enfant-m|Je les porte !",
        "narrateur|Il saisit l'arrosoir à deux mains.",
        "narrateur|L'eau chante, puis elle danse.",
        "papa|Doucement, elle n'aime pas les vagues.",
        "enfant-m|Je vais trop vite.",
        "maman|Tu peux choisir une fleur.",
        "narrateur|Une jaune attend près du bac.",
        "narrateur|Plus loin, une rouge se tient près des tomates.",
        "narrateur|À l'ombre, une bleue penche près du banc.",
        "papa|Merci d'avoir vu sa soif.",
        "maman|Quelle couleur, Raphaël ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois fleurs attendent encore un peu d'eau.",
        "narrateur|La jaune, la rouge, et la bleue.",
        "maman|Tu vas vers laquelle ?",
    )
    extras["CHK_T0001_P0000"] = t3opts("la jaune", "la rouge", "la bleue")

    q_extra = {
        1: qf(
            "dalle",
            "dalle | la dalle | par terre | sur la dalle | dalle chaude | le sol",
            "L'eau a sauté sur la dalle.",
        ),
        2: qf(
            "terre",
            "terre | la terre | sol | dans la terre | près du coquelicot | au pied",
            "La flaque est dans la terre, près du coquelicot.",
        ),
        3: qf(
            "banc",
            "banc | le banc | bois | le bois | le bois du banc",
            "L'eau a mouillé le banc.",
        ),
    }

    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = t1_pass(i)
        s[f"{p}_Q0001"] = t1_q(i)
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = t1_c(i)
        s[f"{p}_T0002_P0000"] = t2_q(i)
        extras[f"{p}_T0002_P0000"] = t3opts("le robinet", "le seau", "l'arrosoir")
        for j in (1, 2, 3):
            sp = f"{p}_T0002_P000{j}"
            s[sp] = t2_pass(i, j)
            s[f"{sp}_T0003_P0000"] = t3_q(i, j)
            extras[f"{sp}_T0003_P0000"] = t3opts("on attend", "la tasse", "papa")
            for k in (1, 2, 3):
                s[f"{sp}_T0003_P000{k}"] = t3_pass(i, j, k)
                s[f"{sp}_T0003_P000{k}_F0001"] = t3_fin(i, j, k)

    write_tree(s, extras, sons)
    relecture(
        SID,
        "Les gouttes de l'arrosoir",
        "Raphaël veut sauver une fleur qui penche avec les gouttes de l'arrosoir. "
        "T1 colore le voyage (marguerite jaune / coquelicot / fleur bleue). "
        "T2 change la source d'eau (robinet trop fort, seau trop lourd, dernières gouttes). "
        "T3 change la fin (attendre, tasse-jeu, papa tient). "
        "L'élan de Raphaël se voit ; la leçon énergie/besoin n'est pas dite.",
        "Gabarit Aniss/Mila/Tom/Léa/Sami jeté. Adam hors troupe remplacé. "
        "Slogans DIF.ENE retirés. Questions factuelles liées à la scène. "
        "Fins vécues, sans « l'histoire est finie ». Audio non cuit. 27 chemins non écoutés.",
    )


if __name__ == "__main__":
    main()
