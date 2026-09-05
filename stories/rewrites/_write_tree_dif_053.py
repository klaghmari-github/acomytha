#!/usr/bin/env python3
"""TREE-DIF-053 — Le nichoir de Nina et le merle du pommier (N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-053"
N2 = 15
TITLE = "Le nichoir de Nina et le merle du pommier"
FIL = (
    "Nina veut accrocher son nichoir et le remplir de graines pour le merle "
    "du pommier, avant que l'oiseau revienne de la haie. Elle veut qu'Aniss "
    "crie merle et monte le bois tout de suite. Aniss répond avec les mains, "
    "pose deux doigts sur le clou à tête ronde. Première idée ratée : trop vite, "
    "le nichoir tape l'herbe. T1 = nichoir / ficelle / graines (les trois partent). "
    "T2 = branche trop basse / fourche trop haute / tronc trop lisse. "
    "T3 = neuf façons d'attendre ses mains. Le clou du toit paie la fin."
)
CHARS = "Nina, Aniss, papa, maman"
SETTING = "sous le pommier, branche, fourche, tronc"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "clou à tête ronde",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le merle n_est_pas_là_mais_Nina_veut_tout_de_suite; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la manière d_attendre; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tend; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_objets_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_Aniss_se_tait; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=Nina_veut_jeter_Aniss_veut_regarder; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_clou_du_début_montre_la_place; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_nichoir_tient_le_merle_peut_venir; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
    "narrateur|Sous le pommier, deux pommes sèches se tapent.",
    "narrateur|Ça fait toc, contre le bois du tronc.",
    "narrateur|Ça sent le fruit chaud, et la résine.",
    "narrateur|Une guêpe quitte une pomme, sans bruit.",
    "narrateur|Nina connaît chaque fourche de cet arbre.",
    "papa|Le merle est dans la haie, Nina.",
    "maman|Ton nichoir de bois attend dans l'herbe.",
    "narrateur|Sur le toit, un clou à tête ronde luit.",
    "enfant-f|On dirait une petite baie.",
    "narrateur|En ce moment, Nina tient la ficelle.",
    "enfant-f|Il va habiter là, avant son retour.",
    "papa|Le merle, tout en haut ?",
    "enfant-f|Oui, et les graines dedans.",
    "narrateur|Le portillon claque, une fois.",
    "narrateur|Aniss arrive, son sac frotte l'herbe.",
    "narrateur|Son sac sent l'herbe coupée.",
    "enfant-f|Dis merle, Aniss !",
    "narrateur|Aniss s'accroupit près du bois.",
    "narrateur|Il pose deux doigts sur le clou.",
    "narrateur|Il ne dit rien.",
    "narrateur|Le sourire de Nina s'en va.",
    "narrateur|Elle veut crier, et elle veut réussir.",
    "narrateur|Dans sa poitrine, l'envie pousse trop fort.",
    "maman|Tu peux lui tendre quelque chose.",
    "papa|Merci, tu as tenu le nichoir droit.",
]

T1_CHOICE = [
    "narrateur|Près des pieds, trois affaires attendent.",
    "narrateur|Le nichoir, la ficelle, les graines.",
    "papa|Tu prends quoi d'abord, Nina ?",
]

T1 = {
    1: {
        "lab": "le nichoir",
        "sons": "bois,herbe",
        "emphasis": "nichoir",
        "passage": [
            "narrateur|Nina prend d'abord le nichoir de bois.",
            "enfant-f|Il sent la résine, Aniss.",
            "papa|Garde le toit contre toi.",
            "narrateur|Elle le pousse trop vite vers lui.",
            "enfant-f|Dis merle, et monte-le !",
            "narrateur|Aniss pose deux doigts sur le clou.",
            "enfant-m|Pas maintenant.",
            "narrateur|Le nichoir tape l'herbe, trop bas.",
            "narrateur|Le sourire de Nina s'en va.",
            "maman|La ficelle et les graines viennent aussi.",
            "narrateur|Papa glisse le tout dans le panier.",
            "narrateur|Les trois partent, collés au bois.",
            "enfant-f|J'ai trop poussé.",
            "papa|Le nichoir d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nina a tendu le nichoir, trop vite.",
            "maman|Elle a tendu quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "nichoir",
            "accepted_examples": "nichoir | le nichoir | le bois | le toit",
            "retry_prompt": "Nina tend le nichoir. Elle tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde le nichoir contre lui.",
            "enfant-f|Il est à toi, un moment.",
            "narrateur|Nina ouvre les mains, sans répéter.",
            "maman|Le bois est tiède, sous le clou.",
            "papa|On pose le nichoir où ?",
            "enfant-f|Vers le pommier, plus haut.",
            "narrateur|Le clou à tête ronde luit, vers la haie.",
        ],
        "voy": "Le nichoir penche vers le pommier.",
    },
    2: {
        "lab": "la ficelle",
        "sons": "ficelle,herbe",
        "emphasis": "ficelle",
        "passage": [
            "narrateur|Nina prend d'abord la ficelle beige.",
            "enfant-f|Elle gratte un peu, Aniss.",
            "maman|Garde la bobine dans tes mains.",
            "narrateur|Elle enroule trop vite, trop fort.",
            "enfant-f|Noue, Aniss, vite !",
            "narrateur|Aniss tient la bobine, sans un mot.",
            "enfant-m|Doucement.",
            "narrateur|Le fil s'emmêle, près de l'herbe.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "papa|Le nichoir et les graines viennent aussi.",
            "narrateur|Maman les pose contre le bois.",
            "narrateur|Les trois partent, collés au fil.",
            "enfant-f|J'ai trop tiré.",
            "maman|La ficelle d'abord, tu l'as.",
        ],
        "question": [
            "narrateur|Nina a tendu la ficelle, trop vite.",
            "maman|Elle a tendu quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "ficelle",
            "accepted_examples": "ficelle | la ficelle | le fil | la bobine",
            "retry_prompt": "Nina tend la ficelle. Elle tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde la ficelle contre sa jambe.",
            "enfant-f|Elle est à toi, un moment.",
            "narrateur|Nina se tait, les lèvres fermées.",
            "papa|Le fil sent le tiroir, un peu.",
            "maman|On pose le nichoir où ?",
            "enfant-f|Vers la fourche, plus tard.",
            "narrateur|Le clou à tête ronde luit, au bout du fil.",
        ],
        "voy": "La ficelle penche vers le pommier.",
    },
    3: {
        "lab": "les graines",
        "sons": "graines,papier",
        "emphasis": "graines",
        "passage": [
            "narrateur|Nina prend d'abord le sachet de graines.",
            "enfant-f|Ça sent le tournesol, Aniss.",
            "papa|Garde le sachet près du bois.",
            "narrateur|Elle verse trop vite, d'un coup.",
            "enfant-f|Mets tout, Aniss !",
            "narrateur|Aniss ramasse une graine, très lent.",
            "enfant-m|Une.",
            "narrateur|Il la pose dans le nichoir, sans un mot.",
            "narrateur|Le sourire de Nina s'en va.",
            "maman|Le nichoir et la ficelle viennent aussi.",
            "narrateur|Papa les glisse près du tronc.",
            "narrateur|Les trois partent, près du sachet.",
            "enfant-f|J'ai trop versé.",
            "papa|Les graines d'abord, tu les as.",
        ],
        "question": [
            "narrateur|Nina a tendu les graines, trop vite.",
            "maman|Elle a tendu quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "graines",
            "accepted_examples": "graines | les graines | le sachet | le tournesol",
            "retry_prompt": "Nina tend les graines. Elle tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss tient le sachet, tout près.",
            "enfant-f|Il est à toi, un moment.",
            "narrateur|Nina attend, sans verser.",
            "papa|Une graine brille, ronde comme le clou.",
            "maman|On pose le nichoir où ?",
            "enfant-f|Vers le tronc, peut-être.",
            "narrateur|Le clou à tête ronde luit, au-dessus des graines.",
        ],
        "voy": "Les graines penchent vers le pommier.",
    },
}

T2 = {
    (1, 1): {
        "sons": "herbe,bois",
        "emphasis": "branche",
        "passage": [
            "narrateur|Le nichoir tape l'herbe, trop bas.",
            "narrateur|La branche basse penche trop, juste là.",
            "enfant-f|Monte-le, Aniss !",
            "narrateur|Aniss montre une branche plus haute, du doigt.",
            "enfant-m|Là.",
            "narrateur|Nina lève le bois, puis s'arrête.",
            "narrateur|Elle ne jette pas.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|Le tabouret dort près du tronc.",
            "narrateur|Le clou à tête ronde luit, vers le haut.",
            "papa|On le monte comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "feuilles,vent",
        "emphasis": "fourche",
        "passage": [
            "narrateur|Le nichoir n'atteint pas la fourche.",
            "enfant-f|C'est trop haut, Aniss.",
            "narrateur|Une pomme cache le creux, un peu.",
            "enfant-f|Jette, Aniss !",
            "narrateur|Aniss lève les bras, puis les baisse.",
            "enfant-m|Pas jeter.",
            "narrateur|Nina serre le bois, les joues chaudes.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|Le vent peut pencher la fourche.",
            "narrateur|Le clou à tête ronde luit, trop loin.",
            "papa|On l'accroche comment, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "ecorce,ficelle",
        "emphasis": "tronc",
        "passage": [
            "narrateur|Le nichoir glisse le long du tronc.",
            "enfant-f|Ça glisse, Aniss !",
            "narrateur|Nina serre trop vite, trop fort.",
            "enfant-f|Dis nœud !",
            "narrateur|Aniss pointe l'écorce lisse, du doigt.",
            "enfant-m|Lisse.",
            "narrateur|Le sourire de Nina s'en va.",
            "narrateur|Elle pose le bois, sans crier.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|La pince dort près du panier.",
            "narrateur|Le clou à tête ronde luit, de travers.",
            "papa|On le tient comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "herbe,ficelle",
        "emphasis": "branche",
        "passage": [
            "narrateur|La ficelle traîne dans l'herbe, trop bas.",
            "narrateur|La branche basse tape le fil.",
            "enfant-f|Tire-la, Aniss !",
            "narrateur|Aniss montre une branche plus haute, du doigt.",
            "enfant-m|Plus haut.",
            "narrateur|Nina tire, puis relâche le fil.",
            "narrateur|Elle ne jette pas la bobine.",
            "narrateur|Dans sa poitrine, ça pousse, puis ça recule.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|Le tabouret peut porter le fil.",
            "narrateur|Le clou à tête ronde luit, au bout du fil.",
            "papa|On le monte comment, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "vent,ficelle",
        "emphasis": "fourche",
        "passage": [
            "narrateur|La ficelle n'atteint pas la fourche.",
            "enfant-f|Le fil est trop court, Aniss.",
            "narrateur|Le vent soulève un bout, puis le lâche.",
            "enfant-f|Lance le fil !",
            "narrateur|Aniss enroule un tour, sans lancer.",
            "enfant-m|Pas lancer.",
            "narrateur|Nina ouvre la bouche, puis la ferme.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|Vos mains peuvent faire un pont.",
            "narrateur|Le clou à tête ronde luit, trop haut.",
            "papa|On l'accroche comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "ecorce,ficelle",
        "emphasis": "tronc",
        "passage": [
            "narrateur|La ficelle glisse le long du tronc.",
            "enfant-f|Le fil part, Aniss !",
            "narrateur|Nina noue trop vite, le nœud lâche.",
            "enfant-f|Serre, Aniss !",
            "narrateur|Aniss pointe l'écorce lisse, du doigt.",
            "enfant-m|Ça glisse.",
            "narrateur|Nina lâche le fil, les doigts chauds.",
            "narrateur|Elle ne recommence pas trop fort.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|La pince peut pincer le fil.",
            "narrateur|Le clou à tête ronde luit, de travers.",
            "papa|On le tient comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "graines,herbe",
        "emphasis": "branche",
        "passage": [
            "narrateur|Les graines tombent trop près de l'herbe.",
            "narrateur|La branche basse penche, trop bas.",
            "enfant-f|Pose-les, Aniss !",
            "narrateur|Aniss montre une branche plus haute, du doigt.",
            "enfant-m|Pas là.",
            "narrateur|Nina referme le sachet, d'un coup.",
            "narrateur|Elle ne verse plus.",
            "narrateur|Dans sa poitrine, l'envie recule un peu.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|Le tabouret peut porter le sachet.",
            "narrateur|Le clou à tête ronde luit, au-dessus des graines.",
            "papa|On le monte comment, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "vent,graines",
        "emphasis": "fourche",
        "passage": [
            "narrateur|Les graines n'arrivent pas à la fourche.",
            "enfant-f|C'est trop haut pour le sachet.",
            "narrateur|Le vent chasse une graine, vers l'herbe.",
            "enfant-f|Jette le sachet !",
            "narrateur|Aniss serre le papier, contre lui.",
            "enfant-m|Non.",
            "narrateur|Nina tend la main, puis la rentre.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|Le vent peut pencher, un peu.",
            "narrateur|Le clou à tête ronde luit, trop loin.",
            "papa|On l'accroche comment, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "ecorce,graines",
        "emphasis": "tronc",
        "passage": [
            "narrateur|Les graines tombent le long du tronc.",
            "enfant-f|Elles glissent, Aniss !",
            "narrateur|Nina verse trop près de l'écorce.",
            "enfant-f|Mets-les dans le trou !",
            "narrateur|Aniss pointe l'écorce lisse, du doigt.",
            "enfant-m|Pas ici.",
            "narrateur|Nina referme le sachet, les joues chaudes.",
            "narrateur|Elle pose le papier, sans verser.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "maman|La fourche peut garder les graines.",
            "narrateur|Le clou à tête ronde luit, de travers.",
            "papa|On le tient comment, tous les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("la branche", "le nichoir", "le tabouret"),
    2: ("le vent", "la ficelle", "les mains"),
    3: ("le nœud", "la pince", "la fourche"),
}

T3_CHOICE = {
    1: [
        "narrateur|La branche reste trop basse, trop près de l'herbe.",
        "papa|La branche, le nichoir, ou le tabouret ?",
    ],
    2: [
        "narrateur|La fourche reste trop haute, trop loin des bras.",
        "maman|Le vent, la ficelle, ou les mains ?",
    ],
    3: [
        "narrateur|La ficelle glisse sur le tronc, trop lisse.",
        "papa|Le nœud, la pince, ou la fourche ?",
    ],
}

T3_SONS = {
    (1, 1): "branche,bois",
    (1, 2): "bois,mains",
    (1, 3): "tabouret,pas",
    (2, 1): "vent,feuilles",
    (2, 2): "ficelle,bois",
    (2, 3): "mains,bois",
    (3, 1): "noeud,ficelle",
    (3, 2): "pince,ecorce",
    (3, 3): "fourche,bois",
}

T3_EMPH = {
    1: {1: "branche", 2: "nichoir", 3: "tabouret"},
    2: {1: "vent", 2: "ficelle", 3: "mains"},
    3: {1: "nœud", 2: "pince", 3: "fourche"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On regarde la branche.",
        "narrateur|Nina lève le nichoir, puis s'arrête.",
        "narrateur|Elle ne jette pas.",
        "narrateur|Aniss cherche, du doigt, très lent.",
        "narrateur|Il montre une branche plus haute.",
        "narrateur|Le clou à tête ronde luit vers cette branche.",
        "papa|Vous avez regardé, avant de monter.",
        "enfant-f|Là, Aniss.",
        "narrateur|Ils poussent le bois, sans crier.",
        "maman|Le merle n'est pas parti.",
    ],
    (1, 1, 2): [
        "enfant-f|Pour toi, le nichoir.",
        "narrateur|Nina tend les deux mains, puis attend.",
        "narrateur|Aniss pose le bois contre ses paumes.",
        "enfant-m|Le clou.",
        "narrateur|Il tourne le toit, clou vers la haie.",
        "narrateur|Nina ne reprend pas le bois.",
        "papa|Tes mains ont trouvé la place.",
        "enfant-f|Il passe !",
        "narrateur|La branche redevient facile, sous leurs doigts.",
        "maman|Le nichoir a pris le bois, tout seul.",
    ],
    (1, 1, 3): [
        "enfant-f|Le tabouret, Aniss.",
        "narrateur|Aniss pose le bois dessus, sans un mot.",
        "narrateur|Nina lève un pied, puis le pose.",
        "narrateur|Elle ne grimpe pas trop vite.",
        "narrateur|Le clou à tête ronde luit, à hauteur d'œil.",
        "enfant-m|Un pas.",
        "papa|Le tabouret a tenu, droit.",
        "enfant-f|Merci.",
        "narrateur|Ils poussent le nichoir vers la branche.",
        "maman|L'herbe peut rester plus loin.",
    ],
    (1, 2, 1): [
        "enfant-f|On attend le vent.",
        "narrateur|Aniss s'assoit dans l'herbe, les genoux pliés.",
        "narrateur|Nina s'assoit aussi, le nichoir sur les cuisses.",
        "narrateur|Elle ne jette pas vers la fourche.",
        "narrateur|Le vent penche une pomme, puis la fourche.",
        "narrateur|Le clou à tête ronde luit, plus près.",
        "papa|La fourche n'est plus trop loin.",
        "enfant-f|Maintenant.",
        "narrateur|Ils glissent le bois, pendant le souffle.",
        "maman|Vous avez laissé le vent finir.",
    ],
    (1, 2, 2): [
        "enfant-f|Tes mains, la ficelle.",
        "narrateur|Aniss tend la ficelle, près du toit.",
        "narrateur|Nina tire avec lui, sans tirer trop.",
        "narrateur|Le fil traverse comme un pont, vers la fourche.",
        "narrateur|Le clou à tête ronde avance, au bout du fil.",
        "enfant-m|On tient.",
        "papa|Vos mains suffisent, toutes les deux.",
        "enfant-f|On tient ensemble.",
        "narrateur|Le nichoir monte, sans être jeté.",
        "maman|La fourche restera après.",
    ],
    (1, 2, 3): [
        "enfant-f|Tes bras, d'abord.",
        "narrateur|Nina tend le bois vers Aniss.",
        "narrateur|Aniss lève, sans un mot, très lent.",
        "narrateur|Nina ne pousse pas ses coudes.",
        "narrateur|Le clou à tête ronde passe sous la fourche.",
        "enfant-m|Là.",
        "papa|Tes bras ont laissé le bois.",
        "enfant-f|C'est plus facile.",
        "narrateur|Une pomme rejoint le creux, puis s'arrête.",
        "maman|La fourche garde son souffle, plus loin.",
    ],
    (1, 3, 1): [
        "enfant-f|Le nœud, dessous.",
        "papa|Je vous laisse le temps, près du tronc.",
        "narrateur|Aniss noue, Nina tend le bois.",
        "narrateur|Nina ne serre pas à sa place.",
        "narrateur|Le nœud prend le clou à tête ronde.",
        "enfant-m|Tient.",
        "papa|Le nœud a tenu le bois.",
        "enfant-f|Ça tient !",
        "narrateur|Le nichoir ne glisse plus sur l'écorce.",
        "maman|Aniss a poussé sans parler.",
    ],
    (1, 3, 2): [
        "enfant-f|La pince, Aniss.",
        "narrateur|Aniss pointe la pince, du doigt.",
        "narrateur|Nina attend, puis ouvre les mains.",
        "narrateur|Elle ne l'arrache pas.",
        "narrateur|La pince pince près du clou à tête ronde.",
        "enfant-m|Pince.",
        "papa|Tes mains ont guidé la pince.",
        "enfant-f|Je le tiens.",
        "narrateur|Le fil glisse vers l'écorce, puis s'arrête.",
        "maman|Le tronc garde son ombre, plus loin.",
    ],
    (1, 3, 3): [
        "enfant-f|La fourche, Aniss.",
        "narrateur|Aniss pointe le creux, du doigt.",
        "narrateur|Nina suit le doigt, sans courir.",
        "narrateur|Ils quittent le tronc trop lisse.",
        "narrateur|Le clou à tête ronde luit dans le creux.",
        "enfant-m|Ici.",
        "papa|La fourche a montré la route.",
        "enfant-f|Il évite le tronc.",
        "narrateur|Le bois prend le chemin du creux.",
        "maman|Vos pieds restent dans l'herbe.",
    ],
    (2, 1, 1): [
        "enfant-f|On regarde la branche, avec le fil.",
        "narrateur|Nina lève la ficelle, puis s'arrête.",
        "narrateur|Elle ne lance pas la bobine.",
        "narrateur|Aniss montre une branche plus haute, du doigt.",
        "narrateur|Le fil suit le doigt, lentement.",
        "narrateur|Le clou à tête ronde luit au bout du fil.",
        "papa|Vous avez regardé, avant de tirer.",
        "enfant-f|Là, le fil.",
        "narrateur|Ils passent la ficelle, sans crier.",
        "maman|La branche n'est plus trop basse.",
    ],
    (2, 1, 2): [
        "enfant-f|Pour toi, le nichoir, et le fil.",
        "narrateur|Nina tend le bois, ficelle autour.",
        "narrateur|Aniss reçoit, les paumes ouvertes.",
        "enfant-m|Le clou.",
        "narrateur|Il tourne le toit, clou vers la haie.",
        "narrateur|Nina laisse le fil dans ses doigts.",
        "papa|Tes mains ont trouvé la place.",
        "enfant-f|Le fil passe !",
        "narrateur|La branche redevient facile, sous le fil.",
        "maman|Le nichoir a pris le bois, tout seul.",
    ],
    (2, 1, 3): [
        "enfant-f|Le tabouret, pour le fil.",
        "narrateur|Aniss pose la bobine dessus, sans un mot.",
        "narrateur|Nina pose un pied, puis attend.",
        "narrateur|Elle ne grimpe pas d'un saut.",
        "narrateur|Le clou à tête ronde luit, à hauteur d'œil.",
        "enfant-m|Un pas.",
        "papa|Le tabouret a tenu, droit.",
        "enfant-f|Merci.",
        "narrateur|Ils poussent le fil vers la branche.",
        "maman|L'herbe ne prend plus la ficelle.",
    ],
    (2, 2, 1): [
        "enfant-f|On attend le vent, fil à plat.",
        "narrateur|Aniss s'assoit, la bobine sur les genoux.",
        "narrateur|Nina s'assoit, sans lancer.",
        "narrateur|Le vent penche la fourche, un peu.",
        "narrateur|Le clou à tête ronde luit, plus près du fil.",
        "enfant-m|Maintenant.",
        "papa|La fourche n'est plus trop loin.",
        "enfant-f|Le fil peut partir.",
        "narrateur|Ils glissent la ficelle, pendant le souffle.",
        "maman|Vous avez laissé le vent finir.",
    ],
    (2, 2, 2): [
        "enfant-f|La ficelle, tes mains.",
        "narrateur|Aniss tend le fil, près du toit.",
        "narrateur|Nina tire avec lui, sans trop tirer.",
        "narrateur|Le fil traverse comme un pont, vers la fourche.",
        "narrateur|Le clou à tête ronde avance, au bout du fil.",
        "enfant-m|On tient.",
        "papa|Vos mains suffisent, toutes les deux.",
        "enfant-f|On tient ensemble.",
        "narrateur|Le nichoir monte au bout de la ficelle.",
        "maman|La fourche restera après.",
    ],
    (2, 2, 3): [
        "enfant-f|Tes bras, et le fil.",
        "narrateur|Nina tend la bobine vers Aniss.",
        "narrateur|Aniss lève le fil, sans un mot.",
        "narrateur|Nina ne pousse pas ses coudes.",
        "narrateur|Le clou à tête ronde passe sous la fourche.",
        "enfant-m|Là.",
        "papa|Tes bras ont laissé le fil.",
        "enfant-f|C'est plus facile.",
        "narrateur|Une pomme rejoint le creux, puis s'arrête.",
        "maman|La fourche garde son souffle, plus loin.",
    ],
    (2, 3, 1): [
        "enfant-f|Le nœud, avec le fil.",
        "papa|Je vous laisse le temps, près du tronc.",
        "narrateur|Aniss noue, Nina tient la bobine.",
        "narrateur|Nina ne serre pas à sa place.",
        "narrateur|Le nœud prend le clou à tête ronde.",
        "enfant-m|Tient.",
        "papa|Le nœud a tenu le fil.",
        "enfant-f|Ça tient !",
        "narrateur|La ficelle ne glisse plus sur l'écorce.",
        "maman|Aniss a poussé sans parler.",
    ],
    (2, 3, 2): [
        "enfant-f|La pince, pour le fil.",
        "narrateur|Aniss pointe la pince, du doigt.",
        "narrateur|Nina attend, puis ouvre les mains.",
        "narrateur|Elle ne l'arrache pas.",
        "narrateur|La pince pince le fil, près du clou.",
        "enfant-m|Pince.",
        "papa|Tes mains ont guidé la pince.",
        "enfant-f|Je le tiens.",
        "narrateur|Le fil s'arrête contre l'écorce, net.",
        "maman|Le tronc garde son ombre, plus loin.",
    ],
    (2, 3, 3): [
        "enfant-f|La fourche, avec le fil.",
        "narrateur|Aniss pointe le creux, du doigt.",
        "narrateur|Nina suit le doigt, bobine contre elle.",
        "narrateur|Ils quittent le tronc trop lisse.",
        "narrateur|Le clou à tête ronde luit dans le creux.",
        "enfant-m|Ici.",
        "papa|La fourche a montré la route.",
        "enfant-f|Le fil évite le tronc.",
        "narrateur|La ficelle court le long de la fourche.",
        "maman|Vos pieds restent dans l'herbe.",
    ],
    (3, 1, 1): [
        "enfant-f|On regarde la branche, sachet fermé.",
        "narrateur|Nina lève les graines, puis s'arrête.",
        "narrateur|Elle ne verse pas dans l'herbe.",
        "narrateur|Aniss montre une branche plus haute, du doigt.",
        "narrateur|Le sachet suit le doigt, fermé.",
        "narrateur|Le clou à tête ronde luit au-dessus des graines.",
        "papa|Vous avez regardé, avant de verser.",
        "enfant-f|Là, les graines.",
        "narrateur|Ils posent le sachet, sans crier.",
        "maman|La branche n'est plus trop basse.",
    ],
    (3, 1, 2): [
        "enfant-f|Pour toi, le nichoir, et les graines.",
        "narrateur|Nina tend le bois, sachet contre le toit.",
        "narrateur|Aniss reçoit, les paumes ouvertes.",
        "enfant-m|Le clou.",
        "narrateur|Il tourne le toit, clou vers la haie.",
        "narrateur|Nina laisse une graine dans sa main.",
        "papa|Tes mains ont trouvé la place.",
        "enfant-f|Elles passent !",
        "narrateur|La branche redevient facile, sous le sachet.",
        "maman|Le nichoir a pris le bois, tout seul.",
    ],
    (3, 1, 3): [
        "enfant-f|Le tabouret, pour les graines.",
        "narrateur|Aniss pose le sachet dessus, sans un mot.",
        "narrateur|Nina pose un pied, puis attend.",
        "narrateur|Elle ne grimpe pas d'un saut.",
        "narrateur|Le clou à tête ronde luit, à hauteur d'œil.",
        "enfant-m|Un pas.",
        "papa|Le tabouret a tenu, droit.",
        "enfant-f|Merci.",
        "narrateur|Ils poussent le sachet vers la branche.",
        "maman|L'herbe ne prend plus les graines.",
    ],
    (3, 2, 1): [
        "enfant-f|On attend le vent, sachet fermé.",
        "narrateur|Aniss s'assoit, le papier sur les genoux.",
        "narrateur|Nina s'assoit, sans verser.",
        "narrateur|Le vent penche la fourche, un peu.",
        "narrateur|Le clou à tête ronde luit, plus près du sachet.",
        "enfant-m|Maintenant.",
        "papa|La fourche n'est plus trop loin.",
        "enfant-f|Les graines peuvent monter.",
        "narrateur|Ils glissent le sachet, pendant le souffle.",
        "maman|Vous avez laissé le vent finir.",
    ],
    (3, 2, 2): [
        "enfant-f|La ficelle, pour les graines.",
        "narrateur|Aniss tend le fil, près du sachet.",
        "narrateur|Nina tire avec lui, sans trop tirer.",
        "narrateur|Le fil traverse comme un pont, vers la fourche.",
        "narrateur|Le clou à tête ronde avance, au bout du fil.",
        "enfant-m|On tient.",
        "papa|Vos mains suffisent, toutes les deux.",
        "enfant-f|On tient ensemble.",
        "narrateur|Les graines suivent le fil, tout droit.",
        "maman|La fourche restera après.",
    ],
    (3, 2, 3): [
        "enfant-f|Tes bras, et les graines.",
        "narrateur|Nina tend le sachet vers Aniss.",
        "narrateur|Aniss lève le papier, sans un mot.",
        "narrateur|Nina ne pousse pas ses coudes.",
        "narrateur|Le clou à tête ronde passe sous la fourche.",
        "enfant-m|Là.",
        "papa|Tes bras ont laissé le sachet.",
        "enfant-f|C'est plus facile.",
        "narrateur|Une pomme rejoint le creux, puis s'arrête.",
        "maman|La fourche garde son souffle, plus loin.",
    ],
    (3, 3, 1): [
        "enfant-f|Le nœud, sous les graines.",
        "papa|Je vous laisse le temps, près du tronc.",
        "narrateur|Aniss noue, Nina tient le sachet.",
        "narrateur|Nina ne serre pas à sa place.",
        "narrateur|Le nœud prend le clou à tête ronde.",
        "enfant-m|Tient.",
        "papa|Le nœud a tenu les graines.",
        "enfant-f|Ça tient !",
        "narrateur|Les graines ne glissent plus sur l'écorce.",
        "maman|Aniss a poussé sans parler.",
    ],
    (3, 3, 2): [
        "enfant-f|La pince, pour les graines.",
        "narrateur|Aniss pointe la pince, du doigt.",
        "narrateur|Nina attend, puis ouvre les mains.",
        "narrateur|Elle ne l'arrache pas.",
        "narrateur|La pince pince près du clou, sachet contre.",
        "enfant-m|Pince.",
        "papa|Tes mains ont guidé la pince.",
        "enfant-f|Je le tiens.",
        "narrateur|Une graine s'arrête contre l'écorce, nette.",
        "maman|Le tronc garde son ombre, plus loin.",
    ],
    (3, 3, 3): [
        "enfant-f|La fourche, pour les graines.",
        "narrateur|Aniss pointe le creux, du doigt.",
        "narrateur|Nina suit le doigt, sachet contre elle.",
        "narrateur|Ils quittent le tronc trop lisse.",
        "narrateur|Le clou à tête ronde luit dans le creux.",
        "enfant-m|Ici.",
        "papa|La fourche a montré la route.",
        "enfant-f|Elles évitent le tronc.",
        "narrateur|Les graines tiennent derrière la fourche.",
        "maman|Vos pieds restent dans l'herbe.",
    ],
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le nichoir pose un toc sur la branche.",
        "enfant-m|Toc.",
        "enfant-f|Il est arrivé.",
        "papa|La branche haute a laissé le passage.",
        "maman|Le merle peut venir, près du clou.",
        "narrateur|Aniss pose une main sur le toit.",
        "narrateur|Le merle quitte la haie, presque trop tard.",
        "narrateur|Un copeau reste coincé sous le clou rond.",
    ],
    (1, 1, 2): [
        "narrateur|Le bois a contourné l'herbe, jusqu'en haut.",
        "enfant-f|Aniss l'a posé, à sa place.",
        "papa|Tu as tendu le bois, d'abord.",
        "maman|Venez, le merle reste calme.",
        "narrateur|Aniss s'assoit près du tronc.",
        "enfant-m|Merle.",
        "narrateur|L'oiseau picore le clou, une fois.",
        "narrateur|Le clou à tête ronde luit vers la haie.",
    ],
    (1, 1, 3): [
        "narrateur|Le bois court jusqu'à la branche, droit.",
        "enfant-f|On a posé le nichoir.",
        "papa|Le tabouret a tenu, droit.",
        "maman|Essuyez vos mains, Nina.",
        "narrateur|Aniss descend, un pied après l'autre.",
        "narrateur|Un merle tourne, puis revient.",
        "narrateur|Sous le tabouret, le bois reste un peu froid.",
        "narrateur|Une ombre courte reste près de l'herbe.",
    ],
    (1, 2, 1): [
        "narrateur|Le bois rejoint la fourche, léger.",
        "enfant-f|On a attendu le vent.",
        "papa|Le vent n'a plus pris vos bras.",
        "maman|Rentrez la ficelle, après le merle.",
        "enfant-m|Toc.",
        "narrateur|Une feuille se tait, puis l'autre.",
        "narrateur|Le merle allait partir, puis se pose.",
        "narrateur|Une feuille sèche s'accroche au clou, puis tombe.",
    ],
    (1, 2, 2): [
        "narrateur|Le fil pose le nichoir dans la fourche.",
        "enfant-f|On tenait, tous les deux.",
        "papa|Je remporte la ficelle, tout à l'heure.",
        "maman|Le merle vous attend.",
        "narrateur|Aniss essuie une main sur son pantalon.",
        "narrateur|Un copeau reste sur le fil.",
        "narrateur|Le merle picore, près du clou.",
        "narrateur|Un bout de ficelle beige pend sous le toit.",
    ],
    (1, 2, 3): [
        "narrateur|Les mains d'Aniss laissent le bois dans la fourche.",
        "enfant-f|C'était plus facile, là.",
        "papa|Tes bras ont guidé le nichoir.",
        "maman|Le creux gardera son ombre.",
        "narrateur|Aniss pose un doigt sur le toit.",
        "narrateur|Une pomme bouge, petite.",
        "narrateur|Le merle entre, presque trop tard.",
        "narrateur|Les paumes d'Aniss gardent la forme du bois.",
    ],
    (1, 3, 1): [
        "narrateur|Le bois tient au tronc, propre.",
        "enfant-f|On a noué, Aniss.",
        "papa|Le nœud n'a pas glissé.",
        "maman|Rentrez, l'herbe est sèche.",
        "narrateur|Aniss pose une graine sur le toit.",
        "narrateur|La graine ne bouge plus.",
        "narrateur|Le merle s'approche, puis picore le clou.",
        "narrateur|Le nœud serre le clou, ferme et net.",
    ],
    (1, 3, 2): [
        "narrateur|La pince laisse le bois contre le tronc.",
        "enfant-f|On l'a tenu, tous les deux.",
        "papa|L'écorce est restée à sa place.",
        "maman|Essuie tes chaussures, Nina.",
        "narrateur|Aniss souffle un peu sur le toit.",
        "narrateur|Un copeau blanchit, puis s'arrête.",
        "narrateur|Le merle vient, le clou vers lui.",
        "narrateur|La pince laisse une trace claire sur l'écorce.",
    ],
    (1, 3, 3): [
        "narrateur|Le bois suit la fourche, jusqu'au creux.",
        "enfant-f|L'ombre était douce.",
        "papa|La fourche a tenu, droite.",
        "maman|Le tronc n'a plus rien à dire.",
        "narrateur|Aniss touche le bois, un instant.",
        "narrateur|Une pomme revient contre le toit.",
        "narrateur|Le merle passe, puis le pommier se tait.",
        "narrateur|La fourche tient l'ombre étroite du nichoir.",
    ],
    (2, 1, 1): [
        "narrateur|Le fil pose un toc sur la branche.",
        "enfant-m|Toc.",
        "enfant-f|La ficelle est arrivée.",
        "papa|La branche haute a laissé le passage.",
        "maman|Le merle peut venir, près du clou.",
        "narrateur|Aniss garde un bout de fil, entre deux doigts.",
        "narrateur|Le merle quitte la haie, presque trop tard.",
        "narrateur|La ficelle laisse un anneau beige autour de la branche.",
    ],
    (2, 1, 2): [
        "narrateur|Le fil a contourné l'herbe, jusqu'en haut.",
        "enfant-f|Aniss a tourné le clou.",
        "papa|Tu as tendu le fil, d'abord.",
        "maman|Venez, le merle reste calme.",
        "narrateur|Aniss s'assoit près du tronc.",
        "enfant-m|Merle.",
        "narrateur|L'oiseau picore le clou, une fois.",
        "narrateur|Le clou brille au bout du fil, vers la haie.",
    ],
    (2, 1, 3): [
        "narrateur|Le fil court jusqu'à la branche, droit.",
        "enfant-f|On a posé la ficelle.",
        "papa|Le tabouret a tenu, droit.",
        "maman|Essuyez vos mains, Nina.",
        "narrateur|Aniss descend, un pied après l'autre.",
        "narrateur|Le merle tourne, puis revient.",
        "narrateur|Un tour de fil reste sur le bois du tabouret.",
        "narrateur|Un tour de ficelle reste sur le tabouret.",
    ],
    (2, 2, 1): [
        "narrateur|Le fil rejoint la fourche, léger.",
        "enfant-f|On a attendu le vent.",
        "papa|Le vent n'a plus pris vos bras.",
        "maman|Rentrez la bobine, après le merle.",
        "enfant-m|Toc.",
        "narrateur|Une feuille se tait, puis l'autre.",
        "narrateur|Le merle allait partir, puis se pose.",
        "narrateur|Le vent a tordu le fil, juste sous le clou.",
    ],
    (2, 2, 2): [
        "narrateur|Deux mains posent le fil dans la fourche.",
        "enfant-f|On tenait, tous les deux.",
        "papa|Je remporte la bobine, tout à l'heure.",
        "maman|Le merle vous attend.",
        "narrateur|Aniss essuie une main sur son pantalon.",
        "narrateur|Un copeau reste sur le fil.",
        "narrateur|Le merle picore, près du clou.",
        "narrateur|Deux brins de ficelle pendent, égaux, sous le toit.",
    ],
    (2, 2, 3): [
        "narrateur|Les bras d'Aniss laissent le fil dans la fourche.",
        "enfant-f|C'était plus facile, là.",
        "papa|Tes bras ont guidé la ficelle.",
        "maman|Le creux gardera son ombre.",
        "narrateur|Aniss pose un doigt sur le toit.",
        "narrateur|Une pomme bouge, petite.",
        "narrateur|Le merle entre, presque trop tard.",
        "narrateur|La bobine vide dort dans l'herbe, près du tronc.",
    ],
    (2, 3, 1): [
        "narrateur|Le fil tient au tronc, propre.",
        "enfant-f|On a noué, Aniss.",
        "papa|Le nœud n'a pas glissé.",
        "maman|Rentrez, l'herbe est sèche.",
        "narrateur|Aniss pose une graine sur le toit.",
        "narrateur|La graine ne bouge plus.",
        "narrateur|Le merle s'approche, puis picore le clou.",
        "narrateur|Le nœud de ficelle tient contre l'écorce lisse.",
    ],
    (2, 3, 2): [
        "narrateur|La pince laisse le fil contre le tronc.",
        "enfant-f|On l'a tenu, tous les deux.",
        "papa|L'écorce est restée à sa place.",
        "maman|Essuie tes chaussures, Nina.",
        "narrateur|Aniss souffle un peu sur le toit.",
        "narrateur|Un copeau blanchit, puis s'arrête.",
        "narrateur|Le merle vient, le clou vers lui.",
        "narrateur|La pince a pincé le fil, près du clou.",
    ],
    (2, 3, 3): [
        "narrateur|Le fil suit la fourche, jusqu'au creux.",
        "enfant-f|L'ombre était douce.",
        "papa|La fourche a tenu, droite.",
        "maman|Le tronc n'a plus rien à dire.",
        "narrateur|Aniss touche le bois, un instant.",
        "narrateur|Une pomme revient contre le toit.",
        "narrateur|Le merle passe, puis le pommier se tait.",
        "narrateur|La fourche porte un fil beige, comme un pont.",
    ],
    (3, 1, 1): [
        "narrateur|Les graines posent un toc dans le bois.",
        "enfant-m|Toc.",
        "enfant-f|Elles sont arrivées.",
        "papa|La branche haute a laissé le passage.",
        "maman|Le merle peut venir, près du clou.",
        "narrateur|Aniss pose une main sur le toit.",
        "narrateur|Le merle quitte la haie, presque trop tard.",
        "narrateur|Une graine reste collée sous le clou rond.",
    ],
    (3, 1, 2): [
        "narrateur|Le sachet a contourné l'herbe, jusqu'en haut.",
        "enfant-f|Aniss a tourné le clou.",
        "papa|Tu as tendu les graines, d'abord.",
        "maman|Venez, le merle reste calme.",
        "narrateur|Aniss s'assoit près du tronc.",
        "enfant-m|Merle.",
        "narrateur|L'oiseau picore le clou, une fois.",
        "narrateur|Le sachet vide penche contre la haie.",
    ],
    (3, 1, 3): [
        "narrateur|Le sachet court jusqu'à la branche, droit.",
        "enfant-f|On a posé les graines.",
        "papa|Le tabouret a tenu, droit.",
        "maman|Essuyez vos mains, Nina.",
        "narrateur|Aniss descend, un pied après l'autre.",
        "narrateur|Le merle tourne, puis revient.",
        "narrateur|Une graine roule, puis s'arrête.",
        "narrateur|Une graine roule sous le tabouret, puis s'arrête.",
    ],
    (3, 2, 1): [
        "narrateur|Les graines rejoignent la fourche, légères.",
        "enfant-f|On a attendu le vent.",
        "papa|Le vent n'a plus pris vos bras.",
        "maman|Rentrez le sachet, après le merle.",
        "enfant-m|Toc.",
        "narrateur|Une feuille se tait, puis l'autre.",
        "narrateur|Le merle allait partir, puis se pose.",
        "narrateur|Une graine brille dans le creux, près du clou.",
    ],
    (3, 2, 2): [
        "narrateur|Le fil pose les graines dans la fourche.",
        "enfant-f|On tenait, tous les deux.",
        "papa|Je remporte le sachet, tout à l'heure.",
        "maman|Le merle vous attend.",
        "narrateur|Aniss essuie une main sur son pantalon.",
        "narrateur|Un copeau reste sur le fil.",
        "narrateur|Le merle picore, près du clou.",
        "narrateur|Deux graines tiennent au fil, sous le toit.",
    ],
    (3, 2, 3): [
        "narrateur|Les bras d'Aniss laissent le sachet dans la fourche.",
        "enfant-f|C'était plus facile, là.",
        "papa|Tes bras ont guidé les graines.",
        "maman|Le creux gardera son ombre.",
        "narrateur|Aniss pose un doigt sur le toit.",
        "narrateur|Une pomme bouge, petite.",
        "narrateur|Le merle entre, presque trop tard.",
        "narrateur|Aniss a une graine collée au pouce.",
    ],
    (3, 3, 1): [
        "narrateur|Les graines tiennent au tronc, propres.",
        "enfant-f|On a noué, Aniss.",
        "papa|Le nœud n'a pas glissé.",
        "maman|Rentrez, l'herbe est sèche.",
        "narrateur|Aniss pose une graine sur le toit.",
        "narrateur|La graine ne bouge plus.",
        "narrateur|Le merle s'approche, puis picore le clou.",
        "narrateur|Une graine est prise dans le nœud, sans tomber.",
    ],
    (3, 3, 2): [
        "narrateur|La pince laisse le sachet contre le tronc.",
        "enfant-f|On l'a tenu, tous les deux.",
        "papa|L'écorce est restée à sa place.",
        "maman|Essuie tes chaussures, Nina.",
        "narrateur|Aniss souffle un peu sur le toit.",
        "narrateur|Un copeau blanchit, puis s'arrête.",
        "narrateur|Le merle vient, le clou vers lui.",
        "narrateur|La pince tient une graine oubliée, contre l'écorce.",
    ],
    (3, 3, 3): [
        "narrateur|Les graines suivent la fourche, jusqu'au creux.",
        "enfant-f|L'ombre était douce.",
        "papa|La fourche a tenu, droite.",
        "maman|Le tronc n'a plus rien à dire.",
        "narrateur|Aniss touche le bois, un instant.",
        "narrateur|Une pomme revient contre le toit.",
        "narrateur|Le merle passe, puis le pommier se tait.",
        "narrateur|La fourche cache une graine, dans son creux.",
    ],
}

END_SONS = {1: "merle,branche", 2: "merle,vent", 3: "merle,tronc"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "pommier,pomme"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("le nichoir", "la ficelle", "les graines")},
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
                "narrateur|Le pommier ouvre trois places.",
                "narrateur|La branche basse tape l'herbe.",
                "maman|La fourche est trop haute, trop loin.",
                "narrateur|Le tronc fait glisser la ficelle.",
                "papa|On commence où, pour le merle ?",
            ],
            "choice",
            "",
            {"fields": t3lab("la branche", "la fourche", "le tronc")},
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
        "mission accomplie",
        "j'ai compris",
        "aujourd'hui,",
        "trois notes",
        "couleur de miel",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "maya",
        "parle peu",
        "camarade",
        "timide",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "zoé",
        "lina",
        "iris",
        "banc de bois",
        "étoile brune",
        "tout doux",
        "tout calme",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "nichoir" not in blob or "merle" not in blob:
        raise SystemExit(f"{SID}: nichoir/merle absents")
    if "clou à tête ronde" not in blob:
        raise SystemExit(f"{SID}: indice clou absent")

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
        "# TREE-DIF-053 — Le nichoir de Nina et le merle du pommier\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — un camarade qui parle peu (vécue : attendre, tendre, "
        "ne pas forcer la parole)\n"
        "- **Personnages :** Nina, Aniss, papa, maman\n"
        "- **Lieu :** sous le pommier, branche, fourche, tronc\n"
        "- **Indice :** clou à tête ronde sur le toit (ouverture → climax)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sous le pommier, deux pommes sèches se tapent. Nina veut accrocher son nichoir "
        "et le remplir de graines **avant que le merle revienne de la haie**. "
        "Sur le toit, un clou à tête ronde luit. Aniss arrive. Nina veut qu'il crie "
        "« merle » et monte le bois tout de suite. Aniss pose deux doigts sur le clou, "
        "sans un mot. Première idée ratée : trop vite, le bois tape l'herbe. "
        "Elle prend le nichoir, la ficelle ou les graines (les trois partent) ; "
        "la branche est trop basse, la fourche trop haute ou le tronc trop lisse ; "
        "une action change l'attente (branche, nichoir, tabouret ; vent, ficelle, mains ; "
        "nœud, pince, fourche). Le clou du début paie. Le merle vient. On rentre.\n\n"
        "## Vécu\n\n"
        "Nina veut le nichoir **maintenant**. Elle pousse Aniss à parler. Silence, "
        "doigts sur le clou, bois trop bas. Chaque choix change l'obstacle et le climax. "
        "La leçon se voit : crier « dis merle » donne une bouche fermée ; tendre et "
        "regarder ses mains donne la branche haute, le clou vers la haie, le tabouret, "
        "le vent, le pont de ficelle, les bras, le nœud, la pince, la fourche. "
        "Fin : nichoir accroché + merle, image unique du chemin (copeau, clou, graine, fil).\n\n"
        "## Vu et corrigé\n\n"
        "- Monde ≠ TREE-COL-023 (banc, pomme, étoile brune, Mila). Ici : nichoir, merle, branche.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Refrains merle trois notes / miel / Mission accomplie / J'ai compris jetés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (nichoir tenu droit). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
