#!/usr/bin/env python3
"""TREE-DIF-038 — F-NAR-019. Cheval de bois de Nino, sous l'auvent. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-038"
N1 = 10
TITLE = "Le cheval de bois de Nino, sous l'auvent"
FIL = (
    "Après la pluie, Nino veut que son cheval de bois galope sur les carreaux secs. "
    "Une roue manque. Papa sait où, mais Nino coupe : « Dans le quoi ? » "
    "Le mot rentre. T1 = cheval / boîte ronde / chiffon ; les trois partent. "
    "T2 = établi (copeaux) / coffre (couvercle) / étagère (trop haute). "
    "T3 = neuf façons de laisser la phrase arriver. La roue rentre. Le cheval galope."
)
CHARS = "Nino, papa, maman"
SETTING = "sous l'auvent, après la pluie : établi, coffre, étagère"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "cheval de bois",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=Nino veut galoper maintenant et coupe papa; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la chasse à la roue; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_roue_n_est_pas_là_mais_on_part; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_mot_de_papa_manque; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=la_phrase_de_papa_se_casse; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=la_roue_arrive_quand_on_laisse_finir; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_galop_paie_les_carreaux_du_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Sous l'auvent, une goutte tape le bois.",
    "narrateur|Les carreaux luisent, presque secs.",
    "narrateur|Ça sent le savon, et le pin mouillé.",
    "narrateur|Un copeau jaune dort près du seuil.",
    "narrateur|Le cheval de bois penche sur trois roues.",
    "papa|Tu as vu le cheval, Nino ?",
    "enfant-m|Il veut galoper, là !",
    "maman|Une roue manque, sur le carreau.",
    "narrateur|En ce moment, Nino touche le bois rêche.",
    "enfant-m|Je le fais galoper, maintenant.",
    "papa|La roue est dans le.",
    "narrateur|Papa cherche, la bouche ouverte.",
    "enfant-m|Dans le quoi ?",
    "narrateur|Nino a trop parlé.",
    "narrateur|Les joues de Nino chauffent.",
    "maman|On n'a pas la fin.",
    "papa|Merci, tu as tenu le cheval.",
]

T1_CHOICE = [
    "narrateur|Près du seuil, trois affaires attendent.",
    "narrateur|Le cheval, la boîte, et le chiffon.",
    "papa|Tu prends quoi, d'abord ?",
]

T1 = {
    1: {
        "lab": "le cheval",
        "sons": "bois,goutte",
        "emphasis": "cheval",
        "passage": [
            "narrateur|Nino saisit le cheval, le bois rêche.",
            "enfant-m|Il sent la pluie.",
            "papa|Une goutte reste sur le dos.",
            "narrateur|Elle glisse, puis s'arrête.",
            "narrateur|Nino secoue le cheval, trop vite.",
            "enfant-m|Où est la roue ?",
            "narrateur|Papa ouvre la bouche.",
            "enfant-m|Dans lequel ?",
            "narrateur|Papa referme, les joues chaudes.",
            "maman|La boîte, contre lui, ensuite.",
            "narrateur|Papa pose le chiffon sur l'encolure.",
            "narrateur|Rien ne reste sous l'auvent.",
            "papa|On marche, il va venir.",
        ],
        "question": [
            "narrateur|Nino a pris le cheval, près de lui.",
            "maman|Nino a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "cheval",
            "accepted_examples": "cheval | le cheval | le bois | cheval de bois",
            "retry_prompt": "Nino tient le cheval. Il tient quoi ?",
        },
        "confirm": [
            "enfant-m|Le cheval.",
            "papa|Oui, le bois rêche.",
            "narrateur|La boîte et le chiffon partent avec.",
            "maman|On marche vers le sec.",
            "enfant-m|Je suis prêt.",
            "papa|On y va, alors ?",
            "enfant-m|Oui, papa.",
        ],
        "voy": "Le cheval penche vers les trois coins.",
    },
    2: {
        "lab": "la boîte ronde",
        "sons": "metal,toc",
        "emphasis": "boîte",
        "passage": [
            "narrateur|Nino ouvre la boîte ronde, d'abord.",
            "enfant-m|Elle sent le métal froid.",
            "maman|Une poussière brille au fond.",
            "narrateur|Le couvercle fait un petit toc.",
            "enfant-m|Alors dis-moi où.",
            "narrateur|Papa inspire, les lèvres rondes.",
            "narrateur|Rien ne sort.",
            "maman|Il cherche la suite.",
            "enfant-m|J'écoute.",
            "papa|Le cheval, sous le bras, ensuite.",
            "narrateur|Maman glisse le chiffon dans la poche.",
            "narrateur|Les trois affaires partent ensemble.",
            "papa|Le métal a un peu sonné.",
        ],
        "question": [
            "narrateur|Nino a pris la boîte, près de lui.",
            "maman|Nino a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "boîte",
            "accepted_examples": "boîte | la boîte | boite | la boite | la ronde",
            "retry_prompt": "Nino tient la boîte. Il tient quoi ?",
        },
        "confirm": [
            "enfant-m|La boîte.",
            "maman|Oui, la ronde.",
            "narrateur|Le cheval penche sous le bras.",
            "narrateur|Le chiffon dort dans la poche.",
            "papa|Ça sent le métal, toi.",
            "enfant-m|J'écoute la suite.",
            "maman|On reste ensemble ?",
            "enfant-m|Oui, maman.",
        ],
        "voy": "La boîte ronde tape un peu sa hanche.",
    },
    3: {
        "lab": "le chiffon",
        "sons": "tissu,savon",
        "emphasis": "chiffon",
        "passage": [
            "narrateur|Nino prend le chiffon, d'abord.",
            "enfant-m|Pour sécher le bois.",
            "papa|Il sent le savon.",
            "narrateur|Le tissu frotte l'encolure, léger.",
            "narrateur|Nino frotte trop fort, trop vite.",
            "enfant-m|Maintenant, tu dis où.",
            "narrateur|Papa ouvre la bouche, puis la referme.",
            "papa|Le mot va arriver.",
            "enfant-m|D'accord.",
            "maman|La boîte, ensuite, et le cheval.",
            "narrateur|Papa les pose contre lui.",
            "narrateur|Sous l'auvent, plus rien n'attend.",
            "maman|On avance, sans crier.",
        ],
        "question": [
            "narrateur|Nino a pris le chiffon, près de lui.",
            "maman|Nino a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "chiffon",
            "accepted_examples": "chiffon | le chiffon | le tissu | le linge",
            "retry_prompt": "Nino tient le chiffon. Il tient quoi ?",
        },
        "confirm": [
            "enfant-m|Le chiffon.",
            "papa|Oui, le tissu du savon.",
            "narrateur|Le cheval et la boîte pèsent contre lui.",
            "maman|Le bois va sécher, en marchant.",
            "enfant-m|Je suis prêt.",
            "papa|On avance, alors ?",
            "enfant-m|Oui.",
        ],
        "voy": "Le chiffon pend contre sa poche.",
    },
}

T2 = {
    (1, 1): {
        "sons": "copeaux,tiroir",
        "emphasis": "copeaux",
        "passage": [
            "narrateur|Le cheval bute contre un tas de copeaux.",
            "narrateur|Des copeaux jaunes cachent les tiroirs.",
            "enfant-m|C'est ici ?",
            "papa|C'est le tiroir.",
            "narrateur|Un copeau saute près de sa bouche.",
            "enfant-m|Lequel ?",
            "narrateur|Papa tousse, le mot perdu.",
            "narrateur|Les épaules de Nino tombent.",
            "maman|Les tiroirs se ressemblent tous.",
            "papa|On fait comment, Nino ?",
        ],
    },
    (1, 2): {
        "sons": "couvercle,bois",
        "emphasis": "couvercle",
        "passage": [
            "narrateur|Le cheval penche contre le couvercle lourd.",
            "narrateur|Le bois du coffre ne bouge pas.",
            "enfant-m|Elle est là-dedans ?",
            "maman|Elle est dans le.",
            "narrateur|Maman cherche, un doigt en l'air.",
            "enfant-m|Ouvre !",
            "narrateur|Nino tape du pied, puis recule.",
            "papa|Le bois est trop lourd, seul.",
            "maman|Tu trouves comment ?",
        ],
    },
    (1, 3): {
        "sons": "etagere,pot",
        "emphasis": "étagère",
        "passage": [
            "narrateur|Le cheval lève le nez, trop bas.",
            "narrateur|L'étagère reste loin, au-dessus.",
            "enfant-m|Tout en haut ?",
            "papa|Tout en haut, près du.",
            "narrateur|Papa s'arrête, les lèvres rondes.",
            "enfant-m|Près du pot ?",
            "narrateur|Papa n'a pas fini.",
            "maman|Le haut est trop loin, pour lui.",
            "papa|Un tabouret dort près du mur.",
            "papa|Tu fais quoi, alors ?",
        ],
    },
    (2, 1): {
        "sons": "metal,copeaux",
        "emphasis": "copeaux",
        "passage": [
            "narrateur|La boîte glisse sur une planche, fine.",
            "narrateur|Elle recouvre l'étiquette d'un tiroir.",
            "enfant-m|C'est sous la boîte ?",
            "papa|C'est le tiroir.",
            "narrateur|Le métal claque, trop fort.",
            "enfant-m|Lequel, papa ?",
            "narrateur|Papa perd le mot, dans le bruit.",
            "maman|La boîte a caché le nom.",
            "papa|On fait comment, Nino ?",
        ],
    },
    (2, 2): {
        "sons": "metal,couvercle",
        "emphasis": "couvercle",
        "passage": [
            "narrateur|La boîte tape le bois, un petit toc.",
            "enfant-m|Je la mets dedans, vite.",
            "maman|Elle est dans le.",
            "narrateur|Nino pousse le couvercle, trop tôt.",
            "narrateur|Le bois ne cède pas.",
            "enfant-m|Ouvre, maman !",
            "papa|Tes mains sont trop petites, seules.",
            "maman|Tu trouves comment ?",
        ],
    },
    (2, 3): {
        "sons": "metal,etagere",
        "emphasis": "étagère",
        "passage": [
            "narrateur|La boîte n'atteint pas le bord, trop haute.",
            "enfant-m|Je saute !",
            "narrateur|Nino saute, la boîte sonne.",
            "papa|Tout en haut, près du.",
            "enfant-m|Près du pot ?",
            "narrateur|Le mot retombe avec Nino.",
            "maman|Le haut est trop loin, pour lui.",
            "papa|Tu fais quoi, alors ?",
        ],
    },
    (3, 1): {
        "sons": "tissu,copeaux",
        "emphasis": "écharde",
        "passage": [
            "narrateur|Le chiffon s'accroche à une écharde.",
            "enfant-m|Aïe, ça pique !",
            "papa|C'est le tiroir.",
            "narrateur|Nino tire le tissu, trop fort.",
            "enfant-m|Lequel ?",
            "narrateur|L'écharde garde le mot, et le linge.",
            "maman|Les tiroirs se ressemblent tous.",
            "papa|On fait comment, Nino ?",
        ],
    },
    (3, 2): {
        "sons": "tissu,couvercle",
        "emphasis": "couvercle",
        "passage": [
            "narrateur|Le chiffon glisse sous le bord, mou.",
            "enfant-m|Il est parti dessous !",
            "maman|Elle est dans le.",
            "narrateur|Nino tire le tissu, le couvercle claque.",
            "enfant-m|Ouvre !",
            "narrateur|Le mot de maman se ferme avec.",
            "papa|Le bois est trop lourd, seul.",
            "maman|Tu trouves comment ?",
        ],
    },
    (3, 3): {
        "sons": "tissu,etagere",
        "emphasis": "étagère",
        "passage": [
            "narrateur|Le chiffon pend, trop court, sous le bois.",
            "enfant-m|Je l'accroche en haut !",
            "papa|Tout en haut, près du.",
            "narrateur|Nino lance le tissu, il retombe.",
            "enfant-m|Près du pot ?",
            "narrateur|Papa n'a pas fini.",
            "maman|Le haut est trop loin, pour lui.",
            "papa|Tu fais quoi, alors ?",
        ],
    },
}

T3_LABS = {
    1: ("le petit tiroir", "les copeaux", "le tiroir bas"),
    2: ("le coin gauche", "les deux mains", "la cale"),
    3: ("le pot bleu", "le tabouret", "les bras de papa"),
}

T3_CHOICE = {
    1: [
        "narrateur|Les copeaux cachent trop les tiroirs.",
        "papa|Le petit, les copeaux, ou le bas ?",
    ],
    2: [
        "narrateur|Le couvercle pèse, trop lourd.",
        "maman|Le coin, les mains, ou la cale ?",
    ],
    3: [
        "narrateur|Le haut reste trop loin.",
        "papa|Le pot, le tabouret, ou mes bras ?",
    ],
}

T3_SONS = {
    (1, 1): "tiroir,silence",
    (1, 2): "souffle,copeaux",
    (1, 3): "pas,tiroir",
    (2, 1): "fenetre,coffre",
    (2, 2): "mains,couvercle",
    (2, 3): "cale,bois",
    (3, 1): "pot,bois",
    (3, 2): "tabouret,pas",
    (3, 3): "bras,souffle",
}

T3_EMPH = {
    1: {1: "petit tiroir", 2: "copeaux", 3: "tiroir bas"},
    2: {1: "coin gauche", 2: "deux mains", 3: "cale"},
    3: {1: "pot bleu", 2: "tabouret", 3: "bras"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|On reste.",
        "narrateur|Ils s'assoient près des copeaux.",
        "papa|Le petit.",
        "narrateur|Nino serre le cheval, sans parler.",
        "papa|Le petit tiroir.",
        "narrateur|Nino tire, sans crier.",
        "narrateur|Une roue brille au fond, jaune.",
        "maman|Le cheval est resté contre ta jambe.",
        "papa|Merci, Nino.",
    ],
    (1, 1, 2): [
        "enfant-m|Je souffle.",
        "narrateur|Les copeaux s'envolent, un par un.",
        "papa|Le.",
        "narrateur|Nino souffle, la bouche occupée.",
        "papa|Le petit.",
        "enfant-m|Je vois l'étiquette, maintenant.",
        "narrateur|La roue apparaît sous le nom.",
        "maman|Le vent a aidé tes yeux.",
        "papa|Le cheval n'a pas bougé.",
    ],
    (1, 1, 3): [
        "enfant-m|On se baisse.",
        "narrateur|Ils s'accroupissent près du tiroir bas.",
        "papa|Pas le haut.",
        "narrateur|Nino pose le cheval, et écoute.",
        "papa|Le bas.",
        "enfant-m|Celui-là, tout près du sol.",
        "narrateur|La roue est là, ronde, un peu poussiéreuse.",
        "maman|Tes genoux ont vu juste.",
        "papa|Le cheval a attendu par terre.",
    ],
    (1, 2, 1): [
        "enfant-m|On ne touche pas.",
        "narrateur|Les deux restent debout, près du coffre.",
        "maman|Le coin gauche.",
        "enfant-m|Celui près de la fenêtre.",
        "narrateur|Papa lève un peu, Nino regarde.",
        "narrateur|La roue brille au coin, contre le bois.",
        "papa|Le cheval n'a pas poussé le couvercle.",
        "maman|Tes yeux ont eu la place.",
    ],
    (1, 2, 2): [
        "enfant-m|À deux.",
        "papa|Tes mains ici, les miennes là.",
        "narrateur|Le couvercle s'ouvre, lent.",
        "maman|Dans le.",
        "narrateur|Nino tient, les lèvres fermées.",
        "maman|Dans le coin.",
        "narrateur|La roue roule vers le cheval, un toc.",
        "papa|On a porté ensemble.",
        "maman|Tes mains étaient à la bonne place.",
    ],
    (1, 2, 3): [
        "enfant-m|La cale, dessous.",
        "papa|Je glisse le bois, sans forcer.",
        "narrateur|Le couvercle reste ouvert, un peu.",
        "maman|À gauche.",
        "narrateur|Nino tourne la tête, sans parler.",
        "enfant-m|Je la vois, au fond.",
        "narrateur|La roue attend, près d'un clou.",
        "papa|La cale a tenu l'ouverture.",
        "maman|Le cheval a regardé avec toi.",
    ],
    (1, 3, 1): [
        "enfant-m|Je dis rien.",
        "narrateur|Nino baisse les yeux, le cheval serré.",
        "papa|Près du pot bleu.",
        "enfant-m|Celui qui brille.",
        "narrateur|Papa tend la main, tout haut.",
        "narrateur|La roue brille entre deux pots.",
        "maman|Le mot a fini sa route.",
        "papa|Le cheval n'a pas sauté.",
    ],
    (1, 3, 2): [
        "enfant-m|Le tabouret, dessous.",
        "papa|Je le tiens, à ta hauteur.",
        "narrateur|Nino monte, un pied, puis l'autre.",
        "papa|Près du.",
        "narrateur|Nino attend, un pied en l'air.",
        "papa|Près du pot.",
        "narrateur|La roue est là, bleue de poussière.",
        "maman|Tu as laissé le mot monter.",
        "papa|Le bois a tenu tes pieds.",
    ],
    (1, 3, 3): [
        "enfant-m|Tes bras, papa.",
        "papa|Viens, tout contre moi.",
        "narrateur|Nino s'élève, le nez au bois.",
        "papa|Près du pot bleu.",
        "enfant-m|Je la vois !",
        "narrateur|La roue brille entre deux pots.",
        "maman|Tes bras ont porté les yeux.",
        "papa|Chacun a fait sa part.",
    ],
    (2, 1, 1): [
        "enfant-m|La boîte, sur la planche.",
        "narrateur|Nino pose le métal, puis s'assoit.",
        "papa|Le petit.",
        "narrateur|La boîte ne claque plus.",
        "papa|Le petit tiroir.",
        "narrateur|Nino tire, la boîte à côté.",
        "narrateur|La roue roule dans la ronde, toc.",
        "maman|Le métal a eu sa place.",
        "papa|Merci, Nino.",
    ],
    (2, 1, 2): [
        "enfant-m|Je souffle, boîte à plat.",
        "narrateur|Les copeaux s'envolent autour du métal.",
        "papa|Le.",
        "narrateur|Nino souffle, sans demander lequel.",
        "papa|Le petit.",
        "enfant-m|L'étiquette, je la vois.",
        "narrateur|La roue glisse vers la boîte, ronde.",
        "maman|Le vent a aidé le métal.",
        "papa|La boîte n'a plus caché le nom.",
    ],
    (2, 1, 3): [
        "enfant-m|On se baisse, boîte avec nous.",
        "narrateur|Ils s'accroupissent, le métal froid.",
        "papa|Pas le haut.",
        "narrateur|Nino tient la boîte, bouche fermée.",
        "papa|Le bas.",
        "enfant-m|Celui-là, tout près du sol.",
        "narrateur|La roue tombe dans la boîte, nette.",
        "maman|Tes genoux et le métal, ensemble.",
        "papa|Le bas a parlé.",
    ],
    (2, 2, 1): [
        "enfant-m|La boîte, on la pose.",
        "narrateur|Nino pose le métal, et attend.",
        "maman|Le coin gauche.",
        "enfant-m|Celui près de la fenêtre.",
        "narrateur|Papa lève un peu, Nino tend la ronde.",
        "narrateur|La roue rentre dans la boîte, froide.",
        "papa|Le métal n'a pas poussé trop tôt.",
        "maman|Tes yeux ont eu la place.",
    ],
    (2, 2, 2): [
        "enfant-m|À deux, boîte contre moi.",
        "papa|Tes mains ici, les miennes là.",
        "narrateur|Le couvercle s'ouvre, lent.",
        "maman|Dans le.",
        "narrateur|Nino tient, la boîte coincée au ventre.",
        "maman|Dans le coin.",
        "narrateur|La roue fait un toc dans le métal.",
        "papa|On a porté ensemble.",
        "maman|La ronde a reçu la suite.",
    ],
    (2, 2, 3): [
        "enfant-m|La cale, et la boîte.",
        "papa|Je glisse le bois, sans forcer.",
        "narrateur|Le couvercle reste ouvert, un peu.",
        "maman|À gauche.",
        "narrateur|Nino tend la boîte, sans parler.",
        "enfant-m|Je la vois, au fond.",
        "narrateur|La roue glisse dans le métal, ronde.",
        "papa|La cale a tenu l'ouverture.",
        "maman|La boîte a fait son nid.",
    ],
    (2, 3, 1): [
        "enfant-m|Je dis rien, boîte serrée.",
        "narrateur|Nino baisse les yeux, le métal froid.",
        "papa|Près du pot bleu.",
        "enfant-m|Celui qui brille.",
        "narrateur|Papa tend la boîte, tout haut.",
        "narrateur|La roue tombe dans la ronde, un toc.",
        "maman|Le mot a fini sa route.",
        "papa|Le métal n'a pas sauté.",
    ],
    (2, 3, 2): [
        "enfant-m|Le tabouret, boîte contre moi.",
        "papa|Je le tiens, à ta hauteur.",
        "narrateur|Nino monte, la boîte sous le bras.",
        "papa|Près du.",
        "narrateur|Nino attend, un pied en l'air.",
        "papa|Près du pot.",
        "narrateur|La roue rentre dans le métal, bleue.",
        "maman|Tu as laissé le mot monter.",
        "papa|Le bois a tenu tes pieds.",
    ],
    (2, 3, 3): [
        "enfant-m|Tes bras, papa, et la boîte.",
        "papa|Viens, tout contre moi.",
        "narrateur|Nino s'élève, la ronde au ventre.",
        "papa|Près du pot bleu.",
        "enfant-m|Je la vois !",
        "narrateur|La roue brille, puis tombe dans le métal.",
        "maman|Tes bras ont porté la ronde.",
        "papa|Chacun a fait sa part.",
    ],
    (3, 1, 1): [
        "enfant-m|On reste, chiffon à la main.",
        "narrateur|Ils s'assoient près des copeaux.",
        "papa|Le petit.",
        "narrateur|Nino essuie le bois du tiroir, lent.",
        "papa|Le petit tiroir.",
        "narrateur|Nino tire, le tissu sur la poignée.",
        "narrateur|Une roue brille, le chiffon la sèche.",
        "maman|Le savon a vu le fond.",
        "papa|Merci, Nino.",
    ],
    (3, 1, 2): [
        "enfant-m|Je souffle, chiffon prêt.",
        "narrateur|Les copeaux s'envolent, le tissu les aide.",
        "papa|Le.",
        "narrateur|Nino souffle, puis frotte, sans parler.",
        "papa|Le petit.",
        "enfant-m|Je vois l'étiquette, maintenant.",
        "narrateur|La roue apparaît, le chiffon la prend.",
        "maman|Le vent et le savon, ensemble.",
        "papa|Le tissu n'a plus tiré l'écharde.",
    ],
    (3, 1, 3): [
        "enfant-m|On se baisse, chiffon avec nous.",
        "narrateur|Ils s'accroupissent près du tiroir bas.",
        "papa|Pas le haut.",
        "narrateur|Nino pose le tissu, et écoute.",
        "papa|Le bas.",
        "enfant-m|Celui-là, tout près du sol.",
        "narrateur|La roue est là, le chiffon l'essuie.",
        "maman|Tes genoux ont vu juste.",
        "papa|Le linge a pris la poussière.",
    ],
    (3, 2, 1): [
        "enfant-m|On ne touche pas, chiffon plat.",
        "narrateur|Les deux restent debout, le tissu sage.",
        "maman|Le coin gauche.",
        "enfant-m|Celui près de la fenêtre.",
        "narrateur|Papa lève un peu, Nino tend le linge.",
        "narrateur|La roue brille, le chiffon la sort.",
        "papa|Le tissu n'est plus sous le bord.",
        "maman|Tes yeux ont eu la place.",
    ],
    (3, 2, 2): [
        "enfant-m|À deux, chiffon entre nous.",
        "papa|Tes mains ici, les miennes là.",
        "narrateur|Le couvercle s'ouvre, lent.",
        "maman|Dans le.",
        "narrateur|Nino tient, le tissu contre le bois.",
        "maman|Dans le coin.",
        "narrateur|La roue roule sur le chiffon, douce.",
        "papa|On a porté ensemble.",
        "maman|Le linge a reçu la suite.",
    ],
    (3, 2, 3): [
        "enfant-m|La cale, chiffon prêt.",
        "papa|Je glisse le bois, sans forcer.",
        "narrateur|Le couvercle reste ouvert, un peu.",
        "maman|À gauche.",
        "narrateur|Nino glisse le tissu, sans parler.",
        "enfant-m|Je la vois, au fond.",
        "narrateur|La roue vient sur le chiffon, ronde.",
        "papa|La cale a tenu l'ouverture.",
        "maman|Le savon a fait un nid.",
    ],
    (3, 3, 1): [
        "enfant-m|Je dis rien, chiffon serré.",
        "narrateur|Nino baisse les yeux, le tissu chaud.",
        "papa|Près du pot bleu.",
        "enfant-m|Celui qui brille.",
        "narrateur|Papa tend le chiffon, tout haut.",
        "narrateur|La roue glisse dans le tissu, bleue.",
        "maman|Le mot a fini sa route.",
        "papa|Le linge n'a pas volé.",
    ],
    (3, 3, 2): [
        "enfant-m|Le tabouret, chiffon au poing.",
        "papa|Je le tiens, à ta hauteur.",
        "narrateur|Nino monte, le tissu contre lui.",
        "papa|Près du.",
        "narrateur|Nino attend, un pied en l'air.",
        "papa|Près du pot.",
        "narrateur|La roue est là, le chiffon la prend.",
        "maman|Tu as laissé le mot monter.",
        "papa|Le bois a tenu tes pieds.",
    ],
    (3, 3, 3): [
        "enfant-m|Tes bras, papa, et le chiffon.",
        "papa|Viens, tout contre moi.",
        "narrateur|Nino s'élève, le tissu au nez.",
        "papa|Près du pot bleu.",
        "enfant-m|Je la vois !",
        "narrateur|La roue brille, le chiffon la cueille.",
        "maman|Tes bras ont porté le savon.",
        "papa|Chacun a fait sa part.",
    ],
}

END_SONS = {1: "carreaux,copeaux", 2: "carreaux,coffre", 3: "carreaux,goutte"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|La roue rentre, un petit clic.",
        "enfant-m|Il galope !",
        "papa|Sur les carreaux secs, tout droit.",
        "maman|Le petit tiroir se tait.",
        "narrateur|Le bois du cheval reste un peu tiède.",
        "narrateur|Un copeau jaune reste collé au seuil.",
    ],
    (1, 1, 2): [
        "narrateur|La roue tourne, enfin, tout ronde.",
        "enfant-m|Les copeaux ont volé, d'abord.",
        "papa|Puis le mot est venu.",
        "maman|Venez, le pain est chaud.",
        "narrateur|Nino pose le cheval près du seuil.",
        "narrateur|Un copeau reste collé à sa chaussure.",
    ],
    (1, 1, 3): [
        "narrateur|La roue du bas tient, nette.",
        "enfant-m|On s'est baissés, papa.",
        "papa|Le haut gardera son ombre.",
        "maman|Lave-toi les mains, Nino.",
        "narrateur|Nino tapote le dos, léger.",
        "narrateur|Une abeille passe, puis l'auvent se tait.",
    ],
    (1, 2, 1): [
        "narrateur|Au coin gauche, la roue était là.",
        "enfant-m|Tu as fini, maman.",
        "maman|Oui, le mot était long.",
        "papa|Le cheval n'a pas crié.",
        "narrateur|Nino fait galoper le cheval, tout près.",
        "narrateur|Le coffre ferme, un petit toc.",
    ],
    (1, 2, 2): [
        "narrateur|À deux, le coffre a parlé, enfin.",
        "enfant-m|On a porté, tous les deux.",
        "papa|Tes mains étaient à la bonne place.",
        "maman|Le pain t'attend.",
        "narrateur|Nino essuie une main sur son pantalon.",
        "narrateur|Le cheval avance, roue après roue.",
    ],
    (1, 2, 3): [
        "narrateur|La cale tient le bord, ouverte.",
        "enfant-m|Je l'ai vue, au fond.",
        "papa|Le bois a gardé l'ouverture.",
        "maman|Rentrez la cale, après le galop.",
        "narrateur|Nino souffle un peu sur la roue.",
        "narrateur|Une poussière s'envole, puis retombe.",
    ],
    (1, 3, 1): [
        "narrateur|Près du pot bleu, la roue brille.",
        "enfant-m|Tu as dit bleu, à la fin.",
        "papa|Tes oreilles ont eu le mot.",
        "maman|Un peu de soupe, après le galop.",
        "narrateur|Nino pose le cheval contre le mur.",
        "narrateur|Le pot bleu reprend sa place, sage.",
    ],
    (1, 3, 2): [
        "narrateur|Sur le tabouret, Nino a vu le bleu.",
        "enfant-m|Le mot est monté avec moi.",
        "papa|Je remporte le tabouret, tout à l'heure.",
        "maman|Essuie tes chaussures, Nino.",
        "narrateur|Le cheval galope jusqu'au seuil, net.",
        "narrateur|L'auvent laisse un rai sur les carreaux.",
    ],
    (1, 3, 3): [
        "narrateur|Dans les bras de papa, la roue était là.",
        "enfant-m|On l'a prise, tout haut.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        "narrateur|Nino pose le cheval près des carreaux.",
        "narrateur|Quatre roues touchent le sol, net.",
    ],
    (2, 1, 1): [
        "narrateur|La roue rentre, toc dans la boîte.",
        "enfant-m|Elle a son nid, maintenant.",
        "papa|Sur les carreaux, le cheval peut partir.",
        "maman|La ronde a fini son voyage.",
        "narrateur|Nino ferme la boîte, un petit clic.",
        "narrateur|La boîte ronde garde une poussière fine.",
    ],
    (2, 1, 2): [
        "narrateur|Après le souffle, la roue tourne.",
        "enfant-m|Les copeaux ont laissé le métal.",
        "papa|Le nom était sous la poussière.",
        "maman|Venez, le pain est chaud.",
        "narrateur|Nino pose la boîte près du seuil.",
        "narrateur|Le métal a sonné, puis s'est tu.",
    ],
    (2, 1, 3): [
        "narrateur|Du tiroir bas, la roue tombe, ronde.",
        "enfant-m|On s'est baissés, la boîte avec.",
        "papa|Le haut gardera son ombre.",
        "maman|Lave-toi les mains, Nino.",
        "narrateur|Nino tapote le métal, léger.",
        "narrateur|Un rond de poussière reste au fond.",
    ],
    (2, 2, 1): [
        "narrateur|Au coin gauche, la roue rentre, froide.",
        "enfant-m|Tu as fini, maman, dans la ronde.",
        "maman|Oui, le mot était long.",
        "papa|Le métal n'a pas crié.",
        "narrateur|Nino fait galoper le cheval, boîte à côté.",
        "narrateur|Le couvercle de la boîte brille, froid.",
    ],
    (2, 2, 2): [
        "narrateur|À deux, la roue fait un toc de métal.",
        "enfant-m|On a porté, la boîte au ventre.",
        "papa|Tes mains étaient à la bonne place.",
        "maman|Le pain t'attend.",
        "narrateur|Nino essuie le métal sur son pantalon.",
        "narrateur|Un toc de métal dort dans la poche.",
    ],
    (2, 2, 3): [
        "narrateur|La cale tient, la roue glisse, ronde.",
        "enfant-m|Je l'ai vue, au fond, dans la boîte.",
        "papa|Le bois a gardé l'ouverture.",
        "maman|Rentrez la cale, après le galop.",
        "narrateur|Nino souffle un peu sur le métal.",
        "narrateur|La boîte ronde se tait contre sa hanche.",
    ],
    (2, 3, 1): [
        "narrateur|Près du pot bleu, la roue tombe, toc.",
        "enfant-m|Tu as dit bleu, dans la ronde.",
        "papa|Tes oreilles ont eu le mot.",
        "maman|Un peu de soupe, après le galop.",
        "narrateur|Nino pose la boîte contre le mur.",
        "narrateur|Le pot bleu se reflète dans le métal.",
    ],
    (2, 3, 2): [
        "narrateur|Sur le tabouret, la roue rentre, bleue.",
        "enfant-m|Le mot est monté avec la boîte.",
        "papa|Je remporte le tabouret, tout à l'heure.",
        "maman|Essuie tes chaussures, Nino.",
        "narrateur|Le cheval galope, la ronde sous le bras.",
        "narrateur|La boîte tape le tabouret, puis se tait.",
    ],
    (2, 3, 3): [
        "narrateur|Dans les bras, la roue tombe dans le métal.",
        "enfant-m|On l'a prise, tout haut, la ronde aussi.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        "narrateur|Nino pose la boîte près des carreaux.",
        "narrateur|Dans les bras, la boîte pèse, ronde.",
    ],
    (3, 1, 1): [
        "narrateur|La roue rentre, le chiffon la sèche.",
        "enfant-m|Il galope, propre !",
        "papa|Sur les carreaux secs, tout droit.",
        "maman|Le petit tiroir sent le savon.",
        "narrateur|Nino range le chiffon sur l'encolure.",
        "narrateur|Le chiffon sent le savon du bois.",
    ],
    (3, 1, 2): [
        "narrateur|Après le souffle, le chiffon prend la roue.",
        "enfant-m|Les copeaux ont volé, le tissu aussi.",
        "papa|Puis le mot est venu.",
        "maman|Venez, le pain est chaud.",
        "narrateur|Nino pose le cheval, chiffon sur le dos.",
        "narrateur|Un fil du chiffon reste dans les copeaux.",
    ],
    (3, 1, 3): [
        "narrateur|La roue du bas, le chiffon l'essuie.",
        "enfant-m|On s'est baissés, le linge avec.",
        "papa|Le haut gardera son ombre.",
        "maman|Lave-toi les mains, Nino.",
        "narrateur|Nino tapote le dos, le tissu dessus.",
        "narrateur|Le chiffon pend, mou, contre sa poche.",
    ],
    (3, 2, 1): [
        "narrateur|Au coin gauche, le chiffon sort la roue.",
        "enfant-m|Tu as fini, maman, le linge aussi.",
        "maman|Oui, le mot était long.",
        "papa|Le tissu n'a pas crié.",
        "narrateur|Nino fait galoper le cheval, chiffon en poche.",
        "narrateur|Le tissu a gardé une poussière de coffre.",
    ],
    (3, 2, 2): [
        "narrateur|À deux, la roue roule sur le chiffon.",
        "enfant-m|On a porté, le linge entre nous.",
        "papa|Tes mains étaient à la bonne place.",
        "maman|Le pain t'attend.",
        "narrateur|Nino essuie une main sur le tissu.",
        "narrateur|Un grain de savon reste sur le linge.",
    ],
    (3, 2, 3): [
        "narrateur|La cale tient, le chiffon cueille la roue.",
        "enfant-m|Je l'ai vue, au fond, sur le tissu.",
        "papa|Le bois a gardé l'ouverture.",
        "maman|Rentrez la cale, après le galop.",
        "narrateur|Nino souffle un peu sur le linge.",
        "narrateur|Le chiffon sèche sur le bord du coffre.",
    ],
    (3, 3, 1): [
        "narrateur|Près du pot bleu, le chiffon cueille.",
        "enfant-m|Tu as dit bleu, le tissu l'a pris.",
        "papa|Tes oreilles ont eu le mot.",
        "maman|Un peu de soupe, après le galop.",
        "narrateur|Nino pose le cheval, chiffon sur le mur.",
        "narrateur|Le chiffon salue le pot bleu, léger.",
    ],
    (3, 3, 2): [
        "narrateur|Sur le tabouret, le chiffon prend la roue.",
        "enfant-m|Le mot est monté avec le tissu.",
        "papa|Je remporte le tabouret, tout à l'heure.",
        "maman|Essuie tes chaussures, Nino.",
        "narrateur|Le cheval galope, le chiffon au vent.",
        "narrateur|Le tissu glisse du tabouret, puis s'arrête.",
    ],
    (3, 3, 3): [
        "narrateur|Dans les bras, le chiffon cueille la roue.",
        "enfant-m|On l'a prise, tout haut, le linge aussi.",
        "papa|Tes yeux allaient assez loin.",
        "maman|Le haut gardera son ombre.",
        "narrateur|Nino pose le cheval près des carreaux.",
        "narrateur|Le chiffon dort, chaud, contre l'encolure.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "gouttiere,bois"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("le cheval", "la boîte ronde", "le chiffon")},
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
                "narrateur|Sous l'auvent, trois coins restent secs.",
                "papa|L'établi, le coffre, ou l'étagère ?",
            ],
            "choice",
            "",
            {"fields": t3lab("l'établi", "le coffre", "l'étagère")},
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
        "noé",
        "noe ",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "dans le salon",
        "joue au salon",
        "tout doux",
        "tout calme",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")

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

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-038 — Le cheval de bois de Nino, sous l'auvent\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.002 — laisser l'autre finir sa phrase (vécue)\n"
        "- **Personnages :** Nino, papa, maman\n"
        "- **Lieu :** sous l'auvent, après la pluie : établi, coffre, étagère\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sous l'auvent, les carreaux sèchent. Nino veut que son cheval de bois "
        "**galope maintenant**. Une roue manque. Papa commence : « La roue est dans le. » "
        "Nino coupe : « Dans le quoi ? » Le mot rentre. Première idée ratée. "
        "Il prend le cheval, la boîte ronde ou le chiffon ; l'établi cache, le coffre pèse "
        "ou l'étagère est trop haute ; une action change l'écoute (petit tiroir, copeaux, "
        "tiroir bas ; coin gauche, deux mains, cale ; pot bleu, tabouret, bras). "
        "La phrase arrive. La roue rentre. Le cheval galope.\n\n"
        "## Vécu\n\n"
        "Nino veut le galop **maintenant**. Il parle à la place de papa. Silence, mot perdu, "
        "cheval sur trois roues. Chaque choix change l'obstacle et le climax. La leçon se voit : "
        "couper donne une bouche fermée ; laisser finir donne le petit tiroir, l'étiquette, "
        "le bas, le coin, les deux mains, la cale, le pot bleu, le tabouret, les bras. "
        "Fin : quatre roues + carreaux secs, image unique du chemin (copeau, toc, rai, savon).\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan salon / Noé / bac-toboggan-balançoires / Tom-Léa-Sami jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (cheval tenu). Question d'adulte. Un « en ce moment ».\n"
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
