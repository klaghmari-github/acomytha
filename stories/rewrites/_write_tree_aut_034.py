#!/usr/bin/env python3
"""TREE-AUT-034 — F-NAR-019. Abri sous le prunier. TTS complet. Pas d'apply."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-034"
N2 = 15
TICS = ("tout doux", "tout calme", "tout lent", " encore ", " déjà ", "aujourd'hui,")

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "abri",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le soleil mange l_ombre; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change l_abri; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_geste; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=l_abri_n_est_pas_fini; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_ça_tombe; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_bazar_vole_l_ombre; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=l_abri_tient_parce_que_la_place_est_libre; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_ombre_promise_est_là; tempo=posé; sourire=léger; respiration=ample",
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
        low = f" {ph.lower()} "
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
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
    nc["sons"] = sons
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


OPENING = [
    "narrateur|Au fond du jardin, un vieux prunier penche.",
    "narrateur|Des prunes violettes sentent le sucre chaud.",
    "narrateur|Un fil à linge coupe l'air, léger.",
    "narrateur|Des pinces dansent quand maman accroche un torchon.",
    "narrateur|Une caisse de bois attend au pied de l'arbre.",
    "narrateur|Sa corde est rêche, un peu froide.",
    "narrateur|L'arrosoir bleu laisse tomber une goutte.",
    "narrateur|Ploc, sur la terre sombre.",
    "narrateur|Papa pose ses bottes près de la porte.",
    "maman|Tu as vu l'escargot, Amir ?",
    "enfant-m|Oui, il est sur la feuille mouillée.",
    "narrateur|En ce moment, Amir s'accroupit sous l'ombre.",
    "narrateur|Le soleil mange le bord de la feuille.",
    "enfant-m|Il va avoir trop chaud !",
    "enfant-m|Je lui fais un abri, vite !",
    "papa|Avant que l'ombre parte ?",
    "enfant-m|Oui papa, un vrai toit.",
    "narrateur|Amir bascule la caisse d'un coup.",
    "narrateur|Jouets, galets, un chiffon : tout tombe.",
    "narrateur|Il empile le tas au-dessus de la feuille.",
    "narrateur|La pile penche, puis s'écroule.",
    "narrateur|Un cube roule vers la coquille.",
    "enfant-m|Ça tombe partout !",
    "narrateur|L'escargot rentre sa tête, d'un coup.",
    "maman|Il a eu peur du tas.",
    "papa|L'ombre part, que prends-tu d'abord ?",
]

T1_CHOICE = [
    "narrateur|Pour l'abri, Amir peut prendre le torchon, la caisse, ou l'arrosoir.",
    "maman|Que prends-tu en premier ?",
]

T1 = {
    1: {
        "lab": "le torchon",
        "sons": "fil-linge,pince",
        "emphasis": "torchon",
        "passage": [
            "narrateur|Amir tire le torchon rayé du fil.",
            "narrateur|Une pince saute et tombe dans l'herbe.",
            "enfant-m|Un toit, tout de suite !",
            "narrateur|Il jette le tissu au-dessus de la feuille.",
            "narrateur|Le torchon est trop large, trop lourd.",
            "narrateur|Il s'affaisse et colle à la terre.",
            "enfant-m|Il ne voit plus rien.",
            "maman|Il étouffe un peu, non ?",
            "papa|Le tissu touche tes bottes, là.",
            "narrateur|Amir tire, le cœur serré.",
            "narrateur|Une botte bascule vers la coquille.",
            "enfant-m|Non, pas sur lui !",
        ],
        "question": [
            "narrateur|Qu'est-ce qu'Amir a tiré du fil ?",
        ],
        "qfields": {
            "expected_answer": "torchon",
            "accepted_examples": "torchon | le torchon | torchon rayé | le tissu",
            "retry_prompt": "Écoute l'indice, et réessaie.",
        },
        "confirm": [
            "enfant-m|Le torchon !",
            "narrateur|Oui, le torchon rayé du fil.",
            "narrateur|Amir le soulève d'un bord.",
            "narrateur|L'escargot est là, serré.",
            "papa|Le tissu peut servir, plus tard.",
            "maman|Le sol autour est trop plein.",
        ],
    },
    2: {
        "lab": "la caisse",
        "sons": "bois,corde",
        "emphasis": "caisse",
        "passage": [
            "narrateur|Amir saisit la corde de la caisse.",
            "narrateur|Il veut la poser comme une grotte.",
            "enfant-m|Une maison en bois, hop !",
            "narrateur|Il pousse trop vite.",
            "narrateur|Un chiffon, un galet, une chaussette s'échappent.",
            "narrateur|La caisse atterrit de travers.",
            "narrateur|L'ouverture tape un râteau couché.",
            "enfant-m|Elle ne tient pas.",
            "papa|Elle est trop pleine pour servir.",
            "maman|On dirait un tas, pas un abri.",
            "narrateur|Amir lâche la corde.",
            "narrateur|Ses épaules baissent.",
        ],
        "question": [
            "narrateur|Qu'est-ce qu'Amir a voulu poser en grotte ?",
        ],
        "qfields": {
            "expected_answer": "caisse",
            "accepted_examples": "caisse | la caisse | caisse de bois | la grotte",
            "retry_prompt": "Écoute l'indice, et réessaie.",
        },
        "confirm": [
            "enfant-m|La caisse !",
            "narrateur|Oui, la caisse de bois.",
            "narrateur|Elle repose de travers.",
            "narrateur|Un coin d'ombre y tremble.",
            "maman|Elle veut être une grotte.",
            "papa|Quand le sol sera libre.",
        ],
    },
    3: {
        "lab": "l'arrosoir",
        "sons": "eau,goutte",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|Amir soulève l'arrosoir bleu à deux mains.",
            "narrateur|Il veut rafraîchir la terre, vite.",
            "enfant-m|De l'eau froide pour lui !",
            "narrateur|Il penche trop.",
            "narrateur|Un filet court vers la feuille.",
            "narrateur|Un caillou part avec l'eau.",
            "narrateur|L'escargot rentre, minuscule.",
            "enfant-m|J'en ai mis trop.",
            "maman|L'eau a cherché le tas.",
            "papa|Elle se perd sous les affaires.",
            "narrateur|Amir pose l'arrosoir, déçu.",
            "narrateur|Le soleil avance d'un doigt.",
        ],
        "question": [
            "narrateur|Que verse Amir près de la feuille ?",
        ],
        "qfields": {
            "expected_answer": "eau",
            "accepted_examples": "eau | de l'eau | arrosoir | l'arrosoir | l'eau",
            "retry_prompt": "Écoute l'indice, et réessaie.",
        },
        "confirm": [
            "enfant-m|De l'eau !",
            "narrateur|Oui, l'eau de l'arrosoir bleu.",
            "narrateur|La terre a soif, et l'escargot aussi.",
            "papa|Un filet, pas une rivière.",
            "maman|Le tas autour boit tout.",
            "narrateur|Une goutte reste au bord du bec.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le torchon s'accroche au bazar du pied.",
        "papa|Les bottes, le râteau, ou le panier gênent.",
        "maman|Que remets-tu à sa place ?",
    ],
    2: [
        "narrateur|La caisse ne pose pas droit.",
        "papa|Les bottes, le râteau, ou le panier gênent.",
        "maman|Que remets-tu à sa place ?",
    ],
    3: [
        "narrateur|L'eau se perd sous les affaires.",
        "papa|Les bottes, le râteau, ou le panier gênent.",
        "maman|Que remets-tu à sa place ?",
    ],
}

T2 = {
    (1, 1): {
        "lab": "les bottes",
        "sons": "bottes,tissu",
        "emphasis": "bottes",
        "passage": [
            "narrateur|Le torchon traîne et s'accroche à une botte.",
            "narrateur|Amir tire plus fort.",
            "narrateur|La botte bascule, lourde.",
            "papa|Attention, elle va sur la feuille !",
            "enfant-m|Je n'arrive pas.",
            "narrateur|Amir lâche le tissu.",
            "narrateur|Il prend les bottes, une par une.",
            "narrateur|Il les pose sur le paillasson.",
            "papa|Merci, Amir, elles ont leur place.",
            "maman|L'ombre est plus large, tu vois ?",
            "narrateur|Le torchon respire, plat.",
        ],
    },
    (1, 2): {
        "lab": "le râteau",
        "sons": "metal,tissu",
        "emphasis": "râteau",
        "passage": [
            "narrateur|Le torchon s'enroule autour d'une dent.",
            "narrateur|Amir secoue le tissu.",
            "narrateur|Le râteau glisse vers l'escargot.",
            "enfant-m|Il va le toucher !",
            "maman|Les dents sont trop près.",
            "narrateur|Amir recule d'un pas.",
            "narrateur|Il soulève le râteau à deux mains.",
            "narrateur|Il le dresse contre le mur du fond.",
            "papa|Merci, le mur le reprend.",
            "narrateur|Le torchon se libère, d'un coup.",
            "maman|La terre est libre, là.",
        ],
    },
    (1, 3): {
        "lab": "le panier",
        "sons": "prunes,osier",
        "emphasis": "panier",
        "passage": [
            "narrateur|Le torchon heurte le panier de prunes.",
            "narrateur|Trois prunes roulent vers la feuille.",
            "enfant-m|Elles vont l'écraser !",
            "papa|Attrape le panier d'abord.",
            "narrateur|Amir rassemble les prunes, vite.",
            "narrateur|Il les remet dans l'osier.",
            "narrateur|Il pose le panier sur le banc.",
            "maman|Merci pour les prunes.",
            "narrateur|Le torchon n'a plus rien à frapper.",
            "papa|L'abri a de la place.",
        ],
    },
    (2, 1): {
        "lab": "les bottes",
        "sons": "bottes,bois",
        "emphasis": "bottes",
        "passage": [
            "narrateur|Amir pousse la caisse vers l'ombre.",
            "narrateur|Une botte bloque le bord.",
            "narrateur|La grotte penche et claque le bois.",
            "enfant-m|Elle ne s'assoit pas.",
            "papa|La botte vole sa place.",
            "narrateur|Amir pose la caisse un instant.",
            "narrateur|Il emporte les bottes vers la porte.",
            "maman|Merci, le paillasson les revoilà.",
            "narrateur|La terre sous le prunier redevient plate.",
            "enfant-m|Maintenant, la grotte peut s'ouvrir.",
        ],
    },
    (2, 2): {
        "lab": "le râteau",
        "sons": "metal,bois",
        "emphasis": "râteau",
        "passage": [
            "narrateur|Le manche du râteau barre l'entrée.",
            "narrateur|Amir veut coincer la caisse quand même.",
            "narrateur|Le bois tape le fer, un coup sec.",
            "enfant-m|Ça fait trop de bruit.",
            "maman|Il va se cacher.",
            "narrateur|Amir recule la caisse.",
            "narrateur|Il porte le râteau contre le mur.",
            "papa|Merci, il ne traîne plus.",
            "narrateur|L'entrée de la grotte est nette.",
            "enfant-m|Il pourra rentrer, là.",
        ],
    },
    (2, 3): {
        "lab": "le panier",
        "sons": "prunes,bois",
        "emphasis": "panier",
        "passage": [
            "narrateur|Le panier coincé sous la caisse l'empêche de poser.",
            "narrateur|Amir pousse, les prunes bougent.",
            "enfant-m|Le panier est trop gros.",
            "papa|Sors-le, puis la grotte.",
            "narrateur|Amir tire l'osier hors du bois.",
            "narrateur|Il pose le panier sur le banc.",
            "maman|Merci, les prunes ont leur ombre à elles.",
            "narrateur|La caisse touche enfin la terre.",
            "enfant-m|Une vraie maison, cette fois.",
        ],
    },
    (3, 1): {
        "lab": "les bottes",
        "sons": "eau,bottes",
        "emphasis": "bottes",
        "passage": [
            "narrateur|L'eau glisse et entre dans une botte.",
            "narrateur|La botte s'alourdit, molle.",
            "enfant-m|J'ai mouillé papa !",
            "papa|Ce n'est pas grave, au paillasson ?",
            "narrateur|Amir rit un peu, puis s'arrête.",
            "narrateur|Il vide la botte, loin de la feuille.",
            "narrateur|Il ramène les deux au paillasson.",
            "maman|Merci, tes pieds papa vont sécher.",
            "narrateur|La terre reste fraîche, sans tas.",
            "enfant-m|L'eau est pour lui, pas pour nous.",
        ],
    },
    (3, 2): {
        "lab": "le râteau",
        "sons": "eau,metal",
        "emphasis": "râteau",
        "passage": [
            "narrateur|L'eau suit le manche du râteau.",
            "narrateur|Elle court droit vers la coquille.",
            "enfant-m|Le râteau fait un fleuve !",
            "maman|Enlève le pont, alors.",
            "narrateur|Amir tire le râteau hors du filet.",
            "narrateur|Il le dresse contre le mur.",
            "papa|Merci, l'eau peut rester près de l'arbre.",
            "narrateur|Un petit creux frais demeure.",
            "enfant-m|Ici, c'est son bain, pas une rivière.",
        ],
    },
    (3, 3): {
        "lab": "le panier",
        "sons": "eau,prunes",
        "emphasis": "panier",
        "passage": [
            "narrateur|Les gouttes tapent les prunes du panier.",
            "narrateur|L'osier s'assombrit, lourd.",
            "enfant-m|Les prunes n'aiment pas ça.",
            "papa|Le banc est plus sec, tu crois ?",
            "narrateur|Amir soulève le panier à deux mains.",
            "narrateur|Il le pose au soleil, sur le banc.",
            "maman|Merci, elles vont sécher, elles.",
            "narrateur|Sous le prunier, la terre reste sombre.",
            "enfant-m|L'eau est à lui, maintenant.",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Les bottes ont quitté l'ombre.",
        "papa|Les pinces, la corde, ou le seau ?",
        "maman|Comment finir l'abri ?",
    ],
    2: [
        "narrateur|Le râteau garde le mur.",
        "papa|Les pinces, la corde, ou le seau ?",
        "maman|Comment finir l'abri ?",
    ],
    3: [
        "narrateur|Le panier repose sur le banc.",
        "papa|Les pinces, la corde, ou le seau ?",
        "maman|Comment finir l'abri ?",
    ],
}

# 27 résolutions distinctes : (t1, t2, t3)
T3 = {
    (1, 1, 1): [
        "narrateur|Amir plie le torchon en deux.",
        "narrateur|Il plante deux pinces dans la terre souple.",
        "narrateur|Le tissu tient, comme une tente minuscule.",
        "enfant-m|Un toit à lui !",
        "narrateur|Une corne sort, puis l'autre.",
        "papa|Il a compris, sans qu'on le pousse.",
        "maman|L'abri est petit, et c'est mieux.",
        "narrateur|Là où les bottes étaient, la terre sèche.",
        "narrateur|Sous le torchon, elle reste sombre.",
    ],
    (1, 1, 2): [
        "narrateur|Amir noue la corde de la caisse au torchon.",
        "narrateur|Il tend un toit en pente, vers le paillasson.",
        "narrateur|Le soleil glisse sur le tissu, pas dessous.",
        "enfant-m|Ça tient tout seul !",
        "narrateur|L'escargot avance d'un pas humide.",
        "maman|La corde savait attendre dans le bois.",
        "papa|Et les bottes savent attendre à la porte.",
        "narrateur|Un triangle d'ombre se pose sur la feuille.",
    ],
    (1, 1, 3): [
        "narrateur|Amir couche le petit seau sur le flanc.",
        "narrateur|L'ouverture regarde la feuille, pas le soleil.",
        "narrateur|Le torchon devient un rideau sur le bord.",
        "enfant-m|Un porche bleu !",
        "narrateur|Deux cornes tâtent l'air frais du seau.",
        "papa|Il choisit l'entrée, tout seul.",
        "maman|Tes bottes, elles, ont choisi le paillasson.",
        "narrateur|Une goutte glisse du seau, ploc, à côté.",
    ],
    (1, 2, 1): [
        "narrateur|Amir plante les pinces dans la trace du râteau.",
        "narrateur|Le torchon s'accroche, sans dent de fer.",
        "narrateur|Un toit étroit suit l'ancienne ligne.",
        "enfant-m|Plus de râteau, plus de danger.",
        "narrateur|L'escargot suit cette ombre neuve.",
        "maman|Les pinces savent tenir autre chose que le linge.",
        "papa|Le mur, lui, tient le râteau.",
        "narrateur|Une dent d'acier ne touche plus le tissu.",
    ],
    (1, 2, 2): [
        "narrateur|Amir tend la corde le long de la trace du râteau.",
        "narrateur|Le torchon s'y couche, en pente douce.",
        "narrateur|Le manche, au mur, ne vole plus le fil.",
        "enfant-m|Un chemin d'ombre !",
        "narrateur|La coquille s'engage dessous, lente.",
        "papa|La corde a trouvé mieux qu'un tas.",
        "maman|Et le fer a trouvé le mur.",
        "narrateur|L'herbe se relève où le râteau couchait.",
    ],
    (1, 2, 3): [
        "narrateur|Amir pose le seau dans l'ombre du râteau parti.",
        "narrateur|Le torchon couvre le dessus, comme un chapeau.",
        "narrateur|Un rond bleu coupe le rayon.",
        "enfant-m|Sa cabane ronde !",
        "narrateur|L'escargot contourne le seau, puis entre.",
        "maman|Le râteau n'aurait pas fait ce toit.",
        "papa|Au mur, il fait un autre métier.",
        "narrateur|Une lame de soleil s'arrête sur le bleu.",
    ],
    (1, 3, 1): [
        "narrateur|Amir pince le torchon au-dessus de la feuille.",
        "narrateur|Une tache de prune teinte un coin du tissu.",
        "enfant-m|Il a un toit rose !",
        "narrateur|Les pinces tiennent malgré le sucre collant.",
        "narrateur|L'escargot sort, attiré par l'ombre sucrée.",
        "papa|Les prunes, elles, dorment dans le panier.",
        "maman|Le banc leur suffit.",
        "narrateur|Une pince claque, puis se tait.",
    ],
    (1, 3, 2): [
        "narrateur|Amir attache le torchon avec la corde, loin de l'anse.",
        "narrateur|Une feuille de prune reste coincée dans le nœud.",
        "enfant-m|Un drapeau de prune !",
        "narrateur|Le toit penche, et l'escargot le suit.",
        "maman|L'anse du panier ne tire plus le tissu.",
        "papa|Les prunes tiennent leur tas, sur le banc.",
        "narrateur|Le nœud sent le fruit, un peu.",
        "narrateur|Sous le prunier, l'air devient plus frais.",
    ],
    (1, 3, 3): [
        "narrateur|Amir glisse le seau près de la feuille tachée.",
        "narrateur|Le torchon tombe en rideau sur le bleu.",
        "enfant-m|Ça sent les prunes, et l'eau.",
        "narrateur|L'escargot hésite, puis choisit le frais.",
        "papa|Le panier sent le sucre, plus loin.",
        "maman|Chacun a son ombre.",
        "narrateur|Une prune mûre brille sur le banc.",
        "narrateur|Sous le seau, la terre reste noire.",
    ],
    (2, 1, 1): [
        "narrateur|Amir couche la caisse sur le flanc.",
        "narrateur|Deux pinces marquent la porte, vers le nord.",
        "narrateur|L'ouverture fuit l'empreinte des bottes.",
        "enfant-m|Entrez, c'est ouvert !",
        "narrateur|La coquille franchit le seuil de bois.",
        "papa|Les pinces font les gardiens.",
        "maman|Les bottes gardent la porte de la maison.",
        "narrateur|Un carré d'ombre s'installe dans la caisse.",
    ],
    (2, 1, 2): [
        "narrateur|Amir cale la caisse avec sa corde, en biais.",
        "narrateur|Le toit de bois penche, loin du paillasson.",
        "enfant-m|Une grotte penchée !",
        "narrateur|L'escargot gravit le bord, puis descend dedans.",
        "maman|La corde l'empêche de refermer.",
        "papa|Tes bottes n'appuient plus dessus.",
        "narrateur|Le bois craque, puis se tait.",
        "narrateur|Au fond, une fraîcheur de cave.",
    ],
    (2, 1, 3): [
        "narrateur|Amir glisse le seau dans l'ouverture de la caisse.",
        "narrateur|Le bleu fait une entrée avant le bois.",
        "enfant-m|Deux maisons, l'une dans l'autre !",
        "narrateur|L'escargot choisit d'abord le seau, plus frais.",
        "papa|Le seau était vide, il servait à rien.",
        "maman|Là, il sert à l'ombre.",
        "narrateur|Une botte sèche au loin, oubliée du drame.",
        "narrateur|Dans le bois, un silence rond.",
    ],
    (2, 2, 1): [
        "narrateur|Amir plante les pinces de chaque côté de l'entrée.",
        "narrateur|La caisse ouvre une bouche vers l'herbe.",
        "narrateur|La trace du râteau passe à côté, vide.",
        "enfant-m|Pas de fer dans la porte.",
        "narrateur|L'escargot s'engage, sans un bruit.",
        "maman|Les pinces tiennent le rideau d'herbe.",
        "papa|Le râteau, au mur, se tait.",
        "narrateur|Un rayon de soleil s'arrête sur le bois.",
    ],
    (2, 2, 2): [
        "narrateur|Amir attache la corde au rebord de la caisse.",
        "narrateur|Il la fixe dans la trace du râteau.",
        "narrateur|La grotte ne peut plus basculer.",
        "enfant-m|Elle est attachée !",
        "narrateur|L'escargot entre, rassuré : plus rien ne bouge.",
        "papa|La corde a gagné contre le manche.",
        "maman|Le fer dort au mur.",
        "narrateur|Le bois ne tremble plus.",
    ],
    (2, 2, 3): [
        "narrateur|Amir cale le seau contre le côté de la caisse.",
        "narrateur|Le bleu bouche le trou où le manche passait.",
        "enfant-m|Plus de courant d'air chaud.",
        "narrateur|L'escargot disparaît dans le double abri.",
        "maman|Le seau ferme ce que le râteau ouvrait.",
        "papa|Bon échange.",
        "narrateur|Une ombre épaisse remplit le bois.",
        "narrateur|Au mur, une dent d'acier capte un rayon.",
    ],
    (2, 3, 1): [
        "narrateur|Amir pince un coin de chiffon à l'entrée de la caisse.",
        "narrateur|Le chiffon sent la prune, un peu.",
        "enfant-m|Un rideau sucré !",
        "narrateur|L'escargot soulève le tissu, puis passe.",
        "papa|Les pinces tiennent le parfum dehors.",
        "maman|Le panier, sur le banc, garde le reste.",
        "narrateur|Une tache violette sèche au soleil du banc.",
        "narrateur|Dans la caisse, l'air n'a plus de fruit.",
    ],
    (2, 3, 2): [
        "narrateur|Amir noue la corde à l'anse vide, trop loin.",
        "narrateur|Non : il la noue au bois, pas à l'osier.",
        "enfant-m|La caisse d'abord !",
        "narrateur|La grotte se cale, solide.",
        "narrateur|L'escargot y glisse, à l'abri du sucre.",
        "maman|L'anse du panier n'a plus à tirer.",
        "papa|Chacun son nœud.",
        "narrateur|Sur le banc, les prunes font un tas rond.",
    ],
    (2, 3, 3): [
        "narrateur|Amir pose le seau en garde devant la caisse.",
        "narrateur|Le bleu sépare le bois du banc aux prunes.",
        "enfant-m|Personne ne roule dessus.",
        "narrateur|L'escargot entre par le côté, loin du fruit.",
        "papa|Le seau fait le garde.",
        "maman|Les prunes font la confiture, plus tard.",
        "narrateur|Une odeur sucrée s'arrête au bleu.",
        "narrateur|Au fond de la caisse, la terre sent l'humide.",
    ],
    (3, 1, 1): [
        "narrateur|Amir plante les pinces autour du creux mouillé.",
        "narrateur|Elles tiennent un bout de torchon, juste assez.",
        "enfant-m|Un puits avec un chapeau !",
        "narrateur|L'escargot redescend vers l'eau, à l'ombre.",
        "papa|Les pinces n'ont pas mouillé, elles.",
        "maman|Tes bottes non plus, maintenant.",
        "narrateur|Le creux brille, petit miroir.",
        "narrateur|Une corne y boit, ou presque.",
    ],
    (3, 1, 2): [
        "narrateur|Amir tend la corde au-dessus du filet d'eau.",
        "narrateur|Un coin de tissu y pend, comme un petit toit.",
        "enfant-m|L'eau reste à lui.",
        "narrateur|L'escargot longe le frais, sous le tissu.",
        "maman|La corde fait le pont, sans bottes dessous.",
        "papa|Au paillasson, le cuir sèche.",
        "narrateur|Le filet ne part plus vers la porte.",
        "narrateur|Il tourne autour de la feuille.",
    ],
    (3, 1, 3): [
        "narrateur|Amir pose le seau à l'envers, près du creux.",
        "narrateur|Une fente laisse l'air, pas le soleil.",
        "enfant-m|Une grotte d'eau !",
        "narrateur|L'escargot s'y glisse, coquille luisante.",
        "papa|Le seau a bu le trop-plein.",
        "maman|La botte, elle, n'en boit plus.",
        "narrateur|Une flaque ronde s'endort sous le bleu.",
        "narrateur|Le paillasson, au loin, reste clair.",
    ],
    (3, 2, 1): [
        "narrateur|Amir pince un toit au-dessus du creux, hors de la trace.",
        "narrateur|L'eau ne suit plus le fer.",
        "enfant-m|Elle reste en rond.",
        "narrateur|L'escargot s'installe au bord, à l'ombre des pinces.",
        "maman|Les pinces font un cercle, pas un fleuve.",
        "papa|Le râteau, au mur, ne pousse plus l'eau.",
        "narrateur|Une dent sèche capte la lumière, loin.",
        "narrateur|Près de la feuille, tout est mat.",
    ],
    (3, 2, 2): [
        "narrateur|Amir barre la trace avec la corde, à plat.",
        "narrateur|L'eau s'arrête et forme une mare.",
        "enfant-m|J'ai fermé la rivière !",
        "narrateur|L'escargot contourne la mare, sous un bout tendu.",
        "papa|La corde a battu le manche.",
        "maman|Le mur garde le fer.",
        "narrateur|La mare tremble, puis se calme.",
        "narrateur|Deux cornes s'y reflètent, un instant.",
    ],
    (3, 2, 3): [
        "narrateur|Amir pose le seau en travers de la trace vide.",
        "narrateur|L'eau s'y rassemble, fraîche.",
        "enfant-m|Un réservoir pour lui.",
        "narrateur|L'escargot gravit le bord humide, puis s'abrite.",
        "maman|Le seau capte ce que le râteau répandait.",
        "papa|Échange réussi.",
        "narrateur|Une goutte tombe dedans, ploc.",
        "narrateur|Au mur, le fer reste sec.",
    ],
    (3, 3, 1): [
        "narrateur|Amir plante les pinces entre le creux et le banc.",
        "narrateur|Un bout de tissu arrête les gouttes vers les prunes.",
        "enfant-m|L'eau d'un côté, le sucre de l'autre.",
        "narrateur|L'escargot choisit le côté mouillé.",
        "papa|Les pinces font la frontière.",
        "maman|Le panier, au sec, se tait.",
        "narrateur|Une prune roule sur le banc, sans tomber.",
        "narrateur|Sous les pinces, la terre brille.",
    ],
    (3, 3, 2): [
        "narrateur|Amir tend la corde du creux jusqu'au tronc.",
        "narrateur|Le bout de tissu fait un couloir, loin du banc.",
        "enfant-m|Son chemin à lui.",
        "narrateur|L'escargot s'y engage, dos aux prunes.",
        "maman|La corde l'éloigne du sucre.",
        "papa|Le panier n'a plus à craindre l'eau.",
        "narrateur|L'osier blanchit au soleil du banc.",
        "narrateur|Le couloir, lui, reste sombre.",
    ],
    (3, 3, 3): [
        "narrateur|Amir pose le seau entre le creux et les prunes.",
        "narrateur|Le bleu coupe l'odeur sucrée.",
        "enfant-m|Deux mondes !",
        "narrateur|L'escargot entre du côté de l'eau.",
        "papa|Le seau a choisi son camp.",
        "maman|Les prunes aussi, sur leur banc.",
        "narrateur|Une goutte chante dans le bleu.",
        "narrateur|Sur le banc, une prune se fend, sans bruit.",
    ],
}

T3_SONS = {1: "pinces,tissu", 2: "corde,bois", 3: "seau,goutte"}
T3_EMPH = {1: "pinces", 2: "corde", 3: "seau"}
T3_LAB = {1: "les pinces", 2: "la corde", 3: "le seau"}
T2_LAB = {1: "les bottes", 2: "le râteau", 3: "le panier"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Amir revient vers le paillasson.",
        "papa|Quel toit as-tu choisi ?",
        "enfant-m|Deux pinces, et le torchon du fil.",
        "maman|Les bottes ont retrouvé la porte.",
        "narrateur|Une pince vide danse sur le fil.",
        "narrateur|Sous le prunier, le petit toit rayé ne bouge pas.",
    ],
    (1, 1, 2): [
        "narrateur|Amir essuie ses mains à la corde vide.",
        "papa|La pente va où ?",
        "enfant-m|Vers vos bottes, mais pas dessus.",
        "maman|Elles sèchent, et lui aussi, à sa façon.",
        "narrateur|Le paillasson garde deux empreintes claires.",
        "narrateur|Le triangle d'ombre tient, sous les prunes.",
    ],
    (1, 1, 3): [
        "narrateur|Amir pose l'arrosoir près du seau resté dehors.",
        "papa|Qui a le porche ?",
        "enfant-m|Lui : le seau bleu, et le rideau.",
        "maman|Tes bottes ont le paillasson, c'est leur porche.",
        "narrateur|Une goutte quitte le bec, ploc.",
        "narrateur|Dans le seau, l'ombre sent l'eau froide.",
    ],
    (1, 2, 1): [
        "narrateur|Amir regarde le mur où le râteau dort.",
        "papa|Il te gêne, maintenant ?",
        "enfant-m|Non, les pinces tiennent le vrai toit.",
        "maman|Chacun son mur, chacun son fil.",
        "narrateur|Une dent d'acier jette un éclat mince.",
        "narrateur|Le torchon, lui, reste mat au-dessus de la feuille.",
    ],
    (1, 2, 2): [
        "narrateur|Amir suit du doigt la trace vide.",
        "papa|C'était le chemin du fer.",
        "enfant-m|Maintenant, c'est le chemin de la corde.",
        "maman|L'herbe va se relever.",
        "narrateur|Le manche au mur ne bouge plus.",
        "narrateur|Sous le tissu, une petite trace mouillée brille.",
    ],
    (1, 2, 3): [
        "narrateur|Amir tape deux doigts sur le seau.",
        "papa|Ça sonne creux ?",
        "enfant-m|Creux et frais, il est dedans.",
        "maman|Le râteau sonnerait trop dur.",
        "narrateur|Au mur, le fer reste silencieux.",
        "narrateur|Le chapeau de tissu coupe le dernier rayon.",
    ],
    (1, 3, 1): [
        "narrateur|Amir s'assoit un instant sur le banc.",
        "papa|Le toit est rose, tu as vu ?",
        "enfant-m|Une prune l'a peint, sans le vouloir.",
        "maman|Les autres prunes restent dans l'osier.",
        "narrateur|Une pince claque au fil, très loin.",
        "narrateur|Sous le rose, la feuille reste mouillée.",
    ],
    (1, 3, 2): [
        "narrateur|Amir touche la feuille de prune du nœud.",
        "papa|C'est ton drapeau ?",
        "enfant-m|Oui, pour dire : ici, on n'écrase pas.",
        "maman|Le panier a compris, il est sur le banc.",
        "narrateur|L'anse d'osier fait un rond d'ombre à elle.",
        "narrateur|Le torchon, noué, ne touche plus les fruits.",
    ],
    (1, 3, 3): [
        "narrateur|Amir respire près du seau, puis près du banc.",
        "papa|Deux odeurs ?",
        "enfant-m|L'eau ici, le sucre là-bas.",
        "maman|L'escargot a choisi l'eau.",
        "narrateur|Une prune mûre luit, hors de portée.",
        "narrateur|Le rideau bleu garde la terre noire.",
    ],
    (2, 1, 1): [
        "narrateur|Amir s'accroupit devant la porte de pinces.",
        "papa|On frappe, avant d'entrer ?",
        "enfant-m|On n'entre pas, c'est chez lui.",
        "maman|Tes bottes, elles, frappent le paillasson.",
        "narrateur|Deux pinces font des gardes bien droites.",
        "narrateur|Au fond du bois, rien ne bouge, et c'est bien.",
    ],
    (2, 1, 2): [
        "narrateur|Amir tire un peu la corde, pour vérifier.",
        "papa|Elle tient ?",
        "enfant-m|Elle tient, la grotte ne tombe plus.",
        "maman|Tes bottes ne pèsent plus dessus.",
        "narrateur|Le bois penche, fidèle à sa corde.",
        "narrateur|Une fraîcheur de cave reste, sous le prunier.",
    ],
    (2, 1, 3): [
        "narrateur|Amir aligne l'arrosoir, le seau, et la caisse du regard.",
        "papa|L'arrosoir, le seau, et la caisse ?",
        "enfant-m|Le seau pour entrer, la caisse pour dormir.",
        "maman|Les bottes pour tes pieds, à la porte.",
        "narrateur|Le bleu de l'entrée capte un rond de ciel.",
        "narrateur|Derrière, le bois reste nuit.",
    ],
    (2, 2, 1): [
        "narrateur|Amir écarte l'herbe à l'entrée, sans la casser.",
        "papa|Les pinces tiennent ça ?",
        "enfant-m|Oui, pas de fer dans la porte.",
        "maman|Le râteau a son mur, c'est mieux.",
        "narrateur|Un rayon s'arrête sur le seuil.",
        "narrateur|Dedans, la caisse sent l'humide et le calme.",
    ],
    (2, 2, 2): [
        "narrateur|Amir appuie sur la caisse : rien ne bascule.",
        "papa|Attachée pour de bon ?",
        "enfant-m|La corde a gagné contre le manche.",
        "maman|Le fer dort, le bois veille.",
        "narrateur|La trace du râteau sert à tenir, maintenant.",
        "narrateur|L'escargot n'entend plus le clac du fer.",
    ],
    (2, 2, 3): [
        "narrateur|Amir touche le seau calé, puis le bois.",
        "papa|Plus de trou ?",
        "enfant-m|Le bleu a bouché le courant chaud.",
        "maman|Le manche ne passera plus là.",
        "narrateur|Une dent au mur prend le rayon perdu.",
        "narrateur|Dans la double ombre, la coquille disparaît.",
    ],
    (2, 3, 1): [
        "narrateur|Amir lève le rideau de chiffon, très peu.",
        "papa|On dérange ?",
        "enfant-m|Non, je vérifie le parfum.",
        "maman|Le sucre est resté sur le banc.",
        "narrateur|Une tache violette sèche, loin de la caisse.",
        "narrateur|Derrière le chiffon, l'air est plat, sans fruit.",
    ],
    (2, 3, 2): [
        "narrateur|Amir compare les deux nœuds : bois, et rien à l'anse.",
        "papa|Tu as choisi le bois ?",
        "enfant-m|Oui, le panier n'a pas à tirer.",
        "maman|Les prunes font un tas rond, sans devoir.",
        "narrateur|L'osier du banc croise une ombre de feuille.",
        "narrateur|La grotte, nouée, ne doit rien au fruit.",
    ],
    (2, 3, 3): [
        "narrateur|Amir salue le seau qui garde, d'un petit coup.",
        "papa|Il laisse passer qui ?",
        "enfant-m|Lui, pas les prunes.",
        "maman|La confiture attendra le soir.",
        "narrateur|L'odeur sucrée s'arrête net au bleu.",
        "narrateur|Au fond de la caisse, l'humide a gagné.",
    ],
    (3, 1, 1): [
        "narrateur|Amir se penche sur le petit miroir du creux.",
        "papa|Il boit ?",
        "enfant-m|Presque, les pinces lui font un chapeau.",
        "maman|Tes bottes, elles, ne boivent plus.",
        "narrateur|Le cuir du paillasson s'éclaircit.",
        "narrateur|Sous le chapeau, le creux reste noir et froid.",
    ],
    (3, 1, 2): [
        "narrateur|Amir suit l'eau du regard : elle tourne, elle reste.",
        "papa|Plus de fuite vers la porte ?",
        "enfant-m|La corde a fermé le chemin des bottes.",
        "maman|Le cuir peut sécher.",
        "narrateur|Un petit toit de tissu tremble, très peu.",
        "narrateur|Autour de la feuille, le filet fait un collier.",
    ],
    (3, 1, 3): [
        "narrateur|Amir écoute le seau à l'envers.",
        "papa|On entend l'eau ?",
        "enfant-m|On entend l'ombre, je crois.",
        "maman|La botte, elle, n'en dit plus rien.",
        "narrateur|Le paillasson reste clair, sans flaque.",
        "narrateur|Sous le bleu, une flaque ronde s'endort.",
    ],
    (3, 2, 1): [
        "narrateur|Amir compare le cercle des pinces et la trace vide.",
        "papa|Rond contre ligne ?",
        "enfant-m|Le rond est pour lui, la ligne est finie.",
        "maman|Le râteau n'écrit plus sur l'eau.",
        "narrateur|Une dent sèche, au mur, garde un éclat.",
        "narrateur|Près de la feuille, l'eau est mate, ronde, sage.",
    ],
    (3, 2, 2): [
        "narrateur|Amir se voit, un instant, dans la mare.",
        "papa|Deux cornes aussi ?",
        "enfant-m|Oui, il est là, sous le tissu.",
        "maman|La corde a battu le fleuve du manche.",
        "narrateur|La mare se calme, sans ride.",
        "narrateur|Au mur, le fer ne pousse plus l'eau.",
    ],
    (3, 2, 3): [
        "narrateur|Amir pose l'oreille contre le seau-réservoir.",
        "papa|Ploc ?",
        "enfant-m|Ploc, il a de l'eau pour plus tard.",
        "maman|Le râteau n'en répand plus une goutte.",
        "narrateur|Une dernière goutte tombe, dedans.",
        "narrateur|Le fer du mur reste sec, et l'escargot aussi, à sa façon.",
    ],
    (3, 3, 1): [
        "narrateur|Amir tend les bras : pinces d'un côté, banc de l'autre.",
        "papa|Une frontière ?",
        "enfant-m|L'eau ici, le sucre là-bas.",
        "maman|Chacun reste chez soi.",
        "narrateur|Une prune s'immobilise au bord du banc.",
        "narrateur|Sous les pinces, la terre mouillée garde l'escargot.",
    ],
    (3, 3, 2): [
        "narrateur|Amir longe le couloir de corde, sans le toucher.",
        "papa|Ça mène où ?",
        "enfant-m|Au tronc, loin des prunes.",
        "maman|L'osier blanchit, lui, au soleil.",
        "narrateur|Le banc sent le fruit, tout entier.",
        "narrateur|Le couloir, sombre, n'en veut pas.",
    ],
    (3, 3, 3): [
        "narrateur|Amir pose une main sur le seau, une autre vers le banc.",
        "papa|Deux mondes, tu disais.",
        "enfant-m|Oui, il a choisi l'eau.",
        "maman|Les prunes se fendent, sans lui.",
        "narrateur|Une goutte chante dans le bleu, une dernière fois.",
        "narrateur|Sous le prunier, l'abri tient, et le soleil perd.",
    ],
}

END_SONS = {
    1: "paillasson,pince",
    2: "mur,metal",
    3: "prunes,banc",
}


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
        by_src["CHK_T0000_P0000"], OPENING, "opening", "prunier,goutte,pinces"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {
            "fields": {
                "option_1_label": "le torchon",
                "option_2_label": "la caisse",
                "option_3_label": "l'arrosoir",
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
                    "option_1_label": "les bottes",
                    "option_2_label": "le râteau",
                    "option_3_label": "le panier",
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
                        "option_1_label": "les pinces",
                        "option_2_label": "la corde",
                        "option_3_label": "le seau",
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
                    {"emphasis": T3_EMPH[c]},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = (
        "Amir veut un abri pour l'escargot sous le prunier, avant que le soleil "
        "mange l'ombre. Son tas de jouets s'écroule. Il prend le torchon, la caisse "
        "ou l'arrosoir ; il remet bottes, râteau ou panier à leur place ; il finit "
        "l'abri avec les pinces, la corde ou le seau. Vingt-sept toits distincts."
    )
    story["title"] = "L'escargot sous le prunier"
    story["characters"] = "Amir, papa, maman"
    story["setting"] = "jardin, prunier, fil à linge, caisse, arrosoir"
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
        "# TREE-AUT-034 — L'escargot sous le prunier\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Public :** N2 (3–6 ans), audio familial\n"
        "- **Leçon :** AUT.RAN.001 — ranger, vécue (l'ombre ne tient qu'une fois les affaires à leur place)\n"
        "- **Personnages :** Amir, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "## Vécu\n\n"
        "Jardin, prunier, fil à linge, pinces, caisse, arrosoir. Désir : un abri pour "
        "l'escargot avant que le soleil mange l'ombre. Première idée : le tas de la caisse. "
        "Ça s'écroule, un cube roule, l'escargot rentre. Enquête **autre** que TREE-COL-015 :\n\n"
        "- T1 matériau : le torchon / la caisse / l'arrosoir\n"
        "- T2 bazar à remettre : les bottes / le râteau / le panier\n"
        "- T3 forme de l'abri : les pinces / la corde / le seau\n\n"
        "Pas de trace d'argent, pas de loupe, pas de carnet, pas de dîner. "
        "Q = torchon / caisse / eau. Merci vécu au moment où l'objet reprend sa place.\n\n"
        "## Vu et corrigé\n\n"
        "- Kenzo absent (D16 : Amir). T1/T2/T3 changés (plus cuisine / cubes / matin).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Vocabulaire 3–6 (sas, sentinelle, auvent, etc. simplifiés).\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration), `style_energy`, "
        "pauses, pitch, volume. `slow` = choix, indice, fin.\n"
        "- 27 toits, 27 dernières images. Ouverture + 3 L1 + 9 L2 + 27 L3/fins relus.\n"
        "- `check()` N2≤15, ~502–540 mots/chemin. Pas apply.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
