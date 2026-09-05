#!/usr/bin/env python3
"""TREE-DIF-059 — Les deux plantes de Nina, à la fenêtre (N1, DIF.COR.002)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-059"
N1 = 10
TITLE = "Les deux plantes de Nina, à la fenêtre"
FIL = (
    "Nina connaît le rebord du midi. Un anneau de liège entoure le pot mince. "
    "Elle veut installer et arroser cactus rond et tige mince avant que le soleil parte. "
    "Papa veut la soupe d'abord ; le cactus prend toute la place. "
    "T1 = arrosoir / cuillère / linge ; les trois partent. "
    "T2 = rebord trop étroit, chaise trop haute, radiateur trop chaud. "
    "T3 = neuf façons de leur faire une place. L'anneau du début revient."
)
CHARS = "Nina, papa, maman"
SETTING = "près de la fenêtre : rebord, chaise, radiateur"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "anneau de liège",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=deux_plantes_un_anneau_beige; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "anneau de liège",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=le_même_geste_ne_suffit_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=deux_corps_un_même_rebord_ça_coinçe; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "anneau de liège",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=une_place_pour_chaque_forme; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "anneau de liège",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_anneau_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Nina connaît cette fenêtre, presque par cœur.",
    "narrateur|Le bois du rebord sent le soleil.",
    "narrateur|Le radiateur fait tic, contre le mur.",
    "papa|Tu vois le toit, Nina ?",
    "enfant-f|Il est sec, papa.",
    "narrateur|Une mouche tape le carreau, puis part.",
    "narrateur|Deux plantes attendent, sur le tabouret.",
    "narrateur|Le cactus a le ventre rond.",
    "narrateur|La tige verte a les feuilles minces.",
    "narrateur|Un détail paraît neuf, sur elles.",
    "narrateur|Un anneau de liège entoure le pot mince.",
    "papa|Il est beige, un peu rêche.",
    "enfant-f|Il tient le pot, tout autour.",
    "maman|Tu l'as vu, cet anneau ?",
    "enfant-f|Je veux les deux, près du soleil.",
    "papa|La soupe, d'abord ?",
    "enfant-f|Elles, maintenant.",
    "narrateur|Papa se tait, un instant.",
    "narrateur|En ce moment, Nina pousse les deux.",
    "narrateur|Le cactus rond prend toute la place.",
    "narrateur|La tige glisse vers le vide.",
    "enfant-f|Oh.",
    "narrateur|Le sourire de Nina disparaît.",
    "narrateur|L'envie et l'inquiétude se bousculent.",
    "maman|Je m'accroupis, à ta hauteur.",
    "papa|Merci, tu as rattrapé le pot.",
    "enfant-f|Je prépare, alors.",
    "maman|L'arrosoir, la cuillère, le linge.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près du tabouret.",
    "narrateur|L'arrosoir, la cuillère, et le linge.",
    "maman|Tu commences par laquelle ?",
]

T1 = {
    1: {
        "lab": "l'arrosoir",
        "sons": "metal,eau",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|Nina prend l'arrosoir, froid.",
            "narrateur|Le métal pique un peu, entre ses doigts.",
            "enfant-f|Il est lourd.",
            "maman|Garde-le, on emporte tout.",
            "narrateur|Elle verse un filet, trop vite.",
            "narrateur|Le cactus boit, trop peu.",
            "narrateur|La tige noie une feuille, trop mince.",
            "enfant-f|Pareil, pour les deux.",
            "enfant-f|Ça ne va pas.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "papa|Tu les regardes, toutes les deux ?",
            "narrateur|Près du tabouret, la cuillère attend.",
            "maman|Le linge aussi, avec vous.",
            "enfant-f|On prend les trois.",
            "narrateur|L'anneau de liège tient, au pot mince.",
        ],
        "question": [
            "narrateur|Nina a pris l'arrosoir, d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "arrosoir",
            "accepted_examples": "arrosoir | l'arrosoir | d'abord l'arrosoir | le métal",
            "retry_prompt": "Nina a pris l'arrosoir, d'abord.",
        },
        "confirm": [
            "enfant-f|L'arrosoir.",
            "papa|Oui.",
            "narrateur|Nina glisse la cuillère sous le bras.",
            "maman|Le linge, je te le tends.",
            "enfant-f|Je le prends.",
            "narrateur|Elle prend le cactus, puis la tige.",
            "papa|Les deux viennent.",
            "enfant-f|On cherche l'endroit.",
            "narrateur|L'anneau de liège luit, beige.",
        ],
    },
    2: {
        "lab": "la cuillère",
        "sons": "metal,goutte",
        "emphasis": "cuillère",
        "passage": [
            "narrateur|Nina saisit la cuillère, froide.",
            "narrateur|Le métal cliquette une fois, sec.",
            "enfant-f|Elle est petite.",
            "papa|C'est pour la tige, goutte à goutte.",
            "narrateur|Elle arrose le cactus, trop vite.",
            "narrateur|Puis elle arrose la tige, trop vite.",
            "enfant-f|Pareil, pour les deux.",
            "narrateur|Le cactus reste sec, trop large.",
            "narrateur|La tige tremble, trop mouillée.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|Le sourire de Nina disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "maman|Tu les regardes, toutes les deux ?",
            "narrateur|Sur le tabouret, l'arrosoir attend.",
            "papa|Le linge aussi, avec vous.",
            "enfant-f|Je garde la cuillère.",
            "narrateur|Les trois affaires partent avec elle.",
        ],
        "question": [
            "narrateur|Nina a pris la cuillère, d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "cuillère",
            "accepted_examples": "cuillère | la cuillère | d'abord la cuillère | le métal",
            "retry_prompt": "Nina a pris la cuillère, d'abord.",
        },
        "confirm": [
            "enfant-f|La cuillère.",
            "maman|Oui.",
            "narrateur|Elle ramasse l'arrosoir, petit.",
            "papa|Le linge, dans l'autre main ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les deux plantes voyagent contre elle.",
            "maman|Vous partez toutes les trois.",
            "enfant-f|On va où, maintenant ?",
            "narrateur|L'anneau de liège penche, au pot mince.",
        ],
    },
    3: {
        "lab": "le linge",
        "sons": "tissu,carreau",
        "emphasis": "linge",
        "passage": [
            "narrateur|Nina saisit le linge, tiède.",
            "narrateur|Le tissu sent le savon, un peu.",
            "enfant-f|Il est doux.",
            "maman|Essuie le rebord, d'abord.",
            "narrateur|Elle frotte le bois, trop vite.",
            "narrateur|Elle pousse les deux, d'un coup.",
            "enfant-f|Pareil, pour les deux.",
            "narrateur|Le cactus rentre, trop large.",
            "narrateur|La tige dépasse, une feuille dehors.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "papa|Tu les regardes, toutes les deux ?",
            "narrateur|Près du tabouret, l'arrosoir attend.",
            "maman|La cuillère aussi, avec vous.",
            "enfant-f|Je garde le linge.",
            "narrateur|Rien ne reste près du tabouret.",
        ],
        "question": [
            "narrateur|Nina a pris le linge, d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "linge",
            "accepted_examples": "linge | le linge | d'abord le linge | le tissu",
            "retry_prompt": "Nina a pris le linge, d'abord.",
        },
        "confirm": [
            "enfant-f|Le linge.",
            "papa|Oui.",
            "narrateur|Maman lui passe l'arrosoir, froid.",
            "maman|La cuillère, sous le bras.",
            "enfant-f|Elle est là.",
            "narrateur|Le cactus et la tige avancent avec elle.",
            "papa|Les deux viennent, avec le linge.",
            "enfant-f|Il me faut de la lumière.",
            "narrateur|L'anneau de liège tient, caché.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|L'arrosoir tape sa jambe, à chaque pas.",
        "narrateur|Les deux plantes veulent boire.",
        "narrateur|L'anneau de liège reste collé, beige.",
        "papa|Le rebord, la chaise, ou le radiateur ?",
    ],
    2: [
        "narrateur|La cuillère cliquette, contre sa hanche.",
        "narrateur|Les deux plantes veulent boire.",
        "narrateur|L'anneau de liège penche, au pot mince.",
        "papa|Le rebord, la chaise, ou le radiateur ?",
    ],
    3: [
        "narrateur|Un coin de linge frotte le carreau.",
        "narrateur|Les deux plantes veulent boire.",
        "narrateur|L'anneau de liège tient, caché.",
        "papa|Le rebord, la chaise, ou le radiateur ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "bois,eau",
        "emphasis": "rebord",
        "passage": [
            "narrateur|Elles s'approchent du rebord, trop étroit.",
            "enfant-f|La lumière est là.",
            "narrateur|Elle pose les deux, d'un même geste.",
            "narrateur|Un filet d'eau tombe, trop loin.",
            "narrateur|Le cactus large bute contre le bois.",
            "narrateur|La tige légère glisse vers le sol.",
            "enfant-f|L'une reste, l'autre part.",
            "narrateur|L'anneau de liège s'enfonce, caché.",
            "narrateur|Nina veut les pousser, plus fort.",
            "narrateur|Ses mains s'arrêtent, au-dessus du vide.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu fais comment, avec les deux ?",
            "narrateur|Une goutte perle sur le bois.",
        ],
    },
    (2, 1): {
        "sons": "bois,metal",
        "emphasis": "rebord",
        "passage": [
            "narrateur|La cuillère accroche le bois, puis lâche.",
            "narrateur|Elles s'approchent du rebord, trop étroit.",
            "enfant-f|Un soleil, ici.",
            "narrateur|Elle verse d'un même geste.",
            "narrateur|Le cactus bute, trop rond.",
            "narrateur|La tige glisse, trop mince.",
            "enfant-f|L'une reste, l'autre part.",
            "narrateur|L'anneau de liège disparaît, un instant.",
            "narrateur|Nina lève la cuillère, trop vite.",
            "narrateur|Puis elle la baisse.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu fais comment, avec les deux ?",
            "narrateur|Une goutte tremble au creux de la cuillère.",
        ],
    },
    (3, 1): {
        "sons": "bois,tissu",
        "emphasis": "rebord",
        "passage": [
            "narrateur|Le linge accroche un clou, trop mince.",
            "narrateur|Elles s'approchent du rebord, trop étroit.",
            "enfant-f|Vous entrez, sous le linge.",
            "narrateur|Elle les pousse d'un même geste.",
            "narrateur|Le cactus bute contre le bois.",
            "narrateur|La tige file vers le vide.",
            "enfant-f|Ça ne tient pas.",
            "narrateur|L'anneau de liège s'enfonce, caché.",
            "narrateur|Nina veut tout recouvrir, trop vite.",
            "narrateur|Ses mains s'arrêtent, au-dessus.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu fais comment, avec les deux ?",
            "narrateur|Un coin de linge traîne dans l'air.",
        ],
    },
    (1, 2): {
        "sons": "chaise,eau",
        "emphasis": "chaise",
        "passage": [
            "narrateur|Sur la chaise, le bois penche un peu.",
            "enfant-f|La lumière, ici.",
            "narrateur|L'eau rate le pot, trop haut.",
            "narrateur|Nina pose un pied, trop haut pour elles.",
            "narrateur|Le cactus pèse, et la chaise penche.",
            "narrateur|La tige légère penche, elle aussi.",
            "enfant-f|Elle va tomber.",
            "narrateur|L'anneau de liège s'éloigne, trop haut.",
            "narrateur|Nina veut tout poser, trop vite.",
            "narrateur|Ses mains s'arrêtent, au dossier.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu les gardes comment, ensemble ?",
            "narrateur|L'arrosoir penche, trop lourd.",
        ],
    },
    (2, 2): {
        "sons": "chaise,metal",
        "emphasis": "chaise",
        "passage": [
            "narrateur|Sur la chaise, le bois penche un peu.",
            "enfant-f|La lumière, ici.",
            "narrateur|La cuillère tremble, trop haute.",
            "narrateur|Elle pousse les deux, d'un coup.",
            "narrateur|Le cactus part trop loin.",
            "narrateur|La tige penche, trop mince.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|L'anneau de liège dérive, au bord.",
            "narrateur|Nina lève la cuillère, trop pleine.",
            "narrateur|Puis elle la retient.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu les gardes comment, ensemble ?",
            "narrateur|Une goutte tombe de la cuillère, trop penchée.",
        ],
    },
    (3, 2): {
        "sons": "chaise,tissu",
        "emphasis": "chaise",
        "passage": [
            "narrateur|Sur la chaise, le bois penche un peu.",
            "enfant-f|La lumière, ici.",
            "narrateur|Le linge glisse du dossier, trop mince.",
            "narrateur|Elle pousse les deux, d'un coup.",
            "narrateur|Le cactus pèse, trop large.",
            "narrateur|La tige glisse du siège.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|L'anneau de liège s'éloigne, mouillé.",
            "narrateur|Nina veut tout envelopper, trop vite.",
            "narrateur|Ses mains s'arrêtent, au bord.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu les gardes comment, ensemble ?",
            "narrateur|Le linge se gonfle, comme un nuage.",
        ],
    },
    (1, 3): {
        "sons": "fer,chaleur",
        "emphasis": "radiateur",
        "passage": [
            "narrateur|Près du radiateur, le fer est trop chaud.",
            "enfant-f|La lumière, là-bas.",
            "narrateur|L'eau tiédit, trop près du fer.",
            "narrateur|Elle pose les deux, d'un même geste.",
            "narrateur|Le cactus tient, le fer est chaud.",
            "narrateur|La tige baisse une feuille, trop près.",
            "enfant-f|Elle n'aime pas.",
            "narrateur|L'anneau de liège penche, presque brûlé.",
            "narrateur|Nina veut tout rapprocher, trop vite.",
            "narrateur|Ses mains s'arrêtent, au-dessus du fer.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu les rassembles comment ?",
            "narrateur|Un air passe, trop sec.",
        ],
    },
    (2, 3): {
        "sons": "fer,metal",
        "emphasis": "radiateur",
        "passage": [
            "narrateur|Près du radiateur, le fer est trop chaud.",
            "enfant-f|La lumière, là-bas.",
            "narrateur|La cuillère chauffe, trop vite.",
            "narrateur|Elle pose les deux, d'un même geste.",
            "narrateur|Le cactus tient, trop large.",
            "narrateur|La tige baisse une feuille, trop près.",
            "enfant-f|Elle n'aime pas.",
            "narrateur|L'anneau de liège penche, presque brûlé.",
            "narrateur|Nina veut verser, trop vite.",
            "narrateur|Puis elle retient la cuillère.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu les rassembles comment ?",
            "narrateur|Le fer fait tic, trop fort.",
        ],
    },
    (3, 3): {
        "sons": "fer,tissu",
        "emphasis": "radiateur",
        "passage": [
            "narrateur|Près du radiateur, le fer est trop chaud.",
            "enfant-f|La lumière, là-bas.",
            "narrateur|Le linge sèche trop vite, trop chaud.",
            "narrateur|Elle pose les deux, d'un même geste.",
            "narrateur|Le cactus tient, trop large.",
            "narrateur|La tige baisse une feuille, trop près.",
            "enfant-f|Elle n'aime pas.",
            "narrateur|L'anneau de liège penche, presque brûlé.",
            "narrateur|Nina veut tout envelopper, trop vite.",
            "narrateur|Ses mains s'arrêtent, au-dessus du fer.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu les rassembles comment ?",
            "narrateur|Le linge claque, trop sec.",
        ],
    },
}

T3_LABS = {
    1: ("la planche", "deux places", "la caisse"),
    2: ("le sol", "le banc", "les mains"),
    3: ("le coin", "le linge", "plus tard"),
}

T3_CHOICE = {
    1: [
        "narrateur|Sur le rebord, l'une reste, l'autre glisse.",
        "narrateur|L'anneau de liège reste caché, un instant.",
        "papa|Tu fais quoi, Nina ?",
    ],
    2: [
        "narrateur|Sur la chaise, l'eau rate le pot.",
        "narrateur|L'anneau de liège dérive, trop haut.",
        "maman|Tu fais quoi, avec elles ?",
    ],
    3: [
        "narrateur|Près du fer, la tige baisse une feuille.",
        "narrateur|L'anneau de liège penche, trop chaud.",
        "papa|Tu fais quoi, maintenant ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "enfant-f|La planche, plus large.",
        "narrateur|Elle pose l'arrosoir sur la planche.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "enfant-f|Je regarde l'anneau.",
        "narrateur|L'anneau de liège luit, beige.",
        "narrateur|Elle le glisse, comme un stop.",
        "enfant-f|Toi ici, toi là.",
        "narrateur|Le cactus trouve sa place, ronde.",
        "narrateur|La tige revient, trop mince.",
        "papa|Deux places, deux formes.",
        "maman|Elles boivent, chacune.",
        "narrateur|Un peu d'eau tremble au bec.",
    ],
    (1, 1, 2): [
        "enfant-f|Deux places, pour elles.",
        "narrateur|Elle écarte les deux pots, lentement.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|L'anneau de liège réapparaît, au bois.",
        "narrateur|Il mesure la tige, trop mince.",
        "narrateur|Le cactus pose le ventre, sans coincer.",
        "narrateur|La tige reste, sans glisser.",
        "enfant-f|Vous tenez, toutes les deux.",
        "maman|L'anneau est là, au bois.",
        "papa|Le rebord les tient, maintenant.",
        "narrateur|Un filet s'arrête, bas.",
    ],
    (1, 1, 3): [
        "enfant-f|La caisse, pour toutes.",
        "narrateur|Elle pose l'arrosoir dans la caisse.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Je regarde d'abord.",
        "narrateur|L'anneau de liège luit, au pot mince.",
        "narrateur|Elle le pose, comme un nid.",
        "narrateur|Le cactus et la tige montent ensemble.",
        "enfant-f|Une lumière, plus large.",
        "papa|Le vide reste en dessous, seul.",
        "maman|Elles se touchent, les deux.",
        "narrateur|Un filet tombe, puis s'arrête.",
        "narrateur|Un rond d'eau reste au bois.",
    ],
    (1, 2, 1): [
        "enfant-f|Le sol, comme une table.",
        "narrateur|Elle pose l'arrosoir au sol, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Je regarde l'anneau.",
        "narrateur|L'anneau de liège brille, au parquet.",
        "narrateur|Nina s'assoit, les pieds au bois.",
        "narrateur|Le cactus tient au parquet, trop rond.",
        "narrateur|La tige s'allonge contre lui, trop mince.",
        "enfant-f|Vous avez le sol, toutes les deux.",
        "papa|Chacun a sa place.",
        "maman|L'eau reste, plus calme.",
        "narrateur|Un peu d'eau perle sur le parquet.",
    ],
    (1, 2, 2): [
        "enfant-f|Le banc, plus bas.",
        "narrateur|Elle pose l'arrosoir sur le banc.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|L'anneau de liège reste collé, beige.",
        "narrateur|Elle le glisse contre le bord.",
        "narrateur|Le cactus tient, le bois aussi.",
        "enfant-f|Vous tenez, sans tomber.",
        "papa|Le banc était assez large.",
        "maman|La tige reste près, trop mince.",
        "narrateur|Une goutte minuscule, puis plus.",
        "narrateur|Un rond d'eau sèche au banc.",
    ],
    (1, 2, 3): [
        "enfant-f|Les mains, pour la mince.",
        "narrateur|Elle tient la tige, l'arrosoir tout près.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Pas toute l'eau.",
        "narrateur|L'anneau de liège luit, mouillé.",
        "narrateur|Une goutte tombe, trop petite.",
        "enfant-f|Vous avez l'eau, toutes les deux.",
        "papa|Plus besoin de monter.",
        "maman|Tes mains ont tenu la tige.",
        "narrateur|L'arrosoir attend, trop bas.",
        "narrateur|Deux gouttes restent sur le cactus.",
    ],
    (1, 3, 1): [
        "enfant-f|Le coin, plus frais.",
        "narrateur|Elle pose l'arrosoir au coin, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Je regarde.",
        "narrateur|L'anneau de liège tient, au pot mince.",
        "narrateur|Elle le pose, pour marquer le frais.",
        "narrateur|Le cactus tient au coin, trop large.",
        "narrateur|La tige tient, une feuille plus haute.",
        "enfant-f|Vous buvez ici, sans le fer.",
        "papa|Le coin a deux places, maintenant.",
        "maman|Plus besoin du fer.",
        "narrateur|Un air passe, plus simple.",
    ],
    (1, 3, 2): [
        "enfant-f|Le linge, pour l'ombre.",
        "narrateur|Elle pose le linge, l'arrosoir tout près.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends le fer.",
        "narrateur|L'anneau de liège reste au frais.",
        "narrateur|Elle le glisse sous le tissu.",
        "narrateur|Les deux plantes avancent, trop lent.",
        "enfant-f|Vous avez l'eau, plus douce.",
        "papa|L'ombre était plus douce.",
        "maman|L'une près de l'autre.",
        "narrateur|Un peu d'eau reste au pli.",
    ],
    (1, 3, 3): [
        "enfant-f|Plus tard, plus calme.",
        "narrateur|Elle pose l'arrosoir plus loin, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|On attend un peu.",
        "narrateur|L'anneau de liège luit, à l'abri.",
        "narrateur|Le fer reste derrière, moins chaud.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Attendre un peu, c'était plus simple.",
        "maman|La vitre sent, plus loin.",
        "narrateur|Un rond d'eau sèche sous l'air.",
        "narrateur|Le tic du fer se tait, presque.",
    ],
    (2, 1, 1): [
        "enfant-f|La planche, plus large.",
        "narrateur|Elle pose la cuillère sur la planche.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "enfant-f|Je regarde l'anneau.",
        "narrateur|L'anneau de liège luit, beige.",
        "narrateur|Elle le glisse, comme un stop.",
        "enfant-f|Toi ici, toi là.",
        "narrateur|Le cactus s'assoit d'un côté.",
        "narrateur|La tige s'assoit de l'autre.",
        "papa|Deux places, deux formes.",
        "maman|Elles boivent, chacune.",
        "narrateur|La cuillère verse un filet, fin.",
    ],
    (2, 1, 2): [
        "enfant-f|Deux places, pour elles.",
        "narrateur|Elle verse moins, avec la cuillère.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|L'anneau de liège réapparaît, au bois.",
        "narrateur|Il mesure la tige, trop mince.",
        "narrateur|Le cactus pose le ventre, sans coincer.",
        "narrateur|La tige reste, sans glisser.",
        "enfant-f|Vous tenez, toutes les deux.",
        "maman|L'anneau est là, au bois.",
        "papa|Le rebord les tient, maintenant.",
        "narrateur|Une goutte reste au fond de la cuillère.",
    ],
    (2, 1, 3): [
        "enfant-f|La caisse, pour toutes.",
        "narrateur|Maman glisse une caisse sous le rebord.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Je verse après.",
        "narrateur|L'anneau de liège luit, au pot mince.",
        "narrateur|Elle le pose, comme un nid.",
        "narrateur|Le cactus et la tige montent ensemble.",
        "enfant-f|Une lumière, plus large.",
        "papa|Le vide reste en dessous, seul.",
        "maman|Elles se touchent, les deux.",
        "narrateur|La cuillère claque, un toc léger.",
        "narrateur|Un filet tremble au bord.",
    ],
    (2, 2, 1): [
        "enfant-f|Le sol, comme une table.",
        "narrateur|Elle pose la cuillère au sol, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Je verse après, pas maintenant.",
        "narrateur|L'anneau de liège brille, au parquet.",
        "narrateur|Nina s'assoit, les pieds au bois.",
        "narrateur|Le cactus tient au parquet, trop rond.",
        "narrateur|La tige s'allonge contre lui, trop mince.",
        "enfant-f|Vous avez le sol, toutes les deux.",
        "papa|Chacun a sa place.",
        "maman|L'eau reste, plus calme.",
        "narrateur|La cuillère repose sur le parquet.",
    ],
    (2, 2, 2): [
        "enfant-f|Le banc, plus bas.",
        "narrateur|Elle glisse la cuillère sur le banc.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|L'anneau de liège reste collé, beige.",
        "narrateur|Elle le glisse contre le bord.",
        "narrateur|Le cactus tient, le bois aussi.",
        "enfant-f|Vous tenez, sans tomber.",
        "papa|Le banc était assez large.",
        "maman|La tige reste près, trop mince.",
        "narrateur|La cuillère penche, puis se tient.",
        "narrateur|Une goutte s'arrête au bord.",
    ],
    (2, 2, 3): [
        "enfant-f|Les mains, pour la mince.",
        "narrateur|Elle tient la tige, la cuillère tout près.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Pas toute l'eau.",
        "narrateur|L'anneau de liège luit, mouillé.",
        "narrateur|La cuillère arrose le cactus, puis la tige.",
        "enfant-f|Vous avez l'eau, toutes les deux.",
        "papa|Plus besoin de monter.",
        "maman|Tes mains ont tenu la tige.",
        "narrateur|La cuillère se vide, presque.",
        "narrateur|Deux gouttes restent au métal.",
    ],
    (2, 3, 1): [
        "enfant-f|Le coin, plus frais.",
        "narrateur|Elle pose la cuillère au coin, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Je verse après.",
        "narrateur|L'anneau de liège tient, au pot mince.",
        "narrateur|Elle le pose, pour marquer le frais.",
        "narrateur|Le cactus tient au coin, trop large.",
        "narrateur|La tige tient, une feuille plus haute.",
        "enfant-f|Vous buvez ici, sans le fer.",
        "papa|Le coin a deux places, maintenant.",
        "maman|Plus besoin du fer.",
        "narrateur|La cuillère tient entre les deux.",
    ],
    (2, 3, 2): [
        "enfant-f|Le linge, pour l'ombre.",
        "narrateur|Elle pose le linge, la cuillère tout près.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends le fer.",
        "narrateur|L'anneau de liège reste au frais.",
        "narrateur|Elle le glisse sous le tissu.",
        "narrateur|Les deux plantes avancent, trop lent.",
        "enfant-f|Vous avez l'eau, plus douce.",
        "papa|L'ombre était plus douce.",
        "maman|L'une près de l'autre.",
        "narrateur|La cuillère chauffe sous le linge.",
    ],
    (2, 3, 3): [
        "enfant-f|Plus tard, plus calme.",
        "narrateur|Elle pose la cuillère plus loin, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|On attend un peu.",
        "narrateur|L'anneau de liège luit, à l'abri.",
        "narrateur|Le fer reste derrière, moins chaud.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Attendre un peu, c'était plus simple.",
        "maman|La vitre sent, plus loin.",
        "narrateur|Une goutte tombe du fer, seule.",
        "narrateur|Le tic du fer se tait, presque.",
    ],
    (3, 1, 1): [
        "enfant-f|La planche, plus large.",
        "narrateur|Elle pose le linge sur la planche.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "enfant-f|Je regarde l'anneau.",
        "narrateur|L'anneau de liège luit, beige.",
        "narrateur|Elle le glisse, comme un stop.",
        "enfant-f|Toi ici, toi là.",
        "narrateur|Le cactus s'assoit d'un côté.",
        "narrateur|La tige s'assoit de l'autre.",
        "papa|Deux places, deux formes.",
        "maman|Elles boivent, chacune.",
        "narrateur|Un fil de linge reste au bois.",
    ],
    (3, 1, 2): [
        "enfant-f|Deux places, pour elles.",
        "narrateur|Elle écarte les deux pots, lentement.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|L'anneau de liège réapparaît, au bois.",
        "narrateur|Il mesure la tige, trop mince.",
        "narrateur|Le cactus pose le ventre, sans coincer.",
        "narrateur|La tige reste, sans glisser.",
        "enfant-f|Vous tenez, toutes les deux.",
        "maman|L'anneau est là, au bois.",
        "papa|Le rebord les tient, maintenant.",
        "narrateur|Le linge garde un pli, tiède.",
    ],
    (3, 1, 3): [
        "enfant-f|La caisse, pour toutes.",
        "narrateur|Elle pose le linge dans la caisse.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Je recouvre après.",
        "narrateur|L'anneau de liège luit, au pot mince.",
        "narrateur|Elle le pose, comme un nid.",
        "narrateur|Le cactus et la tige montent ensemble.",
        "enfant-f|Une lumière, plus large.",
        "papa|Le vide reste en dessous, seul.",
        "maman|Elles se touchent, les deux.",
        "narrateur|La caisse disparaît sous le linge.",
        "narrateur|Un coin de linge sèche au bord.",
    ],
    (3, 2, 1): [
        "enfant-f|Le sol, comme une table.",
        "narrateur|Elle pose le linge au sol, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Le linge, après.",
        "narrateur|L'anneau de liège brille, au parquet.",
        "narrateur|Nina s'assoit, les pieds au bois.",
        "narrateur|Le cactus tient au parquet, trop rond.",
        "narrateur|La tige s'allonge contre lui, trop mince.",
        "enfant-f|Vous avez le sol, toutes les deux.",
        "papa|Chacun a sa place.",
        "maman|L'eau reste, plus calme.",
        "narrateur|Le parquet et le linge se touchent.",
    ],
    (3, 2, 2): [
        "enfant-f|Le banc, plus bas.",
        "narrateur|Elle pose le linge sur le banc.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|L'anneau de liège reste collé, beige.",
        "narrateur|Elle le glisse contre le bord.",
        "narrateur|Le cactus tient, le bois aussi.",
        "enfant-f|Vous tenez, sans tomber.",
        "papa|Le banc était assez large.",
        "maman|La tige reste près, trop mince.",
        "narrateur|Un coin de linge sèche au bord.",
        "narrateur|Le linge garde deux formes, nettes.",
    ],
    (3, 2, 3): [
        "enfant-f|Les mains, pour la mince.",
        "narrateur|Sous le linge, elle tient la tige.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Pas toute l'eau.",
        "narrateur|L'anneau de liège luit, mouillé.",
        "narrateur|Elle arrose le cactus, puis la tige.",
        "enfant-f|Vous avez l'eau, toutes les deux.",
        "papa|Plus besoin de monter.",
        "maman|Tes mains ont tenu la tige.",
        "narrateur|Le linge se lourde, un peu.",
        "narrateur|Deux gouttes restent au tissu.",
    ],
    (3, 3, 1): [
        "enfant-f|Le coin, plus frais.",
        "narrateur|Elle pose le linge au coin, bas.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Le linge, après.",
        "narrateur|L'anneau de liège tient, au pot mince.",
        "narrateur|Elle le pose, pour marquer le frais.",
        "narrateur|Le cactus tient au coin, trop large.",
        "narrateur|La tige tient, une feuille plus haute.",
        "enfant-f|Vous buvez ici, sans le fer.",
        "papa|Le coin a deux places, maintenant.",
        "maman|Plus besoin du fer.",
        "narrateur|Une feuille colle au coin du linge.",
    ],
    (3, 3, 2): [
        "enfant-f|Le linge, pour l'ombre.",
        "narrateur|Elle les enveloppe, cactus contre tige.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Attends le fer.",
        "narrateur|L'anneau de liège reste au frais.",
        "narrateur|Le tissu tient, même si ça chauffe.",
        "enfant-f|Vous avez l'ombre, toutes les deux.",
        "papa|Le fer prend le linge, pas elles.",
        "maman|Feuille contre feuille.",
        "narrateur|Le linge sent le bois, un peu.",
    ],
    (3, 3, 3): [
        "enfant-f|Plus tard, plus calme.",
        "narrateur|Elle porte les deux, le linge autour.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|On attend un peu.",
        "narrateur|L'anneau de liège luit, à l'abri.",
        "narrateur|Le fer reste derrière, moins chaud.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Attendre un peu, c'était plus simple.",
        "maman|La vitre sent, plus loin.",
        "narrateur|Le linge s'égoutte sur le bois.",
        "narrateur|Le tic du fer se tait, presque.",
    ],
}

T3_SONS = {
    (1, 1): "bois,planche",
    (1, 2): "bois,pots",
    (1, 3): "caisse,terre",
    (2, 1): "parquet,eau",
    (2, 2): "banc,bois",
    (2, 3): "mains,goutte",
    (3, 1): "coin,air",
    (3, 2): "linge,ombre",
    (3, 3): "fer,silence",
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Deux ronds d'eau restent sur la planche.",
        "enfant-f|Vous avez eu votre lumière.",
        "narrateur|L'anneau de liège tient, au pot mince.",
        "narrateur|Ça a failli rater.",
        "papa|Tes mains ont fait les deux places.",
        "maman|Elles sont ensemble, quand même.",
        "enfant-f|On reste un peu.",
        "narrateur|La planche garde deux ronds d'eau.",
    ],
    (1, 1, 2): [
        "narrateur|Les deux pots sentent la terre.",
        "enfant-f|Vous teniez, toutes les deux.",
        "narrateur|L'anneau de liège brille, au bois.",
        "narrateur|Un instant, la tige partait.",
        "papa|Le rebord les a tenues.",
        "maman|Elles ont bu, chacune.",
        "enfant-f|On reste, maintenant.",
        "narrateur|Le bois n'a plus qu'une trace, trop bas.",
    ],
    (1, 1, 3): [
        "narrateur|Dans la caisse, la terre tremble.",
        "enfant-f|Une lumière, plus large.",
        "narrateur|L'anneau de liège luit, au nid.",
        "narrateur|Le vide n'a pas gagné.",
        "papa|Tes mains ont mis la caisse.",
        "maman|Elles se touchent, les deux.",
        "enfant-f|Une goutte, pour rire.",
        "narrateur|Une poussière s'arrête sur le bois.",
    ],
    (1, 2, 1): [
        "narrateur|Au sol, deux traces restent, trop différentes.",
        "enfant-f|On a bu ici, sans tomber.",
        "narrateur|L'anneau de liège tient, au parquet.",
        "narrateur|Ça a failli trop haut.",
        "papa|Le sol avait deux places.",
        "maman|Plus besoin de la chaise.",
        "enfant-f|On reste un peu.",
        "narrateur|Le parquet se tait, trop lentement.",
    ],
    (1, 2, 2): [
        "narrateur|Sur le banc, ça sent le bois.",
        "enfant-f|Vous teniez, sans tomber.",
        "narrateur|L'anneau de liège sèche, au bord.",
        "narrateur|Un instant, la tige penchait.",
        "papa|Le banc était assez large.",
        "maman|Deux formes, une même lumière.",
        "enfant-f|La soupe, après ?",
        "narrateur|Un peu de soleil reste sur le bois.",
    ],
    (1, 2, 3): [
        "narrateur|Dans ses mains, une feuille reste, trop petite.",
        "enfant-f|Vous avez eu l'eau.",
        "narrateur|L'anneau de liège luit, mouillé.",
        "narrateur|La chaise n'était pas nécessaire.",
        "papa|Plus besoin de monter.",
        "maman|Tes mains ont tenu la tige.",
        "enfant-f|On est là.",
        "narrateur|La chaise redevient vide, trop simple.",
    ],
    (1, 3, 1): [
        "narrateur|Au coin, deux gouttes restent.",
        "enfant-f|Vous aviez le coin.",
        "narrateur|L'anneau de liège tient, au frais.",
        "narrateur|Un instant, la tige baissait.",
        "papa|Le coin avait deux places.",
        "maman|Plus besoin du fer.",
        "enfant-f|On reste un peu.",
        "narrateur|Le fer se tait, trop lentement.",
    ],
    (1, 3, 2): [
        "narrateur|Sous le linge, l'air est doux.",
        "enfant-f|Vous aviez l'eau, plus douce.",
        "narrateur|L'anneau de liège reste au frais.",
        "narrateur|Le fer a failli les prendre.",
        "papa|L'ombre était plus douce.",
        "maman|L'une près de l'autre.",
        "enfant-f|Elles ont bu, pour de vrai.",
        "narrateur|Un pli de tissu s'arrête contre le pot.",
    ],
    (1, 3, 3): [
        "narrateur|Plus tard, l'air est plus doux.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|L'anneau de liège luit, à l'abri.",
        "narrateur|Le fer reste trop chaud, derrière.",
        "papa|Attendre un peu, c'était plus simple.",
        "maman|La vitre sent, plus loin.",
        "enfant-f|On reste, maintenant.",
        "narrateur|Le fer du radiateur retombe, trop bas.",
    ],
    (2, 1, 1): [
        "narrateur|Deux ronds d'eau restent sur la planche.",
        "enfant-f|Vous avez eu votre lumière.",
        "narrateur|L'anneau de liège tient, au pot mince.",
        "narrateur|Ça a failli rater.",
        "papa|Tes mains ont fait les deux places.",
        "maman|Elles sont ensemble, quand même.",
        "enfant-f|On reste un peu.",
        "narrateur|Une goutte d'argent tremble au bois.",
    ],
    (2, 1, 2): [
        "narrateur|Les deux pots sentent la terre.",
        "enfant-f|Vous teniez, toutes les deux.",
        "narrateur|L'anneau de liège brille, au bois.",
        "narrateur|Un instant, la tige partait.",
        "papa|Le rebord les a tenues.",
        "maman|Elles ont bu, chacune.",
        "enfant-f|On reste, maintenant.",
        "narrateur|La cuillère garde une goutte, trop fine.",
    ],
    (2, 1, 3): [
        "narrateur|Dans la caisse, la terre tremble.",
        "enfant-f|Une lumière, plus large.",
        "narrateur|L'anneau de liège luit, au nid.",
        "narrateur|Le vide n'a pas gagné.",
        "papa|Tes mains ont mis la caisse.",
        "maman|Elles se touchent, les deux.",
        "enfant-f|Une goutte, pour rire.",
        "narrateur|La caisse tient une odeur de terre.",
    ],
    (2, 2, 1): [
        "narrateur|Au sol, deux traces restent, trop différentes.",
        "enfant-f|On a bu ici, sans tomber.",
        "narrateur|L'anneau de liège tient, au parquet.",
        "narrateur|Ça a failli trop haut.",
        "papa|Le sol avait deux places.",
        "maman|Plus besoin de la chaise.",
        "enfant-f|On reste un peu.",
        "narrateur|La cuillère repose, trop froide.",
    ],
    (2, 2, 2): [
        "narrateur|Sur le banc, ça sent le bois.",
        "enfant-f|Vous teniez, sans tomber.",
        "narrateur|L'anneau de liège sèche, au bord.",
        "narrateur|Un instant, la tige penchait.",
        "papa|Le banc était assez large.",
        "maman|Deux formes, une même lumière.",
        "enfant-f|La soupe, après ?",
        "narrateur|Un rai d'eau reste sur le banc.",
    ],
    (2, 2, 3): [
        "narrateur|Dans ses mains, une feuille reste, trop petite.",
        "enfant-f|Vous avez eu l'eau.",
        "narrateur|L'anneau de liège luit, mouillé.",
        "narrateur|La chaise n'était pas nécessaire.",
        "papa|Plus besoin de monter.",
        "maman|Tes mains ont tenu la tige.",
        "enfant-f|On est là.",
        "narrateur|Deux gouttes restent au métal.",
    ],
    (2, 3, 1): [
        "narrateur|Au coin, deux gouttes restent.",
        "enfant-f|Vous aviez le coin.",
        "narrateur|L'anneau de liège tient, au frais.",
        "narrateur|Un instant, la tige baissait.",
        "papa|Le coin avait deux places.",
        "maman|Plus besoin du fer.",
        "enfant-f|On reste un peu.",
        "narrateur|La cuillère tient entre les deux pots.",
    ],
    (2, 3, 2): [
        "narrateur|Sous le linge, l'air est doux.",
        "enfant-f|Vous aviez l'eau, plus douce.",
        "narrateur|L'anneau de liège reste au frais.",
        "narrateur|Le fer a failli les prendre.",
        "papa|L'ombre était plus douce.",
        "maman|L'une près de l'autre.",
        "enfant-f|Elles ont bu, pour de vrai.",
        "narrateur|La cuillère chauffe sous le pli.",
    ],
    (2, 3, 3): [
        "narrateur|Plus tard, l'air est plus doux.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|L'anneau de liège luit, à l'abri.",
        "narrateur|Le fer reste trop chaud, derrière.",
        "papa|Attendre un peu, c'était plus simple.",
        "maman|La vitre sent, plus loin.",
        "enfant-f|On reste, maintenant.",
        "narrateur|Une goutte tombe du fer, trop seule.",
    ],
    (3, 1, 1): [
        "narrateur|Deux ronds d'eau restent sur la planche.",
        "enfant-f|Vous avez eu votre lumière.",
        "narrateur|L'anneau de liège tient, au pot mince.",
        "narrateur|Ça a failli rater.",
        "papa|Tes mains ont fait les deux places.",
        "maman|Elles sont ensemble, quand même.",
        "enfant-f|On reste un peu.",
        "narrateur|Un fil de linge reste au bois.",
    ],
    (3, 1, 2): [
        "narrateur|Les deux pots sentent la terre.",
        "enfant-f|Vous teniez, toutes les deux.",
        "narrateur|L'anneau de liège brille, au bois.",
        "narrateur|Un instant, la tige partait.",
        "papa|Le rebord les a tenues.",
        "maman|Elles ont bu, chacune.",
        "enfant-f|On reste, maintenant.",
        "narrateur|Le linge garde un pli tiède.",
    ],
    (3, 1, 3): [
        "narrateur|Dans la caisse, la terre tremble.",
        "enfant-f|Une lumière, plus large.",
        "narrateur|L'anneau de liège luit, au nid.",
        "narrateur|Le vide n'a pas gagné.",
        "papa|Tes mains ont mis la caisse.",
        "maman|Elles se touchent, les deux.",
        "enfant-f|Une goutte, pour rire.",
        "narrateur|La caisse disparaît sous le linge.",
    ],
    (3, 2, 1): [
        "narrateur|Au sol, deux traces restent, trop différentes.",
        "enfant-f|On a bu ici, sans tomber.",
        "narrateur|L'anneau de liège tient, au parquet.",
        "narrateur|Ça a failli trop haut.",
        "papa|Le sol avait deux places.",
        "maman|Plus besoin de la chaise.",
        "enfant-f|On reste un peu.",
        "narrateur|Le parquet et le linge se touchent.",
    ],
    (3, 2, 2): [
        "narrateur|Sur le banc, ça sent le bois.",
        "enfant-f|Vous teniez, sans tomber.",
        "narrateur|L'anneau de liège sèche, au bord.",
        "narrateur|Un instant, la tige penchait.",
        "papa|Le banc était assez large.",
        "maman|Deux formes, une même lumière.",
        "enfant-f|La soupe, après ?",
        "narrateur|Un coin de linge sèche au bord.",
    ],
    (3, 2, 3): [
        "narrateur|Dans ses mains, une feuille reste, trop petite.",
        "enfant-f|Vous avez eu l'eau.",
        "narrateur|L'anneau de liège luit, mouillé.",
        "narrateur|La chaise n'était pas nécessaire.",
        "papa|Plus besoin de monter.",
        "maman|Tes mains ont tenu la tige.",
        "enfant-f|On est là.",
        "narrateur|Le linge redevient plat, trop rêche.",
    ],
    (3, 3, 1): [
        "narrateur|Au coin, deux gouttes restent.",
        "enfant-f|Vous aviez le coin.",
        "narrateur|L'anneau de liège tient, au frais.",
        "narrateur|Un instant, la tige baissait.",
        "papa|Le coin avait deux places.",
        "maman|Plus besoin du fer.",
        "enfant-f|On reste un peu.",
        "narrateur|Une feuille colle au coin du linge.",
    ],
    (3, 3, 2): [
        "narrateur|Sous le linge, l'air est doux.",
        "enfant-f|Vous aviez l'eau, plus douce.",
        "narrateur|L'anneau de liège reste au frais.",
        "narrateur|Le fer a failli les prendre.",
        "papa|L'ombre était plus douce.",
        "maman|L'une près de l'autre.",
        "enfant-f|Elles ont bu, pour de vrai.",
        "narrateur|Le linge sent le bois, un peu.",
    ],
    (3, 3, 3): [
        "narrateur|Plus tard, l'air est plus doux.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|L'anneau de liège luit, à l'abri.",
        "narrateur|Le fer reste trop chaud, derrière.",
        "papa|Attendre un peu, c'était plus simple.",
        "maman|La vitre sent, plus loin.",
        "enfant-f|On reste, maintenant.",
        "narrateur|Le linge s'égoutte sur le bois.",
    ],
}

END_SONS = {1: "arrosoir,eau", 2: "cuillere,goutte", 3: "linge,bois"}
T3_EMPH = {
    1: {1: "planche", 2: "places", 3: "caisse"},
    2: {1: "sol", 2: "banc", 3: "mains"},
    3: {1: "coin", 2: "linge", 3: "plus tard"},
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "radiateur,carreau",
        {"emphasis": "anneau de liège"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("l'arrosoir", "la cuillère", "le linge"), "pause_before": 200},
    )

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], T1[a]["passage"], "action", T1[a]["sons"],
            {"emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], T1[a]["question"], "clue", "",
            {"fields": T1[a]["qfields"], "emphasis": T1[a]["emphasis"], "pause_before": 200},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], T1[a]["confirm"], "confirm", T1[a]["sons"],
            {"emphasis": "anneau de liège"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le rebord", "la chaise", "le radiateur"), "pause_before": 200},
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
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[a],
                    {"emphasis": "anneau de liège"},
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
        "plus rond ou plus mince",
        "le corps n'est pas",
        "sami",
        "tom ",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "virgule de buée",
        "marque fine",
        "ombre-flèche",
        "perle de verre",
        "œillet de cuivre",
        "bouton de nacre",
        "nœud de raphia",
        "pois ivoire",
        "grain de savon",
        "grain de vanille",
        "pastille de colle",
        "grain de son",
        "bouton de lavande",
        "grand-père",
        "maîtresse",
        "jardinier",
        "merle",
        "miel",
        "étoile de papier",
        "vitre embuée",
        "zoé",
        "zoe",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "anneau de liège" not in blob:
        raise SystemExit(f"{SID}: anneau de liège absent")
    if re.search(r"\b(encore|déjà|deja)\b", blob):
        raise SystemExit(f"{SID}: tic encore/déjà")

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
        if "anneau de liège" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']} indice anneau absent de la fin")
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
    if min(counts) < 380:
        raise SystemExit(f"chemin trop court: {min(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c["text_xai_tags"] == c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-059 — Les deux plantes de Nina, à la fenêtre\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.COR.002 — deux corps, deux places (vécue : cactus rond / tige mince, "
        "même geste raté, une place pour chacune)\n"
        "- **Personnages :** Nina, papa, maman (un seul enfant)\n"
        "- **Lieu :** près de la fenêtre : rebord, chaise, radiateur\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Nina connaît le rebord du midi. Un détail paraît neuf : un **anneau de liège** "
        "entoure le pot mince. Mission : installer et arroser les deux plantes au rebord, "
        "avant que le soleil parte. Papa veut la soupe d'abord. Elle pousse les deux d'un même "
        "geste : le cactus prend la place, la tige glisse. Arrosoir, cuillère ou linge : les trois "
        "partent. Rebord trop étroit, chaise trop haute, radiateur trop chaud. Elle refuse de "
        "foncer. L'anneau du début revient. Planche, deux places, caisse ; sol, banc, mains ; "
        "coin, linge, plus tard. Les deux boivent. L'objet porte une trace.\n\n"
        "## Vécu\n\n"
        "Le sourire disparaît. L'envie et l'inquiétude se bousculent. Papa ou maman s'accroupit "
        "à la même hauteur. Personne ne donne la réponse. Nina observe l'anneau, écoute le tic "
        "du fer, invente une place pour chaque forme. La leçon se voit : on arrose les deux, "
        "sans les forcer dans le même trou. Autre récit que TREE-DIF-048 (étoile papier) et "
        "TREE-COL-019 (vitre embuée).\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Plus rond ou plus mince » / Zoé / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (papa : tu as rattrapé le pot). Question d'adulte. Un « en ce moment ».\n"
        "- Indice unique : anneau de liège (inventé, payé au climax). Pas de gabarit v2 collé.\n"
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
