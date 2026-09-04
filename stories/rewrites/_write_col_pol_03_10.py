#!/usr/bin/env python3
"""F-NAR-008 — merged.json ATOM-COL.POL.001-03..10."""
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
    "tu as fait du bon travail",
    "c'est du bon travail",
    "les trois mots",
    "tu as dit les mots",
    "tu te souviens des mots",
    "j'ai dit bonjour",
    "j'ai dit s'il te plaît",
    "j'ai dit merci",
    "chuchotement",
    "une étape après l'autre",
    "adulte a dit",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom", "léa", "lea", "lina", "iris",
    "denis", "hadrien", "sylvain", "sami", "fatou", "idris", "flora",
    "constentin", "luca", "céline", "celine", "lucas",
    "malik", "lucien", "louise", "ferdinand", "fanny", "pascal",
    "david", "félix", "felix", "zoé", "zoe",
)
TROUPE = (
    "amir", "aniss", "sarah", "chouchou", "mila", "nino", "nina",
    "raphaël", "raphael", "victorino", "victorina",
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
        return 1.18, "medium"
    if kind == "passage_question":
        return 1.24, "medium"
    if kind == "passage_fin":
        return 1.2, "medium"
    return 1.22, "medium"


def make_chunk(src: dict, lines: list[str], sons, age: str, qmeta: dict | None) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons else ""
    ls, rl = scales(age, src.get("kind") or "")
    nc["length_scale_piper"] = ls
    nc["rate_label"] = rl
    nc["text_ssml"] = ""
    if qmeta:
        nc.update(qmeta)
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
    if not any(ln.startswith("papa|") for ln in joined.splitlines()):
        raise SystemExit(f"{sid}: pas de papa")
    if not any(ln.startswith("maman|") for ln in joined.splitlines()):
        raise SystemExit(f"{sid}: pas de maman")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in need_msgs:
        if m.lower() not in all_text:
            raise SystemExit(f"{sid}: message manquant: {m}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    bravo_n = low.count("bravo") + low.count("bon travail")
    if bravo_n > 1:
        raise SystemExit(f"{sid}: trop de bravo ({bravo_n})")
    enfant_lines = [ln for ln in joined.splitlines() if ln.startswith("enfant-")]
    if not enfant_lines:
        raise SystemExit(f"{sid}: enfant muet")
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
    p0 = chunks[0]
    p0_low = p0["text"].lower()
    if "l'histoire est finie" in p0_low:
        raise SystemExit(f"{sid}: fin collée dans P0000")
    enfant_p0 = " ".join(
        ln.split("|", 1)[1] for ln in p0["script"].splitlines() if ln.startswith("enfant-")
    ).lower()
    if "s'il te plaît" in enfant_p0 or "s'il te plait" in enfant_p0:
        raise SystemExit(f"{sid}: s'il te plaît déjà dans P0000")
    if re.search(r"\bbonjour\b", enfant_p0):
        raise SystemExit(f"{sid}: bonjour enfant déjà dans P0000")
    fin = chunks[-1]["script"].splitlines()[-1]
    if not fin.endswith("L'histoire est finie."):
        raise SystemExit(f"{sid}: dernière ligne doit être L'histoire est finie.")
    print(f"OK {sid} {nwords} mots")


def write_relecture(sid: str, title: str, bullets: list[str]) -> None:
    body = "\n".join(f"- {b}" for b in bullets)
    text = (
        f"# F-NAR-015 — {sid}\n\n"
        f"Relu : P0000, Q0001, C0001, END, END_F0001, script, retry_prompt, prénom.\n\n"
        f"## Vu et corrigé\n\n"
        f"{body}\n\n"
        f"## Non vérifié\n\n"
        f"- Audio. Durée ≥ 3 min (texte allongé, pas mesuré). Playtest moteur.\n"
    )
    (ROOT / sid / "RELECTURE.md").write_text(text, encoding="utf-8")


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
    relecture: list[str],
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
    out["secondary_lessons"] = "COL.ECO.002"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, age, out["chunks"], need)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_relecture(sid, title, relecture)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-03 N3 Aniss — livre de trains + crayon bleu
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-03",
    "Aniss veut le livre de trains sous la lampe jaune. Il dit bonjour, s'il te plaît, merci. Le crayon bleu dessine la locomotive.",
    "Le train bleu d'Aniss",
    "Aniss, papa, maman",
    "bibliothèque sous la pluie, puis boutique de crayons",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le radiateur cliquette tout bas.",
            "narrateur|Un foulard bleu sèche dessus.",
            "narrateur|Il est lourd d'eau de pluie.",
            "narrateur|Une horloge pousse un tic.",
            "narrateur|Puis un tac, tout au fond.",
            "narrateur|Une lampe pose un rond jaune.",
            "narrateur|Le tapis est épais sous les bottes.",
            "maman|Tu entends l'horloge, Aniss ?",
            "enfant-m|Tic.",
            "enfant-m|Tac.",
            "papa|On est au chaud, ici.",
            "narrateur|Dehors, la pluie tape le zinc.",
            "narrateur|Les parapluies gouttent dans un seau.",
            "narrateur|Ça sent le papier et le bois.",
            "narrateur|Les étagères montent jusqu'au plafond.",
            "narrateur|Les dos des livres sont verts, rouges, bruns.",
            "narrateur|En ce moment, Aniss cherche un livre.",
            "narrateur|Ses doigts glissent sur les dos lisses.",
            "enfant-m|Maman, un train.",
            "enfant-m|Il est rouge.",
            "maman|Celui avec la locomotive.",
            "papa|On s'approche du bureau.",
            "narrateur|La dame tamponne des cartes.",
            "narrateur|Le tampon fait toc, toc.",
            "narrateur|Aniss attend près du bois.",
            "narrateur|Le livre rouge est sur le chariot.",
            "narrateur|Juste derrière elle.",
            "enfant-m|Il est là.",
            "maman|On attend un peu.",
            "papa|Elle a les mains pleines.",
            "narrateur|Le tampon se pose enfin.",
            "narrateur|La dame lève les yeux.",
            "narrateur|Aniss montre le livre rouge.",
            "maman|Tu demandes, Aniss.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss veut le livre.",
            "narrateur|Que dit-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-m|Bonjour.",
            "maman|Bonjour.",
            "enfant-m|Le livre de trains, s'il te plaît.",
            "enfant-m|Celui avec la locomotive.",
            "narrateur|La dame tend le livre rouge.",
            "narrateur|La couverture est lisse, un peu froide.",
            "enfant-m|Merci.",
            "papa|Merci.",
            "narrateur|Aniss ouvre une page.",
            "narrateur|Un train bleu roule sur un pont.",
            "enfant-m|Il est tout bleu, papa.",
            "papa|Oui.",
            "maman|Tu l'as dans les mains.",
            "narrateur|Ils restent sous la lampe jaune.",
            "narrateur|La pluie continue contre la vitre.",
            "narrateur|Plus tard, le seau de zinc est plein.",
            "narrateur|Ils sortent, le livre sous le bras.",
            "narrateur|Les bottes sonnent sur les dalles mouillées.",
            "narrateur|Une petite boutique a des crayons.",
            "narrateur|Un crayon bleu brille dans un pot.",
            "enfant-m|Pour le train.",
            "enfant-m|Bonjour.",
            "enfant-m|Un crayon bleu, s'il te plaît.",
            "narrateur|La dame du pot tend le crayon.",
            "narrateur|Le bois est lisse, un peu sec.",
            "enfant-m|Merci.",
            "maman|On rentre, maintenant.",
            "narrateur|Aniss tient le livre.",
            "narrateur|Il tient le crayon, tout droit.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|À la maison, le foulard est presque sec.",
            "narrateur|Aniss pose le livre sur la table.",
            "narrateur|Il ouvre la page du pont.",
            "maman|Tu veux le crayon ?",
            "enfant-m|Oui, maman.",
            "enfant-m|S'il te plaît.",
            "narrateur|Le crayon bleu glisse sur le papier.",
            "narrateur|Une locomotive apparaît, tout simple.",
            "enfant-m|C'est mon train.",
            "papa|Il a un pont, comme le livre.",
            "enfant-m|Oui.",
            "maman|Il est bleu, hein ?",
            "enfant-m|Tout bleu.",
            "narrateur|La pluie est plus douce, dehors.",
            "papa|Tu tiens le livre des deux mains ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le crayon sent un peu le bois.",
            "narrateur|La page reste ouverte, près de lui.",
            "maman|On le laisse ouvert ?",
            "enfant-m|Oui.",
            "papa|Le pont est encore là.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le crayon repose près du livre.",
            "narrateur|Le train bleu est sur le papier.",
            "maman|Bonne soirée, Aniss.",
            "papa|Il a un pont, ton train.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "horloge,pluie",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "papier,pas",
        "CHK_T0000_P0000_END": "crayon",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "bonjour",
        "accepted_examples": "bonjour | s'il te plaît | merci | bonjour merci | s'il vous plaît",
        "retry_prompt": "Il dit bonjour. Que dit Aniss ?",
    },
    ("livre", "train", "crayon", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **le livre de trains**, puis le crayon bleu. Aniss veut le train, pas « apprendre merci ».",
        "Ouverture : radiateur, foulard mouillé, horloge. Pas la pluie sur la vitre d'abord.",
        "P0000 s'arrête : le tampon se pose, il montre le livre. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Aniss (plus Malik).",
        "C0001 : bonjour, s'il te plaît, merci. Puis le crayon, mêmes mots vécus, pas un recap.",
        "Fin : locomotive sur le papier, page ouverte. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Aniss = enfant-m. Attente du tampon (COL.ECO.002).",
    ],
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-04 N1 Victorina — tomate au marché
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-04",
    "Victorina veut la tomate ronde au bord de la caisse. Elle dit bonjour, s'il te plaît, merci. La tomate reste tiède.",
    "La tomate tiède de Victorina",
    "Victorina, papa, maman",
    "marché au soleil, caisses de tomates",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le soleil chauffe le bois des caisses.",
            "narrateur|Une feuille de tomate colle à une sandale.",
            "narrateur|Ça sent la terre, un peu sucrée.",
            "narrateur|Une bâche rayée claque au-dessus.",
            "narrateur|Le sac de papa est en toile grise.",
            "narrateur|Il pend à son épaule.",
            "maman|Tu as vu le rouge, Victorina ?",
            "enfant-f|Elles sont rouges, maman.",
            "papa|Bien rouges.",
            "narrateur|Les pavés sont encore un peu humides.",
            "narrateur|Une mouche tourne près d'une feuille.",
            "narrateur|Maman tient un panier d'osier.",
            "narrateur|L'osier gratte un peu le manteau.",
            "papa|Tu sens la terre, Victorina ?",
            "enfant-f|Oui, papa.",
            "enfant-f|C'est sucré un peu.",
            "narrateur|En ce moment, Victorina s'arrête.",
            "narrateur|Une tomate lisse brille au bord.",
            "narrateur|Elle est ronde.",
            "narrateur|Elle est un peu tiède.",
            "enfant-f|Je la veux, papa.",
            "papa|Tu restes près de nous.",
            "narrateur|Le marchand essuie une caisse.",
            "narrateur|Le bois est clair, un peu rêche.",
            "narrateur|Victorina se tient près de maman.",
            "maman|Il a le chiffon à la main.",
            "papa|On le laisse finir.",
            "narrateur|Le chiffon se pose sur le bois.",
            "narrateur|Le marchand lève la tête.",
            "narrateur|Victorina montre la tomate ronde.",
            "maman|Tu demandes, Victorina.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina veut la tomate.",
            "narrateur|Que dit-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-f|Bonjour.",
            "papa|Bonjour.",
            "enfant-f|Une tomate, s'il te plaît.",
            "enfant-f|Celle du bord.",
            "narrateur|Le marchand pose la tomate.",
            "narrateur|Elle est dans la main de Victorina.",
            "narrateur|Elle est lisse.",
            "narrateur|Elle est tiède.",
            "narrateur|Elle sent le jardin.",
            "enfant-f|Merci.",
            "maman|Merci.",
            "enfant-f|Elle est douce, papa.",
            "papa|Oui.",
            "maman|Tu la mets dans le sac ?",
            "enfant-f|Oui, maman.",
            "narrateur|Papa ouvre le sac de toile.",
            "narrateur|Victorina pose la tomate au fond.",
            "narrateur|Le sac sent le pain d'hier.",
            "papa|Tu tiens le bord ?",
            "enfant-f|Oui.",
            "narrateur|La bâche claque encore.",
            "narrateur|Une goutte brille sur la tomate.",
            "maman|On rentre tout doux.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils rentrent par la rue étroite.",
            "narrateur|Les pavés sonnent sous les chaussures.",
            "narrateur|Victorina tient encore le bord du sac.",
            "narrateur|La feuille a quitté la sandale.",
            "narrateur|À la maison, papa lave la tomate.",
            "narrateur|L'eau fait un petit bruit.",
            "maman|Tu veux un bout ?",
            "enfant-f|Oui, maman.",
            "enfant-f|S'il te plaît.",
            "narrateur|Victorina croque un bout.",
            "enfant-f|C'est doux.",
            "enfant-f|C'est un peu sucré.",
            "maman|Merci, Victorina.",
            "enfant-f|Merci, maman.",
            "papa|Merci, Victorina.",
            "narrateur|Une graine reste sur la table.",
            "maman|On la met de côté.",
            "enfant-f|La tomate était tiède.",
            "papa|Oui.",
            "papa|Comme au marché.",
            "narrateur|Le sac de toile repose près de l'évier.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Il reste un bout, bien rouge.",
            "narrateur|La graine attend sur la table.",
            "maman|Bonne journée, Victorina.",
            "papa|Elle était ronde, ta tomate.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "marche,bache",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "sac",
        "CHK_T0000_P0000_END": "eau",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "bonjour",
        "accepted_examples": "bonjour | s'il te plaît | merci | bonjour merci",
        "retry_prompt": "Elle dit bonjour. Que dit Victorina ?",
    },
    ("tomate", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **la tomate ronde** au bord de la caisse. Victorina veut la tomate, pas « dire les trois mots ».",
        "Ouverture : soleil sur le bois, feuille collée à la sandale. Pas la bâche d'abord.",
        "P0000 s'arrête : le marchand lève la tête, elle montre. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Victorina (plus Lucien, plus « Il dit »).",
        "C0001 : bonjour, s'il te plaît, merci. La tomate est tiède dans le sac.",
        "Fin : un bout sucré, une graine sur la table. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Victorina = enfant-f. POS-001 : elle montre, elle demande.",
    ],
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-05 N1 Sarah — poire du poirier
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-05",
    "Sarah veut la poire à joue dorée dans le panier sous le poirier. Elle dit bonjour, s'il te plaît, merci. Le jus reste froid.",
    "La poire dorée de Sarah",
    "Sarah, papa, maman",
    "jardin, poirier, panier de la voisine",
    {
        "CHK_T0000_P0000": [
            "narrateur|Les feuilles du poirier font une ombre ronde.",
            "narrateur|Un panier d'osier attend au pied.",
            "narrateur|Une poire a une joue dorée.",
            "narrateur|Ça sent le sucré, tout près.",
            "narrateur|L'herbe est chaude, un peu sèche.",
            "narrateur|Un arrosoir de zinc sonne contre une pierre.",
            "maman|Tu as vu la joue dorée, Sarah ?",
            "enfant-f|Elle brille, maman.",
            "papa|C'est la poire du panier.",
            "narrateur|La voisine remplit l'arrosoir.",
            "narrateur|L'eau chante dans le zinc.",
            "narrateur|Un oiseau picore sous l'arbre, tout petit.",
            "papa|Il cherche une miette.",
            "enfant-f|Il n'en a pas.",
            "narrateur|En ce moment, Sarah s'approche du panier.",
            "narrateur|La poire courte est bien ronde.",
            "narrateur|Sa peau est lisse, un peu froide.",
            "enfant-f|Celle-là, papa.",
            "papa|On lui parle tout doux.",
            "maman|L'arrosoir est encore plein.",
            "narrateur|La voisine pose l'arrosoir près de la pierre.",
            "narrateur|Elle se tourne vers le panier.",
            "narrateur|Sarah se tient près de maman.",
            "narrateur|Une petite feuille tient encore à la queue.",
            "enfant-f|Elle a un chapeau.",
            "maman|Un tout petit chapeau.",
            "maman|Tu demandes, Sarah.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah veut la poire.",
            "narrateur|Que dit-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-f|Bonjour.",
            "maman|Bonjour.",
            "enfant-f|Une poire, s'il te plaît.",
            "enfant-f|Celle avec la joue.",
            "narrateur|La voisine pose la poire.",
            "narrateur|Elle est dans le panier d'osier.",
            "narrateur|L'osier craque un tout petit peu.",
            "enfant-f|Merci.",
            "papa|Merci.",
            "narrateur|Sarah touche la poire du bout du doigt.",
            "narrateur|Elle est lisse.",
            "narrateur|Elle sent le sucré.",
            "enfant-f|Elle est froide, maman.",
            "maman|Oui.",
            "maman|Elle était sous les feuilles.",
            "papa|Le chapeau est encore là.",
            "enfant-f|Tout petit.",
            "narrateur|Sarah tient une anse du panier.",
            "narrateur|Le panier penche un peu, tout doux.",
            "maman|On rentre par l'herbe ?",
            "enfant-f|Oui, maman.",
            "narrateur|L'oiseau n'est plus sous l'arbre.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils rentrent le long de l'herbe sèche.",
            "narrateur|Les feuilles du poirier bougent un peu.",
            "narrateur|À la maison, maman pose le panier.",
            "narrateur|Sarah prend la poire à deux mains.",
            "papa|Tu veux un bout ?",
            "enfant-f|Oui, papa.",
            "enfant-f|S'il te plaît.",
            "narrateur|Sarah croque.",
            "narrateur|Le jus est sucré, un peu froid.",
            "enfant-f|Merci, papa.",
            "maman|Merci, Sarah.",
            "narrateur|La petite feuille reste sur la table.",
            "papa|Son chapeau.",
            "enfant-f|Oui.",
            "maman|On la met près de la fenêtre.",
            "enfant-f|Elle brille encore.",
            "papa|Moins qu'au jardin.",
            "narrateur|L'ombre du poirier n'est plus là.",
            "narrateur|Le panier d'osier est vide, maintenant.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Il reste un bout, encore froid.",
            "narrateur|La feuille dort près de la fenêtre.",
            "maman|Bonne après-midi, Sarah.",
            "papa|Elle avait une joue dorée.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "feuilles,eau",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "panier",
        "CHK_T0000_P0000_END": "croque",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "s'il te plaît",
        "accepted_examples": "s'il te plaît | merci | bonjour | s'il te plait",
        "retry_prompt": "Elle dit s'il te plaît. Que dit Sarah ?",
    },
    ("poire", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **la poire à joue dorée** sous le poirier. Sarah veut la poire, pas « les trois mots ».",
        "Ouverture : ombre ronde, panier, arrosoir de zinc. Pas l'étal du marché.",
        "P0000 s'arrête : la voisine se tourne, le chapeau-feuille. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Sarah (plus Louise).",
        "C0001 : bonjour, s'il te plaît, merci. La poire est froide dans l'osier.",
        "Fin : jus sucré, feuille près de la fenêtre. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Sarah = enfant-f.",
    ],
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-06 N3 Victorino — pomme + tulipe
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-06",
    "Victorino veut la pomme à joue rose, puis une tulipe pour la table. Il dit bonjour, s'il te plaît, merci aux deux dames. La tulipe tient dans le verre.",
    "La pomme et la tulipe de Victorino",
    "Victorino, papa, maman",
    "épicerie du chat gris, puis fleuriste",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un chat gris se tient sur le pas.",
            "narrateur|Il cligne, tout lent.",
            "narrateur|Une caisse de pommes sent le sucré.",
            "narrateur|Les pommes sont jaunes, avec un point rose.",
            "narrateur|Un volet tape tout doux dans le vent.",
            "papa|Le chat te regarde, Victorino.",
            "enfant-m|Il a des yeux jaunes.",
            "maman|Comme les pommes.",
            "narrateur|Une cloche de cuivre attend au-dessus de la porte.",
            "narrateur|En ce moment, Victorino pousse un peu.",
            "narrateur|La cloche fait ding.",
            "narrateur|L'air dedans est frais, un peu sucré.",
            "narrateur|Des bocaux brillent sur une étagère.",
            "enfant-m|Une pomme, maman.",
            "enfant-m|Celle à joue rose.",
            "maman|On s'approche du comptoir.",
            "narrateur|La dame essuie le bois du comptoir.",
            "narrateur|Le chiffon sent le citron.",
            "papa|Elle a le chiffon à la main.",
            "narrateur|Victorino s'arrête devant les pommes.",
            "narrateur|Le point rose brille sous la lampe.",
            "narrateur|Un rayon touche le verre des bocaux.",
            "narrateur|La dame pose le chiffon.",
            "narrateur|Elle lève les yeux.",
            "maman|Tu demandes, Victorino.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorino veut la pomme.",
            "narrateur|Que dit-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-m|Bonjour.",
            "papa|Bonjour.",
            "enfant-m|Une pomme, s'il te plaît.",
            "enfant-m|Celle à joue rose.",
            "narrateur|La dame tend une pomme jaune.",
            "narrateur|La peau est lisse, un peu froide.",
            "enfant-m|Merci.",
            "maman|Merci.",
            "enfant-m|Elle a une joue rose.",
            "papa|Oui.",
            "maman|Tu la tiens des deux mains.",
            "narrateur|Le chat est encore sur le pas.",
            "narrateur|Il ne les suit pas plus loin.",
            "narrateur|Plus tard, l'air change dans la rue.",
            "narrateur|Chez la fleuriste, ça sent fort.",
            "narrateur|Comme un jardin serré.",
            "narrateur|Des tulipes rouges tiennent dans un seau.",
            "narrateur|L'eau tremble un peu.",
            "enfant-m|Pour la table.",
            "enfant-m|Bonjour.",
            "enfant-m|Une fleur, s'il te plaît.",
            "narrateur|La dame tend une tulipe rouge.",
            "narrateur|La tige est lisse, un peu froide.",
            "narrateur|Une goutte glisse le long de la tige.",
            "enfant-m|Merci.",
            "maman|On la met dans l'eau, à la maison.",
            "narrateur|Victorino porte la pomme.",
            "narrateur|Il porte la tulipe, tout droit.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|À la maison, maman prend un verre.",
            "narrateur|L'eau fait un petit cercle.",
            "narrateur|La tulipe rouge se tient dedans.",
            "papa|Tu veux un bout de pomme ?",
            "enfant-m|Oui, papa.",
            "enfant-m|S'il te plaît.",
            "narrateur|Victorino croque.",
            "narrateur|C'est croquant.",
            "narrateur|C'est un peu sucré.",
            "enfant-m|Merci, papa.",
            "maman|Merci, Victorino.",
            "enfant-m|La tulipe a encore une goutte.",
            "papa|Oui.",
            "papa|Dans le verre, maintenant.",
            "narrateur|Le volet tape plus doux, dehors.",
            "maman|Le chat n'est plus sur le pas.",
            "enfant-m|Il clignait.",
            "papa|Tout lent.",
            "narrateur|Un rayon touche encore le verre.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La tulipe se tient dans le verre.",
            "narrateur|La pomme a une petite marque.",
            "maman|Bonne soirée, Victorino.",
            "papa|Elle a une joue rose, ta pomme.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cloche,volet",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "pas",
        "CHK_T0000_P0000_END": "verre",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "bonjour",
        "accepted_examples": "bonjour | s'il te plaît | merci | bonjour merci | s'il vous plaît",
        "retry_prompt": "Il dit bonjour. Que dit Victorino ?",
    },
    ("pomme", "tulipe", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **la pomme à joue rose**, puis la tulipe pour la table. Victorino veut les porter, pas « les mêmes mots ».",
        "Ouverture : chat gris sur le pas, yeux jaunes. Pas le sac qui court.",
        "P0000 s'arrête : le chiffon se pose, il montre la pomme. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Victorino (plus Ferdinand, plus Nino).",
        "C0001 : bonjour, s'il te plaît, merci. Puis la fleuriste, mêmes mots vécus. Le chat ne suit pas.",
        "Fin : tulipe dans le verre, marque dans la pomme. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Victorino = enfant-m.",
    ],
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-07 N1 Mila — gaufre de la place
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-07",
    "Mila veut la gaufre dorée qui sort du fer. Elle dit bonjour, s'il te plaît, merci. La vanille reste sur ses doigts.",
    "La gaufre de la place de Mila",
    "Mila, papa, maman",
    "place du village, fer à gaufres",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un pigeon picore une miette sur la place.",
            "narrateur|Le fer à gaufres souffle un peu de vapeur.",
            "narrateur|Ça sent la vanille, tout chaud.",
            "narrateur|Un banc de pierre est froid au soleil.",
            "narrateur|Papa tient la main de Mila.",
            "narrateur|Sa main est un peu collante, déjà.",
            "maman|Tu as senti la vanille, Mila ?",
            "enfant-f|Ça sent le gâteau.",
            "papa|C'est le fer.",
            "narrateur|La vapeur fait un petit nuage.",
            "narrateur|Il part vers les pigeons.",
            "papa|Tu vois le nuage, Mila ?",
            "enfant-f|Il s'en va.",
            "narrateur|En ce moment, Mila s'arrête près du fer.",
            "narrateur|Une gaufre dorée est encore fermée.",
            "narrateur|Le fer est chaud, tout silencieux.",
            "enfant-f|Je la veux, papa.",
            "papa|On reste près du fer.",
            "maman|On attend un peu.",
            "narrateur|La dame tourne le fer.",
            "narrateur|Le bois de la poignée est lisse.",
            "narrateur|Mila se tient près de maman.",
            "narrateur|Le fer s'ouvre.",
            "narrateur|La gaufre est dorée, avec des trous.",
            "narrateur|Un peu de vapeur monte encore.",
            "enfant-f|Elle a des trous.",
            "papa|Comme le fer.",
            "maman|Tu demandes, Mila.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila veut la gaufre.",
            "narrateur|Que dit-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-f|Bonjour.",
            "papa|Bonjour.",
            "enfant-f|Une gaufre, s'il te plaît.",
            "enfant-f|Celle qui est dorée.",
            "narrateur|La dame glisse la gaufre dans un papier.",
            "narrateur|Le papier est chaud, un peu gras.",
            "enfant-f|Merci.",
            "maman|Merci.",
            "narrateur|Mila tient le papier contre son manteau.",
            "narrateur|Ça sent la vanille, tout près.",
            "enfant-f|Elle est chaude, papa.",
            "papa|Oui.",
            "maman|La vapeur est sur ton nez.",
            "enfant-f|Ça chatouille.",
            "papa|Un tout petit nuage.",
            "narrateur|Le pigeon n'est plus sur la miette.",
            "narrateur|Le banc de pierre reste froid.",
            "maman|On s'assoit un moment ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le papier craque sur les genoux.",
            "papa|Tu le tiens des deux mains.",
            "enfant-f|Oui, papa.",
            "narrateur|Une miette de vanille reste sur le papier.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils restent sur le banc de pierre.",
            "narrateur|Le soleil touche le papier.",
            "maman|Tu veux un bout ?",
            "enfant-f|Oui, maman.",
            "enfant-f|S'il te plaît.",
            "narrateur|Mila croque.",
            "narrateur|C'est tiède.",
            "narrateur|Ça sent la vanille.",
            "enfant-f|Merci, maman.",
            "papa|Merci, Mila.",
            "enfant-f|Elle a des trous.",
            "maman|Oui.",
            "maman|Comme le fer.",
            "narrateur|Une miette tombe près du banc.",
            "papa|Pour le pigeon, peut-être.",
            "enfant-f|Il va revenir.",
            "narrateur|Le fer souffle encore, plus loin.",
            "maman|On garde le papier ?",
            "enfant-f|Il est encore chaud.",
            "papa|Oui.",
            "narrateur|Le pigeon revient près de la miette.",
            "enfant-f|Il l'a vue.",
            "maman|Tout doux, maintenant.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le papier repose sur le banc.",
            "narrateur|Il reste une miette, encore chaude.",
            "maman|Bonne matinée, Mila.",
            "papa|Elle était dorée, ta gaufre.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "vapeur,place",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "papier",
        "CHK_T0000_P0000_END": "croque",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "bonjour",
        "accepted_examples": "bonjour | s'il te plaît | merci | bonjour merci",
        "retry_prompt": "Elle dit bonjour. Que dit Mila ?",
    },
    ("gaufre", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **la gaufre dorée** du fer. Mila veut la gaufre, pas « dire merci ».",
        "Ouverture : pigeon, vapeur, vanille. Pas la farine sur la vitre (boulangerie de 01).",
        "P0000 s'arrête : le fer s'ouvre, elle voit les trous. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Mila (plus Fanny).",
        "C0001 : bonjour, s'il te plaît, merci. Vapeur sur le nez, papier chaud.",
        "Fin : miette pour le pigeon, banc de pierre. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Mila = enfant-f. POS-001 : on reste près du fer, on ne le touche pas.",
    ],
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-08 N2 Raphaël — brioche sous la lampe
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-08",
    "Raphaël veut la brioche floue dans la vitre embuée. Il dit bonjour, s'il te plaît, merci. Le sac reste tiède.",
    "La brioche sous la lampe de Raphaël",
    "Raphaël, papa, maman",
    "rue mouillée, boulangerie le soir",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une gouttière chante dans la rue.",
            "narrateur|L'eau tombe dans un seau, une goutte après l'autre.",
            "narrateur|Une odeur de sucre sort sous la porte.",
            "narrateur|Papa tient un parapluie encore mouillé.",
            "narrateur|Une goutte glisse le long du tissu.",
            "maman|Tu entends la gouttière, Raphaël ?",
            "enfant-m|Elle chante, maman.",
            "papa|Dans le seau.",
            "narrateur|La boulangerie a une lampe ronde.",
            "narrateur|La vitre est embuée, tout en bas.",
            "narrateur|Une brioche dorée s'y dessine, un peu floue.",
            "enfant-m|Je la vois, papa.",
            "maman|Oui.",
            "papa|On entre.",
            "narrateur|En ce moment, ils poussent la porte.",
            "narrateur|Une cloche fait ding, tout doux.",
            "narrateur|L'air est chaud, comme une couverture.",
            "narrateur|Ça sent la brioche et le sucre.",
            "narrateur|La boulangère range des pains ronds.",
            "maman|Elle a les mains pleines.",
            "papa|On attend un peu.",
            "narrateur|Raphaël s'arrête sous la lampe.",
            "narrateur|Un sac en papier attend sur le marbre.",
            "enfant-m|Il est vide, ce sac.",
            "papa|Pour la brioche, après.",
            "narrateur|La boulangère pose un pain.",
            "narrateur|Elle se tourne, le torchon à la main.",
            "maman|Tu demandes, Raphaël.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Raphaël veut la brioche.",
            "narrateur|Que dit-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-m|Bonjour.",
            "maman|Bonjour.",
            "enfant-m|Une brioche, s'il te plaît.",
            "enfant-m|Celle de la vitre.",
            "narrateur|La boulangère glisse la brioche dans un sac.",
            "narrateur|Le papier craque, un peu gras.",
            "enfant-m|Merci.",
            "papa|Merci.",
            "narrateur|Raphaël tient le sac à deux mains.",
            "narrateur|Le fond du sac est tiède.",
            "enfant-m|Elle est chaude, maman.",
            "maman|Oui.",
            "papa|Un grain de sucre sur ton pouce.",
            "enfant-m|Il brille.",
            "maman|Tu le goûtes ?",
            "enfant-m|Il est sucré.",
            "narrateur|Ils restent un moment près de la vitre.",
            "narrateur|Raphaël dessine un petit rond du doigt.",
            "narrateur|La brioche n'est plus floue, dehors.",
            "papa|Elle est dans le sac, maintenant.",
            "maman|On garde le sac au chaud.",
            "enfant-m|Oui, maman.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils rentrent le long de la gouttière.",
            "narrateur|Le seau est presque plein.",
            "narrateur|Le parapluie goutte encore un peu.",
            "narrateur|À la maison, maman ouvre le sac.",
            "narrateur|La brioche sent le beurre, tout fort.",
            "papa|Tu veux un bout ?",
            "enfant-m|Oui, papa.",
            "enfant-m|S'il te plaît.",
            "narrateur|Raphaël croque.",
            "narrateur|C'est doux.",
            "narrateur|C'est un peu sucré.",
            "enfant-m|Merci, papa.",
            "maman|Merci, Raphaël.",
            "narrateur|Le sac vide reste sur la table, encore tiède.",
            "papa|La gouttière chante moins, dehors.",
            "enfant-m|Le seau est plein.",
            "maman|Oui.",
            "maman|Et la brioche est à toi.",
            "papa|Plus floue du tout.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le sac tiède repose sur la table.",
            "narrateur|Il reste un bout, un peu sucré.",
            "maman|Bonne soirée, Raphaël.",
            "papa|Elle n'est plus floue, ta brioche.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "gouttiere,cloche",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "papier",
        "CHK_T0000_P0000_END": "pas",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "bonjour",
        "accepted_examples": "bonjour | s'il te plaît | merci",
        "retry_prompt": "Il dit bonjour. Que dit Raphaël ?",
    },
    ("brioche", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **la brioche floue** dans la vitre. Raphaël veut la brioche, pas « les trois mots ».",
        "Ouverture : gouttière, seau, odeur de sucre. Pas le réverbère d'abord, pas la farine de 01.",
        "P0000 s'arrête : la boulangère se tourne. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Raphaël (plus Pascal).",
        "C0001 : bonjour, s'il te plaît, merci. Grain de sucre sur le pouce.",
        "Fin : sac tiède, gouttière plus calme. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Raphaël = enfant-m.",
    ],
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-09 N1 Nina — fromage
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-09",
    "Nina veut le petit morceau beige sous le linge à trous. Elle dit bonjour, s'il te plaît, merci. Le sac reste froid.",
    "Le morceau frais de Nina",
    "Nina, papa, maman",
    "fromagerie, linge blanc, cloche de verre",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un linge blanc a de petits trous.",
            "narrateur|Un rayon y passe, tout pâle.",
            "narrateur|Ça sent le lait froid.",
            "narrateur|Des fromages ronds dorment dessous.",
            "narrateur|Une cloche de verre tient un morceau.",
            "narrateur|Le verre est un peu embué, tout doux.",
            "papa|Tu as vu les trous, Nina ?",
            "enfant-f|Comme des fenêtres.",
            "maman|Tout petits.",
            "narrateur|Papa pousse la porte tout doux.",
            "narrateur|Un souffle frais sort de la boutique.",
            "narrateur|Une petite cloche fait ding, tout bas.",
            "maman|Tu as senti le lait, Nina ?",
            "enfant-f|Oui, maman.",
            "enfant-f|C'est frais.",
            "papa|Comme le matin.",
            "narrateur|Le carrelage est froid sous les chaussures.",
            "maman|Tu as les pieds froids, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|En ce moment, Nina s'arrête au comptoir.",
            "narrateur|Un petit morceau beige est sur une feuille.",
            "narrateur|La feuille craque un peu.",
            "enfant-f|Celui-là, papa.",
            "papa|On s'approche du comptoir.",
            "maman|Elle plie encore le linge.",
            "narrateur|Nina se tient près de maman.",
            "narrateur|Elle regarde par un trou du linge.",
            "enfant-f|Je vois le morceau.",
            "maman|Oui.",
            "narrateur|La dame pose le linge.",
            "narrateur|Elle lève les yeux.",
            "papa|Tu demandes, Nina.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nina veut le morceau.",
            "narrateur|Que dit-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-f|Bonjour.",
            "maman|Bonjour.",
            "enfant-f|Un morceau, s'il te plaît.",
            "enfant-f|Celui de la feuille.",
            "narrateur|La dame glisse le morceau dans un sac.",
            "narrateur|Le sac est frais, un peu lourd.",
            "enfant-f|Merci.",
            "papa|Merci.",
            "narrateur|Nina tient le sac contre son manteau.",
            "narrateur|Ça sent le lait, tout près.",
            "enfant-f|Il est froid, papa.",
            "papa|Oui.",
            "maman|Comme le carrelage.",
            "enfant-f|Mes mains sont froides.",
            "papa|On les met dans tes poches ?",
            "enfant-f|Le sac aussi.",
            "maman|Tout contre toi.",
            "narrateur|Le linge blanc couvre encore les ronds.",
            "narrateur|Le rayon pâle n'y passe plus.",
            "papa|On rentre ?",
            "enfant-f|Oui, papa.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils rentrent par la rue étroite.",
            "narrateur|Les pavés sont secs, maintenant.",
            "narrateur|Nina tient encore le bord du sac.",
            "narrateur|À la maison, papa ouvre le sac.",
            "narrateur|Le morceau est pâle, un peu doux au nez.",
            "maman|Tu veux sentir ?",
            "enfant-f|Oui, maman.",
            "enfant-f|S'il te plaît.",
            "narrateur|Nina se penche.",
            "enfant-f|Ça sent le lait.",
            "maman|On le met sur le pain ?",
            "enfant-f|Oui.",
            "narrateur|Papa pose un petit carré sur une tartine.",
            "enfant-f|Merci, papa.",
            "papa|Merci, Nina.",
            "narrateur|Le sac reste frais, sur la table.",
            "maman|Tes mains sont moins froides ?",
            "enfant-f|Un peu.",
            "papa|Le pain est doux.",
            "narrateur|Nina croque un tout petit bout.",
            "enfant-f|C'est frais.",
            "maman|Oui.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le sac frais repose près du pain.",
            "narrateur|Il reste un bout, tout pâle.",
            "maman|Bonne journée, Nina.",
            "papa|Il sentait le lait, ton morceau.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cloche,porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "papier",
        "CHK_T0000_P0000_END": "pain",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "bonjour",
        "accepted_examples": "bonjour | s'il te plaît | merci | bonjour merci",
        "retry_prompt": "Elle dit bonjour. Que dit Nina ?",
    },
    ("morceau", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **le morceau beige** sous le linge. Nina veut le morceau, pas « dire les mots ».",
        "Ouverture : trous du linge, rayon pâle, lait froid. Pas le carrelage d'abord.",
        "P0000 s'arrête : elle regarde par un trou, la dame lève les yeux. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Nina (plus David).",
        "C0001 : bonjour, s'il te plaît, merci. Sac froid contre le manteau.",
        "Fin : tartine, sac près du pain. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Nina = enfant-f.",
    ],
)


# ---------------------------------------------------------------------------
# ATOM-COL.POL.001-10 N1 Amir — croissant du bout
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.POL.001-10",
    "Amir veut le croissant du bout de la rangée. Il dit bonjour, s'il te plaît, merci. Une miette dorée reste sur sa manche.",
    "Le croissant du bout d'Amir",
    "Amir, papa, maman",
    "paillasson mouillé, boulangerie le matin",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le paillasson sent encore la pluie.",
            "narrateur|Les lacets d'Amir laissent deux traits mouillés.",
            "narrateur|Derrière la porte, le four souffle.",
            "narrateur|Ça sent le beurre, déjà.",
            "narrateur|Papa porte un journal encore un peu humide.",
            "narrateur|Le papier du journal sent l'encre.",
            "maman|Tes lacets sont mouillés, Amir.",
            "enfant-m|Ils tapent, maman.",
            "papa|Deux petits tap-tap.",
            "maman|On les entend, hein ?",
            "enfant-m|Oui.",
            "narrateur|De la vapeur colle à la vitre, en bas.",
            "narrateur|Un croissant s'y dessine, un peu flou.",
            "enfant-m|Celui du bout.",
            "papa|On montre celui du bout.",
            "narrateur|En ce moment, Amir pose le pied.",
            "narrateur|Le paillasson est rêche, un peu chaud.",
            "narrateur|Maman pousse la porte.",
            "narrateur|Une cloche fait ding.",
            "narrateur|L'air sent le beurre et le pain.",
            "narrateur|Les croissants sont dorés, en rang.",
            "enfant-m|Ils sont tous pareils.",
            "papa|Sauf celui du bout.",
            "enfant-m|Il est plus brun.",
            "narrateur|La dame essuie une miette sur le marbre.",
            "maman|Elle a le torchon.",
            "papa|On la laisse finir.",
            "narrateur|La miette part.",
            "narrateur|La dame lève les yeux.",
            "narrateur|Amir montre le croissant du bout.",
            "maman|Tu demandes, Amir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Amir veut le croissant.",
            "narrateur|Que dit-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-m|Bonjour.",
            "papa|Bonjour.",
            "enfant-m|Un croissant, s'il te plaît.",
            "enfant-m|Celui du bout.",
            "narrateur|La dame glisse le croissant dans un sac.",
            "narrateur|Le sac est chaud.",
            "narrateur|Le papier craque.",
            "enfant-m|Merci.",
            "maman|Merci.",
            "narrateur|Amir tient le sac à deux mains.",
            "narrateur|Ça sent le beurre, tout près du nez.",
            "enfant-m|Il est chaud, maman.",
            "maman|Oui.",
            "papa|Une miette sur ta manche.",
            "enfant-m|Elle est dorée.",
            "maman|Tu la goûtes ?",
            "enfant-m|Elle est bonne.",
            "narrateur|Ils restent un moment près de la vitre.",
            "narrateur|Dehors, les lacets ne tapent plus.",
            "papa|On rentre ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le sac fume un peu, tout doux.",
            "maman|Tu le tiens haut ?",
            "enfant-m|Oui.",
            "papa|Comme ça, il reste chaud.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils rentrent le long de la rue mouillée.",
            "narrateur|Le croissant fume encore, tout doux.",
            "narrateur|À la maison, papa ouvre le sac.",
            "narrateur|Le croissant est doré, un peu cassant.",
            "maman|Tu veux un bout ?",
            "enfant-m|Oui, maman.",
            "enfant-m|S'il te plaît.",
            "narrateur|Amir croque.",
            "enfant-m|C'est tiède.",
            "enfant-m|Ça sent le beurre.",
            "enfant-m|Merci, maman.",
            "papa|Merci, Amir.",
            "narrateur|Des miettes dorées restent au fond du sac.",
            "maman|Tes lacets sèchent, maintenant.",
            "enfant-m|Ils ne tapent plus.",
            "papa|Non.",
            "maman|C'était celui du bout.",
            "enfant-m|Oui.",
            "narrateur|Le paillasson, loin, garde encore la pluie.",
            "papa|Le journal sèche, lui aussi.",
            "enfant-m|Il était mouillé.",
            "maman|Un peu, oui.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le sac repose sur la table.",
            "narrateur|Il reste une miette, encore tiède.",
            "maman|Bonne matinée, Amir.",
            "papa|C'était celui du bout.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "paillasson,cloche",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "papier",
        "CHK_T0000_P0000_END": "sac",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "expected_answer": "bonjour",
        "accepted_examples": "bonjour | s'il te plaît | merci | bonjour merci",
        "retry_prompt": "Il dit bonjour. Que dit Amir ?",
    },
    ("croissant", "bonjour", "s'il te plaît", "merci"),
    [
        "Fil : **le croissant du bout**. Amir veut celui-là, pas « les trois mots ».",
        "Ouverture : paillasson, lacets mouillés, four. Pas la flaque avec le ciel.",
        "P0000 s'arrête : il montre le croissant du bout. Les mots ne sont pas encore dits.",
        "Q0001 au moment du besoin. retry_prompt : Amir (plus Félix).",
        "C0001 : bonjour, s'il te plaît, merci. Miette dorée sur la manche.",
        "Fin : lacets secs, miettes au fond du sac. « L'histoire est finie. »",
        "Papa et maman parlent. Troupe D16. Amir = enfant-m.",
    ],
)
