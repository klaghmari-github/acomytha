#!/usr/bin/env python3
"""TREE-DIF-070 — F-NAR-019. Album de Nina, arrêt du bus. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-070"
N1 = 10
TITLE = "L'album de Nina, à l'arrêt du bus"
FIL = (
    "À l'arrêt du bus, Nina veut finir la dernière page du loup "
    "avant que le bus arrive. Elle coupe Victorino : « Manger ! » "
    "Le mot manque. T1 = album / ticket / coussin. "
    "T2 = banc (goutte) / vitre (buée) / bord (phare). "
    "T3 = neuf façons d'entendre la fin. On monte, page lue."
)
CHARS = "Nina, Victorino, papa, maman"
SETTING = "arrêt du bus du village : banc mouillé, abri de verre, bord du trottoir"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "album rouge",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le bus n_est_pas_là_mais_Nina_coupe; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change l_écoute; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=le_loup_n_a_pas_sa_fin; tempo=naturel; sourire=léger; respiration=fluide",
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
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=la_phrase_de_Victorino_se_casse; tempo=resserré; sourire=aucun; respiration=retenue",
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
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_dernière_page_et_le_bus_se_rejoignent; tempo=posé; sourire=léger; respiration=ample",
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


OPENING = [
    "narrateur|Sous l'abri de verre, la gouttière tape.",
    "narrateur|Une flaque ronde brille au pied du banc.",
    "narrateur|Ça sent le bitume mouillé, et la laine.",
    "narrateur|La ligne jaune du trottoir luit, mouillée.",
    "papa|Le banc est froid, Nina.",
    "enfant-f|Mon album est resté sec.",
    "maman|Le loup attend sa dernière page.",
    "narrateur|Victorino tient le ticket carton, serré.",
    "narrateur|Un petit coussin gris pend sous le bras.",
    "narrateur|En ce moment, Nina ouvre l'album rouge.",
    "enfant-f|Avant le bus, je finis le loup.",
    "narrateur|Victorino ouvre la bouche.",
    "enfant-m|Le loup, il va.",
    "enfant-f|Manger !",
    "narrateur|Victorino ferme la bouche.",
    "narrateur|Le mot n'est pas venu.",
    "papa|On n'a pas entendu la fin.",
    "enfant-f|Mais le bus arrive !",
    "maman|Le phare est loin, très loin.",
    "papa|Merci, tu as essuyé le banc.",
]

T1_CHOICE = [
    "narrateur|Près des genoux, trois affaires attendent.",
    "narrateur|L'album, le ticket, le coussin.",
    "maman|Par quoi tu commences, Nina ?",
]

T1 = {
    1: {
        "lab": "l'album",
        "sons": "pages,tissu",
        "emphasis": "album rouge",
        "passage": [
            "narrateur|Nina prend d'abord l'album rouge.",
            "enfant-f|La dernière page, vite.",
            "papa|Garde le rouge contre toi.",
            "narrateur|Elle saute trop de pages, d'un coup.",
            "narrateur|Le papier claque sous ses doigts.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Manger !",
            "narrateur|Victorino ferme la bouche.",
            "maman|Le ticket, ensuite, dans la poche.",
            "narrateur|Papa glisse le coussin sous le rouge.",
            "narrateur|Les trois partent, collés à Nina.",
            "enfant-f|C'était trop tôt.",
            "papa|L'album d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nina a pris l'album d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "album",
            "accepted_examples": "album | l'album | le rouge | l'album rouge | le livre",
            "retry_prompt": "Nina prend l'album d'abord.",
        },
        "confirm": [
            "narrateur|L'album reste sur ses genoux.",
            "enfant-f|On va jusqu'à la fin.",
            "maman|Le bus n'est pas là.",
            "papa|Tu tiens bien, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|La dernière page attend, toute proche.",
        ],
        "voy": "L'album penche vers l'abri.",
    },
    2: {
        "lab": "le ticket",
        "sons": "carton,poche",
        "emphasis": "ticket",
        "passage": [
            "narrateur|Nina prend d'abord le ticket carton.",
            "enfant-f|Pour le bus, vite.",
            "maman|Garde le carton dans ta poche.",
            "narrateur|Elle agite le ticket vers la rue.",
            "narrateur|Le carton tape l'air, sec.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Manger !",
            "narrateur|Victorino se tait, les joues chaudes.",
            "papa|L'album, ensuite, sur tes genoux.",
            "narrateur|Maman glisse le coussin sous le rouge.",
            "narrateur|Les trois partent, collés à Nina.",
            "enfant-f|J'ai trop parlé, moi.",
            "maman|Le ticket d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nina a pris le ticket d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "ticket",
            "accepted_examples": "ticket | le ticket | le carton | ticket carton",
            "retry_prompt": "Nina prend le ticket d'abord.",
        },
        "confirm": [
            "narrateur|Le ticket pend à sa poche.",
            "enfant-f|Il va servir, plus tard.",
            "papa|Ça sent le carton, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le carton se tait contre le tissu.",
        ],
        "voy": "Le ticket penche vers l'abri.",
    },
    3: {
        "lab": "le coussin",
        "sons": "tissu,flaque",
        "emphasis": "coussin",
        "passage": [
            "narrateur|Nina prend d'abord le petit coussin.",
            "enfant-f|Pour le banc mouillé.",
            "papa|Mets le tissu sous le rouge.",
            "narrateur|Elle pose le coussin trop fort.",
            "narrateur|Une flaque saute sur le bois.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Manger !",
            "narrateur|L'eau éclabousse.",
            "narrateur|Victorino se tait.",
            "maman|L'album, ensuite, et le ticket.",
            "narrateur|Papa les pose contre elle.",
            "narrateur|Les trois partent, collés à Nina.",
            "enfant-f|Le banc a parlé trop fort.",
            "papa|Le coussin d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nina a pris le coussin d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "coussin",
            "accepted_examples": "coussin | le coussin | le petit coussin | le tissu",
            "retry_prompt": "Nina prend le coussin d'abord.",
        },
        "confirm": [
            "narrateur|Le coussin reste plat, sous le rouge.",
            "enfant-f|Le banc ne mouille plus.",
            "maman|Le tissu sent le tiroir.",
            "papa|On avance, tous les quatre ?",
            "enfant-f|Oui.",
            "narrateur|Le gris tiède attend la suite.",
        ],
        "voy": "Le coussin penche vers l'abri.",
    },
}

T2 = {
    (1, 1): {
        "sons": "goutte,gouttiere",
        "emphasis": "goutte",
        "passage": [
            "narrateur|Sur ses genoux, l'album est tiède.",
            "narrateur|La gouttière tape trop fort.",
            "narrateur|Une goutte tombe sur le rouge.",
            "enfant-m|Le loup, il va.",
            "narrateur|La goutte couvre le mot.",
            "enfant-f|Il va manger, c'est ça ?",
            "narrateur|Victorino reprend trop vite.",
            "narrateur|La goutte prend sa phrase.",
            "papa|On n'entend plus le mot.",
            "maman|La page a bu le son.",
            "enfant-f|Alors on fait quoi ?",
            "papa|Tu vois comment, Nina ?",
        ],
    },
    (1, 2): {
        "sons": "vapeur,verre",
        "emphasis": "buée",
        "passage": [
            "narrateur|Nina presse l'album contre la vitre.",
            "narrateur|La buée cache trop le verre.",
            "narrateur|Le rouge se colle, flou.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Il court, c'est ça ?",
            "narrateur|Victorino secoue la tête.",
            "narrateur|Sa bouche disparaît dans le blanc.",
            "papa|On n'a pas vu ses lèvres.",
            "maman|La buée a pris le mot.",
            "enfant-f|Comment on entend, là ?",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (1, 3): {
        "sons": "phare,rue",
        "emphasis": "phare",
        "passage": [
            "narrateur|Nina avance l'album vers la rue.",
            "narrateur|Un phare brille, trop loin.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Dépêche, le bus arrive !",
            "narrateur|Le mot de Victorino s'arrête.",
            "narrateur|Ce n'est pas le bus.",
            "papa|C'est une voiture, seulement.",
            "maman|Sa phrase n'est pas finie.",
            "enfant-f|On va rater le mot ?",
            "papa|Tu vois comment, Nina ?",
        ],
    },
    (2, 1): {
        "sons": "goutte,carton",
        "emphasis": "ticket",
        "passage": [
            "narrateur|Dans sa poche, le ticket est tiède.",
            "narrateur|Une goutte vise le carton.",
            "narrateur|Nina crie : le ticket !",
            "enfant-m|Le loup, il va.",
            "enfant-f|Le ticket, il est mouillé !",
            "narrateur|Sa voix recouvre celle de Victorino.",
            "narrateur|Le mot tombe dans la flaque.",
            "papa|Le carton va sécher.",
            "maman|Lui, il n'a pas fini.",
            "enfant-f|J'ai trop crié ?",
            "papa|Tu vois comment, Nina ?",
        ],
    },
    (2, 2): {
        "sons": "carton,verre",
        "emphasis": "buée",
        "passage": [
            "narrateur|Nina frotte la vitre avec le ticket.",
            "narrateur|Le carton laisse une trace grise.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Attends, je vois rien !",
            "narrateur|Victorino parle derrière le gris.",
            "narrateur|Sa bouche reste un nuage.",
            "papa|Le carton a sali le verre.",
            "maman|On n'a pas lu ses lèvres.",
            "enfant-f|Il a dit quoi, alors ?",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (2, 3): {
        "sons": "phare,carton",
        "emphasis": "phare",
        "passage": [
            "narrateur|Nina tend le ticket vers la rue.",
            "narrateur|Un rond jaune grandit, loin.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Chauffeur, on est là !",
            "narrateur|Le phare n'est pas le bus.",
            "narrateur|Victorino avale son mot.",
            "papa|Le carton n'arrête pas un phare.",
            "maman|Sa phrase est restée dedans.",
            "enfant-f|On fait comment, papa ?",
            "papa|Tu vois comment, Nina ?",
        ],
    },
    (3, 1): {
        "sons": "goutte,tissu",
        "emphasis": "goutte",
        "passage": [
            "narrateur|Sous l'album, le coussin est tiède.",
            "narrateur|Une goutte pèse sur le gris.",
            "narrateur|Nina saute, et l'eau gicle.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Aïe, c'est froid !",
            "narrateur|Le mot se noie dans le splash.",
            "papa|Le tissu a pris la goutte.",
            "maman|Victorino n'a pas fini.",
            "enfant-f|Le coussin a trop parlé.",
            "papa|Tu vois comment, Nina ?",
        ],
    },
    (3, 2): {
        "sons": "tissu,verre",
        "emphasis": "buée",
        "passage": [
            "narrateur|Nina essuie la vitre avec le coussin.",
            "narrateur|Le gris écarte la buée, puis revient.",
            "enfant-m|Le loup, il va.",
            "enfant-f|C'est tout blanc !",
            "narrateur|Victorino parle dans le nuage.",
            "narrateur|Personne ne voit sa bouche.",
            "papa|Le tissu a trop poussé.",
            "maman|Le mot s'est perdu.",
            "enfant-f|Comment on le rattrape ?",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (3, 3): {
        "sons": "phare,tissu",
        "emphasis": "phare",
        "passage": [
            "narrateur|Le coussin glisse vers le bord.",
            "narrateur|Nina se penche pour l'attraper.",
            "enfant-m|Le loup, il va.",
            "enfant-f|Mon coussin !",
            "narrateur|Un phare passe, trop loin.",
            "narrateur|Le mot tombe entre deux pas.",
            "papa|Le gris est là, rattrapé.",
            "maman|La phrase, non.",
            "enfant-f|Il va rater sa fin ?",
            "papa|Tu vois comment, Nina ?",
        ],
    },
}

T3_LABS = {
    1: ("la goutte", "le manteau", "tout près"),
    2: ("le doigt", "le souffle", "le loup"),
    3: ("le pas", "la page", "le phare"),
}

T3_CHOICE = {
    1: [
        "narrateur|La gouttière n'a pas fini.",
        "papa|La goutte, le manteau, ou tout près ?",
    ],
    2: [
        "narrateur|La buée n'a pas fini.",
        "maman|Le doigt, le souffle, ou le loup ?",
    ],
    3: [
        "narrateur|Le phare n'a pas fini.",
        "papa|Le pas, la page, ou le phare ?",
    ],
}

T3_SONS = {
    (1, 1): "goutte,silence",
    (1, 2): "manteau,tissu",
    (1, 3): "pas,voix",
    (2, 1): "doigt,verre",
    (2, 2): "souffle,vapeur",
    (2, 3): "pages,voix",
    (3, 1): "pas,trottoir",
    (3, 2): "pages,silence",
    (3, 3): "phare,compte",
}

T3_EMPH = {
    1: {1: "goutte", 2: "manteau", 3: "tout près"},
    2: {1: "doigt", 2: "souffle", 3: "loup"},
    3: {1: "pas", 2: "page", 3: "phare"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On attend la goutte.",
        "narrateur|Nina tient l'album, sans tourner.",
        "narrateur|La gouttière se tait, une fois.",
        "enfant-m|Le loup, il va dormir.",
        "narrateur|L'album reste ouvert, sans bouger.",
        "papa|Le mot est arrivé, tout entier.",
        "enfant-f|Il va dormir.",
        "maman|La page peut venir, maintenant.",
    ],
    (1, 1, 2): [
        "enfant-f|Le manteau, dessus.",
        "narrateur|Maman pose le manteau sur le rouge.",
        "narrateur|La goutte tombe à côté, molle.",
        "enfant-m|Le loup, il va se cacher.",
        "narrateur|Sous le tissu, la page reste sèche.",
        "papa|On a entendu, sous le manteau.",
        "enfant-f|Il se cache.",
        "maman|Le manteau a gardé la page.",
    ],
    (1, 1, 3): [
        "enfant-f|Tout près, j'écoute.",
        "narrateur|Nina se glisse contre Victorino, tout près.",
        "narrateur|La goutte reste loin, sur le bois.",
        "enfant-m|Le loup, il va fermer l'œil.",
        "narrateur|L'album ne bouge pas entre eux.",
        "papa|Tu t'es mise tout près.",
        "enfant-f|Il ferme l'œil.",
        "maman|Ses mots sont arrivés.",
    ],
    (1, 2, 1): [
        "enfant-f|Le doigt, sur la buée.",
        "narrateur|Nina trace un rond, tout net.",
        "narrateur|La bouche de Victorino se voit.",
        "enfant-m|Le loup va sous la lune.",
        "narrateur|L'album reste ouvert contre le verre.",
        "papa|On a vu le mot, sur ses lèvres.",
        "enfant-f|Sous la lune.",
        "maman|Le rond a laissé la suite.",
    ],
    (1, 2, 2): [
        "enfant-f|On souffle ensemble.",
        "narrateur|Nina et Victorino respirent, puis s'arrêtent.",
        "narrateur|Personne ne devine trop tôt.",
        "enfant-m|Le loup va près de l'arbre.",
        "narrateur|L'album attend, page tiède.",
        "papa|Vous avez respiré, puis parlé.",
        "enfant-f|Près de l'arbre.",
        "maman|Le souffle a laissé sa place.",
    ],
    (1, 2, 3): [
        "enfant-f|Le loup, sur le dessin.",
        "narrateur|Nina pose le doigt sur le loup.",
        "narrateur|Victorino regarde aussi, sans parler.",
        "enfant-m|Le loup va sans crier.",
        "narrateur|Le rouge reste ouvert, sous le doigt.",
        "papa|Le dessin a tenu le mot.",
        "enfant-f|Sans crier.",
        "maman|Vous avez regardé ensemble.",
    ],
    (1, 3, 1): [
        "enfant-f|On reste, un pas.",
        "narrateur|Nina ne court pas vers le phare.",
        "narrateur|Victorino reprend, plus lent.",
        "enfant-m|Le loup se fait tout petit.",
        "narrateur|L'album reste contre elle, au bord.",
        "papa|Le bus est trop loin.",
        "enfant-f|Tout petit.",
        "maman|Vous n'avez pas couru.",
    ],
    (1, 3, 2): [
        "enfant-f|La page, ouverte.",
        "narrateur|Nina garde l'album ouvert, tout près.",
        "narrateur|Victorino pose un doigt, puis parle.",
        "enfant-m|Le loup rentre dans sa grotte.",
        "narrateur|La page garde le mot, ouverte.",
        "papa|La page a gardé le mot.",
        "enfant-f|Dans sa grotte.",
        "maman|Vous avez lu ensemble.",
    ],
    (1, 3, 3): [
        "enfant-f|Le phare, on le compte.",
        "narrateur|Le rond jaune grandit, lentement.",
        "narrateur|L'album reste ouvert pendant le compte.",
        "enfant-m|Le loup part avec le vent.",
        "narrateur|Personne ne coupe le mot.",
        "papa|Le phare n'a pas coupé le mot.",
        "enfant-f|Avec le vent.",
        "maman|Le compte a laissé sa phrase.",
    ],
    (2, 1, 1): [
        "enfant-f|On attend, ticket à plat.",
        "narrateur|Nina tient le carton, sans crier.",
        "narrateur|La goutte finit sur le banc, seule.",
        "enfant-m|Le loup, il va dormir.",
        "narrateur|Le ticket reste sec, dans la poche.",
        "papa|Le carton a eu le temps.",
        "enfant-f|Il va dormir.",
        "maman|Toi, tu n'as pas crié.",
    ],
    (2, 1, 2): [
        "enfant-f|Le manteau sur le ticket.",
        "narrateur|Maman couvre le carton, et l'album.",
        "narrateur|La goutte frappe le tissu, pas le carton.",
        "enfant-m|Le loup, il va se cacher.",
        "narrateur|Le ticket reste plat, au chaud.",
        "papa|On a entendu sous le manteau.",
        "enfant-f|Il se cache.",
        "maman|Le carton n'a pas volé le mot.",
    ],
    (2, 1, 3): [
        "enfant-f|Tout près, j'écoute le carton.",
        "narrateur|Nina se tait, ticket contre la poche.",
        "narrateur|Victorino parle à son oreille.",
        "enfant-m|Le loup, il va fermer l'œil.",
        "narrateur|Le carton ne bouge plus.",
        "papa|Le ticket a attendu, lui aussi.",
        "enfant-f|Il ferme l'œil.",
        "maman|Tes deux mains étaient prêtes.",
    ],
    (2, 2, 1): [
        "enfant-f|Un rond, sans le ticket.",
        "narrateur|Nina pose le carton, puis elle trace.",
        "narrateur|Un cercle clair montre la bouche.",
        "enfant-m|Le loup va sous la lune.",
        "narrateur|Le ticket reste à plat, loin du verre.",
        "papa|Le doigt a vu le mot.",
        "enfant-f|Sous la lune.",
        "maman|Le carton n'a plus sali.",
    ],
    (2, 2, 2): [
        "enfant-f|On souffle, ticket dans la poche.",
        "narrateur|Nina range le carton, puis ils soufflent.",
        "narrateur|La buée recule, puis s'arrête.",
        "enfant-m|Le loup va près de l'arbre.",
        "narrateur|Le ticket se tait contre le tissu.",
        "papa|Le souffle a parlé après.",
        "enfant-f|Près de l'arbre.",
        "maman|Personne n'a frotté trop tôt.",
    ],
    (2, 2, 3): [
        "enfant-f|Le loup, pas le carton.",
        "narrateur|Nina laisse le ticket, et montre le loup.",
        "narrateur|Victorino regarde le dessin, puis parle.",
        "enfant-m|Le loup va sans crier.",
        "narrateur|Le carton reste dans la poche, sage.",
        "papa|Le dessin a tenu le mot.",
        "enfant-f|Sans crier.",
        "maman|Le ticket a attendu sa porte.",
    ],
    (2, 3, 1): [
        "enfant-f|Un pas en arrière, ticket serré.",
        "narrateur|Nina recule, et le carton rentre.",
        "narrateur|Victorino reprend, face au bord.",
        "enfant-m|Le loup se fait tout petit.",
        "narrateur|Le ticket ne salue plus la rue.",
        "papa|Le pas a laissé le mot.",
        "enfant-f|Tout petit.",
        "maman|Le carton n'a pas appelé trop tôt.",
    ],
    (2, 3, 2): [
        "enfant-f|La page, le ticket au chaud.",
        "narrateur|Nina ouvre l'album, et le carton dort.",
        "narrateur|Victorino pose un doigt, puis parle.",
        "enfant-m|Le loup rentre dans sa grotte.",
        "narrateur|Le ticket reste plat, prêt pour plus tard.",
        "papa|La page a gardé le mot.",
        "enfant-f|Dans sa grotte.",
        "maman|Le carton aura sa porte.",
    ],
    (2, 3, 3): [
        "enfant-f|On compte le phare, ticket bas.",
        "narrateur|Nina baisse le carton, un, deux.",
        "narrateur|Le rond jaune n'est pas le bus.",
        "enfant-m|Le loup part avec le vent.",
        "narrateur|Le ticket n'a pas bougé.",
        "papa|Le compte a laissé sa phrase.",
        "enfant-f|Avec le vent.",
        "maman|Le carton attend le vrai bus.",
    ],
    (3, 1, 1): [
        "enfant-f|On attend, coussin plat.",
        "narrateur|Nina tient le gris, sans sauter.",
        "narrateur|La goutte finit, loin du tissu.",
        "enfant-m|Le loup, il va dormir.",
        "narrateur|Le coussin reste plat, sous le rouge.",
        "papa|Le tissu n'a pas parlé.",
        "enfant-f|Il va dormir.",
        "maman|Toi, tu n'as pas sauté.",
    ],
    (3, 1, 2): [
        "enfant-f|Le manteau sur le coussin.",
        "narrateur|Maman couvre le gris, et l'album.",
        "narrateur|La goutte frappe le manteau, molle.",
        "enfant-m|Le loup, il va se cacher.",
        "narrateur|Le coussin reste sec, au chaud.",
        "papa|On a entendu sous le tissu.",
        "enfant-f|Il se cache.",
        "maman|Le manteau a gardé le gris.",
    ],
    (3, 1, 3): [
        "enfant-f|Tout près, sur le coussin.",
        "narrateur|Nina se glisse, gris entre eux.",
        "narrateur|Victorino parle contre l'épaule.",
        "enfant-m|Le loup, il va fermer l'œil.",
        "narrateur|Le coussin ne gicle plus.",
        "papa|Le gris a fait un nid.",
        "enfant-f|Il ferme l'œil.",
        "maman|Vous étiez tout près.",
    ],
    (3, 2, 1): [
        "enfant-f|Le doigt, pas le coussin.",
        "narrateur|Nina pose le gris, puis elle trace.",
        "narrateur|Un rond clair montre la bouche.",
        "enfant-m|Le loup va sous la lune.",
        "narrateur|Le coussin reste sur les genoux.",
        "papa|Le doigt a vu le mot.",
        "enfant-f|Sous la lune.",
        "maman|Le tissu n'a plus poussé.",
    ],
    (3, 2, 2): [
        "enfant-f|On souffle, coussin sur les genoux.",
        "narrateur|Nina arrête d'essuyer, puis ils soufflent.",
        "narrateur|La buée recule d'un souffle.",
        "enfant-m|Le loup va près de l'arbre.",
        "narrateur|Le gris reste sage, à plat.",
        "papa|Le souffle a parlé après.",
        "enfant-f|Près de l'arbre.",
        "maman|Le coussin a cessé de frotter.",
    ],
    (3, 2, 3): [
        "enfant-f|Le loup, sur le dessin.",
        "narrateur|Nina pose le coussin, et montre le loup.",
        "narrateur|Victorino regarde, puis parle.",
        "enfant-m|Le loup va sans crier.",
        "narrateur|Le gris reste sous l'album, tiède.",
        "papa|Le dessin a tenu le mot.",
        "enfant-f|Sans crier.",
        "maman|Le tissu a laissé le loup.",
    ],
    (3, 3, 1): [
        "enfant-f|Un pas, coussin serré.",
        "narrateur|Nina recule, le gris contre elle.",
        "narrateur|Victorino reprend, face au bord.",
        "enfant-m|Le loup se fait tout petit.",
        "narrateur|Le coussin ne glisse plus.",
        "papa|Le pas a laissé le mot.",
        "enfant-f|Tout petit.",
        "maman|Le gris n'est pas allé trop loin.",
    ],
    (3, 3, 2): [
        "enfant-f|La page, coussin sous le rouge.",
        "narrateur|Nina garde l'album ouvert, gris dessous.",
        "narrateur|Victorino pose un doigt, puis parle.",
        "enfant-m|Le loup rentre dans sa grotte.",
        "narrateur|Le coussin tient la page, à plat.",
        "papa|La page a gardé le mot.",
        "enfant-f|Dans sa grotte.",
        "maman|Le gris a tenu le livre.",
    ],
    (3, 3, 3): [
        "enfant-f|On compte, coussin sur les genoux.",
        "narrateur|Nina compte le phare, un, deux.",
        "narrateur|Le gris ne glisse plus vers la rue.",
        "enfant-m|Le loup part avec le vent.",
        "narrateur|Le coussin reste, pendant le compte.",
        "papa|Le phare n'a pas coupé le mot.",
        "enfant-f|Avec le vent.",
        "maman|Le compte a laissé sa phrase.",
    ],
}

END_SONS = {1: "bus,goutte", 2: "bus,verre", 3: "bus,porte"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Nina tourne la dernière page.",
        "enfant-f|Le loup dort, enfin.",
        "papa|Le bus s'arrête, sans bruit.",
        "maman|On monte, l'album fermé.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Une goutte sèche sur le banc, derrière.",
    ],
    (1, 1, 2): [
        "narrateur|Sous le manteau, la dernière page s'ouvre.",
        "enfant-f|Il se cache, je vois.",
        "papa|Le bus ouvre sa porte, large.",
        "maman|On monte, le manteau sur le rouge.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Le manteau garde un rond mouillé, derrière.",
    ],
    (1, 1, 3): [
        "narrateur|Tout près, la dernière page s'ouvre.",
        "enfant-f|Il ferme l'œil, tout petit.",
        "papa|Le bus attend, moteur bas.",
        "maman|On monte, les deux têtes ensemble.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Le banc reste vide, luisant.",
    ],
    (1, 2, 1): [
        "narrateur|Dans le rond, la dernière page s'ouvre.",
        "enfant-f|Sous la lune, il est là.",
        "papa|Le bus clignote, tout près de l'abri.",
        "maman|On monte, l'album fermé.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Un rond clair reste sur la vitre.",
    ],
    (1, 2, 2): [
        "narrateur|Après le souffle, la dernière page s'ouvre.",
        "enfant-f|Près de l'arbre, il marche.",
        "papa|Le bus s'arrête, portes ouvertes.",
        "maman|On monte, l'album fermé.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|La buée revient, lente, derrière eux.",
    ],
    (1, 2, 3): [
        "narrateur|Sous le doigt, la dernière page s'ouvre.",
        "enfant-f|Sans crier, le loup rentre.",
        "papa|Le bus souffle, puis s'arrête.",
        "maman|On monte, le loup caché.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Le dessin reste au chaud, fermé.",
    ],
    (1, 3, 1): [
        "narrateur|Sans courir, la dernière page s'ouvre.",
        "enfant-f|Tout petit, il tient dans la page.",
        "papa|Le bus arrive, vrai cette fois.",
        "maman|On monte, sans se presser.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Le bord du trottoir reste vide.",
    ],
    (1, 3, 2): [
        "narrateur|La page ouverte se ferme, lente.",
        "enfant-f|Sa grotte est à la fin.",
        "papa|Le bus s'arrête, tout contre l'abri.",
        "maman|On monte, le rouge contre elle.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Le ticket passe près de la porte.",
    ],
    (1, 3, 3): [
        "narrateur|Sous le phare, la dernière page s'ouvre.",
        "enfant-f|Avec le vent, il part.",
        "papa|Le vrai bus s'arrête, enfin.",
        "maman|On monte, le phare tout près.",
        "narrateur|L'album rouge reste chaud, sur ses genoux.",
        "narrateur|Le rond jaune s'éteint, loin.",
    ],
    (2, 1, 1): [
        "narrateur|Nina tourne la page, ticket au chaud.",
        "enfant-f|Le loup dort, je l'ai entendu.",
        "papa|Le bus s'arrête : sortez le carton.",
        "maman|On monte, le ticket vers la fente.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|Le carton sent le bitume, au fond.",
    ],
    (2, 1, 2): [
        "narrateur|Sous le manteau, la page s'ouvre.",
        "enfant-f|Il se cache, sous le tissu.",
        "papa|Le bus ouvre : le carton, Nina.",
        "maman|On monte, manteau et ticket ensemble.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|Une goutte perle sur le carton, puis part.",
    ],
    (2, 1, 3): [
        "narrateur|Tout près, Nina tourne, carton serré.",
        "enfant-f|Il ferme l'œil, je l'ai.",
        "papa|Le bus attend : montrez le ticket.",
        "maman|On monte, oreille contre oreille.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|La poche garde le carton plat.",
    ],
    (2, 2, 1): [
        "narrateur|Dans le rond, la page s'ouvre.",
        "enfant-f|Sous la lune, sans le carton.",
        "papa|Le bus clignote : le ticket, maintenant.",
        "maman|On monte, le carton vers la fente.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|Le ticket a un bord un peu flou.",
    ],
    (2, 2, 2): [
        "narrateur|Après le souffle, Nina tourne.",
        "enfant-f|Près de l'arbre, c'est lui.",
        "papa|Le bus s'arrête : sortez le carton.",
        "maman|On monte, poches fermées d'abord.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|Un souffle a laissé un ovale sur le verre.",
    ],
    (2, 2, 3): [
        "narrateur|Sous le doigt, la page s'ouvre.",
        "enfant-f|Sans crier, comme le carton.",
        "papa|Le bus souffle : le ticket, Nina.",
        "maman|On monte, le loup caché, carton prêt.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|Le carton cache le loup, contre la vitre.",
    ],
    (2, 3, 1): [
        "narrateur|Sans courir, Nina tourne, carton bas.",
        "enfant-f|Tout petit, comme mon ticket.",
        "papa|Le vrai bus arrive : le carton.",
        "maman|On monte, un pas après l'autre.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|Le ticket touche la main du chauffeur.",
    ],
    (2, 3, 2): [
        "narrateur|La page se ferme, et le carton sort.",
        "enfant-f|Sa grotte, puis la porte.",
        "papa|Le bus s'arrête : fente, Nina.",
        "maman|On monte, rouge et carton ensemble.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|La poche claque contre la rampe.",
    ],
    (2, 3, 3): [
        "narrateur|Sous le phare, Nina tourne, carton bas.",
        "enfant-f|Avec le vent, et le ticket.",
        "papa|Le vrai bus s'arrête : le carton.",
        "maman|On monte, le phare sur le carton.",
        "narrateur|Le ticket carton dort dans la poche.",
        "narrateur|Le phare se reflète un moment sur le carton.",
    ],
    (3, 1, 1): [
        "narrateur|Nina tourne, coussin sous le rouge.",
        "enfant-f|Le loup dort, sur le gris.",
        "papa|Le bus s'arrête : prenez le coussin.",
        "maman|On monte, le gris sous le bras.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Le coussin laisse un carré sec sur le banc.",
    ],
    (3, 1, 2): [
        "narrateur|Sous le manteau, la page s'ouvre.",
        "enfant-f|Il se cache, sur le tissu.",
        "papa|Le bus ouvre : le coussin, Nina.",
        "maman|On monte, manteau et gris ensemble.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Le manteau et le tissu sentent la pluie.",
    ],
    (3, 1, 3): [
        "narrateur|Tout près, Nina tourne, gris entre eux.",
        "enfant-f|Il ferme l'œil, sur le nid.",
        "papa|Le bus attend : gardez le coussin.",
        "maman|On monte, épaule contre épaule.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Le coussin garde une goutte, au coin.",
    ],
    (3, 2, 1): [
        "narrateur|Dans le rond, la page s'ouvre.",
        "enfant-f|Sous la lune, sur le gris.",
        "papa|Le bus clignote : le coussin, avec vous.",
        "maman|On monte, le gris sous l'album.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Le tissu a un croissant de buée, pâle.",
    ],
    (3, 2, 2): [
        "narrateur|Après le souffle, Nina tourne.",
        "enfant-f|Près de l'arbre, coussin tiède.",
        "papa|Le bus s'arrête : le gris, Nina.",
        "maman|On monte, sans frotter la vitre.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Le coussin sent le verre froid, un peu.",
    ],
    (3, 2, 3): [
        "narrateur|Sous le doigt, la page s'ouvre.",
        "enfant-f|Sans crier, comme le tissu.",
        "papa|Le bus souffle : le coussin, sous le rouge.",
        "maman|On monte, le loup sur le gris.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Un loup de buée s'efface sur la vitre.",
    ],
    (3, 3, 1): [
        "narrateur|Sans courir, Nina tourne, gris serré.",
        "enfant-f|Tout petit, sur le coussin.",
        "papa|Le vrai bus arrive : le gris.",
        "maman|On monte, sans laisser glisser.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Le coussin rentre le dernier, derrière l'album.",
    ],
    (3, 3, 2): [
        "narrateur|La page se ferme, coussin dessous.",
        "enfant-f|Sa grotte tient sur le gris.",
        "papa|Le bus s'arrête : le rouge, et le tissu.",
        "maman|On monte, page et coussin collés.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Un fil du tissu s'accroche à la rampe.",
    ],
    (3, 3, 3): [
        "narrateur|Sous le phare, Nina tourne, gris à plat.",
        "enfant-f|Avec le vent, sur le coussin.",
        "papa|Le vrai bus s'arrête : le gris.",
        "maman|On monte, le phare sur le tissu.",
        "narrateur|Le petit coussin reste sous le rouge.",
        "narrateur|Le phare allume le gris du coussin, une seconde.",
    ],
}


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "gouttiere,flaque"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("l'album", "le ticket", "le coussin")},
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
                "narrateur|Le banc goutte trop fort.",
                "narrateur|La vitre a trop de buée.",
                "narrateur|Le bord voit le bus, trop loin.",
                "papa|Nina, tu vas où ?",
            ],
            "choice",
            "",
            {"fields": t3lab("le banc", "la vitre", "le bord")},
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
        "nora",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "au parc",
        "joue au salon",
        "tout doux",
        "tout calme",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")

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

    t3s = [c["text"] for c in story["chunks"] if c["chunk_id"].endswith("T0003_P0001") or c["chunk_id"].endswith("T0003_P0002") or c["chunk_id"].endswith("T0003_P0003")]
    t3s = [c["text"] for c in story["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-070 — L'album de Nina, à l'arrêt du bus\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.002 — laisser l'autre finir sa phrase (vécue)\n"
        "- **Personnages :** Nina, Victorino, papa, maman\n"
        "- **Lieu :** arrêt du bus du village : banc mouillé, abri de verre, bord du trottoir\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sous l'abri de verre, la gouttière tape. Nina veut finir la dernière page "
        "de l'album du loup **avant le bus**. Victorino commence : « Le loup, il va. » "
        "Nina coupe : « Manger ! » Le mot n'arrive pas. Première idée ratée. "
        "Elle prend l'album, le ticket ou le coussin ; le banc goutte, la vitre se voile "
        "ou un phare trompe ; une action change l'écoute (goutte, manteau, tout près ; "
        "doigt, souffle, loup ; pas, page, phare). Victorino finit. La page s'ouvre. On monte.\n\n"
        "## Vécu\n\n"
        "Nina veut la dernière page **maintenant**. Elle parle à la place de Victorino. "
        "Silence, mot perdu, page trop tôt. Chaque choix change l'obstacle et le climax. "
        "La leçon se voit : couper donne « manger » ; laisser finir donne dormir, "
        "se cacher, fermer l'œil, la lune, l'arbre, sans crier, tout petit, la grotte, le vent. "
        "Fin : dernière page + bus, image unique du chemin (goutte, buée, phare, carton, gris).\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan parc / Nora / bac / toboggan / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (banc essuyé). Question d'adulte. Un « en ce moment ».\n"
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
