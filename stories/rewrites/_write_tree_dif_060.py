#!/usr/bin/env python3
"""TREE-DIF-060 — Le train de boîtes de Sarah (N2, DIF.COR.003)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-060"
N2 = 15
TITLE = "Le train de boîtes de Sarah"
FIL = (
    "La lampe de papier pose un rond jaune. Un grain de laine tient dans la crinière. "
    "Sarah veut un train de boîtes jusqu'à la fenêtre, avant la lampe éteinte. "
    "Nino arrive du palier : buée, mèches, gilet trop long. Elle propose. Il se tait. "
    "Le cheval n'atteint pas l'endroit promis. T1 = cheval / boîte / foulard (les trois partent). "
    "T2 = canapé (buée), tapis (mèches), fenêtre (manches). Elle refuse de foncer. "
    "Le grain de laine paie le stop. On joue avec Nino tel qu'il arrive."
)
CHARS = "Sarah, Nino, papa, maman"
SETTING = "salon après la pluie : canapé, tapis, fenêtre"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de laine",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=un_grain_beige_dans_la_criniere; tempo=naturel; sourire=léger; respiration=ample",
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
        "emphasis": "grain de laine",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=le_jouet_n_atteint_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=nino_prend_son_temps; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de laine",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=jouer_avec_nino_tel_qu_il_arrive; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de laine",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|La lampe de papier pose un rond jaune.",
    "narrateur|Le tapis sent la pluie, restée dehors.",
    "narrateur|La gouttière laisse un dernier filet, dehors.",
    "narrateur|Sous la table, une boîte à chaussures attend.",
    "narrateur|Le cheval de bois a la crinière lisse.",
    "narrateur|Dans les poils, un grain de laine tient.",
    "papa|Tu vois ce grain, Sarah ?",
    "enfant-f|Il est beige, minuscule.",
    "maman|Un foulard à pois dort, sur le dossier.",
    "enfant-f|Je veux un train, jusqu'à la fenêtre.",
    "papa|Avant que j'éteigne la lampe ?",
    "enfant-f|Oui, sa gare, là-bas.",
    "narrateur|Des pas sonnent sur le palier mouillé.",
    "copain|Sarah.",
    "narrateur|Les lunettes de Nino gardent un rond de buée.",
    "narrateur|Ses cheveux gouttent sur le gilet trop long.",
    "enfant-f|Tu es le conducteur, maintenant.",
    "narrateur|Nino se tait.",
    "narrateur|Sarah attend une seconde, trop peu.",
    "maman|Le cacao attend, dans la cuisine.",
    "narrateur|En ce moment, Sarah tire la boîte.",
    "narrateur|Le cheval n'atteint pas le tapis promis.",
    "narrateur|Le sourire de Sarah disparaît.",
    "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
    "maman|Je m'accroupis, à ta hauteur.",
    "papa|Merci, tu as rattrapé le cheval.",
    "enfant-f|On prépare, alors.",
]

T1_CHOICE = [
    "narrateur|Près de la table, le cheval de bois attend.",
    "narrateur|La boîte à chaussures dort, vide.",
    "narrateur|Le foulard à pois est plié.",
    "maman|Tu prends quoi d'abord, Sarah ?",
]

T1 = {
    1: {
        "lab": "le cheval de bois",
        "sons": "bois,carton",
        "emphasis": "cheval de bois",
        "passage": [
            "narrateur|Sarah glisse le cheval contre sa poitrine.",
            "enfant-f|Son dos est froid, un peu.",
            "enfant-f|Nino, on part !",
            "narrateur|Nino se tait, les verres voilés.",
            "narrateur|Elle pousse trop vite, vers le tapis.",
            "narrateur|Le cheval n'atteint pas le fil promis.",
            "enfant-f|Il tombe.",
            "maman|Garde-le, on emporte tout.",
            "papa|La boîte, au bras ?",
            "narrateur|Nino prend le foulard, sans un mot.",
            "enfant-f|Tu viens ?",
            "copain|J'arrive.",
            "narrateur|Les trois affaires partent avec eux.",
            "narrateur|Le grain de laine tient, dans la crinière.",
        ],
        "question": [
            "narrateur|Le cheval de bois est dans les mains.",
            "maman|Le cheval est où ?",
        ],
        "qfields": {
            "expected_answer": "mains",
            "accepted_examples": "mains | les mains | dans les mains | ses mains",
            "retry_prompt": "Le cheval est dans les mains.",
        },
        "confirm": [
            "enfant-f|Dans les mains.",
            "papa|Oui.",
            "narrateur|Sarah cale la boîte contre son bras.",
            "maman|Le foulard, Nino le tient.",
            "copain|Je le tiens.",
            "enfant-f|On cherche la gare.",
            "narrateur|Le grain de laine luit, beige.",
            "papa|Vous allez où, maintenant ?",
        ],
    },
    2: {
        "lab": "la boîte à chaussures",
        "sons": "carton,bois",
        "emphasis": "boîte à chaussures",
        "passage": [
            "narrateur|Sarah cale la boîte contre son bras.",
            "enfant-f|Le carton gratte, au coude.",
            "enfant-f|Monte, cheval !",
            "narrateur|Nino reste au bord, sans un mot.",
            "narrateur|Elle pousse la boîte, trop vite.",
            "narrateur|Le cheval n'atteint pas le carton promis.",
            "enfant-f|Il rate la porte.",
            "papa|Garde la boîte, on emporte tout.",
            "maman|Le cheval, dans tes mains.",
            "narrateur|Nino prend le foulard, sous le gilet.",
            "enfant-f|Tu portes le foulard ?",
            "narrateur|Nino hoche la tête, tout bas.",
            "narrateur|Les trois affaires avancent avec eux.",
            "narrateur|Le grain de laine penche, au bord.",
        ],
        "question": [
            "narrateur|La boîte à chaussures est au bras.",
            "maman|La boîte est où ?",
        ],
        "qfields": {
            "expected_answer": "bras",
            "accepted_examples": "bras | le bras | au bras | son bras",
            "retry_prompt": "La boîte est au bras.",
        },
        "confirm": [
            "enfant-f|Au bras.",
            "maman|Oui.",
            "narrateur|Elle reprend le cheval, froid.",
            "papa|Le foulard, avec Nino ?",
            "copain|Oui, papa.",
            "enfant-f|Sa gare, plus loin.",
            "narrateur|Le grain de laine tient, minuscule.",
            "maman|Vous avancez ensemble, alors ?",
        ],
    },
    3: {
        "lab": "le foulard à pois",
        "sons": "tissu,carton",
        "emphasis": "foulard à pois",
        "passage": [
            "narrateur|Sarah plie le foulard, sous son bras.",
            "enfant-f|Les pois sentent le tiroir.",
            "enfant-f|Des rails, Nino, vite !",
            "narrateur|Le gilet trop long touche le tissu.",
            "narrateur|Nino recule d'un pas, silencieux.",
            "narrateur|Elle déroule trop vite, vers le tapis.",
            "narrateur|Le cheval n'atteint pas le pois promis.",
            "enfant-f|Le rail part de travers.",
            "maman|Serre le foulard, on emporte tout.",
            "papa|Le cheval et la boîte, avec vous.",
            "copain|Je prends la boîte.",
            "narrateur|Sarah garde le cheval, tout contre elle.",
            "narrateur|Rien ne reste près de la table.",
            "narrateur|Le grain de laine voyage, caché.",
        ],
        "question": [
            "narrateur|Le foulard à pois est sous le bras.",
            "papa|Le foulard est où ?",
        ],
        "qfields": {
            "expected_answer": "bras",
            "accepted_examples": "bras | le bras | sous le bras | son bras",
            "retry_prompt": "Le foulard est sous le bras.",
        },
        "confirm": [
            "enfant-f|Sous le bras.",
            "papa|Oui.",
            "narrateur|Maman lui tend le cheval, lisse.",
            "maman|La boîte, Nino la porte.",
            "copain|Elle est là.",
            "enfant-f|On déroule, plus loin.",
            "narrateur|Le grain de laine luit, sous un pois.",
            "papa|Quelle gare, pour le train ?",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le cheval tape sa hanche, à chaque pas.",
        "narrateur|Nino marche plus lent, derrière.",
        "narrateur|Le grain de laine penche, beige.",
        "papa|Le canapé, le tapis, ou la fenêtre ?",
    ],
    2: [
        "narrateur|La boîte craque, contre son coude.",
        "narrateur|Nino marche plus lent, derrière.",
        "narrateur|Le grain de laine tient, au bord.",
        "papa|Le canapé, le tapis, ou la fenêtre ?",
    ],
    3: [
        "narrateur|Un pois frotte le gilet trop long.",
        "narrateur|Nino marche plus lent, derrière.",
        "narrateur|Le grain de laine voyage, caché.",
        "maman|Le canapé, le tapis, ou la fenêtre ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "canape,radiateur",
        "emphasis": "canapé",
        "passage": [
            "narrateur|Sarah pose le cheval sur le dossier tiède.",
            "enfant-f|La gare, c'est ici, Nino !",
            "narrateur|Le radiateur souffle, trop proche.",
            "copain|Un nuage, sur mes lunettes.",
            "narrateur|Elle pousse le cheval, le long du canapé.",
            "narrateur|Nino vise trop bas, derrière la buée.",
            "narrateur|Le cheval n'atteint pas le dossier promis.",
            "enfant-f|Il glisse.",
            "narrateur|Sarah veut pousser plus fort.",
            "narrateur|Ses mains s'arrêtent, au-dessus du bois.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Tu fais comment, avec ses verres ?",
            "narrateur|Le grain de laine reste au dossier, oublié.",
        ],
    },
    (2, 1): {
        "sons": "canape,carton",
        "emphasis": "canapé",
        "passage": [
            "narrateur|Sarah cale la boîte contre le coussin tiède.",
            "enfant-f|Monte, ici !",
            "narrateur|Le radiateur souffle, trop proche.",
            "narrateur|La buée épaissit les verres de Nino.",
            "narrateur|Elle pousse la boîte, trop vite.",
            "narrateur|Nino rate le bord, trop flou.",
            "narrateur|Le cheval n'atteint pas le coussin promis.",
            "enfant-f|À côté.",
            "narrateur|Sarah veut corriger, trop vite.",
            "narrateur|Puis elle retient la boîte.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Tu fais comment, avec ses verres ?",
            "narrateur|Le grain de laine s'enfonce dans le tissu.",
        ],
    },
    (3, 1): {
        "sons": "canape,tissu",
        "emphasis": "canapé",
        "passage": [
            "narrateur|Sarah déroule le foulard le long du canapé.",
            "enfant-f|Un rail, Nino, suis-le !",
            "narrateur|Le radiateur souffle, trop proche.",
            "copain|Je vois un nuage.",
            "narrateur|Elle tire un pois, trop vite.",
            "narrateur|Nino cherche le bord, trop bas.",
            "narrateur|Le cheval n'atteint pas le pois promis.",
            "enfant-f|Le rail se plie.",
            "narrateur|Sarah veut tout tendre, trop fort.",
            "narrateur|Ses mains s'arrêtent, sur le tissu.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Tu fais comment, avec ses verres ?",
            "narrateur|Le grain de laine se cache sous un pois.",
        ],
    },
    (1, 2): {
        "sons": "tapis,eau",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Sarah pose le cheval au milieu du tapis.",
            "enfant-f|Ici, la gare du coin usé !",
            "copain|Mes cheveux sont lourds.",
            "narrateur|Une mèche goutte, comme un faux rail.",
            "narrateur|Elle suit la goutte, trop vite.",
            "narrateur|Le vrai coin usé reste derrière eux.",
            "narrateur|Le cheval n'atteint pas le coin promis.",
            "enfant-f|On a raté.",
            "narrateur|Sarah veut recommencer, trop vite.",
            "narrateur|Ses pieds s'arrêtent, sur le fil.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Tu fais comment, avec ses mèches ?",
            "narrateur|Le grain de laine attend au coin usé.",
        ],
    },
    (2, 2): {
        "sons": "tapis,carton",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Sarah pose la boîte au milieu du tapis.",
            "enfant-f|Le port, c'est ici !",
            "narrateur|Une goutte tombe dans le carton, toc.",
            "copain|Mes cheveux.",
            "narrateur|Elle essuie trop vite, du plat de la main.",
            "narrateur|La goutte dessine un chemin de travers.",
            "narrateur|Le cheval n'atteint pas le carton sec.",
            "enfant-f|Il est mouillé.",
            "narrateur|Sarah veut vider la boîte, trop vite.",
            "narrateur|Puis elle la pose.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Tu fais comment, avec ses mèches ?",
            "narrateur|Le grain de laine s'accroche au coin usé.",
        ],
    },
    (3, 2): {
        "sons": "tapis,tissu",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Sarah déroule le foulard sur le tapis usé.",
            "enfant-f|Des rails, jusqu'au coin !",
            "narrateur|Une goutte tache un pois, trop sombre.",
            "copain|Mes cheveux tombent.",
            "narrateur|Elle tire le foulard hors de la goutte.",
            "narrateur|Le pois fuit le coin usé, trop loin.",
            "narrateur|Le cheval n'atteint pas le pois promis.",
            "enfant-f|Le rail part.",
            "narrateur|Sarah veut tout ramener, trop vite.",
            "narrateur|Ses mains s'arrêtent, sur un pois.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Tu fais comment, avec ses mèches ?",
            "narrateur|Le grain de laine reste au coin, oublié.",
        ],
    },
    (1, 3): {
        "sons": "rideau,vitre",
        "emphasis": "fenêtre",
        "passage": [
            "narrateur|Sarah tend le cheval vers le rebord.",
            "enfant-f|Ta gare, Nino, la vitre !",
            "copain|Mon gilet me suit.",
            "narrateur|Une manche trop longue accroche le rideau.",
            "narrateur|Elle tire le cheval, et Nino avec.",
            "narrateur|Le rideau tombe devant le rebord.",
            "narrateur|Le cheval n'atteint pas la vitre promise.",
            "enfant-f|On ne voit plus.",
            "narrateur|Sarah veut écarter le tissu, trop vite.",
            "narrateur|Ses mains s'arrêtent, au bord du rideau.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Tu fais comment, avec ses manches ?",
            "narrateur|Le grain de laine luit contre la vitre.",
        ],
    },
    (2, 3): {
        "sons": "rideau,carton",
        "emphasis": "fenêtre",
        "passage": [
            "narrateur|Sarah glisse la boîte vers le rebord.",
            "enfant-f|Le quai, c'est la fenêtre !",
            "narrateur|Une manche trop longue balaie la boîte.",
            "copain|Ça tient mon poignet.",
            "narrateur|Elle tire plus fort, pour arriver.",
            "narrateur|Le carton part de travers, sous le rideau.",
            "narrateur|Le cheval n'atteint pas le rebord promis.",
            "enfant-f|Il tombe dans le pli.",
            "narrateur|Sarah veut plonger la main, trop vite.",
            "narrateur|Puis elle recule.",
            "enfant-f|Je ne fonce pas.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Tu fais comment, avec ses manches ?",
            "narrateur|Le grain de laine voyage dans le rideau.",
        ],
    },
    (3, 3): {
        "sons": "rideau,tissu",
        "emphasis": "fenêtre",
        "passage": [
            "narrateur|Sarah pose le foulard sous la fenêtre.",
            "enfant-f|Un tapis de gare, Nino !",
            "narrateur|Une manche trop longue froisse un pois.",
            "copain|Le gilet est long.",
            "narrateur|Elle tire le foulard sous la manche.",
            "narrateur|Le tissu s'enroule au rideau, trop haut.",
            "narrateur|Le cheval n'atteint pas le pois promis.",
            "enfant-f|Le rail grimpe.",
            "narrateur|Sarah veut tout décrocher, trop vite.",
            "narrateur|Ses mains s'arrêtent, au bas du rideau.",
            "enfant-f|Je ne fonce pas.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Tu fais comment, avec ses manches ?",
            "narrateur|Le grain de laine dort dans un pois, trop haut.",
        ],
    },
}

T3_LABS = {
    1: ("le torchon de maman", "les mains de Sarah", "un pas hors du canapé"),
    2: ("la pince de maman", "la serviette", "Sarah tient le cheval"),
    3: ("les manches retroussées", "Sarah tient la boîte", "maman noue les poignets"),
}

T3_CHOICE = {
    1: [
        "narrateur|Sur le canapé, le bord reste flou.",
        "narrateur|Le grain de laine attend, au dossier.",
        "papa|Tu fais quoi, Sarah ?",
    ],
    2: [
        "narrateur|Sur le tapis, le coin usé attend.",
        "narrateur|Le grain de laine reste derrière, oublié.",
        "maman|Tu fais quoi, avec lui ?",
    ],
    3: [
        "narrateur|Près de la vitre, le rebord disparaît.",
        "narrateur|Le grain de laine luit, trop loin.",
        "papa|Tu fais quoi, maintenant ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "enfant-f|Le torchon, maman ?",
        "maman|Tiens, pour ses verres.",
        "narrateur|Sarah veut frotter, trop vite.",
        "narrateur|Elle s'arrête, devant Nino.",
        "enfant-f|Attends, c'est toi.",
        "narrateur|Nino essuie un rond, puis l'autre.",
        "copain|Le dossier.",
        "enfant-f|Je regarde le grain.",
        "narrateur|Le grain de laine luit, au dossier.",
        "narrateur|Elle glisse le cheval jusqu'à lui.",
        "papa|Chacun son bord, chacun son temps.",
        "maman|Le train a sa gare, tiède.",
    ],
    (1, 1, 2): [
        "enfant-f|Tes mains, Nino, sous le cheval.",
        "copain|Je touche.",
        "narrateur|Sarah parle le chemin, tout bas.",
        "narrateur|Elle refuse de lui prendre les verres.",
        "enfant-f|À gauche, le coussin.",
        "narrateur|Nino pousse, à sa vitesse.",
        "narrateur|Le cheval n'était pas arrivé.",
        "enfant-f|Je regarde le grain.",
        "narrateur|Le grain de laine tient entre deux paumes.",
        "papa|Les mains ont vu, à sa place.",
        "maman|Le canapé vous a gardés.",
        "copain|Il est là.",
    ],
    (1, 1, 3): [
        "enfant-f|Un pas, hors du canapé ?",
        "papa|Un pas, hors de la buée.",
        "narrateur|Sarah veut sauter, trop vite.",
        "narrateur|Elle pose un pied, puis attend.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino descend, le gilet trop long.",
        "narrateur|L'air plus frais chasse la buée.",
        "copain|Je vois le cheval.",
        "enfant-f|Le grain, au pied.",
        "narrateur|Le grain de laine reste au pied du canapé.",
        "maman|Vous avez attendu le verre clair.",
        "papa|La gare est en bas, plus nette.",
    ],
    (1, 2, 1): [
        "enfant-f|La pince, plus haut.",
        "maman|Pour ses mèches, pas pour le train.",
        "narrateur|Sarah veut tout attacher, trop vite.",
        "narrateur|Elle tend la pince, puis attend.",
        "copain|Moi.",
        "narrateur|Nino pince une mèche, à sa hauteur.",
        "narrateur|Les gouttes cessent, sur le tapis.",
        "enfant-f|Le grain, au coin.",
        "narrateur|Le grain de laine penche sous la pince.",
        "narrateur|Elle glisse le cheval jusqu'au coin usé.",
        "papa|Ses cheveux ont eu leur place.",
        "maman|Le tapis reste sec, sous le bois.",
    ],
    (1, 2, 2): [
        "enfant-f|La serviette, maman ?",
        "maman|Pour ses cheveux, Nino.",
        "narrateur|Sarah veut frotter, trop fort.",
        "narrateur|Elle pose la serviette, puis attend.",
        "enfant-f|C'est toi.",
        "narrateur|Nino essuie une mèche, puis l'autre.",
        "copain|Plus légères.",
        "enfant-f|Je regarde le grain.",
        "narrateur|Le grain de laine s'endort dans la serviette.",
        "narrateur|Le cheval rejoint le coin usé, sec.",
        "papa|Vous avez laissé l'eau des cheveux.",
        "maman|Le tapis sent la pluie, dehors.",
    ],
    (1, 2, 3): [
        "enfant-f|Moi le cheval, toi la boîte.",
        "copain|Mes mains, le carton.",
        "narrateur|Sarah tient le cheval, trop haut d'abord.",
        "narrateur|Elle le baisse, à ses yeux.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino pose la boîte, à son pas.",
        "narrateur|Les gouttes tombent derrière, plus loin.",
        "enfant-f|Le grain, sur le dos.",
        "narrateur|Le grain de laine luit contre le bois du cheval.",
        "papa|Vous avancez avec ce que vous avez.",
        "maman|Le coin usé devient une gare.",
        "copain|J'y suis.",
    ],
    (1, 3, 1): [
        "enfant-f|Tes manches, Nino.",
        "copain|Je les remonte.",
        "narrateur|Sarah veut les tirer, trop vite.",
        "narrateur|Elle ouvre les mains, puis attend.",
        "enfant-f|Toi, à ta façon.",
        "narrateur|Nino retrousse une manche, puis l'autre.",
        "narrateur|Le rideau lâche le poignet.",
        "enfant-f|Le grain, à la vitre.",
        "narrateur|Le grain de laine voyage au bord d'une manche.",
        "narrateur|Elle tend le cheval vers le rebord.",
        "papa|Le gilet reste long, les manches libres.",
        "maman|La gare du rebord s'allume.",
    ],
    (1, 3, 2): [
        "enfant-f|Moi la boîte, toi le rideau.",
        "copain|J'écarte.",
        "narrateur|Sarah tient la boîte, trop près d'abord.",
        "narrateur|Elle recule, pour lui laisser l'air.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino écarte le rideau, à sa vitesse.",
        "narrateur|Le rebord reparaît, étroit.",
        "enfant-f|Le grain, au carton.",
        "narrateur|Le grain de laine tient au coin de la boîte.",
        "papa|Tu as tenu, sans tirer.",
        "maman|Le cheval trouve le rebord, enfin.",
        "copain|La vitre.",
    ],
    (1, 3, 3): [
        "enfant-f|Noue les poignets, maman ?",
        "maman|Un nœud souple, pour lui.",
        "narrateur|Sarah veut serrer, trop fort.",
        "narrateur|Elle pose ses mains, puis attend.",
        "enfant-f|À sa taille, pas à la mienne.",
        "narrateur|Maman noue, Nino souffle.",
        "narrateur|Les manches tiennent, le gilet reste long.",
        "copain|Je peux.",
        "enfant-f|Le grain, près du nœud.",
        "narrateur|Le grain de laine dort près du nœud.",
        "papa|Le rebord vous attendait, tout le temps.",
        "maman|Le train arrive, presque trop tard.",
    ],
    (2, 1, 1): [
        "enfant-f|Le torchon, pour tes verres.",
        "maman|Nino, c'est à toi.",
        "narrateur|Sarah tend le torchon, trop vite.",
        "narrateur|Elle le pose sur le coussin, puis attend.",
        "copain|J'essuie.",
        "narrateur|Nino frotte un verre, puis l'autre.",
        "narrateur|La boîte redevient nette, devant lui.",
        "enfant-f|Le grain, sur le verre.",
        "narrateur|Le grain de laine brille sur le verre essuyé.",
        "narrateur|Il glisse la boîte jusqu'au dossier.",
        "papa|Il a vu le bord, à sa façon.",
        "maman|Le carton a sa gare, tiède.",
    ],
    (2, 1, 2): [
        "enfant-f|Tes mains sous la boîte.",
        "copain|Je palpe.",
        "narrateur|Sarah guide avec la voix, pas les bras.",
        "narrateur|Elle refuse de pousser à sa place.",
        "enfant-f|Le coussin, tout près.",
        "narrateur|Nino avance la boîte, trop lent pour elle.",
        "narrateur|Elle attend, les dents serrées, puis lâche.",
        "enfant-f|Le grain, dans ta paume.",
        "narrateur|Le grain de laine glisse dans la paume de Nino.",
        "papa|Sa paume a trouvé le bord.",
        "maman|Le canapé tient le carton.",
        "copain|C'est bon.",
    ],
    (2, 1, 3): [
        "enfant-f|On descend, hors de la buée.",
        "papa|Un pas, pas deux.",
        "narrateur|Sarah veut emporter la boîte, trop vite.",
        "narrateur|Elle la pose d'abord, puis descend.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino suit, le gilet trop long.",
        "narrateur|La buée quitte les verres, plus bas.",
        "copain|Le parquet.",
        "enfant-f|Le grain, au sol.",
        "narrateur|Le grain de laine attend sur le parquet froid.",
        "maman|La gare est plus nette, en bas.",
        "papa|Le cheval entre, enfin.",
    ],
    (2, 2, 1): [
        "enfant-f|La pince, pour tes mèches.",
        "maman|Toi tu pinces, Nino.",
        "narrateur|Sarah veut tout faire, trop vite.",
        "narrateur|Elle ouvre la pince, puis la tend.",
        "copain|Moi.",
        "narrateur|Nino pince, à sa hauteur.",
        "narrateur|Plus de goutte dans le carton.",
        "enfant-f|Le grain, à la pince.",
        "narrateur|Le grain de laine s'accroche à la pince, beige.",
        "narrateur|La boîte rejoint le coin usé, sèche.",
        "papa|Ses mèches ont leur place, à part.",
        "maman|Le tapis garde un fil, rien de plus.",
    ],
    (2, 2, 2): [
        "enfant-f|La serviette, pour tes cheveux.",
        "maman|Frotte, Nino, à toi.",
        "narrateur|Sarah veut presser, trop fort.",
        "narrateur|Elle pose la serviette, puis recule.",
        "enfant-f|Ton rythme.",
        "narrateur|Nino essuie, une mèche après l'autre.",
        "copain|Le carton est sec.",
        "enfant-f|Le grain, un fil.",
        "narrateur|Le grain de laine laisse un fil sur la serviette.",
        "narrateur|Le cheval entre dans la boîte, au coin usé.",
        "papa|L'eau des cheveux est restée dehors.",
        "maman|Le tapis redevient un quai.",
    ],
    (2, 2, 3): [
        "enfant-f|Moi le cheval, toi tu pousses.",
        "copain|La boîte.",
        "narrateur|Sarah tient le cheval hors des gouttes.",
        "narrateur|Elle le baisse quand Nino est prêt.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino pousse, à son pas.",
        "narrateur|Le coin usé arrive, enfin.",
        "enfant-f|Le grain, au fond.",
        "narrateur|Le grain de laine veille au fond de la boîte.",
        "papa|Vous avez partagé les rôles.",
        "maman|Le tapis a tenu, malgré la pluie.",
        "copain|Gare.",
    ],
    (2, 3, 1): [
        "enfant-f|Tes manches, à toi.",
        "copain|Je les monte.",
        "narrateur|Sarah veut aider, trop vite.",
        "narrateur|Elle ouvre les mains, vide.",
        "enfant-f|Toi d'abord.",
        "narrateur|Nino retrousse, le carton contre lui.",
        "narrateur|Le rideau lâche le bord de la boîte.",
        "enfant-f|Le grain, à la manche.",
        "narrateur|Le grain de laine suit la manche retroussée.",
        "narrateur|La boîte gagne le rebord, étroite.",
        "papa|Le gilet reste long, le carton passe.",
        "maman|La vitre devient une gare.",
    ],
    (2, 3, 2): [
        "enfant-f|Je tiens la boîte, toi le rideau.",
        "copain|J'ouvre.",
        "narrateur|Sarah serre trop, d'abord.",
        "narrateur|Elle desserre, pour qu'il voie.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino écarte le rideau, trop lent.",
        "narrateur|Le rebord reparaît, juste assez.",
        "enfant-f|Le grain, au carton.",
        "narrateur|Le grain de laine penche au rebord de carton.",
        "papa|Tu as tenu sans tirer le gilet.",
        "maman|Le cheval entre, contre la vitre.",
        "copain|On y est.",
    ],
    (2, 3, 3): [
        "enfant-f|Un nœud, maman, à ses poignets.",
        "maman|Souple, pour Nino.",
        "narrateur|Sarah veut le nœud trop serré.",
        "narrateur|Elle recule, maman noue.",
        "enfant-f|À lui.",
        "narrateur|Les manches tiennent, le gilet reste long.",
        "copain|Mes mains sont libres.",
        "narrateur|Il pousse la boîte vers le rebord.",
        "enfant-f|Le grain, sous le nœud.",
        "narrateur|Le grain de laine se cache sous le nœud souple.",
        "papa|Le rebord vous attendait.",
        "maman|Le train a failli rester dans le pli.",
    ],
    (3, 1, 1): [
        "enfant-f|Le torchon, pour tes lunettes.",
        "maman|Nino essuie, Sarah attend.",
        "narrateur|Sarah tend un pois, trop vite.",
        "narrateur|Elle le lâche, puis attend.",
        "copain|Un rond, puis l'autre.",
        "narrateur|Les verres s'éclaircissent, au-dessus du foulard.",
        "narrateur|Le rail redevient un chemin.",
        "enfant-f|Le grain, sur un pois.",
        "narrateur|Le grain de laine s'accroche à un pois du foulard.",
        "narrateur|Le cheval suit le pois jusqu'au dossier.",
        "papa|Il a vu le rail, à sa façon.",
        "maman|Le canapé garde le tissu, tiède.",
    ],
    (3, 1, 2): [
        "enfant-f|Tes mains, sous le foulard.",
        "copain|Je sens les pois.",
        "narrateur|Sarah nomme le chemin, sans tirer.",
        "narrateur|Elle refuse de lui poser les verres.",
        "enfant-f|Le dossier, tout droit.",
        "narrateur|Nino tend un pois, trop lent.",
        "narrateur|Le cheval avance, à son toucher.",
        "enfant-f|Le grain, d'une main à l'autre.",
        "narrateur|Le grain de laine voyage d'une main à l'autre.",
        "papa|Ses mains ont été le regard.",
        "maman|Le foulard est arrivé, sans se plier.",
        "copain|Pois.",
    ],
    (3, 1, 3): [
        "enfant-f|Un pas, hors du canapé.",
        "papa|Hors de la buée, un pas.",
        "narrateur|Sarah veut emporter le foulard, trop vite.",
        "narrateur|Elle le laisse un instant, puis descend.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino suit, le gilet trop long.",
        "narrateur|Les verres s'éclaircissent, plus bas.",
        "copain|Le pois.",
        "enfant-f|Le grain, dans le coussin.",
        "narrateur|Le grain de laine reste dans le pli du coussin.",
        "maman|Le rail continue, au parquet.",
        "papa|Le cheval trouve le pois, enfin.",
    ],
    (3, 2, 1): [
        "enfant-f|La pince, tes mèches.",
        "maman|Nino pince, le foulard attend.",
        "narrateur|Sarah veut écarter le pois taché, trop vite.",
        "narrateur|Elle s'arrête, la pince ouverte.",
        "copain|Moi.",
        "narrateur|Nino pince, hors du tissu.",
        "narrateur|Plus de goutte sur les pois.",
        "enfant-f|Le grain, à la mèche.",
        "narrateur|Le grain de laine tremble au bout d'une mèche.",
        "narrateur|Le foulard rejoint le coin usé, net.",
        "papa|Ses cheveux ont leur place, à part.",
        "maman|Le tapis redevient un rail.",
    ],
    (3, 2, 2): [
        "enfant-f|La serviette, tes cheveux.",
        "maman|Nino frotte, Sarah tient un pois.",
        "narrateur|Sarah veut essuyer le foulard, trop vite.",
        "narrateur|Elle le lève, hors des mèches.",
        "enfant-f|Toi d'abord.",
        "narrateur|Nino essuie, puis hoche la tête.",
        "copain|Sec.",
        "enfant-f|Le grain, au coin.",
        "narrateur|Le grain de laine sèche au coin du tapis usé.",
        "narrateur|Le cheval suit le pois jusqu'au coin.",
        "papa|L'eau est restée dans la serviette.",
        "maman|Le tapis a sa gare, un peu rêche.",
    ],
    (3, 2, 3): [
        "enfant-f|Moi le cheval, toi les pois.",
        "copain|Je tends le foulard.",
        "narrateur|Sarah tient le cheval hors des gouttes.",
        "narrateur|Elle attend que le tissu soit plat.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino ouvre le foulard, à son pas.",
        "narrateur|Le coin usé arrive sous un pois.",
        "enfant-f|Le grain, sur le dos.",
        "narrateur|Le grain de laine tient sur le dos du cheval.",
        "papa|Chacun a tenu sa part.",
        "maman|Le rail a tenu, malgré les mèches.",
        "copain|Gare.",
    ],
    (3, 3, 1): [
        "enfant-f|Tes manches, Nino.",
        "copain|Je les remonte.",
        "narrateur|Sarah veut libérer le pois, trop vite.",
        "narrateur|Elle lâche le tissu, puis attend.",
        "enfant-f|Toi, tes manches.",
        "narrateur|Nino retrousse, le foulard se dénoue.",
        "narrateur|Le rideau lâche le pois.",
        "enfant-f|Le grain, à la vitre.",
        "narrateur|Le grain de laine luit contre la vitre mouillée.",
        "narrateur|Le cheval suit le pois jusqu'au rebord.",
        "papa|Le gilet reste long, le rail passe.",
        "maman|La fenêtre a sa gare, étroite.",
    ],
    (3, 3, 2): [
        "enfant-f|Je tiens la boîte, toi le foulard.",
        "copain|J'écarte le rideau.",
        "narrateur|Sarah tient trop près, d'abord.",
        "narrateur|Elle recule, pour ses manches.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Nino écarte, trop lent, puis ça cède.",
        "narrateur|Le rebord reparaît sous un pois.",
        "enfant-f|Le grain, dans la boîte.",
        "narrateur|Le grain de laine voyage dans la boîte, au fond.",
        "papa|Tu as tenu sans tirer le gilet.",
        "maman|Le cheval entre, contre la vitre.",
        "copain|Pois.",
    ],
    (3, 3, 3): [
        "enfant-f|Noue, maman, ses poignets.",
        "maman|Un nœud souple, pour Nino.",
        "narrateur|Sarah veut tout finir, trop vite.",
        "narrateur|Elle pose le foulard, puis attend.",
        "enfant-f|À lui, le nœud.",
        "narrateur|Maman noue, Nino souffle.",
        "narrateur|Les manches tiennent, un pois se libère.",
        "copain|Libre.",
        "enfant-f|Le grain, au poignet.",
        "narrateur|Le grain de laine s'endort au poignet de Nino.",
        "papa|Le rebord vous attendait.",
        "maman|Le train arrive, le pois en tête.",
    ],
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le cheval tient au dossier, enfin.",
        "enfant-f|Ta gare, Nino.",
        "copain|Je vois le bois.",
        "narrateur|Ça a failli glisser, trop vite.",
        "papa|Vous avez attendu ses verres.",
        "maman|Le cacao fume, près de la lampe.",
        "enfant-f|On reste un peu.",
        "narrateur|Le grain de laine sèche au bord du torchon.",
    ],
    (1, 1, 2): [
        "narrateur|Deux paumes gardent le dos du cheval.",
        "enfant-f|Tes mains, ma voix.",
        "copain|Il est chaud, maintenant.",
        "narrateur|Un instant, le dossier partait.",
        "papa|Tu as parlé, sans lui prendre les verres.",
        "maman|Le canapé sent le radiateur, tiède.",
        "enfant-f|On reste.",
        "narrateur|Le grain de laine tient entre deux paumes.",
    ],
    (1, 1, 3): [
        "narrateur|Au pied du canapé, le bois se pose.",
        "enfant-f|Plus net, ici.",
        "copain|Mes lunettes.",
        "narrateur|La buée a failli tout cacher.",
        "papa|Un pas a suffi, hors du souffle.",
        "maman|Le parquet est plus frais, sous vos pieds.",
        "enfant-f|Sa gare, en bas.",
        "narrateur|Le grain de laine reste au pied du canapé.",
    ],
    (1, 2, 1): [
        "narrateur|Au coin usé, le cheval s'arrête.",
        "enfant-f|Tes mèches, plus haut.",
        "copain|Plus de goutte.",
        "narrateur|Le faux rail a failli les perdre.",
        "papa|La pince a gardé sa place, à part.",
        "maman|Le tapis redevient sec, sous le bois.",
        "enfant-f|On s'assoit, un peu.",
        "narrateur|Le grain de laine penche sous la pince.",
    ],
    (1, 2, 2): [
        "narrateur|La serviette garde une mèche, plus légère.",
        "enfant-f|Tu as frotté, toi.",
        "copain|Le tapis est sec.",
        "narrateur|Une goutte a failli tout détourner.",
        "papa|L'eau des cheveux n'est plus sur le bois.",
        "maman|Ça sent la pluie, derrière la vitre.",
        "enfant-f|Le coin usé, c'est sa gare.",
        "narrateur|Le grain de laine s'endort dans la serviette.",
    ],
    (1, 2, 3): [
        "narrateur|Sarah tient le cheval, Nino la boîte.",
        "enfant-f|Toi le carton, moi le bois.",
        "copain|J'y suis.",
        "narrateur|Les gouttes tombaient trop près, d'abord.",
        "papa|Vous avez partagé, sans vous presser.",
        "maman|Le coin usé brille, un peu rêche.",
        "enfant-f|On reste là.",
        "narrateur|Le grain de laine luit contre le bois du cheval.",
    ],
    (1, 3, 1): [
        "narrateur|Au rebord, le cheval regarde la pluie.",
        "enfant-f|Tes manches, libres.",
        "copain|Le gilet est long.",
        "narrateur|Le rideau a failli tout cacher.",
        "papa|Tu as laissé Nino retrousser.",
        "maman|La vitre tremble, un peu.",
        "enfant-f|Sa gare, contre le jour.",
        "narrateur|Le grain de laine voyage au bord d'une manche.",
    ],
    (1, 3, 2): [
        "narrateur|Sarah tient la boîte, le rebord est là.",
        "enfant-f|Tu as ouvert le rideau.",
        "copain|La vitre.",
        "narrateur|Tirer trop fort a failli tout perdre.",
        "papa|Tu as reculé, pour lui laisser l'air.",
        "maman|Le cheval touche le bois du rebord.",
        "enfant-f|On regarde dehors, un peu.",
        "narrateur|Le grain de laine tient au coin de la boîte.",
    ],
    (1, 3, 3): [
        "narrateur|Un nœud souple tient les poignets de Nino.",
        "enfant-f|Tes manches, tes mains.",
        "copain|Je peux pousser.",
        "narrateur|Le pli du rideau a failli tout prendre.",
        "papa|Le nœud est à sa taille, pas à la tienne.",
        "maman|Le rebord sent la pluie, tout près.",
        "enfant-f|Le train est arrivé.",
        "narrateur|Le grain de laine dort près du nœud.",
    ],
    (2, 1, 1): [
        "narrateur|La boîte tient au dossier, le cheval dedans.",
        "enfant-f|Tes verres, nets.",
        "copain|Je vois le carton.",
        "narrateur|La buée a failli viser à côté.",
        "papa|Il a essuyé, à sa façon.",
        "maman|Le cacao fume, derrière vous.",
        "enfant-f|On reste au canapé.",
        "narrateur|Le grain de laine brille sur le verre essuyé.",
    ],
    (2, 1, 2): [
        "narrateur|La paume de Nino garde un coin de carton.",
        "enfant-f|Tes mains, le bord.",
        "copain|C'est bon.",
        "narrateur|Pousser à sa place a failli tout rater.",
        "papa|Tu as parlé, sans pousser.",
        "maman|Le coussin est tiède, sous la boîte.",
        "enfant-f|Sa gare, ici.",
        "narrateur|Le grain de laine glisse dans la paume de Nino.",
    ],
    (2, 1, 3): [
        "narrateur|Sur le parquet, la boîte se pose, nette.",
        "enfant-f|Plus clair, en bas.",
        "copain|Le parquet.",
        "narrateur|Le souffle du radiateur a failli tout voiler.",
        "papa|Un pas a changé l'air.",
        "maman|Vos pieds sont plus frais, hors du canapé.",
        "enfant-f|Le cheval entre.",
        "narrateur|Le grain de laine attend sur le parquet froid.",
    ],
    (2, 2, 1): [
        "narrateur|Au coin usé, la boîte sèche, ouverte.",
        "enfant-f|Tes mèches, à part.",
        "copain|Plus de toc.",
        "narrateur|Une goutte a failli noyer le carton.",
        "papa|La pince a gardé l'eau dehors.",
        "maman|Le tapis a un fil, rien de plus.",
        "enfant-f|On s'assoit près du coin.",
        "narrateur|Le grain de laine s'accroche à la pince, beige.",
    ],
    (2, 2, 2): [
        "narrateur|La serviette porte un fil, plus clair.",
        "enfant-f|Tu as essuyé, toi.",
        "copain|Sec.",
        "narrateur|Frotter trop fort a failli tordre le carton.",
        "papa|L'eau est restée dans le tissu.",
        "maman|Le tapis redevient un quai, rêche.",
        "enfant-f|Le cheval entre, au coin.",
        "narrateur|Le grain de laine laisse un fil sur la serviette.",
    ],
    (2, 2, 3): [
        "narrateur|Nino pousse, Sarah tient le cheval.",
        "enfant-f|Toi le carton, moi le bois.",
        "copain|Gare.",
        "narrateur|Les rôles inversés ont failli tout mêler.",
        "papa|Vous avez attendu le pas de l'autre.",
        "maman|Le coin usé sent la laine, un peu.",
        "enfant-f|On reste.",
        "narrateur|Le grain de laine veille au fond de la boîte.",
    ],
    (2, 3, 1): [
        "narrateur|La boîte gagne le rebord, étroite.",
        "enfant-f|Tes manches, à toi.",
        "copain|Le carton passe.",
        "narrateur|Tirer le gilet a failli tout coincer.",
        "papa|Tu as laissé ses mains faire.",
        "maman|La vitre tremble, tout près du carton.",
        "enfant-f|Sa gare, contre le jour.",
        "narrateur|Le grain de laine suit la manche retroussée.",
    ],
    (2, 3, 2): [
        "narrateur|Sarah desserre, le rebord reparaît.",
        "enfant-f|Tu as ouvert, lentement.",
        "copain|On y est.",
        "narrateur|Serrer trop a failli cacher la vitre.",
        "papa|Tu as desserré, pour qu'il voie.",
        "maman|Le cheval entre, contre le bois.",
        "enfant-f|On regarde la pluie.",
        "narrateur|Le grain de laine penche au rebord de carton.",
    ],
    (2, 3, 3): [
        "narrateur|Le nœud souple laisse les mains libres.",
        "enfant-f|Tes poignets, tes manches.",
        "copain|Mes mains sont libres.",
        "narrateur|Le pli a failli garder la boîte.",
        "papa|Le nœud est à lui, pas à toi.",
        "maman|Le rebord sent le froid, dehors.",
        "enfant-f|Le train est là.",
        "narrateur|Le grain de laine se cache sous le nœud souple.",
    ],
    (3, 1, 1): [
        "narrateur|Un pois touche le dossier, le cheval dessus.",
        "enfant-f|Tes verres, le rail.",
        "copain|Un rond, puis l'autre.",
        "narrateur|Tirer le pois a failli tout plier.",
        "papa|Il a essuyé, puis suivi.",
        "maman|Le canapé garde le tissu, tiède.",
        "enfant-f|On s'allonge un peu.",
        "narrateur|Le grain de laine s'accroche à un pois du foulard.",
    ],
    (3, 1, 2): [
        "narrateur|Les pois passent d'une main à l'autre.",
        "enfant-f|Tes mains, le chemin.",
        "copain|Pois.",
        "narrateur|Poser ses verres a failli tout arrêter.",
        "papa|Tu as dit le chemin, sans prendre.",
        "maman|Le foulard sent le tiroir, un peu.",
        "enfant-f|Sa gare, au dossier.",
        "narrateur|Le grain de laine voyage d'une main à l'autre.",
    ],
    (3, 1, 3): [
        "narrateur|Au parquet, un pois s'ouvre, plat.",
        "enfant-f|Plus net, en bas.",
        "copain|Le pois.",
        "narrateur|Emporter le foulard trop vite a failli tout tordre.",
        "papa|Tu l'as laissé un instant, puis descendu.",
        "maman|Vos pieds quittent la buée, enfin.",
        "enfant-f|Le cheval trouve le pois.",
        "narrateur|Le grain de laine reste dans le pli du coussin.",
    ],
    (3, 2, 1): [
        "narrateur|Le foulard rejoint le coin usé, net.",
        "enfant-f|Tes mèches, hors des pois.",
        "copain|Moi.",
        "narrateur|Le pois taché a failli tout perdre.",
        "papa|La pince a gardé l'eau à part.",
        "maman|Le tapis redevient un rail, rêche.",
        "enfant-f|On s'assoit sur un pois.",
        "narrateur|Le grain de laine tremble au bout d'une mèche.",
    ],
    (3, 2, 2): [
        "narrateur|La serviette et le coin usé se touchent.",
        "enfant-f|Tu as frotté, le pois est sec.",
        "copain|Sec.",
        "narrateur|Essuyer le foulard trop vite a failli tout tacher.",
        "papa|Tu as levé le tissu, lui a frotté.",
        "maman|Le tapis a sa gare, un peu rêche.",
        "enfant-f|Le cheval suit le pois.",
        "narrateur|Le grain de laine sèche au coin du tapis usé.",
    ],
    (3, 2, 3): [
        "narrateur|Nino tend le foulard, Sarah le cheval.",
        "enfant-f|Toi les pois, moi le bois.",
        "copain|Gare.",
        "narrateur|Poser trop tôt a failli tout mouiller.",
        "papa|Tu as attendu le tissu plat.",
        "maman|Le coin usé brille sous un pois.",
        "enfant-f|On reste.",
        "narrateur|Le grain de laine tient sur le dos du cheval.",
    ],
    (3, 3, 1): [
        "narrateur|Un pois touche le rebord, le cheval dessus.",
        "enfant-f|Tes manches, le rail passe.",
        "copain|Je les remonte.",
        "narrateur|Libérer trop vite a failli tout enrouler.",
        "papa|Tu as lâché, lui a retroussé.",
        "maman|La vitre est étroite, et ça tient.",
        "enfant-f|Sa gare, contre le jour.",
        "narrateur|Le grain de laine luit contre la vitre mouillée.",
    ],
    (3, 3, 2): [
        "narrateur|La boîte et le foulard se rejoignent au rebord.",
        "enfant-f|Tu as écarté, lentement.",
        "copain|Pois.",
        "narrateur|Tenir trop près a failli coincer les manches.",
        "papa|Tu as reculé, pour son gilet.",
        "maman|Le cheval entre, un pois en tête.",
        "enfant-f|On regarde la pluie.",
        "narrateur|Le grain de laine voyage dans la boîte, au fond.",
    ],
    (3, 3, 3): [
        "narrateur|Le nœud libère un pois, puis le cheval.",
        "enfant-f|Tes poignets, le rail.",
        "copain|Libre.",
        "narrateur|Tout finir trop vite a failli tout nouer de travers.",
        "papa|Tu as posé le foulard, puis attendu.",
        "maman|Le rebord tient, presque trop tard.",
        "enfant-f|Le train est arrivé.",
        "narrateur|Le grain de laine s'endort au poignet de Nino.",
    ],
}

T3_SONS = {
    (1, 1): "torchon,verre",
    (1, 2): "mains,bois",
    (1, 3): "pas,parquet",
    (2, 1): "pince,cheveux",
    (2, 2): "serviette,tissu",
    (2, 3): "bois,carton",
    (3, 1): "manche,tissu",
    (3, 2): "carton,rideau",
    (3, 3): "noeud,tissu",
}

END_SONS = {1: "bois,lampe", 2: "carton,lampe", 3: "tissu,lampe"}
T3_EMPH = {
    1: {1: "torchon", 2: "mains", 3: "pas"},
    2: {1: "pince", 2: "serviette", 3: "cheval"},
    3: {1: "manches", 2: "boîte", 3: "nœud"},
}

BAD = (
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "la première",
    "la deuxième",
    "la troisième",
    "bravo tu as",
    "bon travail",
    "pas rire",
    "aujourd'hui,",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "tout doux",
    "tout calme",
    "tout lent",
    "merle",
    "miel",
    "gouttes au bord",
    "marque fine",
    "ombre en forme",
    "ancre minuscule",
    "étoile brune",
    "fil pâle",
    "croissant d'eau",
    "virgule de farine",
    "bouton de nacre",
    "nœud de raphia",
    "pois ivoire",
    "grain de savon",
    "grain de vanille",
    "pastille de colle",
    "virgule de buée",
    "capuchon",
    "grain doré",
    "brin de safran",
    "anneau de liège",
    "clou à tête",
    "grain d'ambre",
    "goutte de cire",
    "anneau de zinc",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "anneau de pollen",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille d'étain",
    "vis verte",
    "cristal de sucre",
    "écaille de lichen",
    "grain de cire",
    "dent de fermeture",
    "écaille de nacre",
    "grain de paprika",
    "écaille de boue",
    "point de rouille",
    "grain de mica",
    "grain de cannelle",
    "grain d'ocre",
    "grain de feutre",
    "grain de sésame",
    "écaille de savon",
    "grain de suie",
    "grain de limon",
    "grain de quartz",
    "grain de sel",
    "grain de lessive",
    "grain de cerise",
    "rond d'huile",
    "écaille d'orange",
    "point d'écume",
    "grain de sève",
    "point de beurre",
    "grain de craie",
    "grain de pomme",
    "grain de bitume",
    "locomotive",
    "gare en carton",
    "poisson de papier",
    "grand-père",
    "maîtresse",
    "jardinier",
    "bibliothécaire",
    "gardienne",
    "lunettes, cheveux",
    "sami",
    "tom ",
    "léa",
    "jules",
)


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "pluie,radiateur,lampe",
        {"emphasis": "grain de laine"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {
            "fields": t3lab("le cheval de bois", "la boîte à chaussures", "le foulard à pois"),
            "pause_before": 200,
        },
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
            {"emphasis": "grain de laine"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {
                "fields": t3lab("le canapé", "le tapis", "la fenêtre"),
                "pause_before": 200,
            },
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
                    {"emphasis": "grain de laine"},
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
    for bad in BAD:
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "grain de laine" not in blob:
        raise SystemExit(f"{SID}: grain de laine absent")
    if re.search(r"\bsara\b", blob):
        raise SystemExit(f"{SID}: Sara (sans h)")
    if re.search(r"\b(encore|déjà|deja)\b", blob):
        raise SystemExit(f"{SID}: tic encore/déjà")
    if "je ne fonce pas" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")

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
        if "grain de laine" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']} indice grain absent de la fin")
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
    if min(counts) < 550:
        raise SystemExit(f"chemin trop court: {min(counts)}")
    if max(counts) > 760:
        raise SystemExit(f"chemin trop long: {max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c["text_xai_tags"] == c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-060 — Le train de boîtes de Sarah\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.COR.003 — jouer avec Nino tel qu'il est "
        "(buée, mèches, gilet trop long), vécue, jamais dite\n"
        "- **Personnages :** Sarah, Nino, papa, maman\n"
        "- **Lieu :** salon après la pluie : canapé, tapis, fenêtre\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La lampe de papier pose un rond jaune. Un **grain de laine** tient dans la crinière "
        "du cheval de bois. Mission : un train de boîtes jusqu'à la fenêtre, avant que papa "
        "n'éteigne la lampe. Nino arrive du palier, verres voilés, cheveux qui gouttent, "
        "gilet trop long. Sarah propose ; il se tait (le silence est une réponse). "
        "Première idée : tirer trop vite. Le cheval n'atteint pas l'endroit promis. "
        "T1 = cheval / boîte / foulard (les trois partent). "
        "T2 = canapé (buée du radiateur), tapis (faux rail de gouttes), fenêtre (manches au rideau). "
        "Deuxième ruse plus maline. Sarah refuse de foncer. Elle retrouve le grain du début. "
        "T3 = torchon / mains / pas ; pince / serviette / tenir le cheval ; manches / tenir la boîte / nœud. "
        "On joue avec Nino tel qu'il arrive. Le grain paie le stop. Monde ≠ TREE-DIF-017 "
        "(pas locomotive, pas gare carton) ≠ TREE-DIF-049 (pas poissons papier).\n\n"
        "## Vécu\n\n"
        "Le sourire disparaît. L'envie et l'inquiétude se bousculent. Papa ou maman s'accroupit "
        "à la même hauteur. Personne ne donne la réponse. Sarah observe le cheval, écoute le salon, "
        "retrouve le grain de laine. Rythmes distincts : elle propose, il prend son temps. "
        "La leçon se voit : essuyer, pincer, retrousser, c'est lui ; attendre, c'est elle.\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien F-NAR-016 / xai « On va apprendre : Lunettes, cheveux, habit » jeté. Tout réécrit.\n"
        "- Ouverture inventée (lampe, rond jaune, grain). Pas de gabarit v2.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Indice unique : grain de laine (inventé, payé au climax). Liste d'indices usés évitée.\n"
        "- Corps, 2e ruse, refuse de foncer, 27 fins, 27 dernières images.\n"
        "- Merci vécu (papa : tu as rattrapé le cheval). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes`. "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply. Pas audio. Pas git.\n\n"
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
