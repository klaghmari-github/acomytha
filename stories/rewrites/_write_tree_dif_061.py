#!/usr/bin/env python3
"""TREE-DIF-061 — Le moulin de papier d'Aniss et la grille de l'école (F-NAR-019, N3, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-061"
N3 = 16
TITLE = "Le moulin de papier d'Aniss et la grille de l'école"
FIL = (
    "Sur le chemin de l'école, Aniss veut planter son moulin de papier "
    "à la grille, avant que le vent du matin ne se couche sous le porche. "
    "Une goutte de cire rouge tient une pale. Mila veut qu'il crie tourne ; "
    "Aniss répond avec les mains. Moulin, fil, caillou : les trois partent. "
    "Grille trop serrée, caniveau trop vite, porche trop sage. "
    "Neuf façons. La goutte de cire rouge prend le vent, enfin."
)
CHARS = "Aniss, Mila, papa, maman"
SETTING = "chemin de l'école : grille, caniveau, porche"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "goutte de cire rouge",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_joyeuse; intensite=1; destinataire=enfant; sous_texte=le_moulin_veut_tourner_à_la_grille; tempo=naturel; sourire=léger; respiration=ample",
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
        "emphasis": "goutte de cire rouge",
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
        "emphasis": "goutte de cire rouge",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=ils_ne_veulent_pas_la_même_chose; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "goutte de cire rouge",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=Aniss_tend_Mila_attend_le_moulin_tourne; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "goutte de cire rouge",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_goutte_de_cire_rouge_prend_le_vent; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Un bus passe, trop large, le long du muret.",
    "narrateur|Dans le sac d'Aniss, le papier répond, tout sec.",
    "narrateur|Le bitume fume, un peu mouillé, sous les bottes.",
    "narrateur|Une odeur de pain chaud remonte le muret.",
    "papa|Le boulanger a ouvert, Aniss.",
    "narrateur|La grille de l'école brille, un peu froide.",
    "narrateur|Le porche garde son ombre, plus loin.",
    "maman|Ton moulin dépasse du sac.",
    "narrateur|Aniss sort le bâton, et la goutte de cire rouge.",
    "papa|Cette goutte, tu l'as mise hier soir.",
    "enfant-m|Elle tient la pale, contre le vent.",
    "narrateur|En ce moment, Aniss serre le bâton contre sa veste.",
    "enfant-m|Je le plante à la grille, avant le porche.",
    "narrateur|Mila arrive, les bottes trop pressées.",
    "papa|Mila arrive, tu lui montres ?",
    "narrateur|Aniss hoche la tête, tout petit.",
    "narrateur|Les bottes de Mila tapent le bitume, derrière.",
    "copine|Dis tourne, Aniss !",
    "narrateur|Aniss lève le moulin trop vite, vers la grille.",
    "narrateur|Le bâton bute contre deux barreaux, trop serrés.",
    "enfant-m|Il ne passe pas.",
    "narrateur|Le sourire d'Aniss disparaît, un instant.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|On prépare, puis on pose.",
    "narrateur|Papa s'accroupit, à la hauteur d'Aniss.",
    "papa|Merci, tu as tendu le papier, sans crier.",
    "maman|Le fil et le caillou voyagent aussi.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près des pieds.",
    "narrateur|Le moulin, le fil, le caillou.",
    "papa|Tu prends quoi d'abord, Aniss ?",
]

T1 = {
    1: {
        "lab": "le moulin",
        "sons": "papier,vent",
        "emphasis": "moulin",
        "passage": [
            "narrateur|Aniss sort d'abord le moulin du sac.",
            "enfant-m|Il est froid, contre mes doigts.",
            "papa|La goutte de cire rouge tient une pale.",
            "narrateur|Il le tend vers Mila, tout près.",
            "copine|Dis tourne !",
            "narrateur|Aniss ouvre la bouche, puis la referme.",
            "narrateur|Il pose deux doigts sur le papier.",
            "enfant-m|Pas trop vite.",
            "maman|Le fil et le caillou voyagent aussi.",
            "narrateur|Papa glisse le tout contre le sac.",
            "copine|Aniss, on court ?",
            "narrateur|Aniss hoche la tête, tout petit.",
            "papa|Le moulin d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Aniss a tendu le moulin, tout près.",
            "maman|Il tend quoi, à Mila ?",
        ],
        "qfields": {
            "expected_answer": "moulin",
            "accepted_examples": "moulin | le moulin | le papier | tendre",
            "retry_prompt": "Il tend le moulin. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde le moulin contre lui.",
            "copine|Il est à toi, un moment.",
            "narrateur|Mila attend, les mains ouvertes.",
            "narrateur|Une pale tremble, toute petite, au vent.",
            "maman|La goutte de cire rouge est tiède, maintenant.",
            "papa|On pose le moulin où ?",
            "copine|Vers la grille, peut-être.",
            "narrateur|Le fil et le caillou tapent le sac, à chaque pas.",
        ],
    },
    2: {
        "lab": "le fil",
        "sons": "fil,bobine",
        "emphasis": "fil",
        "passage": [
            "narrateur|Aniss sort d'abord le fil beige.",
            "enfant-m|Il gratte un peu, contre le pouce.",
            "maman|La bobine sent le tiroir, un peu.",
            "narrateur|Il tend le fil vers Mila.",
            "copine|Dis nœud !",
            "narrateur|Aniss enroule un tour, sans un mot.",
            "narrateur|Le fil se tait autour du bâton.",
            "papa|Le moulin et le caillou voyagent aussi.",
            "narrateur|Maman les pose contre le papier.",
            "copine|Aniss, tu viens ?",
            "narrateur|Aniss lève le fil, tout bas.",
            "enfant-m|Pas trop vite.",
            "maman|Le fil d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Aniss a tendu le fil, tout près.",
            "papa|Il tend quoi, à Mila ?",
        ],
        "qfields": {
            "expected_answer": "fil",
            "accepted_examples": "fil | le fil | la bobine | tendre",
            "retry_prompt": "Il tend le fil. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde le fil contre sa jambe.",
            "copine|Il est à toi, un moment.",
            "narrateur|Mila attend, sans répéter.",
            "narrateur|La bobine sent le tiroir, un peu.",
            "maman|La goutte de cire rouge écoute le fil.",
            "papa|On pose le moulin où ?",
            "copine|Vers le caniveau, peut-être.",
            "narrateur|Le moulin et le caillou tapent le sac, à chaque pas.",
        ],
    },
    3: {
        "lab": "le caillou",
        "sons": "caillou,pierre",
        "emphasis": "caillou",
        "passage": [
            "narrateur|Aniss sort d'abord le caillou rond.",
            "enfant-m|Il est tiède, contre la paume.",
            "papa|La pierre a séché près du muret.",
            "narrateur|Il tend le caillou vers Mila.",
            "copine|Dis pierre !",
            "narrateur|Aniss le cale contre le bâton, sans presser.",
            "narrateur|Le papier se tient, sans un mot.",
            "maman|Le moulin et le fil voyagent aussi.",
            "narrateur|Papa les glisse près des bottes.",
            "copine|Aniss, c'est bon ?",
            "narrateur|Aniss appuie sur la pierre, tout petit.",
            "enfant-m|Pas trop vite.",
            "papa|Le caillou d'abord, il tient.",
        ],
        "question": [
            "narrateur|Aniss a tendu le caillou, tout près.",
            "maman|Il tend quoi, à Mila ?",
        ],
        "qfields": {
            "expected_answer": "caillou",
            "accepted_examples": "caillou | le caillou | la pierre | tendre",
            "retry_prompt": "Il tend le caillou. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss tient le caillou, tout près.",
            "copine|Il est à toi, un moment.",
            "narrateur|Mila attend, les lèvres fermées.",
            "narrateur|Un peu de poussière tombe, puis s'arrête.",
            "papa|La goutte de cire rouge écoute la pierre.",
            "maman|On pose le moulin où ?",
            "copine|Vers le porche, tout bas.",
            "narrateur|Le moulin et le fil tapent le sac, à chaque pas.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le moulin tape un peu le sac, à chaque pas.",
        "narrateur|La grille serre trop les barreaux.",
        "narrateur|Le caniveau emporte trop d'eau, plus bas.",
        "narrateur|Sous le porche, l'air ne pousse plus.",
        "papa|On commence où, pour le moulin ?",
    ],
    2: [
        "narrateur|Le fil tape un peu la jambe, à chaque pas.",
        "narrateur|La grille serre trop les barreaux.",
        "narrateur|Le caniveau emporte trop d'eau, plus bas.",
        "narrateur|Sous le porche, l'air ne pousse plus.",
        "papa|On commence où, pour le moulin ?",
    ],
    3: [
        "narrateur|Le caillou tape un peu la botte, à chaque pas.",
        "narrateur|La grille serre trop les barreaux.",
        "narrateur|Le caniveau emporte trop d'eau, plus bas.",
        "narrateur|Sous le porche, l'air ne pousse plus.",
        "papa|On commence où, pour le moulin ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "fer,barreaux",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Le bâton du moulin bute contre deux barreaux.",
            "narrateur|La grille serre trop, juste à hauteur d'Aniss.",
            "copine|Pousse-le, Aniss !",
            "narrateur|Aniss montre un écart plus bas, du doigt.",
            "narrateur|Le fer reste froid, trop près des pales.",
            "copine|Dis-moi où !",
            "narrateur|Aniss secoue la tête, tout petit.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila se tait, et son silence compte.",
            "maman|Il montre, avec le doigt.",
            "papa|Le crochet du loquet brille un peu.",
            "narrateur|La goutte de cire rouge s'est cachée derrière un barreau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "fil,fer",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Le fil se coince entre deux barreaux froids.",
            "narrateur|La grille serre trop, juste à hauteur d'Aniss.",
            "copine|Tire-le, Aniss !",
            "narrateur|Aniss montre un écart plus bas, du doigt.",
            "narrateur|Le beige racle le fer, trop près.",
            "copine|Dis-moi où !",
            "narrateur|Aniss secoue la tête, tout petit.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila se tait, et son silence compte.",
            "maman|Il montre, avec le doigt.",
            "papa|Le crochet du loquet brille un peu.",
            "narrateur|La goutte de cire rouge s'est cachée derrière un barreau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "caillou,fer",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Le caillou reste coincé, trop large pour le fer.",
            "narrateur|La grille serre trop, juste à hauteur d'Aniss.",
            "copine|Force, Aniss !",
            "narrateur|Aniss montre un écart plus bas, du doigt.",
            "narrateur|La pierre cogne, puis recule.",
            "copine|Dis-moi où !",
            "narrateur|Aniss secoue la tête, tout petit.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila se tait, et son silence compte.",
            "maman|Il montre, avec le doigt.",
            "papa|Le crochet du loquet brille un peu.",
            "narrateur|La goutte de cire rouge s'est cachée derrière un barreau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "eau,papier",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Une pale du moulin touche l'eau, trop vite.",
            "copine|L'eau est trop grande.",
            "narrateur|Une feuille jaune part, plus bas.",
            "copine|Attrape, Aniss !",
            "narrateur|Aniss recule le papier, sans presser.",
            "narrateur|L'eau frappe la dalle, puis rebondit.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|La dalle tient le courant.",
            "papa|On reste près du caniveau, tous les deux.",
            "narrateur|La goutte de cire rouge s'est ternie, trop près de l'eau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "eau,fil",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Le fil traîne dans l'eau, trop vite.",
            "copine|L'eau est trop grande.",
            "narrateur|Une feuille jaune part, plus bas.",
            "copine|Tire, Aniss !",
            "narrateur|Aniss ramène le beige, sans presser.",
            "narrateur|L'eau frappe la dalle, puis rebondit.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|La dalle tient le courant.",
            "papa|On reste près du caniveau, tous les deux.",
            "narrateur|La goutte de cire rouge s'est ternie, trop près de l'eau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "eau,pierre",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Le caillou glisse vers l'eau, trop vite.",
            "copine|L'eau est trop grande.",
            "narrateur|Une feuille jaune part, plus bas.",
            "copine|Attrape la pierre !",
            "narrateur|Aniss recule le caillou, sans presser.",
            "narrateur|L'eau frappe la dalle, puis rebondit.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|La dalle tient le courant.",
            "papa|On reste près du caniveau, tous les deux.",
            "narrateur|La goutte de cire rouge s'est ternie, trop près de l'eau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "porche,air",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Les pales du moulin s'arrêtent sous le porche.",
            "copine|Ça ne tourne plus, Aniss !",
            "narrateur|Mila souffle trop vite, trop fort.",
            "copine|Dis vent !",
            "narrateur|Aniss pointe la porte, du doigt.",
            "narrateur|Le porche garde l'air, trop fermé.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila se tait, les joues gonflées.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|La marche du seuil est sèche.",
            "narrateur|La goutte de cire rouge s'est éteinte, dans l'ombre.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "fil,porche",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Le fil pend, trop lourd, sous le porche.",
            "copine|Ça ne tourne plus, Aniss !",
            "narrateur|Mila souffle trop vite, trop fort.",
            "copine|Dis vent !",
            "narrateur|Aniss pointe la porte, du doigt.",
            "narrateur|Le porche garde l'air, trop fermé.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila se tait, les joues gonflées.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|La marche du seuil est sèche.",
            "narrateur|La goutte de cire rouge s'est éteinte, dans l'ombre.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "pierre,porche",
        "emphasis": "goutte de cire rouge",
        "passage": [
            "narrateur|Le caillou reste lourd, sous le porche.",
            "copine|Ça ne tourne plus, Aniss !",
            "narrateur|Mila souffle trop vite, trop fort.",
            "copine|Dis vent !",
            "narrateur|Aniss pointe la porte, du doigt.",
            "narrateur|Le porche garde l'air, trop fermé.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Mila se tait, les joues gonflées.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|La marche du seuil est sèche.",
            "narrateur|La goutte de cire rouge s'est éteinte, dans l'ombre.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("le bas", "les mains de Mila", "le crochet"),
    2: ("la dalle", "le fil", "le bord"),
    3: ("le vent", "la marche", "le nœud"),
}

T3_CHOICE = {
    1: [
        "narrateur|Les barreaux restent trop serrés.",
        "narrateur|La goutte de cire rouge s'est perdue dans le fer.",
        "papa|Le bas, les mains, ou le crochet ?",
    ],
    2: [
        "narrateur|L'eau tient la feuille jaune.",
        "narrateur|La goutte de cire rouge s'est ternie près de l'eau.",
        "maman|La dalle, le fil, ou le bord ?",
    ],
    3: [
        "narrateur|L'air reste trop sage, sous le porche.",
        "narrateur|La goutte de cire rouge s'est cachée dans l'ombre.",
        "papa|Le vent, la marche, ou le nœud ?",
    ],
}

T3_SONS = {
    (1, 1): "fer,bas",
    (1, 2): "mains,papier",
    (1, 3): "crochet,loquet",
    (2, 1): "dalle,eau",
    (2, 2): "fil,eau",
    (2, 3): "bord,pas",
    (3, 1): "porte,vent",
    (3, 2): "marche,seuil",
    (3, 3): "noeud,porche",
}

T3_EMPH = {
    1: {1: "bas", 2: "mains", 3: "crochet"},
    2: {1: "dalle", 2: "fil", 3: "bord"},
    3: {1: "vent", 2: "marche", 3: "nœud"},
}

OBJ_LINE = {
    1: "Le moulin attend, collé aux doigts.",
    2: "Le fil attend, autour du bâton.",
    3: "Le caillou attend, contre le papier.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    obj = OBJ_LINE[a]
    if b == 1 and c == 1:
        wait = {
            1: "Le moulin reste bas, près du bitume.",
            2: "Le fil reste bas, près du bitume.",
            3: "Le caillou reste bas, près du bitume.",
        }[a]
        return [
            "copine|On attend.",
            "narrateur|Aniss cherche l'écart du bas, sans presser.",
            "narrateur|Mila suit le doigt, enfin, un peu.",
            f"narrateur|{wait}",
            "narrateur|Aniss glisse le bâton, sans un mot.",
            "narrateur|Le fer fait toc, plus large.",
            "copine|Toc.",
            "narrateur|La goutte de cire rouge revoit le vent, ronde.",
            f"narrateur|{obj}",
            "papa|Le bas laisse un vrai passage.",
            "enfant-m|Il tourne.",
        ]
    if b == 1 and c == 2:
        hold = {
            1: "Le moulin glisse vers les mains de Mila.",
            2: "Le fil guide le papier vers Mila.",
            3: "Le caillou suit le papier vers Mila.",
        }[a]
        return [
            "copine|Pour toi.",
            "narrateur|Mila ouvre les deux mains, tout près.",
            "narrateur|Aniss pose le jaune contre ses paumes.",
            f"narrateur|{hold}",
            "narrateur|Mila vise l'écart, Aniss pousse le bâton.",
            "copine|Il passe !",
            "narrateur|La goutte de cire rouge échappe au fer, ronde.",
            f"narrateur|{obj}",
            "maman|Tes mains ont trouvé le fer.",
            "papa|Il l'a tendu, d'abord.",
            "enfant-m|Il tourne.",
        ]
    if b == 1 and c == 3:
        hook = {
            1: "Le moulin pend au crochet du loquet.",
            2: "Le fil s'enroule au crochet du loquet.",
            3: "Le caillou cale le crochet du loquet.",
        }[a]
        return [
            "copine|Le crochet, Aniss.",
            "narrateur|Aniss lève le jaune, sans un mot.",
            "narrateur|Mila attend, puis suit sa main.",
            f"narrateur|{hook}",
            "narrateur|Une pale racle le fer, puis se libère.",
            "copine|Il tient.",
            "narrateur|La goutte de cire rouge reprend le rai, petite.",
            f"narrateur|{obj}",
            "papa|Le loquet a gardé le papier.",
            "maman|Les barreaux peuvent dormir, plus loin.",
            "enfant-m|Il tourne.",
        ]
    if b == 2 and c == 1:
        stone = {
            1: "Le moulin sèche contre la dalle.",
            2: "Le fil sèche contre la dalle.",
            3: "Le caillou sèche contre la dalle.",
        }[a]
        return [
            "copine|On attend l'eau.",
            "narrateur|Aniss s'assoit près du caniveau, sans presser.",
            "narrateur|Mila s'assoit aussi, les genoux contre lui.",
            f"narrateur|{stone}",
            "narrateur|L'eau frappe, puis la feuille s'arrête.",
            "copine|Maintenant.",
            "narrateur|La goutte de cire rouge sèche, ronde, sur la dalle.",
            f"narrateur|{obj}",
            "papa|La dalle a cassé le courant.",
            "maman|Vous avez laissé l'eau finir.",
            "enfant-m|Il tourne.",
        ]
    if b == 2 and c == 2:
        rope = {
            1: "Le moulin traverse au bout du fil.",
            2: "Le fil part au bout des mains de Mila.",
            3: "Le caillou guide le fil, tout droit.",
        }[a]
        return [
            "copine|Tes mains, Aniss.",
            "narrateur|Aniss tend le fil, tout près.",
            "narrateur|Mila tire avec lui, sans presser.",
            f"narrateur|{rope}",
            "narrateur|Le papier passe au-dessus de l'eau.",
            "copine|On tient ensemble.",
            "narrateur|La goutte de cire rouge tremble au bout du fil.",
            f"narrateur|{obj}",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|L'eau restera après.",
            "enfant-m|Il tourne.",
        ]
    if b == 2 and c == 3:
        edge = {
            1: "Le moulin suit le bord sec.",
            2: "Le fil suit le bord sec.",
            3: "Le caillou suit le bord sec.",
        }[a]
        return [
            "copine|Le bord, d'abord.",
            "narrateur|Mila tend la pierre sèche vers Aniss.",
            "narrateur|Aniss marche, sans un mot.",
            f"narrateur|{edge}",
            "narrateur|Une goutte rejoint le fond, puis se tait.",
            "copine|C'est doux.",
            "narrateur|La goutte de cire rouge reste au sec, sur le bord.",
            f"narrateur|{obj}",
            "maman|L'eau garde son souffle, plus loin.",
            "papa|Le bord a laissé le papier.",
            "enfant-m|Il tourne.",
        ]
    if b == 3 and c == 1:
        draft = {
            1: "Le moulin prend le vent de la porte.",
            2: "Le fil prend le vent de la porte.",
            3: "Le caillou prend le vent de la porte.",
        }[a]
        return [
            "copine|Le vent, d'abord.",
            "papa|J'ouvre un peu, à votre hauteur.",
            "narrateur|Aniss attend, Mila tient le jaune.",
            f"narrateur|{draft}",
            "narrateur|Une pale part, sans un mot.",
            "copine|Ça tient !",
            "narrateur|La goutte de cire rouge file dans le courant, ronde.",
            f"narrateur|{obj}",
            "papa|La porte a donné le courant.",
            "maman|Aniss a poussé, sans crier.",
            "enfant-m|Il tourne.",
        ]
    if b == 3 and c == 2:
        step = {
            1: "Le moulin pose ses pales sur la marche.",
            2: "Le fil pose le papier sur la marche.",
            3: "Le caillou cale le papier sur la marche.",
        }[a]
        return [
            "enfant-m|Mila.",
            "narrateur|Aniss pointe la marche, du doigt.",
            "narrateur|Mila attend, puis ouvre les mains.",
            f"narrateur|{step}",
            "narrateur|Le courant du seuil pousse, tout net.",
            "copine|Je le tiens.",
            "narrateur|La goutte de cire rouge prend l'air, sur la marche.",
            f"narrateur|{obj}",
            "maman|Le porche garde son ombre, plus loin.",
            "papa|Tes mains ont guidé le moulin.",
            "enfant-m|Il tourne.",
        ]
    knot = {
        1: "Le moulin suit le nœud, tour après tour.",
        2: "Le fil serre le nœud, tout droit.",
        3: "Le caillou tient derrière le nœud, tout droit.",
    }[a]
    return [
        "copine|Le nœud, Aniss.",
        "narrateur|Aniss pointe le crochet du porche, du doigt.",
        "narrateur|Mila attend, puis suit le doigt.",
        f"narrateur|{knot}",
        "narrateur|Le jaune se tient, hors du mur.",
        "copine|Il évite le mur.",
        "narrateur|La goutte de cire rouge veille derrière le nœud.",
        f"narrateur|{obj}",
        "papa|Le nœud a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
        "enfant-m|Il tourne.",
    ]


LAST = {
    (1, 1, 1): "La goutte de cire rouge s'endort entre deux barreaux.",
    (1, 1, 2): "Dans les paumes, la goutte de cire rouge clignote.",
    (1, 1, 3): "Au crochet, la goutte de cire rouge tourne, petite.",
    (1, 2, 1): "Sur la dalle, la goutte de cire rouge sèche, ronde.",
    (1, 2, 2): "Au bout du fil, la goutte de cire rouge tremble.",
    (1, 2, 3): "Au bord sec, la goutte de cire rouge se tait.",
    (1, 3, 1): "Dans le courant de la porte, la goutte de cire rouge file.",
    (1, 3, 2): "Sur la marche, la goutte de cire rouge prend l'air.",
    (1, 3, 3): "Derrière le nœud, la goutte de cire rouge veille.",
    (2, 1, 1): "Le fil laisse la goutte de cire rouge au fer.",
    (2, 1, 2): "Les mains de Mila chauffent la goutte de cire rouge.",
    (2, 1, 3): "Le loquet garde la goutte de cire rouge, minuscule.",
    (2, 2, 1): "L'eau n'a pas pris la goutte de cire rouge.",
    (2, 2, 2): "Le fil tendu montre la goutte de cire rouge au soleil.",
    (2, 2, 3): "Le bord a sauvé la goutte de cire rouge, tiède.",
    (2, 3, 1): "Le vent de la porte lèche la goutte de cire rouge.",
    (2, 3, 2): "La marche tient la goutte de cire rouge, droite.",
    (2, 3, 3): "Le nœud serre près de la goutte de cire rouge.",
    (3, 1, 1): "Le caillou cale la goutte de cire rouge au bas.",
    (3, 1, 2): "La pierre suit la goutte de cire rouge vers Mila.",
    (3, 1, 3): "Le crochet pince la goutte de cire rouge, sans la casser.",
    (3, 2, 1): "La dalle a séché la goutte de cire rouge.",
    (3, 2, 2): "Le caillou guide la goutte de cire rouge au-dessus de l'eau.",
    (3, 2, 3): "Le bord laisse la goutte de cire rouge au sec.",
    (3, 3, 1): "Le vent pousse la goutte de cire rouge, hors du mur.",
    (3, 3, 2): "Deux pieds s'arrêtent, la goutte de cire rouge au milieu.",
    (3, 3, 3): "Le papier tremble, la goutte de cire rouge se tait.",
}

HARD = {
    1: "Les barreaux ont failli garder le papier.",
    2: "L'eau a failli emporter la pale.",
    3: "Le porche a failli manger le vent.",
}

CODA = {
    1: "Le moulin garde une pale un peu froissée.",
    2: "Le fil pend, un peu humide, contre le fer.",
    3: "Le caillou reste tiède, contre le barreau.",
}

TRACE = {
    1: "Un rai rouge s'allonge sur le bitume, puis s'arrête.",
    2: "Au muret, ça sent la cire, tiède.",
    3: "Au loin, le bus se tait.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    last = LAST[(a, b, c)]
    hard = HARD[b]
    coda = CODA[a]
    trace = TRACE[c]
    if b == 1 and c == 1:
        return [
            "narrateur|Le moulin pose une pale sur le fer.",
            "enfant-m|Tourne.",
            "copine|Il est arrivé.",
            f"narrateur|{hard}",
            "papa|Le bas a laissé le passage.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 2:
        return [
            "narrateur|Le jaune s'est glissé jusqu'au barreau.",
            "copine|Aniss l'a tendu, tout seul.",
            "papa|Tu as tendu, d'abord.",
            f"narrateur|{hard}",
            "maman|Venez, le moulin est près de la grille.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 3:
        return [
            "narrateur|Le jaune pend au crochet, tout droit.",
            "copine|On a posé le moulin.",
            "papa|Le crochet a tenu, tout droit.",
            f"narrateur|{hard}",
            "maman|Essuyez vos mains, tout près.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 1:
        return [
            "narrateur|Le jaune rejoint la grille, un peu mouillé.",
            "copine|On a attendu l'eau.",
            "papa|Le caniveau n'a plus pris vos bras.",
            f"narrateur|{hard}",
            "maman|Rentrez le fil, après la grille.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 2:
        return [
            "narrateur|Le fil pose le moulin contre le fer.",
            "copine|On tenait, tous les deux.",
            "papa|Je remporte le fil, tout à l'heure.",
            f"narrateur|{hard}",
            "maman|La grille vous attend.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 3:
        return [
            "narrateur|Les mains d'Aniss laissent le jaune contre le fer.",
            "copine|C'était plus facile, là.",
            "papa|Tes bras ont guidé le moulin.",
            f"narrateur|{hard}",
            "maman|Le barreau gardera son ombre.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 1:
        return [
            "narrateur|Le jaune rejoint la grille, tout sec.",
            "copine|On a trouvé, Aniss.",
            "papa|Le vent n'a pas glissé.",
            f"narrateur|{hard}",
            "maman|Entrez, le seuil est sec.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 2:
        return [
            "narrateur|Les mains de Mila laissent le jaune au fer.",
            "copine|On l'a tenu, tous les deux.",
            "papa|Le porche est resté à sa place.",
            f"narrateur|{hard}",
            "maman|Essuie tes chaussures, Aniss.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    return [
        "narrateur|Le jaune suit le nœud, jusqu'à la grille.",
        "copine|L'ombre était douce.",
        "papa|Le nœud a tenu, tout droit.",
        f"narrateur|{hard}",
        "maman|Le porche n'a plus rien à dire.",
        f"narrateur|{coda}",
        f"narrateur|{trace}",
        f"narrateur|{last}",
    ]


END_SONS = {1: "vent,fer", 2: "fil,eau", 3: "pierre,porche"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "bus,papier,vent",
        {"emphasis": "goutte de cire rouge"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le moulin", "le fil", "le caillou"), "pause_before": 200},
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
            {"emphasis": "goutte de cire rouge"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("la grille", "le caniveau", "le porche"), "pause_before": 200},
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
                    {"emphasis": "goutte de cire rouge"},
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
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "goutte de cire rouge" not in blob:
        raise SystemExit(f"{SID}: indice goutte de cire rouge absent")
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
        if "cire" not in low:
            raise SystemExit(f"fin sans cire: {last_n[-1]}")
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

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-061 — Le moulin de papier d'Aniss et la grille de l'école\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — camarade qui parle peu / tendre, attendre "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Aniss, Mila, papa, maman\n"
        "- **Lieu :** chemin de l'école : grille, caniveau, porche\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un bus passe ; le papier répond depuis le sac. Aniss sort le moulin : "
        "une goutte de cire rouge tient une pale. Il veut le planter à la grille "
        "avant que le vent ne se couche sous le porche. Mila veut qu'il crie "
        "tourne. Aniss lève trop vite : le bâton bute. Sourire parti. "
        "Moulin, fil, caillou : les trois partent. Grille (barreaux trop serrés), "
        "caniveau (eau trop vite), porche (air trop sage). Bas, mains de Mila, "
        "crochet ; dalle, fil, bord ; vent, marche, nœud. "
        "La goutte de cire rouge prend le vent, avec une trace.\n\n"
        "## Vécu\n\n"
        "Aniss veut le moulin **à la grille, maintenant**. Mila ne veut pas "
        "la même chose : elle veut des mots. Première idée : lever trop vite. "
        "Ça rate. Chaque choix change l'obstacle et le climax (fer, eau, ombre). "
        "La leçon se voit : Aniss tend, Mila attend, le silence compte. "
        "On ne force pas la parole, on change le geste. "
        "Fin : goutte de cire rouge + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Zoé / Tom / Léa / Sami / Lila / cuisine-jardin-chambre / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Aniss (`enfant-m`), Mila (`copine`), rythmes distincts, silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique : goutte de cire rouge (ouverture + climax). "
        "Pas d'ancre / étoile / fil pâle / marque fine / pastille de colle.\n"
        "- Ouverture inventée : le bus, le papier qui répond dans le sac.\n"
        "- Corps : sourire parti ; envie et inquiétude ; papa s'accroupit.\n"
        "- Merci vécu (ouverture). Question d'adulte. Un « en ce moment ».\n"
        "- Monde ≠ TREE-DIF-034 (pas de soleil en papier, vestiaire, pastille).\n"
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
