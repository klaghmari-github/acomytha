#!/usr/bin/env python3
"""TREE-DIF-005 — F-NAR-019. Le sable du toboggan et la phrase d'Aniss. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-005"
N1 = 10
TITLE = "Le sable du toboggan et la phrase d'Aniss"
FIL = (
    "À la rampe du platane, Aniss veut glisser avec Nino, le grain de mica "
    "avec eux, après la phrase de Nino, avant que le sable le cache. "
    "Il coupe trop vite. T1 = matin / sieste / soir (temps, pas un objet). "
    "T2 = bac / échelle / herbe. T3 = ballon / seau / doudou. "
    "Aniss refuse de foncer, retrouve le grain de mica."
)
CHARS = "Aniss, Nino, papa, maman"
SETTING = "le parc du village, toboggan et bac à sable : rampe du platane"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de mica",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le grain dort et Aniss coupe Nino; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_sable_et_la_phrase; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grain de mica",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la phrase peut continuer; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=Aniss veut glisser Nino cherche le mot; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "grain de mica",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=couper cache le grain et la phrase; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de mica",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=il refuse de foncer le grain revient; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de mica",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le grain de mica paie le début; tempo=posé; sourire=léger; respiration=ample",
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
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
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
    "narrateur|Un éclat minuscule dort sur le métal.",
    "narrateur|Ce n'est pas une goutte.",
    "enfant-m|Un grain de mica, papa !",
    "papa|Tu le vois, collé au toboggan ?",
    "narrateur|Le platane jette une ombre ronde.",
    "narrateur|Des moineaux picorent près du bac.",
    "maman|Le banc sent le bois, un peu tiède.",
    "narrateur|Du sable fin colle à la rampe.",
    "narrateur|En ce moment, Aniss veut glisser.",
    "enfant-m|Nino, on glisse, tout de suite !",
    "narrateur|Nino ouvre la bouche, trop lent.",
    "copain|Le sable va.",
    "narrateur|Aniss coupe, impatient.",
    "enfant-m|Je sais, on pousse le sable !",
    "narrateur|Nino se tait.",
    "narrateur|Le mot reste coincé.",
    "papa|Tu as coupé sa phrase, Aniss ?",
    "narrateur|Aniss baisse la voix, les joues chaudes.",
    "maman|Merci d'avoir baissé la voix.",
    "narrateur|Le sourire d'Aniss s'en va.",
    "narrateur|Dans sa poitrine, ça se bouscule.",
]

T1_CHOICE = [
    "narrateur|Le parc change avec le jour.",
    "papa|Le matin, après la sieste, ou le soir ?",
    "maman|Tu choisis.",
]

T1 = {
    1: {
        "sons": "rosée,moineau,métal",
        "emphasis": "glisser",
        "passage": [
            "narrateur|La rosée pique l'herbe, froide.",
            "narrateur|Du sable froid remplit le bac.",
            "narrateur|Sous les doigts, le métal pique.",
            "enfant-m|Je veux glisser maintenant !",
            "narrateur|Nino pose un pied sur l'échelle.",
            "copain|Le toboggan a.",
            "narrateur|Le mot reste coincé, minuscule.",
            "narrateur|Aniss ouvre la bouche.",
            "narrateur|Il la referme, les joues chaudes.",
            "maman|Tu l'entends, Aniss ?",
            "enfant-m|Oui.",
            "enfant-m|Il cherche.",
            "papa|Le parc sent l'herbe mouillée.",
            "narrateur|Un moineau crie, tout près.",
            "narrateur|Le grain de mica cligne, pâle.",
        ],
        "question": [
            "narrateur|Aniss a parlé du toboggan.",
            "maman|Aniss veut quoi ?",
        ],
        "qfields": {
            "expected_answer": "glisser",
            "accepted_examples": "glisser | le toboggan | toboggan | glisser maintenant | il veut glisser",
            "retry_prompt": "Aniss veut glisser. Il veut quoi ?",
        },
        "confirm": [
            "narrateur|Nino reprend, plus bas.",
            "copain|Le toboggan a du sable.",
            "enfant-m|On y va.",
            "papa|Sa phrase est arrivée.",
            "maman|On peut avancer, maintenant.",
            "narrateur|Le grain de mica tient au métal.",
            "papa|Où va-t-on d'abord ?",
        ],
        "voy": "Le matin ouvre trois chemins, dans le parc.",
    },
    2: {
        "sons": "cigale,sable,métal",
        "emphasis": "Nino",
        "passage": [
            "narrateur|L'air sent la poussière chaude.",
            "narrateur|Au toucher, le toboggan est tiède.",
            "narrateur|Sous les paumes, le sable brûle.",
            "enfant-m|Je veux glisser, vite !",
            "narrateur|Nino parle, bas, lent.",
            "copain|Le bac est.",
            "narrateur|Aniss se tait, les mains au barreau.",
            "maman|Tu l'entends, ce murmure ?",
            "enfant-m|Oui, maman.",
            "enfant-m|C'est Nino.",
            "papa|Le parc dore, après la sieste.",
            "narrateur|Une cigale frotte, loin.",
            "narrateur|Le grain de mica cligne, tiède.",
            "enfant-m|J'attends sa phrase.",
        ],
        "question": [
            "narrateur|Un murmure est venu, bas.",
            "papa|Qui parle doucement ?",
        ],
        "qfields": {
            "expected_answer": "Nino",
            "accepted_examples": "nino | c'est nino | nino parle | lui",
            "retry_prompt": "Nino parle doucement. Qui parle ?",
        },
        "confirm": [
            "narrateur|Nino reprend, plus bas.",
            "copain|Le bac est plein.",
            "enfant-m|On y va.",
            "papa|Sa phrase est arrivée.",
            "maman|On peut avancer, maintenant.",
            "narrateur|Le grain de mica tient, tiède.",
            "maman|Où va-t-on d'abord ?",
        ],
        "voy": "Après la sieste, trois endroits attendent.",
    },
    3: {
        "sons": "lampadaire,sable,métal",
        "emphasis": "sable",
        "passage": [
            "narrateur|La lumière devient orange, lente.",
            "narrateur|Un lampadaire fait un petit tic.",
            "narrateur|Le sable colle sur le toboggan.",
            "enfant-m|Je veux glisser avant la nuit !",
            "narrateur|Nino cherche un mot.",
            "copain|Je glisse avec.",
            "narrateur|Aniss attend, les lèvres serrées.",
            "papa|Le métal refroidit, ce soir.",
            "maman|Tu vois le sable, Aniss ?",
            "enfant-m|Oui.",
            "enfant-m|Sur le toboggan.",
            "narrateur|L'ombre violette touche l'herbe.",
            "narrateur|Le grain de mica cligne, orange.",
            "enfant-m|On glisse après sa phrase.",
        ],
        "question": [
            "narrateur|Les grains brillent sur le métal.",
            "maman|Où colle le sable ?",
        ],
        "qfields": {
            "expected_answer": "sur le toboggan",
            "accepted_examples": "toboggan | sur le toboggan | le toboggan | rampe | sur la rampe",
            "retry_prompt": "Le sable colle sur le toboggan. Où ?",
        },
        "confirm": [
            "narrateur|Nino reprend, plus bas.",
            "copain|Je glisse avec toi.",
            "enfant-m|On y va.",
            "papa|Sa phrase est arrivée.",
            "maman|On peut avancer, maintenant.",
            "narrateur|Le grain de mica tient, orange.",
            "papa|Où va-t-on d'abord ?",
        ],
        "voy": "Le soir laisse trois petits chemins.",
    },
}

T2 = {
    (1, 1): {
        "sons": "sable,bac,moineau",
        "emphasis": "sable",
        "passage": [
            "narrateur|Aniss court vers le bac.",
            "narrateur|Le sable froid colle aux paumes.",
            "narrateur|Nino y enfonce une main.",
            "copain|Le sable est.",
            "narrateur|Le mot tremble au bord.",
            "enfant-m|Je t'écoute.",
            "narrateur|Aniss veut vider, trop vite.",
            "narrateur|Un nuage recouvre le grain de mica.",
            "narrateur|Le sourire d'Aniss s'en va.",
            "maman|Il cherche, Aniss.",
            "papa|Le bac est plein, ce matin.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "copain|Le sable est collant.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "échelle,métal,moineau",
        "emphasis": "échelle",
        "passage": [
            "narrateur|Aniss pose les mains sur l'échelle.",
            "narrateur|Sous les doigts, le métal pique.",
            "narrateur|Nino grimpe un barreau, puis s'arrête.",
            "copain|Le premier est.",
            "narrateur|Aniss veut passer, trop vite.",
            "narrateur|Sa main cache le grain de mica.",
            "papa|Tu le laisses finir ?",
            "enfant-m|Oui.",
            "narrateur|Aniss recule d'un barreau.",
            "narrateur|Le sourire d'Aniss s'en va.",
            "copain|Le premier est froid.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "maman|Tu as vu sa pause ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "herbe,rosée,moineau",
        "emphasis": "herbe",
        "passage": [
            "narrateur|Ils s'assoient dans l'herbe, bas.",
            "narrateur|La rosée pique l'herbe, froide.",
            "narrateur|Le pied du toboggan arrive là.",
            "copain|Je glisse vers.",
            "narrateur|Aniss veut glisser, trop vite.",
            "narrateur|Il se lève, trop tôt.",
            "maman|Sa phrase va venir.",
            "enfant-m|Je reste ici.",
            "narrateur|Un moineau crie, tout près.",
            "narrateur|Le grain de mica cligne, pâle.",
            "copain|Je glisse vers toi.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "papa|Le bas est mouillé, ce matin.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "sable,cigale,bac",
        "emphasis": "château",
        "passage": [
            "narrateur|Ils rejoignent le bac, pas à pas.",
            "narrateur|Sous les paumes, le sable brûle.",
            "narrateur|Nino souffle, une main au-dessus.",
            "copain|Le château est.",
            "narrateur|Aniss s'assoit, sans presser.",
            "papa|Tu attends sa phrase ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss tasse trop vite, trop fort.",
            "narrateur|Le château s'écroule, chaud.",
            "narrateur|Le grain de mica disparaît, sous les grains.",
            "narrateur|Le sourire d'Aniss s'en va.",
            "copain|Le château est trop sec.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "échelle,métal,cigale",
        "emphasis": "barreau",
        "passage": [
            "narrateur|Ils touchent l'échelle, chaude.",
            "narrateur|Au toucher, le toboggan est tiède.",
            "narrateur|Nino lève un pied, cherche le mot.",
            "copain|Je monte le.",
            "narrateur|Aniss compte dans sa tête, bas.",
            "maman|Il va le trouver.",
            "enfant-m|J'attends.",
            "narrateur|Aniss pousse trop tôt, trop près.",
            "narrateur|Nino recule, le mot perdu.",
            "narrateur|Le grain de mica se cache, sous un pouce.",
            "copain|Je monte le deuxième.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "papa|On reste derrière lui.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "herbe,cigale,sable",
        "emphasis": "herbe",
        "passage": [
            "narrateur|L'herbe craque un peu, sèche.",
            "narrateur|La lumière pèse, blanche.",
            "narrateur|Ils attendent au bas du toboggan.",
            "copain|Le bas est.",
            "narrateur|Aniss souffle, les mains dans l'herbe.",
            "papa|Nino cherche, sans se presser.",
            "enfant-m|J'écoute.",
            "narrateur|Aniss veut appeler, trop fort.",
            "narrateur|Nino se tait, les épaules hautes.",
            "narrateur|Le grain de mica cligne, tiède.",
            "copain|Le bas est chaud.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "maman|On peut s'y asseoir.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "sable,lampadaire,bac",
        "emphasis": "rampe",
        "passage": [
            "narrateur|Ils s'agenouillent près du bac.",
            "narrateur|Voilà le sable, refroidi, fin.",
            "narrateur|Nino trace une ligne, puis s'arrête.",
            "copain|La rampe a.",
            "enfant-m|Je reste.",
            "maman|Le soir donne du temps.",
            "narrateur|Un lampadaire fait un petit tic.",
            "narrateur|Aniss racle trop vite, trop fort.",
            "narrateur|Le sable retourne sur le métal.",
            "narrateur|Le grain de mica s'efface, orange.",
            "copain|La rampe a pris le sable.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "papa|On le verra, ensemble.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "échelle,lampadaire,métal",
        "emphasis": "haut",
        "passage": [
            "narrateur|L'échelle prend la lumière orange.",
            "narrateur|Maintenant le toboggan refroidit.",
            "narrateur|Nino s'accroche, puis ouvre la bouche.",
            "copain|Le haut est.",
            "narrateur|Aniss ne dit rien, tout près.",
            "papa|On écoute, ce soir.",
            "narrateur|Un lampadaire fait un petit tic.",
            "narrateur|Aniss grimpe trop tôt, trop haut.",
            "narrateur|Nino reste en bas, sans mot.",
            "narrateur|Le grain de mica cligne, orange.",
            "copain|Le haut est clair.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "maman|On y va, barreau après barreau.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "herbe,lampadaire,métal",
        "emphasis": "herbe",
        "passage": [
            "narrateur|L'herbe du soir est fraîche.",
            "narrateur|La lumière devient orange, lente.",
            "narrateur|Ils se placent au bas du toboggan.",
            "copain|On se voit dans.",
            "narrateur|Aniss lève les yeux, et attend.",
            "maman|Il finit, Aniss.",
            "enfant-m|Oui.",
            "narrateur|Aniss veut crier, trop tôt.",
            "narrateur|Nino ferme la bouche.",
            "narrateur|Le grain de mica cligne, orange.",
            "copain|On se voit dans l'herbe.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "papa|Le lampadaire les touche, bas.",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
}

T3_CHOICE = {
    1: {
        1: "Dans le bac, trois objets attendent.",
        2: "Dans le bac, trois objets chauffent.",
        3: "Dans le bac, trois objets dorment.",
    },
    2: {
        1: "Près de l'échelle, trois objets attendent.",
        2: "Près de l'échelle, trois objets chauffent.",
        3: "Près de l'échelle, trois objets dorment.",
    },
    3: {
        1: "Dans l'herbe, trois objets attendent.",
        2: "Dans l'herbe, trois objets chauffent.",
        3: "Dans l'herbe, trois objets dorment.",
    },
}

TONE = {
    1: {
        "sable": "Du sable froid remplit le bac.",
        "metal": "Sous les doigts, le métal pique.",
        "air": "La rosée pique l'herbe, froide.",
        "bruit": "Un moineau crie, tout près.",
        "lum": "L'ombre du platane est longue.",
        "mica": "Le grain de mica cligne, pâle.",
        "file": "Ça file, court, vif.",
        "peau": "Les doigts d'Aniss sont un peu rouges.",
        "banc": "Sur le banc du matin, ça pique.",
        "quand": "ce matin",
    },
    2: {
        "sable": "Sous les paumes, le sable brûle.",
        "metal": "Au toucher, le toboggan est tiède.",
        "air": "L'air sent la poussière chaude.",
        "bruit": "Une cigale frotte, loin.",
        "lum": "La lumière pèse, blanche.",
        "mica": "Le grain de mica cligne, tiède.",
        "file": "Ça file, chaud, vif.",
        "peau": "La tempe d'Aniss est chaude, sablée.",
        "banc": "Voilà le banc de la sieste, chaud.",
        "quand": "après la sieste",
    },
    3: {
        "sable": "Voilà le sable, refroidi, fin.",
        "metal": "Maintenant le toboggan refroidit.",
        "air": "La lumière devient orange, lente.",
        "bruit": "Un lampadaire fait un petit tic.",
        "lum": "L'ombre violette touche l'herbe.",
        "mica": "Le grain de mica cligne, orange.",
        "file": "Ça file, orange, vif.",
        "peau": "Les genoux d'Aniss ont du sable froid.",
        "banc": "Près du banc du soir, l'air est frais.",
        "quand": "ce soir",
    },
}


def t3_pass(t1: int, t2: int, t3: int) -> list[str]:
    t = TONE[t1]
    if t2 == 1 and t3 == 1:
        return [
            f"narrateur|{t['sable']}",
            "narrateur|Un rond rouge dépasse, à peine.",
            "copain|Le ballon est.",
            "narrateur|Aniss creuse, puis attend.",
            "papa|Il est sous le sable ?",
            "narrateur|Aniss garde les mains, sans bousculer.",
            "copain|Le ballon est sous le sable.",
            "enfant-m|Je le sors.",
            "narrateur|Le rouge sort, un peu sablé.",
            f"narrateur|{t['mica']}",
            "maman|Vous l'avez, tous les deux.",
            "narrateur|Ils grimpent, le ballon contre la hanche.",
            f"narrateur|{t['file']}",
        ]
    if t2 == 1 and t3 == 2:
        return [
            f"narrateur|{t['air']}",
            "narrateur|Le seau bleu attend près du bac.",
            "copain|Le seau est.",
            "narrateur|Aniss tient l'anse, sans tirer.",
            "maman|Il va le dire.",
            "narrateur|Aniss ne tire pas trop tôt.",
            "copain|Le seau est lourd.",
            "enfant-m|On verse, alors.",
            "narrateur|Ils raclent le sable de la rampe.",
            "narrateur|Le bleu se remplit, grain après grain.",
            f"narrateur|{t['metal']}",
            f"narrateur|{t['mica']}",
            "papa|La rampe redevient lisse.",
            f"narrateur|{t['file']}",
        ]
    if t2 == 1 and t3 == 3:
        return [
            f"narrateur|{t['lum']}",
            "narrateur|Le doudou dort dans le bac, sablé.",
            "copain|Le doudou est.",
            "narrateur|Aniss garde les mains, et attend.",
            "papa|Il le veut, ce doudou ?",
            "narrateur|Aniss laisse le silence répondre.",
            "copain|Le doudou est tout sablé.",
            "enfant-m|On le tapote.",
            "narrateur|Le sable tombe, un nuage minuscule.",
            "narrateur|Nino le serre contre sa joue.",
            f"narrateur|{t['bruit']}",
            f"narrateur|{t['mica']}",
            "maman|Il est prêt, maintenant.",
            "narrateur|Ils glissent, le doudou entre eux.",
        ]
    if t2 == 2 and t3 == 1:
        return [
            f"narrateur|{t['metal']}",
            "narrateur|Le ballon rouge coince un barreau.",
            "copain|Le ballon va.",
            "narrateur|Aniss ouvre les mains, en bas.",
            "maman|Tu le laisses dire ?",
            "narrateur|Aniss reste en bas, sans grimper.",
            "copain|Le ballon va tomber.",
            "enfant-m|Je suis là.",
            "narrateur|Nino pousse, lentement.",
            "narrateur|Le rouge atterrit dans les mains d'Aniss.",
            f"narrateur|{t['bruit']}",
            f"narrateur|{t['mica']}",
            "papa|Le chemin est libre.",
            "narrateur|Ils montent, puis ça dévale.",
        ]
    if t2 == 2 and t3 == 2:
        return [
            f"narrateur|{t['lum']}",
            "narrateur|Le seau bleu pend près du haut.",
            "copain|Le seau va.",
            "narrateur|Aniss reste un barreau plus bas.",
            "papa|On l'écoute, d'accord ?",
            "narrateur|Aniss compte un barreau, sans pousser.",
            "copain|Le seau va nous aider.",
            "enfant-m|Je te le tends.",
            "narrateur|Nino pousse le sable, lentement.",
            "narrateur|Les grains tombent dans le bleu.",
            f"narrateur|{t['sable']}",
            f"narrateur|{t['mica']}",
            "maman|La rampe redevient glissante.",
            "narrateur|Ils dévalent, le seau à la main.",
        ]
    if t2 == 2 and t3 == 3:
        return [
            f"narrateur|{t['air']}",
            "narrateur|Le doudou est coincé sur un barreau.",
            "copain|Le doudou va.",
            "narrateur|Aniss ne le prend pas, et attend.",
            "maman|Il cherche.",
            "narrateur|Aniss n'attrape pas le tissu.",
            "copain|Le doudou va avec moi.",
            "enfant-m|Je te le passe.",
            "narrateur|Nino le glisse sous son bras.",
            "narrateur|Ils montent, barreau après barreau.",
            f"narrateur|{t['metal']}",
            f"narrateur|{t['mica']}",
            "papa|Vous y êtes, tout en haut.",
            "narrateur|Ils glissent, le doudou au milieu.",
        ]
    if t2 == 3 and t3 == 1:
        return [
            f"narrateur|{t['air']}",
            "narrateur|Ils posent le ballon dans l'herbe.",
            "copain|Le ballon reste.",
            "narrateur|Aniss recule d'un pas, et attend.",
            "papa|Il marque l'arrivée ?",
            "narrateur|Aniss ne se lance pas trop tôt.",
            "copain|Le ballon reste ici.",
            "enfant-m|On glisse vers lui.",
            "narrateur|Ils grimpent, puis se lancent.",
            "narrateur|Le métal chante, court.",
            f"narrateur|{t['peau']}",
            f"narrateur|{t['mica']}",
            "maman|Le rouge les attendait.",
            "enfant-m|Une fois de plus !",
        ]
    if t2 == 3 and t3 == 2:
        return [
            f"narrateur|{t['sable']}",
            "narrateur|Le seau bleu attend dans l'herbe.",
            "copain|Le seau est.",
            "narrateur|Aniss pose l'anse, sans parler.",
            "maman|On attend le mot.",
            "narrateur|Aniss ne verse pas trop tôt.",
            "copain|Le seau est prêt.",
            "enfant-m|On glisse, puis on verse.",
            "narrateur|Ils dévalent, un nuage de grains.",
            "narrateur|Aniss secoue ses genoux au-dessus.",
            f"narrateur|{t['bruit']}",
            f"narrateur|{t['mica']}",
            "papa|Le bleu a pris le sable.",
            "enfant-m|La rampe est plus lisse !",
        ]
    return [
        f"narrateur|{t['lum']}",
        "narrateur|Ils posent le doudou dans l'herbe.",
        "copain|Le doudou me.",
        "narrateur|Aniss se tait, les yeux sur Nino.",
        "papa|Il n'a pas fini.",
        "narrateur|Aniss garde les yeux, sans parler.",
        "copain|Le doudou me regarde.",
        "enfant-m|On glisse vers lui.",
        "narrateur|Ils montent, puis descendent, vifs.",
        "narrateur|Le doudou les reçoit, mou.",
        f"narrateur|{t['peau']}",
        f"narrateur|{t['mica']}",
        "maman|Il a vu toute la descente.",
        "enfant-m|On a glissé !",
    ]


T3_SONS = {
    (1, 1): "ballon,sable",
    (1, 2): "seau,sable",
    (1, 3): "doudou,sable",
    (2, 1): "ballon,échelle",
    (2, 2): "seau,échelle",
    (2, 3): "doudou,échelle",
    (3, 1): "ballon,herbe",
    (3, 2): "seau,herbe",
    (3, 3): "doudou,herbe",
}

T3_EMPH = {1: "ballon", 2: "seau", 3: "doudou"}

FIN_IMG = {
    (1, 1, 1): "Un grain de mica dort sur le ballon.",
    (1, 1, 2): "Un grain de mica brille dans le seau.",
    (1, 1, 3): "Un grain de mica colle au doudou.",
    (1, 2, 1): "Un barreau garde le grain de mica.",
    (1, 2, 2): "L'anse froide tient un grain de mica.",
    (1, 2, 3): "Sa joue de tissu a pris le mica.",
    (1, 3, 1): "L'herbe mouillée cache le grain de mica.",
    (1, 3, 2): "Le seau du matin garde le mica.",
    (1, 3, 3): "Un genou d'herbe colle au mica.",
    (2, 1, 1): "Le mica tiède brille sur le ballon.",
    (2, 1, 2): "Le mica chaud cliquette dans le seau.",
    (2, 1, 3): "Le mica chaud dort sur le doudou.",
    (2, 2, 1): "Le mica tiède marque le ballon, au barreau.",
    (2, 2, 2): "Le mica chaud tient à l'anse.",
    (2, 2, 3): "Le mica sent le soleil, sur le doudou.",
    (2, 3, 1): "Dans l'herbe sèche, le mica pique le ballon.",
    (2, 3, 2): "Une couronne de grains chauds borde le mica.",
    (2, 3, 3): "De l'herbe sèche colle au mica, au doudou.",
    (3, 1, 1): "Cette dernière lumière reste sur le mica.",
    (3, 1, 2): "Le seau, presque violet, garde le mica.",
    (3, 1, 3): "Un grain de mica orange dort sur le doudou.",
    (3, 2, 1): "Vers le lampadaire, le mica roule au ballon.",
    (3, 2, 2): "Dans l'ombre, le mica cliquette, au seau.",
    (3, 2, 3): "Contre l'échelle, le mica refroidit le doudou.",
    (3, 3, 1): "Dans l'herbe fraîche, le mica s'endort au ballon.",
    (3, 3, 2): "Un peu de sable du soir reste au mica.",
    (3, 3, 3): "Devant le toboggan, le mica veille au doudou.",
}

LIEU_FIN = {
    1: "Ils quittent le bac, les genoux sablés.",
    2: "Ils descendent de l'échelle, lents.",
    3: "Ils restent un moment dans l'herbe.",
}

OBJ_FIN = {
    1: "Aniss tient le ballon rouge.",
    2: "Nino balance le seau, vide.",
    3: "Le doudou voyage sous le bras de Nino.",
}

END_SONS = {1: "sable,banc", 2: "métal,banc", 3: "herbe,banc"}


def fin_pass(t1: int, t2: int, t3: int) -> list[str]:
    t = TONE[t1]
    return [
        "narrateur|Ils ont glissé, l'un après l'autre.",
        f"narrateur|{LIEU_FIN[t2]}",
        f"narrateur|{OBJ_FIN[t3]}",
        "enfant-m|C'était bien.",
        "papa|Le toboggan a chanté, court.",
        "maman|On rejoint le banc ?",
        "enfant-m|Oui.",
        f"narrateur|{t['banc']}",
        f"narrateur|{FIN_IMG[(t1, t2, t3)]}",
    ]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "enfants_parc,métal,moineaux"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("le matin", "après la sieste", "le soir")},
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
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": "grain de mica"}
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"],
            [
                f"narrateur|{t1['voy']}",
                "papa|Le bac, l'échelle, ou l'herbe ?",
                "maman|Tu choisis.",
            ],
            "choice",
            "",
            {"fields": t3lab("le bac", "l'échelle", "l'herbe")},
        )
        for b in (1, 2, 3):
            t2 = T2[(a, b)]
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]}
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"],
                [
                    f"narrateur|{T3_CHOICE[b][a]}",
                    "papa|Le ballon rouge, le seau bleu, ou le doudou ?",
                    "maman|Tu choisis.",
                ],
                "choice",
                "",
                {"fields": t3lab("le ballon rouge", "le seau bleu", "le doudou")},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf],
                    t3_pass(a, b, c),
                    "resolution",
                    T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    fin_pass(a, b, c),
                    "ending",
                    END_SONS[b],
                    {"emphasis": "grain de mica"},
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
        "j'ai compris",
        "mission accomplie",
        "il faut attendre",
        "noé",
        "noe ",
        "léa",
        "lea ",
        "sami",
        "tom ",
        "iris",
        "lina",
        "merle",
        "miel",
        "aujourd'hui",
        "tout doux",
        "tout calme",
        "galet",
        "poisson",
        "arrosoir",
        "jardinier",
        "maîtresse",
        "maitresse",
        "grain doré",
        "grain d'ambre",
        "étoile brune",
        "fil pâle",
        "point de cire",
        "point de rouille",
        "grain d'indigo",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "aniss" not in blob or "nino" not in blob:
        raise SystemExit(f"{SID}: troupe Aniss/Nino absente")
    if "grain de mica" not in blob:
        raise SystemExit(f"{SID}: indice grain de mica absent")
    if "toboggan" not in blob or "sable" not in blob:
        raise SystemExit(f"{SID}: toboggan/sable absents")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    if "merci" not in aj and "bravo" not in aj:
        raise SystemExit(f"{SID}: merci/bravo absent")
    if aj.count("merci") + aj.count("bravo") != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{aj.count('merci') + aj.count('bravo')}")

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
        if "mica" not in low:
            raise SystemExit(f"fin sans mica: {last_n[-1]}")
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

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-005 — Le sable du toboggan et la phrase d'Aniss\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.002 — laisser l'autre finir sa phrase "
        "(vécue, jamais dite : Aniss coupe, le mot se tait, il attend, Nino finit)\n"
        "- **Personnages :** Aniss, Nino, papa, maman\n"
        "- **Lieu :** parc du village, rampe du platane, toboggan et bac à sable\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un éclat minuscule dort sur le métal : ce n'est pas une goutte, "
        "c'est un **grain de mica**. Aniss veut glisser **maintenant**, "
        "avec Nino, avant que le sable cache le grain. Nino ouvre la bouche, trop lent. "
        "Aniss coupe. Le mot reste coincé. Première idée ratée. "
        "T1 colore le temps (matin froid, sieste chaude, soir orange) : "
        "le sable et la phrase restent. Bac (nuage, château, rampe), "
        "échelle (barreau, pouce, grimpe trop tôt), herbe (levée trop tôt, cri, bouche fermée). "
        "Ballon, seau, doudou. Aniss refuse de foncer, retrouve le grain. Ils glissent.\n\n"
        "## Vécu\n\n"
        "Aniss propose **maintenant**. Nino prend son temps. Silence = réponse. "
        "Le sourire disparaît ; envie et inquiétude se bousculent. "
        "Papa ou maman s'accroupit à la même hauteur. Personne ne donne la réponse. "
        "Aniss observe l'objet, écoute le parc, retrouve le grain de mica. "
        "La leçon se voit : couper fait taire ; attendre fait finir la phrase, "
        "et la rampe redevient lisse. Le dénouement a failli ne pas arriver. "
        "Le grain de mica paie l'ouverture.\n\n"
        "## Vu et corrigé\n\n"
        "- Noé / merle / miel / tics / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Monde ≠ TREE-DIF-045 (pas d'école, galet, poisson). "
        "≠ TREE-COL-008 (pas de jardin, arrosoir).\n"
        "- T1 = temps (matin / sieste / soir) : ne retire pas le sable ni la phrase.\n"
        "- T1/T2/T3 changent l'obstacle. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : le grain de mica, payé au climax et à chaque fin.\n"
        "- Merci vécu (maman : tu as baissé la voix). Question d'adulte. Un « en ce moment ».\n"
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
