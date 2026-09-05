#!/usr/bin/env python3
"""TREE-DIF-020 — L'escargot de Mila et la feuille du balcon (F-NAR-019, N3, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-020"
N3 = 16
TITLE = "L'escargot de Mila et la feuille du balcon"
FIL = (
    "Après la pluie, le balcon répond : bois, gouttière, linge, bassine. "
    "Mila veut aider l'escargot jusqu'à la feuille, sans le forcer, "
    "avant que le bois sèche. Une lune d'étain brille sur la coquille. "
    "T1 = boîte / compte-gouttes / feuille, les trois partent. "
    "Nina reste au seuil, silence = réponse. "
    "T2 = gouttière trop vite, linge trop agité, carreaux trop chauds. "
    "T3 = neuf façons de laisser du temps. La lune d'étain se tourne. L'escargot arrive."
)
CHARS = "Mila, Nina, papa, maman"
SETTING = "balcon de bois après la pluie, gouttière, linge, carreaux"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "lune d'étain",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_balcon_répond_et_Nina_reste; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=Nina_ne_bouge_pas; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "Nina",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=Mila_propose_Nina_reste; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_et_découragement; intensite=2; destinataire=enfant; sous_texte=forcer_fait_rentrer_l_escargot; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "lune d'étain",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=attendre_regarder_sans_forcer; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "lune d'étain",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_lune_d_etain_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|La pluie est partie, mais le balcon lui répond.",
    "narrateur|Le bois boit, sombre, tiède sous les pieds nus.",
    "narrateur|La gouttière chante un filet mince.",
    "narrateur|Le linge goutte dans une bassine, toc.",
    "narrateur|Puis la bassine se tait.",
    "papa|Tu entends le toc, Mila ?",
    "enfant-f|La bassine a parlé, papa.",
    "narrateur|Ça sent le pin mouillé, près des fentes.",
    "narrateur|Un escargot avance, coquille noisette.",
    "narrateur|Sur la coquille, une lune d'étain brille.",
    "narrateur|Pâle, du côté où le bois reste humide.",
    "maman|Nina arrive, ses sandales font un bruit mou.",
    "narrateur|Les carreaux du jardin luisent, trop clairs.",
    "copine|Je te vois, Mila.",
    "enfant-f|Viens, on l'aide, vite.",
    "narrateur|Nina s'arrête au seuil, les mains au cadre.",
    "narrateur|Elle ne dit rien.",
    "narrateur|En ce moment, Mila veut le poser sur la feuille.",
    "enfant-f|Avant que le bois sèche.",
    "papa|Le soleil chauffe les planches, Mila.",
    "maman|Merci, tu le tiens sans le serrer.",
    "papa|On prend les affaires, alors ?",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près des sandales.",
    "narrateur|La boîte, le compte-gouttes, et la feuille.",
    "narrateur|Les trois partiront ensemble.",
    "maman|Tu prends quoi d'abord, Mila ?",
]

T1 = {
    1: {
        "lab": "la boîte",
        "sons": "carton,toc",
        "emphasis": "boîte",
        "passage": [
            "narrateur|Mila glisse l'escargot dans la boîte.",
            "enfant-f|Tu voyages ici.",
            "narrateur|Le couvercle tombe, un petit toc.",
            "narrateur|L'escargot rentre, d'un coup.",
            "enfant-f|Non, sors !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Le compte-gouttes, aussi, pour le chemin.",
            "narrateur|Elle pose la feuille mouillée près de la boîte.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Nina, viens le voir marcher !",
            "narrateur|Des pas légers s'arrêtent près de la porte.",
            "copine|Mila, je suis là.",
            "narrateur|Nina reste sur le seuil, les mains au cadre.",
            "narrateur|Elle ne dit rien.",
        ],
        "question": [
            "narrateur|Nina reste au seuil, les yeux sur la boîte.",
            "maman|Que peut-on faire ?",
        ],
        "qfields": {
            "expected_answer": "répéter",
            "accepted_examples": "répéter | répète | observer | observer d'abord | attendre | attendre un peu",
            "retry_prompt": "On peut répéter. Que fait-on ?",
        },
        "confirm": [
            "enfant-f|On répète, Nina.",
            "enfant-f|On regarde d'abord.",
            "copine|Je reste ici, un peu.",
            "papa|Elle a le temps.",
            "narrateur|Nina écoute, les mains sur le bois.",
            "narrateur|Elle ne dit rien, puis hoche.",
            "maman|Vous partez quand elle est prête.",
            "enfant-f|Oui, maman.",
            "narrateur|La boîte reste tiède, contre sa paume.",
        ],
    },
    2: {
        "lab": "le compte-gouttes",
        "sons": "goutte,verre",
        "emphasis": "compte-gouttes",
        "passage": [
            "narrateur|Mila prend le compte-gouttes, plein d'eau.",
            "enfant-f|Je fais un chemin mouillé.",
            "papa|Une goutte, puis une autre.",
            "narrateur|L'eau trace une ligne trop large.",
            "narrateur|L'escargot recule, la lune d'étain se cache.",
            "enfant-f|Ce n'est pas le bon chemin !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Je m'accroupis, à ta hauteur.",
            "papa|La boîte, ensuite, près de toi.",
            "narrateur|Elle glisse la feuille par-dessus.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Nina va tout voir.",
            "narrateur|La porte du balcon s'ouvre, légère.",
            "copine|Me voilà, Mila.",
            "narrateur|Nina s'arrête au seuil, sans avancer.",
        ],
        "question": [
            "narrateur|Nina reste au seuil, les yeux sur les gouttes.",
            "papa|Que peut-on faire ?",
        ],
        "qfields": {
            "expected_answer": "répéter",
            "accepted_examples": "répéter | répète | observer | observer d'abord | attendre | attendre un peu",
            "retry_prompt": "On peut répéter. Que fait-on ?",
        },
        "confirm": [
            "enfant-f|On répète le chemin, goutte après goutte.",
            "enfant-f|On observe d'abord.",
            "copine|Je te vois, d'ici.",
            "maman|Elle a le temps.",
            "narrateur|Une goutte tremble au bout du verre.",
            "narrateur|Nina hoche, sans un mot.",
            "papa|Vous partez quand elle est prête.",
            "enfant-f|Oui, papa.",
            "narrateur|Le bois garde la ligne d'eau, mince.",
        ],
    },
    3: {
        "lab": "la feuille",
        "sons": "feuille,pas",
        "emphasis": "feuille",
        "passage": [
            "narrateur|Mila prend la feuille, froide de pluie.",
            "enfant-f|C'est ta maison, au bout du bois.",
            "maman|Tiens-la comme un toit, pas trop bas.",
            "narrateur|La feuille sent l'herbe et l'eau.",
            "narrateur|Elle la pose trop tôt, trop près.",
            "narrateur|L'escargot rentre, la lune d'étain s'éteint.",
            "enfant-f|Il n'en veut pas !",
            "narrateur|Le sourire de Mila disparaît.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|La boîte et le compte-gouttes, avec vous.",
            "narrateur|Il les pose près des sandales.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Nina, vite !",
            "narrateur|Des pas frais sonnent sur le carreau.",
            "copine|J'arrive, Mila.",
            "narrateur|Nina reste près du cadre, sans un mot.",
        ],
        "question": [
            "narrateur|Nina reste au seuil, les yeux sur la feuille.",
            "maman|Que peut-on faire ?",
        ],
        "qfields": {
            "expected_answer": "répéter",
            "accepted_examples": "répéter | répète | observer | observer d'abord | attendre | attendre un peu",
            "retry_prompt": "On peut répéter. Que fait-on ?",
        },
        "confirm": [
            "enfant-f|On répète, à voix basse.",
            "enfant-f|La feuille attend, on regarde.",
            "copine|Je viens après.",
            "papa|Elle a le temps.",
            "narrateur|Nina suit des yeux la nervure verte.",
            "narrateur|Elle ne dit rien, puis hoche.",
            "maman|Vous partez quand elle est prête.",
            "enfant-f|Oui.",
            "narrateur|La feuille perle, une goutte au bord.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|La boîte tape un peu le bois, à chaque pas.",
        "narrateur|Le balcon fume, mouillé, au rebord des bassines.",
        "papa|La gouttière, le linge, ou les carreaux ?",
    ],
    2: [
        "narrateur|Une goutte tombe devant elles, puis une autre.",
        "narrateur|Le balcon fume, mouillé, au rebord des bassines.",
        "papa|La gouttière, le linge, ou les carreaux ?",
    ],
    3: [
        "narrateur|La feuille tremble entre les doigts de Mila.",
        "narrateur|Le balcon fume, mouillé, au rebord des bassines.",
        "papa|La gouttière, le linge, ou les carreaux ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "gouttiere,eau",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Un coin de la boîte frotte le bois.",
            "narrateur|Elles gagnent le rebord des bassines.",
            "narrateur|La gouttière chante trop fort, trop vite.",
            "narrateur|Mila pose la boîte au bord, couvercle ouvert.",
            "enfant-f|L'eau va l'aider !",
            "narrateur|Le filet emporte une paille, d'un trait.",
            "narrateur|L'escargot rentre, la lune d'étain se cache.",
            "copine|Il a peur.",
            "narrateur|Nina recule d'un pas, sans un mot.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Le filet est trop fort, ici.",
            "enfant-f|On fait comment, alors ?",
            "narrateur|Mila refuse de foncer.",
            "papa|Vous trouvez, toutes les deux ?",
        ],
    },
    (1, 2): {
        "sons": "drap,vent",
        "emphasis": "linge",
        "passage": [
            "narrateur|Un coin de la boîte frotte le bois.",
            "narrateur|Elles gagnent le passage des draps.",
            "narrateur|Un drap mouillé claque, trop fort.",
            "narrateur|La boîte penche quand le drap claque.",
            "enfant-f|Ça bouge trop.",
            "narrateur|Nina recule d'un pas, les mains aux oreilles.",
            "copine|C'est trop fort.",
            "narrateur|L'escargot rentre, la lune d'étain se cache.",
            "maman|Le vent n'a pas fini.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|L'escargot n'avance plus.",
            "enfant-f|On fait comment, Nina ?",
            "narrateur|Mila refuse de foncer.",
            "maman|Vous trouvez, toutes les deux ?",
        ],
    },
    (1, 3): {
        "sons": "pas,bois",
        "emphasis": "carreaux",
        "passage": [
            "narrateur|Un coin de la boîte frotte le bois.",
            "narrateur|Elles gagnent les carreaux du jardin.",
            "narrateur|Les carreaux brillent, trop chauds, trop secs.",
            "narrateur|Le carton de la boîte chauffe, un peu.",
            "enfant-f|La trace s'arrête.",
            "narrateur|L'escargot reste collé, sans bouger.",
            "copine|Il n'aime pas le chaud.",
            "narrateur|La lune d'étain pâlit, presque éteinte.",
            "papa|Le soleil a trop séché.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le bois fume moins, ici.",
            "enfant-f|On fait comment, alors ?",
            "narrateur|Mila refuse de foncer.",
            "papa|Vous trouvez, toutes les deux ?",
        ],
    },
    (2, 1): {
        "sons": "gouttiere,goutte",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|Une goutte tombe du compte-gouttes, sur le seuil.",
            "narrateur|Elles gagnent le rebord des bassines.",
            "narrateur|La gouttière chante trop fort, trop vite.",
            "narrateur|Une goutte du verre se perd dans le courant.",
            "enfant-f|L'eau emporte tout.",
            "narrateur|L'escargot rentre, la lune d'étain se cache.",
            "copine|Il a peur.",
            "narrateur|Nina recule d'un pas, sans un mot.",
            "papa|Le filet est trop fort, ici.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le verre tremble entre tes doigts.",
            "enfant-f|On fait comment, alors ?",
            "narrateur|Mila refuse de foncer.",
            "papa|Vous trouvez, toutes les deux ?",
        ],
    },
    (2, 2): {
        "sons": "drap,goutte",
        "emphasis": "linge",
        "passage": [
            "narrateur|Une goutte tombe du compte-gouttes, sur le seuil.",
            "narrateur|Elles gagnent le passage des draps.",
            "narrateur|Un drap mouillé claque, trop fort.",
            "narrateur|Les gouttes du linge brouillent le chemin d'eau.",
            "enfant-f|Je ne vois plus la ligne.",
            "narrateur|Nina recule d'un pas, les mains aux oreilles.",
            "copine|C'est trop fort.",
            "narrateur|L'escargot rentre, la lune d'étain se cache.",
            "maman|Le vent n'a pas fini.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|L'escargot n'avance plus.",
            "enfant-f|On fait comment, Nina ?",
            "narrateur|Mila refuse de foncer.",
            "maman|Vous trouvez, toutes les deux ?",
        ],
    },
    (2, 3): {
        "sons": "goutte,bois",
        "emphasis": "carreaux",
        "passage": [
            "narrateur|Une goutte tombe du compte-gouttes, sur le seuil.",
            "narrateur|Elles gagnent les carreaux du jardin.",
            "narrateur|Les carreaux brillent, trop chauds, trop secs.",
            "narrateur|Les gouttes sèchent avant d'arriver au bout.",
            "enfant-f|La trace s'arrête.",
            "narrateur|L'escargot reste collé, sans bouger.",
            "copine|Il n'aime pas le chaud.",
            "narrateur|La lune d'étain pâlit, presque éteinte.",
            "papa|Le soleil a trop séché.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le verre chauffe, contre ta paume.",
            "enfant-f|On fait comment, alors ?",
            "narrateur|Mila refuse de foncer.",
            "papa|Vous trouvez, toutes les deux ?",
        ],
    },
    (3, 1): {
        "sons": "gouttiere,feuille",
        "emphasis": "gouttière",
        "passage": [
            "narrateur|La feuille mouillée colle un peu à sa paume.",
            "narrateur|Elles gagnent le rebord des bassines.",
            "narrateur|La gouttière chante trop fort, trop vite.",
            "narrateur|La feuille frôle l'eau, trop vite emportée.",
            "enfant-f|Elle va partir !",
            "narrateur|L'escargot rentre, la lune d'étain se cache.",
            "copine|Il a peur.",
            "narrateur|Nina recule d'un pas, sans un mot.",
            "papa|Le filet est trop fort, ici.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|La nervure tremble, trop loin du bord.",
            "enfant-f|On fait comment, alors ?",
            "narrateur|Mila refuse de foncer.",
            "papa|Vous trouvez, toutes les deux ?",
        ],
    },
    (3, 2): {
        "sons": "drap,feuille",
        "emphasis": "linge",
        "passage": [
            "narrateur|La feuille mouillée colle un peu à sa paume.",
            "narrateur|Elles gagnent le passage des draps.",
            "narrateur|Un drap mouillé claque, trop fort.",
            "narrateur|La feuille s'envole un peu, puis retombe.",
            "enfant-f|Ça bouge trop.",
            "narrateur|Nina recule d'un pas, les mains aux oreilles.",
            "copine|C'est trop fort.",
            "narrateur|L'escargot rentre, la lune d'étain se cache.",
            "maman|Le vent n'a pas fini.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|L'escargot n'avance plus.",
            "enfant-f|On fait comment, Nina ?",
            "narrateur|Mila refuse de foncer.",
            "maman|Vous trouvez, toutes les deux ?",
        ],
    },
    (3, 3): {
        "sons": "feuille,bois",
        "emphasis": "carreaux",
        "passage": [
            "narrateur|La feuille mouillée colle un peu à sa paume.",
            "narrateur|Elles gagnent les carreaux du jardin.",
            "narrateur|Les carreaux brillent, trop chauds, trop secs.",
            "narrateur|La feuille se recroqueville, trop vite.",
            "enfant-f|La trace s'arrête.",
            "narrateur|L'escargot reste collé, sans bouger.",
            "copine|Il n'aime pas le chaud.",
            "narrateur|La lune d'étain pâlit, presque éteinte.",
            "papa|Le soleil a trop séché.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|La nervure se plie, trop sèche.",
            "enfant-f|On fait comment, alors ?",
            "narrateur|Mila refuse de foncer.",
            "papa|Vous trouvez, toutes les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("attendre un peu", "regarder d'abord", "le petit filet"),
    2: ("attendre le vent", "tenir le drap", "derrière"),
    3: ("l'ombre", "goutte à goutte", "sous le pot"),
}

T3_CHOICE = {
    1: [
        "narrateur|L'eau de la gouttière chante trop vite.",
        "papa|Attendre, regarder, ou le petit filet ?",
    ],
    2: [
        "narrateur|Le drap claque trop fort.",
        "maman|Attendre le vent, tenir, ou derrière ?",
    ],
    3: [
        "narrateur|Les carreaux restent trop chauds, trop secs.",
        "papa|L'ombre, goutte à goutte, ou sous le pot ?",
    ],
}

T3_SONS = {
    (1, 1): "goutte,silence",
    (1, 2): "silence,eau",
    (1, 3): "filet,goutte",
    (2, 1): "vent,drap",
    (2, 2): "drap,mains",
    (2, 3): "linge,pas",
    (3, 1): "ombre,pot",
    (3, 2): "goutte,bois",
    (3, 3): "terre,pot",
}

OBJ = {
    1: "La boîte attend, le couvercle ouvert.",
    2: "Une goutte tremble au bout du verre.",
    3: "La feuille perle, une nervure brillante.",
}

LUNE = {
    1: "La lune d'étain se tourne vers la feuille.",
    2: "La lune d'étain du début reparaît, pâle.",
    3: "La lune d'étain capte l'ombre, puis la feuille.",
}

T3_SIG = {
    (1, 1, 1): "Le carton reste frais, au bord du filet.",
    (1, 1, 2): "Le carton reflète le filet, un instant.",
    (1, 1, 3): "Le carton sert d'abri, hors du courant.",
    (1, 2, 1): "Le carton s'assoit, loin du drap.",
    (1, 2, 2): "Le carton ne penche plus, sous le drap tenu.",
    (1, 2, 3): "Le carton s'abrite, derrière le linge.",
    (1, 3, 1): "Le carton se pose à l'ombre, plus frais.",
    (1, 3, 2): "Le carton reçoit goutte à goutte, sans chauffer.",
    (1, 3, 3): "Le carton glisse sous le pot, à l'abri.",
    (2, 1, 1): "Le verre attend, loin du gros filet.",
    (2, 1, 2): "Le verre reflète la lune, un instant.",
    (2, 1, 3): "Le verre trace un filet mince, à part.",
    (2, 2, 1): "Le verre repose, loin du drap.",
    (2, 2, 2): "Le verre ne tremble plus, le drap tenu.",
    (2, 2, 3): "Le verre reste frais, derrière le linge.",
    (2, 3, 1): "Le verre se pose à l'ombre, plus froid.",
    (2, 3, 2): "Le verre pose goutte à goutte, sur le bois.",
    (2, 3, 3): "Le verre s'abrite sous le pot, à l'ombre.",
    (3, 1, 1): "La nervure attend, hors du courant.",
    (3, 1, 2): "La nervure pointe vers le bord calme.",
    (3, 1, 3): "La nervure sert de pont, sur le petit filet.",
    (3, 2, 1): "La nervure se pose, loin du drap.",
    (3, 2, 2): "La nervure ne tremble plus, le drap tenu.",
    (3, 2, 3): "La nervure s'abrite, derrière le linge.",
    (3, 3, 1): "La nervure se déplie à l'ombre, verte.",
    (3, 3, 2): "La nervure boit goutte à goutte, sans sécher.",
    (3, 3, 3): "La nervure rejoint la terre, sous le pot.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    obj = OBJ[a]
    lune = LUNE[b]
    sig = T3_SIG[(a, b, c)]
    if b == 1 and c == 1:
        return [
            "enfant-f|On attend un peu.",
            "copine|Moi aussi, j'attends.",
            "narrateur|Les gouttes se calment, une, puis une autre.",
            "narrateur|L'escargot sort deux cornes, très lent.",
            f"narrateur|{obj}",
            "papa|Le filet a baissé.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Tu peux marcher.",
            "copine|Il avance, Mila.",
        ]
    if b == 1 and c == 2:
        return [
            "enfant-f|On regarde d'abord.",
            "narrateur|Personne ne parle.",
            "narrateur|Nina suit l'escargot des yeux, sans un mot.",
            "narrateur|Il choisit le bord, hors du courant.",
            f"narrateur|{obj}",
            "maman|Vous l'avez regardé, sans le pousser.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Il savait, lui.",
            "copine|Moi aussi, je vois.",
        ]
    if b == 1 and c == 3:
        return [
            "enfant-f|Le petit filet, plus loin.",
            "copine|Là, ça chante moins.",
            "narrateur|Elles suivent un filet mince, à l'écart.",
            "narrateur|L'escargot sort deux cornes, vers l'eau calme.",
            f"narrateur|{obj}",
            "papa|Celui-là, il ne l'emporte pas.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Tu peux marcher.",
            "copine|Il avance, Mila.",
        ]
    if b == 2 and c == 1:
        return [
            "enfant-f|On attend le vent.",
            "narrateur|Nina ne dit rien.",
            "narrateur|Le drap se tait, un moment.",
            "narrateur|L'escargot sort deux cornes, très lent.",
            f"narrateur|{obj}",
            "maman|Le vent a lâché le linge.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Tu peux marcher.",
            "copine|Il avance, Mila.",
        ]
    if b == 2 and c == 2:
        return [
            "enfant-f|On tient le drap, Nina.",
            "copine|Moi le coin, toi l'autre.",
            "narrateur|Le drap s'arrête, tenu par quatre mains.",
            "narrateur|L'escargot sort deux cornes, vers le calme.",
            f"narrateur|{obj}",
            "papa|Vous l'avez tenu, sans crier.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Tu peux marcher.",
            "copine|Il avance, Mila.",
        ]
    if b == 2 and c == 3:
        return [
            "enfant-f|Derrière, Nina.",
            "narrateur|Nina hoche, puis les suit.",
            "narrateur|Derrière le linge, l'air est plus frais.",
            "narrateur|L'escargot sort deux cornes, à l'abri.",
            f"narrateur|{obj}",
            "maman|Ici, ça ne claque plus.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Tu peux marcher.",
            "copine|Il avance, Mila.",
        ]
    if b == 3 and c == 1:
        return [
            "enfant-f|L'ombre, près du pot.",
            "copine|Là, c'est moins chaud.",
            "narrateur|Elles gagnent l'ombre du pot, plus fraîche.",
            "narrateur|L'escargot sort deux cornes, vers le frais.",
            f"narrateur|{obj}",
            "papa|L'ombre a gardé un peu d'eau.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Tu peux marcher.",
            "copine|Il avance, Mila.",
        ]
    if b == 3 and c == 2:
        return [
            "enfant-f|Goutte à goutte, Nina, avec moi.",
            "copine|Goutte, puis goutte.",
            "narrateur|Elles mouillent le bois, sans le noyer.",
            "narrateur|L'escargot sort deux cornes, vers la ligne.",
            f"narrateur|{obj}",
            "maman|Vous avez versé sans le presser.",
            f"narrateur|{sig}",
            f"narrateur|{lune}",
            "enfant-f|Tu peux marcher.",
            "copine|Il avance, Mila.",
        ]
    return [
        "enfant-f|Sous le pot, Nina.",
        "narrateur|Nina s'accroupit, sans un mot.",
        "narrateur|Sous le pot, la terre reste froide.",
        "narrateur|L'escargot sort deux cornes, vers le sombre.",
        f"narrateur|{obj}",
        "papa|Là, le soleil n'arrive pas.",
        f"narrateur|{sig}",
        f"narrateur|{lune}",
        "enfant-f|Tu peux marcher.",
        "copine|Il avance, Mila.",
    ]


END_CODA = {
    1: "La boîte sèche près de la fenêtre, le couvercle entrouvert.",
    2: "Une goutte reste au bout du compte-gouttes, près de l'évier.",
    3: "La feuille sèche sur le rebord, un peu recroquevillée.",
}

END_LEAD = {
    (1, 1): [
        "narrateur|L'escargot atteint la feuille, deux cornes dressées.",
        "copine|On a attendu, et il est venu.",
        "enfant-f|Il est arrivé.",
        "papa|La lune d'étain regarde la feuille.",
        "maman|La soupe est prête, dedans.",
    ],
    (1, 2): [
        "narrateur|L'escargot gagne la feuille, sans qu'on le pousse.",
        "copine|On l'a regardé, et il a choisi.",
        "enfant-f|Il savait le bord.",
        "papa|La lune d'étain s'est tournée, pile.",
        "maman|La soupe est prête, dedans.",
    ],
    (1, 3): [
        "narrateur|L'escargot suit le petit filet, jusqu'à la feuille.",
        "copine|Celui-là ne l'emportait pas.",
        "enfant-f|Il est arrivé.",
        "papa|La lune d'étain brille, du bon côté.",
        "maman|La soupe est prête, dedans.",
    ],
    (2, 1): [
        "narrateur|L'escargot atteint la feuille, le drap arrêté.",
        "copine|Le vent a lâché, et il est venu.",
        "enfant-f|Il est arrivé.",
        "maman|La lune d'étain a repris sa pâleur.",
        "papa|La soupe est prête, dedans.",
    ],
    (2, 2): [
        "narrateur|L'escargot gagne la feuille, le drap tenu.",
        "copine|On l'a tenu, et il a marché.",
        "enfant-f|Il est arrivé.",
        "maman|La lune d'étain se voit, à présent.",
        "papa|La soupe est prête, dedans.",
    ],
    (2, 3): [
        "narrateur|L'escargot atteint la feuille, derrière le linge.",
        "copine|Là, ça ne claquait plus.",
        "enfant-f|Il est arrivé.",
        "maman|La lune d'étain a trouvé l'abri.",
        "papa|La soupe est prête, dedans.",
    ],
    (3, 1): [
        "narrateur|L'escargot atteint la feuille, à l'ombre du pot.",
        "copine|L'ombre était plus fraîche.",
        "enfant-f|Il est arrivé.",
        "papa|La lune d'étain capte l'ombre, puis s'arrête.",
        "maman|La soupe est prête, dedans.",
    ],
    (3, 2): [
        "narrateur|L'escargot suit les gouttes, jusqu'à la feuille.",
        "copine|Goutte après goutte, il a marché.",
        "enfant-f|Il est arrivé.",
        "papa|La lune d'étain brille sur la ligne d'eau.",
        "maman|La soupe est prête, dedans.",
    ],
    (3, 3): [
        "narrateur|L'escargot atteint la feuille, sous le pot.",
        "copine|La terre était froide, comme il voulait.",
        "enfant-f|Il est arrivé.",
        "papa|La lune d'étain s'allume, dans le sombre.",
        "maman|La soupe est prête, dedans.",
    ],
}

LAST = {
    (1, 1, 1): "La bassine fait un dernier toc, puis se tait.",
    (1, 1, 2): "Un filet mince reste au bord du carton.",
    (1, 1, 3): "Le couvercle garde une goutte, froide.",
    (1, 2, 1): "Le drap retombe, sans claquer.",
    (1, 2, 2): "Une main d'enfant reste imprimée au tissu.",
    (1, 2, 3): "Derrière le linge, l'ombre sent le pin mouillé.",
    (1, 3, 1): "L'ombre du pot reste fraîche, au carton.",
    (1, 3, 2): "Une ligne d'eau sèche sur le bois, mince.",
    (1, 3, 3): "Sous le pot, la terre garde un rond d'ombre.",
    (2, 1, 1): "Une goutte tremble au bout du verre, puis tombe.",
    (2, 1, 2): "Le verre reflète la lune d'étain, un instant.",
    (2, 1, 3): "Le petit filet chante plus bas, à présent.",
    (2, 2, 1): "Le vent laisse le drap, et s'en va.",
    (2, 2, 2): "Une goutte du linge rejoint celle du verre.",
    (2, 2, 3): "Derrière le drap, le verre reste frais.",
    (2, 3, 1): "À l'ombre, le verre ne chauffe plus.",
    (2, 3, 2): "Goutte après goutte, le bois redevient sombre.",
    (2, 3, 3): "Sous le pot, une goutte du verre s'endort.",
    (3, 1, 1): "La feuille perle au bord, une nervure brillante.",
    (3, 1, 2): "La nervure pointe vers la lune d'étain.",
    (3, 1, 3): "Le filet frôle la feuille, sans l'emporter.",
    (3, 2, 1): "Un coin de feuille a séché, l'autre reste froid.",
    (3, 2, 2): "Le drap tenu, la feuille ne tremble plus.",
    (3, 2, 3): "Derrière le linge, la feuille sent l'herbe.",
    (3, 3, 1): "À l'ombre, la feuille se déplie, verte.",
    (3, 3, 2): "Goutte à goutte, la feuille redevient un toit.",
    (3, 3, 3): "Sous le pot, la feuille garde une terre fraîche.",
}

ALMOST = {
    1: "Le bois a failli sécher, trop tôt.",
    2: "Le verre a failli tout verser, trop vite.",
    3: "La feuille a failli s'envoler, trop loin.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    rows = list(END_LEAD[(b, c)])
    rows.append(f"narrateur|{ALMOST[a]}")
    rows.append(f"narrateur|{END_CODA[a]}")
    rows.append("narrateur|Sur la coquille, la lune d'étain reste, pâle.")
    rows.append(f"narrateur|{LAST[(a, b, c)]}")
    return rows


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "goutte,bassine",
        {"emphasis": "lune d'étain"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("la boîte", "le compte-gouttes", "la feuille"), "pause_before": 200},
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
            {"emphasis": "Nina"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("la gouttière", "le linge", "les carreaux"), "pause_before": 200},
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
                    {"emphasis": "lune d'étain"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", "goutte,soupe",
                    {"emphasis": "lune d'étain"},
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
        "celui où j'ai compris",
        "il faut attendre",
        "beaucoup d'énergie",
        "hyperactif",
        "camarade qui bouge",
        "ce n'est pas une faute",
        "mission accomplie",
        "j'ai compris",
        "marque fine",
        "ombre-flèche",
        "ombre en forme",
        "jardinier",
        "bibliothécaire",
        "maîtresse",
        "grand-père",
        "gardienne",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(whole):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: copine absente")
    if "lune d'étain" not in blob:
        raise SystemExit(f"{SID}: indice lune d'étain absent")
    if "boulangerie" in blob or "farine" in blob:
        raise SystemExit(f"{SID}: monde COL-017 collé")

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
    if not all(c.get("text_xai_tags") != c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {SID} {sum(words(c['text']) for c in story['chunks'])} mots")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-020 — L'escargot de Mila et la feuille du balcon\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.BES.001 — plus de temps ou de calme ; "
        "répéter, observer, attendre (vécue, jamais dite)\n"
        "- **Personnages :** Mila, Nina, papa, maman\n"
        "- **Lieu :** balcon de bois après la pluie, gouttière, linge, carreaux "
        "(rebord des bassines, passage des draps)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le balcon répond à la pluie avant que quelqu'un parle. Mila veut aider "
        "l'escargot jusqu'à la feuille, sans le forcer, avant que le bois sèche. "
        "Indice unique : une lune d'étain sur la coquille. Mila propose, vite ; "
        "Nina reste au seuil, silence = réponse. Première idée trop vite : toc, "
        "gouttes trop larges, toit trop tôt. Ça rate. Gouttière, linge ou carreaux : "
        "l'aide trop vite fait rentrer l'animal. On attend, on regarde, ou on change "
        "de coin. La lune d'étain se tourne. L'escargot arrive. Ça a failli ne pas arriver.\n\n"
        "## Vécu\n\n"
        "Mila veut aider **maintenant**. Nina pose sa limite. Silence = réponse. "
        "Première idée : forcer le chemin. Ça rate. Chaque choix change l'obstacle "
        "(filet trop fort, drap trop fort, carreaux trop chauds). La leçon se voit : "
        "pousser fait rentrer ; attendre, regarder ou changer de coin fait sortir. "
        "Fin : lune d'étain du début + objet qui porte une trace + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit 61 % / Lila / slogans chambre jetés. Monde ≠ TREE-COL-017 (pas de boulangerie).\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Mila (`enfant-f`), Nina (`copine`), rythmes distincts, silence = réponse.\n"
        "- Indice unique dès l'ouverture (lune d'étain), payé au climax et à la fin.\n"
        "- T1 ne retire pas l'équipement (boîte, compte-gouttes, feuille partent). "
        "T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Merci vécu (tenir sans serrer). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
