#!/usr/bin/env python3
"""TREE-DIF-055 — La citronnade de Sarah, dans le pichet (N1, DIF.ENE.001, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-055"
N1 = 10
TITLE = "La citronnade de Sarah, dans le pichet"
FIL = (
    "Au comptoir du pichet, Sarah veut remplir le pichet bleu de citronnade, "
    "pendant que le soleil tient la vitre. Elle veut tout verser d'un coup. "
    "Un cristal de sucre brun tient au bord. Elle prend le citron, le sucrier "
    "ou le pichet ; les trois viennent. À la table le citron file, à l'évier "
    "le jus résiste, sur le tabouret ses pieds dansent. Elle refuse de foncer. "
    "Le cristal dit la dose. Le pichet se remplit."
)
CHARS = "Sarah, papa, maman"
SETTING = "la cuisine : table, évier, tabouret"
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
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "cristal de sucre brun",
        "note": "arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=sarah_veut_tout_verser_le_cristal_attend; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_tout_verser; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_objet_résiste_elle_refuse_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "cristal",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le_cristal_dit_la_dose; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "cristal de sucre brun",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_pichet_a_son_jaune_le_cristal_reste; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N1:
            raise SystemExit(f"{where} {n}>{N1}: {ph}")
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
    "narrateur|Le frigo frappe deux fois, trop ouvert.",
    "narrateur|Un air froid glisse sur les carreaux.",
    "narrateur|Le citron jaune a roulé contre le pichet.",
    "narrateur|Au bord bleu, un cristal de sucre brun tient.",
    "enfant-f|Il est collé, tout petit.",
    "papa|C'est du sucre d'avant, Sarah.",
    "maman|Le pichet est vide, lui.",
    "narrateur|Ça sent le toast, et le citron froid.",
    "narrateur|Sarah vit ici, avec papa et maman.",
    "narrateur|Le comptoir du pichet est un peu collant.",
    "enfant-f|Je veux la citronnade, dans le pichet.",
    "papa|Le soleil tient sur la vitre.",
    "maman|Avant qu'il parte, on verse ?",
    "enfant-f|Tout le sucre, tout le citron !",
    "narrateur|En ce moment, Sarah touche le cristal.",
    "papa|Merci, tu as vu le cristal.",
    "narrateur|Le sucrier blanc attend près du bois.",
    "maman|Tes pieds dansent, Sarah.",
]

T1_CHOICE = [
    "narrateur|Près de l'eau, trois affaires attendent.",
    "narrateur|Le citron, le sucrier, et le pichet.",
    "papa|Le citron, le sucrier, ou le pichet ?",
    "maman|Tu prends quoi d'abord, Sarah ?",
]

T1 = {
    1: {
        "lab": "le citron jaune",
        "sons": "citron,pichet",
        "emphasis": "citron jaune",
        "passage": [
            "narrateur|Sarah prend d'abord le citron jaune.",
            "enfant-f|Il est froid, tout rond.",
            "maman|Garde-le dans les mains, tout droit.",
            "narrateur|La peau sent le soleil, un peu.",
            "enfant-f|Je presse tout, maintenant !",
            "papa|Pas tout, Sarah.",
            "narrateur|Papa glisse le sucrier, tout près.",
            "narrateur|Maman pose le pichet contre son bras.",
            "narrateur|Citron, sucrier, pichet, contre elle.",
            "enfant-f|La citronnade va venir.",
            "narrateur|Ses pieds tapent le carreau, trop vite.",
            "papa|Le citron d'abord, tu l'as.",
            "maman|Les trois affaires sont avec toi.",
            "narrateur|Elle veut tout verser, trop fort.",
            "enfant-f|Vite, le pichet veut son jaune.",
        ],
        "question": [
            "narrateur|Sarah a pris le citron jaune.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "mains",
            "accepted_examples": "mains | les mains | dans les mains | ses mains",
            "retry_prompt": "Le citron est dans les mains.",
        },
        "confirm": [
            "enfant-f|Dans les mains.",
            "maman|Oui.",
            "narrateur|Le citron roule un peu, puis s'arrête.",
            "enfant-f|C'est mon soleil de cuisine.",
            "narrateur|Sarah le serre, le lâche, le reprend.",
            "narrateur|Un pied tape, puis l'autre, trop vite.",
            "maman|Tes pieds veulent le jus.",
            "papa|On pose tout ici ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le cristal brun tient au bord bleu.",
        ],
    },
    2: {
        "lab": "le sucrier blanc",
        "sons": "sucrier,grain",
        "emphasis": "sucrier blanc",
        "passage": [
            "narrateur|Sarah serre d'abord le sucrier blanc.",
            "enfant-f|Il gratte un peu, contre moi.",
            "papa|Tiens-le contre le ventre, tout chaud.",
            "narrateur|Un grain blanc tombe, tout petit.",
            "enfant-f|Je verse tout, maintenant !",
            "maman|Pas tout, Sarah.",
            "narrateur|Elle glisse le citron sous l'autre bras.",
            "narrateur|Papa pose le pichet contre sa hanche.",
            "narrateur|Le blanc, le jaune, et le bleu.",
            "enfant-f|Je veux le jus, tout jaune.",
            "narrateur|Un genou rebondit, puis l'autre.",
            "maman|Le sucrier d'abord, il est prêt.",
            "papa|Les trois affaires sont avec toi.",
            "narrateur|Elle secoue le sucrier, trop fort.",
            "enfant-f|Vite, le pichet veut son sucre.",
        ],
        "question": [
            "narrateur|Sarah a serré le sucrier blanc.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "ventre",
            "accepted_examples": "ventre | le ventre | contre le ventre | son ventre",
            "retry_prompt": "Le sucrier est contre le ventre.",
        },
        "confirm": [
            "enfant-f|Contre le ventre.",
            "papa|Oui.",
            "narrateur|Le couvercle du sucrier chatouille sa manche.",
            "enfant-f|C'est ma neige, pour le jus.",
            "narrateur|Sarah secoue, un nuage de grains.",
            "narrateur|Un grain blanc traîne par terre.",
            "maman|Ça sent le sucré, tout près.",
            "papa|Tes mains, sur le sucrier ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le cristal brun tient au bord bleu.",
        ],
    },
    3: {
        "lab": "le pichet bleu",
        "sons": "pichet,eau",
        "emphasis": "pichet bleu",
        "passage": [
            "narrateur|Sarah prend d'abord le pichet bleu.",
            "enfant-f|Il est lourd, par le bord.",
            "maman|Garde-le là, tout droit.",
            "narrateur|L'eau chante un peu, au fond.",
            "enfant-f|Je verse tout, maintenant !",
            "papa|Pas tout, Sarah.",
            "narrateur|Il glisse le citron contre elle.",
            "narrateur|Maman pose le sucrier sous son bras.",
            "narrateur|Le pichet avance, tout bleu, trop sage.",
            "enfant-f|Le pichet veut son jaune.",
            "narrateur|Ses talons frappent le carreau, trop vite.",
            "papa|Le pichet d'abord, il est pris.",
            "maman|Les trois affaires sont avec toi.",
            "narrateur|Elle penche le pichet, trop fort.",
            "enfant-f|Vite, je veux le jus.",
        ],
        "question": [
            "narrateur|Sarah a pris le pichet bleu.",
            "maman|Elle le tient par où ?",
        ],
        "qfields": {
            "expected_answer": "bord",
            "accepted_examples": "bord | le bord | par le bord | le pichet",
            "retry_prompt": "Le pichet est pris par le bord.",
        },
        "confirm": [
            "enfant-f|Par le bord.",
            "maman|Oui.",
            "narrateur|L'eau du pichet danse un peu.",
            "enfant-f|Ma citronnade habite dedans.",
            "narrateur|Sarah le penche, le redresse, trop vite.",
            "narrateur|Une perle frappe le carreau, toute ronde.",
            "maman|La cuisine est prête, devant.",
            "papa|On y va, tous les trois ?",
            "enfant-f|Oui.",
            "narrateur|Le cristal brun tient au bord bleu.",
        ],
    },
}


def t2_question(t1: int) -> list[str]:
    first = {
        1: "narrateur|Sarah roule le citron, trop vite.",
        2: "narrateur|Un grain de sucre saute, trop loin.",
        3: "narrateur|L'eau du pichet clapote, trop fort.",
    }[t1]
    return [
        first,
        "narrateur|Sur la table, la toile cirée brille.",
        "narrateur|À l'évier, l'eau attend.",
        "narrateur|Près du bois, le tabouret attend.",
        "papa|On verse où, Sarah ?",
    ]


T2 = {
    (1, 1): {
        "sons": "toile,citron",
        "emphasis": "citron",
        "passage": [
            "narrateur|Sarah pose le citron sur la toile cirée.",
            "enfant-f|Tout le jus, tout de suite !",
            "narrateur|Elle presse trop fort, trop vite.",
            "narrateur|Le citron file, comme une balle.",
            "enfant-f|Il part !",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça glisse trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle veut le rattraper, tout presser.",
            "narrateur|Le citron se cache sous le sucrier.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du pichet, le cristal brun luit.",
            "maman|Tu vois comment, Sarah ?",
            "narrateur|Sarah pose les mains, sans presser.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "eau,citron",
        "emphasis": "évier",
        "passage": [
            "narrateur|Sarah porte le citron vers l'eau.",
            "enfant-f|Ici, le jus va tomber !",
            "narrateur|Elle presse au-dessus du robinet, trop.",
            "narrateur|Le citron glisse, trop mouillé.",
            "enfant-f|Il file !",
            "narrateur|Sarah ne rit plus.",
            "narrateur|L'envie et la peur se bousculent, dans sa poitrine.",
            "maman|Ici, ça coule trop.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout presser, trop vite.",
            "narrateur|Une graine bloque le jus, au milieu.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le cristal brun luit, au bord bleu.",
            "papa|Tu vois comment, Sarah ?",
            "narrateur|Sarah tient le citron, sans presser.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "bois,citron",
        "emphasis": "tabouret",
        "passage": [
            "narrateur|Sarah grimpe, le citron contre elle.",
            "enfant-f|Ici, je suis grande, papa.",
            "narrateur|Le bois du tabouret rend chaque pas.",
            "narrateur|Le citron saute d'un genou, trop haut.",
            "enfant-f|Il tombe !",
            "narrateur|Son sourire s'en va.",
            "narrateur|Sa poitrine serre, trop vite.",
            "papa|Tes genoux font trop de vagues.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout verser, d'en haut.",
            "narrateur|Le citron refuse, trop loin des mains.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le cristal brun luit, trop bas.",
            "maman|Tu vois comment, Sarah ?",
            "narrateur|Sarah s'assoit, le citron au creux.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "toile,sucrier",
        "emphasis": "sucrier",
        "passage": [
            "narrateur|Sarah pose le sucrier sur la toile cirée.",
            "enfant-f|Tout le sucre, tout de suite !",
            "narrateur|Elle penche trop fort, trop vite.",
            "narrateur|Un nuage de grains saute, trop loin.",
            "enfant-f|Ça part !",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "maman|Ici, ça glisse trop.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout vider, d'un coup.",
            "narrateur|Le couvercle reste coincé, trop serré.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du pichet, le cristal brun luit.",
            "papa|Tu vois comment, Sarah ?",
            "narrateur|Sarah pose le sucrier, sans verser.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "eau,sucrier",
        "emphasis": "évier",
        "passage": [
            "narrateur|Sarah porte le sucrier vers l'eau.",
            "enfant-f|Ici, le sucre va fondre !",
            "narrateur|Elle penche au-dessus du robinet, trop.",
            "narrateur|L'eau emporte un grain, trop fort.",
            "enfant-f|Il part !",
            "narrateur|Sarah ne rit plus.",
            "narrateur|L'envie et la peur se bousculent, dans sa poitrine.",
            "papa|Ici, ça coule trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout verser, trop vite.",
            "narrateur|Le sucre se colle, trop mouillé.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le cristal brun luit, au bord bleu.",
            "maman|Tu vois comment, Sarah ?",
            "narrateur|Sarah tient le sucrier, sans verser.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "bois,sucrier",
        "emphasis": "tabouret",
        "passage": [
            "narrateur|Sarah grimpe, le sucrier contre elle.",
            "enfant-f|Ici, je suis grande, maman.",
            "narrateur|Le bois du tabouret rend chaque pas.",
            "narrateur|Le sucrier vacille, un grain s'envole.",
            "enfant-f|Il tombe !",
            "narrateur|Son sourire s'en va.",
            "narrateur|Sa poitrine serre, trop vite.",
            "maman|Tes genoux font trop de vagues.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout verser, d'en haut.",
            "narrateur|Le couvercle refuse, trop loin des doigts.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le cristal brun luit, trop bas.",
            "papa|Tu vois comment, Sarah ?",
            "narrateur|Sarah s'assoit, le sucrier au creux.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "toile,pichet",
        "emphasis": "pichet",
        "passage": [
            "narrateur|Sarah pose le pichet sur la toile cirée.",
            "enfant-f|Toute l'eau, tout de suite !",
            "narrateur|Elle penche trop fort, trop vite.",
            "narrateur|Le pichet glisse, l'eau tremble.",
            "enfant-f|Ça va tomber !",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça glisse trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout verser, d'un coup.",
            "narrateur|Le pichet refuse, trop lourd, trop mouillé.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du pichet, le cristal brun luit.",
            "maman|Tu vois comment, Sarah ?",
            "narrateur|Sarah pose le pichet, sans verser.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "eau,pichet",
        "emphasis": "évier",
        "passage": [
            "narrateur|Sarah porte le pichet vers l'eau.",
            "enfant-f|Ici, le jus va tomber, maman.",
            "narrateur|Elle ouvre le robinet, trop fort.",
            "narrateur|Le pichet claque le rebord, trop fort.",
            "enfant-f|L'eau file !",
            "narrateur|Sarah ne rit plus.",
            "narrateur|L'envie et la peur se bousculent, dans sa poitrine.",
            "maman|Ici, ça coule trop.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout remplir, trop vite.",
            "narrateur|Le robinet résiste, puis gicle.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le cristal brun luit, au bord bleu.",
            "papa|Tu vois comment, Sarah ?",
            "narrateur|Sarah tient le pichet, sans verser.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "bois,pichet",
        "emphasis": "tabouret",
        "passage": [
            "narrateur|Sarah grimpe, le pichet contre elle.",
            "enfant-f|Ici, je suis grande, papa.",
            "narrateur|Le bois du tabouret rend chaque pas.",
            "narrateur|Le pichet penche, l'eau fait une vague.",
            "enfant-f|Ça va tomber !",
            "narrateur|Son sourire s'en va.",
            "narrateur|Sa poitrine serre, trop vite.",
            "papa|Tes genoux font trop de vagues.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle veut tout verser, d'en haut.",
            "narrateur|Le pichet refuse, trop lourd pour elle.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le cristal brun luit, trop bas.",
            "maman|Tu vois comment, Sarah ?",
            "narrateur|Sarah s'assoit, le pichet au creux.",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
}

T3_LABS = {
    1: ("la balle jaune", "le grain", "maman tient"),
    2: ("les gouttes", "le filet", "papa presse"),
    3: ("les sauts", "le compte", "papa porte"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le jaune veut courir, trop vite.",
        "papa|La balle, le grain, ou maman ?",
    ],
    2: [
        "narrateur|L'eau file, trop vite.",
        "maman|Les gouttes, le filet, ou papa ?",
    ],
    3: [
        "narrateur|Le bois tremble, trop vite.",
        "papa|Les sauts, le compte, ou je porte ?",
    ],
}

T3_SONS = {
    (1, 1): "toile,citron",
    (1, 2): "grain,sucre",
    (1, 3): "mains,table",
    (2, 1): "eau,goutte",
    (2, 2): "robinet,filet",
    (2, 3): "presse,citron",
    (3, 1): "bois,saut",
    (3, 2): "compte,bois",
    (3, 3): "bras,pichet",
}

T3_EMPH = {
    1: {1: "balle jaune", 2: "grain", 3: "maman"},
    2: {1: "gouttes", 2: "filet", 3: "papa"},
    3: {1: "sauts", 2: "compte", 3: "papa"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On joue à la balle jaune.",
        "papa|Tu roules, moi je rattrape.",
        "narrateur|Sarah roule le citron, un, deux.",
        "narrateur|Le jaune va, revient, sent plus fort.",
        "enfant-f|Pas tout le jus d'un coup.",
        "narrateur|Elle s'arrête, le cristal brun luit.",
        "narrateur|Le citron a failli filer sous la chaise.",
        "maman|Un peu, puis on pose.",
        "narrateur|Sarah presse une fois, puis pose.",
        "narrateur|Le jus tombe, une perle, puis deux.",
        "papa|Tu as roulé, sans tout vider.",
        "enfant-f|La balle est fatiguée.",
        "narrateur|Le pichet se teinte, tout jaune.",
        "maman|Le cristal a dit la dose.",
    ],
    (1, 1, 2): [
        "enfant-f|On attend le grain.",
        "narrateur|Sarah pose les genoux au carreau.",
        "narrateur|Le citron repose, enfin sage.",
        "enfant-f|Un grain, pas tout le sucrier.",
        "narrateur|Elle prend le cristal brun, tout petit.",
        "maman|Ce grain-là, puis on pose.",
        "narrateur|Un grain glisse, puis plus.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Sarah presse, tout droit, tout petit.",
        "narrateur|Le jus tombe, une perle, puis deux.",
        "enfant-f|La citronnade peut venir.",
        "narrateur|Le cristal fond, au bord bleu.",
        "maman|Tu as versé un peu, Sarah.",
        "papa|Le sucrier reste plein, lui.",
    ],
    (1, 1, 3): [
        "enfant-f|Maman, tu tiens, s'il te plaît ?",
        "maman|Je tiens, tu verses le sucre.",
        "narrateur|Maman tient le citron, Sarah verse.",
        "enfant-f|Un grain, pas tout.",
        "narrateur|Sarah verse un grain, puis un autre.",
        "narrateur|Le jaune reste sage, dans sa main.",
        "papa|Le cristal brun reste au bord.",
        "narrateur|Le citron a failli glisser, trop vite.",
        "maman|Ma main tient, la tienne verse.",
        "narrateur|Le jus rejoint le sucre, tout jaune.",
        "enfant-f|Toi tu tiens, moi je verse.",
        "narrateur|La table garde un grain, tout mince.",
        "papa|Sans tout vider, ça tient.",
        "maman|Le pichet a son jaune, maintenant.",
    ],
    (1, 2, 1): [
        "enfant-f|On fait des gouttes.",
        "papa|Toi tu presses, moi je compte.",
        "narrateur|Sarah presse le citron, une perle.",
        "narrateur|Des perles tombent, une après l'autre.",
        "enfant-f|Pas tout le jus d'un coup.",
        "narrateur|Elle s'arrête, le cristal brun luit.",
        "narrateur|La graine a failli tout bloquer.",
        "maman|Une goutte, puis on pose.",
        "enfant-f|La dernière est au bout.",
        "narrateur|Le pichet se teinte, tout bas.",
        "papa|L'évier est devenu un ruisseau.",
        "narrateur|Le citron reste près de l'eau.",
        "enfant-f|Le jus est là, tout bas.",
        "maman|Le cristal a dit la dose.",
    ],
    (1, 2, 2): [
        "enfant-f|J'attends le filet.",
        "papa|Moi j'ouvre un peu, puis c'est toi.",
        "narrateur|Sarah tient le citron, le filet attend.",
        "narrateur|L'eau avance, trop mince, trop sage.",
        "enfant-f|Pas toute l'eau d'un coup.",
        "narrateur|Elle souffle, les épaules baissent.",
        "narrateur|Le cristal brun luit, au bord bleu.",
        "maman|D'abord l'eau, ensuite le citron.",
        "papa|C'est à toi, Sarah.",
        "enfant-f|J'y verse le jaune, un peu.",
        "narrateur|Sarah presse une fois, puis pose.",
        "narrateur|Le filet se tait, enfin.",
        "papa|Sans tout ouvrir, ça tient.",
        "maman|Le pichet a son jaune, maintenant.",
    ],
    (1, 2, 3): [
        "enfant-f|Papa, tu presses le citron ?",
        "papa|Je le presse, un peu.",
        "narrateur|Papa presse le citron, au-dessus du pichet.",
        "enfant-f|Pas tout, papa.",
        "narrateur|Sarah glisse un grain, les mains posées.",
        "narrateur|L'autre main suit, le pichet au calme.",
        "maman|Le cristal brun reste au bord.",
        "narrateur|Le citron a failli tout vider.",
        "enfant-f|Toi tu presses, moi je verse.",
        "narrateur|Le jaune tombe, le pichet se remplit.",
        "papa|Le jus tient tout seul, maintenant.",
        "narrateur|Un carré de carreau reste froid, autour.",
        "maman|Sans tout presser, ça pique juste.",
        "papa|Tu as dit stop, Sarah.",
    ],
    (1, 3, 1): [
        "enfant-f|On fait des sauts.",
        "papa|Tu rebondis, puis tu verses.",
        "narrateur|Le citron voyage d'un genou à l'autre.",
        "narrateur|Le bois penche, puis se tient droit.",
        "enfant-f|Les sauts tiennent, puis je pose.",
        "narrateur|Sarah s'arrête, le cristal brun luit.",
        "narrateur|Le citron a failli tomber, trop haut.",
        "maman|Un saut, puis on verse un peu.",
        "narrateur|Sarah verse, le pichet se teinte.",
        "papa|Le tabouret est une table, maintenant.",
        "narrateur|Le citron reste tout près, en haut.",
        "enfant-f|La citronnade est là, tout haut.",
        "maman|Sans tout verser, ça tient.",
        "papa|Tes pieds se sont assis, eux aussi.",
    ],
    (1, 3, 2): [
        "enfant-f|On attend le compte.",
        "papa|Un, deux, trois, tu verses.",
        "narrateur|Un saut, puis le bois reste sage.",
        "narrateur|Le citron reste sage, au creux des mains.",
        "enfant-f|Pas tout le jus d'un coup.",
        "narrateur|Le compte se tait, enfin.",
        "enfant-f|Maintenant, un peu !",
        "narrateur|Sarah verse, une perle, puis l'eau.",
        "narrateur|Le cristal brun fond, au bord bleu.",
        "papa|Tes genoux se sont assis, eux aussi.",
        "narrateur|Un pli du torchon retombe, sans bruit.",
        "maman|Le pichet a son jaune, d'en haut.",
        "enfant-f|J'ai compté, puis j'ai versé.",
        "papa|Sans tout vider, ça tient.",
    ],
    (1, 3, 3): [
        "enfant-f|Papa, tu portes le pichet ?",
        "papa|Je le porte, tout droit.",
        "narrateur|Papa porte le pichet, Sarah tient le citron.",
        "enfant-f|Un peu, pas tout.",
        "narrateur|Sarah écoute les mains, plus que ses pieds.",
        "maman|Tu verses, et ça tient.",
        "narrateur|Le cristal brun luit, trop près du nez.",
        "narrateur|Le pichet a failli pencher, trop haut.",
        "enfant-f|Moi aussi, j'écoute.",
        "narrateur|Le jaune tombe, vu d'en haut.",
        "papa|Tu as demandé, je porte.",
        "maman|Tes mains ont tenu le bord.",
        "narrateur|Sarah presse une fois, puis pose.",
        "papa|Sans tout presser, ça pique juste.",
    ],
    (2, 1, 1): [
        "enfant-f|On joue à la balle jaune.",
        "papa|Tu roules, le sucrier fait colline.",
        "narrateur|Sarah roule, le sucrier devient une colline.",
        "narrateur|Le jaune va, revient, autour du blanc.",
        "enfant-f|Pas tout le sucre d'un coup.",
        "narrateur|Elle s'arrête, le cristal brun luit.",
        "narrateur|Le sucrier a failli tout verser.",
        "maman|Un grain, puis on pose.",
        "narrateur|Sarah ouvre, un grain, puis ferme.",
        "narrateur|Le jus tombe, une perle, puis deux.",
        "papa|Tu as roulé, sans tout vider.",
        "enfant-f|La colline est fatiguée.",
        "narrateur|Le pichet se teinte, tout jaune.",
        "maman|Le cristal a dit la dose.",
    ],
    (2, 1, 2): [
        "enfant-f|On attend le grain.",
        "narrateur|Sarah pose les genoux au carreau.",
        "narrateur|Le sucrier repose, un grain arrêté.",
        "enfant-f|Un grain, pas tout le sucrier.",
        "narrateur|Elle prend le cristal brun, tout petit.",
        "maman|Ce grain-là, puis on pose.",
        "narrateur|Un grain glisse, puis plus.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Sarah verse, tout droit, tout petit.",
        "narrateur|Le sucre fond, une perle, puis deux.",
        "enfant-f|La citronnade peut venir.",
        "narrateur|Le cristal fond, au bord bleu.",
        "maman|Tu as versé un peu, Sarah.",
        "papa|Le sucrier reste plein, lui.",
    ],
    (2, 1, 3): [
        "enfant-f|Maman, tu tiens, s'il te plaît ?",
        "maman|Je tiens, tu verses le sucre.",
        "narrateur|Maman tient le sucrier, Sarah verse.",
        "enfant-f|Un grain, pas tout.",
        "narrateur|Sarah verse un grain, puis un autre.",
        "narrateur|Le blanc reste sage, dans sa main.",
        "papa|Le cristal brun reste au bord.",
        "narrateur|Le sucrier a failli tout vider.",
        "maman|Ma main tient, la tienne verse.",
        "narrateur|Le sucre rejoint le jus, tout jaune.",
        "enfant-f|Toi tu tiens, moi je verse.",
        "narrateur|La table garde un grain, tout mince.",
        "papa|Sans tout vider, ça tient.",
        "maman|Le pichet a son jaune, maintenant.",
    ],
    (2, 2, 1): [
        "enfant-f|On fait des gouttes.",
        "papa|Toi tu penches, moi je compte.",
        "narrateur|Sarah penche le sucrier, papa compte.",
        "narrateur|Des perles de sucre tombent, une après l'autre.",
        "enfant-f|Pas tout le sucrier d'un coup.",
        "narrateur|Elle s'arrête, le cristal brun luit.",
        "narrateur|L'eau a failli tout emporter.",
        "maman|Une goutte de sucre, puis on pose.",
        "enfant-f|La dernière est au bout.",
        "narrateur|Le pichet se teinte, tout bas.",
        "papa|L'évier est devenu un ruisseau.",
        "narrateur|Le sucrier reste près de l'eau.",
        "enfant-f|Le sucre est là, tout bas.",
        "maman|Le cristal a dit la dose.",
    ],
    (2, 2, 2): [
        "enfant-f|J'attends le filet.",
        "papa|Moi j'ouvre un peu, puis c'est toi.",
        "narrateur|Sarah tient le sucrier, le filet attend.",
        "narrateur|L'eau avance, trop mince, trop sage.",
        "enfant-f|Pas toute l'eau d'un coup.",
        "narrateur|Elle souffle, les épaules baissent.",
        "narrateur|Le cristal brun luit, au bord bleu.",
        "maman|D'abord l'eau, ensuite le sucre.",
        "papa|C'est à toi, Sarah.",
        "enfant-f|J'y verse un grain, un peu.",
        "narrateur|Sarah penche une fois, puis pose.",
        "narrateur|Le filet se tait, enfin.",
        "papa|Sans tout ouvrir, ça tient.",
        "maman|Le pichet a son jaune, maintenant.",
    ],
    (2, 2, 3): [
        "enfant-f|Papa, tu presses le citron ?",
        "papa|Je le presse, un peu.",
        "narrateur|Papa presse, près du sucrier.",
        "enfant-f|Pas tout, papa.",
        "narrateur|Sarah glisse un grain, les mains posées.",
        "narrateur|L'autre main suit, le pichet au calme.",
        "maman|Le cristal brun reste au bord.",
        "narrateur|Le sucrier a failli tout vider.",
        "enfant-f|Toi tu presses, moi je verse.",
        "narrateur|Le jaune tombe, le pichet se remplit.",
        "papa|Le jus tient tout seul, maintenant.",
        "narrateur|Un carré de carreau reste froid, autour.",
        "maman|Sans tout presser, ça pique juste.",
        "papa|Tu as dit stop, Sarah.",
    ],
    (2, 3, 1): [
        "enfant-f|On fait des sauts.",
        "papa|Tu rebondis, puis tu verses.",
        "narrateur|Le sucrier voyage d'un genou à l'autre.",
        "narrateur|Le bois penche, puis se tient droit.",
        "enfant-f|Les sauts tiennent, puis je pose.",
        "narrateur|Sarah s'arrête, le cristal brun luit.",
        "narrateur|Le sucrier a failli tout verser.",
        "maman|Un saut, puis on verse un grain.",
        "narrateur|Sarah verse, le pichet se teinte.",
        "papa|Le tabouret est une table, maintenant.",
        "narrateur|Le sucrier reste tout près, en haut.",
        "enfant-f|La citronnade est là, tout haut.",
        "maman|Sans tout verser, ça tient.",
        "papa|Tes pieds se sont assis, eux aussi.",
    ],
    (2, 3, 2): [
        "enfant-f|On attend le compte.",
        "papa|Un, deux, trois, tu verses.",
        "narrateur|Un saut, puis le bois reste sage.",
        "narrateur|Le sucrier reste sage, au creux des mains.",
        "enfant-f|Pas tout le sucre d'un coup.",
        "narrateur|Le compte se tait, enfin.",
        "enfant-f|Maintenant, un grain !",
        "narrateur|Sarah verse, un grain, puis l'eau.",
        "narrateur|Le cristal brun fond, au bord bleu.",
        "papa|Tes genoux se sont assis, eux aussi.",
        "narrateur|Un pli du torchon retombe, sans bruit.",
        "maman|Le pichet a son jaune, d'en haut.",
        "enfant-f|J'ai compté, puis j'ai versé.",
        "papa|Sans tout vider, ça tient.",
    ],
    (2, 3, 3): [
        "enfant-f|Papa, tu portes le pichet ?",
        "papa|Je le porte, tout droit.",
        "narrateur|Papa porte le pichet, près du sucrier.",
        "enfant-f|Un grain, pas tout.",
        "narrateur|Sarah écoute les mains, plus que ses pieds.",
        "maman|Tu verses, et ça tient.",
        "narrateur|Le cristal brun luit, trop près du nez.",
        "narrateur|Le pichet a failli pencher, trop haut.",
        "enfant-f|Moi aussi, j'écoute.",
        "narrateur|Le sucre tombe, vu d'en haut.",
        "papa|Tu as demandé, je porte.",
        "maman|Tes mains ont tenu le sucrier.",
        "narrateur|Sarah verse un grain, puis pose.",
        "papa|Sans tout verser, ça pique juste.",
    ],
    (3, 1, 1): [
        "enfant-f|On joue à la balle jaune.",
        "papa|Tu roules, le pichet fait un lac.",
        "narrateur|Sarah roule, le pichet devient un lac.",
        "narrateur|Le jaune va, revient, vers le bleu.",
        "enfant-f|Pas toute l'eau d'un coup.",
        "narrateur|Elle s'arrête, le cristal brun luit.",
        "narrateur|Le pichet a failli tout verser.",
        "maman|Un peu, puis on pose.",
        "narrateur|Sarah penche une fois, puis pose.",
        "narrateur|Le jus tombe, une perle, puis deux.",
        "papa|Tu as roulé, sans tout vider.",
        "enfant-f|Le lac est fatigué.",
        "narrateur|Le pichet se teinte, tout jaune.",
        "maman|Le cristal a dit la dose.",
    ],
    (3, 1, 2): [
        "enfant-f|On attend le grain.",
        "narrateur|Sarah pose les genoux au carreau.",
        "narrateur|Le pichet repose, l'eau sage.",
        "enfant-f|Un grain, pas tout le sucrier.",
        "narrateur|Elle prend le cristal brun, tout petit.",
        "maman|Ce grain-là, puis on pose.",
        "narrateur|Un grain glisse, puis plus.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Sarah verse, tout droit, tout petit.",
        "narrateur|Le sucre fond dans l'eau, tout bas.",
        "enfant-f|La citronnade peut venir.",
        "narrateur|Le cristal fond, au bord bleu.",
        "maman|Tu as versé un peu, Sarah.",
        "papa|Le pichet reste droit, lui.",
    ],
    (3, 1, 3): [
        "enfant-f|Maman, tu tiens, s'il te plaît ?",
        "maman|Je tiens, tu verses le sucre.",
        "narrateur|Maman tient le pichet, Sarah verse.",
        "enfant-f|Un grain, pas tout.",
        "narrateur|Sarah verse un grain, puis un autre.",
        "narrateur|Le bleu reste sage, dans sa main.",
        "papa|Le cristal brun reste au bord.",
        "narrateur|Le pichet a failli tout verser.",
        "maman|Ma main tient, la tienne verse.",
        "narrateur|Le sucre rejoint l'eau, tout jaune.",
        "enfant-f|Toi tu tiens, moi je verse.",
        "narrateur|La table garde un grain, tout mince.",
        "papa|Sans tout vider, ça tient.",
        "maman|Le pichet a son jaune, maintenant.",
    ],
    (3, 2, 1): [
        "enfant-f|On fait des gouttes.",
        "papa|Toi tu penches, moi je compte.",
        "narrateur|Sarah penche le pichet, papa compte.",
        "narrateur|Des perles d'eau tombent, une après l'autre.",
        "enfant-f|Pas toute l'eau d'un coup.",
        "narrateur|Elle s'arrête, le cristal brun luit.",
        "narrateur|Le robinet a failli tout remplir.",
        "maman|Une goutte, puis on pose.",
        "enfant-f|La dernière est au bout.",
        "narrateur|Le pichet se teinte, tout bas.",
        "papa|L'évier est devenu un ruisseau.",
        "narrateur|Le pichet reste près de l'eau.",
        "enfant-f|Le jus est là, tout bas.",
        "maman|Le cristal a dit la dose.",
    ],
    (3, 2, 2): [
        "enfant-f|J'attends le filet.",
        "papa|Moi j'ouvre un peu, puis c'est toi.",
        "narrateur|Sarah tient le pichet, le filet attend.",
        "narrateur|L'eau avance, trop mince, trop sage.",
        "enfant-f|Pas toute l'eau d'un coup.",
        "narrateur|Elle souffle, les épaules baissent.",
        "narrateur|Le cristal brun luit, au bord bleu.",
        "maman|D'abord l'eau, ensuite le citron.",
        "papa|C'est à toi, Sarah.",
        "enfant-f|J'y verse le jaune, un peu.",
        "narrateur|Sarah penche une fois, puis pose.",
        "narrateur|Le filet se tait, enfin.",
        "papa|Sans tout ouvrir, ça tient.",
        "maman|Le pichet a son jaune, maintenant.",
    ],
    (3, 2, 3): [
        "enfant-f|Papa, tu presses le citron ?",
        "papa|Je le presse, un peu.",
        "narrateur|Papa presse, au-dessus du pichet.",
        "enfant-f|Pas tout, papa.",
        "narrateur|Sarah glisse un grain, les mains posées.",
        "narrateur|L'autre main suit, le pichet au calme.",
        "maman|Le cristal brun reste au bord.",
        "narrateur|Le pichet a failli trop se remplir.",
        "enfant-f|Toi tu presses, moi je verse.",
        "narrateur|Le jaune tombe, le pichet se remplit.",
        "papa|Le jus tient tout seul, maintenant.",
        "narrateur|Un carré de carreau reste froid, autour.",
        "maman|Sans tout presser, ça pique juste.",
        "papa|Tu as dit stop, Sarah.",
    ],
    (3, 3, 1): [
        "enfant-f|On fait des sauts.",
        "papa|Tu rebondis, puis tu verses.",
        "narrateur|Le pichet voyage d'un genou à l'autre.",
        "narrateur|Le bois penche, puis se tient droit.",
        "enfant-f|Les sauts tiennent, puis je pose.",
        "narrateur|Sarah s'arrête, le cristal brun luit.",
        "narrateur|Le pichet a failli tout verser.",
        "maman|Un saut, puis on verse un peu.",
        "narrateur|Sarah verse, le pichet se teinte.",
        "papa|Le tabouret est une table, maintenant.",
        "narrateur|Le pichet reste tout près, en haut.",
        "enfant-f|La citronnade est là, tout haut.",
        "maman|Sans tout verser, ça tient.",
        "papa|Tes pieds se sont assis, eux aussi.",
    ],
    (3, 3, 2): [
        "enfant-f|On attend le compte.",
        "papa|Un, deux, trois, tu verses.",
        "narrateur|Un saut, puis le bois reste sage.",
        "narrateur|Le pichet reste sage, au creux des genoux.",
        "enfant-f|Pas toute l'eau d'un coup.",
        "narrateur|Le compte se tait, enfin.",
        "enfant-f|Maintenant, un peu !",
        "narrateur|Sarah verse, une perle, puis l'eau.",
        "narrateur|Le cristal brun fond, au bord bleu.",
        "papa|Tes genoux se sont assis, eux aussi.",
        "narrateur|Un pli du torchon retombe, sans bruit.",
        "maman|Le pichet a son jaune, d'en haut.",
        "enfant-f|J'ai compté, puis j'ai versé.",
        "papa|Sans tout vider, ça tient.",
    ],
    (3, 3, 3): [
        "enfant-f|Papa, tu portes le pichet ?",
        "papa|Je le porte, tout droit.",
        "narrateur|Papa porte le pichet, tout droit.",
        "enfant-f|Un peu, pas tout.",
        "narrateur|Sarah écoute les mains, plus que ses pieds.",
        "maman|Tu verses, et ça tient.",
        "narrateur|Le cristal brun luit, trop près du nez.",
        "narrateur|Le pichet a failli pencher, trop haut.",
        "enfant-f|Moi aussi, j'écoute.",
        "narrateur|Le jaune tombe, vu d'en haut.",
        "papa|Tu as demandé, je porte.",
        "maman|Tes mains ont tenu le bord.",
        "narrateur|Sarah verse une perle, puis pose.",
        "papa|Sans tout verser, ça pique juste.",
    ],
}

END_SONS = {1: "verre,table", 2: "verre,eau", 3: "verre,bois"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Sarah boit près de la table.",
        "enfant-f|La balle est devenue du jus.",
        "papa|Tu roulais, moi je rattrapais.",
        "maman|Le pichet a son jaune.",
        "narrateur|Ça a failli tout filer.",
        "narrateur|Le cristal de sucre brun tient, mouillé.",
        "enfant-f|Ça pique, puis c'est doux.",
        "papa|Tu as versé un peu, Sarah.",
        "narrateur|La toile cirée garde un rond jaune.",
    ],
    (1, 1, 2): [
        "narrateur|Sarah boit, la toile sage.",
        "enfant-f|J'ai attendu le grain, d'abord.",
        "papa|Puis le citron est resté droit.",
        "maman|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le sucre ne danse plus.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|C'est sucré, tout au fond.",
        "papa|Un grain a suffi, Sarah.",
        "narrateur|Un grain blanc dort près du cristal.",
    ],
    (1, 1, 3): [
        "narrateur|Sarah boit, la main de maman tout près.",
        "enfant-f|Tu tenais le fruit.",
        "papa|Tu demandais, maman tenait.",
        "maman|Ma main a fait le bol.",
        "narrateur|Ça a failli tout glisser.",
        "narrateur|Le cristal de sucre brun reste au doigt.",
        "enfant-f|Il est à nous.",
        "papa|Toi tu versais, elle tenait.",
        "narrateur|La main de maman reste sur le bois.",
    ],
    (1, 2, 1): [
        "narrateur|Sarah boit au bout des gouttes.",
        "enfant-f|Toi tu comptais, moi je pressais.",
        "papa|Tes gouttes ont fait le jus.",
        "maman|L'évier est devenu un ruisseau.",
        "narrateur|Ça a failli tout couler.",
        "narrateur|Le cristal de sucre brun luit, mouillé.",
        "enfant-f|Les perles restent, maman.",
        "papa|Une perle, puis une autre.",
        "narrateur|Une perle sèche contre l'émail.",
    ],
    (1, 2, 2): [
        "narrateur|Sarah boit, le filet sage.",
        "papa|J'ai ouvert, puis c'était toi.",
        "enfant-f|J'ai attendu l'eau.",
        "maman|D'abord l'eau, ensuite le jaune.",
        "narrateur|Le pichet bleu tient, enfin.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|Ça pique, puis c'est doux.",
        "papa|Sans tout ouvrir, ça tient.",
        "narrateur|Le filet a laissé un trait clair.",
    ],
    (1, 2, 3): [
        "narrateur|Sarah boit, le citron pressé par papa.",
        "enfant-f|Tu pressais, un peu.",
        "papa|Le jus est tombé, juste assez.",
        "maman|Le pichet a son jaune, à vous.",
        "narrateur|Ça a failli tout vider.",
        "narrateur|Le cristal de sucre brun reste au bord.",
        "enfant-f|Regarde, papa, il brille.",
        "maman|Tu as dit stop, à temps.",
        "narrateur|Le citron pressé sent plus fort.",
    ],
    (1, 3, 1): [
        "narrateur|Sarah boit, perchée sur le tabouret.",
        "enfant-f|Les sauts sont finis, papa.",
        "papa|Tu rebondissais, puis tu versais.",
        "maman|La table haute a son jus, ici.",
        "narrateur|Ça a failli tout tomber.",
        "narrateur|Le cristal de sucre brun tient, en haut.",
        "enfant-f|Les sauts se taisent.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le tabouret garde une ombre ronde.",
    ],
    (1, 3, 2): [
        "narrateur|Sarah boit, après le compte.",
        "enfant-f|On a attendu le bois.",
        "papa|Quand il s'est tu, tu as versé.",
        "maman|Le tabouret a fait une table.",
        "narrateur|Tes genoux se sont assis.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|J'ai compté, c'était bon.",
        "papa|Un, deux, trois, puis le jus.",
        "narrateur|Le bois tiède tient une goutte sucrée.",
    ],
    (1, 3, 3): [
        "narrateur|Sarah boit, le pichet porté par papa.",
        "enfant-f|J'écoutais tes mains.",
        "papa|Moi aussi, je portais avec toi.",
        "maman|Tu as demandé, il a porté.",
        "narrateur|Ça a failli trop pencher.",
        "narrateur|Le cristal de sucre brun luit, tout près.",
        "enfant-f|Il est à nous, maman.",
        "papa|Tes mains ont tenu le bord.",
        "narrateur|Le pichet bleu penche, puis se tient.",
    ],
    (2, 1, 1): [
        "narrateur|Sarah boit près de la colline blanche.",
        "enfant-f|La balle a tourné autour.",
        "papa|Tu roulais, le sucrier tenait.",
        "maman|Le pichet a son jaune.",
        "narrateur|Ça a failli tout verser.",
        "narrateur|Le cristal de sucre brun tient, collé.",
        "enfant-f|C'est sucré, tout au fond.",
        "papa|Un grain a suffi, Sarah.",
        "narrateur|La peau du citron est devenue mate.",
    ],
    (2, 1, 2): [
        "narrateur|Sarah boit, un grain au fond.",
        "enfant-f|J'ai attendu le grain, d'abord.",
        "papa|Le sucrier est resté plein.",
        "maman|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le sucre ne danse plus.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|C'est doux, tout au fond.",
        "papa|Un grain, pas tout le sucrier.",
        "narrateur|Le sucrier blanc a perdu un grain.",
    ],
    (2, 1, 3): [
        "narrateur|Sarah boit, la main de maman tout près.",
        "enfant-f|Tu tenais le sucrier.",
        "papa|Tu demandais, maman tenait.",
        "maman|Ma main a fait le bol.",
        "narrateur|Ça a failli tout glisser.",
        "narrateur|Le cristal de sucre brun reste au doigt.",
        "enfant-f|Il est à nous.",
        "papa|Toi tu versais, elle tenait.",
        "narrateur|Le bord bleu tient le cristal, mouillé.",
    ],
    (2, 2, 1): [
        "narrateur|Sarah boit au bout des gouttes.",
        "enfant-f|Toi tu comptais, moi je penchais.",
        "papa|Tes gouttes de sucre ont fait le jus.",
        "maman|L'évier est devenu un ruisseau.",
        "narrateur|Ça a failli tout emporter.",
        "narrateur|Le cristal de sucre brun luit, mouillé.",
        "enfant-f|Les perles restent, maman.",
        "papa|Une perle, puis une autre.",
        "narrateur|Un fil de jus brille sur l'émail.",
    ],
    (2, 2, 2): [
        "narrateur|Sarah boit, le filet sage.",
        "papa|J'ai ouvert, puis c'était toi.",
        "enfant-f|J'ai attendu l'eau.",
        "maman|D'abord l'eau, ensuite le sucre.",
        "narrateur|Le pichet bleu tient, enfin.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|C'est sucré, puis ça pique.",
        "papa|Sans tout ouvrir, ça tient.",
        "narrateur|Le torchon a pris une tache jaune.",
    ],
    (2, 2, 3): [
        "narrateur|Sarah boit, le citron pressé par papa.",
        "enfant-f|Tu pressais, un peu.",
        "papa|Le jus est tombé, juste assez.",
        "maman|Le pichet a son jaune, à vous.",
        "narrateur|Ça a failli tout vider.",
        "narrateur|Le cristal de sucre brun reste au bord.",
        "enfant-f|Regarde, papa, il brille.",
        "maman|Tu as dit stop, à temps.",
        "narrateur|Papa essuie le rebord, sans parler.",
    ],
    (2, 3, 1): [
        "narrateur|Sarah boit, perchée sur le tabouret.",
        "enfant-f|Les sauts sont finis, papa.",
        "papa|Tu rebondissais, puis tu versais.",
        "maman|La table haute a son jus, ici.",
        "narrateur|Ça a failli tout tomber.",
        "narrateur|Le cristal de sucre brun tient, en haut.",
        "enfant-f|Les sauts se taisent.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Les pieds de Sarah se taisent, posés.",
    ],
    (2, 3, 2): [
        "narrateur|Sarah boit, après le compte.",
        "enfant-f|On a attendu le bois.",
        "papa|Quand il s'est tu, tu as versé.",
        "maman|Le tabouret a fait une table.",
        "narrateur|Tes genoux se sont assis.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|J'ai compté, un grain.",
        "papa|Un, deux, trois, puis le sucre.",
        "narrateur|Sarah lèche le cristal, tout brun.",
    ],
    (2, 3, 3): [
        "narrateur|Sarah boit, le pichet porté par papa.",
        "enfant-f|J'écoutais tes mains.",
        "papa|Moi aussi, je portais avec toi.",
        "maman|Tu as demandé, il a porté.",
        "narrateur|Ça a failli trop pencher.",
        "narrateur|Le cristal de sucre brun luit, tout près.",
        "enfant-f|Il est à nous, maman.",
        "papa|Tes mains ont tenu le sucrier.",
        "narrateur|Le soleil quitte un coin de vitre.",
    ],
    (3, 1, 1): [
        "narrateur|Sarah boit près du lac bleu.",
        "enfant-f|La balle a trouvé le pichet.",
        "papa|Tu roulais, le pichet tenait.",
        "maman|Le pichet a son jaune.",
        "narrateur|Ça a failli tout verser.",
        "narrateur|Le cristal de sucre brun tient, collé.",
        "enfant-f|Ça pique, puis c'est doux.",
        "papa|Un peu d'eau, un peu de jaune.",
        "narrateur|La chaise vide écoute le pichet.",
    ],
    (3, 1, 2): [
        "narrateur|Sarah boit, un grain au fond.",
        "enfant-f|J'ai attendu le grain, d'abord.",
        "papa|Le pichet est resté droit.",
        "maman|Tes pieds se sont assis, eux aussi.",
        "narrateur|L'eau ne danse plus.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|C'est sucré, tout au fond.",
        "papa|Un grain, pas tout le sucrier.",
        "narrateur|La cuillère de bois dort collée.",
    ],
    (3, 1, 3): [
        "narrateur|Sarah boit, la main de maman tout près.",
        "enfant-f|Tu tenais le pichet.",
        "papa|Tu demandais, maman tenait.",
        "maman|Ma main a fait le bol.",
        "narrateur|Ça a failli tout glisser.",
        "narrateur|Le cristal de sucre brun reste au doigt.",
        "enfant-f|Il est à nous.",
        "papa|Toi tu versais, elle tenait.",
        "narrateur|Le carreau froid garde un pied nu.",
    ],
    (3, 2, 1): [
        "narrateur|Sarah boit au bout des gouttes.",
        "enfant-f|Toi tu comptais, moi je penchais.",
        "papa|Tes gouttes d'eau ont fait le jus.",
        "maman|L'évier est devenu un ruisseau.",
        "narrateur|Ça a failli tout remplir.",
        "narrateur|Le cristal de sucre brun luit, mouillé.",
        "enfant-f|Les perles restent, maman.",
        "papa|Une perle, puis une autre.",
        "narrateur|Maman pose trois verres, pas quatre.",
    ],
    (3, 2, 2): [
        "narrateur|Sarah boit, le filet sage.",
        "papa|J'ai ouvert, puis c'était toi.",
        "enfant-f|J'ai attendu l'eau.",
        "maman|D'abord l'eau, ensuite le jaune.",
        "narrateur|Le pichet bleu tient, enfin.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|Ça pique, puis c'est doux.",
        "papa|Sans tout ouvrir, ça tient.",
        "narrateur|Le couvercle du sucrier fait tic.",
    ],
    (3, 2, 3): [
        "narrateur|Sarah boit, le citron pressé par papa.",
        "enfant-f|Tu pressais, un peu.",
        "papa|Le jus est tombé, juste assez.",
        "maman|Le pichet a son jaune, à vous.",
        "narrateur|Ça a failli trop se remplir.",
        "narrateur|Le cristal de sucre brun reste au bord.",
        "enfant-f|Regarde, papa, il brille.",
        "maman|Tu as dit stop, à temps.",
        "narrateur|Une graine de citron reste au fond.",
    ],
    (3, 3, 1): [
        "narrateur|Sarah boit, perchée sur le tabouret.",
        "enfant-f|Les sauts sont finis, papa.",
        "papa|Tu rebondissais, puis tu versais.",
        "maman|La table haute a son jus, ici.",
        "narrateur|Ça a failli tout tomber.",
        "narrateur|Le cristal de sucre brun tient, en haut.",
        "enfant-f|Les sauts se taisent.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le tabouret craque, puis se tait.",
    ],
    (3, 3, 2): [
        "narrateur|Sarah boit, après le compte.",
        "enfant-f|On a attendu le bois.",
        "papa|Quand il s'est tu, tu as versé.",
        "maman|Le tabouret a fait une table.",
        "narrateur|Tes genoux se sont assis.",
        "narrateur|Le cristal de sucre brun a fondu.",
        "enfant-f|J'ai compté, un peu d'eau.",
        "papa|Un, deux, trois, puis le pichet.",
        "narrateur|Le cristal a fondu, au bord bleu.",
    ],
    (3, 3, 3): [
        "narrateur|Sarah boit, le pichet porté par papa.",
        "enfant-f|J'écoutais tes mains.",
        "papa|Moi aussi, je portais avec toi.",
        "maman|Tu as demandé, il a porté.",
        "narrateur|Ça a failli trop pencher.",
        "narrateur|Le cristal de sucre brun luit, tout près.",
        "enfant-f|Il est à nous, maman.",
        "papa|Tes mains ont tenu le bord.",
        "narrateur|Un nuage de toast reste sur la vitre.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "frigo,carreaux",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le citron jaune", "le sucrier blanc", "le pichet bleu")},
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
            {"fields": t3lab("la table", "l'évier", "le tabouret")},
        )
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[sp] = voice(
                by_src[sp], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{sp}_T0003_P0000"] = voice(
                by_src[f"{sp}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[b],
                    {"emphasis": "cristal de sucre brun"},
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
        "hyperactif",
        "léa",
        "lea ",
        "tom ",
        "dînette",
        "dinette",
        "les cubes",
        "capitaine",
        "plic",
        "volet jaune",
        "boutique",
        "marelle",
        "carrousel",
        "papillon",
        "portail",
        "il faut attendre",
        "on doit demander",
        "miel",
        "merle",
        "tout doux",
        "tout calme",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "larme de bronze",
        "étoile brune",
        "fil pâle",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "citronnade" not in blob:
        raise SystemExit(f"{SID}: citronnade absente")
    if "cristal" not in blob:
        raise SystemExit(f"{SID}: cristal absent")
    if "cristal de sucre brun" not in blob:
        raise SystemExit(f"{SID}: cristal de sucre brun absent")

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

    t2s = [c["text"] for c in story["chunks"] if re.search(r"T0002_P000[123]$", c["chunk_id"])]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

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
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — attendre / doser, pas tout verser d'un coup (vécue, non dite)\n"
        "- **Personnages :** Sarah, papa, maman (un seul enfant ; pas de 2e enfant)\n"
        "- **Lieu :** la cuisine : table, évier, tabouret (comptoir du pichet)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés. Labels T1/T2/T3 gardés.\n\n"
        "## Promesse narrative\n\n"
        "Le frigo frappe, trop ouvert. Un **cristal de sucre brun** tient au bord "
        "du pichet bleu. Sarah veut remplir le pichet de citronnade **pendant que le soleil "
        "tient la vitre**. Elle veut tout le sucre, tout le citron, d'un coup. "
        "Elle prend le citron, le sucrier ou le pichet ; les trois viennent. "
        "À la table le citron file, à l'évier le jus résiste, sur le tabouret ses pieds dansent. "
        "Une 2e ruse (citron caché, graine, couvercle coincé, robinet qui gicle, pichet trop lourd) : "
        "elle refuse de foncer, revoit le cristal du début. Neuf façons de doser. "
        "Le pichet se remplit. Le cristal dit la dose.\n\n"
        "## Vécu\n\n"
        "Sarah veut la citronnade **maintenant**, tout verser. Papa et maman sont là. "
        "Sourire disparu, poitrine bousculée, adulte accroupi. "
        "Chaque choix change l'obstacle et le climax. La leçon se voit : "
        "tout presser fait filer le citron ; un grain, un filet, un compte, "
        "maman qui tient, papa qui porte, ça tient. "
        "Indice d'ouverture payé : cristal de sucre brun. Fin : pichet + trace unique "
        "(rond jaune, grain, doigt, émail, filet, citron pressé, ombre, bois, vitre).\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien merged F-NAR-016 sans notes/xai : tout réécrit.\n"
        "- Audit générique « deux enfants » ignoré : dump = Sarah, papa, maman seulement.\n"
        "- Slogan pédagogique, miel, merle, « encore / déjà / tout doux / tout calme » jetés.\n"
        "- Ouverture inventée (frigo trop ouvert), pas les 5 listées example4.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (cristal vu). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
