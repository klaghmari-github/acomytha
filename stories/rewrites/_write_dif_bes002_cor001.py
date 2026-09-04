#!/usr/bin/env python3
"""F-NAR-008 — ATOM-DIF.BES.002-06/07 + ATOM-DIF.COR.001-01..06."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 18}
ROLES = {
    "narrateur",
    "papa",
    "maman",
    "enfant-m",
    "enfant-f",
    "copain",
    "copine",
}
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
    "chuchotement serre",
    "une étape après l'autre",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom ", "léa", "lea ", "lina", "iris",
    "aïcha", "aicha", "clément", "clement", "léonie", "leonie",
    "clarisse", "éléonore", "eleonore", "dominique", "zoé", "zoe",
    "adam", "ariane", "benoît", "benoit", "solal", "maëlys", "maelys",
    "amandine", "nora", "hugo", "sami", "kamil", "ava ", "achille",
    "diane", "titouan", "romane", "constentin", "constantin", "luca",
    "célène", "celine", "céline", "alice",
)
NEED = {
    "ATOM-DIF.BES.002-06": ("proposer", "accepter plusieurs réponses"),
    "ATOM-DIF.BES.002-07": ("proposer", "accepter plusieurs réponses"),
    "ATOM-DIF.COR.001-01": ("tailles différentes", "jouer ensemble"),
    "ATOM-DIF.COR.001-02": ("tailles différentes", "jouer ensemble"),
    "ATOM-DIF.COR.001-03": ("tailles différentes", "jouer ensemble"),
    "ATOM-DIF.COR.001-04": ("tailles différentes", "jouer ensemble"),
    "ATOM-DIF.COR.001-05": ("tailles différentes", "jouer ensemble"),
    "ATOM-DIF.COR.001-06": ("tailles différentes", "jouer ensemble"),
}


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


def scales(age: str, cid: str) -> tuple[float, str]:
    if "Q0001" in cid:
        if age == "N1":
            return 1.4, "slow"
        if age == "N2":
            return 1.3, "slow"
        return 1.24, "slow"
    if "F0001" in cid:
        return (1.28, "slow" if age == "N1" else "medium")
    if age == "N1":
        return 1.28, "slow"
    return 1.22, "medium"


def make_chunk(src: dict, lines: list[str], sons, age: str) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    sc, rate = scales(age, src["chunk_id"])
    nc["length_scale_piper"] = sc
    nc["rate_label"] = rate
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
    adults = [
        ln for ln in joined.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation")
    if aj.count("bravo") > 2:
        raise SystemExit(f"{sid}: bravo en refrain ({aj.count('bravo')})")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie." not in low:
        raise SystemExit(f"{sid}: manque fin")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in NEED[sid]:
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


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    q: dict | None = None,
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    by = {}
    age = src.get("age_band") or "N2"
    for c in src["chunks"]:
        cid = c["chunk_id"]
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), age)
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


# ---------------------------------------------------------------------------
# ATOM-DIF.BES.002-06 N2 — Aniss, bateaux de papier, cour après la pluie
# ---------------------------------------------------------------------------
S06 = {
    "CHK_T0000_P0000": [
        "narrateur|Le zinc de la gouttière sent le métal froid.",
        "narrateur|Une goutte tombe encore.",
        "narrateur|Elle fait un rond dans la flaque.",
        "narrateur|Les dalles de la cour sont sombres.",
        "narrateur|Un escargot avance sur une fissure.",
        "narrateur|Ça sent la pierre mouillée.",
        "narrateur|Maman pose un torchon sur le rebord.",
        "maman|Tu as vu l'escargot, Aniss ?",
        "enfant-m|Oui, maman.",
        "enfant-m|Il a une petite maison.",
        "maman|Oui.",
        "maman|On le laisse tout doux.",
        "narrateur|Deux bateaux de papier attendent.",
        "narrateur|Ils sont un peu froissés.",
        "narrateur|Papa les a pliés ce matin.",
        "papa|Ils peuvent flotter dans la flaque.",
        "enfant-m|Je veux les faire courir.",
        "maman|Le long des dalles ?",
        "enfant-m|Oui.",
        "narrateur|En ce moment, Aniss pose un bateau.",
        "narrateur|Le papier devient sombre.",
        "narrateur|Il boit un peu d'eau.",
        "enfant-m|Il part !",
        "maman|Tout doux.",
        "narrateur|Chouchou est sur la marche sèche.",
        "narrateur|Ses chaussettes restent au sec.",
        "narrateur|Aniss le voit.",
        "enfant-m|Tu viens ?",
        "enfant-m|On fait courir les bateaux.",
        "copain|Je regarde.",
        "narrateur|Aniss écoute.",
        "enfant-m|D'accord.",
        "maman|On peut proposer.",
        "maman|Tu as proposé, Aniss.",
        "narrateur|Aniss pousse le bateau du doigt.",
        "narrateur|Le bateau glisse entre deux dalles.",
        "narrateur|L'escargot s'écarte, tout lent.",
        "enfant-m|Il laisse passer !",
        "papa|Oui.",
        "narrateur|Une feuille collée barre le chemin.",
        "narrateur|Le bateau s'arrête.",
        "enfant-m|Il est coincé.",
        "maman|Tu peux le dégager.",
        "narrateur|Aniss cherche autour de la flaque.",
        "narrateur|Il regarde Chouchou.",
        "enfant-m|Tu m'aides ?",
        "copain|Plus tard.",
        "enfant-m|D'accord.",
        "papa|La feuille est juste devant.",
        "narrateur|Le zinc goutte encore une fois.",
        "narrateur|Le rond tremble, puis s'arrête.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Chouchou dit plus tard.",
        "narrateur|Que fait Aniss ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Aniss prend une petite brindille.",
        "narrateur|Elle est lisse, un peu mouillée.",
        "narrateur|Il pousse la feuille, tout doux.",
        "narrateur|Le bateau se dégage.",
        "enfant-m|Il repart !",
        "maman|Oui.",
        "maman|On peut accepter plusieurs réponses.",
        "narrateur|Chouchou reste sur la marche.",
        "narrateur|Il penche la tête.",
        "narrateur|Le deuxième bateau attend au sec.",
        "copain|Je mets une voile ?",
        "enfant-m|Si tu veux.",
        "narrateur|Chouchou pose une feuille sèche.",
        "narrateur|C'est une voile, sur le papier.",
        "narrateur|Il ne descend pas dans l'eau.",
        "maman|Tu as accepté, Aniss.",
        "narrateur|Les deux bateaux glissent.",
        "narrateur|Ils font deux ronds dans la flaque.",
        "enfant-m|Ils se croisent !",
        "papa|Ils arrivent au bout.",
        "narrateur|L'escargot a fini sa fissure.",
        "narrateur|Le torchon sent encore l'eau.",
        "maman|Tu as fini de les suivre ?",
        "enfant-m|Oui, maman.",
    ],
    "CHK_T0000_P0000_END": [
        "maman|On pose les bateaux au soleil ?",
        "enfant-m|Oui.",
        "narrateur|Aniss pose un bateau sur le rebord.",
        "narrateur|Chouchou pose l'autre.",
        "narrateur|Le papier sèche un peu.",
        "papa|Tu as fini de poser les bateaux ?",
        "enfant-m|Oui, papa.",
        "maman|Les chaussettes de Chouchou sont sèches.",
        "enfant-m|Les miennes sont un peu mouillées.",
        "maman|On les change après.",
        "narrateur|La cour redevient calme.",
        "narrateur|L'escargot est encore là.",
        "papa|Il avance toujours.",
        "enfant-m|Tout lent.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-m|Mes bateaux ont couru.",
        "enfant-m|Chouchou a regardé.",
        "maman|Bravo, Aniss.",
        "papa|Le rebord a deux bateaux.",
        "narrateur|Le zinc ne goutte plus.",
        "narrateur|L'histoire est finie.",
    ],
}

# ---------------------------------------------------------------------------
# ATOM-DIF.BES.002-07 N1 — Mila, lettre sous la porte
# ---------------------------------------------------------------------------
S07 = {
    "CHK_T0000_P0000": [
        "narrateur|Le tiroir du bureau sent le papier.",
        "narrateur|Une gomme rose roule.",
        "narrateur|Un rayon entre par le volet.",
        "narrateur|Il fait un rectangle sur le tapis.",
        "narrateur|Une enveloppe jaune attend.",
        "narrateur|Un crayon bleu aussi.",
        "maman|Tu as vu le rayon, Mila ?",
        "enfant-f|Oui, maman.",
        "enfant-f|Il est chaud.",
        "maman|Oui.",
        "papa|J'épluche les carottes, là.",
        "papa|Dans la cuisine.",
        "enfant-f|Je veux lui écrire.",
        "maman|Une lettre, pour papa ?",
        "enfant-f|Oui.",
        "narrateur|En ce moment, Mila prend le crayon.",
        "narrateur|Le bois est lisse.",
        "narrateur|Elle dessine un soleil.",
        "narrateur|Le soleil a des rayons ronds.",
        "maman|Il est beau, ce soleil.",
        "enfant-f|Il est pour papa.",
        "narrateur|Maman ouvre la porte.",
        "narrateur|Victorina arrive, tout doux.",
        "narrateur|Elle reste près du tapis.",
        "enfant-f|Tu viens ?",
        "enfant-f|On colle le soleil.",
        "copine|Non.",
        "narrateur|Mila écoute.",
        "enfant-f|D'accord.",
        "maman|On peut proposer.",
        "maman|Tu as proposé, Mila.",
        "narrateur|Mila prend un autocollant.",
        "narrateur|Il est rouge, un peu brillant.",
        "narrateur|Il colle à son doigt.",
        "enfant-f|Il reste !",
        "maman|Tout doux.",
        "narrateur|Victorina s'assoit près du tapis.",
        "narrateur|Elle regarde le doigt.",
        "enfant-f|Tu m'aides ?",
        "copine|Je regarde.",
        "enfant-f|D'accord.",
        "maman|Regarder, c'est une réponse.",
        "narrateur|Le rayon glisse sur la gomme.",
        "narrateur|La gomme est tiède.",
        "papa|La soupe sent déjà, ici.",
        "enfant-f|Ma lettre aussi.",
        "narrateur|Le crayon roule un peu.",
        "narrateur|Mila le rattrape.",
        "maman|Tu as fini de dessiner ?",
        "enfant-f|Presque.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Mila invite Victorina.",
        "narrateur|Que fait-on ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Mila frotte le doigt au bois.",
        "narrateur|L'autocollant se décolle.",
        "enfant-f|Il vient !",
        "maman|Oui.",
        "maman|On peut accepter plusieurs réponses.",
        "narrateur|Mila pose le soleil dans l'enveloppe.",
        "narrateur|Elle colle le rouge, tout doux.",
        "narrateur|Victorina avance un peu.",
        "narrateur|Elle ne touche pas.",
        "enfant-f|Tu veux fermer ?",
        "copine|Plus tard.",
        "enfant-f|D'accord.",
        "narrateur|Mila glisse l'enveloppe.",
        "narrateur|Elle passe sous la porte.",
        "narrateur|Le papier fait un petit bruit.",
        "papa|Il y a une lettre !",
        "enfant-f|C'est le soleil !",
        "papa|Je l'ouvre.",
        "narrateur|La porte s'ouvre un peu.",
        "narrateur|Ça sent la carotte chaude.",
        "papa|Le soleil est pour moi ?",
        "enfant-f|Oui, papa.",
        "maman|Tu as accepté, Mila.",
        "narrateur|Victorina regarde encore.",
        "narrateur|Elle reste près du tapis.",
    ],
    "CHK_T0000_P0000_END": [
        "maman|On range le crayon ?",
        "enfant-f|Oui.",
        "narrateur|Mila pose le crayon.",
        "narrateur|Victorina pose la gomme.",
        "narrateur|Le tiroir sent encore le papier.",
        "papa|Le soleil est sur la table.",
        "papa|Près des carottes.",
        "enfant-f|Il brille un peu.",
        "maman|Tu as fini de ranger ?",
        "enfant-f|Oui, maman.",
        "narrateur|Le rayon a bougé.",
        "narrateur|Il touche maintenant le tapis.",
        "narrateur|La cuisine sent la soupe.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-f|J'ai envoyé le soleil.",
        "enfant-f|Victorina a regardé.",
        "maman|Bravo, Mila.",
        "papa|Le soleil est à table.",
        "narrateur|L'enveloppe est vide, maintenant.",
        "narrateur|L'histoire est finie.",
    ],
}

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.001-01 N1 — Victorino, bol de fraises
# ---------------------------------------------------------------------------
C01 = {
    "CHK_T0000_P0000": [
        "narrateur|Le bol émaillé est froid.",
        "narrateur|Maman l'a rincé.",
        "narrateur|Une goutte coule sur le bord.",
        "narrateur|Les fraisiers sentent la terre.",
        "narrateur|La terre est tiède.",
        "narrateur|Une abeille passe, tout loin.",
        "maman|Tu as vu la goutte ?",
        "enfant-m|Oui, maman.",
        "enfant-m|Elle brille.",
        "maman|Oui.",
        "enfant-m|Je veux des fraises.",
        "maman|Pour le goûter, sur le plaid ?",
        "enfant-m|Oui.",
        "narrateur|En ce moment, Victorino se baisse.",
        "narrateur|Les feuilles lui touchent les mains.",
        "narrateur|Elles sont un peu râpeuses.",
        "narrateur|Nina arrive avec un panier.",
        "narrateur|Nina est plus grande.",
        "narrateur|Victorino est plus petit.",
        "narrateur|Ils ont des tailles différentes.",
        "enfant-m|Tu viens ?",
        "copine|Oui.",
        "narrateur|Ils vont près des fraisiers.",
        "narrateur|Une fraise rouge est trop haut.",
        "narrateur|Victorino lève la main.",
        "narrateur|Il n'arrive pas.",
        "enfant-m|Elle est trop haut.",
        "maman|Il y en a en bas aussi.",
        "narrateur|Nina cueille la haute.",
        "narrateur|Victorino cueille une basse.",
        "narrateur|La basse sent le sucre.",
        "enfant-m|Elle est chaude !",
        "maman|Le soleil l'a chauffée.",
        "maman|Vous jouez ensemble.",
        "maman|On peut jouer ensemble.",
        "narrateur|Le bol sonne un peu.",
        "narrateur|Deux fraises roulent dedans.",
        "copine|Encore une ?",
        "enfant-m|Oui.",
        "narrateur|Une feuille colle au poignet.",
        "narrateur|Victorino la retire, tout doux.",
        "narrateur|La terre reste sur ses genoux.",
        "narrateur|Elle est chaude, un peu sèche.",
        "maman|On laisse l'abeille ?",
        "enfant-m|Oui.",
        "maman|Tu as de la terre aux genoux.",
        "enfant-m|C'est le jardin.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Victorino invite Nina.",
        "narrateur|Que font-ils ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Nina pose une fraise haute.",
        "narrateur|Victorino pose une fraise basse.",
        "narrateur|Le bol se remplit.",
        "narrateur|Le fond devient rouge.",
        "enfant-m|Il est lourd, maintenant.",
        "maman|Oui.",
        "maman|Petit ou grand, on cueille.",
        "narrateur|Ils tapent des mains, tout doux.",
        "narrateur|Une goutte de jus brille.",
        "narrateur|Elle est sur le menton de Nina.",
        "copine|C'est sucré.",
        "enfant-m|La mienne aussi.",
        "maman|Vous avez des tailles différentes.",
        "maman|Et vous jouez ensemble.",
        "maman|Le bol est plein, non ?",
        "enfant-m|Oui, maman.",
        "narrateur|Le plaid attend sous le cerisier.",
        "narrateur|Il sent encore le linge.",
        "narrateur|L'abeille s'éloigne.",
        "narrateur|Les feuilles bougent un peu.",
        "enfant-m|On y va ?",
        "copine|Oui.",
    ],
    "CHK_T0000_P0000_END": [
        "maman|On pose le bol sur le plaid ?",
        "enfant-m|Oui.",
        "narrateur|Victorino pose le bol.",
        "narrateur|Nina pose le panier.",
        "narrateur|Les fraises sentent fort.",
        "maman|Tu as fini de poser le bol ?",
        "enfant-m|Oui, maman.",
        "narrateur|Ils s'assoient sur le plaid.",
        "narrateur|Le plaid est un peu rêche.",
        "copine|À demain.",
        "enfant-m|À demain.",
        "narrateur|Le jardin redevient calme.",
        "narrateur|Le bol émaillé n'est plus froid.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-m|On a un bol de fraises.",
        "enfant-m|On a cueilli ensemble.",
        "maman|Bravo, Victorino.",
        "narrateur|Une goutte sèche sur le bord.",
        "narrateur|L'histoire est finie.",
    ],
}

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.001-02 N3 — Sarah, carton du marché, ballon
# ---------------------------------------------------------------------------
C02 = {
    "CHK_T0000_P0000": [
        "narrateur|Les samares du tilleul tournent.",
        "narrateur|Elles tombent sur un carton.",
        "narrateur|Le carton sent encore l'orange.",
        "narrateur|Papa le pose près du banc.",
        "narrateur|Un filet dort contre le pied.",
        "narrateur|Dedans, un ballon jaune attend.",
        "papa|Tu as vu les samares, Sarah ?",
        "enfant-f|Oui, papa.",
        "enfant-f|Elles tournent comme des hélices.",
        "papa|Oui.",
        "enfant-f|Je veux viser le carton.",
        "papa|Le ballon dans la boîte ?",
        "enfant-f|Oui.",
        "narrateur|En ce moment, Sarah ouvre le filet.",
        "narrateur|Le ballon est un peu froid.",
        "narrateur|Il sent le caoutchouc.",
        "narrateur|Nino arrive près du banc.",
        "narrateur|Nino est plus grand.",
        "narrateur|Sarah est plus petite.",
        "narrateur|Ils ont des tailles différentes.",
        "enfant-f|Tu veux le carton avec moi ?",
        "copain|Oui.",
        "papa|Vous jouez ensemble.",
        "papa|On peut jouer ensemble.",
        "narrateur|Sarah pousse le ballon, tout près.",
        "narrateur|Le carton fait un bruit mou.",
        "enfant-f|Il est dedans !",
        "papa|Oui.",
        "narrateur|Nino pousse plus fort.",
        "narrateur|Le ballon passe au-dessus.",
        "narrateur|Il roule sous le banc.",
        "enfant-f|Il est parti !",
        "papa|On le reprend, tout doux.",
        "narrateur|Sarah se baisse.",
        "narrateur|Son bras passe sous le bois.",
        "narrateur|Nino tient le banc, tout calme.",
        "enfant-f|Je le touche !",
        "copain|Doucement.",
        "narrateur|Le ballon revient, un peu poussiéreux.",
        "narrateur|Une samare est collée dessus.",
        "papa|Le carton est un peu loin, là.",
        "enfant-f|On le rapproche ?",
        "papa|Oui.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Sarah est plus petite.",
        "narrateur|Nino est plus grand.",
        "narrateur|Que font-ils ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Sarah tire le carton, tout près.",
        "narrateur|Nino pousse l'autre bord.",
        "narrateur|Le carton glisse sur l'herbe.",
        "narrateur|Ça sent l'orange encore.",
        "enfant-f|Il est tout près, maintenant.",
        "papa|Oui.",
        "papa|Les deux peuvent viser.",
        "narrateur|Sarah pousse le ballon.",
        "narrateur|Nino le pousse plus bas.",
        "narrateur|Les deux façons marchent.",
        "narrateur|Le ballon entre, deux fois.",
        "copain|Encore !",
        "enfant-f|Encore.",
        "papa|Vous avez des tailles différentes.",
        "papa|Et vous jouez ensemble.",
        "papa|C'était bien, le but ?",
        "enfant-f|Oui, papa.",
        "narrateur|Un pigeon marche près du filet.",
        "narrateur|Sarah souffle un peu.",
        "narrateur|Nino pose le ballon entre eux.",
        "narrateur|Le carton a un coin froissé.",
        "enfant-f|Il a travaillé, le carton.",
        "papa|Oui.",
        "papa|L'orange aussi, ce matin.",
    ],
    "CHK_T0000_P0000_END": [
        "papa|On range le ballon jaune ?",
        "enfant-f|Oui.",
        "narrateur|Papa glisse le ballon dans le filet.",
        "narrateur|Sarah plie le carton, tout doux.",
        "narrateur|Nino ramasse une samare.",
        "copain|À demain.",
        "enfant-f|À demain.",
        "papa|Tu as fini de plier le carton ?",
        "enfant-f|Oui, papa.",
        "narrateur|Le tilleul fait encore tourner une hélice.",
        "narrateur|Le banc redevient calme.",
        "narrateur|L'herbe a une trace de carton.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-f|Le ballon est entré.",
        "enfant-f|On a joué ensemble.",
        "papa|Bravo, Sarah.",
        "narrateur|Le filet est sur l'épaule de papa.",
        "narrateur|L'histoire est finie.",
    ],
}

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.001-03 N3 — Nino, bateaux de pomme, bassine
# ---------------------------------------------------------------------------
C03 = {
    "CHK_T0000_P0000": [
        "narrateur|La tarte aux pommes fume encore.",
        "narrateur|Elle sent le beurre.",
        "narrateur|Maman l'a posée sur la pierre.",
        "narrateur|La pierre est froide, sous le plat.",
        "narrateur|Une pomme tombée attend dans l'herbe.",
        "narrateur|Une feuille y est collée.",
        "maman|Tu as senti la tarte, Nino ?",
        "enfant-m|Oui, maman.",
        "enfant-m|Elle est chaude.",
        "maman|Elle va refroidir.",
        "enfant-m|Je veux un bateau de pomme.",
        "maman|Dans la bassine ?",
        "enfant-m|Oui.",
        "narrateur|En ce moment, Nino prend la pomme.",
        "narrateur|Elle est collante, un peu sucrée.",
        "narrateur|Maman pose une bassine d'eau.",
        "narrateur|La bassine est sur la table.",
        "narrateur|Mila arrive sous l'arbre.",
        "narrateur|Mila est plus petite.",
        "narrateur|Nino est plus grand.",
        "narrateur|Ils ont des tailles différentes.",
        "enfant-m|Tu veux le bateau avec moi ?",
        "copine|Oui.",
        "narrateur|Mila lève les mains.",
        "narrateur|La table est trop haute pour elle.",
        "enfant-m|Elle n'atteint pas.",
        "maman|On pose la bassine plus bas.",
        "narrateur|Maman la pose sur la marche.",
        "narrateur|L'eau tremble, puis s'arrête.",
        "maman|Vous jouez ensemble, là.",
        "maman|On peut jouer ensemble.",
        "narrateur|Nino met une feuille en voile.",
        "narrateur|Mila pousse la pomme dans l'eau.",
        "narrateur|La pomme tourne, tout seule.",
        "enfant-m|Elle fait des ronds !",
        "maman|Oui.",
        "copine|On souffle ?",
        "enfant-m|Oui.",
        "narrateur|Ils soufflent ensemble.",
        "narrateur|L'eau fait de toutes petites vagues.",
        "narrateur|Ça sent encore le beurre, derrière.",
        "maman|La tarte attend.",
        "enfant-m|Le bateau d'abord.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Nino est plus grand.",
        "narrateur|Mila est plus petite.",
        "narrateur|Que font-ils ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Le bateau arrive au bord.",
        "narrateur|Mila le rattrape tout bas.",
        "narrateur|Nino en prépare un autre.",
        "narrateur|Une feuille verte, une pomme jaune.",
        "enfant-m|Deux bateaux, maintenant.",
        "maman|Oui.",
        "maman|Les deux façons marchent.",
        "narrateur|Parfois Nino pousse plus loin.",
        "narrateur|Parfois Mila pousse tout près.",
        "narrateur|Les pommes se croisent.",
        "copine|La mienne a tourné !",
        "enfant-m|La mienne aussi.",
        "maman|Vous avez des tailles différentes.",
        "maman|Et vous jouez ensemble.",
        "maman|Le bateau a bien flotté ?",
        "enfant-m|Oui, maman.",
        "narrateur|Une goutte tombe de la feuille.",
        "narrateur|Elle fait un rond dans l'eau.",
        "narrateur|La tarte ne fume plus.",
        "narrateur|Elle sent encore le beurre.",
        "enfant-m|Elle est prête ?",
        "maman|Presque.",
        "maman|Un bateau encore, si vous voulez.",
        "copine|Encore un.",
    ],
    "CHK_T0000_P0000_END": [
        "maman|On range les pommes sur l'assiette ?",
        "enfant-m|Oui.",
        "narrateur|Nino pose une pomme.",
        "narrateur|Mila pose l'autre.",
        "narrateur|Les voiles de feuilles restent à côté.",
        "maman|Tu as fini de poser les bateaux ?",
        "enfant-m|Oui, maman.",
        "narrateur|Maman vide la bassine, tout bas.",
        "narrateur|L'eau part dans l'herbe.",
        "copine|À demain.",
        "enfant-m|À demain.",
        "narrateur|La pierre sous la tarte est sèche.",
        "narrateur|Le jardin sent le fruit et le beurre.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-m|Les bateaux ont flotté.",
        "enfant-m|On a joué ensemble.",
        "maman|Bravo, Nino.",
        "narrateur|La tarte attend encore un peu.",
        "narrateur|L'histoire est finie.",
    ],
}

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.001-04 N3 — Nina, tunnel du drap
# ---------------------------------------------------------------------------
C04 = {
    "CHK_T0000_P0000": [
        "narrateur|Le drap blanc sent le soleil.",
        "narrateur|Il a séché sur le fil.",
        "narrateur|Une pince à linge tient un coin.",
        "narrateur|Le cerceau rouge est contre le mur.",
        "narrateur|Une petite voiture de bois attend.",
        "narrateur|Ses roues sont un peu poussiéreuses.",
        "papa|Tu as senti le drap, Nina ?",
        "enfant-f|Oui, papa.",
        "enfant-f|Il est chaud.",
        "papa|Oui.",
        "enfant-f|Je veux un tunnel pour la voiture.",
        "maman|Avec le cerceau et le drap ?",
        "enfant-f|Oui.",
        "narrateur|En ce moment, Nina prend le cerceau.",
        "narrateur|Le fer est tiède.",
        "narrateur|Il fait un petit ding contre le mur.",
        "narrateur|Aniss arrive près du fil.",
        "narrateur|Aniss est plus petit.",
        "narrateur|Nina est plus grande.",
        "narrateur|Ils ont des tailles différentes.",
        "enfant-f|Tu viens ?",
        "enfant-f|On fait un tunnel.",
        "copain|Oui.",
        "narrateur|Nina tient le cerceau debout.",
        "narrateur|Le cerceau part, tout seul.",
        "narrateur|Il roule dans les feuilles sèches.",
        "enfant-f|Il est parti !",
        "papa|On le reprend ensemble.",
        "narrateur|Aniss ramène le bas.",
        "narrateur|Nina ramène le haut.",
        "narrateur|Les feuilles raclent le fer.",
        "copain|Il fait ding !",
        "papa|Oui.",
        "maman|Vous jouez ensemble.",
        "maman|On peut jouer ensemble.",
        "narrateur|Nina veut tenir le cerceau haut.",
        "narrateur|Aniss n'atteint pas le haut.",
        "enfant-f|Le haut est loin.",
        "maman|On le pose plus bas, alors.",
        "narrateur|Le cerceau repose sur l'herbe.",
        "narrateur|Aniss tient un coin du drap.",
        "narrateur|Nina tient l'autre coin.",
        "papa|Le tunnel est prêt ?",
        "enfant-f|Presque.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Nina invite Aniss.",
        "narrateur|Que font-ils ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Le drap tombe sur le cerceau.",
        "narrateur|Ça fait une petite grotte claire.",
        "narrateur|La lumière passe à travers.",
        "enfant-f|C'est blanc, dedans.",
        "papa|Oui.",
        "narrateur|Nina pousse la voiture.",
        "narrateur|Aniss l'attend de l'autre côté.",
        "narrateur|Les roues font un bruit de bois.",
        "copain|Elle arrive !",
        "enfant-f|Elle est passée.",
        "maman|Les deux façons marchent.",
        "maman|Vous avez des tailles différentes.",
        "maman|Et vous jouez ensemble.",
        "papa|Encore un tour ?",
        "enfant-f|Oui, papa.",
        "narrateur|Aniss pousse, cette fois.",
        "narrateur|Nina attend, tout bas.",
        "narrateur|La voiture ressort, un peu chaude.",
        "narrateur|Une feuille sèche est restée dessus.",
        "papa|Elle vient du platane, ça.",
        "enfant-f|Oui.",
        "narrateur|Le fil à linge claque un peu.",
        "narrateur|La pince tient encore le coin.",
        "maman|Le tunnel tient bien ?",
        "enfant-f|Oui, maman.",
    ],
    "CHK_T0000_P0000_END": [
        "maman|On plie le drap ?",
        "enfant-f|Oui.",
        "narrateur|Nina plie le drap, tout doux.",
        "narrateur|Aniss pose le cerceau contre le mur.",
        "narrateur|La voiture rentre dans une chaussure.",
        "papa|Tu as fini de plier le drap ?",
        "enfant-f|Oui, papa.",
        "copain|À demain.",
        "enfant-f|À demain.",
        "narrateur|Le fil à linge redevient calme.",
        "narrateur|Les feuilles sèches ne bougent plus.",
        "maman|On se lave les mains ?",
        "enfant-f|Oui.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-f|La voiture a traversé le tunnel.",
        "enfant-f|On a joué ensemble.",
        "maman|Bravo, Nina.",
        "narrateur|Le drap sent encore le soleil.",
        "narrateur|L'histoire est finie.",
    ],
}

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.001-05 N1 — Amir, camion sous le robinet
# ---------------------------------------------------------------------------
C05 = {
    "CHK_T0000_P0000": [
        "narrateur|Le torchon à carreaux sent le savon.",
        "narrateur|Il sèche sur la pierre.",
        "narrateur|Le petit camion de bois a de la poussière.",
        "narrateur|Les carreaux du jardin sont chauds.",
        "narrateur|Le robinet goutte, tout lent.",
        "narrateur|Une coccinelle marche sur une feuille.",
        "maman|Tu as vu le torchon, Amir ?",
        "enfant-m|Oui, maman.",
        "enfant-m|Il sent le propre.",
        "maman|Oui.",
        "enfant-m|Je veux laver le camion.",
        "maman|Pour un voyage, après ?",
        "enfant-m|Oui.",
        "narrateur|En ce moment, Amir prend le camion.",
        "narrateur|Le bois est sec, un peu rêche.",
        "narrateur|Sarah arrive avec le seau.",
        "narrateur|Sarah est plus grande.",
        "narrateur|Amir est plus petit.",
        "narrateur|Ils ont des tailles différentes.",
        "enfant-m|Tu viens ?",
        "enfant-m|On lave le camion.",
        "copine|Oui.",
        "narrateur|Maman ouvre le robinet, tout doux.",
        "narrateur|L'eau est tiède.",
        "narrateur|Elle brille sur les carreaux.",
        "enfant-m|Je n'atteins pas.",
        "maman|Sarah tient le camion.",
        "maman|Toi, tu frottes les roues.",
        "maman|Vous jouez ensemble.",
        "maman|On peut jouer ensemble.",
        "narrateur|Sarah tient le toit sous l'eau.",
        "narrateur|Amir frotte les roues.",
        "narrateur|Le torchon est mouillé, maintenant.",
        "enfant-m|Ça mousse un peu !",
        "maman|Oui.",
        "copine|Le toit brille.",
        "enfant-m|Les roues aussi.",
        "narrateur|Une goutte tombe sur un carreau.",
        "narrateur|Elle fait un petit chemin.",
        "maman|On laisse la coccinelle ?",
        "enfant-m|Oui.",
        "narrateur|Le camion n'a plus de poussière.",
        "narrateur|Le bois est foncé, tout propre.",
        "narrateur|Une goutte reste sur le capot.",
        "enfant-m|Elle brille.",
        "maman|Oui.",
        "maman|Le bois a bu un peu.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Amir invite Sarah.",
        "narrateur|Que font-ils ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Amir essuie une roue.",
        "narrateur|Sarah essuie le toit.",
        "narrateur|Les deux façons marchent.",
        "enfant-m|Il est lisse, maintenant.",
        "maman|Oui.",
        "maman|Vous avez des tailles différentes.",
        "maman|Et vous jouez ensemble.",
        "narrateur|Ils tapent des mains, tout doux.",
        "narrateur|Le torchon goutte sur la pierre.",
        "copine|On fait le voyage ?",
        "enfant-m|Oui.",
        "narrateur|Un plaid attend près des tomates.",
        "narrateur|Il sent le soleil.",
        "narrateur|Amir pousse le camion.",
        "narrateur|Sarah marche à côté.",
        "narrateur|Les roues font un bruit mouillé.",
        "enfant-m|Il va au garage.",
        "maman|Le plaid est le garage ?",
        "enfant-m|Oui, maman.",
        "narrateur|La coccinelle est encore là.",
        "narrateur|Les carreaux sèchent déjà.",
        "maman|Le camion a bien voyagé ?",
        "enfant-m|Oui.",
    ],
    "CHK_T0000_P0000_END": [
        "maman|On pose le camion sur le plaid ?",
        "enfant-m|Oui.",
        "narrateur|Amir pose le camion.",
        "narrateur|Sarah pose le torchon.",
        "narrateur|Le bois sèche au soleil.",
        "maman|Tu as fini de poser le camion ?",
        "enfant-m|Oui, maman.",
        "copine|À demain.",
        "enfant-m|À demain.",
        "narrateur|Le robinet ne goutte plus.",
        "narrateur|Les carreaux redeviennent calmes.",
        "narrateur|Le plaid garde une petite trace d'eau.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-m|Le camion est propre.",
        "enfant-m|On a joué ensemble.",
        "maman|Bravo, Amir.",
        "narrateur|Le torchon sèche encore.",
        "narrateur|L'histoire est finie.",
    ],
}

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.001-06 N3 — Raphaël, garage de la planche
# ---------------------------------------------------------------------------
C06 = {
    "CHK_T0000_P0000": [
        "narrateur|La planche sent la résine.",
        "narrateur|Elle est chaude du soleil.",
        "narrateur|Un fil à linge fait de l'ombre.",
        "narrateur|Le linge claque un peu.",
        "narrateur|Une caisse de bois attend.",
        "narrateur|Dedans, un camion de bois dort.",
        "papa|Tu as senti la planche, Raphaël ?",
        "enfant-m|Oui, papa.",
        "enfant-m|Elle sent l'arbre.",
        "papa|Oui.",
        "enfant-m|Je veux un garage pour le camion.",
        "papa|Avec la caisse et la planche ?",
        "enfant-m|Oui.",
        "narrateur|En ce moment, Raphaël ouvre la caisse.",
        "narrateur|Le bois est lisse, un peu chaud.",
        "narrateur|Chouchou arrive sur les dalles.",
        "narrateur|Chouchou est plus petit.",
        "narrateur|Raphaël est plus grand.",
        "narrateur|Ils ont des tailles différentes.",
        "enfant-m|Chouchou, tu veux le garage ?",
        "copain|Oui.",
        "papa|Vous jouez ensemble.",
        "papa|On peut jouer ensemble.",
        "narrateur|Raphaël pose la planche sur la caisse.",
        "narrateur|Le toit est haut.",
        "narrateur|Chouchou pousse le camion.",
        "narrateur|Le camion n'entre pas.",
        "enfant-m|C'est trop haut.",
        "papa|On baisse un côté, alors.",
        "narrateur|Papa pose un livre sous un bord.",
        "narrateur|L'autre bord reste sur la caisse.",
        "narrateur|Le toit penche, tout doux.",
        "copain|Il entre, maintenant ?",
        "enfant-m|On essaie.",
        "narrateur|Une fourmi croise la terrasse.",
        "narrateur|Elle contourne la caisse.",
        "papa|On laisse la fourmi ?",
        "enfant-m|Oui.",
        "narrateur|Le linge fait une ombre mobile.",
        "narrateur|Elle passe sur le camion.",
        "enfant-m|Le garage a du soleil.",
        "papa|Et de l'ombre, aussi.",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|Chouchou est plus petit.",
        "narrateur|Que fait Raphaël ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Chouchou pousse le camion.",
        "narrateur|Le camion rentre sous la planche.",
        "narrateur|Les roues font un petit clic.",
        "enfant-m|Il est dedans !",
        "papa|Oui.",
        "papa|Les deux façons marchent.",
        "narrateur|Raphaël pose un cube en enseigne.",
        "narrateur|Chouchou pose une feuille devant.",
        "narrateur|C'est la porte, tout doux.",
        "copain|Le camion dort.",
        "enfant-m|Il est au garage.",
        "papa|Vous avez des tailles différentes.",
        "papa|Et vous jouez ensemble.",
        "papa|Le garage est solide, non ?",
        "enfant-m|Oui, papa.",
        "narrateur|La fourmi contourne le cube.",
        "narrateur|Chouchou la suit des yeux.",
        "narrateur|Le linge claque encore une fois.",
        "narrateur|La planche sent toujours la résine.",
        "enfant-m|Encore un voyage ?",
        "copain|Un tout petit.",
        "narrateur|Le camion sort, puis rentre.",
        "narrateur|Le toit ne bouge plus.",
        "papa|Vous construisez ensemble.",
    ],
    "CHK_T0000_P0000_END": [
        "papa|On range le camion dans la caisse ?",
        "enfant-m|Oui.",
        "narrateur|Raphaël glisse le camion.",
        "narrateur|Chouchou pose la feuille à côté.",
        "narrateur|Papa pose la planche contre le mur.",
        "papa|Tu as fini de ranger le camion ?",
        "enfant-m|Oui, papa.",
        "narrateur|Le linge bouge encore, au vent.",
        "narrateur|Les dalles redeviennent calmes.",
        "papa|On se lave les mains ?",
        "enfant-m|Oui.",
        "narrateur|Le soleil du soir baisse un peu.",
        "narrateur|L'ombre du fil s'allonge.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "enfant-m|Le camion a eu un garage.",
        "enfant-m|On a joué ensemble.",
        "papa|Bravo, Raphaël.",
        "narrateur|La planche sent encore la résine.",
        "narrateur|L'histoire est finie.",
    ],
}


def main() -> None:
    write_story(
        "ATOM-DIF.BES.002-06",
        "Aniss veut faire courir ses bateaux de papier dans la flaque de la cour. Chouchou regarde, puis dit plus tard. Aniss accepte, dégage le bateau d'une feuille, et les deux sèchent sur le rebord.",
        "Les bateaux de la cour",
        "Aniss, Chouchou, papa, maman",
        "cour après la pluie, gouttière de zinc, flaque des dalles",
        S06,
        {"CHK_T0000_P0000": "", "CHK_T0000_P0000_END": ""},
        {
            "expected_answer": "accepter",
            "accepted_examples": "accepter | d'accord | proposer | regarder | plus tard",
            "retry_prompt": "Il accepte. Que fait Aniss ?",
        },
    )
    write_story(
        "ATOM-DIF.BES.002-07",
        "Mila veut glisser une lettre-soleil sous la porte de la cuisine. Victorina dit non, puis regarder. L'autocollant colle au doigt. Mila accepte, décolle, et papa trouve la lettre.",
        "La lettre de Mila",
        "Mila, Victorina, papa, maman",
        "bureau près du salon, porte de la cuisine",
        S07,
        {},
        {
            "expected_answer": "proposer",
            "accepted_examples": "proposer | inviter | accepter | d'accord",
            "retry_prompt": "On peut proposer. Que fait Mila ?",
        },
    )
    write_story(
        "ATOM-DIF.COR.001-01",
        "Victorino veut un bol de fraises pour le goûter. Nina est plus grande, lui plus petit. Ils cueillent ensemble, haut et bas. Le bol se remplit sur le plaid.",
        "Le bol de fraises",
        "Victorino, Nina, maman",
        "jardin, fraisiers, plaid sous le cerisier",
        C01,
        {},
        {
            "expected_answer": "jouer ensemble",
            "accepted_examples": "jouer ensemble | ensemble | ils jouent | on joue | jouer",
            "retry_prompt": "Ils jouent. Que font Victorino et Nina ?",
        },
    )
    write_story(
        "ATOM-DIF.COR.001-02",
        "Sarah veut faire entrer le ballon jaune dans le carton du marché. Nino est plus grand, le ballon part sous le banc. Ils rapprochent le carton et jouent ensemble.",
        "Le carton du marché",
        "Sarah, Nino, papa",
        "square sous le tilleul, carton d'oranges, banc",
        C02,
        {"CHK_T0000_P0000": "enfants_parc", "CHK_T0000_P0000_END": "enfants_parc"},
        {
            "expected_answer": "jouer ensemble",
            "accepted_examples": "jouer ensemble | ensemble | ils jouent | inviter | le ballon",
            "retry_prompt": "Ils jouent ensemble. Que font Sarah et Nino ?",
        },
    )
    write_story(
        "ATOM-DIF.COR.001-03",
        "Nino veut faire flotter des bateaux de pomme. La bassine est trop haute pour Mila. Ils la posent sur la marche et soufflent ensemble jusqu'au bord.",
        "Les bateaux de pomme",
        "Nino, Mila, maman",
        "pierre du jardin, tarte qui refroidit, bassine sur la marche",
        C03,
        {},
        {
            "expected_answer": "jouer ensemble",
            "accepted_examples": "jouer ensemble | ensemble | ils jouent | inviter | le panier",
            "retry_prompt": "Ils jouent ensemble. Que font Nino et Mila ?",
        },
    )
    write_story(
        "ATOM-DIF.COR.001-04",
        "Nina veut un tunnel pour la voiture de bois. Le cerceau roule dans les feuilles. Aniss est plus petit. Ils tiennent drap et cerceau plus bas. La voiture passe.",
        "Le tunnel du drap",
        "Nina, Aniss, papa, maman",
        "cour, fil à linge, cerceau rouge, drap au soleil",
        C04,
        {"CHK_T0000_P0000": ""},
        {
            "expected_answer": "jouer ensemble",
            "accepted_examples": "jouer ensemble | ensemble | ils jouent | on joue | jouer",
            "retry_prompt": "Ils jouent. Que font Nina et Aniss ?",
        },
    )
    write_story(
        "ATOM-DIF.COR.001-05",
        "Amir veut laver le camion de bois pour un voyage jusqu'au plaid. Sarah est plus grande, le robinet est haut. Ils lavent ensemble. Le camion brille et roule.",
        "Le camion sous le robinet",
        "Amir, Sarah, maman",
        "jardin, robinet, torchon à carreaux, plaid",
        C05,
        {},
        {
            "expected_answer": "jouer ensemble",
            "accepted_examples": "jouer ensemble | ensemble | ils jouent | jouer",
            "retry_prompt": "Ils jouent. Que font Amir et Sarah ?",
        },
    )
    write_story(
        "ATOM-DIF.COR.001-06",
        "Raphaël veut un garage pour le camion, avec la caisse et la planche. Le toit est trop haut pour Chouchou. Ils baissent un bord. Le camion rentre.",
        "Le garage de la planche",
        "Raphaël, Chouchou, papa",
        "terrasse du soir, planche de résine, fil à linge",
        C06,
        {},
        {
            "expected_answer": "jouer ensemble",
            "accepted_examples": "jouer ensemble | jouer | inviter",
            "retry_prompt": "Ils jouent ensemble. Que fait Raphaël ?",
        },
    )


if __name__ == "__main__":
    main()
