#!/usr/bin/env python3
"""F-NAR-009 — réécriture TREE-COL-013 et TREE-COL-014 (texte seulement)."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TROUPE = {
    "Amir",
    "Aniss",
    "Sarah",
    "Chouchou",
    "Mila",
    "Nino",
    "Nina",
    "Raphaël",
    "Victorino",
    "Victorina",
}
FORBIDDEN = ("On va apprendre", "Voici le geste")
MAX_WORDS = 16
FORBIDDEN_NAMES = {
    "Jules",
    "Noé",
    "Noe",
    "Tom",
    "Léa",
    "Lea",
    "Sami",
    "Iris",
    "Lina",
    "Adam",
    "Hugo",
    "Maya",
    "Sara",
    "Inès",
    "Ines",
    "Nora",
    "Gabin",
    "Kenzo",
    "Corentin",
    "Maëlys",
    "Marceau",
    "Ninon",
    "Lila",
    "Lucas",
    "Céline",
    "Celine",
    "Luca",
    "Barnabé",
    "Barnabe",
}


def L(*items: str):
    out = []
    for it in items:
        role, phrase = it.split("|", 1)
        out.append((role, phrase))
    return out


def pack(lines):
    script = "\n".join(f"{r}|{p}" for r, p in lines)
    text = " ".join(p for _, p in lines)
    return text, script


def apply_chunk(chunk, lines, sons=""):
    text, script = pack(lines)
    chunk["text"] = text
    chunk["script"] = script
    chunk["sons"] = sons if sons is not None else ""
    return chunk


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def check_story(data, required_needles, extra_names=()):
    errors = []
    by = {c["chunk_id"]: c for c in data["chunks"]}
    if len(data["chunks"]) != 86:
        errors.append(f"n_chunks={len(data['chunks'])}")
    for c in data["chunks"]:
        script = c.get("script") or ""
        text = c.get("text") or ""
        lines = [ln for ln in script.splitlines() if ln.strip()]
        phrases = []
        for ln in lines:
            if "|" not in ln:
                errors.append(f"{c['chunk_id']} script sans | : {ln}")
                continue
            role, ph = ln.split("|", 1)
            phrases.append(ph)
            if role not in {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}:
                errors.append(f"{c['chunk_id']} role {role}")
            n = words(ph)
            if n > MAX_WORDS:
                errors.append(f"{c['chunk_id']} {n} mots: {ph}")
            for bad in FORBIDDEN:
                if bad.lower() in ph.lower():
                    errors.append(f"{c['chunk_id']} interdit: {bad}")
        joined = " ".join(phrases)
        if joined != text:
            errors.append(f"{c['chunk_id']} text≠script")
        if c["kind"] == "passage_debut":
            first = phrases[0] if phrases else ""
            if re.match(
                r"^(Raphaël|Amir|Nino|Mila|Nina|Aniss|Sarah|Victorino|Victorina|Chouchou)\s+(est|joue|sort)",
                first,
            ):
                errors.append(f"{c['chunk_id']} entrée brutale: {first}")
            roles = {ln.split("|", 1)[0] for ln in lines}
            if "papa" not in roles and "maman" not in roles:
                errors.append(f"{c['chunk_id']} pas d'adulte")
        blob = text
        for name in re.findall(r"\b([A-ZÉÈÊÀÂÎÔÙÛÇ][a-zéèêàâîôùûçëïü]+)\b", blob):
            if name in FORBIDDEN_NAMES:
                errors.append(f"{c['chunk_id']} nom hors troupe: {name}")
            elif (
                name[0].isupper()
                and name not in TROUPE
                and name not in extra_names
                and name not in {
                    "Papa",
                    "Maman",
                    "Maîtresse",
                    "Malaise",
                }
                and re.match(r"^[A-ZÉÈÊÀÂÎÔÙÛÇ][a-zéèêàâîôùûçëïü]{3,}$", name)
                and name
                in {
                    "Lucas",
                    "Céline",
                    "Julien",
                    "Camille",
                    "Thomas",
                    "Emma",
                }
            ):
                errors.append(f"{c['chunk_id']} adulte prénom: {name}")
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                path = [
                    "CHK_T0000_P0000",
                    "CHK_T0001_P0000",
                    f"CHK_T0001_P000{i}",
                    f"CHK_T0001_P000{i}_Q0001",
                    f"CHK_T0001_P000{i}_C0001",
                    f"CHK_T0001_P000{i}_T0002_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
                ]
                blob = " ".join(by[cid]["text"] for cid in path)
                for needle in required_needles:
                    if needle.lower() not in blob.lower():
                        errors.append(f"path {i}{j}{k} manque {needle}")
                if words(blob) < 350:
                    errors.append(f"path {i}{j}{k} trop court {words(blob)}")
                fin = by[path[-1]]["text"]
                if "L'histoire est finie." not in fin:
                    errors.append(f"{path[-1]} sans clôture")
    return errors


# ---------------------------------------------------------------------------
# TREE-COL-013 — Aniss, Sarah, vitre embuée, soupe
# L1 cuisine / jardin / chambre   L2 cubes / livre / dînette   L3 matin / sieste / soir
# ---------------------------------------------------------------------------


def debut_013():
    return L(
        "narrateur|La vitre de la cuisine est toute embuée.",
        "narrateur|Un petit bateau est dessiné au doigt.",
        "narrateur|Dehors, la gouttière chante, goutte à goutte.",
        "narrateur|Ça sent la soupe aux carottes.",
        "narrateur|L'épluchure orange fait un ruban.",
        "narrateur|Les chaussettes d'Aniss sont un peu humides.",
        "papa|Tu as vu le bateau, Aniss ?",
        "enfant-m|Il est sur la vitre.",
        "maman|La soupe est presque prête.",
        "enfant-m|Elle sent bon.",
        "narrateur|Le bois de la table est tiède, un peu collant.",
        "narrateur|Une cuillère en bois attend près du plat.",
        "narrateur|En ce moment, Aniss touche la vitre, tout doux.",
        "narrateur|Sarah va arriver, le manteau mouillé.",
        "maman|On dit bonjour, d'accord ?",
        "enfant-m|Bonjour.",
        "papa|Et si tu veux du pain ?",
        "enfant-m|S'il te plaît.",
        "maman|Bravo.",
        "maman|Et après ?",
        "enfant-m|Merci.",
        "papa|Bonjour.",
        "papa|S'il te plaît.",
        "papa|Merci.",
        "narrateur|Les cubes attendent dans un panier.",
        "narrateur|Le livre sèche près du radiateur.",
        "narrateur|La dînette brille, toute petite.",
        "maman|Sarah aime les mots gentils.",
        "papa|Toi aussi, tu les connais.",
        "enfant-m|Oui, papa.",
        "narrateur|Une carotte coule dans la soupe, tout orange.",
        "maman|Tu es prêt ?",
        "enfant-m|Oui, maman.",
        "papa|Le pain est encore un peu chaud.",
        "narrateur|L'eau de la gouttière fait tic, tic, tic.",
    )


def tq1_013():
    return L(
        "narrateur|On va où, dans la maison ?",
        "maman|La cuisine, le jardin, ou la chambre.",
    )


def l1_013(i: int):
    if i == 1:
        return L(
            "narrateur|Aniss reste dans la cuisine.",
            "narrateur|La soupe fume, tout doux.",
            "narrateur|La porte s'ouvre. Un peu d'air froid.",
            "narrateur|Sarah entre, les joues mouillées.",
            "enfant-m|Bonjour, Sarah.",
            "enfant-f|Bonjour, Aniss.",
            "maman|Bonjour, Sarah.",
            "papa|Donne-moi ton manteau.",
            "enfant-f|S'il te plaît.",
            "papa|Voilà le crochet.",
            "enfant-f|Merci, papa.",
            "enfant-m|S'il te plaît. Du pain.",
            "maman|Voilà une croûte.",
            "enfant-m|Merci, maman.",
            "maman|Bravo, Aniss.",
            "maman|Tu as dit les trois mots.",
            "papa|Bonjour.",
            "papa|S'il te plaît.",
            "papa|Merci.",
            "narrateur|Le bateau sur la vitre reste, tout flou.",
        )
    if i == 2:
        return L(
            "narrateur|Aniss pousse la porte du jardin.",
            "narrateur|L'herbe brille, toute mouillée.",
            "narrateur|Sarah est sous le porche, le nez rose.",
            "enfant-m|Bonjour, Sarah.",
            "enfant-f|Bonjour.",
            "papa|Bonjour, Sarah.",
            "narrateur|Une flaque tremble près des bottes.",
            "enfant-m|S'il te plaît. L'arrosoir.",
            "maman|Il est près du bac.",
            "enfant-m|Merci, maman.",
            "enfant-f|Merci.",
            "maman|Bravo.",
            "maman|Tu as demandé, puis remercié.",
            "papa|On dit aussi bonjour.",
            "enfant-m|Bonjour.",
            "narrateur|Une goutte tombe de la gouttière, dans l'herbe.",
            "maman|Les mots gentils, même dehors.",
        )
    return L(
        "narrateur|Aniss va vers la chambre.",
        "narrateur|Le tapis est doux, un peu chaud.",
        "narrateur|Sarah a laissé ses bottes près de la porte.",
        "enfant-m|Bonjour, Sarah.",
        "enfant-f|Bonjour, Aniss.",
        "maman|Bonjour. Voici le doudou.",
        "enfant-f|S'il te plaît.",
        "maman|Merci d'avoir demandé.",
        "papa|Tu veux le panier, Aniss ?",
        "enfant-m|S'il te plaît.",
        "narrateur|Le panier sent le bois sec.",
        "enfant-m|Merci, papa.",
        "maman|Bravo, les trois mots.",
        "papa|Bonjour.",
        "papa|S'il te plaît.",
        "papa|Merci.",
        "narrateur|La couverture a un pli, tout calme.",
    )


def q_013(i: int):
    if i == 1:
        return L(
            "narrateur|On dit bonjour, s'il te plaît, merci ?",
        )
    if i == 2:
        return L(
            "narrateur|Aniss veut l'arrosoir.",
            "narrateur|Que dit-il ?",
        )
    return L(
        "narrateur|On dit merci ?",
    )


def c_013(i: int):
    if i == 1:
        return L(
            "narrateur|Oui.",
            "maman|Bonjour.",
            "maman|S'il te plaît.",
            "maman|Merci.",
            "narrateur|Aniss respire, tout calme.",
            "papa|Bravo, Aniss.",
            "papa|Tu as fait du bon travail.",
            "enfant-m|Merci, papa.",
            "maman|On continue, tout doux.",
        )
    if i == 2:
        return L(
            "narrateur|Oui.",
            "papa|On dit s'il te plaît.",
            "maman|Et bonjour. Et merci.",
            "narrateur|Aniss tient l'arrosoir, tout léger.",
            "papa|Bravo.",
            "papa|Tu as demandé gentiment.",
            "enfant-m|S'il te plaît.",
            "maman|C'est ça.",
        )
    return L(
        "narrateur|Oui.",
        "maman|On dit merci.",
        "papa|Et bonjour. Et s'il te plaît.",
        "narrateur|Aniss hoche la tête.",
        "maman|Bravo, Aniss.",
        "maman|Tu as fait du bon travail.",
        "enfant-m|Merci, maman.",
    )


def tq2_013():
    return L(
        "narrateur|On joue avec quoi ?",
        "papa|Les cubes, le livre, ou la dînette.",
    )


def l2_013(i: int, j: int):
    lieu_a = {1: "à la cuisine", 2: "au jardin", 3: "à la chambre"}[i]
    if j == 1:
        extra = {
            1: "Un cube a une miette de pain, tout petit.",
            2: "Un cube a une goutte d'herbe, tout vert.",
            3: "Un cube glisse sur le tapis, tout doux.",
        }[i]
        return L(
            f"narrateur|Aniss pose les cubes, {lieu_a}.",
            f"narrateur|{extra}",
            "narrateur|Sarah prend le cube bleu.",
            "enfant-m|Bonjour, Sarah.",
            "enfant-f|Bonjour.",
            "maman|Tu veux le cube rouge, Aniss ?",
            "enfant-m|S'il te plaît.",
            "narrateur|Le cube rouge est lisse, un peu froid.",
            "enfant-m|Merci, maman.",
            "papa|Bravo. Tu as dit les mots.",
            "enfant-f|S'il te plaît. Le jaune.",
            "papa|Voilà. Merci d'avoir demandé.",
            "narrateur|La tour est basse, toute droite.",
            "maman|Les mots gentils, même pour un cube.",
        )
    if j == 2:
        extra = {
            1: "Le livre a une page un peu collante.",
            2: "Le livre a une feuille collée, toute plate.",
            3: "Le livre sent le papier et le doudou.",
        }[i]
        return L(
            f"narrateur|Aniss ouvre le livre, {lieu_a}.",
            f"narrateur|{extra}",
            "narrateur|Sarah trace un dessin du doigt.",
            "enfant-m|Bonjour, Sarah.",
            "enfant-f|Bonjour.",
            "papa|Tu veux que je tourne la page ?",
            "enfant-m|S'il te plaît.",
            "narrateur|La page fait un bruit de papier.",
            "enfant-m|Merci, papa.",
            "maman|Bravo, Aniss.",
            "enfant-f|Merci. Je vois un bateau.",
            "maman|On dit les mots, même pour un livre.",
            "papa|Bonjour.",
            "papa|S'il te plaît.",
            "papa|Merci.",
        )
    extra = {
        1: "Une petite tasse cliquette près du plat.",
        2: "Une cuillère miniature a un peu de pluie.",
        3: "Une assiette miniature est près du doudou.",
    }[i]
    return L(
        f"narrateur|Aniss sort la dînette, {lieu_a}.",
        f"narrateur|{extra}",
        "narrateur|Sarah s'assoit, les pieds qui balancent.",
        "enfant-m|Bonjour, Sarah.",
        "enfant-f|Bonjour.",
        "maman|Une tasse, Aniss ?",
        "enfant-m|S'il te plaît.",
        "narrateur|La tasse est ronde, un peu froide.",
        "enfant-m|Merci, maman.",
        "papa|Bravo. Tu as dit les mots.",
        "enfant-f|S'il te plaît. De la soupe.",
        "papa|Voilà, pour de faux. Merci.",
        "maman|Les mots gentils, à table aussi.",
        "narrateur|La petite cuillère fait un clic.",
    )


def tq3_013():
    return L(
        "narrateur|On reste à quel moment ?",
        "maman|Le matin, après la sieste, ou le soir.",
    )


L3_OPEN_013 = {
    (1, 1, 1): (
        "narrateur|Le pain du matin est encore tiède.",
        "narrateur|Le bol de soupe est vide, un peu chaud.",
        "narrateur|Aniss aligne les cubes près d'une miette.",
    ),
    (1, 1, 2): (
        "narrateur|Après la sieste, la nappe a un pli.",
        "narrateur|Un cube rouge a glissé sous la chaise.",
        "narrateur|Aniss le ramasse, tout doux.",
    ),
    (1, 1, 3): (
        "narrateur|Le soir, la lampe fait un rond jaune.",
        "narrateur|Les cubes font une petite tour.",
        "narrateur|L'ombre de la tour danse sur le bois.",
    ),
    (1, 2, 1): (
        "narrateur|Le matin, le livre est près du cacao.",
        "narrateur|Une page sent encore le pain.",
        "narrateur|Aniss montre le bateau à Sarah.",
    ),
    (1, 2, 2): (
        "narrateur|Après la sieste, le livre est ouvert.",
        "narrateur|Une joue d'Aniss est encore marquée.",
        "narrateur|Sarah tourne une page, tout lentement.",
    ),
    (1, 2, 3): (
        "narrateur|Le soir, le livre est sous la lampe.",
        "narrateur|Les images brillent, un peu dorées.",
        "narrateur|Aniss suit les mots du doigt.",
    ),
    (1, 3, 1): (
        "narrateur|Le matin, la dînette imite le vrai petit déjeuner.",
        "narrateur|Une tasse miniature a une miette.",
        "narrateur|Aniss sert Sarah, tout sérieux.",
    ),
    (1, 3, 2): (
        "narrateur|Après la sieste, la dînette attend sur la table.",
        "narrateur|Une cuillère a glissé, tout calme.",
        "narrateur|Sarah la pose, tout droit.",
    ),
    (1, 3, 3): (
        "narrateur|Le soir, la dînette a trois assiettes.",
        "narrateur|Une pour papa. Une pour maman. Une pour Aniss.",
        "enfant-m|C'est prêt.",
    ),
    (2, 1, 1): (
        "narrateur|Le matin, les cubes sont dans l'herbe mouillée.",
        "narrateur|Papa souffle une goutte, tout doux.",
        "narrateur|Aniss pose le cube vert.",
    ),
    (2, 1, 2): (
        "narrateur|Après la sieste, les cubes sèchent au soleil.",
        "narrateur|Un oiseau saute près du bac.",
        "narrateur|Aniss fait une file, tout droite.",
    ),
    (2, 1, 3): (
        "narrateur|Le soir, les cubes sont sous le porche.",
        "narrateur|La lumière de la cuisine tombe dehors.",
        "narrateur|Aniss construit un mur tout court.",
    ),
    (2, 2, 1): (
        "narrateur|Le matin, le livre repose sur un plaid.",
        "narrateur|Une fourmi passe au bord.",
        "narrateur|Aniss montre une image à papa.",
    ),
    (2, 2, 2): (
        "narrateur|Après la sieste, le livre a une page qui vole.",
        "narrateur|Maman la rattrape.",
        "narrateur|Aniss rit, tout petit.",
    ),
    (2, 2, 3): (
        "narrateur|Le soir, le livre a une tache d'herbe.",
        "narrateur|Papa essuie, tout doux.",
        "narrateur|Aniss attend la suite.",
    ),
    (2, 3, 1): (
        "narrateur|Le matin, la dînette est sur un drap.",
        "narrateur|Le vent bouge une petite cuillère.",
        "enfant-m|À table.",
    ),
    (2, 3, 2): (
        "narrateur|Après la sieste, la dînette a une feuille dedans.",
        "narrateur|Aniss la retire, tout soigneux.",
        "narrateur|On dirait une salade.",
    ),
    (2, 3, 3): (
        "narrateur|Le soir, la dînette range ses tasses.",
        "narrateur|Sarah essuie une cuillère miniature.",
        "narrateur|Le jardin sent encore la pluie.",
    ),
    (3, 1, 1): (
        "narrateur|Le matin, les cubes sont sous le lit.",
        "narrateur|Aniss les aligne, tout droit.",
        "narrateur|Le tapis est doux sous les genoux.",
    ),
    (3, 1, 2): (
        "narrateur|Après la sieste, les cubes font une file vers la porte.",
        "narrateur|Aniss les compte, tout bas.",
        "narrateur|Sarah pose le dernier cube.",
    ),
    (3, 1, 3): (
        "narrateur|Le soir, les cubes font un chemin vers le doudou.",
        "narrateur|La lampe de la chambre est basse.",
        "narrateur|Aniss pose le cube jaune.",
    ),
    (3, 2, 1): (
        "narrateur|Le matin, le livre est sur l'oreiller.",
        "narrateur|Les pages sentent le papier.",
        "narrateur|Aniss écoute la voix de maman.",
    ),
    (3, 2, 2): (
        "narrateur|Après la sieste, le livre raconte un oiseau.",
        "narrateur|Aniss écoute, les yeux ronds.",
        "narrateur|Papa tourne la page.",
    ),
    (3, 2, 3): (
        "narrateur|Le soir, le livre a une page de maison.",
        "enfant-m|C'est chez nous.",
        "papa|Oui.",
    ),
    (3, 3, 1): (
        "narrateur|Le matin, la dînette est près du doudou.",
        "narrateur|Une assiette miniature fait clic.",
        "narrateur|Aniss sert papa, tout sérieux.",
    ),
    (3, 3, 2): (
        "narrateur|Après la sieste, la dînette a trois tasses.",
        "narrateur|Sarah verse de l'air, pour de faux.",
        "enfant-f|S'il te plaît.",
    ),
    (3, 3, 3): (
        "narrateur|Le soir, la dînette range ses assiettes.",
        "narrateur|Aniss essuie une cuillère miniature.",
        "narrateur|Le doudou sent encore le savon.",
    ),
}


def l3_013(i: int, j: int, k: int):
    lieu_a = {1: "à la cuisine", 2: "au jardin", 3: "à la chambre"}[i]
    jeu = {1: "les cubes", 2: "le livre", 3: "la dînette"}[j]
    moment = {1: "le matin", 2: "après la sieste", 3: "le soir"}[k]
    a, b, c = L3_OPEN_013[(i, j, k)]
    play = {
        1: (
            "papa|Tu as fait une tour ?",
            "enfant-m|Oui. Elle est petite.",
            "maman|Bravo. Les mots aussi.",
        ),
        2: (
            "maman|Tu as écouté l'histoire ?",
            "enfant-m|Oui. S'il te plaît. Encore.",
            "papa|Bravo. Tu as demandé.",
        ),
        3: (
            "maman|Tu as servi tout le monde ?",
            "enfant-m|Oui. S'il te plaît. Merci.",
            "papa|Bravo. Les mots gentils aussi.",
        ),
    }[j]
    return L(
        a,
        b,
        c,
        f"narrateur|Aniss est {lieu_a}, {moment}.",
        f"narrateur|Il joue avec {jeu}, près de Sarah.",
        "enfant-m|Bonjour, Sarah.",
        "enfant-f|Bonjour.",
        "enfant-m|S'il te plaît.",
        "enfant-f|Merci, Aniss.",
        play[0],
        play[1],
        play[2],
        "maman|Bonjour. S'il te plaît. Merci.",
        "papa|Tu as fait du bon travail.",
        "narrateur|Aniss sourit, tout calme.",
    )


def fin_013(i: int, j: int, k: int):
    lieu_a = {1: "à la cuisine", 2: "au jardin", 3: "à la chambre"}[i]
    jeu = {1: "les cubes", 2: "le livre", 3: "la dînette"}[j]
    moment = {1: "le matin", 2: "après la sieste", 3: "le soir"}[k]
    extra = {
        1: "La vitre a gardé le petit bateau.",
        2: "L'herbe a senti bon, encore un peu.",
        3: "La couverture est restée douce.",
    }[i]
    return L(
        f"narrateur|Aniss a dit les mots, {lieu_a}.",
        f"narrateur|Il a joué avec {jeu}.",
        f"narrateur|C'était {moment}.",
        f"narrateur|{extra}",
        "enfant-m|Bonjour. S'il te plaît. Merci.",
        "papa|Bravo, Aniss.",
        "papa|Tu as fait du bon travail.",
        "maman|Sarah a entendu les mots gentils.",
        "enfant-f|Merci, Aniss.",
        "narrateur|L'histoire est finie.",
    )


SONS_L1_013 = {1: "soupe,porte", 2: "jardin,gouttiere", 3: "tapis"}
SONS_L2_013 = {1: "cubes", 2: "pages", 3: "dinette"}
SONS_L3_013 = {1: "matin", 2: "sieste", 3: "soir,lampe"}


def build_013(source):
    data = deepcopy(source)
    data["fil_rouge"] = (
        "La vitre est embuée. Aniss sent la soupe aux carottes. "
        "Sarah arrive, le manteau mouillé. Il dit bonjour, s'il te plaît, merci."
    )
    data["title"] = "Le bateau sur la vitre"
    data["characters"] = "Aniss, Sarah, papa, maman"
    data["setting"] = "maison sous la pluie, cuisine"
    by = {c["chunk_id"]: c for c in data["chunks"]}

    apply_chunk(by["CHK_T0000_P0000"], debut_013(), "gouttiere,soupe")
    apply_chunk(by["CHK_T0001_P0000"], tq1_013(), "")

    for i in (1, 2, 3):
        apply_chunk(by[f"CHK_T0001_P000{i}"], l1_013(i), SONS_L1_013[i])
        apply_chunk(by[f"CHK_T0001_P000{i}_Q0001"], q_013(i), "")
        apply_chunk(by[f"CHK_T0001_P000{i}_C0001"], c_013(i), "")
        apply_chunk(by[f"CHK_T0001_P000{i}_T0002_P0000"], tq2_013(), "")
        for j in (1, 2, 3):
            apply_chunk(
                by[f"CHK_T0001_P000{i}_T0002_P000{j}"],
                l2_013(i, j),
                SONS_L2_013[j],
            )
            apply_chunk(
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"],
                tq3_013(),
                "",
            )
            for k in (1, 2, 3):
                apply_chunk(
                    by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"],
                    l3_013(i, j, k),
                    SONS_L3_013[k],
                )
                apply_chunk(
                    by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"],
                    fin_013(i, j, k),
                    "",
                )
    data["chunks"] = [by[c["chunk_id"]] for c in source["chunks"]]
    return data


# ---------------------------------------------------------------------------
# TREE-COL-014 — Nina, flaque, gant rouge, parc
# L1 bac à sable / toboggan / balançoires
# L2 ballon / seau / doudou
# L3 Nino / Mila / Raphaël
# ---------------------------------------------------------------------------


def debut_014():
    return L(
        "narrateur|Une flaque tient le ciel.",
        "narrateur|Le ciel est tout petit, tout bleu.",
        "narrateur|Un gant rouge sèche sur la barrière.",
        "narrateur|Le toboggan brille, encore froid.",
        "narrateur|Ça sent le sable mouillé.",
        "narrateur|Le cartable de Nina est contre le banc.",
        "maman|Ton gant a trop d'eau, Nina.",
        "enfant-f|Il est lourd.",
        "papa|Je l'ai posé là.",
        "papa|Il va sécher.",
        "narrateur|En ce moment, Nina est au parc.",
        "narrateur|Son manteau sent encore la classe.",
        "narrateur|Elle a écouté la maîtresse.",
        "narrateur|Un camarade a parlé tout bas.",
        "narrateur|Le ventre de Nina s'est serré.",
        "enfant-f|J'ai un malaise, maman.",
        "maman|Tu as bien fait de le dire.",
        "maman|On écoute la maîtresse.",
        "maman|Si malaise, on raconte à la maison.",
        "enfant-f|Je raconte à la maison.",
        "papa|Je t'écoute aussi.",
        "narrateur|Le sable est froid sous les bottes.",
        "narrateur|Le seau est rouge, un peu penché.",
        "maman|Tu as écouté, à l'école ?",
        "enfant-f|Oui. J'ai écouté.",
        "papa|Bravo, Nina.",
        "papa|C'est du bon travail.",
        "narrateur|Une feuille colle au toboggan.",
        "maman|On reste un moment, ici.",
        "enfant-f|D'accord.",
        "narrateur|Une corneille marche près du seau.",
        "papa|Ton ventre est un peu moins serré ?",
        "enfant-f|Un peu.",
    )


def tq1_014():
    return L(
        "narrateur|Nina va où, dans le parc ?",
        "maman|Le bac à sable, le toboggan, ou les balançoires.",
    )


def l1_014(i: int):
    if i == 1:
        return L(
            "narrateur|Nina va vers le bac à sable.",
            "narrateur|Le sable est froid, un peu lourd.",
            "narrateur|Une petite pelle brille, toute mouillée.",
            "narrateur|Elle se souvient de la classe.",
            "narrateur|Elle a écouté la maîtresse.",
            "narrateur|Le camarade a parlé d'un secret, tout bas.",
            "enfant-f|Mon ventre est serré.",
            "maman|C'est un malaise.",
            "maman|Ce soir, tu racontes à la maison.",
            "enfant-f|Je raconte à papa et maman.",
            "maman|Oui. On écoute la maîtresse.",
            "papa|Si malaise, on raconte à la maison.",
            "papa|Je t'écoute, déjà.",
            "narrateur|Nina pose une main dans le sable.",
            "maman|Bravo, Nina. Tu as parlé.",
            "narrateur|Le gant rouge sèche, plus loin.",
        )
    if i == 2:
        return L(
            "narrateur|Nina va vers le toboggan.",
            "narrateur|Le métal est froid sous la main.",
            "narrateur|Une feuille collée brille, toute plate.",
            "narrateur|Elle a écouté la maîtresse, à l'école.",
            "narrateur|Son ventre est encore serré.",
            "enfant-f|C'est un malaise.",
            "maman|Oui. Tu le diras à la maison.",
            "enfant-f|Papa aussi ?",
            "papa|Moi aussi. Je suis là.",
            "maman|On écoute la maîtresse.",
            "maman|Si malaise, raconter à la maison.",
            "narrateur|Nina monte une marche, tout doux.",
            "papa|Tu veux que je tienne ta main ?",
            "enfant-f|Oui.",
            "maman|Bravo. Tu as parlé de ton ventre.",
        )
    return L(
        "narrateur|Nina va vers les balançoires.",
        "narrateur|La chaîne fait tic, tout léger.",
        "narrateur|Le siège est un peu humide.",
        "narrateur|Elle a écouté la maîtresse.",
        "narrateur|Le malaise est encore là, tout petit.",
        "enfant-f|Ce soir, je raconte.",
        "maman|Oui. À la maison.",
        "papa|Donne-moi ta main.",
        "narrateur|La main de papa est tiède.",
        "maman|On écoute la maîtresse.",
        "maman|Si tu as un malaise, tu racontes.",
        "enfant-f|Raconter à la maison.",
        "papa|C'est ça. Bravo, Nina.",
        "narrateur|Une goutte tombe de la chaîne.",
    )


def q_014(i: int):
    if i == 1:
        return L(
            "narrateur|On écoute la maîtresse ?",
            "maman|Si malaise, on raconte à la maison ?",
        )
    if i == 2:
        return L("narrateur|Un malaise : on raconte à la maison ?")
    return L("narrateur|On écoute la maîtresse ?")


def c_014(i: int):
    if i == 1:
        return L(
            "narrateur|Oui.",
            "maman|On écoute la maîtresse.",
            "maman|Si malaise, raconter à la maison.",
            "narrateur|Nina respire, tout calme.",
            "papa|Bravo, Nina.",
            "papa|Tu as fait du bon travail.",
            "enfant-f|Je raconte à la maison.",
        )
    if i == 2:
        return L(
            "narrateur|Oui.",
            "papa|Si malaise, tu racontes à la maison.",
            "maman|On écoute aussi la maîtresse.",
            "narrateur|Nina tient la rampe, tout calme.",
            "maman|Bravo. Tu as parlé.",
            "enfant-f|Papa écoutera.",
            "papa|Oui. J'écoute.",
        )
    return L(
        "narrateur|Oui.",
        "maman|On écoute la maîtresse.",
        "maman|Si malaise, raconter à la maison.",
        "narrateur|Nina hoche la tête.",
        "papa|On continue, avec nous.",
        "enfant-f|D'accord, papa.",
        "maman|Bravo, Nina.",
    )


def tq2_014():
    return L(
        "narrateur|Nina prend quoi ?",
        "papa|Le ballon, le seau, ou le doudou.",
    )


def l2_014(i: int, j: int):
    lieu_a = {1: "au bac à sable", 2: "au toboggan", 3: "aux balançoires"}[i]
    if j == 1:
        extra = {
            1: "Le ballon a un peu de sable.",
            2: "Le ballon rebondit près du toboggan.",
            3: "Le ballon roule sous la balançoire.",
        }[i]
        return L(
            "narrateur|Plus tard, Nina prend le ballon.",
            f"narrateur|{extra}",
            f"narrateur|Elle est encore {lieu_a}.",
            "enfant-f|J'ai écouté la maîtresse.",
            "enfant-f|J'ai un malaise.",
            "papa|Tu as bien fait de raconter.",
            "maman|Tu as écouté, à l'école.",
            "papa|Si malaise, tu viens nous le dire.",
            "enfant-f|Je raconte à la maison.",
            "maman|Bravo, Nina.",
            "maman|C'est du bon travail.",
            "narrateur|Le ballon est un peu froid.",
            "papa|Je t'écoute. On reste un moment.",
        )
    if j == 2:
        extra = {
            1: "Le seau est plein de sable mouillé.",
            2: "Le seau a une feuille dedans.",
            3: "Le seau pend près du gant.",
        }[i]
        return L(
            "narrateur|Plus tard, Nina prend le seau.",
            f"narrateur|{extra}",
            f"narrateur|Elle pense encore {lieu_a}.",
            "enfant-f|J'ai écouté la maîtresse.",
            "enfant-f|J'ai eu un malaise.",
            "papa|Raconte. On est là.",
            "enfant-f|Un camarade a parlé tout bas.",
            "maman|Tu as bien fait de le dire.",
            "maman|À la maison.",
            "papa|On écoute la maîtresse.",
            "papa|Si malaise, raconter à papa ou maman.",
            "maman|Bravo. Ton ventre peut se desserrer.",
            "narrateur|Une goutte glisse du bord du seau.",
            "enfant-f|Merci, papa. Merci, maman.",
        )
    extra = {
        1: "Le doudou a du sable à l'oreille.",
        2: "Le doudou sent encore le manteau.",
        3: "Le doudou est coincé contre la chaîne.",
    }[i]
    return L(
        "narrateur|Plus tard, Nina prend le doudou.",
        f"narrateur|{extra}",
        f"narrateur|Nina pense encore {lieu_a}.",
        "narrateur|Papa s'assoit sur le banc.",
        "enfant-f|J'ai un malaise.",
        "enfant-f|Je raconte à la maison.",
        "maman|On t'écoute.",
        "enfant-f|Un camarade a chuchoté, à l'école.",
        "papa|Tu as écouté la maîtresse.",
        "papa|Puis tu nous as dit.",
        "maman|Si malaise, tu racontes à la maison.",
        "papa|Bravo, Nina. Tu as fait du bon travail.",
        "narrateur|Le doudou est doux, un peu froissé.",
        "maman|Tu veux rester un peu ?",
        "enfant-f|Oui.",
    )


def tq3_014():
    return L(
        "narrateur|Qui arrive, au parc ?",
        "maman|Nino, Mila, ou Raphaël.",
    )


L3_OPEN_014 = {
    (1, 1, 1): (
        "narrateur|Nino arrive, les genoux sablés.",
        "narrateur|Il a une feuille collée au pantalon.",
        "narrateur|Nina tient le ballon contre son manteau.",
    ),
    (1, 1, 2): (
        "narrateur|Mila arrive, un bonnet bleu.",
        "narrateur|Une mèche est encore mouillée.",
        "narrateur|Nina fait rouler le ballon, tout doux.",
    ),
    (1, 1, 3): (
        "narrateur|Raphaël arrive, les bottes rouges.",
        "narrateur|Il a un bâton de bois, trop grand.",
        "narrateur|Nina pose le ballon près du bac.",
    ),
    (1, 2, 1): (
        "narrateur|Nino s'accroupit près du seau.",
        "narrateur|Le sable fait un petit tas.",
        "narrateur|Nina reverse une pelletée.",
    ),
    (1, 2, 2): (
        "narrateur|Mila touche le bord du seau.",
        "narrateur|Le plastique est froid, un peu rêche.",
        "narrateur|Nina sourit, tout petit.",
    ),
    (1, 2, 3): (
        "narrateur|Raphaël pose son bâton près du seau.",
        "narrateur|Une fourmi passe au bord.",
        "narrateur|Nina souffle le sable, tout doux.",
    ),
    (1, 3, 1): (
        "narrateur|Nino voit le doudou dans le sable.",
        "narrateur|Il le tend, tout soigneux.",
        "enfant-m|Tiens.",
    ),
    (1, 3, 2): (
        "narrateur|Mila caresse l'oreille du doudou.",
        "narrateur|Un grain de sable tombe.",
        "narrateur|Nina le serre contre elle.",
    ),
    (1, 3, 3): (
        "narrateur|Raphaël assied le doudou sur le seau.",
        "narrateur|Le doudou penche, tout drôle.",
        "narrateur|Nina rit, tout bas.",
    ),
    (2, 1, 1): (
        "narrateur|Nino attend en bas du toboggan.",
        "narrateur|Le ballon est sous son bras.",
        "narrateur|Nina descend, tout doux.",
    ),
    (2, 1, 2): (
        "narrateur|Mila tient le ballon en haut.",
        "narrateur|Le métal brille sous ses mains.",
        "narrateur|Nina pose un pied, puis l'autre.",
    ),
    (2, 1, 3): (
        "narrateur|Raphaël fait rouler le ballon au pied.",
        "narrateur|Nina glisse, les joues froides.",
        "narrateur|Le vent est doux.",
    ),
    (2, 2, 1): (
        "narrateur|Nino a mis le seau en bas.",
        "narrateur|Comme un panier, tout rouge.",
        "narrateur|Nina arrive près de lui.",
    ),
    (2, 2, 2): (
        "narrateur|Mila a une feuille dans le seau.",
        "narrateur|Nina la retire, tout calme.",
        "narrateur|On dirait un bateau.",
    ),
    (2, 2, 3): (
        "narrateur|Raphaël tape le seau, tout léger.",
        "narrateur|Ça fait un petit bruit rond.",
        "narrateur|Nina écoute, les yeux ronds.",
    ),
    (2, 3, 1): (
        "narrateur|Nino a le doudou sur les genoux.",
        "narrateur|Il est en bas du toboggan.",
        "narrateur|Nina le reprend, tout doux.",
    ),
    (2, 3, 2): (
        "narrateur|Mila pose le doudou sur une marche.",
        "narrateur|Il attend, tout sage.",
        "narrateur|Nina le prend avant de glisser.",
    ),
    (2, 3, 3): (
        "narrateur|Raphaël tient le doudou, tout haut.",
        "narrateur|Pour qu'il voie le ciel dans la flaque.",
        "narrateur|Nina dit merci, tout bas.",
    ),
    (3, 1, 1): (
        "narrateur|Nino pousse la balançoire, tout doux.",
        "narrateur|Le ballon attend dans l'herbe.",
        "narrateur|Nina tient la chaîne.",
    ),
    (3, 1, 2): (
        "narrateur|Mila s'assoit sur l'autre balançoire.",
        "narrateur|Le ballon est entre les deux.",
        "narrateur|Nina balance un peu, tout lentement.",
    ),
    (3, 1, 3): (
        "narrateur|Raphaël ramasse le ballon sous la balançoire.",
        "narrateur|Il le pose sur les genoux de Nina.",
        "narrateur|La chaîne fait tic.",
    ),
    (3, 2, 1): (
        "narrateur|Nino a le seau près des pieds.",
        "narrateur|Nina balance, tout petit.",
        "narrateur|Le seau ne bouge pas.",
    ),
    (3, 2, 2): (
        "narrateur|Mila met le seau sous la balançoire.",
        "narrateur|Comme une maison, tout rouge.",
        "narrateur|Nina rit.",
    ),
    (3, 2, 3): (
        "narrateur|Raphaël verse de l'air dans le seau.",
        "narrateur|Pour de faux, tout sérieux.",
        "narrateur|Nina arrête la balançoire.",
    ),
    (3, 3, 1): (
        "narrateur|Nino pose le doudou à côté.",
        "narrateur|Le doudou voyage, tout doux.",
        "narrateur|Nina le regarde.",
    ),
    (3, 3, 2): (
        "narrateur|Mila cale le doudou contre Nina.",
        "narrateur|Pour qu'il ne tombe pas.",
        "narrateur|Nina le serre.",
    ),
    (3, 3, 3): (
        "narrateur|Raphaël a mis le doudou sur le banc.",
        "narrateur|Il voit le gant rouge, tout loin.",
        "narrateur|Nina balance encore un peu.",
    ),
}

FRIEND_014 = {1: ("Nino", "enfant-m"), 2: ("Mila", "enfant-f"), 3: ("Raphaël", "enfant-m")}


def l3_014(i: int, j: int, k: int):
    lieu_a = {1: "au bac à sable", 2: "au toboggan", 3: "aux balançoires"}[i]
    jouet = {1: "le ballon", 2: "le seau", 3: "le doudou"}[j]
    ami, role = FRIEND_014[k]
    a, b, c = L3_OPEN_014[(i, j, k)]
    return L(
        a,
        b,
        c,
        f"narrateur|Nina est {lieu_a}.",
        f"narrateur|Elle a {jouet}.",
        f"enfant-f|Bonjour, {ami}.",
        f"{role}|Bonjour, Nina.",
        "enfant-f|J'ai raconté mon malaise.",
        "papa|Oui. Tu as écouté, puis raconté.",
        "maman|Si malaise, raconter à la maison.",
        f"{role}|Tu as parlé à maman ?",
        "enfant-f|Oui. Et à papa.",
        "papa|On écoute la maîtresse.",
        "maman|Puis on raconte, à la maison.",
        "narrateur|Le ventre de Nina se desserre, tout doucement.",
        "enfant-f|Merci, papa. Merci, maman.",
    )


def fin_014(i: int, j: int, k: int):
    lieu_a = {1: "au bac à sable", 2: "au toboggan", 3: "aux balançoires"}[i]
    jouet = {1: "le ballon", 2: "le seau", 3: "le doudou"}[j]
    venu = {1: "Nino est venu.", 2: "Mila est venue.", 3: "Raphaël est venu."}[k]
    extra = {
        1: "Le sable est resté froid, tout calme.",
        2: "Le toboggan a gardé sa feuille.",
        3: "La chaîne a fait tic, encore un peu.",
    }[i]
    return L(
        f"narrateur|Nina a joué {lieu_a}.",
        f"narrateur|Elle a pris {jouet}.",
        f"narrateur|{venu}",
        f"narrateur|{extra}",
        "enfant-f|J'ai écouté. Puis j'ai raconté.",
        "papa|Bravo, Nina.",
        "papa|Tu as fait du bon travail.",
        "maman|On t'a écoutée.",
        "maman|Si malaise, tu reviens nous le dire.",
        "narrateur|Le gant rouge est presque sec.",
        "narrateur|L'histoire est finie.",
    )


SONS_L1_014 = {1: "sable", 2: "toboggan", 3: "balancoire"}
SONS_L2_014 = {1: "ballon", 2: "seau", 3: "doudou"}
SONS_L3_014 = {1: "enfants_parc", 2: "enfants_parc", 3: "enfants_parc"}


def build_014(source):
    data = deepcopy(source)
    data["fil_rouge"] = (
        "Une flaque tient le ciel. Le gant rouge de Nina sèche. "
        "Elle a écouté la maîtresse. Un chuchotement a serré son ventre. "
        "Elle raconte à la maison, au parc."
    )
    data["title"] = "Le gant rouge de Nina"
    data["characters"] = "Nina, papa, maman"
    data["setting"] = "au parc, après l'école"
    by = {c["chunk_id"]: c for c in data["chunks"]}

    apply_chunk(by["CHK_T0000_P0000"], debut_014(), "enfants_parc,flaque")
    apply_chunk(by["CHK_T0001_P0000"], tq1_014(), "")

    for i in (1, 2, 3):
        apply_chunk(by[f"CHK_T0001_P000{i}"], l1_014(i), SONS_L1_014[i])
        apply_chunk(by[f"CHK_T0001_P000{i}_Q0001"], q_014(i), "")
        apply_chunk(by[f"CHK_T0001_P000{i}_C0001"], c_014(i), "")
        apply_chunk(by[f"CHK_T0001_P000{i}_T0002_P0000"], tq2_014(), "")
        for j in (1, 2, 3):
            apply_chunk(
                by[f"CHK_T0001_P000{i}_T0002_P000{j}"],
                l2_014(i, j),
                SONS_L2_014[j],
            )
            apply_chunk(
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"],
                tq3_014(),
                "",
            )
            for k in (1, 2, 3):
                apply_chunk(
                    by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"],
                    l3_014(i, j, k),
                    SONS_L3_014[k],
                )
                apply_chunk(
                    by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"],
                    fin_014(i, j, k),
                    "",
                )
    data["chunks"] = [by[c["chunk_id"]] for c in source["chunks"]]
    return data


def main():
    all_err = []
    for sid, builder, needles, extra in (
        (
            "TREE-COL-013",
            build_013,
            ["bonjour", "s'il te plaît", "merci"],
            (),
        ),
        (
            "TREE-COL-014",
            build_014,
            ["écout", "malaise", "maison"],
            (),
        ),
    ):
        src = json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))
        data = builder(src)
        err = check_story(data, needles, extra)
        out = ROOT / sid / "merged.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(sid, "chunks", len(data["chunks"]), "wrote", out)
        print("  debut:", data["chunks"][0]["text"][:90])
        if err:
            print("  ERRORS", len(err))
            for e in err[:50]:
                print("   ", e)
            all_err.extend(err)
        else:
            print("  OK")
    if all_err:
        raise SystemExit(f"{len(all_err)} erreurs")


if __name__ == "__main__":
    main()
