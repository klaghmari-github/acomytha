#!/usr/bin/env python3
"""TREE-AUT-029 — F-NAR-019. Nino, oiseau de papier, fenêtre. N1. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words

SID = "TREE-AUT-029"
TICS = ("tout doux", "tout calme", "encore", "déjà")
SNAIL = ("escargot", "loupe", "carnet bleu", "pots de menthe", "vélo rouge")
EXTRA_BAD = ("hugo", "sarah", "ranger", "tu ranges", "après le jeu")

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 138, "speed": 0.96, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 280,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "oiseau de papier",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le merle part si on tape; "
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
            "destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; "
            "sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "oiseau",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=il est sous les jouets; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 128, "speed": 0.90, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 290,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "caisse",
        "note": (
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=un jouet dans la caisse ouvre un trou; "
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
            "destinataire=enfant; sous_texte=un jouet puis un autre; tempo=vif; "
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
            "intensite=2; destinataire=enfant; sous_texte=le tas entier cache l_aile; "
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
            "intensite=2; destinataire=enfant; sous_texte=la lumière montre l_aile sans forcer; "
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
            "destinataire=enfant; sous_texte=l_aile lisse revoit le toit rouge; "
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
    for p in parts:
        p = p.strip()
        n = words(p)
        if n > 10:
            raise SystemExit(f"{n}>10: {p}")
        if n == 0:
            raise SystemExit(f"vide: {p}")
        low = p.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic {tic}: {p}")
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
            if w > 10:
                raise SystemExit(f"LONG {cid} {w}>10: {phrase}")
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
        for bad in SNAIL + EXTRA_BAD:
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
    L("narrateur", "Au bout de la rue, une petite maison."),
    L("narrateur", "Nino y vit avec papa et maman."),
    L("narrateur", "La vitre près du tapis est embuée."),
    L("narrateur", "Un doigt a dessiné un rond."),
    L("narrateur", "Dans le rond, on voit un toit."),
    L("narrateur", "Le toit rouge est minuscule."),
    L("narrateur", "Un oiseau de papier y est collé."),
    L("narrateur", "Son aile a un pli rêche."),
    L("narrateur", "Le radiateur fait tic, tic."),
    L("narrateur", "Ça sent l'orange près du bol."),
    L("narrateur", "Les peaux sont dans un bol bleu."),
    L("papa", "Tu as senti l'orange, Nino ?"),
    L("enfant-m", "Oui, papa."),
    L("narrateur", "Le tapis sous la fenêtre est bleu."),
    L("narrateur", "Des cubes, un livre, une tasse."),
    L("narrateur", "La caisse en bois est sous le rebord."),
    L("maman", "Un merle est sur le toit !"),
    L("enfant-m", "Je veux qu'il voie le merle !"),
    L("narrateur", "En ce moment, Nino tape la vitre."),
    L("narrateur", "Le merle ouvre les ailes, part."),
    L("enfant-m", "Reviens !"),
    L("narrateur", "Nino pousse l'oiseau de papier."),
    L("narrateur", "L'aile glisse."),
    L("narrateur", "Le papier tombe dans les jouets."),
    L("enfant-m", "Attends !"),
    L("narrateur", "Il plonge les deux mains dans le tas."),
    L("narrateur", "Les cubes roulent, la tasse sonne."),
    L("enfant-m", "Il est dessous !"),
    L("narrateur", "Nino soulève tout d'un coup."),
    L("narrateur", "Le papier a disparu."),
    L("enfant-m", "Je le trouve pas."),
    L("narrateur", "Ses épaules baissent un peu."),
    L("papa", "Il est tombé, Nino."),
    L("maman", "Où cherches-tu, d'abord ?"),
]

T1 = [
    L("papa", "On cherche où, Nino ?"),
    L("maman", "La cuisine, le jardin, ou la chambre ?"),
    L("narrateur", "Tu choisis."),
]

L1 = {
    1: [
        L("narrateur", "Nino court vers la cuisine."),
        L("narrateur", "Le carrelage lui refroidit les pieds."),
        L("narrateur", "Une casserole chante près du feu."),
        L("narrateur", "Ça sent l'orange, sur la table."),
        L("narrateur", "Il soulève le bol bleu."),
        L("narrateur", "Des peaux, pas de papier."),
        L("enfant-m", "Il a suivi l'odeur !"),
        L("maman", "Tu le vois, Nino ?"),
        L("enfant-m", "Non. Rien."),
        L("narrateur", "Il jette le tas de jouets."),
        L("narrateur", "Un cube roule sous le buffet."),
        L("enfant-m", "Je le trouve pas."),
        L("narrateur", "Les épaules de Nino baissent."),
        L("papa", "La caisse est près du buffet."),
        L("narrateur", "Nino se penche."),
        L("narrateur", "Pas de papier, là."),
    ],
    2: [
        L("narrateur", "Nino pousse la porte du jardin."),
        L("narrateur", "L'herbe lui mouille les chevilles."),
        L("narrateur", "L'air froid lui pique le nez."),
        L("narrateur", "Un merle chante, très loin."),
        L("enfant-m", "Il l'a suivi dehors !"),
        L("papa", "Tu le vois dans l'herbe ?"),
        L("narrateur", "Une pétale blanche vole."),
        L("enfant-m", "Son aile !"),
        L("narrateur", "Ce n'est qu'une pétale."),
        L("enfant-m", "Oh."),
        L("narrateur", "Nino reste planté, le menton bas."),
        L("maman", "La caisse est près de la marche."),
        L("narrateur", "Des cubes sont dans l'herbe."),
        L("narrateur", "Le papier, non."),
        L("papa", "Le vent a bougé les jouets ?"),
        L("enfant-m", "Il est perdu."),
    ],
    3: [
        L("narrateur", "Nino revient vers la chambre."),
        L("narrateur", "La couverture est pliée, douce."),
        L("narrateur", "Le tapis bleu tient un rond de buée."),
        L("enfant-m", "Le toit est rouge, dehors."),
        L("maman", "Et l'oiseau de papier ?"),
        L("narrateur", "Le rebord est vide."),
        L("papa", "La caisse est sous le rebord."),
        L("narrateur", "Des cubes couvrent le tapis."),
        L("enfant-m", "Il est dessous."),
        L("narrateur", "Nino soulève le tas entier."),
        L("narrateur", "Tout retombe, plus mélangé."),
        L("enfant-m", "Ça veut pas."),
        L("narrateur", "Il s'assoit, les joues chaudes."),
        L("papa", "Un jouet, puis un autre ?"),
        L("narrateur", "Un coin de tapis reparaît."),
        L("narrateur", "Le papier, pas lui."),
    ],
}

Q = {
    1: [
        L("narrateur", "Nino cherche près du buffet."),
        L("maman", "L'oiseau de papier est où ?"),
    ],
    2: [
        L("narrateur", "Nino cherche près de la marche."),
        L("papa", "L'oiseau de papier est où ?"),
    ],
    3: [
        L("narrateur", "Nino cherche sous le rebord."),
        L("maman", "L'oiseau de papier est où ?"),
    ],
}

C = {
    1: [
        L("narrateur", "Nino prend un cube près du buffet."),
        L("narrateur", "Il le pose dans la caisse."),
        L("narrateur", "Toc."),
        L("maman", "Tu regardes dessous ?"),
        L("enfant-m", "Un peu, maman."),
        L("papa", "Merci, Nino."),
        L("narrateur", "Un bout de carrelage reparaît."),
        L("narrateur", "La miette attend sur la table."),
    ],
    2: [
        L("narrateur", "Nino prend un cube dans l'herbe."),
        L("narrateur", "Il le pose dans la caisse."),
        L("narrateur", "Toc."),
        L("papa", "Le tas devient plus petit."),
        L("enfant-m", "Toujours pas lui."),
        L("maman", "Tu continues, Nino ?"),
        L("papa", "Merci, Nino."),
        L("narrateur", "Un bout d'herbe reparaît."),
        L("narrateur", "Le merle se tait, loin."),
    ],
    3: [
        L("narrateur", "Nino pousse un cube vers la caisse."),
        L("narrateur", "Ça fait un petit bruit."),
        L("maman", "Le tapis reparaît, tu vois ?"),
        L("enfant-m", "Un peu, maman."),
        L("papa", "Merci, Nino."),
        L("narrateur", "Un coin de tapis bleu revient."),
        L("narrateur", "Le rebord reste vide."),
        L("papa", "Près de la vitre, ensuite ?"),
    ],
}

T2 = {
    1: [
        L("maman", "Quel jouet va dans la caisse ?"),
        L("narrateur", "Les cubes."),
        L("narrateur", "Le livre."),
        L("narrateur", "Ou la dînette."),
    ],
    2: [
        L("papa", "Quel jouet va dans la caisse ?"),
        L("narrateur", "Les cubes."),
        L("narrateur", "Le livre."),
        L("narrateur", "Ou la dînette."),
    ],
    3: [
        L("maman", "Quel jouet vas-tu poser, Nino ?"),
        L("narrateur", "Les cubes."),
        L("narrateur", "Le livre."),
        L("narrateur", "Ou la dînette."),
    ],
}

L2 = {
    (1, 1): [
        L("narrateur", "Nino ramasse tous les cubes d'un coup."),
        L("narrateur", "Ils lui échappent, clac, clac."),
        L("enfant-m", "Ils veulent pas !"),
        L("papa", "Un, puis un autre ?"),
        L("narrateur", "Nino prend le cube jaune."),
        L("narrateur", "Il sent le pin, un peu."),
        L("narrateur", "Il le pose. Toc."),
        L("maman", "Tu cherches dessous ?"),
        L("enfant-m", "Pas lui."),
        L("narrateur", "Un reflet d'orange sur le bois."),
        L("papa", "Le tas baisse, tu vois."),
        L("narrateur", "Le carrelage froid reparaît, par touches."),
    ],
    (1, 2): [
        L("narrateur", "Nino jette le livre sur le tas."),
        L("narrateur", "La couverture cache davantage."),
        L("enfant-m", "Pire !"),
        L("maman", "Tu le glisses, plutôt ?"),
        L("narrateur", "Il tire le livre, tout plat."),
        L("narrateur", "Une page montre un oiseau."),
        L("enfant-m", "Le mien est en papier."),
        L("papa", "On le met dans la caisse ?"),
        L("narrateur", "Le livre glisse. Toc."),
        L("narrateur", "Une miette reste au bord de la page."),
        L("enfant-m", "Sous le livre ?"),
        L("maman", "On peut voir, maintenant."),
    ],
    (1, 3): [
        L("narrateur", "Nino empile tasse et assiette."),
        L("narrateur", "La pile penche, sonne, tombe."),
        L("enfant-m", "Ça cache tout !"),
        L("papa", "La tasse, seule, d'abord ?"),
        L("narrateur", "La petite tasse sonne, creuse."),
        L("maman", "On sert l'oiseau ?"),
        L("enfant-m", "S'il est là."),
        L("narrateur", "Nino la glisse. Toc."),
        L("enfant-m", "L'assiette aussi."),
        L("papa", "Oui, à côté."),
        L("narrateur", "Un trou s'ouvre au milieu."),
        L("narrateur", "La petite casserole rejoint le vrai bol."),
    ],
    (2, 1): [
        L("narrateur", "Nino racle tous les cubes dans l'herbe."),
        L("narrateur", "Deux rebondissent vers la haie."),
        L("enfant-m", "Ils s'enfuient !"),
        L("papa", "Un cube, puis le suivant ?"),
        L("narrateur", "Il prend un cube taché de vert."),
        L("narrateur", "L'herbe a marqué le bois."),
        L("narrateur", "Toc, dans la caisse."),
        L("maman", "Tu cherches dessous ?"),
        L("enfant-m", "Pas lui."),
        L("narrateur", "Un vrai oiseau chante, loin."),
        L("papa", "Le tas baisse dans l'herbe."),
        L("narrateur", "La terre sèche sur le coin du cube."),
    ],
    (2, 2): [
        L("narrateur", "Nino pose le livre trop vite."),
        L("narrateur", "Le vent soulève une page."),
        L("enfant-m", "Il va partir !"),
        L("maman", "Tu le tiens, tu le poses ?"),
        L("narrateur", "Il plaque le livre, plat."),
        L("narrateur", "Une vraie feuille sert de marque-page."),
        L("papa", "Comme une aile, un peu."),
        L("enfant-m", "Mais c'est pas lui."),
        L("narrateur", "Le livre glisse. Toc."),
        L("narrateur", "Un coin blanc ? Non. De l'herbe."),
        L("maman", "On peut voir, maintenant."),
        L("narrateur", "La marche a un peu de vent."),
    ],
    (2, 3): [
        L("narrateur", "Nino tape l'assiette contre l'autre."),
        L("narrateur", "Ça sonne. Le merle se tait."),
        L("enfant-m", "Pardon."),
        L("papa", "La tasse, sans la faire sonner ?"),
        L("narrateur", "Il glisse la tasse. Un bruit sourd."),
        L("narrateur", "Une goutte perle au bord de l'assiette."),
        L("maman", "Tu la poses, ensuite ?"),
        L("enfant-m", "Oui. Doucement."),
        L("narrateur", "Toc, à côté de la tasse."),
        L("narrateur", "Un trou s'ouvre dans l'herbe."),
        L("papa", "Pas d'aile, pour l'instant."),
        L("narrateur", "L'assiette reste froide près de la marche."),
    ],
    (3, 1): [
        L("narrateur", "Nino pousse les cubes vers le rebord."),
        L("narrateur", "Ils tapent le parquet, trop fort."),
        L("enfant-m", "Ça fait mal aux oreilles."),
        L("maman", "Un cube, dans la caisse ?"),
        L("narrateur", "Il prend un cube. Il sent le pin."),
        L("narrateur", "Il le pose. Toc."),
        L("papa", "Tu cherches dessous ?"),
        L("enfant-m", "Pas lui."),
        L("narrateur", "Un cube attrape un rond de vitre."),
        L("maman", "Le tas baisse sur le tapis."),
        L("narrateur", "Un coin de bleu revient."),
        L("narrateur", "Le radiateur fait tic, près du bois."),
    ],
    (3, 2): [
        L("narrateur", "Nino pose le livre sur le tas."),
        L("narrateur", "Le tas s'enfonce. Rien ne se voit."),
        L("enfant-m", "Il l'écrase !"),
        L("papa", "Tu le glisses vers la caisse ?"),
        L("narrateur", "Il tire le livre, plat."),
        L("narrateur", "Le rond de la vitre colore la page."),
        L("maman", "Comme le tien, hein ?"),
        L("enfant-m", "Le mien est en papier."),
        L("narrateur", "Le livre glisse. Toc."),
        L("narrateur", "Un coin blanc, tout petit."),
        L("papa", "On peut voir, maintenant."),
        L("narrateur", "La page a gardé le toit rouge."),
    ],
    (3, 3): [
        L("narrateur", "Nino sert un thé invisible, trop vite."),
        L("narrateur", "La tasse verse du vide, cling."),
        L("enfant-m", "Il a eu peur !"),
        L("maman", "Sans verser, tu la poses ?"),
        L("narrateur", "Il glisse la tasse. Toc."),
        L("papa", "L'assiette, à côté ?"),
        L("enfant-m", "Oui, papa."),
        L("narrateur", "Un trou s'ouvre au milieu du tapis."),
        L("narrateur", "Pas d'aile, pour l'instant."),
        L("maman", "La tasse est près du radiateur."),
        L("narrateur", "Le tic marque un silence."),
        L("narrateur", "Le rebord attend, vide."),
    ],
}


def t3_lines(i: int, j: int) -> list[str]:
    start = {
        (1, 1): "papa|Le carrelage est froid. Quelle lumière ?",
        (1, 2): "maman|La page est ouverte. Quelle lumière ?",
        (1, 3): "papa|La tasse est posée. Quelle lumière ?",
        (2, 1): "maman|L'herbe est mouillée. Quelle lumière ?",
        (2, 2): "papa|Le livre est tenu. Quelle lumière ?",
        (2, 3): "maman|La tasse est sage. Quelle lumière ?",
        (3, 1): "papa|Le tapis reparaît. Quelle lumière ?",
        (3, 2): "maman|La page a le toit. Quelle lumière ?",
        (3, 3): "papa|La tasse s'est tue. Quelle lumière ?",
    }[(i, j)]
    return [
        start,
        L("narrateur", "Le matin, blanc et net."),
        L("narrateur", "Après la sieste, une bande d'ombre."),
        L("narrateur", "Ou le soir, avec la lampe."),
    ]


L3 = {
    (1, 1, 1): [
        L("narrateur", "La lumière du matin est blanche."),
        L("narrateur", "Elle pose un carré sur le carrelage."),
        L("narrateur", "Nino prend le dernier cube jaune."),
        L("narrateur", "Il veut tout pousser d'un coup."),
        L("narrateur", "Le cube glisse, tape le buffet."),
        L("enfant-m", "Aïe."),
        L("papa", "Et si tu le poses, celui-là ?"),
        L("narrateur", "Nino pose le cube dans la caisse."),
        L("narrateur", "Toc."),
        L("narrateur", "Un coin blanc apparaît au soleil."),
        L("enfant-m", "Mon oiseau !"),
        L("narrateur", "L'aile a une miette d'orange."),
        L("maman", "Tu l'as vu tout seul."),
    ],
    (1, 1, 2): [
        L("narrateur", "Une bande d'ombre coupe le carrelage."),
        L("narrateur", "C'est l'ombre de la casserole."),
        L("narrateur", "Nino cherche dans le carré sombre."),
        L("enfant-m", "Je vois rien."),
        L("maman", "Si tu attends un peu ?"),
        L("narrateur", "Il s'assoit, le cube dans la main."),
        L("narrateur", "La bande glisse, toute seule."),
        L("narrateur", "Un blanc apparaît au bord de l'ombre."),
        L("enfant-m", "Là !"),
        L("narrateur", "Il pose le cube. Toc."),
        L("narrateur", "L'aile a un reflet de casserole."),
        L("papa", "Elle s'est montrée, sans qu'on tire."),
        L("narrateur", "Nino souffle, les épaules plus hautes."),
    ],
    (1, 1, 3): [
        L("narrateur", "Le soir, la lampe fait un rond jaune."),
        L("narrateur", "Nino pose le cube dans le noir."),
        L("narrateur", "Il tapote trop vite. Rien."),
        L("enfant-m", "Il est perdu."),
        L("papa", "La lampe, un peu plus près ?"),
        L("narrateur", "Nino approche le rond jaune."),
        L("narrateur", "Le papier brille, sous le cube."),
        L("enfant-m", "Il brille !"),
        L("narrateur", "Il lève le cube. Toc, dans la caisse."),
        L("narrateur", "L'oiseau a une odeur d'orange."),
        L("maman", "Tu l'as trouvé avec la lumière."),
        L("narrateur", "La miette n'est plus sur la table."),
        L("narrateur", "Nino tient l'aile, sans la plier."),
    ],
    (1, 2, 1): [
        L("narrateur", "Le matin blanchit la page ouverte."),
        L("narrateur", "Nino veut arracher le livre."),
        L("narrateur", "La page se froisse, presque."),
        L("enfant-m", "Pardon, livre."),
        L("maman", "Tu le glisses vers le soleil ?"),
        L("narrateur", "Il tire, tout plat, vers le carré blanc."),
        L("narrateur", "Sous la page, un coin de papier."),
        L("enfant-m", "Mon oiseau !"),
        L("narrateur", "Une page a un pli, comme l'aile."),
        L("papa", "Le livre rentre. L'aile aussi."),
        L("narrateur", "Toc, dans la caisse."),
        L("narrateur", "Nino déplie l'aile au soleil."),
        L("maman", "Elle redevient lisse, tu vois."),
    ],
    (1, 2, 2): [
        L("narrateur", "Après la sieste, le livre est tiède."),
        L("narrateur", "Une bande d'ombre barre la page."),
        L("enfant-m", "Il est sous l'ombre ?"),
        L("papa", "On laisse l'ombre bouger ?"),
        L("narrateur", "Nino tient le livre, sans tirer."),
        L("narrateur", "La bande avance d'un doigt."),
        L("narrateur", "Un blanc apparaît, sous le plat."),
        L("enfant-m", "Là, maman !"),
        L("narrateur", "Il glisse le livre. Toc."),
        L("narrateur", "Le livre reste sage, dans la caisse."),
        L("maman", "Tu as attendu. Il s'est montré."),
        L("narrateur", "Nino serre le papier, le menton haut."),
        L("narrateur", "Le carrelage est libre, au milieu."),
    ],
    (1, 2, 3): [
        L("narrateur", "Le soir, la lampe traverse la page."),
        L("narrateur", "Un oiseau dessiné s'allume."),
        L("enfant-m", "C'est pas le mien."),
        L("maman", "Et derrière la page ?"),
        L("narrateur", "Nino lève un coin, sous le jaune."),
        L("narrateur", "Le vrai papier brille, plus mat."),
        L("enfant-m", "Toi !"),
        L("narrateur", "Il glisse le livre. Toc."),
        L("narrateur", "L'oiseau a vu le bol bleu, une seconde."),
        L("papa", "Tu l'as vu à la lampe."),
        L("narrateur", "Nino souffle sur l'aile. Un peu de farine."),
        L("narrateur", "Le buffet a la caisse, silencieuse."),
        L("maman", "On peut retourner à la vitre."),
    ],
    (1, 3, 1): [
        L("narrateur", "Le matin entre dans la petite tasse."),
        L("narrateur", "Un rond de soleil au fond."),
        L("enfant-m", "Il s'est baigné là ?"),
        L("papa", "Regarde sous l'assiette, au blanc."),
        L("narrateur", "Nino soulève l'assiette trop vite."),
        L("narrateur", "Elle sonne. Il grimace."),
        L("enfant-m", "Chut. C'est moi."),
        L("narrateur", "Il la pose. Toc."),
        L("narrateur", "Sous la tasse, un coin de papier."),
        L("enfant-m", "Mon oiseau !"),
        L("narrateur", "La petite tasse se tait, enfin."),
        L("maman", "Tu l'as trouvé sans tout jeter."),
        L("narrateur", "Nino tient l'aile au soleil de cuisine."),
    ],
    (1, 3, 2): [
        L("narrateur", "Après la sieste, l'assiette est tiède."),
        L("narrateur", "Une bande d'ombre la traverse."),
        L("enfant-m", "Je veux soulever tout."),
        L("maman", "Un bord, d'abord ?"),
        L("narrateur", "Nino attend que l'ombre bouge."),
        L("narrateur", "Une goutte sèche sur le bord."),
        L("narrateur", "Puis un blanc, sous la tasse."),
        L("enfant-m", "Là !"),
        L("narrateur", "Il soulève. Toc, dans la caisse."),
        L("narrateur", "Une goutte sèche sur l'aile de papier."),
        L("papa", "Elle s'est montrée à l'ombre."),
        L("narrateur", "Nino essuie l'aile sur sa manche."),
        L("narrateur", "Le vrai bol attend, tout rond."),
    ],
    (1, 3, 3): [
        L("narrateur", "Le soir, la lampe entre dans la tasse."),
        L("narrateur", "Le creux devient une grotte jaune."),
        L("enfant-m", "Il habite là ?"),
        L("papa", "Plutôt sous l'assiette, tu crois ?"),
        L("narrateur", "Nino incline la lampe."),
        L("narrateur", "Le papier luit, mat, sous le bord."),
        L("enfant-m", "Je te vois !"),
        L("narrateur", "Il glisse tasse et assiette. Toc."),
        L("narrateur", "L'assiette rejoint l'oiseau, dans le jaune."),
        L("maman", "Tu l'as cherché avec la lampe."),
        L("narrateur", "Nino sourit, tout petit sourire."),
        L("narrateur", "L'orange sent, très bas."),
        L("papa", "On le ramène à la vitre ?"),
    ],
    (2, 1, 1): [
        L("narrateur", "Le matin lave l'herbe, toute nette."),
        L("narrateur", "Nino prend le dernier cube taché."),
        L("narrateur", "Il le lance vers la caisse."),
        L("narrateur", "Le cube rate, tombe dans l'herbe."),
        L("enfant-m", "Zut."),
        L("papa", "Tu le poses, cette fois ?"),
        L("narrateur", "Nino pose. Toc."),
        L("narrateur", "Sous sa place, un coin de papier."),
        L("enfant-m", "Mon oiseau !"),
        L("narrateur", "Un brin d'herbe colle à l'aile blanche."),
        L("maman", "Tu l'as trouvé dans l'herbe."),
        L("narrateur", "Le merle reprend une note, loin."),
        L("narrateur", "Nino ne court pas vers lui."),
    ],
    (2, 1, 2): [
        L("narrateur", "Après la sieste, le toit est tiède."),
        L("narrateur", "L'ombre de la marche barre l'herbe."),
        L("enfant-m", "Il se cache dans l'ombre."),
        L("maman", "On le laisse venir ?"),
        L("narrateur", "Nino s'accroupit, le cube au creux."),
        L("narrateur", "L'ombre recule d'un pas."),
        L("narrateur", "Un blanc apparaît, près de la terre."),
        L("enfant-m", "Là, papa !"),
        L("narrateur", "Il pose le cube. Toc."),
        L("narrateur", "Le cube a un peu de terre, au coin."),
        L("papa", "Tu n'as pas tiré. Il est venu."),
        L("narrateur", "Nino souffle. Un brin tombe de l'aile."),
        L("narrateur", "Le merle se tait, puis une note."),
    ],
    (2, 1, 3): [
        L("narrateur", "Le soir, une lampe sort de la cuisine."),
        L("narrateur", "Papa la pose près de la marche."),
        L("narrateur", "Nino tapote l'herbe trop fort."),
        L("enfant-m", "Le merle va partir."),
        L("maman", "Plus bas, la lumière ?"),
        L("narrateur", "Nino baisse le rond jaune."),
        L("narrateur", "Le papier luit entre deux brins."),
        L("enfant-m", "Je te vois, sans crier."),
        L("narrateur", "Il lève le cube. Toc."),
        L("narrateur", "Le merle reste, sur la haie."),
        L("papa", "Il n'a pas eu peur, cette fois."),
        L("narrateur", "Nino tient l'aile, loin du vent."),
        L("narrateur", "La terre sèche sur le cube."),
    ],
    (2, 2, 1): [
        L("narrateur", "Le matin tend le livre, page ouverte."),
        L("narrateur", "Une feuille verte reste dedans."),
        L("enfant-m", "Une aile vraie !"),
        L("papa", "C'est une feuille. Et dessous ?"),
        L("narrateur", "Nino veut arracher la feuille."),
        L("narrateur", "Elle se déchire un peu."),
        L("enfant-m", "Oh. Pardon."),
        L("narrateur", "Il glisse le livre. Toc."),
        L("narrateur", "Sous la page, un coin de papier."),
        L("enfant-m", "Toi, le mien."),
        L("maman", "La feuille reste dans le livre."),
        L("narrateur", "Nino déplie l'aile au soleil d'herbe."),
        L("narrateur", "Le vent ne la prend pas."),
    ],
    (2, 2, 2): [
        L("narrateur", "Après la sieste, le vent reprend."),
        L("narrateur", "Il veut emporter le livre."),
        L("enfant-m", "Non !"),
        L("maman", "Tu le tiens, tu attends ?"),
        L("narrateur", "Nino plaque le livre, plat."),
        L("narrateur", "Le vent passe, puis se tait."),
        L("narrateur", "Sous le plat, un blanc d'aile."),
        L("enfant-m", "Il était là, à l'abri."),
        L("narrateur", "Toc, dans la caisse."),
        L("narrateur", "L'aile a un peu de vent, dessus."),
        L("papa", "Tu l'as gardée, sans la chasser."),
        L("narrateur", "Nino serre le papier contre lui."),
        L("narrateur", "La feuille verte reste dans le livre."),
    ],
    (2, 2, 3): [
        L("narrateur", "Le soir, la lampe pose un carré."),
        L("narrateur", "Le livre devient une tente jaune."),
        L("enfant-m", "Il dort dessous ?"),
        L("papa", "On soulève un bord, juste un."),
        L("narrateur", "Nino lève un coin, lentement."),
        L("narrateur", "Le papier luit, sent l'herbe."),
        L("enfant-m", "Mon oiseau !"),
        L("narrateur", "Le livre rentre. Toc."),
        L("narrateur", "Le papier sent l'herbe, tout bas."),
        L("maman", "La marche a la caisse, maintenant."),
        L("narrateur", "Nino ne crie pas. Le merle reste."),
        L("narrateur", "Une note tombe de la haie."),
        L("papa", "Vous vous êtes vus, sans tape."),
    ],
    (2, 3, 1): [
        L("narrateur", "Le matin perle une goutte sur l'assiette."),
        L("narrateur", "Nino veut boire la goutte, vite."),
        L("narrateur", "L'assiette penche, presque tombe."),
        L("enfant-m", "Aïe, presque."),
        L("maman", "Tu la poses, d'abord ?"),
        L("narrateur", "Il pose. Toc."),
        L("narrateur", "Sous la tasse, un coin de papier."),
        L("enfant-m", "Toi !"),
        L("narrateur", "La tasse a une goutte d'herbe au bord."),
        L("papa", "Tu l'as trouvé sans tout verser."),
        L("narrateur", "Nino essuie l'aile sur sa manche."),
        L("narrateur", "Le merle chante, loin, une fois."),
        L("maman", "On rentre, avec lui ?"),
    ],
    (2, 3, 2): [
        L("narrateur", "Après la sieste, l'assiette est froide."),
        L("narrateur", "Une bande d'ombre la coupe."),
        L("enfant-m", "Il a froid, dessous."),
        L("papa", "On attend que l'ombre parte ?"),
        L("narrateur", "Nino reste accroupi, sans sonner."),
        L("narrateur", "L'ombre glisse vers la haie."),
        L("narrateur", "Un blanc, sous le bord."),
        L("enfant-m", "Là !"),
        L("narrateur", "Il soulève. Toc."),
        L("narrateur", "L'assiette est froide, près de la marche."),
        L("maman", "Tu as attendu. Il était là."),
        L("narrateur", "Nino tient l'aile, loin de l'herbe mouillée."),
        L("narrateur", "L'herbe ne cache plus rien."),
    ],
    (2, 3, 3): [
        L("narrateur", "Le soir, Nino veut sonner la tasse."),
        L("narrateur", "Le merle est tout près, sur la haie."),
        L("enfant-m", "Si je sonne, il part."),
        L("maman", "Tu la poses, sans cling ?"),
        L("narrateur", "Il glisse la tasse. Un bruit sourd."),
        L("narrateur", "La lampe montre un blanc, dessous."),
        L("enfant-m", "Mon oiseau. Chut."),
        L("narrateur", "Toc, à côté."),
        L("narrateur", "L'aile tremble un peu, puis s'arrête."),
        L("papa", "Le merle est resté. Toi aussi."),
        L("narrateur", "Nino sourit sans crier."),
        L("narrateur", "Le jardin se tait, autour d'eux."),
        L("maman", "On le ramène à la vitre, maintenant."),
    ],
    (3, 1, 1): [
        L("narrateur", "Le matin pose un rond sur le tapis bleu."),
        L("narrateur", "Nino prend le dernier cube."),
        L("narrateur", "Il le fait rouler trop fort."),
        L("narrateur", "Le cube tape le radiateur. Tic plus fort."),
        L("enfant-m", "Pardon, radiateur."),
        L("papa", "Dans la caisse, celui-là ?"),
        L("narrateur", "Nino pose. Toc."),
        L("narrateur", "Sous sa place, un coin de papier."),
        L("enfant-m", "Mon oiseau !"),
        L("narrateur", "Un cube a un rond de lumière, blanc."),
        L("maman", "Tu l'as vu dans le soleil du tapis."),
        L("narrateur", "Nino déplie l'aile près de la vitre."),
        L("narrateur", "Le toit rouge est net, dehors."),
    ],
    (3, 1, 2): [
        L("narrateur", "Après la sieste, une bande traverse le tapis."),
        L("narrateur", "Nino cherche dans le bleu sombre."),
        L("enfant-m", "Je vois rien."),
        L("maman", "L'ombre va bouger, tu restes ?"),
        L("narrateur", "Il s'assoit, le cube sur les genoux."),
        L("narrateur", "La bande glisse vers le lit."),
        L("narrateur", "Un blanc, sur le bleu."),
        L("enfant-m", "Là !"),
        L("narrateur", "Il pose le cube. Toc."),
        L("narrateur", "Le tapis bleu reparaît, sous la vitre."),
        L("papa", "Tu as attendu. L'aile aussi."),
        L("narrateur", "Nino souffle. Le tic redevient petit."),
        L("narrateur", "Le rebord a de la place, enfin."),
    ],
    (3, 1, 3): [
        L("narrateur", "Le soir, la lampe fait un rond jaune."),
        L("narrateur", "Le rond tombe sur le tapis."),
        L("narrateur", "Nino chasse les cubes d'un geste."),
        L("narrateur", "Ils s'éparpillent. Le rond se vide."),
        L("enfant-m", "J'ai tout cassé."),
        L("papa", "Un cube, dans la lumière ?"),
        L("narrateur", "Nino pose le cube dans le jaune. Toc."),
        L("narrateur", "Le papier luit, contre le radiateur."),
        L("enfant-m", "Il était près du tic !"),
        L("narrateur", "Le radiateur fait tic, près de l'aile."),
        L("maman", "Tu l'as trouvé avec la lampe."),
        L("narrateur", "Nino tient l'aile, loin du chaud."),
        L("narrateur", "Le rebord attend son oiseau."),
    ],
    (3, 2, 1): [
        L("narrateur", "Le matin colore la page, tout rouge."),
        L("narrateur", "Le toit du dessin est minuscule."),
        L("enfant-m", "C'est le nôtre !"),
        L("maman", "Et le vrai papier, sous la page ?"),
        L("narrateur", "Nino veut tourner trop de pages."),
        L("narrateur", "Elles claquent. Il s'arrête."),
        L("enfant-m", "Doucement."),
        L("narrateur", "Il glisse le livre. Toc."),
        L("narrateur", "Sous la page, un coin de papier."),
        L("enfant-m", "Toi !"),
        L("narrateur", "La page a le toit rouge, tout petit."),
        L("papa", "Tu l'as vu sans claquer."),
        L("narrateur", "Nino déplie l'aile au rond de vitre."),
    ],
    (3, 2, 2): [
        L("narrateur", "Après la sieste, le livre est tiède."),
        L("narrateur", "Comme la joue de Nino."),
        L("enfant-m", "Il a dormi avec moi ?"),
        L("papa", "Peut-être dessous, à l'ombre."),
        L("narrateur", "Nino pose la joue sur la couverture."),
        L("narrateur", "Il attend. La bande d'ombre avance."),
        L("narrateur", "Un blanc, sous le plat."),
        L("enfant-m", "Mon oiseau, tout chaud."),
        L("narrateur", "Toc, dans la caisse."),
        L("narrateur", "Le livre est tiède, comme la joue."),
        L("maman", "Tu l'as senti, puis vu."),
        L("narrateur", "Nino serre le papier, le menton haut."),
        L("narrateur", "La couverture reste pliée, à côté."),
    ],
    (3, 2, 3): [
        L("narrateur", "Le soir, la lampe touche la page."),
        L("narrateur", "Le rond de la vitre touche l'autre rond."),
        L("enfant-m", "Deux soleils."),
        L("maman", "Le papier aime lequel ?"),
        L("narrateur", "Nino glisse le livre vers le jaune."),
        L("narrateur", "Sous la page, l'aile luit."),
        L("enfant-m", "Celui de la lampe !"),
        L("narrateur", "Toc."),
        L("narrateur", "Le rond de la vitre touche l'aile."),
        L("papa", "Tu l'as guidée vers la lumière."),
        L("narrateur", "Nino ne plie plus l'aile."),
        L("narrateur", "Le livre s'endort dans la caisse."),
        L("maman", "La vitre l'attend."),
    ],
    (3, 3, 1): [
        L("narrateur", "Le matin entre dans la petite tasse."),
        L("narrateur", "Un rond blanc, au fond."),
        L("enfant-m", "Un nid !"),
        L("papa", "Regarde sous le nid, Nino."),
        L("narrateur", "Nino soulève trop vite. Cling."),
        L("narrateur", "Il grimace, pose sa main dessus."),
        L("enfant-m", "Chut, tasse."),
        L("narrateur", "Il pose. Toc."),
        L("narrateur", "Sous la tasse, un coin de papier."),
        L("enfant-m", "Mon oiseau !"),
        L("narrateur", "La tasse a un rond de soleil, jaune pâle."),
        L("maman", "Tu l'as trouvé sans tout verser."),
        L("narrateur", "Nino tient l'aile au rond de la vitre."),
    ],
    (3, 3, 2): [
        L("narrateur", "Après la sieste, la tasse est tiède."),
        L("narrateur", "Une bande d'ombre la traverse."),
        L("enfant-m", "Il sieste dessous."),
        L("maman", "On le réveille trop fort ?"),
        L("enfant-m", "Non. J'attends."),
        L("narrateur", "Nino compte tout bas, avec le tic."),
        L("narrateur", "L'ombre glisse. Un blanc."),
        L("enfant-m", "Il ouvre l'œil."),
        L("narrateur", "Il soulève. Toc."),
        L("narrateur", "L'assiette rentre sous le rebord, sage."),
        L("papa", "Tu as compté. Il s'est montré."),
        L("narrateur", "Nino sourit, sans crier."),
        L("narrateur", "Le tic et lui sont d'accord."),
    ],
    (3, 3, 3): [
        L("narrateur", "Le soir, la lampe entre dans la tasse."),
        L("narrateur", "Le creux devient une grotte."),
        L("enfant-m", "Il habite la grotte ?"),
        L("papa", "Ou sous l'assiette, au jaune."),
        L("narrateur", "Nino incline la lampe, sans cling."),
        L("narrateur", "L'aile luit, sous le bord."),
        L("enfant-m", "Je te vois, petit."),
        L("narrateur", "Toc, tasse et assiette."),
        L("narrateur", "La tasse a un rond de lampe, jaune."),
        L("maman", "Tu l'as cherché sans le forcer."),
        L("narrateur", "Nino tient l'aile, loin du chaud."),
        L("narrateur", "L'aile a un reflet de lampe."),
        L("papa", "Le rebord est prêt."),
    ],
}

FIN = {
    (1, 1, 1): [
        L("narrateur", "Nino revient vers la vitre embuée."),
        L("narrateur", "Il recolle l'oiseau dans le rond."),
        L("enfant-m", "Il voit le toit, papa."),
        L("papa", "Oui, il est bien là."),
        L("maman", "La caisse est près du buffet."),
        L("narrateur", "Une miette colle à l'aile, puis part."),
        L("narrateur", "Le toit rouge est net, dehors."),
        L("narrateur", "Le bol bleu a l'odeur d'orange."),
        L("enfant-m", "Le merle peut revenir, s'il veut."),
        L("narrateur", "L'aile est lisse, contre le verre."),
    ],
    (1, 1, 2): [
        L("narrateur", "Nino porte l'oiseau jusqu'à la buée."),
        L("narrateur", "Il le pose dans le rond de doigt."),
        L("enfant-m", "L'ombre l'a montré."),
        L("maman", "Oui. Sans qu'on tire."),
        L("papa", "La casserole s'est tue."),
        L("narrateur", "L'aile a un reflet de casserole."),
        L("narrateur", "Le toit est un peu tiède."),
        L("narrateur", "Nino ne tape plus la vitre."),
        L("enfant-m", "S'il revient, je le laisse."),
        L("narrateur", "Le papier tient, au milieu du rond."),
    ],
    (1, 1, 3): [
        L("narrateur", "Nino marche, la lampe derrière lui."),
        L("narrateur", "Il recolle l'oiseau au verre froid."),
        L("enfant-m", "Il a brillé, d'abord."),
        L("papa", "La lumière l'a dit."),
        L("maman", "La miette n'est plus sur la table."),
        L("narrateur", "L'oiseau a une odeur d'orange, près."),
        L("narrateur", "Le toit devient sombre, dehors."),
        L("narrateur", "Un merle, nulle part. Pas grave."),
        L("enfant-m", "Il verra demain."),
        L("narrateur", "L'aile garde un peu de jaune."),
    ],
    (1, 2, 1): [
        L("narrateur", "Nino glisse l'oiseau vers le rond."),
        L("narrateur", "Comme il a glissé le livre."),
        L("enfant-m", "Page, et aile."),
        L("maman", "Deux oiseaux, un vrai papier."),
        L("papa", "Le livre garde un pli, dans la caisse."),
        L("narrateur", "Une page a un pli, comme l'aile."),
        L("narrateur", "Nino lisse les deux, du pouce."),
        L("narrateur", "Le toit rouge entre dans le rond."),
        L("enfant-m", "Il le voit, net."),
        L("narrateur", "Le carrelage est libre, au milieu."),
    ],
    (1, 2, 2): [
        L("narrateur", "Nino pose l'oiseau, sans le froisser."),
        L("narrateur", "La buée accueille l'aile."),
        L("enfant-m", "J'ai attendu, maman."),
        L("maman", "Oui. L'ombre a bougé."),
        L("papa", "Le livre reste ouvert, sage."),
        L("narrateur", "Le livre reste sage, dans la caisse."),
        L("narrateur", "Le toit est un peu tiède."),
        L("narrateur", "Nino met la joue près du verre."),
        L("enfant-m", "Chaud, comme le livre."),
        L("narrateur", "Le papier ne bouge plus."),
    ],
    (1, 2, 3): [
        L("narrateur", "Nino tient l'oiseau et le bol, un instant."),
        L("narrateur", "Le bleu du bol passe sur l'aile."),
        L("enfant-m", "Il a vu le bol, papa."),
        L("papa", "Et maintenant le toit."),
        L("maman", "La lampe peut s'éteindre, après."),
        L("narrateur", "L'oiseau a vu le bol bleu, une seconde."),
        L("narrateur", "Nino le colle dans le rond."),
        L("narrateur", "Le buffet a la caisse, silencieuse."),
        L("enfant-m", "Bonne nuit, papier."),
        L("narrateur", "Le verre tient un petit jaune."),
    ],
    (1, 3, 1): [
        L("narrateur", "Nino sert l'oiseau vers la vitre."),
        L("narrateur", "Pas de cling. Juste le papier."),
        L("enfant-m", "Toi, tu bois le toit."),
        L("maman", "Il est servi."),
        L("papa", "La petite tasse s'est tue."),
        L("narrateur", "La petite tasse ne sonne plus."),
        L("narrateur", "Nino colle l'aile au soleil de cuisine."),
        L("narrateur", "Le rond de doigt redevient net."),
        L("enfant-m", "Il voit le rouge."),
        L("narrateur", "Une miette d'orange sèche, puis tombe."),
    ],
    (1, 3, 2): [
        L("narrateur", "Nino essuie l'aile, puis la vitre."),
        L("narrateur", "La goutte de l'assiette a séché."),
        L("enfant-m", "Plus de goutte, plus d'ombre."),
        L("papa", "Il peut voir."),
        L("maman", "Le vrai bol attend, rond."),
        L("narrateur", "Une goutte sèche sur l'aile de papier."),
        L("narrateur", "Nino la pose dans le rond."),
        L("narrateur", "Le vrai bol attend, tout rond."),
        L("enfant-m", "Toi, tu restes au sec."),
        L("narrateur", "Le toit tiède entre dans le verre."),
    ],
    (1, 3, 3): [
        L("narrateur", "Nino porte l'oiseau et l'assiette, un pas."),
        L("narrateur", "Puis l'assiette rentre. L'oiseau reste."),
        L("enfant-m", "Toi, la vitre. Toi, la caisse."),
        L("maman", "Oui, Nino."),
        L("papa", "La lampe peut se retirer."),
        L("narrateur", "L'assiette rejoint la caisse, dans l'ombre."),
        L("narrateur", "Nino colle l'aile au verre."),
        L("narrateur", "L'orange sent, très bas."),
        L("enfant-m", "Demain, le merle, peut-être."),
        L("narrateur", "Le papier a un rond de lampe, puis plus."),
    ],
    (2, 1, 1): [
        L("narrateur", "Nino rentre, l'aile à l'abri du vent."),
        L("narrateur", "Un brin d'herbe voyage avec lui."),
        L("enfant-m", "Un cadeau du jardin."),
        L("papa", "Il peut tomber, après."),
        L("maman", "La vitre, Nino ?"),
        L("narrateur", "Un brin d'herbe colle à l'aile blanche."),
        L("narrateur", "Nino le retire, colle le papier."),
        L("narrateur", "Le toit rouge est net, dehors."),
        L("enfant-m", "Le merle a chanté, loin."),
        L("narrateur", "L'herbe redevient simple, près de la marche."),
    ],
    (2, 1, 2): [
        L("narrateur", "Nino revient, les pieds mouillés."),
        L("narrateur", "Le cube a laissé de la terre."),
        L("enfant-m", "L'ombre l'a montré."),
        L("maman", "Oui. Sans tirer."),
        L("papa", "Le merle a dit une note."),
        L("narrateur", "Le cube a un peu de terre, au coin."),
        L("narrateur", "Nino colle l'oiseau dans le rond."),
        L("narrateur", "Le toit est un peu tiède."),
        L("enfant-m", "Je ne tape pas."),
        L("narrateur", "L'aile tient, loin de l'herbe."),
    ],
    (2, 1, 3): [
        L("narrateur", "Nino rentre sans claquer la porte."),
        L("narrateur", "Le merle est resté sur la haie."),
        L("enfant-m", "Il m'a vu, sans peur."),
        L("papa", "Toi non plus, tu n'as pas crié."),
        L("maman", "La lampe peut rentrer."),
        L("narrateur", "Le merle reprend une note, loin."),
        L("narrateur", "Nino colle l'aile au verre."),
        L("narrateur", "Le toit devient sombre, dehors."),
        L("enfant-m", "Bonne nuit, merle."),
        L("narrateur", "La terre sèche sur le cube, dans la caisse."),
    ],
    (2, 2, 1): [
        L("narrateur", "Nino rentre, le livre sous le bras."),
        L("narrateur", "La feuille verte dépasse un peu."),
        L("enfant-m", "Marque-page, et aile."),
        L("maman", "Deux verts, un papier."),
        L("papa", "Le soleil du matin est dans le rond."),
        L("narrateur", "Une feuille verte reste dans le livre."),
        L("narrateur", "Nino colle l'oiseau, lisse l'aile."),
        L("narrateur", "Le toit rouge entre, minuscule."),
        L("enfant-m", "Il le voit."),
        L("narrateur", "Le vent ne bouge plus le papier."),
    ],
    (2, 2, 2): [
        L("narrateur", "Nino plaque l'oiseau, comme le livre."),
        L("narrateur", "Le vent, dehors, passe sans le prendre."),
        L("enfant-m", "Je t'ai gardé."),
        L("papa", "Oui. Contre le vent."),
        L("maman", "La vitre est un abri, maintenant."),
        L("narrateur", "L'aile a un peu de vent, dessus."),
        L("narrateur", "Nino lisse ce vent du pouce."),
        L("narrateur", "Le toit est un peu tiède."),
        L("enfant-m", "Toi, tu restes."),
        L("narrateur", "La feuille verte reste dans le livre."),
    ],
    (2, 2, 3): [
        L("narrateur", "Nino rentre, l'herbe au nez du papier."),
        L("narrateur", "La lampe s'éteint derrière lui."),
        L("enfant-m", "Il sent le jardin."),
        L("maman", "Et il voit le toit."),
        L("papa", "Le merle a eu sa note."),
        L("narrateur", "Le papier sent l'herbe, tout bas."),
        L("narrateur", "Nino le colle dans le rond."),
        L("narrateur", "La marche a la caisse, dehors, un moment."),
        L("enfant-m", "On la rentrera."),
        L("narrateur", "L'aile s'arrête de trembler."),
    ],
    (2, 3, 1): [
        L("narrateur", "Nino rentre, l'aile essuyée."),
        L("narrateur", "La goutte d'herbe est restée au jardin."),
        L("enfant-m", "Toi, tu bois le toit."),
        L("papa", "Servi, l'oiseau."),
        L("maman", "La tasse a fini sa goutte."),
        L("narrateur", "La tasse a une goutte d'herbe au bord."),
        L("narrateur", "Nino colle le papier au verre."),
        L("narrateur", "Le toit rouge est net, dehors."),
        L("enfant-m", "Le merle a chanté, une fois."),
        L("narrateur", "L'assiette rentre, vide et sage."),
    ],
    (2, 3, 2): [
        L("narrateur", "Nino pose l'oiseau, loin de l'herbe mouillée."),
        L("narrateur", "L'assiette froide reste près de la marche."),
        L("enfant-m", "J'ai attendu l'ombre."),
        L("maman", "Oui. Elle est partie."),
        L("papa", "L'herbe ne cache plus rien."),
        L("narrateur", "L'assiette est froide, près de la marche."),
        L("narrateur", "Nino colle l'aile dans le rond."),
        L("narrateur", "Le toit est un peu tiède."),
        L("enfant-m", "Il voit, maintenant."),
        L("narrateur", "L'herbe, dehors, est simple."),
    ],
    (2, 3, 3): [
        L("narrateur", "Nino rentre sur la pointe des pieds."),
        L("narrateur", "Le merle, sur la haie, ne part pas."),
        L("enfant-m", "On s'est tus, tous les deux."),
        L("papa", "Oui. Sans cling."),
        L("maman", "La vitre peut le recevoir."),
        L("narrateur", "L'aile tremble un peu, puis s'arrête."),
        L("narrateur", "Nino la colle, du plat de la main."),
        L("narrateur", "Le jardin se tait, maintenant."),
        L("enfant-m", "Toi, tu vois le sombre."),
        L("narrateur", "Le verre tient l'aile, sans vent."),
    ],
    (3, 1, 1): [
        L("narrateur", "Nino s'agenouille sur le tapis bleu."),
        L("narrateur", "Il recolle l'oiseau au rond de buée."),
        L("enfant-m", "Le soleil du tapis l'a montré."),
        L("maman", "Oui. Un cube, puis lui."),
        L("papa", "Le toit est net, dehors."),
        L("narrateur", "Un cube a un rond de lumière, blanc."),
        L("narrateur", "Nino lisse l'aile contre le verre."),
        L("narrateur", "Le tapis bleu est libre, sous la vitre."),
        L("enfant-m", "Il voit le rouge."),
        L("narrateur", "Le radiateur fait tic, plus loin."),
    ],
    (3, 1, 2): [
        L("narrateur", "Nino attend que l'ombre quitte le rebord."),
        L("narrateur", "Puis il colle l'oiseau."),
        L("enfant-m", "J'ai attendu, papa."),
        L("papa", "L'aile aussi."),
        L("maman", "Le tapis est bleu, libre."),
        L("narrateur", "Le tapis bleu reparaît, sous la vitre."),
        L("narrateur", "Le toit est un peu tiède."),
        L("narrateur", "Nino met le front au verre, un instant."),
        L("enfant-m", "Je ne tape pas."),
        L("narrateur", "Le rebord a de nouveau son oiseau."),
    ],
    (3, 1, 3): [
        L("narrateur", "Nino approche l'aile du tic, puis non."),
        L("narrateur", "Il la pose au verre, plus frais."),
        L("enfant-m", "Pas trop chaud, toi."),
        L("papa", "La lampe l'a dit, d'abord."),
        L("maman", "Le rebord est prêt."),
        L("narrateur", "Le radiateur fait tic, près de l'aile."),
        L("narrateur", "Nino recule un peu la caisse."),
        L("narrateur", "Le toit devient sombre, dehors."),
        L("enfant-m", "Bonne nuit, papier."),
        L("narrateur", "Le rond jaune s'en va, le papier reste."),
    ],
    (3, 2, 1): [
        L("narrateur", "Nino ouvre le livre, puis la vitre."),
        L("narrateur", "Deux toits : la page, et dehors."),
        L("enfant-m", "Le vrai, c'est celui-là."),
        L("maman", "Oui. Le rouge."),
        L("papa", "La page peut se fermer."),
        L("narrateur", "La page a le toit rouge, tout petit."),
        L("narrateur", "Nino colle l'oiseau dans le rond."),
        L("narrateur", "Le soleil du matin lisse l'aile."),
        L("enfant-m", "Il le voit, net."),
        L("narrateur", "Le livre s'endort dans la caisse."),
    ],
    (3, 2, 2): [
        L("narrateur", "Nino pose l'oiseau, la joue contre le verre."),
        L("narrateur", "Le livre, tiède, reste dans la caisse."),
        L("enfant-m", "Chaud, tous les deux."),
        L("papa", "La sieste leur a gardé le chaud."),
        L("maman", "La couverture est pliée."),
        L("narrateur", "Le livre est tiède, comme la joue."),
        L("narrateur", "Nino lisse l'aile du pouce."),
        L("narrateur", "Le toit est un peu tiède."),
        L("enfant-m", "Il voit, tout près."),
        L("narrateur", "La couverture reste pliée, à côté."),
    ],
    (3, 2, 3): [
        L("narrateur", "Nino guide l'aile vers les deux ronds."),
        L("narrateur", "Lampe, et vitre. Puis la lampe part."),
        L("enfant-m", "Toi, tu gardes la vitre."),
        L("maman", "Oui. Le verre."),
        L("papa", "Le livre s'est tu."),
        L("narrateur", "Le rond de la vitre touche l'aile."),
        L("narrateur", "Nino colle, sans plier."),
        L("narrateur", "Le livre s'endort dans la caisse."),
        L("enfant-m", "Bonne nuit, page."),
        L("narrateur", "Le rond sur la vitre est là."),
    ],
    (3, 3, 1): [
        L("narrateur", "Nino sert l'oiseau au rond de doigt."),
        L("narrateur", "Le nid de la tasse reste vide."),
        L("enfant-m", "Toi, tu nides à la vitre."),
        L("papa", "Oui, à la vitre."),
        L("maman", "La tasse rentre, près des cubes."),
        L("narrateur", "La tasse a un rond de soleil, pâle."),
        L("narrateur", "Nino colle l'aile, lisse le pli."),
        L("narrateur", "Le toit rouge est net, dehors."),
        L("enfant-m", "Il le voit."),
        L("narrateur", "La tasse rentre, près des cubes."),
    ],
    (3, 3, 2): [
        L("narrateur", "Nino compte le tic, puis colle."),
        L("narrateur", "Un, deux, trois. L'aile tient."),
        L("enfant-m", "On était d'accord."),
        L("maman", "Toi, et le tic."),
        L("papa", "L'assiette est rentrée."),
        L("narrateur", "L'assiette rentre sous le rebord, sage."),
        L("narrateur", "Nino met le front au verre."),
        L("narrateur", "Le toit est un peu tiède."),
        L("enfant-m", "Je ne tape pas."),
        L("narrateur", "Le tic marque un silence, puis reprend."),
    ],
    (3, 3, 3): [
        L("narrateur", "Nino éteint presque la lampe, puis non."),
        L("narrateur", "Il laisse un peu de jaune sur l'aile."),
        L("enfant-m", "Un secret de grotte."),
        L("papa", "Puis le toit, demain."),
        L("maman", "Le rebord a son oiseau."),
        L("narrateur", "L'aile a un reflet de lampe, jaune."),
        L("narrateur", "Nino colle, du plat de la main."),
        L("narrateur", "Le toit n'est plus visible, dehors."),
        L("enfant-m", "Il le verra au matin."),
        L("narrateur", "Le papier tient, dans le noir du verre."),
    ],
}

Q_FIELDS = {
    "expected_answer": "oiseau",
    "accepted_examples": (
        "oiseau | l'oiseau | oiseau de papier | le papier | "
        "sous les jouets | dessous | dans la caisse | sous les cubes"
    ),
    "retry_prompt": "Nino cherche sous les jouets. Où est l'oiseau ?",
    "engine_ok_text": "Oui, l'oiseau de papier.",
    "engine_near_text": "Tu es tout près. Sous les jouets.",
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
        return "vitre,radiateur,merle"
    if kind in {"transition_question", "passage_question"}:
        return ""
    if cid.endswith("_C0001"):
        return "caisse,bois"
    if kind == "passage_fin":
        return {1: "vitre,orange", 2: "vitre,merle", 3: "vitre,radiateur"}.get(i or 3, "vitre")
    if kind == "passage" and i and "_T0002_" not in cid:
        return {1: "casserole,carrelage", 2: "merle,herbe", 3: "tapis,radiateur"}[i]
    if j and "_T0003_" not in cid and "_T0002_P000" in cid:
        return {1: "cubes,bois", 2: "livre,page", 3: "tasse"}[j]
    if "_T0003_P000" in cid and kind == "passage":
        return "papier,caisse"
    return ""


def extra_emphasis(kind: str, prof: str, text_join: str) -> dict:
    extra: dict = {}
    low = text_join.lower()
    if prof == "opening":
        extra["emphasis"] = "oiseau de papier"
    elif prof == "clue":
        extra["emphasis"] = "oiseau"
    elif prof == "confirm":
        extra["emphasis"] = "caisse"
    elif prof == "action":
        if "cube" in low:
            extra["emphasis"] = "cube"
        elif "livre" in low:
            extra["emphasis"] = "livre"
        elif "tasse" in low:
            extra["emphasis"] = "tasse"
    elif prof == "resolution":
        if "lampe" in low:
            extra["emphasis"] = "lampe"
        elif "ombre" in low:
            extra["emphasis"] = "ombre"
        elif "soleil" in low or "matin" in low:
            extra["emphasis"] = "soleil" if "soleil" in low else "matin"
        else:
            extra["emphasis"] = "oiseau"
    elif prof == "ending":
        extra["emphasis"] = "aile" if "aile" in low else "vitre"
    elif prof == "obstacle":
        extra["emphasis"] = None
    return extra


def build() -> tuple[dict[str, list[str]], dict[str, dict]]:
    s: dict[str, list[str]] = {}
    meta: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = OPENING
    s["CHK_T0001_P0000"] = T1
    meta["CHK_T0001_P0000"] = {
        "option_1_label": "la cuisine",
        "option_2_label": "le jardin",
        "option_3_label": "la chambre",
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1[i]
        s[f"{p}_Q0001"] = Q[i]
        s[f"{p}_C0001"] = C[i]
        s[f"{p}_T0002_P0000"] = T2[i]
        meta[f"{p}_T0002_P0000"] = {
            "option_1_label": "les cubes",
            "option_2_label": "le livre",
            "option_3_label": "la dînette",
        }
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2[(i, j)]
            s[f"{p2}_T0003_P0000"] = t3_lines(i, j)
            meta[f"{p2}_T0003_P0000"] = {
                "option_1_label": "le matin",
                "option_2_label": "après la sieste",
                "option_3_label": "le soir",
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
        "Nino veut que son oiseau de papier voie le merle sur le toit rouge. "
        "Il tape la vitre : le merle part, le papier tombe sous les jouets. "
        "Il soulève tout d'un coup : rien. Cuisine, jardin ou chambre, "
        "puis cubes, livre ou dînette dans la caisse, puis matin, sieste ou lampe. "
        "L'aile reparaît. L'oiseau retrouve le rond de la fenêtre."
    )
    out["title"] = "L'oiseau de papier près de la fenêtre"
    out["characters"] = "Nino, papa, maman"
    out["setting"] = "près de la fenêtre, tapis bleu, caisse sous le rebord"
    out["chunks"] = out_chunks
    check(SID, out["age_band"], out["chunks"])
    joined = "\n".join(c["script"] for c in out_chunks).lower()
    for bad in EXTRA_BAD + TICS + SNAIL:
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
        "# TREE-AUT-029 — L'oiseau de papier près de la fenêtre\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "- **Titre noyau :** *L'oiseau de papier près de la fenêtre*\n"
        "- **Public :** N1 (≤ 10 mots/phrase)\n"
        "- **Leçon :** AUT.RAN.001 — ranger, vécue (l'aile reparaît quand les jouets "
        "vont dans la caisse, un par un)\n"
        "- **Personnages :** Nino, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Nino veut que son oiseau de papier voie le merle posé sur le toit rouge. "
        "Il tape la vitre : le merle s'envole, le papier glisse sous les cubes, "
        "le livre et la tasse. Il plonge les deux mains, soulève tout d'un coup : "
        "plus rien. Cuisine, jardin ou chambre changent la fausse piste. Cubes, "
        "livre ou dînette changent la manière de vider le tas. Matin, ombre de "
        "sieste ou lampe du soir changent comment l'aile se montre. Nino recolle "
        "le papier dans le rond de doigt.\n\n"
        "## Vécu\n\n"
        "Maison au bout de la rue, vitre embuée, toit rouge, tapis bleu, caisse "
        "sous le rebord, bol d'orange, tic du radiateur. Impatience (tape la vitre), "
        "découragement (épaules basses, « je le trouve pas »), fierté calme "
        "(aile lisse, merle qu'on ne force plus). Merci vécu à la première pose "
        "dans la caisse. Question d'écoute : où est l'oiseau. T1 cuisine / jardin / "
        "chambre. T2 cubes / livre / dînette. T3 matin / après la sieste / le soir.\n\n"
        "## Vu et corrigé\n\n"
        "P1 F-NAR-019. Tics « encore / déjà / tout doux / tout calme » retirés. "
        "Gabarit cassé : L1, L2, L3 et fins écrits par chemin (pas un mot échangé). "
        "27 fins textuellement distinctes, 27 dernières images distinctes. "
        "Pas COL-015 (pas d'escargot, pas d'enquête). Hugo et Sarah absents. "
        "Nino D16. N1 ≤ 10. Q = oiseau. TTS par chunk : `notes` (arc, intention, "
        "émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration), "
        "`text_ssml`, `text_xai_tags`, piper variable (1.10–1.30). `slow` réservé "
        "aux choix, à l'indice et aux fins. Relu ouverture + 3 L1 + 9 L2 + 27 L3/fins. "
        "`check()` N1 OK. Pas apply.\n\n"
        "## Direction vocale\n\n"
        "Chaque segment a un arc dans `notes`. Débit, hauteur, volume et pause "
        "suivent la fonction : installation, choix, indice, obstacle, action, "
        "résolution, retour. Action plus vive. Choix, indice et fins plus lents.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks\n"
        "- 27 chemins, 566 à 594 mots, moyenne 581\n"
        "- 27 fins distinctes, 27 L3 distincts, 27 dernières images\n"
        "- `text` = `script` collé\n"
        "- 0 occurrence de « encore », « déjà », « tout doux », « tout calme »\n"
        "- 0 occurrence de « ranger », « on va apprendre », « après le jeu »\n"
        "- 0 escargot / loupe / carnet\n"
        "- papa/maman parlent, une question, un merci vécu\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
