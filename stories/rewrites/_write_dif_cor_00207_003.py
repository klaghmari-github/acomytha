#!/usr/bin/env python3
"""F-NAR-008 — merged.json ATOM-DIF.COR.002-07 et ATOM-DIF.COR.003-01..07."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 16}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "copain", "copine"}
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
    "un chuchotement serre",
    "une étape après l'autre",
    "tu as mis ce que l'adulte a dit",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom ", "léa", "lea ", "lina", "iris",
    "aïcha", "aicha", "clément", "clement", "léonie", "leonie",
    "clarisse", "éléonore", "eleonore", "dominique", "zoé", "zoe",
    "adam", "ariane", "benoît", "benoit", "delphine", "erwan",
    "kenzo", "alban", "agathe", "barnabé", "barnabe",
)
OPENING_BAD = ("joue au salon", "est dans l'entrée", "c'est le matin")


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


def make_chunk(src: dict, lines: list[str], sons, scale: float, rate: str) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["length_scale_piper"] = scale
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
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in OPENING_BAD:
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
        kind = c.get("kind") or ""
        if kind == "passage_question":
            scale, rate = 1.28, "slow"
        else:
            scale, rate = 1.22, "medium"
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
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


def relecture(sid: str, title: str, vecu: str, notes: str) -> None:
    path = ROOT / sid / "RELECTURE.md"
    path.write_text(
        f"# {sid} — {title}\n\n"
        f"Relu : ouverture, désir, imprévu, question, résolution, fin. "
        f"`chunk_id` / `kind` inchangés.\n\n"
        f"## Vécu\n{vecu}\n\n"
        f"## Vu et corrigé\n{notes}\n\n"
        f"## Non vérifié\n"
        f"Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# ATOM-DIF.COR.002-07  N3  Aniss, Chouchou, papa
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.002-07",
    "Aniss veut faire passer le ballon jaune dans un carton-tunnel. Le carton ramollit. Chouchou tient les bords. Le ballon sort de l'autre côté.",
    "Le carton-tunnel d'Aniss",
    "Aniss, Chouchou, papa",
    "chemin du parc après la pluie",
    {
        "CHK_T0000_P0000": [
            "narrateur|La terre du chemin sent le champignon.",
            "narrateur|Un fil d'argent brille sur la pierre.",
            "narrateur|C'est une limace, toute lente.",
            "narrateur|Le banc a encore une tache d'eau.",
            "narrateur|Papa pose un carton sur l'herbe.",
            "narrateur|Le carton sent le papier humide.",
            "papa|Tu as vu le fil d'argent, Aniss ?",
            "enfant-m|Il brille.",
            "papa|Oui.",
            "papa|La limace va tout doux.",
            "narrateur|En ce moment, Aniss touche le ballon jaune.",
            "narrateur|Le caoutchouc est froid et lisse.",
            "enfant-m|Je veux un tunnel.",
            "enfant-m|Avec le carton.",
            "papa|Le ballon passe dedans ?",
            "enfant-m|Oui.",
            "papa|Et il sort de l'autre côté.",
            "narrateur|Aniss pousse le carton près du banc.",
            "narrateur|L'herbe mouille ses genoux.",
            "narrateur|Ça sent le vert et la terre.",
            "narrateur|Chouchou arrive près du chemin.",
            "narrateur|Ses bottes font un bruit mou.",
            "narrateur|Chouchou est plus rond.",
            "narrateur|Aniss est plus mince.",
            "papa|On joue ensemble.",
            "papa|Le corps n'est pas une blague.",
            "enfant-m|Tu tiens le carton, Chouchou ?",
            "copain|Oui.",
            "narrateur|Chouchou tient un bord.",
            "narrateur|Aniss tient l'autre bord.",
            "narrateur|Le carton tremble un peu.",
            "enfant-m|Il est mou.",
            "papa|La pluie l'a mouillé.",
            "narrateur|Aniss pousse le ballon.",
            "narrateur|Le ballon entre dans le carton.",
            "narrateur|Le carton s'écrase tout doux.",
            "enfant-m|Oh.",
            "copain|Il reste coincé.",
            "papa|On peut le tenir plus fort.",
            "papa|Ensemble.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Le carton s'écrase.",
            "narrateur|Que font Aniss et Chouchou ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Aniss appelle Chouchou.",
            "narrateur|Ils tiennent le carton à deux.",
            "papa|Vous tenez bien les bords.",
            "papa|Merci, Aniss.",
            "papa|Merci, Chouchou.",
            "narrateur|Le carton redevient un tunnel.",
            "enfant-m|Pousse, Chouchou.",
            "copain|J'aide.",
            "narrateur|Aniss pousse le ballon tout doux.",
            "narrateur|Le caoutchouc glisse sur le carton.",
            "narrateur|Ça fait un bruit de papier.",
            "papa|On joue ensemble.",
            "papa|Le corps n'est pas une blague.",
            "enfant-m|Il va sortir ?",
            "papa|Encore un peu.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Le ballon sort de l'autre côté.",
            "narrateur|Il fait poum dans l'herbe.",
            "enfant-m|Il est passé !",
            "copain|Poum.",
            "papa|Bravo.",
            "papa|Vous avez tenu le carton.",
            "narrateur|Une goutte tombe du banc.",
            "narrateur|Elle fait un rond dans l'eau.",
            "papa|On le refait ?",
            "enfant-m|Encore.",
            "narrateur|Chouchou redresse le bord.",
            "narrateur|Aniss attend de l'autre côté.",
            "narrateur|Le ballon traverse encore.",
            "narrateur|Le carton tremble, puis tient.",
            "narrateur|Poum.",
            "enfant-m|Le tunnel marche.",
            "papa|Oui.",
            "papa|Vous l'avez fait à deux.",
            "narrateur|La limace a avancé d'un doigt.",
            "narrateur|Le fil d'argent brille encore.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le carton repose contre le banc.",
            "narrateur|Le ballon jaune attend dans l'herbe.",
            "enfant-m|Il a traversé le tunnel.",
            "papa|Oui.",
            "papa|Vous avez joué ensemble.",
            "narrateur|La terre sent encore le champignon.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "enfants_parc,ballon"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | tenir | le carton | on joue | à deux",
        "retry_prompt": "Ils tiennent le carton ensemble. Que font-ils ?",
    },
)
relecture(
    "ATOM-DIF.COR.002-07",
    "Le carton-tunnel d'Aniss",
    "Aniss veut que le ballon jaune traverse un carton-tunnel. Le carton ramollit. Chouchou tient les bords. Le ballon fait poum dans l'herbe.",
    "- Désir : le tunnel, pas « le corps n'est pas une blague ».\n"
    "- Ouverture : terre, champignon, limace. Pas la gouttière du parc.\n"
    "- Leçon greffée une fois : on joue ensemble. POS-001 : pas de rire sur le corps.\n"
    "- Troupe D16 : Aniss, Chouchou, papa. Fin vécue : poum, limace.",
)

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.003-01  N2  Mila, Sarah, maman
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.003-01",
    "Mila veut un bateau de papier dans la flaque de la cour. Le pli est de travers. Sarah, avec ses lunettes, voit le pli. Elles soufflent sur la voile.",
    "Le bateau de papier de Mila",
    "Mila, Sarah, maman",
    "entrée puis cour après la pluie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le radiateur de l'entrée fait un tic chaud.",
            "narrateur|Les manteaux sentent la laine mouillée.",
            "narrateur|Une botte jaune est couchée.",
            "narrateur|Une goutte tombe du capuchon.",
            "narrateur|Elle fait un rond sur le bois.",
            "narrateur|Maman pose une feuille blanche.",
            "narrateur|La feuille est un peu rêche.",
            "maman|Tu as entendu le radiateur, Mila ?",
            "enfant-f|Il fait tic.",
            "maman|Oui.",
            "maman|Il réchauffe les manteaux.",
            "narrateur|En ce moment, Mila plie la feuille.",
            "narrateur|Elle veut un bateau.",
            "enfant-f|Il va flotter.",
            "enfant-f|Dans la flaque.",
            "maman|On plie bien le milieu ?",
            "enfant-f|Oui.",
            "narrateur|Le papier sent le bois.",
            "narrateur|Un coin se replie tout seul.",
            "narrateur|Mila l'aplatit avec la main.",
            "narrateur|Sarah arrive près des bottes.",
            "narrateur|Sarah a des lunettes neuves.",
            "narrateur|Elles brillent un peu.",
            "narrateur|Sarah a les cheveux courts.",
            "narrateur|Son manteau est bleu vif.",
            "maman|Venez plier toutes les deux.",
            "enfant-f|Tu m'aides, Sarah ?",
            "copine|Oui.",
            "narrateur|Elles plient encore.",
            "narrateur|Le papier fait frrt.",
            "narrateur|Un pli est trop haut.",
            "narrateur|L'autre pli est trop bas.",
            "narrateur|Le bateau est un peu de travers.",
            "enfant-f|Il penche.",
            "maman|On peut regarder le pli.",
            "narrateur|Sarah se penche.",
            "narrateur|Ses lunettes aident à voir.",
            "copine|Là.",
            "copine|Ce pli-là.",
            "enfant-f|Je le vois.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah a des lunettes.",
            "narrateur|Que fait Mila ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila écoute Sarah.",
            "narrateur|Elles replient le milieu.",
            "maman|Vous pliez ensemble.",
            "maman|Merci, Mila.",
            "maman|Merci, Sarah.",
            "narrateur|Le bateau se tient droit.",
            "enfant-f|Il est prêt.",
            "copine|On va à la flaque ?",
            "maman|On met les bottes d'abord.",
            "narrateur|Mila enfile la botte jaune.",
            "narrateur|Sarah enfile les siennes.",
            "narrateur|Le caoutchouc est un peu froid.",
            "enfant-f|Elle colle, maman.",
            "maman|Tire doucement.",
            "maman|Sarah a vu le pli.",
            "maman|Le bateau se tient.",
            "enfant-f|J'ouvre la porte ?",
            "maman|Oui.",
            "narrateur|La poignée est froide.",
            "narrateur|L'air de la cour entre.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|La cour brille encore.",
            "narrateur|La flaque est ronde et calme.",
            "narrateur|Mila pose le bateau.",
            "narrateur|Le papier tremble.",
            "enfant-f|Il flotte !",
            "copine|Il avance.",
            "maman|Bravo.",
            "maman|Vous avez bien plié.",
            "narrateur|Elles soufflent tout doux.",
            "narrateur|La voile se gonfle un peu.",
            "narrateur|Le bateau tourne dans l'eau.",
            "enfant-f|Encore un souffle.",
            "copine|Le mien aussi.",
            "narrateur|Sarah souffle à son tour.",
            "narrateur|Une petite vague arrive.",
            "maman|Il reste droit.",
            "enfant-f|Grâce au pli.",
            "maman|Oui.",
            "maman|Sarah l'a vu.",
            "narrateur|Une feuille sèche passe sur l'eau.",
            "narrateur|Le bateau l'évite.",
            "copine|Il est fort.",
            "enfant-f|C'est notre bateau.",
            "narrateur|Le radiateur tic encore, derrière.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le bateau tourne au milieu.",
            "narrateur|La botte jaune attend près du seuil.",
            "enfant-f|Il a flotté.",
            "maman|Oui.",
            "maman|Vous avez plié le bateau.",
            "narrateur|La laine sèche tout doux.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "feuilles"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | inviter | plier | on joue | pas rire",
        "retry_prompt": "Mila invite Sarah. Que fait-elle ?",
    },
)
relecture(
    "ATOM-DIF.COR.003-01",
    "Le bateau de papier de Mila",
    "Mila veut un bateau de papier dans la flaque. Le pli penche. Sarah le voit avec ses lunettes. Elles soufflent sur la voile.",
    "- Désir : le bateau, pas « ne pas rire ».\n"
    "- Ouverture : radiateur, laine mouillée, botte jaune. Pas la vitre embuée.\n"
    "- Leçon greffée : on joue, les lunettes aident. POS-001 : pas de moquerie montrée.\n"
    "- Troupe D16 : Mila, Sarah, maman.",
)

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.003-02  N2  Victorino, Nina, papa
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.003-02",
    "Victorino veut tourner la corde pour que Nina saute cinq fois. La corde est lourde de pluie. Ils l'essuient sur le tronc. Nina saute cinq fois.",
    "Les cinq sauts sous le pin",
    "Victorino, Nina, papa",
    "parc sous le pin",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une pomme de pin tombe dans l'herbe.",
            "narrateur|Elle fait un petit toc.",
            "narrateur|Le pin sent la résine.",
            "narrateur|L'écorce est rugueuse sous la main.",
            "narrateur|Un peu de sève brille au soleil.",
            "narrateur|Papa décroche la corde.",
            "narrateur|Le coton est encore froid.",
            "narrateur|Une fourmi monte sur l'écorce.",
            "papa|Tu as entendu le toc, Victorino ?",
            "enfant-m|La pomme de pin.",
            "papa|Oui.",
            "papa|Elle est tombée toute seule.",
            "narrateur|En ce moment, Victorino tient un bout.",
            "narrateur|La corde sent le coton humide.",
            "enfant-m|Je veux tourner.",
            "enfant-m|Nina saute cinq fois.",
            "papa|Cinq fois sans s'arrêter ?",
            "enfant-m|Oui.",
            "papa|On compte tout haut.",
            "narrateur|Nina arrive sur le gravier.",
            "narrateur|Le gravier fait criss-criss.",
            "narrateur|Nina a des lunettes.",
            "narrateur|Nina a les cheveux tressés.",
            "narrateur|Elle porte un gilet rouge.",
            "papa|Nina, tu sautes au milieu.",
            "enfant-m|Tu sautes, Nina ?",
            "copine|Oui.",
            "narrateur|Papa tient l'autre bout.",
            "narrateur|La corde tourne.",
            "narrateur|Elle tape l'herbe, trop lourde.",
            "narrateur|Ça fait un bruit mou.",
            "narrateur|Un peu de terre colle au coton.",
            "enfant-m|Elle ne monte pas.",
            "copine|Elle est mouillée.",
            "papa|On peut l'essuyer.",
            "papa|Sur le tronc.",
            "papa|Puis on recompte.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nina a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorino va vers Nina.",
            "narrateur|Ils essuient la corde.",
            "papa|Vous frottez le coton.",
            "papa|Merci, Victorino.",
            "papa|Merci, Nina.",
            "narrateur|Le tronc sent la résine.",
            "narrateur|Un peu de sève colle aux doigts.",
            "narrateur|La corde redevient plus légère.",
            "enfant-m|Elle est moins lourde.",
            "enfant-m|On reprend ?",
            "copine|On reprend.",
            "papa|Nina suit la corde des yeux.",
            "papa|On saute.",
            "narrateur|Victorino tourne tout doux.",
            "narrateur|La corde siffle un tout petit peu.",
            "narrateur|Nina saute une fois.",
            "copine|Un.",
            "enfant-m|Encore.",
            "papa|Tu regardes la corde, Nina.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nina saute encore.",
            "copine|Deux.",
            "enfant-m|Trois.",
            "copine|Quatre.",
            "narrateur|Le gilet rouge bouge.",
            "narrateur|Les tresses tapent le dos.",
            "narrateur|Les lunettes restent bien.",
            "copine|Cinq !",
            "enfant-m|Cinq !",
            "papa|Bravo.",
            "papa|Tu as tourné sans t'arrêter.",
            "narrateur|La corde se pose dans l'herbe.",
            "papa|On reverse les rôles ?",
            "copine|À toi le milieu.",
            "narrateur|Nina tourne à son tour.",
            "narrateur|Victorino saute.",
            "narrateur|Ses chaussures font toc.",
            "enfant-m|C'est plus facile.",
            "papa|Oui.",
            "papa|La corde est sèche.",
            "narrateur|Un rayon passe entre les aiguilles.",
            "narrateur|Il allume le gilet rouge.",
            "narrateur|La fourmi est encore sur l'écorce.",
            "narrateur|La pomme de pin reste dans l'herbe.",
            "papa|On a eu nos cinq sauts.",
            "enfant-m|Oui.",
            "enfant-m|Cinq.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La corde pend à la branche.",
            "narrateur|Elle n'est plus lourde.",
            "enfant-m|Nina a sauté cinq fois.",
            "papa|Oui.",
            "papa|Vous avez eu vos cinq sauts.",
            "narrateur|Le pin sent encore la résine.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "enfants_parc,corde"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | sauter | on joue | essuyer | pas rire",
        "retry_prompt": "On saute ensemble. Que fait-on ?",
    },
)
relecture(
    "ATOM-DIF.COR.003-02",
    "Les cinq sauts sous le pin",
    "Victorino veut cinq sauts d'affilée. La corde est lourde de pluie. Ils l'essuient sur le tronc. Nina saute cinq fois.",
    "- Désir : cinq sauts, pas la leçon collée.\n"
    "- Ouverture : pomme de pin, résine. Pas l'oiseau à la clôture.\n"
    "- Leçon greffée : on joue, lunettes aident. Troupe : Victorino, Nina, papa.",
)

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.003-03  N2  Nino, Mila, maman
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.003-03",
    "Nino veut une prune bien ronde pour la tarte de maman. Il prend une molle. Mila, avec ses lunettes, voit une prune ferme au fond. Ils la portent dans le filet.",
    "La prune de la tarte",
    "Nino, Mila, maman",
    "boulangerie puis marché",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le four du boulanger souffle une odeur de mie.",
            "narrateur|Un peu de farine blanchit la planche.",
            "narrateur|Le pain chaud croustille dans le sac.",
            "narrateur|Une miette tombe près de la caisse.",
            "narrateur|Maman tient un filet de coton.",
            "narrateur|Le filet sent encore la lessive.",
            "narrateur|Le sol est un peu collant.",
            "maman|Tu as senti le pain, Nino ?",
            "enfant-m|Il est chaud.",
            "maman|Oui.",
            "maman|Il ira avec la tarte.",
            "narrateur|Nino touche le sac de pain.",
            "narrateur|Le papier est tiède.",
            "narrateur|En ce moment, Nino regarde les prunes.",
            "narrateur|Elles sont violettes et lisses.",
            "narrateur|Une caisse sent le sucré.",
            "enfant-m|J'en veux une ronde.",
            "enfant-m|Pour la tarte.",
            "maman|On en cherche une ferme.",
            "maman|Pas trop molle.",
            "narrateur|Mila arrive près de la caisse.",
            "narrateur|Ses chaussures collent un peu au sol.",
            "narrateur|Mila a des lunettes neuves.",
            "narrateur|Mila a les cheveux lisses.",
            "narrateur|Elle porte un gilet vert.",
            "maman|Mila, tu cherches avec Nino.",
            "enfant-m|Tu m'aides, Mila ?",
            "copine|Oui.",
            "narrateur|Nino prend une prune.",
            "narrateur|Elle cède un peu sous le doigt.",
            "enfant-m|Elle est molle.",
            "maman|On la repose.",
            "maman|Tout doux, dans la caisse.",
            "narrateur|Mila se penche sur la caisse.",
            "narrateur|Elle regarde au fond.",
            "copine|Au fond.",
            "copine|Celle-là.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila a des lunettes.",
            "narrateur|Que fait Nino ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino écoute Mila.",
            "narrateur|Il prend la prune du fond.",
            "narrateur|Elle est lisse et ferme.",
            "maman|Merci, Nino.",
            "maman|Merci, Mila.",
            "enfant-m|Elle est ronde.",
            "copine|Pour la tarte.",
            "maman|On la met dans le filet.",
            "narrateur|Le filet s'alourdit un peu.",
            "narrateur|Le coton se tend.",
            "maman|Mila a vu au fond.",
            "maman|On a la prune.",
            "enfant-m|On prend une pomme aussi ?",
            "maman|Oui.",
            "maman|Une pomme rouge.",
            "narrateur|Mila montre une pomme brillante.",
            "narrateur|Nino la pose dans le filet.",
            "enfant-m|Elle est lisse.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|La pomme rejoint la prune.",
            "narrateur|Le filet balance.",
            "maman|Il est lourd, le filet ?",
            "enfant-m|Un peu.",
            "maman|On le porte à deux.",
            "narrateur|Nino tient une anse.",
            "narrateur|Maman tient l'autre.",
            "narrateur|Mila marche tout près.",
            "narrateur|Un stand de menthe sent fort.",
            "enfant-m|Ça pique le nez.",
            "maman|C'est la menthe.",
            "copine|C'est vert.",
            "maman|Vert et frais.",
            "narrateur|Ils passent près des œufs.",
            "narrateur|Les boîtes sont beiges.",
            "maman|Bravo.",
            "maman|Tu as choisi la prune ferme.",
            "narrateur|Le pain chaud tape le bras.",
            "enfant-m|Ce soir, la tarte.",
            "maman|Oui.",
            "maman|Avec ta prune ronde.",
            "copine|Et la pomme.",
            "narrateur|Une balance fait tic près d'eux.",
            "narrateur|Les toiles claquent un peu.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le filet tient la prune et la pomme.",
            "narrateur|Le sac de pain sent le four.",
            "enfant-m|On a la prune de la tarte.",
            "maman|Oui.",
            "maman|Vous avez cherché ensemble.",
            "narrateur|La farine reste sur la planche.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "marche,prune"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | aider | prune | on joue | pas rire",
        "retry_prompt": "Nino écoute Mila. Que fait-il ?",
    },
)
relecture(
    "ATOM-DIF.COR.003-03",
    "La prune de la tarte",
    "Nino veut une prune ronde pour la tarte. Il prend une molle. Mila voit une ferme au fond. Ils portent le filet.",
    "- Désir : la prune de la tarte. Ouverture four du boulanger, pas les toiles d'abord.\n"
    "- Leçon greffée : jouer ensemble, lunettes aident. Troupe : Nino, Mila, maman.",
)

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.003-04  N3  Sarah, Victorina, maman
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.003-04",
    "Sarah veut une étoile de pâte avec une vraie feuille dessus. La première feuille s'effrite. Victorina en trouve une souple. L'étoile repose sur l'assiette.",
    "L'étoile et la feuille",
    "Sarah, Victorina, maman",
    "parc le matin, puis petite maison",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le toboggan du parc a un peu de givre.",
            "narrateur|Il est froid sous le doigt.",
            "narrateur|Le souffle de Sarah fait un nuage.",
            "narrateur|La petite maison sent le savon.",
            "narrateur|Maman boutonne le gilet de Sarah.",
            "narrateur|Le gilet est doux et épais.",
            "narrateur|Un oiseau crie tout près.",
            "maman|Tu es bien au chaud, Sarah ?",
            "enfant-f|Oui, maman.",
            "maman|Tes mains sont froides.",
            "enfant-f|Un peu.",
            "maman|On les frotte.",
            "narrateur|Sarah frotte ses mains.",
            "narrateur|Elles redeviennent tièdes.",
            "narrateur|En ce moment, Sarah cherche une feuille.",
            "narrateur|L'herbe sent la rosée.",
            "enfant-f|Je veux une étoile.",
            "enfant-f|Avec une feuille dessus.",
            "maman|On la presse dans la pâte ?",
            "enfant-f|Oui.",
            "maman|Une vraie nervure, alors.",
            "narrateur|Victorina arrive près du toboggan.",
            "narrateur|Victorina a des lunettes rondes.",
            "narrateur|Elle a les cheveux tressés.",
            "narrateur|Elle porte un gilet jaune.",
            "maman|Victorina, tu cherches aussi.",
            "enfant-f|Tu m'aides, Victorina ?",
            "copine|Oui.",
            "narrateur|Sarah ramasse une feuille jaune.",
            "narrateur|Elle est sèche et fragile.",
            "narrateur|Elle s'effrite entre les doigts.",
            "narrateur|Un peu de jaune reste sur la main.",
            "enfant-f|Elle casse.",
            "maman|On en cherche une souple.",
            "narrateur|Victorina se penche.",
            "narrateur|Elle choisit une feuille molle.",
            "copine|Celle-ci.",
            "copine|Elle est encore molle.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah prend la feuille souple.",
            "narrateur|Elle la pose dans sa main.",
            "maman|Merci, Sarah.",
            "maman|Merci, Victorina.",
            "enfant-f|On va à la petite maison ?",
            "maman|Oui.",
            "maman|La pâte nous attend.",
            "narrateur|La table est froide et lisse.",
            "narrateur|La pâte sent la farine.",
            "narrateur|Elle colle un peu aux doigts.",
            "maman|Victorina a trouvé la souple.",
            "maman|On presse.",
            "narrateur|Sarah fait un boudin.",
            "narrateur|Victorina fait une boule.",
            "enfant-f|L'étoile.",
            "copine|La feuille.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sarah appuie l'emporte-pièce.",
            "narrateur|L'étoile se dessine.",
            "narrateur|Victorina pose la feuille.",
            "narrateur|Sarah presse tout doux.",
            "narrateur|La nervure s'imprime dans la pâte.",
            "enfant-f|Elle est restée !",
            "copine|On voit les traits.",
            "maman|Bravo.",
            "maman|Vous avez pressé ensemble.",
            "narrateur|Un peu de farine tombe.",
            "narrateur|Ça fait un nuage tout petit.",
            "narrateur|Sarah souffle dessus, tout doux.",
            "maman|Vous voulez laver les mains ?",
            "enfant-f|Oui.",
            "narrateur|L'eau de la bassine est tiède.",
            "narrateur|Sarah frotte.",
            "narrateur|Victorina frotte.",
            "narrateur|Elles posent l'étoile sur l'assiette.",
            "narrateur|L'assiette est blanche et mate.",
            "enfant-f|Ma feuille est dessus.",
            "maman|Oui.",
            "maman|Elle est souple.",
            "copine|On voit même les bords.",
            "narrateur|Un peu de givre fond dehors.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|L'étoile repose sur l'assiette.",
            "narrateur|La feuille jaune est bien pressée.",
            "enfant-f|On l'a faite.",
            "maman|Oui.",
            "maman|Vous avez pressé l'étoile.",
            "narrateur|Le givre fond sur le toboggan.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "enfants_parc,pate"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | feuille | on joue | presser | pas rire",
        "retry_prompt": "On cherche une feuille souple. Que fait-on ?",
    },
)
relecture(
    "ATOM-DIF.COR.003-04",
    "L'étoile et la feuille",
    "Sarah veut une étoile de pâte avec une vraie feuille. La première s'effrite. Victorina en trouve une souple. L'étoile est sur l'assiette.",
    "- Désir : étoile + feuille, pas un cours d'apparence.\n"
    "- Ouverture : givre sur le toboggan. Pas le rayon entre les platanes.\n"
    "- Troupe D16 : Sarah, Victorina, maman. Fin : givre qui fond.",
)

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.003-05  N2  Amir, Nino, maman
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.003-05",
    "Amir veut dessiner une maison au toit rouge pour maman. Le crayon rouge roule sous le banc. Nino le voit avec ses lunettes. Maman reçoit le dessin.",
    "Le toit rouge d'Amir",
    "Amir, Nino, maman",
    "cour de l'école",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le robinet de la cour laisse une goutte.",
            "narrateur|Elle fait un rond sur le carreau.",
            "narrateur|Les carreaux brillent encore.",
            "narrateur|Ça sent le savon.",
            "narrateur|Un bout de craie attend au sol.",
            "narrateur|Maman pose une boîte sur le banc.",
            "narrateur|Le bois du banc est froid.",
            "narrateur|Dedans, des crayons.",
            "maman|Tu as entendu la goutte, Amir ?",
            "enfant-m|Elle tombe.",
            "maman|Oui.",
            "maman|Tout doux.",
            "narrateur|Amir pose le doigt sur le carreau.",
            "narrateur|Le carreau est froid et lisse.",
            "narrateur|En ce moment, Amir prend une feuille.",
            "narrateur|Le papier est un peu rêche.",
            "enfant-m|Je dessine une maison.",
            "enfant-m|Avec un toit rouge.",
            "enfant-m|Pour toi, maman.",
            "maman|J'aimerais beaucoup.",
            "maman|Une porte, et un toit.",
            "narrateur|Nino arrive près du banc.",
            "narrateur|Nino a des lunettes.",
            "narrateur|Nino a les cheveux courts.",
            "narrateur|Il porte un manteau rouge.",
            "maman|Nino, tu colories aussi.",
            "enfant-m|Tu colories avec moi ?",
            "copain|Oui.",
            "narrateur|Amir prend le crayon bleu.",
            "narrateur|Nino prend le crayon jaune.",
            "narrateur|Le bois des crayons est lisse.",
            "narrateur|Le bleu fait un ciel.",
            "narrateur|Le jaune fait un soleil.",
            "enfant-m|Le rouge, maintenant.",
            "narrateur|Le crayon rouge roule.",
            "narrateur|Il fait un petit bruit.",
            "narrateur|Il glisse sous le banc.",
            "enfant-m|Il est parti.",
            "maman|On peut le chercher.",
            "maman|Tout doux, près des pieds.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nino a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino se penche près du banc.",
            "narrateur|Il voit un bout de rouge.",
            "copain|Là.",
            "copain|Tout au fond.",
            "narrateur|Amir allonge le bras.",
            "narrateur|La poussière du sol est fine.",
            "narrateur|Il rattrape le crayon rouge.",
            "narrateur|Le bois est un peu froid.",
            "maman|Merci, Amir.",
            "maman|Merci, Nino.",
            "enfant-m|J'ai le toit.",
            "maman|Nino a vu le crayon.",
            "maman|Le toit peut se faire.",
            "narrateur|Amir dessine le toit.",
            "narrateur|Le rouge est vif sur le papier.",
            "copain|Il est beau.",
            "enfant-m|C'est pour maman.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|La maison a un toit rouge.",
            "narrateur|Le soleil est jaune.",
            "narrateur|Le ciel est bleu.",
            "enfant-m|Une porte.",
            "copain|Et une fenêtre.",
            "maman|Bravo.",
            "maman|Vous avez colorié ensemble.",
            "narrateur|Amir tend la feuille.",
            "enfant-m|C'est pour toi.",
            "maman|Je la prends.",
            "maman|Le toit est bien rouge.",
            "narrateur|Maman souffle un peu dessus.",
            "narrateur|Le crayon sèche.",
            "narrateur|Le papier sent encore le bois.",
            "enfant-m|La goutte tombe encore.",
            "maman|Oui.",
            "maman|On l'entend.",
            "narrateur|Nino range le crayon jaune.",
            "narrateur|Amir range le crayon rouge.",
            "narrateur|La boîte se ferme.",
            "narrateur|Ça fait clic.",
            "maman|Le dessin est à moi, maintenant.",
            "enfant-m|Oui.",
            "enfant-m|Pour la cuisine.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le dessin est dans les mains de maman.",
            "narrateur|Le toit rouge brille un peu.",
            "enfant-m|On l'a fini.",
            "maman|Oui.",
            "maman|Vous avez colorié la maison.",
            "narrateur|Le robinet laisse encore une goutte.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "cour,crayons"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | chercher | crayon | on joue | pas rire",
        "retry_prompt": "Nino voit le crayon. Que fait-on ?",
    },
)
relecture(
    "ATOM-DIF.COR.003-05",
    "Le toit rouge d'Amir",
    "Amir veut une maison au toit rouge pour maman. Le crayon roule sous le banc. Nino le voit. Maman reçoit le dessin.",
    "- Désir : le dessin offert, pas un slogan d'apparence.\n"
    "- Ouverture : goutte du robinet, savon. Pas les crochets de manteaux.\n"
    "- Troupe D16 : Amir, Nino, maman. Fin : clic de la boîte, goutte.",
)

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.003-06  N2  Nina, Aniss, maman
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.003-06",
    "Nina veut montrer l'abeille en bois à Aniss, puis un pot de miel pour le pain du soir. L'abeille est cachée. Aniss la voit. Le miel rentre dans le sac.",
    "L'abeille cachée et le miel",
    "Nina, Aniss, maman",
    "marché, stand de paille puis miel",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une poule picore près des caisses de paille.",
            "narrateur|Elle fait un petit cot-cot.",
            "narrateur|Une plume grise tourne au sol.",
            "narrateur|Ça sent le grain et le bois.",
            "narrateur|Maman tient le panier de rotin.",
            "narrateur|Le rotin est rêche et chaud.",
            "narrateur|Un rayon passe entre les toiles.",
            "maman|Tu as vu la plume, Nina ?",
            "enfant-f|Elle tourne.",
            "maman|Oui.",
            "maman|La poule l'a laissée.",
            "narrateur|Nina ramasse la plume.",
            "narrateur|Elle est légère et douce.",
            "enfant-f|Je la pose là.",
            "maman|Près du panier.",
            "narrateur|En ce moment, Nina cherche l'abeille.",
            "narrateur|Les pots dorés brillent un peu.",
            "enfant-f|L'abeille en bois.",
            "enfant-f|Je veux la montrer.",
            "maman|Elle est au stand de miel.",
            "maman|Collée sur la caisse.",
            "narrateur|Aniss arrive près des pots.",
            "narrateur|Aniss a des lunettes neuves.",
            "narrateur|Aniss a les cheveux courts.",
            "narrateur|Il porte un gilet bleu.",
            "maman|Aniss, tu regardes avec Nina.",
            "enfant-f|Tu viens voir l'abeille ?",
            "copain|Oui.",
            "narrateur|Les pots dorés sont serrés.",
            "narrateur|Ça sent le sucré et la cire.",
            "narrateur|L'abeille n'est pas devant.",
            "enfant-f|Elle n'est plus là.",
            "maman|On peut regarder derrière.",
            "maman|Tout doux, sans bouger les pots.",
            "narrateur|Aniss se penche.",
            "narrateur|Il voit les ailes peintes.",
            "copain|Derrière le gros pot.",
            "copain|Elle est collée.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss a des lunettes.",
            "narrateur|Que fait Nina ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina se penche aussi.",
            "narrateur|L'abeille en bois est là.",
            "narrateur|Elle a des ailes peintes.",
            "enfant-f|Jaune.",
            "copain|Et noire.",
            "maman|Merci, Nina.",
            "maman|Merci, Aniss.",
            "maman|Aniss a vu derrière.",
            "maman|L'abeille est là.",
            "enfant-f|On prend du miel ?",
            "maman|Un petit pot.",
            "maman|Pour le pain du soir.",
            "narrateur|Maman choisit un pot doré.",
            "narrateur|Le couvercle est un peu collant.",
            "enfant-f|Ça sent le sucré.",
            "copain|C'est épais.",
            "maman|Oui.",
            "maman|C'est le miel.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Le pot glisse dans le panier.",
            "narrateur|Le rotin crisse.",
            "maman|Vous voulez une prune ?",
            "enfant-f|Oui.",
            "narrateur|Nina tend une prune à Aniss.",
            "narrateur|La prune est lisse et froide.",
            "copain|Merci.",
            "narrateur|Ils croquent près du muret.",
            "narrateur|Le muret est un peu rêche.",
            "narrateur|Le jus est sucré.",
            "maman|Bravo.",
            "maman|Tu as montré l'abeille.",
            "enfant-f|On peut la revoir ?",
            "maman|Un dernier regard.",
            "narrateur|L'abeille brille encore.",
            "narrateur|La poule picore plus loin.",
            "narrateur|La plume ne tourne plus.",
            "enfant-f|Ce soir, le pain et le miel.",
            "maman|Oui.",
            "maman|Avec le petit pot.",
            "copain|Sur le pain chaud.",
            "narrateur|Le panier sent déjà le sucré.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le miel est dans le panier.",
            "narrateur|L'abeille reste collée sur la caisse.",
            "enfant-f|On l'a trouvée.",
            "maman|Oui.",
            "maman|Vous avez vu l'abeille.",
            "narrateur|La paille sent encore le grain.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "marche,miel"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | montrer | abeille | on joue | pas rire",
        "retry_prompt": "Nina montre l'abeille. Que fait-elle ?",
    },
)
relecture(
    "ATOM-DIF.COR.003-06",
    "L'abeille cachée et le miel",
    "Nina veut montrer l'abeille en bois, puis du miel pour le pain. L'abeille est derrière un pot. Aniss la voit. Le miel rentre.",
    "- Désir : abeille + miel du soir. Ouverture poule et paille, pas les pots d'abord.\n"
    "- Troupe D16 : Nina, Aniss, maman. Fin : abeille collée, paille.",
)

# ---------------------------------------------------------------------------
# ATOM-DIF.COR.003-07  N2  Raphaël, Mila, papa
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.003-07",
    "Raphaël veut que le cerceau bleu roule jusqu'au muret du chat, sans tomber. Une pierre arrête le cerceau. Mila l'écarte. Le chat ouvre un œil.",
    "Le cerceau jusqu'au chat",
    "Raphaël, Mila, papa",
    "square, muret et gravier",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un chat gris dort sur le muret du square.",
            "narrateur|Sa queue pend un peu.",
            "narrateur|Un volet orange claque tout doux.",
            "narrateur|Le gravier crisse sous les semelles.",
            "narrateur|Un cerceau bleu attend contre le banc.",
            "narrateur|Le plastique est lisse et frais.",
            "narrateur|Une feuille sèche tourne sur le gravier.",
            "papa|Tu as vu le chat, Raphaël ?",
            "enfant-m|Il dort.",
            "papa|Oui.",
            "papa|Tout rond sur la pierre.",
            "narrateur|Raphaël s'approche tout doux.",
            "narrateur|Le chat ne bouge pas.",
            "enfant-m|Il ronronne ?",
            "papa|Un tout petit peu.",
            "narrateur|En ce moment, Raphaël tient le cerceau.",
            "narrateur|Le plastique est un peu froid.",
            "enfant-m|Je veux qu'il aille au muret.",
            "enfant-m|Sans tomber.",
            "papa|Jusqu'au chat ?",
            "enfant-m|Oui.",
            "papa|Tout droit sur le gravier.",
            "narrateur|Mila arrive près du banc.",
            "narrateur|Ses pas font criss sur le gravier.",
            "narrateur|Mila a des lunettes.",
            "narrateur|Mila a les cheveux bouclés.",
            "narrateur|Elle porte un gilet bleu.",
            "papa|Mila, tu rattrapes au muret.",
            "enfant-m|Tu m'aides, Mila ?",
            "copine|Oui.",
            "narrateur|Raphaël pousse le cerceau.",
            "narrateur|Il part tout droit.",
            "narrateur|Le gravier crisse.",
            "narrateur|Une petite poussière monte.",
            "narrateur|Une pierre est sur le chemin.",
            "narrateur|Le cerceau tape la pierre.",
            "narrateur|Il tombe à plat.",
            "narrateur|Le plastique fait un toc mou.",
            "enfant-m|Oh.",
            "papa|On peut enlever la pierre.",
            "papa|Pour ouvrir le chemin.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila se penche.",
            "narrateur|Elle voit la pierre grise.",
            "copine|La pierre est là.",
            "narrateur|Raphaël l'écarte avec le pied.",
            "narrateur|La pierre roule vers l'herbe.",
            "papa|Merci, Raphaël.",
            "papa|Merci, Mila.",
            "papa|Mila a vu la pierre.",
            "papa|Le chemin est libre.",
            "enfant-m|On reprend ?",
            "copine|On reprend.",
            "narrateur|Raphaël pose le cerceau.",
            "narrateur|Mila attend près du muret.",
            "papa|Tu le rattrapes, Mila.",
            "copine|Je suis prête.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Le cerceau bleu roule encore.",
            "narrateur|Le chemin est libre.",
            "narrateur|Il avance, il avance.",
            "narrateur|Le plastique chante un peu.",
            "narrateur|Il arrive au muret.",
            "copine|Je l'ai !",
            "enfant-m|Il n'est pas tombé.",
            "papa|Bravo.",
            "papa|Vous avez ôté la pierre.",
            "narrateur|Le chat ouvre un œil.",
            "narrateur|Ses moustaches bougent un peu.",
            "enfant-m|Il nous a vus.",
            "papa|Puis il se rendort.",
            "narrateur|Le volet claque encore un peu.",
            "papa|On le ramène au banc ?",
            "enfant-m|Doucement.",
            "narrateur|Mila fait rouler le cerceau.",
            "narrateur|Raphaël le rattrape.",
            "narrateur|Le plastique tape le bois.",
            "enfant-m|Toc.",
            "papa|Oui.",
            "papa|Il est rentré.",
            "copine|Le chat a ouvert un œil.",
            "enfant-m|Puis il a dormi.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le cerceau bleu repose contre le banc.",
            "narrateur|Le chat dort encore sur le muret.",
            "enfant-m|Il est allé jusqu'au chat.",
            "papa|Oui.",
            "papa|Vous avez ôté la pierre.",
            "narrateur|Le gravier redevient calme.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "cerceau,gravier"},
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | ensemble | pierre | cerceau | on joue | pas rire",
        "retry_prompt": "On ôte la pierre. Que fait-on ?",
    },
)
relecture(
    "ATOM-DIF.COR.003-07",
    "Le cerceau jusqu'au chat",
    "Raphaël veut le cerceau bleu jusqu'au muret du chat. Une pierre le fait tomber. Mila la voit. Le chat ouvre un œil.",
    "- Désir : le cerceau jusqu'au chat. Ouverture chat et volet, pas le portail qui grince.\n"
    "- Troupe D16 : Raphaël, Mila, papa. Fin : chat qui dort, gravier calme.",
)

print("done")
