#!/usr/bin/env python3
"""F-NAR-009 — merged.json pour ATOM-AUT.AFF.002-01..07 et 003-01."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 16}
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
    "aujourd'hui ",
)
BAD_NAMES = (
    "nora", "kenzo", "sara ", "violette", "damien", "brice", "florian",
    "sami", "tom ", "léa", "lea ", "lina", "iris", "lucas", "céline",
    "celine", "constentin", "luca",
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


def piper_scale(lines: list[str]) -> float:
    first = lines[0].split("|", 1)[0]
    if first.startswith("enfant"):
        return 1.28
    return 1.22


def make_chunk(src: dict, lines: list[str], sons, extra: dict | None = None) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["length_scale_piper"] = piper_scale(lines)
    age = extra.get("age") if extra else None
    kind = src.get("kind") or ""
    if kind == "passage_question" or (age == "N1"):
        nc["rate_label"] = "slow"
    else:
        nc["rate_label"] = src.get("rate_label") or "medium"
    if extra:
        for k, v in extra.items():
            if k != "age":
                nc[k] = v
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
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie." not in low:
        raise SystemExit(f"{sid}: manque fin")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in ("joue au salon", "est dans l'entrée", "c'est le matin"):
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 400:
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


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    extras: dict | None = None,
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra_ids}")
    extras = extras or {}
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        extra = dict(extras.get(cid) or {})
        extra["age"] = src.get("age_band")
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), extra)
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
    relecture = folder / "RELECTURE.md"
    relecture.write_text(
        f"# F-NAR-009 — {sid}\n\n"
        f"**Titre :** {title}\n\n"
        f"**Fil rouge :** {fil}\n\n"
        f"Relu : P0000, question, confirmation, fin. `chunk_id` / `kind` inchangés.\n\n"
        f"## Vu\n\n"
        f"- Monde d'abord, désir, imprévu, résolution, fin vécue.\n"
        f"- Leçon greffée (manteau / affaires), pas un cours.\n"
        f"- Troupe D16. Papa/maman parlent. POS-001. Une félicitation, pas un refrain.\n"
        f"- `length_scale_piper` : narrateur 1.22, enfant 1.28.\n\n"
        f"## Non vérifié\n\n"
        f"- Audio (pas cuit). Durée réelle à l'écoute.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# 002-01 N1 Victorino, maman — feuille rouge, jardin
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.002-01",
    "Victorino veut la feuille rouge collée à la vitre, pour le bol blanc. Une manche du manteau est à l'envers. Maman tourne le tissu. Ils ramassent la feuille. Le manteau rentre au crochet. La feuille brille dans le bol.",
    "La feuille rouge de Victorino",
    "Victorino, maman",
    "maison et jardin, vitre mouillée",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une goutte glisse sur la vitre.",
            "narrateur|Elle laisse un trait brillant.",
            "narrateur|Une feuille rouge est collée.",
            "narrateur|On dirait une petite étoile.",
            "narrateur|La cuisine sent le pain tiède.",
            "narrateur|Maman essuie la table en bois.",
            "narrateur|Un bol blanc attend au milieu.",
            "narrateur|La lumière est jaune et douce.",
            "narrateur|Victorino vit ici, avec maman.",
            "enfant-m|Maman, la feuille est rouge !",
            "maman|Oui.",
            "maman|Elle est collée à la vitre.",
            "narrateur|En ce moment, Victorino s'approche.",
            "narrateur|Il pose le doigt sur le verre.",
            "narrateur|Le verre est un peu froid.",
            "enfant-m|Je la veux pour le bol.",
            "maman|On peut aller la chercher.",
            "maman|Elle est tombée dans le jardin.",
            "narrateur|Victorino court vers la porte.",
            "narrateur|Le manteau rouge attend au crochet.",
            "narrateur|Le crochet est bas, à sa hauteur.",
            "narrateur|Il tire le manteau vers lui.",
            "narrateur|Une manche est à l'envers.",
            "narrateur|Son bras ne passe pas.",
            "enfant-m|Oh.",
            "enfant-m|Je n'y arrive pas.",
            "maman|Attends.",
            "maman|On tourne la manche.",
            "narrateur|Maman tourne le tissu tout doux.",
            "narrateur|Le rouge est chaud comme une pomme.",
            "maman|Glisse un bras.",
            "narrateur|Victorino glisse un bras.",
            "maman|Maintenant l'autre.",
            "narrateur|Victorino glisse l'autre bras.",
            "enfant-m|Il est chaud.",
            "maman|Oui.",
            "maman|Il te tiendra chaud dehors.",
            "maman|On ouvre la porte ?",
            "enfant-m|Oui.",
            "enfant-m|On va chercher la feuille.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|L'air sent la terre mouillée.",
            "narrateur|Le jardin est pâle et calme.",
            "narrateur|Victorino marche près de maman.",
            "narrateur|L'herbe est un peu froide.",
            "narrateur|La feuille rouge est dans l'herbe.",
            "enfant-m|Elle est là !",
            "maman|Tu la prends tout doux ?",
            "narrateur|Victorino ramasse la feuille.",
            "narrateur|Elle est lisse et un peu mouillée.",
            "narrateur|Il la glisse dans la poche.",
            "enfant-m|Elle est dans la poche.",
            "maman|Bien.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Oui.",
            "enfant-m|Dans les poches.",
            "narrateur|Un oiseau passe tout bas.",
            "maman|Tu as vu l'oiseau ?",
            "enfant-m|Oui.",
            "enfant-m|Il est parti.",
            "maman|C'est l'heure de rentrer.",
            "narrateur|Ils rentrent dans la maison.",
            "narrateur|La maison est tiède.",
            "narrateur|Victorino retire le manteau rouge.",
            "narrateur|Il le raccroche au crochet.",
            "narrateur|Le manteau est à sa place.",
            "enfant-m|Je sors la feuille.",
            "narrateur|Il prend la feuille dans la poche.",
            "narrateur|Il la pose dans le bol blanc.",
            "maman|Elle est belle, dans le bol.",
            "enfant-m|C'est ma feuille rouge.",
            "maman|Oui.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de sortir, que prend Victorino ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorino a pris le manteau rouge.",
            "narrateur|Il est allé au jardin.",
            "narrateur|Il a ramassé la feuille.",
            "narrateur|En rentrant, il a raccroché.",
            "narrateur|La feuille est dans le bol.",
            "maman|Tu as pris le manteau pour sortir.",
            "enfant-m|Il est au crochet, maman.",
            "maman|Oui.",
            "maman|Il attend pour la prochaine fois.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Victorino pose les chaussures.",
            "narrateur|Elles restent près de la porte.",
            "narrateur|Le bol blanc brille un peu.",
            "maman|Tu as les pieds au chaud ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le manteau rouge reste au crochet.",
            "narrateur|La vitre n'a plus de feuille.",
            "maman|On reste un peu à la maison ?",
            "enfant-m|Oui.",
            "enfant-m|Avec ma feuille.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai mis la feuille dans le bol.",
            "enfant-m|J'avais le manteau.",
            "maman|Bravo, Victorino.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Le bol blanc brille encore.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Il prend le manteau. Que prend Victorino ?",
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | son manteau",
        }
    },
)


# ---------------------------------------------------------------------------
# 002-02 N3 Chouchou (enfant-f), maman — pommes du marché
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.002-02",
    "Chouchou veut quatre pommes pour le saladier. Le panier coince la capuche du manteau bleu. Elle pose le panier, enfile le manteau, choisit les pommes. Une pomme roule. Elle la rattrape. Le manteau rentre au crochet. Les pommes brillent.",
    "Les pommes de Chouchou",
    "Chouchou, maman",
    "entrée, marché, cuisine",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le panier d'osier attend près des bottes.",
            "narrateur|Une liste dépasse du bord.",
            "narrateur|Le papier est un peu froissé.",
            "narrateur|Une pièce tinte dans la poche de maman.",
            "narrateur|De la rue, une clochette de vélo passe.",
            "narrateur|Ça sent la pierre encore humide.",
            "narrateur|Le marché n'est pas loin.",
            "maman|Chouchou, tu as vu le panier ?",
            "enfant-f|Oui.",
            "enfant-f|Il est près des bottes.",
            "narrateur|En ce moment, Chouchou lève le panier.",
            "narrateur|Son manteau bleu pend au crochet.",
            "narrateur|Le tissu a une petite capuche.",
            "narrateur|La capuche est coincée sous l'anse.",
            "narrateur|Le panier ne vient pas.",
            "enfant-f|Il tient, maman !",
            "maman|Pose le panier un moment.",
            "maman|On prend le manteau d'abord.",
            "narrateur|Chouchou pose le panier près des bottes.",
            "narrateur|Elle prend le manteau bleu.",
            "narrateur|Elle glisse un bras, puis l'autre.",
            "narrateur|La capuche tapote son dos.",
            "maman|Tu as les boutons ?",
            "enfant-f|Un, deux, trois.",
            "maman|Parfait.",
            "maman|Maintenant le panier.",
            "enfant-f|On va chercher des pommes ?",
            "maman|Oui.",
            "maman|Quatre, pour le saladier.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|Le vent est frais.",
            "narrateur|Il sent un peu le pain.",
            "narrateur|Ils marchent vers le marché.",
            "narrateur|Chouchou tient une anse du panier.",
            "maman|Tu as chaud dans le manteau ?",
            "enfant-f|Oui.",
            "enfant-f|J'ai chaud dedans.",
            "narrateur|Au marché, les étals sont colorés.",
            "narrateur|Les pommes brillent.",
            "narrateur|Une pomme est rouge.",
            "narrateur|Une autre est jaune.",
            "maman|On en prend quatre ?",
            "enfant-f|Quatre pommes.",
            "narrateur|Maman pose trois pommes dans le panier.",
            "narrateur|La quatrième pomme jaune roule.",
            "narrateur|Elle part vers le bord de l'étal.",
            "enfant-f|Elle part !",
            "maman|Tu peux la rattraper ?",
            "narrateur|Chouchou avance la main.",
            "narrateur|La pomme est lisse et froide.",
            "narrateur|Elle la pose dans le panier.",
            "enfant-f|Je l'ai !",
            "maman|Merci.",
            "narrateur|Le panier devient un peu lourd.",
            "narrateur|Chouchou sent le sucré des fruits.",
            "maman|C'est l'heure de rentrer.",
            "enfant-f|Oui.",
            "enfant-f|On rentre.",
            "narrateur|Ils rentrent.",
            "narrateur|L'entrée est calme.",
            "narrateur|Chouchou retire le manteau bleu.",
            "narrateur|Elle le raccroche au crochet.",
            "narrateur|Le crochet fait un petit clic.",
            "narrateur|Le manteau est à sa place.",
            "narrateur|Elle pose le panier près des bottes.",
            "narrateur|Les pommes tapotent le fond.",
            "maman|Tu as fini de poser le panier ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Les pommes sont dedans.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de sortir, que prend Chouchou ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Chouchou a pris le manteau bleu.",
            "narrateur|Elle l'a mis pour le marché.",
            "narrateur|Elle a rattrapé la pomme jaune.",
            "narrateur|En rentrant, elle a raccroché.",
            "maman|Tu as pris le manteau pour sortir.",
            "enfant-f|Il attend près des bottes.",
            "maman|Oui.",
            "maman|Près du panier.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman pose les pommes sur la table.",
            "narrateur|Elles roulent un tout petit peu.",
            "enfant-f|Elles sentent le marché.",
            "maman|Tu veux les ranger dans le saladier ?",
            "narrateur|Chouchou les pose une par une.",
            "narrateur|Le saladier devient coloré.",
            "narrateur|Chouchou touche le manteau au crochet.",
            "narrateur|Le tissu est encore un peu frais.",
            "maman|Les pommes sont prêtes.",
            "enfant-f|Moi aussi.",
            "maman|Oui.",
            "maman|Toi aussi.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|J'ai mis les pommes dans le saladier.",
            "enfant-f|J'avais le manteau pour le marché.",
            "maman|Bravo, Chouchou.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Les pommes brillent dans le saladier.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "clochette,porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Elle prend le manteau. Que prend Chouchou ?",
            "expected_answer": "le manteau",
            "accepted_examples": "le manteau | manteau | son manteau",
        }
    },
)


# ---------------------------------------------------------------------------
# 002-03 N2 Sarah, papa — pain doré de la vitrine
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.002-03",
    "Sarah veut voir le pain doré derrière la vitrine. Les clés tintent. Une manche du manteau jaune est tordue. Papa l'aide. Ils voient le pigeon et le pain. Le foulard et le manteau rentrent à leur place.",
    "Le pain doré de Sarah",
    "Sarah, papa",
    "hall, rue, vitrine de la boulangerie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Les clés de papa pendent à un clou.",
            "narrateur|Elles font une petite chanson.",
            "narrateur|Un foulard dort sur la rampe.",
            "narrateur|Il est rayé, bleu et blanc.",
            "narrateur|Sous la porte, un filet d'air froid.",
            "narrateur|La rue sent déjà le pain.",
            "papa|Sarah, tu as entendu les clés ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Elles tintent.",
            "narrateur|En ce moment, Sarah écoute les clés.",
            "narrateur|Son manteau jaune attend au crochet.",
            "narrateur|Le tissu est doux comme une couverture.",
            "enfant-f|On va voir le pain, papa ?",
            "papa|Oui.",
            "papa|On va marcher jusqu'à la vitrine.",
            "narrateur|Papa prend les clés.",
            "narrateur|Sarah avance vers la porte.",
            "narrateur|Papa tend le manteau jaune.",
            "narrateur|Une manche est un peu tordue.",
            "narrateur|Le bras de Sarah ne glisse pas.",
            "enfant-f|Ça coince.",
            "papa|Attends.",
            "papa|Je tiens la manche ouverte.",
            "narrateur|Sarah enfile une manche.",
            "narrateur|Puis l'autre manche.",
            "narrateur|Le tissu est doux sur ses bras.",
            "papa|Tu veux le foulard aussi ?",
            "enfant-f|Oui.",
            "enfant-f|Il est rayé.",
            "narrateur|Papa noue le foulard tout doux.",
            "papa|On peut sortir.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air de la rue est frais.",
            "narrateur|Ça sent le pain chaud.",
            "narrateur|Ils marchent près.",
            "narrateur|Sarah tient la main de papa.",
            "enfant-f|J'ai chaud dans le manteau.",
            "papa|Oui.",
            "papa|Parce que tu l'as pris.",
            "narrateur|Ils marchent encore un peu.",
            "narrateur|Un pigeon picore près du trottoir.",
            "papa|Tu as vu le pigeon ?",
            "enfant-f|Oui.",
            "enfant-f|Il picore.",
            "narrateur|Une vitrine brille.",
            "narrateur|Le pain est derrière la vitre.",
            "papa|Tu as vu le pain ?",
            "enfant-f|Il est doré.",
            "papa|On le regarde un moment ?",
            "enfant-f|Oui.",
            "narrateur|Sarah pose le front près de la vitre.",
            "narrateur|La vitre est un peu froide.",
            "narrateur|Le pain brille comme le soleil.",
            "papa|C'est l'heure de rentrer.",
            "narrateur|Ils rentrent.",
            "narrateur|Le hall est calme.",
            "narrateur|Sarah retire le manteau jaune.",
            "narrateur|Elle le raccroche au crochet.",
            "narrateur|Le crochet fait un petit bruit.",
            "narrateur|Elle pose le foulard sur la rampe.",
            "papa|Tu as fini de poser le foulard ?",
            "enfant-f|Oui.",
            "enfant-f|Sur la rampe.",
            "enfant-f|Le manteau est au crochet.",
            "papa|Oui.",
            "papa|Tu as su.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah va dehors.",
            "narrateur|Que prend-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah a pris le manteau jaune.",
            "narrateur|Elle l'a mis pour la rue.",
            "narrateur|Elle a vu le pain doré.",
            "narrateur|En rentrant, elle a raccroché.",
            "papa|Tu as pris le manteau pour sortir.",
            "enfant-f|Il est à sa place.",
            "papa|Oui.",
            "papa|Avec le foulard sur la rampe.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sarah pose ses chaussures.",
            "narrateur|Elles restent près du paillasson.",
            "papa|Tu as fini de poser tes chaussures ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa ferme la porte.",
            "narrateur|Le filet d'air s'arrête.",
            "narrateur|Les clés redeviennent silencieuses.",
            "papa|On reste au chaud, maintenant.",
            "enfant-f|Le pain était doré.",
            "papa|Oui.",
            "papa|Et le manteau attend au crochet.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|J'ai vu le pain doré.",
            "enfant-f|J'avais le manteau pour la rue.",
            "papa|Bravo, Sarah.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Le pain sent encore sous la porte.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cles,porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Avant de sortir, que prend Sarah ?",
            "expected_answer": "le manteau",
            "accepted_examples": "le manteau | manteau | elle l'enfile",
        }
    },
)


# ---------------------------------------------------------------------------
# 002-04 N3 Amir, papa — jardin puis carottes
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.002-04",
    "Amir veut des carottes orange pour la soupe. D'abord le jardin : le tuyau est froid, une feuille lisse. Le manteau vert va au crochet. Plus tard le sac cache le crochet. Amir le déplace, reprend le manteau. Au marché les carottes. Deux sorties, le même manteau.",
    "Les carottes d'Amir",
    "Amir, papa",
    "cuisine, jardin, marché",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une cuillère en bois sèche près de l'évier.",
            "narrateur|La soupe sent encore dans la cuisine.",
            "narrateur|La vitre a un peu de buée.",
            "narrateur|Dehors, le tuyau d'arrosage est enroulé.",
            "narrateur|Papa plie un sac de toile.",
            "papa|Amir, tu as vu la buée ?",
            "enfant-m|Oui.",
            "enfant-m|On dirait un nuage.",
            "narrateur|En ce moment, Amir essuie un peu la buée.",
            "narrateur|Son manteau vert attend au crochet.",
            "papa|On va d'abord au jardin.",
            "papa|Le tuyau a peut-être de l'eau.",
            "papa|Avant de sortir, on prend le manteau.",
            "narrateur|Amir prend le manteau vert.",
            "narrateur|Il est un peu épais.",
            "narrateur|Amir glisse un bras, puis l'autre.",
            "papa|Tu es prêt ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa lace les chaussures d'Amir.",
            "narrateur|Ils vont au jardin.",
            "narrateur|L'air est frais.",
            "narrateur|Amir touche une feuille lisse.",
            "enfant-m|Elle sent le jardin.",
            "papa|Oui.",
            "papa|Un peu l'herbe.",
            "papa|Un peu l'eau.",
            "narrateur|Le tuyau d'arrosage est froid.",
            "narrateur|Amir le touche du doigt.",
            "enfant-m|Il est froid !",
            "papa|Oui.",
            "papa|C'est l'heure de rentrer.",
            "narrateur|Amir entre.",
            "narrateur|Il retire le manteau.",
            "narrateur|Il le raccroche au crochet.",
            "narrateur|Le manteau vert est à sa place.",
            "narrateur|Plus tard, le sac de toile attend.",
            "papa|On va au marché, maintenant.",
            "papa|Pour les carottes de la soupe.",
            "narrateur|Amir se souvient.",
            "narrateur|Il va vers le crochet.",
            "narrateur|Le sac de toile cache le manteau.",
            "enfant-m|Je ne vois plus le manteau.",
            "papa|Le sac est devant.",
            "papa|Tu peux le déplacer ?",
            "narrateur|Amir pousse le sac tout doux.",
            "narrateur|Le manteau vert réapparaît.",
            "narrateur|Avant de sortir, il le prend.",
            "narrateur|Le même manteau vert.",
            "papa|Tu t'es souvenu tout seul.",
            "narrateur|Au marché, ça sent le pain.",
            "narrateur|Papa achète une botte de carottes.",
            "enfant-m|Elles sont orange.",
            "papa|Oui.",
            "papa|On les met dans le sac.",
            "narrateur|Puis ils rentrent.",
            "narrateur|Amir raccroche encore le manteau.",
            "narrateur|Le crochet fait le même petit bruit.",
            "enfant-m|Deux fois, papa.",
            "papa|Oui.",
            "papa|Deux fois.",
            "narrateur|Amir pose le sac de toile.",
            "narrateur|Les carottes font un petit bruit.",
            "papa|Tu as fini de poser le sac ?",
            "enfant-m|Oui, papa.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de sortir, que prend Amir ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir a pris le manteau.",
            "narrateur|Au jardin, puis au marché.",
            "narrateur|Deux sorties.",
            "narrateur|Le même manteau vert.",
            "narrateur|En rentrant, il l'a raccroché.",
            "papa|Tu t'es souvenu.",
            "enfant-m|Il est au crochet.",
            "papa|Oui.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Amir pose les chaussures.",
            "narrateur|Le manteau reste au crochet.",
            "narrateur|Papa pose les carottes près de l'évier.",
            "papa|Tu as fini de poser tes chaussures ?",
            "enfant-m|Oui, papa.",
            "narrateur|La cuillère en bois est sèche.",
            "narrateur|La buée a disparu de la vitre.",
            "papa|On a les carottes pour la soupe.",
            "enfant-m|Le manteau aussi a travaillé.",
            "papa|Oui.",
            "papa|Le manteau aussi.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai pris le manteau deux fois.",
            "enfant-m|Jardin, puis marché.",
            "papa|Et tu l'as raccroché.",
            "papa|Bravo, Amir.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Les carottes attendent près de l'évier.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "evier,porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Il prend le manteau. Que prend Amir ?",
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | son manteau",
        }
    },
)


# ---------------------------------------------------------------------------
# 002-05 N2 Nina, papa — sonnette argentée, square
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.002-05",
    "Nina veut faire ding au square avec la trottinette. Le guidon heurte le manteau bleu au crochet. Elle range la trottinette, enfile le manteau, sonne au square, rentre, raccroche.",
    "La sonnette argentée de Nina",
    "Nina, papa",
    "entrée puis square",
    {
        "CHK_T0000_P0000": [
            "narrateur|La trottinette s'appuie au mur.",
            "narrateur|Sa sonnette est argentée.",
            "narrateur|Une bande de soleil coupe les carreaux.",
            "narrateur|Les chaussures de papa font une paire.",
            "narrateur|Le square est juste en bas de la rue.",
            "papa|Nina, tu as vu la sonnette ?",
            "enfant-f|Elle brille, papa.",
            "narrateur|En ce moment, Nina touche le guidon.",
            "narrateur|La sonnette est froide.",
            "narrateur|Son manteau bleu attend au crochet.",
            "enfant-f|On va au square ?",
            "papa|Oui.",
            "papa|Avec la trottinette.",
            "narrateur|Nina fait rouler la trottinette.",
            "narrateur|Les roues font un bruit léger.",
            "narrateur|Le guidon heurte le crochet.",
            "narrateur|Le manteau bleu se balance.",
            "enfant-f|Oh.",
            "enfant-f|Le manteau a bougé.",
            "papa|Pose la trottinette un moment.",
            "papa|On prend le manteau d'abord.",
            "narrateur|Nina pose la trottinette contre le mur.",
            "narrateur|Elle prend son manteau bleu.",
            "narrateur|Elle passe les manches.",
            "narrateur|Le tissu est doux.",
            "papa|Tu as le manteau ?",
            "enfant-f|Oui.",
            "papa|On ouvre la porte ?",
            "enfant-f|Oui.",
            "enfant-f|Doucement.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air est frais.",
            "narrateur|Ils sortent.",
            "narrateur|Au square, Nina pousse la trottinette.",
            "narrateur|Les roues chantent un peu.",
            "narrateur|La sonnette fait ding, une fois.",
            "enfant-f|Ding !",
            "papa|Tu as le manteau bien mis ?",
            "enfant-f|Oui.",
            "enfant-f|J'ai chaud.",
            "narrateur|Un banc est vide.",
            "narrateur|Nina s'arrête un moment.",
            "narrateur|Elle pose un pied par terre.",
            "narrateur|Les feuilles du square sont sèches.",
            "narrateur|Elles craquent sous la roue.",
            "papa|Tu as entendu les feuilles ?",
            "enfant-f|Oui.",
            "enfant-f|Ça fait chh.",
            "papa|Encore un ding ?",
            "narrateur|Nina touche la sonnette.",
            "narrateur|Ça fait ding encore.",
            "papa|C'est l'heure de rentrer.",
            "enfant-f|Oui.",
            "enfant-f|On rentre.",
            "narrateur|Ils rentrent.",
            "narrateur|Nina raccroche le manteau au crochet.",
            "narrateur|Le crochet est bas.",
            "narrateur|Elle pose la trottinette contre le mur.",
            "narrateur|Nina essuie un peu le guidon.",
            "narrateur|La sonnette est froide sous le doigt.",
            "papa|Tu as fini de poser la trottinette ?",
            "enfant-f|Oui.",
            "enfant-f|Contre le mur.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de sortir, que prend Nina ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina a pris le manteau bleu.",
            "narrateur|Elle l'a mis pour le square.",
            "narrateur|Elle a poussé la trottinette.",
            "narrateur|La sonnette a fait ding.",
            "narrateur|En rentrant, elle a raccroché.",
            "papa|Tu as pris le manteau pour sortir.",
            "enfant-f|Il est à sa place.",
            "papa|Oui.",
            "papa|Près de la trottinette.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nina pose ses chaussures.",
            "narrateur|Papa ferme la porte.",
            "narrateur|La bande de soleil a bougé.",
            "papa|Tu as fini de poser tes chaussures ?",
            "enfant-f|Oui, papa.",
            "narrateur|La sonnette est silencieuse.",
            "narrateur|Le manteau bleu reste au crochet.",
            "papa|On reste un peu à la maison.",
            "enfant-f|La trottinette attend.",
            "papa|Oui.",
            "papa|Et le manteau aussi.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|J'ai fait ding au square.",
            "enfant-f|J'avais le manteau.",
            "papa|Bravo, Nina.",
            "papa|Tu as fait du bon travail.",
            "narrateur|La sonnette argentée attend contre le mur.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "sonnette,porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Avant de sortir, on prend le manteau. Que prend Nina ?",
            "expected_answer": "manteau",
            "accepted_examples": "manteau | son manteau | le manteau",
        }
    },
)


# ---------------------------------------------------------------------------
# 002-06 N3 Nino, maman — jardin puis pain
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.002-06",
    "Le sac à pain est vide. Nino veut un pain doré. D'abord un tour au jardin : oiseau, feuille froide. Le manteau gris au crochet. Le sac vide pendait sur le manteau. À la boulangerie il se souvient. Le pain rentre chaud.",
    "Le sac à pain de Nino",
    "Nino, maman",
    "cuisine, jardin, boulangerie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un sac à pain vide pend à une chaise.",
            "narrateur|Des miettes dorment sur la planche.",
            "narrateur|L'horloge de la cuisine avance doucement.",
            "narrateur|Une mouche marche sur la vitre.",
            "narrateur|Maman s'essuie les mains dans un torchon.",
            "maman|Nino, tu as vu le sac vide ?",
            "enfant-m|Oui.",
            "enfant-m|Il n'y a plus de pain.",
            "narrateur|En ce moment, Nino souffle sur les miettes.",
            "narrateur|Son manteau gris attend au crochet.",
            "maman|L'horloge dit qu'il est tôt.",
            "maman|On va d'abord au jardin.",
            "maman|On verra si l'oiseau est là.",
            "narrateur|Nino va vers le crochet.",
            "narrateur|Le sac vide pendait aussi au crochet.",
            "narrateur|Il cache un peu le manteau.",
            "enfant-m|Le sac est devant.",
            "maman|Enlève le sac d'abord.",
            "maman|Puis le manteau.",
            "narrateur|Nino pose le sac sur la chaise.",
            "narrateur|Il prend le manteau gris.",
            "narrateur|Il est un peu épais.",
            "narrateur|Nino glisse un bras, puis l'autre.",
            "maman|Tu as pris ton manteau ?",
            "enfant-m|Oui, maman.",
            "narrateur|Maman lace les chaussures.",
            "narrateur|Ils vont au jardin.",
            "narrateur|L'air est frais.",
            "narrateur|Nino touche une feuille lisse.",
            "enfant-m|Elle est froide, maman.",
            "maman|Oui.",
            "maman|L'air est frais.",
            "narrateur|Un oiseau picore près de la haie.",
            "narrateur|Nino l'écoute un moment.",
            "maman|Tu as vu l'oiseau ?",
            "enfant-m|Oui.",
            "enfant-m|Il picore.",
            "maman|C'est l'heure de rentrer.",
            "narrateur|Nino entre.",
            "narrateur|Il retire le manteau.",
            "narrateur|Il le raccroche au crochet.",
            "narrateur|Le manteau gris est à sa place.",
            "narrateur|Plus tard, maman prend le sac vide.",
            "maman|On va à la boulangerie.",
            "narrateur|Nino se souvient.",
            "narrateur|Avant de sortir, il prend le manteau.",
            "narrateur|Le même manteau gris.",
            "maman|Tu t'es souvenu tout seul.",
            "narrateur|À la boulangerie, ça sent le pain chaud.",
            "narrateur|La vitrine est un peu embuée.",
            "enfant-m|Le pain est doré.",
            "maman|Oui.",
            "maman|On en prend un.",
            "narrateur|Maman glisse le pain dans le sac.",
            "narrateur|Puis ils rentrent.",
            "narrateur|Nino raccroche encore le manteau.",
            "narrateur|Le crochet fait le même petit bruit.",
            "enfant-m|Deux fois, maman.",
            "maman|Oui.",
            "maman|Deux fois.",
            "narrateur|Nino pose le sac à pain sur la chaise.",
            "narrateur|Le pain est encore un peu chaud.",
            "maman|Tu as fini de poser le sac ?",
            "enfant-m|Oui, maman.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de sortir, que prend Nino ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino a pris le manteau.",
            "narrateur|Au jardin, puis à la boulangerie.",
            "narrateur|Deux sorties.",
            "narrateur|Le même manteau gris.",
            "narrateur|En rentrant, il l'a raccroché.",
            "maman|Tu t'es souvenu.",
            "enfant-m|Il est au crochet.",
            "maman|Oui.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nino pose les chaussures.",
            "narrateur|Le manteau reste au crochet.",
            "narrateur|Maman pose le pain sur la planche.",
            "maman|Tu as fini de poser tes chaussures ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le sac n'est plus vide.",
            "narrateur|Les miettes nouvelles sentent le chaud.",
            "maman|On a le pain, maintenant.",
            "enfant-m|Et le manteau est à sa place.",
            "maman|Oui.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai pris le manteau deux fois.",
            "enfant-m|Jardin, puis boulangerie.",
            "maman|Et tu l'as raccroché.",
            "maman|Bravo, Nino.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Le pain doré attend sur la planche.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "horloge,porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Il prend le manteau. Que prend Nino ?",
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | son manteau",
        }
    },
)


# ---------------------------------------------------------------------------
# 002-07 N2 Mila, papa — cacao puis pain
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.002-07",
    "Après le cacao, Mila veut le pain chaud de la boulangerie. Une moufle est coincée dans la manche du manteau vert. Elle la sort, enfile le manteau, sent le pain, raccroche.",
    "Le cacao et le pain de Mila",
    "Mila, papa",
    "cuisine, entrée, boulangerie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Deux tasses encore tièdes.",
            "narrateur|Un peu de cacao au fond.",
            "narrateur|La table sent le lait.",
            "narrateur|La veste de papa est sur le dossier.",
            "narrateur|Une moufle sèche sur le radiateur.",
            "papa|Mila, tu as fini ton cacao ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il était chaud.",
            "narrateur|En ce moment, Mila pose sa tasse.",
            "narrateur|Son manteau vert attend au crochet.",
            "enfant-f|On va chercher le pain ?",
            "papa|Oui.",
            "papa|À la boulangerie.",
            "narrateur|Mila va vers le crochet.",
            "narrateur|Elle prend le manteau vert.",
            "narrateur|Quelque chose est dans la manche.",
            "enfant-f|Il y a quelque chose !",
            "papa|Tu peux sortir ce qu'il y a ?",
            "narrateur|Mila tire tout doux.",
            "narrateur|C'est la moufle.",
            "narrateur|Elle est sèche, maintenant.",
            "enfant-f|C'est la moufle !",
            "papa|Elle était dans la manche.",
            "papa|Maintenant tu peux l'enfiler.",
            "narrateur|Mila passe les manches.",
            "narrateur|Le tissu est doux.",
            "papa|Tu veux la moufle ?",
            "enfant-f|Oui.",
            "enfant-f|Elle est sèche.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air est frais.",
            "narrateur|Ils sortent.",
            "narrateur|À la boulangerie, ça sent le pain chaud.",
            "narrateur|Mila tient la main de papa.",
            "enfant-f|J'ai chaud dans le manteau.",
            "papa|Oui.",
            "papa|Parce que tu l'as pris.",
            "narrateur|La cloche de la porte tinte.",
            "narrateur|Le pain brille derrière la vitre.",
            "papa|Tu as vu le pain ?",
            "enfant-f|Il est doré.",
            "narrateur|Papa prend le pain.",
            "narrateur|Il le glisse dans un sac.",
            "narrateur|Le sac est un peu chaud.",
            "papa|C'est l'heure de rentrer.",
            "enfant-f|Oui.",
            "enfant-f|On rentre.",
            "narrateur|Ils rentrent.",
            "narrateur|Mila raccroche le manteau au crochet.",
            "narrateur|Le crochet est bas.",
            "narrateur|Mila pose la moufle près du radiateur.",
            "narrateur|Elle est un peu froide, maintenant.",
            "papa|Tu as fini de poser la moufle ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Le manteau est au crochet.",
            "papa|Oui.",
            "papa|Tu as su.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de sortir, que prend Mila ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila a pris le manteau vert.",
            "narrateur|Elle l'a mis pour chercher le pain.",
            "narrateur|Dehors, elle a eu chaud.",
            "narrateur|En rentrant, elle l'a raccroché.",
            "papa|Tu as pris le manteau pour sortir.",
            "enfant-f|Il est à sa place.",
            "papa|Oui.",
            "papa|Près de la moufle.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Mila pose le pain sur la table.",
            "narrateur|Le sac est encore un peu chaud.",
            "narrateur|Papa ferme la porte.",
            "papa|Tu as fini de poser le pain ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les tasses sont froides, maintenant.",
            "narrateur|Le manteau vert reste au crochet.",
            "papa|On goûtera le pain tout à l'heure.",
            "enfant-f|Il sent bon.",
            "papa|Oui.",
            "papa|Il sent le chaud.",
            "narrateur|Mila pose une main sur le pain.",
            "narrateur|Le sac craque un peu.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|J'ai pris le manteau pour le pain.",
            "enfant-f|En rentrant, je l'ai raccroché.",
            "papa|Bravo, Mila.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Le cacao a laissé une petite odeur.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "tasses,porte",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Elle prend le manteau. Que prend Mila ?",
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | son manteau | elle prend le manteau",
        }
    },
)


# ---------------------------------------------------------------------------
# 003-01 N1 Raphaël, papa — seau jaune au parc
# ---------------------------------------------------------------------------
write_story(
    "ATOM-AUT.AFF.003-01",
    "Raphaël veut faire chanter le sable dans le seau jaune. L'heure arrive. Il prend le seau. Le doudou gris et le manteau bleu sont encore au banc. Il revient les chercher. Ils rentrent avec tout.",
    "Le seau jaune de Raphaël",
    "Raphaël, papa",
    "parc, bac à sable",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un oiseau saute sur la barrière.",
            "narrateur|Le sable du bac est frais.",
            "narrateur|Un seau jaune attend.",
            "narrateur|Un doudou gris est assis sur le banc.",
            "narrateur|L'ombre de papa est longue.",
            "papa|Raphaël, tu as vu l'oiseau ?",
            "enfant-m|Oui.",
            "enfant-m|Il saute.",
            "narrateur|En ce moment, Raphaël verse le sable.",
            "narrateur|Il est près de papa.",
            "narrateur|Il a un manteau bleu.",
            "narrateur|Le manteau est un peu ouvert.",
            "narrateur|Le sable glisse.",
            "narrateur|Ça fait chh.",
            "enfant-m|Ça fait chh, papa.",
            "papa|Oui.",
            "papa|Le sable chante.",
            "narrateur|Le seau se remplit.",
            "narrateur|Puis il se vide.",
            "narrateur|Le doudou reste sur le banc.",
            "narrateur|Papa s'assoit un moment.",
            "papa|Le sable est frais, hein ?",
            "enfant-m|Oui.",
            "enfant-m|Il est frais.",
            "narrateur|Raphaël verse encore un peu.",
            "narrateur|Ça fait encore chh.",
            "narrateur|Le seau est lisse sous ses mains.",
            "enfant-m|Il est jaune, papa.",
            "papa|Oui.",
            "papa|Tout jaune.",
            "papa|C'est l'heure.",
            "papa|On va rentrer à la maison.",
            "narrateur|Raphaël prend le seau jaune.",
            "narrateur|Il marche vers la barrière.",
            "narrateur|Le seau tapote contre sa jambe.",
            "papa|Attends, Raphaël.",
            "papa|On reprend tes affaires avant de partir.",
            "narrateur|Raphaël s'arrête.",
            "narrateur|Il regarde derrière lui.",
            "narrateur|Le banc n'est pas vide.",
            "papa|Tu cherches le manteau ?",
            "narrateur|Raphaël revient vers le banc.",
            "narrateur|Le manteau bleu est là.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai le manteau.",
            "papa|Bien.",
            "papa|Et le doudou ?",
            "narrateur|Raphaël cherche le doudou.",
            "narrateur|Le doudou gris est là.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai le doudou.",
            "papa|Tu as le seau aussi ?",
            "enfant-m|Oui.",
            "enfant-m|Le seau jaune.",
            "narrateur|Ses affaires sont avec lui.",
            "papa|On peut partir, maintenant.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|Raphaël tient le seau.",
            "narrateur|Le doudou est contre lui.",
            "narrateur|Le manteau est sur son bras.",
            "papa|Tu as tout, hein ?",
            "enfant-m|Oui.",
            "enfant-m|J'ai tout.",
            "narrateur|Le seau tapote contre sa jambe.",
            "narrateur|Le doudou sent encore le sable.",
            "papa|Le doudou vient avec nous ?",
            "enfant-m|Oui.",
            "enfant-m|Il vient.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Avant de partir, que fait Raphaël ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Raphaël a cherché.",
            "narrateur|Il a repris le seau.",
            "narrateur|Il a repris le manteau.",
            "narrateur|Il a repris le doudou.",
            "narrateur|C'était avant de partir.",
            "papa|Tu as repris tes affaires.",
            "papa|Avant de partir.",
            "enfant-m|J'ai tout, papa.",
            "papa|Oui.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Raphaël tient le seau.",
            "narrateur|Le doudou est contre lui.",
            "papa|Je marche à côté de toi.",
            "narrateur|Le sable reste au parc.",
            "papa|Tu as les affaires avec toi ?",
            "enfant-m|Oui, papa.",
            "narrateur|L'oiseau n'est plus sur la barrière.",
            "narrateur|Le banc est vide, maintenant.",
            "narrateur|Le sable reste dans le bac.",
            "papa|On rentre à la maison.",
            "enfant-m|Avec mes affaires.",
            "papa|Oui.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|J'ai repris mes affaires.",
            "enfant-m|Avant de partir.",
            "papa|Bravo, Raphaël.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Le seau jaune tapote tout doux.",
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
    {
        "CHK_T0000_P0000_Q0001": {
            "retry_prompt": "Il reprend ses affaires. Que fait Raphaël ?",
            "expected_answer": "reprendre",
            "accepted_examples": "reprendre | ses affaires | il reprend | avant de partir",
        }
    },
)

