#!/usr/bin/env python3
"""TREE-DIF-047 — Le camp de Nino, sous la lampe (N2, DIF.ENE.001, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-047"
N2 = 15
TITLE = "Le camp de Nino, sous la lampe"
FIL = (
    "La salle d'eau se tait. Une écaille de savon tient sur la lampe torche. "
    "Nino veut planter son camp dans la chambre, toute la nuit, d'un coup, "
    "avant que le grillon se taise. Il prend la lampe, le sac vert ou "
    "l'oreiller rayé ; les trois viennent. À la fenêtre le faisceau court, "
    "sur le tapis ça glisse, au pied du lit les genoux dansent. Il refuse "
    "de foncer. L'écaille dit la dose. Le camp tient."
)
CHARS = "Nino, papa, maman"
SETTING = "la chambre de Nino : fenêtre, tapis, pied du lit"
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
        "emphasis": "écaille de savon",
        "note": "arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=nino_veut_tout_planter_l_ecaille_attend; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_veut_tout_planter; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_objet_résiste_il_refuse_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "écaille",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=l_ecaille_dit_la_dose; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "écaille de savon",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_camp_tient_l_ecaille_reste; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N2:
            raise SystemExit(f"{where} {n}>{N2}: {ph}")
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
    "narrateur|La salle d'eau vient de se taire, derrière la porte.",
    "narrateur|Le savon a laissé une odeur ronde, dans le couloir.",
    "narrateur|Sur la lampe torche, une écaille de savon tient.",
    "enfant-m|Elle est collée, toute mince.",
    "papa|C'est du bain d'avant, Nino.",
    "maman|La chambre sent le linge tiède.",
    "narrateur|Derrière le volet, un grillon chante, tout bas.",
    "narrateur|On dirait qu'il a planté sa tente, lui.",
    "narrateur|Nino vit ici, avec papa et maman.",
    "enfant-m|Je veux camper ici, toute la nuit.",
    "papa|Le grillon chante, dehors.",
    "maman|On plante le camp, avant qu'il se taise ?",
    "enfant-m|Tout, d'un coup, maintenant !",
    "narrateur|En ce moment, Nino touche l'écaille de savon.",
    "papa|Merci, tu as vu l'écaille.",
    "maman|Tes pieds dansent, Nino.",
]

T1_CHOICE = [
    "narrateur|Près du tapis, trois affaires attendent.",
    "narrateur|La lampe, le sac, et l'oreiller.",
    "papa|La lampe, le sac, ou l'oreiller ?",
    "maman|Tu prends quoi d'abord, Nino ?",
]

T1 = {
    1: {
        "lab": "la lampe torche",
        "sons": "lampe,clic",
        "emphasis": "lampe torche",
        "passage": [
            "narrateur|Nino prend d'abord la lampe torche.",
            "enfant-m|Elle est tiède, contre les doigts.",
            "maman|Garde-la dans les mains, tout droit.",
            "narrateur|Le plastique sent le savon, un peu.",
            "enfant-m|Je plante tout, maintenant !",
            "papa|Pas tout, Nino.",
            "narrateur|Papa glisse le sac vert, tout près.",
            "narrateur|Maman pose l'oreiller contre son bras.",
            "narrateur|Lampe, sac, oreiller, contre lui.",
            "narrateur|Ses pieds tapent le parquet, trop vite.",
            "papa|La lampe d'abord, tu l'as.",
            "enfant-m|Vite, la tente veut sa nuit.",
        ],
        "question": [
            "narrateur|Nino a mis la lampe torche.",
            "maman|Elle est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "mains",
            "accepted_examples": "mains | les mains | dans les mains | ses mains",
            "retry_prompt": "La lampe est dans les mains.",
        },
        "confirm": [
            "enfant-m|Dans les mains.",
            "maman|Oui.",
            "narrateur|Un clic de lampe réveille le plafond.",
            "enfant-m|C'est mon soleil de camp.",
            "narrateur|Nino plie un genou, trop vite.",
            "narrateur|Le faisceau dessine un lapin, puis le perd.",
            "maman|Tes pieds veulent la nuit.",
            "papa|On pose le camp ici ?",
            "enfant-m|Oui, papa.",
            "narrateur|L'écaille de savon tient, sur le plastique.",
        ],
    },
    2: {
        "lab": "le sac vert",
        "sons": "sac,fermeture",
        "emphasis": "sac vert",
        "passage": [
            "narrateur|Nino passe d'abord le sac vert, sous le bras.",
            "enfant-m|Il gratte un peu, à la manche.",
            "papa|Tiens-le sous le bras, tout chaud.",
            "narrateur|La fermeture fait un petit clic.",
            "enfant-m|Je plante tout, maintenant !",
            "maman|Pas tout, Nino.",
            "narrateur|Il glisse la lampe contre l'autre main.",
            "narrateur|Maman pose l'oreiller près de lui.",
            "narrateur|Le vert, le plastique, et les rayures.",
            "narrateur|Un genou rebondit, puis l'autre.",
            "maman|Le sac d'abord, il est prêt.",
            "enfant-m|Vite, la tente veut sa nuit.",
        ],
        "question": [
            "narrateur|Nino a passé le sac vert.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "bras",
            "accepted_examples": "bras | le bras | sous le bras | son bras",
            "retry_prompt": "Le sac est sous le bras.",
        },
        "confirm": [
            "enfant-m|Sous le bras.",
            "papa|Oui.",
            "narrateur|La fermeture du sac chatouille sa manche.",
            "enfant-m|C'est ma tente, pour ce soir.",
            "narrateur|Nino secoue le sac, un nuage de coton.",
            "narrateur|Un coin vert traîne par terre.",
            "maman|Ça sent le linge tiède, tout près.",
            "papa|Tes mains, sur le sac ?",
            "enfant-m|Oui, papa.",
            "narrateur|L'écaille de savon tient, près du clic.",
        ],
    },
    3: {
        "lab": "l'oreiller rayé",
        "sons": "oreiller,coton",
        "emphasis": "oreiller rayé",
        "passage": [
            "narrateur|Nino prend d'abord l'oreiller rayé.",
            "enfant-m|Il est chaud, contre le ventre.",
            "maman|Garde-le là, contre toi.",
            "narrateur|Le coton sent le linge, un peu.",
            "enfant-m|Je plante tout, maintenant !",
            "papa|Pas tout, Nino.",
            "narrateur|Il glisse la lampe près des chaussettes.",
            "narrateur|Papa pose le sac contre sa hanche.",
            "narrateur|Les rayures avancent, trop sages.",
            "narrateur|Ses talons frappent le tapis, trop vite.",
            "papa|L'oreiller d'abord, il est pris.",
            "enfant-m|Vite, la tente veut sa nuit.",
        ],
        "question": [
            "narrateur|Nino a pris l'oreiller rayé.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "ventre",
            "accepted_examples": "ventre | le ventre | contre le ventre | son ventre",
            "retry_prompt": "L'oreiller est contre le ventre.",
        },
        "confirm": [
            "enfant-m|Contre le ventre.",
            "maman|Oui.",
            "narrateur|Les rayures de l'oreiller dansent un peu.",
            "enfant-m|Ma tête campe dessus.",
            "narrateur|Nino le serre, le lâche, le reprend.",
            "narrateur|Un coin rayé frotte sa joue, chaud.",
            "maman|La chambre est prête, devant.",
            "papa|On y va, tous les trois ?",
            "enfant-m|Oui.",
            "narrateur|L'écaille de savon tient, sur la lampe.",
        ],
    },
}


def t2_question(t1: int) -> list[str]:
    first = {
        1: "narrateur|Nino tapote le parquet, trop vite.",
        2: "narrateur|Le sac tape sa hanche, trop fort.",
        3: "narrateur|L'oreiller rebondit contre lui, trop haut.",
    }[t1]
    return [
        first,
        "narrateur|Sous la fenêtre, le rideau garde un rai de rue.",
        "narrateur|Au milieu, le tapis fait un carré chaud.",
        "narrateur|Près du bois, le pied du lit attend.",
        "papa|On campe où, Nino ?",
    ]


T2 = {
    (1, 1): {
        "sons": "rideau,grillon",
        "emphasis": "lampe",
        "passage": [
            "narrateur|Nino porte la lampe vers le rideau.",
            "enfant-m|Le camp, c'est là, papa !",
            "narrateur|Il lance le faisceau, trop vite, trop fort.",
            "narrateur|Le faisceau devient un lapin, puis s'enfuit.",
            "enfant-m|Il part !",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ici, ça court trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Le grillon se tait, d'un coup.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, sur le plastique.",
            "maman|Tu vois comment, Nino ?",
            "narrateur|Nino pose la lampe, sans tout allumer.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "tapis,laine",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Nino pose la lampe au milieu du tapis.",
            "enfant-m|Ici, c'est la clairière, maman.",
            "narrateur|Il pose tout d'un coup, trop vite.",
            "narrateur|Le faisceau roule, et le rond se perd.",
            "enfant-m|Elle file !",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Ici, ça glisse trop.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|La lampe refuse de rester, dans la laine.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, trop loin.",
            "papa|Tu vois comment, Nino ?",
            "narrateur|Nino pose les mains, sans tout jeter.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "bois,matelas",
        "emphasis": "pied du lit",
        "passage": [
            "narrateur|Nino glisse la lampe au pied du lit.",
            "enfant-m|Ici, c'est la grotte, papa.",
            "narrateur|Le bois du lit rend chaque pas.",
            "narrateur|Le rond grimpe au bois, trop haut, trop vite.",
            "enfant-m|Elle tombe !",
            "narrateur|Son sourire s'en va.",
            "narrateur|Sa poitrine serre, trop vite.",
            "papa|Tes genoux font trop de vagues.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Le bois grogne, et la lampe veut se cacher.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, trop bas.",
            "maman|Tu vois comment, Nino ?",
            "narrateur|Nino s'assoit, la lampe au creux.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "rideau,fermeture",
        "emphasis": "sac",
        "passage": [
            "narrateur|Nino traîne le sac vers le rideau.",
            "enfant-m|Le camp, c'est là, maman !",
            "narrateur|Il pousse trop fort, trop vite.",
            "narrateur|Le sac cogne le rebord, clic trop fort.",
            "enfant-m|Il part !",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Ici, ça tape trop.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|La fermeture s'accroche au rideau, trop serrée.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, près du clic.",
            "papa|Tu vois comment, Nino ?",
            "narrateur|Nino pose le sac, sans tout tirer.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "tapis,sac",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Nino déroule le sac au milieu du tapis.",
            "enfant-m|Ici, c'est la clairière, papa.",
            "narrateur|Il jette le vert d'un coup, trop vite.",
            "narrateur|Le sac glisse, trop pressé, trop plat.",
            "enfant-m|Il file !",
            "narrateur|Nino ne rit plus.",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "papa|Ici, ça glisse trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|La fermeture reste coincée, trop serrée.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, trop loin.",
            "maman|Tu vois comment, Nino ?",
            "narrateur|Nino pose le sac, sans tout ouvrir.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "bois,sac",
        "emphasis": "pied du lit",
        "passage": [
            "narrateur|Nino pousse le sac au pied du lit.",
            "enfant-m|Ici, c'est la grotte, maman.",
            "narrateur|Le bois du lit rend chaque pas.",
            "narrateur|Le sac se faufile sous le bois, tout seul.",
            "enfant-m|Il disparaît !",
            "narrateur|Son sourire s'en va.",
            "narrateur|Sa poitrine serre, trop vite.",
            "maman|Tes genoux font trop de vagues.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Le sac refuse d'avoir une forme, trop loin.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, trop bas.",
            "papa|Tu vois comment, Nino ?",
            "narrateur|Nino s'assoit, le sac au creux.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "rideau,coton",
        "emphasis": "oreiller",
        "passage": [
            "narrateur|Nino pousse l'oreiller vers le rideau.",
            "enfant-m|Le camp, c'est là, papa !",
            "narrateur|Il lance les rayures, trop vite, trop haut.",
            "narrateur|L'oreiller tape le bois, rebondit trop haut.",
            "enfant-m|Il part !",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ici, ça rebondit trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Le rideau avale une rayure, trop vite.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, sur la lampe.",
            "maman|Tu vois comment, Nino ?",
            "narrateur|Nino pose l'oreiller, sans tout jeter.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "tapis,laine",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Nino jette l'oreiller au milieu du tapis.",
            "enfant-m|Ici, c'est la clairière, maman.",
            "narrateur|Il jette tout d'un coup, trop vite.",
            "narrateur|L'oreiller file, une rayure après l'autre.",
            "enfant-m|Il file !",
            "narrateur|Nino ne rit plus.",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "maman|Ici, ça glisse trop.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Un fil de laine se lève, puis retombe.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, trop loin.",
            "papa|Tu vois comment, Nino ?",
            "narrateur|Nino pose l'oreiller, sans tout lancer.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "bois,coton",
        "emphasis": "pied du lit",
        "passage": [
            "narrateur|Nino pose l'oreiller au pied du lit.",
            "enfant-m|Ici, c'est la grotte, papa.",
            "narrateur|Le bois du lit rend chaque pas.",
            "narrateur|L'oreiller disparaît sous le drap, trop loin.",
            "enfant-m|Je le perds !",
            "narrateur|Son sourire s'en va.",
            "narrateur|Sa poitrine serre, trop vite.",
            "papa|Tes genoux font trop de vagues.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Le matelas refuse, trop mou, trop loin.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de savon luit, trop bas.",
            "maman|Tu vois comment, Nino ?",
            "narrateur|Nino s'assoit, l'oreiller au creux.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
}

T3_LABS = {
    1: ("les lucioles", "le rideau calme", "maman tient"),
    2: ("le sentier", "la fermeture", "papa ouvre"),
    3: ("les vagues", "le matelas", "maman borde"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le lapin de lumière court, trop vite.",
        "papa|Les lucioles, le rideau, ou maman ?",
    ],
    2: [
        "narrateur|Le sac n'a pas de forme, trop vite.",
        "maman|Le sentier, la fermeture, ou papa ?",
    ],
    3: [
        "narrateur|Le bois du lit tremble, trop vite.",
        "papa|Les vagues, le matelas, ou maman ?",
    ],
}

T3_SONS = {
    (1, 1): "lampe,rideau",
    (1, 2): "rideau,volet",
    (1, 3): "mains,rideau",
    (2, 1): "pas,tapis",
    (2, 2): "fermeture,clic",
    (2, 3): "sac,mains",
    (3, 1): "bois,vague",
    (3, 2): "matelas,drap",
    (3, 3): "maman,sac",
}

T3_EMPH = {
    1: {1: "lucioles", 2: "rideau", 3: "maman"},
    2: {1: "sentier", 2: "fermeture", 3: "papa"},
    3: {1: "vagues", 2: "matelas", 3: "maman"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|On joue aux lucioles.",
        "papa|Toi tu clignes, moi je compte.",
        "narrateur|Nino cligne la lampe, un, deux, trois.",
        "narrateur|Des points d'or s'allument sur le rideau.",
        "enfant-m|Pas tout le faisceau d'un coup.",
        "narrateur|Il s'arrête, l'écaille de savon luit.",
        "narrateur|Le lapin de lumière a failli tout manger.",
        "maman|Un clignotement, puis on pose.",
        "narrateur|Nino cligne une fois, puis pose.",
        "papa|Tu as dansé, puis tu as posé.",
        "enfant-m|Les lucioles sont fatiguées.",
        "maman|L'écaille a dit la dose.",
    ],
    (1, 1, 2): [
        "enfant-m|On attend le rideau.",
        "narrateur|Nino pose les genoux au parquet.",
        "narrateur|La lampe repose contre le rebord, éteinte.",
        "enfant-m|Un rai, pas toute la rue.",
        "narrateur|Il regarde l'écaille de savon, toute mince.",
        "maman|Quand le tissu se tait, tu allumes.",
        "narrateur|Le volet tape une fois, puis plus.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Nino rallume, tout droit, tout petit.",
        "enfant-m|Le camp peut s'ouvrir.",
        "narrateur|Le rideau a failli tout cacher.",
        "maman|Tu as attendu le tissu, Nino.",
    ],
    (1, 1, 3): [
        "enfant-m|Maman, tu tiens, s'il te plaît ?",
        "maman|Je tiens, tu poses le camp.",
        "narrateur|Maman prend la lampe, Nino tend le sac.",
        "enfant-m|Toi tu tiens, moi je range.",
        "narrateur|Nino étale le sac sous le rai de rue.",
        "narrateur|Le faisceau reste sage, dans sa main.",
        "papa|L'écaille de savon reste sur le plastique.",
        "narrateur|Le camp a failli filer avec le rideau.",
        "maman|Ma main fait le piquet, ce soir.",
        "narrateur|La fenêtre garde un rai, tout mince.",
        "enfant-m|Sans tout lancer, ça tient.",
        "papa|Tu as demandé, elle a tenu.",
    ],
    (1, 2, 1): [
        "enfant-m|On fait un sentier.",
        "papa|Toi tu poses, moi je suis derrière.",
        "narrateur|Nino pose la lampe, un pas, puis un autre.",
        "narrateur|Des pas dessinent un chemin sur le tapis.",
        "enfant-m|Pas tout le tapis d'un coup.",
        "narrateur|Il s'arrête, l'écaille de savon luit.",
        "narrateur|Le faisceau a failli tout rouler.",
        "maman|Un pas, puis on pose.",
        "narrateur|Nino pose le rond, tout petit.",
        "papa|Tu as marché, sans tout jeter.",
        "enfant-m|Le sentier est fatigué.",
        "maman|L'écaille a dit la dose.",
    ],
    (1, 2, 2): [
        "enfant-m|J'attends la fermeture.",
        "papa|Moi j'écoute le clic, puis c'est toi.",
        "narrateur|Nino tient la lampe, le sac attend.",
        "narrateur|La fermeture avance, trop mince, trop sage.",
        "enfant-m|Pas tout le sac d'un coup.",
        "narrateur|Il souffle, les épaules baissent.",
        "narrateur|L'écaille de savon luit, trop près du clic.",
        "maman|D'abord le clic, ensuite la lampe.",
        "papa|C'est à toi, Nino.",
        "enfant-m|J'y pose le rond, un peu.",
        "narrateur|Nino pose une fois, puis s'arrête.",
        "papa|Sans tout ouvrir, ça tient.",
    ],
    (1, 2, 3): [
        "enfant-m|Papa, tu ouvres le sac ?",
        "papa|Je l'ouvre, un peu.",
        "narrateur|Papa ouvre le sac, Nino tient la lampe.",
        "enfant-m|Pas tout, papa.",
        "narrateur|Nino glisse le rond, les mains posées.",
        "narrateur|L'autre main suit, le tapis au calme.",
        "maman|L'écaille de savon reste sur le plastique.",
        "narrateur|Le sac a failli tout avaler.",
        "enfant-m|Toi tu ouvres, moi je pose.",
        "narrateur|Le rond tombe, le camp se tient.",
        "papa|Le sac tient tout seul, maintenant.",
        "maman|Tu as dit stop, Nino.",
    ],
    (1, 3, 1): [
        "enfant-m|On fait des vagues.",
        "papa|Tu rebondis, puis tu poses.",
        "narrateur|La lampe voyage d'un genou à l'autre.",
        "narrateur|Le bois penche, puis se tient droit.",
        "enfant-m|Les vagues tiennent, puis je pose.",
        "narrateur|Nino s'arrête, l'écaille de savon luit.",
        "narrateur|La lampe a failli tomber, trop haut.",
        "maman|Une vague, puis on pose un peu.",
        "narrateur|Nino pose le rond, au pied du lit.",
        "papa|Le bois est devenu une grotte, maintenant.",
        "enfant-m|Le camp est là, tout bas.",
        "maman|Sans tout verser, ça tient.",
    ],
    (1, 3, 2): [
        "enfant-m|On attend le matelas.",
        "papa|Un, deux, trois, tu poses.",
        "narrateur|Une vague, puis le bois reste sage.",
        "narrateur|La lampe reste sage, au creux des mains.",
        "enfant-m|Pas tout le rond d'un coup.",
        "narrateur|Le compte se tait, enfin.",
        "enfant-m|Maintenant, un peu !",
        "narrateur|Nino pose, un cercle, puis s'arrête.",
        "narrateur|L'écaille de savon luit, au creux.",
        "papa|Tes genoux se sont assis, eux aussi.",
        "narrateur|Un pli du drap retombe, sans bruit.",
        "maman|Le camp a sa lumière, d'en bas.",
    ],
    (1, 3, 3): [
        "enfant-m|Maman, tu bordes le sac ?",
        "maman|Je le borde, tout droit.",
        "narrateur|Maman borde le sac, Nino tient la lampe.",
        "enfant-m|Un peu, pas tout.",
        "narrateur|Nino écoute les mains, plus que ses pieds.",
        "papa|Tu poses, et ça tient.",
        "narrateur|L'écaille de savon luit, trop près du nez.",
        "narrateur|Le sac a failli glisser, trop loin.",
        "enfant-m|Moi aussi, j'écoute.",
        "narrateur|Le rond tombe, vu d'en bas.",
        "maman|Tu as demandé, je borde.",
        "papa|Tes mains ont tenu le plastique.",
    ],
    (2, 1, 1): [
        "enfant-m|On joue aux lucioles.",
        "papa|Toi tu clignes, le sac fait colline.",
        "narrateur|Nino cligne, le sac devient une colline.",
        "narrateur|Des points d'or s'allument sur le vert.",
        "enfant-m|Pas tout le faisceau d'un coup.",
        "narrateur|Il s'arrête, l'écaille de savon luit.",
        "narrateur|Le sac a failli tout cacher.",
        "maman|Un clignotement, puis on pose.",
        "narrateur|Nino cligne une fois, puis pose.",
        "papa|Tu as dansé, sans tout tirer.",
        "enfant-m|Les lucioles sont fatiguées.",
        "maman|L'écaille a dit la dose.",
    ],
    (2, 1, 2): [
        "enfant-m|On attend le rideau.",
        "narrateur|Nino pose les genoux au parquet.",
        "narrateur|Le sac repose contre le rebord, plié.",
        "enfant-m|Un rai, pas toute la rue.",
        "narrateur|Il regarde l'écaille de savon, près du clic.",
        "maman|Quand le tissu se tait, tu ouvres.",
        "narrateur|Le volet tape une fois, puis plus.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Nino ouvre un peu, tout petit.",
        "enfant-m|Le camp peut s'ouvrir.",
        "narrateur|Le rideau a failli tout cacher.",
        "maman|Tu as attendu le tissu, Nino.",
    ],
    (2, 1, 3): [
        "enfant-m|Maman, tu tiens, s'il te plaît ?",
        "maman|Je tiens, tu poses le camp.",
        "narrateur|Maman tient le sac, Nino tend la lampe.",
        "enfant-m|Toi tu tiens, moi je range.",
        "narrateur|Nino étale le vert sous le rai de rue.",
        "narrateur|La fermeture reste sage, dans sa main.",
        "papa|L'écaille de savon reste près du clic.",
        "narrateur|Le camp a failli filer avec le rideau.",
        "maman|Ma main fait le piquet, ce soir.",
        "narrateur|La fenêtre garde un rai, tout mince.",
        "enfant-m|Sans tout tirer, ça tient.",
        "papa|Tu as demandé, elle a tenu.",
    ],
    (2, 2, 1): [
        "enfant-m|On fait un sentier.",
        "papa|Toi tu poses, moi je suis derrière.",
        "narrateur|Nino pose le sac, un pas, puis un autre.",
        "narrateur|Des pas dessinent un chemin sur le tapis.",
        "enfant-m|Pas tout le tapis d'un coup.",
        "narrateur|Il s'arrête, l'écaille de savon luit.",
        "narrateur|Le sac a failli tout glisser.",
        "maman|Un pas, puis on pose.",
        "narrateur|Nino pose le vert, tout petit.",
        "papa|Tu as marché, sans tout jeter.",
        "enfant-m|Le sentier est fatigué.",
        "maman|L'écaille a dit la dose.",
    ],
    (2, 2, 2): [
        "enfant-m|J'attends la fermeture.",
        "papa|Moi j'écoute le clic, puis c'est toi.",
        "narrateur|Nino tient le sac, le clic attend.",
        "narrateur|La fermeture avance, trop mince, trop sage.",
        "enfant-m|Pas tout le sac d'un coup.",
        "narrateur|Il souffle, les épaules baissent.",
        "narrateur|L'écaille de savon luit, trop près du clic.",
        "maman|D'abord le clic, ensuite le camp.",
        "papa|C'est à toi, Nino.",
        "enfant-m|J'ouvre un peu, un cran.",
        "narrateur|Nino ouvre une fois, puis s'arrête.",
        "papa|Sans tout ouvrir, ça tient.",
    ],
    (2, 2, 3): [
        "enfant-m|Papa, tu ouvres le sac ?",
        "papa|Je l'ouvre, un peu.",
        "narrateur|Papa ouvre le sac, Nino tient le bord.",
        "enfant-m|Pas tout, papa.",
        "narrateur|Nino glisse les mains, posées.",
        "narrateur|L'autre main suit, le tapis au calme.",
        "maman|L'écaille de savon reste près du clic.",
        "narrateur|Le sac a failli tout avaler.",
        "enfant-m|Toi tu ouvres, moi je pose.",
        "narrateur|Le vert s'ouvre, le camp se tient.",
        "papa|Le sac tient tout seul, maintenant.",
        "maman|Tu as dit stop, Nino.",
    ],
    (2, 3, 1): [
        "enfant-m|On fait des vagues.",
        "papa|Tu rebondis, puis tu poses.",
        "narrateur|Le sac voyage d'un genou à l'autre.",
        "narrateur|Le bois penche, puis se tient droit.",
        "enfant-m|Les vagues tiennent, puis je pose.",
        "narrateur|Nino s'arrête, l'écaille de savon luit.",
        "narrateur|Le sac a failli filer sous le bois.",
        "maman|Une vague, puis on pose un peu.",
        "narrateur|Nino pose le vert, au pied du lit.",
        "papa|Le bois est devenu une grotte, maintenant.",
        "enfant-m|Le camp est là, tout bas.",
        "maman|Sans tout pousser, ça tient.",
    ],
    (2, 3, 2): [
        "enfant-m|On attend le matelas.",
        "papa|Un, deux, trois, tu poses.",
        "narrateur|Une vague, puis le bois reste sage.",
        "narrateur|Le sac reste sage, au creux des genoux.",
        "enfant-m|Pas tout le vert d'un coup.",
        "narrateur|Le compte se tait, enfin.",
        "enfant-m|Maintenant, un peu !",
        "narrateur|Nino ouvre, un cran, puis s'arrête.",
        "narrateur|L'écaille de savon luit, au creux.",
        "papa|Tes genoux se sont assis, eux aussi.",
        "narrateur|Un pli du drap retombe, sans bruit.",
        "maman|Le camp a sa tente, d'en bas.",
    ],
    (2, 3, 3): [
        "enfant-m|Maman, tu bordes le sac ?",
        "maman|Je le borde, tout droit.",
        "narrateur|Maman borde le sac, Nino tient le bord.",
        "enfant-m|Un peu, pas tout.",
        "narrateur|Nino écoute les mains, plus que ses pieds.",
        "papa|Tu poses, et ça tient.",
        "narrateur|L'écaille de savon luit, trop près du nez.",
        "narrateur|Le sac a failli glisser, trop loin.",
        "enfant-m|Moi aussi, j'écoute.",
        "narrateur|Le vert se tient, vu d'en bas.",
        "maman|Tu as demandé, je borde.",
        "papa|Tes mains ont tenu la fermeture.",
    ],
    (3, 1, 1): [
        "enfant-m|On joue aux lucioles.",
        "papa|Toi tu clignes, l'oreiller fait nuage.",
        "narrateur|Nino cligne, l'oreiller devient un nuage.",
        "narrateur|Des points d'or s'allument sur les rayures.",
        "enfant-m|Pas tout le faisceau d'un coup.",
        "narrateur|Il s'arrête, l'écaille de savon luit.",
        "narrateur|L'oreiller a failli tout cacher.",
        "maman|Un clignotement, puis on pose.",
        "narrateur|Nino cligne une fois, puis pose.",
        "papa|Tu as dansé, sans tout lancer.",
        "enfant-m|Les lucioles sont fatiguées.",
        "maman|L'écaille a dit la dose.",
    ],
    (3, 1, 2): [
        "enfant-m|On attend le rideau.",
        "narrateur|Nino pose les genoux au parquet.",
        "narrateur|L'oreiller repose contre le rebord, sage.",
        "enfant-m|Un rai, pas toute la rue.",
        "narrateur|Il regarde l'écaille de savon, sur la lampe.",
        "maman|Quand le tissu se tait, tu poses.",
        "narrateur|Le volet tape une fois, puis plus.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Nino pose les rayures, tout petit.",
        "enfant-m|Le camp peut s'ouvrir.",
        "narrateur|Le rideau a failli tout cacher.",
        "maman|Tu as attendu le tissu, Nino.",
    ],
    (3, 1, 3): [
        "enfant-m|Maman, tu tiens, s'il te plaît ?",
        "maman|Je tiens, tu poses le camp.",
        "narrateur|Maman tient l'oreiller, Nino tend la lampe.",
        "enfant-m|Toi tu tiens, moi je range.",
        "narrateur|Nino étale le sac sous le rai de rue.",
        "narrateur|Les rayures restent sages, dans sa main.",
        "papa|L'écaille de savon reste sur le plastique.",
        "narrateur|Le camp a failli filer avec le rideau.",
        "maman|Ma main fait le piquet, ce soir.",
        "narrateur|La fenêtre garde un rai, tout mince.",
        "enfant-m|Sans tout lancer, ça tient.",
        "papa|Tu as demandé, elle a tenu.",
    ],
    (3, 2, 1): [
        "enfant-m|On fait un sentier.",
        "papa|Toi tu poses, moi je suis derrière.",
        "narrateur|Nino pose l'oreiller, un pas, puis un autre.",
        "narrateur|Des pas dessinent un chemin sur le tapis.",
        "enfant-m|Pas tout le tapis d'un coup.",
        "narrateur|Il s'arrête, l'écaille de savon luit.",
        "narrateur|L'oreiller a failli tout filer.",
        "maman|Un pas, puis on pose.",
        "narrateur|Nino pose les rayures, tout petit.",
        "papa|Tu as marché, sans tout jeter.",
        "enfant-m|Le sentier est fatigué.",
        "maman|L'écaille a dit la dose.",
    ],
    (3, 2, 2): [
        "enfant-m|J'attends la fermeture.",
        "papa|Moi j'écoute le clic, puis c'est toi.",
        "narrateur|Nino tient l'oreiller, le sac attend.",
        "narrateur|La fermeture avance, trop mince, trop sage.",
        "enfant-m|Pas tout le sac d'un coup.",
        "narrateur|Il souffle, les épaules baissent.",
        "narrateur|L'écaille de savon luit, trop près du clic.",
        "maman|D'abord le clic, ensuite l'oreiller.",
        "papa|C'est à toi, Nino.",
        "enfant-m|J'y pose les rayures, un peu.",
        "narrateur|Nino pose une fois, puis s'arrête.",
        "papa|Sans tout ouvrir, ça tient.",
    ],
    (3, 2, 3): [
        "enfant-m|Papa, tu ouvres le sac ?",
        "papa|Je l'ouvre, un peu.",
        "narrateur|Papa ouvre le sac, Nino tient l'oreiller.",
        "enfant-m|Pas tout, papa.",
        "narrateur|Nino glisse les rayures, les mains posées.",
        "narrateur|L'autre main suit, le tapis au calme.",
        "maman|L'écaille de savon reste sur la lampe.",
        "narrateur|Le sac a failli tout avaler.",
        "enfant-m|Toi tu ouvres, moi je pose.",
        "narrateur|Les rayures tombent, le camp se tient.",
        "papa|Le sac tient tout seul, maintenant.",
        "maman|Tu as dit stop, Nino.",
    ],
    (3, 3, 1): [
        "enfant-m|On fait des vagues.",
        "papa|Tu rebondis, puis tu poses.",
        "narrateur|L'oreiller voyage d'un genou à l'autre.",
        "narrateur|Le bois penche, puis se tient droit.",
        "enfant-m|Les vagues tiennent, puis je pose.",
        "narrateur|Nino s'arrête, l'écaille de savon luit.",
        "narrateur|L'oreiller a failli filer sous le drap.",
        "maman|Une vague, puis on pose un peu.",
        "narrateur|Nino pose les rayures, au pied du lit.",
        "papa|Le bois est devenu une grotte, maintenant.",
        "enfant-m|Le camp est là, tout bas.",
        "maman|Sans tout lancer, ça tient.",
    ],
    (3, 3, 2): [
        "enfant-m|On attend le matelas.",
        "papa|Un, deux, trois, tu poses.",
        "narrateur|Une vague, puis le bois reste sage.",
        "narrateur|L'oreiller reste sage, au creux des mains.",
        "enfant-m|Pas toutes les rayures d'un coup.",
        "narrateur|Le compte se tait, enfin.",
        "enfant-m|Maintenant, un peu !",
        "narrateur|Nino pose, un coin, puis s'arrête.",
        "narrateur|L'écaille de savon luit, au creux.",
        "papa|Tes genoux se sont assis, eux aussi.",
        "narrateur|Un pli du drap retombe, sans bruit.",
        "maman|Le camp a son nuage, d'en bas.",
    ],
    (3, 3, 3): [
        "enfant-m|Maman, tu bordes le sac ?",
        "maman|Je le borde, tout droit.",
        "narrateur|Maman borde le sac, Nino tient l'oreiller.",
        "enfant-m|Un peu, pas tout.",
        "narrateur|Nino écoute les mains, plus que ses pieds.",
        "papa|Tu poses, et ça tient.",
        "narrateur|L'écaille de savon luit, trop près du nez.",
        "narrateur|Le sac a failli glisser, trop loin.",
        "enfant-m|Moi aussi, j'écoute.",
        "narrateur|Les rayures se tiennent, vu d'en bas.",
        "maman|Tu as demandé, je borde.",
        "papa|Tes mains ont tenu le coton.",
    ],
}

END_SONS = {1: "rideau,grillon", 2: "tapis,laine", 3: "bois,matelas"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Nino s'allonge, le sac sous le rideau.",
        "enfant-m|Les lucioles sont devenues un camp.",
        "papa|Tu raconteras aussi le moment difficile ?",
        "enfant-m|Surtout celui-là.",
        "maman|Le camp a sa lumière.",
        "narrateur|Ça a failli tout manger.",
        "narrateur|L'écaille de savon tient, sur le plastique.",
        "papa|Tu as cligné un peu, Nino.",
        "narrateur|Le rideau garde trois points d'or, trop petits.",
    ],
    (1, 1, 2): [
        "narrateur|Nino s'allonge, le rideau sage.",
        "enfant-m|J'ai attendu le tissu, d'abord.",
        "papa|Puis la lampe est restée droite.",
        "maman|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le grillon reprend, tout bas.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|Le rai est à nous.",
        "papa|Un rai a suffi, Nino.",
        "narrateur|Le volet s'est tu, le rai reste mince.",
    ],
    (1, 1, 3): [
        "narrateur|Nino s'allonge, la main de maman tout près.",
        "enfant-m|Tu tenais la lampe.",
        "papa|Tu demandais, maman tenait.",
        "maman|Ma main a fait le piquet.",
        "narrateur|Ça a failli tout filer.",
        "narrateur|L'écaille de savon reste au doigt.",
        "enfant-m|Il est à nous.",
        "papa|Toi tu rangeais, elle tenait.",
        "narrateur|La main de maman fait un piquet, près du verre.",
    ],
    (1, 2, 1): [
        "narrateur|Nino s'allonge au bout du sentier.",
        "enfant-m|Toi tu suivais, moi je posais.",
        "papa|Tes pas ont fait le camp.",
        "maman|Le tapis est devenu une clairière.",
        "narrateur|Ça a failli tout rouler.",
        "narrateur|L'écaille de savon luit, trop mince.",
        "enfant-m|Le sentier reste, maman.",
        "papa|Un pas, puis un autre.",
        "narrateur|Le tapis garde un sentier de lumière, trop mince.",
    ],
    (1, 2, 2): [
        "narrateur|Nino s'allonge dans le sac ouvert.",
        "papa|J'ai écouté, puis c'était toi.",
        "enfant-m|J'ai attendu le clic.",
        "maman|D'abord le clic, ensuite la lampe.",
        "narrateur|Le camp tient, enfin.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|C'est chaud, tout au fond.",
        "papa|Sans tout ouvrir, ça tient.",
        "narrateur|La fermeture brille, un clic tiède au creux.",
    ],
    (1, 2, 3): [
        "narrateur|Nino s'allonge, le sac ouvert par papa.",
        "enfant-m|Tu ouvrais, un peu.",
        "papa|Le sac s'est ouvert, juste assez.",
        "maman|Le camp a sa tente, à vous.",
        "narrateur|Ça a failli tout avaler.",
        "narrateur|L'écaille de savon reste sur le plastique.",
        "enfant-m|Regarde, papa, elle brille.",
        "maman|Tu as dit stop, à temps.",
        "narrateur|Le sac ouvert par papa tient un rond de lampe.",
    ],
    (1, 3, 1): [
        "narrateur|Nino s'allonge au pied du lit.",
        "enfant-m|Les vagues sont finies, papa.",
        "papa|Tu rebondissais, puis tu posais.",
        "maman|La grotte a sa lumière, ici.",
        "narrateur|Ça a failli tout tomber.",
        "narrateur|L'écaille de savon tient, trop bas.",
        "enfant-m|Les vagues se taisent.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le bois du lit tient un rond, sans vague.",
    ],
    (1, 3, 2): [
        "narrateur|Nino s'allonge, après le compte.",
        "enfant-m|On a attendu le bois.",
        "papa|Quand il s'est tu, tu as posé.",
        "maman|Le matelas a fait un camp.",
        "narrateur|Tes genoux se sont assis.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|J'ai compté, c'était bon.",
        "papa|Un, deux, trois, puis le rond.",
        "narrateur|Le matelas garde un cercle tiède, au creux.",
    ],
    (1, 3, 3): [
        "narrateur|Nino s'allonge, le sac bordé par maman.",
        "enfant-m|J'écoutais tes mains.",
        "papa|Moi aussi, je bordais avec toi.",
        "maman|Tu as demandé, j'ai bordé.",
        "narrateur|Ça a failli trop glisser.",
        "narrateur|L'écaille de savon luit, tout près.",
        "enfant-m|Il est à nous, maman.",
        "papa|Tes mains ont tenu le plastique.",
        "narrateur|Le sac bordé tient la lampe, tout droit.",
    ],
    (2, 1, 1): [
        "narrateur|Nino s'allonge, le sac sous le rideau.",
        "enfant-m|La colline est devenue un camp.",
        "papa|Tu raconteras aussi le moment difficile ?",
        "enfant-m|Surtout celui-là.",
        "maman|Le camp a sa lumière.",
        "narrateur|Ça a failli tout cacher.",
        "narrateur|L'écaille de savon tient, près du clic.",
        "papa|Tu as cligné un peu, Nino.",
        "narrateur|Le sac vert fait colline, sous trois points d'or.",
    ],
    (2, 1, 2): [
        "narrateur|Nino s'allonge, le rideau sage.",
        "enfant-m|J'ai attendu le tissu, d'abord.",
        "papa|Puis le sac est resté plié.",
        "maman|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le grillon reprend, tout bas.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|Le rai est à nous.",
        "papa|Un rai a suffi, Nino.",
        "narrateur|Le sac plié sent le savon, sous le rai.",
    ],
    (2, 1, 3): [
        "narrateur|Nino s'allonge, la main de maman tout près.",
        "enfant-m|Tu tenais le sac.",
        "papa|Tu demandais, maman tenait.",
        "maman|Ma main a fait le piquet.",
        "narrateur|Ça a failli tout filer.",
        "narrateur|L'écaille de savon reste au doigt.",
        "enfant-m|Il est à nous.",
        "papa|Toi tu rangeais, elle tenait.",
        "narrateur|Le vert du sac touche la main de maman.",
    ],
    (2, 2, 1): [
        "narrateur|Nino s'allonge au bout du sentier.",
        "enfant-m|Toi tu suivais, moi je posais.",
        "papa|Tes pas ont fait le camp.",
        "maman|Le tapis est devenu une clairière.",
        "narrateur|Ça a failli tout glisser.",
        "narrateur|L'écaille de savon luit, trop mince.",
        "enfant-m|Le sentier reste, maman.",
        "papa|Un pas, puis un autre.",
        "narrateur|Le sac marque le bout du sentier, vert.",
    ],
    (2, 2, 2): [
        "narrateur|Nino s'allonge dans le sac ouvert.",
        "papa|J'ai écouté, puis c'était toi.",
        "enfant-m|J'ai attendu le clic.",
        "maman|D'abord le clic, ensuite le camp.",
        "narrateur|Le camp tient, enfin.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|C'est chaud, tout au fond.",
        "papa|Sans tout ouvrir, ça tient.",
        "narrateur|Un clic dort près de l'écaille, sur le vert.",
    ],
    (2, 2, 3): [
        "narrateur|Nino s'allonge, le sac ouvert par papa.",
        "enfant-m|Tu ouvrais, un peu.",
        "papa|Le sac s'est ouvert, juste assez.",
        "maman|Le camp a sa tente, à vous.",
        "narrateur|Ça a failli tout avaler.",
        "narrateur|L'écaille de savon reste près du clic.",
        "enfant-m|Regarde, papa, elle brille.",
        "maman|Tu as dit stop, à temps.",
        "narrateur|Les mains de papa restent sur la fermeture.",
    ],
    (2, 3, 1): [
        "narrateur|Nino s'allonge au pied du lit.",
        "enfant-m|Les vagues sont finies, papa.",
        "papa|Tu rebondissais, puis tu posais.",
        "maman|La grotte a sa tente, ici.",
        "narrateur|Ça a failli tout filer.",
        "narrateur|L'écaille de savon tient, trop bas.",
        "enfant-m|Les vagues se taisent.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le vert du sac ne danse plus, sous le bois.",
    ],
    (2, 3, 2): [
        "narrateur|Nino s'allonge, après le compte.",
        "enfant-m|On a attendu le bois.",
        "papa|Quand il s'est tu, tu as ouvert.",
        "maman|Le matelas a fait un camp.",
        "narrateur|Tes genoux se sont assis.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|J'ai compté, un cran.",
        "papa|Un, deux, trois, puis le vert.",
        "narrateur|Le sac ouvert attend, plat, au pied du lit.",
    ],
    (2, 3, 3): [
        "narrateur|Nino s'allonge, le sac bordé par maman.",
        "enfant-m|J'écoutais tes mains.",
        "papa|Moi aussi, je bordais avec toi.",
        "maman|Tu as demandé, j'ai bordé.",
        "narrateur|Ça a failli trop glisser.",
        "narrateur|L'écaille de savon luit, tout près.",
        "enfant-m|Il est à nous, maman.",
        "papa|Tes mains ont tenu la fermeture.",
        "narrateur|Le bord du sac sent la main de maman.",
    ],
    (3, 1, 1): [
        "narrateur|Nino s'allonge, le sac sous le rideau.",
        "enfant-m|Le nuage est devenu un camp.",
        "papa|Tu raconteras aussi le moment difficile ?",
        "enfant-m|Surtout celui-là.",
        "maman|Le camp a sa lumière.",
        "narrateur|Ça a failli tout cacher.",
        "narrateur|L'écaille de savon tient, sur la lampe.",
        "papa|Tu as cligné un peu, Nino.",
        "narrateur|Les rayures reçoivent trois points d'or, puis plus.",
    ],
    (3, 1, 2): [
        "narrateur|Nino s'allonge, le rideau sage.",
        "enfant-m|J'ai attendu le tissu, d'abord.",
        "papa|Puis l'oreiller est resté sage.",
        "maman|Tes pieds se sont assis, eux aussi.",
        "narrateur|Le grillon reprend, tout bas.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|Le rai est à nous.",
        "papa|Un rai a suffi, Nino.",
        "narrateur|L'oreiller rayé garde le rai, contre le rebord.",
    ],
    (3, 1, 3): [
        "narrateur|Nino s'allonge, la main de maman tout près.",
        "enfant-m|Tu tenais l'oreiller.",
        "papa|Tu demandais, maman tenait.",
        "maman|Ma main a fait le piquet.",
        "narrateur|Ça a failli tout filer.",
        "narrateur|L'écaille de savon reste au doigt.",
        "enfant-m|Il est à nous.",
        "papa|Toi tu rangeais, elle tenait.",
        "narrateur|Les rayures touchent la main de maman, près du verre.",
    ],
    (3, 2, 1): [
        "narrateur|Nino s'allonge au bout du sentier.",
        "enfant-m|Toi tu suivais, moi je posais.",
        "papa|Tes pas ont fait le camp.",
        "maman|Le tapis est devenu une clairière.",
        "narrateur|Ça a failli tout filer.",
        "narrateur|L'écaille de savon luit, trop mince.",
        "enfant-m|Le sentier reste, maman.",
        "papa|Un pas, puis un autre.",
        "narrateur|L'oreiller attend au bout du sentier, rayé.",
    ],
    (3, 2, 2): [
        "narrateur|Nino s'allonge dans le sac ouvert.",
        "papa|J'ai écouté, puis c'était toi.",
        "enfant-m|J'ai attendu le clic.",
        "maman|D'abord le clic, ensuite l'oreiller.",
        "narrateur|Le camp tient, enfin.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|C'est chaud, tout au fond.",
        "papa|Sans tout ouvrir, ça tient.",
        "narrateur|Une rayure passe sous la fermeture, tiède.",
    ],
    (3, 2, 3): [
        "narrateur|Nino s'allonge, le sac ouvert par papa.",
        "enfant-m|Tu ouvrais, un peu.",
        "papa|Le sac s'est ouvert, juste assez.",
        "maman|Le camp a sa tente, à vous.",
        "narrateur|Ça a failli tout avaler.",
        "narrateur|L'écaille de savon reste sur la lampe.",
        "enfant-m|Regarde, papa, elle brille.",
        "maman|Tu as dit stop, à temps.",
        "narrateur|L'oreiller rayé s'adosse au sac ouvert par papa.",
    ],
    (3, 3, 1): [
        "narrateur|Nino s'allonge au pied du lit.",
        "enfant-m|Les vagues sont finies, papa.",
        "papa|Tu rebondissais, puis tu posais.",
        "maman|La grotte a son nuage, ici.",
        "narrateur|Ça a failli tout filer.",
        "narrateur|L'écaille de savon tient, trop bas.",
        "enfant-m|Les vagues se taisent.",
        "papa|Tes pieds se sont assis, eux aussi.",
        "narrateur|Les rayures ne dansent plus, sous le bois.",
    ],
    (3, 3, 2): [
        "narrateur|Nino s'allonge, après le compte.",
        "enfant-m|On a attendu le bois.",
        "papa|Quand il s'est tu, tu as posé.",
        "maman|Le matelas a fait un camp.",
        "narrateur|Tes genoux se sont assis.",
        "narrateur|L'écaille de savon a séché.",
        "enfant-m|J'ai compté, un coin.",
        "papa|Un, deux, trois, puis les rayures.",
        "narrateur|L'oreiller rayé s'enfonce, sans vague, au creux.",
    ],
    (3, 3, 3): [
        "narrateur|Nino s'allonge, le sac bordé par maman.",
        "enfant-m|J'écoutais tes mains.",
        "papa|Moi aussi, je bordais avec toi.",
        "maman|Tu as demandé, j'ai bordé.",
        "narrateur|Ça a failli trop glisser.",
        "narrateur|L'écaille de savon luit, tout près.",
        "enfant-m|Il est à nous, maman.",
        "papa|Tes mains ont tenu le coton.",
        "narrateur|Une rayure reste sous la main qui borde.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "grillon,savon",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("la lampe torche", "le sac vert", "l'oreiller rayé")},
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
            {"fields": t3lab("la fenêtre", "le tapis", "le pied du lit")},
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
                    {"emphasis": "écaille de savon"},
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
        "cristal de sucre brun",
        "brin de safran",
        "étoile brune",
        "fil pâle",
        "citronnade",
        "chapeau",
        "grain de savon rose",
        "écaille de nacre",
        "écaille d'étain",
        "écaille de lichen",
        "écaille de boue",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "écaille de savon" not in blob:
        raise SystemExit(f"{SID}: écaille de savon absente")
    if "grillon" not in blob:
        raise SystemExit(f"{SID}: grillon absent")

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
    if min(counts) < 500 or max(counts) > 780:
        raise SystemExit(f"chemins hors barre: {min(counts)}-{max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")
    if len(story["chunks"]) != 86:
        raise SystemExit(f"{SID}: {len(story['chunks'])} chunks != 86")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — attendre / doser, pas tout d'un coup (vécue, non dite)\n"
        "- **Personnages :** Nino, papa, maman (un seul enfant ; pas de 2e enfant)\n"
        "- **Lieu :** la chambre de Nino : fenêtre, tapis, pied du lit (camp sous la lampe)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés. Labels T1/T2/T3 gardés.\n\n"
        "## Promesse narrative\n\n"
        "La salle d'eau se tait. Une **écaille de savon** tient sur la lampe torche. "
        "Derrière le volet, un grillon chante comme s'il avait planté sa tente. "
        "Nino veut planter **son** camp dans la chambre, toute la nuit, **d'un coup**, "
        "avant que le grillon se taise. Il prend la lampe, le sac vert ou l'oreiller rayé ; "
        "les trois viennent. À la fenêtre le faisceau court, sur le tapis ça glisse, "
        "au pied du lit les genoux dansent. Une 2e ruse (grillon qui se tait, fermeture "
        "coincée, lampe qui refuse, rideau qui avale, matelas trop mou) : il refuse de "
        "foncer, revoit l'écaille du début. Neuf façons de doser. Le camp tient. "
        "L'écaille dit la dose.\n\n"
        "## Vécu\n\n"
        "Nino veut le camp **maintenant**, tout planter. Papa et maman sont là. "
        "Sourire disparu, poitrine bousculée, adulte accroupi. "
        "Chaque choix change l'obstacle et le climax. La leçon se voit : "
        "tout lancer fait filer le faisceau ; un clignotement, un pas, un clic, "
        "maman qui tient, papa qui ouvre, ça tient. "
        "Indice d'ouverture payé : écaille de savon. Fin : camp + trace unique "
        "(points d'or, rai, piquet, sentier, clic, sac ouvert, rond, cercle, bord).\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien merged F-NAR-016 sans notes/xai : tout réécrit.\n"
        "- Audit générique « deux enfants » ignoré : dump = Nino, papa, maman seulement.\n"
        "- Slogan pédagogique, miel, merle, « encore / déjà / tout doux / tout calme » jetés.\n"
        "- Ouverture inventée (salle d'eau qui se tait, grillon voisin), pas les 5 listées example4.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (écaille vue). Question d'adulte. Un « en ce moment ».\n"
        "- Monde ≠ TREE-DIF-055 (Sarah, citronnade, cuisine) ≠ TREE-DIF-025 (Nina, chapeaux, hall).\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
