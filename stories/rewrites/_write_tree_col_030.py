#!/usr/bin/env python3
"""TREE-COL-030 — F-NAR-019. Nina, le petit rond, COL.ECO.002, N1. Texte + TTS. Pas apply."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-030"
LIM = 10

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
        "emphasis": "petit rond",
        "note": "arc=installation; intention=émerveiller; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=un secret vient de commencer; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
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
        "emphasis": "ballon",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_piste_continue; tempo=naturel; sourire=léger; respiration=fluide",
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
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_faut_faire_vite; tempo=vif; sourire=léger; respiration=courte",
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
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=les_voix_se_mélangent; tempo=resserré; sourire=aucun; respiration=retenue",
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
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_solution_vient_de_l_écoute; tempo=naturel; sourire=franc; respiration=relâchée",
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
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_parole_a_trouvé_sa_place; tempo=posé; sourire=léger; respiration=ample",
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
        "lab": "le doigt",
        "prop": "le doigt",
        "sons": "vitre,doigt",
        "passage": vet(
            [
                "narrateur|Nina tape la vitre du doigt.",
                "narrateur|Le verre fait toc, toc.",
                "narrateur|Le ballon jaune sursaute dehors.",
                "enfant-f|Regardez !",
                "narrateur|Papa parle à maman, tout bas.",
                "narrateur|Sa voix couvre le petit toc.",
                "narrateur|Nina tape plus fort.",
                "narrateur|Le ballon recule dans les branches.",
                "enfant-f|Non !",
                "narrateur|Elle arrête sa main.",
                "narrateur|Elle pose le doigt sur le poignet de papa.",
                "enfant-f|Quand tu as fini, viens.",
                "papa|Une seconde.",
                "papa|Voilà, je t'écoute.",
                "narrateur|Le rond s'est presque refermé.",
                "maman|Dépêchons-nous, alors.",
            ]
        ),
        "question": vet(
            [
                "narrateur|Nina tape trop fort.",
                "papa|Que fait le ballon, alors ?",
            ]
        ),
        "qextra": {
            "expected_answer": "saute",
            "accepted_examples": "saute | il saute | recule | il recule | tremble",
            "retry_prompt": "Nina tape. Le jaune bouge. Il fait quoi ?",
            "engine_ok_text": "Oui, il saute.",
            "engine_near_text": "Tu es près. Écoute le toc.",
        },
        "qemp": "ballon",
        "confirm": vet(
            [
                "enfant-f|Il a sauté !",
                "narrateur|Oui, le jaune a reculé.",
                "narrateur|Nina l'a dit quand papa écoutait.",
                "narrateur|Maman prend les bottes près de la porte.",
                "papa|On y va.",
                "narrateur|Le petit rond reste mince.",
            ]
        ),
        "arrive": {
            1: ["Nina court, le doigt vers le romarin."],
            2: ["Nina montre la flaque du doigt."],
            3: ["Nina court vers le portail, le doigt levé."],
        },
    },
    2: {
        "lab": "la tasse",
        "prop": "la tasse",
        "sons": "casserole,tasse",
        "passage": vet(
            [
                "narrateur|Nina saisit sa tasse vide.",
                "narrateur|Elle court vers la casserole.",
                "narrateur|Le cacao danse au bord.",
                "enfant-f|Le ballon !",
                "narrateur|Papa verse, les yeux sur le lait.",
                "narrateur|Maman parle des lettres.",
                "narrateur|La tasse cogne le bois de la table.",
                "narrateur|Une goutte brune saute.",
                "papa|Attention, c'est chaud.",
                "narrateur|Nina recule d'un pas.",
                "narrateur|Elle serre la tasse contre elle.",
                "narrateur|La casserole chante, puis se tait.",
                "enfant-f|Maintenant, je peux dire.",
                "maman|Oui.",
                "maman|Nous t'écoutons.",
                "enfant-f|Le jaune, dans le rond.",
            ]
        ),
        "question": vet(
            [
                "narrateur|La casserole chante très fort.",
                "maman|Nina fait quoi, avec sa tasse ?",
            ]
        ),
        "qextra": {
            "expected_answer": "attendre",
            "accepted_examples": "attendre | elle attend | recule | elle recule | elle serre",
            "retry_prompt": "La casserole chante. Nina fait quoi ?",
            "engine_ok_text": "Oui, elle a attendu.",
            "engine_near_text": "Tu es près. La casserole chantait.",
        },
        "qemp": "tasse",
        "confirm": vet(
            [
                "enfant-f|J'ai attendu.",
                "narrateur|Oui, la tasse est restée sage.",
                "narrateur|Papa a entendu toute la phrase.",
                "narrateur|Maman ouvre la porte du jardin.",
                "papa|Le jaune nous attend.",
                "narrateur|Une goutte de cacao sèche sur le bois.",
            ]
        ),
        "arrive": {
            1: ["Nina court, la tasse contre le ventre."],
            2: ["Nina pose la tasse loin de l'eau."],
            3: ["Nina court vers le portail, tasse en main."],
        },
    },
    3: {
        "lab": "le crayon",
        "prop": "le crayon",
        "sons": "crayon,buee",
        "passage": vet(
            [
                "narrateur|Nina prend le gros crayon gras.",
                "narrateur|Sur la buée, elle dessine un ballon.",
                "narrateur|Un ovale, puis un trait pour la ficelle.",
                "enfant-f|Comme ça !",
                "narrateur|Papa se tourne vers le dessin.",
                "papa|Joli ballon, Nina.",
                "narrateur|Maman regarde le crayon, pas la vitre.",
                "narrateur|Dehors, le vrai jaune glisse.",
                "enfant-f|Pas celui-là.",
                "enfant-f|L'autre, dehors !",
                "narrateur|Nina pose le crayon sur le rebord.",
                "narrateur|Elle attend que papa finisse sa phrase.",
                "enfant-f|Le vrai est dans le jardin.",
                "maman|Alors ouvrons les yeux, dehors.",
            ]
        ),
        "question": vet(
            [
                "narrateur|Papa a vu le dessin.",
                "papa|Où est le vrai ballon ?",
            ]
        ),
        "qextra": {
            "expected_answer": "dehors",
            "accepted_examples": "dehors | jardin | romarin | dans le jardin",
            "retry_prompt": "Le dessin est sur la vitre. Le vrai est où ?",
            "engine_ok_text": "Oui, il est dehors.",
            "engine_near_text": "Tu es près. Regarde par le rond.",
        },
        "qemp": "ballon",
        "confirm": vet(
            [
                "enfant-f|Dehors !",
                "narrateur|Oui, dans le jardin mouillé.",
                "narrateur|Papa laisse le crayon sur le rebord.",
                "narrateur|Maman glisse les bras dans le manteau.",
                "maman|Montre-nous le vrai.",
                "narrateur|Le dessin reste, petit et jaune.",
            ]
        ),
        "arrive": {
            1: ["Nina court.", "Le crayon reste sur le rebord."],
            2: ["Nina court vers la flaque brillante."],
            3: ["Nina court vers le portail claquant."],
        },
    },
}

LOCS = {
    1: {
        "lab": "le romarin",
        "sound": "feuilles,vent",
        "q": ["Le vent secoue le jaune.", "Comment l'aider ?"],
        "body": vet(
            [
                "narrateur|Le ballon jaune est coincé entre deux branches.",
                "maman|J'ai vu la ficelle, à gauche.",
                "papa|Moi, j'ai vu une feuille collée.",
                "narrateur|Les deux voix arrivent ensemble.",
                "narrateur|Nina tourne la tête, perdue.",
                "enfant-f|Papa d'abord.",
                "enfant-f|Après, maman.",
                "narrateur|Papa montre la ficelle bleue.",
                "narrateur|Maman montre la feuille collée.",
                "narrateur|Les deux signes se rejoignent.",
                "narrateur|Le vent secoue le romarin.",
                "enfant-f|Il va s'envoler !",
            ]
        ),
    },
    2: {
        "lab": "la flaque",
        "sound": "flaque,botte",
        "q": ["La ficelle est dans l'eau.", "Comment l'aider ?"],
        "body": vet(
            [
                "narrateur|La ficelle traîne dans une flaque.",
                "papa|Je prends les bottes.",
                "maman|Je prends un bâton.",
                "narrateur|Ils parlent et marchent ensemble.",
                "narrateur|Deux éclaboussures cachent la ficelle.",
                "enfant-f|Un à la fois, s'il vous plaît.",
                "narrateur|Papa s'arrête.",
                "narrateur|Maman s'arrête aussi.",
                "narrateur|L'eau redevient un miroir.",
                "enfant-f|La ficelle, là, au milieu.",
            ]
        ),
    },
    3: {
        "lab": "le portail",
        "sound": "portail,vent",
        "q": ["Le portail va claquer.", "Comment l'aider ?"],
        "body": vet(
            [
                "narrateur|Le ballon se colle contre le portail.",
                "papa|Je ferme le gond, vite.",
                "narrateur|Sa main attrape le loquet.",
                "enfant-f|Stop, papa !",
                "narrateur|Le jaune est juste derrière.",
                "narrateur|Nina n'attend pas.",
                "narrateur|C'est trop près du gond.",
                "papa|J'écoute.",
                "papa|Je lâche.",
                "maman|Tu as bien fait de crier.",
                "narrateur|Le ballon tremble contre le bois.",
            ]
        ),
    },
}

SOLS = {
    1: {
        "lab": "la pince",
        "sons": "pince",
        "scenes": {
            1: vet(
                [
                    "narrateur|Nina prend une pince à linge bleue.",
                    "narrateur|Elle attend que papa finisse.",
                    "enfant-f|Pour la ficelle.",
                    "papa|Je te la tiens ?",
                    "narrateur|Nina tend la pince, sans un mot.",
                    "papa|Merci, Nina.",
                    "narrateur|Papa pince la ficelle près du nœud.",
                    "narrateur|Le romarin se redresse.",
                    "narrateur|Le ballon redescend vers maman.",
                    "maman|Je le tiens.",
                    "enfant-f|Il est un peu mouillé.",
                ]
            ),
            2: vet(
                [
                    "narrateur|Nina prend la pince à linge.",
                    "narrateur|Elle la tend quand maman a fini.",
                    "enfant-f|Pour sortir la ficelle.",
                    "maman|Je pince, tu dis où.",
                    "enfant-f|Un peu plus à gauche.",
                    "narrateur|La pince attrape le fil mouillé.",
                    "narrateur|Une goutte tombe dans la flaque.",
                    "papa|Bravo, Nina.",
                    "narrateur|Le ballon suit, léger.",
                    "maman|Il est à nous.",
                ]
            ),
            3: vet(
                [
                    "narrateur|Nina prend la pince à linge.",
                    "narrateur|Elle attend que le loquet soit libre.",
                    "enfant-f|On attache la ficelle au bois.",
                    "papa|Oui.",
                    "papa|À toi.",
                    "narrateur|Nina pince le fil au gond.",
                    "narrateur|Le ballon ne peut plus filer.",
                    "maman|Merci.",
                    "maman|Il reste avec nous.",
                    "narrateur|Le portail ne claque plus.",
                    "enfant-f|Il est sage, maintenant.",
                ]
            ),
        },
    },
    2: {
        "lab": "le bâton",
        "sons": "bois",
        "scenes": {
            1: vet(
                [
                    "narrateur|Nina choisit un bâton de noisette.",
                    "narrateur|Papa ouvre la bouche.",
                    "narrateur|Elle attend.",
                    "papa|Tu pousses la branche, ou moi ?",
                    "enfant-f|Toi.",
                    "enfant-f|Je dis quand.",
                    "narrateur|Papa baisse la branche.",
                    "narrateur|Nina lève la main.",
                    "enfant-f|Là.",
                    "narrateur|Maman attrape la ficelle.",
                    "narrateur|Le romarin reprend sa forme.",
                    "papa|Merci.",
                    "papa|J'ai entendu ton là.",
                ]
            ),
            2: vet(
                [
                    "narrateur|Nina prend un bâton plat.",
                    "narrateur|Elle le glisse vers papa.",
                    "enfant-f|Quand tu es prêt.",
                    "papa|Je le suis.",
                    "narrateur|Le bâton soulève la ficelle.",
                    "narrateur|L'eau fait un petit cercle.",
                    "maman|Je prends le fil.",
                    "narrateur|Le ballon quitte la flaque.",
                    "enfant-f|Il goutte sur mes bottes.",
                    "papa|Merci pour le tour de bâton.",
                ]
            ),
            3: vet(
                [
                    "narrateur|Nina prend le bâton de noisette.",
                    "narrateur|Elle touche le coude de papa.",
                    "enfant-f|Pousse le jaune vers maman.",
                    "papa|J'attends ton signal.",
                    "enfant-f|Maintenant.",
                    "narrateur|Le bâton guide le ballon.",
                    "narrateur|Maman ouvre les mains.",
                    "narrateur|Le portail reste immobile.",
                    "maman|Merci.",
                    "maman|Je l'ai.",
                    "enfant-f|Il sent le bois mouillé.",
                ]
            ),
        },
    },
    3: {
        "lab": "le silence",
        "sons": "jardin-calme",
        "scenes": {
            1: vet(
                [
                    "narrateur|Nina ne prend rien.",
                    "enfant-f|Chut.",
                    "enfant-f|Le vent va s'arrêter.",
                    "narrateur|La famille s'accroupit près du romarin.",
                    "narrateur|Une goutte tombe.",
                    "narrateur|Une abeille passe.",
                    "narrateur|Le ballon se calme entre les branches.",
                    "papa|Voilà ce que je n'avais pas vu.",
                    "maman|Il est venu tout seul.",
                    "narrateur|Maman prend la ficelle, sans tirer.",
                    "enfant-f|On a parlé avec les yeux.",
                ]
            ),
            2: vet(
                [
                    "narrateur|Nina s'assoit au bord de la flaque.",
                    "enfant-f|On regarde.",
                    "enfant-f|On ne marche pas.",
                    "narrateur|Papa ferme la bouche.",
                    "narrateur|Maman aussi.",
                    "narrateur|L'eau redevient lisse.",
                    "enfant-f|Le fil, au milieu.",
                    "narrateur|Papa avance un doigt, lentement.",
                    "narrateur|La ficelle vient.",
                    "maman|Merci d'avoir laissé l'eau parler.",
                    "enfant-f|Le ballon est à nous.",
                ]
            ),
            3: vet(
                [
                    "narrateur|Nina s'assoit contre le mur.",
                    "enfant-f|Le vent va se taire.",
                    "narrateur|Papa garde les mains loin du loquet.",
                    "narrateur|Maman s'accroupit de l'autre côté.",
                    "narrateur|On entend un merle, puis plus rien.",
                    "maman|Il avance vers toi, Nina.",
                    "narrateur|Nina ne répond pas tout de suite.",
                    "narrateur|Le ballon glisse vers l'herbe.",
                    "enfant-f|Maintenant, tu peux fermer.",
                    "papa|Merci.",
                    "papa|J'ai entendu ton maintenant.",
                ]
            ),
        },
    },
}

# Une ligne-objet unique par chemin (T3).
CB = {
    (1, 1, 1): "Le doigt de Nina reste froid, près de la pince.",
    (1, 1, 2): "Son doigt a dit là, sur le bâton.",
    (1, 1, 3): "Son doigt s'est tu, comme le vent.",
    (1, 2, 1): "Des gouttes perlent sur son doigt.",
    (1, 2, 2): "Son doigt a suivi le bâton plat.",
    (1, 2, 3): "Son doigt n'a pas touché l'eau.",
    (1, 3, 1): "Son doigt s'éloigne du gond, enfin.",
    (1, 3, 2): "Son doigt a donné le signal au bâton.",
    (1, 3, 3): "Son doigt se pose sur ses genoux.",
    (2, 1, 1): "La tasse vide attend au pied du romarin.",
    (2, 1, 2): "La tasse penche, comme le bâton.",
    (2, 1, 3): "La tasse est sage, dans l'herbe.",
    (2, 2, 1): "Nina pose la tasse loin de la flaque.",
    (2, 2, 2): "Une goutte d'eau rejoint la tasse.",
    (2, 2, 3): "La tasse reflète le ciel, près de l'eau.",
    (2, 3, 1): "La tasse sert de poids, près du gond.",
    (2, 3, 2): "La tasse tremble quand le bâton pousse.",
    (2, 3, 3): "La tasse reste entre Nina et le portail.",
    (3, 1, 1): "Sur la vitre, le dessin a un vrai frère.",
    (3, 1, 2): "Le crayon, au rebord, semble pousser aussi.",
    (3, 1, 3): "Le dessin sur la buée ne bouge plus.",
    (3, 2, 1): "Le trait gras penche vers la flaque, au loin.",
    (3, 2, 2): "Le crayon sent le bois, comme le bâton.",
    (3, 2, 3): "Le dessin attend, pendant que l'eau se tait.",
    (3, 3, 1): "Le crayon a laissé un gond minuscule, au rebord.",
    (3, 3, 2): "Le trait du crayon pointe vers le portail.",
    (3, 3, 3): "Le dessin respire, comme le jardin.",
}

# Fins : cuisine + recap + objet + rond. 27 textes distincts.
KITCHEN = {
    (1, 1, 1): "Dans la cuisine, le cacao a un peu refroidi.",
    (1, 1, 2): "Papa repose le bâton près du torchon rayé.",
    (1, 1, 3): "Une abeille bute un instant contre la vitre.",
    (1, 2, 1): "Des bottes mouillées sèchent près de l'évier.",
    (1, 2, 2): "Papa essuie le bâton plat sur le torchon.",
    (1, 2, 3): "Une flaque minuscule brille sur le carreau.",
    (1, 3, 1): "Le loquet a laissé une odeur de fer, au hall.",
    (1, 3, 2): "Le bâton de noisette sèche contre le mur.",
    (1, 3, 3): "Un merle chante derrière le portail fermé.",
    (2, 1, 1): "Nina pose la tasse près du cacao tiède.",
    (2, 1, 2): "Une feuille de romarin flotte dans la tasse.",
    (2, 1, 3): "Le cacao sent le romarin, un peu.",
    (2, 2, 1): "La tasse a une goutte d'eau sur l'oreille.",
    (2, 2, 2): "Papa verse enfin le cacao dans la tasse.",
    (2, 2, 3): "La tasse reflète la fenêtre, toute ronde.",
    (2, 3, 1): "Nina souffle sur le cacao, tasse aux deux mains.",
    (2, 3, 2): "Le cacao tremble, comme le portail tout à l'heure.",
    (2, 3, 3): "Maman pose la tasse loin du rebord.",
    (3, 1, 1): "Le crayon gras a taché le rebord, un point.",
    (3, 1, 2): "Papa range le crayon près des lettres sèches.",
    (3, 1, 3): "Le dessin jaune a pâli, sur la buée.",
    (3, 2, 1): "Une goutte coule du crayon vers l'évier.",
    (3, 2, 2): "Le crayon roule contre la tasse de papa.",
    (3, 2, 3): "Maman souffle sur le dessin, tout léger.",
    (3, 3, 1): "Le crayon pointe vers le jardin, oublié.",
    (3, 3, 2): "Papa pose le crayon à côté du ticket mouillé.",
    (3, 3, 3): "Le dessin et le vrai ballon se ressemblent enfin.",
}

RECAP = {
    (1, 1, 1): "J'ai tendu la pince. Papa avait fini.",
    (1, 1, 2): "J'ai dit là, avec le bâton.",
    (1, 1, 3): "On a laissé le vent se taire.",
    (1, 2, 1): "J'ai montré la gauche, pour la pince.",
    (1, 2, 2): "Le bâton a sorti le fil de l'eau.",
    (1, 2, 3): "L'eau a parlé. Après, le fil.",
    (1, 3, 1): "J'ai pincé le fil au gond.",
    (1, 3, 2): "J'ai dit maintenant, pour le bâton.",
    (1, 3, 3): "J'ai dit stop, puis j'ai attendu.",
    (2, 1, 1): "La tasse a attendu. La pince aussi.",
    (2, 1, 2): "J'ai gardé la tasse. Papa poussait.",
    (2, 1, 3): "On a regardé le romarin, sans un bruit.",
    (2, 2, 1): "J'ai posé la tasse. Maman a pincé.",
    (2, 2, 2): "Le bâton plat a fait un cercle.",
    (2, 2, 3): "On n'a pas marché dans l'eau.",
    (2, 3, 1): "La tasse pesait. La pince tenait.",
    (2, 3, 2): "J'ai touché le coude, puis le bâton.",
    (2, 3, 3): "Le vent s'est tu. J'ai dit fermer.",
    (3, 1, 1): "Le dessin était faux. La pince, vraie.",
    (3, 1, 2): "J'ai dit là. Le crayon restait dedans.",
    (3, 1, 3): "Le vrai ballon est venu tout seul.",
    (3, 2, 1): "On a pincé le fil. Le dessin regardait.",
    (3, 2, 2): "Le bâton a travaillé. Le crayon, non.",
    (3, 2, 3): "L'eau s'est tue. Le crayon aussi.",
    (3, 3, 1): "J'ai pincé le gond. Le dessin restait.",
    (3, 3, 2): "Le bâton a poussé. Le crayon pointait.",
    (3, 3, 3): "On a laissé le merle finir, d'abord.",
}

THANKS = {
    (1, 1, 1): "Merci. J'ai vu le jaune, grâce à toi.",
    (1, 1, 2): "Ton là était juste.",
    (1, 1, 3): "Le silence nous a aidés.",
    (1, 2, 1): "Tu as dit la gauche au bon moment.",
    (1, 2, 2): "Le bâton a bien travaillé.",
    (1, 2, 3): "L'eau était plus claire, après.",
    (1, 3, 1): "Le gond est sage, maintenant.",
    (1, 3, 2): "Ton maintenant est arrivé à temps.",
    (1, 3, 3): "Tu as crié, puis tu as laissé le vent.",
    (2, 1, 1): "La tasse a eu son tour, elle aussi.",
    (2, 1, 2): "Merci d'avoir gardé la tasse.",
    (2, 1, 3): "On a regardé ensemble, longtemps.",
    (2, 2, 1): "La pince a parlé après la tasse.",
    (2, 2, 2): "Le cacao est pour toi, après ça.",
    (2, 2, 3): "Merci d'avoir laissé l'eau se taire.",
    (2, 3, 1): "La tasse a tenu le portail, un peu.",
    (2, 3, 2): "J'ai senti ton doigt sur mon coude.",
    (2, 3, 3): "Merci pour le maintenant.",
    (3, 1, 1): "Le vrai ballon a gagné, dehors.",
    (3, 1, 2): "Le crayon peut dormir, maintenant.",
    (3, 1, 3): "Le dessin et le vent se sont tus.",
    (3, 2, 1): "La pince a fini ce que le dessin commençait.",
    (3, 2, 2): "Deux bois : le bâton, et le crayon.",
    (3, 2, 3): "Merci d'avoir distingué le vrai.",
    (3, 3, 1): "Le gond et le crayon se ressemblent, un peu.",
    (3, 3, 2): "Le portail a compris ton signal.",
    (3, 3, 3): "Le merle a eu son tour, lui aussi.",
}

CIRCLE = {
    (1, 1, 1): "Le petit rond garde une trace de doigt.",
    (1, 1, 2): "Le rond encadre le romarin, sans le jaune.",
    (1, 1, 3): "La buée revient autour du rond, lentement.",
    (1, 2, 1): "Une goutte descend le long du petit rond.",
    (1, 2, 2): "Le rond montre la flaque, calme à présent.",
    (1, 2, 3): "Nina souffle sur la vitre.",
    (1, 3, 1): "Le rond cadre le portail fermé.",
    (1, 3, 2): "Le doigt a laissé un trait sous le rond.",
    (1, 3, 3): "Derrière le rond, il reste le ciel.",
    (2, 1, 1): "Dans le rond, la tasse se reflète, minuscule.",
    (2, 1, 2): "Le rond sent le cacao, tout contre le nez.",
    (2, 1, 3): "Nina pose la tasse sous le petit rond.",
    (2, 2, 1): "Le rond a une larme, comme la flaque.",
    (2, 2, 2): "La buée du cacao agrandit le petit rond.",
    (2, 2, 3): "Le rond est un miroir, comme l'eau.",
    (2, 3, 1): "Le rond cadre la tasse et le jardin.",
    (2, 3, 2): "Nina voit le portail dans le rond, loin.",
    (2, 3, 3): "Le rond se ferme, chaud de cacao.",
    (3, 1, 1): "Le dessin rejoint le petit rond.",
    (3, 1, 2): "Le crayon a souligné le petit rond.",
    (3, 1, 3): "Le rond garde un ovale pâle, souvenir.",
    (3, 2, 1): "Une goutte traverse le rond, puis le dessin.",
    (3, 2, 2): "Le rond, le crayon, le cacao : trois ronds.",
    (3, 2, 3): "Nina efface le dessin, garde le petit rond.",
    (3, 3, 1): "Le rond cadre le gond, tout petit.",
    (3, 3, 2): "Le trait du crayon fuit vers le rond.",
    (3, 3, 3): "Le petit rond reste, vide et clair.",
}


def ending_lines(a: int, b: int, c: int) -> list[str]:
    key = (a, b, c)
    rec = RECAP[key]
    # Certaines recaps ont deux phrases. Les fendre si besoin.
    rec_lines = []
    if rec.count(".") + rec.count("?") + rec.count("!") > 1:
        parts = [p.strip() for p in rec.replace("?", "?|").replace("!", "!|").replace(".", ".|").split("|") if p.strip()]
        rec_lines = [f"enfant-f|{p}" for p in parts]
    else:
        rec_lines = [f"enfant-f|{rec}"]
    th = THANKS[key]
    th_lines = []
    if th.count(".") + th.count("?") + th.count("!") > 1:
        parts = [p.strip() for p in th.replace("?", "?|").replace("!", "!|").replace(".", ".|").split("|") if p.strip()]
        th_lines = [f"papa|{p}" for p in parts]
    else:
        th_lines = [f"papa|{th}"]
    return vet(
        [
            f"narrateur|{KITCHEN[key]}",
            "maman|À toi, Nina.",
            "maman|Nous t'écoutons.",
            *rec_lines,
            *th_lines,
            f"narrateur|{CB[key]}",
            f"narrateur|{CIRCLE[key]}",
        ]
    )


def t3_choice(b: int) -> list[str]:
    qs = [f"narrateur|{p}" for p in LOCS[b]["q"]]
    return vet(qs + ["papa|La pince, le bâton, ou le silence ?"])


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

    def put(cid: str, lines: list[str], profile: str, son: str = "", extra: dict | None = None, emp: str | None = None) -> None:
        scripts[cid] = lines if lines is scripts.get(cid) else vet(lines) if "|" in lines[0] and not lines[0].split("|", 1)[1] is None else lines
        # lines already vetted
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
                "narrateur|Sur le carreau froid, la buée fait des îles.",
                "narrateur|La petite maison sent le cacao.",
                "narrateur|Dehors, les toits brillent, mouillés.",
                "narrateur|Une gouttière laisse tomber une perle.",
                "narrateur|Nina vit ici, avec papa et maman.",
                "narrateur|Papa tourne la casserole brune.",
                "narrateur|Maman étale des lettres humides.",
                "narrateur|Un torchon rayé pend près de l'évier.",
                "narrateur|En ce moment, Nina monte sur le tabouret.",
                "narrateur|Elle trace un petit rond sur la buée.",
                "enfant-f|Un trou pour voir le jardin !",
                "narrateur|Dans le rond, un ballon jaune tremble.",
                "narrateur|Il est coincé dans le romarin.",
                "enfant-f|Papa, maman, le ballon !",
                "narrateur|Papa parle des lettres à maman.",
                "narrateur|Maman répond plus fort que Nina.",
                "narrateur|Les mots de Nina tombent dans les leurs.",
                "papa|Tu disais quelque chose, Nina ?",
                "enfant-f|Le ballon va partir.",
                "narrateur|La buée referme le petit rond.",
                "narrateur|Dehors, le vent pousse le jaune.",
                "enfant-f|Venez voir, vite !",
                "maman|Montre-nous, quand nous avons fini.",
            ]
        ),
        "opening",
        "pluie-legere,casserole",
        emp="petit rond",
    )

    put(
        "CHK_T0001_P0000",
        vet(
            [
                "narrateur|Nina peut se faire entendre autrement.",
                "papa|Le doigt, la tasse, ou le crayon ?",
                "maman|Que prends-tu, pour commencer ?",
            ]
        ),
        "choice",
        "",
        {"option_1_label": "le doigt", "option_2_label": "la tasse", "option_3_label": "le crayon"},
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
        put(f"{p}_C0001", st["confirm"], "confirm", "", emp="ballon")
        put(
            f"{p}_T0002_P0000",
            vet(
                [
                    "narrateur|Le ballon a bougé.",
                    "papa|Vers le romarin, la flaque, ou le portail ?",
                    "maman|Où va-t-on le chercher ?",
                ]
            ),
            "choice",
            "",
            {
                "option_1_label": "le romarin",
                "option_2_label": "la flaque",
                "option_3_label": "le portail",
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
                    "option_1_label": "la pince",
                    "option_2_label": "le bâton",
                    "option_3_label": "le silence",
                },
            )
            for c, sol in SOLS.items():
                leaf = f"{sp}_T0003_P000{c}"
                put(leaf, leaf_body(a, b, c), "resolution", sol["sons"])
                fin_sons = {1: "cacao,romarin", 2: "cacao,goutte", 3: "cacao,merle"}[b]
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
        "Après la pluie, Nina trace un petit rond sur la vitre embuée. "
        "À travers, un ballon jaune tremble dans le romarin. Elle veut le montrer "
        "avant que la buée referme le trou, mais papa et maman parlent : ses mots "
        "tombent. Taper, apporter la tasse ou dessiner échoue d'abord. Quand on "
        "l'écoute, la piste mène au romarin, à la flaque ou au portail. Une pince, "
        "un bâton ou un silence rendent le jaune. Le cacao attend. Le petit rond aussi."
    )
    out["title"] = "Le petit rond sur la vitre"
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "petite maison du village, vitre de cuisine embuée après la pluie"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    fins = [c["text"] for c in out["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27:
        raise SystemExit(f"fins {len(fins)}")
    if len(set(fins)) != 27:
        raise SystemExit("fins non distinctes")

    # chemins
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

    tics = ("tout doux", "tout calme", "on lève la main", "puis on parle", "voici le geste")
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for t in tics:
        if t in blob:
            raise SystemExit(f"tic: {t}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    vecu = (
        "Nina veut montrer le ballon vu dans le petit rond, avant que la buée "
        "referme le trou. Crier échoue : papa et maman parlent. Taper trop fort, "
        "porter la tasse trop tôt ou montrer un dessin à la place du vrai : "
        "première idée ratée. Le doigt sur le poignet, la casserole qui se tait, "
        "ou attendre la fin de la phrase changent l'action. Au romarin les voix "
        "se mélangent ; à la flaque les pas aussi ; au portail Nina crie stop "
        "parce que le gond menace. Pince, bâton ou silence : trois façons d'être "
        "entendu. Le cacao et le petit rond referment."
    )
    notes = (
        "Reprise complète 86 nœuds. Labels T1 doigt/tasse/crayon, T2 romarin/"
        "flaque/portail, T3 pince/bâton/silence : le choix change l'obstacle et "
        "la fin. 27 fins textuellement distinctes. Leçon COL.ECO.002 vécue, pas "
        "dite. N1≤10. TTS par fonction (opening/choice/clue/confirm/action/"
        "obstacle/resolution/ending). Un merci et un bravo vécus, une question "
        "adulte. Pas apply."
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — Le petit rond sur la vitre\n\n"
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


if __name__ == "__main__":
    main()
