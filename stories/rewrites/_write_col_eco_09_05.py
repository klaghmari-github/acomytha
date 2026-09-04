#!/usr/bin/env python3
"""F-NAR-008 — merged.json ATOM-COL.ECO.001-09..11 et 002-01..05."""
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
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom", "léa", "lea", "lina", "iris",
    "denis", "hadrien", "sylvain", "sami", "fatou", "idris", "flora",
    "constentin", "luca", "céline", "celine", "lucas",
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


def make_chunk(src: dict, lines: list[str], sons, age: str, qmeta: dict | None) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
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
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, age, out["chunks"], need)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


NEED_001 = ("écouter", "raconter", "malaise")
NEED_002 = ("attendre", "main", "parl")


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.001-09 N3 Victorina — soleil sur la buée
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.001-09",
    "La casserole frémit. La buée fait un rond sur la vitre. Victorina peint un soleil jaune. Un chuchotement lui serre le ventre. Le soir, elle raconte, et le soleil va sur la fenêtre.",
    "Le soleil sur la buée",
    "Victorina, papa, maman, maîtresse",
    "cuisine, atelier peinture, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|La casserole frémit sur le feu.",
            "narrateur|Une buée ronde s'étale sur la vitre.",
            "narrateur|Ça sent l'orange pelée, un peu vive.",
            "narrateur|Les gouttes d'huile brillent sur les doigts de maman.",
            "narrateur|Papa essuie la table avec une éponge jaune.",
            "narrateur|L'éponge est froide, encore mouillée.",
            "narrateur|Dehors, le village est gris et calme.",
            "papa|Victorina, tu vois le rond sur la vitre ?",
            "enfant-f|Oui, papa.",
            "enfant-f|On dirait un soleil.",
            "enfant-f|Maman, je veux un vrai soleil, en jaune.",
            "enfant-f|Pour la fenêtre de la cuisine.",
            "maman|On pourra le peindre à l'école.",
            "maman|Tu écoutes la maîtresse, d'accord ?",
            "enfant-f|Oui, maman.",
            "narrateur|Papa glisse un biscuit dans la poche.",
            "narrateur|Le biscuit sent le beurre.",
            "papa|Il est pour plus tard.",
            "narrateur|En ce moment, Victorina pousse la porte de l'atelier.",
            "narrateur|La table a une nappe bleue, un peu tâchée.",
            "narrateur|Les pots de peinture sont ouverts.",
            "narrateur|Ça sent le papier mouillé.",
            "narrateur|Un pinceau attend près de l'eau.",
            "maitresse|On écoute d'abord.",
            "maitresse|Ensuite, on peint un rond.",
            "maitresse|Puis on lave les pinceaux.",
            "narrateur|Victorina aime écouter.",
            "narrateur|Elle prend le pinceau.",
            "narrateur|Le bois est lisse, un peu collant.",
            "narrateur|Elle plonge le poil dans le jaune.",
            "narrateur|Le jaune est épais.",
            "enfant-f|C'est mon soleil, maîtresse.",
            "maitresse|Oui, Victorina.",
            "maitresse|Tu as bien écouté.",
            "maitresse|Maintenant, on lave les pinceaux.",
            "narrateur|Victorina va vers le bac.",
            "narrateur|L'eau devient un peu jaune.",
            "narrateur|Elle lave le poil, tout doucement.",
            "narrateur|Le soleil reste sur la feuille, encore humide.",
            "narrateur|Près du bac, quelqu'un parle tout bas.",
            "narrateur|Victorina entend parler d'un secret.",
            "narrateur|Son ventre se serre.",
            "narrateur|Ses joues deviennent chaudes.",
            "narrateur|Elle pose le pinceau propre.",
            "enfant-f|Je raconterai à la maison.",
            "narrateur|Le soir, la casserole frémit encore.",
            "narrateur|La buée revient sur la vitre.",
            "narrateur|Ça sent le poireau.",
            "narrateur|Papa tourne la soupe.",
            "papa|Tu as faim, Victorina ?",
            "narrateur|Victorina s'approche de la table.",
            "narrateur|Elle a encore le ventre serré.",
            "narrateur|Le soleil peint est dans le cartable.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina a un malaise.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-f|Papa, j'ai eu un malaise.",
            "enfant-f|Quelqu'un a parlé d'un secret.",
            "narrateur|Maman pose la louche.",
            "maman|Tu as bien fait de raconter.",
            "maman|On aime écouter la maîtresse.",
            "papa|Si tu as un malaise, tu viens raconter.",
            "papa|À papa ou à maman.",
            "narrateur|Victorina respire.",
            "narrateur|Son ventre se desserre, tout doucement.",
            "enfant-f|J'ai peint un soleil.",
            "enfant-f|Il est dans le cartable.",
            "maman|On le sort ?",
            "enfant-f|Oui.",
            "narrateur|Papa ouvre le cartable.",
            "narrateur|La feuille est un peu gondolée.",
            "narrateur|Le jaune brille encore.",
            "papa|Il est rond, comme la buée.",
            "maman|Tu as écouté, puis tu as peint.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Papa tient la feuille contre la vitre.",
            "narrateur|La buée fait un halo autour du jaune.",
            "enfant-f|Le soleil est à sa place.",
            "maman|Tu veux un peu d'eau ?",
            "enfant-f|Oui, maman.",
            "narrateur|Victorina boit une gorgée.",
            "narrateur|L'eau est fraîche.",
            "papa|Je te tiens la main ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sa main est chaude.",
            "maman|Le biscuit est encore dans ta poche.",
            "maman|Tu le manges après la soupe ?",
            "enfant-f|Oui.",
            "narrateur|La casserole frémit plus bas.",
            "narrateur|La cuisine est calme.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Mon soleil est sur la vitre.",
            "enfant-f|J'ai écouté.",
            "enfant-f|Puis j'ai raconté.",
            "maman|On t'a écoutée aussi.",
            "papa|Bravo, Victorina.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "casserole,eau", "CHK_T0000_P0000_END": "verre"},
    {
        "expected_answer": "raconter",
        "accepted_examples": "raconter | elle raconte | à papa | à la maison | écouter",
        "retry_prompt": "Elle raconte à papa. Que fait Victorina ?",
    },
    NEED_001,
)


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.001-10 N1 Chouchou — livre rouge du bateau
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.001-10",
    "La cuillère tape la casserole. Chouchou veut le livre rouge du bateau. Un chuchotement lui serre le ventre. Le soir, il raconte, et papa ouvre le bateau à la maison.",
    "Le livre rouge de Chouchou",
    "Chouchou, papa, maman, maîtresse",
    "cuisine, coin tapis, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|La cuillère en bois tape la casserole.",
            "narrateur|Toc.",
            "narrateur|Toc.",
            "narrateur|Ça sent les lentilles chaudes.",
            "narrateur|Une chaussette bleue attend sur la chaise.",
            "narrateur|La vapeur fait un nuage bas.",
            "narrateur|Papa remue tout doucement.",
            "maman|Le doudou est dans le sac.",
            "maman|Il t'attend ce soir.",
            "enfant-m|Je veux le livre rouge.",
            "enfant-m|Celui avec le bateau.",
            "papa|Il est au coin tapis.",
            "papa|Tu écoutes la maîtresse, Chouchou ?",
            "enfant-m|Oui, papa.",
            "maman|Tu écoutes, puis tu regardes.",
            "enfant-m|Oui, maman.",
            "narrateur|En ce moment, Chouchou s'assoit.",
            "narrateur|Le tapis est bleu, tout doux.",
            "narrateur|Ça chatouille un peu les genoux.",
            "narrateur|Un rayon touche une page.",
            "narrateur|Les livres sentent le papier.",
            "narrateur|Les chaussons sont en rang.",
            "maitresse|On écoute.",
            "maitresse|Ensuite, on range les livres.",
            "narrateur|Chouchou aime écouter.",
            "narrateur|Il cherche le livre rouge.",
            "narrateur|Le dos du livre est rêche.",
            "narrateur|Il l'ouvre.",
            "narrateur|Le bateau a une voile.",
            "enfant-m|La voile est grande, maîtresse.",
            "maitresse|Oui, Chouchou.",
            "maitresse|Tu as bien écouté.",
            "maitresse|On range, maintenant.",
            "narrateur|Chouchou pose le livre dans le bac.",
            "narrateur|Les pages font un petit bruit.",
            "narrateur|Plus tard, quelqu'un parle tout bas.",
            "narrateur|Chouchou entend parler d'un secret.",
            "narrateur|Son ventre se serre.",
            "narrateur|Il pose les mains sur le tapis.",
            "enfant-m|Je raconterai à la maison.",
            "narrateur|Le soir, papa coupe des carottes.",
            "narrateur|Ça sent la terre.",
            "narrateur|Les ronds orange brillent.",
            "papa|Tu as faim, Chouchou ?",
            "narrateur|Chouchou vient près de la table.",
            "narrateur|Il a encore le ventre serré.",
            "narrateur|Le doudou attend dans le sac.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Chouchou a un malaise.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-m|Papa, j'ai eu un malaise.",
            "enfant-m|Quelqu'un a parlé d'un secret.",
            "narrateur|Maman s'approche.",
            "maman|Tu as bien fait de raconter.",
            "maman|On aime écouter la maîtresse.",
            "papa|Si tu as un malaise, tu viens raconter.",
            "papa|À papa ou à maman.",
            "narrateur|Chouchou respire.",
            "enfant-m|J'ai vu le bateau.",
            "enfant-m|Dans le livre rouge.",
            "maman|On a un livre, ici aussi.",
            "maman|Tu veux le voir ?",
            "enfant-m|Oui.",
            "narrateur|Papa prend un livre sur l'étagère.",
            "narrateur|La couverture est un peu usée.",
            "narrateur|Il y a un bateau, lui aussi.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Papa ouvre le livre.",
            "narrateur|La voile est un peu pliée.",
            "enfant-m|Il va jusqu'à demain.",
            "papa|Je te tiens la main ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sa main est chaude.",
            "maman|Tu prends le doudou ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le doudou sent la maison.",
            "narrateur|Papa verse un verre d'eau.",
            "narrateur|Chouchou boit une gorgée.",
            "maman|L'eau est fraîche.",
            "narrateur|La cuillère repose dans la casserole.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai vu le bateau.",
            "enfant-m|J'ai écouté.",
            "enfant-m|Puis j'ai raconté.",
            "maman|On t'a écouté.",
            "papa|Bravo, Chouchou.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "casserole,pages", "CHK_T0000_P0000_END": "verre,pages"},
    {
        "expected_answer": "raconter",
        "accepted_examples": "raconter | il raconte | à papa | à la maison | écouter",
        "retry_prompt": "Il raconte à papa. Que fait Chouchou ?",
    },
    NEED_001,
)


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.001-11 N1 Sarah — oiseau de papier
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.001-11",
    "Un oiseau de papier pose sur la salière. Sarah veut lui dessiner une aile verte. Un chuchotement lui serre le ventre. Le soir, elle raconte, et l'oiseau gagne son aile.",
    "L'oiseau de papier de Sarah",
    "Sarah, papa, maman, maîtresse",
    "cuisine, coin tapis, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un oiseau de papier pose sur la salière.",
            "narrateur|Le papier fait un petit frou.",
            "narrateur|Ça sent le pain grillé.",
            "narrateur|Des miettes dorées sont sur la nappe.",
            "narrateur|Un rayon touche l'aile pliée.",
            "narrateur|La salière est un peu froide.",
            "narrateur|Maman a plié l'oiseau ce matin.",
            "maman|Il est léger, tu vois ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Je veux lui dessiner une aile.",
            "enfant-f|Une aile verte.",
            "papa|Tu pourras à l'école.",
            "papa|Tu écoutes la maîtresse.",
            "enfant-f|Oui, papa.",
            "maman|Les lacets sont bien faits.",
            "narrateur|En ce moment, Sarah s'assoit.",
            "narrateur|Le tapis a un carré d'or.",
            "narrateur|Les cubes sont dans leur bac.",
            "maitresse|On écoute.",
            "maitresse|Ensuite, on range les crayons.",
            "narrateur|Sarah aime écouter.",
            "narrateur|Elle prend un crayon vert.",
            "narrateur|Le bois est un peu râpeux.",
            "narrateur|Elle dessine une aile, tout doux.",
            "narrateur|L'aile a une petite plume.",
            "narrateur|Le vert sent un peu le bois.",
            "enfant-f|C'est pour l'oiseau, maîtresse.",
            "maitresse|Oui, Sarah.",
            "maitresse|Tu as bien écouté.",
            "maitresse|On range, maintenant.",
            "narrateur|Sarah pose le crayon dans la boîte.",
            "narrateur|L'aile verte reste sur la feuille.",
            "narrateur|Plus tard, quelqu'un parle tout bas.",
            "narrateur|Sarah entend parler d'un secret.",
            "narrateur|Son ventre se serre.",
            "narrateur|Elle pose la feuille près d'elle.",
            "enfant-f|Je raconterai à la maison.",
            "narrateur|Le soir, papa coupe du pain.",
            "narrateur|La croûte fait un petit bruit.",
            "narrateur|Ça sent le four.",
            "papa|Tu as faim, Sarah ?",
            "narrateur|Sarah vient près de la planche.",
            "narrateur|Elle a encore le ventre serré.",
            "narrateur|L'oiseau de papier attend sur la salière.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah a un malaise.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "enfant-f|Papa, j'ai un malaise.",
            "enfant-f|Quelqu'un a parlé d'un secret.",
            "narrateur|Maman pose le beurre.",
            "maman|Tu as bien fait de raconter.",
            "maman|On aime écouter la maîtresse.",
            "papa|Si tu as un malaise, tu viens raconter.",
            "papa|À papa ou à maman.",
            "narrateur|Sarah respire.",
            "enfant-f|J'ai dessiné une aile verte.",
            "maman|On la colle sur l'oiseau ?",
            "enfant-f|Oui.",
            "narrateur|Papa prend la feuille.",
            "narrateur|L'aile est un peu recourbée.",
            "narrateur|Il la pose près du papier plié.",
            "papa|Elle va bien, là ?",
            "enfant-f|Un peu plus près du bec.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman tient l'oiseau.",
            "narrateur|L'aile verte le rejoint.",
            "enfant-f|Il peut partir.",
            "papa|Je te tiens la main ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sa main est chaude.",
            "maman|Tu veux un bout de pain ?",
            "enfant-f|Oui, maman.",
            "narrateur|La mie est toute douce.",
            "narrateur|Papa verse un verre d'eau.",
            "narrateur|Sarah boit une gorgée.",
            "narrateur|L'oiseau reste près de la salière.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|L'oiseau a son aile.",
            "enfant-f|J'ai écouté.",
            "enfant-f|J'ai raconté.",
            "maman|On t'a écoutée.",
            "papa|Bravo, Sarah.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "papier,pain", "CHK_T0000_P0000_END": "verre,pain"},
    {
        "expected_answer": "raconter",
        "accepted_examples": "raconter | elle raconte | à papa | à la maison | écouter",
        "retry_prompt": "Elle raconte à papa. Que fait Sarah ?",
    },
    NEED_001,
)


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.002-01 N2 Amir — nez rose du lapin
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.002-01",
    "Une carotte sent encore la terre. Amir veut dire que le lapin a un nez rose. Il lève la main, il attend, puis il le dit et le dessine.",
    "Le nez rose d'Amir",
    "Amir, papa, maman, maîtresse",
    "cuisine, classe, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un sac en papier craque sur la table.",
            "narrateur|Dedans, une carotte sent encore la terre.",
            "narrateur|Un peu de terre est sur le carreau.",
            "narrateur|Une chaussette blanche a une oreille de lapin.",
            "narrateur|Le jardin, derrière la porte, sent l'herbe mouillée.",
            "maman|La carotte est pour plus tard, Amir.",
            "enfant-m|Le lapin du livre a un nez rose.",
            "enfant-m|Tout petit.",
            "papa|Tu pourras le dire à l'école.",
            "papa|Tu attends ton tour, d'accord ?",
            "enfant-m|D'accord, papa.",
            "maman|Le cartable est un peu lourd.",
            "maman|Tu vas bien t'asseoir ?",
            "enfant-m|Oui, maman.",
            "narrateur|En ce moment, Amir arrive en classe.",
            "narrateur|Le tapis est gris, un peu rêche.",
            "maman|Au revoir, Amir.",
            "maman|Bonne journée.",
            "enfant-m|Au revoir, maman.",
            "narrateur|Amir s'assoit sur le tapis.",
            "narrateur|Ses pieds restent bien posés.",
            "narrateur|Une feuille jaune est collée sous une chaussure.",
            "narrateur|Le vent pousse encore les arbres du jardin.",
            "narrateur|La maîtresse montre une image.",
            "narrateur|C'est un lapin blanc.",
            "narrateur|Les oreilles sont trop longues.",
            "narrateur|Le nez est rose, tout petit.",
            "maitresse|On écoute d'abord l'image.",
            "maitresse|Qui veut parler du lapin ?",
            "narrateur|Amir a une idée.",
            "narrateur|Le nez est rose, comme une gomme.",
            "narrateur|Les mots lui chatouillent la bouche.",
            "enfant-m|Je veux parler du nez.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Amir veut parler.",
            "narrateur|Que fait-il d'abord ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir lève la main.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Il faut attendre.",
            "narrateur|Il attend.",
            "narrateur|Quelqu'un parle d'abord.",
            "narrateur|On entend parler des oreilles.",
            "narrateur|Amir attend encore.",
            "narrateur|Il regarde le petit nez rose.",
            "maitresse|Amir, c'est ton tour.",
            "narrateur|Amir parle, tout doucement.",
            "enfant-m|Le lapin a un nez rose.",
            "enfant-m|Tout petit.",
            "maitresse|Merci, Amir.",
            "maitresse|Tu as attendu.",
            "maitresse|Puis tu as parlé.",
            "maitresse|Tu veux dessiner le nez ?",
            "enfant-m|Oui.",
            "narrateur|Amir prend un crayon rose.",
            "narrateur|Le crayon sent un peu le bois.",
            "narrateur|Il fait un point, tout rond.",
            "narrateur|Le point est trop gros, d'abord.",
            "narrateur|Il le frotte un peu, tout doux.",
            "narrateur|Le lapin a son nez, sur le papier.",
            "maitresse|Le nez est bien là.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Le soir, maman ouvre la porte.",
            "narrateur|La fermeture du cartable fait un petit zzz.",
            "maman|Alors, Amir ?",
            "enfant-m|J'ai dit le nez rose.",
            "enfant-m|Il est sur le papier.",
            "papa|Tu montres ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le point rose est un peu fort.",
            "maman|Il est bien là.",
            "papa|La carotte est encore dans le sac.",
            "papa|Tu la croques en chemin ?",
            "enfant-m|Oui.",
            "maman|Tu mets ton manteau ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le manteau sent le jardin.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Le nez rose est sur le papier.",
            "enfant-m|J'ai levé la main.",
            "enfant-m|J'ai attendu.",
            "enfant-m|Puis j'ai parlé.",
            "maman|Bravo, Amir.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "sac,porte", "CHK_T0000_P0000_END": "porte,manteau"},
    {
        "expected_answer": "attendre",
        "accepted_examples": "attendre | il attend | lever la main | la main",
        "retry_prompt": "Il lève la main et il attend. Que fait Amir ?",
    },
    NEED_002,
)


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.002-02 N3 Nino — mer dans la coquille
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.002-02",
    "Des grains de sable restent sur le paillasson. Nino veut entendre la mer dans la coquille. Il lève la main, il attend, puis il l'écoute contre son oreille.",
    "La mer dans la coquille",
    "Nino, papa, maman, maîtresse",
    "entrée, classe, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|Des grains de sable restent sur le paillasson.",
            "narrateur|Ils piquent un peu sous le pied.",
            "narrateur|Un seau en fer est près des bottes.",
            "narrateur|Le seau sent encore le bord de l'eau.",
            "narrateur|Le radiateur fait tic-tic, tout bas.",
            "papa|Le galet lisse reste à la maison.",
            "papa|Toi, tu vas à l'école.",
            "enfant-m|Je veux entendre la mer.",
            "enfant-m|Dans une coquille.",
            "maman|Tes mains sont un peu froides.",
            "maman|Tu vas t'asseoir sur le tapis ?",
            "enfant-m|Oui, maman.",
            "papa|Tu attends ton tour, d'accord ?",
            "enfant-m|D'accord, papa.",
            "narrateur|En ce moment, Nino pousse la porte.",
            "maman|Au revoir, Nino.",
            "maman|Bonne journée.",
            "enfant-m|Au revoir, maman.",
            "narrateur|Nino s'assoit sur le tapis.",
            "narrateur|Le tapis sent un peu la laine.",
            "narrateur|Un grain de sable brille près du genou.",
            "narrateur|Sur le rebord, le soleil réchauffe une boîte.",
            "narrateur|Dedans, un peu de sable a voyagé.",
            "narrateur|La maîtresse ouvre la boîte.",
            "narrateur|Un grain tombe sur la table.",
            "narrateur|Elle montre une coquille.",
            "narrateur|La coquille est crème, avec des lignes.",
            "maitresse|On écoute d'abord.",
            "maitresse|Qui veut parler de la coquille ?",
            "narrateur|Nino a une idée.",
            "narrateur|La mer est peut-être dedans.",
            "narrateur|Il a envie de la poser contre l'oreille.",
            "enfant-m|Je veux parler de la mer.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nino veut parler.",
            "narrateur|Que fait-il d'abord ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino lève la main.",
            "narrateur|Sa main reste en l'air, bien droite.",
            "narrateur|Il faut attendre.",
            "narrateur|Il attend.",
            "narrateur|Quelqu'un parle d'abord.",
            "narrateur|On entend : la coquille est blanche.",
            "narrateur|Nino attend encore.",
            "narrateur|Il regarde le grain de sable.",
            "maitresse|Nino, c'est toi.",
            "narrateur|Nino parle, tout près de la coquille.",
            "enfant-m|La coquille est lisse.",
            "enfant-m|La mer est peut-être dedans.",
            "maitresse|Merci, Nino.",
            "maitresse|Tu as attendu.",
            "maitresse|Puis tu as parlé.",
            "maitresse|Tu veux l'écouter ?",
            "enfant-m|Oui.",
            "narrateur|Nino pose la coquille contre son oreille.",
            "narrateur|Elle est un peu froide, très lisse.",
            "narrateur|Un hush arrive, tout doux.",
            "enfant-m|Je l'entends.",
            "maitresse|La mer est restée dedans.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nino range son cartable.",
            "narrateur|Maman l'attend près de la porte.",
            "maman|Tu mets ton manteau ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le manteau sent encore le vent.",
            "narrateur|Une manche est un peu froide.",
            "papa|Le galet t'attend à la maison.",
            "papa|Tu le touches ce soir ?",
            "enfant-m|Oui, papa.",
            "enfant-m|La coquille a fait hush.",
            "maman|Tu as attendu, puis tu as écouté.",
            "narrateur|Les grains de sable brillent encore.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai entendu la mer.",
            "enfant-m|J'ai levé la main.",
            "enfant-m|J'ai attendu.",
            "enfant-m|Puis j'ai parlé.",
            "maman|Bravo, Nino.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "radiateur,boite", "CHK_T0000_P0000_END": "cartable,porte"},
    {
        "expected_answer": "attendre",
        "accepted_examples": "attendre | il attend | lever la main | la main",
        "retry_prompt": "Il lève la main et il attend. Que fait Nino ?",
    },
    NEED_002,
)


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.002-03 N3 Mila — chat du carton de lait
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.002-03",
    "De la farine reste sur la table. Mila veut dire que le chat de la classe ressemble au chat du carton. Elle attend son tour à l'école, puis encore à table.",
    "Le chat du carton",
    "Mila, papa, maman, maîtresse",
    "cuisine, classe, puis table",
    {
        "CHK_T0000_P0000": [
            "narrateur|De la farine reste sur la table en bois.",
            "narrateur|Elle fait un nuage quand maman souffle.",
            "narrateur|Un carton de lait a un chat gris.",
            "narrateur|Le chat a des moustaches trop longues.",
            "narrateur|Dans la rue, une sonnette de vélo tinte.",
            "papa|À ce soir, Mila.",
            "papa|Tu attends ton tour, d'accord ?",
            "enfant-f|D'accord, papa.",
            "enfant-f|Le chat du carton est gris.",
            "enfant-f|Je veux le dire à l'école.",
            "maman|Ta main est toute petite dans la mienne.",
            "maman|Tu vas t'asseoir sur le tapis ?",
            "enfant-f|Oui, maman.",
            "narrateur|En ce moment, Mila arrive en classe.",
            "maman|Au revoir, Mila.",
            "maman|Bonne journée.",
            "enfant-f|Au revoir, maman.",
            "narrateur|Mila s'assoit sur le tapis.",
            "narrateur|Le tapis a des pois verts.",
            "narrateur|Un pois est un peu défait.",
            "narrateur|La maîtresse montre une image.",
            "narrateur|C'est un chat gris.",
            "narrateur|Les moustaches sont trop longues.",
            "maitresse|On écoute d'abord l'image.",
            "maitresse|Qui veut parler du chat ?",
            "narrateur|Mila a une idée.",
            "narrateur|C'est le même chat que le carton.",
            "narrateur|Les mots lui chatouillent la bouche.",
            "enfant-f|Je veux parler du chat du lait.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila veut parler.",
            "narrateur|Que fait-elle d'abord ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila lève la main.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Il faut attendre.",
            "narrateur|Elle attend.",
            "narrateur|Quelqu'un parle d'abord.",
            "narrateur|On entend parler des moustaches.",
            "narrateur|Mila attend encore.",
            "maitresse|Mila, c'est ton tour.",
            "narrateur|Mila parle.",
            "enfant-f|Le chat est gris.",
            "enfant-f|Comme le chat du carton, à la maison.",
            "maitresse|Merci, Mila.",
            "maitresse|Tu as attendu.",
            "maitresse|Puis tu as parlé.",
            "narrateur|Le soir, les assiettes sont chaudes.",
            "narrateur|Ça sent le gratin.",
            "narrateur|La nappe a des petits carreaux.",
            "papa|Alors, Mila ?",
            "narrateur|Mila se souvient.",
            "narrateur|Elle lève la main, même à table.",
            "narrateur|Papa écoute maman d'abord.",
            "maman|Le gratin est prêt.",
            "narrateur|Mila attend.",
            "narrateur|Elle pose l'autre main sur la nappe.",
            "papa|Mila, c'est toi.",
            "enfant-f|Le chat de l'école est le même.",
            "enfant-f|Il est sur le carton.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman tourne le carton de lait.",
            "narrateur|Le chat gris les regarde.",
            "enfant-f|C'est lui.",
            "maman|Tu as fini de ranger le cartable ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le cartable sent encore la farine du matin.",
            "papa|On se dit bonne nuit dans un moment ?",
            "enfant-f|Oui, papa.",
            "maman|Tu as attendu à l'école, et à table.",
            "narrateur|Les pois verts restent dans sa tête.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Le chat était sur le carton.",
            "enfant-f|J'ai levé la main.",
            "enfant-f|J'ai attendu.",
            "enfant-f|Puis j'ai parlé.",
            "papa|Bravo, Mila.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "farine,porte", "CHK_T0000_P0000_C0001": "table"},
    {
        "expected_answer": "attendre",
        "accepted_examples": "attendre | elle attend | lever la main | la main",
        "retry_prompt": "Elle lève la main et elle attend. Que fait Mila ?",
    },
    NEED_002,
)


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.002-04 N3 Nina — pomme de pin et hérisson
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.002-04",
    "Une pomme de pin roule dans la poche. Nina veut la montrer près du hérisson. Elle attend, elle parle, puis au goûter elle attend encore pour sa pomme verte.",
    "La pomme de pin de Nina",
    "Nina, papa, maman, maîtresse",
    "entrée, classe, goûter, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une pomme de pin roule dans la poche.",
            "narrateur|Elle chatouille les doigts, tout sec.",
            "narrateur|Un filet d'escargot brille sur le mur.",
            "narrateur|L'air sent la mousse froide.",
            "narrateur|Maman tient le cartable de Nina.",
            "maman|Le cartable est un peu humide, dehors.",
            "maman|Tu vas t'asseoir sur le tapis ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Je veux montrer la pomme de pin.",
            "enfant-f|Près du hérisson.",
            "papa|La pomme verte est pour le goûter.",
            "papa|Tu attends ton tour, d'accord ?",
            "enfant-f|D'accord, papa.",
            "narrateur|En ce moment, Nina entre dans la classe.",
            "maman|Au revoir, Nina.",
            "maman|Bonne journée.",
            "enfant-f|Au revoir, maman.",
            "narrateur|Nina s'assoit sur le tapis.",
            "narrateur|Le tapis est un peu froid, encore.",
            "narrateur|La pomme de pin reste dans la poche.",
            "narrateur|La maîtresse montre une affiche.",
            "narrateur|C'est un hérisson.",
            "narrateur|Les piquants sont dessinés au crayon brun.",
            "maitresse|On écoute d'abord l'affiche.",
            "maitresse|Qui veut parler du hérisson ?",
            "narrateur|Nina a une idée.",
            "narrateur|Les piquants ressemblent à la pomme de pin.",
            "narrateur|Elle a envie de le dire.",
            "enfant-f|Je veux parler des piquants.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nina veut parler.",
            "narrateur|Que fait-elle d'abord ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina lève la main.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Il faut attendre.",
            "narrateur|Elle attend.",
            "narrateur|Quelqu'un parle d'abord.",
            "narrateur|Nina attend encore.",
            "maitresse|Nina, c'est ton tour.",
            "narrateur|Nina parle.",
            "enfant-f|Le hérisson a des piquants.",
            "enfant-f|Comme ma pomme de pin.",
            "narrateur|Elle la pose près de l'affiche.",
            "narrateur|Les piquants et les écailles se regardent.",
            "maitresse|Merci, Nina.",
            "maitresse|Tu as attendu.",
            "maitresse|Puis tu as parlé.",
            "narrateur|Plus tard, c'est le goûter.",
            "narrateur|Les boîtes s'ouvrent.",
            "narrateur|Ça sent la pomme.",
            "narrateur|La pomme de Nina est verte, un peu brillante.",
            "narrateur|Nina a envie de raconter son goûter.",
            "narrateur|Elle lève la main.",
            "narrateur|Elle attend.",
            "narrateur|Quelqu'un parle.",
            "maitresse|Nina.",
            "enfant-f|J'ai une pomme verte.",
            "maitresse|Merci.",
            "maitresse|Sur le tapis, puis au goûter, c'est pareil.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Le soir, maman demande près de la porte.",
            "maman|Alors, Nina ?",
            "enfant-f|J'ai montré la pomme de pin.",
            "enfant-f|J'ai attendu.",
            "enfant-f|Puis j'ai parlé.",
            "papa|On la pose sur le rebord ?",
            "enfant-f|Oui, papa.",
            "narrateur|La pomme de pin s'assoit près de la vitre.",
            "maman|Tu as attendu au goûter aussi ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina met son manteau.",
            "narrateur|Le manteau sent encore la mousse.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|La pomme de pin attend sur le rebord.",
            "enfant-f|J'ai levé la main.",
            "enfant-f|J'ai attendu.",
            "enfant-f|Puis j'ai parlé.",
            "maman|Bravo, Nina.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "poche,porte", "CHK_T0000_P0000_C0001": "boite,pomme"},
    {
        "expected_answer": "attendre",
        "accepted_examples": "attendre | elle attend | lever la main | la main",
        "retry_prompt": "Elle lève la main et elle attend. Que fait Nina ?",
    },
    NEED_002,
)


# ---------------------------------------------------------------------------
# ATOM-COL.ECO.002-05 N1 Aniss — pompon et ballon
# ---------------------------------------------------------------------------
write_story(
    "ATOM-COL.ECO.002-05",
    "Un pompon rouge rebondit sur la fermeture. Aniss veut dire que le ballon est rouge comme le pompon. Il attend, il le dit, puis il fait bouger le ballon.",
    "Le pompon d'Aniss",
    "Aniss, papa, maman, maîtresse",
    "entrée, classe, puis maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un pompon rouge rebondit sur la fermeture.",
            "narrateur|Il est en laine, un peu rêche.",
            "narrateur|La cuisine sent le lait chaud.",
            "narrateur|Une tasse laisse un rond sur la table.",
            "narrateur|Un doudou attend sur une chaise.",
            "narrateur|Le doudou a une oreille un peu pliée.",
            "narrateur|Papa tient la main d'Aniss.",
            "papa|Ta main est bien dans la mienne.",
            "papa|Tu vas t'asseoir, Aniss ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Je veux parler du rouge.",
            "maman|Le doudou t'attend ce soir.",
            "maman|Tu attends ton tour, d'accord ?",
            "enfant-m|D'accord, maman.",
            "narrateur|En ce moment, Aniss arrive.",
            "papa|Au revoir, Aniss.",
            "papa|Bonne journée.",
            "enfant-m|Au revoir, papa.",
            "narrateur|Aniss s'assoit sur le tapis.",
            "narrateur|Le tapis est doux.",
            "narrateur|Le pompon reste sur le manteau.",
            "narrateur|Ça sent les crayons.",
            "narrateur|Une chaise grince tout bas.",
            "narrateur|Un cube rouge est près du genou.",
            "narrateur|Aniss le pousse un peu, tout doux.",
            "narrateur|La maîtresse montre un ballon.",
            "narrateur|Le ballon est rouge.",
            "narrateur|Il est un peu lisse, un peu chaud.",
            "narrateur|Il sent le caoutchouc.",
            "maitresse|Qui veut parler du ballon ?",
            "narrateur|Aniss a une idée.",
            "narrateur|Le ballon est rouge, comme le pompon.",
            "narrateur|Les mots lui chatouillent la bouche.",
            "enfant-m|Je veux parler du rouge.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss veut parler.",
            "narrateur|Que fait-il d'abord ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Aniss lève la main.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Il faut attendre.",
            "narrateur|Il attend.",
            "narrateur|Quelqu'un parle d'abord.",
            "narrateur|Aniss attend encore.",
            "maitresse|Aniss, c'est toi.",
            "narrateur|Aniss parle.",
            "enfant-m|Le ballon est rouge.",
            "enfant-m|Comme mon pompon.",
            "maitresse|Merci, Aniss.",
            "maitresse|Tu as attendu.",
            "maitresse|Puis tu as parlé.",
            "maitresse|Tu veux le faire bouger ?",
            "enfant-m|Oui.",
            "narrateur|Aniss tapote le ballon.",
            "narrateur|Le ballon tremble, tout doux.",
            "narrateur|Il revient, tout lent.",
            "enfant-m|Il danse.",
            "maitresse|Il est rouge, comme tu as dit.",
            "narrateur|Le pompon, sur le manteau, reste sage.",
            "narrateur|Aniss tapote encore une fois.",
            "narrateur|Le ballon fait un petit floup.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Aniss range son cartable.",
            "narrateur|Papa l'attend à la porte.",
            "papa|Tu mets ton manteau ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le pompon rebondit encore.",
            "narrateur|Le couloir est long, tout calme.",
            "maman|Le doudou est dans le sac.",
            "maman|Tu le prends ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le doudou sent la maison.",
            "papa|Alors, Aniss ?",
            "enfant-m|Le ballon a dansé.",
            "enfant-m|J'ai attendu.",
            "maman|Tu as levé la main ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le lait chaud n'est plus là.",
            "narrateur|Le rond de la tasse reste.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Le pompon est revenu.",
            "enfant-m|J'ai levé la main.",
            "enfant-m|J'ai attendu.",
            "enfant-m|Puis j'ai parlé.",
            "papa|Bravo, Aniss.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "pompon,porte", "CHK_T0000_P0000_END": "cartable,porte"},
    {
        "expected_answer": "attendre",
        "accepted_examples": "attendre | il attend | lever la main | la main",
        "retry_prompt": "Il lève la main et il attend. Que fait Aniss ?",
    },
    NEED_002,
)

print("écrit 8 merged.json")
