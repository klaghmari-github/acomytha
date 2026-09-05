#!/usr/bin/env python3
"""TREE-DIF-023 — La marelle de Sarah et Nino (F-NAR-019, N3, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-023"
N3 = 16
TITLE = "La marelle de Sarah et Nino"
FIL = (
    "Au couloir aux étoiles, Sarah veut finir la marelle avec Nino "
    "avant que les chaussures mangent le trait de craie. "
    "Elle veut tout d'un coup. Nino ne dit rien : le silence répond. "
    "T1 = craie bleue / galet plat / ruban rouge ; les trois restent. "
    "T2 = classe (tapis), cour (bitume), préau (écho). "
    "T3 = neuf façons de doser l'élan. Le trait de craie paie le début."
)
CHARS = "Sarah, Nino, papa, maman"
SETTING = "école : classe, cour, préau"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "trait de craie",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=sarah_veut_tout_finir_nino_prend_son_temps; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_où_reste_l_objet; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "Nino",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=sarah_propose_nino_prend_son_temps; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=tout_finir_d_un_coup_ne_tient_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_silence_de_nino_est_une_réponse; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "trait de craie",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=doser_l_élan_une_case_après_l_autre; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "trait de craie",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_trait_de_craie_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Un banc du couloir grince, et se tait.",
    "narrateur|Les manteaux trop longs frôlent les crochets.",
    "narrateur|Des étoiles de papier collent aux vitres de la classe.",
    "narrateur|Elles jettent des carrés bleus sur le carrelage.",
    "papa|Ton lacet a glissé, Sarah.",
    "narrateur|Papa noue le nœud, près du banc.",
    "enfant-f|Il tient, papa.",
    "narrateur|Un trait de craie coupe une dalle, mince.",
    "narrateur|Il barre un carré bleu, sans bruit.",
    "enfant-f|C'est le départ, maman.",
    "maman|Le trait de craie, sur le carrelage ?",
    "enfant-f|La marelle commence là.",
    "narrateur|Nino arrive au bout du couloir.",
    "narrateur|En ce moment, Sarah serre la craie bleue.",
    "enfant-f|Nino, on finit tout, vite !",
    "narrateur|Nino ne dit rien.",
    "narrateur|Ce silence tient, comme une réponse.",
    "narrateur|Le sourire de Sarah disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|Je m'accroupis, à ta hauteur.",
    "papa|Merci, tu as vu le trait.",
    "maman|Tu lui proposes comment, Sarah ?",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près du banc.",
    "narrateur|La craie bleue, le galet plat, le ruban rouge.",
    "narrateur|Les trois resteront avec eux.",
    "maman|Tu prends quoi, d'abord ?",
]

T1 = {
    1: {
        "lab": "la craie bleue",
        "sons": "craie,poche",
        "emphasis": "craie bleue",
        "passage": [
            "narrateur|Sarah prend d'abord la craie bleue.",
            "enfant-f|Elle laisse un trait de craie sur ma paume.",
            "maman|Glisse-la dans ta poche.",
            "narrateur|Papa pose le galet plat dans la boîte.",
            "narrateur|Maman noue le ruban rouge au poignet.",
            "narrateur|Les trois affaires restent avec eux.",
            "enfant-f|Nino, on finit tout, d'un coup !",
            "narrateur|Nino s'arrête au bout du couloir.",
            "narrateur|Il ne dit rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|Sarah trace trop vite, sur sa paume.",
            "narrateur|Le trait de craie tremble, trop mince.",
            "papa|Je m'accroupis, à ta hauteur.",
            "enfant-f|Oui, papa.",
        ],
        "question": [
            "narrateur|Sarah a glissé la craie bleue dans la poche.",
            "maman|Elle est où, la craie ?",
        ],
        "qfields": {
            "expected_answer": "poche",
            "accepted_examples": "poche | la poche | dans la poche | sa poche",
            "retry_prompt": "La craie est dans la poche. Elle est où ?",
        },
        "confirm": [
            "narrateur|La poche porte la craie, contre le tissu.",
            "copain|Elle est trop bleue.",
            "enfant-f|C'est pour nos cases.",
            "narrateur|Nino a les genoux plus bas que Sarah.",
            "narrateur|Ses pieds n'arrêtent pas de bouger.",
            "narrateur|Sarah propose, et Nino prend son temps.",
            "maman|Il a beaucoup d'élan, ce n'est rien.",
            "papa|On reste à l'école ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un trait de craie tient au carrelage.",
        ],
    },
    2: {
        "lab": "le galet plat",
        "sons": "galet,boite",
        "emphasis": "galet plat",
        "passage": [
            "narrateur|Sarah prend d'abord le galet plat.",
            "enfant-f|Il est tiède, un peu rugueux.",
            "papa|Pose-le dans la boîte.",
            "narrateur|La pierre fait un petit toc contre le bois.",
            "maman|La craie bleue, ensuite, dans la poche.",
            "narrateur|Elle glisse le ruban rouge au poignet.",
            "narrateur|Les trois affaires restent avec eux.",
            "enfant-f|On lance jusqu'à huit, Nino !",
            "narrateur|Nino serre le galet, sans le lancer.",
            "narrateur|Il ne dit rien.",
            "narrateur|Le sourire de Sarah disparaît.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie tient au carrelage, derrière eux.",
        ],
        "question": [
            "narrateur|Le galet plat reste dans la boîte.",
            "maman|Il est où, le galet ?",
        ],
        "qfields": {
            "expected_answer": "boîte",
            "accepted_examples": "boîte | boite | la boîte | dans la boîte | la boite",
            "retry_prompt": "Le galet est dans la boîte. Il est où ?",
        },
        "confirm": [
            "narrateur|La boîte veille près du galet plat.",
            "copain|Je vois la pierre.",
            "enfant-f|Ne la lance pas.",
            "narrateur|Nino penche pour voir le galet.",
            "narrateur|Sa mèche touche presque le couvercle.",
            "papa|Ça sent la craie, dans le couloir.",
            "maman|Vos mains, au-dessus de la boîte ?",
            "copain|Oui.",
            "enfant-f|On y va, Nino ?",
            "narrateur|Un trait de craie tient au carrelage.",
        ],
    },
    3: {
        "lab": "le ruban rouge",
        "sons": "ruban,tissu",
        "emphasis": "ruban rouge",
        "passage": [
            "narrateur|Sarah passe le ruban rouge autour du poignet.",
            "enfant-f|C'est la ligne de départ.",
            "maman|Serre-le, comme un secret.",
            "papa|La craie et le galet, avec vous.",
            "narrateur|Il les pose près de la boîte.",
            "narrateur|Les trois affaires restent avec eux.",
            "enfant-f|Nino, saute tout, vite !",
            "narrateur|Nino touche le ruban, sans sauter.",
            "narrateur|Il ne dit rien.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie barre la dalle, derrière le ruban.",
        ],
        "question": [
            "narrateur|Le ruban rouge reste au poignet.",
            "maman|Il est où, le ruban ?",
        ],
        "qfields": {
            "expected_answer": "poignet",
            "accepted_examples": "poignet | au poignet | le poignet | son poignet",
            "retry_prompt": "Le ruban est au poignet. Il est où ?",
        },
        "confirm": [
            "narrateur|Le ruban rouge cache le pouls.",
            "copain|Ça sent le savon.",
            "enfant-f|La ligne de départ est là.",
            "narrateur|Le manteau de Nino s'arrête trop haut.",
            "narrateur|Les manches laissent ses poignets libres.",
            "maman|L'école est tiède, devant.",
            "papa|On y va, tous les quatre ?",
            "enfant-f|Oui.",
            "narrateur|Nino touche le ruban, sans parler.",
            "narrateur|Un trait de craie barre la dalle.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|La craie bleue attend, dans la poche.",
        "narrateur|Nino tapote le sol, léger.",
        "narrateur|La classe, la cour, ou le préau.",
        "papa|On commence où, pour la marelle ?",
    ],
    2: [
        "narrateur|Le galet plat veille dans la boîte.",
        "narrateur|Nino tapote le sol, léger.",
        "maman|La classe, la cour, ou le préau ?",
        "papa|On commence où, Sarah ?",
    ],
    3: [
        "narrateur|Le ruban rouge reste au poignet.",
        "narrateur|Nino tapote le sol, léger.",
        "narrateur|La classe, la cour, ou le préau.",
        "maman|On commence où, Sarah ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "craie,tapis",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Sarah trace une case sur le grand papier.",
            "enfant-f|On fait toutes les cases, Nino, d'un coup.",
            "copain|Moi je saute, Sarah.",
            "narrateur|Nino saute entre les tables, trop vite.",
            "narrateur|Une boîte de crayons cliquette, trop haut.",
            "narrateur|Le trait bleu tremble, puis s'élargit.",
            "enfant-f|La craie n'attendait pas ça.",
            "narrateur|Le tapis de laine avale le bleu, plus rusé.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
        ],
    },
    (2, 1): {
        "sons": "galet,chaise",
        "emphasis": "chaise",
        "passage": [
            "narrateur|Sarah pose le galet sur une case dessinée.",
            "enfant-f|On le lance jusqu'au bout, d'un coup.",
            "copain|Moi je le jette sous la chaise.",
            "narrateur|Deux envies, au même moment.",
            "narrateur|Le galet glisse, roule sous une chaise.",
            "narrateur|Nino ne dit plus rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|La chaise recule, plus rusée, et cache la pierre.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Sarah disparaît.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie attend au bord du tapis.",
        ],
    },
    (3, 1): {
        "sons": "ruban,chaise",
        "emphasis": "ruban",
        "passage": [
            "narrateur|Sarah noue le ruban à la jambe d'une chaise.",
            "enfant-f|C'est le départ, on saute tout.",
            "copain|Moi je tire, Sarah.",
            "narrateur|La chaise recule, le ruban se défait.",
            "narrateur|Nino s'arrête, la main sur le tissu.",
            "narrateur|Il ne dit rien.",
            "narrateur|Le ruban s'accroche à un pied de table, plus rusé.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie barre le papier, trop pâle.",
        ],
    },
    (1, 2): {
        "sons": "craie,bitume",
        "emphasis": "bitume",
        "passage": [
            "narrateur|Sarah dessine une case sur le bitume chaud.",
            "enfant-f|La cour est à nous, Nino.",
            "copain|Je vais jusqu'au bout, trop vite !",
            "narrateur|Ses chaussures prennent le bleu frais.",
            "narrateur|Sarah veut retracer les huit cases, d'un coup.",
            "narrateur|La poussière lève, plus rusée, et mange le trait.",
            "enfant-f|On n'arrive pas, comme ça.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie tient près de la grille.",
        ],
    },
    (2, 2): {
        "sons": "galet,grille",
        "emphasis": "grille",
        "passage": [
            "narrateur|Sarah lance le galet vers la case huit.",
            "enfant-f|Tout d'un coup, jusqu'au bout.",
            "copain|Moi je le fais voler.",
            "narrateur|Le galet file trop loin, vers le grillage.",
            "narrateur|Nino court, puis s'arrête.",
            "narrateur|Il ne dit rien.",
            "narrateur|La pierre se loge dans une fente, plus rusée.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Sarah disparaît.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie attend sur la case un.",
        ],
    },
    (3, 2): {
        "sons": "ruban,vent",
        "emphasis": "ruban",
        "passage": [
            "narrateur|Sarah pose le ruban, pile sur la ligne.",
            "enfant-f|On saute tout, Nino.",
            "copain|Moi je passe par-dessus.",
            "narrateur|Nino saute par-dessus le ruban, sans s'arrêter.",
            "narrateur|Sarah veut le rattraper, trop vite.",
            "narrateur|Le vent lève le tissu, plus rusé, vers la grille.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Ce silence de Nino tient, net.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie barre la ligne de départ.",
        ],
    },
    (1, 3): {
        "sons": "craie,echo",
        "emphasis": "écho",
        "passage": [
            "narrateur|Sarah trace une case pâle sous le préau.",
            "enfant-f|Ici, ça résonne, Nino.",
            "copain|J'entends mes pieds deux fois !",
            "narrateur|Les sauts de Nino effacent le trait pâle.",
            "narrateur|Sarah retrace trop vite, pour tout finir.",
            "narrateur|L'écho montre deux traits, plus rusé, et elle se trompe.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie tient au pied du pilier.",
        ],
    },
    (2, 3): {
        "sons": "galet,echo",
        "emphasis": "écho",
        "passage": [
            "narrateur|Le galet claque, et l'écho répond.",
            "enfant-f|On fait toutes les cases, d'un coup.",
            "copain|J'entends la pierre deux fois !",
            "narrateur|Nino court après le bruit, plus loin.",
            "narrateur|Sarah veut compter vite, pour tout finir.",
            "narrateur|L'écho couvre les chiffres, plus rusé.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie attend sous le toit.",
        ],
    },
    (3, 3): {
        "sons": "ruban,echo",
        "emphasis": "écho",
        "passage": [
            "narrateur|Le ruban flotte un peu, sous le toit.",
            "enfant-f|On saute tout le chemin, Nino.",
            "copain|Je chasse le tissu !",
            "narrateur|Nino chasse le ruban, l'écho le suit.",
            "narrateur|Sarah tire trop vite, pour tout nouer.",
            "narrateur|Le ruban s'enroule à un pilier, plus rusé.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Tu proposes comment, Sarah ?",
            "narrateur|Un trait de craie barre le béton, mince.",
        ],
    },
}

T3_LABS = {
    1: ("jouer sur le tapis", "attendre le coussin", "compter avec maman"),
    2: ("sauter ensemble", "attendre la case", "le galet de papa"),
    3: ("le train de sauts", "attendre l'écho", "le rythme de maman"),
}

T3_CHOICE = {
    1: [
        "narrateur|Nino saute entre les tables.",
        "narrateur|Personne ne donne la réponse.",
        "papa|Le tapis, le coussin, ou compter avec maman ?",
    ],
    2: [
        "narrateur|Les cases de la cour attendent.",
        "maman|Sauter ensemble, attendre, ou le galet de papa ?",
        "narrateur|Personne ne donne la réponse.",
    ],
    3: [
        "narrateur|L'écho remplit le préau.",
        "papa|Le train, l'écho, ou le rythme de maman ?",
        "narrateur|Personne ne donne la réponse.",
    ],
}

T3_EMPH = {
    1: {1: "tapis", 2: "coussin", 3: "compter"},
    2: {1: "ensemble", 2: "case", 3: "galet de papa"},
    3: {1: "train de sauts", 2: "écho", 3: "rythme de maman"},
}

T3_SONS = {
    (1, 1): "tapis,laine",
    (1, 2): "coussin,souffle",
    (1, 3): "voix,chiffres",
    (2, 1): "pas,bitume",
    (2, 2): "case,attente",
    (2, 3): "galet,papa",
    (3, 1): "pas,train",
    (3, 2): "echo,beton",
    (3, 3): "mains,rythme",
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On joue sur le tapis.",
        "copain|Moi je tiens, toi tu dessines.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe la craie bleue.",
        "narrateur|Un trait de craie brille au bord du tapis.",
        "enfant-f|Le départ, là.",
        "narrateur|Nino tient la boîte, contre ses genoux.",
        "narrateur|Sarah trace une seule case, large.",
        "narrateur|Nino saute cette case, puis s'arrête.",
        "enfant-f|Maintenant c'est moi.",
        "copain|Après, c'est moi.",
        "papa|Une case, puis l'autre.",
        "maman|Le tapis vous a gardés.",
    ],
    (1, 1, 2): [
        "enfant-f|On attend un peu.",
        "copain|Je m'assois, alors.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute la classe, un instant.",
        "narrateur|Un trait de craie dort près du coussin.",
        "enfant-f|Le départ, dessous.",
        "narrateur|Nino pose les genoux sur le coussin.",
        "narrateur|La craie bleue attend près de lui.",
        "narrateur|Sa respiration redevient calme, plus basse.",
        "enfant-f|Tu es prêt ?",
        "copain|Je saute la case un.",
        "papa|Vous avez laissé l'élan s'asseoir.",
        "maman|Le coussin vous a tenus.",
    ],
    (1, 1, 3): [
        "enfant-f|Maman, tu comptes avec nous ?",
        "maman|Un, deux, trois.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle regarde le trait de craie, sur le papier.",
        "enfant-f|Le départ compte un.",
        "narrateur|Sarah lève la craie à chaque chiffre.",
        "narrateur|Nino saute seulement quand elle dit trois.",
        "copain|Je peux attendre le trois !",
        "enfant-f|Moi aussi, j'attends.",
        "narrateur|Les tables restent tranquilles, autour.",
        "papa|Vous avez demandé, et ça marche.",
        "maman|Mes chiffres ont tenu l'élan.",
    ],
    (1, 2, 1): [
        "enfant-f|On saute ensemble.",
        "copain|Toi derrière, moi devant !",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe la craie, au bitume.",
        "narrateur|Un trait de craie barre la case un.",
        "enfant-f|Le départ, entre nous.",
        "narrateur|Sarah garde la craie, Nino saute devant.",
        "narrateur|Deux ombres passent sur la même case.",
        "narrateur|Nino va plus vite, Sarah plus loin.",
        "copain|On arrive au même huit.",
        "papa|Chacun son pas, même case.",
        "maman|Le bitume vous a tenus.",
    ],
    (1, 2, 2): [
        "enfant-f|On attend la case.",
        "copain|Je ne lance plus.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute la cour, un instant.",
        "narrateur|Un trait de craie tient au centre de la case.",
        "enfant-f|Le départ, au milieu.",
        "narrateur|La craie marque le bord, et ils regardent.",
        "narrateur|Le bleu reste, sans poussière.",
        "copain|Je saute quand elle est nette.",
        "enfant-f|Moi après toi.",
        "maman|La case vous a attendus.",
        "papa|Le bleu a tenu, au centre.",
    ],
    (1, 2, 3): [
        "enfant-f|Papa, ton galet, s'il te plaît.",
        "papa|Le mien va moins vite.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle cherche le trait de craie.",
        "narrateur|Il brille près de la grille.",
        "enfant-f|Le départ, à côté.",
        "narrateur|Le galet de papa roule, case après case.",
        "narrateur|Sarah pose la craie où la pierre s'arrête.",
        "copain|Je saute là, pas plus loin.",
        "enfant-f|Moi la case d'après.",
        "maman|La pierre de papa a ralenti le jeu.",
        "papa|Vous avez suivi, tous les deux.",
    ],
    (1, 3, 1): [
        "enfant-f|Un train de sauts, un wagon après l'autre.",
        "copain|Moi le premier wagon.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe la craie, sous le toit.",
        "narrateur|Un trait de craie tient au pied du pilier.",
        "enfant-f|Le départ, au pilier.",
        "narrateur|Sarah trace un wagon, puis s'arrête.",
        "narrateur|Nino saute ce wagon, et attend.",
        "copain|Le mien est passé.",
        "enfant-f|Le mien suit, sans le rattraper.",
        "papa|Le train a pris son temps.",
        "maman|Le toit a gardé vos pas.",
    ],
    (1, 3, 2): [
        "enfant-f|On attend l'écho.",
        "copain|Je n'entends plus mes pieds.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute le préau, un instant.",
        "narrateur|Un trait de craie tient au pilier.",
        "enfant-f|Le départ, quand ça se tait.",
        "narrateur|Sarah pose la craie, et le toit répond.",
        "narrateur|Ils attendent que l'écho finisse.",
        "copain|Maintenant je saute.",
        "enfant-f|Moi après le silence.",
        "papa|L'écho vous a donné le temps.",
        "maman|Le préau s'est tu, juste assez.",
    ],
    (1, 3, 3): [
        "enfant-f|Maman, tu tapes le rythme ?",
        "maman|Une claque, un saut.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle regarde le trait de craie, au béton.",
        "enfant-f|Le départ, sur ta main.",
        "narrateur|Maman frappe dans ses mains, lentement.",
        "narrateur|Sarah lève la craie à chaque claque.",
        "narrateur|Nino saute seulement sur le bruit.",
        "copain|Je peux attendre la claque !",
        "enfant-f|Moi aussi.",
        "papa|Vos pieds ont suivi ses mains.",
        "maman|Le rythme a tenu l'élan.",
    ],
    (2, 1, 1): [
        "enfant-f|On joue sur le tapis.",
        "copain|Moi je tiens le galet.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe le galet plat.",
        "narrateur|Un trait de craie brille au bord du tapis.",
        "enfant-f|Le départ, autour de la pierre.",
        "narrateur|Nino pose le galet sur la laine du bord.",
        "narrateur|Sarah trace une case autour, large.",
        "narrateur|Nino saute cette case, puis s'arrête.",
        "enfant-f|Maintenant c'est moi.",
        "copain|Après, c'est moi.",
        "papa|Une case, puis l'autre.",
        "maman|Le tapis vous a gardés.",
    ],
    (2, 1, 2): [
        "enfant-f|On attend un peu.",
        "copain|Je m'assois, avec la pierre.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute la classe, un instant.",
        "narrateur|Un trait de craie dort près du coussin.",
        "enfant-f|Le départ, dessous.",
        "narrateur|Nino pose le galet sur le coussin.",
        "narrateur|La pierre ne roule plus.",
        "narrateur|Sa respiration redevient calme, plus basse.",
        "enfant-f|Tu es prêt ?",
        "copain|Je saute la case un.",
        "papa|Vous avez laissé l'élan s'asseoir.",
        "maman|Le coussin a tenu la pierre.",
    ],
    (2, 1, 3): [
        "enfant-f|Maman, tu comptes avec nous ?",
        "maman|Un, deux, trois.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle regarde le trait de craie, sur le papier.",
        "enfant-f|Le départ compte un.",
        "narrateur|Sarah lève le galet à chaque chiffre.",
        "narrateur|Nino saute seulement quand elle dit trois.",
        "copain|Je peux attendre le trois !",
        "enfant-f|Moi aussi, j'attends.",
        "narrateur|Les tables restent tranquilles, autour.",
        "papa|Vous avez demandé, et ça marche.",
        "maman|Mes chiffres ont tenu l'élan.",
    ],
    (2, 2, 1): [
        "enfant-f|On saute ensemble.",
        "copain|Toi derrière, moi devant !",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe le galet, au bitume.",
        "narrateur|Un trait de craie barre la case un.",
        "enfant-f|Le départ, entre nous.",
        "narrateur|Sarah garde le galet, Nino saute devant.",
        "narrateur|Deux ombres passent sur la même case.",
        "narrateur|Nino va plus vite, Sarah plus loin.",
        "copain|On arrive au même huit.",
        "papa|Chacun son pas, même case.",
        "maman|Le bitume vous a tenus.",
    ],
    (2, 2, 2): [
        "enfant-f|On attend la case.",
        "copain|Je ne lance plus.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute la cour, un instant.",
        "narrateur|Un trait de craie tient au centre de la case.",
        "enfant-f|Le départ, au milieu.",
        "narrateur|Le galet reste, sans rouler.",
        "narrateur|La poussière retombe, autour.",
        "copain|Je saute quand il est calme.",
        "enfant-f|Moi après toi.",
        "maman|La case vous a attendus.",
        "papa|La pierre est restée au milieu.",
    ],
    (2, 2, 3): [
        "enfant-f|Papa, ton galet, s'il te plaît.",
        "papa|Le mien va moins vite.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle cherche le trait de craie.",
        "narrateur|Il brille près de la grille.",
        "enfant-f|Le départ, à côté.",
        "narrateur|Le galet de papa roule, case après case.",
        "narrateur|Sarah pose le leur où la pierre s'arrête.",
        "copain|Je saute là, pas plus loin.",
        "enfant-f|Moi la case d'après.",
        "maman|Deux pierres, le même chemin.",
        "papa|Vous avez suivi, tous les deux.",
    ],
    (2, 3, 1): [
        "enfant-f|Un train de sauts, un wagon après l'autre.",
        "copain|Moi le premier wagon.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe le galet, sous le toit.",
        "narrateur|Un trait de craie tient au pied du pilier.",
        "enfant-f|Le départ, au pilier.",
        "narrateur|Le galet claque une fois, un wagon.",
        "narrateur|Nino saute ce wagon, et attend.",
        "copain|Le mien est passé.",
        "enfant-f|Le mien suit, sans le rattraper.",
        "papa|Le train a pris son temps.",
        "maman|Le toit a gardé vos pas.",
    ],
    (2, 3, 2): [
        "enfant-f|On attend l'écho.",
        "copain|Je n'entends plus la pierre.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute le préau, un instant.",
        "narrateur|Un trait de craie tient au pilier.",
        "enfant-f|Le départ, quand ça se tait.",
        "narrateur|Sarah pose le galet, et le toit répond.",
        "narrateur|Ils attendent que l'écho finisse.",
        "copain|Maintenant je saute.",
        "enfant-f|Moi après le silence.",
        "papa|L'écho vous a donné le temps.",
        "maman|Le préau s'est tu, juste assez.",
    ],
    (2, 3, 3): [
        "enfant-f|Maman, tu tapes le rythme ?",
        "maman|Une claque, un saut.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle regarde le trait de craie, au béton.",
        "enfant-f|Le départ, sur ta main.",
        "narrateur|Maman frappe dans ses mains, lentement.",
        "narrateur|Sarah lève le galet à chaque claque.",
        "narrateur|Nino saute seulement sur le bruit.",
        "copain|Je peux attendre la claque !",
        "enfant-f|Moi aussi.",
        "papa|Vos pieds ont suivi ses mains.",
        "maman|Le rythme a tenu l'élan.",
    ],
    (3, 1, 1): [
        "enfant-f|On joue sur le tapis.",
        "copain|Moi je tiens le ruban.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe le ruban rouge.",
        "narrateur|Un trait de craie brille au bord du tapis.",
        "enfant-f|Le départ, sous le tissu.",
        "narrateur|Nino tend le ruban, comme une ligne.",
        "narrateur|Sarah trace une case derrière, large.",
        "narrateur|Nino saute cette case, puis s'arrête.",
        "enfant-f|Maintenant c'est moi.",
        "copain|Après, c'est moi.",
        "papa|Une case, puis l'autre.",
        "maman|Le tapis vous a gardés.",
    ],
    (3, 1, 2): [
        "enfant-f|On attend un peu.",
        "copain|Je m'assois, dans le ruban.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute la classe, un instant.",
        "narrateur|Un trait de craie dort près du coussin.",
        "enfant-f|Le départ, dessous.",
        "narrateur|Nino pose le ruban autour du coussin.",
        "narrateur|Il s'assoit au milieu, sans tirer.",
        "narrateur|Sa respiration redevient calme, plus basse.",
        "enfant-f|Tu es prêt ?",
        "copain|Je saute la case un.",
        "papa|Vous avez laissé l'élan s'asseoir.",
        "maman|Le coussin a tenu le tissu.",
    ],
    (3, 1, 3): [
        "enfant-f|Maman, tu comptes avec nous ?",
        "maman|Un, deux, trois.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle regarde le trait de craie, sur le papier.",
        "enfant-f|Le départ compte un.",
        "narrateur|Sarah lève le ruban à chaque chiffre.",
        "narrateur|Nino saute seulement quand elle dit trois.",
        "copain|Je peux attendre le trois !",
        "enfant-f|Moi aussi, j'attends.",
        "narrateur|Les tables restent tranquilles, autour.",
        "papa|Vous avez demandé, et ça marche.",
        "maman|Mes chiffres ont tenu l'élan.",
    ],
    (3, 2, 1): [
        "enfant-f|On saute ensemble.",
        "copain|Toi derrière, moi devant !",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe le ruban, au bitume.",
        "narrateur|Un trait de craie barre la case un.",
        "enfant-f|Le départ, entre nous.",
        "narrateur|Sarah garde le ruban, Nino saute devant.",
        "narrateur|Deux ombres passent sur la même case.",
        "narrateur|Nino va plus vite, Sarah plus loin.",
        "copain|On arrive au même huit.",
        "papa|Chacun son pas, même case.",
        "maman|Le bitume vous a tenus.",
    ],
    (3, 2, 2): [
        "enfant-f|On attend la case.",
        "copain|Je ne saute plus par-dessus.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute la cour, un instant.",
        "narrateur|Un trait de craie tient au centre de la case.",
        "enfant-f|Le départ, au milieu.",
        "narrateur|Le ruban reste sur la ligne, sans voler.",
        "narrateur|Le vent se tait, autour.",
        "copain|Je saute quand il est calme.",
        "enfant-f|Moi après toi.",
        "maman|La case vous a attendus.",
        "papa|La ligne est restée en place.",
    ],
    (3, 2, 3): [
        "enfant-f|Papa, ton galet, s'il te plaît.",
        "papa|Le mien va moins vite.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle cherche le trait de craie.",
        "narrateur|Il brille près de la grille.",
        "enfant-f|Le départ, à côté.",
        "narrateur|Le galet de papa roule, case après case.",
        "narrateur|Sarah pose le ruban où la pierre s'arrête.",
        "copain|Je saute là, pas plus loin.",
        "enfant-f|Moi la case d'après.",
        "maman|Le tissu a suivi la pierre.",
        "papa|Vous avez suivi, tous les deux.",
    ],
    (3, 3, 1): [
        "enfant-f|Un train de sauts, un wagon après l'autre.",
        "copain|Moi le premier wagon.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle observe le ruban, sous le toit.",
        "narrateur|Un trait de craie tient au pied du pilier.",
        "enfant-f|Le départ, au pilier.",
        "narrateur|Le ruban avance d'un wagon, puis s'arrête.",
        "narrateur|Nino saute ce wagon, et attend.",
        "copain|Le mien est passé.",
        "enfant-f|Le mien suit, sans le rattraper.",
        "papa|Le train a pris son temps.",
        "maman|Le toit a gardé vos pas.",
    ],
    (3, 3, 2): [
        "enfant-f|On attend l'écho.",
        "copain|Je n'entends plus le tissu.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle écoute le préau, un instant.",
        "narrateur|Un trait de craie tient au pilier.",
        "enfant-f|Le départ, quand ça se tait.",
        "narrateur|Sarah agite le ruban, et le toit répond.",
        "narrateur|Ils attendent que l'écho finisse.",
        "copain|Maintenant je saute.",
        "enfant-f|Moi après le silence.",
        "papa|L'écho vous a donné le temps.",
        "maman|Le préau s'est tu, juste assez.",
    ],
    (3, 3, 3): [
        "enfant-f|Maman, tu tapes le rythme ?",
        "maman|Une claque, un saut.",
        "narrateur|Sarah refuse de foncer.",
        "narrateur|Elle regarde le trait de craie, au béton.",
        "enfant-f|Le départ, sur ta main.",
        "narrateur|Maman frappe dans ses mains, lentement.",
        "narrateur|Sarah lève le ruban à chaque claque.",
        "narrateur|Nino saute seulement sur le bruit.",
        "copain|Je peux attendre la claque !",
        "enfant-f|Moi aussi.",
        "papa|Vos pieds ont suivi ses mains.",
        "maman|Le rythme a tenu l'élan.",
    ],
}

END_SONS = {1: "craie,couloir", 2: "galet,boite", 3: "ruban,tissu"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Ils s'assoient au bord du tapis.",
        "enfant-f|Une case, puis l'autre.",
        "copain|On a fini, sans tout sauter.",
        "papa|Vous avez pris le temps.",
        "maman|La craie a laissé du bleu à la laine.",
        "narrateur|Sarah glisse la craie dans la poche.",
        "narrateur|Un trait de craie tient au tapis, mince.",
        "enfant-f|C'est notre départ, Nino.",
        "narrateur|Les étoiles de papier jettent un dernier carré.",
        "narrateur|La craie bleue rentre dans la poche, un trait de craie tient au tapis.",
    ],
    (1, 1, 2): [
        "narrateur|Nino se lève du coussin, lentement.",
        "copain|J'ai attendu, Sarah.",
        "enfant-f|Moi aussi, près de toi.",
        "maman|Le bleu a séché, au bord.",
        "papa|Soufflez un peu, vos mains.",
        "narrateur|Sarah range la craie, contre le tissu.",
        "narrateur|Un trait de craie dort près du coussin.",
        "enfant-f|On le garde, Nino.",
        "narrateur|Le coussin garde un creux, un peu tiède.",
        "narrateur|Le coussin garde un trait de craie, pâle, au bord.",
    ],
    (1, 1, 3): [
        "narrateur|Maman baisse les mains.",
        "copain|Un, deux, trois, on a compté.",
        "enfant-f|Le trois nous a tenus.",
        "papa|Les tables n'ont plus bougé.",
        "maman|Le papier a gardé vos chiffres.",
        "narrateur|Sarah pose la craie sur le trois.",
        "narrateur|Un trait de craie reste sous le chiffre.",
        "enfant-f|C'est notre marelle, Nino.",
        "narrateur|Un peu de bleu tient sous le trois.",
        "narrateur|Sous le chiffre trois, un trait de craie reste sur le papier.",
    ],
    (1, 2, 1): [
        "narrateur|Ils s'arrêtent sur la case huit.",
        "enfant-f|Toi devant, moi derrière.",
        "copain|On est arrivés au même bout.",
        "papa|Chacun son pas, même arrivée.",
        "maman|Le bitume est tiède, sous vos semelles.",
        "narrateur|Sarah glisse la craie dans la poche.",
        "narrateur|Un trait de craie barre la case, au soleil.",
        "enfant-f|Regarde, Nino, il tient.",
        "narrateur|Deux ombres se touchent, puis se séparent.",
        "narrateur|Deux ombres s'arrêtent sur un trait de craie, au bitume.",
    ],
    (1, 2, 2): [
        "narrateur|La case est nette, au centre.",
        "copain|J'ai attendu qu'elle soit belle.",
        "enfant-f|Moi j'ai attendu tes pieds.",
        "maman|La poussière est retombée.",
        "papa|Lavez-vous un peu les mains.",
        "narrateur|Sarah pose la craie au milieu.",
        "narrateur|Un trait de craie tient, net, au centre.",
        "enfant-f|C'est notre case, Nino.",
        "narrateur|Le bleu ne bouge plus.",
        "narrateur|La case huit garde un trait de craie, net, au centre.",
    ],
    (1, 2, 3): [
        "narrateur|Le galet de papa s'arrête près de la grille.",
        "copain|On a suivi ta pierre.",
        "enfant-f|Case après case, pas plus loin.",
        "papa|La mienne va moins vite, oui.",
        "maman|Vos chaussures ont de la poussière.",
        "narrateur|Sarah pose la craie à côté du galet.",
        "narrateur|Un trait de craie brille près de la grille.",
        "enfant-f|Deux pierres, un chemin.",
        "narrateur|Le galet de papa garde un peu de bleu.",
        "narrateur|Le galet de papa repose près d'un trait de craie bleu.",
    ],
    (1, 3, 1): [
        "narrateur|Le train de sauts s'arrête sous le toit.",
        "copain|Mon wagon est passé.",
        "enfant-f|Le mien a suivi, sans le rattraper.",
        "papa|Le préau a pris son temps.",
        "maman|Le béton est frais, sous vos mains.",
        "narrateur|Sarah glisse la craie dans la poche.",
        "narrateur|Un trait de craie tient au pied du pilier.",
        "enfant-f|Le départ reste là, Nino.",
        "narrateur|Un dernier pas sonne, puis plus rien.",
        "narrateur|Le train de sauts laisse un trait de craie sous le toit.",
    ],
    (1, 3, 2): [
        "narrateur|L'écho s'est tu, sous le toit.",
        "copain|J'ai attendu le silence.",
        "enfant-f|Moi aussi, avant de sauter.",
        "maman|Le préau vous a laissés finir.",
        "papa|Le pilier est un peu bleu.",
        "narrateur|Sarah pose la craie au pied du pilier.",
        "narrateur|Un trait de craie tient au béton.",
        "enfant-f|Quand ça se tait, on saute.",
        "narrateur|Le toit ne répond plus.",
        "narrateur|L'écho s'est tu près d'un trait de craie, au pilier.",
    ],
    (1, 3, 3): [
        "narrateur|Maman baisse les mains, une dernière fois.",
        "copain|J'ai sauté sur ta claque.",
        "enfant-f|Moi aussi, pas avant.",
        "papa|Vos pieds ont appris ses mains.",
        "maman|Le rythme est resté au sol.",
        "narrateur|Sarah pose la craie où maman a frappé.",
        "narrateur|Un trait de craie tient au béton, mince.",
        "enfant-f|C'est notre rythme, Nino.",
        "narrateur|Les mains de maman sentent un peu le bleu.",
        "narrateur|Les mains de maman laissent un trait de craie au sol.",
    ],
    (2, 1, 1): [
        "narrateur|Ils s'assoient au bord du tapis.",
        "enfant-f|Une case autour de la pierre.",
        "copain|On a fini, sans tout sauter.",
        "papa|Vous avez pris le temps.",
        "maman|Le galet a laissé un creux à la laine.",
        "narrateur|Sarah range le galet dans la boîte.",
        "narrateur|Un trait de craie borde le tapis, mince.",
        "enfant-f|C'est notre départ, Nino.",
        "narrateur|Les étoiles de papier jettent un dernier carré.",
        "narrateur|Le galet plat rentre dans la boîte, un trait de craie borde le tapis.",
    ],
    (2, 1, 2): [
        "narrateur|Nino se lève du coussin, lentement.",
        "copain|La pierre n'a plus roulé.",
        "enfant-f|On a attendu, tous les deux.",
        "maman|Le coussin a gardé sa forme.",
        "papa|Soufflez un peu, vos mains.",
        "narrateur|Sarah pose le galet dans la boîte.",
        "narrateur|Un trait de craie dort près du coussin.",
        "enfant-f|On le garde, Nino.",
        "narrateur|Le galet reste tiède, contre le bois.",
        "narrateur|Le galet tiède touche un trait de craie, près du coussin.",
    ],
    (2, 1, 3): [
        "narrateur|Maman baisse les mains.",
        "copain|Un, deux, trois, on a compté.",
        "enfant-f|Le trois nous a tenus.",
        "papa|Les tables n'ont plus bougé.",
        "maman|Le papier a gardé vos chiffres.",
        "narrateur|Sarah pose le galet sur le trois.",
        "narrateur|Un trait de craie reste sous la pierre.",
        "enfant-f|C'est notre marelle, Nino.",
        "narrateur|Le galet marque le chiffre, un peu.",
        "narrateur|Le galet marque le trois ; un trait de craie le suit.",
    ],
    (2, 2, 1): [
        "narrateur|Ils s'arrêtent sur la case huit.",
        "enfant-f|Toi devant, moi derrière.",
        "copain|On est arrivés au même bout.",
        "papa|Chacun son pas, même arrivée.",
        "maman|Le bitume est tiède, sous vos semelles.",
        "narrateur|Sarah range le galet dans la boîte.",
        "narrateur|Un trait de craie barre la case, au soleil.",
        "enfant-f|Regarde, Nino, il tient.",
        "narrateur|Deux ombres se touchent, puis se séparent.",
        "narrateur|Le galet et le trait de craie restent sur la même case.",
    ],
    (2, 2, 2): [
        "narrateur|La case est nette, au centre.",
        "copain|J'ai attendu qu'il soit calme.",
        "enfant-f|Moi j'ai attendu tes pieds.",
        "maman|La poussière est retombée.",
        "papa|Lavez-vous un peu les mains.",
        "narrateur|Sarah pose le galet au milieu.",
        "narrateur|Un trait de craie tient, net, au centre.",
        "enfant-f|C'est notre case, Nino.",
        "narrateur|La pierre ne roule plus.",
        "narrateur|Le galet attend ; un trait de craie barre la case, mince.",
    ],
    (2, 2, 3): [
        "narrateur|Deux galets s'arrêtent près de la grille.",
        "copain|Le tien, le nôtre.",
        "enfant-f|Case après case, pas plus loin.",
        "papa|La mienne va moins vite, oui.",
        "maman|Vos chaussures ont de la poussière.",
        "narrateur|Sarah pose leur galet à côté de celui de papa.",
        "narrateur|Un trait de craie brille entre les deux.",
        "enfant-f|Deux pierres, un chemin.",
        "narrateur|Les deux galets se touchent, un peu.",
        "narrateur|Deux galets se touchent près d'un trait de craie.",
    ],
    (2, 3, 1): [
        "narrateur|Le train de sauts s'arrête sous le toit.",
        "copain|Mon wagon est passé.",
        "enfant-f|Le mien a suivi, sans le rattraper.",
        "papa|Le préau a pris son temps.",
        "maman|Le béton est frais, sous vos mains.",
        "narrateur|Sarah range le galet dans la boîte.",
        "narrateur|Un trait de craie tient au pied du pilier.",
        "enfant-f|Le départ reste là, Nino.",
        "narrateur|Un dernier toc sonne, puis plus rien.",
        "narrateur|Le galet claque une dernière fois près du trait de craie.",
    ],
    (2, 3, 2): [
        "narrateur|L'écho s'est tu, sous le toit.",
        "copain|J'ai attendu le silence.",
        "enfant-f|Moi aussi, avant de sauter.",
        "maman|Le préau vous a laissés finir.",
        "papa|Le pilier est un peu bleu.",
        "narrateur|Sarah pose le galet au pied du pilier.",
        "narrateur|Un trait de craie tient au béton.",
        "enfant-f|Quand ça se tait, on saute.",
        "narrateur|Le toit ne répond plus.",
        "narrateur|Le galet se tait près d'un trait de craie, sous le toit.",
    ],
    (2, 3, 3): [
        "narrateur|Maman baisse les mains, une dernière fois.",
        "copain|J'ai sauté sur ta claque.",
        "enfant-f|Moi aussi, pas avant.",
        "papa|Vos pieds ont appris ses mains.",
        "maman|Le rythme est resté au sol.",
        "narrateur|Sarah pose le galet où maman a frappé.",
        "narrateur|Un trait de craie tient au béton, mince.",
        "enfant-f|C'est notre rythme, Nino.",
        "narrateur|Le galet suit la dernière claque.",
        "narrateur|Le galet suit les mains de maman, le long d'un trait de craie.",
    ],
    (3, 1, 1): [
        "narrateur|Ils s'assoient au bord du tapis.",
        "enfant-f|Une case derrière le ruban.",
        "copain|On a fini, sans tout sauter.",
        "papa|Vous avez pris le temps.",
        "maman|Le ruban a laissé une marque à la laine.",
        "narrateur|Sarah serre le ruban au poignet.",
        "narrateur|Un trait de craie borde le tapis, mince.",
        "enfant-f|C'est notre départ, Nino.",
        "narrateur|Les étoiles de papier jettent un dernier carré.",
        "narrateur|Le ruban rouge reste au poignet, un trait de craie borde le tapis.",
    ],
    (3, 1, 2): [
        "narrateur|Nino se lève du coussin, lentement.",
        "copain|Le ruban n'a plus tiré.",
        "enfant-f|On a attendu, tous les deux.",
        "maman|Le coussin a gardé un rond de tissu.",
        "papa|Soufflez un peu, vos mains.",
        "narrateur|Sarah noue le ruban, plus lâche.",
        "narrateur|Un trait de craie dort près du coussin.",
        "enfant-f|On le garde, Nino.",
        "narrateur|Le ruban sent le coussin, un peu.",
        "narrateur|Le ruban frôle un trait de craie, près du coussin.",
    ],
    (3, 1, 3): [
        "narrateur|Maman baisse les mains.",
        "copain|Un, deux, trois, on a compté.",
        "enfant-f|Le trois nous a tenus.",
        "papa|Les tables n'ont plus bougé.",
        "maman|Le papier a gardé vos chiffres.",
        "narrateur|Sarah pose le ruban sur le trois.",
        "narrateur|Un trait de craie reste sous le tissu.",
        "enfant-f|C'est notre marelle, Nino.",
        "narrateur|Le ruban cache le chiffre, un peu.",
        "narrateur|Le ruban compte le trois au-dessus d'un trait de craie.",
    ],
    (3, 2, 1): [
        "narrateur|Ils s'arrêtent sur la case huit.",
        "enfant-f|Toi devant, moi derrière.",
        "copain|On est arrivés au même bout.",
        "papa|Chacun son pas, même arrivée.",
        "maman|Le bitume est tiède, sous vos semelles.",
        "narrateur|Sarah serre le ruban au poignet.",
        "narrateur|Un trait de craie barre la case, au soleil.",
        "enfant-f|Regarde, Nino, il tient.",
        "narrateur|Le ruban flotte un peu, puis retombe.",
        "narrateur|Le ruban flotte un peu au-dessus d'un trait de craie.",
    ],
    (3, 2, 2): [
        "narrateur|La case est nette, au centre.",
        "copain|J'ai attendu qu'il soit calme.",
        "enfant-f|Moi j'ai attendu tes pieds.",
        "maman|Le vent s'est tu.",
        "papa|Lavez-vous un peu les mains.",
        "narrateur|Sarah pose le ruban au milieu.",
        "narrateur|Un trait de craie tient, net, au centre.",
        "enfant-f|C'est notre case, Nino.",
        "narrateur|Le tissu ne vole plus.",
        "narrateur|Le ruban marque la case ; un trait de craie la barre.",
    ],
    (3, 2, 3): [
        "narrateur|Le galet de papa s'arrête près de la grille.",
        "copain|On a suivi ta pierre.",
        "enfant-f|Le ruban s'est posé où elle s'arrêtait.",
        "papa|La mienne va moins vite, oui.",
        "maman|Vos chaussures ont de la poussière.",
        "narrateur|Sarah pose le ruban à côté du galet.",
        "narrateur|Un trait de craie brille près de la grille.",
        "enfant-f|Le tissu et la pierre, un chemin.",
        "narrateur|Le ruban frôle le galet de papa.",
        "narrateur|Le ruban et le galet de papa gardent un trait de craie.",
    ],
    (3, 3, 1): [
        "narrateur|Le train de sauts s'arrête sous le toit.",
        "copain|Mon wagon est passé.",
        "enfant-f|Le mien a suivi, sans le rattraper.",
        "papa|Le préau a pris son temps.",
        "maman|Le béton est frais, sous vos mains.",
        "narrateur|Sarah serre le ruban au poignet.",
        "narrateur|Un trait de craie tient au pied du pilier.",
        "enfant-f|Le départ reste là, Nino.",
        "narrateur|Le ruban retombe, wagon après wagon.",
        "narrateur|Le ruban suit le train, le long d'un trait de craie.",
    ],
    (3, 3, 2): [
        "narrateur|L'écho s'est tu, sous le toit.",
        "copain|J'ai attendu le silence.",
        "enfant-f|Moi aussi, avant de sauter.",
        "maman|Le préau vous a laissés finir.",
        "papa|Le pilier est un peu bleu.",
        "narrateur|Sarah pose le ruban au pied du pilier.",
        "narrateur|Un trait de craie tient au béton.",
        "enfant-f|Quand ça se tait, on saute.",
        "narrateur|Le toit ne répond plus.",
        "narrateur|Le ruban ne bouge plus près d'un trait de craie, au pilier.",
    ],
    (3, 3, 3): [
        "narrateur|Maman baisse les mains, une dernière fois.",
        "copain|J'ai sauté sur ta claque.",
        "enfant-f|Moi aussi, pas avant.",
        "papa|Vos pieds ont appris ses mains.",
        "maman|Le rythme est resté au sol.",
        "narrateur|Sarah lève le ruban où maman a frappé.",
        "narrateur|Un trait de craie tient au béton, mince.",
        "enfant-f|C'est notre rythme, Nino.",
        "narrateur|Le ruban bat une dernière fois, puis s'arrête.",
        "narrateur|Le ruban bat le rythme, juste au-dessus d'un trait de craie.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "couloir,craie,banc",
        {"emphasis": "trait de craie"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("la craie bleue", "le galet plat", "le ruban rouge")},
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
            {"emphasis": "trait de craie"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("la classe", "la cour", "le préau")},
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
                    {"emphasis": "trait de craie"},
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
        "pas rire",
        "sami",
        "il ne faut pas",
        "hyperactif",
        "ce n'est pas une faute",
        "camarade qui bouge",
        "sara ",
        "au marché",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
        "couleur de miel",
        "merle",
        "j'ai une idée",
        "on dirait que notre mission",
        "poisson",
        "escargot",
        "jardin",
        "maîtresse",
        "grain de craie",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    for clue in (
        "étoile brune", "fil pâle", "croissant d'eau", "croissant pâle",
        "virgule farine", "bouton nacre", "nœud raphia", "pois ivoire",
        "grain savon rose", "grain vanille", "pastille colle", "virgule buée",
        "virgule de buée", "capuchon penche", "grain doré", "brin safran",
        "anneau liège", "clou tête ronde", "grain d'ambre", "goutte de cire",
        "anneau de zinc", "larme de bronze", "point de cire", "bracelet d'écorce",
        "boucle d'étain", "anneau de pollen", "dent de laitue", "éclat de zinc",
        "éclat de thym", "lune d'étain", "grain de grenat", "grain d'indigo",
        "grain de brique", "éclat vert", "écaille d'étain", "vis verte",
        "cristal de sucre", "écaille de lichen", "grain de cire claire",
        "dent de fermeture", "écaille de nacre", "grain de paprika",
        "écaille de boue", "point de rouille", "grain de mica", "grain de cannelle",
        "grain d'ocre", "grain de feutre", "grain de sésame", "écaille de savon",
        "grain de suie", "grain de limon", "grain de quartz", "grain de sel",
        "grain de lessive", "grain de cerise", "rond d'huile", "écaille d'orange",
        "point d'écume", "grain de sève", "point de beurre", "grain de craie",
        "grain de pomme", "grain de bitume", "grain de laine", "grain de grelot",
        "grain de parquet",
    ):
        if clue in whole:
            raise SystemExit(f"{SID} indice interdit: {clue}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "trait de craie" not in blob:
        raise SystemExit(f"{SID}: trait de craie absent")

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
        if "trait de craie" not in c["text"].lower():
            raise SystemExit(f"fin sans trait: {c['chunk_id']}")
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

    tts_ok = all(
        c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") and c.get("text_ssml")
        for c in story["chunks"]
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c["text_xai_tags"] == c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {SID} {sum(words(c['text']) for c in story['chunks'])} mots")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-023 — La marelle de Sarah et Nino\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — attendre / ne pas tout brûler d'un coup "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Sarah, Nino, papa, maman\n"
        "- **Lieu :** école : classe, cour, préau — couloir aux étoiles, "
        "tapis à cases, cour des huit, toit qui parle\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un banc grince dans le couloir. Les étoiles de papier jettent des carrés "
        "bleus. Un **trait de craie** coupe une dalle. Sarah veut finir la marelle "
        "avec Nino **maintenant**, tout d'un coup, avant que les chaussures mangent "
        "le trait. Elle appelle trop vite : Nino ne dit rien. Le silence est une "
        "réponse. Sourire parti. Papa s'accroupit. Merci vécu : tu as vu le trait. "
        "Craie, galet, ruban : les trois restent. Classe (le tapis avale le bleu), "
        "cour (poussière, fente, vent), préau (l'écho trompe). Sarah refuse de "
        "foncer. Tapis, coussin, compter ; ensemble, attendre la case, galet de "
        "papa ; train, écho, rythme de maman. Le trait du début revient. L'objet "
        "porte une trace.\n\n"
        "## Vécu\n\n"
        "Sarah propose, veut tout finir. Nino prend son temps, ou pose sa limite. "
        "Deux rythmes, sans voix caricaturale. Le sourire disparaît ; envie et "
        "inquiétude se bousculent. Papa ou maman s'accroupit à la même hauteur. "
        "Personne ne donne la réponse. Sarah observe l'objet, écoute le lieu, "
        "retrouve le trait. La leçon se voit : une case, puis l'autre ; attendre "
        "l'écho, le coussin, la claque. Jamais dite.\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien gabarit F-NAR-016 / « encore » / « tout doux » / notes vides jetés.\n"
        "- Ouverture inventée (banc qui grince, étoiles, lacet). Pas les cinq gabarits v2.\n"
        "- Indice unique : trait de craie (pas grain de craie, pris par TREE-DIF-022).\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent », merle, miel, slogans jetés.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Merci vécu (papa : tu as vu le trait). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply. Monde ≠ TREE-DIF-022 (jardin, Nina/Aniss), "
        "≠ TREE-DIF-045 (poisson, galet peint).\n\n"
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
