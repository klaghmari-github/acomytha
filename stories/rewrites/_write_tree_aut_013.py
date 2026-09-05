#!/usr/bin/env python3
"""TREE-AUT-013 — Le carré d'or sur le plancher (F-NAR-019, N3, AUT.ROU.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-013"
N3 = 16
TITLE = "Le carré d'or sur le plancher"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="carré d'or",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_coquille_doit_attraper_l_or; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="chose",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=une_main_puis_l_autre; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="coquille",
        note="arc=confirmation; intention=relancer; emotion=élan_prudent; intensite=1; destinataire=enfant; sous_texte=le_carré_glisse_toujours; tempo=naturel; sourire=léger; respiration=fluide",
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
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=la_seconde_ruse_mange_l_or; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="coquille",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=un_geste_puis_le_clic; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="mer",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_coquille_a_gardé_l_or; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|La maison sur la dune a le bois tiède.",
    "narrateur|Un grain de sable brille sur le plancher.",
    "narrateur|Le soleil en fait un carré d'or.",
    "narrateur|Ça sent le sel, et un peu le pain.",
    "narrateur|Sur le rebord, une coquille striée attend.",
    "narrateur|Elle est rose et blanche, légère.",
    "narrateur|Si on la pose, elle fait clic.",
    "narrateur|Dehors, le phare du jardin pointe vers l'eau.",
    "narrateur|Un parasol jaune tremble au vent.",
    "papa|Tu entends la mer, Raphaël ?",
    "narrateur|Papa pousse les volets.",
    "narrateur|Les volets font clic, comme la coquille.",
    "maman|L'eau de la casserole chante.",
    "narrateur|En ce moment, Raphaël ouvre les yeux.",
    "narrateur|Ses pieds cherchent le tapis rêche.",
    "enfant-m|Je mets la coquille dans le carré !",
    "enfant-m|Après, le parasol, et la mer !",
    "papa|Le carré glisse vers la porte, tu vois ?",
    "narrateur|Raphaël attrape la coquille, le pull, une chaussure.",
    "narrateur|Trop de choses pour deux petites mains.",
    "narrateur|La coquille file sous le tapis.",
    "narrateur|Clic.",
    "narrateur|La chaussure tombe.",
    "narrateur|Toc.",
    "narrateur|Le carré d'or recule vers la porte.",
    "enfant-m|Il part !",
    "maman|Quelle main est vide, là ?",
]

T1_CHOICE = [
    "narrateur|Le carré d'or fuit le plancher, lentement.",
    "papa|On commence où, Raphaël ?",
    "maman|La cuisine, le jardin, ou la chambre ?",
]

T1 = {
    1: {
        "lab": "la cuisine",
        "sons": "bol,lait,carrelage",
        "emphasis": "bol",
        "passage": [
            "narrateur|Raphaël pousse la porte de la cuisine.",
            "narrateur|Le carrelage est frais sous ses pieds.",
            "narrateur|Le pain fume près du bol.",
            "enfant-m|Le bol, le carré, et la mer !",
            "narrateur|Il tire la chaise et le bol ensemble.",
            "narrateur|La chaise crie.",
            "narrateur|Le lait danse au bord.",
            "maman|Le bol va tomber, tu sens ?",
            "narrateur|Une goutte file sur le carrelage.",
            "narrateur|Elle coupe le carré d'or en deux.",
            "enfant-m|Mon or, il se casse !",
            "papa|Tes deux mains tiennent trop, non ?",
            "narrateur|Raphaël pose le bol de travers.",
            "narrateur|Dans sa poche, la coquille fait clic.",
            "enfant-m|Je voulais les trois d'un coup.",
            "narrateur|Ses épaules baissent, un peu.",
        ],
        "question": [
            "narrateur|Raphaël a tiré la chaise et le bol ensemble.",
            "maman|Il fait comment, pour garder le carré ?",
        ],
        "qfields": {
            "expected_answer": "une chose",
            "accepted_examples": (
                "une chose | puis l'autre | d'abord | une chose puis l'autre | "
                "puis la suivante | le bol | une main | poser le bol"
            ),
            "retry_prompt": "Il a trop dans les mains. Il fait comment ?",
            "engine_ok_text": "Oui. Une chose d'abord.",
            "engine_near_text": "Tu es tout près. Écoute l'indice.",
        },
        "confirm": [
            "enfant-m|Une chose !",
            "narrateur|Oui, Raphaël pose le bol, seulement.",
            "narrateur|Il boit une gorgée.",
            "narrateur|Le lait est tiède.",
            "papa|Merci, tes mains sont libres.",
            "narrateur|La coquille sort de la poche.",
            "narrateur|Clic.",
            "maman|Le carré avance vers la porte, tu vois ?",
            "enfant-m|On le rattrape !",
            "narrateur|Une miette brille, comme un grain de sable.",
        ],
    },
    2: {
        "lab": "le jardin",
        "sons": "vent,parasol,sable",
        "emphasis": "parasol",
        "passage": [
            "narrateur|Raphaël ouvre la porte du jardin.",
            "narrateur|Le vent sent le thym et le sel.",
            "narrateur|Le phare du jardin cligne vers l'eau.",
            "enfant-m|Je cours au carré !",
            "narrateur|Le carré d'or chauffe la pierre du banc.",
            "narrateur|Raphaël part avec une seule chaussure.",
            "narrateur|Le sable du chemin pique l'autre pied.",
            "papa|Tes pieds ne sont pas d'accord, là.",
            "narrateur|Le parasol jaune se penche.",
            "narrateur|Son ombre mange un coin de l'or.",
            "enfant-m|Le carré rétrécit !",
            "maman|Tu as mis les deux chaussures ?",
            "narrateur|Raphaël s'arrête, le pied levé.",
            "narrateur|La coquille, dans sa main, glisse.",
            "enfant-m|Aïe, le sable est méchant !",
            "narrateur|Il souffle, les joues chaudes.",
        ],
        "question": [
            "narrateur|Raphaël a couru avec une seule chaussure.",
            "papa|Il fait comment, pour garder le carré ?",
        ],
        "qfields": {
            "expected_answer": "une chose",
            "accepted_examples": (
                "une chose | puis l'autre | d'abord | une chose puis l'autre | "
                "puis la suivante | les chaussures | une chaussure | les deux"
            ),
            "retry_prompt": "Un pied est nu. Il fait comment ?",
            "engine_ok_text": "Oui. Une chose d'abord.",
            "engine_near_text": "Tu es tout près. Écoute l'indice.",
        },
        "confirm": [
            "enfant-m|Une chose !",
            "narrateur|Oui, Raphaël enfile la chaussure gauche.",
            "narrateur|Puis la droite.",
            "narrateur|Ça fait toc toc sur la pierre.",
            "maman|Merci, tes pieds peuvent marcher.",
            "narrateur|La coquille revient dans sa main.",
            "narrateur|Clic.",
            "papa|Le parasol a pris un bout d'or, tu vois ?",
            "enfant-m|On le reprend !",
            "narrateur|Une feuille de figuier tremble, près du phare.",
        ],
    },
    3: {
        "lab": "la chambre",
        "sons": "tissu,drap,tapis",
        "emphasis": "pull",
        "passage": [
            "narrateur|Raphaël revient vers la chambre.",
            "narrateur|Le drap est chaud, un peu froissé.",
            "narrateur|Le pull bleu attend sur la chaise.",
            "enfant-m|Le carré, et la mer !",
            "narrateur|Il passe la tête dans le pull.",
            "narrateur|La coquille reste dans sa main fermée.",
            "narrateur|Le tricot gratte.",
            "narrateur|La coquille file dans les draps.",
            "enfant-m|Elle est perdue !",
            "papa|Tes deux mains faisaient deux métiers, non ?",
            "maman|Le carré attend près de la porte.",
            "narrateur|Raphaël fouille le drap, trop vite.",
            "narrateur|Le tapis rêche cache le clic.",
            "enfant-m|Je la veux, et le pull aussi.",
            "narrateur|Ses yeux piquent un peu.",
            "narrateur|Le carré d'or, sur le tapis, recule.",
        ],
        "question": [
            "narrateur|Raphaël a pris le pull et la coquille ensemble.",
            "maman|Il fait comment, pour garder le carré ?",
        ],
        "qfields": {
            "expected_answer": "une chose",
            "accepted_examples": (
                "une chose | puis l'autre | d'abord | une chose puis l'autre | "
                "puis la suivante | le pull | poser la coquille | une main"
            ),
            "retry_prompt": "Pull et coquille ensemble. Il fait comment ?",
            "engine_ok_text": "Oui. Une chose d'abord.",
            "engine_near_text": "Tu es tout près. Écoute l'indice.",
        },
        "confirm": [
            "enfant-m|Une chose !",
            "narrateur|Oui, Raphaël pose la coquille sur la chaise.",
            "narrateur|Clic.",
            "narrateur|Il enfile le pull, les deux manches.",
            "papa|Merci, tes mains sont à elle, maintenant.",
            "narrateur|La coquille revient, rose et blanche.",
            "maman|Le carré touche le seuil, tu vois ?",
            "enfant-m|Vite, on le suit !",
            "narrateur|Un fil bleu du pull reste sur le tapis.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le lait a laissé une goutte, sur le carrelage.",
        "maman|Quel jeu t'aide, près du carré ?",
        "papa|Les cubes, le livre, ou la dînette ?",
    ],
    2: [
        "narrateur|Le parasol jaune tremble, et l'or recule.",
        "papa|Quel jeu t'aide, près du carré ?",
        "maman|Les cubes, le livre, ou la dînette ?",
    ],
    3: [
        "narrateur|Le fil bleu du pull montre le seuil.",
        "maman|Quel jeu t'aide, près du carré ?",
        "papa|Les cubes, le livre, ou la dînette ?",
    ],
}

T2 = {
    (1, 1): {
        "lab": "les cubes",
        "sons": "bois,cubes,lait",
        "emphasis": "cubes",
        "passage": [
            "narrateur|Les cubes attendent, en bois clair.",
            "narrateur|Ils sentent le sapin, près du bol.",
            "enfant-m|Une allée, pour garder l'or !",
            "narrateur|Raphaël pose le cube rouge et le bleu.",
            "narrateur|Les deux, d'un seul geste.",
            "narrateur|La tour penche vers le carré.",
            "papa|Elle va manger la lumière, tu vois ?",
            "narrateur|Patatras.",
            "narrateur|L'ombre des cubes coupe l'or en lanière.",
            "enfant-m|Mon carré est trop mince !",
            "maman|Un cube, tu regardes, et après ?",
            "narrateur|Raphaël serre un cube, déçu.",
            "narrateur|La goutte de lait brille au bord.",
        ],
    },
    (1, 2): {
        "lab": "le livre",
        "sons": "pages,papier,bol",
        "emphasis": "livre",
        "passage": [
            "narrateur|Le livre a une couverture bleue, comme l'eau.",
            "narrateur|Raphaël l'ouvre sur la table, trop large.",
            "enfant-m|Un bateau !",
            "maman|Tu as bien vu la page, oui.",
            "narrateur|Le livre glisse.",
            "narrateur|Il couvre le carré d'or, sur les carreaux.",
            "enfant-m|L'or est parti sous le papier !",
            "papa|Le bateau du livre cache la mer vraie ?",
            "narrateur|Un signet en forme de barque s'envole.",
            "narrateur|Il file vers la casserole.",
            "enfant-m|Attends, petit bateau !",
            "narrateur|Raphaël lâche le livre, les lèvres pincées.",
            "narrateur|Sous une page, un filet d'or reste.",
        ],
    },
    (1, 3): {
        "lab": "la dînette",
        "sons": "tasse,porcelaine,lait",
        "emphasis": "tasse",
        "passage": [
            "narrateur|La dînette est sur une serviette.",
            "narrateur|La petite tasse est blanche, légère.",
            "enfant-m|Du thé, pour la coquille !",
            "narrateur|Raphaël verse en marchant vers le carré.",
            "maman|La théière penche trop, non ?",
            "narrateur|Une goutte tombe sur le carrelage.",
            "narrateur|Le bois mouillé devient sombre.",
            "enfant-m|Le carré s'est éteint !",
            "papa|C'est l'eau qui a volé la lumière.",
            "narrateur|Raphaël pose la théière de travers.",
            "narrateur|La coquille, collée à la tasse, fait clic.",
            "enfant-m|Je voulais la servir, et courir.",
            "narrateur|Ses mains tremblent un peu.",
        ],
    },
    (2, 1): {
        "lab": "les cubes",
        "sons": "bois,vent,parasol",
        "emphasis": "cubes",
        "passage": [
            "narrateur|Les cubes attendent sur la pierre du banc.",
            "narrateur|Ils sentent le sapin et le thym.",
            "enfant-m|Une allée jusqu'au phare !",
            "narrateur|Raphaël pose deux cubes contre le vent.",
            "narrateur|Le vent les pousse vers le parasol.",
            "papa|Ils roulent, tu les vois ?",
            "narrateur|Un cube tape le pied du parasol.",
            "narrateur|L'ombre jaune s'étale sur l'or.",
            "enfant-m|Le parasol a tout mangé !",
            "maman|Un cube, tu t'arrêtes, tu regardes ?",
            "narrateur|Raphaël ramasse le cube rouge, trop vite.",
            "narrateur|Le sable colle au bois.",
            "narrateur|Le phare du jardin cligne, patient.",
        ],
    },
    (2, 2): {
        "lab": "le livre",
        "sons": "pages,vent,figuier",
        "emphasis": "pages",
        "passage": [
            "narrateur|Raphaël ouvre le livre sur le banc.",
            "narrateur|La couverture bleue claque au vent.",
            "enfant-m|Le bateau va vers les vagues !",
            "papa|Les pages veulent voler, elles.",
            "narrateur|Le vent tourne trois pages d'un coup.",
            "narrateur|Le livre se referme sur le carré.",
            "enfant-m|Il a pris l'or !",
            "maman|Le banc n'a plus de soleil, tu vois ?",
            "narrateur|Une feuille de figuier tombe sur la couverture.",
            "narrateur|Raphaël tire le livre, trop fort.",
            "narrateur|Le banc reste gris, sans lumière.",
            "enfant-m|Je voulais lire, et courir à la mer.",
            "narrateur|Il pose sa joue sur le papier tiède.",
        ],
    },
    (2, 3): {
        "lab": "la dînette",
        "sons": "tasse,parasol,pierre",
        "emphasis": "théière",
        "passage": [
            "narrateur|La dînette s'installe sur la pierre chaude.",
            "narrateur|La petite tasse sonne, légère.",
            "enfant-m|Un goûter sous le parasol !",
            "narrateur|Raphaël verse en tenant le parasol.",
            "maman|Deux métiers, une seule main ?",
            "narrateur|La théière goutte sur la pierre.",
            "narrateur|La tache sombre cache le carré d'or.",
            "enfant-m|Il a disparu dans la pierre !",
            "papa|L'eau a fait un faux plancher, tu vois ?",
            "narrateur|Le parasol claque, et l'ombre saute.",
            "narrateur|Raphaël lâche le manche, déçu.",
            "enfant-m|Je voulais servir, et garder l'or.",
            "narrateur|La coquille, au fond de la tasse, fait clic.",
        ],
    },
    (3, 1): {
        "lab": "les cubes",
        "sons": "bois,tapis,drap",
        "emphasis": "tapis",
        "passage": [
            "narrateur|Les cubes attendent sur le tapis rêche.",
            "narrateur|Ils sentent le sapin, près du pull.",
            "enfant-m|Une allée jusqu'à la porte !",
            "narrateur|Raphaël enfonce deux cubes dans le tapis.",
            "narrateur|Le tissu les avale à moitié.",
            "papa|Le tapis mange tes murs, non ?",
            "narrateur|L'allée penche, puis s'écroule.",
            "narrateur|Un cube roule sur le carré d'or.",
            "enfant-m|Il a bouché la lumière !",
            "maman|Un cube, tu le poses, tu regardes ?",
            "narrateur|Raphaël retire le cube, trop vite.",
            "narrateur|Le tapis se plisse, et l'or fuit.",
            "narrateur|Un fil bleu du pull s'accroche au bois.",
        ],
    },
    (3, 2): {
        "lab": "le livre",
        "sons": "pages,drap,chaise",
        "emphasis": "livre",
        "passage": [
            "narrateur|Raphaël ouvre le livre sur le lit.",
            "narrateur|Le drap chaud tient les pages.",
            "enfant-m|Le bateau dort près de moi !",
            "maman|La page, ou le carré, lequel d'abord ?",
            "narrateur|Il tire le livre vers le seuil.",
            "narrateur|La couverture bleue recouvre l'or du tapis.",
            "enfant-m|Je ne vois plus le carré !",
            "papa|Le bateau de papier a fait la nuit.",
            "narrateur|Raphaël soulève le livre d'un coup.",
            "narrateur|Le tapis reste sombre, un instant.",
            "enfant-m|L'or a peur, je crois.",
            "narrateur|Il pose le livre sur la chaise, trop fort.",
            "narrateur|Un coin de page se plie.",
        ],
    },
    (3, 3): {
        "lab": "la dînette",
        "sons": "tasse,tissu,tapis",
        "emphasis": "goutte",
        "passage": [
            "narrateur|La dînette s'assoit sur le tapis rêche.",
            "narrateur|La petite tasse penche, blanche.",
            "enfant-m|Du thé, dans le carré !",
            "narrateur|Raphaël verse, la manche du pull trop longue.",
            "papa|La manche va au thé, tu vois ?",
            "narrateur|Une goutte tombe sur le tapis.",
            "narrateur|Le rêche devient sombre, sans or.",
            "enfant-m|Le carré a bu l'eau !",
            "maman|C'est la tache qui a volé le soleil.",
            "narrateur|Raphaël essuie trop vite, avec la manche.",
            "narrateur|La tache s'étale.",
            "enfant-m|Pire !",
            "narrateur|La coquille, au bord de la tasse, fait clic.",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Les cubes ont fait de l'ombre sur l'or.",
        "papa|On y va à quelle heure ?",
        "maman|Le matin, après la sieste, ou le soir ?",
    ],
    2: [
        "narrateur|Le livre a couvert un bout de lumière.",
        "maman|On y va à quelle heure ?",
        "papa|Le matin, après la sieste, ou le soir ?",
    ],
    3: [
        "narrateur|La goutte a fait un faux plancher sombre.",
        "papa|On y va à quelle heure ?",
        "maman|Le matin, après la sieste, ou le soir ?",
    ],
}

T3_SONS = {1: "soleil,mer,coquille", 2: "volet,ombre,coquille", 3: "lampe,mer,parasol"}
T3_EMPH = {1: "coquille", 2: "ombre", 3: "parasol"}
END_SONS = {1: "bol,mer,coquille", 2: "parasol,mer,phare", 3: "tapis,mer,volet"}


def t3_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "soulagement_joyeux", 3: "tendresse"}
    tempos = {1: "vif_puis_posé", 2: "prudent", 3: "ample"}
    return (
        f"arc=résolution; intention=faire_vivre_la_réussite; emotion={emos[c]}; "
        f"intensite=2; destinataire=enfant; sous_texte=un_geste_puis_le_clic; "
        f"tempo={tempos[c]}; sourire=franc; respiration=relâchée; chemin={a}{b}{c}"
    )


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_coquille_a_gardé_l_or; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


T3 = {
    (1, 1, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|Le carré d'or file sur les carreaux.",
        "enfant-m|Un cube, seulement.",
        "narrateur|Raphaël pose le cube rouge au bord.",
        "narrateur|L'or s'arrête contre le bois.",
        "papa|Il a trouvé un mur, ton carré.",
        "narrateur|Raphaël pose la coquille au milieu.",
        "narrateur|Clic.",
        "enfant-m|Elle brille, maman !",
        "maman|Elle a pris le soleil, oui.",
        "narrateur|Un grain de sable colle au cube.",
        "narrateur|Le bol attend, vide, sur la table.",
    ],
    (1, 1, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|Le carré d'or n'est plus qu'un ruban.",
        "enfant-m|J'ouvre un peu, d'abord.",
        "narrateur|Raphaël pousse le volet d'un cran.",
        "narrateur|Le ruban s'élargit sur les carreaux.",
        "maman|La lumière revient, tu vois ?",
        "narrateur|Il pose un cube, puis la coquille.",
        "narrateur|Clic.",
        "papa|Le ruban a un cœur, maintenant.",
        "enfant-m|Elle est dedans.",
        "narrateur|Les cubes sont tièdes, près du bol.",
        "narrateur|Dehors, la mer parle plus bas.",
    ],
    (1, 1, 3): [
        "narrateur|La mer parle orange, derrière la vitre.",
        "narrateur|Le carré d'or devient un rond de lampe.",
        "enfant-m|L'or du jour est parti ?",
        "papa|Regarde le seuil, tout au bout.",
        "narrateur|Un dernier coin d'or tient la porte.",
        "narrateur|Raphaël pose un cube, comme une marche.",
        "narrateur|Puis la coquille, dans le coin.",
        "narrateur|Clic.",
        "maman|Elle a le dernier soleil.",
        "enfant-m|On peut y aller.",
        "narrateur|La tour de cubes garde l'ombre du soir.",
        "narrateur|Le pain a refroidi, près du bol.",
    ],
    (1, 2, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|Le bateau du livre regarde vers la mer.",
        "enfant-m|Une page, puis le carré.",
        "narrateur|Raphaël ferme le livre à côté.",
        "narrateur|Le carré d'or reparaît, net, sur les carreaux.",
        "maman|Le papier ne le cache plus.",
        "narrateur|Il pose la coquille au milieu.",
        "narrateur|Clic.",
        "papa|Le bateau de papier a laissé la place.",
        "enfant-m|Le vrai bateau, c'est elle.",
        "narrateur|Le signet repose sur la table.",
        "narrateur|Une miette brille près de la couverture.",
    ],
    (1, 2, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|Le livre tient le ruban d'or prisonnier.",
        "enfant-m|Je glisse le livre, d'abord.",
        "narrateur|Raphaël pousse la couverture, tout droit.",
        "narrateur|Le ruban s'allonge vers la porte.",
        "papa|Doucement, les pages restent sages.",
        "narrateur|Il pose la coquille sur le ruban.",
        "narrateur|Clic.",
        "maman|Elle a trouvé sa lanière de soleil.",
        "enfant-m|On la porte à la mer.",
        "narrateur|Le livre sent le fruit de la sieste.",
        "narrateur|Le bol a une ombre ronde, à côté.",
    ],
    (1, 2, 3): [
        "narrateur|La mer parle orange, derrière la vitre.",
        "narrateur|Le carré d'or devient un rond de lampe.",
        "enfant-m|Le livre sera la rive, là.",
        "narrateur|Raphaël pose le livre, fermé, au bord.",
        "narrateur|Le rond d'or reste libre, au milieu.",
        "maman|Une rive de papier, une mer de lumière.",
        "narrateur|La coquille s'assoit dans le rond.",
        "narrateur|Clic.",
        "papa|Le bateau de la page peut dormir.",
        "enfant-m|Le nôtre va dehors.",
        "narrateur|La dernière page a un bruit de papier.",
        "narrateur|Le lait a laissé un cercle blanc.",
    ],
    (1, 3, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|La tache sombre a volé un bout d'or.",
        "enfant-m|J'essuie, d'abord.",
        "narrateur|Raphaël pose la serviette sur la goutte.",
        "narrateur|Le carrelage redevient clair.",
        "papa|Le soleil a repris sa place.",
        "narrateur|Il pose la tasse, puis la coquille.",
        "narrateur|Clic.",
        "maman|La tasse garde le bord, elle.",
        "enfant-m|Et elle, le milieu.",
        "narrateur|Une goutte de lait brille près de la tasse.",
        "narrateur|Le bol vrai attend, sage, derrière.",
    ],
    (1, 3, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|La tache et l'ombre font un double piège.",
        "enfant-m|La serviette, puis le volet.",
        "narrateur|Raphaël essuie la pierre sombre.",
        "narrateur|Il pousse le volet d'un cran.",
        "maman|Deux gestes, l'un après l'autre.",
        "narrateur|Le ruban d'or revient, mince.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "papa|Elle a choisi le filet de lumière.",
        "enfant-m|On y va, maman.",
        "narrateur|La nappe de dînette a un pli de vent.",
    ],
    (1, 3, 3): [
        "narrateur|La mer parle orange, derrière la vitre.",
        "narrateur|Le rond de lampe tremble sur la tasse.",
        "enfant-m|La tasse attrape l'or, d'abord.",
        "narrateur|Raphaël pose la tasse dans le rond.",
        "narrateur|Un cercle orange danse au fond.",
        "papa|Elle a pris le soir, ta tasse.",
        "narrateur|La coquille s'assoit à côté.",
        "narrateur|Clic.",
        "maman|Deux invitées, une lumière.",
        "enfant-m|On les emmène ?",
        "papa|La coquille vient, la tasse reste.",
        "narrateur|Les assiettes jouets rentrent sur l'étagère.",
    ],
    (2, 1, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|Le carré d'or chauffe la pierre du banc.",
        "enfant-m|Un cube contre le vent, d'abord.",
        "narrateur|Raphaël pose le cube rouge au pied du parasol.",
        "narrateur|Le parasol arrête de tourner.",
        "papa|L'ombre reste sage, maintenant.",
        "narrateur|L'or revient sur la pierre.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "maman|Le phare du jardin cligne, content.",
        "enfant-m|Elle brille comme lui !",
        "narrateur|Un grain de sable colle au cube rouge.",
    ],
    (2, 1, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|Le parasol mange le ruban qui reste.",
        "enfant-m|Je pousse le parasol, d'abord.",
        "narrateur|Raphaël fait glisser le pied jaune.",
        "narrateur|Le ruban s'allonge sur le banc.",
        "maman|Un geste, et le soleil respire.",
        "narrateur|Il pose un cube, puis la coquille.",
        "narrateur|Clic.",
        "papa|Le phare a retrouvé son petit soleil.",
        "enfant-m|On va à la mer, après.",
        "narrateur|Les cubes du banc ont du soleil dessus.",
        "narrateur|Une fourmi change de chemin, entre eux.",
    ],
    (2, 1, 3): [
        "narrateur|La mer parle orange, derrière le phare.",
        "narrateur|Le rond de lampe tombe sur la pierre.",
        "enfant-m|Les cubes font un escalier, vers lui.",
        "narrateur|Raphaël pose un cube, puis un autre.",
        "narrateur|L'escalier s'arrête au rond orange.",
        "papa|Tu as regardé entre chaque pas.",
        "narrateur|La coquille gravit la dernière marche.",
        "narrateur|Clic.",
        "maman|Elle a le soir, sur le banc.",
        "enfant-m|Le parasol peut dormir.",
        "narrateur|Le panier rentre, les cubes cliquettent.",
        "narrateur|Le phare du jardin garde une lueur.",
    ],
    (2, 2, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|Le livre claque, puis se tient.",
        "enfant-m|Je le ferme, d'abord.",
        "narrateur|Raphaël pose une pierre plate sur la couverture.",
        "narrateur|Les pages restent sages.",
        "maman|Le banc a son soleil, à nouveau.",
        "narrateur|Il pose la coquille au milieu de l'or.",
        "narrateur|Clic.",
        "papa|Le bateau de papier cède la mer vraie.",
        "enfant-m|On y va, avec elle.",
        "narrateur|Une feuille de figuier ombre le livre.",
        "narrateur|Le sel pique l'air, tout près.",
    ],
    (2, 2, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|Le livre tient le ruban sous sa couverture.",
        "enfant-m|Je le glisse vers moi, d'abord.",
        "narrateur|Raphaël tire le livre, tout droit, sans voler.",
        "narrateur|Le ruban d'or reparaît sur le banc.",
        "papa|Les pages n'ont pas pris le vent.",
        "narrateur|La coquille s'assoit sur le ruban.",
        "narrateur|Clic.",
        "maman|Elle a sa lanière de soleil.",
        "enfant-m|Le figuier peut garder l'ombre.",
        "narrateur|Le livre sent le thym, un peu.",
        "narrateur|L'ombre du figuier s'arrête au bord du banc.",
    ],
    (2, 2, 3): [
        "narrateur|La mer parle orange, derrière le phare.",
        "narrateur|Le rond de lampe tremble sur les pages.",
        "enfant-m|Le livre sera le quai, le soir.",
        "narrateur|Raphaël pose le livre fermé, comme un quai.",
        "narrateur|Le rond orange reste l'eau.",
        "maman|Une rive, une mer, un bateau.",
        "narrateur|La coquille entre dans le rond.",
        "narrateur|Clic.",
        "papa|Le vrai voyage commence dehors.",
        "enfant-m|J'emporte le livre ?",
        "maman|Si tu veux, la coquille surtout.",
        "narrateur|Le livre a du sable au coin.",
    ],
    (2, 3, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|La tache sombre cache l'or de la pierre.",
        "enfant-m|J'essuie, d'abord.",
        "narrateur|Raphaël pose la serviette sur la goutte.",
        "narrateur|La pierre redevient claire, chaude.",
        "papa|Le carré était dessous, tu vois ?",
        "narrateur|Il pose la tasse, puis la coquille.",
        "narrateur|Clic.",
        "maman|Deux places, deux gestes.",
        "enfant-m|Elle brille plus que la tasse.",
        "narrateur|Une fourmi contourne la tasse, sur la pierre.",
        "narrateur|Le parasol jaune fait un peu d'ombre, plus loin.",
    ],
    (2, 3, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|La tache et le parasol volent le ruban.",
        "enfant-m|La serviette, puis le parasol.",
        "narrateur|Raphaël essuie la pierre.",
        "narrateur|Il pousse le pied du parasol.",
        "maman|L'un, puis l'autre.",
        "narrateur|Le ruban d'or revient, mince, sur le banc.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "papa|Elle a choisi le filet qui restait.",
        "enfant-m|On va à l'eau.",
        "narrateur|La nappe a un pli de vent, on la secoue.",
    ],
    (2, 3, 3): [
        "narrateur|La mer parle orange, derrière le phare.",
        "narrateur|Le rond de lampe danse au fond de la tasse.",
        "enfant-m|La tasse prend le soir, d'abord.",
        "narrateur|Raphaël pose la tasse dans le rond.",
        "narrateur|Un cercle orange y tremble.",
        "papa|Elle a bu la lumière, ta tasse.",
        "narrateur|La coquille s'assoit contre elle.",
        "narrateur|Clic.",
        "maman|Deux petites choses, une lumière.",
        "enfant-m|La coquille vient à la mer.",
        "narrateur|Le panier rentre, et la dînette cliquette.",
        "narrateur|Le phare du jardin cligne une dernière fois.",
    ],
    (3, 1, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|Le carré d'or tient sur le tapis rêche.",
        "enfant-m|Un cube, posé, pas enfoncé.",
        "narrateur|Raphaël pose le cube bleu au bord du tapis.",
        "narrateur|Le tissu ne l'avale plus.",
        "papa|Il fait un seuil, ton cube.",
        "narrateur|La coquille entre dans l'or.",
        "narrateur|Clic.",
        "maman|Elle a le tapis, et le soleil.",
        "enfant-m|Le pull est mis, elle aussi.",
        "narrateur|Un cube bleu touche le tapis, puis s'arrête.",
        "narrateur|Un fil bleu reste coincé sous le bois.",
    ],
    (3, 1, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|Le tapis plissé cache le ruban d'or.",
        "enfant-m|Je lisse le tapis, d'abord.",
        "narrateur|Raphaël passe la main, une fois.",
        "narrateur|Le ruban reparaît, mince, vers la porte.",
        "maman|Le rêche a rendu la lumière.",
        "narrateur|Il pose un cube, puis la coquille.",
        "narrateur|Clic.",
        "papa|Elle a sa lanière, jusqu'au seuil.",
        "enfant-m|On sort, après.",
        "narrateur|Les cubes sont chauds, sur le tapis rêche.",
        "narrateur|Le drap retombe, sans bruit.",
    ],
    (3, 1, 3): [
        "narrateur|La mer parle orange, derrière les volets.",
        "narrateur|Le rond de lampe tombe près du lit.",
        "enfant-m|La boîte, d'abord.",
        "narrateur|Raphaël range un cube, puis l'autre.",
        "narrateur|La boîte se ferme, près du lit.",
        "papa|Le tapis est libre, maintenant.",
        "narrateur|Le rond orange attend au seuil.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "maman|Elle a le dernier or de la chambre.",
        "enfant-m|Le pull me tient chaud, dehors.",
        "narrateur|La boîte de cubes garde l'ombre du soir.",
    ],
    (3, 2, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|Le livre a fait la nuit sur le tapis.",
        "enfant-m|Je le pose sur la chaise, d'abord.",
        "narrateur|Raphaël pose le livre, fermé, près du pull.",
        "narrateur|Le carré d'or revient, net, sur le rêche.",
        "maman|La page a laissé la place.",
        "narrateur|La coquille s'assoit au milieu.",
        "narrateur|Clic.",
        "papa|Le bateau de papier reste au port.",
        "enfant-m|Le nôtre va à la mer.",
        "narrateur|Le pull bleu a gardé une page, un moment.",
        "narrateur|Le sel entre par la fenêtre.",
    ],
    (3, 2, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|Le livre tient le ruban sous sa couverture.",
        "enfant-m|Je le glisse vers la chaise.",
        "narrateur|Raphaël pousse le livre, tout droit.",
        "narrateur|Le ruban d'or s'allonge sur le tapis.",
        "papa|Les pages n'ont pas volé, cette fois.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "maman|Elle a sa lanière, jusqu'à la porte.",
        "enfant-m|J'ai le pull, et elle.",
        "narrateur|Le livre sent le drap, un peu.",
        "narrateur|L'ombre du volet s'arrête au bord du tapis.",
    ],
    (3, 2, 3): [
        "narrateur|La mer parle orange, derrière les volets.",
        "narrateur|Le rond de lampe tremble sur la chaise.",
        "enfant-m|Le livre, sur la chaise, d'abord.",
        "narrateur|Raphaël pose le livre près du pull.",
        "narrateur|Le rond orange reste au seuil, libre.",
        "maman|Deux places, deux lumières.",
        "narrateur|La coquille entre dans le rond.",
        "narrateur|Clic.",
        "papa|Elle a le soir de la porte.",
        "enfant-m|On ouvre, maintenant.",
        "narrateur|Raphaël laisse le livre sur la chaise.",
        "narrateur|Un coin de page reste plié, comme un secret.",
    ],
    (3, 3, 1): [
        "narrateur|La lumière est blanche, comme le sel.",
        "narrateur|La tache sombre a bu l'or du tapis.",
        "enfant-m|Un vrai linge, d'abord.",
        "narrateur|Raphaël prend le linge du drap, pas la manche.",
        "narrateur|Il pose le linge sur la goutte.",
        "papa|La tache recule, tu vois ?",
        "narrateur|Le carré d'or revient, net.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "maman|La manche est restée sèche, cette fois.",
        "enfant-m|La tasse à sa place, elle au milieu.",
        "narrateur|La petite tasse a un reflet de coquille.",
    ],
    (3, 3, 2): [
        "narrateur|Les volets ont laissé une bande d'ombre.",
        "narrateur|La tache et l'ombre font un double piège.",
        "enfant-m|Le linge, puis le volet.",
        "narrateur|Raphaël essuie le tapis.",
        "narrateur|Il pousse le volet d'un cran.",
        "maman|Deux gestes, l'or revient.",
        "narrateur|Le ruban s'allonge vers la porte.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "papa|Elle a choisi le filet du seuil.",
        "enfant-m|Une chaussette a glissé, près de la tasse.",
        "narrateur|Raphaël la range, puis prend la coquille.",
    ],
    (3, 3, 3): [
        "narrateur|La mer parle orange, derrière les volets.",
        "narrateur|Le rond de lampe danse dans la petite tasse.",
        "enfant-m|La dînette rentre, d'abord.",
        "narrateur|Raphaël pose la tasse dans le panier.",
        "narrateur|Le tapis se libère.",
        "papa|Le seuil a gardé le rond orange.",
        "narrateur|La coquille s'y pose.",
        "narrateur|Clic.",
        "maman|Elle a le dernier or de la maison.",
        "enfant-m|On va à la mer, avec elle.",
        "narrateur|La dînette rentre.",
        "narrateur|La coquille, elle, reste au rebord un instant.",
    ],
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Près de la porte, le carré glisse dehors.",
        "enfant-m|La mer, maman !",
        "maman|Oui, on y va, maintenant.",
        "narrateur|Raphaël tient la coquille, chaude de soleil.",
        "papa|Elle a un grain de sable, sur le bord.",
        "enfant-m|C'est le grain du plancher.",
        "narrateur|Le cube rouge garde une miette, comme ce grain.",
    ],
    (1, 1, 2): [
        "narrateur|Sous ses pieds, le plancher est chaud.",
        "enfant-m|La mer, après la sieste !",
        "papa|Le parasol nous attend, dehors.",
        "narrateur|Raphaël pose la coquille contre sa joue.",
        "maman|Elle sent le lait, un peu.",
        "enfant-m|Et le bois des cubes.",
        "narrateur|Les cubes tièdes restent près du bol, et la mer appelle.",
    ],
    (1, 1, 3): [
        "narrateur|Dans le vent, une mouette passe, très haut.",
        "enfant-m|La mer est orange, papa.",
        "papa|Comme le rond de ta lampe.",
        "narrateur|Raphaël serre la coquille, légère.",
        "maman|Elle a gardé un peu de soir.",
        "enfant-m|Le phare du jardin cligne aussi.",
        "narrateur|La tour de cubes garde l'ombre du soir, près du pain.",
    ],
    (1, 2, 1): [
        "narrateur|Enfin le sable mouillé, tout proche.",
        "enfant-m|Le bateau du livre, et la mer vraie !",
        "maman|Tu as fermé la page, puis ouvert la porte.",
        "narrateur|La coquille clic contre la coquille de la plage.",
        "papa|Deux coquilles, un même sel.",
        "enfant-m|La mienne a l'or dedans.",
        "narrateur|La tartine a une marque de dent, et le livre sent le sel.",
    ],
    (1, 2, 2): [
        "narrateur|Voilà l'eau, tout près de la maison.",
        "enfant-m|Le parasol, maman !",
        "papa|Il fait un rond d'ombre, sur le sable.",
        "narrateur|Raphaël glisse la coquille dans ce rond-là.",
        "maman|Un carré d'or, puis un rond d'ombre.",
        "enfant-m|Elle a les deux.",
        "narrateur|Le livre sent le fruit de la sieste, sous le parasol.",
    ],
    (1, 2, 3): [
        "narrateur|Raphaël a les pieds dans la lumière du soir.",
        "enfant-m|On marche jusqu'à l'eau ?",
        "maman|Oui, le livre reste au quai de la table.",
        "narrateur|La coquille chauffe, orange, dans sa main.",
        "papa|Le signet n'a pas volé, cette fois.",
        "enfant-m|Il dort sur le bateau de papier.",
        "narrateur|La dernière page fait un bruit de papier, orange.",
    ],
    (1, 3, 1): [
        "narrateur|Le carré d'or tient sous les orteils, une seconde.",
        "enfant-m|La tasse est restée, elle vient pas.",
        "papa|La coquille vient, la mer l'attend.",
        "narrateur|Raphaël descend la dune, la coquille au creux.",
        "maman|Elle a une goutte de lait, au bord.",
        "enfant-m|C'est sa trace du bol.",
        "narrateur|Une goutte de lait brille près de la petite tasse, à la maison.",
    ],
    (1, 3, 2): [
        "narrateur|Contre le seuil, le sel arrive, tiède.",
        "enfant-m|On secoue la nappe, dehors !",
        "maman|Un pli de vent, et on part.",
        "narrateur|La coquille clic dans la main de Raphaël.",
        "papa|Le parasol nous suit, jaune.",
        "enfant-m|L'or est à elle, maintenant.",
        "narrateur|La nappe de dînette a un pli de vent, dehors.",
    ],
    (1, 3, 3): [
        "narrateur|Au bout du chemin, la mer dit chhh.",
        "enfant-m|Les assiettes sont rentrées, papa.",
        "papa|Et nous, on sort.",
        "narrateur|Raphaël pose la coquille sur le sable mouillé.",
        "maman|Elle retrouve l'eau, un instant.",
        "enfant-m|Elle a l'or, et le sel.",
        "narrateur|Les assiettes jouets montent sur l'étagère, et la casserole se tait.",
    ],
    (2, 1, 1): [
        "narrateur|Près de la porte, le carré glisse vers le phare.",
        "enfant-m|Le phare du jardin, d'abord, puis la mer !",
        "maman|Tu poses un pas, puis l'autre.",
        "narrateur|Raphaël passe devant le phare, la coquille haute.",
        "papa|Elle cligne avec lui, tu vois ?",
        "enfant-m|Deux petites lumières.",
        "narrateur|Les cubes du banc ont du soleil, et le phare cligne.",
    ],
    (2, 1, 2): [
        "narrateur|Sous ses pieds, la pierre du banc est chaude.",
        "enfant-m|La fourmi a changé de chemin.",
        "papa|Nous aussi, vers l'eau.",
        "narrateur|Raphaël tient la coquille, un peu de sable dessus.",
        "maman|Le parasol nous fait un toit, maintenant.",
        "enfant-m|L'or est à elle, pas à l'ombre.",
        "narrateur|Une fourmi change de chemin, entre les cubes oubliés.",
    ],
    (2, 1, 3): [
        "narrateur|Dans le vent, une mouette passe, très haut.",
        "enfant-m|Le panier rentre, on sort.",
        "maman|Le soir sent le thym, et le sel.",
        "narrateur|Raphaël descend vers l'eau, la coquille orange.",
        "papa|Le phare du jardin garde la maison.",
        "enfant-m|Elle, elle vient.",
        "narrateur|Le panier rentre, les cubes cliquettent contre le bois.",
    ],
    (2, 2, 1): [
        "narrateur|Enfin le sable mouillé, tout proche.",
        "enfant-m|Le livre sous le bras, la coquille au creux !",
        "papa|Deux trésors, deux mains.",
        "narrateur|La mer dit chhh, contre les pieds.",
        "maman|Le bateau de papier a cédé la place.",
        "enfant-m|Le vrai, c'est l'eau.",
        "narrateur|Raphaël tient le livre sous le bras, vers les vagues.",
    ],
    (2, 2, 2): [
        "narrateur|Voilà l'eau, tout près de la maison.",
        "enfant-m|Le figuier garde le banc.",
        "maman|Et nous, on prend le sel.",
        "narrateur|Raphaël glisse la coquille dans une vague petite.",
        "papa|Elle revient, brillante.",
        "enfant-m|Elle a l'or, et l'eau.",
        "narrateur|L'ombre du figuier mange le banc, pas le livre.",
    ],
    (2, 2, 3): [
        "narrateur|Raphaël a les pieds dans la lumière du soir.",
        "enfant-m|Le livre a du sable au coin.",
        "papa|Un secret de plage, dans le papier.",
        "narrateur|La coquille chauffe, orange, contre sa paume.",
        "maman|Le phare du jardin cligne, loin.",
        "enfant-m|On dirait qu'il dit bonsoir.",
        "narrateur|Le livre a du sable au coin, comme un secret.",
    ],
    (2, 3, 1): [
        "narrateur|Le carré d'or tient sous les orteils, sur la pierre.",
        "enfant-m|La fourmi a contourné la tasse !",
        "maman|Elle a choisi son chemin, elle aussi.",
        "narrateur|Raphaël descend la dune, la coquille au creux.",
        "papa|Le parasol jaune nous suit.",
        "enfant-m|L'or est à elle, maintenant.",
        "narrateur|Une fourmi contourne la tasse, sur la pierre chaude.",
    ],
    (2, 3, 2): [
        "narrateur|Contre le seuil, le sel arrive, tiède.",
        "enfant-m|On a secoué la nappe !",
        "papa|Un pli de vent, et c'est parti.",
        "narrateur|La coquille clic dans la main de Raphaël.",
        "maman|Le phare du jardin pointe vers l'eau.",
        "enfant-m|On le suit.",
        "narrateur|La nappe a un pli de vent, on la secoue une fois.",
    ],
    (2, 3, 3): [
        "narrateur|Au bout du chemin, la mer dit chhh.",
        "enfant-m|La dînette cliquette, dans le panier.",
        "maman|Elle rentre, et nous on avance.",
        "narrateur|Raphaël pose la coquille sur le sable orange.",
        "papa|Le phare cligne une dernière fois.",
        "enfant-m|Elle a le soir, et le sel.",
        "narrateur|Le panier rentre, et la dînette cliquette derrière la dune.",
    ],
    (3, 1, 1): [
        "narrateur|Près de la porte, le carré glisse dehors.",
        "enfant-m|Le pull est mis, la coquille aussi !",
        "papa|Deux gestes, deux réussites.",
        "narrateur|Raphaël passe le seuil, le tapis derrière lui.",
        "maman|Un fil bleu s'accroche au cube, tu vois ?",
        "enfant-m|C'est la trace du pull.",
        "narrateur|Un cube bleu touche le tapis, puis s'écarte vers le jour.",
    ],
    (3, 1, 2): [
        "narrateur|Sous ses pieds, le plancher est chaud.",
        "enfant-m|Les cubes sont chauds, eux aussi.",
        "maman|Le drap retombe, et nous on sort.",
        "narrateur|Raphaël serre la coquille, un fil bleu au bord.",
        "papa|Le parasol nous attend, jaune.",
        "enfant-m|L'or est à elle.",
        "narrateur|Les cubes sont chauds, sur le tapis rêche, et le drap se tait.",
    ],
    (3, 1, 3): [
        "narrateur|Dans le vent, une mouette passe, très haut.",
        "enfant-m|La boîte est fermée, papa.",
        "papa|Le lit peut dormir, pas la mer.",
        "narrateur|Raphaël descend, le pull chaud, la coquille orange.",
        "maman|Elle a le dernier or de la chambre.",
        "enfant-m|Je le lui garde.",
        "narrateur|La boîte de cubes se ferme, près du lit, et le soir entre.",
    ],
    (3, 2, 1): [
        "narrateur|Enfin le sable mouillé, tout proche.",
        "enfant-m|Le pull a gardé une page !",
        "maman|Une page de chaleur, contre toi.",
        "narrateur|La coquille clic, rose, contre le sel.",
        "papa|Le bateau de papier reste au port, sur la chaise.",
        "enfant-m|Le nôtre, c'est l'eau.",
        "narrateur|Le pull bleu a gardé une page, un moment, puis le vent.",
    ],
    (3, 2, 2): [
        "narrateur|Voilà l'eau, tout près de la maison.",
        "enfant-m|Le livre sent le drap.",
        "papa|Et toi, tu sens le sel.",
        "narrateur|Raphaël glisse la coquille dans une vague.",
        "maman|Elle revient, brillante, avec un grain.",
        "enfant-m|Le grain du plancher, maman.",
        "narrateur|Le livre sent le drap, un peu, sur la chaise vide.",
    ],
    (3, 2, 3): [
        "narrateur|Raphaël a les pieds dans la lumière du soir.",
        "enfant-m|Le livre reste sur la chaise.",
        "maman|Le coin plié garde ton secret.",
        "narrateur|La coquille chauffe, orange, dans sa main.",
        "papa|On ouvre, et la dune commence.",
        "enfant-m|Elle a l'or du seuil.",
        "narrateur|Raphaël pose le souvenir du livre sur la chaise, près du pull.",
    ],
    (3, 3, 1): [
        "narrateur|Le carré d'or tient sous les orteils, une seconde.",
        "enfant-m|La tasse a un reflet, maman !",
        "maman|Un reflet de coquille, oui.",
        "narrateur|Raphaël descend la dune, la vraie coquille au creux.",
        "papa|La manche est sèche, cette fois.",
        "enfant-m|J'ai pris le linge, pas le pull.",
        "narrateur|La petite tasse a un reflet de coquille, et le tapis sèche.",
    ],
    (3, 3, 2): [
        "narrateur|Contre le seuil, le sel arrive, tiède.",
        "enfant-m|La chaussette est rangée !",
        "papa|Un geste, puis la porte.",
        "narrateur|La coquille clic dans la main de Raphaël.",
        "maman|Le parasol jaune s'ouvre, dehors.",
        "enfant-m|L'or est à elle, sous le tissu.",
        "narrateur|Une chaussette a retrouvé sa paire, près de la dînette rentrée.",
    ],
    (3, 3, 3): [
        "narrateur|Au bout du chemin, la mer dit chhh.",
        "enfant-m|La dînette est rentrée, la coquille vient.",
        "maman|Deux maisons : l'étagère, et ta main.",
        "narrateur|Raphaël pose la coquille sur le sable orange.",
        "papa|Elle a le dernier or, et le sel.",
        "enfant-m|Demain, le carré reviendra.",
        "narrateur|La dînette rentre, et la coquille reste au rebord du monde.",
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
        by_src["CHK_T0000_P0000"], OPENING, "opening", "mer,volet,coquille"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
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
            {"emphasis": "chose", "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": "coquille"}
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
                        "option_1_label": "le matin",
                        "option_2_label": "après la sieste",
                        "option_3_label": "le soir",
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
                    {"emphasis": T3_EMPH[c], "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = (
        "Raphaël, dans la maison sur la dune, veut poser sa coquille striée "
        "dans le carré d'or du plancher avant qu'il ne glisse vers la mer. "
        "Il prend coquille, pull et chaussure ensemble : clic, toc, l'or fuit. "
        "Cuisine, jardin (phare, parasol) ou chambre changent le premier revers. "
        "Cubes, livre ou dînette amènent une seconde ruse plus rusée "
        "(ombre, page, tache). Matin, sieste ou soir changent le climax. "
        "Un geste, puis le clic. Vingt-sept fins : la coquille garde une trace, "
        "le carré du début se paie sur le sable."
    )
    story["title"] = TITLE
    story["characters"] = "Raphaël, papa, maman"
    story["setting"] = "petite maison au bord de la mer, carré de soleil"
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

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Public :** N3 (3–6 ans), audio familial\n"
        "- **Leçon :** AUT.ROU.001 — une chose puis la suivante, vécue "
        "(la coquille n'attrape l'or que lorsque Raphaël pose un seul geste)\n"
        "- **Personnages :** Raphaël, papa, maman\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "## Vécu\n\n"
        "Maison sur la dune, grain de sable, carré d'or, coquille striée rose "
        "(clic), phare du jardin, parasol jaune. "
        "Désir : poser la coquille dans le carré avant qu'il ne glisse vers la mer. "
        "Première idée : coquille + pull + chaussure. Ça file, toc, l'or recule. "
        "Chaque branche est une autre histoire :\n\n"
        "- T1 lieu (équipement gardé) : cuisine (bol et lait qui coupent l'or) / "
        "jardin (une chaussure, ombre du parasol) / chambre (pull et coquille dans le drap)\n"
        "- T2 seconde ruse : cubes (ombre de tour) / livre (page qui recouvre) / "
        "dînette (goutte qui éteint l'or)\n"
        "- T3 climax : matin (or net, un cube-mur) / sieste (ruban, volet ou parasol) / "
        "soir (rond de lampe au seuil)\n\n"
        "Q = une chose. Merci vécu quand les mains se libèrent. "
        "Fin : la coquille porte une trace, le grain du début se paie, sans morale.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Héros Raphaël (D16). Décor xlsx : maison de mer, carré de soleil.\n"
        "- Inventivité example3 : objet nommé (coquille striée, clic), mission, "
        "coins (maison sur la dune, phare du jardin, parasol). Pas les refrains.\n"
        "- Obstacle allongé (audit P1) : premier revers + seconde ruse plus rusée "
        "(ombre, page, tache), pas une résolution automatique.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Pas « on va ranger » / « une étape après l'autre » / leçon dite. "
        "La routine se voit.\n"
        "- T1/T2/T3 changent obstacle et climax, pas seulement la lumière.\n"
        "- 1er choix = lieux, n'enlève pas l'équipement (coquille, pull, chaussures restent).\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration), `style_energy`, "
        "pauses, pitch, volume. `slow` = choix, indice, fin.\n"
        f"- 27 fins, 27 dernières images. Chemins {min(counts)}–{max(counts)} mots "
        f"(moy. {sum(counts)//len(counts)}). `check()` N3≤16. Pas apply.\n"
        "- Relu : ouverture + 3 L1 + 9 L2 + 27 L3/fins.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
