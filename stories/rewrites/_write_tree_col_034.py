#!/usr/bin/env python3
"""TREE-COL-034 — F-NAR-019. Mila, l'arrosoir et le ver rose. COL.ECO.002, N1. Texte + TTS. Pas apply."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-034"
LIM = 10
CHILD = "enfant-f"

PROFILES = {
    "opening": {
        "rate": "medium",
        "wpm": 142,
        "speed": 0.98,
        "piper": 1.12,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 500,
        "sentence": 260,
        "energy": "warm",
        "contour": "storytelling",
        "noise": 0.36,
        "emphasis": "ver rose",
        "note": "arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la terre a soif et le ver est là; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow",
        "wpm": 116,
        "speed": 0.84,
        "piper": 1.30,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 900,
        "sentence": 330,
        "energy": "focused",
        "contour": "rising",
        "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow",
        "wpm": 120,
        "speed": 0.86,
        "piper": 1.27,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "soft",
        "db": -2,
        "pause": 700,
        "sentence": 320,
        "energy": "focused",
        "contour": "rising",
        "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_vient_d_arriver; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium",
        "wpm": 132,
        "speed": 0.92,
        "piper": 1.20,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 450,
        "sentence": 280,
        "energy": "bright",
        "contour": "falling",
        "noise": 0.34,
        "emphasis": "ver rose",
        "note": "arc=confirmation; intention=relancer; emotion=soulagement_discret; intensite=1; destinataire=enfant; sous_texte=la_parole_a_une_place; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium",
        "wpm": 146,
        "speed": 1.0,
        "piper": 1.10,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 420,
        "sentence": 250,
        "energy": "lively",
        "contour": "dynamic",
        "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_arroser_tout_de_suite; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium",
        "wpm": 134,
        "speed": 0.93,
        "piper": 1.18,
        "pitch": "low",
        "pitchSsml": "-2st",
        "pitchTag": "low-pitch",
        "volume": "medium",
        "db": 0,
        "pause": 520,
        "sentence": 300,
        "energy": "tense",
        "contour": "dynamic",
        "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=l_eau_peut_emporter_le_ver; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium",
        "wpm": 140,
        "speed": 0.97,
        "piper": 1.14,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 560,
        "sentence": 270,
        "energy": "bright",
        "contour": "falling",
        "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=écouter_change_l_arrosage; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow",
        "wpm": 118,
        "speed": 0.85,
        "piper": 1.28,
        "pitch": "low",
        "pitchSsml": "-2st",
        "pitchTag": "low-pitch",
        "volume": "soft",
        "db": -3,
        "pause": 900,
        "sentence": 340,
        "energy": "calm",
        "contour": "falling",
        "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_arrosoir_a_trouvé_sa_place; tempo=posé; sourire=léger; respiration=ample",
    },
}


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        out.append(f"{role}|{ph}")
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp and emp in text:
        e = esc(emp)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp and emp in text:
        body = body.replace(emp, f"<emphasis>{emp}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    if m["pause"] >= 800:
        pause = "[long-pause]"
    elif m["pause"] >= 400:
        pause = "[pause]"
    else:
        pause = ""
    return f"{body} {pause}".strip() if pause else body


def voice(src: dict, lines: list[str], sons: str, profile: str, extra: dict | None, emp: str | None) -> dict:
    m = dict(PROFILES[profile])
    if emp is not None:
        m["emphasis"] = emp
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["length_scale_piper"] = m["piper"]
    nc["rate_label"] = m["rate"]
    nc["rate_wpm"] = m["wpm"]
    nc["speed_xai"] = m["speed"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = 0
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
    if extra:
        nc.update(extra)
    return nc


STARTS = {
    1: {
        "lab": "l'arrosoir",
        "prop": "l'arrosoir",
        "sons": "eau,arrosoir",
        "passage": vet(
            [
                "narrateur|Mila soulève l'arrosoir jaune, trop vite.",
                "narrateur|L'eau claque contre le zinc chaud.",
                "enfant-f|Regardez le ver !",
                "narrateur|Papa répond à maman, près de la menthe.",
                "narrateur|Sa voix couvre le clac de l'eau.",
                "narrateur|Mila agite le bec, plus fort.",
                "narrateur|Une langue d'eau part vers la fente.",
                "narrateur|Le ver se recroqueville, tout petit.",
                "enfant-f|Non !",
                "narrateur|Elle rattrape le bec, d'un coup.",
                "narrateur|Elle pose deux doigts sur le poignet de papa.",
                "enfant-f|Quand tu as fini, viens.",
                "papa|Une seconde.",
                "papa|Voilà, je t'écoute.",
                "narrateur|La fente a repris un peu d'ombre.",
                "maman|Allons voir, alors.",
            ]
        ),
        "question": vet(
            [
                "narrateur|L'eau a failli toucher le ver.",
                "papa|Que fait le ver rose, alors ?",
            ]
        ),
        "qextra": {
            "expected_answer": "cache",
            "accepted_examples": "il se cache | se cache | se recroqueville | il rentre | il fuit",
            "retry_prompt": "L'eau part. Le rose fait quoi ?",
            "engine_ok_text": "Oui, il se cache.",
            "engine_near_text": "Tu es près. Regarde la fente.",
        },
        "qemp": "ver rose",
        "confirm": vet(
            [
                "enfant-f|Il s'est caché !",
                "narrateur|Oui, dans la fente sèche.",
                "narrateur|Mila l'a dit quand papa écoutait.",
                "narrateur|Maman pose la menthe sur le banc.",
                "papa|On y va.",
                "narrateur|L'arrosoir pèse, un peu moins penché.",
            ]
        ),
        "arrive": {
            1: ["Mila porte l'arrosoir, trop plein, vers les tomates."],
            2: ["L'arrosoir cogne le pot de menthe."],
            3: ["Mila traîne l'arrosoir jusqu'au compost."],
        },
    },
    2: {
        "lab": "la pelle",
        "prop": "la pelle",
        "sons": "terre,pelle",
        "passage": vet(
            [
                "narrateur|Mila saisit la petite pelle rouge.",
                "narrateur|Elle tape la croûte, pour montrer la fente.",
                "enfant-f|Il est là !",
                "narrateur|Papa parle des tomates à maman.",
                "narrateur|Le toc de la pelle se perd.",
                "narrateur|Mila tape plus fort, trop près.",
                "narrateur|La terre saute.",
                "narrateur|Le ver glisse plus bas.",
                "enfant-f|Reviens !",
                "narrateur|Elle pose la pelle à plat.",
                "narrateur|Elle attend que maman finisse sa phrase.",
                "enfant-f|Maintenant, je peux dire.",
                "maman|Oui.",
                "maman|Nous t'écoutons.",
                "enfant-f|Le ver, sous la croûte.",
            ]
        ),
        "question": vet(
            [
                "narrateur|La pelle a trop parlé.",
                "maman|Que fait le ver, sous la croûte ?",
            ]
        ),
        "qextra": {
            "expected_answer": "cache",
            "accepted_examples": "il se cache | se cache | il glisse | il rentre | il fuit",
            "retry_prompt": "La terre saute. Le rose va où ?",
            "engine_ok_text": "Oui, il se cache.",
            "engine_near_text": "Tu es près. Écoute la terre.",
        },
        "qemp": "ver",
        "confirm": vet(
            [
                "enfant-f|Il s'est caché !",
                "narrateur|Oui, plus bas, sous la croûte.",
                "narrateur|Papa a entendu toute la phrase.",
                "narrateur|Maman essuie la pelle sur l'herbe.",
                "papa|Montre-nous la fente.",
                "narrateur|La pelle repose, sage, contre le banc.",
            ]
        ),
        "arrive": {
            1: ["La pelle racle la terre, près des tomates."],
            2: ["La pelle tape le bord du pot."],
            3: ["La pelle soulève une croûte du compost."],
        },
    },
    3: {
        "lab": "le seau",
        "prop": "le seau",
        "sons": "seau,zinc",
        "passage": vet(
            [
                "narrateur|Mila prend le seau vide, près du robinet.",
                "narrateur|Elle le frappe du plat de la main.",
                "narrateur|Le zinc sonne, trop fort.",
                "enfant-f|Venez !",
                "narrateur|Papa se tourne vers le bruit, pas vers la fente.",
                "papa|Doucement, les oreilles.",
                "narrateur|Maman parle du robinet, qui goutte.",
                "narrateur|Personne n'a vu le rose.",
                "enfant-f|Pas le seau.",
                "enfant-f|Le ver !",
                "narrateur|Mila pose le seau.",
                "narrateur|Elle attend.",
                "narrateur|Le robinet finit sa goutte.",
                "enfant-f|Le vrai secret est dans la terre.",
                "maman|Alors baissons les yeux, dehors.",
            ]
        ),
        "question": vet(
            [
                "narrateur|Papa a entendu le seau.",
                "papa|Où est le vrai secret, Mila ?",
            ]
        ),
        "qextra": {
            "expected_answer": "terre",
            "accepted_examples": "terre | dans la terre | la fente | le ver | dehors",
            "retry_prompt": "Le seau sonnait. Le secret est où ?",
            "engine_ok_text": "Oui, dans la terre.",
            "engine_near_text": "Tu es près. Regarde la fente.",
        },
        "qemp": "terre",
        "confirm": vet(
            [
                "enfant-f|Dans la terre !",
                "narrateur|Oui, dans la fente sèche.",
                "narrateur|Papa laisse le seau près du robinet.",
                "narrateur|Maman essuie ses mains sur le tablier.",
                "maman|Montre-nous le rose.",
                "narrateur|Le seau reste, muet, à l'ombre.",
            ]
        ),
        "arrive": {
            1: ["Le seau vide penche, près des tomates."],
            2: ["Mila pose le seau sous la menthe."],
            3: ["Le seau sonne, contre le bois du compost."],
        },
    },
}

LOCS = {
    1: {
        "lab": "les tomates",
        "sound": "feuilles,terre",
        "q": ["L'eau va faire une rivière.", "Comment aider le ver ?"],
        "body": vet(
            [
                "narrateur|Le ver rose est dans une fente, sous les tomates.",
                "maman|Je verse au pied, pas sur les feuilles.",
                "papa|Moi, je verse un peu plus loin.",
                "narrateur|Les deux voix arrivent ensemble.",
                "narrateur|Mila tourne la tête, perdue.",
                "enfant-f|Papa d'abord.",
                "enfant-f|Après, maman.",
                "narrateur|Papa montre la terre fendue, au pied.",
                "narrateur|Maman montre une feuille qui touche le sol.",
                "narrateur|Les deux signes se rejoignent.",
                "narrateur|Une goutte trop grosse ferait une rivière.",
                "enfant-f|Il va partir avec l'eau !",
            ]
        ),
    },
    2: {
        "lab": "la menthe",
        "sound": "pot,menthe",
        "q": ["La soucoupe déborde.", "Comment aider le ver ?"],
        "body": vet(
            [
                "narrateur|Le ver rose tient au bord du pot de menthe.",
                "papa|Je soulève le pot.",
                "maman|Je vide la soucoupe.",
                "narrateur|Ils parlent et bougent ensemble.",
                "narrateur|Le pot penche.",
                "narrateur|L'eau de la soucoupe tremble.",
                "enfant-f|Un à la fois, s'il vous plaît.",
                "narrateur|Papa s'arrête.",
                "narrateur|Maman s'arrête aussi.",
                "narrateur|La soucoupe redevient un petit lac.",
                "enfant-f|Le ver, là, sur le bord.",
            ]
        ),
    },
    3: {
        "lab": "le compost",
        "sound": "compost,bois",
        "q": ["Le tas est trop chaud.", "Comment aider le ver ?"],
        "body": vet(
            [
                "narrateur|Le ver rose glisse au bord du compost.",
                "papa|Je verse tout, pour refroidir.",
                "narrateur|Sa main attrape le bec.",
                "enfant-f|Stop, papa !",
                "narrateur|Le rose est juste sous le filet.",
                "narrateur|Mila n'attend pas.",
                "narrateur|C'est trop près de l'eau.",
                "papa|J'écoute.",
                "papa|Je lâche.",
                "maman|Tu as bien fait de crier.",
                "narrateur|Une vapeur tiède sort du tas.",
            ]
        ),
    },
}

SOLS = {
    1: {
        "lab": "la feuille",
        "sons": "feuille",
        "scenes": {
            1: vet(
                [
                    "narrateur|Mila prend une large feuille de salade.",
                    "narrateur|Elle attend que papa finisse.",
                    "enfant-f|Un toit, pour le ver.",
                    "papa|Je te la tiens ?",
                    "narrateur|Mila tend la feuille, sans un mot.",
                    "papa|Merci, Mila.",
                    "narrateur|Papa pose le toit au-dessus de la fente.",
                    "narrateur|Maman verse un filet, loin du rose.",
                    "narrateur|Les tomates boivent.",
                    "narrateur|Le ver reste à l'ombre.",
                    "maman|Je le vois, sous le vert.",
                    "enfant-f|Il a son chemin, à lui.",
                ]
            ),
            2: vet(
                [
                    "narrateur|Mila prend une feuille de menthe, plus grande.",
                    "narrateur|Elle la tend quand maman a fini.",
                    "enfant-f|Un pont, au-dessus de l'eau.",
                    "maman|Je pince, tu dis où.",
                    "enfant-f|Un peu plus à gauche.",
                    "narrateur|La feuille rejoint le bord du pot.",
                    "narrateur|Le ver touche le vert, d'une pointe.",
                    "papa|Bravo, Mila.",
                    "narrateur|Il glisse vers la terre fraîche.",
                    "maman|La soucoupe peut attendre.",
                ]
            ),
            3: vet(
                [
                    "narrateur|Mila prend une feuille de platane.",
                    "narrateur|Elle attend que le bec soit libre.",
                    "enfant-f|On fait un toit, sur le tas.",
                    "papa|Oui.",
                    "papa|À toi.",
                    "narrateur|Mila pose le vert au-dessus du rose.",
                    "narrateur|L'eau tombe à côté, pas dessus.",
                    "maman|Merci.",
                    "maman|Il reste au frais.",
                    "narrateur|Le compost fume moins.",
                    "enfant-f|Il est sage, maintenant.",
                ]
            ),
        },
    },
    2: {
        "lab": "le caillou",
        "sons": "pierre",
        "scenes": {
            1: vet(
                [
                    "narrateur|Mila choisit un caillou plat, clair.",
                    "narrateur|Papa ouvre la bouche.",
                    "narrateur|Elle attend.",
                    "papa|Tu poses le barrage, ou moi ?",
                    "enfant-f|Toi.",
                    "enfant-f|Je dis quand.",
                    "narrateur|Papa glisse la pierre devant la fente.",
                    "narrateur|Mila lève la main.",
                    "enfant-f|Là.",
                    "narrateur|Maman verse derrière le caillou.",
                    "narrateur|L'eau s'arrête.",
                    "narrateur|Les tomates boivent.",
                    "papa|Merci.",
                    "papa|J'ai entendu ton là.",
                ]
            ),
            2: vet(
                [
                    "narrateur|Mila prend trois petits cailloux.",
                    "narrateur|Elle les glisse vers papa.",
                    "enfant-f|Quand tu es prêt.",
                    "papa|Je le suis.",
                    "narrateur|Les pierres marquent le bord de la soucoupe.",
                    "narrateur|L'eau ne peut plus lécher le ver.",
                    "maman|Je verse dans le pot, pas autour.",
                    "narrateur|La menthe se redresse, un peu.",
                    "enfant-f|Il contourne les cailloux.",
                    "papa|Merci pour le tour de pierre.",
                ]
            ),
            3: vet(
                [
                    "narrateur|Mila prend un caillou rond, tiède.",
                    "narrateur|Elle touche le coude de papa.",
                    "enfant-f|Pose-le entre l'eau et lui.",
                    "papa|J'attends ton signal.",
                    "enfant-f|Maintenant.",
                    "narrateur|La pierre fait un petit mur.",
                    "narrateur|Maman verse derrière, tout lent.",
                    "narrateur|Le compost boit, sans noyer le bord.",
                    "maman|Merci.",
                    "maman|Je l'ai vu partir.",
                    "enfant-f|Il sent la terre chaude.",
                ]
            ),
        },
    },
    3: {
        "lab": "la pomme",
        "sons": "arrosoir,gouttes",
        "scenes": {
            1: vet(
                [
                    "narrateur|Mila visse la pomme sur le bec.",
                    "enfant-f|Des gouttes, pas une rivière.",
                    "narrateur|La famille s'accroupit près des tomates.",
                    "narrateur|Papa veut parler.",
                    "narrateur|Mila lève un doigt, puis attend.",
                    "papa|À toi le premier tour.",
                    "narrateur|Elle penche, très peu.",
                    "narrateur|La pluie fine tombe loin de la fente.",
                    "maman|Le ver avance, à l'abri.",
                    "narrateur|Les tomates brillent, sans rivière.",
                    "enfant-f|On a parlé avec les gouttes.",
                ]
            ),
            2: vet(
                [
                    "narrateur|Mila visse la pomme, près de la menthe.",
                    "enfant-f|On arrose le pot, pas le bord.",
                    "narrateur|Papa ferme la bouche.",
                    "narrateur|Maman aussi.",
                    "narrateur|La soucoupe redevient lisse.",
                    "enfant-f|Maintenant, un peu.",
                    "narrateur|Les gouttes chantent sur les feuilles.",
                    "narrateur|Le ver quitte le bord, vers la terre.",
                    "maman|Merci d'avoir laissé l'eau se taire.",
                    "enfant-f|La menthe a soif, pas lui.",
                ]
            ),
            3: vet(
                [
                    "narrateur|Mila visse la pomme, loin du tas.",
                    "enfant-f|Le compost boit à côté.",
                    "narrateur|Papa garde les mains loin du bec.",
                    "narrateur|Maman s'accroupit de l'autre côté.",
                    "narrateur|On entend un merle, puis plus rien.",
                    "maman|Il avance vers l'ombre, Mila.",
                    "narrateur|Mila ne répond pas tout de suite.",
                    "narrateur|Les gouttes tombent sur le bois, pas sur lui.",
                    "enfant-f|Maintenant, tu peux parler.",
                    "papa|Merci.",
                    "papa|J'ai entendu ton maintenant.",
                ]
            ),
        },
    },
}

# Ligne-objet unique par chemin (T1 × T2 × T3).
CB = {
    (1, 1, 1): "L'arrosoir sent la terre, et un peu de feuille.",
    (1, 1, 2): "Le bec a une tache de poussière, près du caillou.",
    (1, 1, 3): "La pomme goutte, loin de la fente.",
    (1, 2, 1): "L'arrosoir a une odeur de menthe, collée au zinc.",
    (1, 2, 2): "Trois cailloux brillent au pied de l'arrosoir.",
    (1, 2, 3): "La pomme a chanté, tout près du pot.",
    (1, 3, 1): "L'arrosoir repose, plus léger, contre le compost.",
    (1, 3, 2): "Le caillou tiède sèche près du bec.",
    (1, 3, 3): "La pomme a laissé un rond d'eau.",
    (2, 1, 1): "La pelle rouge attend au pied des tomates.",
    (2, 1, 2): "La pelle penche, comme le caillou plat.",
    (2, 1, 3): "La pelle est sage, dans l'herbe.",
    (2, 2, 1): "Mila pose la pelle loin de la soucoupe.",
    (2, 2, 2): "Un peu de terre colle à la pelle.",
    (2, 2, 3): "La pelle reflète les gouttes, un instant.",
    (2, 3, 1): "La pelle sert de poids, près de la feuille.",
    (2, 3, 2): "La pelle tremble quand le caillou se pose.",
    (2, 3, 3): "La pelle reste entre Mila et le tas.",
    (3, 1, 1): "Le seau vide a un vrai frère : l'arrosoir.",
    (3, 1, 2): "Le seau, au robinet, semble pousser aussi.",
    (3, 1, 3): "Le seau ne sonne plus, près des tomates.",
    (3, 2, 1): "Le seau penche vers la menthe, au loin.",
    (3, 2, 2): "Le seau sent le zinc, comme les cailloux.",
    (3, 2, 3): "Le seau attend, pendant que les gouttes parlent.",
    (3, 3, 1): "Le seau a laissé un rond minuscule, au bois.",
    (3, 3, 2): "Le seau pointe vers le compost, oublié.",
    (3, 3, 3): "Le seau respire, comme le jardin.",
}

HOUSE = {
    (1, 1, 1): "L'arrosoir jaune se tient droit, près du banc.",
    (1, 1, 2): "Une feuille sèche colle au bec de l'arrosoir.",
    (1, 1, 3): "Papa essuie la pomme sur le torchon rayé.",
    (1, 2, 1): "La menthe sent plus fort, dans la cuisine.",
    (1, 2, 2): "Trois cailloux sèchent sur le rebord de la fenêtre.",
    (1, 2, 3): "Une goutte de menthe brille sur le zinc.",
    (1, 3, 1): "Le compost a laissé une odeur tiède, au hall.",
    (1, 3, 2): "Le caillou rond sèche contre le mur.",
    (1, 3, 3): "Un merle chante derrière le tas, au loin.",
    (2, 1, 1): "Mila pose la pelle près des chaussures.",
    (2, 1, 2): "Un peu de terre tombe de la pelle.",
    (2, 1, 3): "La pelle rouge brille, essuyée, près de l'évier.",
    (2, 2, 1): "La pelle a une odeur de menthe, sur le bois.",
    (2, 2, 2): "Papa range la pelle derrière la porte.",
    (2, 2, 3): "La pelle reflète la fenêtre, un instant.",
    (2, 3, 1): "Mila souffle sur ses mains, pelle au pied.",
    (2, 3, 2): "La terre du compost sèche sur le fer.",
    (2, 3, 3): "Maman pose la pelle loin du rebord.",
    (3, 1, 1): "Le seau vide attend près du robinet.",
    (3, 1, 2): "Papa range le seau sous l'évier.",
    (3, 1, 3): "Le seau a un peu d'eau, au fond.",
    (3, 2, 1): "Une feuille de menthe flotte dans le seau.",
    (3, 2, 2): "Le seau sonne tout bas, contre le carreau.",
    (3, 2, 3): "Maman souffle sur ses mains, près du seau.",
    (3, 3, 1): "Le seau pointe vers le jardin, oublié.",
    (3, 3, 2): "Papa pose le seau à côté des bottes.",
    (3, 3, 3): "Le seau et l'arrosoir se ressemblent enfin.",
}

RECAP = {
    (1, 1, 1): "J'ai tendu la feuille. Papa avait fini.",
    (1, 1, 2): "J'ai dit là, avec le caillou.",
    (1, 1, 3): "On a laissé les gouttes parler.",
    (1, 2, 1): "J'ai montré la gauche, pour le pont.",
    (1, 2, 2): "Les cailloux ont gardé le bord.",
    (1, 2, 3): "L'eau s'est tue. Après, les gouttes.",
    (1, 3, 1): "J'ai posé le toit sur le tas.",
    (1, 3, 2): "J'ai dit maintenant, pour la pierre.",
    (1, 3, 3): "J'ai dit stop, puis j'ai attendu.",
    (2, 1, 1): "La pelle a attendu. La feuille aussi.",
    (2, 1, 2): "J'ai gardé la pelle. Papa poussait.",
    (2, 1, 3): "On a regardé les tomates, sans un bruit.",
    (2, 2, 1): "J'ai posé la pelle. Maman a pincé.",
    (2, 2, 2): "Les trois cailloux ont fait un mur.",
    (2, 2, 3): "On n'a pas versé sur le bord.",
    (2, 3, 1): "La pelle pesait. La feuille tenait.",
    (2, 3, 2): "J'ai touché le coude, puis la pierre.",
    (2, 3, 3): "Le merle a fini. J'ai dit parler.",
    (3, 1, 1): "Le seau était faux. La feuille, vraie.",
    (3, 1, 2): "J'ai dit là. Le seau restait dedans.",
    (3, 1, 3): "Le vrai secret était dans la terre.",
    (3, 2, 1): "On a fait un pont. Le seau regardait.",
    (3, 2, 2): "Les cailloux ont travaillé. Le seau, non.",
    (3, 2, 3): "Les gouttes ont parlé. Le seau, non.",
    (3, 3, 1): "J'ai posé le toit. Le seau restait.",
    (3, 3, 2): "La pierre a tenu. Le seau pointait.",
    (3, 3, 3): "On a laissé le merle finir, d'abord.",
}

THANKS = {
    (1, 1, 1): "Merci. J'ai vu le rose, grâce à toi.",
    (1, 1, 2): "Ton là était juste.",
    (1, 1, 3): "Les gouttes nous ont aidés.",
    (1, 2, 1): "Tu as dit la gauche au bon moment.",
    (1, 2, 2): "Les cailloux ont bien travaillé.",
    (1, 2, 3): "L'eau était plus calme, après.",
    (1, 3, 1): "Le tas est plus frais, maintenant.",
    (1, 3, 2): "Ton maintenant est arrivé à temps.",
    (1, 3, 3): "Tu as crié, puis tu as laissé le bec.",
    (2, 1, 1): "La pelle a eu son tour, elle aussi.",
    (2, 1, 2): "Merci d'avoir gardé la pelle.",
    (2, 1, 3): "On a regardé ensemble, longtemps.",
    (2, 2, 1): "La feuille a parlé après la pelle.",
    (2, 2, 2): "Le jardin a soif, pas le ver.",
    (2, 2, 3): "Merci d'avoir laissé l'eau se taire.",
    (2, 3, 1): "La pelle a tenu le tas, un peu.",
    (2, 3, 2): "J'ai senti ton doigt sur mon coude.",
    (2, 3, 3): "Merci pour le maintenant.",
    (3, 1, 1): "Le vrai secret a gagné, dehors.",
    (3, 1, 2): "Le seau peut dormir, maintenant.",
    (3, 1, 3): "Le seau et les gouttes se sont tus.",
    (3, 2, 1): "La feuille a fini ce que le seau commençait.",
    (3, 2, 2): "Deux durs : le seau, et les cailloux.",
    (3, 2, 3): "Merci d'avoir montré le vrai.",
    (3, 3, 1): "Le tas et le seau se ressemblent, un peu.",
    (3, 3, 2): "Le compost a compris ton signal.",
    (3, 3, 3): "Le merle a eu son tour, lui aussi.",
}

CLOSE = {
    (1, 1, 1): "Une goutte tient au bec, puis tombe ailleurs.",
    (1, 1, 2): "Les chaussettes ont de l'herbe mouillée.",
    (1, 1, 3): "Le banc de bois reste chaud, sous l'arrosoir droit.",
    (1, 2, 1): "La menthe colle au mur, plus verte.",
    (1, 2, 2): "Une abeille passe, loin des cailloux.",
    (1, 2, 3): "Le zinc sent la menthe, et un peu d'eau.",
    (1, 3, 1): "La vapeur du tas s'en va, toute mince.",
    (1, 3, 2): "Le caillou garde un peu de chaleur, dans la main.",
    (1, 3, 3): "Derrière le compost, il reste le ciel.",
    (2, 1, 1): "Dans la fente, plus rien de rose, juste l'ombre.",
    (2, 1, 2): "La pelle sent la terre, contre le nez.",
    (2, 1, 3): "Mila pose la pelle sous le banc chaud.",
    (2, 2, 1): "Une goutte descend le long du pot de menthe.",
    (2, 2, 2): "La soucoupe est un miroir, comme le ciel.",
    (2, 2, 3): "Mila souffle sur une feuille de menthe.",
    (2, 3, 1): "La pelle cadre le tas, plus calme.",
    (2, 3, 2): "Le fer a laissé un trait sur le bois.",
    (2, 3, 3): "Derrière la pelle, il reste l'herbe.",
    (3, 1, 1): "Le seau rejoint l'arrosoir, près du banc.",
    (3, 1, 2): "Le robinet a fini sa goutte, tout seul.",
    (3, 1, 3): "Le seau garde un ovale d'eau, souvenir.",
    (3, 2, 1): "Une goutte traverse le seau, puis la menthe.",
    (3, 2, 2): "Le seau, les cailloux, l'arrosoir : trois ronds.",
    (3, 2, 3): "Mila laisse le seau, garde l'odeur de menthe.",
    (3, 3, 1): "Le seau cadre le tas, minuscule.",
    (3, 3, 2): "Le zinc du seau fuit vers le jardin.",
    (3, 3, 3): "L'arrosoir reste, vide et clair, contre le banc.",
}


def split_thanks(key: tuple[int, int, int]) -> list[str]:
    th = THANKS[key]
    if th.count(".") + th.count("?") + th.count("!") > 1:
        parts = [
            p.strip()
            for p in th.replace("?", "?|").replace("!", "!|").replace(".", ".|").split("|")
            if p.strip()
        ]
        return [f"papa|{p}" for p in parts]
    return [f"papa|{th}"]


def ending_lines(a: int, b: int, c: int) -> list[str]:
    key = (a, b, c)
    rec = RECAP[key]
    if rec.count(".") + rec.count("?") + rec.count("!") > 1:
        parts = [
            p.strip()
            for p in rec.replace("?", "?|").replace("!", "!|").replace(".", ".|").split("|")
            if p.strip()
        ]
        rec_lines = [f"{CHILD}|{p}" for p in parts]
    else:
        rec_lines = [f"{CHILD}|{rec}"]
    return vet(
        [
            f"narrateur|{HOUSE[key]}",
            "maman|À toi, Mila.",
            "maman|Nous t'écoutons.",
            *rec_lines,
            *split_thanks(key),
            f"narrateur|{CB[key]}",
            f"narrateur|{CLOSE[key]}",
        ]
    )


def t3_choice(b: int) -> list[str]:
    qs = [f"narrateur|{p}" for p in LOCS[b]["q"]]
    return vet(qs + ["papa|La feuille, le caillou, ou la pomme ?"])


def loc_passage(a: int, b: int) -> list[str]:
    arrive = [f"narrateur|{p}" for p in STARTS[a]["arrive"][b]]
    return vet(arrive) + LOCS[b]["body"]


def leaf_body(a: int, b: int, c: int) -> list[str]:
    return SOLS[c]["scenes"][b] + vet([f"narrateur|{CB[a, b, c]}"])


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    profs: dict[str, str] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}
    emps: dict[str, str | None] = {}

    def put(
        cid: str,
        lines: list[str],
        profile: str,
        son: str = "",
        extra: dict | None = None,
        emp: str | None = None,
    ) -> None:
        scripts[cid] = lines
        profs[cid] = profile
        sons[cid] = son
        if extra:
            extras[cid] = extra
        emps[cid] = emp

    put(
        "CHK_T0000_P0000",
        vet(
            [
                "narrateur|Au bout du chemin, la petite maison a un jardin.",
                "narrateur|Mila y vit, avec papa et maman.",
                "narrateur|Le soleil chauffe la terre, toute fendue.",
                "narrateur|Les tomates vertes pendent, un peu molles.",
                "narrateur|La menthe colle au mur, et sent fort.",
                "narrateur|Un banc de bois reste chaud, près du mur.",
                "narrateur|L'arrosoir jaune penche contre le banc.",
                "narrateur|Une goutte tremble au bec, puis tient.",
                "narrateur|Les chaussettes de Mila ont de l'herbe.",
                "narrateur|Papa parle des plantes à maman.",
                "narrateur|Maman pince une feuille de menthe.",
                "narrateur|En ce moment, Mila tire l'arrosoir vers les tomates.",
                "enfant-f|Je les arrose, toutes, maintenant !",
                "narrateur|Une fente s'ouvre dans la terre sèche.",
                "narrateur|Un ver rose glisse entre deux croûtes.",
                "enfant-f|Papa, maman, un ver rose !",
                "narrateur|Papa continue sa phrase, vers maman.",
                "narrateur|Les mots de Mila tombent dans les leurs.",
                "narrateur|Elle penche l'arrosoir, trop vite.",
                "narrateur|L'eau part en une petite langue.",
                "narrateur|Le ver se recroqueville, tout petit.",
                "enfant-f|Il va partir !",
                "papa|Tu disais quelque chose, Mila ?",
                "enfant-f|Le ver va boire trop d'eau.",
                "maman|Montre-nous, quand nous avons fini.",
            ]
        ),
        "opening",
        "terre,arrosoir",
        emp="ver rose",
    )

    put(
        "CHK_T0001_P0000",
        vet(
            [
                "narrateur|Mila peut se faire entendre autrement.",
                "papa|L'arrosoir, la pelle, ou le seau ?",
                "maman|Que prends-tu, pour commencer ?",
            ]
        ),
        "choice",
        "",
        {"option_1_label": "l'arrosoir", "option_2_label": "la pelle", "option_3_label": "le seau"},
    )

    for a, st in STARTS.items():
        p = f"CHK_T0001_P000{a}"
        put(p, st["passage"], "action", st["sons"])
        put(
            f"{p}_Q0001",
            st["question"],
            "clue",
            "",
            st["qextra"],
            st["qemp"],
        )
        put(f"{p}_C0001", st["confirm"], "confirm", "", emp="ver rose")
        put(
            f"{p}_T0002_P0000",
            vet(
                [
                    "narrateur|Le ver a bougé.",
                    "papa|Vers les tomates, la menthe, ou le compost ?",
                    "maman|Où va-t-on l'aider ?",
                ]
            ),
            "choice",
            "",
            {
                "option_1_label": "les tomates",
                "option_2_label": "la menthe",
                "option_3_label": "le compost",
            },
        )
        for b, loc in LOCS.items():
            sp = f"{p}_T0002_P000{b}"
            put(sp, loc_passage(a, b), "obstacle", loc["sound"])
            put(
                f"{sp}_T0003_P0000",
                t3_choice(b),
                "choice",
                "",
                {
                    "option_1_label": "la feuille",
                    "option_2_label": "le caillou",
                    "option_3_label": "la pomme",
                },
            )
            for c, sol in SOLS.items():
                leaf = f"{sp}_T0003_P000{c}"
                put(leaf, leaf_body(a, b, c), "resolution", sol["sons"])
                fin_sons = {1: "jardin,tomate", 2: "menthe,pot", 3: "compost,merle"}[b]
                put(f"{leaf}_F0001", ending_lines(a, b, c), "ending", fin_sons)

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        by[cid] = voice(c, scripts[cid], sons.get(cid, ""), profs[cid], extras.get(cid), emps.get(cid))

    out = dict(src)
    out["fil_rouge"] = (
        "Au jardin, la terre est fendue et l'arrosoir jaune penche contre le banc. "
        "Mila veut arroser les tomates tout de suite. Un ver rose glisse dans une fente. "
        "Elle crie : papa et maman parlent, l'eau part trop vite, le ver se cache. "
        "L'arrosoir, la pelle ou le seau changent la façon d'être entendue. "
        "Les tomates, la menthe ou le compost changent le danger. "
        "Une feuille, un caillou ou la pomme de l'arrosoir changent l'arrosage. "
        "Le soir, l'arrosoir se tient droit : chacun a écouté jusqu'au bout."
    )
    out["title"] = "L'arrosoir et le ver rose"
    out["characters"] = "Mila, papa, maman"
    out["setting"] = "jardin d'une petite maison, terre sèche, banc et menthe"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    fins = [c["text"] for c in out["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27:
        raise SystemExit(f"fins {len(fins)}")
    if len(set(fins)) != 27:
        raise SystemExit("fins non distinctes")

    t3_only = [
        c["text"]
        for c in out["chunks"]
        if c["kind"] == "passage"
        and "T0003_P000" in c["chunk_id"]
        and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    def wtxt(cid: str) -> int:
        return words(by[cid]["text"])

    lengths = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                n = wtxt("CHK_T0000_P0000") + wtxt("CHK_T0001_P0000")
                p = f"CHK_T0001_P000{a}"
                n += wtxt(p) + wtxt(f"{p}_Q0001") + wtxt(f"{p}_C0001") + wtxt(f"{p}_T0002_P0000")
                sp = f"{p}_T0002_P000{b}"
                n += wtxt(sp) + wtxt(f"{sp}_T0003_P0000")
                leaf = f"{sp}_T0003_P000{c}"
                n += wtxt(leaf) + wtxt(f"{leaf}_F0001")
                lengths.append(n)
    print(f"chemins {min(lengths)}–{max(lengths)} mots, moy {sum(lengths)//len(lengths)}")

    tics = (
        "tout doux",
        "tout calme",
        "on lève la main",
        "puis on parle",
        "voici le geste",
        "on va apprendre",
        "l'histoire est finie",
    )
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for t in tics:
        if t in blob:
            raise SystemExit(f"tic: {t}")
    for tic in (" encore ", " déjà "):
        if tic in f" {blob} ":
            # trop strict si un mot contient ces lettres ; on cible les adverbes isolés
            pass
    if " encore" in blob or "déjà" in blob:
        raise SystemExit("tic encore/déjà")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    vecu = (
        "Mila veut arroser les tomates avec l'arrosoir jaune, tout de suite. "
        "Un ver rose glisse dans la terre fendue. Crier échoue : papa et maman parlent, "
        "l'eau part trop vite, le ver se cache. Agiter l'arrosoir, taper de la pelle "
        "ou frapper le seau : première idée ratée. Le doigt sur le poignet, poser la pelle "
        "ou attendre la goutte du robinet changent l'action. Aux tomates les voix se mélangent ; "
        "à la menthe les mains aussi ; au compost Mila crie stop parce que le bec menace. "
        "Feuille, caillou ou pomme d'arrosoir : trois façons d'arroser sans noyer. "
        "L'arrosoir droit et le banc chaud referment."
    )
    notes = (
        "Reprise complète 86 nœuds. Labels T1 arrosoir/pelle/seau, T2 tomates/"
        "menthe/compost, T3 feuille/caillou/pomme : le choix change l'obstacle et "
        "la fin. 27 fins textuellement distinctes. Leçon COL.ECO.002 vécue, pas "
        "dite. N1≤10. TTS par fonction (opening/choice/clue/confirm/action/"
        "obstacle/resolution/ending). Un merci et un bravo vécus, une question "
        "adulte. Pas apply."
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — L'arrosoir et le ver rose\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        f"## Vécu\n{vecu}\n\n"
        f"## Vu et corrigé\n{notes}\n\n"
        "## Contrôles\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes\n"
        f"- {min(lengths)} à {max(lengths)} mots par chemin, moyenne {sum(lengths)//len(lengths)}\n"
        "- `text` / `script` synchronisés ; `text_ssml` et `text_xai_tags` sur 86 nœuds\n"
        "- N1 ≤ 10 mots/phrase ; papa et maman parlent ; `en ce moment`\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(out['chunks'])} chunks")


if __name__ == "__main__":
    main()
