#!/usr/bin/env python3
"""TREE-AUT-030 — F-NAR-019 v2. Raphaël, bouilloire, bateaux. N2. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words

SID = "TREE-AUT-030"
LIM = 15
TICS = ("tout doux", "tout calme", "encore", "déjà")
BAN = (
    "escargot", "loupe", "carnet bleu", "pots de menthe", "vélo rouge",
    "hugo", "sarah", "ranger", "tu ranges", "après le jeu",
    "mission accomplie", "j'ai compris", "on dirait que notre mission",
    "lumière couleur de miel", "gouttes pendent", "aujourd'hui",
    "grand-père", "maîtresse", "jardinier", "bibliothécaire", "gardienne",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 138, "speed": 0.96, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 280,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "croissant de buée",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=les bateaux veulent la flaque; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    },
    "choice": {
        "rate": "slow", "wpm": 112, "speed": 0.82, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 340,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": (
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton choix change le voyage; tempo=suspendu; "
            "sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "ce matin",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=la chaussette puis les bateaux; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 128, "speed": 0.90, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 290,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "chaussette",
        "note": (
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=un geste puis le suivant; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    },
    "action": {
        "rate": "medium", "wpm": 144, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 400, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": (
            "arc=action; intention=entraîner; emotion=élan; intensite=2; "
            "destinataire=enfant; sous_texte=l_objet change la ruse; tempo=vif; "
            "sourire=léger; respiration=courte"
        ),
    },
    "obstacle": {
        "rate": "medium", "wpm": 130, "speed": 0.92, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 540, "sentence": 310,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=le bateau n_atteint pas la flaque; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 136, "speed": 0.95, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=le croissant de buée guide; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    },
    "ending": {
        "rate": "slow", "wpm": 114, "speed": 0.84, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 350,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": (
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=la bouilloire s_est tue, le croissant reste; "
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


def split_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for raw in lines:
        role, phrase = raw.split("|", 1)
        parts = re.findall(r"[^.?!]+[.?!]", phrase.strip())
        if not parts:
            raise SystemExit(f"PUNCT {raw}")
        for p in parts:
            p = re.sub(r"\s+", " ", p).strip()
            out.append(f"{role}|{p}")
    return out


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


OPENING = [
    L("narrateur", "Les bateaux du rideau ont voyagé toute la nuit."),
    L("narrateur", "Ils n'ont pas bougé d'un fil."),
    L("narrateur", "Le matin, la bouilloire leur donne un faux vent."),
    L("narrateur", "Siff, tout aigu."),
    L("narrateur", "Un bateau du tissu est bleu."),
    L("narrateur", "Un bateau du tissu est jaune."),
    L("narrateur", "Sur le rebord, deux bateaux de papier."),
    L("narrateur", "Le bleu a le nez un peu plié."),
    L("narrateur", "Le jaune porte un croissant de buée."),
    L("narrateur", "La vapeur l'a dessiné, sans personne."),
    L("papa", "Tu as vu ce croissant, Raphaël ?"),
    L("enfant-m", "Il est mouillé, papa."),
    L("maman", "La bouilloire n'a pas fini."),
    L("narrateur", "Le couloir sent le savon."),
    L("narrateur", "Un gobelet attend près du lavabo."),
    L("narrateur", "En ce moment, Raphaël veut partir."),
    L("enfant-m", "Les bateaux, au parc, vite !"),
    L("narrateur", "Il attrape les bateaux et une chaussure."),
    L("narrateur", "Le jaune glisse sous la chaise."),
    L("enfant-m", "Oh non."),
    L("narrateur", "Le croissant de buée frotte le tapis."),
    L("narrateur", "Le sourire de Raphaël disparaît."),
    L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    L("papa", "On s'accroupit ?"),
    L("narrateur", "Papa se met à sa hauteur."),
    L("maman", "La chaussette, d'abord ?"),
    L("narrateur", "Raphaël pose la chaussure."),
    L("narrateur", "Il enfile la chaussette tiède."),
    L("narrateur", "Puis il glisse les bateaux dans sa poche."),
    L("enfant-m", "Le croissant est là, dans la poche."),
    L("papa", "La bouilloire s'est tue."),
    L("narrateur", "L'eau est prête."),
    L("enfant-m", "On y va ?"),
    L("maman", "Oui."),
    L("maman", "La flaque du parc attend."),
    L("narrateur", "Le manteau attend sur le crochet."),
]

T1 = [
    L("narrateur", "La flaque du parc brille, mince."),
    L("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
    L("maman", "Où les bateaux tentent le voyage ?"),
]

L1 = {
    1: [
        L("narrateur", "Au parc, le bac sent le sable humide."),
        L("narrateur", "Une flaque mince brille au fond."),
        L("enfant-m", "C'est le port !"),
        L("enfant-m", "Comme le rideau."),
        L("papa", "Avant que le soleil la boive ?"),
        L("enfant-m", "Le jaune va jusqu'à l'eau."),
        L("narrateur", "Raphaël creuse trop vite, les deux mains."),
        L("narrateur", "Il pose les deux bateaux d'un coup."),
        L("narrateur", "Le bleu s'enfonce dans le sable mouillé."),
        L("narrateur", "Le jaune s'arrête, loin de l'eau."),
        L("enfant-m", "Il n'arrive pas."),
        L("narrateur", "Le croissant de buée regarde le ciel."),
        L("narrateur", "Les épaules de Raphaël baissent."),
        L("maman", "Tu le vois, ce croissant ?"),
        L("enfant-m", "Il est un peu pâle."),
        L("narrateur", "Maman s'accroupit, à sa hauteur."),
    ],
    2: [
        L("narrateur", "La rampe du toboggan est froide sous la main."),
        L("narrateur", "En bas, une flaque tremble."),
        L("enfant-m", "La mer de la rampe !"),
        L("maman", "Le jaune glisse jusqu'à l'eau ?"),
        L("enfant-m", "Avec moi."),
        L("narrateur", "Raphaël pose le bateau, puis se lance."),
        L("narrateur", "Trop vite."),
        L("narrateur", "Le papier s'envole à mi-pente."),
        L("narrateur", "Il tombe dans l'herbe, pas dans l'eau."),
        L("enfant-m", "Il n'est pas arrivé."),
        L("narrateur", "Le croissant de buée a de l'herbe."),
        L("narrateur", "Raphaël reste en haut, les joues chaudes."),
        L("papa", "On s'accroupit, en bas ?"),
        L("narrateur", "Papa se met à sa hauteur, près de l'herbe."),
        L("enfant-m", "Je le veux dans l'eau."),
    ],
    3: [
        L("narrateur", "Les chaînes des balançoires sont froides."),
        L("narrateur", "Elles font un bruit de goutte."),
        L("narrateur", "Près des pieds, une flaque tremble."),
        L("enfant-m", "Le golfe des chaînes."),
        L("papa", "Les bateaux tiennent, si on pousse ?"),
        L("enfant-m", "Je les tiens."),
        L("narrateur", "Raphaël pompe trop fort."),
        L("narrateur", "Le jaune glisse, tombe sur la terre sèche."),
        L("enfant-m", "Zut."),
        L("narrateur", "Loin de l'eau."),
        L("narrateur", "Le croissant de buée a de la poussière."),
        L("narrateur", "Raphaël pose un pied au sol, le menton bas."),
        L("maman", "Je m'accroupis, d'accord ?"),
        L("narrateur", "Maman s'accroupit, à sa hauteur."),
        L("enfant-m", "Il n'est pas au golfe."),
    ],
}

Q = {
    1: [
        L("narrateur", "Raphaël a un bateau dans le sable."),
        L("papa", "Il s'est préparé comment, ce matin ?"),
    ],
    2: [
        L("narrateur", "Le bateau a quitté la rampe."),
        L("maman", "Raphaël s'est préparé comment ?"),
    ],
    3: [
        L("narrateur", "Les bateaux ont voyagé sur ses genoux."),
        L("papa", "Il s'est préparé comment, Raphaël ?"),
    ],
}

C = {
    1: [
        L("narrateur", "Oui."),
        L("narrateur", "D'abord la chaussette tiède."),
        L("narrateur", "Ensuite les bateaux dans la poche."),
        L("papa", "Merci, Raphaël."),
        L("maman", "La bouilloire a attendu, elle aussi."),
        L("enfant-m", "On continue ?"),
        L("papa", "On prend un jeu, près du bac ?"),
        L("narrateur", "Un grain de sable brille sur son genou."),
    ],
    2: [
        L("narrateur", "Oui."),
        L("narrateur", "D'abord la chaussette."),
        L("narrateur", "Ensuite les bateaux."),
        L("maman", "Merci, Raphaël."),
        L("papa", "Le sifflet s'est tu, à la maison."),
        L("enfant-m", "On continue ?"),
        L("maman", "On prend un jeu, près de la rampe ?"),
        L("narrateur", "Une feuille reste collée au métal."),
    ],
    3: [
        L("narrateur", "Oui."),
        L("narrateur", "La chaussette d'abord."),
        L("narrateur", "Les bateaux ensuite."),
        L("papa", "Merci, Raphaël."),
        L("maman", "Le manteau a attendu, au crochet."),
        L("enfant-m", "On continue ?"),
        L("papa", "On prend un jeu, près des chaînes ?"),
        L("narrateur", "La chaîne se tait, un instant."),
    ],
}

T2 = {
    1: [
        L("maman", "Quel jeu aide le port ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    2: [
        L("papa", "Quel jeu aide la mer de la rampe ?"),
        L("maman", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    3: [
        L("maman", "Quel jeu aide le golfe ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
}

L2 = {
    (1, 1): [
        L("narrateur", "Près du bac, le ballon rouge attend."),
        L("narrateur", "Il est lisse, un peu frais."),
        L("enfant-m", "Il pousse le bateau !"),
        L("narrateur", "Raphaël frappe trop fort."),
        L("narrateur", "Le ballon chasse le jaune vers le sable sec."),
        L("enfant-m", "Plus loin de l'eau !"),
        L("narrateur", "Un rebond soulève une vague de grains."),
        L("enfant-m", "Une mer ?"),
        L("papa", "C'est du sable, Raphaël."),
        L("narrateur", "Raphaël refuse de foncer."),
        L("narrateur", "Il regarde le croissant de buée."),
        L("enfant-m", "Il pointe la petite flaque."),
        L("maman", "Tu l'as vu, toi."),
    ],
    (1, 2): [
        L("narrateur", "Près du bac, le seau jaune sonne."),
        L("narrateur", "L'anse est froide."),
        L("enfant-m", "De l'eau, beaucoup !"),
        L("narrateur", "Raphaël verse d'un coup."),
        L("narrateur", "Le flot emporte le jaune trop loin."),
        L("narrateur", "Le bateau finit dans une empreinte."),
        L("enfant-m", "Un autre port ?"),
        L("maman", "C'est un pied, pas la mer."),
        L("narrateur", "Le croissant de buée est pâle, lavé."),
        L("narrateur", "Raphaël s'arrête, les mains mouillées."),
        L("enfant-m", "Un tout petit filet, alors."),
        L("papa", "Tu regardes le croissant ?"),
        L("enfant-m", "Il montre la flaque mince."),
    ],
    (1, 3): [
        L("narrateur", "Près du bac, le doudou gris attend."),
        L("narrateur", "Une oreille a du sable."),
        L("enfant-m", "Il sera le quai."),
        L("narrateur", "Raphaël jette le doudou vers l'eau."),
        L("narrateur", "Le tissu s'imbibe, lourd."),
        L("narrateur", "Le bateau colle à l'oreille grise."),
        L("enfant-m", "Il n'avance plus."),
        L("papa", "Le quai a trop bu."),
        L("narrateur", "L'empreinte mouillée ressemble à une mer."),
        L("narrateur", "Raphaël refuse d'y pousser."),
        L("narrateur", "Il décolle le papier, tout plat."),
        L("enfant-m", "Le croissant est là."),
        L("maman", "Sur la voile, oui."),
    ],
    (2, 1): [
        L("narrateur", "Au pied du toboggan, le ballon attend."),
        L("narrateur", "Il est froid, près de la rampe."),
        L("enfant-m", "Il sera le butoir."),
        L("narrateur", "Raphaël lance le bateau trop fort."),
        L("narrateur", "Le papier tape le ballon, rebondit."),
        L("narrateur", "Il remonte la rampe, à l'envers."),
        L("enfant-m", "Il recule !"),
        L("maman", "Le butoir l'a renvoyé."),
        L("narrateur", "Le ballon roule vers l'herbe."),
        L("narrateur", "Le bateau veut le suivre."),
        L("narrateur", "Raphaël pose une main, refuse de foncer."),
        L("enfant-m", "Le croissant pointe en bas."),
        L("papa", "Vers la flaque, pas vers le ballon."),
    ],
    (2, 2): [
        L("narrateur", "Au toboggan, le seau sonne contre une marche."),
        L("narrateur", "L'anse est froide."),
        L("enfant-m", "Le bateau rentre là, en bas."),
        L("narrateur", "Raphaël verse le seau sur la rampe."),
        L("narrateur", "L'eau file trop vite, brillante."),
        L("narrateur", "Le papier se colle au plastique mouillé."),
        L("enfant-m", "Il est coincé !"),
        L("papa", "Trop d'eau, trop de glisse."),
        L("narrateur", "Une goutte cache le croissant de buée."),
        L("narrateur", "Raphaël attend que la rampe sèche un peu."),
        L("enfant-m", "Juste un filet, au pied."),
        L("maman", "Tu as vu le croissant ?"),
        L("enfant-m", "Il revient, pâle."),
    ],
    (2, 3): [
        L("narrateur", "Au toboggan, le doudou a vu la rampe."),
        L("narrateur", "L'oreille grise est un peu froide."),
        L("enfant-m", "Il attrape le bateau, en bas."),
        L("narrateur", "Raphaël glisse le papier, puis le doudou."),
        L("narrateur", "Le bateau atterrit sur le ventre gris."),
        L("narrateur", "Pas dans l'eau."),
        L("enfant-m", "Une île ?"),
        L("maman", "Une île sèche, Raphaël."),
        L("narrateur", "Le doudou fait un creux, comme un port."),
        L("narrateur", "Raphaël refuse d'y laisser le jaune."),
        L("narrateur", "Il soulève l'oreille, tout plat."),
        L("enfant-m", "Le croissant veut la flaque."),
        L("papa", "À côté, pas dessus."),
    ],
    (3, 1): [
        L("narrateur", "Près des chaînes, le ballon a de l'herbe."),
        L("narrateur", "Un brin colle au cuir."),
        L("enfant-m", "On roule, et le bateau voyage."),
        L("narrateur", "Raphaël pousse le ballon en se balançant."),
        L("narrateur", "Le jaune s'envole, disparaît dans l'herbe."),
        L("enfant-m", "Je le vois plus !"),
        L("papa", "L'herbe bouge, comme de l'eau."),
        L("narrateur", "Raphaël veut foncer dans les brins."),
        L("narrateur", "Puis il s'arrête."),
        L("narrateur", "Sous une chaîne, le croissant de buée brille."),
        L("enfant-m", "Là."),
        L("enfant-m", "À l'ombre."),
        L("maman", "Pas dans la fausse mer."),
        L("narrateur", "Le ballon s'immobilise, un brin collé."),
    ],
    (3, 2): [
        L("narrateur", "Près des balançoires, le seau est dans l'herbe."),
        L("narrateur", "L'anse est froide, près de la corde."),
        L("enfant-m", "Le golfe, dans le seau."),
        L("narrateur", "Raphaël pose le seau sous le siège."),
        L("narrateur", "Il se balance, trop fort."),
        L("narrateur", "Le bateau tombe à côté, pas dedans."),
        L("enfant-m", "À côté !"),
        L("maman", "L'eau tourne, dans le seau."),
        L("narrateur", "Le papier voudrait y tourner aussi."),
        L("narrateur", "Raphaël attend que l'eau se taise."),
        L("enfant-m", "Le croissant, quand c'est calme."),
        L("papa", "Tu le poses, sans pomper ?"),
        L("enfant-m", "Oui."),
        L("enfant-m", "Après."),
    ],
    (3, 3): [
        L("narrateur", "Près des balançoires, le doudou a du vent."),
        L("narrateur", "L'oreille molle clignote."),
        L("enfant-m", "Il s'assoit avec moi."),
        L("narrateur", "Raphaël pompe trop fort, les deux sur les genoux."),
        L("narrateur", "Doudou et bateau tombent sur la terre sèche."),
        L("enfant-m", "Aïe."),
        L("papa", "Le golfe est l'eau, pas la terre."),
        L("narrateur", "Le doudou a un creux, comme un port."),
        L("narrateur", "Raphaël refuse d'y pousser le jaune."),
        L("narrateur", "Il ramasse le papier, tout plat."),
        L("enfant-m", "Le croissant pointe la flaque qui tremble."),
        L("maman", "Celle des chaînes, oui."),
        L("narrateur", "L'oreille grise a de la poussière."),
    ],
}


def t3_lines(i: int, j: int) -> list[str]:
    start = {
        (1, 1): "papa|Le ballon s'est tu. On s'arrête où ?",
        (1, 2): "maman|Le seau a versé. On s'arrête où ?",
        (1, 3): "papa|Le doudou a bu. On s'arrête où ?",
        (2, 1): "maman|Le ballon a renvoyé. On s'arrête où ?",
        (2, 2): "papa|La rampe sèche. On s'arrête où ?",
        (2, 3): "maman|L'île grise attend. On s'arrête où ?",
        (3, 1): "papa|L'herbe a caché. On s'arrête où ?",
        (3, 2): "maman|L'eau du seau se tait. On s'arrête où ?",
        (3, 3): "papa|Le doudou a de la poussière. On s'arrête où ?",
    }[(i, j)]
    return [
        start,
        L("maman", "Le banc, le portail, ou le manteau ?"),
        L("narrateur", "Tu choisis."),
    ]


L3 = {
    (1, 1, 1): [
        L("narrateur", "Ils vont vers le banc de bois."),
        L("narrateur", "Le bois est un peu froid."),
        L("enfant-m", "Le ballon pousse, d'ici."),
        L("narrateur", "Raphaël donne un coup, trop sec."),
        L("narrateur", "Le jaune file sous le banc."),
        L("enfant-m", "Il se cache !"),
        L("papa", "Tu regardes le croissant, d'abord ?"),
        L("narrateur", "Sous le bois, le croissant pointe la flaque."),
        L("narrateur", "Raphaël pose le ballon comme un mur."),
        L("narrateur", "Le bateau glisse, lent, jusqu'à l'eau."),
        L("enfant-m", "Il y est."),
        L("maman", "Tu l'as guidé, sans frapper."),
        L("narrateur", "Un grain de sable colle au croissant."),
    ],
    (1, 1, 2): [
        L("narrateur", "Ils marchent vers le portail."),
        L("narrateur", "Le métal est froid sous la main."),
        L("enfant-m", "Le ballon ouvre la mer !"),
        L("narrateur", "Le ballon file vers la rue."),
        L("narrateur", "Raphaël veut courir."),
        L("maman", "Le croissant, Raphaël ?"),
        L("narrateur", "Sur la voile, le croissant est pâle, du côté du parc."),
        L("narrateur", "Raphaël pose le ballon contre le portail."),
        L("narrateur", "Une flaque mince tremble près du pied."),
        L("narrateur", "Le jaune y entre, tout seul."),
        L("enfant-m", "Ici."),
        L("enfant-m", "Pas la rue."),
        L("papa", "Tu as regardé, avant de courir."),
        L("narrateur", "Le portail reste fermé, un instant."),
    ],
    (1, 1, 3): [
        L("narrateur", "Le manteau attend sur le crochet du parc."),
        L("narrateur", "Il est un peu frais."),
        L("enfant-m", "Le bateau rentre au chaud."),
        L("narrateur", "Raphaël glisse le jaune dans la poche trop vite."),
        L("narrateur", "Le papier se plie, le croissant disparaît."),
        L("enfant-m", "Je le vois plus."),
        L("papa", "La manche, d'abord ?"),
        L("narrateur", "Raphaël enfile une manche, puis l'autre."),
        L("narrateur", "Il pose le bateau à plat, dans la poche."),
        L("narrateur", "Le croissant reparaît, tiède comme la vapeur."),
        L("enfant-m", "Comme la bouilloire."),
        L("maman", "Il a voyagé, sans se cacher."),
        L("narrateur", "Un peu de vapeur froide reste dans le tissu."),
    ],
    (1, 2, 1): [
        L("narrateur", "Ils s'assoient sur le banc de bois."),
        L("narrateur", "Le seau sonne contre une planche."),
        L("enfant-m", "Je verse, d'ici."),
        L("narrateur", "L'eau tombe trop haut, éclabousse."),
        L("narrateur", "Le jaune part vers l'herbe."),
        L("enfant-m", "Zut."),
        L("maman", "Un filet, depuis le bois ?"),
        L("narrateur", "Raphaël incline l'anse, tout bas."),
        L("narrateur", "Le croissant pâle suit le filet."),
        L("narrateur", "Le bateau rejoint la flaque, sans nager trop loin."),
        L("enfant-m", "Le port est là."),
        L("papa", "Tu as versé moins, cette fois."),
        L("narrateur", "L'anse pose une ombre ronde sur le bois."),
    ],
    (1, 2, 2): [
        L("narrateur", "Près du portail, le seau penche."),
        L("narrateur", "Une flaque mince y attend."),
        L("enfant-m", "Je remplis le portail !"),
        L("narrateur", "L'eau fuit sous le métal, vers la rue."),
        L("enfant-m", "Elle s'en va !"),
        L("papa", "Le croissant, de quel côté ?"),
        L("narrateur", "Le croissant pâle reste côté parc."),
        L("narrateur", "Raphaël pose le seau comme un mur, bas."),
        L("narrateur", "Un filet court jusqu'à la flaque, pas plus loin."),
        L("narrateur", "Le jaune s'y installe."),
        L("enfant-m", "Il reste."),
        L("maman", "Tu as fermé la fuite, toi."),
        L("narrateur", "Le portail a une goutte, puis plus."),
    ],
    (1, 2, 3): [
        L("narrateur", "Raphaël prend le manteau, le seau à l'autre main."),
        L("narrateur", "Trop d'objets, d'un coup."),
        L("narrateur", "L'anse cogne, un peu d'eau tache le tissu."),
        L("enfant-m", "Oh."),
        L("maman", "Le manteau, d'abord ?"),
        L("narrateur", "Il pose le seau."),
        L("narrateur", "Il enfile une manche, puis l'autre."),
        L("narrateur", "Ensuite le seau, tout droit."),
        L("narrateur", "Le croissant, au fond, reste sec."),
        L("enfant-m", "Le bateau n'a pas bu."),
        L("papa", "Toi non plus, presque."),
        L("narrateur", "Une tache d'eau sèche sur la manche."),
        L("maman", "Le port rentre avec vous."),
    ],
    (1, 3, 1): [
        L("narrateur", "Sur le banc, le doudou a du sable à l'oreille."),
        L("enfant-m", "Il garde le port, ici."),
        L("narrateur", "Raphaël pose le doudou trop près de l'eau."),
        L("narrateur", "Le tissu boit, de nouveau lourd."),
        L("enfant-m", "Non !"),
        L("papa", "Le banc, d'abord, tout sec ?"),
        L("narrateur", "Raphaël installe le doudou sur le bois."),
        L("narrateur", "Puis le bateau, contre l'oreille sèche."),
        L("narrateur", "Le croissant de buée touche le bois, pas l'eau."),
        L("enfant-m", "Ils se parlent."),
        L("maman", "Le quai n'a pas trop bu."),
        L("narrateur", "Un grain reste sous l'ongle de Raphaël."),
        L("narrateur", "La flaque brille, en bas, sans les avaler."),
    ],
    (1, 3, 2): [
        L("narrateur", "Près du portail, le doudou sent le sable."),
        L("enfant-m", "Il ouvre, lui."),
        L("narrateur", "Raphaël tend l'oreille grise vers le loquet."),
        L("narrateur", "Le tissu glisse, le loquet reste."),
        L("enfant-m", "Il peut pas."),
        L("maman", "Ta main, d'abord ?"),
        L("narrateur", "Raphaël pose le doudou."),
        L("narrateur", "Il pousse le portail, tout seul."),
        L("narrateur", "Ensuite il glisse le bateau contre l'oreille."),
        L("narrateur", "Le croissant de buée voit le chemin du retour."),
        L("enfant-m", "On rentre, le port avec nous."),
        L("papa", "Le doudou n'ouvre pas."),
        L("papa", "Toi, oui."),
        L("narrateur", "Le métal se tait derrière eux."),
    ],
    (1, 3, 3): [
        L("narrateur", "Le manteau, le doudou, le bateau."),
        L("narrateur", "Raphaël veut tout mettre d'un coup."),
        L("narrateur", "L'oreille grise bloque la manche."),
        L("enfant-m", "Ça rentre pas."),
        L("papa", "Une manche, puis l'oreille ?"),
        L("narrateur", "Raphaël glisse un bras."),
        L("narrateur", "Puis l'autre bras."),
        L("narrateur", "Ensuite le doudou, contre lui."),
        L("narrateur", "Le bateau, à plat, dans la poche."),
        L("narrateur", "Le croissant de buée chauffe un peu."),
        L("enfant-m", "Ils sont ensemble, dans l'ordre."),
        L("maman", "Tu as fait de la place."),
        L("narrateur", "Un fil gris pend de la poche."),
    ],
    (2, 1, 1): [
        L("narrateur", "Au banc, près de la rampe, le ballon est froid."),
        L("enfant-m", "Butoir, ici."),
        L("narrateur", "Raphaël le pose trop près du bois."),
        L("narrateur", "Le bateau, relancé, tape le banc, rebondit."),
        L("enfant-m", "Pareil !"),
        L("maman", "Le ballon plus loin, le banc pour regarder ?"),
        L("narrateur", "Raphaël s'assoit."),
        L("narrateur", "Il place le ballon entre le banc et la flaque."),
        L("narrateur", "Le croissant de buée pointe l'eau, pas le cuir."),
        L("narrateur", "Le jaune glisse, s'arrête au bord, entre."),
        L("enfant-m", "La mer de la rampe."),
        L("papa", "Tu as changé le butoir."),
        L("narrateur", "Une feuille de la rampe sèche sur le bois."),
    ],
    (2, 1, 2): [
        L("narrateur", "Vers le portail, le ballon rebondit."),
        L("narrateur", "La rampe est derrière, la rue devant."),
        L("enfant-m", "Il veut la rue, lui."),
        L("papa", "Et le croissant ?"),
        L("narrateur", "Raphaël arrête le ballon du pied."),
        L("narrateur", "Sur la voile, le croissant penche vers la flaque du bas."),
        L("narrateur", "Il pose le ballon contre le portail, comme une porte."),
        L("narrateur", "Le jaune descend la dernière pente d'herbe."),
        L("narrateur", "Il rejoint l'eau, près du métal."),
        L("enfant-m", "Arrivé."),
        L("maman", "Sans suivre le ballon."),
        L("narrateur", "Le sifflet de la rampe, loin, se tait."),
        L("narrateur", "Le portail a un rond de cuir, un instant."),
    ],
    (2, 1, 3): [
        L("narrateur", "Raphaël enfile le manteau, le ballon sous le bras."),
        L("narrateur", "Le ballon glisse, tombe."),
        L("enfant-m", "Il veut pas."),
        L("maman", "Les manches, d'abord ?"),
        L("narrateur", "Une manche, puis l'autre."),
        L("narrateur", "Ensuite le ballon, contre la hanche."),
        L("narrateur", "Le bateau, à plat, dans la poche."),
        L("narrateur", "Le croissant de buée sent le froid de la rampe."),
        L("enfant-m", "Il a glissé, lui, pour de vrai."),
        L("papa", "Et il rentre, maintenant."),
        L("narrateur", "Le manteau a gardé le froid du métal."),
        L("narrateur", "La rampe reste loin, sèche."),
        L("maman", "La mer de la rampe a eu son bateau."),
    ],
    (2, 2, 1): [
        L("narrateur", "Sur le banc, Raphaël pose le seau trop plein."),
        L("narrateur", "L'eau lèche le bois."),
        L("enfant-m", "Le banc boit !"),
        L("papa", "Un peu moins, dans le seau ?"),
        L("narrateur", "Raphaël verse le surplus dans l'herbe."),
        L("narrateur", "Il incline un filet vers la flaque du bas."),
        L("narrateur", "Le croissant pâle réapparaît, hors de l'eau."),
        L("narrateur", "Le jaune quitte la rampe collante, rejoint la flaque."),
        L("enfant-m", "Il n'est plus coincé."),
        L("maman", "Tu as vidé un peu, d'abord."),
        L("narrateur", "Le seau pose son ombre sur le banc."),
        L("narrateur", "La rampe sèche au soleil."),
        L("narrateur", "Une goutte, seule, glisse, lente."),
    ],
    (2, 2, 2): [
        L("narrateur", "Près du portail, Raphaël veut laver la rampe."),
        L("narrateur", "Le seau penche vers le métal."),
        L("enfant-m", "Pour qu'il glisse mieux !"),
        L("maman", "La rampe est loin, là."),
        L("narrateur", "Raphaël s'arrête."),
        L("narrateur", "Il regarde le croissant de buée."),
        L("narrateur", "Pâle, il montre la flaque au pied du portail."),
        L("narrateur", "Un filet, juste là."),
        L("narrateur", "Le jaune y flotte, sans coller."),
        L("enfant-m", "Pas besoin de toute la rampe."),
        L("papa", "Tu as changé de mer."),
        L("narrateur", "L'anse cliquette près du loquet."),
        L("narrateur", "Le portail a une goutte, puis plus."),
    ],
    (2, 2, 3): [
        L("narrateur", "Le manteau, et le seau trop plein."),
        L("narrateur", "Raphaël verse un peu, d'abord, dans l'herbe."),
        L("enfant-m", "Pour pas tacher."),
        L("papa", "Puis les manches ?"),
        L("narrateur", "Une manche, puis l'autre."),
        L("narrateur", "Le seau, ensuite, l'anse froide."),
        L("narrateur", "Le bateau, à plat, dans la poche sèche."),
        L("narrateur", "Le croissant de buée n'a plus de goutte dessus."),
        L("enfant-m", "Il a séché, tout seul."),
        L("maman", "Comme la rampe."),
        L("narrateur", "Une goutte de rampe sèche dans la manche."),
        L("narrateur", "Le gobelet, à la maison, attend."),
        L("papa", "On lui racontera la mer."),
    ],
    (2, 3, 1): [
        L("narrateur", "Sur le banc, le doudou a vu le toboggan."),
        L("enfant-m", "L'île, sur le bois."),
        L("narrateur", "Raphaël pose le doudou, puis le bateau dessus."),
        L("narrateur", "Le papier reste sur le ventre, pas dans l'eau."),
        L("enfant-m", "Il voyage pas."),
        L("maman", "L'île pour s'asseoir."),
        L("maman", "L'eau, en bas ?"),
        L("narrateur", "Raphaël s'assoit, le doudou contre lui."),
        L("narrateur", "Il glisse le jaune le long du bois, vers la flaque."),
        L("narrateur", "Le croissant de buée quitte le tissu, rejoint l'eau."),
        L("enfant-m", "Toi, tu restes."),
        L("enfant-m", "Lui, il va."),
        L("papa", "Deux places, deux gestes."),
        L("narrateur", "L'oreille molle dépasse du banc."),
        L("narrateur", "La rampe, derrière, se tait."),
    ],
    (2, 3, 2): [
        L("narrateur", "Près du portail, le doudou a l'oreille froide."),
        L("enfant-m", "Il pousse le loquet."),
        L("narrateur", "L'oreille glisse, le métal reste fermé."),
        L("papa", "Ta main, puis lui ?"),
        L("narrateur", "Raphaël pousse le portail."),
        L("narrateur", "Il pose le doudou contre le pied, au sec."),
        L("narrateur", "Le bateau, ensuite, vers la flaque du seuil."),
        L("narrateur", "Le croissant de buée quitte l'île grise."),
        L("enfant-m", "Il a sa mer, tout près."),
        L("maman", "Sans atterrir sur le ventre."),
        L("narrateur", "L'oreille molle dépasse, près du métal."),
        L("narrateur", "Le loquet se tait."),
        L("papa", "Vous passez, dans l'ordre."),
    ],
    (2, 3, 3): [
        L("narrateur", "Le manteau attend, le doudou aussi."),
        L("narrateur", "Raphaël veut les deux, plus le bateau."),
        L("enfant-m", "Tout le monde, vite."),
        L("maman", "Les manches, d'abord ?"),
        L("narrateur", "Un bras, puis l'autre."),
        L("narrateur", "Le doudou, contre la poitrine."),
        L("narrateur", "Le bateau, à plat, dans la poche."),
        L("narrateur", "Le croissant de buée chauffe, loin de l'herbe."),
        L("enfant-m", "Il n'est plus collé."),
        L("papa", "La rampe l'a lâché."),
        L("narrateur", "Le papier jaune n'est plus collé à l'herbe."),
        L("narrateur", "La poche sent un peu le métal froid."),
        L("maman", "On rentre, la mer dans le tissu."),
    ],
    (3, 1, 1): [
        L("narrateur", "Sur le banc, près des chaînes, le ballon a de l'herbe."),
        L("enfant-m", "Je le cherche avec."),
        L("narrateur", "Raphaël roule le ballon sous le banc."),
        L("narrateur", "Le jaune n'est pas là."),
        L("enfant-m", "Perdu."),
        L("papa", "L'ombre de la chaîne, tu te souviens ?"),
        L("narrateur", "Raphaël s'assoit, lève les yeux."),
        L("narrateur", "Le croissant de buée brille sous une chaîne."),
        L("narrateur", "Il ramasse le bateau, le pose au bord de la flaque."),
        L("narrateur", "Le ballon reste, un brin collé."),
        L("enfant-m", "Le golfe, enfin."),
        L("maman", "Tu as regardé l'ombre, pas l'herbe."),
        L("narrateur", "Un cling lointain, puis le banc."),
    ],
    (3, 1, 2): [
        L("narrateur", "Vers le portail, le ballon a de l'herbe."),
        L("enfant-m", "Il a mangé le bateau."),
        L("narrateur", "Raphaël veut secouer le cuir, trop fort."),
        L("maman", "Doucement."),
        L("maman", "Le croissant ?"),
        L("narrateur", "Sous le portail, une ombre de chaîne n'est plus."),
        L("narrateur", "Une ombre de barre, oui."),
        L("narrateur", "Le croissant de buée y est, pâle."),
        L("narrateur", "Raphaël ramasse le jaune, le pose dans la flaque du seuil."),
        L("enfant-m", "Le golfe a bougé."),
        L("papa", "Toi aussi, jusqu'ici."),
        L("narrateur", "Le ballon a de l'herbe, près du portail."),
        L("narrateur", "Le métal se tait."),
        L("maman", "La fausse mer est restée derrière."),
    ],
    (3, 1, 3): [
        L("narrateur", "Raphaël cherche le bateau dans le manteau, trop vite."),
        L("narrateur", "Les poches sont vides."),
        L("enfant-m", "Il est dehors !"),
        L("papa", "Les manches, puis on cherche ?"),
        L("narrateur", "Une manche, puis l'autre."),
        L("narrateur", "Ensuite Raphaël se baisse, près du crochet."),
        L("narrateur", "Le croissant de buée brille dans l'herbe du pied."),
        L("narrateur", "Il glisse le jaune dans la poche, à plat."),
        L("enfant-m", "Je t'ai, maintenant."),
        L("maman", "Après le manteau, pas avant."),
        L("narrateur", "Un nuage passe au-dessus du crochet."),
        L("narrateur", "Le manteau a un brin d'herbe, à l'ourlet."),
        L("papa", "Le golfe rentre avec vous."),
    ],
    (3, 2, 1): [
        L("narrateur", "Sur le banc, le seau a de l'eau trop vive."),
        L("enfant-m", "Je pose, là, pendant que ça tourne."),
        L("narrateur", "Le bateau tourne, manque le bord, tombe."),
        L("enfant-m", "Aïe."),
        L("maman", "On attend que ça se taise ?"),
        L("narrateur", "Raphaël pose le seau sur le bois."),
        L("narrateur", "Il compte, tout bas, sans pomper."),
        L("narrateur", "L'eau s'arrête."),
        L("narrateur", "Le croissant de buée se lit, net, au fond."),
        L("narrateur", "Le jaune entre, sans tourner."),
        L("enfant-m", "Le golfe est sage."),
        L("papa", "Tu as attendu le silence."),
        L("narrateur", "L'anse froide repose sur le banc."),
    ],
    (3, 2, 2): [
        L("narrateur", "Près du portail, l'eau du seau tremble."),
        L("narrateur", "Un vélo passe, loin."),
        L("enfant-m", "Ça va tout verser !"),
        L("papa", "Tu poses le seau, d'abord ?"),
        L("narrateur", "Raphaël pose l'anse contre le métal."),
        L("narrateur", "Il attend que l'eau se taise."),
        L("narrateur", "Le croissant de buée redevient un croissant."),
        L("narrateur", "Le jaune entre, sans tourner."),
        L("enfant-m", "Le golfe tient."),
        L("maman", "Le vélo est passé."),
        L("maman", "Toi, tu es resté."),
        L("narrateur", "La flaque du seuil tremble, puis s'arrête."),
        L("narrateur", "Le portail a une ombre d'anse."),
        L("papa", "Vous pouvez rentrer."),
    ],
    (3, 2, 3): [
        L("narrateur", "Raphaël tient le seau et cherche le manteau."),
        L("narrateur", "L'eau penche, presque verse sur le tissu."),
        L("enfant-m", "Attention !"),
        L("maman", "Le seau au sol, les manches ensuite ?"),
        L("narrateur", "Il pose le seau, droit."),
        L("narrateur", "Une manche, puis l'autre."),
        L("narrateur", "Le bateau, à plat, dans la poche."),
        L("narrateur", "Le croissant de buée n'a pas bu le manteau."),
        L("enfant-m", "L'eau est restée dans le seau."),
        L("papa", "Deux gestes, pas trois d'un coup."),
        L("narrateur", "Le seau laisse une ombre sur le manteau, un instant."),
        L("narrateur", "Ça sent le savon, un peu, dans le vent."),
        L("maman", "Le golfe rentre, sans tacher."),
    ],
    (3, 3, 1): [
        L("narrateur", "Sur le banc, le doudou a du vent, de la poussière."),
        L("enfant-m", "On se balance, ici."),
        L("narrateur", "Le banc ne bouge pas."),
        L("enfant-m", "Ah."),
        L("papa", "Le banc pour s'asseoir."),
        L("papa", "La flaque, devant ?"),
        L("narrateur", "Raphaël s'assoit, le doudou sur les genoux."),
        L("narrateur", "Il glisse le jaune vers la flaque qui tremble."),
        L("narrateur", "Le croissant de buée quitte la poussière, touche l'eau."),
        L("enfant-m", "Le golfe, sans pomper."),
        L("maman", "Tu as changé de siège."),
        L("narrateur", "Le doudou a senti le vent, sur le banc."),
        L("narrateur", "La chaîne, derrière, se tait."),
        L("papa", "Les bateaux, eux, sont arrivés."),
    ],
    (3, 3, 2): [
        L("narrateur", "Près du portail, le doudou a de la poussière."),
        L("enfant-m", "Il essuie le loquet."),
        L("narrateur", "L'oreille grise laisse un nuage, le loquet reste."),
        L("maman", "Ta main, puis l'oreille au sec ?"),
        L("narrateur", "Raphaël pousse le portail."),
        L("narrateur", "Il pose le doudou contre le pied, loin de l'eau."),
        L("narrateur", "Le bateau, ensuite, dans la flaque du seuil."),
        L("narrateur", "Le croissant de buée quitte la poussière."),
        L("enfant-m", "Toi au sec."),
        L("enfant-m", "Lui à l'eau."),
        L("papa", "Deux places."),
        L("narrateur", "La chaîne se tait, près du portail."),
        L("narrateur", "L'oreille molle dépasse, propre un peu."),
        L("maman", "Vous passez."),
    ],
    (3, 3, 3): [
        L("narrateur", "Le manteau, le doudou, le vent des chaînes."),
        L("narrateur", "Raphaël veut tout serrer, d'un coup."),
        L("narrateur", "L'oreille bloque la poche, le bateau tombe."),
        L("enfant-m", "Presque par terre."),
        L("papa", "Les manches, l'oreille, le papier ?"),
        L("narrateur", "Un bras, puis l'autre."),
        L("narrateur", "Le doudou, contre lui."),
        L("narrateur", "Le bateau, à plat, dans la poche."),
        L("narrateur", "Le croissant de buée chauffe, loin du vent."),
        L("enfant-m", "Il n'est plus à terre."),
        L("maman", "Le golfe rentre, dans l'ordre."),
        L("narrateur", "L'oreille grise dépasse du manteau."),
        L("papa", "La bouilloire, tout à l'heure, a fait pareil."),
    ],
}

FIN = {
    (1, 1, 1): [
        L("narrateur", "Ils rentrent."),
        L("narrateur", "Le jaune a un grain de sable sur le croissant."),
        L("enfant-m", "Un cadeau du port."),
        L("papa", "Il peut tomber, après."),
        L("maman", "Le rideau a voyagé, lui aussi."),
        L("narrateur", "Raphaël pose les bateaux sur le rebord."),
        L("narrateur", "Le faux vent de la bouilloire s'est tu."),
        L("enfant-m", "Ils sont arrivés, pour de vrai."),
        L("narrateur", "Un grain de sable sèche sur le croissant de buée."),
    ],
    (1, 1, 2): [
        L("narrateur", "Derrière le portail, le salon."),
        L("narrateur", "Le ballon roule jusqu'au tapis à pois."),
        L("enfant-m", "Pas la rue."),
        L("maman", "Tu as regardé, avant."),
        L("papa", "Le croissant a dit le parc."),
        L("narrateur", "Raphaël pose le jaune sous le bateau du rideau."),
        L("narrateur", "Les deux jaunes se font face."),
        L("enfant-m", "Toi, tu as de l'eau, un peu."),
        L("narrateur", "Le ballon s'endort contre le rideau à bateaux."),
    ],
    (1, 1, 3): [
        L("narrateur", "Raphaël raccroche le manteau."),
        L("narrateur", "La poche garde un peu de vapeur froide."),
        L("enfant-m", "Comme la bouilloire, tout à l'heure."),
        L("papa", "Elle s'est tue."),
        L("maman", "Le croissant est tiède, à peine."),
        L("narrateur", "Il sort le bateau, à plat."),
        L("narrateur", "Le rebord le reçoit."),
        L("enfant-m", "Le port rentre."),
        L("narrateur", "La poche du manteau garde un peu de vapeur froide."),
    ],
    (1, 2, 1): [
        L("narrateur", "Le seau rentre, l'anse mouillée."),
        L("narrateur", "Raphaël pose le jaune près du gobelet."),
        L("enfant-m", "Deux ports."),
        L("maman", "L'un a du savon."),
        L("maman", "L'autre, du sable."),
        L("papa", "Tu as versé moins, au banc."),
        L("narrateur", "Le croissant pâle sèche, net."),
        L("narrateur", "La bouilloire reste muette."),
        L("enfant-m", "On a fini le filet."),
        L("narrateur", "L'anse du seau pose une ombre ronde sur le gobelet."),
    ],
    (1, 2, 2): [
        L("narrateur", "Le portail est loin, fermé."),
        L("narrateur", "Raphaël pose le seau sous le portemanteau."),
        L("enfant-m", "La fuite est restée dehors."),
        L("papa", "Oui."),
        L("papa", "Côté parc."),
        L("maman", "Le croissant a choisi."),
        L("narrateur", "Le jaune sèche sur le rebord."),
        L("narrateur", "Un filet de sable sèche près du métal froid."),
        L("enfant-m", "La bouilloire se tait."),
        L("narrateur", "Un filet de sable sèche près de la bouilloire muette."),
    ],
    (1, 2, 3): [
        L("narrateur", "Raphaël raccroche le manteau taché d'un peu d'eau."),
        L("narrateur", "Il sort le bateau, sec."),
        L("enfant-m", "Lui n'a pas bu."),
        L("maman", "Le manteau, d'abord."),
        L("maman", "Le seau, ensuite."),
        L("papa", "Deux mains, deux temps."),
        L("narrateur", "Le croissant de buée est net, sur le rebord."),
        L("narrateur", "Le couloir sent le savon."),
        L("enfant-m", "On a fait le port."),
        L("narrateur", "Le manteau sent le sable, très bas."),
    ],
    (1, 3, 1): [
        L("narrateur", "Le doudou rentre, une oreille sablée."),
        L("narrateur", "Raphaël le pose sur le fauteuil."),
        L("enfant-m", "Le quai s'endort."),
        L("papa", "Sec, cette fois."),
        L("maman", "Le bateau, au rebord."),
        L("narrateur", "Le croissant de buée a un grain, pâle."),
        L("narrateur", "Les bateaux du rideau ne bougent plus."),
        L("enfant-m", "Ils se parlent, sans vent."),
        L("narrateur", "L'oreille grise porte un croissant pâle de sable."),
    ],
    (1, 3, 2): [
        L("narrateur", "Le doudou a senti le portail."),
        L("narrateur", "Raphaël le glisse sous le rideau, tout bas."),
        L("enfant-m", "Il garde le chemin."),
        L("maman", "Toi, tu as ouvert."),
        L("papa", "Lui, non."),
        L("narrateur", "Le jaune rejoint le rebord."),
        L("narrateur", "Le croissant de buée voit le bateau du tissu."),
        L("enfant-m", "Deux jaunes."),
        L("narrateur", "Le doudou s'endort sous le bateau du rideau."),
    ],
    (1, 3, 3): [
        L("narrateur", "Raphaël raccroche le manteau."),
        L("narrateur", "Un fil gris pend de la poche."),
        L("enfant-m", "L'oreille a voyagé."),
        L("papa", "Dans l'ordre."),
        L("maman", "Les manches, puis lui, puis le papier."),
        L("narrateur", "Le jaune est à plat, sur le rebord."),
        L("narrateur", "Le croissant de buée chauffe, puis sèche."),
        L("enfant-m", "La bouilloire se tait."),
        L("narrateur", "Un fil gris pend du crochet, sans vent."),
    ],
    (2, 1, 1): [
        L("narrateur", "Ils rentrent, une feuille de rampe à la main."),
        L("narrateur", "Raphaël la pose sur la chaise."),
        L("enfant-m", "Le butoir, c'était le banc."),
        L("papa", "Pas le ballon, trop près."),
        L("maman", "Le croissant a dit l'eau."),
        L("narrateur", "Le jaune sèche, le nez vers le rideau."),
        L("narrateur", "La bouilloire est froide."),
        L("enfant-m", "La mer de la rampe est rentrée."),
        L("narrateur", "Une feuille de la rampe sèche sur la chaise."),
    ],
    (2, 1, 2): [
        L("narrateur", "Le portail est loin."),
        L("narrateur", "Raphaël pose le ballon près des clés."),
        L("enfant-m", "Il n'a pas pris la rue."),
        L("maman", "Toi non plus."),
        L("papa", "Le croissant a penché vers le parc."),
        L("narrateur", "Le jaune rejoint le rebord."),
        L("narrateur", "Le sifflet de la maison reste muet."),
        L("enfant-m", "On a changé de mer."),
        L("narrateur", "Le sifflet de la bouilloire reste muet, pour de bon."),
    ],
    (2, 1, 3): [
        L("narrateur", "Raphaël raccroche le manteau froid de rampe."),
        L("narrateur", "Il sort le bateau, à plat."),
        L("enfant-m", "Il a glissé, pour de vrai."),
        L("papa", "Les manches, d'abord."),
        L("maman", "Le ballon, ensuite."),
        L("narrateur", "Le croissant de buée a un peu de froid."),
        L("narrateur", "Le rebord le réchauffe."),
        L("enfant-m", "La mer est rentrée."),
        L("narrateur", "Le manteau a gardé le froid de la rampe."),
    ],
    (2, 2, 1): [
        L("narrateur", "Le seau rentre, moins plein."),
        L("narrateur", "Raphaël le pose sous le portemanteau."),
        L("enfant-m", "J'ai vidé un peu, d'abord."),
        L("maman", "Puis le filet."),
        L("papa", "Le croissant a pu sécher."),
        L("narrateur", "Le jaune est sur le rebord, net."),
        L("narrateur", "La rampe, loin, sèche aussi."),
        L("enfant-m", "Il n'est plus coincé."),
        L("narrateur", "Le seau penche un peu, sous le portemanteau."),
    ],
    (2, 2, 2): [
        L("narrateur", "Raphaël pose les bateaux sur le rebord."),
        L("narrateur", "Le nez du jaune regarde le rideau."),
        L("enfant-m", "Pas besoin de toute la rampe."),
        L("papa", "Une petite mer, près du portail."),
        L("maman", "Le croissant l'a montrée."),
        L("narrateur", "La bouilloire reste muette."),
        L("narrateur", "Le gobelet attend près du lavabo."),
        L("enfant-m", "Deux eaux, une à la maison."),
        L("narrateur", "Les bateaux sèchent sur le rebord, nez vers le rideau."),
    ],
    (2, 2, 3): [
        L("narrateur", "Raphaël raccroche le manteau."),
        L("narrateur", "Une goutte de rampe sèche dans la manche."),
        L("enfant-m", "Elle a voyagé."),
        L("maman", "Le seau, d'abord vidé."),
        L("papa", "Les manches, ensuite."),
        L("narrateur", "Le croissant de buée n'a plus de goutte."),
        L("narrateur", "Le jaune sèche sur le rebord."),
        L("enfant-m", "La mer est dans la poche, un peu."),
        L("narrateur", "Une goutte de rampe sèche dans la manche."),
    ],
    (2, 3, 1): [
        L("narrateur", "Le doudou rentre, l'oreille trop longue."),
        L("narrateur", "Raphaël le pose sur le fauteuil."),
        L("enfant-m", "Toi, tu restes."),
        L("enfant-m", "Lui, il est allé."),
        L("papa", "Deux places."),
        L("maman", "Le bois, puis l'eau."),
        L("narrateur", "Le jaune rejoint le rebord."),
        L("narrateur", "Le croissant de buée a quitté le tissu."),
        L("enfant-m", "La rampe se tait, loin."),
        L("narrateur", "L'oreille du doudou dépasse du fauteuil."),
    ],
    (2, 3, 2): [
        L("narrateur", "Ils ont passé le portail, dans l'ordre."),
        L("narrateur", "Raphaël pose le doudou près des chaussures."),
        L("enfant-m", "Ma main, puis lui."),
        L("maman", "Oui."),
        L("papa", "Le croissant a quitté l'île."),
        L("narrateur", "Le jaune sèche sur le rebord."),
        L("narrateur", "Le loquet, loin, se tait."),
        L("enfant-m", "La mer du seuil est rentrée."),
        L("narrateur", "Le papier jaune n'est plus collé à l'herbe."),
    ],
    (2, 3, 3): [
        L("narrateur", "Raphaël raccroche le manteau."),
        L("narrateur", "La poche sent un peu le métal froid."),
        L("enfant-m", "Il n'est plus collé."),
        L("papa", "Les manches, l'oreille, le papier."),
        L("maman", "La rampe l'a lâché."),
        L("narrateur", "Le jaune est à plat, sur le rebord."),
        L("narrateur", "Le croissant de buée sèche, loin de l'herbe."),
        L("enfant-m", "La bouilloire est froide."),
        L("narrateur", "La bouilloire est froide, tout à fait."),
    ],
    (3, 1, 1): [
        L("narrateur", "Ils rentrent, le ballon sous le bras."),
        L("narrateur", "Un brin d'herbe voyage avec."),
        L("enfant-m", "L'ombre l'a montré."),
        L("papa", "Pas l'herbe."),
        L("maman", "Le croissant, sous la chaîne."),
        L("narrateur", "Raphaël pose le jaune sur le rebord."),
        L("narrateur", "Le cling des chaînes n'entre pas."),
        L("enfant-m", "Le golfe est là, petit."),
        L("narrateur", "Le ballon a cessé de rouler, au salon."),
    ],
    (3, 1, 2): [
        L("narrateur", "Le portail est loin, fermé."),
        L("narrateur", "Raphaël pose le ballon près du tapis."),
        L("enfant-m", "Le golfe a bougé jusqu'ici."),
        L("maman", "Toi aussi."),
        L("papa", "La fausse mer est restée derrière."),
        L("narrateur", "Le jaune rejoint le bateau bleu du rideau."),
        L("narrateur", "Les deux se regardent."),
        L("enfant-m", "Toi, tu as l'eau."),
        L("narrateur", "Un bateau bleu du rideau fixe le papier jaune."),
    ],
    (3, 1, 3): [
        L("narrateur", "Raphaël raccroche le manteau."),
        L("narrateur", "Un brin d'herbe reste à l'ourlet."),
        L("enfant-m", "Après le manteau, je t'ai trouvé."),
        L("papa", "Les manches, puis le sol."),
        L("maman", "Le croissant brillait au pied."),
        L("narrateur", "Le jaune est dans la poche, puis sur le rebord."),
        L("narrateur", "Le crochet fait un petit bruit."),
        L("enfant-m", "Le golfe rentre."),
        L("narrateur", "Le crochet du manteau fait un petit toc."),
    ],
    (3, 2, 1): [
        L("narrateur", "Le seau rentre, l'eau sage."),
        L("narrateur", "Raphaël le pose sur le tapis à pois."),
        L("enfant-m", "J'ai attendu le silence."),
        L("maman", "Puis le croissant, net."),
        L("papa", "Le golfe n'a pas tourné."),
        L("narrateur", "Le jaune sèche sur le rebord."),
        L("narrateur", "Un pois rouge, un pois vert."),
        L("enfant-m", "Le salon a un port, maintenant."),
        L("narrateur", "Le seau pose son ombre sur un pois du tapis."),
    ],
    (3, 2, 2): [
        L("narrateur", "Ils ont attendu le vélo, puis rentré."),
        L("narrateur", "Raphaël pose le seau près de la porte."),
        L("enfant-m", "Le golfe a tenu."),
        L("papa", "L'anse contre le métal, d'abord."),
        L("maman", "L'eau, ensuite."),
        L("narrateur", "Le jaune rejoint le rebord."),
        L("narrateur", "Le croissant de buée est net, sans tourner."),
        L("enfant-m", "Le portail reste loin."),
        L("narrateur", "Le portail du parc reste loin, fermé."),
    ],
    (3, 2, 3): [
        L("narrateur", "Raphaël raccroche le manteau, sans tache."),
        L("narrateur", "Le seau est resté droit, au parc, un moment."),
        L("enfant-m", "L'eau n'a pas bu le tissu."),
        L("maman", "Le seau au sol, les manches ensuite."),
        L("papa", "Deux gestes."),
        L("narrateur", "Le jaune est à plat, sur le rebord."),
        L("narrateur", "Le croissant de buée n'a pas bu."),
        L("enfant-m", "Ça sent le savon."),
        L("narrateur", "Ça sent le savon, dans le couloir."),
    ],
    (3, 3, 1): [
        L("narrateur", "Le doudou rentre, l'odeur de l'herbe."),
        L("narrateur", "Raphaël le pose sur le fauteuil."),
        L("enfant-m", "Le golfe, sans pomper."),
        L("papa", "Le banc, pas la chaîne."),
        L("maman", "Le croissant a quitté la poussière."),
        L("narrateur", "Le jaune sèche sur le rebord."),
        L("narrateur", "Les bateaux du rideau ne bougent plus."),
        L("enfant-m", "Ils sont arrivés, tous."),
        L("narrateur", "Le doudou a l'odeur de l'herbe, au salon."),
    ],
    (3, 3, 2): [
        L("narrateur", "Ils ont passé le portail, deux places."),
        L("narrateur", "Raphaël pose le doudou, puis les bateaux."),
        L("enfant-m", "Toi au sec."),
        L("enfant-m", "Lui à l'eau."),
        L("maman", "Puis le rebord."),
        L("papa", "Le croissant a quitté la poussière."),
        L("narrateur", "Le bleu et le jaune se touchent, sur la chaise."),
        L("narrateur", "La bouilloire se tait."),
        L("enfant-m", "Le golfe est rentré."),
        L("narrateur", "Les deux bateaux se touchent, sur la chaise."),
    ],
    (3, 3, 3): [
        L("narrateur", "Raphaël raccroche le manteau."),
        L("narrateur", "L'oreille grise dépasse, puis rentre."),
        L("enfant-m", "Les manches, l'oreille, le papier."),
        L("papa", "Comme la bouilloire, tout à l'heure."),
        L("maman", "Un chant, puis l'eau, puis le silence."),
        L("narrateur", "Le jaune est à plat, sur le rebord."),
        L("narrateur", "Le croissant de buée sèche, loin du vent."),
        L("enfant-m", "Elle ne chante plus."),
        L("narrateur", "La bouilloire ne chante plus."),
    ],
}

Q_FIELDS = {
    "expected_answer": "une chose",
    "accepted_examples": (
        "une chose | puis l'autre | d'abord | ensuite | une chose puis l'autre | "
        "puis la suivante | la chaussette | les bateaux"
    ),
    "retry_prompt": "Il a fait une chose, puis la suivante. Comment s'est préparé Raphaël ?",
    "engine_ok_text": "Oui, une chose, puis la suivante.",
    "engine_near_text": "Tu es tout près. La chaussette, puis les bateaux.",
    "engine_timeout_text": "On continue.",
}


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
    if "_T0003_P000" in cid and not cid.endswith("_P0000"):
        return "resolution"
    if "_T0002_P000" in cid and "_T0003_" not in cid:
        return "action"
    return "obstacle"


def sons_for(cid: str, kind: str, i: int | None, j: int | None) -> str:
    if cid == "CHK_T0000_P0000":
        return "bouilloire"
    if kind in {"transition_question", "passage_question"}:
        return ""
    if cid.endswith("_C0001"):
        return "enfants_parc"
    if kind == "passage_fin":
        return {1: "bouilloire", 2: "bouilloire,rideau", 3: "manteau,bouilloire"}.get(i or 3, "bouilloire")
    if kind == "passage" and i and "_T0002_" not in cid:
        return {1: "enfants_parc,sable", 2: "enfants_parc,toboggan", 3: "enfants_parc,balancoire"}[i]
    if j and "_T0003_" not in cid and "_T0002_P000" in cid:
        return {1: "ballon", 2: "seau", 3: "tissu"}[j]
    if "_T0003_P000" in cid and kind == "passage":
        return "enfants_parc"
    return ""


def extra_emphasis(kind: str, prof: str, text_join: str) -> dict:
    extra: dict = {}
    low = text_join.lower()
    if prof == "opening":
        extra["emphasis"] = "croissant de buée"
    elif prof == "clue":
        extra["emphasis"] = "ce matin"
    elif prof == "confirm":
        extra["emphasis"] = "chaussette"
    elif prof == "action":
        if "ballon" in low:
            extra["emphasis"] = "ballon"
        elif "seau" in low:
            extra["emphasis"] = "seau"
        elif "doudou" in low:
            extra["emphasis"] = "doudou"
    elif prof == "resolution":
        if "croissant" in low:
            extra["emphasis"] = "croissant de buée"
        elif "flaque" in low:
            extra["emphasis"] = "flaque"
        else:
            extra["emphasis"] = "bateau"
    elif prof == "ending":
        extra["emphasis"] = "croissant" if "croissant" in low else "bouilloire"
    elif prof == "obstacle":
        extra["emphasis"] = None
    return extra


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
            s[f"{p2}_T0003_P0000"] = t3_lines(i, j)
            meta[f"{p2}_T0003_P0000"] = {
                "option_1_label": "le banc",
                "option_2_label": "le portail",
                "option_3_label": "le manteau",
            }
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = L3[(i, j, k)]
                s[f"{p3}_F0001"] = FIN[(i, j, k)]
    s = {cid: split_lines(lines) for cid, lines in s.items()}
    return s, meta


def path_stats(scripts: dict) -> None:
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
    print(f"chemins mots min={min(lengths)} max={max(lengths)} moy={sum(lengths)//len(lengths)}")


def parse_ijk(cid: str) -> tuple[int | None, int | None]:
    i = j = None
    m = re.search(r"CHK_T0001_P000(\d)", cid)
    if m:
        i = int(m.group(1))
    m2 = re.search(r"_T0002_P000(\d)", cid)
    if m2:
        j = int(m2.group(1))
    return i, j


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts, meta = build()
    preview(scripts)
    path_stats(scripts)
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
        i, j = parse_ijk(cid)
        text_join = " ".join(ln.split("|", 1)[1] for ln in scripts[cid])
        extra = extra_emphasis(kind, prof, text_join)
        if cid.endswith("_Q0001"):
            extra["fields"] = dict(Q_FIELDS)
        if cid in meta:
            extra.setdefault("fields", {}).update(meta[cid])
        nc = apply_tts(c, scripts[cid], sons_for(cid, kind, i, j), prof, extra)
        piper_vals.add(nc["length_scale_piper"])
        out_chunks.append(nc)
    if len(piper_vals) < 4:
        raise SystemExit(f"piper trop uniforme: {piper_vals}")
    out = dict(src)
    out["fil_rouge"] = (
        "Raphaël veut porter ses deux bateaux de papier jusqu'à la flaque du parc, "
        "celle qui ressemble à la mer du rideau, avant que le soleil la boive. "
        "La bouilloire a laissé un croissant de buée sur la voile jaune. "
        "Il attrape bateaux et chaussure d'un coup : le jaune glisse. "
        "Chaussette, puis poche, puis parc. Bac, rampe ou chaînes : le bateau "
        "n'atteint pas l'eau. Ballon, seau ou doudou changent la ruse. "
        "Banc, portail ou manteau : le croissant guide. Retour, la bouilloire s'est tue."
    )
    out["title"] = "La bouilloire et les petits bateaux"
    out["characters"] = "Raphaël, papa, maman"
    out["setting"] = "salon le matin, rideau à bateaux, puis parc"
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
        "# TREE-AUT-030 — La bouilloire et les petits bateaux\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "- **Titre noyau :** *La bouilloire et les petits bateaux*\n"
        "- **Public :** N2 (≤ 15 mots/phrase)\n"
        "- **Leçon :** AUT.ROU.001 — une chose puis la suivante, vécue "
        "(chaussette puis poche ; un geste, puis l'eau ; le bateau n'atteint la flaque "
        "que lorsqu'il refuse de tout faire d'un coup)\n"
        "- **Personnages :** Raphaël, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Les bateaux du rideau ont voyagé toute la nuit sans bouger. La bouilloire "
        "leur donne un faux vent et laisse un croissant de buée sur la voile jaune. "
        "Raphaël veut porter les deux bateaux de papier jusqu'à la flaque du parc "
        "avant que le soleil la boive. Il attrape bateaux et chaussure d'un coup : "
        "le jaune glisse. Chaussette, puis poche. Au parc, le jouet n'atteint pas "
        "l'endroit promis (port de sable, mer de la rampe, golfe des chaînes). "
        "Ballon, seau ou doudou changent la seconde ruse. Banc, portail ou manteau "
        "changent le climax. Le croissant du début se paie. Retour : la bouilloire s'est tue.\n\n"
        "## Vécu\n\n"
        "Salon, siff de bouilloire, rideau bleu et jaune, rebord, chaussette tiède, "
        "savon du couloir. Impatience (vite, au parc), découragement (épaules, "
        "menton bas, « il n'arrive pas »), fierté calme (il y est, sans frapper). "
        "Merci vécu après la chaussette puis la poche. Question : comment il s'est "
        "préparé. T1 bac / toboggan / balançoires. T2 ballon / seau / doudou. "
        "T3 banc / portail / manteau.\n\n"
        "## Vu et corrigé\n\n"
        "P1 F-NAR-019 example4 v2. Ouverture inventée (bateaux du rideau, faux vent), "
        "pas les cinq manières listées. Indice unique : croissant de buée, payé au "
        "climax. Corps : sourire disparaît, envie et inquiétude, adulte à la même "
        "hauteur. 2e ruse plus rusée (vague de sable, empreinte, île grise, butoir "
        "qui renvoie, rampe collante, fausse mer d'herbe). Pas gabarit example3. "
        "Tics « encore / déjà / tout doux / tout calme » retirés. Troupe D16 Raphaël. "
        "1er choix = lieux, n'enlève pas les bateaux. 27 fins, 27 dernières images. "
        "TTS par chunk : `notes`, `text_ssml`, `text_xai_tags`, piper 1.10–1.30. "
        "`slow` = choix, indice, fins. `check()` N2 OK. Pas apply.\n\n"
        "## Direction vocale\n\n"
        "Chaque segment a un arc dans `notes`. Débit, hauteur, volume et pause "
        "suivent la fonction : installation, choix, indice, obstacle, action, "
        "résolution, retour. Action plus vive. Choix, indice et fins plus lents.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks\n"
        "- 27 chemins, 611 à 639 mots, moyenne 627\n"
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
