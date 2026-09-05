#!/usr/bin/env python3
"""TREE-DIF-006 — Les gouttes de l'arrosoir (N2, DIF.ENE.001, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-006"
N2 = 15
TITLE = "Les gouttes de l'arrosoir"
CHARS = "Raphaël, papa, maman"
SETTING = "le jardin derrière la maison, après l'arrosage"
FIL = (
    "Après l'arrosage, maman pose trois arrosoirs sur le sentier des dalles. "
    "Sous le bec de la jaune, un éclat vert brille ; une goutte s'y tient. "
    "Raphaël veut rattraper les gouttes, avant que le soleil les boive. "
    "Il saisit trop vite : la dalle siffle. La rouge et la bleue restent. "
    "Robinet, seau ou arrosoir de maman : une 2e ruse. Il refuse de foncer. "
    "Il regarde l'éclat vert du début. On attend, la tasse, ou papa. "
    "La plante boit. L'éclat garde une trace."
)
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
    "papa sourit",
    "maman sourit",
    "énergie n'est pas",
    "ce n'est pas une faute",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "éclat vert",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_goutte_tient_sous_l_eclat_vert; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ou_l_eau_est_partie; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les_trois_arrosoirs_restent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_rattraper_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=la_2e_ruse_il_refuse_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "éclat vert",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=l_eclat_vert_montre_la_goutte; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "éclat vert",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_plante_boit_l_eclat_garde_une_trace; tempo=posé; sourire=léger; respiration=ample",
    },
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict, emphasis: str | None) -> str:
    body = esc(text)
    if emphasis:
        e = esc(emphasis)
        if e in body:
            body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
        else:
            emphasis = None
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict, emphasis: str | None) -> str:
    body = text
    if emphasis and emphasis in body:
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
        if n > N2:
            raise SystemExit(f"{where} {n}>{N2}: {ph}")
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


OPENING = [
    "narrateur|Maman pose trois arrosoirs, un par un.",
    "narrateur|Le métal fait toc, toc, toc, sur les dalles.",
    "narrateur|Puis le jardin se tait, derrière la maison.",
    "narrateur|Ça sent la terre mouillée, et la tomate.",
    "narrateur|Le cerisier jette une ombre chaude, courte.",
    "narrateur|Sous le bec de la jaune, un éclat vert brille.",
    "narrateur|Une goutte s'y tient, sans tomber.",
    "papa|Tu as vu celle-là, Raphaël ?",
    "enfant-m|Elle ne veut pas partir !",
    "maman|Le soleil va la boire, sur la dalle.",
    "narrateur|En ce moment, Raphaël tend les deux mains.",
    "enfant-m|Je la rattrape, avant le soleil !",
    "narrateur|Il saisit la jaune, trop vite, trop fort.",
    "narrateur|La goutte tombe, et la dalle siffle.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
    "papa|Merci, tu as vu la goutte.",
    "narrateur|Papa s'accroupit, à la même hauteur.",
    "maman|La rouge et la bleue sont là, aussi.",
]

T1_CHOICE = [
    "narrateur|Trois arrosoirs restent sur le sentier des dalles.",
    "narrateur|La jaune, la rouge, et la bleue.",
    "maman|Par laquelle tu commences, Raphaël ?",
]

T1 = {
    1: {
        "lab": "la jaune",
        "sons": "dalle,arrosoir",
        "emphasis": "jaune",
        "passage": [
            "narrateur|Raphaël prend d'abord la jaune, par l'anse.",
            "enfant-m|Toi d'abord, éclat vert !",
            "narrateur|La rouge et la bleue restent sur les dalles.",
            "narrateur|Il court vers la petite salade, près du bac.",
            "narrateur|L'eau saute, et la dalle siffle, blanche.",
            "enfant-m|Elle est partie trop vite !",
            "narrateur|La petite salade penche, sèche, trop légère.",
            "maman|La dalle a tout pris, vois-tu ?",
            "papa|La rouge et la bleue n'ont pas bougé.",
            "narrateur|Raphaël serre l'anse, les joues chaudes.",
            "enfant-m|Il m'en faut, pour elle.",
            "narrateur|L'éclat vert tremble au bec, sans goutte.",
        ],
        "question": [
            "narrateur|L'eau a sauté, trop vite.",
            "maman|Elle est allée où ?",
        ],
        "qfields": {
            "expected_answer": "dalle",
            "accepted_examples": "dalle | la dalle | par terre | sur la dalle | dalle chaude | le sol",
            "retry_prompt": "L'eau a sauté sur la dalle.",
        },
        "confirm": [
            "narrateur|Oui, sur la dalle chaude, un rond mouillé.",
            "enfant-m|La petite salade n'a rien eu.",
            "maman|Il nous faut d'autre eau.",
            "papa|Le jardin a des réserves, plus loin.",
            "narrateur|La jaune est trop légère, à présent.",
            "narrateur|La rouge et la bleue attendent sur le sentier.",
            "papa|Tu tiens bien l'anse ?",
            "enfant-m|Oui, papa.",
        ],
    },
    2: {
        "lab": "la rouge",
        "sons": "terre,arrosoir",
        "emphasis": "rouge",
        "passage": [
            "narrateur|Raphaël prend d'abord la rouge, plus chaude.",
            "enfant-m|Toi, tu vas aux tomates !",
            "narrateur|La jaune et la bleue restent sur les dalles.",
            "narrateur|Il verse trop, d'un seul élan, près des plants.",
            "narrateur|Une flaque s'ouvre dans la terre, trop large.",
            "enfant-m|Il a trop bu, d'un coup !",
            "narrateur|Le pied de tomate se tord, trop lourd.",
            "papa|La flaque est à son pied, vois-tu ?",
            "maman|La jaune et la bleue n'ont pas bougé.",
            "narrateur|Une coccinelle grimpe, puis s'arrête.",
            "enfant-m|Il m'en faut, une gorgée.",
            "narrateur|L'éclat vert de la jaune luit, derrière lui.",
        ],
        "question": [
            "narrateur|Le trop d'eau a fait une flaque.",
            "maman|Elle est où, cette flaque ?",
        ],
        "qfields": {
            "expected_answer": "terre",
            "accepted_examples": "terre | la terre | sol | dans la terre | près du pied | au pied | flaque",
            "retry_prompt": "La flaque est dans la terre, près du pied.",
        },
        "confirm": [
            "narrateur|Oui, la flaque brille au pied du plant.",
            "enfant-m|Il a trop bu, trop vite.",
            "papa|Le plant a trop bu, d'un coup.",
            "maman|On va chercher de l'eau ailleurs.",
            "narrateur|La rouge pèse à peine, à présent.",
            "narrateur|La jaune et la bleue attendent sur le sentier.",
            "maman|Tu tiens bien l'anse ?",
            "enfant-m|Oui, maman.",
        ],
    },
    3: {
        "lab": "la bleue",
        "sons": "bois,arrosoir",
        "emphasis": "bleue",
        "passage": [
            "narrateur|Raphaël prend d'abord la bleue, plus fraîche.",
            "enfant-m|Toi, tu vas au banc !",
            "narrateur|La jaune et la rouge restent sur les dalles.",
            "narrateur|Il tourne, l'arrosoir au ventre, trop content.",
            "narrateur|L'eau gicle, et mouille le bois du banc.",
            "enfant-m|J'ai trop tourné !",
            "narrateur|La campanule penche dans l'ombre, sèche.",
            "papa|Le bois n'a pas soif, vois-tu ?",
            "maman|La jaune et la rouge n'ont pas bougé.",
            "narrateur|Un papillon quitte le pétale mouillé.",
            "enfant-m|Il m'en faut, pour elle.",
            "narrateur|L'éclat vert de la jaune luit, au sentier.",
        ],
        "question": [
            "narrateur|L'eau a mouillé le bois.",
            "maman|Elle a mouillé quoi ?",
        ],
        "qfields": {
            "expected_answer": "banc",
            "accepted_examples": "banc | le banc | bois | le bois | le bois du banc",
            "retry_prompt": "L'eau a mouillé le banc.",
        },
        "confirm": [
            "narrateur|Oui, le banc a pris l'eau, un nuage mouillé.",
            "enfant-m|La campanule a soif, elle.",
            "maman|On lui en rapporte, sans danser.",
            "papa|Le jardin n'a pas dit son dernier mot.",
            "narrateur|La bleue sonne creux, à présent.",
            "narrateur|La jaune et la rouge attendent sur le sentier.",
            "papa|Tu tiens bien l'anse ?",
            "enfant-m|Oui, papa.",
        ],
    },
}

T2 = {
    (1, 1): {
        "sons": "robinet,dalle",
        "emphasis": "robinet",
        "passage": [
            "narrateur|Près du bac, le petit robinet brille.",
            "narrateur|Raphaël ouvre trop, d'un coup.",
            "narrateur|L'eau part comme une fusée, trop haute.",
            "enfant-m|Ça va trop fort !",
            "narrateur|La jaune déborde sur la dalle chaude.",
            "papa|Ferme un tout petit peu.",
            "narrateur|Il ferme, puis ouvre un filet, mince.",
            "narrateur|Le robinet tousse, et un jet revient, rusé.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Raphaël regarde l'éclat vert, sur le bec.",
            "narrateur|L'éclat ne tremble plus, puis oui, puis non.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "seau,sable",
        "emphasis": "seau",
        "passage": [
            "narrateur|Près du bac, le seau est trop lourd.",
            "narrateur|Raphaël tire, ça avance mal, ça penche.",
            "narrateur|L'eau cliquette, et lui mouille les orteils.",
            "narrateur|Du sable nage au fond, gris.",
            "papa|On le glisse, sans le lever.",
            "narrateur|Ils traînent le seau vers la salade.",
            "narrateur|Raphaël plonge la jaune, trop vite.",
            "narrateur|Une feuille de sable monte, rusée.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Raphaël regarde l'éclat vert, sous l'eau.",
            "narrateur|Le sable cache l'éclat, puis le lâche.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "goutte,abeille",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|L'arrosoir de maman goutte dans les fleurs.",
            "narrateur|Raphaël le secoue, trop content, trop fort.",
            "narrateur|Des gouttes volent, et une abeille s'en va.",
            "maman|Il reste les dernières, au bec.",
            "narrateur|Il tend la jaune dessous, trop tôt.",
            "narrateur|Rien, puis une goutte lui tombe au genou.",
            "enfant-m|Elle s'est cachée !",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "enfant-m|Pas maintenant.",
            "narrateur|Raphaël regarde l'éclat vert, sur la jaune.",
            "narrateur|Une goutte s'y accroche, puis recule.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
            "papa|Les dernières n'aiment pas danser.",
        ],
    },
    (2, 1): {
        "sons": "robinet,terre",
        "emphasis": "robinet",
        "passage": [
            "narrateur|Vers les tomates, le robinet du potager.",
            "narrateur|Raphaël ouvre, trop content, trop large.",
            "narrateur|Le jet brille, puis inonde la terre du plant.",
            "enfant-m|Le pied va trop boire !",
            "papa|Un filet, comme un fil.",
            "narrateur|Il referme, puis ouvre un peu, mince.",
            "narrateur|Le robinet tousse, et un jet revient, rusé.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Une coccinelle grimpe sur le bord, puis part.",
            "narrateur|Raphaël regarde l'éclat vert, sur la jaune.",
            "narrateur|L'éclat tremble quand le jet tousse.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "seau,terre",
        "emphasis": "seau",
        "passage": [
            "narrateur|Le seau près des tomates sent la terre.",
            "narrateur|Raphaël veut le porter comme papa.",
            "narrateur|Il le soulève, ça penche, ça verse.",
            "narrateur|L'eau lui mouille le ventre, froide.",
            "papa|Laisse, on le traîne à deux.",
            "narrateur|Ils glissent le seau entre les plants.",
            "narrateur|Le pied de tomate tremble au passage.",
            "narrateur|Raphaël puise avec la rouge, trop vite.",
            "narrateur|Une vague de terre monte, rusée.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Raphaël cherche l'éclat vert, au sentier.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "goutte,coccinelle",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|L'arrosoir de maman est coincé entre les tomates.",
            "narrateur|Raphaël tire, ça vient, trop d'un coup.",
            "narrateur|Une coccinelle était sur le bec.",
            "narrateur|Il souffle pour la faire partir.",
            "narrateur|Les dernières gouttes sont roses de terre.",
            "maman|Celles-là, on les garde.",
            "narrateur|Il pose la rouge dessous, trop tôt.",
            "narrateur|Une goutte tombe à côté, rusée.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Raphaël regarde l'éclat vert, sur la jaune.",
            "narrateur|L'éclat luit entre les feuilles, loin.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "robinet,bois",
        "emphasis": "robinet",
        "passage": [
            "narrateur|Près du banc, un petit robinet froid.",
            "narrateur|Raphaël ouvre en tournant trop.",
            "narrateur|Le jet mouille le bois du banc.",
            "enfant-m|Le banc n'a pas soif !",
            "papa|La campanule, elle, oui.",
            "narrateur|Il réduit le filet, puis le robinet tousse.",
            "narrateur|Un jet rusé revient, trop large.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un papillon se pose sur l'anse, puis part.",
            "narrateur|Raphaël regarde l'éclat vert, au sentier.",
            "narrateur|L'éclat brille, loin, sous le cerisier.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "seau,ombre",
        "emphasis": "seau",
        "passage": [
            "narrateur|Le seau d'ombre est sous le banc.",
            "narrateur|Raphaël s'assoit, veut le tirer d'un coup.",
            "narrateur|Ça résiste, le bois est tiède.",
            "narrateur|Il recule, il avance, il souffle.",
            "papa|On le sort ensemble.",
            "narrateur|Ils posent le seau au soleil du banc.",
            "narrateur|Raphaël plonge la bleue, trop vite.",
            "narrateur|L'eau froide gicle sur le bois, rusée.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Raphaël cherche l'éclat vert, au sentier.",
            "narrateur|L'éclat luit, loin, sur la jaune.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "goutte,papillon",
        "emphasis": "arrosoir",
        "passage": [
            "narrateur|L'arrosoir de maman dort contre le banc.",
            "narrateur|Presque vide, à l'ombre, tiède.",
            "narrateur|Raphaël le soulève et le secoue.",
            "narrateur|L'eau gicle sur le bois, trop vive.",
            "papa|Les dernières gouttes n'aiment pas danser.",
            "maman|Tends le tien dessous.",
            "narrateur|Il s'immobilise, la bleue ouverte, trop tôt.",
            "narrateur|Une goutte, un papillon, une goutte rusée.",
            "enfant-m|Pas maintenant.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Raphaël regarde l'éclat vert, au sentier.",
            "narrateur|L'éclat attend, loin, sous le cerisier.",
            "maman|Tu vois comment, Raphaël ?",
            "enfant-m|Alors on fait quoi ?",
        ],
    },
}

T2_Q = {
    1: [
        "narrateur|La petite salade a soif, près du bac.",
        "narrateur|Le robinet, le seau, ou l'arrosoir de maman.",
        "papa|On prend l'eau où ?",
    ],
    2: [
        "narrateur|Le pied de tomate penche, trop lourd d'un côté.",
        "narrateur|Le robinet, le seau, ou l'arrosoir de maman.",
        "papa|On prend l'eau où ?",
    ],
    3: [
        "narrateur|La campanule attend, dans l'ombre du banc.",
        "narrateur|Le robinet, le seau, ou l'arrosoir de maman.",
        "papa|On prend l'eau où ?",
    ],
}

T3_Q = {
    (1, 1): [
        "narrateur|L'eau du robinet attend dans la jaune.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (1, 2): [
        "narrateur|L'eau du seau est près de la salade.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (1, 3): [
        "narrateur|Les dernières gouttes pendent, au bec de maman.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (2, 1): [
        "narrateur|L'eau du robinet attend dans la rouge.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (2, 2): [
        "narrateur|L'eau du seau est entre les tomates.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (2, 3): [
        "narrateur|Les dernières gouttes sont roses de terre.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (3, 1): [
        "narrateur|L'eau froide du robinet attend dans la bleue.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (3, 2): [
        "narrateur|L'eau du seau d'ombre est près du banc.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
    (3, 3): [
        "narrateur|Les dernières gouttes pendent contre le banc.",
        "narrateur|On attend, la tasse, ou papa.",
        "maman|Tu fais comment, Raphaël ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "enfant-m|J'attends la goutte.",
        "narrateur|Raphaël s'accroupit près de la salade.",
        "narrateur|Il penche la jaune, un tout petit peu.",
        "narrateur|L'éclat vert ne tremble plus, du tout.",
        "narrateur|Une goutte tombe, puis une autre.",
        "papa|Elle boit, tu vois ?",
        "narrateur|La petite salade se redresse, lente.",
        "enfant-m|Je ne fonce pas.",
        "maman|L'éclat a montré le moment.",
        "narrateur|Le filet du robinet se tait, mince.",
        "enfant-m|C'est pour toi, salade.",
    ],
    (1, 1, 2): [
        "enfant-m|La tasse fait les voyages.",
        "narrateur|Maman tend une petite tasse, émaillée.",
        "narrateur|Raphaël marche vers le robinet, sans courir.",
        "narrateur|Chaque fois, une gorgée pour la salade.",
        "papa|Tes jambes vont vite, pas l'eau.",
        "maman|La tasse tient, si tu marches.",
        "narrateur|La petite salade se redresse, gorgée après gorgée.",
        "enfant-m|J'ai envie de courir, un peu.",
        "papa|La tasse t'attend, pas le fleuve.",
        "narrateur|L'éclat vert brille au fond de la tasse.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (1, 1, 3): [
        "enfant-m|Papa, tu le tiens ?",
        "papa|Je le tiens.",
        "narrateur|Papa tient la jaune, bien stable.",
        "narrateur|Raphaël pose deux doigts sur le bec.",
        "narrateur|Ils penchent ensemble, très peu.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais tout seul, très vite.",
        "papa|On vise près de la salade, là.",
        "narrateur|La petite salade boit, sans se tordre.",
        "narrateur|L'éclat vert reste droit, sous leurs doigts.",
        "enfant-m|À deux, ça ne saute pas.",
    ],
    (1, 2, 1): [
        "enfant-m|J'attends que le sable se pose.",
        "narrateur|Raphaël s'accroupit, le seau entre les genoux.",
        "narrateur|Deux ronds montent, puis le fond se tait.",
        "narrateur|Il penche la jaune, un tout petit peu.",
        "narrateur|L'éclat vert reparaît, net, sous l'eau.",
        "papa|Le sable est resté en bas.",
        "narrateur|Une goutte claire arrive à la salade.",
        "enfant-m|Je ne fonce pas.",
        "maman|Tu as laissé le fond se taire.",
        "narrateur|La petite salade se redresse, lente.",
        "enfant-m|C'est de l'eau, pas du sable.",
    ],
    (1, 2, 2): [
        "enfant-m|La tasse puise, pas l'arrosoir.",
        "narrateur|Maman tend la petite tasse, émaillée.",
        "narrateur|Raphaël la glisse au bord du seau, bas.",
        "narrateur|Une gorgée, sans le sable du fond.",
        "papa|Tu n'as pas plongé trop bas.",
        "narrateur|Il marche vers la salade, tasse à deux mains.",
        "narrateur|La petite salade boit, gorgée après gorgée.",
        "enfant-m|Mes jambes peuvent courir, pas l'eau.",
        "maman|La tasse a fait le voyage.",
        "narrateur|L'éclat vert se mire au fond de la tasse.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (1, 2, 3): [
        "enfant-m|Papa, tu tiens le seau ?",
        "papa|Je le tiens, toi tu verses.",
        "narrateur|Papa cale le seau, Raphaël plonge la jaune.",
        "narrateur|Deux doigts sur le bec, très peu.",
        "narrateur|Ils visent le pied de la salade, ensemble.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais le lever tout seul.",
        "papa|À deux, il ne penche plus.",
        "narrateur|La petite salade boit, sans se tordre.",
        "narrateur|L'éclat vert reste droit, sous leurs doigts.",
        "enfant-m|Le seau est resté sage.",
    ],
    (1, 3, 1): [
        "enfant-m|J'attends la suivante.",
        "narrateur|Raphaël se met à genoux, la jaune ouverte.",
        "narrateur|Le bec de maman goutte, puis rien, puis goutte.",
        "narrateur|L'éclat vert s'allume à chaque goutte.",
        "narrateur|Il ne bouge pas, même quand ça tarde.",
        "maman|Elle vient.",
        "papa|Tu es resté, toi.",
        "narrateur|Trois gouttes, et la salade se redresse.",
        "enfant-m|Je ne fonce pas.",
        "narrateur|L'abeille revient, tout près du bec.",
        "enfant-m|C'est pour toi, salade.",
    ],
    (1, 3, 2): [
        "enfant-m|La tasse attrape les dernières.",
        "narrateur|Maman tend la petite tasse, émaillée.",
        "narrateur|Raphaël la glisse sous le bec de maman.",
        "narrateur|Une goutte, un silence, une goutte.",
        "papa|Tu n'as pas secoué.",
        "narrateur|Il porte la tasse à la salade, sans courir.",
        "narrateur|La petite salade boit, goutte après goutte.",
        "enfant-m|Elles ont voyagé, les dernières.",
        "maman|La tasse a fait le pont.",
        "narrateur|L'éclat vert se mire au fond, minuscule.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (1, 3, 3): [
        "enfant-m|Papa, tu tiens celui de maman ?",
        "papa|Je le tiens, toi tu reçois.",
        "narrateur|Papa tient l'arrosoir de maman, stable.",
        "narrateur|Raphaël pose la jaune dessous, deux doigts au bec.",
        "narrateur|Ils attendent la goutte, ensemble, sans secouer.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais tout secouer, tout seul.",
        "papa|À deux, elles tombent où on veut.",
        "narrateur|La petite salade boit, sans se tordre.",
        "narrateur|L'éclat vert reste droit, sous leurs doigts.",
        "enfant-m|Le bec ne gicle plus.",
    ],
    (2, 1, 1): [
        "enfant-m|J'attends le filet.",
        "narrateur|Raphaël s'accroupit près du pied de tomate.",
        "narrateur|Il penche la rouge, un tout petit peu.",
        "narrateur|L'éclat vert, au sentier, ne tremble plus.",
        "narrateur|Une goutte, puis une autre, au pied, pas à la flaque.",
        "papa|Elle boit, tu vois ?",
        "narrateur|Le pied de tomate se redresse, lent.",
        "enfant-m|Je ne fonce pas.",
        "maman|Tu as visé le pied, pas la terre.",
        "narrateur|Le filet du robinet se tait, mince.",
        "enfant-m|C'est pour toi, tomate.",
    ],
    (2, 1, 2): [
        "enfant-m|La tasse fait les voyages.",
        "narrateur|Maman tend une petite tasse, émaillée.",
        "narrateur|Raphaël marche vers le robinet, sans courir.",
        "narrateur|Chaque fois, une gorgée au pied du plant.",
        "papa|Tes jambes vont vite, pas l'eau.",
        "maman|La tasse tient, si tu marches.",
        "narrateur|Le pied de tomate se redresse, gorgée après gorgée.",
        "enfant-m|J'ai envie de tout verser.",
        "papa|La tasse t'attend, pas le fleuve.",
        "narrateur|L'éclat vert se mire au fond de la tasse.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (2, 1, 3): [
        "enfant-m|Papa, tu le tiens ?",
        "papa|Je le tiens.",
        "narrateur|Papa tient la rouge, bien stable.",
        "narrateur|Raphaël pose deux doigts sur le bec.",
        "narrateur|Ils penchent ensemble, très peu, au pied.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais tout seul, très vite.",
        "papa|On vise le pied, pas la flaque.",
        "narrateur|Le pied de tomate boit, sans se tordre.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "enfant-m|À deux, ça ne saute pas.",
    ],
    (2, 2, 1): [
        "enfant-m|J'attends que la terre se pose.",
        "narrateur|Raphaël s'accroupit, le seau entre les plants.",
        "narrateur|Des bulles montent, puis le fond se tait.",
        "narrateur|Il penche la rouge, un tout petit peu.",
        "narrateur|L'éclat vert, au sentier, redevient net.",
        "papa|La terre est restée en bas.",
        "narrateur|Une goutte claire arrive au pied.",
        "enfant-m|Je ne fonce pas.",
        "maman|Tu as laissé les bulles finir.",
        "narrateur|Le pied de tomate se redresse, lent.",
        "enfant-m|C'est de l'eau, pas de la boue.",
    ],
    (2, 2, 2): [
        "enfant-m|La tasse puise, pas l'arrosoir.",
        "narrateur|Maman tend la petite tasse, émaillée.",
        "narrateur|Raphaël la glisse au bord du seau, bas.",
        "narrateur|Une gorgée, sans la terre du fond.",
        "papa|Tu n'as pas plongé trop bas.",
        "narrateur|Il marche vers le plant, tasse à deux mains.",
        "narrateur|Le pied de tomate boit, gorgée après gorgée.",
        "enfant-m|Mes jambes peuvent courir, pas l'eau.",
        "maman|La tasse a fait le voyage.",
        "narrateur|L'éclat vert se mire au fond, un peu brun.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (2, 2, 3): [
        "enfant-m|Papa, tu tiens le seau ?",
        "papa|Je le tiens, toi tu verses.",
        "narrateur|Papa cale le seau, Raphaël plonge la rouge.",
        "narrateur|Deux doigts sur le bec, très peu.",
        "narrateur|Ils visent le pied du plant, ensemble.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais le lever tout seul.",
        "papa|À deux, il ne penche plus.",
        "narrateur|Le pied de tomate boit, sans se tordre.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "enfant-m|Le seau est resté sage.",
    ],
    (2, 3, 1): [
        "enfant-m|J'attends la suivante.",
        "narrateur|Raphaël se met à genoux, la rouge ouverte.",
        "narrateur|Le bec de maman goutte, rose, puis rien.",
        "narrateur|L'éclat vert, au sentier, s'allume de loin.",
        "narrateur|Il ne bouge pas, même quand ça tarde.",
        "maman|Elle vient.",
        "papa|Tu es resté, toi.",
        "narrateur|Trois gouttes, et le pied se redresse.",
        "enfant-m|Je ne fonce pas.",
        "narrateur|La coccinelle reprend le bec, sans bruit.",
        "enfant-m|C'est pour toi, tomate.",
    ],
    (2, 3, 2): [
        "enfant-m|La tasse attrape les dernières.",
        "narrateur|Maman tend la petite tasse, émaillée.",
        "narrateur|Raphaël la glisse sous le bec de maman.",
        "narrateur|Une goutte rose, un silence, une goutte.",
        "papa|Tu n'as pas secoué.",
        "narrateur|Il porte la tasse au pied, sans courir.",
        "narrateur|Le pied de tomate boit, goutte après goutte.",
        "enfant-m|Elles ont voyagé, les dernières.",
        "maman|La tasse a fait le pont.",
        "narrateur|L'éclat vert se mire au fond, un peu rose.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (2, 3, 3): [
        "enfant-m|Papa, tu tiens celui de maman ?",
        "papa|Je le tiens, toi tu reçois.",
        "narrateur|Papa tient l'arrosoir de maman, stable.",
        "narrateur|Raphaël pose la rouge dessous, deux doigts au bec.",
        "narrateur|Ils attendent la goutte, ensemble, sans secouer.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais tout secouer, tout seul.",
        "papa|À deux, elles tombent où on veut.",
        "narrateur|Le pied de tomate boit, sans se tordre.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "enfant-m|Le bec ne gicle plus.",
    ],
    (3, 1, 1): [
        "enfant-m|J'attends le filet froid.",
        "narrateur|Raphaël s'accroupit près de la campanule.",
        "narrateur|Il penche la bleue, un tout petit peu.",
        "narrateur|L'éclat vert, au sentier, ne tremble plus.",
        "narrateur|Une goutte froide, puis une autre, au pied.",
        "papa|Elle boit, tu vois ?",
        "narrateur|La campanule se redresse, dans l'ombre.",
        "enfant-m|Je ne fonce pas.",
        "maman|Tu as visé la fleur, pas le banc.",
        "narrateur|Le filet du robinet se tait, mince.",
        "enfant-m|C'est pour toi, campanule.",
    ],
    (3, 1, 2): [
        "enfant-m|La tasse fait les voyages.",
        "narrateur|Maman tend une petite tasse, émaillée.",
        "narrateur|Raphaël marche vers le robinet, sans courir.",
        "narrateur|Chaque fois, une gorgée froide pour la fleur.",
        "papa|Tes jambes vont vite, pas l'eau.",
        "maman|La tasse tient, si tu marches.",
        "narrateur|La campanule se redresse, gorgée après gorgée.",
        "enfant-m|J'ai envie de danser, un peu.",
        "papa|La tasse t'attend, pas le bois.",
        "narrateur|L'éclat vert se mire au fond, tout froid.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (3, 1, 3): [
        "enfant-m|Papa, tu le tiens ?",
        "papa|Je le tiens.",
        "narrateur|Papa tient la bleue, bien stable.",
        "narrateur|Raphaël pose deux doigts sur le bec.",
        "narrateur|Ils penchent ensemble, très peu, au pied.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais tout seul, en tournant.",
        "papa|On vise la fleur, pas le banc.",
        "narrateur|La campanule boit, sans se tordre.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "enfant-m|À deux, ça ne gicle pas.",
    ],
    (3, 2, 1): [
        "enfant-m|J'attends que l'ombre se tienne.",
        "narrateur|Raphaël s'accroupit, le seau au soleil du banc.",
        "narrateur|L'eau froide se tait, puis un rond monte.",
        "narrateur|Il penche la bleue, un tout petit peu.",
        "narrateur|L'éclat vert, au sentier, redevient net.",
        "papa|Le bois n'a plus d'eau, lui.",
        "narrateur|Une goutte froide arrive à la campanule.",
        "enfant-m|Je ne fonce pas.",
        "maman|Tu as laissé le seau se tenir.",
        "narrateur|La campanule se redresse, dans l'ombre.",
        "enfant-m|C'est pour la fleur, pas pour le banc.",
    ],
    (3, 2, 2): [
        "enfant-m|La tasse puise, pas l'arrosoir.",
        "narrateur|Maman tend la petite tasse, émaillée.",
        "narrateur|Raphaël la glisse au bord du seau, bas.",
        "narrateur|Une gorgée froide, sans mouiller le bois.",
        "papa|Tu n'as pas penché trop.",
        "narrateur|Il marche vers la fleur, tasse à deux mains.",
        "narrateur|La campanule boit, gorgée après gorgée.",
        "enfant-m|Mes jambes peuvent danser, pas l'eau.",
        "maman|La tasse a fait le voyage.",
        "narrateur|L'éclat vert se mire au fond, tout froid.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (3, 2, 3): [
        "enfant-m|Papa, tu tiens le seau ?",
        "papa|Je le tiens, toi tu verses.",
        "narrateur|Papa cale le seau, Raphaël plonge la bleue.",
        "narrateur|Deux doigts sur le bec, très peu.",
        "narrateur|Ils visent le pied de la campanule, ensemble.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais le tirer tout seul.",
        "papa|À deux, il ne gicle plus.",
        "narrateur|La campanule boit, sans se tordre.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "enfant-m|Le seau d'ombre est resté sage.",
    ],
    (3, 3, 1): [
        "enfant-m|J'attends la suivante.",
        "narrateur|Raphaël se met à genoux, la bleue ouverte.",
        "narrateur|Le bec de maman goutte, puis rien, puis goutte.",
        "narrateur|L'éclat vert, au sentier, s'allume de loin.",
        "narrateur|Il ne bouge pas, même quand ça tarde.",
        "maman|Elle vient.",
        "papa|Tu es resté, toi.",
        "narrateur|Trois gouttes, et la campanule se redresse.",
        "enfant-m|Je ne fonce pas.",
        "narrateur|Le papillon revient, tout près de l'anse.",
        "enfant-m|C'est pour toi, campanule.",
    ],
    (3, 3, 2): [
        "enfant-m|La tasse attrape les dernières.",
        "narrateur|Maman tend la petite tasse, émaillée.",
        "narrateur|Raphaël la glisse sous le bec de maman.",
        "narrateur|Une goutte, un papillon, une goutte.",
        "papa|Tu n'as pas secoué.",
        "narrateur|Il porte la tasse à la fleur, sans danser.",
        "narrateur|La campanule boit, goutte après goutte.",
        "enfant-m|Elles ont voyagé, les dernières.",
        "maman|La tasse a fait le pont.",
        "narrateur|L'éclat vert se mire au fond, minuscule.",
        "enfant-m|Toi, tu restes ronde.",
    ],
    (3, 3, 3): [
        "enfant-m|Papa, tu tiens celui de maman ?",
        "papa|Je le tiens, toi tu reçois.",
        "narrateur|Papa tient l'arrosoir de maman, stable.",
        "narrateur|Raphaël pose la bleue dessous, deux doigts au bec.",
        "narrateur|Ils attendent la goutte, ensemble, sans secouer.",
        "maman|Comme ça, oui.",
        "enfant-m|Je voulais tout secouer, tout seul.",
        "papa|À deux, elles tombent où on veut.",
        "narrateur|La campanule boit, sans se tordre.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "enfant-m|Le bec ne gicle plus.",
    ],
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|On a failli tout verser.",
        "papa|Le filet a failli trop courir.",
        "maman|Vous avez laissé l'éclat se taire.",
        "narrateur|Ils restent près du bac, sans beaucoup bouger.",
        "narrateur|La jaune a un rond d'ombre, sous l'anse.",
        "narrateur|Un grain de sable sèche sur la feuille.",
    ],
    (1, 1, 2): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|La tasse a failli trop danser.",
        "papa|Tes jambes ont failli trop courir.",
        "maman|La tasse a tenu, elle.",
        "narrateur|La petite tasse repose près du bac.",
        "narrateur|L'éclat vert a laissé un bord mouillé.",
        "narrateur|La tasse garde un rond de soleil, au bac.",
    ],
    (1, 1, 3): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|J'ai failli tout verser tout seul.",
        "papa|Tes doigts ont visé juste.",
        "maman|Vous avez tenu à deux.",
        "narrateur|Papa repose la jaune près du bac.",
        "narrateur|L'éclat vert reste droit, sous l'anse.",
        "narrateur|L'ombre de papa reste un moment sur le bac.",
    ],
    (1, 2, 1): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|Le sable a failli tout prendre.",
        "papa|Tu as laissé le fond se taire.",
        "maman|L'eau claire est arrivée.",
        "narrateur|Ils restent près du bac, le seau entre eux.",
        "narrateur|L'éclat vert a un voile de sable, minuscule.",
        "narrateur|Le seau a un fond de sable, immobile.",
    ],
    (1, 2, 2): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|La tasse a failli trop plonger.",
        "papa|Tu as pris au bord, pas au fond.",
        "maman|La tasse a fait le voyage.",
        "narrateur|La petite tasse repose près du bac.",
        "narrateur|L'éclat vert se mire, un peu gris.",
        "narrateur|Une miette de sable brille dans la tasse.",
    ],
    (1, 2, 3): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|J'ai failli le lever tout seul.",
        "papa|À deux, il n'a pas penché.",
        "maman|Vos mains sentent le seau.",
        "narrateur|Papa repose la jaune près du bac.",
        "narrateur|L'éclat vert a séché, pâle.",
        "narrateur|Les orteils de Raphaël ont séché, pâles.",
    ],
    (1, 3, 1): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|Elle a failli tomber au genou.",
        "papa|Tu es resté sous le bec.",
        "maman|Les dernières sont arrivées.",
        "narrateur|Ils restent près des fleurs, sans beaucoup bouger.",
        "narrateur|L'éclat vert a gardé une goutte, minuscule.",
        "narrateur|L'abeille est revenue, tout près du bec.",
    ],
    (1, 3, 2): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|Les dernières ont failli voler.",
        "papa|Tu n'as pas secoué.",
        "maman|La tasse a fait le pont.",
        "narrateur|La petite tasse repose près du bac.",
        "narrateur|L'éclat vert se mire, minuscule.",
        "narrateur|La dernière goutte de maman a voyagé.",
    ],
    (1, 3, 3): [
        "narrateur|La petite salade ne penche plus.",
        "enfant-m|J'ai failli tout secouer.",
        "papa|À deux, elles sont tombées juste.",
        "maman|Le bec de maman s'est tu.",
        "narrateur|Papa repose la jaune près du bac.",
        "narrateur|L'éclat vert reste droit, sous l'anse.",
        "narrateur|Le bec de la jaune ne gicle plus.",
    ],
    (2, 1, 1): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|On a failli faire un fleuve.",
        "papa|Le filet a failli trop courir.",
        "maman|Vous avez visé le pied.",
        "narrateur|Ils restent entre les plants, sans beaucoup bouger.",
        "narrateur|L'éclat vert luit au sentier, loin.",
        "narrateur|Une coccinelle s'est posée sur la feuille rouge.",
    ],
    (2, 1, 2): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|La tasse a failli trop danser.",
        "papa|Tes jambes ont failli trop courir.",
        "maman|La tasse a tenu, elle.",
        "narrateur|La petite tasse repose entre les plants.",
        "narrateur|L'éclat vert se mire, un peu rouge.",
        "narrateur|Une tomate a une goutte, pour de rire.",
    ],
    (2, 1, 3): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|J'ai failli tout verser tout seul.",
        "papa|Tes doigts ont visé le pied.",
        "maman|Vous avez tenu à deux.",
        "narrateur|Papa repose la rouge entre les plants.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "narrateur|Le filet du robinet s'est tu, entre les plants.",
    ],
    (2, 2, 1): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|La boue a failli tout prendre.",
        "papa|Tu as laissé les bulles finir.",
        "maman|L'eau claire est arrivée.",
        "narrateur|Ils restent entre les plants, le seau entre eux.",
        "narrateur|L'éclat vert a un voile de terre, minuscule.",
        "narrateur|La terre a cessé de faire des bulles.",
    ],
    (2, 2, 2): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|La tasse a failli trop plonger.",
        "papa|Tu as pris au bord, pas au fond.",
        "maman|La tasse a fait le voyage.",
        "narrateur|La petite tasse repose entre les plants.",
        "narrateur|L'éclat vert se mire, un peu brun.",
        "narrateur|La tasse a une auréole de terre, sèche.",
    ],
    (2, 2, 3): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|J'ai failli le lever tout seul.",
        "papa|À deux, il n'a pas penché.",
        "maman|Vos mains sentent la terre.",
        "narrateur|Papa repose la rouge entre les plants.",
        "narrateur|L'éclat vert luit au sentier, pâle.",
        "narrateur|Le seau repose entre les tomates, lourd.",
    ],
    (2, 3, 1): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|Elle a failli tomber à côté.",
        "papa|Tu es resté sous le bec.",
        "maman|Les dernières sont arrivées.",
        "narrateur|Ils restent entre les tomates, sans beaucoup bouger.",
        "narrateur|L'éclat vert luit au sentier, loin.",
        "narrateur|Un pétale rouge a gardé une goutte ronde.",
    ],
    (2, 3, 2): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|Les dernières ont failli voler.",
        "papa|Tu n'as pas secoué.",
        "maman|La tasse a fait le pont.",
        "narrateur|La petite tasse repose entre les plants.",
        "narrateur|L'éclat vert se mire, un peu rose.",
        "narrateur|La coccinelle a repris le bec, sans bruit.",
    ],
    (2, 3, 3): [
        "narrateur|Le pied de tomate ne penche plus.",
        "enfant-m|J'ai failli tout secouer.",
        "papa|À deux, elles sont tombées juste.",
        "maman|Le bec de maman s'est tu.",
        "narrateur|Papa repose la rouge entre les plants.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "narrateur|L'arrosoir de maman s'est assis dans l'herbe.",
    ],
    (3, 1, 1): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|On a failli mouiller le banc.",
        "papa|Le filet a failli trop courir.",
        "maman|Vous avez visé la fleur.",
        "narrateur|Ils restent près du banc, sans beaucoup bouger.",
        "narrateur|L'éclat vert luit au sentier, loin.",
        "narrateur|Le robinet du banc garde une goutte froide.",
    ],
    (3, 1, 2): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|La tasse a failli trop danser.",
        "papa|Tes jambes ont failli trop tourner.",
        "maman|La tasse a tenu, elle.",
        "narrateur|La petite tasse repose sous le banc.",
        "narrateur|L'éclat vert se mire, tout froid.",
        "narrateur|Le bois du banc a un petit nuage mouillé.",
    ],
    (3, 1, 3): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|J'ai failli tout verser en tournant.",
        "papa|Tes doigts ont visé la fleur.",
        "maman|Vous avez tenu à deux.",
        "narrateur|Papa repose la bleue près du banc.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "narrateur|Un papillon est resté sur l'anse bleue.",
    ],
    (3, 2, 1): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|Le seau a failli trop gicler.",
        "papa|Tu as laissé le seau se tenir.",
        "maman|L'eau froide est arrivée.",
        "narrateur|Ils restent près du banc, le seau entre eux.",
        "narrateur|L'éclat vert luit au sentier, loin.",
        "narrateur|L'ombre du seau a reculé d'un pas.",
    ],
    (3, 2, 2): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|La tasse a failli trop pencher.",
        "papa|Tu as pris au bord, pas trop.",
        "maman|La tasse a fait le voyage.",
        "narrateur|La petite tasse repose sous le banc.",
        "narrateur|L'éclat vert se mire, tout froid.",
        "narrateur|La tasse cliquette une dernière fois, sous le banc.",
    ],
    (3, 2, 3): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|J'ai failli le tirer tout seul.",
        "papa|À deux, il n'a pas giclé.",
        "maman|Vos mains sentent l'ombre.",
        "narrateur|Papa repose la bleue près du banc.",
        "narrateur|L'éclat vert luit au sentier, pâle.",
        "narrateur|Le seau d'ombre est rentré sous le banc.",
    ],
    (3, 3, 1): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|Elle a failli tomber sur le bois.",
        "papa|Tu es resté sous le bec.",
        "maman|Les dernières sont arrivées.",
        "narrateur|Ils restent près du banc, sans beaucoup bouger.",
        "narrateur|L'éclat vert luit au sentier, loin.",
        "narrateur|Une feuille d'ombre a bu, elle aussi.",
    ],
    (3, 3, 2): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|Les dernières ont failli voler.",
        "papa|Tu n'as pas secoué.",
        "maman|La tasse a fait le pont.",
        "narrateur|La petite tasse repose sous le banc.",
        "narrateur|L'éclat vert se mire, minuscule.",
        "narrateur|Le papillon a suivi la tasse, puis parti.",
    ],
    (3, 3, 3): [
        "narrateur|La campanule ne penche plus.",
        "enfant-m|J'ai failli tout secouer.",
        "papa|À deux, elles sont tombées juste.",
        "maman|Le bec de maman s'est tu.",
        "narrateur|Papa repose la bleue près du banc.",
        "narrateur|L'éclat vert luit au sentier, droit.",
        "narrateur|Le bois du banc a séché, tiède.",
    ],
}

T3_SONS = {
    (1, 1): "silence,goutte",
    (1, 2): "tasse,pas",
    (1, 3): "arrosoir,mains",
    (2, 1): "silence,goutte",
    (2, 2): "tasse,pas",
    (2, 3): "arrosoir,mains",
    (3, 1): "silence,goutte",
    (3, 2): "tasse,pas",
    (3, 3): "arrosoir,mains",
}

END_SONS = {1: "dalle,jardin", 2: "terre,jardin", 3: "bois,jardin"}

T3_EMPH = {1: "éclat vert", 2: "tasse", 3: "éclat vert"}


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_plante_boit_l_eclat_garde_une_trace; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "goutte,dalle",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("la jaune", "la rouge", "la bleue")},
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
            by_src[f"{p}_T0002_P0000"], T2_Q[a], "choice", "",
            {"fields": t3lab("le robinet", "le seau", "l'arrosoir")},
        )
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[sp] = voice(
                by_src[sp], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{sp}_T0003_P0000"] = voice(
                by_src[f"{sp}_T0003_P0000"], T3_Q[(a, b)], "choice", "",
                {"fields": t3lab("on attend", "la tasse", "papa")},
            )
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[a],
                    {"emphasis": "éclat vert", "notes": ending_note(a, b, c)},
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
        "énergie n'est pas",
        "ce n'est pas une faute",
        "bravo tu as",
        "bon travail",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "zoé",
        "zoe",
        "lina",
        "iris",
        "miel",
        "merle",
        "tout doux",
        "tout calme",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "il faut attendre",
        "dans la serre",
        "chouchou",
        "anneau de zinc",
        "grand-père",
        "maîtresse",
        "jardinier",
        "marque fine",
        "ombre-flèche",
        "ombre en forme",
        "tache de couleur",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "éclat vert" not in blob:
        raise SystemExit(f"{SID}: éclat vert absent")
    if blob.count("éclat vert") < 20:
        raise SystemExit(f"{SID}: éclat vert trop rare ({blob.count('éclat vert')})")

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
        raise SystemExit(f"chemin trop court: {min(counts)}")
    if max(counts) > 780:
        raise SystemExit(f"chemin trop long: {max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — l'énergie n'est pas une faute ; jouer, attendre, demander "
        "(vécue par la conséquence, non dite)\n"
        "- **Personnages :** Raphaël, papa, maman (un seul enfant)\n"
        "- **Lieu :** jardin derrière la maison, après l'arrosage : sentier des dalles, "
        "bac, tomates, banc du cerisier\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Maman pose trois arrosoirs, toc toc toc. Sous le bec de la jaune, "
        "un **éclat vert** brille ; une goutte s'y tient. Raphaël veut **rattraper "
        "les gouttes**, avant que le soleil les boive sur les dalles. Il saisit trop "
        "vite : la dalle siffle. Sourire disparu, poitrine bousculée, papa accroupi. "
        "Il commence par la jaune, la rouge ou la bleue ; les trois restent. "
        "Robinet qui tousse, seau trop lourd, dernières gouttes rusées : il refuse "
        "de foncer, regarde l'éclat du début. On attend, la tasse, ou papa. "
        "La plante boit. L'éclat garde une trace. Monde ≠ TREE-DIF-065 (serre, Chouchou).\n\n"
        "## Vécu\n\n"
        "Raphaël veut les gouttes **maintenant**. Trop vite, l'eau saute : dalle, "
        "flaque, banc. Personne ne dit la leçon. Conséquence : la plante n'a rien ; "
        "attendre l'éclat, voyager en tasse, ou demander à papa, et elle boit. "
        "Indice d'ouverture payé : éclat vert. Fin : plante redressée + image unique "
        "(sable, tasse, ombre, abeille, coccinelle, papillon, bois tiède).\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit 52 %, slogans DIF.ENE (« énergie / faute »), Adam hors troupe, "
        "tics « encore / déjà / tout doux / tout calme », merle, miel, "
        "« Mission accomplie », « J'ai compris » jetés.\n"
        "- T1 = trois arrosoirs (équipement non retiré). T2/T3 changent l'action. "
        "9 T2 distincts, 27 T3, 27 fins, 27 dernières images.\n"
        "- Merci vécu (goutte vue). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, "
        "émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
