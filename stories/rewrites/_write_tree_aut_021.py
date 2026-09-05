#!/usr/bin/env python3
"""TREE-AUT-021 — Le grain de sable dans la sangle (F-NAR-019, N2, AUT.AFF.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-021"
N2 = LIMITS["N2"]
TITLE = "Le grain de sable dans la sangle"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
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
    "sac bleu",
    "sac jaune",
    "ancre",
    "étoile brune",
    "fil pâle",
    "bouton nacre",
    "bouton de nacre",
    "nœud de raphia",
    "nœud raphia",
    "anneau de pollen",
    "dent de laitue",
    "écaille d'étain",
    "écaille de lichen",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="écaille de nacre",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le_grain_pique_elle_veut_l_eau; "
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
            "destinataire=enfant; sous_texte=le_sac_vient_avec_toi; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sac",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=elle_reprend_le_sac_sans_secouer; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="sac",
        note=(
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=le_grain_reste_le_sac_pèse; "
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
            "destinataire=enfant; sous_texte=elle_pose_le_sac_trop_vite; "
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
            "intensite=2; destinataire=enfant; sous_texte=le_jouet_file_elle_refuse_de_foncer; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="écaille de nacre",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_glisse_le_jouet_sans_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="écaille de nacre",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_grain_et_l_ecaille_paient_le_debut; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

COIN = {
    1: dict(lab="le bac à sable", short="bac", sons="sable,mer"),
    2: dict(lab="le toboggan", short="toboggan", sons="metal,mer"),
    3: dict(lab="les balançoires", short="balançoires", sons="corde,mer"),
}
TOY = {
    1: dict(lab="le ballon", le="le ballon", un="un ballon", short="ballon", sons="ballon,mer"),
    2: dict(lab="le seau", le="le seau", un="le seau", short="seau", sons="seau,mer"),
    3: dict(lab="le doudou", le="le doudou", un="le doudou", short="doudou", sons="doudou,mer"),
}
LIEU = {
    1: dict(lab="le banc", ou="vers le banc", short="banc", sons="banc,vague"),
    2: dict(lab="la cabine", ou="vers la cabine", short="cabine", sons="porte,bois"),
    3: dict(lab="les galets", ou="vers les galets", short="galets", sons="galets,mer"),
}

Q_FIELDS = {
    1: {
        "expected_answer": "sac",
        "accepted_examples": "sac | le sac | son sac | le sac roux | elle le prend | je le prends",
        "retry_prompt": "Le sac roux. Mila prend quoi ?",
        "engine_ok_text": "Oui, le sac.",
        "engine_near_text": "Tu es près. Écoute l'indice.",
    },
    2: {
        "expected_answer": "sac",
        "accepted_examples": "sac | le sac | son sac | le sac roux | elle le prend | je le prends",
        "retry_prompt": "Le sac roux. Mila prend quoi ?",
        "engine_ok_text": "Oui, le sac.",
        "engine_near_text": "Tu es près. Écoute l'indice.",
    },
    3: {
        "expected_answer": "sac",
        "accepted_examples": "sac | le sac | son sac | le sac roux | elle le prend | je le prends",
        "retry_prompt": "Le sac roux. Mila prend quoi ?",
        "engine_ok_text": "Oui, le sac.",
        "engine_near_text": "Tu es près. Écoute l'indice.",
    },
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
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


# Ouverture : le vent de l'eau entre. Indice = écaille de nacre. Objet = grain.
OPENING = [
    "narrateur|Le vent de l'eau pousse la porte, un peu.",
    "narrateur|La chaise de paille répond, craque.",
    "narrateur|La paille sent le sel, et le soleil.",
    "narrateur|Mila vit ici, avec papa et maman.",
    "narrateur|Un détail paraît, sur la sangle du sac.",
    "narrateur|Une écaille de nacre y tient, minuscule.",
    "narrateur|Elle est lisse, un peu rose.",
    "narrateur|À côté, un grain de sable pique.",
    "narrateur|Les sandales de papa sèchent, près du bois.",
    "narrateur|Ça sent la pêche, toute mûre.",
    "narrateur|Dehors, un bateau fait rum rum, loin.",
    "maman|Mila, tu as vu l'eau ?",
    "enfant-f|Je veux l'eau, tout de suite !",
    "narrateur|En ce moment, Mila tire la sangle.",
    "narrateur|Le sac roux glisse, trop vite.",
    "narrateur|Le grain pique sa paume.",
    "enfant-f|Aïe, ça glisse !",
    "narrateur|Le sourire de Mila disparaît.",
    "narrateur|Elle secoue la sangle, trop fort.",
    "narrateur|Le grain vacille, presque tombé.",
    "papa|Tu veux garder le grain, Mila ?",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "enfant-f|Oui, il est à moi !",
    "maman|Le sac vient avec nous.",
]

T1_CHOICE = [
    "narrateur|Près de l'eau, trois coins attendent.",
    "papa|Le bac à sable, le toboggan, ou les balançoires ?",
    "maman|On emporte le sac roux.",
    "maman|Tu choisis quel coin, Mila ?",
]

T1 = {
    1: [
        "narrateur|Mila court vers le bac à sable.",
        "narrateur|Le sable est frais, un peu collant.",
        "narrateur|Ça fait chh sous la paume.",
        "enfant-f|Un château, tout de suite !",
        "narrateur|Elle pose le sac roux, trop vite.",
        "narrateur|Le grain pique, contre sa hanche.",
        "enfant-f|Aïe, la sangle !",
        "narrateur|Le sac tombe sur le côté, mou.",
        "narrateur|Le sourire de Mila disparaît.",
        "narrateur|Dans sa poitrine, envie et peur se bousculent.",
        "narrateur|Papa s'accroupit, à sa hauteur.",
        "papa|Le sac est là, près du bois.",
        "narrateur|Mila reprend la sangle, sans secouer.",
        "narrateur|L'écaille de nacre y tient, minuscule.",
        "enfant-f|Le grain est là, papa.",
        "maman|Il voyage avec toi ?",
    ],
    2: [
        "narrateur|Mila grimpe vers le toboggan.",
        "narrateur|Le métal est tiède sous la paume.",
        "enfant-f|Je glisse, sans le sac !",
        "narrateur|Elle laisse le sac au bas, trop vite.",
        "narrateur|La sangle penche, le grain pique.",
        "enfant-f|Il va tomber !",
        "narrateur|Le sac bascule, vers le sable.",
        "narrateur|Le sourire de Mila disparaît.",
        "narrateur|Ses épaules baissent, au haut des marches.",
        "narrateur|Maman s'accroupit, en bas.",
        "maman|Le sac t'attend, au bas.",
        "narrateur|Mila redescend, sans foncer.",
        "narrateur|Elle reprend la sangle, deux mains.",
        "narrateur|L'écaille de nacre y brille, minuscule.",
        "enfant-f|Le grain est là, maman.",
        "papa|Il voyage avec toi ?",
    ],
    3: [
        "narrateur|Mila court vers les balançoires.",
        "narrateur|La corde est rêche, un peu tiède.",
        "enfant-f|Je pousse, les mains libres !",
        "narrateur|Elle accroche le sac à la corde.",
        "narrateur|Le siège part, la sangle glisse.",
        "enfant-f|Mon sac !",
        "narrateur|Le sac tombe, près du bois.",
        "narrateur|Le sourire de Mila disparaît.",
        "narrateur|L'envie de courir lui pique les doigts.",
        "narrateur|Papa s'accroupit, près de la corde.",
        "papa|Le sac est là, sur le sable.",
        "narrateur|Mila reprend la sangle, sans tirer.",
        "narrateur|L'écaille de nacre y tient, minuscule.",
        "enfant-f|Le grain est là, papa.",
        "maman|Il voyage avec toi ?",
    ],
}

T1_Q = {
    1: [
        "narrateur|La sangle pique, contre le bac.",
        "maman|Mila prend quoi, pour l'eau ?",
    ],
    2: [
        "narrateur|La sangle pique, au bas du toboggan.",
        "papa|Mila prend quoi, pour l'eau ?",
    ],
    3: [
        "narrateur|La sangle pique, près de la corde.",
        "maman|Mila prend quoi, pour l'eau ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Mila serre le sac roux, contre elle.",
        "enfant-f|Je le prends, il vient.",
        "maman|Merci, Mila.",
        "papa|Tu le portes, sans secouer ?",
        "enfant-f|Oui, le grain reste.",
        "narrateur|L'écaille de nacre veille, sur la sangle.",
        "narrateur|Le grain de sable tient, coincé.",
        "narrateur|Un peu de sable frais reste au fond.",
    ],
    2: [
        "narrateur|Mila serre le sac roux, contre elle.",
        "enfant-f|Je le prends, il vient.",
        "papa|Merci, Mila.",
        "maman|Tu le portes, sans glisser ?",
        "enfant-f|Oui, le grain reste.",
        "narrateur|L'écaille de nacre veille, sur la sangle.",
        "narrateur|Le grain de sable tient, coincé.",
        "narrateur|Le métal se tait, un instant.",
    ],
    3: [
        "narrateur|Mila serre le sac roux, contre elle.",
        "enfant-f|Je le prends, il vient.",
        "maman|Merci, Mila.",
        "papa|Tu le portes, sans balancer ?",
        "enfant-f|Oui, le grain reste.",
        "narrateur|L'écaille de nacre veille, sur la sangle.",
        "narrateur|Le grain de sable tient, coincé.",
        "narrateur|La corde retombe, sans bruit.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Mila veut un jeu, près du bac.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le sac roux vient avec toi.",
    ],
    2: [
        "narrateur|Mila veut un jeu, près des marches.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Le sac roux vient avec toi.",
    ],
    3: [
        "narrateur|Mila veut un jeu, près des cordes.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le sac roux vient avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    return {
        (1, 1): [
            "narrateur|Près du bac, Mila sort le ballon.",
            "narrateur|Le cuir est lisse, un peu tiède.",
            "enfant-f|Il roule vers l'eau, avec moi !",
            "narrateur|Elle le pousse, trop vite.",
            "narrateur|Le ballon part, vers une vague.",
            "enfant-f|Reviens !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Elle lève le pied, pour courir.",
            "narrateur|Elle le repose, sans foncer.",
            "enfant-f|Pas trop vite.",
            "papa|Regarde le ballon, vois.",
            "narrateur|Une écaille de nacre y colle, minuscule.",
            "maman|Personne ne dit où courir.",
            "narrateur|Mila rattrape le ballon, sans crier.",
        ],
        (1, 2): [
            "narrateur|Près du bac, Mila soulève le seau.",
            "narrateur|L'anse est froide, un peu rêche.",
            "enfant-f|Je verse un château, tout de suite !",
            "narrateur|Elle penche le seau, trop près de l'eau.",
            "narrateur|Le sable fuit, vers la vague.",
            "enfant-f|Mon château part !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Ses épaules baissent, près du bois.",
            "narrateur|Elle veut courir, puis s'arrête.",
            "enfant-f|J'attends.",
            "maman|Regarde le seau, au fond.",
            "narrateur|Une écaille de nacre y dort, minuscule.",
            "papa|Personne ne donne la réponse.",
            "narrateur|Mila pose le seau, sans verser.",
            "narrateur|Du sable fin reste au fond.",
        ],
        (1, 3): [
            "narrateur|Près du bac, Mila sort le doudou.",
            "narrateur|L'oreille grise est molle, un peu froide.",
            "enfant-f|Il s'assoit dans le sable !",
            "narrateur|Elle pose le doudou, trop près de l'eau.",
            "narrateur|Une vague lèche l'oreille grise.",
            "enfant-f|Il va partir !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Elle ouvre la bouche, puis se tait.",
            "enfant-f|Je reste là.",
            "papa|Regarde l'oreille, vois.",
            "narrateur|Une écaille de nacre y brille, minuscule.",
            "maman|Personne ne dit de foncer.",
            "narrateur|Mila reprend le doudou, sans crier.",
            "narrateur|Un peu de sable colle à l'oreille.",
        ],
        (2, 1): [
            "narrateur|Près des marches, Mila prend le ballon.",
            "narrateur|Le cuir est un peu froid, lisse.",
            "enfant-f|Il glisse avec moi !",
            "narrateur|Elle le pose sur la rampe, trop vite.",
            "narrateur|Le ballon dévale, toc, vers l'eau.",
            "enfant-f|Il file !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Elle gravit une marche, puis s'arrête.",
            "enfant-f|Pas trop vite.",
            "maman|Regarde le ballon, au bas.",
            "narrateur|Une écaille de nacre y colle, minuscule.",
            "papa|Personne ne dit où courir.",
            "narrateur|Mila rattrape le ballon, sans glisser.",
            "narrateur|Une feuille de sel colle au cuir.",
        ],
        (2, 2): [
            "narrateur|Près des marches, Mila tient le seau.",
            "narrateur|L'anse sonne, contre le métal, cling.",
            "enfant-f|C'est un bateau, pour glisser !",
            "narrateur|Elle pose le seau sur la rampe.",
            "narrateur|Le seau part, trop loin, vers l'eau.",
            "enfant-f|Mon seau !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Ses épaules baissent, au bas.",
            "narrateur|Elle baisse les mains, sans foncer.",
            "enfant-f|J'attends.",
            "papa|Regarde le seau, vois.",
            "narrateur|Une écaille de nacre y dort, minuscule.",
            "maman|Personne ne donne la réponse.",
            "narrateur|Mila reprend le seau, au bas des marches.",
            "narrateur|Le métal se tait, un instant.",
        ],
        (2, 3): [
            "narrateur|Près des marches, Mila pose le doudou.",
            "narrateur|L'oreille molle dépasse, sur le métal.",
            "enfant-f|Il glisse, lui aussi !",
            "narrateur|Elle pousse le doudou, trop vite.",
            "narrateur|Le tissu dévale, vers le sable mouillé.",
            "enfant-f|Mon doudou part !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|L'envie de courir lui pique les doigts.",
            "narrateur|Elle reste au bas, les pieds lourds.",
            "enfant-f|Je reste là.",
            "maman|Regarde l'oreille, vois.",
            "narrateur|Une écaille de nacre y brille, minuscule.",
            "papa|Personne ne dit de foncer.",
            "narrateur|Mila reprend le doudou, sans glisser.",
            "narrateur|Une feuille reste collée au gris.",
        ],
        (3, 1): [
            "narrateur|Près des cordes, Mila pousse le ballon.",
            "narrateur|Le cuir tape le bois, ding.",
            "enfant-f|Pousse-moi, et le ballon aussi !",
            "narrateur|Le ballon roule sous le siège, vif.",
            "narrateur|Il part vers l'eau, trop loin.",
            "enfant-f|Il ne veut pas rester.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Envie et inquiétude se bousculent, dedans.",
            "narrateur|Elle lève la corde, puis la lâche.",
            "enfant-f|Pas trop vite.",
            "papa|Regarde le ballon, vois.",
            "narrateur|Une écaille de nacre y colle, minuscule.",
            "maman|Personne ne dit où courir.",
            "narrateur|Mila pose le ballon, loin des cordes.",
            "narrateur|Un brin d'herbe colle au ballon.",
        ],
        (3, 2): [
            "narrateur|Près des cordes, Mila pose le seau.",
            "narrateur|L'anse est froide, sur le siège.",
            "enfant-f|Le seau s'assoit, avec moi !",
            "narrateur|Elle soulève le seau, trop près de l'eau.",
            "narrateur|Le siège balance, le seau penche.",
            "enfant-f|Il verse !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Ses épaules baissent, près du bois.",
            "narrateur|Elle pose le seau au pied de bois.",
            "enfant-f|J'attends.",
            "maman|Regarde le seau, vois.",
            "narrateur|Une écaille de nacre y dort, minuscule.",
            "papa|Personne ne donne la réponse.",
            "narrateur|Le seau pose son ombre, ronde.",
            "narrateur|La corde se tait, un instant.",
        ],
        (3, 3): [
            "narrateur|Près des cordes, Mila installe le doudou.",
            "narrateur|L'oreille grise pend, près du bois.",
            "enfant-f|Il se balance, et il reste !",
            "narrateur|Elle tend le doudou vers le siège.",
            "narrateur|Le tissu glisse, vers le sable mouillé.",
            "enfant-f|Il ne veut pas mon siège.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Elle serre le doudou, puis le pose.",
            "enfant-f|Je reste là.",
            "papa|Regarde l'oreille, vois.",
            "narrateur|Une écaille de nacre y brille, minuscule.",
            "maman|Personne ne dit de foncer.",
            "narrateur|L'oreille grise pend, loin de l'eau.",
            "narrateur|Mila pose le doudou, loin du bois.",
        ],
    }[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Le ballon veut rouler, plus loin.",
        "papa|On va où, avec le sac ?",
        "maman|Le banc, la cabine, ou les galets ?",
    ],
    2: [
        "narrateur|Le seau penche, trop lourd.",
        "maman|On va où, avec le sac ?",
        "papa|Le banc, la cabine, ou les galets ?",
    ],
    3: [
        "narrateur|Le doudou a du sable, partout.",
        "papa|On va où, avec le sac ?",
        "maman|Le banc, la cabine, ou les galets ?",
    ],
}

ARRIVE = {
    (1, 1): "narrateur|Du bac, Mila gagne le banc d'écume.",
    (1, 2): "narrateur|Du bac, Mila gagne la cabine de bois.",
    (1, 3): "narrateur|Du bac, Mila gagne les galets ronds.",
    (2, 1): "narrateur|Du toboggan, Mila gagne le banc d'écume.",
    (2, 2): "narrateur|Du toboggan, Mila gagne la cabine de bois.",
    (2, 3): "narrateur|Du toboggan, Mila gagne les galets ronds.",
    (3, 1): "narrateur|Des cordes, Mila gagne le banc d'écume.",
    (3, 2): "narrateur|Des cordes, Mila gagne la cabine de bois.",
    (3, 3): "narrateur|Des cordes, Mila gagne les galets ronds.",
}

FAUX = {
    1: "narrateur|L'écume blanche ment, une seconde.",
    2: "narrateur|Un crochet luisant ment, une seconde.",
    3: "narrateur|Un galet mouillé ment, une seconde.",
}

PLACE = {
    1: "narrateur|Une vague lèche le bois du banc.",
    2: "narrateur|La porte de la cabine sent le sel.",
    3: "narrateur|Les galets font clic, sous le pied.",
}

ALMOST = {
    (1, 1, 1): "narrateur|Le ballon a failli rouler sous le banc.",
    (1, 1, 2): "narrateur|Le ballon a failli rester près du crochet.",
    (1, 1, 3): "narrateur|Le ballon a failli sauter vers l'eau.",
    (1, 2, 1): "narrateur|Le seau a failli verser sous le bois.",
    (1, 2, 2): "narrateur|Le seau a failli coincer la porte.",
    (1, 2, 3): "narrateur|Le seau a failli se coincer aux galets.",
    (1, 3, 1): "narrateur|Le doudou a failli glisser sous le banc.",
    (1, 3, 2): "narrateur|Le doudou a failli rester sur le crochet.",
    (1, 3, 3): "narrateur|Le doudou a failli dormir entre les galets.",
    (2, 1, 1): "narrateur|Après le métal, le ballon a failli fuir.",
    (2, 1, 2): "narrateur|Après le métal, le ballon a failli rouler.",
    (2, 1, 3): "narrateur|Après le métal, le ballon a failli sauter.",
    (2, 2, 1): "narrateur|Après le métal, le seau a failli verser.",
    (2, 2, 2): "narrateur|Après le métal, le seau a failli coincer.",
    (2, 2, 3): "narrateur|Après le métal, le seau a failli se coincer.",
    (2, 3, 1): "narrateur|Après le métal, le doudou a failli glisser.",
    (2, 3, 2): "narrateur|Après le métal, le doudou a failli rester.",
    (2, 3, 3): "narrateur|Après le métal, le doudou a failli dormir.",
    (3, 1, 1): "narrateur|Après la corde, le ballon a failli fuir.",
    (3, 1, 2): "narrateur|Après la corde, le ballon a failli rouler.",
    (3, 1, 3): "narrateur|Après la corde, le ballon a failli sauter.",
    (3, 2, 1): "narrateur|Après la corde, le seau a failli verser.",
    (3, 2, 2): "narrateur|Après la corde, le seau a failli coincer.",
    (3, 2, 3): "narrateur|Après la corde, le seau a failli se coincer.",
    (3, 3, 1): "narrateur|Après la corde, le doudou a failli glisser.",
    (3, 3, 2): "narrateur|Après la corde, le doudou a failli rester.",
    (3, 3, 3): "narrateur|Après la corde, le doudou a failli dormir.",
}

TRACE = {
    (1, 1, 1): "narrateur|Un grain rouge colle au bois du banc.",
    (1, 1, 2): "narrateur|Un grain rouge colle au bois de la porte.",
    (1, 1, 3): "narrateur|Un grain rouge colle à un galet plat.",
    (1, 2, 1): "narrateur|L'anse a laissé un rond, sous le banc.",
    (1, 2, 2): "narrateur|L'anse a laissé un rond, sur la porte.",
    (1, 2, 3): "narrateur|L'anse a laissé un rond, sur un galet.",
    (1, 3, 1): "narrateur|L'oreille grise a un fil, sous le banc.",
    (1, 3, 2): "narrateur|L'oreille grise a un fil, près du crochet.",
    (1, 3, 3): "narrateur|L'oreille grise a un fil, entre les galets.",
    (2, 1, 1): "narrateur|Une feuille de rampe sèche au banc.",
    (2, 1, 2): "narrateur|Une feuille de rampe sèche à la porte.",
    (2, 1, 3): "narrateur|Une feuille de rampe sèche sur un galet.",
    (2, 2, 1): "narrateur|Un cling lointain reste sous le banc.",
    (2, 2, 2): "narrateur|Un cling lointain reste près du crochet.",
    (2, 2, 3): "narrateur|Un cling lointain reste entre les galets.",
    (2, 3, 1): "narrateur|Une feuille grise sèche sous le banc.",
    (2, 3, 2): "narrateur|Une feuille grise sèche près du crochet.",
    (2, 3, 3): "narrateur|Une feuille grise sèche entre les galets.",
    (3, 1, 1): "narrateur|Un brin de corde s'accroche au banc.",
    (3, 1, 2): "narrateur|Un brin de corde s'accroche à la porte.",
    (3, 1, 3): "narrateur|Un brin de corde s'accroche à un galet.",
    (3, 2, 1): "narrateur|L'ombre du seau s'endort sous le banc.",
    (3, 2, 2): "narrateur|L'ombre du seau s'endort près du crochet.",
    (3, 2, 3): "narrateur|L'ombre du seau s'endort entre les galets.",
    (3, 3, 1): "narrateur|L'oreille veille, sous le bois du banc.",
    (3, 3, 2): "narrateur|L'oreille veille, près du crochet de bois.",
    (3, 3, 3): "narrateur|L'oreille veille, entre deux galets ronds.",
}

GESTURE = {
    1: "narrateur|Elle glisse le ballon, au fond du sac.",
    2: "narrateur|Elle glisse le seau, au fond du sac.",
    3: "narrateur|Elle glisse le doudou, au fond du sac.",
}

WANT = {
    1: "enfant-f|Je joue, les mains libres !",
    2: "enfant-f|Je verse, les mains libres !",
    3: "enfant-f|Il s'assoit, les mains libres !",
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    adult_cue = "papa" if c != 2 else "maman"
    adult_wait = "maman" if c != 2 else "papa"
    listen = {
        1: "narrateur|Elle écoute le bois du banc, puis la sangle.",
        2: "narrateur|Elle écoute la porte, puis la sangle.",
        3: "narrateur|Elle écoute les galets, puis la sangle.",
    }[c]
    cue = {
        1: f"{adult_cue}|Tu secoues, ou tu regardes ?",
        2: f"{adult_cue}|Tu forces, ou tu regardes ?",
        3: f"{adult_cue}|Tu vois l'écaille, où ?",
    }[c]
    body = {
        1: "narrateur|Dans sa poitrine, ça serre, fort.",
        2: "narrateur|Ses épaules baissent, un peu.",
        3: "narrateur|L'envie de secouer lui pique les doigts.",
    }[c]
    return [
        ARRIVE[(a, c)],
        PLACE[c],
        f"narrateur|Mila tient {TOY[b]['le']}, et le sac roux.",
        WANT[b],
        "narrateur|Elle veut poser le sac, trop vite.",
        FAUX[c],
        "enfant-f|C'est l'écaille ?",
        "narrateur|Le sourire de Mila disparaît.",
        body,
        f"{adult_cue}|Personne ne donne la réponse.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Papa s'accroupit, à sa hauteur." if c != 2 else "narrateur|Maman s'accroupit, à sa hauteur.",
        cue,
        listen,
        "narrateur|L'écaille de nacre reparaît, sur la sangle.",
        "enfant-f|C'est la vraie, du début !",
        "narrateur|Mila ouvre le sac, sans secouer.",
        GESTURE[b],
        "narrateur|Le grain de sable reste, dans la sangle.",
        f"{adult_wait}|Tu l'as glissé, sans forcer.",
        ALMOST[(a, b, c)],
        TRACE[(a, b, c)],
    ]


END_FIRST = {
    (1, 1, 1): "La chaise de paille attend, dans la maison.",
    (1, 1, 2): "La paille de la chaise sent le sel, un peu.",
    (1, 1, 3): "Près de la porte, les sandales de papa sèchent.",
    (1, 2, 1): "Une goutte de pêche sèche, sur le bois.",
    (1, 2, 2): "Le bateau se tait, loin de la fenêtre.",
    (1, 2, 3): "Le vent de l'eau pousse moins, à présent.",
    (1, 3, 1): "La chaise craque moins, sous le sac roux.",
    (1, 3, 2): "Un quartier de pêche attend, sur la table.",
    (1, 3, 3): "Le carrelage est froid, sous les pieds de Mila.",
    (2, 1, 1): "Après le métal, la paille paraît douce.",
    (2, 1, 2): "Après le métal, la maison sent la pêche.",
    (2, 1, 3): "Après le métal, le vent se tait, un peu.",
    (2, 2, 1): "Le cling du seau reste loin, dehors.",
    (2, 2, 2): "La rampe se tait, loin de la chaise.",
    (2, 2, 3): "Un pas sur le carrelage, puis plus.",
    (2, 3, 1): "L'oreille grise dépasse du sac, au chaud.",
    (2, 3, 2): "Le doudou a vu le métal, depuis la paille.",
    (2, 3, 3): "Un rayon a bougé, sur la chaise de paille.",
    (3, 1, 1): "La corde se tait, loin de la maison.",
    (3, 1, 2): "Un ding lointain, puis la paille, puis rien.",
    (3, 1, 3): "Le sac roux a cessé de balancer.",
    (3, 2, 1): "L'anse froide a laissé le tissu tranquille.",
    (3, 2, 2): "Le seau pose son ombre, loin des pieds.",
    (3, 2, 3): "Au pied de la chaise, le sac tient bon.",
    (3, 3, 1): "L'oreille grise veille, près de la paille.",
    (3, 3, 2): "Le doudou chauffe, la sangle aussi.",
    (3, 3, 3): "Trois tissus, et le grain au milieu.",
}

END_LAST = {
    (1, 1, 1): "Sur le bois de la chaise, un grain rouge sèche.",
    (1, 1, 2): "Dans l'ombre de la cabine, rien ne bouge plus.",
    (1, 1, 3): "Entre deux galets, un fil de sangle s'endort.",
    (1, 2, 1): "L'anse du seau a laissé un rond, au tissu.",
    (1, 2, 2): "Sur la porte, un rond d'eau sèche, minuscule.",
    (1, 2, 3): "Un galet plat garde un rond d'anse, secret.",
    (1, 3, 1): "Sous le banc, un fil gris s'endort.",
    (1, 3, 2): "Près du crochet, un fil gris s'endort.",
    (1, 3, 3): "Entre les galets, un fil gris s'endort.",
    (2, 1, 1): "Une feuille de rampe s'endort au tissu roux.",
    (2, 1, 2): "Une feuille de rampe s'endort près des clés.",
    (2, 1, 3): "Une feuille de rampe s'endort sur un galet.",
    (2, 2, 1): "Loin du cling, la paille se tait.",
    (2, 2, 2): "Loin du métal, la porte de bois se tait.",
    (2, 2, 3): "Loin du métal, les galets se taisent.",
    (2, 3, 1): "Près de la paille, une feuille grise veille.",
    (2, 3, 2): "Dans le sac, un peu de métal froid.",
    (2, 3, 3): "Sur la paille, le rayon a bougé.",
    (3, 1, 1): "Près de la chaise, un brin de corde s'endort.",
    (3, 1, 2): "Loin de l'écaille, la corde se tait.",
    (3, 1, 3): "Un galet garde un brin de corde, unique.",
    (3, 2, 1): "Sur la paille, l'ombre du seau dort.",
    (3, 2, 2): "Près du banc, le seau a laissé son rond.",
    (3, 2, 3): "Dans les galets, une ombre ronde se tait.",
    (3, 3, 1): "Au chaud, l'oreille sent la paille.",
    (3, 3, 2): "Dans le sac, une écaille de nacre se tait.",
    (3, 3, 3): "À la chaise, le bois ne craque plus.",
}

END_ANS = {
    (1, 1, 1): "enfant-f|Quand le ballon a failli filer, sous le banc.",
    (1, 1, 2): "enfant-f|Quand le crochet a menti, une seconde.",
    (1, 1, 3): "enfant-f|Quand le galet a menti, une seconde.",
    (1, 2, 1): "enfant-f|Quand le seau a failli verser, sous le bois.",
    (1, 2, 2): "enfant-f|Quand j'ai ouvert, sans secouer.",
    (1, 2, 3): "enfant-f|Quand le seau s'est coincé, presque.",
    (1, 3, 1): "enfant-f|Quand le doudou a glissé, sous le banc.",
    (1, 3, 2): "enfant-f|Quand le doudou a voulu le crochet.",
    (1, 3, 3): "enfant-f|Quand le doudou a voulu les galets.",
    (2, 1, 1): "enfant-f|Quand le ballon a dévalé, trop vite.",
    (2, 1, 2): "enfant-f|Quand l'écume n'était pas l'écaille.",
    (2, 1, 3): "enfant-f|Quand le ballon a voulu l'eau.",
    (2, 2, 1): "enfant-f|Quand le seau a sonné, trop fort.",
    (2, 2, 2): "enfant-f|Quand le crochet a menti, une seconde.",
    (2, 2, 3): "enfant-f|Quand le seau a voulu glisser.",
    (2, 3, 1): "enfant-f|Quand le doudou a dévalé, trop vite.",
    (2, 3, 2): "enfant-f|Quand j'ai regardé la sangle, d'abord.",
    (2, 3, 3): "enfant-f|Quand l'oreille a touché le sel.",
    (3, 1, 1): "enfant-f|Quand le ballon a roulé sous le siège.",
    (3, 1, 2): "enfant-f|Quand la corde a voulu garder le sac.",
    (3, 1, 3): "enfant-f|Quand le ballon a tapé le bois.",
    (3, 2, 1): "enfant-f|Quand le seau a penché, sur le siège.",
    (3, 2, 2): "enfant-f|Quand j'ai attendu, près de la porte.",
    (3, 2, 3): "enfant-f|Quand l'ombre du seau a menti.",
    (3, 3, 1): "enfant-f|Quand le doudou a glissé du siège.",
    (3, 3, 2): "enfant-f|Quand le doudou a voulu rester.",
    (3, 3, 3): "enfant-f|Quand j'ai glissé sans secouer.",
}

END_Q = {
    1: "papa|Quel moment tu gardes, Mila ?",
    2: "maman|Quel moment tu gardes, Mila ?",
    3: "papa|Quel moment tu gardes, près des galets ?",
}


def ending_lines(a: int, b: int, c: int) -> list[str]:
    return [
        f"narrateur|{END_FIRST[(a, b, c)]}",
        "narrateur|Mila pose le sac roux, sur la chaise.",
        "narrateur|Le grain de sable reste, dans la sangle.",
        "narrateur|L'écaille de nacre y tient, minuscule.",
        END_Q[c],
        END_ANS[(a, b, c)],
        "enfant-f|Surtout celui-là.",
        f"narrateur|{TOY[b]['le'].capitalize()} reste au fond, avec une trace.",
        f"narrateur|{END_LAST[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{COIN[a]['short']}_{TOY[b]['short']}_{LIEU[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "mer,sac,chaise")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "mer",
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
            COIN[a]["sons"],
            {"emphasis": "écaille de nacre"},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": "sac", "fields": Q_FIELDS[a]},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            COIN[a]["sons"],
            {"emphasis": "sac"},
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
                TOY[b]["sons"],
                {"emphasis": "écaille de nacre"},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le banc",
                    "option_2_label": "la cabine",
                    "option_3_label": "les galets",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    LIEU[c]["sons"],
                    {"emphasis": "écaille de nacre"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "chaise,sac,mer",
                    {"emphasis": "écaille de nacre", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = [out_chunks[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    lasts = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in out_chunks[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    t2_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "_T0002_P000" in c["chunk_id"] and "T0003" not in c["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    blob = "\n".join(c["script"] for c in out_chunks.values()).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment x{blob.count('en ce moment')}")
    if "écaille de nacre" not in out_chunks["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    if "grain de sable" not in out_chunks["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("objet-titre absent de l'ouverture")
    for c in src["chunks"]:
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"] and not c["chunk_id"].endswith("T0003_P0000"):
            if "écaille de nacre" not in out_chunks[c["chunk_id"]]["text"].lower():
                raise SystemExit(f"indice non payé: {c['chunk_id']}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Le vent de l'eau pousse la porte : la chaise de paille craque. "
        "Sur la sangle du sac roux, une écaille de nacre tient, lisse, "
        "un peu rose. À côté, un grain de sable pique. Mila veut l'eau "
        "tout de suite. Elle tire trop vite : le grain pique, le sac "
        "glisse, elle secoue trop fort. Le grain vacille. Papa "
        "s'accroupit. Bac, toboggan ou balançoires : le sac vient. "
        "Ballon, seau ou doudou : à la main ça file vers l'eau ; dans "
        "le sac, ça tient. Banc, cabine ou galets : l'écume, le crochet "
        "ou le galet mentent, l'écaille dit vrai. Elle refuse de foncer. "
        "Elle glisse sans secouer. L'écaille paie le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Mila, papa, maman"
    merged["setting"] = "maison près de la mer, chaise de paille, puis le bord de l'eau"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    if min(counts) < 550 or max(counts) > 700:
        raise SystemExit(f"chemin hors barre 550-700: min {min(counts)} max {max(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types "
        "de blocs et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le vent de l'eau pousse la porte : la chaise de paille craque. "
        "Sur la sangle du sac roux, une écaille de nacre tient, lisse, "
        "un peu rose. À côté, un grain de sable pique. Mila veut l'eau "
        "tout de suite. Elle tire trop vite : le grain pique, le sac "
        "glisse, elle secoue trop fort. Le grain vacille. Papa "
        "s'accroupit. Bac, toboggan ou balançoires : le sac vient. "
        "Ballon, seau ou doudou : à la main ça file vers l'eau ; dans "
        "le sac, ça tient. Banc, cabine ou galets : un faux éclat ment, "
        "l'écaille dit vrai. Elle refuse de foncer. Elle glisse sans "
        "secouer. L'écaille et le grain paient le début. Le sac garde "
        "une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison près de la mer, chaise de paille, bord de l'eau.\n"
        "- Désir : porter le sac roux jusqu'à l'eau, garder le grain.\n"
        "- Objet : grain de sable dans la sangle, plus ballon / seau / doudou.\n"
        "- Indice unique : l'écaille de nacre, vue dès l'ouverture, payée au climax.\n"
        "- Urgence douce : Mila veut l'eau tout de suite.\n"
        "- Imprévu 1 : le grain pique, le sac glisse, elle secoue trop fort.\n"
        "- Cue : le sac est là. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : écume / crochet / galet mentent ; l'écaille dit vrai.\n"
        "- Revers allongé : coincé, corps (envie et peur), refus de foncer, geste neuf.\n"
        "- Résolution : ouvrir sans secouer, glisser le jouet dans le sac.\n"
        "- Retour : écaille de nacre, grain dans la sangle, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (le vent de l'eau pousse la porte), pas un gabarit v2.\n"
        "- Pas « Le sac bleu attend », pas « sandales encore mouillées ».\n"
        "- Le premier choix n'enlève pas le sac : il vient aux trois coins.\n"
        "- Revers allongé : coincé, corps, refus, second arrêt, geste lent.\n"
        "- Neuf T2 distincts, vingt-sept T3, vingt-sept fins.\n"
        "- Leçon AUT.AFF.001 vécue (glisser dans le sac, garder le grain), jamais dite.\n"
        "- Monde ≠ TREE-AUT-009 sac bleu salon, ≠ TREE-AUT-046 sac jaune laitue.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Mila, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience de Mila au départ, petit découragement quand le sac "
        "glisse ou le jouet file, fierté calme quand elle glisse sans "
        "secouer. L'adulte guide peu. `slow` réservé aux choix, à la "
        "question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N2 ≤ 15 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
