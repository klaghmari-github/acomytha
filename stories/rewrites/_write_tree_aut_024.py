#!/usr/bin/env python3
"""TREE-AUT-024 — F-NAR-019. Canard sous la caisse. TTS complet. Pas d'apply."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-024"
N2 = 15
TICS = ("tout doux", "tout calme", "tout lent", " encore ", " déjà ", "aujourd'hui,")

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "canard",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=l_eau tiède attend le bec; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": (
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton choix change la recherche; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=regarde_le_geste; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; "
            "destinataire=enfant; sous_texte=le_canard_n_est_pas_fini; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": (
            "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; "
            "destinataire=enfant; sous_texte=trop_vite_le_tas_gagne; tempo=vif; "
            "sourire=léger; respiration=courte"
        ),
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=le_jouet_vole_la_place_du_bec; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_canard_revient_quand_la_caisse_a_sa_place; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": (
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_eau_et_la_tarte_ont_tenu_promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
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
        low = f" {ph.lower()} "
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        if tok and tok == prev:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {tok}: {ph}")
        else:
            run = 1
        prev = tok
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
    "narrateur|Dans le village, le zinc du toit fait tic.",
    "narrateur|Une goutte frappe la tôle, puis s'arrête.",
    "narrateur|La cuisine sent la tarte aux pommes.",
    "narrateur|Sur la table, la nappe à carreaux racle les genoux.",
    "narrateur|Sous le bois, une caisse déborde de jouets.",
    "narrateur|Près du sel, un bol d'eau fume.",
    "papa|Les pommes sont tièdes, Sarah.",
    "maman|On sort la tarte dans un moment.",
    "narrateur|Mila aligne des cubes au bord de la nappe.",
    "copine|Ma tour reste là.",
    "copine|Je joue.",
    "enfant-f|Moi, je veux le canard, maintenant !",
    "narrateur|En ce moment, Sarah tire la caisse d'un coup.",
    "narrateur|Cubes, livre, tasses : tout tombe sur le carrelage.",
    "narrateur|Elle fouille le tas, trop vite.",
    "enfant-f|Mon canard jaune !",
    "enfant-f|Il n'est pas là.",
    "papa|Il était dans la caisse, non ?",
    "narrateur|Sarah écarte un cube, puis le livre.",
    "narrateur|Rien de jaune.",
    "narrateur|Ses épaules baissent.",
    "maman|Tu as regardé sous le tas ?",
    "enfant-f|C'est trop haut.",
    "enfant-f|Je ne vois rien.",
    "copine|Ne casse pas ma tour, Sarah.",
    "narrateur|Le bol fume moins.",
    "narrateur|L'eau refroidit.",
    "papa|Par où commences-tu, pour le retrouver ?",
]

T1_CHOICE = [
    "narrateur|Sarah peut soulever la nappe, fouiller le tas, ou regarder près du bol.",
    "maman|Que choisis-tu d'abord ?",
]

T1 = {
    1: {
        "lab": "la nappe",
        "sons": "nappe,farine",
        "emphasis": "nappe",
        "passage": [
            "narrateur|Sarah soulève la nappe à carreaux d'un bord.",
            "narrateur|Un nuage de farine tombe sur les cubes de Mila.",
            "copine|Ma tour est blanche !",
            "enfant-f|Le canard est dessous, vite.",
            "narrateur|Elle plonge la tête sous le tissu.",
            "narrateur|Le carrelage est froid, et vide.",
            "enfant-f|Rien.",
            "narrateur|Le tissu retombe sur ses cheveux.",
            "papa|La farine a caché autre chose, non ?",
            "maman|Mila, ta tour a pris la poussière.",
            "narrateur|Sarah reste accroupie, les poings serrés.",
            "copine|Tu as tout mélangé.",
        ],
        "question": [
            "narrateur|Qu'est-ce que Sarah a soulevé d'un bord ?",
        ],
        "qfields": {
            "expected_answer": "nappe",
            "accepted_examples": "nappe | la nappe | nappe à carreaux | le tissu",
            "retry_prompt": "Écoute l'indice, et réessaie.",
        },
        "confirm": [
            "enfant-f|La nappe !",
            "narrateur|Oui, la nappe à carreaux.",
            "narrateur|Sarah la relève d'un coin, plus lentement.",
            "papa|Le tissu peut aider, plus tard.",
            "maman|Dessous, le sol est trop plein.",
            "narrateur|Un grain de farine brille sur un cube rouge.",
        ],
    },
    2: {
        "lab": "le tas",
        "sons": "jouets,carrelage",
        "emphasis": "tas",
        "passage": [
            "narrateur|Sarah plonge les deux mains dans le tas.",
            "narrateur|Une tasse roule jusqu'au pied de papa.",
            "copine|Tu casses tout !",
            "enfant-f|Il est au fond, je le sais.",
            "narrateur|Elle creuse.",
            "narrateur|Le tas devient plus haut, plus large.",
            "narrateur|Un cube tape le bol, tout près.",
            "papa|Attention à l'eau, Sarah.",
            "enfant-f|Je n'arrive pas.",
            "narrateur|Ses mains s'arrêtent, collées de farine.",
            "maman|Le bec se cache plus bas, peut-être.",
            "copine|Ma tour, elle, n'existe plus.",
        ],
        "question": [
            "narrateur|Où Sarah a-t-elle plongé les deux mains ?",
        ],
        "qfields": {
            "expected_answer": "tas",
            "accepted_examples": "tas | le tas | dans le tas | le tas de jouets",
            "retry_prompt": "Écoute l'indice, et réessaie.",
        },
        "confirm": [
            "enfant-f|Dans le tas !",
            "narrateur|Oui, dans le tas tombé de la caisse.",
            "narrateur|Sarah essuie ses paumes à la nappe.",
            "papa|Creuser plus fort n'a pas suffi.",
            "maman|Il manque une place, au milieu.",
            "narrateur|La tasse arrêtée près du pied ne bouge plus.",
        ],
    },
    3: {
        "lab": "le bol",
        "sons": "bol,eau",
        "emphasis": "bol",
        "passage": [
            "narrateur|Sarah se tourne vers le bol qui fume.",
            "copine|Moi, je veux l'eau pour le thé.",
            "enfant-f|Non, c'est le bain du canard.",
            "narrateur|Elle pousse le bol pour voir dessous.",
            "narrateur|L'eau danse, trop près du bord.",
            "papa|J'attrape !",
            "narrateur|Papa recule le bol d'une main.",
            "enfant-f|Il n'est pas là non plus.",
            "maman|L'eau n'est plus si chaude, tu sens ?",
            "narrateur|Sarah pose le front contre le bois de la table.",
            "copine|Alors on partage le bol ?",
            "narrateur|Une ride d'eau s'endort, sans bec jaune.",
        ],
        "question": [
            "narrateur|Près de quoi Sarah a-t-elle cherché le canard ?",
        ],
        "qfields": {
            "expected_answer": "bol",
            "accepted_examples": "bol | le bol | bol d'eau | l'eau | eau",
            "retry_prompt": "Écoute l'indice, et réessaie.",
        },
        "confirm": [
            "enfant-f|Le bol !",
            "narrateur|Oui, le bol d'eau, près du sel.",
            "narrateur|Papa l'a sauvé, de justesse.",
            "maman|Le canard n'était pas collé au fond.",
            "papa|L'eau l'attend, si on trouve le bec.",
            "narrateur|Une petite vapeur quitte le bord, lente.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Sous la nappe, un jouet vole la place du bec.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Que remets-tu dans la caisse ?",
    ],
    2: [
        "narrateur|Dans le tas, un jouet pèse trop.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Que remets-tu dans la caisse ?",
    ],
    3: [
        "narrateur|Près du bol, un jouet barre le sol.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Que remets-tu dans la caisse ?",
    ],
}

T2 = {
    (1, 1): {
        "lab": "les cubes",
        "sons": "cubes,bois",
        "emphasis": "cubes",
        "passage": [
            "narrateur|Sous la nappe, les cubes de Mila forment un mur.",
            "copine|Laisse ma tour !",
            "enfant-f|Je ne vois plus le sol.",
            "narrateur|Sarah veut écarter le rouge d'un coup.",
            "narrateur|La pile penche vers le bol.",
            "papa|Un par un, peut-être ?",
            "narrateur|Elle pose le rouge dans la caisse.",
            "narrateur|Puis le bleu.",
            "maman|Merci, Sarah, ils ont une place.",
            "copine|Ma tour, elle, attendra.",
            "narrateur|Un trou s'ouvre sous le tissu.",
            "enfant-f|Un peu d'air, enfin.",
        ],
    },
    (1, 2): {
        "lab": "le livre",
        "sons": "livre,page",
        "emphasis": "livre",
        "passage": [
            "narrateur|Le livre est collé sous la nappe, plat.",
            "narrateur|Une page a pris de la farine.",
            "enfant-f|Il cache tout le milieu.",
            "copine|C'est mon bateau, dans l'image.",
            "narrateur|Sarah tire le livre trop vite.",
            "narrateur|La nappe se plisse et masque plus fort.",
            "papa|Glisse-le vers la caisse, sans le froisser.",
            "narrateur|Elle le pousse, page contre bois.",
            "maman|Merci, les pages ont leur abri.",
            "narrateur|Sous l'ancienne place, le carrelage apparaît.",
            "enfant-f|Le bateau n'était pas un bec.",
        ],
    },
    (1, 3): {
        "lab": "la dînette",
        "sons": "tasse,porcelaine",
        "emphasis": "dînette",
        "passage": [
            "narrateur|Sous la nappe, les tasses de Mila font un dîner.",
            "copine|C'est ma tarte à moi.",
            "enfant-f|Elle n'est pas vraie, ta tarte.",
            "narrateur|Sarah veut tout ramasser d'un geste.",
            "narrateur|Une assiette jouet glisse sous le tissu.",
            "papa|Les tasses, dans la caisse ?",
            "narrateur|Sarah les rassemble, une, puis l'autre.",
            "maman|Merci, le dîner a un tiroir, maintenant.",
            "copine|Je rejouerai, après.",
            "narrateur|Le tissu retombe sur un sol plus nu.",
            "enfant-f|Plus de tarte jouet au milieu.",
        ],
    },
    (2, 1): {
        "lab": "les cubes",
        "sons": "cubes,tas",
        "emphasis": "cubes",
        "passage": [
            "narrateur|Au milieu du tas, les cubes font une colline.",
            "copine|Ma tour est devenue un tas.",
            "enfant-f|Je n'arrive pas à creuser.",
            "narrateur|Sarah soulève trois cubes à la fois.",
            "narrateur|Ils lui échappent, et rebondissent.",
            "papa|La caisse les reprend, un cube après l'autre.",
            "narrateur|Elle s'arrête, respire, puis recommence.",
            "narrateur|Rouge, bleu, jaune : chacun trouve le bois.",
            "maman|Merci, la colline baisse.",
            "copine|Ils sont plus sages, là-dedans.",
            "narrateur|Un creux s'ouvre au centre du tas.",
        ],
    },
    (2, 2): {
        "lab": "le livre",
        "sons": "livre,tas",
        "emphasis": "livre",
        "passage": [
            "narrateur|Le livre sert de toit au tas, trop lourd.",
            "enfant-f|Je l'ai pris pour creuser.",
            "narrateur|Les pages se plient, collées de farine.",
            "copine|Mon bateau va se casser !",
            "papa|Le livre n'est pas une pelle.",
            "narrateur|Sarah le pose à plat dans la caisse.",
            "narrateur|Les pages se déplient, un peu.",
            "maman|Merci, il n'écrase plus les autres.",
            "narrateur|Sans le toit, le tas s'affaisse.",
            "enfant-f|Je vois un trou, au fond.",
        ],
    },
    (2, 3): {
        "lab": "la dînette",
        "sons": "tasse,roule",
        "emphasis": "dînette",
        "passage": [
            "narrateur|Dans le tas, les tasses s'accrochent partout.",
            "narrateur|Sarah en dégage une, trop vite.",
            "narrateur|Elle roule sous la chaise de maman.",
            "copine|Ramène-la !",
            "enfant-f|J'en ai marre.",
            "papa|La caisse les attend, toutes.",
            "narrateur|Sarah rampe, reprend la tasse, la pose dedans.",
            "narrateur|Puis l'assiette, puis la petite casserole.",
            "maman|Merci, plus rien ne roule.",
            "copine|Mon dîner a un coffre, alors.",
            "narrateur|Le tas perd ses bords, enfin.",
        ],
    },
    (3, 1): {
        "lab": "les cubes",
        "sons": "cubes,bol",
        "emphasis": "cubes",
        "passage": [
            "narrateur|Près du bol, les cubes font une barrière.",
            "copine|C'est mon mur, pour le thé.",
            "enfant-f|Il barre le chemin du canard.",
            "narrateur|Sarah veut pousser le mur d'un coup.",
            "narrateur|Le cube du haut frôle l'eau.",
            "papa|Loin du bol, dans la caisse.",
            "narrateur|Elle porte le rouge, puis le bleu, à deux mains.",
            "maman|Merci, l'eau ne tremble plus.",
            "copine|Mon mur habite le bois, d'accord.",
            "narrateur|Un passage s'ouvre entre le bol et la table.",
            "enfant-f|Je peux m'accroupir, là.",
        ],
    },
    (3, 2): {
        "lab": "le livre",
        "sons": "livre,eau",
        "emphasis": "livre",
        "passage": [
            "narrateur|Le livre est coincé contre le bol, penché.",
            "narrateur|Une page touche presque l'eau.",
            "enfant-f|Il va boire, le bateau !",
            "copine|Sèche-le !",
            "papa|Le bois de la caisse est plus sûr.",
            "narrateur|Sarah soulève le livre à deux mains.",
            "narrateur|Elle le glisse à plat, loin du bol.",
            "maman|Merci, les pages restent sèches.",
            "narrateur|Sans le livre, le pied du bol est libre.",
            "enfant-f|Je vois le carrelage, tout autour.",
        ],
    },
    (3, 3): {
        "lab": "la dînette",
        "sons": "tasse,bol",
        "emphasis": "dînette",
        "passage": [
            "narrateur|Les tasses de Mila cernent le bol, comme des invitées.",
            "copine|C'est mon goûter.",
            "enfant-f|Le canard n'a plus de place.",
            "narrateur|Sarah veut tout chasser d'un balayage.",
            "narrateur|Une tasse cogne le bol : clac.",
            "papa|Une tasse, puis l'autre, vers la caisse.",
            "narrateur|Sarah obéit, les dents serrées.",
            "maman|Merci, le bol a de l'air.",
            "copine|Mon goûter ira dans le bois, alors.",
            "narrateur|Autour de l'eau, le sol redevient rond, vide.",
            "enfant-f|Plus d'invitées.",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Les cubes ont quitté le milieu.",
        "papa|Un par un, le couvercle, ou le coin ?",
        "maman|Comment finir, pour le bec ?",
    ],
    2: [
        "narrateur|Le livre a quitté le milieu.",
        "papa|Un par un, le couvercle, ou le coin ?",
        "maman|Comment finir, pour le bec ?",
    ],
    3: [
        "narrateur|Les tasses ont quitté le milieu.",
        "papa|Un par un, le couvercle, ou le coin ?",
        "maman|Comment finir, pour le bec ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "narrateur|Sarah prend les derniers cubes, un par un.",
        "narrateur|Le rouge, le bleu, le petit jaune.",
        "narrateur|Sous le dernier, un bec apparaît, coincé.",
        "enfant-f|Toi !",
        "narrateur|Elle le soulève, collé de farine.",
        "papa|Il attendait le dernier cube.",
        "maman|Mila, ta tour a laissé le passage.",
        "narrateur|Sarah le pose dans l'eau, tout droit.",
        "narrateur|Le canard fait une ride ronde.",
    ],
    (1, 1, 2): [
        "narrateur|Sarah prend le couvercle de la caisse.",
        "narrateur|Elle y pose les cubes restants, comme un plateau.",
        "narrateur|En le soulevant, un jaune colle au dessous.",
        "enfant-f|Il était sous le bois !",
        "copine|Le couvercle l'avait gardé.",
        "papa|Tu as trouvé son toit, sans le chercher.",
        "narrateur|Elle détache le canard, le glisse dans le bol.",
        "narrateur|Les cubes glissent dans la caisse, d'un coup.",
        "narrateur|L'eau accueille le bec, sans éclaboussure.",
    ],
    (1, 1, 3): [
        "narrateur|Sarah vide un coin de la caisse, d'abord.",
        "narrateur|Elle y pousse les cubes, bien serrés.",
        "narrateur|Au fond du coin, un jaune est coincé dans le bois.",
        "enfant-f|Il s'était caché dans l'angle !",
        "maman|L'angle est un bon abri, trop bon.",
        "papa|Maintenant, il a le bol.",
        "narrateur|Sarah souffle la farine du dos du canard.",
        "narrateur|Elle le pose dans l'eau, près du sel.",
        "narrateur|Un grain de farine dort au coin vide.",
    ],
    (1, 2, 1): [
        "narrateur|Sarah glisse le livre, puis les miettes, une à une.",
        "narrateur|Une miette de pomme, un grain, une page pliée.",
        "narrateur|Sous la dernière miette, le bec jaune.",
        "enfant-f|Il avait un goûter, lui aussi.",
        "papa|La page ne l'écrase plus.",
        "maman|Les miettes ont leur place, à part.",
        "narrateur|Sarah rince le canard d'un doigt d'eau.",
        "narrateur|Elle le pose dans le bol, propre.",
        "narrateur|Une page du livre garde une tache de farine.",
    ],
    (1, 2, 2): [
        "narrateur|Sarah pose le livre sur le couvercle.",
        "narrateur|Elle le porte, plat, jusqu'à la caisse.",
        "narrateur|En basculant le bois, le canard tombe du rebord.",
        "enfant-f|Il voyageait sous le bateau !",
        "copine|Mon bateau l'a conduit.",
        "papa|Le plateau a tout ramené.",
        "narrateur|Sarah rit, un peu, puis le baigne.",
        "narrateur|Le livre se couche, sage, dans le bois.",
        "narrateur|Le couvercle porte une miette de pomme, collée.",
    ],
    (1, 2, 3): [
        "narrateur|Sarah ouvre un coin de caisse, étroit.",
        "narrateur|Elle y glisse le livre, droit comme un mur.",
        "narrateur|Derrière le dos du livre, le canard était plié.",
        "enfant-f|Il faisait le signet !",
        "maman|Un drôle de signet, tout jaune.",
        "papa|Le coin l'a rendu.",
        "narrateur|Elle le déplie, le pose dans l'eau.",
        "narrateur|Les pages se ferment, sans lui.",
        "narrateur|Le coin de la caisse tient le livre, droit.",
    ],
    (1, 3, 1): [
        "narrateur|Sarah range les tasses, une par une.",
        "narrateur|Petite, moyenne, puis celle à l'envers.",
        "narrateur|Sous celle à l'envers, le bec jaillit.",
        "enfant-f|Il était le gâteau !",
        "copine|C'était ma tarte, pardon.",
        "papa|Il a joué au gâteau, assez longtemps.",
        "narrateur|Sarah le libère, le baigne.",
        "narrateur|Les tasses s'empilent, dans le bois.",
        "narrateur|Une tasse vide attend, près du bol vrai.",
    ],
    (1, 3, 2): [
        "narrateur|Sarah sert les tasses sur le couvercle.",
        "narrateur|Ça cliquette, comme un vrai plateau.",
        "narrateur|Au centre, coincé, le canard fait le plat.",
        "enfant-f|On l'a servi par erreur !",
        "maman|Le plat d'honneur, c'est lui.",
        "papa|Vers l'eau, maintenant.",
        "narrateur|Elle le descend dans le bol, solennelle.",
        "narrateur|Les tasses glissent dans la caisse.",
        "narrateur|Le couvercle cliquette, puis se tait.",
    ],
    (1, 3, 3): [
        "narrateur|Sarah dégage le coin gauche de la caisse.",
        "narrateur|Elle y glisse assiette, casserole, tasse.",
        "narrateur|Dans l'angle, une petite assiette cachait le jaune.",
        "enfant-f|Son assiette à lui !",
        "copine|Je lui en prête une, alors.",
        "maman|Il a mieux : le bol.",
        "narrateur|Sarah le pose dans l'eau, fier.",
        "narrateur|Le coin brille, avec l'assiette jouet.",
        "narrateur|Au coin, une petite assiette jouet brille.",
    ],
    (2, 1, 1): [
        "narrateur|Sarah finit la colline, cube après cube.",
        "narrateur|Le dernier est collé au carrelage, lourd.",
        "narrateur|Elle le lève : le canard était dessous, plat.",
        "enfant-f|Il étouffait !",
        "papa|Le dernier cube pesait trop.",
        "maman|Un par un, tu as allégé.",
        "narrateur|Sarah le plonge, et l'eau le redresse.",
        "narrateur|Les cubes, dans la caisse, ne pèsent plus.",
        "narrateur|Au fond du bol, une ride rejoint le bec.",
    ],
    (2, 1, 2): [
        "narrateur|Sarah racle les cubes restants sur le couvercle.",
        "narrateur|Elle bascule le plateau au-dessus de la caisse.",
        "narrateur|Un jaune reste collé au bois du couvercle.",
        "enfant-f|Il s'est accroché !",
        "copine|Le plateau l'a pêché.",
        "papa|Sans le tas, il n'avait plus d'accroche.",
        "narrateur|Elle le décolle, le baigne.",
        "narrateur|Les cubes tombent en pluie douce, dans le bois.",
        "narrateur|Le zinc, dehors, répond d'un tic.",
    ],
    (2, 1, 3): [
        "narrateur|Sarah pousse les cubes vers un coin de caisse.",
        "narrateur|Elle les tasse, pour libérer le milieu.",
        "narrateur|Au milieu, collé au fond, le canard.",
        "enfant-f|Le cœur du tas, c'était lui.",
        "maman|Le coin a pris les cubes, lui le centre.",
        "papa|Chacun sa place.",
        "narrateur|Elle le lève, le pose dans l'eau tiède.",
        "narrateur|La colline n'existe plus.",
        "narrateur|Au centre du carrelage, un rond propre.",
    ],
    (2, 2, 1): [
        "narrateur|Sarah ôte les derniers papiers, un par un.",
        "narrateur|Une page, un coin plié, un grain de farine.",
        "narrateur|Sous le grain, le bec, poudreux.",
        "enfant-f|Il a lu, lui aussi.",
        "papa|Le livre n'est plus un toit.",
        "maman|Les pages, une à une, l'ont rendu.",
        "narrateur|Sarah souffle, puis le baigne.",
        "narrateur|Le livre se ferme, dans la caisse.",
        "narrateur|Une page du livre garde un grain, tout seul.",
    ],
    (2, 2, 2): [
        "narrateur|Sarah sert le livre sur le couvercle, comme un plateau.",
        "narrateur|Elle le porte, et le tas s'ouvre dessous.",
        "narrateur|Le canard était calé sous la tranche.",
        "enfant-f|La tranche l'avait coincé.",
        "copine|Mon bateau faisait le pont.",
        "papa|Le plateau a levé le pont.",
        "narrateur|Sarah le glisse dans l'eau, soulagée.",
        "narrateur|Le livre rejoint le bois, sans plier.",
        "narrateur|Le couvercle sent la farine, un instant.",
    ],
    (2, 2, 3): [
        "narrateur|Sarah glisse le livre dans le coin droit.",
        "narrateur|La tranche racle le bois, puis s'arrête.",
        "narrateur|Derrière, dans l'ombre du coin, le jaune.",
        "enfant-f|Il faisait le garde !",
        "maman|Un garde trop caché.",
        "papa|Le coin l'a montré.",
        "narrateur|Elle le sort, le pose dans le bol.",
        "narrateur|Le livre tient le coin, comme un mur.",
        "narrateur|L'ombre du coin n'a plus de bec.",
    ],
    (2, 3, 1): [
        "narrateur|Sarah ramasse les dernières tasses, une par une.",
        "narrateur|Celle de la chaise, celle du tas, celle du pied.",
        "narrateur|Sous le pied de papa, le canard était logé.",
        "enfant-f|Il s'était sauvé !",
        "papa|J'ai failli le marcher.",
        "maman|Une par une, tu as tout vu.",
        "narrateur|Sarah le sauve, le baigne, les yeux grands.",
        "narrateur|Les tasses s'empilent, sans rouler.",
        "narrateur|Près du pied de papa, le carrelage est nu.",
    ],
    (2, 3, 2): [
        "narrateur|Sarah fait un plateau de tasses sur le couvercle.",
        "narrateur|Elle marche, prudente, vers la caisse.",
        "narrateur|Une tasse bascule : dessous, le canard.",
        "enfant-f|Il faisait le soucoupe !",
        "copine|Le plus petit plat, c'était lui.",
        "papa|Le plateau a tout révélé.",
        "narrateur|Elle le pose dans l'eau, tout heureuse.",
        "narrateur|Les tasses descendent, sans un roulement.",
        "narrateur|Le couvercle garde un cercle d'eau, minuscule.",
    ],
    (2, 3, 3): [
        "narrateur|Sarah range les tasses dans le coin le plus sombre.",
        "narrateur|Elle les cale, pour qu'elles ne partent plus.",
        "narrateur|Au fond du coin, coincé, le jaune.",
        "enfant-f|Il s'était mis à l'ombre.",
        "maman|L'ombre du bois, pas celle du tas.",
        "papa|Le coin l'a rendu, au calme.",
        "narrateur|Sarah le sort, le baigne.",
        "narrateur|Les tasses tiennent, serrées.",
        "narrateur|Le coin sombre a perdu son secret.",
    ],
    (3, 1, 1): [
        "narrateur|Sarah porte les derniers cubes, un par un, loin du bol.",
        "narrateur|Le rouge, le bleu, le plus petit.",
        "narrateur|Sous le plus petit, collé au pied du bol, le bec.",
        "enfant-f|Il se chauffait !",
        "papa|Près de l'eau, sans y entrer.",
        "maman|Un par un, tu as vu le pied.",
        "narrateur|Sarah le glisse par-dessus le bord, dans l'eau.",
        "narrateur|Les cubes, dans la caisse, ne menacent plus.",
        "narrateur|Une vapeur mince entoure le canard, enfin.",
    ],
    (3, 1, 2): [
        "narrateur|Sarah charge les cubes sur le couvercle.",
        "narrateur|Elle contourne le bol, sans le frôler.",
        "narrateur|Un cube manque : il cachait le canard, contre le sel.",
        "enfant-f|À côté du sel !",
        "copine|Ton bain, pas mon thé.",
        "papa|Le plateau a fait le détour.",
        "narrateur|Elle le pose dans l'eau, et Mila recule.",
        "narrateur|Les cubes rejoignent le bois, loin du bol.",
        "narrateur|Le sel a un voisin jaune, qui nage.",
    ],
    (3, 1, 3): [
        "narrateur|Sarah pousse les cubes dans le coin opposé au bol.",
        "narrateur|Loin de l'eau, serrés.",
        "narrateur|Entre le bol et ce coin, le canard, oublié.",
        "enfant-f|Le passage, c'était lui.",
        "maman|Le coin a pris le mur, lui le chemin.",
        "papa|L'eau l'attendait, juste là.",
        "narrateur|Sarah le lève, le pose, et l'eau l'accepte.",
        "narrateur|Les cubes, au loin, ne font plus barrière.",
        "narrateur|Entre le bol et le bois, plus rien ne barre.",
    ],
    (3, 2, 1): [
        "narrateur|Sarah essuie la page mouillée, puis la suivante.",
        "narrateur|Une, puis l'autre, loin du bol.",
        "narrateur|Entre deux pages, plat, le canard.",
        "enfant-f|Il s'était mis dans le livre !",
        "papa|Un signet trop gros.",
        "maman|Page après page, tu l'as vu.",
        "narrateur|Elle le sort, le plonge, riant.",
        "narrateur|Le livre, sec, rejoint la caisse.",
        "narrateur|Une page reste un peu ondulée, près de l'eau.",
    ],
    (3, 2, 2): [
        "narrateur|Sarah pose le livre sur le couvercle, loin du bol.",
        "narrateur|Elle le porte comme un plateau de papier.",
        "narrateur|Du rebord du bol, le canard tombe sur le bois.",
        "enfant-f|Il s'accrochait au bol !",
        "copine|Il voulait l'eau, sans le tas.",
        "papa|Le plateau l'a décroché.",
        "narrateur|Sarah le met dans l'eau, d'un geste sûr.",
        "narrateur|Le livre se couche, sec, dans la caisse.",
        "narrateur|Le couvercle a une goutte, qu'elle essuie.",
    ],
    (3, 2, 3): [
        "narrateur|Sarah glisse le livre dans le coin le plus sec.",
        "narrateur|Loin de la vapeur du bol.",
        "narrateur|Sous le pied du bol, libéré, le canard.",
        "enfant-f|Le livre le pressait contre l'eau.",
        "maman|Le coin sec a pris le papier.",
        "papa|Le pied du bol a rendu le jaune.",
        "narrateur|Sarah le baigne, enfin.",
        "narrateur|Le livre, au sec, ne boit plus.",
        "narrateur|Sous le pied du bol, le carrelage luit.",
    ],
    (3, 3, 1): [
        "narrateur|Sarah écarte les tasses, une par une, du bol.",
        "narrateur|Invitée, invitée, puis la dernière.",
        "narrateur|La dernière cachait le canard, bec dans l'eau.",
        "enfant-f|Il buvait en cachette !",
        "copine|C'était mon invité, alors.",
        "papa|Un par un, tu as vu l'invité.",
        "narrateur|Sarah le laisse dans le bol, cette fois pour de vrai.",
        "narrateur|Les tasses rentrent, sans cérémonie.",
        "narrateur|Autour du bol, plus d'assiette jouet.",
    ],
    (3, 3, 2): [
        "narrateur|Sarah charge les tasses sur le couvercle.",
        "narrateur|Elle tourne autour du bol, lente.",
        "narrateur|Au centre du plateau, le canard faisait le gâteau.",
        "enfant-f|On l'a servi deux fois.",
        "maman|Le vrai plat, c'est l'eau.",
        "papa|Le plateau a fini le goûter.",
        "narrateur|Elle le descend dans le bol, et Mila applaudit.",
        "narrateur|Les tasses trouvent la caisse.",
        "narrateur|Le couvercle sent le goûter, plus le canard.",
    ],
    (3, 3, 3): [
        "narrateur|Sarah pousse les tasses dans le coin loin du bol.",
        "narrateur|Le goûter a un camp, l'eau un autre.",
        "narrateur|Entre les deux, oublié, le canard.",
        "enfant-f|Deux mondes, et lui au milieu.",
        "copine|Le mien, le tien.",
        "papa|Le coin a tranché.",
        "narrateur|Sarah le pose dans l'eau, et Mila garde les tasses.",
        "narrateur|Chacun son camp, chacun son jeu.",
        "narrateur|Entre le coin et le bol, le carrelage est un chemin.",
    ],
}

# Last T3 lines that duplicated: (1,3,3) has two similar. I'll uniquify in ENDINGS.

T3_SONS = {1: "caisse,canard", 2: "couvercle,bois", 3: "coin,bois"}
T3_EMPH = {1: "canard", 2: "couvercle", 3: "coin"}
T3_LAB = {1: "un par un", 2: "le couvercle", 3: "le coin"}
T2_LAB = {1: "les cubes", 2: "le livre", 3: "la dînette"}
T1_LAB = {1: "la nappe", 2: "le tas", 3: "le bol"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Sarah s'assoit, les genoux farineux.",
        "papa|Qui a trouvé le dernier cube ?",
        "enfant-f|Moi, et le bec était dessous.",
        "maman|Mila, ta tour a laissé le passage.",
        "narrateur|Dehors, le zinc fait tic, une fois.",
        "narrateur|Dans le bol, le canard pousse une ride d'eau.",
    ],
    (1, 1, 2): [
        "narrateur|Sarah pose le couvercle, à côté de la caisse.",
        "papa|Il s'était collé où ?",
        "enfant-f|Sous le bois, comme un aimant.",
        "maman|Les cubes, eux, ont glissé d'un coup.",
        "narrateur|La tarte sent chaud, tout près.",
        "narrateur|Le zinc fait tic, et le canard répond d'un ploc.",
    ],
    (1, 1, 3): [
        "narrateur|Sarah touche l'angle de la caisse, vide maintenant.",
        "papa|L'angle est trop bon, parfois.",
        "enfant-f|Il s'y était coincé, avec la farine.",
        "maman|Le bol, lui, n'a pas d'angle.",
        "narrateur|Un grain de farine dort au coin du bois.",
        "narrateur|Une miette de tarte brille au bord du bol.",
    ],
    (1, 2, 1): [
        "narrateur|Sarah essuie la miette de pomme, du doigt.",
        "papa|C'était son goûter ?",
        "enfant-f|Un vrai, collé sous la page.",
        "maman|La nappe a rendu le milieu.",
        "narrateur|La nappe à carreaux retombe, lente.",
        "narrateur|L'eau tremble, et le bec jaune brille.",
    ],
    (1, 2, 2): [
        "narrateur|Sarah referme le couvercle, sans le canard.",
        "papa|Le bateau l'avait conduit ?",
        "enfant-f|Jusqu'au plateau, puis jusqu'à l'eau.",
        "maman|Le livre a fini son voyage.",
        "narrateur|Une image de bateau reste dans le bois.",
        "narrateur|La tarte sent chaud, et le bec jaune nage.",
    ],
    (1, 2, 3): [
        "narrateur|Sarah caresse le dos du livre, droit dans le coin.",
        "papa|Un signet trop vivant, non ?",
        "enfant-f|Il faisait le signet, tout jaune.",
        "maman|Les pages se ferment, sans lui.",
        "narrateur|Sous la table, le carrelage redevient visible.",
        "narrateur|Dans l'eau, le canard se redresse, fier.",
    ],
    (1, 3, 1): [
        "narrateur|Sarah aligne la petite tasse, près de la caisse.",
        "papa|C'était le gâteau, tu disais.",
        "enfant-f|Oui, et je l'ai libéré.",
        "maman|Mila rejouera, plus tard.",
        "narrateur|Une tasse vide attend, loin du bol vrai.",
        "narrateur|Le canard, lui, a l'eau, pas l'assiette.",
    ],
    (1, 3, 2): [
        "narrateur|Sarah écoute le silence du couvercle.",
        "papa|Plus de cliquetis ?",
        "enfant-f|Le plat d'honneur est dans l'eau.",
        "maman|Les tasses se taisent, dans le bois.",
        "narrateur|Le couvercle reste muet, posé de travers.",
        "narrateur|Une ride d'eau entoure le bec, comme une nappe.",
    ],
    (1, 3, 3): [
        "narrateur|Sarah montre à Mila le coin de l'assiette jouet.",
        "papa|Son assiette à lui, tu disais.",
        "enfant-f|Il a mieux, maintenant.",
        "maman|Le bol est plus grand, et plus vrai.",
        "narrateur|Au coin, l'assiette jouet capte un carré de nappe.",
        "narrateur|Dans le bol, le jaune nage sans assiette.",
    ],
    (2, 1, 1): [
        "narrateur|Sarah se lave les doigts au bord du bol.",
        "papa|Le dernier cube pesait trop ?",
        "enfant-f|Oui, il l'écrasait, plat.",
        "maman|Un par un, la colline a fondu.",
        "narrateur|Les cubes, dans la caisse, ne pèsent plus.",
        "narrateur|Au fond du bol, une ride rejoint le bec.",
    ],
    (2, 1, 2): [
        "narrateur|Sarah lève les yeux vers le toit.",
        "papa|Le zinc a parlé ?",
        "enfant-f|Il a dit tic, et mon canard a dit ploc.",
        "maman|Le plateau a pêché le jaune.",
        "narrateur|Une goutte, dehors, frappe la tôle.",
        "narrateur|Dedans, le canard répond, dans l'eau tiède.",
    ],
    (2, 1, 3): [
        "narrateur|Sarah pose la paume au centre du carrelage.",
        "papa|Le cœur du tas, c'était lui.",
        "enfant-f|Oui, coincé au milieu.",
        "maman|Le coin a pris les cubes, lui le centre.",
        "narrateur|Au centre du carrelage, un rond propre.",
        "narrateur|Le bol, à côté, tient le jaune au chaud.",
    ],
    (2, 2, 1): [
        "narrateur|Sarah souffle sur ses doigts, un peu farineux.",
        "papa|Il a lu, toi aussi ?",
        "enfant-f|Il avait un grain, comme un mot.",
        "maman|Les pages, une à une, l'ont rendu.",
        "narrateur|Une page du livre garde un grain, tout seul.",
        "narrateur|Le canard, rincé, nage sans poussière.",
    ],
    (2, 2, 2): [
        "narrateur|Sarah renifle le couvercle, puis le bol.",
        "papa|Deux odeurs ?",
        "enfant-f|La farine ici, l'eau là.",
        "maman|Le pont du bateau est fini.",
        "narrateur|Le couvercle sent la farine, un instant.",
        "narrateur|Le bol, lui, sent la pomme et le bec.",
    ],
    (2, 2, 3): [
        "narrateur|Sarah tapote le mur de papier, dans le coin.",
        "papa|Le garde a quitté son poste ?",
        "enfant-f|Oui, pour nager.",
        "maman|L'ombre du coin n'a plus de bec.",
        "narrateur|Le livre tient le coin, comme un mur.",
        "narrateur|Dans l'eau, le canard n'a plus à garder.",
    ],
    (2, 3, 1): [
        "narrateur|Sarah regarde le pied de papa, nu maintenant.",
        "papa|J'ai failli le marcher.",
        "enfant-f|Il s'était sauvé, sous toi.",
        "maman|Une par une, tu as tout vu.",
        "narrateur|Près du pied de papa, le carrelage est nu.",
        "narrateur|Le canard, sauvé, tourne dans le bol.",
    ],
    (2, 3, 2): [
        "narrateur|Sarah montre le petit cercle d'eau sur le bois.",
        "papa|Une soucoupe, vraiment ?",
        "enfant-f|La plus petite, et la plus jaune.",
        "maman|Le plateau a tout révélé.",
        "narrateur|Le couvercle garde un cercle d'eau, minuscule.",
        "narrateur|Le vrai bol, plus large, tient le canard.",
    ],
    (2, 3, 3): [
        "narrateur|Sarah ferme un peu le coin, d'un cube oublié.",
        "papa|L'ombre a perdu son secret ?",
        "enfant-f|Oui, il nage, maintenant.",
        "maman|Les tasses tiennent, serrées, sans lui.",
        "narrateur|Le coin sombre a perdu son secret.",
        "narrateur|L'eau du bol, claire, montre le jaune.",
    ],
    (3, 1, 1): [
        "narrateur|Sarah approche le visage de la vapeur.",
        "papa|Il se chauffait, disais-tu.",
        "enfant-f|Oui, collé au pied, avant le bain.",
        "maman|Un par un, tu as vu le pied.",
        "narrateur|Une vapeur mince entoure le canard, enfin.",
        "narrateur|La tarte, au four, sent la même chaleur.",
    ],
    (3, 1, 2): [
        "narrateur|Sarah pousse le sel d'un doigt, pour faire de la place.",
        "papa|Voisin du sel, maintenant ?",
        "enfant-f|Voisin, et nageur.",
        "maman|Le plateau a fait le détour, loin du thé.",
        "narrateur|Le sel a un voisin jaune, qui nage.",
        "narrateur|Mila, plus loin, reprend un cube, sans l'eau.",
    ],
    (3, 1, 3): [
        "narrateur|Sarah tend le bras : bol d'un côté, caisse de l'autre.",
        "papa|Plus de barrière ?",
        "enfant-f|Le passage, c'était lui.",
        "maman|Les cubes, au loin, ne font plus mur.",
        "narrateur|Entre le bol et le bois, plus rien ne barre.",
        "narrateur|Le canard va, vient, dans son rond d'eau.",
    ],
    (3, 2, 1): [
        "narrateur|Sarah lisse la page un peu ondulée.",
        "papa|Un signet trop gros, vraiment.",
        "enfant-f|Il s'était mis dans le livre.",
        "maman|Page après page, tu l'as vu.",
        "narrateur|Une page reste un peu ondulée, près de l'eau.",
        "narrateur|Le canard, lui, n'est plus plat.",
    ],
    (3, 2, 2): [
        "narrateur|Sarah essuie la goutte du couvercle, d'un coin de nappe.",
        "papa|Il s'accrochait au bol ?",
        "enfant-f|Oui, et le plateau l'a décroché.",
        "maman|Le livre, sec, n'a plus soif.",
        "narrateur|Le couvercle a une goutte, qu'elle essuie.",
        "narrateur|Le canard, dans l'eau, n'a plus à s'accrocher.",
    ],
    (3, 2, 3): [
        "narrateur|Sarah pose la main sous le pied du bol, vide.",
        "papa|Le papier pressait, tu disais.",
        "enfant-f|Le livre le serrait contre l'eau.",
        "maman|Le coin sec a pris le papier.",
        "narrateur|Sous le pied du bol, le carrelage luit.",
        "narrateur|Le canard nage, libre, sans papier.",
    ],
    (3, 3, 1): [
        "narrateur|Sarah tourne autour du bol, plus personne.",
        "papa|L'invité a quitté la table ?",
        "enfant-f|Il buvait en cachette, maintenant c'est vrai.",
        "maman|Les tasses rentrent, sans cérémonie.",
        "narrateur|Autour du bol, plus d'assiette jouet.",
        "narrateur|Le canard boit, ou nage, on ne sait pas.",
    ],
    (3, 3, 2): [
        "narrateur|Sarah salue Mila, d'un petit coup de tasse.",
        "papa|Le goûter est fini ?",
        "enfant-f|Le vrai plat, c'est l'eau.",
        "maman|Mila a applaudi, c'est assez.",
        "narrateur|Le couvercle sent le goûter, plus le canard.",
        "narrateur|Dans le bol, le jaune est le seul invité.",
    ],
    (3, 3, 3): [
        "narrateur|Sarah trace du doigt le chemin entre les deux camps.",
        "papa|Deux mondes, tu disais.",
        "enfant-f|Le mien, c'est l'eau.",
        "maman|Mila garde les tasses, toi le bol.",
        "narrateur|Entre le coin et le bol, le carrelage est un chemin.",
        "narrateur|Au bout, le canard tourne, et la tarte attend.",
    ],
}

END_SONS = {
    1: "bol,eau",
    2: "tarte,zinc",
    3: "caisse,carrelage",
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
        by_src["CHK_T0000_P0000"], OPENING, "opening", "zinc,tarte,caisse"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {
            "fields": {
                "option_1_label": "la nappe",
                "option_2_label": "le tas",
                "option_3_label": "le bol",
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
                    "option_1_label": "les cubes",
                    "option_2_label": "le livre",
                    "option_3_label": "la dînette",
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
                        "option_1_label": "un par un",
                        "option_2_label": "le couvercle",
                        "option_3_label": "le coin",
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
        "Sarah veut son canard jaune dans l'eau tiède, pendant la tarte aux pommes. "
        "Mila veut garder sa tour. Sarah tire la caisse : le tas tombe, le bec disparaît. "
        "Elle cherche sous la nappe, dans le tas ou près du bol ; elle remet cubes, "
        "livre ou dînette dans la caisse ; elle finit un par un, avec le couvercle "
        "ou par le coin. Vingt-sept bains distincts."
    )
    story["title"] = "Le canard sous la caisse de Sarah"
    story["characters"] = "Sarah, Mila, papa, maman"
    story["setting"] = "cuisine de village, nappe à carreaux, caisse sous la table, tarte aux pommes"
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
        "# TREE-AUT-024 — Le canard sous la caisse de Sarah\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Public :** N2 (3–6 ans), audio familial\n"
        "- **Leçon :** AUT.RAN.001 — ranger, vécue (le bec ne revient que lorsque "
        "les jouets ont une place dans la caisse)\n"
        "- **Personnages :** Sarah, Mila, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "## Vécu\n\n"
        "Cuisine de village, zinc, tarte aux pommes, nappe à carreaux, caisse sous "
        "la table, bol d'eau. Désir : le canard jaune dans l'eau tiède, maintenant. "
        "Mila veut garder sa tour. Première idée : tirer la caisse d'un coup. Le tas "
        "tombe, le bec disparaît, les épaules baissent. Enquête autre que le gabarit "
        "cuisine / jardin / chambre :\n\n"
        "- T1 recherche : la nappe / le tas / le bol\n"
        "- T2 bazar à remettre : les cubes / le livre / la dînette\n"
        "- T3 manière : un par un / le couvercle / le coin\n\n"
        "Q = nappe / tas / bol. Merci vécu quand l'objet reprend sa place. "
        "Chaque fin paie zinc, tarte, nappe, bol ou bec, sans morale.\n\n"
        "## Vu et corrigé\n\n"
        "- Inès / Victorina absentes (D16 : Sarah + Mila). T1/T2/T3 changés "
        "(plus cuisine / cubes-lieu / matin).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Impatience au départ, découragement sous le tas, fierté calme au bain.\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, "
        "émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration), "
        "`style_energy`, pauses, pitch, volume. `slow` = choix, indice, fin.\n"
        "- 27 bains, 27 dernières images. Ouverture + 3 L1 + 9 L2 + 27 L3/fins relus.\n"
        "- `check()` N2≤15. Pas apply.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
