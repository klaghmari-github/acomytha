#!/usr/bin/env python3
"""F-NAR-008 — merged.json ATOM-AUT.AFF.003-02 à 09."""
from __future__ import annotations

import json
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
    "tu as fait du bon travail",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom ", "léa", "lea ", "lina", "iris",
    "aïcha", "aicha", "clément", "clement", "léonie", "leonie",
    "clarisse", "éléonore", "eleonore", "dominique", "zoé", "zoe",
    "adam", "ariane", "benoît", "benoit",
)
NEED = ("ses affaires", "avant de partir")


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
    nc["text_ssml"] = text
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    return nc


def check(sid: str, age: str, chunks: list[dict]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if name in low:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie." not in low:
        raise SystemExit(f"{sid}: manque fin")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in NEED:
        if m.lower() not in all_text:
            raise SystemExit(f"{sid}: message manquant: {m}")
    if not any(x in all_text for x in ("reprendre", "reprend", "repris")):
        raise SystemExit(f"{sid}: message manquant: reprendre")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in ("joue au salon", "est dans l'entrée", "c'est le matin"):
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
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
    print(f"OK {sid} {nwords} mots  1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}")


def write_story(sid: str, fil: str, title: str, chars: str, setting: str,
                scripts: dict, sons: dict, q: dict | None = None) -> None:
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
    if q:
        qc = by["CHK_T0000_P0000_Q0001"]
        for k, v in q.items():
            qc[k] = v
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


Q = lambda name, elle=False: {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": (
        f"Elle reprend ses affaires. Que fait {name} ?"
        if elle
        else f"Il reprend ses affaires. Que fait {name} ?"
    ),
}


# ---------------------------------------------------------------------------
# 02 N2 Aniss, maman — peaux d'orange, maison du lapin
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-02",
    "Aniss veut une maison avec une porte pour son lapin. Au parc, le soleil baisse. Il reprend pelle, casquette et lapin pour finir la porte à la maison.",
    "La maison du lapin",
    "Aniss, maman",
    "cuisine puis parc, fin d'après-midi",
    {
        "CHK_T0000_P0000": [
            "narrateur|Sur la table, les peaux d'orange brillent.",
            "narrateur|Elles sentent encore le goûter.",
            "narrateur|Un peu de jus a collé au bois.",
            "maman|Tes doigts sont collants, Aniss.",
            "enfant-m|Ça sent l'orange.",
            "narrateur|Maman passe un linge tiède.",
            "narrateur|Le linge est doux, un peu rêche.",
            "maman|On va au parc ?",
            "enfant-m|Oui.",
            "enfant-m|Avec le lapin.",
            "narrateur|Le doudou lapin attend près de la porte.",
            "narrateur|Sa grande oreille plie un peu.",
            "narrateur|Ils ferment la porte.",
            "narrateur|La rue sent encore l'orange, un peu.",
            "narrateur|En ce moment, Aniss est au parc.",
            "narrateur|Le soleil baisse derrière les arbres.",
            "narrateur|Le banc est un peu froid.",
            "narrateur|Maman s'assoit.",
            "narrateur|Aniss a une pelle rouge.",
            "narrateur|Il a une casquette verte.",
            "narrateur|Le lapin est dans l'herbe.",
            "enfant-m|Je lui fais une maison.",
            "maman|Une maison pour le lapin ?",
            "enfant-m|Oui.",
            "enfant-m|Avec une porte.",
            "narrateur|Aniss verse le sable.",
            "narrateur|Ça fait chh.",
            "narrateur|La pelle tape le bac.",
            "narrateur|Toc, toc.",
            "narrateur|Les murs du château montent.",
            "narrateur|Le lapin regarde, dans l'herbe.",
            "narrateur|L'herbe chatouille un peu.",
            "maman|Tu as entendu l'oiseau ?",
            "enfant-m|Oui.",
            "enfant-m|Il est parti.",
            "narrateur|Le ciel devient orange.",
            "narrateur|Comme les peaux, sur la table.",
            "maman|Le soleil baisse, Aniss.",
            "maman|On rentre.",
            "enfant-m|La porte n'est pas finie.",
            "maman|Le château reste ici.",
            "maman|La porte, on la fera à la maison.",
            "enfant-m|Avec la pelle ?",
            "maman|Avec la pelle.",
            "maman|Et le lapin.",
            "maman|On reprend ses affaires, avant de partir.",
            "narrateur|Aniss s'arrête.",
            "narrateur|Il regarde ses mains.",
            "narrateur|Elles sont vides.",
            "narrateur|La pelle est encore dans le sable.",
            "narrateur|Il la prend.",
            "narrateur|Un peu de sable tombe.",
            "enfant-m|J'ai la pelle.",
            "maman|Bien.",
            "maman|Elle servira pour la porte.",
            "narrateur|La casquette est sur le banc.",
            "narrateur|Le lapin est encore dans l'herbe.",
            "narrateur|Aniss cherche des yeux.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Aniss ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Aniss cherche la casquette.",
            "narrateur|Le banc est froid sous ses doigts.",
            "narrateur|La casquette est sous la main de maman.",
            "maman|Oh.",
            "maman|Je la cachais.",
            "enfant-m|Ma casquette !",
            "narrateur|Il la prend.",
            "narrateur|Il va dans l'herbe.",
            "narrateur|L'herbe chatouille.",
            "narrateur|Le lapin a une oreille pliée.",
            "enfant-m|Le voilà.",
            "narrateur|Aniss le prend contre lui.",
            "maman|Tu as repris tes affaires.",
            "enfant-m|Avant de partir.",
            "maman|Oui.",
            "maman|On peut aller faire la porte.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|La pelle tape un peu sa jambe.",
            "maman|Tu tiens bien tout ?",
            "enfant-m|Oui, maman.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils arrivent à la porte.",
            "narrateur|Les peaux d'orange sont encore sur la table.",
            "enfant-m|Elles ont attendu.",
            "maman|Oui.",
            "maman|Comme le lapin.",
            "maman|Tu poses la pelle près des chaussures ?",
            "narrateur|Aniss pose la pelle.",
            "narrateur|Il pose la casquette.",
            "narrateur|Le lapin reste dans son bras.",
            "narrateur|Maman sort une boîte.",
            "narrateur|Une petite boîte à chaussures.",
            "maman|Voici la maison.",
            "enfant-m|Et la porte ?",
            "maman|On plie un bout.",
            "maman|Ça fait une porte.",
            "narrateur|Aniss plie le carton.",
            "narrateur|Ça fait un petit clap.",
            "narrateur|Il glisse le lapin dedans.",
            "enfant-m|Il rentre.",
            "maman|Sa maison est prête.",
            "narrateur|Aniss souffle un peu, tout doux.",
            "enfant-m|Il dort.",
            "maman|Bravo.",
            "maman|Tu as trouvé le lapin.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Le lapin a sa maison.",
            "maman|Et toi, tu as repris tes affaires.",
            "narrateur|La pelle repose près des chaussures.",
            "narrateur|L'orange sent encore un peu.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Aniss"),
)


# ---------------------------------------------------------------------------
# 03 N3 Victorina, papa — bateau de papier, capitaine, pique-nique
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-03",
    "Victorina veut que son ours soit capitaine du seau-bateau, puis l'inviter au pique-nique. À chaque départ, elle reprend ce qu'il faut pour continuer.",
    "Le capitaine dans l'herbe",
    "Victorina, papa",
    "maison, parc, puis pique-nique au jardin",
    {
        "CHK_T0000_P0000": [
            "narrateur|Sur le radiateur, un bateau de papier sèche.",
            "narrateur|Il sent encore la colle et la poussière.",
            "narrateur|La voile est un peu froissée.",
            "papa|C'est le bateau d'hier, Victorina.",
            "enfant-f|Il est tout chaud.",
            "papa|Le radiateur l'a gardé.",
            "narrateur|Une goutte glisse encore sur la vitre.",
            "narrateur|Dehors, le ciel se déchire.",
            "papa|La pluie s'en va.",
            "papa|On met les chaussures ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Avec l'ours.",
            "narrateur|L'ours attend sur la chaise.",
            "narrateur|Papa noue une chaussure.",
            "narrateur|Ils ferment la porte.",
            "narrateur|En ce moment, Victorina est au parc.",
            "narrateur|Le soleil revient sur le bac à sable.",
            "narrateur|Papa s'assoit sur le banc.",
            "narrateur|Victorina a un seau jaune.",
            "narrateur|Elle a un manteau bleu.",
            "narrateur|L'ours est dans l'herbe.",
            "enfant-f|Le seau, c'est un bateau.",
            "papa|Et l'ours ?",
            "enfant-f|Le capitaine.",
            "papa|Je te vois.",
            "narrateur|Victorina verse le sable.",
            "narrateur|Ça fait chh.",
            "narrateur|Le seau est lourd.",
            "narrateur|Elle le pose près du bac.",
            "narrateur|L'ours attend dans l'herbe mouillée.",
            "papa|Le soleil baisse.",
            "papa|On rentre.",
            "enfant-f|Le bateau reste ?",
            "papa|Le bateau peut venir.",
            "papa|C'est ton seau.",
            "papa|On reprend ses affaires, avant de partir.",
            "narrateur|Victorina prend le seau jaune.",
            "narrateur|Il est lourd de sable.",
            "papa|On le vide un peu.",
            "narrateur|Le sable retombe.",
            "narrateur|Chh.",
            "enfant-f|Il est plus léger.",
            "narrateur|Le manteau est sur le banc.",
            "narrateur|Elle le prend.",
            "narrateur|Il est un peu froid.",
            "enfant-f|Et le capitaine ?",
            "papa|Il est dans l'herbe.",
            "narrateur|Victorina cherche.",
            "narrateur|Une feuille couvre une oreille de l'ours.",
            "enfant-f|Il dormait.",
            "narrateur|Elle le prend contre elle.",
            "papa|Merci.",
            "papa|On a tout.",
            "narrateur|Ils rentrent.",
            "narrateur|Plus tard, le jardin sent l'herbe coupée.",
            "narrateur|Papa pose une nappe sur la table basse.",
            "papa|C'est le pique-nique du capitaine.",
            "enfant-f|Il a faim.",
            "narrateur|Victorina a une gourde.",
            "narrateur|Elle a une casquette.",
            "narrateur|L'ours est assis sur la nappe.",
            "enfant-f|J'ai soif.",
            "papa|Bois un peu.",
            "narrateur|L'eau fait glouglou.",
            "narrateur|Une miette reste près de l'ours.",
            "papa|On rentre.",
            "papa|La soupe attend.",
            "enfant-f|Le capitaine aussi.",
            "papa|Oui.",
            "papa|Avant de partir, on reprend ses affaires.",
            "narrateur|Victorina regarde la nappe.",
            "narrateur|La gourde a roulé sous la table.",
            "narrateur|La casquette est sur le banc du jardin.",
            "narrateur|L'ours a encore la miette.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Victorina ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorina se penche.",
            "narrateur|Elle prend la gourde sous la table.",
            "enfant-f|Elle s'était cachée.",
            "papa|Oui.",
            "papa|Comme le capitaine, tout à l'heure.",
            "narrateur|Elle prend la casquette sur le banc.",
            "narrateur|L'ours garde la miette dans sa patte.",
            "enfant-f|Je le prends.",
            "narrateur|Elle le prend.",
            "papa|Tu as repris tes affaires.",
            "enfant-f|Avant de partir.",
            "enfant-f|Les deux fois.",
            "papa|Les deux fois.",
            "papa|Bravo, Victorina.",
            "narrateur|Papa plie la nappe.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|L'ours est contre elle.",
            "papa|Tu tiens tout ?",
            "enfant-f|Oui, papa.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils ouvrent la porte.",
            "narrateur|Le bateau de papier est encore chaud.",
            "enfant-f|Il a attendu.",
            "papa|Oui.",
            "papa|Pose le seau à côté.",
            "narrateur|Victorina pose le seau jaune.",
            "narrateur|Les deux bateaux se touchent.",
            "enfant-f|Le petit et le grand.",
            "papa|Tu poses la casquette sur la chaise ?",
            "narrateur|Elle pose la casquette.",
            "narrateur|Elle pose la gourde près de l'évier.",
            "narrateur|L'ours garde la miette.",
            "papa|Le capitaine a son goûter.",
            "enfant-f|Il peut naviguer demain.",
            "papa|Demain, s'il fait beau.",
            "narrateur|Victorina pose l'ours contre le bateau de papier.",
            "narrateur|La voile froissée touche une oreille.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|J'ai repris mes affaires.",
            "papa|Avant de partir.",
            "papa|Au parc, puis au jardin.",
            "narrateur|Les deux bateaux restent côte à côte.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Victorina", elle=True),
)


# ---------------------------------------------------------------------------
# 04 N2 Mila, papa — chaussettes jaunes, route du doudou
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-04",
    "Après la pluie, Mila veut une route de sable pour son doudou gris. Le doudou reste au bout. Elle reprend seau, manteau et doudou pour finir la route avec les chaussettes jaunes.",
    "La route des chaussettes jaunes",
    "Mila, papa",
    "maison après la pluie, puis square",
    {
        "CHK_T0000_P0000": [
            "narrateur|Près du radiateur, deux chaussettes jaunes sèchent.",
            "narrateur|Elles sentent encore la lessive.",
            "narrateur|Papa range les bottes mouillées.",
            "narrateur|Une goutte tombe de la semelle.",
            "papa|Tes chaussettes sont chaudes, Mila.",
            "enfant-f|Elles sont douces.",
            "papa|On met les chaussettes sèches ?",
            "narrateur|Mila enfile les chaussettes jaunes.",
            "narrateur|Le radiateur fait un petit clic.",
            "papa|On va au square ?",
            "enfant-f|Oui.",
            "enfant-f|Pour la route.",
            "papa|Quelle route ?",
            "enfant-f|Pour le doudou.",
            "narrateur|Ils ferment la porte.",
            "narrateur|La rue sent la pluie.",
            "narrateur|En ce moment, Mila est au square.",
            "narrateur|Le sable est frais, encore un peu humide.",
            "narrateur|Papa s'assoit près du bac.",
            "narrateur|Mila a un seau jaune.",
            "narrateur|Elle a un manteau bleu.",
            "narrateur|Le doudou gris est au bout du bac.",
            "narrateur|Le manteau est posé sur le banc.",
            "enfant-f|Je verse le sable, papa.",
            "papa|Je t'écoute.",
            "narrateur|Mila verse le sable.",
            "narrateur|Ça fait chh.",
            "narrateur|Le seau est froid contre ses mains.",
            "narrateur|Un grain reste collé à son poignet.",
            "papa|Il y a du sable sur toi.",
            "enfant-f|Sur le poignet.",
            "narrateur|Mila fait une petite route.",
            "narrateur|Le sable est frais sous les doigts.",
            "narrateur|Ça sent la terre mouillée.",
            "papa|Ça sent la pluie, encore.",
            "enfant-f|Oui, la pluie.",
            "narrateur|Le doudou attend au bout de la route.",
            "enfant-f|Il va marcher.",
            "papa|C'est l'heure.",
            "enfant-f|La route n'est pas finie.",
            "papa|Le château de sable reste ici.",
            "papa|La route, on la fera à la maison.",
            "papa|On reprend ses affaires, avant de partir.",
            "narrateur|Mila s'arrête.",
            "narrateur|Le seau est encore dans le sable.",
            "narrateur|Elle le prend.",
            "enfant-f|Le seau est là.",
            "papa|Bien.",
            "papa|Il servira pour la route.",
            "narrateur|Le manteau est sur le banc.",
            "narrateur|Le doudou est encore au bout.",
            "narrateur|Un grain de sable est sur son nez.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Mila ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila cherche le manteau.",
            "narrateur|Le tissu est un peu frais.",
            "narrateur|Elle le prend.",
            "enfant-f|Le manteau aussi.",
            "papa|Et le doudou ?",
            "narrateur|Mila va au bout de la route.",
            "narrateur|Elle essuie le grain sur le nez.",
            "enfant-f|Il est gris.",
            "enfant-f|Il est là.",
            "narrateur|Elle le prend.",
            "papa|Tu as repris tes affaires.",
            "enfant-f|Avant de partir.",
            "papa|Oui.",
            "papa|On peut continuer la route.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|Papa tient le sac.",
            "narrateur|Mila tient le doudou.",
            "papa|Tu es prête ?",
            "enfant-f|Je suis prête.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils arrivent à la porte.",
            "narrateur|Les chaussettes jaunes ne sont plus au radiateur.",
            "papa|Elles sont à tes pieds.",
            "papa|Tu poses le seau près de la porte ?",
            "narrateur|Mila pose le seau.",
            "narrateur|Elle pose le manteau sur la chaise.",
            "narrateur|Le doudou reste contre elle.",
            "papa|On fait la route ici.",
            "narrateur|Mila retire une chaussette jaune.",
            "narrateur|Puis l'autre.",
            "narrateur|Elle les pose en ligne sur le plancher.",
            "enfant-f|C'est la route.",
            "papa|Le doudou peut marcher.",
            "narrateur|Mila fait avancer le doudou.",
            "narrateur|Pas à pas, sur le jaune.",
            "enfant-f|Il arrive.",
            "papa|Bravo.",
            "papa|Il a fini sa route.",
            "narrateur|Le radiateur fait encore clic.",
            "narrateur|La maison est tiède.",
            "papa|Tu as les pieds au chaud, maintenant ?",
            "enfant-f|Oui, papa.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Le doudou a fini sa route.",
            "papa|Et toi, tu as repris tes affaires.",
            "narrateur|Les chaussettes jaunes restent en ligne.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Mila", elle=True),
)


# ---------------------------------------------------------------------------
# 05 N2 Nino, maman — feuille à la vitre, seau vert
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-05",
    "Nino veut garder une feuille qui danse dans son seau vert. Elle s'envole. Il reprend seau, manteau et ours pour lui faire une place près de la feuille de la fenêtre.",
    "La feuille qui danse",
    "Nino, maman",
    "fenêtre de la maison, puis aire de jeux",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une feuille collée à la vitre tapote.",
            "narrateur|Toc, toc.",
            "narrateur|Le soleil de l'après-midi la rend orange.",
            "narrateur|Maman ouvre un peu la fenêtre.",
            "narrateur|Un souffle d'air entre.",
            "maman|Tu as vu la feuille, Nino ?",
            "enfant-m|Elle est orange.",
            "maman|Elle veut rentrer.",
            "narrateur|Maman la pose sur le rebord.",
            "maman|On va à l'aire de jeux ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Je veux une feuille, moi aussi.",
            "maman|On regardera.",
            "narrateur|Ils prennent le sac.",
            "narrateur|La rue est calme.",
            "narrateur|En ce moment, Nino est à l'aire de jeux.",
            "narrateur|Le sable est un peu chaud.",
            "narrateur|Maman s'assoit au bord.",
            "narrateur|Nino a un seau vert.",
            "narrateur|Il a un manteau bleu posé au bord.",
            "narrateur|Il a son doudou ours.",
            "narrateur|Le petit toboggan est tiède.",
            "enfant-m|Il est chaud, maman.",
            "maman|Le soleil l'a touché.",
            "narrateur|Nino verse le sable.",
            "narrateur|Ça fait chh.",
            "narrateur|Une feuille passe.",
            "enfant-m|Une feuille, maman !",
            "maman|Comme celle de la fenêtre.",
            "maman|Elle danse.",
            "narrateur|La feuille se pose dans le seau.",
            "narrateur|Nino la sort tout doux.",
            "enfant-m|Elle habite ici.",
            "narrateur|Le vent reprend la feuille.",
            "narrateur|Elle s'envole au-dessus du bac.",
            "enfant-m|Elle est partie.",
            "maman|Elle vole encore.",
            "maman|C'est l'heure.",
            "enfant-m|La feuille aussi ?",
            "maman|La feuille peut voler.",
            "maman|Tes affaires viennent à la maison.",
            "maman|On reprend ses affaires, avant de partir.",
            "narrateur|Nino cherche le seau.",
            "narrateur|Le seau est encore vert, un peu sableux.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai le seau.",
            "maman|Bien.",
            "maman|On lui fera une place, à la maison.",
            "narrateur|Le manteau est au bord.",
            "narrateur|Une manche est à l'envers.",
            "narrateur|L'ours est près du toboggan.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Nino ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino cherche le manteau.",
            "narrateur|Il tourne la manche tout doux.",
            "enfant-m|Le manteau est bleu.",
            "narrateur|Il le prend.",
            "maman|Et l'ours ?",
            "narrateur|Nino va près du toboggan.",
            "narrateur|L'ours est tiède, comme le plastique.",
            "enfant-m|L'ours est là.",
            "narrateur|Il le prend.",
            "maman|Tu as repris tes affaires.",
            "enfant-m|Avant de partir.",
            "maman|Oui.",
            "maman|La feuille de la fenêtre t'attend.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|Le seau cogne un peu.",
            "narrateur|Le doudou est contre lui.",
            "maman|Je marche à côté.",
            "enfant-m|Moi aussi.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nino tient le seau.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|La feuille du rebord est encore là.",
            "enfant-m|Elle a attendu.",
            "maman|Oui.",
            "maman|Tu poses le seau près de la fenêtre ?",
            "narrateur|Nino pose le seau sous le rebord.",
            "narrateur|Il pose le manteau.",
            "narrateur|L'ours reste dans son bras.",
            "maman|On met la feuille dans le seau ?",
            "enfant-m|Oui.",
            "enfant-m|Elle visite.",
            "narrateur|Maman glisse la feuille orange.",
            "narrateur|Elle tapote le fond.",
            "narrateur|Toc.",
            "enfant-m|Elle danse plus.",
            "maman|Ici, elle se repose.",
            "maman|Bravo.",
            "maman|Tu as repris tes affaires.",
            "narrateur|La vitre est calme.",
            "narrateur|Plus de toc, toc.",
            "narrateur|L'ours regarde le seau.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|La feuille a sa place.",
            "maman|Et toi, tu as repris tes affaires.",
            "narrateur|Le seau vert reste sous la fenêtre.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Nino"),
)


# ---------------------------------------------------------------------------
# 06 N1 Sarah, maman — gouttière, seau vert, eau pour doudou
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-06",
    "Sarah veut remplir le seau vert avec les gouttes. Pour donner de l'eau au doudou à la maison, elle reprend seau, manteau et doudou.",
    "Les gouttes du seau vert",
    "Sarah, maman",
    "rebord de fenêtre puis jardin après la pluie",
    {
        "CHK_T0000_P0000": [
            "narrateur|La gouttière fait plic, plic, plic.",
            "narrateur|Une goutte tombe.",
            "narrateur|Elle tombe dans la cuvette.",
            "narrateur|La cuvette est grise.",
            "maman|Tu entends, Sarah ?",
            "enfant-f|Plic, plic.",
            "maman|Oui.",
            "maman|Plic, plic.",
            "narrateur|Maman essuie le rebord.",
            "narrateur|Le bois est froid.",
            "narrateur|Les bottes de Sarah attendent.",
            "narrateur|Elles sont rouges.",
            "maman|On met les bottes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah enfile les bottes.",
            "maman|On va au jardin ?",
            "enfant-f|Oui.",
            "enfant-f|Pour l'eau.",
            "narrateur|La porte s'ouvre.",
            "narrateur|En ce moment, Sarah est au jardin.",
            "narrateur|La terre est fraîche.",
            "narrateur|Les feuilles brillent.",
            "maman|Je m'assois près du bac.",
            "narrateur|Sarah a un seau vert.",
            "narrateur|Elle a un manteau rouge.",
            "narrateur|Elle a son doudou beige.",
            "enfant-f|De l'eau pour lui.",
            "maman|Pour le doudou ?",
            "enfant-f|Oui.",
            "narrateur|Sarah verse l'eau.",
            "narrateur|Ça fait ploc.",
            "enfant-f|Ploc, maman.",
            "maman|Ploc, oui.",
            "maman|Je t'écoute.",
            "narrateur|Sarah verse encore.",
            "narrateur|Ça fait ploc, ploc.",
            "narrateur|Le seau est mouillé.",
            "maman|Tes mains sont froides ?",
            "enfant-f|Un peu.",
            "narrateur|L'eau coule un peu.",
            "narrateur|La terre devient sombre.",
            "narrateur|Le doudou est sur la terre.",
            "maman|C'est l'heure.",
            "maman|On reprend ses affaires, avant de partir.",
            "enfant-f|Le seau ?",
            "maman|Oui.",
            "maman|Tu cherches le seau.",
            "narrateur|Sarah cherche le seau.",
            "narrateur|Elle le prend.",
            "enfant-f|J'ai le seau.",
            "maman|Bien.",
            "maman|L'eau vient à la maison.",
            "narrateur|Le manteau est sur la chaise.",
            "narrateur|Le doudou est sur la terre.",
            "narrateur|Une oreille est un peu mouillée.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Sarah ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah cherche le manteau.",
            "narrateur|Elle le prend.",
            "enfant-f|Le manteau.",
            "maman|Oui.",
            "maman|Tu cherches le doudou.",
            "narrateur|Sarah cherche le doudou.",
            "narrateur|Elle le prend.",
            "enfant-f|Le doudou.",
            "maman|Son oreille est mouillée.",
            "enfant-f|Un peu.",
            "maman|Tu as repris tes affaires.",
            "enfant-f|Avant de partir.",
            "maman|Oui.",
            "narrateur|Ses affaires sont dans ses mains.",
            "narrateur|Elles marchent vers la maison.",
            "narrateur|Les bottes font poum, poum.",
            "maman|Tu tiens tout ?",
            "enfant-f|Oui.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sarah tient le seau.",
            "narrateur|Le doudou est contre elle.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|La gouttière fait encore plic.",
            "maman|Tu poses le seau ?",
            "narrateur|Sarah pose le seau.",
            "narrateur|Elle pose le manteau.",
            "maman|Merci, Sarah.",
            "maman|On donne de l'eau au doudou ?",
            "enfant-f|Oui, maman.",
            "narrateur|Maman prend une soucoupe.",
            "narrateur|Sarah verse une goutte.",
            "narrateur|Ploc.",
            "enfant-f|Il boit.",
            "maman|Bravo.",
            "maman|Tu as repris tes affaires.",
            "narrateur|Les bottes s'arrêtent.",
            "narrateur|La maison est calme.",
            "maman|Tu poses les bottes ?",
            "narrateur|Sarah pose les bottes.",
            "narrateur|Elles sont un peu mouillées.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Le doudou a de l'eau.",
            "maman|Et toi, tu as repris tes affaires.",
            "narrateur|La gouttière fait encore plic.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Sarah", elle=True),
)


# ---------------------------------------------------------------------------
# 07 N3 Amir, maman — soupe, lapin voyageur, parc puis jardin
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-07",
    "Amir veut faire visiter le parc puis le jardin à son lapin, avant la soupe. À chaque départ, il reprend ce qu'il faut pour que le lapin rentre.",
    "Le lapin et la soupe",
    "Amir, maman",
    "cuisine, parc, puis jardin",
    {
        "CHK_T0000_P0000": [
            "narrateur|Dans la cuisine, la casserole sent la carotte.",
            "narrateur|Elle est encore tiède.",
            "narrateur|La cuillère en bois repose sur le torchon.",
            "maman|La soupe attend pour ce soir, Amir.",
            "enfant-m|Ça sent bon.",
            "maman|Oui.",
            "maman|Carotte et poireau.",
            "narrateur|Maman pose le couvercle.",
            "narrateur|Ça fait un petit toc.",
            "maman|On va au parc, maintenant.",
            "enfant-m|Oui.",
            "enfant-m|Le lapin vient.",
            "maman|Il voyage.",
            "narrateur|Ils ferment la porte.",
            "narrateur|La soupe reste à la maison.",
            "narrateur|En ce moment, Amir est au parc.",
            "narrateur|Le vent fraîchit.",
            "narrateur|Maman s'assoit sur le banc.",
            "narrateur|Amir a un seau rouge.",
            "narrateur|Il a un manteau vert.",
            "narrateur|Il a son doudou lapin.",
            "narrateur|Le manteau est sur le banc.",
            "enfant-m|Le seau, c'est sa valise.",
            "maman|Je te vois.",
            "narrateur|Amir verse le sable.",
            "narrateur|Ça fait chh.",
            "narrateur|Le vent soulève un peu de poussière.",
            "narrateur|Le lapin attend dans l'herbe.",
            "narrateur|L'herbe chatouille.",
            "maman|Le vent fraîchit.",
            "maman|On rentre.",
            "enfant-m|Le lapin n'a pas tout vu.",
            "maman|Il verra le jardin, après.",
            "maman|On reprend ses affaires, avant de partir.",
            "narrateur|Amir s'arrête.",
            "narrateur|Il cherche le seau près du bac.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai la valise.",
            "maman|Bien.",
            "narrateur|Il cherche le manteau sur le banc.",
            "narrateur|Il le prend.",
            "enfant-m|Le manteau vert.",
            "maman|Et le lapin ?",
            "narrateur|Il cherche le doudou dans l'herbe.",
            "narrateur|L'herbe chatouille.",
            "narrateur|Il le prend.",
            "enfant-m|Le lapin aussi.",
            "maman|Merci, Amir.",
            "narrateur|Maintenant Amir a tout.",
            "narrateur|Ils rentrent un moment.",
            "narrateur|Plus tard, ils jouent au jardin.",
            "narrateur|L'odeur de soupe est encore là.",
            "narrateur|Elle passe sous la porte.",
            "narrateur|Amir a une gourde.",
            "narrateur|Il a une casquette.",
            "narrateur|Il a encore le doudou.",
            "enfant-m|Je bois.",
            "maman|Doucement.",
            "narrateur|L'eau est fraîche.",
            "narrateur|Une feuille tourne près du pied.",
            "enfant-m|Le jardin, il a vu.",
            "maman|On rentre.",
            "maman|La soupe est prête.",
            "enfant-m|Le lapin aussi.",
            "maman|Avant de partir, on reprend ses affaires.",
            "narrateur|La gourde a roulé près de la feuille.",
            "narrateur|La casquette est sur une chaise.",
            "narrateur|Le lapin est dans l'herbe courte.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Amir ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir se souvient.",
            "narrateur|Il cherche la gourde.",
            "narrateur|Il la prend près de la feuille.",
            "narrateur|Il cherche la casquette.",
            "narrateur|Il la prend.",
            "narrateur|Il cherche le doudou.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai tout.",
            "maman|Tu as repris tes affaires.",
            "enfant-m|Avant de partir.",
            "enfant-m|Au parc, puis au jardin.",
            "maman|Les deux fois.",
            "maman|Bravo, Amir.",
            "narrateur|Amir a tout.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|Le doudou est dans son bras.",
            "maman|Tu tiens le lapin ?",
            "enfant-m|Oui.",
            "enfant-m|Il a voyagé.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Amir marche près de maman.",
            "narrateur|Le doudou est dans son bras.",
            "narrateur|Ils ouvrent la porte.",
            "narrateur|La soupe sent encore plus fort.",
            "maman|Tu poses la gourde près de l'évier ?",
            "narrateur|Amir pose la gourde.",
            "narrateur|Il pose la casquette.",
            "maman|Merci.",
            "maman|Ce soir, on mange la soupe.",
            "enfant-m|Carotte et poireau.",
            "maman|Oui.",
            "narrateur|Amir pose le lapin sur une chaise.",
            "enfant-m|Il a vu le parc.",
            "enfant-m|Il a vu le jardin.",
            "maman|Et maintenant, la soupe.",
            "narrateur|Un peu de vapeur monte.",
            "enfant-m|Il goûte l'odeur.",
            "maman|Tout doux.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Le lapin a voyagé.",
            "maman|Et toi, tu as repris tes affaires.",
            "narrateur|La casserole est encore tiède.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Amir"),
)


# ---------------------------------------------------------------------------
# 08 N2 Nina, maman — couverture à carreaux, miette pour l'ours
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-08",
    "Nina veut garder une miette pour l'ours, dans le seau bleu. Le vent soulève la couverture. Avant de rentrer, elle reprend seau, manteau et ours.",
    "La miette de la couverture",
    "Nina, maman",
    "cuisine puis square, pique-nique",
    {
        "CHK_T0000_P0000": [
            "narrateur|Sur la chaise, une couverture à carreaux attend.",
            "narrateur|Elle a encore des miettes de pain.",
            "narrateur|Maman la secoue au-dessus de l'évier.",
            "narrateur|Les miettes tombent.",
            "maman|On emporte la couverture, Nina ?",
            "enfant-f|Oui.",
            "enfant-f|Pour s'asseoir.",
            "maman|Pour le pique-nique.",
            "narrateur|Maman plie la couverture.",
            "narrateur|Le tissu est doux, un peu rêche.",
            "maman|On va au square ?",
            "enfant-f|Oui.",
            "enfant-f|Avec l'ours.",
            "narrateur|Ils marchent.",
            "narrateur|Le sac sent le pain.",
            "narrateur|En ce moment, Nina est au square.",
            "narrateur|La couverture est déjà posée dans l'herbe.",
            "maman|Je m'assois dessus.",
            "narrateur|Nina a un seau bleu.",
            "narrateur|Elle a un manteau jaune.",
            "narrateur|Elle a son doudou ours.",
            "narrateur|Le vent fraîchit.",
            "enfant-f|J'ai mangé le pain, maman.",
            "maman|Oui.",
            "maman|Il reste une miette.",
            "narrateur|Nina la montre.",
            "enfant-f|C'est pour l'ours.",
            "narrateur|Elle la pose dans le seau bleu.",
            "maman|Tu as encore faim ?",
            "enfant-f|Non.",
            "enfant-f|Je joue.",
            "narrateur|Elle verse le sable dans le seau.",
            "narrateur|Ça fait chh.",
            "narrateur|La miette reste au fond.",
            "narrateur|Le vent soulève un coin de la couverture.",
            "maman|Je le tiens.",
            "enfant-f|Merci, maman.",
            "maman|Le vent fraîchit.",
            "maman|On rentre.",
            "enfant-f|La couverture aussi ?",
            "maman|Oui.",
            "maman|On reprend ses affaires, avant de partir.",
            "narrateur|Nina s'arrête.",
            "narrateur|Elle cherche le seau près du bac.",
            "narrateur|Elle le prend.",
            "enfant-f|Le seau bleu.",
            "enfant-f|La miette est dedans.",
            "maman|Bien.",
            "narrateur|Le manteau est sur la couverture.",
            "narrateur|L'ours est dans l'herbe.",
            "narrateur|L'herbe chatouille.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Nina ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina cherche le manteau.",
            "narrateur|Elle le prend sur la couverture.",
            "enfant-f|Il est jaune.",
            "maman|Et l'ours ?",
            "narrateur|Elle cherche le doudou dans l'herbe.",
            "narrateur|L'herbe chatouille.",
            "narrateur|Elle le prend.",
            "enfant-f|L'ours est là.",
            "maman|Tu as repris tes affaires.",
            "enfant-f|Avant de partir.",
            "maman|Oui.",
            "maman|La miette vient aussi.",
            "narrateur|Maintenant Nina a tout.",
            "narrateur|Maman plie la couverture.",
            "narrateur|Nina marche vers la maison.",
            "narrateur|Le doudou est dans son bras.",
            "maman|Tu tiens le seau ?",
            "enfant-f|Oui, maman.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nina marche près de maman.",
            "narrateur|Le seau tape sa jambe.",
            "narrateur|Ils arrivent à la cuisine.",
            "narrateur|Maman pose la couverture sur la chaise.",
            "maman|Tu poses le seau près de la porte ?",
            "narrateur|Nina pose le seau.",
            "narrateur|Elle pose le manteau.",
            "narrateur|L'ours reste contre elle.",
            "enfant-f|La miette ?",
            "maman|On la met dans une soucoupe.",
            "narrateur|Nina cherche au fond du seau.",
            "narrateur|La miette est un peu sableuse.",
            "maman|Je la prends.",
            "narrateur|Maman la pose dans la soucoupe.",
            "narrateur|Nina assied l'ours devant.",
            "enfant-f|C'est son pain.",
            "maman|Bravo.",
            "maman|Tu as repris tes affaires.",
            "narrateur|Une autre miette reste sur la chaise.",
            "maman|Je la prends.",
            "enfant-f|Plus de miettes.",
            "maman|Plus de miettes.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|L'ours a sa miette.",
            "maman|Et toi, tu as repris tes affaires.",
            "narrateur|La couverture à carreaux repose.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Nina", elle=True),
)


# ---------------------------------------------------------------------------
# 09 N2 Chouchou, maman — grains du tapis, montagne, jardin
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-09",
    "Chouchou veut une montagne de sable, puis un chemin au jardin, sans laisser le square dans l'entrée. Il reprend ses affaires aux deux départs.",
    "Les grains du tapis bleu",
    "Chouchou, maman",
    "entrée, square, puis jardin",
    {
        "CHK_T0000_P0000": [
            "narrateur|Dans l'entrée, le tapis bleu garde des grains.",
            "narrateur|Encore un grain.",
            "narrateur|Maman les chasse d'un coup de main doux.",
            "narrateur|La porte claque un peu.",
            "maman|Le square est venu jusqu'ici, Chouchou.",
            "enfant-m|C'est du sable.",
            "maman|Oui.",
            "maman|Du square.",
            "narrateur|Le tapis redevient lisse.",
            "maman|On retourne au square ?",
            "enfant-m|Oui.",
            "enfant-m|Pour la montagne.",
            "narrateur|Ils ferment la porte.",
            "narrateur|En ce moment, Chouchou est au square.",
            "narrateur|Le vent fraîchit.",
            "narrateur|Maman s'assoit sur le banc.",
            "narrateur|Chouchou a un seau bleu.",
            "narrateur|Il a un manteau gris.",
            "narrateur|Il a son doudou ours.",
            "narrateur|Le manteau est sur le banc.",
            "enfant-m|Je remplis le seau.",
            "maman|Je te vois.",
            "narrateur|Le sable glisse.",
            "narrateur|Ça fait chh.",
            "narrateur|Un grain reste sur le seau.",
            "enfant-m|Encore du sable.",
            "maman|Tu fais une montagne ?",
            "enfant-m|Oui.",
            "narrateur|La montagne est petite.",
            "narrateur|Le vent la touche un peu.",
            "maman|On rentre.",
            "maman|On reprend ses affaires, avant de partir.",
            "narrateur|Chouchou cherche le seau près du bac.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai le seau.",
            "maman|On le vide ici.",
            "maman|Le tapis restera propre.",
            "narrateur|Le sable retombe dans le bac.",
            "narrateur|Chh.",
            "enfant-m|La montagne reste au square.",
            "maman|Oui.",
            "narrateur|Il cherche le manteau sur le banc.",
            "narrateur|Il le prend.",
            "enfant-m|Le manteau gris.",
            "maman|Et l'ours ?",
            "narrateur|Il cherche le doudou dans l'herbe.",
            "narrateur|Il le prend.",
            "enfant-m|L'ours aussi.",
            "maman|Merci.",
            "narrateur|Maintenant Chouchou a tout.",
            "narrateur|Rien ne reste sur le banc.",
            "narrateur|Plus tard, au jardin, le vent est plus doux.",
            "narrateur|Chouchou a une gourde.",
            "narrateur|Il a une casquette.",
            "narrateur|Il a encore le doudou.",
            "enfant-m|Je fais un chemin.",
            "maman|Avec des feuilles ?",
            "enfant-m|Oui.",
            "narrateur|Il pose trois feuilles.",
            "enfant-m|Je bois.",
            "maman|Bien.",
            "narrateur|Une abeille passe loin, très loin.",
            "maman|On rentre.",
            "enfant-m|Avant de partir, on reprend ses affaires.",
            "maman|Oui, Chouchou.",
            "maman|Tu te souviens.",
            "narrateur|La gourde est près des feuilles.",
            "narrateur|La casquette est sur l'ours.",
            "narrateur|L'ours a un chapeau.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Chouchou ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Chouchou prend la gourde.",
            "narrateur|Il prend la casquette.",
            "narrateur|L'ours n'a plus de chapeau.",
            "enfant-m|C'était drôle.",
            "maman|Oui.",
            "narrateur|Chouchou prend le doudou.",
            "enfant-m|J'ai tout.",
            "maman|Tu as repris tes affaires.",
            "enfant-m|Avant de partir.",
            "enfant-m|Au square, puis au jardin.",
            "maman|Les deux fois.",
            "maman|Bravo, Chouchou.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|Le doudou est dans son bras.",
            "maman|Cette fois, pas de sable.",
            "enfant-m|Pas de sable.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Chouchou marche près de maman.",
            "narrateur|Le doudou est dans son bras.",
            "narrateur|Ils poussent la porte.",
            "narrateur|Le tapis bleu est lisse.",
            "maman|Tu poses la gourde ?",
            "narrateur|Chouchou pose la gourde.",
            "narrateur|Il pose la casquette.",
            "maman|Merci.",
            "maman|Cette fois, le tapis reste propre.",
            "enfant-m|Pas de sable.",
            "maman|Pas de sable.",
            "narrateur|Chouchou pose l'ours sur le tapis.",
            "enfant-m|Il garde l'entrée.",
            "maman|Oui.",
            "maman|Sans grains.",
            "narrateur|Le tapis est doux sous les pieds.",
            "maman|Tu as repris tes affaires, avant de partir.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Le tapis est propre.",
            "maman|Et toi, tu as repris tes affaires.",
            "narrateur|L'ours reste sur le tapis bleu.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    Q("Chouchou"),
)
