#!/usr/bin/env python3
"""TREE-DIF-073 — F-NAR-019. La marguerite de Raphaël, à l'étal. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-073"
N1 = 10
TITLE = "La marguerite de Raphaël, à l'étal"
FIL = (
    "Sous la bâche de l'étal, Raphaël veut porter la marguerite jusqu'à Nina, "
    "dans le petit seau, avec le papier, avant que la bâche se rabatte. "
    "Il tend trop vite. Nina ne veut pas la même chose. "
    "Un point de cire guide. T1 = marguerite / petit seau / papier. "
    "T2 = roses / seaux / bâche. Neuf façons de tendre, d'entendre non, "
    "ou de prendre sa fleur."
)
CHARS = "Raphaël, Nina, papa, maman"
SETTING = "étal de fleurs du marché : seaux, tiges, abeille, bâche"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "point de cire",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_bâche_respire_et_Raphaël_tend_trop_vite; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la manière de tendre; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_objets_partent_avec_eux; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_tend_trop_vite_Nina_ne_prend_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=Nina_pose_sa_limite_il_veut_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_point_de_cire_et_le_refus_de_foncer; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_point_de_cire_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|La bâche de l'étal respire, large.",
    "narrateur|Elle se lève, puis retombe, lente.",
    "narrateur|Ça sent le zinc mouillé, et les tiges.",
    "papa|Les seaux gouttent sur la pierre.",
    "enfant-m|Une abeille marche sur le blanc.",
    "maman|Elle a posé un point de cire.",
    "narrateur|Le point de cire brille, ambré.",
    "copine|Je veux voir les roses, moi.",
    "narrateur|En ce moment, Raphaël prend une tige.",
    "enfant-m|La marguerite, pour toi, Nina.",
    "narrateur|Il la tend trop près, trop vite.",
    "narrateur|Nina recule, sans un mot.",
    "enfant-m|Elle n'a pas pris le blanc.",
    "papa|Tu as vu son pas, Raphaël ?",
    "maman|Merci, tu as baissé la tige.",
    "narrateur|Le sourire de Raphaël s'en va.",
]

T1_CHOICE = [
    "narrateur|Trois choses attendent, sous la bâche.",
    "narrateur|La marguerite, le petit seau, le papier.",
    "papa|Par quoi tu commences, Raphaël ?",
]

T1 = {
    1: {
        "lab": "la marguerite",
        "sons": "tige,abeille",
        "emphasis": "marguerite",
        "passage": [
            "narrateur|Raphaël prend d'abord la marguerite.",
            "enfant-m|Elle a un cœur jaune.",
            "maman|Tiens-la par la tige, bas.",
            "narrateur|Le point de cire tremble, ambré.",
            "papa|Le seau et le papier aussi.",
            "narrateur|Il tient les trois contre lui.",
            "enfant-m|Nina, je te la tends.",
            "narrateur|Il avance trop vite, trop près.",
            "copine|Attends.",
            "narrateur|Nina ne tend pas la main.",
            "enfant-m|Pourquoi tu ne la prends pas ?",
            "papa|Tu as vu sa main, Raphaël ?",
            "narrateur|Dans sa poitrine, ça se bouscule.",
        ],
        "question": [
            "narrateur|Raphaël tient la marguerite.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "marguerite",
            "accepted_examples": "marguerite | la marguerite | d'abord la marguerite | la fleur blanche | le blanc",
            "retry_prompt": "Raphaël a pris la marguerite.",
        },
        "confirm": [
            "enfant-m|La marguerite.",
            "maman|Oui.",
            "narrateur|Le cœur jaune reste un peu mouillé.",
            "narrateur|Le papier attend contre son poignet.",
            "enfant-m|Nina est devant l'étal.",
            "papa|Je la vois, plus près.",
            "maman|Vous allez lui proposer ça.",
            "enfant-m|Je lui tends la tige.",
            "narrateur|Le point de cire voyage avec lui.",
        ],
        "voy": "La marguerite penche vers Nina.",
    },
    2: {
        "lab": "le petit seau",
        "sons": "seau,eau",
        "emphasis": "petit seau",
        "passage": [
            "narrateur|Raphaël prend d'abord le petit seau.",
            "enfant-m|L'eau tremble un peu.",
            "papa|Pas trop plein, Raphaël.",
            "narrateur|Une goutte clabousse sur la pierre.",
            "maman|La marguerite et le papier aussi.",
            "narrateur|Il pose les trois près de Nina.",
            "enfant-m|Nina, je te tends ça.",
            "narrateur|Le seau penche trop, trop vite.",
            "copine|Mes pieds.",
            "narrateur|Nina recule, sans un mot.",
            "enfant-m|Le seau est pour la fleur.",
            "maman|Tu as vu ses pieds, Raphaël ?",
            "narrateur|Le sourire de Raphaël s'en va.",
        ],
        "question": [
            "narrateur|Le petit seau est dans ses mains.",
            "papa|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "seau",
            "accepted_examples": "seau | le seau | le petit seau | d'abord le seau | le zinc",
            "retry_prompt": "Raphaël a pris le petit seau.",
        },
        "confirm": [
            "enfant-m|Le seau.",
            "papa|Oui.",
            "narrateur|Une goutte pend au bord du zinc.",
            "narrateur|La marguerite voyage contre le seau.",
            "enfant-m|Nina est devant l'étal.",
            "maman|Je la vois, plus près.",
            "papa|Le seau tient bien, là.",
            "enfant-m|Je lui tends ça, après.",
            "narrateur|Le point de cire brille au zinc.",
        ],
        "voy": "Le petit seau penche vers Nina.",
    },
    3: {
        "lab": "le papier",
        "sons": "papier,pli",
        "emphasis": "papier",
        "passage": [
            "narrateur|Raphaël prend d'abord le papier.",
            "enfant-m|Il craque un peu.",
            "maman|Enroule-le sans trop serrer.",
            "narrateur|Le papier sent le bois, sec.",
            "papa|La marguerite et le seau aussi.",
            "narrateur|Il porte les trois sous la bâche.",
            "enfant-m|Nina, je t'enveloppe ça.",
            "narrateur|Il tend le pli trop vite.",
            "copine|Pas comme ça.",
            "narrateur|Nina croise les bras, un instant.",
            "enfant-m|C'est pour le blanc.",
            "papa|Tu as vu ses bras, Raphaël ?",
            "narrateur|Le papier reste ouvert, inutile.",
        ],
        "question": [
            "narrateur|Le papier craque contre son poignet.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "papier",
            "accepted_examples": "papier | le papier | d'abord le papier | l'enveloppe | le pli",
            "retry_prompt": "Raphaël a pris le papier.",
        },
        "confirm": [
            "enfant-m|Le papier.",
            "maman|Oui.",
            "narrateur|Un coin blanc dépasse, net.",
            "narrateur|La marguerite glisse dans le pli.",
            "enfant-m|Nina est devant l'étal.",
            "papa|Je la vois, plus près.",
            "maman|Le papier est prêt, là.",
            "enfant-m|Je l'enveloppe pour elle.",
            "narrateur|Le point de cire voyage au pli.",
        ],
        "voy": "Le papier penche vers Nina.",
    },
}

T2 = {
    (1, 1): {
        "sons": "epine,abeille",
        "emphasis": "épines",
        "passage": [
            "narrateur|La tige blanche reste un peu mouillée.",
            "narrateur|Une épine brille, trop près des roses.",
            "enfant-m|Nina, cette marguerite est pour toi.",
            "copine|Les épines, non.",
            "narrateur|Nina recule d'un pas.",
            "narrateur|Une abeille revient vers le point de cire.",
            "enfant-m|J'y vais, vite.",
            "narrateur|L'abeille barre la tige, un instant.",
            "narrateur|Le sourire de Raphaël s'en va.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Tu as vu son pas ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "eau,seau",
        "emphasis": "eau",
        "passage": [
            "narrateur|La marguerite penche au-dessus des seaux.",
            "narrateur|L'eau clabousse sur la pierre.",
            "enfant-m|Nina, je te tends la fleur.",
            "copine|Mes pieds, l'eau.",
            "narrateur|Une goutte saute sur sa chaussure.",
            "narrateur|Nina recule, les orteils mouillés.",
            "enfant-m|Je peux plus près.",
            "narrateur|Le seau du bord se renverse un peu.",
            "narrateur|Le sourire de Raphaël s'en va.",
            "papa|Ici, ça clabousse trop.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Tu as vu ses pieds ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "bache,tige",
        "emphasis": "bâche",
        "passage": [
            "narrateur|Sous la bâche, la marguerite penche.",
            "narrateur|L'ombre est fraîche, un peu grise.",
            "enfant-m|Nina, la marguerite est pour toi.",
            "copine|Une autre, plutôt.",
            "narrateur|Nina pointe une autre tige.",
            "narrateur|Elle ne dit rien de plus.",
            "enfant-m|Celle-là, c'est la plus belle.",
            "narrateur|Le point de cire brille, oublié.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "papa|Elle a choisi autre chose.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "maman|Tu as entendu sa voix ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "epine,zinc",
        "emphasis": "roses",
        "passage": [
            "narrateur|Le petit seau glisse trop près des roses.",
            "narrateur|Une épine racle le zinc, sèche.",
            "enfant-m|Nina, je te tends la fleur.",
            "copine|Les épines, non.",
            "narrateur|Nina recule, le seau trop proche.",
            "narrateur|L'eau tremble contre les tiges piquantes.",
            "enfant-m|Le seau va la protéger.",
            "narrateur|Une abeille revient vers le point de cire.",
            "narrateur|Le sourire de Raphaël s'en va.",
            "papa|Le seau ne coupe pas l'épine.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Tu as vu son pas ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "clabousse,zinc",
        "emphasis": "seaux",
        "passage": [
            "narrateur|Le petit seau heurte un seau du bord.",
            "narrateur|L'eau clabousse, trop haute.",
            "enfant-m|Nina, le seau est là.",
            "copine|Mes pieds, l'eau.",
            "narrateur|Une goutte saute sur sa chaussure.",
            "narrateur|Nina essuie, puis recule.",
            "enfant-m|Je verse moins, alors.",
            "narrateur|Il verse trop vite, trop fort.",
            "narrateur|Le zinc chante, trop plein.",
            "papa|Ici, ça clabousse trop.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "maman|Tu as vu ses pieds ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "bache,seau",
        "emphasis": "bâche",
        "passage": [
            "narrateur|Sous la bâche, le petit seau cloche.",
            "narrateur|L'ombre cache le cœur jaune.",
            "enfant-m|Nina, je te tends ça.",
            "copine|Une autre, plutôt.",
            "narrateur|Nina pointe une autre tige.",
            "narrateur|Le seau reste entre eux, inutile.",
            "enfant-m|Dans le seau, elle est belle.",
            "narrateur|Nina secoue la tête, sans un mot.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "papa|Elle a choisi autre chose.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Tu as entendu sa voix ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "papier,epine",
        "emphasis": "épines",
        "passage": [
            "narrateur|Le papier s'ouvre trop près des roses.",
            "narrateur|Une épine accroche le pli, nette.",
            "enfant-m|Nina, je t'enveloppe ça.",
            "copine|Les épines, non.",
            "narrateur|Nina recule d'un pas.",
            "narrateur|Le pli se déchire un peu, bas.",
            "enfant-m|Le papier va la cacher.",
            "narrateur|Une abeille revient vers le point de cire.",
            "narrateur|Le sourire de Raphaël s'en va.",
            "papa|Le papier n'arrête pas l'épine.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Tu as vu son pas ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "papier,eau",
        "emphasis": "eau",
        "passage": [
            "narrateur|Le papier passe au-dessus des seaux.",
            "narrateur|L'eau clabousse, et le pli mouille.",
            "enfant-m|Nina, le papier est prêt.",
            "copine|Mes pieds, l'eau.",
            "narrateur|Une goutte saute sur sa chaussure.",
            "narrateur|Nina recule, le papier trop mou.",
            "enfant-m|Je l'essuie, vite.",
            "narrateur|Il frotte trop fort, trop vite.",
            "narrateur|Le pli se déchire, mouillé.",
            "papa|Ici, ça clabousse trop.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "maman|Tu as vu ses pieds ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "bache,papier",
        "emphasis": "bâche",
        "passage": [
            "narrateur|Sous la bâche, le papier craque.",
            "narrateur|L'ombre rend le pli un peu gris.",
            "enfant-m|Nina, je t'enveloppe ça.",
            "copine|Une autre, plutôt.",
            "narrateur|Nina pointe une autre tige.",
            "narrateur|Le papier reste ouvert, trop tôt.",
            "enfant-m|Dans le papier, elle est à toi.",
            "narrateur|Nina ne dit rien.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "papa|Elle a choisi autre chose.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Tu as entendu sa voix ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
}

T3_LABS = {
    1: ("deux pas", "le bord", "la tulipe"),
    2: ("après l'eau", "le pas de côté", "le bleu"),
    3: ("sous la bâche", "l'autre tige", "le tournesol"),
}

T3_CHOICE = {
    1: [
        "narrateur|Les roses n'ont pas fini d'épiner.",
        "papa|Deux pas, le bord, ou la tulipe ?",
    ],
    2: [
        "narrateur|Les seaux n'ont pas fini de clabousser.",
        "maman|L'eau, le pas de côté, le bleu ?",
    ],
    3: [
        "narrateur|La bâche n'a pas fini son ombre.",
        "papa|Sous la bâche, l'autre tige, ou le tournesol ?",
    ],
}

T3_SONS = {
    (1, 1): "pas,silence",
    (1, 2): "bord,tige",
    (1, 3): "tulipe,papier",
    (2, 1): "eau,goutte",
    (2, 2): "pas,pierre",
    (2, 3): "bleu,tige",
    (3, 1): "bache,ombre",
    (3, 2): "tige,feuille",
    (3, 3): "tournesol,pollen",
}

T3_EMPH = {
    1: {1: "deux pas", 2: "bord", 3: "tulipe"},
    2: {1: "après l'eau", 2: "pas de côté", 3: "bleu"},
    3: {1: "sous la bâche", 2: "autre tige", 3: "tournesol"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|Deux pas, plus loin des épines.",
        "narrateur|Il recule, la marguerite tendue.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "copine|Là, je vois le blanc.",
        "enfant-m|Elle est pour toi, alors ?",
        "copine|Oui.",
        "papa|Tu as tendu de plus loin.",
        "maman|Elle a dit oui, toute seule.",
        "narrateur|Le point de cire reste, ambré.",
    ],
    (1, 1, 2): [
        "enfant-m|On reste au bord, d'accord.",
        "copine|Oui, loin des épines.",
        "narrateur|Il baisse la marguerite.",
        "narrateur|Le point de cire penche vers le sol.",
        "narrateur|Nina respire, les épaules plus basses.",
        "copine|Pas celle-là, Raphaël.",
        "enfant-m|D'accord.",
        "papa|Tu as gardé son recul.",
        "maman|Le bord n'a pas d'épines.",
        "narrateur|Personne n'a forcé la main.",
    ],
    (1, 1, 3): [
        "copine|La tulipe, plutôt.",
        "enfant-m|D'accord, la tulipe.",
        "narrateur|Il pose la marguerite.",
        "narrateur|Le point de cire reste sur le blanc.",
        "narrateur|La tulipe a une tige lisse.",
        "copine|Celle-là, oui.",
        "enfant-m|Je te la tends.",
        "papa|Tu as pris sa fleur.",
        "maman|La tulipe n'a pas d'épine, ici.",
        "narrateur|Il a écouté, sans foncer.",
    ],
    (1, 2, 1): [
        "enfant-m|Après l'eau, je te la tends.",
        "narrateur|La marguerite attend, sans bouger.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "narrateur|Le seau du bord se tait.",
        "copine|Mes pieds sont secs.",
        "enfant-m|La marguerite, alors ?",
        "copine|Oui.",
        "papa|Tu as tendu après l'eau.",
        "maman|Elle a dit oui, pieds secs.",
    ],
    (1, 2, 2): [
        "enfant-m|Un pas de côté, alors.",
        "copine|Oui, loin de l'eau.",
        "narrateur|Il ne tend plus, tout de suite.",
        "narrateur|Le point de cire penche, à l'écart.",
        "narrateur|Nina essuie sa chaussure.",
        "copine|Pas maintenant, Raphaël.",
        "enfant-m|D'accord.",
        "papa|Tu as gardé ses pieds secs.",
        "maman|Le pas de côté a suffi.",
        "narrateur|Personne n'a forcé la fleur.",
    ],
    (1, 2, 3): [
        "copine|Le bleu, là-bas.",
        "enfant-m|D'accord, le bleu.",
        "narrateur|Il pose la marguerite près du seau.",
        "narrateur|Le point de cire reste sur le blanc.",
        "narrateur|Une fleur bleue a la tige sèche.",
        "copine|Celle-là, loin de l'eau.",
        "enfant-m|Je te la tends.",
        "papa|Tu as pris sa fleur.",
        "maman|Le bleu n'a pas claboussé.",
        "narrateur|Il a écouté, sans foncer.",
    ],
    (1, 3, 1): [
        "enfant-m|Sous la bâche, une fois de plus.",
        "narrateur|Il tend la marguerite, à l'ombre.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "narrateur|Nina regarde le blanc, plus longtemps.",
        "copine|Là, le cœur jaune est doux.",
        "enfant-m|Elle est pour toi, alors ?",
        "copine|Oui.",
        "papa|Tu as tendu sous l'ombre.",
        "maman|Elle a dit oui, à l'ombre.",
    ],
    (1, 3, 2): [
        "copine|Une autre tige, Raphaël.",
        "enfant-m|D'accord, pas celle-là.",
        "narrateur|Il baisse la marguerite.",
        "narrateur|Le point de cire penche, oublié.",
        "narrateur|Nina cherche, sous la bâche.",
        "copine|Celle-ci, plus ronde.",
        "enfant-m|Je te la prends, alors.",
        "papa|Tu as entendu son autre voix.",
        "maman|L'autre tige était à elle.",
        "narrateur|Personne n'a forcé le blanc.",
    ],
    (1, 3, 3): [
        "copine|Le tournesol, plutôt.",
        "enfant-m|D'accord, le tournesol.",
        "narrateur|Il pose la marguerite.",
        "narrateur|Le point de cire reste sur le blanc.",
        "narrateur|Le tournesol chauffe un peu.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|Je te le tends.",
        "papa|Tu as pris sa fleur.",
        "maman|Le jaune tient dans sa main.",
        "narrateur|Il a écouté, sans foncer.",
    ],
    (2, 1, 1): [
        "enfant-m|Deux pas, le seau plus loin.",
        "narrateur|Il recule, le seau contre la hanche.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "copine|Là, je vois le blanc.",
        "enfant-m|Dans le seau, pour toi ?",
        "copine|Oui.",
        "papa|Tu as tendu de plus loin.",
        "maman|Elle a dit oui, toute seule.",
        "narrateur|Le zinc garde le point de cire.",
    ],
    (2, 1, 2): [
        "enfant-m|On reste au bord, seau bas.",
        "copine|Oui, loin des épines.",
        "narrateur|Il pose le seau au bord.",
        "narrateur|Le point de cire penche au zinc.",
        "narrateur|Nina respire, les épaules plus basses.",
        "copine|Pas celle-là, Raphaël.",
        "enfant-m|D'accord.",
        "papa|Tu as gardé son recul.",
        "maman|Le bord n'a pas d'épines.",
        "narrateur|Le seau n'a pas forcé.",
    ],
    (2, 1, 3): [
        "copine|La tulipe, plutôt.",
        "enfant-m|D'accord, la tulipe.",
        "narrateur|Il pose le seau.",
        "narrateur|Le point de cire reste au zinc.",
        "narrateur|La tulipe a une tige lisse.",
        "copine|Celle-là, oui.",
        "enfant-m|Je te la mets dans le seau.",
        "papa|Tu as pris sa fleur.",
        "maman|La tulipe n'a pas d'épine, ici.",
        "narrateur|Le seau porte sa tulipe.",
    ],
    (2, 2, 1): [
        "enfant-m|Après l'eau, je te tends le seau.",
        "narrateur|Le petit seau attend, sans bouger.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "narrateur|Le seau du bord se tait.",
        "copine|Mes pieds sont secs.",
        "enfant-m|La marguerite, alors ?",
        "copine|Oui.",
        "papa|Tu as tendu après l'eau.",
        "maman|Elle a dit oui, pieds secs.",
    ],
    (2, 2, 2): [
        "enfant-m|Un pas de côté, seau à l'écart.",
        "copine|Oui, loin de l'eau.",
        "narrateur|Le seau reste à l'écart.",
        "narrateur|Le point de cire penche, au zinc.",
        "narrateur|Nina essuie sa chaussure.",
        "copine|Pas maintenant, Raphaël.",
        "enfant-m|D'accord.",
        "papa|Tu as gardé ses pieds secs.",
        "maman|Le pas de côté a suffi.",
        "narrateur|Le seau n'a plus claboussé.",
    ],
    (2, 2, 3): [
        "copine|Le bleu, là-bas.",
        "enfant-m|D'accord, le bleu.",
        "narrateur|Il pose le petit seau plus loin.",
        "narrateur|Le point de cire reste au zinc.",
        "narrateur|Une fleur bleue a la tige sèche.",
        "copine|Celle-là, loin de l'eau.",
        "enfant-m|Je te la mets dans le seau.",
        "papa|Tu as pris sa fleur.",
        "maman|Le bleu n'a pas claboussé.",
        "narrateur|Le seau porte le bleu, sec.",
    ],
    (2, 3, 1): [
        "enfant-m|Sous la bâche, le seau à l'ombre.",
        "narrateur|Il tend le seau, à l'ombre.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "narrateur|Nina regarde le blanc, plus longtemps.",
        "copine|Là, le cœur jaune est doux.",
        "enfant-m|Dans le seau, pour toi ?",
        "copine|Oui.",
        "papa|Tu as tendu sous l'ombre.",
        "maman|Elle a dit oui, à l'ombre.",
    ],
    (2, 3, 2): [
        "copine|Une autre tige, Raphaël.",
        "enfant-m|D'accord, pas celle-là.",
        "narrateur|Il baisse le seau.",
        "narrateur|Le point de cire penche au zinc.",
        "narrateur|Nina cherche, sous la bâche.",
        "copine|Celle-ci, plus ronde.",
        "enfant-m|Je te la mets dans le seau.",
        "papa|Tu as entendu son autre voix.",
        "maman|L'autre tige était à elle.",
        "narrateur|Le seau n'a pas forcé le blanc.",
    ],
    (2, 3, 3): [
        "copine|Le tournesol, plutôt.",
        "enfant-m|D'accord, le tournesol.",
        "narrateur|Il pose le seau.",
        "narrateur|Le point de cire reste au zinc.",
        "narrateur|Le tournesol chauffe un peu.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|Je te le mets dans le seau.",
        "papa|Tu as pris sa fleur.",
        "maman|Le jaune tient dans sa main.",
        "narrateur|Le seau penche vers le grand jaune.",
    ],
    (3, 1, 1): [
        "enfant-m|Deux pas, le papier plus loin.",
        "narrateur|Il recule, le papier ouvert.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "copine|Là, je vois le blanc.",
        "enfant-m|Dans le papier, pour toi ?",
        "copine|Oui.",
        "papa|Tu as tendu de plus loin.",
        "maman|Elle a dit oui, toute seule.",
        "narrateur|Le pli garde le point de cire.",
    ],
    (3, 1, 2): [
        "enfant-m|On reste au bord, papier plié.",
        "copine|Oui, loin des épines.",
        "narrateur|Il plie le papier.",
        "narrateur|Le point de cire penche au pli.",
        "narrateur|Nina respire, les épaules plus basses.",
        "copine|Pas celle-là, Raphaël.",
        "enfant-m|D'accord.",
        "papa|Tu as gardé son recul.",
        "maman|Le bord n'a pas d'épines.",
        "narrateur|Le papier n'a pas forcé.",
    ],
    (3, 1, 3): [
        "copine|La tulipe, plutôt.",
        "enfant-m|D'accord, la tulipe.",
        "narrateur|Il pose le papier.",
        "narrateur|Le point de cire reste au pli.",
        "narrateur|La tulipe a une tige lisse.",
        "copine|Celle-là, oui.",
        "enfant-m|Je t'enveloppe la tulipe.",
        "papa|Tu as pris sa fleur.",
        "maman|La tulipe n'a pas d'épine, ici.",
        "narrateur|Le papier porte sa tulipe.",
    ],
    (3, 2, 1): [
        "enfant-m|Après l'eau, je t'enveloppe ça.",
        "narrateur|Le papier attend, sans bouger.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "narrateur|Le seau du bord se tait.",
        "copine|Mes pieds sont secs.",
        "enfant-m|La marguerite, alors ?",
        "copine|Oui.",
        "papa|Tu as tendu après l'eau.",
        "maman|Elle a dit oui, pieds secs.",
    ],
    (3, 2, 2): [
        "enfant-m|Un pas de côté, papier plié.",
        "copine|Oui, loin de l'eau.",
        "narrateur|Le papier reste plié.",
        "narrateur|Le point de cire penche au pli.",
        "narrateur|Nina essuie sa chaussure.",
        "copine|Pas maintenant, Raphaël.",
        "enfant-m|D'accord.",
        "papa|Tu as gardé ses pieds secs.",
        "maman|Le pas de côté a suffi.",
        "narrateur|Le papier n'a plus mouillé.",
    ],
    (3, 2, 3): [
        "copine|Le bleu, là-bas.",
        "enfant-m|D'accord, le bleu.",
        "narrateur|Il pose le papier près du zinc.",
        "narrateur|Le point de cire reste au pli.",
        "narrateur|Une fleur bleue a la tige sèche.",
        "copine|Celle-là, loin de l'eau.",
        "enfant-m|Je t'enveloppe le bleu.",
        "papa|Tu as pris sa fleur.",
        "maman|Le bleu n'a pas claboussé.",
        "narrateur|Le papier porte le bleu, sec.",
    ],
    (3, 3, 1): [
        "enfant-m|Sous la bâche, le papier à l'ombre.",
        "narrateur|Il tend le papier, à l'ombre.",
        "narrateur|Il regarde le point de cire.",
        "narrateur|Il refuse de foncer.",
        "narrateur|Nina regarde le blanc, plus longtemps.",
        "copine|Là, le cœur jaune est doux.",
        "enfant-m|Dans le papier, pour toi ?",
        "copine|Oui.",
        "papa|Tu as tendu sous l'ombre.",
        "maman|Elle a dit oui, à l'ombre.",
    ],
    (3, 3, 2): [
        "copine|Une autre tige, Raphaël.",
        "enfant-m|D'accord, pas celle-là.",
        "narrateur|Il baisse le papier.",
        "narrateur|Le point de cire penche au pli.",
        "narrateur|Nina cherche, sous la bâche.",
        "copine|Celle-ci, plus ronde.",
        "enfant-m|Je t'enveloppe celle-ci.",
        "papa|Tu as entendu son autre voix.",
        "maman|L'autre tige était à elle.",
        "narrateur|Le papier n'a pas forcé le blanc.",
    ],
    (3, 3, 3): [
        "copine|Le tournesol, plutôt.",
        "enfant-m|D'accord, le tournesol.",
        "narrateur|Il pose le papier.",
        "narrateur|Le point de cire reste au pli.",
        "narrateur|Le tournesol chauffe un peu.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|Je t'enveloppe le grand jaune.",
        "papa|Tu as pris sa fleur.",
        "maman|Le jaune tient dans sa main.",
        "narrateur|Le papier chauffe contre le jaune.",
    ],
}

END_SONS = {1: "abeille,pierre", 2: "eau,pas", 3: "bache,tige"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|La marguerite voyage, serrée dans sa main.",
        "copine|Le blanc est à moi.",
        "enfant-m|Deux pas, et tu as dit oui.",
        "papa|Les épines sont restées loin.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|Une abeille s'éloigne, lente.",
        "narrateur|Loin des roses, le point de cire tient.",
    ],
    (1, 1, 2): [
        "narrateur|Une petite tige sans épine, au bord.",
        "copine|Celle du bord, je la prends.",
        "enfant-m|Tu as dit non, d'abord.",
        "papa|Son recul a gardé sa place.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|Les épines restent loin, muettes.",
        "narrateur|Au bord de l'étal, le point de cire dort.",
    ],
    (1, 1, 3): [
        "narrateur|La tulipe rose dort dans sa main.",
        "copine|Elle n'a pas piqué.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|La tige lisse a suffi.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|Un pétale rose suit le pas, bas.",
        "narrateur|Sur la tulipe, le point de cire pâlit.",
    ],
    (1, 2, 1): [
        "narrateur|La marguerite voyage, serrée dans sa main.",
        "copine|Mes pieds sont secs.",
        "enfant-m|Après l'eau, tu as dit oui.",
        "papa|L'eau s'est tue, d'abord.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|Un seau du bord se tait, derrière.",
        "narrateur|Après l'eau, le point de cire sèche au soleil.",
    ],
    (1, 2, 2): [
        "narrateur|Une tige sèche reste dans sa main.",
        "copine|Loin de l'eau, celle-là.",
        "enfant-m|Tu as dit pas maintenant.",
        "papa|Ses pieds sont restés secs.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|La pierre de l'étal sèche, lente.",
        "narrateur|À l'écart, le point de cire penche, intact.",
    ],
    (1, 2, 3): [
        "narrateur|Le bleu reste contre sa paume chaude.",
        "copine|Il n'a pas claboussé.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|La tige sèche a suffi.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|Une goutte retombe, plus loin.",
        "narrateur|Sur le bleu, le point de cire reste sec.",
    ],
    (1, 3, 1): [
        "narrateur|La marguerite voyage, serrée dans sa main.",
        "copine|Sous la bâche, le blanc est doux.",
        "enfant-m|Tu as dit oui, à l'ombre.",
        "papa|L'ombre a laissé le temps.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|L'ombre de la bâche reste derrière.",
        "narrateur|Sous la bâche, le point de cire garde l'ombre.",
    ],
    (1, 3, 2): [
        "narrateur|La fleur ronde penche vers son pouce.",
        "copine|Celle-ci, plus ronde, c'est la mienne.",
        "enfant-m|Tu as choisi l'autre tige.",
        "papa|Sa voix a dit une autre.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|Un coin de bâche claque, loin.",
        "narrateur|Sur l'autre tige, le point de cire voyage.",
    ],
    (1, 3, 3): [
        "narrateur|Le tournesol penche vers son nez.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|Le jaune tient dans sa main.",
        "maman|On rentre, la fleur avec vous.",
        "narrateur|Un peu de pollen suit le pas.",
        "narrateur|Sur le tournesol, le point de cire chauffe.",
    ],
    (2, 1, 1): [
        "narrateur|Le petit seau voyage, tige au zinc.",
        "copine|Le blanc est à moi, dans l'eau.",
        "enfant-m|Deux pas, et tu as dit oui.",
        "papa|Les épines n'ont pas touché le seau.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|Une abeille s'éloigne du zinc.",
        "narrateur|Le seau garde le point de cire, loin.",
    ],
    (2, 1, 2): [
        "narrateur|Le petit seau reste au bord, vide de roses.",
        "copine|Celle du bord, dans le seau.",
        "enfant-m|Tu as dit non, d'abord.",
        "papa|Son recul a gardé le zinc.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|Les épines restent loin du zinc.",
        "narrateur|Le zinc tient le point de cire, au bord.",
    ],
    (2, 1, 3): [
        "narrateur|La tulipe penche dans le petit seau.",
        "copine|Elle n'a pas piqué le zinc.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|La tige lisse a suffi.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|Un pétale rose colle au zinc.",
        "narrateur|Dans le seau, le point de cire côtoie la tulipe.",
    ],
    (2, 2, 1): [
        "narrateur|Le petit seau voyage, eau basse.",
        "copine|Mes pieds sont secs, le seau aussi.",
        "enfant-m|Après l'eau, tu as dit oui.",
        "papa|L'eau s'est tue, d'abord.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|Un seau du bord se tait, derrière.",
        "narrateur|Le seau sèche, le point de cire aussi.",
    ],
    (2, 2, 2): [
        "narrateur|Le petit seau reste à l'écart, sage.",
        "copine|Loin de l'eau, celui-là.",
        "enfant-m|Tu as dit pas maintenant.",
        "papa|Ses pieds sont restés secs.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|La pierre de l'étal sèche, lente.",
        "narrateur|Le seau à l'écart, le point de cire intact.",
    ],
    (2, 2, 3): [
        "narrateur|Le bleu penche dans le petit seau.",
        "copine|Il n'a pas claboussé le zinc.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|La tige sèche a suffi.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|Une goutte retombe, plus loin.",
        "narrateur|Le seau porte le bleu, et le point de cire.",
    ],
    (2, 3, 1): [
        "narrateur|Le petit seau voyage, à l'ombre.",
        "copine|Sous la bâche, le blanc est doux.",
        "enfant-m|Tu as dit oui, à l'ombre.",
        "papa|L'ombre a laissé le temps.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|L'ombre de la bâche reste derrière.",
        "narrateur|Sous la bâche, le seau tient le point de cire.",
    ],
    (2, 3, 2): [
        "narrateur|La fleur ronde penche dans le seau.",
        "copine|Celle-ci, plus ronde, dans le zinc.",
        "enfant-m|Tu as choisi l'autre tige.",
        "papa|Sa voix a dit une autre.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|Un coin de bâche claque, loin.",
        "narrateur|Le seau suit l'autre tige, cire au zinc.",
    ],
    (2, 3, 3): [
        "narrateur|Le tournesol penche hors du seau.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|Le jaune tient dans sa main.",
        "maman|On rentre, le seau avec vous.",
        "narrateur|Un peu de pollen suit le zinc.",
        "narrateur|Le seau penche vers le tournesol, cire au bord.",
    ],
    (3, 1, 1): [
        "narrateur|Le papier voyage, tige au pli.",
        "copine|Le blanc est à moi, dans le papier.",
        "enfant-m|Deux pas, et tu as dit oui.",
        "papa|Les épines n'ont pas déchiré le pli.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|Une abeille s'éloigne du pli.",
        "narrateur|Le papier plie le point de cire, loin des roses.",
    ],
    (3, 1, 2): [
        "narrateur|Le papier reste au bord, plié.",
        "copine|Celle du bord, dans le papier.",
        "enfant-m|Tu as dit non, d'abord.",
        "papa|Son recul a gardé le pli.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|Les épines restent loin du papier.",
        "narrateur|Au bord, le papier garde le point de cire.",
    ],
    (3, 1, 3): [
        "narrateur|La tulipe dort dans le papier.",
        "copine|Elle n'a pas piqué le pli.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|La tige lisse a suffi.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|Un pétale rose suit le pli, bas.",
        "narrateur|Le papier enveloppe la tulipe, cire au pli.",
    ],
    (3, 2, 1): [
        "narrateur|Le papier voyage, un peu sec.",
        "copine|Mes pieds sont secs, le pli aussi.",
        "enfant-m|Après l'eau, tu as dit oui.",
        "papa|L'eau s'est tue, d'abord.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|Un seau du bord se tait, derrière.",
        "narrateur|Le papier sèche, le point de cire au coin.",
    ],
    (3, 2, 2): [
        "narrateur|Le papier reste à l'écart, plié.",
        "copine|Loin de l'eau, celui-là.",
        "enfant-m|Tu as dit pas maintenant.",
        "papa|Ses pieds sont restés secs.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|La pierre de l'étal sèche, lente.",
        "narrateur|Le papier à l'écart, cire au pli.",
    ],
    (3, 2, 3): [
        "narrateur|Le bleu dort dans le papier.",
        "copine|Il n'a pas claboussé le pli.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|La tige sèche a suffi.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|Une goutte retombe, plus loin.",
        "narrateur|Le papier porte le bleu, cire au coin.",
    ],
    (3, 3, 1): [
        "narrateur|Le papier voyage, à l'ombre.",
        "copine|Sous la bâche, le blanc est doux.",
        "enfant-m|Tu as dit oui, à l'ombre.",
        "papa|L'ombre a laissé le temps.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|L'ombre de la bâche reste derrière.",
        "narrateur|Sous la bâche, le papier tient le point de cire.",
    ],
    (3, 3, 2): [
        "narrateur|La fleur ronde penche dans le pli.",
        "copine|Celle-ci, plus ronde, dans le papier.",
        "enfant-m|Tu as choisi l'autre tige.",
        "papa|Sa voix a dit une autre.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|Un coin de bâche claque, loin.",
        "narrateur|Le papier suit l'autre tige, cire au pli.",
    ],
    (3, 3, 3): [
        "narrateur|Le tournesol dépasse du papier.",
        "copine|Il est trop grand, j'aime.",
        "enfant-m|C'était ta fleur, Nina.",
        "papa|Le jaune tient dans sa main.",
        "maman|On rentre, le papier avec vous.",
        "narrateur|Un peu de pollen suit le pli.",
        "narrateur|Le papier chauffe contre le tournesol, cire au coin.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "bache,abeille,seaux"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("la marguerite", "le petit seau", "le papier")},
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
                "narrateur|Près des roses, une épine brille.",
                "narrateur|Au bord, les seaux claboussent.",
                "narrateur|Sous la bâche, l'ombre est fraîche.",
                "papa|On va vers où, Raphaël ?",
            ],
            "choice",
            "",
            {"fields": t3lab("les roses", "les seaux", "la bâche")},
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
        "inviter sans forcer",
        "j'ai compris",
        "mission accomplie",
        "il faut attendre",
        "léa",
        "lea ",
        "kenzo",
        "sami",
        "tom ",
        "iris",
        "lina",
        "zoé",
        "zoe",
        "aniss",
        "moulinet",
        "le four",
        "wagon",
        "la mer",
        "la serre",
        "arrosoir",
        "le tapis",
        "poisson",
        "canapé",
        "le store",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
        "capitaine",
        "plic",
        "volet jaune",
        "fort de coussins",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "aujourd'hui",
        "nœud de raphia",
        "oeillet",
        "œillet",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob or "nina" not in blob:
        raise SystemExit(f"{SID}: troupe Raphaël/Nina absente")
    if "point de cire" not in blob:
        raise SystemExit(f"{SID}: indice point de cire absent")
    if "abeille" not in blob or "bâche" not in blob:
        raise SystemExit(f"{SID}: étal/abeille/bâche absents")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    if aj.count("merci") + aj.count("bravo") != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{aj.count('merci') + aj.count('bravo')}")

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

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-073 — La marguerite de Raphaël, à l'étal\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter sans forcer (vécue : proposer, accepter oui / non / plus tard)\n"
        "- **Personnages :** Raphaël, Nina, papa, maman\n"
        "- **Lieu :** étal de fleurs du marché : seaux, tiges, abeille, bâche\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La bâche de l'étal respire. Ça sent le zinc et les tiges. Une abeille pose "
        "un **point de cire** ambré sur le blanc. Raphaël veut porter la marguerite "
        "jusqu'à Nina, dans le petit seau, avec le papier, **avant que la bâche se rabatte**. "
        "Il tend trop vite. Nina veut les roses, pas la même chose au même moment. "
        "Première idée ratée. Il prend la marguerite, le petit seau ou le papier ; "
        "les trois viennent. Roses (épines), seaux (eau), bâche (autre tige). "
        "Il refuse de foncer, retrouve le point de cire. Deux pas, le bord, la tulipe ; "
        "après l'eau, le pas de côté, le bleu ; sous la bâche, l'autre tige, le tournesol. "
        "Une fleur dans une main. On rentre.\n\n"
        "## Vécu\n\n"
        "Raphaël propose **maintenant**. Nina prend son temps, ou pose sa limite. "
        "Silence = réponse. Le sourire disparaît ; envie et inquiétude se bousculent. "
        "Papa ou maman s'accroupit à la même hauteur. Personne ne donne la réponse. "
        "Raphaël observe l'objet, écoute l'étal, retrouve le point de cire. "
        "La leçon se voit : il tend, il entend non, il prend sa fleur. "
        "Le dénouement a failli ne pas arriver. Le point de cire paie l'ouverture.\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Inviter sans forcer » / Léa / merle / miel / tics jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Monde ≠ TREE-COL-012 (pas Aniss, pas pliage de bâche) : ici étal de fleurs, marguerite, abeille.\n"
        "- Monde ≠ TREE-DIF-031 (pas potager, pas nœud de raphia).\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'obstacle. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : le point de cire, payé au climax.\n"
        "- Merci vécu (maman : tu as baissé la tige). Question d'adulte. Un « en ce moment ».\n"
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
