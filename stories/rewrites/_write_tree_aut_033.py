#!/usr/bin/env python3
"""TREE-AUT-033 — La gouttière du kiosque et le manteau bleu (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-033"
N1 = 10
TITLE = "La gouttière du kiosque et le manteau bleu"
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
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="virgule de zinc",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=la_virgule_pointe_le_bouton; "
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
            "destinataire=enfant; sous_texte=ton_choix_change_la_chasse_aux_gouttes; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="seau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=il_reprend_ce_qui_compte; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="virgule",
        note=(
            "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; "
            "destinataire=enfant; sous_texte=le_seau_revient_la_virgule_reste; "
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
            "destinataire=enfant; sous_texte=il_veut_les_gouttes_trop_vite; "
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
            "intensite=2; destinataire=enfant; sous_texte=la_flaque_ment_la_virgule_dit_vrai; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="virgule de zinc",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=il_soulève_sans_tirer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="virgule",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_ploc_et_la_virgule_ont_tenu_promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | le seau | le manteau",
    "retry_prompt": "Il reprend le seau. Nino fait quoi ?",
}

LOC = {
    1: dict(name="le bac à sable", short="bac", sons="sable,seau"),
    2: dict(name="le toboggan", short="toboggan", sons="metal,glisse"),
    3: dict(name="les balançoires", short="balançoires", sons="chaine,vent"),
}
OBJ = {
    1: dict(name="le ballon", short="ballon", sons="ballon,rebond"),
    2: dict(name="le seau", short="seau", sons="seau,anse"),
    3: dict(name="le doudou", short="doudou", sons="tissu,doudou"),
}
LIEU = {
    1: dict(name="le filet", short="filet", sons="filet,maille"),
    2: dict(name="la fontaine", short="fontaine", sons="eau,fontaine"),
    3: dict(name="la grille", short="grille", sons="grille,metal"),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = ph.lower()
        if TICS.search(low):
            raise SystemExit(f"tic: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
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


# Ouverture : papa frotte, le zinc répond. Indice unique = virgule de zinc.
OPENING = [
    "narrateur|Papa frotte le banc, goutte par goutte.",
    "narrateur|Le bois reste mouillé, têtu.",
    "narrateur|Un manteau bleu sèche dessus.",
    "narrateur|Le zinc du kiosque répond, ploc.",
    "narrateur|Une virgule de zinc pend, sans tomber.",
    "narrateur|Elle pointe le bouton du manteau.",
    "narrateur|Maman ouvre le sac de pain.",
    "narrateur|Ça sent la croûte chaude, vive.",
    "narrateur|Un seau jaune attend sous le banc.",
    "narrateur|L'anse est rêche, un peu froide.",
    "narrateur|En ce moment, Nino saisit l'anse.",
    "enfant-m|Les gouttes, dans le seau, vite !",
    "narrateur|Il lève le seau sous le zinc.",
    "narrateur|L'anse glisse, trop mouillée.",
    "narrateur|Le seau tape le banc, toc.",
    "narrateur|Le manteau prend une éclaboussure.",
    "narrateur|La virgule saute sur le bouton.",
    "narrateur|Le seau roule sous le bois.",
    "narrateur|Le sourire de Nino disparaît.",
    "enfant-m|Il ne veut pas rester !",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Regarde la virgule, sur le bouton.",
    "maman|Tu veux les gouttes, comment ?",
]

T1_CHOICE = [
    "narrateur|Le parc a trois coins, près du kiosque.",
    "papa|Le bac à sable, le toboggan, ou les balançoires ?",
    "maman|Le seau vient avec toi.",
]

T1 = {
    1: [
        "narrateur|Nino prend le seau, deux mains.",
        "narrateur|L'anse rêche tape, contre lui.",
        "narrateur|Le manteau bleu reste sur le banc.",
        "narrateur|Le bac à sable sent l'eau froide.",
        "enfant-m|Je verse, je fais une rivière !",
        "narrateur|Il penche le seau, trop vite.",
        "narrateur|Le sable boit tout, d'un coup.",
        "narrateur|L'anse s'enfonce, collée, lourde.",
        "enfant-m|Il est trop lourd, maintenant.",
        "narrateur|Il tire, et le sable vole.",
        "enfant-m|Je n'y arrive pas.",
        "papa|La virgule, vois, sur le bouton.",
        "maman|Le manteau t'attend, sur le banc.",
        "narrateur|Ses mains s'arrêtent, collées de grains.",
    ],
    2: [
        "narrateur|Nino serre le seau contre lui.",
        "narrateur|Le plastique frotte, un petit bruit rêche.",
        "narrateur|Au toboggan, le métal est froid.",
        "narrateur|Les marches font toc, sous les pieds.",
        "enfant-m|Je le mets sur la rampe !",
        "narrateur|Il pose le seau sur le métal.",
        "narrateur|Le seau glisse, d'un coup, loin.",
        "narrateur|Un tas jaune s'étale au bas.",
        "enfant-m|Il est parti tout seul !",
        "papa|Il a glissé, trop vite.",
        "enfant-m|Je n'y arrive pas.",
        "maman|La virgule, vois, sur le bouton.",
        "narrateur|Ses épaules baissent, au bas.",
        "papa|Tu le reprends, avec le manteau ?",
    ],
    3: [
        "narrateur|Nino porte le seau vers les cordes.",
        "narrateur|La chaîne est rêche, un peu froide.",
        "narrateur|Le siège de bois balance, vide.",
        "enfant-m|Il se balance avec moi !",
        "narrateur|Il accroche l'anse à la chaîne.",
        "narrateur|Une poussée, et le seau part.",
        "narrateur|L'eau s'échappe, autour des pieds.",
        "enfant-m|Il s'envole, je ne peux pas.",
        "papa|La chaîne tient l'anse, vois.",
        "maman|Le manteau est sur le banc mouillé.",
        "narrateur|Ses mains lâchent, un peu.",
        "enfant-m|Je n'y arrive pas.",
        "narrateur|Une virgule tremble sur le bouton.",
        "papa|Tu le reprends, avant de rentrer ?",
    ],
}

T1_Q = {
    1: [
        "narrateur|Le seau est collé dans le bac.",
        "papa|Nino, tu fais quoi ?",
    ],
    2: [
        "narrateur|Le seau est au bas du toboggan.",
        "maman|Nino, tu fais quoi ?",
    ],
    3: [
        "narrateur|Le seau est pris dans la chaîne.",
        "papa|Nino, tu fais quoi ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Nino se baisse vers le plastique.",
        "narrateur|Il secoue le sable, grain par grain.",
        "narrateur|La virgule de zinc reparaît, tiède.",
        "enfant-m|Je le reprends, il vient.",
        "maman|Merci, Nino, il est avec toi.",
        "papa|Tu le portes, pour les gouttes ?",
        "enfant-m|Oui, je le garde.",
        "narrateur|Un grain reste dans le fond.",
        "narrateur|Le manteau bleu attend, lui aussi.",
        "enfant-m|Il ne glisse plus.",
    ],
    2: [
        "narrateur|Nino descend les marches, une à une.",
        "narrateur|Il ramasse le tas jaune, au bas.",
        "narrateur|La virgule de zinc reparaît, froide.",
        "enfant-m|Je le reprends, il est froid.",
        "papa|Merci, Nino, il est avec toi.",
        "maman|Tu le portes, pour les gouttes ?",
        "enfant-m|Oui, je le serre.",
        "narrateur|Une feuille reste collée au plastique.",
        "narrateur|Le manteau reste près des pieds.",
        "enfant-m|Il ne glisse plus.",
    ],
    3: [
        "narrateur|Nino tient la chaîne, puis l'anse.",
        "narrateur|Il tourne, lent, autour du bois.",
        "narrateur|L'anse se libère, un peu froide.",
        "enfant-m|Je le reprends, il est à moi.",
        "maman|Merci, Nino, il est avec toi.",
        "papa|Tu le portes, pour les gouttes ?",
        "enfant-m|Oui, contre moi.",
        "narrateur|Un brin de chaîne reste à l'anse.",
        "narrateur|Le manteau reste au banc mouillé.",
        "enfant-m|Il ne s'envole plus.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près du bac, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le manteau reste sur le banc.",
    ],
    2: [
        "narrateur|Près du toboggan, un jeu l'appelle.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Le manteau reste sur le banc.",
    ],
    3: [
        "narrateur|Près des cordes, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le manteau reste sur le banc.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Nino pose le seau au bord du bac.",
            "narrateur|Il prend le ballon, rouge, un peu lisse.",
            "enfant-m|Il va rebondir, près de moi !",
            "narrateur|Le ballon tape le bois, puis file.",
            "narrateur|Il court, le seau reste derrière.",
            "narrateur|Au retour, une flaque jaune tient le bord.",
            "enfant-m|Il est là !",
            "narrateur|Il saisit la flaque, vide.",
            "narrateur|Sa main touche le sable, seulement.",
            "enfant-m|Il n'est plus là.",
            "narrateur|Le sourire de Nino disparaît.",
            "papa|Regarde la virgule, pas la flaque.",
            "narrateur|La virgule brille sur le bouton.",
            "maman|Elle mène vers le kiosque, plus loin.",
            "enfant-m|Je ne fonce pas.",
        ],
        (1, 2): [
            "narrateur|Nino pose le manteau près du seau.",
            "narrateur|Il creuse, l'anse froide dans la paume.",
            "enfant-m|Je fais un puits, trop grand !",
            "narrateur|Le seau pèse, plein de sable mouillé.",
            "narrateur|La manche glisse dans le trou, lente.",
            "narrateur|Il tire l'anse, trop occupé.",
            "narrateur|Au bord, une forme bleue reste, plate.",
            "enfant-m|Il est là, je le vois !",
            "narrateur|C'est l'ombre du seau, sur le bois.",
            "enfant-m|Le manteau a disparu.",
            "papa|La virgule, vois, dans le creux.",
            "narrateur|Une virgule sort du sable, mince.",
            "maman|Elle mène plus loin, vers le kiosque.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le seau sonne, vide de manteau.",
        ],
        (1, 3): [
            "narrateur|Nino pose le doudou sur le manteau.",
            "narrateur|Les deux tissus se ressemblent, de dos.",
            "enfant-m|Vous restez là, tous les deux.",
            "narrateur|Il creuse, le doudou contre la hanche.",
            "narrateur|Au retour, un dos bleu attend, flou.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le doudou, pas le manteau.",
            "narrateur|Sous le doudou, le sable est nu.",
            "enfant-m|Il s'est caché, le rusé.",
            "maman|La virgule, vois, pas le doudou.",
            "narrateur|La virgule fuit sous une planche.",
            "papa|L'ombre a menti, la virgule dit vrai.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le doudou a du sable à l'oreille.",
            "narrateur|Le bac garde un creux, sans bleu.",
        ],
        (2, 1): [
            "narrateur|Nino pose le seau sur une marche.",
            "narrateur|Il prend le ballon, près du métal.",
            "enfant-m|Il glisse, comme moi !",
            "narrateur|Le ballon dévale, vif, trop loin.",
            "narrateur|Il court au bas, sans le plastique.",
            "narrateur|En haut, une ombre jaune tient la rampe.",
            "enfant-m|Il m'attend, là-haut !",
            "narrateur|Il gravit, et l'ombre se casse.",
            "narrateur|Le métal est nu, froid, vide.",
            "enfant-m|Ce n'était pas lui.",
            "papa|La virgule, vois, sur le bouton.",
            "narrateur|La virgule descend, marche par marche.",
            "maman|Elle mène plus loin, vers le kiosque.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le ballon s'arrête, loin du jaune.",
        ],
        (2, 2): [
            "narrateur|Nino pose le manteau près des marches.",
            "narrateur|Il emplit le seau, au pied du métal.",
            "enfant-m|Je verse en haut, comme le zinc !",
            "narrateur|L'eau du seau mouille la rampe, vive.",
            "narrateur|La manche boit, puis file, lourde.",
            "narrateur|Il regarde le seau, pas le tissu.",
            "narrateur|Une tache bleue reste, plate, sur le métal.",
            "enfant-m|Il est collé, je le vois !",
            "narrateur|C'est l'eau, pas le manteau.",
            "enfant-m|Il a disparu, mouillé.",
            "maman|La virgule, vois, le long du métal.",
            "narrateur|La virgule fuit vers le kiosque.",
            "papa|L'eau a menti, la virgule dit vrai.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le seau goutte, sans manche dedans.",
        ],
        (2, 3): [
            "narrateur|Nino pose le doudou contre le manteau.",
            "narrateur|Sur la marche, les deux dos se touchent.",
            "enfant-m|Vous glissez avec moi, tous les deux.",
            "narrateur|Il monte, le doudou sous le bras.",
            "narrateur|Au bas, un dos bleu attend, flou.",
            "enfant-m|Mon manteau m'attend !",
            "narrateur|Il saisit l'air, et le doudou.",
            "narrateur|Le manteau n'est plus sur la marche.",
            "enfant-m|L'ombre a pris sa place.",
            "papa|La virgule, vois, pas le doudou.",
            "narrateur|La virgule court sous le métal.",
            "maman|Elle mène plus loin, vers le kiosque.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le doudou a une feuille, collée.",
            "narrateur|La rampe du toboggan reste nue.",
        ],
        (3, 1): [
            "narrateur|Nino pose le seau sur le siège.",
            "narrateur|Il prend le ballon, près des cordes.",
            "enfant-m|Je le lance, pendant que j'attends !",
            "narrateur|Le ballon file, et le siège part.",
            "narrateur|Il court, le plastique reste derrière.",
            "narrateur|Au retour, un dos jaune balance, vide.",
            "enfant-m|Il se balance, je le vois !",
            "narrateur|Il saisit l'ombre, sur le bois.",
            "narrateur|Le siège est nu, un peu froid.",
            "enfant-m|Ce n'était que l'ombre.",
            "maman|La virgule, vois, sur le bouton.",
            "narrateur|La virgule tremble, puis fuit.",
            "papa|L'ombre a menti, la virgule dit vrai.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le ballon roule sous les cordes.",
        ],
        (3, 2): [
            "narrateur|Nino pose le manteau au pied de bois.",
            "narrateur|Il emplit le seau, près des cordes.",
            "enfant-m|Je fais un poids, pour le siège !",
            "narrateur|Le seau pèse, et le siège part.",
            "narrateur|La manche s'accroche, puis se libère.",
            "narrateur|Il regarde le seau, trop occupé.",
            "narrateur|Une tache bleue reste, au pied.",
            "enfant-m|Il est là, contre le bois !",
            "narrateur|C'est l'ombre du seau, allongée.",
            "enfant-m|Le manteau a disparu.",
            "papa|La virgule, vois, autour de la chaîne.",
            "narrateur|La virgule fuit vers le kiosque.",
            "maman|La chaîne a menti, la virgule dit vrai.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le seau sonne, contre le pied nu.",
        ],
        (3, 3): [
            "narrateur|Nino pose le doudou sur le manteau.",
            "narrateur|Sur le siège, les deux dos se confondent.",
            "enfant-m|Vous vous balancez, tous les deux.",
            "narrateur|Il pousse, le doudou sous le bras.",
            "narrateur|Au retour, un dos bleu attend, flou.",
            "enfant-m|Mon manteau se balance !",
            "narrateur|Il saisit le doudou, trop vite.",
            "narrateur|Le siège est nu, sans manteau.",
            "enfant-m|L'ombre a pris sa place.",
            "maman|La virgule, vois, pas le doudou.",
            "narrateur|La virgule court dans l'herbe.",
            "papa|Le siège a menti, la virgule dit vrai.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le doudou sent l'herbe, un peu.",
            "narrateur|La chaîne se tait, sans anse.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|La virgule mène vers trois coins.",
        "papa|Le filet, la fontaine, ou la grille ?",
        "maman|On suit la virgule, pas la flaque.",
    ],
    2: [
        "narrateur|La virgule mène vers trois coins.",
        "maman|Le filet, la fontaine, ou la grille ?",
        "papa|On suit la virgule, pas l'eau.",
    ],
    3: [
        "narrateur|La virgule mène vers trois coins.",
        "papa|Le filet, la fontaine, ou la grille ?",
        "maman|On suit la virgule, pas le doudou.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    arrive = {
        1: [
            "narrateur|La virgule court vers le filet.",
            "narrateur|Les mailles sont mouillées, un peu froides.",
            "enfant-m|Il est pris, je le vois !",
        ],
        2: [
            "narrateur|La virgule court vers la fontaine.",
            "narrateur|L'eau chante, plus fort que le zinc.",
            "enfant-m|Il est dans le bac, je le vois !",
        ],
        3: [
            "narrateur|La virgule court vers la grille.",
            "narrateur|Le fer est froid, un peu rêche.",
            "enfant-m|Le bouton est pris, je le vois !",
        ],
    }[c]
    snag = {
        1: [
            "narrateur|Il tire la manche, trop vite.",
            "narrateur|Le tissu se coince entre deux mailles.",
            "enfant-m|Il tient, dans le filet !",
        ],
        2: [
            "narrateur|Il tire l'anse, trop vite.",
            "narrateur|Le seau tape le rebord, puis glisse.",
            "enfant-m|La fontaine le garde !",
        ],
        3: [
            "narrateur|Il tire le bouton, trop vite.",
            "narrateur|L'anse s'enroule autour du fer.",
            "enfant-m|La grille le mange !",
        ],
    }[c]
    body = {
        1: [
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Envie et peur se bousculent, dans sa poitrine.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu regardes, ou tu tires ?",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute les mailles, puis le bouton.",
            "narrateur|La virgule de zinc brille, minuscule.",
        ],
        2: [
            "narrateur|Ses épaules baissent, près de l'eau.",
            "narrateur|Dans sa poitrine, ça serre, trop fort.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu forces, ou tu regardes ?",
            "enfant-m|J'attends, je regarde.",
            "narrateur|Il écoute la fontaine, puis le zinc.",
            "narrateur|La virgule de zinc clignote, minuscule.",
        ],
        3: [
            "narrateur|Nino fixe le fer, sans bouger.",
            "narrateur|L'envie de tirer lui pique les doigts.",
            "narrateur|Papa s'accroupit, près de la grille.",
            "papa|Tu vois la virgule, où ?",
            "enfant-m|Je cherche, sans tirer.",
            "narrateur|Il écarte une feuille, lente.",
            "narrateur|La virgule de zinc brille, sous le bord.",
        ],
    }[c]
    again = {
        1: "narrateur|La manche avance, puis s'arrête.",
        2: "narrateur|L'anse glisse, puis se bloque.",
        3: "narrateur|Un bouton cède, puis refuse.",
    }[c]
    helper = {
        1: {
            1: "narrateur|Il cale le ballon sous la maille.",
            2: "narrateur|Il glisse l'anse sous la maille.",
            3: "narrateur|Il glisse le doudou sous la maille.",
        },
        2: {
            1: "narrateur|Il cale le ballon contre le rebord.",
            2: "narrateur|Il glisse l'anse sous le rebord.",
            3: "narrateur|Il glisse le doudou sous le rebord.",
        },
        3: {
            1: "narrateur|Il cale le ballon sous le fer.",
            2: "narrateur|Il glisse l'anse sous le fer.",
            3: "narrateur|Il glisse le doudou sous le fer.",
        },
    }[c][b]
    gesture = {
        1: "enfant-m|Je soulève la maille, sans tirer.",
        2: "enfant-m|Je soulève le rebord, sans tirer.",
        3: "enfant-m|Je soulève le fer, sans tirer.",
    }[c]
    free = {
        1: "narrateur|La manche se libère, lente, pleine.",
        2: "narrateur|L'anse se libère, lente, froide.",
        3: "narrateur|Le bouton se libère, lent, rêche.",
    }[c]
    traces = {
        (1, 1): "narrateur|Un grain de sable reste à la virgule.",
        (1, 2): "narrateur|L'anse du seau a laissé du sable.",
        (1, 3): "narrateur|L'oreille du doudou a du sable.",
        (2, 1): "narrateur|Une feuille du toboggan reste au tissu.",
        (2, 2): "narrateur|Une goutte du seau sèche à la virgule.",
        (2, 3): "narrateur|Une feuille reste sur le doudou.",
        (3, 1): "narrateur|Un brin de chaîne reste à la virgule.",
        (3, 2): "narrateur|L'anse a senti la chaîne, froide.",
        (3, 3): "narrateur|Le doudou a l'odeur de l'herbe.",
    }[(a, b)]
    almost = {
        (1, 1, 1): "narrateur|Un grain cachait la virgule, presque.",
        (1, 1, 2): "narrateur|Le rebord serrait trop, une seconde.",
        (1, 1, 3): "narrateur|La feuille recouvrait le bouton, presque.",
        (1, 2, 1): "narrateur|Le sable buvait la manche, presque.",
        (1, 2, 2): "narrateur|L'anse tirait trop, une seconde.",
        (1, 2, 3): "narrateur|Le fer gardait le pli, presque.",
        (1, 3, 1): "narrateur|Le doudou cachait le bleu, presque.",
        (1, 3, 2): "narrateur|L'eau mordait la manche, une seconde.",
        (1, 3, 3): "narrateur|Le pli se refermait, presque.",
        (2, 1, 1): "narrateur|Une feuille couvrait le bouton, presque.",
        (2, 1, 2): "narrateur|Le métal glissait trop, une seconde.",
        (2, 1, 3): "narrateur|Le fer pliait le tissu, presque.",
        (2, 2, 1): "narrateur|L'eau mentait, une seconde de trop.",
        (2, 2, 2): "narrateur|Le seau versait trop, une seconde.",
        (2, 2, 3): "narrateur|Une goutte cachait la virgule, presque.",
        (2, 3, 1): "narrateur|L'oreille prenait la place, presque.",
        (2, 3, 2): "narrateur|Le doudou trompait l'œil, une seconde.",
        (2, 3, 3): "narrateur|La feuille collait trop, une seconde.",
        (3, 1, 1): "narrateur|La chaîne tenait l'anse, presque.",
        (3, 1, 2): "narrateur|Un cling couvrait la virgule, presque.",
        (3, 1, 3): "narrateur|L'herbe cachait le bouton, presque.",
        (3, 2, 1): "narrateur|Le seau pesait trop, une seconde.",
        (3, 2, 2): "narrateur|La chaîne mentait, une seconde de trop.",
        (3, 2, 3): "narrateur|Le pied nu manquait le fer, presque.",
        (3, 3, 1): "narrateur|Le siège mélangeait les dos, presque.",
        (3, 3, 2): "narrateur|Un dos flou prenait la place, presque.",
        (3, 3, 3): "narrateur|L'odeur égarait la main, presque.",
    }[(a, b, c)]
    obj = OBJ[b]["name"]
    leave = {
        1: "On quitte le bac, virgule en vue.",
        2: "On quitte le toboggan, virgule en vue.",
        3: "On quitte les cordes, virgule en vue.",
    }[a]
    adult = {
        1: "maman|Tu l'as, sans forcer.",
        2: "papa|Il est à toi, maintenant.",
        3: "maman|Tu l'as repris, Nino.",
    }[c]
    return (
        arrive
        + snag
        + body
        + [again, helper, gesture, free, adult]
        + [
            "narrateur|Nino serre le manteau, fier.",
            f"narrateur|{obj.capitalize()} vient aussi, près de lui.",
            f"narrateur|{leave}",
            "enfant-m|On va au kiosque, maintenant.",
            traces,
            almost,
        ]
    )


def ending_lines(a: int, b: int, c: int) -> list[str]:
    obj = OBJ[b]["name"]
    lieu = LIEU[c]["name"]
    firsts = {
        (1, 1, 1): "Le zinc du kiosque fait ploc, ploc.",
        (1, 1, 2): "Le sac de pain sent la croûte, plus fort.",
        (1, 1, 3): "L'affiche du kiosque claque, sèche.",
        (1, 2, 1): "Un grain roule sur le banc mouillé.",
        (1, 2, 2): "Le seau pose son ombre au bois.",
        (1, 2, 3): "Le sac de pain attend, ouvert.",
        (1, 3, 1): "L'oreille du doudou dépasse du banc.",
        (1, 3, 2): "Un fil du doudou pend près du sac.",
        (1, 3, 3): "Le doudou sent le sable, au bois.",
        (2, 1, 1): "Une feuille sèche sur le banc, loin.",
        (2, 1, 2): "Le métal du toboggan se tait, loin.",
        (2, 1, 3): "Un pas sur le zinc, puis plus.",
        (2, 2, 1): "Le seau penche, sous le kiosque.",
        (2, 2, 2): "Le ploc de la fontaine s'arrête.",
        (2, 2, 3): "La rampe du toboggan reste loin.",
        (2, 3, 1): "L'oreille molle dépasse du filet.",
        (2, 3, 2): "Le doudou a vu le métal, depuis le bois.",
        (2, 3, 3): "Un rayon a bougé, sur le zinc.",
        (3, 1, 1): "Le ballon s'endort près du kiosque.",
        (3, 1, 2): "La chaîne ne fait plus cling.",
        (3, 1, 3): "Le zinc du kiosque se tait.",
        (3, 2, 1): "Le seau pose son ombre sur le banc.",
        (3, 2, 2): "Le pain tiède attend, dans le sac.",
        (3, 2, 3): "Les clés de papa restent dans la poche.",
        (3, 3, 1): "Le doudou a l'odeur de l'herbe.",
        (3, 3, 2): "Une croûte rentre dans le sac.",
        (3, 3, 3): "Le kiosque retrouve son ploc, unique.",
    }
    lasts = {
        (1, 1, 1): "Un grain de sable dort sur la virgule.",
        (1, 1, 2): "La fontaine garde un fil bleu, minuscule.",
        (1, 1, 3): "Un grain reste coincé dans la grille.",
        (1, 2, 1): "L'anse du seau sèche, sous le filet.",
        (1, 2, 2): "Une miette roule près du pain tiède.",
        (1, 2, 3): "L'ombre du seau s'endort au fer.",
        (1, 3, 1): "Du sable reste dans l'oreille du doudou.",
        (1, 3, 2): "Près du pain, un fil gris pend.",
        (1, 3, 3): "Au bouton, un grain de sable brille.",
        (2, 1, 1): "Une feuille sèche, collée à la virgule.",
        (2, 1, 2): "Loin du bouton, le métal se tait.",
        (2, 1, 3): "Sur le banc, un pas s'éteint.",
        (2, 2, 1): "Sous le filet, le seau penche, vide.",
        (2, 2, 2): "Le ploc de la fontaine s'endort, loin.",
        (2, 2, 3): "Loin d'ici, la rampe reste muette.",
        (2, 3, 1): "Près du filet, une oreille molle veille.",
        (2, 3, 2): "Dans l'oreille, un peu de métal froid.",
        (2, 3, 3): "Sur le bois, le rayon a bougé.",
        (3, 1, 1): "Près du zinc, le ballon s'endort.",
        (3, 1, 2): "Loin du bouton, la chaîne se tait.",
        (3, 1, 3): "Le kiosque garde un ploc, unique.",
        (3, 2, 1): "Sur le banc, l'ombre du seau dort.",
        (3, 2, 2): "Près du sac, le pain attend.",
        (3, 2, 3): "Dans la grille, un fil bleu reste.",
        (3, 3, 1): "Au chaud, le doudou sent l'herbe.",
        (3, 3, 2): "Dans le sac, une croûte rentre.",
        (3, 3, 3): "Au bouton, la virgule de zinc se tait.",
    }
    qs = {
        1: "papa|Où s'était-il caché, dans le filet ?",
        2: "maman|Qui l'avait pris, à la fontaine ?",
        3: "papa|Qui l'avait tenu, sur la grille ?",
    }[c]
    ans = {
        1: "enfant-m|Dans les mailles, avec la virgule.",
        2: "enfant-m|Le rebord, et la virgule.",
        3: "enfant-m|La grille, tout contre le fer.",
    }[c]
    joue = {
        1: "Nino a joué au bac.",
        2: "Nino a joué au toboggan.",
        3: "Nino a joué aux cordes.",
    }[a]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|{joue}",
        f"narrateur|Il a choisi {obj}, pour le jeu.",
        f"narrateur|La virgule l'a mené vers {lieu}.",
        "narrateur|Voilà le manteau bleu, sur le banc.",
        "narrateur|Au bouton, la virgule de zinc brille.",
        "enfant-m|Il est rentré, avec sa trace.",
        qs,
        ans,
        "maman|Le pain nous attend, maintenant.",
        "enfant-m|Je croque, il est chaud.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{LOC[a]['short']}_{OBJ[b]['short']}_{LIEU[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "kiosque,zinc,pain")
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
            {"emphasis": "seau", "fields": Q_FIELDS},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            LOC[a]["sons"],
            {"emphasis": "virgule"},
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
                    "option_1_label": "le filet",
                    "option_2_label": "la fontaine",
                    "option_3_label": "la grille",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    LIEU[c]["sons"],
                    {"emphasis": "virgule de zinc"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "zinc,pain",
                    {"emphasis": "virgule", "note": ending_note(a, b, c)},
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

    merged = dict(src)
    merged["fil_rouge"] = (
        "Au parc, papa frotte le banc mouillé. Le zinc du kiosque à pain "
        "répond, ploc. Une virgule de zinc pend, pointe le bouton du manteau "
        "bleu. Nino veut les dernières gouttes dans le seau jaune, maintenant. "
        "L'anse glisse : le seau tape, la virgule saute sur le bouton. Bac, "
        "toboggan ou balançoires, la première idée rate. Il reprend le seau. "
        "Ballon, seau ou doudou : une flaque ment, la virgule dit vrai. Il "
        "refuse de foncer. Filet, fontaine ou grille, le tissu se coince, "
        "avance, s'arrête. Il soulève sans tirer. Le ploc et la virgule "
        "paient le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Nino, papa, maman"
    merged["setting"] = "parc, kiosque à pain, zinc, banc mouillé"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")
    if min(counts) < 550 or max(counts) > 700:
        raise SystemExit(f"longueur chemins hors barre: {min(counts)}-{max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-AUT-033 — La gouttière du kiosque et le manteau bleu\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, "
        "types de blocs et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Papa frotte le banc mouillé. Le zinc du kiosque répond, ploc. Une "
        "virgule de zinc pend, pointe le bouton du manteau bleu. Nino veut "
        "les dernières gouttes dans le seau jaune, avant que le kiosque se "
        "taise. Il lève trop vite : l'anse glisse, le seau tape, la virgule "
        "saute sur le bouton. Au bac, au toboggan ou aux balançoires, la "
        "première idée rate. Il reprend le seau. Ballon, seau ou doudou : une "
        "flaque ment, la virgule dit vrai. Il refuse de foncer. Filet, "
        "fontaine ou grille, le tissu se coince, avance, s'arrête. Il "
        "soulève sans tirer. Le ploc et la virgule paient le début. Le "
        "manteau garde une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc, kiosque à pain, zinc, banc mouillé, sac de croûte.\n"
        "- Désir : attraper les gouttes du zinc dans le seau, maintenant.\n"
        "- Objet : seau jaune (anse rêche) et manteau bleu (boutons ronds).\n"
        "- Indice unique : la virgule de zinc, vue dès l'ouverture, payée au climax.\n"
        "- Urgence douce : le zinc se tait, le pain attend.\n"
        "- Imprévu 1 : anse mouillée, seau qui glisse, sable qui boit.\n"
        "- Cue : la virgule, pas la force. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : la flaque ou l'ombre ment ; la virgule mène.\n"
        "- Revers allongé : coincé, corps (envie et peur), refus de foncer, "
        "manche qui avance puis s'arrête, geste neuf.\n"
        "- Résolution : soulever sans tirer, au filet, à la fontaine, à la grille.\n"
        "- Retour : pain, ploc, virgule, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (papa frotte, le zinc répond), pas un gabarit v2.\n"
        "- Le premier choix n'enlève pas le seau : il vient au jeu. Le manteau reste visible.\n"
        "- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.003 vécue (reprendre seau et manteau), jamais dite.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Nino, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience au départ, petit découragement quand le seau résiste ou "
        "disparaît, fierté calme quand Nino soulève sans tirer. L'adulte guide "
        "peu. `slow` réservé aux choix, à la question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//len(counts)}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N1 ≤ 10 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
