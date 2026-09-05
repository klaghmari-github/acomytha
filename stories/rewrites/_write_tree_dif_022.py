#!/usr/bin/env python3
"""TREE-DIF-022 — La marelle de Nina, pour Aniss aussi (F-NAR-019, N1, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-022"
N1 = 10
TITLE = "La marelle de Nina, pour Aniss aussi"
FIL = (
    "Après la pluie, Nina veut une marelle où Aniss saute aussi, "
    "avant que le grain de craie sèche sur la table. "
    "Elle appelle trop vite : Aniss se tait. Le silence répond. "
    "T1 = craie blanche / caillou plat / linge ; les trois partent. "
    "T2 = allée mouillée / terrasse / bac. "
    "T3 = neuf façons de jouer avec lui, pas toute seule. "
    "Nina refuse de foncer. Le grain de craie paie le début."
)
CHARS = "Nina, Aniss, papa, maman"
SETTING = "jardin mouillé, allée, terrasse, bac à sable"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de craie",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=nina_veut_sa_marelle_aniss_prend_son_temps; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_où_reste_le_caillou; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "Aniss",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=nina_propose_aniss_prend_son_temps; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=appeler_trop_vite_ne_suffit_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_silence_d_aniss_est_une_réponse; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de craie",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=jouer_avec_aniss_pas_toute_seule; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de craie",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_craie_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
        found = TIC_WORDS.search(low)
        if found:
            raise SystemExit(f"tic {found.group(0)!r}: {ph}")
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
    "narrateur|Nina connaît le jardin, après la pluie.",
    "narrateur|L'herbe colle aux chaussures, un peu.",
    "narrateur|Un escargot avance sur une feuille.",
    "narrateur|Papa tend le linge, entre deux arbres.",
    "narrateur|Maman pose deux verres, sur la table.",
    "papa|L'eau est fraîche, Nina.",
    "narrateur|Sur le bois, un grain de craie.",
    "narrateur|Il brille dans une goutte, minuscule.",
    "enfant-f|C'est le départ, papa.",
    "papa|Le grain de craie, sur la table ?",
    "enfant-f|La marelle commence là.",
    "maman|Aniss arrive, derrière la haie.",
    "narrateur|En ce moment, Nina serre la craie.",
    "enfant-f|Aniss, on saute, vite !",
    "narrateur|Aniss ne dit rien.",
    "narrateur|Ce silence tient, comme une réponse.",
    "narrateur|Le sourire de Nina disparaît.",
    "papa|Il s'accroupit, à sa hauteur.",
    "papa|Merci, tu as vu le grain.",
    "maman|Tu lui proposes comment, Nina ?",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près des verres.",
    "narrateur|La craie blanche, le caillou plat, le linge.",
    "maman|Tu prends quoi, d'abord ?",
]

T1 = {
    1: {
        "lab": "la craie blanche",
        "sons": "craie,poussiere",
        "emphasis": "craie blanche",
        "passage": [
            "narrateur|Nina prend la craie blanche.",
            "enfant-f|Elle sent la poussière, un peu.",
            "papa|Elle écrit bien, celle-là.",
            "narrateur|Le caillou reste près du verre.",
            "maman|Le linge reste, plié, au bord.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Aniss, je fais tes carrés !",
            "narrateur|Aniss regarde ses chaussures, longtemps.",
            "narrateur|Il ne dit rien.",
            "narrateur|Nina trace des petits carrés, trop vite.",
            "narrateur|Le trait tremble, trop mince.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "papa|Tu l'invites, sans te presser ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un grain de craie tient au bois.",
        ],
        "question": [
            "narrateur|Nina a glissé le caillou près de la craie.",
            "maman|Il est où, le caillou ?",
        ],
        "qfields": {
            "expected_answer": "craie",
            "accepted_examples": "craie | la craie | près de la craie | à côté de la craie",
            "retry_prompt": "Le caillou est près de la craie. Il est où ?",
        },
        "confirm": [
            "narrateur|La craie blanche veille près du caillou.",
            "copain|Il est plat.",
            "enfant-f|C'est pour sauter, Aniss.",
            "narrateur|Aniss a des chaussures plus longues.",
            "narrateur|Les siennes font un petit bruit.",
            "narrateur|Nina propose, Aniss prend son temps.",
            "maman|Le jardin vous attend.",
            "papa|On reste dehors ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le grain de craie tient, minuscule.",
        ],
    },
    2: {
        "lab": "le caillou plat",
        "sons": "caillou,pierre",
        "emphasis": "caillou plat",
        "passage": [
            "narrateur|Nina prend le caillou plat.",
            "enfant-f|Il est lisse, chaud.",
            "maman|Il a séché au soleil.",
            "narrateur|La craie reste près du verre.",
            "papa|Prends la craie, près de toi.",
            "narrateur|Elle glisse le linge par-dessus.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Aniss va tout voir.",
            "narrateur|Des pas longs sonnent dans l'herbe.",
            "copain|Me voilà, Nina.",
            "enfant-f|On saute, tous les deux ?",
            "narrateur|Aniss serre le caillou, sans sauter.",
            "narrateur|Le sourire de Nina disparaît.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
        "question": [
            "narrateur|Le caillou plat reste dans sa main.",
            "maman|Il est où, le caillou ?",
        ],
        "qfields": {
            "expected_answer": "main",
            "accepted_examples": "main | sa main | dans sa main | dans la main",
            "retry_prompt": "Le caillou est dans sa main. Il est où ?",
        },
        "confirm": [
            "narrateur|Le caillou veille dans sa main.",
            "copain|Je le vois.",
            "enfant-f|Ne le lance pas.",
            "narrateur|Aniss penche pour voir le caillou.",
            "narrateur|Sa mèche touche presque le linge.",
            "papa|Ça sent l'herbe mouillée.",
            "maman|Vos mains, au-dessus du caillou ?",
            "copain|Oui.",
            "narrateur|Le grain de craie tient au bois.",
        ],
    },
    3: {
        "lab": "le linge",
        "sons": "linge,eau",
        "emphasis": "linge",
        "passage": [
            "narrateur|Nina prend le linge, un peu frais.",
            "enfant-f|Il sent l'eau.",
            "papa|Pour sécher le chemin, oui.",
            "narrateur|Elle cache le caillou dessous.",
            "maman|La craie reste avec vous.",
            "narrateur|Papa pose la craie au bord.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Aniss, vite !",
            "narrateur|Une grande ombre arrive au seuil.",
            "copain|J'arrive, Nina.",
            "enfant-f|Je te fais une marelle.",
            "narrateur|Aniss touche le linge, sans parler.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
        "question": [
            "narrateur|Le caillou reste sous le linge.",
            "maman|Il est où, le caillou ?",
        ],
        "qfields": {
            "expected_answer": "linge",
            "accepted_examples": "linge | le linge | sous le linge | dessous",
            "retry_prompt": "Le caillou est sous le linge. Il est où ?",
        },
        "confirm": [
            "narrateur|Le linge cache le caillou.",
            "copain|Ça sent l'eau.",
            "enfant-f|Il est là, dessous.",
            "narrateur|Le linge arrive aux genoux d'Aniss.",
            "narrateur|Pour Nina, il tombe plus bas.",
            "maman|Le jardin est tiède, devant.",
            "papa|On y va, tous les quatre ?",
            "enfant-f|Oui.",
            "narrateur|Le grain de craie tient au bois.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|La craie blanche attend, au bord.",
        "narrateur|Aniss n'est plus près des verres.",
        "narrateur|L'allée, la terrasse, ou le bac.",
        "papa|On commence où, Nina ?",
    ],
    2: [
        "narrateur|Le caillou plat tient dans sa main.",
        "narrateur|Aniss n'est plus près des verres.",
        "maman|L'allée, la terrasse, ou le bac ?",
        "papa|On commence où, Nina ?",
    ],
    3: [
        "narrateur|Le linge reste plié, au bord.",
        "narrateur|Aniss n'est plus près des verres.",
        "narrateur|L'allée, la terrasse, ou le bac.",
        "maman|On commence où, Nina ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "craie,gravier",
        "emphasis": "allée",
        "passage": [
            "narrateur|La craie blanche frotte l'allée mouillée.",
            "enfant-f|Un petit carré, pour moi.",
            "copain|Le mien, trop étroit.",
            "narrateur|La chaussure d'Aniss cache le trait.",
            "narrateur|L'eau efface le trait, plus rusée.",
            "enfant-f|On n'arrive pas, comme ça.",
            "narrateur|Nina lève la craie, trop vite.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
    (2, 1): {
        "sons": "caillou,gravier",
        "emphasis": "allée",
        "passage": [
            "narrateur|Le caillou plat tape un peu le gravier.",
            "enfant-f|On le pose dans le carré.",
            "copain|Moi, je le lance loin.",
            "narrateur|Deux envies, au même moment.",
            "narrateur|Aniss ne dit plus rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|L'eau cache le caillou, plus rusée.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Nina disparaît.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
            "narrateur|Le grain de craie attend, au bois.",
        ],
    },
    (3, 1): {
        "sons": "linge,gravier",
        "emphasis": "allée",
        "passage": [
            "narrateur|Le linge frôle l'allée, un peu frais.",
            "enfant-f|Je sèche, vite, pour sauter.",
            "copain|Moi, je le touche.",
            "narrateur|Aniss s'assoit sur le linge.",
            "narrateur|Nina veut tirer, trop vite.",
            "narrateur|L'eau revient sous le tissu, rusée.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Ce silence d'Aniss tient, net.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
    (1, 2): {
        "sons": "craie,carreau",
        "emphasis": "terrasse",
        "passage": [
            "narrateur|La craie tapote un carreau chaud.",
            "enfant-f|Les carreaux sont des carrés.",
            "copain|Moi, j'en prends deux d'un coup.",
            "narrateur|Le pied d'Aniss couvre deux carreaux.",
            "narrateur|Celui de Nina reste dans un seul.",
            "enfant-f|Ce n'est pas le même saut.",
            "narrateur|Aniss veut aller vers les verres.",
            "narrateur|Nina veut tracer, trop vite.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Nina disparaît.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
    (2, 2): {
        "sons": "caillou,carreau",
        "emphasis": "terrasse",
        "passage": [
            "narrateur|Le caillou glisse sur un carreau.",
            "enfant-f|Pose-le sur la ligne.",
            "copain|Je le fais rouler, moi.",
            "narrateur|Le caillou part vers la table.",
            "narrateur|Nina court, trop vite.",
            "narrateur|Aniss tend la main, puis s'arrête.",
            "narrateur|Il ne dit rien.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
    (3, 2): {
        "sons": "linge,carreau",
        "emphasis": "terrasse",
        "passage": [
            "narrateur|Le linge frôle un carreau chaud.",
            "enfant-f|On sèche les joints, Aniss.",
            "copain|Moi, je m'assois dessus.",
            "narrateur|Aniss s'assoit, pile au milieu.",
            "narrateur|Nina veut tirer le linge.",
            "narrateur|Les verres tremblent, plus rusés.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|Le sourire de Nina disparaît.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
    (1, 3): {
        "sons": "craie,sable",
        "emphasis": "bac",
        "passage": [
            "narrateur|La craie trace un trait dans le sable.",
            "enfant-f|Une marelle dans le bac, Aniss.",
            "copain|Mes pieds font un grand trou.",
            "narrateur|L'empreinte d'Aniss ressemble à un lac.",
            "narrateur|Celle de Nina est une flaque.",
            "enfant-f|Mes carrés disparaissent dessous.",
            "narrateur|Aniss creuse, au lieu de sauter.",
            "narrateur|Nina veut retracer, trop vite.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
    (2, 3): {
        "sons": "caillou,sable",
        "emphasis": "bac",
        "passage": [
            "narrateur|Le caillou s'enfonce dans le sable.",
            "enfant-f|On le pose dans un carré.",
            "copain|Moi, je creuse un puits.",
            "narrateur|Le puits avale le caillou, rusé.",
            "narrateur|Nina plonge la main, trop vite.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|Le sourire de Nina disparaît.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
    (3, 3): {
        "sons": "linge,sable",
        "emphasis": "bac",
        "passage": [
            "narrateur|Le linge lisse un coin de sable.",
            "enfant-f|On dessine, Aniss.",
            "copain|Moi, je le cache.",
            "narrateur|Aniss enterre un coin du linge.",
            "narrateur|Nina tire, trop vite.",
            "narrateur|Le sable tombe, plus rusé.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Aniss reste accroupi, sans un mot.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu proposes comment, Nina ?",
        ],
    },
}

T3_LABS = {
    1: ("attendre un peu", "le linge tendu", "trois grands carrés"),
    2: ("deux carreaux", "les joints", "autour de la table"),
    3: ("l'empreinte", "lisser le sable", "le râteau"),
}

T3_CHOICE = {
    1: [
        "narrateur|L'allée garde trop d'eau.",
        "narrateur|Personne ne donne la réponse.",
        "papa|Attendre, le linge, ou trois carrés ?",
    ],
    2: [
        "narrateur|Les carreaux n'ont pas la même place.",
        "maman|Deux carreaux, les joints, ou la table ?",
        "narrateur|Personne ne donne la réponse.",
    ],
    3: [
        "narrateur|Le sable garde les deux empreintes.",
        "papa|L'empreinte, lisser, ou le râteau ?",
        "narrateur|Personne ne donne la réponse.",
    ],
}

T3_EMPH = {
    1: {1: "attendre", 2: "linge tendu", 3: "trois grands carrés"},
    2: {1: "deux carreaux", 2: "joints", 3: "table"},
    3: {1: "empreinte", 2: "lisser", 3: "râteau"},
}

T3_SONS = {
    (1, 1): "soleil,gravier",
    (1, 2): "linge,eau",
    (1, 3): "craie,gravier",
    (2, 1): "carreau,verre",
    (2, 2): "joint,pierre",
    (2, 3): "table,verre",
    (3, 1): "sable,chaussure",
    (3, 2): "sable,vent",
    (3, 3): "rateau,bois",
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On attend un peu.",
        "copain|Moi aussi, j'attends.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe la craie blanche.",
        "narrateur|Un grain de craie brille au bois.",
        "enfant-f|Le départ, là.",
        "narrateur|Le soleil lèche l'allée, grain après grain.",
        "narrateur|La craie attend au bord, au sec.",
        "narrateur|Nina fait un grand carré, maintenant.",
        "copain|Le mien rentre, cette fois.",
        "papa|Le chemin vous a laissé la place.",
        "maman|Vous avez laissé l'eau partir.",
    ],
    (1, 1, 2): [
        "copain|Je tends le linge, comme un toit.",
        "enfant-f|Un îlot sec, juste là.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute l'allée, un instant.",
        "narrateur|Un grain de craie brille sous le tissu.",
        "enfant-f|Le départ, dessous.",
        "narrateur|Nina trace sous le linge tendu.",
        "narrateur|Quatre grands carrés tiennent dessous.",
        "copain|Mes pieds rentrent, Nina.",
        "enfant-f|Les miens aussi, au milieu.",
        "papa|Vous avez séché, tous les deux.",
        "maman|Le linge a fait de l'ombre.",
    ],
    (1, 1, 3): [
        "enfant-f|Trois grands carrés, pas huit petits.",
        "copain|Un, deux, trois, les mêmes.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle regarde le grain de craie.",
        "enfant-f|Le départ compte un.",
        "narrateur|La craie marque un, puis deux.",
        "narrateur|Les traits sont larges, cette fois.",
        "narrateur|Le pied d'Aniss tient dans un carré.",
        "narrateur|Nina saute le même, légère.",
        "enfant-f|C'est notre marelle, Aniss.",
        "papa|Vous avez compté, tous les deux.",
        "maman|Trois carrés suffisent, dehors.",
    ],
    (1, 2, 1): [
        "copain|Moi, je saute deux carreaux.",
        "enfant-f|Moi, j'en saute un.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe la craie, au joint.",
        "narrateur|Un grain de craie dort sur le carreau.",
        "enfant-f|Le départ, entre nous.",
        "narrateur|La craie marque le bord des deux.",
        "narrateur|Aniss attend au bout, sans presser.",
        "narrateur|Nina le rejoint, un carreau après.",
        "copain|On arrive au même verre.",
        "papa|Chacun sa longueur, même arrivée.",
        "maman|Les verres sont frais.",
    ],
    (1, 2, 2): [
        "enfant-f|On suit les joints, Aniss.",
        "copain|Les lignes minces, entre les carreaux.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute la terrasse, un instant.",
        "narrateur|Un grain de craie tient sur un joint.",
        "enfant-f|Le départ, sur la ligne.",
        "narrateur|Nina pose la craie sur un joint.",
        "narrateur|Nina marche dessus, sans mal.",
        "narrateur|Aniss met un pied devant l'autre.",
        "copain|J'arrive, tout droit.",
        "maman|Le joint vous a gardés.",
        "papa|Les carreaux sont restés à leur place.",
    ],
    (1, 2, 3): [
        "enfant-f|On tourne autour de la table.",
        "copain|Moi dehors, toi plus près.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle cherche le grain de craie.",
        "narrateur|Il brille près des verres.",
        "enfant-f|Le départ, aux verres.",
        "narrateur|La craie suit le tour de table.",
        "narrateur|Le chemin d'Aniss est plus long.",
        "narrateur|Celui de Nina est plus court.",
        "enfant-f|On se retrouve aux verres.",
        "papa|Vous vous êtes rejoints.",
        "maman|La table a gardé l'ombre.",
    ],
    (1, 3, 1): [
        "enfant-f|Reste là, Aniss.",
        "copain|Je ne bouge plus.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe la craie, au sable.",
        "narrateur|Un grain de craie dort dans l'empreinte.",
        "enfant-f|Le départ, dans ton pied.",
        "narrateur|Nina trace autour de sa chaussure.",
        "narrateur|Puis autour de la sienne, plus petite.",
        "narrateur|La craie suit d'abord le grand pied.",
        "copain|Je saute le grand, toi le petit.",
        "papa|Vos pieds ont dessiné le jeu.",
        "maman|Le bac garde les deux traces.",
    ],
    (1, 3, 2): [
        "enfant-f|On lisse, tous les deux.",
        "copain|Moi les bords, toi le milieu.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute le bac, un instant.",
        "narrateur|Un grain de craie tient au rebord.",
        "enfant-f|Le départ, au bord.",
        "narrateur|Le sable redevient plat, sous leurs mains.",
        "narrateur|La craie attend sur le bord lisse.",
        "copain|Un chemin moyen, pour nous deux.",
        "enfant-f|Ni un lac, ni une flaque.",
        "maman|Vous avez aplani, tous les deux.",
        "papa|Le bac vous a laissé la place.",
    ],
    (1, 3, 3): [
        "enfant-f|Papa, le râteau, s'il te plaît.",
        "papa|Je vous fais un grand cadre.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle regarde le grain de craie.",
        "narrateur|Il brille dans un coin du cadre.",
        "enfant-f|Le départ, au coin.",
        "narrateur|Le bois trace un carré large.",
        "narrateur|La craie remplit le grand cadre.",
        "copain|Je mets des traits longs, dedans.",
        "enfant-f|Moi des petits, au bord.",
        "maman|Le râteau a juste aidé.",
        "papa|Vous avez rempli le cadre.",
    ],
    (2, 1, 1): [
        "enfant-f|On attend, avec le caillou.",
        "copain|Moi aussi, j'attends.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe le caillou plat.",
        "narrateur|Un grain de craie brille au bois.",
        "enfant-f|Le départ, là.",
        "narrateur|Le soleil lèche l'allée, grain après grain.",
        "narrateur|Le caillou attend au bord, au sec.",
        "narrateur|Nina pose un grand carré, autour.",
        "copain|Mon pied rentre, cette fois.",
        "papa|Le chemin vous a laissé la place.",
        "maman|Vous avez laissé l'eau partir.",
    ],
    (2, 1, 2): [
        "copain|Je tends le linge, comme un toit.",
        "enfant-f|Le caillou reste au sec.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute l'allée, un instant.",
        "narrateur|Un grain de craie brille sous le tissu.",
        "enfant-f|Le départ, dessous.",
        "narrateur|Le caillou attend sous le linge tendu.",
        "narrateur|Quatre grands carrés tiennent dessous.",
        "copain|Mes pieds rentrent, Nina.",
        "enfant-f|Les miens aussi, au milieu.",
        "papa|Vous avez séché, tous les deux.",
        "maman|Le linge a fait de l'ombre.",
    ],
    (2, 1, 3): [
        "enfant-f|Trois grands carrés, pas huit petits.",
        "copain|Un, deux, trois, les mêmes.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle regarde le grain de craie.",
        "enfant-f|Le départ compte un.",
        "narrateur|Le caillou pose un, puis deux.",
        "narrateur|Les traits sont larges, cette fois.",
        "narrateur|Le pied d'Aniss tient dans un carré.",
        "narrateur|Nina saute le même, légère.",
        "enfant-f|C'est notre marelle, Aniss.",
        "papa|Vous avez compté, tous les deux.",
        "maman|Trois carrés suffisent, dehors.",
    ],
    (2, 2, 1): [
        "copain|Moi, je saute deux carreaux.",
        "enfant-f|Moi, j'en saute un.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe le caillou, au joint.",
        "narrateur|Un grain de craie dort sur le carreau.",
        "enfant-f|Le départ, entre nous.",
        "narrateur|Le caillou saute les deux carreaux.",
        "narrateur|Aniss attend au bout, sans presser.",
        "narrateur|Nina le rejoint, un carreau après.",
        "copain|On arrive au même verre.",
        "papa|Chacun sa longueur, même arrivée.",
        "maman|Les verres sont frais.",
    ],
    (2, 2, 2): [
        "enfant-f|On suit les joints, Aniss.",
        "copain|Les lignes minces, entre les carreaux.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute la terrasse, un instant.",
        "narrateur|Un grain de craie tient sur un joint.",
        "enfant-f|Le départ, sur la ligne.",
        "narrateur|Nina pose le caillou sur un joint.",
        "narrateur|Nina marche dessus, sans mal.",
        "narrateur|Aniss met un pied devant l'autre.",
        "copain|J'arrive, tout droit.",
        "maman|Le joint vous a gardés.",
        "papa|Les carreaux sont restés à leur place.",
    ],
    (2, 2, 3): [
        "enfant-f|On tourne autour de la table.",
        "copain|Moi dehors, toi plus près.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle cherche le grain de craie.",
        "narrateur|Il brille près des verres.",
        "enfant-f|Le départ, aux verres.",
        "narrateur|Le caillou suit le tour de table.",
        "narrateur|Le chemin d'Aniss est plus long.",
        "narrateur|Celui de Nina est plus court.",
        "enfant-f|On se retrouve aux verres.",
        "papa|Vous vous êtes rejoints.",
        "maman|La table a gardé l'ombre.",
    ],
    (2, 3, 1): [
        "enfant-f|Reste là, Aniss.",
        "copain|Je ne bouge plus.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe le caillou, au sable.",
        "narrateur|Un grain de craie dort dans l'empreinte.",
        "enfant-f|Le départ, dans ton pied.",
        "narrateur|Nina trace autour de sa chaussure.",
        "narrateur|Puis autour de la sienne, plus petite.",
        "narrateur|Le caillou attend près du grand pied.",
        "copain|Je saute le grand, toi le petit.",
        "papa|Vos pieds ont dessiné le jeu.",
        "maman|Le bac garde les deux traces.",
    ],
    (2, 3, 2): [
        "enfant-f|On lisse, tous les deux.",
        "copain|Moi les bords, toi le milieu.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute le bac, un instant.",
        "narrateur|Un grain de craie tient au rebord.",
        "enfant-f|Le départ, au bord.",
        "narrateur|Le sable redevient plat, sous leurs mains.",
        "narrateur|Le caillou attend sur le bord lisse.",
        "copain|Un chemin moyen, pour nous deux.",
        "enfant-f|Ni un lac, ni une flaque.",
        "maman|Vous avez aplani, tous les deux.",
        "papa|Le bac vous a laissé la place.",
    ],
    (2, 3, 3): [
        "enfant-f|Papa, le râteau, s'il te plaît.",
        "papa|Je vous fais un grand cadre.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle regarde le grain de craie.",
        "narrateur|Il brille dans un coin du cadre.",
        "enfant-f|Le départ, au coin.",
        "narrateur|Le bois trace un carré large.",
        "narrateur|Le caillou saute dans le grand cadre.",
        "copain|Je mets des traits longs, dedans.",
        "enfant-f|Moi des petits, au bord.",
        "maman|Le râteau a juste aidé.",
        "papa|Vous avez rempli le cadre.",
    ],
    (3, 1, 1): [
        "enfant-f|On attend, avec le linge.",
        "copain|Moi aussi, j'attends.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe le linge plié.",
        "narrateur|Un grain de craie brille au bois.",
        "enfant-f|Le départ, là.",
        "narrateur|Le soleil lèche l'allée, grain après grain.",
        "narrateur|Le linge attend au bord, au sec.",
        "narrateur|Nina essuie, puis trace un grand carré.",
        "copain|Mon pied rentre, cette fois.",
        "papa|Le chemin vous a laissé la place.",
        "maman|Vous avez laissé l'eau partir.",
    ],
    (3, 1, 2): [
        "copain|Je tends le linge, comme un toit.",
        "enfant-f|Un îlot sec, juste là.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute l'allée, un instant.",
        "narrateur|Un grain de craie brille sous le tissu.",
        "enfant-f|Le départ, dessous.",
        "narrateur|Aniss tient le linge, tout haut.",
        "narrateur|Quatre grands carrés tiennent dessous.",
        "copain|Mes pieds rentrent, Nina.",
        "enfant-f|Les miens aussi, au milieu.",
        "papa|Vous avez séché, tous les deux.",
        "maman|Le linge a fait de l'ombre.",
    ],
    (3, 1, 3): [
        "enfant-f|Trois grands carrés, pas huit petits.",
        "copain|Un, deux, trois, les mêmes.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle regarde le grain de craie.",
        "enfant-f|Le départ compte un.",
        "narrateur|Le linge essuie un, puis deux.",
        "narrateur|Les traits sont larges, cette fois.",
        "narrateur|Le pied d'Aniss tient dans un carré.",
        "narrateur|Nina saute le même, légère.",
        "enfant-f|C'est notre marelle, Aniss.",
        "papa|Vous avez compté, tous les deux.",
        "maman|Trois carrés suffisent, dehors.",
    ],
    (3, 2, 1): [
        "copain|Moi, je saute deux carreaux.",
        "enfant-f|Moi, j'en saute un.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe le linge, au joint.",
        "narrateur|Un grain de craie dort sur le carreau.",
        "enfant-f|Le départ, entre nous.",
        "narrateur|Le linge repose entre les deux.",
        "narrateur|Aniss attend au bout, sans presser.",
        "narrateur|Nina le rejoint, un carreau après.",
        "copain|On arrive au même verre.",
        "papa|Chacun sa longueur, même arrivée.",
        "maman|Les verres sont frais.",
    ],
    (3, 2, 2): [
        "enfant-f|On suit les joints, Aniss.",
        "copain|Les lignes minces, entre les carreaux.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute la terrasse, un instant.",
        "narrateur|Un grain de craie tient sur un joint.",
        "enfant-f|Le départ, sur la ligne.",
        "narrateur|Nina pose le linge sur un joint.",
        "narrateur|Nina marche dessus, sans mal.",
        "narrateur|Aniss met un pied devant l'autre.",
        "copain|J'arrive, tout droit.",
        "maman|Le joint vous a gardés.",
        "papa|Les carreaux sont restés à leur place.",
    ],
    (3, 2, 3): [
        "enfant-f|On tourne autour de la table.",
        "copain|Moi dehors, toi plus près.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle cherche le grain de craie.",
        "narrateur|Il brille près des verres.",
        "enfant-f|Le départ, aux verres.",
        "narrateur|Le linge suit le tour de table.",
        "narrateur|Le chemin d'Aniss est plus long.",
        "narrateur|Celui de Nina est plus court.",
        "enfant-f|On se retrouve aux verres.",
        "papa|Vous vous êtes rejoints.",
        "maman|La table a gardé l'ombre.",
    ],
    (3, 3, 1): [
        "enfant-f|Reste là, Aniss.",
        "copain|Je ne bouge plus.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle observe le linge, au sable.",
        "narrateur|Un grain de craie dort dans l'empreinte.",
        "enfant-f|Le départ, dans ton pied.",
        "narrateur|Nina trace autour de sa chaussure.",
        "narrateur|Puis autour de la sienne, plus petite.",
        "narrateur|Le linge essuie autour du grand pied.",
        "copain|Je saute le grand, toi le petit.",
        "papa|Vos pieds ont dessiné le jeu.",
        "maman|Le bac garde les deux traces.",
    ],
    (3, 3, 2): [
        "enfant-f|On lisse, tous les deux.",
        "copain|Moi les bords, toi le milieu.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle écoute le bac, un instant.",
        "narrateur|Un grain de craie tient au rebord.",
        "enfant-f|Le départ, au bord.",
        "narrateur|Le sable redevient plat, sous leurs mains.",
        "narrateur|Le linge a lissé le milieu.",
        "copain|Un chemin moyen, pour nous deux.",
        "enfant-f|Ni un lac, ni une flaque.",
        "maman|Vous avez aplani, tous les deux.",
        "papa|Le bac vous a laissé la place.",
    ],
    (3, 3, 3): [
        "enfant-f|Papa, le râteau, s'il te plaît.",
        "papa|Je vous fais un grand cadre.",
        "narrateur|Nina refuse de foncer.",
        "narrateur|Elle regarde le grain de craie.",
        "narrateur|Il brille dans un coin du cadre.",
        "enfant-f|Le départ, au coin.",
        "narrateur|Le bois trace un carré large.",
        "narrateur|Le linge essuie le grand cadre.",
        "copain|Je mets des traits longs, dedans.",
        "enfant-f|Moi des petits, au bord.",
        "maman|Le râteau a juste aidé.",
        "papa|Vous avez rempli le cadre.",
    ],
}

END_SONS = {1: "verre,craie", 2: "verre,caillou", 3: "verre,linge"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|L'allée est sèche, maintenant.",
        "copain|On a attendu le soleil, d'abord.",
        "enfant-f|Puis on a sauté.",
        "papa|Le grand carré a pris ton pied.",
        "maman|Buvez, l'eau est fraîche.",
        "narrateur|La craie repose près du verre.",
        "narrateur|Un grain de craie tient au bois.",
        "copain|Il est à nous.",
        "narrateur|Une goutte sèche sur le gravier.",
    ],
    (1, 1, 2): [
        "narrateur|Le linge retombe, lentement.",
        "enfant-f|Ton toit a séché l'allée.",
        "copain|Tes carrés étaient assez larges.",
        "papa|Vous avez tendu, tous les deux.",
        "maman|Accrochez le linge, s'il est mouillé.",
        "narrateur|Nina pose la craie au bord.",
        "narrateur|Un grain de craie brille sous le tissu.",
        "enfant-f|Goûte l'eau, Aniss.",
        "narrateur|Une tache sèche reste au milieu.",
    ],
    (1, 1, 3): [
        "narrateur|Trois carrés brillent, un peu.",
        "copain|Un, deux, trois, on a compté.",
        "enfant-f|Les mêmes pour toi et moi.",
        "maman|Vos chaussures ont de la poussière.",
        "papa|Soufflez, léger, dessus.",
        "narrateur|La craie laisse un trait blanc.",
        "narrateur|Un grain de craie dort dans le premier.",
        "enfant-f|C'est notre marelle.",
        "narrateur|Le gravier se tait, chaud.",
    ],
    (1, 2, 1): [
        "narrateur|Ils s'assoient au bord des carreaux.",
        "enfant-f|Toi deux, moi un.",
        "copain|On est arrivés au même verre.",
        "papa|Chacun sa longueur, même jeu.",
        "maman|L'eau a attendu à sa place.",
        "enfant-f|Elle est pour Aniss, maintenant.",
        "narrateur|La craie repose près du verre.",
        "narrateur|Un grain de craie tient sur ton carreau.",
        "narrateur|Un carreau garde le soleil.",
    ],
    (1, 2, 2): [
        "narrateur|Les joints sont un peu poussiéreux.",
        "copain|On les a suivis, tous les deux.",
        "enfant-f|Tes pieds allaient tout droit.",
        "maman|Le mince chemin vous a gardés.",
        "papa|Lavez-vous, un peu, les mains.",
        "narrateur|La craie garde un grain de sable.",
        "copain|Je bois, Nina.",
        "narrateur|Un grain de craie reste au joint.",
        "narrateur|L'eau claque, puis se tait.",
    ],
    (1, 2, 3): [
        "narrateur|La table a un peu d'ombre.",
        "enfant-f|Tu as fait le grand tour.",
        "copain|Moi dehors, toi plus près.",
        "papa|Vous vous êtes rejoints aux verres.",
        "maman|Changez le linge, s'il est chaud.",
        "narrateur|La craie repose près du verre.",
        "narrateur|Un grain de craie brille sur le bois.",
        "enfant-f|Regarde-le, Aniss, il brille.",
        "narrateur|Les carreaux redeviennent calmes.",
    ],
    (1, 3, 1): [
        "narrateur|Le bac garde deux traces.",
        "copain|Tu as dessiné mon pied.",
        "enfant-f|Puis le mien, plus petit.",
        "maman|Essuie tes chaussures, sur l'herbe.",
        "papa|Le sable est tiède, maintenant.",
        "narrateur|Nina pose la craie au milieu.",
        "narrateur|Un grain de craie dort dans l'empreinte.",
        "copain|On a sauté, tous les deux.",
        "narrateur|Un rai de soleil traverse le bac.",
    ],
    (1, 3, 2): [
        "narrateur|Le sable est plat, jusqu'au bord.",
        "enfant-f|On a lissé, tous les deux.",
        "copain|Un chemin moyen, après.",
        "papa|Le bac vous a laissé le temps.",
        "maman|Le grain sèche sur vos doigts.",
        "narrateur|La craie pose un grain de sable.",
        "narrateur|Un grain de craie tient au rebord.",
        "copain|Il roule trop bien, Nina.",
        "narrateur|Le verre garde l'eau, proche.",
    ],
    (1, 3, 3): [
        "narrateur|Un peu de sable reste au râteau.",
        "enfant-f|Papa a fait le cadre.",
        "copain|Nous, on a rempli dedans.",
        "papa|Le bois a juste aidé.",
        "maman|Vos mains sentent le soleil.",
        "narrateur|La craie repose près du verre.",
        "narrateur|Un grain de craie brille au coin.",
        "enfant-f|Tu as sauté, Aniss.",
        "narrateur|Le bac brille un peu, puis s'endort.",
    ],
    (2, 1, 1): [
        "narrateur|L'allée est sèche, maintenant.",
        "copain|On a attendu le soleil, d'abord.",
        "enfant-f|Puis on a sauté.",
        "papa|Le grand carré a pris ton pied.",
        "maman|Buvez, l'eau est fraîche.",
        "narrateur|Le caillou clique, un dernier coup.",
        "narrateur|Un grain de craie tient au bois.",
        "copain|Il est à nous.",
        "narrateur|Le caillou repose près du verre.",
    ],
    (2, 1, 2): [
        "narrateur|Le linge retombe, lentement.",
        "enfant-f|Ton toit a séché l'allée.",
        "copain|Tes carrés étaient assez larges.",
        "papa|Vous avez tendu, tous les deux.",
        "maman|Accrochez le linge, s'il est mouillé.",
        "narrateur|Nina pose le caillou au bord.",
        "narrateur|Un grain de craie brille sous le tissu.",
        "enfant-f|Goûte l'eau, Aniss.",
        "narrateur|Un fil d'eau sèche sous le linge.",
    ],
    (2, 1, 3): [
        "narrateur|Trois carrés brillent, un peu.",
        "copain|Un, deux, trois, on a compté.",
        "enfant-f|Les mêmes pour toi et moi.",
        "maman|Vos chaussures ont de la poussière.",
        "papa|Soufflez, léger, dessus.",
        "narrateur|Le caillou laisse un creux blanc.",
        "narrateur|Un grain de craie dort dans le deuxième.",
        "enfant-f|C'est notre marelle.",
        "narrateur|Trois traces blanches tiennent au gravier.",
    ],
    (2, 2, 1): [
        "narrateur|Ils s'assoient au bord des carreaux.",
        "enfant-f|Toi deux, moi un.",
        "copain|On est arrivés au même verre.",
        "papa|Chacun sa longueur, même jeu.",
        "maman|L'eau a attendu à sa place.",
        "enfant-f|Elle est pour Aniss, maintenant.",
        "narrateur|Le caillou repose près du verre.",
        "narrateur|Un grain de craie tient sur son carreau.",
        "narrateur|L'eau claque dans le verre, nette.",
    ],
    (2, 2, 2): [
        "narrateur|Les joints sont un peu poussiéreux.",
        "copain|On les a suivis, tous les deux.",
        "enfant-f|Tes pieds allaient tout droit.",
        "maman|Le mince chemin vous a gardés.",
        "papa|Lavez-vous, un peu, les mains.",
        "narrateur|Le caillou garde un grain de sable.",
        "copain|Je bois, Nina.",
        "narrateur|Un grain de craie reste au joint.",
        "narrateur|Un joint garde un grain de craie.",
    ],
    (2, 2, 3): [
        "narrateur|La table a un peu d'ombre.",
        "enfant-f|Tu as fait le grand tour.",
        "copain|Moi dehors, toi plus près.",
        "papa|Vous vous êtes rejoints aux verres.",
        "maman|Changez le linge, s'il est chaud.",
        "narrateur|Le caillou repose près du verre.",
        "narrateur|Un grain de craie brille sur le bois.",
        "enfant-f|Regarde-le, Aniss, il brille.",
        "narrateur|Un rond d'eau marque le bois.",
    ],
    (2, 3, 1): [
        "narrateur|Le bac garde deux traces.",
        "copain|Tu as dessiné mon pied.",
        "enfant-f|Puis le mien, plus petit.",
        "maman|Essuie tes chaussures, sur l'herbe.",
        "papa|Le sable est tiède, maintenant.",
        "narrateur|Aniss pose le caillou au milieu.",
        "narrateur|Un grain de craie dort dans l'empreinte.",
        "copain|On a sauté, tous les deux.",
        "narrateur|Deux empreintes gardent le caillou.",
    ],
    (2, 3, 2): [
        "narrateur|Le sable est plat, jusqu'au bord.",
        "enfant-f|On a lissé, tous les deux.",
        "copain|Un chemin moyen, après.",
        "papa|Le bac vous a laissé le temps.",
        "maman|Le grain sèche sur vos doigts.",
        "narrateur|Le caillou pose un grain de sable.",
        "narrateur|Un grain de craie tient au rebord.",
        "copain|Il roule trop bien, Nina.",
        "narrateur|Le caillou roule droit, sans se perdre.",
    ],
    (2, 3, 3): [
        "narrateur|Un peu de sable reste au râteau.",
        "enfant-f|Papa a fait le cadre.",
        "copain|Nous, on a rempli dedans.",
        "papa|Le bois a juste aidé.",
        "maman|Vos mains sentent le soleil.",
        "narrateur|Le caillou repose près du verre.",
        "narrateur|Un grain de craie brille au coin.",
        "enfant-f|Tu as sauté, Aniss.",
        "narrateur|Le râteau garde un fil de sable.",
    ],
    (3, 1, 1): [
        "narrateur|L'allée est sèche, maintenant.",
        "copain|On a attendu le soleil, d'abord.",
        "enfant-f|Puis on a sauté.",
        "papa|Le grand carré a pris ton pied.",
        "maman|Buvez, l'eau est fraîche.",
        "narrateur|Le linge sèche près du verre.",
        "narrateur|Un grain de craie tient au bois.",
        "copain|Il est à nous.",
        "narrateur|Le linge plié garde une odeur d'eau.",
    ],
    (3, 1, 2): [
        "narrateur|Le linge retombe, lentement.",
        "enfant-f|Ton toit a séché l'allée.",
        "copain|Tes carrés étaient assez larges.",
        "papa|Vous avez tendu, tous les deux.",
        "maman|Accrochez le linge, s'il est mouillé.",
        "narrateur|Nina pose le linge au bord.",
        "narrateur|Un grain de craie brille sous le tissu.",
        "enfant-f|Goûte l'eau, Aniss.",
        "narrateur|Le toit de linge retombe, lent.",
    ],
    (3, 1, 3): [
        "narrateur|Trois carrés brillent, un peu.",
        "copain|Un, deux, trois, on a compté.",
        "enfant-f|Les mêmes pour toi et moi.",
        "maman|Vos chaussures ont de la poussière.",
        "papa|Soufflez, léger, dessus.",
        "narrateur|Le linge laisse un trait blanc.",
        "narrateur|Un grain de craie dort dans le troisième.",
        "enfant-f|C'est notre marelle.",
        "narrateur|Le linge garde un trait blanc.",
    ],
    (3, 2, 1): [
        "narrateur|Ils s'assoient au bord des carreaux.",
        "enfant-f|Toi deux, moi un.",
        "copain|On est arrivés au même verre.",
        "papa|Chacun sa longueur, même jeu.",
        "maman|L'eau a attendu à sa place.",
        "enfant-f|Elle est pour Aniss, maintenant.",
        "narrateur|Le linge repose près du verre.",
        "narrateur|Un grain de craie tient entre deux carreaux.",
        "narrateur|Le linge repose entre deux carreaux.",
    ],
    (3, 2, 2): [
        "narrateur|Les joints sont un peu poussiéreux.",
        "copain|On les a suivis, tous les deux.",
        "enfant-f|Tes pieds allaient tout droit.",
        "maman|Le mince chemin vous a gardés.",
        "papa|Lavez-vous, un peu, les mains.",
        "narrateur|Le linge garde un grain de sable.",
        "copain|Je bois, Nina.",
        "narrateur|Un grain de craie reste au joint.",
        "narrateur|Le linge sent le joint, un peu.",
    ],
    (3, 2, 3): [
        "narrateur|La table a un peu d'ombre.",
        "enfant-f|Tu as fait le grand tour.",
        "copain|Moi dehors, toi plus près.",
        "papa|Vous vous êtes rejoints aux verres.",
        "maman|Changez le linge, s'il est chaud.",
        "narrateur|Le linge repose près du verre.",
        "narrateur|Un grain de craie brille sur le bois.",
        "enfant-f|Regarde-le, Aniss, il brille.",
        "narrateur|Le linge sent le bois chaud.",
    ],
    (3, 3, 1): [
        "narrateur|Le bac garde deux traces.",
        "copain|Tu as dessiné mon pied.",
        "enfant-f|Puis le mien, plus petit.",
        "maman|Essuie tes chaussures, sur l'herbe.",
        "papa|Le sable est tiède, maintenant.",
        "narrateur|Nina pose le linge au milieu.",
        "narrateur|Un grain de craie dort dans l'empreinte.",
        "copain|On a sauté, tous les deux.",
        "narrateur|Le linge borde les deux traces.",
    ],
    (3, 3, 2): [
        "narrateur|Le sable est plat, jusqu'au bord.",
        "enfant-f|On a lissé, tous les deux.",
        "copain|Un chemin moyen, après.",
        "papa|Le bac vous a laissé le temps.",
        "maman|Le grain sèche sur vos doigts.",
        "narrateur|Le linge pose un grain de sable.",
        "narrateur|Un grain de craie tient au rebord.",
        "copain|Il roule trop bien, Nina.",
        "narrateur|Le linge a lissé le milieu, net.",
    ],
    (3, 3, 3): [
        "narrateur|Un peu de sable reste au râteau.",
        "enfant-f|Papa a fait le cadre.",
        "copain|Nous, on a rempli dedans.",
        "papa|Le bois a juste aidé.",
        "maman|Vos mains sentent le soleil.",
        "narrateur|Le linge repose près du verre.",
        "narrateur|Un grain de craie brille au coin.",
        "enfant-f|Tu as sauté, Aniss.",
        "narrateur|Le linge essuie le grand cadre, une dernière fois.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "pluie,escargot,linge",
        {"emphasis": "grain de craie"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("la craie blanche", "le caillou plat", "le linge")},
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
            {"emphasis": "grain de craie"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("l'allée", "la terrasse", "le bac")},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[a],
                    {"emphasis": "grain de craie"},
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
        "tailles différentes",
        "plus petit ou plus grand",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "jouer ensemble",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
        "arrosoir",
        "toboggan",
        "mica",
        "couleur de miel",
        "merle",
        "j'ai une idée",
        "on dirait que notre mission",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    for clue in (
        "étoile brune", "fil pâle", "croissant d'eau", "croissant pâle",
        "virgule farine", "bouton nacre", "nœud raphia", "pois ivoire",
        "grain savon rose", "grain vanille", "pastille colle", "virgule buée",
        "virgule de buée", "capuchon penche", "grain doré", "brin safran",
        "anneau liège", "clou tête ronde", "grain d'ambre", "goutte de cire",
        "anneau de zinc", "larme de bronze", "point de cire", "bracelet d'écorce",
        "boucle d'étain", "anneau de pollen", "dent de laitue", "éclat de zinc",
        "éclat de thym", "lune d'étain", "grain de grenat", "grain d'indigo",
        "grain de brique", "éclat vert", "écaille d'étain", "vis verte",
        "cristal de sucre", "écaille de lichen", "grain de cire claire",
        "dent de fermeture", "écaille de nacre", "grain de paprika",
        "écaille de boue", "point de rouille", "grain de mica", "grain de cannelle",
        "grain d'ocre", "grain de feutre", "grain de sésame", "écaille de savon",
        "grain de suie", "grain de limon", "grain de quartz", "grain de sel",
        "grain de lessive", "grain de cerise", "rond d'huile", "écaille d'orange",
        "point d'écume", "grain de sève", "point de beurre",
    ):
        if clue in whole:
            raise SystemExit(f"{SID} indice interdit: {clue}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "grain de craie" not in blob:
        raise SystemExit(f"{SID}: grain de craie absent")
    if "escargot" not in blob:
        raise SystemExit(f"{SID}: escargot absent")

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
        if "grain de craie" not in c["text"].lower():
            raise SystemExit(f"fin sans grain: {c['chunk_id']}")
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

    tts_ok = all(
        c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") and c.get("text_ssml")
        for c in story["chunks"]
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c["text_xai_tags"] == c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-022 — La marelle de Nina, pour Aniss aussi\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.COR.001 — jouer avec Aniss, pas toute seule (vécue, non dite)\n"
        "- **Personnages :** Nina, Aniss, papa, maman\n"
        "- **Lieu :** jardin mouillé, allée, terrasse, bac à sable — piste des carrés\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Nina connaît le jardin après la pluie. Un escargot avance. Papa tend le linge. "
        "Sur la table, un **grain de craie** brille dans une goutte. Nina veut une marelle "
        "où Aniss saute aussi, maintenant. Elle appelle trop vite : Aniss se tait. "
        "Le silence est une réponse. Première idée ratée. Craie, caillou, linge : les trois "
        "restent. Allée mouillée (l'eau efface), terrasse (deux carreaux contre un), "
        "bac (le trou d'Aniss avale le dessin). Nina refuse de foncer. Attendre, linge-toit, "
        "trois grands carrés ; deux carreaux, joints, tour de table ; empreinte, lisser, "
        "râteau. Le grain du début revient. L'objet porte une trace.\n\n"
        "## Vécu\n\n"
        "Nina propose. Aniss prend son temps, ou pose sa limite. Deux rythmes, "
        "sans voix caricaturale. Le sourire disparaît ; envie et inquiétude se bousculent. "
        "Papa ou maman s'accroupit à la même hauteur. Personne ne donne la réponse. "
        "Nina observe l'objet, écoute le jardin, retrouve le grain. La leçon se voit : "
        "elle refait le jeu pour qu'Aniss saute aussi.\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Plus petit ou plus grand » / Zoé / « voici le geste » / « encore » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (papa : tu as vu le grain). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N1 ≤ 10. `check()` OK. Pas apply. Monde ≠ TREE-DIF-005, ≠ TREE-COL-008.\n\n"
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
