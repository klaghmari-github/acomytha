#!/usr/bin/env python3
"""F-NAR-009 — merged.json pour 8 atomiques SEC.RUE.001."""
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
    "course sur",
    "courir sur",
    "sur la chaussée",
    "dans la rue tout seul",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom ", "léa", "lea ", "lina", "iris",
    "aïcha", "aicha", "clément", "clement", "léonie", "leonie",
    "clarisse", "éléonore", "eleonore", "dominique",
)
NEED = ("trottoir", "s'arrêter", "pieds au bord")


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
    if "bravo" not in aj and "bon travail" not in aj:
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
    check(sid, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# 01 N1 Amir, papa, marché — oranges, gouttière, flaque
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-01",
    "Une caisse d'oranges sent le soleil. Amir et papa vont au marché. Au bord, Amir s'arrête. Pieds au bord, sur le trottoir. Ils attendent. Puis le pain tiède.",
    "Les oranges d'Amir",
    "Amir, papa",
    "maison puis trottoir vers le marché, après la pluie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une caisse d'oranges sent le soleil.",
            "narrateur|Les oranges sont rondes et brillantes.",
            "narrateur|Dehors, une gouttière fait tic tic.",
            "narrateur|Le paillasson est encore un peu mouillé.",
            "narrateur|Les chaussures de papa sentent le cuir.",
            "narrateur|Un sac en toile pend au crochet.",
            "narrateur|La maison sent le café tiède.",
            "narrateur|Amir vit ici, avec papa.",
            "enfant-m|Papa, ça sent les oranges !",
            "papa|Oui.",
            "papa|Le marché est ouvert.",
            "papa|Tu mets tes chaussures ?",
            "narrateur|En ce moment, Amir s'assoit.",
            "narrateur|Il enfile la chaussure gauche.",
            "narrateur|Puis la chaussure droite.",
            "narrateur|Les lacets font un petit bruit.",
            "papa|Tu as fini tes chaussures ?",
            "enfant-m|Oui, papa.",
            "papa|Bravo.",
            "papa|On prend le sac.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air sent le pain chaud.",
            "narrateur|Une flaque brille sur le trottoir.",
            "enfant-m|Elle brille !",
            "papa|Oui.",
            "papa|On marche sur le trottoir.",
            "narrateur|Amir donne la main à papa.",
            "narrateur|Ils marchent tout doucement.",
            "narrateur|Le sac tape contre la jambe.",
            "narrateur|Un oiseau crie sur un toit.",
            "narrateur|L'eau de la gouttière chante encore.",
            "enfant-m|J'entends le marché !",
            "papa|Bientôt.",
            "papa|On reste sur le trottoir.",
            "narrateur|Les oranges sont plus près.",
            "narrateur|Le bord du trottoir arrive.",
            "narrateur|Le bord est gris et net.",
            "papa|On va s'arrêter.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "narrateur|Amir s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-m|Je m'arrête.",
            "papa|Oui.",
            "papa|On attend avec papa.",
            "papa|Tes pieds sont calmes ?",
            "enfant-m|Oui.",
            "narrateur|Une voiture passe au loin.",
            "narrateur|Amir serre la main de papa.",
            "narrateur|Il sent le pain encore plus fort.",
            "papa|Bravo, Amir.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Amir arrive au bord.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "papa|Tu t'arrêtes au trottoir ?",
            "enfant-m|Oui.",
            "enfant-m|Je m'arrête.",
            "papa|Bravo, Amir.",
            "papa|On attend avec papa.",
            "narrateur|La main de papa est chaude.",
            "narrateur|Le sac de toile est lisse.",
            "narrateur|La flaque brille encore.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Papa serre doucement la main.",
            "papa|On y va ensemble ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils marchent avec l'adulte.",
            "narrateur|Le marché sent le beurre.",
            "narrateur|Une orange brille dans une caisse.",
            "papa|Tu prends le pain ?",
            "narrateur|Amir tient le pain tiède.",
            "enfant-m|Il est chaud !",
            "papa|Oui.",
            "papa|Tu as fini de le tenir ?",
            "enfant-m|Oui.",
            "papa|Bravo.",
            "narrateur|Le sac devient tout rond.",
            "narrateur|Les oranges sentent encore le soleil.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Je me suis arrêté.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "papa|Bravo, Amir.",
            "narrateur|Le pain sent encore le four.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "voiture_passe"},
)


# ---------------------------------------------------------------------------
# 02 N3 Sarah, maman, boulangerie puis jardin — buée, sac jaune, deux bords
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-02",
    "La vitre est buée. Sarah et maman vont chercher le pain. Au premier bord, Sarah s'arrête. Pieds au bord. Plus tard, vers le jardin, elle s'arrête encore. Le sac est tiède.",
    "Le pain tiède de Sarah",
    "Sarah, maman",
    "cuisine embuée, trottoir vers la boulangerie, puis vers le jardin public",
    {
        "CHK_T0000_P0000": [
            "narrateur|La vitre de la cuisine est toute buée.",
            "narrateur|Un petit doigt y dessine un rond.",
            "narrateur|Dehors, le village sent le beurre chaud.",
            "narrateur|Un sac jaune attend sur la chaise.",
            "narrateur|Le tissu du sac est un peu rêche.",
            "narrateur|Les chaussettes de Sarah sèchent près du radiateur.",
            "narrateur|Elles sont épaisses, toutes chaudes.",
            "narrateur|Sarah vit ici, avec maman.",
            "enfant-f|Maman, la vitre est toute douce !",
            "maman|Oui.",
            "maman|Le four de la boulangerie est allumé.",
            "maman|Tu mets tes chaussettes chaudes ?",
            "narrateur|En ce moment, Sarah s'assoit près du radiateur.",
            "narrateur|Elle enfile les chaussettes épaisses.",
            "narrateur|Puis les petites chaussures brunes.",
            "maman|Tu as fini tes chaussures ?",
            "enfant-f|Oui, maman.",
            "maman|Bravo.",
            "maman|On prend le sac jaune.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|L'air sent le beurre et le pain.",
            "narrateur|Une feuille colle au bas de la porte.",
            "enfant-f|Ça sent trop bon !",
            "maman|Oui.",
            "maman|On marche sur le trottoir.",
            "narrateur|Sarah donne la main à maman.",
            "narrateur|Le sac jaune tape doucement contre la jambe.",
            "narrateur|Elles passent devant une fenêtre orange.",
            "narrateur|Le pain est tout proche maintenant.",
            "narrateur|Le bord du trottoir arrive, gris et net.",
            "maman|On va s'arrêter.",
            "maman|Pieds au bord.",
            "maman|Sur le trottoir.",
            "narrateur|Sarah s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-f|Je m'arrête.",
            "maman|Oui.",
            "maman|On attend avec maman.",
            "maman|Tes pieds sont calmes ?",
            "enfant-f|Oui.",
            "narrateur|Le vent touche les joues de Sarah.",
            "narrateur|Le beurre sent encore plus fort.",
            "maman|Bravo, Sarah.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah arrive au bord.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "maman|Tu t'arrêtes au trottoir ?",
            "enfant-f|Oui.",
            "enfant-f|Je m'arrête.",
            "maman|Bravo, Sarah.",
            "maman|On attend avec maman.",
            "narrateur|La main de maman est chaude.",
            "narrateur|Le sac jaune est un peu rêche.",
            "narrateur|Le vent glisse encore sur les joues.",
        ],
        "CHK_T0000_P0000_END": [
            "maman|On y va ensemble ?",
            "enfant-f|Oui, maman.",
            "narrateur|Elles marchent avec l'adulte.",
            "narrateur|La clochette de la boulangerie fait ding.",
            "narrateur|Le pain est tiède dans le sac jaune.",
            "enfant-f|Il est chaud !",
            "maman|Oui.",
            "maman|On va au jardin, maintenant.",
            "narrateur|Plus loin, un autre bord arrive.",
            "narrateur|Sarah se souvient du premier bord.",
            "enfant-f|On va s'arrêter ?",
            "maman|Oui.",
            "maman|Pieds au bord.",
            "maman|Sur le trottoir.",
            "narrateur|Sarah s'arrête encore.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "maman|Tu as repris le même arrêt ?",
            "enfant-f|Oui.",
            "maman|Bravo.",
            "maman|Même règle, autre chemin.",
            "narrateur|Le sac tiède pèse un peu.",
            "narrateur|Le jardin sent l'herbe coupée.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Je me suis arrêtée deux fois.",
            "maman|Pieds au bord.",
            "maman|Sur le trottoir.",
            "maman|Bravo, Sarah.",
            "narrateur|Le pain tiède reste dans le sac jaune.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "", "CHK_T0000_P0000_END": ""},
)


# ---------------------------------------------------------------------------
# 03 N2 Mila, papa, école — cartable bleu, boucle, carré de lumière
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-03",
    "Le cartable bleu pend au crochet. Mila et papa vont à l'école. Au bord, Mila s'arrête. Pieds au bord, sur le trottoir. Parce qu'elle s'arrête, elle attend avec papa.",
    "Le cartable bleu de Mila",
    "Mila, papa",
    "entrée de la maison, trottoir vers l'école",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le cartable bleu pend au crochet.",
            "narrateur|La boucle métallique fait un petit clic.",
            "narrateur|Un carré de lumière pose sur le plancher.",
            "narrateur|Il est jaune, un peu poussiéreux.",
            "narrateur|Les chaussures de Mila attendent près du tapis.",
            "narrateur|Le tapis est rêche sous les orteils.",
            "narrateur|Dehors, un merle chante sur le mur.",
            "narrateur|Mila vit ici, avec papa.",
            "enfant-f|Papa, le cartable brille !",
            "papa|Oui.",
            "papa|On va à l'école.",
            "papa|Tu mets tes chaussures ?",
            "narrateur|En ce moment, Mila s'accroupit.",
            "narrateur|Elle enfile la chaussure gauche.",
            "narrateur|Puis la chaussure droite.",
            "papa|Tu as fini tes chaussures ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|On met le cartable.",
            "narrateur|Papa aide pour la sangle.",
            "narrateur|La sangle est lisse et froide.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air sent le pain de la rue.",
            "enfant-f|Ça sent bon !",
            "papa|Oui.",
            "papa|On marche sur le trottoir.",
            "narrateur|Mila donne la main à papa.",
            "narrateur|Le cartable tape doucement dans le dos.",
            "narrateur|Le merle chante encore, plus loin.",
            "narrateur|Les pierres du trottoir sont un peu froides.",
            "enfant-f|L'école est près ?",
            "papa|Bientôt.",
            "papa|On reste sur le trottoir.",
            "narrateur|Le bord du trottoir arrive.",
            "narrateur|Le bord est gris, bien droit.",
            "papa|On va s'arrêter.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "narrateur|Mila s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-f|Je m'arrête.",
            "papa|Oui.",
            "papa|On attend avec papa.",
            "papa|Tes pieds sont calmes ?",
            "enfant-f|Oui.",
            "narrateur|Parce qu'elle s'arrête, elle attend.",
            "narrateur|Une voiture passe au loin.",
            "narrateur|Mila serre la main de papa.",
            "papa|Bravo, Mila.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila arrive au bord.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "papa|Tu t'arrêtes au trottoir ?",
            "enfant-f|Oui.",
            "enfant-f|Je m'arrête.",
            "papa|Bravo, Mila.",
            "papa|On attend avec papa.",
            "narrateur|Parce que les pieds restent au bord, Mila attend.",
            "narrateur|La sangle du cartable est froide.",
            "narrateur|La main de papa est chaude.",
        ],
        "CHK_T0000_P0000_END": [
            "papa|On y va ensemble ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils marchent avec l'adulte.",
            "narrateur|Le portail de l'école est bleu.",
            "narrateur|Il sent le métal froid.",
            "papa|Tu donnes le cartable ?",
            "narrateur|Mila pousse la sangle.",
            "enfant-f|Il est prêt.",
            "papa|Tu as fini ?",
            "enfant-f|Oui.",
            "papa|Bravo.",
            "narrateur|Le merle chante encore sur le mur.",
            "narrateur|Le carré de lumière reste loin, à la maison.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Je me suis arrêtée.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "papa|Bravo, Mila.",
            "narrateur|Le cartable bleu tape encore un peu.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "voiture_passe"},
)


# ---------------------------------------------------------------------------
# 04 N1 Nino, maman, parc — feuille jaune, bottes rouges, balle
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-04",
    "Une feuille jaune colle à la vitre. Nino et maman vont au parc. La balle est dans le sac. Au bord, Nino s'arrête. Pieds au bord, sur le trottoir.",
    "Les bottes rouges de Nino",
    "Nino, maman",
    "fenêtre, entrée, trottoir vers le parc",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une feuille jaune colle à la vitre.",
            "narrateur|Elle est un peu froissée, toute sèche.",
            "narrateur|Le vent la fait trembler.",
            "narrateur|Les bottes rouges attendent près de la porte.",
            "narrateur|Elles brillent, encore un peu humides.",
            "narrateur|Un sac souple tient une balle bleue.",
            "narrateur|La balle sent le caoutchouc.",
            "narrateur|Nino vit ici, avec maman.",
            "enfant-m|Maman, la feuille tremble !",
            "maman|Oui.",
            "maman|Le vent est doux.",
            "maman|Tu mets tes bottes ?",
            "narrateur|En ce moment, Nino s'assoit.",
            "narrateur|Il enfile la botte gauche.",
            "narrateur|Puis la botte droite.",
            "narrateur|Le caoutchouc fait un petit ploc.",
            "maman|Tu as fini tes bottes ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "maman|On prend la balle.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|L'air sent les feuilles mouillées.",
            "enfant-m|Ça sent le parc !",
            "maman|Oui.",
            "maman|On marche sur le trottoir.",
            "narrateur|Nino donne la main à maman.",
            "narrateur|Les bottes tapent un rythme doux.",
            "narrateur|Une feuille sèche crisse sous une botte.",
            "narrateur|Le sac souple tape contre la jambe.",
            "enfant-m|La balle est dedans ?",
            "maman|Oui.",
            "maman|On reste sur le trottoir.",
            "narrateur|Les arbres du parc sont plus près.",
            "narrateur|Le bord du trottoir arrive.",
            "narrateur|Le bord est gris et net.",
            "maman|On va s'arrêter.",
            "maman|Pieds au bord.",
            "maman|Sur le trottoir.",
            "narrateur|Nino s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-m|Je m'arrête.",
            "maman|Oui.",
            "maman|On attend avec maman.",
            "maman|Tes pieds sont calmes ?",
            "enfant-m|Oui.",
            "narrateur|Le vent touche les joues de Nino.",
            "narrateur|Les bottes rouges restent bien posées.",
            "maman|Bravo, Nino.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nino arrive au bord.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "maman|Tu t'arrêtes au trottoir ?",
            "enfant-m|Oui.",
            "enfant-m|Je m'arrête.",
            "maman|Bravo, Nino.",
            "maman|On attend avec maman.",
            "narrateur|La main de maman est chaude.",
            "narrateur|Les bottes rouges sont un peu froides.",
            "narrateur|Le vent bouge encore la feuille.",
        ],
        "CHK_T0000_P0000_END": [
            "maman|On y va ensemble ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils marchent avec l'adulte.",
            "narrateur|Le parc sent l'herbe.",
            "narrateur|La balle bleue sort du sac.",
            "maman|Tu la lances ?",
            "narrateur|Nino lance la balle.",
            "narrateur|Elle fait un petit ploc.",
            "enfant-m|Elle rebondit !",
            "maman|Oui.",
            "maman|Tu as fini de lancer ?",
            "enfant-m|Oui.",
            "maman|Bravo.",
            "narrateur|Les bottes rouges brillent dans l'herbe.",
            "narrateur|Une feuille jaune vole encore.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Je me suis arrêté.",
            "maman|Pieds au bord.",
            "maman|Sur le trottoir.",
            "maman|Bravo, Nino.",
            "narrateur|La balle bleue dort dans l'herbe.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "enfants_parc", "CHK_T0000_P0000_END": "enfants_parc"},
)


# ---------------------------------------------------------------------------
# 05 N1 Nina, papa, boulangerie — farine, cuillère en bois, clochette
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-05",
    "Un nuage de farine dort sur la table. Nina et papa vont à la boulangerie. Au bord, Nina s'arrête. Pieds au bord, sur le trottoir. Le pain est tiède.",
    "La farine de Nina",
    "Nina, papa",
    "cuisine farinée, trottoir vers la boulangerie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un nuage de farine dort sur la table.",
            "narrateur|Il est blanc, tout doux sous le doigt.",
            "narrateur|Une cuillère en bois sent la pâte.",
            "narrateur|Le bol est encore un peu collant.",
            "narrateur|Les chaussons de Nina attendent sous la chaise.",
            "narrateur|Un manteau rouge pend au crochet.",
            "narrateur|La cuisine sent le lait tiède.",
            "narrateur|Nina vit ici, avec papa.",
            "enfant-f|Papa, c'est tout blanc !",
            "papa|Oui.",
            "papa|C'est de la farine.",
            "papa|On va chercher le pain ?",
            "enfant-f|Oui !",
            "papa|Tu mets tes chaussures ?",
            "narrateur|En ce moment, Nina s'assoit.",
            "narrateur|Elle pose les chaussons sous la chaise.",
            "narrateur|Elle enfile les chaussures brunes.",
            "papa|Tu as fini tes chaussures ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|On prend le manteau rouge.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air sent le four de la rue.",
            "enfant-f|Ça sent le pain !",
            "papa|Oui.",
            "papa|On marche sur le trottoir.",
            "narrateur|Nina donne la main à papa.",
            "narrateur|Le manteau rouge est un peu rêche.",
            "narrateur|Une clochette sonne, tout au loin.",
            "narrateur|Ding, tout doux.",
            "enfant-f|J'entends la clochette !",
            "papa|Bientôt.",
            "papa|On reste sur le trottoir.",
            "narrateur|Le bord du trottoir arrive.",
            "narrateur|Le bord est gris et net.",
            "papa|On va s'arrêter.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "narrateur|Nina s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-f|Je m'arrête.",
            "papa|Oui.",
            "papa|On attend avec papa.",
            "papa|Tes pieds sont calmes ?",
            "enfant-f|Oui.",
            "narrateur|Le pain sent encore plus fort.",
            "narrateur|Nina serre la main de papa.",
            "papa|Bravo, Nina.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nina arrive au bord.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "papa|Tu t'arrêtes au trottoir ?",
            "enfant-f|Oui.",
            "enfant-f|Je m'arrête.",
            "papa|Bravo, Nina.",
            "papa|On attend avec papa.",
            "narrateur|La main de papa est chaude.",
            "narrateur|Le manteau rouge gratte un peu.",
            "narrateur|La clochette sonne encore, loin.",
        ],
        "CHK_T0000_P0000_END": [
            "papa|On y va ensemble ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils marchent avec l'adulte.",
            "narrateur|La clochette fait ding, tout près.",
            "narrateur|Le pain est chaud dans le sac.",
            "papa|Tu le touches ?",
            "narrateur|Nina pose la main.",
            "enfant-f|Il est tiède !",
            "papa|Oui.",
            "papa|Tu as fini de le toucher ?",
            "enfant-f|Oui.",
            "papa|Bravo.",
            "narrateur|Le sac sent le beurre.",
            "narrateur|Un peu de farine reste à la maison.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Je me suis arrêtée.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "papa|Bravo, Nina.",
            "narrateur|Le pain tiède reste dans le sac.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": ""},
)


# ---------------------------------------------------------------------------
# 06 N1 Chouchou, maman, square — grain de sable, doudou, balançoire
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-06",
    "Un grain de sable brille dans la chaussure. Chouchou et maman vont au square. Le doudou vient aussi. Au bord, Chouchou s'arrête. Pieds au bord, sur le trottoir.",
    "Le grain de sable de Chouchou",
    "Chouchou, maman",
    "entrée, chaussure sablée, trottoir vers le square",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un grain de sable brille dans la chaussure.",
            "narrateur|Il est tout petit, un peu doré.",
            "narrateur|Le doudou gris attend sur le banc de l'entrée.",
            "narrateur|Il sent encore le lit.",
            "narrateur|Une cordelette pend de sa couture.",
            "narrateur|Dehors, une balançoire grince, loin.",
            "narrateur|Le paillasson est rêche et beige.",
            "narrateur|Chouchou vit ici, avec maman.",
            "enfant-m|Maman, y a du sable !",
            "maman|Oui.",
            "maman|C'est le square d'hier.",
            "maman|Tu mets tes chaussures ?",
            "narrateur|En ce moment, Chouchou s'assoit.",
            "narrateur|Maman verse le grain tout doux.",
            "narrateur|Il tombe sur le paillasson.",
            "narrateur|Chouchou enfile la chaussure gauche.",
            "narrateur|Puis la chaussure droite.",
            "maman|Tu as fini tes chaussures ?",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "maman|On prend le doudou.",
            "narrateur|Le doudou est chaud et mou.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|L'air sent le sable et l'herbe.",
            "enfant-m|J'entends la balançoire !",
            "maman|Oui.",
            "maman|On marche sur le trottoir.",
            "narrateur|Chouchou donne la main à maman.",
            "narrateur|Le doudou pend de l'autre main.",
            "narrateur|La cordelette chatouille les doigts.",
            "narrateur|La balançoire grince encore, plus près.",
            "maman|On reste sur le trottoir.",
            "narrateur|Le bord du trottoir arrive.",
            "narrateur|Le bord est gris et net.",
            "maman|On va s'arrêter.",
            "maman|Pieds au bord.",
            "maman|Sur le trottoir.",
            "narrateur|Chouchou s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-m|Je m'arrête.",
            "maman|Oui.",
            "maman|On attend avec maman.",
            "maman|Tes pieds sont calmes ?",
            "enfant-m|Oui.",
            "narrateur|Le doudou reste contre le ventre.",
            "narrateur|Chouchou serre la main de maman.",
            "maman|Bravo, Chouchou.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Chouchou arrive au bord.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Chouchou s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "maman|Tu t'arrêtes au trottoir ?",
            "enfant-m|Oui.",
            "enfant-m|Je m'arrête.",
            "maman|Bravo, Chouchou.",
            "maman|On attend avec maman.",
            "narrateur|La main de maman est chaude.",
            "narrateur|Le doudou sent encore le lit.",
            "narrateur|La balançoire grince tout doux.",
        ],
        "CHK_T0000_P0000_END": [
            "maman|On y va ensemble ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils marchent avec l'adulte.",
            "narrateur|Le square sent le sable chaud.",
            "narrateur|Le seau rouge attend dans le bac.",
            "maman|Tu poses le doudou ?",
            "narrateur|Chouchou le pose sur le banc.",
            "enfant-m|Il attend.",
            "maman|Oui.",
            "maman|Tu as fini de le poser ?",
            "enfant-m|Oui.",
            "maman|Bravo.",
            "narrateur|Le grain doré brille encore au soleil.",
            "narrateur|La balançoire grince, tout près.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Je me suis arrêté.",
            "maman|Pieds au bord.",
            "maman|Sur le trottoir.",
            "maman|Bravo, Chouchou.",
            "narrateur|Le doudou reste au soleil, sur le banc.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "enfants_parc", "CHK_T0000_P0000_END": "enfants_parc"},
)


# ---------------------------------------------------------------------------
# 07 N1 Victorina, papa, marché — caisses, tomate, soleil sur les tuiles
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-07",
    "Les caisses du marché claquent au loin. Victorina et papa prennent le panier rouge. Au bord, Victorina s'arrête. Pieds au bord, sur le trottoir. La tomate est ronde.",
    "Le panier rouge de Victorina",
    "Victorina, papa",
    "maison ensoleillée, trottoir vers le marché",
    {
        "CHK_T0000_P0000": [
            "narrateur|Les caisses du marché claquent au loin.",
            "narrateur|Clac, clac, tout doux.",
            "narrateur|Le soleil tape sur les tuiles.",
            "narrateur|Les tuiles sont chaudes, presque rouges.",
            "narrateur|Une tomate roule un peu sur la table.",
            "narrateur|Elle est ronde, un peu luisante.",
            "narrateur|Le panier rouge attend près de la porte.",
            "narrateur|L'anse est lisse, un peu usée.",
            "narrateur|Victorina vit ici, avec papa.",
            "enfant-f|Papa, la tomate roule !",
            "papa|Oui.",
            "papa|On va en chercher d'autres.",
            "papa|Tu mets tes sandales ?",
            "narrateur|En ce moment, Victorina s'assoit.",
            "narrateur|Elle enfile la sandale gauche.",
            "narrateur|Puis la sandale droite.",
            "narrateur|La boucle fait un petit clic.",
            "papa|Tu as fini tes sandales ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|On prend le panier rouge.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air sent la tomate et le soleil.",
            "enfant-f|Ça sent le marché !",
            "papa|Oui.",
            "papa|On marche sur le trottoir.",
            "narrateur|Victorina donne la main à papa.",
            "narrateur|Le panier tape un rythme léger.",
            "narrateur|Les caisses claquent encore, plus près.",
            "narrateur|Le soleil chauffe les cheveux.",
            "enfant-f|J'entends les caisses !",
            "papa|Bientôt.",
            "papa|On reste sur le trottoir.",
            "narrateur|Le bord du trottoir arrive.",
            "narrateur|Le bord est gris et net.",
            "papa|On va s'arrêter.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "narrateur|Victorina s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-f|Je m'arrête.",
            "papa|Oui.",
            "papa|On attend avec papa.",
            "papa|Tes pieds sont calmes ?",
            "enfant-f|Oui.",
            "narrateur|Le panier rouge reste contre la jambe.",
            "narrateur|Victorina serre la main de papa.",
            "papa|Bravo, Victorina.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina arrive au bord.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorina s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "papa|Tu t'arrêtes au trottoir ?",
            "enfant-f|Oui.",
            "enfant-f|Je m'arrête.",
            "papa|Bravo, Victorina.",
            "papa|On attend avec papa.",
            "narrateur|La main de papa est chaude.",
            "narrateur|L'anse du panier est lisse.",
            "narrateur|Les caisses claquent encore, loin.",
        ],
        "CHK_T0000_P0000_END": [
            "papa|On y va ensemble ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils marchent avec l'adulte.",
            "narrateur|Le marché sent la tomate mûre.",
            "narrateur|Une caisse rouge est pleine.",
            "papa|Tu poses une tomate ?",
            "narrateur|Victorina la pose dans le panier.",
            "enfant-f|Elle est ronde !",
            "papa|Oui.",
            "papa|Tu as fini de la poser ?",
            "enfant-f|Oui.",
            "papa|Bravo.",
            "narrateur|Le panier devient un peu lourd.",
            "narrateur|Le soleil reste sur les tuiles.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Je me suis arrêtée.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "papa|Bravo, Victorina.",
            "narrateur|La tomate roule un peu dans le panier.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": ""},
)


# ---------------------------------------------------------------------------
# 08 N1 Raphaël, papa, parc — tilleuls, abeille, ombre de la grille
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.RUE.001-08",
    "Les tilleuls sentent le miel tiède. Raphaël et papa vont au parc. Le doudou est dans la poche. Au bord, Raphaël s'arrête. Pieds au bord, sur le trottoir.",
    "Les tilleuls de Raphaël",
    "Raphaël, papa",
    "jardin de devant, trottoir vers le parc aux tilleuls",
    {
        "CHK_T0000_P0000": [
            "narrateur|Les tilleuls sentent le miel tiède.",
            "narrateur|Une abeille passe, tout près des fleurs.",
            "narrateur|Elle fait un petit bzz.",
            "narrateur|L'ombre de la grille raye le chemin.",
            "narrateur|Les rayures sont longues, un peu bleues.",
            "narrateur|Un doudou bleu dort dans la poche.",
            "narrateur|La poche est chaude, un peu rêche.",
            "narrateur|Raphaël vit ici, avec papa.",
            "enfant-m|Papa, ça sent le miel !",
            "papa|Oui.",
            "papa|Les tilleuls sont en fleurs.",
            "papa|On va au parc ?",
            "enfant-m|Oui !",
            "papa|Tu mets tes chaussures ?",
            "narrateur|En ce moment, Raphaël s'accroupit.",
            "narrateur|Il enfile la chaussure gauche.",
            "narrateur|Puis la chaussure droite.",
            "papa|Tu as fini tes chaussures ?",
            "enfant-m|Oui, papa.",
            "papa|Bravo.",
            "papa|Le doudou reste dans la poche ?",
            "enfant-m|Oui.",
            "narrateur|Papa ouvre le petit portillon.",
            "narrateur|L'air sent le miel et l'herbe.",
            "enfant-m|Bzz, l'abeille !",
            "papa|Elle butine.",
            "papa|On marche sur le trottoir.",
            "narrateur|Raphaël donne la main à papa.",
            "narrateur|Les rayures d'ombre glissent sur les pieds.",
            "narrateur|Les tilleuls sont plus près.",
            "narrateur|Le doudou fait un petit paquet chaud.",
            "papa|On reste sur le trottoir.",
            "narrateur|Le bord du trottoir arrive.",
            "narrateur|Le bord est gris et net.",
            "papa|On va s'arrêter.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "narrateur|Raphaël s'arrête.",
            "narrateur|Ses pieds sont au bord.",
            "narrateur|Les pieds restent au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "enfant-m|Je m'arrête.",
            "papa|Oui.",
            "papa|On attend avec papa.",
            "papa|Tes pieds sont calmes ?",
            "enfant-m|Oui.",
            "narrateur|Le miel sent encore plus fort.",
            "narrateur|Raphaël serre la main de papa.",
            "papa|Bravo, Raphaël.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Les pieds restent au bord du trottoir.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Raphaël arrive au bord.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Raphaël s'arrête au bord.",
            "narrateur|Les pieds sont sur le trottoir.",
            "narrateur|Les pieds restent au bord.",
            "papa|Tu t'arrêtes au trottoir ?",
            "enfant-m|Oui.",
            "enfant-m|Je m'arrête.",
            "papa|Bravo, Raphaël.",
            "papa|On attend avec papa.",
            "narrateur|La main de papa est chaude.",
            "narrateur|Le doudou reste dans la poche.",
            "narrateur|L'abeille fait encore bzz, loin.",
        ],
        "CHK_T0000_P0000_END": [
            "papa|On y va ensemble ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils marchent avec l'adulte.",
            "narrateur|Le parc sent le miel et l'herbe.",
            "narrateur|Un banc est à l'ombre.",
            "papa|Tu sors le doudou ?",
            "narrateur|Raphaël le pose sur le banc.",
            "enfant-m|Il a de l'ombre.",
            "papa|Oui.",
            "papa|Tu as fini de le poser ?",
            "enfant-m|Oui.",
            "papa|Bravo.",
            "narrateur|Les tilleuls bougent un peu.",
            "narrateur|L'ombre de la grille reste derrière eux.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Je me suis arrêté.",
            "papa|Pieds au bord.",
            "papa|Sur le trottoir.",
            "papa|Bravo, Raphaël.",
            "narrateur|Le doudou bleu dort à l'ombre.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "enfants_parc", "CHK_T0000_P0000_END": "enfants_parc"},
)
