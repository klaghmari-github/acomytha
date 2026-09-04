#!/usr/bin/env python3
"""F-NAR-009 — réécriture TREE-DIF-012 et TREE-DIF-013 (texte seulement)."""
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
FORBIDDEN = (
    "On va apprendre",
    "Voici le geste",
    "Il était une fois",
    "Ceci est l'histoire",
    "papa sourit",
    "maman sourit",
    "maman est là",
    "papa est là",
)
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}
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
    "Tom",
    "Léa",
    "Sami",
    "Où",
    "Doudou",
    "Amir",
    "Nino",
    "Sarah",
    "Victorino",
}


def split_phrases(lines: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for role, ph in lines:
        for p in re.split(r"(?<=[.!?])\s+", ph.strip()):
            if not p:
                continue
            if not p.endswith((".", "?", "!")):
                p = p + "."
            out.append((role, p))
    return out


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    lines = split_phrases(lines)
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
) -> dict:
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
    return merged


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def wc_strict(phrase: str) -> int:
    return len(phrase.replace("'", " ").replace("’", " ").split())


def check_story(data: dict, max_words: int, needles: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    by = {c["chunk_id"]: c for c in data["chunks"]}
    if len(data["chunks"]) != 86:
        errors.append(f"n_chunks={len(data['chunks'])}")
    allowed = TROUPE | SKIP_NAMES
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
            if role not in ROLES:
                errors.append(f"{c['chunk_id']} role {role}")
            n = wc_strict(ph)
            if n > max_words:
                errors.append(f"{c['chunk_id']} {n} mots: {ph}")
            if not ph.endswith((".", "?", "!")):
                errors.append(f"{c['chunk_id']} punct: {ph}")
            if "|" in ph:
                errors.append(f"{c['chunk_id']} pipe: {ph}")
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
            low = first.lower()
            if low.startswith(("c'est le matin", "aujourd'hui")):
                errors.append(f"{c['chunk_id']} entrée brutale: {first}")
            roles = {ln.split("|", 1)[0] for ln in lines}
            if "papa" not in roles or "maman" not in roles:
                errors.append(f"{c['chunk_id']} papa/maman manquant")
        blob = text
        for bad_name in (
            "Adam",
            "Iris",
            "Lina",
            "Nora",
            "Lucas",
            "Céline",
            "Celine",
            "Luca",
            "Noé",
            "Hugo",
            "Jules",
            "Maya",
            "Inès",
            "Zoé",
            "Kenzo",
            "Sara",
        ):
            if re.search(rf"\b{bad_name}\b", blob):
                errors.append(f"{c['chunk_id']} nom hors troupe: {bad_name}")
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


LOC_012 = {
    1: ("le bac à sable", "près du bac à sable"),
    2: ("le toboggan", "près du toboggan"),
    3: ("les balançoires", "près des balançoires"),
}
TOY_012 = {
    1: ("le ballon rouge", "ballon"),
    2: ("le seau bleu", "seau"),
    3: ("le doudou", "doudou"),
}
PEL = {
    1: ("Tom", "l'ours Tom", "ours"),
    2: ("Léa", "la poupée Léa", "poupée"),
    3: ("Sami", "le lion Sami", "lion"),
}

EXTRA_L2_012 = {
    (1, 1): "Le ballon a une tache de sable, toute fine.",
    (1, 2): "Le seau laisse un rond mouillé dans le sable.",
    (1, 3): "Un grain de sable colle à l'oreille du doudou.",
    (2, 1): "Le ballon roule jusqu'à la première marche.",
    (2, 2): "Le seau sonne contre le métal, tout creux.",
    (2, 3): "Le doudou s'assoit en bas du toboggan.",
    (3, 1): "Le ballon attend sous la balançoire, tout sage.",
    (3, 2): "Le seau tremble un peu, près de la chaîne.",
    (3, 3): "Le doudou a une place, sur les genoux.",
}

EXTRA_L3_012 = {
    (1, 1, 1): "L'ours a du sable sur le ventre, tout fin.",
    (1, 1, 2): "La poupée a le ballon contre la robe.",
    (1, 1, 3): "Le lion a du sable dans la crinière.",
    (1, 2, 1): "L'ours a le seau trop grand, sous le bras.",
    (1, 2, 2): "La poupée a une goutte sur la chaussure.",
    (1, 2, 3): "Le lion regarde l'eau, tout calme.",
    (1, 3, 1): "L'ours serre le doudou, tout doux.",
    (1, 3, 2): "La poupée a le doudou sur les genoux.",
    (1, 3, 3): "Le lion pose une patte sur le doudou.",
    (2, 1, 1): "L'ours est assis en bas de la rampe.",
    (2, 1, 2): "La poupée a une feuille sur le chapeau.",
    (2, 1, 3): "Le lion regarde le métal, tout calme.",
    (2, 2, 1): "L'ours a une goutte sur le nez.",
    (2, 2, 2): "La poupée tient le seau, trop lourd.",
    (2, 2, 3): "Le lion a l'oreille contre le seau.",
    (2, 3, 1): "L'ours a le doudou sous le bras.",
    (2, 3, 2): "La poupée caresse le doudou, tout lent.",
    (2, 3, 3): "Le lion a le doudou dans la crinière.",
    (3, 1, 1): "L'ours penche, comme la balançoire.",
    (3, 1, 2): "La poupée a le ballon entre les pieds.",
    (3, 1, 3): "Le lion suit le ballon des yeux.",
    (3, 2, 1): "L'ours a le seau entre les pattes.",
    (3, 2, 2): "La poupée a une chaîne froide, tout près.",
    (3, 2, 3): "Le lion écoute le seau, tout creux.",
    (3, 3, 1): "L'ours a le doudou sur les genoux.",
    (3, 3, 2): "La poupée berce le doudou, tout doux.",
    (3, 3, 3): "Le lion a le doudou contre le ventre.",
}

FIN_IMG_012 = {
    (1, 1, 1): "Une pomme verte reste près du bac.",
    (1, 1, 2): "Le ballon a encore un grain de sable.",
    (1, 1, 3): "L'ombre du pommier couvre le lion.",
    (1, 2, 1): "Le seau garde un peu d'eau, tout calme.",
    (1, 2, 2): "Une goutte sèche sur le bord du seau.",
    (1, 2, 3): "Le sable redevient lisse, tout plat.",
    (1, 3, 1): "Le doudou a une oreille un peu sablée.",
    (1, 3, 2): "Une fourmi passe près du doudou.",
    (1, 3, 3): "La caisse de pommes sent encore le jus.",
    (2, 1, 1): "Le métal du toboggan redevient froid.",
    (2, 1, 2): "Une feuille tourne au pied de la rampe.",
    (2, 1, 3): "Le ballon s'arrête, tout sage, en bas.",
    (2, 2, 1): "Le seau sonne une dernière fois, tout creux.",
    (2, 2, 2): "Une goutte glisse sur la rampe, tout lent.",
    (2, 2, 3): "L'herbe est un peu aplatie, tout près.",
    (2, 3, 1): "Le doudou garde une petite poussière.",
    (2, 3, 2): "Le chapeau de paille pend encore au clou.",
    (2, 3, 3): "Un oiseau chante, tout loin, tout bas.",
    (3, 1, 1): "La chaîne de la balançoire se tait.",
    (3, 1, 2): "Le ballon attend sous le siège, tout rond.",
    (3, 1, 3): "Un rayon glisse encore entre les feuilles.",
    (3, 2, 1): "Le seau a une goutte, toute ronde.",
    (3, 2, 2): "La balançoire ne crie plus, tout calme.",
    (3, 2, 3): "L'herbe sent encore la pomme écrasée.",
    (3, 3, 1): "Le doudou a une place, sur le banc.",
    (3, 3, 2): "Maman plie le doudou, tout doux.",
    (3, 3, 3): "Le pommier fait une dernière ombre ronde.",
}


def debut_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Une fourmi grimpe sur l'écorce du pommier."),
        ("narrateur", "L'écorce est rêche, un peu tiède."),
        ("narrateur", "Une pomme verte a une feuille collée."),
        ("narrateur", "La feuille tremble, tout petit."),
        ("narrateur", "L'ombre du pommier est fraîche."),
        ("narrateur", "Un chapeau de paille pend à un clou."),
        ("papa", "Tu sens la pomme, Nino ?"),
        ("enfant-m", "Elle est sucrée."),
        ("narrateur", "Une caisse sent le jus écrasé."),
        ("narrateur", "Un arrosoir goutte sur la mousse."),
        ("maman", "Tes doigts sont collants, dis ?"),
        ("enfant-m", "Un peu, maman."),
        ("narrateur", "Un rayon glisse entre les feuilles."),
        ("narrateur", "Il fait des ronds jaunes sur l'herbe."),
        ("narrateur", "En ce moment, Nino touche le tronc."),
        ("narrateur", "Le tronc est frais, tout rugueux."),
        ("narrateur", "Amir arrive en sautant."),
        ("narrateur", "Ses chaussures font toc toc."),
        ("narrateur", "Il a beaucoup d'énergie."),
        ("enfant-m", "Il bouge tout le temps."),
        ("maman", "Beaucoup d'énergie, ce n'est pas une faute."),
        ("papa", "On peut jouer."),
        ("papa", "On peut attendre."),
        ("papa", "On peut demander à un adulte."),
        ("narrateur", "Amir est un peu plus grand."),
        ("narrateur", "Nino est un peu plus petit."),
        ("narrateur", "Ils ont des tailles différentes."),
        ("maman", "On joue ensemble, d'accord ?"),
        ("enfant-m", "Oui, maman."),
        ("narrateur", "Une pomme roule, tout doux, dans l'herbe."),
        ("papa", "On reste près du pommier, tous les deux."),
        ("maman", "Amir, tu souffles un peu ?"),
        ("enfant-m", "Oui."),
        ("narrateur", "Amir souffle. Puis il tape des mains, tout content."),
        ("papa", "Bravo."),
        ("papa", "L'énergie, ce n'est pas une faute."),
    ]


def tq1_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Trois coins attendent, sous le pommier."),
        ("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ("maman", "On peut jouer, ou attendre."),
    ]


def l1_012(i: int) -> list[tuple[str, str]]:
    lieu, prep = LOC_012[i]
    if i == 1:
        return [
            ("narrateur", "Nino s'agenouille près du bac à sable."),
            ("narrateur", "Le sable est tiède, un peu rêche."),
            ("narrateur", "Un grain colle à son genou."),
            ("narrateur", "Amir saute autour du bac."),
            ("narrateur", "Ses pieds font des petits nuages."),
            ("narrateur", "Il a beaucoup d'énergie."),
            ("enfant-m", "Il bouge trop, maman."),
            ("maman", "Ce n'est pas une faute."),
            ("maman", "On peut jouer."),
            ("maman", "On peut attendre."),
            ("papa", "On peut demander à un adulte."),
            ("enfant-m", "Maman, on fait quoi ?"),
            ("maman", "Vous pouvez jouer ensemble."),
            ("narrateur", "Amir est plus grand, un peu."),
            ("narrateur", "Nino est plus petit."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("narrateur", "Nino tend une petite pelle."),
            ("narrateur", "Amir attend une seconde, puis prend."),
            ("papa", "Bravo, Amir."),
            ("papa", "Tu as attendu."),
            ("enfant-m", "On joue."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Le sable glisse entre leurs doigts."),
            ("papa", "L'énergie reste. Ce n'est pas une faute."),
        ]
    if i == 2:
        return [
            ("narrateur", "Nino pose la main sur le toboggan."),
            ("narrateur", "Le métal est un peu froid."),
            ("narrateur", "Une marche sonne, tout creux."),
            ("narrateur", "Amir saute en bas de la rampe."),
            ("narrateur", "Ses genoux plient, tout vite."),
            ("narrateur", "Il a beaucoup d'énergie."),
            ("enfant-m", "Il n'arrête pas, papa."),
            ("papa", "Ce n'est pas une faute."),
            ("papa", "On peut jouer."),
            ("papa", "On peut attendre."),
            ("maman", "On peut demander à un adulte."),
            ("enfant-m", "J'attends mon tour."),
            ("maman", "Bravo, Nino."),
            ("narrateur", "Amir souffle, puis il attend."),
            ("papa", "Bravo, Amir."),
            ("papa", "Tu as attendu."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("maman", "On joue ensemble, ici aussi."),
            ("narrateur", "Nino glisse, tout doux."),
            ("narrateur", "Amir glisse après, tout content."),
            ("enfant-m", "Encore ?"),
            ("maman", "On peut jouer. On peut attendre."),
            ("narrateur", "L'herbe est un peu aplatie, en bas."),
            ("papa", "Beaucoup d'énergie, près du toboggan."),
        ]
    return [
        ("narrateur", "Nino s'assoit sur la balançoire."),
        ("narrateur", "La chaîne est froide, un peu rêche."),
        ("narrateur", "Elle fait un tout petit criiiii."),
        ("narrateur", "Amir court autour des poteaux."),
        ("narrateur", "Ses chaussures tapent l'herbe, toc toc."),
        ("narrateur", "Il a beaucoup d'énergie."),
        ("enfant-m", "Maman, il court partout."),
        ("maman", "Ce n'est pas une faute."),
        ("maman", "On peut jouer."),
        ("maman", "On peut attendre."),
        ("papa", "On peut demander à un adulte."),
        ("enfant-m", "Papa, on fait quoi ?"),
        ("papa", "On attend un peu. Puis on joue."),
        ("narrateur", "Amir s'arrête. Il souffle."),
        ("maman", "Bravo, Amir."),
        ("maman", "Tu as attendu."),
        ("narrateur", "Ils ont des tailles différentes."),
        ("papa", "On joue ensemble, d'accord ?"),
        ("enfant-m", "Oui."),
        ("narrateur", "Nino pousse un tout petit peu."),
        ("narrateur", "Amir attend son tour, tout près."),
        ("maman", "C'est du bon travail."),
        ("narrateur", "La chaîne se tait, un moment."),
        ("papa", "L'énergie n'est pas une faute."),
    ]


def q_012(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "Un camarade bouge beaucoup."),
            ("maman", "Nino fait quoi ?"),
        ]
    if i == 2:
        return [
            ("narrateur", "Amir a beaucoup d'énergie."),
            ("papa", "On fait quoi ?"),
        ]
    return [
        ("narrateur", "Un camarade bouge beaucoup."),
        ("papa", "Nino fait quoi ?"),
    ]


def c_012(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("maman", "Oui."),
            ("maman", "C'est de l'énergie."),
            ("maman", "Ce n'est pas une faute."),
            ("papa", "On peut jouer, ou attendre."),
            ("papa", "On peut demander à un adulte."),
            ("narrateur", "Nino souffle un peu."),
            ("narrateur", "Un grain de sable reste sur son genou."),
            ("enfant-m", "On joue ensemble."),
            ("maman", "Bravo, Nino."),
            ("maman", "Tu as fait du bon travail."),
            ("narrateur", "Amir pose les mains sur le bac, tout calme."),
        ]
    if i == 2:
        return [
            ("papa", "Oui."),
            ("papa", "C'est de l'énergie."),
            ("papa", "Ce n'est pas une faute."),
            ("maman", "On peut jouer, ou attendre."),
            ("maman", "On peut demander à un adulte."),
            ("narrateur", "Nino essuie ses mains sur son manteau."),
            ("narrateur", "Le tissu est un peu rêche."),
            ("enfant-m", "J'attends. Puis on joue."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Le métal du toboggan reste froid, tout calme."),
        ]
    return [
        ("maman", "Oui."),
        ("maman", "C'est de l'énergie."),
        ("maman", "Ce n'est pas une faute."),
        ("papa", "On peut jouer, ou attendre."),
        ("papa", "On peut demander à un adulte."),
        ("narrateur", "Nino hoche la tête."),
        ("narrateur", "La chaîne ne crie plus."),
        ("enfant-m", "On joue ensemble."),
        ("maman", "Bravo."),
        ("maman", "On continue ensemble."),
        ("narrateur", "Amir pose un pied, tout sage, tout près."),
    ]


def tq2_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Trois objets attendent, tout proches."),
        ("maman", "Le ballon rouge, le seau bleu, ou le doudou ?"),
        ("papa", "On peut jouer. On peut attendre."),
    ]


def l2_012(i: int, j: int) -> list[tuple[str, str]]:
    _, prep = LOC_012[i]
    extra = EXTRA_L2_012[(i, j)]
    if j == 1:
        return [
            ("narrateur", f"Nino prend le ballon rouge, {prep}."),
            ("narrateur", "Le ballon est un peu sablé."),
            ("narrateur", extra),
            ("narrateur", "Amir saute vers le ballon."),
            ("narrateur", "Il a encore de l'énergie."),
            ("enfant-m", "À moi aussi !"),
            ("papa", "On attend un peu."),
            ("papa", "Ce n'est pas une faute."),
            ("maman", "On peut jouer ensemble."),
            ("narrateur", "Amir souffle. Il attend son tour."),
            ("papa", "Bravo, Amir."),
            ("papa", "Tu as attendu."),
            ("enfant-m", "Tiens."),
            ("maman", "Bravo, Nino."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("narrateur", "Le ballon va de l'un à l'autre."),
            ("maman", "On peut demander à un adulte."),
            ("papa", "L'énergie reste. On joue, ou on attend."),
        ]
    if j == 2:
        return [
            ("narrateur", f"Nino prend le seau bleu, {prep}."),
            ("narrateur", "Un peu d'eau tremble au fond."),
            ("narrateur", extra),
            ("narrateur", "Amir secoue les bras, tout content."),
            ("narrateur", "Il a encore de l'énergie."),
            ("enfant-m", "Je verse, maman ?"),
            ("maman", "On peut jouer."),
            ("maman", "On peut attendre."),
            ("papa", "Ce n'est pas une faute."),
            ("narrateur", "Amir attend que Nino verse."),
            ("maman", "Bravo, Amir."),
            ("enfant-m", "Merci."),
            ("papa", "Vous jouez ensemble."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("narrateur", "L'eau fait un petit ploc."),
            ("maman", "On peut demander à un adulte."),
            ("papa", "Beaucoup d'énergie, près du seau."),
            ("narrateur", "Nino pose le seau, tout doux."),
        ]
    return [
        ("narrateur", f"Nino prend le doudou, {prep}."),
        ("narrateur", "Le doudou est gris, un peu sablé."),
        ("narrateur", extra),
        ("narrateur", "Amir saute encore, tout près."),
        ("narrateur", "Il a encore de l'énergie."),
        ("enfant-m", "Doudou, il bouge beaucoup."),
        ("maman", "Ce n'est pas une faute."),
        ("papa", "On peut jouer, ou attendre."),
        ("papa", "On peut demander à un adulte."),
        ("narrateur", "Amir pose une main sur le doudou."),
        ("maman", "Tout doux, Amir."),
        ("enfant-m", "On joue ensemble."),
        ("papa", "Bravo, vous deux."),
        ("narrateur", "Ils ont des tailles différentes."),
        ("narrateur", "Nino serre le doudou, tout calme."),
        ("maman", "L'énergie n'est pas une faute."),
        ("papa", "Tu as attendu. C'est du bon travail."),
        ("narrateur", "Une oreille du doudou reste chaude."),
    ]


def tq3_012() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Qui vient jouer, tout près ?"),
        ("papa", "Tom, Léa, ou Sami ?"),
        ("maman", "On joue ensemble, avec eux aussi."),
    ]


def l3_012(i: int, j: int, k: int) -> list[tuple[str, str]]:
    nom, np, kind = PEL[k]
    extra = EXTRA_L3_012[(i, j, k)]
    toy = TOY_012[j][0]
    _, prep = LOC_012[i]
    if k == 1:
        return [
            ("narrateur", f"Nino rejoint {np}, {prep}."),
            ("narrateur", "L'ours est brun, un peu râpé."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("narrateur", extra),
            ("enfant-m", "Bonjour, Tom."),
            ("papa", "Bonjour, Tom."),
            ("narrateur", "Amir saute encore, tout près de l'ours."),
            ("maman", "Beaucoup d'énergie, ce n'est pas une faute."),
            ("papa", "On peut jouer. On peut attendre."),
            ("narrateur", "Amir pose l'ours, tout doux."),
            ("maman", "Bravo, Amir."),
            ("enfant-m", f"Tom, voilà {toy}."),
            ("papa", "Vous jouez ensemble."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("maman", "On peut demander à un adulte."),
            ("narrateur", "Nino caresse l'oreille de l'ours."),
            ("papa", "C'est du bon travail."),
        ]
    if k == 2:
        return [
            ("narrateur", f"Nino rejoint {np}, {prep}."),
            ("narrateur", "La robe est bleue, un peu froissée."),
            ("narrateur", "Un bouton brille, tout petit."),
            ("narrateur", extra),
            ("enfant-m", "Bonjour, Léa."),
            ("maman", "Bonjour, Léa."),
            ("narrateur", "Amir court un peu, puis s'arrête."),
            ("papa", "L'énergie n'est pas une faute."),
            ("maman", "On peut jouer, ou attendre."),
            ("narrateur", "Amir attend. Puis il tend la poupée."),
            ("papa", "Bravo, Amir."),
            ("papa", "Tu as attendu."),
            ("enfant-m", f"Léa, on a {toy}."),
            ("maman", "Vous jouez ensemble."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("papa", "On peut demander à un adulte."),
            ("narrateur", "Nino lisse la robe bleue."),
        ]
    return [
        ("narrateur", f"Nino rejoint {np}, {prep}."),
        ("narrateur", "La crinière est en laine, un peu mêlée."),
        ("narrateur", "Un œil de bouton regarde, tout calme."),
        ("narrateur", extra),
        ("enfant-m", "Bonjour, Sami."),
        ("papa", "Bonjour, Sami."),
        ("narrateur", "Amir tape des pieds, tout content."),
        ("maman", "Beaucoup d'énergie, ce n'est pas une faute."),
        ("papa", "On peut jouer. On peut attendre."),
        ("narrateur", "Amir souffle. Il range une mèche."),
        ("maman", "Bravo, Amir."),
        ("enfant-m", f"Sami, voici {toy}."),
        ("papa", "Vous jouez ensemble."),
        ("narrateur", "Ils ont des tailles différentes."),
        ("maman", "On peut demander à un adulte."),
        ("narrateur", "Le lion reste contre le genou de Nino."),
        ("papa", "Tu as fait du bon travail."),
    ]


def fin_012(i: int, j: int, k: int) -> list[tuple[str, str]]:
    lieu, prep = LOC_012[i]
    toy = TOY_012[j][0]
    nom = PEL[k][0]
    img = FIN_IMG_012[(i, j, k)]
    return [
        ("enfant-m", "On a joué sous le pommier."),
        ("enfant-m", "Amir avait de l'énergie."),
        ("maman", "Ce n'est pas une faute."),
        ("papa", "Vous avez joué, ou attendu."),
        ("maman", "Vous avez joué ensemble."),
        ("papa", "Bravo, Nino."),
        ("papa", "Tu as fait du bon travail."),
        ("narrateur", f"Nino a vécu ça {prep}."),
        ("narrateur", f"Il avait {toy}, et {nom} tout près."),
        ("narrateur", img),
        ("maman", "On rentre, tout doux ?"),
        ("enfant-m", "Oui, maman."),
        ("narrateur", "L'histoire est finie."),
    ]


def story_012() -> None:
    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}
    by["CHK_T0000_P0000"] = debut_012()
    sons["CHK_T0000_P0000"] = "oiseau,goutte"
    by["CHK_T0001_P0000"] = tq1_012()
    sons["CHK_T0001_P0000"] = ""
    l1_sons = {1: "sable", 2: "", 3: ""}
    l2_sons = {1: "ballon", 2: "eau", 3: ""}
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
            sons[cid2] = l2_sons[j]
            by[f"{cid2}_T0003_P0000"] = tq3_012()
            sons[f"{cid2}_T0003_P0000"] = ""
            for k in (1, 2, 3):
                cid3 = f"{cid2}_T0003_P000{k}"
                by[cid3] = l3_012(i, j, k)
                sons[cid3] = ""
                by[f"{cid3}_F0001"] = fin_012(i, j, k)
                sons[f"{cid3}_F0001"] = ""
    data = write_story(
        "TREE-DIF-012",
        {
            "fil_rouge": (
                "Sous le pommier, une pomme verte a une feuille collée. "
                "Nino voit Amir qui saute. C'est de l'énergie, pas une faute. "
                "Ils jouent ou attendent, avec papa et maman."
            ),
            "title": "La pomme verte et les pieds d'Amir",
            "characters": "Nino, Amir, papa, maman",
            "setting": "jardin sous le pommier, puis l'aire de jeux",
            "secondary_lessons": "DIF.COR.001",
        },
        by,
        sons,
    )
    err = check_story(
        data,
        10,
        (
            "énergie",
            "pas une faute",
            "jouer",
            "attendre",
            "tailles différentes",
            "ensemble",
        ),
    )
    if err:
        raise SystemExit("TREE-DIF-012\n" + "\n".join(err[:60]))


MOMENT_013 = {
    1: ("le matin", "au matin"),
    2: ("après la sieste", "après la sieste"),
    3: ("le soir", "au soir"),
}

EXTRA_L2_013 = {
    (1, 1): "Le ballon a un grain de sable, tout collé.",
    (1, 2): "Le seau laisse un rond d'eau sur le sable.",
    (1, 3): "Le doudou a une oreille un peu salée.",
    (2, 1): "Le ballon est tiède, comme les joues.",
    (2, 2): "Le seau a encore une goutte, toute ronde.",
    (2, 3): "Le doudou sent la serviette, un peu.",
    (3, 1): "Le ballon a une ombre longue, tout orange.",
    (3, 2): "Le seau reflète le ciel, tout bas.",
    (3, 3): "Le doudou a une place sur la serviette.",
}

EXTRA_L3_013 = {
    (1, 1, 1): "L'ours a du sable mouillé sur le ventre.",
    (1, 1, 2): "La poupée a le ballon contre la robe.",
    (1, 1, 3): "Le lion a du sel dans la crinière.",
    (1, 2, 1): "L'ours a le seau trop grand, tout lourd.",
    (1, 2, 2): "La poupée a une goutte sur la chaussure.",
    (1, 2, 3): "Le lion écoute l'eau, tout creux.",
    (1, 3, 1): "L'ours serre le doudou, tout doux.",
    (1, 3, 2): "La poupée a le doudou sur les genoux.",
    (1, 3, 3): "Le lion pose une patte sur le doudou.",
    (2, 1, 1): "L'ours a les joues de la sieste, tout chaud.",
    (2, 1, 2): "La poupée a un pli de serviette, au chapeau.",
    (2, 1, 3): "Le lion cligne, encore un peu endormi.",
    (2, 2, 1): "L'ours a une goutte sur le nez.",
    (2, 2, 2): "La poupée tient le seau, trop lourd.",
    (2, 2, 3): "Le lion a l'oreille contre le seau.",
    (2, 3, 1): "L'ours a le doudou sous le bras.",
    (2, 3, 2): "La poupée berce le doudou, tout lent.",
    (2, 3, 3): "Le lion a le doudou dans la crinière.",
    (3, 1, 1): "L'ours a une ombre orange, tout longue.",
    (3, 1, 2): "La poupée a le ballon entre les pieds.",
    (3, 1, 3): "Le lion suit le ballon des yeux.",
    (3, 2, 1): "L'ours a le seau entre les pattes.",
    (3, 2, 2): "La poupée a du sable froid, aux pieds.",
    (3, 2, 3): "Le lion écoute le seau, tout creux.",
    (3, 3, 1): "L'ours a le doudou sur les genoux.",
    (3, 3, 2): "La poupée berce le doudou, tout doux.",
    (3, 3, 3): "Le lion a le doudou contre le ventre.",
}

FIN_IMG_013 = {
    (1, 1, 1): "Une coquille fendue garde encore l'écume.",
    (1, 1, 2): "Le ballon a un grain de sable, tout collé.",
    (1, 1, 3): "Un oiseau blanc passe, tout loin.",
    (1, 2, 1): "Le seau garde un peu d'eau, tout calme.",
    (1, 2, 2): "Une goutte sèche sur le bord du seau.",
    (1, 2, 3): "Le trou de crabe reste, tout rond.",
    (1, 3, 1): "Le doudou a une oreille un peu salée.",
    (1, 3, 2): "La serviette rayée sent encore le sel.",
    (1, 3, 3): "Les tongs de papa ont encore un grain.",
    (2, 1, 1): "La serviette a un pli, tout chaud.",
    (2, 1, 2): "Le ballon est tiède, comme les joues.",
    (2, 1, 3): "La mer est plus calme, tout bas.",
    (2, 2, 1): "Le seau a une goutte, toute ronde.",
    (2, 2, 2): "Un filet d'eau sèche sur le sable.",
    (2, 2, 3): "La corde du bateau reste mouillée.",
    (2, 3, 1): "Le doudou sent encore la sieste.",
    (2, 3, 2): "La serviette redescend, tout calme.",
    (2, 3, 3): "Un oiseau se tait, tout loin.",
    (3, 1, 1): "L'ombre du ballon est longue, tout orange.",
    (3, 1, 2): "Le ciel baisse un peu, tout doux.",
    (3, 1, 3): "Une vague laisse un trait brillant.",
    (3, 2, 1): "Le seau reflète encore le soir.",
    (3, 2, 2): "Le sable redevient frais, tout gris.",
    (3, 2, 3): "La mer respire plus lentement.",
    (3, 3, 1): "Le doudou a une place, sur la serviette.",
    (3, 3, 2): "Maman plie la serviette, tout doux.",
    (3, 3, 3): "Le sel pique encore un tout petit peu.",
}


def debut_013() -> list[tuple[str, str]]:
    return [
        ("narrateur", "La mer respire, tout près, tout loin."),
        ("narrateur", "Une écume tremble dans une coquille fendue."),
        ("narrateur", "Un trou de crabe tient du sable mouillé."),
        ("narrateur", "Les tongs de papa ont un grain collé."),
        ("narrateur", "La serviette rayée sent le sel."),
        ("papa", "Tu sens le sel, Sarah ?"),
        ("enfant-f", "Ça pique un peu."),
        ("maman", "La corde du bateau est encore mouillée."),
        ("narrateur", "Un oiseau passe, tout loin, tout blanc."),
        ("narrateur", "Le vent pousse un peu de sable."),
        ("narrateur", "En ce moment, Sarah pose les pieds."),
        ("narrateur", "Le sable est frais, un peu rêche."),
        ("narrateur", "Victorino arrive avec un petit seau."),
        ("narrateur", "Victorino est plus petit."),
        ("narrateur", "Sarah est plus grande."),
        ("narrateur", "Ils ont des tailles différentes."),
        ("papa", "On peut jouer ensemble."),
        ("maman", "Le corps n'est pas une blague."),
        ("enfant-f", "Viens jouer."),
        ("enfant-m", "Oui."),
        ("narrateur", "Sarah tend une pelle, tout doux."),
        ("narrateur", "Victorino tend le seau, tout petit."),
        ("maman", "Bravo."),
        ("maman", "Vous jouez ensemble."),
        ("papa", "Personne ne commente le corps."),
        ("enfant-f", "On joue."),
        ("papa", "C'est ça."),
        ("narrateur", "Une vague laisse un trait brillant."),
        ("maman", "Tu as fait du bon travail, Sarah."),
        ("narrateur", "Le petit seau a une fissure, toute fine."),
        ("papa", "Plus petit, plus grand, on joue ensemble."),
        ("enfant-m", "Ensemble."),
    ]


def tq1_013() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Quel moment, au bord de l'eau ?"),
        ("papa", "Le matin, après la sieste, ou le soir ?"),
        ("maman", "On joue ensemble, à chaque fois."),
    ]


def l1_013(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "La lumière du matin est pâle, tout douce."),
            ("narrateur", "Le sable mouillé est encore froid."),
            ("narrateur", "Une coquille brille, toute nacrée."),
            ("narrateur", "Sarah marche, pieds nus, tout lentement."),
            ("narrateur", "Victorino court un peu, plus petit."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("enfant-f", "Tu es plus petit."),
            ("papa", "Oui."),
            ("papa", "Et on joue ensemble."),
            ("maman", "Le corps n'est pas une blague."),
            ("enfant-m", "On joue ?"),
            ("enfant-f", "Oui. Viens."),
            ("narrateur", "Sarah tend le seau, tout près de l'eau."),
            ("narrateur", "Victorino tient la pelle, trop grande."),
            ("maman", "Chacun a sa taille. On joue ensemble."),
            ("papa", "Bravo, Sarah."),
            ("papa", "Tu as invité."),
            ("narrateur", "L'écume touche leurs orteils, tout froid."),
            ("enfant-f", "C'est froid !"),
            ("maman", "Oui."),
            ("maman", "Vous jouez ensemble, au matin."),
            ("papa", "Personne ne commente le corps."),
            ("narrateur", "Un oiseau blanc se pose, tout loin."),
        ]
    if i == 2:
        return [
            ("narrateur", "Après la sieste, les joues sont chaudes."),
            ("narrateur", "La serviette a un pli, tout doux."),
            ("narrateur", "La mer est plus calme, tout bas."),
            ("narrateur", "Sarah cligne, encore un peu endormie."),
            ("narrateur", "Victorino arrive, plus petit, tout près."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("maman", "Tu es réveillée, Sarah ?"),
            ("enfant-f", "Oui, maman."),
            ("papa", "On joue ensemble, maintenant ?"),
            ("enfant-f", "Oui."),
            ("enfant-m", "Le seau."),
            ("maman", "Le corps n'est pas une blague."),
            ("papa", "Plus petit, plus grand, on joue."),
            ("narrateur", "Sarah baisse un peu la pelle."),
            ("narrateur", "Victorino atteint le manche, tout juste."),
            ("maman", "Bravo."),
            ("maman", "Vous jouez ensemble."),
            ("enfant-f", "Tiens, Victorino."),
            ("papa", "Tu as invité. C'est du bon travail."),
            ("narrateur", "Le sable tiède colle aux genoux."),
            ("maman", "Personne ne commente le corps."),
            ("narrateur", "Une vague plus petite vient, tout lent."),
            ("papa", "On joue ensemble, après la sieste."),
        ]
    return [
        ("narrateur", "Le soir, la lumière est orange, tout longue."),
        ("narrateur", "Le sable redevient frais, sous les pieds."),
        ("narrateur", "Les ombres s'allongent vers l'eau."),
        ("narrateur", "Sarah tient la serviette, un peu lourde."),
        ("narrateur", "Victorino tient un coin, plus petit."),
        ("narrateur", "Ils ont des tailles différentes."),
        ("papa", "On plie ensemble ?"),
        ("enfant-f", "Oui, papa."),
        ("maman", "Le corps n'est pas une blague."),
        ("papa", "On joue ensemble, au soir aussi."),
        ("enfant-m", "Le ballon ?"),
        ("enfant-f", "On joue."),
        ("narrateur", "Sarah lance tout doux, pas trop loin."),
        ("narrateur", "Victorino court, plus petit, tout content."),
        ("maman", "Bravo, Sarah."),
        ("maman", "Tu as adapté le jeu."),
        ("papa", "Vous jouez ensemble."),
        ("narrateur", "Une vague laisse un trait brillant."),
        ("maman", "Personne ne commente le corps."),
        ("enfant-f", "On est différents. On joue."),
        ("papa", "C'est ça."),
        ("papa", "Tu as fait du bon travail."),
        ("narrateur", "Le sel pique encore un tout petit peu."),
    ]


def q_013(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("narrateur", "Plus petit ou plus grand."),
            ("maman", "Sarah fait quoi ?"),
        ]
    if i == 2:
        return [
            ("narrateur", "Sarah et Victorino ont des tailles différentes."),
            ("papa", "On fait quoi ?"),
        ]
    return [
        ("narrateur", "Plus petit ou plus grand."),
        ("papa", "Sarah fait quoi ?"),
    ]


def c_013(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return [
            ("maman", "Oui."),
            ("maman", "On peut jouer ensemble."),
            ("papa", "Tailles différentes. On joue ensemble."),
            ("maman", "Le corps n'est pas une blague."),
            ("narrateur", "Sarah souffle un peu."),
            ("narrateur", "Un grain de sable reste sur son genou."),
            ("enfant-f", "On joue ensemble."),
            ("papa", "Bravo, Sarah."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", "Victorino pose le seau, tout calme."),
            ("maman", "Personne ne commente le corps."),
        ]
    if i == 2:
        return [
            ("papa", "Oui."),
            ("papa", "On peut jouer ensemble."),
            ("maman", "Tailles différentes. On joue ensemble."),
            ("papa", "Le corps n'est pas une blague."),
            ("narrateur", "Sarah essuie une joue, encore chaude."),
            ("narrateur", "La serviette est un peu rêche."),
            ("enfant-f", "Viens, Victorino."),
            ("maman", "Bravo."),
            ("maman", "Tu as invité."),
            ("narrateur", "Le sable tiède garde deux traces, côte à côte."),
            ("papa", "Personne ne commente le corps."),
        ]
    return [
        ("maman", "Oui."),
        ("maman", "On joue ensemble."),
        ("papa", "Tailles différentes. On joue ensemble."),
        ("maman", "Le corps n'est pas une blague."),
        ("narrateur", "Sarah hoche la tête."),
        ("narrateur", "L'ombre orange glisse sur l'eau."),
        ("enfant-f", "On joue ensemble."),
        ("papa", "Bravo."),
        ("papa", "On continue ensemble."),
        ("narrateur", "Victorino serre le coin de la serviette."),
        ("maman", "Personne ne commente le corps."),
    ]


def tq2_013() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Trois objets attendent, sur le sable."),
        ("maman", "Le ballon rouge, le seau bleu, ou le doudou ?"),
        ("papa", "On joue ensemble, avec ça."),
    ]


def l2_013(i: int, j: int) -> list[tuple[str, str]]:
    extra = EXTRA_L2_013[(i, j)]
    moment = MOMENT_013[i][1]
    if j == 1:
        return [
            ("narrateur", f"Sarah prend le ballon rouge, {moment}."),
            ("narrateur", "Le ballon est un peu sablé, tout rêche."),
            ("narrateur", extra),
            ("enfant-f", "Victorino, on joue ?"),
            ("enfant-m", "Oui."),
            ("papa", "Tu lances tout doux, d'accord ?"),
            ("enfant-f", "Oui, papa."),
            ("narrateur", "Sarah est plus grande. Victorino plus petit."),
            ("narrateur", "Ils ont des tailles différentes."),
            ("maman", "On joue ensemble."),
            ("maman", "Le corps n'est pas une blague."),
            ("narrateur", "Sarah lance près des pieds, pas trop loin."),
            ("papa", "Bravo, Sarah."),
            ("papa", "Tu as adapté."),
            ("enfant-m", "À moi !"),
            ("narrateur", "Victorino pousse le ballon, tout content."),
            ("maman", "Vous jouez ensemble."),
            ("papa", "Personne ne commente le corps."),
        ]
    if j == 2:
        return [
            ("narrateur", f"Sarah prend le seau bleu, {moment}."),
            ("narrateur", "Un peu d'eau tremble au fond."),
            ("narrateur", extra),
            ("maman", "Tu verses, tout doux ?"),
            ("enfant-f", "Oui, maman."),
            ("narrateur", "Victorino tient un petit moule."),
            ("narrateur", "Le moule est trop grand pour lui, un peu."),
            ("papa", "Tailles différentes. On joue ensemble."),
            ("maman", "Le corps n'est pas une blague."),
            ("enfant-f", "Tiens, de l'eau."),
            ("enfant-m", "Merci."),
            ("narrateur", "Sarah verse. Victorino lisse le sable."),
            ("papa", "Bravo, vous deux."),
            ("maman", "Vous jouez ensemble."),
            ("narrateur", "Le gâteau de sable tient, tout petit."),
            ("papa", "Personne ne commente le corps."),
            ("enfant-f", "Il est beau."),
            ("maman", "Oui. C'est du bon travail."),
        ]
    return [
        ("narrateur", f"Sarah prend le doudou, {moment}."),
        ("narrateur", "Le doudou est gris, un peu salé."),
        ("narrateur", extra),
        ("enfant-f", "Doudou, viens jouer."),
        ("maman", "Victorino peut le tenir aussi."),
        ("papa", "On joue ensemble."),
        ("narrateur", "Sarah est plus grande. Victorino plus petit."),
        ("narrateur", "Ils ont des tailles différentes."),
        ("maman", "Le corps n'est pas une blague."),
        ("enfant-f", "Tiens."),
        ("enfant-m", "Doudou."),
        ("narrateur", "Victorino serre le doudou, tout doux."),
        ("papa", "Bravo, Sarah."),
        ("papa", "Tu as partagé."),
        ("maman", "Vous jouez ensemble."),
        ("papa", "Personne ne commente le corps."),
        ("narrateur", "Une oreille du doudou reste chaude."),
        ("maman", "C'est du bon travail."),
    ]


def tq3_013() -> list[tuple[str, str]]:
    return [
        ("narrateur", "Qui vient jouer, sur le sable ?"),
        ("papa", "Tom, Léa, ou Sami ?"),
        ("maman", "On joue ensemble, avec eux aussi."),
    ]


def l3_013(i: int, j: int, k: int) -> list[tuple[str, str]]:
    nom, np, _kind = PEL[k]
    extra = EXTRA_L3_013[(i, j, k)]
    toy = TOY_012[j][0]
    moment = MOMENT_013[i][1]
    if k == 1:
        return [
            ("narrateur", f"Sarah rejoint {np}, {moment}."),
            ("narrateur", "L'ours est brun, un peu râpé."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("narrateur", extra),
            ("enfant-f", "Bonjour, Tom."),
            ("papa", "Bonjour, Tom."),
            ("narrateur", "Victorino pose l'ours, plus petit, tout près."),
            ("maman", "Tailles différentes. On joue ensemble."),
            ("papa", "Le corps n'est pas une blague."),
            ("enfant-f", f"Tom, voilà {toy}."),
            ("enfant-m", "Ensemble."),
            ("maman", "Bravo, Sarah."),
            ("maman", "Tu as invité."),
            ("papa", "Vous jouez ensemble."),
            ("narrateur", "L'ours s'assoit entre eux, tout sage."),
            ("maman", "Personne ne commente le corps."),
            ("papa", "C'est du bon travail."),
        ]
    if k == 2:
        return [
            ("narrateur", f"Sarah rejoint {np}, {moment}."),
            ("narrateur", "La robe est bleue, un peu froissée."),
            ("narrateur", "Un bouton brille, tout petit."),
            ("narrateur", extra),
            ("enfant-f", "Bonjour, Léa."),
            ("maman", "Bonjour, Léa."),
            ("narrateur", "Victorino lisse la robe, tout lent."),
            ("papa", "Tailles différentes. On joue ensemble."),
            ("maman", "Le corps n'est pas une blague."),
            ("enfant-f", f"Léa, on a {toy}."),
            ("enfant-m", "Joue."),
            ("papa", "Bravo, Sarah."),
            ("papa", "Tu as partagé."),
            ("maman", "Vous jouez ensemble."),
            ("narrateur", "La poupée a les pieds froids, tout plastique."),
            ("papa", "Personne ne commente le corps."),
            ("maman", "C'est du bon travail."),
        ]
    return [
        ("narrateur", f"Sarah rejoint {np}, {moment}."),
        ("narrateur", "La crinière est en laine, un peu mêlée."),
        ("narrateur", "Un œil de bouton regarde, tout calme."),
        ("narrateur", extra),
        ("enfant-f", "Bonjour, Sami."),
        ("papa", "Bonjour, Sami."),
        ("narrateur", "Victorino range une mèche, tout doux."),
        ("maman", "Tailles différentes. On joue ensemble."),
        ("papa", "Le corps n'est pas une blague."),
        ("enfant-f", f"Sami, voici {toy}."),
        ("enfant-m", "Lion."),
        ("maman", "Bravo, Sarah."),
        ("maman", "Tu as invité."),
        ("papa", "Vous jouez ensemble."),
        ("narrateur", "Le lion reste contre le genou de Sarah."),
        ("maman", "Personne ne commente le corps."),
        ("papa", "Tu as fait du bon travail."),
    ]


def fin_013(i: int, j: int, k: int) -> list[tuple[str, str]]:
    moment_np, moment = MOMENT_013[i]
    toy = TOY_012[j][0]
    nom = PEL[k][0]
    img = FIN_IMG_013[(i, j, k)]
    return [
        ("enfant-f", "On a joué au bord de la mer."),
        ("enfant-f", "On a joué ensemble."),
        ("maman", "Tailles différentes. On joue ensemble."),
        ("papa", "Le corps n'est pas une blague."),
        ("maman", "Bravo, Sarah."),
        ("papa", "Tu as fait du bon travail."),
        ("narrateur", f"Sarah a vécu ça {moment}."),
        ("narrateur", f"Elle avait {toy}, et {nom} tout près."),
        ("narrateur", img),
        ("maman", "On rince les pieds, tout doux ?"),
        ("enfant-f", "Oui, maman."),
        ("narrateur", "L'histoire est finie."),
    ]


def story_013() -> None:
    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}
    by["CHK_T0000_P0000"] = debut_013()
    sons["CHK_T0000_P0000"] = "mer,oiseau"
    by["CHK_T0001_P0000"] = tq1_013()
    sons["CHK_T0001_P0000"] = ""
    l1_sons = {1: "oiseau", 2: "", 3: "mer"}
    l2_sons = {1: "ballon", 2: "eau", 3: ""}
    for i in (1, 2, 3):
        by[f"CHK_T0001_P000{i}"] = l1_013(i)
        sons[f"CHK_T0001_P000{i}"] = l1_sons[i]
        by[f"CHK_T0001_P000{i}_Q0001"] = q_013(i)
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        by[f"CHK_T0001_P000{i}_C0001"] = c_013(i)
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        by[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_013()
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""
        for j in (1, 2, 3):
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            by[cid2] = l2_013(i, j)
            sons[cid2] = l2_sons[j]
            by[f"{cid2}_T0003_P0000"] = tq3_013()
            sons[f"{cid2}_T0003_P0000"] = ""
            for k in (1, 2, 3):
                cid3 = f"{cid2}_T0003_P000{k}"
                by[cid3] = l3_013(i, j, k)
                sons[cid3] = ""
                by[f"{cid3}_F0001"] = fin_013(i, j, k)
                sons[f"{cid3}_F0001"] = "mer"
    data = write_story(
        "TREE-DIF-013",
        {
            "fil_rouge": (
                "Au bord de la mer, le sel pique les lèvres. "
                "Sarah est plus grande. Victorino est plus petit. "
                "Ils jouent ensemble. Le corps n'est pas une blague."
            ),
            "title": "Le sel sur les lèvres de Sarah",
            "characters": "Sarah, Victorino, papa, maman",
            "setting": "plage, serviette rayée, sable mouillé",
            "secondary_lessons": "DIF.COR.002",
        },
        by,
        sons,
    )
    err = check_story(
        data,
        15,
        (
            "tailles différentes",
            "jouer ensemble",
            "blague",
        ),
    )
    if err:
        raise SystemExit("TREE-DIF-013\n" + "\n".join(err[:60]))


def main() -> None:
    story_012()
    story_013()
    print("ok TREE-DIF-012 TREE-DIF-013")


if __name__ == "__main__":
    main()
