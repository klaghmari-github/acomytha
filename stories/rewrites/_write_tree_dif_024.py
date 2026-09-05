#!/usr/bin/env python3
"""TREE-DIF-024 — Le cerf-volant de Chouchou dans le pommier (F-NAR-019, N1, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-024"
LIM = 10
TITLE = "Le cerf-volant de Chouchou dans le pommier"
CHARS = "Chouchou, Aniss, papa, maman"
SETTING = "jardin, pommier après le vent"
FIL = (
    "Après le vent, l'herbe aux pommes fendues sent le fruit. "
    "Sur la marche, la queue rouge du cerf-volant jaune est déchirée. "
    "Un grain de pomme y reste, collé. Chouchou l'avait promis au toit. "
    "Le jaune dort dans le pommier : le jouet n'a pas atteint le ciel promis. "
    "Aniss arrive, plus grand, sans se presser. Silence = réponse. "
    "T1 = ficelle / bâton / tabouret, les trois partent. "
    "Première idée trop vite : poche froissée, pique de travers, toc. "
    "T2 = branches basses / fourche / branche haute. "
    "Le jaune glisse, s'enfonce, ou s'éloigne. Sourire parti. "
    "T3 : ils refusent de foncer, retrouvent le grain, font avec. "
    "27 fins : le papier rentre, le grain paie, ça a failli."
)
TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "il faut attendre",
    "bravo tu as",
    "bon travail",
    "j'ai compris",
    "mission accomplie",
    "aujourd'hui,",
    "aujourd'hui ",
)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp:
        body = body.replace(emp, f"<emphasis>{emp}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return f"{body}{tail}".strip()


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_grain_de_pomme_tient_sur_la_queue_rouge; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_colore_la_descente; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ou_voyage_le_papier_jaune; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_papier_resiste; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=le_jaune_n_atteint_pas_le_toit_promis; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=ils_refusent_de_foncer_retrouvent_le_grain; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_pomme_paie_le_debut; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(pairs: list[tuple[str, str]], where: str) -> None:
    prev = ""
    run = 1
    for role, ph in pairs:
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{where} {n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide")
        if "|" in ph:
            raise SystemExit(f"{where} pipe: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} ponctuation: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} {marks} phrases: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"{where} tic « {tic} »: {ph}")
        for tic in ("encore", "déjà", "deja", "tout doux", "tout calme"):
            if tic in low:
                raise SystemExit(f"{where} tic corpus « {tic} »: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"{where} puces « {tok} »")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""


def voice(old: dict, pairs: list[tuple[str, str]], profile: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    vet(pairs, old["chunk_id"])
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    elif "emphasis" not in m:
        m["emphasis"] = None
    lines = [f"{r}|{p}" for r, p in pairs]
    text, script = from_script(lines)
    out = deepcopy(old)
    out["text"] = text
    out["script"] = script
    out["sons"] = extra.get("sons", old.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitch_ssml"]
    out["pitch_xai_tag"] = m["pitch_tag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before", 0)
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
    out["notes"] = extra.get("note", m["note"])
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        out[k] = v
    return out


def L(*rows: tuple[str, str]) -> list[tuple[str, str]]:
    return list(rows)


OPENING = L(
    ("narrateur", "Après le vent, l'herbe garde des pommes fendues."),
    ("narrateur", "Le volet claque une fois, puis se tait."),
    ("narrateur", "La cuisine sent le fruit écrasé."),
    ("narrateur", "Sur la marche, une queue rouge est déchirée."),
    ("narrateur", "Un grain de pomme y reste, collé."),
    ("papa", "Tu as vu ce grain, Chouchou ?"),
    ("enfant-f", "Il tient sur le papier jaune."),
    ("narrateur", "Chouchou lève le nez vers le pommier."),
    ("narrateur", "Son cerf-volant jaune dort dans les branches."),
    ("enfant-f", "Je l'avais promis au toit."),
    ("narrateur", "Le ciel au-dessus du toit reste vide."),
    ("narrateur", "La piste du toit n'a pas son jaune."),
    ("narrateur", "En ce moment, Aniss arrive dans l'herbe."),
    ("narrateur", "Son ombre va jusqu'aux pommes fendues."),
    ("enfant-f", "Viens, on le prend !"),
    ("narrateur", "Aniss ne bouge pas."),
    ("narrateur", "Il pose un doigt sur le grain."),
    ("papa", "Merci, tu as vu qu'il attend."),
    ("maman", "On prépare les affaires, alors ?"),
)

T1 = {
    1: dict(
        name="la ficelle",
        expected="poche",
        accepted="poche | la poche | dans la poche | dans ma poche",
        retry="Le papier est dans la poche.",
        ok="Oui, il est dans la poche.",
        sons="ficelle,papier",
        emphasis="ficelle",
        passage=L(
            ("narrateur", "Chouchou enroule la ficelle, trop vite."),
            ("enfant-f", "Le papier jaune va avec."),
            ("narrateur", "Elle le pousse dans la poche."),
            ("narrateur", "Le grain de pomme froisse, un peu."),
            ("enfant-m", "Doucement."),
            ("narrateur", "Aniss ne dit rien de plus."),
            ("enfant-f", "Je ralentis."),
            ("maman", "Glisse-le dans ta poche."),
            ("papa", "Le bâton aussi, près du sac."),
            ("narrateur", "Maman pose le tabouret contre le tronc."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("narrateur", "Aniss marche derrière, sans se presser."),
            ("papa", "La ficelle d'abord, vous l'avez."),
        ),
        question=L(
            ("narrateur", "Chouchou a glissé le papier dans la poche."),
            ("maman", "Il est où, le bout de papier ?"),
        ),
        confirm=L(
            ("narrateur", "La ficelle porte le papier, dans la poche."),
            ("enfant-m", "Ça a fait un froissement."),
            ("enfant-f", "C'est pour retrouver le jaune."),
            ("narrateur", "Le grain de pomme tient, contre le tissu."),
            ("narrateur", "Le bâton et le tabouret voyagent aussi."),
            ("maman", "Le grand jaune vous attend, plus haut."),
            ("enfant-f", "Il doit voler au-dessus du toit."),
            ("papa", "On avance sous les feuilles ?"),
            ("enfant-f", "Oui, papa."),
        ),
        choice=L(
            ("narrateur", "La ficelle tape, contre sa poche."),
            ("narrateur", "Des branches basses pendent à gauche."),
            ("narrateur", "Au milieu, une fourche écarte le ciel."),
            ("narrateur", "À droite, une branche haute penche."),
            ("papa", "Où allez-vous chercher le jaune ?"),
        ),
    ),
    2: dict(
        name="le bâton",
        expected="bâton",
        accepted="bâton | le bâton | sur le bâton | le bois",
        retry="Le papier est sur le bâton.",
        ok="Oui, il est sur le bâton.",
        sons="bois,papier",
        emphasis="bâton",
        passage=L(
            ("narrateur", "Chouchou prend le bâton, trop vite."),
            ("enfant-f", "Je pique le papier dessus."),
            ("narrateur", "Le jaune penche, presque dehors."),
            ("narrateur", "Le grain de pomme bascule, un peu."),
            ("enfant-m", "Attends."),
            ("narrateur", "Aniss reste là, les lèvres fermées."),
            ("enfant-f", "Je le tiens plus droit."),
            ("papa", "Enroule-le, comme un drapeau."),
            ("maman", "La ficelle, ensuite, près des pieds."),
            ("narrateur", "Elle glisse le tabouret d'une main."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("narrateur", "Aniss marche derrière, sans se presser."),
            ("maman", "Le bâton d'abord, il est prêt."),
        ),
        question=L(
            ("narrateur", "Chouchou a piqué le papier sur le bâton."),
            ("papa", "Il est où, le bout de papier ?"),
        ),
        confirm=L(
            ("narrateur", "Le bâton tient le papier, comme un drapeau."),
            ("enfant-m", "Je vois un coin, tout jaune."),
            ("enfant-f", "Ne touche pas, pas maintenant."),
            ("narrateur", "Le grain de pomme brille, contre le bois."),
            ("narrateur", "La ficelle et le tabouret voyagent aussi."),
            ("papa", "Ça sent le fruit, ici."),
            ("enfant-f", "Il doit voler au-dessus du toit."),
            ("maman", "Vos pieds, dans l'herbe ?"),
            ("enfant-m", "Oui, maman."),
        ),
        choice=L(
            ("narrateur", "Le bâton sent la sève, un peu."),
            ("narrateur", "Des branches basses pendent à gauche."),
            ("narrateur", "Au milieu, une fourche écarte le ciel."),
            ("narrateur", "À droite, une branche haute penche."),
            ("maman", "Où allez-vous chercher le jaune ?"),
        ),
    ),
    3: dict(
        name="le tabouret",
        expected="tabouret",
        accepted="tabouret | le tabouret | sous le tabouret | le bois",
        retry="Le papier est sous le tabouret.",
        ok="Oui, il est sous le tabouret.",
        sons="bois,toc",
        emphasis="tabouret",
        passage=L(
            ("narrateur", "Chouchou tire le tabouret, trop vite."),
            ("enfant-f", "Le papier reste dessous."),
            ("narrateur", "Le bois tape un petit toc."),
            ("narrateur", "Le grain de pomme tremble, au-dessous."),
            ("enfant-m", "Stop."),
            ("narrateur", "Aniss pose sa paume, sans parler."),
            ("enfant-f", "Je le tiens droit."),
            ("maman", "Tiens-le droit, près du tronc."),
            ("papa", "La ficelle et le bâton, avec vous."),
            ("narrateur", "Il les pose près des sandales."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("narrateur", "Aniss marche derrière, sans se presser."),
            ("papa", "Le tabouret d'abord, il est prêt."),
        ),
        question=L(
            ("narrateur", "Chouchou a glissé le papier sous le tabouret."),
            ("maman", "Il est où, le bout de papier ?"),
        ),
        confirm=L(
            ("narrateur", "Le tabouret cache le papier, au-dessous."),
            ("enfant-f", "Ça sent le bois."),
            ("enfant-m", "Il est là, au creux."),
            ("narrateur", "Le grain de pomme tient, sous l'assise."),
            ("narrateur", "La ficelle et le bâton voyagent aussi."),
            ("maman", "Le pommier vous attend, devant."),
            ("enfant-f", "Il doit voler au-dessus du toit."),
            ("papa", "On y va, tous les quatre ?"),
            ("enfant-f", "Oui."),
        ),
        choice=L(
            ("narrateur", "Le tabouret frotte l'herbe fendue."),
            ("narrateur", "Des branches basses pendent à gauche."),
            ("narrateur", "Au milieu, une fourche écarte le ciel."),
            ("narrateur", "À droite, une branche haute penche."),
            ("papa", "Où allez-vous chercher le jaune ?"),
        ),
    ),
}

T2_LABS = ("les branches basses", "la fourche", "la branche haute")
T3_LABS = {
    1: ("le passage de Chouchou", "la branche levée", "le vent qui défait"),
    2: ("les mains d'Aniss", "le bâton d'en bas", "tirer à deux"),
    3: ("le tabouret d'Aniss", "la ficelle lancée", "le geste d'en bas"),
}
OBJ = {1: "la ficelle", 2: "le bâton", 3: "le tabouret"}
CAP = {1: "La ficelle", 2: "Le bâton", 3: "Le tabouret"}


def t2_basses(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Chouchou pose la ficelle sous les branches.",
        2: "Chouchou tend le bâton sous les branches.",
        3: "Chouchou pousse le tabouret sous les branches.",
    }[a]
    mishap = {
        1: "La ficelle s'accroche trop bas, trop tôt.",
        2: "Le bâton tape trop bas, à côté.",
        3: "Le tabouret bute, trop large pour passer.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-f", "Je passe dessous, Aniss !"),
        ("narrateur", "Les branches basses sentent le fruit."),
        ("narrateur", "Chouchou se baisse, d'un coup."),
        ("narrateur", mishap),
        ("enfant-f", "Ma main n'y arrive pas."),
        ("enfant-m", "Moi, je ne rentre pas."),
        ("narrateur", "Aniss reste dehors, trop grand."),
        ("enfant-f", "Attrape-le, vite !"),
        ("narrateur", "Aniss ne bouge pas."),
        ("narrateur", "Le jaune glisse vers une autre branche."),
        ("narrateur", "Il n'est plus à l'endroit promis."),
        ("narrateur", "Le sourire de Chouchou disparaît."),
        ("narrateur", "L'envie et l'inquiétude se bousculent."),
        ("papa", "Je m'accroupis, à votre hauteur."),
        ("maman", "Vous faites comment, tous les deux ?"),
    )


def t2_fourche(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "La ficelle file trop vite vers la fourche.",
        2: "Le bâton pique trop vite dans la fourche.",
        3: "Le tabouret penche sous la fourche, trop court.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-f", "Je le sors, toute seule !"),
        ("narrateur", "Le jaune s'enfonce, plus loin."),
        ("enfant-m", "Je le vois, entre les deux bois."),
        ("narrateur", "Un grain de pomme luit, puis se cache."),
        ("enfant-f", "Prends-le, Aniss, tes mains !"),
        ("narrateur", "Aniss lève les bras, puis les baisse."),
        ("narrateur", "Il reste planté, sans un mot."),
        ("enfant-f", "Il va partir plus haut !"),
        ("narrateur", "Le jaune ne vole pas vers le toit."),
        ("narrateur", "L'endroit promis reste vide, au-dessus."),
        ("narrateur", "Le sourire de Chouchou n'est plus là."),
        ("narrateur", "Ça serre, juste sous la gorge."),
        ("papa", "Je m'accroupis, près du tronc."),
        ("papa", "Vous le reprenez comment ?"),
    )


def t2_haute(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Chouchou lance la ficelle, trop courte.",
        2: "Chouchou lève le bâton, trop court.",
        3: "Chouchou monte sur le tabouret, trop petite.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-f", "Je l'attrape pour le toit !"),
        ("enfant-m", "Il est trop loin, Chouchou."),
        ("narrateur", "La branche haute penche, trop haute."),
        ("narrateur", "Un souffle lève le jaune, un peu."),
        ("enfant-f", "Il s'éloigne du ciel promis !"),
        ("narrateur", "Le toit promis reste trop loin."),
        ("narrateur", "Chouchou veut grimper plus."),
        ("narrateur", "Aniss tend la paume, sans parler."),
        ("enfant-f", "Aide-moi, alors !"),
        ("narrateur", "Aniss ne grimpe pas."),
        ("narrateur", "Le sourire de Chouchou s'en va."),
        ("narrateur", "Dans sa poitrine, deux envies se poussent."),
        ("maman", "Je m'accroupis, face à l'arbre."),
        ("papa", "Vous le descendez comment, tous les deux ?"),
    )


T2_FN = {1: t2_basses, 2: t2_fourche, 3: t2_haute}
T2_SONS = {1: "feuilles,pas", 2: "bois,branche", 3: "vent,bois"}
T2_EMPH = {1: "branches", 2: "fourche", 3: "branche"}


def t3_choice(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "Les branches restent trop basses pour Aniss."),
            ("narrateur", "Chouchou pose une main, sans sauter."),
            ("papa", "Ton passage, la branche levée, ou le vent ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "Le jaune s'est enfoncé dans la fourche."),
            ("narrateur", "Chouchou pose le bois, sans piquer."),
            ("maman", "Les mains d'Aniss, le bâton, ou tirer ?"),
        )
    return L(
        ("narrateur", "La branche haute reste trop loin."),
        ("narrateur", "Chouchou pose un pied, sans grimper."),
        ("papa", "Le tabouret, la ficelle, ou le geste ?"),
    )


def t3(a: int, b: int, c: int) -> list[tuple[str, str]]:
    o = OBJ[a]
    cap = CAP[a]
    table = {
        (1, 1): L(
            ("enfant-f", "On n'y court pas."),
            ("enfant-m", "Toi tu passes, moi je reste dehors."),
            ("narrateur", "Chouchou glisse sous le vert bas."),
            ("narrateur", f"Aniss garde {o} contre le tronc."),
            ("narrateur", "Papa se tait, accroupi."),
            ("narrateur", "Chouchou écoute les feuilles, puis l'herbe."),
            ("narrateur", "Le grain de pomme brille, sur le jaune."),
            ("enfant-f", "Je le touche !"),
            ("narrateur", "Le papier vient, sans se déchirer."),
            ("papa", "Ton passage allait jusque-là, Chouchou."),
            ("enfant-m", "Regarde, il est à nous."),
            ("enfant-f", "Il est un peu froissé."),
        ),
        (1, 2): L(
            ("enfant-f", "Pas de saut, Aniss."),
            ("enfant-m", "Je lève la branche, tout haut."),
            ("narrateur", "Un tunnel s'ouvre, à sa taille."),
            ("narrateur", f"{cap} attend en bas, plein d'herbe."),
            ("enfant-f", "Je le vois, tout près."),
            ("narrateur", "Chouchou tend les deux mains."),
            ("narrateur", "Elle refuse de tirer trop fort."),
            ("narrateur", "Le grain de pomme penche, à hauteur d'yeux."),
            ("enfant-m", "C'est lui, je le reconnais."),
            ("narrateur", "Le jaune glisse vers Chouchou."),
            ("maman", "Vous le partagez."),
            ("enfant-f", "Il est à moi, un moment."),
        ),
        (1, 3): L(
            ("enfant-f", "On attend le petit vent."),
            ("enfant-m", "Moi aussi, j'attends."),
            ("narrateur", "Un souffle défait la queue rouge."),
            ("narrateur", "Le jaune descend, tout près."),
            ("narrateur", f"{cap} cueille le papier, au bord."),
            ("narrateur", "Chouchou refuse de foncer sous le vert."),
            ("narrateur", "Le grain de pomme voyage avec la queue."),
            ("papa", "Il est venu vers vous."),
            ("enfant-f", "On l'a repris."),
            ("enfant-m", "Regarde, il brille, Chouchou."),
            ("maman", "Vos poches sentent le fruit."),
            ("narrateur", "Les branches se taisent, sans rien garder."),
        ),
        (2, 1): L(
            ("enfant-f", "Tes mains, Aniss."),
            ("enfant-m", "Je les tends, sans sauter."),
            ("narrateur", "Ses doigts passent dans la fourche."),
            ("narrateur", "Une bulle de papier cache le jaune."),
            ("enfant-f", "Là !"),
            ("narrateur", f"Chouchou pose le papier dans {o}."),
            ("narrateur", "Elle ne pique pas vers le bois."),
            ("narrateur", "Le grain de pomme réapparaît, sur le jaune."),
            ("papa", "Tes mains allaient assez loin."),
            ("enfant-m", "On l'a, Chouchou."),
            ("enfant-f", "Il est tiède."),
            ("maman", "Vous avez suivi ce qui était petit."),
        ),
        (2, 2): L(
            ("enfant-f", "On reste ici."),
            ("enfant-m", "On attrape de loin."),
            ("narrateur", f"Aniss tend {o}, bras tout longs."),
            ("narrateur", "Chouchou guide le bord, sans avancer."),
            ("narrateur", "Papa ne dit pas le geste."),
            ("narrateur", f"Chouchou écoute la fourche, puis {o}."),
            ("narrateur", "Le grain de pomme marque le bois, brun."),
            ("narrateur", "Le jaune rentre, un peu rêche."),
            ("enfant-f", "Je le tiens !"),
            ("maman", "Vous n'avez pas piqué trop fort."),
            ("enfant-m", "Il sent les pommes."),
            ("papa", "Soufflez dessus, sans presser."),
        ),
        (2, 3): L(
            ("enfant-f", "On tire à deux."),
            ("enfant-m", "Moi la ficelle, toi le bord."),
            ("narrateur", "Ils tirent, un tout petit peu."),
            ("narrateur", "Le jaune se décroche, sans se déchirer."),
            ("narrateur", f"{cap} reçoit le papier, au creux."),
            ("narrateur", "Chouchou refuse de foncer dans la fourche."),
            ("narrateur", "Le grain de pomme tient, au centre."),
            ("papa", "Vous avez tiré ensemble."),
            ("enfant-f", "On l'a repris."),
            ("enfant-m", "Regarde, il brille, Chouchou."),
            ("maman", "Vos mains sentent le bois."),
            ("narrateur", "La fourche reste vide, sans eux."),
        ),
        (3, 1): L(
            ("enfant-m", "Je monte, toi tu guides."),
            ("narrateur", f"Chouchou garde {o} au pied."),
            ("narrateur", "Aniss est plus haut, d'une tête."),
            ("enfant-f", "Passe-moi la queue rouge."),
            ("enfant-m", "La voilà."),
            ("narrateur", "Il la tend, un tout petit peu."),
            ("narrateur", "Il ne grimpe pas plus loin."),
            ("narrateur", "Le grain de pomme redevient net, au creux."),
            ("enfant-f", "Il brille pour de vrai."),
            ("papa", "Tu es monté juste assez."),
            ("maman", "Chouchou tenait bien le pied."),
            ("narrateur", "Le ciel du toit les attend, plus tard."),
        ),
        (3, 2): L(
            ("enfant-f", "On lance la ficelle, vers la queue."),
            ("enfant-m", "Oui, un peu."),
            ("narrateur", "La boucle accroche la queue rouge."),
            ("narrateur", "Un fil relie leurs deux mains."),
            ("enfant-m", "Maintenant, on peut."),
            ("narrateur", "Ils tirent le jaune, tous les deux."),
            ("narrateur", f"Ils posent {o} sur l'herbe fendue."),
            ("narrateur", "Chouchou ne grimpe pas trop tôt."),
            ("narrateur", "Le grain de pomme tient, propre, au centre."),
            ("enfant-f", "Il est à nous."),
            ("papa", "Le fil vous a laissé la place."),
            ("maman", "Vous avez regardé ensemble."),
        ),
        (3, 3): L(
            ("enfant-f", "On le descend d'ici, d'en bas."),
            ("enfant-m", "Sans monter trop."),
            ("narrateur", f"Papa tend {o}, près des pieds."),
            ("narrateur", "Aniss et Chouchou tiennent le bord."),
            ("narrateur", "La queue rouge glisse vers l'herbe."),
            ("narrateur", "Personne ne pousse, ici."),
            ("narrateur", "Le grain de pomme redevient brun, net."),
            ("enfant-f", "Il brille, Aniss."),
            ("enfant-m", "Je le vois trop bien."),
            ("maman", "Vous avez tiré ensemble."),
            ("papa", "La branche haute reste à sa place."),
            ("narrateur", "Le jaune s'endort, contre leurs genoux."),
        ),
    }
    return table[(b, c)]


def fin(a: int, b: int, c: int) -> list[tuple[str, str]]:
    cap = CAP[a]
    last = {
        (1, 1, 1): "La ficelle garde un grain de pomme au nœud.",
        (1, 1, 2): "La ficelle porte une feuille basse, collée.",
        (1, 1, 3): "La ficelle sent le vent, près du palier.",
        (1, 2, 1): "La ficelle pose une écorce au paillasson.",
        (1, 2, 2): "La ficelle sent la sève, à la porte.",
        (1, 2, 3): "La ficelle laisse un trait brun sur le carreau.",
        (1, 3, 1): "La ficelle sèche au seuil, un peu rêche.",
        (1, 3, 2): "Un fil relie la ficelle au crochet du palier.",
        (1, 3, 3): "La ficelle brille, pleine d'herbe, au rebord.",
        (2, 1, 1): "Le bâton sèche, un grain de pomme au bois.",
        (2, 1, 2): "Le bâton garde une poudre de feuille basse.",
        (2, 1, 3): "Le bâton ombre la marche, près des sandales.",
        (2, 2, 1): "Le bâton pose une écorce au palier.",
        (2, 2, 2): "Le bois sent la sève, à la porte.",
        (2, 2, 3): "Le bâton laisse un fil d'écorce sur le carreau.",
        (2, 3, 1): "Le bâton sèche au seuil, un peu lourd.",
        (2, 3, 2): "Un anneau d'herbe cerne le bâton, au carrelage.",
        (2, 3, 3): "Le bâton brille, lourd de sève, au rebord.",
        (3, 1, 1): "Le tabouret garde un grain de pomme à l'assise.",
        (3, 1, 2): "Le tabouret garde une poudre de feuille.",
        (3, 1, 3): "Le tabouret borde la marche, près des sandales.",
        (3, 2, 1): "Le tabouret pose une écorce au palier.",
        (3, 2, 2): "Le bois du tabouret sent la sève, à la porte.",
        (3, 2, 3): "Le tabouret laisse un trait d'herbe sur le carreau.",
        (3, 3, 1): "Le tabouret sèche au seuil, un pied rêche.",
        (3, 3, 2): "Un rond d'herbe cerne le tabouret, au carrelage.",
        (3, 3, 3): "Le tabouret brille, lourd d'herbe, au rebord.",
    }[(a, b, c)]
    cores = {
        (1, 1): L(
            ("narrateur", "Ils rentrent, le jaune au creux."),
            ("enfant-f", "Il sent le fruit."),
            ("enfant-m", "Ton passage l'a fait descendre."),
            ("papa", "Vous l'avez descendu, enfin."),
            ("maman", "Posez-le sur la marche, au grain."),
            ("narrateur", "Le volet garde le grain de pomme, minuscule."),
            ("narrateur", "Le ciel du toit reste vide, un peu."),
            ("enfant-f", "Tu l'as vu, Aniss."),
            ("enfant-m", "Oui."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (1, 2): L(
            ("narrateur", "Sous la branche levée, la maison était proche."),
            ("enfant-f", "Aniss, tu l'as vu briller."),
            ("enfant-m", "Oui, tout près de tes yeux."),
            ("papa", "Je vous ai regardés, pas trop longtemps."),
            ("maman", "Vos traces rentrent, grandes et petites."),
            ("narrateur", "Le jaune reste dans la paume de Chouchou."),
            ("narrateur", "Le grain de pomme y tient, un peu plat."),
            ("enfant-f", "Je le tiens, Aniss."),
            ("narrateur", "La table sent les pommes fendues."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (1, 3): L(
            ("narrateur", "Le petit vent les suit jusqu'à la porte."),
            ("enfant-f", "Il est venu vers nos mains."),
            ("enfant-m", "On a attendu, tous les deux."),
            ("papa", "Il est descendu vers vous."),
            ("maman", "Changez le linge des poches, d'abord."),
            ("narrateur", "Une ligne d'herbe marque le carreau."),
            ("enfant-f", "Regarde-le, Aniss, il brille."),
            ("narrateur", "Sur la table, le grain de pomme tient."),
            ("narrateur", "Près du pain, le jaune reste au chaud."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (2, 1): L(
            ("narrateur", "Ils rentrent avec de l'écorce aux genoux."),
            ("enfant-m", "Mes mains savaient le chemin."),
            ("enfant-f", "La fourche aussi, peut-être."),
            ("papa", "Vous avez suivi ce qui était à vous."),
            ("maman", "Soufflez la dernière feuille, dehors."),
            ("enfant-m", "Il est pour Chouchou, maintenant."),
            ("enfant-f", "Il est un peu rêche."),
            ("narrateur", "Le grain de pomme sèche sur le palier."),
            ("narrateur", "Chouchou pose le jaune contre le bois."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (2, 2): L(
            ("narrateur", "Ils n'ont pas piqué jusqu'au bois."),
            ("enfant-f", "On l'a attrapé de loin."),
            ("enfant-m", "Tes bras guidaient assez bien."),
            ("maman", "La sève sent fort, sur vos mains."),
            ("papa", "Lavez-les, au bac, sans presser."),
            ("narrateur", f"{cap} garde une feuille de pommier."),
            ("enfant-f", "Je le tiens, Aniss."),
            ("narrateur", "Le grain de pomme reste au creux, brun."),
            ("narrateur", "Le bac se tait, puis la fenêtre."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (2, 3): L(
            ("narrateur", "Leurs mains sentent le bois, un peu."),
            ("enfant-f", "On a tiré ensemble."),
            ("enfant-m", "Sans trop entrer."),
            ("papa", "La fourche est restée à sa place."),
            ("maman", "Vos paumes sentent le fruit."),
            ("narrateur", "Chouchou pose le jaune au rebord."),
            ("enfant-m", "Tu l'as vu, enfin."),
            ("narrateur", "Le grain de pomme s'endort, contre le bois."),
            ("narrateur", "Dehors, le volet se tait."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (3, 1): L(
            ("narrateur", "Les chevilles d'Aniss sont rêches, un peu."),
            ("enfant-f", "Tu l'as tendu pour moi."),
            ("enfant-m", "Tu tenais le pied."),
            ("maman", "Essuie tes pieds, sur le paillasson."),
            ("papa", "Le jaune est net, maintenant."),
            ("narrateur", "Chouchou le pose contre la vitre."),
            ("narrateur", "Un rai de soleil traverse le papier."),
            ("narrateur", "Le grain de pomme y fait un éclat."),
            ("enfant-m", "Tu l'as vu, enfin."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (3, 2): L(
            ("narrateur", "Un fil les suit jusqu'à la porte."),
            ("enfant-f", "La boucle nous l'a rendu."),
            ("enfant-m", "On a tiré ensemble, après."),
            ("papa", "Le fil vous a laissé le temps."),
            ("maman", "L'herbe sèche sur vos mollets."),
            ("narrateur", f"{cap} pose une auréole au carrelage."),
            ("enfant-f", "Il brille trop, Aniss."),
            ("enfant-m", "C'est pour ça."),
            ("narrateur", "Le grain de pomme tient, tout proche de la vitre."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
        (3, 3): L(
            ("narrateur", "Un peu d'herbe fendue reste au seuil."),
            ("enfant-f", "On a tiré d'en bas."),
            ("enfant-m", "Sans trop monter."),
            ("papa", "La branche haute est restée à sa place."),
            ("maman", "Vos mains sentent le fruit."),
            ("narrateur", "Chouchou pose le jaune au rebord."),
            ("enfant-m", "Tu l'as vu, enfin."),
            ("narrateur", "Le grain de pomme s'endort, contre le bois."),
            ("narrateur", "Dehors, le volet se tait."),
            ("narrateur", "Ça a failli rester dans l'arbre."),
        ),
    }
    rows = list(cores[(b, c)])
    rows.append(("narrateur", last))
    return rows


T3_EMPH = {
    1: {1: "passage", 2: "branche", 3: "vent"},
    2: {1: "mains", 2: "bâton", 3: "ensemble"},
    3: {1: "tabouret", 2: "ficelle", 3: "bas"},
}
T3_SONS = {
    1: {1: "feuilles,pas", 2: "branche,pas", 3: "vent,papier"},
    2: {1: "bois,mains", 2: "bois,branche", 3: "ficelle,bois"},
    3: {1: "bois,pas", 2: "ficelle,vent", 3: "herbe,papier"},
}
FIN_SONS = {1: "porte,papier", 2: "bois,porte", 3: "vent,silence"}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "vent,volet", "emphasis": "grain de pomme"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Trois affaires attendent sous le pommier."),
            ("narrateur", "La ficelle, le bâton, et le tabouret."),
            ("maman", "Tu prends quoi d'abord, Chouchou ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "la ficelle",
            "option_2_label": "le bâton",
            "option_3_label": "le tabouret",
        }},
    )

    for a in (1, 2, 3):
        t1 = T1[a]
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(
            by_old[base], t1["passage"], "action",
            extra={"sons": t1["sons"], "emphasis": t1["emphasis"]},
        )
        by[f"{base}_Q0001"] = voice(
            by_old[f"{base}_Q0001"], t1["question"], "clue",
            extra={"sons": "", "emphasis": t1["emphasis"], "fields": {
                "expected_answer": t1["expected"],
                "accepted_examples": t1["accepted"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "Tu es très proche. Reprenons l'indice.",
            }},
        )
        by[f"{base}_C0001"] = voice(
            by_old[f"{base}_C0001"], t1["confirm"], "confirm",
            extra={"sons": "", "emphasis": t1["emphasis"]},
        )
        tid = f"{base}_T0002_P0000"
        by[tid] = voice(
            by_old[tid], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": T2_LABS[0],
                "option_2_label": T2_LABS[1],
                "option_3_label": T2_LABS[2],
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], T2_FN[b](a), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": T2_EMPH[b]},
            )
            t3q = f"{p2}_T0003_P0000"
            labs = T3_LABS[b]
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": labs[0],
                    "option_2_label": labs[1],
                    "option_3_label": labs[2],
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], t3(a, b, c), "resolution",
                    extra={"sons": T3_SONS[b][c], "emphasis": "grain de pomme"},
                )
                fin_id = f"{leaf}_F0001"
                by[fin_id] = voice(
                    by_old[fin_id], fin(a, b, c), "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": "grain de pomme"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for tic in TICS:
        if tic in whole:
            raise SystemExit(f"tic global: {tic}")
    n_enc = len(re.findall(r"\bencore\b", blob))
    n_dej = len(re.findall(r"\bd[eé]jà\b", blob))
    if n_enc or n_dej:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob or "aniss" not in blob:
        raise SystemExit("Chouchou/Aniss absents")
    if "grain de pomme" not in blob:
        raise SystemExit("indice grain de pomme absent")
    if "cerf-volant" not in blob and "cerf volant" not in blob:
        raise SystemExit("cerf-volant absent")
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "merle",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "bibliothécaire",
        "gardienne",
        "grain d'ambre",
        "grain de sève",
        "grain de seve",
        "point d'écume",
        "point d'ecume",
        "étoile brune",
        "etoile brune",
        "fil pâle",
        "fil pale",
        "ancre",
        "clou à tête",
        "clou a tete",
        "nichoir",
        "rond de jus",
        "pomme du haut",
        "marque fine",
        "ombre-flèche",
        "ombre-fleche",
        "tache de couleur",
        "tailles sont différentes",
        "tailles sont differentes",
        "on peut jouer ensemble",
        "inès",
        "ines",
        "sami",
        "toboggan",
        "balançoire",
        "balancoire",
        "gouttes au bord",
    ):
        if bad in whole:
            raise SystemExit(f"calque: {bad}")
    for c in out["chunks"]:
        if not c.get("text_xai_tags") or not c.get("notes") or not c.get("style_energy"):
            raise SystemExit(f"{c['chunk_id']}: TTS incomplet")
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")

    nwords = sum(words(c["text"]) for c in out["chunks"])
    path_lens = []
    for a in (1, 2, 3):
        t1 = f"CHK_T0001_P000{a}"
        seq1 = ["CHK_T0000_P0000", "CHK_T0001_P0000", t1, f"{t1}_Q0001", f"{t1}_C0001", f"{t1}_T0002_P0000"]
        for b in (1, 2, 3):
            t2 = f"{t1}_T0002_P000{b}"
            seq2 = seq1 + [t2, f"{t2}_T0003_P0000"]
            for c in (1, 2, 3):
                t3 = f"{t2}_T0003_P000{c}"
                seq = seq2 + [t3, f"{t3}_F0001"]
                path_lens.append(sum(words(by[i]["text"]) for i in seq))
    pmin, pmax = min(path_lens), max(path_lens)
    pavg = round(sum(path_lens) / len(path_lens))
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Graphe `option_*_next` conservé.\n\n"
        "## Vécu\n"
        "Jardin après le vent, herbe aux pommes fendues. Le volet claque, "
        "puis se tait. Sur la marche, la queue rouge du cerf-volant jaune "
        "est déchirée. Un grain de pomme y reste, collé. Mission : le "
        "descendre pour le promettre au toit, maintenant. Le ciel au-dessus "
        "du toit reste vide : le jouet n'a pas atteint l'endroit promis. "
        "Aniss arrive, plus grand, sans se presser. Chouchou propose de "
        "courir ; son silence compte. Papa remercie Chouchou d'avoir vu "
        "qu'il attend. T1 = ficelle / bâton / tabouret (les trois partent ; "
        "trop vite : poche froissée, pique de travers, toc). T2 = branches "
        "basses (Aniss trop grand pour passer) / fourche (Chouchou trop "
        "petite, le jaune s'enfonce) / branche haute (un souffle l'éloigne "
        "du ciel promis). Sourire parti, poitrine serrée, adulte accroupi. "
        "T3 : ils refusent de foncer, retrouvent le grain du début, font "
        "avec. 27 fins : le jaune rentre, l'objet porte une trace, ça a "
        "failli. Leçon DIF.COR.001 vécue (faire avec Aniss, pas toute "
        "seule), jamais dite. Monde ≠ TREE-DIF-014 (Mila, pomme du haut, "
        "grain de sève), ≠ TREE-DIF-053 (Nina, merle, nichoir).\n\n"
        "## Vu et corrigé\n"
        f"`python3 stories/rewrites/_write_tree_dif_024.py` → `OK {SID} {nwords} mots`. "
        "N1 ≤ 10. `_lib.check` vert.\n"
        "- Ouverture inventée (volet, pommes fendues, pas « encore »).\n"
        "- Indice unique : grain de pomme, payé au climax et en coda.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js. "
        "`slow` = choix, question, retour.\n"
        "- Tics encore / déjà / tout doux / tout calme jetés. "
        "Merle, miel, Mission accomplie, J'ai compris jetés.\n"
        "- Un merci vécu (voir le silence d'Aniss). Pas apply. Audio non cuit.\n\n"
        "## Contrôles\n"
        "- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {pmin} à {pmax} mots par chemin (moyenne {pavg})\n"
        "- `text` = `script` collé ; graphe inchangé\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes`\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} {nwords} mots  1re: {out['chunks'][0]['script'].splitlines()[0].split('|',1)[1]}")


if __name__ == "__main__":
    main()
