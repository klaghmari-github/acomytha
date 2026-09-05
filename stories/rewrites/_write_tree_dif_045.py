#!/usr/bin/env python3
"""TREE-DIF-045 — Le galet peint d'Aniss et le poisson de la classe (F-NAR-019, N3, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-045"
N3 = 16
TITLE = "Le galet peint d'Aniss et le poisson de la classe"
FIL = (
    "Dans la classe, Aniss veut poser son galet peint au fond du bac, "
    "pour le poisson, avant que le grain d'indigo fonde dans le papier. "
    "Sarah veut un plouf. Aniss répond avec les mains. "
    "Galet, épuisette, torchon : les trois partent. "
    "Bac trop haut, évier trop vite, bac à sable trop mêlé. "
    "Neuf façons. Le grain d'indigo tient, enfin, sous l'eau."
)
CHARS = "Aniss, Sarah, papa, maman"
SETTING = "école : classe, bac à poisson, évier, bac à sable de la cour"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain d'indigo",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_joyeuse; intensite=1; destinataire=enfant; sous_texte=le_galet_veut_devenir_maison; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tend; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grain d'indigo",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_partent_ensemble; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=Sarah_veut_un_plouf_Aniss_tend; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "grain d'indigo",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=ils_ne_veulent_pas_la_même_chose; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain d'indigo",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=Aniss_tend_Sarah_attend_le_poisson_tourne; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain d'indigo",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_d_indigo_tient_sous_l_eau; tempo=posé; sourire=léger; respiration=ample",
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
    if emphasis and emphasis not in text:
        emphasis = None
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
    "narrateur|Entre deux tics d'horloge, une bulle éclate.",
    "narrateur|Sur le mur, un poisson de craie penche.",
    "narrateur|Le vrai poisson du bac copie la courbe.",
    "papa|Il cherche une maison, Aniss.",
    "maman|Ton galet peint sèche sur le papier.",
    "narrateur|Le papier a bu un anneau bleu, autour.",
    "narrateur|Sur la pierre, un grain d'indigo tient.",
    "enfant-m|Il n'est pas parti dans le papier.",
    "papa|Cette tache, tu l'as vue, là.",
    "narrateur|En ce moment, Aniss serre le galet contre sa chemise.",
    "enfant-m|Je le pose au fond, pour lui.",
    "maman|Avant que le grain fonde dans le papier.",
    "narrateur|Les sandales de Sarah tapent le sol.",
    "copine|Dis plouf !",
    "narrateur|Aniss le tend trop vite, trop tôt.",
    "narrateur|Le galet cogne le bord du bac.",
    "enfant-m|Il ne passe pas.",
    "narrateur|Le sourire d'Aniss disparaît, un instant.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|On prépare, puis on pose.",
    "narrateur|Papa s'accroupit, à la hauteur d'Aniss.",
    "papa|Merci, tu as tenu le galet droit.",
    "maman|L'épuisette et le torchon voyagent aussi.",
    "narrateur|Le poisson recule derrière la plante.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près des pieds.",
    "narrateur|Le galet, l'épuisette, le torchon.",
    "papa|Tu prends quoi d'abord, Aniss ?",
]

T1 = {
    1: {
        "lab": "le galet",
        "sons": "galet,craie",
        "emphasis": "galet",
        "passage": [
            "narrateur|Aniss prend d'abord le galet peint.",
            "enfant-m|Il est froid.",
            "papa|Le bleu tient un peu de craie, au doigt.",
            "narrateur|Il le tend vers Sarah, tout près.",
            "copine|Dis plouf !",
            "narrateur|Aniss ouvre la bouche, puis la referme.",
            "narrateur|Il pose deux doigts sur la pierre.",
            "enfant-m|Pas trop vite.",
            "maman|L'épuisette et le torchon voyagent aussi.",
            "narrateur|Papa glisse le tout contre le galet.",
            "copine|Aniss, on court ?",
            "narrateur|Aniss hoche la tête, un peu.",
            "papa|Le galet d'abord, vous l'avez.",
            "narrateur|Le grain d'indigo reste au sommet.",
        ],
        "question": [
            "narrateur|Aniss a tendu le galet, tout près.",
            "maman|Il tend quoi, à Sarah ?",
        ],
        "qfields": {
            "expected_answer": "galet",
            "accepted_examples": "galet | le galet | le bleu | tendre",
            "retry_prompt": "Il tend le galet. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde le galet contre lui.",
            "copine|Il est à toi, un moment.",
            "narrateur|Sarah attend, les mains ouvertes.",
            "narrateur|Une bulle se fait, minuscule, dans le bac.",
            "maman|Le grain d'indigo est tiède, maintenant.",
            "papa|On pose le galet où ?",
            "copine|Vers le bac, peut-être.",
            "narrateur|L'épuisette et le torchon tapent, à chaque pas.",
        ],
    },
    2: {
        "lab": "l'épuisette",
        "sons": "filet,eau",
        "emphasis": "épuisette",
        "passage": [
            "narrateur|Aniss prend d'abord l'épuisette ronde.",
            "enfant-m|Elle est mouillée.",
            "maman|Le filet sent le bac, un peu.",
            "narrateur|Il tend le manche vers Sarah.",
            "copine|Dis filet !",
            "narrateur|Aniss secoue une goutte, sans un mot.",
            "narrateur|La goutte tombe, puis s'arrête.",
            "papa|Le galet et le torchon voyagent aussi.",
            "narrateur|Maman les pose contre le filet.",
            "copine|Aniss, tu viens ?",
            "narrateur|Aniss lève l'épuisette, sans presser.",
            "enfant-m|Pas trop vite.",
            "maman|L'épuisette d'abord, vous l'avez.",
            "narrateur|Le grain d'indigo écoute le filet.",
        ],
        "question": [
            "narrateur|Aniss a tendu l'épuisette, tout près.",
            "papa|Il tend quoi, à Sarah ?",
        ],
        "qfields": {
            "expected_answer": "épuisette",
            "accepted_examples": "épuisette | l'épuisette | le filet | filet | tendre",
            "retry_prompt": "Il tend l'épuisette. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde l'épuisette contre sa jambe.",
            "copine|Elle est à toi, un moment.",
            "narrateur|Sarah attend, sans répéter.",
            "narrateur|Le filet sent l'eau du bac, un peu.",
            "maman|Le grain d'indigo écoute le filet.",
            "papa|On pose le galet où ?",
            "copine|Vers l'évier, peut-être.",
            "narrateur|Le galet et le torchon tapent, à chaque pas.",
        ],
    },
    3: {
        "lab": "le torchon",
        "sons": "tissu,carreaux",
        "emphasis": "torchon",
        "passage": [
            "narrateur|Aniss prend d'abord le torchon à carreaux.",
            "enfant-m|Il sent le savon.",
            "papa|Le tissu a séché près de l'évier.",
            "narrateur|Il tend le pliage vers Sarah.",
            "copine|Dis essuie !",
            "narrateur|Aniss enroule le galet, sans presser.",
            "narrateur|Le bleu se cache, sans un mot.",
            "maman|Le galet et l'épuisette voyagent aussi.",
            "narrateur|Papa les glisse près des tables.",
            "copine|Aniss, c'est bon ?",
            "narrateur|Aniss appuie sur le tissu, un peu.",
            "enfant-m|Pas trop vite.",
            "papa|Le torchon d'abord, il tient.",
            "narrateur|Le grain d'indigo se tient sous le pli.",
        ],
        "question": [
            "narrateur|Aniss a tendu le torchon, tout près.",
            "maman|Il tend quoi, à Sarah ?",
        ],
        "qfields": {
            "expected_answer": "torchon",
            "accepted_examples": "torchon | le torchon | les carreaux | tendre",
            "retry_prompt": "Il tend le torchon. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss tient le torchon, tout près.",
            "copine|Il est à toi, un moment.",
            "narrateur|Sarah attend, les lèvres fermées.",
            "narrateur|Un carreau bouge un peu, puis s'arrête.",
            "papa|Le grain d'indigo écoute le tissu.",
            "maman|On pose le galet où ?",
            "copine|Vers le sable, tout près.",
            "narrateur|Le galet et l'épuisette tapent, à chaque pas.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le galet tape un peu le verre, à chaque pas.",
        "narrateur|Au bac, le verre est trop haut.",
        "narrateur|À l'évier, l'eau court trop vite.",
        "narrateur|Vers le bac à sable, le bleu se mêle.",
        "papa|On commence où, pour le poisson ?",
    ],
    2: [
        "narrateur|L'épuisette tape un peu la jambe, à chaque pas.",
        "narrateur|Au bac, le verre est trop haut.",
        "narrateur|À l'évier, l'eau court trop vite.",
        "narrateur|Vers le bac à sable, le bleu se mêle.",
        "papa|On commence où, pour le poisson ?",
    ],
    3: [
        "narrateur|Le torchon tape un peu le bras, à chaque pas.",
        "narrateur|Au bac, le verre est trop haut.",
        "narrateur|À l'évier, l'eau court trop vite.",
        "narrateur|Vers le bac à sable, le bleu se mêle.",
        "papa|On commence où, pour le poisson ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "verre,bac",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|Le galet bute contre le verre trop haut.",
            "narrateur|Le bac est trop haut, juste là.",
            "copine|Monte-le, Aniss !",
            "narrateur|Aniss lève les bras, trop vite.",
            "narrateur|Le galet tape le bord, et recule.",
            "enfant-m|Il ne passe pas.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "copine|Dis-moi où !",
            "narrateur|Aniss secoue la tête, un peu.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Sarah se tait, les mains ouvertes.",
            "narrateur|Le poisson se cache derrière la plante.",
            "maman|Il montre le pied du bac, du doigt.",
            "papa|La chaise dort près des tables.",
            "narrateur|Le grain d'indigo a failli glisser.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "filet,verre",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|L'épuisette n'atteint pas l'eau du bac.",
            "narrateur|Le bac est trop haut, juste là.",
            "copine|Monte-la, Aniss !",
            "narrateur|Aniss lève le filet, trop vite.",
            "narrateur|Le manche tape le bord, et recule.",
            "enfant-m|Elle ne passe pas.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "copine|Dis filet, alors !",
            "narrateur|Aniss montre le bas, du doigt.",
            "enfant-m|Plus bas.",
            "narrateur|Sarah se tait, les mains ouvertes.",
            "narrateur|Le poisson se cache derrière la plante.",
            "maman|Il a levé, sans crier.",
            "papa|La chaise dort près des tables.",
            "narrateur|Le grain d'indigo a failli glisser.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "tissu,verre",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|Le torchon glisse sur le bord du bac.",
            "narrateur|Le bac est trop haut, juste là.",
            "copine|Force, Aniss !",
            "narrateur|Aniss pose le tissu au pied du verre.",
            "narrateur|Il le fait glisser, le long du bas.",
            "copine|Dis torchon !",
            "narrateur|Aniss appuie sur le pli, un peu.",
            "enfant-m|Il passe là.",
            "narrateur|Sarah se tait, les lèvres fermées.",
            "narrateur|Le poisson se cache derrière la plante.",
            "maman|Le tissu a cherché l'écart.",
            "papa|La chaise dort près des tables.",
            "narrateur|Le grain d'indigo a failli glisser.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "eau,evier",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|Le galet saute sous l'eau trop vite.",
            "copine|L'eau est trop grande.",
            "narrateur|Sarah veut rincer, pour un plus grand plouf.",
            "copine|Tourne fort, Aniss !",
            "narrateur|Aniss pose la pierre, sans presser.",
            "narrateur|L'eau court, puis rebondit.",
            "enfant-m|Attends l'eau.",
            "narrateur|Sarah referme la bouche.",
            "narrateur|Une peau de savon cache le grain d'indigo.",
            "maman|Le robinet barre le calme.",
            "papa|On reste près de l'évier, tous les deux.",
            "narrateur|Le bleu a failli partir avec l'eau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "filet,savon",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|L'épuisette se remplit trop, d'un coup.",
            "copine|L'eau est trop grande.",
            "narrateur|Sarah veut rincer, pour un plus grand plouf.",
            "copine|Tourne, Aniss !",
            "narrateur|Aniss tient le filet, sans presser.",
            "narrateur|Le savon claque, puis rebondit.",
            "enfant-m|Attends l'eau.",
            "narrateur|Sarah referme la bouche.",
            "narrateur|Une peau de savon cache le grain d'indigo.",
            "maman|Le robinet barre le calme.",
            "papa|On reste près de l'évier, tous les deux.",
            "narrateur|Le filet a failli partir avec l'eau.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "tissu,eau",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|Le torchon se mouille trop, d'un coup.",
            "copine|L'eau est trop grande.",
            "narrateur|Le tissu veut partir avec le savon.",
            "copine|Attrape le pli !",
            "narrateur|Aniss cale le torchon contre le zinc.",
            "narrateur|L'eau frappe, puis recule un peu.",
            "enfant-m|Il reste là.",
            "narrateur|Sarah referme la bouche.",
            "narrateur|Une peau de savon cache le grain d'indigo.",
            "maman|Le robinet barre le calme.",
            "papa|On reste près de l'évier, tous les deux.",
            "narrateur|Le tissu a failli se noyer.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "sable,cour",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|Le galet peint tombe dans le sable beige.",
            "copine|C'est trop mêlé, Aniss !",
            "narrateur|Sarah cherche, trop vite, trop fort.",
            "copine|Dis bleu !",
            "narrateur|Aniss pointe un grain plus foncé, du doigt.",
            "narrateur|Le bac à sable reste trop large.",
            "enfant-m|Pas trop fort.",
            "narrateur|Sarah se tait, les joues chaudes.",
            "narrateur|Un caillou beige imite le galet, trop clair.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|Le tamis dort près du seau.",
            "narrateur|Le grain d'indigo s'est perdu sous le sable.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "filet,sable",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|L'épuisette ramasse trop de grains, d'un coup.",
            "copine|C'est trop mêlé, Aniss !",
            "narrateur|Sarah cherche, trop vite, trop fort.",
            "copine|Dis filet !",
            "narrateur|Aniss secoue le filet, sans presser.",
            "narrateur|Le sable reste collé, trop lourd.",
            "enfant-m|Le tamis.",
            "narrateur|Sarah se tait, les joues dégonflées.",
            "narrateur|Un caillou beige imite le galet, trop clair.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|Le tamis dort près du seau.",
            "narrateur|Le grain d'indigo s'est perdu sous le sable.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "tissu,sable",
        "emphasis": "grain d'indigo",
        "passage": [
            "narrateur|Le torchon se charge de sable chaud.",
            "copine|C'est trop mêlé, Aniss !",
            "narrateur|Sarah cherche, trop vite, trop fort.",
            "copine|Dis torchon !",
            "narrateur|Aniss pose le tissu sur le seau.",
            "narrateur|Le pli ne bouge plus, trop bas.",
            "enfant-m|Plus haut.",
            "narrateur|Sarah se tait, les joues dégonflées.",
            "narrateur|Un caillou beige imite le galet, trop clair.",
            "maman|Tes yeux vont plus loin, Aniss.",
            "papa|Le tamis dort près du seau.",
            "narrateur|Le grain d'indigo s'est perdu sous le sable.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("la chaise", "les mains de Sarah", "le marchepied"),
    2: ("l'eau", "l'épuisette", "le robinet"),
    3: ("le tamis", "les mains de Sarah", "le seau"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le verre reste trop haut, trop loin.",
        "narrateur|Le poisson se cache derrière la plante.",
        "papa|La chaise, les mains, ou le marchepied ?",
    ],
    2: [
        "narrateur|L'eau tient le savon.",
        "narrateur|Le grain d'indigo s'est caché sous la peau.",
        "maman|L'eau, l'épuisette, ou le robinet ?",
    ],
    3: [
        "narrateur|Le sable reste trop mêlé, trop large.",
        "narrateur|Le grain d'indigo s'est perdu sous le beige.",
        "papa|Le tamis, les mains, ou le seau ?",
    ],
}

T3_SONS = {
    (1, 1): "chaise,verre",
    (1, 2): "mains,galet",
    (1, 3): "marchepied,bois",
    (2, 1): "eau,evier",
    (2, 2): "filet,mains",
    (2, 3): "robinet,zinc",
    (3, 1): "tamis,sable",
    (3, 2): "mains,sable",
    (3, 3): "seau,cour",
}

T3_EMPH = {
    1: {1: "chaise", 2: "mains", 3: "marchepied"},
    2: {1: "eau", 2: "épuisette", 3: "robinet"},
    3: {1: "tamis", 2: "mains", 3: "seau"},
}

OBJ_LINE = {
    1: "Le galet attend, collé aux doigts.",
    2: "L'épuisette attend, autour du bleu.",
    3: "Le torchon attend, contre la pierre.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    obj = OBJ_LINE[a]
    if b == 1 and c == 1:
        wait = {
            1: "Le galet reste près du dossier.",
            2: "L'épuisette reste près du dossier.",
            3: "Le torchon reste près du dossier.",
        }[a]
        return [
            "copine|On attend.",
            "narrateur|Aniss tire la chaise, sans presser.",
            "narrateur|Sarah tient le dossier, un peu.",
            f"narrateur|{wait}",
            "narrateur|Aniss monte vers le bac, sans un mot.",
            "narrateur|Ça fait toc, tout net, contre le verre.",
            "copine|Toc.",
            "narrateur|Le grain d'indigo revoit l'eau, rond.",
            f"narrateur|{obj}",
            "papa|La chaise n'est plus trop basse.",
            "enfant-m|La chaise.",
        ]
    if b == 1 and c == 2:
        hold = {
            1: "Le galet glisse vers les mains de Sarah.",
            2: "L'épuisette guide la pierre vers Sarah.",
            3: "Le torchon suit la pierre vers Sarah.",
        }[a]
        return [
            "copine|Pour toi.",
            "narrateur|Sarah ouvre les deux mains, tout près.",
            "narrateur|Aniss pose le bleu contre ses paumes.",
            f"narrateur|{hold}",
            "narrateur|Sarah vise le bord, Aniss pousse le galet.",
            "copine|Il passe !",
            "narrateur|Le grain d'indigo échappe au verre, rond.",
            f"narrateur|{obj}",
            "maman|Tes mains ont trouvé le bleu.",
            "papa|Il l'a tendu, d'abord.",
            "enfant-m|Tes mains.",
        ]
    if b == 1 and c == 3:
        step = {
            1: "Le galet attend sur le marchepied.",
            2: "L'épuisette attend sur le marchepied.",
            3: "Le torchon attend sur le marchepied.",
        }[a]
        return [
            "copine|Le marchepied, Aniss.",
            "narrateur|Aniss pose le bleu dessus, sans un mot.",
            "narrateur|Sarah attend, puis suit sa main.",
            f"narrateur|{step}",
            "narrateur|Ils le poussent, ensuite, vers le bac.",
            "copine|Il tient.",
            "narrateur|Le grain d'indigo reprend le rai, petit.",
            f"narrateur|{obj}",
            "papa|Le bois a gardé le calme.",
            "maman|La chaise peut dormir, plus loin.",
            "enfant-m|Le marchepied.",
        ]
    if b == 2 and c == 1:
        water = {
            1: "Le galet attend au calme, contre l'évier.",
            2: "L'épuisette retombe, contre l'évier.",
            3: "Le torchon retombe, contre l'évier.",
        }[a]
        return [
            "copine|On attend l'eau.",
            "narrateur|Aniss s'assoit près de l'évier, sans presser.",
            "narrateur|Sarah s'assoit aussi, les genoux contre lui.",
            f"narrateur|{water}",
            "narrateur|L'eau tombe, une bulle s'arrête.",
            "copine|Maintenant.",
            "narrateur|Le grain d'indigo sèche, rond, contre le zinc.",
            f"narrateur|{obj}",
            "papa|Le robinet ne chante plus.",
            "maman|Vous avez laissé l'eau finir.",
            "enfant-m|L'eau.",
        ]
    if b == 2 and c == 2:
        net = {
            1: "Le galet descend au bout du filet.",
            2: "L'épuisette part au bout des mains de Sarah.",
            3: "Le torchon guide le filet, tout droit.",
        }[a]
        return [
            "copine|Tes mains, Aniss.",
            "narrateur|Aniss tend l'épuisette, tout près.",
            "narrateur|Sarah tire avec lui, sans presser.",
            f"narrateur|{net}",
            "narrateur|Le filet traverse comme un pont.",
            "copine|On tient ensemble.",
            "narrateur|Le grain d'indigo tremble au bout du filet.",
            f"narrateur|{obj}",
            "maman|Vos mains suffisent, toutes les deux.",
            "papa|L'eau restera après.",
            "enfant-m|On tient.",
        ]
    if b == 2 and c == 3:
        tap = {
            1: "Le galet passe, dès que l'eau se tait.",
            2: "L'épuisette se libère, dès que l'eau se tait.",
            3: "Le torchon se libère, dès que l'eau se tait.",
        }[a]
        return [
            "copine|Le robinet, d'abord.",
            "narrateur|Sarah tend la poignée vers Aniss.",
            "narrateur|Aniss tourne, sans un mot.",
            f"narrateur|{tap}",
            "narrateur|Une goutte rejoint le fond, sans bruit.",
            "copine|C'est plus simple.",
            "narrateur|Le grain d'indigo reste au sec, sur le bleu.",
            f"narrateur|{obj}",
            "maman|L'eau garde son souffle, plus loin.",
            "papa|Le robinet a laissé le filet.",
            "enfant-m|Au sec.",
        ]
    if b == 3 and c == 1:
        sieve = {
            1: "Le galet monte avec le tamis.",
            2: "L'épuisette monte avec le tamis.",
            3: "Le torchon monte avec le tamis.",
        }[a]
        return [
            "copine|Le tamis, dessous.",
            "papa|Je vous le tends, à votre hauteur.",
            "narrateur|Aniss secoue, Sarah tend le bleu.",
            f"narrateur|{sieve}",
            "narrateur|Aniss souffle le sable, sans parler.",
            "copine|Ça tient !",
            "narrateur|Le grain d'indigo file hors du beige, rond.",
            f"narrateur|{obj}",
            "papa|Le métal a tenu le tamis.",
            "maman|Aniss a poussé, sans crier.",
            "enfant-m|Le tamis.",
        ]
    if b == 3 and c == 2:
        hands = {
            1: "Le galet part au bout des mains de Sarah.",
            2: "L'épuisette part au bout des mains de Sarah.",
            3: "Le torchon part au bout des mains de Sarah.",
        }[a]
        return [
            "enfant-m|Sarah.",
            "narrateur|Aniss pointe ses paumes, du doigt.",
            "narrateur|Sarah attend, puis ouvre les mains.",
            f"narrateur|{hands}",
            "narrateur|Le bleu glisse, tout net, vers elle.",
            "copine|Je le tiens.",
            "narrateur|Le grain d'indigo prend l'air, dans ses paumes.",
            f"narrateur|{obj}",
            "maman|Le sable garde son ombre, plus loin.",
            "papa|Tes mains ont guidé le galet.",
            "enfant-m|Tes mains.",
        ]
    bucket = {
        1: "Le galet suit le seau, grain après grain.",
        2: "L'épuisette court le long du seau, au calme.",
        3: "Le torchon tient derrière le seau, tout droit.",
    }[a]
    return [
        "copine|Le seau, Aniss.",
        "narrateur|Aniss pointe le fond, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        f"narrateur|{bucket}",
        "narrateur|Le bleu prend le chemin du calme.",
        "copine|Il évite le beige.",
        "narrateur|Le grain d'indigo veille derrière le seau.",
        f"narrateur|{obj}",
        "papa|Le seau a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
        "enfant-m|Le seau.",
    ]


LAST = {
    (1, 1, 1): "Le grain d'indigo s'endort contre le verre.",
    (1, 1, 2): "Dans les paumes, le grain d'indigo clignote.",
    (1, 1, 3): "Sur le marchepied, le grain d'indigo se tait.",
    (1, 2, 1): "Au calme de l'évier, le grain d'indigo sèche.",
    (1, 2, 2): "Au bout du filet, le grain d'indigo tremble.",
    (1, 2, 3): "Près du robinet, le grain d'indigo se tait.",
    (1, 3, 1): "Sur le tamis, le grain d'indigo prend l'air.",
    (1, 3, 2): "Dans les mains de Sarah, le grain d'indigo veille.",
    (1, 3, 3): "Le long du seau, le grain d'indigo file.",
    (2, 1, 1): "L'épuisette laisse le grain d'indigo au bac.",
    (2, 1, 2): "Les mains de Sarah chauffent le grain d'indigo.",
    (2, 1, 3): "Le marchepied tient le grain d'indigo, petit.",
    (2, 2, 1): "L'eau n'a pas pris le grain d'indigo.",
    (2, 2, 2): "Le filet tendu montre le grain d'indigo au poisson.",
    (2, 2, 3): "Le robinet a sauvé le grain d'indigo, tiède.",
    (2, 3, 1): "Le tamis lèche le grain d'indigo, au métal.",
    (2, 3, 2): "Les paumes tiennent le grain d'indigo, droit.",
    (2, 3, 3): "Le seau serre près du grain d'indigo.",
    (3, 1, 1): "Le torchon cale le grain d'indigo au bac.",
    (3, 1, 2): "Le tissu suit le grain d'indigo vers Sarah.",
    (3, 1, 3): "Le marchepied pince le grain d'indigo, sans le cacher.",
    (3, 2, 1): "L'évier a séché le grain d'indigo.",
    (3, 2, 2): "Le torchon guide le grain d'indigo au-dessus de l'eau.",
    (3, 2, 3): "Le robinet laisse le grain d'indigo au sec.",
    (3, 3, 1): "Le tamis pousse le grain d'indigo, hors du sable.",
    (3, 3, 2): "Deux mains s'arrêtent, le grain d'indigo au milieu.",
    (3, 3, 3): "Le bleu tremble, le grain d'indigo se tait.",
}

HARD = {
    (1, 1): "Le verre a failli garder le galet.",
    (2, 1): "L'épuisette a failli rester trop basse.",
    (3, 1): "Le torchon a failli glisser du bord.",
    (1, 2): "L'eau a failli emporter le bleu.",
    (2, 2): "Le filet a failli partir avec le savon.",
    (3, 2): "Le torchon a failli se noyer trop fort.",
    (1, 3): "Le sable a failli trop mêler le bleu.",
    (2, 3): "L'épuisette a failli ramasser trop de grains.",
    (3, 3): "Le torchon a failli se charger de sable.",
}

CODA = {
    1: "Le bleu garde une goutte, au fond.",
    2: "L'épuisette sent l'eau tiède, un peu.",
    3: "Un carreau de torchon reste humide.",
}

TRACE = {
    (1, 1): "Une goutte tiède reste sur le verre.",
    (1, 2): "À l'évier, ça sent le savon, tiède.",
    (1, 3): "Au loin, le poisson se tait.",
    (2, 1): "Un filet mouillé tremble, puis se tait.",
    (2, 2): "Une bulle sèche, contre le zinc.",
    (2, 3): "Sur le sol, une ombre mince.",
    (3, 1): "Un carreau de torchon reste tiède, dans la paume.",
    (3, 2): "Un tic d'horloge s'éteint, tout près.",
    (3, 3): "L'ombre de la plante recule, un peu.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    last = LAST[(a, b, c)]
    hard = HARD[(a, b)]
    coda = CODA[a]
    trace = TRACE[(a, c)]
    if b == 1 and c == 1:
        return [
            "narrateur|Le galet pose une bulle sur le verre.",
            "enfant-m|Poisson.",
            "copine|Il est arrivé.",
            f"narrateur|{hard}",
            "papa|La chaise a laissé le passage.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 2:
        return [
            "narrateur|Le bleu a contourné le verre, jusqu'au fond.",
            "copine|Aniss l'a tendu, tout seul.",
            "papa|Tu as tendu, d'abord.",
            f"narrateur|{hard}",
            "maman|Venez, le poisson est calme.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 3:
        return [
            "narrateur|Le bleu court jusqu'au fond, tout droit.",
            "copine|On a posé le galet.",
            "papa|Le marchepied a tenu, tout droit.",
            f"narrateur|{hard}",
            "maman|Essuyez vos mains, tout près.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 1:
        return [
            "narrateur|Le bleu rejoint le bac, un peu mouillé.",
            "copine|On a attendu l'eau.",
            "papa|Le savon n'a plus pris vos bras.",
            f"narrateur|{hard}",
            "maman|Rentrez le torchon, après le bac.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 2:
        return [
            "narrateur|Le filet pose le galet au fond du bac.",
            "copine|On tenait, tous les deux.",
            "papa|Je remporte l'épuisette, tout à l'heure.",
            f"narrateur|{hard}",
            "maman|Le poisson vous attend.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 3:
        return [
            "narrateur|Les mains d'Aniss laissent le bleu au fond.",
            "copine|C'était plus facile, là.",
            "papa|Tes bras ont guidé le galet.",
            f"narrateur|{hard}",
            "maman|Le fond gardera son ombre.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 1:
        return [
            "narrateur|Le bleu rejoint le bac, tout propre.",
            "copine|On a trouvé, Aniss.",
            "papa|Le tamis n'a pas glissé.",
            f"narrateur|{hard}",
            "maman|Rentrez, le seuil est sec.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 2:
        return [
            "narrateur|Les mains de Sarah laissent le bleu au fond.",
            "copine|On l'a tenu, tous les deux.",
            "papa|Le sable est resté à sa place.",
            f"narrateur|{hard}",
            "maman|Essuie tes chaussures, Aniss.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    return [
        "narrateur|Le bleu suit le seau, jusqu'au bac.",
        "copine|L'ombre était nette.",
        "papa|Le seau a tenu, tout droit.",
        f"narrateur|{hard}",
        "maman|Le sable n'a plus rien à dire.",
        f"narrateur|{coda}",
        f"narrateur|{trace}",
        f"narrateur|{last}",
    ]


END_SONS = {1: "eau,verre", 2: "filet,zinc", 3: "sable,cour"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "horloge,bulle,bac",
        {"emphasis": "grain d'indigo"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le galet", "l'épuisette", "le torchon"), "pause_before": 200},
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
            {"emphasis": "grain d'indigo"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le bac", "l'évier", "le bac à sable"), "pause_before": 200},
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
                    {"emphasis": "grain d'indigo"},
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
        "noé",
        "noe ",
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
        "j'ai compris",
        "mission accomplie",
        "on dirait que notre mission",
        "il faut attendre",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "virgule d'or",
        "croissant de buée",
        "fil blanc",
        "perle de verre",
        "cran en croissant",
        "œillet de cuivre",
        "oeillet de cuivre",
        "virgule de farine",
        "marque fine",
        "ombre en forme de flèche",
        "minuscule symbole",
        "pastille de colle",
        "goutte de cire",
        "larme de bronze",
        "bouton de nacre",
        "nœud de raphia",
        "grain de savon",
        "grain de vanille",
        "grain de son",
        "bouton de lavande",
        "grain doré",
        "brin de safran",
        "anneau de liège",
        "clou à tête ronde",
        "grain d'ambre",
        "anneau de zinc",
        "point de cire",
        "bracelet d'écorce",
        "boucle d'étain",
        "anneau de pollen",
        "dent de laitue",
        "éclat de zinc",
        "éclat de thym",
        "lune d'étain",
        "grain de grenat",
        "soleil en papier",
        "maîtresse",
        "jardinier",
        "grand-père",
        "camarade",
        "parle peu",
        "parlé peu",
        "forcer la parole",
        "vis verte",
        "petite roue",
        "poissons de papier",
        "panier d'osier",
        "cuisine",
        "la chambre",
        "le jardin",
        "dînette",
        "dinette",
        "capitaine",
        "plic",
        "volet jaune",
        "locomotive",
        "cuillère",
        "véranda",
        "jules",
        "zoé",
        "zoe",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "grain d'indigo" not in blob:
        raise SystemExit(f"{SID}: indice grain d'indigo absent")
    if "enfant-m|" not in blob:
        raise SystemExit(f"{SID}: enfant-m absent")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: copine absente")
    if blob.count("merci") > 3:
        raise SystemExit(f"{SID}: merci refrain ×{blob.count('merci')}")

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
        if "grain d'indigo" not in low:
            raise SystemExit(f"fin sans grain d'indigo: {last_n[-1]}")
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
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-045 — Le galet peint d'Aniss et le poisson de la classe\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — laisser l'autre poser sa limite / prendre son tour "
        "(vécue, jamais dite : on ne force ni Sarah ni le poisson)\n"
        "- **Personnages :** Aniss, Sarah, papa, maman\n"
        "- **Lieu :** école : classe, bac à poisson, évier, bac à sable de la cour\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Entre deux tics d'horloge, une bulle éclate. Un poisson de craie penche au mur ; "
        "le vrai poisson copie la courbe. Aniss serre son galet peint : un grain d'indigo "
        "tient, le papier a bu le reste. Il veut le poser au fond du bac, pour le poisson, "
        "avant que le grain fonde. Sarah veut un plouf. Aniss tend trop vite : le galet "
        "cogne le bord. Sourire parti. Galet, épuisette, torchon : les trois partent. "
        "Bac (verre trop haut, poisson caché), évier (eau trop vite, peau de savon), "
        "bac à sable (bleu mêlé, caillou beige). Chaise, mains de Sarah, marchepied ; "
        "eau, épuisette, robinet ; tamis, mains de Sarah, seau. "
        "Le grain d'indigo tient sous l'eau, avec une trace.\n\n"
        "## Vécu\n\n"
        "Aniss veut le galet **au fond du bac, maintenant**. Sarah ne veut pas "
        "la même chose : elle veut un plouf. Première idée : tendre trop vite. "
        "Ça rate. Chaque choix change l'obstacle et le climax (verre, savon, beige). "
        "La leçon se voit : Aniss tend, Sarah attend, le silence compte. "
        "On ne force pas la parole, on ne force pas le poisson, on change le geste. "
        "Fin : grain d'indigo + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Noé / Tom / Léa / Sami / Jules / cuisine-jardin-chambre / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Aniss (`enfant-m`), Sarah (`copine`), rythmes distincts, silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique : grain d'indigo (ouverture + climax). "
        "Pas d'ancre / étoile / fil pâle / marque fine / goutte de cire / larme de bronze.\n"
        "- Ouverture inventée : tics d'horloge, bulle, poisson de craie, puis le grain.\n"
        "- Corps : sourire parti ; envie et inquiétude ; papa s'accroupit.\n"
        "- Merci vécu (ouverture). Question d'adulte. Un « en ce moment ».\n"
        "- Monde ≠ TREE-DIF-037 (pas de panier, petite roue, vis verte). "
        "≠ TREE-DIF-049 (pas de poissons de papier, tapis).\n"
        "- Adultes = papa/maman. Pas de maîtresse.\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {min(counts)} à {max(counts)} mots par chemin (moyenne {sum(counts)//len(counts)})\n"
        "- `text` = `script` collé ; graphe inchangé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
