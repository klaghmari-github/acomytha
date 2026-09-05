#!/usr/bin/env python3
"""TREE-AUT-040 — La toile et la pompe d'Amir. N2 AUT.ROU.001. F-NAR-019 v2."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words

SID = "TREE-AUT-040"
LIM = 15
TITLE = "La toile et la pompe d'Amir"
CHARS = "Amir, papa, maman"
SETTING = "ferme, cour, toile d'araignée, pompe, lanterne"
FIL = (
    "Au coin de la lanterne, Amir veut faire chanter la pompe "
    "avant que la flamme meure. Une toile barre la poignée. "
    "Un éclat de zinc y cligne. Il prend poignée et verre ensemble : "
    "la toile colle, la pompe refuse. Papa veut les poules. "
    "Amir refuse de foncer. L'éclat de zinc paie le début."
)

TICS = ("tout doux", "tout calme", "encore", "déjà")
BAN = (
    "aujourd'hui",
    "mission accomplie",
    "j'ai compris",
    "on dirait que notre mission",
    "lumière couleur de miel",
    "gouttes pendent",
    "merle",
    "miel",
    "grand-père",
    "maîtresse",
    "jardinier",
    "bibliothécaire",
    "gardienne",
    "on va apprendre",
    "on va ranger",
    "après le jeu",
    "bon travail",
    "marque fine",
    "ombre-flèche",
    "ombre en forme",
    "tache de couleur",
    "ancre minuscule",
    "étoile brune",
    "fil pâle",
    "croissant",
    "virgule d'or",
    "virgule de",
    "œillet",
    "oeillet",
    "perle de verre",
    "bouton de nacre",
    "nœud de raphia",
    "pois ivoire",
    "grain de savon",
    "grain de vanille",
    "pastille de colle",
    "grain de son",
    "bouton de lavande",
    "capuchon",
    "grain doré",
    "brin de safran",
    "anneau de liège",
    "clou à tête",
    "grain d'ambre",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "éclat de zinc",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=la pompe se tait, il veut tout à la fois; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": (
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton choix change la ruse; tempo=suspendu; "
            "sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "éclat de zinc",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=regarde_la_poignee; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "zinc",
        "note": (
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=savoir n_est pas lever; tempo=naturel; "
            "sourire=léger; respiration=fluide"
        ),
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": (
            "arc=action; intention=entraîner; emotion=élan; intensite=2; "
            "destinataire=enfant; sous_texte=il_prend_poignee_et_verre_ensemble; "
            "tempo=vif; sourire=léger; respiration=courte"
        ),
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; "
            "intensite=2; destinataire=enfant; sous_texte=la_toile_colle_la_pompe_refuse; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "éclat de zinc",
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=une_main_sur_l_eclat_l_autre_vide; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": (
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_eclat_reste_la_toile_tient; "
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
    if re.search(r"\bencore\b", low) or re.search(r"\bd[eé]j[àa]\b", low):
        raise SystemExit(f"tic encore/déjà: {p}")
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
    if cid.endswith(("_T0002_P0001", "_T0002_P0002", "_T0002_P0003")):
        return "obstacle"
    return "action"


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

OPENING = [
    L("narrateur", "À cette heure, la pompe devrait chanter."),
    L("narrateur", "Elle se tait, contre la grange."),
    L("narrateur", "Le verre de la lanterne est tiède, sous la paume."),
    L("narrateur", "Ça sent le foin mouillé, près du seuil."),
    L("narrateur", "Une paille colle à la pierre."),
    L("narrateur", "Une poule gratte le zinc, toc toc."),
    L("narrateur", "Entre deux lattes, une toile d'araignée tient."),
    L("narrateur", "Sur la poignée, un éclat de zinc cligne."),
    L("maman", "Tu as vu cet éclat, Amir ?"),
    L("enfant-m", "Il brille, maman."),
    L("papa", "Les poules ont soif."),
    L("papa", "Leur bac d'eau est bas."),
    L("narrateur", "En ce moment, Amir a une botte à la main."),
    L("enfant-m", "Je veux la pompe !"),
    L("enfant-m", "Avant que la lanterne meure !"),
    L("papa", "Les poules, moi."),
    L("narrateur", "Amir lâche la botte."),
    L("narrateur", "Il prend la poignée et le verre, ensemble."),
    L("narrateur", "La toile colle à sa manche."),
    L("narrateur", "La poignée refuse, froide et rêche."),
    L("narrateur", "La flamme de la lanterne se baisse."),
    L("enfant-m", "Elle ne bouge pas !"),
    L("narrateur", "Le sourire d'Amir disparaît."),
    L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    L("maman", "Tes deux mains, Amir ?"),
    L("narrateur", "Maman s'accroupit, à sa hauteur."),
    L("narrateur", "Il pose la lanterne, près du mur."),
    L("enfant-m", "Je veux les deux."),
    L("papa", "On va dans la cour ?"),
]

T1 = [
    L("narrateur", "La cour a trois coins, connus."),
    L("papa", "Le bac à sable."),
    L("papa", "Le toboggan."),
    L("maman", "Ou les balançoires ?"),
    L("maman", "Tu choisis."),
]

L1 = {
    1: [
        L("narrateur", "Amir s'agenouille près du bac."),
        L("narrateur", "Le sable est pâle, un peu frais."),
        L("narrateur", "Il glisse entre les doigts, chh."),
        L("enfant-m", "De l'eau, dans le sable !"),
        L("maman", "Avec tes mains pleines ?"),
        L("enfant-m", "Avec la pompe !"),
        L("narrateur", "Il court vers la poignée, trop vite."),
        L("narrateur", "Le sable colle à la toile."),
        L("narrateur", "La poignée refuse, rêche."),
        L("enfant-m", "Elle est coincée."),
        L("narrateur", "Ses épaules tombent."),
        L("narrateur", "L'envie et l'inquiétude se bousculent, dans sa poitrine."),
        L("papa", "On s'accroupit ?"),
        L("narrateur", "Papa se met à sa hauteur."),
        L("enfant-m", "L'éclat, il est où ?"),
        L("maman", "Tu l'as vu, au départ."),
    ],
    2: [
        L("narrateur", "Amir gravit la marche du toboggan."),
        L("narrateur", "Le métal est lisse, un peu froid."),
        L("narrateur", "Une paille de grange y colle."),
        L("enfant-m", "Je vois la pompe, d'en haut !"),
        L("papa", "Et la lanterne ?"),
        L("enfant-m", "Je prends les deux."),
        L("narrateur", "Il dévale, les deux mains ouvertes."),
        L("narrateur", "Il attrape poignée et verre, d'un coup."),
        L("narrateur", "La toile s'accroche à la manche."),
        L("narrateur", "La flamme se baisse, nette."),
        L("enfant-m", "Oh."),
        L("narrateur", "Le sourire d'Amir disparaît."),
        L("maman", "Je m'accroupis, d'accord ?"),
        L("narrateur", "Maman se met à sa hauteur."),
        L("enfant-m", "L'éclat ne cligne plus."),
        L("papa", "Tu l'as vu, toi."),
    ],
    3: [
        L("narrateur", "Amir va vers les balançoires."),
        L("narrateur", "Une corde est rêche, près de la haie."),
        L("narrateur", "Le siège de bois est lisse."),
        L("enfant-m", "La pompe, je la vois d'ici."),
        L("maman", "Tu restes sur le siège ?"),
        L("enfant-m", "Je cours."),
        L("narrateur", "Il court, les deux mains ouvertes."),
        L("narrateur", "Il saisit poignée et verre, ensemble."),
        L("narrateur", "La toile colle, puis tire."),
        L("narrateur", "La poignée reste morte."),
        L("enfant-m", "Elle ne veut pas."),
        L("narrateur", "Un nœud lui serre la gorge."),
        L("papa", "On s'accroupit ?"),
        L("narrateur", "Papa se met à sa hauteur."),
        L("enfant-m", "L'éclat s'est tu."),
        L("maman", "Tu l'as entendu, au départ."),
    ],
}

Q = {
    1: [
        L("narrateur", "Amir a du sable aux doigts."),
        L("papa", "Qu'est-ce qui brille sur la poignée ?"),
    ],
    2: [
        L("narrateur", "Amir a une paille au genou."),
        L("maman", "Qu'est-ce qui brille sur la poignée ?"),
    ],
    3: [
        L("narrateur", "Amir a le vent dans les cheveux."),
        L("papa", "Qu'est-ce qui brille sur la poignée ?"),
    ],
}

C = {
    1: [
        L("narrateur", "Amir regarde vers la pompe."),
        L("enfant-m", "Un éclat de zinc."),
        L("papa", "Oui."),
        L("papa", "Sur la poignée."),
        L("maman", "Merci, Amir."),
        L("narrateur", "Un grain de sable brille sur son pouce."),
        L("papa", "On prend un jeu, près du bac ?"),
        L("enfant-m", "Oui."),
        L("narrateur", "La lanterne fume, loin, très bas."),
    ],
    2: [
        L("narrateur", "Amir montre la poignée du doigt."),
        L("enfant-m", "Un éclat de zinc."),
        L("maman", "Oui."),
        L("maman", "Sur la poignée."),
        L("papa", "Merci, Amir."),
        L("narrateur", "La paille reste sur la marche."),
        L("maman", "On prend un jeu, près de la rampe ?"),
        L("enfant-m", "Oui."),
        L("narrateur", "Le métal garde un peu de froid."),
    ],
    3: [
        L("narrateur", "Amir se tourne vers la grange."),
        L("enfant-m", "Un éclat de zinc."),
        L("papa", "Oui."),
        L("papa", "Sur la poignée."),
        L("maman", "Merci, Amir."),
        L("narrateur", "La corde se tait, un instant."),
        L("papa", "On prend un jeu, près des chaînes ?"),
        L("enfant-m", "Oui."),
        L("narrateur", "Le vent touche son nez, froid."),
    ],
}

T2 = {
    1: [
        L("maman", "Quel jeu aide le bac ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    2: [
        L("papa", "Quel jeu aide la rampe ?"),
        L("maman", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    3: [
        L("maman", "Quel jeu aide la corde ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
}

L2 = {
    (1, 1): [
        L("narrateur", "Près du bac, le ballon rouge attend."),
        L("narrateur", "Il est lisse, un peu frais."),
        L("enfant-m", "Il pousse la poignée !"),
        L("narrateur", "Amir frappe trop fort."),
        L("narrateur", "Le ballon file contre la toile."),
        L("narrateur", "La poignée ne cède pas."),
        L("enfant-m", "Le ballon aussi, coincé ?"),
        L("narrateur", "Il s'élance pour le rattraper."),
        L("narrateur", "Puis il s'arrête, net."),
        L("enfant-m", "Pas comme ça."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "Il écoute le zinc, muet."),
        L("narrateur", "Sur la poignée, l'éclat de zinc cligne, faible."),
        L("papa", "Tu as vu, toi."),
        L("narrateur", "Papa se tait, accroupi."),
        L("narrateur", "Un grain de sable reste sur le cuir."),
    ],
    (1, 2): [
        L("narrateur", "Près du bac, le seau sonne."),
        L("narrateur", "L'anse est froide, un peu rêche."),
        L("enfant-m", "Un vrai puits, maman !"),
        L("narrateur", "Il glisse le seau sous le bec."),
        L("narrateur", "Puis il tire la poignée, d'un coup."),
        L("narrateur", "L'anse cliquette, vide."),
        L("narrateur", "La toile tremble, la pompe se tait."),
        L("enfant-m", "Rien."),
        L("narrateur", "Il veut tirer plus fort."),
        L("narrateur", "Ses doigts se crispent, puis s'ouvrent."),
        L("enfant-m", "J'attends."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "L'éclat de zinc cligne, sous la lanterne."),
        L("maman", "Tu l'as vu, au départ."),
        L("narrateur", "Maman se tait, près du bac."),
        L("narrateur", "Un grain de sable reste au fond du seau."),
    ],
    (1, 3): [
        L("narrateur", "Près du bac, le doudou a du sable."),
        L("narrateur", "Une oreille est pâle, un peu rêche."),
        L("enfant-m", "Il essuie la toile."),
        L("narrateur", "Amir frotte trop vite."),
        L("narrateur", "La toile colle à l'oreille grise."),
        L("enfant-m", "Je n'aime pas ça."),
        L("narrateur", "Il veut frotter plus fort."),
        L("narrateur", "Puis il serre le doudou, sans bouger."),
        L("enfant-m", "Pas comme ça."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "Il écoute la lanterne, très bas."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("papa", "Tu l'as vu, toi."),
        L("narrateur", "Le zinc reste muet, sous la toile."),
        L("narrateur", "Un grain de sable reste sur le tissu."),
    ],
    (2, 1): [
        L("narrateur", "Au pied du toboggan, le ballon attend."),
        L("narrateur", "Il est froid, près de la rampe."),
        L("enfant-m", "Il glisse avec moi !"),
        L("narrateur", "Amir le lance vers la pompe."),
        L("narrateur", "Le cuir tape la toile, puis rebondit."),
        L("narrateur", "La poignée ne bouge pas."),
        L("enfant-m", "Zut."),
        L("narrateur", "Il veut courir après le cuir."),
        L("narrateur", "Une marche du toboggan fait toc, sous son pied."),
        L("narrateur", "Il s'arrête, le pied sur le métal."),
        L("enfant-m", "Pas trop vite."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "L'éclat de zinc cligne, faible, sur la poignée."),
        L("maman", "Tu l'as vu, au départ."),
        L("narrateur", "La rampe reste froide, sans mot."),
        L("narrateur", "Une paille de rampe colle au cuir."),
    ],
    (2, 2): [
        L("narrateur", "Au toboggan, le seau sonne contre une marche."),
        L("narrateur", "L'anse est froide, près du métal."),
        L("enfant-m", "C'est sa gare."),
        L("narrateur", "Amir descend, le seau à bout de bras."),
        L("narrateur", "Il pose l'anse et tire, ensemble."),
        L("narrateur", "Le seau penche, vide."),
        L("narrateur", "La toile s'accroche à l'anse."),
        L("enfant-m", "Il est pris."),
        L("narrateur", "Il veut arracher l'anse."),
        L("narrateur", "Puis il lâche, les doigts ouverts."),
        L("enfant-m", "J'attends."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "L'éclat de zinc cligne, sous la lanterne."),
        L("papa", "Tu as vu, toi."),
        L("narrateur", "Papa garde les mains dans les poches."),
        L("narrateur", "Une paille de rampe reste dans le seau."),
    ],
    (2, 3): [
        L("narrateur", "Au toboggan, le doudou a vu la rampe."),
        L("narrateur", "L'oreille grise est froide, un peu."),
        L("enfant-m", "Il glisse des yeux."),
        L("narrateur", "Amir l'essuie contre la toile, trop vite."),
        L("narrateur", "La toile colle à l'oreille."),
        L("enfant-m", "Oh."),
        L("narrateur", "Il veut tirer le tissu."),
        L("narrateur", "La rampe est froide sous son genou."),
        L("narrateur", "Il s'arrête, le doudou contre la joue."),
        L("enfant-m", "Pas comme ça."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("maman", "Tu l'as vu, au départ."),
        L("narrateur", "Maman s'accroupit, sans parler."),
        L("narrateur", "Une paille de rampe reste sur le gris."),
    ],
    (3, 1): [
        L("narrateur", "Près des chaînes, le ballon a de l'herbe."),
        L("narrateur", "Un brin colle au cuir."),
        L("enfant-m", "On roule jusqu'à la pompe !"),
        L("narrateur", "Amir pousse trop fort."),
        L("narrateur", "Le ballon part sous la toile."),
        L("narrateur", "La poignée reste morte."),
        L("enfant-m", "Il est parti."),
        L("narrateur", "Il veut se jeter à plat."),
        L("narrateur", "La corde rêche frotte son poignet."),
        L("narrateur", "Il s'arrête, la corde à la main."),
        L("enfant-m", "Pas trop vite."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "L'éclat de zinc cligne, faible."),
        L("papa", "Tu as vu, toi."),
        L("narrateur", "La corde se tait, contre la haie."),
        L("narrateur", "Un brin d'herbe reste sur le cuir."),
    ],
    (3, 2): [
        L("narrateur", "Près des balançoires, le seau est dans l'herbe."),
        L("narrateur", "L'anse est froide, près de la corde."),
        L("enfant-m", "Il va sous le bec !"),
        L("narrateur", "Amir court, l'anse et la poignée, ensemble."),
        L("narrateur", "Le seau sonne, vide, contre le zinc."),
        L("narrateur", "La toile s'accroche à l'anse."),
        L("enfant-m", "Coincé."),
        L("narrateur", "Il veut tirer les deux, plus fort."),
        L("narrateur", "Le vent de la haie lui pique le nez."),
        L("narrateur", "Il ouvre les doigts, lent."),
        L("enfant-m", "J'attends."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "L'éclat de zinc cligne, sous la lanterne."),
        L("maman", "Tu l'as vu, au départ."),
        L("narrateur", "Le vent de la haie passe, sans mot."),
        L("narrateur", "L'herbe mouille le bord du seau."),
    ],
    (3, 3): [
        L("narrateur", "Près des balançoires, le doudou a du vent."),
        L("narrateur", "L'oreille molle clignote."),
        L("enfant-m", "Il s'assoit avec moi."),
        L("narrateur", "Amir court, doudou et poignée, ensemble."),
        L("narrateur", "La toile colle à l'oreille."),
        L("enfant-m", "Je n'aime pas ça."),
        L("narrateur", "Il veut arracher le tissu."),
        L("narrateur", "La corde rêche frotte son coude."),
        L("narrateur", "Il s'arrête, le doudou contre le ventre."),
        L("enfant-m", "Pas comme ça."),
        L("narrateur", "Il refuse de foncer."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("papa", "Tu as vu, toi."),
        L("narrateur", "Papa reste à sa hauteur, silencieux."),
        L("narrateur", "Le vent de la haie touche l'oreille grise."),
    ],
}

T3 = {
    (1, 1): [
        L("narrateur", "Le ballon s'est tu, près du bac."),
        L("papa", "On va où, avec ça ?"),
        L("maman", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (1, 2): [
        L("narrateur", "Le seau attend, un grain au fond."),
        L("maman", "On va où, avec l'anse ?"),
        L("papa", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (1, 3): [
        L("narrateur", "Le doudou a du sable à l'oreille."),
        L("papa", "On va où, avec lui ?"),
        L("maman", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (2, 1): [
        L("narrateur", "Le ballon a une paille de rampe."),
        L("maman", "On va où, avec le cuir ?"),
        L("papa", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (2, 2): [
        L("narrateur", "Le seau a sonné contre la marche."),
        L("papa", "On va où, avec l'anse ?"),
        L("maman", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (2, 3): [
        L("narrateur", "Le doudou a froid, près du métal."),
        L("maman", "On va où, avec lui ?"),
        L("papa", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (3, 1): [
        L("narrateur", "Le ballon a de l'herbe au cuir."),
        L("papa", "On va où, avec ça ?"),
        L("maman", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (3, 2): [
        L("narrateur", "Le seau a l'herbe au bord."),
        L("maman", "On va où, avec l'anse ?"),
        L("papa", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
    (3, 3): [
        L("narrateur", "Le doudou a pris le vent de la haie."),
        L("papa", "On va où, avec lui ?"),
        L("maman", "La pompe, le poulailler, ou le pré ?"),
        L("narrateur", "Tu choisis."),
    ],
}

L3 = {
    (1, 1, 1): [
        L("narrateur", "Amir revient vers la pompe, le ballon sous le bras."),
        L("narrateur", "La toile barre la poignée, serrée."),
        L("enfant-m", "Je pousse avec le cuir !"),
        L("narrateur", "Le cuir touche la toile."),
        L("narrateur", "La poignée ne cède pas."),
        L("narrateur", "Il pose le ballon dans le sable, loin."),
        L("narrateur", "La lanterne fume, très bas."),
        L("narrateur", "Sur la poignée, l'éclat de zinc cligne."),
        L("enfant-m", "Ma main, ici."),
        L("papa", "Tu as vu."),
        L("narrateur", "Amir pose la paume sur l'éclat."),
        L("narrateur", "L'autre main est vide."),
        L("narrateur", "Il lève, sans la toile."),
        L("narrateur", "Une seconde, plus rien."),
        L("narrateur", "Puis l'eau arrive, froide."),
        L("narrateur", "La flamme se relève, un peu."),
    ],
    (1, 1, 2): [
        L("narrateur", "Amir part vers le poulailler, le ballon sous le bras."),
        L("narrateur", "Les poules se précipitent, ailes ouvertes."),
        L("enfant-m", "De l'eau, les poules !"),
        L("narrateur", "Le ballon roule vers le grillage."),
        L("narrateur", "Il veut courir après, les deux mains prises."),
        L("narrateur", "Puis il s'arrête."),
        L("enfant-m", "Le ballon, derrière moi."),
        L("narrateur", "Il le pose, puis ouvre le loquet."),
        L("narrateur", "L'éclat de zinc lui revient, sur la paume."),
        L("maman", "Tu as vu."),
        L("narrateur", "Il revient à la pompe, une main libre."),
        L("narrateur", "La paume trouve l'éclat."),
        L("narrateur", "L'eau vient, juste à temps."),
        L("narrateur", "Il pose l'eau des poules, après."),
        L("narrateur", "Une poule boit, le bec contre le zinc."),
        L("narrateur", "La lanterne n'est pas morte."),
    ],
    (1, 1, 3): [
        L("narrateur", "Amir part vers le pré, le ballon sous le bras."),
        L("narrateur", "La barrière a une toile, fine."),
        L("enfant-m", "Je passe, le cuir avec moi !"),
        L("narrateur", "Il se cale, trop étroit."),
        L("narrateur", "Le ballon manque de tomber dans l'herbe."),
        L("narrateur", "Il recule, le cœur serré."),
        L("enfant-m", "La barrière, puis le cuir."),
        L("narrateur", "Il pose le ballon, ouvre, puis reprend."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("papa", "Tu as vu."),
        L("narrateur", "Au bac d'eau du pré, il s'arrête."),
        L("narrateur", "Une main sur l'éclat, l'autre vide."),
        L("narrateur", "L'eau arrive, presque trop tard."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "Le cuir rouge a une herbe collée."),
        L("narrateur", "Le pré sent le foin mouillé."),
    ],
    (1, 2, 1): [
        L("narrateur", "Amir glisse le seau sous le bec de la pompe."),
        L("narrateur", "Il tire la poignée, l'anse à la main."),
        L("narrateur", "L'anse cliquette, vide."),
        L("enfant-m", "Les deux, ça ne va pas."),
        L("narrateur", "Il pose le seau, net."),
        L("narrateur", "La lanterne fume, trop bas."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Ma main, ici."),
        L("maman", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat, loin de la toile."),
        L("narrateur", "Il lève."),
        L("narrateur", "Une seconde, le bec se tait."),
        L("narrateur", "Puis l'eau tombe, froide, dans le seau."),
        L("narrateur", "Ting."),
        L("narrateur", "La flamme se relève."),
        L("narrateur", "Un grain de sable nage, au fond."),
    ],
    (1, 2, 2): [
        L("narrateur", "Amir porte le seau vers le poulailler."),
        L("narrateur", "Les poules se jettent, trop près."),
        L("enfant-m", "Vous allez le faire tomber !"),
        L("narrateur", "L'eau manque de sauter par-dessus l'anse."),
        L("narrateur", "Il pose le seau, loin des pattes."),
        L("narrateur", "Le loquet a une petite toile."),
        L("enfant-m", "Le loquet, puis l'eau."),
        L("narrateur", "Il ouvre, une main libre."),
        L("narrateur", "L'éclat de zinc lui revient, sur la paume."),
        L("papa", "Tu as vu."),
        L("narrateur", "Il pose l'eau, après le loquet."),
        L("narrateur", "Une poule boit, le bec contre le seau."),
        L("narrateur", "La lanterne, à la cour, n'est pas morte."),
        L("narrateur", "L'anse a un peu de paille."),
        L("narrateur", "Amir souffle, les épaules basses."),
        L("narrateur", "Puis il se redresse, calme."),
    ],
    (1, 2, 3): [
        L("narrateur", "Amir porte le seau vers le pré."),
        L("narrateur", "À la barrière, l'eau penche."),
        L("enfant-m", "Je me faufile !"),
        L("narrateur", "L'anse cogne le bois."),
        L("narrateur", "Une goutte tombe dans l'herbe."),
        L("narrateur", "Il recule, le seau des deux mains."),
        L("enfant-m", "J'ouvre, puis je passe."),
        L("narrateur", "Il pose le seau, ouvre, reprend."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("maman", "Tu as vu."),
        L("narrateur", "Au bac du pré, il verse, lent."),
        L("narrateur", "L'eau fait un cercle, dans l'herbe."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "Ça a failli se vider, à la barrière."),
        L("narrateur", "L'anse garde une goutte, froide."),
        L("narrateur", "Le pré sent le foin."),
    ],
    (1, 3, 1): [
        L("narrateur", "Amir tient le doudou et la poignée, ensemble."),
        L("narrateur", "La toile colle à l'oreille grise."),
        L("enfant-m", "Il essuie, puis je tire !"),
        L("narrateur", "Les deux gestes se cognent."),
        L("narrateur", "La pompe se tait."),
        L("narrateur", "Il glisse le doudou sous le bras, loin."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Ma main, ici."),
        L("papa", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat."),
        L("narrateur", "L'autre main est vide."),
        L("narrateur", "Il lève, sans la toile."),
        L("narrateur", "Une seconde, plus rien."),
        L("narrateur", "Puis l'eau arrive."),
        L("narrateur", "Une goutte brille sur l'oreille, puis sèche."),
        L("narrateur", "La flamme se relève, un peu."),
    ],
    (1, 3, 2): [
        L("narrateur", "Amir part vers le poulailler, le doudou à la main."),
        L("narrateur", "Le loquet demande l'autre main."),
        L("enfant-m", "Je tiens les deux !"),
        L("narrateur", "Le doudou glisse, le loquet reste fermé."),
        L("narrateur", "Il serre les dents, puis lâche le tissu."),
        L("enfant-m", "Toi, sous le bras."),
        L("narrateur", "Il ouvre le loquet, une main libre."),
        L("narrateur", "L'éclat de zinc lui revient."),
        L("maman", "Tu as vu."),
        L("narrateur", "Il revient à la pompe, sans le doudou aux doigts."),
        L("narrateur", "La paume trouve l'éclat."),
        L("narrateur", "L'eau vient, juste à temps."),
        L("narrateur", "Une poule picore près de l'oreille grise."),
        L("narrateur", "Une paille reste coincée dans le tissu."),
        L("narrateur", "La lanterne n'est pas morte."),
        L("narrateur", "Amir souffle, puis sourit, petit."),
    ],
    (1, 3, 3): [
        L("narrateur", "Amir part vers le pré, le doudou qui traîne."),
        L("narrateur", "L'herbe mouille l'oreille."),
        L("enfant-m", "Je marche, et je le traîne."),
        L("narrateur", "Le tissu s'alourdit, plein d'eau d'herbe."),
        L("narrateur", "Il s'arrête, les épaules lourdes."),
        L("enfant-m", "Je le prends, puis je marche."),
        L("narrateur", "Il ramasse le doudou, puis ouvre la barrière."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("papa", "Tu as vu."),
        L("narrateur", "Au bac du pré, une main sur l'éclat."),
        L("narrateur", "L'eau arrive, presque trop tard."),
        L("narrateur", "L'herbe haute a parfumé le tissu gris."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "Le doudou est lourd, et sauvé."),
        L("narrateur", "Amir le serre, sans courir."),
        L("narrateur", "Le pré sent le foin mouillé."),
    ],
    (2, 1, 1): [
        L("narrateur", "Amir quitte le toboggan, le ballon sous le bras."),
        L("narrateur", "La rampe est froide, derrière lui."),
        L("enfant-m", "Le cuir pousse la poignée !"),
        L("narrateur", "Le ballon glisse, comme sur la rampe."),
        L("narrateur", "La toile l'arrête, nette."),
        L("narrateur", "Il pose le cuir au pied du métal."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Pas le cuir."),
        L("papa", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat, loin de la toile."),
        L("narrateur", "Il lève, l'autre main vide."),
        L("narrateur", "Une seconde, le bec se tait."),
        L("narrateur", "Puis l'eau arrive, froide."),
        L("narrateur", "Le ballon a glissé, puis s'est tu contre le zinc."),
        L("narrateur", "La flamme se relève."),
        L("narrateur", "Une paille de rampe reste au cuir."),
    ],
    (2, 1, 2): [
        L("narrateur", "Amir part vers le poulailler, le ballon sous le bras."),
        L("narrateur", "Une paille de rampe colle au cuir."),
        L("narrateur", "Les poules se précipitent."),
        L("enfant-m", "Le ballon passe en premier !"),
        L("narrateur", "Le cuir roule sous le grillage, trop loin."),
        L("narrateur", "Il veut se faufiler, les deux mains prises."),
        L("narrateur", "Puis il pose le ballon, derrière le pied."),
        L("enfant-m", "Le loquet, puis vous."),
        L("narrateur", "L'éclat de zinc lui revient."),
        L("maman", "Tu as vu."),
        L("narrateur", "Il ouvre, une main libre."),
        L("narrateur", "L'eau vient de la pompe, après."),
        L("narrateur", "Une poule picore près du cuir, puis s'en va."),
        L("narrateur", "La paille de rampe reste collée."),
        L("narrateur", "La lanterne n'est pas morte."),
        L("narrateur", "Amir reprend le ballon, sans courir."),
    ],
    (2, 1, 3): [
        L("narrateur", "Amir part vers le pré, le ballon sous le bras."),
        L("narrateur", "Le cuir veut rebondir, comme à la rampe."),
        L("enfant-m", "Il roule dans l'herbe !"),
        L("narrateur", "À la barrière, le ballon manque de filer."),
        L("narrateur", "Il le serre, trop fort, et bute."),
        L("enfant-m", "J'ouvre, puis il vient."),
        L("narrateur", "Il pose le cuir, ouvre, reprend."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("papa", "Tu as vu."),
        L("narrateur", "Au bac du pré, la paume trouve l'éclat."),
        L("narrateur", "L'eau arrive, presque trop tard."),
        L("narrateur", "Le ballon roule une fois, dans l'herbe, puis s'arrête."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "Le métal du toboggan reste froid, derrière."),
        L("narrateur", "Amir souffle, calme."),
        L("narrateur", "Le pré sent le foin."),
    ],
    (2, 2, 1): [
        L("narrateur", "Amir quitte le toboggan, le seau à l'anse."),
        L("narrateur", "L'anse a sonné contre la marche."),
        L("enfant-m", "Je tiens l'anse, et je tire !"),
        L("narrateur", "Les deux font ting, vides."),
        L("narrateur", "La toile s'accroche à l'anse."),
        L("narrateur", "Il pose le seau, au pied de la rampe."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Ma main, ici."),
        L("maman", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat."),
        L("narrateur", "Il lève, sans l'anse."),
        L("narrateur", "Une seconde, plus rien."),
        L("narrateur", "Puis l'eau tombe, froide, dans le seau."),
        L("narrateur", "Le seau sonne, plein, sous la poignée rêche."),
        L("narrateur", "La flamme se relève."),
        L("narrateur", "Une paille de rampe nage, au fond."),
    ],
    (2, 2, 2): [
        L("narrateur", "Amir porte le seau vers le poulailler."),
        L("narrateur", "L'anse cliquette, près du grillage."),
        L("narrateur", "Les poules se jettent."),
        L("enfant-m", "L'anse, et le loquet !"),
        L("narrateur", "Le seau penche, l'eau saute."),
        L("narrateur", "Il pose l'anse, loin des pattes."),
        L("enfant-m", "Le loquet, puis vous."),
        L("narrateur", "L'éclat de zinc lui revient."),
        L("papa", "Tu as vu."),
        L("narrateur", "Il ouvre, une main libre."),
        L("narrateur", "Il pose l'eau, après."),
        L("narrateur", "Une poule boit, le bec contre le seau."),
        L("narrateur", "L'anse se tait près du grillage."),
        L("narrateur", "La lanterne n'est pas morte."),
        L("narrateur", "Une paille de rampe reste au bord."),
        L("narrateur", "Amir se redresse, calme."),
    ],
    (2, 2, 3): [
        L("narrateur", "Amir porte le seau vers le pré."),
        L("narrateur", "À la barrière, une goutte de rampe brille au bord."),
        L("enfant-m", "Je me faufile, l'anse avec moi !"),
        L("narrateur", "L'anse cogne, l'eau penche."),
        L("narrateur", "Il recule, les deux mains sur le seau."),
        L("enfant-m", "J'ouvre, puis je passe."),
        L("narrateur", "Il pose, ouvre, reprend."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("maman", "Tu as vu."),
        L("narrateur", "Au bac du pré, il verse, lent."),
        L("narrateur", "Une goutte de rampe nage dans l'eau du seau."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "Ça a failli se vider."),
        L("narrateur", "Le métal du toboggan reste froid, derrière."),
        L("narrateur", "Amir souffle."),
        L("narrateur", "Le pré sent le foin."),
    ],
    (2, 3, 1): [
        L("narrateur", "Amir quitte le toboggan, le doudou contre la joue."),
        L("narrateur", "L'oreille grise a froid, près du métal."),
        L("enfant-m", "Il essuie, et je tire !"),
        L("narrateur", "La toile colle à l'oreille."),
        L("narrateur", "La pompe se tait."),
        L("narrateur", "Il glisse le doudou sous le bras."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Ma main, ici."),
        L("papa", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat, loin de la toile."),
        L("narrateur", "Il lève, l'autre main vide."),
        L("narrateur", "Une seconde, plus rien."),
        L("narrateur", "Puis l'eau arrive."),
        L("narrateur", "Une goutte brille au bout de l'oreille."),
        L("narrateur", "La flamme se relève."),
        L("narrateur", "Une paille de rampe reste sur le gris."),
    ],
    (2, 3, 2): [
        L("narrateur", "Amir part vers le poulailler, le doudou à la main."),
        L("narrateur", "Le loquet demande l'autre main."),
        L("enfant-m", "Je tiens les deux !"),
        L("narrateur", "Le doudou glisse vers les pattes."),
        L("narrateur", "Une poule le picore, presque."),
        L("narrateur", "Il le serre sous le bras, puis ouvre."),
        L("enfant-m", "Toi, à l'abri."),
        L("narrateur", "L'éclat de zinc lui revient."),
        L("maman", "Tu as vu."),
        L("narrateur", "L'eau vient de la pompe, une main libre."),
        L("narrateur", "Une paille de rampe reste sur le gris."),
        L("narrateur", "Une poule picore à côté, puis s'en va."),
        L("narrateur", "La lanterne n'est pas morte."),
        L("narrateur", "Amir reprend le doudou, sans courir."),
        L("narrateur", "L'oreille a un peu de paille."),
        L("narrateur", "Il souffle, calme."),
    ],
    (2, 3, 3): [
        L("narrateur", "Amir part vers le pré, le doudou contre lui."),
        L("narrateur", "Le vent du pré sèche l'oreille."),
        L("enfant-m", "Il vole, et je marche !"),
        L("narrateur", "À la barrière, le tissu s'accroche."),
        L("narrateur", "Il tire, trop fort, et bute."),
        L("enfant-m", "Je le prends, puis j'ouvre."),
        L("narrateur", "Il ramasse, ouvre, passe."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("papa", "Tu as vu."),
        L("narrateur", "Au bac du pré, la paume trouve l'éclat."),
        L("narrateur", "L'eau arrive, presque trop tard."),
        L("narrateur", "Le vent du pré a séché l'oreille."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "Le métal du toboggan reste froid, derrière."),
        L("narrateur", "Amir serre le doudou, sans courir."),
        L("narrateur", "Le pré sent le foin."),
    ],
    (3, 1, 1): [
        L("narrateur", "Amir quitte les balançoires, le ballon sous le bras."),
        L("narrateur", "La corde rêche reste derrière."),
        L("enfant-m", "On roule jusqu'à la poignée !"),
        L("narrateur", "Le cuir frotte la toile."),
        L("narrateur", "La poignée refuse."),
        L("narrateur", "Il pose le ballon, loin de la haie."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Ma main, ici."),
        L("maman", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat, loin de la toile."),
        L("narrateur", "Il lève, l'autre main vide."),
        L("narrateur", "Une seconde, le bec se tait."),
        L("narrateur", "Puis l'eau arrive, froide."),
        L("narrateur", "Le ballon frotte la poignée rêche, puis s'arrête."),
        L("narrateur", "La flamme se relève."),
        L("narrateur", "Un brin de haie reste au cuir."),
    ],
    (3, 1, 2): [
        L("narrateur", "Amir part vers le poulailler, le ballon sous le bras."),
        L("narrateur", "Un bout de haie colle au cuir."),
        L("narrateur", "Les poules se précipitent."),
        L("enfant-m", "Le cuir passe sous le grillage !"),
        L("narrateur", "Le ballon se coince, trop loin."),
        L("narrateur", "Il veut tirer le cuir et le loquet."),
        L("narrateur", "Puis il lâche le ballon, derrière le pied."),
        L("enfant-m", "Le loquet, puis vous."),
        L("narrateur", "L'éclat de zinc lui revient."),
        L("papa", "Tu as vu."),
        L("narrateur", "Il ouvre, une main libre."),
        L("narrateur", "L'eau vient, après."),
        L("narrateur", "Un bout de haie reste collé au cuir."),
        L("narrateur", "Une poule picore, puis s'en va."),
        L("narrateur", "La lanterne n'est pas morte."),
        L("narrateur", "Amir reprend le ballon, sans courir."),
    ],
    (3, 1, 3): [
        L("narrateur", "Amir part vers le pré, le ballon sous le bras."),
        L("narrateur", "Le cuir a de l'herbe, près de la clôture."),
        L("enfant-m", "Il rebondit dans le pré !"),
        L("narrateur", "À la barrière, le ballon manque de filer."),
        L("narrateur", "La corde des balançoires lui revient aux doigts, trop vite."),
        L("narrateur", "Il s'arrête, le cuir serré."),
        L("enfant-m", "J'ouvre, puis il vient."),
        L("narrateur", "Il pose, ouvre, reprend."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("maman", "Tu as vu."),
        L("narrateur", "Au bac du pré, la paume trouve l'éclat."),
        L("narrateur", "L'eau arrive, presque trop tard."),
        L("narrateur", "Le ballon a de l'herbe, près de la clôture."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "La corde, derrière, se tait."),
        L("narrateur", "Le pré sent le foin."),
    ],
    (3, 2, 1): [
        L("narrateur", "Amir quitte les balançoires, le seau à l'anse."),
        L("narrateur", "L'herbe a mouillé le bord."),
        L("enfant-m", "L'anse, et la poignée !"),
        L("narrateur", "Les deux sonnent, vides."),
        L("narrateur", "La toile s'accroche à l'anse."),
        L("narrateur", "Il pose le seau, loin de la corde."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Ma main, ici."),
        L("papa", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat."),
        L("narrateur", "Il lève, sans l'anse."),
        L("narrateur", "Une seconde, plus rien."),
        L("narrateur", "Puis l'eau tombe, froide."),
        L("narrateur", "L'anse froide garde une goutte, juste sous l'éclat."),
        L("narrateur", "La flamme se relève."),
        L("narrateur", "L'herbe de la haie reste au bord."),
    ],
    (3, 2, 2): [
        L("narrateur", "Amir porte le seau vers le poulailler."),
        L("narrateur", "L'ombre du seau coupe le grillage, nette."),
        L("narrateur", "Les poules se jettent."),
        L("enfant-m", "L'anse, et le loquet !"),
        L("narrateur", "Le seau penche, l'eau saute."),
        L("narrateur", "Il pose l'anse, loin des pattes."),
        L("enfant-m", "Le loquet, puis vous."),
        L("narrateur", "L'éclat de zinc lui revient."),
        L("maman", "Tu as vu."),
        L("narrateur", "Il ouvre, une main libre."),
        L("narrateur", "Il pose l'eau, après."),
        L("narrateur", "Une poule boit, le bec contre le seau."),
        L("narrateur", "L'ombre du seau coupe le grillage."),
        L("narrateur", "La lanterne n'est pas morte."),
        L("narrateur", "L'herbe de la haie reste au bord."),
        L("narrateur", "Amir se redresse, calme."),
    ],
    (3, 2, 3): [
        L("narrateur", "Amir porte le seau vers le pré."),
        L("narrateur", "L'herbe de la haie mouille le bord."),
        L("enfant-m", "Je me faufile !"),
        L("narrateur", "L'anse cogne la barrière."),
        L("narrateur", "L'eau penche, une goutte tombe."),
        L("narrateur", "Il recule, les deux mains sur le seau."),
        L("enfant-m", "J'ouvre, puis je passe."),
        L("narrateur", "Il pose, ouvre, reprend."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("papa", "Tu as vu."),
        L("narrateur", "Au bac du pré, il verse, lent."),
        L("narrateur", "L'herbe de la haie mouille le bord."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "Ça a failli se vider."),
        L("narrateur", "La corde, derrière, se tait."),
        L("narrateur", "Le pré sent le foin."),
    ],
    (3, 3, 1): [
        L("narrateur", "Amir quitte les balançoires, le doudou contre lui."),
        L("narrateur", "Le vent de la haie a touché l'oreille."),
        L("enfant-m", "Il essuie, et je tire !"),
        L("narrateur", "La toile colle à l'oreille."),
        L("narrateur", "La pompe se tait."),
        L("narrateur", "Il glisse le doudou sous le bras."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("enfant-m", "Ma main, ici."),
        L("maman", "Tu as vu."),
        L("narrateur", "La paume trouve l'éclat, loin de la toile."),
        L("narrateur", "Il lève, l'autre main vide."),
        L("narrateur", "Une seconde, plus rien."),
        L("narrateur", "Puis l'eau arrive."),
        L("narrateur", "Le doudou a senti l'eau, puis le zinc."),
        L("narrateur", "La flamme se relève."),
        L("narrateur", "L'oreille a pris le vent de la haie."),
    ],
    (3, 3, 2): [
        L("narrateur", "Amir part vers le poulailler, le doudou à la main."),
        L("narrateur", "Le loquet demande l'autre main."),
        L("enfant-m", "Je tiens les deux !"),
        L("narrateur", "Le doudou glisse vers la paille."),
        L("narrateur", "Une poule le picore, presque."),
        L("narrateur", "Il le serre sous le bras, puis ouvre."),
        L("enfant-m", "Toi, à l'abri."),
        L("narrateur", "L'éclat de zinc lui revient."),
        L("papa", "Tu as vu."),
        L("narrateur", "L'eau vient, une main libre."),
        L("narrateur", "L'oreille grise a un peu de paille."),
        L("narrateur", "Une poule picore à côté, puis s'en va."),
        L("narrateur", "La lanterne n'est pas morte."),
        L("narrateur", "Amir reprend le doudou, sans courir."),
        L("narrateur", "Le vent de la haie a séché l'oreille."),
        L("narrateur", "Il souffle, calme."),
    ],
    (3, 3, 3): [
        L("narrateur", "Amir part vers le pré, le doudou contre lui."),
        L("narrateur", "L'herbe haute frotte le tissu."),
        L("enfant-m", "Il vole, et je marche !"),
        L("narrateur", "À la barrière, le tissu s'accroche."),
        L("narrateur", "Il tire, trop fort, et bute."),
        L("enfant-m", "Je le prends, puis j'ouvre."),
        L("narrateur", "Il ramasse, ouvre, passe."),
        L("narrateur", "L'éclat de zinc lui revient, froid."),
        L("maman", "Tu as vu."),
        L("narrateur", "Au bac du pré, la paume trouve l'éclat."),
        L("narrateur", "L'eau arrive, presque trop tard."),
        L("narrateur", "Le doudou a l'odeur de l'herbe haute."),
        L("narrateur", "La lanterne, loin, se relève."),
        L("narrateur", "La corde, derrière, se tait."),
        L("narrateur", "Amir serre le tissu, sans courir."),
        L("narrateur", "Le pré sent le foin mouillé."),
    ],
}

FIN = {
    (1, 1, 1): [
        L("narrateur", "Le ballon garde un rond d'eau, face à l'éclat."),
        L("narrateur", "Amir a les deux mains libres, à présent."),
        L("enfant-m", "Elle a chanté, papa."),
        L("papa", "Oui, quand ta main était seule."),
        L("maman", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont joué au bac à sable."),
        L("narrateur", "Le cuir a poussé, trop vite, puis s'est tu."),
        L("narrateur", "L'éclat de zinc cligne, faible, sur la poignée."),
        L("narrateur", "Le rond d'eau tremble, face à l'éclat."),
    ],
    (1, 1, 2): [
        L("narrateur", "Une poule picore le cuir, puis s'en va."),
        L("narrateur", "Amir reprend le ballon, sans courir."),
        L("enfant-m", "Elles ont bu, maman."),
        L("maman", "Oui, après le loquet."),
        L("papa", "Le bac d'eau n'est plus bas."),
        L("narrateur", "Ils ont quitté le bac à sable."),
        L("narrateur", "Le ballon a roulé, trop loin, puis attendu."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "Une poule picore le cuir, puis s'en va."),
    ],
    (1, 1, 3): [
        L("narrateur", "Le cuir rouge a une herbe collée, plate."),
        L("narrateur", "Amir le serre sous le bras, sans rebond."),
        L("enfant-m", "La barrière, puis le cuir."),
        L("papa", "Oui, comme ça."),
        L("maman", "Le pré a de l'eau, à présent."),
        L("narrateur", "Ils ont quitté le bac à sable."),
        L("narrateur", "Le ballon a failli tomber, à la barrière."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "Le cuir rouge a une herbe collée, plate."),
    ],
    (1, 2, 1): [
        L("narrateur", "L'eau fait ting, au fond du seau."),
        L("narrateur", "Amir tient l'anse, l'autre main vide."),
        L("enfant-m", "Elle a chanté, dans le seau."),
        L("papa", "Oui, quand l'anse était posée."),
        L("maman", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont joué au bac à sable."),
        L("narrateur", "Le seau a sonné, vide, puis plein."),
        L("narrateur", "L'éclat de zinc cligne, juste au-dessus."),
        L("narrateur", "Un grain de sable nage, au fond, minuscule."),
    ],
    (1, 2, 2): [
        L("narrateur", "Une poule boit, le bec contre le zinc du seau."),
        L("narrateur", "Amir a posé l'anse, puis le loquet."),
        L("enfant-m", "Elles ont bu, sans tout renverser."),
        L("maman", "Oui, loin des pattes."),
        L("papa", "Le bac d'eau n'est plus bas."),
        L("narrateur", "Ils ont quitté le bac à sable."),
        L("narrateur", "L'eau a failli sauter, près des ailes."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "Une poule boit, le bec contre le zinc du seau."),
    ],
    (1, 2, 3): [
        L("narrateur", "Le seau laisse un cercle humide dans l'herbe."),
        L("narrateur", "Amir a ouvert, puis passé."),
        L("enfant-m", "Une goutte est tombée, maman."),
        L("maman", "Une seule, pas tout le seau."),
        L("papa", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté le bac à sable."),
        L("narrateur", "L'anse a cogné, puis attendu."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "Le seau laisse un cercle humide dans l'herbe."),
    ],
    (1, 3, 1): [
        L("narrateur", "Une goutte brille sur l'oreille, puis sèche."),
        L("narrateur", "Amir serre le doudou, l'autre main vide."),
        L("enfant-m", "Il a senti l'eau, papa."),
        L("papa", "Oui, après ta paume sur l'éclat."),
        L("maman", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont joué au bac à sable."),
        L("narrateur", "Le tissu a essuyé, trop vite, puis attendu."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("narrateur", "Une goutte brille sur l'oreille, puis sèche."),
    ],
    (1, 3, 2): [
        L("narrateur", "Le doudou a une paille coincée dans l'oreille."),
        L("narrateur", "Amir l'a mis à l'abri, sous le bras."),
        L("enfant-m", "Le loquet, puis lui."),
        L("maman", "Oui, une main à la fois."),
        L("papa", "Les poules ont bu."),
        L("narrateur", "Ils ont quitté le bac à sable."),
        L("narrateur", "Le doudou a failli glisser, vers les pattes."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "Le doudou a une paille coincée dans l'oreille."),
    ],
    (1, 3, 3): [
        L("narrateur", "L'herbe haute a parfumé le tissu gris."),
        L("narrateur", "Amir le serre, sans le traîner."),
        L("enfant-m", "Il était lourd, d'herbe."),
        L("papa", "Oui, quand tu l'as ramassé."),
        L("maman", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté le bac à sable."),
        L("narrateur", "Le doudou a traîné, puis il a marché."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "L'herbe haute a parfumé le tissu gris."),
    ],
    (2, 1, 1): [
        L("narrateur", "Le ballon s'est tu contre le zinc, une paille au cuir."),
        L("narrateur", "Amir a les deux mains libres."),
        L("enfant-m", "Il a glissé, comme la rampe."),
        L("papa", "Puis tu l'as posé."),
        L("maman", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "Le cuir a poussé, trop vite, puis s'est tu."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("narrateur", "La paille de rampe sèche sur le cuir, près du zinc."),
    ],
    (2, 1, 2): [
        L("narrateur", "Une paille de rampe reste collée au cuir."),
        L("narrateur", "Amir reprend le ballon, sans se faufiler."),
        L("enfant-m", "Il était sous le grillage, maman."),
        L("maman", "Oui, trop loin."),
        L("papa", "Les poules ont bu."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "Le cuir a roulé, puis attendu derrière le pied."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "Une paille de rampe reste collée au cuir."),
    ],
    (2, 1, 3): [
        L("narrateur", "Le ballon roule une fois, dans l'herbe, puis s'arrête."),
        L("narrateur", "Amir ne court pas après."),
        L("enfant-m", "La barrière, puis le cuir."),
        L("papa", "Oui, comme ça."),
        L("maman", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "Le ballon a failli filer, à la barrière."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "Le ballon roule une fois, dans l'herbe, puis s'arrête."),
    ],
    (2, 2, 1): [
        L("narrateur", "Le seau sonne, plein, sous la poignée rêche."),
        L("narrateur", "Amir tient l'anse, l'autre main vide."),
        L("enfant-m", "Elle a chanté, dans le seau."),
        L("maman", "Oui, quand l'anse était au pied de la rampe."),
        L("papa", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "Le seau a sonné, vide, contre la marche, puis plein."),
        L("narrateur", "L'éclat de zinc cligne, juste au-dessus."),
        L("narrateur", "Une paille de rampe nage, au fond."),
    ],
    (2, 2, 2): [
        L("narrateur", "L'anse cliquette, puis se tait près du grillage."),
        L("narrateur", "Amir a posé, puis ouvert."),
        L("enfant-m", "Elles ont bu, papa."),
        L("papa", "Oui, loin des pattes."),
        L("maman", "Le bac d'eau n'est plus bas."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "L'eau a failli sauter, près des ailes."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "L'anse cliquette, puis se tait près du grillage."),
    ],
    (2, 2, 3): [
        L("narrateur", "Une goutte de rampe nage dans l'eau du seau."),
        L("narrateur", "Amir a ouvert, puis passé."),
        L("enfant-m", "Elle a failli se vider, maman."),
        L("maman", "Puis tu as ouvert, large."),
        L("papa", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "L'anse a cogné, puis attendu."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "Une goutte de rampe nage dans l'eau du seau."),
    ],
    (2, 3, 1): [
        L("narrateur", "L'oreille grise a une goutte au bout."),
        L("narrateur", "Amir serre le doudou, l'autre main vide."),
        L("enfant-m", "Il a senti l'eau, papa."),
        L("papa", "Oui, après ta paume sur l'éclat."),
        L("maman", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "Le tissu a essuyé, trop vite, puis attendu."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("narrateur", "L'oreille grise a une goutte au bout."),
    ],
    (2, 3, 2): [
        L("narrateur", "Une paille de rampe reste sur le gris."),
        L("narrateur", "Amir a mis le doudou à l'abri."),
        L("enfant-m", "La poule a failli le picorer."),
        L("maman", "Puis tu l'as serré, sous le bras."),
        L("papa", "Les poules ont bu."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "Le doudou a glissé, puis attendu."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "Une paille de rampe reste sur le gris."),
    ],
    (2, 3, 3): [
        L("narrateur", "Le vent du pré a séché l'oreille."),
        L("narrateur", "Amir serre le doudou, sans le laisser voler."),
        L("enfant-m", "Il s'accrochait, à la barrière."),
        L("papa", "Puis tu l'as pris, puis tu as ouvert."),
        L("maman", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté le toboggan."),
        L("narrateur", "Le tissu a buté, puis passé."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "Le vent du pré a séché l'oreille."),
    ],
    (3, 1, 1): [
        L("narrateur", "Le ballon frotte la poignée rêche, puis s'arrête."),
        L("narrateur", "Amir a les deux mains libres."),
        L("enfant-m", "On a roulé, trop vite."),
        L("maman", "Puis tu l'as posé, loin de la haie."),
        L("papa", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "Le cuir a poussé, trop vite, puis s'est tu."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("narrateur", "Un brin de haie reste au cuir, près du zinc."),
    ],
    (3, 1, 2): [
        L("narrateur", "Un bout de haie reste collé au cuir."),
        L("narrateur", "Amir reprend le ballon, sans tirer."),
        L("enfant-m", "Il s'était coincé, papa."),
        L("papa", "Oui, trop loin sous le grillage."),
        L("maman", "Les poules ont bu."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "Le cuir a passé, trop vite, puis attendu."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "Un bout de haie reste collé au cuir."),
    ],
    (3, 1, 3): [
        L("narrateur", "Le ballon a de l'herbe, près de la clôture."),
        L("narrateur", "Amir ne le laisse pas rebondir."),
        L("enfant-m", "La barrière, puis le cuir."),
        L("maman", "Oui, comme ça."),
        L("papa", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "Le ballon a failli filer, à la barrière."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "Le ballon a de l'herbe, près de la clôture."),
    ],
    (3, 2, 1): [
        L("narrateur", "L'anse froide garde une goutte, juste sous l'éclat."),
        L("narrateur", "Amir tient l'anse, l'autre main vide."),
        L("enfant-m", "Elle a chanté, dans le seau."),
        L("papa", "Oui, quand l'anse était loin de la corde."),
        L("maman", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "Le seau a sonné, vide, puis plein."),
        L("narrateur", "L'éclat de zinc cligne, juste au-dessus."),
        L("narrateur", "L'herbe de la haie reste au bord."),
    ],
    (3, 2, 2): [
        L("narrateur", "L'ombre du seau coupe le grillage, nette."),
        L("narrateur", "Amir a posé, puis ouvert."),
        L("enfant-m", "Elles ont bu, maman."),
        L("maman", "Oui, loin des pattes."),
        L("papa", "Le bac d'eau n'est plus bas."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "L'eau a failli sauter, près des ailes."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "L'ombre du seau coupe le grillage, nette."),
    ],
    (3, 2, 3): [
        L("narrateur", "L'herbe de la haie mouille le bord."),
        L("narrateur", "Amir a ouvert, puis passé."),
        L("enfant-m", "Une goutte est tombée, papa."),
        L("papa", "Une seule, pas tout le seau."),
        L("maman", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "L'anse a cogné, puis attendu."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "L'herbe de la haie mouille le bord."),
    ],
    (3, 3, 1): [
        L("narrateur", "Le doudou a senti l'eau, puis le zinc."),
        L("narrateur", "Amir le serre, l'autre main vide."),
        L("enfant-m", "Il a senti les deux, maman."),
        L("maman", "Oui, après ta paume sur l'éclat."),
        L("papa", "La toile tient, entre les lattes."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "Le tissu a essuyé, trop vite, puis attendu."),
        L("narrateur", "L'éclat de zinc cligne, sur la poignée."),
        L("narrateur", "Le doudou a senti l'eau, puis le zinc."),
    ],
    (3, 3, 2): [
        L("narrateur", "L'oreille grise a un peu de paille."),
        L("narrateur", "Amir a mis le doudou à l'abri."),
        L("enfant-m", "La poule a failli le picorer."),
        L("papa", "Puis tu l'as serré, sous le bras."),
        L("maman", "Les poules ont bu."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "Le doudou a glissé, puis attendu."),
        L("narrateur", "L'éclat de zinc reste sur la poignée, loin."),
        L("narrateur", "L'oreille grise a un peu de paille."),
    ],
    (3, 3, 3): [
        L("narrateur", "Le doudou a l'odeur de l'herbe haute."),
        L("narrateur", "Amir le serre, sans le laisser voler."),
        L("enfant-m", "Il s'accrochait, à la barrière."),
        L("maman", "Puis tu l'as pris, puis tu as ouvert."),
        L("papa", "Le pré a de l'eau."),
        L("narrateur", "Ils ont quitté les balançoires."),
        L("narrateur", "Le tissu a buté, puis passé."),
        L("narrateur", "L'éclat de zinc cligne, loin, à la cour."),
        L("narrateur", "Le doudou a l'odeur de l'herbe haute."),
    ],
}

Q_FIELDS = {
    "expected_answer": "zinc",
    "accepted_examples": (
        "zinc | éclat | éclat de zinc | un éclat de zinc | la poignée | "
        "sur la poignée | l'éclat | eclat"
    ),
    "retry_prompt": "Un petit éclat brille. Qu'est-ce qui brille sur la poignée ?",
}

SONS_L1 = {1: "poule,sable", 2: "bois,lanterne", 3: "vent,corde"}
SONS_L2 = {1: "ballon,toile", 2: "seau,zinc", 3: "doudou,tissu"}
SONS_L3 = {1: "pompe,eau", 2: "poule,grillage", 3: "vent,herbe"}
SONS_FIN = {1: "pompe,lanterne", 2: "poule,eau", 3: "vent,foin"}


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
            s[f"{p2}_T0003_P0000"] = T3[(i, j)]
            meta[f"{p2}_T0003_P0000"] = {
                "option_1_label": "la pompe",
                "option_2_label": "le poulailler",
                "option_3_label": "le pré",
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
        return "pompe,lanterne"
    if kind in {"transition_question", "passage_question"}:
        return ""
    if kind == "passage_fin":
        return SONS_FIN.get(k or 1, "pompe,lanterne")
    if cid.endswith("_C0001"):
        return "cour"
    if i and "_T0002_P000" in cid and "_T0003_" not in cid:
        if cid.endswith(("_P0001", "_P0002", "_P0003")):
            return SONS_L2.get(j or 1, "toile")
        return ""
    if "_T0003_P000" in cid and cid[-1] in "123":
        return SONS_L3.get(k or 1, "pompe")
    if i:
        return SONS_L1.get(i, "cour")
    return "cour"


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
        extra["emphasis"] = "éclat de zinc"
    elif prof == "clue":
        extra["emphasis"] = "poignée"
    elif prof == "confirm":
        extra["emphasis"] = "éclat de zinc"
    elif prof == "resolution":
        extra["emphasis"] = "éclat de zinc" if "éclat" in low else "pompe"
    elif prof == "ending":
        extra["emphasis"] = "éclat de zinc" if "éclat" in low else None
    elif prof == "action":
        extra["emphasis"] = "pompe" if "pompe" in low else None
    elif prof == "obstacle":
        extra["emphasis"] = None
    return extra


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
    enc = sum(1 for cid, lines in scripts.items() for ln in lines if "en ce moment" in ln.lower())
    if enc != 1:
        raise SystemExit(f"en ce moment count={enc}")
    print(f"preview {SID} {n} mots  chunks={len(scripts)}")


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
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = out_chunks
    check(SID, out["age_band"], out["chunks"])
    joined = "\n".join(c["script"] for c in out_chunks).lower()
    for bad in BAN + TICS:
        if bad in joined:
            raise SystemExit(f"{SID} extra interdit: {bad}")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment ≠ 1")
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
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        f"- **Titre noyau :** *{TITLE}*\n"
        "- **Public :** N2 (≤ 15 mots/phrase)\n"
        "- **Leçon :** AUT.ROU.001 — une chose puis l'autre, vécue "
        "(poignée et verre ensemble : ça colle ; une main sur l'éclat, l'autre vide)\n"
        f"- **Personnages :** {CHARS} (un seul enfant)\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "À cette heure, la pompe devrait chanter. Elle se tait. Le verre de la "
        "lanterne est tiède sous la paume. Une toile tient entre deux lattes. "
        "Sur la poignée, un éclat de zinc cligne. Amir veut faire chanter la pompe "
        "avant que la flamme meure. Papa veut les poules. Amir prend poignée et "
        "verre ensemble : la toile colle, la pompe refuse, la flamme se baisse. "
        "Le sourire disparaît. Maman s'accroupit. Bac, toboggan ou balançoires : "
        "il fonce, ça rate. Ballon, seau ou doudou : seconde ruse, il refuse de "
        "foncer, retrouve l'éclat. Pompe, poulailler ou pré : une main sur l'éclat, "
        "l'autre vide. L'eau arrive, presque trop tard. La toile tient.\n\n"
        "## Vécu\n\n"
        "Ferme, cour, grange, foin mouillé, paille, poule sur le zinc, toile, "
        "lanterne, éclat de zinc, pompe coincée. Impatience (je veux les deux), "
        "découragement (sourire disparu, poitrine, épaules), fierté calme "
        "(une main, l'autre vide). Merci vécu à l'éclat nommé. Question : "
        "qu'est-ce qui brille sur la poignée. T1 bac / toboggan / balançoires "
        "(coins, pas d'équipement retiré). T2 ballon / seau / doudou. "
        "T3 pompe / poulailler / pré. Monde ≠ TREE-DIF-040 (lait, veau).\n\n"
        "## Vu et corrigé\n\n"
        "P2 F-NAR-019 example4 v2. Ouverture inventée (son manquant : la pompe "
        "devrait chanter), pas les cinq manières listées. Indice unique : éclat "
        "de zinc, payé au climax (paume sur l'éclat). Corps : sourire disparaît, "
        "envie et inquiétude, adulte à la même hauteur. 2e ruse plus maligne "
        "(cuir, anse, oreille) ; refuse de foncer ; personne ne donne le geste. "
        "Dénouement qui a failli (une seconde, plus rien ; flamme trop basse). "
        "Pas gabarit example3. Tics encore / déjà / tout doux / tout calme "
        "retirés. Troupe D16 Amir seul. 27 fins, 27 L3, 27 dernières images. "
        "TTS par chunk : notes, text_ssml, text_xai_tags, piper 1.10–1.30. "
        f"`slow` = choix, indice, fins. `check()` N2 OK. Chemins {mn}–{mx} mots, "
        "moyenne {moy}. Pas apply.\n\n"
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
        "- papa/maman parlent, une question, un merci vécu\n"
        "- `en ce moment` une fois\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
