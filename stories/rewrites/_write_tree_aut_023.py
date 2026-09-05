#!/usr/bin/env python3
"""TREE-AUT-023 — Le manteau sur la rampe (F-NAR-019, N1, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-023"
N1 = LIMITS["N1"]
TITLE = "Le manteau sur la rampe"
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
        emphasis="croissant de cuivre",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=le_croissant_brille_vers_le_jardin; "
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
            "destinataire=enfant; sous_texte=ton_choix_change_la_recherche; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="manteau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=reprendre_le_tissu_avant_de_jouer; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; intensite=1; "
            "destinataire=enfant; sous_texte=le_manteau_revient_dans_les_bras; "
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
            "destinataire=enfant; sous_texte=elle_pose_le_manteau_trop_vite; "
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
            "intensite=2; destinataire=enfant; sous_texte=l_ombre_ment_le_croissant_dit_vrai; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="croissant de cuivre",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_soulève_sans_tirer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="croissant",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_cric_et_le_croissant_ont_tenu_promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | elle reprend | le seau | le manteau",
    "retry_prompt": "Elle reprend le seau. Chouchou fait quoi ?",
}

LOC = {
    1: dict(name="le bac à sable", short="bac", sons="sable,seau"),
    2: dict(name="le toboggan", short="toboggan", sons="metal,glisse"),
    3: dict(name="les balançoires", short="balançoires", sons="corde,bois"),
}
OBJ = {
    1: dict(name="le ballon", short="ballon", sons="ballon,rebond"),
    2: dict(name="le seau", short="seau", sons="seau,sable"),
    3: dict(name="le doudou", short="doudou", sons="tissu,doudou"),
}
LIEU = {
    1: dict(name="le banc", short="banc", sons="banc,bois"),
    2: dict(name="le portail", short="portail", sons="loquet,portail"),
    3: dict(name="le paillasson", short="paillasson", sons="paille,seuil"),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
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


# Ouverture : le manteau a choisi la rampe. Indice unique = croissant de cuivre.
OPENING = [
    "narrateur|Le bois de la rampe garde une chaleur.",
    "narrateur|Un manteau rouge a choisi sa place.",
    "narrateur|Le couloir sent les fraises du panier.",
    "narrateur|L'escalier de bois fait cric, cric.",
    "narrateur|Au col, un croissant de cuivre brille.",
    "narrateur|Il est tourné vers le jardin, ouvert.",
    "narrateur|Le chat passe sous la manche, sans bruit.",
    "papa|Les fraises attendent, après le jardin.",
    "maman|Le soleil quitte la rampe, vois.",
    "narrateur|En ce moment, Chouchou saisit le tissu.",
    "enfant-f|Je le porte au crochet, vite !",
    "narrateur|Elle tire, et la manche accroche.",
    "narrateur|Le croissant racle le bois, minuscule.",
    "narrateur|Elle tire plus fort, trop vite.",
    "narrateur|Le sourire de Chouchou disparaît.",
    "enfant-f|Il ne veut pas venir !",
    "narrateur|Ses épaules baissent, près du bois.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Regarde le croissant, sur le col.",
    "maman|Où le portes-tu, d'abord ?",
]

T1_CHOICE = [
    "narrateur|Le jardin a trois coins pour jouer.",
    "papa|Le bac à sable, le toboggan, ou les balançoires ?",
    "maman|Le manteau vient avec toi.",
]

T1 = {
    1: [
        "narrateur|Chouchou prend le manteau, deux mains.",
        "narrateur|Le croissant de cuivre tape, contre elle.",
        "narrateur|La porte du jardin racle, un peu.",
        "narrateur|Le bac à sable sent l'eau froide.",
        "enfant-f|Je le pose, je creuse !",
        "narrateur|Elle jette le manteau sur le bord.",
        "narrateur|Le tissu glisse dans le sable, lourd.",
        "narrateur|La manche se remplit de grains, froids.",
        "enfant-f|Il est trop lourd, maintenant.",
        "narrateur|Elle tire, et le sable vole.",
        "enfant-f|Je n'y arrive pas.",
        "papa|Le croissant, vois, sur le bois.",
        "maman|Le seau t'attend, près du bac.",
        "narrateur|Ses mains s'arrêtent, collées de grains.",
    ],
    2: [
        "narrateur|Chouchou serre le manteau contre elle.",
        "narrateur|Le tissu frotte, un petit bruit rêche.",
        "narrateur|Au toboggan, le métal est tiède.",
        "narrateur|Les marches font toc, sous les pieds.",
        "enfant-f|Je le mets sur la rampe !",
        "narrateur|Elle accroche la manche au métal.",
        "narrateur|Le manteau glisse, d'un coup, loin.",
        "narrateur|Un tas rouge s'étale au bas.",
        "enfant-f|Il est parti tout seul !",
        "papa|Il a glissé, trop vite.",
        "enfant-f|Je n'y arrive pas.",
        "maman|Le croissant, vois, sur le métal.",
        "narrateur|Ses épaules baissent, au bas.",
        "papa|Tu le reprends, avec le seau ?",
    ],
    3: [
        "narrateur|Chouchou porte le manteau vers les cordes.",
        "narrateur|La corde est rêche, un peu tiède.",
        "narrateur|Le siège de bois balance, vide.",
        "enfant-f|Il s'assoit avec moi !",
        "narrateur|Elle pose le manteau sur le siège.",
        "narrateur|Une poussée, et le tissu tombe.",
        "narrateur|La manche s'enroule autour de la corde.",
        "enfant-f|Il s'accroche, je ne peux pas.",
        "papa|La corde tient la manche, vois.",
        "maman|Le seau est au pied de bois.",
        "narrateur|Ses mains lâchent, un peu.",
        "enfant-f|Je n'y arrive pas.",
        "narrateur|Un croissant tremble sur la corde.",
        "papa|Tu le reprends, avant de rentrer ?",
    ],
}

T1_Q = {
    1: [
        "narrateur|Le manteau est au bord du bac.",
        "papa|Chouchou, tu fais quoi ?",
    ],
    2: [
        "narrateur|Le manteau est au bas du toboggan.",
        "maman|Chouchou, tu fais quoi ?",
    ],
    3: [
        "narrateur|Le manteau est pris dans la corde.",
        "papa|Chouchou, tu fais quoi ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Chouchou se baisse vers le tissu.",
        "narrateur|Elle secoue le sable, grain par grain.",
        "narrateur|Le croissant de cuivre reparaît, tiède.",
        "enfant-f|Je le reprends, il vient.",
        "maman|Merci, Chouchou, il est avec toi.",
        "papa|Tu le portes, pour le crochet ?",
        "enfant-f|Oui, je le garde.",
        "narrateur|Un grain reste dans une poche.",
        "narrateur|Le seau jaune revient, lui aussi.",
        "enfant-f|Il ne glisse plus.",
    ],
    2: [
        "narrateur|Chouchou descend les marches, une à une.",
        "narrateur|Elle ramasse le tas rouge, au bas.",
        "narrateur|Le croissant de cuivre reparaît, froid.",
        "enfant-f|Je le reprends, il est froid.",
        "papa|Merci, Chouchou, il est avec toi.",
        "maman|Tu le portes, pour le crochet ?",
        "enfant-f|Oui, je le serre.",
        "narrateur|Une feuille reste collée au tissu.",
        "narrateur|Le seau revient près des pieds.",
        "enfant-f|Il ne glisse plus.",
    ],
    3: [
        "narrateur|Chouchou tient la corde, puis la manche.",
        "narrateur|Elle tourne, lente, autour du bois.",
        "narrateur|La manche se libère, un peu froide.",
        "enfant-f|Je le reprends, il est à moi.",
        "maman|Merci, Chouchou, il est avec toi.",
        "papa|Tu le portes, pour le crochet ?",
        "enfant-f|Oui, contre moi.",
        "narrateur|Un brin de corde reste au croissant.",
        "narrateur|Le seau revient au pied de bois.",
        "enfant-f|Il ne s'enroule plus.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près du bac, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le manteau reste avec toi.",
    ],
    2: [
        "narrateur|Près du toboggan, un jeu l'appelle.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Le manteau reste avec toi.",
    ],
    3: [
        "narrateur|Près des cordes, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le manteau reste avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Chouchou pose le manteau au bord du bac.",
            "narrateur|Elle prend le ballon, rouge, un peu lisse.",
            "enfant-f|Il va rebondir, près de moi !",
            "narrateur|Le ballon tape le bois, puis file.",
            "narrateur|Elle court, le manteau reste derrière.",
            "narrateur|Au retour, une ombre rouge tient le bord.",
            "enfant-f|Il est là !",
            "narrateur|Elle saisit l'ombre, vide.",
            "narrateur|Sa main touche le bois, seulement.",
            "enfant-f|Il n'est plus là.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "papa|Regarde le croissant, pas l'ombre.",
            "narrateur|Le croissant brille dans le sable.",
            "maman|Il mène vers le jardin, plus loin.",
            "enfant-f|Je ne fonce pas.",
        ],
        (1, 2): [
            "narrateur|Chouchou pose le manteau près du seau.",
            "narrateur|Elle creuse, l'anse froide dans la paume.",
            "enfant-f|Je fais un puits, trop grand !",
            "narrateur|Le seau pèse, plein de sable mouillé.",
            "narrateur|La manche glisse dans le trou, lente.",
            "narrateur|Elle tire l'anse, trop occupée.",
            "narrateur|Au bord, une forme rouge reste, plate.",
            "enfant-f|Il est là, je le vois !",
            "narrateur|C'est l'ombre du seau, sur le bois.",
            "enfant-f|Le manteau a disparu.",
            "papa|Le croissant, vois, dans le creux.",
            "narrateur|Un croissant sort du sable, mince.",
            "maman|Il mène plus loin, dans le jardin.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le seau sonne, vide de manteau.",
        ],
        (1, 3): [
            "narrateur|Chouchou pose le doudou sur le manteau.",
            "narrateur|Les deux tissus se ressemblent, de dos.",
            "enfant-f|Vous restez là, tous les deux.",
            "narrateur|Elle creuse, le doudou contre la hanche.",
            "narrateur|Au retour, un dos rouge attend, flou.",
            "enfant-f|Mon manteau !",
            "narrateur|Elle saisit le doudou, pas le manteau.",
            "narrateur|Sous le doudou, le sable est nu.",
            "enfant-f|Il s'est caché, le rusé.",
            "maman|Le croissant, vois, pas le doudou.",
            "narrateur|Le croissant fuit sous une planche.",
            "papa|L'ombre a menti, le croissant dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le doudou a du sable à l'oreille.",
            "narrateur|Le bac garde un creux, sans rouge.",
        ],
        (2, 1): [
            "narrateur|Chouchou pose le manteau sur une marche.",
            "narrateur|Elle prend le ballon, près du métal.",
            "enfant-f|Il glisse, comme moi !",
            "narrateur|Le ballon dévale, vif, trop loin.",
            "narrateur|Elle court au bas, sans le tissu.",
            "narrateur|En haut, une ombre rouge tient la rampe.",
            "enfant-f|Il m'attend, là-haut !",
            "narrateur|Elle gravit, et l'ombre se casse.",
            "narrateur|Le métal est nu, tiède, vide.",
            "enfant-f|Ce n'était pas lui.",
            "papa|Le croissant, vois, sur le métal.",
            "narrateur|Le croissant descend, marche par marche.",
            "maman|Il mène plus loin, dans le jardin.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le ballon s'arrête, loin du rouge.",
        ],
        (2, 2): [
            "narrateur|Chouchou pose le manteau près des marches.",
            "narrateur|Elle emplit le seau, au pied du métal.",
            "enfant-f|Je verse en haut, comme la pluie !",
            "narrateur|L'eau du seau mouille la rampe, vive.",
            "narrateur|La manche boit, puis file, lourde.",
            "narrateur|Elle regarde le seau, pas le tissu.",
            "narrateur|Une tache rouge reste, plate, sur le métal.",
            "enfant-f|Il est collé, je le vois !",
            "narrateur|C'est l'eau, pas le manteau.",
            "enfant-f|Il a disparu, mouillé.",
            "maman|Le croissant, vois, le long du métal.",
            "narrateur|Le croissant fuit vers le jardin.",
            "papa|L'eau a menti, le croissant dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le seau goutte, sans manche dedans.",
        ],
        (2, 3): [
            "narrateur|Chouchou pose le doudou contre le manteau.",
            "narrateur|Sur la marche, les deux dos se touchent.",
            "enfant-f|Vous glissez avec moi, tous les deux.",
            "narrateur|Elle monte, le doudou sous le bras.",
            "narrateur|Au bas, un dos rouge attend, flou.",
            "enfant-f|Mon manteau m'attend !",
            "narrateur|Elle saisit l'air, et le doudou.",
            "narrateur|Le manteau n'est plus sur la marche.",
            "enfant-f|L'ombre a pris sa place.",
            "papa|Le croissant, vois, pas le doudou.",
            "narrateur|Le croissant court sous le métal.",
            "maman|Il mène plus loin, dans le jardin.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le doudou a une feuille, collée.",
            "narrateur|La rampe du toboggan reste nue.",
        ],
        (3, 1): [
            "narrateur|Chouchou pose le manteau sur le siège.",
            "narrateur|Elle prend le ballon, près des cordes.",
            "enfant-f|Je le lance, pendant que j'attends !",
            "narrateur|Le ballon file, et le siège part.",
            "narrateur|Elle court, le tissu reste derrière.",
            "narrateur|Au retour, un dos rouge balance, vide.",
            "enfant-f|Il se balance, je le vois !",
            "narrateur|Elle saisit l'ombre, sur le bois.",
            "narrateur|Le siège est nu, un peu tiède.",
            "enfant-f|Ce n'était que l'ombre.",
            "maman|Le croissant, vois, sur la corde.",
            "narrateur|Le croissant tremble, puis fuit.",
            "papa|L'ombre a menti, le croissant dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le ballon roule sous les cordes.",
        ],
        (3, 2): [
            "narrateur|Chouchou pose le manteau au pied de bois.",
            "narrateur|Elle emplit le seau, près des cordes.",
            "enfant-f|Je fais un poids, pour le siège !",
            "narrateur|Le seau pèse, et le siège part.",
            "narrateur|La manche s'accroche, puis se libère.",
            "narrateur|Elle regarde le seau, trop occupée.",
            "narrateur|Une tache rouge reste, au pied.",
            "enfant-f|Il est là, contre le bois !",
            "narrateur|C'est l'ombre du seau, allongée.",
            "enfant-f|Le manteau a disparu.",
            "papa|Le croissant, vois, autour de la corde.",
            "narrateur|Le croissant fuit vers le jardin.",
            "maman|La corde a menti, le croissant dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le seau sonne, contre le pied nu.",
        ],
        (3, 3): [
            "narrateur|Chouchou pose le doudou sur le manteau.",
            "narrateur|Sur le siège, les deux dos se confondent.",
            "enfant-f|Vous vous balancez, tous les deux.",
            "narrateur|Elle pousse, le doudou sous le bras.",
            "narrateur|Au retour, un dos rouge attend, flou.",
            "enfant-f|Mon manteau se balance !",
            "narrateur|Elle saisit le doudou, trop vite.",
            "narrateur|Le siège est nu, sans manteau.",
            "enfant-f|L'ombre a pris sa place.",
            "maman|Le croissant, vois, pas le doudou.",
            "narrateur|Le croissant court dans l'herbe.",
            "papa|Le siège a menti, le croissant dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le doudou sent l'herbe, un peu.",
            "narrateur|La corde se tait, sans manche.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Le croissant mène vers trois coins.",
        "papa|Le banc, le portail, ou le paillasson ?",
        "maman|On suit le croissant, pas l'ombre.",
    ],
    2: [
        "narrateur|Le croissant mène vers trois coins.",
        "maman|Le banc, le portail, ou le paillasson ?",
        "papa|On suit le croissant, pas l'eau.",
    ],
    3: [
        "narrateur|Le croissant mène vers trois coins.",
        "papa|Le banc, le portail, ou le paillasson ?",
        "maman|On suit le croissant, pas le doudou.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    """Revers allongé : tir trop vite, coincé, corps, refus, indice, geste neuf."""
    arrive = {
        1: [
            "narrateur|Le croissant court vers le banc.",
            "narrateur|Le bois des lattes est chaud, un peu.",
            "enfant-f|Il est dessous, je le vois !",
        ],
        2: [
            "narrateur|Le croissant court vers le portail.",
            "narrateur|Le loquet est froid, un peu rêche.",
            "enfant-f|Il est accroché, je le vois !",
        ],
        3: [
            "narrateur|Le croissant court vers le paillasson.",
            "narrateur|La paille est rêche, couleur d'herbe.",
            "enfant-f|Il est plié, je le vois !",
        ],
    }[c]
    snag = {
        1: [
            "narrateur|Elle tire la manche, trop vite.",
            "narrateur|Le tissu se coince entre deux lattes.",
            "enfant-f|Il tient, entre les lattes !",
        ],
        2: [
            "narrateur|Elle tire la manche, trop vite.",
            "narrateur|Le tissu s'enroule autour du loquet.",
            "enfant-f|Le loquet le mange !",
        ],
        3: [
            "narrateur|Elle tire le pli, trop vite.",
            "narrateur|Le tissu se coince sous le seuil.",
            "enfant-f|Le seuil le garde !",
        ],
    }[c]
    body = {
        1: [
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Envie et peur se bousculent, dans sa poitrine.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu regardes, ou tu tires ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute le bois, puis le col.",
            "narrateur|Le croissant de cuivre brille, minuscule.",
        ],
        2: [
            "narrateur|Ses épaules baissent, près du fer.",
            "narrateur|Dans sa poitrine, ça serre, trop fort.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu forces, ou tu regardes ?",
            "enfant-f|J'attends, je regarde.",
            "narrateur|Elle écoute le fer, puis le col.",
            "narrateur|Le croissant de cuivre clignote, minuscule.",
        ],
        3: [
            "narrateur|Chouchou fixe le pli, sans bouger.",
            "narrateur|L'envie de tirer lui pique les doigts.",
            "narrateur|Papa s'accroupit, près du paillasson.",
            "papa|Tu vois le croissant, où ?",
            "enfant-f|Je cherche, sans tirer.",
            "narrateur|Elle écarte la paille, lente.",
            "narrateur|Le croissant de cuivre brille, sous le bord.",
        ],
    }[c]
    # second snag — the reverse stays open a beat longer
    again = {
        1: "narrateur|La manche avance, puis s'arrête.",
        2: "narrateur|Le col glisse, puis se bloque.",
        3: "narrateur|Un pli cède, puis refuse.",
    }[c]
    helper = {
        1: {
            1: "narrateur|Elle cale le ballon sous la latte.",
            2: "narrateur|Elle glisse l'anse sous la latte.",
            3: "narrateur|Elle glisse le doudou sous la latte.",
        },
        2: {
            1: "narrateur|Elle cale le ballon contre le loquet.",
            2: "narrateur|Elle glisse l'anse sous le loquet.",
            3: "narrateur|Elle glisse le doudou sous le loquet.",
        },
        3: {
            1: "narrateur|Elle cale le ballon sous le bord.",
            2: "narrateur|Elle glisse l'anse sous le bord.",
            3: "narrateur|Elle glisse le doudou sous le bord.",
        },
    }[c][b]
    gesture = {
        1: "enfant-f|Je soulève la latte, sans tirer.",
        2: "enfant-f|Je soulève le loquet, sans tirer.",
        3: "enfant-f|Je soulève le bord, sans tirer.",
    }[c]
    free = {
        1: "narrateur|La manche se libère, lente, pleine.",
        2: "narrateur|La manche se libère, lente, froide.",
        3: "narrateur|La manche se libère, lente, rêche.",
    }[c]
    traces = {
        (1, 1): "narrateur|Un grain de sable reste au croissant.",
        (1, 2): "narrateur|L'anse du seau a laissé du sable.",
        (1, 3): "narrateur|L'oreille du doudou a du sable.",
        (2, 1): "narrateur|Une feuille du toboggan reste au tissu.",
        (2, 2): "narrateur|Une goutte du seau sèche au croissant.",
        (2, 3): "narrateur|Une feuille reste sur le doudou.",
        (3, 1): "narrateur|Un brin de corde reste au croissant.",
        (3, 2): "narrateur|L'anse a senti la corde, froide.",
        (3, 3): "narrateur|Le doudou a l'odeur de l'herbe.",
    }[(a, b)]
    almost = {
        (1, 1, 1): "narrateur|Le grain a failli tout cacher.",
        (1, 1, 2): "narrateur|Le loquet a failli tout garder.",
        (1, 1, 3): "narrateur|La paille a failli tout plier.",
        (1, 2, 1): "narrateur|Le sable a failli tout boire.",
        (1, 2, 2): "narrateur|L'anse a failli tout tirer.",
        (1, 2, 3): "narrateur|Le seuil a failli tout garder.",
        (1, 3, 1): "narrateur|Le doudou a failli tout cacher.",
        (1, 3, 2): "narrateur|Le fer a failli tout mordre.",
        (1, 3, 3): "narrateur|Le pli a failli tout perdre.",
        (2, 1, 1): "narrateur|La feuille a failli tout couvrir.",
        (2, 1, 2): "narrateur|Le métal a failli tout glisser.",
        (2, 1, 3): "narrateur|Le bord a failli tout plier.",
        (2, 2, 1): "narrateur|L'eau a failli tout mentir.",
        (2, 2, 2): "narrateur|Le seau a failli tout verser.",
        (2, 2, 3): "narrateur|La goutte a failli tout cacher.",
        (2, 3, 1): "narrateur|L'oreille a failli tout prendre.",
        (2, 3, 2): "narrateur|Le doudou a failli tout tromper.",
        (2, 3, 3): "narrateur|La feuille a failli tout coller.",
        (3, 1, 1): "narrateur|La corde a failli tout tenir.",
        (3, 1, 2): "narrateur|Le cling a failli tout couvrir.",
        (3, 1, 3): "narrateur|L'herbe a failli tout cacher.",
        (3, 2, 1): "narrateur|Le seau a failli tout peser.",
        (3, 2, 2): "narrateur|La corde a failli tout mentir.",
        (3, 2, 3): "narrateur|Le pied nu a failli tout perdre.",
        (3, 3, 1): "narrateur|Le siège a failli tout confondre.",
        (3, 3, 2): "narrateur|Le dos flou a failli tout prendre.",
        (3, 3, 3): "narrateur|L'odeur a failli tout perdre.",
    }[(a, b, c)]
    obj = OBJ[b]["name"]
    leave = {
        1: "On quitte le bac, croissant en main.",
        2: "On quitte le toboggan, croissant en main.",
        3: "On quitte les cordes, croissant en main.",
    }[a]
    adult = {
        1: "maman|Tu l'as, sans forcer.",
        2: "papa|Il est à toi, maintenant.",
        3: "maman|Tu l'as repris, Chouchou.",
    }[c]
    return (
        arrive
        + snag
        + body
        + [again, helper, gesture, free, adult]
        + [
            "narrateur|Chouchou serre le manteau, fière.",
            f"narrateur|{obj.capitalize()} vient aussi, près d'elle.",
            f"narrateur|{leave}",
            "enfant-f|On va au crochet, maintenant.",
            traces,
            almost,
            "narrateur|Voilà le manteau, au coin des crochets.",
        ]
    )


def ending_lines(a: int, b: int, c: int) -> list[str]:
    obj = OBJ[b]["name"]
    loc = LOC[a]["name"]
    lieu = LIEU[c]["name"]
    firsts = {
        (1, 1, 1): "L'escalier de bois fait cric, cric.",
        (1, 1, 2): "Le couloir sent les fraises, plus fort.",
        (1, 1, 3): "Le chat se recouche, sous la rampe.",
        (1, 2, 1): "Un grain roule sur une marche.",
        (1, 2, 2): "Le seau pose son ombre au bois.",
        (1, 2, 3): "Le panier de fraises attend, ouvert.",
        (1, 3, 1): "L'oreille du doudou dépasse du couloir.",
        (1, 3, 2): "Un fil du doudou pend près des clés.",
        (1, 3, 3): "Le doudou sent le sable, au bois.",
        (2, 1, 1): "Une feuille sèche sur le banc, loin.",
        (2, 1, 2): "Le métal du toboggan se tait, loin.",
        (2, 1, 3): "Un pas sur la rampe, puis plus.",
        (2, 2, 1): "Le seau penche, sous la rampe.",
        (2, 2, 2): "Le criiic du portail s'arrête.",
        (2, 2, 3): "La rampe du toboggan reste loin.",
        (2, 3, 1): "L'oreille molle dépasse du banc.",
        (2, 3, 2): "Le doudou a vu le métal, depuis le bois.",
        (2, 3, 3): "Un rayon a bougé, sur le bois.",
        (3, 1, 1): "Le ballon s'endort près de l'escalier.",
        (3, 1, 2): "La corde ne fait plus cling.",
        (3, 1, 3): "L'escalier de bois se tait.",
        (3, 2, 1): "Le seau pose son ombre sur la marche.",
        (3, 2, 2): "Le pain tiède attend, sur la table.",
        (3, 2, 3): "Les clés de papa restent dans la coupelle.",
        (3, 3, 1): "Le doudou a l'odeur de l'herbe.",
        (3, 3, 2): "Une fraise rentre dans le panier.",
        (3, 3, 3): "Le couloir retrouve son cric, unique.",
    }
    lasts = {
        (1, 1, 1): "Un grain de sable dort sur le croissant.",
        (1, 1, 2): "Le loquet garde un fil rouge.",
        (1, 1, 3): "Le paillasson tient un grain, minuscule.",
        (1, 2, 1): "L'anse du seau sèche sous la rampe.",
        (1, 2, 2): "Une fraise roule près du pain.",
        (1, 2, 3): "Le seau pose son ombre au seuil.",
        (1, 3, 1): "L'oreille du doudou veille, au bois.",
        (1, 3, 2): "Un fil gris pend près des clés.",
        (1, 3, 3): "Le doudou garde le sable, au col.",
        (2, 1, 1): "Une feuille sèche, loin du croissant.",
        (2, 1, 2): "Le métal se tait, loin du col.",
        (2, 1, 3): "Un pas s'éteint, sur le bois.",
        (2, 2, 1): "Le seau penche, vide, sous la rampe.",
        (2, 2, 2): "Le criiic du portail s'endort.",
        (2, 2, 3): "La rampe du toboggan reste muette.",
        (2, 3, 1): "L'oreille molle dépasse, près du banc.",
        (2, 3, 2): "Le doudou a le métal dans l'oreille.",
        (2, 3, 3): "Un rayon a quitté le bois.",
        (3, 1, 1): "Le ballon s'endort, près du cric.",
        (3, 1, 2): "La corde se tait, loin du col.",
        (3, 1, 3): "L'escalier garde un cric, unique.",
        (3, 2, 1): "Le seau pose son ombre, sur la marche.",
        (3, 2, 2): "Le pain tiède attend, près des fraises.",
        (3, 2, 3): "Les clés restent dans la coupelle.",
        (3, 3, 1): "Le doudou garde l'herbe, au chaud.",
        (3, 3, 2): "Une fraise rentre, rouge, dans le panier.",
        (3, 3, 3): "Le croissant de cuivre se tait, au crochet.",
    }
    qs = {
        1: "papa|Où s'était-il caché, sous le banc ?",
        2: "maman|Qui l'avait pris, au loquet ?",
        3: "papa|Qui l'avait plié, sur la paille ?",
    }[c]
    ans = {
        1: "enfant-f|Sous les lattes, avec le croissant.",
        2: "enfant-f|Le loquet, et le croissant.",
        3: "enfant-f|Le paillasson, tout plat.",
    }[c]
    joue = {
        1: "Chouchou a joué au bac.",
        2: "Chouchou a joué au toboggan.",
        3: "Chouchou a joué aux cordes.",
    }[a]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|{joue}",
        f"narrateur|Elle a choisi {obj}, pour le jeu.",
        f"narrateur|Le croissant l'a menée vers {lieu}.",
        "narrateur|Voilà le manteau rouge, sur la rampe.",
        "narrateur|Au col, le croissant de cuivre brille.",
        "enfant-f|Il est rentré, avec sa trace.",
        qs,
        ans,
        "maman|Les fraises nous attendent, maintenant.",
        "enfant-f|Je croque, elle est sucrée.",
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

    put("CHK_T0000_P0000", OPENING, "opening", "escalier,fraise,manteau")
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
            {"emphasis": "manteau", "fields": Q_FIELDS},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            LOC[a]["sons"],
            {"emphasis": "manteau"},
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
                    "option_1_label": "le banc",
                    "option_2_label": "le portail",
                    "option_3_label": "le paillasson",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    LIEU[c]["sons"],
                    {"emphasis": "croissant de cuivre"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "fraise,escalier",
                    {"emphasis": "croissant", "note": ending_note(a, b, c)},
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
        "Dans le couloir, le manteau rouge a choisi la rampe. Un croissant "
        "de cuivre brille au col, tourné vers le jardin. Chouchou veut le "
        "porter au coin des crochets avant que le soleil quitte le bois. "
        "Elle tire trop vite : la manche résiste, le sourire part. Au jardin, "
        "bac, toboggan ou balançoires, elle pose le manteau pour jouer : il "
        "glisse. Elle le reprend. Ballon, seau ou doudou : une ombre rouge "
        "ment, le croissant dit vrai. Elle refuse de foncer. Banc, portail "
        "ou paillasson, le tissu se coince, avance, s'arrête. Elle soulève "
        "sans tirer. Le croissant et le cric paient le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Chouchou, papa, maman"
    merged["setting"] = "couloir, rampe de bois, jardin de la maison, coin des crochets"
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
        "Le bois de la rampe garde une chaleur : le manteau rouge a choisi "
        "sa place. Au col, un croissant de cuivre brille vers le jardin. "
        "Chouchou veut le porter au coin des crochets avant que le soleil "
        "quitte le bois. Elle tire trop vite : la manche accroche, le sourire "
        "disparaît. Papa s'accroupit. Au bac, au toboggan ou aux balançoires, "
        "elle pose le manteau pour jouer : première idée, patatras. Elle le "
        "reprend. Ballon, seau ou doudou : une ombre rouge ment, le croissant "
        "dit vrai. Elle refuse de foncer. Banc, portail ou paillasson, le "
        "tissu se coince, avance, s'arrête. Elle soulève sans tirer. Le "
        "croissant et le cric paient le début. Le manteau garde une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : couloir, rampe de bois qui garde la chaleur, fraises, cric, "
        "coin des crochets.\n"
        "- Désir : porter le manteau au crochet, maintenant.\n"
        "- Objet : manteau rouge (croissant de cuivre), plus ballon / seau / doudou.\n"
        "- Indice unique : le croissant de cuivre, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : le soleil quitte la rampe.\n"
        "- Imprévu 1 : manche coincée, tissu qui glisse au jeu.\n"
        "- Cue : le croissant, pas la force. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : l'ombre du manteau ment ; le croissant mène.\n"
        "- Revers allongé : coincé, corps (envie et peur), refus de foncer, "
        "manche qui avance puis s'arrête, geste neuf.\n"
        "- Résolution : soulever sans tirer, au banc, au portail, au paillasson.\n"
        "- Retour : cric, croissant, fraise, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (le manteau a choisi la rampe), pas un gabarit v2.\n"
        "- Le premier choix n'enlève pas le manteau : il vient au jardin.\n"
        "- Revers allongé (audit : obstacle trop ponctuel) : coincé, corps, "
        "refus, second arrêt, geste lent.\n"
        "- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.003 vécue (reprendre le manteau), jamais dite.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Chouchou, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience au départ, petit découragement quand le manteau résiste "
        "ou disparaît, fierté calme quand Chouchou soulève sans tirer. "
        "L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N1 ≤ 10 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
