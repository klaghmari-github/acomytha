#!/usr/bin/env python3
"""F-NAR-009 — merged.json TREE-DIF-006 et TREE-DIF-007 (texte seulement)."""
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
    "Ou",
    "Moi",
    "Ensemble",
    "Rouge",
    "Bleu",
    "Vert",
    "Sinon",
    "Alors",
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


def apply_chunk(src: dict, lines: list[tuple[str, str]], sons: str | None = None) -> dict:
    text, script = pack(lines)
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    if sons is None:
        out["sons"] = src.get("sons") or ""
    else:
        out["sons"] = sons
    return out


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str] | None = None,
) -> dict:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:12]} extra={extra[:12]}")
    sons_map = sons_map or {}
    chunks = []
    for c in source["chunks"]:
        cid = c["chunk_id"]
        chunks.append(apply_chunk(c, by_id[cid], sons_map.get(cid)))
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
            if not ph.endswith((".", "?", "!")):
                errors.append(f"{c['chunk_id']} sans ponctuation: {ph}")
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
            if first.startswith("Il était une fois") or first.startswith("Ceci est l'histoire"):
                errors.append(f"{c['chunk_id']} moule: {first}")
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
# TREE-DIF-006 — Aniss, jardin, N2 — DIF.ENE.001
# L1 bac / cerisier / banc   L2 cubes / livre / dînette   L3 pomme / yaourt / pain
# ---------------------------------------------------------------------------

LIEU6 = {1: "le bac", 2: "le cerisier", 3: "le banc"}
LIEU6_PRES = {1: "du bac", 2: "du cerisier", 3: "du banc"}
TOY6 = {1: "les cubes", 2: "le livre", 3: "la dînette"}
TOY6_PRES = {1: "des cubes", 2: "du livre", 3: "de la dînette"}
SNACK6 = {1: "une pomme", 2: "un yaourt", 3: "un morceau de pain"}
SNACK6_DE = {1: "d'une pomme", 2: "d'un yaourt", 3: "d'un morceau de pain"}


def debut_006() -> list[tuple[str, str]]:
    return L(
        "narrateur|Une goutte tombe de l'arrosoir.",
        "narrateur|Elle fait ploc, sur la dalle.",
        "narrateur|L'herbe brille encore, toute mouillée.",
        "narrateur|Ça sent la terre, et la menthe.",
        "narrateur|Un linge rose sèche, tout léger.",
        "narrateur|Papa pose ses bottes près du seau.",
        "maman|Tu as vu la goutte, Aniss ?",
        "enfant-m|Elle a fait ploc.",
        "papa|La dalle est froide, hein ?",
        "enfant-m|Oui, papa.",
        "narrateur|Un seau jaune attend près du tuyau.",
        "narrateur|Une abeille passe, tout bas.",
        "narrateur|Le banc de bois est déjà tiède.",
        "narrateur|Le cerisier laisse tomber un pétale.",
        "maman|Je verse encore un peu d'eau.",
        "narrateur|L'eau chante dans les fleurs.",
        "papa|Tu sens la menthe ?",
        "enfant-m|Oui. Elle pique un peu.",
        "narrateur|En ce moment, Aniss s'accroupit.",
        "narrateur|Il touche une feuille, toute douce.",
        "narrateur|Mila arrive dans le jardin.",
        "narrateur|Elle court. Elle saute. Elle tourne.",
        "narrateur|Ses chaussures font toc toc, sur l'herbe.",
        "narrateur|Elle a beaucoup d'énergie.",
        "papa|Cette énergie n'est pas une faute.",
        "maman|On peut jouer ou attendre.",
        "papa|On peut demander à un adulte.",
        "enfant-m|Elle bouge tout le temps.",
        "maman|Ce n'est pas une faute, Aniss.",
        "narrateur|Mila s'arrête. Puis elle reprend.",
        "enfant-f|On joue ?",
        "papa|On peut jouer ensemble.",
        "papa|On peut aussi attendre son tour.",
        "enfant-m|Je peux attendre.",
        "papa|Bravo, Aniss.",
        "maman|C'est du bon travail.",
        "narrateur|Le bac attend, tout sombre.",
        "narrateur|Le cerisier attend, tout rose.",
        "narrateur|Le banc attend, tout calme.",
        "maman|Tu es prêt ?",
        "enfant-m|Oui, maman.",
    )


def tq1_006() -> list[tuple[str, str]]:
    return L(
        "narrateur|Aniss va où, dans le jardin ?",
        "papa|Le bac, le cerisier, ou le banc.",
    )


def l1_006(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Aniss va vers le bac.",
            "narrateur|La terre est sombre, encore mouillée.",
            "narrateur|Une marguerite penche, toute légère.",
            "narrateur|Mila court autour du bac.",
            "narrateur|Elle a beaucoup d'énergie.",
            "papa|Cette énergie n'est pas une faute.",
            "maman|On peut jouer ou attendre.",
            "enfant-m|Je peux attendre mon tour.",
            "papa|Oui. On joue ensemble aussi.",
            "narrateur|Mila s'arrête. Puis elle reprend.",
            "maman|Tu peux demander à un adulte.",
            "enfant-m|Maman, on fait quoi ?",
            "maman|On joue, ou on attend.",
            "papa|Bravo, Aniss.",
            "narrateur|Le seau jaune reste près du bac.",
        )
    if i == 2:
        return L(
            "narrateur|Aniss va vers le cerisier.",
            "narrateur|Un pétale rose tombe sur l'herbe.",
            "narrateur|L'ombre est douce, un peu froide.",
            "narrateur|Mila saute sous les branches.",
            "narrateur|Elle a beaucoup d'énergie.",
            "maman|Cette énergie n'est pas une faute.",
            "papa|On peut jouer ou attendre.",
            "enfant-f|Je saute, moi.",
            "enfant-m|J'attends un peu.",
            "papa|C'est bien. On attend son tour.",
            "narrateur|Mila souffle. Puis elle reprend.",
            "maman|On peut demander à un adulte.",
            "enfant-m|Papa, on joue ensemble ?",
            "papa|Oui. On peut aussi attendre.",
            "narrateur|Un pétale reste sur l'épaule d'Aniss.",
        )
    return L(
        "narrateur|Aniss va vers le banc.",
        "narrateur|Le bois est tiède, un peu lisse.",
        "narrateur|Un escargot avance, tout lent.",
        "narrateur|Mila tourne. Puis elle s'assoit.",
        "narrateur|Elle a beaucoup d'énergie.",
        "papa|Cette énergie n'est pas une faute.",
        "maman|On peut jouer ou attendre.",
        "enfant-m|Elle s'assoit. Puis elle se lève.",
        "papa|On attend. Puis on joue.",
        "narrateur|Mila pose une main sur le bois.",
        "maman|Tu peux demander à papa.",
        "enfant-m|On joue, ou on attend ?",
        "maman|Les deux. Ce n'est pas une faute.",
        "papa|Bravo. Tu as demandé.",
        "narrateur|Le banc garde une trace de soleil.",
    )


def q_006(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Cette énergie, c'est une faute ?",
        )
    if i == 2:
        return L(
            "narrateur|On joue, ou on attend ?",
        )
    return L(
        "narrateur|On demande à un adulte ?",
    )


def c_006(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Oui.",
            "papa|Cette énergie n'est pas une faute.",
            "maman|On peut jouer ou attendre.",
            "narrateur|Aniss respire, tout calme.",
            "papa|Bravo, Aniss.",
            "papa|Tu as fait du bon travail.",
            "enfant-m|Merci, papa.",
            "maman|On continue, tout doux.",
        )
    if i == 2:
        return L(
            "narrateur|Oui.",
            "maman|On joue, ou on attend.",
            "papa|Cette énergie n'est pas une faute.",
            "narrateur|Aniss retient un petit saut.",
            "maman|Bravo.",
            "maman|Tu as attendu ton tour.",
            "enfant-m|Je peux jouer aussi.",
            "papa|Oui. On joue ensemble.",
            "papa|On peut aussi attendre.",
        )
    return L(
        "narrateur|Oui.",
        "papa|On demande à un adulte.",
        "maman|Cette énergie n'est pas une faute.",
        "narrateur|Aniss hoche la tête.",
        "papa|On peut jouer ou attendre.",
        "maman|Bravo, Aniss.",
        "enfant-m|Merci, maman.",
        "papa|C'est du bon travail.",
    )


def tq2_006() -> list[tuple[str, str]]:
    return L(
        "narrateur|On prend quel jeu ?",
        "maman|Les cubes, le livre, ou la dînette.",
    )


def l2_006(i: int, j: int) -> list[tuple[str, str]]:
    lieu = LIEU6[i]
    if j == 1:
        return L(
            f"narrateur|Près de {lieu}, Mila veut les cubes.",
            "narrateur|Les cubes sont en bois, un peu rudes.",
            "narrateur|Un cube rouge fait toc, sur l'herbe.",
            "narrateur|Mila bouge beaucoup, encore.",
            "papa|Cette énergie n'est pas une faute.",
            "maman|On peut jouer ou attendre.",
            "enfant-m|J'attends mon tour.",
            "papa|Oui. Puis on joue ensemble.",
            "narrateur|Mila pose un cube. Puis elle reprend.",
            "maman|Tu peux demander à papa.",
            "enfant-m|Papa, c'est mon tour ?",
            "papa|Oui. Bravo, Aniss.",
            "narrateur|Le cube rouge reste dans sa main.",
        )
    if j == 2:
        return L(
            f"narrateur|Près de {lieu}, Mila veut le livre.",
            "narrateur|La couverture est un peu rêche.",
            "narrateur|Une page chuchote sous le doigt.",
            "narrateur|Mila tourne les pages, tout vite.",
            "maman|Cette énergie n'est pas une faute.",
            "papa|On peut jouer ou attendre.",
            "enfant-m|On attend un peu.",
            "maman|Oui. Puis on lit ensemble.",
            "narrateur|Mila souffle. Elle pose le livre.",
            "papa|Tu peux demander à maman.",
            "enfant-m|Maman, on lit ?",
            "maman|Oui. Bravo. Tu as attendu.",
            "narrateur|Un pétale reste sur la page.",
        )
    return L(
        f"narrateur|Près de {lieu}, Mila veut la dînette.",
        "narrateur|Une petite tasse sonne, tout creux.",
        "narrateur|Ça sent presque la soupe, pour de rire.",
        "narrateur|Mila range. Puis elle dérange.",
        "papa|Cette énergie n'est pas une faute.",
        "maman|On peut jouer ou attendre.",
        "enfant-m|On sert à tour de rôle.",
        "papa|Oui. On attend son tour.",
        "narrateur|Mila pose la cuillère, tout doux.",
        "maman|Tu as demandé. C'est bien.",
        "enfant-m|Merci, maman.",
        "papa|Bravo, vous deux.",
        "narrateur|La petite casserole reste au calme.",
    )


def tq3_006() -> list[tuple[str, str]]:
    return L(
        "narrateur|On prend quel goûter ?",
        "papa|Une pomme, un yaourt, ou un morceau de pain.",
    )


OPEN_006 = {
    (1, 1, 1): ("Une pomme brille au bord du bac.", "Un cube rouge a une goutte."),
    (1, 1, 2): ("Un yaourt frais attend près des cubes.", "La terre du bac est encore sombre."),
    (1, 1, 3): ("Un morceau de pain sent le four.", "Un cube jaune garde une miette."),
    (1, 2, 1): ("Une pomme roule vers le livre.", "Le bac a laissé une tache d'eau."),
    (1, 2, 2): ("Un yaourt cliquette près du livre.", "Une marguerite penche vers la page."),
    (1, 2, 3): ("Un morceau de pain repose sur le livre.", "L'eau du bac chante encore."),
    (1, 3, 1): ("Une pomme sert de gâteau, pour de rire.", "La dînette est près du bac."),
    (1, 3, 2): ("Un yaourt brille comme de la crème.", "La petite tasse a une goutte."),
    (1, 3, 3): ("Un morceau de pain devient un gâteau.", "La dînette a des miettes de terre."),
    (2, 1, 1): ("Une pomme attrape un pétale rose.", "Un cube rouge dort sous le cerisier."),
    (2, 1, 2): ("Un yaourt est froid, sous l'ombre.", "Les cubes ont des pétales dessus."),
    (2, 1, 3): ("Un morceau de pain a un pétale.", "Un cube bleu reste dans l'herbe."),
    (2, 2, 1): ("Une pomme pose sur le livre ouvert.", "Le cerisier fait une ombre ronde."),
    (2, 2, 2): ("Un yaourt attend près de la page.", "Un pétale colle à la couverture."),
    (2, 2, 3): ("Un morceau de pain tiédit au soleil.", "Le livre garde une page ouverte."),
    (2, 3, 1): ("Une pomme rentre dans une petite assiette.", "Le cerisier laisse tomber un pétale."),
    (2, 3, 2): ("Un yaourt fait un goûter de poupée.", "La dînette est sous les branches."),
    (2, 3, 3): ("Un morceau de pain sert de tartine.", "Une abeille passe près de la tasse."),
    (3, 1, 1): ("Une pomme roule sous le banc.", "Un cube rouge tape le bois, tout doux."),
    (3, 1, 2): ("Un yaourt reste au frais, sur le banc.", "Les cubes font un petit tas."),
    (3, 1, 3): ("Un morceau de pain attend sur le bois.", "Un cube jaune a une miette."),
    (3, 2, 1): ("Une pomme brille près du livre.", "Le banc est tiède, encore."),
    (3, 2, 2): ("Un yaourt cliquette sur le banc.", "Le livre a une ombre de linge."),
    (3, 2, 3): ("Un morceau de pain sent le bois chaud.", "Une page du livre claque, tout léger."),
    (3, 3, 1): ("Une pomme devient un gâteau de banc.", "La dînette sonne contre le bois."),
    (3, 3, 2): ("Un yaourt refroidit la petite cuillère.", "Le banc garde la dînette, tout calme."),
    (3, 3, 3): ("Un morceau de pain a des miettes.", "La dînette rentre dans la boîte."),
}

FIN_IMG_006 = {
    (1, 1, 1): "Une coccinelle s'est posée sur la marguerite.",
    (1, 1, 2): "La cuillère a gardé un peu de froid.",
    (1, 1, 3): "Une miette dort encore sur le bord du bac.",
    (1, 2, 1): "Un pétale a séché sur la pomme.",
    (1, 2, 2): "Le livre a une petite tache d'eau.",
    (1, 2, 3): "Le pain a tiédi près des fleurs.",
    (1, 3, 1): "La petite tasse a un rond de pomme.",
    (1, 3, 2): "La casserole de dînette s'est tue.",
    (1, 3, 3): "Une miette reste dans la petite assiette.",
    (2, 1, 1): "Un cube rouge a gardé un pétale.",
    (2, 1, 2): "L'ombre du cerisier a glissé, tout doux.",
    (2, 1, 3): "Une abeille a visité le pain, de loin.",
    (2, 2, 1): "La page a gardé une odeur de pomme.",
    (2, 2, 2): "Un pétale rose reste dans le livre.",
    (2, 2, 3): "Le cerisier a fait un tapis de pétales.",
    (2, 3, 1): "La petite assiette a un pétale, tout drôle.",
    (2, 3, 2): "Une fourmi a visité la soucoupe, puis elle est partie.",
    (2, 3, 3): "Le linge rose a claqué, tout loin.",
    (3, 1, 1): "Le bois du banc est encore tiède.",
    (3, 1, 2): "Un escargot a avancé près du pied.",
    (3, 1, 3): "Le seau jaune a gardé une miette.",
    (3, 2, 1): "Le tuyau a fait chhh, tout doux.",
    (3, 2, 2): "Un papillon a touché la page, puis parti.",
    (3, 2, 3): "L'herbe mouillée brille encore, sous le banc.",
    (3, 3, 1): "La balançoire vide a bougé, tout léger.",
    (3, 3, 2): "Une feuille de menthe sent encore, tout près.",
    (3, 3, 3): "Une trace de botte reste sur la dalle.",
}


def l3_006(i: int, j: int, k: int) -> list[tuple[str, str]]:
    a, b = OPEN_006[(i, j, k)]
    return L(
        f"narrateur|{a}",
        f"narrateur|{b}",
        f"narrateur|Aniss a choisi {LIEU6[i]}.",
        f"narrateur|Puis {TOY6[j]}. Puis {SNACK6[k]}.",
        "narrateur|Mila a encore de l'énergie.",
        "papa|Cette énergie n'est pas une faute.",
        "maman|On peut jouer ou attendre.",
        "enfant-m|On joue ou on attend.",
        "papa|On peut demander à un adulte.",
        "enfant-m|Merci, papa.",
        "maman|Bravo, Aniss.",
        "maman|C'est du bon travail.",
        "enfant-f|Merci, maman.",
        "narrateur|Le jardin redevient calme, tout doux.",
        f"narrateur|Aniss se souvient {LIEU6_PRES[i]}, et {TOY6_PRES[j]}.",
    )


def fin_006(i: int, j: int, k: int) -> list[tuple[str, str]]:
    return L(
        "enfant-m|Mila a de l'énergie.",
        "enfant-m|Ce n'est pas une faute.",
        "papa|On a joué ou on a attendu.",
        "maman|Bravo, Aniss.",
        "papa|Tu as fait du bon travail.",
        f"narrateur|Aniss a visité {LIEU6[i]}.",
        f"narrateur|Il a pris {TOY6[j]}.",
        f"narrateur|Il a goûté {SNACK6[k]}.",
        f"narrateur|{FIN_IMG_006[(i, j, k)]}",
        "narrateur|L'histoire est finie.",
    )


def build_006() -> dict:
    by: dict[str, list[tuple[str, str]]] = {
        "CHK_T0000_P0000": debut_006(),
        "CHK_T0001_P0000": tq1_006(),
    }
    for i in (1, 2, 3):
        by[f"CHK_T0001_P000{i}"] = l1_006(i)
        by[f"CHK_T0001_P000{i}_Q0001"] = q_006(i)
        by[f"CHK_T0001_P000{i}_C0001"] = c_006(i)
        by[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_006()
        for j in (1, 2, 3):
            by[f"CHK_T0001_P000{i}_T0002_P000{j}"] = l2_006(i, j)
            by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"] = tq3_006()
            for k in (1, 2, 3):
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"] = l3_006(i, j, k)
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin_006(i, j, k)
    return write_story(
        "TREE-DIF-006",
        {
            "fil_rouge": "L'arrosoir goutte sur la dalle. Aniss rejoint Mila dans le jardin. Mila a beaucoup d'énergie. Ce n'est pas une faute. Ils jouent, ou ils attendent.",
            "title": "Les gouttes de l'arrosoir",
            "characters": "Aniss, Mila, papa, maman",
            "setting": "dans le jardin",
        },
        by,
        {"CHK_T0000_P0000": "enfants_parc"},
    )


# ---------------------------------------------------------------------------
# TREE-DIF-007 — Nino, école, N2 — DIF.BES.001
# L1 chat / chien / poule   L2 bac à sable / toboggan / balançoires   L3 rouge / bleu / vert
# ---------------------------------------------------------------------------

COIN7 = {1: "le chat", 2: "le chien", 3: "la poule"}
COIN7_DE = {1: "du chat", 2: "du chien", 3: "de la poule"}
JEUX7 = {1: "le bac à sable", 2: "le toboggan", 3: "les balançoires"}
JEUX7_PRES = {1: "du bac à sable", 2: "du toboggan", 3: "des balançoires"}
COUL7 = {1: "rouge", 2: "bleu", 3: "vert"}
COUL7_DET = {1: "le rouge", 2: "le bleu", 3: "le vert"}


def debut_007() -> list[tuple[str, str]]:
    return L(
        "narrateur|Un rayon glisse sur le casier.",
        "narrateur|Il touche un bouton de manteau.",
        "narrateur|Le couloir sent le savon, et la banane.",
        "narrateur|Une gouttière cliquette, tout dehors.",
        "narrateur|La vitre a des gouttes, en file.",
        "narrateur|Papa trace une goutte du doigt.",
        "maman|Tu as vu le rayon, Nino ?",
        "enfant-m|Il est tout chaud.",
        "papa|Le bouton brille, hein ?",
        "enfant-m|Oui, papa.",
        "narrateur|Un bateau en papier attend sur le rebord.",
        "narrateur|La craie a laissé un petit nuage.",
        "narrateur|Les crochets font un clic, tout doux.",
        "maman|On accroche le manteau, d'accord ?",
        "enfant-m|D'accord, maman.",
        "narrateur|En ce moment, Nino pose son cartable.",
        "narrateur|Le cartable est encore un peu froid.",
        "narrateur|Un camarade reste près du mur.",
        "narrateur|Il a besoin de calme.",
        "narrateur|Il a besoin de plus de temps.",
        "narrateur|Il regarde d'abord, sans bouger.",
        "maman|On peut répéter la règle.",
        "papa|On peut observer d'abord.",
        "enfant-m|Il ne vient pas encore.",
        "maman|C'est possible. On attend.",
        "papa|On répète la règle, tout doux.",
        "maman|On laisse observer d'abord.",
        "narrateur|Nino hoche la tête.",
        "enfant-m|On répète. On attend.",
        "papa|Bravo, Nino.",
        "maman|C'est du bon travail.",
        "narrateur|Le coin du chat attend.",
        "narrateur|Le coin du chien attend.",
        "narrateur|Le coin de la poule attend.",
        "maman|Tu es prêt ?",
        "enfant-m|Oui, maman.",
    )


def tq1_007() -> list[tuple[str, str]]:
    return L(
        "narrateur|Nino va vers quel coin ?",
        "maman|Le chat, le chien, ou la poule.",
    )


def l1_007(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Nino va vers le coin du chat.",
            "narrateur|Le chat en peluche est tout doux.",
            "narrateur|Un camarade reste au bord.",
            "narrateur|Il observe d'abord.",
            "enfant-m|On touche tout doux.",
            "maman|Oui. Tu répètes la règle.",
            "papa|On peut observer d'abord.",
            "narrateur|Le camarade regarde. Il ne joue pas encore.",
            "maman|C'est bien. On attend.",
            "enfant-m|On répète. On observe d'abord.",
            "papa|Bravo, Nino.",
            "maman|On peut jouer ensemble, plus tard.",
            "narrateur|Le chat en peluche reste au calme.",
        )
    if i == 2:
        return L(
            "narrateur|Nino va vers le coin du chien.",
            "narrateur|Une image de chien est sur le mur.",
            "narrateur|Un camarade a besoin de calme.",
            "narrateur|Il reste près du mur.",
            "enfant-m|On parle tout doux.",
            "papa|Oui. Tu répètes la règle.",
            "maman|On peut observer d'abord.",
            "narrateur|Le camarade écoute. Il regarde l'image.",
            "papa|C'est bien. On laisse le temps.",
            "enfant-m|On répète. On attend.",
            "maman|Bravo. Tu as répété.",
            "papa|On peut jouer ensemble, plus tard.",
            "narrateur|L'image du chien reste, tout calme.",
        )
    return L(
        "narrateur|Nino va vers le coin de la poule.",
        "narrateur|Une image de ferme est sur la table.",
        "narrateur|Un camarade n'entre pas tout de suite.",
        "narrateur|Il observe d'abord.",
        "enfant-m|On reste assis. On attend.",
        "maman|Oui. Tu répètes la règle.",
        "papa|On peut observer d'abord.",
        "narrateur|Le camarade hoche la tête, de loin.",
        "maman|C'est possible. On attend.",
        "enfant-m|On répète. On laisse regarder.",
        "papa|Bravo, Nino.",
        "maman|On peut jouer ensemble, plus tard.",
        "narrateur|La poule de papier reste sur la table.",
    )


def q_007(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|On répète la règle ?",
        )
    if i == 2:
        return L(
            "narrateur|On peut observer d'abord ?",
        )
    return L(
        "narrateur|On répète, ou on attend ?",
    )


def c_007(i: int) -> list[tuple[str, str]]:
    if i == 1:
        return L(
            "narrateur|Oui.",
            "maman|On peut répéter la règle.",
            "papa|On peut observer d'abord.",
            "narrateur|Nino respire, tout calme.",
            "maman|Bravo, Nino.",
            "papa|Tu as fait du bon travail.",
            "enfant-m|Merci, maman.",
            "maman|On continue, tout doux.",
        )
    if i == 2:
        return L(
            "narrateur|Oui.",
            "papa|On peut observer d'abord.",
            "maman|On peut répéter la règle.",
            "narrateur|Nino retient le geste.",
            "papa|Bravo.",
            "papa|Tu as laissé le temps.",
            "enfant-m|Il observe d'abord.",
            "maman|Oui. C'est ça.",
        )
    return L(
        "narrateur|Oui.",
        "maman|On répète. On attend.",
        "papa|On laisse observer d'abord.",
        "narrateur|Nino hoche la tête.",
        "maman|Bravo, Nino.",
        "maman|Tu as fait du bon travail.",
        "enfant-m|Merci, papa.",
        "papa|On continue, tout doux.",
    )


def tq2_007() -> list[tuple[str, str]]:
    return L(
        "narrateur|On joue où, dans la cour ?",
        "papa|Le bac à sable, le toboggan, ou les balançoires.",
    )


def l2_007(i: int, j: int) -> list[tuple[str, str]]:
    coin = COIN7[i]
    if j == 1:
        return L(
            f"narrateur|Nino va vers le bac à sable, après {coin}.",
            "narrateur|Le sable est frais, un peu rêche.",
            "narrateur|Un camarade observe d'abord.",
            "enfant-m|On reste assis. On attend.",
            "maman|Oui. Tu répètes la règle.",
            "papa|On peut observer d'abord.",
            "narrateur|Le camarade regarde le sable, de loin.",
            "maman|C'est bien. On laisse le temps.",
            "enfant-m|On répète. On attend.",
            "papa|Bravo, Nino.",
            "maman|On peut jouer ensemble, plus tard.",
            "narrateur|Un seau attend dans le sable.",
        )
    if j == 2:
        return L(
            f"narrateur|Nino va vers le toboggan, après {coin}.",
            "narrateur|Le plastique est froid, tout lisse.",
            "narrateur|Un camarade observe d'abord.",
            "enfant-m|Un à la fois. On attend.",
            "papa|Oui. Tu répètes la règle.",
            "maman|On peut observer d'abord.",
            "narrateur|Le camarade reste en bas, tout calme.",
            "papa|C'est bien. On laisse regarder.",
            "enfant-m|On répète. On attend.",
            "maman|Bravo. Tu as répété.",
            "papa|On peut jouer ensemble, plus tard.",
            "narrateur|Une feuille colle encore au toboggan.",
        )
    return L(
        f"narrateur|Nino va vers les balançoires, après {coin}.",
        "narrateur|Une chaîne fait un petit clic.",
        "narrateur|Un camarade observe d'abord.",
        "enfant-m|On s'arrête. On attend.",
        "maman|Oui. Tu répètes la règle.",
        "papa|On peut observer d'abord.",
        "narrateur|Le camarade reste au bord, les mains dans les poches.",
        "maman|C'est possible. On attend.",
        "enfant-m|On répète. On laisse regarder.",
        "papa|Bravo, Nino.",
        "maman|On peut jouer ensemble, plus tard.",
        "narrateur|La balançoire vide bouge, tout léger.",
    )


def tq3_007() -> list[tuple[str, str]]:
    return L(
        "narrateur|On prend quelle couleur ?",
        "maman|Le rouge, le bleu, ou le vert.",
    )


OPEN_007 = {
    (1, 1, 1): ("Un seau rouge attend dans le sable.", "Le chat en peluche a un grain de sable."),
    (1, 1, 2): ("Un ruban bleu flotte près du bac.", "Le chat en peluche regarde le sable."),
    (1, 1, 3): ("Une feuille verte colle au seau.", "Le chat en peluche reste au bord."),
    (1, 2, 1): ("Une craie rouge marque le toboggan.", "Le chat en peluche attend en bas."),
    (1, 2, 2): ("Un manteau bleu sèche près du toboggan.", "Le chat en peluche a un poil au vent."),
    (1, 2, 3): ("Un seau vert repose au pied du toboggan.", "Le chat en peluche observe, tout calme."),
    (1, 3, 1): ("Un ruban rouge noue la balançoire.", "Le chat en peluche est sur le banc."),
    (1, 3, 2): ("Un seau bleu attend sous la balançoire.", "Le chat en peluche a fermé un œil."),
    (1, 3, 3): ("Une craie verte trace un trait au sol.", "Le chat en peluche reste près de Nino."),
    (2, 1, 1): ("Un seau rouge sonne dans le sable.", "L'image du chien est encore dans la tête."),
    (2, 1, 2): ("Un galet bleu brille dans le bac.", "Le chien de l'image a l'air calme."),
    (2, 1, 3): ("Une pelle verte repose dans le sable.", "Le camarade regarde encore le chien."),
    (2, 2, 1): ("Une balle rouge attend près du toboggan.", "L'image du chien reste au mur, tout loin."),
    (2, 2, 2): ("Un ruban bleu claque au vent.", "Le toboggan est froid, comme le calme."),
    (2, 2, 3): ("Une feuille verte colle à la rampe.", "Le camarade observe le chien, puis le jeu."),
    (2, 3, 1): ("Un manteau rouge pend près des balançoires.", "Le chien de l'image a une oreille pliée."),
    (2, 3, 2): ("Un seau bleu pose sur le banc.", "La chaîne des balançoires fait clic."),
    (2, 3, 3): ("Un galet vert est sous la balançoire.", "Le camarade a encore besoin de calme."),
    (3, 1, 1): ("Un seau rouge a un peu de sable.", "La poule de papier a une aile pliée."),
    (3, 1, 2): ("Une craie bleue marque le bord du bac.", "La poule de papier regarde le sable."),
    (3, 1, 3): ("Un brin d'herbe vert pique le seau.", "La poule de papier reste sur la table, tout loin."),
    (3, 2, 1): ("Un gobelet rouge attend au toboggan.", "La poule de papier a un point d'œil."),
    (3, 2, 2): ("Un manteau bleu fait un dos de toboggan.", "La poule de papier sent encore la colle."),
    (3, 2, 3): ("Un seau vert sonne, tout creux.", "Le camarade observe la poule, puis le jeu."),
    (3, 3, 1): ("Un ruban rouge danse à la balançoire.", "La poule de papier a une plume peinte."),
    (3, 3, 2): ("Un seau bleu est sous le banc.", "La poule de papier reste dans le souvenir."),
    (3, 3, 3): ("Une craie verte trace un nid, pour de rire.", "La poule de papier a séché, tout calme."),
}

FIN_IMG_007 = {
    (1, 1, 1): "Un grain de sable brille sur le seau rouge.",
    (1, 1, 2): "Le ruban bleu a pris un peu de vent.",
    (1, 1, 3): "La feuille verte a séché sur le seau.",
    (1, 2, 1): "La craie rouge a laissé un trait, tout court.",
    (1, 2, 2): "Le manteau bleu a gardé une odeur de pluie.",
    (1, 2, 3): "Le seau vert a sonné, puis s'est tu.",
    (1, 3, 1): "Le ruban rouge a bougé, tout léger.",
    (1, 3, 2): "Le seau bleu a gardé une goutte.",
    (1, 3, 3): "Le trait vert est encore sur le sol.",
    (2, 1, 1): "Le seau rouge a un cercle de sable.",
    (2, 1, 2): "Le galet bleu est froid, tout lisse.",
    (2, 1, 3): "La pelle verte a une trace de main.",
    (2, 2, 1): "La balle rouge s'est arrêtée, tout calme.",
    (2, 2, 2): "Le ruban bleu s'est endormi au vent.",
    (2, 2, 3): "La feuille verte reste collée, tout doux.",
    (2, 3, 1): "Le manteau rouge a un bouton qui brille.",
    (2, 3, 2): "Le seau bleu a fait un dernier clic.",
    (2, 3, 3): "Le galet vert a une tache d'eau.",
    (3, 1, 1): "Le seau rouge a gardé un peu de terre.",
    (3, 1, 2): "La craie bleue s'est usée, tout petit.",
    (3, 1, 3): "Le brin d'herbe vert a plié, puis repris.",
    (3, 2, 1): "Le gobelet rouge a une goutte, au fond.",
    (3, 2, 2): "Le manteau bleu a séché au soleil.",
    (3, 2, 3): "Le seau vert est rentré près du mur.",
    (3, 3, 1): "Le ruban rouge s'est dénoué, tout doux.",
    (3, 3, 2): "Le seau bleu a dormi sous le banc.",
    (3, 3, 3): "Le nid vert de craie reste au sol.",
}


def l3_007(i: int, j: int, k: int) -> list[tuple[str, str]]:
    a, b = OPEN_007[(i, j, k)]
    return L(
        f"narrateur|{a}",
        f"narrateur|{b}",
        f"narrateur|Nino a choisi {COIN7[i]}.",
        f"narrateur|Puis {JEUX7[j]}. Puis {COUL7[k]}.",
        "narrateur|Le camarade a encore besoin de calme.",
        "maman|On peut répéter la règle.",
        "papa|On peut observer d'abord.",
        "enfant-m|On répète. On attend.",
        "maman|On laisse observer d'abord.",
        "enfant-m|Merci, maman.",
        "papa|Bravo, Nino.",
        "papa|C'est du bon travail.",
        "narrateur|La cour redevient calme, tout doux.",
        f"narrateur|Nino se souvient {COIN7_DE[i]}, et {JEUX7_PRES[j]}.",
    )


def fin_007(i: int, j: int, k: int) -> list[tuple[str, str]]:
    return L(
        "enfant-m|J'ai répété la règle.",
        "enfant-m|Il a observé d'abord.",
        "maman|Bravo, Nino.",
        "papa|Tu as fait du bon travail.",
        f"narrateur|Nino a visité le coin {COIN7_DE[i]}.",
        f"narrateur|Il a joué à {JEUX7[j]}.",
        f"narrateur|Il a pris {COUL7_DET[k]}.",
        f"narrateur|{FIN_IMG_007[(i, j, k)]}",
        "narrateur|L'histoire est finie.",
    )


def sons_007() -> dict[str, str]:
    out: dict[str, str] = {}
    # premier embranchement chien + toutes les feuilles du chien
    out["CHK_T0001_P0000"] = "chien_bonjour"
    out["CHK_T0001_P0002"] = "chien_bonjour"
    for j in (1, 2, 3):
        out[f"CHK_T0001_P0002_T0002_P000{j}"] = "chien_bonjour"
        for k in (1, 2, 3):
            out[f"CHK_T0001_P0002_T0002_P000{j}_T0003_P000{k}"] = "chien_bonjour"
    return out


def build_007() -> dict:
    by: dict[str, list[tuple[str, str]]] = {
        "CHK_T0000_P0000": debut_007(),
        "CHK_T0001_P0000": tq1_007(),
    }
    for i in (1, 2, 3):
        by[f"CHK_T0001_P000{i}"] = l1_007(i)
        by[f"CHK_T0001_P000{i}_Q0001"] = q_007(i)
        by[f"CHK_T0001_P000{i}_C0001"] = c_007(i)
        by[f"CHK_T0001_P000{i}_T0002_P0000"] = tq2_007()
        for j in (1, 2, 3):
            by[f"CHK_T0001_P000{i}_T0002_P000{j}"] = l2_007(i, j)
            by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000"] = tq3_007()
            for k in (1, 2, 3):
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}"] = l3_007(i, j, k)
                by[f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001"] = fin_007(i, j, k)
    return write_story(
        "TREE-DIF-007",
        {
            "fil_rouge": "Un rayon touche le casier. Nino accroche son manteau. Un camarade a besoin de calme. Nino répète la règle. On laisse observer d'abord.",
            "title": "Le rayon sur le casier",
            "characters": "Nino, papa, maman",
            "setting": "à l'école",
        },
        by,
        sons_007(),
    )


def main() -> None:
    d6 = build_006()
    d7 = build_007()
    e6 = check_story(d6, ["énergie", "pas une faute", "jouer ou attendre"], 15)
    e7 = check_story(d7, ["répéter", "observer d'abord"], 15)
    if e6 or e7:
        msg = ""
        if e6:
            msg += "TREE-DIF-006\n" + "\n".join(e6[:40]) + f"\n({len(e6)} erreurs)\n"
        if e7:
            msg += "TREE-DIF-007\n" + "\n".join(e7[:40]) + f"\n({len(e7)} erreurs)\n"
        raise SystemExit(msg)
    print("ok", d6["story_id"], len(d6["chunks"]), d6["chunks"][0]["text"].split(".")[0] + ".")
    print("ok", d7["story_id"], len(d7["chunks"]), d7["chunks"][0]["text"].split(".")[0] + ".")


if __name__ == "__main__":
    main()
