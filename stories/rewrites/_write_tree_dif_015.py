#!/usr/bin/env python3
"""TREE-DIF-015 — Le drap du salon et les deux peluches (N3, DIF.COR.002, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-015"
N3 = 16
TITLE = "Le drap du salon et les deux peluches"
FIL = (
    "Au campement du salon, un grain de parquet luit sur une latte. "
    "Nino veut une tente pour l'ours rond et le lapin mince, maintenant, "
    "avant la soupe. Il jette trop vite, seul : le tissu glisse. "
    "Il prend le drap, la pince ou la lampe ; les trois partent. "
    "Sous la table, derrière le canapé ou dans le couloir, ça résiste. "
    "Il refuse de foncer, retrouve le grain, demande. "
    "Neuf façons d'attendre l'aide. Les deux peluches restent ensemble."
)
CHARS = "Nino, papa, maman"
SETTING = "salon, fin d'après-midi, à la maison"
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
    "gouttes au bord",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
FORBIDDEN_CLUES = (
    "étoile brune",
    "fil pâle",
    "virgule farine",
    "bouton nacre",
    "nœud raphia",
    "pois ivoire",
    "grain savon",
    "grain vanille",
    "pastille colle",
    "virgule de buée",
    "virgule buée",
    "grain doré",
    "brin safran",
    "anneau liège",
    "grain d'ambre",
    "larme de bronze",
    "point de cire",
    "grain d'ocre",
    "grain de feutre",
    "grain de sève",
    "point de beurre",
    "grain de sel",
    "cristal de sucre brun",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de parquet",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=nino_veut_la_tente_maintenant_le_grain_luit; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent_avec_lui; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_jette_seul_le_tissu_glisse; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_découragement; intensite=2; destinataire=enfant; sous_texte=l_objet_resiste_il_veut_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de parquet",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_grain_et_la_demande_sans_forcer_seul; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de parquet",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_paie_le_debut_les_peluches_restent; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N3:
            raise SystemExit(f"{where} {n}>{N3}: {ph}")
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
                    raise SystemExit(f"{where} puces « {tok} »")
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


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=le_grain_paie_le_debut_les_peluches_dorment; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = [
    "narrateur|Papa plie le journal, trop vite.",
    "narrateur|Un coussin tombe du canapé, sans un bruit.",
    "enfant-m|Je le remets.",
    "papa|Merci, tu as posé le coussin.",
    "narrateur|Une mouche marche sur l'abat-jour.",
    "narrateur|Ça sent la soupe, depuis la cuisine.",
    "narrateur|Le parquet sent le bois chaud, sous les pieds.",
    "narrateur|Sur une latte, un grain de parquet luit.",
    "enfant-m|Il fait une petite porte.",
    "maman|La lumière le touche, Nino.",
    "narrateur|L'ours rond attend sur le tapis rêche.",
    "narrateur|Le lapin mince a une oreille trop longue.",
    "narrateur|En ce moment, Nino veut une tente pour eux.",
    "enfant-m|C'est le campement du salon.",
    "papa|Avant la soupe, alors.",
    "maman|Le drap, la pince, et la lampe.",
    "enfant-m|Ils dorment ensemble, les deux.",
]

T1_CHOICE = [
    "narrateur|Près du tapis, trois affaires attendent.",
    "narrateur|Le drap, la pince, et la lampe.",
    "narrateur|Elles vont au campement, toutes les trois.",
    "papa|Tu prends quoi d'abord, Nino ?",
]

T1 = {
    1: {
        "lab": "le drap",
        "sons": "tissu,drap",
        "emphasis": "drap",
        "passage": [
            "narrateur|Nino prend d'abord le drap, trop plié.",
            "enfant-m|Je le jette, sans vous.",
            "maman|Doucement, Nino.",
            "narrateur|Le tissu tombe, trop large, jusqu'au tapis.",
            "narrateur|L'ours fait une colline, trop ronde.",
            "narrateur|Le lapin fait une ligne, une oreille dehors.",
            "enfant-m|Ils ne se ressemblent pas.",
            "narrateur|Le drap glisse, et le grain de parquet disparaît.",
            "enfant-m|Il est parti !",
            "papa|La pince aussi, près du panier.",
            "narrateur|Maman tend la lampe, trop tiède.",
            "narrateur|Drap, pince et lampe restent avec lui.",
            "enfant-m|On les prend.",
            "papa|Le drap est à toi, là.",
        ],
        "question": [
            "narrateur|Nino a jeté le tissu sur les peluches.",
            "maman|Nino a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "le drap",
            "accepted_examples": "drap | le drap | un drap | le tissu | tissu",
            "retry_prompt": "Nino a jeté le tissu sur les peluches. Il a pris quoi ?",
        },
        "confirm": [
            "enfant-m|Le drap.",
            "papa|Oui.",
            "narrateur|Nino glisse la pince dans sa poche.",
            "maman|La lampe, je te la tends.",
            "enfant-m|Oui, maman.",
            "narrateur|Il prend l'ours d'un bras, le lapin de l'autre.",
            "papa|Les deux viennent.",
            "narrateur|Le drap traîne un peu, derrière lui.",
            "enfant-m|On cherche l'endroit.",
        ],
        "voy": "Un coin du drap frotte le parquet.",
    },
    2: {
        "lab": "la pince",
        "sons": "bois,pince",
        "emphasis": "pince",
        "passage": [
            "narrateur|Nino saisit d'abord la pince, dans le panier.",
            "enfant-m|Elle tient fort, sans vous.",
            "papa|C'est pour le coin du drap.",
            "narrateur|Le bois claque une fois, trop sec.",
            "narrateur|Il l'essaie sur un pli, trop vite.",
            "narrateur|Le ventre rond soulève le tissu.",
            "narrateur|L'oreille du lapin reste dehors, trop mince.",
            "enfant-m|Elle pince le drap, pas l'oreille.",
            "narrateur|Le grain de parquet se cache sous le pli.",
            "enfant-m|Je ne le vois plus.",
            "maman|Le drap attend sur la chaise.",
            "narrateur|Papa pose la lampe près du tapis.",
            "narrateur|Pince, drap et lampe restent avec lui.",
            "papa|La pince est à toi, là.",
        ],
        "question": [
            "narrateur|Le bois de la pince a claqué.",
            "papa|Nino a pris quoi, dans le panier ?",
        ],
        "qfields": {
            "expected_answer": "la pince",
            "accepted_examples": "pince | la pince | une pince | le bois",
            "retry_prompt": "Le bois a claqué. Nino a pris quoi ?",
        },
        "confirm": [
            "enfant-m|La pince.",
            "maman|Oui.",
            "narrateur|Il ramasse le drap, tout un nuage.",
            "papa|La lampe, dans l'autre main ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux peluches voyagent contre lui.",
            "maman|Les deux viennent avec toi.",
            "narrateur|La pince tape sa poche, à chaque pas.",
            "enfant-m|On va où, maintenant ?",
        ],
        "voy": "La pince tape sa poche, à chaque pas.",
    },
    3: {
        "lab": "la lampe",
        "sons": "clic,lampe",
        "emphasis": "lampe",
        "passage": [
            "narrateur|Nino allume d'abord la lampe, un clic.",
            "enfant-m|Ça fait un camp, sans vous.",
            "maman|Tu éclaires qui, d'abord ?",
            "narrateur|Un rond jaune tombe sur le tapis rêche.",
            "narrateur|Le rond passe sur le ventre de l'ours.",
            "narrateur|Puis il glisse sur l'oreille du lapin.",
            "enfant-m|Ils ne se ressemblent pas.",
            "narrateur|Le rond couvre le grain de parquet.",
            "enfant-m|La petite porte est partie.",
            "papa|Le drap attend, plié, sur la chaise.",
            "narrateur|Maman glisse la pince dans sa poche à lui.",
            "narrateur|Lampe, drap et pince restent avec lui.",
            "enfant-m|Je garde la lampe.",
            "papa|Le rond tremble un peu, dans sa main.",
        ],
        "question": [
            "narrateur|Un rond jaune est tombé sur le tapis.",
            "maman|Nino a allumé quoi ?",
        ],
        "qfields": {
            "expected_answer": "la lampe",
            "accepted_examples": "lampe | la lampe | une lampe | la lumière",
            "retry_prompt": "Un rond jaune est tombé. Nino a allumé quoi ?",
        },
        "confirm": [
            "enfant-m|La lampe.",
            "papa|Oui.",
            "narrateur|Maman lui passe le drap, trop plié.",
            "maman|La pince, dans la poche.",
            "enfant-m|Elle est là.",
            "narrateur|L'ours et le lapin avancent avec lui.",
            "papa|Les deux viennent.",
            "narrateur|Le rond de la lampe court sur le parquet.",
            "enfant-m|Il me faut un endroit.",
        ],
        "voy": "Le rond de la lampe court sur le parquet.",
    },
}

T2 = {
    (1, 1): {
        "sons": "bois,chaise",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|Un coin du drap frotte le parquet.",
            "narrateur|Ils s'accroupissent sous la table.",
            "narrateur|Le drap accroche un pied de chaise, puis lâche.",
            "enfant-m|Je le tends, sans vous.",
            "narrateur|L'ours bute contre un pied, trop rond.",
            "narrateur|Le lapin glisse de l'autre côté, trop mince.",
            "enfant-m|L'un reste, l'autre part.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ils n'ont pas la même forme.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, sous la table.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le bois, trop proche.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "tissu,canape",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|Un coin du drap frotte le parquet.",
            "narrateur|Derrière le canapé, ça sent le tissu.",
            "narrateur|Le drap s'accroche au pied de bois, et tire.",
            "enfant-m|Je pousse l'ours, sans vous.",
            "narrateur|Le ventre rond ne passe pas.",
            "narrateur|Le lapin, lui, disparaît dans la fente.",
            "enfant-m|Ce n'est pas juste.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Le passage est étroit, voilà tout.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, au pied du canapé.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le tissu, trop serré.",
            "maman|Tu les gardes comment, ensemble ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "air,couloir",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|Un coin du drap frotte le parquet.",
            "narrateur|Dans le couloir, un courant d'air passe.",
            "narrateur|Le drap se gonfle, comme une voile trop grande.",
            "enfant-m|La tente, ici, sans vous.",
            "narrateur|Le drap se lève, tout seul.",
            "narrateur|Le lapin tombe, trop léger.",
            "narrateur|L'ours reste, trop lourd, trop rond.",
            "enfant-m|Il est tombé !",
            "narrateur|Cette fois, Nino ne rit plus.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le vent a choisi, pas toi.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, sur le seuil.",
            "enfant-m|Je ne fonce pas.",
            "papa|Tu les rassembles comment ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "bois,pince",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|La pince tape sa poche, à chaque pas.",
            "narrateur|Ils s'accroupissent sous la table.",
            "narrateur|Nino pince un coin, trop vite, trop bas.",
            "enfant-m|Ça tient, sans vous.",
            "narrateur|L'ours bute contre un pied, trop rond.",
            "narrateur|Le lapin glisse de l'autre côté, trop mince.",
            "enfant-m|L'un reste, l'autre part.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ils n'ont pas la même forme.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, sous la pince.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le clic, trop sec.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "tissu,pince",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|La pince tape sa poche, à chaque pas.",
            "narrateur|Derrière le canapé, ça sent le tissu.",
            "narrateur|La pince cogne le bois, un petit toc.",
            "enfant-m|Je pousse l'ours, sans vous.",
            "narrateur|Le ventre rond ne passe pas.",
            "narrateur|Le lapin, lui, disparaît dans la fente.",
            "enfant-m|Ce n'est pas juste.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Le passage est étroit, voilà tout.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, près du toc.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le bois, trop dur.",
            "maman|Tu les gardes comment, ensemble ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "air,pince",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|La pince tape sa poche, à chaque pas.",
            "narrateur|Dans le couloir, un courant d'air passe.",
            "narrateur|Nino serre la pince, pour un coin qui vole.",
            "enfant-m|La tente, ici, sans vous.",
            "narrateur|Le drap se lève, tout seul.",
            "narrateur|Le lapin tombe, trop léger.",
            "narrateur|L'ours reste, trop lourd, trop rond.",
            "enfant-m|Il est tombé !",
            "narrateur|Cette fois, Nino ne rit plus.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le vent a choisi, pas toi.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, sous la pince.",
            "enfant-m|Je ne fonce pas.",
            "papa|Tu les rassembles comment ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "bois,lampe",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|Le rond de la lampe court sur le parquet.",
            "narrateur|Ils s'accroupissent sous la table.",
            "narrateur|La lampe éclaire les barreaux, trop proches.",
            "enfant-m|Je le tends, sans vous.",
            "narrateur|L'ours bute contre un pied, trop rond.",
            "narrateur|Le lapin glisse de l'autre côté, trop mince.",
            "enfant-m|L'un reste, l'autre part.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ils n'ont pas la même forme.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, dans le rond.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le clic, trop bas.",
            "maman|Tu vois comment, Nino ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "tissu,lampe",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|Le rond de la lampe court sur le parquet.",
            "narrateur|Derrière le canapé, ça sent le tissu.",
            "narrateur|La lampe montre un passage étroit, trop sombre.",
            "enfant-m|Je pousse l'ours, sans vous.",
            "narrateur|Le ventre rond ne passe pas.",
            "narrateur|Le lapin, lui, disparaît dans la fente.",
            "enfant-m|Ce n'est pas juste.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Le passage est étroit, voilà tout.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, dans le rond.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le tissu, trop sombre.",
            "maman|Tu les gardes comment, ensemble ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "air,lampe",
        "emphasis": "grain de parquet",
        "passage": [
            "narrateur|Le rond de la lampe court sur le parquet.",
            "narrateur|Dans le couloir, un courant d'air passe.",
            "narrateur|La lampe dessine deux ombres, l'une ronde.",
            "enfant-m|La tente, ici, sans vous.",
            "narrateur|Le drap se lève, tout seul.",
            "narrateur|Le lapin tombe, trop léger.",
            "narrateur|L'ours reste, trop lourd, trop rond.",
            "enfant-m|Il est tombé !",
            "narrateur|Cette fois, Nino ne rit plus.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le vent a choisi, pas toi.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "narrateur|Un grain de parquet luit, dans le rond.",
            "enfant-m|Je ne fonce pas.",
            "papa|Tu les rassembles comment ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
}

T3_LABS = {
    1: ("la porte", "plus petit", "la chaise"),
    2: ("la pince", "le poids", "dessus"),
    3: ("fermer", "dos à dos", "le train"),
}

T3_CHOICE = {
    1: [
        "narrateur|Sous la table, l'ours bute, le lapin glisse.",
        "papa|Une porte, plus petit, ou la chaise ?",
    ],
    2: [
        "narrateur|Derrière le canapé, le passage est étroit.",
        "maman|La pince, le poids, ou dessus ?",
    ],
    3: [
        "narrateur|Dans le couloir, le lapin est tombé.",
        "papa|Fermer, dos à dos, ou le train ?",
    ],
}

T3_SONS = {
    (1, 1): "tissu,porte",
    (1, 2): "tissu,pli",
    (1, 3): "chaise,bois",
    (2, 1): "pince,canape",
    (2, 2): "ours,poids",
    (2, 3): "canape,tissu",
    (3, 1): "porte,air",
    (3, 2): "peluches,dos",
    (3, 3): "train,tissu",
}

T3_EMPH = {
    1: {1: "porte", 2: "plus petit", 3: "chaise"},
    2: {1: "pince", 2: "poids", 3: "dessus"},
    3: {1: "fermer", 2: "dos à dos", 3: "train"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|Une porte, dans le drap.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu tiens le pan ?",
        "papa|Oui, je le tiens, tu guides.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet montre une latte sèche.",
        "maman|L'ours garde l'entrée, trop rond.",
        "narrateur|Le lapin entre, et s'assoit au fond.",
        "enfant-m|Tu surveilles, toi.",
        "papa|Deux places, une tente.",
        "maman|Tes mains ont demandé le pan.",
        "narrateur|Le grain de parquet reste sous le pli.",
    ],
    (1, 1, 2): [
        "enfant-m|Plus petit, le drap.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu plies avec moi ?",
        "maman|Oui, deux fois, contre le parquet.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet reste au milieu du pli.",
        "papa|La grotte devient étroite, plus basse.",
        "narrateur|L'ours s'assoit, le lapin se couche.",
        "enfant-m|Vous tenez, tous les deux.",
        "maman|Ils n'ont pas besoin d'être pareils.",
        "papa|Tes mains ont demandé le pli.",
        "narrateur|Le grain de parquet dort sous le drap plié.",
    ],
    (1, 1, 3): [
        "enfant-m|Sur la chaise, à côté.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu pousses la chaise ?",
        "papa|Oui, je la pousse, tu poses le drap.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet touche le pied de chaise.",
        "maman|L'ours et le lapin montent, l'un contre l'autre.",
        "narrateur|Le drap tombe du dossier, comme un toit.",
        "enfant-m|Un camp, plus haut.",
        "papa|La grotte reste vide, en dessous.",
        "maman|Tes mains ont demandé la chaise.",
        "narrateur|Le grain de parquet reste au pied de la chaise.",
    ],
    (1, 2, 1): [
        "enfant-m|La pince, sur le dossier.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu tiens le drap ?",
        "maman|Oui, je le tends, tu pinces.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet s'arrête au pied du canapé.",
        "papa|Ça fait clic, et le tissu tient.",
        "narrateur|L'ours s'assoit devant, trop large pour la fente.",
        "narrateur|Le lapin se glisse dans le pli.",
        "papa|Chacun a sa place.",
        "maman|Tes mains ont demandé le clic.",
        "narrateur|Le grain de parquet reste près du clic.",
    ],
    (1, 2, 2): [
        "enfant-m|L'ours, pour tenir le drap.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu poses l'ours ?",
        "papa|Oui, sur le coin, tu guides.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet porte un peu le poids.",
        "maman|Le tissu ne bouge plus.",
        "narrateur|Le lapin se couche dans le pli, trop mince.",
        "enfant-m|Tu es le mur, toi.",
        "papa|Et lui, le toit.",
        "maman|Tes mains ont demandé le poids.",
        "narrateur|Le grain de parquet tient sous le ventre rond.",
    ],
    (1, 2, 3): [
        "enfant-m|On monte dessus.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu m'aides à grimper ?",
        "maman|Oui, je te hisse, tu tires le drap.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet luit sur le dossier.",
        "papa|Le tissu devient une couverture, trop grande.",
        "narrateur|L'ours et le lapin s'installent au milieu.",
        "enfant-m|Plus besoin de la fente.",
        "papa|Vous êtes tous les trois, au chaud.",
        "maman|Tes mains ont demandé le dessus.",
        "narrateur|Le grain de parquet grimpe avec le pli.",
    ],
    (1, 3, 1): [
        "enfant-m|On ferme la porte.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu pousses la porte ?",
        "papa|Oui, je la pousse, sans claquer.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet s'arrête au seuil.",
        "maman|Le courant s'arrête.",
        "narrateur|Le drap retombe, comme un toit.",
        "narrateur|Nino rassied le lapin contre l'ours.",
        "papa|Plus de vent, plus de chute.",
        "maman|Tes mains ont demandé de fermer.",
        "narrateur|Le grain de parquet reste derrière la porte.",
    ],
    (1, 3, 2): [
        "enfant-m|Dos à dos.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu les tiens un moment ?",
        "maman|Oui, le rond contre le mince.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet se loge entre les deux dos.",
        "papa|Le drap passe par-dessus, un seul toit.",
        "narrateur|Le rond et le mince se tiennent.",
        "enfant-m|Vous ne tombez plus.",
        "papa|L'un calme l'autre.",
        "maman|Tes mains ont demandé les deux dos.",
        "narrateur|Le grain de parquet tient entre les deux dos.",
    ],
    (1, 3, 3): [
        "enfant-m|Un train, dans le drap.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu tiens le tunnel ?",
        "papa|Oui, je le tends, tu alignes.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet montre la direction du tapis.",
        "maman|L'ours rond est la locomotive.",
        "narrateur|Le lapin mince est le wagon.",
        "narrateur|Le drap fait un tunnel, au-dessus.",
        "enfant-m|On roule jusqu'au tapis.",
        "papa|Tes mains ont demandé le train.",
        "narrateur|Le grain de parquet suit le train de drap.",
    ],
    (2, 1, 1): [
        "enfant-m|Une porte, avec la pince.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu tiens le pan ?",
        "papa|Oui, je le tiens, tu pinces le bord.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet claque sous le bois.",
        "maman|L'ours garde l'entrée, trop rond.",
        "narrateur|Le lapin entre, et s'assoit au fond.",
        "enfant-m|Tu surveilles, toi.",
        "papa|Deux places, un clic.",
        "maman|Tes mains ont demandé le pan.",
        "narrateur|Le grain de parquet reste sous le clic.",
    ],
    (2, 1, 2): [
        "enfant-m|Plus petit, pincé deux fois.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu plies, je pince ?",
        "maman|Oui, deux fois, contre le parquet.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet reste entre deux plis.",
        "papa|La grotte devient étroite, plus basse.",
        "narrateur|L'ours s'assoit, le lapin se couche.",
        "enfant-m|Vous tenez, tous les deux.",
        "maman|La pince a fait le toit petit.",
        "papa|Tes mains ont demandé le pli.",
        "narrateur|Le grain de parquet dort sous la pince.",
    ],
    (2, 1, 3): [
        "enfant-m|La pince, sur la chaise.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu pousses la chaise ?",
        "papa|Oui, je la pousse, tu pinces le dossier.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet touche le pied de chaise.",
        "maman|L'ours et le lapin montent, l'un contre l'autre.",
        "narrateur|Le clic tient le drap, trop haut.",
        "enfant-m|Un camp, plus haut.",
        "papa|La grotte reste vide, en dessous.",
        "maman|Tes mains ont demandé la chaise.",
        "narrateur|Le grain de parquet luit sous la chaise pincée.",
    ],
    (2, 2, 1): [
        "enfant-m|La pince, sur le dossier.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu tends le tissu ?",
        "maman|Oui, je le tends, tu fais le clic.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet s'arrête au pied du canapé.",
        "papa|Le bois tient, trop net.",
        "narrateur|L'ours s'assoit devant, trop large pour la fente.",
        "narrateur|Le lapin se glisse dans le pli.",
        "papa|Chacun a sa place.",
        "maman|Tes mains ont demandé le clic.",
        "narrateur|Le grain de parquet garde la pince, trop près.",
    ],
    (2, 2, 2): [
        "enfant-m|L'ours, et la pince, pour le poids.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu poses l'ours ?",
        "papa|Oui, sur le coin, tu pinces après.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet porte un peu le poids.",
        "maman|Le tissu ne bouge plus.",
        "narrateur|Le lapin se couche dans le pli, trop mince.",
        "enfant-m|Tu es le mur, toi.",
        "papa|Et lui, le toit pincé.",
        "maman|Tes mains ont demandé le poids.",
        "narrateur|Le grain de parquet tient sous l'ours et la pince.",
    ],
    (2, 2, 3): [
        "enfant-m|On monte dessus, avec la pince.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu m'aides à grimper ?",
        "maman|Oui, je te hisse, tu pinces le dossier.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet luit sur le dossier.",
        "papa|Le clic tient le toit, trop haut.",
        "narrateur|L'ours et le lapin s'installent au milieu.",
        "enfant-m|Plus besoin de la fente.",
        "papa|Vous êtes tous les trois, au chaud.",
        "maman|Tes mains ont demandé le dessus.",
        "narrateur|Le grain de parquet grimpe avec la pince.",
    ],
    (2, 3, 1): [
        "enfant-m|On ferme, et on pince.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu pousses la porte ?",
        "papa|Oui, je la pousse, tu pinces le coin.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet s'arrête au seuil.",
        "maman|Le courant s'arrête.",
        "narrateur|Le drap retombe, pincé, comme un toit.",
        "narrateur|Nino rassied le lapin contre l'ours.",
        "papa|Plus de vent, plus de chute.",
        "maman|Tes mains ont demandé de fermer.",
        "narrateur|Le grain de parquet reste près de la pince fermée.",
    ],
    (2, 3, 2): [
        "enfant-m|Dos à dos, pincés ensemble.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu les tiens un moment ?",
        "maman|Oui, le rond contre le mince.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet se loge entre les deux dos.",
        "papa|La pince tient le toit, trop juste.",
        "narrateur|Le rond et le mince se tiennent.",
        "enfant-m|Vous ne tombez plus.",
        "papa|L'un calme l'autre.",
        "maman|Tes mains ont demandé les deux dos.",
        "narrateur|Le grain de parquet tient entre pince et dos.",
    ],
    (2, 3, 3): [
        "enfant-m|Un train, pincé au bout.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu tiens le tunnel ?",
        "papa|Oui, je le tends, tu pinces l'arrivée.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet montre la direction du tapis.",
        "maman|L'ours rond est la locomotive.",
        "narrateur|Le lapin mince est le wagon.",
        "narrateur|Le drap fait un tunnel, pincé au bout.",
        "enfant-m|On roule jusqu'au tapis.",
        "papa|Tes mains ont demandé le train.",
        "narrateur|Le grain de parquet roule jusqu'à la pince.",
    ],
    (3, 1, 1): [
        "enfant-m|Une porte, dans le rond.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu tiens le pan ?",
        "papa|Oui, je le tiens, tu éclaires.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet brille dans le rond.",
        "maman|L'ours garde l'entrée, trop rond.",
        "narrateur|Le lapin entre, et s'assoit au fond.",
        "enfant-m|Tu surveilles, toi.",
        "papa|Deux places, une lumière.",
        "maman|Tes mains ont demandé le pan.",
        "narrateur|Le grain de parquet reste dans le rond de lampe.",
    ],
    (3, 1, 2): [
        "enfant-m|Plus petit, sous le rond.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu plies, j'éclaire ?",
        "maman|Oui, deux fois, contre le parquet.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet reste au milieu du rond.",
        "papa|La grotte devient étroite, plus basse.",
        "narrateur|L'ours s'assoit, le lapin se couche.",
        "enfant-m|Vous tenez, tous les deux.",
        "maman|Le rond a fait le camp petit.",
        "papa|Tes mains ont demandé le pli.",
        "narrateur|Le grain de parquet dort dans le rond plié.",
    ],
    (3, 1, 3): [
        "enfant-m|La lampe, sur la chaise.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu pousses la chaise ?",
        "papa|Oui, je la pousse, tu poses la lampe.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet touche le pied de chaise.",
        "maman|L'ours et le lapin montent, l'un contre l'autre.",
        "narrateur|Le rond tombe du dossier, trop chaud.",
        "enfant-m|Un camp, plus haut.",
        "papa|La grotte reste vide, en dessous.",
        "maman|Tes mains ont demandé la chaise.",
        "narrateur|Le grain de parquet luit sous la chaise éclairée.",
    ],
    (3, 2, 1): [
        "enfant-m|La pince, dans le rond.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu tends le tissu ?",
        "maman|Oui, je le tends, tu éclaires le clic.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet s'arrête au pied du canapé.",
        "papa|Ça fait clic, et le rond tient.",
        "narrateur|L'ours s'assoit devant, trop large pour la fente.",
        "narrateur|Le lapin se glisse dans le pli.",
        "papa|Chacun a sa place.",
        "maman|Tes mains ont demandé le clic.",
        "narrateur|Le grain de parquet cligne dans le rond, au pied.",
    ],
    (3, 2, 2): [
        "enfant-m|L'ours, pour le poids, sous le rond.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu poses l'ours ?",
        "papa|Oui, sur le coin, tu éclaires.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet porte un peu le poids.",
        "maman|Le tissu ne bouge plus.",
        "narrateur|Le lapin se couche dans le pli, trop mince.",
        "enfant-m|Tu es le mur, toi.",
        "papa|Et lui, le toit éclairé.",
        "maman|Tes mains ont demandé le poids.",
        "narrateur|Le grain de parquet reste sous l'ours, dans le rond.",
    ],
    (3, 2, 3): [
        "enfant-m|On monte dessus, avec la lampe.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu m'aides à grimper ?",
        "maman|Oui, je te hisse, tu lèves le rond.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet luit sur le dossier.",
        "papa|Le tissu devient une couverture, trop grande.",
        "narrateur|L'ours et le lapin s'installent au milieu.",
        "enfant-m|Plus besoin de la fente.",
        "papa|Vous êtes tous les trois, au chaud.",
        "maman|Tes mains ont demandé le dessus.",
        "narrateur|Le grain de parquet monte sur le canapé, trop clair.",
    ],
    (3, 3, 1): [
        "enfant-m|On ferme, et j'éclaire.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu pousses la porte ?",
        "papa|Oui, je la pousse, tu gardes le rond.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet s'arrête au seuil.",
        "maman|Le courant s'arrête.",
        "narrateur|Le drap retombe, comme un toit.",
        "narrateur|Nino rassied le lapin contre l'ours.",
        "papa|Plus de vent, plus de chute.",
        "maman|Tes mains ont demandé de fermer.",
        "narrateur|Le grain de parquet s'arrête au seuil, dans le rond.",
    ],
    (3, 3, 2): [
        "enfant-m|Dos à dos, dans le rond.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Maman, tu les tiens un moment ?",
        "maman|Oui, le rond contre le mince.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet se loge entre les deux dos.",
        "papa|La lampe dessine deux ombres, collées.",
        "narrateur|Le rond et le mince se tiennent.",
        "enfant-m|Vous ne tombez plus.",
        "papa|L'un calme l'autre.",
        "maman|Tes mains ont demandé les deux dos.",
        "narrateur|Le grain de parquet reste entre deux ombres, trop rond.",
    ],
    (3, 3, 3): [
        "enfant-m|Un train, dans le rond.",
        "narrateur|Nino refuse de foncer.",
        "enfant-m|Papa, tu tiens le tunnel ?",
        "papa|Oui, je le tends, tu éclaires l'arrivée.",
        "narrateur|Il cherche le grain de parquet.",
        "narrateur|Le grain de parquet montre la direction du tapis.",
        "maman|L'ours rond est la locomotive.",
        "narrateur|Le lapin mince est le wagon.",
        "narrateur|Le drap fait un tunnel, au-dessus.",
        "enfant-m|On roule jusqu'au tapis.",
        "papa|Tes mains ont demandé le train.",
        "narrateur|Le grain de parquet arrive au tapis, dans le rond.",
    ],
}

END_SONS = {1: "table,bois", 2: "canape,tissu", 3: "couloir,porte"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|L'ours garde l'entrée, le ventre chaud.",
        "narrateur|Le lapin fait coucou, depuis le fond.",
        "enfant-m|Bonsoir, tous les deux.",
        "maman|Ta tente a une porte, maintenant.",
        "papa|Ça a failli glisser.",
        "enfant-m|Puis j'ai tendu le pan.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet garde un pli de drap, sous la table.",
    ],
    (1, 1, 2): [
        "narrateur|Sous la table, ça sent le bois et le linge.",
        "enfant-m|Je rentre aussi, un peu.",
        "narrateur|Ses genoux touchent l'ours, puis le lapin.",
        "papa|Il y a de la place, pour trois.",
        "maman|Ça a failli trop large.",
        "enfant-m|Puis on a plié.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet brille sous le drap plié, trop bas.",
    ],
    (1, 1, 3): [
        "narrateur|Sur la chaise, les deux peluches se touchent.",
        "enfant-m|Le camp est plus haut, ici.",
        "papa|La grotte attendra une autre fois.",
        "maman|Ils sont bien, l'un contre l'autre.",
        "enfant-m|Ça a failli trop bas.",
        "papa|Puis tu as demandé la chaise.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet reste au pied de la chaise, trop sec.",
    ],
    (1, 2, 1): [
        "narrateur|La pince tient, au dos du canapé.",
        "enfant-m|Clic, et ça reste.",
        "narrateur|L'ours regarde le salon, le lapin le pli.",
        "papa|Chacun voit un côté.",
        "maman|Ça a failli trop étroit.",
        "enfant-m|Puis j'ai demandé le clic.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet reste au pied du canapé, près du clic.",
    ],
    (1, 2, 2): [
        "narrateur|L'ours rond pèse sur le coin.",
        "narrateur|Le lapin respire, trop mince, dans le pli.",
        "enfant-m|Vous dormez ?",
        "papa|On parle plus bas, alors.",
        "maman|Le nid a tenu.",
        "enfant-m|Ça a failli trop bouger.",
        "papa|Puis tu as demandé le poids.",
        "narrateur|Le grain de parquet porte le poids de l'ours, trop rond.",
    ],
    (1, 2, 3): [
        "narrateur|Sur le canapé, le drap les couvre, trop grand.",
        "enfant-m|Moi aussi, je m'assois.",
        "narrateur|Trois silhouettes, sous le même tissu.",
        "papa|Le secret est devenu un lit.",
        "maman|Ça a failli trop serré.",
        "enfant-m|Puis j'ai demandé le dessus.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet luit sur le dossier, trop haut.",
    ],
    (1, 3, 1): [
        "narrateur|La porte fermée, le couloir n'a plus d'air.",
        "enfant-m|Le toit est retombé.",
        "narrateur|Le lapin s'appuie contre le ventre rond.",
        "papa|Plus personne ne tombe.",
        "maman|Ça a failli trop voler.",
        "enfant-m|Puis j'ai demandé de fermer.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet reste derrière la porte, trop immobile.",
    ],
    (1, 3, 2): [
        "narrateur|Dos à dos, le rond et le mince tiennent.",
        "enfant-m|Une tente, pour deux.",
        "papa|Ils n'ont pas la même ombre.",
        "maman|Et ils jouent quand même.",
        "enfant-m|Ça a failli trop léger.",
        "papa|Puis tu as demandé les deux dos.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet tient entre les deux dos, trop bas.",
    ],
    (1, 3, 3): [
        "narrateur|Le train arrive sur le tapis, trop lent.",
        "enfant-m|Terminus.",
        "narrateur|L'ours s'arrête, le lapin contre lui.",
        "papa|Vous avez voyagé ensemble.",
        "maman|Ça a failli trop loin.",
        "enfant-m|Puis j'ai demandé le train.",
        "narrateur|Un pli du drap reste tiède, contre l'ours.",
        "narrateur|Le grain de parquet suit le train de drap, trop loin.",
    ],
    (2, 1, 1): [
        "narrateur|L'ours garde l'entrée, le ventre chaud.",
        "narrateur|Le lapin fait coucou, depuis le fond.",
        "enfant-m|Bonsoir, tous les deux.",
        "maman|Ta tente a une porte, pincée.",
        "papa|Ça a failli trop bas.",
        "enfant-m|Puis j'ai pincé le pan.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet tient près du clic de pince, trop bas.",
    ],
    (2, 1, 2): [
        "narrateur|Sous la table, ça sent le bois et le clic.",
        "enfant-m|Je rentre aussi, un peu.",
        "narrateur|Ses genoux touchent l'ours, puis le lapin.",
        "papa|Il y a de la place, pour trois.",
        "maman|Ça a failli trop large.",
        "enfant-m|Puis on a pincé le pli.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet dort sous le drap plié, trop court.",
    ],
    (2, 1, 3): [
        "narrateur|Sur la chaise, les deux peluches se touchent.",
        "enfant-m|Le camp est plus haut, ici.",
        "papa|La grotte attendra une autre fois.",
        "maman|Ils sont bien, l'un contre l'autre.",
        "enfant-m|Ça a failli trop bas.",
        "papa|Puis tu as pincé la chaise.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet luit sous la chaise, un peu chaud.",
    ],
    (2, 2, 1): [
        "narrateur|La pince tient, au dos du canapé.",
        "enfant-m|Clic, et ça reste.",
        "narrateur|L'ours regarde le salon, le lapin le pli.",
        "papa|Chacun voit un côté.",
        "maman|Ça a failli trop étroit.",
        "enfant-m|Puis j'ai demandé le clic.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet garde la pince, trop près du bois.",
    ],
    (2, 2, 2): [
        "narrateur|L'ours rond pèse sur le coin.",
        "narrateur|Le lapin respire, trop mince, dans le pli.",
        "enfant-m|Vous dormez ?",
        "papa|On parle plus bas, alors.",
        "maman|Le nid a tenu, pincé.",
        "enfant-m|Ça a failli trop bouger.",
        "papa|Puis tu as demandé le poids.",
        "narrateur|Le grain de parquet tient sous le ventre de l'ours.",
    ],
    (2, 2, 3): [
        "narrateur|Sur le canapé, le drap les couvre, trop grand.",
        "enfant-m|Moi aussi, je m'assois.",
        "narrateur|Trois silhouettes, sous le même tissu.",
        "papa|Le secret est devenu un lit.",
        "maman|Ça a failli trop serré.",
        "enfant-m|Puis j'ai pincé le dessus.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet grimpe avec eux, sur le tissu.",
    ],
    (2, 3, 1): [
        "narrateur|La porte fermée, le couloir n'a plus d'air.",
        "enfant-m|Le toit est retombé.",
        "narrateur|Le lapin s'appuie contre le ventre rond.",
        "papa|Plus personne ne tombe.",
        "maman|Ça a failli trop voler.",
        "enfant-m|Puis j'ai pincé la porte.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet reste près de la pince, derrière la porte.",
    ],
    (2, 3, 2): [
        "narrateur|Dos à dos, le rond et le mince tiennent.",
        "enfant-m|Une tente, pour deux.",
        "papa|Ils n'ont pas la même ombre.",
        "maman|Et ils jouent quand même.",
        "enfant-m|Ça a failli trop léger.",
        "papa|Puis tu as pincé les deux dos.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet se loge entre l'ours et le lapin.",
    ],
    (2, 3, 3): [
        "narrateur|Le train arrive sur le tapis, trop lent.",
        "enfant-m|Terminus.",
        "narrateur|L'ours s'arrête, le lapin contre lui.",
        "papa|Vous avez voyagé ensemble.",
        "maman|Ça a failli trop loin.",
        "enfant-m|Puis j'ai pincé l'arrivée.",
        "narrateur|La pince repose près du pied de chaise.",
        "narrateur|Le grain de parquet roule jusqu'au tapis, avec le train.",
    ],
    (3, 1, 1): [
        "narrateur|L'ours garde l'entrée, le ventre chaud.",
        "narrateur|Le lapin fait coucou, depuis le fond.",
        "enfant-m|Bonsoir, tous les deux.",
        "maman|Ta tente a une porte, éclairée.",
        "papa|Ça a failli trop sombre.",
        "enfant-m|Puis j'ai levé le rond.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet brille dans le rond de lampe, trop court.",
    ],
    (3, 1, 2): [
        "narrateur|Sous la table, ça sent le bois et le chaud.",
        "enfant-m|Je rentre aussi, un peu.",
        "narrateur|Ses genoux touchent l'ours, puis le lapin.",
        "papa|Il y a de la place, pour trois.",
        "maman|Ça a failli trop large.",
        "enfant-m|Puis on a plié sous le rond.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet reste dans le rond, sous le pli.",
    ],
    (3, 1, 3): [
        "narrateur|Sur la chaise, les deux peluches se touchent.",
        "enfant-m|Le camp est plus haut, ici.",
        "papa|La grotte attendra une autre fois.",
        "maman|Ils sont bien, l'un contre l'autre.",
        "enfant-m|Ça a failli trop bas.",
        "papa|Puis tu as éclairé la chaise.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet touche le pied de chaise, trop clair.",
    ],
    (3, 2, 1): [
        "narrateur|La pince tient, au dos du canapé.",
        "enfant-m|Clic, et ça reste.",
        "narrateur|L'ours regarde le salon, le lapin le pli.",
        "papa|Chacun voit un côté.",
        "maman|Ça a failli trop étroit.",
        "enfant-m|Puis j'ai éclairé le clic.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet cligne dans le rond, au pied du canapé.",
    ],
    (3, 2, 2): [
        "narrateur|L'ours rond pèse sur le coin.",
        "narrateur|Le lapin respire, trop mince, dans le pli.",
        "enfant-m|Vous dormez ?",
        "papa|On parle plus bas, alors.",
        "maman|Le nid a tenu, éclairé.",
        "enfant-m|Ça a failli trop bouger.",
        "papa|Puis tu as éclairé le poids.",
        "narrateur|Le grain de parquet reste sous l'ours, dans le rond.",
    ],
    (3, 2, 3): [
        "narrateur|Sur le canapé, le drap les couvre, trop grand.",
        "enfant-m|Moi aussi, je m'assois.",
        "narrateur|Trois silhouettes, sous le même tissu.",
        "papa|Le secret est devenu un lit.",
        "maman|Ça a failli trop serré.",
        "enfant-m|Puis j'ai levé le rond.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet monte sur le canapé, trop clair.",
    ],
    (3, 3, 1): [
        "narrateur|La porte fermée, le couloir n'a plus d'air.",
        "enfant-m|Le toit est retombé.",
        "narrateur|Le lapin s'appuie contre le ventre rond.",
        "papa|Plus personne ne tombe.",
        "maman|Ça a failli trop voler.",
        "enfant-m|Puis j'ai éclairé le seuil.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet s'arrête au seuil, dans le rond.",
    ],
    (3, 3, 2): [
        "narrateur|Dos à dos, le rond et le mince tiennent.",
        "enfant-m|Une tente, pour deux.",
        "papa|Ils n'ont pas la même ombre.",
        "maman|Et ils jouent quand même.",
        "enfant-m|Ça a failli trop léger.",
        "papa|Puis tu as éclairé les deux dos.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet reste entre deux ombres, trop rond.",
    ],
    (3, 3, 3): [
        "narrateur|Le train arrive sur le tapis, trop lent.",
        "enfant-m|Terminus.",
        "narrateur|L'ours s'arrête, le lapin contre lui.",
        "papa|Vous avez voyagé ensemble.",
        "maman|Ça a failli trop loin.",
        "enfant-m|Puis j'ai éclairé l'arrivée.",
        "narrateur|Le rond de la lampe reste sur le tapis.",
        "narrateur|Le grain de parquet arrive au tapis, dans le rond.",
    ],
}


def t2_question(t1: int) -> list[str]:
    return [
        f"narrateur|{T1[t1]['voy']}",
        "narrateur|Les deux peluches attendent un camp.",
        "narrateur|Sous la table, l'ombre fait une grotte.",
        "narrateur|Derrière le canapé, ça sent le tissu.",
        "narrateur|Le grain de parquet attend, quelque part.",
        "papa|Sous la table, derrière le canapé, ou le couloir ?",
    ]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "journal,coussin",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le drap", "la pince", "la lampe")},
    )

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        out_chunks[p] = voice(by_src[p], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        out_chunks[f"{p}_Q0001"] = voice(
            by_src[f"{p}_Q0001"], t1["question"], "clue", "",
            {"emphasis": t1["emphasis"], "fields": t1["qfields"]},
        )
        out_chunks[f"{p}_C0001"] = voice(
            by_src[f"{p}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["emphasis"]},
        )
        out_chunks[f"{p}_T0002_P0000"] = voice(
            by_src[f"{p}_T0002_P0000"], t2_question(a), "choice", "",
            {"fields": t3lab("sous la table", "derrière le canapé", "dans le couloir")},
        )
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[sp] = voice(
                by_src[sp], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{sp}_T0003_P0000"] = voice(
                by_src[f"{sp}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[b],
                    {"emphasis": "grain de parquet", "notes": ending_note(a, b, c)},
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
        "sami",
        "léa",
        "lea ",
        "tom ",
        "capitaine",
        "merle",
        "miel",
        "tout doux",
        "tout calme",
        "aujourd'hui,",
        "sarah",
        "amir",
        "aniss",
        "nina",
        "chouchou",
        "mila",
        "raphaël",
        "victorino",
        "victorina",
        "cheval de bois",
        "boîte à chaussures",
        "poisson",
        "train de boîtes",
        *FORBIDDEN_CLUES,
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "grain de parquet" not in blob:
        raise SystemExit(f"{SID}: grain de parquet absent")
    if "campement du salon" not in blob:
        raise SystemExit(f"{SID}: campement du salon absent")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    n_merci = aj.count("merci") + aj.count("bravo")
    if n_merci != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{n_merci}")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        lasts.append(last_n[-1])
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
        if "grain de parquet" not in c["text"].lower():
            raise SystemExit(f"{SID} {c['chunk_id']} fin sans grain")
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
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.COR.002 — demander / attendre l'aide, pas tout seul "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Nino, papa, maman (un seul enfant)\n"
        "- **Lieu :** salon, fin d'après-midi, à la maison "
        "(campement du salon)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Papa plie le journal. Un coussin tombe. Nino le remet. "
        "Un **grain de parquet** luit sur une latte, comme une petite porte. "
        "Nino veut une tente pour l'ours rond et le lapin mince, **maintenant**, "
        "avant la soupe. Il jette trop vite, seul : le tissu glisse, le grain disparaît. "
        "Il prend le drap, la pince ou la lampe ; les trois partent. "
        "Sous la table l'ours bute, derrière le canapé la fente refuse, "
        "dans le couloir le vent lève le toit. Une 2e ruse : le grain revient. "
        "Il refuse de foncer, écoute le lieu, demande. Neuf façons : "
        "porte, plus petit, chaise ; pince, poids, dessus ; fermer, dos à dos, train. "
        "Les deux peluches restent. Le grain paie l'ouverture.\n\n"
        "## Vécu\n\n"
        "Nino veut le campement **maintenant**. Il force seul, ça résiste. "
        "Sourire disparu, poitrine bousculée, adulte accroupi. "
        "Personne ne donne la réponse. Il observe l'objet, écoute le salon, "
        "retrouve le grain du début. La leçon se voit : lâcher, demander, "
        "attendre, faire à deux. Le dénouement a failli (glisser, disparaître, tomber). "
        "Le grain paie l'ouverture. Chaque fin porte une trace unique.\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien merged F-NAR-016 sans notes/xai : tout réécrit.\n"
        "- Ouverture inventée (journal, coussin qui tombe, mouche sur l'abat-jour), "
        "pas les 5 listées example4.\n"
        "- Pas de 2e enfant (xlsx : Nino, papa, maman seulement).\n"
        "- Monde ≠ TREE-DIF-060 (Sarah/Nino, train de boîtes) ≠ TREE-DIF-049 "
        "(Sarah, tapis, poissons) ≠ TREE-DIF-021 (fort, fenêtre) ≠ TREE-DIF-026 "
        "(théâtre de draps).\n"
        "- T1 ne retire pas l'équipement. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : le grain de parquet, payé au climax.\n"
        "- Merci vécu (papa : tu as posé le coussin). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes`. "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
