#!/usr/bin/env python3
"""TREE-DIF-062 — F-NAR-019. Le seau rouge de Nino, à la pompe. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-062"
N1 = 10
TITLE = "Le seau rouge de Nino, à la pompe"
FIL = (
    "Dans la cour, Nino veut remplir son seau rouge "
    "et donner à boire au basilic de la fenêtre. "
    "Papa commence : « On met le seau sous le… » "
    "Nino coupe : « Bec ! » Le seau tape de travers. Rien ne tombe. "
    "T1 = seau / arrosoir / torchon, les trois partent. "
    "T2 = pompe (le fer couvre) / muret (les abeilles couvrent) / "
    "fenêtre (trop haute). "
    "T3 = neuf façons de laisser le mot arriver. L'eau tombe. Le basilic boit."
)
CHARS = "Nino, papa, maman"
SETTING = "la cour : pompe, muret au thym, fenêtre du basilic"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "seau rouge",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_basilic_a_soif_Nino_coupe; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_peuvent_partir; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_mot_manque; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=la_phrase_de_papa_se_casse; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_mot_arrive_quand_on_laisse_finir; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=leau_est_arrivée_le_basilic_boit; tempo=posé; sourire=léger; respiration=ample",
    },
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict, emphasis: str | None) -> str:
    body = esc(text)
    if emphasis:
        e = esc(emphasis)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict, emphasis: str | None) -> str:
    body = text
    if emphasis:
        body = body.replace(emphasis, f"<emphasis>{emphasis}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m["pitchTag"]:
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    tail = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {tail}".strip()


def vet(lines: list[str]) -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"puces « {tok} »: {ph}")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""
        out.append(f"{role}|{ph}")
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    lines = vet(lines)
    m = dict(PROFILES[profile])
    extra = extra or {}
    emphasis = extra.get("emphasis", m["emphasis"])
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else ""
    nc["text_ssml"] = ssml(text, m, emphasis)
    nc["text_xai_tags"] = xai(text, m, emphasis)
    nc["length_scale_piper"] = m["piper"]
    nc["rate_label"] = m["rate"]
    nc["rate_wpm"] = m["wpm"]
    nc["speed_xai"] = m["speed"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = emphasis or ""
    nc["pause_before_ms"] = extra.get("pause_before", 0)
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
    nc["notes"] = extra.get("notes", m["note"])
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


def path_words(by: dict, a: int, b: int, c: int) -> int:
    ids = [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        f"CHK_T0001_P000{a}",
        f"CHK_T0001_P000{a}_Q0001",
        f"CHK_T0001_P000{a}_C0001",
        f"CHK_T0001_P000{a}_T0002_P0000",
        f"CHK_T0001_P000{a}_T0002_P000{b}",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001",
    ]
    return sum(words(by[i]["text"]) for i in ids)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


OPENING = [
    "narrateur|Une goutte pend au bec de la pompe.",
    "narrateur|Elle tombe sur la pierre, tic.",
    "narrateur|La cour sent le fer et le thym.",
    "narrateur|Nino vit ici, avec papa et maman.",
    "papa|Le basilic a soif, là-haut.",
    "enfant-m|Je veux lui donner à boire.",
    "maman|Le soleil quitte le mur, vite.",
    "narrateur|En ce moment, Nino tient le seau.",
    "enfant-m|Il est rouge, pour l'eau.",
    "papa|On met le seau sous le.",
    "enfant-m|Bec !",
    "narrateur|Le seau tape trop tôt, de travers.",
    "narrateur|Le manche grince, sans une goutte.",
    "enfant-m|Pourquoi ça ne vient pas ?",
    "papa|Ma phrase n'était pas finie.",
    "maman|Le mot manquait, tout bas.",
    "papa|Merci, tu as tenu le seau.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près de la pierre.",
    "narrateur|Le seau, l'arrosoir, et le torchon.",
    "papa|Tu prends quoi d'abord, Nino ?",
]

T1 = {
    1: {
        "lab": "le seau",
        "sons": "seau,fer",
        "emphasis": "seau rouge",
        "passage": [
            "narrateur|Nino prend d'abord le seau rouge.",
            "enfant-m|Pour l'eau, tout de suite.",
            "papa|Tiens-le droit, près de toi.",
            "narrateur|Il penche trop tôt, trop fort.",
            "narrateur|Une poussière roule au fond, sèche.",
            "papa|On met le seau sous le.",
            "enfant-m|Bec !",
            "narrateur|Papa referme la bouche.",
            "maman|L'arrosoir, ensuite, contre lui.",
            "narrateur|Papa glisse le torchon dans la poche.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|J'ai trop parlé, moi.",
            "papa|Le seau d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nino a pris le seau d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "seau",
            "accepted_examples": "seau | le seau | rouge | le rouge | seau rouge",
            "retry_prompt": "Nino tient le seau. Il tient quoi ?",
        },
        "confirm": [
            "narrateur|Le seau reste contre sa jambe.",
            "enfant-m|On va jusqu'à l'eau.",
            "maman|Le basilic attend, là-haut.",
            "papa|Tu tiens bien, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le seau penche vers la pompe.",
        ],
        "voy": "Le seau penche vers la pompe.",
    },
    2: {
        "lab": "l'arrosoir",
        "sons": "metal,eau",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|Nino prend d'abord l'arrosoir vert.",
            "enfant-m|Le bec est froid, dans ma main.",
            "maman|Garde le bec vers le bas.",
            "narrateur|Le métal fait un petit toc.",
            "papa|On met le bec sous le.",
            "enfant-m|Fer !",
            "narrateur|Papa s'arrête, les lèvres rondes.",
            "narrateur|Rien ne sort, trop tôt.",
            "papa|Le seau, ensuite, sous le bras.",
            "narrateur|Maman glisse le torchon dans la poche.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|J'écoute, cette fois.",
            "maman|L'arrosoir d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nino a pris l'arrosoir d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "arrosoir",
            "accepted_examples": "arrosoir | l'arrosoir | le vert | arrosoir vert | le bec",
            "retry_prompt": "Nino tient l'arrosoir. Il tient quoi ?",
        },
        "confirm": [
            "narrateur|L'arrosoir tape un peu sa hanche.",
            "enfant-m|Le bec va chercher l'eau.",
            "papa|Le seau voyage avec, sous le bras.",
            "maman|Tu tiens le bec, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le torchon dort dans la poche.",
        ],
        "voy": "L'arrosoir tape un peu sa hanche.",
    },
    3: {
        "lab": "le torchon",
        "sons": "tissu,fer",
        "emphasis": "torchon",
        "passage": [
            "narrateur|Nino prend d'abord le torchon beige.",
            "enfant-m|Pour essuyer le fer, vite.",
            "papa|Il sent le savon, un peu.",
            "narrateur|Le tissu frotte la pompe, trop vite.",
            "papa|On essuie le manche, puis le.",
            "enfant-m|Bec !",
            "narrateur|Papa referme la bouche, un doigt levé.",
            "maman|Le seau, ensuite, et l'arrosoir.",
            "narrateur|Papa les pose contre lui, l'un après l'autre.",
            "narrateur|Près de la pierre, plus rien n'attend.",
            "enfant-m|Le mot n'était pas là.",
            "papa|Le torchon d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nino a pris le torchon d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "torchon",
            "accepted_examples": "torchon | le torchon | le tissu | le linge | le beige",
            "retry_prompt": "Nino tient le torchon. Il tient quoi ?",
        },
        "confirm": [
            "narrateur|Le torchon pend contre sa poche.",
            "enfant-m|Pour le fer, après.",
            "maman|Le seau et l'arrosoir pèsent contre lui.",
            "papa|On avance, tous les trois ?",
            "enfant-m|Oui.",
            "narrateur|Le tissu sent le savon du fer.",
        ],
        "voy": "Le torchon pend contre sa poche.",
    },
}

T2 = {
    (1, 1): {
        "sons": "pompe,grincement",
        "emphasis": "pompe",
        "passage": [
            "narrateur|Le seau rouge arrive près de la pompe.",
            "narrateur|Il tape le fer, un petit toc.",
            "narrateur|Le manche grince, trop fort.",
            "enfant-m|C'est ici, pour l'eau ?",
            "papa|On met le seau sous le.",
            "narrateur|Le grincement mange la fin.",
            "enfant-m|Sous le bec !",
            "narrateur|L'eau rate le seau, sur la pierre.",
            "enfant-m|Elle n'est pas dedans.",
            "maman|Le fer a couvert le mot.",
            "papa|On fait comment, Nino ?",
        ],
    },
    (2, 1): {
        "sons": "pompe,grincement",
        "emphasis": "pompe",
        "passage": [
            "narrateur|L'arrosoir arrive près de la pompe.",
            "narrateur|Le bec s'accroche au bras, sec.",
            "enfant-m|Le bec, sous le fer ?",
            "papa|On met le bec sous le.",
            "narrateur|Le manche grince, trop fort.",
            "enfant-m|Sous le bec !",
            "narrateur|Nino a parlé trop tôt, trop fort.",
            "narrateur|Une goutte tombe à côté, perdue.",
            "enfant-m|Le vert n'a rien pris.",
            "maman|Le fer a mangé la fin.",
            "papa|On fait comment, Nino ?",
        ],
    },
    (3, 1): {
        "sons": "pompe,grincement",
        "emphasis": "pompe",
        "passage": [
            "narrateur|Le torchon arrive près de la pompe.",
            "narrateur|Il s'enroule autour du manche, trop vite.",
            "enfant-m|J'essuie, et l'eau vient ?",
            "papa|On essuie, puis on met sous le.",
            "narrateur|Le fer grince, trop fort.",
            "enfant-m|Sous le bec !",
            "narrateur|Le tissu saute, sans une goutte.",
            "narrateur|Nino baisse les épaules, les joues chaudes.",
            "maman|Le grincement a couvert le mot.",
            "papa|On fait comment, Nino ?",
        ],
    },
    (1, 2): {
        "sons": "abeilles,thym",
        "emphasis": "muret",
        "passage": [
            "narrateur|Le seau se pose dans la terre, un peu.",
            "enfant-m|Le pot a soif, ici ?",
            "maman|Il est près des.",
            "narrateur|Les abeilles couvrent le mot, trop fort.",
            "narrateur|Un thym sent, tout chaud.",
            "enfant-m|Près des fleurs !",
            "narrateur|Nino verse trop tôt, à côté.",
            "narrateur|L'eau file sous les abeilles, perdue.",
            "enfant-m|Le petit pot n'a rien.",
            "papa|On n'entend plus la fin.",
            "maman|Tu trouves comment ?",
        ],
    },
    (2, 2): {
        "sons": "abeilles,thym",
        "emphasis": "muret",
        "passage": [
            "narrateur|Le bec de l'arrosoir touche une feuille.",
            "enfant-m|Je verse sur le thym ?",
            "maman|Pas le thym, près des.",
            "narrateur|Les abeilles bourdonnent, trop près.",
            "enfant-m|Près des fleurs !",
            "narrateur|Nino verse, et les abeilles s'envolent.",
            "narrateur|Le petit pot, plus bas, reste sec.",
            "enfant-m|J'ai trop vite parlé.",
            "papa|Le bourdon a mangé le mot.",
            "maman|Tu trouves comment ?",
        ],
    },
    (3, 2): {
        "sons": "abeilles,thym",
        "emphasis": "muret",
        "passage": [
            "narrateur|Le torchon prend une poussière de thym.",
            "enfant-m|J'essuie le pot, ici ?",
            "maman|Le petit, près des.",
            "narrateur|Les abeilles couvrent la fin, trop fort.",
            "enfant-m|Près des fleurs !",
            "narrateur|Nino frotte le grand pot, trop haut.",
            "narrateur|Le petit, contre le thym, reste sec.",
            "enfant-m|Ce n'était pas celui-là.",
            "papa|On n'a pas eu le mot.",
            "maman|Tu trouves comment ?",
        ],
    },
    (1, 3): {
        "sons": "oiseau,fenetre",
        "emphasis": "fenêtre",
        "passage": [
            "narrateur|Sous la fenêtre, le seau reste trop bas.",
            "narrateur|Là-haut, le basilic sent le poivre.",
            "enfant-m|Je le vois, les feuilles ?",
            "papa|À gauche du.",
            "narrateur|Papa s'arrête, un doigt en l'air.",
            "enfant-m|Du bord !",
            "narrateur|Nino verse contre le mur, trop tôt.",
            "narrateur|L'eau file, et le basilic reste sec.",
            "enfant-m|Mes pieds n'arrivent pas.",
            "maman|Tes pieds n'arrivent pas, Nino.",
            "papa|Tu fais quoi, alors ?",
        ],
    },
    (2, 3): {
        "sons": "oiseau,fenetre",
        "emphasis": "fenêtre",
        "passage": [
            "narrateur|Le bec n'atteint pas le bord.",
            "narrateur|Le basilic penche, trop haut pour lui.",
            "enfant-m|Je tends le bec, comme ça ?",
            "papa|À gauche du.",
            "narrateur|Papa garde le doigt en l'air.",
            "enfant-m|Du bord !",
            "narrateur|L'arrosoir verse trop court, sur le mur.",
            "narrateur|Les feuilles restent sèches, là-haut.",
            "enfant-m|Le vert n'arrive pas.",
            "maman|La caisse dort près du mur.",
            "papa|Tu fais quoi, alors ?",
        ],
    },
    (3, 3): {
        "sons": "oiseau,fenetre",
        "emphasis": "fenêtre",
        "passage": [
            "narrateur|Sous le pot, le torchon pend, trop court.",
            "narrateur|Là-haut, le basilic sent le poivre.",
            "enfant-m|J'essuie le bord, d'ici ?",
            "papa|À gauche du.",
            "narrateur|Papa s'arrête, la bouche ouverte.",
            "enfant-m|Du bord !",
            "narrateur|Le tissu n'atteint pas les feuilles.",
            "narrateur|Nino saute, et rien ne change.",
            "enfant-m|C'est trop haut, papa.",
            "maman|La caisse dort près du mur.",
            "papa|Tu fais quoi, alors ?",
        ],
    },
}

T3_LABS = {
    1: ("le crochet", "le torchon", "le petit bois"),
    2: ("le pas de côté", "les deux mains", "le banc"),
    3: ("le pot du bas", "le tabouret", "les bras de papa"),
}

T3_CHOICE = {
    1: [
        "narrateur|Sur la pompe, la suite manque.",
        "papa|Le crochet, le torchon, ou le bois ?",
    ],
    2: [
        "narrateur|Près du thym, le mot n'est pas fini.",
        "maman|Le pas, les mains, ou le banc ?",
    ],
    3: [
        "narrateur|Sous la fenêtre, le haut attend.",
        "papa|Le pot du bas, le tabouret, ou mes bras ?",
    ],
}

T3_SONS = {
    (1, 1): "crochet,eau",
    (1, 2): "tissu,pompe",
    (1, 3): "bois,goutte",
    (2, 1): "pas,abeilles",
    (2, 2): "mains,thym",
    (2, 3): "banc,pierre",
    (3, 1): "pot,terre",
    (3, 2): "tabouret,bois",
    (3, 3): "bras,basilic",
}

T3_EMPH = {
    1: {1: "crochet", 2: "torchon", 3: "petit bois"},
    2: {1: "pas de côté", 2: "deux mains", 3: "banc"},
    3: {1: "pot du bas", 2: "tabouret", 3: "bras"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|Le crochet, là.",
        "narrateur|Ils pendent le seau rouge, sans parler.",
        "papa|Sous le.",
        "narrateur|Nino garde la bouche fermée.",
        "papa|Sous le bec.",
        "enfant-m|Je vois l'eau !",
        "narrateur|Le seau rouge reste contre la jambe.",
        "maman|La phrase est arrivée, toute seule.",
        "papa|Merci, Nino.",
    ],
    (1, 1, 2): [
        "enfant-m|Le torchon, autour.",
        "papa|Sur le manche, sans frotter trop.",
        "narrateur|Le grincement tombe, puis se tait.",
        "papa|Sous le.",
        "narrateur|Nino ne dit rien.",
        "papa|Sous le bec, maintenant.",
        "narrateur|Le seau rouge reste contre la jambe.",
        "maman|Le fer a laissé le mot.",
        "papa|Tu as écouté, tout près.",
    ],
    (1, 1, 3): [
        "enfant-m|Le petit bois, dessous.",
        "papa|Sous le bras de la pompe.",
        "narrateur|Le bois cale le fer, tout net.",
        "papa|La goutte.",
        "narrateur|Nino garde sa bouche fermée.",
        "papa|La goutte va venir.",
        "enfant-m|Elle vient !",
        "narrateur|Le seau rouge reste contre la jambe.",
        "maman|Tu n'as pas parlé trop tôt.",
    ],
    (1, 2, 1): [
        "enfant-m|On recule.",
        "narrateur|Ils s'éloignent des abeilles, un pas.",
        "papa|Près des.",
        "narrateur|Nino attend, les lèvres fermées.",
        "papa|Près des pots, le petit.",
        "enfant-m|Je l'entends, maintenant.",
        "narrateur|Le seau rouge reste contre la jambe.",
        "maman|Le mot est venu, tout seul.",
        "papa|Tu as laissé la fin.",
    ],
    (1, 2, 2): [
        "enfant-m|Mes mains, ici.",
        "papa|En creux, tout près des oreilles.",
        "narrateur|Le bourdonnement devient un peu loin.",
        "maman|Près des.",
        "narrateur|Nino attend, les lèvres fermées.",
        "maman|Près des feuilles.",
        "narrateur|Le seau rouge reste contre la jambe.",
        "papa|On a écouté ensemble.",
        "maman|La suite a eu sa place.",
    ],
    (1, 2, 3): [
        "enfant-m|Le banc, là.",
        "papa|On s'assoit, sur la pierre chaude.",
        "narrateur|La pierre tient leurs deux ombres.",
        "maman|Le petit pot.",
        "narrateur|Nino tourne la tête, sans parler.",
        "enfant-m|Je le vois, contre le thym.",
        "narrateur|Le seau rouge reste contre la jambe.",
        "papa|Le banc a tenu le mot.",
        "maman|On a regardé ensemble.",
    ],
    (1, 3, 1): [
        "enfant-m|Je dis rien.",
        "narrateur|Nino baisse les yeux, vers le mur.",
        "papa|Pas le grand.",
        "enfant-m|Le petit.",
        "narrateur|Papa tend le bras, tout bas.",
        "narrateur|Un pot de basilic penche, tout bas.",
        "narrateur|Le seau rouge reste contre la jambe.",
        "maman|Le mot a fini sa route.",
        "papa|Merci d'avoir écouté, Nino.",
    ],
    (1, 3, 2): [
        "enfant-m|Le tabouret, dessous.",
        "papa|Je le tiens, à ta hauteur.",
        "narrateur|Nino monte, un pied, sans crier.",
        "papa|À gauche du.",
        "narrateur|Nino attend, un pied en l'air.",
        "papa|À gauche du bord.",
        "narrateur|Le seau rouge reste contre la jambe.",
        "maman|Tu as laissé le mot monter.",
        "papa|Le bois a tenu tes pieds.",
    ],
    (1, 3, 3): [
        "enfant-m|Tes bras, papa.",
        "papa|Viens, tout contre moi.",
        "narrateur|Nino s'élève, le nez au basilic.",
        "papa|Le petit pot, tout près du bord.",
        "enfant-m|Je le vois !",
        "narrateur|Les feuilles touchent sa joue, tièdes.",
        "narrateur|Le seau rouge reste contre la jambe.",
        "maman|Tes bras ont fini la phrase.",
        "papa|Chacun a fait sa part.",
    ],
    (2, 1, 1): [
        "enfant-m|Le crochet, pour le vert.",
        "narrateur|Ils pendent l'arrosoir, par l'anse.",
        "papa|Sous le.",
        "narrateur|Nino serre les lèvres, sans deviner.",
        "papa|Sous le bec.",
        "enfant-m|Le vert se remplit !",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "maman|Le mot a suivi l'anse.",
        "papa|Merci, Nino.",
    ],
    (2, 1, 2): [
        "enfant-m|Le torchon, sur le fer.",
        "papa|Autour du manche, sans trop serrer.",
        "narrateur|Le grincement s'éteint, comme une voix.",
        "papa|Sous le.",
        "narrateur|Nino tient le bec, sans parler.",
        "papa|Sous le bec, maintenant.",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "maman|Le fer a rendu le mot.",
        "papa|Tu as tenu le bec, tout près.",
    ],
    (2, 1, 3): [
        "enfant-m|Le petit bois, sous le bras.",
        "papa|Pour caler, sans bouger le fer.",
        "narrateur|Le bois tient, et le fer se tait.",
        "papa|La goutte.",
        "narrateur|Nino ouvre les yeux, pas la bouche.",
        "papa|La goutte va venir.",
        "enfant-m|Elle glisse dans le bec !",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "maman|Tu as laissé le bois parler.",
    ],
    (2, 2, 1): [
        "enfant-m|Un pas, loin des abeilles.",
        "narrateur|L'arrosoir recule, le bec vers le bas.",
        "papa|Près des.",
        "narrateur|Nino compte un pas, sans parler.",
        "papa|Près des pots, le petit.",
        "enfant-m|Le vert va là.",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "maman|Loin du bourdon, le mot est venu.",
        "papa|Tu as reculé, puis écouté.",
    ],
    (2, 2, 2): [
        "enfant-m|Mes deux mains, en creux.",
        "maman|Près des oreilles, comme deux coquilles.",
        "narrateur|Le bourdon s'éloigne, un peu.",
        "maman|Près des.",
        "narrateur|Nino reste ainsi, sans couper.",
        "maman|Près des feuilles.",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "papa|Tes mains ont fait un abri.",
        "maman|La suite a passé.",
    ],
    (2, 2, 3): [
        "enfant-m|Sur le banc, avec le vert.",
        "papa|La pierre est chaude, assieds-toi.",
        "narrateur|L'arrosoir repose entre ses genoux.",
        "maman|Le petit pot.",
        "narrateur|Nino suit son doigt, sans parler.",
        "enfant-m|Contre le thym, je le vois.",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "papa|Le banc a tenu le bec.",
        "maman|On a vu le petit, ensemble.",
    ],
    (2, 3, 1): [
        "enfant-m|Je regarde en bas.",
        "narrateur|L'arrosoir reste au sol, le bec bas.",
        "papa|Pas le grand.",
        "enfant-m|Le petit.",
        "narrateur|Papa montre un pot, tout bas.",
        "narrateur|Le basilic du bas penche, vert.",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "maman|Le mot est descendu avec tes yeux.",
        "papa|Merci d'avoir regardé, Nino.",
    ],
    (2, 3, 2): [
        "enfant-m|Le tabouret, pour le bec.",
        "papa|Je le tiens, monte un pied.",
        "narrateur|Nino monte, le bec au bord.",
        "papa|À gauche du.",
        "narrateur|Nino tient le bec, sans verser.",
        "papa|À gauche du bord.",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "maman|Le bec a attendu le mot.",
        "papa|Le bois a porté le vert.",
    ],
    (2, 3, 3): [
        "enfant-m|Tes bras, pour le vert.",
        "papa|Viens, l'arrosoir contre nous.",
        "narrateur|Nino s'élève, le bec vers les feuilles.",
        "papa|Le petit pot, tout près du bord.",
        "enfant-m|Le bec touche, presque !",
        "narrateur|Les feuilles frôlent le métal, tièdes.",
        "narrateur|L'arrosoir attend une dernière goutte.",
        "maman|Tes bras ont porté le mot.",
        "papa|Le vert a trouvé sa hauteur.",
    ],
    (3, 1, 1): [
        "enfant-m|Le crochet, et le tissu.",
        "narrateur|Ils pendent le seau, le torchon reste.",
        "papa|Sous le.",
        "narrateur|Nino frotte le fer, sans parler.",
        "papa|Sous le bec.",
        "enfant-m|Le tissu a laissé le mot !",
        "narrateur|Le torchon dort contre sa poche.",
        "maman|Le savon a rendu le fer silencieux.",
        "papa|Merci, Nino.",
    ],
    (3, 1, 2): [
        "enfant-m|Le torchon, autour du manche.",
        "papa|Doucement, pour taire le fer.",
        "narrateur|Le tissu étouffe le grincement, net.",
        "papa|Sous le.",
        "narrateur|Nino tient le tissu, sans couper.",
        "papa|Sous le bec, maintenant.",
        "narrateur|Le torchon dort contre sa poche.",
        "maman|Le linge a ouvert le mot.",
        "papa|Tu as essuyé, puis écouté.",
    ],
    (3, 1, 3): [
        "enfant-m|Le petit bois, et le tissu.",
        "papa|Le bois cale, le torchon essuie.",
        "narrateur|Le fer se tait, tout net.",
        "papa|La goutte.",
        "narrateur|Nino pose le tissu, bouche fermée.",
        "papa|La goutte va venir.",
        "enfant-m|Elle glisse sur le savon !",
        "narrateur|Le torchon dort contre sa poche.",
        "maman|Le bois et le linge ont parlé.",
    ],
    (3, 2, 1): [
        "enfant-m|Un pas, le torchon à la main.",
        "narrateur|Ils reculent, le tissu pend, propre.",
        "papa|Près des.",
        "narrateur|Nino n'essuie rien : il écoute.",
        "papa|Près des pots, le petit.",
        "enfant-m|Je peux essuyer celui-là.",
        "narrateur|Le torchon dort contre sa poche.",
        "maman|Loin des abeilles, le mot est venu.",
        "papa|Tu as reculé, le linge prêt.",
    ],
    (3, 2, 2): [
        "enfant-m|Mes mains, et le torchon.",
        "maman|Une main écoute, l'autre tient le linge.",
        "narrateur|Le bourdon s'éloigne, un peu.",
        "maman|Près des.",
        "narrateur|Nino ne frotte pas trop tôt.",
        "maman|Près des feuilles.",
        "narrateur|Le torchon dort contre sa poche.",
        "papa|Tes mains ont deux métiers.",
        "maman|Écouter d'abord, essuyer après.",
    ],
    (3, 2, 3): [
        "enfant-m|Le banc, le torchon sur les genoux.",
        "papa|On s'assoit, le thym est là.",
        "narrateur|Le tissu attend, plié, sans bouger.",
        "maman|Le petit pot.",
        "narrateur|Nino lève le torchon, après le mot.",
        "enfant-m|Je l'essuie, contre le thym.",
        "narrateur|Le torchon dort contre sa poche.",
        "papa|Le banc a gardé le linge.",
        "maman|Le mot d'abord, le tissu ensuite.",
    ],
    (3, 3, 1): [
        "enfant-m|Je dis rien, le torchon reste.",
        "narrateur|Nino baisse les yeux, le linge au poing.",
        "papa|Pas le grand.",
        "enfant-m|Le petit.",
        "narrateur|Papa montre, Nino essuie le petit.",
        "narrateur|Un pot de basilic penche, tout bas.",
        "narrateur|Le torchon dort contre sa poche.",
        "maman|Le linge a suivi le mot, pas avant.",
        "papa|Merci d'avoir écouté, Nino.",
    ],
    (3, 3, 2): [
        "enfant-m|Le tabouret, le torchon avec moi.",
        "papa|Je le tiens, monte, le linge prêt.",
        "narrateur|Nino monte, le tissu au bord.",
        "papa|À gauche du.",
        "narrateur|Nino n'essuie pas trop tôt.",
        "papa|À gauche du bord.",
        "narrateur|Le torchon dort contre sa poche.",
        "maman|Le linge a attendu le mot, en haut.",
        "papa|Le bois a porté le tissu.",
    ],
    (3, 3, 3): [
        "enfant-m|Tes bras, et le torchon.",
        "papa|Viens, le linge entre nous.",
        "narrateur|Nino s'élève, le tissu vers les feuilles.",
        "papa|Le petit pot, tout près du bord.",
        "enfant-m|J'essuie, maintenant !",
        "narrateur|Les feuilles touchent le linge, tièdes.",
        "narrateur|Le torchon dort contre sa poche.",
        "maman|Tes bras ont porté le mot, et le linge.",
        "papa|Le basilic a son tissu, propre.",
    ],
}

END_SONS = {1: "goutte,fer", 2: "thym,pierre", 3: "basilic,fenetre"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|L'eau tombe dans le seau, un petit clic.",
        "enfant-m|Elle est là !",
        "papa|Vers la fenêtre, tout droit.",
        "maman|Le basilic va boire, Nino.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Une goutte sèche sur le fer, tiède.",
    ],
    (1, 1, 2): [
        "narrateur|Le seau se remplit, sous le bec silencieux.",
        "enfant-m|J'ai tenu le manche, d'abord.",
        "papa|Puis le mot est venu.",
        "maman|Venez, la soupe sent.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Un fil de fer reste tiède, contre le seau.",
    ],
    (1, 1, 3): [
        "narrateur|Sous le bois, l'eau tient, nette.",
        "enfant-m|On a calé, papa.",
        "papa|Le bras gardera son ombre.",
        "maman|Tiens bien le seau, Nino.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Une poussière s'envole du manche, puis retombe.",
    ],
    (1, 2, 1): [
        "narrateur|Loin des abeilles, le pot était là.",
        "enfant-m|Tu as fini, papa.",
        "papa|Oui, le mot était long.",
        "maman|Tu as reculé, un pas.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Une terre sèche au bord du seau.",
    ],
    (1, 2, 2): [
        "narrateur|Dans le creux, le mot a parlé.",
        "enfant-m|J'ai écouté, tout contre.",
        "papa|Tes mains étaient à la bonne place.",
        "maman|La soupe t'attend.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Une poussière reste sur le thym, fine.",
    ],
    (1, 2, 3): [
        "narrateur|Sur le banc, le pot penche, vert.",
        "enfant-m|Je l'ai vu, contre le thym.",
        "papa|La pierre a gardé l'ombre.",
        "maman|Verse après le mot, Nino.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Sur le banc, une ombre ronde reste, seule.",
    ],
    (1, 3, 1): [
        "narrateur|Tout en bas, le basilic brille.",
        "enfant-m|Tu as dit petit, à la fin.",
        "papa|Merci d'avoir écouté, Nino.",
        "maman|Un peu de soupe, après l'eau.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|La fenêtre reprend un carreau, net.",
    ],
    (1, 3, 2): [
        "narrateur|Sur le tabouret, Nino a vu le bord.",
        "enfant-m|Le mot est monté avec moi.",
        "papa|Je remporte le tabouret, plus tard.",
        "maman|Essuie tes chaussures, Nino.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Les deux marches se taisent, l'une après l'autre.",
    ],
    (1, 3, 3): [
        "narrateur|Dans les bras de papa, le pot était là.",
        "enfant-m|On a versé, tout haut.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        "narrateur|Le seau rouge tient l'eau, tout droit.",
        "narrateur|Une goutte claque, puis le fer se tait.",
    ],
    (2, 1, 1): [
        "narrateur|L'eau glisse dans l'arrosoir, au crochet.",
        "enfant-m|Le vert est lourd, maintenant.",
        "papa|Vers la fenêtre, le bec devant.",
        "maman|Le basilic va boire, Nino.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|Le bec de l'arrosoir garde une perle.",
    ],
    (2, 1, 2): [
        "narrateur|Sous le torchon, l'eau entre dans le vert.",
        "enfant-m|Le fer s'est tu, papa.",
        "papa|Puis le bec a pris sa goutte.",
        "maman|Venez, ça sent la soupe.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|L'arrosoir penche, une goutte au bec.",
    ],
    (2, 1, 3): [
        "narrateur|Le bois tient, l'eau remplit le vert.",
        "enfant-m|Le bec n'a plus bougé.",
        "papa|Le bras de la pompe reste calé.",
        "maman|Porte l'arrosoir, Nino.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|Le bois sous le bras reste mouillé.",
    ],
    (2, 2, 1): [
        "narrateur|Loin du bourdon, Nino verse au petit pot.",
        "enfant-m|Le vert a trouvé le bon.",
        "papa|Le mot était : le petit.",
        "maman|Tu as reculé, puis versé.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|Une abeille passe, loin du thym.",
    ],
    (2, 2, 2): [
        "narrateur|Les mains en creux, l'eau part au bon endroit.",
        "enfant-m|Près des feuilles, j'ai entendu.",
        "papa|Tes oreilles ont fait le chemin.",
        "maman|La soupe t'attend, après le vert.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|L'arrosoir laisse un rond d'eau, au pied.",
    ],
    (2, 2, 3): [
        "narrateur|Du banc, le bec verse contre le thym.",
        "enfant-m|Le petit pot boit, je vois.",
        "papa|La pierre a tenu le vert.",
        "maman|On rentre, l'arrosoir vide.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|La pierre du banc reste chaude, vide.",
    ],
    (2, 3, 1): [
        "narrateur|En bas, le bec touche le petit basilic.",
        "enfant-m|Pas le grand, celui-là.",
        "papa|Merci d'avoir regardé, Nino.",
        "maman|Un peu d'eau, un peu de soupe.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|Le petit pot brille, tout bas.",
    ],
    (2, 3, 2): [
        "narrateur|Du tabouret, le bec atteint le bord.",
        "enfant-m|À gauche, comme tu as dit.",
        "papa|Je remporte le bois, plus tard.",
        "maman|Essuie tes chaussures, Nino.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|Le tabouret rentre, un pied qui frotte.",
    ],
    (2, 3, 3): [
        "narrateur|Dans les bras, le bec trouve les feuilles.",
        "enfant-m|On verse, tout haut, tout près.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut a pris sa goutte.",
        "narrateur|L'arrosoir serre le bec, tout net.",
        "narrateur|Les feuilles du basilic touchent l'air.",
    ],
    (3, 1, 1): [
        "narrateur|Au crochet, l'eau tombe, le torchon propre.",
        "enfant-m|Le savon a laissé le fer.",
        "papa|Vers la fenêtre, le seau plein.",
        "maman|Le basilic va boire, Nino.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Le torchon sèche au soleil, sur la pierre.",
    ],
    (3, 1, 2): [
        "narrateur|Le manche est muet, l'eau entre.",
        "enfant-m|Le linge a tué le grincement.",
        "papa|Puis le mot a suivi.",
        "maman|Venez, la soupe est prête.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Un coin de tissu reste accroché au bois.",
    ],
    (3, 1, 3): [
        "narrateur|Le bois et le linge tiennent l'eau.",
        "enfant-m|Deux choses, un mot.",
        "papa|Le fer garde son ombre, calé.",
        "maman|Porte le seau, Nino.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Le torchon a pris une poussière de thym.",
    ],
    (3, 2, 1): [
        "narrateur|Loin des abeilles, Nino essuie le petit pot.",
        "enfant-m|Le linge a suivi le mot.",
        "papa|Le petit, près des pots.",
        "maman|Tu as reculé, le tissu prêt.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Le tissu pend, un peu vert de feuille.",
    ],
    (3, 2, 2): [
        "narrateur|Une main écoute, l'autre essuie après.",
        "enfant-m|Près des feuilles, j'ai frotté.",
        "papa|Tes deux métiers ont marché.",
        "maman|La soupe, après le linge.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Le torchon reste plié sur le banc.",
    ],
    (3, 2, 3): [
        "narrateur|Du banc, le torchon essuie le petit pot.",
        "enfant-m|Contre le thym, il brille.",
        "papa|La pierre a tenu le linge.",
        "maman|On rentre, le tissu plié.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Sur le bord, le torchon essuie le petit pot.",
    ],
    (3, 3, 1): [
        "narrateur|En bas, le linge suit le petit basilic.",
        "enfant-m|Pas le grand, j'ai essuyé celui-là.",
        "papa|Merci d'avoir écouté, Nino.",
        "maman|Un peu d'eau, un peu de soupe.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Le torchon descend du tabouret, plié.",
    ],
    (3, 3, 2): [
        "narrateur|Du tabouret, le linge atteint le bord.",
        "enfant-m|À gauche, comme tu as dit.",
        "papa|Je remporte le bois, plus tard.",
        "maman|Essuie tes chaussures, Nino.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Le torchon rentre, sentant le basilic.",
    ],
    (3, 3, 3): [
        "narrateur|Dans les bras, le linge touche les feuilles.",
        "enfant-m|On essuie, tout haut, tout près.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut a pris son tissu, propre.",
        "narrateur|Le torchon sent le savon du fer.",
        "narrateur|Une abeille passe, puis la pompe se tait.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "pompe,goutte"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("le seau", "l'arrosoir", "le torchon")},
    )

    for a in (1, 2, 3):
        t1 = T1[a]
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]}
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"],
            t1["question"],
            "clue",
            "",
            {"emphasis": t1["emphasis"], "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["emphasis"]}
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"],
            [
                f"narrateur|{t1['voy']}",
                "narrateur|La pompe grince trop fort.",
                "narrateur|Le muret a trop d'abeilles.",
                "narrateur|La fenêtre est trop haute.",
                "papa|Nino, tu vas où ?",
            ],
            "choice",
            "",
            {"fields": t3lab("la pompe", "le muret", "la fenêtre")},
        )
        for b in (1, 2, 3):
            t2 = T2[(a, b)]
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]}
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"],
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf],
                    T3[(a, b, c)],
                    "resolution",
                    T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    ENDINGS[(a, b, c)],
                    "ending",
                    END_SONS[b],
                    {"emphasis": T3_EMPH[b][c]},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = FIL
    story["title"] = TITLE
    story["characters"] = CHARS
    story["setting"] = SETTING
    story["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]

    check(SID, story["age_band"], story["chunks"])

    blob = "\n".join(c["script"] for c in story["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in story["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "il faut attendre",
        "laisser le temps",
        "attendre la fin",
        "noé",
        "noe ",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "biscuit",
        "gâteau",
        "cheval",
        "moulinet",
        "loup de carton",
        "dans le salon",
        "joue au salon",
        "à la ferme",
        "veau",
        "tout doux",
        "tout calme",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    n_enc = len(re.findall(r"\bencore\b", blob))
    n_dej = len(re.findall(r"\bd[ée]jà\b", blob))
    if n_enc > 0 or n_dej > 0:
        raise SystemExit(f"{SID} tics encore={n_enc} déjà={n_dej}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3s = [c["text"] for c in story["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    for c in story["chunks"]:
        if not str(c.get("text_ssml") or "").startswith("<speak>"):
            raise SystemExit(f"{c['chunk_id']} SSML manquant")
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")
        if "arc=" not in (c.get("notes") or ""):
            raise SystemExit(f"{c['chunk_id']} notes manquantes")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-062 — Le seau rouge de Nino, à la pompe\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.002 — laisser l'autre finir sa phrase (vécue)\n"
        "- **Personnages :** Nino, papa, maman\n"
        "- **Lieu :** la cour : pompe, muret au thym, fenêtre du basilic\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte pend au bec de la pompe. Nino veut remplir son seau rouge "
        "**maintenant** et donner à boire au basilic. Papa commence : "
        "« On met le seau sous le… » Nino coupe : « Bec ! » Le seau tape de travers. "
        "Rien ne tombe. Il prend le seau, l'arrosoir ou le torchon ; la pompe grince, "
        "les abeilles couvrent, ou la fenêtre est trop haute ; une action change l'écoute "
        "(crochet, torchon, petit bois ; pas, mains, banc ; pot du bas, tabouret, bras). "
        "Papa finit. L'eau tombe. Le basilic boit.\n\n"
        "## Vécu\n\n"
        "Nino veut l'eau **maintenant**. Il parle à la place de papa. "
        "Silence, mot perdu, seau de travers. Chaque choix change l'obstacle et le climax. "
        "La leçon se voit : couper donne la pierre mouillée ; laisser finir donne le bec, "
        "les pots, les feuilles, le petit, le bord. "
        "Fin : seau / arrosoir / torchon + basilic, image unique du chemin "
        "(fer, thym, carreau, perle, banc, linge).\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan ferme / Tom / bac / toboggan / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (seau tenu). Question d'adulte. Un « en ce moment ».\n"
        "- Autre récit que DIF-018 (biscuits), DIF-028 (gâteau), DIF-038 (cheval), "
        "DIF-046 (moulinet), DIF-054 (loup de carton), DIF-067 (puits).\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {min(counts)} à {max(counts)} mots par chemin (moyenne {sum(counts)//len(counts)})\n"
        "- `text` = `script` collé ; graphe inchangé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
