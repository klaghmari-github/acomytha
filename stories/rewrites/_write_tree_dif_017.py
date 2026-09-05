#!/usr/bin/env python3
"""TREE-DIF-017 — La locomotive de Nino et la gare en carton (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-017"
N2 = 15
TITLE = "La locomotive de Nino et la gare en carton"
FIL = (
    "Nino veut que sa locomotive de bois arrive sous le grain d'ocre, "
    "sur la gare en carton, avant que le sac d'Aniss reparte. "
    "Aniss commence un mot ; le mot s'arrête. Nino propose, Aniss pose sa limite. "
    "T1 = locomotive / rails / drapeau, les trois partent. "
    "T2 = couloir (chaussure, trou) / salon (tapis) / terrasse (flaque, vent). "
    "T3 = neuf façons d'arriver. Nino refuse de foncer. Le grain d'ocre paie le stop."
)
CHARS = "Nino, Aniss, papa, maman"
SETTING = "couloir, salon, terrasse, gare en carton"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain d'ocre",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_mot_d_Aniss_s_arrête_Nino_veut_partir; tempo=naturel; sourire=léger; respiration=ample",
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
        "emphasis": "locomotive",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté_le_mot_manque; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=Nino_propose_Aniss_prend_son_temps; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_silence_d_Aniss_est_une_réponse; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain d'ocre",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=laisser_l_autre_poser_sa_limite; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain d'ocre",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_d_ocre_paie_le_début_Aniss_finit_son_mot; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Nino est à genoux, sur les carreaux tièdes.",
    "narrateur|Il compte les fenêtres de la boîte.",
    "enfant-m|Une, deux, trois, quatre.",
    "narrateur|Les ciseaux de papa font crac dans le carton.",
    "narrateur|Ça sent le carton coupé, un peu sec.",
    "narrateur|Sur le toit, un grain d'ocre, minuscule.",
    "enfant-m|C'est le stop, papa.",
    "papa|Le grain d'ocre, sur le carton ?",
    "enfant-m|Le train s'arrête dessous.",
    "maman|Aniss arrive, son sac frotte le sol.",
    "narrateur|La sonnette tinte, une fois.",
    "copain|On va ?",
    "enfant-m|On part, Aniss !",
    "enfant-m|Dis go !",
    "narrateur|Aniss referme la bouche, sans un mot.",
    "narrateur|Il pose deux doigts sur une roue.",
    "narrateur|En ce moment, Nino serre la locomotive.",
    "narrateur|Son sourire vacille, un peu.",
    "papa|Tu peux lui tendre quelque chose.",
    "maman|Merci, tu as laissé la roue à Aniss.",
    "papa|Le sac reste près de la porte.",
]

T1_CHOICE = [
    "narrateur|Le panier reste ouvert, près des pieds.",
    "narrateur|La locomotive, les rails, et le drapeau rouge.",
    "papa|Tu prends quoi d'abord, Nino ?",
]

T1 = {
    1: {
        "lab": "la locomotive",
        "sons": "bois,roue",
        "emphasis": "locomotive",
        "passage": [
            "narrateur|Nino prend la locomotive de bois, d'abord.",
            "enfant-m|Elle sent le bois, un peu rêche.",
            "papa|Le toit est rêche, sous le doigt.",
            "narrateur|Il la tend vers Aniss, tout près.",
            "enfant-m|Dis vroom, Aniss !",
            "copain|Vrr.",
            "narrateur|Le mot s'arrête, trop court.",
            "narrateur|Aniss pose deux doigts sur une roue.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "maman|Les rails et le drapeau viennent aussi.",
            "narrateur|Papa glisse le tout dans le panier.",
            "enfant-m|Aniss, on part ?",
            "narrateur|Aniss hoche la tête, tout petit.",
            "papa|La locomotive d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Nino a tendu la locomotive, tout près.",
            "maman|Il tend quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "la locomotive",
            "accepted_examples": "locomotive | la locomotive | le train | le jouet | tendre",
            "retry_prompt": "Il tend la locomotive. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss prend la locomotive contre lui.",
            "enfant-m|Elle est à toi, un moment.",
            "narrateur|Nino attend, les mains ouvertes.",
            "narrateur|Une roue fait un tout petit clic.",
            "maman|Le bois est tiède, sous ses doigts.",
            "papa|On pose la ligne où ?",
            "enfant-m|Jusqu'à la gare, sous le grain d'ocre.",
            "copain|Le train ?",
            "narrateur|Le mot d'Aniss s'arrête, trop court.",
        ],
    },
    2: {
        "lab": "les rails",
        "sons": "bois,clic",
        "emphasis": "rails",
        "passage": [
            "narrateur|Nino prend deux rails de bois, d'abord.",
            "enfant-m|Ça fait clic.",
            "papa|Un clic, puis un autre clic.",
            "narrateur|Il tend un rail vers Aniss.",
            "enfant-m|Dis clic, Aniss !",
            "copain|Cli.",
            "narrateur|Le son s'arrête, trop court.",
            "narrateur|Aniss aligne les deux bouts, tout droit.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Je me baisse, à votre hauteur.",
            "papa|La locomotive et le drapeau viennent aussi.",
            "narrateur|Maman les pose près du panier.",
            "enfant-m|Aniss, c'est bon ?",
            "narrateur|Aniss appuie sur le rail, sans un mot.",
            "papa|Les rails d'abord, ils tiennent.",
        ],
        "question": [
            "narrateur|Nino a tendu un rail, tout près.",
            "papa|Il tend quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "un rail",
            "accepted_examples": "rail | un rail | les rails | le bois | tendre",
            "retry_prompt": "Il tend un rail. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde le rail contre sa jambe.",
            "enfant-m|Il est à toi, un moment.",
            "narrateur|Nino reste là, sans répéter le mot.",
            "narrateur|Le bois sent le grenier, un peu.",
            "maman|La ligne peut grandir, après.",
            "papa|On pose la ligne où ?",
            "enfant-m|Jusqu'à la gare, sous le grain d'ocre.",
            "copain|Le rail ?",
            "narrateur|Aniss s'arrête, la bouche ouverte.",
        ],
    },
    3: {
        "lab": "le drapeau",
        "sons": "tissu,bois",
        "emphasis": "drapeau",
        "passage": [
            "narrateur|Nino prend le drapeau rouge, d'abord.",
            "enfant-m|C'est pour la gare.",
            "maman|Le tissu est un peu rêche.",
            "narrateur|Il tend le bâton vers Aniss.",
            "enfant-m|Dis gare, Aniss !",
            "copain|Ga.",
            "narrateur|Le mot s'arrête, trop court.",
            "narrateur|Aniss tient le bâton à deux mains.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je me mets à genoux, près de vous.",
            "maman|La locomotive et les rails viennent aussi.",
            "narrateur|Papa les glisse près du sac.",
            "enfant-m|Aniss, tu viens ?",
            "narrateur|Aniss lève le drapeau, tout bas.",
            "maman|Le drapeau d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Nino a tendu le drapeau, tout près.",
            "maman|Il tend quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "le drapeau",
            "accepted_examples": "drapeau | le drapeau | le rouge | le bâton | tendre",
            "retry_prompt": "Il tend le drapeau. Il tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss tient le drapeau, tout près.",
            "enfant-m|Il est à toi, un moment.",
            "narrateur|Nino ferme les lèvres, cette fois.",
            "narrateur|Le rouge bouge un peu, puis s'arrête.",
            "papa|La gare va le voir, plus tard.",
            "maman|On pose la ligne où ?",
            "enfant-m|Jusqu'à la boîte, sous le grain d'ocre.",
            "copain|Le stop ?",
            "narrateur|Le silence d'Aniss reste une réponse.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Dans le panier, la locomotive voyage.",
        "narrateur|Des carreaux tièdes, au couloir.",
        "narrateur|Un tapis épais, au salon.",
        "narrateur|Une flaque ronde, à la terrasse.",
        "papa|On commence où, pour la gare ?",
    ],
    2: [
        "narrateur|Dans le panier, les rails voyagent.",
        "narrateur|Des carreaux tièdes, au couloir.",
        "narrateur|Un tapis épais, au salon.",
        "narrateur|Une flaque ronde, à la terrasse.",
        "papa|On commence où, pour la ligne ?",
    ],
    3: [
        "narrateur|Dans le panier, le drapeau voyage.",
        "narrateur|Des carreaux tièdes, au couloir.",
        "narrateur|Un tapis épais, au salon.",
        "narrateur|Une flaque ronde, à la terrasse.",
        "maman|On commence où, pour le stop ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "carreau,chaussure",
        "emphasis": "chaussure",
        "passage": [
            "narrateur|La locomotive tape un peu le carreau.",
            "narrateur|Ils portent la gare, le grain d'ocre en haut.",
            "narrateur|Une chaussure de papa barre le passage.",
            "enfant-m|Pousse-la, Aniss !",
            "narrateur|Aniss pointe un trou, entre deux rails.",
            "narrateur|Un bout de ligne manque, juste là.",
            "enfant-m|Dis-moi où !",
            "maman|Il montre, avec le doigt.",
            "papa|La chaussure reste lourde, au milieu.",
            "narrateur|Le sourire de Nino s'en va.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il écoute les carreaux, puis le carton.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "carreau,bois",
        "emphasis": "rail",
        "passage": [
            "narrateur|Un rail frotte le carreau, tout sec.",
            "narrateur|Le grain d'ocre tremble un peu, sur le toit.",
            "narrateur|La chaussure avale le bout d'un rail.",
            "enfant-m|Tire-le, Aniss !",
            "narrateur|Aniss secoue la tête, une fois.",
            "narrateur|Il montre le trou, plus loin.",
            "enfant-m|Parle, vas-y !",
            "papa|Son doigt a parlé, Nino.",
            "maman|Le trou attend un autre bois.",
            "narrateur|Nino sent ses épaules se crisper.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il regarde le toit, puis le trou.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "tissu,carreau",
        "emphasis": "lacet",
        "passage": [
            "narrateur|Le drapeau frôle le mur du couloir.",
            "narrateur|Le grain d'ocre passe sous la lumière.",
            "narrateur|Un lacet attrape le tissu rouge.",
            "enfant-m|Dégage, Aniss !",
            "narrateur|Aniss pose la paume, stop.",
            "narrateur|Le rouge s'arrête contre le cuir.",
            "enfant-m|On pousse ensemble, vite !",
            "maman|Sa main dit non, pour l'instant.",
            "papa|Le lacet tient le bâton.",
            "narrateur|Nino ne rit plus.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il écoute le silence, puis le carton.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "tapis,roue",
        "emphasis": "tapis",
        "passage": [
            "narrateur|La locomotive s'enfonce dans le tapis.",
            "narrateur|Le grain d'ocre penche, sur le toit mou.",
            "enfant-m|Le tapis est trop mou.",
            "narrateur|Les roues s'enfoncent, puis s'arrêtent.",
            "enfant-m|Pousse, Aniss !",
            "narrateur|Aniss pose la paume sur le toit.",
            "narrateur|Le train ne bouge presque plus.",
            "maman|Le tapis avale les petites roues.",
            "papa|Le parquet, plus loin, est lisse.",
            "narrateur|Un livre épais dort sous la table.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "tapis,bois",
        "emphasis": "livre",
        "passage": [
            "narrateur|Un rail disparaît un peu dans le tapis.",
            "narrateur|Le grain d'ocre se cache, vu d'ici.",
            "enfant-m|Ils s'enfoncent !",
            "narrateur|Aniss ramène le rail, sans un mot.",
            "enfant-m|Pousse plus fort !",
            "narrateur|Aniss secoue la tête, les lèvres serrées.",
            "maman|Le tapis a trop de poils, ici.",
            "papa|Une planche dort derrière le canapé.",
            "narrateur|Le livre épais reste sous la table.",
            "narrateur|Le sourire de Nino s'en va.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il écoute le tapis, puis le carton.",
            "maman|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "tapis,tissu",
        "emphasis": "planche",
        "passage": [
            "narrateur|Le drapeau traîne sur le tapis, trop mou.",
            "narrateur|Le grain d'ocre penche vers le tissu.",
            "enfant-m|Il s'accroche partout !",
            "narrateur|Aniss ramasse le rouge, tout bas.",
            "enfant-m|On tire, allez !",
            "narrateur|Aniss garde le bâton, sans bouger.",
            "papa|Le parquet luit, près de la vitre.",
            "maman|La planche peut faire un pont.",
            "narrateur|Nino sent son corps se crisper.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il observe le drapeau, écoute le salon.",
            "narrateur|Personne ne donne la réponse.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "vent,eau",
        "emphasis": "flaque",
        "passage": [
            "narrateur|La locomotive sent le vent, tout de suite.",
            "narrateur|Le grain d'ocre tremble au bord du toit.",
            "enfant-m|La flaque est trop grande.",
            "narrateur|Le vent secoue le carton de la gare.",
            "enfant-m|Aniss, on court ?",
            "narrateur|Aniss recule d'un pas, près du seuil.",
            "narrateur|Une goutte brille sur le toit, trop près.",
            "maman|Le carton n'aime pas l'eau.",
            "papa|Le vent tient le drapeau, trop fort.",
            "narrateur|Le sourire de Nino s'en va.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il écoute le vent, puis le carton.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "vent,pierre",
        "emphasis": "vent",
        "passage": [
            "narrateur|Les rails cliquent au vent, sur la pierre.",
            "narrateur|Le grain d'ocre penche vers la flaque.",
            "enfant-m|Ça va tomber !",
            "narrateur|Aniss couvre les rails, des deux mains.",
            "enfant-m|On pose près de l'eau, vite !",
            "narrateur|Aniss recule, et les rails reculent.",
            "maman|L'eau ferait fondre le carton.",
            "papa|Le vent pousse, puis se tait un peu.",
            "narrateur|Nino ouvre la bouche, puis la referme.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il observe les rails, écoute la pierre.",
            "narrateur|Personne ne donne la réponse.",
            "maman|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "vent,tissu",
        "emphasis": "drapeau",
        "passage": [
            "narrateur|Le drapeau claque une fois, trop fort.",
            "narrateur|Le grain d'ocre manque de glisser.",
            "enfant-m|Il va s'envoler !",
            "narrateur|Aniss plaque le tissu contre sa poitrine.",
            "enfant-m|On court jusqu'au bord !",
            "narrateur|Aniss secoue la tête, le dos au vent.",
            "papa|Le vent tient le rouge, trop fort.",
            "maman|La flaque lèche les dalles, tout près.",
            "narrateur|Nino sent l'inquiétude dans sa poitrine.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il écoute le claquement, puis le carton.",
            "narrateur|Le silence d'Aniss pèse, utile.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("le rail", "la locomotive", "la chaussure"),
    2: ("le livre", "la planche", "le parquet"),
    3: ("le vent", "la gare", "le drapeau"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le trou entre les rails reste ouvert.",
        "papa|Le rail, la locomotive, ou la chaussure ?",
    ],
    2: [
        "narrateur|Les roues restent prises dans le tapis.",
        "maman|Le livre, la planche, ou le parquet ?",
    ],
    3: [
        "narrateur|La flaque barre le chemin, trop large.",
        "papa|Le vent, la gare, ou le drapeau ?",
    ],
}

T3_SONS = {
    (1, 1): "sac,clic",
    (1, 2): "bois,cuir",
    (1, 3): "chaussure,lacet",
    (2, 1): "livre,roue",
    (2, 2): "planche,bois",
    (2, 3): "parquet,clic",
    (3, 1): "vent,carton",
    (3, 2): "carton,pas",
    (3, 3): "tissu,vent",
}

def pose(a: int, key: str) -> str:
    table = {
        "trou": (
            "La locomotive attend près du trou.",
            "Les rails attendent près du trou.",
            "Le drapeau attend près du trou.",
        ),
        "guide": (
            "Aniss guide la locomotive, autour du cuir.",
            "Aniss guide les rails, autour du cuir.",
            "Aniss guide le drapeau, autour du cuir.",
        ),
        "bord": (
            "La locomotive reste un instant sur le bord.",
            "Les rails restent un instant sur le bord.",
            "Le drapeau reste un instant sur le bord.",
        ),
        "poussent": (
            "La locomotive attend pendant qu'ils poussent.",
            "Les rails attendent pendant qu'ils poussent.",
            "Le drapeau attend pendant qu'ils poussent.",
        ),
        "livre": (
            "La locomotive monte sur la couverture.",
            "Les rails montent sur la couverture.",
            "Le drapeau monte sur la couverture.",
        ),
        "elance": (
            "La locomotive s'élance, trop tôt.",
            "Les rails s'élancent, trop tôt.",
            "Le drapeau s'élance, trop tôt.",
        ),
        "chante": (
            "La locomotive chante sur le bois.",
            "Les rails chantent sur le bois.",
            "Le drapeau chante sur le bois.",
        ),
        "sec": (
            "La locomotive attend au sec, près du seuil.",
            "Les rails attendent au sec, près du seuil.",
            "Le drapeau attend au sec, près du seuil.",
        ),
        "eau": (
            "La locomotive n'a plus à traverser l'eau.",
            "Les rails n'ont plus à traverser l'eau.",
            "Le drapeau n'a plus à traverser l'eau.",
        ),
        "abrite": (
            "La locomotive s'abrite derrière le tissu.",
            "Les rails s'abritent derrière le tissu.",
            "Le drapeau s'abrite derrière le tissu.",
        ),
    }
    return "narrateur|" + table[key][a - 1]


def t3_pass(a: int, b: int, c: int) -> list[str]:
    rows: dict[tuple[int, int], list[str]] = {
        (1, 1): [
            "enfant-m|Ton sac, Aniss.",
            "narrateur|Aniss fouille son sac, sans se presser.",
            "narrateur|Un rail de bois en sort, le dernier.",
            pose(a, "trou"),
            "narrateur|Nino observe l'objet, écoute les carreaux.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "narrateur|Aniss pose le rail dans le trou.",
            "narrateur|Ça fait clic, tout net.",
            "enfant-m|Clic.",
            "papa|Le trou n'est plus un trou.",
            "maman|Le grain d'ocre garde le stop.",
        ],
        (1, 2): [
            "enfant-m|Pour toi.",
            "narrateur|Nino tend la locomotive vers Aniss.",
            pose(a, "guide"),
            "narrateur|Le train contourne la chaussure, sans la pousser.",
            "narrateur|Une roue manque de taper le talon.",
            "narrateur|Nino observe l'objet, écoute le cuir.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "enfant-m|Il passe !",
            "maman|Le train a pris le bord, tout seul.",
            "papa|Les roues ont trouvé le cuir.",
            pose(a, "bord"),
        ],
        (1, 3): [
            "enfant-m|La chaussure, Aniss.",
            "narrateur|Aniss tire le lacet, sans un mot.",
            "narrateur|Nino pousse le talon vers le mur.",
            pose(a, "poussent"),
            "narrateur|Le passage redevient droit, presque.",
            "narrateur|Nino observe l'objet, écoute le lacet.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "enfant-m|Merci.",
            "papa|La chaussure a sa place, maintenant.",
            "maman|La ligne peut courir, maintenant.",
            "narrateur|Alors le grain d'ocre vise le quai des carreaux.",
        ],
        (2, 1): [
            "enfant-m|Le livre, dessous.",
            "narrateur|Aniss glisse le livre sous les roues.",
            "narrateur|La couverture fait une piste, un peu dure.",
            pose(a, "livre"),
            "narrateur|Le train avance, tout droit, sans s'enfoncer.",
            "narrateur|Nino observe l'objet, écoute le papier.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "enfant-m|Ça roule !",
            "papa|Le livre a tenu le tapis.",
            "maman|Aniss a poussé sans brusquer.",
            "narrateur|Une trace de roue reste sur le livre.",
        ],
        (2, 2): [
            "enfant-m|La planche, Aniss.",
            "narrateur|Aniss tire la planche derrière le canapé.",
            "narrateur|Ils la posent, pont mince sur le tapis.",
            pose(a, "elance"),
            "narrateur|Une roue glisse, manque de tomber.",
            "narrateur|Nino refuse de foncer, cette fois.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "narrateur|Aniss cale le bout, avec la paume.",
            "enfant-m|Ça tient.",
            "papa|Le pont a tenu, tout juste.",
            "maman|Le grain d'ocre reste au bout du pont.",
        ],
        (2, 3): [
            "enfant-m|On recommence au parquet.",
            "narrateur|Aniss pointe la bande lisse, près de la vitre.",
            "narrateur|Nino suit le doigt, sans parler.",
            pose(a, "chante"),
            "narrateur|Les roues glissent, nettes, sans s'enfoncer.",
            "narrateur|Nino observe l'objet, écoute le parquet.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "enfant-m|Elles glissent.",
            "maman|Le tapis garde son creux, plus loin.",
            "papa|Le bois est plus facile, ici.",
            "narrateur|Alors le grain d'ocre brille contre la vitre.",
        ],
        (3, 1): [
            "enfant-m|On tient le carton, Aniss.",
            "narrateur|Une rafale pousse, puis se tait un peu.",
            "narrateur|Ils tournent la gare, dos au vent.",
            pose(a, "sec"),
            "narrateur|Le grain d'ocre manque de glisser, puis tient.",
            "narrateur|Nino observe l'objet, écoute le vent.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "enfant-m|Il reste !",
            "papa|Le vent n'a pas pris le toit.",
            "maman|Vous avez laissé la rafale passer.",
            "narrateur|Une dalle sèche reçoit la boîte.",
        ],
        (3, 2): [
            "enfant-m|On rapproche la gare.",
            "narrateur|Aniss tire la boîte, un tout petit cran.",
            "narrateur|Nino pousse de l'autre côté, sans courir.",
            pose(a, "eau"),
            "narrateur|La flaque reste là, sans les toucher.",
            "narrateur|Nino observe l'objet, écoute les dalles.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "enfant-m|On est assez près.",
            "maman|Le carton reste au sec.",
            "papa|La gare a fait le chemin, vers vous.",
            "narrateur|Alors le grain d'ocre vise le quai, tout près.",
        ],
        (3, 3): [
            "enfant-m|Le drapeau, devant.",
            "narrateur|Aniss plante le bâton, face au vent.",
            "narrateur|Aniss tend le rouge, comme un mur.",
            pose(a, "abrite"),
            "narrateur|Alors le carton penche, puis se tient.",
            "narrateur|Nino observe l'objet, écoute le claquement.",
            "narrateur|Il retrouve le grain d'ocre, sur le toit.",
            "enfant-m|Le stop tient.",
            "papa|Le drapeau a pris le vent.",
            "maman|Le toit n'a plus peur.",
            "narrateur|Alors le grain d'ocre reste, derrière le rouge.",
        ],
    }
    return rows[(b, c)]


END_LEAD = {
    (1, 1): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Gare.",
        "enfant-m|Tu as fini le mot.",
        "papa|Le clic a fermé le trou.",
        "maman|Vous avez laissé le sac parler.",
    ],
    (1, 2): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Là.",
        "enfant-m|Tu as montré le bord.",
        "papa|Les roues ont contourné le cuir.",
        "maman|Vous n'avez pas poussé la chaussure.",
    ],
    (1, 3): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Mur.",
        "enfant-m|Le passage est droit.",
        "papa|La chaussure a sa place, au mur.",
        "maman|Vous avez poussé ensemble, sans crier.",
    ],
    (2, 1): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Livre.",
        "enfant-m|La couverture a tenu.",
        "maman|Le tapis n'a plus avalé les roues.",
        "papa|Aniss a glissé le livre, sans se presser.",
    ],
    (2, 2): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Pont.",
        "enfant-m|Ça a failli tomber.",
        "papa|La planche a tenu, tout juste.",
        "maman|Vous avez calé le bout, ensemble.",
    ],
    (2, 3): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Bois.",
        "enfant-m|Le parquet chantait.",
        "maman|Le tapis garde son creux, plus loin.",
        "papa|Vous avez suivi le doigt, jusqu'à la vitre.",
    ],
    (3, 1): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Stop.",
        "enfant-m|Le vent n'a pas gagné.",
        "papa|Vous avez tourné la gare, dos à la rafale.",
        "maman|Le toit est resté sec.",
    ],
    (3, 2): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Près.",
        "enfant-m|On n'a pas traversé l'eau.",
        "maman|La gare a fait le chemin, vers vous.",
        "papa|Le carton n'a pas goûté la flaque.",
    ],
    (3, 3): [
        "narrateur|Le train entre dans la boîte, sous le grain d'ocre.",
        "copain|Mur.",
        "enfant-m|Le rouge a pris le vent.",
        "papa|Le drapeau a fait un mur, tout court.",
        "maman|Le grain d'ocre n'a pas glissé.",
    ],
}

END_MID = {
    1: "narrateur|La locomotive garde une poussière de chemin.",
    2: "narrateur|Un rail reste contre le carton, tout droit.",
    3: "narrateur|Le drapeau penche sur le toit, sans claquer.",
}

END_CODA = {
    1: "narrateur|Nino pose un doigt près du grain d'ocre.",
    2: "narrateur|Aniss aligne un dernier bois, sous le grain d'ocre.",
    3: "narrateur|Le rouge frôle le grain d'ocre, puis s'arrête.",
}

LAST = {
    (1, 1, 1): "Un clic dort dans le rail du sac.",
    (1, 1, 2): "Une roue garde une poussière de carreau.",
    (1, 1, 3): "Le lacet de la chaussure reste un peu tiède.",
    (1, 2, 1): "La couverture du livre porte une trace de roue.",
    (1, 2, 2): "La planche garde un sillon, tout mince.",
    (1, 2, 3): "Le parquet luit où les roues ont passé.",
    (1, 3, 1): "Le grain d'ocre n'a pas bougé, malgré le vent.",
    (1, 3, 2): "Une auréole sèche au pied de la boîte.",
    (1, 3, 3): "Le drapeau penche, et le vent se tait.",
    (2, 1, 1): "Le rail du sac reste dans la ligne, droit.",
    (2, 1, 2): "Un rail frôle le cuir, sans le pousser.",
    (2, 1, 3): "La chaussure touche le mur, enfin.",
    (2, 2, 1): "Un coin de livre reste chaud, sous le bois.",
    (2, 2, 2): "La planche sent le grenier, un peu.",
    (2, 2, 3): "Une bande de parquet garde le clic.",
    (2, 3, 1): "Le carton a cessé de trembler.",
    (2, 3, 2): "La gare s'est rapprochée, hors de l'eau.",
    (2, 3, 3): "Le tissu rouge arrête un peu d'air.",
    (3, 1, 1): "Le drapeau voit le clic, au-dessus du trou.",
    (3, 1, 2): "Le rouge contourne le cuir, sans le toucher.",
    (3, 1, 3): "Le bâton vise le mur, pendant qu'ils poussent.",
    (3, 2, 1): "Le rouge repose au bord du livre.",
    (3, 2, 2): "Le drapeau traverse la planche, sans tomber.",
    (3, 2, 3): "Le rouge suit la bande près de la vitre.",
    (3, 3, 1): "Le grain d'ocre tient, sous le drapeau.",
    (3, 3, 2): "Le drapeau entre dans la boîte, hors de l'eau.",
    (3, 3, 3): "Le tissu rouge fait un mur, tout court.",
}

ASK = {
    1: "papa|Tu raconteras ce qui bloquait ?",
    2: "maman|Tu gardes quoi, de la ligne ?",
    3: "papa|Le moment difficile, tu le dis ?",
}

ANS = {
    1: "enfant-m|Surtout le trou.",
    2: "enfant-m|Surtout le tapis.",
    3: "enfant-m|Surtout le vent.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    rows = list(END_LEAD[(b, c)])
    rows.append(END_MID[a])
    rows.append(END_CODA[a])
    rows.append(ASK[b])
    rows.append(ANS[b])
    rows.append(f"narrateur|{LAST[(a, b, c)]}")
    return rows


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "ciseaux,carton,sonnette",
        {"emphasis": "grain d'ocre"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("la locomotive", "les rails", "le drapeau"), "pause_before": 200},
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
            {"emphasis": "grain d'ocre"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le couloir", "le salon", "la terrasse"), "pause_before": 200},
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
                    {"emphasis": "grain d'ocre"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", "carton,roue",
                    {"emphasis": "grain d'ocre"},
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
        "hugo",
        "parle peu",
        "camarade",
        "timide",
        "forcer la parole",
        "il faut attendre",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui",
        "merle",
        "couleur de miel",
        "j'ai une idée",
        "celui où j'ai compris",
        "mission accomplie",
        "j'ai compris",
        "croissant pâle",
        "étoile brune",
        "fil pâle",
        "grain d'ambre",
        "grain de cannelle",
        "colline",
        "chouchou",
        "hérisson",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(whole):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "enfant-m|" not in blob:
        raise SystemExit(f"{SID}: enfant-m absent")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: copain absent")
    if "grain d'ocre" not in blob:
        raise SystemExit(f"{SID}: indice grain d'ocre absent")
    if "refuse de foncer" not in blob:
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
    if not all(c.get("text_xai_tags") != c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")
    if len(story["chunks"]) != 86:
        raise SystemExit(f"chunks {len(story['chunks'])}≠86")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {SID} {sum(words(c['text']) for c in story['chunks'])} mots")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-017 — La locomotive de Nino et la gare en carton\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — laisser l'autre poser sa limite / son tour "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Nino, Aniss, papa, maman\n"
        "- **Lieu :** couloir (quai des carreaux), salon (tapis), terrasse (flaque), "
        "gare en carton\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Nino compte les fenêtres d'une boîte. Un grain d'ocre sur le toit sert de stop. "
        "Il veut que sa locomotive de bois arrive dessous, avec Aniss, avant que le sac "
        "reparte. Aniss commence « On va ? » ; Nino complète trop vite. Le mot s'arrête. "
        "Silence = réponse. T1 : locomotive / rails / drapeau (les trois partent). "
        "Première idée : faire dire go / vroom / gare. Ça rate. T2 : couloir, salon, "
        "terrasse. Deuxième ruse : chaussure et trou, tapis qui avale, vent et flaque. "
        "Aniss pointe, pose la paume, recule. Nino refuse de foncer. T3 : rail, "
        "locomotive, chaussure ; livre, planche, parquet ; vent, gare, drapeau. "
        "Le grain d'ocre paie le stop. Aniss finit son mot. Monde ≠ TREE-DIF-051 "
        "(pas colline, pas Chouchou).\n\n"
        "## Vécu\n\n"
        "Nino propose, Aniss prend son temps. Le message ne peut pas être terminé "
        "tout de suite. Première tentative : remplir le mot. Ça rate. Chaque lieu "
        "change l'obstacle. La leçon se voit : pousser / crier n'avance pas ; "
        "tendre, écouter le doigt, laisser le sac, le vent, le silence, ça tient. "
        "Fin : train sous le grain d'ocre + mot d'Aniss + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Hugo / « on va apprendre » / « camarade qui parle peu » / xai F-NAR-016 jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Ouverture inventée (genoux, fenêtres, ciseaux). Indice unique : grain d'ocre.\n"
        "- Corps : sourire parti, poitrine, adulte à la même hauteur. 2e ruse. "
        "Refuse de foncer. Dénouement qui a failli.\n"
        "- T1 ne retire pas l'équipement. 9 T2, 27 T3, 27 fins.\n"
        "- Merci vécu (laisser la roue). Question d'adulte. Un « en ce moment ».\n"
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
