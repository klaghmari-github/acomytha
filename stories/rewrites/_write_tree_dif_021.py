#!/usr/bin/env python3
"""TREE-DIF-021 — F-NAR-019. Fort d'Amir, grande fenêtre. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-021"
N1 = 10
TITLE = "Le fort d'Amir près de la fenêtre"
FIL = (
    "Au campement du salon, Amir veut finir le fort près de la grande fenêtre "
    "pour Nina, avant que la virgule de buée sèche. "
    "T1 = coussin-phare / couverture-voile / lanterne de poche ; les trois restent. "
    "Il crie trop tôt : le couloir se tait. "
    "T2 = fenêtre (virgule), cave sous la table, couloir (une chaussure). "
    "T3 = neuf façons d'inviter sans tirer. La virgule du début revient."
)
CHARS = "Amir, Nina, papa, maman"
SETTING = "salon, grande fenêtre, table, couloir"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "virgule de buée",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=un_fort_est_né_tout_seul; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "Nina",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=nina_arrive_à_son_pas; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=crier_trop_tôt_ne_suffit_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=nina_n_est_pas_au_même_endroit; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=proposer_sans_tirer; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "virgule",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_virgule_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
        found = TIC_WORDS.search(low)
        if found:
            raise SystemExit(f"tic {found.group(0)!r}: {ph}")
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
    "narrateur|Papa secoue le drap à carreaux.",
    "narrateur|Le tissu gonfle, puis retombe.",
    "narrateur|Il couvre le fauteuil, de travers.",
    "narrateur|Un toit bancal, né tout seul.",
    "enfant-m|Un fort !",
    "narrateur|La vapeur du cacao touche le verre.",
    "narrateur|Une virgule de buée s'y dessine.",
    "enfant-m|Elle fait un drapeau, là.",
    "papa|Tu as vu le pli, merci.",
    "maman|Nina arrive, dans un moment.",
    "narrateur|Le tapis du salon est tiède.",
    "narrateur|Ça sent le savon, et le cacao.",
    "enfant-m|Je veux le fort, pour Nina.",
    "narrateur|En ce moment, Amir tire le drap.",
    "narrateur|Le toit glisse, trop vite.",
    "narrateur|Le fauteuil redevient un fauteuil.",
    "enfant-m|Oh.",
    "narrateur|Le sourire d'Amir disparaît.",
    "maman|Tu le finis comment, ce toit ?",
    "papa|On prépare le campement du salon.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près du tapis.",
    "narrateur|Le coussin-phare, la couverture-voile, la lanterne.",
    "maman|Tu prends quoi, d'abord ?",
]

T1 = {
    1: {
        "lab": "le coussin-phare",
        "sons": "coussin,tapis",
        "emphasis": "coussin-phare",
        "passage": [
            "narrateur|Amir saisit le coussin-phare, jaune.",
            "enfant-m|Il a un rond, comme une lampe.",
            "papa|Pose-le sur le tapis, près du fauteuil.",
            "narrateur|Un petit toc sonne contre le sol.",
            "maman|La couverture-voile, ensuite, près de toi.",
            "narrateur|Papa glisse la lanterne, à côté.",
            "enfant-m|Nina, le fort est prêt !",
            "narrateur|Le couloir ne répond pas.",
            "narrateur|Amir serre le tissu, trop fort.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "papa|Tu l'invites, quand elle arrive ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le coussin reste tiède, au milieu.",
        ],
        "question": [
            "narrateur|Le coussin-phare attend, jaune.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "tapis",
            "accepted_examples": "tapis | le tapis | sur le tapis | par terre | au milieu",
            "retry_prompt": "Le coussin est sur le tapis. Il est où ?",
        },
        "confirm": [
            "narrateur|Des pas légers sonnent dans l'entrée.",
            "copine|Amir, je suis là.",
            "enfant-m|Viens voir le fort !",
            "narrateur|Nina a les joues froides.",
            "narrateur|Elle ne bouge pas, un instant.",
            "maman|Elle enlève son manteau, sans se presser.",
            "papa|Vous restez dans le salon ?",
            "enfant-m|Oui, papa.",
            "narrateur|La virgule de buée tient sur le verre.",
            "copine|J'ai vu ça, dehors.",
        ],
    },
    2: {
        "lab": "la couverture-voile",
        "sons": "tissu,savon",
        "emphasis": "couverture-voile",
        "passage": [
            "narrateur|Amir prend la couverture-voile, bleue.",
            "enfant-m|Elle sent le savon.",
            "maman|Enroule-la autour du coussin-phare.",
            "narrateur|Le tissu tombe, un peu froid.",
            "papa|Le coussin, dessous, pour le poids.",
            "narrateur|Il pose la lanterne, à côté.",
            "enfant-m|Nina va tout voir !",
            "narrateur|Personne ne répond, du couloir.",
            "narrateur|Amir mord sa lèvre, trop vite.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "maman|Tu lui proposes le fort ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un pli de voile garde le savon.",
        ],
        "question": [
            "narrateur|La couverture-voile tient le coussin.",
            "papa|Elle est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "coussin",
            "accepted_examples": "coussin | le coussin | autour | autour du coussin | sur le coussin",
            "retry_prompt": "La couverture est autour du coussin. Elle est où ?",
        },
        "confirm": [
            "narrateur|La porte s'ouvre, un peu d'air.",
            "copine|Me voilà, Amir.",
            "enfant-m|Regarde, c'est tout bleu.",
            "narrateur|Nina touche le tissu, un instant.",
            "narrateur|Puis sa main se retire.",
            "papa|Ça sent le savon, hein ?",
            "maman|Vous restez près du tapis ?",
            "copine|Je ne sais pas.",
            "narrateur|La virgule de buée penche, mince.",
            "enfant-m|Le fort t'attend.",
        ],
    },
    3: {
        "lab": "la lanterne de poche",
        "sons": "clic,lampe",
        "emphasis": "lanterne",
        "passage": [
            "narrateur|Amir allume la lanterne de poche.",
            "enfant-m|Ça fait un camp, là.",
            "maman|Le rond jaune éclaire le tapis.",
            "narrateur|Un clic sec, puis le silence.",
            "papa|Le coussin et la couverture, avec toi.",
            "narrateur|Il les pose près du fort.",
            "enfant-m|Nina, viens voir la lumière !",
            "narrateur|Le couloir reste muet.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "papa|Tu lui proposes, sans crier ?",
            "enfant-m|Oui.",
            "narrateur|Le rond jaune tient, tout petit.",
        ],
        "question": [
            "narrateur|La lanterne tient le fort allumé.",
            "maman|Elle éclaire quoi, Amir ?",
        ],
        "qfields": {
            "expected_answer": "tapis",
            "accepted_examples": "tapis | le tapis | fort | le fort | le camp | un rond",
            "retry_prompt": "La lanterne éclaire le tapis. Elle éclaire quoi ?",
        },
        "confirm": [
            "narrateur|Un manteau mouillé apparaît au seuil.",
            "copine|J'arrive, Amir.",
            "enfant-m|Regarde le rond jaune.",
            "narrateur|Nina cligne, puis se tait.",
            "maman|Le salon est tiède, devant.",
            "papa|On vous laisse le temps ?",
            "enfant-m|Oui.",
            "narrateur|La virgule de buée luit, un peu.",
            "copine|La lumière est forte.",
            "narrateur|Amir baisse la lanterne, d'un cran.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le coussin-phare attend, au milieu.",
        "narrateur|Nina n'est plus près du tapis.",
        "narrateur|La fenêtre, la table, ou le couloir.",
        "papa|On l'invite où, Amir ?",
    ],
    2: [
        "narrateur|La couverture-voile traîne un peu.",
        "narrateur|Nina n'est plus près du tapis.",
        "maman|La fenêtre, la table, ou le couloir ?",
        "papa|On l'invite où, Amir ?",
    ],
    3: [
        "narrateur|La lanterne fait un rond, au tapis.",
        "narrateur|Nina n'est plus près du tapis.",
        "narrateur|La fenêtre, la table, ou le couloir.",
        "maman|On l'invite où, Amir ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "pluie,vitre",
        "emphasis": "virgule de buée",
        "passage": [
            "narrateur|Le coussin-phare voyage vers la fenêtre.",
            "narrateur|Nina a le nez contre le verre.",
            "enfant-m|Nina, le fort est prêt !",
            "narrateur|Elle ne se tourne pas.",
            "copine|La virgule de buée bouge.",
            "enfant-m|Tu viens ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|Amir tend la main, puis s'arrête.",
            "narrateur|Le sourire d'Amir disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu proposes comment, Amir ?",
        ],
    },
    (2, 1): {
        "sons": "pluie,tissu",
        "emphasis": "virgule de buée",
        "passage": [
            "narrateur|La couverture-voile glisse vers la fenêtre.",
            "narrateur|Nina suit une goutte, du doigt.",
            "enfant-m|Regarde, c'est tout bleu !",
            "narrateur|Le tissu frôle son genou.",
            "copine|Attends.",
            "narrateur|Elle ne quitte pas le verre.",
            "enfant-m|Le fort, Nina.",
            "narrateur|Nina ne dit rien, plus longtemps.",
            "narrateur|Amir veut tirer le tissu.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu proposes comment, Amir ?",
        ],
    },
    (3, 1): {
        "sons": "pluie,lampe",
        "emphasis": "virgule de buée",
        "passage": [
            "narrateur|La lanterne avance vers la fenêtre.",
            "narrateur|Un rond jaune touche sa joue.",
            "enfant-m|Nina, viens dans la lumière !",
            "narrateur|Elle cligne, trop fort.",
            "copine|C'est trop.",
            "narrateur|Elle colle son nez au verre.",
            "enfant-m|Le camp t'attend.",
            "narrateur|Nina se tait, les yeux au dehors.",
            "narrateur|Le clic a été trop vif.",
            "narrateur|Le sourire d'Amir disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu proposes comment, Amir ?",
        ],
    },
    (1, 2): {
        "sons": "bois,chaise",
        "emphasis": "cave",
        "passage": [
            "narrateur|Le coussin-phare penche vers les chaises.",
            "narrateur|Nina est sous la table.",
            "copine|C'est ma cave, à moi.",
            "enfant-m|Mon fort est au salon.",
            "narrateur|Deux jeux, trop loin l'un de l'autre.",
            "enfant-m|Tu viens dans le mien ?",
            "copine|Le mien a commencé.",
            "narrateur|Nina recule d'un pouce, sous le bois.",
            "narrateur|Amir pousse le coussin, trop vite.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu fais comment, Amir ?",
        ],
    },
    (2, 2): {
        "sons": "bois,tissu",
        "emphasis": "cave",
        "passage": [
            "narrateur|La couverture-voile frôle le pied de table.",
            "narrateur|Nina tient la nappe, comme un toit.",
            "copine|Ma cave a sa règle.",
            "enfant-m|On met le bleu, dessus ?",
            "narrateur|Nina serre la nappe, plus fort.",
            "copine|Pas tout recouvrir.",
            "enfant-m|Alors tu sors ?",
            "narrateur|Nina secoue la tête, minuscule.",
            "narrateur|Le savon sent, trop près d'elle.",
            "narrateur|Le sourire d'Amir disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu fais comment, Amir ?",
        ],
    },
    (3, 2): {
        "sons": "bois,lampe",
        "emphasis": "cave",
        "passage": [
            "narrateur|La lanterne éclaire un peu, dessous.",
            "narrateur|Nina plisse les yeux, sous le bois.",
            "copine|Ma cave n'aime pas ça.",
            "enfant-m|C'est pour voir, Nina.",
            "narrateur|Le rond jaune mange l'ombre.",
            "copine|L'ombre, c'est la cave.",
            "enfant-m|Tu viens au camp, alors ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu fais comment, Amir ?",
        ],
    },
    (1, 3): {
        "sons": "chaussure,porte",
        "emphasis": "chaussure",
        "passage": [
            "narrateur|Le coussin-phare voyage jusqu'au couloir.",
            "narrateur|Nina enfile une chaussure.",
            "copine|Maman m'attend, tout à l'heure.",
            "enfant-m|Le fort est prêt, Nina.",
            "narrateur|L'autre chaussure attend, ouverte.",
            "enfant-m|Tu restes un peu ?",
            "copine|Je ne sais pas.",
            "narrateur|Amir s'assoit sur le coussin, au seuil.",
            "narrateur|Nina serre le lacet, sans parler.",
            "narrateur|Le sourire d'Amir disparaît.",
            "maman|Le manteau est près de la porte.",
            "papa|Tu proposes quoi, Amir ?",
        ],
    },
    (2, 3): {
        "sons": "chaussure,tissu",
        "emphasis": "chaussure",
        "passage": [
            "narrateur|La couverture-voile traîne, au seuil.",
            "narrateur|Nina noue un lacet, lentement.",
            "enfant-m|Une cape, pour partir ?",
            "copine|Pas une cape.",
            "narrateur|Le tissu reste en tas, près d'elle.",
            "enfant-m|Le fort, alors ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Une chaussure est faite, l'autre non.",
            "narrateur|Amir veut l'envelopper, trop vite.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu proposes quoi, Amir ?",
        ],
    },
    (3, 3): {
        "sons": "chaussure,lampe",
        "emphasis": "chaussure",
        "passage": [
            "narrateur|La lanterne éclaire les chaussures, au sol.",
            "narrateur|Nina enfile une chaussure, puis s'arrête.",
            "copine|Le rond jaune, sur mes pieds.",
            "enfant-m|C'est le phare du fort.",
            "narrateur|L'autre chaussure baille, ouverte.",
            "enfant-m|Tu restes jouer ?",
            "copine|Peut-être.",
            "narrateur|Nina regarde la porte, puis Amir.",
            "narrateur|Le clic a fait trop de bruit.",
            "narrateur|Le sourire d'Amir disparaît.",
            "maman|Le manteau est près de la porte.",
            "papa|Tu proposes quoi, Amir ?",
        ],
    },
}

T3_LABS = {
    1: ("attendre un peu", "parler tout bas", "s'asseoir à côté"),
    2: ("glisser le fort", "mélanger les forts", "rester à côté"),
    3: ("un tout petit jeu", "l'accompagner", "proposer plus tard"),
}

T3_CHOICE = {
    1: [
        "narrateur|Nina reste collée à la fenêtre.",
        "narrateur|La virgule de buée penche, mince.",
        "papa|Attendre, parler tout bas, ou s'asseoir ?",
    ],
    2: [
        "narrateur|La cave de Nina a sa place.",
        "narrateur|Deux toits, trop loin l'un de l'autre.",
        "maman|Glisser, mélanger, ou rester à côté ?",
    ],
    3: [
        "narrateur|Une chaussure est enfilée, l'autre non.",
        "narrateur|Le manteau attend, près de la porte.",
        "papa|Un petit jeu, accompagner, ou plus tard ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "enfant-m|J'attends un peu.",
        "copine|Merci, Amir.",
        "narrateur|Une goutte glisse, puis une autre.",
        "narrateur|Le coussin-phare attend derrière elle.",
        "narrateur|Amir regarde la virgule de buée.",
        "narrateur|Nina se tourne, à son heure.",
        "copine|Je viens, maintenant.",
        "enfant-m|Le fort est chaud.",
        "papa|Son regard a fini, tout seul.",
        "maman|Elle a dit oui, à son pas.",
        "narrateur|Le coussin garde un rond tiède.",
    ],
    (1, 1, 2): [
        "enfant-m|Nina, je te propose le fort.",
        "narrateur|Sa voix reste basse, près du verre.",
        "narrateur|Il pose le coussin, tout proche.",
        "copine|J'ai entendu, Amir.",
        "enfant-m|Tu peux dire non.",
        "narrateur|Nina suit la virgule, du doigt.",
        "copine|Oui, je viens.",
        "narrateur|Elle quitte la fenêtre, sans se presser.",
        "papa|Tu as proposé, sans tirer.",
        "maman|Elle a choisi d'elle-même.",
        "narrateur|Le coussin a un pli, au bord.",
    ],
    (1, 1, 3): [
        "enfant-m|Je m'assois à côté.",
        "narrateur|Amir s'assoit sur le coussin-phare.",
        "narrateur|Il ne tire pas sa manche.",
        "copine|Tu regardes la pluie, toi aussi ?",
        "enfant-m|Oui, avec toi.",
        "narrateur|Deux nez, contre le verre.",
        "narrateur|Deux virgules de buée, côte à côte.",
        "copine|Après, on va dans le fort.",
        "papa|Tu es resté près d'elle.",
        "maman|Elle a proposé la suite.",
        "narrateur|Le coussin tient deux chaleurs, maintenant.",
    ],
    (1, 2, 1): [
        "enfant-m|Je te propose mon coussin.",
        "copine|Dans ma cave ?",
        "enfant-m|Si tu veux.",
        "narrateur|Le coussin-phare glisse sous la table.",
        "narrateur|Nina recule un peu, puis accepte.",
        "copine|Il est mou, merci.",
        "enfant-m|On est deux, maintenant.",
        "narrateur|La virgule de buée luit, loin, au verre.",
        "papa|Tu as glissé, sans pousser.",
        "maman|Sa cave a gardé sa place.",
        "narrateur|Le coussin porte une miette, au coin.",
    ],
    (1, 2, 2): [
        "enfant-m|On mélange les deux forts ?",
        "copine|Le mien reste, le tien aussi.",
        "enfant-m|D'accord.",
        "narrateur|Le coussin-phare fait un mur commun.",
        "narrateur|Une chaise bouge, d'un pouce.",
        "copine|C'est plus grand, maintenant.",
        "enfant-m|C'est le nôtre.",
        "narrateur|La virgule de buée éclaire le bois.",
        "papa|Vous avez dit oui, tous les deux.",
        "maman|Deux idées, une seule cave.",
        "narrateur|Le coussin a deux empreintes, au milieu.",
    ],
    (1, 2, 3): [
        "copine|Pas dans ma cave, Amir.",
        "enfant-m|D'accord.",
        "enfant-m|Je reste à côté, alors.",
        "narrateur|Le coussin-phare reste juste à côté.",
        "narrateur|Il joue tout près, sans entrer.",
        "copine|Tu peux parler, d'ici.",
        "enfant-m|Mon fort t'écoute.",
        "narrateur|Une main passe sous la nappe.",
        "papa|Le non a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "narrateur|Le coussin garde sa rondeur, dehors.",
    ],
    (1, 3, 1): [
        "enfant-m|Un tout petit jeu, Nina ?",
        "copine|Très petit, alors.",
        "enfant-m|D'accord.",
        "narrateur|Le coussin-phare devient un siège, une minute.",
        "narrateur|Ils comptent jusqu'à trois, tout bas.",
        "copine|C'est fini.",
        "enfant-m|Merci d'être restée.",
        "narrateur|La virgule de buée penche, au loin.",
        "papa|Tu as proposé court, juste assez.",
        "maman|La chaussure attendait, sans se fâcher.",
        "narrateur|Le coussin a un creux, au milieu.",
    ],
    (1, 3, 2): [
        "copine|Je m'en vais, Amir.",
        "enfant-m|Je t'accompagne, alors.",
        "narrateur|Le coussin-phare reste au seuil, un instant.",
        "narrateur|Il marche à côté d'elle, sans presser.",
        "papa|La porte s'ouvre, un peu d'air.",
        "enfant-m|À bientôt, Nina.",
        "copine|À bientôt, le fort.",
        "narrateur|La virgule de buée reste au salon.",
        "maman|Tu as marché à son pas.",
        "narrateur|Ils se font un petit signe.",
        "narrateur|Le coussin garde la forme de l'attente.",
    ],
    (1, 3, 3): [
        "enfant-m|On joue plus tard, alors ?",
        "copine|Oui, plus tard.",
        "enfant-m|D'accord.",
        "narrateur|Le coussin-phare garde sa place, au salon.",
        "narrateur|Nina noue l'autre chaussure.",
        "copine|Garde le fort allumé.",
        "enfant-m|Il t'attend.",
        "narrateur|La virgule de buée tient, mince.",
        "papa|Tu as proposé une autre heure.",
        "maman|Elle a dit oui, pour plus tard.",
        "narrateur|Le coussin reste tiède, au milieu.",
    ],
    (2, 1, 1): [
        "enfant-m|J'attends, près du bleu.",
        "copine|Merci.",
        "narrateur|Nina suit la virgule, sans parler.",
        "narrateur|La couverture-voile attend derrière elle.",
        "narrateur|Un pli sent le savon, froid.",
        "narrateur|Nina se tourne, à son heure.",
        "copine|Je viens sous le bleu.",
        "enfant-m|Il est un peu froid.",
        "papa|Son doigt a fini la goutte.",
        "maman|Elle a dit oui, après.",
        "narrateur|La voile garde un pli, en drapeau.",
    ],
    (2, 1, 2): [
        "enfant-m|Nina, le bleu est pour toi.",
        "narrateur|Sa voix reste basse, près du verre.",
        "narrateur|Il pose la couverture, tout proche.",
        "copine|J'ai entendu.",
        "enfant-m|Tu peux dire non.",
        "narrateur|Nina souffle sur la virgule de buée.",
        "copine|Oui, je viens.",
        "narrateur|Le savon la suit, jusqu'au tapis.",
        "papa|Tu as proposé, sans tirer.",
        "maman|Elle a choisi d'elle-même.",
        "narrateur|La voile a un coin plus chaud.",
    ],
    (2, 1, 3): [
        "enfant-m|Je m'assois sous le bleu.",
        "narrateur|Amir s'assoit sous la couverture-voile.",
        "narrateur|Il ne tire pas sa manche.",
        "copine|Tu regardes la pluie, toi aussi ?",
        "enfant-m|Oui, avec toi.",
        "narrateur|Deux nez, contre le verre.",
        "copine|Après, on rentre sous le bleu.",
        "narrateur|La virgule de buée s'étire, fine.",
        "papa|Tu es resté près d'elle.",
        "maman|Elle a proposé la suite.",
        "narrateur|La voile sent le savon, et la pluie.",
    ],
    (2, 2, 1): [
        "enfant-m|Je te prête le bleu.",
        "copine|Dans ma cave ?",
        "enfant-m|Si tu veux.",
        "narrateur|La couverture-voile glisse sous la table.",
        "narrateur|Nina recule un peu, puis accepte.",
        "copine|Ça sent le savon, merci.",
        "enfant-m|On est deux, maintenant.",
        "narrateur|Un fil de savon brille sous le bois.",
        "papa|Tu as glissé, sans pousser.",
        "maman|Sa cave a gardé sa place.",
        "narrateur|La voile porte une miette, au bord.",
    ],
    (2, 2, 2): [
        "enfant-m|On mélange les deux toits ?",
        "copine|Le mien reste, le tien aussi.",
        "enfant-m|D'accord.",
        "narrateur|La couverture-voile recouvre les deux coins.",
        "narrateur|Une chaise bouge, d'un pouce.",
        "copine|C'est plus grand, maintenant.",
        "enfant-m|C'est le nôtre.",
        "narrateur|La virgule de buée éclaire le bleu.",
        "papa|Vous avez dit oui, tous les deux.",
        "maman|Deux idées, une seule cave.",
        "narrateur|Deux coins de tissu se touchent, à peine.",
    ],
    (2, 2, 3): [
        "copine|Pas dans ma cave, Amir.",
        "enfant-m|D'accord.",
        "enfant-m|Je reste à côté, alors.",
        "narrateur|La couverture-voile reste juste à côté.",
        "narrateur|Il joue tout près, sans entrer.",
        "copine|Tu peux parler, d'ici.",
        "enfant-m|Mon bleu t'écoute.",
        "narrateur|Une main passe sous la nappe.",
        "papa|Le non a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "narrateur|La voile garde son savon, dehors.",
    ],
    (2, 3, 1): [
        "enfant-m|Un tout petit jeu, Nina ?",
        "copine|Très petit, alors.",
        "enfant-m|D'accord.",
        "narrateur|La couverture-voile devient une cape, une minute.",
        "narrateur|Ils comptent jusqu'à trois, tout bas.",
        "copine|C'est fini.",
        "enfant-m|Merci d'être restée.",
        "narrateur|La virgule de buée penche, au loin.",
        "papa|Tu as proposé court, juste assez.",
        "maman|La chaussure attendait, sans se fâcher.",
        "narrateur|La cape redevient un tas, au seuil.",
    ],
    (2, 3, 2): [
        "copine|Je m'en vais, Amir.",
        "enfant-m|Je t'accompagne, alors.",
        "narrateur|La couverture-voile reste au seuil, un instant.",
        "narrateur|Il marche à côté d'elle, sans presser.",
        "papa|La porte s'ouvre, un peu d'air.",
        "enfant-m|À bientôt, Nina.",
        "copine|À bientôt, le bleu.",
        "narrateur|La virgule de buée reste au salon.",
        "maman|Tu as marché à son pas.",
        "narrateur|Ils se font un petit signe.",
        "narrateur|La voile garde un pli, au seuil.",
    ],
    (2, 3, 3): [
        "enfant-m|On joue plus tard, alors ?",
        "copine|Oui, plus tard.",
        "enfant-m|D'accord.",
        "narrateur|La couverture-voile garde sa place, au salon.",
        "narrateur|Nina noue l'autre chaussure.",
        "copine|Garde le bleu pour moi.",
        "enfant-m|Il t'attend.",
        "narrateur|La virgule de buée tient, mince.",
        "papa|Tu as proposé une autre heure.",
        "maman|Elle a dit oui, pour plus tard.",
        "narrateur|La voile garde un pli, au salon.",
    ],
    (3, 1, 1): [
        "enfant-m|J'attends, près du rond.",
        "copine|Merci.",
        "narrateur|Nina suit la virgule, sans parler.",
        "narrateur|La lanterne attend derrière elle.",
        "narrateur|Le rond jaune reste bas, sur le tapis.",
        "narrateur|Nina se tourne, à son heure.",
        "copine|Je viens, maintenant.",
        "enfant-m|Le camp est allumé.",
        "papa|Son regard a fini, tout seul.",
        "maman|Elle a dit oui, à son pas.",
        "narrateur|La lanterne fait un croissant, au tapis.",
    ],
    (3, 1, 2): [
        "enfant-m|Nina, je te propose le camp.",
        "narrateur|Sa voix reste basse, près du verre.",
        "narrateur|Il pose la lanterne, tout proche.",
        "copine|J'ai entendu, Amir.",
        "enfant-m|Tu peux dire non.",
        "narrateur|Nina souffle sur la virgule de buée.",
        "copine|Oui, je viens.",
        "narrateur|Elle quitte la fenêtre, sans se presser.",
        "papa|Tu as proposé, sans tirer.",
        "maman|Elle a choisi d'elle-même.",
        "narrateur|La lanterne a un clic plus doux.",
    ],
    (3, 1, 3): [
        "enfant-m|Je m'assois dans le rond.",
        "narrateur|Amir s'assoit dans le rond jaune.",
        "narrateur|Il ne tire pas sa manche.",
        "copine|Tu regardes la pluie, toi aussi ?",
        "enfant-m|Oui, avec toi.",
        "narrateur|Deux nez, contre le verre.",
        "copine|Après, on va dans le camp.",
        "narrateur|Deux virgules de buée, côte à côte.",
        "papa|Tu es resté près d'elle.",
        "maman|Elle a proposé la suite.",
        "narrateur|Le rond jaune tient deux ombres.",
    ],
    (3, 2, 1): [
        "enfant-m|Je te prête le rond.",
        "copine|Dans ma cave ?",
        "enfant-m|Tout petit, si tu veux.",
        "narrateur|La lanterne glisse sous la table.",
        "narrateur|Nina recule un peu, puis accepte.",
        "copine|C'est moins fort, merci.",
        "enfant-m|On est deux, maintenant.",
        "narrateur|Un rond jaune dort sous le bois.",
        "papa|Tu as glissé, sans pousser.",
        "maman|Sa cave a gardé son ombre.",
        "narrateur|La lanterne porte une poussière, au verre.",
    ],
    (3, 2, 2): [
        "enfant-m|On mélange les deux coins ?",
        "copine|Le mien reste, le tien aussi.",
        "enfant-m|D'accord.",
        "narrateur|La lanterne éclaire les deux coins.",
        "narrateur|Une chaise bouge, d'un pouce.",
        "copine|C'est plus grand, maintenant.",
        "enfant-m|C'est le nôtre.",
        "narrateur|Deux ronds jaunes se mêlent, au bois.",
        "papa|Vous avez dit oui, tous les deux.",
        "maman|Deux idées, une seule cave.",
        "narrateur|La lanterne a deux reflets, au pied.",
    ],
    (3, 2, 3): [
        "copine|Pas dans ma cave, Amir.",
        "enfant-m|D'accord.",
        "enfant-m|Je reste à côté, alors.",
        "narrateur|La lanterne reste juste à côté.",
        "narrateur|Il joue tout près, sans entrer.",
        "copine|Tu peux parler, d'ici.",
        "enfant-m|Mon camp t'écoute.",
        "narrateur|Une main passe sous la nappe.",
        "papa|Le non a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "narrateur|La lanterne veille à côté, sans entrer.",
    ],
    (3, 3, 1): [
        "enfant-m|Un tout petit jeu, Nina ?",
        "copine|Très petit, alors.",
        "enfant-m|D'accord.",
        "narrateur|La lanterne devient un phare, une minute.",
        "narrateur|Ils comptent jusqu'à trois, tout bas.",
        "copine|C'est fini.",
        "enfant-m|Merci d'être restée.",
        "narrateur|La virgule de buée penche, au loin.",
        "papa|Tu as proposé court, juste assez.",
        "maman|La chaussure attendait, sans se fâcher.",
        "narrateur|Le clic se tait, net.",
    ],
    (3, 3, 2): [
        "copine|Je m'en vais, Amir.",
        "enfant-m|Je t'accompagne, alors.",
        "narrateur|La lanterne reste au seuil, un instant.",
        "narrateur|Il marche à côté d'elle, sans presser.",
        "papa|La porte s'ouvre, un peu d'air.",
        "enfant-m|À bientôt, Nina.",
        "copine|À bientôt, le camp.",
        "narrateur|La virgule de buée reste au salon.",
        "maman|Tu as marché à son pas.",
        "narrateur|Ils se font un petit signe.",
        "narrateur|La lanterne garde un rond, au seuil.",
    ],
    (3, 3, 3): [
        "enfant-m|On joue plus tard, alors ?",
        "copine|Oui, plus tard.",
        "enfant-m|D'accord.",
        "narrateur|La lanterne garde sa place, au salon.",
        "narrateur|Nina noue l'autre chaussure.",
        "copine|Garde le camp allumé.",
        "enfant-m|Il t'attend.",
        "narrateur|La virgule de buée tient, mince.",
        "papa|Tu as proposé une autre heure.",
        "maman|Elle a dit oui, pour plus tard.",
        "narrateur|Le tapis garde un rond jaune, tiède.",
    ],
}

T3_EMPH = {
    1: {1: "virgule de buée", 2: "fort", 3: "nez"},
    2: {1: "cave", 2: "deux", 3: "côté"},
    3: {1: "petit jeu", 2: "accompagne", 3: "plus tard"},
}

T3_SONS = {
    (1, 1): "pluie,coussin",
    (1, 2): "voix,tissu",
    (1, 3): "vitre,pas",
    (2, 1): "bois,tissu",
    (2, 2): "chaise,tissu",
    (2, 3): "bois,silence",
    (3, 1): "voix,chaussure",
    (3, 2): "porte,pas",
    (3, 3): "lacet,tissu",
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Ils rentrent dans le fort, à son heure.",
        "copine|La virgule de buée a fini son chemin.",
        "enfant-m|Toi aussi.",
        "papa|Vous avez attendu le bon moment.",
        "maman|Le cacao est un peu chaud.",
        "narrateur|Le coussin-phare reste tiède, au milieu.",
        "narrateur|Nina souffle sur sa tasse.",
        "enfant-m|C'est notre fort, maintenant.",
        "narrateur|Une virgule sèche, en croissant, sur le verre.",
    ],
    (1, 1, 2): [
        "narrateur|Le fort sent le savon, un peu.",
        "enfant-m|Tu as dit oui, tout bas.",
        "copine|J'avais entendu, près du verre.",
        "papa|Tu as proposé, sans tirer.",
        "maman|Buvez un peu.",
        "narrateur|Le coussin-phare a un pli, au bord.",
        "narrateur|Nina pose sa joue sur le tissu.",
        "enfant-m|Reste autant que tu veux.",
        "narrateur|Le cacao laisse un rond sur le bois.",
    ],
    (1, 1, 3): [
        "narrateur|Après la pluie, ils glissent dans le fort.",
        "copine|On a regardé ensemble, d'abord.",
        "enfant-m|Puis tu as dit : on y va.",
        "maman|Deux nez, puis deux coussins.",
        "papa|Le salon se tait, un moment.",
        "narrateur|Le coussin-phare tient deux chaleurs.",
        "narrateur|Nina rit, tout petit.",
        "enfant-m|Le fort t'a attendue.",
        "narrateur|Deux buées restent, côte à côte.",
    ],
    (1, 2, 1): [
        "narrateur|Sous la table, ça sent le bois.",
        "copine|Ton coussin est dans ma cave.",
        "enfant-m|Tu as dit oui.",
        "papa|Vous tenez tous les deux, là-dessous.",
        "maman|Le cacao descend jusqu'à vous.",
        "narrateur|Le coussin-phare porte une miette, au coin.",
        "narrateur|Nina tape deux fois, sous le bois.",
        "enfant-m|C'est le signal.",
        "narrateur|Une miette dort près du pied de chaise.",
    ],
    (1, 2, 2): [
        "narrateur|La grande cave a deux coins, maintenant.",
        "enfant-m|Le tien, et le mien.",
        "copine|C'est le nôtre, Amir.",
        "papa|Vous avez mélangé sans tout casser.",
        "maman|Le cacao, au milieu, pour deux.",
        "narrateur|Le coussin-phare a deux empreintes.",
        "narrateur|Nina souffle, puis Amir souffle.",
        "enfant-m|On reste un peu.",
        "narrateur|Une chaise garde leur secret, penchée.",
    ],
    (1, 2, 3): [
        "narrateur|Deux jeux restent côte à côte.",
        "copine|Tu n'es pas entré, Amir.",
        "enfant-m|Tu avais dit non.",
        "papa|Le non a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "narrateur|Le coussin-phare garde sa rondeur, dehors.",
        "narrateur|Nina tend une main, sous la nappe.",
        "enfant-m|Je la prends, d'à côté.",
        "narrateur|Le bois craque, puis se tait.",
    ],
    (1, 3, 1): [
        "narrateur|Le petit jeu est fini.",
        "copine|J'ai eu le temps, juste assez.",
        "enfant-m|Merci d'être restée.",
        "papa|Vous avez compté jusqu'à trois.",
        "maman|L'autre chaussure se ferme, maintenant.",
        "narrateur|Le coussin-phare a un creux, au milieu.",
        "narrateur|Nina fait un signe vers le salon.",
        "enfant-m|Le fort t'a vue, une minute.",
        "narrateur|Le paillasson garde une petite boue.",
    ],
    (1, 3, 2): [
        "narrateur|La porte se referme, sans bruit.",
        "enfant-m|Je l'ai accompagnée.",
        "papa|Tu as marché à son pas.",
        "maman|Le manteau a pris le vent.",
        "narrateur|Le coussin-phare garde la forme de l'attente.",
        "narrateur|Amir revient vers le salon.",
        "enfant-m|Le fort attendra.",
        "papa|Il a eu son au revoir.",
        "narrateur|Une goutte sèche sur le carreau, mince.",
    ],
    (1, 3, 3): [
        "narrateur|Nina est partie, le fort reste allumé.",
        "enfant-m|Plus tard, elle a dit.",
        "enfant-m|Garde-le pour moi.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le cacao attend, au salon.",
        "narrateur|Le coussin-phare reste tiède, au milieu.",
        "narrateur|Amir souffle sur le rond jaune.",
        "enfant-m|Il t'attend, Nina.",
        "narrateur|Le tapis garde sa chaleur, au milieu.",
    ],
    (2, 1, 1): [
        "narrateur|Ils rentrent sous le bleu, à son heure.",
        "copine|La virgule de buée a fini son chemin.",
        "enfant-m|Toi aussi.",
        "papa|Vous avez attendu le bon moment.",
        "maman|Le cacao est un peu chaud.",
        "narrateur|La couverture-voile garde un pli, en drapeau.",
        "narrateur|Nina souffle sur sa tasse.",
        "enfant-m|C'est notre fort, maintenant.",
        "narrateur|La virgule de buée penche, plus fine.",
    ],
    (2, 1, 2): [
        "narrateur|Le bleu sent le savon, un peu.",
        "enfant-m|Tu as dit oui, tout bas.",
        "copine|J'avais entendu, près du verre.",
        "papa|Tu as proposé, sans tirer.",
        "maman|Buvez un peu.",
        "narrateur|La couverture-voile a un coin plus chaud.",
        "narrateur|Nina pose sa joue sur le tissu.",
        "enfant-m|Reste autant que tu veux.",
        "narrateur|Un rond de cacao fige sur la table.",
    ],
    (2, 1, 3): [
        "narrateur|Après la pluie, ils glissent sous le bleu.",
        "copine|On a regardé ensemble, d'abord.",
        "enfant-m|Puis tu as dit : on y va.",
        "maman|Deux nez, puis un même toit.",
        "papa|Le salon se tait, un moment.",
        "narrateur|La couverture-voile sent le savon, et la pluie.",
        "narrateur|Nina rit, tout petit.",
        "enfant-m|Le bleu t'a attendue.",
        "narrateur|Le verre redevient net, sans virgule.",
    ],
    (2, 2, 1): [
        "narrateur|Sous la table, ça sent le savon.",
        "copine|Ton bleu est dans ma cave.",
        "enfant-m|Tu as dit oui.",
        "papa|Vous tenez tous les deux, là-dessous.",
        "maman|Le cacao descend jusqu'à vous.",
        "narrateur|La couverture-voile porte une miette, au bord.",
        "narrateur|Nina tape deux fois, sous le bois.",
        "enfant-m|C'est le signal.",
        "narrateur|Un fil de savon brille sous la nappe.",
    ],
    (2, 2, 2): [
        "narrateur|La grande cave a deux toits, maintenant.",
        "enfant-m|Le tien, et le mien.",
        "copine|C'est le nôtre, Amir.",
        "papa|Vous avez mélangé sans tout casser.",
        "maman|Le cacao, au milieu, pour deux.",
        "narrateur|Deux coins de tissu se touchent, à peine.",
        "narrateur|Nina souffle, puis Amir souffle.",
        "enfant-m|On reste un peu.",
        "narrateur|Le pied de table garde une miette bleue.",
    ],
    (2, 2, 3): [
        "narrateur|Deux toits restent côte à côte.",
        "copine|Tu n'es pas entré, Amir.",
        "enfant-m|Tu avais dit non.",
        "papa|Le non a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "narrateur|La couverture-voile garde son savon, dehors.",
        "narrateur|Nina tend une main, sous la nappe.",
        "enfant-m|Je la prends, d'à côté.",
        "narrateur|La nappe tremble, puis s'arrête.",
    ],
    (2, 3, 1): [
        "narrateur|La cape redevient un tas.",
        "copine|J'ai eu le temps, juste assez.",
        "enfant-m|Merci d'être restée.",
        "papa|Vous avez compté jusqu'à trois.",
        "maman|L'autre chaussure se ferme, maintenant.",
        "narrateur|La couverture-voile redevient un tas, au seuil.",
        "narrateur|Nina fait un signe vers le salon.",
        "enfant-m|Le bleu t'a vue, une minute.",
        "narrateur|Une boucle de lacet attend, ouverte.",
    ],
    (2, 3, 2): [
        "narrateur|La porte se referme, sans bruit.",
        "enfant-m|Je l'ai accompagnée.",
        "papa|Tu as marché à son pas.",
        "maman|Le manteau a pris le vent.",
        "narrateur|La couverture-voile garde un pli, au seuil.",
        "narrateur|Amir revient vers le salon.",
        "enfant-m|Le bleu attendra.",
        "papa|Il a eu son au revoir.",
        "narrateur|Un lacet mouillé marque le carreau.",
    ],
    (2, 3, 3): [
        "narrateur|Nina est partie, le bleu reste au salon.",
        "enfant-m|Plus tard, elle a dit.",
        "enfant-m|Garde-le pour moi.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le cacao attend, au salon.",
        "narrateur|La couverture-voile garde un pli, au salon.",
        "narrateur|Amir souffle sur le pli.",
        "enfant-m|Il t'attend, Nina.",
        "narrateur|Un pli de savon dort sur le tapis.",
    ],
    (3, 1, 1): [
        "narrateur|Ils rentrent dans le camp, à son heure.",
        "copine|La virgule de buée a fini son chemin.",
        "enfant-m|Toi aussi.",
        "papa|Vous avez attendu le bon moment.",
        "maman|Le cacao est un peu chaud.",
        "narrateur|La lanterne fait un croissant, au tapis.",
        "narrateur|Nina souffle sur sa tasse.",
        "enfant-m|C'est notre camp, maintenant.",
        "narrateur|Le rond jaune tient sous la virgule.",
    ],
    (3, 1, 2): [
        "narrateur|Le camp sent le clic, un peu.",
        "enfant-m|Tu as dit oui, tout bas.",
        "copine|J'avais entendu, près du verre.",
        "papa|Tu as proposé, sans tirer.",
        "maman|Buvez un peu.",
        "narrateur|La lanterne a un clic plus doux.",
        "narrateur|Nina pose sa joue près du rond.",
        "enfant-m|Reste autant que tu veux.",
        "narrateur|La lanterne fait un croissant sur le tapis.",
    ],
    (3, 1, 3): [
        "narrateur|Après la pluie, ils glissent dans le camp.",
        "copine|On a regardé ensemble, d'abord.",
        "enfant-m|Puis tu as dit : on y va.",
        "maman|Deux nez, puis un même rond.",
        "papa|Le salon se tait, un moment.",
        "narrateur|Le rond jaune tient deux ombres.",
        "narrateur|Nina rit, tout petit.",
        "enfant-m|Le camp t'a attendue.",
        "narrateur|Le clic de la lanterne se tait, net.",
    ],
    (3, 2, 1): [
        "narrateur|Sous la table, ça sent le bois chaud.",
        "copine|Ton rond est dans ma cave.",
        "enfant-m|Tu as dit oui.",
        "papa|Vous tenez tous les deux, là-dessous.",
        "maman|Le cacao descend jusqu'à vous.",
        "narrateur|La lanterne porte une poussière, au verre.",
        "narrateur|Nina tape deux fois, sous le bois.",
        "enfant-m|C'est le signal.",
        "narrateur|Un rond jaune dort sous la table.",
    ],
    (3, 2, 2): [
        "narrateur|La grande cave a deux lumières, maintenant.",
        "enfant-m|Le tien, et le mien.",
        "copine|C'est le nôtre, Amir.",
        "papa|Vous avez mélangé sans tout casser.",
        "maman|Le cacao, au milieu, pour deux.",
        "narrateur|La lanterne a deux reflets, au pied.",
        "narrateur|Nina souffle, puis Amir souffle.",
        "enfant-m|On reste un peu.",
        "narrateur|Deux ronds jaunes se mêlent, au bois.",
    ],
    (3, 2, 3): [
        "narrateur|Deux lumières restent côte à côte.",
        "copine|Tu n'es pas entré, Amir.",
        "enfant-m|Tu avais dit non.",
        "papa|Le non a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "narrateur|La lanterne veille à côté, sans entrer.",
        "narrateur|Nina tend une main, sous la nappe.",
        "enfant-m|Je la prends, d'à côté.",
        "narrateur|Un grain de poussière tombe, puis plus rien.",
    ],
    (3, 3, 1): [
        "narrateur|Le petit phare est fini.",
        "copine|J'ai eu le temps, juste assez.",
        "enfant-m|Merci d'être restée.",
        "papa|Vous avez compté jusqu'à trois.",
        "maman|L'autre chaussure se ferme, maintenant.",
        "narrateur|Le clic se tait, net.",
        "narrateur|Nina fait un signe vers le salon.",
        "enfant-m|Le camp t'a vue, une minute.",
        "narrateur|Le paillasson a un rond de lumière, court.",
    ],
    (3, 3, 2): [
        "narrateur|La porte se referme, sans bruit.",
        "enfant-m|Je l'ai accompagnée.",
        "papa|Tu as marché à son pas.",
        "maman|Le manteau a pris le vent.",
        "narrateur|La lanterne garde un rond, au seuil.",
        "narrateur|Amir revient vers le salon.",
        "enfant-m|Le camp attendra.",
        "papa|Il a eu son au revoir.",
        "narrateur|Une virgule mince reste sur le carreau.",
    ],
    (3, 3, 3): [
        "narrateur|Nina est partie, le camp reste allumé.",
        "enfant-m|Plus tard, elle a dit.",
        "enfant-m|Garde-le pour moi.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le cacao attend, au salon.",
        "narrateur|Le tapis garde un rond jaune, tiède.",
        "narrateur|Amir souffle sur le rond jaune.",
        "enfant-m|Il t'attend, Nina.",
        "narrateur|La virgule de buée tient, au verre, mince.",
    ],
}

END_SONS = {1: "cacao,coussin", 2: "cacao,tissu", 3: "cacao,lampe"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "tissu,cacao",
        {"emphasis": "virgule de buée"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le coussin-phare", "la couverture-voile", "la lanterne de poche")},
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
            {"emphasis": "virgule de buée"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("la fenêtre", "sous la table", "le couloir")},
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
                    {"emphasis": "virgule"},
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
        "inviter sans forcer",
        "accepter plusieurs réponses",
        "tom ",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "virgule" not in blob:
        raise SystemExit(f"{SID}: virgule de buée absente")

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

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-021 — Le fort d'Amir près de la fenêtre\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter sans forcer (vécue : proposer, accepter oui / non / plus tard)\n"
        "- **Personnages :** Amir, Nina, papa, maman\n"
        "- **Lieu :** salon, grande fenêtre, table, couloir — campement du salon\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Papa secoue le drap à carreaux : il gonfle, retombe, couvre le fauteuil. "
        "Un toit bancal, né tout seul. La vapeur du cacao écrit une **virgule de buée** "
        "sur la grande fenêtre. Amir veut finir ce fort pour Nina, maintenant. "
        "Il tire trop vite : le fauteuil redevient un fauteuil. Première idée ratée. "
        "Coussin-phare, couverture-voile ou lanterne : les trois restent. Il crie trop tôt. "
        "Nina arrive à son pas. Fenêtre (elle suit la virgule), cave sous la table, "
        "ou couloir (une chaussure). Le silence compte. Attendre, parler bas, s'asseoir ; "
        "glisser, mélanger, rester à côté ; petit jeu, accompagner, plus tard. "
        "La virgule du début revient. L'objet porte une trace.\n\n"
        "## Vécu\n\n"
        "Amir propose. Nina prend son temps, ou pose sa limite. "
        "Deux rythmes, sans voix caricaturale. Le sourire disparaît ; "
        "envie et inquiétude se bousculent. Papa ou maman s'accroupit à la même hauteur. "
        "Personne ne donne la réponse. Amir observe l'objet, écoute le salon, "
        "retrouve la virgule. La leçon se voit : il invite, il accepte oui, non, ou une autre heure.\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Inviter sans forcer » / Tom / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (papa : le pli du drap). Question d'adulte. Un « en ce moment ».\n"
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
