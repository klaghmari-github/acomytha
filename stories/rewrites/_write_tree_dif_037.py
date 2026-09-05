#!/usr/bin/env python3
"""TREE-DIF-037 — Le panier d'Aniss et la petite roue de la cour (F-NAR-019, N3, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-037"
N3 = 16
TITLE = "Le panier d'Aniss et la petite roue de la cour"
FIL = (
    "Dans la cour, Aniss veut porter le panier jusqu'à la petite roue, "
    "avant que l'ombre de l'appentis ne cache la vis verte. "
    "Mila veut qu'il crie tire ; Aniss répond avec les mains. "
    "Panier, corde, nappe : les trois partent. "
    "Palier trop étroit, balcon trop venteux, appentis trop haut. "
    "Neuf façons. La vis verte reprend le soleil, enfin."
)
CHARS = "Aniss, Mila, papa, maman"
SETTING = "cour, palier, balcon, appentis"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "vis verte",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_joyeuse; intensite=1; destinataire=enfant; sous_texte=le_panier_veut_monter_à_la_petite_roue; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tend; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "vis verte",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_partent_ensemble; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=Mila_veut_des_mots_Aniss_tend; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "vis verte",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=ils_ne_veulent_pas_la_même_chose; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "vis verte",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=Aniss_tend_Mila_attend_le_panier_monte; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "vis verte",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_vis_verte_reprend_le_soleil; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
    "narrateur|La cour sent le pain chaud, et les dalles.",
    "narrateur|Un pigeon passe, trop bas, au-dessus du mur.",
    "narrateur|Son ombre glisse, ronde, sur les carreaux.",
    "papa|Le goûter est prêt, Aniss.",
    "maman|La nappe a des miettes, dans le panier.",
    "narrateur|La petite roue de la cour pend, trop haute.",
    "narrateur|Aniss lève les yeux : une vis verte brille sur le bois.",
    "enfant-m|Elle tient la roue, contre la corde.",
    "papa|Cette vis, tu l'as vue, là-haut.",
    "narrateur|En ce moment, Aniss serre l'osier contre sa chemise.",
    "enfant-m|Je le porte jusqu'à la petite roue.",
    "maman|Avant que l'ombre de l'appentis la cache.",
    "narrateur|Les sandales de Mila tapent le palier, trop vite.",
    "copine|Dis tire, Aniss !",
    "narrateur|Aniss tire trop fort, trop tôt.",
    "narrateur|Le panier penche, une miette tombe.",
    "enfant-m|Il ne passe pas.",
    "narrateur|Le sourire d'Aniss disparaît, un instant.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|On prépare, puis on monte.",
    "narrateur|Papa s'accroupit, à la hauteur d'Aniss.",
    "papa|Merci, tu as tenu l'osier, sans crier.",
    "maman|La corde et la nappe voyagent aussi.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près des pieds.",
    "narrateur|Le panier, la corde, la nappe.",
    "papa|Tu prends quoi d'abord, Aniss ?",
]

T1 = {
    1: {
        "lab": "le panier",
        "sons": "osier,pain",
        "emphasis": "panier",
        "passage": [
            "narrateur|Aniss prend d'abord le panier d'osier.",
            "enfant-m|Il sent le pain.",
            "papa|L'osier est un peu rêche, contre les doigts.",
            "narrateur|Il le tend vers Mila, tout près.",
            "copine|Dis goûter !",
            "narrateur|Aniss ouvre la bouche, puis la referme.",
            "narrateur|Il pose deux doigts sur le bord.",
            "enfant-m|Pas trop vite.",
            "maman|La corde et la nappe voyagent aussi.",
            "narrateur|Papa glisse le tout contre l'osier.",
            "copine|Aniss, on court ?",
            "narrateur|Aniss hoche la tête, un peu.",
            "papa|Le panier d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Aniss a tendu le panier, tout près.",
            "maman|Il tend quoi, à Mila ?",
        ],
        "qfields": {
            "expected_answer": "panier",
            "accepted_examples": "panier | le panier | l'osier | osier | tendre",
            "retry_prompt": "Il tend le panier. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde le panier contre lui.",
            "copine|Il est à toi, un moment.",
            "narrateur|Mila attend, les mains ouvertes.",
            "narrateur|Un tic se fait, minuscule, en haut.",
            "maman|La vis verte est tiède, maintenant.",
            "papa|On envoie le goûter où ?",
            "copine|Vers le palier, peut-être.",
            "narrateur|La corde et la nappe tapent l'osier, à chaque pas.",
        ],
    },
    2: {
        "lab": "la corde",
        "sons": "corde,roue",
        "emphasis": "corde",
        "passage": [
            "narrateur|Aniss prend d'abord la corde rêche.",
            "enfant-m|Elle gratte un peu, contre le pouce.",
            "maman|La petite roue attend, trop haute.",
            "narrateur|Il tend le bout vers Mila.",
            "copine|Dis tire !",
            "narrateur|Aniss enroule un tour, sans un mot.",
            "narrateur|La vis verte écoute la corde, en haut.",
            "papa|Le panier et la nappe voyagent aussi.",
            "narrateur|Maman les pose contre l'osier.",
            "copine|Aniss, tu viens ?",
            "narrateur|Aniss lève la corde, tout bas.",
            "enfant-m|Pas trop vite.",
            "maman|La corde d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Aniss a tendu la corde, tout près.",
            "papa|Il tend quoi, à Mila ?",
        ],
        "qfields": {
            "expected_answer": "corde",
            "accepted_examples": "corde | la corde | la roue | tendre",
            "retry_prompt": "Il tend la corde. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde la corde contre sa jambe.",
            "copine|Elle est à toi, un moment.",
            "narrateur|Mila attend, sans répéter.",
            "narrateur|La poussière sent le mur chaud, un peu.",
            "maman|La vis verte écoute la corde.",
            "papa|On envoie le goûter où ?",
            "copine|Vers le balcon, peut-être.",
            "narrateur|Le panier et la nappe tapent l'osier, à chaque pas.",
        ],
    },
    3: {
        "lab": "la nappe",
        "sons": "nappe,tissu",
        "emphasis": "nappe",
        "passage": [
            "narrateur|Aniss prend d'abord la nappe à carreaux.",
            "enfant-m|Elle a des miettes, au pli.",
            "papa|Le tissu sent le tiroir, un peu.",
            "narrateur|Il tend le pliage vers Mila.",
            "copine|Dis nappe !",
            "narrateur|Aniss enroule le pain, sans presser.",
            "narrateur|Le goûter se tient, sans un mot.",
            "maman|Le panier et la corde voyagent aussi.",
            "narrateur|Papa les glisse près des dalles.",
            "copine|Aniss, c'est bon ?",
            "narrateur|Aniss appuie sur le tissu, un peu.",
            "enfant-m|Pas trop vite.",
            "papa|La nappe d'abord, elle tient.",
        ],
        "question": [
            "narrateur|Aniss a tendu la nappe, tout près.",
            "maman|Il tend quoi, à Mila ?",
        ],
        "qfields": {
            "expected_answer": "nappe",
            "accepted_examples": "nappe | la nappe | les carreaux | tendre",
            "retry_prompt": "Il tend la nappe. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss tient la nappe, tout près.",
            "copine|Elle est à toi, un moment.",
            "narrateur|Mila attend, les lèvres fermées.",
            "narrateur|Un carreau bouge un peu, puis s'arrête.",
            "papa|La vis verte écoute le tissu.",
            "maman|On envoie le goûter où ?",
            "copine|Vers l'appentis, tout bas.",
            "narrateur|Le panier et la corde tapent l'osier, à chaque pas.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le panier tape un peu l'osier, à chaque pas.",
        "narrateur|Au palier, un paillasson barre le passage.",
        "narrateur|Au balcon, le linge claque trop fort.",
        "narrateur|Vers l'appentis, une poutre attend trop haut.",
        "papa|On commence où, pour le goûter ?",
    ],
    2: [
        "narrateur|La corde tape un peu la jambe, à chaque pas.",
        "narrateur|Au palier, un paillasson barre le passage.",
        "narrateur|Au balcon, le linge claque trop fort.",
        "narrateur|Vers l'appentis, une poutre attend trop haut.",
        "papa|On commence où, pour le goûter ?",
    ],
    3: [
        "narrateur|La nappe tape un peu le bras, à chaque pas.",
        "narrateur|Au palier, un paillasson barre le passage.",
        "narrateur|Au balcon, le linge claque trop fort.",
        "narrateur|Vers l'appentis, une poutre attend trop haut.",
        "papa|On commence où, pour le goûter ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "paillasson,osier",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|Le panier bute contre le paillasson.",
            "narrateur|Le palier est trop étroit, juste là.",
            "copine|Pousse-le, Aniss !",
            "narrateur|Aniss montre le nœud du tapis, du doigt.",
            "narrateur|Le paillasson reste coincé, sous l'osier.",
            "copine|Dis-moi où !",
            "narrateur|Aniss secoue la tête, un peu.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila se tait, les mains ouvertes.",
            "maman|Il montre, avec le doigt.",
            "papa|Le tapis reste lourd, au milieu.",
            "narrateur|La vis verte s'est cachée derrière le palier.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "corde,paillasson",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|La corde s'accroche au paillasson rêche.",
            "narrateur|Le palier est trop étroit, juste là.",
            "copine|Tire-la, Aniss !",
            "narrateur|Aniss enroule un tour, au lieu de tirer.",
            "narrateur|La corde se tait, puis lâche un peu.",
            "copine|Dis nœud, alors !",
            "narrateur|Aniss montre le bas, du doigt.",
            "enfant-m|Plus bas.",
            "narrateur|Mila se tait, les mains ouvertes.",
            "maman|Il a enroulé, sans crier.",
            "papa|Le tapis reste lourd, au milieu.",
            "narrateur|La vis verte s'est cachée derrière le palier.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "nappe,paillasson",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|La nappe froisse contre le paillasson.",
            "narrateur|Le palier est trop étroit, juste là.",
            "copine|Force, Aniss !",
            "narrateur|Aniss pose le tissu au pied du tapis.",
            "narrateur|Il le fait glisser, le long du bas.",
            "copine|Dis nappe !",
            "narrateur|Aniss appuie sur le pli, un peu.",
            "enfant-m|Elle passe là.",
            "narrateur|Mila se tait, les lèvres fermées.",
            "maman|Le tissu a cherché l'écart.",
            "papa|Le tapis reste lourd, au milieu.",
            "narrateur|La vis verte s'est cachée derrière le palier.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "vent,linge",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|Le panier penche, trop loin, vers le linge.",
            "copine|Le vent est trop grand.",
            "narrateur|Une pince tient une chaussette, trop près.",
            "copine|Tire fort, Aniss !",
            "narrateur|Aniss serre la corde, sans presser.",
            "narrateur|La petite roue grince, puis s'arrête.",
            "enfant-m|Attends le vent.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Elle pose les mains, ouvertes, près de l'osier.",
            "maman|Le linge barre le chemin.",
            "papa|On reste près du mur, tous les deux.",
            "narrateur|La vis verte s'est mise à danser, trop vite.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "corde,pince",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|La corde se coince dans une pince.",
            "copine|Le vent est trop grand.",
            "narrateur|Le rêche s'alourdit, puis tire l'osier.",
            "copine|Tire, Aniss !",
            "narrateur|Aniss enroule la corde, tour après tour.",
            "narrateur|Le linge claque, puis rebondit.",
            "enfant-m|Attends le vent.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Elle pose une main sur la corde, sans tirer.",
            "maman|Le linge barre le chemin.",
            "papa|On reste près du mur, tous les deux.",
            "narrateur|La vis verte s'est mise à danser, trop vite.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "nappe,vent",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|La nappe claque au vent, trop fort.",
            "copine|Le vent est trop grand.",
            "narrateur|Le tissu veut partir avec la chaussette.",
            "copine|Attrape le pli !",
            "narrateur|Aniss cale la nappe contre le mur.",
            "narrateur|Le vent frappe, puis recule un peu.",
            "enfant-m|Elle reste là.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Elle pose un genou, tout près d'Aniss.",
            "maman|Le linge barre le chemin.",
            "papa|On reste près du mur, tous les deux.",
            "narrateur|La vis verte s'est mise à danser, trop vite.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "appentis,gouttiere",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|Le panier accroche la gouttière de l'appentis.",
            "copine|C'est trop haut, Aniss !",
            "narrateur|Mila lève les talons, trop petite.",
            "copine|Dis monte !",
            "narrateur|Aniss pointe le banc, du doigt.",
            "narrateur|Le bois de l'appentis reste trop loin.",
            "enfant-m|Pas trop fort.",
            "narrateur|Mila se tait, les joues chaudes.",
            "narrateur|Elle pose les mains, ouvertes, sous la poutre.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|Le banc dort près du mur.",
            "narrateur|La vis verte s'est éteinte, dans l'ombre.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "corde,poutre",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|La corde frotte la poutre, trop haut.",
            "copine|C'est trop haut, Aniss !",
            "narrateur|Mila lève les talons, trop petite.",
            "copine|Dis nœud !",
            "narrateur|Aniss enroule la corde autour du doigt.",
            "narrateur|Le rêche reste mou, sans prise.",
            "enfant-m|Le banc.",
            "narrateur|Mila se tait, les joues dégonflées.",
            "narrateur|Elle suit le doigt, vers le bois.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|Le banc dort près du mur.",
            "narrateur|La vis verte s'est éteinte, dans l'ombre.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "nappe,bois",
        "emphasis": "vis verte",
        "passage": [
            "narrateur|La nappe se prend dans le bois sec.",
            "copine|C'est trop haut, Aniss !",
            "narrateur|Mila lève les talons, trop petite.",
            "copine|Dis nappe !",
            "narrateur|Aniss pose le tissu sur le banc.",
            "narrateur|Le pli ne bouge plus, trop bas.",
            "enfant-m|Plus haut.",
            "narrateur|Mila se tait, les joues dégonflées.",
            "narrateur|Elle pose les mains autour du tissu.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|Le banc dort près du mur.",
            "narrateur|La vis verte s'est éteinte, dans l'ombre.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("le paillasson", "le panier", "la marche"),
    2: ("le vent", "la corde", "le linge"),
    3: ("le banc", "les mains de Mila", "la poutre"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le paillasson reste fermé, trop lourd.",
        "narrateur|La vis verte s'est perdue derrière le palier.",
        "papa|Le paillasson, le panier, ou la marche ?",
    ],
    2: [
        "narrateur|Le vent tient le linge.",
        "narrateur|La vis verte s'est mise à danser.",
        "maman|Le vent, la corde, ou le linge ?",
    ],
    3: [
        "narrateur|La poutre reste trop haute, trop loin.",
        "narrateur|La vis verte s'est cachée dans l'ombre.",
        "papa|Le banc, les mains, ou la poutre ?",
    ],
}

T3_SONS = {
    (1, 1): "paillasson,tapis",
    (1, 2): "mains,osier",
    (1, 3): "marche,palier",
    (2, 1): "vent,mur",
    (2, 2): "corde,mains",
    (2, 3): "linge,pince",
    (3, 1): "banc,bois",
    (3, 2): "mains,poutre",
    (3, 3): "poutre,appentis",
}

T3_EMPH = {
    1: {1: "paillasson", 2: "panier", 3: "marche"},
    2: {1: "vent", 2: "corde", 3: "linge"},
    3: {1: "banc", 2: "mains", 3: "poutre"},
}

OBJ_LINE = {
    1: "Le panier attend, collé aux doigts.",
    2: "La corde attend, autour de l'osier.",
    3: "La nappe attend, contre le pain.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    obj = OBJ_LINE[a]
    if b == 1 and c == 1:
        wait = {
            1: "Le panier reste près du nœud.",
            2: "La corde reste près du nœud.",
            3: "La nappe reste près du nœud.",
        }[a]
        return [
            "copine|On attend.",
            "narrateur|Aniss tire le paillasson, sans presser.",
            "narrateur|Mila suit le doigt, enfin, un peu.",
            f"narrateur|{wait}",
            "narrateur|Aniss pousse l'osier vers le palier.",
            "narrateur|Ça fait tic, tout net, en haut.",
            "copine|Tic.",
            "narrateur|La vis verte revoit le soleil, ronde.",
            f"narrateur|{obj}",
            "papa|Le tapis n'est plus un bouchon.",
            "enfant-m|Le tapis.",
        ]
    if b == 1 and c == 2:
        hold = {
            1: "Le panier glisse vers les mains de Mila.",
            2: "La corde guide l'osier vers Mila.",
            3: "La nappe suit l'osier vers Mila.",
        }[a]
        return [
            "copine|Pour toi.",
            "narrateur|Mila ouvre les deux mains, tout près.",
            "narrateur|Aniss pose l'osier contre ses paumes.",
            f"narrateur|{hold}",
            "narrateur|Mila vise le bord, Aniss pousse le panier.",
            "copine|Il passe !",
            "narrateur|La vis verte échappe au palier, ronde.",
            f"narrateur|{obj}",
            "maman|Tes mains ont trouvé l'osier.",
            "papa|Il l'a tendu, d'abord.",
            "enfant-m|Tes mains.",
        ]
    if b == 1 and c == 3:
        step = {
            1: "Le panier attend sur la marche.",
            2: "La corde attend sur la marche.",
            3: "La nappe attend sur la marche.",
        }[a]
        return [
            "copine|La marche, Aniss.",
            "narrateur|Aniss pose l'osier dessus, sans un mot.",
            "narrateur|Mila attend, puis suit sa main.",
            f"narrateur|{step}",
            "narrateur|Ils le poussent, ensuite, vers le palier.",
            "copine|Il tient.",
            "narrateur|La vis verte reprend le rai, petite.",
            f"narrateur|{obj}",
            "papa|La marche a gardé le goûter.",
            "maman|Le paillasson peut dormir, plus loin.",
            "enfant-m|La marche.",
        ]
    if b == 2 and c == 1:
        wind = {
            1: "Le panier attend au calme, contre le mur.",
            2: "La corde retombe, enfin, contre le mur.",
            3: "La nappe retombe, enfin, contre le mur.",
        }[a]
        return [
            "copine|On attend le vent.",
            "narrateur|Aniss s'assoit près du mur, sans presser.",
            "narrateur|Mila s'assoit aussi, les genoux contre lui.",
            f"narrateur|{wind}",
            "narrateur|Le vent tombe, une chaussette s'arrête.",
            "copine|Maintenant.",
            "narrateur|La vis verte sèche, ronde, contre le bois.",
            f"narrateur|{obj}",
            "papa|La petite roue ne grince plus.",
            "maman|Vous avez laissé le vent finir.",
            "enfant-m|Le vent.",
        ]
    if b == 2 and c == 2:
        rope = {
            1: "Le panier monte au bout de la corde.",
            2: "La corde part au bout des mains de Mila.",
            3: "La nappe monte au bout de la corde.",
        }[a]
        return [
            "copine|Tes mains, Aniss.",
            "narrateur|Aniss tend la corde, tout près.",
            "narrateur|Mila tire avec lui, sans presser.",
            f"narrateur|{rope}",
            "narrateur|La petite roue traverse comme un pont.",
            "copine|On tient ensemble.",
            "narrateur|La vis verte tremble au bout de la corde.",
            f"narrateur|{obj}",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|Le linge restera après.",
            "enfant-m|On tient.",
        ]
    if b == 2 and c == 3:
        cloth = {
            1: "Le panier passe, dès que le linge part.",
            2: "La corde se libère, dès que le linge part.",
            3: "La nappe se libère, dès que le linge part.",
        }[a]
        return [
            "copine|Le linge, d'abord.",
            "narrateur|Mila tend la pince vers Aniss.",
            "narrateur|Aniss l'ouvre, sans un mot.",
            f"narrateur|{cloth}",
            "narrateur|La chaussette rejoint le panier à linge.",
            "copine|C'est plus simple.",
            "narrateur|La vis verte reste au sec, sur la roue.",
            f"narrateur|{obj}",
            "maman|Le vent garde son souffle, plus loin.",
            "papa|Le linge a laissé la corde.",
            "enfant-m|Au sec.",
        ]
    if b == 3 and c == 1:
        bench = {
            1: "Le panier monte avec le banc.",
            2: "La corde monte avec le banc.",
            3: "La nappe monte avec le banc.",
        }[a]
        return [
            "copine|Le banc, dessous.",
            "papa|Je vous le tends, à votre hauteur.",
            "narrateur|Aniss attend, Mila tient l'osier.",
            f"narrateur|{bench}",
            "narrateur|Aniss accroche, sans un mot.",
            "copine|Ça tient !",
            "narrateur|La vis verte file dans le courant, ronde.",
            f"narrateur|{obj}",
            "papa|Le bois a tenu le banc.",
            "maman|Aniss a poussé, sans crier.",
            "enfant-m|Le banc.",
        ]
    if b == 3 and c == 2:
        hands = {
            1: "Le panier part au bout des mains de Mila.",
            2: "La corde part au bout des mains de Mila.",
            3: "La nappe part au bout des mains de Mila.",
        }[a]
        return [
            "enfant-m|Mila.",
            "narrateur|Aniss pointe ses paumes, du doigt.",
            "narrateur|Mila attend, puis ouvre les mains.",
            f"narrateur|{hands}",
            "narrateur|L'osier glisse, tout net, vers elle.",
            "copine|Je le tiens.",
            "narrateur|La vis verte prend l'air, dans ses paumes.",
            f"narrateur|{obj}",
            "maman|Le haut garde son ombre, plus loin.",
            "papa|Tes mains ont guidé le goûter.",
            "enfant-m|Tes mains.",
        ]
    beam = {
        1: "Le panier suit la poutre, bois après bois.",
        2: "La corde court le long de la poutre, au calme.",
        3: "La nappe tient derrière la poutre, tout droit.",
    }[a]
    return [
        "copine|La poutre, Aniss.",
        "narrateur|Aniss pointe l'ombre, du doigt.",
        "narrateur|Mila attend, puis suit le doigt.",
        f"narrateur|{beam}",
        "narrateur|L'osier prend le chemin de l'ombre.",
        "copine|Il évite la gouttière.",
        "narrateur|La vis verte veille derrière la poutre.",
        f"narrateur|{obj}",
        "papa|Le bois a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
        "enfant-m|La poutre.",
    ]


LAST = {
    (1, 1, 1): "La vis verte s'endort contre le paillasson.",
    (1, 1, 2): "Dans les paumes, la vis verte clignote.",
    (1, 1, 3): "Sur la marche, la vis verte se tait.",
    (1, 2, 1): "Au calme du mur, la vis verte sèche.",
    (1, 2, 2): "Au bout de la corde, la vis verte tremble.",
    (1, 2, 3): "Près du linge, la vis verte se tait.",
    (1, 3, 1): "Sur le banc, la vis verte prend l'air.",
    (1, 3, 2): "Dans les mains de Mila, la vis verte veille.",
    (1, 3, 3): "Le long de la poutre, la vis verte file.",
    (2, 1, 1): "La corde laisse la vis verte au palier.",
    (2, 1, 2): "Les mains de Mila chauffent la vis verte.",
    (2, 1, 3): "La marche tient la vis verte, petite.",
    (2, 2, 1): "Le vent n'a pas pris la vis verte.",
    (2, 2, 2): "La corde tendue montre la vis verte au soleil.",
    (2, 2, 3): "Le linge a sauvé la vis verte, tiède.",
    (2, 3, 1): "Le banc lèche la vis verte, au bois.",
    (2, 3, 2): "Les paumes tiennent la vis verte, droite.",
    (2, 3, 3): "La poutre serre près de la vis verte.",
    (3, 1, 1): "La nappe cale la vis verte au palier.",
    (3, 1, 2): "Le tissu suit la vis verte vers Mila.",
    (3, 1, 3): "La marche pince la vis verte, sans la cacher.",
    (3, 2, 1): "Le mur a séché la vis verte.",
    (3, 2, 2): "La nappe guide la vis verte au-dessus du vent.",
    (3, 2, 3): "Le linge laisse la vis verte au sec.",
    (3, 3, 1): "Le banc pousse la vis verte, hors de l'ombre.",
    (3, 3, 2): "Deux mains s'arrêtent, la vis verte au milieu.",
    (3, 3, 3): "L'osier tremble, la vis verte se tait.",
}

HARD = {
    (1, 1): "Le paillasson a failli garder l'osier.",
    (2, 1): "La corde a failli rester sous le tapis.",
    (3, 1): "La nappe a failli coincer le palier.",
    (1, 2): "Le vent a failli emporter le panier.",
    (2, 2): "La corde a failli partir avec le linge.",
    (3, 2): "La nappe a failli claquer trop fort.",
    (1, 3): "La poutre a failli trop peser.",
    (2, 3): "La corde a failli rester trop haute.",
    (3, 3): "La nappe a failli se prendre dans le bois.",
}

CODA = {
    1: "L'osier garde une miette tiède.",
    2: "La corde garde un peu de poussière chaude.",
    3: "Un carreau de nappe garde une miette.",
}

TRACE = {
    (1, 1): "Une miette tiède reste sur le palier.",
    (1, 2): "Au mur, ça sent le pain, tiède.",
    (1, 3): "Au loin, le pigeon se tait.",
    (2, 1): "Une corde rêche tremble, puis se tait.",
    (2, 2): "Une pince sèche, contre le bois.",
    (2, 3): "Sur les dalles, une ombre mince.",
    (3, 1): "Un carreau de nappe reste tiède, dans la paume.",
    (3, 2): "Un tic de roue s'éteint, tout près.",
    (3, 3): "L'ombre de l'appentis recule, un peu.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    last = LAST[(a, b, c)]
    hard = HARD[(a, b)]
    coda = CODA[a]
    trace = TRACE[(a, c)]
    if b == 1 and c == 1:
        return [
            "narrateur|Le panier pose une miette sur le palier.",
            "enfant-m|Pain.",
            "copine|Il est arrivé.",
            f"narrateur|{hard}",
            "papa|Le paillasson a laissé le passage.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 2:
        return [
            "narrateur|L'osier a contourné le tapis, jusqu'au bout.",
            "copine|Aniss l'a tendu, tout seul.",
            "papa|Tu as tendu, d'abord.",
            f"narrateur|{hard}",
            "maman|Venez, le pain est tiède.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 3:
        return [
            "narrateur|L'osier court jusqu'au palier, tout droit.",
            "copine|On a posé le panier.",
            "papa|La marche a tenu, tout droit.",
            f"narrateur|{hard}",
            "maman|Essuyez vos mains, tout près.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 1:
        return [
            "narrateur|La petite roue glisse, puis s'arrête.",
            "copine|On a attendu le vent.",
            "papa|Le linge n'a plus pris vos bras.",
            f"narrateur|{hard}",
            "maman|Rentrez la pince, après le goûter.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 2:
        return [
            "narrateur|La petite roue tient la corde, tout net.",
            "copine|On tenait, tous les deux.",
            "papa|Je remporte la pince, tout à l'heure.",
            f"narrateur|{hard}",
            "maman|Le pain vous attend.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 3:
        return [
            "narrateur|Les mains d'Aniss laissent la corde monter.",
            "copine|C'était plus facile, là.",
            "papa|Tes bras ont guidé l'osier.",
            f"narrateur|{hard}",
            "maman|Le haut gardera son ombre.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 1:
        return [
            "narrateur|L'osier pose une feuille sèche sur le banc.",
            "copine|On a monté, Aniss.",
            "papa|Le bois n'a pas glissé.",
            f"narrateur|{hard}",
            "maman|Rentrez, le seuil est sec.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 2:
        return [
            "narrateur|Les mains de Mila laissent l'osier poser.",
            "copine|On l'a tenu, tous les deux.",
            "papa|Le haut est resté à sa place.",
            f"narrateur|{hard}",
            "maman|Essuie tes chaussures, Aniss.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    return [
        "narrateur|L'osier suit la poutre, jusqu'à l'ombre.",
        "copine|L'ombre était nette.",
        "papa|Le bois a tenu, tout droit.",
        f"narrateur|{hard}",
        "maman|L'appentis n'a plus rien à dire.",
        f"narrateur|{coda}",
        f"narrateur|{trace}",
        f"narrateur|{last}",
    ]


END_SONS = {1: "pain,palier", 2: "corde,vent", 3: "bois,appentis"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "pigeon,dalles,roue",
        {"emphasis": "vis verte"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le panier", "la corde", "la nappe"), "pause_before": 200},
    )

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], T1[a]["passage"], "action", T1[a]["sons"],
            {"emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], T1[a]["question"], "clue", "",
            {"fields": T1[a]["qfields"], "emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], T1[a]["confirm"], "confirm", T1[a]["sons"],
            {"emphasis": "vis verte"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le palier", "le balcon", "l'appentis"), "pause_before": 200},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b]), "pause_before": 200},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], t3_pass(a, b, c), "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", END_SONS[a],
                    {"emphasis": "vis verte"},
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
        "zoé",
        "zoe",
        "sami",
        "tom ",
        "léa",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui",
        "merle",
        "couleur de miel",
        "j'ai une idée",
        "j'ai compris",
        "mission accomplie",
        "on dirait que notre mission",
        "il faut attendre",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "virgule d'or",
        "croissant de buée",
        "fil blanc",
        "perle de verre",
        "cran en croissant",
        "œillet de cuivre",
        "oeillet de cuivre",
        "virgule de farine",
        "marque fine",
        "ombre en forme de flèche",
        "minuscule symbole",
        "pastille de colle",
        "goutte de cire",
        "larme de bronze",
        "bouton de nacre",
        "nœud de raphia",
        "grain de savon",
        "grain de vanille",
        "grain de son",
        "bouton de lavande",
        "grain doré",
        "brin de safran",
        "anneau de liège",
        "clou à tête ronde",
        "grain d'ambre",
        "anneau de zinc",
        "point de cire",
        "bracelet d'écorce",
        "boucle d'étain",
        "soleil en papier",
        "vestiaire",
        "maîtresse",
        "jardinier",
        "grand-père",
        "camarade",
        "parle peu",
        "cloche",
        "lila",
        "cuisine",
        "la chambre",
        "le jardin",
        "moulin",
        "la grille",
        "caniveau",
        "le porche",
        "jules",
        "locomotive",
        "cuillère",
        "véranda",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "vis verte" not in blob:
        raise SystemExit(f"{SID}: indice vis verte absent")
    if "enfant-m|" not in blob:
        raise SystemExit(f"{SID}: enfant-m absent")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: copine absente")
    if blob.count("merci") > 3:
        raise SystemExit(f"{SID}: merci refrain ×{blob.count('merci')}")

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
        if "vis verte" not in low:
            raise SystemExit(f"fin sans vis verte: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3s = [c["text"] for c in story["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    t2s = [c["text"] for c in story["chunks"] if re.search(r"T0002_P000[123]$", c["chunk_id"])]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")
    if min(counts) < 500:
        raise SystemExit(f"chemins trop courts: {min(counts)}")
    if max(counts) > 780:
        raise SystemExit(f"chemins trop longs: {max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-037 — Le panier d'Aniss et la petite roue de la cour\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — camarade qui parle peu / tendre, attendre "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Aniss, Mila, papa, maman\n"
        "- **Lieu :** cour, palier, balcon, appentis\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un pigeon passe ; son ombre glisse sur les dalles. Aniss lève les yeux : "
        "une vis verte brille sur la petite roue. Il veut porter le panier "
        "jusqu'à la roue avant que l'ombre de l'appentis ne la cache. "
        "Mila veut qu'il crie tire. Aniss tire trop fort : le panier penche. "
        "Sourire parti. Panier, corde, nappe : les trois partent. "
        "Palier (paillasson trop étroit), balcon (linge, vent), appentis (poutre trop haute). "
        "Paillasson, panier, marche ; vent, corde, linge ; banc, mains de Mila, poutre. "
        "La vis verte reprend le soleil, avec une trace.\n\n"
        "## Vécu\n\n"
        "Aniss veut le panier **à la petite roue, maintenant**. Mila ne veut pas "
        "la même chose : elle veut des mots. Première idée : tirer trop vite. "
        "Ça rate. Chaque choix change l'obstacle et le climax (tapis, vent, ombre). "
        "La leçon se voit : Aniss tend, Mila attend, le silence compte. "
        "On ne force pas la parole, on change le geste. "
        "Fin : vis verte + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Zoé / Tom / Léa / Sami / Jules / cuisine-jardin-chambre / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Aniss (`enfant-m`), Mila (`copine`), rythmes distincts, silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique : vis verte (ouverture + climax). "
        "Pas d'ancre / étoile / fil pâle / marque fine / goutte de cire / larme de bronze.\n"
        "- Ouverture inventée : le pigeon, l'ombre sur les dalles, puis la vis verte.\n"
        "- Corps : sourire parti ; envie et inquiétude ; papa s'accroupit.\n"
        "- Merci vécu (ouverture). Question d'adulte. Un « en ce moment ».\n"
        "- Monde ≠ TREE-DIF-061 (pas de moulin, grille, école, caniveau, porche).\n"
        "- Adultes = papa/maman. Pas de maîtresse.\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {min(counts)} à {max(counts)} mots par chemin (moyenne {sum(counts)//len(counts)})\n"
        "- `text` = `script` collé ; graphe inchangé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
