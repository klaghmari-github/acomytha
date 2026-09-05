#!/usr/bin/env python3
"""TREE-DIF-018 — F-NAR-019. Biscuits de Mila, fond du jardin. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-018"
N3 = 16
TITLE = "Les biscuits de Mila au fond du jardin"
FIL = (
    "Au jardin aromatique, Mila veut porter sa boîte à pois jusqu'au goûter de la cabane "
    "avant que le vent n'enlève la nappe. Raphaël coupe : « Caisse ! » Le mot manque. "
    "T1 = sac / carnet / clochette, les trois partent. "
    "T2 = cabanon (caisses), verger des rubans (pierres), table du thym (vent). "
    "T3 = neuf façons de laisser la phrase arriver. La boîte s'ouvre. On croque."
)
CHARS = "Mila, Raphaël, papa, maman"
SETTING = "jardin aromatique, fin d'après-midi : cabane, verger des rubans, table du thym"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "boîte à pois",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le goûter attend et Raphaël coupe; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change le geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        "emphasis": "boîte à pois",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté; tempo=naturel; sourire=léger; respiration=fluide",
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
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=la_phrase_de_Raphaël_se_casse; tempo=resserré; sourire=aucun; respiration=retenue",
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
        "emphasis": "biscuits",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_boîte_paie_le_toc_et_le_ruban_du_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Au fond du jardin, le romarin sent le soleil.",
    "narrateur|Les carreaux de la terrasse sont tièdes sous les pieds.",
    "narrateur|Une nappe à carreaux bleus se soulève, puis retombe.",
    "narrateur|Le thym pique un peu, près des tomates chaudes.",
    "narrateur|Ça sent le beurre, mêlé au romarin.",
    "narrateur|Un ruban jaune pend au cerisier du fond.",
    "narrateur|C'est le verger des rubans, au fond.",
    "papa|J'ai coupé la menthe, pour la carafe.",
    "maman|Les tasses attendent le goûter de la cabane.",
    "narrateur|Une miette de beurre brille au pouce de Mila.",
    "narrateur|La cabane du fond a un degré de bois.",
    "narrateur|En ce moment, le portail grince, léger.",
    "narrateur|Mila entre, un doigt contre ses lèvres.",
    "enfant-f|J'ai caché la boîte à pois.",
    "copain|Des biscuits ?",
    "enfant-f|Oui, pour la cabane, avant le vent.",
    "copain|Où ?",
    "enfant-f|Au fond, dans la.",
    "copain|Caisse !",
    "narrateur|Mila referme la bouche.",
    "narrateur|Le mot n'est pas fini.",
    "narrateur|Raphaël baisse les yeux.",
    "maman|Il a parlé trop vite, Mila ?",
    "papa|Prenez le sac, le carnet, et la clochette.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près de la nappe.",
    "narrateur|Le sac, le carnet, et la clochette.",
    "papa|Tu prends quoi, d'abord ?",
]

T1 = {
    1: {
        "lab": "le sac",
        "sons": "toile,pas",
        "emphasis": "sac",
        "passage": [
            "narrateur|Mila saisit d'abord le sac en toile.",
            "enfant-f|Pour porter la boîte, après.",
            "papa|Il sent le pain, un peu rêche.",
            "narrateur|La toile est chaude, du soleil de la terrasse.",
            "maman|Le carnet, contre le sac.",
            "narrateur|Raphaël le glisse, sans un mot.",
            "copain|La clochette aussi.",
            "narrateur|Elle tinte une fois, trop courte.",
            "narrateur|Mila a trop de hâte dans les épaules.",
            "enfant-f|Maintenant, tu dis où.",
            "copain|Au fond, près du.",
            "enfant-f|Cabanon !",
            "narrateur|Raphaël referme la bouche.",
            "papa|On marche, le mot suivra.",
            "narrateur|Les trois affaires partent ensemble.",
            "maman|Le sac d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Le sac en toile pèse dans sa main.",
            "maman|Mila a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "le sac",
            "accepted_examples": "sac | le sac | un sac | sac en toile | la toile",
            "retry_prompt": "Mila a pris le sac en premier. Elle a pris quoi ?",
        },
        "confirm": [
            "enfant-f|Le sac.",
            "papa|Oui.",
            "narrateur|Le carnet et la clochette voyagent avec.",
            "copain|Je vais dire l'endroit.",
            "narrateur|Papa pose un doigt sur sa bouche.",
            "enfant-f|J'écoute, cette fois.",
            "maman|Vous partez ensemble.",
            "narrateur|La toile frotte la hanche de Mila.",
            "papa|La boîte à pois attend, quelque part.",
        ],
    },
    2: {
        "lab": "le carnet",
        "sons": "papier,crayon",
        "emphasis": "carnet",
        "passage": [
            "narrateur|Mila ouvre d'abord le carnet à spirale.",
            "enfant-f|Il y a un mot, à moitié.",
            "maman|Le crayon a laissé un trait pâle.",
            "narrateur|Le papier est un peu gondolé, tiède.",
            "papa|Le sac, ensuite, pour porter.",
            "narrateur|Raphaël passe la lanière à Mila.",
            "copain|La clochette, dans ta poche.",
            "narrateur|Le métal reste froid contre le tissu.",
            "enfant-f|Lis-moi l'endroit.",
            "narrateur|Raphaël pose un doigt sous le trait.",
            "copain|Ceri.",
            "enfant-f|Cerisier !",
            "narrateur|Le doigt s'arrête, trop tôt.",
            "papa|Le mot n'était pas fini.",
            "narrateur|Mila mord sa lèvre, déçue.",
            "maman|Le carnet d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Le carnet est ouvert, sur un trait.",
            "papa|Mila a ouvert quoi ?",
        ],
        "qfields": {
            "expected_answer": "le carnet",
            "accepted_examples": "carnet | le carnet | un carnet | carnet à spirale | le papier",
            "retry_prompt": "Mila a ouvert le carnet. Elle a ouvert quoi ?",
        },
        "confirm": [
            "enfant-f|Le carnet.",
            "maman|Oui.",
            "narrateur|Le sac pend à son épaule.",
            "narrateur|La clochette dort dans la poche.",
            "copain|Le trait n'est pas fini.",
            "narrateur|Maman tient le crayon, sans lire.",
            "enfant-f|Je te laisse, Raphaël.",
            "papa|Vous restez ensemble.",
            "narrateur|Un trait pâle attend la suite.",
        ],
    },
    3: {
        "lab": "la clochette",
        "sons": "clochette,tissu",
        "emphasis": "clochette",
        "passage": [
            "narrateur|Mila prend d'abord la clochette, au bord.",
            "enfant-f|Pour crier quand on trouve.",
            "papa|Elle tinte trop tôt, parfois.",
            "narrateur|Le métal est froid, à l'ombre de la nappe.",
            "maman|Le sac, ensuite, et le carnet.",
            "narrateur|Raphaël les pose contre elle, l'un après l'autre.",
            "copain|Pas de tintement, pas tout de suite.",
            "enfant-f|Alors dis-moi où.",
            "narrateur|Raphaël inspire, les lèvres rondes.",
            "narrateur|La clochette tinte, trop vite.",
            "copain|Au.",
            "narrateur|Le mot se perd dans le tintement.",
            "maman|Elle a couvert ta voix.",
            "enfant-f|Je la serre, alors.",
            "narrateur|Mila a trop de hâte dans les doigts.",
            "papa|La clochette d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Un petit tintement vient de sa main.",
            "maman|Mila a pris quoi, au bord ?",
        ],
        "qfields": {
            "expected_answer": "la clochette",
            "accepted_examples": "clochette | la clochette | une clochette | la cloche | le métal",
            "retry_prompt": "Mila a pris la clochette. Elle a pris quoi ?",
        },
        "confirm": [
            "enfant-f|La clochette.",
            "papa|Oui.",
            "narrateur|Le sac et le carnet pèsent contre elle.",
            "copain|Pas de tintement, avant le goûter.",
            "narrateur|Papa ferme la main de Mila, autour du métal.",
            "enfant-f|Je la garde muette.",
            "maman|Elle va dire la suite.",
            "papa|On avance, alors ?",
            "narrateur|Le métal se réchauffe, sans son.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le sac tape un peu sa hanche, à chaque pas.",
        "narrateur|Trois coins du jardin aromatique attendent.",
        "narrateur|Le cabanon, le cerisier, et la table.",
        "papa|On cherche où, d'abord ?",
    ],
    2: [
        "narrateur|Le carnet claque une fois, contre le sac.",
        "narrateur|Trois coins du jardin aromatique attendent.",
        "narrateur|Le cabanon, le cerisier, et la table.",
        "papa|On cherche où, d'abord ?",
    ],
    3: [
        "narrateur|La clochette reste muette, dans la poche.",
        "narrateur|Trois coins du jardin aromatique attendent.",
        "narrateur|Le cabanon, le cerisier, et la table.",
        "papa|On cherche où, d'abord ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "bois,poussiere",
        "emphasis": "cabanon",
        "passage": [
            "narrateur|Le sac en toile pose un carré d'ombre.",
            "narrateur|Ils s'arrêtent devant le cabanon du fond.",
            "narrateur|L'ombre sent le bois chaud, et la poussière.",
            "enfant-f|C'est ici, le goûter de la cabane ?",
            "copain|C'est dans la caisse.",
            "narrateur|Mila lève un doigt, trop tard.",
            "copain|La.",
            "enfant-f|La haute !",
            "narrateur|Raphaël secoue la tête, minuscule.",
            "maman|Les caisses sont trop nombreuses.",
            "narrateur|Le sac glisse vers le seuil, lourd.",
            "narrateur|Une araignée de poussière descend, lente.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "bois,papier",
        "emphasis": "cabanon",
        "passage": [
            "narrateur|Le carnet s'ouvre sur un mot inachevé.",
            "narrateur|Ils s'arrêtent devant le cabanon du fond.",
            "narrateur|Un trait du carnet s'arrête au milieu.",
            "enfant-f|C'est écrit, alors ?",
            "copain|C'est dans la.",
            "enfant-f|Fenêtre !",
            "narrateur|Raphaël cache le papier contre lui.",
            "papa|Le mot n'est pas sur la page.",
            "maman|Les caisses sont trop nombreuses.",
            "narrateur|La poussière colle au crayon, pâle.",
            "copain|Pas la fenêtre.",
            "narrateur|Un copeau de bois colle au crayon.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "bois,clochette",
        "emphasis": "cabanon",
        "passage": [
            "narrateur|La clochette reste silencieuse, dans sa main.",
            "narrateur|Ils s'arrêtent devant le cabanon du fond.",
            "narrateur|Mila serre le métal, sans le bouger.",
            "enfant-f|C'est ici ?",
            "copain|C'est dans la caisse.",
            "narrateur|Un grain de poussière fait presque tinter.",
            "enfant-f|La haute !",
            "narrateur|Raphaël met sa main sur la clochette.",
            "maman|Les caisses sont trop nombreuses.",
            "papa|Le tintement a mangé le mot.",
            "copain|Pas la haute.",
            "narrateur|La poussière pique le nez de Mila.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "feuilles,herbe",
        "emphasis": "cerisier",
        "passage": [
            "narrateur|Le sac s'accroche à une racine, puis lâche.",
            "narrateur|Sous le cerisier, l'herbe est tachetée de soleil.",
            "narrateur|Le ruban jaune tremble, au-dessus des pierres.",
            "enfant-f|Les pierres se ressemblent toutes.",
            "copain|Sous la pierre.",
            "enfant-f|Celle-là !",
            "narrateur|Raphaël recule d'un pas.",
            "papa|Il y en a trop, des pierres.",
            "maman|La suite n'est pas dite.",
            "narrateur|Le sac penche, plein d'ombre.",
            "copain|Pas celle-là.",
            "narrateur|Une fourmi contourne la pierre plate.",
            "papa|Vous trouvez comment ?",
        ],
    },
    (2, 2): {
        "sons": "papier,pierre",
        "emphasis": "cerisier",
        "passage": [
            "narrateur|Mila pose le carnet sur une pierre plate.",
            "narrateur|Sous le cerisier, l'herbe est tachetée de soleil.",
            "narrateur|Le ruban jaune tremble, au-dessus des pierres.",
            "enfant-f|Dessine, alors !",
            "copain|Un rond, comme.",
            "enfant-f|Comme la lune !",
            "narrateur|Le crayon s'arrête, trop court.",
            "papa|Le dessin n'est pas fini.",
            "maman|La suite n'est pas dite.",
            "narrateur|Une fourmi traverse le papier, lente.",
            "copain|Pas la lune.",
            "narrateur|Le ruban jaune fait un petit claquement.",
            "papa|Vous trouvez comment ?",
        ],
    },
    (3, 2): {
        "sons": "feuilles,metal",
        "emphasis": "cerisier",
        "passage": [
            "narrateur|Un pinson fait tinter presque la clochette.",
            "narrateur|Sous le cerisier, l'herbe est tachetée de soleil.",
            "narrateur|Le ruban jaune tremble, au-dessus des pierres.",
            "enfant-f|Les pierres se ressemblent toutes.",
            "copain|Sous la pierre.",
            "enfant-f|La grise !",
            "narrateur|Raphaël ouvre la bouche, puis la referme.",
            "papa|Il y en a trop, des pierres.",
            "maman|La suite n'est pas dite.",
            "narrateur|Mila serre le métal contre sa poche.",
            "copain|Pas la grise.",
            "narrateur|Mila sent le métal, froid, contre sa cuisse.",
            "papa|Vous trouvez comment ?",
        ],
    },
    (1, 3): {
        "sons": "vent,nappe",
        "emphasis": "nappe",
        "passage": [
            "narrateur|Le sac penche contre un pied de table.",
            "narrateur|Près de la table du thym, le vent prend la nappe.",
            "narrateur|Les carreaux bleus claquent, puis se taisent.",
            "enfant-f|Derrière quoi ?",
            "copain|Derrière le.",
            "enfant-f|Le seau !",
            "narrateur|Raphaël secoue la tête.",
            "papa|Le vent mélange les choses.",
            "maman|Sa phrase n'a pas de fin.",
            "narrateur|Un seau et un vase attendent, tous les deux.",
            "copain|Pas le seau.",
            "narrateur|Le thym penche, sous le vent de la nappe.",
            "papa|Vous faites quoi, alors ?",
        ],
    },
    (2, 3): {
        "sons": "vent,papier",
        "emphasis": "nappe",
        "passage": [
            "narrateur|Sous le vent, le carnet frôle la nappe.",
            "narrateur|Près de la table du thym, le vent prend le tissu.",
            "narrateur|Les carreaux bleus claquent, puis se taisent.",
            "enfant-f|Derrière quoi ?",
            "copain|Derrière le.",
            "enfant-f|Le seau !",
            "narrateur|Une page se plie, trop tôt.",
            "papa|Le vent mélange les choses.",
            "maman|Sa phrase n'a pas de fin.",
            "narrateur|Un seau et un vase attendent, tous les deux.",
            "copain|Pas le seau.",
            "narrateur|Une page s'envole, puis retombe.",
            "papa|Vous faites quoi, alors ?",
        ],
    },
    (3, 3): {
        "sons": "vent,toc",
        "emphasis": "nappe",
        "passage": [
            "narrateur|La clochette cogne le bois, un petit toc.",
            "narrateur|Près de la table du thym, le vent prend la nappe.",
            "narrateur|Les carreaux bleus claquent, puis se taisent.",
            "enfant-f|Derrière quoi ?",
            "copain|Derrière le.",
            "enfant-f|Le seau !",
            "narrateur|Le toc a couvert le mot, comme la boîte.",
            "papa|Le vent mélange les choses.",
            "maman|Sa phrase n'a pas de fin.",
            "narrateur|Un seau et un vase attendent, tous les deux.",
            "copain|Pas le seau.",
            "narrateur|Mila serre le métal, pour ne plus toquer.",
            "papa|Vous faites quoi, alors ?",
        ],
    },
}

T3_LABS = {
    1: ("attendre", "la lampe", "la caisse basse"),
    2: ("la pierre", "le dessin", "les racines"),
    3: ("la nappe", "s'asseoir", "le vase"),
}

T3_CHOICE = {
    1: [
        "narrateur|Dans le cabanon, Raphaël n'a pas fini.",
        "narrateur|Un mot manque, au milieu.",
        "papa|Attendre, la lampe, ou la caisse basse ?",
    ],
    2: [
        "narrateur|Sous le cerisier, la suite manque.",
        "narrateur|Le ruban jaune penche, au-dessus.",
        "maman|La pierre, le dessin, ou les racines ?",
    ],
    3: [
        "narrateur|Près de la table, le vent tient la nappe.",
        "narrateur|Les carreaux bleus claquent, un peu.",
        "papa|La nappe, s'asseoir, ou le vase ?",
    ],
}

T3_SONS = {
    (1, 1): "abeille,bois",
    (1, 2): "lampe,bois",
    (1, 3): "caisse,clic",
    (2, 1): "pierre,herbe",
    (2, 2): "crayon,papier",
    (2, 3): "racines,ecorce",
    (3, 1): "nappe,vent",
    (3, 2): "banc,bois",
    (3, 3): "vase,table",
}

T3_EMPH = {
    1: {1: "caisse bleue", 2: "lampe", 3: "caisse basse"},
    2: {1: "pierre ronde", 2: "dessin", 3: "racines"},
    3: {1: "nappe", 2: "banc", 3: "vase"},
}

COL = {
    1: "Le sac reste au seuil, sage.",
    2: "Le carnet attend un dernier trait.",
    3: "La clochette dort contre sa paume.",
}


CLUE = {
    1: "La poussière du cabanon brille, un peu.",
    2: "Le ruban jaune du début penche, au-dessus.",
    3: "Un coin de nappe bleue attend, sage.",
}


def t3_core(a: int, b: int, c: int) -> list[str]:
    col = COL[a]
    if b == 1 and c == 1:
        extra = {
            1: "Le sac s'assoit entre eux, lourd.",
            2: "Le carnet repose sur les genoux.",
            3: "La clochette reste fermée dans le poing.",
        }[a]
        return [
            "enfant-f|On attend.",
            "copain|Oui.",
            "narrateur|Ils s'assoient sur le seuil, l'un contre l'autre.",
            extra if extra.startswith("narrateur|") else f"narrateur|{extra}",
            "narrateur|Une abeille passe, puis plus rien.",
            "copain|La bleue.",
            "enfant-f|La caisse bleue.",
            f"narrateur|{col}",
            "papa|Tu as laissé la fin arriver.",
            "maman|Elle est là, maintenant.",
        ]
    if b == 1 and c == 2:
        extra = {
            1: "Le sac reste hors du rond jaune.",
            2: "Le carnet capte un bout de lumière.",
            3: "La clochette brille une seconde, muette.",
        }[a]
        return [
            "papa|J'allume la petite lampe.",
            "narrateur|Un rond jaune court sur les caisses.",
            "copain|Près de la.",
            "narrateur|Mila ne dit rien.",
            "copain|Près de la fenêtre.",
            "enfant-f|Je vois le bleu, maintenant.",
            f"narrateur|{extra}",
            f"narrateur|{col}",
            "maman|La lumière a aidé le mot.",
            "papa|Vous avez écouté jusqu'au bout.",
        ]
    if b == 1 and c == 3:
        extra = {
            1: "Le sac s'affaisse près du sol.",
            2: "Le carnet glisse vers la caisse basse.",
            3: "La clochette frôle le bois, sans son.",
        }[a]
        return [
            "enfant-f|On se baisse.",
            "narrateur|Ils s'accroupissent près des caisses.",
            "copain|Pas la haute.",
            "narrateur|Mila garde sa bouche fermée.",
            "copain|La basse.",
            "enfant-f|Celle-là, trop près du sol.",
            f"narrateur|{extra}",
            f"narrateur|{col}",
            "papa|Tu n'as pas deviné trop tôt.",
            "maman|La phrase est complète.",
        ]
    if b == 2 and c == 1:
        extra = {
            1: "Le sac reste accroché à la racine.",
            2: "Le carnet attend, ouvert, sans crayon.",
            3: "La clochette pèse, froide, dans la poche.",
        }[a]
        return [
            "enfant-f|On ne touche pas.",
            "narrateur|Les deux restent debout, immobiles.",
            "copain|La ronde.",
            "enfant-f|Celle qui ressemble à une lune.",
            "narrateur|Ils soulèvent la pierre ronde, ensemble.",
            f"narrateur|{extra}",
            f"narrateur|{col}",
            "maman|Le mot est venu, tout seul.",
            "papa|Vous l'avez laissée finir.",
            "narrateur|Le ruban jaune ne tremble plus.",
        ]
    if b == 2 and c == 2:
        extra = {
            1: "Le sac sert de table, un instant.",
            2: "Le crayon gratte le carnet, puis s'arrête.",
            3: "La clochette tient le papier, à plat.",
        }[a]
        return [
            "copain|Je dessine.",
            "narrateur|Raphaël trace un rond, dans le carnet.",
            extra if extra.startswith("narrateur|") else f"narrateur|{extra}",
            "copain|Ronde.",
            "enfant-f|Comme ton dessin.",
            "narrateur|Ils posent le papier contre la pierre ronde.",
            f"narrateur|{col}",
            "papa|Le dessin a tenu le mot.",
            "maman|Vous avez lu ensemble.",
            "narrateur|Le ruban jaune penche vers le rond.",
        ]
    if b == 2 and c == 3:
        extra = {
            1: "Le sac s'adosse à l'écorce.",
            2: "Le carnet reste ouvert sur une racine.",
            3: "La clochette se tait contre l'écorce.",
        }[a]
        return [
            "enfant-f|On s'assoit dans les racines.",
            "narrateur|L'écorce est rêche, un peu fraîche.",
            "copain|À gauche.",
            "narrateur|Mila tourne la tête, sans parler.",
            "copain|Sous les racines, à gauche.",
            "enfant-f|Je vois le coin, maintenant.",
            f"narrateur|{extra}",
            f"narrateur|{col}",
            "maman|Les racines ont gardé le secret.",
            "papa|Tu as écouté la fin.",
        ]
    if b == 3 and c == 1:
        extra = {
            1: "Le sac pèse sur un coin de nappe.",
            2: "Le carnet cale le tissu, plat.",
            3: "La clochette ancre un coin, muette.",
        }[a]
        return [
            "enfant-f|On tient la nappe.",
            "copain|Moi aussi.",
            "narrateur|Le vent lâche le tissu.",
            "copain|Le vase.",
            "enfant-f|Derrière le vase.",
            f"narrateur|{extra}",
            f"narrateur|{col}",
            "papa|La nappe s'est tue, le mot aussi.",
            "maman|Vous l'avez entendue jusqu'au bout.",
            "narrateur|Les carreaux bleus retombent, sages.",
        ]
    if b == 3 and c == 2:
        extra = {
            1: "Le sac repose sous le banc.",
            2: "Le carnet s'ouvre sur les genoux.",
            3: "La clochette reste entre deux paumes.",
        }[a]
        return [
            "enfant-f|On s'assoit, d'abord.",
            "narrateur|Le banc de bois est tiède.",
            "copain|Derrière le vase blanc.",
            "enfant-f|Pas le seau.",
            "narrateur|Ils se lèvent, ensemble.",
            f"narrateur|{extra}",
            f"narrateur|{col}",
            "papa|S'asseoir a ralenti les mots.",
            "maman|La phrase a eu sa place.",
            "narrateur|Le thym sent plus fort, tout près.",
        ]
    extra = {
        1: "Le sac penche vers le vase, pas vers le seau.",
        2: "Le carnet désigne le vase, d'un coin.",
        3: "La clochette tinte une fois, trop tard, puis se tait.",
    }[a]
    return [
        "narrateur|Le seau brille, plus proche que le vase.",
        "enfant-f|Le seau ?",
        "narrateur|Mila referme sa bouche, tout de suite.",
        "copain|Le vase.",
        "enfant-f|Derrière le vase, d'accord.",
        f"narrateur|{extra}",
        f"narrateur|{col}",
        "maman|Tu as laissé la vraie fin.",
        "papa|Le seau peut attendre.",
        "narrateur|Le vent passe ailleurs, plus loin.",
    ]


END_SONS = {1: "miettes,toile", 2: "miettes,papier", 3: "miettes,clochette"}

END_CODA = {
    1: "La toile du sac reste rêche, un peu beurrée.",
    2: "Sur le papier, un trait de beurre reste.",
    3: "La clochette reste muette, tiède dans la poche.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    rows = t3_core(a, b, c)
    rows.append(f"narrateur|{CLUE[b]}")
    return rows


def ending(a: int, b: int, c: int) -> list[str]:
    cd = END_CODA[a]
    last = {
        (1, 1, 1): "Le seuil du cabanon garde un carré d'ombre, tiède.",
        (1, 1, 2): "La poussière du cabanon se repose, jaune.",
        (1, 1, 3): "Le cabanon garde son ombre, plus rien d'autre.",
        (1, 2, 1): "Une cerise tombe, trop loin, dans l'herbe.",
        (1, 2, 2): "L'herbe tachetée se calme, sous les branches.",
        (1, 2, 3): "Une racine reprend sa place, rêche.",
        (1, 3, 1): "La table redevient une table, simple.",
        (1, 3, 2): "La nappe à carreaux bleus retombe, et reste.",
        (1, 3, 3): "Le seau garde son ombre, tout seul.",
        (2, 1, 1): "Le crayon repose, sans écrire, sur le seuil.",
        (2, 1, 2): "Le rond jaune de la lampe s'éteint, lent.",
        (2, 1, 3): "Une page du carnet se referme, sur le beurre.",
        (2, 2, 1): "Le ruban jaune ne tremble plus, au cerisier.",
        (2, 2, 2): "Le dessin du carnet colle à la pierre ronde.",
        (2, 2, 3): "Plus de secret au cerisier, ce soir.",
        (2, 3, 1): "Le vent passe ailleurs, loin de la nappe.",
        (2, 3, 2): "Les pieds restent sous la table, sages.",
        (2, 3, 3): "Un coin de nappe garde une miette ronde.",
        (3, 1, 1): "La clochette n'a pas tinté, une seule fois.",
        (3, 1, 2): "Le métal reflète la lampe, puis s'éteint.",
        (3, 1, 3): "Le seuil craque, sans tintement.",
        (3, 2, 1): "Le pinson se tait, au-dessus du ruban.",
        (3, 2, 2): "Le ruban jaune penche vers les miettes.",
        (3, 2, 3): "L'écorce garde une trace de métal, froide.",
        (3, 3, 1): "Les carreaux bleus ne claquent plus.",
        (3, 3, 2): "Le thym pique un peu, sur les lèvres.",
        (3, 3, 3): "Le toc de la boîte répond au toc du bois.",
    }[(a, b, c)]

    def pack(rows: list[str]) -> list[str]:
        rows.insert(-1, "narrateur|Ça sent le beurre, comme au pouce.")
        return rows

    if b == 1 and c == 1:
        return pack([
            "narrateur|La caisse bleue s'ouvre, un petit clic.",
            "narrateur|Une boîte à pois sent le beurre.",
            "enfant-f|On les a.",
            "copain|Parce que tu as attendu.",
            "papa|Merci, Mila.",
            "maman|Un pour Raphaël, un pour toi.",
            f"narrateur|{cd}",
            f"narrateur|{last}",
        ])
    if b == 1 and c == 2:
        return pack([
            "narrateur|Près de la fenêtre, la caisse bleue attend.",
            "enfant-f|Le rond jaune l'a montrée.",
            "copain|Et le mot, après.",
            "papa|Merci d'avoir écouté.",
            "narrateur|Ils croquent, tout petit, à l'ombre.",
            "narrateur|Le couvercle fait toc, comme ce matin.",
            f"narrateur|{cd}",
            f"narrateur|{last}",
        ])
    if b == 1 and c == 3:
        return pack([
            "narrateur|La caisse basse livre la boîte, tout de suite.",
            "enfant-f|Elle était trop près du sol.",
            "copain|La haute était vide.",
            "papa|Merci de ne pas avoir deviné.",
            "maman|Le beurre sent chaud.",
            f"narrateur|{cd}",
            "narrateur|Ils s'assoient sur le seuil, les miettes aux doigts.",
            f"narrateur|{last}",
        ])
    if b == 2 and c == 1:
        return pack([
            "narrateur|Sous la pierre ronde, la boîte est fraîche.",
            "enfant-f|Comme une lune, tu avais dit.",
            "copain|Oui.",
            "papa|Merci d'avoir attendu le mot.",
            "maman|Goûtez, un chacun.",
            f"narrateur|{cd}",
            "narrateur|Le couvercle à pois fait toc.",
            f"narrateur|{last}",
        ])
    if b == 2 and c == 2:
        return pack([
            "narrateur|Le dessin colle à la pierre, un peu beurré.",
            "copain|Le rond était le bon.",
            "enfant-f|On a lu ensemble.",
            "papa|Merci, Mila.",
            "narrateur|Un biscuit casse, net, entre les dents.",
            f"narrateur|{cd}",
            "narrateur|Le ruban jaune a montré le verger.",
            f"narrateur|{last}",
        ])
    if b == 2 and c == 3:
        return pack([
            "narrateur|À gauche, sous les racines, la boîte attend.",
            "enfant-f|Tu as dit à gauche, à la fin.",
            "copain|Oui, à la fin.",
            "papa|Merci d'avoir écouté jusque-là.",
            "maman|Les miettes, dans l'herbe, toutes petites.",
            f"narrateur|{cd}",
            "narrateur|Alors le goûter de la cabane peut commencer.",
            f"narrateur|{last}",
        ])
    if b == 3 and c == 1:
        return pack([
            "narrateur|Derrière le vase, la boîte touche le bois.",
            "enfant-f|La nappe s'est tue, d'abord.",
            "copain|Puis j'ai fini.",
            "papa|Merci d'avoir tenu le tissu.",
            "maman|Un biscuit chacun, sur la nappe.",
            f"narrateur|{cd}",
            "narrateur|Le vent a lâché les carreaux bleus.",
            f"narrateur|{last}",
        ])
    if b == 3 and c == 2:
        return pack([
            "narrateur|Derrière le vase blanc, ça sent le beurre.",
            "enfant-f|Le seau n'avait rien.",
            "copain|Le banc nous a aidés.",
            "papa|Merci de vous être assis.",
            f"narrateur|{cd}",
            "narrateur|Ils croquent, les pieds sous la table.",
            "narrateur|Une miette reste au pouce de Mila.",
            f"narrateur|{last}",
        ])
    return pack([
        "narrateur|Derrière le vase, pas derrière le seau.",
        "enfant-f|J'ai failli dire le seau.",
        "copain|Tu as attendu ma fin.",
        "papa|Merci, Mila.",
        "maman|Le biscuit casse, net.",
        f"narrateur|{cd}",
        "narrateur|Le toc de la boîte est le bon toc.",
        f"narrateur|{last}",
    ])


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "nappe,portail",
        {"emphasis": "boîte à pois"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le sac", "le carnet", "la clochette"), "pause_before": 200},
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
            {"emphasis": "boîte à pois"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le cabanon", "le cerisier", "la table"), "pause_before": 200},
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
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", END_SONS[a],
                    {"emphasis": "biscuits"},
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
        "jules",
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
        "laisser le temps",
        "finir sa phrase",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "raphaël" not in blob and "raphael" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: copain absent")

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

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-018 — Les biscuits de Mila au fond du jardin\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.002 — laisser l'autre finir (vécue, jamais dite)\n"
        "- **Personnages :** Mila, Raphaël, papa, maman\n"
        "- **Lieu :** jardin aromatique, fin d'après-midi : goûter de la cabane, "
        "verger des rubans, table du thym\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Au jardin aromatique, la nappe à carreaux bleus se soulève. Un ruban jaune "
        "pend au cerisier. Mila a caché sa boîte à pois pour le goûter de la cabane, "
        "avant le vent. Raphaël coupe : « Caisse ! » Le mot n'est pas fini. "
        "Sac, carnet ou clochette : les trois partent ; Mila reprend trop vite. "
        "Cabanon (caisses), verger des rubans (pierres), table du thym (vent). "
        "Attendre, lampe, caisse basse ; pierre, dessin, racines ; nappe, s'asseoir, vase. "
        "La phrase finit. La boîte fait toc. On croque.\n\n"
        "## Vécu\n\n"
        "Mila veut les biscuits **maintenant**. Raphaël prend son temps. "
        "Première idée : deviner trop tôt. Ça rate. "
        "Chaque choix change l'obstacle et le climax (poussière, ruban, nappe). "
        "La leçon se voit : couper fait manquer la boîte ; laisser finir la trouve. "
        "Fin : miette au pouce + image unique du chemin (seuil, ruban, toc).\n\n"
        "## Vu et corrigé\n\n"
        "- Jules / Tom / Léa / Sami / bac-toboggan / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Mila (`enfant-f`), Raphaël (`copain`), rythmes distincts, silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Merci vécu. Question d'adulte. Un « en ce moment ».\n"
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
