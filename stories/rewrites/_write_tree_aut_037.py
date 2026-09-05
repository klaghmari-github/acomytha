#!/usr/bin/env python3
"""TREE-AUT-037 — F-NAR-019 v2. Chouchou, manteau jaune, gouttière. N2. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words

SID = "TREE-AUT-037"
LIM = 15
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
    "bon travail",
    "limaçon",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 128, "speed": 0.94, "piper": 1.16,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 300,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "boucle d'étain",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=la_boucle_cligne_comme_le_zinc; "
            "tempo=naturel; sourire=léger; respiration=ample; volume=medium; pause_motivée=vapeur"
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
            "destinataire=enfant; sous_texte=ton_choix_change_la_ruse; tempo=suspendu; "
            "sourire=léger; respiration=pause_avant_choix; volume=medium; pause_motivée=trois_portes"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 110, "speed": 0.82, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "manteau",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=près_du_crochet; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question; volume=soft; pause_motivée=écoute"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 124, "speed": 0.90, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 290,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "manteau jaune",
        "note": (
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=le_porter_n_est_pas_le_boutonner; "
            "tempo=naturel; sourire=léger; respiration=fluide; volume=medium; pause_motivée=merci"
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
            "destinataire=enfant; sous_texte=trop_vite_la_manche_se_retourne; tempo=vif; "
            "sourire=léger; respiration=courte; volume=medium; pause_motivée=tirage"
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
            "intensite=2; destinataire=enfant; sous_texte=le_jeu_vole_la_boucle; "
            "tempo=resserré; sourire=aucun; respiration=retenue; volume=medium; pause_motivée=refus"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 130, "speed": 0.94, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "boucle d'étain",
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=la_boucle_guide_sans_tirer; "
            "tempo=naturel; sourire=franc; respiration=relâchée; volume=medium; pause_motivée=clignement"
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
            "destinataire=enfant; sous_texte=la_boucle_reste_au_crochet; "
            "tempo=posé; sourire=léger; respiration=ample; volume=soft; pause_motivée=zinc_nourri"
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
    L("narrateur", "Le grille-pain fait clic, net."),
    L("narrateur", "Une croûte saute, chaude."),
    L("narrateur", "La buée monte sur la vitre."),
    L("narrateur", "Elle dessine une rivière d'argent."),
    L("narrateur", "Dehors, le zinc a la même rivière."),
    L("narrateur", "La gouttière répond, glou."),
    L("narrateur", "Chouchou colle son nez au verre."),
    L("enfant-f", "Le zinc est sec, un peu."),
    L("papa", "Tu as vu le manteau, Chouchou ?"),
    L("narrateur", "Le manteau jaune attend au crochet."),
    L("narrateur", "Une boucle d'étain y cligne, une fois."),
    L("enfant-f", "Elle brille comme le zinc !"),
    L("maman", "La croûte, tu la portes où ?"),
    L("enfant-f", "Sur le zinc, vite !"),
    L("narrateur", "Le dernier coin sec attend."),
    L("papa", "La gouttière va le noyer ?"),
    L("enfant-f", "Avant, papa."),
    L("narrateur", "En ce moment, Chouchou tire le manteau."),
    L("narrateur", "Trop fort."),
    L("narrateur", "Une manche se retourne, molle."),
    L("narrateur", "La boucle d'étain s'accroche au crochet."),
    L("enfant-f", "Oh."),
    L("enfant-f", "Il ne vient pas."),
    L("narrateur", "Le sourire de Chouchou disparaît."),
    L("narrateur", "Une goutte tombe sur le carreau."),
]

T1 = [
    L("papa", "On passe où, avant le zinc ?"),
    L("narrateur", "La cuisine."),
    L("narrateur", "Le jardin."),
    L("maman", "Ou la chambre ?"),
]

L1 = {
    1: [
        L("narrateur", "Chouchou reste près de la table."),
        L("narrateur", "Le carrelage pique ses pieds, froid."),
        L("narrateur", "Ça sent la croûte, tout près."),
        L("enfant-f", "Je le mets ici, papa."),
        L("papa", "Le manteau, sur la chaise ?"),
        L("enfant-f", "Oui, vite."),
        L("narrateur", "Elle glisse un bras, trop vite."),
        L("narrateur", "La manche reste à l'envers."),
        L("narrateur", "La boucle d'étain frotte le bois."),
        L("enfant-f", "Elle ne passe pas."),
        L("narrateur", "Le sourire de Chouchou disparaît."),
        L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
        L("maman", "On s'accroupit ?"),
        L("narrateur", "Maman se met à sa hauteur."),
        L("enfant-f", "La boucle, elle clignait."),
        L("papa", "Tu l'as vue, au départ."),
    ],
    2: [
        L("narrateur", "Chouchou pousse la porte du jardin."),
        L("narrateur", "L'air touche son cou, frais."),
        L("narrateur", "Le zinc brille, tout près."),
        L("enfant-f", "Je le mets dehors, maman."),
        L("maman", "Le manteau, sur le pas ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Elle tire la manche, trop fort."),
        L("narrateur", "Une goutte saute de la gouttière."),
        L("narrateur", "Elle touche le tissu jaune."),
        L("narrateur", "La boucle d'étain s'accroche au gond."),
        L("enfant-f", "Il reste."),
        L("narrateur", "Le sourire de Chouchou disparaît."),
        L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
        L("papa", "On s'accroupit ?"),
        L("narrateur", "Papa se met à sa hauteur."),
        L("enfant-f", "La boucle ne cligne plus."),
        L("maman", "Tu l'as vue, toi."),
    ],
    3: [
        L("narrateur", "Chouchou emporte le manteau dans la chambre."),
        L("narrateur", "Le tapis est tiède sous les pieds."),
        L("narrateur", "L'armoire sent le linge."),
        L("enfant-f", "Devant la glace, papa."),
        L("papa", "Tu le mets toute seule ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Elle pousse un bras, trop vite."),
        L("narrateur", "La manche avale sa main."),
        L("narrateur", "La boucle d'étain tape un tiroir."),
        L("enfant-f", "Zut."),
        L("narrateur", "Le sourire de Chouchou disparaît."),
        L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
        L("maman", "Je m'accroupis, d'accord ?"),
        L("narrateur", "Maman se met à sa hauteur."),
        L("enfant-f", "La boucle s'est tue."),
        L("papa", "Tu l'as entendue, au crochet."),
    ],
}

Q = {
    1: [
        L("narrateur", "Chouchou a du pain aux doigts."),
        L("papa", "Elle a pris quoi, près du crochet ?"),
    ],
    2: [
        L("narrateur", "Chouchou a une goutte au poignet."),
        L("maman", "Elle a pris quoi, près du crochet ?"),
    ],
    3: [
        L("narrateur", "Chouchou a le tapis sous les pieds."),
        L("papa", "Elle a pris quoi, près du crochet ?"),
    ],
}

C = {
    1: [
        L("narrateur", "Oui."),
        L("narrateur", "Elle a pris le manteau jaune."),
        L("papa", "Merci, Chouchou."),
        L("maman", "La boucle est à ta hauteur."),
        L("enfant-f", "Elle est tiède."),
        L("papa", "On emporte un jeu, près du pain ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "La croûte reste dans sa main."),
    ],
    2: [
        L("narrateur", "Oui."),
        L("narrateur", "Le manteau jaune est contre elle."),
        L("maman", "Merci, Chouchou."),
        L("papa", "Tu n'as plus le cou nu."),
        L("enfant-f", "Il est chaud."),
        L("maman", "On emporte un jeu, pour le jardin ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Une feuille tremble sur le pas."),
    ],
    3: [
        L("narrateur", "Oui."),
        L("narrateur", "Le manteau jaune est dans ses bras."),
        L("papa", "Merci, Chouchou."),
        L("maman", "La glace te montre le jaune."),
        L("enfant-f", "Je me vois."),
        L("papa", "On emporte un jeu, près du lit ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Le tiroir reste un peu ouvert."),
    ],
}

T2 = {
    1: [
        L("maman", "Tu emportes quel jeu ?"),
        L("papa", "Les cubes."),
        L("papa", "Le livre."),
        L("maman", "Ou la dînette ?"),
    ],
    2: [
        L("papa", "Tu emportes quel jeu ?"),
        L("maman", "Les cubes."),
        L("maman", "Le livre."),
        L("papa", "Ou la dînette ?"),
    ],
    3: [
        L("maman", "Tu emportes quel jeu, près du lit ?"),
        L("papa", "Les cubes."),
        L("papa", "Le livre."),
        L("maman", "Ou la dînette ?"),
    ],
}

L2 = {
    (1, 1): [
        L("narrateur", "Près du pain, les cubes attendent."),
        L("narrateur", "Le bois est lisse, un peu chaud."),
        L("enfant-f", "Une tour, pour la croûte !"),
        L("narrateur", "Chouchou empile trop vite."),
        L("narrateur", "La tour penche, puis tombe."),
        L("narrateur", "Un cube rouge cache la boucle d'étain."),
        L("enfant-f", "Je n'aime pas ça."),
        L("papa", "On chasse le cube ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Elle observe le manteau jaune."),
        L("narrateur", "Elle écoute la gouttière."),
        L("maman", "Le coin sec part, presque."),
        L("enfant-f", "Pas sans le clignement."),
        L("narrateur", "Glou, très loin, sur le zinc."),
        L("enfant-f", "La boucle."),
        L("papa", "Tu l'as, ce son."),
    ],
    (1, 2): [
        L("narrateur", "Près de la table, le livre attend."),
        L("narrateur", "La couverture est froide, un peu rêche."),
        L("enfant-f", "Il garde la croûte, dans la poche !"),
        L("narrateur", "Elle glisse le livre trop fort."),
        L("narrateur", "Une page se lève, large."),
        L("narrateur", "Elle cache la boucle d'étain."),
        L("enfant-f", "Elle est partie."),
        L("maman", "On tire la page ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Maman se met à sa hauteur."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Elle observe le tissu jaune."),
        L("papa", "Le zinc attend, un peu."),
        L("enfant-f", "Pas sans le clignement."),
        L("enfant-f", "Celui du départ."),
        L("papa", "Tu l'as vu, toi."),
    ],
    (1, 3): [
        L("narrateur", "Près du pain, la dînette attend."),
        L("narrateur", "Une tasse blanche est tiède."),
        L("enfant-f", "Un goûter, sur le zinc !"),
        L("narrateur", "Elle pose l'assiette trop vite."),
        L("narrateur", "L'assiette glisse sur le tissu."),
        L("narrateur", "Elle recouvre la boucle d'étain."),
        L("enfant-f", "Plus de lumière."),
        L("papa", "On soulève tout ?"),
        L("enfant-f", "Doucement."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Elle écoute la cuisine."),
        L("narrateur", "Le grille-pain s'est tu."),
        L("maman", "Le coin sec part, presque."),
        L("enfant-f", "Pas sans le clignement."),
        L("narrateur", "Un toc minuscule, sous l'assiette."),
        L("enfant-f", "La boucle."),
        L("papa", "Tu l'as entendue, seule."),
    ],
    (2, 1): [
        L("narrateur", "Sur le pas, les cubes sont frais."),
        L("narrateur", "Un cube bleu a pris une goutte."),
        L("enfant-f", "Une marche, jusqu'au zinc !"),
        L("narrateur", "Elle pose le cube trop près de l'eau."),
        L("narrateur", "Il glisse vers la gouttière."),
        L("narrateur", "Le cube bleu cache la boucle d'étain."),
        L("enfant-f", "Elle s'est éteinte."),
        L("maman", "On court après ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Elle observe le manteau, mouillé."),
        L("narrateur", "Elle écoute le zinc."),
        L("papa", "Le coin sec part, presque."),
        L("enfant-f", "Pas sans le clignement."),
        L("narrateur", "Glou, tout bas, près du gond."),
        L("enfant-f", "La boucle."),
        L("maman", "Tu l'as, ce bruit."),
    ],
    (2, 2): [
        L("narrateur", "Sur le pas, le livre a une feuille collée."),
        L("narrateur", "Le vent tourne une page."),
        L("enfant-f", "Il montre le zinc, à papa !"),
        L("narrateur", "Elle ouvre trop vite."),
        L("narrateur", "La page claque contre le jaune."),
        L("narrateur", "Elle vole la boucle d'étain."),
        L("enfant-f", "Je n'aime pas ça."),
        L("papa", "On chasse le vent ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Papa se met à sa hauteur."),
        L("narrateur", "Personne ne dit le lieu."),
        L("narrateur", "Elle écoute la gouttière."),
        L("maman", "Le zinc attend, un peu."),
        L("enfant-f", "Pas sans le clignement."),
        L("enfant-f", "Celui du crochet."),
        L("papa", "Tu l'as, ce souvenir."),
    ],
    (2, 3): [
        L("narrateur", "Sur le pas, la dînette tremble."),
        L("narrateur", "La tasse a pris une goutte."),
        L("enfant-f", "Le goûter, dehors !"),
        L("narrateur", "Elle avance trop vite."),
        L("narrateur", "La tasse roule vers le gond."),
        L("narrateur", "Elle cache la boucle d'étain."),
        L("enfant-f", "Elle est sous la tasse."),
        L("maman", "On tire ?"),
        L("enfant-f", "J'attends."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Elle écarte la tasse, un pouce."),
        L("papa", "Le coin sec part, presque."),
        L("enfant-f", "Pas sans le clignement."),
        L("narrateur", "Un toc minuscule, sous la porcelaine."),
        L("enfant-f", "La boucle."),
        L("maman", "Tu l'as entendue, seule."),
        L("narrateur", "Une feuille colle à la tasse."),
    ],
    (3, 1): [
        L("narrateur", "Près du lit, les cubes sentent le tapis."),
        L("narrateur", "Un cube jaune ressemble au manteau."),
        L("enfant-f", "Une tour, devant la glace !"),
        L("narrateur", "Elle empile trop haut."),
        L("narrateur", "La tour tombe sur le tissu."),
        L("narrateur", "Le cube jaune cache la boucle d'étain."),
        L("enfant-f", "Plus de clignement."),
        L("papa", "On range d'un coup ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Elle observe le manteau, au sol."),
        L("narrateur", "Elle écoute, loin, la gouttière."),
        L("maman", "Le zinc attend, un peu."),
        L("enfant-f", "Pas sans le clignement."),
        L("narrateur", "Glou, à travers la vitre de la chambre."),
        L("enfant-f", "La boucle."),
        L("papa", "Tu l'as, ce son."),
    ],
    (3, 2): [
        L("narrateur", "Près de l'armoire, le livre est lourd."),
        L("narrateur", "Une image montre un toit de zinc."),
        L("enfant-f", "C'est le nôtre !"),
        L("narrateur", "Elle ouvre trop vite."),
        L("narrateur", "La page se plie sur la boucle d'étain."),
        L("enfant-f", "Elle a disparu."),
        L("maman", "On déplie fort ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Maman se met à sa hauteur."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "Elle observe le tissu jaune."),
        L("papa", "Le coin sec part, presque."),
        L("enfant-f", "Pas sans le clignement."),
        L("enfant-f", "Celui du départ."),
        L("maman", "Tu l'as vu, au crochet."),
        L("narrateur", "Le tiroir reste ouvert, un peu."),
    ],
    (3, 3): [
        L("narrateur", "Près du lit, la dînette attend."),
        L("narrateur", "Une cuillère tape le bois, tic."),
        L("enfant-f", "Le goûter, après le manteau !"),
        L("narrateur", "Elle pose l'assiette trop près."),
        L("narrateur", "L'assiette cache la boucle d'étain."),
        L("enfant-f", "Plus de lumière, maman."),
        L("papa", "On soulève ?"),
        L("enfant-f", "Un pouce."),
        L("narrateur", "Chouchou refuse de foncer."),
        L("narrateur", "Elle écarte l'assiette, lentement."),
        L("maman", "Le zinc attend, un peu."),
        L("enfant-f", "Pas sans le clignement."),
        L("narrateur", "Un toc minuscule, sous la faïence."),
        L("enfant-f", "La boucle."),
        L("papa", "Tu l'as entendue, seule."),
        L("narrateur", "La cuillère s'est tue."),
        L("narrateur", "La glace montre le jaune, plié."),
    ],
}

T3 = {
    1: [
        L("papa", "On sort par où, avec le manteau ?"),
        L("maman", "Le perron."),
        L("maman", "Le tonneau."),
        L("papa", "Ou le lilas ?"),
    ],
    2: [
        L("maman", "On sort par où, vers le zinc ?"),
        L("papa", "Le perron."),
        L("papa", "Le tonneau."),
        L("maman", "Ou le lilas ?"),
    ],
    3: [
        L("papa", "On sort par où, depuis la chambre ?"),
        L("maman", "Le perron."),
        L("maman", "Le tonneau."),
        L("papa", "Ou le lilas ?"),
    ],
}

L3 = {
    (1, 1, 1): [
        L("narrateur", "Chouchou pose un cube sur le perron."),
        L("narrateur", "La pierre est humide, un peu rêche."),
        L("enfant-f", "La croûte, après le manteau."),
        L("narrateur", "Elle veut tirer la manche."),
        L("papa", "Le zinc se noie, presque."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle relève le cube, sans à-coup."),
        L("narrateur", "La boucle d'étain cligne, à peine."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle tourne la manche, tout droit."),
        L("narrateur", "Un bras, puis l'autre."),
        L("maman", "Tu l'as, sans foncer."),
        L("narrateur", "La croûte pose sur le coin sec."),
        L("narrateur", "Une goutte manque le zinc, de justesse."),
        L("enfant-f", "Il a failli partir."),
        L("papa", "Tu as vu la boucle, seule."),
    ],
    (1, 1, 2): [
        L("narrateur", "Chouchou s'accroupit près du tonneau."),
        L("narrateur", "Le bois sonne, mouillé."),
        L("enfant-f", "J'écoute."),
        L("narrateur", "Un cube rouge roule contre le cerceau."),
        L("maman", "On y va ?"),
        L("enfant-f", "Pas trop vite."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "La boucle d'étain cligne, sur le bois."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, un pouce."),
        L("narrateur", "Le jaune se pose, chaud."),
        L("papa", "Tu l'as, près de l'eau."),
        L("narrateur", "La croûte trouve le coin sec."),
        L("narrateur", "Le tonneau a failli gicler dessus."),
        L("enfant-f", "Presque."),
        L("maman", "Tu as attendu le clignement."),
    ],
    (1, 1, 3): [
        L("narrateur", "Chouchou va sous le lilas."),
        L("narrateur", "Une grappe penche, mauve."),
        L("enfant-f", "Toi, tu caches le zinc."),
        L("narrateur", "Un cube se coinse dans l'herbe."),
        L("papa", "La gouttière monte."),
        L("enfant-f", "J'attends la boucle."),
        L("narrateur", "Elle écarte une branche, un doigt."),
        L("narrateur", "La boucle d'étain cligne, pâle."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle glisse les bras, sans tirer."),
        L("narrateur", "Le manteau sent la fleur, un peu."),
        L("maman", "Tu l'as, sous les grappes."),
        L("narrateur", "La croûte pose, au bord du zinc."),
        L("narrateur", "Un pétale manque de la couvrir."),
        L("enfant-f", "Il a failli."),
        L("papa", "Tu as vu, toute seule."),
    ],
    (1, 2, 1): [
        L("narrateur", "Chouchou pose le livre sur le perron."),
        L("narrateur", "Une page prend l'humidité."),
        L("enfant-f", "Le zinc est dans l'image."),
        L("narrateur", "La page veut retomber."),
        L("maman", "Le coin sec part."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle retient la page, sans claquer."),
        L("narrateur", "La boucle d'étain cligne, nette."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, tout droit."),
        L("narrateur", "Le jaune se ferme, un bouton."),
        L("papa", "Tu l'as, après le livre."),
        L("narrateur", "La croûte pose, ronde, sur le zinc."),
        L("narrateur", "L'eau du perron a failli la prendre."),
        L("enfant-f", "Presque trop tard."),
        L("maman", "Tu as lu le clignement."),
    ],
    (1, 2, 2): [
        L("narrateur", "Chouchou ouvre le livre près du tonneau."),
        L("narrateur", "L'image du toit tremble, mouillée."),
        L("enfant-f", "C'est ici."),
        L("narrateur", "Une goutte du tonneau vise la page."),
        L("papa", "On rentre ?"),
        L("enfant-f", "Pas sans lui."),
        L("narrateur", "Elle ferme le livre, un doigt."),
        L("narrateur", "La boucle d'étain cligne, à l'ombre."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle enfile le manteau, sans à-coup."),
        L("narrateur", "Le tissu frotte le bois du tonneau."),
        L("maman", "Tu l'as, sans foncer."),
        L("narrateur", "La croûte trouve le dernier sec."),
        L("narrateur", "Le cerceau a failli la noyer."),
        L("enfant-f", "Il a failli."),
        L("papa", "Tu as vu la boucle, seule."),
    ],
    (1, 2, 3): [
        L("narrateur", "Chouchou tient le livre sous le lilas."),
        L("narrateur", "Une grappe ombre la page."),
        L("enfant-f", "Le zinc, après la fleur."),
        L("narrateur", "Un pétale colle à la couverture."),
        L("maman", "La gouttière chante plus fort."),
        L("enfant-f", "J'écoute la boucle."),
        L("narrateur", "Personne ne dit le lieu."),
        L("narrateur", "La boucle d'étain cligne, mauve."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, un pouce."),
        L("narrateur", "Le jaune sent le lilas."),
        L("papa", "Tu l'as, sous la grappe."),
        L("narrateur", "La croûte pose, au bord."),
        L("narrateur", "Un pétale a failli la cacher."),
        L("enfant-f", "Presque."),
        L("maman", "Tu as attendu le clignement."),
    ],
    (1, 3, 1): [
        L("narrateur", "Chouchou pose la tasse sur le perron."),
        L("narrateur", "La porcelaine sonne, mince."),
        L("enfant-f", "Le goûter, après le jaune."),
        L("narrateur", "L'assiette veut glisser."),
        L("papa", "Le zinc se noie."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle retient l'assiette, sans tirer."),
        L("narrateur", "La boucle d'étain cligne, sous le bord."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle glisse les bras, tout droit."),
        L("narrateur", "Le manteau se ferme, chaud."),
        L("maman", "Tu l'as, avec la tasse."),
        L("narrateur", "La croûte pose dans un coin de zinc."),
        L("narrateur", "L'eau du perron a failli la prendre."),
        L("enfant-f", "Il a failli."),
        L("papa", "Tu as vu, toute seule."),
    ],
    (1, 3, 2): [
        L("narrateur", "Chouchou pose l'assiette contre le tonneau."),
        L("narrateur", "Le bois mouille le blanc."),
        L("enfant-f", "Le goûter, ici."),
        L("narrateur", "La tasse penche vers l'eau."),
        L("maman", "On y va ?"),
        L("enfant-f", "Pas trop vite."),
        L("narrateur", "Elle redresse la tasse, un doigt."),
        L("narrateur", "La boucle d'étain cligne, sur le cerceau."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, sans à-coup."),
        L("narrateur", "Le jaune frotte le tonneau, froid."),
        L("papa", "Tu l'as, près de l'eau."),
        L("narrateur", "La croûte trouve le coin sec."),
        L("narrateur", "Une giclée a failli tout prendre."),
        L("enfant-f", "Presque trop tard."),
        L("maman", "Tu as attendu le toc."),
    ],
    (1, 3, 3): [
        L("narrateur", "Chouchou pose la tasse sous le lilas."),
        L("narrateur", "Un pétale tombe dedans."),
        L("enfant-f", "Un invité mauve."),
        L("narrateur", "L'assiette cache un peu de jaune."),
        L("papa", "La gouttière monte."),
        L("enfant-f", "J'attends."),
        L("narrateur", "Elle écarte l'assiette, un pouce."),
        L("narrateur", "La boucle d'étain cligne, pâle."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle enfile le manteau, tout droit."),
        L("narrateur", "Le tissu sent la fleur."),
        L("maman", "Tu l'as, avec le pétale."),
        L("narrateur", "La croûte pose, au bord du zinc."),
        L("narrateur", "La grappe a failli la couvrir."),
        L("enfant-f", "Presque."),
        L("papa", "Tu as vu la boucle, seule."),
    ],
    (2, 1, 1): [
        L("narrateur", "Chouchou pose un cube mouillé sur le perron."),
        L("narrateur", "La pierre sonne, basse."),
        L("enfant-f", "Lui d'abord, puis le jaune."),
        L("narrateur", "Le cube glisse vers la marche."),
        L("maman", "Le zinc se noie, presque."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle arrête le cube, sans le chasser."),
        L("narrateur", "La boucle d'étain cligne, nette."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, un pouce."),
        L("narrateur", "Un bras, puis l'autre, au chaud."),
        L("papa", "Tu l'as, sur le pas."),
        L("narrateur", "La croûte pose, ronde."),
        L("narrateur", "Une goutte du gond a failli la noyer."),
        L("enfant-f", "Il a failli."),
        L("maman", "Tu as vu, toute seule."),
    ],
    (2, 1, 2): [
        L("narrateur", "Chouchou pose le cube bleu sur le tonneau."),
        L("narrateur", "Le cerceau est froid, lisse."),
        L("enfant-f", "Il écoute l'eau."),
        L("narrateur", "Le cube penche vers le noir."),
        L("papa", "On tire le manteau ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Elle recule le cube, un doigt."),
        L("narrateur", "La boucle d'étain cligne, à l'ombre."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse les bras, sans tirer."),
        L("narrateur", "Le jaune frotte le bois mouillé."),
        L("maman", "Tu l'as, sans foncer."),
        L("narrateur", "La croûte trouve le coin sec."),
        L("narrateur", "Le tonneau a failli gicler."),
        L("enfant-f", "Presque."),
        L("papa", "Tu as attendu le clignement."),
    ],
    (2, 1, 3): [
        L("narrateur", "Chouchou pose le cube sous le lilas."),
        L("narrateur", "L'herbe est froide, un peu."),
        L("enfant-f", "Une marche de bois, pour moi."),
        L("narrateur", "Une branche touche le jaune."),
        L("maman", "La gouttière monte."),
        L("enfant-f", "J'écoute."),
        L("narrateur", "Elle écarte la branche, lentement."),
        L("narrateur", "La boucle d'étain cligne, mauve."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle enfile le manteau, tout droit."),
        L("narrateur", "Le tissu sent la terre mouillée."),
        L("papa", "Tu l'as, sous les grappes."),
        L("narrateur", "La croûte pose, au bord."),
        L("narrateur", "Un pétale a failli la cacher."),
        L("enfant-f", "Il a failli."),
        L("maman", "Tu as vu la boucle, seule."),
    ],
    (2, 2, 1): [
        L("narrateur", "Chouchou pose le livre ouvert sur le perron."),
        L("narrateur", "Le vent du jardin tourne la page."),
        L("enfant-f", "Reste."),
        L("narrateur", "La page veut cacher le jaune."),
        L("papa", "Le coin sec part."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle retient le coin, sans claquer."),
        L("narrateur", "La boucle d'étain cligne, pâle."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, sans à-coup."),
        L("narrateur", "Le bouton se ferme, net."),
        L("maman", "Tu l'as, après le vent."),
        L("narrateur", "La croûte pose sur le zinc."),
        L("narrateur", "L'eau du pas a failli la prendre."),
        L("enfant-f", "Presque trop tard."),
        L("papa", "Tu as lu le clignement."),
    ],
    (2, 2, 2): [
        L("narrateur", "Chouchou tient le livre contre le tonneau."),
        L("narrateur", "L'image du toit se mouille."),
        L("enfant-f", "Le vrai zinc est là."),
        L("narrateur", "Une goutte vise la page."),
        L("maman", "On rentre ?"),
        L("enfant-f", "Pas sans lui."),
        L("narrateur", "Elle ferme le livre, un pouce."),
        L("narrateur", "La boucle d'étain cligne, sur le cerceau."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse les bras, tout droit."),
        L("narrateur", "Le jaune sent le bois mouillé."),
        L("papa", "Tu l'as, près de l'eau."),
        L("narrateur", "La croûte trouve le dernier sec."),
        L("narrateur", "Le tonneau a failli tout noyer."),
        L("enfant-f", "Il a failli."),
        L("maman", "Tu as vu, toute seule."),
    ],
    (2, 2, 3): [
        L("narrateur", "Chouchou ouvre le livre sous le lilas."),
        L("narrateur", "Une grappe ombre l'image du zinc."),
        L("enfant-f", "Les deux toits."),
        L("narrateur", "Un pétale colle au papier."),
        L("papa", "La gouttière chante plus fort."),
        L("enfant-f", "J'attends la boucle."),
        L("narrateur", "Personne ne dit le mot."),
        L("narrateur", "La boucle d'étain cligne, nette."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, un doigt."),
        L("narrateur", "Le tissu sent la fleur."),
        L("maman", "Tu l'as, sous la grappe."),
        L("narrateur", "La croûte pose, au bord."),
        L("narrateur", "La branche a failli la couvrir."),
        L("enfant-f", "Presque."),
        L("papa", "Tu as attendu le clignement."),
    ],
    (2, 3, 1): [
        L("narrateur", "Chouchou pose la tasse sur le perron mouillé."),
        L("narrateur", "Une goutte sonne dedans, tic."),
        L("enfant-f", "Le goûter, dehors."),
        L("narrateur", "L'assiette glisse vers la marche."),
        L("maman", "Le zinc se noie."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle arrête l'assiette, sans tirer."),
        L("narrateur", "La boucle d'étain cligne, sous le blanc."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle enfile le manteau, tout droit."),
        L("narrateur", "Le jaune se ferme, chaud."),
        L("papa", "Tu l'as, avec la tasse."),
        L("narrateur", "La croûte pose, ronde."),
        L("narrateur", "L'eau du perron a failli la prendre."),
        L("enfant-f", "Il a failli."),
        L("maman", "Tu as vu la boucle, seule."),
    ],
    (2, 3, 2): [
        L("narrateur", "Chouchou pose la tasse sur le tonneau."),
        L("narrateur", "La porcelaine tremble, un peu."),
        L("enfant-f", "Elle écoute l'eau."),
        L("narrateur", "La tasse penche vers le noir."),
        L("papa", "On soulève tout ?"),
        L("enfant-f", "Un pouce."),
        L("narrateur", "Elle redresse la tasse, lentement."),
        L("narrateur", "La boucle d'étain cligne, à l'ombre."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, sans à-coup."),
        L("narrateur", "Le tissu frotte le cerceau."),
        L("maman", "Tu l'as, près de l'eau."),
        L("narrateur", "La croûte trouve le coin sec."),
        L("narrateur", "Une giclée a failli tout prendre."),
        L("enfant-f", "Presque trop tard."),
        L("papa", "Tu as attendu le toc."),
    ],
    (2, 3, 3): [
        L("narrateur", "Chouchou pose l'assiette sous le lilas."),
        L("narrateur", "Un pétale tombe au fond."),
        L("enfant-f", "Un invité."),
        L("narrateur", "La tasse cache un peu de jaune."),
        L("maman", "La gouttière monte."),
        L("enfant-f", "J'attends."),
        L("narrateur", "Elle écarte la tasse, un doigt."),
        L("narrateur", "La boucle d'étain cligne, mauve."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle glisse les bras, tout droit."),
        L("narrateur", "Le manteau sent la fleur mouillée."),
        L("papa", "Tu l'as, avec le pétale."),
        L("narrateur", "La croûte pose, au bord du zinc."),
        L("narrateur", "La grappe a failli la couvrir."),
        L("enfant-f", "Presque."),
        L("maman", "Tu as vu, toute seule."),
    ],
    (3, 1, 1): [
        L("narrateur", "Chouchou pose un cube du tapis sur le perron."),
        L("narrateur", "Le bois tiède rencontre la pierre."),
        L("enfant-f", "Il a voyagé."),
        L("narrateur", "Le cube jaune tremble, humide."),
        L("papa", "Le zinc se noie, presque."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle tient le cube, sans le chasser."),
        L("narrateur", "La boucle d'étain cligne, nette."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, un pouce."),
        L("narrateur", "Un bras, puis l'autre."),
        L("maman", "Tu l'as, depuis la chambre."),
        L("narrateur", "La croûte pose sur le zinc."),
        L("narrateur", "L'eau du pas a failli la prendre."),
        L("enfant-f", "Il a failli."),
        L("papa", "Tu as vu la boucle, seule."),
    ],
    (3, 1, 2): [
        L("narrateur", "Chouchou pose le cube contre le tonneau."),
        L("narrateur", "Le tapis n'est plus là, sous le bois."),
        L("enfant-f", "Il écoute."),
        L("narrateur", "Le cube penche vers l'eau."),
        L("maman", "On tire ?"),
        L("enfant-f", "Non."),
        L("narrateur", "Elle recule le cube, un doigt."),
        L("narrateur", "La boucle d'étain cligne, à l'ombre."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle enfile le manteau, sans tirer."),
        L("narrateur", "Le jaune frotte le cerceau, froid."),
        L("papa", "Tu l'as, sans foncer."),
        L("narrateur", "La croûte trouve le coin sec."),
        L("narrateur", "Le tonneau a failli gicler."),
        L("enfant-f", "Presque."),
        L("maman", "Tu as attendu le clignement."),
    ],
    (3, 1, 3): [
        L("narrateur", "Chouchou pose le cube sous le lilas."),
        L("narrateur", "L'herbe prend la chaleur du tapis."),
        L("enfant-f", "Une marche, pour le jaune."),
        L("narrateur", "Une branche touche le cube."),
        L("papa", "La gouttière monte."),
        L("enfant-f", "J'écoute."),
        L("narrateur", "Elle écarte la branche, lentement."),
        L("narrateur", "La boucle d'étain cligne, pâle."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle glisse les bras, tout droit."),
        L("narrateur", "Le manteau sent la terre."),
        L("maman", "Tu l'as, sous les grappes."),
        L("narrateur", "La croûte pose, au bord."),
        L("narrateur", "Un pétale a failli la cacher."),
        L("enfant-f", "Il a failli."),
        L("papa", "Tu as vu, toute seule."),
    ],
    (3, 2, 1): [
        L("narrateur", "Chouchou pose le livre sur le perron."),
        L("narrateur", "L'image du zinc a quitté la chambre."),
        L("enfant-f", "Le vrai, maintenant."),
        L("narrateur", "Une page prend l'eau de la marche."),
        L("maman", "Le coin sec part."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle soulève la page, sans claquer."),
        L("narrateur", "La boucle d'étain cligne, nette."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, un pouce."),
        L("narrateur", "Le bouton se ferme, chaud."),
        L("papa", "Tu l'as, après l'image."),
        L("narrateur", "La croûte pose, ronde."),
        L("narrateur", "L'eau du perron a failli la noyer."),
        L("enfant-f", "Presque trop tard."),
        L("maman", "Tu as lu le clignement."),
    ],
    (3, 2, 2): [
        L("narrateur", "Chouchou ouvre le livre près du tonneau."),
        L("narrateur", "L'image tremble sur le bois."),
        L("enfant-f", "Le toit est ici."),
        L("narrateur", "Une goutte vise le papier."),
        L("papa", "On rentre ?"),
        L("enfant-f", "Pas sans lui."),
        L("narrateur", "Elle ferme le livre, un doigt."),
        L("narrateur", "La boucle d'étain cligne, sur le cerceau."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle enfile le manteau, sans à-coup."),
        L("narrateur", "Le jaune sent le bois."),
        L("maman", "Tu l'as, près de l'eau."),
        L("narrateur", "La croûte trouve le dernier sec."),
        L("narrateur", "Le tonneau a failli tout prendre."),
        L("enfant-f", "Il a failli."),
        L("papa", "Tu as vu la boucle, seule."),
    ],
    (3, 2, 3): [
        L("narrateur", "Chouchou tient le livre sous le lilas."),
        L("narrateur", "Une grappe ombre l'image du toit."),
        L("enfant-f", "Deux zincs."),
        L("narrateur", "Un pétale colle à la page."),
        L("maman", "La gouttière chante plus fort."),
        L("enfant-f", "J'attends la boucle."),
        L("narrateur", "Personne ne dit le lieu."),
        L("narrateur", "La boucle d'étain cligne, mauve."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, tout droit."),
        L("narrateur", "Le tissu sent la fleur."),
        L("papa", "Tu l'as, sous la grappe."),
        L("narrateur", "La croûte pose, au bord."),
        L("narrateur", "La branche a failli la couvrir."),
        L("enfant-f", "Presque."),
        L("maman", "Tu as attendu le clignement."),
    ],
    (3, 3, 1): [
        L("narrateur", "Chouchou pose la tasse sur le perron."),
        L("narrateur", "La cuillère de la chambre s'est tue."),
        L("enfant-f", "Le goûter, dehors."),
        L("narrateur", "L'assiette glisse vers la pierre."),
        L("papa", "Le zinc se noie."),
        L("enfant-f", "Une seconde."),
        L("narrateur", "Elle arrête l'assiette, sans tirer."),
        L("narrateur", "La boucle d'étain cligne, sous le bord."),
        L("enfant-f", "Là."),
        L("narrateur", "Elle glisse les bras, un pouce."),
        L("narrateur", "Le manteau se ferme, chaud."),
        L("maman", "Tu l'as, avec la tasse."),
        L("narrateur", "La croûte pose sur le zinc."),
        L("narrateur", "L'eau du pas a failli la prendre."),
        L("enfant-f", "Il a failli."),
        L("papa", "Tu as vu, toute seule."),
    ],
    (3, 3, 2): [
        L("narrateur", "Chouchou pose l'assiette contre le tonneau."),
        L("narrateur", "La faïence de la chambre rencontre l'eau."),
        L("enfant-f", "Elle écoute."),
        L("narrateur", "La tasse penche vers le noir."),
        L("maman", "On soulève ?"),
        L("enfant-f", "Un pouce."),
        L("narrateur", "Elle redresse la tasse, lentement."),
        L("narrateur", "La boucle d'étain cligne, à l'ombre."),
        L("enfant-f", "Le manteau."),
        L("narrateur", "Elle tourne la manche, sans à-coup."),
        L("narrateur", "Le jaune frotte le cerceau."),
        L("papa", "Tu l'as, près de l'eau."),
        L("narrateur", "La croûte trouve le coin sec."),
        L("narrateur", "Une giclée a failli tout noyer."),
        L("enfant-f", "Presque trop tard."),
        L("maman", "Tu as attendu le toc."),
    ],
    (3, 3, 3): [
        L("narrateur", "Chouchou pose la tasse sous le lilas."),
        L("narrateur", "Un pétale tombe, comme dans la glace."),
        L("enfant-f", "Un invité mauve."),
        L("narrateur", "L'assiette cache un peu de jaune."),
        L("papa", "La gouttière monte."),
        L("enfant-f", "J'attends."),
        L("narrateur", "Elle écarte l'assiette, un doigt."),
        L("narrateur", "La boucle d'étain cligne, nette."),
        L("enfant-f", "Toi."),
        L("narrateur", "Elle enfile le manteau, tout droit."),
        L("narrateur", "Le tissu sent la fleur, et le tapis."),
        L("maman", "Tu l'as, avec le pétale."),
        L("narrateur", "La croûte pose, au bord du zinc."),
        L("narrateur", "La grappe a failli la couvrir."),
        L("enfant-f", "Presque."),
        L("papa", "Tu as vu la boucle, seule."),
    ],
}

FIN = {
    (1, 1, 1): [
        L("narrateur", "Chouchou raccroche le manteau, au crochet."),
        L("enfant-f", "La croûte est sur le zinc."),
        L("papa", "Oui."),
        L("maman", "Le coin sec a tenu."),
        L("narrateur", "Un cube rouge reste sur le perron."),
        L("enfant-f", "La boucle a cligné, à la fin."),
        L("papa", "Tu l'as attendue."),
        L("narrateur", "La pierre garde une miette, plate."),
        L("narrateur", "La boucle d'étain dort contre le crochet, tiède."),
    ],
    (1, 1, 2): [
        L("narrateur", "Chouchou tient le manteau par la boucle."),
        L("enfant-f", "Il a failli rester au tonneau."),
        L("maman", "Une seconde de plus."),
        L("papa", "Le cerceau était plein."),
        L("narrateur", "Elle le pose au crochet, net."),
        L("enfant-f", "La croûte est là, ronde."),
        L("maman", "Tu l'as vue, seule."),
        L("narrateur", "Un cube rouge sèche sur le bois."),
        L("narrateur", "L'eau du tonneau n'a pas eu le coin sec."),
    ],
    (1, 1, 3): [
        L("narrateur", "Chouchou serre un pétale dans sa main."),
        L("enfant-f", "Il a failli cacher la croûte."),
        L("papa", "Le lilas penche, vide."),
        L("maman", "On rentre."),
        L("narrateur", "Le manteau retrouve le crochet."),
        L("enfant-f", "La boucle a cligné, mauve."),
        L("papa", "Tu as écarté la branche."),
        L("narrateur", "Un cube reste dans l'herbe, oublié."),
        L("narrateur", "Un pétale de lilas colle à la boucle d'étain."),
    ],
    (1, 2, 1): [
        L("narrateur", "Chouchou pose le livre près du crochet."),
        L("enfant-f", "La page a pris l'eau du perron."),
        L("maman", "Elle sèche."),
        L("papa", "Le manteau aussi."),
        L("narrateur", "Elle raccroche le jaune, un bouton."),
        L("enfant-f", "La croûte est sur le zinc."),
        L("maman", "Tu as retenu la page."),
        L("narrateur", "Une goutte ronde reste au coin du livre."),
        L("narrateur", "La marche du perron garde une empreinte jaune."),
    ],
    (1, 2, 2): [
        L("narrateur", "Chouchou ferme le livre, contre elle."),
        L("enfant-f", "L'image a vu le vrai zinc."),
        L("papa", "Oui."),
        L("maman", "Le tonneau s'est tu."),
        L("narrateur", "Le manteau va au crochet, lourd d'eau."),
        L("enfant-f", "La boucle a cligné, à l'ombre."),
        L("papa", "Tu as fermé le livre, à temps."),
        L("narrateur", "Une goutte sèche sur la couverture."),
        L("narrateur", "Le tonneau sonne, une fois, puis plus."),
    ],
    (1, 2, 3): [
        L("narrateur", "Chouchou tient le livre, un pétale dessus."),
        L("enfant-f", "Le lilas a lu avec nous."),
        L("maman", "Oui."),
        L("papa", "On rentre."),
        L("narrateur", "Elle raccroche le manteau, net."),
        L("enfant-f", "La croûte est au bord."),
        L("maman", "Tu as attendu le mauve."),
        L("narrateur", "Le pétale reste entre deux pages."),
        L("narrateur", "Le lilas penche, sans le manteau."),
    ],
    (1, 3, 1): [
        L("narrateur", "Chouchou pose la tasse près du crochet."),
        L("enfant-f", "Le goûter a eu le perron."),
        L("papa", "Une miette, pour plus tard."),
        L("maman", "Le manteau rentre."),
        L("narrateur", "Elle le raccroche, la boucle en avant."),
        L("enfant-f", "La croûte est sur le zinc."),
        L("papa", "Tu as retenu l'assiette."),
        L("narrateur", "La tasse garde une miette, sèche."),
        L("narrateur", "Le perron a une tasse vide, et plus de jaune."),
    ],
    (1, 3, 2): [
        L("narrateur", "Chouchou essuie la tasse, un doigt."),
        L("enfant-f", "Elle a vu le tonneau."),
        L("maman", "Elle a tremblé."),
        L("papa", "Toi, non."),
        L("narrateur", "Le manteau va au crochet, un peu mouillé."),
        L("enfant-f", "La boucle a cligné, sur le cerceau."),
        L("maman", "Tu as redressé la tasse."),
        L("narrateur", "Une goutte sèche au fond du blanc."),
        L("narrateur", "Le cerceau du tonneau n'a plus de jaune."),
    ],
    (1, 3, 3): [
        L("narrateur", "Chouchou verse le pétale de la tasse."),
        L("enfant-f", "L'invité mauve rentre aussi."),
        L("papa", "Dans ta poche ?"),
        L("enfant-f", "Oui."),
        L("narrateur", "Elle raccroche le manteau, tiède."),
        L("maman", "La croûte est au bord."),
        L("papa", "Tu as écarté l'assiette."),
        L("narrateur", "Un pétale reste dans la poche jaune."),
        L("narrateur", "Sous le lilas, la tasse n'a plus de goûter."),
    ],
    (2, 1, 1): [
        L("narrateur", "Chouchou secoue le cube mouillé, une fois."),
        L("enfant-f", "Il a pris le jardin."),
        L("maman", "Et le perron."),
        L("papa", "Le manteau aussi."),
        L("narrateur", "Elle raccroche le jaune, au crochet."),
        L("enfant-f", "La croûte est là."),
        L("maman", "Tu as arrêté le cube."),
        L("narrateur", "Le cube bleu sèche près de la porte."),
        L("narrateur", "Le gond n'a plus de boucle d'étain."),
    ],
    (2, 1, 2): [
        L("narrateur", "Chouchou pose le cube bleu au crochet, non."),
        L("enfant-f", "Lui, dans la caisse."),
        L("papa", "Le manteau, au crochet."),
        L("narrateur", "Elle le pose, net."),
        L("enfant-f", "Le tonneau a failli."),
        L("maman", "Tu as reculé le cube."),
        L("papa", "La croûte est sèche, un peu."),
        L("narrateur", "Le cube bleu garde une goutte, ronde."),
        L("narrateur", "Sur le tonneau, plus rien ne penche."),
    ],
    (2, 1, 3): [
        L("narrateur", "Chouchou ramasse le cube sous le lilas."),
        L("enfant-f", "Il sent l'herbe."),
        L("maman", "Le manteau sent la terre."),
        L("papa", "Au crochet, maintenant."),
        L("narrateur", "Elle raccroche, la boucle en avant."),
        L("enfant-f", "La croûte est au bord."),
        L("maman", "Tu as écarté la branche."),
        L("narrateur", "Un brin d'herbe colle au cube."),
        L("narrateur", "Le lilas n'a plus de marche de bois."),
    ],
    (2, 2, 1): [
        L("narrateur", "Chouchou ferme le livre, le vent dedans."),
        L("enfant-f", "La page a voulu partir."),
        L("papa", "Tu l'as retenue."),
        L("maman", "Le manteau aussi."),
        L("narrateur", "Elle le raccroche, près de la porte."),
        L("enfant-f", "La croûte est sur le zinc."),
        L("papa", "Tu as lu le clignement, dehors."),
        L("narrateur", "Un coin de page reste un peu gonflé."),
        L("narrateur", "Sur le perron, le vent n'a plus de page."),
    ],
    (2, 2, 2): [
        L("narrateur", "Chouchou essuie la couverture, un doigt."),
        L("enfant-f", "Le vrai zinc a mouillé l'image."),
        L("maman", "Oui."),
        L("papa", "Le tonneau s'est tu."),
        L("narrateur", "Le manteau va au crochet, lourd."),
        L("enfant-f", "La boucle a cligné, sur le cerceau."),
        L("maman", "Tu as fermé le livre."),
        L("narrateur", "Une goutte sèche au milieu du toit dessiné."),
        L("narrateur", "Le tonneau n'a plus de page ouverte."),
    ],
    (2, 2, 3): [
        L("narrateur", "Chouchou souffle le pétale du livre."),
        L("enfant-f", "Il a lu le lilas."),
        L("papa", "Les deux toits."),
        L("maman", "On rentre."),
        L("narrateur", "Elle raccroche le manteau, net."),
        L("enfant-f", "La croûte est au bord."),
        L("papa", "Tu as attendu sous la grappe."),
        L("narrateur", "Un parfum mauve reste dans les pages."),
        L("narrateur", "Sous le lilas, plus d'image de zinc."),
    ],
    (2, 3, 1): [
        L("narrateur", "Chouchou vide la tasse, une goutte."),
        L("enfant-f", "Le perron a sonné dedans."),
        L("maman", "Tic."),
        L("papa", "Le manteau rentre."),
        L("narrateur", "Elle le raccroche, la boucle tiède."),
        L("enfant-f", "La croûte est ronde, sur le zinc."),
        L("maman", "Tu as arrêté l'assiette."),
        L("narrateur", "La tasse sèche près du gond."),
        L("narrateur", "Le perron n'a plus de porcelaine."),
    ],
    (2, 3, 2): [
        L("narrateur", "Chouchou pose la tasse, loin du tonneau."),
        L("enfant-f", "Elle a tremblé, pas moi."),
        L("papa", "Toi, tu as attendu."),
        L("maman", "Le manteau aussi."),
        L("narrateur", "Elle le pose au crochet, un peu mouillé."),
        L("enfant-f", "La croûte est sèche."),
        L("papa", "Tu as redressé la tasse."),
        L("narrateur", "Une goutte sèche au fond, ronde."),
        L("narrateur", "Le cerceau n'a plus de porcelaine qui penche."),
    ],
    (2, 3, 3): [
        L("narrateur", "Chouchou garde le pétale dans la tasse."),
        L("enfant-f", "L'invité du lilas."),
        L("maman", "Il rentre avec nous."),
        L("papa", "Le manteau aussi."),
        L("narrateur", "Elle raccroche le jaune, net."),
        L("enfant-f", "La croûte est au bord."),
        L("maman", "Tu as écarté la tasse."),
        L("narrateur", "Le pétale flotte, minuscule, dans le blanc."),
        L("narrateur", "Sous le lilas, plus de goûter."),
    ],
    (3, 1, 1): [
        L("narrateur", "Chouchou pose le cube du tapis près du crochet."),
        L("enfant-f", "Il a vu la chambre, et le perron."),
        L("papa", "Deux voyages."),
        L("maman", "Le manteau, un seul."),
        L("narrateur", "Elle le raccroche, la boucle en avant."),
        L("enfant-f", "La croûte est sur le zinc."),
        L("papa", "Tu as tenu le cube."),
        L("narrateur", "Un fil de tapis colle au bois."),
        L("narrateur", "Le perron a le cube, plus le jaune."),
    ],
    (3, 1, 2): [
        L("narrateur", "Chouchou range le cube, loin de l'eau."),
        L("enfant-f", "Le tonneau n'a pas eu le tapis."),
        L("maman", "Ni le manteau."),
        L("papa", "Au crochet."),
        L("narrateur", "Elle le pose, net."),
        L("enfant-f", "La boucle a cligné, à l'ombre."),
        L("maman", "Tu as reculé le cube."),
        L("narrateur", "Le cube sent le bois mouillé, un peu."),
        L("narrateur", "Sur le tonneau, plus de cube qui penche."),
    ],
    (3, 1, 3): [
        L("narrateur", "Chouchou ramasse le cube, une feuille dessus."),
        L("enfant-f", "Le lilas a donné l'herbe."),
        L("papa", "Le manteau, la terre."),
        L("maman", "Au crochet, maintenant."),
        L("narrateur", "Elle raccroche, tiède."),
        L("enfant-f", "La croûte est au bord."),
        L("papa", "Tu as écarté la branche."),
        L("narrateur", "Un brin d'herbe reste sur le cube jaune."),
        L("narrateur", "Sous le lilas, plus de marche de tapis."),
    ],
    (3, 2, 1): [
        L("narrateur", "Chouchou essuie la page, du bout du doigt."),
        L("enfant-f", "L'image a quitté la chambre, mouillée."),
        L("maman", "Le vrai zinc l'a vue."),
        L("papa", "Le manteau rentre."),
        L("narrateur", "Elle le raccroche, un bouton."),
        L("enfant-f", "La croûte est ronde."),
        L("maman", "Tu as soulevé la page."),
        L("narrateur", "Un coin de papier reste gonflé, sur le perron d'avant."),
        L("narrateur", "La glace de la chambre n'a plus de jaune."),
    ],
    (3, 2, 2): [
        L("narrateur", "Chouchou ferme le livre, une goutte au milieu."),
        L("enfant-f", "Le tonneau a signé l'image."),
        L("papa", "Une ronde, minuscule."),
        L("maman", "Le manteau, au crochet."),
        L("narrateur", "Elle le pose, lourd d'eau."),
        L("enfant-f", "La boucle a cligné, sur le cerceau."),
        L("papa", "Tu as fermé le livre."),
        L("narrateur", "La goutte sèche sur le toit dessiné."),
        L("narrateur", "Le tiroir de la chambre reste ouvert, vide de jaune."),
    ],
    (3, 2, 3): [
        L("narrateur", "Chouchou laisse le pétale dans le livre."),
        L("enfant-f", "Un signet mauve."),
        L("maman", "Du lilas."),
        L("papa", "Le manteau rentre."),
        L("narrateur", "Elle le raccroche, net."),
        L("enfant-f", "La croûte est au bord."),
        L("maman", "Tu as attendu sous la grappe."),
        L("narrateur", "Le parfum reste entre l'image et la page."),
        L("narrateur", "L'armoire n'a plus de livre ouvert."),
    ],
    (3, 3, 1): [
        L("narrateur", "Chouchou pose la tasse, la cuillère à côté."),
        L("enfant-f", "Elle s'est tue, dans la chambre."),
        L("papa", "Et dehors."),
        L("maman", "Le manteau, au crochet."),
        L("narrateur", "Elle le raccroche, la boucle tiède."),
        L("enfant-f", "La croûte est sur le zinc."),
        L("papa", "Tu as arrêté l'assiette."),
        L("narrateur", "La cuillère reste muette, près de la porte."),
        L("narrateur", "Le perron n'a plus de faïence de chambre."),
    ],
    (3, 3, 2): [
        L("narrateur", "Chouchou essuie l'assiette, un peu d'eau."),
        L("enfant-f", "Le tonneau a voulu le goûter."),
        L("maman", "Toi, tu as redressé."),
        L("papa", "Le manteau aussi."),
        L("narrateur", "Elle le pose au crochet, mouillé au bas."),
        L("enfant-f", "La croûte est sèche."),
        L("maman", "Tu as attendu le toc."),
        L("narrateur", "Une goutte sèche au fond de l'assiette."),
        L("narrateur", "Le lit n'attend plus la dînette."),
    ],
    (3, 3, 3): [
        L("narrateur", "Chouchou range la tasse, le pétale dedans."),
        L("enfant-f", "Comme dans la glace, mauve."),
        L("papa", "L'invité rentre."),
        L("maman", "Le manteau aussi."),
        L("narrateur", "Elle raccroche le jaune, au crochet."),
        L("enfant-f", "La croûte est au bord du zinc."),
        L("papa", "Tu as écarté l'assiette."),
        L("narrateur", "Le pétale reste, minuscule, dans le blanc."),
        L("narrateur", "La glace de la chambre n'a plus de manteau plié."),
    ],
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | le manteau | son manteau | le manteau jaune",
    "retry_prompt": "Le manteau jaune. Chouchou a pris quoi ?",
}

SONS_L1 = {1: "pain,casserole", 2: "gouttiere,porte", 3: "tissu,tiroir"}
SONS_L2 = {1: "cubes,bois", 2: "livre,papier", 3: "dinette,assiette"}
SONS_L3 = {1: "perron,gouttiere", 2: "tonneau,eau", 3: "lilas,vent"}
SONS_FIN = {1: "crochet,pain", 2: "manteau,eau", 3: "lilas,tissu"}


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
            s[f"{p2}_T0003_P0000"] = T3[i]
            meta[f"{p2}_T0003_P0000"] = {
                "option_1_label": "le perron",
                "option_2_label": "le tonneau",
                "option_3_label": "le lilas",
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
        return "gouttiere,pain"
    if kind in {"transition_question", "passage_question"}:
        return ""
    if kind == "passage_fin":
        return SONS_FIN.get(k or 1, "crochet,pain")
    if cid.endswith("_C0001"):
        return "pain,tissu"
    if i and "_T0002_P000" in cid and "_T0003_" not in cid:
        if cid.endswith(("_P0001", "_P0002", "_P0003")):
            return SONS_L2.get(j or 1, "bois")
        return ""
    if "_T0003_P000" in cid and cid[-1] in "123":
        return SONS_L3.get(k or 1, "gouttiere")
    if i:
        return SONS_L1.get(i, "pain")
    return "gouttiere"


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
        extra["emphasis"] = "boucle d'étain"
    elif prof == "clue":
        extra["emphasis"] = "manteau"
    elif prof == "confirm":
        extra["emphasis"] = "manteau jaune"
    elif prof == "resolution":
        extra["emphasis"] = "boucle d'étain" if "boucle" in low else "manteau"
    elif prof == "ending":
        extra["emphasis"] = "boucle d'étain" if "boucle d'étain" in low else None
    elif prof == "action":
        extra["emphasis"] = "manteau" if "manteau" in low else None
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
        "Chouchou veut son manteau jaune pour porter la croûte chaude jusqu'au zinc, "
        "avant que la gouttière noie le dernier coin sec. Une boucle d'étain cligne "
        "sur le manteau, comme le zinc. Elle tire trop fort : la manche se retourne, "
        "la boucle s'accroche. Cuisine, jardin ou chambre : le manteau reste. "
        "Cubes, livre ou dînette volent le clignement. Elle refuse de foncer, "
        "écoute la gouttière. Perron, tonneau ou lilas : la boucle se paie. "
        "La croûte pose. Le manteau rentre au crochet. La boucle reste."
    )
    out["title"] = "Le manteau jaune près de la gouttière"
    out["characters"] = "Chouchou, papa, maman"
    out["setting"] = "cuisine, pain grillé, vitre, zinc, gouttière, crochet"
    out["chunks"] = out_chunks
    check(SID, out["age_band"], out["chunks"])
    joined = "\n".join(c["script"] for c in out_chunks).lower()
    if joined.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment x{joined.count('en ce moment')}")
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
        f"# TREE-AUT-037 — Le manteau jaune près de la gouttière\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Titre noyau :** *Le manteau jaune près de la gouttière*\n"
        "- **Public :** N2 (≤ 15 mots/phrase)\n"
        "- **Leçon :** AUT.AFF.002 — prendre son manteau pour sortir, le raccrocher, "
        "vécue (manche tournée, boucle, crochet ; personne ne récite la règle)\n"
        "- **Personnages :** Chouchou, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Le grille-pain fait clic. La buée dessine une rivière d'argent sur la vitre, "
        "la même que le zinc. Le manteau jaune attend au crochet. Une boucle d'étain "
        "cligne, une fois. Chouchou veut porter la croûte chaude jusqu'au zinc, avant "
        "que la gouttière noie le dernier coin sec. Elle tire trop fort : la manche "
        "se retourne, la boucle s'accroche. Cuisine, jardin ou chambre : le manteau "
        "reste avec elle. Cubes, livre ou dînette volent le clignement. Elle refuse "
        "de foncer, observe le jaune, écoute la gouttière. Perron, tonneau ou lilas : "
        "la boucle se paie. La croûte pose. Le manteau rentre au crochet.\n\n"
        "## Vécu\n\n"
        "Cuisine, pain grillé, vitre, zinc, gouttière, crochet, boucle d'étain, "
        "perron, tonneau, lilas. Impatience (vite, la croûte), découragement "
        "(sourire disparu, poitrine, manche à l'envers), fierté calme (sans foncer, "
        "le clignement). Merci vécu quand elle nomme le manteau. Question : elle a "
        "pris quoi, près du crochet. T1 cuisine / jardin / chambre. T2 cubes / "
        "livre / dînette. T3 perron / tonneau / lilas. 1er choix = lieux, n'enlève "
        "pas le manteau.\n\n"
        "## Vu et corrigé\n\n"
        "P2 F-NAR-019 example4 v2. Ouverture inventée (clic du grille-pain, rivière "
        "de buée), pas les cinq manières listées. Indice unique : boucle d'étain, "
        "payée au climax (cligne à l'ombre, toc, mauve). Corps : sourire disparaît, "
        "envie et inquiétude, adulte à la même hauteur. 2e ruse (cube, page, "
        "assiette) ; elle refuse de foncer. Fin qui a failli (goutte, giclée, "
        "pétale, une seconde). Monde ≠ TREE-AUT-032 manteau vert casserole ≠ "
        "TREE-AUT-033 gouttière kiosque. Pas gabarit example3. Tics « encore / "
        "déjà / tout doux / tout calme » retirés. Troupe D16 Chouchou. 27 fins, "
        "27 L3, 27 dernières images. TTS par chunk : `notes`, `text_ssml`, "
        "`text_xai_tags`, piper 1.10–1.30. `slow` = choix, indice, fins. "
        f"`check()` N2 OK. Chemins {mn}–{mx} mots, moyenne {moy}. Pas apply.\n\n"
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
