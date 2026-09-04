#!/usr/bin/env python3
"""F-NAR-009 — merged.json pour 8 atomiques SEC.ADU.002 / SEC.MAI.001."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 18}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}
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
    "dans la prise",
    "dans une prise",
    "ne mets pas",
    "ne touche pas",
    "étranger",
    "inconnu",
    "se perd",
    "tu te perds",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom ", "léa", "lea ", "lina", "iris",
    "myriam", "diane", "domitille", "hadrien", "dahlia", "adam",
    "loïc", "loic", "noé", "noe", "ava", "pablo",
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


def make_chunk(src: dict, lines: list[str], sons) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    return nc


def check(sid: str, age: str, chunks: list[dict], need_msgs: tuple[str, ...]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if re.search(rf"\b{re.escape(name.strip())}\b", low):
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
    if "en ce moment" not in all_text:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie." not in all_text:
        raise SystemExit(f"{sid}: manque fin")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad_open in ("joue au salon", "est dans l'entrée", "c'est le matin", "aujourd'hui"):
        if first.startswith(bad_open) or bad_open in first[:40]:
            raise SystemExit(f"{sid} ouverture brute: {first}")
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
    print(f"OK {sid} {nwords} mots  1re: {chunks[0]['script'].splitlines()[0].split('|', 1)[1]}")


def write_story(sid: str, fil: str, title: str, chars: str, setting: str,
                scripts: dict, sons: dict) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""))
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    age = out["age_band"]
    need = {
        "SEC.ADU.002": ("rester avec l'accompagnant",),
        "SEC.MAI.001": ("appeler un adulte", "mains avec les jouets"),
    }[out["lesson_id"]]
    check(sid, age, out["chunks"], need)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# ATOM-SEC.ADU.002-04 N3 Mila, maman, marché puis bibliothèque
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.ADU.002-04",
    "Les tentes claquent. Les cerises brillent. Puis les livres sentent le papier. Mila reste avec l'accompagnant, au marché et à la bibliothèque.",
    "Les cerises et le livre de papier",
    "Mila, maman",
    "marché du village puis bibliothèque",
    {
        "CHK_T0000_P0000": [
            "narrateur|Les tentes du marché claquent un peu.",
            "narrateur|Le vent les pousse, tout doux.",
            "narrateur|Une tache rouge brille sur une caisse.",
            "narrateur|C'est du jus de cerise.",
            "narrateur|Le pavé est encore un peu mouillé.",
            "narrateur|Ça sent le pain, tout près.",
            "narrateur|Une balance fait tic.",
            "narrateur|Puis encore tic.",
            "narrateur|Un cabas sent le linge propre.",
            "narrateur|Mila vit ici, avec maman.",
            "enfant-f|Maman, la tente claque !",
            "maman|Oui.",
            "maman|C'est le vent.",
            "maman|Tu vois les cerises ?",
            "enfant-f|Oui.",
            "enfant-f|Elles sont toutes rouges.",
            "narrateur|En ce moment, elles marchent sous la tente.",
            "narrateur|Maman tient la main de Mila.",
            "narrateur|La main est douce, un peu chaude.",
            "narrateur|Les pieds de Mila restent près.",
            "narrateur|Maman est l'accompagnant.",
            "narrateur|Mila aime rester avec l'accompagnant.",
            "maman|Tu restes avec moi ?",
            "enfant-f|Oui, maman.",
            "maman|Bravo.",
            "maman|Tu restes avec l'adulte connu.",
            "narrateur|Elles s'arrêtent devant les cerises.",
            "narrateur|Une cerise a une petite queue.",
            "narrateur|Elle brille comme un bijou.",
            "enfant-f|Elle est trop rouge !",
            "maman|Oui.",
            "maman|On en prend un peu.",
            "narrateur|Maman choisit les cerises.",
            "narrateur|Mila reste à côté.",
            "narrateur|Ses pieds restent près des pieds de maman.",
            "maman|Tu restes bien près.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Le sac en papier fait un petit bruit.",
            "narrateur|Il sent le fruit sucré.",
            "enfant-f|Ça sent bon.",
            "maman|Oui.",
            "maman|Ça sent les cerises.",
            "narrateur|Elles paient à la balance.",
            "narrateur|La balance fait encore tic.",
            "maman|On reste ensemble.",
            "enfant-f|Je reste avec l'accompagnant.",
            "maman|Oui.",
            "maman|Bravo, Mila.",
            "narrateur|Plus tard, le pavé devient plus calme.",
            "narrateur|Elles marchent vers la bibliothèque.",
            "narrateur|La main de maman reste dans la main de Mila.",
            "narrateur|Les pieds restent près.",
            "narrateur|La porte de la bibliothèque est lourde.",
            "narrateur|Elle fait un petit souffle.",
            "narrateur|Le tapis cache les pas.",
            "narrateur|Ça sent le papier, tout doux.",
            "enfant-f|Ça sent les livres !",
            "maman|Oui.",
            "maman|Tu restes avec moi, ici aussi.",
            "narrateur|Mila se souvient.",
            "narrateur|Ici aussi, elle reste près.",
            "narrateur|Elle reste avec l'accompagnant.",
            "narrateur|Elle reste à côté de maman.",
            "narrateur|Un livre a une couverture bleue.",
            "narrateur|Une poule jaune est dessus.",
            "enfant-f|La poule !",
            "maman|On le prend ensemble ?",
            "enfant-f|Oui.",
            "narrateur|Maman prend le livre.",
            "narrateur|Mila reste tout près.",
            "maman|Tu restes avec l'adulte connu.",
            "enfant-f|Oui, maman.",
            "maman|Bravo.",
            "narrateur|Elles s'assoient un moment.",
            "narrateur|Le banc est lisse, un peu froid.",
            "narrateur|Maman ouvre une page.",
            "narrateur|Le papier est mat, tout calme.",
            "maman|Tu es bien près de moi ?",
            "enfant-f|Oui.",
            "enfant-f|Je reste avec l'accompagnant.",
            "maman|C'est du bon travail.",
            "narrateur|Elles referment le livre.",
            "narrateur|Le sac de cerises pèse un peu.",
            "narrateur|Elles sortent ensemble.",
            "narrateur|Le vent touche encore les tentes, au loin.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila est au marché, puis à la bibliothèque.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila reste avec maman.",
            "narrateur|Au marché, puis à la bibliothèque.",
            "narrateur|Maman est l'accompagnant.",
            "maman|Tu restes avec l'accompagnant ?",
            "enfant-f|Oui.",
            "enfant-f|Avec toi.",
            "maman|Bravo, Mila.",
            "maman|Tu restes avec l'adulte connu.",
            "narrateur|Le livre bleu reste dans le cabas.",
            "narrateur|Les cerises sentent encore le sucre.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sur le chemin, le pavé sèche.",
            "maman|Tu tiens encore ma main ?",
            "enfant-f|Oui, maman.",
            "maman|Bravo.",
            "narrateur|Elles rentrent à la maison.",
            "narrateur|Le cabas pose un bruit doux.",
            "maman|Tu as fini de marcher près de moi ?",
            "enfant-f|Oui.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Une cerise roule un peu dans le sac.",
            "narrateur|Le livre bleu attend sur la table.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Je suis restée avec maman.",
            "maman|Avec l'accompagnant.",
            "maman|Bravo.",
            "maman|C'est du bon travail.",
            "narrateur|Les tentes du marché se taisent.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "marche,livres",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
)


# ---------------------------------------------------------------------------
# ATOM-SEC.ADU.002-05 N2 Nina, papa, marché aux pommes
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.ADU.002-05",
    "Une caisse sent la pomme. Une feuille reste collée. Nina marche près de papa. Elle reste avec l'accompagnant.",
    "La caisse qui sent la pomme",
    "Nina, papa",
    "marché, caisses de pommes, balance",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une caisse de bois sent la pomme.",
            "narrateur|Le bois est rêche, un peu humide.",
            "narrateur|Une feuille verte reste collée.",
            "narrateur|Elle est sur une pomme rouge.",
            "narrateur|Une flaque brille entre les étals.",
            "narrateur|La balance fait un petit tic.",
            "narrateur|Un sac en papier attend, tout plat.",
            "narrateur|Nina vit ici, avec papa.",
            "enfant-f|Papa, ça sent la pomme !",
            "papa|Oui.",
            "papa|Les caisses sont pleines.",
            "papa|Tu vois la feuille verte ?",
            "enfant-f|Oui.",
            "enfant-f|Elle est collée.",
            "narrateur|En ce moment, ils marchent entre les étals.",
            "narrateur|Papa tient la main de Nina.",
            "narrateur|La main est chaude.",
            "narrateur|Les pieds de Nina restent près.",
            "narrateur|Papa est l'accompagnant.",
            "narrateur|Nina aime rester avec l'accompagnant.",
            "papa|Tu restes avec moi ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|Tu restes avec l'adulte connu.",
            "narrateur|Ils s'arrêtent devant les pommes.",
            "narrateur|Une pomme rouge dépasse.",
            "narrateur|Elle a encore sa petite feuille.",
            "enfant-f|Celle-là, papa !",
            "papa|On la prend ensemble.",
            "narrateur|Papa choisit les pommes.",
            "narrateur|Nina reste à côté.",
            "narrateur|Ses pieds restent près des pieds de papa.",
            "papa|Tu restes bien près.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Le sac en papier se froisse.",
            "narrateur|Il fait un bruit de feuille sèche.",
            "enfant-f|Ça froisse !",
            "papa|Oui.",
            "papa|Le sac est content.",
            "narrateur|Ils écoutent le marchand.",
            "narrateur|La voix est ronde, tout près.",
            "narrateur|Nina reste avec papa.",
            "narrateur|L'adulte connu reste près.",
            "enfant-f|Je reste avec l'accompagnant.",
            "papa|Oui.",
            "papa|Bravo, Nina.",
            "narrateur|Papa prend le sac.",
            "narrateur|Le sac pèse un peu.",
            "narrateur|Nina reste à côté.",
            "papa|On rentre ensemble ?",
            "enfant-f|Oui.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|La flaque fait un petit miroir.",
            "narrateur|Les chaussures font un bruit mouillé.",
            "papa|Tu tiens encore ma main ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "narrateur|Parce qu'elle reste près, la main est douce.",
            "narrateur|Rester avec l'accompagnant, c'est rester près.",
            "narrateur|Nina est calme.",
            "narrateur|Le sac sent encore le jardin.",
            "narrateur|La feuille verte tremble un peu.",
            "papa|On est bien ensemble.",
            "enfant-f|Oui.",
            "narrateur|Le marché devient plus calme, derrière eux.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nina est au marché.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina reste avec papa.",
            "narrateur|Papa est l'accompagnant.",
            "papa|Tu restes avec l'accompagnant ?",
            "enfant-f|Oui.",
            "enfant-f|Avec toi.",
            "papa|Bravo, Nina.",
            "papa|Tu restes avec l'adulte connu.",
            "narrateur|Le sac de pommes pèse encore.",
            "narrateur|La feuille verte est toujours là.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|À la maison, le sac pose un bruit doux.",
            "papa|Tu as marché près de moi ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Nina touche une pomme.",
            "narrateur|Elle est lisse, un peu froide.",
            "papa|Tu restes avec moi, au marché.",
            "enfant-f|Oui.",
            "narrateur|La caisse de bois n'est plus là.",
            "narrateur|Mais l'odeur de pomme reste.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Je suis restée avec papa.",
            "papa|Avec l'accompagnant.",
            "papa|Bravo.",
            "papa|C'est du bon travail.",
            "narrateur|La feuille verte repose sur la table.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "marche",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
)


# ---------------------------------------------------------------------------
# ATOM-SEC.ADU.002-06 N2 Victorina, papa, bibliothèque
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.ADU.002-06",
    "Un signet dépasse. Le tapis cache les pas. Victorina choisit un album bleu. Elle reste avec l'accompagnant.",
    "Le signet dans le gros livre",
    "Victorina, papa",
    "bibliothèque, tapis, albums colorés",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un signet dépasse d'un gros livre.",
            "narrateur|Il est rouge, tout mince.",
            "narrateur|Le tapis cache les pas.",
            "narrateur|On n'entend presque plus les chaussures.",
            "narrateur|Un rayon de soleil glisse entre les rayons.",
            "narrateur|La poussière y danse, tout doux.",
            "narrateur|Ça sent le papier et le bois.",
            "narrateur|Victorina vit ici, avec papa.",
            "enfant-f|Papa, le signet dépasse !",
            "papa|Oui.",
            "papa|Il garde la page.",
            "papa|Tu vois le rayon de soleil ?",
            "enfant-f|Oui.",
            "enfant-f|Il est tout jaune.",
            "narrateur|En ce moment, ils marchent entre les livres.",
            "narrateur|Papa tient la main de Victorina.",
            "narrateur|La main est chaude.",
            "narrateur|Les pieds de Victorina restent près.",
            "narrateur|Papa est l'accompagnant.",
            "narrateur|Victorina aime rester avec l'accompagnant.",
            "papa|Tu restes avec moi ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|Tu restes avec l'adulte connu.",
            "narrateur|Ils voient des livres colorés.",
            "narrateur|Un album a une couverture bleue.",
            "narrateur|Un bateau blanc est dessus.",
            "enfant-f|Le bateau !",
            "papa|On le regarde ensemble.",
            "narrateur|Papa prend l'album.",
            "narrateur|Victorina reste à côté.",
            "narrateur|Ses pieds restent près des pieds de papa.",
            "papa|Tu restes bien près.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Ils s'assoient sur un coussin.",
            "narrateur|Le coussin est mou, un peu froid.",
            "narrateur|Papa ouvre l'album.",
            "narrateur|Les pages sentent le papier neuf.",
            "enfant-f|Ça sent le livre.",
            "papa|Oui.",
            "papa|Tout calme.",
            "narrateur|Victorina reste avec papa.",
            "narrateur|L'adulte connu reste près.",
            "enfant-f|Je reste avec l'accompagnant.",
            "papa|Oui.",
            "papa|Bravo, Victorina.",
            "narrateur|Une page montre une vague.",
            "narrateur|La vague est bleue, tout ronde.",
            "papa|Tu vois la vague ?",
            "enfant-f|Oui.",
            "enfant-f|Elle est bleue.",
            "narrateur|Ils regardent encore un peu.",
            "narrateur|Parce qu'elle reste près, c'est facile.",
            "narrateur|Rester avec l'accompagnant, c'est rester près.",
            "papa|On emprunte l'album ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa prend l'album sous le bras.",
            "narrateur|Victorina reste à côté.",
            "papa|Tu tiens encore ma main ?",
            "enfant-f|Oui.",
            "papa|Bravo.",
            "narrateur|Ils marchent vers la porte.",
            "narrateur|Le tapis est encore tout silencieux.",
            "narrateur|Le signet rouge reste dans le gros livre.",
            "narrateur|Le rayon de soleil a bougé un peu.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina est à la bibliothèque.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorina reste avec papa.",
            "narrateur|Papa est l'accompagnant.",
            "papa|Tu restes avec l'accompagnant ?",
            "enfant-f|Oui.",
            "enfant-f|Avec toi.",
            "papa|Bravo, Victorina.",
            "papa|Tu restes avec l'adulte connu.",
            "narrateur|L'album bleu pèse un peu.",
            "narrateur|Le bateau blanc reste sur la couverture.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Dehors, l'air est plus vif.",
            "papa|Tu as marché près de moi ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Ils rentrent avec l'album.",
            "narrateur|Ils marchent ensemble.",
            "papa|Tu restes avec moi, à la bibliothèque.",
            "enfant-f|Oui.",
            "narrateur|Le tapis de la maison est plus chaud.",
            "narrateur|L'album attend sur les genoux.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Je suis restée avec papa.",
            "papa|Avec l'accompagnant.",
            "papa|Bravo.",
            "papa|C'est du bon travail.",
            "narrateur|Le signet garde encore sa page.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "livres",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
)


# ---------------------------------------------------------------------------
# ATOM-SEC.ADU.002-07 N2 Raphaël, maman, marché aux fleurs
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.ADU.002-07",
    "L'eau clapote dans un seau. Un pétale rose colle à la chaussure. Raphaël reste avec l'accompagnant, près des tulipes.",
    "Le pétale collé à la chaussure",
    "Raphaël, maman",
    "marché aux fleurs, seaux, tulipes et roses",
    {
        "CHK_T0000_P0000": [
            "narrateur|L'eau clapote dans un seau vert.",
            "narrateur|Les tiges trempent, toutes droites.",
            "narrateur|Un pétale rose colle à une chaussure.",
            "narrateur|Il est tout mouillé, tout léger.",
            "narrateur|Le pavé brille, encore humide.",
            "narrateur|Ça sent les roses, tout fort.",
            "narrateur|Une tulipe rouge penche un peu.",
            "narrateur|Raphaël vit ici, avec maman.",
            "enfant-m|Maman, l'eau clapote !",
            "maman|Oui.",
            "maman|Les fleurs boivent.",
            "maman|Tu vois le pétale, sur ta chaussure ?",
            "enfant-m|Oui.",
            "enfant-m|Il est rose.",
            "narrateur|En ce moment, ils marchent entre les seaux.",
            "narrateur|Maman tient la main de Raphaël.",
            "narrateur|La main est chaude.",
            "narrateur|Les pieds de Raphaël restent près.",
            "narrateur|Maman est l'accompagnant.",
            "narrateur|Raphaël aime rester avec l'accompagnant.",
            "maman|Tu restes avec moi ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "maman|Tu restes avec l'adulte connu.",
            "narrateur|Ils voient des tulipes.",
            "narrateur|Les tulipes sont rouges et jaunes.",
            "narrateur|Une feuille lisse touche le seau.",
            "enfant-m|Elles sont droites !",
            "maman|Oui.",
            "maman|Toutes droites, dans l'eau.",
            "narrateur|Maman choisit un bouquet.",
            "narrateur|Raphaël reste à côté.",
            "narrateur|Ses pieds restent près des pieds de maman.",
            "narrateur|Les mains restent dans la main de maman.",
            "maman|Tu restes bien près.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Ils sentent les roses.",
            "narrateur|L'odeur est douce, un peu sucrée.",
            "enfant-m|Ça sent bon !",
            "maman|Oui.",
            "maman|Ça sent les roses.",
            "narrateur|Raphaël reste avec maman.",
            "narrateur|L'adulte connu reste près.",
            "enfant-m|Je reste avec l'accompagnant.",
            "maman|Oui.",
            "maman|Bravo, Raphaël.",
            "narrateur|Maman prend le bouquet.",
            "narrateur|Le papier autour fait un petit bruit.",
            "narrateur|Raphaël reste à côté.",
            "maman|On rentre ensemble ?",
            "enfant-m|Oui.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|Le pétale voyage encore sur la chaussure.",
            "narrateur|Le pavé fait un bruit mouillé.",
            "maman|Tu tiens encore ma main ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "narrateur|Parce qu'il reste près, c'est simple.",
            "narrateur|Rester avec l'accompagnant, c'est rester près.",
            "narrateur|Raphaël est calme.",
            "narrateur|Le bouquet penche un peu.",
            "maman|Les pieds restent près.",
            "enfant-m|Oui.",
            "narrateur|Le seau vert clapote encore, derrière eux.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Raphaël est au marché.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Raphaël reste avec maman.",
            "narrateur|Maman est l'accompagnant.",
            "narrateur|La main est tenue.",
            "narrateur|Les pieds restent près.",
            "maman|Tu restes avec l'accompagnant ?",
            "enfant-m|Oui.",
            "enfant-m|Avec toi.",
            "maman|Bravo, Raphaël.",
            "maman|Tu restes avec l'adulte connu.",
            "narrateur|Le bouquet sent encore les roses.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|À la maison, le bouquet va dans l'eau.",
            "maman|Tu as marché près de moi ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Raphaël enlève le pétale de sa chaussure.",
            "narrateur|Il est encore un peu mouillé.",
            "maman|Tu restes avec moi, au marché.",
            "enfant-m|Oui.",
            "narrateur|Les tulipes se tiennent droites.",
            "narrateur|L'eau de la carafe est calme.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Je suis resté avec maman.",
            "maman|Avec l'accompagnant.",
            "maman|Bravo.",
            "maman|C'est du bon travail.",
            "narrateur|Le pétale sèche sur le rebord.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "marche,fleurs",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
)


# ---------------------------------------------------------------------------
# ATOM-SEC.MAI.001-01 N2 Sarah, chambre, cubes, lumière
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.MAI.001-01",
    "Un cube jaune garde un carré de soleil. Le linge sent le savon. Sarah veut plus de lumière. Elle va appeler un adulte. Les mains avec les jouets.",
    "Le cube jaune et la lumière",
    "Sarah, maman, papa",
    "chambre, cubes au sol, linge près de la porte",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un cube jaune garde un carré de soleil.",
            "narrateur|Le soleil est déjà plus bas.",
            "narrateur|Le linge sent le savon, près de la porte.",
            "narrateur|Une chaussette pend d'une chaise.",
            "narrateur|Elle fait un petit drapeau mou.",
            "narrateur|Le tapis de la chambre est épais.",
            "narrateur|Les cubes sont par terre, tout calmes.",
            "narrateur|Sarah vit ici, avec papa et maman.",
            "enfant-f|Maman, le cube est tout jaune !",
            "maman|Oui.",
            "maman|Il a pris le soleil.",
            "maman|Tu vois la chaussette ?",
            "enfant-f|Oui.",
            "enfant-f|Elle pend.",
            "narrateur|En ce moment, Sarah construit une tour.",
            "narrateur|Un cube rouge.",
            "narrateur|Puis un cube bleu.",
            "narrateur|La pièce devient un peu sombre.",
            "narrateur|Le carré de soleil a bougé.",
            "enfant-f|Maman, la lumière.",
            "narrateur|Sarah regarde ses mains.",
            "narrateur|Les mains avec les jouets.",
            "narrateur|Sarah appelle maman.",
            "narrateur|On va appeler un adulte.",
            "maman|J'arrive, Sarah.",
            "narrateur|Maman vient.",
            "narrateur|Maman allume.",
            "narrateur|La pièce devient claire.",
            "narrateur|Le cube jaune brille encore plus.",
            "papa|Tu as appelé un adulte ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo, Sarah.",
            "papa|On appelle papa ou maman pour la lumière.",
            "maman|Les prises sont pour les adultes.",
            "maman|Les mains avec les jouets.",
            "narrateur|Sarah reprend un cube jaune.",
            "narrateur|Elle le pose sur la tour.",
            "narrateur|La tour est petite, un peu penchée.",
            "enfant-f|Elle est haute !",
            "maman|Oui.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Parce qu'elle a appelé, la lumière est là.",
            "narrateur|Les mains tiennent les jouets.",
            "papa|Tu construis encore ?",
            "enfant-f|Oui.",
            "narrateur|Papa s'assoit près d'elle.",
            "narrateur|Le tapis est doux sous les genoux.",
            "maman|Tu as fini de plier le linge, toi ?",
            "papa|Presque.",
            "narrateur|Sarah ajoute un cube bleu.",
            "narrateur|Il fait un petit toc.",
            "maman|Tes mains sont avec les jouets ?",
            "enfant-f|Oui, maman.",
            "maman|Bravo.",
            "narrateur|La chaussette pend encore.",
            "narrateur|Le savon du linge sent toujours.",
            "narrateur|La pièce reste claire.",
            "enfant-f|J'ai appelé un adulte.",
            "papa|Oui.",
            "papa|C'est bien.",
            "narrateur|Sarah est calme.",
            "narrateur|La tour tient, tout doux.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah veut la lumière.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah a appelé un adulte.",
            "narrateur|Les mains avec les jouets.",
            "maman|Tu as appelé un adulte ?",
            "enfant-f|Oui.",
            "enfant-f|Maman.",
            "papa|Bravo, Sarah.",
            "papa|Tu as fait du bon travail.",
            "maman|Les prises sont pour les adultes.",
            "narrateur|Le cube jaune reste en haut.",
            "narrateur|La lumière reste allumée.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sarah pose un dernier cube.",
            "narrateur|La tour ne penche plus.",
            "maman|Tu ranges un cube, maintenant ?",
            "enfant-f|Un peu.",
            "narrateur|Elle pose le cube rouge dans la boîte.",
            "maman|Tu as fini de ranger ce cube ?",
            "enfant-f|Oui.",
            "maman|Bravo.",
            "papa|La lumière reste allumée.",
            "narrateur|La chaussette rejoint le linge.",
            "narrateur|Ça sent encore le savon.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|J'ai appelé un adulte.",
            "enfant-f|Les mains avec les jouets.",
            "maman|Bravo.",
            "papa|C'est du bon travail.",
            "narrateur|Le cube jaune garde encore un peu de soleil.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cubes",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
)


# ---------------------------------------------------------------------------
# ATOM-SEC.MAI.001-02 N1 Amir, salon, voitures, lumière
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.MAI.001-02",
    "Le rideau bouge. Une voiture rouge attend. Amir veut la lumière. Il va appeler un adulte. Les mains avec les jouets.",
    "La petite voiture sous le rideau",
    "Amir, papa, maman",
    "salon, rideau, voitures rouges, linge",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le rideau bouge, tout doux.",
            "narrateur|Un peu de vent.",
            "narrateur|Le salon sent le linge.",
            "narrateur|Papa plie une serviette.",
            "narrateur|Elle est encore un peu chaude.",
            "narrateur|Une voiture rouge attend.",
            "narrateur|Elle est sous la table.",
            "narrateur|Le tapis est doux, un peu épais.",
            "narrateur|Un rayon glisse sur le bois.",
            "narrateur|Il est long, tout pâle.",
            "narrateur|Amir vit ici.",
            "narrateur|Avec papa et maman.",
            "narrateur|Une autre voiture attend.",
            "narrateur|Elle est bleue, près du canapé.",
            "enfant-m|Papa, le rideau bouge !",
            "papa|Oui.",
            "papa|C'est le vent.",
            "papa|Tu vois ta voiture ?",
            "enfant-m|Oui.",
            "enfant-m|Elle est rouge.",
            "narrateur|En ce moment, Amir joue.",
            "narrateur|Il tient la voiture.",
            "narrateur|Il la pose sur le tapis.",
            "narrateur|La pièce est un peu sombre.",
            "narrateur|Le rayon pâle ne suffit plus.",
            "enfant-m|Papa, la lumière.",
            "narrateur|Amir regarde ses mains.",
            "narrateur|Les mains avec les jouets.",
            "narrateur|Amir appelle papa.",
            "narrateur|On va appeler un adulte.",
            "papa|J'arrive, Amir.",
            "narrateur|Papa vient.",
            "narrateur|Papa allume.",
            "narrateur|La pièce est claire.",
            "maman|Tu as appelé un adulte ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo, Amir.",
            "maman|On appelle papa ou maman.",
            "papa|Les prises sont pour les adultes.",
            "papa|Les mains avec les jouets.",
            "narrateur|Amir reprend la voiture.",
            "narrateur|Il fait une petite route.",
            "narrateur|La voiture roule tout doux.",
            "enfant-m|Vroum.",
            "papa|Bien roulé.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Maman entre.",
            "narrateur|Elle pose une serviette.",
            "maman|Tes mains sont avec les jouets ?",
            "enfant-m|Oui.",
            "maman|Bravo.",
            "narrateur|Amir pousse la voiture rouge.",
            "narrateur|Puis la bleue.",
            "narrateur|Le tapis fait un bruit doux.",
            "papa|Tu joues encore ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils font un garage avec un livre.",
            "narrateur|Le livre est épais.",
            "papa|Tu ranges une voiture ?",
            "enfant-m|Dans le garage.",
            "papa|Bravo.",
            "narrateur|La lumière reste allumée.",
            "narrateur|Le rideau ne bouge plus.",
            "narrateur|La voiture rouge brille.",
            "enfant-m|J'ai appelé un adulte.",
            "papa|Oui.",
            "papa|C'est bien.",
            "narrateur|Amir est calme.",
            "narrateur|Les mains tiennent les jouets.",
            "narrateur|La serviette sent encore le chaud.",
            "narrateur|Le canapé est tout calme.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Amir veut la lumière.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir a appelé un adulte.",
            "narrateur|Les mains avec les jouets.",
            "papa|Tu as appelé un adulte ?",
            "enfant-m|Oui.",
            "enfant-m|Papa.",
            "maman|Bravo, Amir.",
            "maman|Tu as fait du bon travail.",
            "papa|Les prises sont pour les adultes.",
            "narrateur|La voiture rouge reste dans la main.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Amir pousse la voiture.",
            "narrateur|La lumière reste allumée.",
            "papa|Tu ranges la voiture ?",
            "enfant-m|Un peu.",
            "narrateur|Il pose la voiture près du tapis.",
            "narrateur|La bleue aussi.",
            "papa|Tu as fini ?",
            "enfant-m|Oui.",
            "papa|Bravo.",
            "maman|La pièce est claire.",
            "maman|Tu as appelé papa ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le rideau est calme.",
            "narrateur|Le linge est plié.",
            "narrateur|Le livre du garage reste ouvert.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai appelé un adulte.",
            "enfant-m|Les mains avec les jouets.",
            "papa|Bravo.",
            "maman|C'est du bon travail.",
            "narrateur|La petite voiture se repose.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "voitures",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "voitures",
        "CHK_T0000_P0000_END_F0001": "",
    },
)


# ---------------------------------------------------------------------------
# ATOM-SEC.MAI.001-03 N2 Aniss, chambre, train, lampe
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.MAI.001-03",
    "Un rail de bois fait clic. Le ciel à la fenêtre est orange. Aniss veut la lampe. Il va appeler un adulte. Les mains avec les jouets.",
    "Le wagon rouge et la lampe",
    "Aniss, maman, papa",
    "chambre, train en bois, fenêtre orange, linge",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un rail de bois fait un petit clic.",
            "narrateur|Le clic est sec, tout net.",
            "narrateur|Un wagon rouge attend sur le tapis.",
            "narrateur|La fenêtre est orange, tout bas.",
            "narrateur|Le jour s'en va, tout doux.",
            "narrateur|Le linge sent le savon, près de la porte.",
            "narrateur|Maman plie une petite chemise.",
            "narrateur|Aniss vit ici, avec papa et maman.",
            "enfant-m|Maman, le rail fait clic !",
            "maman|Oui.",
            "maman|C'est le bois.",
            "maman|Tu vois le wagon rouge ?",
            "enfant-m|Oui.",
            "enfant-m|Il attend.",
            "narrateur|En ce moment, Aniss pose un rail.",
            "narrateur|Puis un autre.",
            "narrateur|Le chemin est encore court.",
            "narrateur|La pièce devient un peu sombre.",
            "enfant-m|Maman, la lumière.",
            "narrateur|Aniss regarde ses mains.",
            "narrateur|Les mains avec les jouets.",
            "narrateur|Aniss appelle maman.",
            "narrateur|On va appeler un adulte.",
            "maman|J'arrive, Aniss.",
            "narrateur|Maman vient.",
            "narrateur|Maman allume la lampe.",
            "narrateur|La pièce devient claire.",
            "narrateur|Le wagon rouge brille.",
            "papa|Tu as appelé un adulte ?",
            "enfant-m|Oui, papa.",
            "papa|Bravo, Aniss.",
            "papa|On appelle papa ou maman pour la lumière.",
            "maman|Les prises sont pour les adultes.",
            "maman|Les mains avec les jouets.",
            "narrateur|Aniss reprend le wagon rouge.",
            "narrateur|Il le pose sur le rail.",
            "narrateur|Le wagon glisse.",
            "narrateur|Il fait un petit bruit de bois.",
            "enfant-m|Il avance !",
            "maman|Oui.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Parce qu'il a appelé, la lumière est là.",
            "narrateur|Les mains tiennent les jouets.",
            "papa|Tu fais un plus long chemin ?",
            "enfant-m|Oui.",
            "narrateur|Papa s'assoit près du tapis.",
            "narrateur|Il tend un rail.",
            "maman|Tes mains sont avec les jouets ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "narrateur|La fenêtre n'est plus orange.",
            "narrateur|Elle est plus sombre, dehors.",
            "narrateur|La lampe fait un rond chaud.",
            "enfant-m|J'ai appelé un adulte.",
            "papa|Oui.",
            "papa|C'est bien.",
            "narrateur|Aniss est calme.",
            "narrateur|Le train a un petit chemin.",
            "narrateur|Le linge reste près de la porte.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss veut la lumière.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Aniss a appelé un adulte.",
            "narrateur|Les mains avec les jouets.",
            "maman|Tu as appelé un adulte ?",
            "enfant-m|Oui.",
            "enfant-m|Maman.",
            "papa|Bravo, Aniss.",
            "papa|Tu as fait du bon travail.",
            "maman|Les prises sont pour les adultes.",
            "narrateur|Le wagon rouge reste sur le rail.",
            "narrateur|La lampe reste allumée.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Aniss pose un dernier wagon.",
            "narrateur|Le chemin est fini.",
            "maman|Tu ranges un rail, maintenant ?",
            "enfant-m|Un peu.",
            "narrateur|Il pose un rail dans la boîte.",
            "maman|Tu as fini de ranger ce rail ?",
            "enfant-m|Oui.",
            "maman|Bravo.",
            "papa|La lampe reste allumée.",
            "narrateur|La chemise est pliée.",
            "narrateur|Ça sent encore le savon.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai appelé un adulte.",
            "enfant-m|Les mains avec les jouets.",
            "maman|Bravo.",
            "papa|C'est du bon travail.",
            "narrateur|Le wagon rouge se repose sur le tapis.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "train_bois",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
)


# ---------------------------------------------------------------------------
# ATOM-SEC.MAI.001-04 N2 Nino, salle de jeux, voitures bois
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.MAI.001-04",
    "La poussière danse dans un rayon. Les voitures de bois dorment. La pièce est un peu sombre. Nino va appeler un adulte. Les mains avec les jouets.",
    "Les voitures dans le rayon",
    "Nino, papa, maman",
    "salle de jeux, voitures en bois, pile de livres",
    {
        "CHK_T0000_P0000": [
            "narrateur|La poussière danse dans un rayon.",
            "narrateur|Le rayon est mince, tout pâle.",
            "narrateur|Des voitures en bois dorment par terre.",
            "narrateur|Le bois est lisse, un peu froid.",
            "narrateur|Une pile de livres attend près de la porte.",
            "narrateur|Papa range un livre, tout doux.",
            "narrateur|La pièce est un peu sombre.",
            "narrateur|Nino vit ici, avec papa et maman.",
            "enfant-m|Papa, la poussière danse !",
            "papa|Oui.",
            "papa|C'est le soleil.",
            "papa|Tu vois tes voitures ?",
            "enfant-m|Oui.",
            "enfant-m|Elles dorment.",
            "narrateur|En ce moment, Nino prend une voiture rouge.",
            "narrateur|Il la fait rouler tout doux.",
            "narrateur|Le bois fait un petit bruit.",
            "narrateur|Le rayon pâle ne suffit plus.",
            "enfant-m|Papa, la lumière.",
            "narrateur|Nino regarde ses mains.",
            "narrateur|Les mains avec les jouets.",
            "narrateur|Nino appelle papa.",
            "narrateur|On va appeler un adulte.",
            "papa|J'arrive, Nino.",
            "narrateur|Papa vient.",
            "narrateur|Papa allume.",
            "narrateur|La pièce devient claire.",
            "narrateur|Les voitures de bois brillent.",
            "maman|Tu as appelé un adulte ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo, Nino.",
            "maman|On appelle papa ou maman pour la lumière.",
            "papa|Les prises sont pour les adultes.",
            "papa|Les mains avec les jouets.",
            "narrateur|Nino reprend la voiture rouge.",
            "narrateur|Il fait un petit garage.",
            "narrateur|Deux livres forment les murs.",
            "enfant-m|Le garage !",
            "papa|Oui.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Parce qu'il a appelé, la lumière est là.",
            "narrateur|Les mains tiennent les jouets.",
            "papa|Tu ranges une voiture dans le garage ?",
            "enfant-m|Oui.",
            "narrateur|Papa s'assoit près de lui.",
            "narrateur|Le plancher est un peu froid.",
            "maman|Tes mains sont avec les jouets ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "narrateur|La poussière ne se voit plus.",
            "narrateur|La pièce est claire, tout simple.",
            "enfant-m|J'ai appelé un adulte.",
            "papa|Oui.",
            "papa|C'est bien.",
            "narrateur|Nino est calme.",
            "narrateur|La voiture rouge entre dans le garage.",
            "narrateur|Elle fait un petit toc.",
            "narrateur|Les autres voitures attendent leur tour.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nino veut la lumière.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino a appelé un adulte.",
            "narrateur|Les mains avec les jouets.",
            "papa|Tu as appelé un adulte ?",
            "enfant-m|Oui.",
            "enfant-m|Papa.",
            "maman|Bravo, Nino.",
            "maman|Tu as fait du bon travail.",
            "papa|Les prises sont pour les adultes.",
            "narrateur|La voiture rouge reste dans le garage.",
            "narrateur|La lumière reste allumée.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nino pose une dernière voiture.",
            "narrateur|Le garage est plein.",
            "papa|Tu as fini ton garage ?",
            "enfant-m|Oui, papa.",
            "papa|Bravo.",
            "maman|La lumière reste allumée.",
            "narrateur|Papa pose le dernier livre sur la pile.",
            "maman|Tu as fini de ranger les livres ?",
            "papa|Oui.",
            "narrateur|Le plancher n'a plus de poussière visible.",
            "narrateur|Les voitures de bois se reposent.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai appelé un adulte.",
            "enfant-m|Les mains avec les jouets.",
            "papa|Bravo.",
            "maman|C'est du bon travail.",
            "narrateur|Le rayon de soleil s'en va, tout pâle.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "voitures_bois",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
)
