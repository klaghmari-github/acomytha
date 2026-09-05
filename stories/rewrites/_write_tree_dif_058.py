#!/usr/bin/env python3
"""TREE-DIF-058 — Les clochettes de Chouchou, au-dessus de la porte (F-NAR-019, N3, DIF.COR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-058"
LIM = 16
TITLE = "Les clochettes de Chouchou, au-dessus de la porte"
CHARS = "Chouchou, Nino, papa, maman"
SETTING = "chambre le soir : porte, lit, fenêtre, réverbère"
TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "tailles différentes",
    "plus petit ou plus grand",
    "l'histoire est finie",
    "il faut attendre",
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la_porte_peut_sonner_si_chouchou_atteint; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_porte; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrete; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_peuvent_partir; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=porter_sans_lancer_trop_haut; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=deception_legere; intensite=2; destinataire=enfant; sous_texte=les_hauteurs_ne_sont_pas_les_memes; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=jouer_a_deux_hauteurs; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=la_barre_jaune_et_les_clochettes_se_rejoignent; tempo=pose; sourire=léger; respiration=ample",
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
    ("narrateur", "Le réverbère pose une barre jaune sur le plancher."),
    ("narrateur", "Le bois de la chambre sent le savon tiède."),
    ("narrateur", "Une soucoupe tient trois clochettes, près du lit."),
    ("narrateur", "Un ruban rouge dort, plié, sur la chaise."),
    ("narrateur", "Un anneau de bois attend, un peu rêche."),
    ("narrateur", "Chouchou vit ici avec papa, maman, et Nino."),
    ("papa", "La chemise de Nino est pliée, sur le dossier."),
    ("maman", "Le savon de la salle d'eau sent fort."),
    ("narrateur", "En ce moment, Chouchou lève la soucoupe vers le crochet."),
    ("enfant-f", "Elles vont sonner, pour Nino, là-haut !"),
    ("narrateur", "Elle se hausse, sur la pointe."),
    ("narrateur", "Ses doigts n'arrivent pas au crochet."),
    ("narrateur", "Une clochette glisse, et tinte sur le plancher."),
    ("enfant-f", "Trop haut pour moi."),
    ("narrateur", "Elle rattrape la soucoupe, les joues chaudes."),
    ("papa", "Merci, tu l'as tenue à deux mains."),
    ("narrateur", "Nino a les cheveux sous l'abat-jour."),
    ("copain", "Moi, je l'atteins."),
    ("maman", "Le crochet est loin, pour tes bras."),
    ("enfant-f", "Je veux qu'elles sonnent, pour lui, maintenant."),
)

T1 = {
    1: dict(
        name="les clochettes",
        expected="ventre",
        accepted="ventre | le ventre | contre le ventre | son ventre",
        retry="Les clochettes sont contre le ventre.",
        ok="Oui, contre le ventre.",
        sons="clochette,soucoupe",
        emphasis="clochettes",
        passage=L(
            ("narrateur", "Chouchou lève la soucoupe, trop haut, comme Nino."),
            ("narrateur", "Les clochettes glissent, ding, dans sa paume."),
            ("enfant-f", "Elles ne restent pas en l'air."),
            ("maman", "Contre ton ventre, à ta hauteur."),
            ("narrateur", "Le métal tient, collé au pull."),
            ("papa", "Le ruban, autour du poignet, après."),
            ("narrateur", "Nino prend l'anneau, sans se baisser."),
            ("enfant-f", "Nino, tu viens près du seuil ?"),
            ("copain", "J'arrive."),
            ("narrateur", "Le métal tinte à chaque pas, vers la porte."),
            ("papa", "Vous les avez, contre vous."),
        ),
        question=L(
            ("narrateur", "Le métal reste collé contre son pull."),
            ("maman", "Elle a mis les clochettes où ?"),
        ),
        confirm=L(
            ("enfant-f", "Contre le ventre."),
            ("maman", "Oui, à ta hauteur."),
            ("narrateur", "La soucoupe chauffe le pull, un peu."),
            ("narrateur", "Nino a les genoux plus hauts."),
            ("maman", "Regarde ses genoux, près du bois."),
            ("papa", "On reste dans la chambre ?"),
            ("enfant-f", "Oui, papa."),
            ("copain", "Moi, je vois le crochet."),
        ),
        choice=L(
            ("narrateur", "Les clochettes tapent le ventre, tout bas."),
            ("narrateur", "Au crochet de la porte, c'est trop haut."),
            ("narrateur", "Au pied du lit, Nino cognerait."),
            ("narrateur", "Près du loquet, le vent pourrait sonner."),
            ("papa", "Vous les accrochez où, pour Nino ?"),
        ),
    ),
    2: dict(
        name="le ruban rouge",
        expected="poignet",
        accepted="poignet | le poignet | autour du poignet | son poignet",
        retry="Le ruban est autour du poignet.",
        ok="Oui, autour du poignet.",
        sons="tissu,satin",
        emphasis="ruban",
        passage=L(
            ("narrateur", "Chouchou enroule le ruban autour du poignet."),
            ("enfant-f", "Je le lance, jusqu'au crochet !"),
            ("narrateur", "Le satin vole, trop court, et retombe."),
            ("enfant-f", "Il n'atteint pas."),
            ("papa", "Autour du poignet, d'abord, sans lancer."),
            ("narrateur", "Le satin se tait, contre sa peau."),
            ("maman", "Les clochettes, contre le ventre, après."),
            ("narrateur", "Nino prend l'anneau de bois."),
            ("enfant-f", "On les accroche, tous les deux ?"),
            ("copain", "Me voilà."),
            ("maman", "Le ruban est prêt, à ta hauteur."),
        ),
        question=L(
            ("narrateur", "Le rouge veille près de sa peau."),
            ("papa", "Elle a mis le ruban où ?"),
        ),
        confirm=L(
            ("enfant-f", "Autour du poignet."),
            ("papa", "Oui, collé à ta peau."),
            ("narrateur", "Le satin froisse, puis se tait."),
            ("narrateur", "Une mèche de Nino saute sous l'abat-jour."),
            ("maman", "Vos mains, au-dessus de la soucoupe ?"),
            ("copain", "Oui, maman."),
            ("enfant-f", "Ne le noue pas, trop tôt."),
            ("papa", "Ça sent la lavande, sur le satin."),
        ),
        choice=L(
            ("narrateur", "Le ruban frotte le poignet, un peu lisse."),
            ("narrateur", "Au crochet de la porte, c'est trop haut."),
            ("narrateur", "Au pied du lit, Nino cognerait."),
            ("narrateur", "Près du loquet, le vent pourrait sonner."),
            ("maman", "Vous les accrochez où, pour Nino ?"),
        ),
    ),
    3: dict(
        name="l'anneau de bois",
        expected="bras",
        accepted="bras | le bras | sous le bras | son bras",
        retry="L'anneau est sous le bras.",
        ok="Oui, sous le bras.",
        sons="bois,porte",
        emphasis="anneau",
        passage=L(
            ("narrateur", "Chouchou glisse l'anneau sous son bras."),
            ("enfant-f", "Je l'accroche, toute seule."),
            ("narrateur", "Elle se hausse, le bois contre le chambranle."),
            ("narrateur", "L'anneau tape trop bas, et retombe."),
            ("enfant-f", "Il n'accroche pas."),
            ("maman", "Serre-le sous le bras, tout droit."),
            ("papa", "Les clochettes et le ruban, avec vous."),
            ("narrateur", "Rien ne reste dans la soucoupe."),
            ("enfant-f", "Nino, vite !"),
            ("copain", "J'arrive près des clochettes."),
            ("papa", "L'anneau d'abord, sous ton bras."),
        ),
        question=L(
            ("narrateur", "Le bois cache le coude, un instant."),
            ("maman", "Elle a mis l'anneau où ?"),
        ),
        confirm=L(
            ("enfant-f", "Sous le bras."),
            ("maman", "Oui, contre le pull."),
            ("narrateur", "L'anneau de bois cache le coude."),
            ("narrateur", "Le pull de Nino s'arrête trop haut."),
            ("papa", "On y va, tous les quatre ?"),
            ("enfant-f", "Oui."),
            ("copain", "Ça sent le tiède."),
            ("maman", "La chambre est tiède, autour."),
        ),
        choice=L(
            ("narrateur", "L'anneau tape le coude, un peu rêche."),
            ("narrateur", "Au crochet de la porte, c'est trop haut."),
            ("narrateur", "Au pied du lit, Nino cognerait."),
            ("narrateur", "Près du loquet, le vent pourrait sonner."),
            ("papa", "Vous les accrochez où, pour Nino ?"),
        ),
    ),
}


def t2_hook(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Chouchou lève la soucoupe, trop loin du crochet."),
            ("copain", "Moi je l'atteins, Chouchou !"),
            ("narrateur", "Nino se hausse, le front contre le bois."),
            ("narrateur", "Une clochette tinte, puis retombe dans la paume."),
            ("enfant-f", "Tes cheveux touchent, pas moi."),
            ("maman", "Ses bras vont jusqu'au crochet."),
            ("papa", "Toi tu vois la poignée, lui le haut."),
            ("copain", "Ça va sonner sur mon front."),
            ("enfant-f", "On fait comment, alors ?"),
            ("papa", "Vous les mettez à quelle hauteur ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Chouchou lève le ruban, trop court pour le crochet."),
            ("copain", "Moi je l'atteins, Chouchou !"),
            ("narrateur", "Nino se hausse, le front contre le bois."),
            ("narrateur", "Le satin glisse, sans accrocher le métal."),
            ("enfant-f", "Le ruban n'attendait pas ça."),
            ("maman", "Ses bras vont jusqu'au crochet."),
            ("papa", "Toi tu vois la poignée, lui le haut."),
            ("copain", "Ça va sonner sur mon front."),
            ("enfant-f", "On fait comment, alors ?"),
            ("papa", "Vous les mettez à quelle hauteur ?"),
        )
    return L(
        ("narrateur", "Chouchou lève l'anneau, trop bas pour le crochet."),
        ("copain", "Moi je l'atteins, Chouchou !"),
        ("narrateur", "Nino se hausse, le front contre le bois."),
        ("narrateur", "Le bois tape le chambranle, trop bas."),
        ("enfant-f", "L'anneau n'attendait pas ça."),
        ("maman", "Ses bras vont jusqu'au crochet."),
        ("papa", "Toi tu vois la poignée, lui le haut."),
        ("copain", "Ça va sonner sur mon front."),
        ("enfant-f", "On fait comment, alors ?"),
        ("papa", "Vous les mettez à quelle hauteur ?"),
    )


def t2_bed(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Chouchou pose la soucoupe au pied du lit."),
            ("enfant-f", "Ici, c'est à ma hauteur, Nino."),
            ("copain", "Je m'assois, trop large !"),
            ("narrateur", "Sa hanche heurte le métal, ding."),
            ("narrateur", "Les clochettes s'emmêlent dans la couverture."),
            ("maman", "Ses genoux arrivent au bois."),
            ("papa", "Toi tu noues, lui il cogne."),
            ("enfant-f", "On peut sonner avec lui ?"),
            ("papa", "Comment sonner, sans cogner ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Chouchou noue le ruban au pied du lit."),
            ("enfant-f", "Ici, c'est à ma hauteur, Nino."),
            ("copain", "Je m'assois, trop large !"),
            ("narrateur", "Sa hanche heurte le métal, ding."),
            ("narrateur", "Le satin se coince sous le matelas."),
            ("maman", "Ses genoux arrivent au bois."),
            ("papa", "Toi tu noues, lui il cogne."),
            ("enfant-f", "On peut sonner avec lui ?"),
            ("papa", "Comment sonner, sans cogner ?"),
        )
    return L(
        ("narrateur", "Chouchou glisse l'anneau au pied du lit."),
        ("enfant-f", "Ici, c'est à ma hauteur, Nino."),
        ("copain", "Je m'assois, trop large !"),
        ("narrateur", "Sa hanche heurte le métal, ding."),
        ("narrateur", "L'anneau roule, puis bute contre un pied."),
        ("maman", "Ses genoux arrivent au bois."),
        ("papa", "Toi tu noues, lui il cogne."),
        ("enfant-f", "On peut sonner avec lui ?"),
        ("papa", "Comment sonner, sans cogner ?"),
    )


def t2_window(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Chouchou porte la soucoupe vers le carreau."),
            ("enfant-f", "Ici, ça respire, Nino."),
            ("copain", "Je touche le loquet, tout haut !"),
            ("narrateur", "Le nœud reste trop loin pour Chouchou."),
            ("narrateur", "Le vent fait tinter, sans que Nino entre."),
            ("maman", "Ses coudes vont jusqu'au cadre."),
            ("papa", "Toi tu vois le bas, lui le vent."),
            ("copain", "On noue comment, alors ?"),
            ("papa", "Le nœud, vous le faites où ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Chouchou tend le ruban vers le loquet."),
            ("enfant-f", "Ici, ça respire, Nino."),
            ("copain", "Je touche le loquet, tout haut !"),
            ("narrateur", "Le nœud reste trop loin pour Chouchou."),
            ("narrateur", "Le satin claque, trop loin de ses doigts."),
            ("maman", "Ses coudes vont jusqu'au cadre."),
            ("papa", "Toi tu vois le bas, lui le vent."),
            ("copain", "On noue comment, alors ?"),
            ("papa", "Le nœud, vous le faites où ?"),
        )
    return L(
        ("narrateur", "Chouchou pousse l'anneau vers le rebord."),
        ("enfant-f", "Ici, ça respire, Nino."),
        ("copain", "Je touche le loquet, tout haut !"),
        ("narrateur", "Le nœud reste trop loin pour Chouchou."),
        ("narrateur", "L'anneau n'atteint pas le loquet."),
        ("maman", "Ses coudes vont jusqu'au cadre."),
        ("papa", "Toi tu vois le bas, lui le vent."),
        ("copain", "On noue comment, alors ?"),
        ("papa", "Le nœud, vous le faites où ?"),
    )


T2_FN = {1: t2_hook, 2: t2_bed, 3: t2_window}
T2_SONS = {1: "porte,bois", 2: "lit,laine", 3: "fenetre,vent"}
T2_EMPH = {1: "crochet", 2: "lit", 3: "loquet"}
T3_LABS = {
    1: ("les bras de Nino", "le tabouret à deux", "la poignée plus bas"),
    2: ("le pied du lit", "deux fils", "s'asseoir ensemble"),
    3: ("le loquet du bas", "tenir le cadre", "un ruban plus long"),
}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Le crochet attend, trop haut."),
            ("papa", "Les bras, le tabouret, ou la poignée ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "Le pied du lit attend, trop bas."),
            ("maman", "Le pied, deux fils, ou s'asseoir ensemble ?"),
        )
    return L(
        ("narrateur", "Le loquet attend, trop loin."),
        ("papa", "Le loquet du bas, le cadre, ou un ruban plus long ?"),
    )


T3 = {
    (1, 1, 1): L(
        ("enfant-f", "Tu noues, toi, tu vois le crochet."),
        ("narrateur", "Nino passe le ruban, assez haut."),
        ("copain", "Ça tient."),
        ("narrateur", "Chouchou tend la soucoupe, bras tout courts."),
        ("narrateur", "Elle lève la paume, pour tester."),
        ("enfant-f", "Ça sonne au-dessus de moi !"),
        ("papa", "Tes doigts allaient assez loin."),
        ("copain", "Écoute, Chouchou."),
        ("enfant-f", "Elles sont à nous."),
    ),
    (1, 1, 2): L(
        ("enfant-f", "Je monte, tu tiens."),
        ("papa", "Tiens le bois, Chouchou."),
        ("narrateur", "Chouchou se hausse, le nez au crochet."),
        ("copain", "Moi je noue, tout près."),
        ("narrateur", "Nino tient le tabouret, des deux mains."),
        ("narrateur", "Le nœud glisse, puis serre."),
        ("copain", "Tu vois, maintenant."),
        ("maman", "Vous le partagez."),
        ("enfant-f", "La soucoupe attend au bord."),
    ),
    (1, 1, 3): L(
        ("enfant-f", "On les met plus bas, à la poignée."),
        ("copain", "Moi aussi, je baisse."),
        ("narrateur", "Nino incline le front, pour passer."),
        ("narrateur", "Chouchou noue autour du métal, assez petite."),
        ("narrateur", "Les clochettes glissent vers la poignée, ding."),
        ("papa", "La poignée est venue vers vous."),
        ("copain", "On l'ouvre, ça sonne."),
        ("enfant-f", "Ça tinte, là."),
        ("maman", "Vos cheveux sentent le métal tiède."),
    ),
    (1, 2, 1): L(
        ("enfant-f", "Je noue au pied, tout bas."),
        ("copain", "Je te tends les affaires."),
        ("narrateur", "Chouchou s'agenouille, assez petite."),
        ("narrateur", "Le bois du lit s'ouvre, un peu."),
        ("enfant-f", "Je le tiens !"),
        ("narrateur", "Nino pose la soucoupe au pied du bois."),
        ("papa", "Tes hanches étaient à la bonne hauteur."),
        ("copain", "Passe-le, un peu."),
        ("enfant-f", "Il sent la lavande."),
    ),
    (1, 2, 2): L(
        ("enfant-f", "On met deux fils, ici."),
        ("copain", "Un haut pour moi, un bas pour toi."),
        ("narrateur", "Chouchou tend les clochettes, bras tout courts."),
        ("narrateur", "Deux rubans font deux hauteurs, côte à côte."),
        ("narrateur", "Nino passe dessous, Chouchou noue devant."),
        ("copain", "Je l'entends !"),
        ("maman", "Vos fils ont trouvé le chemin."),
        ("enfant-f", "Ça sent le satin."),
        ("papa", "Le lit a deux voix, maintenant."),
    ),
    (1, 2, 3): L(
        ("enfant-f", "Assieds-toi, Nino, près de moi."),
        ("copain", "Je me baisse, à ta hauteur."),
        ("narrateur", "Les genoux de Nino rejoignent les siens."),
        ("narrateur", "Chouchou noue, Nino tient le satin."),
        ("narrateur", "Les clochettes deviennent un nid, contre le bois."),
        ("copain", "On se parle tout près."),
        ("enfant-f", "Oui."),
        ("maman", "Vous y arrivez, tous les deux."),
        ("papa", "Deux voix tiennent le même tintement."),
    ),
    (1, 3, 1): L(
        ("copain", "Je me hausse, moi, en haut."),
        ("narrateur", "Chouchou garde la soucoupe au bas du cadre."),
        ("narrateur", "Les doigts de Chouchou touchent le loquet du bas."),
        ("enfant-f", "Il bouge !"),
        ("narrateur", "Le nœud penche, puis s'accroche."),
        ("copain", "Je tiens le haut."),
        ("papa", "Tes doigts allaient assez près."),
        ("maman", "Nino tenait bien le cadre."),
        ("enfant-f", "Elles sont à nous."),
    ),
    (1, 3, 2): L(
        ("enfant-f", "Tu tiens le cadre, Nino ?"),
        ("copain", "Oui, tout ferme."),
        ("narrateur", "Chouchou pose la soucoupe contre le bois."),
        ("narrateur", "Papa veille près de la vitre, sans parler."),
        ("narrateur", "Chouchou et Nino se haussent ensemble."),
        ("enfant-f", "Je vois le nœud !"),
        ("copain", "Je le sens."),
        ("maman", "Vous avez noué ensemble."),
        ("papa", "Le cadre est resté doux."),
    ),
    (1, 3, 3): L(
        ("enfant-f", "Un ruban plus long, Nino."),
        ("copain", "Je tends, d'ici."),
        ("narrateur", "Nino tend la soucoupe, bras tout longs."),
        ("narrateur", "Nino fait glisser le satin, sans monter."),
        ("narrateur", "Le rebord prend Chouchou, puis lui."),
        ("enfant-f", "Je le tiens !"),
        ("papa", "Chacun a noué sa part."),
        ("copain", "Il sent le soir."),
        ("maman", "Vos bras n'avaient pas la même longueur."),
    ),
    (2, 1, 1): L(
        ("enfant-f", "Tu noues le rouge, toi, tu vois."),
        ("narrateur", "Nino passe le satin, assez haut."),
        ("copain", "Ça tient."),
        ("narrateur", "Chouchou tend le ruban, bras tout courts."),
        ("narrateur", "Elle lève la paume, pour tester le nœud."),
        ("enfant-f", "Ça sonne au-dessus de moi !"),
        ("papa", "Tes doigts allaient assez loin."),
        ("copain", "Écoute le rouge, Chouchou."),
        ("enfant-f", "Il est à nous."),
    ),
    (2, 1, 2): L(
        ("enfant-f", "Je monte, tu tiens le tabouret."),
        ("papa", "Tiens le bois, Chouchou."),
        ("narrateur", "Chouchou se hausse, le nez au crochet."),
        ("copain", "Moi je noue le rouge, tout près."),
        ("narrateur", "Nino tient le tabouret, des deux mains."),
        ("narrateur", "Le nœud glisse, puis serre le satin."),
        ("copain", "Tu vois le rouge, maintenant."),
        ("maman", "Vous le partagez."),
        ("enfant-f", "Le ruban attend au bord."),
    ),
    (2, 1, 3): L(
        ("enfant-f", "On le met plus bas, à la poignée."),
        ("copain", "Moi aussi, je baisse."),
        ("narrateur", "Nino incline le front, pour passer."),
        ("narrateur", "Chouchou noue le satin autour du métal."),
        ("narrateur", "Le ruban glisse vers la poignée, lisse."),
        ("papa", "La poignée est venue vers vous."),
        ("copain", "On l'ouvre, ça sonne."),
        ("enfant-f", "Ça tinte, là."),
        ("maman", "Vos cheveux sentent le métal tiède."),
    ),
    (2, 2, 1): L(
        ("enfant-f", "Je noue le rouge au pied, tout bas."),
        ("copain", "Je te tends le satin."),
        ("narrateur", "Chouchou s'agenouille, assez petite."),
        ("narrateur", "Le bois du lit s'ouvre, un peu."),
        ("enfant-f", "Je le tiens !"),
        ("narrateur", "Nino pose le ruban au pied du bois."),
        ("papa", "Tes hanches étaient à la bonne hauteur."),
        ("copain", "Passe-le, un peu."),
        ("enfant-f", "Il sent la lavande."),
    ),
    (2, 2, 2): L(
        ("enfant-f", "On met deux fils, ici."),
        ("copain", "Un haut pour moi, un bas pour toi."),
        ("narrateur", "Chouchou tend le ruban, bras tout courts."),
        ("narrateur", "Deux satins font deux hauteurs, côte à côte."),
        ("narrateur", "Nino passe dessous, Chouchou noue devant."),
        ("copain", "Je l'entends !"),
        ("maman", "Vos fils ont trouvé le chemin."),
        ("enfant-f", "Ça sent le satin."),
        ("papa", "Le lit a deux voix, maintenant."),
    ),
    (2, 2, 3): L(
        ("enfant-f", "Assieds-toi, Nino, près de moi."),
        ("copain", "Je me baisse, à ta hauteur."),
        ("narrateur", "Les genoux de Nino rejoignent les siens."),
        ("narrateur", "Chouchou noue, Nino tient le satin."),
        ("narrateur", "Le ruban devient un nid, contre le bois."),
        ("copain", "On se parle tout près."),
        ("enfant-f", "Oui."),
        ("maman", "Vous y arrivez, tous les deux."),
        ("papa", "Deux voix tiennent le même tintement."),
    ),
    (2, 3, 1): L(
        ("copain", "Je me hausse, moi, en haut."),
        ("narrateur", "Chouchou garde le ruban au bas du cadre."),
        ("narrateur", "Les doigts de Chouchou touchent le loquet du bas."),
        ("enfant-f", "Il bouge !"),
        ("narrateur", "Le nœud penche, puis s'accroche."),
        ("copain", "Je tiens le haut."),
        ("papa", "Tes doigts allaient assez près."),
        ("maman", "Nino tenait bien le cadre."),
        ("enfant-f", "Il est à nous."),
    ),
    (2, 3, 2): L(
        ("enfant-f", "Tu tiens le cadre, Nino ?"),
        ("copain", "Oui, tout ferme."),
        ("narrateur", "Chouchou pose le ruban contre le bois."),
        ("narrateur", "Papa veille près de la vitre, sans parler."),
        ("narrateur", "Chouchou et Nino se haussent ensemble."),
        ("enfant-f", "Je vois le nœud !"),
        ("copain", "Je le sens."),
        ("maman", "Vous avez noué ensemble."),
        ("papa", "Le cadre est resté doux."),
    ),
    (2, 3, 3): L(
        ("enfant-f", "Un ruban plus long, Nino."),
        ("copain", "Je tends, d'ici."),
        ("narrateur", "Nino tend le satin, bras tout longs."),
        ("narrateur", "Nino fait glisser le rouge, sans monter."),
        ("narrateur", "Le rebord prend Chouchou, puis lui."),
        ("enfant-f", "Je le tiens !"),
        ("papa", "Chacun a noué sa part."),
        ("copain", "Il sent le soir."),
        ("maman", "Vos bras n'avaient pas la même longueur."),
    ),
    (3, 1, 1): L(
        ("enfant-f", "Tu noues, toi, tu vois le crochet."),
        ("narrateur", "Nino passe l'anneau, assez haut."),
        ("copain", "Ça tient."),
        ("narrateur", "Chouchou pousse l'anneau, tout près."),
        ("narrateur", "Elle lève la paume, pour tester le bois."),
        ("enfant-f", "Ça sonne au-dessus de moi !"),
        ("papa", "Tes doigts allaient assez loin."),
        ("copain", "Écoute, Chouchou."),
        ("enfant-f", "Il est à nous."),
    ),
    (3, 1, 2): L(
        ("enfant-f", "Je monte, tu tiens."),
        ("papa", "Tiens le bois, Chouchou."),
        ("narrateur", "Chouchou se hausse, le nez au crochet."),
        ("copain", "Moi je noue, tout près."),
        ("narrateur", "Nino tient le tabouret, des deux mains."),
        ("narrateur", "Le nœud glisse, puis serre l'anneau."),
        ("copain", "Tu vois, maintenant."),
        ("maman", "Vous le partagez."),
        ("enfant-f", "L'anneau attend au bord."),
    ),
    (3, 1, 3): L(
        ("enfant-f", "On le met plus bas, à la poignée."),
        ("copain", "Moi aussi, je baisse."),
        ("narrateur", "Nino incline le front, pour passer."),
        ("narrateur", "Chouchou noue l'anneau autour du métal."),
        ("narrateur", "L'anneau glisse vers la poignée, toc."),
        ("papa", "La poignée est venue vers vous."),
        ("copain", "On l'ouvre, ça sonne."),
        ("enfant-f", "Ça tinte, là."),
        ("maman", "Vos cheveux sentent le métal tiède."),
    ),
    (3, 2, 1): L(
        ("enfant-f", "Je noue au pied, tout bas."),
        ("copain", "Je te tends l'anneau."),
        ("narrateur", "Chouchou s'agenouille, assez petite."),
        ("narrateur", "Le bois du lit s'ouvre, un peu."),
        ("enfant-f", "Je le tiens !"),
        ("narrateur", "Nino pose l'anneau au pied du bois."),
        ("papa", "Tes hanches étaient à la bonne hauteur."),
        ("copain", "Passe-le, un peu."),
        ("enfant-f", "Il sent le tiède."),
    ),
    (3, 2, 2): L(
        ("enfant-f", "On met deux fils, ici."),
        ("copain", "Un haut pour moi, un bas pour toi."),
        ("narrateur", "Chouchou pousse l'anneau, tout près."),
        ("narrateur", "Deux fils font deux hauteurs, côte à côte."),
        ("narrateur", "Nino passe dessous, Chouchou noue devant."),
        ("copain", "Je l'entends !"),
        ("maman", "Vos fils ont trouvé le chemin."),
        ("enfant-f", "Ça sent le bois."),
        ("papa", "Le lit a deux voix, maintenant."),
    ),
    (3, 2, 3): L(
        ("enfant-f", "Assieds-toi, Nino, près de moi."),
        ("copain", "Je me baisse, à ta hauteur."),
        ("narrateur", "Les genoux de Nino rejoignent les siens."),
        ("narrateur", "Chouchou noue, Nino tient le satin."),
        ("narrateur", "L'anneau devient un nid, contre le bois."),
        ("copain", "On se parle tout près."),
        ("enfant-f", "Oui."),
        ("maman", "Vous y arrivez, tous les deux."),
        ("papa", "Deux voix tiennent le même tintement."),
    ),
    (3, 3, 1): L(
        ("copain", "Je me hausse, moi, en haut."),
        ("narrateur", "Chouchou garde l'anneau au bas du cadre."),
        ("narrateur", "Les doigts de Chouchou touchent le loquet du bas."),
        ("enfant-f", "Il bouge !"),
        ("narrateur", "Le nœud penche, puis s'accroche."),
        ("copain", "Je tiens le haut."),
        ("papa", "Tes doigts allaient assez près."),
        ("maman", "Nino tenait bien le cadre."),
        ("enfant-f", "Il est à nous."),
    ),
    (3, 3, 2): L(
        ("enfant-f", "Tu tiens le cadre, Nino ?"),
        ("copain", "Oui, tout ferme."),
        ("narrateur", "Chouchou pousse l'anneau, tout près."),
        ("narrateur", "Papa veille près de la vitre, sans parler."),
        ("narrateur", "Chouchou et Nino se haussent ensemble."),
        ("enfant-f", "Je vois le nœud !"),
        ("copain", "Je le sens."),
        ("maman", "Vous avez noué ensemble."),
        ("papa", "Le cadre est resté doux."),
    ),
    (3, 3, 3): L(
        ("enfant-f", "Un ruban plus long, Nino."),
        ("copain", "Je tends, d'ici."),
        ("narrateur", "Nino pousse l'anneau, tout près."),
        ("narrateur", "Nino fait glisser le satin, sans monter."),
        ("narrateur", "Le rebord prend Chouchou, puis lui."),
        ("enfant-f", "Je le tiens !"),
        ("papa", "Chacun a noué sa part."),
        ("copain", "Il sent le soir."),
        ("maman", "Vos bras n'avaient pas la même longueur."),
    ),
}

FIN = {
    (1, 1, 1): L(
        ("narrateur", "Au crochet, la porte sent le bois chaud."),
        ("copain", "Tu as tendu, moi j'ai noué."),
        ("enfant-f", "Tes bras l'ont fait pendre."),
        ("papa", "Vous l'avez, enfin."),
        ("maman", "La chemise pliée dort sur la chaise."),
        ("narrateur", "Les clochettes pendent au-dessus du seuil."),
        ("enfant-f", "On reste un peu, Nino."),
        ("narrateur", "Un tintement s'endort sur le plancher."),
        ("narrateur", "La barre jaune s'endort sur les clochettes."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Sur le tabouret, deux têtes se calment."),
        ("enfant-f", "Nino, tu l'as vue glisser."),
        ("copain", "Oui, tout près de tes mains."),
        ("papa", "Toi haute, lui qui noue, ça tenait."),
        ("maman", "Vos voix sont devenues toutes petites."),
        ("narrateur", "Les clochettes restent dans la paume de Chouchou."),
        ("copain", "Je reste un peu."),
        ("enfant-f", "Tes cheveux sentent le bois."),
        ("narrateur", "Une poussière dore les cheveux, sous l'abat-jour."),
    ),
    (1, 1, 3): L(
        ("narrateur", "La poignée redescend, sans bruit."),
        ("copain", "Ça sonne dès qu'on tourne."),
        ("enfant-f", "On a baissé, tous les deux."),
        ("maman", "Elles n'étaient plus trop hautes."),
        ("papa", "Le métal froisse, dans l'air."),
        ("narrateur", "Les clochettes retombent, légères."),
        ("enfant-f", "On souffle dessus."),
        ("narrateur", "Un tintement veille près des oreillers."),
        ("narrateur", "Le réverbère se tait, près de la poignée."),
    ),
    (1, 2, 1): L(
        ("narrateur", "Au pied du lit, ça sent le bois."),
        ("copain", "Mes mains savaient le chemin."),
        ("enfant-f", "Moi, je nouais trop bas."),
        ("papa", "Vous avez suivi ce qui était à vous."),
        ("maman", "Un brin de laine reste au pull."),
        ("narrateur", "Les clochettes gardent un brin de laine."),
        ("enfant-f", "Elles sont pour demain."),
        ("copain", "Elles sont un peu chaudes."),
        ("narrateur", "L'ombre du lit coupe la barre jaune."),
    ),
    (1, 2, 2): L(
        ("narrateur", "Les deux fils restent, comme deux voix."),
        ("enfant-f", "J'ai noué d'en bas."),
        ("copain", "Tes bras étaient assez courts."),
        ("maman", "Le satin sent fort, sur vos mains."),
        ("papa", "Frottez-les sur le tapis."),
        ("narrateur", "Les clochettes gardent un brin de laine."),
        ("copain", "Je le tiens, Chouchou."),
        ("narrateur", "Un pied de bois grince, puis se tait."),
        ("narrateur", "Le satin rouge sèche au bord du tapis."),
    ),
    (1, 2, 3): L(
        ("narrateur", "Une voix basse, une voix plus haute."),
        ("enfant-f", "Nino s'est assis à ma hauteur."),
        ("copain", "On a noué tout près."),
        ("papa", "Le lit vous a laissé la place."),
        ("maman", "Le secret tient, tout chaud."),
        ("narrateur", "Les clochettes marquent le bois."),
        ("enfant-f", "Écoute-les, Nino, elles brillent."),
        ("copain", "Je les entends, d'ici."),
        ("narrateur", "Le métal garde un brin de laine, sur le drap."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Les talons de Nino sont chauds."),
        ("enfant-f", "Tu as tenu le haut pour moi."),
        ("copain", "Tu nouais le bas."),
        ("maman", "Le carreau sent le soir, tout près."),
        ("papa", "La porte sonnera, demain."),
        ("enfant-f", "Je les pose contre la vitre."),
        ("narrateur", "Les clochettes pèsent sur le loquet."),
        ("copain", "Le jaune de la rue les touche."),
        ("narrateur", "Un rai jaune traverse le loquet."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Sur le rebord, deux paires de pieds se touchent."),
        ("copain", "Tu as noué, d'en bas."),
        ("enfant-f", "Tes bras ont tenu le cadre."),
        ("papa", "Chacun a fait sa part, à sa hauteur."),
        ("maman", "Le satin du ruban sèche."),
        ("narrateur", "Les clochettes posent une ombre au plancher."),
        ("copain", "Ça tinte trop, Chouchou."),
        ("enfant-f", "C'est pour ça."),
        ("narrateur", "La vitre garde une ombre rouge, mince."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Un peu de buée reste au carreau."),
        ("enfant-f", "On a tiré ensemble."),
        ("copain", "Sans trop monter."),
        ("papa", "Le rebord est resté à sa place."),
        ("maman", "Vos mains sentent le soir."),
        ("narrateur", "Chouchou pose les clochettes au rebord."),
        ("copain", "Tu les as eues, enfin."),
        ("enfant-f", "Elles sont à nous."),
        ("narrateur", "Le métal tremble, puis s'endort au rebord."),
    ),
    (2, 1, 1): L(
        ("narrateur", "Au crochet, la porte sent le bois chaud."),
        ("copain", "Tu as tendu, moi j'ai noué."),
        ("enfant-f", "Tes bras l'ont fait pendre."),
        ("papa", "Vous l'avez, enfin."),
        ("maman", "La chemise pliée dort sur la chaise."),
        ("narrateur", "Le ruban rouge pèse au-dessus du seuil."),
        ("enfant-f", "On reste un peu, Nino."),
        ("narrateur", "Un tintement s'endort sur le plancher."),
        ("narrateur", "La barre jaune pèse sur le nœud rouge."),
    ),
    (2, 1, 2): L(
        ("narrateur", "Sur le tabouret, deux têtes se calment."),
        ("enfant-f", "Nino, tu l'as vue glisser."),
        ("copain", "Oui, tout près de tes mains."),
        ("papa", "Toi haute, lui qui noue, ça tenait."),
        ("maman", "Vos voix sont devenues toutes petites."),
        ("narrateur", "Le ruban reste dans la paume de Chouchou."),
        ("copain", "Je reste un peu."),
        ("enfant-f", "Une mèche à toi, sur le bois."),
        ("narrateur", "Le tabouret garde une mèche, dans l'ombre jaune."),
    ),
    (2, 1, 3): L(
        ("narrateur", "La poignée redescend, sans bruit."),
        ("copain", "Ça sonne dès qu'on tourne."),
        ("enfant-f", "On a baissé, tous les deux."),
        ("maman", "Elles n'étaient plus trop hautes."),
        ("papa", "Le métal froisse, dans l'air."),
        ("narrateur", "Le ruban rouge retombe, léger."),
        ("enfant-f", "On souffle dessus."),
        ("narrateur", "Un tintement veille près des oreillers."),
        ("narrateur", "La poignée tient un fil rouge, tiède."),
    ),
    (2, 2, 1): L(
        ("narrateur", "Au pied du lit, ça sent le bois."),
        ("copain", "Mes mains savaient le chemin."),
        ("enfant-f", "Moi, je nouais trop bas."),
        ("papa", "Vous avez suivi ce qui était à vous."),
        ("maman", "Un brin de laine reste au pull."),
        ("narrateur", "Le ruban rouge garde un brin de laine."),
        ("enfant-f", "Elles sont pour demain."),
        ("copain", "Elles sont un peu chaudes."),
        ("narrateur", "Un brin de laine croise la barre jaune."),
    ),
    (2, 2, 2): L(
        ("narrateur", "Les deux fils restent, comme deux voix."),
        ("enfant-f", "J'ai noué d'en bas."),
        ("copain", "Tes bras étaient assez courts."),
        ("maman", "Le satin sent fort, sur vos mains."),
        ("papa", "Frottez-les sur le tapis."),
        ("narrateur", "Le ruban garde un brin de laine."),
        ("copain", "Je le tiens, Chouchou."),
        ("narrateur", "Un pied de bois grince, puis se tait."),
        ("narrateur", "Deux fils gardent deux ombres, sur le plancher."),
    ),
    (2, 2, 3): L(
        ("narrateur", "Une voix basse, une voix plus haute."),
        ("enfant-f", "Nino s'est assis à ma hauteur."),
        ("copain", "On a noué tout près."),
        ("papa", "Le lit vous a laissé la place."),
        ("maman", "Le secret tient, tout chaud."),
        ("narrateur", "Le ruban rouge marque le bois."),
        ("enfant-f", "Écoute-les, Nino, elles brillent."),
        ("copain", "Je les entends, d'ici."),
        ("narrateur", "Deux genoux touchent, dans la barre jaune."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Les talons de Nino sont chauds."),
        ("enfant-f", "Tu as tenu le haut pour moi."),
        ("copain", "Tu nouais le bas."),
        ("maman", "Le carreau sent le soir, tout près."),
        ("papa", "La porte sonnera, demain."),
        ("enfant-f", "Je pose le rouge contre la vitre."),
        ("narrateur", "Le ruban rouge veille au loquet."),
        ("copain", "La rue le dore, un peu."),
        ("narrateur", "Le loquet pèse, doré par la rue."),
    ),
    (2, 3, 2): L(
        ("narrateur", "Sur le rebord, deux paires de pieds se touchent."),
        ("copain", "Tu as noué, d'en bas."),
        ("enfant-f", "Tes bras ont tenu le cadre."),
        ("papa", "Chacun a fait sa part, à sa hauteur."),
        ("maman", "Le satin du ruban sèche."),
        ("narrateur", "Le ruban pose une ombre au plancher."),
        ("copain", "Ça tinte trop, Chouchou."),
        ("enfant-f", "C'est pour ça."),
        ("narrateur", "Le satin laisse un trait rouge, au rebord."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Un peu de buée reste au carreau."),
        ("enfant-f", "On a tiré ensemble."),
        ("copain", "Sans trop monter."),
        ("papa", "Le rebord est resté à sa place."),
        ("maman", "Vos mains sentent le soir."),
        ("narrateur", "Chouchou pose le ruban au rebord."),
        ("copain", "Tu les as eues, enfin."),
        ("enfant-f", "Elles sont à nous."),
        ("narrateur", "Un peu de buée garde le rouge du soir."),
    ),
    (3, 1, 1): L(
        ("narrateur", "Au crochet, la porte sent le bois chaud."),
        ("copain", "Tu as tendu, moi j'ai noué."),
        ("enfant-f", "Tes bras l'ont fait pendre."),
        ("papa", "Vous l'avez, enfin."),
        ("maman", "La chemise pliée dort sur la chaise."),
        ("narrateur", "L'anneau de bois veille au-dessus du seuil."),
        ("enfant-f", "On reste un peu, Nino."),
        ("narrateur", "Un tintement s'endort sur le plancher."),
        ("narrateur", "L'anneau de bois veille dans la barre jaune."),
    ),
    (3, 1, 2): L(
        ("narrateur", "Sur le tabouret, deux têtes se calment."),
        ("enfant-f", "Nino, tu l'as vue glisser."),
        ("copain", "Oui, tout près de tes mains."),
        ("papa", "Toi haute, lui qui noue, ça tenait."),
        ("maman", "Vos voix sont devenues toutes petites."),
        ("narrateur", "L'anneau reste dans la paume de Chouchou."),
        ("copain", "Je reste un peu."),
        ("enfant-f", "Il a pris ta poussière, Nino."),
        ("narrateur", "Le tabouret sent le bois, sous la lumière."),
    ),
    (3, 1, 3): L(
        ("narrateur", "La poignée redescend, sans bruit."),
        ("copain", "Ça sonne dès qu'on tourne."),
        ("enfant-f", "On a baissé, tous les deux."),
        ("maman", "Elles n'étaient plus trop hautes."),
        ("papa", "Le métal froisse, dans l'air."),
        ("narrateur", "L'anneau de bois retombe, léger."),
        ("enfant-f", "On souffle dessus."),
        ("narrateur", "Un tintement veille près des oreillers."),
        ("narrateur", "La poignée sonne, et le plancher dore."),
    ),
    (3, 2, 1): L(
        ("narrateur", "Au pied du lit, ça sent le bois."),
        ("copain", "Mes mains savaient le chemin."),
        ("enfant-f", "Moi, je nouais trop bas."),
        ("papa", "Vous avez suivi ce qui était à vous."),
        ("maman", "Un brin de laine reste au pull."),
        ("narrateur", "L'anneau de bois garde un brin de laine."),
        ("enfant-f", "Elles sont pour demain."),
        ("copain", "Elles sont un peu chaudes."),
        ("narrateur", "L'anneau garde un brin de laine, au pied."),
    ),
    (3, 2, 2): L(
        ("narrateur", "Les deux fils restent, comme deux voix."),
        ("enfant-f", "J'ai noué d'en bas."),
        ("copain", "Tes bras étaient assez courts."),
        ("maman", "Le satin sent fort, sur vos mains."),
        ("papa", "Frottez-les sur le tapis."),
        ("narrateur", "L'anneau garde un brin de laine."),
        ("copain", "Je le tiens, Chouchou."),
        ("narrateur", "Un pied de bois grince, puis se tait."),
        ("narrateur", "Deux hauteurs, deux ombres, un seul bois."),
    ),
    (3, 2, 3): L(
        ("narrateur", "Une voix basse, une voix plus haute."),
        ("enfant-f", "Nino s'est assis à ma hauteur."),
        ("copain", "On a noué tout près."),
        ("papa", "Le lit vous a laissé la place."),
        ("maman", "Le secret tient, tout chaud."),
        ("narrateur", "L'anneau de bois marque le pied."),
        ("enfant-f", "Écoute-les, Nino, elles brillent."),
        ("copain", "Je les entends, d'ici."),
        ("narrateur", "L'anneau marque le pied, dans la lumière."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Les talons de Nino sont chauds."),
        ("enfant-f", "Tu as tenu le haut pour moi."),
        ("copain", "Tu nouais le bas."),
        ("maman", "Le carreau sent le soir, tout près."),
        ("papa", "La porte sonnera, demain."),
        ("enfant-f", "Je pose l'anneau contre la vitre."),
        ("narrateur", "L'anneau de bois veille au loquet."),
        ("copain", "Mes talons sont chauds, là."),
        ("narrateur", "Les talons de Nino restent chauds, au loquet."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Sur le rebord, deux paires de pieds se touchent."),
        ("copain", "Tu as noué, d'en bas."),
        ("enfant-f", "Tes bras ont tenu le cadre."),
        ("papa", "Chacun a fait sa part, à sa hauteur."),
        ("maman", "Le satin du ruban sèche."),
        ("narrateur", "L'anneau pose une ombre au plancher."),
        ("copain", "Ça tinte trop, Chouchou."),
        ("enfant-f", "C'est pour ça."),
        ("narrateur", "Une ombre d'anneau tombe au plancher."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Un peu de buée reste au carreau."),
        ("enfant-f", "On a tiré ensemble."),
        ("copain", "Sans trop monter."),
        ("papa", "Le rebord est resté à sa place."),
        ("maman", "Vos mains sentent le soir."),
        ("narrateur", "Chouchou pose l'anneau au rebord."),
        ("copain", "Tu les as eues, enfin."),
        ("enfant-f", "Elles sont à nous."),
        ("narrateur", "L'anneau s'endort au rebord, dans le jaune."),
    ),
}

T3_SONS = {1: "clochette,bois", 2: "tabouret,tissu", 3: "poignee,vent"}
FIN_SONS = {1: "reverbere,clochette", 2: "reverbere,laine", 3: "reverbere,vitre"}
T3_EMPH = {
    1: {1: "crochet", 2: "tabouret", 3: "poignée"},
    2: {1: "pied", 2: "fils", 3: "genoux"},
    3: {1: "loquet", 2: "cadre", 3: "ruban"},
}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "reverbere,clochette", "emphasis": "clochettes"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Trois affaires attendent près du tapis."),
            ("papa", "Les clochettes, le ruban, ou l'anneau ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "les clochettes",
            "option_2_label": "le ruban rouge",
            "option_3_label": "l'anneau de bois",
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
                "engine_near_text": "Tu es tout près. Reprenons l'indice.",
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
                "option_1_label": "au crochet de la porte",
                "option_2_label": "au pied du lit",
                "option_3_label": "au loquet de la fenêtre",
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
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], FIN[(a, b, c)], "ending",
                    extra={"sons": FIN_SONS[c], "emphasis": "barre jaune"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")

    out = dict(src)
    out["fil_rouge"] = (
        "Le soir, une barre jaune du réverbère traverse le plancher. "
        "Chouchou veut accrocher trois clochettes au-dessus de la porte, "
        "pour qu'elles sonnent quand Nino entre. Elle se hausse : trop court, "
        "une clochette glisse. Elle reprend par les clochettes, le ruban rouge "
        "ou l'anneau de bois. Au crochet trop haut, au pied du lit trop bas, "
        "au loquet trop loin : Nino est plus grand. Ils nouent avec ses bras, "
        "un tabouret, une poignée plus bas ; le pied, deux fils, s'asseoir ; "
        "le loquet du bas, le cadre, un ruban plus long. La barre jaune "
        "s'endort sur le tintement."
    )
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
    if n_enc > 2 or n_dej > 2:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob or "nino" not in blob:
        raise SystemExit("troupe Chouchou/Nino absente")
    for bad in (
        "escargot", "loupe", "carnet bleu", "pots de menthe", "trace d'argent",
        "prunier", "carillon", "bocal", "grelot", "coccinelle",
        "bac à sable", "toboggan", "balançoire", "sami", "léa", "lea ",
        "tom ", "drap à pois", "cabane", "cacao", "étoile", "loup de carton",
        "camp", "doudou", "ballon", "seau", "capitaine", "plic",
        "volet jaune", "pommier", "la première", "la deuxième", "la troisième",
        "bravo tu as", "bon travail",
    ):
        if bad in whole:
            raise SystemExit(f"calque: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Chambre le soir : barre jaune du réverbère, savon tiède, soucoupe. "
        "Chouchou veut accrocher trois clochettes au-dessus de la porte, pour "
        "que Nino (plus grand) les fasse sonner en entrant, maintenant. Elle se "
        "hausse : trop court, une clochette glisse, papa remercie qu'elle ait "
        "rattrapé la soucoupe. T1 change le premier geste (soucoupe trop haute "
        "/ ruban lancé trop court / anneau trop bas). T2 : trois hauteurs "
        "(crochet trop haut, front de Nino ; pied du lit trop bas, hanche ; "
        "loquet trop loin, le vent tinte sans lui). T3 change la façon de jouer "
        "à deux tailles : bras de Nino, tabouret à deux, poignée plus bas ; "
        "pied, deux fils, s'asseoir ; loquet du bas, cadre, ruban plus long. "
        "La leçon se vit dans les hauteurs, sans slogan. Chaque fin paie la "
        "barre jaune et le tintement. Autre récit que TREE-DIF-032 (cabane, "
        "drap à pois) et TREE-DIF-042 (cacao, étagère).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N3 ≤ 16. Troupe D16 : Chouchou, Nino, papa, maman.\n"
        "- Léa et le slogan « Plus petit ou plus grand » jetés. Première idée "
        "échoue (pointe, clochette au plancher).\n"
        "- 27 fins textuellement distinctes. Un merci vécu (rattraper la soucoupe), "
        "pas un refrain Bravo.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/"
        "resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n"
        "- Tics « tout doux / tout calme / encore / déjà » écartés. "
        "Deux rythmes : Chouchou propose, Nino atteint trop haut.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
