#!/usr/bin/env python3
"""TREE-DIF-035 — Les deux poupées de Chouchou dans le bain (N1, DIF.COR.002)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-035"
N1 = 10
TITLE = "Les deux poupées de Chouchou dans le bain"
FIL = (
    "Après la pluie, au rebord du robinet, Chouchou veut un vrai bain "
    "pour ses deux poupées. Un bouton de lavande colle au ventre de coton. "
    "Elle les pousse d'un même geste : le coton bute, le bois glisse. "
    "T1 = savon / gobelet / serviette ; les trois partent. "
    "T2 = évier étroit, baignoire trop haute, bac du jardin trop venteux. "
    "T3 = neuf façons de leur faire une place. Le bouton du début revient."
)
CHARS = "Chouchou, papa, maman"
SETTING = "salle de bain après la pluie, puis le bac du jardin"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "bouton de lavande",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=deux_poupées_un_bouton_rose; tempo=naturel; sourire=léger; respiration=ample",
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
        "emphasis": "bouton de lavande",
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
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=deux_corps_un_même_bain_ça_coinçe; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "bouton de lavande",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=une_place_pour_chaque_forme; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "bouton de lavande",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_bouton_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Après la pluie, le carrelage sent l'eau.",
    "narrateur|Chouchou connaît cette salle de bain.",
    "narrateur|Ça sent le carrelage mouillé, et le savon.",
    "narrateur|Le rebord du robinet brille, tiède.",
    "enfant-f|Mes poupées, vous êtes là.",
    "narrateur|Elles attendent sur le rebord, tièdes.",
    "narrateur|La poupée de coton a le ventre rond.",
    "narrateur|Celle de bois a les jambes minces.",
    "narrateur|Un détail paraît neuf, sur elles.",
    "narrateur|Un bouton de lavande colle au ventre.",
    "papa|Il est collé, rose, minuscule.",
    "enfant-f|Il sent le savon, rose.",
    "maman|Tu l'as vu, ce bouton ?",
    "papa|Tu veux leur donner un bain ?",
    "enfant-f|Les deux, dans l'eau.",
    "narrateur|En ce moment, Chouchou ouvre le robinet.",
    "narrateur|L'eau tombe trop vite, trop haute.",
    "narrateur|Elle pousse les deux, d'un coup.",
    "narrateur|Le coton bute contre le rebord.",
    "narrateur|Le bois glisse vers le trou.",
    "enfant-f|Oh.",
    "narrateur|Le sourire de Chouchou disparaît.",
    "narrateur|L'envie et l'inquiétude se bousculent.",
    "maman|Je m'accroupis, à ta hauteur.",
    "papa|Merci d'avoir sorti les deux.",
    "enfant-f|Je prépare, alors.",
    "maman|Le savon, le gobelet, la serviette.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près du rebord.",
    "narrateur|Le savon, le gobelet, et la serviette.",
    "maman|Tu commences par laquelle ?",
]

T1 = {
    1: {
        "lab": "le savon",
        "sons": "savon,eau",
        "emphasis": "savon",
        "passage": [
            "narrateur|Chouchou prend le savon, froid.",
            "narrateur|Il pèse un peu, dans sa paume.",
            "enfant-f|Il sent la lavande.",
            "maman|Garde-le, on emporte tout.",
            "narrateur|Elle frotte le ventre rond, vite.",
            "narrateur|Puis elle frotte les jambes minces.",
            "enfant-f|Pareil, pour les deux.",
            "narrateur|Le coton mousse, trop.",
            "narrateur|Le bois reste sec, lui.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "papa|Tu les regardes, toutes les deux ?",
            "narrateur|Près du robinet, le gobelet attend.",
            "maman|La serviette aussi, avec vous.",
            "enfant-f|On prend les trois.",
            "narrateur|Le bouton de lavande tient, au ventre.",
        ],
        "question": [
            "narrateur|Chouchou a pris le savon, d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "savon",
            "accepted_examples": "savon | le savon | d'abord le savon | la lavande",
            "retry_prompt": "Chouchou a pris le savon, d'abord.",
        },
        "confirm": [
            "enfant-f|Le savon.",
            "papa|Oui.",
            "narrateur|Chouchou glisse le gobelet sous le bras.",
            "maman|La serviette, je te la tends.",
            "enfant-f|Je la prends.",
            "narrateur|Elle prend le coton, puis le bois.",
            "papa|Les deux viennent.",
            "enfant-f|On cherche l'endroit.",
            "narrateur|Le bouton de lavande luit, au ventre.",
        ],
    },
    2: {
        "lab": "le gobelet",
        "sons": "plastique,eau",
        "emphasis": "gobelet",
        "passage": [
            "narrateur|Chouchou saisit le gobelet, bleu.",
            "narrateur|Le plastique claque une fois, sec.",
            "enfant-f|Il tient l'eau.",
            "papa|C'est pour verser, pas trop.",
            "narrateur|Elle arrose le ventre rond, vite.",
            "narrateur|Puis elle arrose les jambes minces.",
            "enfant-f|Pareil, pour les deux.",
            "narrateur|Le coton boit, trop.",
            "narrateur|Le bois laisse glisser, lui.",
            "enfant-f|Ça ne va pas.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "maman|Tu les regardes, toutes les deux ?",
            "narrateur|Sur le rebord, le savon attend.",
            "papa|La serviette aussi, avec vous.",
            "enfant-f|Je garde le gobelet.",
            "narrateur|Les trois affaires partent avec elle.",
        ],
        "question": [
            "narrateur|Chouchou a pris le gobelet, d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "gobelet",
            "accepted_examples": "gobelet | le gobelet | d'abord le gobelet | le plastique",
            "retry_prompt": "Chouchou a pris le gobelet, d'abord.",
        },
        "confirm": [
            "enfant-f|Le gobelet.",
            "maman|Oui.",
            "narrateur|Elle ramasse le savon, petit.",
            "papa|La serviette, dans l'autre main ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les deux poupées voyagent contre elle.",
            "maman|Vous partez toutes les trois.",
            "enfant-f|On va où, maintenant ?",
            "narrateur|Le bouton de lavande penche, au ventre.",
        ],
    },
    3: {
        "lab": "la serviette",
        "sons": "linge,eau",
        "emphasis": "serviette",
        "passage": [
            "narrateur|Chouchou déplie la serviette, tiède.",
            "narrateur|Le tissu tombe, trop large, jusqu'au carrelage.",
            "enfant-f|Elle sent le linge.",
            "maman|Garde-la, on emporte tout.",
            "narrateur|Elle enveloppe le ventre rond, vite.",
            "narrateur|Puis elle enveloppe les jambes minces.",
            "enfant-f|Pareil, pour les deux.",
            "narrateur|Le coton rentre, trop large.",
            "narrateur|Le bois dépasse, une jambe dehors.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à sa hauteur.",
            "papa|Tu les regardes, toutes les deux ?",
            "narrateur|Près du robinet, le savon attend.",
            "maman|Le gobelet aussi, avec vous.",
            "enfant-f|Je garde la serviette.",
            "narrateur|Rien ne reste près du rebord.",
        ],
        "question": [
            "narrateur|Chouchou a pris la serviette, d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "serviette",
            "accepted_examples": "serviette | la serviette | d'abord la serviette | le linge",
            "retry_prompt": "Chouchou a pris la serviette, d'abord.",
        },
        "confirm": [
            "enfant-f|La serviette.",
            "papa|Oui.",
            "narrateur|Maman lui passe le savon, froid.",
            "maman|Le gobelet, dans la poche.",
            "enfant-f|Il est là.",
            "narrateur|Le coton et le bois avancent avec elle.",
            "papa|Les deux viennent, avec le linge.",
            "enfant-f|Il me faut de l'eau.",
            "narrateur|Le bouton de lavande tient, caché.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le savon glisse entre ses doigts.",
        "narrateur|Les deux poupées attendent de l'eau.",
        "narrateur|Le bouton de lavande reste collé, rond.",
        "papa|L'évier, la baignoire, ou le bac ?",
    ],
    2: [
        "narrateur|Le gobelet tape sa hanche, à chaque pas.",
        "narrateur|Les deux poupées attendent de l'eau.",
        "narrateur|Le bouton de lavande penche, au ventre.",
        "papa|L'évier, la baignoire, ou le bac ?",
    ],
    3: [
        "narrateur|Un coin de serviette frotte le carrelage.",
        "narrateur|Les deux poupées attendent de l'eau.",
        "narrateur|Le bouton de lavande tient, caché.",
        "papa|L'évier, la baignoire, ou le bac ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "chrome,eau",
        "emphasis": "évier",
        "passage": [
            "narrateur|Ils s'approchent de l'évier, étroit.",
            "enfant-f|Vous entrez, toutes les deux.",
            "narrateur|Elle les pose d'un même geste.",
            "narrateur|Le coton bute contre le chrome.",
            "narrateur|Le bois file vers le trou.",
            "enfant-f|L'une reste, l'autre part.",
            "narrateur|Le bouton de lavande s'enfonce, caché.",
            "narrateur|Chouchou veut les pousser, plus fort.",
            "narrateur|Ses mains s'arrêtent, au-dessus de l'eau.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu fais comment, avec les deux ?",
            "narrateur|Le savon perle sur le chrome.",
        ],
    },
    (2, 1): {
        "sons": "chrome,plastique",
        "emphasis": "évier",
        "passage": [
            "narrateur|Le gobelet cogne le métal, un toc.",
            "narrateur|Ils s'approchent de l'évier, étroit.",
            "enfant-f|Un bain, ici.",
            "narrateur|Elle verse d'un même geste.",
            "narrateur|Le coton bute, trop rond.",
            "narrateur|Le bois glisse, trop mince.",
            "enfant-f|L'une reste, l'autre part.",
            "narrateur|Le bouton de lavande disparaît, un instant.",
            "narrateur|Chouchou lève le gobelet, trop vite.",
            "narrateur|Puis elle le baisse.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu fais comment, avec les deux ?",
            "narrateur|Une goutte tremble au bord du gobelet.",
        ],
    },
    (3, 1): {
        "sons": "chrome,linge",
        "emphasis": "évier",
        "passage": [
            "narrateur|La serviette accroche le robinet, puis lâche.",
            "narrateur|Ils s'approchent de l'évier, étroit.",
            "enfant-f|Vous entrez, sous le linge.",
            "narrateur|Elle les pousse d'un même geste.",
            "narrateur|Le coton bute contre le rebord.",
            "narrateur|Le bois file vers le trou.",
            "enfant-f|Ça ne tient pas.",
            "narrateur|Le bouton de lavande s'enfonce, caché.",
            "narrateur|Chouchou veut tout recouvrir, trop vite.",
            "narrateur|Ses mains s'arrêtent, au-dessus.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu fais comment, avec les deux ?",
            "narrateur|Un coin de linge traîne dans l'eau.",
        ],
    },
    (1, 2): {
        "sons": "baignoire,eau",
        "emphasis": "baignoire",
        "passage": [
            "narrateur|Dans la baignoire, l'eau est haute.",
            "enfant-f|C'est une mer, ici.",
            "narrateur|Elle pousse le coton vers l'eau.",
            "narrateur|Le ventre rond flotte, trop loin.",
            "narrateur|Le bois, lui, glisse au fond.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|Un peu de savon perle sur l'eau.",
            "narrateur|Le bouton de lavande s'éloigne, sur l'eau.",
            "narrateur|Chouchou veut tout plonger, trop vite.",
            "narrateur|Ses mains s'arrêtent, au bord.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu les gardes comment, ensemble ?",
            "narrateur|Le savon fait un rond, à la surface.",
        ],
    },
    (2, 2): {
        "sons": "baignoire,plastique",
        "emphasis": "baignoire",
        "passage": [
            "narrateur|Dans la baignoire, l'eau est haute.",
            "enfant-f|C'est une mer, ici.",
            "narrateur|Le gobelet flotte un instant, léger.",
            "narrateur|Elle pousse les deux, d'un coup.",
            "narrateur|Le coton part trop loin.",
            "narrateur|Le bois coule, trop mince.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|Le bouton de lavande dérive, au milieu.",
            "narrateur|Chouchou lève le gobelet, trop plein.",
            "narrateur|Puis elle le retient.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu les gardes comment, ensemble ?",
            "narrateur|Une goutte tombe du gobelet, trop penché.",
        ],
    },
    (3, 2): {
        "sons": "baignoire,linge",
        "emphasis": "baignoire",
        "passage": [
            "narrateur|Dans la baignoire, l'eau est haute.",
            "enfant-f|C'est une mer, ici.",
            "narrateur|La serviette tombe, trop large, trop lourde.",
            "narrateur|Elle pousse les deux, d'un coup.",
            "narrateur|Le coton flotte, emporté.",
            "narrateur|Le bois glisse au fond.",
            "enfant-f|Ce n'est pas juste.",
            "narrateur|Le bouton de lavande s'éloigne, mouillé.",
            "narrateur|Chouchou veut tout envelopper, trop vite.",
            "narrateur|Ses mains s'arrêtent, au bord.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu les gardes comment, ensemble ?",
            "narrateur|Le linge se gonfle, comme un nuage.",
        ],
    },
    (1, 3): {
        "sons": "vent,terre",
        "emphasis": "bac",
        "passage": [
            "narrateur|Dehors, le bac du jardin sent la terre.",
            "enfant-f|Le bain, ici.",
            "narrateur|Un vent passe, froid.",
            "narrateur|Elle pose les deux, d'un même geste.",
            "narrateur|Le bois tombe, trop léger.",
            "narrateur|Le coton reste, trop lourd, trop rond.",
            "enfant-f|Elle est tombée !",
            "narrateur|Dehors, le savon sent la lavande.",
            "narrateur|Le bouton de lavande penche, presque parti.",
            "narrateur|Chouchou veut tout rattraper, trop vite.",
            "narrateur|Ses mains s'arrêtent, au-dessus du bac.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu les rassembles comment ?",
            "narrateur|Un grain de savon roule dans l'herbe.",
        ],
    },
    (2, 3): {
        "sons": "vent,plastique",
        "emphasis": "bac",
        "passage": [
            "narrateur|Dehors, le bac du jardin sent la terre.",
            "enfant-f|Le bain, ici.",
            "narrateur|Une goutte tombe du gobelet, trop penché.",
            "narrateur|Elle pose les deux, d'un même geste.",
            "narrateur|Le bois tombe, trop léger.",
            "narrateur|Le coton reste, trop lourd.",
            "enfant-f|Elle est tombée !",
            "narrateur|Le bouton de lavande penche, presque parti.",
            "narrateur|Chouchou veut verser, trop vite.",
            "narrateur|Puis elle retient le gobelet.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à sa hauteur.",
            "maman|Tu les rassembles comment ?",
            "narrateur|Le vent fait tinter le plastique.",
        ],
    },
    (3, 3): {
        "sons": "vent,linge",
        "emphasis": "bac",
        "passage": [
            "narrateur|Dehors, le bac du jardin sent la terre.",
            "enfant-f|Le bain, ici.",
            "narrateur|La serviette se gonfle, comme un nuage.",
            "narrateur|Elle pose les deux, d'un même geste.",
            "narrateur|Le bois tombe, trop léger.",
            "narrateur|Le coton reste, trop lourd.",
            "enfant-f|Elle est tombée !",
            "narrateur|Le bouton de lavande penche, presque parti.",
            "narrateur|Chouchou veut tout envelopper, trop vite.",
            "narrateur|Ses mains s'arrêtent, au-dessus du bac.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu les rassembles comment ?",
            "narrateur|Le linge claque, pris par le vent.",
        ],
    },
}

T3_LABS = {
    1: ("deux places", "moins d'eau", "la bassine"),
    2: ("le tapis", "le bord", "verser"),
    3: ("le rebord", "la serviette", "l'auvent"),
}

T3_CHOICE = {
    1: [
        "narrateur|Dans l'évier, le coton bute.",
        "narrateur|Le bois glisse vers le trou.",
        "narrateur|Le bouton de lavande reste caché, un instant.",
        "papa|Tu fais quoi, Chouchou ?",
    ],
    2: [
        "narrateur|Dans la baignoire, l'eau est trop haute.",
        "narrateur|Le coton flotte trop loin.",
        "narrateur|Le bouton de lavande dérive, au milieu.",
        "maman|Tu fais quoi, avec elles ?",
    ],
    3: [
        "narrateur|Dans le bac, le bois est tombé.",
        "narrateur|Le coton reste, trop lourd.",
        "narrateur|Le bouton de lavande penche, presque parti.",
        "papa|Tu fais quoi, maintenant ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "enfant-f|Deux places, dans l'évier.",
        "narrateur|Elle pose le savon au milieu.",
        "narrateur|Un mur de savon, mince.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "enfant-f|Je regarde.",
        "narrateur|Le bouton de lavande réapparaît, rond.",
        "enfant-f|Toi ici, toi là.",
        "narrateur|Le coton s'assoit d'un côté.",
        "narrateur|Le bois s'assoit de l'autre.",
        "papa|Deux places, deux formes.",
        "maman|Elles se baignent, chacune.",
        "narrateur|Un peu de savon reste sur le coton.",
    ],
    (1, 1, 2): [
        "enfant-f|Moins d'eau.",
        "narrateur|Elle ferme un peu le robinet.",
        "narrateur|Le rond devient une flaque, basse.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|Le bouton de lavande réapparaît, au fond.",
        "narrateur|Le coton pose le ventre, sans coincer.",
        "narrateur|Le bois reste, sans glisser.",
        "enfant-f|Vous tenez, toutes les deux.",
        "maman|Le bouton est là, au fond.",
        "papa|L'évier les tient, maintenant.",
        "narrateur|Un filet de savon s'arrête, bas.",
    ],
    (1, 1, 3): [
        "enfant-f|La bassine, dedans.",
        "narrateur|Maman glisse une bassine dans l'évier.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Je regarde d'abord.",
        "narrateur|Le bouton de lavande luit, au ventre.",
        "narrateur|Le coton et le bois montent ensemble.",
        "enfant-f|Un bain, plus large.",
        "papa|Le trou reste en dessous, seul.",
        "maman|Elles se touchent, les deux.",
        "narrateur|Un filet tombe, puis s'arrête.",
        "narrateur|Un rond de savon reste au bord.",
    ],
    (1, 2, 1): [
        "enfant-f|Le tapis, comme une île.",
        "narrateur|Elle pose le tapis de bain, rêche.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Je regarde le bouton.",
        "narrateur|Le bouton de lavande brille, au ventre.",
        "narrateur|Le coton s'assoit dessus, trop rond.",
        "narrateur|Le bois s'allonge contre lui, trop mince.",
        "enfant-f|Vous avez le fond, toutes les deux.",
        "papa|Chacun a sa place.",
        "maman|L'eau passe autour, plus lente.",
        "narrateur|Un peu de savon perle sur le tapis.",
    ],
    (1, 2, 2): [
        "enfant-f|Le bord, pas le fond.",
        "narrateur|Elle les pose au bout, où l'eau est basse.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|Le bouton de lavande reste collé, rond.",
        "narrateur|Le coton tient, le bois aussi.",
        "enfant-f|Vous tenez, sans couler.",
        "papa|Le bord était assez large.",
        "maman|Lui, trop mince, reste près.",
        "narrateur|Une vague minuscule, puis plus.",
        "narrateur|Un rond de savon sèche au bord.",
    ],
    (1, 2, 3): [
        "enfant-f|Verser, juste un peu.",
        "narrateur|Elle arrose le coton, puis le bois.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Pas toute la mer.",
        "narrateur|Le bouton de lavande luit, mouillé.",
        "enfant-f|Vous avez de l'eau, toutes les deux.",
        "papa|Pas besoin du grand bain.",
        "maman|Tes mains ont fait la pluie.",
        "narrateur|Le savon attend sur le rebord.",
        "narrateur|Deux gouttes restent sur le coton.",
    ],
    (1, 3, 1): [
        "enfant-f|Le rebord, pour tous.",
        "narrateur|Elle les assied sur le bord du bac.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Je regarde.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Le coton tient, trop large, trop rond.",
        "narrateur|Le bois tient, une jambe dans le vide.",
        "enfant-f|Vous vous baignez ici, sans tomber.",
        "papa|Le bord a deux places, maintenant.",
        "maman|Plus besoin du vent.",
        "narrateur|Un grain de savon sèche sur le rebord.",
    ],
    (1, 3, 2): [
        "enfant-f|La serviette, contre le vent.",
        "narrateur|Elle les enveloppe, savon contre le linge.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends le vent.",
        "narrateur|Le bouton de lavande reste au chaud.",
        "narrateur|Le tissu tient, même si ça souffle.",
        "enfant-f|Vous avez chaud, toutes les deux.",
        "papa|Le vent prend le linge, pas elles.",
        "maman|Tête contre tête.",
        "narrateur|Un peu de savon reste au pli.",
    ],
    (1, 3, 3): [
        "enfant-f|Sous l'auvent, plus à l'abri.",
        "narrateur|Elle porte les deux, le savon contre elle.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|On rentre un peu.",
        "narrateur|Le bouton de lavande luit, à l'abri.",
        "narrateur|Le vent reste dehors, dans le bac.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Rentrer un peu, c'était plus simple.",
        "maman|La terre sent, plus loin.",
        "narrateur|Un rond de savon sèche sous l'auvent.",
    ],
    (2, 1, 1): [
        "enfant-f|Deux places, dans l'évier.",
        "narrateur|Elle pose le gobelet au milieu.",
        "narrateur|Un mur de plastique, bleu.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "enfant-f|Je regarde.",
        "narrateur|Le bouton de lavande réapparaît, rond.",
        "enfant-f|Toi ici, toi là.",
        "narrateur|Le coton s'assoit d'un côté.",
        "narrateur|Le bois s'assoit de l'autre.",
        "papa|Deux places, deux formes.",
        "maman|Elles se baignent, chacune.",
        "narrateur|Le gobelet verse un filet, fin.",
    ],
    (2, 1, 2): [
        "enfant-f|Moins d'eau.",
        "narrateur|Elle verse moins, avec le gobelet.",
        "narrateur|La flaque devient basse, nette.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|Le bouton de lavande réapparaît, au fond.",
        "narrateur|Le coton pose le ventre, sans coincer.",
        "narrateur|Le bois reste, sans glisser.",
        "enfant-f|Vous tenez, toutes les deux.",
        "maman|Le bouton est là, au fond.",
        "papa|L'évier les tient, maintenant.",
        "narrateur|Une goutte reste au fond du gobelet.",
    ],
    (2, 1, 3): [
        "enfant-f|La bassine, dedans.",
        "narrateur|Maman glisse une bassine dans l'évier.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Je verse après.",
        "narrateur|Le bouton de lavande luit, au ventre.",
        "narrateur|Le coton et le bois montent ensemble.",
        "enfant-f|Un bain, plus large.",
        "papa|Le trou reste en dessous, seul.",
        "maman|Elles se touchent, les deux.",
        "narrateur|Le gobelet claque, un toc léger.",
        "narrateur|Un filet bleu tremble au bord.",
    ],
    (2, 2, 1): [
        "enfant-f|Le tapis, comme une île.",
        "narrateur|Elle pose le tapis de bain, rêche.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Je verse après, pas maintenant.",
        "narrateur|Le bouton de lavande brille, au ventre.",
        "narrateur|Le coton s'assoit dessus, trop rond.",
        "narrateur|Le bois s'allonge contre lui, trop mince.",
        "enfant-f|Vous avez le fond, toutes les deux.",
        "papa|Chacun a sa place.",
        "maman|L'eau passe autour, plus lente.",
        "narrateur|Le gobelet repose sur le tapis.",
    ],
    (2, 2, 2): [
        "enfant-f|Le bord, pas le fond.",
        "narrateur|Elle les pose au bout, où l'eau est basse.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|Le bouton de lavande reste collé, rond.",
        "narrateur|Le coton tient, le bois aussi.",
        "enfant-f|Vous tenez, sans couler.",
        "papa|Le bord était assez large.",
        "maman|Lui, trop mince, reste près.",
        "narrateur|Le gobelet penche, puis se tient.",
        "narrateur|Une vague minuscule s'arrête au bord.",
    ],
    (2, 2, 3): [
        "enfant-f|Verser, juste un peu.",
        "narrateur|Le gobelet arrose le coton, puis le bois.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Pas toute la mer.",
        "narrateur|Le bouton de lavande luit, mouillé.",
        "enfant-f|Vous avez de l'eau, toutes les deux.",
        "papa|Pas besoin du grand bain.",
        "maman|Tes mains ont fait la pluie.",
        "narrateur|Le gobelet se vide, presque.",
        "narrateur|Deux gouttes restent au plastique.",
    ],
    (2, 3, 1): [
        "enfant-f|Le rebord, pour tous.",
        "narrateur|Elle les assied sur le bord du bac.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Je verse après.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Le coton tient, trop large, trop rond.",
        "narrateur|Le bois tient, une jambe dans le vide.",
        "enfant-f|Vous vous baignez ici, sans tomber.",
        "papa|Le bord a deux places, maintenant.",
        "maman|Plus besoin du vent.",
        "narrateur|Le gobelet tient entre les deux.",
    ],
    (2, 3, 2): [
        "enfant-f|La serviette, contre le vent.",
        "narrateur|Elle les enveloppe, gobelet contre le linge.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends le vent.",
        "narrateur|Le bouton de lavande reste au chaud.",
        "narrateur|Le tissu tient, même si ça souffle.",
        "enfant-f|Vous avez chaud, toutes les deux.",
        "papa|Le vent prend le linge, pas elles.",
        "maman|Tête contre tête.",
        "narrateur|Le gobelet chauffe sous le linge.",
    ],
    (2, 3, 3): [
        "enfant-f|Sous l'auvent, plus à l'abri.",
        "narrateur|Elle porte les deux, le gobelet contre elle.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|On rentre un peu.",
        "narrateur|Le bouton de lavande luit, à l'abri.",
        "narrateur|Le vent reste dehors, dans le bac.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Rentrer un peu, c'était plus simple.",
        "maman|La terre sent, plus loin.",
        "narrateur|Une goutte tombe de l'auvent, seule.",
    ],
    (3, 1, 1): [
        "enfant-f|Deux places, dans l'évier.",
        "narrateur|Elle pose la serviette au milieu.",
        "narrateur|Un pli de linge, comme un mur.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "enfant-f|Je regarde.",
        "narrateur|Le bouton de lavande réapparaît, rond.",
        "enfant-f|Toi ici, toi là.",
        "narrateur|Le coton s'assoit d'un côté.",
        "narrateur|Le bois s'assoit de l'autre.",
        "papa|Deux places, deux formes.",
        "maman|Elles se baignent, chacune.",
        "narrateur|Un fil de linge reste au chrome.",
    ],
    (3, 1, 2): [
        "enfant-f|Moins d'eau.",
        "narrateur|Elle ferme un peu le robinet.",
        "narrateur|La flaque devient basse, nette.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|Le bouton de lavande réapparaît, au fond.",
        "narrateur|Le coton pose le ventre, sans coincer.",
        "narrateur|Le bois reste, sans glisser.",
        "enfant-f|Vous tenez, toutes les deux.",
        "maman|Le bouton est là, au fond.",
        "papa|L'évier les tient, maintenant.",
        "narrateur|La serviette garde un pli, tiède.",
    ],
    (3, 1, 3): [
        "enfant-f|La bassine, dedans.",
        "narrateur|Maman glisse une bassine dans l'évier.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Je recouvre après.",
        "narrateur|Le bouton de lavande luit, au ventre.",
        "narrateur|Le coton et le bois montent ensemble.",
        "enfant-f|Un bain, plus large.",
        "papa|Le trou reste en dessous, seul.",
        "maman|Elles se touchent, les deux.",
        "narrateur|La bassine disparaît sous le linge.",
        "narrateur|Un coin de serviette sèche au bord.",
    ],
    (3, 2, 1): [
        "enfant-f|Le tapis, comme une île.",
        "narrateur|Elle pose le tapis de bain, rêche.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Le linge, après.",
        "narrateur|Le bouton de lavande brille, au ventre.",
        "narrateur|Le coton s'assoit dessus, trop rond.",
        "narrateur|Le bois s'allonge contre lui, trop mince.",
        "enfant-f|Vous avez le fond, toutes les deux.",
        "papa|Chacun a sa place.",
        "maman|L'eau passe autour, plus lente.",
        "narrateur|Le tapis et le linge se touchent.",
    ],
    (3, 2, 2): [
        "enfant-f|Le bord, pas le fond.",
        "narrateur|Elle les pose au bout, où l'eau est basse.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends.",
        "narrateur|Le bouton de lavande reste collé, rond.",
        "narrateur|Le coton tient, le bois aussi.",
        "enfant-f|Vous tenez, sans couler.",
        "papa|Le bord était assez large.",
        "maman|Lui, trop mince, reste près.",
        "narrateur|Un coin de serviette sèche au bord.",
        "narrateur|Le linge garde deux formes, nettes.",
    ],
    (3, 2, 3): [
        "enfant-f|Verser, juste un peu.",
        "narrateur|Sous la serviette, elle arrose les deux.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Pas toute la mer.",
        "narrateur|Le bouton de lavande luit, mouillé.",
        "enfant-f|Vous avez de l'eau, toutes les deux.",
        "papa|Pas besoin du grand bain.",
        "maman|Tes mains ont fait la pluie.",
        "narrateur|La serviette se lourde, un peu.",
        "narrateur|Deux gouttes restent au linge.",
    ],
    (3, 3, 1): [
        "enfant-f|Le rebord, pour tous.",
        "narrateur|Elle les assied sur le bord du bac.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Le linge, après.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Le coton tient, trop large, trop rond.",
        "narrateur|Le bois tient, une jambe dans le vide.",
        "enfant-f|Vous vous baignez ici, sans tomber.",
        "papa|Le bord a deux places, maintenant.",
        "maman|Plus besoin du vent.",
        "narrateur|Une feuille colle au rebord du bac.",
    ],
    (3, 3, 2): [
        "enfant-f|La serviette, contre le vent.",
        "narrateur|Elle les enveloppe, coton contre bois.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|Attends le vent.",
        "narrateur|Le bouton de lavande reste au chaud.",
        "narrateur|Le tissu tient, même si ça souffle.",
        "enfant-f|Vous avez chaud, toutes les deux.",
        "papa|Le vent prend le linge, pas elles.",
        "maman|Tête contre tête.",
        "narrateur|La serviette sent la terre, un peu.",
    ],
    (3, 3, 3): [
        "enfant-f|Sous l'auvent, plus à l'abri.",
        "narrateur|Elle porte les deux, la serviette autour.",
        "narrateur|Chouchou refuse de foncer.",
        "enfant-f|On rentre un peu.",
        "narrateur|Le bouton de lavande luit, à l'abri.",
        "narrateur|Le vent reste dehors, dans le bac.",
        "enfant-f|Vous avez la place, à l'abri.",
        "papa|Rentrer un peu, c'était plus simple.",
        "maman|La terre sent, plus loin.",
        "narrateur|L'auvent s'égoutte sur le linge.",
    ],
}

T3_SONS = {
    (1, 1): "chrome,savon",
    (1, 2): "robinet,eau",
    (1, 3): "bassine,eau",
    (2, 1): "tapis,eau",
    (2, 2): "bord,eau",
    (2, 3): "verser,eau",
    (3, 1): "rebord,terre",
    (3, 2): "linge,vent",
    (3, 3): "auvent,goutte",
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Deux ronds d'eau restent dans l'évier.",
        "enfant-f|Vous avez eu votre bain.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Ça a failli rater.",
        "papa|Tes mains ont fait les deux places.",
        "maman|Elles sont ensemble, quand même.",
        "enfant-f|On reste un peu.",
        "narrateur|Le chrome garde deux ronds d'eau.",
    ],
    (1, 1, 2): [
        "narrateur|La flaque basse sent la lavande.",
        "enfant-f|Vous teniez, toutes les deux.",
        "narrateur|Le bouton de lavande brille, au fond.",
        "narrateur|Un instant, le bois partait.",
        "papa|L'évier les a tenues.",
        "maman|Elles sont propres, chacune.",
        "enfant-f|On rentre, maintenant.",
        "narrateur|Un filet bas s'arrête au fond.",
    ],
    (1, 1, 3): [
        "narrateur|Dans la bassine, l'eau tremble.",
        "enfant-f|Un bain, plus large.",
        "narrateur|Le bouton de lavande luit, au ventre.",
        "narrateur|Le trou n'a pas gagné.",
        "papa|Tes mains ont mis la bassine.",
        "maman|Elles se touchent, les deux.",
        "enfant-f|Une goutte, pour rire.",
        "narrateur|La bassine tient une odeur rose.",
    ],
    (1, 2, 1): [
        "narrateur|Le tapis de bain garde deux traces.",
        "enfant-f|Vous aviez votre île.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Ça a failli flotter trop loin.",
        "papa|Chacun avait sa place.",
        "maman|L'eau passait autour.",
        "enfant-f|On les essuie.",
        "narrateur|Le tapis de bain a deux traces.",
    ],
    (1, 2, 2): [
        "narrateur|Au bout, le bord reste mouillé.",
        "enfant-f|Vous teniez, sans couler.",
        "narrateur|Le bouton de lavande sèche, au ventre.",
        "narrateur|Un instant, le bois coulait.",
        "papa|Le bord était assez large.",
        "maman|Deux silhouettes, une même eau.",
        "enfant-f|Le dîner, après ?",
        "narrateur|Un rai d'eau reste sur le bord.",
    ],
    (1, 2, 3): [
        "narrateur|Un filet d'eau a marqué le coton.",
        "enfant-f|Vous avez eu la pluie.",
        "narrateur|Le bouton de lavande luit, mouillé.",
        "narrateur|La mer n'était pas nécessaire.",
        "papa|Pas besoin du grand bain.",
        "maman|Tes mains ont versé.",
        "enfant-f|On est arrivés.",
        "narrateur|Un rond de savon sèche au tapis.",
    ],
    (1, 3, 1): [
        "narrateur|Sur le bac, deux ronds restent.",
        "enfant-f|On s'est baignées ici, sans tomber.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Un instant, le bois tombait.",
        "papa|Le bord avait deux places.",
        "maman|Plus besoin du vent.",
        "enfant-f|On reste un peu.",
        "narrateur|L'herbe se recouche contre le bac.",
    ],
    (1, 3, 2): [
        "narrateur|Sous le linge, ça sent la terre.",
        "enfant-f|Vous aviez chaud, toutes les deux.",
        "narrateur|Le bouton de lavande reste au chaud.",
        "narrateur|Le vent a failli les prendre.",
        "papa|Le vent a pris le linge, pas elles.",
        "maman|Tête contre tête.",
        "enfant-f|On rentre, maintenant.",
        "narrateur|Un pli de savon reste au linge.",
    ],
    (1, 3, 3): [
        "narrateur|Sous l'auvent, l'air est plus simple.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|Le bouton de lavande luit, à l'abri.",
        "narrateur|Dehors, le bac reste trop venteux.",
        "papa|Rentrer un peu, c'était plus simple.",
        "maman|La terre sent, plus loin.",
        "enfant-f|Le bain est fini, pour de vrai.",
        "narrateur|L'auvent goutte, puis se tait.",
    ],
    (2, 1, 1): [
        "narrateur|Deux ronds d'eau restent dans l'évier.",
        "enfant-f|Vous avez eu votre bain.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Ça a failli rater.",
        "papa|Tes mains ont fait les deux places.",
        "maman|Elles sont ensemble, quand même.",
        "enfant-f|On reste un peu.",
        "narrateur|Une goutte bleue tremble au chrome.",
    ],
    (2, 1, 2): [
        "narrateur|La flaque basse sent la lavande.",
        "enfant-f|Vous teniez, toutes les deux.",
        "narrateur|Le bouton de lavande brille, au fond.",
        "narrateur|Un instant, le bois partait.",
        "papa|L'évier les a tenues.",
        "maman|Elles sont propres, chacune.",
        "enfant-f|On rentre, maintenant.",
        "narrateur|Le gobelet garde un filet, au fond.",
    ],
    (2, 1, 3): [
        "narrateur|Dans la bassine, l'eau tremble.",
        "enfant-f|Un bain, plus large.",
        "narrateur|Le bouton de lavande luit, au ventre.",
        "narrateur|Le trou n'a pas gagné.",
        "papa|Tes mains ont mis la bassine.",
        "maman|Elles se touchent, les deux.",
        "enfant-f|Une goutte, pour rire.",
        "narrateur|La bassine claque, un toc léger.",
    ],
    (2, 2, 1): [
        "narrateur|Le tapis de bain garde deux traces.",
        "enfant-f|Vous aviez votre île.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Ça a failli flotter trop loin.",
        "papa|Chacun avait sa place.",
        "maman|L'eau passait autour.",
        "enfant-f|On les essuie.",
        "narrateur|Le gobelet repose sur le tapis.",
    ],
    (2, 2, 2): [
        "narrateur|Au bout, le bord reste mouillé.",
        "enfant-f|Vous teniez, sans couler.",
        "narrateur|Le bouton de lavande sèche, au ventre.",
        "narrateur|Un instant, le bois coulait.",
        "papa|Le bord était assez large.",
        "maman|Deux silhouettes, une même eau.",
        "enfant-f|Le dîner, après ?",
        "narrateur|Une vague minuscule s'arrête au bord.",
    ],
    (2, 2, 3): [
        "narrateur|Un filet d'eau a marqué le coton.",
        "enfant-f|Vous avez eu la pluie.",
        "narrateur|Le bouton de lavande luit, mouillé.",
        "narrateur|La mer n'était pas nécessaire.",
        "papa|Pas besoin du grand bain.",
        "maman|Tes mains ont versé.",
        "enfant-f|On est arrivés.",
        "narrateur|Une goutte sèche au fond du gobelet.",
    ],
    (2, 3, 1): [
        "narrateur|Sur le bac, deux ronds restent.",
        "enfant-f|On s'est baignées ici, sans tomber.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Un instant, le bois tombait.",
        "papa|Le bord avait deux places.",
        "maman|Plus besoin du vent.",
        "enfant-f|On reste un peu.",
        "narrateur|Une feuille s'arrête contre le pas.",
    ],
    (2, 3, 2): [
        "narrateur|Sous le linge, ça sent la terre.",
        "enfant-f|Vous aviez chaud, toutes les deux.",
        "narrateur|Le bouton de lavande reste au chaud.",
        "narrateur|Le vent a failli les prendre.",
        "papa|Le vent a pris le linge, pas elles.",
        "maman|Tête contre tête.",
        "enfant-f|On rentre, maintenant.",
        "narrateur|Le gobelet chauffe sous le linge.",
    ],
    (2, 3, 3): [
        "narrateur|Sous l'auvent, l'air est plus simple.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|Le bouton de lavande luit, à l'abri.",
        "narrateur|Dehors, le bac reste trop venteux.",
        "papa|Rentrer un peu, c'était plus simple.",
        "maman|La terre sent, plus loin.",
        "enfant-f|Le bain est fini, pour de vrai.",
        "narrateur|Une goutte tombe de l'auvent, seule.",
    ],
    (3, 1, 1): [
        "narrateur|Deux ronds d'eau restent dans l'évier.",
        "enfant-f|Vous avez eu votre bain.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Ça a failli rater.",
        "papa|Tes mains ont fait les deux places.",
        "maman|Elles sont ensemble, quand même.",
        "enfant-f|On reste un peu.",
        "narrateur|Un fil de linge reste au chrome.",
    ],
    (3, 1, 2): [
        "narrateur|La flaque basse sent la lavande.",
        "enfant-f|Vous teniez, toutes les deux.",
        "narrateur|Le bouton de lavande brille, au fond.",
        "narrateur|Un instant, le bois partait.",
        "papa|L'évier les a tenues.",
        "maman|Elles sont propres, chacune.",
        "enfant-f|On rentre, maintenant.",
        "narrateur|La serviette garde un pli tiède.",
    ],
    (3, 1, 3): [
        "narrateur|Dans la bassine, l'eau tremble.",
        "enfant-f|Un bain, plus large.",
        "narrateur|Le bouton de lavande luit, au ventre.",
        "narrateur|Le trou n'a pas gagné.",
        "papa|Tes mains ont mis la bassine.",
        "maman|Elles se touchent, les deux.",
        "enfant-f|Une goutte, pour rire.",
        "narrateur|La bassine disparaît sous le linge.",
    ],
    (3, 2, 1): [
        "narrateur|Le tapis de bain garde deux traces.",
        "enfant-f|Vous aviez votre île.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Ça a failli flotter trop loin.",
        "papa|Chacun avait sa place.",
        "maman|L'eau passait autour.",
        "enfant-f|On les essuie.",
        "narrateur|Le tapis et le linge se touchent.",
    ],
    (3, 2, 2): [
        "narrateur|Au bout, le bord reste mouillé.",
        "enfant-f|Vous teniez, sans couler.",
        "narrateur|Le bouton de lavande sèche, au ventre.",
        "narrateur|Un instant, le bois coulait.",
        "papa|Le bord était assez large.",
        "maman|Deux silhouettes, une même eau.",
        "enfant-f|Le dîner, après ?",
        "narrateur|Un coin de serviette sèche au bord.",
    ],
    (3, 2, 3): [
        "narrateur|Un filet d'eau a marqué le coton.",
        "enfant-f|Vous avez eu la pluie.",
        "narrateur|Le bouton de lavande luit, mouillé.",
        "narrateur|La mer n'était pas nécessaire.",
        "papa|Pas besoin du grand bain.",
        "maman|Tes mains ont versé.",
        "enfant-f|On est arrivés.",
        "narrateur|La serviette redevient plate, rêche.",
    ],
    (3, 3, 1): [
        "narrateur|Sur le bac, deux ronds restent.",
        "enfant-f|On s'est baignées ici, sans tomber.",
        "narrateur|Le bouton de lavande tient, au ventre.",
        "narrateur|Un instant, le bois tombait.",
        "papa|Le bord avait deux places.",
        "maman|Plus besoin du vent.",
        "enfant-f|On reste un peu.",
        "narrateur|Une feuille colle au rebord du bac.",
    ],
    (3, 3, 2): [
        "narrateur|Sous le linge, ça sent la terre.",
        "enfant-f|Vous aviez chaud, toutes les deux.",
        "narrateur|Le bouton de lavande reste au chaud.",
        "narrateur|Le vent a failli les prendre.",
        "papa|Le vent a pris le linge, pas elles.",
        "maman|Tête contre tête.",
        "enfant-f|On rentre, maintenant.",
        "narrateur|La serviette sent la terre, un peu.",
    ],
    (3, 3, 3): [
        "narrateur|Sous l'auvent, l'air est plus simple.",
        "enfant-f|Vous aviez la place, à l'abri.",
        "narrateur|Le bouton de lavande luit, à l'abri.",
        "narrateur|Dehors, le bac reste trop venteux.",
        "papa|Rentrer un peu, c'était plus simple.",
        "maman|La terre sent, plus loin.",
        "enfant-f|Le bain est fini, pour de vrai.",
        "narrateur|L'auvent s'égoutte sur le linge.",
    ],
}

END_SONS = {1: "savon,eau", 2: "gobelet,eau", 3: "linge,eau"}
T3_EMPH = {
    1: {1: "deux places", 2: "flaque", 3: "bassine"},
    2: {1: "tapis", 2: "bord", 3: "verser"},
    3: {1: "rebord", 2: "serviette", 3: "auvent"},
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "goutte,robinet",
        {"emphasis": "bouton de lavande"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le savon", "le gobelet", "la serviette")},
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
            {"emphasis": "bouton de lavande"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("l'évier", "la baignoire", "le bac")},
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
                    {"emphasis": "bouton de lavande"},
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
        "grand-père",
        "maîtresse",
        "jardinier",
        "merle",
        "miel",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    if "bouton de lavande" not in blob:
        raise SystemExit(f"{SID}: bouton de lavande absent")
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
    if any(c["text_xai_tags"] == c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-035 — Les deux poupées de Chouchou dans le bain\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.COR.002 — deux corps, deux places (vécue : coton rond / bois mince, "
        "même geste raté, une place pour chacune)\n"
        "- **Personnages :** Chouchou, papa, maman (un seul enfant)\n"
        "- **Lieu :** salle de bain après la pluie, rebord du robinet, puis le bac du jardin\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Chouchou connaît la salle de bain. Après la pluie, un détail paraît neuf : "
        "un **bouton de lavande** colle au ventre de la poupée de coton. "
        "Mission : un vrai bain pour les deux, coton rond et bois mince. "
        "Elle ouvre le robinet, les pousse d'un même geste : le coton bute, le bois glisse. "
        "Savon, gobelet ou serviette : les trois partent. "
        "Évier trop étroit, baignoire trop haute, bac trop venteux. "
        "Elle refuse de foncer. Le bouton du début revient. "
        "Deux places, moins d'eau, bassine ; tapis, bord, verser ; rebord, serviette, auvent. "
        "Les deux se baignent. L'objet porte une trace.\n\n"
        "## Vécu\n\n"
        "Le sourire disparaît. L'envie et l'inquiétude se bousculent. "
        "Papa ou maman s'accroupit à la même hauteur. Personne ne donne la réponse. "
        "Chouchou observe le bouton, écoute l'eau, invente une place pour chaque forme. "
        "La leçon se voit : on joue avec les deux, sans les forcer dans le même trou.\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Plus rond ou plus mince » / Sami / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (papa : les deux poupées sorties). Question d'adulte. Un « en ce moment ».\n"
        "- Indice unique : bouton de lavande (inventé, payé au climax). Pas de gabarit v2 collé.\n"
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
