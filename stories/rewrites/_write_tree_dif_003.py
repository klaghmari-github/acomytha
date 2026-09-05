#!/usr/bin/env python3
"""TREE-DIF-003 — Le manteau à pois et les lunettes de Mila (N2, DIF.COR.003, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-003"
N2 = 15
TITLE = "Le manteau à pois et les lunettes de Mila"
FIL = (
    "Après la pluie, la gouttière compte dans la cuisine. "
    "Mila veut le manteau à pois, les lunettes et le seau jusqu'au seuil, "
    "avant la dernière goutte, pour une maison de feuille. "
    "Un éclat de thym colle à un pois. Aniss arrive sans un mot. "
    "Elle propose. Il prend son temps. Le silence répond. "
    "La manche résiste, les lunettes voilent, le seau coince. "
    "Paillasson, pots ou gouttière : trop vite, la coccinelle part. "
    "L'éclat du début montre la place. On le pose, on attend, on dessine. "
    "La maison tient. Ça a failli ne pas arriver."
)
CHARS = "Mila, Aniss, papa, maman"
SETTING = "cuisine puis seuil, après la pluie"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "miel",
    "merle",
    "aujourd'hui,",
    "j'ai compris",
    "mission accomplie",
    "on va apprendre",
    "bon travail",
    "il faut attendre",
    "papa sourit",
    "maman sourit",
    "escargot",
    "manteau vert",
    "manteau jaune",
    "drap à pois",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "éclat de thym",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=mila_propose_aniss_prend_son_temps; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_maison; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_prend; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_l_objet_resiste; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=aniss_se_tait_mila_refuse_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "éclat de thym",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=l_eclat_du_debut_montre_la_place; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "éclat de thym",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_maison_tient_l_eclat_reste; tempo=posé; sourire=léger; respiration=ample",
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


def vet(lines: list[str], where: str = "") -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{where} {n}>{N2}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} fin: {ph}")
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"{where} tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"{where} tic {m.group(0)!r}: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"{where} puces « {tok} »")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""
        out.append(f"{role}|{ph}")
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines, src.get("chunk_id", "?"))
    m = dict(PROFILES[profile])
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


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


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


OPENING = [
    "narrateur|La gouttière compte, goutte après goutte.",
    "narrateur|Mila compte avec elle, dans la cuisine.",
    "narrateur|Ça sent le poireau, et le thym coupé.",
    "narrateur|La casserole frémit, près du thym.",
    "narrateur|Un nuage de soupe cache la vitre.",
    "papa|Je fais un rond, pour voir.",
    "narrateur|Papa essuie, et le seuil apparaît.",
    "narrateur|Le manteau à pois goutte, au crochet.",
    "narrateur|Un éclat de thym colle à un pois.",
    "enfant-f|Il n'était pas là, ce matin.",
    "maman|C'est le thym de la soupe.",
    "narrateur|En ce moment, Mila touche le pois.",
    "enfant-f|Je sors, avant la dernière goutte.",
    "narrateur|Elle veut le manteau, et les lunettes.",
    "narrateur|Le seau attend sous l'évier.",
    "narrateur|Aniss pousse la porte, sans un mot.",
    "narrateur|Il s'arrête, et regarde l'éclat.",
    "enfant-f|On y va, Aniss.",
    "narrateur|Aniss ne dit rien.",
    "papa|Merci, tu as attendu sa voix.",
    "enfant-m|Le thym, moi je le vois.",
]

T1_CHOICE = [
    "narrateur|Près du seuil, trois affaires attendent.",
    "narrateur|Le manteau, les lunettes, le seau.",
    "maman|Qu'est-ce que tu prends d'abord, Mila ?",
]

T1 = {
    1: {
        "lab": "le manteau à pois",
        "sons": "tissu,goutte",
        "emphasis": "manteau à pois",
        "passage": [
            "narrateur|Mila tire le manteau à pois du crochet.",
            "narrateur|Une manche est retournée, trop molle.",
            "enfant-f|J'ai la manche !",
            "enfant-m|Je la tiens.",
            "narrateur|Aniss tend le tissu, sans se presser.",
            "maman|Glisse un bras, puis l'autre.",
            "narrateur|Mila pousse trop vite, et la manche résiste.",
            "enfant-f|Elle ne veut pas.",
            "narrateur|Le sourire de Mila disparaît.",
            "papa|On y va ensemble, d'accord ?",
            "enfant-f|Oui.",
            "narrateur|Elle glisse une feuille sèche, dans la poche.",
            "enfant-f|C'est sa maison.",
            "papa|Les lunettes, et le seau aussi ?",
            "enfant-m|J'apporte le seau.",
            "narrateur|Les pois brillent, un peu mouillés.",
        ],
        "question": [
            "narrateur|Mila a pris le manteau d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | manteau à pois | le manteau à pois | d'abord le manteau",
            "retry_prompt": "Mila prend le manteau d'abord.",
        },
        "confirm": [
            "narrateur|Le manteau reste sur elle, un peu lourd.",
            "enfant-f|La feuille est dans la poche.",
            "maman|Les lunettes tiennent, Mila ?",
            "enfant-f|Oui, sur mon nez.",
            "papa|Le seau, Aniss le tient.",
            "enfant-m|J'ai l'anse.",
            "narrateur|Ils avancent vers le seuil, sans courir.",
            "maman|La gouttière n'a pas fini.",
            "enfant-f|Une maison, avant la dernière goutte.",
            "narrateur|Aniss marche derrière, sans se presser.",
            "narrateur|Un éclat de thym brille, sur un pois.",
        ],
        "voy": "Le manteau à pois frotte le seuil.",
    },
    2: {
        "lab": "les lunettes",
        "sons": "verre,souffle",
        "emphasis": "lunettes",
        "passage": [
            "narrateur|Mila prend les lunettes près du bol.",
            "narrateur|Un peu de buée les rend floues.",
            "enfant-f|Je ne vois plus l'éclat !",
            "papa|Souffle, puis j'essuie.",
            "narrateur|Elle souffle trop fort, trop vite.",
            "narrateur|Les verres restent voilés, tout blancs.",
            "enfant-m|Moi, je souffle plus lent.",
            "narrateur|Aniss attend, puis souffle une fois.",
            "papa|Voilà, je passe le torchon.",
            "narrateur|Les verres redeviennent clairs.",
            "enfant-f|L'éclat de thym, je le revois.",
            "maman|Le manteau, et le seau aussi ?",
            "enfant-f|Oui, on les prend.",
            "narrateur|Elle pose les lunettes, sur son nez.",
            "papa|Elles tiennent bien ?",
            "enfant-f|Oui, papa.",
        ],
        "question": [
            "narrateur|Mila a pris les lunettes d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "lunettes",
            "accepted_examples": "lunettes | les lunettes | d'abord les lunettes | ses lunettes",
            "retry_prompt": "Mila prend les lunettes d'abord.",
        },
        "confirm": [
            "narrateur|Les lunettes restent nettes, sur son nez.",
            "enfant-f|Je vois le seuil, dehors.",
            "papa|Le manteau te tient chaud ?",
            "enfant-f|Oui, il est un peu lourd.",
            "maman|Aniss, tu tiens le seau ?",
            "enfant-m|J'ai l'anse.",
            "narrateur|Ils avancent vers le seuil, sans courir.",
            "papa|La gouttière n'a pas fini.",
            "enfant-f|Une maison, avant la dernière goutte.",
            "narrateur|Aniss marche derrière, sans se presser.",
            "narrateur|Un éclat de thym brille, au bord d'un verre.",
        ],
        "voy": "Les lunettes cherchent le seuil.",
    },
    3: {
        "lab": "le seau",
        "sons": "seau,eau",
        "emphasis": "seau",
        "passage": [
            "narrateur|Mila attrape le seau sous l'évier.",
            "narrateur|Il sonne creux, comme un petit tambour.",
            "enfant-f|Il est coincé !",
            "enfant-m|Je tire, moi.",
            "narrateur|Aniss pose les deux mains, et attend.",
            "narrateur|Mila veut tirer trop fort, trop vite.",
            "papa|Deux mains, et on glisse.",
            "narrateur|Le seau se libère, d'un coup.",
            "enfant-f|C'est l'hôtel.",
            "maman|Une feuille, et une goutte ?",
            "narrateur|Mila pose une feuille sèche, au fond.",
            "papa|Le manteau, et les lunettes aussi ?",
            "enfant-f|Oui, on les prend.",
            "enfant-m|Je porte l'anse.",
            "narrateur|Le seau se balance, puis se tient.",
            "maman|L'hôtel est prêt ?",
            "enfant-f|Oui.",
        ],
        "question": [
            "narrateur|Mila a pris le seau d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "seau",
            "accepted_examples": "seau | le seau | d'abord le seau | l'hôtel | hotel",
            "retry_prompt": "Mila prend le seau d'abord.",
        },
        "confirm": [
            "narrateur|La feuille nage dans sa goutte, au fond.",
            "enfant-f|L'hôtel voyage.",
            "papa|Deux mains sur l'anse, Aniss.",
            "enfant-m|J'ai.",
            "maman|Le manteau te tient, Mila ?",
            "enfant-f|Oui, et les lunettes.",
            "narrateur|Ils avancent vers le seuil, sans courir.",
            "papa|La gouttière n'a pas fini.",
            "enfant-f|Une maison, avant la dernière goutte.",
            "narrateur|Aniss marche derrière, sans se presser.",
            "narrateur|Un éclat de thym brille, au bord du seau.",
        ],
        "voy": "Le seau penche vers le seuil.",
    },
}

T2 = {
    (1, 1): {
        "sons": "paillasson,pas",
        "emphasis": "paillasson",
        "passage": [
            "narrateur|Le manteau à pois frotte le paillasson.",
            "narrateur|Les fibres sont mouillées, trop lourdes.",
            "enfant-f|Elle est dessous, la coccinelle !",
            "narrateur|Mila lève le tapis, trop vite.",
            "narrateur|Une coccinelle fuit, toute petite.",
            "enfant-f|Reviens !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça serre, trop.",
            "papa|Ici, ça n'aime pas le vent.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Aniss ne dit rien, et il pointe.",
            "narrateur|Un éclat de thym brille, dans les fibres.",
            "enfant-f|Pas maintenant.",
            "maman|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "terre,pot",
        "emphasis": "pots",
        "passage": [
            "narrateur|Un pois du manteau accroche une feuille.",
            "narrateur|Les pots de géranium luisent, trop glissants.",
            "enfant-f|Elle est là, entre les pots !",
            "narrateur|Mila penche la poche, trop vite.",
            "narrateur|Un pot bascule, et la terre tombe.",
            "enfant-f|Oh, le pot !",
            "narrateur|La joie de Mila se plie, d'un coup.",
            "narrateur|L'envie et la peur se bousculent.",
            "maman|La terre n'aime pas la course.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "narrateur|Aniss se tait, et montre le bord.",
            "narrateur|Un éclat de thym brille, sur le rebord.",
            "enfant-f|Je ne fonce pas.",
            "papa|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "gouttiere,goutte",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Une goutte tombe du tuyau, sur un pois.",
            "narrateur|La gouttière laisse une goutte, puis plus.",
            "enfant-f|Vite, avant qu'elle se taise !",
            "narrateur|Mila tend la poche, trop haut, trop vite.",
            "narrateur|La goutte rate, et la coccinelle recule.",
            "enfant-f|Je l'ai manquée.",
            "narrateur|Ses joues chauffent, et ses mains tremblent.",
            "papa|Le tuyau est froid, un peu vert.",
            "narrateur|Papa s'accroupit, près du tuyau.",
            "narrateur|Aniss reste immobile, les yeux levés.",
            "narrateur|Un éclat de thym brille, sur le zinc.",
            "enfant-m|Là.",
            "enfant-f|Pas maintenant.",
            "maman|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "paillasson,verre",
        "emphasis": "paillasson",
        "passage": [
            "narrateur|Mila penche les lunettes vers le paillasson.",
            "narrateur|Les fibres deviennent nettes, une par une.",
            "enfant-f|Une petite bosse, là !",
            "narrateur|Elle essuie trop vite, et ça voile.",
            "narrateur|La coccinelle disparaît, dans le tapis.",
            "enfant-f|Je ne vois plus.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Ça tape, dans sa poitrine, trop vite.",
            "papa|Les fibres n'aiment pas le vent.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Aniss ne parle pas, et il pointe.",
            "narrateur|Un éclat de thym brille, entre deux fibres.",
            "enfant-f|Pas maintenant.",
            "maman|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "terre,verre",
        "emphasis": "pots",
        "passage": [
            "narrateur|Mila penche les lunettes entre les pots.",
            "narrateur|La terre des géraniums brille, trop proche.",
            "enfant-f|Un fil, sur la terre !",
            "narrateur|Elle avance le nez, trop vite.",
            "narrateur|Un pot tremble, et un pétale tombe.",
            "enfant-f|Le pot va tomber !",
            "narrateur|Ses épaules se serrent, toutes dures.",
            "maman|Les pots n'aiment pas la course.",
            "narrateur|Maman s'accroupit, entre deux pots.",
            "narrateur|Aniss reste silencieux, et il montre.",
            "narrateur|Un éclat de thym brille, sur le rebord.",
            "enfant-m|Là.",
            "enfant-f|Je ne fonce pas.",
            "papa|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "gouttiere,verre",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Les lunettes attrapent un éclat, tout haut.",
            "narrateur|La gouttière laisse une goutte, trop loin.",
            "enfant-f|Une coccinelle, sur le tuyau !",
            "narrateur|Mila se hausse, trop vite, trop haut.",
            "narrateur|La goutte éclabousse, et l'insecte recule.",
            "enfant-f|Elle part !",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Les pieds restent au sol, d'accord ?",
            "narrateur|Papa s'accroupit, sous le tuyau.",
            "narrateur|Aniss ne bouge pas, et lève un doigt.",
            "narrateur|Un éclat de thym brille, sur le zinc.",
            "enfant-f|Pas maintenant.",
            "maman|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "paillasson,seau",
        "emphasis": "paillasson",
        "passage": [
            "narrateur|Le seau pose un rond d'eau, sur le paillasson.",
            "narrateur|Les fibres boivent, trop vite, trop fort.",
            "enfant-f|L'hôtel, je le pose là !",
            "narrateur|Le seau sonne, trop fort, sur le tapis.",
            "narrateur|La coccinelle fuit, sous une fibre.",
            "enfant-f|Elle a peur du bruit.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Ses mains serrent l'anse, trop.",
            "papa|Le paillasson n'aime pas le tambour.",
            "narrateur|Papa s'accroupit, près du seau.",
            "narrateur|Aniss se tait, et pointe une fibre.",
            "narrateur|Un éclat de thym brille, dans le tapis.",
            "enfant-f|Pas maintenant.",
            "maman|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "terre,seau",
        "emphasis": "pots",
        "passage": [
            "narrateur|Le seau se cale entre deux pots, trop juste.",
            "narrateur|La terre sent le mouillé, trop proche.",
            "enfant-f|L'hôtel attend ici.",
            "narrateur|Mila pousse l'anse, trop vite.",
            "narrateur|Un pot penche, et l'eau verse.",
            "enfant-f|La feuille est mouillée !",
            "narrateur|Ça serre, dans sa poitrine, d'un coup.",
            "maman|Les pots n'aiment pas les coups.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "narrateur|Aniss ne répond pas, et il montre.",
            "narrateur|Un éclat de thym brille, sur le rebord.",
            "enfant-m|Là.",
            "enfant-f|Je ne fonce pas.",
            "papa|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "gouttiere,seau",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Le seau s'arrête sous la gouttière, trop tôt.",
            "narrateur|Le tuyau est froid, un peu vert.",
            "enfant-f|Une goutte, dedans !",
            "narrateur|Mila lève le seau, trop haut, trop vite.",
            "narrateur|La goutte rate le fond, et la coccinelle fuit.",
            "enfant-f|L'hôtel est vide.",
            "narrateur|Ses joues chauffent, et elle baisse l'anse.",
            "papa|Les pieds restent au sol.",
            "narrateur|Papa s'accroupit, sous le tuyau.",
            "narrateur|Aniss reste silencieux, le seau contre lui.",
            "narrateur|Un éclat de thym brille, sur le zinc.",
            "enfant-f|Pas maintenant.",
            "maman|Tu vois comment, Mila ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
}

T2_Q = [
    "narrateur|Devant, le paillasson cache trop.",
    "narrateur|Les pots, eux, glissent.",
    "narrateur|Sous la gouttière, la goutte se tait.",
    "papa|Mila, tu vas où ?",
    "maman|La maison de feuille attend.",
]

T3_CHOICE = {
    1: [
        "narrateur|Le paillasson n'a pas dit son secret.",
        "papa|On le pose, on attend, ou on dessine ?",
    ],
    2: [
        "narrateur|Les pots gardent un secret, tout bas.",
        "maman|On le pose, on attend, ou on dessine ?",
    ],
    3: [
        "narrateur|La gouttière n'a pas fini sa goutte.",
        "papa|On le pose, on attend, ou on dessine ?",
    ],
}

T3_SONS = {
    1: "feuille,paillasson",
    2: "silence,seuil",
    3: "crayon,papier",
}

T3_EMPH = {1: "pose", 2: "attend", 3: "dessine"}

T3 = {
    (1, 1, 1): [
        "enfant-f|On le pose, là.",
        "narrateur|Mila ouvre la poche à pois, tout large.",
        "narrateur|Elle pose la feuille sèche, sur le tapis.",
        "narrateur|Aniss ne parle pas, et pose un doigt.",
        "narrateur|Un éclat de thym brille, près de la feuille.",
        "enfant-m|Ici.",
        "papa|Vous avez posé, sans lever le tapis.",
        "narrateur|Une coccinelle avance, une patte, puis l'autre.",
        "enfant-f|Ta maison est tiède.",
        "narrateur|Pendant ce temps, le manteau reste ouvert.",
        "maman|Tu n'as pas foncé.",
    ],
    (1, 1, 2): [
        "enfant-f|On attend.",
        "narrateur|Mila ouvre un peu la poche, sans bouger.",
        "narrateur|Aniss s'assoit, et il ne dit rien.",
        "narrateur|Le paillasson se tait, fibre après fibre.",
        "narrateur|Un éclat de thym brille, dans le tapis.",
        "enfant-m|Elle vient.",
        "papa|Vous avez laissé le tapis se taire.",
        "narrateur|Une coccinelle sort, toute petite, toute lente.",
        "enfant-f|Si elle veut, elle entre.",
        "narrateur|La poche attend, comme une grotte.",
        "maman|Son silence a compté.",
    ],
    (1, 1, 3): [
        "enfant-f|On dessine, d'abord.",
        "narrateur|Aniss sort un papier, de sa poche.",
        "narrateur|Il dessine un pois, et une feuille.",
        "narrateur|Mila regarde, sans toucher le tapis.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|La maison, c'est ça.",
        "papa|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent la vraie feuille, tout bas.",
        "narrateur|Une coccinelle suit le trait, jusqu'à la poche.",
        "enfant-f|Elle a lu ton dessin.",
        "maman|Le papier a montré le chemin.",
    ],
    (1, 2, 1): [
        "enfant-f|On le pose, entre les pots.",
        "narrateur|Mila ouvre la poche, près du géranium.",
        "narrateur|Elle pose la feuille, comme un toit.",
        "narrateur|Aniss tient le pot, sans le bouger.",
        "narrateur|Un éclat de thym brille, sur le rebord.",
        "enfant-m|Le toit, là.",
        "maman|Vous avez posé, sans basculer.",
        "narrateur|Une coccinelle grimpe la tige, puis la feuille.",
        "enfant-f|Ta maison sent la terre.",
        "narrateur|Un pois touche le pot, tout léger.",
        "papa|Tu n'as pas foncé.",
    ],
    (1, 2, 2): [
        "enfant-f|On attend, entre les pots.",
        "narrateur|Mila reste accroupie, la poche ouverte.",
        "narrateur|Aniss ne dit rien, et regarde la terre.",
        "narrateur|Les géraniums se taisent, feuille après feuille.",
        "narrateur|Un éclat de thym brille, sur le rebord.",
        "enfant-m|Elle monte.",
        "maman|Vous avez laissé la terre se taire.",
        "narrateur|Une coccinelle sort, sous une feuille large.",
        "enfant-f|Si elle veut, elle entre.",
        "narrateur|La poche attend, entre deux pots.",
        "papa|Son silence a compté.",
    ],
    (1, 2, 3): [
        "enfant-f|On dessine le pot, d'abord.",
        "narrateur|Aniss dessine un pot, et un pois.",
        "narrateur|Mila tient le manteau, sans le pencher.",
        "narrateur|Le crayon sent la terre, un peu.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|Le toit, c'est ça.",
        "maman|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent la feuille, contre la tige.",
        "narrateur|Une coccinelle suit le trait, jusqu'à la poche.",
        "enfant-f|Elle a lu ton pot.",
        "papa|Le papier a montré le chemin.",
    ],
    (1, 3, 1): [
        "enfant-f|On le pose, sous le tuyau.",
        "narrateur|Mila ouvre la poche, tout bas, sous le zinc.",
        "narrateur|Elle pose la feuille, pour la dernière goutte.",
        "narrateur|Aniss compte la goutte, sans parler.",
        "narrateur|Un éclat de thym brille, sur le zinc.",
        "enfant-m|Maintenant.",
        "papa|Vous avez posé, les pieds au sol.",
        "narrateur|Une coccinelle avance, sous la goutte.",
        "enfant-f|Ta maison prend l'eau, juste une.",
        "narrateur|Un pois brille, mouillé, tout rond.",
        "maman|Tu n'as pas foncé.",
    ],
    (1, 3, 2): [
        "enfant-f|On attend la goutte.",
        "narrateur|Mila tient la poche, sans la tendre.",
        "narrateur|Aniss lève un doigt, et se tait.",
        "narrateur|La gouttière laisse une goutte, puis plus.",
        "narrateur|Un éclat de thym brille, sur le zinc.",
        "enfant-m|Elle est là.",
        "papa|Vous avez laissé la goutte finir.",
        "narrateur|Une coccinelle descend le tuyau, toute lente.",
        "enfant-f|Si elle veut, elle entre.",
        "narrateur|La poche attend, sous le zinc froid.",
        "maman|Son silence a compté.",
    ],
    (1, 3, 3): [
        "enfant-f|On dessine la goutte, d'abord.",
        "narrateur|Aniss dessine le tuyau, et un pois.",
        "narrateur|Mila regarde le zinc, sans se hausser.",
        "narrateur|Le crayon fait un rond, comme une goutte.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|La goutte, c'est ça.",
        "papa|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent la feuille, sous le tuyau.",
        "narrateur|Une coccinelle suit le trait, jusqu'à la poche.",
        "enfant-f|Elle a lu ta goutte.",
        "maman|Le papier a montré le chemin.",
    ],
    (2, 1, 1): [
        "enfant-f|On le pose, sous les lunettes.",
        "narrateur|Mila pose les lunettes, tout bas, près du tapis.",
        "narrateur|Les fibres deviennent nettes, une par une.",
        "narrateur|Aniss pose la feuille, sans un mot.",
        "narrateur|Un éclat de thym brille, entre deux fibres.",
        "enfant-m|Ici.",
        "papa|Vous avez posé, sans lever le tapis.",
        "narrateur|Une coccinelle avance, vue tout près.",
        "enfant-f|Je te vois, maintenant.",
        "narrateur|Les verres restent clairs, contre le tapis.",
        "maman|Tu n'as pas foncé.",
    ],
    (2, 1, 2): [
        "enfant-f|On attend, avec les lunettes.",
        "narrateur|Mila garde les lunettes, sans essuyer.",
        "narrateur|Aniss s'assoit, et il ne dit rien.",
        "narrateur|Le paillasson se tait, fibre après fibre.",
        "narrateur|Un éclat de thym brille, dans le tapis.",
        "enfant-m|Elle vient.",
        "papa|Vous avez laissé les fibres se taire.",
        "narrateur|Une coccinelle sort, nette, toute lente.",
        "enfant-f|Je la vois avancer.",
        "narrateur|Les lunettes restent immobiles, sur son nez.",
        "maman|Son silence a compté.",
    ],
    (2, 1, 3): [
        "enfant-f|On dessine ce que je vois.",
        "narrateur|Aniss dessine les fibres, et un rond.",
        "narrateur|Mila dicte, tout bas, sans bouger.",
        "narrateur|Les lunettes gardent le tapis, tout net.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|La bosse, c'est ça.",
        "papa|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent la feuille, sur le trait.",
        "narrateur|Une coccinelle suit le trait, sous les verres.",
        "enfant-f|Elle a lu tes fibres.",
        "maman|Le papier a montré le chemin.",
    ],
    (2, 2, 1): [
        "enfant-f|On le pose, contre le pot.",
        "narrateur|Mila pose les lunettes, près du rebord.",
        "narrateur|Le géranium devient net, feuille après feuille.",
        "narrateur|Aniss pose la feuille, sans bouger le pot.",
        "narrateur|Un éclat de thym brille, sur le rebord.",
        "enfant-m|Le toit, là.",
        "maman|Vous avez posé, sans basculer.",
        "narrateur|Une coccinelle grimpe, vue tout près.",
        "enfant-f|Je te vois, sur la terre.",
        "narrateur|Les verres sentent le géranium, un peu.",
        "papa|Tu n'as pas foncé.",
    ],
    (2, 2, 2): [
        "enfant-f|On attend, entre les pots.",
        "narrateur|Mila garde les lunettes, sans avancer.",
        "narrateur|Aniss ne dit rien, et regarde la terre.",
        "narrateur|Les géraniums se taisent, un par un.",
        "narrateur|Un éclat de thym brille, sur le rebord.",
        "enfant-m|Elle monte.",
        "maman|Vous avez laissé la terre se taire.",
        "narrateur|Une coccinelle sort, nette, sous une feuille.",
        "enfant-f|Je la vois grimper.",
        "narrateur|Les lunettes restent immobiles, entre deux pots.",
        "papa|Son silence a compté.",
    ],
    (2, 2, 3): [
        "enfant-f|On dessine les pots, d'abord.",
        "narrateur|Aniss dessine deux pots, et un rebord.",
        "narrateur|Mila dicte ce qu'elle voit, tout bas.",
        "narrateur|Les lunettes gardent la terre, tout nette.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|Le rebord, c'est ça.",
        "maman|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent la feuille, contre la tige.",
        "narrateur|Une coccinelle suit le trait, sous les verres.",
        "enfant-f|Elle a lu tes pots.",
        "papa|Le papier a montré le chemin.",
    ],
    (2, 3, 1): [
        "enfant-f|On le pose, sous le tuyau.",
        "narrateur|Mila pose les lunettes, tout bas, sous le zinc.",
        "narrateur|La goutte devient nette, toute ronde.",
        "narrateur|Aniss pose la feuille, les pieds au sol.",
        "narrateur|Un éclat de thym brille, sur le zinc.",
        "enfant-m|Maintenant.",
        "papa|Vous avez posé, sans vous hausser.",
        "narrateur|Une coccinelle descend, vue tout près.",
        "enfant-f|Je te vois, sur le tuyau.",
        "narrateur|Une goutte sèche, au coin d'un verre.",
        "maman|Tu n'as pas foncé.",
    ],
    (2, 3, 2): [
        "enfant-f|On attend la goutte.",
        "narrateur|Mila garde les lunettes, sans se hausser.",
        "narrateur|Aniss lève un doigt, et se tait.",
        "narrateur|La gouttière laisse une goutte, puis plus.",
        "narrateur|Un éclat de thym brille, sur le zinc.",
        "enfant-m|Elle est là.",
        "papa|Vous avez laissé la goutte finir.",
        "narrateur|Une coccinelle descend le tuyau, nette.",
        "enfant-f|Je la vois descendre.",
        "narrateur|Les lunettes restent immobiles, sous le zinc.",
        "maman|Son silence a compté.",
    ],
    (2, 3, 3): [
        "enfant-f|On dessine la goutte, d'abord.",
        "narrateur|Aniss dessine le tuyau, et un rond.",
        "narrateur|Mila dicte l'éclat, tout bas.",
        "narrateur|Les lunettes gardent le zinc, tout net.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|La goutte, c'est ça.",
        "papa|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent la feuille, sous le tuyau.",
        "narrateur|Une coccinelle suit le trait, sous les verres.",
        "enfant-f|Elle a lu ta goutte.",
        "maman|Le papier a montré le chemin.",
    ],
    (3, 1, 1): [
        "enfant-f|On le pose, sur le tapis.",
        "narrateur|Ils posent le seau, sans un bruit, sans sonner.",
        "narrateur|La feuille du fond reste sèche, au milieu.",
        "narrateur|Aniss tient l'anse, sans la bouger.",
        "narrateur|Un éclat de thym brille, dans les fibres.",
        "enfant-m|L'hôtel, ici.",
        "papa|Vous avez posé, sans faire le tambour.",
        "narrateur|Une coccinelle avance, vers le seau.",
        "enfant-f|L'hôtel a un voyageur.",
        "narrateur|Le seau reste droit, sur le paillasson.",
        "maman|Tu n'as pas foncé.",
    ],
    (3, 1, 2): [
        "enfant-f|On attend, avec le seau.",
        "narrateur|Aniss tient le seau, sans le pencher.",
        "narrateur|Il ne dit rien, et l'eau ne bouge plus.",
        "narrateur|Le paillasson se tait, fibre après fibre.",
        "narrateur|Un éclat de thym brille, dans le tapis.",
        "enfant-m|Elle vient.",
        "papa|Vous avez laissé le tapis se taire.",
        "narrateur|Une coccinelle sort, vers l'anse.",
        "enfant-f|Il peut venir.",
        "narrateur|Le seau attend, comme un tambour muet.",
        "maman|Son silence a compté.",
    ],
    (3, 1, 3): [
        "enfant-f|On dessine l'hôtel, d'abord.",
        "narrateur|Aniss dessine le seau, et le tapis.",
        "narrateur|Mila tient l'anse, sans la poser.",
        "narrateur|Le crayon fait un rond, comme le fond.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|L'hôtel, c'est ça.",
        "papa|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent le seau, sur le trait.",
        "narrateur|Une coccinelle suit le trait, jusqu'à l'anse.",
        "enfant-f|Elle a lu ton hôtel.",
        "maman|Le papier a montré le chemin.",
    ],
    (3, 2, 1): [
        "enfant-f|On le pose, entre les pots.",
        "narrateur|Ils calent le seau, sans pousser.",
        "narrateur|La feuille du fond reste sèche, au milieu.",
        "narrateur|Aniss tient un pot, de l'autre main.",
        "narrateur|Un éclat de thym brille, sur le rebord.",
        "enfant-m|L'hôtel, ici.",
        "maman|Vous avez posé, sans verser.",
        "narrateur|Une coccinelle grimpe, vers l'anse.",
        "enfant-f|L'hôtel sent la terre.",
        "narrateur|Le seau reste droit, entre deux pots.",
        "papa|Tu n'as pas foncé.",
    ],
    (3, 2, 2): [
        "enfant-f|On attend, entre les pots.",
        "narrateur|Aniss tient le seau, sans le pencher.",
        "narrateur|Il ne dit rien, et il regarde la terre.",
        "narrateur|Les géraniums se taisent, un par un.",
        "narrateur|Un éclat de thym brille, sur le rebord.",
        "enfant-m|Elle monte.",
        "maman|Vous avez laissé la terre se taire.",
        "narrateur|Une coccinelle sort, vers le seau.",
        "enfant-f|Il peut venir.",
        "narrateur|Le seau attend, entre deux pots.",
        "papa|Son silence a compté.",
    ],
    (3, 2, 3): [
        "enfant-f|On dessine les pots, d'abord.",
        "narrateur|Aniss dessine le seau, entre deux pots.",
        "narrateur|Mila tient l'anse, sans pousser.",
        "narrateur|Le crayon sent la terre, un peu.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|L'hôtel, c'est ça.",
        "maman|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils calent le seau, sur le trait.",
        "narrateur|Une coccinelle suit le trait, jusqu'à l'anse.",
        "enfant-f|Elle a lu tes pots.",
        "papa|Le papier a montré le chemin.",
    ],
    (3, 3, 1): [
        "enfant-f|On le pose, sous le tuyau.",
        "narrateur|Ils posent le seau, tout bas, sous le zinc.",
        "narrateur|La feuille du fond attend la goutte.",
        "narrateur|Aniss compte, sans parler.",
        "narrateur|Un éclat de thym brille, sur le zinc.",
        "enfant-m|Maintenant.",
        "papa|Vous avez posé, les pieds au sol.",
        "narrateur|Une coccinelle descend, vers le seau.",
        "enfant-f|L'hôtel prend l'eau, juste une.",
        "narrateur|Le seau reste droit, sous la gouttière.",
        "maman|Tu n'as pas foncé.",
    ],
    (3, 3, 2): [
        "enfant-f|On attend la goutte.",
        "narrateur|Aniss tient le seau, sans le lever.",
        "narrateur|Il lève un doigt, et se tait.",
        "narrateur|La gouttière laisse une goutte, puis plus.",
        "narrateur|Un éclat de thym brille, sur le zinc.",
        "enfant-m|Elle est là.",
        "papa|Vous avez laissé la goutte finir.",
        "narrateur|Une coccinelle descend le tuyau, vers l'anse.",
        "enfant-f|Il peut venir.",
        "narrateur|Le seau attend, sous le zinc froid.",
        "maman|Son silence a compté.",
    ],
    (3, 3, 3): [
        "enfant-f|On dessine la gouttière, d'abord.",
        "narrateur|Aniss dessine le tuyau, et le seau.",
        "narrateur|Mila tient l'anse, sans la lever.",
        "narrateur|Le crayon fait un rond, comme une goutte.",
        "narrateur|Un éclat de thym brille, sur le papier.",
        "enfant-m|La goutte, c'est ça.",
        "papa|Tu as laissé Aniss dessiner.",
        "narrateur|Puis ils posent le seau, sous le tuyau.",
        "narrateur|Une coccinelle suit le trait, jusqu'à l'anse.",
        "enfant-f|Elle a lu ta gouttière.",
        "maman|Le papier a montré le chemin.",
    ],
}

END_SONS = {1: "coccinelle,paillasson", 2: "coccinelle,pots", 3: "coccinelle,gouttiere"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|La coccinelle entre, dans la poche à pois.",
        "enfant-f|On a posé, sans lever.",
        "papa|Le tapis n'a pas volé.",
        "maman|La gouttière s'est tue, pour vous.",
        "narrateur|Ça a failli trop bouger.",
        "enfant-f|Surtout le moment du tapis.",
        "narrateur|Un éclat de thym sèche, sur un pois.",
    ],
    (1, 1, 2): [
        "narrateur|La coccinelle entre, après le silence.",
        "enfant-f|On a attendu, tous les deux.",
        "papa|Aniss n'a pas parlé, et ça a suffi.",
        "maman|La poche est restée ouverte.",
        "narrateur|Ça a failli trop vite.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|Une fibre du paillasson colle à la poche.",
    ],
    (1, 1, 3): [
        "narrateur|La coccinelle suit le dessin, jusqu'à la poche.",
        "enfant-f|On a dessiné, d'abord.",
        "papa|Le papier a montré le pois.",
        "maman|Tes doigts sentent le crayon.",
        "narrateur|Ça a failli trop toucher.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le dessin d'Aniss tient un pois, et l'éclat.",
    ],
    (1, 2, 1): [
        "narrateur|La coccinelle grimpe, dans la poche à pois.",
        "enfant-f|On a posé, sans basculer.",
        "papa|Le pot n'a pas versé.",
        "maman|Le géranium sent la terre, un peu.",
        "narrateur|Ça a failli trop pencher.",
        "enfant-f|Surtout le moment du pot.",
        "narrateur|Un pétale de géranium reste collé à un pois.",
    ],
    (1, 2, 2): [
        "narrateur|La coccinelle entre, après le silence des pots.",
        "enfant-f|On a attendu, entre les pots.",
        "papa|Aniss a regardé la terre, longtemps.",
        "maman|La poche a senti la terre.",
        "narrateur|Ça a failli trop pousser.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|La poche sent la terre des pots, un peu.",
    ],
    (1, 2, 3): [
        "narrateur|La coccinelle suit le pot dessiné, jusqu'à la poche.",
        "enfant-f|On a dessiné le pot, d'abord.",
        "papa|Le papier a montré la tige.",
        "maman|Tes doigts sentent le crayon, et la terre.",
        "narrateur|Ça a failli trop bouger le pot.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le papier montre un pot, et le manteau.",
    ],
    (1, 3, 1): [
        "narrateur|La coccinelle entre, sous la dernière goutte.",
        "enfant-f|On a posé, les pieds au sol.",
        "papa|Le tuyau n'a plus goutté.",
        "maman|Un pois brille, mouillé, tout rond.",
        "narrateur|Ça a failli trop se hausser.",
        "enfant-f|Surtout le moment du tuyau.",
        "narrateur|Une goutte de gouttière sèche sur un pois.",
    ],
    (1, 3, 2): [
        "narrateur|La coccinelle entre, après la dernière goutte.",
        "enfant-f|On a attendu la gouttière.",
        "papa|Aniss a compté, sans parler.",
        "maman|La poche a pris une goutte, juste une.",
        "narrateur|Ça a failli trop tendre.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|Le bas du manteau garde un rond d'eau.",
    ],
    (1, 3, 3): [
        "narrateur|La coccinelle suit la goutte dessinée, jusqu'à la poche.",
        "enfant-f|On a dessiné la goutte, d'abord.",
        "papa|Le papier a montré le zinc.",
        "maman|Tes doigts sentent le crayon, un peu froids.",
        "narrateur|Ça a failli trop se hausser.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le dessin montre la gouttière, et un pois.",
    ],
    (2, 1, 1): [
        "narrateur|La coccinelle avance, nette, sous les lunettes.",
        "enfant-f|On a posé les verres, tout bas.",
        "papa|Le tapis n'a pas volé.",
        "maman|Tu l'as vue, tout près.",
        "narrateur|Ça a failli trop essuyer.",
        "enfant-f|Surtout le moment des fibres.",
        "narrateur|Les lunettes gardent un éclat de thym, au bord.",
    ],
    (2, 1, 2): [
        "narrateur|La coccinelle avance, après le silence des fibres.",
        "enfant-f|On a attendu, avec les lunettes.",
        "papa|Aniss n'a pas parlé, et ça a suffi.",
        "maman|Les verres sont restés clairs.",
        "narrateur|Ça a failli trop voiler.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|Un rond de buée reste sur un verre, minuscule.",
    ],
    (2, 1, 3): [
        "narrateur|La coccinelle suit les fibres dessinées, sous les verres.",
        "enfant-f|On a dessiné ce que je voyais.",
        "papa|Le papier a montré la bosse.",
        "maman|Tes doigts sentent le crayon.",
        "narrateur|Ça a failli trop bouger les lunettes.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le dessin copie le rond des lunettes.",
    ],
    (2, 2, 1): [
        "narrateur|La coccinelle grimpe, nette, contre le pot.",
        "enfant-f|On a posé les verres, au rebord.",
        "papa|Le pot n'a pas versé.",
        "maman|Tu l'as vue, sur la terre.",
        "narrateur|Ça a failli trop avancer le nez.",
        "enfant-f|Surtout le moment du rebord.",
        "narrateur|Un trait de terre barre un verre, tout fin.",
    ],
    (2, 2, 2): [
        "narrateur|La coccinelle grimpe, après le silence des pots.",
        "enfant-f|On a attendu, entre les pots.",
        "papa|Aniss a regardé la terre, longtemps.",
        "maman|Les verres ont senti le géranium.",
        "narrateur|Ça a failli trop pousser.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|Les lunettes sentent le géranium, un peu.",
    ],
    (2, 2, 3): [
        "narrateur|La coccinelle suit les pots dessinés, sous les verres.",
        "enfant-f|On a dessiné les pots, d'abord.",
        "papa|Le papier a montré le rebord.",
        "maman|Tes doigts sentent le crayon, et la terre.",
        "narrateur|Ça a failli trop bouger le pot.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le papier montre les pots, vus des lunettes.",
    ],
    (2, 3, 1): [
        "narrateur|La coccinelle descend, nette, sous le tuyau.",
        "enfant-f|On a posé les verres, tout bas.",
        "papa|Les pieds sont restés au sol.",
        "maman|Tu l'as vue, sur le zinc.",
        "narrateur|Ça a failli trop se hausser.",
        "enfant-f|Surtout le moment du tuyau.",
        "narrateur|Une goutte sèche au coin des lunettes.",
    ],
    (2, 3, 2): [
        "narrateur|La coccinelle descend, après la dernière goutte.",
        "enfant-f|On a attendu, sous les lunettes.",
        "papa|Aniss a levé un doigt, sans parler.",
        "maman|Les verres ont gardé la goutte.",
        "narrateur|Ça a failli trop se hausser.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|Les lunettes gardent un éclat de gouttière.",
    ],
    (2, 3, 3): [
        "narrateur|La coccinelle suit la goutte dessinée, sous les verres.",
        "enfant-f|On a dessiné la goutte, d'abord.",
        "papa|Le papier a montré le zinc.",
        "maman|Tes doigts sentent le crayon, un peu froids.",
        "narrateur|Ça a failli trop se hausser.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le dessin montre la goutte, dans un verre.",
    ],
    (3, 1, 1): [
        "narrateur|La coccinelle entre, dans le seau, sans bruit.",
        "enfant-f|On a posé, sans le tambour.",
        "papa|Le tapis n'a pas sonné.",
        "maman|L'hôtel a un voyageur.",
        "narrateur|Ça a failli trop sonner.",
        "enfant-f|Surtout le moment de l'anse.",
        "narrateur|Le seau garde un éclat de thym, au fond.",
    ],
    (3, 1, 2): [
        "narrateur|La coccinelle entre, après le silence du seau.",
        "enfant-f|On a attendu, avec l'anse.",
        "papa|Aniss n'a pas penché.",
        "maman|L'eau n'a plus bougé.",
        "narrateur|Ça a failli trop sonner.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|Une fibre du paillasson colle à l'anse.",
    ],
    (3, 1, 3): [
        "narrateur|La coccinelle suit l'hôtel dessiné, jusqu'à l'anse.",
        "enfant-f|On a dessiné l'hôtel, d'abord.",
        "papa|Le papier a montré le seau.",
        "maman|Tes doigts sentent le crayon.",
        "narrateur|Ça a failli trop poser trop tôt.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le dessin montre le seau, et le paillasson.",
    ],
    (3, 2, 1): [
        "narrateur|La coccinelle entre, dans le seau, entre les pots.",
        "enfant-f|On a posé, sans verser.",
        "papa|Le pot n'a pas penché.",
        "maman|L'hôtel sent la terre.",
        "narrateur|Ça a failli trop pousser.",
        "enfant-f|Surtout le moment des pots.",
        "narrateur|Un pétale nage au fond du seau.",
    ],
    (3, 2, 2): [
        "narrateur|La coccinelle entre, après le silence des pots.",
        "enfant-f|On a attendu, entre les pots.",
        "papa|Aniss a tenu l'anse, longtemps.",
        "maman|La terre n'a pas bougé.",
        "narrateur|Ça a failli trop caler.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|L'anse garde un peu de terre.",
    ],
    (3, 2, 3): [
        "narrateur|La coccinelle suit les pots dessinés, jusqu'à l'anse.",
        "enfant-f|On a dessiné les pots, d'abord.",
        "papa|Le papier a montré l'hôtel.",
        "maman|Tes doigts sentent le crayon, et la terre.",
        "narrateur|Ça a failli trop pousser.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le papier montre le seau entre les pots.",
    ],
    (3, 3, 1): [
        "narrateur|La coccinelle entre, dans le seau, sous le tuyau.",
        "enfant-f|On a posé, les pieds au sol.",
        "papa|La goutte a trouvé le fond.",
        "maman|L'hôtel a pris juste une goutte.",
        "narrateur|Ça a failli trop lever.",
        "enfant-f|Surtout le moment du tuyau.",
        "narrateur|Une goutte de gouttière reste au fond.",
    ],
    (3, 3, 2): [
        "narrateur|La coccinelle entre, après la dernière goutte.",
        "enfant-f|On a attendu, sous le zinc.",
        "papa|Aniss a compté, sans lever.",
        "maman|Le seau n'a pas sonné.",
        "narrateur|Ça a failli trop lever.",
        "enfant-f|Surtout le moment d'attendre.",
        "narrateur|Le seau sonne plus bas, avec l'eau.",
    ],
    (3, 3, 3): [
        "narrateur|La coccinelle suit la gouttière dessinée, jusqu'à l'anse.",
        "enfant-f|On a dessiné la gouttière, d'abord.",
        "papa|Le papier a montré le seau, et le zinc.",
        "maman|Tes doigts sentent le crayon, un peu froids.",
        "narrateur|Ça a failli trop lever.",
        "enfant-f|Surtout le moment du trait.",
        "narrateur|Le dessin montre la gouttière, et le seau.",
    ],
}


def t2_question(t1: int) -> list[str]:
    return [f"narrateur|{T1[t1]['voy']}"] + T2_Q


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "goutte,soupe",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le manteau à pois", "les lunettes", "le seau")},
    )

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        out_chunks[p] = voice(by_src[p], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        out_chunks[f"{p}_Q0001"] = voice(
            by_src[f"{p}_Q0001"], t1["question"], "clue", "",
            {"emphasis": t1["emphasis"], "fields": t1["qfields"]},
        )
        out_chunks[f"{p}_C0001"] = voice(
            by_src[f"{p}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["emphasis"]},
        )
        out_chunks[f"{p}_T0002_P0000"] = voice(
            by_src[f"{p}_T0002_P0000"], t2_question(a), "choice", "",
            {"fields": t3lab("le paillasson", "les pots", "la gouttière")},
        )
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[sp] = voice(
                by_src[sp], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{sp}_T0003_P0000"] = voice(
                by_src[f"{sp}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab("on le pose", "on attend", "on dessine")},
            )
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[c],
                    {"emphasis": T3_EMPH[c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[b],
                    {"emphasis": "éclat de thym"},
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
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "il faut attendre",
        "escargot",
        "manteau vert",
        "manteau jaune",
        "drap à pois",
        "miel",
        "merle",
        "tout doux",
        "tout calme",
        "zoé",
        "zoe",
        "sami",
        "grand-père",
        "grand pere",
        "maîtresse",
        "maitresse",
        "jardinier",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "marque fine",
        "ombre-flèche",
        "grain d'ambre",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absente")
    if "éclat de thym" not in blob and "eclat de thym" not in blob:
        raise SystemExit(f"{SID}: éclat de thym absent")
    if "manteau à pois" not in blob:
        raise SystemExit(f"{SID}: manteau à pois absent")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        lasts.append(last_n[-1])
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
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
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.COR.003 — jouer avec l'autre tel qu'il est (vécue, non dite)\n"
        "- **Personnages :** Mila, Aniss, papa, maman\n"
        "- **Lieu :** cuisine puis seuil, après la pluie\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La gouttière compte dans la cuisine. Mila veut le **manteau à pois**, "
        "les **lunettes** et le **seau** jusqu'au seuil, **avant la dernière goutte**, "
        "pour une maison de feuille. Un **éclat de thym** colle à un pois. "
        "Aniss arrive sans un mot : elle propose, il prend son temps, le silence répond. "
        "Première idée trop vite : manche retournée, verres voilés, seau coincé. "
        "Les trois affaires partent. Paillasson, pots ou gouttière : trop vite, "
        "la coccinelle part. 2e ruse : l'éclat du début montre la place. "
        "Aniss pointe, sans parler. Mila refuse de foncer. "
        "On le pose, on attend, on dessine. La maison tient. Ça a failli ne pas arriver. "
        "Monde ≠ TREE-AUT-032 (manteau vert) ≠ TREE-AUT-037 (manteau jaune) "
        "≠ TREE-DIF-032 (drap à pois).\n\n"
        "## Vécu\n\n"
        "Mila veut sortir **maintenant**. Aniss veut regarder l'éclat. "
        "Sourire disparu, poitrine serrée, adulte accroupi. "
        "Chaque choix change l'obstacle et le climax. La leçon se voit : "
        "poser sans lever, attendre le silence, dessiner d'abord. "
        "Indice d'ouverture payé : éclat de thym. Fin : objet + trace unique.\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit 62 % jeté (escargot, merle, miel, « tout doux / encore / déjà »).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (attendre la voix d'Aniss). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
