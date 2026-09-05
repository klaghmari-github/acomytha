#!/usr/bin/env python3
"""TREE-DIF-004 — La gouttière et le cube de Nino (N3, DIF.PAR.001, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-004"
N3 = 16
TITLE = "La gouttière et le cube de Nino"
FIL = (
    "Après la pluie, une goutte tape les cubes dans la cuisine. "
    "Un éclat de goutte reste collé. Nino veut poser LE cube avec Aniss, "
    "sous la gouttière, dans le bac ou au potager, avant la prochaine goutte. "
    "Aniss arrive sans un mot. Nino propose. Aniss prend son temps. "
    "Le silence répond. Première idée trop vite : le cube glisse. "
    "Rouge, bleu, jaune : les trois partent. Trop vite, la goutte bouscule, "
    "le sable avale, la laitue cache. L'éclat du début montre la place. "
    "Ils refusent de foncer. Pont, feuille ou quai. Le cube tient. "
    "Ça a failli ne pas arriver."
)
CHARS = "Nino, Aniss, papa, maman"
SETTING = "cuisine après la pluie, puis le jardin"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "toute ronde",
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
    "bateau",
    "escargot",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "éclat de goutte",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=nino_propose_aniss_prend_son_temps; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_pose; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_cube; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_cubes_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_cube_glisse; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=aniss_se_tait_nino_refuse_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "éclat de goutte",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=l_eclat_du_debut_montre_la_place; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "éclat de goutte",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_cube_tient_l_eclat_reste; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N3:
            raise SystemExit(f"{where} {n}>{N3}: {ph}")
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
    "narrateur|La goutte du rebord hésite, puis tombe.",
    "narrateur|Elle tape les cubes, sur la table.",
    "narrateur|Un éclat de goutte reste collé, minuscule.",
    "narrateur|Nino connaît cette cuisine, après la pluie.",
    "narrateur|Ça sent le pain tiède, et le bois mouillé.",
    "narrateur|La nappe garde une tache d'eau, près des cubes.",
    "papa|J'essuie, pour voir le bois.",
    "narrateur|Papa passe le torchon rayé.",
    "narrateur|Maman ouvre la fenêtre, un cran.",
    "narrateur|Dehors, la gouttière prépare une autre goutte.",
    "narrateur|Trois cubes attendent : rouge, bleu, jaune.",
    "narrateur|En ce moment, Nino touche l'éclat.",
    "enfant-m|Je le pose avec Aniss, avant la goutte.",
    "narrateur|Aniss pousse la porte, sans un mot.",
    "narrateur|Il s'arrête, et regarde l'éclat.",
    "enfant-m|On y va, Aniss.",
    "narrateur|Aniss ne dit rien.",
    "narrateur|Ses mains restent dans les poches.",
    "narrateur|Nino pousse un cube, trop vite.",
    "narrateur|Le cube glisse, et l'éclat s'étale.",
    "enfant-m|Oh.",
    "narrateur|Le sourire de Nino disparaît.",
    "papa|Merci, tu as vu ses mains.",
    "maman|Tu entends la goutte, Nino ?",
]

T1_CHOICE = [
    "narrateur|Sur la table, trois cubes brillent, un peu mouillés.",
    "narrateur|Le rouge, le bleu, le jaune.",
    "papa|Tu poses lequel d'abord, Nino ?",
]

T1 = {
    1: {
        "lab": "le cube rouge",
        "sons": "bois,goutte",
        "emphasis": "cube rouge",
        "passage": [
            "narrateur|Nino saisit le cube rouge, un peu lourd.",
            "narrateur|L'éclat de goutte tremble, sur le bois rouge.",
            "enfant-m|Prends-le, Aniss.",
            "narrateur|Il le pose dans la paume, trop vite.",
            "narrateur|Aniss ouvre les doigts, sans un mot.",
            "narrateur|Le rouge tombe, et roule vers le torchon.",
            "enfant-m|Il ne veut pas.",
            "narrateur|Dans sa poitrine, ça serre, trop.",
            "papa|On le tend, sans le pousser.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Nino ramasse le rouge, et attend.",
            "narrateur|Aniss avance un doigt, puis la main.",
            "enfant-m|Le bleu, et le jaune aussi.",
            "maman|Les trois cubes viennent ?",
            "enfant-m|Oui, les trois.",
        ],
        "question": [
            "narrateur|Nino a pris le cube rouge d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "rouge",
            "accepted_examples": "rouge | le rouge | cube rouge | le cube rouge | d'abord le rouge",
            "retry_prompt": "Nino prend le cube rouge d'abord.",
        },
        "confirm": [
            "narrateur|Le cube rouge tient, dans deux mains.",
            "enfant-m|L'éclat est là, minuscule.",
            "papa|Le bleu, Aniss le porte ?",
            "enfant-m|J'ai le jaune.",
            "narrateur|Aniss serre le bleu, sans parler.",
            "maman|La gouttière n'a pas fini.",
            "enfant-m|On pose le rouge, avant la goutte.",
            "narrateur|Ils avancent vers la porte, sans courir.",
            "papa|Les trois cubes partent.",
            "narrateur|Un éclat de goutte brille, sur le rouge.",
        ],
        "voy": "Le cube rouge cherche sa place.",
    },
    2: {
        "lab": "le cube bleu",
        "sons": "bois,verre",
        "emphasis": "cube bleu",
        "passage": [
            "narrateur|Nino choisit le cube bleu, plus froid.",
            "narrateur|Il le glisse vers Aniss, trop vite.",
            "narrateur|Le bleu tape la vitre, clic.",
            "enfant-m|Regarde, Aniss !",
            "narrateur|Aniss regarde la fenêtre, pas le cube.",
            "narrateur|L'éclat de goutte s'étale, sur le bleu.",
            "enfant-m|Il ne prend pas.",
            "narrateur|Le sourire de Nino disparaît.",
            "maman|Il te montre la goutte, pas la course.",
            "narrateur|Maman s'accroupit, près de la table.",
            "narrateur|Nino laisse le bleu, au milieu.",
            "narrateur|Aniss pose un doigt, puis le prend.",
            "papa|Le rouge, et le jaune aussi ?",
            "enfant-m|Oui, les trois.",
            "narrateur|Les trois cubes quittent la nappe.",
        ],
        "question": [
            "narrateur|Nino a pris le cube bleu d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "bleu",
            "accepted_examples": "bleu | le bleu | cube bleu | le cube bleu | d'abord le bleu",
            "retry_prompt": "Nino prend le cube bleu d'abord.",
        },
        "confirm": [
            "narrateur|Le cube bleu reste froid, contre la paume.",
            "enfant-m|L'éclat tient, tout petit.",
            "maman|Le rouge, qui le porte ?",
            "enfant-m|Moi le jaune.",
            "narrateur|Aniss garde le bleu, et le rouge.",
            "papa|La gouttière n'a pas fini.",
            "enfant-m|On pose le bleu, avant la goutte.",
            "narrateur|Ils avancent vers la porte, sans courir.",
            "maman|Les trois cubes partent.",
            "narrateur|Un éclat de goutte brille, sur le bleu.",
        ],
        "voy": "Le cube bleu cherche sa place.",
    },
    3: {
        "lab": "le cube jaune",
        "sons": "bois,fenetre",
        "emphasis": "cube jaune",
        "passage": [
            "narrateur|Nino lève le cube jaune, vers la fenêtre.",
            "narrateur|Il le montre trop haut, trop vite.",
            "narrateur|Une goutte du rebord tape le jaune.",
            "enfant-m|Pour toi, Aniss !",
            "narrateur|Aniss recule d'un pas, et secoue la tête.",
            "narrateur|L'éclat de goutte glisse, sur le bois jaune.",
            "enfant-m|Il ne veut pas le prendre.",
            "narrateur|Les épaules de Nino se serrent.",
            "papa|On le baisse, près de ses mains.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "narrateur|Nino baisse le jaune, et attend.",
            "narrateur|Aniss s'approche, et le prend.",
            "maman|Le rouge, et le bleu aussi ?",
            "enfant-m|Oui, les trois.",
            "narrateur|Les trois cubes quittent la table.",
        ],
        "question": [
            "narrateur|Nino a pris le cube jaune d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "jaune",
            "accepted_examples": "jaune | le jaune | cube jaune | le cube jaune | d'abord le jaune",
            "retry_prompt": "Nino prend le cube jaune d'abord.",
        },
        "confirm": [
            "narrateur|Le cube jaune reste tiède, dans la main.",
            "enfant-m|L'éclat tient, minuscule.",
            "papa|Le rouge, Aniss le porte ?",
            "enfant-m|J'ai le bleu.",
            "narrateur|Aniss serre le jaune, sans parler.",
            "maman|La gouttière n'a pas fini.",
            "enfant-m|On pose le jaune, avant la goutte.",
            "narrateur|Ils avancent vers la porte, sans courir.",
            "papa|Les trois cubes partent.",
            "narrateur|Un éclat de goutte brille, sur le jaune.",
        ],
        "voy": "Le cube jaune cherche sa place.",
    },
}

T2 = {
    (1, 1): {
        "sons": "gouttiere,goutte",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Nino pose le cube rouge, sous la gouttière.",
            "narrateur|Il le pose trop vite, trop près du filet.",
            "enfant-m|Là, avant la goutte !",
            "narrateur|La goutte tape le rouge, et le cube glisse.",
            "enfant-m|Il part !",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Le filet n'aime pas la course.",
            "narrateur|Papa s'accroupit, sous le tuyau.",
            "narrateur|Aniss ne dit rien, et il pointe.",
            "narrateur|Un éclat de goutte brille, sur le bois rouge.",
            "enfant-m|Pas maintenant.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "sable,eau",
        "emphasis": "bac",
        "passage": [
            "narrateur|Nino lâche le cube rouge, dans le bac.",
            "narrateur|Le sable mouillé attrape un coin, trop fort.",
            "enfant-m|Au milieu, Aniss !",
            "narrateur|Le rouge penche, et s'enfonce un peu.",
            "enfant-m|Il avale mon cube.",
            "narrateur|Ses joues chauffent, et ses mains tremblent.",
            "maman|Le sable n'aime pas les coups.",
            "narrateur|Maman s'accroupit, au bord du bac.",
            "narrateur|Aniss recule les mains, sans un mot.",
            "narrateur|Un éclat de goutte brille, sur le sable.",
            "enfant-m|Je ne fonce pas.",
            "papa|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "terre,feuille",
        "emphasis": "potager",
        "passage": [
            "narrateur|Nino glisse le cube rouge, entre les laitues.",
            "narrateur|Un filet d'arrosoir tourne le bois, trop vite.",
            "enfant-m|Entre les feuilles, Aniss !",
            "narrateur|Une laitue cache le rouge, d'un coup.",
            "enfant-m|Je ne le vois plus.",
            "narrateur|Ça serre, dans sa poitrine, trop.",
            "papa|La terre n'aime pas la course.",
            "narrateur|Papa s'accroupit, entre deux rangs.",
            "narrateur|Aniss s'arrête au bord, les pieds propres.",
            "narrateur|Un éclat de goutte brille, sur une nervure.",
            "enfant-m|Pas maintenant.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "gouttiere,bois",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Nino lève le cube bleu, sous la gouttière.",
            "narrateur|Il le tend trop haut, trop vite.",
            "enfant-m|Attrape la goutte, bleu !",
            "narrateur|La goutte rate le bois, et mouille un côté.",
            "enfant-m|Je l'ai manquée.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça tape, trop vite.",
            "papa|Les pieds restent au sol, d'accord ?",
            "narrateur|Papa s'accroupit, sous le tuyau.",
            "narrateur|Aniss reste immobile, et lève un doigt.",
            "narrateur|Un éclat de goutte brille, sur le bleu.",
            "enfant-m|Là.",
            "enfant-m|Pas maintenant.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "sable,flaque",
        "emphasis": "bac",
        "passage": [
            "narrateur|Nino pousse le cube bleu, vers la flaque du bac.",
            "narrateur|Le sable colle au bois bleu, grain par grain.",
            "enfant-m|Dans l'eau, Aniss !",
            "narrateur|Un coin s'enfonce, et le bleu penche.",
            "enfant-m|Il ne veut pas avancer.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "maman|La flaque n'aime pas les coups.",
            "narrateur|Maman s'accroupit, au bord du bac.",
            "narrateur|Aniss ne met pas les mains, et il montre.",
            "narrateur|Un éclat de goutte brille, sur la flaque.",
            "enfant-m|Je ne fonce pas.",
            "papa|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "terre,arrosoir",
        "emphasis": "potager",
        "passage": [
            "narrateur|Nino veut le cube bleu, dans le filet d'arrosoir.",
            "narrateur|La terre grasse retient ses chaussures.",
            "enfant-m|Suis l'eau, Aniss !",
            "narrateur|Aniss s'arrête au bord, sans avancer.",
            "enfant-m|Viens !",
            "narrateur|Aniss secoue la tête, et se tait.",
            "narrateur|Les épaules de Nino se serrent.",
            "papa|La boue n'aime pas la course.",
            "narrateur|Papa s'accroupit, près des laitues.",
            "narrateur|Un éclat de goutte brille, sur une feuille.",
            "enfant-m|Pas maintenant.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "gouttiere,bois",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Nino pose le cube jaune, trop près du filet.",
            "narrateur|Le tuyau est froid, un peu vert.",
            "enfant-m|Juste dessous, Aniss !",
            "narrateur|Le filet tourne le jaune, et l'éclat fuit.",
            "enfant-m|Il tourne tout seul.",
            "narrateur|Ses joues chauffent, et il recule le cube.",
            "papa|Le filet n'aime pas le bord trop juste.",
            "narrateur|Papa s'accroupit, sous le tuyau.",
            "narrateur|Aniss compte une goutte, sans parler.",
            "narrateur|Un éclat de goutte brille, sur le jaune.",
            "enfant-m|Pas maintenant.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "sable,bois",
        "emphasis": "bac",
        "passage": [
            "narrateur|Nino plante le cube jaune, dans le sable du bac.",
            "narrateur|Il le pousse trop fort, comme un piquet.",
            "enfant-m|Il tient, Aniss !",
            "narrateur|Le jaune s'enfonce, et l'éclat disparaît.",
            "enfant-m|Je ne le vois plus.",
            "narrateur|Le sourire de Nino disparaît.",
            "maman|Le sable n'aime pas les piquets.",
            "narrateur|Maman s'accroupit, au bord du bac.",
            "narrateur|Aniss pose la paume à plat, sans parler.",
            "narrateur|Un éclat de goutte brille, au bord du bac.",
            "enfant-m|Je ne fonce pas.",
            "papa|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "terre,laitue",
        "emphasis": "potager",
        "passage": [
            "narrateur|Nino glisse le cube jaune, sous une laitue.",
            "narrateur|La feuille large cache le bois, trop vite.",
            "enfant-m|Dessous, Aniss !",
            "narrateur|L'éclat de goutte disparaît, sous le vert.",
            "enfant-m|Il est perdu.",
            "narrateur|Ça serre, dans sa poitrine, d'un coup.",
            "papa|Les feuilles n'aiment pas la cachette.",
            "narrateur|Papa s'accroupit, entre deux rangs.",
            "narrateur|Aniss soulève un bord, sans un mot.",
            "narrateur|Un éclat de goutte brille, sous la nervure.",
            "enfant-m|Là.",
            "enfant-m|Pas maintenant.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
}

T2_Q = [
    "narrateur|Devant, la gouttière laisse une goutte, trop loin.",
    "narrateur|Le bac, lui, avale le bois.",
    "narrateur|Au potager, la laitue cache trop.",
    "papa|Nino, tu le poses où ?",
    "maman|Avant la prochaine goutte.",
]

T3_CHOICE = {
    1: [
        "narrateur|La goutte va revenir, sous le tuyau.",
        "papa|Le pont, la feuille, ou le quai ?",
    ],
    2: [
        "narrateur|Le bac n'a pas lâché le cube.",
        "maman|Le pont, la feuille, ou le quai ?",
    ],
    3: [
        "narrateur|La laitue n'a pas dit son secret.",
        "papa|Le pont, la feuille, ou le quai ?",
    ],
}

T3_SONS = {1: "cubes,eau", 2: "feuille,goutte", 3: "pierre,eau"}
T3_EMPH = {1: "pont", 2: "feuille", 3: "quai"}

T3 = {
    (1, 1, 1): [
        "enfant-m|Un pont, avec les cubes.",
        "narrateur|Nino pose le bleu, au-dessus du filet.",
        "narrateur|Il tend le jaune, sans le pousser.",
        "narrateur|Aniss le prend, et le pose.",
        "narrateur|Les deux cubes font un pont, étroit.",
        "narrateur|Un éclat de goutte brille, sur le rouge.",
        "enfant-m|Ici.",
        "papa|Vous avez posé, sans bousculer le filet.",
        "narrateur|L'eau passe dessous, et le rouge tient.",
        "enfant-m|Il est à nous, ce cube.",
        "maman|Tu n'as pas foncé.",
    ],
    (1, 1, 2): [
        "enfant-m|Une feuille, pour la goutte.",
        "narrateur|Nino glisse une feuille, sous le tuyau.",
        "narrateur|Aniss tient le bord, sans parler.",
        "narrateur|Ils posent le rouge, sur la feuille.",
        "narrateur|La goutte tape le vert, pas le bois.",
        "narrateur|Un éclat de goutte brille, sur la nervure.",
        "enfant-m|Elle le garde.",
        "papa|Vous avez posé, sans lever trop haut.",
        "narrateur|Le cube rouge reste droit, au milieu.",
        "enfant-m|La feuille a pris la goutte.",
        "maman|Son silence a compté.",
    ],
    (1, 1, 3): [
        "enfant-m|Un quai, plus loin du filet.",
        "narrateur|Nino cherche une pierre plate, sous le tuyau.",
        "narrateur|Aniss la pose, sans un mot.",
        "narrateur|Ils calent le rouge, au bord de la pierre.",
        "narrateur|Le filet passe à côté, sans le tourner.",
        "narrateur|Un éclat de goutte brille, au bord du quai.",
        "enfant-m|Il a son bord.",
        "papa|Vous avez laissé l'eau son chemin.",
        "narrateur|Le cube rouge reste sec, d'un côté.",
        "enfant-m|Le quai le tient.",
        "maman|Tu n'as pas foncé.",
    ],
    (1, 2, 1): [
        "enfant-m|Un pont, au-dessus du sable.",
        "narrateur|Nino pose le bleu, puis tend le jaune.",
        "narrateur|Aniss le pose, sans enfoncer.",
        "narrateur|Les deux cubes font un pont, dans le bac.",
        "narrateur|Ils posent le rouge, dessus, tout léger.",
        "narrateur|Un éclat de goutte brille, entre deux cubes.",
        "enfant-m|Il ne s'enfonce plus.",
        "maman|Vous avez posé, sans lâcher.",
        "narrateur|Le sable reste dessous, et le rouge tient.",
        "enfant-m|Le pont le porte.",
        "papa|Tu n'as pas foncé.",
    ],
    (1, 2, 2): [
        "enfant-m|Une feuille, sous le rouge.",
        "narrateur|Nino glisse une feuille, sur le sable mouillé.",
        "narrateur|Aniss tient un coin, sans parler.",
        "narrateur|Ils posent le rouge, au milieu de la feuille.",
        "narrateur|Le sable n'attrape plus le bois.",
        "narrateur|Un éclat de goutte brille, sur le vert.",
        "enfant-m|Elle le porte.",
        "maman|Vous avez posé, sans planter.",
        "narrateur|Le cube rouge reste à la surface.",
        "enfant-m|La feuille a dit non au sable.",
        "papa|Son silence a compté.",
    ],
    (1, 2, 3): [
        "enfant-m|Un quai, au bord du bac.",
        "narrateur|Nino pose le bleu, contre le rebord.",
        "narrateur|Aniss cale le jaune, sans un mot.",
        "narrateur|Ils posent le rouge, sur ce petit quai.",
        "narrateur|La flaque reste au milieu, sans l'avaler.",
        "narrateur|Un éclat de goutte brille, au rebord.",
        "enfant-m|Il a son bord sec.",
        "maman|Vous avez laissé la flaque au milieu.",
        "narrateur|Le cube rouge reste droit, au quai.",
        "enfant-m|Le bac n'a pas gagné.",
        "papa|Tu n'as pas foncé.",
    ],
    (1, 3, 1): [
        "enfant-m|Un pont, entre les laitues.",
        "narrateur|Nino pose le bleu, d'un rang à l'autre.",
        "narrateur|Il tend le jaune, sans pousser la terre.",
        "narrateur|Aniss le pose, les pieds propres.",
        "narrateur|Ils posent le rouge, sur ce pont étroit.",
        "narrateur|Un éclat de goutte brille, sous une nervure.",
        "enfant-m|Il n'est plus caché.",
        "papa|Vous avez posé, sans glisser sous la feuille.",
        "narrateur|Le filet d'arrosoir passe dessous.",
        "enfant-m|Le pont le montre.",
        "maman|Tu n'as pas foncé.",
    ],
    (1, 3, 2): [
        "enfant-m|Une feuille, pour le toit.",
        "narrateur|Nino prend une feuille large, tombée.",
        "narrateur|Aniss la tient, comme un toit.",
        "narrateur|Ils posent le rouge, dessous, à l'abri.",
        "narrateur|Le filet tape le vert, pas le bois.",
        "narrateur|Un éclat de goutte brille, sous le toit.",
        "enfant-m|Il est au sec.",
        "papa|Vous avez posé, sans cacher.",
        "narrateur|Le cube rouge reste visible, sous la feuille.",
        "enfant-m|Le toit le garde.",
        "maman|Son silence a compté.",
    ],
    (1, 3, 3): [
        "enfant-m|Un quai, entre les rangs.",
        "narrateur|Nino pose une planchette, au bord de la terre.",
        "narrateur|Aniss cale le bleu, sans un mot.",
        "narrateur|Ils posent le rouge, sur ce quai de bois.",
        "narrateur|La laitue reste à côté, sans le cacher.",
        "narrateur|Un éclat de goutte brille, sur la planchette.",
        "enfant-m|Il a son bord.",
        "papa|Vous avez laissé la terre à la terre.",
        "narrateur|Le cube rouge reste propre, au quai.",
        "enfant-m|Le potager le laisse.",
        "maman|Tu n'as pas foncé.",
    ],
    (2, 1, 1): [
        "enfant-m|Un pont, pour le bleu.",
        "narrateur|Nino pose le rouge, au-dessus du filet.",
        "narrateur|Il tend le jaune, sans se hausser.",
        "narrateur|Aniss le pose, les pieds au sol.",
        "narrateur|Ils posent le bleu, sur ce pont étroit.",
        "narrateur|Un éclat de goutte brille, sur le bois bleu.",
        "enfant-m|Il n'a plus besoin de sauter.",
        "papa|Vous avez posé, sans lever trop haut.",
        "narrateur|La goutte passe dessous, et le bleu tient.",
        "enfant-m|Le pont l'a attrapée.",
        "maman|Tu n'as pas foncé.",
    ],
    (2, 1, 2): [
        "enfant-m|Une feuille, sous le tuyau.",
        "narrateur|Nino glisse une feuille, tout bas.",
        "narrateur|Aniss tient le bord, et se tait.",
        "narrateur|Ils posent le bleu, sur la feuille.",
        "narrateur|La goutte tape le vert, pas le bois froid.",
        "narrateur|Un éclat de goutte brille, sur la nervure.",
        "enfant-m|Elle l'a eue.",
        "papa|Vous avez posé, les pieds au sol.",
        "narrateur|Le cube bleu reste droit, au milieu.",
        "enfant-m|La feuille a pris la goutte.",
        "maman|Son silence a compté.",
    ],
    (2, 1, 3): [
        "enfant-m|Un quai, plus bas que le tuyau.",
        "narrateur|Nino pose une pierre, sans se hausser.",
        "narrateur|Aniss cale le rouge, sans un mot.",
        "narrateur|Ils posent le bleu, au bord de la pierre.",
        "narrateur|Le filet passe à côté, trop loin pour tourner.",
        "narrateur|Un éclat de goutte brille, au quai bleu.",
        "enfant-m|Il a son bord.",
        "papa|Vous avez laissé le filet descendre.",
        "narrateur|Le cube bleu reste sec, d'un côté.",
        "enfant-m|Le quai le tient.",
        "maman|Tu n'as pas foncé.",
    ],
    (2, 2, 1): [
        "enfant-m|Un pont, au-dessus de la flaque.",
        "narrateur|Nino pose le rouge, puis tend le jaune.",
        "narrateur|Aniss le pose, sans coller au sable.",
        "narrateur|Ils posent le bleu, sur ce pont étroit.",
        "narrateur|La flaque reste dessous, sans l'attraper.",
        "narrateur|Un éclat de goutte brille, entre deux cubes.",
        "enfant-m|Il avance, sans s'enfoncer.",
        "maman|Vous avez posé, sans pousser.",
        "narrateur|Le cube bleu reste à la surface.",
        "enfant-m|Le pont le porte.",
        "papa|Tu n'as pas foncé.",
    ],
    (2, 2, 2): [
        "enfant-m|Une feuille, sous le bleu.",
        "narrateur|Nino glisse une feuille, sur la flaque.",
        "narrateur|Aniss tient un coin, sans parler.",
        "narrateur|Ils posent le bleu, au milieu de la feuille.",
        "narrateur|Le sable n'attrape plus le bois froid.",
        "narrateur|Un éclat de goutte brille, sur le vert.",
        "enfant-m|Elle flotte, un peu.",
        "maman|Vous avez posé, sans coller.",
        "narrateur|Le cube bleu reste visible, au milieu.",
        "enfant-m|La feuille a dit non au sable.",
        "papa|Son silence a compté.",
    ],
    (2, 2, 3): [
        "enfant-m|Un quai, au rebord du bac.",
        "narrateur|Nino pose le rouge, contre le bord.",
        "narrateur|Aniss cale le jaune, sans un mot.",
        "narrateur|Ils posent le bleu, sur ce petit quai.",
        "narrateur|La flaque reste au centre, sans l'avaler.",
        "narrateur|Un éclat de goutte brille, au rebord froid.",
        "enfant-m|Il a son bord sec.",
        "maman|Vous avez laissé la flaque au milieu.",
        "narrateur|Le cube bleu reste droit, au quai.",
        "enfant-m|Le bac n'a pas gagné.",
        "papa|Tu n'as pas foncé.",
    ],
    (2, 3, 1): [
        "enfant-m|Un pont, sans la boue.",
        "narrateur|Nino pose le rouge, d'un rang à l'autre.",
        "narrateur|Il tend le jaune, depuis le bord propre.",
        "narrateur|Aniss le pose, sans avancer dans la terre.",
        "narrateur|Ils posent le bleu, sur ce pont étroit.",
        "narrateur|Un éclat de goutte brille, sous une nervure.",
        "enfant-m|On n'a pas marché dans la boue.",
        "papa|Vous avez posé, depuis le bord.",
        "narrateur|Le filet d'arrosoir passe dessous.",
        "enfant-m|Le pont le montre.",
        "maman|Tu n'as pas foncé.",
    ],
    (2, 3, 2): [
        "enfant-m|Une feuille, pour le toit.",
        "narrateur|Nino prend une feuille large, au bord.",
        "narrateur|Aniss la tient, sans entrer dans la terre.",
        "narrateur|Ils posent le bleu, dessous, à l'abri.",
        "narrateur|Le filet tape le vert, pas le bois froid.",
        "narrateur|Un éclat de goutte brille, sous le toit.",
        "enfant-m|Il est au sec.",
        "papa|Vous avez posé, sans la boue.",
        "narrateur|Le cube bleu reste visible, sous la feuille.",
        "enfant-m|Le toit le garde.",
        "maman|Son silence a compté.",
    ],
    (2, 3, 3): [
        "enfant-m|Un quai, au bord propre.",
        "narrateur|Nino pose une planchette, hors de la boue.",
        "narrateur|Aniss cale le rouge, sans un mot.",
        "narrateur|Ils posent le bleu, sur ce quai de bois.",
        "narrateur|La terre reste à côté, sans le tacher.",
        "narrateur|Un éclat de goutte brille, sur la planchette.",
        "enfant-m|Il a son bord propre.",
        "papa|Vous avez laissé la boue à la boue.",
        "narrateur|Le cube bleu reste propre, au quai.",
        "enfant-m|Le potager le laisse.",
        "maman|Tu n'as pas foncé.",
    ],
    (3, 1, 1): [
        "enfant-m|Un pont, un peu plus loin.",
        "narrateur|Nino pose le rouge, loin du filet trop juste.",
        "narrateur|Il tend le bleu, sans le pousser.",
        "narrateur|Aniss le pose, et compte une goutte.",
        "narrateur|Ils posent le jaune, sur ce pont étroit.",
        "narrateur|Un éclat de goutte brille, sur le bois jaune.",
        "enfant-m|Il ne tourne plus.",
        "papa|Vous avez posé, loin du bord trop juste.",
        "narrateur|L'eau passe dessous, et le jaune tient.",
        "enfant-m|Le pont l'a calé.",
        "maman|Tu n'as pas foncé.",
    ],
    (3, 1, 2): [
        "enfant-m|Une feuille, pour arrêter le tournis.",
        "narrateur|Nino glisse une feuille, sous le tuyau.",
        "narrateur|Aniss tient le bord, et se tait.",
        "narrateur|Ils posent le jaune, sur la feuille.",
        "narrateur|Le filet tape le vert, et le bois reste droit.",
        "narrateur|Un éclat de goutte brille, sur la nervure.",
        "enfant-m|Il ne tourne plus.",
        "papa|Vous avez posé, sans coller au filet.",
        "narrateur|Le cube jaune reste droit, au milieu.",
        "enfant-m|La feuille l'a tenu.",
        "maman|Son silence a compté.",
    ],
    (3, 1, 3): [
        "enfant-m|Un quai, loin du filet.",
        "narrateur|Nino pose une pierre, un peu à l'écart.",
        "narrateur|Aniss cale le rouge, sans un mot.",
        "narrateur|Ils posent le jaune, au bord de la pierre.",
        "narrateur|Le filet passe à côté, trop loin pour tourner.",
        "narrateur|Un éclat de goutte brille, au quai jaune.",
        "enfant-m|Il a son bord.",
        "papa|Vous avez laissé le filet descendre.",
        "narrateur|Le cube jaune reste sec, d'un côté.",
        "enfant-m|Le quai le tient.",
        "maman|Tu n'as pas foncé.",
    ],
    (3, 2, 1): [
        "enfant-m|Un pont, sans planter.",
        "narrateur|Nino pose le rouge, à plat, sur le sable.",
        "narrateur|Il tend le bleu, sans enfoncer.",
        "narrateur|Aniss le pose, la paume à plat.",
        "narrateur|Ils posent le jaune, dessus, tout léger.",
        "narrateur|Un éclat de goutte brille, entre deux cubes.",
        "enfant-m|Il n'est plus un piquet.",
        "maman|Vous avez posé, sans planter.",
        "narrateur|Le sable reste dessous, et le jaune tient.",
        "enfant-m|Le pont le porte.",
        "papa|Tu n'as pas foncé.",
    ],
    (3, 2, 2): [
        "enfant-m|Une feuille, sous le jaune.",
        "narrateur|Nino glisse une feuille, sur le sable.",
        "narrateur|Aniss tient un coin, la paume à plat.",
        "narrateur|Ils posent le jaune, au milieu de la feuille.",
        "narrateur|Le bois ne s'enfonce plus, comme un piquet.",
        "narrateur|Un éclat de goutte brille, sur le vert.",
        "enfant-m|Je le revois.",
        "maman|Vous avez posé, sans cacher.",
        "narrateur|Le cube jaune reste à la surface.",
        "enfant-m|La feuille l'a montré.",
        "papa|Son silence a compté.",
    ],
    (3, 2, 3): [
        "enfant-m|Un quai, au rebord du bac.",
        "narrateur|Nino pose le rouge, contre le bord.",
        "narrateur|Aniss cale le bleu, sans un mot.",
        "narrateur|Ils posent le jaune, sur ce petit quai.",
        "narrateur|Le sable du milieu n'attrape plus le bois.",
        "narrateur|Un éclat de goutte brille, au rebord.",
        "enfant-m|Il a son bord sec.",
        "maman|Vous avez laissé le sable au milieu.",
        "narrateur|Le cube jaune reste droit, au quai.",
        "enfant-m|Le bac n'a pas gagné.",
        "papa|Tu n'as pas foncé.",
    ],
    (3, 3, 1): [
        "enfant-m|Un pont, au-dessus de la cachette.",
        "narrateur|Nino pose le rouge, d'un rang à l'autre.",
        "narrateur|Il tend le bleu, sans glisser sous la feuille.",
        "narrateur|Aniss le pose, et soulève un bord.",
        "narrateur|Ils posent le jaune, sur ce pont étroit.",
        "narrateur|Un éclat de goutte brille, sous une nervure.",
        "enfant-m|Il n'est plus caché.",
        "papa|Vous avez posé, sans le glisser dessous.",
        "narrateur|La laitue reste à côté, trop basse.",
        "enfant-m|Le pont le montre.",
        "maman|Tu n'as pas foncé.",
    ],
    (3, 3, 2): [
        "enfant-m|Une feuille, pour le toit, pas la cachette.",
        "narrateur|Nino prend une feuille large, tombée.",
        "narrateur|Aniss la tient haute, comme un toit.",
        "narrateur|Ils posent le jaune, dessous, visible.",
        "narrateur|La laitue n'avale plus le bois.",
        "narrateur|Un éclat de goutte brille, sous le toit.",
        "enfant-m|Je le vois, là.",
        "papa|Vous avez posé, sans cacher.",
        "narrateur|Le cube jaune reste visible, sous la feuille.",
        "enfant-m|Le toit le garde.",
        "maman|Son silence a compté.",
    ],
    (3, 3, 3): [
        "enfant-m|Un quai, hors de la feuille.",
        "narrateur|Nino pose une planchette, au bord du rang.",
        "narrateur|Aniss cale le rouge, sans un mot.",
        "narrateur|Ils posent le jaune, sur ce quai de bois.",
        "narrateur|La laitue reste à côté, trop loin pour cacher.",
        "narrateur|Un éclat de goutte brille, sur la planchette.",
        "enfant-m|Il a son bord.",
        "papa|Vous avez laissé la feuille à la feuille.",
        "narrateur|Le cube jaune reste propre, au quai.",
        "enfant-m|Le potager le laisse.",
        "maman|Tu n'as pas foncé.",
    ],
}

END_SONS = {1: "gouttiere,bois", 2: "bac,bois", 3: "potager,bois"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le cube rouge tient, sur le pont.",
        "enfant-m|On a posé, sans bousculer.",
        "papa|Le filet est passé dessous.",
        "maman|Aniss a posé le jaune.",
        "narrateur|Ça a failli trop glisser.",
        "enfant-m|Surtout le moment du filet.",
        "narrateur|Un éclat de goutte sèche sur le pont rouge.",
    ],
    (1, 1, 2): [
        "narrateur|Le cube rouge tient, sous la feuille.",
        "enfant-m|On a posé, sans lever trop haut.",
        "papa|La goutte a tapé le vert.",
        "maman|Aniss a tenu le bord.",
        "narrateur|Ça a failli trop près du tuyau.",
        "enfant-m|Surtout le moment de la feuille.",
        "narrateur|Un éclat de goutte tient sous la feuille, au rouge.",
    ],
    (1, 1, 3): [
        "narrateur|Le cube rouge tient, au quai de pierre.",
        "enfant-m|On a laissé l'eau à côté.",
        "papa|La pierre a fait le bord.",
        "maman|Aniss a calé sans parler.",
        "narrateur|Ça a failli trop coller au filet.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte brille au quai, sur le rouge.",
    ],
    (1, 2, 1): [
        "narrateur|Le cube rouge tient, au-dessus du sable.",
        "enfant-m|On a posé, sans lâcher.",
        "papa|Le pont n'a pas enfoncé.",
        "maman|Aniss a posé le jaune à plat.",
        "narrateur|Ça a failli trop avaler.",
        "enfant-m|Surtout le moment du bac.",
        "narrateur|Un éclat de goutte reste entre deux cubes, dans le bac.",
    ],
    (1, 2, 2): [
        "narrateur|Le cube rouge tient, sur la feuille du bac.",
        "enfant-m|On a posé, sans planter.",
        "papa|Le sable n'a pas attrapé le bois.",
        "maman|Aniss a tenu un coin.",
        "narrateur|Ça a failli trop s'enfoncer.",
        "enfant-m|Surtout le moment de la feuille.",
        "narrateur|Un éclat de goutte tremble sur la feuille, au sable.",
    ],
    (1, 2, 3): [
        "narrateur|Le cube rouge tient, au rebord du bac.",
        "enfant-m|On a laissé la flaque au milieu.",
        "papa|Le quai n'a pas versé.",
        "maman|Aniss a calé le jaune.",
        "narrateur|Ça a failli trop au centre.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte sèche au bord du bac, rouge.",
    ],
    (1, 3, 1): [
        "narrateur|Le cube rouge tient, entre les rangs.",
        "enfant-m|On a posé, sans le cacher.",
        "papa|Le pont a montré le bois.",
        "maman|Aniss a gardé les pieds propres.",
        "narrateur|Ça a failli trop sous la laitue.",
        "enfant-m|Surtout le moment du pont.",
        "narrateur|Un éclat de goutte brille sous une laitue, sur le pont.",
    ],
    (1, 3, 2): [
        "narrateur|Le cube rouge tient, sous le toit de feuille.",
        "enfant-m|On a posé, sans cacher.",
        "papa|Le filet a tapé le vert.",
        "maman|Aniss a tenu le toit.",
        "narrateur|Ça a failli trop entre les choux.",
        "enfant-m|Surtout le moment du toit.",
        "narrateur|Un éclat de goutte tient à la feuille, entre les choux.",
    ],
    (1, 3, 3): [
        "narrateur|Le cube rouge tient, sur la planchette.",
        "enfant-m|On a laissé la terre à la terre.",
        "papa|Le quai n'a pas glissé.",
        "maman|Aniss a calé le bleu.",
        "narrateur|Ça a failli trop dans le rang.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte sèche au quai du potager, rouge.",
    ],
    (2, 1, 1): [
        "narrateur|Le cube bleu tient, sur le pont.",
        "enfant-m|On a posé, sans se hausser.",
        "papa|Les pieds sont restés au sol.",
        "maman|Aniss a posé le jaune.",
        "narrateur|Ça a failli trop haut.",
        "enfant-m|Surtout le moment du tuyau.",
        "narrateur|Un éclat de goutte sèche sur le pont bleu.",
    ],
    (2, 1, 2): [
        "narrateur|Le cube bleu tient, sous la feuille.",
        "enfant-m|On a posé, les pieds au sol.",
        "papa|La goutte a tapé le vert.",
        "maman|Aniss a tenu le bord.",
        "narrateur|Ça a failli trop lever.",
        "enfant-m|Surtout le moment de la feuille.",
        "narrateur|Un éclat de goutte tient sous la feuille, au bleu.",
    ],
    (2, 1, 3): [
        "narrateur|Le cube bleu tient, au quai de pierre.",
        "enfant-m|On a laissé le filet descendre.",
        "papa|La pierre a fait le bord bas.",
        "maman|Aniss a calé le rouge.",
        "narrateur|Ça a failli trop se hausser.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte brille au quai, sur le bleu.",
    ],
    (2, 2, 1): [
        "narrateur|Le cube bleu tient, au-dessus de la flaque.",
        "enfant-m|On a posé, sans pousser.",
        "papa|Le pont n'a pas collé.",
        "maman|Aniss a posé le jaune à plat.",
        "narrateur|Ça a failli trop dans l'eau.",
        "enfant-m|Surtout le moment du pont.",
        "narrateur|Un éclat de goutte reste entre deux cubes, sur la flaque.",
    ],
    (2, 2, 2): [
        "narrateur|Le cube bleu tient, sur la feuille de la flaque.",
        "enfant-m|On a posé, sans coller.",
        "papa|Le sable n'a pas attrapé le bleu.",
        "maman|Aniss a tenu un coin.",
        "narrateur|Ça a failli trop vers l'eau.",
        "enfant-m|Surtout le moment de la feuille.",
        "narrateur|Un éclat de goutte tremble sur la feuille, au bleu.",
    ],
    (2, 2, 3): [
        "narrateur|Le cube bleu tient, au rebord du bac.",
        "enfant-m|On a laissé la flaque au centre.",
        "papa|Le quai n'a pas versé.",
        "maman|Aniss a calé le jaune.",
        "narrateur|Ça a failli trop au milieu.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte sèche au bord du bac, bleu.",
    ],
    (2, 3, 1): [
        "narrateur|Le cube bleu tient, depuis le bord propre.",
        "enfant-m|On n'a pas marché dans la boue.",
        "papa|Le pont est parti du bord.",
        "maman|Aniss n'a pas avancé.",
        "narrateur|Ça a failli trop dans la terre.",
        "enfant-m|Surtout le moment du pont.",
        "narrateur|Un éclat de goutte brille sous une laitue, sur le bleu.",
    ],
    (2, 3, 2): [
        "narrateur|Le cube bleu tient, sous le toit, hors de la boue.",
        "enfant-m|On a posé, sans la terre.",
        "papa|Le filet a tapé le vert.",
        "maman|Aniss a tenu le toit au bord.",
        "narrateur|Ça a failli trop dans la boue.",
        "enfant-m|Surtout le moment du toit.",
        "narrateur|Un éclat de goutte tient à la feuille, hors de la boue.",
    ],
    (2, 3, 3): [
        "narrateur|Le cube bleu tient, sur la planchette propre.",
        "enfant-m|On a laissé la boue à la boue.",
        "papa|Le quai n'a pas glissé.",
        "maman|Aniss a calé le rouge.",
        "narrateur|Ça a failli trop au filet d'arrosoir.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte sèche au quai du potager, bleu.",
    ],
    (3, 1, 1): [
        "narrateur|Le cube jaune tient, loin du filet trop juste.",
        "enfant-m|On a posé, sans le tournis.",
        "papa|Le pont a calé le bois.",
        "maman|Aniss a compté une goutte.",
        "narrateur|Ça a failli trop près du tuyau.",
        "enfant-m|Surtout le moment du pont.",
        "narrateur|Un éclat de goutte sèche sur le pont jaune.",
    ],
    (3, 1, 2): [
        "narrateur|Le cube jaune tient, droit, sous la feuille.",
        "enfant-m|On a posé, sans coller au filet.",
        "papa|La feuille a arrêté le tournis.",
        "maman|Aniss a tenu le bord.",
        "narrateur|Ça a failli trop tourner.",
        "enfant-m|Surtout le moment de la feuille.",
        "narrateur|Un éclat de goutte tient sous la feuille, au jaune.",
    ],
    (3, 1, 3): [
        "narrateur|Le cube jaune tient, à l'écart du filet.",
        "enfant-m|On a laissé le filet descendre.",
        "papa|La pierre a fait le bord loin.",
        "maman|Aniss a calé le rouge.",
        "narrateur|Ça a failli trop juste.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte brille au quai, sur le jaune.",
    ],
    (3, 2, 1): [
        "narrateur|Le cube jaune tient, à plat, sur le pont.",
        "enfant-m|On a posé, sans planter.",
        "papa|Le pont n'est pas un piquet.",
        "maman|Aniss a posé la paume à plat.",
        "narrateur|Ça a failli trop s'enfoncer.",
        "enfant-m|Surtout le moment du pont.",
        "narrateur|Un éclat de goutte reste entre deux cubes, au jaune.",
    ],
    (3, 2, 2): [
        "narrateur|Le cube jaune tient, visible, sur la feuille.",
        "enfant-m|On a posé, sans cacher.",
        "papa|Le sable n'a pas avalé le jaune.",
        "maman|Aniss a tenu un coin à plat.",
        "narrateur|Ça a failli trop comme un piquet.",
        "enfant-m|Surtout le moment de la feuille.",
        "narrateur|Un éclat de goutte tremble sur la feuille, au jaune.",
    ],
    (3, 2, 3): [
        "narrateur|Le cube jaune tient, au rebord du bac.",
        "enfant-m|On a laissé le sable au milieu.",
        "papa|Le quai n'a pas versé.",
        "maman|Aniss a calé le bleu.",
        "narrateur|Ça a failli trop planter.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte sèche au bord du bac, jaune.",
    ],
    (3, 3, 1): [
        "narrateur|Le cube jaune tient, au-dessus de la cachette.",
        "enfant-m|On a posé, sans le glisser dessous.",
        "papa|Le pont a montré le bois.",
        "maman|Aniss a soulevé un bord.",
        "narrateur|Ça a failli trop sous la laitue.",
        "enfant-m|Surtout le moment du pont.",
        "narrateur|Un éclat de goutte brille sous une laitue, sur le jaune.",
    ],
    (3, 3, 2): [
        "narrateur|Le cube jaune tient, visible, sous le toit.",
        "enfant-m|On a posé, sans cacher.",
        "papa|Le toit n'est pas une cachette.",
        "maman|Aniss a tenu la feuille haute.",
        "narrateur|Ça a failli trop sous le vert.",
        "enfant-m|Surtout le moment du toit.",
        "narrateur|Un éclat de goutte tient à la feuille, au jaune visible.",
    ],
    (3, 3, 3): [
        "narrateur|Le cube jaune tient, hors de la feuille.",
        "enfant-m|On a laissé la feuille à la feuille.",
        "papa|Le quai n'a pas glissé.",
        "maman|Aniss a calé le rouge.",
        "narrateur|Ça a failli trop sous la laitue.",
        "enfant-m|Surtout le moment du quai.",
        "narrateur|Un éclat de goutte sèche au quai du potager, jaune.",
    ],
}


def t2_question(t1: int) -> list[str]:
    return [f"narrateur|{T1[t1]['voy']}"] + T2_Q


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "goutte,cuisine",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le cube rouge", "le cube bleu", "le cube jaune")},
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
            {"fields": t3lab("la gouttière", "le bac", "le potager")},
        )
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[sp] = voice(
                by_src[sp], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{sp}_T0003_P0000"] = voice(
                by_src[f"{sp}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab("le pont", "la feuille", "le quai")},
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
                    {"emphasis": "éclat de goutte"},
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
        "bateau",
        "miel",
        "merle",
        "tout doux",
        "tout calme",
        "toute ronde",
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
        "éclat de zinc",
        "éclat de thym",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "éclat de goutte" not in blob and "eclat de goutte" not in blob:
        raise SystemExit(f"{SID}: éclat de goutte absent")
    if "cube rouge" not in blob or "cube bleu" not in blob or "cube jaune" not in blob:
        raise SystemExit(f"{SID}: un cube manque")

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
        if "éclat de goutte" not in last and "eclat de goutte" not in last:
            raise SystemExit(f"{SID} {c['chunk_id']} éclat absent en fin: {last}")
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
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — partage / participation (vécue, jamais dite)\n"
        "- **Personnages :** Nino, Aniss, papa, maman\n"
        "- **Lieu :** cuisine après la pluie, puis le jardin (gouttière, bac, potager)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte tape les cubes dans la cuisine. Un **éclat de goutte** reste collé. "
        "Nino veut poser **LE cube** avec Aniss, **avant la prochaine goutte**. "
        "Aniss arrive sans un mot : Nino propose, Aniss prend son temps, le silence répond. "
        "Première idée trop vite : le cube glisse, l'éclat s'étale. "
        "T1 : cube rouge / bleu / jaune — **les trois partent**. "
        "T2 : gouttière / bac / potager — trop vite, la goutte bouscule, le sable avale, "
        "la laitue cache. 2e ruse : l'éclat du début montre la place. "
        "Aniss pointe, sans parler. Nino refuse de foncer. "
        "T3 : pont / feuille / quai (eau, gouttière, cubes). Le cube tient. "
        "Ça a failli ne pas arriver. Monde ≠ TREE-COL-013 (pas de bateau sur la vitre) "
        "≠ TREE-AUT-011 (pas de seau de ferme).\n\n"
        "## Vécu\n\n"
        "Nino veut poser **maintenant**. Aniss veut regarder l'éclat. "
        "Sourire disparu, poitrine serrée, adulte accroupi. "
        "Chaque choix change l'obstacle et le climax. La leçon se voit : "
        "tendre sans pousser, poser à deux, le silence d'Aniss compte. "
        "Indice d'ouverture payé : éclat de goutte. Fin : cube + trace unique.\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit 65 % jeté (toute ronde, zinc-refrain, bateau de cubes, « tout doux / encore / déjà »).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (voir les mains d'Aniss). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
