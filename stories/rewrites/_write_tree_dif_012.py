#!/usr/bin/env python3
"""TREE-DIF-012 — F-NAR-019. Pomme verte, pieds d'Amir. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-012"
N1 = 10
TITLE = "La pomme verte et les pieds d'Amir"
FIL = (
    "Sous le pommier, Amir veut la pomme verte qui tremble tout en haut. "
    "Ses pieds dansent. Il saute : sa main frotte l'air. "
    "T1 = bac / toboggan / balançoires. "
    "T2 = caisse / arrosoir / chapeau : l'objet penche tant que les pieds tapent. "
    "T3 = papa porte, pieds arrêtés, ou la famille pousse. "
    "Amir croque. Le jus sucré tient la promesse."
)
CHARS = "Amir, papa, maman"
SETTING = "le jardin, sous le pommier"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "pomme verte",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_pomme_attend_les_pieds_dansent; tempo=naturel; sourire=léger; respiration=ample",
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
        "emphasis": "pomme",
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_veut; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "pomme verte",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=sauter_ne_suffit_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_objet_penche_tant_que_les_pieds_tapent; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=demander_attendre_ou_pousser_ensemble; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "jus",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_jus_tient_la_promesse_du_début; tempo=posé; sourire=léger; respiration=ample",
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


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


OPENING = [
    "narrateur|Au fond du jardin, le pommier chauffe.",
    "narrateur|L'écorce est rêche, un peu tiède.",
    "narrateur|Une fourmi grimpe, sans se presser.",
    "narrateur|Tout en haut, une pomme verte attend.",
    "narrateur|Une feuille y reste collée, et tremble.",
    "narrateur|Ça sent le jus écrasé, sous l'arbre.",
    "narrateur|Au clou, un chapeau de paille pend.",
    "narrateur|Près du tronc, une caisse sent le sucré.",
    "papa|Tu as ramené l'arrosoir, merci.",
    "enfant-m|Il gouttait sur la mousse.",
    "maman|Tu sens la pomme, Amir ?",
    "enfant-m|Elle est sucrée, celle-là.",
    "narrateur|En ce moment, Amir tape des pieds.",
    "narrateur|Toc, toc, sur l'herbe sèche.",
    "enfant-m|Je la veux, la verte !",
    "narrateur|Il saute, et sa main frotte l'air.",
    "narrateur|La pomme reste, trop haute.",
    "maman|Tes pieds dansent, trop forts ?",
    "enfant-m|Ils vont l'attraper.",
    "papa|On te suit, sous l'arbre.",
]

T1_CHOICE = [
    "narrateur|Sous les feuilles, trois coins attendent.",
    "narrateur|Le bac, le toboggan, les balançoires.",
    "papa|Tu cours où, d'abord ?",
]

T1 = {
    1: {
        "lab": "le bac à sable",
        "sons": "sable,oiseau",
        "emphasis": "sable",
        "passage": [
            "narrateur|Amir court vers le bac à sable.",
            "narrateur|Le sable est tiède, un peu rêche.",
            "enfant-m|L'ombre de la pomme est ici !",
            "narrateur|Il saute, et un nuage s'élève.",
            "narrateur|Un grain colle à son genou.",
            "enfant-m|Attends, je viens !",
            "narrateur|Sa main n'arrive pas.",
            "maman|Tes pieds dansent, trop forts.",
            "papa|La pomme, elle, reste sage.",
            "enfant-m|Je la veux quand même.",
            "narrateur|La feuille collée tremble, là-haut.",
            "maman|On la cherche d'ici, alors ?",
        ],
        "question": [
            "narrateur|Amir saute sous l'ombre ronde.",
            "maman|Il saute vers quoi ?",
        ],
        "qfields": {
            "expected_answer": "pomme",
            "accepted_examples": "pomme | la pomme | pomme verte | la verte | une pomme",
            "retry_prompt": "Amir veut la pomme verte. Il veut quoi ?",
        },
        "confirm": [
            "narrateur|Oui, la pomme verte, tout en haut.",
            "enfant-m|Mes pieds n'y arrivent pas.",
            "papa|Une affaire du jardin, peut-être ?",
            "maman|La caisse, l'arrosoir, ou le chapeau.",
            "enfant-m|Pour l'atteindre.",
            "narrateur|Un grain de sable reste au genou.",
        ],
    },
    2: {
        "lab": "le toboggan",
        "sons": "metal,pas",
        "emphasis": "toboggan",
        "passage": [
            "narrateur|Amir court vers le toboggan.",
            "narrateur|Le métal est chaud, un peu lisse.",
            "enfant-m|Plus haut, je l'attrape !",
            "narrateur|Il grimpe les marches, trop vite.",
            "narrateur|Ses pieds tapent, toc toc.",
            "papa|Doucement, les marches sont chaudes.",
            "narrateur|Du haut, la pomme paraît plus près.",
            "enfant-m|Presque !",
            "narrateur|Sa main frotte l'air, rien.",
            "maman|Tes pieds veulent sauter, trop forts.",
            "enfant-m|Je la veux, celle-là.",
            "papa|On reste un moment, ici ?",
        ],
        "question": [
            "narrateur|Du haut, Amir tend la main.",
            "maman|Il tend la main vers quoi ?",
        ],
        "qfields": {
            "expected_answer": "pomme",
            "accepted_examples": "pomme | la pomme | pomme verte | la verte | une pomme",
            "retry_prompt": "Du haut, Amir veut la pomme. Il veut quoi ?",
        },
        "confirm": [
            "narrateur|Oui, c'est la pomme, tout en haut.",
            "enfant-m|Du haut, ma main est trop courte.",
            "maman|On prend une affaire, alors ?",
            "papa|La caisse, l'arrosoir, ou le chapeau.",
            "enfant-m|Oui, pour elle.",
            "narrateur|Le métal garde un toc, trop chaud.",
        ],
    },
    3: {
        "lab": "les balançoires",
        "sons": "chaine,herbe",
        "emphasis": "chaîne",
        "passage": [
            "narrateur|Amir court vers les balançoires.",
            "narrateur|La chaîne est froide, un peu rêche.",
            "enfant-m|Elle est juste au-dessus !",
            "narrateur|Il s'assoit, et ses pieds partent.",
            "narrateur|La chaîne chante un petit cri.",
            "maman|Tes pieds font voler le siège.",
            "papa|La pomme danse avec toi, là-haut.",
            "enfant-m|Je l'attrape en l'air !",
            "narrateur|Sa main claque le vide, tout près.",
            "narrateur|La pomme revient, trop haute.",
            "enfant-m|Une autre fois !",
            "papa|On cherche un autre geste ?",
        ],
        "question": [
            "narrateur|Amir lève le nez, sous la chaîne.",
            "maman|Il veut quoi, tout en haut ?",
        ],
        "qfields": {
            "expected_answer": "pomme",
            "accepted_examples": "pomme | la pomme | pomme verte | la verte | une pomme",
            "retry_prompt": "Sous la chaîne, c'est la pomme. Il veut quoi ?",
        },
        "confirm": [
            "narrateur|Oui, la pomme, au-dessus de la chaîne.",
            "enfant-m|Mes pieds volent, mais pas assez.",
            "papa|Une affaire du jardin, avec nous ?",
            "maman|La caisse, l'arrosoir, ou le chapeau.",
            "enfant-m|Je choisis.",
            "narrateur|La chaîne se balance, puis ralentit.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le bac n'atteint pas la pomme.",
        "narrateur|La caisse sent le jus, collée de grains.",
        "narrateur|L'arrosoir goutte, une flaque ronde.",
        "narrateur|Le chapeau attend, plein d'ombre.",
        "papa|Tu prends quoi, pour l'atteindre ?",
    ],
    2: [
        "narrateur|Le toboggan n'atteint pas la pomme.",
        "narrateur|La caisse sonnerait sur la marche.",
        "narrateur|L'arrosoir attend en bas, le bec ouvert.",
        "narrateur|Le chapeau ferait un nid, au pied.",
        "papa|Tu prends quoi, pour l'atteindre ?",
    ],
    3: [
        "narrateur|La balançoire n'atteint pas la pomme.",
        "narrateur|La caisse tiendrait sous le siège.",
        "narrateur|L'arrosoir irait sur les genoux.",
        "narrateur|Le chapeau irait sur l'autre siège.",
        "papa|Tu prends quoi, pour l'atteindre ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "bois,sable",
        "emphasis": "caisse",
        "passage": [
            "narrateur|Amir tire la caisse sur le sable.",
            "enfant-m|Je monte, et je l'ai !",
            "narrateur|Il grimpe, et ses pieds dansent.",
            "narrateur|La caisse s'enfonce, tout mou.",
            "papa|Elle penche, avec tes pieds.",
            "enfant-m|Attends, pomme !",
            "narrateur|Sa main frôle la feuille collée.",
            "maman|Le sable mange la caisse, un peu.",
            "narrateur|La pomme reste, trop haute.",
            "enfant-m|Elle est trop loin.",
            "papa|On fait comment, avec la caisse ?",
        ],
    },
    (1, 2): {
        "sons": "eau,sable",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|Amir pose l'arrosoir sur le sable.",
            "enfant-m|Je monte dessus, tout petit.",
            "narrateur|Ses pieds tapent le métal, toc.",
            "narrateur|L'eau saute, une flaque ronde.",
            "maman|Tes pieds ont donné un coup.",
            "papa|L'arrosoir a glissé, tout seul.",
            "enfant-m|La pomme, elle, n'a pas bougé.",
            "narrateur|Une goutte brille sur le grain.",
            "narrateur|La feuille collée tremble à peine.",
            "enfant-m|Il est trop petit, l'arrosoir.",
            "papa|On le tient comment, alors ?",
        ],
    },
    (1, 3): {
        "sons": "paille,sable",
        "emphasis": "chapeau",
        "passage": [
            "narrateur|Amir pose le chapeau sur le sable.",
            "enfant-m|Tombe dedans, pomme verte !",
            "narrateur|Il saute autour, pieds trop vifs.",
            "narrateur|Le chapeau se remplit de sable.",
            "maman|C'est un nid, mais plein de grains.",
            "papa|La pomme n'a pas vu le nid.",
            "enfant-m|Je saute plus fort !",
            "narrateur|La branche tremble, puis s'arrête.",
            "narrateur|Le chapeau reste vide, tout sablé.",
            "enfant-m|Elle n'est pas venue.",
            "maman|On l'aide, cette pomme ?",
        ],
    },
    (2, 1): {
        "sons": "bois,metal",
        "emphasis": "caisse",
        "passage": [
            "narrateur|Amir hisse la caisse en haut.",
            "enfant-m|Plus haut, maintenant !",
            "narrateur|Il pose un pied, puis l'autre.",
            "narrateur|Le métal sonne sous le bois.",
            "papa|La caisse penche, sur la marche.",
            "enfant-m|Je l'ai presque !",
            "narrateur|Ses pieds dansent, et ça vacille.",
            "maman|Tiens le bord, Amir.",
            "narrateur|Sa main manque la pomme, trop courte.",
            "enfant-m|Elle rit, là-haut.",
            "papa|On la reprend comment, la caisse ?",
        ],
    },
    (2, 2): {
        "sons": "eau,metal",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|Amir pose l'arrosoir en bas.",
            "enfant-m|Si elle tombe, je l'attrape !",
            "narrateur|Il glisse, pieds trop vite.",
            "narrateur|Toc, contre le bec de l'arrosoir.",
            "maman|L'eau a fait une ligne brillante.",
            "papa|Tes pieds l'ont rencontré, trop fort.",
            "enfant-m|Je voulais juste l'attendre.",
            "narrateur|La pomme n'est pas tombée.",
            "narrateur|L'arrosoir roule d'un pouce, puis s'arrête.",
            "enfant-m|Il n'est plus sous elle.",
            "papa|On le remet, sans taper ?",
        ],
    },
    (2, 3): {
        "sons": "paille,metal",
        "emphasis": "chapeau",
        "passage": [
            "narrateur|Amir pose le chapeau en bas.",
            "enfant-m|Un nid, pour quand elle vient !",
            "narrateur|Il regarde du haut, pieds impatients.",
            "narrateur|Le chapeau attend, tout plat.",
            "maman|Tes pieds veulent redescendre, trop vite.",
            "papa|La pomme, elle, n'a pas bougé.",
            "enfant-m|Je saute dans le nid !",
            "narrateur|Il s'arrête au bord, un souffle.",
            "narrateur|Le chapeau reste vide, en bas.",
            "enfant-m|Elle ne veut pas tomber.",
            "maman|On l'invite, autrement ?",
        ],
    },
    (3, 1): {
        "sons": "bois,chaine",
        "emphasis": "caisse",
        "passage": [
            "narrateur|Amir glisse la caisse sous le siège.",
            "enfant-m|Je monte, puis je m'envole !",
            "narrateur|Il se hausse, et ses pieds tapent.",
            "narrateur|La caisse recule d'un cran, dans l'herbe.",
            "papa|Elle part, avec tes pieds.",
            "enfant-m|Reviens, caisse !",
            "narrateur|La chaîne chante, et la pomme danse.",
            "maman|Le siège va, la caisse non.",
            "narrateur|Sa main manque la feuille, trop loin.",
            "enfant-m|C'est trop loin.",
            "papa|On tient la caisse, comment ?",
        ],
    },
    (3, 2): {
        "sons": "eau,chaine",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|Amir pose l'arrosoir sur ses genoux.",
            "enfant-m|Je l'attrape en volant !",
            "narrateur|Il se balance, et l'eau gicle.",
            "narrateur|Une goutte mouille son genou.",
            "maman|Tes pieds donnent trop d'élan.",
            "papa|L'arrosoir n'aime pas le vent.",
            "enfant-m|La pomme, elle, se balance aussi.",
            "narrateur|Ils dansent ensemble, trop loin.",
            "narrateur|Le bec reste vide, tout creux.",
            "enfant-m|Elle n'est pas rentrée.",
            "papa|On arrête les pieds, un peu ?",
        ],
    },
    (3, 3): {
        "sons": "paille,chaine",
        "emphasis": "chapeau",
        "passage": [
            "narrateur|Amir pose le chapeau sur l'autre siège.",
            "enfant-m|Toi tu attends, chapeau !",
            "narrateur|Il se balance vers la pomme.",
            "narrateur|Ses pieds volent, tout contents.",
            "maman|Le chapeau, lui, reste sage.",
            "papa|La pomme passe au-dessus, trop haute.",
            "enfant-m|Viens, viens !",
            "narrateur|Sa main claque l'air, tout près.",
            "narrateur|Le chapeau attend, vide et plat.",
            "enfant-m|Elle n'a pas voulu.",
            "maman|On l'aide à descendre ?",
        ],
    },
}

T3_LABS = {
    1: ("les bras de papa", "mes pieds sages", "on pousse"),
    2: ("les bras de papa", "j'attends", "maman penche"),
    3: ("papa secoue", "un petit vent", "maman incline"),
}

T3_CHOICE = {
    1: [
        "narrateur|La caisse n'a pas suffi, toute seule.",
        "papa|Mes bras, tes pieds sages, ou on pousse ?",
    ],
    2: [
        "narrateur|L'arrosoir n'a pas cueilli la pomme.",
        "maman|Papa te porte, tu attends, ou je penche ?",
    ],
    3: [
        "narrateur|Le chapeau attend, tout vide.",
        "papa|Je secoue, un vent, ou maman incline ?",
    ],
}

T3_SONS = {
    (1, 1): "bras,bois",
    (1, 2): "silence,bois",
    (1, 3): "pas,bois",
    (2, 1): "bras,eau",
    (2, 2): "vent,eau",
    (2, 3): "branche,eau",
    (3, 1): "branche,paille",
    (3, 2): "vent,paille",
    (3, 3): "branche,paille",
}

T3_EMPH = {
    1: {1: "bras", 2: "pieds", 3: "caisse"},
    2: {1: "arrosoir", 2: "vent", 3: "branche"},
    3: {1: "chapeau", 2: "vent", 3: "nid"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|Papa, porte-moi un peu.",
        "papa|Je te tiens, Amir.",
        "narrateur|Papa cale la caisse dans le sable.",
        "narrateur|Amir se hausse, pieds arrêtés.",
        "narrateur|Sa main touche la pomme verte.",
        "enfant-m|Elle est à moi !",
        "narrateur|La feuille collée vient avec.",
        "maman|Tu l'as cueillie, sans sauter.",
        "narrateur|Le sable tiède colle aux mollets.",
    ],
    (1, 1, 2): [
        "enfant-m|Mes pieds, restez sages.",
        "narrateur|Il attend, et les pieds s'arrêtent.",
        "narrateur|Le sable cesse de manger la caisse.",
        "narrateur|La caisse ne penche plus.",
        "enfant-m|Un geste, tout seul.",
        "narrateur|Il se hausse, lentement.",
        "narrateur|La pomme vient dans sa paume.",
        "papa|Tes pieds ont attendu, cette fois.",
        "maman|Elle est verte, et à toi.",
    ],
    (1, 1, 3): [
        "enfant-m|On pousse, tous les trois !",
        "narrateur|Ils poussent la caisse sous l'ombre.",
        "maman|J'incline la branche, un peu.",
        "narrateur|La pomme descend, lente.",
        "enfant-m|Dans la caisse !",
        "narrateur|Ploc, un jus mince sur le bois.",
        "papa|Vous l'avez faite venir.",
        "narrateur|Le sable tiède colle aux talons.",
        "narrateur|La feuille collée brille, au fond.",
    ],
    (1, 2, 1): [
        "enfant-m|Papa, plus haut, s'il te plaît.",
        "papa|Je te porte, tiens l'arrosoir.",
        "narrateur|Papa soulève Amir au-dessus du bac.",
        "narrateur|Amir cueille, et la pomme glisse au bec.",
        "enfant-m|Elle est dedans !",
        "narrateur|Une goutte d'eau la lave, tout petit.",
        "maman|Tes pieds pendent, sans taper.",
        "narrateur|Le sable tiède colle aux chevilles.",
        "narrateur|Une goutte reste sur le vert.",
    ],
    (1, 2, 2): [
        "enfant-m|J'attends, pieds sages.",
        "narrateur|Il pose l'arrosoir juste dessous.",
        "narrateur|Le sable ne vole plus.",
        "maman|On laisse le vent travailler.",
        "narrateur|La feuille tremble, puis s'en va.",
        "narrateur|La pomme lâche, sans bruit.",
        "enfant-m|Ploc !",
        "papa|Elle est venue vers le bec.",
        "narrateur|Le sable tiède colle aux orteils.",
    ],
    (1, 2, 3): [
        "maman|Je penche la branche, vers toi.",
        "narrateur|Amir tient l'arrosoir, pieds dans le sable.",
        "enfant-m|Je ne tape plus.",
        "narrateur|La pomme glisse le long des feuilles.",
        "narrateur|Elle rentre dans le bec, ploc.",
        "papa|Tu l'as gardé droit, l'arrosoir.",
        "enfant-m|Elle est à nous !",
        "narrateur|Une goutte reste sur le vert.",
        "narrateur|Le grain de sable brille, à côté.",
    ],
    (1, 3, 1): [
        "enfant-m|Papa, secoue un peu.",
        "papa|Sans la meurtrir, Amir.",
        "narrateur|Le chapeau attend dans le sable.",
        "narrateur|La branche ondule, une fois.",
        "narrateur|La pomme tombe dans la paille.",
        "enfant-m|Dans le nid !",
        "maman|Tu as bien visé le chapeau.",
        "narrateur|Le sable tiède colle aux genoux.",
        "narrateur|La feuille collée couvre le nid.",
    ],
    (1, 3, 2): [
        "enfant-m|On attend le petit vent.",
        "maman|Pieds sages, alors.",
        "narrateur|Amir se tait, le chapeau aussi.",
        "narrateur|Un grain de sable s'envole, puis rien.",
        "narrateur|Un souffle passe dans les feuilles.",
        "narrateur|La pomme se détache, lente.",
        "enfant-m|Elle vient !",
        "papa|Dans le chapeau, pile.",
        "narrateur|La paille sent le sucré, au bac.",
    ],
    (1, 3, 3): [
        "maman|J'incline la branche, vers le nid.",
        "narrateur|Le chapeau reste au creux du bac.",
        "enfant-m|Je ne saute plus.",
        "narrateur|La pomme glisse, puis se pose.",
        "papa|Dans le chapeau, tout au fond.",
        "enfant-m|Merci, maman.",
        "narrateur|La paille a un rond vert, maintenant.",
        "narrateur|Le sable tiède colle aux paumes.",
    ],
    (2, 1, 1): [
        "enfant-m|Papa, porte-moi, sur la marche.",
        "papa|Je te tiens, contre moi.",
        "narrateur|Papa cale la caisse sur la marche.",
        "narrateur|Le métal sonne, puis se tait.",
        "narrateur|Amir se hausse, pieds arrêtés.",
        "narrateur|Sa main cueille la pomme verte.",
        "enfant-m|Je l'ai !",
        "maman|Tu l'as prise, sans danser.",
        "narrateur|Le métal reste chaud, un peu.",
    ],
    (2, 1, 2): [
        "enfant-m|Mes pieds, plus de toc.",
        "narrateur|Il attend, collé à la rampe.",
        "narrateur|Le métal cesse de sonner.",
        "narrateur|La caisse ne penche plus.",
        "enfant-m|Un pas, puis la main.",
        "narrateur|Il se hausse, un seul pas.",
        "narrateur|La pomme vient dans sa paume.",
        "papa|Tes pieds ont su s'arrêter.",
        "maman|Elle est verte, à toi.",
    ],
    (2, 1, 3): [
        "enfant-m|On pousse, jusqu'au pied.",
        "narrateur|Ils poussent la caisse au pied du métal.",
        "maman|J'incline la branche, vers le bois.",
        "narrateur|La pomme descend, lente.",
        "enfant-m|Dans la caisse !",
        "narrateur|Ploc, un jus mince sur le bois.",
        "papa|Vous l'avez menée ici.",
        "narrateur|Le métal reste chaud, au-dessus.",
        "narrateur|La feuille collée brille, au fond.",
    ],
    (2, 2, 1): [
        "enfant-m|Papa, plus haut, s'il te plaît.",
        "papa|Je te porte, tiens l'arrosoir.",
        "narrateur|Papa soulève Amir près du métal.",
        "narrateur|Amir cueille, et la pomme glisse au bec.",
        "enfant-m|Elle est dedans !",
        "narrateur|Une goutte lave le vert, tout petit.",
        "maman|Tes pieds pendent, sans toc.",
        "narrateur|Le métal reste chaud, à côté.",
        "narrateur|Le bec sonne, un coup, puis rien.",
    ],
    (2, 2, 2): [
        "enfant-m|J'attends, pieds sages.",
        "narrateur|Il pose l'arrosoir au pied du métal.",
        "narrateur|Le métal ne sonne plus.",
        "maman|On laisse le vent travailler.",
        "narrateur|La feuille tremble, puis s'en va.",
        "narrateur|La pomme lâche, sans bruit.",
        "enfant-m|Ploc !",
        "papa|Elle est venue vers le bec.",
        "narrateur|Une ligne d'eau brille, puis sèche.",
    ],
    (2, 2, 3): [
        "maman|Je penche la branche, vers le bec.",
        "narrateur|Amir tient l'arrosoir, pieds au métal.",
        "enfant-m|Je ne tape plus.",
        "narrateur|La pomme glisse le long des feuilles.",
        "narrateur|Elle rentre dans le bec, ploc.",
        "papa|Tu l'as gardé droit, l'arrosoir.",
        "enfant-m|Elle est à nous !",
        "narrateur|Une goutte reste sur le vert.",
        "narrateur|Une poussière de métal brille au bec.",
    ],
    (2, 3, 1): [
        "enfant-m|Papa, secoue un peu.",
        "papa|Sans la meurtrir, Amir.",
        "narrateur|Le chapeau attend au pied du métal.",
        "narrateur|La branche ondule, une fois.",
        "narrateur|La pomme tombe dans la paille.",
        "enfant-m|Dans le nid !",
        "maman|Tu as bien visé le chapeau.",
        "narrateur|Le métal reste chaud, au-dessus.",
        "narrateur|La paille reçoit un rond vert.",
    ],
    (2, 3, 2): [
        "enfant-m|On attend le petit vent.",
        "maman|Pieds sages, alors.",
        "narrateur|Amir se tait, le chapeau aussi.",
        "narrateur|Une poussière de métal s'envole, puis rien.",
        "narrateur|Un souffle passe dans les feuilles.",
        "narrateur|La pomme se détache, lente.",
        "enfant-m|Elle vient !",
        "papa|Dans le chapeau, pile.",
        "narrateur|La paille sent le sucré, au métal.",
    ],
    (2, 3, 3): [
        "maman|J'incline la branche, vers le nid.",
        "narrateur|Le chapeau reste au pied du toboggan.",
        "enfant-m|Je ne saute plus.",
        "narrateur|La pomme glisse, puis se pose.",
        "papa|Dans le chapeau, tout au fond.",
        "enfant-m|Merci, maman.",
        "narrateur|La paille a un rond vert, au métal.",
        "narrateur|Le métal luit, le nid à côté.",
    ],
    (3, 1, 1): [
        "enfant-m|Papa, porte-moi sous la chaîne.",
        "papa|Je te tiens, Amir.",
        "narrateur|Papa cale la caisse dans l'herbe.",
        "narrateur|La chaîne se tait, un instant.",
        "narrateur|Amir se hausse, pieds arrêtés.",
        "narrateur|Sa main cueille la pomme verte.",
        "enfant-m|Je l'ai !",
        "maman|Tu l'as prise, sans voler.",
        "narrateur|Un brin d'herbe reste au mollet.",
    ],
    (3, 1, 2): [
        "enfant-m|Mes pieds, plus de vol.",
        "narrateur|Il attend, et l'herbe cesse de glisser.",
        "narrateur|La caisse ne recule plus.",
        "enfant-m|Un geste, tout seul.",
        "narrateur|Il se hausse, lentement.",
        "narrateur|La pomme vient dans sa paume.",
        "papa|Tes pieds ont su s'arrêter.",
        "maman|Elle est verte, à toi.",
        "narrateur|La chaîne reste muette, au-dessus.",
    ],
    (3, 1, 3): [
        "enfant-m|On pousse, sous la chaîne !",
        "narrateur|Ils poussent la caisse sous la chaîne.",
        "maman|J'incline la branche, vers le bois.",
        "narrateur|La pomme descend, lente.",
        "enfant-m|Dans la caisse !",
        "narrateur|Ploc, un jus mince sur le bois.",
        "papa|Vous l'avez menée ici.",
        "narrateur|L'herbe a un sillon, tout net.",
        "narrateur|La feuille collée brille, au fond.",
    ],
    (3, 2, 1): [
        "enfant-m|Papa, plus haut, s'il te plaît.",
        "papa|Je te porte, tiens l'arrosoir.",
        "narrateur|Papa soulève Amir sous la chaîne.",
        "narrateur|Amir cueille, et la pomme glisse au bec.",
        "enfant-m|Elle est dedans !",
        "narrateur|Une goutte lave le vert, tout petit.",
        "maman|Tes pieds pendent, sans voler.",
        "narrateur|Un brin d'herbe reste au mollet.",
        "narrateur|Le bec penche, plein, sous la chaîne.",
    ],
    (3, 2, 2): [
        "enfant-m|J'attends, pieds sages.",
        "narrateur|Il pose l'arrosoir sous le siège.",
        "narrateur|La chaîne ne chante plus.",
        "maman|On laisse le vent travailler.",
        "narrateur|La feuille tremble, puis s'en va.",
        "narrateur|La pomme lâche, sans bruit.",
        "enfant-m|Ploc !",
        "papa|Elle est venue vers le bec.",
        "narrateur|Une goutte sèche sur le genou.",
    ],
    (3, 2, 3): [
        "maman|Je penche la branche, vers le bec.",
        "narrateur|Amir tient l'arrosoir, pieds dans l'herbe.",
        "enfant-m|Je ne tape plus.",
        "narrateur|La pomme glisse le long des feuilles.",
        "narrateur|Elle rentre dans le bec, ploc.",
        "papa|Tu l'as gardé droit, l'arrosoir.",
        "enfant-m|Elle est à nous !",
        "narrateur|Une goutte reste sur le vert.",
        "narrateur|La chaîne se tait, le bec aussi.",
    ],
    (3, 3, 1): [
        "enfant-m|Papa, secoue un peu.",
        "papa|Sans la meurtrir, Amir.",
        "narrateur|Le chapeau attend sous la chaîne.",
        "narrateur|La branche ondule, une fois.",
        "narrateur|La pomme tombe dans la paille.",
        "enfant-m|Dans le nid !",
        "maman|Tu as bien visé le chapeau.",
        "narrateur|Un brin d'herbe reste au mollet.",
        "narrateur|Un toit de feuille sur le nid.",
    ],
    (3, 3, 2): [
        "enfant-m|On attend le petit vent.",
        "maman|Pieds sages, alors.",
        "narrateur|Amir se tait, le chapeau aussi.",
        "narrateur|Un brin d'herbe s'envole, puis rien.",
        "narrateur|Un souffle passe dans les feuilles.",
        "narrateur|La pomme se détache, lente.",
        "enfant-m|Elle vient !",
        "papa|Dans le chapeau, pile.",
        "narrateur|La paille sent le sucré, sous la chaîne.",
    ],
    (3, 3, 3): [
        "maman|J'incline la branche, vers le nid.",
        "narrateur|Le chapeau reste sous la balançoire.",
        "enfant-m|Je ne saute plus.",
        "narrateur|La pomme glisse, puis se pose.",
        "papa|Dans le chapeau, tout au fond.",
        "enfant-m|Merci, maman.",
        "narrateur|La paille a un rond vert, sous le siège.",
        "narrateur|Le siège d'à côté reste sage.",
    ],
}

END_SONS = {1: "oiseau,sable", 2: "oiseau,metal", 3: "oiseau,chaine"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Ils s'assoient sous le pommier.",
        "enfant-m|Elle est sucrée, papa !",
        "papa|Tes bras ont cueilli, avec les miens.",
        "maman|Un morceau pour chacun.",
        "narrateur|Le jus colle un peu au menton.",
        "narrateur|La caisse sèche, à côté, un peu molle.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Un trou rond reste dans le bac.",
    ],
    (1, 1, 2): [
        "narrateur|Amir croque, assis tout près.",
        "enfant-m|Mes pieds ont su attendre.",
        "maman|Et la pomme est venue.",
        "papa|Le jus, sur le pouce ?",
        "enfant-m|Oui, il brille.",
        "narrateur|La caisse garde son ombre, au sable.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Un grain de sable brille au menton.",
    ],
    (1, 1, 3): [
        "narrateur|Ils partagent la pomme, trois bouchées.",
        "enfant-m|On a poussé, et elle est venue.",
        "papa|Le bois sent le jus, un peu.",
        "maman|Essuie ton menton, Amir.",
        "narrateur|Un filet sucré reste au coin.",
        "narrateur|La caisse a un rond mouillé, au fond.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Le bois garde un rond de jus.",
    ],
    (1, 2, 1): [
        "narrateur|L'arrosoir sert d'assiette, un moment.",
        "enfant-m|Elle a voyagé dans le bec !",
        "papa|Je t'ai porté, tu as cueilli.",
        "maman|Le vert est froid, un peu.",
        "narrateur|Amir souffle dessus, puis croque.",
        "narrateur|L'arrosoir sonne creux, après.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Le bec garde un rond vert, sablé.",
    ],
    (1, 2, 2): [
        "narrateur|Ils croquent à l'ombre, sans se presser.",
        "enfant-m|J'ai attendu, et ploc.",
        "maman|Le vent a fait le reste.",
        "papa|Le sucré, ça valait l'attente.",
        "narrateur|Le jus coule, une perle, au poignet.",
        "narrateur|L'arrosoir garde une auréole verte.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Une auréole verte sèche au bec.",
    ],
    (1, 2, 3): [
        "narrateur|Maman coupe la pomme en trois.",
        "enfant-m|Tu as penché, et je tenais.",
        "papa|Le bec a fait un bon nid.",
        "maman|Tes pieds sont restés sages.",
        "narrateur|Chaque bouchée sent l'herbe chaude.",
        "narrateur|L'arrosoir repose, le bec vers le ciel.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Une goutte verte reste sur le grain.",
    ],
    (1, 3, 1): [
        "narrateur|Le chapeau devient une petite table.",
        "enfant-m|Papa a secoué, sans la meurtrir.",
        "papa|Elle n'a pas eu mal.",
        "maman|La paille sent le sucré, maintenant.",
        "narrateur|Amir croque, et un jus perle.",
        "narrateur|Le chapeau garde un rond plus foncé.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|La paille a un toit de feuille.",
    ],
    (1, 3, 2): [
        "narrateur|Ils s'allongent un peu, sous les feuilles.",
        "enfant-m|Le vent l'a mise dans le nid.",
        "maman|Tes pieds ont su se taire.",
        "papa|Une bouchée, puis une autre.",
        "narrateur|Le sucré reste longtemps, en bouche.",
        "narrateur|Le chapeau a une tache ronde, au fond.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Le nid sent le sucré, au creux du bac.",
    ],
    (1, 3, 3): [
        "narrateur|Ils rentrent la pomme vers le banc.",
        "enfant-m|Maman a incliné, pile.",
        "maman|Tu as laissé le nid à sa place.",
        "papa|Le vert craque, tout frais.",
        "narrateur|Trois bouches, un même sucré.",
        "narrateur|Le chapeau reprendra le clou, plus tard.",
        "narrateur|Sous les pieds, le sable chuchote.",
        "narrateur|Le sable a un cercle autour du nid.",
    ],
    (2, 1, 1): [
        "narrateur|Ils s'assoient au pied du métal.",
        "enfant-m|Elle est sucrée, papa !",
        "papa|Tes bras ont cueilli, avec les miens.",
        "maman|Un morceau pour chacun.",
        "narrateur|Le jus colle un peu au menton.",
        "narrateur|La caisse sèche, contre la marche.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Le métal se tait, vide et chaud.",
    ],
    (2, 1, 2): [
        "narrateur|Amir croque, assis sur la marche basse.",
        "enfant-m|Mes pieds ont su attendre.",
        "maman|Et la pomme est venue.",
        "papa|Le jus, sur le pouce ?",
        "enfant-m|Oui, il brille.",
        "narrateur|La caisse garde son ombre, au métal.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Un toc reste dans la marche.",
    ],
    (2, 1, 3): [
        "narrateur|Ils partagent la pomme, trois bouchées.",
        "enfant-m|On a poussé, et elle est venue.",
        "papa|Le bois sent le jus, un peu.",
        "maman|Essuie ton menton, Amir.",
        "narrateur|Un filet sucré reste au coin.",
        "narrateur|La caisse a un rond mouillé, au fond.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Le bois sent le jus, contre le métal.",
    ],
    (2, 2, 1): [
        "narrateur|L'arrosoir sert d'assiette, au pied.",
        "enfant-m|Elle a voyagé dans le bec !",
        "papa|Je t'ai porté, tu as cueilli.",
        "maman|Le vert est froid, un peu.",
        "narrateur|Amir souffle dessus, puis croque.",
        "narrateur|L'arrosoir sonne creux, après.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Le bec sonne creux, au pied du métal.",
    ],
    (2, 2, 2): [
        "narrateur|Ils croquent à l'ombre du toboggan.",
        "enfant-m|J'ai attendu, et ploc.",
        "maman|Le vent a fait le reste.",
        "papa|Le sucré, ça valait l'attente.",
        "narrateur|Le jus coule, une perle, au poignet.",
        "narrateur|L'arrosoir garde une auréole verte.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Une ligne d'eau sèche sur le métal.",
    ],
    (2, 2, 3): [
        "narrateur|Maman coupe la pomme en trois.",
        "enfant-m|Tu as penché, et je tenais.",
        "papa|Le bec a fait un bon nid.",
        "maman|Tes pieds sont restés sages.",
        "narrateur|Chaque bouchée sent l'herbe chaude.",
        "narrateur|L'arrosoir repose, le bec vers le ciel.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Une poussière de métal brille au bec.",
    ],
    (2, 3, 1): [
        "narrateur|Le chapeau devient une petite table.",
        "enfant-m|Papa a secoué, sans la meurtrir.",
        "papa|Elle n'a pas eu mal.",
        "maman|La paille sent le sucré, maintenant.",
        "narrateur|Amir croque, et un jus perle.",
        "narrateur|Le chapeau garde un rond plus foncé.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Le chapeau a un rond plus foncé, au métal.",
    ],
    (2, 3, 2): [
        "narrateur|Ils s'allongent un peu, au pied du métal.",
        "enfant-m|Le vent l'a mise dans le nid.",
        "maman|Tes pieds ont su se taire.",
        "papa|Une bouchée, puis une autre.",
        "narrateur|Le sucré reste longtemps, en bouche.",
        "narrateur|Le chapeau a une tache ronde, au fond.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|La paille sent le sucré, au pied du toboggan.",
    ],
    (2, 3, 3): [
        "narrateur|Ils rentrent la pomme vers le banc.",
        "enfant-m|Maman a incliné, pile.",
        "maman|Tu as laissé le nid à sa place.",
        "papa|Le vert craque, tout frais.",
        "narrateur|Trois bouches, un même sucré.",
        "narrateur|Le chapeau reprendra le clou, plus tard.",
        "narrateur|Un petit toc reste dans le métal.",
        "narrateur|Le métal luit, le chapeau à côté.",
    ],
    (3, 1, 1): [
        "narrateur|Ils s'assoient sous la chaîne.",
        "enfant-m|Elle est sucrée, papa !",
        "papa|Tes bras ont cueilli, avec les miens.",
        "maman|Un morceau pour chacun.",
        "narrateur|Le jus colle un peu au menton.",
        "narrateur|La caisse sèche, dans l'herbe.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|Plus aucun cri sur la chaîne.",
    ],
    (3, 1, 2): [
        "narrateur|Amir croque, assis dans l'herbe.",
        "enfant-m|Mes pieds ont su attendre.",
        "maman|Et la pomme est venue.",
        "papa|Le jus, sur le pouce ?",
        "enfant-m|Oui, il brille.",
        "narrateur|La caisse garde son ombre, dans l'herbe.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|Un brin d'herbe reste au mollet.",
    ],
    (3, 1, 3): [
        "narrateur|Ils partagent la pomme, trois bouchées.",
        "enfant-m|On a poussé, et elle est venue.",
        "papa|Le bois sent le jus, un peu.",
        "maman|Essuie ton menton, Amir.",
        "narrateur|Un filet sucré reste au coin.",
        "narrateur|La caisse a un rond mouillé, au fond.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|L'herbe a un sillon sous la caisse.",
    ],
    (3, 2, 1): [
        "narrateur|L'arrosoir sert d'assiette, sous la chaîne.",
        "enfant-m|Elle a voyagé dans le bec !",
        "papa|Je t'ai porté, tu as cueilli.",
        "maman|Le vert est froid, un peu.",
        "narrateur|Amir souffle dessus, puis croque.",
        "narrateur|L'arrosoir sonne creux, après.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|Le bec penche, après, sous la chaîne.",
    ],
    (3, 2, 2): [
        "narrateur|Ils croquent à l'ombre des sièges.",
        "enfant-m|J'ai attendu, et ploc.",
        "maman|Le vent a fait le reste.",
        "papa|Le sucré, ça valait l'attente.",
        "narrateur|Le jus coule, une perle, au poignet.",
        "narrateur|L'arrosoir garde une auréole verte.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|Une goutte sèche sur le genou.",
    ],
    (3, 2, 3): [
        "narrateur|Maman coupe la pomme en trois.",
        "enfant-m|Tu as penché, et je tenais.",
        "papa|Le bec a fait un bon nid.",
        "maman|Tes pieds sont restés sages.",
        "narrateur|Chaque bouchée sent l'herbe chaude.",
        "narrateur|L'arrosoir repose, le bec vers le ciel.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|Le bec et la chaîne se taisent ensemble.",
    ],
    (3, 3, 1): [
        "narrateur|Le chapeau devient une petite table.",
        "enfant-m|Papa a secoué, sans la meurtrir.",
        "papa|Elle n'a pas eu mal.",
        "maman|La paille sent le sucré, maintenant.",
        "narrateur|Amir croque, et un jus perle.",
        "narrateur|Le chapeau garde un rond plus foncé.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|La feuille collée fait un toit sur la paille.",
    ],
    (3, 3, 2): [
        "narrateur|Ils s'allongent un peu, sous les sièges.",
        "enfant-m|Le vent l'a mise dans le nid.",
        "maman|Tes pieds ont su se taire.",
        "papa|Une bouchée, puis une autre.",
        "narrateur|Le sucré reste longtemps, en bouche.",
        "narrateur|Le chapeau a une tache ronde, au fond.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|Le siège d'à côté reste vide.",
    ],
    (3, 3, 3): [
        "narrateur|Ils rentrent la pomme vers le banc.",
        "enfant-m|Maman a incliné, pile.",
        "maman|Tu as laissé le nid à sa place.",
        "papa|Le vert craque, tout frais.",
        "narrateur|Trois bouches, un même sucré.",
        "narrateur|Le chapeau reprendra le clou, plus tard.",
        "narrateur|Puis la chaîne se tait, un instant.",
        "narrateur|La fourmi arrive en haut, sans se presser.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "oiseau,goutte",
        {"emphasis": "pomme verte"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le bac à sable", "le toboggan", "les balançoires")},
    )

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], T1[a]["passage"], "action", T1[a]["sons"],
            {"emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], T1[a]["question"], "clue", "",
            {"fields": T1[a]["qfields"], "emphasis": "pomme"},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], T1[a]["confirm"], "confirm", T1[a]["sons"],
            {"emphasis": "pomme verte"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("la caisse", "l'arrosoir", "le chapeau")},
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
                    {"emphasis": "jus"},
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
        "ce n'est pas une faute",
        "beaucoup d'énergie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "sami",
        "nino",
        "tom ",
        "léa",
        "energie",
        "énergie",
        "tout doux",
        "tout calme",
        "tout lent",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")

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
        "# TREE-DIF-012 — La pomme verte et les pieds d'Amir\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — l'énergie n'est pas une faute ; jouer, attendre, demander (vécue)\n"
        "- **Personnages :** Amir, papa, maman\n"
        "- **Lieu :** le jardin, sous le pommier\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Au fond du jardin, le pommier chauffe. Une fourmi grimpe. Une pomme verte "
        "a une feuille collée qui tremble. Amir veut **cette** pomme, maintenant. "
        "Il saute : sa main frotte l'air. Première idée ratée. "
        "Bac, toboggan ou balançoires : les pieds dansent, la pomme reste. "
        "Caisse, arrosoir ou chapeau : l'objet penche, glisse ou se vide tant que les pieds tapent. "
        "Papa porte, les pieds s'arrêtent, ou la famille pousse. Amir croque. Le jus sucré paie le début.\n\n"
        "## Vécu\n\n"
        "Amir veut la pomme verte **maintenant**. Ses pieds tapent. Sauter ne suffit pas. "
        "Chaque choix change l'obstacle et le climax (sable qui mange, métal qui sonne, chaîne qui chante). "
        "La leçon se voit : taper fait pencher ; demander, attendre ou pousser ensemble cueille. "
        "Fin : jus au menton + image unique du chemin (trou du bac, toc du métal, fourmi en haut).\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan énergie / faute / Nino / Sami / Tom / Léa / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (arrosoir ramené). Question d'adulte. Un « en ce moment ».\n"
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
