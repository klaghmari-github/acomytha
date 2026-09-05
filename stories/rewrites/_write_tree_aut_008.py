#!/usr/bin/env python3
"""TREE-AUT-008 — Le seau jaune d'Aniss (F-NAR-019, N2, AUT.AFF.003, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-008"
N2 = LIMITS["N2"]
TITLE = "Le seau jaune d'Aniss"
CHILD = "enfant-m"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "marque fine",
    "ombre-flèche",
    "ombre en forme de flèche",
    "étoile brune",
    "fil pâle",
    "croissant",
    "virgule",
    "bouton de nacre",
    "nœud de raphia",
    "pois ivoire",
    "grain savon",
    "grain vanille",
    "pastille colle",
    "capuchon",
    "grain doré",
    "brin safran",
    "anneau",
    "clou tête",
    "grain d'ambre",
    "goutte de cire",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille",
    "vis verte",
    "cristal de sucre",
    "laitue",
    "escargot",
    "grain de mica",
    "grain de cannelle",
    "grain d'ocre",
    "grain de feutre",
    "grain de sésame",
    "grain de suie",
    "grain de paprika",
    "hugo",
    "nino",
    "raphaël",
    "raphael",
    "nina",
    "amir",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de limon",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le_seau_résiste_l_anse_pince; "
            "tempo=naturel; volume=medium; sourire=léger; respiration=ample; "
            "pause=goutte_au_bord"
        ),
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note=(
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton_choix_change_la_manière; "
            "tempo=suspendu; volume=medium; sourire=léger; "
            "respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="seau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=il_a_laissé_une_affaire; "
            "tempo=suspendu; volume=soft; sourire=aucun; "
            "respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="seau",
        note=(
            "arc=confirmation; intention=relancer; emotion=élan; intensite=1; "
            "destinataire=enfant; sous_texte=il_reprend_ce_qui_est_à_lui; "
            "tempo=naturel; volume=medium; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=il_part_trop_vite_avec_le_seau; "
            "tempo=vif; volume=medium; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=découragement_léger; intensite=2; destinataire=enfant; "
            "sous_texte=l_objet_cache_le_grain_de_limon; tempo=resserré; "
            "volume=medium; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de limon",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=le_grain_de_limon_paie_le_début; tempo=naturel; "
            "volume=medium; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de limon",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; sous_texte=le_grain_reste_au_fond; "
            "tempo=posé; volume=soft; sourire=léger; respiration=ample"
        ),
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
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
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    out["sons"] = sons if sons is not None else (src.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitchSsml"]
    out["pitch_xai_tag"] = m["pitchTag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before_ms", 0)
    out["pause_after_ms"] = m["pause"]
    out["pause_sentence_ms"] = m["sentence"]
    out["style_energy"] = m["energy"]
    out["style_contour"] = m["contour"]
    out["noise_scale_piper"] = m["noise"]
    out["kokoro_speed"] = m["speed"]
    out["melo_speed"] = m["speed"]
    out["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    out["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    out["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    out["notes"] = m["note"]
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    out.update(extra.get("fields") or {})
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms", "night_policy", "fields"):
            continue
        out[k] = v
    return out


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=grain_de_limon_au_fond_{a}{b}{c}; "
        f"tempo={tempos[c]}; volume=soft; sourire=léger; respiration=ample; "
        f"chemin={a}{b}{c}"
    )


# Ouverture inventée : Aniss connaît la cour ; un détail paraît neuf.
# Indice unique : un grain de limon au fond du seau jaune.
OPENING = vet(
    [
        "narrateur|Aniss connaît la cour, dalle par dalle.",
        "narrateur|Après la pluie, un détail paraît neuf.",
        "narrateur|L'air sent la pierre mouillée, et le bois.",
        "narrateur|Des feuilles collent aux dalles, plates.",
        "narrateur|Ça sent la terre, sous la gouttière.",
        "narrateur|Près de la porte, le seau jaune attend.",
        "narrateur|Au fond, un grain de limon colle, minuscule.",
        "narrateur|Il ne sait pas à quoi ce grain servira.",
        "narrateur|Un manteau bleu pend, au crochet.",
        "papa|Tu as vu le grain, au fond ?",
        f"{CHILD}|Oui, il est collé, tout petit.",
        "maman|La cour est une grande flaque, Aniss.",
        f"{CHILD}|Je veux le seau, pour les flaques !",
        f"{CHILD}|Vite, que le soleil ne les boive pas !",
        "narrateur|En ce moment, Aniss saisit l'anse.",
        "narrateur|Le plastique est froid, un peu lisse.",
        "narrateur|Il tire trop fort, d'un seul coup.",
        "narrateur|L'anse résiste, et pince ses doigts.",
        f"{CHILD}|Il ne veut pas venir !",
        "narrateur|Le sourire d'Aniss disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|Regarde le seau, pas tes pieds.",
        "maman|Tu l'emportes où, d'abord ?",
        f"{CHILD}|Je le prends, je cours dehors !",
        "narrateur|Une goutte tremble au bord, puis tient.",
        "papa|Merci d'avoir gardé le seau avec toi.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Le seau jaune part avec lui, lourd.",
        "narrateur|La cuisine, le jardin, ou la chambre.",
        "maman|Où vas-tu d'abord, Aniss ?",
    ]
)

T1 = {
    1: dict(
        lab="la cuisine",
        ans="manteau",
        acc="manteau | le manteau | la chaise | sur la chaise | il revient",
        retry="Le manteau est sur la chaise. Aniss reprend quoi ?",
        ok="Oui, le manteau.",
        sons="seau,chaise,carrelage",
        emp="manteau",
        passage=vet(
            [
                "narrateur|Aniss pousse la porte de la cuisine.",
                "narrateur|Le carrelage est froid, luisant.",
                "narrateur|Ça sent le pain, tiède, sous la table.",
                "narrateur|Le seau jaune part avec lui, lourd.",
                "narrateur|Au fond, le grain de limon tient.",
                f"{CHILD}|Je verse la mare des dalles, papa !",
                "narrateur|Il court vers la porte, trop vite.",
                "narrateur|L'anse glisse, l'eau penche.",
                "narrateur|Le manteau reste sur la chaise.",
                "narrateur|Une botte attend, dans le passage.",
                f"{CHILD}|Il pince, je le lâche presque !",
                "papa|Le seau est avec toi.",
                "maman|Et le manteau, près de la chaise ?",
                "narrateur|Aniss s'arrête, les épaules basses.",
                f"{CHILD}|Il est resté, là.",
            ]
        ),
        question=vet(
            [
                "narrateur|Aniss tient le seau, près de la porte.",
                "maman|Il a laissé quoi, sur la chaise ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Aniss pose le seau un instant.",
                "narrateur|Il reprend le manteau, sur la chaise.",
                f"{CHILD}|Il était là, à moi.",
                "papa|Tu l'as repris, tout seul.",
                "maman|Le seau t'attend, au pied.",
                "narrateur|Le grain de limon n'a pas bougé.",
                f"{CHILD}|On continue, avec le seau.",
            ]
        ),
    ),
    2: dict(
        lab="le jardin",
        ans="manteau",
        acc="manteau | le manteau | le banc | sur le banc | il le prend",
        retry="Le manteau est sur le banc. Aniss reprend quoi ?",
        ok="Oui, le manteau.",
        sons="seau,banc,herbe",
        emp="manteau",
        passage=vet(
            [
                "narrateur|Aniss ouvre la porte du jardin.",
                "narrateur|L'air sent l'herbe, mouillée, coupée.",
                "narrateur|Une flaque ronde attend près du banc.",
                "narrateur|Le seau jaune part avec lui.",
                "narrateur|Il penche trop vite, vers l'eau.",
                "narrateur|Le filet manque la flaque, et file.",
                f"{CHILD}|Elle s'en va, ma rivière !",
                "maman|Le manteau boit, sur le banc.",
                "papa|Le tissu est lourd, Aniss.",
                "narrateur|Aniss pose le seau, les joues chaudes.",
                f"{CHILD}|Mon manteau, il est froid.",
                "narrateur|Le grain de limon reste au fond, sage.",
                "narrateur|Une feuille colle au bois du banc.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le banc est mouillé, le tissu aussi.",
                "papa|Aniss reprend quoi, sur le banc ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Aniss essuie le manteau, du plat de la main.",
                f"{CHILD}|Il est froid, un peu lourd.",
                "maman|Il va sécher, dehors, sur toi.",
                "papa|Le seau t'attend, près du pied.",
                "narrateur|Il reprend l'anse, à deux mains.",
                "narrateur|Le grain de limon n'a pas bougé.",
                f"{CHILD}|Toi aussi, tu viens.",
            ]
        ),
    ),
    3: dict(
        lab="la chambre",
        ans="seau",
        acc="seau | le seau | près de la porte | la porte | il le prend",
        retry="Le seau est près de la porte. Il est où ?",
        ok="Oui, le seau.",
        sons="seau,porte,volet",
        emp="seau",
        passage=vet(
            [
                "narrateur|Aniss court vers la chambre.",
                "narrateur|Le seau vient avec lui, contre la hanche.",
                "narrateur|Le volet est mouillé, par endroits.",
                "narrateur|Par la fenêtre, la cour brille.",
                f"{CHILD}|Je la vois, la mare des dalles !",
                "papa|Les flaques sont là, oui.",
                "narrateur|Il pose le seau, près de la porte.",
                "narrateur|Il prend le doudou, sur le lit.",
                "narrateur|Il court, le seau reste.",
                "maman|Aniss.",
                "papa|Le seau est là, tout seul.",
                f"{CHILD}|Oh.",
                "narrateur|Il revient sur ses pas, lent.",
                "narrateur|L'anse est froide, le grain au fond.",
                f"{CHILD}|Je le prends, lui aussi.",
            ]
        ),
        question=vet(
            [
                "narrateur|Aniss a couru vers la porte.",
                "papa|Le seau est resté où ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Aniss reprend le seau, près de la porte.",
                "narrateur|Il prend aussi le manteau, au pied du lit.",
                f"{CHILD}|J'ai tout, maintenant.",
                "maman|Le doudou est contre toi.",
                "papa|On peut aller à la cour.",
                "narrateur|Le grain de limon n'a pas bougé.",
                f"{CHILD}|Oui, avec le seau.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le manteau est repris, le seau aussi.",
            "narrateur|Les cubes, le livre, ou la dînette.",
            "papa|Près de quoi, Aniss ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le manteau sèche, le seau reste lourd.",
            "narrateur|Les cubes, le livre, ou la dînette.",
            "maman|Près de quoi, Aniss ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le seau est repris, près de la porte.",
            "narrateur|Les cubes, le livre, ou la dînette.",
            "papa|Près de quoi, Aniss ?",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    bodies = {
        (1, 1): [
            "narrateur|Sur le carrelage, une petite tour attend.",
            "narrateur|Aniss jette un cube, dans le seau.",
            f"{CHILD}|C'est le barrage, pour la mare !",
            "narrateur|Le cube tape le fond, trop fort.",
            "narrateur|L'eau saute, et cache le grain.",
            "papa|Le cube cache le fond, Aniss.",
            "maman|Le seau n'aime pas les coups.",
            f"{CHILD}|Je secoue, et ça sort !",
            "narrateur|Il lève le seau, puis s'arrête.",
            "narrateur|Cette fois, il ne fonce pas.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (1, 2): [
            "narrateur|Un livre est ouvert, sur la table.",
            "narrateur|Une barque est peinte, toute petite.",
            f"{CHILD}|Comme dans la cour, maman.",
            "narrateur|Il approche le seau, trop près.",
            "narrateur|Une goutte menace la page, et tient.",
            "papa|Le livre n'aime pas l'eau.",
            "maman|Une feuille peut faire bateau.",
            f"{CHILD}|Je verse dessus, pour la barque !",
            "narrateur|Il penche, puis s'arrête.",
            "narrateur|Une feuille collée cache le grain.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (1, 3): [
            "narrateur|Deux tasses sont en rond, près du buffet.",
            "narrateur|Aniss verse une goutte, dans une tasse.",
            f"{CHILD}|Soupe de pluie, pour le doudou.",
            "narrateur|Il pose la tasse, dans le seau.",
            "narrateur|La tasse colle, et cache le grain.",
            "papa|Elle s'est coincée, au fond.",
            "maman|Le seau n'est pas une casserole.",
            f"{CHILD}|Je tire, fort !",
            "narrateur|Il tire, puis s'arrête.",
            "narrateur|Cette fois, il ne fonce pas.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (2, 1): [
            "narrateur|Dans l'herbe, des cubes sont mouillés.",
            "narrateur|Un cube glisse sous le doigt.",
            f"{CHILD}|Ils sont trop glissants.",
            "narrateur|Il jette un cube, dans le seau.",
            "narrateur|Le cube recouvre le grain de limon.",
            "papa|Pour le barrage, un seul suffit.",
            "maman|Les autres restent dans l'herbe.",
            f"{CHILD}|Je secoue, dehors !",
            "narrateur|Il lève le seau, trop haut.",
            "narrateur|Puis il s'arrête, les bras lourds.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (2, 2): [
            "narrateur|Le livre est sous le banc, au sec.",
            "narrateur|Aniss le tire un peu.",
            f"{CHILD}|Les pages sont sèches.",
            "maman|On le laisse sous le banc, alors.",
            "narrateur|Il veut une feuille, pour le bateau.",
            "narrateur|Il plonge la main, dans le seau.",
            "narrateur|Une feuille collée cache le grain.",
            "papa|Dehors, l'eau est partout.",
            f"{CHILD}|Je sors tout, d'un coup !",
            "narrateur|Il s'arrête, la main mouillée.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (2, 3): [
            "narrateur|Les tasses sont sur une planche.",
            "narrateur|Une tasse a un fond d'eau.",
            f"{CHILD}|La pluie a servi, maman.",
            "narrateur|Aniss penche le seau, trop vite.",
            "narrateur|Une vague manque la tasse, et file.",
            "papa|La dînette reste au jardin ?",
            f"{CHILD}|Oui, moi je verse.",
            "narrateur|Il pose la tasse, dans le seau.",
            "narrateur|Elle cache le grain, collée.",
            "narrateur|Il veut tirer, puis s'arrête.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (3, 1): [
            "narrateur|Près du lit, une tour de cubes tient.",
            "narrateur|Aniss passe trop vite, le seau contre lui.",
            "narrateur|Un cube tombe, et roule.",
            f"{CHILD}|Oh.",
            "papa|On la recule, la tour.",
            "narrateur|Il jette le cube, dans le seau.",
            "narrateur|Le cube cache le grain, au fond.",
            "maman|Maintenant tu peux passer.",
            f"{CHILD}|Je secoue, jusqu'à la cour !",
            "narrateur|L'anse tape le bois, puis il s'arrête.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (3, 2): [
            "narrateur|Le livre est sur le lit, ouvert.",
            "narrateur|Un rond de fenêtre touche la page.",
            f"{CHILD}|La cour est dedans, papa.",
            "maman|Une feuille peut faire bateau.",
            "narrateur|Il approche le seau, du lit.",
            "narrateur|Une goutte tremble, trop près.",
            "papa|Les pages n'aiment pas l'eau.",
            f"{CHILD}|Je verse sur la barque !",
            "narrateur|Une feuille du seau cache le grain.",
            "narrateur|Il penche, puis s'arrête.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
        (3, 3): [
            "narrateur|Deux tasses attendent, sur le chevet.",
            "narrateur|Aniss avait servi le doudou.",
            f"{CHILD}|Il a bu, tout seul.",
            "narrateur|Il verse une goutte, dans une tasse.",
            "narrateur|Puis il pose la tasse, dans le seau.",
            "narrateur|La tasse colle, et cache le grain.",
            "papa|Elle s'est coincée, Aniss.",
            "maman|La dînette reste ici, alors ?",
            f"{CHILD}|Je tire, et on court !",
            "narrateur|Il tire, puis s'arrête.",
            f"{CHILD}|Je veux voir, au fond.",
        ],
    }
    return vet(bodies[(a, b)])


T3_CHOICE = {
    1: vet(
        [
            "narrateur|Le cube cache le fond, le seau attend.",
            "narrateur|Le matin, après la sieste, ou le soir.",
            "maman|C'est quel moment, Aniss ?",
        ]
    ),
    2: vet(
        [
            "narrateur|La feuille cache le fond, le seau attend.",
            "narrateur|Le matin, après la sieste, ou le soir.",
            "papa|C'est quel moment, Aniss ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La tasse cache le fond, le seau attend.",
            "narrateur|Le matin, après la sieste, ou le soir.",
            "maman|C'est quel moment, Aniss ?",
        ]
    ),
}


def t3_scene(a: int, b: int, c: int) -> list[str]:
    bodies = {
        (1, 1, 1): [
            f"{CHILD}|Le matin, le soleil est pâle !",
            "narrateur|Les flaques dorent un peu, sur les dalles.",
            "narrateur|Aniss penche le seau, vers la lumière.",
            "narrateur|Le cube glisse, et le grain de limon paraît.",
            f"{CHILD}|Il était là, depuis la porte !",
            "papa|Tu l'as vu, sans secouer.",
            "narrateur|Il pose le cube, contre la tour.",
            "narrateur|Puis il verse, lent, vers la mare.",
            "maman|Le barrage tient, au bord.",
            "narrateur|Le grain de limon reste au fond, mouillé.",
        ],
        (1, 1, 2): [
            f"{CHILD}|Après la sieste, la maison est tiède.",
            "narrateur|Le store claque, une fois, puis se tait.",
            "narrateur|Aniss écoute le plastique, tout près.",
            "narrateur|Il sort le cube, sans le jeter.",
            "narrateur|Le grain de limon brille, dans l'ombre.",
            f"{CHILD}|Il n'est pas parti, papa.",
            "maman|Tu l'as regardé, au fond.",
            "narrateur|Il range le cube, sous la table.",
            "narrateur|Il verse une rivière, vers la cour.",
            "narrateur|Le grain de limon reste, collé.",
        ],
        (1, 1, 3): [
            f"{CHILD}|Le soir, la lampe fait un rond jaune.",
            "narrateur|Un vélo passe, tout loin.",
            "narrateur|L'ombre du cube tombe, sur le fond.",
            "narrateur|Aniss soulève le cube, sans le lancer.",
            "narrateur|Le grain de limon luit, sous la lampe.",
            f"{CHILD}|Je le vois, collé !",
            "papa|Tu as attendu, pour le voir.",
            "narrateur|Il pose le cube, près du buffet.",
            "narrateur|Il verse, vers la mare sombre.",
            "narrateur|Le grain de limon veille, au plastique.",
        ],
        (1, 2, 1): [
            f"{CHILD}|Le matin, je sors la feuille, doucement.",
            "narrateur|Le soleil pâle entre, par la fenêtre.",
            "narrateur|Aniss tire la feuille, sans la déchirer.",
            "narrateur|Le grain de limon apparaît, au fond.",
            "papa|Le livre reste au sec, sur la table.",
            f"{CHILD}|Le bateau, c'est cette feuille.",
            "maman|Tu l'as prise, sans verser.",
            "narrateur|Il recule le livre, d'une main.",
            "narrateur|Il pose la feuille, sur la mare dorée.",
            "narrateur|Le grain de limon reste au seau.",
        ],
        (1, 2, 2): [
            f"{CHILD}|Après la sieste, je regarde d'abord.",
            "narrateur|La maison est calme, tiède.",
            "narrateur|Aniss écoute, puis sort la feuille.",
            "narrateur|Le grain de limon est là, dans l'ombre.",
            "maman|Les pages n'ont pas bu.",
            f"{CHILD}|Il tenait sous la feuille, papa.",
            "papa|Tu as vu, sans foncer.",
            "narrateur|Il referme le livre, au sec.",
            "narrateur|La feuille-bateau part, vers la cour.",
            "narrateur|Le grain de limon reste, au chaud.",
        ],
        (1, 2, 3): [
            f"{CHILD}|Le soir, la lampe montre le fond.",
            "narrateur|Un rond jaune touche le plastique.",
            "narrateur|Aniss lève la feuille, sans la froisser.",
            "narrateur|Le grain de limon luit, collé.",
            "papa|Le livre dort, loin de l'eau.",
            f"{CHILD}|Je le mets sur la mare, tout seul.",
            "maman|La barque a une feuille, pas une page.",
            "narrateur|Il pose le livre, contre le buffet.",
            "narrateur|La feuille sombre, sur l'eau noire.",
            "narrateur|Le grain de limon veille, au fond.",
        ],
        (1, 3, 1): [
            f"{CHILD}|Le matin, je sors la tasse, lentement.",
            "narrateur|Le soleil pâle touche le bord.",
            "narrateur|Aniss tourne la tasse, sans tirer.",
            "narrateur|Elle se décolle, le grain de limon paraît.",
            "papa|Tu as tourné, pas arraché.",
            f"{CHILD}|La soupe reste dans la tasse.",
            "maman|La dînette rentre, près du buffet.",
            "narrateur|Il pose la tasse, dans le rond.",
            "narrateur|Il verse le reste, vers la mare.",
            "narrateur|Le grain de limon tient le fond.",
        ],
        (1, 3, 2): [
            f"{CHILD}|Après la sieste, j'écoute la tasse.",
            "narrateur|Un petit bruit de plastique, puis rien.",
            "narrateur|Aniss soulève la tasse, tout droit.",
            "narrateur|Le grain de limon brille, dans l'ombre.",
            "maman|Elle n'est plus coincée.",
            f"{CHILD}|Il était dessous, papa.",
            "papa|Tu as levé, sans secouer.",
            "narrateur|Il essuie le bord, du doigt.",
            "narrateur|La tasse rentre, la rivière part.",
            "narrateur|Le grain de limon reste, collé.",
        ],
        (1, 3, 3): [
            f"{CHILD}|Le soir, la lampe montre la tasse.",
            "narrateur|Une ombre ronde tombe, sur le fond.",
            "narrateur|Aniss fait tourner la tasse, lent.",
            "narrateur|Le grain de limon luit, sous le rond.",
            "papa|Tu l'as vue, collée.",
            f"{CHILD}|Je la range, puis je verse.",
            "maman|La dînette reste sage, près du buffet.",
            "narrateur|Il pose la tasse, dans le cercle.",
            "narrateur|Il verse, vers la mare sombre.",
            "narrateur|Le grain de limon tremble, au plastique.",
        ],
        (2, 1, 1): [
            f"{CHILD}|Le matin, je sors le cube, dans l'herbe.",
            "narrateur|Les flaques dorent, près du banc.",
            "narrateur|Aniss penche le seau, vers le soleil.",
            "narrateur|Le cube glisse, le grain de limon paraît.",
            "papa|Un seul cube, pour le barrage.",
            f"{CHILD}|Les autres restent là, mouillés.",
            "maman|Tu as regardé, avant de verser.",
            "narrateur|Il pose le cube, au bord de la flaque.",
            "narrateur|L'eau tourne autour, et tient.",
            "narrateur|Le grain de limon reste au seau.",
        ],
        (2, 1, 2): [
            f"{CHILD}|Après la sieste, le jardin est tiède.",
            "narrateur|Une abeille passe, puis s'éloigne.",
            "narrateur|Aniss écoute l'anse, contre sa paume.",
            "narrateur|Il sort le cube, sans le lancer.",
            "narrateur|Le grain de limon brille, à l'ombre du banc.",
            "maman|Les cubes restent dans l'herbe.",
            f"{CHILD}|Lui, il reste avec moi.",
            "papa|Tu as vu le fond, sans foncer.",
            "narrateur|Il verse, vers la flaque ronde.",
            "narrateur|Le grain de limon reste, au chaud.",
        ],
        (2, 1, 3): [
            f"{CHILD}|Le soir, la lampe de la cuisine éclaire.",
            "narrateur|Le banc fait une ombre longue.",
            "narrateur|Aniss soulève le cube, face à la lumière.",
            "narrateur|Le grain de limon luit, au fond jaune.",
            "papa|Le dessous du banc est vide, maintenant.",
            f"{CHILD}|Le cube va au bord, pas au fond.",
            "maman|Tu l'as posé, sans le jeter.",
            "narrateur|Il range le cube, dans l'herbe.",
            "narrateur|Il verse, vers la flaque sombre.",
            "narrateur|Le grain de limon veille, au seau.",
        ],
        (2, 2, 1): [
            f"{CHILD}|Le matin, je sors la feuille, au soleil.",
            "narrateur|Les pots du jardin gardent le livre, au sec.",
            "narrateur|Aniss tire la feuille, sans la casser.",
            "narrateur|Le grain de limon apparaît, mouillé.",
            "papa|Le bateau, c'est une feuille de la cour.",
            f"{CHILD}|Pas le livre, lui reste là.",
            "maman|Tu l'as laissé, sous le banc.",
            "narrateur|Il referme le livre, d'une main.",
            "narrateur|La feuille part, sur la flaque dorée.",
            "narrateur|Le grain de limon reste au seau.",
        ],
        (2, 2, 2): [
            f"{CHILD}|Après la sieste, je regarde sous le banc.",
            "narrateur|La barrière n'a plus le manteau.",
            "narrateur|Aniss sort la feuille, tout droit.",
            "narrateur|Le grain de limon est là, dans l'ombre.",
            "maman|Les pages sont restées sèches.",
            f"{CHILD}|Il tenait dessous, papa.",
            "papa|Tu as vu, sans plonger trop fort.",
            "narrateur|Il glisse le livre, à sa place.",
            "narrateur|La feuille-bateau part, vers l'herbe.",
            "narrateur|Le grain de limon reste, au chaud.",
        ],
        (2, 2, 3): [
            f"{CHILD}|Le soir, la lampe touche l'herbe haute.",
            "narrateur|Aniss lève la feuille, face au rond jaune.",
            "narrateur|Le grain de limon luit, collé.",
            "papa|L'herbe haute n'a plus besoin du livre.",
            f"{CHILD}|Le bateau nage, le livre dort.",
            "maman|Tu l'as sorti, sans le froisser.",
            "narrateur|Il pose le livre, sous le banc.",
            "narrateur|La feuille sombre, sur l'eau noire.",
            "narrateur|Une chouette crie, tout loin.",
            "narrateur|Le grain de limon veille, au fond.",
        ],
        (2, 3, 1): [
            f"{CHILD}|Le matin, je sors la tasse, au cerisier.",
            "narrateur|Le soleil pâle touche la planche.",
            "narrateur|Aniss tourne la tasse, sans tirer.",
            "narrateur|Le grain de limon paraît, au fond.",
            "papa|La dînette reste au jardin.",
            f"{CHILD}|La soupe est froide, je verse dehors.",
            "maman|Tu as tourné, pas arraché.",
            "narrateur|Il pose la tasse, sur la planche.",
            "narrateur|Il verse le reste, vers la flaque.",
            "narrateur|Le grain de limon tient le seau.",
        ],
        (2, 3, 2): [
            f"{CHILD}|Après la sieste, le paillasson est tiède.",
            "narrateur|Aniss écoute la tasse, collée.",
            "narrateur|Il la soulève, tout droit.",
            "narrateur|Le grain de limon brille, à l'ombre.",
            "maman|Le paillasson du jardin est vide.",
            f"{CHILD}|Elle n'est plus coincée, papa.",
            "papa|Tu as levé, sans secouer.",
            "narrateur|Il essuie le bord, du doigt.",
            "narrateur|La tasse rentre, la rivière part.",
            "narrateur|Le grain de limon reste, collé.",
        ],
        (2, 3, 3): [
            f"{CHILD}|Le soir, la brouette fait une ombre.",
            "narrateur|La lampe de la cuisine éclaire le fond.",
            "narrateur|Aniss fait tourner la tasse, lent.",
            "narrateur|Le grain de limon luit, sous le rond.",
            "papa|La brouette reste, toute seule.",
            f"{CHILD}|Je range la tasse, puis je verse.",
            "maman|La dînette tient, sur la planche.",
            "narrateur|Il pose la tasse, près de l'eau froide.",
            "narrateur|Il verse, vers la flaque sombre.",
            "narrateur|Le grain de limon tremble, au seau.",
        ],
        (3, 1, 1): [
            f"{CHILD}|Le matin, je sors le cube, près du lit.",
            "narrateur|Le soleil pâle entre, par le volet.",
            "narrateur|Aniss penche le seau, vers la lumière.",
            "narrateur|Le cube glisse, le grain de limon paraît.",
            "papa|On recule la tour, puis on verse.",
            f"{CHILD}|Le cube va sur la tour, pas au fond.",
            "maman|Tu as vu, sans secouer.",
            "narrateur|Il pose le cube, contre la tour.",
            "narrateur|Il verse, vers la mare dorée.",
            "narrateur|Le grain de limon reste au seau.",
        ],
        (3, 1, 2): [
            f"{CHILD}|Après la sieste, un cube a roulé.",
            "narrateur|La maison est calme, tiède.",
            "narrateur|Aniss écoute, puis sort le cube.",
            "narrateur|Le grain de limon brille, dans l'ombre du lit.",
            "maman|Un cube reste sous le lit.",
            f"{CHILD}|Lui, je le range, papa.",
            "papa|Tu as regardé, au fond.",
            "narrateur|Il pousse le cube, sous le bois.",
            "narrateur|Il verse, vers la cour tiède.",
            "narrateur|Le grain de limon reste, au chaud.",
        ],
        (3, 1, 3): [
            f"{CHILD}|Le soir, la lampe touche l'oreiller.",
            "narrateur|L'ombre du cube tombe, sur le fond.",
            "narrateur|Aniss soulève le cube, sans le lancer.",
            "narrateur|Le grain de limon luit, collé.",
            "papa|L'oreiller n'a plus le doudou.",
            f"{CHILD}|Le doudou est avec moi, le cube ici.",
            "maman|Tu l'as posé, sans le jeter.",
            "narrateur|Il range le cube, près de la tour.",
            "narrateur|Il verse, vers la mare sombre.",
            "narrateur|Le grain de limon veille, au seau.",
        ],
        (3, 2, 1): [
            f"{CHILD}|Le matin, je sors la feuille, du seau.",
            "narrateur|Le soleil pâle touche le livre, sur le lit.",
            "narrateur|Aniss tire la feuille, sans la déchirer.",
            "narrateur|Le grain de limon apparaît, au fond.",
            "papa|Le livre de la chambre se referme.",
            f"{CHILD}|Le bateau, c'est la feuille, pas la page.",
            "maman|Tu l'as prise, sans verser.",
            "narrateur|Il recule le livre, d'une main.",
            "narrateur|La feuille part, sur la mare dorée.",
            "narrateur|Le grain de limon reste au seau.",
        ],
        (3, 2, 2): [
            f"{CHILD}|Après la sieste, la fenêtre est un peu floue.",
            "narrateur|Aniss écoute, puis sort la feuille.",
            "narrateur|Le grain de limon est là, dans l'ombre.",
            "maman|Les pages n'ont pas bu.",
            f"{CHILD}|Il tenait sous la feuille, papa.",
            "papa|Tu as vu, sans foncer.",
            "narrateur|Il referme le livre, au sec.",
            "narrateur|La feuille-bateau part, vers la cour.",
            "narrateur|Un store claque, une fois.",
            "narrateur|Le grain de limon reste, au chaud.",
        ],
        (3, 2, 3): [
            f"{CHILD}|Le soir, un signet dépasse, du livre.",
            "narrateur|La lampe fait un rond, sur le plastique.",
            "narrateur|Aniss lève la feuille, sans la froisser.",
            "narrateur|Le grain de limon luit, collé.",
            "papa|Le signet garde la page, au sec.",
            f"{CHILD}|Je mets la feuille, sur la mare.",
            "maman|La barque a une feuille, pas une page.",
            "narrateur|Il pose le livre, sur le lit.",
            "narrateur|La feuille sombre, sur l'eau noire.",
            "narrateur|Le grain de limon veille, au fond.",
        ],
        (3, 3, 1): [
            f"{CHILD}|Le matin, je sors la tasse, du seau.",
            "narrateur|Le soleil pâle touche le chevet.",
            "narrateur|Aniss tourne la tasse, sans tirer.",
            "narrateur|Le grain de limon paraît, au fond.",
            "papa|Les tasses restent au chevet.",
            f"{CHILD}|La soupe est pour le doudou, ici.",
            "maman|Tu as tourné, pas arraché.",
            "narrateur|Il pose la tasse, dans le rond.",
            "narrateur|Il verse le reste, vers la mare.",
            "narrateur|Le grain de limon tient le fond.",
        ],
        (3, 3, 2): [
            f"{CHILD}|Après la sieste, le lit est défait.",
            "narrateur|Aniss écoute la tasse, collée.",
            "narrateur|Il la soulève, tout droit.",
            "narrateur|Le grain de limon brille, dans l'ombre.",
            "maman|Le lit attend, un peu froissé.",
            f"{CHILD}|Elle n'est plus coincée, papa.",
            "papa|Tu as levé, sans secouer.",
            "narrateur|Il essuie le bord, du doigt.",
            "narrateur|La tasse rentre, la rivière part.",
            "narrateur|Le grain de limon reste, collé.",
        ],
        (3, 3, 3): [
            f"{CHILD}|Le soir, le crochet de la chambre est vide.",
            "narrateur|La lampe montre le fond, tout rond.",
            "narrateur|Aniss fait tourner la tasse, lent.",
            "narrateur|Le grain de limon luit, sous le rond.",
            "papa|Le manteau est sur toi, pas au crochet.",
            f"{CHILD}|Je range la tasse, puis je verse.",
            "maman|La dînette reste au chevet.",
            "narrateur|Il pose la tasse, près du doudou.",
            "narrateur|Il verse, vers la mare sombre.",
            "narrateur|Le grain de limon tremble, au plastique.",
        ],
    }
    return vet(bodies[(a, b, c)])


END_LAST = {
    (1, 1, 1): "Le grain de limon sèche au fond, sous le soleil pâle.",
    (1, 1, 2): "Le cube a laissé un rond d'ombre, autour du grain.",
    (1, 1, 3): "La lampe dorée le grain, collé au plastique jaune.",
    (1, 2, 1): "Une page sèche au buffet, le grain brille au fond.",
    (1, 2, 2): "Le livre garde son signet, le grain son fond jaune.",
    (1, 2, 3): "Le grain veille, sous le rond de la lampe.",
    (1, 3, 1): "La tasse est rentrée, le grain tient le fond.",
    (1, 3, 2): "Une trace de soupe a quitté le grain, au plastique.",
    (1, 3, 3): "Le grain tremble, près de la tasse du buffet.",
    (2, 1, 1): "L'herbe n'a plus le cube, le grain voyage au seau.",
    (2, 1, 2): "Les cubes restent dans l'herbe, le grain au chaud.",
    (2, 1, 3): "Le dessous du banc est vide, le grain rentré.",
    (2, 2, 1): "Les pots gardent le livre, le grain voyage au seau.",
    (2, 2, 2): "La barrière n'a plus le manteau, le grain reste.",
    (2, 2, 3): "L'herbe haute ignore le grain, au fond jaune.",
    (2, 3, 1): "Le cerisier n'a plus le seau, le grain part.",
    (2, 3, 2): "Le paillasson du jardin est vide, le grain voyage.",
    (2, 3, 3): "La brouette reste seule, le grain rentré au seau.",
    (3, 1, 1): "La tour de la chambre tient, le grain dort au fond.",
    (3, 1, 2): "Un cube a roulé sous le lit, le grain au seau.",
    (3, 1, 3): "L'oreiller n'a plus le doudou, le grain veille.",
    (3, 2, 1): "Le livre de la chambre est fermé, le grain au plastique.",
    (3, 2, 2): "La fenêtre de la chambre est floue, le grain au chaud.",
    (3, 2, 3): "Un signet dépasse, le grain reste au fond jaune.",
    (3, 3, 1): "Les tasses restent au chevet, le grain au seau.",
    (3, 3, 2): "Le lit est défait, le grain rentré dans le jaune.",
    (3, 3, 3): "Le crochet de la chambre est vide, le grain au seau.",
}

END_TRACE = {
    (1, 1, 1): "Le cube jaune sèche, au bord de la flaque.",
    (1, 1, 2): "La petite tour reste à l'ombre, près du seau.",
    (1, 1, 3): "Le cube brille, sous la lampe, un peu mouillé.",
    (1, 2, 1): "La feuille-bateau s'arrête, contre une dalle.",
    (1, 2, 2): "Le livre reste sur la table, bien sec.",
    (1, 2, 3): "La feuille sombre dans l'eau, sans un bruit.",
    (1, 3, 1): "La tasse a un fond d'eau claire.",
    (1, 3, 2): "La dînette reste sage, près du buffet.",
    (1, 3, 3): "Une goutte tremble, au bord de la tasse.",
    (2, 1, 1): "L'herbe ne tient plus le seau.",
    (2, 1, 2): "Les cubes mouillés restent dans l'herbe.",
    (2, 1, 3): "Le dessous du banc est vide, maintenant.",
    (2, 2, 1): "Les pots du jardin gardent le livre au sec.",
    (2, 2, 2): "La barrière n'a plus le manteau.",
    (2, 2, 3): "L'herbe haute est calme, sans le doudou.",
    (2, 3, 1): "Le cerisier n'a plus le seau, à son pied.",
    (2, 3, 2): "Le paillasson du jardin est vide.",
    (2, 3, 3): "La brouette reste, toute seule.",
    (3, 1, 1): "La tour de la chambre tient, un peu de travers.",
    (3, 1, 2): "Un cube a roulé sous le lit, et reste.",
    (3, 1, 3): "L'oreiller n'a plus le doudou.",
    (3, 2, 1): "Le livre de la chambre est refermé.",
    (3, 2, 2): "La fenêtre de la chambre est un peu floue.",
    (3, 2, 3): "Un signet dépasse, du livre fermé.",
    (3, 3, 1): "Les tasses restent au chevet.",
    (3, 3, 2): "Le lit est défait, un peu froissé.",
    (3, 3, 3): "Le crochet de la chambre est vide.",
}

END_FAIL = {
    1: "Le seau a failli rester, sous la table.",
    2: "Le manteau a failli boire, tout seul.",
    3: "Le seau a failli rester, près de la porte.",
}

END_SAY = {
    (1, 1): "J'ai le seau, et le cube est rentré.",
    (1, 2): "J'ai le seau, et le livre est au sec.",
    (1, 3): "J'ai le seau, et la tasse est rentrée.",
    (2, 1): "J'ai le seau, et le cube est dans l'herbe.",
    (2, 2): "J'ai le seau, et le livre est sous le banc.",
    (2, 3): "J'ai le seau, et la tasse est sur la planche.",
    (3, 1): "J'ai le seau, et la tour tient.",
    (3, 2): "J'ai le seau, et le livre est fermé.",
    (3, 3): "J'ai le seau, et les tasses sont au chevet.",
}

END_PAPA = {
    1: "Tu as repris ce qui t'attendait.",
    2: "Tu as regardé, avant de verser.",
    3: "Tu as ramené le seau, avec toi.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    return vet(
        [
            f"narrateur|{END_TRACE[(a, b, c)]}",
            f"{CHILD}|{END_SAY[(a, b)]}",
            f"narrateur|{END_FAIL[a]}",
            f"{CHILD}|Ça a failli rater.",
            f"papa|{END_PAPA[c]}",
            "maman|Le grain est resté, au fond.",
            f"{CHILD}|Je le garde, dans le seau jaune.",
            f"narrateur|{END_LAST[(a, b, c)]}",
        ]
    )


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (
        OPENING,
        "opening",
        "pluie,seau,porte",
        {"emphasis": "grain de limon"},
    )
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "la cuisine",
            "option_2_label": "le jardin",
            "option_3_label": "la chambre",
            "pause_before_ms": 200,
        },
    )

    t2_labs = ("les cubes", "le livre", "la dînette")
    t3_labs = ("le matin", "après la sieste", "le soir")
    t2_sons = {1: "cubes,bois", 2: "livre,pages", 3: "tasse,dinette"}
    t2_emp = {1: "cubes", 2: "livre", 3: "tasse"}
    t3_sons = {1: "porte,matin", 2: "rideau,sieste", 3: "lampe,soir"}
    fin_sons = {1: "seau,dalles", 2: "seau,store", 3: "seau,lampe"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        scripts[base] = (t1["passage"], "action", t1["sons"], {"emphasis": t1["emp"]})
        scripts[f"{base}_Q0001"] = (
            t1["question"],
            "clue",
            "",
            {
                "expected_answer": t1["ans"],
                "accepted_examples": t1["acc"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["ans"],
            },
        )
        scripts[f"{base}_C0001"] = (
            t1["confirm"],
            "confirm",
            t1["sons"],
            {"emphasis": "seau"},
        )
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": t2_labs[0],
                "option_2_label": t2_labs[1],
                "option_3_label": t2_labs[2],
                "pause_before_ms": 200,
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                t2_scene(a, b),
                "obstacle",
                t2_sons[b],
                {"emphasis": t2_emp[b]},
            )
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_CHOICE[b],
                "choice",
                "",
                {
                    "option_1_label": t3_labs[0],
                    "option_2_label": t3_labs[1],
                    "option_3_label": t3_labs[2],
                    "pause_before_ms": 200,
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    t3_scene(a, b, c),
                    "resolution",
                    t3_sons[c],
                    {"emphasis": "grain de limon"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    ending(a, b, c),
                    "ending",
                    fin_sons[c],
                    {"emphasis": "grain de limon", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra)[:8]}")

    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        lines, profile, sons, extra = scripts[cid]
        chunks.append(voice(by_src[cid], lines, profile, sons, extra))

    fins = [ch["text"] for ch in chunks if ch["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(fins))}/27")
    last_n = []
    for ch in chunks:
        if ch.get("kind") != "passage_fin":
            continue
        last = [x for x in ch["script"].splitlines() if x.startswith("narrateur|")][-1]
        last_n.append(last.split("|", 1)[1])
        last_low = last.split("|", 1)[1].lower()
        if "histoire" in last_low or "bravo" in last_low or "bon travail" in last_low:
            raise SystemExit(f"{ch['chunk_id']} fin mécanique: {last_low}")
    if len(set(last_n)) != 27:
        raise SystemExit(f"dernières images: {len(set(last_n))}/27")
    res_txt = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage"
        and "_T0003_P000" in ch["chunk_id"]
        and "_F0001" not in ch["chunk_id"]
        and not ch["chunk_id"].endswith("_T0003_P0000")
    ]
    if len(res_txt) != 27 or len(set(res_txt)) != 27:
        raise SystemExit(f"résolutions distinctes: {len(set(res_txt))}/{len(res_txt)}")
    t2_only = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage" and "_T0002_P000" in ch["chunk_id"] and "T0003" not in ch["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "seau jaune" not in blob:
        raise SystemExit(f"{SID}: seau jaune absent")
    if "grain de limon" not in chunks[0]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    for ch in chunks:
        if (
            ch["kind"] == "passage"
            and "T0003_P000" in ch["chunk_id"]
            and "_F0001" not in ch["chunk_id"]
            and not ch["chunk_id"].endswith("T0003_P0000")
        ):
            if "grain de limon" not in ch["text"].lower():
                raise SystemExit(f"indice non payé: {ch['chunk_id']}")
    for tic in ("tout doux", "tout calme", " aujourd'hui,"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in ("merle", "couleur de miel", "tom ", "léa", "sami", "hugo", "laitue"):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] if "|" in a else a for a in adults)
    if "merci" not in aj:
        raise SystemExit(f"{SID}: merci absent des adultes")

    out = dict(src)
    out["fil_rouge"] = (
        "Aniss connaît la cour, dalle par dalle. Après la pluie, un détail "
        "paraît neuf : un grain de limon colle au fond du seau jaune. Il veut "
        "porter le seau jusqu'à la mare des dalles, avant que le soleil boive "
        "les flaques. Il tire trop fort ; l'anse résiste, pince. Papa "
        "s'accroupit. Cuisine, jardin ou chambre : le seau part avec lui. Il "
        "laisse le manteau, ou le seau. Il revient. Cubes, livre ou dînette : "
        "l'objet cache le grain. Il refuse de foncer. Matin, sieste ou soir : "
        "il regarde, range, verse. Le grain paie le début. Vingt-sept traces."
    )
    out["title"] = TITLE
    out["characters"] = "Aniss, papa, maman"
    out["setting"] = "cour après la pluie, maison"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])

    def path_words(a: int, b: int, c: int) -> int:
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
        mp = {ch["chunk_id"]: ch for ch in chunks}
        return sum(words(mp[i]["text"]) for i in ids)

    lengths = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(lengths) < 380:
        raise SystemExit(f"chemin trop court: {min(lengths)}")

    t1s = [next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P000{i}") for i in (1, 2, 3)]
    if len(set(t1s)) < 3:
        raise SystemExit("T1 ne change pas l'histoire")
    t2s = [
        next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P000{j}")
        for j in (1, 2, 3)
    ]
    if len(set(t2s)) < 3:
        raise SystemExit("T2 ne change pas l'histoire")
    t3s = [
        next(
            ch["text"]
            for ch in chunks
            if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P0001_T0003_P000{k}"
        )
        for k in (1, 2, 3)
    ]
    if len(set(t3s)) < 3:
        raise SystemExit("T3 ne change pas l'histoire")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-AUT-008 — Le seau jaune d'Aniss\n\n"
        "- **Nouveau titre :** *Le seau jaune d'Aniss*\n"
        "- **Public :** 4–5 ans (N2), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.AFF.003 — reprendre / ranger ses affaires "
        "(vécue, non dite)\n"
        "- **Personnages :** Aniss, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, "
        "27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Aniss connaît la cour, dalle par dalle. Après la pluie, un détail "
        "paraît neuf : un grain de limon colle au fond du seau jaune. Il veut "
        "porter le seau jusqu'à la mare des dalles, avant que le soleil boive "
        "les flaques. Il tire trop fort ; l'anse résiste. Papa s'accroupit. "
        "Cuisine, jardin ou chambre : le seau part avec lui. Il laisse le "
        "manteau ou le seau, puis revient. Cubes, livre ou dînette cachent le "
        "grain. Il refuse de foncer. Matin, sieste ou soir : il regarde, range, "
        "verse. Le grain paie l'ouverture. Le seau a failli rester.\n\n"
        "## Améliorations appliquées\n\n"
        "- Ouverture inventée (cour connue, détail neuf), pas la goutte-cloche.\n"
        "- Indice unique : grain de limon, payé à chaque climax et chaque fin.\n"
        "- Corps : sourire disparu, poitrine bousculée, adulte accroupi.\n"
        "- Première idée échoue (anse, manteau, seau oublié). Seconde ruse : "
        "l'objet cache le grain. Aniss refuse de foncer.\n"
        "- T1/T2/T3 changent l'action. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Un merci vécu (ouverture). Papa et maman parlent. Une question.\n"
        "- Pas de 2e enfant. Pas « encore / déjà / tout doux ». Pas merle, "
        "pas miel, pas apply.\n"
        "- Monde ≠ TREE-DIF-006 (arrosoirs), ≠ TREE-COL-008 (goutte arrosoir), "
        "≠ TREE-DIF-067 (puits), ≠ TREE-DIF-005 (toboggan, mica).\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/"
        "ending) : notes, text_ssml, text_xai_tags, piper 1.10–1.30.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N2 ≤ 15 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(manteau / manteau / seau). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(
        f"OK {SID} {nwords} mots  fins={len(set(fins))}  "
        f"chemins {min(lengths)}-{max(lengths)} moy {sum(lengths)//len(lengths)}  "
        f"1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}"
    )


if __name__ == "__main__":
    main()
