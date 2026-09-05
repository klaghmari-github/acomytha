#!/usr/bin/env python3
"""TREE-AUT-038 — F-NAR-019 v2. Mila, seau sous la table. N1. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words

SID = "TREE-AUT-038"
LIM = 10
TICS = ("tout doux", "tout calme", "encore", "déjà")
BAN = (
    "aujourd'hui",
    "mission accomplie",
    "j'ai compris",
    "on dirait que notre mission",
    "lumière couleur de miel",
    "gouttes pendent",
    "merle",
    "grand-père",
    "maîtresse",
    "jardinier",
    "bibliothécaire",
    "gardienne",
    "on va apprendre",
    "on va ranger",
    "après le jeu",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 128, "speed": 0.94, "piper": 1.16,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 300,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "clou de cuivre",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le seau doit rester à l_ombre; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    },
    "choice": {
        "rate": "slow", "wpm": 108, "speed": 0.80, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 340,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": (
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton choix change la ruse; tempo=suspendu; "
            "sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 110, "speed": 0.82, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "seau jaune",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=le seau attend sous le bois; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 124, "speed": 0.90, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 290,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "table",
        "note": (
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=savoir n_est pas tenir; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    },
    "action": {
        "rate": "medium", "wpm": 140, "speed": 0.98, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 400, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": (
            "arc=action; intention=entraîner; emotion=élan; intensite=2; "
            "destinataire=enfant; sous_texte=trop_vite_l_anse_bute; tempo=vif; "
            "sourire=léger; respiration=courte"
        ),
    },
    "obstacle": {
        "rate": "medium", "wpm": 122, "speed": 0.90, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 540, "sentence": 310,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=la_serviette_vole_le_clou; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 130, "speed": 0.94, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "clou de cuivre",
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=le_clou_guide_sous_l_ombre; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    },
    "ending": {
        "rate": "slow", "wpm": 108, "speed": 0.82, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 350,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": (
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_clou_reste_sur_l_anse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    },
}


def L(role: str, text: str) -> str:
    if not text.endswith((".", "?", "!")):
        raise SystemExit(f"ponct: {text}")
    parts = re.findall(r"[^.?!]+[.?!]", text.strip())
    if not parts:
        raise SystemExit(f"vide: {text}")
    if len(parts) > 1:
        raise SystemExit(f"multi: {text}")
    p = parts[0].strip()
    n = words(p)
    if n > LIM:
        raise SystemExit(f"{n}>{LIM}: {p}")
    if n == 0:
        raise SystemExit(f"vide: {p}")
    low = p.lower()
    for tic in TICS:
        if tic in low:
            raise SystemExit(f"tic {tic}: {p}")
    for bad in BAN:
        if bad in low:
            raise SystemExit(f"ban {bad}: {p}")
    return f"{role}|{text}"


def ssml(text: str, m: dict) -> str:
    body = html.escape(text, quote=False)
    if m.get("emphasis"):
        e = html.escape(m["emphasis"], quote=False)
        tagged = f'<emphasis level="moderate">{e}</emphasis>'
        body = body.replace(e, tagged, 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
    )


def xai(text: str, m: dict) -> str:
    body = text
    if m.get("emphasis"):
        e = m["emphasis"]
        body = body.replace(e, f"<emphasis>{e}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + tail).strip()


def apply_tts(src: dict, lines: list[str], sons: str, profile: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    text, script = from_script(lines)
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = extra.get("pauseBefore", 0)
    nc["pause_after_ms"] = m["pause"]
    nc["pause_sentence_ms"] = m["sentence"]
    nc["style_energy"] = m["energy"]
    nc["style_contour"] = m["contour"]
    nc["noise_scale_piper"] = m["noise"]
    nc["kokoro_speed"] = m["speed"]
    nc["melo_speed"] = m["speed"]
    nc["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    nc["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    nc["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


def profile_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "opening"
    if kind == "transition_question":
        return "choice"
    if kind == "passage_question":
        return "clue"
    if kind == "passage_fin":
        return "ending"
    if cid.endswith("_C0001"):
        return "confirm"
    if "_T0003_P000" in cid and not cid.endswith("_T0003_P0000"):
        return "resolution"
    if "_T0002_P000" in cid and cid[-1] in "123" and "_T0003_" not in cid.split("_T0002_")[-1][:6]:
        # CHK_T0001_P000i_T0002_P000j  (obstacle) vs T0002_P0000 (choice)
        if cid.endswith(("_T0002_P0001", "_T0002_P0002", "_T0002_P0003")):
            return "obstacle"
    return "action"


def preview(scripts: dict) -> None:
    n = 0
    starts: list[str] = []
    for cid, lines in scripts.items():
        prev = ""
        run = 1
        for raw in lines:
            role, phrase = raw.split("|", 1)
            w = words(phrase)
            n += w
            if w > LIM:
                raise SystemExit(f"LONG {cid} {w}>{LIM}: {phrase}")
            marks = phrase.count(".") + phrase.count("?") + phrase.count("!")
            if marks > 1:
                raise SystemExit(f"MULTI {cid}: {phrase}")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"PUNCT {cid}: {phrase}")
            tok = phrase.split()[0].lower() if role == "narrateur" else ""
            starts.append(tok)
            if tok and tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"PUCES {cid}: {tok}")
            else:
                run = 1
            prev = tok
        blob = " ".join(ln.split("|", 1)[1] for ln in lines).lower()
        for tic in TICS:
            if tic in blob:
                raise SystemExit(f"TIC {cid}: {tic}")
        for bad in BAN:
            if bad in blob:
                raise SystemExit(f"BAN {cid}: {bad}")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"PUCES global: {starts[i]}")
        else:
            run = 1
    print(f"preview {SID} {n} mots  chunks={len(scripts)}")


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

OPENING = [
    L("narrateur", "Le bois de la table fait tic au soleil."),
    L("narrateur", "Il sèche, sans personne."),
    L("narrateur", "Un pain tiède y pose son ventre."),
    L("narrateur", "Ça sent la croûte, près du nez."),
    L("narrateur", "Une mouche marche sur la mie."),
    L("narrateur", "Mila pose sa joue sur le bois."),
    L("enfant-f", "Il est chaud, maman."),
    L("maman", "Le pain vient du fournil."),
    L("narrateur", "Un seau jaune attend près du pied."),
    L("narrateur", "L'anse a un clou de cuivre."),
    L("narrateur", "Le clou cligne, une fois."),
    L("papa", "Tu as vu ce clou, Mila ?"),
    L("enfant-f", "Il brille, papa."),
    L("narrateur", "En ce moment, Mila veut le bac."),
    L("enfant-f", "Un gâteau de sable, vite !"),
    L("narrateur", "Elle tire le seau par l'anse."),
    L("narrateur", "Un pigeon se pose sur le pain."),
    L("narrateur", "Il pique une miette, nette."),
    L("enfant-f", "Oh !"),
    L("narrateur", "Mila sursaute."),
    L("narrateur", "Le seau roule sous la table."),
    L("narrateur", "Toc, contre le pied de bois."),
    L("narrateur", "Le clou de cuivre s'éteint, à l'ombre."),
    L("narrateur", "Une miette reste collée à l'anse."),
    L("enfant-f", "Il reste là, à l'abri."),
    L("papa", "On y va ?"),
    L("narrateur", "Mila pousse le seau plus loin."),
    L("narrateur", "Il ne roule plus."),
    L("narrateur", "Elle part, les mains vides."),
]

T1 = [
    L("narrateur", "Le square a trois coins, nets."),
    L("papa", "Le bac à sable."),
    L("papa", "Le toboggan."),
    L("maman", "Ou les balançoires ?"),
    L("maman", "Tu choisis."),
]

L1 = {
    1: [
        L("narrateur", "Mila s'agenouille près du bac."),
        L("narrateur", "Le sable est frais, un peu fin."),
        L("narrateur", "Il coule entre ses doigts."),
        L("enfant-f", "Un gâteau, maman."),
        L("maman", "Avec tes mains ?"),
        L("enfant-f", "Avec le seau !"),
        L("narrateur", "Elle court vers la table."),
        L("narrateur", "Elle tire l'anse, trop fort."),
        L("narrateur", "L'anse bute contre le pied."),
        L("narrateur", "Le seau recule, dans l'ombre."),
        L("enfant-f", "Il ne vient pas."),
        L("narrateur", "Le sourire de Mila disparaît."),
        L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
        L("papa", "On s'accroupit ?"),
        L("narrateur", "Papa se met à sa hauteur."),
        L("enfant-f", "Le clou, il est où ?"),
        L("maman", "Tu l'as vu, au départ."),
    ],
    2: [
        L("narrateur", "Mila grimpe la marche du toboggan."),
        L("narrateur", "Le plastique est lisse, un peu froid."),
        L("narrateur", "Une miette de pain y colle."),
        L("enfant-f", "Le seau glisse avec moi !"),
        L("papa", "Il est où, ce seau ?"),
        L("enfant-f", "Je le prends."),
        L("narrateur", "Elle redescend, trop vite."),
        L("narrateur", "Elle tire l'anse sous le bois."),
        L("narrateur", "L'anse bute, sèche."),
        L("narrateur", "Le seau recule, dans l'ombre."),
        L("enfant-f", "Zut."),
        L("narrateur", "Le sourire de Mila disparaît."),
        L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
        L("maman", "Je m'accroupis, d'accord ?"),
        L("narrateur", "Maman se met à sa hauteur."),
        L("enfant-f", "Le clou ne cligne plus."),
        L("papa", "Tu l'as vu, toi."),
    ],
    3: [
        L("narrateur", "Mila va vers les balançoires."),
        L("narrateur", "Une chaîne fait tic, mince."),
        L("narrateur", "Le siège rouge est tiède."),
        L("enfant-f", "Le seau s'assoit avec moi."),
        L("maman", "Il est resté où ?"),
        L("enfant-f", "Je le cherche."),
        L("narrateur", "Elle court, les mains ouvertes."),
        L("narrateur", "Elle tire l'anse d'un coup."),
        L("narrateur", "L'anse bute contre le pied."),
        L("narrateur", "Le seau recule, dans l'ombre."),
        L("enfant-f", "Il reste coincé."),
        L("narrateur", "Le sourire de Mila disparaît."),
        L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
        L("papa", "On s'accroupit ?"),
        L("narrateur", "Papa se met à sa hauteur."),
        L("enfant-f", "Le clou, il s'est tu."),
        L("maman", "Tu l'as entendu, au départ."),
    ],
}

Q = {
    1: [
        L("narrateur", "Mila a du sable aux doigts."),
        L("papa", "Le seau jaune est où ?"),
    ],
    2: [
        L("narrateur", "Mila a une miette au genou."),
        L("maman", "Le seau jaune est où ?"),
    ],
    3: [
        L("narrateur", "Mila a le vent dans les cheveux."),
        L("papa", "Le seau jaune est où ?"),
    ],
}

C = {
    1: [
        L("narrateur", "Mila regarde vers la table."),
        L("enfant-f", "Dessous."),
        L("papa", "Oui."),
        L("papa", "Sous la table."),
        L("maman", "Merci, Mila."),
        L("narrateur", "Un grain brille sur son genou."),
        L("papa", "On prend un jeu, près du bac ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Le pain tiède sent, loin."),
    ],
    2: [
        L("narrateur", "Mila montre la table du doigt."),
        L("enfant-f", "Dessous."),
        L("maman", "Oui."),
        L("maman", "Sous la table."),
        L("papa", "Merci, Mila."),
        L("narrateur", "La miette reste sur la marche."),
        L("maman", "On prend un jeu, près de la rampe ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Le plastique garde un peu de croûte."),
    ],
    3: [
        L("narrateur", "Mila se tourne vers la table."),
        L("enfant-f", "Dessous."),
        L("papa", "Oui."),
        L("papa", "Sous la table."),
        L("maman", "Merci, Mila."),
        L("narrateur", "La chaîne se tait, un instant."),
        L("papa", "On prend un jeu, près des chaînes ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Le vent touche son nez, froid."),
    ],
}

T2 = {
    1: [
        L("maman", "Quel jeu aide le gâteau ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    2: [
        L("papa", "Quel jeu aide la rampe ?"),
        L("maman", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    3: [
        L("maman", "Quel jeu aide la chaîne ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
}

# Revers allongé : 1re idée, patatras, 2e ruse, refuse de foncer, clou.
L2 = {
    (1, 1): [
        L("narrateur", "Près du bac, le ballon rouge attend."),
        L("narrateur", "Il est lisse, un peu frais."),
        L("enfant-f", "Il pousse le sable !"),
        L("narrateur", "Mila frappe trop fort."),
        L("narrateur", "Le ballon file sous la table."),
        L("enfant-f", "Le seau aussi ?"),
        L("narrateur", "Elle se jette à plat ventre."),
        L("narrateur", "Sa main trouve le cuir rouge."),
        L("narrateur", "Pas l'anse."),
        L("enfant-f", "Ce n'est pas lui."),
        L("narrateur", "La serviette du pain tombe, large."),
        L("narrateur", "Elle cache le clou de cuivre."),
        L("papa", "On tire tout ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Elle écoute le square."),
        L("narrateur", "Le pigeon reprend une miette, loin."),
        L("papa", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("narrateur", "Toc, très loin, sous le bois."),
        L("enfant-f", "Le clou."),
        L("maman", "Tu l'as entendu, toi."),
    ],
    (1, 2): [
        L("narrateur", "Mila revient vers la table."),
        L("narrateur", "L'ombre sous le plateau est froide."),
        L("enfant-f", "Le seau, maman."),
        L("narrateur", "Elle tire l'anse d'un coup."),
        L("narrateur", "L'anse bute, sèche, contre le pied."),
        L("enfant-f", "Il reste."),
        L("narrateur", "La serviette glisse du pain."),
        L("narrateur", "Elle tombe comme un rideau."),
        L("narrateur", "Le clou de cuivre disparaît."),
        L("enfant-f", "Je n'aime pas ça."),
        L("maman", "On s'accroupit ?"),
        L("narrateur", "Maman se met à sa hauteur."),
        L("papa", "Je tire, moi ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Elle observe le seau, dans le noir."),
        L("narrateur", "Elle écoute le bois."),
        L("papa", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("enfant-f", "Le toc du clou."),
        L("papa", "Tu l'as, ce son."),
    ],
    (1, 3): [
        L("narrateur", "Près du bac, le doudou gris attend."),
        L("narrateur", "Le tissu est chaud, un peu lourd."),
        L("enfant-f", "Il voit sous la table."),
        L("narrateur", "Mila le serre trop fort."),
        L("narrateur", "L'oreille grise cache l'ombre."),
        L("narrateur", "Elle cherche l'anse, à l'aveugle."),
        L("narrateur", "Sa main trouve le banc, pas le seau."),
        L("enfant-f", "Il n'est pas là."),
        L("narrateur", "Le sourire de Mila reste bas."),
        L("papa", "L'oreille, un peu de côté ?"),
        L("narrateur", "Papa se met à sa hauteur."),
        L("enfant-f", "J'attends."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Elle écarte l'oreille, lentement."),
        L("papa", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("narrateur", "Un toc minuscule, sous le bois."),
        L("enfant-f", "Le clou."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Un grain colle à l'oreille grise."),
    ],
    (2, 1): [
        L("narrateur", "Au pied du toboggan, le ballon attend."),
        L("narrateur", "Il est froid, près de la rampe."),
        L("enfant-f", "Il roule jusqu'au seau !"),
        L("narrateur", "Mila le lance trop fort."),
        L("narrateur", "Le ballon tape le pied de table."),
        L("narrateur", "Il rebondit, puis se cache."),
        L("enfant-f", "Avec le seau ?"),
        L("narrateur", "Elle rampe."),
        L("narrateur", "Sa main attrape le cuir, pas l'anse."),
        L("enfant-f", "Faux."),
        L("narrateur", "Une miette de marche tombe, large."),
        L("narrateur", "Elle colle au clou de cuivre."),
        L("maman", "On chasse tout ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Elle écoute le square."),
        L("maman", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("narrateur", "Toc, sous le plastique et le bois."),
        L("enfant-f", "Le clou est là."),
        L("papa", "Tu l'as trouvé, ce son."),
    ],
    (2, 2): [
        L("narrateur", "Mila revient vers la table."),
        L("narrateur", "Une miette brille sur la marche."),
        L("enfant-f", "Le seau, papa."),
        L("narrateur", "Elle tire, trop vite."),
        L("narrateur", "L'anse bute, sèche."),
        L("narrateur", "Le seau penche, puis recule."),
        L("enfant-f", "Il ne veut pas."),
        L("narrateur", "La serviette du pain tombe."),
        L("narrateur", "Elle cache le clou de cuivre."),
        L("papa", "Un coup sec ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Maman se met à sa hauteur."),
        L("narrateur", "Personne ne dit le lieu."),
        L("narrateur", "Mila observe le seau, dans l'ombre."),
        L("narrateur", "Elle écoute le bois."),
        L("papa", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("enfant-f", "Le toc du clou."),
        L("maman", "Tu l'as, ce bruit."),
        L("narrateur", "La miette reste sur le plastique."),
    ],
    (2, 3): [
        L("narrateur", "Au toboggan, le doudou a vu la rampe."),
        L("narrateur", "L'oreille grise est un peu froide."),
        L("enfant-f", "Il attrape le seau, en bas."),
        L("narrateur", "Mila glisse le doudou sous le bois."),
        L("narrateur", "Le tissu s'accroche au pied."),
        L("narrateur", "L'anse reste loin."),
        L("enfant-f", "Il est coincé, lui."),
        L("narrateur", "Le sourire de Mila disparaît."),
        L("papa", "On tire le tissu ?"),
        L("enfant-f", "Doucement."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Elle recule le doudou, un pouce."),
        L("narrateur", "Puis un autre."),
        L("papa", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("narrateur", "Un toc minuscule, sous le plateau."),
        L("enfant-f", "Le clou."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Papa se met à sa hauteur."),
        L("narrateur", "Une miette colle au ventre gris."),
    ],
    (3, 1): [
        L("narrateur", "Près des chaînes, le ballon rouge attend."),
        L("narrateur", "Il est lisse, un peu frais."),
        L("enfant-f", "Il roule sous la table !"),
        L("narrateur", "Mila pousse trop fort."),
        L("narrateur", "Le ballon rebondit une fois, mou."),
        L("narrateur", "Il se cache derrière le pied."),
        L("enfant-f", "Le seau aussi ?"),
        L("narrateur", "Elle rampe, le vent dans le dos."),
        L("narrateur", "Sa main trouve le cuir."),
        L("narrateur", "Pas l'anse jaune."),
        L("enfant-f", "Ce n'est pas lui."),
        L("maman", "On chasse le ballon ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Elle écoute le square."),
        L("narrateur", "La chaîne se tait."),
        L("maman", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("narrateur", "Toc, sous le bois, minuscule."),
        L("enfant-f", "Le clou."),
        L("papa", "Tu l'as entendu, toi."),
    ],
    (3, 2): [
        L("narrateur", "Mila revient vers la table."),
        L("narrateur", "Le vent a touché le pain."),
        L("enfant-f", "Le seau, maman."),
        L("narrateur", "Elle tire l'anse d'un coup."),
        L("narrateur", "L'anse bute contre le pied."),
        L("enfant-f", "Il reste."),
        L("narrateur", "Le manteau rouge bouge au dossier."),
        L("narrateur", "Une manche tombe, large."),
        L("narrateur", "Elle cache le clou de cuivre."),
        L("papa", "On soulève tout ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Maman se met à sa hauteur."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Mila observe le seau, dans l'ombre."),
        L("narrateur", "Elle écoute le bois."),
        L("papa", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("enfant-f", "Le toc du clou."),
        L("maman", "Tu l'as, ce son."),
        L("narrateur", "La chaîne reste muette, derrière."),
    ],
    (3, 3): [
        L("narrateur", "Près des balançoires, le doudou gris attend."),
        L("narrateur", "Le tissu a pris le vent."),
        L("enfant-f", "Il cherche le seau, avec moi."),
        L("narrateur", "Mila le serre contre sa joue."),
        L("narrateur", "L'oreille grise cache l'ombre."),
        L("narrateur", "Elle cherche l'anse, trop vite."),
        L("narrateur", "Sa main trouve le banc de pierre."),
        L("enfant-f", "Pas lui."),
        L("narrateur", "Le sourire de Mila reste bas."),
        L("papa", "L'oreille, un peu de côté ?"),
        L("narrateur", "Papa se met à sa hauteur."),
        L("enfant-f", "J'attends."),
        L("narrateur", "Mila refuse de foncer."),
        L("narrateur", "Elle écarte l'oreille, lentement."),
        L("papa", "C'est l'heure, presque."),
        L("enfant-f", "Pas sans le toc."),
        L("narrateur", "Un toc minuscule, sous le bois."),
        L("enfant-f", "Le clou."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "L'oreille du doudou est froide."),
    ],
}

T3 = {
    1: [
        L("papa", "C'est l'heure."),
        L("maman", "Le manteau, le seau, ou le doudou ?"),
        L("narrateur", "Tu commences par quoi ?"),
    ],
    2: [
        L("maman", "Le pain refroidit."),
        L("papa", "Le manteau, le seau, ou le doudou ?"),
        L("narrateur", "Tu commences par quoi ?"),
    ],
    3: [
        L("papa", "Le pigeon revient, presque."),
        L("maman", "Le manteau, le seau, ou le doudou ?"),
        L("narrateur", "Tu commences par quoi ?"),
    ],
}

# 27 résolutions distinctes — le clou se paie, le seau faillit rester.
L3 = {
    (1, 1, 1): [
        L("narrateur", "Mila va vers le dossier."),
        L("narrateur", "Le manteau rouge est tiède."),
        L("enfant-f", "Lui d'abord."),
        L("narrateur", "Elle l'enfile, une manche, puis l'autre."),
        L("narrateur", "La manche tombe devant l'ombre."),
        L("papa", "On y va, Mila ?"),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle relève la manche, sans tirer."),
        L("narrateur", "Le clou de cuivre cligne, à peine."),
        L("enfant-f", "Le seau !"),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, un grain au fond."),
        L("maman", "Tu l'as, sans foncer."),
        L("narrateur", "Le ballon rouge reste contre sa jambe."),
        L("narrateur", "Le doudou attend sur le banc."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle le serre, le seau à l'autre main."),
    ],
    (1, 1, 2): [
        L("narrateur", "Mila se penche sous la table."),
        L("narrateur", "L'ombre est froide, un peu rêche."),
        L("papa", "Le pain part, tout à l'heure."),
        L("enfant-f", "J'écoute."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Elle observe le seau, dans le noir."),
        L("narrateur", "Le clou de cuivre cligne, minuscule."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse l'anse, sans à-coup."),
        L("narrateur", "Le seau sort, toc, contre le bois."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Le ballon roule contre l'anse."),
        L("narrateur", "Le manteau reste au dossier."),
        L("enfant-f", "Lui, après."),
        L("narrateur", "Elle le prend, puis le doudou du banc."),
        L("papa", "Les trois, avec toi."),
    ],
    (1, 1, 3): [
        L("narrateur", "Mila va vers le banc de pierre."),
        L("narrateur", "Le doudou gris montre une oreille."),
        L("enfant-f", "Toi, tu viens."),
        L("narrateur", "Elle le serre, trop près de l'ombre."),
        L("narrateur", "L'oreille cache le clou de cuivre."),
        L("maman", "On rentre ?"),
        L("enfant-f", "Pas sans lui."),
        L("narrateur", "Elle écarte l'oreille, un pouce."),
        L("narrateur", "Le clou cligne, pâle."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, un grain au fond."),
        L("papa", "Tu l'as, avec l'oreille."),
        L("narrateur", "Le ballon tape le ventre gris."),
        L("narrateur", "Le manteau rouge attend au dossier."),
        L("enfant-f", "Lui aussi."),
    ],
    (1, 2, 1): [
        L("narrateur", "Mila prend le manteau au dossier."),
        L("narrateur", "Il sent le pain, un peu."),
        L("enfant-f", "Chaud."),
        L("narrateur", "La manche tombe sur la serviette."),
        L("narrateur", "L'ombre s'épaissit."),
        L("papa", "Le fournil va fermer."),
        L("enfant-f", "J'attends le toc."),
        L("narrateur", "Elle relève la manche."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans tirer fort."),
        L("narrateur", "Le seau sort, du sable au fond."),
        L("maman", "Tu l'as, après le manteau."),
        L("narrateur", "Le doudou reste sur le banc."),
        L("enfant-f", "Toi, viens."),
        L("narrateur", "Elle le serre contre le rouge."),
    ],
    (1, 2, 2): [
        L("narrateur", "Mila s'accroupit sous le plateau."),
        L("narrateur", "La serviette touche son nez."),
        L("papa", "On y va ?"),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle écarte le linge, un doigt."),
        L("narrateur", "Personne ne dit le lieu."),
        L("narrateur", "Le clou de cuivre cligne, à l'ombre."),
        L("enfant-f", "Toi, je te vois."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, toc, contre le pied."),
        L("maman", "Tu l'as, sans foncer."),
        L("narrateur", "Un grain tombe sur le bois."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Puis le doudou du banc."),
        L("papa", "Les trois rentrent."),
    ],
    (1, 2, 3): [
        L("narrateur", "Mila prend le doudou sur le banc."),
        L("narrateur", "Il sent le sable, un peu."),
        L("enfant-f", "On cherche ensemble."),
        L("narrateur", "L'oreille passe sous la table."),
        L("narrateur", "Elle touche le clou de cuivre."),
        L("maman", "Le pain refroidit."),
        L("enfant-f", "Je le tiens."),
        L("narrateur", "Elle glisse l'anse, avec l'oreille."),
        L("narrateur", "Le seau sort, un grain au fond."),
        L("papa", "Tu l'as, tous les deux."),
        L("narrateur", "Le doudou tapote le bord jaune."),
        L("narrateur", "Le manteau rouge attend."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, le seau à la main."),
        L("maman", "Tu as tout, Mila."),
    ],
    (1, 3, 1): [
        L("narrateur", "Mila enfile le manteau rouge."),
        L("narrateur", "Le doudou reste contre son ventre."),
        L("enfant-f", "On est trois."),
        L("narrateur", "La manche cache l'ombre, large."),
        L("papa", "Le square se vide."),
        L("enfant-f", "Pas sans le seau."),
        L("narrateur", "Elle relève la manche, un pouce."),
        L("narrateur", "Le clou de cuivre cligne, pâle."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, du sable au fond."),
        L("maman", "Tu l'as, avec le doudou."),
        L("narrateur", "L'oreille grise a un grain, fin."),
        L("papa", "Les trois, près du pain."),
    ],
    (1, 3, 2): [
        L("narrateur", "Mila se penche, le doudou au bras."),
        L("narrateur", "L'ombre sent le pain froid."),
        L("papa", "On rentre, ma puce ?"),
        L("enfant-f", "J'écoute le clou."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Le clou de cuivre cligne, minuscule."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans à-coup."),
        L("narrateur", "Le seau sort, toc."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Le doudou regarde au fond du seau."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Elle le prend, le seau à l'autre main."),
        L("papa", "Tout est là."),
    ],
    (1, 3, 3): [
        L("narrateur", "Mila serre le doudou plus fort."),
        L("narrateur", "Une miette colle à l'oreille."),
        L("enfant-f", "Toi, tu restes."),
        L("narrateur", "Elle s'accroupit, l'oreille de côté."),
        L("maman", "Le fournil ferme, bientôt."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Le seau !"),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, un grain au fond."),
        L("papa", "Tu l'as, sans foncer."),
        L("narrateur", "Le manteau rouge attend au dossier."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, le doudou contre elle."),
        L("maman", "Les trois rentrent."),
    ],
    (2, 1, 1): [
        L("narrateur", "Mila prend le manteau au dossier."),
        L("narrateur", "Une miette de marche y colle."),
        L("enfant-f", "Tiède."),
        L("narrateur", "Elle l'enfile, le ballon sous le bras."),
        L("narrateur", "La manche tombe sur la rampe, loin."),
        L("papa", "On y va ?"),
        L("enfant-f", "Le clou, d'abord."),
        L("narrateur", "Elle se penche, la manche relevée."),
        L("narrateur", "Le clou de cuivre cligne, pâle."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans tirer fort."),
        L("narrateur", "Le seau sort, toc, contre le bois."),
        L("maman", "Tu l'as, après le manteau."),
        L("narrateur", "Le doudou attend sur le banc."),
        L("enfant-f", "Toi, viens."),
        L("narrateur", "Le ballon s'appuie contre l'anse."),
    ],
    (2, 1, 2): [
        L("narrateur", "Mila pose le ballon près du pied."),
        L("narrateur", "Elle s'accroupit sous le plateau."),
        L("papa", "La rampe sèche."),
        L("enfant-f", "J'écoute."),
        L("narrateur", "Personne ne dit le lieu."),
        L("narrateur", "Le clou de cuivre cligne, minuscule."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, une miette au bord."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Le ballon tape l'anse, mou."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Puis le doudou du banc."),
        L("papa", "Les trois, avec la miette."),
    ],
    (2, 1, 3): [
        L("narrateur", "Mila va vers le banc, le ballon au bras."),
        L("narrateur", "Le doudou gris attend, une oreille."),
        L("enfant-f", "Toi, tu viens."),
        L("narrateur", "Le ballon frotte le ventre gris."),
        L("maman", "On rentre ?"),
        L("enfant-f", "Pas sans le seau."),
        L("narrateur", "Elle écarte l'oreille, un pouce."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, toc."),
        L("papa", "Tu l'as, avec eux."),
        L("narrateur", "Le manteau rouge attend."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, les bras pleins."),
    ],
    (2, 2, 1): [
        L("narrateur", "Mila enfile le manteau, près de la rampe."),
        L("narrateur", "L'anse du seau a buté, tout à l'heure."),
        L("enfant-f", "Pas cette fois."),
        L("narrateur", "La manche tombe, large."),
        L("papa", "Le fournil ferme."),
        L("enfant-f", "J'attends le toc."),
        L("narrateur", "Elle relève la manche."),
        L("narrateur", "Le clou de cuivre cligne, à l'ombre."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans à-coup."),
        L("narrateur", "Le seau sort, du sable au fond."),
        L("maman", "Tu l'as, après le rouge."),
        L("narrateur", "Le doudou attend sur le banc."),
        L("enfant-f", "Toi."),
        L("narrateur", "L'anse frotte le manteau, clou au chaud."),
    ],
    (2, 2, 2): [
        L("narrateur", "Mila s'accroupit, la miette au genou."),
        L("narrateur", "La serviette touche son front."),
        L("papa", "On y va, Mila ?"),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle écarte le linge, un doigt."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Le clou de cuivre cligne, pâle."),
        L("enfant-f", "Toi, je te vois."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, toc, contre le pied."),
        L("maman", "Tu l'as, sans foncer."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Puis le doudou du banc."),
        L("papa", "Les trois rentrent."),
        L("narrateur", "Une miette brille au bord du seau."),
    ],
    (2, 2, 3): [
        L("narrateur", "Mila prend le doudou, près de la rampe."),
        L("narrateur", "Une miette colle au ventre gris."),
        L("enfant-f", "On cherche le toc."),
        L("narrateur", "L'oreille passe sous le bois."),
        L("maman", "Le pain refroidit."),
        L("enfant-f", "Je le tiens."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, avec l'oreille."),
        L("narrateur", "Le seau sort, un grain au fond."),
        L("papa", "Tu l'as, tous les deux."),
        L("narrateur", "Le manteau rouge attend."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, le seau à la main."),
        L("maman", "Tu as tout."),
    ],
    (2, 3, 1): [
        L("narrateur", "Mila enfile le manteau, le doudou au ventre."),
        L("narrateur", "La marche du toboggan sèche."),
        L("enfant-f", "On est prêts, presque."),
        L("narrateur", "La manche cache l'ombre."),
        L("papa", "Le square se vide."),
        L("enfant-f", "Pas sans le seau."),
        L("narrateur", "Elle relève la manche, un pouce."),
        L("narrateur", "Le clou de cuivre cligne, pâle."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, toc."),
        L("maman", "Tu l'as, avec le doudou."),
        L("narrateur", "L'oreille a senti la marche lisse."),
        L("papa", "Les trois, près du pain."),
    ],
    (2, 3, 2): [
        L("narrateur", "Mila se penche, le doudou au bras."),
        L("narrateur", "L'ombre sent le plastique froid."),
        L("papa", "On rentre ?"),
        L("enfant-f", "J'écoute le clou."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Le clou de cuivre cligne, minuscule."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans à-coup."),
        L("narrateur", "Le seau sort, toc."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Le doudou touche le clou, froid."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Elle le prend, le seau à l'autre main."),
        L("papa", "Tout est là."),
    ],
    (2, 3, 3): [
        L("narrateur", "Mila serre le doudou, près du banc."),
        L("narrateur", "L'oreille a pris le vent de la rampe."),
        L("enfant-f", "Toi, tu restes."),
        L("narrateur", "Elle s'accroupit, l'oreille de côté."),
        L("maman", "Le pigeon revient, presque."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Le seau !"),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, un grain au fond."),
        L("papa", "Tu l'as, sans foncer."),
        L("narrateur", "Le manteau rouge attend au dossier."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, le doudou contre elle."),
        L("maman", "Les trois rentrent."),
    ],
    (3, 1, 1): [
        L("narrateur", "Mila prend le manteau au dossier."),
        L("narrateur", "Un brin d'herbe y colle, mince."),
        L("enfant-f", "Il a vu la chaîne."),
        L("narrateur", "Elle l'enfile, le ballon sous le bras."),
        L("narrateur", "La manche tombe, large."),
        L("papa", "On y va ?"),
        L("enfant-f", "Le clou, d'abord."),
        L("narrateur", "Elle se penche, la manche relevée."),
        L("narrateur", "Le clou de cuivre cligne, pâle."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans tirer fort."),
        L("narrateur", "Le seau sort, toc, contre le bois."),
        L("maman", "Tu l'as, après le manteau."),
        L("narrateur", "Le doudou attend sur le banc."),
        L("enfant-f", "Toi, viens."),
        L("narrateur", "Le ballon a gardé le vent."),
    ],
    (3, 1, 2): [
        L("narrateur", "Mila pose le ballon près du pied."),
        L("narrateur", "Elle s'accroupit sous le plateau."),
        L("papa", "La chaîne se tait."),
        L("enfant-f", "J'écoute."),
        L("narrateur", "Personne ne dit le lieu."),
        L("narrateur", "Le clou de cuivre cligne, minuscule."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, un brin d'herbe au bord."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Le ballon tape l'anse, mou."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Puis le doudou du banc."),
        L("papa", "Les trois, avec le vent."),
    ],
    (3, 1, 3): [
        L("narrateur", "Mila va vers le banc, le ballon au bras."),
        L("narrateur", "Le doudou gris a pris le vent."),
        L("enfant-f", "Toi, tu viens."),
        L("narrateur", "Le ballon frotte l'oreille grise."),
        L("maman", "On rentre ?"),
        L("enfant-f", "Pas sans le seau."),
        L("narrateur", "Elle écarte l'oreille, un pouce."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, toc."),
        L("papa", "Tu l'as, avec eux."),
        L("narrateur", "Le manteau rouge attend."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, les bras pleins."),
        L("narrateur", "Le clou de cuivre a vu le siège vide."),
    ],
    (3, 2, 1): [
        L("narrateur", "Mila enfile le manteau, près des chaînes."),
        L("narrateur", "Du sable de l'anse reste dans l'herbe."),
        L("enfant-f", "Pas cette fois, trop vite."),
        L("narrateur", "La manche tombe, large."),
        L("papa", "Le fournil ferme."),
        L("enfant-f", "J'attends le toc."),
        L("narrateur", "Elle relève la manche."),
        L("narrateur", "Le clou de cuivre cligne, à l'ombre."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans à-coup."),
        L("narrateur", "Le seau sort, de l'herbe au fond."),
        L("maman", "Tu l'as, après le rouge."),
        L("narrateur", "Le doudou attend sur le banc."),
        L("enfant-f", "Toi."),
        L("narrateur", "L'anse frotte le manteau, froide."),
    ],
    (3, 2, 2): [
        L("narrateur", "Mila s'accroupit, le vent dans le dos."),
        L("narrateur", "La manche du manteau touche son nez."),
        L("papa", "On y va, Mila ?"),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle écarte le tissu, un doigt."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Le clou de cuivre cligne, pâle."),
        L("enfant-f", "Toi, je te vois."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, toc, contre le pied."),
        L("maman", "Tu l'as, sans foncer."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Puis le doudou du banc."),
        L("papa", "Les trois rentrent."),
        L("narrateur", "L'anse du seau est froide, clou pâle."),
    ],
    (3, 2, 3): [
        L("narrateur", "Mila prend le doudou, près des chaînes."),
        L("narrateur", "L'oreille a pris le vent."),
        L("enfant-f", "On cherche le toc."),
        L("narrateur", "L'oreille passe sous le bois."),
        L("maman", "Le pain refroidit."),
        L("enfant-f", "Je le tiens."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, avec l'oreille."),
        L("narrateur", "Le seau sort, un brin d'herbe au fond."),
        L("papa", "Tu l'as, tous les deux."),
        L("narrateur", "Le manteau rouge attend."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, le seau à la main."),
        L("maman", "Tu as tout."),
        L("narrateur", "Le seau tapote le banc, toc de cuivre."),
    ],
    (3, 3, 1): [
        L("narrateur", "Mila enfile le manteau, le doudou au ventre."),
        L("narrateur", "L'oreille du doudou a pris le vent."),
        L("enfant-f", "On est prêts, presque."),
        L("narrateur", "La manche cache l'ombre."),
        L("papa", "Le square se vide."),
        L("enfant-f", "Pas sans le seau."),
        L("narrateur", "Elle relève la manche, un pouce."),
        L("narrateur", "Le clou de cuivre cligne, pâle."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, toc."),
        L("maman", "Tu l'as, avec le doudou."),
        L("narrateur", "Un brin d'herbe colle au rouge."),
        L("papa", "Les trois, près du pain."),
    ],
    (3, 3, 2): [
        L("narrateur", "Mila se penche, le doudou au bras."),
        L("narrateur", "L'ombre sent l'herbe froide."),
        L("papa", "On rentre ?"),
        L("enfant-f", "J'écoute le clou."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Le clou de cuivre cligne, minuscule."),
        L("enfant-f", "Le seau."),
        L("narrateur", "Elle glisse l'anse, sans à-coup."),
        L("narrateur", "Le seau sort, toc."),
        L("maman", "Tu l'as entendu, seule."),
        L("narrateur", "Le doudou sent le sable du seau."),
        L("narrateur", "Le manteau attend au dossier."),
        L("enfant-f", "Lui."),
        L("narrateur", "Elle le prend, le seau à l'autre main."),
        L("papa", "Tout est là."),
    ],
    (3, 3, 3): [
        L("narrateur", "Mila serre le doudou, près du banc."),
        L("narrateur", "L'oreille a quitté la chaîne."),
        L("enfant-f", "Toi, tu restes."),
        L("narrateur", "Elle s'accroupit, l'oreille de côté."),
        L("maman", "Le pigeon a presque le pain."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Le clou de cuivre cligne, net."),
        L("enfant-f", "Le seau !"),
        L("narrateur", "Elle glisse l'anse, tout droit."),
        L("narrateur", "Le seau sort, un grain au fond."),
        L("papa", "Tu l'as, sans foncer."),
        L("narrateur", "Le manteau rouge attend au dossier."),
        L("enfant-f", "Lui aussi."),
        L("narrateur", "Elle l'enfile, le doudou contre elle."),
        L("maman", "Les trois rentrent."),
        L("narrateur", "Plus rien n'attend sur le banc de pierre."),
    ],
}

FIN = {
    (1, 1, 1): [
        L("narrateur", "Mila a le manteau sur le bras."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Oui."),
        L("papa", "Sous la table."),
        L("maman", "On rentre."),
        L("narrateur", "Le pain n'est plus tiède."),
        L("enfant-f", "Le clou est là, sur l'anse."),
        L("papa", "Tu l'as attendu."),
        L("narrateur", "Le ballon a un peu de sable."),
        L("narrateur", "Le clou de cuivre dort dans la poche du manteau."),
    ],
    (1, 1, 2): [
        L("narrateur", "Mila tient le seau par l'anse."),
        L("enfant-f", "Il a failli rester."),
        L("maman", "Une seconde de plus."),
        L("papa", "Sous la table, oui."),
        L("narrateur", "Le pain a perdu sa chaleur."),
        L("enfant-f", "Le clou a cligné, à la fin."),
        L("maman", "Tu l'as vu, seule."),
        L("narrateur", "Le ballon roule contre l'anse, une fois."),
        L("narrateur", "Sous la table, l'ombre n'a plus de seau."),
        L("narrateur", "Le clou de cuivre tape l'anse, toc."),
    ],
    (1, 1, 3): [
        L("narrateur", "Mila serre le doudou contre elle."),
        L("enfant-f", "L'oreille a vu le clou."),
        L("papa", "Oui."),
        L("maman", "On rentre."),
        L("narrateur", "Le pain est froid, sur le bois."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Tu l'as pris, sans foncer."),
        L("narrateur", "Le ballon frotte l'oreille du doudou."),
        L("narrateur", "Une miette reste sur le bois."),
        L("narrateur", "Le clou de cuivre a frotté l'oreille grise."),
    ],
    (1, 2, 1): [
        L("narrateur", "Le seau tape le manteau, tout bas."),
        L("enfant-f", "Du sable, pour plus tard."),
        L("maman", "Le gâteau attendra."),
        L("papa", "Le fournil a fermé."),
        L("narrateur", "Le dossier est vide."),
        L("enfant-f", "Le clou est chaud, dans le rouge."),
        L("papa", "Tu l'as, après le manteau."),
        L("narrateur", "Du sable du seau colle au manteau."),
        L("narrateur", "Une miette de pain colle au clou de cuivre."),
    ],
    (1, 2, 2): [
        L("narrateur", "Le seau jaune a du sable au fond."),
        L("enfant-f", "Il a failli rester."),
        L("papa", "La serviette tombait."),
        L("maman", "Tu as écarté le linge."),
        L("narrateur", "Sous la table, plus rien."),
        L("enfant-f", "Le clou a cligné, à peine."),
        L("papa", "Tu l'as vu, seule."),
        L("narrateur", "Un grain brille, au fond du seau."),
        L("narrateur", "Le pain froid garde une mouche, loin."),
        L("narrateur", "Sous la table, l'ombre n'a plus de seau."),
    ],
    (1, 2, 3): [
        L("narrateur", "Le seau et le doudou se touchent."),
        L("enfant-f", "L'oreille a touché le clou."),
        L("maman", "Oui."),
        L("papa", "On rentre."),
        L("narrateur", "Le banc de pierre est vide."),
        L("enfant-f", "Le seau était dessous."),
        L("maman", "Tu l'as tenu, tous les deux."),
        L("narrateur", "Le seau tapote le ventre du doudou."),
        L("narrateur", "Le clou de cuivre a une miette, plate."),
    ],
    (1, 3, 1): [
        L("narrateur", "Le doudou frotte le manteau rouge."),
        L("enfant-f", "On est trois, plus le seau."),
        L("papa", "Quatre, avec le clou."),
        L("maman", "On rentre."),
        L("narrateur", "Le pain est froid."),
        L("enfant-f", "Le clou a cligné, sous la manche."),
        L("papa", "Tu as relevé le tissu."),
        L("narrateur", "L'oreille grise a un grain, fin."),
        L("narrateur", "Le carré de soleil a glissé du bois."),
    ],
    (1, 3, 2): [
        L("narrateur", "Le doudou regarde au fond du seau."),
        L("enfant-f", "Un grain, pour le gâteau."),
        L("maman", "Plus tard."),
        L("papa", "Le fournil a fermé."),
        L("narrateur", "L'ombre de la table est vide."),
        L("enfant-f", "Le clou a parlé, toc."),
        L("maman", "Tu l'as écouté, seule."),
        L("narrateur", "Le doudou a vu le clou, à l'ombre."),
        L("narrateur", "Un grain brille sur le bois, oublié."),
    ],
    (1, 3, 3): [
        L("narrateur", "Le doudou a une miette sur l'oreille."),
        L("enfant-f", "Du pain, pour lui."),
        L("papa", "Et le seau, pour toi."),
        L("maman", "On rentre."),
        L("narrateur", "Le pigeon a quitté le plateau."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Tu l'as pris, sans foncer."),
        L("narrateur", "Une miette reste sur le banc de pierre."),
        L("narrateur", "Le clou de cuivre a gardé sa miette, plate."),
    ],
    (2, 1, 1): [
        L("narrateur", "Une miette de marche colle au manteau."),
        L("enfant-f", "La rampe, c'était lisse."),
        L("papa", "Oui."),
        L("maman", "On rentre."),
        L("narrateur", "Le pain n'a plus de mouche."),
        L("enfant-f", "Le clou est dans la poche."),
        L("papa", "Tu l'as attendu."),
        L("narrateur", "Le ballon a touché l'anse, une fois."),
        L("narrateur", "Une miette de marche sèche sur le manteau."),
    ],
    (2, 1, 2): [
        L("narrateur", "Le ballon s'appuie contre le seau."),
        L("enfant-f", "Il a failli prendre sa place."),
        L("maman", "Le cuir, pas l'anse."),
        L("papa", "Tu as écouté le toc."),
        L("narrateur", "Le soleil a quitté la table."),
        L("enfant-f", "Le clou a cligné, à la fin."),
        L("maman", "Tu l'as vu, seule."),
        L("narrateur", "Le ballon a touché le clou de cuivre."),
        L("narrateur", "La marche du toboggan sèche, vide."),
    ],
    (2, 1, 3): [
        L("narrateur", "Le ballon et le doudou rentrent."),
        L("enfant-f", "L'oreille a vu le clou."),
        L("papa", "Oui."),
        L("maman", "On rentre."),
        L("narrateur", "Une miette sèche sur la pierre."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Tu l'as pris, avec eux."),
        L("narrateur", "Le ballon s'appuie contre le doudou gris."),
        L("narrateur", "Le clou de cuivre a une miette de rampe."),
    ],
    (2, 2, 1): [
        L("narrateur", "L'anse du seau tient le manteau."),
        L("enfant-f", "Chaud, le rouge."),
        L("maman", "Le clou aussi."),
        L("papa", "Le fournil a fermé."),
        L("narrateur", "Le manteau n'est plus au dossier."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Tu as attendu le toc."),
        L("narrateur", "L'anse du seau frotte le manteau rouge."),
        L("narrateur", "Une miette de rampe sèche sur le clou."),
    ],
    (2, 2, 2): [
        L("narrateur", "Le seau sonne, près du pain froid."),
        L("enfant-f", "Il a failli rester."),
        L("papa", "La serviette tombait."),
        L("maman", "Tu as écarté le linge."),
        L("narrateur", "L'anse jaune ne traîne plus."),
        L("enfant-f", "Le clou a cligné, à peine."),
        L("papa", "Tu l'as vu, seule."),
        L("narrateur", "Le seau sonne contre le pain froid."),
        L("narrateur", "Sous la table, l'ombre est vide, nette."),
    ],
    (2, 2, 3): [
        L("narrateur", "Une miette brille au bord du seau."),
        L("enfant-f", "L'oreille l'a vue."),
        L("maman", "Oui."),
        L("papa", "On rentre."),
        L("narrateur", "Le doudou n'est plus au banc."),
        L("enfant-f", "Le seau était dessous."),
        L("maman", "Tu l'as tenu, tous les deux."),
        L("narrateur", "Le seau a une miette sur le bord."),
        L("narrateur", "Le clou de cuivre a gardé la croûte."),
    ],
    (2, 3, 1): [
        L("narrateur", "Le doudou a senti la marche froide."),
        L("enfant-f", "Lisse, la rampe."),
        L("papa", "Oui."),
        L("maman", "On rentre."),
        L("narrateur", "Le dossier reste vide."),
        L("enfant-f", "Le clou a cligné, sous la manche."),
        L("papa", "Tu as relevé le tissu."),
        L("narrateur", "Le doudou a senti la marche lisse."),
        L("narrateur", "Le pain froid garde sa forme, seule."),
    ],
    (2, 3, 2): [
        L("narrateur", "Le doudou touche l'anse du seau."),
        L("enfant-f", "Le clou est froid."),
        L("maman", "Il était à l'ombre."),
        L("papa", "Le fournil a fermé."),
        L("narrateur", "Sous la table, l'ombre est vide."),
        L("enfant-f", "Le clou a parlé, toc."),
        L("maman", "Tu l'as écouté, seule."),
        L("narrateur", "Le doudou touche le clou, tout froid."),
        L("narrateur", "Une miette de rampe sèche sur le bois."),
    ],
    (2, 3, 3): [
        L("narrateur", "Le doudou rentre, l'oreille au vent."),
        L("enfant-f", "Le pigeon est parti."),
        L("papa", "Le pain aussi, presque."),
        L("maman", "On rentre."),
        L("narrateur", "Le doudou n'est plus au banc."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Tu l'as pris, sans foncer."),
        L("narrateur", "Le pigeon a quitté le pain."),
        L("narrateur", "Le clou de cuivre a une miette de rampe, plate."),
    ],
    (3, 1, 1): [
        L("narrateur", "Un brin d'herbe colle au manteau."),
        L("enfant-f", "La chaîne, c'était le vent."),
        L("papa", "Oui."),
        L("maman", "On rentre."),
        L("narrateur", "La chaîne ne fait plus tic."),
        L("enfant-f", "Le clou est dans la poche."),
        L("papa", "Tu l'as attendu."),
        L("narrateur", "Un brin d'herbe colle au manteau rouge."),
        L("narrateur", "Le siège rouge est vide, au soleil."),
    ],
    (3, 1, 2): [
        L("narrateur", "Le ballon a gardé le vent des chaînes."),
        L("enfant-f", "Il a failli prendre sa place."),
        L("maman", "Le cuir, pas l'anse."),
        L("papa", "Tu as écouté le toc."),
        L("narrateur", "Le vent a quitté le pain."),
        L("enfant-f", "Le clou a cligné, à la fin."),
        L("maman", "Tu l'as vu, seule."),
        L("narrateur", "Le ballon a gardé le vent des chaînes."),
        L("narrateur", "Le clou de cuivre a un brin d'herbe, mince."),
    ],
    (3, 1, 3): [
        L("narrateur", "Le ballon frotte le doudou, près du banc."),
        L("enfant-f", "L'oreille a vu le clou."),
        L("papa", "Oui."),
        L("maman", "On rentre."),
        L("narrateur", "Le siège rouge est vide."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Tu l'as pris, avec eux."),
        L("narrateur", "Le ballon frotte la feuille du banc."),
        L("narrateur", "Le clou de cuivre a vu le siège vide."),
    ],
    (3, 2, 1): [
        L("narrateur", "Le seau a un peu d'herbe au fond."),
        L("enfant-f", "Pour plus tard."),
        L("maman", "Le gâteau attendra."),
        L("papa", "Le fournil a fermé."),
        L("narrateur", "L'herbe a un peu de sable."),
        L("enfant-f", "Le clou est chaud, dans le rouge."),
        L("papa", "Tu l'as, après le manteau."),
        L("narrateur", "Du sable du seau reste dans l'herbe."),
        L("narrateur", "La chaîne reste muette, derrière eux."),
    ],
    (3, 2, 2): [
        L("narrateur", "L'anse du seau est froide, clou pâle."),
        L("enfant-f", "Il a failli rester."),
        L("papa", "La manche tombait."),
        L("maman", "Tu as écarté le tissu."),
        L("narrateur", "La table n'a plus de seau."),
        L("enfant-f", "Le clou a cligné, à peine."),
        L("papa", "Tu l'as vu, seule."),
        L("narrateur", "L'anse du seau est froide, clou pâle."),
        L("narrateur", "Le vent a quitté le pain tiède."),
    ],
    (3, 2, 3): [
        L("narrateur", "Le seau tapote le doudou, toc."),
        L("enfant-f", "L'oreille a touché le clou."),
        L("maman", "Oui."),
        L("papa", "On rentre."),
        L("narrateur", "Le banc de pierre est calme."),
        L("enfant-f", "Le seau était dessous."),
        L("maman", "Tu l'as tenu, tous les deux."),
        L("narrateur", "Le seau tapote le banc, toc de cuivre."),
        L("narrateur", "Un brin d'herbe reste au bord jaune."),
    ],
    (3, 3, 1): [
        L("narrateur", "L'oreille du doudou a pris l'herbe."),
        L("enfant-f", "Et le vent."),
        L("papa", "Oui."),
        L("maman", "On rentre."),
        L("narrateur", "Le manteau a quitté le dossier."),
        L("enfant-f", "Le clou a cligné, sous la manche."),
        L("papa", "Tu as relevé le tissu."),
        L("narrateur", "L'oreille du doudou a pris le vent."),
        L("narrateur", "Un brin d'herbe colle au rouge, mince."),
    ],
    (3, 3, 2): [
        L("narrateur", "Le doudou sent le sable du seau."),
        L("enfant-f", "Un grain, pour le gâteau."),
        L("maman", "Plus tard."),
        L("papa", "Le fournil a fermé."),
        L("narrateur", "Le seau a quitté l'ombre."),
        L("enfant-f", "Le clou a parlé, toc."),
        L("maman", "Tu l'as écouté, seule."),
        L("narrateur", "Le doudou sent le sable du seau."),
        L("narrateur", "La chaîne ne fait plus tic, derrière."),
    ],
    (3, 3, 3): [
        L("narrateur", "Le doudou a quitté la chaîne."),
        L("enfant-f", "Le pigeon a presque eu le pain."),
        L("papa", "Presque."),
        L("maman", "On rentre."),
        L("narrateur", "Plus rien n'attend sur le banc."),
        L("enfant-f", "Le seau était dessous."),
        L("papa", "Tu l'as pris, sans foncer."),
        L("narrateur", "Plus rien n'attend sur le banc de pierre."),
        L("narrateur", "Le pigeon a laissé le pain, intact."),
    ],
}

Q_FIELDS = {
    "expected_answer": "table",
    "accepted_examples": "table | sous la table | dessous | le seau | seau | sous la table",
    "retry_prompt": "Le seau jaune. Il est où ?",
}

SONS_L1 = {1: "enfants_parc,sable", 2: "enfants_parc,toboggan", 3: "enfants_parc,chaine"}
SONS_L2 = {1: "ballon,table", 2: "seau,bois", 3: "doudou,tissu"}
SONS_L3 = {1: "manteau,tissu", 2: "seau,table", 3: "doudou,banc"}
SONS_FIN = {1: "pas,pain", 2: "seau,pain", 3: "doudou,pas"}


def build() -> tuple[dict[str, list[str]], dict[str, dict]]:
    s: dict[str, list[str]] = {}
    meta: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = OPENING
    s["CHK_T0001_P0000"] = T1
    meta["CHK_T0001_P0000"] = {
        "option_1_label": "le bac à sable",
        "option_2_label": "le toboggan",
        "option_3_label": "les balançoires",
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1[i]
        s[f"{p}_Q0001"] = Q[i]
        s[f"{p}_C0001"] = C[i]
        s[f"{p}_T0002_P0000"] = T2[i]
        meta[f"{p}_T0002_P0000"] = {
            "option_1_label": "le ballon",
            "option_2_label": "le seau",
            "option_3_label": "le doudou",
        }
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2[(i, j)]
            s[f"{p2}_T0003_P0000"] = T3[i]
            meta[f"{p2}_T0003_P0000"] = {
                "option_1_label": "le manteau",
                "option_2_label": "le seau",
                "option_3_label": "le doudou",
            }
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = L3[(i, j, k)]
                s[f"{p3}_F0001"] = FIN[(i, j, k)]
    return s, meta


def path_stats(scripts: dict) -> tuple[int, int, int]:
    def txt(cid: str) -> str:
        return " ".join(ln.split("|", 1)[1] for ln in scripts[cid])

    lengths = []
    fins = []
    l3s = []
    lasts = []
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                ids = [
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
                n = sum(words(txt(c)) for c in ids)
                lengths.append(n)
                fins.append(txt(ids[-1]))
                l3s.append(txt(ids[-2]))
                last = [ln for ln in scripts[ids[-1]] if ln.startswith("narrateur|")][-1]
                lasts.append(last.split("|", 1)[1])
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}")
    if len(set(l3s)) != 27:
        raise SystemExit(f"L3 non distincts: {len(set(l3s))}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images non distinctes: {len(set(lasts))}")
    mn, mx, moy = min(lengths), max(lengths), sum(lengths) // len(lengths)
    print(f"chemins mots min={mn} max={mx} moy={moy}")
    return mn, mx, moy


def sons_for(cid: str, kind: str, i: int | None, j: int | None, k: int | None) -> str:
    if kind == "passage_debut":
        return "enfants_parc,pain,pigeon"
    if kind in {"transition_question", "passage_question"}:
        return ""
    if kind == "passage_fin":
        return SONS_FIN.get(k or 1, "pas,pain")
    if cid.endswith("_C0001"):
        return "enfants_parc"
    if i and "_T0002_P000" in cid and "_T0003_" not in cid:
        if cid.endswith(("_P0001", "_P0002", "_P0003")):
            return SONS_L2.get(j or 1, "table")
        return ""
    if "_T0003_P000" in cid and cid[-1] in "123":
        return SONS_L3.get(k or 1, "table")
    if i:
        return SONS_L1.get(i, "enfants_parc")
    return "enfants_parc"


def parse_ijk(cid: str) -> tuple[int | None, int | None, int | None]:
    i = j = k = None
    m = re.search(r"CHK_T0001_P000(\d)", cid)
    if m:
        i = int(m.group(1))
    m2 = re.search(r"_T0002_P000(\d)", cid)
    if m2:
        j = int(m2.group(1))
    m3 = re.search(r"_T0003_P000(\d)", cid)
    if m3:
        k = int(m3.group(1))
    return i, j, k


def extra_emphasis(kind: str, prof: str, text_join: str) -> dict:
    extra: dict = {}
    low = text_join.lower()
    if prof == "opening":
        extra["emphasis"] = "clou de cuivre"
    elif prof == "clue":
        extra["emphasis"] = "seau jaune"
    elif prof == "confirm":
        extra["emphasis"] = "table"
    elif prof == "resolution":
        extra["emphasis"] = "clou de cuivre" if "clou" in low else "seau"
    elif prof == "ending":
        extra["emphasis"] = "clou de cuivre" if "clou" in low else None
    elif prof == "action":
        extra["emphasis"] = "gâteau" if "gâteau" in low else None
    elif prof == "obstacle":
        extra["emphasis"] = None
    return extra


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts, meta = build()
    preview(scripts)
    mn, mx, moy = path_stats(scripts)
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={list(extra_ids)[:8]}")
    out_chunks = []
    piper_vals = set()
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        prof = profile_for(cid, kind)
        i, j, k = parse_ijk(cid)
        text_join = " ".join(ln.split("|", 1)[1] for ln in scripts[cid])
        extra = extra_emphasis(kind, prof, text_join)
        if cid.endswith("_Q0001"):
            extra["fields"] = dict(Q_FIELDS)
        if cid in meta:
            extra.setdefault("fields", {}).update(meta[cid])
        nc = apply_tts(c, scripts[cid], sons_for(cid, kind, i, j, k), prof, extra)
        piper_vals.add(nc["length_scale_piper"])
        out_chunks.append(nc)
    if len(piper_vals) < 4:
        raise SystemExit(f"piper trop uniforme: {piper_vals}")
    out = dict(src)
    out["fil_rouge"] = (
        "Mila veut un gâteau de sable près du pain tiède du fournil, "
        "avant que la croûte refroidisse. L'anse du seau jaune a un clou de cuivre "
        "qui cligne au soleil. Un pigeon pique une miette : le seau roule sous la table, "
        "toc. Elle tire trop fort, l'anse bute. Ballon, seau ou doudou : la serviette "
        "vole le clou. Elle refuse de foncer, écoute le toc. Manteau, seau ou doudou : "
        "le clou se paie. Le pain n'est plus tiède. Le clou reste sur l'anse."
    )
    out["title"] = "Le seau sous la table"
    out["characters"] = "Mila, papa, maman"
    out["setting"] = "square du village, table de bois, pain tiède, seau sous la table"
    out["chunks"] = out_chunks
    check(SID, out["age_band"], out["chunks"])
    joined = "\n".join(c["script"] for c in out_chunks).lower()
    for bad in BAN + TICS:
        if bad in joined:
            raise SystemExit(f"{SID} extra interdit: {bad}")
    for c in out_chunks:
        if not c.get("notes") or "arc=" not in c["notes"]:
            raise SystemExit(f"notes manquantes {c['chunk_id']}")
        if not c.get("text_xai_tags") or c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"xai trop plat {c['chunk_id']}")
        if "<speak>" not in (c.get("text_ssml") or ""):
            raise SystemExit(f"ssml plat {c['chunk_id']}")
        if c.get("kind") != "passage_fin":
            continue
        last_lines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_lines[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"fin mécanique: {last}")
    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size} piper={sorted(piper_vals)}")
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# TREE-AUT-038 — Le seau sous la table\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Titre noyau :** *Le seau sous la table*\n"
        "- **Public :** N1 (≤ 10 mots/phrase)\n"
        "- **Leçon :** AUT.AFF.003 — retrouver ses affaires avant de partir, vécue "
        "(le seau, le manteau et le doudou rentrent ; personne ne récite la règle)\n"
        "- **Personnages :** Mila, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Au square, la table du fournil fait tic au soleil. Un pain tiède y pose "
        "son ventre. L'anse du seau jaune a un clou de cuivre qui cligne. Mila "
        "veut un gâteau de sable avant que la croûte refroidisse. Un pigeon pique "
        "une miette : elle sursaute, le seau roule sous la table, toc. Elle part "
        "les mains vides. Au bac, à la rampe ou aux chaînes, elle tire trop fort : "
        "l'anse bute. Ballon, seau ou doudou changent la seconde ruse (serviette, "
        "manche, oreille). Elle refuse de foncer, écoute le toc du début. Manteau, "
        "seau ou doudou : le clou se paie. Le pain n'est plus tiède.\n\n"
        "## Vécu\n\n"
        "Square, table de bois, pain tiède, mouche, pigeon, clou de cuivre, seau "
        "jaune, manteau rouge, doudou gris. Impatience (vite, le gâteau), "
        "découragement (sourire disparu, poitrine, anse qui bute), fierté calme "
        "(sans foncer, le toc). Merci vécu quand elle dit « dessous ». Question : "
        "le seau jaune est où. T1 bac / toboggan / balançoires. T2 ballon / seau / "
        "doudou. T3 manteau / seau / doudou. 1er choix = lieux, n'enlève pas le seau.\n\n"
        "## Vu et corrigé\n\n"
        "P1 F-NAR-019 example4 v2. Ouverture inventée (tic du bois, fournil, clou "
        "qui cligne), pas les cinq manières listées. Indice unique : clou de cuivre, "
        "payé au climax (cligne à l'ombre, toc). Corps : sourire disparaît, envie et "
        "inquiétude, adulte à la même hauteur. Revers allongé (audit : obstacle trop "
        "ponctuel) : 1re traction, butée, serviette ou manche, refuse de foncer, "
        "écoute. Fin qui a failli (une seconde, le fournil, le pigeon). Pas gabarit "
        "example3. Tics « encore / déjà / tout doux / tout calme » retirés. Troupe "
        "D16 Mila. 27 fins, 27 L3, 27 dernières images. TTS par chunk : `notes`, "
        "`text_ssml`, `text_xai_tags`, piper 1.10–1.30. `slow` = choix, indice, "
        f"fins. `check()` N1 OK. Chemins {mn}–{mx} mots, moyenne {moy}. Pas apply.\n\n"
        "## Direction vocale\n\n"
        "Chaque segment a un arc dans `notes`. Débit, hauteur, volume et pause "
        "suivent la fonction : installation, choix, indice, obstacle, action, "
        "résolution, retour. Action plus vive. Choix, indice et fins plus lents.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks\n"
        f"- 27 chemins, {mn} à {mx} mots, moyenne {moy}\n"
        "- 27 fins distinctes, 27 L3 distincts, 27 dernières images\n"
        "- `text` = `script` collé\n"
        "- 0 occurrence de « encore », « déjà », « tout doux », « tout calme »\n"
        "- 0 « on va apprendre », « mission accomplie », « aujourd'hui »\n"
        "- papa/maman parlent, une question, un merci vécu\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
