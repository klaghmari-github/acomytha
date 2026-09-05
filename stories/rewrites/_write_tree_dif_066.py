#!/usr/bin/env python3
"""TREE-DIF-066 — La petite valise d'Amir, dans le grenier (N2, DIF.COR.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-066"
N2 = LIMITS["N2"]
TITLE = "La petite valise d'Amir, dans le grenier"
CHARS = "Amir, Nina, papa, maman"
SETTING = "grenier de la maison du village : lucarne, caisses, escalier, malle"
FIL = (
    "La trappe du grenier gémit, prête à se fermer. "
    "Sur la poignée de la petite valise, un grain de toile tient. "
    "Amir veut descendre la petite valise à deux, avec Nina, avant la trappe. "
    "Nina veut rester dans la malle. Il tire trop vite : elle ne vient pas. "
    "Il prend d'abord la valise à pois, la valise en carton ou la cordelette ; les trois partent. "
    "À la lucarne elle veut les toits, entre les caisses elle fouille, à l'escalier elle s'assoit. "
    "Il refuse de foncer. Le grain de toile du début revient. "
    "Ils descendent à deux. Le grain voyage."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de toile",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_trappe_veut_se_fermer_le_grain_tient; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="valise",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="grain de toile",
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent_nina_reste_en_retard; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_partir_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=nina_pose_sa_limite_le_grain_glisse; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de toile",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=ils_font_a_deux_le_grain_revient; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de toile",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_petite_valise_est_en_bas_le_grain_a_voyagé; tempo=posé; sourire=léger; respiration=ample",
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
        f"destinataire=enfant; sous_texte=le_grain_de_toile_a_voyagé; "
        f"tempo={times[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|La trappe du grenier gémit, comme une bouche qui se ferme.",
        "narrateur|Un rai de soleil tient la poussière, immobile.",
        "narrateur|Ça sent le bois chaud, et le linge trop vieux.",
        "papa|La malle a grincé, tu as entendu ?",
        "enfant-m|Elle a bougé, toute seule.",
        "maman|C'est le bois, il travaille.",
        "narrateur|Nina est accroupie, le nez dans la malle.",
        "narrateur|En ce moment, Amir touche la petite valise à pois.",
        "narrateur|Sur la poignée, un grain de toile tient, pâle.",
        "enfant-m|Je veux la petite, pour le pique-nique.",
        "copine|Moi, je reste dans la malle.",
        "papa|Le panier attend, en bas, Nina.",
        "enfant-m|On descend à deux, avant la trappe !",
        "narrateur|Il tire trop vite, tout seul.",
        "narrateur|Nina ne bouge pas.",
        "narrateur|Le sourire d'Amir disparaît.",
        "narrateur|Dans sa poitrine, ça se serre.",
        "enfant-m|Tu ne viens pas ?",
        "papa|Merci, tu as tenu la trappe.",
        "maman|Les trois affaires attendent, près de la malle.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Près de la malle, trois affaires attendent.",
        "narrateur|La valise à pois, la valise en carton, la cordelette.",
        "maman|Tu prends quoi d'abord, Amir ?",
    ]
)

T1 = {
    1: dict(
        lab="la valise à pois",
        ans="pois",
        acc="pois | valise à pois | la valise à pois | petite valise | la petite",
        retry="Amir a pris la valise à pois.",
        sons="valise,tissu",
        emp="valise à pois",
        passage=vet(
            [
                "narrateur|Amir attrape la valise à pois, trop vite.",
                "enfant-m|Elle est légère, celle-là.",
                "narrateur|Le grain de toile penche, presque tombé.",
                "maman|Tiens la poignée, pas trop fort.",
                "enfant-m|Il a bougé !",
                "papa|Voici la cordelette, accroche-la.",
                "narrateur|Maman glisse aussi la valise en carton.",
                "narrateur|Les trois affaires collent contre Amir.",
                "copine|La malle, moi, après.",
                "enfant-m|Nina, on descend à deux.",
                "papa|Tu lui proposes, sans la tirer ?",
                "enfant-m|Oui, papa.",
                "narrateur|Il tient la poignée, plus lentement.",
                "maman|Les trois affaires partent ensemble.",
            ]
        ),
        question=vet(
            [
                "narrateur|La valise à pois pèse, contre lui.",
                "maman|Il a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|La valise à pois.",
                "maman|Oui, la petite.",
                "narrateur|Le grain de toile se recale, pâle.",
                "enfant-m|On va jusqu'à Nina.",
                "papa|La trappe gémit, un peu.",
                "enfant-m|Oui, papa, j'y vais.",
                "narrateur|Le carton frotte sa manche, sec.",
                "papa|On y va, sans la tirer ?",
                "enfant-m|Sans la tirer.",
                "maman|Les pois sentent le bois chaud.",
            ]
        ),
    ),
    2: dict(
        lab="la valise en carton",
        ans="carton",
        acc="carton | valise en carton | la valise en carton | grande valise | la grande",
        retry="Amir a pris la valise en carton.",
        sons="carton,bois",
        emp="valise en carton",
        passage=vet(
            [
                "narrateur|Amir tire la valise en carton, trop lourde.",
                "enfant-m|Elle ne vient pas !",
                "narrateur|Le carton râpe le plancher, sec.",
                "papa|Laisse-la, prends aussi la petite.",
                "narrateur|Maman noue la cordelette au poignet.",
                "enfant-m|Elle pique !",
                "maman|La petite t'attend, près de la malle.",
                "narrateur|Le grain de toile brille, sur la poignée.",
                "narrateur|Amir serre les trois contre son ventre.",
                "copine|La malle, moi, après.",
                "enfant-m|Nina, tu portes avec moi ?",
                "papa|Tu lui proposes, sans la presser ?",
                "enfant-m|Oui.",
                "maman|Les trois affaires partent ensemble.",
            ]
        ),
        question=vet(
            [
                "narrateur|La valise en carton pèse au poignet.",
                "papa|Il a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|La valise en carton.",
                "papa|Oui, la grande.",
                "narrateur|Le grain de toile reste sur la petite.",
                "enfant-m|On va jusqu'à Nina.",
                "maman|Ça sent le bois, ici.",
                "enfant-m|Oui, maman.",
                "narrateur|La cordelette chauffe contre son poignet.",
                "papa|On y va, sans la presser ?",
                "enfant-m|Sans la presser.",
                "papa|Le carton reste trop large, trop loin.",
            ]
        ),
    ),
    3: dict(
        lab="la cordelette",
        ans="cordelette",
        acc="cordelette | la cordelette | corde | la corde | le fil",
        retry="Amir a pris la cordelette.",
        sons="corde",
        emp="cordelette",
        passage=vet(
            [
                "narrateur|Amir lève la cordelette, trop vite.",
                "enfant-m|Elle va tirer la valise.",
                "maman|Pas trop fort, juste un fil.",
                "narrateur|Le nœud glisse, puis se tait.",
                "enfant-m|Il glisse !",
                "papa|Voici la petite, et la grande.",
                "narrateur|Il les glisse contre son genou.",
                "narrateur|Le grain de toile frôle le fil, pâle.",
                "copine|La malle, moi, après.",
                "enfant-m|Nina, tu tiens le fil ?",
                "papa|Tu lui proposes, sans la tirer ?",
                "enfant-m|Oui.",
                "narrateur|Il noue à nouveau, plus lentement.",
                "maman|La cordelette tient, bien nouée.",
            ]
        ),
        question=vet(
            [
                "narrateur|La cordelette reste nouée, au poignet.",
                "maman|Il a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|La cordelette.",
                "maman|Oui, le fil.",
                "narrateur|Le grain de toile frôle le nœud.",
                "enfant-m|Nina va voir le fil.",
                "papa|On avance, tous les trois ?",
                "enfant-m|Oui.",
                "narrateur|La petite valise chauffe contre son genou.",
                "maman|On y va, sans la tirer ?",
                "enfant-m|Sans la tirer.",
                "papa|Le nœud simple brille au poignet.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Nina reste près de la malle, trop loin.",
            "maman|La lucarne est trop basse, trop petite.",
            "narrateur|Les caisses laissent un trou étroit.",
            "papa|L'escalier a une marche trop haute.",
            "papa|On va vers où, Amir ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le carton pèse, trop large, trop loin.",
            "maman|La lucarne est trop basse, trop petite.",
            "narrateur|Les caisses laissent un trou étroit.",
            "papa|L'escalier a une marche trop haute.",
            "maman|On va vers où, Amir ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le fil appuie contre son poignet.",
            "papa|La lucarne est trop basse, trop petite.",
            "narrateur|Les caisses laissent un trou étroit.",
            "maman|L'escalier a une marche trop haute.",
            "papa|On va vers où, Amir ?",
        ]
    ),
}

T2_SCENE = {
    (1, 1): vet(
        [
            "narrateur|La valise à pois penche vers la lucarne.",
            "narrateur|Nina a le nez contre le verre.",
            "enfant-m|On descend, viens !",
            "copine|Les toits, moi.",
            "narrateur|Il tire sa manche, trop vite.",
            "narrateur|Un souffle entre, froid.",
            "narrateur|Le grain de toile glisse vers une fente.",
            "copine|Non.",
            "narrateur|Nina ne dit plus rien.",
            "narrateur|Le sourire d'Amir disparaît.",
            "enfant-m|Tu ne veux pas ?",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-m|J'écoute.",
            "narrateur|S'il force, le grain tombe.",
            "narrateur|Il regarde le grain, sans foncer.",
        ]
    ),
    (1, 2): vet(
        [
            "narrateur|Les pois frottent une caisse, trop sèche.",
            "narrateur|Nina fouille entre les cartons.",
            "enfant-m|Tu portes avec moi ?",
            "copine|Les chapeaux, d'abord.",
            "narrateur|Il pousse le carton dans le trou.",
            "narrateur|Le carton se coince, trop large.",
            "narrateur|La poussière cache le grain de toile.",
            "copine|Le trou, pas ça.",
            "narrateur|Elle ne lâche pas un chapeau.",
            "narrateur|L'envie serre la poitrine d'Amir.",
            "enfant-m|Elle est trop large !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-m|J'écoute.",
            "narrateur|S'il force, le grain disparaît.",
            "narrateur|Il recule le carton, sans pousser.",
        ]
    ),
    (1, 3): vet(
        [
            "narrateur|Les pois pendent au-dessus de la marche.",
            "narrateur|Nina s'assoit, sur la marche du haut.",
            "enfant-m|On descend, tout de suite !",
            "copine|Ici, moi.",
            "narrateur|Il descend trop vite, tout seul.",
            "narrateur|La valise tape la marche, toc.",
            "narrateur|Le grain de toile penche vers le trou.",
            "copine|Pas tout seul.",
            "narrateur|Elle reste assise, les lèvres fermées.",
            "narrateur|Le sourire d'Amir disparaît.",
            "enfant-m|Tu ne viens pas ?",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|La marche reste trop haute.",
            "enfant-m|J'écoute.",
            "narrateur|S'il saute, le grain tombe.",
            "narrateur|Il recule d'un pas, sans foncer.",
        ]
    ),
    (2, 1): vet(
        [
            "narrateur|Le carton bute sous la lucarne, trop haut.",
            "narrateur|Nina a le nez contre le verre.",
            "enfant-m|On passe sous le toit ?",
            "copine|Les toits, d'abord.",
            "narrateur|Il pousse le carton, trop près du verre.",
            "narrateur|Le bois touche, trop serré, trop bas.",
            "narrateur|Le grain de toile glisse vers une fente.",
            "copine|Non.",
            "narrateur|Nina secoue la tête, sans mot.",
            "narrateur|Amir serre le carton, les joues chaudes.",
            "enfant-m|Elle ne passe pas !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-m|J'écoute.",
            "narrateur|S'il force, le grain tombe.",
            "narrateur|Il pose le carton, sans foncer.",
        ]
    ),
    (2, 2): vet(
        [
            "narrateur|Le carton râpe les caisses, trop large.",
            "narrateur|Nina presse un chapeau trop vieux.",
            "enfant-m|On passe par le trou ?",
            "copine|Mes mains collent trop.",
            "narrateur|Il pousse le carton vers le passage.",
            "narrateur|Une caisse racle, puis une autre.",
            "narrateur|La poussière cache le grain de toile.",
            "copine|Le chapeau, à moi.",
            "narrateur|Un peu de poussière tombe sur ses pieds.",
            "narrateur|L'inquiétude bouscule l'envie, au ventre.",
            "enfant-m|Je ne vois plus le grain !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-m|J'écoute.",
            "narrateur|S'il pousse, le grain se perd.",
            "narrateur|Il recule le carton, sans jeter.",
        ]
    ),
    (2, 3): vet(
        [
            "narrateur|Le carton pèse au-dessus de la marche.",
            "narrateur|Nina s'assoit, trop loin de lui.",
            "enfant-m|Tu prends une poignée ?",
            "copine|Pas là-dedans.",
            "narrateur|Il descend trop vite, le carton penche.",
            "narrateur|Un pied cherche, trop bas, trop court.",
            "narrateur|Le grain de toile penche vers le trou.",
            "copine|Ça pèse !",
            "narrateur|Elle recule, les lèvres fermées.",
            "narrateur|Amir referme les doigts, le cœur serré.",
            "enfant-m|Elle est trop lourde !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|La marche reste trop haute.",
            "enfant-m|J'écoute.",
            "narrateur|S'il saute, le grain se perd.",
            "narrateur|Il pose le carton, sans foncer.",
        ]
    ),
    (3, 1): vet(
        [
            "narrateur|La cordelette se penche vers le verre.",
            "narrateur|Nina a le nez contre la lucarne.",
            "enfant-m|Tu tiens le fil ?",
            "copine|Les toits restent ici.",
            "narrateur|Il tire trop vite, près du verre.",
            "narrateur|Le nœud glisse, trop fort.",
            "narrateur|Le grain de toile tremble, dans le rai.",
            "copine|Non.",
            "narrateur|Nina ne dit plus rien.",
            "narrateur|Le sourire d'Amir disparaît.",
            "enfant-m|Tu ne veux pas le fil ?",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Elle ne bouge pas.",
            "enfant-m|J'écoute.",
            "narrateur|S'il tire, le grain tombe.",
            "narrateur|Il relâche le fil, sans foncer.",
        ]
    ),
    (3, 2): vet(
        [
            "narrateur|Le fil se tache de poussière, trop gris.",
            "narrateur|Nina a de la poussière aux doigts.",
            "enfant-m|Tu tires avec moi ?",
            "copine|Mes mains collent trop.",
            "narrateur|Il noue trop vite, trop près des caisses.",
            "narrateur|Le carton se coince, trop large.",
            "narrateur|La poussière cache le grain de toile.",
            "copine|Le chapeau, d'abord.",
            "narrateur|La poussière tache le nœud, d'un coup.",
            "narrateur|Amir baisse les yeux, la gorge serrée.",
            "enfant-m|Je ne vois plus rien !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-m|J'écoute.",
            "narrateur|S'il tire, le grain se salit.",
            "narrateur|Il recule le fil, sans nouer.",
        ]
    ),
    (3, 3): vet(
        [
            "narrateur|Le fil pend au-dessus de la marche.",
            "narrateur|Nina s'assoit, trop près du trou.",
            "enfant-m|Tu viens, marche après marche ?",
            "copine|Pas tout de suite.",
            "narrateur|Il descend trop vite, le fil s'accroche.",
            "narrateur|Une marche sonne, trop sèche.",
            "narrateur|Le grain de toile penche vers le trou.",
            "copine|Le fil accroche !",
            "narrateur|Elle recule, les lèvres fermées.",
            "narrateur|Le sourire d'Amir disparaît.",
            "enfant-m|Le fil s'est accroché !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-m|J'écoute.",
            "narrateur|S'il tire, le grain tombe.",
            "narrateur|Il recule d'un pas, sans foncer.",
        ]
    ),
}

T3_LABS = {
    1: ("la petite valise", "le plancher", "la cordelette"),
    2: ("le passage", "les poignées", "la poussière"),
    3: ("la rampe", "le palier", "la petite valise"),
}

T3_Q = {
    1: vet(
        [
            "narrateur|La lucarne tient Nina, sans un mot.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "maman|Tu vois le grain, toi ?",
            "papa|La petite valise, le plancher, ou la cordelette ?",
        ]
    ),
    2: vet(
        [
            "narrateur|La poussière colle aux doigts, trop grise.",
            "narrateur|Amir refuse de pousser, cette fois.",
            "papa|Tu vois le grain, toi ?",
            "maman|Le passage, les poignées, ou la poussière ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La marche reste trop haute, trop sèche.",
            "narrateur|Amir refuse de sauter, cette fois.",
            "maman|Tu vois le grain, toi ?",
            "papa|La rampe, le palier, ou la petite valise ?",
        ]
    ),
}

T3_EMP = {
    1: {1: "petite valise", 2: "plancher", 3: "cordelette"},
    2: {1: "passage", 2: "poignées", 3: "poussière"},
    3: {1: "rampe", 2: "palier", 3: "petite valise"},
}

RES = {
    (1, 1, 1): vet(
        [
            "enfant-m|D'accord, on prend la petite.",
            "narrateur|Il pose le carton, trop large, trop haut.",
            "narrateur|Il refuse de forcer sous le toit.",
            "narrateur|Le grain de toile reste au sec.",
            "copine|Je regarde, un peu.",
            "enfant-m|Puis tu tiens une poignée.",
            "narrateur|Deux mains, une petite valise.",
            "papa|La lucarne lui reste, un moment.",
            "maman|Ta petite valise est restée légère.",
            "enfant-m|C'est bien, comme ça.",
            "narrateur|Papa ne dit pas comment faire.",
            "narrateur|Le grain de toile a parlé, sans mot.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "copine|À plat, plutôt, sur le plancher.",
            "enfant-m|D'accord, on glisse.",
            "narrateur|Il refuse de lever sous le toit.",
            "narrateur|Les pois glissent, tout bas, sous la poutre.",
            "narrateur|Le grain de toile se mire dans le rai.",
            "copine|Elle passe !",
            "enfant-m|Toi, tu pousses, moi je tire.",
            "narrateur|Le carton reste debout, trop haut.",
            "papa|Vous avez glissé, sans la lever.",
            "maman|La petite attend, plus loin.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|Le grain de toile a guidé le plat.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "copine|Le fil, moi je le tiens ici.",
            "enfant-m|D'accord, tu restes un peu.",
            "narrateur|Il noue le fil à la petite valise.",
            "narrateur|Il refuse de la jeter sous le toit.",
            "copine|Je tire, tout petit.",
            "enfant-m|Le carton reste, trop large.",
            "narrateur|Le grain de toile avance au bout du fil.",
            "papa|Le fil a tiré la petite.",
            "maman|La lucarne n'a plus coincé.",
            "narrateur|Le nœud a tenu, sans se jeter.",
            "enfant-m|Tu es de l'autre côté.",
            "narrateur|Le grain de toile a passé le rai.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "enfant-m|D'accord, on mesure le trou.",
            "copine|Le chapeau, c'est à moi.",
            "narrateur|La petite valise reste à côté.",
            "narrateur|Il refuse de pousser le carton.",
            "narrateur|Le grain de toile reparaît, hors de la poussière.",
            "narrateur|Le carton est trop large, trop sec.",
            "enfant-m|Les pois passent, juste.",
            "narrateur|Nina lâche le chapeau, un instant.",
            "papa|Le trou était de sa taille.",
            "maman|Le carton est resté entre les caisses.",
            "enfant-m|Deux jeux, l'un près de l'autre.",
            "narrateur|Le grain de toile a dit : par là.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "copine|Les poignées, plutôt, à deux.",
            "enfant-m|D'accord, tu prends celle-là.",
            "narrateur|Deux paumes collent près des pois.",
            "narrateur|Il refuse de tirer tout seul.",
            "narrateur|Le grain de toile reste entre leurs mains.",
            "narrateur|Ils lèvent la petite, pas la grande.",
            "copine|Elle est légère !",
            "enfant-m|Le carton reste, trop large.",
            "papa|Vous n'avez pas tiré tout seuls.",
            "maman|Les poignées ont parlé, à deux.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|Le grain de toile a vu les deux mains.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "copine|La poussière, d'abord, j'attends.",
            "enfant-m|D'accord, on attend.",
            "narrateur|La petite valise attend près des caisses.",
            "narrateur|Il refuse de la retenir de force.",
            "narrateur|La poussière retombe, une fois, puis plus.",
            "copine|Je vois le grain !",
            "enfant-m|Le trou est net, maintenant.",
            "narrateur|Le grain de toile cligne, hors du gris.",
            "papa|Le rai est redevenu net.",
            "maman|Les caisses gardent leur poussière.",
            "enfant-m|Quand tes mains seront prêtes.",
            "narrateur|Le grain de toile a attendu le rai.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "enfant-m|D'accord, on glisse le long de la rampe.",
            "copine|Je tiens le bois, moi.",
            "narrateur|La petite valise recule d'un pas.",
            "narrateur|Il refuse de sauter la marche.",
            "narrateur|Le grain de toile sort de l'ombre.",
            "narrateur|Ils glissent, côte à côte, marche après marche.",
            "enfant-m|Le carton reste en haut, trop lourd.",
            "narrateur|La petite glisse, sans se jeter.",
            "papa|La rampe a tenu la petite.",
            "maman|Ton pied n'a pas sauté.",
            "enfant-m|De loin, ça suffit.",
            "narrateur|Le grain de toile a choisi la rampe.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "copine|Le palier, plutôt, on s'arrête.",
            "enfant-m|D'accord, on pose, d'abord.",
            "narrateur|La petite valise s'arrête sur le palier.",
            "narrateur|Il refuse de foncer dans le trou.",
            "narrateur|Le grain de toile frôle une marche.",
            "narrateur|Papa se met plus bas, une marche.",
            "copine|Je te la tends.",
            "enfant-m|Puis tu descends, tout petit.",
            "papa|Vous n'avez pas sauté la marche.",
            "maman|Le palier vous a aidés.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|Le grain de toile a suivi le palier.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "copine|La petite, elle tient dans tes mains.",
            "enfant-m|D'accord, celle-là.",
            "narrateur|Il descend la petite, une marche, puis l'autre.",
            "narrateur|Il refuse de porter le carton trop lourd.",
            "narrateur|Nina tient la rampe, sans parler fort.",
            "copine|Je viens, derrière.",
            "enfant-m|Tu restes avec moi.",
            "narrateur|Le grain de toile descend, marche après marche.",
            "papa|La petite tenait dans tes mains.",
            "maman|La grande reste au grenier, trop haute.",
            "enfant-m|Quand tu seras prête.",
            "narrateur|Le grain de toile a tenu dans la paume.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "enfant-m|D'accord, on pose la grande.",
            "narrateur|Il pose le carton, trop large, trop haut.",
            "narrateur|Il refuse de forcer sous le toit.",
            "narrateur|Le grain de toile reste au sec.",
            "copine|Je reste ici, un peu.",
            "enfant-m|La petite, elle passe.",
            "narrateur|Deux mains, une petite valise.",
            "papa|La lucarne lui reste, à elle.",
            "maman|Le carton est resté trop haut.",
            "enfant-m|C'est bien, comme ça.",
            "narrateur|Papa ne dit pas comment faire.",
            "narrateur|Le grain de toile a choisi la petite.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "copine|À plat, plutôt, sous le toit.",
            "enfant-m|D'accord, on couche la petite.",
            "narrateur|Il refuse de lever le carton.",
            "narrateur|La petite glisse, tout bas, sous la poutre.",
            "narrateur|Le grain de toile se mire dans le rai.",
            "copine|Elle passe, celle-là !",
            "enfant-m|Toi, tu pousses, moi je tire.",
            "narrateur|Le carton reste debout, trop haut.",
            "papa|Vous avez glissé, sans la lever.",
            "maman|Au sol, ça passait mieux.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|Le grain de toile a guidé le sol.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "copine|Le fil, pas le carton trop large.",
            "enfant-m|D'accord, on noue la petite.",
            "narrateur|Il noue le fil, pas au carton trop large.",
            "narrateur|Il refuse de forcer sous le toit.",
            "copine|Je tire, tout petit.",
            "enfant-m|Le carton reste, trop large.",
            "narrateur|Le grain de toile avance au bout du fil.",
            "papa|Le fil a tiré la petite.",
            "maman|La lucarne n'a plus coincé.",
            "narrateur|Le nœud a tenu, sans se jeter.",
            "enfant-m|Tu es de l'autre côté.",
            "narrateur|Le grain de toile a suivi le fil.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "enfant-m|D'accord, on compare le trou.",
            "copine|Le chapeau, c'est à moi.",
            "narrateur|Il compare le carton, trop large, au trou.",
            "narrateur|Il refuse de pousser la grande.",
            "narrateur|Le grain de toile reparaît, hors de la poussière.",
            "narrateur|Le carton est trop large, trop sec.",
            "enfant-m|La petite passe entre les caisses, juste.",
            "narrateur|Nina lâche le chapeau, un instant.",
            "papa|Le trou était de sa taille.",
            "maman|Le carton est resté trop large.",
            "enfant-m|Maintenant, tu me suis.",
            "narrateur|Le grain de toile a mesuré le trou.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "copine|Les poignées, à deux, pas tout seul.",
            "enfant-m|D'accord, tu prends celle-là.",
            "narrateur|Ils laissent le carton, trop large, trop lourd.",
            "narrateur|Il refuse de tirer tout seul.",
            "narrateur|Le grain de toile reste entre leurs mains.",
            "narrateur|Ils lèvent la petite, pas la grande.",
            "copine|Elle est légère !",
            "enfant-m|C'est pour le pique-nique.",
            "papa|Tu n'as pas tiré tout seul.",
            "maman|À deux, la petite avançait.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|Le grain de toile a vu les poignées.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "copine|La poussière, d'abord, j'attends.",
            "enfant-m|D'accord, on s'arrête.",
            "narrateur|Amir s'arrête, le carton trop gris.",
            "narrateur|Il refuse de pousser dans le gris.",
            "narrateur|La poussière retombe, une fois, puis plus.",
            "copine|Je vois le grain !",
            "enfant-m|Je vois le trou, maintenant.",
            "narrateur|Le grain de toile cligne, hors du gris.",
            "papa|Le rai est redevenu net.",
            "maman|Le trou était de sa taille.",
            "enfant-m|Quand tes mains seront prêtes.",
            "narrateur|Le grain de toile a attendu le net.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "enfant-m|D'accord, on glisse le long de la rampe.",
            "copine|Je tiens le bois, moi.",
            "narrateur|Il pose le carton, trop lourd, trop haut.",
            "narrateur|Il refuse de sauter la marche.",
            "narrateur|Le grain de toile sort de l'ombre.",
            "narrateur|La petite glisse, marche après marche.",
            "enfant-m|Le carton reste en haut, trop lourd.",
            "narrateur|Nina tient la rampe, sans parler.",
            "papa|La rampe a tenu la petite.",
            "maman|Tu as glissé, sans la jeter.",
            "enfant-m|Maintenant, tu peux rester.",
            "narrateur|Le grain de toile a suivi le bois.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "copine|Le palier, on s'arrête.",
            "enfant-m|D'accord, on pose, un moment.",
            "narrateur|Ils posent le carton, trop lourd, un moment.",
            "narrateur|Il refuse de foncer dans le trou.",
            "narrateur|Le grain de toile frôle une marche.",
            "narrateur|Papa se met plus bas, une marche.",
            "copine|Je te tends la petite.",
            "enfant-m|Puis tu descends, tout petit.",
            "papa|Tu n'as pas sauté la marche.",
            "maman|Le palier vous a aidés.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|Le grain de toile a posé le palier.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "copine|La petite, elle est légère.",
            "enfant-m|D'accord, celle-là.",
            "narrateur|Il laisse le carton, trop lourd pour la marche.",
            "narrateur|Il refuse de porter trop haut.",
            "narrateur|Nina tient la rampe, sans parler fort.",
            "copine|Je viens, derrière.",
            "enfant-m|Tu restes avec moi.",
            "narrateur|Le grain de toile descend, marche après marche.",
            "papa|La petite tenait dans tes mains.",
            "maman|La petite a suffi.",
            "enfant-m|Quand tu seras prête.",
            "narrateur|Le grain de toile a suffi, en bas.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "enfant-m|D'accord, on prend la petite.",
            "narrateur|Il noue le fil, puis pose la grande.",
            "narrateur|Il refuse de forcer sous le toit.",
            "narrateur|Le grain de toile reste au sec.",
            "copine|Je regarde, un peu.",
            "enfant-m|Puis tu tiens une poignée.",
            "narrateur|Deux mains, une petite valise.",
            "papa|La lucarne lui reste, un moment.",
            "maman|Le fil a tenu la petite.",
            "enfant-m|C'est bien, comme ça.",
            "narrateur|Papa ne dit pas comment faire.",
            "narrateur|Le grain de toile a parlé au fil.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "copine|À plat, plutôt, le long du plancher.",
            "enfant-m|D'accord, on glisse le fil.",
            "narrateur|Il glisse le fil le long du plancher.",
            "narrateur|Il refuse de lever sous le toit.",
            "narrateur|Le grain de toile se mire dans le rai.",
            "copine|Elle passe !",
            "enfant-m|Toi, tu pousses, moi je tire.",
            "narrateur|Le carton reste debout, trop haut.",
            "papa|Vous avez glissé, sans la lever.",
            "maman|Au sol, ça passait mieux.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|Le grain de toile a suivi le fil plat.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "copine|Le fil, moi je le serre.",
            "enfant-m|D'accord, tu serres le nœud.",
            "narrateur|Il serre le nœud sur la petite valise.",
            "narrateur|Il refuse de la jeter sous le toit.",
            "copine|Je tire, tout petit.",
            "enfant-m|Le carton reste, trop large.",
            "narrateur|Le grain de toile avance au bout du fil.",
            "papa|Le fil a tiré la petite.",
            "maman|La lucarne n'a plus coincé.",
            "narrateur|Le nœud a tenu, sans se jeter.",
            "enfant-m|Tu es de l'autre côté.",
            "narrateur|Le grain de toile a tenu le nœud.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "enfant-m|D'accord, on passe le fil, d'abord.",
            "copine|Le chapeau, c'est à moi.",
            "narrateur|Il passe le fil, puis la petite valise.",
            "narrateur|Il refuse de pousser le carton.",
            "narrateur|Le grain de toile reparaît, hors de la poussière.",
            "narrateur|Le carton est trop large, trop sec.",
            "enfant-m|Les pois passent entre les caisses, juste.",
            "narrateur|Nina lâche le chapeau, un instant.",
            "papa|Le trou était de sa taille.",
            "maman|Le fil a montré le passage.",
            "enfant-m|Maintenant, tu me suis.",
            "narrateur|Le grain de toile a passé le fil.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "copine|Les poignées, le fil les relie.",
            "enfant-m|D'accord, tu prends celle-là.",
            "narrateur|Le fil relie les deux poignées, sans forcer.",
            "narrateur|Il refuse de tirer tout seul.",
            "narrateur|Le grain de toile reste entre leurs mains.",
            "narrateur|Ils lèvent la petite, pas la grande.",
            "copine|Elle est légère !",
            "enfant-m|C'est pour le pique-nique.",
            "papa|Tu n'as pas tiré tout seul.",
            "maman|À deux, la petite avançait.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|Le grain de toile a relié les poignées.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "copine|La poussière, d'abord, j'attends.",
            "enfant-m|D'accord, on s'arrête.",
            "narrateur|Amir s'arrête, le fil trop gris.",
            "narrateur|Il refuse de tirer dans le gris.",
            "narrateur|La poussière retombe, une fois, puis plus.",
            "copine|Je vois le grain !",
            "enfant-m|Je vois, maintenant.",
            "narrateur|Le grain de toile cligne, hors du gris.",
            "papa|Le rai est redevenu net.",
            "maman|Le trou était de sa taille.",
            "enfant-m|Quand tes mains seront prêtes.",
            "narrateur|Le grain de toile a attendu le fil net.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "enfant-m|D'accord, on glisse le fil le long de la rampe.",
            "copine|Je tiens le bois, moi.",
            "narrateur|Il glisse le fil le long de la rampe.",
            "narrateur|Il refuse de sauter la marche.",
            "narrateur|Le grain de toile sort de l'ombre.",
            "narrateur|La petite glisse, marche après marche.",
            "enfant-m|Le carton reste en haut, trop lourd.",
            "narrateur|Nina tient la rampe, sans parler.",
            "papa|La rampe a tenu la petite.",
            "maman|Tu as glissé, sans la jeter.",
            "enfant-m|Maintenant, tu peux rester.",
            "narrateur|Le grain de toile a glissé le fil.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "copine|Le palier, on s'arrête.",
            "enfant-m|D'accord, on pose le fil, un moment.",
            "narrateur|Ils posent le fil sur le palier, un moment.",
            "narrateur|Il refuse de foncer dans le trou.",
            "narrateur|Le grain de toile frôle une marche.",
            "narrateur|Papa se met plus bas, une marche.",
            "copine|Je te tends la petite.",
            "enfant-m|Puis tu descends, tout petit.",
            "papa|Tu n'as pas sauté la marche.",
            "maman|Le palier vous a aidés.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|Le grain de toile a posé le fil.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "copine|La petite valise, elle est légère.",
            "enfant-m|D'accord, celle-là.",
            "narrateur|Il descend le fil, puis la petite valise.",
            "narrateur|Il refuse de porter trop haut.",
            "narrateur|Nina tient la rampe, sans parler fort.",
            "copine|Je viens, derrière.",
            "enfant-m|Tu restes avec moi.",
            "narrateur|Le grain de toile descend, marche après marche.",
            "papa|La petite tenait dans tes mains.",
            "maman|La petite a suffi.",
            "enfant-m|Quand tu seras prête.",
            "narrateur|Le grain de toile a descendu le fil.",
        ]
    ),
}

LAST = {
    (1, 1, 1): "Un pois tiède garde le grain de toile.",
    (1, 1, 2): "Le plancher lisse le grain de toile, mince.",
    (1, 1, 3): "Le nœud serre le grain de toile, sans casser.",
    (1, 2, 1): "Entre deux caisses, le grain de toile respire.",
    (1, 2, 2): "La paume de Nina tient le grain de toile.",
    (1, 2, 3): "La poussière s'écarte : le grain de toile brille.",
    (1, 3, 1): "La rampe a retenu le grain de toile.",
    (1, 3, 2): "Sur le palier, le grain de toile se tait.",
    (1, 3, 3): "Une marche sèche autour du grain de toile.",
    (2, 1, 1): "Le carton reste ; le grain de toile descend.",
    (2, 1, 2): "Sous la lucarne, le grain de toile glisse à plat.",
    (2, 1, 3): "La cordelette tire le grain de toile, bas.",
    (2, 2, 1): "Le trou laisse passer le grain de toile.",
    (2, 2, 2): "Deux poignées, un grain de toile au milieu.",
    (2, 2, 3): "Quand la poussière tombe, le grain de toile cligne.",
    (2, 3, 1): "Le long du bois, le grain de toile voyage.",
    (2, 3, 2): "Papa pose le grain de toile sur le palier.",
    (2, 3, 3): "La petite valise porte le grain de toile, en bas.",
    (3, 1, 1): "Le fil a sauvé le grain de toile, sous le toit.",
    (3, 1, 2): "À plat, le grain de toile frotte le plancher.",
    (3, 1, 3): "Le nœud du poignet garde le grain de toile.",
    (3, 2, 1): "Nina souffle : le grain de toile reparaît.",
    (3, 2, 2): "Amir et Nina lèvent le grain de toile, ensemble.",
    (3, 2, 3): "Un rai net montre le grain de toile, enfin.",
    (3, 3, 1): "La rampe chauffe le grain de toile, lentement.",
    (3, 3, 2): "Le palier garde une poussière et le grain de toile.",
    (3, 3, 3): "En bas, le grain de toile brille sur la nappe.",
}

FIN_OPEN = {
    (1, 1, 1): (
        "narrateur|La petite valise descend, sous la lucarne.",
        "enfant-m|On a pris celle qui passe.",
        "copine|J'ai vu les toits, un peu.",
        "papa|La petite passait sous le toit.",
        "maman|Le panier attend, en bas.",
        "enfant-m|On a failli tirer trop vite.",
    ),
    (1, 1, 2): (
        "narrateur|Sur le plancher, la petite valise rejoint la trappe.",
        "enfant-m|On a glissé, d'abord.",
        "copine|J'ai poussé, tout bas.",
        "papa|Tu as poussé, sans la lever.",
        "maman|Le panier sent le linge, en bas.",
        "enfant-m|On a failli buter sous le toit.",
    ),
    (1, 1, 3): (
        "narrateur|Au bout du fil, la petite valise a passé.",
        "enfant-m|J'ai tiré, tout petit.",
        "copine|Moi, j'ai tenu le nœud.",
        "papa|Le fil a tenu.",
        "maman|Le panier attend, près de la nappe.",
        "enfant-m|On a failli jeter trop fort.",
    ),
    (1, 2, 1): (
        "narrateur|Dans le passage, la petite valise a tenu.",
        "enfant-m|On a regardé le trou.",
        "copine|Mon chapeau est resté à moi.",
        "papa|Le trou était juste, pour elle.",
        "maman|Le panier chauffe, en bas.",
        "enfant-m|On a failli pousser trop large.",
    ),
    (1, 2, 2): (
        "narrateur|À deux, la petite valise a quitté les caisses.",
        "enfant-m|On a porté les poignées.",
        "copine|Une pour toi, une pour moi.",
        "papa|Tu n'as pas tiré tout seul.",
        "maman|On sent le linge, dans le panier.",
        "enfant-m|On a failli rester coincés.",
    ),
    (1, 2, 3): (
        "narrateur|Quand la poussière s'est tue, la petite a passé.",
        "enfant-m|J'ai vu le trou, après.",
        "copine|J'ai vu le grain, moi aussi.",
        "papa|Le rai est redevenu net.",
        "maman|Le panier attend, trop loin.",
        "enfant-m|On a failli perdre le grain.",
    ),
    (1, 3, 1): (
        "narrateur|Le long de la rampe, la petite valise est en bas.",
        "enfant-m|On a glissé, marche après marche.",
        "copine|J'ai tenu le bois.",
        "papa|La rampe a tenu.",
        "maman|Le panier sent le linge, tout près.",
        "enfant-m|On a failli sauter trop vite.",
    ),
    (1, 3, 2): (
        "narrateur|Du palier, la petite valise a rejoint le bas.",
        "enfant-m|On s'est arrêtés, d'abord.",
        "copine|Je te l'ai tendue.",
        "papa|Tu n'as pas sauté la marche.",
        "maman|On sent le linge, tout près.",
        "enfant-m|On a failli tomber dans le trou.",
    ),
    (1, 3, 3): (
        "narrateur|Tout légère, la petite valise est en bas.",
        "enfant-m|On a pris celle qu'on porte.",
        "copine|Je suis venue, derrière.",
        "papa|La petite tenait dans tes mains.",
        "maman|Le panier est prêt, on descend.",
        "enfant-m|On a failli porter trop lourd.",
    ),
}


def fin_lines(a: int, b: int, c: int) -> list[str]:
    key = (1, b, c)
    head = FIN_OPEN[key]
    extra = {
        1: "narrateur|Les pois gardent un peu de poussière.",
        2: "narrateur|Le carton reste au grenier, trop lourd.",
        3: "narrateur|La cordelette reste nouée, tout bas.",
    }[a]
    last = f"narrateur|{LAST[(a, b, c)]}"
    # vary a middle beat so 27 texts differ even when head is shared by T2/T3
    mid = {
        1: "enfant-m|Le grain est resté, sur la poignée.",
        2: "enfant-m|Le grain a voyagé, malgré le carton.",
        3: "enfant-m|Le grain a suivi le fil, jusqu'en bas.",
    }[a]
    return vet(list(head) + [extra, mid, last])


T2_SONS = {1: "lucarne,vent", 2: "caisses,poussiere", 3: "marches,bois"}
FIN_SONS = {1: "trappe,panier", 2: "caisses,panier", 3: "marches,panier"}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "trappe,bois,poussiere", {})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "la valise à pois",
            "option_2_label": "la valise en carton",
            "option_3_label": "la cordelette",
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
            {"emphasis": "grain de toile"},
        )
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": "la lucarne",
                "option_2_label": "les caisses",
                "option_3_label": "l'escalier",
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                T2_SCENE[(a, b)],
                "obstacle",
                T2_SONS[b],
                {"emphasis": "Nina"},
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
                    fin_lines(a, b, c),
                    "ending",
                    FIN_SONS[b],
                    {"emphasis": "grain de toile", "note": ending_note(a, b, c)},
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
        "plus petit ou plus grand",
        "tailles différentes",
        "jouer ensemble",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
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
        "kenzo",
        "il faut attendre",
        "il faut demander",
        "on doit demander",
        "papa sourit",
        "maman sourit",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "volet jaune",
        "la mer",
        "plage",
        "vague",
        "cacao",
        "cerf-volant",
        "cerf volant",
        "soleil en papier",
        "le four",
        "rails",
        "wagon",
        "salon",
        "drap à pois",
        "vestiaire",
        "marque fine",
        "ombre-flèche",
        "ombre en forme",
        "tache de couleur",
        "minuscule symbole",
        "anneau de zinc",
        "pois ivoire",
        "grain de savon",
        "grain de vanille",
        "toute chaude",
        "toute fine",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if re.search(r"\bmer\b", whole):
        raise SystemExit(f"{SID} slogan/calque: mer")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob or "nina" not in blob:
        raise SystemExit(f"{SID}: troupe Amir/Nina absente")
    if "grain de toile" not in blob:
        raise SystemExit(f"{SID}: indice grain de toile absent")
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

La trappe du grenier gémit, prête à se fermer. Amir connaît le bois, la malle, le rai ; un détail paraît nouveau : un **grain de toile** tient sur la poignée de la petite valise à pois. Il veut descendre la petite valise à deux, avec Nina, avant que la trappe se referme. Nina veut rester dans la malle. Il tire trop vite : elle ne vient pas. Sourire parti. Papa s'accroupit. Merci vécu : la trappe tenue. Valise à pois, valise en carton ou cordelette : les trois partent. À la lucarne elle veut les toits, entre les caisses elle fouille, à l'escalier elle s'assoit. Deuxième ruse : le grain glisse vers une fente, sous la poussière, vers le trou. Il refuse de foncer. Petite valise, plancher, cordelette ; passage, poignées, poussière ; rampe, palier, petite valise. Le grain du début revient. L'objet porte une trace. La descente a failli.

## Vécu

Amir propose de descendre maintenant. Nina prend son temps ou pose sa limite. Deux rythmes, sans voix caricaturale. Le silence compte. Le sourire disparaît ; envie et inquiétude se bousculent. Papa ou maman s'accroupit à la même hauteur. Personne ne donne la réponse. Amir observe la valise, écoute le grenier, retrouve le grain de toile. La leçon se voit : la petite passe où la grande bute ; deux poignées, deux mains ; un palier à deux hauteurs.

## Vu et corrigé

- Titre noyau conservé. Troupe D16 : Amir, Nina, papa, maman. N2 ≤ 15.
- 86 nœuds, graphe et libellés d'options conservés.
- 27 fins textuellement distinctes, 27 résolutions distinctes, 27 dernières images.
- Première tentative échoue (tirer trop vite, puis lieu choisi). Chaque choix change l'obstacle, le climax, la dernière image.
- Indice unique : grain de toile (pas ancre, étoile brune, fil pâle, croissant, virgule, bouton nacre, nœud raphia, pois ivoire, grain savon, marque fine, ombre-flèche, tache).
- Monde grenier / lucarne / caisses / escalier / malle, distinct de TREE-DIF-015 (salon drap) et TREE-DIF-072 (vestiaire).
- TTS par fonction (ouverture, choix, indice, action, obstacle, résolution, retour).
- `slow` réservé aux choix, à l'indice et aux fins.
- Tics « tout doux / encore / déjà / tout calme » interdits. Gabarit « toute chaude / toute fine » jeté.
- Chemins : {min(ws)}–{max(ws)} mots (moyenne {sum(ws)//len(ws)}). `check()` OK. Pas d'apply.

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. Adulte conversationnel, pas maître. Obstacle en `low-pitch` ; fins `soft` / `slow` / `low-pitch`. Deux rythmes : il propose, elle pose sa limite.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
