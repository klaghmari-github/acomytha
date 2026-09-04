#!/usr/bin/env python3
"""F-NAR-008 — merged.json ATOM-COL.POL.001-11..13 et ATOM-DIF.BES.001-01..05."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 18}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "maitresse"}
FORBIDDEN = (
    "on va apprendre",
    "voici le geste",
    "papa sourit",
    "maman sourit",
    "papa est là",
    "maman est là",
    "il était une fois",
    "ceci est l'histoire",
    "aujourd'hui,",
    "ne le dis pas",
    "tu as fait du bon travail",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom", "léa", "lea", "lina", "iris",
    "denis", "hadrien", "sylvain", "sami", "fatou", "idris", "flora",
    "constentin", "luca", "céline", "celine", "lucas", "georges",
    "honoré", "honore", "lise", "zoé", "zoe", "léo", "leo",
    "amina", "clément", "clement", "bérénice", "berenice",
    "olympe", "swann", "nora", "kenzo",
)


def words(s: str) -> int:
    return len(s.replace("'", " ").replace("’", " ").replace("-", " ").split())


def from_script(lines: list[str]) -> tuple[str, str]:
    phrases, out = [], []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        role, phrase = raw.split("|", 1)
        phrase = phrase.strip()
        out.append(f"{role}|{phrase}")
        phrases.append(phrase)
    return " ".join(phrases), "\n".join(out)


def scales(age: str, kind: str) -> tuple[float, str]:
    if age == "N1":
        if kind == "passage_question":
            return 1.4, "slow"
        if kind == "passage_fin":
            return 1.36, "slow"
        return 1.28, "slow"
    if age == "N2":
        if kind == "passage_question":
            return 1.3, "slow"
        if kind == "passage_fin":
            return 1.26, "slow"
        return 1.22, "medium"
    if kind == "passage_question":
        return 1.24, "medium"
    if kind == "passage_fin":
        return 1.2, "medium"
    return 1.22, "medium"


KEEP = (
    "chunk_id",
    "kind",
    "text",
    "script",
    "sons",
    "length_scale_piper",
    "rate_label",
    "pause_after_ms",
    "expected_answer",
    "accepted_examples",
    "retry_prompt",
)


def make_chunk(src: dict, lines: list[str], sons, age: str, qmeta: dict | None) -> dict:
    text, script = from_script(lines)
    nc = {k: src.get(k) for k in KEEP if k in src}
    nc["chunk_id"] = src["chunk_id"]
    nc["kind"] = src.get("kind")
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else ""
    if nc["sons"] is None:
        nc["sons"] = ""
    ls, rl = scales(age, src.get("kind") or "")
    nc["length_scale_piper"] = ls
    nc["rate_label"] = rl
    if qmeta:
        nc.update(qmeta)
    else:
        nc.pop("expected_answer", None)
        nc.pop("accepted_examples", None)
        nc.pop("retry_prompt", None)
    return nc


def check(sid: str, age: str, chunks: list[dict], need_msgs: tuple[str, ...]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if re.search(r"\b" + re.escape(name) + r"\b", low):
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "bon travail" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in need_msgs:
        if m.lower() not in all_text:
            raise SystemExit(f"{sid}: message manquant: {m}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    bravo_n = aj.count("bravo") + aj.count("bon travail")
    if bravo_n > 3:
        raise SystemExit(f"{sid}: trop de bravo ({bravo_n})")
    for c in chunks:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: text ≠ script")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                raise SystemExit(f"{sid} ligne sans | : {ln}")
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                raise SystemExit(f"{sid} rôle {role}")
            n = words(phrase)
            if n > lim:
                raise SystemExit(f"{sid} {c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    p0 = chunks[0]["text"].lower()
    if "l'histoire est finie" in p0:
        raise SystemExit(f"{sid}: fin collée dans P0000")
    print(f"OK {sid} {nwords} mots")


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    qmeta: dict,
    need: tuple[str, ...],
    secondary: str = "",
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    age = src.get("age_band") or "N2"
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        by[cid] = make_chunk(
            c,
            scripts[cid],
            sons.get(cid, ""),
            age,
            qmeta if cid.endswith("Q0001") else None,
        )
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    if secondary:
        out["secondary_lessons"] = secondary
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, age, out["chunks"], need)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


NEED_POL = ("bonjour", "s'il te plaît", "merci")
NEED_DIF = ("répéter", "observer d'abord")


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-11 N3 Chouchou — ballon rouge sous les lampions
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-11",
    "Chouchou veut le ballon rouge qui tire sur sa ficelle. Il dit bonjour, s'il te plaît, merci. Le ballon tape le lampion jusqu'à la fenêtre.",
    "Le ballon rouge de Chouchou",
    "Chouchou, papa, maman",
    "place du village, lampions, puis fenêtre",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un lampion rouge se balance sous la corde.",
            "narrateur|La corde va d'un platane à l'autre.",
            "narrateur|La poussière de la place sent encore la pluie.",
            "narrateur|Les dalles sont froides, un peu brillantes.",
            "narrateur|Un accordéon joue tout bas, derrière un stand.",
            "narrateur|Une ficelle danse au-dessus d'une caisse.",
            "narrateur|Le ballon au bout est rouge, tout tendu.",
            "maman|Tu as vu la ficelle, Chouchou ?",
            "enfant-m|Elle tire.",
            "enfant-m|Le ballon veut partir.",
            "maman|Il est bien rouge.",
            "enfant-m|Je le veux.",
            "enfant-m|Celui qui danse.",
            "narrateur|Le vent soulève un peu de papier.",
            "narrateur|Ça sent le sucre filé, tout près.",
            "narrateur|Une miette colle au bord d'une table.",
            "maman|On essuie tes mains, d'abord.",
            "maman|Voilà.",
            "narrateur|En ce moment, Chouchou tient le panier de maman.",
            "narrateur|Le panier est léger, encore vide.",
            "narrateur|Ils s'arrêtent devant la caisse.",
            "narrateur|Le monsieur du stand parle encore.",
            "narrateur|Il range des ficelles bleues.",
            "maman|On attend un petit moment.",
            "maman|Il a les mains prises.",
            "enfant-m|Le rouge, maman.",
            "enfant-m|Il tape la caisse.",
            "maman|Oui.",
            "maman|Celui-là.",
            "narrateur|Le lampion penche au-dessus d'eux.",
            "narrateur|Une ombre ronde passe sur le nez de Chouchou.",
            "narrateur|Le monsieur pose la dernière ficelle.",
            "narrateur|Il se tourne.",
            "maman|Tu demandes, Chouchou.",
            "narrateur|La ficelle rouge tremble encore.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Chouchou veut le ballon.",
            "narrateur|Que dit-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-m|Bonjour.",
            "maman|Bonjour.",
            "enfant-m|Le ballon rouge, s'il te plaît.",
            "enfant-m|Celui qui tire.",
            "narrateur|Le monsieur détache la ficelle.",
            "narrateur|Le ballon monte un peu, puis s'arrête.",
            "narrateur|Chouchou tient le bout, des deux mains.",
            "enfant-m|Merci.",
            "maman|Merci.",
            "narrateur|Le rouge tape le lampion, tout doux.",
            "narrateur|Ça fait un petit bruit de papier.",
            "maman|Il est à toi, maintenant.",
            "enfant-m|Il est chaud du soleil.",
            "maman|Un peu, oui.",
            "narrateur|Plus loin, un moulinet de papier attend.",
            "narrateur|Il est jaune, avec une tige de bois.",
            "narrateur|Il tourne dès qu'on souffle.",
            "maman|Tu en veux un, aussi ?",
            "enfant-m|Oui.",
            "narrateur|La dame du stand écoute.",
            "enfant-m|Bonjour.",
            "enfant-m|Le moulinet jaune, s'il te plaît.",
            "narrateur|La dame pose la tige dans sa main.",
            "enfant-m|Merci.",
            "maman|Tu as demandé, tout clair.",
            "maman|Bravo, Chouchou.",
            "narrateur|Le moulinet tourne contre le ballon.",
            "narrateur|Le jaune chatouille le rouge.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils quittent la place, tout doucement.",
            "narrateur|Le ballon tape chaque lampion, un par un.",
            "enfant-m|Il dit bonjour aux lampions.",
            "maman|On dirait, oui.",
            "narrateur|Les dalles sèchent sous leurs pas.",
            "narrateur|L'accordéon devient plus loin.",
            "narrateur|À la maison, papa ouvre la fenêtre.",
            "papa|C'est un vrai soleil, ça.",
            "enfant-m|C'est mon ballon.",
            "papa|Tu l'as demandé ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Bonjour.",
            "enfant-m|S'il te plaît.",
            "enfant-m|Merci.",
            "papa|Et le moulinet ?",
            "enfant-m|Il tourne sur le rebord.",
            "maman|On le pose près de la vitre.",
            "narrateur|Le ballon touche le bois, tout léger.",
            "narrateur|Le moulinet prend le vent de la rue.",
            "papa|Il reste avec nous, ce soir.",
            "enfant-m|Oui.",
            "enfant-m|Il est rouge.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le ballon repose contre la fenêtre.",
            "narrateur|Le lampion de la place n'est plus là.",
            "maman|Bonne soirée, Chouchou.",
            "papa|Le rouge est rentré.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "marche,corde",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "papier",
        "CHK_T0000_P0000_END": "pas,fenetre",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "s'il te plaît",
        "accepted_examples": "s'il te plaît | merci | bonjour | s'il te plait",
        "retry_prompt": "Il dit s'il te plaît. Que dit Chouchou ?",
    },
    NEED_POL,
    "COL.ECO.002",
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-12 N3 Mila — œuf chaud à la ferme
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-12",
    "Mila veut un œuf encore chaud pour le gâteau. À la poule, puis au lait de chèvre, elle dit bonjour, s'il te plaît, merci.",
    "L'œuf encore chaud de Mila",
    "Mila, papa, maman",
    "cour de ferme, paille, puis cuisine",
    {
        "CHK_T0000_P0000": [
            "narrateur|La paille pique un peu sous les sandales.",
            "narrateur|Une poule rousse picore près du seau.",
            "narrateur|Le seau sent le grain, tout sec.",
            "narrateur|Le soleil chauffe le bois de la porte.",
            "narrateur|Une plume reste collée au loquet.",
            "maman|Tu as vu la plume, Mila ?",
            "enfant-f|Elle est douce.",
            "enfant-f|Elle est un peu chaude.",
            "maman|Le soleil l'a chauffée.",
            "enfant-f|Je veux un œuf.",
            "enfant-f|Pour le gâteau de papa.",
            "maman|Un œuf encore chaud, alors.",
            "narrateur|La cour sent le foin coupé.",
            "narrateur|Une goutte tombe du robinet de zinc.",
            "narrateur|Elle fait un rond dans la poussière.",
            "maman|On marche doucement.",
            "maman|La poule est près du nid.",
            "narrateur|En ce moment, Mila tient le petit panier.",
            "narrateur|Le panier sent encore le linge propre.",
            "narrateur|Un torchon blanc est plié au fond.",
            "narrateur|La dame de la ferme essuie ses mains.",
            "narrateur|Elle a de la paille sur le tablier.",
            "maman|On attend un peu.",
            "maman|Elle range le grain.",
            "enfant-f|Le nid est là.",
            "enfant-f|Il est dans l'ombre.",
            "maman|Oui.",
            "narrateur|Un œuf brun brille sous la paille.",
            "narrateur|Il a des taches plus claires.",
            "enfant-f|Celui-là.",
            "enfant-f|Il est tout rond.",
            "narrateur|La dame pose le seau.",
            "narrateur|Elle se tourne vers elles.",
            "maman|Tu demandes, Mila.",
            "narrateur|L'œuf attend dans la paille.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila veut l'œuf.",
            "narrateur|Que dit-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-f|Bonjour.",
            "maman|Bonjour.",
            "enfant-f|L'œuf brun, s'il te plaît.",
            "enfant-f|Celui du nid.",
            "narrateur|La dame glisse la main sous la paille.",
            "narrateur|Elle pose l'œuf sur le torchon.",
            "narrateur|Le torchon se creuse un peu.",
            "enfant-f|Merci.",
            "maman|Merci.",
            "enfant-f|Il est chaud, maman.",
            "maman|Comme un petit soleil.",
            "narrateur|Mila pose les deux mains autour.",
            "narrateur|La chaleur passe à travers le linge.",
            "narrateur|Plus loin, une chèvre sonne sa cloche.",
            "narrateur|Le lait attend dans un pot de verre.",
            "maman|Un peu de lait, pour la pâte ?",
            "enfant-f|Oui.",
            "narrateur|Ils s'arrêtent près de la barrière.",
            "enfant-f|Bonjour.",
            "enfant-f|Un peu de lait, s'il te plaît.",
            "narrateur|La dame verse le lait, tout blanc.",
            "narrateur|Le pot devient lourd dans le panier.",
            "enfant-f|Merci.",
            "maman|Tu as demandé deux fois.",
            "maman|Bravo, Mila.",
            "narrateur|La poule picore encore, derrière eux.",
            "narrateur|La cloche de la chèvre s'éloigne.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sur le chemin, le panier penche un peu.",
            "narrateur|L'œuf roule contre le pot, tout doux.",
            "enfant-f|Il est encore chaud.",
            "maman|On marche sans sauter.",
            "narrateur|La paille laisse une odeur sur les sandales.",
            "narrateur|À la maison, papa a déjà le saladier.",
            "papa|Vous avez l'œuf ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il était dans le nid.",
            "papa|Il sent la paille, encore.",
            "maman|Et le lait est là.",
            "narrateur|Papa casse l'œuf au-dessus du bol.",
            "narrateur|Le jaune tombe, tout rond.",
            "enfant-f|C'est pour le gâteau.",
            "papa|Tu l'as demandé, Mila ?",
            "enfant-f|Bonjour.",
            "enfant-f|S'il te plaît.",
            "enfant-f|Merci.",
            "papa|Le gâteau va sentir la ferme.",
            "maman|Un peu le grain, un peu le lait.",
            "narrateur|La plume du loquet n'est plus là.",
            "narrateur|Le saladier est jaune, maintenant.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le saladier repose sur la table.",
            "narrateur|L'œuf n'est plus dans le nid.",
            "maman|Bonne après-midi, Mila.",
            "papa|Le gâteau va cuire.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "poule,paille",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "cloche",
        "CHK_T0000_P0000_END": "bol,pas",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "s'il te plaît",
        "accepted_examples": "s'il te plaît | merci | bonjour | s'il te plait",
        "retry_prompt": "Elle dit s'il te plaît. Que dit Mila ?",
    },
    NEED_POL,
    "COL.ECO.002",
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-13 N1 Victorino — cacao derrière la vitre
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-13",
    "Victorino veut la tasse de cacao derrière la vitre. Il dit bonjour, s'il te plaît, merci. La mousse laisse un point sur son nez.",
    "Le cacao de Victorino",
    "Victorino, papa, maman",
    "café du village, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|La vapeur fait un nuage sur la vitre.",
            "narrateur|Un petit rond s'ouvre, puis se referme.",
            "narrateur|Ça sent le cacao, tout chaud.",
            "narrateur|Une cuillère tinte contre une tasse.",
            "narrateur|Le store rayé claque, dehors.",
            "papa|Tu as vu le nuage, Victorino ?",
            "enfant-m|Il s'ouvre.",
            "enfant-m|Puis il part.",
            "papa|C'est la vapeur du cacao.",
            "narrateur|Le trottoir est encore un peu mouillé.",
            "narrateur|Une feuille collée brille près du pas.",
            "papa|On essuie tes chaussures.",
            "papa|Voilà.",
            "enfant-m|J'ai les joues froides.",
            "papa|On entre.",
            "papa|Tu restes près de moi.",
            "narrateur|En ce moment, Victorino tient la manche.",
            "narrateur|La cloche de la porte fait ding.",
            "narrateur|L'air est chaud, comme un câlin.",
            "narrateur|Le bois du comptoir est lisse.",
            "narrateur|De la mousse blanche dort dans une tasse.",
            "enfant-m|Celle-là.",
            "enfant-m|Elle a de la mousse.",
            "papa|Le cacao bien chaud.",
            "narrateur|La dame essuie encore une tasse.",
            "narrateur|Le torchon est à carreaux rouges.",
            "papa|On attend un peu.",
            "papa|Elle a les mains prises.",
            "narrateur|Victorino regarde la tasse.",
            "narrateur|Il avance le doigt vers la vitre.",
            "enfant-m|Je veux celle-là.",
            "papa|Tu demandes, Victorino.",
            "narrateur|La dame se tourne.",
            "narrateur|Un peu de mousse est sur son tablier.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorino veut le cacao.",
            "narrateur|Que dit-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-m|Bonjour.",
            "papa|Bonjour.",
            "enfant-m|Un cacao, s'il te plaît.",
            "enfant-m|Avec la mousse.",
            "narrateur|La dame pose la tasse.",
            "narrateur|La mousse tremble un peu.",
            "narrateur|Ça sent le chocolat, tout près.",
            "enfant-m|Merci.",
            "papa|Merci.",
            "papa|Tu as demandé, Victorino.",
            "papa|Bravo.",
            "narrateur|Victorino tient l'anse des deux mains.",
            "narrateur|La chaleur passe dans ses doigts.",
            "enfant-m|Elle est chaude, papa.",
            "papa|On souffle un peu.",
            "narrateur|Il souffle.",
            "narrateur|La mousse fait un petit trou.",
            "enfant-m|Un point sur mon nez.",
            "papa|Oui.",
            "papa|Un point de mousse.",
            "narrateur|La cuillère tinte encore.",
            "narrateur|Le store claque, dehors.",
            "papa|On dit au revoir, maintenant.",
            "enfant-m|Au revoir.",
            "papa|Au revoir.",
            "narrateur|La cloche fait ding, encore.",
            "narrateur|L'air froid revient sur les joues.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sur le chemin, le foulard sent le cacao.",
            "papa|Tu as encore le point ?",
            "enfant-m|Un peu.",
            "enfant-m|Il est sucré.",
            "papa|On le laisse.",
            "narrateur|La feuille n'est plus sur le pas.",
            "narrateur|Le store rayé claque loin derrière.",
            "narrateur|À la maison, ça sent déjà la soupe.",
            "maman|Vous sentez le chocolat ?",
            "enfant-m|C'est mon foulard.",
            "enfant-m|J'ai bu le cacao.",
            "maman|Tu as demandé, Victorino ?",
            "enfant-m|Bonjour.",
            "enfant-m|S'il te plaît.",
            "enfant-m|Merci.",
            "papa|La mousse a fait un point.",
            "maman|Sur le nez ?",
            "enfant-m|Oui, maman.",
            "maman|Il n'est plus là.",
            "enfant-m|Il est dans le foulard.",
            "papa|Le nuage de la vitre est parti.",
            "narrateur|Victorino pose le foulard sur la chaise.",
            "narrateur|Ça sent encore le cacao, tout bas.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le foulard repose sur la chaise.",
            "narrateur|Il sent encore le cacao.",
            "maman|Bonne soirée, Victorino.",
            "papa|La tasse était chaude.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cloche,tasse",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "tasse,cuillere",
        "CHK_T0000_P0000_END": "pas,porte",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "s'il te plaît",
        "accepted_examples": "s'il te plaît | merci | bonjour | s'il te plait",
        "retry_prompt": "Il dit s'il te plaît. Que dit Victorino ?",
    },
    NEED_POL,
    "COL.ECO.002",
)


# ---------------------------------------------------------------------------
# ATOM-DIF.BES.001-01 N2 Sarah — carte tortue jusqu'au soleil
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-01",
    "Sarah veut faire marcher la carte tortue jusqu'au soleil de la vitre. Raphaël reste près du mur. Elle répète. Il observe d'abord. La tortue arrive.",
    "La tortue de Sarah",
    "Sarah, Raphaël, papa, maman",
    "classe, tapis, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un soleil de doigt dort sur la vitre.",
            "narrateur|Il a trois rayons, un peu flous.",
            "narrateur|Le tapis sent encore le savon.",
            "narrateur|Une carte dépasse d'un sac.",
            "narrateur|C'est une oreille de chat, toute grise.",
            "papa|Tu as vu le soleil, Sarah ?",
            "enfant-f|Il est sur la vitre.",
            "enfant-f|Il a trois rayons.",
            "papa|Oui.",
            "papa|Un petit soleil de doigt.",
            "narrateur|En ce moment, papa ouvre la porte.",
            "narrateur|Sarah entre avec lui.",
            "narrateur|Les chaussures font un bruit doux.",
            "enfant-f|Je veux la tortue.",
            "enfant-f|Elle va jusqu'au soleil.",
            "papa|Tu la fais marcher, alors.",
            "narrateur|Des cartes d'animaux attendent sur le tapis.",
            "narrateur|Un sac est ouvert, tout bas.",
            "narrateur|Raphaël reste près du mur.",
            "narrateur|Ses mains touchent le crépi, tout doux.",
            "narrateur|Il ne vient pas encore.",
            "enfant-f|Raphaël.",
            "enfant-f|Tu viens ?",
            "narrateur|Raphaël ne bouge pas.",
            "narrateur|Il regarde le sac, sans avancer.",
            "papa|Il a besoin de calme.",
            "papa|Tu peux dire comment on joue.",
            "narrateur|Sarah s'arrête au bord du tapis.",
            "narrateur|La carte du chat dépasse encore.",
            "narrateur|Le soleil de doigt attend sur la vitre.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Raphaël a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah va près du mur.",
            "narrateur|Elle parle tout doux.",
            "enfant-f|On pioche une carte.",
            "enfant-f|On fait marcher l'animal.",
            "enfant-f|Puis on repose.",
            "papa|Tu as su répéter.",
            "narrateur|Raphaël écoute.",
            "narrateur|Il va observer d'abord.",
            "narrateur|Il reste près du mur.",
            "narrateur|Sarah retourne au tapis.",
            "narrateur|Elle pioche le chat.",
            "narrateur|Elle marche sur la pointe, tout lentement.",
            "narrateur|Raphaël suit des yeux.",
            "narrateur|Il ne joue pas encore.",
            "papa|Observer d'abord, c'est possible.",
            "narrateur|Plus tard, Raphaël tend la main.",
            "narrateur|Il pioche une carte.",
            "narrateur|C'est la tortue.",
            "enfant-f|Elle va au soleil.",
            "narrateur|Raphaël avance très lentement.",
            "narrateur|Sarah laisse l'espace.",
            "narrateur|La tortue arrive sous la vitre.",
            "narrateur|Le soleil de doigt a un peu bougé.",
            "papa|Bravo, Sarah.",
            "papa|Tu as laissé le temps.",
            "enfant-f|La tortue est arrivée.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sarah range le sac.",
            "narrateur|Raphaël range la tortue, tout doux.",
            "papa|Tu as fini de ranger, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Raphaël fait un petit signe.",
            "enfant-f|À demain.",
            "narrateur|Les chaussures attendent près de la porte.",
            "narrateur|Le soir, la maison sent la soupe.",
            "maman|Tu as joué aux cartes ?",
            "enfant-f|La tortue a marché.",
            "enfant-f|Jusqu'au soleil.",
            "maman|Raphaël était avec toi ?",
            "enfant-f|Il a regardé d'abord.",
            "papa|Sarah a répété la règle.",
            "maman|C'est pour ça, alors.",
            "narrateur|Le soleil de doigt n'est plus à la maison.",
            "narrateur|Il est resté sur la vitre de la classe.",
            "enfant-f|La tortue l'a rejoint.",
            "maman|Oui.",
            "maman|Tout doucement.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La soupe fume encore un peu.",
            "narrateur|La tortue est restée à l'école.",
            "maman|Bonne soirée, Sarah.",
            "papa|Le soleil avait trois rayons.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "porte_classe,tapis",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "cartes",
        "CHK_T0000_P0000_END": "porte,soupe",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "répéter",
        "accepted_examples": "répéter | observer d'abord | observer | attendre",
        "retry_prompt": "On peut répéter. On peut observer d'abord. Que fait-on ?",
    },
    NEED_DIF,
)


# ---------------------------------------------------------------------------
# ATOM-DIF.BES.001-02 N3 Amir — escargot de pâte
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-02",
    "Amir veut un escargot de pâte, tout en spirale. Victorina regarde d'abord. Le soir, un oiseau de cartes. Même calme, autre table.",
    "L'escargot de pâte d'Amir",
    "Amir, Victorina, papa, maman",
    "atelier de pâte, puis nappe à la maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|La cour sent l'herbe coupée.",
            "narrateur|Un arrosoir goutte sous le robinet.",
            "narrateur|Dans l'atelier, la table est froide.",
            "narrateur|Un rouleau de bois attend, tout lisse.",
            "narrateur|Un morceau de pâte a déjà une oreille.",
            "maman|Tu as vu l'oreille, Amir ?",
            "enfant-m|Elle sèche.",
            "enfant-m|Près de la fenêtre.",
            "maman|Oui.",
            "maman|On en fait un autre.",
            "enfant-m|Je veux un escargot.",
            "enfant-m|Tout en spirale.",
            "maman|Une boule, puis on roule.",
            "narrateur|En ce moment, Amir arrive à la table.",
            "narrateur|La pâte est froide sous les doigts.",
            "narrateur|Elle sent un peu la farine.",
            "enfant-m|Elle est molle.",
            "maman|Oui.",
            "maman|Froide et molle.",
            "narrateur|Victorina reste près de la table.",
            "narrateur|Elle regarde les mains, sans bouger.",
            "narrateur|Ses doigts restent sur le bord.",
            "narrateur|Elle ne prend pas encore de pâte.",
            "enfant-m|Victorina.",
            "enfant-m|Tu viens ?",
            "narrateur|Victorina ne vient pas encore.",
            "maman|Elle a besoin de calme.",
            "maman|Tu peux dire la règle.",
            "narrateur|L'arrosoir goutte encore, dehors.",
            "narrateur|La spirale n'est pas commencée.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir va près d'elle.",
            "narrateur|Il parle tout doux.",
            "enfant-m|Une boule.",
            "enfant-m|Puis on aplatit.",
            "enfant-m|Puis on roule la spirale.",
            "maman|Tu as su répéter.",
            "narrateur|Victorina écoute.",
            "narrateur|Elle va observer d'abord.",
            "narrateur|Amir roule une boule douce.",
            "narrateur|Il l'aplatit avec la paume.",
            "narrateur|Il enroule un long boudin.",
            "narrateur|La spirale devient un escargot.",
            "narrateur|Victorina suit des yeux.",
            "maman|Observer d'abord, c'est possible.",
            "narrateur|Plus tard, elle pose un doigt.",
            "narrateur|Elle aplatit un tout petit palet.",
            "enfant-m|C'est une coquille, ça.",
            "maman|Bravo, Amir.",
            "maman|Tu as laissé le temps.",
            "narrateur|Le soir, à la maison, papa sort un jeu.",
            "narrateur|Des cartes d'oiseaux sur la nappe.",
            "papa|Tu te souviens, Amir ?",
            "enfant-m|On pioche.",
            "enfant-m|On montre.",
            "enfant-m|On pose.",
            "narrateur|C'est répéter, encore.",
            "narrateur|Victorina observe d'abord.",
            "narrateur|Puis elle pioche une carte.",
            "narrateur|C'est un oiseau bleu.",
            "papa|Même calme.",
            "papa|Autre table.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|L'escargot sèche sur une assiette.",
            "narrateur|La spirale tient, tout nette.",
            "papa|Tu as fini de ranger les cartes, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|L'oiseau bleu est reposé.",
            "enfant-m|Victorina a regardé d'abord.",
            "papa|Oui.",
            "papa|À l'atelier, puis ici.",
            "narrateur|La lampe fait un rond jaune.",
            "narrateur|Le rond touche l'assiette.",
            "maman|On dirait une coquille, aussi.",
            "enfant-m|Comme l'escargot.",
            "papa|On a pris le temps.",
            "narrateur|L'arrosoir ne goutte plus.",
            "narrateur|La nappe redevient lisse.",
            "enfant-m|La spirale est à moi.",
            "maman|Oui.",
            "maman|Elle sèche jusqu'à demain.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|L'escargot repose sur l'assiette.",
            "narrateur|La spirale est sèche, presque.",
            "maman|Bonne soirée, Amir.",
            "papa|L'oiseau bleu est rangé.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "pate,robinet",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "pate,cartes",
        "CHK_T0000_P0000_END": "assiette,cartes",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "répéter",
        "accepted_examples": "répéter | observer d'abord | observer | attendre | répéter la règle",
        "retry_prompt": "On peut répéter. On peut observer d'abord. Que fait-on ?",
    },
    NEED_DIF,
)


# ---------------------------------------------------------------------------
# ATOM-DIF.BES.001-03 N3 Nina — chemin de galets
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-03",
    "Nina veut un chemin de galets jusqu'à l'escargot. Raphaël reste au banc. Elle répète. Il observe d'abord. Le chemin arrive.",
    "Le chemin de galets de Nina",
    "Nina, Raphaël, papa, maman",
    "jardin après la pluie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une gouttière chante encore, tout fin.",
            "narrateur|L'eau tombe dans un seau de zinc.",
            "narrateur|Le seau a un cercle de mousse.",
            "narrateur|Des galets luisent dans la terre noire.",
            "narrateur|On dirait des bonbons mouillés.",
            "maman|Tu as vu le seau, Nina ?",
            "enfant-f|Il a de la mousse.",
            "enfant-f|Tout autour.",
            "maman|La pluie l'a laissée.",
            "enfant-f|Je veux un chemin.",
            "enfant-f|Jusqu'à l'escargot.",
            "maman|Un galet après l'autre, alors.",
            "narrateur|L'escargot avance sur une pierre.",
            "narrateur|Très lentement.",
            "narrateur|L'herbe mouillée colle aux chaussures.",
            "narrateur|Ça sent la terre, tout près.",
            "narrateur|Une feuille collée brille sur le banc.",
            "maman|Tu as senti la terre ?",
            "enfant-f|Oui.",
            "enfant-f|Elle est mouillée.",
            "narrateur|En ce moment, Nina est au jardin.",
            "narrateur|Maman essuie le banc avec la main.",
            "narrateur|Le bois reste froid et sombre.",
            "narrateur|Raphaël reste près du banc.",
            "narrateur|Ses mains restent sur le bois mouillé.",
            "enfant-f|Raphaël.",
            "enfant-f|Tu viens ?",
            "narrateur|Raphaël ne vient pas encore.",
            "maman|Il a besoin de calme.",
            "maman|Tu peux dire comment on pose.",
            "narrateur|Un galet gris brille près du pied de Nina.",
            "narrateur|L'escargot n'a presque pas bougé.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Raphaël a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina va vers le banc.",
            "narrateur|Elle parle tout doux.",
            "enfant-f|On pose un galet.",
            "enfant-f|On dit une couleur.",
            "maman|Tu as su répéter.",
            "narrateur|Raphaël écoute.",
            "narrateur|Il va observer d'abord.",
            "narrateur|Nina pose un galet gris.",
            "enfant-f|Gris.",
            "narrateur|Le galet fait un petit bruit sur la terre.",
            "narrateur|Raphaël suit des yeux.",
            "maman|Observer d'abord, c'est possible.",
            "narrateur|Nina pose un galet brun.",
            "enfant-f|Brun.",
            "narrateur|Le chemin avance vers la pierre.",
            "narrateur|Plus tard, Raphaël prend un galet bleu.",
            "narrateur|Il le pose, tout doux.",
            "enfant-f|Bleu.",
            "maman|Bravo, Nina.",
            "maman|Tu as laissé le temps.",
            "narrateur|Le dernier galet touche la pierre.",
            "narrateur|L'escargot est encore là.",
            "enfant-f|Le chemin est arrivé.",
            "maman|Oui.",
            "maman|Sans le presser.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Un oiseau chante dans l'arbre.",
            "papa|J'ai entendu, depuis la cuisine.",
            "papa|Vous avez fait un chemin ?",
            "enfant-f|Jusqu'à l'escargot.",
            "papa|Il est encore sur sa pierre ?",
            "enfant-f|Oui, papa.",
            "maman|Raphaël a regardé d'abord.",
            "papa|Nina a répété la règle.",
            "maman|Tu as fini de ranger, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina donne la main.",
            "narrateur|Raphaël donne l'autre main.",
            "narrateur|Les chaussures laissent des traces mouillées.",
            "narrateur|La gouttière chante plus bas, maintenant.",
            "enfant-f|Les galets sont froids.",
            "papa|Ils vont sécher.",
            "maman|Le seau a encore sa mousse.",
            "narrateur|L'escargot n'a presque pas bougé.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le chemin brille encore un peu.",
            "narrateur|L'escargot reste sur sa pierre.",
            "maman|Bonne fin de journée, Nina.",
            "papa|Le seau chante tout fin.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "gouttiere,jardin",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "galets",
        "CHK_T0000_P0000_END": "oiseau,pas",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "répéter",
        "accepted_examples": "répéter | observer | observer d'abord | la règle",
        "retry_prompt": "On peut répéter. On peut observer d'abord. Que fait-on ?",
    },
    NEED_DIF,
)


# ---------------------------------------------------------------------------
# ATOM-DIF.BES.001-04 N1 Nino — tour jusqu'au rayon
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-04",
    "Nino veut une tour qui touche le rayon. Victorina reste près du canapé. Il répète. Elle observe d'abord. Un cube, puis la tour.",
    "La tour de Nino",
    "Nino, Victorina, papa, maman",
    "salon, tapis, canapé",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le doudou a glissé entre deux coussins.",
            "narrateur|Une oreille dépasse, toute molle.",
            "narrateur|Ça sent le cacao du goûter, encore.",
            "narrateur|L'horloge pose un tic, puis un tac.",
            "narrateur|Un cube rouge brille près du canapé.",
            "maman|Tu as vu l'oreille, Nino ?",
            "enfant-m|Le doudou attend.",
            "maman|Oui.",
            "maman|Entre les coussins.",
            "enfant-m|Je veux une tour.",
            "enfant-m|Qui touche la lumière.",
            "maman|Une tour de cubes, alors.",
            "narrateur|Un rayon passe sur le tapis.",
            "narrateur|Il est pâle, un peu long.",
            "narrateur|Le rideau bouge un peu.",
            "maman|Tu as vu le rideau ?",
            "enfant-m|Il fait du vent.",
            "maman|Un tout petit vent.",
            "narrateur|En ce moment, Nino est au salon.",
            "narrateur|D'autres cubes sont là.",
            "narrateur|Bleus.",
            "narrateur|Verts.",
            "narrateur|Ils sont lisses, un peu froids.",
            "narrateur|Victorina reste près du canapé.",
            "narrateur|Elle tient le bord du tissu.",
            "enfant-m|Victorina.",
            "enfant-m|Tu viens ?",
            "narrateur|Victorina ne vient pas encore.",
            "maman|Elle a besoin de calme.",
            "maman|Tu peux dire comment on pose.",
            "narrateur|Le cube jaune se cache sous le canapé.",
            "narrateur|Le rayon attend sur le tapis.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino va près du canapé.",
            "narrateur|Il parle tout doux.",
            "enfant-m|Un cube.",
            "enfant-m|Puis un autre.",
            "enfant-m|Tout doux.",
            "maman|Tu as su répéter.",
            "narrateur|Victorina écoute.",
            "narrateur|Elle va observer d'abord.",
            "narrateur|Nino pose un cube bleu.",
            "narrateur|Le cube fait un petit bruit.",
            "narrateur|Victorina regarde.",
            "maman|Observer d'abord, c'est possible.",
            "narrateur|Nino pose un cube vert.",
            "narrateur|La tour monte un peu.",
            "narrateur|Plus tard, Victorina tend la main.",
            "narrateur|Elle pose le cube rouge.",
            "enfant-m|Encore un.",
            "narrateur|Nino glisse le cube jaune.",
            "narrateur|Celui du canapé.",
            "narrateur|Il le pose tout en haut.",
            "narrateur|La tour touche le rayon.",
            "maman|Bravo, Nino.",
            "maman|Tu as laissé le temps.",
            "enfant-m|Elle touche la lumière.",
            "maman|Oui.",
            "narrateur|Le cube jaune brille un peu.",
            "narrateur|Victorina pose une main à plat.",
            "enfant-m|On n'avance plus.",
            "maman|On regarde, maintenant.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Le doudou a encore l'oreille dehors.",
            "papa|Je rentre.",
            "papa|C'est une belle tour.",
            "enfant-m|Elle touche le rayon.",
            "papa|Le cube jaune est le toit.",
            "maman|Victorina a regardé d'abord.",
            "papa|Nino a répété.",
            "maman|Tu as fini de ranger tes cubes ?",
            "enfant-m|Oui, maman.",
            "narrateur|Victorina range le cube rouge.",
            "narrateur|Nino range le bleu.",
            "enfant-m|Le jaune aussi.",
            "papa|Le tapis redevient plat.",
            "narrateur|L'horloge fait tic-tac, encore.",
            "narrateur|Le cacao n'est plus dans l'air.",
            "maman|Le doudou attend toujours.",
            "enfant-m|Je le mets sur le canapé.",
            "papa|Voilà.",
            "narrateur|L'oreille n'est plus coincée.",
            "enfant-m|Il est avec nous.",
            "maman|Oui.",
            "maman|Sur le coussin.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le doudou est sur le canapé.",
            "narrateur|La tour n'est plus là.",
            "maman|Bonne fin d'après-midi, Nino.",
            "papa|Le rayon a bougé.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cubes,horloge",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "cubes",
        "CHK_T0000_P0000_END": "cubes,porte",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "répéter",
        "accepted_examples": "répéter | observer d'abord | observer | attendre",
        "retry_prompt": "On peut répéter. On peut observer d'abord. Que fait-on ?",
    },
    NEED_DIF,
)


# ---------------------------------------------------------------------------
# ATOM-DIF.BES.001-05 N2 Aniss — bulle jusqu'à la chemise
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-05",
    "Aniss veut une bulle qui va jusqu'à la chemise bleue. Il reste près du mur. Il observe d'abord. La bulle part, puis se pose.",
    "La bulle d'Aniss",
    "Aniss, Raphaël, papa, maman",
    "cour, linge, bol de savon",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le linge claque sur la corde.",
            "narrateur|Une goutte tombe d'une chemise bleue.",
            "narrateur|Le savon sent la fleur, dans le bol.",
            "narrateur|Un cercle irisé tremble au bord.",
            "narrateur|La cour est encore chaude.",
            "maman|Tu as vu la chemise, Aniss ?",
            "enfant-m|Elle est bleue.",
            "enfant-m|Une goutte tombe.",
            "maman|Oui.",
            "maman|Le linge sèche.",
            "enfant-m|Je veux une bulle.",
            "enfant-m|Jusqu'à la chemise.",
            "maman|On souffle tout doux, alors.",
            "narrateur|Une pince à linge brille au soleil.",
            "maman|Tu as vu la pince ?",
            "enfant-m|Elle est jaune.",
            "maman|Oui.",
            "maman|Elle tient la manche.",
            "narrateur|En ce moment, Aniss rentre de l'école.",
            "narrateur|La classe était un peu bruyante.",
            "narrateur|Il reste près du mur.",
            "narrateur|Le mur est chaud sous sa main.",
            "narrateur|Raphaël tient déjà l'anneau.",
            "narrateur|L'anneau goutte un peu de savon.",
            "enfant-m|J'attends un peu.",
            "maman|Tu as besoin de calme.",
            "maman|On peut dire comment on souffle.",
            "narrateur|Le cercle irisé tremble encore.",
            "narrateur|La chemise bleue attend sur la corde.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "maman|On trempe l'anneau.",
            "maman|On souffle tout doux.",
            "narrateur|Maman vient de répéter.",
            "narrateur|Aniss va observer d'abord.",
            "narrateur|Raphaël trempe l'anneau.",
            "narrateur|Il souffle une petite bulle.",
            "narrateur|La bulle part, puis crève.",
            "narrateur|Aniss suit des yeux.",
            "narrateur|Il ne souffle pas encore.",
            "maman|Observer d'abord, c'est possible.",
            "narrateur|Plus tard, Aniss tend la main.",
            "narrateur|Il prend l'anneau.",
            "narrateur|Le savon est froid, un peu glissant.",
            "enfant-m|Je souffle.",
            "narrateur|Une bulle ronde se détache.",
            "narrateur|Elle va vers la chemise bleue.",
            "narrateur|Elle se pose, une seconde.",
            "enfant-m|Elle est arrivée.",
            "maman|Bravo, Aniss.",
            "maman|Tu as regardé, puis soufflé.",
            "narrateur|Un rond mouillé reste sur le bleu.",
            "narrateur|Puis il s'en va.",
            "enfant-m|Elle a touché la manche.",
            "maman|Oui.",
            "maman|Une seconde, pas plus.",
            "narrateur|Raphaël pose l'anneau au bord du bol.",
            "narrateur|Le savon sent encore la fleur.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Papa ouvre le portail.",
            "papa|Ça sent le savon, ici.",
            "enfant-m|J'ai fait une bulle.",
            "enfant-m|Jusqu'à la chemise.",
            "papa|Elle est encore là ?",
            "enfant-m|Un rond, puis plus rien.",
            "maman|Aniss a observé d'abord.",
            "papa|Puis il a soufflé.",
            "maman|Tu as fini de tenir l'anneau ?",
            "enfant-m|Oui, maman.",
            "narrateur|L'anneau rentre dans le bol.",
            "narrateur|Le savon fait un petit ploc.",
            "papa|Le linge claque encore.",
            "enfant-m|La chemise est presque sèche.",
            "maman|On rentre les pinces, maintenant.",
            "narrateur|La cour redevient calme.",
            "narrateur|Le mur n'est plus si chaud.",
            "enfant-m|La pince jaune aussi.",
            "papa|Oui.",
            "papa|Avec les autres.",
            "narrateur|Une goutte tombe encore, puis plus.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le bol repose près du robinet.",
            "narrateur|La chemise bleue sèche encore.",
            "maman|Bonne fin de journée, Aniss.",
            "papa|La bulle a fait un rond.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "linge,savon",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "bulle",
        "CHK_T0000_P0000_END": "portail,linge",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "répéter",
        "accepted_examples": "répéter | observer | observer d'abord | la règle",
        "retry_prompt": "On répète la règle. Aniss peut quoi d'abord ?",
    },
    NEED_DIF,
)
