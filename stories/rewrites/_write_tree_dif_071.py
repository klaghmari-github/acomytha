#!/usr/bin/env python3
"""TREE-DIF-071 — F-NAR-019. Avion de papier de Mila, hangar. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-071"
N3 = 16
TITLE = "L'avion de papier de Mila, dans le hangar"
FIL = (
    "Dans le hangar à vélos, Mila veut faire voler un avion de papier "
    "d'un bout à l'autre, sans virer, avant la pluie. Elle le jette trop "
    "vite : il tape une roue. Victorino n'arrête pas de bouger. "
    "T1 = feuille / trombone / craie. T2 = guidons (roue) / flaque / porte. "
    "T3 = neuf façons de jouer avec son élan : il tient, il compte, il s'assoit. "
    "L'avion glisse jusqu'à la porte. On rentre."
)
CHARS = "Mila, Victorino, papa, maman"
SETTING = "hangar à vélos derrière la maison : guidons, flaque, porte"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "hangar à vélos",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_pluie_arrive_et_l_avion_doit_partir; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change l_élan; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_objets_partent_avec_eux; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_l_avion_rate; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_élan_de_Victorino_prend_l_avion; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=l_élan_trouve_un_métier; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_avion_a_payé_le_nez_plié_du_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Derrière la maison, le hangar à vélos sent la graisse.",
    "narrateur|Un filet de pluie coupe le ciment, étroit.",
    "narrateur|Une sonnette de vélo tinte, toute seule.",
    "papa|Tu as vu le trait d'eau, Mila ?",
    "enfant-f|Il barre le sol, jusqu'à la porte.",
    "maman|Ça sent le caoutchouc mouillé, ici.",
    "narrateur|En ce moment, Mila plie un coin de papier.",
    "enfant-f|Je veux qu'il vole, sans virer.",
    "papa|Avant la pluie, d'un bout à l'autre.",
    "narrateur|Les pieds de Victorino tapent le ciment.",
    "enfant-m|On le lance, Mila, maintenant !",
    "narrateur|Elle le jette trop vite, vers la roue.",
    "narrateur|Le nez se plie de travers.",
    "enfant-f|Il n'est pas allé jusqu'à la porte.",
    "maman|Le papier, le trombone, et la craie.",
    "papa|Merci, tu as replié le nez.",
]

T1_CHOICE = [
    "narrateur|Près de la pompe, trois affaires attendent.",
    "narrateur|Une feuille blanche, un trombone, une craie.",
    "maman|Tu prends quoi d'abord, Mila ?",
]

T1 = {
    1: {
        "lab": "la feuille",
        "sons": "papier,pli",
        "emphasis": "feuille blanche",
        "passage": [
            "narrateur|Mila prend d'abord la feuille blanche.",
            "enfant-f|Elle est froide, sous les doigts.",
            "papa|Le pli du nez tient, là.",
            "narrateur|Elle la tend vers Victorino, trop près.",
            "enfant-m|Moi je la lance, trop vite !",
            "narrateur|Mila replie le coin, sans crier.",
            "narrateur|Un grain de graisse tache le bord.",
            "maman|Le trombone et la craie viennent aussi.",
            "narrateur|Papa glisse le tout contre sa poche.",
            "narrateur|Rien ne reste sur le ciment.",
            "enfant-m|Mila, on part ?",
            "enfant-f|Jusqu'à la porte, sans virer.",
            "papa|La feuille d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Mila a pris la feuille d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "feuille",
            "accepted_examples": "feuille | la feuille | d'abord la feuille | le papier | la feuille blanche",
            "retry_prompt": "Mila prend la feuille d'abord.",
        },
        "confirm": [
            "narrateur|La feuille reste contre elle, froide.",
            "enfant-f|On va jusqu'à la porte.",
            "maman|La pluie n'est pas loin.",
            "papa|Tu tiens bien, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un pli blanc cherche l'air.",
            "enfant-m|Moi je tiens la sonnette, fort.",
            "narrateur|Un tintement court, puis se tait.",
        ],
        "voy": "La feuille penche vers le hangar.",
    },
    2: {
        "lab": "le trombone",
        "sons": "metal,cliquetis",
        "emphasis": "trombone",
        "passage": [
            "narrateur|Mila prend d'abord le trombone, minuscule.",
            "enfant-f|Il pique un peu, au pouce.",
            "maman|Il va tenir le nez, droit.",
            "narrateur|Elle le glisse sur le pli, trop vite.",
            "enfant-m|Moi je le lance avec, trop fort !",
            "narrateur|Le métal cliquette contre le papier.",
            "narrateur|Une goutte de graisse brille au bout.",
            "papa|La feuille et la craie viennent aussi.",
            "narrateur|Maman les pose contre le sac.",
            "narrateur|Le ciment reste vide, derrière eux.",
            "enfant-m|On y va, Mila ?",
            "enfant-f|Le nez d'abord, il pèse.",
            "maman|Le trombone d'abord, il est pris.",
        ],
        "question": [
            "narrateur|Mila a pris le trombone d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "trombone",
            "accepted_examples": "trombone | le trombone | d'abord le trombone | le métal",
            "retry_prompt": "Mila prend le trombone d'abord.",
        },
        "confirm": [
            "narrateur|Le trombone pend au pli, un peu lâche.",
            "enfant-f|Il va garder le nez.",
            "papa|Ça sent la graisse, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le métal se tait, puis plus rien.",
            "enfant-m|Moi je fais tinter, fort.",
            "narrateur|La sonnette cliquette, trop vite.",
        ],
        "voy": "Le trombone colle au pli, lourd.",
    },
    3: {
        "lab": "la craie",
        "sons": "craie,poussiere",
        "emphasis": "craie",
        "passage": [
            "narrateur|Mila prend d'abord la craie, un peu rêche.",
            "enfant-f|Elle va faire la piste.",
            "papa|Un trait, pas tout le ciment.",
            "narrateur|Un blanc court sous son doigt.",
            "enfant-m|Moi je cours sur la piste !",
            "narrateur|Mila tient la craie, serrée.",
            "narrateur|Un peu de poussière blanche tombe.",
            "maman|La feuille et le trombone viennent aussi.",
            "narrateur|Papa les glisse contre son genou.",
            "narrateur|La pompe reste seule, plus loin.",
            "enfant-m|La piste, c'est pour l'avion ?",
            "enfant-f|Oui, droit, jusqu'à la porte.",
            "papa|La craie d'abord, elle est à toi.",
        ],
        "question": [
            "narrateur|Mila a pris la craie d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "craie",
            "accepted_examples": "craie | la craie | d'abord la craie | le trait",
            "retry_prompt": "Mila prend la craie d'abord.",
        },
        "confirm": [
            "narrateur|La craie reste chaude, contre sa poche.",
            "enfant-f|Le trait ne verse pas.",
            "maman|Le blanc sent la poussière.",
            "papa|On avance, tous les quatre ?",
            "enfant-f|Oui.",
            "narrateur|Un trait blanc attend, droit, au sol.",
            "enfant-m|Moi je cours devant, Mila !",
            "narrateur|Ses talons tapent le ciment, trop vite.",
        ],
        "voy": "La craie appuie contre sa poche.",
    },
}

T2 = {
    (1, 1): {
        "sons": "roue,rayons",
        "emphasis": "roue",
        "passage": [
            "narrateur|Entre ses doigts, le papier est froid.",
            "narrateur|Près des guidons, une roue tourne toute seule.",
            "narrateur|Mila vise le couloir, trop tôt.",
            "enfant-m|Je la fais tourner, trop fort !",
            "narrateur|Le papier tape les rayons, de travers.",
            "enfant-f|Mon avion a touché !",
            "narrateur|Les rayons claquent, trop près.",
            "papa|Ici, la roue n'arrête pas.",
            "maman|L'avion a besoin d'un couloir.",
            "enfant-f|Alors on fait comment ?",
            "papa|Tu vois comment, avec lui ?",
        ],
    },
    (1, 2): {
        "sons": "flaque,eau",
        "emphasis": "flaque",
        "passage": [
            "narrateur|Le papier cherche l'air, léger.",
            "narrateur|Au milieu, la flaque brille sous le filet.",
            "narrateur|Mila veut passer au-dessus, trop tôt.",
            "enfant-m|Je saute dedans, trop fort !",
            "narrateur|Le papier boit l'eau, trop gris.",
            "enfant-f|Mon avion est mouillé !",
            "narrateur|Des ronds d'eau courent, trop larges.",
            "papa|Ici, ça saute trop.",
            "maman|L'avion n'arrive pas à glisser.",
            "enfant-f|Alors on fait comment ?",
            "maman|Tu vois comment, avec lui ?",
        ],
    },
    (1, 3): {
        "sons": "vent,porte",
        "emphasis": "vent",
        "passage": [
            "narrateur|Le pli blanc tremble vers la porte.",
            "narrateur|Près du battant, le vent pousse, fort.",
            "narrateur|Mila lève le papier, trop tôt.",
            "enfant-m|J'ouvre, trop vite !",
            "narrateur|Le papier part de travers, pris.",
            "enfant-f|Le vent l'a pris !",
            "narrateur|Le battant claque, trop large.",
            "papa|Ici, ça souffle trop.",
            "maman|Il lui faut un air plus calme.",
            "enfant-f|Alors on fait comment ?",
            "papa|Tu vois comment, avec lui ?",
        ],
    },
    (2, 1): {
        "sons": "roue,metal",
        "emphasis": "rayon",
        "passage": [
            "narrateur|Dans sa paume, le trombone pique un peu.",
            "narrateur|Près des guidons, une roue tourne, vive.",
            "narrateur|Mila avance le nez lourd, trop près.",
            "enfant-m|Je pousse les rayons, hop !",
            "narrateur|Le trombone accroche un rayon, trop fort.",
            "enfant-f|Le nez est coincé !",
            "narrateur|Le métal sonne, puis le papier se tord.",
            "papa|Ici, la roue attrape tout.",
            "maman|Le nez a besoin d'un passage libre.",
            "enfant-f|Alors on fait comment ?",
            "papa|Tu vois comment, avec lui ?",
        ],
    },
    (2, 2): {
        "sons": "flaque,metal",
        "emphasis": "flaque",
        "passage": [
            "narrateur|Le trombone pèse le nez plié.",
            "narrateur|Au milieu, la flaque tremble, ronde.",
            "narrateur|Mila veut glisser au-dessus, trop tôt.",
            "enfant-m|Je tape l'eau, avec les deux pieds !",
            "narrateur|Le trombone gicle, trop mouillé, trop lourd.",
            "enfant-f|Il plonge dans l'eau !",
            "narrateur|Le papier s'alourdit, trop bas.",
            "papa|Ici, l'eau prend le métal.",
            "maman|Le nez n'arrive plus à voler.",
            "enfant-f|Alors on fait comment ?",
            "maman|Tu vois comment, avec lui ?",
        ],
    },
    (2, 3): {
        "sons": "vent,metal",
        "emphasis": "vent",
        "passage": [
            "narrateur|Le nez trop lourd penche vers le seuil.",
            "narrateur|Près de la porte, le vent pousse, large.",
            "narrateur|Mila lève le trombone, trop tôt.",
            "enfant-m|Je tiens le battant, ouvert !",
            "narrateur|Le nez trop lourd plonge, trop vite.",
            "enfant-f|Il est tombé près du seuil !",
            "narrateur|Le papier file de côté, trop loin.",
            "papa|Ici, le vent plus le poids, ça plonge.",
            "maman|Il lui faut un air plus calme.",
            "enfant-f|Alors on fait comment ?",
            "papa|Tu vois comment, avec lui ?",
        ],
    },
    (3, 1): {
        "sons": "roue,craie",
        "emphasis": "pneu",
        "passage": [
            "narrateur|Contre sa poche, la craie reste un peu chaude.",
            "narrateur|Près des guidons, une roue tourne, grise.",
            "narrateur|Mila trace un trait, trop près du pneu.",
            "enfant-m|Je roule dessus, regarder !",
            "narrateur|Le trait de craie se brouille sous le pneu.",
            "enfant-f|Ma piste est partie !",
            "narrateur|Un nuage blanc s'écrase, trop court.",
            "papa|Ici, la roue mange le blanc.",
            "maman|La piste a besoin d'un couloir.",
            "enfant-f|Alors on fait comment ?",
            "papa|Tu vois comment, avec lui ?",
        ],
    },
    (3, 2): {
        "sons": "flaque,craie",
        "emphasis": "flaque",
        "passage": [
            "narrateur|La craie appuie, prête à tracer.",
            "narrateur|Au milieu, la flaque coupe le ciment.",
            "narrateur|Mila veut un trait au sec, trop tôt.",
            "enfant-m|Je saute la ligne, trop fort !",
            "narrateur|Le trait de craie fond, trop mou, trop pâle.",
            "enfant-f|Le blanc a disparu !",
            "narrateur|Une bouillie blanche court dans l'eau.",
            "papa|Ici, l'eau boit la piste.",
            "maman|L'avion n'a plus de chemin.",
            "enfant-f|Alors on fait comment ?",
            "maman|Tu vois comment, avec lui ?",
        ],
    },
    (3, 3): {
        "sons": "vent,craie",
        "emphasis": "vent",
        "passage": [
            "narrateur|Un trait blanc cherche la porte.",
            "narrateur|Près du battant, le vent pousse la poussière.",
            "narrateur|Mila allonge le trait, trop tôt.",
            "enfant-m|J'ouvre grand, pour voir dehors !",
            "narrateur|Le trait s'envole en poussière, trop loin.",
            "enfant-f|Ma piste a volé !",
            "narrateur|Le blanc disparaît vers le seuil.",
            "papa|Ici, le vent prend le trait.",
            "maman|Il lui faut un air plus calme.",
            "enfant-f|Alors on fait comment ?",
            "papa|Tu vois comment, avec lui ?",
        ],
    },
}

T3_LABS = {
    1: ("le guidon", "les tours", "le seau"),
    2: ("l'avion", "les gouttes", "le bord"),
    3: ("la porte", "jusqu'à trois", "le banc"),
}

T3_CHOICE = {
    1: [
        "narrateur|La roue n'a pas fini de tourner.",
        "papa|Le guidon, les tours, ou le seau ?",
    ],
    2: [
        "narrateur|La flaque n'a pas fini de sauter.",
        "maman|L'avion, les gouttes, ou le bord ?",
    ],
    3: [
        "narrateur|Le vent n'a pas fini de pousser.",
        "papa|La porte, jusqu'à trois, ou le banc ?",
    ],
}

T3_SONS = {
    (1, 1): "guidon,roue",
    (1, 2): "compte,roue",
    (1, 3): "seau,pas",
    (2, 1): "papier,eau",
    (2, 2): "gouttes,toit",
    (2, 3): "bord,flaque",
    (3, 1): "porte,vent",
    (3, 2): "compte,souffle",
    (3, 3): "banc,bois",
}

T3_EMPH = {
    1: {1: "guidon", 2: "tours", 3: "seau"},
    2: {1: "avion", 2: "gouttes", 3: "bord"},
    3: {1: "porte", 2: "trois", 3: "banc"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|Tu tiens le guidon, Victorino.",
        "enfant-m|Je le serre, tout fort.",
        "narrateur|Elle tient la feuille, lui le guidon.",
        "narrateur|La roue ralentit, un tour, puis plus.",
        "narrateur|Un pli blanc cherche l'air, libre.",
        "papa|Tes mains ont tenu la roue.",
        "enfant-f|Le couloir est libre, maintenant.",
        "maman|L'élan a trouvé le guidon.",
    ],
    (1, 1, 2): [
        "enfant-f|Tu comptes les tours, d'abord.",
        "enfant-m|Un, deux, trois, quatre.",
        "narrateur|Il compte, la feuille reste contre elle.",
        "narrateur|La roue s'essouffle, puis s'arrête.",
        "narrateur|Un pli blanc attend le silence.",
        "papa|Tu as compté jusqu'au silence.",
        "enfant-m|Elle ne tourne plus, Mila.",
        "maman|Les tours ont pris son élan.",
    ],
    (1, 1, 3): [
        "enfant-f|Tu t'assoies un moment, là.",
        "enfant-m|Je m'assoie, les pieds vifs.",
        "narrateur|Victorino pose le seau, puis s'assoit.",
        "narrateur|Sur le seau, la feuille ne tremble plus.",
        "narrateur|Ses genoux dansent un peu, puis se posent.",
        "papa|Le seau a reçu tes jambes.",
        "enfant-f|Le papier peut partir, là.",
        "maman|Un moment assis, et la roue s'est tue.",
    ],
    (1, 2, 1): [
        "enfant-f|Tu tiens l'avion, tout haut.",
        "enfant-m|Je le serre, il ne tombe pas.",
        "narrateur|Il tient la feuille, au-dessus de l'eau.",
        "narrateur|Mila trace un trait, au sec.",
        "narrateur|Un pli blanc cherche l'air, sec.",
        "papa|Tes mains ont porté l'avion.",
        "enfant-f|La piste est sèche, maintenant.",
        "maman|L'élan a tenu le papier.",
    ],
    (1, 2, 2): [
        "enfant-f|Tu comptes les gouttes, sur le toit.",
        "enfant-m|Une, deux, trois, plus une.",
        "narrateur|Il compte, la feuille sèche un peu.",
        "narrateur|Ses pieds restent au bord, sans sauter.",
        "narrateur|La flaque se tait, une fois, puis plus.",
        "papa|Tu as compté le toit, pas l'eau.",
        "enfant-f|Le papier n'a plus soif.",
        "maman|Les gouttes ont pris son élan.",
    ],
    (1, 2, 3): [
        "enfant-f|Tu t'assoies au bord, tout petit.",
        "enfant-m|Je m'assoie, les pieds dansent un peu.",
        "narrateur|Victorino s'assoit, juste hors de l'eau.",
        "narrateur|Au bord, la feuille n'a plus d'eau.",
        "narrateur|Ses talons tapotent, puis se calment.",
        "papa|Le bord t'a gardé au sec.",
        "enfant-f|On peut glisser, là.",
        "maman|Un moment assis, et la flaque s'est tue.",
    ],
    (1, 3, 1): [
        "enfant-f|Tu tiens la porte, tout fort.",
        "enfant-m|Je la serre, elle ne claque plus.",
        "narrateur|Il tient la porte, la feuille ne file plus.",
        "narrateur|Le vent reste dehors, tout seul.",
        "narrateur|Un pli blanc cherche l'air, droit.",
        "papa|Tes mains ont tenu le battant.",
        "enfant-f|Le couloir est droit, maintenant.",
        "maman|L'élan a trouvé la porte.",
    ],
    (1, 3, 2): [
        "enfant-f|Tu comptes jusqu'à trois, d'abord.",
        "enfant-m|Un, deux, trois.",
        "narrateur|À trois, la feuille quitte ses doigts.",
        "narrateur|Victorino souffle avec, tout droit.",
        "narrateur|Le battant reste fermé, derrière eux.",
        "papa|Tu as compté, puis vous avez lancé.",
        "enfant-f|Il part avec nous.",
        "maman|Jusqu'à trois, l'élan a suivi.",
    ],
    (1, 3, 3): [
        "enfant-f|Tu t'assoies un moment, sur le banc.",
        "enfant-m|Je m'assoie, les mains vives.",
        "narrateur|Victorino s'assoit, près du battant.",
        "narrateur|Sur le banc, la feuille ne tremble plus.",
        "narrateur|Ses genoux dansent, puis se posent.",
        "papa|Le banc a reçu tes jambes.",
        "enfant-f|Le vent ne le prend plus.",
        "maman|Un moment assis, et le vent s'est tu.",
    ],
    (2, 1, 1): [
        "enfant-f|Le guidon, toi, le nez à moi.",
        "enfant-m|Je serre le guidon, il ne bouge plus.",
        "narrateur|Elle tient le trombone, lui le guidon.",
        "narrateur|La roue s'arrête avant le métal.",
        "narrateur|Le métal pèse le nez plié, libre.",
        "papa|Tes mains ont laissé le nez passer.",
        "enfant-f|Les rayons ne l'attrapent plus.",
        "maman|Le guidon a gardé la roue.",
    ],
    (2, 1, 2): [
        "enfant-f|Tu comptes les tours, pas les rayons.",
        "enfant-m|Un, deux, trois, elle ralentit.",
        "narrateur|Il compte, le trombone reste au pli.",
        "narrateur|Le cliquetis devient un compte, puis rien.",
        "narrateur|Le métal pèse le nez, sans accrocher.",
        "papa|Tu as compté le silence de la roue.",
        "enfant-m|Plus de rayons, Mila.",
        "maman|Les tours ont calmé le métal.",
    ],
    (2, 1, 3): [
        "enfant-f|Le seau, tes jambes, le nez ici.",
        "enfant-m|Je m'assoie, le métal loin des rayons.",
        "narrateur|Victorino s'assoit, le seau froid sous lui.",
        "narrateur|Sur le seau, le trombone ne cliquette plus.",
        "narrateur|Ses pieds battent l'air, puis se posent.",
        "papa|Le seau a tenu tes genoux.",
        "enfant-f|Le nez peut glisser, maintenant.",
        "maman|Assis, le métal n'accroche plus.",
    ],
    (2, 2, 1): [
        "enfant-f|Tu portes l'avion, nez en l'air.",
        "enfant-m|Je le tiens haut, au-dessus de l'eau.",
        "narrateur|Il tient le trombone, au-dessus de l'eau.",
        "narrateur|Mila essuie le nez, au sec.",
        "narrateur|Le métal pèse le nez plié, sec.",
        "papa|Tes bras ont gardé le nez hors de l'eau.",
        "enfant-f|Il n'est plus lourd d'eau.",
        "maman|L'élan a porté le métal.",
    ],
    (2, 2, 2): [
        "enfant-f|Les gouttes du toit, pas la flaque.",
        "enfant-m|Une, deux, trois, je reste ici.",
        "narrateur|Il compte, le trombone sèche un peu.",
        "narrateur|Ses talons restent au sec, collés au ciment.",
        "narrateur|La flaque se tait, sans éclaboussure.",
        "papa|Tu as compté le toit, pas l'eau.",
        "enfant-f|Le nez sèche, tout seul.",
        "maman|Les gouttes ont pris les pieds.",
    ],
    (2, 2, 3): [
        "enfant-f|Au bord, tu t'assoies, nez au sec.",
        "enfant-m|Je m'assoie, loin de la flaque.",
        "narrateur|Victorino s'assoit, sur le ciment sec.",
        "narrateur|Au bord, le trombone n'a plus d'eau.",
        "narrateur|Ses mains tapotent ses genoux, puis s'arrêtent.",
        "papa|Le bord t'a gardé au sec.",
        "enfant-f|Le métal ne gicle plus.",
        "maman|Assis au bord, l'eau reste là.",
    ],
    (2, 3, 1): [
        "enfant-f|Tu fermes la porte, je tiens le nez.",
        "enfant-m|Je la pousse, elle reste close.",
        "narrateur|Il tient la porte, le trombone ne plonge plus.",
        "narrateur|Le vent reste dehors, le nez reste droit.",
        "narrateur|Le métal pèse le nez plié, stable.",
        "papa|Tes mains ont tenu le battant.",
        "enfant-f|Le poids n'a plus le vent.",
        "maman|La porte a gardé l'air.",
    ],
    (2, 3, 2): [
        "enfant-f|Jusqu'à trois, puis le nez part.",
        "enfant-m|Un, deux, trois.",
        "narrateur|À trois, le trombone quitte le pli.",
        "narrateur|Victorino souffle avec, sans ouvrir.",
        "narrateur|Le battant reste fermé, le nez file droit.",
        "papa|Tu as compté, puis le nez a volé.",
        "enfant-f|Il n'a pas plongé.",
        "maman|Jusqu'à trois, le poids a suivi.",
    ],
    (2, 3, 3): [
        "enfant-f|Le banc, toi, le nez à moi.",
        "enfant-m|Je m'assoie, loin du battant.",
        "narrateur|Victorino s'assoit, les mains sur le bois.",
        "narrateur|Sur le banc, le trombone ne pique plus.",
        "narrateur|Ses épaules dansent, puis se posent.",
        "papa|Le banc a reçu tes bras.",
        "enfant-f|Le vent n'a plus de porte.",
        "maman|Assis, le nez n'a plus peur.",
    ],
    (3, 1, 1): [
        "enfant-f|Tu tiens le guidon, je tiens la craie.",
        "enfant-m|Je serre, la roue s'arrête.",
        "narrateur|Elle tient la craie, lui le guidon.",
        "narrateur|Mila retrace un blanc, hors du pneu.",
        "narrateur|Un trait blanc attend, tout droit, au sol.",
        "papa|Tes mains ont laissé la piste.",
        "enfant-f|Le pneu n'écrase plus le blanc.",
        "maman|Le guidon a sauvé le trait.",
    ],
    (3, 1, 2): [
        "enfant-f|Tu comptes les tours, je trace.",
        "enfant-m|Un, deux, trois, quatre, stop.",
        "narrateur|Il compte, la craie reste dans sa main.",
        "narrateur|La roue s'arrête, le blanc reste net.",
        "narrateur|Un trait blanc attend, hors des pneus.",
        "papa|Tu as compté, elle a tracé.",
        "enfant-m|La piste est là, Mila.",
        "maman|Les tours ont laissé le trait.",
    ],
    (3, 1, 3): [
        "enfant-f|Le seau, toi, la piste autour.",
        "enfant-m|Je m'assoie, loin de la roue.",
        "narrateur|Victorino s'assoit, le seau sous lui.",
        "narrateur|Sur le seau, la craie ne tombe plus.",
        "narrateur|Mila trace autour du seau, jusqu'à la porte.",
        "papa|Le seau a reçu tes jambes.",
        "enfant-f|La piste contourne tes pieds.",
        "maman|Assis, le pneu n'a plus le blanc.",
    ],
    (3, 2, 1): [
        "enfant-f|Tu tiens l'avion, je trace au sec.",
        "enfant-m|Je le porte haut, loin de l'eau.",
        "narrateur|Il tient la craie, au-dessus de l'eau.",
        "narrateur|Mila trace un trait, au sec, large.",
        "narrateur|Un trait blanc attend, tout droit, au sol.",
        "papa|Tes mains ont porté la craie.",
        "enfant-f|Le blanc n'a pas bu.",
        "maman|L'élan a gardé le trait.",
    ],
    (3, 2, 2): [
        "enfant-f|Les gouttes du toit, je retrace.",
        "enfant-m|Une, deux, trois, je ne saute pas.",
        "narrateur|Il compte, le trait redevient blanc.",
        "narrateur|Ses pieds restent au bord, secs.",
        "narrateur|Mila rallonge le blanc, hors de l'eau.",
        "papa|Tu as compté le toit, pas l'eau.",
        "enfant-f|La piste a une rive sèche.",
        "maman|Les gouttes ont laissé le trait.",
    ],
    (3, 2, 3): [
        "enfant-f|Au bord, tu t'assoies, je trace.",
        "enfant-m|Je m'assoie, le blanc à côté.",
        "narrateur|Victorino s'assoit, juste hors de l'eau.",
        "narrateur|Au bord, la craie n'a plus d'eau.",
        "narrateur|Mila trace entre lui et la porte.",
        "papa|Le bord t'a gardé au sec.",
        "enfant-f|Le trait passe près de tes genoux.",
        "maman|Assis, la flaque n'a plus le blanc.",
    ],
    (3, 3, 1): [
        "enfant-f|Tu tiens la porte, je finis le trait.",
        "enfant-m|Je la serre, le vent reste dehors.",
        "narrateur|Il tient la porte, le trait ne s'envole plus.",
        "narrateur|Mila allonge le blanc jusqu'au seuil.",
        "narrateur|Un trait blanc attend, tout droit, au sol.",
        "papa|Tes mains ont tenu le battant.",
        "enfant-f|La poussière reste au sol.",
        "maman|La porte a gardé le trait.",
    ],
    (3, 3, 2): [
        "enfant-f|Jusqu'à trois, le trait guide.",
        "enfant-m|Un, deux, trois.",
        "narrateur|À trois, le trait guide le papier.",
        "narrateur|Victorino souffle avec, le battant fermé.",
        "narrateur|Le blanc reste au sol, net.",
        "papa|Tu as compté, le trait a montré.",
        "enfant-f|Il suit le blanc.",
        "maman|Jusqu'à trois, la piste a tenu.",
    ],
    (3, 3, 3): [
        "enfant-f|Le banc, toi, le trait jusqu'à toi.",
        "enfant-m|Je m'assoie, le vent loin de moi.",
        "narrateur|Victorino s'assoit, près du battant.",
        "narrateur|Sur le banc, la craie ne tombe plus.",
        "narrateur|Mila trace jusqu'aux pieds du banc.",
        "papa|Le banc a reçu tes jambes.",
        "enfant-f|Le blanc arrive à tes chaussures.",
        "maman|Assis, le vent n'a plus le trait.",
    ],
}

END_SONS = {1: "roue,porte", 2: "flaque,porte", 3: "vent,porte"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|L'avion glisse entre les guidons, jusqu'à la porte.",
        "enfant-f|Tu as tenu le guidon.",
        "enfant-m|La roue s'est tue, alors il a volé.",
        "papa|Tes mains ont laissé le couloir.",
        "maman|On rentre, la pluie n'est pas loin.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Un grain de graisse sèche sur le ciment.",
    ],
    (1, 1, 2): [
        "narrateur|Après les tours, l'avion file jusqu'à la porte.",
        "enfant-f|Tu as compté les tours.",
        "enfant-m|Quatre, puis plus rien, puis il a volé.",
        "papa|Les tours ont pris ton élan.",
        "maman|Essuie tes mains, on rentre.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|La sonnette se tait, plus loin, toute seule.",
    ],
    (1, 1, 3): [
        "narrateur|Depuis le seau, l'avion part jusqu'à la porte.",
        "enfant-f|Tu t'es assis un moment.",
        "enfant-m|Le seau était froid, puis ça allait.",
        "papa|Le seau a reçu tes jambes.",
        "maman|On rentre, le hangar sent la graisse.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Une chaîne de vélo cliquette, puis plus rien.",
    ],
    (1, 2, 1): [
        "narrateur|Au-dessus de l'eau, l'avion glisse jusqu'à la porte.",
        "enfant-f|Tu as tenu l'avion, tout haut.",
        "enfant-m|Il n'est pas tombé dans l'eau.",
        "papa|Tes mains ont porté le papier.",
        "maman|On rentre, vos chaussures sont un peu mouillées.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Un rond d'eau sèche sur le ciment, pâle.",
    ],
    (1, 2, 2): [
        "narrateur|Après les gouttes, l'avion file jusqu'à la porte.",
        "enfant-f|Tu as compté les gouttes.",
        "enfant-m|Le toit parlait, pas la flaque.",
        "papa|Tu as compté le toit, pas l'eau.",
        "maman|On rentre, ça sent le caoutchouc.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Une goutte sèche sur le guidon, minuscule.",
    ],
    (1, 2, 3): [
        "narrateur|Depuis le bord, l'avion part, sec, jusqu'à la porte.",
        "enfant-f|Tu t'es assis au bord.",
        "enfant-m|Mes pieds dansaient, puis ils se sont tus.",
        "papa|Le bord t'a gardé au sec.",
        "maman|On rentre, la flaque redevient un miroir.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Le filet de pluie pâlit, puis s'efface.",
    ],
    (1, 3, 1): [
        "narrateur|Derrière la porte tenue, l'avion file droit.",
        "enfant-f|Tu as tenu le battant.",
        "enfant-m|Le vent est resté dehors.",
        "papa|Tes mains ont tenu la porte.",
        "maman|On rentre, le seuil est sec.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Un reflet jaune tremble au seuil, puis s'arrête.",
    ],
    (1, 3, 2): [
        "narrateur|À trois, l'avion quitte les doigts, droit.",
        "enfant-f|Tu as compté jusqu'à trois.",
        "enfant-m|Un, deux, trois, et il a volé.",
        "papa|Vous avez lancé ensemble, tout droit.",
        "maman|On rentre, la pluie tapote le toit.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Le battant reste fermé, derrière le papier.",
    ],
    (1, 3, 3): [
        "narrateur|Depuis le banc, l'avion glisse jusqu'au seuil.",
        "enfant-f|Tu t'es assis un moment.",
        "enfant-m|Le banc était froid, puis ça allait.",
        "papa|Le banc a reçu tes jambes.",
        "maman|On rentre, le hangar se tait.",
        "narrateur|La feuille garde un pli tiède, tout petit.",
        "narrateur|Une sonnette oubliée tinte, puis le silence.",
    ],
    (2, 1, 1): [
        "narrateur|Le nez lourd glisse entre les rayons, libre.",
        "enfant-f|Tu as tenu le guidon, loin du métal.",
        "enfant-m|La roue n'a plus attrapé le nez.",
        "papa|Tes mains ont laissé le nez passer.",
        "maman|On rentre, essuie le trombone.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Le trombone reste froid, contre le nez plié.",
    ],
    (2, 1, 2): [
        "narrateur|Après le compte, le nez file entre les guidons.",
        "enfant-f|Tu as compté, le métal n'a pas sonné.",
        "enfant-m|Trois, puis plus de rayons.",
        "papa|Les tours ont calmé le métal.",
        "maman|On rentre, le cliquetis s'est tu.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Le métal ne cliquette plus, dans sa poche.",
    ],
    (2, 1, 3): [
        "narrateur|Depuis le seau, le nez lourd part, droit.",
        "enfant-f|Tu t'es assis, loin des rayons.",
        "enfant-m|Le seau tenait mes genoux.",
        "papa|Le seau a tenu tes genoux.",
        "maman|On rentre, le hangar sent le métal.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Un rayon luisant s'arrête, sans tourner.",
    ],
    (2, 2, 1): [
        "narrateur|Le nez, porté haut, glisse au-dessus de l'eau.",
        "enfant-f|Tu as porté l'avion, nez en l'air.",
        "enfant-m|Mes bras ont eu mal, puis ça volait.",
        "papa|Tes bras ont gardé le nez hors de l'eau.",
        "maman|On rentre, tes manches sont sèches.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Une tache d'eau quitte le trombone, lente.",
    ],
    (2, 2, 2): [
        "narrateur|Après les gouttes du toit, le nez file au sec.",
        "enfant-f|Tu as compté le toit.",
        "enfant-m|La flaque n'a pas parlé.",
        "papa|Tu as compté le toit, pas l'eau.",
        "maman|On rentre, ça sent le caoutchouc mouillé.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Une goutte glisse sur le métal, puis part.",
    ],
    (2, 2, 3): [
        "narrateur|Depuis le ciment sec, le nez glisse jusqu'à la porte.",
        "enfant-f|Tu t'es assis au bord, au sec.",
        "enfant-m|Mes genoux étaient froids, puis ça allait.",
        "papa|Le bord t'a gardé au sec.",
        "maman|On rentre, la flaque reste ronde.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|La flaque redevient un miroir, sous la pompe.",
    ],
    (2, 3, 1): [
        "narrateur|Porte close, le nez lourd file jusqu'au seuil.",
        "enfant-f|Tu as fermé, j'ai lancé.",
        "enfant-m|Le vent est resté derrière le bois.",
        "papa|Tes mains ont tenu le battant.",
        "maman|On rentre, le seuil est sec.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Le nez lourd reste droit, contre sa paume.",
    ],
    (2, 3, 2): [
        "narrateur|À trois, le nez quitte le pli, sans plonger.",
        "enfant-f|Tu as compté, il n'a pas plongé.",
        "enfant-m|Un, deux, trois, droit.",
        "papa|Tu as compté, puis le nez a volé.",
        "maman|On rentre, la pluie tapote le toit.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Le battant et le métal se taisent ensemble.",
    ],
    (2, 3, 3): [
        "narrateur|Depuis le banc, le nez lourd glisse, sans vent.",
        "enfant-f|Tu t'es assis, loin du battant.",
        "enfant-m|Le bois était froid sous mes mains.",
        "papa|Le banc a reçu tes bras.",
        "maman|On rentre, le hangar se tait.",
        "narrateur|Le trombone reste froid, contre le nez.",
        "narrateur|Une sonnette froide tinte contre le trombone.",
    ],
    (3, 1, 1): [
        "narrateur|Le long du blanc, l'avion glisse jusqu'à la porte.",
        "enfant-f|Tu as tenu, j'ai tracé.",
        "enfant-m|Le pneu n'a plus mangé la piste.",
        "papa|Tes mains ont laissé la piste.",
        "maman|On rentre, essuie tes doigts blancs.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|Un trait de craie sèche sur le ciment, net.",
    ],
    (3, 1, 2): [
        "narrateur|Après le compte, l'avion suit le blanc, droit.",
        "enfant-f|Tu as compté, j'ai tracé.",
        "enfant-m|Quatre, stop, puis la piste.",
        "papa|Tu as compté, elle a tracé.",
        "maman|On rentre, la poussière reste au sol.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|La poussière blanche reste au creux de sa main.",
    ],
    (3, 1, 3): [
        "narrateur|Autour du seau, l'avion suit le blanc, jusqu'à la porte.",
        "enfant-f|Tu t'es assis, la piste t'a contourné.",
        "enfant-m|Le seau avait un trait, sur le bord.",
        "papa|Le seau a reçu tes jambes.",
        "maman|On rentre, le hangar sent la craie.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|Le seau garde un trait blanc, sur le bord.",
    ],
    (3, 2, 1): [
        "narrateur|Au sec, l'avion suit le blanc jusqu'à la porte.",
        "enfant-f|Tu as porté, j'ai tracé au sec.",
        "enfant-m|L'eau n'a pas bu le blanc.",
        "papa|Tes mains ont porté la craie.",
        "maman|On rentre, vos chaussures restent sèches.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|Un trait blanc attend, au sec, près de l'eau.",
    ],
    (3, 2, 2): [
        "narrateur|Après les gouttes, l'avion suit la rive sèche.",
        "enfant-f|Tu as compté, j'ai rallongé.",
        "enfant-m|Je n'ai pas sauté, le blanc est resté.",
        "papa|Tu as compté le toit, pas l'eau.",
        "maman|On rentre, ça sent le caoutchouc et la craie.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|La craie tiède reste dans sa poche.",
    ],
    (3, 2, 3): [
        "narrateur|Près de ses genoux, l'avion suit le blanc, sec.",
        "enfant-f|Tu t'es assis, j'ai tracé à côté.",
        "enfant-m|Le trait passait près de moi.",
        "papa|Le bord t'a gardé au sec.",
        "maman|On rentre, la flaque reste à sa place.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|Le bord du ciment redevient blanc, net.",
    ],
    (3, 3, 1): [
        "narrateur|Jusqu'au seuil, l'avion suit le blanc, sans vent.",
        "enfant-f|Tu as tenu, le trait est resté.",
        "enfant-m|La poussière n'a pas volé.",
        "papa|Tes mains ont tenu le battant.",
        "maman|On rentre, le seuil a un trait.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|Un trait blanc court jusqu'au seuil, droit.",
    ],
    (3, 3, 2): [
        "narrateur|À trois, l'avion suit le blanc, battant fermé.",
        "enfant-f|Tu as compté, il a suivi le trait.",
        "enfant-m|Un, deux, trois, sur le blanc.",
        "papa|Tu as compté, le trait a montré.",
        "maman|On rentre, la pluie tapote le toit.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|La craie rentre dans la poche, porte close.",
    ],
    (3, 3, 3): [
        "narrateur|Jusqu'aux chaussures du banc, l'avion glisse, droit.",
        "enfant-f|Tu t'es assis, le blanc t'a rejoint.",
        "enfant-m|Mes chaussures ont un peu de blanc.",
        "papa|Le banc a reçu tes jambes.",
        "maman|On rentre, le hangar se tait.",
        "narrateur|Un trait de craie sèche sur le ciment.",
        "narrateur|Le banc garde un peu de blanc, au bois.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "pluie,sonnette"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("la feuille", "le trombone", "la craie")},
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
            [
                f"narrateur|{t1['voy']}",
                "narrateur|Près des guidons, une roue tourne trop.",
                "narrateur|Au milieu, une flaque coupe le ciment.",
                "narrateur|Près de la porte, le vent pousse.",
                "papa|Mila, tu vas où ?",
            ],
            "choice",
            "",
            {"fields": t3lab("les guidons", "la flaque", "la porte")},
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
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf],
                    T3[(a, b, c)],
                    "resolution",
                    T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    ENDINGS[(a, b, c)],
                    "ending",
                    END_SONS[b],
                    {"emphasis": T3_EMPH[b][c]},
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
        "maya",
        "camarade qui bouge",
        "un camarade",
        "hyperactif",
        "ce n'est pas une faute",
        "beaucoup d'énergie",
        "il faut attendre",
        "jardin",
        "carrousel",
        "papillon",
        "portail",
        "citronnade",
        "cuisine",
        "chambre",
        "dînette",
        "dinette",
        "les cubes",
        "après la sieste",
        "capitaine",
        "plic",
        "volet jaune",
        "balle rouge",
        "pichet",
        "tout doux",
        "tout calme",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
    if "hangar" not in blob:
        raise SystemExit(f"{SID}: hangar absent")

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
        "# TREE-DIF-071 — L'avion de papier de Mila, dans le hangar\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — un camarade qui bouge beaucoup (vécue : l'élan trouve un métier)\n"
        "- **Personnages :** Mila, Victorino, papa, maman\n"
        "- **Lieu :** hangar à vélos derrière la maison : guidons, flaque, porte\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Derrière la maison, le hangar sent la graisse. Un filet de pluie coupe le ciment. "
        "Mila veut faire voler un avion de papier **d'un bout à l'autre, avant la pluie**. "
        "Elle le jette trop vite : il tape une roue. Première idée ratée. "
        "Victorino n'arrête pas de bouger. Elle prend la feuille, le trombone ou la craie ; "
        "près des guidons la roue tourne trop, au milieu la flaque saute trop, près de la porte "
        "le vent pousse trop ; une action change l'élan (guidon, tours, seau ; avion, gouttes, bord ; "
        "porte, jusqu'à trois, banc). L'avion glisse jusqu'à la porte. On rentre.\n\n"
        "## Vécu\n\n"
        "Mila veut l'avion **maintenant**. Elle lance trop tôt. Nez de travers, roue, flaque ou vent. "
        "Chaque choix change l'obstacle et le climax. La leçon se voit : gronder n'arrive pas ; "
        "tenir, compter ou s'asseoir donne un couloir. Fin : avion à la porte + pluie, "
        "image unique du chemin (graisse, sonnette, chaîne, flaque, guidon, filet, seuil, battant, craie).\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan jardin / Maya / « un camarade qui bouge » / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (nez replié). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
