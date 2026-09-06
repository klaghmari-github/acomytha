#!/usr/bin/env python3
"""TREE-AUT-012 — Le doudou sous la caisse du train (F-NAR-019, N2, AUT.RAN.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-012"
N2 = 15
TITLE = "Le doudou sous la caisse du train"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="doudou",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_doudou_doit_voir_les_champs; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_recherche; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="doudou",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_cache; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="caisse",
        note="arc=confirmation; intention=relancer; emotion=élan_prudent; intensite=1; destinataire=enfant; sous_texte=un_objet_dans_la_caisse_ouvre_un_trou; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_veut_tout_lever_d_un_coup; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_premier_geste_rate; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="doudou",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_gris_revient_quand_le_tas_descend; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="vitre",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_truffe_a_les_champs; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
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
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        starts.append(tok)
        out.append(f"{role}|{ph}")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {starts[i]}")
        else:
            run = 1
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        if e in body:
            body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp and emp in body:
        body = body.replace(emp, f"<emphasis>{emp}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    tag = m.get("pitchTag")
    if tag:
        body = f"<{tag}>{body}</{tag}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines)
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m.get("emphasis") or ""
    nc["pause_before_ms"] = extra.get("pause_before_ms", 0)
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
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


OPENING = [
    "narrateur|Le wagon sent le goûter, un peu sucré.",
    "narrateur|Une vitre froide tremble contre les champs.",
    "narrateur|Le blé se penche, jaune, puis s'en va.",
    "narrateur|Amir voyage là, avec papa et maman.",
    "narrateur|Le siège bleu gratte un peu les genoux.",
    "papa|Ta caisse est près de tes pieds ?",
    "enfant-m|Oui, le doudou va voir les vaches !",
    "maman|Il aime coller sa truffe à la vitre.",
    "narrateur|La petite table se déplie.",
    "narrateur|Ça fait clic.",
    "narrateur|En ce moment, Amir bascule la caisse.",
    "narrateur|Le ballon rouge saute sur le siège.",
    "narrateur|Des crayons tombent du seau bleu.",
    "narrateur|Un à-coup sec secoue le wagon.",
    "narrateur|Les jouets glissent en tas.",
    "enfant-m|Mon doudou, vite !",
    "narrateur|Amir plonge les deux mains dans le tas.",
    "narrateur|Le tas s'écroule vers ses genoux.",
    "narrateur|Pas de tissu gris.",
    "papa|Il était dans la caisse, non ?",
    "enfant-m|Il devait voir les champs avec moi !",
    "maman|Le tas est trop haut pour tes yeux ?",
]

T1_CHOICE = [
    "narrateur|On peut chercher le matin, après la sieste, ou le soir.",
    "papa|Quand ouvres-tu le tas, Amir ?",
]

T1 = {
    1: {
        "lab": "le matin",
        "sons": "rosée,crayon,train",
        "emphasis": "tas",
        "passage": [
            "narrateur|La lumière pâle pose un froid sur la vitre.",
            "narrateur|Des gouttes de rosée glissent, droites.",
            "enfant-m|Les champs sont mouillés, papa !",
            "papa|Oui, le blé boit l'eau de la nuit.",
            "narrateur|Amir saisit le ballon et le seau ensemble.",
            "narrateur|Ses bras sont trop petits, ça glisse.",
            "enfant-m|Je veux tout lever d'un coup !",
            "narrateur|Le ballon fuit sous la table.",
            "narrateur|Des crayons roulent contre le sac.",
            "maman|Tes mains n'y voient plus, là-dessous ?",
            "enfant-m|Le gris n'est pas là.",
            "papa|Le tas cache le fond du siège.",
            "narrateur|Amir souffle, les joues chaudes d'impatience.",
            "narrateur|Une vache passe, loin, dans l'herbe mouillée.",
        ],
        "question": [
            "narrateur|Amir a voulu tout lever d'un coup.",
            "maman|Qu'est-ce qui cache le doudou ?",
        ],
        "qfields": {
            "expected_answer": "tas",
            "accepted_examples": "tas | le tas | jouets | les jouets | le tas de jouets | dessous | sous le tas",
            "retry_prompt": "Le tas est trop haut. Qu'est-ce qui cache le doudou ?",
        },
        "confirm": [
            "enfant-m|Le tas !",
            "narrateur|Oui, le tas trop haut.",
            "narrateur|Amir glisse un crayon dans la caisse.",
            "narrateur|Toc, sur le bois.",
            "papa|Un bout de siège bleu reparaît.",
            "enfant-m|Pas lui.",
            "maman|Le fond va se montrer, un par un.",
            "narrateur|La rosée brille sur la vitre, dehors.",
        ],
    },
    2: {
        "lab": "après la sieste",
        "sons": "couverture,sac,train",
        "emphasis": "couverture",
        "passage": [
            "narrateur|Amir a les joues tièdes de la sieste.",
            "narrateur|La couverture est pliée sur le siège.",
            "maman|Tu as dormi un peu, Amir ?",
            "enfant-m|Les rails ont chanté, j'ai entendu.",
            "papa|Le train a roulé pendant que tu fermais les yeux.",
            "narrateur|Amir soulève la couverture d'un coup.",
            "enfant-m|Il dort avec moi, d'habitude !",
            "narrateur|Rien que le tissu bleu du siège.",
            "narrateur|L'odeur du goûter sort du sac.",
            "maman|Tu as regardé près du sac ?",
            "enfant-m|Non, je veux mon gris.",
            "papa|Le tas, lui, n'a pas dormi.",
            "narrateur|Amir laisse tomber la couverture.",
            "narrateur|Ses épaules baissent, un peu.",
        ],
        "question": [
            "narrateur|Amir a soulevé la couverture.",
            "papa|Où a-t-il cherché, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "couverture",
            "accepted_examples": "couverture | la couverture | sous la couverture | le plaid | le nid",
            "retry_prompt": "Il a soulevé le tissu du siège. Où a-t-il cherché ?",
        },
        "confirm": [
            "enfant-m|Sous la couverture !",
            "narrateur|Oui, et le gris n'y était pas.",
            "narrateur|Amir pose une tasse jouet dans la caisse.",
            "narrateur|Toc.",
            "maman|Le tas devient plus petit.",
            "enfant-m|Toujours pas.",
            "papa|Tu continues, un par un ?",
            "narrateur|La lumière ronde touche le bois de la table.",
        ],
    },
    3: {
        "lab": "le soir",
        "sons": "lampe,vitre,train",
        "emphasis": "vitre",
        "passage": [
            "narrateur|Les lampes du wagon sont petites, jaunes.",
            "narrateur|Dehors, le ciel vire à l'orange.",
            "enfant-m|Ça brille, maman.",
            "maman|Le soir pose des lumières dans les maisons.",
            "narrateur|Amir colle son nez à la vitre.",
            "enfant-m|Le doudou devait voir le village !",
            "narrateur|Dans la vitre, c'est son visage qui répond.",
            "narrateur|Les jouets font des ombres sur le siège.",
            "papa|Le gris se cache sous les ombres, peut-être.",
            "enfant-m|Je ne vois plus rien de gris.",
            "narrateur|Le seau a roulé contre le sac.",
            "maman|Tes yeux cherchent trop loin, non ?",
            "enfant-m|Il me manque pour la fenêtre.",
            "narrateur|Amir recule, déçu, vers le tas.",
        ],
        "question": [
            "narrateur|Amir a regardé la vitre d'abord.",
            "maman|Que voit-il dans le verre, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "visage",
            "accepted_examples": "visage | son visage | lui | Amir | son nez | moi",
            "retry_prompt": "Dans la vitre, ce n'est pas le gris. Que voit-il ?",
        },
        "confirm": [
            "enfant-m|Mon visage !",
            "narrateur|Oui, pas le doudou.",
            "narrateur|Amir pousse un cube vers la caisse.",
            "narrateur|Ça fait un petit bruit de bois.",
            "papa|Les ombres bougent, tu vois ?",
            "enfant-m|Un peu, papa.",
            "maman|Le fond du siège peut revenir.",
            "narrateur|Dehors, le ciel reste orange.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le matin reste pâle sur les champs.",
        "maman|Où cherches-tu, dans le wagon ?",
        "narrateur|La petite cuisine, le jardin de la fenêtre, ou la chambre du siège.",
    ],
    2: [
        "narrateur|La sieste a laissé ses joues tièdes.",
        "papa|Où cherches-tu, dans le wagon ?",
        "narrateur|La petite cuisine, le jardin de la fenêtre, ou la chambre du siège.",
    ],
    3: [
        "narrateur|Les lampes jaunes tremblent un peu.",
        "maman|Où cherches-tu, dans le wagon ?",
        "narrateur|La petite cuisine, le jardin de la fenêtre, ou la chambre du siège.",
    ],
}

T2 = {
    (1, 1): {
        "lab": "la cuisine",
        "sons": "gobelet,table",
        "emphasis": "gobelets",
        "passage": [
            "narrateur|La petite table du wagon devient une cuisine.",
            "narrateur|Deux gobelets attendent, sages, sur le bois.",
            "maman|On fait semblant de goûter ?",
            "enfant-m|Oui, le doudou a soif aussi.",
            "narrateur|Amir verse un jus invisible.",
            "narrateur|La place du doudou reste vide.",
            "papa|Il est sous le tas, près des gobelets ?",
            "narrateur|Amir soulève un gobelet, trop vite.",
            "narrateur|Une miette colle au bois, rien de gris.",
            "enfant-m|Je voulais le servir, d'abord.",
            "maman|Le ballon et le seau font un mur.",
            "narrateur|Amir pose le gobelet, les lèvres pincées.",
        ],
    },
    (1, 2): {
        "lab": "le jardin",
        "sons": "vitre,champs",
        "emphasis": "vitre",
        "passage": [
            "narrateur|Par la fenêtre, le wagon a un jardin de champs.",
            "narrateur|L'herbe défile, puis une haie, puis un arbre.",
            "papa|Tu vois les haies, Amir ?",
            "enfant-m|Oui, et une vache blanche et noire.",
            "narrateur|Amir pose un doigt sur la vitre froide.",
            "maman|Le doudou voulait ça, cette vue.",
            "narrateur|Les jouets sont collés contre le verre.",
            "enfant-m|Il ne peut pas voir, avec ça !",
            "narrateur|Amir écarte le tas d'un coup de bras.",
            "narrateur|Le tas revient, plus mêlé qu'avant.",
            "papa|Tes bras font un plus grand tas.",
            "enfant-m|Je suis fatigué.",
        ],
    },
    (1, 3): {
        "lab": "la chambre",
        "sons": "couverture,tissu",
        "emphasis": "nid",
        "passage": [
            "narrateur|Le siège bleu devient une petite chambre.",
            "maman|On fait un nid avec la couverture ?",
            "enfant-m|Oui, il aime le chaud.",
            "narrateur|Amir tire la couverture sur ses genoux.",
            "narrateur|Le tissu sent le savon propre.",
            "papa|La chambre du train est prête.",
            "narrateur|Les jouets sont dans le nid du siège.",
            "enfant-m|Il est dans le pli, je crois.",
            "narrateur|Amir soulève un coin, trop fort.",
            "narrateur|Le ballon et le seau glissent sous le bord.",
            "maman|Le pli est vide, tu vois ?",
            "enfant-m|Le nid n'a pas de gris.",
        ],
    },
    (2, 1): {
        "lab": "la cuisine",
        "sons": "gobelet,goûter",
        "emphasis": "goûter",
        "passage": [
            "narrateur|Après la sieste, la table sent le goûter.",
            "narrateur|Deux gobelets attendent près du sac sucré.",
            "maman|Une gorgée, puis on cherche ?",
            "enfant-m|Le doudou boit d'abord.",
            "narrateur|Amir pousse un gobelet vers la place vide.",
            "narrateur|Rien ne le tient.",
            "papa|Il n'est pas à table, lui.",
            "narrateur|Amir se penche sous le bois.",
            "narrateur|L'odeur du gâteau, pas le tissu gris.",
            "enfant-m|Je le voulais pour le goûter.",
            "maman|Le tas garde sa cachette.",
            "narrateur|Amir rentre la tête, déçu.",
        ],
    },
    (2, 2): {
        "lab": "le jardin",
        "sons": "vitre,arbre",
        "emphasis": "arbre",
        "passage": [
            "narrateur|La vitre est tiède, après la sieste.",
            "narrateur|Un arbre passe, lent, dans le jardin des champs.",
            "papa|Il s'éloigne, tu le suis des yeux ?",
            "enfant-m|Le doudou devait le voir.",
            "narrateur|Amir frotte la buée d'un poing.",
            "narrateur|Un rond clair s'ouvre, puis se referme.",
            "maman|Tes jouets collent au verre, là.",
            "narrateur|Amir tire le seau, le ballon bascule.",
            "narrateur|Le tas se tasse contre la fenêtre.",
            "enfant-m|Ça cache tout l'arbre !",
            "papa|Plus tu tires, plus ça bouche.",
            "narrateur|Amir laisse ses mains, lourdes.",
        ],
    },
    (2, 3): {
        "lab": "la chambre",
        "sons": "couverture,siège",
        "emphasis": "couverture",
        "passage": [
            "narrateur|Le nid du siège est tiède, comme les joues.",
            "narrateur|La couverture garde la forme d'Amir.",
            "maman|Tu le cherches dans ton sommeil ?",
            "enfant-m|Il était contre moi, avant.",
            "narrateur|Amir fouille le pli, doigt après doigt.",
            "narrateur|Un coin de tissu bleu, seulement.",
            "papa|Les jouets ont pris sa place, dans le nid.",
            "narrateur|Amir soulève le ballon du nid.",
            "narrateur|Le seau reste, lourd, sur le tissu.",
            "enfant-m|Le nid est trop plein.",
            "maman|Trop plein pour voir le fond.",
            "narrateur|Amir pose sa joue sur le vide du pli.",
        ],
    },
    (3, 1): {
        "lab": "la cuisine",
        "sons": "lampe,gobelet",
        "emphasis": "lampe",
        "passage": [
            "narrateur|Sous la lampe jaune, les gobelets font des ombres.",
            "narrateur|Un rond orange danse au fond d'une tasse.",
            "enfant-m|On dirait un jus de ciel.",
            "maman|C'est le soir dans ta cuisine.",
            "narrateur|Amir regarde au fond des deux gobelets.",
            "narrateur|Pas de truffe, pas de gris.",
            "papa|Il n'habite pas les tasses, tu sais.",
            "enfant-m|Je croyais le voir dans l'ombre.",
            "narrateur|Le tas, sous la lampe, devient une montagne noire.",
            "maman|Tes yeux suivent les ombres, pas le bois.",
            "narrateur|Amir cligne, fatigué de chercher trop haut.",
            "narrateur|Un village passe, minuscule, derrière la vitre.",
        ],
    },
    (3, 2): {
        "lab": "le jardin",
        "sons": "vitre,village",
        "emphasis": "village",
        "passage": [
            "narrateur|Le jardin de la fenêtre s'allume, loin.",
            "narrateur|Des maisons allument des carrés jaunes.",
            "papa|Le village dit bonsoir, tu vois ?",
            "enfant-m|Le doudou devait dire bonsoir aussi.",
            "narrateur|Amir cherche une truffe dans le reflet.",
            "narrateur|Il ne trouve que son œil, orange.",
            "maman|Le tas fait une montagne contre le verre.",
            "narrateur|Amir pousse la montagne d'un genou.",
            "narrateur|Elle glisse, et cache plus de lumières.",
            "enfant-m|Je ne vois plus le village !",
            "papa|Le genou n'a pas aidé.",
            "narrateur|Amir retire le genou, honteux un peu.",
        ],
    },
    (3, 3): {
        "lab": "la chambre",
        "sons": "lampe,couverture",
        "emphasis": "ombres",
        "passage": [
            "narrateur|Sous la lampe, le nid du siège a des ombres.",
            "narrateur|Les jouets y dessinent des bêtes noires.",
            "maman|On dirait une forêt, sur tes genoux.",
            "enfant-m|Le doudou a peur des ombres ?",
            "papa|Ou il est dessous, c'est tout.",
            "narrateur|Amir lève la couverture comme un rideau.",
            "narrateur|Le ballon et le seau glissent sous le siège.",
            "enfant-m|Ils tombent dans le noir !",
            "maman|Le bord a mangé tes jouets.",
            "narrateur|Amir se penche, le cœur serré.",
            "narrateur|Ses doigts touchent le plastique, pas le gris.",
            "papa|On les reprend, un par un, d'accord ?",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Les gobelets attendent sur la table.",
        "papa|Quel jouet prends-tu, pour voir dessous ?",
        "maman|Le ballon, le seau, ou le doudou ?",
    ],
    2: [
        "narrateur|La vitre garde un bout de champ.",
        "papa|Quel jouet prends-tu, pour voir dessous ?",
        "maman|Le ballon, le seau, ou le doudou ?",
    ],
    3: [
        "narrateur|Le nid du siège attend, un peu vide.",
        "papa|Quel jouet prends-tu, pour voir dessous ?",
        "maman|Le ballon, le seau, ou le doudou ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "narrateur|Amir prend le ballon à deux mains.",
        "narrateur|Il est souple, un peu rouge, une miette dessus.",
        "enfant-m|Toi, tu vas dans la caisse.",
        "narrateur|Le ballon tombe dans le bois, toc.",
        "narrateur|Sous sa place, un coin de tissu gris.",
        "enfant-m|Mon doudou !",
        "maman|Te voilà, petit.",
        "papa|Merci, tu as ouvert un trou.",
        "narrateur|Amir essuie la miette, puis serre le gris.",
        "narrateur|Une goutte de rosée mouille l'oreille du doudou.",
    ],
    (1, 1, 2): [
        "narrateur|Amir soulève le seau bleu.",
        "narrateur|Un crayon jaune reste collé au fond.",
        "enfant-m|Le seau, dans la caisse.",
        "narrateur|Le seau glisse, droit, toc.",
        "narrateur|Sous le seau, le tissu gris attend.",
        "enfant-m|Il était là !",
        "papa|Merci, le bois a rendu sa cachette.",
        "maman|Le crayon peut rouler vers le gobelet.",
        "narrateur|Amir pose le doudou contre sa joue.",
        "narrateur|Le crayon jaune avance, lent, vers la tasse.",
    ],
    (1, 1, 3): [
        "narrateur|Amir écarte un cube, puis un autre.",
        "narrateur|Un trou s'ouvre au milieu du tas.",
        "enfant-m|Il reste un trou.",
        "narrateur|Au fond du trou, le doudou gris.",
        "narrateur|Il sent la maison, un peu.",
        "enfant-m|Je t'ai trouvé.",
        "maman|Merci, tu as regardé le fond.",
        "papa|Les gobelets ont de la place, maintenant.",
        "narrateur|Amir glisse le ballon et le seau dans la caisse.",
        "narrateur|Une miette reste collée à l'oreille grise.",
    ],
    (1, 2, 1): [
        "narrateur|Amir décroche le ballon de la vitre froide.",
        "narrateur|Un rond de champ vert reste sur sa peau.",
        "enfant-m|Tu bouchais la vache.",
        "narrateur|Le ballon rentre dans la caisse, souple.",
        "narrateur|Un coin gris apparaît contre le verre.",
        "enfant-m|Il voyait les champs, lui !",
        "papa|Merci, la vitre est libre.",
        "maman|La vache est à lui, cette fois.",
        "narrateur|Amir colle la truffe grise au froid.",
        "narrateur|Le ballon garde son rond vert, dans le bois.",
    ],
    (1, 2, 2): [
        "narrateur|Amir tire le seau loin de la haie qui défile.",
        "narrateur|Une goutte de rosée tremble au bord bleu.",
        "enfant-m|Le seau buvait la fenêtre.",
        "narrateur|Le seau rentre, et la goutte tombe, ploc.",
        "narrateur|Sous lui, le doudou était plaqué au verre.",
        "enfant-m|Il était collé !",
        "maman|Merci, tu as décollé sa vue.",
        "papa|La haie peut passer, claire.",
        "narrateur|Amir essuie le gris d'un pouce.",
        "narrateur|La goutte a laissé un trait sur la vitre.",
    ],
    (1, 2, 3): [
        "narrateur|Amir fait un trou contre la vitre mouillée.",
        "narrateur|Ses doigts trouvent le poil gris, froid.",
        "enfant-m|Il regardait la vache, sans moi.",
        "narrateur|Le doudou se décolle du verre, lent.",
        "maman|Merci, tu l'as pris sans tirer trop fort.",
        "papa|Le tas peut descendre, maintenant.",
        "narrateur|Amir pose ballon et seau dans la caisse.",
        "narrateur|La vache est toute proche, un instant.",
        "enfant-m|Regarde, c'est pour toi.",
        "narrateur|Le nez gris touche la vache, puis l'herbe.",
    ],
    (1, 3, 1): [
        "narrateur|Amir sort le ballon du nid du matin.",
        "narrateur|Le rouge s'enfonce un peu dans la couverture.",
        "enfant-m|Tu prenais sa place, toi.",
        "narrateur|Le ballon va dans la caisse, malgré le pli.",
        "narrateur|Sous le rouge, un coin gris, chaud.",
        "enfant-m|Il était dans mon nid !",
        "papa|Merci, le nid a rendu son secret.",
        "maman|Il peut aller à la vitre, s'il veut.",
        "narrateur|Amir porte le doudou du pli au verre.",
        "narrateur|Le ballon s'enfonce dans le bois, sous le tissu.",
    ],
    (1, 3, 2): [
        "narrateur|Amir cherche le seau dans le pli du nid.",
        "narrateur|Un crayon a glissé sous la couverture.",
        "enfant-m|Le seau et le crayon, dehors.",
        "narrateur|Le seau rentre dans la caisse, le crayon aussi.",
        "narrateur|Le fond du nid montre le gris.",
        "enfant-m|Il était sous le bleu !",
        "maman|Merci, tu as vidé le pli.",
        "papa|La chambre du siège respire.",
        "narrateur|Amir soulève le doudou, tiède d'avoir dormi là.",
        "narrateur|Le crayon reste sage, dans le seau, dans le bois.",
    ],
    (1, 3, 3): [
        "narrateur|Amir ouvre le pli chaud du nid, avec soin.",
        "narrateur|Au fond, le doudou était gris, ramassé.",
        "enfant-m|Tu étais dans ma chambre.",
        "maman|Merci, tu as regardé le fond du nid.",
        "papa|Les autres peuvent rentrer, maintenant.",
        "narrateur|Amir glisse le ballon, puis le seau.",
        "narrateur|Le nid du siège se vide.",
        "enfant-m|Maintenant, la vitre.",
        "narrateur|Le doudou quitte le pli pour le froid du verre.",
        "narrateur|Une goutte de rosée l'accueille sur le nez.",
    ],
    (2, 1, 1): [
        "narrateur|Amir prend le ballon, tiède comme sa joue.",
        "narrateur|Il sent un peu la couverture de la sieste.",
        "enfant-m|Dans la caisse, toi.",
        "narrateur|Le ballon tombe, toc, près des gobelets.",
        "narrateur|Sous lui, le gris a une marque de joue.",
        "enfant-m|Il a dormi contre moi !",
        "papa|Merci, tu as rendu sa place à table.",
        "maman|Il peut goûter des yeux, à la vitre.",
        "narrateur|Amir porte le doudou vers le verre tiède.",
        "narrateur|Le ballon reste tiède, lui, au fond du bois.",
    ],
    (2, 1, 2): [
        "narrateur|Amir soulève le seau, qui a senti la couverture.",
        "narrateur|Des miettes de goûter collent au bord.",
        "enfant-m|Tu sentais le gâteau, toi.",
        "narrateur|Le seau rentre, et les miettes restent sur le bois.",
        "narrateur|Le doudou était sous le bleu, près du sac.",
        "enfant-m|Près du goûter !",
        "maman|Merci, tu as vidé le coin sucré.",
        "papa|La table a de l'air, autour des tasses.",
        "narrateur|Amir souffle une miette du poil gris.",
        "narrateur|Le seau, dans la caisse, garde une odeur de gâteau.",
    ],
    (2, 1, 3): [
        "narrateur|Amir écarte les gobelets, puis le tas.",
        "narrateur|Un trou s'ouvre près du sac de goûter.",
        "enfant-m|Là, près du sucre.",
        "narrateur|Le doudou a une joue un peu marquée.",
        "maman|Merci, tu as cherché près de l'odeur.",
        "papa|Le fond de la table est à lui.",
        "narrateur|Amir met ballon et seau dans la caisse.",
        "enfant-m|On goûte à la fenêtre, nous.",
        "narrateur|Le doudou regarde les champs, la marque au chaud.",
        "narrateur|Une miette reste sur l'oreille, minuscule.",
    ],
    (2, 2, 1): [
        "narrateur|Amir décroche le ballon de la vitre tiède.",
        "narrateur|Le rouge a un grain de lumière ronde.",
        "enfant-m|Tu bouchais l'arbre.",
        "narrateur|Le ballon rentre, et l'arbre reparaît, loin.",
        "narrateur|Le doudou était plié contre le verre chaud.",
        "enfant-m|Il a vu l'arbre sans moi.",
        "papa|Merci, la fenêtre respire.",
        "maman|L'arbre s'éloigne, il peut le suivre.",
        "narrateur|Amir lève le gris à hauteur de l'arbre.",
        "narrateur|Le ballon touche le bois, puis se tait.",
    ],
    (2, 2, 2): [
        "narrateur|Amir prend le seau collé à la buée.",
        "narrateur|Un grain de lumière ronde dort au fond.",
        "enfant-m|Tu as un soleil, dedans.",
        "narrateur|Le seau rentre, le grain s'éteint.",
        "narrateur|Sous le bleu, le doudou regardait l'arbre.",
        "enfant-m|Il a eu le soleil, lui.",
        "maman|Merci, tu as rendu le verre.",
        "papa|L'arbre a de la place, maintenant.",
        "narrateur|Amir essuie la buée d'un pouce, pour le gris.",
        "narrateur|Au fond du seau, plus de grain, plus de lumière.",
    ],
    (2, 2, 3): [
        "narrateur|Amir ouvre un trou contre la vitre tiède.",
        "narrateur|Ses doigts trouvent le gris, un peu humide.",
        "enfant-m|Tu regardais l'arbre, sans moi.",
        "maman|Merci, tu l'as pris sans frotter trop fort.",
        "papa|Le tas peut quitter le verre.",
        "narrateur|Amir pose ballon et seau dans la caisse.",
        "narrateur|L'arbre s'éloigne, petit.",
        "enfant-m|Regarde-le, avant qu'il parte.",
        "narrateur|Le doudou suit l'arbre, sans un mot.",
        "narrateur|La buée reprend, autour de sa truffe.",
    ],
    (2, 3, 1): [
        "narrateur|Amir sort le ballon du nid tiède.",
        "narrateur|Le rouge a gardé la chaleur de la sieste.",
        "enfant-m|Tu étais dans mon sommeil.",
        "narrateur|Le ballon quitte le nid pour la caisse.",
        "narrateur|Sous lui, le doudou a la forme du pli.",
        "enfant-m|Il a dormi en rond !",
        "papa|Merci, le nid a dit son secret.",
        "maman|Il peut se réveiller à la vitre.",
        "narrateur|Amir déplie le gris, sans brusquer.",
        "narrateur|Le ballon s'endort au fond du bois, lui.",
    ],
    (2, 3, 2): [
        "narrateur|Amir soulève le seau du nid, lourd.",
        "narrateur|La couverture se creuse, vide.",
        "enfant-m|Tu pesais sur lui.",
        "narrateur|Le seau rentre près de la couverture pliée.",
        "narrateur|Le doudou était plat, sous le bleu.",
        "enfant-m|Il ne pouvait plus respirer.",
        "maman|Merci, tu as enlevé le poids.",
        "papa|Le nid est léger, maintenant.",
        "narrateur|Amir gonfle un peu le gris, d'un souffle.",
        "narrateur|Le seau, dans la caisse, ne pèse plus sur personne.",
    ],
    (2, 3, 3): [
        "narrateur|Amir ouvre le nid tiède, sans le jeter.",
        "narrateur|Au fond, le doudou a une joue marquée.",
        "enfant-m|Tu as dormi dans ma chambre.",
        "maman|Merci, tu as regardé le fond du pli.",
        "papa|Le ballon et le seau peuvent rentrer.",
        "narrateur|Amir les glisse dans la caisse, un puis l'autre.",
        "narrateur|Le nid du siège se vide, enfin.",
        "enfant-m|Du nid à la vitre.",
        "narrateur|Le doudou passe des bras au verre tiède.",
        "narrateur|La marque de joue s'efface, un peu, contre le champ.",
    ],
    (3, 1, 1): [
        "narrateur|Amir prend le ballon sous la lampe jaune.",
        "narrateur|Un rond de lampe reste sur le rouge.",
        "enfant-m|Tu avais une lune, toi.",
        "narrateur|Le ballon tombe dans la caisse, toc.",
        "narrateur|Sous lui, le doudou a un ventre orange.",
        "enfant-m|Le soir est sur lui !",
        "papa|Merci, la table a perdu sa lune.",
        "maman|Il peut porter l'orange à la vitre.",
        "narrateur|Amir lève le gris vers les lampes du village.",
        "narrateur|Le ballon garde son rond jaune, dans le bois.",
    ],
    (3, 1, 2): [
        "narrateur|Amir soulève le seau sous la lampe.",
        "narrateur|Le bleu cliquette, bas, puis se tait.",
        "enfant-m|Tu faisais trop d'ombre.",
        "narrateur|Le seau glisse dans la caisse, silencieux.",
        "narrateur|Le doudou était dans l'ombre du bleu.",
        "enfant-m|Je te vois, maintenant.",
        "maman|Merci, tu as ôté la montagne noire.",
        "papa|Les gobelets ont leur lampe, à eux.",
        "narrateur|Amir porte le gris vers le ciel orange.",
        "narrateur|Le seau, dans le bois, ne cliquette plus.",
    ],
    (3, 1, 3): [
        "narrateur|Amir écarte les gobelets, sous la lampe.",
        "narrateur|Un trou s'ouvre dans l'ombre de la table.",
        "enfant-m|Là, dans le noir jaune.",
        "narrateur|Le doudou a un reflet orange sur le ventre.",
        "maman|Merci, tu as cherché sous les ombres.",
        "papa|Le fond de la cuisine est à lui.",
        "narrateur|Amir met ballon et seau dans la caisse.",
        "enfant-m|Le soir, c'est pour nous deux.",
        "narrateur|Le doudou voit les maisons s'allumer.",
        "narrateur|Un reflet orange s'allonge sur le ventre gris.",
    ],
    (3, 2, 1): [
        "narrateur|Amir décroche le ballon de la vitre orange.",
        "narrateur|Le rouge a vu les lumières du village.",
        "enfant-m|Tu prenais son bonsoir.",
        "narrateur|Le ballon rentre, une seconde de lumières en moins.",
        "narrateur|Le doudou était là, collé au soir.",
        "enfant-m|Il disait bonsoir, lui.",
        "papa|Merci, la vitre lui rend le village.",
        "maman|Les carrés jaunes sont à sa truffe.",
        "narrateur|Amir pose le gris contre l'orange du verre.",
        "narrateur|Le ballon, dans la caisse, n'a plus de village.",
    ],
    (3, 2, 2): [
        "narrateur|Amir tire le seau loin du ciel orange.",
        "narrateur|Un instant, le ciel entre dans le bleu.",
        "enfant-m|Tu as un soir, dedans.",
        "narrateur|Le seau rentre, et le ciel s'en va.",
        "narrateur|Sous lui, le doudou regardait les maisons.",
        "enfant-m|Il a eu le ciel, une seconde.",
        "maman|Merci, tu as rendu la fenêtre.",
        "papa|Le village peut rentrer dans ses yeux.",
        "narrateur|Amir essuie l'orange du poil, d'un doigt.",
        "narrateur|Au fond du seau, plus de ciel, plus d'orange.",
    ],
    (3, 2, 3): [
        "narrateur|Amir fait un trou contre la vitre orange.",
        "narrateur|Ses doigts trouvent le gris, tiède du verre.",
        "enfant-m|Tu étais le village, presque.",
        "maman|Merci, tu l'as pris face aux lumières.",
        "papa|Le tas peut quitter le soir.",
        "narrateur|Amir pose ballon et seau dans la caisse.",
        "narrateur|Les maisons restent, petites, jaunes.",
        "enfant-m|Dis-leur bonsoir.",
        "narrateur|Le nez du doudou colle à la vitre orange.",
        "narrateur|Un carré jaune s'allume, pile dans son œil.",
    ],
    (3, 3, 1): [
        "narrateur|Amir sort le ballon du nid, sous la lampe.",
        "narrateur|Le rouge s'endort presque, dans ses mains.",
        "enfant-m|Tu dors dans la caisse, toi.",
        "narrateur|Le ballon s'enfonce dans le bois, sous la lampe.",
        "narrateur|Sous lui, le doudou a un pli de couverture.",
        "enfant-m|Il voulait le nid et la vitre.",
        "papa|Merci, le nid a lâché le rouge.",
        "maman|Il peut finir le soir au verre.",
        "narrateur|Amir porte le gris du nid à la vitre orange.",
        "narrateur|Le ballon s'endort dans la caisse, sous la lampe jaune.",
    ],
    (3, 3, 2): [
        "narrateur|Amir soulève le seau du nid du soir.",
        "narrateur|Un cliquetis bas, puis plus rien.",
        "enfant-m|Tu restes près du nid, dans le bois.",
        "narrateur|Le seau rentre, près de la couverture pliée.",
        "narrateur|Le doudou était sous le bleu, dans l'ombre.",
        "enfant-m|Je t'ai eu.",
        "maman|Merci, tu as vidé le nid noir.",
        "papa|Le village passe, il peut le voir.",
        "narrateur|Amir lève le gris vers les maisons.",
        "narrateur|Le seau rentre près du nid, et le village glisse.",
    ],
    (3, 3, 3): [
        "narrateur|Amir ouvre le nid sous la lampe, avec soin.",
        "narrateur|Au fond, le doudou a un ventre orange.",
        "enfant-m|Tu as pris le soir avec toi.",
        "maman|Merci, tu as regardé le fond des ombres.",
        "papa|Ballon et seau peuvent rentrer.",
        "narrateur|Amir les glisse dans la caisse, sans bruit.",
        "narrateur|Le nid du siège se tait.",
        "enfant-m|On s'endort à la vitre, nous.",
        "narrateur|Le doudou s'endort contre la vitre orange.",
        "narrateur|Les champs noircissent, et les rails chantent bas.",
    ],
}

T3_SONS = {1: "ballon,bois", 2: "seau,crayon", 3: "tissu,vitre"}
T3_EMPH = {1: "ballon", 2: "seau", 3: "doudou"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Amir tient le doudou contre la vitre pâle.",
        "papa|Il voit les champs, maintenant ?",
        "enfant-m|Oui, l'oreille est mouillée de rosée.",
        "maman|La caisse est calme, sous la table.",
        "narrateur|Le ballon ne roule plus, dans le bois.",
        "narrateur|La rosée de la vitre mouille l'oreille du doudou.",
    ],
    (1, 1, 2): [
        "narrateur|Amir pose le gris entre les gobelets et le verre.",
        "papa|Le crayon a trouvé sa tasse ?",
        "enfant-m|Oui, il dort dans le seau, près du gobelet.",
        "maman|Merci, la cuisine du wagon est nette.",
        "narrateur|Dehors, le blé boit sa dernière goutte.",
        "narrateur|Un crayon jaune dort dans le seau, près du gobelet.",
    ],
    (1, 1, 3): [
        "narrateur|Amir souffle la miette de l'oreille grise.",
        "papa|Elle voulait voyager, cette miette ?",
        "enfant-m|Non, les champs, c'est pour lui.",
        "maman|Les gobelets restent vides, bien droits.",
        "narrateur|Le trou du tas n'est plus un trou.",
        "narrateur|Une miette reste collée au ventre gris, face aux champs.",
    ],
    (1, 2, 1): [
        "narrateur|Amir et le doudou regardent la vache ensemble.",
        "papa|Le ballon a gardé un peu de champ ?",
        "enfant-m|Un rond vert, sur sa peau, dans la caisse.",
        "maman|La vitre est à vous deux, maintenant.",
        "narrateur|La vache baisse la tête, puis part.",
        "narrateur|Le ballon garde un rond de champ, vert, sur sa peau.",
    ],
    (1, 2, 2): [
        "narrateur|Amir suit du doigt le trait de la goutte.",
        "papa|C'est sa rivière, à lui ?",
        "enfant-m|Une petite, juste pour le nez gris.",
        "maman|La haie passe, claire, sans le seau.",
        "narrateur|Le bleu, dans la caisse, n'a plus de rosée.",
        "narrateur|Une goutte de rosée tremble au bord du verre, puis tombe.",
    ],
    (1, 2, 3): [
        "narrateur|La vache est si près que le poil gris la touche, presque.",
        "papa|Elle te dit bonjour, tu crois ?",
        "enfant-m|Elle dit bonjour à lui.",
        "maman|Tu as vidé le verre, pour ça.",
        "narrateur|L'herbe mouillée glisse, puis une autre vache.",
        "narrateur|Le doudou voit une vache, collé à la vitre froide.",
    ],
    (1, 3, 1): [
        "narrateur|Amir a quitté le nid, le doudou contre le verre.",
        "papa|Le ballon a pris le pli, lui ?",
        "enfant-m|Il dort sous le tissu, dans la caisse.",
        "maman|Ta chambre du siège est vide, et c'est bien.",
        "narrateur|Le savon du tissu reste, loin du gris.",
        "narrateur|Le ballon s'enfonce dans la caisse, sous la couverture.",
    ],
    (1, 3, 2): [
        "narrateur|Amir cale le doudou au bord du nid, face aux champs.",
        "papa|Le crayon a fini de glisser ?",
        "enfant-m|Il est sage, dans le seau, dans le bois.",
        "maman|Merci, le pli n'a plus de secret.",
        "narrateur|Le siège bleu reparaît, net.",
        "narrateur|Un crayon a glissé dans le pli, puis dans le seau.",
    ],
    (1, 3, 3): [
        "narrateur|Le doudou a le froid du verre, après le chaud du pli.",
        "papa|Deux maisons, le nid et la vitre ?",
        "enfant-m|La vitre, pour les vaches, le nid, pour plus tard.",
        "maman|Le nid du siège est vide, maintenant.",
        "narrateur|Une goutte accueille le nez, puis s'en va.",
        "narrateur|Le doudou quitte le pli chaud pour le froid de la vitre.",
    ],
    (2, 1, 1): [
        "narrateur|Amir a la joue contre le gris, à la table.",
        "papa|Il est tiède comme toi ?",
        "enfant-m|Comme après la sieste, papa.",
        "maman|Les gobelets n'attendent plus personne.",
        "narrateur|Le goûter sent moins, le sac est fermé.",
        "narrateur|Le ballon est tiède, comme la joue d'Amir après la sieste.",
    ],
    (2, 1, 2): [
        "narrateur|Amir pose le doudou près du sac, puis le lève au verre.",
        "papa|L'odeur du gâteau, c'est fini ?",
        "enfant-m|Le seau l'a gardée, dans la caisse.",
        "maman|Merci, la table n'a plus de miettes pour cacher.",
        "narrateur|Un gobelet brille, vide, au soleil rond.",
        "narrateur|Le seau a senti la couverture, un instant, puis la caisse.",
    ],
    (2, 1, 3): [
        "narrateur|Amir montre au doudou le champ, la marque au chaud.",
        "papa|C'est ta joue, sur lui ?",
        "enfant-m|On a dormi collés.",
        "maman|Le trou près du sac n'est plus un trou.",
        "narrateur|Les gobelets se touchent, toc, sans main.",
        "narrateur|Une marque de joue reste sur le tissu gris.",
    ],
    (2, 2, 1): [
        "narrateur|Amir lève le doudou à la hauteur de l'arbre qui part.",
        "papa|Il le rattrape ?",
        "enfant-m|Presque, du bout du nez.",
        "maman|Le ballon, lui, a fini de boucher.",
        "narrateur|L'arbre devient un point, puis plus rien.",
        "narrateur|Le ballon touche la vitre tiède, puis rentre dans le bois.",
    ],
    (2, 2, 2): [
        "narrateur|Amir et le doudou regardent le verre, sans buée.",
        "papa|Le grain de lumière, il est où ?",
        "enfant-m|Il a dormi au fond du seau, puis plus.",
        "maman|La fenêtre est à vous, ronde et claire.",
        "narrateur|Un oiseau passe, minuscule, dans le jardin du train.",
        "narrateur|Un grain de lumière ronde dort au fond du seau.",
    ],
    (2, 2, 3): [
        "narrateur|La truffe grise suit l'arbre, jusqu'au bout.",
        "papa|Il dit au revoir ?",
        "enfant-m|Sans un mot, comme les arbres.",
        "maman|Tu as rendu le verre, pour cet adieu.",
        "narrateur|La buée revient, douce, autour du nez.",
        "narrateur|Le doudou suit un arbre qui s'éloigne, sans un mot.",
    ],
    (2, 3, 1): [
        "narrateur|Amir a quitté le nid tiède, le doudou réveillé.",
        "papa|Le ballon a pris le sommeil ?",
        "enfant-m|Il dort au fond, à ma place.",
        "maman|Ta chambre du siège n'a plus de tas.",
        "narrateur|La couverture reste pliée, sans forme d'enfant.",
        "narrateur|Le ballon quitte le nid tiède pour le fond de la caisse.",
    ],
    (2, 3, 2): [
        "narrateur|Amir souffle une dernière fois sur le gris.",
        "papa|Il respire, maintenant ?",
        "enfant-m|Oui, le seau ne pèse plus.",
        "maman|Merci, le nid est léger comme une sieste finie.",
        "narrateur|Le siège bleu se voit, entier.",
        "narrateur|Le seau rentre, et la couverture reste pliée, vide.",
    ],
    (2, 3, 3): [
        "narrateur|Amir cale le doudou entre le nid et la vitre.",
        "papa|Les deux maisons, tu les gardes ?",
        "enfant-m|Le nid pour plus tard, les champs pour maintenant.",
        "maman|La marque s'en va, contre le verre.",
        "narrateur|Un champ de blé se penche, comme au début.",
        "narrateur|Le doudou passe du nid aux bras, puis à la vitre.",
    ],
    (3, 1, 1): [
        "narrateur|Amir montre au doudou les lampes du village.",
        "papa|Le ballon a gardé sa lune ?",
        "enfant-m|Dans la caisse, une lune jaune, à lui.",
        "maman|Ta cuisine du soir n'a plus de montagne.",
        "narrateur|Un gobelet capte un rond de lampe, puis le perd.",
        "narrateur|Le ballon a un rond de lampe jaune, dans la caisse.",
    ],
    (3, 1, 2): [
        "narrateur|Amir et le doudou écoutent : plus de cliquetis.",
        "papa|Le seau s'est tu ?",
        "enfant-m|Oui, l'ombre est partie avec lui.",
        "maman|Merci, la table a sa lampe, claire.",
        "narrateur|Le ciel orange entre un instant dans un gobelet.",
        "narrateur|Le seau cliquette sous la lampe, puis se tait pour de bon.",
    ],
    (3, 1, 3): [
        "narrateur|Amir cale le doudou entre les gobelets et le soir.",
        "papa|Le ventre orange, c'est le village ?",
        "enfant-m|C'est le soir, sur lui.",
        "maman|Les ombres de la table n'ont plus de secret.",
        "narrateur|Une maison s'allume, minuscule.",
        "narrateur|Un reflet orange s'allonge sur le ventre du doudou.",
    ],
    (3, 2, 1): [
        "narrateur|Amir et le doudou disent bonsoir aux carrés jaunes.",
        "papa|Le ballon n'a plus de village ?",
        "enfant-m|Il l'a rendu, papa.",
        "maman|La vitre orange est à sa truffe.",
        "narrateur|Un carré s'éteint, un autre s'allume.",
        "narrateur|Le ballon voit les lumières du village, une seconde, plus jamais.",
    ],
    (3, 2, 2): [
        "narrateur|Amir regarde le seau, puis le ciel, puis le gris.",
        "papa|Trois soirs ?",
        "enfant-m|Un seul, le vrai, à la vitre.",
        "maman|Le bleu n'a plus de ciel, c'est mieux.",
        "narrateur|Le village glisse, lent, vers la gauche.",
        "narrateur|Le ciel orange entre dans le seau, puis s'en va.",
    ],
    (3, 2, 3): [
        "narrateur|Le nez gris a un carré jaune pile dans l'œil.",
        "papa|C'est sa lampe, à lui ?",
        "enfant-m|Sa maison, dans le village.",
        "maman|Tu as vidé le verre, pour ce bonsoir.",
        "narrateur|Les rails chantent, bas, sous le soir.",
        "narrateur|Le nez du doudou colle à la vitre orange du soir.",
    ],
    (3, 3, 1): [
        "narrateur|Amir a le doudou au verre, le nid derrière lui.",
        "papa|Le ballon dort pour vous deux ?",
        "enfant-m|Sous la lampe, dans la caisse, oui.",
        "maman|Ta chambre du soir a rendu le gris.",
        "narrateur|La couverture ne fait plus de forêt d'ombres.",
        "narrateur|Le ballon s'endort dans la caisse, sous la lampe jaune.",
    ],
    (3, 3, 2): [
        "narrateur|Amir lève le doudou : le village passe, pile.",
        "papa|Le seau a laissé le nid ?",
        "enfant-m|Il est rentré, près de la couverture.",
        "maman|Merci, plus de cliquetis dans les ombres.",
        "narrateur|Une maison jaune traverse l'œil du gris.",
        "narrateur|Le seau rentre près du nid, et le village passe.",
    ],
    (3, 3, 3): [
        "narrateur|Amir et le doudou ferment les yeux, un peu, au verre.",
        "papa|Vous dormez sur les champs ?",
        "enfant-m|On les regarde, jusqu'au noir.",
        "maman|Le nid est vide, la caisse est pleine, c'est bien.",
        "narrateur|Un dernier carré jaune s'éteint, loin.",
        "narrateur|Les champs noircissent, et le doudou reste contre la vitre.",
    ],
}

END_SONS = {1: "gobelet,table", 2: "vitre,champs", 3: "couverture,rails"}


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_truffe_a_les_champs; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


def path_words(chunks_by_id: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(chunks_by_id[i]["text"]) for i in ids)


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "train,vitre,caisse"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {
            "fields": {
                "option_1_label": "le matin",
                "option_2_label": "après la sieste",
                "option_3_label": "le soir",
            }
        },
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
            T2_CHOICE[a],
            "choice",
            "",
            {
                "fields": {
                    "option_1_label": "la cuisine",
                    "option_2_label": "le jardin",
                    "option_3_label": "la chambre",
                }
            },
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
                {
                    "fields": {
                        "option_1_label": "le ballon",
                        "option_2_label": "le seau",
                        "option_3_label": "le doudou",
                    }
                },
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf],
                    T3[(a, b, c)],
                    "resolution",
                    T3_SONS[c],
                    {"emphasis": T3_EMPH[c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    ENDINGS[(a, b, c)],
                    "ending",
                    END_SONS[b],
                    {"emphasis": T3_EMPH[c], "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = (
        "Amir veut coller son doudou à la vitre du train pour lui montrer les champs. "
        "Un à-coup renverse la caisse. Le tas cache le gris. Lever le tout échoue. "
        "Selon le moment, il cherche trop vite, sous la couverture, ou dans la vitre. "
        "Cuisine, jardin de fenêtre ou nid du siège changent l'obstacle. "
        "Ballon, seau ou trou dans le tas font reparaître le doudou. "
        "Vingt-sept fins : la truffe a les champs, la caisse a le tas."
    )
    story["title"] = TITLE
    story["characters"] = "Amir, papa, maman"
    story["setting"] = "wagon, fenêtre sur les champs, caisse de jouets"
    story["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]

    check(SID, story["age_band"], story["chunks"])

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

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Public :** N2 (3–6 ans), audio familial\n"
        "- **Leçon :** AUT.RAN.001 — ranger, vécue (le doudou ne reparaît que lorsque le tas "
        "descend dans la caisse)\n"
        "- **Personnages :** Amir, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "## Vécu\n\n"
        "Wagon, vitre froide, champs de blé, caisse, ballon, seau, doudou gris. "
        "Désir : coller la truffe à la vitre pour voir les vaches. "
        "Première idée : tout lever d'un coup. Ça s'écroule, pas de gris. "
        "Chaque branche est une autre recherche :\n\n"
        "- T1 moment : le matin (lever le tas entier) / après la sieste (chercher sous la "
        "couverture) / le soir (chercher dans la vitre)\n"
        "- T2 lieu du wagon : cuisine de table / jardin de fenêtre / chambre-nid du siège\n"
        "- T3 geste : le ballon / le seau / le trou jusqu'au doudou\n\n"
        "Q = tas / couverture / visage. Merci vécu au moment où l'objet rentre et le gris "
        "revient. Fin : la promesse du début (champs, truffe, vitre), sans morale.\n\n"
        "## Vu et corrigé\n\n"
        "- Noé absent (D16 : Amir). Titre noyau conservé.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Pas « on va ranger » / « après le jeu » / leçon dite. Ranger se voit.\n"
        "- T1/T2/T3 changent l'obstacle et le climax, pas seulement la lumière.\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration), `style_energy`, "
        "pauses, pitch, volume. `slow` = choix, indice, fin.\n"
        f"- 27 fins, 27 dernières images. Chemins {min(counts)}–{max(counts)} mots "
        f"(moy. {sum(counts)//len(counts)}). `check()` N2≤15. Pas apply.\n"
        "- Relu : ouverture + 3 L1 + 9 L2 + 27 L3/fins.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
