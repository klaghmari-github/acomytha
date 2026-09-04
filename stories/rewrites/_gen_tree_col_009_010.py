#!/usr/bin/env python3
"""F-NAR-009 — merged.json TREE-COL-009 et TREE-COL-010 (texte seulement)."""
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
SKIP_NAMES = {
    "Papa",
    "Maman",
    "Oui",
    "Non",
    "Bravo",
    "Merci",
    "Bonjour",
    "Ensuite",
    "Après",
    "Avec",
    "Puis",
    "Près",
    "Dans",
    "Une",
    "Un",
    "Le",
    "La",
    "Les",
    "Des",
    "Du",
    "De",
    "Au",
    "En",
    "Ce",
    "Cette",
    "Il",
    "Elle",
    "On",
    "Tu",
    "Je",
    "Nous",
    "Vous",
    "Et",
    "Mais",
    "Si",
    "Quand",
    "Voici",
    "Voilà",
    "L",
    "D",
    "C",
    "S",
    "N",
    "Qu",
    "Maîtresse",
    "Malaise",
    "Alors",
    "Comme",
    "Tout",
    "Tous",
    "Toutes",
    "Plus",
    "Moins",
    "Très",
    "Bien",
    "Bon",
    "Belle",
    "Petit",
    "Petite",
    "Grand",
    "Grande",
    "Ici",
    "Là",
    "Maintenant",
    "Encore",
    "Toujours",
    "Jamais",
    "Aussi",
    "Donc",
    "Car",
    "Parce",
    "Pour",
    "Sans",
    "Sous",
    "Sur",
    "Vers",
    "Chez",
    "Entre",
    "Pendant",
    "Avant",
    "Depuis",
    "Aujourd",
    "Demain",
    "Hier",
    "Midi",
    "Soir",
    "Matin",
    "Daccord",
    "Ça",
    "Son",
    "Sa",
    "Ses",
    "Ils",
    "Elles",
    "Mon",
    "Ma",
    "Mes",
    "Ton",
    "Ta",
    "Tes",
    "Nos",
    "Vos",
    "Leur",
    "Leurs",
    "Que",
    "Qui",
    "Quoi",
    "Dont",
    "Où",
    "Comment",
    "Pourquoi",
}


def L(*items: str) -> list[tuple[str, str]]:
    out = []
    for it in items:
        role, phrase = it.split("|", 1)
        out.append((role, phrase))
    return out


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    script = "\n".join(f"{r}|{p}" for r, p in lines)
    text = " ".join(p for _, p in lines)
    return text, script


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def apply_chunk(src: dict, lines: list[tuple[str, str]]) -> dict:
    text, script = pack(lines)
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    if out.get("sons") is None:
        out["sons"] = ""
    return out


def write_story(story_id: str, meta: dict, by_id: dict[str, list[tuple[str, str]]]) -> dict:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:12]} extra={extra[:12]}")
    chunks = [apply_chunk(c, by_id[c["chunk_id"]]) for c in source["chunks"]]
    merged = dict(source)
    merged.update(meta)
    merged["chunks"] = chunks
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return merged


def check_story(data: dict, needles: list[str], maxw: int) -> list[str]:
    errors: list[str] = []
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
                errors.append(f"{c['chunk_id']} script sans |")
                continue
            role, ph = ln.split("|", 1)
            phrases.append(ph)
            if role not in {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}:
                errors.append(f"{c['chunk_id']} role {role}")
            n = words(ph)
            if n > maxw:
                errors.append(f"{c['chunk_id']} {n} mots: {ph}")
            for bad in FORBIDDEN:
                if bad.lower() in ph.lower():
                    errors.append(f"{c['chunk_id']} interdit: {bad}")
        if " ".join(phrases) != text:
            errors.append(f"{c['chunk_id']} text≠script")
        if c["kind"] == "passage_debut":
            first = phrases[0] if phrases else ""
            if re.match(
                r"^(Raphaël|Amir|Nino|Mila|Nina|Sarah|Aniss|Chouchou|Victorino|Victorina)\s+(est|joue|sort)",
                first,
            ):
                errors.append(f"{c['chunk_id']} entrée brutale: {first}")
            if first.startswith("Aujourd'hui") or first.startswith("On va apprendre"):
                errors.append(f"{c['chunk_id']} amorce interdite: {first}")
            roles = {ln.split("|", 1)[0] for ln in lines}
            if "papa" not in roles and "maman" not in roles:
                errors.append(f"{c['chunk_id']} pas d'adulte")
        blob = text
        for name in re.findall(r"\b([A-ZÉÈÊÀÂÎÔÙÛÇ][a-zéèêàâîôùûçëïü]+)\b", blob):
            if name in SKIP_NAMES or name in TROUPE:
                continue
            errors.append(f"{c['chunk_id']} nom hors troupe: {name}")
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
                for needle in needles:
                    if needle.lower() not in blob.lower():
                        errors.append(f"path {i}{j}{k} manque {needle}")
                if words(blob) < 350:
                    errors.append(f"path {i}{j}{k} trop court {words(blob)}")
                fin = by[path[-1]]["text"]
                if "L'histoire est finie." not in fin:
                    errors.append(f"{path[-1]} sans clôture")
    return errors


# ---------------------------------------------------------------------------
# TREE-COL-009 — Nina, école, N3
# L1 cubes / livre / dînette   L2 pomme / yaourt / pain   L3 chat / chien / poule
# ---------------------------------------------------------------------------

TOY = {1: "les cubes", 2: "le livre", 3: "la dînette"}
TOY_PRES = {1: "des cubes", 2: "du livre", 3: "de la dînette"}
SNACK = {1: "une pomme", 2: "un yaourt", 3: "un morceau de pain"}
SNACK_DE = {1: "d'une pomme", 2: "d'un yaourt", 3: "d'un morceau de pain"}
ANIMAL = {1: "le chat", 2: "le chien", 3: "la poule"}


def debut_009() -> list[tuple[str, str]]:
    return L(
        "narrateur|Le radiateur de la classe fait tic, tout chaud.",
        "narrateur|Un bouton rouge attend sur le crochet.",
        "narrateur|La vitre est embuée, toute douce.",
        "narrateur|Papa trace un petit rond du doigt.",
        "narrateur|Ça sent la cire des crayons.",
        "narrateur|Ça sent aussi le savon des mains.",
        "narrateur|Le sol brille encore, après la serpillière.",
        "narrateur|Le cartable de Nina pose contre le casier.",
        "narrateur|Un crayon bleu dépasse, tout lisse.",
        "maman|Tu as vu le bouton rouge ?",
        "enfant-f|Il est tout seul.",
        "papa|On le range dans la poche.",
        "maman|Tu écoutes la maîtresse, d'accord ?",
        "enfant-f|D'accord, maman.",
        "papa|Et si tu as un malaise ?",
        "papa|Tu racontes à papa ou maman.",
        "enfant-f|Je raconte à la maison.",
        "narrateur|En ce moment, Nina accroche son manteau.",
        "narrateur|Le manteau est encore un peu froid.",
        "narrateur|La classe est calme, un peu claire.",
        "narrateur|La maîtresse parle près du tableau.",
        "narrateur|Nina écoute, tout près.",
        "narrateur|Les mots arrivent, tout doux.",
        "narrateur|Un camarade se penche près de l'oreille.",
        "narrateur|Il parle tout bas.",
        "narrateur|Nina sent un malaise.",
        "narrateur|Son ventre se serre, tout petit.",
        "enfant-f|Papa. J'ai un malaise.",
        "papa|Tu as bien fait de le dire.",
        "maman|On écoute la maîtresse.",
        "maman|Si malaise, on raconte à la maison.",
        "papa|Bravo, Nina.",
        "papa|C'est du bon travail.",
        "enfant-f|Merci, papa.",
        "narrateur|Les cubes attendent sur le tapis.",
        "narrateur|Le livre est près de la fenêtre.",
        "narrateur|La dînette brille, toute petite.",
        "maman|Tu es prête ?",
        "enfant-f|Oui, maman.",
    )


def tq1_009() -> list[tuple[str, str]]:
    return L(
        "narrateur|Nina va vers quel jeu ?",
        "papa|Les cubes, le livre, ou la dînette.",
    )


def l1_009(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Nina s'assoit près des cubes.",
            "narrateur|Ils sont en bois, un peu rudes.",
            "narrateur|Un cube rouge fait toc, sur le tapis.",
            "narrateur|Papa s'assoit aussi, tout près.",
            "maman|Tu écoutes encore, Nina ?",
            "enfant-f|J'écoute la maîtresse.",
            "papa|Et le malaise ?",
            "enfant-f|Je raconte à la maison.",
            "maman|Oui. À papa ou à maman.",
            "narrateur|La maîtresse parle, plus loin.",
            "narrateur|Nina écoute, les mains sur un cube.",
            "papa|Bravo. Tu as écouté.",
            "maman|Tu as raconté aussi.",
            "enfant-f|Mon ventre est plus calme.",
            "narrateur|Le cube rouge reste dans sa main.",
        )
    if i == 2:
        return L(
            "narrateur|Nina ouvre le livre, tout doux.",
            "narrateur|La couverture est un peu rêche.",
            "narrateur|Une page chuchote sous le doigt.",
            "narrateur|Maman s'assoit près de la fenêtre.",
            "papa|Tu écoutes l'histoire ?",
            "enfant-f|J'écoute la maîtresse aussi.",
            "maman|Et si le ventre se serre ?",
            "enfant-f|Je raconte à la maison.",
            "papa|Oui. Papa ou maman t'écoute.",
            "narrateur|La maîtresse lit, plus loin.",
            "narrateur|Nina écoute, le livre sur les genoux.",
            "maman|Bravo, Nina.",
            "papa|Tu as écouté. Tu as raconté.",
            "enfant-f|Le malaise s'en va, tout doux.",
            "narrateur|Un oiseau passe derrière la vitre.",
        )
    return L(
        "narrateur|Nina pose une tasse de dînette.",
        "narrateur|La tasse est froide, toute petite.",
        "narrateur|Ça sent presque la soupe, pour de rire.",
        "narrateur|Papa tient une cuillère en bois.",
        "maman|On écoute, même à la dînette ?",
        "enfant-f|J'écoute la maîtresse.",
        "papa|Et le malaise, on le dit ?",
        "enfant-f|Oui. À la maison.",
        "maman|À papa ou à maman.",
        "narrateur|La maîtresse parle encore.",
        "narrateur|Nina écoute, la tasse dans les mains.",
        "papa|Bravo. C'est du bon travail.",
        "maman|Tu as raconté ton malaise.",
        "enfant-f|Merci, maman.",
        "narrateur|La petite casserole reste au calme.",
    )


def q_009(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Nina a un malaise.",
            "narrateur|Que fait-elle ?",
        )
    if i == 2:
        return L(
            "narrateur|Nina raconte à qui ?",
        )
    return L(
        "narrateur|On écoute qui ?",
    )


def c_009(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Oui.",
            "papa|Elle raconte à papa ou maman.",
            "maman|On écoute la maîtresse.",
            "narrateur|Nina respire, tout calme.",
            "papa|Bravo, Nina.",
            "papa|Tu as fait du bon travail.",
            "enfant-f|Merci, papa.",
            "maman|On continue, tout doux.",
        )
    if i == 2:
        return L(
            "narrateur|Oui.",
            "maman|À papa. À maman. À la maison.",
            "papa|On écoute la maîtresse aussi.",
            "narrateur|Nina tient encore le livre.",
            "maman|Bravo.",
            "maman|Tu as raconté le malaise.",
            "enfant-f|Je raconte.",
            "papa|C'est ça.",
        )
    return L(
        "narrateur|Oui.",
        "papa|La maîtresse.",
        "maman|Et si malaise, on raconte à la maison.",
        "narrateur|Nina hoche la tête.",
        "maman|Bravo, Nina.",
        "maman|Tu as fait du bon travail.",
        "enfant-f|Merci, maman.",
    )


def tq2_009() -> list[tuple[str, str]]:
    return L(
        "narrateur|On prend quel goûter ?",
        "maman|Une pomme, un yaourt, ou un morceau de pain.",
    )


def l2_009(i: int, j: int) -> list[tuple[str, str]]:
    pres = TOY_PRES[i]
    if j == 1:
        return L(
            f"narrateur|Nina a choisi une pomme, près {pres}.",
            "narrateur|La pomme est rouge, un peu froide.",
            "narrateur|Un oiseau chante derrière la vitre.",
            "papa|Tu as encore le malaise ?",
            "enfant-f|Un peu. Je raconte.",
            "maman|On écoute la maîtresse.",
            "maman|Puis on raconte à la maison.",
            "papa|Bravo. Tu as dit les mots.",
            "enfant-f|J'écoute. Je raconte.",
            "narrateur|La pomme brille dans sa main.",
            "maman|Le ventre se desserre, tout doux.",
            "papa|On reste ensemble.",
            "narrateur|Une feuille colle encore à la vitre.",
        )
    if j == 2:
        return L(
            f"narrateur|Nina a choisi un yaourt, près {pres}.",
            "narrateur|Le pot est frais, tout lisse.",
            "narrateur|Ça sent le lait, tout doux.",
            "maman|Tu écoutes encore ?",
            "enfant-f|J'écoute la maîtresse.",
            "papa|Et le malaise ?",
            "enfant-f|Je raconte à papa ou maman.",
            "maman|Oui. À la maison aussi.",
            "papa|Bravo, Nina.",
            "narrateur|La cuillère fait un petit clic.",
            "maman|Tu as fait du bon travail.",
            "enfant-f|Merci.",
            f"narrateur|Le pot reste près {pres}.",
        )
    return L(
        f"narrateur|Nina a choisi un morceau de pain, près {pres}.",
        "narrateur|La croûte est un peu chaude.",
        "narrateur|Des miettes tombent sur la table.",
        "papa|On écoute, même avec le pain ?",
        "enfant-f|J'écoute la maîtresse.",
        "maman|Si malaise, tu racontes.",
        "enfant-f|À la maison.",
        "papa|À papa ou à maman.",
        "maman|Bravo. C'est ça.",
        "narrateur|Nina souffle une miette, tout léger.",
        "papa|Tu as écouté. Tu as raconté.",
        "enfant-f|Mon ventre est calme.",
        "narrateur|Le pain reste à sa place.",
    )


def tq3_009() -> list[tuple[str, str]]:
    return L(
        "narrateur|On va voir qui, dans la cour ?",
        "papa|Le chat, le chien, ou la poule.",
    )


OPEN_009 = {
    (1, 1, 1): (
        "Le chat se frotte aux cubes, tout doux.",
        "Une pomme roule, tout près du tapis.",
    ),
    (1, 1, 2): (
        "Le chien pose le museau près de la pomme.",
        "Un cube rouge tremble, tout petit.",
    ),
    (1, 1, 3): (
        "La poule picore à côté d'un cube rouge.",
        "La pomme attend dans la main de Nina.",
    ),
    (1, 2, 1): (
        "Le chat regarde le pot de yaourt, tout calme.",
        "Un cube bleu reste contre sa patte.",
    ),
    (1, 2, 2): (
        "Le chien attend près du pot, la queue douce.",
        "Les cubes font un petit tas.",
    ),
    (1, 2, 3): (
        "La poule fait un petit cot près des cubes.",
        "Le yaourt reste au frais, sur la table.",
    ),
    (1, 3, 1): (
        "Le chat marche entre les miettes, tout léger.",
        "Un cube jaune garde une miette.",
    ),
    (1, 3, 2): (
        "Le chien sent le pain, sans se presser.",
        "Les cubes restent en rang, tout sages.",
    ),
    (1, 3, 3): (
        "La poule picore une miette, près d'un cube.",
        "Le pain sent encore le four.",
    ),
    (2, 1, 1): (
        "Le chat s'assoit sur le livre fermé.",
        "La pomme brille près de la couverture.",
    ),
    (2, 1, 2): (
        "Le chien pose la tête près du livre.",
        "La pomme roule vers la page.",
    ),
    (2, 1, 3): (
        "La poule regarde l'image du livre, de loin.",
        "Nina tient encore sa pomme.",
    ),
    (2, 2, 1): (
        "Le chat ronronne contre le livre ouvert.",
        "Le pot de yaourt est tout froid.",
    ),
    (2, 2, 2): (
        "Le chien écoute, près de la page.",
        "Une goutte de yaourt brille, tout petit.",
    ),
    (2, 2, 3): (
        "La poule picote le sol, loin du livre.",
        "Le yaourt attend sur le rebord.",
    ),
    (2, 3, 1): (
        "Le chat a une miette sur la moustache.",
        "Le livre garde une page ouverte.",
    ),
    (2, 3, 2): (
        "Le chien reste assis pendant l'histoire.",
        "Une miette de pain dort sur la page.",
    ),
    (2, 3, 3): (
        "La poule écoute le livre, tout calme.",
        "Le pain repose près de la reliure.",
    ),
    (3, 1, 1): (
        "Le chat touche la tasse de dînette, du nez.",
        "La pomme sert de gâteau, pour de rire.",
    ),
    (3, 1, 2): (
        "Le chien attend une pomme de dînette.",
        "La petite casserole est tiède.",
    ),
    (3, 1, 3): (
        "La poule passe près de la petite casserole.",
        "Nina pose la pomme dans une assiette.",
    ),
    (3, 2, 1): (
        "Le chat se couche près de la dînette.",
        "Le yaourt fait un goûter de poupée.",
    ),
    (3, 2, 2): (
        "Le chien ne prend pas la petite cuillère.",
        "Le pot de yaourt reste à sa place.",
    ),
    (3, 2, 3): (
        "La poule fait cot cot, près des assiettes.",
        "Le yaourt brille comme de la crème.",
    ),
    (3, 3, 1): (
        "Le chat suit une miette vers la dînette.",
        "Le pain devient un gâteau, tout petit.",
    ),
    (3, 3, 2): (
        "Le chien reste près du pain, tout sage.",
        "La dînette a des miettes sur le bois.",
    ),
    (3, 3, 3): (
        "La poule picore loin de la dînette.",
        "Nina range le pain dans une assiette.",
    ),
}

FIN_IMG_009 = {
    (1, 1, 1): "Le cube rouge a gardé un poil de chat.",
    (1, 1, 2): "La pomme a une petite marque de museau.",
    (1, 1, 3): "Un cube rouge a une plume, tout léger.",
    (1, 2, 1): "Le pot de yaourt est vide, tout propre.",
    (1, 2, 2): "La queue du chien a bougé un cube.",
    (1, 2, 3): "Un cot cot reste dans la classe, tout loin.",
    (1, 3, 1): "Une miette dort encore sur le tapis.",
    (1, 3, 2): "Le pain a tiédi près du radiateur.",
    (1, 3, 3): "La poule a laissé une plume sur un cube.",
    (2, 1, 1): "Le livre a un rond de soleil, tout chaud.",
    (2, 1, 2): "La page a gardé une odeur de pomme.",
    (2, 1, 3): "L'image du livre reste ouverte, tout calme.",
    (2, 2, 1): "Le ronron du chat s'est tu, tout doux.",
    (2, 2, 2): "Le chien a posé la tête, puis dormi.",
    (2, 2, 3): "Une goutte de yaourt a séché sur le rebord.",
    (2, 3, 1): "La moustache du chat n'a plus de miette.",
    (2, 3, 2): "La page sent encore le pain chaud.",
    (2, 3, 3): "La reliure est chaude, près du radiateur.",
    (3, 1, 1): "La petite tasse a un rond de pomme.",
    (3, 1, 2): "La casserole de dînette s'est tue.",
    (3, 1, 3): "L'assiette de dînette brille, vide.",
    (3, 2, 1): "Le chat a laissé un creux près des tasses.",
    (3, 2, 2): "La petite cuillère est rentrée dans la boîte.",
    (3, 2, 3): "Les assiettes de dînette sont en pile.",
    (3, 3, 1): "Une miette reste dans la petite casserole.",
    (3, 3, 2): "Le pain a une marque de dînette, tout drôle.",
    (3, 3, 3): "La dînette rentre dans le carton, tout calme.",
}


def l3_009(i: int, j: int, k: int) -> list[tuple[str, str]]:
    a, b = OPEN_009[(i, j, k)]
    animal = ANIMAL[k]
    return L(
        f"narrateur|{a}",
        f"narrateur|{b}",
        f"narrateur|Nina rejoint {animal}.",
        "narrateur|La cour sent l'herbe et la terre.",
        "enfant-f|J'ai écouté la maîtresse.",
        "enfant-f|J'ai eu un malaise.",
        "enfant-f|Je raconte à la maison.",
        "papa|Tu as bien fait de raconter.",
        "maman|On écoute la maîtresse.",
        "maman|Si malaise, on raconte à papa ou maman.",
        "papa|Bravo, Nina.",
        "papa|C'est du bon travail.",
        "enfant-f|Merci, maman.",
        "enfant-f|Merci, papa.",
        "narrateur|Le ventre de Nina se desserre, tout doucement.",
        f"narrateur|Elle se souvient {TOY_PRES[i]}, et {SNACK_DE[j]}.",
    )


def fin_009(i: int, j: int, k: int) -> list[tuple[str, str]]:
    return L(
        "enfant-f|J'ai écouté.",
        "enfant-f|Puis j'ai raconté.",
        "maman|Bravo, Nina.",
        "papa|Tu as fait du bon travail.",
        f"narrateur|Nina a joué avec {TOY[i]}.",
        f"narrateur|Elle a pris {SNACK[j]}.",
        f"narrateur|Elle a vu {ANIMAL[k]}.",
        f"narrateur|{FIN_IMG_009[(i, j, k)]}",
        "narrateur|L'histoire est finie.",
    )


def build_009(source: dict) -> dict:
    by: dict[str, list[tuple[str, str]]] = {
        "CHK_T0000_P0000": debut_009(),
        "CHK_T0001_P0000": tq1_009(),
    }
    for i in (1, 2, 3):
        by[f"CHK_T0001_P000{i}"] = l1_009(i)
        by[f"CHK_T0001_P000{i}_Q0001"] = q_009(i)
        by[f"CHK_T0001_P000{i}_C0001"] = c_009(i)
        by[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_009()
        for j in (1, 2, 3):
            by[f"CHK_T0001_P000{i}_T0002_P000{j}"] = l2_009(i, j)
            by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"] = tq3_009()
            for k in (1, 2, 3):
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"] = l3_009(i, j, k)
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin_009(i, j, k)
    return write_story(
        "TREE-COL-009",
        {
            "fil_rouge": "Le radiateur tic. Nina accroche son manteau. Elle écoute la maîtresse. Un chuchotement serre son ventre. Elle raconte à papa et maman, puis elle joue.",
            "title": "Le bouton rouge de Nina",
            "characters": "Nina, papa, maman",
            "setting": "à l'école, puis dans la cour",
        },
        by,
    )


# ---------------------------------------------------------------------------
# TREE-COL-010 — Mila, marché, N1
# L1 matin / sieste / soir   L2 cuisine / jardin / chambre   L3 ballon / seau / doudou
# ---------------------------------------------------------------------------

MOM = {1: "le matin", 2: "après la sieste", 3: "le soir"}
ROOM = {1: "la cuisine", 2: "le jardin", 3: "la chambre"}
TOY10 = {1: "le ballon", 2: "le seau", 3: "le doudou"}


def debut_010() -> list[tuple[str, str]]:
    return L(
        "narrateur|La bâche du stand claque, tout doux.",
        "narrateur|Les oranges brillent, toutes rondes.",
        "narrateur|La balance fait clic.",
        "narrateur|Les pavés sont encore froids.",
        "narrateur|Le panier de maman est vide.",
        "narrateur|Il gratte un peu, contre le bras.",
        "narrateur|Les pièces de papa tintent.",
        "narrateur|Ça sent le thym.",
        "narrateur|Ça sent la fraise aussi.",
        "narrateur|Un pigeon picore une miette.",
        "maman|Tu as tes mains au chaud ?",
        "enfant-f|Oui, maman.",
        "papa|Le marché parle, tout bas.",
        "maman|On écoute d'abord.",
        "papa|On lève la main.",
        "papa|On attend.",
        "papa|Puis on parle.",
        "narrateur|En ce moment, Mila tient le panier.",
        "narrateur|Elle veut une orange.",
        "enfant-f|Une orange.",
        "maman|On lève la main, Mila.",
        "narrateur|Mila lève la main.",
        "narrateur|Elle attend.",
        "narrateur|La marchande parle encore.",
        "narrateur|Mila attend encore.",
        "papa|C'est ton tour.",
        "enfant-f|Une orange, s'il te plaît.",
        "maman|Bravo. Tu as attendu.",
        "papa|Puis tu as parlé.",
        "narrateur|L'orange est froide, un peu lisse.",
        "enfant-f|Merci.",
        "papa|Tu as fait du bon travail.",
        "narrateur|Le matin, le marché est pâle.",
        "narrateur|Après la sieste, il est calme.",
        "narrateur|Le soir, les lampes s'allument.",
        "maman|Tu es prête ?",
        "enfant-f|Oui, maman.",
    )


def tq1_010() -> list[tuple[str, str]]:
    return L(
        "narrateur|On va au marché quand ?",
        "maman|Le matin, après la sieste, ou le soir.",
    )


def l1_010(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|C'est le matin, au marché.",
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Les caisses sont encore humides.",
            "narrateur|Mila marche près de maman.",
            "narrateur|Elle veut parler.",
            "narrateur|Elle lève la main.",
            "narrateur|Elle attend.",
            "papa|J'écoute les cerises d'abord.",
            "maman|Puis c'est ton tour, Mila.",
            "enfant-f|Les cerises sont rouges.",
            "papa|Bravo. Tu as attendu.",
            "maman|Puis tu as parlé.",
            "narrateur|Le panier se remplit, tout doux.",
            "papa|On lève la main. On attend.",
            "enfant-f|Puis on parle.",
        )
    if i == 2:
        return L(
            "narrateur|C'est après la sieste.",
            "narrateur|Le marché est calme, un peu chaud.",
            "narrateur|La bâche fait de l'ombre.",
            "narrateur|Mila tient encore son doudou.",
            "narrateur|Elle veut une fraise.",
            "narrateur|Elle lève la main.",
            "narrateur|Elle attend.",
            "maman|J'écoute le pain d'abord.",
            "papa|Ensuite, c'est toi.",
            "enfant-f|Une fraise, s'il te plaît.",
            "maman|Bravo, Mila.",
            "papa|Tu as attendu. Puis parlé.",
            "narrateur|La fraise est tiède, tout douce.",
            "maman|On lève la main.",
            "enfant-f|J'attends. Puis je parle.",
        )
    return L(
        "narrateur|C'est le soir, au marché.",
        "narrateur|Les lampes sont jaunes, tout bas.",
        "narrateur|Les ombres sont longues.",
        "narrateur|Mila a froid aux mains.",
        "narrateur|Elle veut parler.",
        "narrateur|Elle lève la main.",
        "narrateur|Elle attend.",
        "papa|J'écoute les œufs d'abord.",
        "maman|Puis c'est ton tour.",
        "enfant-f|Les lampes sont jaunes.",
        "papa|Bravo. Tu as attendu.",
        "maman|Puis tu as parlé.",
        "narrateur|Le panier est lourd, tout plein.",
        "papa|On lève la main. On attend.",
        "enfant-f|Puis on parle.",
    )


def q_010(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Mila veut parler.",
            "narrateur|Que fait-elle d'abord ?",
        )
    if i == 2:
        return L(
            "narrateur|On lève quoi ?",
        )
    return L(
        "narrateur|On attend, puis on parle ?",
    )


def c_010(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Oui.",
            "maman|Elle lève la main.",
            "papa|Elle attend.",
            "narrateur|Mila respire, tout calme.",
            "maman|Bravo, Mila.",
            "papa|Tu as fait du bon travail.",
            "enfant-f|Merci, papa.",
            "maman|On continue, tout doux.",
        )
    if i == 2:
        return L(
            "narrateur|Oui.",
            "papa|La main.",
            "maman|On lève la main. On attend.",
            "narrateur|Mila lève encore la main.",
            "papa|Bravo.",
            "maman|Puis tu parles.",
            "enfant-f|J'attends.",
            "papa|C'est ça.",
        )
    return L(
        "narrateur|Oui.",
        "maman|On attend.",
        "papa|Puis on parle.",
        "narrateur|Mila hoche la tête.",
        "maman|Bravo, Mila.",
        "papa|Tu as fait du bon travail.",
        "enfant-f|Merci, maman.",
    )


def tq2_010() -> list[tuple[str, str]]:
    return L(
        "narrateur|On rentre où, maintenant ?",
        "papa|La cuisine, le jardin, ou la chambre.",
    )


def l2_010(i: int, j: int) -> list[tuple[str, str]]:
    moment = MOM[i]
    if j == 1:
        return L(
            f"narrateur|Mila a choisi la cuisine, {moment}.",
            "narrateur|Ça sent le pain chaud.",
            "narrateur|La table est un peu farinée.",
            "narrateur|Mila veut parler.",
            "narrateur|Elle lève la main.",
            "narrateur|Elle attend.",
            "papa|Je parle du pain d'abord.",
            "maman|Puis c'est toi, Mila.",
            "enfant-f|Le pain est chaud.",
            "papa|Bravo. Tu as attendu.",
            "maman|Puis tu as parlé.",
            "narrateur|Une miette brille sur le bois.",
            "papa|On lève la main, même à table.",
            "enfant-f|J'attends. Puis je parle.",
        )
    if j == 2:
        return L(
            f"narrateur|Mila a choisi le jardin, {moment}.",
            "narrateur|Le vent est doux, un peu frais.",
            "narrateur|Une feuille tourne, tout lent.",
            "narrateur|Mila veut parler.",
            "narrateur|Elle lève la main.",
            "narrateur|Elle attend.",
            "maman|Je parle du vent d'abord.",
            "papa|Ensuite, c'est toi.",
            "enfant-f|La feuille tourne.",
            "maman|Bravo, Mila.",
            "papa|Tu as attendu. Puis parlé.",
            "narrateur|L'herbe est un peu mouillée.",
            "maman|On lève la main, même dehors.",
            "enfant-f|Puis on parle.",
        )
    return L(
        f"narrateur|Mila a choisi la chambre, {moment}.",
        "narrateur|Le plaid est doux, tout chaud.",
        "narrateur|La lampe fait un rond jaune.",
        "narrateur|Mila veut parler.",
        "narrateur|Elle lève la main.",
        "narrateur|Elle attend.",
        "papa|Je parle de la lampe d'abord.",
        "maman|Puis c'est ton tour.",
        "enfant-f|Le plaid est doux.",
        "papa|Bravo. Tu as attendu.",
        "maman|Puis tu as parlé.",
        "narrateur|Le doudou attend sur l'oreiller.",
        "papa|On lève la main, même ici.",
        "enfant-f|J'attends. Puis je parle.",
    )


def tq3_010() -> list[tuple[str, str]]:
    return L(
        "narrateur|On prend quel jouet ?",
        "maman|Le ballon, le seau, ou le doudou.",
    )


OPEN_010 = {
    (1, 1, 1): (
        "Le ballon roule vers la table, tout doux.",
        "Une miette de pain l'arrête.",
    ),
    (1, 1, 2): (
        "Le seau pose près de l'évier.",
        "L'eau fait un tout petit bruit.",
    ),
    (1, 1, 3): (
        "Le doudou s'assoit sur la chaise.",
        "Ça sent encore le pain.",
    ),
    (1, 2, 1): (
        "Le ballon glisse dans l'herbe froide.",
        "Une goutte d'eau brille dessus.",
    ),
    (1, 2, 2): (
        "Le seau attend près du bac.",
        "Le vent pousse une feuille dedans.",
    ),
    (1, 2, 3): (
        "Le doudou a un peu d'herbe au pied.",
        "Le jardin sent la terre mouillée.",
    ),
    (1, 3, 1): (
        "Le ballon dort sous le lit.",
        "Un rayon touche sa rondeur.",
    ),
    (1, 3, 2): (
        "Le seau est près de la commode.",
        "Il est vide, tout calme.",
    ),
    (1, 3, 3): (
        "Le doudou est déjà sur l'oreiller.",
        "Le plaid le recouvre, tout doux.",
    ),
    (2, 1, 1): (
        "Le ballon est tiède, après la sieste.",
        "Il roule vers la miette.",
    ),
    (2, 1, 2): (
        "Le seau a gardé un peu d'eau.",
        "La cuisine est encore calme.",
    ),
    (2, 1, 3): (
        "Le doudou sent le pain chaud.",
        "Il a un pli, après la sieste.",
    ),
    (2, 2, 1): (
        "Le ballon rebondit, tout bas, dans l'herbe.",
        "L'ombre de la bâche n'est plus là.",
    ),
    (2, 2, 2): (
        "Le seau est chaud, au soleil.",
        "Une abeille passe, tout loin.",
    ),
    (2, 2, 3): (
        "Le doudou sèche un peu, dehors.",
        "Une feuille s'y pose, tout léger.",
    ),
    (2, 3, 1): (
        "Le ballon a une marque d'oreiller.",
        "La chambre est encore un peu sombre.",
    ),
    (2, 3, 2): (
        "Le seau attend au pied du lit.",
        "Le volet est à moitié ouvert.",
    ),
    (2, 3, 3): (
        "Le doudou a chaud, sous le plaid.",
        "La sieste sent encore la chambre.",
    ),
    (3, 1, 1): (
        "Le ballon brille sous la lampe.",
        "La cuisine est jaune, tout doux.",
    ),
    (3, 1, 2): (
        "Le seau pose près de la soupe.",
        "La vapeur fait un nuage.",
    ),
    (3, 1, 3): (
        "Le doudou a une miette sur l'oreille.",
        "La tasse de papa fume.",
    ),
    (3, 2, 1): (
        "Le ballon se cache dans l'ombre du soir.",
        "Un grillon chante, tout loin.",
    ),
    (3, 2, 2): (
        "Le seau est froid, le soir.",
        "La terre du jardin sent fort.",
    ),
    (3, 2, 3): (
        "Le doudou rentre du jardin, tout sage.",
        "Une étoile apparaît, tout petit.",
    ),
    (3, 3, 1): (
        "Le ballon roule vers la lampe.",
        "Le soir est calme, dans la chambre.",
    ),
    (3, 3, 2): (
        "Le seau rentre sous le lit.",
        "La lampe fait un rond sur le bois.",
    ),
    (3, 3, 3): (
        "Le doudou ferme les yeux, presque.",
        "Le plaid sent encore le marché.",
    ),
}

FIN_IMG_010 = {
    (1, 1, 1): "L'orange brille encore, près du ballon.",
    (1, 1, 2): "Une goutte sèche sur le bord du seau.",
    (1, 1, 3): "Le doudou a gardé l'odeur du thym.",
    (1, 2, 1): "L'herbe a un creux, tout rond.",
    (1, 2, 2): "Le seau a une feuille collée.",
    (1, 2, 3): "Le doudou a un brin d'herbe.",
    (1, 3, 1): "Le ballon dort, sous le lit.",
    (1, 3, 2): "Le seau est rentré, tout vide.",
    (1, 3, 3): "Le doudou est chaud, sous le plaid.",
    (2, 1, 1): "Le pain a tiédi, près du ballon.",
    (2, 1, 2): "Le seau a un fond d'eau, tout calme.",
    (2, 1, 3): "Le doudou a un pli de sieste.",
    (2, 2, 1): "Le ballon a une tache d'herbe.",
    (2, 2, 2): "Le seau sent encore le soleil.",
    (2, 2, 3): "Une feuille reste sur le doudou.",
    (2, 3, 1): "Le ballon a un rond d'oreiller.",
    (2, 3, 2): "Le seau attend au pied du lit.",
    (2, 3, 3): "Le plaid recouvre le doudou.",
    (3, 1, 1): "La lampe pose un rond sur le ballon.",
    (3, 1, 2): "La vapeur a quitté le seau.",
    (3, 1, 3): "La miette a quitté le doudou.",
    (3, 2, 1): "Le grillon s'est tu, tout loin.",
    (3, 2, 2): "Le seau a de la terre au fond.",
    (3, 2, 3): "Une étoile reste à la fenêtre.",
    (3, 3, 1): "Le ballon est jaune, sous la lampe.",
    (3, 3, 2): "Le seau a disparu sous le lit.",
    (3, 3, 3): "Le doudou sent encore les oranges.",
}


def l3_010(i: int, j: int, k: int) -> list[tuple[str, str]]:
    a, b = OPEN_010[(i, j, k)]
    toy = TOY10[k]
    room = ROOM[j]
    moment = MOM[i]
    return L(
        f"narrateur|{a}",
        f"narrateur|{b}",
        f"narrateur|Mila rejoint {toy}.",
        f"narrateur|On est dans {room}, {moment}.",
        "narrateur|Mila veut parler.",
        "narrateur|Elle lève la main.",
        "narrateur|Elle attend.",
        "papa|C'est ton tour, Mila.",
        "enfant-f|J'ai levé la main.",
        "enfant-f|J'ai attendu.",
        "enfant-f|Puis j'ai parlé.",
        "maman|Bravo, Mila.",
        "papa|Tu as fait du bon travail.",
        "maman|On lève la main. On attend.",
        "papa|Puis on parle.",
        "enfant-f|Merci, maman.",
        "enfant-f|Merci, papa.",
        "narrateur|Le panier du marché repose, tout plein.",
    )


def fin_010(i: int, j: int, k: int) -> list[tuple[str, str]]:
    return L(
        "enfant-f|J'ai levé la main.",
        "enfant-f|J'ai attendu. Puis parlé.",
        "maman|Bravo, Mila.",
        "papa|Tu as fait du bon travail.",
        f"narrateur|Mila est allée au marché, {MOM[i]}.",
        f"narrateur|Elle a vu {ROOM[j]}.",
        f"narrateur|Elle a pris {TOY10[k]}.",
        f"narrateur|{FIN_IMG_010[(i, j, k)]}",
        "narrateur|L'histoire est finie.",
    )


def build_010(source: dict) -> dict:
    by: dict[str, list[tuple[str, str]]] = {
        "CHK_T0000_P0000": debut_010(),
        "CHK_T0001_P0000": tq1_010(),
    }
    for i in (1, 2, 3):
        by[f"CHK_T0001_P000{i}"] = l1_010(i)
        by[f"CHK_T0001_P000{i}_Q0001"] = q_010(i)
        by[f"CHK_T0001_P000{i}_C0001"] = c_010(i)
        by[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_010()
        for j in (1, 2, 3):
            by[f"CHK_T0001_P000{i}_T0002_P000{j}"] = l2_010(i, j)
            by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"] = tq3_010()
            for k in (1, 2, 3):
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"] = l3_010(i, j, k)
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin_010(i, j, k)
    return write_story(
        "TREE-COL-010",
        {
            "fil_rouge": "La balance du marché fait clic. Mila lève la main. Elle attend. Puis elle parle, pour une orange.",
            "title": "La balance et les oranges de Mila",
            "characters": "Mila, maman, papa",
            "setting": "au marché, puis à la maison",
        },
        by,
    )


def main() -> None:
    all_err: list[str] = []
    jobs = (
        ("TREE-COL-009", build_009, ["écout", "malaise", "maison"], 18),
        ("TREE-COL-010", build_010, ["attend", "main", "parler"], 10),
    )
    for sid, builder, needles, maxw in jobs:
        src = json.loads((ROOT / sid / "source.json").read_text(encoding="utf-8"))
        data = builder(src)
        err = check_story(data, needles, maxw)
        print(sid, "chunks", len(data["chunks"]))
        print("  debut:", data["chunks"][0]["text"][:90])
        if err:
            print("  ERRORS", len(err))
            for e in err[:50]:
                print("   -", e)
            all_err.extend(f"{sid}: {e}" for e in err)
        else:
            print("  OK")
    if all_err:
        raise SystemExit(f"{len(all_err)} erreurs")


if __name__ == "__main__":
    main()
