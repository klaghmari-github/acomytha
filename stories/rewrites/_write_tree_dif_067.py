#!/usr/bin/env python3
"""TREE-DIF-067 — Le seau rond de Nino, au puits (N1, DIF.COR.002, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-067"
N1 = 10
TITLE = "Le seau rond de Nino, au puits"
FIL = (
    "Au puits du village, le puits se tait. Une écaille de lichen brille sur la corde. "
    "Nino veut remonter de l'eau pour la bassine de maman, maintenant. "
    "Il tire tout seul : la corde refuse. Il prend le seau rond, le seau mince ou la corde ; "
    "les trois partent. La margelle glisse, l'auge est trop basse, la treille accroche. "
    "Il refuse de foncer, retrouve l'écaille. Neuf façons de demander, d'attendre, de faire à deux. "
    "L'eau arrive. L'écaille voyage."
)
CHARS = "Nino, papa, maman"
SETTING = "puits du village : mousse, margelle, auge, treille"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "miel",
    "merle",
    "aujourd'hui,",
    "j'ai compris",
    "mission accomplie",
    "on va apprendre",
    "bon travail",
    "il faut attendre",
    "il faut demander",
    "on doit demander",
    "papa sourit",
    "maman sourit",
    "plus rond ou plus mince",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "écaille de lichen",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_puits_se_tait_l_ecaille_brille_il_tire_seul; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_maniere_de_demander; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_prend; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent_avec_eux; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_tire_tout_seul_ca_refuse; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=l_objet_resiste_il_veut_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "écaille de lichen",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=l_ecaille_et_la_demande_sans_tirer_seul; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "écaille de lichen",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_ecaille_paie_le_debut_l_eau_est_la; tempo=posé; sourire=léger; respiration=ample",
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


def vet(lines: list[str], where: str = "") -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{where} {n}>{N1}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} fin: {ph}")
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"{where} tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"{where} tic {m.group(0)!r}: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"{where} puces « {tok} »: {ph}")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""
        out.append(f"{role}|{ph}")
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines, src.get("chunk_id", "?"))
    m = dict(PROFILES[profile])
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


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


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


OPENING = [
    "narrateur|D'habitude, le puits cliquette.",
    "narrateur|Cet après-midi, il se tait.",
    "narrateur|Un souffle froid sort de la pierre.",
    "narrateur|L'ombre du puits sent le fer mouillé.",
    "enfant-m|Ça sent l'eau, en bas.",
    "narrateur|Nino pose la paume sur la mousse.",
    "enfant-m|Il est muet, le puits.",
    "papa|Tu as vu l'écaille, Nino ?",
    "narrateur|Une écaille de lichen brille, grise.",
    "narrateur|Elle colle à la corde rêche.",
    "maman|La bassine est vide, à la maison.",
    "enfant-m|Je veux remonter de l'eau.",
    "narrateur|En ce moment, Nino tire la corde.",
    "narrateur|La corde refuse, trop lourde.",
    "enfant-m|Je tire tout seul !",
    "narrateur|Le seau tape en bas, sourd.",
    "narrateur|Le sourire de Nino s'en va.",
    "papa|Lâche un peu, on regarde.",
    "maman|Merci, tu as lâché la corde.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "maman|Deux seaux attendent, près de la corde.",
    "papa|Un rond de bois, un mince de zinc.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près du puits.",
    "narrateur|Le seau rond, le seau mince, la corde.",
    "maman|Tu commences par laquelle ?",
]

T1 = {
    1: {
        "lab": "le seau rond",
        "sons": "seau-bois,mousse",
        "emphasis": "seau rond",
        "passage": [
            "narrateur|Nino prend d'abord le seau rond.",
            "enfant-m|Le bois est lourd, mouillé.",
            "maman|Le fond est large, stable.",
            "narrateur|Il pose le seau contre sa jambe.",
            "papa|Le mince de zinc vient aussi.",
            "narrateur|La corde rêche pend à son poignet.",
            "enfant-m|On les prend, tous.",
            "narrateur|Rien ne reste près de la pierre.",
            "enfant-m|Je descends le rond, tout seul.",
            "narrateur|Il tire sur l'anse.",
            "narrateur|L'anse glisse sur la mousse.",
            "narrateur|Le seau tape la paroi, sourd.",
            "papa|Tu as vu l'anse, Nino ?",
            "narrateur|Dans sa poitrine, ça se bouscule.",
        ],
        "question": [
            "narrateur|Nino a pris le seau rond.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "seau rond",
            "accepted_examples": "seau rond | le seau rond | d'abord le seau rond | le bois | rond",
            "retry_prompt": "Nino a pris le seau rond.",
        },
        "confirm": [
            "enfant-m|Le seau rond.",
            "papa|Oui.",
            "narrateur|Nino glisse le zinc sous le bras.",
            "maman|La corde, je te la tends.",
            "enfant-m|Elle gratte un peu.",
            "narrateur|Les trois affaires tapent sa jambe.",
            "papa|On cherche l'endroit.",
            "enfant-m|Pour l'eau de maman.",
            "narrateur|L'écaille de lichen voyage avec eux.",
            "maman|Tu tiens bien, Nino ?",
            "enfant-m|Oui, maman.",
        ],
        "voy": "L'anse de bois marque sa paume.",
    },
    2: {
        "lab": "le seau mince",
        "sons": "seau-zinc,cliquetis",
        "emphasis": "seau mince",
        "passage": [
            "narrateur|Nino prend d'abord le seau mince.",
            "enfant-m|Le zinc est froid, cliquetant.",
            "papa|Le fond est étroit, léger.",
            "narrateur|Il le serre contre son ventre.",
            "maman|Le rond de bois vient aussi.",
            "narrateur|La corde rêche pend à son poignet.",
            "enfant-m|On les prend, tous.",
            "narrateur|Rien ne reste près de la pierre.",
            "enfant-m|Je verse le mince, tout seul.",
            "narrateur|Le zinc penche trop vite.",
            "narrateur|Une lame d'eau fuit, trop fine.",
            "papa|Tu as vu le bord, Nino ?",
            "narrateur|Le sourire de Nino s'en va.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
        ],
        "question": [
            "narrateur|Nino a pris le seau mince.",
            "papa|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "seau mince",
            "accepted_examples": "seau mince | le seau mince | d'abord le seau mince | le zinc | mince",
            "retry_prompt": "Nino a pris le seau mince.",
        },
        "confirm": [
            "enfant-m|Le seau mince.",
            "maman|Oui.",
            "narrateur|Il ramasse le bois, lourd.",
            "papa|La corde, dans l'autre main ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux seaux voyagent contre lui.",
            "maman|On cherche l'endroit.",
            "enfant-m|Pour l'eau de maman.",
            "narrateur|L'écaille de lichen voyage au zinc.",
            "papa|Le mince penche moins, là.",
            "enfant-m|Je le tiens mieux.",
        ],
        "voy": "Le zinc cliquette contre sa jambe.",
    },
    3: {
        "lab": "la corde",
        "sons": "corde,pierre",
        "emphasis": "corde",
        "passage": [
            "narrateur|Nino prend d'abord la corde rêche.",
            "enfant-m|Elle pique les doigts.",
            "maman|C'est pour descendre le seau.",
            "narrateur|Il enroule un tour, lent.",
            "papa|Le rond et le mince viennent aussi.",
            "narrateur|Maman les pose contre la pierre.",
            "enfant-m|Je garde la corde.",
            "narrateur|Les trois affaires avancent avec lui.",
            "enfant-m|Je tire la corde, tout seul.",
            "narrateur|La corde refuse, trop tendue.",
            "narrateur|Un nœud se serre, trop vite.",
            "papa|Tu as vu le nœud, Nino ?",
            "narrateur|Le sourire de Nino s'en va.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
        ],
        "question": [
            "narrateur|Nino a pris la corde.",
            "maman|Il a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "corde",
            "accepted_examples": "corde | la corde | d'abord la corde | la corde rêche | rêche",
            "retry_prompt": "Nino a pris la corde.",
        },
        "confirm": [
            "enfant-m|La corde.",
            "papa|Oui.",
            "narrateur|Maman lui passe le seau rond.",
            "maman|Le mince, sous le bras.",
            "enfant-m|Il est là.",
            "narrateur|Le bois et le zinc avancent avec lui.",
            "papa|On cherche l'endroit.",
            "enfant-m|Pour l'eau de maman.",
            "narrateur|L'écaille de lichen voyage au fil.",
            "maman|Tu lâches un peu, Nino ?",
            "enfant-m|Un peu, oui.",
        ],
        "voy": "La corde rêche gratte ses doigts.",
    },
}

T2 = {
    (1, 1): {
        "sons": "mousse,pierre",
        "emphasis": "margelle",
        "passage": [
            "narrateur|L'anse de bois marque sa paume.",
            "narrateur|La margelle est trop glissante, trop verte.",
            "enfant-m|Je tire le rond, tout seul.",
            "narrateur|Le seau part de travers.",
            "narrateur|Une écaille de lichen glisse sur la mousse.",
            "enfant-m|Elle part !",
            "narrateur|Nino veut tirer plus fort.",
            "narrateur|Le seau tape la pierre, sourd.",
            "narrateur|Le sourire de Nino s'en va.",
            "papa|Ici, la pierre n'arrête pas.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois l'écaille, Nino ?",
            "narrateur|Nino ne tire plus.",
        ],
    },
    (1, 2): {
        "sons": "auge,eau",
        "emphasis": "auge",
        "passage": [
            "narrateur|L'anse de bois bute le bord, trop large.",
            "narrateur|L'auge est trop basse, trop étroite.",
            "enfant-m|Je verse le rond, tout seul.",
            "narrateur|Le seau bute, trop large.",
            "narrateur|L'eau va à côté, trop vite.",
            "narrateur|Une écaille de lichen colle au rebord.",
            "enfant-m|Ça ne rentre pas !",
            "narrateur|Il pousse plus fort, trop vite.",
            "papa|Ici, c'est trop bas.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Le sourire de Nino s'en va.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois l'écaille, au bord ?",
            "narrateur|Nino arrête de pousser.",
            "maman|L'écaille montre la vraie hauteur.",
        ],
    },
    (1, 3): {
        "sons": "vigne,corde",
        "emphasis": "treille",
        "passage": [
            "narrateur|L'anse de bois tape la vigne, trop large.",
            "narrateur|Près de la treille, la corde s'accroche.",
            "enfant-m|Je tire, tout seul.",
            "narrateur|Une vrille de vigne tient le nœud.",
            "narrateur|Le seau rond pend, trop lourd.",
            "narrateur|Une écaille de lichen brille sur la vrille.",
            "enfant-m|La corde ne descend plus !",
            "narrateur|Il tire plus fort, trop vite.",
            "narrateur|Le nœud se serre, trop sec.",
            "papa|Ici, ça s'accroche trop.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois l'écaille, sur la vrille ?",
            "narrateur|Nino lâche un peu la corde.",
        ],
    },
    (2, 1): {
        "sons": "zinc,mousse",
        "emphasis": "margelle",
        "passage": [
            "narrateur|Le zinc cliquette, trop léger, trop vite.",
            "narrateur|La margelle est trop glissante, trop verte.",
            "enfant-m|Je tiens le mince, tout seul.",
            "narrateur|Le seau penche, trop mince.",
            "narrateur|Une écaille de lichen glisse sous le zinc.",
            "enfant-m|Il part de travers !",
            "narrateur|Nino serre plus fort, trop vite.",
            "narrateur|Une lame d'eau fuit sur la mousse.",
            "narrateur|Le sourire de Nino s'en va.",
            "papa|Ici, la pierre n'arrête pas.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois l'écaille, sous le zinc ?",
            "narrateur|Nino ne serre plus.",
        ],
    },
    (2, 2): {
        "sons": "zinc,auge",
        "emphasis": "auge",
        "passage": [
            "narrateur|Une goutte de zinc part, trop vite.",
            "narrateur|L'auge est trop basse, trop étroite.",
            "enfant-m|Je verse le mince, tout seul.",
            "narrateur|Le zinc penche, et l'eau fuit.",
            "narrateur|Ça va à côté, trop fin.",
            "narrateur|Une écaille de lichen colle au rebord.",
            "enfant-m|Je n'arrive pas à verser !",
            "narrateur|Il penche plus, trop vite.",
            "papa|Ici, c'est trop bas.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Le sourire de Nino s'en va.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois l'écaille, au bord ?",
            "narrateur|Nino redresse le zinc.",
            "papa|L'écaille montre où poser.",
        ],
    },
    (2, 3): {
        "sons": "zinc,vigne",
        "emphasis": "treille",
        "passage": [
            "narrateur|Le zinc s'accroche, trop mince, trop vif.",
            "narrateur|Près de la treille, la corde s'accroche.",
            "enfant-m|Je décroche, tout seul.",
            "narrateur|Une vrille tient l'anse du zinc.",
            "narrateur|Le mince tape la pierre, trop mince.",
            "narrateur|Une écaille de lichen brille sur la vrille.",
            "enfant-m|Le zinc ne passe plus !",
            "narrateur|Il tire le zinc, trop vite.",
            "narrateur|La vrille se serre, trop verte.",
            "papa|Ici, ça s'accroche trop.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois l'écaille, sur la vrille ?",
            "narrateur|Nino lâche le zinc, un peu.",
        ],
    },
    (3, 1): {
        "sons": "corde,mousse",
        "emphasis": "margelle",
        "passage": [
            "narrateur|La corde rêche frotte la pierre, trop mouillée.",
            "narrateur|La margelle est trop glissante, trop verte.",
            "enfant-m|Je tire la corde, tout seul.",
            "narrateur|La corde brûle un peu ses paumes.",
            "narrateur|Une écaille de lichen glisse sur la mousse.",
            "enfant-m|Elle ne monte pas !",
            "narrateur|Nino tire plus fort, trop vite.",
            "narrateur|Le seau tape en bas, sourd.",
            "narrateur|Le sourire de Nino s'en va.",
            "papa|Ici, la pierre n'arrête pas.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois l'écaille, sur la mousse ?",
            "narrateur|Nino lâche un tour de corde.",
        ],
    },
    (3, 2): {
        "sons": "corde,auge",
        "emphasis": "auge",
        "passage": [
            "narrateur|La corde traîne dans l'auge, trop longue.",
            "narrateur|L'auge est trop basse, trop étroite.",
            "enfant-m|Je descends tout seul.",
            "narrateur|Le fil claque le bord, trop long.",
            "narrateur|L'eau part à côté, trop vite.",
            "narrateur|Une écaille de lichen colle au rebord.",
            "enfant-m|La corde est trop longue !",
            "narrateur|Il tire le fil, trop vite.",
            "papa|Ici, c'est trop bas.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Le sourire de Nino s'en va.",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois l'écaille, au bord ?",
            "narrateur|Nino arrête de tirer.",
            "maman|L'écaille montre où poser le fil.",
        ],
    },
    (3, 3): {
        "sons": "corde,vrille",
        "emphasis": "treille",
        "passage": [
            "narrateur|La corde rêche s'enroule autour d'une vrille.",
            "narrateur|Près de la treille, la corde s'accroche.",
            "enfant-m|Je tire la corde, tout seul.",
            "narrateur|Une vrille de vigne tient le nœud.",
            "narrateur|Plus il tire, plus ça serre.",
            "narrateur|Une écaille de lichen brille sur la vrille.",
            "enfant-m|La corde ne descend plus !",
            "narrateur|Il tire plus fort, trop vite.",
            "narrateur|Le nœud devient un petit poing.",
            "papa|Ici, ça s'accroche trop.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "enfant-m|Alors on fait quoi ?",
            "maman|Tu vois l'écaille, sur la vrille ?",
            "narrateur|Nino lâche, sans tirer.",
        ],
    },
}

T3_LABS = {
    1: ("le seau rond", "tenir le mince", "attendre"),
    2: ("à deux", "la corde", "poser le rond"),
    3: ("décrocher", "attendre", "à deux"),
}

T3_CHOICE = {
    1: [
        "narrateur|La margelle n'a pas fini de glisser.",
        "papa|Le seau rond, tenir le mince, ou attendre ?",
    ],
    2: [
        "narrateur|L'auge n'a pas fini d'être basse.",
        "maman|À deux, la corde, ou poser le rond ?",
    ],
    3: [
        "narrateur|La corde n'a pas fini de s'accrocher.",
        "papa|Décrocher, attendre, ou à deux ?",
    ],
}

T3_SONS = {
    (1, 1): "bois,pierre",
    (1, 2): "zinc,mains",
    (1, 3): "goutte,mousse",
    (2, 1): "deux-mains,eau",
    (2, 2): "corde,nœud",
    (2, 3): "bois,auge",
    (3, 1): "vrille,doigt",
    (3, 2): "silence,vigne",
    (3, 3): "deux-mains,treille",
}

T3_EMPH = {
    1: {1: "seau rond", 2: "mince", 3: "écaille de lichen"},
    2: {1: "à deux", 2: "corde", 3: "seau rond"},
    3: {1: "décrocher", 2: "écaille de lichen", 3: "à deux"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|Le seau rond, d'abord.",
        "narrateur|Nino pose le bois sur la pierre sèche.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle n'est pas sur la mousse glissante.",
        "enfant-m|Papa, tu tiens l'anse avec moi ?",
        "papa|Oui, on pose, on ne tire pas.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Le seau rond tient, large.",
        "maman|Le mince attend, contre lui.",
        "enfant-m|Toi, tu restes droit.",
        "narrateur|L'eau tremble, sans verser.",
        "narrateur|L'écaille de lichen reste au bord.",
    ],
    (1, 1, 2): [
        "enfant-m|Je tiens le mince.",
        "narrateur|Ses deux mains serrent le zinc.",
        "narrateur|Le bois reste, tout seul, large.",
        "enfant-m|Maman, tu regardes le rond ?",
        "maman|Oui, je le garde.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle glisse hors du zinc, lente.",
        "papa|Tu l'as tenu, tout près.",
        "enfant-m|Tu ne glisses plus.",
        "narrateur|Le mince se redresse, froid.",
        "narrateur|Deux formes, une même eau.",
    ],
    (1, 1, 3): [
        "enfant-m|On attend un peu.",
        "narrateur|Nino tient le bois, sans bouger.",
        "narrateur|Une goutte quitte la mousse, puis plus.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle sèche, et la pierre tient.",
        "papa|La mousse s'est tue, maintenant.",
        "enfant-m|Papa, tu poses avec moi ?",
        "papa|Oui, après la goutte.",
        "narrateur|Nino refuse de foncer.",
        "maman|Tu as laissé la pierre se calmer.",
        "enfant-m|Maintenant, ça tient.",
        "narrateur|Le seau rond s'assoit, large.",
    ],
    (1, 2, 1): [
        "enfant-m|À deux, on verse.",
        "narrateur|Papa tient le seau rond, large.",
        "enfant-m|Moi, je guide le mince.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle marque le rebord, juste.",
        "papa|On verse là, au trait gris.",
        "narrateur|L'eau tombe dans l'auge, droite.",
        "maman|Le rond tient, le mince verse.",
        "enfant-m|Les deux, ensemble.",
        "papa|Tes mains ont aidé les miennes.",
        "narrateur|L'écaille de lichen reste mouillée.",
    ],
    (1, 2, 2): [
        "enfant-m|La corde, pour descendre.",
        "narrateur|Nino noue la corde au seau rond.",
        "enfant-m|Papa, tu tiens le fil avec moi ?",
        "papa|Oui, on descend, sans jeter.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle colle au rebord, comme un cran.",
        "narrateur|Le bois descend, sans pencher.",
        "maman|Le mince suit, tenu par le nœud.",
        "enfant-m|Tu vas jusqu'en bas.",
        "papa|La corde a gardé les deux.",
        "narrateur|L'écaille de lichen guide le nœud.",
    ],
    (1, 2, 3): [
        "enfant-m|On pose le rond, d'abord.",
        "narrateur|Le seau rond s'assoit dans l'auge.",
        "enfant-m|Maman, tu le tiens droit ?",
        "maman|Oui, je le reçois.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle brille au fond du bois.",
        "narrateur|Nino y verse le mince, lent.",
        "papa|Le rond fait bassine, un moment.",
        "enfant-m|Toi, tu reçois.",
        "maman|Le mince a pu pencher, sans perdre.",
        "narrateur|L'écaille de lichen tremble au fond.",
    ],
    (1, 3, 1): [
        "enfant-m|On décroche, d'abord.",
        "narrateur|Nino glisse la corde hors de la vrille.",
        "enfant-m|Papa, tu lèves la feuille ?",
        "papa|Oui, doigt par doigt.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle montre le vrai crochet, gris.",
        "narrateur|Le seau rond redescend, lourd.",
        "maman|La vigne a lâché, toute seule.",
        "enfant-m|Tu es libre, corde.",
        "papa|Tu n'as pas tiré trop fort.",
        "narrateur|L'écaille de lichen reste sur la vrille.",
    ],
    (1, 3, 2): [
        "enfant-m|On attend la vigne.",
        "narrateur|Nino tient le bois, sans tirer.",
        "narrateur|La vrille va, revient, puis lâche.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle tremble, puis se tait.",
        "papa|La treille n'a plus accroché.",
        "enfant-m|Maintenant, tu descends.",
        "maman|Tu as laissé la vigne finir.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Le seau rond pend, enfin droit.",
        "papa|On descend, après le silence.",
        "narrateur|L'écaille de lichen reste crochue.",
    ],
    (1, 3, 3): [
        "enfant-m|À deux, on libère.",
        "narrateur|Papa lève la vrille, Nino le bois.",
        "enfant-m|Tu lèves, je glisse.",
        "papa|Oui, sans tirer fort.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle glisse hors de la vrille.",
        "narrateur|Le seau rond passe, puis le mince.",
        "maman|Le rond et le mince, ensemble.",
        "enfant-m|Vous deux, vous descendez.",
        "papa|Tes mains ont glissé, les miennes ont levé.",
        "narrateur|L'écaille de lichen voyage au bois.",
    ],
    (2, 1, 1): [
        "enfant-m|Le seau rond, sous le zinc.",
        "narrateur|Nino pose le bois sur la pierre sèche.",
        "enfant-m|Papa, tu tiens le mince ?",
        "papa|Oui, on pose le rond d'abord.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle n'est plus sous le zinc.",
        "narrateur|Le zinc s'assoit sur le bois, calme.",
        "maman|Le rond a une assise, voilà.",
        "enfant-m|Toi, tu ne penches plus.",
        "papa|Le mince a trouvé le rond.",
        "narrateur|L'écaille de lichen reste au bois.",
    ],
    (2, 1, 2): [
        "enfant-m|Je tiens le mince.",
        "narrateur|Ses deux mains serrent le zinc.",
        "enfant-m|Maman, tu prends l'autre bord ?",
        "maman|Oui, tout près.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle quitte le zinc, lente.",
        "narrateur|Le mince penche, puis se redresse.",
        "papa|Tu l'as tenu, tout près.",
        "enfant-m|Tu ne glisses plus.",
        "maman|Deux mains, un zinc.",
        "narrateur|L'écaille de lichen sèche sur la pierre.",
    ],
    (2, 1, 3): [
        "enfant-m|On attend un peu.",
        "narrateur|Nino tient le zinc, sans verser.",
        "narrateur|Une goutte quitte la mousse, puis plus.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle sèche, et le zinc tient.",
        "papa|La mousse s'est tue, maintenant.",
        "enfant-m|Papa, tu poses avec moi ?",
        "papa|Oui, après la goutte.",
        "narrateur|Nino refuse de foncer.",
        "maman|Tu as laissé la pierre se calmer.",
        "enfant-m|Maintenant, ça tient.",
        "narrateur|Le mince reste droit, froid.",
    ],
    (2, 2, 1): [
        "enfant-m|À deux, on verse.",
        "narrateur|Papa tient le zinc, trop mince.",
        "enfant-m|Moi, je montre le rebord.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle marque le rebord, juste.",
        "papa|On verse là, au trait gris.",
        "narrateur|L'eau tombe dans l'auge, droite.",
        "maman|Le mince verse, sans fuir.",
        "enfant-m|Les deux, ensemble.",
        "papa|Tes mains ont aidé les miennes.",
        "narrateur|L'écaille de lichen reste mouillée.",
    ],
    (2, 2, 2): [
        "enfant-m|La corde, pour descendre.",
        "narrateur|Nino noue la corde au zinc mince.",
        "enfant-m|Papa, tu tiens le fil avec moi ?",
        "papa|Oui, on descend, sans jeter.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle colle au rebord, comme un cran.",
        "narrateur|Le mince descend, tenu par le nœud.",
        "maman|Le bois suit, sans pencher.",
        "enfant-m|Tu vas jusqu'en bas.",
        "papa|La corde a gardé les deux.",
        "narrateur|L'écaille de lichen guide le nœud.",
    ],
    (2, 2, 3): [
        "enfant-m|On pose le rond, d'abord.",
        "narrateur|Le zinc attend, le bois s'assoit.",
        "enfant-m|Maman, tu reçois dans le rond ?",
        "maman|Oui, je le tiens.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle brille au fond du bois.",
        "narrateur|Nino y verse le mince, lent.",
        "papa|Le rond fait bassine, un moment.",
        "enfant-m|Toi, tu reçois.",
        "maman|Le mince a pu pencher, sans perdre.",
        "narrateur|L'écaille de lichen tremble au fond.",
    ],
    (2, 3, 1): [
        "enfant-m|On décroche, d'abord.",
        "narrateur|Le zinc se libère, puis la corde.",
        "enfant-m|Papa, tu lèves la feuille ?",
        "papa|Oui, doigt par doigt.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle montre le vrai crochet, gris.",
        "narrateur|Le mince penche, puis se calme.",
        "maman|La vigne a lâché, toute seule.",
        "enfant-m|Tu es libre, zinc.",
        "papa|Tu n'as pas tiré trop fort.",
        "narrateur|L'écaille de lichen reste sur la vrille.",
    ],
    (2, 3, 2): [
        "enfant-m|On attend la vigne.",
        "narrateur|Nino tient le zinc, sans tirer.",
        "narrateur|La vrille va, revient, puis lâche.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle tremble, puis se tait.",
        "papa|La treille n'a plus accroché.",
        "enfant-m|Maintenant, tu descends.",
        "maman|Tu as laissé la vigne finir.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Le mince pend, enfin droit.",
        "papa|On descend, après le silence.",
        "narrateur|L'écaille de lichen reste crochue.",
    ],
    (2, 3, 3): [
        "enfant-m|À deux, on libère.",
        "narrateur|Papa lève la vrille, Nino le zinc.",
        "enfant-m|Tu lèves, je glisse.",
        "papa|Oui, sans tirer fort.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle glisse hors de la vrille.",
        "narrateur|Le mince passe, puis le rond.",
        "maman|Le rond et le mince, ensemble.",
        "enfant-m|Vous deux, vous descendez.",
        "papa|Tes mains ont glissé, les miennes ont levé.",
        "narrateur|L'écaille de lichen voyage au zinc.",
    ],
    (3, 1, 1): [
        "enfant-m|Le seau rond, d'abord.",
        "narrateur|Nino pose la corde sur l'anse.",
        "enfant-m|Papa, tu tiens l'anse avec moi ?",
        "papa|Oui, on pose, on ne tire pas.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle n'est pas sur la mousse glissante.",
        "narrateur|Le seau rond tient, large.",
        "maman|Le mince attend, contre lui.",
        "enfant-m|Toi, tu restes droit.",
        "papa|Le rond a une assise, voilà.",
        "narrateur|L'écaille de lichen reste au bord.",
    ],
    (3, 1, 2): [
        "enfant-m|Je tiens le mince.",
        "narrateur|La corde l'aide à serrer le zinc.",
        "enfant-m|Maman, tu regardes le fil ?",
        "maman|Oui, je le garde lâche.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle glisse hors du zinc, lente.",
        "narrateur|Le mince penche, puis se redresse.",
        "papa|Tu l'as tenu, tout près.",
        "enfant-m|Tu ne glisses plus.",
        "maman|La corde a tenu, sans brûler.",
        "narrateur|L'écaille de lichen sèche sur la pierre.",
    ],
    (3, 1, 3): [
        "enfant-m|On attend un peu.",
        "narrateur|Nino tient la corde, sans tirer.",
        "narrateur|Une goutte quitte la mousse, puis plus.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle sèche, et la pierre tient.",
        "papa|La mousse s'est tue, maintenant.",
        "enfant-m|Papa, tu poses avec moi ?",
        "papa|Oui, après la goutte.",
        "narrateur|Nino refuse de foncer.",
        "maman|Tu as laissé la pierre se calmer.",
        "enfant-m|Maintenant, ça tient.",
        "narrateur|La corde pend, lâche, prête.",
    ],
    (3, 2, 1): [
        "enfant-m|À deux, on verse.",
        "narrateur|Papa tient la corde, Nino le bois.",
        "enfant-m|Moi, je guide le mince.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle marque le rebord, juste.",
        "papa|On verse là, au trait gris.",
        "narrateur|L'eau tombe dans l'auge, droite.",
        "maman|Le rond tient, le mince verse.",
        "enfant-m|Les deux, ensemble.",
        "papa|Tes mains ont aidé les miennes.",
        "narrateur|L'écaille de lichen reste mouillée.",
    ],
    (3, 2, 2): [
        "enfant-m|La corde, pour descendre.",
        "narrateur|Nino noue la corde, dans ses mains.",
        "enfant-m|Papa, tu tiens le fil avec moi ?",
        "papa|Oui, on descend, sans jeter.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle colle au rebord, comme un cran.",
        "narrateur|Le bois descend, sans pencher.",
        "maman|Le mince suit, tenu par le nœud.",
        "enfant-m|Tu vas jusqu'en bas.",
        "papa|La corde a gardé les deux.",
        "narrateur|L'écaille de lichen guide le nœud.",
    ],
    (3, 2, 3): [
        "enfant-m|On pose le rond, d'abord.",
        "narrateur|La corde lâche, le bois s'assoit.",
        "enfant-m|Maman, tu le tiens droit ?",
        "maman|Oui, je le reçois.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle brille au fond du bois.",
        "narrateur|Nino y verse le mince, lent.",
        "papa|Le rond fait bassine, un moment.",
        "enfant-m|Toi, tu reçois.",
        "maman|Le mince a pu pencher, sans perdre.",
        "narrateur|L'écaille de lichen tremble au fond.",
    ],
    (3, 3, 1): [
        "enfant-m|On décroche, d'abord.",
        "narrateur|Nino glisse la corde, doigt par doigt.",
        "enfant-m|Papa, tu lèves la feuille ?",
        "papa|Oui, doigt par doigt.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle montre le vrai crochet, gris.",
        "narrateur|Le seau rond redescend, lourd.",
        "maman|La vigne a lâché, toute seule.",
        "enfant-m|Tu es libre, corde.",
        "papa|Tu n'as pas tiré trop fort.",
        "narrateur|L'écaille de lichen reste sur la vrille.",
    ],
    (3, 3, 2): [
        "enfant-m|On attend la vigne.",
        "narrateur|Nino tient la corde, sans tirer.",
        "narrateur|La vrille va, revient, puis lâche.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle tremble, puis se tait.",
        "papa|La treille n'a plus accroché.",
        "enfant-m|Maintenant, tu descends.",
        "maman|Tu as laissé la vigne finir.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Le seau rond pend, enfin droit.",
        "papa|On descend, après le silence.",
        "narrateur|L'écaille de lichen reste crochue.",
    ],
    (3, 3, 3): [
        "enfant-m|À deux, on libère.",
        "narrateur|Papa lève la vrille, Nino la corde.",
        "enfant-m|Tu lèves, je glisse.",
        "papa|Oui, sans tirer fort.",
        "narrateur|Nino refuse de foncer.",
        "narrateur|Il cherche l'écaille de lichen.",
        "narrateur|Elle glisse hors de la vrille.",
        "narrateur|Le seau rond passe, puis le mince.",
        "maman|Le rond et le mince, ensemble.",
        "enfant-m|Vous deux, vous descendez.",
        "papa|Tes mains ont glissé, les miennes ont levé.",
        "narrateur|L'écaille de lichen voyage au fil.",
    ],
}

END_SONS = {1: "bassine,pierre", 2: "bassine,eau", 3: "bassine,vigne"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|L'eau tremble dans la bassine.",
        "enfant-m|On a posé le seau rond.",
        "papa|Le rond a tenu, sur la pierre.",
        "maman|On rentre, maintenant.",
        "enfant-m|Ça a failli glisser.",
        "papa|Puis tu as posé, sans tirer.",
        "narrateur|Nino touche l'anse, mouillée.",
        "narrateur|La bassine sent le puits, froide.",
        "narrateur|Sur le bois, l'écaille de lichen sèche, plate.",
    ],
    (1, 1, 2): [
        "narrateur|Dans la bassine, l'eau fait un rond.",
        "enfant-m|J'ai tenu le mince.",
        "papa|Tu l'as tenu, tout près.",
        "maman|Essuie tes mains, on rentre.",
        "enfant-m|Ça a failli pencher.",
        "maman|Puis tu as serré, avec moi.",
        "narrateur|Le zinc reste froid, contre sa jambe.",
        "narrateur|Une ligne d'eau brille, prête.",
        "narrateur|Au zinc, l'écaille de lichen fait un clic.",
    ],
    (1, 1, 3): [
        "narrateur|L'eau est arrivée, froide.",
        "enfant-m|On a attendu la pierre.",
        "papa|La mousse s'est tue.",
        "maman|La bassine est pleine, on rentre.",
        "enfant-m|Ça a failli partir.",
        "papa|Puis tu as attendu la goutte.",
        "narrateur|Le seau rond sèche, une goutte au fond.",
        "narrateur|Nino pose l'anse, sans tirer.",
        "narrateur|La margelle garde l'écaille de lichen, pâle.",
    ],
    (1, 2, 1): [
        "narrateur|La bassine reçoit l'eau, un peu froide.",
        "enfant-m|On a versé à deux.",
        "papa|Tes mains ont aidé.",
        "maman|Le rond et le mince, tous les deux.",
        "enfant-m|Ça a failli aller à côté.",
        "papa|Puis tu as montré le trait gris.",
        "narrateur|Le seau rond sèche, une goutte au fond.",
        "narrateur|L'auge garde une flaque, tout bas.",
        "narrateur|Dans l'auge, l'écaille de lichen tourne, lente.",
    ],
    (1, 2, 2): [
        "narrateur|De l'auge, l'eau rejoint la bassine.",
        "enfant-m|La corde a descendu les deux.",
        "papa|La corde a gardé les deux.",
        "maman|On rentre, tes doigts sont froids.",
        "enfant-m|Ça a failli se jeter.",
        "maman|Puis tu as noué, avec papa.",
        "narrateur|Un brin de corde reste mouillé.",
        "narrateur|Le seau rond sèche, une goutte au fond.",
        "narrateur|Un brin mouillé porte l'écaille de lichen.",
    ],
    (1, 2, 3): [
        "narrateur|Le seau rond a versé, lent.",
        "enfant-m|Il a reçu le mince.",
        "papa|Le rond a fait bassine.",
        "maman|Vos manches sentent l'eau.",
        "enfant-m|Ça a failli rater le bord.",
        "papa|Puis tu as posé le bois.",
        "narrateur|Le seau rond sèche, une goutte au fond.",
        "narrateur|L'auge se tait, plus loin, trop basse.",
        "narrateur|Au fond du rond, l'écaille de lichen brille.",
    ],
    (1, 3, 1): [
        "narrateur|Quand la corde a lâché, l'eau a monté.",
        "enfant-m|On a décroché la vrille.",
        "papa|Tu n'as pas tiré trop fort.",
        "maman|La bassine tremble, on rentre.",
        "enfant-m|Ça a failli se serrer.",
        "maman|Puis tu as glissé, doigt par doigt.",
        "narrateur|Le seau rond sèche, une goutte au fond.",
        "narrateur|Une feuille de vigne reste, trop verte.",
        "narrateur|La vrille garde l'écaille de lichen, crochue.",
    ],
    (1, 3, 2): [
        "narrateur|Quand la vigne s'est tue, l'eau a monté.",
        "enfant-m|On a attendu la treille.",
        "papa|La treille n'a plus accroché.",
        "maman|Tes doigts sentent la corde.",
        "enfant-m|Ça a failli rester coincé.",
        "papa|Puis tu as laissé la vrille finir.",
        "narrateur|Le seau rond sèche, une goutte au fond.",
        "narrateur|La vrille se recouche, lentement.",
        "narrateur|L'écaille de lichen tremble, puis se tait.",
    ],
    (1, 3, 3): [
        "narrateur|À deux, l'eau a rejoint la bassine.",
        "enfant-m|Papa a levé, j'ai glissé.",
        "papa|Tes mains ont glissé.",
        "maman|On rentre, la bassine est froide.",
        "enfant-m|Ça a failli rester là.",
        "maman|Puis vous avez levé, ensemble.",
        "narrateur|Le seau rond sèche, une goutte au fond.",
        "narrateur|La treille se tait, plus loin, toute seule.",
        "narrateur|Vers la maison, l'écaille de lichen voyage.",
    ],
    (2, 1, 1): [
        "narrateur|L'eau tremble dans la bassine.",
        "enfant-m|On a posé le rond sous le zinc.",
        "papa|Le mince a trouvé le bois.",
        "maman|On rentre, maintenant.",
        "enfant-m|Ça a failli glisser.",
        "papa|Puis tu as posé, sans tirer.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|La bassine sent le puits, froide.",
        "narrateur|Le zinc froid garde l'écaille de lichen.",
    ],
    (2, 1, 2): [
        "narrateur|Dans la bassine, l'eau fait un rond.",
        "enfant-m|J'ai tenu le mince.",
        "papa|Tu l'as tenu, tout près.",
        "maman|Essuie tes mains, on rentre.",
        "enfant-m|Ça a failli pencher.",
        "maman|Puis tu as serré, avec moi.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|Nino essuie le bord, sans verser.",
        "narrateur|Une ligne d'eau tient l'écaille de lichen.",
    ],
    (2, 1, 3): [
        "narrateur|L'eau est arrivée, froide.",
        "enfant-m|On a attendu la pierre.",
        "papa|La mousse s'est tue.",
        "maman|La bassine est pleine, on rentre.",
        "enfant-m|Ça a failli partir.",
        "papa|Puis tu as attendu la goutte.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|Nino pose le mince, droit.",
        "narrateur|Sur la mousse, l'écaille de lichen pâlit.",
    ],
    (2, 2, 1): [
        "narrateur|La bassine reçoit l'eau, un peu froide.",
        "enfant-m|On a versé à deux.",
        "papa|Tes mains ont aidé.",
        "maman|Le rond et le mince, tous les deux.",
        "enfant-m|Ça a failli aller à côté.",
        "papa|Puis tu as montré le trait gris.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|L'auge garde une flaque, tout bas.",
        "narrateur|L'auge reflète l'écaille de lichen, minuscule.",
    ],
    (2, 2, 2): [
        "narrateur|De l'auge, l'eau rejoint la bassine.",
        "enfant-m|La corde a descendu les deux.",
        "papa|La corde a gardé les deux.",
        "maman|On rentre, tes doigts sont froids.",
        "enfant-m|Ça a failli se jeter.",
        "maman|Puis tu as noué, avec papa.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|Un nœud reste mouillé, contre le zinc.",
        "narrateur|La corde rêche porte l'écaille de lichen.",
    ],
    (2, 2, 3): [
        "narrateur|Le seau rond a versé, lent.",
        "enfant-m|Il a reçu le mince.",
        "papa|Le rond a fait bassine.",
        "maman|Vos manches sentent l'eau.",
        "enfant-m|Ça a failli rater le bord.",
        "papa|Puis tu as posé le bois.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|L'auge se tait, plus loin, trop basse.",
        "narrateur|Le rond de bois abrite l'écaille de lichen.",
    ],
    (2, 3, 1): [
        "narrateur|Quand la corde a lâché, l'eau a monté.",
        "enfant-m|On a décroché la vrille.",
        "papa|Tu n'as pas tiré trop fort.",
        "maman|La bassine tremble, on rentre.",
        "enfant-m|Ça a failli se serrer.",
        "maman|Puis tu as glissé, doigt par doigt.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|Une feuille de vigne reste, trop verte.",
        "narrateur|Une feuille de vigne cache l'écaille de lichen.",
    ],
    (2, 3, 2): [
        "narrateur|Quand la vigne s'est tue, l'eau a monté.",
        "enfant-m|On a attendu la treille.",
        "papa|La treille n'a plus accroché.",
        "maman|Tes doigts sentent la corde.",
        "enfant-m|Ça a failli rester coincé.",
        "papa|Puis tu as laissé la vrille finir.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|La vrille se recouche, lentement.",
        "narrateur|La vrille lâche l'écaille de lichen, lente.",
    ],
    (2, 3, 3): [
        "narrateur|À deux, l'eau a rejoint la bassine.",
        "enfant-m|Papa a levé, j'ai glissé.",
        "papa|Tes mains ont glissé.",
        "maman|On rentre, la bassine est froide.",
        "enfant-m|Ça a failli rester là.",
        "maman|Puis vous avez levé, ensemble.",
        "narrateur|Le zinc reste froid, une ligne d'eau.",
        "narrateur|La treille se tait, plus loin, toute seule.",
        "narrateur|Papa porte l'écaille de lichen, au zinc.",
    ],
    (3, 1, 1): [
        "narrateur|L'eau tremble dans la bassine.",
        "enfant-m|On a posé le seau rond.",
        "papa|Le rond a tenu, sur la pierre.",
        "maman|On rentre, maintenant.",
        "enfant-m|Ça a failli glisser.",
        "papa|Puis tu as posé, sans tirer.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|La bassine sent le puits, froide.",
        "narrateur|Un tour de corde serre l'écaille de lichen.",
    ],
    (3, 1, 2): [
        "narrateur|Dans la bassine, l'eau fait un rond.",
        "enfant-m|J'ai tenu le mince.",
        "papa|Tu l'as tenu, tout près.",
        "maman|Essuie tes mains, on rentre.",
        "enfant-m|Ça a failli pencher.",
        "maman|Puis tu as serré, avec moi.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|Nino lâche le fil, sans brûler.",
        "narrateur|L'écaille de lichen glisse le long du fil.",
    ],
    (3, 1, 3): [
        "narrateur|L'eau est arrivée, froide.",
        "enfant-m|On a attendu la pierre.",
        "papa|La mousse s'est tue.",
        "maman|La bassine est pleine, on rentre.",
        "enfant-m|Ça a failli partir.",
        "papa|Puis tu as attendu la goutte.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|Nino pose le fil, lâche.",
        "narrateur|La pierre sèche tient l'écaille de lichen.",
    ],
    (3, 2, 1): [
        "narrateur|La bassine reçoit l'eau, un peu froide.",
        "enfant-m|On a versé à deux.",
        "papa|Tes mains ont aidé.",
        "maman|Le rond et le mince, tous les deux.",
        "enfant-m|Ça a failli aller à côté.",
        "papa|Puis tu as montré le trait gris.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|L'auge garde une flaque, tout bas.",
        "narrateur|Deux mains ont laissé l'écaille de lichen.",
    ],
    (3, 2, 2): [
        "narrateur|De l'auge, l'eau rejoint la bassine.",
        "enfant-m|La corde a descendu les deux.",
        "papa|La corde a gardé les deux.",
        "maman|On rentre, tes doigts sont froids.",
        "enfant-m|Ça a failli se jeter.",
        "maman|Puis tu as noué, avec papa.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|Un nœud reste mouillé, contre le zinc.",
        "narrateur|Le nœud garde l'écaille de lichen, rêche.",
    ],
    (3, 2, 3): [
        "narrateur|Le seau rond a versé, lent.",
        "enfant-m|Il a reçu le mince.",
        "papa|Le rond a fait bassine.",
        "maman|Vos manches sentent l'eau.",
        "enfant-m|Ça a failli rater le bord.",
        "papa|Puis tu as posé le bois.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|L'auge se tait, plus loin, trop basse.",
        "narrateur|L'auge basse montre l'écaille de lichen.",
    ],
    (3, 3, 1): [
        "narrateur|Quand la corde a lâché, l'eau a monté.",
        "enfant-m|On a décroché la vrille.",
        "papa|Tu n'as pas tiré trop fort.",
        "maman|La bassine tremble, on rentre.",
        "enfant-m|Ça a failli se serrer.",
        "maman|Puis tu as glissé, doigt par doigt.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|Une feuille de vigne reste, trop verte.",
        "narrateur|Le doigt de Nino a l'écaille de lichen.",
    ],
    (3, 3, 2): [
        "narrateur|Quand la vigne s'est tue, l'eau a monté.",
        "enfant-m|On a attendu la treille.",
        "papa|La treille n'a plus accroché.",
        "maman|Tes doigts sentent la corde.",
        "enfant-m|Ça a failli rester coincé.",
        "papa|Puis tu as laissé la vrille finir.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|La vrille se recouche, lentement.",
        "narrateur|Le silence garde l'écaille de lichen, grise.",
    ],
    (3, 3, 3): [
        "narrateur|À deux, l'eau a rejoint la bassine.",
        "enfant-m|Papa a levé, j'ai glissé.",
        "papa|Tes mains ont glissé.",
        "maman|On rentre, la bassine est froide.",
        "enfant-m|Ça a failli rester là.",
        "maman|Puis vous avez levé, ensemble.",
        "narrateur|La corde pend, rêche, mouillée.",
        "narrateur|Nino lâche le fil, sans tirer.",
        "narrateur|La treille se tait, l'écaille de lichen aussi.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "puits,mousse,corde"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("le seau rond", "le seau mince", "la corde")},
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
                "narrateur|Devant, la margelle est trop glissante.",
                "narrateur|L'auge, elle, est trop basse.",
                "narrateur|Près de la treille, la corde s'accroche.",
                "papa|Nino, tu vas où ?",
            ],
            "choice",
            "",
            {"fields": t3lab("la margelle", "l'auge", "la treille")},
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
                    {"emphasis": "écaille de lichen"},
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
        "plus rond ou plus mince",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "il faut attendre",
        "il faut demander",
        "on doit demander",
        "pommier",
        "canard",
        "pain chaud",
        "cheval",
        "auvent",
        "veau",
        "étable",
        "abreuvoir",
        "lampe",
        "capitaine",
        "plic",
        "volet jaune",
        "dînette",
        "dinette",
        "sami",
        "cuisine",
        "chambre",
        "pull",
        "arrosoir",
        "dalle",
        "la serre",
        "merle",
        "miel",
        "tout doux",
        "tout calme",
        "aujourd'hui",
        "nina",
        "amir",
        "aniss",
        "raphaël",
        "chouchou",
        "mila",
        "victorino",
        "victorina",
        "sarah",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "puits" not in blob:
        raise SystemExit(f"{SID}: puits absent")
    if "écaille de lichen" not in blob:
        raise SystemExit(f"{SID}: écaille de lichen absente")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
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
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")
    if len(story["chunks"]) != 86:
        raise SystemExit(f"chunks {len(story['chunks'])}≠86")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.COR.002 — demander / attendre l'aide, pas tirer tout seul "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Nino, papa, maman (un seul enfant)\n"
        "- **Lieu :** puits du village : mousse, margelle, auge, treille\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "D'habitude le puits cliquette. Cet après-midi, il se tait. Un souffle froid "
        "sort de la pierre. Une **écaille de lichen** grise colle à la corde. "
        "Nino veut remonter de l'eau pour la bassine de maman, **maintenant**. "
        "Il tire tout seul : la corde refuse, le seau tape en bas. Sourire parti. "
        "Il prend le seau rond, le seau mince ou la corde ; les trois partent. "
        "Margelle glissante, auge trop basse, treille qui accroche. "
        "Deuxième ruse : l'écaille glisse, montre le vrai endroit. Il refuse de foncer. "
        "Neuf façons : poser le rond, tenir le mince, attendre ; à deux, la corde, "
        "poser le rond ; décrocher, attendre, à deux. L'eau arrive. L'écaille voyage. "
        "Monde ≠ TREE-DIF-006 (arrosoirs, dalles), ≠ TREE-DIF-065 (serre, arrosoirs).\n\n"
        "## Vécu\n\n"
        "Nino veut l'eau **maintenant**. Il tire tout seul, ça résiste. "
        "Sourire disparu, poitrine bousculée, adulte accroupi. Personne ne donne "
        "la réponse. Il observe l'objet, écoute le puits, retrouve l'écaille du début. "
        "La leçon se voit : lâcher, demander, attendre, faire à deux. "
        "Le dénouement a failli (glisser, pencher, coincer). L'écaille paie l'ouverture. "
        "Chaque fin porte une trace unique.\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Plus rond ou plus mince », pommier, merle, miel, tics jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Pas de 2e enfant (xlsx : Nino, papa, maman seulement).\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'obstacle. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : l'écaille de lichen, payée au climax.\n"
        "- Merci vécu (maman : tu as lâché la corde). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
