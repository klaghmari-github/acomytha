#!/usr/bin/env python3
"""F-NAR-009 — réécriture TREE-COL-011 et TREE-COL-012 (texte seulement)."""
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
MAX_WORDS_N2 = 16
NEEDLES = ("bonjour", "s'il te plaît", "merci")

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
    "Cet",
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
    "Que",
    "Qui",
    "Quoi",
    "Ça",
    "Ca",
    "Son",
    "Sa",
    "Ses",
    "Toi",
    "Moi",
    "Lui",
    "Eux",
    "Elles",
    "Ils",
    "Trois",
    "Deux",
    "Maîtresse",
    "Tom",
    "Léa",
    "Sami",
    "Où",
}


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    script = "\n".join(f"{role}|{phrase}" for role, phrase in lines)
    text = " ".join(phrase for _, phrase in lines)
    return text, script


def apply_chunk(src: dict, lines: list[tuple[str, str]], sons: str | None = None) -> dict:
    text, script = pack(lines)
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    out["sons"] = "" if sons is None else sons
    return out


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str],
) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:12]} extra={extra[:12]}")
    chunks = []
    for c in source["chunks"]:
        cid = c["chunk_id"]
        chunks.append(apply_chunk(c, by_id[cid], sons_map.get(cid, "")))
    merged = dict(source)
    merged.update(meta)
    merged["chunks"] = chunks
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def check_story(data: dict, extra_names=()) -> list[str]:
    errors: list[str] = []
    by = {c["chunk_id"]: c for c in data["chunks"]}
    if len(data["chunks"]) != 86:
        errors.append(f"n_chunks={len(data['chunks'])}")
    allowed = TROUPE | set(extra_names)
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
            if n > MAX_WORDS_N2:
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
                r"^(Raphaël|Amir|Nino|Mila|Nina|Victorino|Aniss|Sarah|Chouchou|Victorina)\s+(est|joue|sort|tient)",
                first,
            ):
                errors.append(f"{c['chunk_id']} entrée brutale: {first}")
            roles = {ln.split("|", 1)[0] for ln in lines}
            if "papa" not in roles and "maman" not in roles:
                errors.append(f"{c['chunk_id']} pas d'adulte")
        blob = text
        for name in re.findall(r"\b([A-ZÉÈÊÀÂÎÔÙÛÇ][a-zéèêàâîôùûçëïü]+)\b", blob):
            if name in SKIP_NAMES or name in allowed:
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
                for needle in NEEDLES:
                    if needle.lower() not in blob.lower():
                        errors.append(f"path {i}{j}{k} manque {needle}")
                if words(blob) < 350:
                    errors.append(f"path {i}{j}{k} trop court {words(blob)}")
                fin = by[path[-1]]["text"]
                if "L'histoire est finie." not in fin:
                    errors.append(f"{path[-1]} sans clôture")
    return errors


# ---------------------------------------------------------------------------
# TREE-COL-011 — Victorino, gare, train, petit parc
# L1 bac à sable / toboggan / balançoires
# L2 cubes / livre / dînette
# L3 Tom / Léa / Sami
# ---------------------------------------------------------------------------

LOC_011 = {
    1: ("le bac à sable", "près du bac à sable", "du bac à sable"),
    2: ("le toboggan", "près du toboggan", "du toboggan"),
    3: ("les balançoires", "près des balançoires", "des balançoires"),
}
TOY_011 = {
    1: ("les cubes", "les cubes"),
    2: ("le livre", "le livre"),
    3: ("la dînette", "la dînette"),
}
PEL_011 = {
    1: ("Tom", "l'ours Tom", "ours"),
    2: ("Léa", "la poupée Léa", "poupée"),
    3: ("Sami", "le lion Sami", "lion"),
}

EXTRA_L2_011 = {
    (1, 1): "Un cube jaune s'enfonce un peu dans le sable.",
    (1, 2): "Un grain de sable reste sur la couverture.",
    (1, 3): "Une tasse de dînette se pose sur le bois.",
    (2, 1): "Les cubes s'empilent au pied de la rampe.",
    (2, 2): "Le livre reste à plat, sur une marche.",
    (2, 3): "La petite casserole sonne, tout léger.",
    (3, 1): "Un cube roule sous le siège, tout lent.",
    (3, 2): "Le livre s'ouvre sur le bois mouillé.",
    (3, 3): "Une assiette de dînette attend sur le banc.",
}

EXTRA_L3_011 = {
    (1, 1, 1): "L'ours a du sable sur le ventre, tout fin.",
    (1, 1, 2): "La poupée a un cube contre la robe.",
    (1, 1, 3): "Le lion a un cube jaune dans la crinière.",
    (1, 2, 1): "L'ours écoute le livre, une oreille pliée.",
    (1, 2, 2): "La poupée a un dessin de bac, tout bleu.",
    (1, 2, 3): "Le lion pose une patte sur la page.",
    (1, 3, 1): "L'ours a une tasse minuscule, trop petite.",
    (1, 3, 2): "La poupée tient une cuillère de dînette.",
    (1, 3, 3): "Le lion a une assiette ronde, tout carton.",
    (2, 1, 1): "L'ours est assis en bas de la rampe.",
    (2, 1, 2): "La poupée a une feuille sur le chapeau.",
    (2, 1, 3): "Le lion regarde le métal, tout calme.",
    (2, 2, 1): "L'ours a le livre sur les genoux.",
    (2, 2, 2): "La poupée tourne une page, tout doux.",
    (2, 2, 3): "Le lion a un ticket de papier, tout plié.",
    (2, 3, 1): "L'ours sent la petite casserole, tout chaud.",
    (2, 3, 2): "La poupée verse de l'eau imaginaire.",
    (2, 3, 3): "Le lion a une miette sur la laine.",
    (3, 1, 1): "L'ours se balance un tout petit peu.",
    (3, 1, 2): "La poupée a une chaîne de papier.",
    (3, 1, 3): "Le lion est calé contre le poteau.",
    (3, 2, 1): "L'ours a une histoire de balançoire.",
    (3, 2, 2): "La poupée lit, les pieds qui bougent.",
    (3, 2, 3): "Le lion écoute le cliquetis, tout sage.",
    (3, 3, 1): "L'ours a une tasse, près de la chaîne.",
    (3, 3, 2): "La poupée sert le goûter, tout sérieux.",
    (3, 3, 3): "Le lion a une assiette sur les pattes.",
}

FIN_IMG_011 = {
    (1, 1, 1): "Le sable retombe, tout fin, sur le bois.",
    (1, 1, 2): "Un cube reste dans le sac, tout jaune.",
    (1, 1, 3): "L'oreille de l'ours sèche au vent.",
    (1, 2, 1): "La couverture du livre a un grain.",
    (1, 2, 2): "La page reste ouverte, tout calme.",
    (1, 2, 3): "Le sac de toile sent encore le sable.",
    (1, 3, 1): "La petite tasse rentre dans le sac.",
    (1, 3, 2): "La cuillère de dînette fait un clic.",
    (1, 3, 3): "Le bois du bac reste un peu humide.",
    (2, 1, 1): "Une feuille glisse au pied de la rampe.",
    (2, 1, 2): "Le métal du toboggan redevient silencieux.",
    (2, 1, 3): "Les cubes rentrent, un par un.",
    (2, 2, 1): "Le livre se ferme, tout doux.",
    (2, 2, 2): "Une marche reste brillante, après la pluie.",
    (2, 2, 3): "Le manteau jaune sent encore le quai.",
    (2, 3, 1): "La petite casserole ne sonne plus.",
    (2, 3, 2): "Une goutte sèche sur la rampe.",
    (2, 3, 3): "Le thermos attend, dans le sac de papa.",
    (3, 1, 1): "La chaîne de la balançoire s'arrête.",
    (3, 1, 2): "Le siège de bois reste un peu sombre.",
    (3, 1, 3): "Un cube a roulé, puis il est rentré.",
    (3, 2, 1): "Le livre a une page un peu ondulée.",
    (3, 2, 2): "Le vent pousse encore la chaîne, tout bas.",
    (3, 2, 3): "La vitre du train s'embue de nouveau.",
    (3, 3, 1): "L'assiette de dînette rentre dans le sac.",
    (3, 3, 2): "Le banc du parc sèche au soleil.",
    (3, 3, 3): "Le ticket orange brille dans la poche.",
}


def debut_011() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Le toit de la gare goutte, tout doux."),
        ("narrateur", "Le banc de bois est encore mouillé."),
        ("narrateur", "Ça sent la soupe dans le thermos."),
        ("papa", "Tu as tes chaussettes sèches, Victorino ?"),
        ("enfant-m", "Oui, papa."),
        ("maman", "Le ticket est dans ma poche."),
        ("maman", "Tu l'as vu ?"),
        ("enfant-m", "Il est orange."),
        ("narrateur", "Une gouttière chante le long du quai."),
        ("narrateur", "Les roues du train font un long souffle."),
        ("narrateur", "La vitre est toute embuée."),
        ("narrateur", "Victorino dessine un rond du doigt."),
        ("papa", "On voit le village, derrière."),
        ("maman", "Un petit parc, tout près des rails."),
        ("narrateur", "En ce moment, Victorino est dans le train."),
        ("narrateur", "Son manteau jaune sent la pluie."),
        ("narrateur", "Le sac de toile est à ses pieds."),
        ("maman", "On dit bonjour, d'accord ?"),
        ("enfant-m", "Bonjour."),
        ("papa", "Et si tu veux le thermos ?"),
        ("enfant-m", "S'il te plaît."),
        ("maman", "Bravo."),
        ("papa", "Et après ?"),
        ("enfant-m", "Merci."),
        ("papa", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "Le sac cache des cubes, un livre, une dînette."),
        ("narrateur", "Trois peluches regardent, tout calmes."),
        ("maman", "Tom, Léa et Sami voyagent avec nous."),
        ("enfant-m", "Je les entends."),
        ("papa", "Toi, tu connais les mots gentils."),
        ("enfant-m", "Oui, papa."),
        ("narrateur", "Une perle d'eau court sur la vitre."),
        ("maman", "On descend tout à l'heure."),
        ("enfant-m", "Oui, maman."),
    ]


def tq1_011() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Qu'est-ce que Victorino rejoint ?"),
        ("maman", "Le bac à sable, le toboggan, ou les balançoires."),
    ]


def l1_011(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "Le train s'arrête, tout long."),
            ("narrateur", "Victorino descend vers le bac à sable."),
            ("narrateur", "Le bois du bord est froid, un peu rugueux."),
            ("narrateur", "Le sable est sombre, après la pluie."),
            ("enfant-m", "Bonjour, petit parc."),
            ("papa", "Bonjour, Victorino."),
            ("maman", "Tu veux le seau, dans le sac ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le seau est rouge, un peu rayé."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les trois mots."),
            ("maman", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Une flaque brille au bord du bac."),
        ]
    if i == 2:
        return [
            ("narrateur", "Victorino va vers le toboggan."),
            ("narrateur", "Le métal est lisse, un peu froid."),
            ("narrateur", "Une feuille jaune reste sur une marche."),
            ("papa", "Bonjour, mon grand."),
            ("enfant-m", "Bonjour, papa."),
            ("maman", "Tu veux ma main, pour la rampe ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "La rampe est humide, toute fine."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo, Victorino."),
            ("maman", "Les mots gentils, même au toboggan."),
            ("papa", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Un oiseau passe au-dessus des rails."),
        ]
    return [
        ("narrateur", "Victorino rejoint les balançoires."),
        ("narrateur", "La chaîne fait un petit cliquetis."),
        ("narrateur", "Le siège de bois est encore sombre."),
        ("maman", "Bonjour, Victorino."),
        ("enfant-m", "Bonjour, maman."),
        ("papa", "Tu veux un coup de chiffon, sur le siège ?"),
        ("enfant-m", "S'il te plaît."),
        ("narrateur", "Le chiffon sent le savon, tout doux."),
        ("enfant-m", "Merci, papa."),
        ("maman", "Bravo."),
        ("maman", "Tu as demandé, puis remercié."),
        ("papa", "On dit aussi bonjour."),
        ("enfant-m", "Bonjour."),
        ("narrateur", "Le vent pousse la chaîne, tout bas."),
    ]


def q_011(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [("narrateur", "On dit bonjour, s'il te plaît, merci ?")]
    if i == 2:
        return [
            ("narrateur", "Victorino veut la main de maman."),
            ("papa", "Que dit-il ?"),
        ]
    return [
        ("narrateur", "Victorino a le chiffon."),
        ("maman", "On dit merci ?"),
    ]


def c_011(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "Oui."),
            ("maman", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Victorino pose le seau, tout calme."),
            ("papa", "Bravo, Victorino."),
            ("papa", "Tu as fait du bon travail."),
            ("enfant-m", "Merci, papa."),
            ("maman", "On continue, tout doux."),
        ]
    if i == 2:
        return [
            ("narrateur", "Oui."),
            ("papa", "On dit s'il te plaît."),
            ("maman", "Et bonjour. Et merci."),
            ("narrateur", "Victorino tient la rampe, tout léger."),
            ("papa", "Bravo."),
            ("papa", "Tu as demandé gentiment."),
            ("enfant-m", "S'il te plaît."),
            ("maman", "C'est ça."),
        ]
    return [
        ("narrateur", "Oui."),
        ("maman", "On dit merci."),
        ("papa", "Et bonjour. Et s'il te plaît."),
        ("narrateur", "Victorino hoche la tête."),
        ("maman", "Bravo, Victorino."),
        ("maman", "Tu as fait du bon travail."),
        ("enfant-m", "Merci, maman."),
    ]


def tq2_011() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Qu'est-ce qu'on sort du sac ?"),
        ("papa", "Les cubes, le livre, ou la dînette."),
    ]


def l2_011(i: int, j: int) -> list[tuple[str, str]]:
    _, loc, _ = LOC_011[i]
    extra = EXTRA_L2_011[(i, j)]
    if j == 1:
        return [
            ("narrateur", f"Victorino sort les cubes, {loc}."),
            ("narrateur", "Le bois des cubes est lisse, un peu froid."),
            ("narrateur", extra),
            ("enfant-m", "Bonjour, cubes."),
            ("papa", "Bonjour."),
            ("maman", "Tu veux le cube jaune ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le jaune est plus chaud, au soleil."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo. Tu as dit les mots."),
            ("maman", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Une tour toute petite tient, un moment."),
        ]
    if j == 2:
        return [
            ("narrateur", f"Victorino ouvre le livre, {loc}."),
            ("narrateur", "La couverture est un peu ondulée."),
            ("narrateur", extra),
            ("enfant-m", "Bonjour, livre."),
            ("maman", "Bonjour."),
            ("papa", "Tu veux que je tourne la page ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le papier sent encore la maison."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo, Victorino."),
            ("papa", "Les mots gentils, même pour un livre."),
            ("narrateur", "Un dessin de train apparaît, tout bleu."),
        ]
    return [
        ("narrateur", f"Victorino pose la dînette, {loc}."),
        ("narrateur", "Une tasse minuscule sonne, tout clair."),
        ("narrateur", extra),
        ("enfant-m", "Bonjour, dînette."),
        ("maman", "Bonjour."),
        ("papa", "Tu veux la petite casserole ?"),
        ("enfant-m", "S'il te plaît."),
        ("narrateur", "Le métal est froid, tout léger."),
        ("enfant-m", "Merci, papa."),
        ("maman", "Bravo."),
        ("maman", "Tu as demandé, puis remercié."),
        ("papa", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "Une goutte sèche sur le bord de l'assiette."),
    ]


def tq3_011() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Qui sort encore du sac ?"),
        ("maman", "Tom, Léa, ou Sami."),
    ]


def l3_011(i: int, j: int, k: int) -> list[tuple[str, str]]:
    nom, np, _kind = PEL_011[k]
    extra = EXTRA_L3_011[(i, j, k)]
    toy = TOY_011[j][0]
    _, loc, _ = LOC_011[i]
    if k == 1:
        return [
            ("narrateur", f"Victorino rejoint {np}, {loc}."),
            ("narrateur", "L'ours est brun, un peu râpé."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("narrateur", extra),
            ("enfant-m", f"Bonjour, {nom}."),
            ("papa", "Bonjour, Tom."),
            ("maman", f"Tu veux {toy} près de lui ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "L'ours s'assoit, tout sage."),
            ("enfant-m", "Merci, maman."),
            ("papa", "Bravo."),
            ("papa", "Tu as dit les trois mots."),
            ("maman", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Victorino caresse l'oreille de l'ours."),
        ]
    if k == 2:
        return [
            ("narrateur", f"Victorino rejoint {np}, {loc}."),
            ("narrateur", "La robe est bleue, un peu froissée."),
            ("narrateur", "Un bouton brille, tout petit."),
            ("narrateur", extra),
            ("enfant-m", f"Bonjour, {nom}."),
            ("maman", "Bonjour, Léa."),
            ("papa", "Tu veux l'asseoir près de toi ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "La poupée a les pieds froids, tout plastique."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo, Victorino."),
            ("papa", "Les mots gentils, pour Léa aussi."),
            ("narrateur", "Victorino lisse la robe bleue."),
        ]
    return [
        ("narrateur", f"Victorino rejoint {np}, {loc}."),
        ("narrateur", "La crinière est en laine, un peu mêlée."),
        ("narrateur", "Un œil de bouton regarde, tout calme."),
        ("narrateur", extra),
        ("enfant-m", f"Bonjour, {nom}."),
        ("papa", "Bonjour, Sami."),
        ("maman", "Tu veux ranger une mèche ?"),
        ("enfant-m", "S'il te plaît."),
        ("narrateur", "La laine est douce, un peu mêlée."),
        ("enfant-m", "Merci, maman."),
        ("papa", "Bravo."),
        ("maman", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "Le lion reste contre le sac de toile."),
    ]


def fin_011(i: int, j: int, k: int) -> list[tuple[str, str]]:
    place = LOC_011[i][0]
    toy = TOY_011[j][0]
    nom = PEL_011[k][0]
    img = FIN_IMG_011[(i, j, k)]
    return [
        ("narrateur", f"Victorino a joué {LOC_011[i][1]}."),
        ("narrateur", f"Il avait {toy}, et {nom} tout près."),
        ("narrateur", img),
        ("papa", "Tu as dit bonjour."),
        ("maman", "Tu as dit s'il te plaît."),
        ("papa", "Et merci."),
        ("maman", "Bravo, Victorino."),
        ("maman", "Tu as fait du bon travail."),
        ("enfant-m", "Merci, maman."),
        ("papa", "On remonte dans le train, mon grand."),
        ("narrateur", "L'histoire est finie."),
    ]


def story_011() -> None:
    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}
    by["CHK_T0000_P0000"] = debut_011()
    sons["CHK_T0000_P0000"] = "pluie,train"
    by["CHK_T0001_P0000"] = tq1_011()
    sons["CHK_T0001_P0000"] = ""
    l1_sons = {1: "sable", 2: "", 3: ""}
    l2_sons = {1: "cubes", 2: "", 3: "assiette"}
    for i in (1, 2, 3):
        by[f"CHK_T0001_P000{i}"] = l1_011(i)
        sons[f"CHK_T0001_P000{i}"] = l1_sons[i]
        by[f"CHK_T0001_P000{i}_Q0001"] = q_011(i)
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        by[f"CHK_T0001_P000{i}_C0001"] = c_011(i)
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        by[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_011()
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""
        for j in (1, 2, 3):
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            by[cid2] = l2_011(i, j)
            sons[cid2] = l2_sons[j]
            by[f"{cid2}_T0003_P0000"] = tq3_011()
            sons[f"{cid2}_T0003_P0000"] = ""
            for k in (1, 2, 3):
                cid3 = f"{cid2}_T0003_P000{k}"
                by[cid3] = l3_011(i, j, k)
                sons[cid3] = ""
                by[f"{cid3}_F0001"] = fin_011(i, j, k)
                sons[f"{cid3}_F0001"] = "train"
    write_story(
        "TREE-COL-011",
        {
            "fil_rouge": (
                "La vitre du train est embuée. Victorino dessine un rond. "
                "Au petit parc près des rails, il dit bonjour, s'il te plaît, merci."
            ),
            "title": "La vitre embuée de Victorino",
            "characters": "Victorino, papa, maman",
            "setting": "gare, train, puis petit parc près des rails",
        },
        by,
        sons,
    )


# ---------------------------------------------------------------------------
# TREE-COL-012 — Aniss, marché
# L1 boulangerie / étal / fromagerie
# L2 boulangère / voisin / maîtresse
# L3 pain / pomme / fromage
# ---------------------------------------------------------------------------

LIEU_012 = {
    1: ("la boulangerie", "à la boulangerie"),
    2: ("l'étal des fruits", "à l'étal des fruits"),
    3: ("la fromagerie", "à la fromagerie"),
}
QUI_012 = {
    1: ("la boulangère", "près de la boulangère"),
    2: ("le voisin", "près du voisin"),
    3: ("la maîtresse", "près de la maîtresse"),
}
OBJ_012 = {
    1: ("le pain", "le pain"),
    2: ("une pomme", "une pomme"),
    3: ("un fromage", "un fromage"),
}

EXTRA_L2_012 = {
    (1, 1): "De la farine blanche reste sur le tablier.",
    (1, 2): "Le voisin tient un sachet déjà tiède.",
    (1, 3): "La maîtresse choisit un petit pain doré.",
    (2, 1): "La boulangère pèse une poire, tout doux.",
    (2, 2): "Le voisin prend une fraise, encore mouillée.",
    (2, 3): "La maîtresse choisit des fraises, tout rouge.",
    (3, 1): "La boulangère sent le lait, tout calme.",
    (3, 2): "Le voisin goûte un tout petit bout.",
    (3, 3): "La maîtresse attend près du comptoir frais.",
}

EXTRA_L3_012 = {
    (1, 1, 1): "Le pain est chaud, dans le papier rêche.",
    (1, 1, 2): "Une pomme brille, près des croûtes dorées.",
    (1, 1, 3): "Le fromage sent le lait, à côté du four.",
    (1, 2, 1): "Le voisin glisse le pain dans son filet.",
    (1, 2, 2): "Le voisin a une pomme, tout lisse.",
    (1, 2, 3): "Le voisin a un fromage, tout blanc.",
    (1, 3, 1): "La maîtresse a le pain contre le cartable.",
    (1, 3, 2): "La maîtresse a une pomme dans la poche.",
    (1, 3, 3): "La maîtresse a un fromage, tout frais.",
    (2, 1, 1): "Le pain dore, près des caisses de fruits.",
    (2, 1, 2): "La pomme est rouge, encore un peu humide.",
    (2, 1, 3): "Le fromage est posé loin des fraises.",
    (2, 2, 1): "Le voisin a du pain, et une poire.",
    (2, 2, 2): "Le voisin choisit une pomme, tout ronde.",
    (2, 2, 3): "Le voisin a un fromage, près des cerises.",
    (2, 3, 1): "La maîtresse a le pain, et des fraises.",
    (2, 3, 2): "La maîtresse pèse une pomme, tout doux.",
    (2, 3, 3): "La maîtresse a un fromage, tout pâle.",
    (3, 1, 1): "Le pain reste au chaud, loin du lait.",
    (3, 1, 2): "Une pomme attend sur le marbre froid.",
    (3, 1, 3): "Le fromage est blanc, un peu tendre.",
    (3, 2, 1): "Le voisin a le pain, près du comptoir.",
    (3, 2, 2): "Le voisin pose une pomme, tout loin.",
    (3, 2, 3): "Le voisin a un fromage, tout rond.",
    (3, 3, 1): "La maîtresse a le pain, tout contre elle.",
    (3, 3, 2): "La maîtresse a une pomme, tout brillante.",
    (3, 3, 3): "La maîtresse a un fromage, tout frais.",
}

# fix accidental paren in (3,3,1) - I'll write the dict correctly without the typo
FIN_IMG_012 = {
    (1, 1, 1): "Le papier du pain reste tiède, dans le filet.",
    (1, 1, 2): "La pomme roule un peu, puis s'arrête.",
    (1, 1, 3): "Le fromage sent le lait, tout doux.",
    (1, 2, 1): "Le sachet du voisin fait un bruit de papier.",
    (1, 2, 2): "Une croûte dore encore, derrière la vitre.",
    (1, 2, 3): "La cloche de la porte fait ding, encore.",
    (1, 3, 1): "Le cartable de la maîtresse est un peu lourd.",
    (1, 3, 2): "La farine reste blanche, sur le bois.",
    (1, 3, 3): "L'air chaud de la boutique caresse les joues.",
    (2, 1, 1): "Une fraise brille encore, dans la caisse.",
    (2, 1, 2): "La balance fait un petit clic.",
    (2, 1, 3): "Le filet de maman s'alourdit, tout doux.",
    (2, 2, 1): "Une poire reste verte, près de la pomme.",
    (2, 2, 2): "L'eau tremble encore dans l'ornière.",
    (2, 2, 3): "La bâche claque, au-dessus des caisses.",
    (2, 3, 1): "Les fraises sentent le sucre, tout bas.",
    (2, 3, 2): "Un pigeon picore plus loin, tout calme.",
    (2, 3, 3): "Le soleil revient sur les fruits rouges.",
    (3, 1, 1): "Le marbre de la fromagerie reste froid.",
    (3, 1, 2): "Le papier blanc fait un bruit doux.",
    (3, 1, 3): "Ça sent le lait, tout près du filet.",
    (3, 2, 1): "Le voisin range son sachet, tout sage.",
    (3, 2, 2): "Une pièce tinte, dans le porte-monnaie.",
    (3, 2, 3): "Le thym sent encore, sur le pavé.",
    (3, 3, 1): "La maîtresse dit au revoir, tout bas.",
    (3, 3, 2): "Le filet frotte la jambe, un peu rêche.",
    (3, 3, 3): "La maison n'est plus très loin, maintenant.",
}


def debut_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Une bâche claque au-dessus des caisses."),
        ("narrateur", "Une fraise brille, encore mouillée."),
        ("narrateur", "L'eau tremble dans une ornière."),
        ("papa", "Tu entends les pièces, Aniss ?"),
        ("maman", "Elles font tic, dans le porte-monnaie."),
        ("narrateur", "Ça sent l'oignon et le savon."),
        ("narrateur", "Le filet de maman est encore vide."),
        ("narrateur", "Il est un peu rêche, contre la jambe."),
        ("narrateur", "Un pigeon picore près d'une caisse."),
        ("narrateur", "En ce moment, Aniss tient le filet."),
        ("narrateur", "Il est au marché, avec papa et maman."),
        ("maman", "On dit bonjour, d'accord ?"),
        ("enfant-m", "Bonjour."),
        ("papa", "Si tu veux une fraise ?"),
        ("enfant-m", "S'il te plaît."),
        ("maman", "Bravo."),
        ("papa", "Et ensuite ?"),
        ("enfant-m", "Merci."),
        ("papa", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "La boulangerie sent le four, plus loin."),
        ("narrateur", "L'étal des fruits est tout rouge."),
        ("narrateur", "La fromagerie est un peu fraîche."),
        ("maman", "Tu restes près de nous."),
        ("enfant-m", "Oui, maman."),
        ("papa", "Le filet va se remplir, tout doux."),
        ("maman", "Tu es prêt ?"),
        ("enfant-m", "Oui, papa."),
        ("narrateur", "Une feuille collée au pavé, tout plat."),
        ("narrateur", "Le soleil revient sur la bâche."),
        ("narrateur", "Ça sent aussi le thym, tout bas."),
    ]


def tq1_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Où va Aniss, d'abord ?"),
        ("maman", "La boulangerie, l'étal des fruits, ou la fromagerie."),
    ]


def l1_012(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "Aniss pousse la porte de la boulangerie."),
            ("narrateur", "Un grelot tinte, tout aigu."),
            ("narrateur", "L'air sent le beurre, tout chaud."),
            ("narrateur", "Des croûtes dorées sont alignées."),
            ("enfant-m", "Bonjour."),
            ("papa", "Bonjour."),
            ("maman", "Tu veux un petit pain, Aniss ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le papier du sachet est un peu rêche."),
            ("enfant-m", "Merci."),
            ("papa", "Bravo, Aniss."),
            ("maman", "Tu as dit les trois mots."),
            ("papa", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Le bois du comptoir est lisse, tout chaud."),
        ]
    if i == 2:
        return [
            ("narrateur", "Aniss s'arrête à l'étal des fruits."),
            ("narrateur", "Les caisses sont rouges, un peu humides."),
            ("narrateur", "Une balance de fer attend, tout calme."),
            ("enfant-m", "Bonjour."),
            ("maman", "Bonjour."),
            ("papa", "Tu veux une pomme, Aniss ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "La pomme est lisse, encore un peu froide."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Tu as demandé, puis remercié."),
            ("papa", "On dit aussi bonjour."),
            ("enfant-m", "Bonjour."),
            ("narrateur", "Une fraise brille, tout près du filet."),
        ]
    return [
        ("narrateur", "Aniss entre à la fromagerie."),
        ("narrateur", "L'air est frais, comme le marbre."),
        ("narrateur", "Ça sent le lait, tout doux."),
        ("enfant-m", "Bonjour."),
        ("papa", "Bonjour."),
        ("maman", "Tu veux voir un fromage rond ?"),
        ("enfant-m", "S'il te plaît."),
        ("narrateur", "Le papier blanc fait un bruit doux."),
        ("enfant-m", "Merci, maman."),
        ("papa", "Bravo, Aniss."),
        ("maman", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "Le filet reste ouvert, tout près de la jambe."),
        ("papa", "On reste ensemble, ici."),
    ]


def q_012(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "Aniss veut le petit pain."),
            ("maman", "Que dit-il ?"),
        ]
    if i == 2:
        return [("narrateur", "À l'étal, quels mots ?")]
    return [
        ("narrateur", "À la fromagerie, Aniss salue."),
        ("papa", "On dit bonjour, s'il te plaît, merci ?"),
    ]


def c_012(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "Oui."),
            ("maman", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Aniss tient le sachet, tout calme."),
            ("papa", "Bravo, Aniss."),
            ("papa", "Tu as fait du bon travail."),
            ("enfant-m", "Merci, papa."),
            ("maman", "On continue, tout doux."),
        ]
    if i == 2:
        return [
            ("narrateur", "Oui."),
            ("papa", "On dit bonjour."),
            ("maman", "S'il te plaît. Merci."),
            ("narrateur", "Aniss pose la pomme dans le filet."),
            ("papa", "Bravo."),
            ("papa", "Tu as demandé gentiment."),
            ("enfant-m", "S'il te plaît."),
            ("maman", "C'est ça."),
        ]
    return [
        ("narrateur", "Oui."),
        ("maman", "Les trois mots sont là."),
        ("papa", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "Aniss hoche la tête."),
        ("maman", "Bravo, Aniss."),
        ("maman", "Tu as fait du bon travail."),
        ("enfant-m", "Merci, maman."),
    ]


def tq2_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Qui est là, près d'Aniss ?"),
        ("papa", "La boulangère, le voisin, ou la maîtresse."),
    ]


def l2_012(i: int, j: int) -> list[tuple[str, str]]:
    lieu = LIEU_012[i][1]
    extra = EXTRA_L2_012[(i, j)]
    if j == 1:
        return [
            ("narrateur", f"Aniss voit la boulangère, {lieu}."),
            ("narrateur", extra),
            ("narrateur", "Le tablier sent le four, tout chaud."),
            ("enfant-m", "Bonjour."),
            ("papa", "Bonjour."),
            ("maman", "Tu restes près de nous, Aniss."),
            ("enfant-m", "Oui, maman."),
            ("papa", "Tu veux que je tienne le filet ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le filet est rêche, un peu lourd déjà."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo."),
            ("maman", "Tu as dit les mots gentils."),
            ("papa", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Aniss reste tout près de la jambe de maman."),
        ]
    if j == 2:
        return [
            ("narrateur", f"Aniss voit le voisin, {lieu}."),
            ("narrateur", extra),
            ("narrateur", "Le sac du voisin est déjà un peu plein."),
            ("enfant-m", "Bonjour."),
            ("maman", "Bonjour."),
            ("papa", "Tu veux le filet un moment ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Papa tend le filet, tout doux."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo."),
            ("papa", "Bonjour. S'il te plaît. Merci."),
            ("narrateur", "Le voisin hoche la tête, tout calme."),
            ("enfant-m", "Merci."),
        ]
    return [
        ("narrateur", f"Aniss voit la maîtresse, {lieu}."),
        ("narrateur", extra),
        ("narrateur", "Son panier a un linge à carreaux."),
        ("enfant-m", "Bonjour."),
        ("papa", "Bonjour."),
        ("maman", "Tu veux un fruit, Aniss ?"),
        ("enfant-m", "S'il te plaît."),
        ("narrateur", "Maman tend le filet, tout ouvert."),
        ("enfant-m", "Merci, maman."),
        ("papa", "Bravo, Aniss."),
        ("maman", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "La maîtresse range un fruit, tout doux."),
        ("papa", "On reste ensemble."),
    ]


def tq3_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Qu'est-ce qui va dans le filet ?"),
        ("maman", "Le pain, une pomme, ou un fromage."),
    ]


def l3_012(i: int, j: int, k: int) -> list[tuple[str, str]]:
    lieu = LIEU_012[i][1]
    qui = QUI_012[j][0]
    qui_loc = QUI_012[j][1]
    obj = OBJ_012[k][0]
    extra = EXTRA_L3_012[(i, j, k)]
    if k == 1:
        toucher = "Le pain est tiède, contre les doigts."
    elif k == 2:
        toucher = "La pomme est lisse, un peu froide."
    else:
        toucher = "Le fromage est frais, tout enveloppé."
    return [
        ("narrateur", f"Aniss est encore {lieu}, {qui_loc}."),
        ("narrateur", extra),
        ("enfant-m", "Bonjour."),
        ("maman", f"Tu veux {obj} ?"),
        ("enfant-m", "S'il te plaît."),
        ("narrateur", toucher),
        ("enfant-m", "Merci."),
        ("papa", "Bravo, Aniss."),
        ("papa", "Tu as dit les trois mots."),
        ("maman", "Bonjour. S'il te plaît. Merci."),
        ("narrateur", "Le filet s'arrondit, tout doux."),
        ("papa", "On a ce qu'il faut, maintenant."),
    ]


def fin_012(i: int, j: int, k: int) -> list[tuple[str, str]]:
    lieu = LIEU_012[i][0]
    qui = QUI_012[j][0]
    obj = OBJ_012[k][0]
    img = FIN_IMG_012[(i, j, k)]
    return [
        ("narrateur", f"Aniss a vu {lieu}."),
        ("narrateur", f"Il a salué {qui}."),
        ("narrateur", f"Il a {obj} dans le filet."),
        ("narrateur", img),
        ("papa", "Tu as dit bonjour."),
        ("maman", "Tu as dit s'il te plaît."),
        ("papa", "Et merci."),
        ("maman", "Bravo, Aniss."),
        ("maman", "Tu as fait du bon travail."),
        ("enfant-m", "Merci, maman."),
        ("papa", "On rentre, le filet est plein."),
        ("narrateur", "L'histoire est finie."),
    ]


def story_012() -> None:
    # repair extras with accidental parens if any slipped — use clean dicts
    extra_l3 = dict(EXTRA_L3_012)
    extra_l3[(3, 3, 1)] = "La maîtresse a le pain, tout contre elle."
    EXTRA_L3_012[(3, 3, 1)] = extra_l3[(3, 3, 1)]
    FIN_IMG_012[(3, 3, 1)] = "La maîtresse dit au revoir, tout bas."

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}
    by["CHK_T0000_P0000"] = debut_012()
    sons["CHK_T0000_P0000"] = "bache,marche"
    by["CHK_T0001_P0000"] = tq1_012()
    sons["CHK_T0001_P0000"] = ""
    l1_sons = {1: "cloche,papier", 2: "", 3: ""}
    for i in (1, 2, 3):
        by[f"CHK_T0001_P000{i}"] = l1_012(i)
        sons[f"CHK_T0001_P000{i}"] = l1_sons[i]
        by[f"CHK_T0001_P000{i}_Q0001"] = q_012(i)
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        by[f"CHK_T0001_P000{i}_C0001"] = c_012(i)
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        by[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_012()
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""
        for j in (1, 2, 3):
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            by[cid2] = l2_012(i, j)
            sons[cid2] = ""
            by[f"{cid2}_T0003_P0000"] = tq3_012()
            sons[f"{cid2}_T0003_P0000"] = ""
            for k in (1, 2, 3):
                cid3 = f"{cid2}_T0003_P000{k}"
                by[cid3] = l3_012(i, j, k)
                sons[cid3] = "papier" if k == 1 else ""
                by[f"{cid3}_F0001"] = fin_012(i, j, k)
                sons[f"{cid3}_F0001"] = ""
    write_story(
        "TREE-COL-012",
        {
            "fil_rouge": (
                "Une bâche claque au-dessus des caisses. Aniss tient le filet. "
                "Au marché, il dit bonjour, s'il te plaît, merci."
            ),
            "title": "La bâche du marché d'Aniss",
            "characters": "Aniss, papa, maman",
            "setting": "marché du village, après la pluie",
        },
        by,
        sons,
    )


def main() -> None:
    story_011()
    story_012()
    for sid, extra in (
        ("TREE-COL-011", ("Tom", "Léa", "Sami")),
        ("TREE-COL-012", ()),
    ):
        data = json.loads((ROOT / sid / "merged.json").read_text(encoding="utf-8"))
        errs = check_story(data, extra_names=extra)
        if errs:
            print(sid, "ERRORS", len(errs))
            for e in errs[:40]:
                print(" ", e)
            raise SystemExit(1)
        first = (data["chunks"][0]["script"] or "").splitlines()[0]
        print(sid, "OK", first)


if __name__ == "__main__":
    main()
