#!/usr/bin/env python3
"""TREE-AUT-014 — La goutte du palier (F-NAR-019, N3, AUT.AFF.003, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-014"
N3 = 16
TITLE = "La goutte du palier"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BANNED_IMG = re.compile(
    r"(merle|miel|gouttes pendent|aujourd'hui,|j'ai compris|"
    r"mission accomplie|marque fine|ombre en forme)",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="goutte de verre",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_goutte_doit_descendre_avant_les_flaques; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="reprend",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=la_goutte_attend_sa_main; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="goutte",
        note="arc=confirmation; intention=relancer; emotion=élan_prudent; intensite=1; destinataire=enfant; sous_texte=il_a_la_goutte_les_affaires_attendent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_veut_tout_d_un_coup; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=la_seconde_ruse_menace_la_goutte; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de quartz",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=un_geste_puis_le_ting; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="goutte",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_goutte_porte_une_trace; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
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
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        if BANNED_IMG.search(ph):
            raise SystemExit(f"image interdite: {ph}")
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
    "narrateur|Les clés de papa sonnent contre le radiateur.",
    "narrateur|Le palier sent le caoutchouc mouillé.",
    "narrateur|Deux étages plus bas, une porte claque.",
    "narrateur|La lumière grise remplit la cage d'escalier.",
    "narrateur|Sur la vitre, une goutte de verre pend.",
    "narrateur|Elle tient à une ventouse ronde.",
    "narrateur|Le verre est lourd, clair, presque froid.",
    "narrateur|Si on le touche, ça fait ting.",
    "narrateur|À côté, un grain de quartz colle.",
    "narrateur|Il brille, collé par la pluie du matin.",
    "maman|Tu as vu ce grain, Nino ?",
    "papa|La cour a des flaques, en bas.",
    "narrateur|En ce moment, Nino colle le nez au verre.",
    "narrateur|Ses chaussettes frottent le carreau froid.",
    "enfant-m|Les flaques vont partir !",
    "enfant-m|Je descends la goutte, vite !",
    "narrateur|Il tire la goutte, trop fort.",
    "narrateur|La ventouse reste, ronde et vide.",
    "narrateur|Il prend manteau, seau, doudou, goutte.",
    "narrateur|Trop pour deux petites mains.",
    "narrateur|Le seau tombe.",
    "narrateur|Toc.",
    "narrateur|La goutte glisse contre son pouce.",
    "enfant-m|Non !",
    "narrateur|Nino ne rit plus.",
    "papa|Quelle main tient la goutte, là ?",
    "narrateur|Papa plie les genoux, face à face.",
    "maman|Merci, tu l'as gardée.",
]

T1_CHOICE = [
    "narrateur|La goutte de verre part avec Nino, en bas.",
    "papa|On la pose où, dans la cour ?",
    "maman|Le bac à sable, le toboggan, ou les balançoires ?",
]

T1 = {
    1: {
        "lab": "le bac à sable",
        "sons": "sable,goutte,dalles",
        "emphasis": "sable",
        "passage": [
            "narrateur|Les dalles de la cour luisent, sombres.",
            "narrateur|Nino court vers le bac à sable.",
            "narrateur|Le sable est frais, couleur chocolat.",
            "narrateur|Ça fait chh sous sa paume.",
            "enfant-m|Une maison pour la goutte !",
            "narrateur|Il plante la goutte, et un château.",
            "narrateur|Les deux, d'un seul geste.",
            "narrateur|Le château s'écroule.",
            "narrateur|La goutte penche, presque avalée.",
            "enfant-m|Elle s'en va !",
            "narrateur|Ça tape dans sa poitrine, trop vite.",
            "papa|Tes deux mains voulaient tout, non ?",
            "narrateur|Papa plie les genoux, près du bac.",
            "maman|Le seau, lui, est resté au palier.",
            "narrateur|Nino regarde ses doigts, déçu.",
            "enfant-m|Je voulais tout, tout de suite.",
        ],
        "question": [
            "narrateur|La goutte penche dans le sable.",
            "papa|Nino, tu fais quoi ?",
        ],
        "qfields": {
            "expected_answer": "reprendre",
            "accepted_examples": (
                "reprendre | le seau | le manteau | le doudou | ses affaires | "
                "il le prend | la goutte | il la reprend"
            ),
            "retry_prompt": "Il reprend la goutte. Que fait Nino ?",
            "engine_ok_text": "Oui. Il reprend.",
            "engine_near_text": "Tu es tout près. Écoute l'indice.",
        },
        "confirm": [
            "enfant-m|Je la reprends !",
            "narrateur|Oui, Nino prend la goutte à deux mains.",
            "narrateur|Le verre fait ting, avec un peu de sable.",
            "papa|Elle est à toi, maintenant.",
            "narrateur|Un grain de sable colle au verre.",
            "maman|Le palier a gardé tes affaires, tu vois ?",
            "enfant-m|On joue, et on y retourne.",
            "narrateur|La goutte brille, avec sa poussière.",
            "narrateur|Au-dessus, la vitre garde le grain de quartz.",
        ],
    },
    2: {
        "lab": "le toboggan",
        "sons": "metal,toboggan,goutte",
        "emphasis": "toboggan",
        "passage": [
            "narrateur|Le toboggan luisant attend, tout mouillé.",
            "narrateur|Nino grimpe, la goutte dans une main.",
            "narrateur|L'autre main cherche le manteau.",
            "narrateur|Le manteau est resté au palier.",
            "enfant-m|Elle glisse, comme la pluie !",
            "narrateur|Il lâche trop tôt.",
            "narrateur|La goutte file sur le métal.",
            "narrateur|Ting, ting, vers le bas.",
            "enfant-m|Attrape-la !",
            "narrateur|Papa tend le bras, trop loin.",
            "narrateur|Nino glisse, les joues chaudes.",
            "narrateur|Il rattrape la goutte, de justesse.",
            "maman|Tes épaules sont montées, tu sens ?",
            "papa|Une main pour la goutte, d'accord ?",
            "narrateur|Nino souffle, déçu, le verre froid.",
            "enfant-m|J'ai failli la perdre.",
        ],
        "question": [
            "narrateur|La goutte a filé sur le toboggan.",
            "maman|Nino, tu fais quoi ?",
        ],
        "qfields": {
            "expected_answer": "reprendre",
            "accepted_examples": (
                "reprendre | le seau | le manteau | le doudou | ses affaires | "
                "il le prend | la goutte | il la reprend"
            ),
            "retry_prompt": "Il reprend la goutte. Que fait Nino ?",
            "engine_ok_text": "Oui. Il reprend.",
            "engine_near_text": "Tu es tout près. Écoute l'indice.",
        },
        "confirm": [
            "enfant-m|Je la reprends, dans ma main.",
            "narrateur|Oui, Nino serre la goutte contre sa poitrine.",
            "narrateur|Une traînée d'eau reste sur le métal.",
            "papa|Elle a voyagé, ta goutte.",
            "maman|Le manteau t'attend, en haut, tu vois ?",
            "narrateur|Nino hoche la tête, plus calme.",
            "enfant-m|On joue, puis on remonte.",
            "narrateur|Le verre fait ting, tout près de l'oreille.",
            "narrateur|La vitre du palier garde le grain de quartz.",
        ],
    },
    3: {
        "lab": "les balançoires",
        "sons": "chaine,balancoire,flaque",
        "emphasis": "chaîne",
        "passage": [
            "narrateur|Les balançoires cliquent, lourdes d'eau.",
            "narrateur|Nino accroche la goutte à la chaîne.",
            "narrateur|Le doudou, lui, est resté au palier.",
            "enfant-m|Elle se balance, comme moi !",
            "narrateur|Il pousse trop fort.",
            "narrateur|La chaîne claque.",
            "narrateur|La goutte danse, folle, au-dessus d'une flaque.",
            "enfant-m|Elle va tomber !",
            "narrateur|Ses mains veulent tout rattraper.",
            "papa|La chaîne, ou la goutte, laquelle ?",
            "narrateur|Papa se met à hauteur de nez.",
            "maman|Le doudou n'est pas là pour l'aider.",
            "narrateur|Nino arrête la chaîne, trop tard.",
            "narrateur|La goutte penche, au bord de la flaque.",
            "enfant-m|Je n'aime pas ça.",
            "narrateur|Il fixe le verre, les lèvres pincées.",
        ],
        "question": [
            "narrateur|La goutte penche au-dessus de la flaque.",
            "papa|Nino, tu fais quoi ?",
        ],
        "qfields": {
            "expected_answer": "reprendre",
            "accepted_examples": (
                "reprendre | le seau | le manteau | le doudou | ses affaires | "
                "il le prend | la goutte | il la reprend"
            ),
            "retry_prompt": "Il reprend la goutte. Que fait Nino ?",
            "engine_ok_text": "Oui. Il reprend.",
            "engine_near_text": "Tu es tout près. Écoute l'indice.",
        },
        "confirm": [
            "enfant-m|Je la reprends !",
            "narrateur|Oui, Nino décroche la goutte, tout près.",
            "narrateur|Le verre fait ting contre la chaîne.",
            "maman|Elle est rentrée dans ta main.",
            "papa|Le doudou t'attend, au palier, tu vois ?",
            "narrateur|Nino souffle, les épaules plus basses.",
            "enfant-m|On joue, et on le cherche.",
            "narrateur|Une goutte d'eau vraie reste sur le verre.",
            "narrateur|Au-dessus, le grain de quartz brille à la vitre.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le sable a voulu garder la goutte.",
        "papa|Quel jeu t'aide, près du bac ?",
        "maman|Les cubes, le livre, ou la dînette ?",
    ],
    2: [
        "narrateur|Le toboggan a voulu l'avaler.",
        "maman|Quel jeu t'aide, près de la pente ?",
        "papa|Les cubes, le livre, ou la dînette ?",
    ],
    3: [
        "narrateur|La chaîne a trop dansé.",
        "papa|Quel jeu t'aide, près des balançoires ?",
        "maman|Les cubes, le livre, ou la dînette ?",
    ],
}

T2 = {
    (1, 1): {
        "lab": "les cubes",
        "sons": "bois,cubes,grille",
        "emphasis": "cubes",
        "passage": [
            "narrateur|Les cubes attendent près du bac, en bois clair.",
            "narrateur|Ils sentent le sapin mouillé.",
            "enfant-m|Une maison, tout de suite !",
            "narrateur|Nino pose deux cubes, d'un geste.",
            "narrateur|La tour penche vers la goutte.",
            "papa|Elle va la manger, tu vois ?",
            "narrateur|Patatras.",
            "narrateur|Un cube pousse la goutte vers la grille.",
            "enfant-m|La grille !",
            "narrateur|Il veut foncer.",
            "narrateur|Il s'arrête, les mains ouvertes.",
            "enfant-m|Pas comme ça.",
            "narrateur|Personne ne dit le geste.",
            "narrateur|Nino écoute la cour, puis le verre.",
        ],
    },
    (1, 2): {
        "lab": "le livre",
        "sons": "pages,sable,papier",
        "emphasis": "livre",
        "passage": [
            "narrateur|Le livre a une couverture bleue, un peu humide.",
            "narrateur|Nino l'ouvre sur le bord du bac.",
            "enfant-m|Un toit, pour la goutte !",
            "narrateur|Les pages collent, à cause du sable.",
            "maman|Le toit devient un piège, non ?",
            "narrateur|La couverture recouvre le verre.",
            "enfant-m|Elle a disparu !",
            "narrateur|Il veut arracher le livre, trop vite.",
            "narrateur|Il s'arrête.",
            "papa|Tu l'as vue, sous le papier ?",
            "enfant-m|Pas foncer.",
            "narrateur|Personne ne lève la couverture pour lui.",
            "narrateur|Nino pose l'oreille, écoute le ting minuscule.",
            "narrateur|Sous une page, un éclat tient bon.",
        ],
    },
    (1, 3): {
        "lab": "la dînette",
        "sons": "tasse,eau,sable",
        "emphasis": "tasse",
        "passage": [
            "narrateur|La dînette s'installe au bord du bac.",
            "narrateur|La petite tasse est blanche, légère.",
            "enfant-m|Du thé de pluie, pour elle !",
            "narrateur|Nino verse en marchant.",
            "papa|La théière penche trop, tu sens ?",
            "narrateur|L'eau voile le verre de la goutte.",
            "enfant-m|Je ne la vois plus !",
            "narrateur|Il veut essuyer avec la main sablée.",
            "narrateur|Il s'arrête, le pouce en l'air.",
            "enfant-m|Ça va rayer.",
            "maman|Le verre aime les mains propres, peut-être.",
            "narrateur|Personne ne tend le linge.",
            "narrateur|Nino souffle sur la buée, tout près.",
            "narrateur|Un éclat revient, minuscule.",
        ],
    },
    (2, 1): {
        "lab": "les cubes",
        "sons": "bois,metal,cubes",
        "emphasis": "cubes",
        "passage": [
            "narrateur|Les cubes attendent au pied du toboggan.",
            "narrateur|Ils sentent le sapin et le métal froid.",
            "enfant-m|Un escalier, jusqu'en haut !",
            "narrateur|Nino empile trop vite, deux par deux.",
            "narrateur|La pile penche contre la pente.",
            "maman|Elle va rouler, tu vois ?",
            "narrateur|Un cube tape la goutte.",
            "narrateur|Le verre part vers la gouttière du toboggan.",
            "enfant-m|Elle file !",
            "narrateur|Il veut courir sur le métal.",
            "narrateur|Il s'arrête, un pied levé.",
            "enfant-m|Pas foncer.",
            "papa|Le métal est une rivière, là.",
            "narrateur|Nino écoute le ting, plus bas.",
        ],
    },
    (2, 2): {
        "lab": "le livre",
        "sons": "pages,vent,metal",
        "emphasis": "pages",
        "passage": [
            "narrateur|Nino ouvre le livre sur la rampe du toboggan.",
            "narrateur|La couverture bleue claque, un peu.",
            "enfant-m|Un bateau, sur la pente !",
            "papa|Les pages veulent voler, elles.",
            "narrateur|Le vent tourne deux pages d'un coup.",
            "narrateur|Le livre se referme sur la goutte.",
            "enfant-m|Il l'a prise !",
            "narrateur|Il tire trop fort.",
            "narrateur|Le livre glisse vers le bas.",
            "maman|La pente avale le papier, tu vois ?",
            "narrateur|Nino s'immobilise.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Personne ne rattrape le livre pour lui.",
            "narrateur|Il écoute : un ting, sous le papier.",
        ],
    },
    (2, 3): {
        "lab": "la dînette",
        "sons": "tasse,metal,eau",
        "emphasis": "théière",
        "passage": [
            "narrateur|La dînette s'assoit au bas du toboggan.",
            "narrateur|La petite tasse sonne, légère.",
            "enfant-m|Elle boit la pente !",
            "narrateur|Nino verse en tenant la goutte.",
            "maman|Deux métiers, une seule main ?",
            "narrateur|L'eau file sur le métal, puis sur le verre.",
            "enfant-m|Elle est toute floue !",
            "narrateur|Il veut secouer la goutte, trop fort.",
            "narrateur|Il s'arrête.",
            "papa|Le verre n'aime pas la danse, là.",
            "enfant-m|Pas foncer.",
            "narrateur|Personne ne donne le linge.",
            "narrateur|Nino pose la goutte sur la rampe sèche.",
            "narrateur|Un éclat revient, tout mince.",
        ],
    },
    (3, 1): {
        "lab": "les cubes",
        "sons": "bois,chaine,cubes",
        "emphasis": "tour",
        "passage": [
            "narrateur|Les cubes attendent sous les balançoires.",
            "narrateur|Ils sentent le sapin, près de la flaque.",
            "enfant-m|Une tour, pour regarder la goutte !",
            "narrateur|Nino pose deux cubes contre un pied.",
            "narrateur|La chaîne cliquette au-dessus.",
            "papa|La tour va danser, tu sens ?",
            "narrateur|Un cube roule dans la flaque.",
            "narrateur|L'eau pousse la goutte vers le gravier.",
            "enfant-m|Le gravier !",
            "narrateur|Il veut plonger la main.",
            "narrateur|Il s'arrête, les doigts ouverts.",
            "enfant-m|Pas foncer.",
            "maman|Le gravier râpe le verre, parfois.",
            "narrateur|Nino écoute la flaque, puis le ting.",
        ],
    },
    (3, 2): {
        "lab": "le livre",
        "sons": "pages,chaine,flaque",
        "emphasis": "livre",
        "passage": [
            "narrateur|Nino pose le livre sur le siège de la balançoire.",
            "narrateur|La couverture bleue tremble.",
            "enfant-m|Elle lit, la goutte !",
            "narrateur|Il pousse la balançoire, et tourne une page.",
            "maman|Deux jeux, en même temps ?",
            "narrateur|Le livre glisse.",
            "narrateur|Il tombe vers la flaque, avec la goutte.",
            "enfant-m|Mes deux trésors !",
            "narrateur|Il veut tout attraper.",
            "narrateur|Il s'arrête, les bras en croix.",
            "enfant-m|Un, puis l'autre.",
            "papa|Lequel d'abord, selon toi ?",
            "narrateur|Personne ne choisit à sa place.",
            "narrateur|Nino écoute : le ting, plus près du livre.",
        ],
    },
    (3, 3): {
        "lab": "la dînette",
        "sons": "tasse,chaine,eau",
        "emphasis": "tasse",
        "passage": [
            "narrateur|La dînette s'installe sous la balançoire.",
            "narrateur|La petite tasse penche, blanche.",
            "enfant-m|Un goûter, pour la goutte !",
            "narrateur|Nino verse, la chaîne trop proche.",
            "papa|La chaîne va au thé, tu vois ?",
            "narrateur|Une vraie goutte d'eau tombe dans la tasse.",
            "narrateur|Puis sur le verre, qui se voile.",
            "enfant-m|Je ne la reconnais plus !",
            "narrateur|Il veut frotter, trop vite.",
            "narrateur|Il s'arrête.",
            "enfant-m|Pas foncer.",
            "maman|Le verre aime le souffle, parfois.",
            "narrateur|Personne ne souffle pour lui.",
            "narrateur|Nino approche la bouche, tout près, et attend.",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Les cubes ont failli tout prendre.",
        "papa|On reprend quoi, d'abord ?",
        "maman|Le manteau, le seau, ou le doudou ?",
    ],
    2: [
        "narrateur|Le livre a caché la goutte.",
        "maman|On reprend quoi, d'abord ?",
        "papa|Le manteau, le seau, ou le doudou ?",
    ],
    3: [
        "narrateur|L'eau a voilé le verre.",
        "papa|On reprend quoi, d'abord ?",
        "maman|Le manteau, le seau, ou le doudou ?",
    ],
}

T3_SONS = {1: "tissu,crochet,vitre", 2: "seau,sable,vitre", 3: "doudou,chaise,vitre"}
T3_EMPH = {1: "manteau", 2: "seau", 3: "doudou"}
END_SONS = {1: "sable,vitre,goutte", 2: "metal,vitre,goutte", 3: "chaine,vitre,goutte"}


def t3_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "soulagement_joyeux", 3: "tendresse"}
    tempos = {1: "vif_puis_posé", 2: "prudent", 3: "ample"}
    return (
        f"arc=résolution; intention=faire_vivre_la_réussite; emotion={emos[c]}; "
        f"intensite=2; destinataire=enfant; sous_texte=un_geste_puis_le_ting; "
        f"tempo={tempos[c]}; sourire=franc; respiration=relâchée; chemin={a}{b}{c}"
    )


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_goutte_porte_une_trace; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


T3 = {
    (1, 1, 1): [
        "narrateur|Nino remonte, la goutte contre sa poitrine.",
        "narrateur|La porte du palier va claquer.",
        "enfant-m|J'y vais !",
        "narrateur|Il s'arrête sur la dernière marche.",
        "narrateur|Le grain de quartz brille, à la vitre.",
        "enfant-m|Il m'attend, le grain.",
        "narrateur|Le manteau bleu pend au crochet.",
        "narrateur|La manche pourrait bousculer le verre.",
        "papa|Quelle main, Nino ?",
        "narrateur|Il pose la goutte sur le rebord, d'abord.",
        "narrateur|Ting.",
        "narrateur|Puis il prend le manteau, une manche, l'autre.",
        "maman|Tes deux affaires sont là.",
        "narrateur|Un peu de sable reste sur le poignet du manteau.",
    ],
    (1, 1, 2): [
        "narrateur|Nino remonte, un cube collé au pouce.",
        "narrateur|Le seau jaune attend près des bottes.",
        "enfant-m|Je le prends, et je cours !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, sur la vitre.",
        "enfant-m|D'abord le grain, d'abord le seau.",
        "narrateur|Il glisse la goutte au fond du seau.",
        "narrateur|Le verre fait ting, contre le plastique.",
        "papa|Elle a une maison, maintenant.",
        "maman|Le seau n'est plus vide, tu vois ?",
        "narrateur|Un cube de bois reste au bord, sage.",
        "narrateur|La ventouse ronde attend, vide, à côté du grain.",
        "enfant-m|On a failli laisser le seau.",
        "narrateur|Nino serre l'anse, fier, sans crier.",
    ],
    (1, 1, 3): [
        "narrateur|Nino remonte, les cubes oubliés en bas.",
        "narrateur|Le doudou gris est sur la chaise du palier.",
        "enfant-m|Viens, vite !",
        "narrateur|Il s'arrête, face à la vitre.",
        "narrateur|Le grain de quartz brille, tout petit.",
        "enfant-m|Toi, et lui.",
        "narrateur|Il pose la goutte dans le creux du doudou.",
        "narrateur|Ting, tout mou.",
        "maman|Il l'a gardée au chaud, ton doudou.",
        "papa|La chaise est vide, maintenant.",
        "narrateur|Un grain de sable du bac colle à l'oreille grise.",
        "narrateur|La porte n'a pas claqué, de justesse.",
        "enfant-m|On l'a eue, la goutte.",
        "narrateur|Nino respire, les épaules basses.",
    ],
    (1, 2, 1): [
        "narrateur|Nino remonte, le livre sous le bras.",
        "narrateur|Une page veut s'échapper.",
        "enfant-m|Le manteau, et je file !",
        "narrateur|Il s'arrête au crochet.",
        "narrateur|Le grain de quartz est là, sur la vitre.",
        "enfant-m|Je te vois.",
        "narrateur|Il pose le livre, puis la goutte, sur le rebord.",
        "narrateur|Ting.",
        "narrateur|Le manteau glisse dans ses bras, bleu et lourd.",
        "papa|Une chose, puis l'autre, tu as vu ?",
        "maman|La page s'est calmée, elle aussi.",
        "narrateur|Un grain de sable marque la couverture bleue.",
        "enfant-m|On a failli partir sans lui.",
        "narrateur|Le crochet fait toc, vide, content.",
    ],
    (1, 2, 2): [
        "narrateur|Nino remonte, le livre fermé contre la goutte.",
        "narrateur|Le seau jaune attend, un peu de sable au fond.",
        "enfant-m|Dedans, les deux !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, comme au départ.",
        "papa|Le seau, ou le livre, lequel d'abord ?",
        "narrateur|Nino pose le livre près des bottes.",
        "narrateur|Puis il glisse la goutte dans le seau.",
        "narrateur|Ting, au fond, sur le sable.",
        "maman|Elle a retrouvé sa poussière.",
        "enfant-m|Le palier nous rend le seau.",
        "narrateur|La ventouse ronde reste vide, à côté du grain.",
        "narrateur|Un coin de page porte un grain de sable.",
        "narrateur|Nino serre l'anse, sans courir.",
    ],
    (1, 2, 3): [
        "narrateur|Nino remonte, une page collée au pouce.",
        "narrateur|Le doudou gris regarde depuis la chaise.",
        "enfant-m|Je te prends, on descend !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, collé par la pluie.",
        "enfant-m|Toi d'abord, petit grain.",
        "narrateur|Il pose le livre, puis la goutte, dans les bras gris.",
        "narrateur|Ting, tout près de l'oreille en tissu.",
        "maman|Il a deux trésors, ton doudou.",
        "papa|La chaise peut respirer, maintenant.",
        "narrateur|Un fil de la page reste sur le doudou.",
        "narrateur|La porte du dessous n'a pas claqué.",
        "enfant-m|On l'emmène.",
        "narrateur|Nino descend la marche, lentement.",
    ],
    (1, 3, 1): [
        "narrateur|Nino remonte, la petite tasse à la main.",
        "narrateur|Le manteau bleu pend, un peu lourd d'humidité.",
        "enfant-m|Je m'enroule, et on part !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz perce la buée de la vitre.",
        "enfant-m|Je te vois, malgré l'eau.",
        "narrateur|Il pose la tasse, puis la goutte, sur le rebord.",
        "narrateur|Ting.",
        "narrateur|Le manteau entre, une manche, puis l'autre.",
        "papa|Tes mains sont libres, maintenant.",
        "maman|La tasse peut rentrer, elle aussi.",
        "narrateur|Une trace d'eau de dînette sèche sur le poignet.",
        "enfant-m|On a failli oublier le bleu.",
        "narrateur|Le crochet fait toc, léger.",
    ],
    (1, 3, 2): [
        "narrateur|Nino remonte, la théière qui penche.",
        "narrateur|Le seau jaune attend près des bottes mouillées.",
        "enfant-m|Je verse dans le seau !",
        "narrateur|Il s'arrête, la théière en l'air.",
        "narrateur|Le grain de quartz brille, sec, sur la vitre.",
        "maman|L'eau, ou le seau, lequel ?",
        "narrateur|Nino pose la théière.",
        "narrateur|Il glisse la goutte dans le seau, sans verser.",
        "narrateur|Ting, au fond.",
        "papa|Elle a un nid, sans bain.",
        "enfant-m|Le seau était là, tout le temps.",
        "narrateur|Une tache d'eau sèche sur l'anse jaune.",
        "narrateur|La ventouse ronde garde le grain, à côté.",
        "narrateur|Nino souffle, fier, sans crier.",
    ],
    (1, 3, 3): [
        "narrateur|Nino remonte, la tasse voilée d'eau.",
        "narrateur|Le doudou gris attend sur la chaise.",
        "enfant-m|Essuie, doudou !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, net, à la vitre.",
        "papa|Le tissu, ou le verre, lequel d'abord ?",
        "narrateur|Nino pose la tasse.",
        "narrateur|Il essuie la goutte au coin du doudou, une fois.",
        "narrateur|Ting, clair.",
        "maman|Elle a retrouvé son visage.",
        "enfant-m|Toi, tu viens.",
        "narrateur|Le doudou quitte la chaise, la goutte au creux.",
        "narrateur|Une petite tache d'eau reste sur l'oreille grise.",
        "narrateur|Nino descend, sans courir.",
    ],
    (2, 1, 1): [
        "narrateur|Nino remonte, un cube froid de métal.",
        "narrateur|Le manteau bleu pend au crochet du palier.",
        "enfant-m|Je le mets, et je redescends !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, à la hauteur des yeux.",
        "enfant-m|Tu as vu la pente, toi.",
        "narrateur|Il pose la goutte sur le rebord, loin de la manche.",
        "narrateur|Ting.",
        "narrateur|Le manteau entre, lourd, un peu mouillé.",
        "papa|La pente n'a pas gagné, tu vois ?",
        "maman|Tes épaules ont un toit, maintenant.",
        "narrateur|Une traînée d'eau du toboggan sèche sur le col.",
        "enfant-m|On a failli laisser le bleu.",
        "narrateur|Le crochet fait toc, vide.",
    ],
    (2, 1, 2): [
        "narrateur|Nino remonte, les cubes cliquetant.",
        "narrateur|Le seau jaune attend, un peu de sable au fond.",
        "enfant-m|Les cubes dedans, et la goutte !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, comme un phare minuscule.",
        "maman|Le seau a de la place, oui, mais lentement.",
        "narrateur|Nino pose un cube, puis l'autre, dans le seau.",
        "narrateur|Puis la goutte, au milieu.",
        "narrateur|Ting, entre le bois.",
        "papa|Elle a des murs, ta goutte.",
        "enfant-m|Le toboggan n'a pas tout pris.",
        "narrateur|Une odeur de métal reste sur l'anse.",
        "narrateur|La ventouse ronde attend, vide, près du grain.",
        "narrateur|Nino serre l'anse, sans sauter les marches.",
    ],
    (2, 1, 3): [
        "narrateur|Nino remonte, un cube dans la poche.",
        "narrateur|Le doudou gris est sur la chaise, un peu penché.",
        "enfant-m|On glisse ensemble !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, collé par la pluie.",
        "enfant-m|Pas la pente, ici.",
        "narrateur|Il pose la goutte dans les bras du doudou.",
        "narrateur|Ting, tout près du tissu.",
        "papa|Il l'a reçue, ton doudou.",
        "maman|La chaise est libre, maintenant.",
        "narrateur|Un reflet de métal danse sur l'œil du doudou.",
        "narrateur|Deux étages plus bas, la porte n'a pas claqué.",
        "enfant-m|On l'a gardée.",
        "narrateur|Nino descend, le doudou contre lui.",
    ],
    (2, 2, 1): [
        "narrateur|Nino remonte, le livre fermé trop vite.",
        "narrateur|Une page dépasse, froissée par le vent.",
        "enfant-m|Le manteau cache tout !",
        "narrateur|Il s'arrête au crochet.",
        "narrateur|Le grain de quartz est là, net, sur la vitre.",
        "papa|Le manteau, ou le livre, lequel ?",
        "narrateur|Nino pose le livre sur la chaise.",
        "narrateur|Puis la goutte, sur le rebord.",
        "narrateur|Ting.",
        "narrateur|Le manteau glisse, bleu, sur ses épaules.",
        "maman|La page peut se reposer, maintenant.",
        "enfant-m|On a failli partir en papier.",
        "narrateur|Un fil d'eau du toboggan sèche sur la manche.",
        "narrateur|Le crochet fait toc, léger.",
    ],
    (2, 2, 2): [
        "narrateur|Nino remonte, le livre comme un toit.",
        "narrateur|Le seau jaune attend près des bottes.",
        "enfant-m|Le livre dans le seau !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, à côté de la ventouse.",
        "maman|Le papier n'aime pas le fond, parfois.",
        "narrateur|Nino pose le livre à côté, pas dedans.",
        "narrateur|Il glisse la goutte dans le seau.",
        "narrateur|Ting, sur le sable.",
        "papa|Elle a sa maison, le livre a la sienne.",
        "enfant-m|Deux places.",
        "narrateur|Une page garde une traînée d'eau, mince.",
        "narrateur|Nino prend l'anse, et le livre sous l'autre bras.",
        "narrateur|Les marches restent sages, sous ses pieds.",
    ],
    (2, 2, 3): [
        "narrateur|Nino remonte, le livre serré trop fort.",
        "narrateur|Le doudou gris attend, une oreille pliée.",
        "enfant-m|Il tient le livre, lui !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, collé au verre de la vitre.",
        "enfant-m|Toi, d'abord.",
        "narrateur|Il pose le livre.",
        "narrateur|Puis la goutte, dans le creux du doudou.",
        "narrateur|Ting.",
        "papa|Il a les bras pour elle.",
        "maman|Le livre peut fermer sa couverture.",
        "narrateur|Un coin de page reste dans la patte grise.",
        "enfant-m|On a failli tout laisser glisser.",
        "narrateur|Nino descend, sans sauter.",
    ],
    (2, 3, 1): [
        "narrateur|Nino remonte, la tasse mouillée.",
        "narrateur|Le manteau bleu pend, prêt à tout essuyer.",
        "enfant-m|La manche, comme un linge !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz perce, sec, à la vitre.",
        "papa|La manche aime rester sèche, non ?",
        "narrateur|Nino pose la tasse, puis la goutte, sur le rebord.",
        "narrateur|Ting.",
        "narrateur|Il enfile le manteau, sans frotter le verre.",
        "maman|Deux métiers, deux temps.",
        "enfant-m|On a failli tout mouiller.",
        "narrateur|Une goutte d'eau de dînette sèche sur le bouton.",
        "narrateur|Le crochet fait toc.",
        "narrateur|Nino souffle, le col chaud.",
    ],
    (2, 3, 2): [
        "narrateur|Nino ramène la théière, trop pleine.",
        "narrateur|Le seau jaune attend, comme une cuvette.",
        "enfant-m|Je vide tout !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, sans buée.",
        "maman|Le seau, pour la goutte, pas pour la mer.",
        "narrateur|Nino pose la théière près des bottes.",
        "narrateur|Il glisse la goutte au fond du seau, seul.",
        "narrateur|Ting.",
        "papa|Elle a de la place, sans nager.",
        "enfant-m|Le toboggan a assez d'eau, lui.",
        "narrateur|Une odeur de plastique mouillé monte.",
        "narrateur|La ventouse ronde garde le grain, à côté.",
        "narrateur|Nino prend l'anse, fier, sans verser.",
    ],
    (2, 3, 3): [
        "narrateur|Nino remonte, la tasse floue.",
        "narrateur|Le doudou gris peut essuyer, trop vite.",
        "enfant-m|Frotte, frotte !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, net.",
        "papa|Un souffle, parfois, suffit.",
        "narrateur|Nino souffle sur la goutte, une fois.",
        "narrateur|Le verre redevient clair.",
        "narrateur|Ting, dans les bras du doudou.",
        "maman|Il l'a reçue propre, ton doudou.",
        "enfant-m|On a failli la rayer.",
        "narrateur|Une petite buée reste sur l'oreille, puis part.",
        "narrateur|La chaise du palier est vide.",
        "narrateur|Nino descend, le doudou contre sa joue.",
    ],
    (3, 1, 1): [
        "narrateur|Nino remonte, un cube mouillé de flaque.",
        "narrateur|Le manteau bleu pend au crochet.",
        "enfant-m|Je le mets, on se balance !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, à la vitre.",
        "enfant-m|La chaîne n'est pas ici.",
        "narrateur|Il pose la goutte sur le rebord, loin du tissu.",
        "narrateur|Ting.",
        "narrateur|Le manteau entre, une manche, l'autre.",
        "papa|Tes épaules ont un toit, sans chaîne.",
        "maman|Le cube peut sécher, près des bottes.",
        "narrateur|Un cliquetis de chaîne reste dans l'air, puis s'en va.",
        "enfant-m|On a failli laisser le bleu.",
        "narrateur|Le crochet fait toc, vide.",
    ],
    (3, 1, 2): [
        "narrateur|Nino remonte, deux cubes trop pleins d'eau.",
        "narrateur|Le seau jaune attend, près des bottes.",
        "enfant-m|Tout dans le seau !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, collé par la pluie.",
        "maman|Un cube, tu le poses, tu regardes ?",
        "narrateur|Nino pose un cube, puis l'autre, à côté du seau.",
        "narrateur|Puis la goutte, au fond, seule.",
        "narrateur|Ting.",
        "papa|Elle a de l'espace, ta goutte.",
        "enfant-m|La flaque n'a pas gagné.",
        "narrateur|Une odeur de bois mouillé reste sur l'anse.",
        "narrateur|La ventouse ronde attend, vide, près du grain.",
        "narrateur|Nino serre l'anse, sans courir.",
    ],
    (3, 1, 3): [
        "narrateur|Nino remonte, un cube dans chaque main.",
        "narrateur|Le doudou gris n'a plus de place.",
        "enfant-m|Il tient les cubes !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, à hauteur de chaise.",
        "papa|Le doudou a les bras pour la goutte, non ?",
        "narrateur|Nino pose les cubes près des bottes.",
        "narrateur|Il glisse la goutte dans le creux gris.",
        "narrateur|Ting, tout mou.",
        "maman|Il l'a, maintenant.",
        "enfant-m|On a failli trop lui donner.",
        "narrateur|Un reflet de chaîne danse sur l'œil du doudou.",
        "narrateur|La chaise est vide.",
        "narrateur|Nino descend, sans sauter.",
    ],
    (3, 2, 1): [
        "narrateur|Nino remonte, le livre trop ouvert.",
        "narrateur|Le manteau bleu peut servir de marque-page.",
        "enfant-m|La manche dans le livre !",
        "narrateur|Il s'arrête au crochet.",
        "narrateur|Le grain de quartz est là, net.",
        "maman|Le manteau aime les épaules, le livre la chaise.",
        "narrateur|Nino pose le livre, fermé, sur la chaise.",
        "narrateur|Puis la goutte, sur le rebord.",
        "narrateur|Ting.",
        "narrateur|Le manteau glisse, bleu, sans page.",
        "papa|Deux places, deux choses.",
        "enfant-m|On a failli tout mélanger.",
        "narrateur|Un cliquetis de chaîne s'éloigne, en bas.",
        "narrateur|Le crochet fait toc.",
    ],
    (3, 2, 2): [
        "narrateur|Nino remonte, le livre au-dessus de la flaque, dans sa tête.",
        "narrateur|Le seau jaune attend, comme un port.",
        "enfant-m|Le livre navigue dans le seau !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz cligne, à côté de la ventouse.",
        "papa|Le papier n'aime pas nager, toi tu le sais.",
        "narrateur|Nino pose le livre près des bottes.",
        "narrateur|Il glisse la goutte dans le seau.",
        "narrateur|Ting, au fond.",
        "maman|Elle a son quai, le livre a le sec.",
        "enfant-m|Deux voyages.",
        "narrateur|Une page garde un point d'eau, minuscule.",
        "narrateur|Nino prend l'anse, le livre sous l'autre bras.",
        "narrateur|Les marches sonnent, une par une.",
    ],
    (3, 2, 3): [
        "narrateur|Nino remonte, le livre et la goutte trop serrés.",
        "narrateur|Le doudou gris peut les tenir tous.",
        "enfant-m|Tout dans ses bras !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, collé par la pluie.",
        "enfant-m|Toi, d'abord, petit grain.",
        "narrateur|Nino pose le livre sur la chaise.",
        "narrateur|Puis la goutte, seule, dans le creux du doudou.",
        "narrateur|Ting.",
        "papa|Un trésor, des bras.",
        "maman|Le livre garde sa place, lui.",
        "enfant-m|On a failli trop charger.",
        "narrateur|Un fil de page reste sur l'oreille grise.",
        "narrateur|Nino descend, le doudou contre lui.",
    ],
    (3, 3, 1): [
        "narrateur|Nino remonte, la tasse qui cliquette.",
        "narrateur|Le manteau bleu pend, prêt à cacher la tasse.",
        "enfant-m|Dans la poche !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz perce, à la vitre.",
        "papa|La poche aime les mains, la tasse l'étagère.",
        "narrateur|Nino pose la tasse près des bottes.",
        "narrateur|Puis la goutte, sur le rebord.",
        "narrateur|Ting.",
        "narrateur|Le manteau entre, sans poche trop pleine.",
        "maman|Tes épaules sont libres, et chaudes.",
        "enfant-m|On a failli tout coincer.",
        "narrateur|Un reflet de chaîne sèche sur le bouton.",
        "narrateur|Le crochet fait toc, vide.",
    ],
    (3, 3, 2): [
        "narrateur|Nino remonte, la théière trop près de la chaîne, dans sa tête.",
        "narrateur|Le seau jaune attend, large.",
        "enfant-m|Le goûter, dans le seau !",
        "narrateur|Il s'arrête.",
        "narrateur|Le grain de quartz brille, sans buée.",
        "maman|Le seau pour la goutte, la tasse pour plus tard.",
        "narrateur|Nino pose la théière.",
        "narrateur|Il glisse la goutte au fond du seau.",
        "narrateur|Ting.",
        "papa|Elle a un nid, sans thé.",
        "enfant-m|La balançoire a assez dansé.",
        "narrateur|Une odeur de plastique et de tissu mouillé monte.",
        "narrateur|La ventouse ronde garde le grain, à côté.",
        "narrateur|Nino prend l'anse, sans verser.",
    ],
    (3, 3, 3): [
        "narrateur|Nino remonte, la tasse et le doudou trop proches.",
        "narrateur|Le doudou gris pourrait tout essuyer, trop fort.",
        "enfant-m|Frotte le verre !",
        "narrateur|Il s'arrête, face à la vitre.",
        "narrateur|Le grain de quartz cligne, net, comme au début.",
        "enfant-m|Je te vois, grain.",
        "narrateur|Nino souffle sur la goutte, une fois.",
        "narrateur|Puis il la pose dans les bras du doudou.",
        "narrateur|Ting, clair.",
        "papa|Il l'a, propre.",
        "maman|La chaise peut se reposer.",
        "enfant-m|On a failli la rayer, et l'oublier.",
        "narrateur|Une petite buée quitte l'oreille grise.",
        "narrateur|Nino descend, fier, sans courir.",
    ],
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Au rebord, la goutte de verre retrouve la ventouse.",
        "enfant-m|Ting, maman.",
        "maman|Elle a du sable, sur le bord.",
        "papa|Comme le grain de quartz, à côté.",
        "enfant-m|Deux grains, maintenant.",
        "narrateur|Le manteau bleu sèche au crochet, un peu de bac au poignet.",
        "narrateur|La vitre garde le grain, et la goutte, face à la cour chocolat.",
    ],
    (1, 1, 2): [
        "narrateur|Dans le seau, la goutte fait ting, sur le sable.",
        "enfant-m|Elle a une maison jaune.",
        "papa|Le grain de quartz la regarde, depuis la vitre.",
        "maman|Deux lumières, une en haut, une au fond.",
        "enfant-m|On a failli laisser le seau.",
        "narrateur|Un cube de bois reste au bord, sage.",
        "narrateur|Le palier sent le caoutchouc, et un peu le sapin.",
    ],
    (1, 1, 3): [
        "narrateur|Le doudou tient la goutte, près de la chaise vide.",
        "enfant-m|Elle est au chaud.",
        "maman|Le grain de quartz cligne, à la vitre.",
        "papa|Il a vu le bac, lui aussi.",
        "enfant-m|Un grain de sable sur son oreille.",
        "narrateur|Nino pose sa joue contre le tissu gris.",
        "narrateur|La cour, en bas, garde un château écroulé, et c'est bien.",
    ],
    (1, 2, 1): [
        "narrateur|La goutte pend à la ventouse, lourde d'un grain de sable.",
        "enfant-m|Le manteau est là.",
        "papa|Le grain de quartz a un voisin, maintenant.",
        "maman|La page s'est calmée, sur la chaise.",
        "enfant-m|On a lu, un peu.",
        "narrateur|Le crochet fait toc, léger.",
        "narrateur|Sur la couverture bleue, un grain de sable brille, comme en haut.",
    ],
    (1, 2, 2): [
        "narrateur|Le seau jaune tient la goutte, près des bottes.",
        "enfant-m|Elle a du sable, comme au bac.",
        "maman|Le grain de quartz reste à la vitre, sec.",
        "papa|Deux maisons : le seau, et le verre.",
        "enfant-m|Le livre, lui, reste au sec.",
        "narrateur|Nino pose l'anse, sans la lâcher trop tôt.",
        "narrateur|Un coin de page porte un grain, face à la cour.",
    ],
    (1, 2, 3): [
        "narrateur|Le doudou a la goutte, et le livre a la chaise.",
        "enfant-m|Deux places.",
        "papa|Le grain de quartz cligne, content.",
        "maman|Un fil de page sur l'oreille, tu vois ?",
        "enfant-m|C'est notre secret.",
        "narrateur|Nino descend une marche, puis s'arrête.",
        "narrateur|La vitre garde le grain, et l'odeur du bac entre.",
    ],
    (1, 3, 1): [
        "narrateur|La goutte retrouve la ventouse, claire après la buée.",
        "enfant-m|Le manteau est mis.",
        "maman|Le grain de quartz perce, net.",
        "papa|Une trace d'eau sur le poignet, puis plus.",
        "enfant-m|La tasse rentre, elle aussi.",
        "narrateur|Le crochet fait toc.",
        "narrateur|La cour chocolat luit, sous la vitre du palier.",
    ],
    (1, 3, 2): [
        "narrateur|Au fond du seau, la goutte fait ting, sans nager.",
        "enfant-m|Pas de thé, juste elle.",
        "papa|Le grain de quartz la regarde, sec.",
        "maman|L'anse a une tache d'eau, qui sèche.",
        "enfant-m|On a failli tout verser.",
        "narrateur|Nino pose le seau près des bottes, droit.",
        "narrateur|La ventouse ronde garde le grain, et le palier redevient tiède.",
    ],
    (1, 3, 3): [
        "narrateur|Le doudou tient une goutte claire, près de l'oreille.",
        "enfant-m|Elle a son visage.",
        "maman|Le grain de quartz cligne, comme un œil.",
        "papa|Une tache d'eau sur le tissu, minuscule.",
        "enfant-m|On a soufflé, tous les deux.",
        "narrateur|La chaise du palier reste vide, contente.",
        "narrateur|En bas, le bac garde un creux de main, dans le sable.",
    ],
    (2, 1, 1): [
        "narrateur|La goutte pend, une traînée d'eau sur le verre.",
        "enfant-m|Comme le toboggan.",
        "papa|Le grain de quartz est sec, lui.",
        "maman|Le manteau a le col un peu mouillé.",
        "enfant-m|Mes épaules ont un toit.",
        "narrateur|Le crochet fait toc, vide.",
        "narrateur|La pente, en bas, luit, sans la goutte.",
    ],
    (2, 1, 2): [
        "narrateur|Dans le seau, la goutte tient entre deux cubes.",
        "enfant-m|Une maison d'escalier.",
        "maman|Le grain de quartz la voit, depuis la vitre.",
        "papa|Le métal n'a pas tout pris.",
        "enfant-m|L'anse sent le toboggan, un peu.",
        "narrateur|Nino ne saute pas les marches.",
        "narrateur|La ventouse ronde reste vide, le grain à côté, patient.",
    ],
    (2, 1, 3): [
        "narrateur|Le doudou a la goutte, un reflet de métal dans l'œil.",
        "enfant-m|Elle a glissé, et elle est là.",
        "papa|Le grain de quartz cligne, en haut.",
        "maman|La chaise est libre.",
        "enfant-m|On l'a gardée.",
        "narrateur|Nino pose sa joue, le tissu gris un peu froid.",
        "narrateur|Le toboggan, en bas, garde une traînée, et c'est tout.",
    ],
    (2, 2, 1): [
        "narrateur|La goutte retrouve la ventouse, une page plus loin.",
        "enfant-m|Le manteau est sur moi.",
        "maman|Le grain de quartz a un voisin de verre.",
        "papa|La page froissée sèche, sur la chaise.",
        "enfant-m|Le vent n'a pas gagné.",
        "narrateur|Un fil d'eau sèche sur la manche bleue.",
        "narrateur|Le palier sent le papier, et le caoutchouc.",
    ],
    (2, 2, 2): [
        "narrateur|Le seau tient la goutte, le livre reste au sec.",
        "enfant-m|Deux maisons.",
        "papa|Le grain de quartz cligne, à côté de la ventouse.",
        "maman|Une page a une traînée d'eau, mince.",
        "enfant-m|Le papier n'a pas nagé.",
        "narrateur|Nino a l'anse, et le livre sous l'autre bras.",
        "narrateur|Les marches du palier sonnent, sages, une par une.",
    ],
    (2, 2, 3): [
        "narrateur|Le doudou tient la goutte, le livre sur la chaise.",
        "enfant-m|Un coin de page dans sa patte.",
        "maman|Le grain de quartz brille, collé.",
        "papa|Il a les bras pour elle, pas pour tout.",
        "enfant-m|On a failli tout laisser glisser.",
        "narrateur|Nino descend, sans sauter.",
        "narrateur|La vitre garde le grain, face à la pente luisante.",
    ],
    (2, 3, 1): [
        "narrateur|La goutte pend, claire, le manteau chaud.",
        "enfant-m|La manche est sèche.",
        "papa|Le grain de quartz perce, net.",
        "maman|Un bouton a une goutte d'eau de dînette, qui s'en va.",
        "enfant-m|Deux temps, tu as dit.",
        "narrateur|Le crochet fait toc.",
        "narrateur|Le toboggan, en bas, n'a plus la goutte, seulement l'eau vraie.",
    ],
    (2, 3, 2): [
        "narrateur|Au fond du seau, la goutte fait ting, seule.",
        "enfant-m|Pas la mer, juste elle.",
        "maman|Le grain de quartz la regarde, sans buée.",
        "papa|La théière reste près des bottes, sage.",
        "enfant-m|Le toboggan a assez d'eau.",
        "narrateur|Nino pose l'anse, droit.",
        "narrateur|La ventouse ronde et le grain partagent la vitre, tiède.",
    ],
    (2, 3, 3): [
        "narrateur|Le doudou tient une goutte claire, près de la joue.",
        "enfant-m|On a soufflé.",
        "papa|Le grain de quartz cligne, net.",
        "maman|Une buée quitte l'oreille, puis plus.",
        "enfant-m|On a failli la rayer.",
        "narrateur|La chaise du palier est vide.",
        "narrateur|En bas, la rampe du toboggan sèche, sans le verre.",
    ],
    (3, 1, 1): [
        "narrateur|La goutte pend à la ventouse, loin de la chaîne.",
        "enfant-m|Le manteau est un toit.",
        "maman|Le grain de quartz brille, à hauteur d'yeux.",
        "papa|Un cube sèche près des bottes.",
        "enfant-m|La chaîne n'est pas ici.",
        "narrateur|Le crochet fait toc, vide.",
        "narrateur|Les balançoires, en bas, cliquent plus loin, plus sages.",
    ],
    (3, 1, 2): [
        "narrateur|Dans le seau, la goutte fait ting, seule, au fond.",
        "enfant-m|Les cubes à côté, pas dessus.",
        "papa|Le grain de quartz cligne, collé par la pluie.",
        "maman|La flaque n'a pas gagné.",
        "enfant-m|Elle a de l'espace.",
        "narrateur|L'anse sent le bois mouillé, un peu.",
        "narrateur|La ventouse ronde attend, vide, le grain tout près.",
    ],
    (3, 1, 3): [
        "narrateur|Le doudou a la goutte, les cubes près des bottes.",
        "enfant-m|Ses bras sont pour elle.",
        "maman|Le grain de quartz brille, à hauteur de chaise.",
        "papa|Un reflet de chaîne dans l'œil, puis plus.",
        "enfant-m|On a failli trop lui donner.",
        "narrateur|Nino descend, sans sauter.",
        "narrateur|La vitre garde le grain, face aux balançoires arrêtées.",
    ],
    (3, 2, 1): [
        "narrateur|La goutte retrouve la ventouse, le manteau sur les épaules.",
        "enfant-m|Pas de page dans la manche.",
        "papa|Le grain de quartz a son voisin de verre.",
        "maman|Le livre sèche, fermé, sur la chaise.",
        "enfant-m|Deux places.",
        "narrateur|Un cliquetis de chaîne s'éloigne.",
        "narrateur|Le palier sent le papier, et le tissu bleu.",
    ],
    (3, 2, 2): [
        "narrateur|Le seau tient la goutte, le livre reste au sec.",
        "enfant-m|Elle a un quai jaune.",
        "maman|Le grain de quartz cligne, à côté de la ventouse.",
        "papa|Une page a un point d'eau, minuscule.",
        "enfant-m|Deux voyages.",
        "narrateur|Les marches sonnent, une par une.",
        "narrateur|En bas, le siège de la balançoire reste vide, luisant.",
    ],
    (3, 2, 3): [
        "narrateur|Le doudou tient la goutte, le livre sur la chaise.",
        "enfant-m|Un fil de page sur l'oreille.",
        "papa|Le grain de quartz brille, collé par la pluie.",
        "maman|Un trésor, des bras.",
        "enfant-m|On a failli trop charger.",
        "narrateur|Nino pose sa joue, le tissu gris tiède.",
        "narrateur|La vitre garde le grain, et la cour redevient calme.",
    ],
    (3, 3, 1): [
        "narrateur|La goutte pend, le manteau chaud, la tasse près des bottes.",
        "enfant-m|Pas dans la poche.",
        "maman|Le grain de quartz perce, net.",
        "papa|Tes épaules sont libres.",
        "enfant-m|On a failli tout coincer.",
        "narrateur|Le crochet fait toc, vide.",
        "narrateur|Un reflet de chaîne sèche sur le bouton, puis s'en va.",
    ],
    (3, 3, 2): [
        "narrateur|Au fond du seau, la goutte fait ting, sans thé.",
        "enfant-m|Un nid, pas un goûter.",
        "papa|Le grain de quartz la voit, sans buée.",
        "maman|La balançoire a assez dansé.",
        "enfant-m|L'anse est à moi.",
        "narrateur|Nino pose le seau, droit, près des bottes.",
        "narrateur|La ventouse et le grain partagent la vitre, face à la flaque vide.",
    ],
    (3, 3, 3): [
        "narrateur|Le doudou tient une goutte claire, l'oreille sèche.",
        "enfant-m|Je te vois, grain.",
        "maman|Le grain de quartz cligne, comme au début.",
        "papa|On a failli, et puis on a eu.",
        "enfant-m|Ting.",
        "narrateur|Nino descend, fier, sans courir.",
        "narrateur|Sur la vitre du palier, le grain et la goutte se regardent, enfin.",
    ],
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
        by_src["CHK_T0000_P0000"], OPENING, "opening", "cles,radiateur,vitre"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {
            "fields": {
                "option_1_label": "le bac à sable",
                "option_2_label": "le toboggan",
                "option_3_label": "les balançoires",
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
            {"emphasis": "fais quoi", "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": "goutte"}
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
                        "option_1_label": "le manteau",
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
                    {"emphasis": T3_EMPH[c], "note": t3_note(a, b, c)},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    ENDINGS[(a, b, c)],
                    "ending",
                    END_SONS[a],
                    {"emphasis": "goutte", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = (
        "Nino, au palier, veut descendre la goutte de verre jusqu'à la cour "
        "avant que les flaques ne partent. Il prend goutte, manteau, seau et "
        "doudou ensemble : toc, la goutte glisse. Bac, toboggan ou balançoires "
        "changent le premier revers. Cubes, livre ou dînette amènent une seconde "
        "ruse plus rusée. Manteau, seau ou doudou changent le climax : il "
        "reprend ses affaires, le grain de quartz de la vitre se paie. "
        "Vingt-sept fins : la goutte porte une trace."
    )
    story["title"] = TITLE
    story["characters"] = "Nino, papa, maman"
    story["setting"] = "palier d'immeuble, vitre sur la cour, après la pluie"
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
    if min(counts) < 550 or max(counts) > 720:
        raise SystemExit(f"longueur chemins hors cible 550-700: {min(counts)}-{max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if not all(c.get("text_xai_tags") != c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Public :** N3 (3–6 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.003 — reprendre ses affaires, vécue "
        "(Nino reprend la goutte, puis manteau, seau ou doudou), jamais dite\n"
        "- **Personnages :** Nino, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "## Vécu\n\n"
        "Palier d'immeuble, clés sur le radiateur, caoutchouc mouillé, "
        "goutte de verre à la ventouse (ting), grain de quartz collé à la vitre. "
        "Désir : descendre la goutte jusqu'à la cour avant que les flaques ne partent. "
        "Première idée : goutte + manteau + seau + doudou. Toc, ça glisse. "
        "Papa plie les genoux. Merci vécu : tu l'as gardée. "
        "Chaque branche est une autre histoire :\n\n"
        "- T1 coins (goutte AVEC) : bac chocolat (château qui s'écroule) / "
        "toboggan luisant (la goutte file) / balançoires (chaîne folle, flaque)\n"
        "- T2 seconde ruse : cubes (grille, gouttière, gravier) / livre (couverture-piège, "
        "pages, deux trésors) / dînette (buée, main sablée, chaîne dans le thé)\n"
        "- T3 climax : manteau (crochet, manche) / seau (anse, fond) / doudou (chaise, creux). "
        "Il refuse de foncer, retrouve le grain de quartz, reprend l'affaire. "
        "Ça a failli (porte, voisin, rayer, verser).\n\n"
        "Q = reprendre. Fin : la goutte porte une trace, le grain du début se paie, sans morale.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Héros Nino (D16). Décor xlsx : palier, vitre, cour après la pluie.\n"
        "- Ouverture inventée (clés, radiateur, cage d'escalier) : pas les cinq gabarits v2.\n"
        "- Indice unique : grain de quartz sur la vitre (ouverture + climax). "
        "Pas ancre / étoile / fil pâle / merle / miel / gouttes-refrain.\n"
        "- Monde ≠ TREE-DIF-037 (Aniss, roue, vis verte) ≠ TREE-DIF-068 "
        "(Victorina, portrait, cire) ≠ TREE-COL-008 (jardin, arrosoir, laitue).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés. Pas « on va ranger ».\n"
        "- 1er choix = coins, n'enlève pas l'équipement (la goutte part avec).\n"
        "- T1/T2/T3 changent obstacle et climax. 9 T2, 27 T3, 27 fins, 27 dernières images.\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration), `style_energy`, "
        "pauses, pitch, volume. `slow` = choix, indice, fin.\n"
        f"- Chemins {min(counts)}–{max(counts)} mots "
        f"(moy. {sum(counts)//len(counts)}). `check()` N3≤16. Pas apply.\n"
        "- Relu : ouverture + 3 L1 + 9 L2 + 27 L3/fins.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
