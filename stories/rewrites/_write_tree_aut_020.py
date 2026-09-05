#!/usr/bin/env python3
"""TREE-AUT-020 — Le chat à la fenêtre d'Amir (F-NAR-019, N1, AUT.AFF.003, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-020"
N1 = LIMITS["N1"]
TITLE = "Le chat à la fenêtre d'Amir"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="anneau de pollen",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=1; destinataire=enfant; sous_texte=le_chat_tapote_l_anneau; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note=(
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton_choix_change_la_suite; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="coussin",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=reprendre_le_coussin_sans_forcer; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="coussin rayé",
        note=(
            "arc=confirmation; intention=relancer; emotion=élan; intensite=1; "
            "destinataire=enfant; sous_texte=il_reprend_sans_courir; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=il_jette_le_coussin_trop_vite; "
            "tempo=vif; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=le_jouet_n_appelle_pas_le_chat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="anneau de pollen",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=il_pose_le_nid_et_attend; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="anneau de pollen",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_anneau_a_quitté_le_verre; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": (
        "reprendre | le seau | le manteau | ses affaires | il le prend | "
        "je le prends | le coussin | je le reprends"
    ),
    "retry_prompt": "Il reprend le coussin. Amir fait quoi ?",
    "engine_ok_text": "Oui, reprendre.",
    "engine_near_text": "Tu es près. Écoute l'indice.",
}

LOC = {
    1: dict(name="le bac à sable", short="bac", sons="sable,chat"),
    2: dict(name="le toboggan", short="toboggan", sons="metal,chat"),
    3: dict(name="les balançoires", short="balançoires", sons="corde,chat"),
}
OBJ = {
    1: dict(name="le ballon", short="ballon", sons="ballon,chat"),
    2: dict(name="le seau", short="seau", sons="seau,chat"),
    3: dict(name="le doudou", short="doudou", sons="doudou,chat"),
}
AFF = {
    1: dict(name="le manteau", short="manteau", sons="tissu,chat"),
    2: dict(name="les chaussures", short="chaussures", sons="cuir,chat"),
    3: dict(name="le sac", short="sac", sons="sac,chat"),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
        if tok and tok == prev:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {tok}: {ph}")
        else:
            run = 1
        prev = tok
        out.append(f"{role}|{ph}")
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


def path_ids(a: int, b: int, c: int) -> list[str]:
    return [
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


# Ouverture : un tic sans maître, puis l'anneau de pollen (indice unique).
OPENING = [
    "narrateur|Un tic minuscule frappe le verre.",
    "narrateur|Puis un autre tic, plus près.",
    "narrateur|Amir lève les yeux, vers la fenêtre.",
    "narrateur|Le bois du rebord sent le soleil.",
    "narrateur|Un coussin rayé dort, un peu plat.",
    "narrateur|Il fait poc, si on le pose.",
    "narrateur|Dehors, le jardin des trois coins attend.",
    "narrateur|Sur le verre, un détail brille, nouveau.",
    "narrateur|Un anneau de pollen, orange, minuscule.",
    "narrateur|Il est collé, côté maison, tout net.",
    "narrateur|Un chat tapote, pile sur l'anneau.",
    "narrateur|Sa moustache touche le cercle, puis recule.",
    "papa|Tu as vu, Amir ?",
    "enfant-m|Il veut jouer, tout de suite !",
    "narrateur|En ce moment, Amir ouvre trop vite.",
    "narrateur|Le chat saute, loin du rebord chaud.",
    "narrateur|Le sourire d'Amir disparaît.",
    "enfant-m|Reviens !",
    "narrateur|Ses épaules baissent, près du bois.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "maman|Il n'aime pas la main trop vite.",
    "papa|Le jardin, peut-être ?",
    "enfant-m|Je le rattrape, avec le coussin !",
    "narrateur|Amir serre le coussin, impatient.",
    "maman|On sort, le chat est dehors.",
]

T1_CHOICE = [
    "narrateur|Le chat a choisi un coin, dehors.",
    "narrateur|Le bac à sable.",
    "narrateur|Le toboggan.",
    "narrateur|Les balançoires.",
    "papa|On le rejoint où, Amir ?",
]

T1 = {
    1: [
        "narrateur|Amir court vers le bac à sable.",
        "narrateur|Le sable est frais, un peu pâle.",
        "narrateur|Le chat est là, près du bord.",
        "enfant-m|Je te pose le coussin, viens !",
        "narrateur|Il jette le coussin, trop vite.",
        "narrateur|Le poc fait lever le chat.",
        "narrateur|Des grains collent aux pattes grises.",
        "enfant-m|Reviens, je t'attrape !",
        "narrateur|Sa main ferme l'air, vide.",
        "narrateur|Le chat saute vers la haie.",
        "narrateur|Le sourire d'Amir disparaît.",
        "enfant-m|Il part, papa.",
        "papa|Regarde le coussin, pas tes mains.",
        "narrateur|Un anneau de pollen y brille, minuscule.",
        "maman|Le chat n'aime pas la main trop vite.",
        "narrateur|Les épaules d'Amir baissent, lourdes.",
        "narrateur|Un grain pâle reste sous son ongle.",
    ],
    2: [
        "narrateur|Amir grimpe vers le toboggan.",
        "narrateur|Le métal est tiède sous la paume.",
        "narrateur|Le chat est en haut, tout petit.",
        "enfant-m|Le coussin glisse avec toi !",
        "narrateur|Il pose le coussin sur la rampe.",
        "narrateur|Un toc, et le tissu dévale.",
        "narrateur|Le chat bondit, loin du métal.",
        "enfant-m|Attends, je te rattrape !",
        "narrateur|Amir descend trop vite, les pieds lourds.",
        "narrateur|Sa main ferme l'air, vide.",
        "narrateur|Le sourire d'Amir disparaît.",
        "enfant-m|Il est parti, maman.",
        "maman|Regarde le coussin, au bas.",
        "narrateur|Un anneau de pollen y brille, minuscule.",
        "papa|Le métal a fait trop de bruit.",
        "narrateur|Les épaules d'Amir baissent, au bas.",
        "narrateur|Une feuille colle au tissu rayé.",
    ],
    3: [
        "narrateur|Amir court vers les balançoires.",
        "narrateur|La corde est rêche, un peu tiède.",
        "narrateur|Le chat est sur le siège, immobile.",
        "enfant-m|Le coussin s'assoit avec toi !",
        "narrateur|Il pose le coussin, puis pousse.",
        "narrateur|Le siège part, le chat saute.",
        "narrateur|La corde racle, un petit cri sec.",
        "enfant-m|Reviens, je t'attrape !",
        "narrateur|Sa main ferme l'air, vide.",
        "narrateur|Le chat file sous les cordes.",
        "narrateur|Le sourire d'Amir disparaît.",
        "enfant-m|Il ne veut pas, papa.",
        "papa|Regarde le coussin, sur le bois.",
        "narrateur|Un anneau de pollen y brille, minuscule.",
        "maman|Le siège a bougé trop vite.",
        "narrateur|Les épaules d'Amir baissent, près du bois.",
        "narrateur|Un brin de corde reste au tissu.",
    ],
}

T1_Q = {
    1: [
        "narrateur|Le coussin rayé attend, tombé au bac.",
        "papa|Amir, tu fais quoi ?",
    ],
    2: [
        "narrateur|Le coussin rayé attend, au bas.",
        "maman|Amir, tu fais quoi ?",
    ],
    3: [
        "narrateur|Le coussin rayé attend, sur le bois.",
        "papa|Amir, tu fais quoi ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Amir se baisse vers le coussin rayé.",
        "narrateur|Il le reprend, grain par grain.",
        "enfant-m|Je le reprends, il est à moi.",
        "papa|Merci, Amir.",
        "maman|Tu le portes, sans courir ?",
        "enfant-m|Oui, je reste.",
        "narrateur|Un grain orange reste sur le tissu.",
        "narrateur|Le chat observe, loin, dans l'herbe.",
        "enfant-m|J'attends, moi aussi.",
        "narrateur|Le bac garde un creux, vide.",
    ],
    2: [
        "narrateur|Amir ramasse le coussin rayé, au bas.",
        "narrateur|Il le reprend, contre lui.",
        "enfant-m|Je le reprends, il est froid.",
        "maman|Bravo, Amir.",
        "papa|Tu le portes, sans glisser ?",
        "enfant-m|Oui, je marche.",
        "narrateur|Une feuille reste collée au tissu.",
        "narrateur|Le chat observe, loin, dans l'herbe.",
        "enfant-m|J'attends, moi aussi.",
        "narrateur|Le métal se tait, un instant.",
    ],
    3: [
        "narrateur|Amir reprend le coussin rayé, sur le bois.",
        "narrateur|Il le secoue, sans pousser le siège.",
        "enfant-m|Je le reprends, il est à moi.",
        "papa|Oui, tes mains sont prêtes.",
        "maman|Tu le portes, sans balancer ?",
        "enfant-m|Oui, je reste.",
        "narrateur|Un brin de corde reste au tissu.",
        "narrateur|Le chat observe, loin, dans l'herbe.",
        "enfant-m|J'attends, moi aussi.",
        "narrateur|La corde retombe, sans bruit.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Amir veut un jeu, sans forcer.",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
        "maman|Tu prends quoi, pour l'attendre ?",
    ],
    2: [
        "narrateur|Amir veut un jeu, près des marches.",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
        "papa|Tu prends quoi, pour l'attendre ?",
    ],
    3: [
        "narrateur|Amir veut un jeu, près des cordes.",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
        "maman|Tu prends quoi, pour l'attendre ?",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Près du bac, Amir prend le ballon.",
            "narrateur|Le cuir est lisse, un peu tiède.",
            "enfant-m|Il va l'appeler, le ballon !",
            "narrateur|Le ballon roule vers le chat, vif.",
            "narrateur|Le chat s'aplatit, les oreilles basses.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Il ne veut pas le ballon.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir lève le pied, pour courir.",
            "narrateur|Il le repose, sans foncer.",
            "enfant-m|Pas trop vite.",
            "papa|Regarde le ballon, vois.",
            "narrateur|Un anneau de pollen y colle, orange.",
            "maman|Il mène vers la porte, pas vers toi.",
            "narrateur|Le ballon s'arrête, loin des pattes.",
        ],
        (1, 2): [
            "narrateur|Près du bac, Amir soulève le seau.",
            "narrateur|L'anse est froide, un peu rêche.",
            "enfant-m|Je lui verse un nid de sable !",
            "narrateur|Il penche le seau, trop près.",
            "narrateur|Le chat recule, le nez plissé.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Le seau ne lui plaît pas.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir veut courir, puis s'arrête.",
            "enfant-m|J'attends.",
            "maman|Regarde le seau, au fond.",
            "narrateur|Un anneau de pollen y dort, orange.",
            "papa|Il mène vers la porte, pas ici.",
            "narrateur|Du sable fin reste au fond du seau.",
            "narrateur|Amir pose le seau, sans verser.",
        ],
        (1, 3): [
            "narrateur|Près du bac, Amir serre le doudou.",
            "narrateur|L'oreille grise est molle, un peu froide.",
            "enfant-m|C'est un lit, pour lui !",
            "narrateur|Il tend le doudou, trop près.",
            "narrateur|Le chat recule, le dos rond.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Il ne veut pas mon doudou.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir ouvre la bouche, puis se tait.",
            "enfant-m|Je reste là.",
            "papa|Regarde l'oreille, vois.",
            "narrateur|Un anneau de pollen y brille, orange.",
            "maman|Il mène vers la porte, pas vers toi.",
            "narrateur|Un peu de sable colle à l'oreille.",
            "narrateur|Amir pose le doudou, sans forcer.",
        ],
        (2, 1): [
            "narrateur|Près des marches, Amir prend le ballon.",
            "narrateur|Le cuir est un peu froid, lisse.",
            "enfant-m|Il glisse, et le chat vient !",
            "narrateur|Le ballon dévale, toc, trop loin.",
            "narrateur|Le chat bondit, loin du métal.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Le ballon l'a fait peur.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir gravit une marche, puis s'arrête.",
            "enfant-m|Pas trop vite.",
            "maman|Regarde le ballon, au bas.",
            "narrateur|Un anneau de pollen y colle, orange.",
            "papa|Il mène vers la porte, pas ici.",
            "narrateur|Une feuille jaune colle au cuir.",
            "narrateur|Amir rattrape le ballon, sans courir.",
        ],
        (2, 2): [
            "narrateur|Près des marches, Amir tient le seau.",
            "narrateur|L'anse sonne, contre le métal, cling.",
            "enfant-m|C'est un casque, pour glisser !",
            "narrateur|Il veut le poser sur le chat.",
            "narrateur|Le chat recule, les oreilles basses.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Le seau n'est pas pour lui.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir baisse le seau, sans foncer.",
            "enfant-m|J'attends.",
            "papa|Regarde le seau, vois.",
            "narrateur|Un anneau de pollen y dort, orange.",
            "maman|Il mène vers la porte, pas ici.",
            "narrateur|Amir pose le seau au bas des marches.",
            "narrateur|Le métal se tait, un instant.",
        ],
        (2, 3): [
            "narrateur|Près des marches, Amir pose le doudou.",
            "narrateur|L'oreille molle dépasse, sur le métal.",
            "enfant-m|Il glisse, lui aussi !",
            "narrateur|Il pousse le doudou, trop vite.",
            "narrateur|Le chat fuit le tissu qui tombe.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Mon doudou l'a fait peur.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir reste au bas, les pieds lourds.",
            "enfant-m|Je reste là.",
            "maman|Regarde l'oreille, vois.",
            "narrateur|Un anneau de pollen y brille, orange.",
            "papa|Il mène vers la porte, pas ici.",
            "narrateur|Amir reprend le doudou, sans glisser.",
            "narrateur|Une feuille reste collée au gris.",
        ],
        (3, 1): [
            "narrateur|Près des cordes, Amir pousse le ballon.",
            "narrateur|Le cuir tape le bois, ding.",
            "enfant-m|Pousse-moi, et le chat aussi !",
            "narrateur|Le ballon roule sous le siège, vif.",
            "narrateur|Le chat s'aplatit, loin de la corde.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Il ne veut pas le ballon.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir lève la corde, puis la lâche.",
            "enfant-m|Pas trop vite.",
            "papa|Regarde le ballon, vois.",
            "narrateur|Un anneau de pollen y colle, orange.",
            "maman|Il mène vers la porte, pas ici.",
            "narrateur|Un brin d'herbe colle au ballon.",
            "narrateur|Amir pose le ballon, loin des cordes.",
        ],
        (3, 2): [
            "narrateur|Près des cordes, Amir pose le seau.",
            "narrateur|L'anse est froide, sur le siège.",
            "enfant-m|Le chat s'assoit, dans le seau !",
            "narrateur|Il soulève le seau, trop près.",
            "narrateur|Le chat fuit le bois qui balance.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Le seau n'est pas un siège.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir pose le seau au pied de bois.",
            "enfant-m|J'attends.",
            "maman|Regarde le seau, vois.",
            "narrateur|Un anneau de pollen y dort, orange.",
            "papa|Il mène vers la porte, pas ici.",
            "narrateur|Le seau pose son ombre, ronde.",
            "narrateur|La corde se tait, un instant.",
        ],
        (3, 3): [
            "narrateur|Près des cordes, Amir installe le doudou.",
            "narrateur|L'oreille grise pend, près du bois.",
            "enfant-m|Il se balance, et il reste !",
            "narrateur|Il tend le doudou vers le chat.",
            "narrateur|Le chat recule, le dos rond.",
            "narrateur|Puis il tourne la tête, vers la porte.",
            "enfant-m|Il ne veut pas mon doudou.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Amir serre le doudou, puis le pose.",
            "enfant-m|Je reste là.",
            "papa|Regarde l'oreille, vois.",
            "narrateur|Un anneau de pollen y brille, orange.",
            "maman|Il mène vers la porte, pas ici.",
            "narrateur|L'oreille grise pend, loin du chat.",
            "narrateur|Amir pose le doudou, loin du bois.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Le chat quitte le ballon, vers la porte.",
        "narrateur|Le manteau.",
        "narrateur|Les chaussures.",
        "narrateur|Ou le sac.",
        "papa|Tu reprends quoi, Amir ?",
    ],
    2: [
        "narrateur|Le chat quitte le seau, vers la porte.",
        "narrateur|Le manteau.",
        "narrateur|Les chaussures.",
        "narrateur|Ou le sac.",
        "maman|Tu reprends quoi, Amir ?",
    ],
    3: [
        "narrateur|Le chat quitte le doudou, vers la porte.",
        "narrateur|Le manteau.",
        "narrateur|Les chaussures.",
        "narrateur|Ou le sac.",
        "papa|Tu reprends quoi, Amir ?",
    ],
}

T3_DETAIL = {
    (1, 1, 1): "Un grain de sable roule sur la manche.",
    (1, 1, 2): "Un grain de sable se loge dans le lacet.",
    (1, 1, 3): "Un grain de sable brille sur la sangle.",
    (1, 2, 1): "L'anse du seau a touché le col.",
    (1, 2, 2): "Du sable fin reste dans une chaussure.",
    (1, 2, 3): "Le seau penche, près du sac ouvert.",
    (1, 3, 1): "L'oreille du doudou frotte la manche.",
    (1, 3, 2): "Le doudou gris sent le cuir, tout près.",
    (1, 3, 3): "Le doudou glisse dans le sac, puis sort.",
    (2, 1, 1): "Une feuille de rampe colle au manteau.",
    (2, 1, 2): "Le métal a laissé le lacet froid.",
    (2, 1, 3): "Le sac a glissé d'une marche, toc.",
    (2, 2, 1): "Une goutte du seau mouille le col.",
    (2, 2, 2): "L'eau du seau brille dans une chaussure.",
    (2, 2, 3): "Le seau cale le sac, au bas.",
    (2, 3, 1): "Le doudou a une feuille, sur le manteau.",
    (2, 3, 2): "L'oreille molle dépasse d'une chaussure.",
    (2, 3, 3): "Le doudou tient le sac, près du métal.",
    (3, 1, 1): "Un brin de corde s'accroche au manteau.",
    (3, 1, 2): "La corde a frotté le lacet, rêche.",
    (3, 1, 3): "Le sac balance, puis s'arrête.",
    (3, 2, 1): "L'anse du seau sonne, contre le col.",
    (3, 2, 2): "Le seau pose son ombre sur les chaussures.",
    (3, 2, 3): "Le seau tient le sac, au pied de bois.",
    (3, 3, 1): "L'oreille du doudou pend, près du col.",
    (3, 3, 2): "Le doudou chauffe une chaussure, un peu.",
    (3, 3, 3): "Le doudou veille à l'ouverture du sac.",
}

AFF_SCENE = {
    1: {
        "see": "Le manteau bleu y dort, à l'envers.",
        "grab": "Je l'attrape, avec le manteau !",
        "cue": "Le manteau, vois, sous l'anneau.",
        "ring": "Un anneau de pollen brille, sur la manche.",
        "take": "Il reprend le manteau, deux mains.",
        "use": "Il plie le manteau, comme un nid.",
    },
    2: {
        "see": "Les chaussures brunes y sentent la maison.",
        "grab": "Je l'attrape, avec les chaussures !",
        "cue": "Les chaussures, vois, sous l'anneau.",
        "ring": "Un anneau de pollen brille, sur le lacet.",
        "take": "Il reprend les chaussures, deux mains.",
        "use": "Il pose les chaussures, près du bois.",
    },
    3: {
        "see": "Le sac beige y bâille, un peu ouvert.",
        "grab": "Je l'attrape, avec le sac !",
        "cue": "Le sac, vois, sous l'anneau.",
        "ring": "Un anneau de pollen brille, sur la sangle.",
        "take": "Il reprend le sac, deux mains.",
        "use": "Il ouvre le sac, comme une grotte.",
    },
}

TOY_LEFT = {
    1: "Voilà le ballon, resté derrière.",
    2: "Voilà le seau, resté derrière.",
    3: "Voilà le doudou, resté derrière.",
}

LOC_DOOR = {
    1: "Le chat file vers la chaise, près du bac.",
    2: "Le chat file vers la chaise, près des marches.",
    3: "Le chat file vers la chaise, près des cordes.",
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    aff = AFF_SCENE[c]
    adult_cue = "papa" if c != 2 else "maman"
    adult_wait = "maman" if c != 2 else "papa"
    return [
        f"narrateur|{LOC_DOOR[a]}",
        f"narrateur|{aff['see']}",
        f"narrateur|{TOY_LEFT[b]}",
        f"enfant-m|{aff['grab']}",
        "narrateur|Une patte passe la haie, presque.",
        "narrateur|Amir serre les poings, puis les ouvre.",
        "enfant-m|Je ne fonce pas.",
        f"{adult_cue}|{aff['cue']}",
        f"narrateur|{aff['ring']}",
        "enfant-m|C'est le même, du verre !",
        f"narrateur|{aff['take']}",
        "narrateur|Il pose le coussin sur le rebord chaud.",
        f"narrateur|{aff['use']}",
        f"narrateur|{T3_DETAIL[(a, b, c)]}",
        "narrateur|Le chat hésite, un long moment.",
        "narrateur|Puis il revient, pas à pas.",
        "narrateur|Il s'assoit, et l'anneau touche le tissu.",
        f"{adult_wait}|Tu as attendu, Amir.",
        "enfant-m|Il est là.",
    ]


END_FIRST = {
    (1, 1, 1): "Le rebord chaud porte le chat, enfin.",
    (1, 1, 2): "Voilà le chat, près des chaussures brunes.",
    (1, 1, 3): "Contre le sac, le chat se fait petit.",
    (1, 2, 1): "Au chaud, le chat a choisi le nid.",
    (1, 2, 2): "Près du seau, le chat ferme un œil.",
    (1, 2, 3): "Sous le rabat, un museau gris paraît.",
    (1, 3, 1): "Le doudou veille, le chat est au nid.",
    (1, 3, 2): "L'oreille grise pend, près des souliers.",
    (1, 3, 3): "Dans le sac, le chat se tait.",
    (2, 1, 1): "Après le métal, le rebord est doux.",
    (2, 1, 2): "Au bas des marches, le chat s'installe.",
    (2, 1, 3): "Le sac beige tient un secret gris.",
    (2, 2, 1): "Le seau sonne, loin du nid bleu.",
    (2, 2, 2): "Une goutte sèche, près du cuir brun.",
    (2, 2, 3): "Le seau cale le sac, le chat dedans.",
    (2, 3, 1): "Le doudou a vu le manteau, puis le chat.",
    (2, 3, 2): "L'oreille molle touche un lacet, puis se tait.",
    (2, 3, 3): "Près du métal, le sac garde le chat.",
    (3, 1, 1): "La corde se tait, le chat est rentré.",
    (3, 1, 2): "Un cling lointain, et les chaussures, et lui.",
    (3, 1, 3): "Le sac beige a cessé de balancer.",
    (3, 2, 1): "L'anse froide a laissé le nid tranquille.",
    (3, 2, 2): "Le seau pose son ombre, loin des pattes.",
    (3, 2, 3): "Au pied de bois, le sac tient le chat.",
    (3, 3, 1): "L'oreille grise veille, près du col bleu.",
    (3, 3, 2): "Le doudou chauffe, les chaussures aussi.",
    (3, 3, 3): "Trois tissus, et le chat au milieu.",
}

END_LAST = {
    (1, 1, 1): "L'anneau de pollen dort sur la manche.",
    (1, 1, 2): "L'anneau de pollen dore le lacet, minuscule.",
    (1, 1, 3): "L'anneau de pollen brille sur la sangle.",
    (1, 2, 1): "Un cercle orange reste au col, secret.",
    (1, 2, 2): "Un cercle orange dort dans le cuir.",
    (1, 2, 3): "Un cercle orange veille sur le rabat.",
    (1, 3, 1): "Voilà le pollen, parti du verre à la manche.",
    (1, 3, 2): "Voilà le pollen, parti du verre au lacet.",
    (1, 3, 3): "Voilà le pollen, parti du verre au sac.",
    (2, 1, 1): "L'anneau orange a glissé du métal au tissu.",
    (2, 1, 2): "L'anneau orange a glissé du métal au lacet.",
    (2, 1, 3): "L'anneau orange a glissé du métal au sac.",
    (2, 2, 1): "Une poussière orange sèche au col, fine.",
    (2, 2, 2): "Une poussière orange sèche au cuir, fine.",
    (2, 2, 3): "Une poussière orange sèche au rabat, fine.",
    (2, 3, 1): "Voici le verre nu, le manteau garde l'anneau.",
    (2, 3, 2): "Voici le verre nu, le lacet garde l'anneau.",
    (2, 3, 3): "Voici le verre nu, le sac garde l'anneau.",
    (3, 1, 1): "Un tic lointain, puis l'anneau sur le bleu.",
    (3, 1, 2): "Un tic lointain, puis l'anneau sur le lacet.",
    (3, 1, 3): "Un tic lointain, puis l'anneau sur le beige.",
    (3, 2, 1): "La corde se tait, l'anneau reste au col.",
    (3, 2, 2): "La corde se tait, l'anneau reste au cuir.",
    (3, 2, 3): "La corde se tait, l'anneau reste au rabat.",
    (3, 3, 1): "Sur le nid, l'anneau reste, tout net.",
    (3, 3, 2): "Près des souliers, l'anneau reste, tout net.",
    (3, 3, 3): "Près du sac, l'anneau reste, tout net.",
}

END_TRACE = {
    (1, 1, 1): "Le coussin rayé a un grain de sable.",
    (1, 1, 2): "Le coussin rayé a un grain, et un lacet.",
    (1, 1, 3): "Le coussin rayé a un grain, près du rabat.",
    (1, 2, 1): "Le coussin rayé sent le seau, et le col.",
    (1, 2, 2): "Le coussin rayé sent le seau, et le cuir.",
    (1, 2, 3): "Le coussin rayé sent le seau, et le sac.",
    (1, 3, 1): "Le coussin rayé a l'oreille grise, collée.",
    (1, 3, 2): "Le coussin rayé a l'oreille, près du cuir.",
    (1, 3, 3): "Le coussin rayé a l'oreille, près du sac.",
    (2, 1, 1): "Le coussin rayé a une feuille de rampe.",
    (2, 1, 2): "Le coussin rayé a une feuille, et le lacet.",
    (2, 1, 3): "Le coussin rayé a une feuille, près du sac.",
    (2, 2, 1): "Le coussin rayé a une goutte, au col.",
    (2, 2, 2): "Le coussin rayé a une goutte, au cuir.",
    (2, 2, 3): "Le coussin rayé a une goutte, au rabat.",
    (2, 3, 1): "Le coussin rayé a le doudou, et le bleu.",
    (2, 3, 2): "Le coussin rayé a le doudou, et le brun.",
    (2, 3, 3): "Le coussin rayé a le doudou, et le beige.",
    (3, 1, 1): "Le coussin rayé a un brin de corde.",
    (3, 1, 2): "Le coussin rayé a un brin, près du lacet.",
    (3, 1, 3): "Le coussin rayé a un brin, près du sac.",
    (3, 2, 1): "Le coussin rayé a l'ombre du seau, ronde.",
    (3, 2, 2): "Le coussin rayé a l'ombre du seau, au cuir.",
    (3, 2, 3): "Le coussin rayé a l'ombre du seau, au rabat.",
    (3, 3, 1): "Le coussin rayé a l'oreille, près du nid.",
    (3, 3, 2): "Le coussin rayé a l'oreille, près des souliers.",
    (3, 3, 3): "Le coussin rayé a l'oreille, près du sac.",
}

END_CHILD = {
    1: "enfant-m|Il est venu, presque pas.",
    2: "enfant-m|J'ai attendu, et il est venu.",
    3: "enfant-m|Le tic s'est tu, papa.",
}

END_ADULT = {
    1: "maman|Le jardin des trois coins se tait.",
    2: "papa|Le métal se tait, lui aussi.",
    3: "maman|La corde se tait, maintenant.",
}

END_AFF = {
    1: "narrateur|Le manteau bleu fait nid, sous lui.",
    2: "narrateur|Les chaussures brunes veillent, près de lui.",
    3: "narrateur|Le sac beige fait grotte, autour de lui.",
}

END_TOY = {
    1: "narrateur|Le ballon dort, loin des pattes.",
    2: "narrateur|Le seau dort, loin des pattes.",
    3: "narrateur|Le doudou dort, loin des pattes.",
}

END_GO = {
    1: "papa|On rentre, le manteau avec nous.",
    2: "maman|On rentre, les chaussures avec nous.",
    3: "papa|On rentre, le sac avec nous.",
}


def ending_lines(a: int, b: int, c: int) -> list[str]:
    return [
        f"narrateur|{END_FIRST[(a, b, c)]}",
        f"narrateur|{END_TRACE[(a, b, c)]}",
        END_CHILD[c],
        END_ADULT[a],
        END_AFF[c],
        END_TOY[b],
        END_GO[c],
        "enfant-m|Le chat aussi, sur le rebord.",
        "narrateur|Amir pose une main, loin de l'anneau de pollen.",
        "narrateur|Sa poitrine se desserre, fière, calme.",
        f"narrateur|{END_LAST[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=l_anneau_a_quitté_le_verre; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "chat,vitre,coussin")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "le bac à sable",
            "option_2_label": "le toboggan",
            "option_3_label": "les balançoires",
        }},
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            LOC[a]["sons"],
            {"emphasis": LOC[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": "coussin", "fields": Q_FIELDS},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            LOC[a]["sons"],
            {"emphasis": "coussin rayé"},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "le ballon",
                "option_2_label": "le seau",
                "option_3_label": "le doudou",
            }},
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                OBJ[b]["sons"],
                {"emphasis": OBJ[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le manteau",
                    "option_2_label": "les chaussures",
                    "option_3_label": "le sac",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    AFF[c]["sons"],
                    {"emphasis": "anneau de pollen"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "chat,vitre",
                    {"emphasis": "anneau de pollen", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    chunks = [out_chunks[c["chunk_id"]] for c in src["chunks"]]

    ends = [ch["text"] for ch in chunks if ch["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    lasts = []
    for ch in chunks:
        if ch["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in ch["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3_only = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage"
        and "T0003_P000" in ch["chunk_id"]
        and "_F0001" not in ch["chunk_id"]
        and not ch["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    t2_only = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage"
        and "_T0002_P000" in ch["chunk_id"]
        and "T0003" not in ch["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    t1_only = [next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P000{i}") for i in (1, 2, 3)]
    if len(set(t1_only)) < 3:
        raise SystemExit("T1 ne change pas l'histoire")

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment: {blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit("Amir absent")
    if "anneau de pollen" not in blob:
        raise SystemExit("anneau de pollen absent")
    if "coussin rayé" not in blob:
        raise SystemExit("coussin rayé absent")
    for tic in ("tout doux", "tout calme", "aujourd'hui,", "j'ai compris", "mission accomplie"):
        if tic in blob:
            raise SystemExit(f"tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"tic corpus {TICS.search(blob).group(0)}")
    for bad in (
        "merle", "couleur de miel", "tom ", "léa", "sami", "grand-père",
        "maîtresse", "jardinier", "zoé", "lina", "iris",
        "marque fine", "ombre-flèche", "ancre minuscule", "étoile brune",
    ):
        if bad in blob:
            raise SystemExit(f"interdit {bad}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Près de la fenêtre, un tic cherche son maître. Un coussin rayé "
        "dort sur le rebord chaud. Un anneau de pollen orange, collé côté "
        "maison, marque le verre. Amir veut rejoindre le chat avant qu'il "
        "parte : il ouvre trop vite, le chat saute. Au jardin des trois "
        "coins (bac, toboggan, balançoires), il jette le coussin : patatras. "
        "Il le reprend, sans courir. Ballon, seau ou doudou n'appellent pas "
        "le chat, qui file vers la porte. Amir refuse de foncer. Manteau, "
        "chaussures ou sac portent le même anneau. Il pose un nid sur le "
        "rebord. Le chat revient, presque pas. L'anneau quitte le verre."
    )
    merged["title"] = TITLE
    merged["characters"] = "Amir, papa, maman"
    merged["setting"] = "près de la fenêtre, petit jardin, rebord chaud"
    merged["chunks"] = chunks
    check(SID, merged["age_band"], merged["chunks"])

    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    print(f"chemins {min(counts)}-{max(counts)} moy {sum(counts)//len(counts)}")
    if min(counts) < 550 or max(counts) > 700:
        for a in (1, 2, 3):
            for b in (1, 2, 3):
                for c in (1, 2, 3):
                    n = sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
                    if n < 550 or n > 700:
                        print(f"  {a}{b}{c}: {n}")
        raise SystemExit(f"chemin hors barre 550-700: min {min(counts)} max {max(counts)}")

    folder = ROOT / SID
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    moy = sum(counts) // len(counts)
    nwords = sum(words(c["text"]) for c in chunks)
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types "
        "et labels T1/T2/T3 inchangés. Pas d'audio. Pas d'apply. Pas de git.\n\n"
        "## Promesse narrative\n\n"
        "Près de la fenêtre, un tic minuscule cherche son maître. Un coussin "
        "rayé (poc) dort sur le rebord chaud. Un **anneau de pollen** orange, "
        "collé côté maison, marque le verre : indice unique, payé au climax. "
        "Amir veut rejoindre le chat avant qu'il parte. Il ouvre trop vite : "
        "le chat saute, le sourire disparaît. Au jardin des trois coins "
        "(bac, toboggan, balançoires — coins, pas jouets qu'on enlève), "
        "il jette le coussin. Première idée ratée. Il **reprend** le coussin, "
        "sans courir. Ballon, seau ou doudou n'appellent pas le chat, qui "
        "file vers la porte. Seconde ruse. Amir refuse de foncer. Manteau, "
        "chaussures ou sac portent le même anneau. Il pose un nid sur le "
        "rebord. Le chat revient — le dénouement a failli ne pas arriver. "
        "AUT.AFF.003 vécue (reprendre ses affaires), jamais dite.\n\n"
        "## Améliorations appliquées\n\n"
        "- Ouverture par le son (tic) puis l'objet, pas le gabarit v2.\n"
        "- Indice unique : anneau de pollen (pas marque fine / ombre-flèche / tache).\n"
        "- Corps : sourire qui part, poitrine, adulte accroupi.\n"
        "- Deuxième imprévu plus rusé ; l'enfant refuse de foncer.\n"
        "- 27 fins et 27 dernières images distinctes.\n"
        "- T1 ne retire pas l'équipement. Un seul enfant (Amir).\n"
        "- Un merci (bac) et un bravo vécu (toboggan), pas un refrain.\n"
        "- Pas de « encore / déjà / tout doux », pas merle, pas miel.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc. "
        "`slow` réservé aux choix, à l'indice et aux fins.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(counts)} à {max(counts)} mots, moyenne {moy}\n"
        f"- {nwords} mots au total (tous nœuds)\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N1 ≤ 10 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Question liée à la scène "
        "(reprendre). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(
        f"OK {SID} {nwords} mots  fins={len(set(ends))}  "
        f"chemins {min(counts)}-{max(counts)} moy {moy}  "
        f"1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}"
    )


if __name__ == "__main__":
    build()
