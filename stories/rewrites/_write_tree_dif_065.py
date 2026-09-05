#!/usr/bin/env python3
"""TREE-DIF-065 — Les arrosoirs de Chouchou, dans la serre (N1, DIF.BES.002, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-065"
N1 = LIMITS["N1"]
TITLE = "Les arrosoirs de Chouchou, dans la serre"
CHARS = "Chouchou, Raphaël, papa, maman"
SETTING = "serre derrière la maison, après la pluie : allée, table, bac"
FIL = (
    "Après la pluie, la serre fume derrière la maison. "
    "Sur le bec de l'arrosoir rouge, un anneau de zinc brille. "
    "Chouchou veut arroser avec Raphaël, avant que le soleil sèche tout. "
    "Elle appelle trop vite : il ne vient pas. "
    "Elle prend d'abord l'arrosoir rouge, la graine ou le tablier à pois ; les trois partent. "
    "À l'allée la flaque le retient, à la table le godet déborde, au bac il court trop. "
    "Elle refuse de foncer. L'anneau de zinc du début revient. "
    "Elle accepte son non, son autre idée, ou plus tard. Un arrosoir trouve sa place."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="anneau de zinc",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=l_anneau_brille_la_mission_peut_rater; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="arrosoir",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="serre",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_viennent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_partir_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=il_pose_sa_limite_elle_écoute; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="anneau de zinc",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=l_anneau_a_montré_d_attendre; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="anneau de zinc",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=un_arrosoir_a_trouvé_sa_place; tempo=posé; sourire=léger; respiration=ample",
    ),
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
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"puces « {tok} »: {ph}")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""
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
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
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
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if "note" in extra:
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
    out["night_policy"] = "play"
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms"):
            continue
        out[k] = v
    return out


def ending_note(a: int, b: int, c: int) -> str:
    times = {1: "posé", 2: "lent", 3: "ample"}
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=l_anneau_a_gardé_une_trace; "
        f"tempo={times[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|Derrière la maison, la serre fume, tiède.",
        "narrateur|Chouchou connaît chaque planche, chaque bac.",
        "narrateur|Après la pluie, un détail paraît nouveau.",
        "narrateur|Sur le bec rouge, un anneau de zinc brille.",
        "papa|Tu as vu cet anneau, Chouchou ?",
        "enfant-f|Il brille, comme une petite lune.",
        "maman|La terre sent le basilic mouillé.",
        "narrateur|En ce moment, Chouchou tient l'arrosoir.",
        "enfant-f|Je veux arroser, avec Raphaël.",
        "papa|Avant que le soleil sèche tout ?",
        "enfant-f|Oui, les arrosoirs, dans la serre.",
        "narrateur|Elle appelle trop vite, vers l'allée.",
        "narrateur|Raphaël ne bouge pas.",
        "narrateur|Le sourire de Chouchou disparaît.",
        "enfant-f|Il ne vient pas !",
        "maman|L'arrosoir, la graine, le tablier attendent.",
        "papa|Merci, tu as tenu la porte.",
        "narrateur|Une goutte glisse sur l'anneau de zinc.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Près de la porte, trois affaires attendent.",
        "narrateur|L'arrosoir, la graine, ou le tablier.",
        "papa|Par quoi tu commences, Chouchou ?",
    ]
)

T1 = {
    1: dict(
        lab="l'arrosoir rouge",
        ans="arrosoir",
        acc="arrosoir | l'arrosoir | l'arrosoir rouge | le rouge",
        retry="Chouchou a pris l'arrosoir.",
        sons="arrosoir,goutte",
        emp="arrosoir",
        passage=vet(
            [
                "narrateur|Chouchou prend l'arrosoir rouge, lourd.",
                "enfant-f|Toi, tu vas arroser avec moi.",
                "narrateur|Elle penche trop vite, une goutte tombe.",
                "maman|Tiens le bec, pas trop vite.",
                "narrateur|L'anneau de zinc se mouille, froid.",
                "papa|La graine et le tablier viennent.",
                "narrateur|Elle glisse le tablier sous son bras.",
                "narrateur|La graine reste au fond d'une poche.",
                "enfant-f|Raphaël arrose avec moi.",
                "papa|Tu lui proposes, sans le tirer ?",
                "enfant-f|Oui, papa.",
                "maman|Les trois affaires partent ensemble.",
            ]
        ),
        question=vet(
            [
                "narrateur|L'arrosoir rouge pèse, contre elle.",
                "maman|Elle a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|L'arrosoir.",
                "maman|Oui, le rouge.",
                "narrateur|Une goutte glisse de l'anneau de zinc.",
                "enfant-f|On va jusqu'à Raphaël.",
                "papa|La serre est embuée, tiède.",
                "enfant-f|Oui, papa, j'y vais.",
                "narrateur|L'anneau de zinc reste froid.",
                "maman|Les planches sentent la terre mouillée.",
            ]
        ),
    ),
    2: dict(
        lab="la graine",
        ans="graine",
        acc="graine | la graine | la graine de basilic | basilic",
        retry="Chouchou a pris la graine.",
        sons="graine",
        emp="graine",
        passage=vet(
            [
                "narrateur|Chouchou prend la graine, trop sèche.",
                "enfant-f|Toi, tu vas pousser, tout petit.",
                "narrateur|Elle serre trop, la graine pique.",
                "papa|Ouvre la paume, laisse-la reposer.",
                "narrateur|La graine sent le basilic, tiède.",
                "maman|L'arrosoir t'attend, près du seau.",
                "narrateur|Elle enfile le tablier, un peu trop vite.",
                "narrateur|Le bec rouge tape contre son genou.",
                "enfant-f|On plante, avec Raphaël.",
                "maman|Tu lui proposes, sans le presser ?",
                "enfant-f|Oui, maman.",
                "papa|La poche garde bien la graine.",
            ]
        ),
        question=vet(
            [
                "narrateur|La graine reste dans sa paume.",
                "papa|Elle a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|La graine.",
                "papa|Oui.",
                "narrateur|Un peu de terre colle au pouce.",
                "enfant-f|On va la montrer à Raphaël.",
                "maman|Ça sent le basilic, ici.",
                "enfant-f|Oui, maman.",
                "narrateur|L'anneau de zinc brille, au bec.",
                "papa|La poche reste bien fermée.",
            ]
        ),
    ),
    3: dict(
        lab="le tablier à pois",
        ans="tablier",
        acc="tablier | le tablier | le tablier à pois | les pois",
        retry="Chouchou a mis le tablier.",
        sons="tissu",
        emp="tablier",
        passage=vet(
            [
                "narrateur|Chouchou enfile le tablier à pois.",
                "enfant-f|Les pois sont ronds, tout blancs.",
                "maman|Noue-le lentement, pas trop fort.",
                "narrateur|Elle noue trop vite, le nœud glisse.",
                "papa|Voici l'arrosoir, accroche-le.",
                "narrateur|Le bec rouge tape contre son genou.",
                "narrateur|Elle glisse la graine dans une poche.",
                "enfant-f|Raphaël va aimer les pois.",
                "papa|Tu lui proposes, sans le tirer ?",
                "enfant-f|Oui.",
                "maman|Le tablier tient, bien noué.",
                "narrateur|L'anneau de zinc frôle un pois.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le tablier à pois tient, noué.",
                "maman|Elle a mis quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|Le tablier.",
                "maman|Oui, celui aux pois.",
                "narrateur|Un pois blanc brille, un peu humide.",
                "enfant-f|Raphaël va voir les pois.",
                "papa|On avance, tous les trois ?",
                "enfant-f|Oui.",
                "narrateur|L'anneau de zinc cogne un pois.",
                "maman|Les poches sentent l'eau de pluie.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Raphaël est dans la serre.",
            "maman|L'allée a une flaque, au milieu.",
            "narrateur|La table à rempoter colle.",
            "papa|Le bac à tomates tremble, mouillé.",
            "papa|On va vers où, Chouchou ?",
        ]
    ),
    2: vet(
        [
            "narrateur|La graine chauffe au fond de la poche.",
            "maman|L'allée a une flaque, au milieu.",
            "narrateur|La table à rempoter colle.",
            "papa|Le bac à tomates tremble, mouillé.",
            "maman|On va vers où, Chouchou ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Un pois blanc frotte l'anneau de zinc.",
            "papa|L'allée a une flaque, au milieu.",
            "narrateur|La table à rempoter colle.",
            "maman|Le bac à tomates tremble, mouillé.",
            "papa|On va vers où, Chouchou ?",
        ]
    ),
}

T2_SCENE = {
    (1, 1): vet(
        [
            "narrateur|L'arrosoir rouge pèse contre son bras.",
            "narrateur|Raphaël est accroupi, près de l'eau.",
            "enfant-f|On aligne les arrosoirs, viens !",
            "copain|La flaque, moi.",
            "narrateur|Elle tire sa manche, trop vite.",
            "narrateur|Une goutte tombe dans l'eau, ploc.",
            "narrateur|L'anneau de zinc tremble, dans l'eau.",
            "copain|Non.",
            "narrateur|Raphaël ne dit plus rien.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "enfant-f|Tu ne veux pas ?",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
        ]
    ),
    (1, 2): vet(
        [
            "narrateur|Le bec rouge sonne contre le bois.",
            "narrateur|Raphaël a de la terre aux doigts.",
            "enfant-f|Tu arroses avec moi ?",
            "copain|Mes mains collent trop.",
            "narrateur|Elle penche l'arrosoir vers le godet.",
            "narrateur|Le godet est trop plein, ça déborde.",
            "narrateur|L'anneau de zinc disparaît sous l'eau.",
            "copain|Le godet, d'abord.",
            "narrateur|Il ne lâche pas le godet.",
            "narrateur|L'envie serre la poitrine de Chouchou.",
            "enfant-f|Ça a trop coulé !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
        ]
    ),
    (1, 3): vet(
        [
            "narrateur|Le bec rouge passe sous les feuilles.",
            "narrateur|Raphaël court trop, entre les tomates.",
            "enfant-f|On arrose les feuilles ?",
            "copain|Pas là-dedans.",
            "narrateur|Elle le suit trop vite, l'arrosoir penche.",
            "narrateur|Une feuille mouillée tape le visage.",
            "narrateur|L'anneau de zinc se cache sous le vert.",
            "copain|Ça mouille, Chouchou !",
            "narrateur|Il recule, les lèvres fermées.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "enfant-f|Tu ne viens pas ?",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Les feuilles restent trop basses.",
            "enfant-f|J'écoute.",
        ]
    ),
    (2, 1): vet(
        [
            "narrateur|La graine reste au sec, dans la poche.",
            "narrateur|Raphaël est accroupi, près de l'eau.",
            "enfant-f|On plante, puis on arrose ?",
            "copain|La flaque, d'abord.",
            "narrateur|Elle avance trop près, la poche penche.",
            "narrateur|La graine manque de tomber dans l'eau.",
            "narrateur|L'anneau de zinc tremble, dans l'eau.",
            "copain|Non.",
            "narrateur|Raphaël secoue la tête, sans mot.",
            "narrateur|Chouchou serre la poche, les joues chaudes.",
            "enfant-f|Elle a failli tomber !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
        ]
    ),
    (2, 2): vet(
        [
            "narrateur|La graine pique sa paume, trop sèche.",
            "narrateur|Raphaël presse la terre du godet.",
            "enfant-f|On plante la graine ici ?",
            "copain|Mes mains collent trop.",
            "narrateur|Elle pousse la graine vers le godet.",
            "narrateur|Le godet est trop plein, ça déborde.",
            "narrateur|L'anneau de zinc disparaît sous la boue.",
            "copain|Le godet, à moi.",
            "narrateur|Un peu de terre tombe sur ses pieds.",
            "narrateur|L'inquiétude bouscule l'envie, au ventre.",
            "enfant-f|Elle va se noyer !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
        ]
    ),
    (2, 3): vet(
        [
            "narrateur|La poche frotte une feuille, trop mouillée.",
            "narrateur|Raphaël court trop, entre les tomates.",
            "enfant-f|On plante ici, tout près ?",
            "copain|Pas là-dedans.",
            "narrateur|Elle le suit trop vite, la poche s'ouvre.",
            "narrateur|Une feuille mouillée tape le visage.",
            "narrateur|L'anneau de zinc se cache sous le vert.",
            "copain|Ça mouille !",
            "narrateur|Il recule, les lèvres fermées.",
            "narrateur|Chouchou referme la poche, le cœur serré.",
            "enfant-f|La graine est restée ?",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Les feuilles restent trop basses.",
            "enfant-f|J'écoute.",
        ]
    ),
    (3, 1): vet(
        [
            "narrateur|Un pois blanc se penche vers l'eau.",
            "narrateur|Raphaël est accroupi, près de la flaque.",
            "enfant-f|Tu prends un arrosoir ?",
            "copain|Mes bottes restent ici.",
            "narrateur|Elle entre trop vite dans l'eau.",
            "narrateur|Un pois blanc se mouille, trop fort.",
            "narrateur|L'anneau de zinc tremble, dans l'eau.",
            "copain|Non.",
            "narrateur|Raphaël ne dit plus rien.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "enfant-f|Tu ne veux pas les pois ?",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Il ne bouge pas.",
            "enfant-f|J'écoute.",
        ]
    ),
    (3, 2): vet(
        [
            "narrateur|Un pois blanc se tache de brun.",
            "narrateur|Raphaël a de la terre aux doigts.",
            "enfant-f|Tu veux le tablier ?",
            "copain|Mes mains collent trop.",
            "narrateur|Elle noue trop vite, trop près du godet.",
            "narrateur|Le godet est trop plein, ça déborde.",
            "narrateur|L'anneau de zinc disparaît sous la boue.",
            "copain|Le godet, d'abord.",
            "narrateur|La terre tache trois pois, d'un coup.",
            "narrateur|Chouchou baisse les yeux, la gorge serrée.",
            "enfant-f|Les pois sont bruns !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
        ]
    ),
    (3, 3): vet(
        [
            "narrateur|Un pois blanc se colle d'eau.",
            "narrateur|Raphaël court trop, entre les tomates.",
            "enfant-f|Tu viens sous les feuilles ?",
            "copain|Pas là-dedans.",
            "narrateur|Elle le suit trop vite, le tablier s'accroche.",
            "narrateur|Une feuille mouillée tape le visage.",
            "narrateur|L'anneau de zinc se cache sous le vert.",
            "copain|Ça mouille, Chouchou !",
            "narrateur|Il recule, les lèvres fermées.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "enfant-f|Le tablier s'est accroché !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
        ]
    ),
}

T3_LABS = {
    1: ("le bord", "la feuille", "les bottes"),
    2: ("le godet", "la terre", "le robinet"),
    3: ("le pas", "le basilic", "le torchon"),
}

T3_Q = {
    1: vet(
        [
            "narrateur|La flaque tient Raphaël, sans un mot.",
            "papa|Le bord, la feuille, ou les bottes ?",
        ]
    ),
    2: vet(
        [
            "narrateur|La terre colle à ses doigts, trop brune.",
            "maman|Le godet, la terre, ou le robinet ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Les feuilles restent trop mouillées.",
            "papa|Le pas, le basilic, ou le torchon ?",
        ]
    ),
}

T3_EMP = {
    1: {1: "bord", 2: "feuille", 3: "bottes"},
    2: {1: "godet", 2: "terre", 3: "robinet"},
    3: {1: "pas", 2: "basilic", 3: "torchon"},
}

RES = {
    (1, 1, 1): vet(
        [
            "enfant-f|D'accord, on reste au bord.",
            "narrateur|Elle pose l'arrosoir hors de l'eau.",
            "narrateur|Elle refuse de foncer dans la flaque.",
            "narrateur|L'anneau de zinc reste au sec.",
            "copain|Je reste ici, moi.",
            "enfant-f|J'arrose une plante, alors.",
            "narrateur|Un seul bec penche, près du bord.",
            "papa|La flaque lui reste, à lui.",
            "maman|Ton arrosoir est resté au sec.",
            "enfant-f|C'est bien, comme ça.",
            "narrateur|Papa ne dit pas comment faire.",
            "narrateur|L'anneau de zinc a parlé, sans mot.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "copain|Une feuille bateau, plutôt.",
            "enfant-f|D'accord, on pousse la feuille.",
            "narrateur|Elle refuse de tirer Raphaël.",
            "narrateur|Le bec rouge pousse la feuille, lent.",
            "narrateur|L'anneau de zinc se mire dans l'eau.",
            "copain|Elle va jusqu'au bord !",
            "enfant-f|Après, une plante, tout petit.",
            "narrateur|Une goutte part, puis le bec se tait.",
            "papa|Vous avez fait un bateau, d'abord.",
            "maman|L'arrosoir attend, plus loin.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|L'anneau de zinc a guidé la feuille.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "copain|Plus tard, quand les bottes sèchent.",
            "enfant-f|D'accord, plus tard.",
            "narrateur|Elle laisse l'arrosoir, sans insister.",
            "narrateur|Elle refuse de foncer, les pieds mouillés.",
            "copain|Je reste un peu.",
            "enfant-f|Une plante m'attend, au sec.",
            "narrateur|Un seul bec reste au bord.",
            "papa|Les bottes restent dans l'eau.",
            "maman|La flaque n'a plus de défilé.",
            "narrateur|L'anneau de zinc attend, froid.",
            "enfant-f|On reviendra, quand tu voudras.",
            "narrateur|Le zinc a tenu, sans se jeter.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "enfant-f|D'accord, tu gardes le godet.",
            "copain|La terre, c'est à moi.",
            "narrateur|L'arrosoir rouge reste à côté.",
            "narrateur|Elle refuse de verser dans le trop-plein.",
            "narrateur|L'anneau de zinc reparaît, hors de l'eau.",
            "narrateur|Il presse la terre, trop brun.",
            "enfant-f|J'arrose une plante, à côté.",
            "narrateur|Un seul bec penche, près du bois.",
            "papa|Le godet est resté à lui.",
            "maman|L'arrosoir est resté à toi.",
            "enfant-f|Deux jeux, l'un près de l'autre.",
            "narrateur|L'anneau de zinc a dit : à côté.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "copain|On presse la terre, plutôt.",
            "enfant-f|D'accord, on appuie ensemble.",
            "narrateur|Deux paumes collent près de l'arrosoir.",
            "narrateur|Elle refuse de verser trop vite.",
            "narrateur|L'anneau de zinc reste hors du godet.",
            "narrateur|Un petit mont brun se tient.",
            "copain|C'est un nid de terre !",
            "enfant-f|Puis une plante, tout petit.",
            "papa|Vous avez pressé, d'abord.",
            "maman|L'eau viendra après.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|L'anneau de zinc a vu le nid.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "copain|Plus tard, après le robinet.",
            "enfant-f|D'accord, va te laver.",
            "narrateur|L'arrosoir rouge attend près du robinet.",
            "narrateur|Elle refuse de le retenir.",
            "narrateur|L'eau du robinet chante, tout près.",
            "copain|Mes doigts sont bruns.",
            "enfant-f|Une plante m'attend, au sec.",
            "narrateur|L'anneau de zinc sèche, sans verser.",
            "papa|Le robinet chante pour lui.",
            "maman|La table garde sa terre.",
            "enfant-f|Quand tes mains seront propres.",
            "narrateur|Le zinc a attendu le chant d'eau.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "enfant-f|D'accord, on reste dehors.",
            "copain|Les feuilles, j'aime pas.",
            "narrateur|L'arrosoir rouge recule d'un pas.",
            "narrateur|Elle refuse de le pousser sous le vert.",
            "narrateur|L'anneau de zinc sort de l'ombre.",
            "narrateur|Ils reculent d'un pas, côte à côte.",
            "enfant-f|J'arrose une plante, d'ici.",
            "narrateur|Un seul bec penche, de loin.",
            "papa|Le bac lui reste trop mouillé.",
            "maman|Ton arrosoir n'est pas entré.",
            "enfant-f|De loin, ça suffit.",
            "narrateur|L'anneau de zinc a choisi le pas.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "copain|Le basilic, plutôt, il sent bon.",
            "enfant-f|D'accord, on sent, d'abord.",
            "narrateur|Le bec rouge s'arrête près du basilic.",
            "narrateur|Elle refuse de foncer sous les tomates.",
            "narrateur|L'anneau de zinc frôle une feuille verte.",
            "narrateur|Une feuille de basilic, trop près du nez.",
            "copain|Ça pique le nez, un peu.",
            "enfant-f|Puis une plante, tout petit.",
            "papa|Vous avez senti, d'abord.",
            "maman|Les feuilles restent derrière, mouillées.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|L'anneau de zinc a suivi l'odeur.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "copain|Plus tard, après le torchon.",
            "enfant-f|D'accord, essuie-toi.",
            "narrateur|L'arrosoir rouge attend pendant le torchon.",
            "narrateur|Elle refuse de le tirer sous les feuilles.",
            "narrateur|Maman tend le torchon, sans parler fort.",
            "copain|Mon nez n'est plus mouillé.",
            "enfant-f|Une plante m'attend, au sec.",
            "narrateur|L'anneau de zinc sèche, essuyé.",
            "papa|Son nez est sec, maintenant.",
            "maman|Les feuilles n'ont plus collé.",
            "enfant-f|Quand tu seras prêt.",
            "narrateur|Le zinc a attendu le tissu sec.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "enfant-f|D'accord, on reste au bord.",
            "narrateur|Elle pose la graine hors de l'eau.",
            "narrateur|Elle refuse de foncer dans la flaque.",
            "narrateur|L'anneau de zinc reste au sec.",
            "copain|Je reste ici, moi.",
            "enfant-f|Je plante une graine, alors.",
            "narrateur|La poche s'ouvre, hors de l'eau.",
            "papa|La flaque lui reste, à lui.",
            "maman|Ta graine est restée au sec.",
            "enfant-f|C'est bien, comme ça.",
            "narrateur|Papa ne dit pas comment faire.",
            "narrateur|L'anneau de zinc a gardé la graine.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "copain|Une feuille bateau, plutôt.",
            "enfant-f|D'accord, on pousse la feuille.",
            "narrateur|Elle refuse de tirer Raphaël.",
            "narrateur|La poche reste au sec, près de l'eau.",
            "narrateur|L'anneau de zinc se mire dans l'eau.",
            "narrateur|La feuille glisse, trop verte.",
            "copain|Elle va jusqu'au bord !",
            "enfant-f|Après, on plante, tout petit.",
            "papa|Vous avez fait un bateau, d'abord.",
            "maman|La graine attend, plus loin.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|L'anneau de zinc a guidé la feuille.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "copain|Plus tard, quand les bottes sèchent.",
            "enfant-f|D'accord, plus tard.",
            "narrateur|Elle laisse la graine, sans insister.",
            "narrateur|Elle refuse de foncer, les pieds mouillés.",
            "copain|Je reste un peu.",
            "enfant-f|Une terre m'attend, au sec.",
            "narrateur|La poche reste au bord.",
            "papa|Les bottes restent dans l'eau.",
            "maman|La flaque n'a plus de défilé.",
            "narrateur|L'anneau de zinc attend, froid.",
            "enfant-f|On reviendra, quand tu voudras.",
            "narrateur|Le zinc a tenu la graine au sec.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "enfant-f|D'accord, tu gardes le godet.",
            "copain|La terre, c'est à moi.",
            "narrateur|La graine reste à côté du godet.",
            "narrateur|Elle refuse de la noyer là-dedans.",
            "narrateur|L'anneau de zinc reparaît, hors de la boue.",
            "narrateur|Il presse la terre, trop brun.",
            "enfant-f|Je plante à côté, alors.",
            "narrateur|Un trou minuscule s'ouvre, au sec.",
            "papa|Le godet est resté à lui.",
            "maman|La graine est restée à toi.",
            "enfant-f|Deux terres, l'une près de l'autre.",
            "narrateur|L'anneau de zinc a dit : à côté.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "copain|On presse la terre, plutôt.",
            "enfant-f|D'accord, on appuie ensemble.",
            "narrateur|Deux paumes collent autour de la graine.",
            "narrateur|Elle refuse de la jeter trop vite.",
            "narrateur|L'anneau de zinc reste hors du godet.",
            "narrateur|Un petit mont brun se tient.",
            "copain|C'est un nid de terre !",
            "enfant-f|La graine dort là, tout petit.",
            "papa|Vous avez pressé, d'abord.",
            "maman|L'eau viendra après.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|L'anneau de zinc a vu le nid.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "copain|Plus tard, après le robinet.",
            "enfant-f|D'accord, va te laver.",
            "narrateur|La graine attend près du robinet.",
            "narrateur|Elle refuse de le retenir.",
            "narrateur|L'eau du robinet chante, tout près.",
            "copain|Mes doigts sont bruns.",
            "enfant-f|Une terre m'attend, au sec.",
            "narrateur|L'anneau de zinc sèche, sans verser.",
            "papa|Le robinet chante pour lui.",
            "maman|La table garde sa terre.",
            "enfant-f|Quand tes mains seront propres.",
            "narrateur|Le zinc a attendu le chant d'eau.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "enfant-f|D'accord, on reste dehors.",
            "copain|Les feuilles, j'aime pas.",
            "narrateur|La graine recule d'un pas, dans la poche.",
            "narrateur|Elle refuse de la perdre sous le vert.",
            "narrateur|L'anneau de zinc sort de l'ombre.",
            "narrateur|Ils reculent d'un pas, côte à côte.",
            "enfant-f|Je plante d'ici, au sec.",
            "narrateur|La poche s'ouvre, de loin.",
            "papa|Le bac lui reste trop mouillé.",
            "maman|Ta graine n'est pas entrée.",
            "enfant-f|De loin, ça suffit.",
            "narrateur|L'anneau de zinc a choisi le pas.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "copain|Le basilic, plutôt, il sent bon.",
            "enfant-f|D'accord, on sent, d'abord.",
            "narrateur|La graine sent le basilic, trop près.",
            "narrateur|Elle refuse de foncer sous les tomates.",
            "narrateur|L'anneau de zinc frôle une feuille verte.",
            "narrateur|Une feuille de basilic, trop près du nez.",
            "copain|Ça pique le nez, un peu.",
            "enfant-f|Puis on plante, tout petit.",
            "papa|Vous avez senti, d'abord.",
            "maman|Les feuilles restent derrière, mouillées.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|L'anneau de zinc a suivi l'odeur.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "copain|Plus tard, après le torchon.",
            "enfant-f|D'accord, essuie-toi.",
            "narrateur|La graine attend pendant le torchon.",
            "narrateur|Elle refuse de le tirer sous les feuilles.",
            "narrateur|Maman tend le torchon, sans parler fort.",
            "copain|Mon nez n'est plus mouillé.",
            "enfant-f|Une terre m'attend, au sec.",
            "narrateur|L'anneau de zinc sèche, essuyé.",
            "papa|Son nez est sec, maintenant.",
            "maman|Les feuilles n'ont plus collé.",
            "enfant-f|Quand tu seras prêt.",
            "narrateur|Le zinc a attendu le tissu sec.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "enfant-f|D'accord, on reste au bord.",
            "narrateur|Elle pose le tablier hors de l'eau.",
            "narrateur|Elle refuse de foncer dans la flaque.",
            "narrateur|L'anneau de zinc reste au sec.",
            "copain|Je reste ici, moi.",
            "enfant-f|J'arrose une plante, alors.",
            "narrateur|Un pois blanc sèche, hors de l'eau.",
            "papa|La flaque lui reste, à lui.",
            "maman|Ton tablier est resté au sec.",
            "enfant-f|C'est bien, comme ça.",
            "narrateur|Papa ne dit pas comment faire.",
            "narrateur|L'anneau de zinc a gardé les pois.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "copain|Une feuille bateau, plutôt.",
            "enfant-f|D'accord, on pousse la feuille.",
            "narrateur|Elle refuse de tirer Raphaël.",
            "narrateur|Un pois blanc se penche vers l'eau.",
            "narrateur|L'anneau de zinc se mire dans l'eau.",
            "narrateur|La feuille glisse, trop verte.",
            "copain|Elle va jusqu'au bord !",
            "enfant-f|Après, une plante, tout petit.",
            "papa|Vous avez fait un bateau, d'abord.",
            "maman|Le tablier attend, plus loin.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|L'anneau de zinc a guidé la feuille.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "copain|Plus tard, quand les bottes sèchent.",
            "enfant-f|D'accord, plus tard.",
            "narrateur|Elle laisse le tablier, sans insister.",
            "narrateur|Elle refuse de foncer, les pieds mouillés.",
            "copain|Je reste un peu.",
            "enfant-f|Une plante m'attend, au sec.",
            "narrateur|Un pois blanc reste au bord.",
            "papa|Les bottes restent dans l'eau.",
            "maman|La flaque n'a plus de défilé.",
            "narrateur|L'anneau de zinc attend, froid.",
            "enfant-f|On reviendra, quand tu voudras.",
            "narrateur|Le zinc a tenu les pois au sec.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "enfant-f|D'accord, tu gardes le godet.",
            "copain|La terre, c'est à moi.",
            "narrateur|Le tablier à pois reste à côté.",
            "narrateur|Elle refuse de le salir dans le trop-plein.",
            "narrateur|L'anneau de zinc reparaît, hors de la boue.",
            "narrateur|Il presse la terre, trop brun.",
            "enfant-f|J'arrose une plante, à côté.",
            "narrateur|Un pois blanc sèche, près du bois.",
            "papa|Le godet est resté à lui.",
            "maman|Le tablier est resté à toi.",
            "enfant-f|Deux jeux, l'un près de l'autre.",
            "narrateur|L'anneau de zinc a dit : à côté.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "copain|On presse la terre, plutôt.",
            "enfant-f|D'accord, on appuie ensemble.",
            "narrateur|Deux paumes collent sur le tablier.",
            "narrateur|Elle refuse de verser trop vite.",
            "narrateur|L'anneau de zinc reste hors du godet.",
            "narrateur|Un petit mont brun se tient.",
            "copain|C'est un nid de terre !",
            "enfant-f|Puis une plante, tout petit.",
            "papa|Vous avez pressé, d'abord.",
            "maman|L'eau viendra après.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|L'anneau de zinc a vu le nid.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "copain|Plus tard, après le robinet.",
            "enfant-f|D'accord, va te laver.",
            "narrateur|Le tablier à pois attend, trop brun.",
            "narrateur|Elle refuse de le retenir.",
            "narrateur|L'eau du robinet chante, tout près.",
            "copain|Mes doigts sont bruns.",
            "enfant-f|Une plante m'attend, au sec.",
            "narrateur|L'anneau de zinc sèche, sans verser.",
            "papa|Le robinet chante pour lui.",
            "maman|La table garde sa terre.",
            "enfant-f|Quand tes mains seront propres.",
            "narrateur|Le zinc a attendu le chant d'eau.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "enfant-f|D'accord, on reste dehors.",
            "copain|Les feuilles, j'aime pas.",
            "narrateur|Le tablier à pois recule d'un pas.",
            "narrateur|Elle refuse de l'accrocher sous le vert.",
            "narrateur|L'anneau de zinc sort de l'ombre.",
            "narrateur|Ils reculent d'un pas, côte à côte.",
            "enfant-f|J'arrose une plante, d'ici.",
            "narrateur|Un pois blanc sèche, de loin.",
            "papa|Le bac lui reste trop mouillé.",
            "maman|Ton tablier n'est pas entré.",
            "enfant-f|De loin, ça suffit.",
            "narrateur|L'anneau de zinc a choisi le pas.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "copain|Le basilic, plutôt, il sent bon.",
            "enfant-f|D'accord, on sent, d'abord.",
            "narrateur|Un pois blanc frôle le basilic.",
            "narrateur|Elle refuse de foncer sous les tomates.",
            "narrateur|L'anneau de zinc frôle une feuille verte.",
            "narrateur|Une feuille de basilic, trop près du nez.",
            "copain|Ça pique le nez, un peu.",
            "enfant-f|Puis une plante, tout petit.",
            "papa|Vous avez senti, d'abord.",
            "maman|Les feuilles restent derrière, mouillées.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|L'anneau de zinc a suivi l'odeur.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "copain|Plus tard, après le torchon.",
            "enfant-f|D'accord, essuie-toi.",
            "narrateur|Le tablier à pois attend, trop mouillé.",
            "narrateur|Elle refuse de le tirer sous les feuilles.",
            "narrateur|Maman tend le torchon, sans parler fort.",
            "copain|Mon nez n'est plus mouillé.",
            "enfant-f|Une plante m'attend, au sec.",
            "narrateur|L'anneau de zinc sèche, essuyé.",
            "papa|Son nez est sec, maintenant.",
            "maman|Les feuilles n'ont plus collé.",
            "enfant-f|Quand tu seras prêt.",
            "narrateur|Le zinc a attendu le tissu sec.",
        ]
    ),
}

FIN = {
    (1, 1, 1): vet(
        [
            "narrateur|Un seul arrosoir, une seule plante.",
            "enfant-f|Le défilé n'est pas venu.",
            "copain|La flaque m'a gardé.",
            "papa|On rentre, les bottes sont lourdes.",
            "maman|Ça sent le basilic, dehors.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|La plante a bu, tout petit.",
            "narrateur|Une goutte tient dans l'anneau de zinc.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "narrateur|Après le bateau, un seul arrosoir penche.",
            "copain|La feuille est arrivée au bord.",
            "enfant-f|Puis on a arrosé une plante.",
            "papa|Vous avez soufflé, d'abord.",
            "maman|La serre reste tiède, trop grise.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|On rentre, les pieds mouillés.",
            "narrateur|Une feuille sèche contre l'anneau de zinc.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mes bottes sèchent.",
            "enfant-f|Une plante a bu, sans lui.",
            "papa|On rentre, sans le défilé.",
            "maman|La flaque reste, trop ronde.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|Raphaël viendra, une autre fois.",
            "narrateur|L'anneau de zinc sèche près des bottes.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "narrateur|Un seul arrosoir, une seule plante.",
            "copain|Mon godet est resté à moi.",
            "enfant-f|J'ai arrosé à côté.",
            "papa|On rentre, les mains brunes.",
            "maman|La table garde sa terre.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|Le godet et l'arrosoir se parlent.",
            "narrateur|L'anneau de zinc porte un grain de terre.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "narrateur|Après le nid, un seul arrosoir penche.",
            "copain|On a pressé, d'abord.",
            "enfant-f|Puis une plante a bu.",
            "papa|Vos paumes sentent la terre.",
            "maman|On rentre, trop bruns, trop contents.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|Le nid reste sur la table.",
            "narrateur|L'anneau de zinc garde le nid brun.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mes doigts sont bruns.",
            "enfant-f|Une plante a bu, sans lui.",
            "papa|On rentre, le robinet se tait.",
            "maman|La terre reste sur la table.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|Raphaël lavera, une autre fois.",
            "narrateur|Une goutte du robinet sèche sur l'anneau.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "narrateur|Un seul arrosoir, une seule plante.",
            "copain|Je suis resté dehors, moi.",
            "enfant-f|J'ai arrosé de loin.",
            "papa|On rentre, les visages secs.",
            "maman|Le bac reste trop mouillé, derrière.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|Les feuilles n'ont pas tapé.",
            "narrateur|L'anneau de zinc reste hors du bac.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "narrateur|Après le basilic, un seul arrosoir penche.",
            "copain|Ça piquait le nez.",
            "enfant-f|Puis une plante a bu.",
            "papa|Vos manches sentent le vert.",
            "maman|On rentre, ça sent le basilic.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|Les feuilles restent derrière, mouillées.",
            "narrateur|Une feuille de basilic colle à l'anneau.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mon nez est sec, maintenant.",
            "enfant-f|Une plante a bu, sans lui.",
            "papa|On rentre, le torchon sous le bras.",
            "maman|Les vitres restent embuées, trop grises.",
            "narrateur|L'arrosoir rouge a une goutte, au bec.",
            "enfant-f|Raphaël essuiera, une autre fois.",
            "narrateur|Le torchon a séché l'anneau de zinc.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "narrateur|Une seule graine, une seule terre.",
            "enfant-f|Le défilé n'est pas venu.",
            "copain|La flaque m'a gardé.",
            "papa|On rentre, les bottes sont lourdes.",
            "maman|Ça sent le basilic, dehors.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Elle a une maison, tout petit.",
            "narrateur|La graine sèche près de l'anneau de zinc.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "narrateur|Après le bateau, la graine trouve un trou.",
            "copain|La feuille est arrivée au bord.",
            "enfant-f|Puis on a planté, tout petit.",
            "papa|Vous avez soufflé, d'abord.",
            "maman|La serre reste tiède, trop grise.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|On rentre, les pieds mouillés.",
            "narrateur|La graine a voyagé sur la feuille bateau.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mes bottes sèchent.",
            "enfant-f|Une graine a une terre, sans lui.",
            "papa|On rentre, sans le défilé.",
            "maman|La flaque reste, trop ronde.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Raphaël viendra, une autre fois.",
            "narrateur|La graine attend dans la poche sèche.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "narrateur|Une seule graine, une seule terre.",
            "copain|Mon godet est resté à moi.",
            "enfant-f|J'ai planté à côté.",
            "papa|On rentre, les mains brunes.",
            "maman|La table garde sa terre.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Le godet et la graine se parlent.",
            "narrateur|La graine reste hors du godet trop plein.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "narrateur|Après le nid, la graine s'endort.",
            "copain|On a pressé, d'abord.",
            "enfant-f|Puis elle a une maison.",
            "papa|Vos paumes sentent la terre.",
            "maman|On rentre, trop bruns, trop contents.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Le nid reste sur la table.",
            "narrateur|La graine dort dans le nid de terre.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mes doigts sont bruns.",
            "enfant-f|Une graine a une terre, sans lui.",
            "papa|On rentre, le robinet se tait.",
            "maman|La terre reste sur la table.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Raphaël lavera, une autre fois.",
            "narrateur|La graine sèche loin du robinet.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "narrateur|Une seule graine, une seule terre.",
            "copain|Je suis resté dehors, moi.",
            "enfant-f|J'ai planté de loin.",
            "papa|On rentre, les visages secs.",
            "maman|Le bac reste trop mouillé, derrière.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Les feuilles n'ont pas tapé.",
            "narrateur|La graine reste hors des feuilles mouillées.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "narrateur|Après le basilic, la graine trouve un trou.",
            "copain|Ça piquait le nez.",
            "enfant-f|Puis on a planté, tout petit.",
            "papa|Vos manches sentent le vert.",
            "maman|On rentre, ça sent le basilic.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Les feuilles restent derrière, mouillées.",
            "narrateur|La graine sent le basilic, au chaud.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mon nez est sec, maintenant.",
            "enfant-f|Une graine a une terre, sans lui.",
            "papa|On rentre, le torchon sous le bras.",
            "maman|Les vitres restent embuées, trop grises.",
            "narrateur|La graine dort dans la terre sèche.",
            "enfant-f|Raphaël essuiera, une autre fois.",
            "narrateur|La graine sèche contre le torchon.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "narrateur|Un seul tablier, une seule plante.",
            "enfant-f|Le défilé n'est pas venu.",
            "copain|La flaque m'a gardé.",
            "papa|On rentre, les bottes sont lourdes.",
            "maman|Ça sent le basilic, dehors.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|La plante a bu, tout petit.",
            "narrateur|Un pois blanc sèche au bord de l'eau.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "narrateur|Après le bateau, un pois blanc sèche.",
            "copain|La feuille est arrivée au bord.",
            "enfant-f|Puis on a arrosé une plante.",
            "papa|Vous avez soufflé, d'abord.",
            "maman|La serre reste tiède, trop grise.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|On rentre, les pieds mouillés.",
            "narrateur|Un pois blanc porte une feuille verte.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mes bottes sèchent.",
            "enfant-f|Une plante a bu, sans lui.",
            "papa|On rentre, sans le défilé.",
            "maman|La flaque reste, trop ronde.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|Raphaël viendra, une autre fois.",
            "narrateur|Un pois blanc sèche près des bottes.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "narrateur|Un seul tablier, une seule plante.",
            "copain|Mon godet est resté à moi.",
            "enfant-f|J'ai arrosé à côté.",
            "papa|On rentre, les mains brunes.",
            "maman|La table garde sa terre.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|Le godet et les pois se parlent.",
            "narrateur|Un pois blanc porte un grain brun.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "narrateur|Après le nid, un pois blanc sèche.",
            "copain|On a pressé, d'abord.",
            "enfant-f|Puis une plante a bu.",
            "papa|Vos paumes sentent la terre.",
            "maman|On rentre, trop bruns, trop contents.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|Le nid reste sur la table.",
            "narrateur|Un pois blanc garde la terre du nid.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mes doigts sont bruns.",
            "enfant-f|Une plante a bu, sans lui.",
            "papa|On rentre, le robinet se tait.",
            "maman|La terre reste sur la table.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|Raphaël lavera, une autre fois.",
            "narrateur|Un pois blanc sèche sous le robinet.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "narrateur|Un seul tablier, une seule plante.",
            "copain|Je suis resté dehors, moi.",
            "enfant-f|J'ai arrosé de loin.",
            "papa|On rentre, les visages secs.",
            "maman|Le bac reste trop mouillé, derrière.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|Les feuilles n'ont pas tapé.",
            "narrateur|Un pois blanc reste hors des feuilles.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "narrateur|Après le basilic, un pois blanc sèche.",
            "copain|Ça piquait le nez.",
            "enfant-f|Puis une plante a bu.",
            "papa|Vos manches sentent le vert.",
            "maman|On rentre, ça sent le basilic.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|Les feuilles restent derrière, mouillées.",
            "narrateur|Un pois blanc sent le basilic, lui aussi.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "narrateur|Plus tard n'est pas là, pas tout de suite.",
            "copain|Mon nez est sec, maintenant.",
            "enfant-f|Une plante a bu, sans lui.",
            "papa|On rentre, le torchon sous le bras.",
            "maman|Les vitres restent embuées, trop grises.",
            "narrateur|Le tablier à pois sent le basilic.",
            "enfant-f|Raphaël essuiera, une autre fois.",
            "narrateur|Un pois blanc brille, essuyé par le torchon.",
        ]
    ),
}

T2_SONS = {1: "flaque,pas", 2: "terre,godet", 3: "feuilles"}
FIN_SONS = {1: "goutte,porte", 2: "terre,porte", 3: "tissu,porte"}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple] = {}

    scripts["CHK_T0000_P0000"] = (
        OPENING,
        "opening",
        "pluie-legere,goutte",
        {"emphasis": "anneau de zinc"},
    )
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "l'arrosoir rouge",
            "option_2_label": "la graine",
            "option_3_label": "le tablier à pois",
        },
    )

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
                "engine_ok_text": "Oui, c'est ça.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["ans"],
            },
        )
        scripts[f"{base}_C0001"] = (
            t1["confirm"],
            "confirm",
            t1["sons"],
            {"emphasis": "anneau de zinc"},
        )
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": "l'allée",
                "option_2_label": "la table",
                "option_3_label": "le bac",
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                T2_SCENE[(a, b)],
                "obstacle",
                T2_SONS[b],
                {"emphasis": "Raphaël"},
            )
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_Q[b],
                "choice",
                "",
                {
                    "option_1_label": T3_LABS[b][0],
                    "option_2_label": T3_LABS[b][1],
                    "option_3_label": T3_LABS[b][2],
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    RES[(a, b, c)],
                    "resolution",
                    T2_SONS[b],
                    {"emphasis": T3_EMP[b][c]},
                )
                scripts[f"{leaf3}_F0001"] = (
                    FIN[(a, b, c)],
                    "ending",
                    FIN_SONS[b],
                    {"emphasis": "anneau de zinc", "note": ending_note(a, b, c)},
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
        if not ch.get("text_xai_tags") or ch["text_xai_tags"] == ch["text"]:
            raise SystemExit(f"{ch['chunk_id']}: text_xai_tags = text")
        if not str(ch.get("text_ssml") or "").startswith("<speak>"):
            raise SystemExit(f"{ch['chunk_id']}: SSML manquant")
        if "arc=" not in (ch.get("notes") or ""):
            raise SystemExit(f"{ch['chunk_id']}: notes manquantes")
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

    blob = "\n".join(c["script"] for c in chunks).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in chunks
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "inviter sans forcer",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "merle",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "zoé",
        "zoe",
        "tom ",
        "lina",
        "iris",
        "léa",
        "lea ",
        "sami",
        "jules",
        "pommier",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
        "après la sieste",
        "panier rouge",
        "figuier",
        "poupée",
        "poisson",
        "fort de coussins",
        "wagon",
        "il faut attendre",
        "fenêtre",
        "cactus",
        "rebord",
        "radiateur",
        "marque fine",
        "ombre-flèche",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "croissant",
        "virgule d'or",
        "œillet de cuivre",
        "perle de verre",
        "bouton de nacre",
        "nœud de raphia",
        "pois ivoire",
        "grain de savon",
        "grain de vanille",
        "pastille de colle",
        "grain de son",
        "bouton de lavande",
        "capuchon",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob or "raphaël" not in blob:
        raise SystemExit(f"{SID}: troupe Chouchou/Raphaël absente")
    if "anneau de zinc" not in blob:
        raise SystemExit(f"{SID}: indice anneau de zinc absent")
    n_enc = len(re.findall(r"\bencore\b", blob))
    n_dej = len(re.findall(r"\bd[ée]jà\b", blob))
    if n_enc or n_dej:
        raise SystemExit(f"{SID} tics encore={n_enc} déjà={n_dej}")
    for c in chunks:
        if not c.get("text_xai_tags") or c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")
        if not str(c.get("text_ssml") or "").startswith("<speak>"):
            raise SystemExit(f"{c['chunk_id']}: SSML manquant")
        if "arc=" not in (c.get("notes") or ""):
            raise SystemExit(f"{c['chunk_id']}: notes manquantes")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
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

    ws = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(ws)} max={max(ws)} moy={sum(ws)//len(ws)}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"""# {SID} — {TITLE}

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Après la pluie, la serre fume derrière la maison. Chouchou connaît chaque planche ; un détail paraît nouveau : un anneau de zinc brille sur le bec de l'arrosoir rouge. Elle veut arroser avec Raphaël, avant que le soleil sèche tout. Elle appelle trop vite : il ne vient pas. Elle prend d'abord l'arrosoir rouge, la graine ou le tablier à pois ; les trois partent. À l'allée la flaque le retient, à la table le godet déborde, au bac il court trop. Elle refuse de foncer. L'anneau de zinc du début revient. Elle accepte son non, son autre idée, ou plus tard.

## Vécu

Chouchou propose, Raphaël prend son temps ou pose sa limite. Le silence compte. T1 = arrosoir rouge / graine / tablier à pois (équipement non retiré). T2 = allée (flaque) / table (godet trop plein) / bac (Raphaël trop vite). T3 = bord, feuille, bottes ; godet, terre, robinet ; pas, basilic, torchon. La leçon DIF.BES.002 se voit : elle n'insiste pas. L'anneau de zinc de l'ouverture est payé au climax. Un merci de papa, lié à la porte tenue.

## Vu et corrigé

- Titre noyau conservé. Troupe D16 : Chouchou, Raphaël, papa, maman. N1 ≤ 10.
- 86 nœuds, graphe et libellés d'options conservés.
- 27 fins textuellement distinctes, 27 résolutions distinctes, 27 dernières images.
- Première tentative échoue (appel trop vite, puis lieu choisi). Chaque choix change l'obstacle, le climax, la dernière image.
- Indice unique : anneau de zinc (pas ancre, étoile, fil pâle, croissant, virgule, œillet, perle, nacre, raphia, pois ivoire, grain, pastille, capuchon, marque fine, ombre-flèche, tache).
- Monde serre / allée / table / bac, distinct de TREE-DIF-059 (plantes à la fenêtre).
- TTS par fonction (ouverture, choix, indice, action, obstacle, résolution, retour).
- `slow` réservé aux choix, à l'indice et aux fins.
- Tics « tout doux / encore / déjà / tout calme » interdits. Slogan « Inviter sans forcer » jeté.
- Chemins : {min(ws)}–{max(ws)} mots (moyenne {sum(ws)//len(ws)}). `check()` OK. Pas d'apply.

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. Adulte conversationnel, pas maître. Obstacle en `low-pitch` ; fins `soft` / `slow` / `low-pitch`. Deux rythmes : elle propose, il pose sa limite.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
