#!/usr/bin/env python3
"""TREE-DIF-009 — F-NAR-019. Petit train d'Amir, rails qui chantent. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-009"
N2 = 15
TITLE = "Le petit train d'Amir, sous les rails qui chantent"
FIL = (
    "Dans le wagon, les grands rails chantent sous le plancher. "
    "Un éclat de ticket pâle brille près des rails de bois. "
    "Amir veut que le petit train arrive sous la chaise, avec Nina, "
    "avant que papa ferme le sac. Il pousse trop vite : le jouet n'arrive pas. "
    "T1 = rails jaunes / bleus / rouges, sans retirer pont, gare, tunnel, grelot, plume, galet. "
    "T2 = pont / gare / tunnel : l'éclat glisse. Ils refusent de foncer. "
    "T3 = grelot / plume / galet. L'éclat paie le début."
)
CHARS = "Amir, Nina, papa, maman"
SETTING = "dans le wagon, rails de bois près du plancher"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "éclat de ticket",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=l_éclat_brille_Amir_veut_sous_la_chaise; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_voie; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_la_couleur_des_rails; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté_le_sac_garde_tout; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=il_pousse_trop_vite_Nina_n_est_pas_prête; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "éclat de ticket",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_éclat_glisse_ils_refusent_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=Amir_attend_le_rythme_de_Nina; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "éclat de ticket",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=les_rails_chantent_l_éclat_a_une_place; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Le plancher fait tic, puis tac, sous les sièges.",
    "papa|Tu entends les rails, Amir ?",
    "enfant-m|Ils chantent.",
    "narrateur|Le wagon sent le bois chaud, et le tissu.",
    "narrateur|Un éclat de ticket brille près d'un rail.",
    "narrateur|Le numéro imprimé est coupé, tout pâle.",
    "maman|Il est tombé de ta poche ?",
    "papa|Oui.",
    "narrateur|Dehors, un champ passe derrière la vitre.",
    "narrateur|Nina pose le sac de bois, près des genoux.",
    "narrateur|Les rails de jouet s'entrechoquent, à l'intérieur.",
    "enfant-m|Je veux le petit train sous la chaise.",
    "enfant-m|Avec Nina, avant que papa ferme le sac.",
    "papa|Tu le poses où, alors ?",
    "enfant-m|Près des rails, tout bas.",
    "maman|Les pièces sont dans le sac.",
    "narrateur|Le sac penche vers le plancher.",
    "narrateur|Amir le rattrape des deux mains.",
    "papa|Merci, tu as tenu le sac.",
    "narrateur|En ce moment, Amir sort la locomotive de bois.",
    "narrateur|Elle est petite, lisse, un peu lourde.",
    "enfant-f|J'ai les rails.",
    "narrateur|Nina ne dit rien de plus.",
    "narrateur|Elle tient un rail, sans le poser.",
    "enfant-m|On fait une longue voie.",
    "narrateur|Le sourire d'Amir attend, un peu trop vite.",
    "papa|Jaune, bleu, ou rouge ?",
]

T1_CHOICE = [
    "narrateur|Trois paquets de rails attendent dans le sac.",
    "narrateur|Les jaunes, les bleus, ou les rouges.",
    "maman|Lequel pose-t-on d'abord ?",
]

T1 = {
    1: {
        "lab": "les rails jaunes",
        "sons": "bois,allée,chaussure",
        "emphasis": "rails jaunes",
        "coul": "jaune",
        "passage": [
            "narrateur|Amir glisse les rails jaunes sous les sièges.",
            "narrateur|L'or de l'allée tombe sur le bois.",
            "enfant-m|C'est un tunnel, tout bas.",
            "papa|Tes mains passent près du plancher ?",
            "narrateur|Nina plie un genou, plus haut que lui.",
            "enfant-f|Moi, je tiens le bout.",
            "narrateur|Amir pousse la locomotive, trop vite.",
            "enfant-m|Va sous la chaise !",
            "narrateur|Le train heurte une chaussure, puis s'arrête.",
            "narrateur|Il n'atteint pas l'ombre de la chaise.",
            "narrateur|Le sourire d'Amir disparaît.",
            "maman|Nina n'avait pas posé son rail.",
            "narrateur|Dans sa poitrine, l'envie se bouscule.",
            "papa|Le pont, la gare, le tunnel, restent.",
            "maman|Le grelot, la plume, le galet, aussi.",
            "enfant-m|Les rails sont jaunes.",
            "narrateur|Un éclat de ticket brille sous le siège.",
        ],
        "question": [
            "narrateur|Le bois a pris la lumière de l'allée.",
            "papa|De quelle couleur sont les rails ?",
        ],
        "qfields": {
            "expected_answer": "jaune",
            "accepted_examples": "jaune | jaunes | rails jaunes | or | dorée | doré | le jaune",
            "retry_prompt": "Le bois a pris la lumière. De quelle couleur sont les rails ?",
        },
        "confirm": [
            "enfant-m|Jaune.",
            "papa|Oui, jaune comme l'or.",
            "narrateur|La locomotive attend au bord de l'ombre.",
            "maman|La chaise est plus loin, là-bas.",
            "enfant-f|Je pose mon rail.",
            "narrateur|Nina le pose, sans se presser.",
            "papa|Le pont, la gare, le tunnel, sont prêts.",
            "narrateur|L'éclat de ticket reste sous le siège.",
        ],
    },
    2: {
        "lab": "les rails bleus",
        "sons": "bois,vitre,verre",
        "emphasis": "rails bleus",
        "coul": "bleu",
        "passage": [
            "narrateur|Amir aligne les rails bleus contre la vitre.",
            "narrateur|Le ciel colle au verre, tout pâle.",
            "enfant-m|On va vers les nuages.",
            "maman|La tablette vibre, tout près ?",
            "narrateur|Nina pose un rail plus haut, au rebord.",
            "enfant-f|Ma main arrive jusqu'ici.",
            "enfant-m|La mienne reste plus bas.",
            "narrateur|Amir pousse, trop fort, le long du verre.",
            "enfant-m|Cours jusqu'à la chaise !",
            "narrateur|Le train dérape, puis quitte la voie.",
            "narrateur|Il n'atteint pas le pied de la chaise.",
            "narrateur|Le sourire d'Amir se plie.",
            "papa|Nina tenait son rail en l'air.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "maman|Le pont, la gare, le tunnel, restent.",
            "papa|Le grelot, la plume, le galet, aussi.",
            "enfant-m|Les rails sont bleus.",
            "narrateur|Un éclat de ticket brille contre le verre.",
        ],
        "question": [
            "narrateur|Le bois a pris le ciel de la vitre.",
            "maman|De quelle couleur sont les rails ?",
        ],
        "qfields": {
            "expected_answer": "bleu",
            "accepted_examples": "bleu | bleus | rails bleus | ciel | vitre | le bleu",
            "retry_prompt": "Le bois a pris le ciel. De quelle couleur sont les rails ?",
        },
        "confirm": [
            "enfant-m|Bleu.",
            "maman|Oui, bleu comme le verre.",
            "narrateur|La locomotive attend contre la goutte.",
            "papa|La chaise est plus loin, sous la tablette.",
            "enfant-f|Je garde le rebord.",
            "narrateur|Nina pose enfin son rail, lente.",
            "maman|Le pont, la gare, le tunnel, sont prêts.",
            "narrateur|L'éclat de ticket reste collé au verre.",
        ],
    },
    3: {
        "lab": "les rails rouges",
        "sons": "bois,valise,tissu",
        "emphasis": "rails rouges",
        "coul": "rouge",
        "passage": [
            "narrateur|Amir monte les rails rouges sur la valise.",
            "narrateur|Le tissu est rêche, un peu chaud.",
            "enfant-m|C'est une montagne.",
            "papa|Le petit train grimpe, alors ?",
            "enfant-m|Oui, puis sous la chaise.",
            "narrateur|Nina tient le haut, près de la poignée.",
            "enfant-f|Je pose le dernier rail.",
            "narrateur|Amir cale le bas, trop vite.",
            "enfant-m|Descends !",
            "narrateur|Le train dévale, puis tombe sur le tapis.",
            "narrateur|Il n'atteint pas le pied de la chaise.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "maman|Nina n'avait pas fini le haut.",
            "papa|Le pont, la gare, le tunnel, restent.",
            "maman|Le grelot, la plume, le galet, aussi.",
            "enfant-m|Les rails sont rouges.",
            "narrateur|Un éclat de ticket brille près de la fermeture.",
        ],
        "question": [
            "narrateur|Le bois a pris le rouge du tissu.",
            "papa|De quelle couleur sont les rails ?",
        ],
        "qfields": {
            "expected_answer": "rouge",
            "accepted_examples": "rouge | rouges | rails rouges | tissu | valise | le rouge",
            "retry_prompt": "Le bois a pris le tissu. De quelle couleur sont les rails ?",
        },
        "confirm": [
            "enfant-m|Rouge.",
            "papa|Oui, rouge comme le tissu.",
            "narrateur|La locomotive attend au pied du tapis.",
            "maman|La chaise est plus loin, après la pente.",
            "enfant-f|Je tiens la poignée.",
            "narrateur|Nina pose le haut, sans se presser.",
            "papa|Le pont, la gare, le tunnel, sont prêts.",
            "narrateur|L'éclat de ticket reste près de la fermeture.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le petit train attend un chemin, sous les sièges.",
        "papa|Le pont, la gare, ou le tunnel ?",
        "maman|Tu le fais aller où ?",
    ],
    2: [
        "narrateur|Le petit train attend un chemin, contre la vitre.",
        "maman|Le pont, la gare, ou le tunnel ?",
        "papa|Tu le fais aller où ?",
    ],
    3: [
        "narrateur|Le petit train attend un chemin, sur la valise.",
        "papa|Le pont, la gare, ou le tunnel ?",
        "maman|Tu le fais aller où ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "pont,chaussure,rails",
        "emphasis": "pont",
        "passage": [
            "narrateur|Amir pose un pont de bois au-dessus de la chaussure.",
            "enfant-m|Il va passer par-dessus !",
            "narrateur|Il pousse, trop fort.",
            "narrateur|Le train saute, puis tombe à côté.",
            "enfant-m|Je le rattrape !",
            "narrateur|Sa main part, puis s'arrête.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Les adultes se taisent, accroupis.",
            "narrateur|Amir écoute les rails, sous le wagon.",
            "narrateur|Ils chantent, tic, puis tac.",
            "narrateur|Il retrouve l'éclat de ticket, coincé sous le pont.",
            "papa|Le pont tremble, tu vois ?",
            "narrateur|Nina tient le milieu, sans parler.",
            "enfant-m|Tu tiens le haut ?",
            "narrateur|Nina hoche la tête, rien de plus.",
            "maman|Le bois attend, entre vous.",
        ],
    },
    (1, 2): {
        "sons": "gare,bois,chaise",
        "emphasis": "gare",
        "passage": [
            "narrateur|Amir pose une petite gare au pied de la chaise.",
            "enfant-m|Il s'arrête là !",
            "narrateur|Le train arrive trop tôt, tout seul.",
            "narrateur|Le quai est vide.",
            "enfant-m|Nina, viens !",
            "narrateur|Nina ne bouge pas.",
            "narrateur|Amir ouvre la bouche, puis se tait.",
            "narrateur|Il refuse de foncer vers elle.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "narrateur|Amir écoute les joints, sous le plancher.",
            "narrateur|L'éclat de ticket a glissé sous le toit.",
            "maman|Le toit est trop haut, pour tes doigts ?",
            "narrateur|Nina pose une main sur le toit, lente.",
            "enfant-m|Tu restes à la gare ?",
            "narrateur|Nina serre le bois, sans répondre.",
            "papa|Le quai attend, entre vous.",
        ],
    },
    (1, 3): {
        "sons": "tissu,chaussette,rails",
        "emphasis": "tunnel",
        "passage": [
            "narrateur|Amir tend une chaussette, en tunnel sous le siège.",
            "enfant-m|Il traverse le noir !",
            "narrateur|Le train entre, trop vite.",
            "narrateur|Un talon de laine le bloque.",
            "enfant-m|Il est coincé !",
            "narrateur|Amir tire, puis relâche.",
            "narrateur|Il refuse de forcer.",
            "narrateur|Maman se tait, accroupie.",
            "narrateur|Amir écoute le tissu, et les rails.",
            "narrateur|Un point pâle brille à l'entrée.",
            "narrateur|C'est l'éclat de ticket, au bord.",
            "papa|Le noir cache le bout, tu vois ?",
            "narrateur|Nina tient la sortie, plus loin.",
            "enfant-m|Tu es de l'autre côté ?",
            "narrateur|Nina souffle, tout bas, oui.",
            "maman|Le tunnel attend, entre vos mains.",
        ],
    },
    (2, 1): {
        "sons": "pont,bouteille,vitre",
        "emphasis": "pont",
        "passage": [
            "narrateur|Amir pose un pont au-dessus d'une bouteille d'eau.",
            "enfant-m|Il passe au-dessus du fleuve !",
            "narrateur|Le verre de la bouteille glisse.",
            "narrateur|Le pont penche, le train dérape.",
            "enfant-m|Je pousse plus fort !",
            "narrateur|Sa main se ferme, puis s'ouvre.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Les adultes se taisent, près de la vitre.",
            "narrateur|Amir écoute le chant des rails, dehors.",
            "narrateur|L'éclat de ticket a glissé contre le verre.",
            "maman|Le pont est mouillé, tu sens ?",
            "narrateur|Nina tient un pied du pont, en haut.",
            "enfant-m|Tu tiens le verre ?",
            "narrateur|Nina pose un doigt, puis le retire.",
            "papa|La bouteille attend, entre vous.",
            "narrateur|Le ciel pâle reste collé au wagon.",
        ],
    },
    (2, 2): {
        "sons": "gare,tablette,vitre",
        "emphasis": "gare",
        "passage": [
            "narrateur|Amir pose la gare sur la tablette froide.",
            "enfant-m|C'est la gare des nuages !",
            "narrateur|La tablette est trop haute, pour lui.",
            "narrateur|Le train grimpe, puis recule.",
            "enfant-m|Nina, mets-le !",
            "narrateur|Nina regarde le verre, longtemps.",
            "narrateur|Amir tend le train, trop tôt.",
            "narrateur|Il le repose, sans insister.",
            "narrateur|Il refuse de foncer vers le haut.",
            "narrateur|Papa s'accroupit, sous la tablette.",
            "narrateur|L'éclat de ticket brille sur le rebord.",
            "papa|Tes bras arrivent jusque-là ?",
            "narrateur|Nina pose le toit, à sa hauteur.",
            "enfant-m|Tu restes en haut ?",
            "narrateur|Nina hoche, les lèvres fermées.",
            "maman|La gare attend, trop haute pour un seul.",
        ],
    },
    (2, 3): {
        "sons": "veste,tissu,vitre",
        "emphasis": "tunnel",
        "passage": [
            "narrateur|Amir plie la veste de papa, en tunnel.",
            "enfant-m|Il passe sous le manteau !",
            "narrateur|Le tissu est sombre, trop long.",
            "narrateur|Le train disparaît, puis plus rien.",
            "enfant-m|Je le cherche !",
            "narrateur|Sa main entre, puis ressort.",
            "narrateur|Il refuse de fouiller trop vite.",
            "narrateur|Maman se tait, près du verre.",
            "narrateur|Amir écoute le tissu, et le chant.",
            "narrateur|L'éclat de ticket luit à la manche.",
            "maman|Le noir est long, tu l'entends ?",
            "narrateur|Nina tient la manche, à la sortie.",
            "enfant-m|Tu vois le bout ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Ses doigts restent sur le tissu.",
            "papa|Le tunnel de laine attend, entre vous.",
        ],
    },
    (3, 1): {
        "sons": "pont,fermeture,valise",
        "emphasis": "pont",
        "passage": [
            "narrateur|Amir pose un pont sur la fermeture de la valise.",
            "enfant-m|Il traverse la rivière de dents !",
            "narrateur|La fermeture fait un petit zzz.",
            "narrateur|Le pont vibre, le train déraille.",
            "enfant-m|Je le tiens !",
            "narrateur|Il lâche, exprès.",
            "narrateur|Il refuse de foncer sur le zzz.",
            "narrateur|Papa se tait, une main sur le tissu.",
            "narrateur|Amir écoute le chant, sous le tapis.",
            "narrateur|L'éclat de ticket penche près des dents.",
            "papa|La fermeture danse, tu vois ?",
            "narrateur|Nina tient la poignée, tout en haut.",
            "enfant-m|Tu tiens le haut ?",
            "narrateur|Nina serre, sans parler.",
            "maman|Le pont de tissu attend, entre vous.",
            "narrateur|La pente rouge reste chaude, un peu.",
        ],
    },
    (3, 2): {
        "sons": "gare,sac,valise",
        "emphasis": "gare",
        "passage": [
            "narrateur|Amir pose la gare contre le sac, au bas.",
            "enfant-m|C'est la gare du sac !",
            "narrateur|Papa approche la fermeture du sac.",
            "narrateur|Le quai est trop près du zip.",
            "enfant-m|Pas maintenant !",
            "narrateur|Le train arrive, trop tôt, tout seul.",
            "narrateur|Nina reste en haut, à la poignée.",
            "narrateur|Amir recule le train, d'un doigt.",
            "narrateur|Il refuse de le jeter dans le sac.",
            "narrateur|Maman s'accroupit, près du tapis.",
            "narrateur|L'éclat de ticket brille sur le zip.",
            "maman|Le sac va se fermer, tu le vois ?",
            "narrateur|Nina descend d'une marche de tissu.",
            "enfant-m|Tu viens à la gare ?",
            "narrateur|Nina s'arrête à mi-pente, silencieuse.",
            "papa|Le quai attend, avant le sac.",
        ],
    },
    (3, 3): {
        "sons": "écharpe,tissu,valise",
        "emphasis": "tunnel",
        "passage": [
            "narrateur|Amir roule l'écharpe, en tunnel rouge.",
            "enfant-m|Il traverse la grotte !",
            "narrateur|Le tissu avale le train, trop vite.",
            "narrateur|Plus rien ne sort, de l'autre bout.",
            "enfant-m|Il est perdu !",
            "narrateur|Amir veut secouer, puis s'arrête.",
            "narrateur|Il refuse de foncer dans la laine.",
            "narrateur|Les adultes se taisent, accroupis.",
            "narrateur|Amir écoute l'écharpe, et les rails.",
            "narrateur|L'éclat de ticket brille à l'entrée.",
            "papa|Le bout est loin, tu le sens ?",
            "narrateur|Nina tient la sortie, près du tapis.",
            "enfant-m|Tu tiens le trou ?",
            "narrateur|Nina ouvre le tissu, sans un mot.",
            "maman|Le tunnel de laine attend, entre vous.",
            "narrateur|La valise garde sa pente, au-dessus.",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Le pont attend un petit poids, ou un signe.",
        "papa|Le grelot, la plume, ou le galet ?",
    ],
    2: [
        "narrateur|La gare attend un petit poids, ou un signe.",
        "maman|Le grelot, la plume, ou le galet ?",
    ],
    3: [
        "narrateur|Le tunnel attend un petit poids, ou un signe.",
        "papa|Le grelot, la plume, ou le galet ?",
    ],
}

T3_SONS = {
    1: {1: "grelot,pont", 2: "plume,pont", 3: "galet,pont"},
    2: {1: "grelot,gare", 2: "plume,gare", 3: "galet,gare"},
    3: {1: "grelot,tissu", 2: "plume,tissu", 3: "galet,tissu"},
}

T3_EMPH = {
    1: {1: "grelot", 2: "plume", 3: "galet"},
    2: {1: "grelot", 2: "plume", 3: "galet"},
    3: {1: "grelot", 2: "plume", 3: "galet"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|Le grelot, dessus.",
        "narrateur|Amir accroche le grelot à la locomotive.",
        "narrateur|Nina reste au bout du pont, silencieuse.",
        "enfant-m|Quand tu l'entends, tu tiens.",
        "narrateur|Le train avance, lent, sur le pont.",
        "narrateur|Le grelot tinte, tout près de la chaussure.",
        "narrateur|Nina serre le bois, au bon moment.",
        "papa|Vous l'avez passé, tous les deux.",
        "narrateur|L'éclat de ticket reste sous le pied du pont.",
        "maman|La chaise est juste derrière.",
    ],
    (1, 1, 2): [
        "enfant-m|La plume, comme un drapeau.",
        "narrateur|Amir pique la plume sur le toit.",
        "narrateur|Nina, plus haute, suit le blanc des yeux.",
        "enfant-m|Tu la vois, là ?",
        "narrateur|Nina lève un doigt, sans parler.",
        "narrateur|Le train passe la chaussure, sous la plume.",
        "narrateur|La plume penche, puis se redresse.",
        "maman|Vous l'avez guidé, de deux hauteurs.",
        "narrateur|L'éclat de ticket se colle à la plume.",
        "papa|L'ombre de la chaise est là.",
    ],
    (1, 1, 3): [
        "enfant-m|Le galet, pour peser.",
        "narrateur|Amir pose le galet dans le wagon.",
        "narrateur|Le train devient lent, plus lourd.",
        "enfant-m|J'attends que Nina tienne.",
        "narrateur|Nina pose les deux mains sur le pont.",
        "narrateur|Le galet garde les roues sur le bois.",
        "narrateur|La chaussure passe dessous, sans choc.",
        "papa|Vous l'avez ralenti, ensemble.",
        "narrateur|L'éclat de ticket reste sous le galet.",
        "maman|Le petit train vise la chaise.",
    ],
    (1, 2, 1): [
        "enfant-m|Le grelot, pour l'annoncer.",
        "narrateur|Amir pose le grelot sur le quai.",
        "narrateur|Nina s'approche, à son rythme.",
        "enfant-m|Quand ça tinte, tu es là.",
        "narrateur|Le train roule, lent, vers la gare.",
        "narrateur|Le grelot tinte, Nina pose sa main.",
        "narrateur|Le quai n'est plus vide.",
        "maman|Vous l'avez attendu, tous les deux.",
        "narrateur|L'éclat de ticket brille sous le toit.",
        "papa|La chaise touche presque le quai.",
    ],
    (1, 2, 2): [
        "enfant-m|La plume, sur le toit.",
        "narrateur|Nina glisse la plume au toit, haute.",
        "narrateur|Amir pousse depuis le plancher, lent.",
        "enfant-f|Je la vois.",
        "narrateur|La plume tremble, puis s'arrête.",
        "narrateur|Le train s'aligne sous le blanc.",
        "narrateur|Deux hauteurs tiennent la gare.",
        "papa|Vous l'avez posé, chacun son bout.",
        "narrateur|L'éclat de ticket se loge sous la plume.",
        "maman|Le pied de la chaise est tout près.",
    ],
    (1, 2, 3): [
        "enfant-m|Le galet, contre le mur.",
        "narrateur|Amir cale le galet au quai, bas.",
        "narrateur|Nina pose le toit, sans se presser.",
        "enfant-m|Il ne partira pas trop tôt.",
        "narrateur|Le galet retient le wagon, un instant.",
        "narrateur|Nina est là, enfin, les deux mains.",
        "narrateur|Le train s'arrête, pile au quai.",
        "maman|Vous l'avez calé, ensemble.",
        "narrateur|L'éclat de ticket reste contre le mur.",
        "papa|La chaise ouvre son ombre, juste là.",
    ],
    (1, 3, 1): [
        "enfant-m|Le grelot, dans le noir.",
        "narrateur|Amir accroche le grelot, avant l'entrée.",
        "narrateur|Nina écoute, à la sortie de laine.",
        "enfant-m|Quand ça tinte, tu ouvres.",
        "narrateur|Le train entre, lent, sous le siège.",
        "narrateur|Le grelot tinte au talon, puis après.",
        "narrateur|Nina écarte la laine, au bon moment.",
        "papa|Vous l'avez entendu, des deux bouts.",
        "narrateur|L'éclat de ticket reste à l'entrée.",
        "maman|La chaise est juste après le trou.",
    ],
    (1, 3, 2): [
        "enfant-m|La plume, pour le voir.",
        "narrateur|Amir pique la plume sur le toit.",
        "narrateur|Dans le noir, un blanc avance.",
        "enfant-f|Je le vois.",
        "narrateur|Nina suit la plume, à la sortie.",
        "narrateur|Le talon de laine s'écarte, tout seul.",
        "narrateur|Le train sort, la plume un peu pliée.",
        "maman|Vous l'avez guidé, dans le sombre.",
        "narrateur|L'éclat de ticket voyage sous la plume.",
        "papa|L'ombre de la chaise ouvre la voie.",
    ],
    (1, 3, 3): [
        "enfant-m|Le galet, pour pas trop vite.",
        "narrateur|Amir pose le galet dans le wagon.",
        "narrateur|Le train entre, lourd, sous le siège.",
        "enfant-m|J'attends que tu tiennes.",
        "narrateur|Nina ouvre la sortie, sans tirer.",
        "narrateur|Le galet passe le talon, tout droit.",
        "narrateur|Le train ressort, lent, vers la chaise.",
        "papa|Vous l'avez ralenti, dans le noir.",
        "narrateur|L'éclat de ticket sort, collé au galet.",
        "maman|La chaise est là, tout près.",
    ],
    (2, 1, 1): [
        "enfant-m|Le grelot, sur le pont.",
        "narrateur|Amir accroche le grelot, près du verre.",
        "narrateur|Nina tient le pied du pont, en haut.",
        "enfant-m|Quand ça tinte, tu serres.",
        "narrateur|Le train avance, lent, au-dessus de l'eau.",
        "narrateur|Le grelot tinte, la bouteille ne glisse plus.",
        "narrateur|Nina serre, au bon tintement.",
        "papa|Vous l'avez tenu, au-dessus du fleuve.",
        "narrateur|L'éclat de ticket reste contre le verre.",
        "maman|La chaise est sous la tablette, après.",
    ],
    (2, 1, 2): [
        "enfant-m|La plume, contre le ciel.",
        "narrateur|Amir pique la plume, elle touche presque le verre.",
        "narrateur|Nina, au rebord, suit le blanc.",
        "enfant-f|Elle penche.",
        "narrateur|Amir pousse moins fort.",
        "narrateur|La plume se redresse, au-dessus de l'eau.",
        "narrateur|Le pont tient, la bouteille aussi.",
        "maman|Vous l'avez lu, dans le ciel.",
        "narrateur|L'éclat de ticket se colle à la plume.",
        "papa|Le pied de la chaise est tout près.",
    ],
    (2, 1, 3): [
        "enfant-m|Le galet, pour coller.",
        "narrateur|Amir pose le galet, les roues s'alourdissent.",
        "narrateur|Nina cale la bouteille, d'un doigt.",
        "enfant-m|Il ne glisse plus.",
        "narrateur|Le train traverse, lent, au-dessus de l'eau.",
        "narrateur|Le galet garde le bois sur le pont.",
        "narrateur|La vitre reflète le passage, tout pâle.",
        "papa|Vous l'avez collé, ensemble.",
        "narrateur|L'éclat de ticket reste sous le galet.",
        "maman|La chaise attend, sous la tablette.",
    ],
    (2, 2, 1): [
        "enfant-m|Le grelot, en haut.",
        "narrateur|Nina pose le grelot sur le toit de gare.",
        "narrateur|Amir pousse depuis le plancher, lent.",
        "enfant-m|Quand ça tinte, tu es prête.",
        "narrateur|Le grelot tinte, trop haut pour lui.",
        "narrateur|Nina reçoit le train, à sa hauteur.",
        "narrateur|La gare des nuages n'est plus trop haute.",
        "maman|Vous l'avez monté, chacun son étage.",
        "narrateur|L'éclat de ticket tinte avec le grelot.",
        "papa|La chaise est juste sous la tablette.",
    ],
    (2, 2, 2): [
        "enfant-m|La plume, pour le ciel.",
        "narrateur|Nina plante la plume au toit, contre le verre.",
        "narrateur|Amir vise le blanc, d'en bas.",
        "enfant-f|C'est ici.",
        "narrateur|Le train grimpe, lent, vers la plume.",
        "narrateur|Deux hauteurs se rejoignent au quai.",
        "narrateur|Le ciel pâle reste collé au toit.",
        "papa|Vous l'avez visé, de loin.",
        "narrateur|L'éclat de ticket se loge sous la plume.",
        "maman|Le pied de la chaise touche la tablette.",
    ],
    (2, 2, 3): [
        "enfant-m|Le galet, pour pas reculer.",
        "narrateur|Amir cale le galet derrière les roues.",
        "narrateur|Nina tire le train, d'en haut, douce.",
        "enfant-m|Je pousse, toi tu tires.",
        "narrateur|Le galet empêche de redescendre.",
        "narrateur|Le train gagne le quai, lent.",
        "narrateur|La tablette froide devient une gare.",
        "maman|Vous l'avez monté, sans le lâcher.",
        "narrateur|L'éclat de ticket reste derrière le galet.",
        "papa|La chaise est là, sous vos mains.",
    ],
    (2, 3, 1): [
        "enfant-m|Le grelot, dans la manche.",
        "narrateur|Amir accroche le grelot, avant le tissu.",
        "narrateur|Nina écoute, à la sortie de la manche.",
        "enfant-m|Quand ça tinte, tu ouvres.",
        "narrateur|Le train entre, lent, sous la veste.",
        "narrateur|Le grelot tinte au milieu, puis au bout.",
        "narrateur|Nina écarte la manche, au tintement.",
        "papa|Vous l'avez suivi, dans le sombre.",
        "narrateur|L'éclat de ticket luit à la manche.",
        "maman|La chaise est après le tissu, tout près.",
    ],
    (2, 3, 2): [
        "enfant-m|La plume, pour le noir.",
        "narrateur|Amir pique la plume, un blanc dans la veste.",
        "narrateur|Nina suit le blanc, à la sortie.",
        "enfant-f|Il avance.",
        "narrateur|Le tissu s'ouvre, un peu, sur la plume.",
        "narrateur|Le train sort, la plume un peu froissée.",
        "narrateur|Deux regards ont tenu le noir.",
        "maman|Vous l'avez vu, malgré le manteau.",
        "narrateur|L'éclat de ticket voyage sous la plume.",
        "papa|La chaise ouvre son pied, après la manche.",
    ],
    (2, 3, 3): [
        "enfant-m|Le galet, pour pas se perdre.",
        "narrateur|Amir pose le galet, le train pèse.",
        "narrateur|Nina tient la manche, ouverte, lente.",
        "enfant-m|Il va tout droit.",
        "narrateur|Le galet trace une ligne, sous la laine.",
        "narrateur|Le train ressort, lourd, vers le verre.",
        "narrateur|La veste redevient un manteau, pas un piège.",
        "papa|Vous l'avez pesé, dans le long noir.",
        "narrateur|L'éclat de ticket sort, collé au galet.",
        "maman|La chaise est là, sous la tablette.",
    ],
    (3, 1, 1): [
        "enfant-m|Le grelot, sur les dents.",
        "narrateur|Amir accroche le grelot, près de la fermeture.",
        "narrateur|Nina serre la poignée, en haut.",
        "enfant-m|Quand ça tinte, tu tiens le haut.",
        "narrateur|Le train avance, lent, sur le pont.",
        "narrateur|Le grelot tinte, le zzz se tait.",
        "narrateur|Nina tient, le pont ne vibre plus.",
        "papa|Vous l'avez calmé, tous les deux.",
        "narrateur|L'éclat de ticket reste près des dents.",
        "maman|La chaise est au bas de la pente.",
    ],
    (3, 1, 2): [
        "enfant-m|La plume, sur la poignée.",
        "narrateur|Nina plante la plume, tout en haut.",
        "narrateur|Amir vise le blanc, depuis le tapis.",
        "enfant-f|Monte.",
        "narrateur|Le train monte la pente, sous la plume.",
        "narrateur|La fermeture reste close, sans danser.",
        "narrateur|Deux hauteurs tiennent le pont de tissu.",
        "maman|Vous l'avez visé, de la poignée au tapis.",
        "narrateur|L'éclat de ticket se colle à la plume.",
        "papa|La chaise attend, après la descente.",
    ],
    (3, 1, 3): [
        "enfant-m|Le galet, pour coller au tissu.",
        "narrateur|Amir pose le galet, les roues s'enfoncent un peu.",
        "narrateur|Nina cale la fermeture, d'un doigt.",
        "enfant-m|Il ne danse plus.",
        "narrateur|Le train traverse, lourd, sur le pont.",
        "narrateur|Le galet garde le bois sur le rêche.",
        "narrateur|La pente rouge se tait.",
        "papa|Vous l'avez collé, sur les dents.",
        "narrateur|L'éclat de ticket reste sous le galet.",
        "maman|La chaise est au pied du tapis.",
    ],
    (3, 2, 1): [
        "enfant-m|Le grelot, avant le sac.",
        "narrateur|Amir pose le grelot sur le quai, bas.",
        "narrateur|Nina descend d'une marche, puis s'arrête.",
        "enfant-m|Quand ça tinte, tu es arrivée.",
        "narrateur|Papa laisse le zip, sans le fermer.",
        "narrateur|Le grelot tinte, Nina pose sa main.",
        "narrateur|Le train s'arrête au quai, pas dans le sac.",
        "maman|Vous l'avez annoncé, avant la fermeture.",
        "narrateur|L'éclat de ticket brille sur le zip.",
        "papa|La chaise est juste après le sac.",
    ],
    (3, 2, 2): [
        "enfant-m|La plume, pour qu'elle voie.",
        "narrateur|Amir pique la plume, visible depuis la pente.",
        "narrateur|Nina suit le blanc, de la poignée au bas.",
        "enfant-f|J'arrive.",
        "narrateur|Elle descend, à son rythme, jusqu'au quai.",
        "narrateur|Le train l'attend, sous la plume.",
        "narrateur|Le sac reste ouvert, un instant de plus.",
        "papa|Vous l'avez rejoint, sans le jeter.",
        "narrateur|L'éclat de ticket se loge sous la plume.",
        "maman|La chaise ouvre son ombre, près du sac.",
    ],
    (3, 2, 3): [
        "enfant-m|Le galet, pour pas trop tôt.",
        "narrateur|Amir cale le galet devant le zip.",
        "narrateur|Nina finit la pente, sans se presser.",
        "enfant-m|Le sac ne le prend pas.",
        "narrateur|Le galet garde le quai, ouvert.",
        "narrateur|Le train s'arrête, pile, Nina pose la main.",
        "narrateur|Papa recule le zip, d'un cran.",
        "maman|Vous l'avez gardé, hors du sac.",
        "narrateur|L'éclat de ticket reste contre le galet.",
        "papa|La chaise est là, tout contre le tissu.",
    ],
    (3, 3, 1): [
        "enfant-m|Le grelot, dans l'écharpe.",
        "narrateur|Amir accroche le grelot, avant la grotte.",
        "narrateur|Nina écoute, à la sortie, près du tapis.",
        "enfant-m|Quand ça tinte, tu ouvres.",
        "narrateur|Le train entre, lent, dans la laine.",
        "narrateur|Le grelot tinte au milieu, puis au bout.",
        "narrateur|Nina ouvre le tissu, au tintement.",
        "papa|Vous l'avez suivi, dans la grotte.",
        "narrateur|L'éclat de ticket brille à l'entrée.",
        "maman|La chaise est juste après l'écharpe.",
    ],
    (3, 3, 2): [
        "enfant-m|La plume, pour le voir.",
        "narrateur|Amir pique la plume, un blanc dans le rouge.",
        "narrateur|Nina suit le blanc, à la sortie.",
        "enfant-f|Il est là.",
        "narrateur|L'écharpe s'ouvre, un peu, sur la plume.",
        "narrateur|Le train sort, la plume un peu pliée.",
        "narrateur|Deux regards ont tenu la grotte.",
        "maman|Vous l'avez vu, malgré la laine.",
        "narrateur|L'éclat de ticket voyage sous la plume.",
        "papa|La chaise ouvre son pied, après le tissu.",
    ],
    (3, 3, 3): [
        "enfant-m|Le galet, pour pas s'avaler.",
        "narrateur|Amir pose le galet, le train pèse.",
        "narrateur|Nina tient la sortie, ouverte, lente.",
        "enfant-m|Il va tout droit.",
        "narrateur|Le galet trace une ligne, dans l'écharpe.",
        "narrateur|Le train ressort, lourd, vers le tapis.",
        "narrateur|L'écharpe redevient un foulard, pas un piège.",
        "papa|Vous l'avez pesé, dans le rouge.",
        "narrateur|L'éclat de ticket sort, collé au galet.",
        "maman|La chaise est là, au pied de la valise.",
    ],
}

END_SONS = {1: "pont,rails", 2: "gare,rails", 3: "tissu,rails"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le pont a failli tout jeter.",
        "narrateur|Le petit train est sous la chaise, enfin.",
        "enfant-m|Tu as tenu.",
        "enfant-f|J'ai entendu.",
        "papa|Le grelot s'est tu.",
        "maman|La voie jaune reste sous les sièges.",
        "narrateur|Les grands rails chantent, plus bas.",
        "narrateur|L'éclat de ticket dort sous le pied du pont.",
    ],
    (1, 1, 2): [
        "narrateur|La plume a failli tomber dans l'allée.",
        "narrateur|Le petit train glisse sous la chaise, le drapeau haut.",
        "enfant-f|Je l'ai vue.",
        "enfant-m|Tu étais plus haute.",
        "papa|Deux hauteurs ont tenu le blanc.",
        "maman|L'or de l'allée reste sur le bois.",
        "narrateur|Les grands rails chantent, sous l'ombre.",
        "narrateur|L'éclat de ticket voyage, collé à la plume.",
    ],
    (1, 1, 3): [
        "narrateur|Le galet a failli faire trop lourd.",
        "narrateur|Le petit train s'arrête sous la chaise, lourd et juste.",
        "enfant-m|On a ralenti.",
        "enfant-f|Oui.",
        "papa|Les roues sont restées sur le bois.",
        "maman|La chaussure est devenue un pont, presque.",
        "narrateur|Les grands rails chantent, sous le plancher.",
        "narrateur|L'éclat de ticket reste coincé sous le galet.",
    ],
    (1, 2, 1): [
        "narrateur|Le quai a failli rester vide.",
        "narrateur|Le petit train est sous la chaise, collé au quai.",
        "enfant-m|Tu es venue.",
        "enfant-f|J'ai entendu.",
        "papa|Le grelot a parlé, pour deux.",
        "maman|Le toit jaune garde son or.",
        "narrateur|Les grands rails chantent, sous la gare.",
        "narrateur|L'éclat de ticket brille sous le toit de bois.",
    ],
    (1, 2, 2): [
        "narrateur|Le toit a failli rester trop haut.",
        "narrateur|Le petit train s'aligne sous la chaise, sous la plume.",
        "enfant-f|Je l'ai posée.",
        "enfant-m|Moi, j'ai poussé.",
        "papa|Chacun son bout, chacun sa hauteur.",
        "maman|Le quai jaune touche presque le pied.",
        "narrateur|Les grands rails chantent, tout bas.",
        "narrateur|L'éclat de ticket se loge sous la plume du toit.",
    ],
    (1, 2, 3): [
        "narrateur|Le train a failli partir trop tôt.",
        "narrateur|Le petit train tient sous la chaise, calé au galet.",
        "enfant-m|Il a attendu.",
        "enfant-f|Moi aussi.",
        "papa|Le mur de la gare a gardé le wagon.",
        "maman|L'ombre de la chaise recouvre le quai.",
        "narrateur|Les grands rails chantent, sous le bois.",
        "narrateur|L'éclat de ticket reste contre le mur de gare.",
    ],
    (1, 3, 1): [
        "narrateur|Le talon de laine a failli tout garder.",
        "narrateur|Le petit train sort sous la chaise, le grelot muet.",
        "enfant-m|Tu as ouvert.",
        "enfant-f|J'ai entendu.",
        "papa|Le noir a rendu le train, aux deux bouts.",
        "maman|La chaussette redevient une chaussette.",
        "narrateur|Les grands rails chantent, sous le siège.",
        "narrateur|L'éclat de ticket reste à l'entrée du tunnel.",
    ],
    (1, 3, 2): [
        "narrateur|Le noir a failli avaler le blanc.",
        "narrateur|Le petit train glisse sous la chaise, plume pliée.",
        "enfant-f|Je l'ai vue.",
        "enfant-m|Dans le sombre.",
        "papa|Un drapeau a tenu le tunnel.",
        "maman|L'or de l'allée reprend le bois.",
        "narrateur|Les grands rails chantent, sous la laine.",
        "narrateur|L'éclat de ticket voyage, caché sous la plume.",
    ],
    (1, 3, 3): [
        "narrateur|Le tunnel a failli trop vite tout prendre.",
        "narrateur|Le petit train ressort sous la chaise, le galet droit.",
        "enfant-m|On a ralenti.",
        "enfant-f|Oui.",
        "papa|Le poids a choisi le droit chemin.",
        "maman|Le siège garde un trou de lumière.",
        "narrateur|Les grands rails chantent, sous le tissu.",
        "narrateur|L'éclat de ticket sort, collé au galet de laine.",
    ],
    (2, 1, 1): [
        "narrateur|La bouteille a failli tout verser.",
        "narrateur|Le petit train gagne le pied de la chaise, grelot tu.",
        "enfant-m|Tu as serré.",
        "enfant-f|J'ai entendu.",
        "papa|Le fleuve de verre est resté en bas.",
        "maman|Le ciel pâle reste collé au pont.",
        "narrateur|Les grands rails chantent, contre la vitre.",
        "narrateur|L'éclat de ticket dort contre le verre du pont.",
    ],
    (2, 1, 2): [
        "narrateur|La plume a failli se coller au ciel.",
        "narrateur|Le petit train arrive sous la chaise, drapeau haut.",
        "enfant-f|Elle a penché.",
        "enfant-m|J'ai ralenti.",
        "papa|Le blanc a lu le pont, pour deux.",
        "maman|L'eau de la bouteille reste sage.",
        "narrateur|Les grands rails chantent, derrière le verre.",
        "narrateur|L'éclat de ticket voyage, collé à la plume du ciel.",
    ],
    (2, 1, 3): [
        "narrateur|Le pont a failli glisser avec l'eau.",
        "narrateur|Le petit train tient sous la chaise, galet collé.",
        "enfant-m|Il n'a plus glissé.",
        "enfant-f|Moi non plus.",
        "papa|Le poids a collé le bois au fleuve.",
        "maman|La tablette ouvre son ombre, tout près.",
        "narrateur|Les grands rails chantent, sous le verre.",
        "narrateur|L'éclat de ticket reste sous le galet mouillé.",
    ],
    (2, 2, 1): [
        "narrateur|La gare a failli rester trop haute.",
        "narrateur|Le petit train est sous la chaise, monté au tintement.",
        "enfant-m|Tu étais en haut.",
        "enfant-f|J'ai entendu.",
        "papa|Le grelot a parlé d'un étage à l'autre.",
        "maman|La tablette froide est devenue un quai.",
        "narrateur|Les grands rails chantent, sous les nuages.",
        "narrateur|L'éclat de ticket tinte, caché sous le grelot du toit.",
    ],
    (2, 2, 2): [
        "narrateur|Le ciel a failli cacher le quai.",
        "narrateur|Le petit train s'aligne sous la chaise, sous la plume.",
        "enfant-f|C'était ici.",
        "enfant-m|Je visais le blanc.",
        "papa|Deux hauteurs ont visé le même toit.",
        "maman|Le verre garde un fil de plume.",
        "narrateur|Les grands rails chantent, contre le ciel.",
        "narrateur|L'éclat de ticket se loge sous la plume du toit bleu.",
    ],
    (2, 2, 3): [
        "narrateur|Le train a failli redescendre, tout seul.",
        "narrateur|Le petit train tient sous la chaise, galet derrière.",
        "enfant-m|J'ai poussé.",
        "enfant-f|J'ai tiré.",
        "papa|Le poids a gardé la pente, pour deux.",
        "maman|La tablette ne recule plus.",
        "narrateur|Les grands rails chantent, sous le quai.",
        "narrateur|L'éclat de ticket reste derrière le galet de gare.",
    ],
    (2, 3, 1): [
        "narrateur|La veste a failli tout avaler.",
        "narrateur|Le petit train sort sous la chaise, le grelot muet.",
        "enfant-m|Tu as ouvert.",
        "enfant-f|J'ai entendu.",
        "papa|La manche a rendu le train, aux deux bouts.",
        "maman|Le manteau redevient un manteau.",
        "narrateur|Les grands rails chantent, sous le tissu.",
        "narrateur|L'éclat de ticket luit, pris dans la manche.",
    ],
    (2, 3, 2): [
        "narrateur|Le noir de la veste a failli garder le blanc.",
        "narrateur|Le petit train glisse sous la chaise, plume froissée.",
        "enfant-f|Il avançait.",
        "enfant-m|Tu l'as vu.",
        "papa|Un drapeau a tenu le manteau, pour deux.",
        "maman|Le verre reprend sa lumière, pâle.",
        "narrateur|Les grands rails chantent, sous la laine.",
        "narrateur|L'éclat de ticket voyage, caché sous la plume de manche.",
    ],
    (2, 3, 3): [
        "narrateur|Le long noir a failli le perdre.",
        "narrateur|Le petit train ressort sous la chaise, le galet droit.",
        "enfant-m|Il a pesé.",
        "enfant-f|Oui.",
        "papa|Le poids a tracé une ligne, dans la veste.",
        "maman|La manche s'ouvre sur le pied de chaise.",
        "narrateur|Les grands rails chantent, sous le manteau.",
        "narrateur|L'éclat de ticket sort, collé au galet de laine bleue.",
    ],
    (3, 1, 1): [
        "narrateur|La fermeture a failli tout faire danser.",
        "narrateur|Le petit train descend sous la chaise, grelot tu.",
        "enfant-m|Tu as tenu le haut.",
        "enfant-f|J'ai entendu.",
        "papa|Le zzz s'est tu, pour deux.",
        "maman|La pente rouge reste chaude, un peu.",
        "narrateur|Les grands rails chantent, sous le tapis.",
        "narrateur|L'éclat de ticket dort près des dents du pont.",
    ],
    (3, 1, 2): [
        "narrateur|La poignée a failli rester trop loin.",
        "narrateur|Le petit train arrive sous la chaise, plume au toit.",
        "enfant-f|Monte, j'ai dit.",
        "enfant-m|J'ai visé.",
        "papa|Le blanc a relié le tapis à la poignée.",
        "maman|Le tissu rêche garde un fil de plume.",
        "narrateur|Les grands rails chantent, sous la valise.",
        "narrateur|L'éclat de ticket voyage, collé à la plume de poignée.",
    ],
    (3, 1, 3): [
        "narrateur|Les dents ont failli tout jeter.",
        "narrateur|Le petit train tient sous la chaise, galet collé.",
        "enfant-m|Il n'a plus dansé.",
        "enfant-f|Moi non plus.",
        "papa|Le poids a collé le bois au rêche.",
        "maman|La pente rouge se tait, enfin.",
        "narrateur|Les grands rails chantent, sous le tissu.",
        "narrateur|L'éclat de ticket reste sous le galet de fermeture.",
    ],
    (3, 2, 1): [
        "narrateur|Le sac a failli tout prendre trop tôt.",
        "narrateur|Le petit train est sous la chaise, hors du zip.",
        "enfant-m|Tu es descendue.",
        "enfant-f|J'ai entendu.",
        "papa|Le grelot a parlé, avant la fermeture.",
        "maman|Le quai du sac reste ouvert, un cran.",
        "narrateur|Les grands rails chantent, sous le tapis.",
        "narrateur|L'éclat de ticket brille, coincé sur le zip.",
    ],
    (3, 2, 2): [
        "narrateur|La pente a failli garder Nina trop haut.",
        "narrateur|Le petit train l'attend sous la chaise, sous la plume.",
        "enfant-f|J'arrive.",
        "enfant-m|Je t'ai vue.",
        "papa|Le blanc a descendu la montagne, pour deux.",
        "maman|Le sac reste ouvert, un instant de plus.",
        "narrateur|Les grands rails chantent, près du tissu.",
        "narrateur|L'éclat de ticket se loge sous la plume du quai.",
    ],
    (3, 2, 3): [
        "narrateur|Le zip a failli avaler le quai.",
        "narrateur|Le petit train tient sous la chaise, galet devant le sac.",
        "enfant-m|Il n'est pas parti.",
        "enfant-f|Moi non plus.",
        "papa|Le poids a gardé le quai, hors du sac.",
        "maman|La chaise touche presque le tissu.",
        "narrateur|Les grands rails chantent, sous le zip.",
        "narrateur|L'éclat de ticket reste contre le galet du sac.",
    ],
    (3, 3, 1): [
        "narrateur|L'écharpe a failli tout garder.",
        "narrateur|Le petit train sort sous la chaise, le grelot muet.",
        "enfant-m|Tu as ouvert.",
        "enfant-f|J'ai entendu.",
        "papa|La grotte a rendu le train, aux deux bouts.",
        "maman|L'écharpe redevient un foulard.",
        "narrateur|Les grands rails chantent, sous le rouge.",
        "narrateur|L'éclat de ticket brille, posé à l'entrée de laine.",
    ],
    (3, 3, 2): [
        "narrateur|Le rouge a failli cacher le blanc.",
        "narrateur|Le petit train glisse sous la chaise, plume pliée.",
        "enfant-f|Il était là.",
        "enfant-m|Tu l'as vu.",
        "papa|Un drapeau a tenu la grotte, pour deux.",
        "maman|La valise garde sa pente, au-dessus.",
        "narrateur|Les grands rails chantent, sous l'écharpe.",
        "narrateur|L'éclat de ticket voyage, caché sous la plume rouge.",
    ],
    (3, 3, 3): [
        "narrateur|La grotte a failli trop vite tout prendre.",
        "narrateur|Le petit train ressort sous la chaise, le galet droit.",
        "enfant-m|Il a pesé.",
        "enfant-f|Oui.",
        "papa|Le poids a tracé une ligne, dans le foulard.",
        "maman|La chaise ouvre son pied, au bas de la valise.",
        "narrateur|Les grands rails chantent, sous le tapis.",
        "narrateur|L'éclat de ticket sort, collé au galet de l'écharpe.",
    ],
}

RECYCLED = (
    "étoile brune", "fil pâle", "croissant d'eau", "croissant pâle",
    "virgule de farine", "bouton de nacre", "nœud de raphia", "pois ivoire",
    "grain de savon", "grain de vanille", "pastille de colle", "virgule de buée",
    "capuchon", "grain doré", "brin de safran", "anneau de liège",
    "clou à tête", "grain d'ambre", "goutte de cire", "anneau de zinc",
    "larme de bronze", "point de cire", "bracelet d'écorce", "boucle d'étain",
    "anneau de pollen", "dent de laitue", "éclat de zinc", "éclat de thym",
    "lune d'étain", "grain de grenat", "grain d'indigo", "grain de brique",
    "éclat vert", "écaille d'étain", "vis verte", "cristal de sucre",
    "écaille de lichen", "grain de cire", "dent de fermeture", "écaille de nacre",
    "grain de paprika", "écaille de boue", "point de rouille", "grain de mica",
    "marque fine", "ombre en forme", "panier d'osier", "merle",
    "couleur de miel", "gouttes au bord", "grain de cannelle", "grain de grelot",
    "éclat de thermos", "éclat de coquille", "éclat de bouton", "grain de paille",
    "grain de parquet", "trait de craie", "victorino", "thermos",
)


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "rails,ticket,sac",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "bois",
        {"fields": t3lab("les rails jaunes", "les rails bleus", "les rails rouges"), "pause_before": 200},
    )

    for a in (1, 2, 3):
        t1 = T1[a]
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(by_src[base], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], t1["question"], "clue", "",
            {"emphasis": t1["coul"], "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["coul"]},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le pont", "la gare", "le tunnel")},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[bse] = voice(
                by_src[bse], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab("le grelot", "la plume", "le galet")},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[b][c],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[b],
                    {"emphasis": "éclat de ticket"},
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
        "bravo tu as",
        "bon travail",
        "il faut attendre",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "tout doux",
        "tout calme",
        "kenzo",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "tu ranges",
        "grain de grelot",
        "sent l'orange",
        "tailles sont différentes",
        "jouer ensemble ?",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    for rec in RECYCLED:
        if rec in whole:
            raise SystemExit(f"{SID} indice recyclé: {rec}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "éclat de ticket" not in blob:
        raise SystemExit(f"{SID}: éclat de ticket absent")

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
        if "éclat de ticket" not in c["text"].lower():
            raise SystemExit(f"éclat non payé: {c['chunk_id']}")
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
    if min(counts) < 520 or max(counts) > 760:
        raise SystemExit(f"longueur chemins hors barre: {min(counts)}-{max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# TREE-DIF-009 — {TITLE}\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.COR.001 — coopération vécue (jamais dite)\n"
        "- **Personnages :** Amir, Nina, papa, maman\n"
        "- **Lieu :** dans le wagon, rails de bois près du plancher "
        "(train jouet au sol, pas la vraie gare, pas la gare carton, pas le train de boîtes)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Les grands rails chantent sous le plancher. Un **éclat de ticket** pâle brille près du bois. "
        "Amir veut que le petit train arrive sous la chaise, avec Nina, "
        "avant que papa ferme le sac. Il pousse trop vite : le jouet n'atteint pas. "
        "Nina n'avait pas posé son rail. Silence. Le sourire disparaît. "
        "Papa s'accroupit. Merci vécu : le sac rattrapé. "
        "T1 = rails jaunes / bleus / rouges : pont, gare, tunnel, grelot, plume, galet restent. "
        "T2 = pont / gare / tunnel : l'éclat glisse, deuxième ruse. "
        "Ils refusent de foncer, écoutent le chant, retrouvent l'éclat du début. "
        "T3 = grelot / plume / galet. Les rails chantent. L'éclat a une place. Le dénouement a failli.\n\n"
        "## Vécu\n\n"
        "Amir propose, Nina prend son temps ou pose sa limite. "
        "Le silence compte. Chaque choix change l'obstacle et le climax. "
        "La leçon se voit : pousser trop tôt laisse le train seul ; "
        "tinter, viser la plume, ou peser le galet, ça tient à deux. "
        "Indice unique : éclat de ticket, payé aux 27 fins. "
        "Monde distinct de TREE-COL-011 (vraie gare), TREE-DIF-017 (gare carton), "
        "TREE-DIF-060 (train de boîtes au salon).\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (tic-tac du plancher, éclat de ticket). Gabarit orange / encore jeté.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (sac tenu). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). "
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
