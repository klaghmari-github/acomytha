#!/usr/bin/env python3
"""TREE-DIF-068 — Le portrait de Victorina, sur le palier (N3, DIF.COR.003, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-068"
N3 = LIMITS["N3"]
TITLE = "Le portrait de Victorina, sur le palier"
CHARS = "Victorina, Mila, papa, maman"
SETTING = "le palier : fenêtre ronde, rampe, porte des chambres, odeur de cire"
FIL = (
    "Sur le palier de cire, un toc minuscule, puis un grain de cire claire sur le clou. "
    "Victorina veut accrocher le portrait avant que Mila parte. "
    "Mila veut regarder la photo, lentement. Deux rythmes. "
    "Elle prend d'abord le cadre, le chiffon ou le tabouret ; les trois viennent. "
    "À la fenêtre le soleil cache le clou, à la rampe les cheveux gênent, "
    "à la porte la manche cache le grain. Elle refuse de foncer. "
    "Le grain de cire claire revient. Le portrait tient, Mila comme elle est."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de cire claire",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=elle_veut_accrocher_mila_regarde; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="cadre",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_a_pris; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="portrait",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_viennent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_accrocher_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_découragement; intensite=2; destinataire=enfant; sous_texte=deux_rythmes_au_même_instant; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de cire claire",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=faire_avec_mila_comme_elle_est; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de cire claire",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_portrait_tient_mila_comme_elle_est; tempo=posé; sourire=léger; respiration=ample",
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
    if emp and emp in text:
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
        f"destinataire=enfant; sous_texte=le_grain_a_gardé_une_trace; "
        f"tempo={times[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|Un tout petit toc claque contre le bois.",
        "narrateur|La fenêtre ronde pose un rond pâle sur la rampe.",
        "narrateur|Le portrait penche, trop bas, près de la rampe.",
        "narrateur|L'odeur de cire monte du palier.",
        "papa|Tu as vu le clou, Victorina ?",
        "enfant-f|Il y a un grain de cire claire.",
        "maman|Mila met son manteau, près de la porte.",
        "maman|Tu sens la cire, sur le bois ?",
        "enfant-f|Oui, ça sent le palier.",
        "narrateur|En ce moment, Victorina touche le cadre.",
        "enfant-f|Je veux l'accrocher, avant qu'elle parte.",
        "narrateur|Mila regarde la photo, sans un mot.",
        "copine|C'est moi, avec les lunettes.",
        "enfant-f|On accroche, vite !",
        "narrateur|Mila ne bouge pas.",
        "narrateur|Le sourire de Victorina disparaît.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se touchent.",
        "papa|Merci, tu as ramené le chiffon.",
        "maman|Le cadre, le chiffon, le tabouret attendent.",
        "narrateur|Le grain de cire claire brille, sur le clou.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Trois affaires attendent au haut de l'escalier.",
        "narrateur|Le cadre, le chiffon, le petit tabouret.",
        "maman|Par quoi tu commences, Victorina ?",
    ]
)

T1 = {
    1: dict(
        lab="le cadre",
        ans="cadre",
        acc="cadre | le cadre | d'abord le cadre | le bois",
        retry="Victorina a pris le cadre.",
        sons="bois,cadre",
        emp="cadre",
        passage=vet(
            [
                "narrateur|Victorina prend le cadre en bois, trop vite.",
                "enfant-f|Il sent la cire, sur le coin.",
                "papa|Le verre est propre, vois-tu ?",
                "narrateur|Le cadre penche, trop lourd pour une main.",
                "narrateur|Elle veut tirer trop haut, trop vite.",
                "copine|Je le porte, moi.",
                "narrateur|Mila pose une main sous le bas, lente.",
                "maman|Tu la laisses tenir, elle ?",
                "maman|Le chiffon et le tabouret viennent aussi.",
                "narrateur|Papa glisse le chiffon contre le cadre.",
                "narrateur|Le petit tabouret suit, près des pieds.",
                "enfant-f|On a tout, Mila.",
                "narrateur|Mila ne dit rien, elle tient.",
                "papa|Le cadre d'abord, vous l'avez.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le cadre reste contre elle, tiède.",
                "maman|Elle a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|Le cadre.",
                "maman|Oui, le bois.",
                "narrateur|Un grain de cire claire brille au coin.",
                "enfant-f|On va jusqu'au clou.",
                "copine|Je tiens le bas, moi.",
                "papa|Tu tiens bien, Victorina ?",
                "enfant-f|Oui, papa.",
                "maman|Mila n'a plus beaucoup de temps.",
                "narrateur|Mila marche plus lentement qu'elle.",
                "narrateur|Le verre du cadre cherche le clou.",
            ]
        ),
    ),
    2: dict(
        lab="le chiffon",
        ans="chiffon",
        acc="chiffon | le chiffon | d'abord le chiffon | la cire",
        retry="Victorina a pris le chiffon.",
        sons="tissu,cire",
        emp="chiffon",
        passage=vet(
            [
                "narrateur|Victorina prend le chiffon de cire, trop vite.",
                "enfant-f|Il sent le bois chaud, un peu.",
                "maman|Un peu, pas tout le pot.",
                "narrateur|Le chiffon glisse, trop gras, entre ses doigts.",
                "narrateur|Elle veut frotter trop vite, trop fort.",
                "papa|Tu la laisses frotter, elle ?",
                "papa|Le cadre et le tabouret viennent aussi.",
                "narrateur|Mila glisse le cadre contre son ventre.",
                "narrateur|Le petit tabouret tape une marche, bas.",
                "copine|Le palier sent la cire, partout.",
                "enfant-f|On a tout, Mila.",
                "narrateur|Mila frotte le verre, très lentement.",
                "papa|Le chiffon d'abord, vous l'avez.",
                "narrateur|Un grain de cire claire colle au fil.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le chiffon pend à son poignet, gras.",
                "papa|Elle a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|Le chiffon.",
                "papa|Oui, celui de cire.",
                "narrateur|Un grain de cire claire brille au fil.",
                "enfant-f|Il va lustrer le verre.",
                "copine|Ça sent le bois chaud.",
                "maman|Tes mains sont prêtes ?",
                "enfant-f|Oui, maman.",
                "papa|Mila n'a plus beaucoup de temps.",
                "narrateur|Mila frotte plus lentement qu'elle.",
                "narrateur|L'odeur de cire suit le palier.",
            ]
        ),
    ),
    3: dict(
        lab="le tabouret",
        ans="tabouret",
        acc="tabouret | le tabouret | d'abord le tabouret | le petit",
        retry="Victorina a pris le tabouret.",
        sons="bois,tabouret",
        emp="tabouret",
        passage=vet(
            [
                "narrateur|Victorina tire le petit tabouret, trop vite.",
                "enfant-f|Il va me porter, près du clou.",
                "papa|Deux pieds, bien à plat.",
                "narrateur|Le bois racle le palier, trop fort.",
                "narrateur|Elle veut pousser trop vite, trop fort.",
                "maman|Tu la laisses pousser, elle ?",
                "maman|Le cadre et le chiffon viennent aussi.",
                "narrateur|Mila pose le cadre contre le tabouret.",
                "narrateur|Le chiffon reste sur le bois, plat.",
                "copine|On monte toutes, alors.",
                "enfant-f|Le clou m'attend.",
                "narrateur|Mila pousse le tabouret, pas trop vite.",
                "papa|Le tabouret d'abord, il est à toi.",
                "narrateur|Un grain de cire claire colle au pied.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le petit tabouret reste collé aux genoux.",
                "maman|Elle a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|Le tabouret.",
                "maman|Oui, le petit.",
                "narrateur|Un grain de cire claire colle au pied.",
                "enfant-f|Je vais monter, tout près.",
                "copine|Je le pousse, moi.",
                "papa|On avance, toutes les deux ?",
                "enfant-f|Oui, papa.",
                "maman|Mila n'a plus beaucoup de temps.",
                "narrateur|Mila pousse plus lentement qu'elle.",
                "narrateur|Le bois du tabouret attend, plat.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le cadre penche vers le clou, trop vite.",
            "narrateur|Devant, le soleil pique trop, dans les lunettes.",
            "narrateur|La rampe, elle, prend les cheveux dans la bouche.",
            "narrateur|Près de la porte, la manche trop longue cache le clou.",
            "papa|Victorina, tu vas où ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le chiffon colle à sa manche, trop gras.",
            "narrateur|Devant, le soleil pique trop, dans les lunettes.",
            "narrateur|La rampe, elle, prend les cheveux dans la bouche.",
            "narrateur|Près de la porte, la manche trop longue cache le clou.",
            "maman|Victorina, tu vas où ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le tabouret appuie contre son genou.",
            "narrateur|Devant, le soleil pique trop, dans les lunettes.",
            "narrateur|La rampe, elle, prend les cheveux dans la bouche.",
            "narrateur|Près de la porte, la manche trop longue cache le clou.",
            "papa|Victorina, tu vas où ?",
        ]
    ),
}

T2_SONS = {1: "soleil,vitre", 2: "bois,rampe", 3: "porte,tissu"}
FIN_SONS = {1: "vitre,pas", 2: "rampe,pas", 3: "porte,pas"}

T2_SCENE = {
    (1, 1): vet(
        [
            "narrateur|Le cadre penche vers le clou, trop vite.",
            "narrateur|Le rond de soleil tape dans les lunettes.",
            "enfant-f|On accroche, Mila, maintenant !",
            "copine|Je veux voir, d'abord.",
            "narrateur|Victorina tire trop fort, le verre claque.",
            "narrateur|Le grain de cire claire disparaît, trop blanc.",
            "narrateur|Dans sa poitrine, l'envie pousse, trop fort.",
            "enfant-f|Je n'aime pas ça.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila ne dit plus rien.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (1, 2): vet(
        [
            "narrateur|Le cadre frotte la rampe, trop vite.",
            "narrateur|Un cheveu entre dans sa bouche, rêche.",
            "enfant-f|Tiens le cadre, Mila !",
            "copine|La rampe, moi.",
            "narrateur|Victorina tire, Mila garde le bois.",
            "narrateur|Le grain de cire claire glisse, trop loin.",
            "narrateur|Dans sa poitrine, l'inquiétude se bouscule.",
            "enfant-f|Tu ne tiens pas !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila serre la rampe, sans un mot.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (1, 3): vet(
        [
            "narrateur|Le cadre passe près de la porte des chambres.",
            "narrateur|La manche trop longue cache le clou.",
            "enfant-f|Reste, Mila, on accroche !",
            "copine|Mon manteau, d'abord.",
            "narrateur|Victorina lève le cadre, trop vite.",
            "narrateur|Le grain de cire claire se cache sous le tissu.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "enfant-f|Tu t'en vas !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila reste près de la porte, silencieuse.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (2, 1): vet(
        [
            "narrateur|Le chiffon luit trop, sous le rond de soleil.",
            "narrateur|Le verre devient trop blanc, trop fort.",
            "enfant-f|On lustre, Mila, vite !",
            "copine|Je veux voir, d'abord.",
            "narrateur|Victorina frotte trop fort, le chiffon tombe.",
            "narrateur|Le grain de cire claire disparaît, trop blanc.",
            "narrateur|Dans sa poitrine, l'envie pousse, trop fort.",
            "enfant-f|Il est tombé !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila ramasse le chiffon, sans un mot.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (2, 2): vet(
        [
            "narrateur|Le chiffon s'accroche à la rampe, trop gras.",
            "narrateur|Un cheveu entre dans sa bouche, rêche.",
            "enfant-f|Frotte avec moi, Mila !",
            "copine|La rampe, moi.",
            "narrateur|Victorina tire le chiffon, Mila garde le bois.",
            "narrateur|Le grain de cire claire glisse, trop loin.",
            "narrateur|Dans sa poitrine, l'inquiétude se bouscule.",
            "enfant-f|Le chiffon se coince !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila serre la rampe, sans un mot.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (2, 3): vet(
        [
            "narrateur|Le chiffon passe près de la porte des chambres.",
            "narrateur|La manche trop longue cache le clou.",
            "enfant-f|Lustre, Mila, avant de partir !",
            "copine|Mon manteau, d'abord.",
            "narrateur|Victorina tend le chiffon, trop vite.",
            "narrateur|Le grain de cire claire se cache sous le tissu.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "enfant-f|Tu t'en vas !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila reste près de la porte, silencieuse.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (3, 1): vet(
        [
            "narrateur|Le tabouret penche sous le rond de soleil.",
            "narrateur|Le bois devient trop blanc, trop chaud.",
            "enfant-f|Monte, Mila, on accroche !",
            "copine|Je veux voir, d'abord.",
            "narrateur|Victorina pousse le tabouret, trop vite.",
            "narrateur|Le grain de cire claire disparaît, trop blanc.",
            "narrateur|Dans sa poitrine, l'envie pousse, trop fort.",
            "enfant-f|Il penche !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila pose un pied, puis s'arrête.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (3, 2): vet(
        [
            "narrateur|Le tabouret tape la rampe, trop près.",
            "narrateur|Un cheveu entre dans sa bouche, rêche.",
            "enfant-f|Pousse avec moi, Mila !",
            "copine|La rampe, moi.",
            "narrateur|Victorina pousse, Mila garde le bois.",
            "narrateur|Le grain de cire claire glisse, trop loin.",
            "narrateur|Dans sa poitrine, l'inquiétude se bouscule.",
            "enfant-f|Ça coince !",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila serre la rampe, sans un mot.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
    (3, 3): vet(
        [
            "narrateur|Le tabouret barre la porte des chambres.",
            "narrateur|La manche trop longue cache le clou.",
            "enfant-f|Reste, Mila, monte !",
            "copine|Mon manteau, d'abord.",
            "narrateur|Victorina pousse le tabouret, trop vite.",
            "narrateur|Le grain de cire claire se cache sous le tissu.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "enfant-f|Tu t'en vas !",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu fais quoi, alors ?",
            "enfant-f|J'écoute.",
            "narrateur|Mila reste près de la porte, silencieuse.",
            "narrateur|Sans le grain, le clou n'a plus de voix.",
            "narrateur|Victorina refuse de foncer, cette fois.",
        ]
    ),
}

T3_LABS = {
    1: ("les lunettes", "Mila tient", "le nuage"),
    2: ("le nœud", "l'oreille", "Mila souffle"),
    3: ("la manche", "le bouton", "le clou"),
}

T3_Q = {
    1: vet(
        [
            "narrateur|Le soleil cache le clou, trop blanc.",
            "narrateur|Victorina refuse de foncer, cette fois.",
            "narrateur|Elle observe le cadre, et elle écoute le palier.",
            "maman|Tu vois le grain, toi ?",
            "papa|Les lunettes, Mila tient, ou le nuage ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Les cheveux gênent, contre la rampe.",
            "narrateur|Victorina refuse de foncer, cette fois.",
            "narrateur|Elle observe le cadre, et elle écoute le palier.",
            "papa|Tu vois le grain, toi ?",
            "maman|Le nœud, l'oreille, ou Mila souffle ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La manche cache le clou, trop longue.",
            "narrateur|Victorina refuse de foncer, cette fois.",
            "narrateur|Elle observe le cadre, et elle écoute le palier.",
            "maman|Tu vois le grain, toi ?",
            "papa|La manche, le bouton, ou le clou ?",
        ]
    ),
}

T3_EMP = {
    1: {1: "lunettes", 2: "Mila", 3: "nuage"},
    2: {1: "nœud", 2: "oreille", 3: "souffle"},
    3: {1: "manche", 2: "bouton", 3: "clou"},
}

RES = {
    (1, 1, 1): vet(
        [
            "enfant-f|Tes lunettes, d'abord.",
            "narrateur|Elle baisse les lunettes, trop vite, trop fort.",
            "narrateur|Puis elle s'arrête, et elle écoute le palier.",
            "narrateur|Le grain de cire claire reparaît, un peu.",
            "copine|La photo, moi.",
            "narrateur|Mila tient le cadre, plus bas, plus lent.",
            "papa|Tu vois le clou, maintenant ?",
            "enfant-f|Oui, le grain est dessus.",
            "maman|Vous l'avez, toutes les deux.",
            "narrateur|Personne n'a dit comment faire.",
            "narrateur|Le portrait monte, droit, à son rythme.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "enfant-f|Tu tiens, Mila.",
            "narrateur|Elle lâche un peu, sans arracher le cadre.",
            "narrateur|Mila tient à sa hauteur, trop basse.",
            "narrateur|Victorina refuse de le lui prendre.",
            "narrateur|Le grain de cire claire brille, tout bas.",
            "copine|Là, je vois.",
            "papa|Tu as laissé ses mains finir.",
            "enfant-f|On monte, après.",
            "maman|Le clou attend, un peu.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|Le portrait monte, porté par Mila.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "enfant-f|Le nuage, d'abord.",
            "narrateur|Elle attend, le cadre contre elle.",
            "narrateur|Un nuage passe sur la fenêtre ronde.",
            "narrateur|Le grain de cire claire reparaît, net.",
            "copine|Je vois, maintenant.",
            "narrateur|Mila lève le cadre, à son heure.",
            "papa|Le soleil a laissé le clou.",
            "enfant-f|On accroche, lentement.",
            "maman|Vous avez attendu ensemble.",
            "narrateur|Personne n'a pressé le nuage.",
            "narrateur|Le portrait monte, sans le blanc.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "enfant-f|Un nœud, dans tes cheveux.",
            "narrateur|Elle tend un élastique, trop vite.",
            "narrateur|Puis elle attend que Mila noue.",
            "narrateur|Mila fait le nœud, très lentement.",
            "narrateur|Le grain de cire claire reste au coin.",
            "copine|C'est fait.",
            "papa|Tu as laissé ses doigts finir.",
            "enfant-f|La bouche est libre.",
            "maman|La rampe peut attendre.",
            "narrateur|Personne n'a tiré les cheveux.",
            "narrateur|Le portrait monte, le nœud tenu.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "enfant-f|J'écoute, près de ton oreille.",
            "narrateur|Elle se tait, le cadre contre la rampe.",
            "narrateur|Mila souffle un tout petit mot.",
            "copine|Pas trop haut.",
            "narrateur|Le grain de cire claire attend, collé.",
            "narrateur|Victorina baisse le cadre, vers l'oreille.",
            "papa|Tu as entendu, sans parler dessus.",
            "enfant-f|On accroche, plus bas.",
            "maman|Sa voix a choisi la hauteur.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|Le portrait monte, à voix basse.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "enfant-f|Tu souffles, Mila.",
            "narrateur|Elle attend, les lèvres fermées.",
            "narrateur|Mila souffle le cheveu, tout petit.",
            "narrateur|Le grain de cire claire tremble, sous le souffle.",
            "copine|Voilà.",
            "narrateur|Victorina lève le cadre, après le souffle.",
            "papa|Tu as laissé son souffle passer.",
            "enfant-f|La bouche est libre.",
            "maman|La rampe n'a plus pris les cheveux.",
            "narrateur|Personne n'a soufflé à sa place.",
            "narrateur|Le portrait monte, après son air.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "enfant-f|Ta manche, on la relève.",
            "narrateur|Elle tire trop vite, puis s'arrête.",
            "narrateur|Mila relève la manche, à son rythme.",
            "narrateur|Le grain de cire claire sort du tissu.",
            "copine|Je vois le clou.",
            "narrateur|Victorina tient le cadre, sans presser.",
            "papa|Tu as laissé sa manche finir.",
            "enfant-f|On accroche, maintenant.",
            "maman|Le manteau attend, un peu.",
            "narrateur|Personne n'a tiré le bras.",
            "narrateur|Le portrait monte, la manche haute.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "enfant-f|Le bouton, d'abord.",
            "narrateur|Elle tend le poignet, trop vite.",
            "narrateur|Mila boutonne la manche, lentement.",
            "narrateur|Le grain de cire claire reparaît, au clou.",
            "copine|C'est fermé.",
            "narrateur|Victorina attend la dernière boucle.",
            "papa|Tu as laissé ses doigts boutonner.",
            "enfant-f|Le clou est libre.",
            "maman|Le manteau peut attendre un bouton.",
            "narrateur|Personne n'a fermé à sa place.",
            "narrateur|Le portrait monte, le poignet net.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "enfant-f|Le clou, on le cherche.",
            "narrateur|Elle regarde le bois, sans lever trop haut.",
            "narrateur|Mila montre le grain de cire claire.",
            "copine|Là.",
            "narrateur|Le clou apparaît, sous le grain.",
            "narrateur|Victorina lève le cadre, vers le doigt.",
            "papa|Tu as suivi son doigt.",
            "enfant-f|On accroche, sur le grain.",
            "maman|Le manteau a attendu le clou.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|Le portrait monte, sur le grain.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "enfant-f|Tes lunettes, d'abord.",
            "narrateur|Elle baisse les lunettes, le chiffon à la main.",
            "narrateur|Puis elle s'arrête, et elle écoute le palier.",
            "narrateur|Le grain de cire claire reparaît, au fil.",
            "copine|La photo, moi.",
            "narrateur|Mila frotte le verre, plus lentement.",
            "papa|Tu vois le clou, maintenant ?",
            "enfant-f|Oui, le grain est dessus.",
            "maman|Vous l'avez, toutes les deux.",
            "narrateur|Personne n'a dit comment frotter.",
            "narrateur|Le verre luit, puis le portrait monte.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "enfant-f|Tu tiens le chiffon, Mila.",
            "narrateur|Elle lâche un peu, sans l'arracher.",
            "narrateur|Mila frotte à sa hauteur, trop basse.",
            "narrateur|Victorina refuse de le lui prendre.",
            "narrateur|Le grain de cire claire brille, au fil.",
            "copine|Là, je vois.",
            "papa|Tu as laissé ses mains finir.",
            "enfant-f|On lustre, après.",
            "maman|Le clou attend, un peu.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|Le verre luit, porté par Mila.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "enfant-f|Le nuage, d'abord.",
            "narrateur|Elle attend, le chiffon contre elle.",
            "narrateur|Un nuage passe sur la fenêtre ronde.",
            "narrateur|Le grain de cire claire reparaît, net.",
            "copine|Je vois, maintenant.",
            "narrateur|Mila frotte le verre, à son heure.",
            "papa|Le soleil a laissé le clou.",
            "enfant-f|On lustre, lentement.",
            "maman|Vous avez attendu ensemble.",
            "narrateur|Personne n'a pressé le nuage.",
            "narrateur|Le verre luit, sans le blanc.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "enfant-f|Un nœud, dans tes cheveux.",
            "narrateur|Elle tend un élastique, le chiffon au poignet.",
            "narrateur|Puis elle attend que Mila noue.",
            "narrateur|Mila fait le nœud, très lentement.",
            "narrateur|Le grain de cire claire reste au fil.",
            "copine|C'est fait.",
            "papa|Tu as laissé ses doigts finir.",
            "enfant-f|La bouche est libre.",
            "maman|La rampe peut attendre.",
            "narrateur|Personne n'a tiré les cheveux.",
            "narrateur|Le chiffon luit, le nœud tenu.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "enfant-f|J'écoute, près de ton oreille.",
            "narrateur|Elle se tait, le chiffon contre la rampe.",
            "narrateur|Mila souffle un tout petit mot.",
            "copine|Pas trop haut.",
            "narrateur|Le grain de cire claire attend, au fil.",
            "narrateur|Victorina baisse le chiffon, vers l'oreille.",
            "papa|Tu as entendu, sans parler dessus.",
            "enfant-f|On lustre, plus bas.",
            "maman|Sa voix a choisi la hauteur.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|Le verre luit, à voix basse.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "enfant-f|Tu souffles, Mila.",
            "narrateur|Elle attend, le chiffon plié.",
            "narrateur|Mila souffle le cheveu, tout petit.",
            "narrateur|Le grain de cire claire tremble, sous le souffle.",
            "copine|Voilà.",
            "narrateur|Victorina frotte le verre, après le souffle.",
            "papa|Tu as laissé son souffle passer.",
            "enfant-f|La bouche est libre.",
            "maman|La rampe n'a plus pris les cheveux.",
            "narrateur|Personne n'a soufflé à sa place.",
            "narrateur|Le verre luit, après son air.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "enfant-f|Ta manche, on la relève.",
            "narrateur|Elle tire trop vite, puis s'arrête.",
            "narrateur|Mila relève la manche, le chiffon dedans.",
            "narrateur|Le grain de cire claire sort du tissu.",
            "copine|Je vois le clou.",
            "narrateur|Victorina tend le chiffon, sans presser.",
            "papa|Tu as laissé sa manche finir.",
            "enfant-f|On lustre, maintenant.",
            "maman|Le manteau attend, un peu.",
            "narrateur|Personne n'a tiré le bras.",
            "narrateur|Le verre luit, la manche haute.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "enfant-f|Le bouton, d'abord.",
            "narrateur|Elle tend le poignet, le chiffon collé.",
            "narrateur|Mila boutonne la manche, lentement.",
            "narrateur|Le grain de cire claire reparaît, au clou.",
            "copine|C'est fermé.",
            "narrateur|Victorina attend la dernière boucle.",
            "papa|Tu as laissé ses doigts boutonner.",
            "enfant-f|Le clou est libre.",
            "maman|Le manteau peut attendre un bouton.",
            "narrateur|Personne n'a fermé à sa place.",
            "narrateur|Le verre luit, le poignet net.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "enfant-f|Le clou, on le cherche.",
            "narrateur|Elle frotte le bois, sans lever trop haut.",
            "narrateur|Mila montre le grain de cire claire.",
            "copine|Là.",
            "narrateur|Le clou apparaît, sous le grain.",
            "narrateur|Victorina lustre vers le doigt.",
            "papa|Tu as suivi son doigt.",
            "enfant-f|On accroche, sur le grain.",
            "maman|Le manteau a attendu le clou.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|Le verre luit, sur le grain.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "enfant-f|Tes lunettes, d'abord.",
            "narrateur|Elle baisse les lunettes, près du tabouret.",
            "narrateur|Puis elle s'arrête, et elle écoute le palier.",
            "narrateur|Le grain de cire claire reparaît, au pied.",
            "copine|La photo, moi.",
            "narrateur|Mila pose un pied, plus lentement.",
            "papa|Tu vois le clou, maintenant ?",
            "enfant-f|Oui, le grain est dessus.",
            "maman|Vous l'avez, toutes les deux.",
            "narrateur|Personne n'a dit comment monter.",
            "narrateur|Le tabouret tient, puis le portrait monte.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "enfant-f|Tu tiens le tabouret, Mila.",
            "narrateur|Elle lâche un peu, sans le tirer.",
            "narrateur|Mila le pousse à sa hauteur, trop basse.",
            "narrateur|Victorina refuse de le lui prendre.",
            "narrateur|Le grain de cire claire brille, au pied.",
            "copine|Là, je vois.",
            "papa|Tu as laissé ses mains finir.",
            "enfant-f|On monte, après.",
            "maman|Le clou attend, un peu.",
            "narrateur|Personne n'a crié la réponse.",
            "narrateur|Le tabouret avance, poussé par Mila.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "enfant-f|Le nuage, d'abord.",
            "narrateur|Elle attend, le tabouret contre elle.",
            "narrateur|Un nuage passe sur la fenêtre ronde.",
            "narrateur|Le grain de cire claire reparaît, net.",
            "copine|Je vois, maintenant.",
            "narrateur|Mila pose les deux pieds, à son heure.",
            "papa|Le soleil a laissé le clou.",
            "enfant-f|On monte, lentement.",
            "maman|Vous avez attendu ensemble.",
            "narrateur|Personne n'a pressé le nuage.",
            "narrateur|Le tabouret tient, sans le blanc.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "enfant-f|Un nœud, dans tes cheveux.",
            "narrateur|Elle tend un élastique, près du tabouret.",
            "narrateur|Puis elle attend que Mila noue.",
            "narrateur|Mila fait le nœud, très lentement.",
            "narrateur|Le grain de cire claire reste au pied.",
            "copine|C'est fait.",
            "papa|Tu as laissé ses doigts finir.",
            "enfant-f|La bouche est libre.",
            "maman|La rampe peut attendre.",
            "narrateur|Personne n'a tiré les cheveux.",
            "narrateur|Le tabouret avance, le nœud tenu.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "enfant-f|J'écoute, près de ton oreille.",
            "narrateur|Elle se tait, le tabouret contre la rampe.",
            "narrateur|Mila souffle un tout petit mot.",
            "copine|Pas trop haut.",
            "narrateur|Le grain de cire claire attend, au pied.",
            "narrateur|Victorina baisse le tabouret, vers l'oreille.",
            "papa|Tu as entendu, sans parler dessus.",
            "enfant-f|On monte, plus bas.",
            "maman|Sa voix a choisi la hauteur.",
            "narrateur|Personne n'a donné le plan.",
            "narrateur|Le tabouret avance, à voix basse.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "enfant-f|Tu souffles, Mila.",
            "narrateur|Elle attend, les deux pieds à plat.",
            "narrateur|Mila souffle le cheveu, tout petit.",
            "narrateur|Le grain de cire claire tremble, sous le souffle.",
            "copine|Voilà.",
            "narrateur|Victorina pousse le tabouret, après le souffle.",
            "papa|Tu as laissé son souffle passer.",
            "enfant-f|La bouche est libre.",
            "maman|La rampe n'a plus pris les cheveux.",
            "narrateur|Personne n'a soufflé à sa place.",
            "narrateur|Le tabouret avance, après son air.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "enfant-f|Ta manche, on la relève.",
            "narrateur|Elle tire trop vite, puis s'arrête.",
            "narrateur|Mila relève la manche, près du tabouret.",
            "narrateur|Le grain de cire claire sort du tissu.",
            "copine|Je vois le clou.",
            "narrateur|Victorina tient le tabouret, sans presser.",
            "papa|Tu as laissé sa manche finir.",
            "enfant-f|On monte, maintenant.",
            "maman|Le manteau attend, un peu.",
            "narrateur|Personne n'a tiré le bras.",
            "narrateur|Le tabouret avance, la manche haute.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "enfant-f|Le bouton, d'abord.",
            "narrateur|Elle tend le poignet, près du tabouret.",
            "narrateur|Mila boutonne la manche, lentement.",
            "narrateur|Le grain de cire claire reparaît, au clou.",
            "copine|C'est fermé.",
            "narrateur|Victorina attend la dernière boucle.",
            "papa|Tu as laissé ses doigts boutonner.",
            "enfant-f|Le clou est libre.",
            "maman|Le manteau peut attendre un bouton.",
            "narrateur|Personne n'a fermé à sa place.",
            "narrateur|Le tabouret avance, le poignet net.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "enfant-f|Le clou, on le cherche.",
            "narrateur|Elle pose le tabouret, sans lever trop haut.",
            "narrateur|Mila montre le grain de cire claire.",
            "copine|Là.",
            "narrateur|Le clou apparaît, sous le grain.",
            "narrateur|Victorina monte vers le doigt.",
            "papa|Tu as suivi son doigt.",
            "enfant-f|On accroche, sur le grain.",
            "maman|Le manteau a attendu le clou.",
            "narrateur|Personne n'a nommé le chemin.",
            "narrateur|Le tabouret porte, sur le grain.",
        ]
    ),
}

_FAIL = vet(["narrateur|Ça a failli ne pas tenir."])[0]
RES = {k: v[:-1] + [_FAIL] + v[-1:] for k, v in RES.items()}

FIN = {
    (1, 1, 1): vet(
        [
            "narrateur|Le portrait a failli rester trop blanc.",
            "enfant-f|Les lunettes ont laissé le clou.",
            "copine|J'ai vu la photo, d'abord.",
            "papa|On descend, le palier sent la cire.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Mila a tenu, à sa façon.",
            "narrateur|Un grain de cire claire reste au coin du cadre.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "narrateur|Le portrait a failli rester trop bas.",
            "copine|Je l'ai tenu, moi.",
            "enfant-f|Puis on a monté, ensemble.",
            "papa|On descend, les mains un peu grasses.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Ses mains ont choisi la hauteur.",
            "narrateur|Le grain de cire claire brille, là où Mila a tenu.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "narrateur|Le portrait a failli attendre le soleil.",
            "copine|Le nuage a passé.",
            "enfant-f|Puis on a accroché, sans le blanc.",
            "papa|On descend, la fenêtre ronde est grise.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|On a attendu le nuage, toutes les deux.",
            "narrateur|Le grain de cire claire reparaît, après le nuage.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "narrateur|Le portrait a failli rester dans les cheveux.",
            "copine|Le nœud tient, tout petit.",
            "enfant-f|Puis on a accroché, la bouche libre.",
            "papa|On descend, la rampe est lisse.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Ses doigts ont noué, lentement.",
            "narrateur|Un grain de cire claire colle au nœud, minuscule.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "narrateur|Le portrait a failli parler trop fort.",
            "copine|Pas trop haut.",
            "enfant-f|J'ai écouté, près de l'oreille.",
            "papa|On descend, sans crier.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Sa voix a choisi, toute basse.",
            "narrateur|Le grain de cire claire attend près de l'oreille de Mila.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "narrateur|Le portrait a failli garder le cheveu.",
            "copine|J'ai soufflé, moi.",
            "enfant-f|Puis on a accroché, après l'air.",
            "papa|On descend, la rampe est libre.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Son souffle a passé, d'abord.",
            "narrateur|Le grain de cire claire tremble, sous le souffle arrêté.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "narrateur|Le portrait a failli rester sous la manche.",
            "copine|J'ai relevé, moi.",
            "enfant-f|Puis on a vu le clou.",
            "papa|On descend, le manteau sous le bras.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Sa manche a fini, à son rythme.",
            "narrateur|Le grain de cire claire sort de la manche, au clou.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "narrateur|Le portrait a failli attendre le bouton.",
            "copine|C'est fermé, maintenant.",
            "enfant-f|Puis on a accroché, le poignet net.",
            "papa|On descend, un bouton brille.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Ses doigts ont boutonné, lentement.",
            "narrateur|Le grain de cire claire brille près du bouton.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "narrateur|Le portrait a failli manquer le clou.",
            "copine|Là, j'ai montré.",
            "enfant-f|On a suivi le doigt, jusqu'au grain.",
            "papa|On descend, la porte des chambres se tait.",
            "maman|Le cadre reste droit, contre le mur.",
            "enfant-f|Son doigt a trouvé le clou.",
            "narrateur|Le grain de cire claire montre le clou, enfin.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "narrateur|Le verre a failli rester trop blanc.",
            "enfant-f|Les lunettes ont laissé le chiffon.",
            "copine|J'ai vu la photo, d'abord.",
            "papa|On descend, ça sent la cire.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Mila a frotté, à sa façon.",
            "narrateur|Un grain de cire claire reste au fil du chiffon.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "narrateur|Le verre a failli rester trop bas.",
            "copine|J'ai tenu le chiffon, moi.",
            "enfant-f|Puis on a lustré, ensemble.",
            "papa|On descend, les mains un peu grasses.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Ses mains ont choisi la hauteur.",
            "narrateur|Le grain de cire claire brille au fil, bas.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "narrateur|Le verre a failli attendre le soleil.",
            "copine|Le nuage a passé.",
            "enfant-f|Puis on a lustré, sans le blanc.",
            "papa|On descend, la fenêtre ronde est grise.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|On a attendu le nuage, toutes les deux.",
            "narrateur|Le grain de cire claire sèche au fil, après le nuage.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "narrateur|Le chiffon a failli rester dans les cheveux.",
            "copine|Le nœud tient, tout petit.",
            "enfant-f|Puis on a lustré, la bouche libre.",
            "papa|On descend, la rampe est lisse.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Ses doigts ont noué, lentement.",
            "narrateur|Un grain de cire claire colle au nœud du chiffon.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "narrateur|Le chiffon a failli parler trop fort.",
            "copine|Pas trop haut.",
            "enfant-f|J'ai écouté, près de l'oreille.",
            "papa|On descend, sans crier.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Sa voix a choisi, toute basse.",
            "narrateur|Le grain de cire claire attend au fil, près de l'oreille.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "narrateur|Le chiffon a failli garder le cheveu.",
            "copine|J'ai soufflé, moi.",
            "enfant-f|Puis on a lustré, après l'air.",
            "papa|On descend, la rampe est libre.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Son souffle a passé, d'abord.",
            "narrateur|Le grain de cire claire tremble au fil, sous l'air arrêté.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "narrateur|Le chiffon a failli rester sous la manche.",
            "copine|J'ai relevé, moi.",
            "enfant-f|Puis on a vu le clou.",
            "papa|On descend, le manteau sous le bras.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Sa manche a fini, à son rythme.",
            "narrateur|Le grain de cire claire sort du chiffon, au clou.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "narrateur|Le chiffon a failli attendre le bouton.",
            "copine|C'est fermé, maintenant.",
            "enfant-f|Puis on a lustré, le poignet net.",
            "papa|On descend, un bouton brille.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Ses doigts ont boutonné, lentement.",
            "narrateur|Le grain de cire claire brille au fil, près du bouton.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "narrateur|Le chiffon a failli manquer le clou.",
            "copine|Là, j'ai montré.",
            "enfant-f|On a suivi le doigt, jusqu'au grain.",
            "papa|On descend, la porte des chambres se tait.",
            "maman|Le chiffon reste plié, près du cadre.",
            "enfant-f|Son doigt a trouvé le clou.",
            "narrateur|Le grain de cire claire luit au fil, sur le clou.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "narrateur|Le tabouret a failli rester trop blanc.",
            "enfant-f|Les lunettes ont laissé le bois.",
            "copine|J'ai vu la photo, d'abord.",
            "papa|On descend, le palier sent la cire.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Mila a posé le pied, à sa façon.",
            "narrateur|Un grain de cire claire reste au pied du tabouret.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "narrateur|Le tabouret a failli rester trop bas.",
            "copine|Je l'ai poussé, moi.",
            "enfant-f|Puis on a monté, ensemble.",
            "papa|On descend, les mains un peu grasses.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Ses mains ont choisi la hauteur.",
            "narrateur|Le grain de cire claire brille au pied, bas.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "narrateur|Le tabouret a failli attendre le soleil.",
            "copine|Le nuage a passé.",
            "enfant-f|Puis on a monté, sans le blanc.",
            "papa|On descend, la fenêtre ronde est grise.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|On a attendu le nuage, toutes les deux.",
            "narrateur|Le grain de cire claire sèche au pied, après le nuage.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "narrateur|Le tabouret a failli rester dans les cheveux.",
            "copine|Le nœud tient, tout petit.",
            "enfant-f|Puis on a monté, la bouche libre.",
            "papa|On descend, la rampe est lisse.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Ses doigts ont noué, lentement.",
            "narrateur|Un grain de cire claire colle au nœud, près du bois.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "narrateur|Le tabouret a failli parler trop fort.",
            "copine|Pas trop haut.",
            "enfant-f|J'ai écouté, près de l'oreille.",
            "papa|On descend, sans crier.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Sa voix a choisi, toute basse.",
            "narrateur|Le grain de cire claire attend au pied, près de l'oreille.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "narrateur|Le tabouret a failli garder le cheveu.",
            "copine|J'ai soufflé, moi.",
            "enfant-f|Puis on a monté, après l'air.",
            "papa|On descend, la rampe est libre.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Son souffle a passé, d'abord.",
            "narrateur|Le grain de cire claire tremble au pied, sous l'air arrêté.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "narrateur|Le tabouret a failli rester sous la manche.",
            "copine|J'ai relevé, moi.",
            "enfant-f|Puis on a vu le clou.",
            "papa|On descend, le manteau sous le bras.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Sa manche a fini, à son rythme.",
            "narrateur|Le grain de cire claire sort du pied, au clou.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "narrateur|Le tabouret a failli attendre le bouton.",
            "copine|C'est fermé, maintenant.",
            "enfant-f|Puis on a monté, le poignet net.",
            "papa|On descend, un bouton brille.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Ses doigts ont boutonné, lentement.",
            "narrateur|Le grain de cire claire brille au pied, près du bouton.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "narrateur|Le tabouret a failli manquer le clou.",
            "copine|Là, j'ai montré.",
            "enfant-f|On a suivi le doigt, jusqu'au grain.",
            "papa|On descend, la porte des chambres se tait.",
            "maman|Le tabouret reste bas, près du mur.",
            "enfant-f|Son doigt a trouvé le clou.",
            "narrateur|Le grain de cire claire luit au pied, sur le clou.",
        ]
    ),
}

_TOC = vet(["narrateur|Le petit toc du début s'est tu."])[0]
FIN = {k: v[:-1] + [_TOC] + v[-1:] for k, v in FIN.items()}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "cire,bois", {"emphasis": "grain de cire claire"})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "le cadre",
            "option_2_label": "le chiffon",
            "option_3_label": "le tabouret",
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
            {"emphasis": "grain de cire claire"},
        )
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": "la fenêtre",
                "option_2_label": "la rampe",
                "option_3_label": "la porte",
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                T2_SCENE[(a, b)],
                "obstacle",
                T2_SONS[b],
                {"emphasis": "Mila"},
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
                    {"emphasis": "grain de cire claire", "note": ending_note(a, b, c)},
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
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "merle",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "point de cire",
        "goutte de cire rouge",
        "ancre",
        "étoile brune",
        "fil pâle",
        "croissant",
        "virgule",
        "bouton nacre",
        "nœud raphia",
        "pois ivoire",
        "grain savon",
        "grain vanille",
        "pastille colle",
        "capuchon",
        "grain doré",
        "brin safran",
        "anneau liège",
        "clou tête ronde",
        "grain d'ambre",
        "anneau de zinc",
        "larme de bronze",
        "bracelet d'écorce",
        "boucle d'étain",
        "loup",
        "cour ",
        "roue",
        "appentis",
        "buffet",
        "placard",
        "bac à sable",
        "toboggan",
        "balançoire",
        "kenzo",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "lina",
        "iris",
        "il faut attendre",
        "lunettes, cheveux, habit",
        "apparence",
        "pas rire",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorina" not in blob or "mila" not in blob:
        raise SystemExit(f"{SID}: troupe Victorina/Mila absente")
    if "palier" not in blob or "portrait" not in blob:
        raise SystemExit(f"{SID}: palier/portrait absent")
    if "grain de cire claire" not in blob:
        raise SystemExit(f"{SID}: indice grain de cire claire absent")
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

Un toc minuscule sur le palier de cire. Victorina voit un grain de cire claire sur le clou. Elle veut accrocher le portrait de famille avant que Mila parte. Mila veut regarder la photo, lentement. Deux rythmes. Silence = réponse. Elle prend d'abord le cadre, le chiffon ou le tabouret ; les trois viennent. À la fenêtre le soleil cache le clou, à la rampe les cheveux gênent, à la porte la manche cache le grain. Elle refuse de foncer. Le grain du début revient. Le portrait tient.

## Vécu

Victorina propose, trop vite. Mila prend son temps, pose sa limite, ou se tait. T1 = cadre / chiffon / tabouret (équipement non retiré). T2 = fenêtre (soleil, lunettes, photo) / rampe (cheveux, bois gardé) / porte (manteau, manche). T3 = lunettes, Mila tient, nuage ; nœud, oreille, Mila souffle ; manche, bouton, clou. La leçon DIF.COR.003 se voit : on accroche avec Mila telle qu'elle est. Un merci de papa, lié au chiffon ramené.

## Vu et corrigé

- Titre noyau conservé. Troupe D16 : Victorina, Mila, papa, maman. N3 ≤ 16.
- 86 nœuds, graphe et libellés d'options conservés.
- 27 fins textuellement distinctes, 27 résolutions distinctes, 27 dernières images.
- Première tentative échoue (accrocher trop vite). Chaque choix change l'obstacle, le climax, la dernière image.
- Indice unique : grain de cire claire (pas ancre, étoile, fil pâle, croissant, virgule, nacre, raphia, pois ivoire, grain savon/vanille, pastille, capuchon, point de cire).
- Monde palier (fenêtre ronde, rampe, porte des chambres, odeur de cire), distinct de TREE-DIF-037 (cour/roue) et TREE-DIF-054 (loup carton, couloir).
- TTS par fonction (ouverture, choix, indice, action, obstacle, résolution, retour).
- `slow` réservé aux choix, à l'indice et aux fins.
- Tics « tout doux / encore / déjà / tout calme » interdits. Pas merle, pas miel.
- Chemins : {min(ws)}–{max(ws)} mots (moyenne {sum(ws)//len(ws)}). `check()` OK. Pas d'apply.

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. Adulte conversationnel, pas maître. Obstacle en `low-pitch` ; fins `soft` / `slow` / `low-pitch`. Deux rythmes : elle propose, Mila pose sa limite. Le silence compte.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
