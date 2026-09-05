#!/usr/bin/env python3
"""TREE-AUT-031 — Le sac vert d'Aniss sur le banc. F-NAR-019 v2. N2. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words

SID = "TREE-AUT-031"
LIM = 15
TICS = ("tout doux", "tout calme", "encore", "déjà")
BAN = (
    "escargot", "loupe", "carnet bleu", "pots de menthe", "vélo rouge",
    "hugo", "sarah", "ranger", "tu ranges", "après le jeu",
    "mission accomplie", "j'ai compris", "on dirait que notre mission",
    "lumière couleur de miel", "gouttes pendent", "aujourd'hui",
    "grand-père", "maîtresse", "jardinier", "bibliothécaire", "gardienne",
    "merle", "miel", "croissant de buée", "étoile brune", "laitue",
    "sac jaune", "sac bleu", "dent de fermeture", "buée",
    "noé", "noe",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 138, "speed": 0.96, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 280,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de lessive",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le sac vide veut le parc; "
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
            "destinataire=enfant; sous_texte=ton choix change le coin du parc; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "sac",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=le doudou glisse dans le sac; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 128, "speed": 0.90, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 290,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "sac",
        "note": (
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=le sac voyage avec lui; "
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
            "destinataire=enfant; sous_texte=le jeu résiste, il refuse de foncer; "
            "tempo=vif; sourire=léger; respiration=courte"
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
            "intensite=2; destinataire=enfant; sous_texte=le sac glisse, trop léger; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 136, "speed": 0.95, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de lessive",
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=le grain guide, il glisse dans le sac; "
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
            "destinataire=enfant; sous_texte=le grain de lessive a voyagé; "
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
    for raw_p in parts:
        p = raw_p.strip()
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
    L("narrateur", "La boucle jaune cliquette, toute seule."),
    L("narrateur", "Une chaussette tiède a quitté le panier."),
    L("narrateur", "Elle a heurté le sac vert, sur le banc."),
    L("narrateur", "Un grain de lessive reste collé au métal."),
    L("narrateur", "Il est blanc, minuscule, un peu rêche."),
    L("narrateur", "L'entrée sent le linge chaud."),
    L("papa", "Tu as vu ce grain, Aniss ?"),
    L("enfant-m", "Il pique, papa."),
    L("maman", "Le panier se tait, peu à peu."),
    L("narrateur", "Le bois du banc est clair, lisse."),
    L("narrateur", "Les bottes attendent près de la porte."),
    L("enfant-m", "Le parc, vite !"),
    L("narrateur", "Aniss saute. Ses talons tapent."),
    L("narrateur", "En ce moment, il tire le sac."),
    L("narrateur", "La sangle est lisse, trop légère."),
    L("narrateur", "La boucle résiste, sèche, un peu raide."),
    L("enfant-m", "Il est vide !"),
    L("narrateur", "Le sourire d'Aniss disparaît."),
    L("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    L("papa", "On s'accroupit ?"),
    L("narrateur", "Papa se met à sa hauteur."),
    L("maman", "Le doudou, sous le linge ?"),
    L("narrateur", "Aniss fouille le panier tiède."),
    L("narrateur", "Une oreille grise dépasse, puis un ventre."),
    L("narrateur", "Le grain de lessive brille sur le tissu."),
    L("enfant-m", "Te voilà."),
    L("narrateur", "Il glisse le doudou dans le sac."),
    L("maman", "Merci, Aniss."),
    L("papa", "Le sac vient avec nous ?"),
    L("enfant-m", "Oui. Avec moi."),
    L("narrateur", "La boucle cliquette, plus lourde."),
    L("narrateur", "Le grain de lessive voyage sur le métal."),
]

T1 = [
    L("narrateur", "Le parc ouvre trois coins."),
    L("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
    L("maman", "Où le sac vert pose sa sangle ?"),
]

L1 = {
    1: [
        L("narrateur", "Le quai de bois du bac est frais."),
        L("narrateur", "Le sable sent la terre humide."),
        L("enfant-m", "C'est mon quai !"),
        L("papa", "Le sac reste avec toi ?"),
        L("enfant-m", "Je le pose, je cours."),
        L("narrateur", "Aniss jette le sac contre le bois."),
        L("narrateur", "La boucle cliquette, trop vite."),
        L("narrateur", "Le sac glisse, s'ouvre, trop léger."),
        L("narrateur", "Le doudou penche vers le sable."),
        L("enfant-m", "Oh non."),
        L("narrateur", "Les épaules d'Aniss baissent."),
        L("maman", "Je m'accroupis, d'accord ?"),
        L("narrateur", "Maman se met à sa hauteur."),
        L("enfant-m", "Il voulait le quai, pas le sable."),
    ],
    2: [
        L("narrateur", "La pente tiède du toboggan brille."),
        L("narrateur", "Le plastique sent le soleil."),
        L("enfant-m", "Je glisse, le premier !"),
        L("maman", "Et le sac ?"),
        L("enfant-m", "En bas. Je le rattrape."),
        L("narrateur", "Aniss grimpe trop vite, les deux mains."),
        L("narrateur", "Le sac reste au pied, seul."),
        L("narrateur", "La sangle glisse dans l'herbe."),
        L("narrateur", "Le doudou touche presque le sol."),
        L("enfant-m", "Il tombe !"),
        L("narrateur", "Aniss s'arrête à mi-marche, les joues chaudes."),
        L("papa", "On s'accroupit, en bas ?"),
        L("narrateur", "Papa se met à sa hauteur, près du sac."),
        L("enfant-m", "Je le voulais avec moi."),
    ],
    3: [
        L("narrateur", "Au nid des chaînes, ça craque un peu."),
        L("narrateur", "Sous Aniss, le siège de bois est lisse, froid."),
        L("enfant-m", "Mon nid !"),
        L("papa", "Le sac, près de toi ?"),
        L("enfant-m", "Dans l'herbe, ça va."),
        L("narrateur", "Aniss s'assoit trop vite."),
        L("narrateur", "Le sac reste trop loin, mou."),
        L("narrateur", "Une chaîne accroche la sangle, puis la lâche."),
        L("narrateur", "Le doudou roule hors du bord."),
        L("enfant-m", "Zut."),
        L("narrateur", "Le menton d'Aniss baisse."),
        L("maman", "Je m'accroupis, près de l'herbe ?"),
        L("narrateur", "Maman se met à sa hauteur."),
        L("enfant-m", "Il n'est plus dans le nid."),
    ],
}

Q = {
    1: [
        L("narrateur", "Le doudou penche hors du sac."),
        L("papa", "Aniss met où le doudou ?"),
    ],
    2: [
        L("narrateur", "Les affaires touchent l'herbe, au pied."),
        L("maman", "Aniss met où les affaires ?"),
    ],
    3: [
        L("narrateur", "Le doudou a quitté le bord du sac."),
        L("papa", "Aniss met où le doudou ?"),
    ],
}

C = {
    1: [
        L("narrateur", "Aniss rattrape l'oreille grise."),
        L("narrateur", "Il la glisse au fond, bien droit."),
        L("narrateur", "La boucle cliquette, fermée."),
        L("papa", "Merci, Aniss."),
        L("maman", "Le grain est là, sur le métal."),
        L("enfant-m", "On reste au quai ?"),
        L("papa", "Avec le sac, oui."),
        L("narrateur", "Un filet de sable brille sur le bois."),
    ],
    2: [
        L("narrateur", "Aniss redescend, une marche, puis l'autre."),
        L("narrateur", "Il glisse le doudou, puis ferme."),
        L("narrateur", "La sangle revient contre son ventre."),
        L("maman", "Merci, Aniss."),
        L("papa", "Le grain voyage avec la boucle."),
        L("enfant-m", "Je grimpe avec lui ?"),
        L("maman", "Avec le sac, oui."),
        L("narrateur", "Le plastique tiède attend, muet."),
    ],
    3: [
        L("narrateur", "Aniss pose un pied au sol."),
        L("narrateur", "Il glisse le doudou, au fond."),
        L("narrateur", "La sangle reste près de sa main."),
        L("papa", "Merci, Aniss."),
        L("maman", "Le grain pique un peu, sur le métal."),
        L("enfant-m", "Le nid, avec le sac ?"),
        L("papa", "Oui. Tout près."),
        L("narrateur", "Une chaîne se tait, un instant."),
    ],
}

T2 = {
    1: [
        L("maman", "Quel jeu aide le quai ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    2: [
        L("papa", "Quel jeu aide la pente ?"),
        L("maman", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
    3: [
        L("maman", "Quel jeu aide le nid ?"),
        L("papa", "Le ballon, le seau, ou le doudou ?"),
        L("narrateur", "Tu choisis."),
    ],
}

L2 = {
    (1, 1): [
        L("narrateur", "Près du quai, le ballon rouge attend."),
        L("narrateur", "Il est lisse, un peu frais."),
        L("enfant-m", "Il pousse le sable !"),
        L("narrateur", "Aniss frappe trop fort."),
        L("narrateur", "Le ballon chasse le sac vers le bord."),
        L("narrateur", "La boucle s'ouvre. Le doudou penche."),
        L("enfant-m", "Il va au sable !"),
        L("papa", "Tu cours après le ballon ?"),
        L("narrateur", "Aniss veut foncer. Puis il s'arrête."),
        L("narrateur", "Sur le métal, le grain de lessive brille."),
        L("enfant-m", "Le sac d'abord."),
        L("maman", "Tu l'as vu, toi."),
        L("narrateur", "Il rentre l'oreille, sans courir."),
    ],
    (1, 2): [
        L("narrateur", "Près du quai, le seau jaune sonne."),
        L("narrateur", "L'anse est froide, un peu rêche."),
        L("enfant-m", "Une rivière, beaucoup !"),
        L("narrateur", "Aniss verse d'un coup, trop haut."),
        L("narrateur", "Le sable entre dans le sac ouvert."),
        L("narrateur", "Le doudou disparaît sous un tas."),
        L("enfant-m", "Je le vois plus !"),
        L("maman", "Le grain, Aniss ?"),
        L("narrateur", "Aniss refuse de fouiller au hasard."),
        L("narrateur", "Le grain de lessive pique, hors du tas."),
        L("enfant-m", "La boucle est là."),
        L("papa", "Tu as regardé, avant de creuser."),
        L("narrateur", "Il sort l'oreille, puis ferme."),
    ],
    (1, 3): [
        L("narrateur", "Près du quai, Aniss sort le doudou."),
        L("narrateur", "Une oreille a un peu de sable."),
        L("enfant-m", "Il sera ma pelle !"),
        L("narrateur", "Il creuse trop vite, le ventre gris."),
        L("narrateur", "Le doudou se confond avec le sable."),
        L("enfant-m", "Il s'est caché !"),
        L("papa", "Une oreille, ou un tas ?"),
        L("narrateur", "Aniss refuse de jeter le sable."),
        L("narrateur", "Le grain de lessive brille sur le tissu."),
        L("enfant-m", "Là. L'oreille."),
        L("maman", "Le grain l'a dit."),
        L("narrateur", "Il glisse le doudou, sans le secouer."),
        L("narrateur", "Le sac redevient un peu lourd."),
    ],
    (2, 1): [
        L("narrateur", "Au pied de la pente, le ballon attend."),
        L("narrateur", "Il est froid, près du plastique."),
        L("enfant-m", "Il sera le tapis, en bas !"),
        L("narrateur", "Aniss lance le ballon, puis se lance."),
        L("narrateur", "Le ballon roule sous la rampe, disparaît."),
        L("narrateur", "Le sac, en haut, reste seul."),
        L("enfant-m", "Je plonge !"),
        L("maman", "Le sac, Aniss ?"),
        L("narrateur", "Aniss refuse de plonger au hasard."),
        L("narrateur", "En haut, le grain de lessive pique au soleil."),
        L("enfant-m", "Je redescends avec lui."),
        L("papa", "Puis le ballon, sous la pente."),
        L("narrateur", "La sangle revient contre son ventre."),
    ],
    (2, 2): [
        L("narrateur", "Au toboggan, le seau sonne contre une marche."),
        L("narrateur", "L'anse est froide."),
        L("enfant-m", "Il m'attrape, en bas !"),
        L("narrateur", "Aniss pose le seau, puis glisse avec le sac."),
        L("narrateur", "La sangle accroche une marche. Ça résiste."),
        L("enfant-m", "Je suis coincé !"),
        L("papa", "Tirer plus fort ?"),
        L("narrateur", "Aniss refuse de tirer."),
        L("narrateur", "Il recule. Le grain de lessive apparaît, net."),
        L("enfant-m", "La sangle, au-dessus, pas dessous."),
        L("maman", "Tu as regardé le grain."),
        L("narrateur", "Il passe la sangle par-dessus l'épaule."),
        L("narrateur", "Le seau attend en bas, droit."),
    ],
    (2, 3): [
        L("narrateur", "Au toboggan, le doudou a vu la pente."),
        L("narrateur", "L'oreille grise est un peu froide."),
        L("enfant-m", "Il glisse avec moi !"),
        L("narrateur", "Aniss pose le doudou, puis se lance."),
        L("narrateur", "Le tissu file, disparaît dans l'herbe."),
        L("enfant-m", "Je le vois plus !"),
        L("maman", "Foncer dans l'herbe ?"),
        L("narrateur", "Aniss refuse de foncer."),
        L("narrateur", "Sur le plastique, un grain de lessive reste."),
        L("enfant-m", "Il a glissé là."),
        L("papa", "L'herbe, juste après, alors."),
        L("narrateur", "L'oreille grise est là, au bord."),
        L("narrateur", "Il la glisse, sans la jeter."),
    ],
    (3, 1): [
        L("narrateur", "Près des chaînes, le ballon a de l'herbe."),
        L("narrateur", "Un brin colle au cuir."),
        L("enfant-m", "On roule, et moi je vole !"),
        L("narrateur", "Aniss pousse le ballon en se balançant."),
        L("narrateur", "Le rouge disparaît dans les brins."),
        L("narrateur", "Le sac, trop loin, s'affaisse."),
        L("enfant-m", "Je saute !"),
        L("papa", "Le sac d'abord ?"),
        L("narrateur", "Aniss refuse de sauter au hasard."),
        L("narrateur", "Sur la sangle, le grain de lessive pique."),
        L("enfant-m", "Je le ramène, puis je cherche."),
        L("maman", "Pas dans la fausse mer d'herbe."),
        L("narrateur", "Le ballon s'immobilise, un brin collé."),
    ],
    (3, 2): [
        L("narrateur", "Près du nid, le seau est dans l'herbe."),
        L("narrateur", "L'anse est froide, près de la corde."),
        L("enfant-m", "Il attrape le ciel !"),
        L("narrateur", "Aniss pose le seau sous le siège."),
        L("narrateur", "Il se balance, trop fort."),
        L("narrateur", "Le siège tape l'anse. La sangle s'accroche."),
        L("enfant-m", "Ça tire !"),
        L("maman", "Tirer la sangle ?"),
        L("narrateur", "Aniss refuse de tirer."),
        L("narrateur", "Il descend. Le grain de lessive montre le nœud."),
        L("enfant-m", "Je desserre, sans forcer."),
        L("papa", "Le seau, plus loin, alors."),
        L("narrateur", "L'anse se tait, dans l'herbe."),
    ],
    (3, 3): [
        L("narrateur", "Près du nid, le doudou a du vent."),
        L("narrateur", "L'oreille molle clignote."),
        L("enfant-m", "Il s'assoit avec moi."),
        L("narrateur", "Aniss pompe trop fort, les deux sur les genoux."),
        L("narrateur", "Doudou et sac tombent sur la terre sèche."),
        L("enfant-m", "Aïe."),
        L("papa", "Le nid est le bois, pas la terre."),
        L("narrateur", "Aniss veut tout ramasser d'un coup."),
        L("narrateur", "Puis il refuse de foncer."),
        L("narrateur", "Le grain de lessive brille sur l'oreille."),
        L("enfant-m", "Lui d'abord, dans le sac."),
        L("maman", "Puis tu remontes."),
        L("narrateur", "L'oreille grise a un peu de poussière."),
    ],
}


def t3_lines(i: int, j: int) -> list[str]:
    start = {
        (1, 1): "papa|Le ballon s'est tu. Il manque quoi ?",
        (1, 2): "maman|Le seau a versé. Il manque quoi ?",
        (1, 3): "papa|Le doudou a du sable. Il manque quoi ?",
        (2, 1): "maman|Le ballon a disparu. Il manque quoi ?",
        (2, 2): "papa|La sangle a lâché. Il manque quoi ?",
        (2, 3): "maman|L'oreille a glissé. Il manque quoi ?",
        (3, 1): "papa|L'herbe a caché. Il manque quoi ?",
        (3, 2): "maman|L'anse s'est tue. Il manque quoi ?",
        (3, 3): "papa|Le doudou a du vent. Il manque quoi ?",
    }[(i, j)]
    return [
        start,
        L("maman", "La casquette, la gourde, ou le goûter ?"),
        L("narrateur", "Tu choisis."),
    ]


L3 = {
    (1, 1, 1): [
        L("narrateur", "Le soleil pique les yeux d'Aniss."),
        L("enfant-m", "Ma casquette !"),
        L("narrateur", "Il fouille le sac. Rien."),
        L("narrateur", "Elle était sur le banc, à la maison."),
        L("papa", "Dans ma poche. Tu la mets où ?"),
        L("narrateur", "Aniss la pose sur sa tête, trop vite."),
        L("narrateur", "Le vent la pousse vers le sable."),
        L("enfant-m", "Elle part !"),
        L("maman", "Le grain, sur la visière ?"),
        L("narrateur", "Un grain de lessive pique le tissu bleu."),
        L("narrateur", "Aniss refuse de foncer après le vent."),
        L("narrateur", "Il glisse la casquette dans le sac, d'abord."),
        L("enfant-m", "Puis sur ma tête, après."),
        L("papa", "Tu l'as gardée, toi."),
    ],
    (1, 1, 2): [
        L("narrateur", "Aniss a la bouche sèche, après le ballon."),
        L("enfant-m", "J'ai soif !"),
        L("narrateur", "Il ouvre le sac. Pas de gourde."),
        L("narrateur", "Elle était près des bottes."),
        L("papa", "Je l'ai. Tu la mets où ?"),
        L("narrateur", "Aniss boit d'un trait, le bouchon trop vite."),
        L("narrateur", "Un filet tombe vers le sable, vers le sac."),
        L("enfant-m", "Oh."),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste collé au plastique."),
        L("narrateur", "Aniss referme, refuse de reboire debout."),
        L("narrateur", "Il glisse la gourde dans le sac."),
        L("enfant-m", "Elle voyage, maintenant."),
        L("papa", "Sans mouiller le doudou."),
    ],
    (1, 1, 3): [
        L("narrateur", "Le vent apporte une odeur de pomme."),
        L("enfant-m", "J'ai faim, un peu."),
        L("narrateur", "Il cherche dans le sac. Rien."),
        L("narrateur", "Le goûter était dans le torchon du panier."),
        L("maman", "Je le tends. Tu le mets où ?"),
        L("narrateur", "Aniss croque trop vite, une main trop pleine."),
        L("narrateur", "Une miette file vers le sable, le torchon aussi."),
        L("enfant-m", "Il s'en va !"),
        L("papa", "Le grain, sur le linge ?"),
        L("narrateur", "Un grain de lessive brille sur le carreau."),
        L("narrateur", "Aniss refuse de courir après la miette."),
        L("narrateur", "Il glisse le torchon dans le sac."),
        L("enfant-m", "La pomme rentre, elle aussi."),
        L("maman", "Le quai n'a pas eu le goûter."),
    ],
    (1, 2, 1): [
        L("narrateur", "Le soleil tape, pendant que le seau sonne."),
        L("enfant-m", "Ça pique !"),
        L("narrateur", "Pas de casquette dans le sac."),
        L("papa", "Elle était sur le banc. Ma poche."),
        L("narrateur", "Aniss veut la mettre, le seau à l'autre main."),
        L("narrateur", "L'anse cogne. La visière tombe vers le tas."),
        L("enfant-m", "Dans le sable !"),
        L("maman", "Le seau d'abord, au sol ?"),
        L("narrateur", "Aniss refuse de plonger les deux mains."),
        L("narrateur", "Un grain de lessive pique la visière, hors du tas."),
        L("narrateur", "Il pose le seau. Puis il glisse la casquette."),
        L("enfant-m", "Dans le sac. Pas dans le sable."),
        L("papa", "Deux gestes, pas un."),
        L("narrateur", "L'anse pose une ombre ronde sur le bois."),
    ],
    (1, 2, 2): [
        L("narrateur", "Aniss a du sable aux lèvres, après le seau."),
        L("enfant-m", "J'ai soif."),
        L("narrateur", "La gourde n'est pas dans le sac."),
        L("papa", "Près des bottes, tout à l'heure. Tiens."),
        L("narrateur", "Aniss ouvre le bouchon au-dessus du seau."),
        L("narrateur", "L'eau file dans le sable mouillé, pas dans sa bouche."),
        L("enfant-m", "Elle s'en va !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste, net, hors de l'eau."),
        L("narrateur", "Aniss refuse de verser une deuxième fois."),
        L("narrateur", "Il glisse la gourde dans le sac, bouchon fermé."),
        L("enfant-m", "Je bois après, sans le seau."),
        L("papa", "Le quai n'a pas bu ta gourde."),
        L("narrateur", "L'anse se tait, un instant."),
    ],
    (1, 2, 3): [
        L("narrateur", "Une odeur de pomme sort du torchon de maman."),
        L("enfant-m", "Le goûter !"),
        L("narrateur", "Le sac n'a pas de pli de linge."),
        L("maman", "Il était dans le panier. Tu le mets où ?"),
        L("narrateur", "Aniss pose le torchon sur le sable, trop vite."),
        L("narrateur", "Le seau penche. Un peu de sable tache la pomme."),
        L("enfant-m", "Oh."),
        L("papa", "Le grain, sur le carreau ?"),
        L("narrateur", "Un grain de lessive brille, hors du tas."),
        L("narrateur", "Aniss refuse de secouer le torchon au-dessus."),
        L("narrateur", "Il le glisse dans le sac, pomme au fond."),
        L("enfant-m", "Le seau reste dehors."),
        L("maman", "La pomme n'est plus un tas."),
        L("narrateur", "Le sac a une bosse ronde, tiède."),
    ],
    (1, 3, 1): [
        L("narrateur", "Le soleil pique. Le doudou a du sable à l'oreille."),
        L("enfant-m", "La casquette, pour nous deux !"),
        L("narrateur", "Elle n'est pas dans le sac."),
        L("papa", "Ma poche. Tu la mets où ?"),
        L("narrateur", "Aniss veut coiffer le doudou, trop vite."),
        L("narrateur", "La visière glisse. Le tissu gris la cache."),
        L("enfant-m", "Elle est sous lui !"),
        L("maman", "Le doudou dans le sac, d'abord ?"),
        L("narrateur", "Aniss refuse de tirer l'oreille."),
        L("narrateur", "Un grain de lessive pique, entre les deux tissus."),
        L("narrateur", "Il glisse le doudou, puis la casquette."),
        L("enfant-m", "Chacun sa place."),
        L("papa", "Toi, la tête. Lui, le fond."),
        L("narrateur", "La visière fait une petite ombre, au bord."),
    ],
    (1, 3, 2): [
        L("narrateur", "Aniss a soif. Le doudou a du sable, lui aussi."),
        L("enfant-m", "De l'eau, pour nous !"),
        L("narrateur", "Pas de gourde dans le sac."),
        L("papa", "Près des bottes. Tiens."),
        L("narrateur", "Aniss ouvre le bouchon près de l'oreille grise."),
        L("narrateur", "Un filet mouille le tissu. Le doudou s'alourdit."),
        L("enfant-m", "Il boit trop !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste sec, lui."),
        L("narrateur", "Aniss refuse de verser une autre gorgée."),
        L("narrateur", "Il glisse la gourde, puis le doudou à côté."),
        L("enfant-m", "Toi au sec. L'eau au bouchon."),
        L("papa", "Deux places, dans le sac."),
        L("narrateur", "L'oreille grise sèche un peu, au soleil."),
    ],
    (1, 3, 3): [
        L("narrateur", "L'odeur de pomme touche l'oreille du doudou."),
        L("enfant-m", "On partage !"),
        L("narrateur", "Le goûter n'est pas dans le sac."),
        L("maman", "Le torchon du panier. Tu le mets où ?"),
        L("narrateur", "Aniss pose la pomme sur le ventre gris, trop vite."),
        L("narrateur", "Le fruit roule. Le doudou ne sait pas tenir."),
        L("enfant-m", "Elle part au sable !"),
        L("papa", "Le grain, sur le torchon ?"),
        L("narrateur", "Un grain de lessive brille, au coin du carreau."),
        L("narrateur", "Aniss refuse de courir après la pomme."),
        L("narrateur", "Il glisse le torchon, puis le doudou, au fond."),
        L("enfant-m", "Ils se parlent, là-dedans."),
        L("maman", "Sans le sable."),
        L("narrateur", "Le sac sent la pomme et le linge, ensemble."),
    ],
    (2, 1, 1): [
        L("narrateur", "Sur la pente, le soleil tape les yeux."),
        L("enfant-m", "Ma casquette !"),
        L("narrateur", "Le sac, au ventre, n'a pas de visière."),
        L("papa", "Le banc de l'entrée. Ma poche."),
        L("narrateur", "Aniss la met, puis veut glisser."),
        L("narrateur", "Le vent de la pente l'arrache, presque."),
        L("enfant-m", "Elle vole !"),
        L("maman", "Le grain, sur la visière ?"),
        L("narrateur", "Un grain de lessive pique, net, au soleil."),
        L("narrateur", "Aniss refuse de glisser avec elle trop lâche."),
        L("narrateur", "Il la glisse dans le sac, sous la sangle."),
        L("enfant-m", "Elle voyage, collée à moi."),
        L("papa", "Pas dans l'herbe, en bas."),
        L("narrateur", "Le plastique tiède attend, sans vent."),
    ],
    (2, 1, 2): [
        L("narrateur", "En bas de la pente, Aniss a la bouche sèche."),
        L("enfant-m", "La gourde !"),
        L("narrateur", "Elle n'est pas dans le sac."),
        L("papa", "Près des bottes. Tiens."),
        L("narrateur", "Aniss boit, le ballon sous le bras, trop d'objets."),
        L("narrateur", "Le bouchon file. L'eau lèche le plastique."),
        L("enfant-m", "Elle glisse, elle aussi !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste, hors de l'eau."),
        L("narrateur", "Aniss refuse de reboire sur la pente."),
        L("narrateur", "Il glisse la gourde dans le sac, bien fermée."),
        L("enfant-m", "Le ballon dehors. L'eau dedans."),
        L("papa", "La pente n'a pas bu."),
        L("narrateur", "Un rond d'eau sèche sur le plastique, puis plus."),
    ],
    (2, 1, 3): [
        L("narrateur", "Une odeur de pomme monte le long de la rampe."),
        L("enfant-m", "Le goûter, en haut !"),
        L("narrateur", "Le sac n'a pas de torchon."),
        L("maman", "Le panier. Je le tends. Tu le mets où ?"),
        L("narrateur", "Aniss pose le torchon sur une marche, trop vite."),
        L("narrateur", "La pente le fait glisser, vers l'herbe."),
        L("enfant-m", "Il part !"),
        L("papa", "Le grain, sur le carreau ?"),
        L("narrateur", "Un grain de lessive brille, à mi-pente."),
        L("narrateur", "Aniss refuse de dévaler après lui."),
        L("narrateur", "Il reprend le torchon, le glisse au fond."),
        L("enfant-m", "Il voyage contre moi, pas sur la pente."),
        L("maman", "La pomme n'a pas glissé, cette fois."),
        L("narrateur", "Le sac a un pli de linge, tiède."),
    ],
    (2, 2, 1): [
        L("narrateur", "Le soleil pique, l'anse du seau à la main."),
        L("enfant-m", "La casquette !"),
        L("narrateur", "Pas dans le sac."),
        L("papa", "Ma poche. Le banc, à la maison."),
        L("narrateur", "Aniss veut coiffer et porter le seau, ensemble."),
        L("narrateur", "L'anse heurte la visière. Ça tombe vers la marche."),
        L("enfant-m", "Non !"),
        L("maman", "Le seau au sol, d'abord ?"),
        L("narrateur", "Aniss refuse de tout tenir d'un coup."),
        L("narrateur", "Un grain de lessive pique la visière, sur le plastique."),
        L("narrateur", "Il pose le seau. Il glisse la casquette."),
        L("enfant-m", "Dans le sac. L'anse dehors."),
        L("papa", "La sangle n'accroche plus."),
        L("narrateur", "La visière fait de l'ombre sur la marche."),
    ],
    (2, 2, 2): [
        L("narrateur", "Aniss a soif, après avoir reculé sur la pente."),
        L("enfant-m", "La gourde, vite."),
        L("narrateur", "Le sac n'a pas de bouchon."),
        L("papa", "Près des bottes. Tiens."),
        L("narrateur", "Aniss verse un peu dans le seau, pour boire plus."),
        L("narrateur", "L'eau tourne, s'échappe entre le plastique et l'anse."),
        L("enfant-m", "Elle file !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste sec, lui."),
        L("narrateur", "Aniss refuse de verser le reste."),
        L("narrateur", "Il glisse la gourde dans le sac, bouchon tourné."),
        L("enfant-m", "Je bois à la gourde, pas au seau."),
        L("papa", "La pente n'a pas eu d'eau."),
        L("narrateur", "L'anse cliquette, puis se tait."),
    ],
    (2, 2, 3): [
        L("narrateur", "Près de l'anse, le torchon sent la pomme."),
        L("enfant-m", "Le goûter !"),
        L("narrateur", "Il n'est pas dans le sac."),
        L("maman", "Le panier. Tu le mets où ?"),
        L("narrateur", "Aniss pose le torchon dans le seau, trop vite."),
        L("narrateur", "L'anse penche. Le pli glisse vers la marche."),
        L("enfant-m", "Il veut la pente !"),
        L("papa", "Le grain, sur le carreau ?"),
        L("narrateur", "Un grain de lessive brille, hors du seau."),
        L("narrateur", "Aniss refuse de le laisser glisser."),
        L("narrateur", "Il glisse le torchon dans le sac, pas dans l'anse."),
        L("enfant-m", "Le seau, pour plus tard. La pomme, au fond."),
        L("maman", "Deux contenants, deux places."),
        L("narrateur", "Le sac a un pli de linge, contre la sangle."),
    ],
    (2, 3, 1): [
        L("narrateur", "Le soleil pique. Le doudou a de l'herbe à l'oreille."),
        L("enfant-m", "La casquette, pour l'ombre !"),
        L("narrateur", "Pas dans le sac."),
        L("papa", "Ma poche. Tu la mets où ?"),
        L("narrateur", "Aniss coiffe le doudou, sur la pente, trop vite."),
        L("narrateur", "La visière et l'oreille glissent ensemble, vers l'herbe."),
        L("enfant-m", "Les deux !"),
        L("maman", "Le grain, sur la visière ?"),
        L("narrateur", "Un grain de lessive pique, au bord du plastique."),
        L("narrateur", "Aniss refuse de dévaler après eux."),
        L("narrateur", "Il glisse le doudou, puis la casquette, au fond."),
        L("enfant-m", "Ils voyagent, collés à moi."),
        L("papa", "Pas sur la pente."),
        L("narrateur", "Un brin d'herbe reste à l'ourlet de la visière."),
    ],
    (2, 3, 2): [
        L("narrateur", "Aniss a soif. L'oreille grise a de l'herbe."),
        L("enfant-m", "De l'eau, après la glisse !"),
        L("narrateur", "Pas de gourde dans le sac."),
        L("papa", "Près des bottes. Tiens."),
        L("narrateur", "Aniss ouvre le bouchon, le doudou sous le bras."),
        L("narrateur", "Un filet mouille l'oreille. Le tissu s'alourdit."),
        L("enfant-m", "Il est lourd !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste sec, net."),
        L("narrateur", "Aniss refuse de verser sur le tissu."),
        L("narrateur", "Il glisse la gourde, puis le doudou à côté, sec."),
        L("enfant-m", "L'eau au bouchon. Lui au fond."),
        L("papa", "La pente n'a pas bu l'oreille."),
        L("narrateur", "L'oreille grise sèche, contre la sangle."),
    ],
    (2, 3, 3): [
        L("narrateur", "L'odeur de pomme touche le plastique tiède."),
        L("enfant-m", "Le goûter, pour le doudou aussi !"),
        L("narrateur", "Le torchon n'est pas dans le sac."),
        L("maman", "Le panier. Tu le mets où ?"),
        L("narrateur", "Aniss pose la pomme sur le doudou, sur une marche."),
        L("narrateur", "Le fruit roule. La pente l'invite."),
        L("enfant-m", "Elle glisse !"),
        L("papa", "Le grain, sur le torchon ?"),
        L("narrateur", "Un grain de lessive brille, à mi-pente."),
        L("narrateur", "Aniss refuse de la rattraper en dévalant."),
        L("narrateur", "Il reprend le fruit, glisse le torchon au fond."),
        L("enfant-m", "Puis l'oreille, à côté."),
        L("maman", "La pomme n'a pas pris la pente."),
        L("narrateur", "Le sac sent la pomme, contre le plastique."),
    ],
    (3, 1, 1): [
        L("narrateur", "Le soleil pique, sous les chaînes."),
        L("enfant-m", "Ma casquette !"),
        L("narrateur", "Le sac, dans l'herbe, n'a pas de visière."),
        L("papa", "Le banc de l'entrée. Ma poche."),
        L("narrateur", "Aniss la met, puis pompe trop fort."),
        L("narrateur", "Le vent du nid l'envoie vers les brins."),
        L("enfant-m", "Dans l'herbe !"),
        L("maman", "Le grain, sur la visière ?"),
        L("narrateur", "Un grain de lessive pique, hors des brins."),
        L("narrateur", "Aniss refuse de plonger dans l'herbe."),
        L("narrateur", "Il glisse la casquette dans le sac, d'abord."),
        L("enfant-m", "Puis je pompe, moins fort."),
        L("papa", "Le nid n'a pas eu la visière."),
        L("narrateur", "Une chaîne se tait, un instant."),
    ],
    (3, 1, 2): [
        L("narrateur", "Aniss a la bouche sèche, après le ballon."),
        L("enfant-m", "La gourde !"),
        L("narrateur", "Pas dans le sac."),
        L("papa", "Près des bottes. Tiens."),
        L("narrateur", "Aniss boit sur le siège, le ballon contre le bois."),
        L("narrateur", "Le bouchon file. L'eau lèche la chaîne."),
        L("enfant-m", "Elle tombe !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste, hors de la chaîne."),
        L("narrateur", "Aniss refuse de reboire en pompant."),
        L("narrateur", "Il glisse la gourde dans le sac, bien fermée."),
        L("enfant-m", "Je bois au sol, après."),
        L("papa", "Le nid n'a pas bu."),
        L("narrateur", "L'eau de la gourde a un petit bruit, sous les chaînes."),
    ],
    (3, 1, 3): [
        L("narrateur", "Le vent apporte une odeur de pomme, sous le nid."),
        L("enfant-m", "Le goûter !"),
        L("narrateur", "Le sac n'a pas de torchon."),
        L("maman", "Le panier. Tu le mets où ?"),
        L("narrateur", "Aniss pose le torchon sur le siège, trop vite."),
        L("narrateur", "Le vent du nid l'envole vers l'herbe."),
        L("enfant-m", "Il vole !"),
        L("papa", "Le grain, sur le carreau ?"),
        L("narrateur", "Un grain de lessive brille, accroché au bois."),
        L("narrateur", "Aniss refuse de courir sous les chaînes."),
        L("narrateur", "Il reprend le torchon, le glisse au fond."),
        L("enfant-m", "Le vent n'a plus le goûter."),
        L("maman", "Le sac l'a, lui."),
        L("narrateur", "Le pli de linge se tait, contre le doudou."),
    ],
    (3, 2, 1): [
        L("narrateur", "Le soleil pique. L'anse du seau est dans l'herbe."),
        L("enfant-m", "La casquette !"),
        L("narrateur", "Pas dans le sac."),
        L("papa", "Ma poche. Le banc."),
        L("narrateur", "Aniss veut coiffer, le seau trop près du siège."),
        L("narrateur", "L'anse accroche. La visière tombe vers le seau."),
        L("enfant-m", "Dedans !"),
        L("maman", "Le grain, sur la visière ?"),
        L("narrateur", "Un grain de lessive pique, au bord de l'anse."),
        L("narrateur", "Aniss refuse de tirer le seau."),
        L("narrateur", "Il écarte l'anse. Il glisse la casquette."),
        L("enfant-m", "Dans le sac. Pas dans le seau."),
        L("papa", "Le nid n'a pas eu la visière."),
        L("narrateur", "Le seau sous le nid a un rond d'ombre."),
    ],
    (3, 2, 2): [
        L("narrateur", "Aniss a soif, après avoir desserré la sangle."),
        L("enfant-m", "La gourde."),
        L("narrateur", "Le sac n'a pas de bouchon."),
        L("papa", "Près des bottes. Tiens."),
        L("narrateur", "Aniss verse dans le seau, sous le siège, pour boire."),
        L("narrateur", "Le siège bouge. L'eau se renverse dans l'herbe."),
        L("enfant-m", "Perdue !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste sec, hors de l'herbe."),
        L("narrateur", "Aniss refuse de verser le reste."),
        L("narrateur", "Il glisse la gourde dans le sac, bouchon fermé."),
        L("enfant-m", "Je bois loin du nid."),
        L("papa", "Le seau reste vide, lui."),
        L("narrateur", "La gourde et le seau s'adossent, sans se mêler."),
    ],
    (3, 2, 3): [
        L("narrateur", "Le torchon sent la pomme, près de l'anse froide."),
        L("enfant-m", "Le goûter, dans le seau !"),
        L("narrateur", "Il n'est pas dans le sac."),
        L("maman", "Le panier. Tu le mets où ?"),
        L("narrateur", "Aniss pose le torchon dans le seau, sous le nid."),
        L("narrateur", "Le siège frôle. Le pli manque de tomber."),
        L("enfant-m", "Ça tape !"),
        L("papa", "Le grain, sur le carreau ?"),
        L("narrateur", "Un grain de lessive brille, hors de l'anse."),
        L("narrateur", "Aniss refuse de laisser le seau sous le bois."),
        L("narrateur", "Il glisse le torchon dans le sac, pomme au fond."),
        L("enfant-m", "Le seau, plus loin. La pomme, avec moi."),
        L("maman", "Le nid n'a pas eu le goûter."),
        L("narrateur", "La pomme sent le linge, dans le sac fermé."),
    ],
    (3, 3, 1): [
        L("narrateur", "Le soleil pique. Le doudou a de la poussière."),
        L("enfant-m", "La casquette, pour l'ombre du nid !"),
        L("narrateur", "Pas dans le sac."),
        L("papa", "Ma poche. Tu la mets où ?"),
        L("narrateur", "Aniss coiffe le doudou sur le siège, trop vite."),
        L("narrateur", "Le vent les penche. La visière quitte le bois."),
        L("enfant-m", "Elle tombe !"),
        L("maman", "Le grain, sur la visière ?"),
        L("narrateur", "Un grain de lessive pique, au pied du nid."),
        L("narrateur", "Aniss refuse de pomper pour la rattraper."),
        L("narrateur", "Il glisse le doudou, puis la casquette, au fond."),
        L("enfant-m", "Plus de vent, là-dedans."),
        L("papa", "Le siège reste vide, lui."),
        L("narrateur", "Le doudou a quitté le siège. Le grain voyage."),
    ],
    (3, 3, 2): [
        L("narrateur", "Aniss a soif. L'oreille grise a de la poussière."),
        L("enfant-m", "De l'eau, sur le nid !"),
        L("narrateur", "Pas de gourde dans le sac."),
        L("papa", "Près des bottes. Tiens."),
        L("narrateur", "Aniss ouvre le bouchon, le doudou sur les genoux."),
        L("narrateur", "Un filet mouille l'oreille. Le siège devient froid."),
        L("enfant-m", "Il est mouillé !"),
        L("maman", "Le grain, au bouchon ?"),
        L("narrateur", "Un grain de lessive reste sec, net."),
        L("narrateur", "Aniss refuse de verser sur le bois."),
        L("narrateur", "Il glisse la gourde, puis le doudou, au fond."),
        L("enfant-m", "Ils se touchent, sans eau."),
        L("papa", "Le nid reste sec."),
        L("narrateur", "Le doudou et la gourde se parlent, grain entre deux."),
    ],
    (3, 3, 3): [
        L("narrateur", "L'odeur de pomme tourne, sous les chaînes."),
        L("enfant-m", "Le goûter, sur le siège, avec lui !"),
        L("narrateur", "Le torchon n'est pas dans le sac."),
        L("maman", "Le panier. Tu le mets où ?"),
        L("narrateur", "Aniss pose la pomme sur le doudou, sur le bois."),
        L("narrateur", "Le vent du nid fait rouler le fruit."),
        L("enfant-m", "Elle part !"),
        L("papa", "Le grain, sur le torchon ?"),
        L("narrateur", "Un grain de lessive brille, accroché au siège."),
        L("narrateur", "Aniss refuse de pomper pour la rattraper."),
        L("narrateur", "Il reprend la pomme, glisse le torchon au fond."),
        L("enfant-m", "Puis l'oreille, à côté."),
        L("maman", "Le vent n'a plus le goûter."),
        L("narrateur", "Le goûter et le doudou partagent le grain, sans vent."),
    ],
}

FIN = {
    (1, 1, 1): [
        L("narrateur", "Ils s'assoient sur le banc du parc."),
        L("narrateur", "Le bois est un peu chaud."),
        L("enfant-m", "Le ballon s'est tu."),
        L("papa", "La visière a voyagé, elle aussi."),
        L("maman", "Le grain de lessive est au fond."),
        L("enfant-m", "J'ai failli la perdre, dans le sable."),
        L("narrateur", "Aniss touche la sangle, plus lourde."),
        L("narrateur", "Un grain de lessive dort sur la visière, au fond."),
    ],
    (1, 1, 2): [
        L("narrateur", "Le quai de bois se tait."),
        L("enfant-m", "J'ai bu, après."),
        L("papa", "Sans mouiller le doudou."),
        L("maman", "Le bouchon a gardé le grain."),
        L("enfant-m", "J'ai failli verser, trop vite."),
        L("narrateur", "Le ballon rouge repose, un peu de sable."),
        L("narrateur", "Aniss ferme la boucle, un clic net."),
        L("narrateur", "Le bouchon blanc porte le grain, contre le ballon."),
    ],
    (1, 1, 3): [
        L("narrateur", "Aniss s'essuie les doigts à l'herbe."),
        L("enfant-m", "La pomme est rentrée."),
        L("maman", "Le torchon aussi."),
        L("papa", "Le grain a dit le carreau."),
        L("enfant-m", "J'ai failli la laisser au sable."),
        L("narrateur", "Le sac sent la pomme, un peu tiède."),
        L("narrateur", "La boucle cliquette, fermée."),
        L("narrateur", "Une miette de pomme colle au grain, dans le torchon."),
    ],
    (1, 2, 1): [
        L("narrateur", "Le seau sonne une dernière fois, puis plus."),
        L("enfant-m", "L'anse est dehors."),
        L("papa", "La casquette, dedans."),
        L("maman", "Deux gestes."),
        L("enfant-m", "J'ai failli tout tenir, d'un coup."),
        L("narrateur", "Aniss pose la main sur la visière, au fond."),
        L("narrateur", "Le quai a de l'ombre, maintenant."),
        L("narrateur", "L'anse du seau ombre la visière, et le grain."),
    ],
    (1, 2, 2): [
        L("narrateur", "Aniss s'assoit, le seau à ses pieds."),
        L("enfant-m", "J'ai bu à la gourde."),
        L("maman", "Pas au seau."),
        L("papa", "Le grain est resté sec."),
        L("enfant-m", "J'ai failli verser le quai."),
        L("narrateur", "L'eau chante un peu, au fond du sac."),
        L("narrateur", "La boucle est fermée."),
        L("narrateur", "Le seau et la gourde se touchent, grain au milieu."),
    ],
    (1, 2, 3): [
        L("narrateur", "Le sac a une bosse ronde, contre la hanche."),
        L("enfant-m", "La pomme n'est plus un tas."),
        L("papa", "Le seau est resté dehors."),
        L("maman", "Le grain a tenu le torchon."),
        L("enfant-m", "J'ai failli la poser sur le sable."),
        L("narrateur", "Aniss respire. Ça sent le linge."),
        L("narrateur", "Le quai de bois est vide, maintenant."),
        L("narrateur", "Le sable n'a pas eu la pomme. Le grain tient."),
    ],
    (1, 3, 1): [
        L("narrateur", "Aniss remet la casquette, après le sac."),
        L("enfant-m", "Chacun sa place."),
        L("papa", "Toi, la tête."),
        L("maman", "Lui, le fond."),
        L("enfant-m", "J'ai failli la cacher sous l'oreille."),
        L("narrateur", "L'ombre de la visière touche le quai."),
        L("narrateur", "Le doudou chauffe un peu, au fond."),
        L("narrateur", "L'oreille grise chauffe la visière. Le grain pique."),
    ],
    (1, 3, 2): [
        L("narrateur", "L'oreille grise sèche, contre la sangle."),
        L("enfant-m", "Toi au sec."),
        L("maman", "L'eau au bouchon."),
        L("papa", "Deux places."),
        L("enfant-m", "J'ai failli le faire boire."),
        L("narrateur", "Aniss pose le sac sur le bois du quai."),
        L("narrateur", "La boucle cliquette, un peu rêche."),
        L("narrateur", "Le doudou sent la lessive, près du bouchon."),
    ],
    (1, 3, 3): [
        L("narrateur", "Le sac sent la pomme et le linge, ensemble."),
        L("enfant-m", "Ils se parlent, là-dedans."),
        L("papa", "Sans le sable."),
        L("maman", "Le grain a dit le carreau."),
        L("enfant-m", "J'ai failli la laisser rouler."),
        L("narrateur", "Aniss s'assoit. Le quai est frais."),
        L("narrateur", "Une bosse ronde pousse le ventre gris."),
        L("narrateur", "Au fond, le torchon garde le grain qui brille."),
    ],
    (2, 1, 1): [
        L("narrateur", "Ils quittent la pente, la sangle au ventre."),
        L("enfant-m", "Elle n'a pas volé."),
        L("papa", "Collée à toi, dans le sac."),
        L("maman", "Le grain a piqué, au soleil."),
        L("enfant-m", "J'ai failli glisser avec elle trop lâche."),
        L("narrateur", "Aniss touche la visière, au fond, tiède."),
        L("narrateur", "Le plastique derrière eux se tait."),
        L("narrateur", "La pente a laissé un rond chaud sur la visière."),
    ],
    (2, 1, 2): [
        L("narrateur", "Au pied du toboggan, Aniss s'assoit."),
        L("enfant-m", "Le ballon dehors. L'eau dedans."),
        L("maman", "La pente n'a pas bu."),
        L("papa", "Le grain est resté hors de l'eau."),
        L("enfant-m", "J'ai failli tout tenir, d'un coup."),
        L("narrateur", "Un rond d'eau a séché sur le plastique."),
        L("narrateur", "La boucle cliquette, fermée."),
        L("narrateur", "L'eau chante dans la gourde, au pied du plastique."),
    ],
    (2, 1, 3): [
        L("narrateur", "Aniss porte le sac, le pli de linge au fond."),
        L("enfant-m", "La pomme n'a pas glissé."),
        L("papa", "Tu as repris le torchon, à mi-pente."),
        L("maman", "Le grain a brillé, sur le carreau."),
        L("enfant-m", "J'ai failli la laisser dévaler."),
        L("narrateur", "Ça sent la pomme, contre lui."),
        L("narrateur", "La rampe reste vide, tiède."),
        L("narrateur", "Une odeur de pomme monte le long de la rampe."),
    ],
    (2, 2, 1): [
        L("narrateur", "Le seau reste au sol, l'anse froide."),
        L("enfant-m", "La casquette, dans le sac."),
        L("papa", "La sangle n'accroche plus."),
        L("maman", "Le grain a piqué, sur le plastique."),
        L("enfant-m", "J'ai failli tout porter, ensemble."),
        L("narrateur", "Aniss remet la visière, après."),
        L("narrateur", "L'ombre touche une marche, puis plus."),
        L("narrateur", "La sangle verte a un grain, près de l'anse."),
    ],
    (2, 2, 2): [
        L("narrateur", "Aniss boit loin de la pente, bouchon tourné."),
        L("enfant-m", "Pas au seau."),
        L("maman", "Le grain est resté sec."),
        L("papa", "La pente n'a pas eu d'eau."),
        L("enfant-m", "J'ai failli verser, pour aller plus vite."),
        L("narrateur", "L'anse cliquette une fois, puis se tait."),
        L("narrateur", "Contre la hanche, le sac pèse."),
        L("narrateur", "Au bouchon, le seau droit garde la gourde et le grain."),
    ],
    (2, 2, 3): [
        L("narrateur", "Le sac a un pli de linge, contre la sangle."),
        L("enfant-m", "Le seau, pour plus tard."),
        L("papa", "La pomme, au fond."),
        L("maman", "Deux places."),
        L("enfant-m", "J'ai failli la mettre dans l'anse."),
        L("narrateur", "Aniss respire. Ça sent le linge chaud."),
        L("narrateur", "La pente est vide, derrière."),
        L("narrateur", "Le goûter n'a pas glissé. Le grain tient le pli."),
    ],
    (2, 3, 1): [
        L("narrateur", "Un brin d'herbe reste à l'ourlet de la visière."),
        L("enfant-m", "Ils voyagent, collés à moi."),
        L("papa", "Pas sur la pente."),
        L("maman", "Le grain a piqué, au bord."),
        L("enfant-m", "J'ai failli les perdre, tous les deux."),
        L("narrateur", "Aniss ferme la boucle, contre le plastique."),
        L("narrateur", "La rampe se tait."),
        L("narrateur", "Le doudou n'est plus sur la pente. Le grain est à la visière."),
    ],
    (2, 3, 2): [
        L("narrateur", "L'oreille grise sèche, contre la sangle."),
        L("enfant-m", "L'eau au bouchon. Lui au fond."),
        L("maman", "La pente n'a pas bu l'oreille."),
        L("papa", "Le grain est resté sec."),
        L("enfant-m", "J'ai failli le mouiller, sous le bras."),
        L("narrateur", "Aniss pose le sac, plus lourd."),
        L("narrateur", "Le toboggan brille, sans eux."),
        L("narrateur", "L'oreille et le bouchon se parlent, grain entre eux."),
    ],
    (2, 3, 3): [
        L("narrateur", "Le sac sent la pomme, contre le plastique."),
        L("enfant-m", "Elle n'a pas pris la pente."),
        L("papa", "Tu as repris le fruit, sans dévaler."),
        L("maman", "Le grain a brillé, à mi-pente."),
        L("enfant-m", "J'ai failli la voir filer."),
        L("narrateur", "L'oreille grise fait une bosse, à côté."),
        L("narrateur", "Aniss sourit, un peu, sans courir."),
        L("narrateur", "Au pli du torchon, le grain s'endort sur le doudou."),
    ],
    (3, 1, 1): [
        L("narrateur", "Une chaîne se tait, près du nid."),
        L("enfant-m", "J'ai pompé moins fort."),
        L("papa", "Le nid n'a pas eu la visière."),
        L("maman", "Le grain a piqué, hors des brins."),
        L("enfant-m", "J'ai failli la jeter dans l'herbe."),
        L("narrateur", "Aniss touche le sac, sur ses genoux."),
        L("narrateur", "Le bois du siège est vide, lisse."),
        L("narrateur", "Une chaîne se tait. Le grain reste sur la visière."),
    ],
    (3, 1, 2): [
        L("narrateur", "Aniss boit au sol, loin du siège."),
        L("enfant-m", "Le nid n'a pas bu."),
        L("maman", "Le bouchon est fermé, maintenant."),
        L("papa", "Le grain est resté hors de la chaîne."),
        L("enfant-m", "J'ai failli boire en pompant."),
        L("narrateur", "Le ballon a cessé de rouler, dans l'herbe."),
        L("narrateur", "La sangle pèse, juste."),
        L("narrateur", "L'eau de la gourde a un petit bruit, sous les chaînes."),
    ],
    (3, 1, 3): [
        L("narrateur", "Le pli de linge se tait, contre le doudou."),
        L("enfant-m", "Le vent n'a plus le goûter."),
        L("papa", "Le sac l'a, lui."),
        L("maman", "Le grain a brillé, accroché au bois."),
        L("enfant-m", "J'ai failli le voir voler."),
        L("narrateur", "Aniss pose le sac dans l'herbe sèche, près de lui."),
        L("narrateur", "Le nid craque, vide."),
        L("narrateur", "Le vent n'a pas le goûter. Le grain le tient."),
    ],
    (3, 2, 1): [
        L("narrateur", "Le seau sous le nid a un rond d'ombre."),
        L("enfant-m", "Pas dans le seau. Dans le sac."),
        L("papa", "Tu as écarté l'anse."),
        L("maman", "Le grain a piqué, au bord."),
        L("enfant-m", "J'ai failli la laisser tomber dedans."),
        L("narrateur", "Aniss remet la casquette, après."),
        L("narrateur", "Les chaînes bougent, un peu, sans lui."),
        L("narrateur", "Le seau sous le nid a un grain, près de la casquette."),
    ],
    (3, 2, 2): [
        L("narrateur", "Aniss boit loin du nid, bouchon fermé."),
        L("enfant-m", "Le seau est vide, lui."),
        L("maman", "Le grain est resté sec."),
        L("papa", "Tu n'as pas versé le reste."),
        L("enfant-m", "J'ai failli tout perdre, sous le siège."),
        L("narrateur", "L'herbe a un peu d'eau, puis plus."),
        L("narrateur", "Le sac pèse, contre la hanche."),
        L("narrateur", "La gourde et le seau s'adossent. Le grain est au milieu."),
    ],
    (3, 2, 3): [
        L("narrateur", "La pomme sent le linge, dans le sac fermé."),
        L("enfant-m", "Le seau, plus loin."),
        L("papa", "La pomme, avec toi."),
        L("maman", "Le nid n'a pas eu le goûter."),
        L("enfant-m", "J'ai failli la laisser sous le bois."),
        L("narrateur", "Aniss s'assoit dans l'herbe, le sac contre lui."),
        L("narrateur", "L'anse froide reste seule."),
        L("narrateur", "La pomme sent le linge, dans le sac fermé, au nid."),
    ],
    (3, 3, 1): [
        L("narrateur", "Le siège de bois est vide, lisse."),
        L("enfant-m", "Plus de vent, là-dedans."),
        L("papa", "Le doudou a quitté le siège."),
        L("maman", "Le grain voyage, à la visière."),
        L("enfant-m", "J'ai failli pomper pour la rattraper."),
        L("narrateur", "Aniss pose le sac sur ses genoux, lourd."),
        L("narrateur", "Une chaîne fait un petit bruit, puis plus."),
        L("narrateur", "Le doudou a quitté le siège. Le grain voyage à la visière."),
    ],
    (3, 3, 2): [
        L("narrateur", "Le nid reste sec, sous les chaînes."),
        L("enfant-m", "Ils se touchent, sans eau."),
        L("maman", "Le grain est resté sec, lui."),
        L("papa", "Tu n'as pas versé sur le bois."),
        L("enfant-m", "J'ai failli mouiller l'oreille, sur le nid."),
        L("narrateur", "Aniss ferme la boucle, un clic bas."),
        L("narrateur", "Le siège de bois se tait."),
        L("narrateur", "Le doudou et la gourde se parlent, grain entre deux."),
    ],
    (3, 3, 3): [
        L("narrateur", "Le vent du nid n'a plus de pomme."),
        L("enfant-m", "Elle est au fond, avec lui."),
        L("papa", "Tu as repris le fruit, sans pomper."),
        L("maman", "Le grain a brillé, accroché au siège."),
        L("enfant-m", "J'ai failli la voir rouler."),
        L("narrateur", "Aniss serre la sangle, un peu, sans forcer."),
        L("narrateur", "Le bois du nid est nu, froid."),
        L("narrateur", "Le goûter et le doudou partagent le grain, sans vent."),
    ],
}

Q_FIELDS = {
    "expected_answer": "sac",
    "accepted_examples": (
        "sac | le sac | dans le sac | il met | mettre | le doudou | "
        "les affaires | au fond"
    ),
    "retry_prompt": "Il les met dans le sac. Où les met Aniss ?",
    "engine_ok_text": "Oui, dans le sac.",
    "engine_near_text": "Tu es tout près. Le doudou glisse dans le sac.",
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
        return "linge"
    if kind in {"transition_question", "passage_question"}:
        return ""
    if cid.endswith("_C0001"):
        return "enfants_parc"
    if kind == "passage_fin":
        return {1: "linge,banc", 2: "linge,toboggan", 3: "linge,balancoire"}.get(i or 3, "linge")
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
        extra["emphasis"] = "grain de lessive"
    elif prof == "clue":
        extra["emphasis"] = "sac"
    elif prof == "confirm":
        extra["emphasis"] = "sac"
    elif prof == "action":
        if "ballon" in low:
            extra["emphasis"] = "ballon"
        elif "seau" in low:
            extra["emphasis"] = "seau"
        elif "doudou" in low:
            extra["emphasis"] = "doudou"
    elif prof == "resolution":
        extra["emphasis"] = "grain de lessive" if "grain" in low else "sac"
    elif prof == "ending":
        extra["emphasis"] = "grain de lessive" if "grain" in low else "sac"
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
                "option_1_label": "la casquette",
                "option_2_label": "la gourde",
                "option_3_label": "le goûter",
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
        "La boucle jaune du sac vert cliquette toute seule : une chaussette "
        "du panier a heurté le banc. Un grain de lessive, blanc, rêche, reste "
        "collé au métal. Aniss veut le parc, maintenant. Il tire trop vite : "
        "le sac est vide, trop léger, la boucle résiste. Le doudou est sous "
        "le linge. Il le glisse dans le sac. Le sac part AVEC lui. Au quai "
        "du bac, à la pente tiède ou au nid des chaînes, le sac glisse. "
        "Ballon, seau ou doudou : l'objet résiste, disparaît ou révèle le "
        "grain. Aniss refuse de foncer. Casquette, gourde ou goûter manquent : "
        "il faillit les user hors du sac. Le grain du début se paie. Retour, "
        "le sac est plus lourd, le grain a voyagé."
    )
    out["title"] = "Le sac vert d'Aniss sur le banc"
    out["characters"] = "Aniss, papa, maman"
    out["setting"] = "entrée, banc, panier à linge, puis parc"
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
        "# TREE-AUT-031 — Le sac vert d'Aniss sur le banc\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "- **Titre noyau :** *Le sac vert d'Aniss sur le banc*\n"
        "- **Public :** N2 (≤ 15 mots/phrase)\n"
        "- **Leçon :** AUT.AFF.001 — mettre dans le sac, vécue "
        "(glisser le doudou, puis casquette / gourde / goûter), jamais dite\n"
        "- **Personnages :** Aniss, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "La boucle jaune cliquette toute seule : une chaussette du panier a "
        "heurté le sac vert, sur le banc de l'entrée. Un grain de lessive, "
        "blanc, rêche, reste collé au métal. Aniss veut le parc, maintenant. "
        "Il tire trop vite : le sac est vide, trop léger, la boucle résiste. "
        "Le sourire disparaît. Papa s'accroupit. Le doudou est sous le linge ; "
        "le grain brille sur l'oreille. Aniss le glisse dans le sac. Merci. "
        "Le sac part AVEC lui. Au quai du bac, à la pente tiède ou au nid des "
        "chaînes, le sac glisse, s'ouvre, trop léger. Ballon, seau ou doudou "
        "changent la seconde ruse : l'objet résiste, disparaît ou révèle le "
        "grain. Aniss refuse de foncer. Casquette, gourde ou goûter manquent : "
        "il faillit les user hors du sac. Le grain du début se paie. Retour : "
        "le sac est plus lourd, le grain a voyagé.\n\n"
        "## Vécu\n\n"
        "Entrée, panier tiède, banc de bois, boucle jaune, grain de lessive. "
        "Impatience (le parc, vite), découragement (épaules, menton, sac trop "
        "léger), fierté calme (il glisse, sans foncer). Merci vécu après le "
        "doudou dans le sac. Question : où Aniss met le doudou / les affaires. "
        "T1 bac / toboggan / balançoires (coins : quai, pente, nid). T2 ballon "
        "/ seau / doudou. T3 casquette / gourde / goûter.\n\n"
        "## Vu et corrigé\n\n"
        "P2 F-NAR-019 example4 v2. Ouverture inventée (boucle qui cliquette "
        "toute seule), pas les cinq manières listées, pas « encore » du dump. "
        "Indice unique : grain de lessive, payé au climax. Corps : sourire "
        "disparaît, envie et inquiétude, adulte à la même hauteur. 2e ruse "
        "plus rusée (sac chassé, doudou sous le tas, ballon sous la rampe, "
        "sangle coincée, doudou disparu dans l'herbe, visière au vent). "
        "Dénouement qui a failli (casquette / gourde / goûter hors du sac). "
        "Monde ≠ TREE-AUT-046 (sac jaune, laitue), ≠ TREE-AUT-009 (sac bleu, "
        "salon), ≠ TREE-AUT-015 (Nina, buée), ≠ TREE-COL-023 (banc, pomme). "
        "Pas gabarit example3. Tics « encore / déjà / tout doux / tout calme » "
        "retirés. Troupe D16 Aniss. 1er choix = lieux, n'enlève pas le sac. "
        "27 fins, 27 dernières images. TTS par chunk : `notes`, `text_ssml`, "
        "`text_xai_tags`, piper 1.10–1.30. `slow` = choix, indice, fins. "
        "`check()` N2 OK. Pas apply.\n\n"
        "## Direction vocale\n\n"
        "Chaque segment a un arc dans `notes`. Débit, hauteur, volume et pause "
        "suivent la fonction : installation, choix, indice, obstacle, action, "
        "résolution, retour. Action plus vive. Choix, indice et fins plus lents.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks\n"
        "- 27 chemins, 596 à 638 mots, moyenne 618\n"
        "- 27 fins distinctes, 27 L3 distincts, 27 dernières images\n"
        "- `text` = `script` collé\n"
        "- 0 occurrence de « encore », « déjà », « tout doux », « tout calme »\n"
        "- 0 « on va apprendre », « mission accomplie », « aujourd'hui »\n"
        "- papa/maman parlent, une question, un merci vécu, `en ce moment`\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
