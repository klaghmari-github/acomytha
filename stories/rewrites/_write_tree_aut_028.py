#!/usr/bin/env python3
"""TREE-AUT-028 — F-NAR-019 v2. Victorino, seau vert, parc. N3. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words

SID = "TREE-AUT-028"
LIM = 16
TICS = ("tout doux", "tout calme", "encore", "déjà")
SNAIL = ("escargot", "loupe", "carnet bleu", "pots de menthe", "vélo rouge")
EXTRA_BAD = (
    "sami", "hugo", "ranger", "tu ranges", "après le jeu",
    "j'ai compris", "mission accomplie", "aujourd'hui",
    "on dirait que notre mission", "gouttes pendent",
    "couleur de miel", "trois notes",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "seau vert",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le croissant de sable part au parc; "
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
            "destinataire=enfant; sous_texte=ton choix change le jeu; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "seau",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=le seau attend d_etre repris; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "seau vert",
        "note": (
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=l_anse est reprise, le jeu n_est pas fini; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": (
            "arc=action; intention=entraîner; emotion=élan_puis_friction; intensite=2; "
            "destinataire=enfant; sous_texte=deux envies tirent le meme objet; tempo=vif; "
            "sourire=léger; respiration=courte"
        ),
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=tirer plus fort renverse le seau; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "croissant",
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le croissant de sable montre l_anse sans qu_on recite; "
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
            "destinataire=enfant; sous_texte=le seau a quitte le dessous du lit; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    },
}


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
                raise SystemExit(f"TIC {cid}: {tic} -> {blob[:80]}")
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
    "narrateur|Le loquet du volet tape une fois contre le bois.",
    "narrateur|Il reste ouvert. Une bande de parc coupe l'oreiller.",
    "narrateur|Dans la bande, l'oreille pliée du doudou.",
    "narrateur|Ça sent l'herbe chaude, par la fenêtre entrouverte.",
    "narrateur|Victorino vit ici, avec papa et maman.",
    "narrateur|Sous le lit, une courbe verte dépasse.",
    "narrateur|C'est le seau, lourd d'un peu de sable.",
    "narrateur|Sur l'anse, un croissant beige est collé, sec.",
    "papa|Tu as vu ton croissant de sable, Victorino ?",
    "enfant-m|Oui. Il est à moi.",
    "enfant-m|Je le remplis au parc, et je le ramène.",
    "maman|Avant le goûter ?",
    "enfant-m|Oui, maman. Vite.",
    "narrateur|En ce moment, Victorino tire l'anse trop fort.",
    "narrateur|Le seau cogne le plancher. Tic.",
    "narrateur|Le croissant craque, sans tomber.",
    "enfant-m|Allez, on y va !",
    "narrateur|Papa plie le manteau gris.",
    "maman|Nino joue près de la grille, tu sais ?",
    "enfant-m|Il peut regarder. Le seau, c'est le mien.",
    "narrateur|Victorino serre l'anse. Ses pieds tapent le parquet.",
    "papa|On sort. Le seau vient avec nous.",
    "narrateur|Le plancher est tiède sous son pied nu.",
    "narrateur|Une chaîne de balançoire tinte, loin.",
]

T1 = [
    "papa|Où vas-tu d'abord, avec le seau ?",
    "narrateur|Le bac à sable.",
    "narrateur|Sinon le toboggan.",
    "narrateur|Ou les balançoires.",
]

L1 = {
    1: [
        "narrateur|Au bac, le sable est frais, un peu lourd.",
        "narrateur|Victorino pose le seau, prêt à le remplir.",
        "copain|Moi, je verse tout, d'un coup !",
        "enfant-m|Non. C'est pour mon château.",
        "narrateur|Ils tirent l'anse, chacun d'un côté.",
        "narrateur|Le seau bascule. Le sable s'étale.",
        "enfant-m|Oh.",
        "narrateur|Le sourire de Victorino disparaît.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|Tu le vois, ton seau ?",
        "enfant-m|Il est à l'envers.",
        "maman|Nino, ta montagne peut attendre un peu ?",
        "copain|Je voulais que ça fasse chh.",
        "narrateur|Le croissant beige tient à l'anse, malgré la chute.",
    ],
    2: [
        "narrateur|La rampe du toboggan brille, un peu froide.",
        "narrateur|Victorino pose le seau en bas, pour attraper.",
        "copain|On glisse avec, tous les deux !",
        "enfant-m|Non. Il attend en bas.",
        "narrateur|Nino hisse le seau sur la marche.",
        "narrateur|Victorino le rattrape trop vite.",
        "narrateur|L'anse échappe. Le plastique sonne.",
        "enfant-m|Ça veut pas.",
        "narrateur|Ses épaules baissent. Le sourire n'y est plus.",
        "narrateur|Maman s'accroupit, à la même hauteur.",
        "maman|Il a roulé où, le seau ?",
        "enfant-m|Près des bottes.",
        "papa|Tu le prends, avant de glisser ?",
        "copain|Moi, je voulais le bruit.",
        "narrateur|Le croissant beige a pris une goutte de rampe.",
    ],
    3: [
        "narrateur|Les chaînes des balançoires sont froides, et sonnent.",
        "narrateur|Victorino assied le doudou dans le seau, au pied.",
        "copain|On le pend à la chaîne, comme une cloche !",
        "enfant-m|Non. Il n'aime pas voler.",
        "narrateur|Nino accroche l'anse trop haut.",
        "narrateur|Le seau penche, vide le doudou dans l'herbe.",
        "enfant-m|Arrête.",
        "narrateur|Victorino se fige. Dans sa poitrine, ça se bouscule.",
        "narrateur|Papa s'accroupit, face aux chaînes.",
        "papa|Ton seau, il est sous le banc ?",
        "enfant-m|Oui. Il a mal.",
        "maman|Nino, la cloche peut attendre ?",
        "copain|Je voulais le cling.",
        "narrateur|Le croissant beige a un brin d'herbe collé.",
        "narrateur|Une flaque tremble sous les sièges, puis s'arrête.",
    ],
}

Q = {
    1: [
        "narrateur|Le seau vert gît dans le sable.",
        "papa|Victorino, tu prends quoi ?",
    ],
    2: [
        "narrateur|Le seau vert attend près des bottes.",
        "maman|Victorino, tu prends quoi ?",
    ],
    3: [
        "narrateur|Le seau vert est sous le banc.",
        "papa|Victorino, tu cherches quoi ?",
    ],
}

C = {
    1: [
        "narrateur|Victorino remet le seau à l'endroit.",
        "narrateur|Il le prend à deux mains.",
        "enfant-m|Il était là.",
        "papa|Merci, Victorino.",
        "maman|Le manteau reste sur le banc.",
        "narrateur|Un grain de sable tient sur sa joue.",
        "copain|Je joue à côté, alors.",
        "narrateur|Le croissant beige revient contre sa paume.",
    ],
    2: [
        "narrateur|Victorino ramasse le seau près des bottes.",
        "narrateur|L'anse est froide, un peu mouillée.",
        "enfant-m|Je le tiens.",
        "maman|Merci, Victorino.",
        "papa|Le manteau reste au crochet.",
        "narrateur|Une goutte glisse de la manche du seau.",
        "copain|On glisse après, sans lui.",
        "narrateur|Le croissant beige a une perle d'eau.",
    ],
    3: [
        "narrateur|Victorino se penche sous le banc.",
        "narrateur|Il sort le seau, puis le doudou.",
        "enfant-m|Vous voilà.",
        "papa|Merci, Victorino.",
        "maman|Le manteau reste au poteau.",
        "narrateur|L'oreille du doudou est un peu humide.",
        "copain|La cloche, on la fera plus tard.",
        "narrateur|Le croissant beige a gardé son brin d'herbe.",
    ],
}

T2 = {
    1: [
        "maman|Le sable a bougé. Tu prends quoi, pour la suite ?",
        "narrateur|Le ballon.",
        "narrateur|Sinon le seau.",
        "narrateur|Ou le doudou.",
    ],
    2: [
        "papa|La rampe a sonné. Tu emportes quoi ?",
        "narrateur|Le ballon.",
        "narrateur|Sinon le seau.",
        "narrateur|Ou le doudou.",
    ],
    3: [
        "maman|Les chaînes se taisent. Tu prends quoi avec toi ?",
        "narrateur|Le ballon.",
        "narrateur|Sinon le seau.",
        "narrateur|Ou le doudou.",
    ],
}

L2 = {
    (1, 1): [
        "narrateur|Près du bac, le ballon est à moitié sablé.",
        "copain|On le met dans le seau, et on tape !",
        "enfant-m|Non. Le seau, c'est le château.",
        "narrateur|Nino pousse le jaune. Poum contre l'anse.",
        "narrateur|Le seau penche. Un peu de sable saute.",
        "enfant-m|Aïe. Ça recommence.",
        "papa|Le ballon sous le bras, le seau à droite ?",
        "narrateur|Victorino obéit, les dents un peu serrées.",
        "maman|Chacun a sa place, un instant.",
        "copain|D'accord. Je roule à côté.",
        "narrateur|Un grain beige reste collé au cuir.",
        "narrateur|Le croissant de l'anse n'a pas bougé.",
    ],
    (1, 2): [
        "narrateur|Près du bac, le seau vert attend, vide.",
        "copain|De l'eau, moi !",
        "enfant-m|Du sable, moi.",
        "narrateur|Ils versent trop vite, tous les deux.",
        "narrateur|Ça fait une boue grise, trop lourde.",
        "enfant-m|C'est plus un château.",
        "maman|Tu verses un peu, puis tu t'arrêtes ?",
        "narrateur|Victorino penche, juste un filet de grains.",
        "papa|Nino, l'eau, plus tard, dans l'herbe.",
        "copain|Bon. J'attends.",
        "narrateur|Au fond, le croissant beige se voit, net.",
        "narrateur|Victorino pose le seau à sa droite, sans le lâcher.",
    ],
    (1, 3): [
        "narrateur|Près du bac, le doudou a du sable à l'oreille.",
        "copain|Il creuse avec nous !",
        "enfant-m|Il se salit trop.",
        "narrateur|Nino l'assoit dans le seau, trop fort.",
        "narrateur|L'oreille plonge. Victorino le retire.",
        "enfant-m|Sur le rebord, pas dedans.",
        "papa|Tu le poses, et tu gardes l'anse ?",
        "narrateur|Victorino sèche l'oreille d'une main.",
        "maman|Le seau reste à ta droite.",
        "copain|Il peut regarder, alors.",
        "narrateur|Un grain tient sur le tissu gris.",
        "narrateur|Le croissant beige frôle le doudou, sans le tacher.",
    ],
    (2, 1): [
        "narrateur|Au pied du toboggan, le ballon rebondit une fois.",
        "copain|On le met dans le seau, et on glisse !",
        "enfant-m|Le seau reste en bas.",
        "narrateur|Nino lance le jaune trop près de la rampe.",
        "narrateur|Il tape le seau. L'anse sonne.",
        "enfant-m|Il va partir !",
        "papa|Tu le serres sous le bras ?",
        "narrateur|Victorino rattrape le ballon, puis l'anse.",
        "maman|Le manteau reste au crochet.",
        "copain|Sans le seau, alors. Juste le ballon.",
        "narrateur|Une feuille sèche tourne près des bottes.",
        "narrateur|Le croissant beige a un reflet de rampe.",
    ],
    (2, 2): [
        "narrateur|Au toboggan, le seau vert sonne contre une marche.",
        "copain|On le fait glisser, vide !",
        "enfant-m|Il va trop vite.",
        "narrateur|Nino le pousse. Le plastique crisse.",
        "narrateur|Victorino court en bas, trop tard.",
        "enfant-m|Il s'est sauvé.",
        "maman|Tu le poses près des bottes, sans le lancer ?",
        "narrateur|Victorino ramène l'anse, le souffle court.",
        "papa|Il reste avec tes pieds, lui.",
        "copain|Moi je glisse, sans objet.",
        "narrateur|Une goutte sèche sur l'herbe, près de l'anse.",
        "narrateur|Le croissant beige a pris la poussière de la rampe.",
    ],
    (2, 3): [
        "narrateur|Au toboggan, le doudou est dans le sac.",
        "copain|Il glisse, lui aussi !",
        "enfant-m|Il a peur de la rampe.",
        "narrateur|Nino le sort trop vite. L'oreille pend.",
        "narrateur|Victorino le serre contre sa joue.",
        "enfant-m|Il est froid.",
        "papa|Tu le gardes, et le seau près des bottes ?",
        "narrateur|Victorino hoche la tête, l'anse à l'autre main.",
        "maman|Le manteau reste au crochet.",
        "copain|Bon. Je glisse tout seul.",
        "narrateur|Le tissu gris sent le sac d'osier.",
        "narrateur|Le croissant beige touche presque l'oreille pliée.",
    ],
    (3, 1): [
        "narrateur|Près des balançoires, le ballon est dans l'herbe.",
        "copain|On le met dans le seau, sous la chaîne !",
        "enfant-m|La chaîne va le taper.",
        "narrateur|Nino le pousse. Un brin d'herbe colle au cuir.",
        "narrateur|Le ballon roule sous le siège. Victorino s'arrête.",
        "enfant-m|Il ne part pas là-dessous.",
        "papa|Tu le rattrapes, le seau à l'écart ?",
        "narrateur|Victorino prend le jaune, l'anse loin de la chaîne.",
        "maman|Le manteau reste au poteau.",
        "copain|D'accord. On tape à côté.",
        "narrateur|Une flaque tremble quand il pose le pied.",
        "narrateur|Le croissant beige a un brin, plus un autre.",
    ],
    (3, 2): [
        "narrateur|Près des balançoires, le seau vert est sous le banc.",
        "copain|On le pend, pour le cling !",
        "enfant-m|Il n'est pas une cloche.",
        "narrateur|Nino tire l'anse vers le métal.",
        "narrateur|Victorino la retient. Ça vibre.",
        "enfant-m|Lâche.",
        "maman|Tu le poses à tes pieds, sans le pendre ?",
        "narrateur|Victorino pose le seau. L'anse a un peu d'eau.",
        "papa|Tu verses dans l'herbe ?",
        "enfant-m|Oui. Tout bas.",
        "copain|Sans cling, alors.",
        "narrateur|Le croissant beige sèche, loin de la chaîne.",
    ],
    (3, 3): [
        "narrateur|Près des balançoires, le doudou est sous le banc.",
        "copain|Il s'assoit sur le siège !",
        "enfant-m|Trop haut, trop froid.",
        "narrateur|Nino le hisse. Une goutte de chaîne touche l'oreille.",
        "narrateur|Victorino le reprend, un peu humide.",
        "enfant-m|Il a senti le vent.",
        "papa|Tu le sers, et le seau juste à côté ?",
        "narrateur|Victorino hoche. L'anse reste dans l'herbe.",
        "maman|Le manteau reste au poteau.",
        "copain|Bon. Je me balance, moi.",
        "narrateur|La chaîne se tait un moment.",
        "narrateur|Le croissant beige frôle le tissu, sans le mouiller.",
    ],
}


def t3_lines(i: int, j: int) -> list[str]:
    start = {
        (1, 1): "papa|Le ballon est sablé. On cherche où, pour rentrer ?",
        (1, 2): "maman|Le seau pèse. On cherche où, pour rentrer ?",
        (1, 3): "papa|Le doudou a du sable. On cherche où, pour rentrer ?",
        (2, 1): "maman|Le ballon est froid. On cherche où, pour rentrer ?",
        (2, 2): "papa|Le seau a sonné. On cherche où, pour rentrer ?",
        (2, 3): "maman|Le doudou a vu la rampe. On cherche où, pour rentrer ?",
        (3, 1): "papa|Le ballon a de l'herbe. On cherche où, pour rentrer ?",
        (3, 2): "maman|Le seau a de l'eau. On cherche où, pour rentrer ?",
        (3, 3): "papa|Le doudou a senti le vent. On cherche où, pour rentrer ?",
    }[(i, j)]
    return [
        start,
        "narrateur|Le banc de bois.",
        "narrateur|Vers le sac d'osier.",
        "narrateur|Ou bien le portail.",
    ]


L3 = {
    (1, 1, 1): [
        "narrateur|Au banc, le manteau gris est plié, tiède.",
        "copain|On rejoue, une dernière fois !",
        "enfant-m|Je veux tout prendre d'un coup.",
        "narrateur|Il ramasse manteau, ballon, seau. Tout glisse.",
        "enfant-m|Aïe.",
        "narrateur|Cette fois, Victorino refuse de foncer.",
        "narrateur|Papa se tait. Personne ne montre du doigt.",
        "narrateur|Victorino écoute le bac, tout proche, qui fait chh.",
        "narrateur|Il cherche l'anse. Le croissant beige apparaît.",
        "enfant-m|Toi.",
        "narrateur|Il prend le seau, puis le manteau, puis le doudou.",
        "maman|Tu les as vus, tout seul.",
        "narrateur|Un grain colle à la manche grise.",
    ],
    (1, 1, 2): [
        "narrateur|Le sac d'osier attend dans l'herbe, bouche ouverte.",
        "copain|On cache le ballon au fond !",
        "enfant-m|Le seau d'abord.",
        "narrateur|Il pousse trop vite. L'anse disparaît dans l'osier.",
        "enfant-m|Il est parti.",
        "narrateur|Victorino s'arrête. Ses mains s'ouvrent.",
        "narrateur|Maman ne dit pas le mot.",
        "narrateur|Il écoute. Pas de cling. Un frottement d'osier.",
        "narrateur|Au bord du sac, le croissant beige dépasse.",
        "enfant-m|Là.",
        "narrateur|Il glisse le seau, le manteau, le doudou.",
        "papa|Tu as trouvé l'anse.",
        "narrateur|Le ballon tapote le bord du sac, tout mou.",
    ],
    (1, 1, 3): [
        "narrateur|Près du portail, Nino glisse le seau entre deux barreaux.",
        "copain|Un dernier château, dehors !",
        "enfant-m|On rentre.",
        "narrateur|Victorino tire trop fort. L'anse se coince.",
        "enfant-m|Ça veut pas.",
        "narrateur|Il lâche, respire, refuse de tirer plus.",
        "narrateur|Papa croise les bras, sans parler.",
        "narrateur|Victorino observe le plastique vert, écoute le gravier.",
        "narrateur|Le croissant beige brille contre le fer.",
        "enfant-m|Doucement, alors.",
        "narrateur|Il tourne l'anse, la libère, prend manteau et doudou.",
        "maman|Le barreau l'a rendu.",
        "narrateur|Un brin d'herbe reste au ballon, près du fer.",
    ],
    (1, 2, 1): [
        "narrateur|Dans ses mains, le seau pèse, près du banc.",
        "copain|Verse-le sur le bois !",
        "enfant-m|Non. Il rentre.",
        "narrateur|Victorino veut tout poser d'un geste. Le seau penche.",
        "narrateur|Un filet de sable mouille le banc.",
        "enfant-m|Pardon, banc.",
        "narrateur|Il s'assoit. Il ne fonce plus.",
        "narrateur|Personne ne donne la réponse.",
        "narrateur|Il regarde l'anse. Le croissant beige est plus gros, humide.",
        "enfant-m|Je te reconnais.",
        "narrateur|Manteau, doudou, seau : chacun sur le bois, puis dans les bras.",
        "papa|Tu as ralenti, à temps.",
        "narrateur|Du sable fin brille au fond, comme un secret.",
    ],
    (1, 2, 2): [
        "narrateur|Victorino glisse le seau dans le sac trop vite.",
        "copain|Et mon eau, avec !",
        "enfant-m|Pas d'eau. Du sable.",
        "narrateur|L'osier avale l'anse. Plus rien ne se voit.",
        "enfant-m|Je le trouve pas.",
        "narrateur|Il recule d'un pas. Les épaules descendent, puis se relèvent.",
        "narrateur|Maman s'accroupit, sans parler.",
        "narrateur|Victorino écoute le sac. Un grain roule, tout bas.",
        "narrateur|Il écarte l'osier. Le croissant beige est là.",
        "enfant-m|Reste avec moi.",
        "narrateur|Il range manteau et doudou à côté, sans tasser.",
        "papa|L'anse a parlé, à sa façon.",
        "narrateur|L'anse du seau touche le bord d'osier, tiède.",
    ],
    (1, 2, 3): [
        "narrateur|Au portail, le seau pèse, trop plein.",
        "copain|On le vide dans la rue !",
        "enfant-m|Il vient à la chambre.",
        "narrateur|Victorino le hisse trop haut. Un coquillage minuscule tombe.",
        "enfant-m|Oh.",
        "narrateur|Il s'agenouille. Il refuse de courir après tout.",
        "narrateur|Papa ne ramasse pas pour lui.",
        "narrateur|Victorino observe le fond. Le croissant beige entoure le coquillage.",
        "enfant-m|Vous deux.",
        "narrateur|Il reprend le coquillage, le manteau, le doudou.",
        "maman|Le barreau a vu ton geste.",
        "narrateur|Le coquillage roule au fond, collé au croissant.",
    ],
    (1, 3, 1): [
        "narrateur|Le doudou voyage contre lui, près du banc.",
        "copain|Il s'assoit sur le manteau !",
        "enfant-m|Il s'endort, lui.",
        "narrateur|Victorino pose tout en tas. L'oreille cache l'anse.",
        "enfant-m|Où es-tu ?",
        "narrateur|Il soulève l'oreille, lentement, sans fouiller.",
        "narrateur|Personne ne dit le mot seau.",
        "narrateur|Sous le tissu, le croissant beige apparaît.",
        "enfant-m|Toi, dessous.",
        "narrateur|Il prend le seau, le manteau, le doudou contre la poitrine.",
        "papa|L'oreille a laissé le passage.",
        "narrateur|L'oreille grise dépasse du manteau, un grain dessus.",
    ],
    (1, 3, 2): [
        "narrateur|Le doudou sent le sable, au bord du sac.",
        "copain|On le cache au fond, surprise !",
        "enfant-m|Il n'aime pas le noir.",
        "narrateur|Nino pousse. Le doudou et le seau s'emmêlent.",
        "enfant-m|Attends.",
        "narrateur|Victorino ouvre les mains. Il ne pousse plus.",
        "narrateur|Maman reste accroupie, silencieuse.",
        "narrateur|Il écoute l'osier. Un frottement de plastique.",
        "narrateur|Le croissant beige racle le bord, tout fin.",
        "enfant-m|Sors.",
        "narrateur|Il tire le seau, glisse le manteau, garde le doudou haut.",
        "papa|Tu as écouté le sac.",
        "narrateur|Un grain reste dans l'osier, comme un souvenir.",
    ],
    (1, 3, 3): [
        "narrateur|Près du portail, un fil gris pend du doudou.",
        "copain|On l'accroche au barreau !",
        "enfant-m|Il rentre.",
        "narrateur|Victorino veut tout tenir : fil, anse, manteau. Trop.",
        "narrateur|Le seau pose son ombre sur l'herbe, oublié une seconde.",
        "enfant-m|Non.",
        "narrateur|Il s'arrête. Il refuse de passer sans regarder.",
        "narrateur|Papa pose la main sur le loquet, sans l'ouvrir.",
        "narrateur|Victorino baisse les yeux. Le croissant beige est dans l'ombre.",
        "enfant-m|Je t'avais vu.",
        "narrateur|Il reprend le seau, le manteau, le fil dans l'autre main.",
        "maman|Le portail peut attendre une seconde.",
        "narrateur|Le fil gris pend près du barreau, puis le suit.",
    ],
    (2, 1, 1): [
        "narrateur|Au banc près du toboggan, le manteau fait toc.",
        "copain|On rebondit, une fois !",
        "enfant-m|Le manteau d'abord.",
        "narrateur|Victorino décroche trop vite. Le ballon échappe.",
        "narrateur|Il roule sous le banc, contre le seau.",
        "enfant-m|Les deux, dessous.",
        "narrateur|Il s'agenouille. Il ne plonge pas les deux mains.",
        "narrateur|Personne ne se baisse à sa place.",
        "narrateur|Il cherche le plastique. Le croissant beige luit.",
        "enfant-m|Et toi, ballon.",
        "narrateur|Seau, manteau, doudou, ballon : chacun son tour.",
        "papa|Tu as décroché, puis tu as cherché.",
        "narrateur|Une feuille jaune colle au manteau, au bois.",
    ],
    (2, 1, 2): [
        "narrateur|Victorino pose le seau dans le sac d'osier.",
        "copain|Le ballon par-dessus, comme un couvercle !",
        "enfant-m|Il écrase l'anse.",
        "narrateur|Le jaune s'enfonce. Plus d'anse.",
        "enfant-m|Pire.",
        "narrateur|Il retire le ballon, lentement, sans vider le sac.",
        "narrateur|Maman ne fouille pas.",
        "narrateur|Sous le cuir, le croissant beige revient.",
        "enfant-m|Respirer.",
        "narrateur|Il glisse manteau et doudou sur les côtés, pas dessus.",
        "papa|Le couvercle n'était pas un couvercle.",
        "narrateur|Le ballon reste un peu froid, près du sac.",
    ],
    (2, 1, 3): [
        "narrateur|Près du portail, Victorino a le ballon sous le bras.",
        "copain|On le lance par-dessus !",
        "enfant-m|Il rentre, lui aussi.",
        "narrateur|Le lancer manque. Le ballon tape le seau oublié au crochet.",
        "enfant-m|Le seau !",
        "narrateur|Il ne court pas. Il pose le ballon, puis marche.",
        "narrateur|Papa garde le portail entrebâillé, sans parler.",
        "narrateur|Victorino écoute. Un toc de plastique contre le fer.",
        "narrateur|Le croissant beige est au crochet, à côté du manteau.",
        "enfant-m|Vous deux.",
        "narrateur|Il décroche seau et manteau, prend le doudou au sac.",
        "maman|Une goutte sèche sur l'herbe, derrière vous.",
        "narrateur|Une goutte de rampe a suivi jusqu'au barreau.",
    ],
    (2, 2, 1): [
        "narrateur|Près du banc du toboggan, le seau vert sonne.",
        "copain|On le pose sur le bois, et on frappe !",
        "enfant-m|Il n'est pas un tambour.",
        "narrateur|Nino frappe. Victorino sursaute. L'anse lui échappe.",
        "enfant-m|Assez.",
        "narrateur|Il pose les paumes à plat. Il refuse de frapper.",
        "narrateur|Papa s'accroupit, silencieux.",
        "narrateur|Victorino regarde. Le croissant beige a un cercle plus clair.",
        "enfant-m|C'est toi.",
        "narrateur|Il prend le manteau au bois, le doudou dans le sac.",
        "maman|Le tambour s'est tu.",
        "narrateur|La rampe brille derrière eux, sans bruit.",
    ],
    (2, 2, 2): [
        "narrateur|Victorino glisse le seau dans le sac.",
        "enfant-m|Il rentre, maman.",
        "copain|Moi aussi, je rentre dedans !",
        "narrateur|Nino pousse trop. L'osier se tord. L'anse file au fond.",
        "enfant-m|Nino, stop.",
        "narrateur|Victorino attend que les mains de Nino sortent.",
        "narrateur|Personne ne tire à sa place.",
        "narrateur|Il écarte un brin d'osier. Le croissant beige est au fond.",
        "enfant-m|Tout au fond, toi.",
        "narrateur|Il sort le seau, glisse le manteau, le doudou.",
        "papa|L'osier a trop avalé, un moment.",
        "narrateur|L'anse jaune touche le bord, puis se calme.",
    ],
    (2, 2, 3): [
        "narrateur|Le seau vert est avec lui, près du portail.",
        "copain|On le fait sonner contre le fer !",
        "enfant-m|Ça fait mal aux oreilles.",
        "narrateur|Nino tape. Victorino recule. Le seau bascule.",
        "enfant-m|Il va partir dans la rue.",
        "narrateur|Il pose un pied devant, sans crier.",
        "narrateur|Maman ne ramasse pas. Elle attend.",
        "narrateur|Victorino observe l'anse au sol. Le croissant beige, côté herbe.",
        "enfant-m|Je te prends, sans taper.",
        "narrateur|Manteau au crochet, doudou au barreau, seau contre lui.",
        "papa|Le métal de la rampe se tait, lui aussi.",
        "narrateur|Le seau pose son ombre sur l'herbe du seuil.",
    ],
    (2, 3, 1): [
        "narrateur|Le doudou est contre sa joue, près du banc.",
        "copain|Il met le manteau, comme papa !",
        "enfant-m|Trop grand, le manteau.",
        "narrateur|Nino enroule le tissu. Le seau disparaît dessous.",
        "enfant-m|Mon seau.",
        "narrateur|Victorino déroule, pli après pli, sans arracher.",
        "narrateur|Papa ne déplie pas pour lui.",
        "narrateur|Au dernier pli, le croissant beige.",
        "enfant-m|Caché.",
        "narrateur|Il prend le seau près des bottes, le doudou, le manteau.",
        "maman|Le tissu a rendu l'anse.",
        "narrateur|Une feuille reste collée à la rampe, derrière.",
    ],
    (2, 3, 2): [
        "narrateur|Le doudou voyage, gris, vers le sac.",
        "copain|On le met avec le seau, tout serré !",
        "enfant-m|Il étouffe.",
        "narrateur|Trop serré. L'oreille et l'anse s'emmêlent.",
        "enfant-m|Je n'arrive pas.",
        "narrateur|Victorino ouvre le sac, largement, et attend.",
        "narrateur|Maman ne dénoue pas.",
        "narrateur|Il suit l'oreille, puis le plastique. Le croissant beige.",
        "enfant-m|Chacun sa place.",
        "narrateur|Seau d'un côté, doudou de l'autre, manteau au-dessus.",
        "papa|Le sac d'osier devient lourd, sans crier.",
        "narrateur|L'oreille grise dépasse, sans se coincer.",
    ],
    (2, 3, 3): [
        "narrateur|Le doudou retrouve le barreau un instant.",
        "copain|Il garde le portail !",
        "enfant-m|C'est nous, qui rentrons.",
        "narrateur|Victorino prend le doudou, oublie le seau au crochet.",
        "enfant-m|Attends. Il manque.",
        "narrateur|Il ne franchit pas. Il se retourne.",
        "narrateur|Papa tient le loquet, sans pousser.",
        "narrateur|Victorino écoute. Pas de chaîne. Un toc de plastique.",
        "narrateur|Le croissant beige, au crochet du toboggan.",
        "enfant-m|Toi aussi.",
        "narrateur|Il décroche le seau, le manteau, serre le doudou.",
        "maman|Tu as cherché derrière toi.",
        "narrateur|Le portail cliquette, tout bas, puis s'ouvre.",
    ],
    (3, 1, 1): [
        "narrateur|Au poteau, le manteau gris fait toc.",
        "copain|On le met sur la balançoire !",
        "enfant-m|Il n'est pas un siège.",
        "narrateur|Nino le jette. Il tombe sur le seau, sous le banc.",
        "enfant-m|Tout est dessous.",
        "narrateur|Victorino se penche, une main, pas les deux.",
        "narrateur|Personne ne ramone le dessous pour lui.",
        "narrateur|Il écarte le tissu. Le croissant beige, dans l'ombre du bois.",
        "enfant-m|Je me penche.",
        "narrateur|Seau, doudou, manteau, ballon : un, puis l'autre.",
        "papa|Le poteau a rendu le gris.",
        "narrateur|Le ballon reste dans l'herbe un instant, puis il le prend.",
    ],
    (3, 1, 2): [
        "narrateur|Victorino pose le seau dans le sac.",
        "maman|Il est froid, celui-là.",
        "copain|Le ballon, on le gonfle avec le sac !",
        "narrateur|Nino souffle. L'osier s'envole presque. L'anse bascule.",
        "enfant-m|Nino !",
        "narrateur|Victorino plaque le sac, sans crier.",
        "narrateur|Papa ne retient pas le sac à sa place.",
        "narrateur|Quand ça s'arrête, le croissant beige est contre la toile.",
        "enfant-m|On souffle plus.",
        "narrateur|Il prend le manteau au poteau, le doudou sous le banc.",
        "maman|Le sac a failli partir.",
        "narrateur|Le ballon a un brin d'herbe, sous le bras.",
    ],
    (3, 1, 3): [
        "narrateur|Près du portail, le ballon tapote le barreau.",
        "copain|On le fait passer à travers !",
        "enfant-m|Il est trop gros.",
        "narrateur|Le ballon coince. Victorino lâche le seau pour tirer.",
        "enfant-m|Le seau.",
        "narrateur|Il lâche aussi le ballon. Il refuse de tout tirer.",
        "narrateur|Maman ne pousse pas le jaune.",
        "narrateur|Victorino regarde l'herbe. Le croissant beige, au pied du fer.",
        "enfant-m|Toi d'abord.",
        "narrateur|Seau, manteau au poteau, doudou, puis le ballon de travers.",
        "papa|Le barreau a rendu le jaune, après.",
        "narrateur|La flaque redevient plate, derrière eux.",
    ],
    (3, 2, 1): [
        "narrateur|Près du banc, le seau vert a un peu d'eau.",
        "copain|On arrose la chaîne !",
        "enfant-m|Elle n'a pas soif.",
        "narrateur|Victorino verse trop vite. L'eau gicle. L'anse glisse.",
        "enfant-m|Pardon.",
        "narrateur|Il pose le seau. Il attend que l'eau finisse.",
        "narrateur|Papa ne ramasse pas l'anse.",
        "narrateur|Quand c'est calme, le croissant beige est plus foncé, mouillé.",
        "enfant-m|Je te verse dans l'herbe, tout bas.",
        "narrateur|Manteau au poteau, doudou sous le banc, seau vide.",
        "maman|L'anse reste froide, dans sa main.",
        "narrateur|Un cling lointain, puis plus rien.",
    ],
    (3, 2, 2): [
        "narrateur|Victorino glisse le seau dans le sac.",
        "enfant-m|Il rentre.",
        "copain|On le cache, et tu cherches !",
        "narrateur|Nino ferme l'osier trop fort. L'anse plie.",
        "enfant-m|Ouvre.",
        "narrateur|Victorino ne cherche pas au hasard. Il attend l'ouverture.",
        "narrateur|Maman tient le bord, sans vider.",
        "narrateur|Une fente. Le croissant beige, plié, puis il se détend.",
        "enfant-m|Tout droit, toi.",
        "narrateur|Manteau au poteau, doudou sous le banc, seau redressé.",
        "papa|Le sac a trop serré, un moment.",
        "narrateur|Un cling lointain, et le sac d'osier qui s'apaise.",
    ],
    (3, 2, 3): [
        "narrateur|Le seau vert pèse, près du portail.",
        "copain|On le pose sur le fer, comme un chapeau !",
        "enfant-m|Il va tomber dans la rue.",
        "narrateur|Nino le hisse. Victorino le rattrape au bord.",
        "enfant-m|Assez haut.",
        "narrateur|Il le baisse. Il refuse le chapeau.",
        "narrateur|Papa ne lève pas les bras.",
        "narrateur|Victorino observe l'anse. Le croissant beige a une ombre de barreau.",
        "enfant-m|Tu restes avec moi, pas sur le fer.",
        "narrateur|Doudou au barreau, manteau au poteau, seau contre la hanche.",
        "maman|Il vient.",
        "narrateur|Le seau pose son ombre sur l'herbe du portail.",
    ],
    (3, 3, 1): [
        "narrateur|Le doudou est un peu humide, contre lui.",
        "copain|On le sèche sur la chaîne !",
        "enfant-m|Trop froid, la chaîne.",
        "narrateur|Nino l'accroche. L'oreille s'enroule au métal.",
        "enfant-m|Il est coincé.",
        "narrateur|Victorino dénoue, tour après tour, sans tirer.",
        "narrateur|Personne ne coupe le nœud.",
        "narrateur|Au pied du poteau, le seau attend. Le croissant beige, sec.",
        "enfant-m|Toi, tu n'étais pas coincé.",
        "narrateur|Il tire le seau par l'anse, prend le manteau.",
        "papa|Tu as cherché.",
        "narrateur|La chaîne se tait, tout à fait.",
    ],
    (3, 3, 2): [
        "narrateur|Le doudou voyage, l'oreille molle, vers le sac.",
        "copain|On le met à califourchon sur l'anse !",
        "enfant-m|Il va tomber.",
        "narrateur|Nino l'assoit. Le doudou glisse au fond, avec le seau.",
        "enfant-m|Les deux, perdus.",
        "narrateur|Victorino ouvre tout grand, et regarde avant de plonger.",
        "narrateur|Maman tient l'osier ouvert, sans fouiller.",
        "narrateur|L'oreille, puis le croissant beige, l'un contre l'autre.",
        "enfant-m|Vous deux, dehors.",
        "narrateur|Il les sort, prend le manteau au poteau.",
        "papa|C'est le tien, le seau.",
        "narrateur|L'oreille grise dépasse du sac d'osier, puis le quitte.",
    ],
    (3, 3, 3): [
        "narrateur|Le doudou retrouve le barreau, puis les bras.",
        "copain|On reste, un tour chacun !",
        "enfant-m|Le goûter attend.",
        "narrateur|Victorino dit non, trop vite, et part sans le seau.",
        "enfant-m|Stop.",
        "narrateur|Un pas en arrière. Il refuse de franchir comme ça.",
        "narrateur|Papa ne le rappelle pas. Il attend le geste.",
        "narrateur|Victorino écoute le parc. Un silence, puis rien.",
        "narrateur|Il cherche des yeux. Le croissant beige, contre le barreau.",
        "enfant-m|J'ai tout, maintenant.",
        "narrateur|Seau, manteau au poteau, doudou. Le banc est vide.",
        "maman|Le banc est vide, oui.",
        "narrateur|Le portail est frais, sous la main libre.",
    ],
}

FIN = {
    (1, 1, 1): [
        "narrateur|Dans la chambre, la bande de parc a bougé.",
        "narrateur|Elle touche le seau, posé sur le rebord.",
        "enfant-m|Il n'est plus sous le lit.",
        "papa|Tu te souviens du seau à l'envers ?",
        "enfant-m|Surtout de ça.",
        "maman|Le croissant a voyagé, tu vois.",
        "narrateur|Un grain de sable colle à la manche grise.",
        "narrateur|Le croissant beige sèche sur l'anse, au rebord.",
    ],
    (1, 1, 2): [
        "narrateur|Le sac d'osier s'endort sous le portemanteau.",
        "narrateur|Le seau, lui, a gagné le rebord de la fenêtre.",
        "enfant-m|L'anse a parlé, dans le sac.",
        "papa|Tu l'as écoutée.",
        "maman|Le volet reste ouvert, un peu.",
        "narrateur|Le ballon tapote le bord, puis s'arrête.",
        "narrateur|Le sac d'osier garde un grain, au fond.",
    ],
    (1, 1, 3): [
        "narrateur|Le ballon s'assoit près de la porte.",
        "narrateur|Un brin d'herbe tient au cuir.",
        "enfant-m|Le barreau a coincé l'anse.",
        "papa|Et tu as tourné, sans tirer.",
        "maman|Le goûter sent le pain, maintenant.",
        "narrateur|La fenêtre est entrouverte. Le seau coupe la bande de lumière.",
        "narrateur|Le brin d'herbe sèche, près de la poignée.",
    ],
    (1, 2, 1): [
        "narrateur|Victorino pose le seau sur le rebord, lourd.",
        "enfant-m|Il a du sable, pour plus tard.",
        "papa|Tu as ralenti, au banc.",
        "enfant-m|Oui. Il penchait.",
        "maman|Le doudou a retrouvé l'oreiller.",
        "narrateur|Du sable fin brille au fond du seau.",
        "narrateur|Le croissant beige est plus gros, un peu humide.",
    ],
    (1, 2, 2): [
        "narrateur|L'anse touche le bois du rebord, tiède.",
        "enfant-m|Dans le sac, je l'entendais.",
        "papa|Un grain a roulé, tu te souviens ?",
        "enfant-m|Oui. Puis le croissant.",
        "maman|Le manteau gris est sur la chaise.",
        "narrateur|Un peu de sable reste au fond, collé.",
        "narrateur|L'osier, sous le portemanteau, sent le parc.",
    ],
    (1, 2, 3): [
        "narrateur|Un coquillage minuscule roule au fond du seau.",
        "enfant-m|Il est venu avec nous.",
        "papa|Tu t'es agenouillé, au portail.",
        "enfant-m|Pour lui, et pour l'anse.",
        "maman|L'anse du seau est tiède, maintenant.",
        "narrateur|Le coquillage reste collé au croissant beige.",
        "narrateur|Le loquet du volet ne tape plus.",
    ],
    (1, 3, 1): [
        "narrateur|Le doudou retrouve l'oreiller, l'oreille pliée.",
        "enfant-m|Elle avait caché l'anse.",
        "papa|Tu as soulevé l'oreille, sans fouiller.",
        "enfant-m|Le croissant était dessous.",
        "maman|Un grain tient sur le tissu, tu vois.",
        "narrateur|L'oreille grise a un grain, sur l'oreiller.",
        "narrateur|Le seau, au rebord, veille le doudou.",
    ],
    (1, 3, 2): [
        "narrateur|Le doudou sent le bac, contre la joue du soir.",
        "enfant-m|Le sac a trop serré, un moment.",
        "papa|Tu as écouté l'osier.",
        "enfant-m|Le plastique a frotté.",
        "maman|Le seau sèche près des chaussettes.",
        "narrateur|Un grain reste dans l'osier, oublié.",
        "narrateur|L'oreille, elle, est sèche, sur l'oreiller.",
    ],
    (1, 3, 3): [
        "narrateur|Un fil gris pend près de la poignée de la chambre.",
        "enfant-m|Il venait du doudou, au barreau.",
        "papa|Tu as regardé l'ombre, avant de passer.",
        "enfant-m|Le croissant était là.",
        "maman|Le portail a attendu une seconde.",
        "narrateur|Le fil s'endort sur la commode.",
        "narrateur|Le seau coupe la bande de parc, au rebord.",
    ],
    (2, 1, 1): [
        "narrateur|Le manteau gris retrouve le crochet de la chambre.",
        "enfant-m|Une feuille jaune est collée.",
        "papa|Tu as décroché, puis tu as cherché dessous.",
        "enfant-m|Le ballon et le seau, ensemble.",
        "maman|La feuille peut rester, un soir.",
        "narrateur|La feuille jaune colle au manteau, sur la chaise.",
        "narrateur|Le seau, au rebord, a un reflet de rampe, pâle.",
    ],
    (2, 1, 2): [
        "narrateur|Le ballon est un peu froid, près des clés.",
        "enfant-m|Il n'était pas un couvercle.",
        "papa|Tu l'as retiré, lentement.",
        "enfant-m|Le croissant est revenu.",
        "maman|Les clés de papa sont dans la coupelle.",
        "narrateur|Une feuille sèche près des clés.",
        "narrateur|Le seau tient sur le rebord, l'anse libre.",
    ],
    (2, 1, 3): [
        "narrateur|Une goutte de rampe a séché sur le plancher.",
        "enfant-m|Elle a suivi jusqu'au barreau.",
        "papa|Tu as posé le ballon, puis tu as marché.",
        "enfant-m|Sans courir.",
        "maman|Le volet laisse passer l'herbe.",
        "narrateur|Le ballon garde l'odeur du plastique froid.",
        "narrateur|Le croissant beige, au rebord, n'a plus de goutte.",
    ],
    (2, 2, 1): [
        "narrateur|Le seau penche un peu, cette fois sur le rebord.",
        "enfant-m|Il n'est pas un tambour.",
        "papa|Tu as posé les paumes, au banc.",
        "enfant-m|Le cercle clair, sur le croissant.",
        "maman|La rampe est loin, maintenant.",
        "narrateur|Le seau penche vers le parc, par la fenêtre.",
        "narrateur|Un cercle plus clair reste sur l'anse.",
    ],
    (2, 2, 2): [
        "narrateur|Le manteau a glissé, puis Victorino le remet.",
        "enfant-m|L'osier avait trop avalé.",
        "papa|Tu as attendu que Nino sorte les mains.",
        "enfant-m|Puis le croissant, au fond.",
        "maman|Le sac sèche sous le portemanteau.",
        "narrateur|L'anse touche le rebord, sage.",
        "narrateur|Le manteau gris tient au crochet, sans glisser.",
    ],
    (2, 2, 3): [
        "narrateur|La rampe du toboggan reste loin, derrière le volet.",
        "enfant-m|Nino voulait taper le fer.",
        "papa|Tu as mis un pied devant.",
        "enfant-m|Pour qu'il ne parte pas dans la rue.",
        "maman|L'ombre du seau est sur le plancher, maintenant.",
        "narrateur|Le seau pose son ombre courte, au rebord.",
        "narrateur|Le loquet tient, sans taper.",
    ],
    (2, 3, 1): [
        "narrateur|L'oreille du doudou dépasse, tournée vers le parc.",
        "enfant-m|Le manteau l'avait enroulé.",
        "papa|Pli après pli.",
        "enfant-m|Le croissant, au dernier.",
        "maman|L'oreille est sèche, tu sens ?",
        "narrateur|L'oreille du doudou dépasse de l'oreiller.",
        "narrateur|Une feuille, collée à la rampe, n'est plus là.",
    ],
    (2, 3, 2): [
        "narrateur|L'anse lisse a gardé le froid de la rampe.",
        "enfant-m|Chacun sa place, dans le sac.",
        "papa|Tu as ouvert, largement.",
        "enfant-m|L'oreille d'un côté.",
        "maman|Le seau de l'autre.",
        "narrateur|L'oreille molle est sèche, sur l'oreiller.",
        "narrateur|Le seau, au rebord, n'étouffe plus personne.",
    ],
    (2, 3, 3): [
        "narrateur|Le rayon a bougé : il touche le seau, plus l'oreiller.",
        "enfant-m|J'allais partir sans lui.",
        "papa|Tu t'es retourné.",
        "enfant-m|Le toc de plastique.",
        "maman|Le crochet du toboggan l'avait gardé.",
        "narrateur|Le rayon d'après-midi a bougé, sur le plancher.",
        "narrateur|Le seau, dans le rayon, a l'anse claire.",
    ],
    (3, 1, 1): [
        "narrateur|La chaîne lointaine se tait. Le seau pose son ombre.",
        "enfant-m|Le manteau était un siège, pour Nino.",
        "papa|Tu t'es penché, une main.",
        "enfant-m|Le croissant, dans l'ombre du bois.",
        "maman|Le ballon s'endort près du seau.",
        "narrateur|Le ballon s'endort près du seau vert.",
        "narrateur|L'ombre du seau est ronde, sur le rebord.",
    ],
    (3, 1, 2): [
        "narrateur|Le creux de l'oreiller attend, vide d'une seconde.",
        "enfant-m|Nino a soufflé trop fort.",
        "papa|Tu as plaqué le sac.",
        "enfant-m|Le croissant contre la toile.",
        "maman|Le doudou peut s'asseoir, maintenant.",
        "narrateur|Le creux de l'oreiller reprend le doudou.",
        "narrateur|Un brin d'herbe sèche, sous le bras du ballon.",
    ],
    (3, 1, 3): [
        "narrateur|Ça sent l'herbe, un peu, dans la bande de lumière.",
        "enfant-m|Le ballon était trop gros, pour le barreau.",
        "papa|Tu as tout lâché, pour mieux prendre.",
        "enfant-m|Le seau d'abord.",
        "maman|La flaque, derrière, s'est tue.",
        "narrateur|Ça sent l'herbe, un peu, près du volet.",
        "narrateur|Le seau, au rebord, a un brin collé au croissant.",
    ],
    (3, 2, 1): [
        "narrateur|L'anse froide se réchauffe contre le bois.",
        "enfant-m|J'ai versé trop vite.",
        "papa|Tu as attendu que l'eau finisse.",
        "enfant-m|Le croissant était plus foncé.",
        "maman|Il sèche, maintenant.",
        "narrateur|L'anse se réchauffe, sur le rebord.",
        "narrateur|Un cling lointain n'arrive plus jusqu'ici.",
    ],
    (3, 2, 2): [
        "narrateur|Le manteau gris est chaud, sur la chaise.",
        "enfant-m|Nino a trop serré l'osier.",
        "papa|Tu as attendu la fente.",
        "enfant-m|Le croissant s'est détendu.",
        "maman|Un grain à la manche, tu vois.",
        "narrateur|Le manteau gris est chaud, un grain à la manche.",
        "narrateur|Le seau, redressé, tient droit au rebord.",
    ],
    (3, 2, 3): [
        "narrateur|Les clés de papa restent dans la coupelle, à côté du seau.",
        "enfant-m|Il n'était pas un chapeau, pour le fer.",
        "papa|Tu l'as baissé.",
        "enfant-m|L'ombre du barreau, sur le croissant.",
        "maman|Les clés font un petit bruit, puis plus.",
        "narrateur|Les clés restent dans la coupelle.",
        "narrateur|Le seau, lui, a quitté le fer pour le bois.",
    ],
    (3, 3, 1): [
        "narrateur|La chaîne a laissé un cling dans la mémoire du seau.",
        "enfant-m|L'oreille était coincée.",
        "papa|Tour après tour, sans tirer.",
        "enfant-m|Le seau, lui, attendait au pied.",
        "maman|Le doudou est sec, tu sens ?",
        "narrateur|L'oreille est sèche, sur l'oreiller.",
        "narrateur|Le seau, au rebord, n'a plus de cling.",
    ],
    (3, 3, 2): [
        "narrateur|L'oreille molle dépasse du seau, au rebord, une seconde.",
        "enfant-m|Puis je la mets sur l'oreiller.",
        "papa|Tu as regardé avant de plonger.",
        "enfant-m|L'oreille, puis le croissant.",
        "maman|C'est le tien, le seau.",
        "narrateur|L'oreille molle quitte le seau pour l'oreiller.",
        "narrateur|Le croissant beige reste, seul, sur l'anse.",
    ],
    (3, 3, 3): [
        "narrateur|Le loquet du volet ne tape plus. Il tient.",
        "enfant-m|J'allais partir trop vite.",
        "papa|Tu as fait un pas en arrière.",
        "enfant-m|Le croissant, contre le barreau.",
        "maman|Le banc du parc est vide, maintenant.",
        "enfant-m|J'ai tout.",
        "narrateur|Le loquet tient. La bande de parc touche le seau.",
    ],
}

Q_FIELDS = {
    "expected_answer": "le seau",
    "accepted_examples": (
        "le seau | seau | le manteau | le doudou | ses affaires | "
        "il le prend | seau vert | le seau vert"
    ),
    "retry_prompt": "Le seau vert est là. Victorino prend quoi ?",
    "engine_ok_text": "Oui, le seau vert.",
    "engine_near_text": "Tu es tout près. L'anse, le croissant.",
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
        return "volet,enfants_parc"
    if kind in {"transition_question", "passage_question"}:
        return ""
    if cid.endswith("_C0001"):
        return "seau,anse"
    if kind == "passage_fin":
        return {1: "chambre,volet", 2: "chambre,manteau", 3: "chambre,chaine"}.get(i or 3, "chambre")
    if kind == "passage" and i and "_T0002_" not in cid:
        return {1: "sable,bac", 2: "toboggan,plastique", 3: "chaine,balancoire"}[i]
    if j and "_T0003_" not in cid and "_T0002_P000" in cid:
        return {1: "ballon", 2: "seau,sable", 3: "doudou,tissu"}[j]
    if "_T0003_P000" in cid and kind == "passage":
        return "parc,anse"
    return ""


def extra_emphasis(kind: str, prof: str, text_join: str) -> dict:
    extra: dict = {}
    low = text_join.lower()
    if prof == "opening":
        extra["emphasis"] = "croissant beige"
    elif prof == "clue":
        extra["emphasis"] = "seau"
    elif prof == "confirm":
        extra["emphasis"] = "seau"
    elif prof == "action":
        if "ballon" in low:
            extra["emphasis"] = "ballon"
        elif "doudou" in low:
            extra["emphasis"] = "doudou"
        else:
            extra["emphasis"] = "seau"
    elif prof == "resolution":
        extra["emphasis"] = "croissant" if "croissant" in low else "anse"
    elif prof == "ending":
        extra["emphasis"] = "seau" if "seau" in low else "rebord"
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
                "option_2_label": "le sac",
                "option_3_label": "le portail",
            }
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = L3[(i, j, k)]
                s[f"{p3}_F0001"] = FIN[(i, j, k)]
    s = {cid: split_lines(lines) for cid, lines in s.items()}
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
    print(f"chemins mots min={min(lengths)} max={max(lengths)} moy={sum(lengths)//len(lengths)}")
    return min(lengths), max(lengths), sum(lengths) // len(lengths)


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
        "Victorino veut remplir son seau vert au parc et le ramener à la chambre "
        "avant le goûter. Sur l'anse, un croissant de sable beige. Nino ne veut "
        "pas la même chose : verser, glisser, pendre. La première traction "
        "renverse le seau. Bac, toboggan ou balançoires, puis ballon, seau ou "
        "doudou, puis banc, sac ou portail. Victorino refuse de foncer, retrouve "
        "le croissant, reprend ses affaires. Au retour, le seau n'est plus sous "
        "le lit : il tient au rebord, dans la bande de parc."
    )
    out["title"] = "Le seau vert de Victorino"
    out["characters"] = "Victorino, Nino, papa, maman"
    out["setting"] = "chambre entrouverte, puis le parc"
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
        f"# TREE-AUT-028 — Le seau vert de Victorino\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "- **Titre noyau :** *Le seau vert de Victorino*\n"
        "- **Public :** N3 (≤ 16 mots/phrase)\n"
        "- **Leçon :** AUT.AFF.003 — reprendre, vécue (le seau, le manteau et le "
        "doudou rentrent quand Victorino retrouve l'anse au croissant, sans liste)\n"
        "- **Personnages :** Victorino, Nino, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Le loquet du volet tape, la fenêtre est entrouverte, une bande de parc "
        "coupe l'oreiller. Sous le lit, le seau vert porte un croissant de sable "
        "beige. Victorino veut le remplir au parc et le ramener avant le goûter. "
        "Nino ne veut pas la même chose au même moment : tout verser, glisser avec, "
        "pendre à la chaîne. La première traction renverse l'objet. Bac, toboggan "
        "ou balançoires changent la chute. Ballon, seau ou doudou changent la "
        "friction. Banc, sac ou portail changent comment l'anse se retrouve. "
        "Victorino refuse de foncer, écoute le lieu, paie le croissant du début. "
        "Au retour, le seau n'est plus sous le lit : il tient au rebord.\n\n"
        "## Vécu\n\n"
        "Chambre, loquet, bande de lumière, oreille pliée, croissant beige, "
        "manteau gris, grille du parc. Impatience (tire trop fort, « vite »), "
        "découragement (seau à l'envers, épaules, sourire disparu), fierté calme "
        "(il reconnaît l'anse tout seul). Merci vécu quand il reprend le seau. "
        "Question d'écoute : tu prends quoi. T1 bac / toboggan / balançoires. "
        "T2 ballon / seau / doudou. T3 banc / sac / portail. Indice unique payé "
        "au climax : le croissant de sable.\n\n"
        "## Vu et corrigé\n\n"
        "P1 F-NAR-019 example4 v2. Ouverture inventée (loquet, bande de parc), "
        "pas les cinq manières listées. Tics « encore / déjà / tout doux / tout "
        "calme » retirés. Gabarit cassé : L1, L2, L3 et fins écrits par chemin. "
        "27 fins textuellement distinctes, 27 dernières images distinctes. "
        "Deux enfants, deux envies. Adulte accroupi, sans réciter la règle. "
        "Pas COL-015. Sami, Tom, Léa absents. Troupe D16. N3 ≤ 16. Q = seau. "
        "TTS par chunk : `notes`, `text_ssml`, `text_xai_tags`, piper variable. "
        "`slow` réservé aux choix, à l'indice et aux fins. Relu ouverture + 3 L1 "
        f"+ 9 L2 + 27 L3/fins. `check()` N3 OK. Chemins {mn}–{mx} mots, moy. {moy}. "
        "Pas apply.\n\n"
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
        "- 0 occurrence de « ranger », « on va apprendre », « après le jeu »\n"
        "- 0 escargot / loupe / carnet\n"
        "- papa/maman parlent, une question, un merci vécu\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
