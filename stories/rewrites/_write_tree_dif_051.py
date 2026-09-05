#!/usr/bin/env python3
"""TREE-DIF-051 — Les deux voyageurs de Chouchou, jusqu'au tunnel (F-NAR-019, N3)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-051"
LIM = 16
TITLE = "Les deux voyageurs de Chouchou, jusqu'au tunnel"
CHARS = "Chouchou, papa, maman"
SETTING = "gare de colline, train de montagne : filet, banquette, passage"
TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "plus rond ou plus mince",
    "corps pas une blague",
    "l'histoire est finie",
    "il faut attendre",
    "bravo tu as",
    "bon travail",
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=les_deux_doivent_voir_le_tunnel; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_a_pris; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_montent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=elle_prend_trop_vite_un_seul; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; intensite=2; destinataire=enfant; sous_texte=ils_se_séparent_sans_blague; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=garder_les_deux_ensemble; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_noir_puis_la_neige; tempo=posé; sourire=léger; respiration=ample",
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
    ("narrateur", "Sous le pont de pierre, l'eau frappe les galets."),
    ("narrateur", "La petite gare sent le fer mouillé et les feuilles."),
    ("narrateur", "Une lampe jaune tremble sur le quai."),
    ("narrateur", "La colline a mangé le dernier soleil."),
    ("narrateur", "Chouchou vit ici, avec papa et maman."),
    ("narrateur", "Le thermos de cacao chauffe le sac de laine."),
    ("maman", "Le cacao sent le sucre, Chouchou."),
    ("papa", "Le train de montagne arrive, lentement."),
    ("enfant-f", "Mes deux voyageurs vont voir le tunnel."),
    ("narrateur", "En ce moment, Chouchou ouvre le sac de laine."),
    ("narrateur", "Le hérisson rond pèse dans sa paume."),
    ("narrateur", "Le renard de bois glisse entre les doigts."),
    ("enfant-f", "Toi d'abord, tu es plus facile !"),
    ("narrateur", "Le renard tombe dans un pli du sac."),
    ("enfant-f", "Je t'ai perdu !"),
    ("narrateur", "Elle fouille, les joues chaudes, le cœur serré."),
    ("papa", "Merci, tu l'as repris avec l'autre."),
    ("maman", "On prend les affaires, avant la marche."),
    ("enfant-f", "Vous voyez le tunnel, tous les deux."),
)

T1 = {
    1: dict(
        name="le châle bleu",
        expected="autour",
        accepted="autour | autour d'eux | autour des deux | sur eux | le châle",
        retry="Le châle est autour des deux.",
        ok="Oui, il est autour d'eux.",
        sons="laine,sac",
        emphasis="châle",
        passage=L(
            ("narrateur", "Chouchou saisit le châle bleu, tiède du sac."),
            ("enfant-f", "Il sent la maison."),
            ("narrateur", "Elle enroule d'abord le hérisson, trop vite."),
            ("narrateur", "Le museau du renard reste dehors, oublié."),
            ("enfant-f", "Attends, toi aussi."),
            ("maman", "Enroule-les ensemble, les deux."),
            ("narrateur", "Le bleu recouvre le bois et la laine ronde."),
            ("papa", "La boîte et la ficelle viennent dans le sac."),
            ("narrateur", "Deux têtes dépassent, l'une ronde, l'autre fine."),
            ("enfant-f", "Je vois mes voyageurs."),
            ("narrateur", "Châle, boîte et ficelle montent avec elle."),
        ),
        question=L(
            ("narrateur", "Le châle bleu tient les deux voyageurs."),
            ("maman", "Il est où, maintenant ?"),
        ),
        confirm=L(
            ("enfant-f", "Autour d'eux."),
            ("papa", "Deux têtes regardent la marche."),
            ("maman", "Tu tiens le paquet contre toi ?"),
            ("enfant-f", "Oui, maman."),
            ("narrateur", "Le cacao sent le sucre, dans le thermos."),
            ("narrateur", "La marche du train est haute, un peu froide."),
        ),
        choice=L(
            ("narrateur", "Le wagon sent le cacao et le fer chaud."),
            ("narrateur", "Un filet pend au-dessus des sièges."),
            ("narrateur", "La banquette brille, lisse comme une pierre."),
            ("narrateur", "Le passage entre les voitures souffle."),
            ("papa", "On les pose où, pour attendre le tunnel ?"),
        ),
    ),
    2: dict(
        name="la boîte à biscuits",
        expected="genoux",
        accepted="genoux | les genoux | sur les genoux | la boîte",
        retry="La boîte est sur les genoux.",
        ok="Oui, sur les genoux.",
        sons="boite,clic",
        emphasis="boîte",
        passage=L(
            ("narrateur", "Chouchou ouvre la boîte à biscuits, clic."),
            ("enfant-f", "Ça sent le beurre."),
            ("narrateur", "Le hérisson prend presque toute la place."),
            ("narrateur", "Elle pousse le couvercle, trop tôt."),
            ("enfant-f", "Le renard n'est pas dedans !"),
            ("papa", "Pose-les côte à côte, les deux."),
            ("narrateur", "Le bois mince se glisse le long du bord."),
            ("maman", "Le châle viendra par-dessus, et la ficelle."),
            ("enfant-f", "Votre cabine, pour le tunnel."),
            ("narrateur", "Elle garde la boîte sur les genoux."),
            ("narrateur", "Les trois affaires montent avec elle."),
        ),
        question=L(
            ("narrateur", "La boîte à biscuits repose sur les genoux."),
            ("papa", "Elle est où, maintenant ?"),
        ),
        confirm=L(
            ("enfant-f", "Sur les genoux."),
            ("maman", "Le hérisson touche le renard, dedans."),
            ("papa", "Tu montes avec les deux mains ?"),
            ("enfant-f", "Oui, papa."),
            ("narrateur", "Une miette de beurre reste au couvercle."),
            ("narrateur", "La marche sonne sous la semelle."),
        ),
        choice=L(
            ("narrateur", "La boîte cliquette contre le genou."),
            ("narrateur", "Un filet pend au-dessus des sièges."),
            ("narrateur", "La banquette brille, lisse comme une pierre."),
            ("narrateur", "Le passage entre les voitures souffle."),
            ("maman", "On les pose où, pour attendre le tunnel ?"),
        ),
    ),
    3: dict(
        name="la ficelle de laine",
        expected="nœud",
        accepted="nœud | le nœud | un nœud | autour | la ficelle",
        retry="La ficelle fait un nœud, autour d'eux.",
        ok="Oui, un nœud.",
        sons="laine,noeud",
        emphasis="ficelle",
        passage=L(
            ("narrateur", "Chouchou saisit la ficelle de laine, un peu rêche."),
            ("enfant-f", "Elle chatouille le poignet."),
            ("narrateur", "Elle noue le hérisson, et s'arrête."),
            ("narrateur", "Le renard reste libre, trop loin."),
            ("enfant-f", "Sans toi, le nœud ne marche pas."),
            ("maman", "Un nœud autour des deux, pas d'un seul."),
            ("narrateur", "Le bois se colle contre la laine ronde."),
            ("papa", "Le châle et la boîte viennent aussi."),
            ("narrateur", "Elle glisse le paquet dans le sac."),
            ("enfant-f", "La ficelle d'abord, pour marcher ensemble."),
            ("narrateur", "Les trois affaires montent avec elle."),
        ),
        question=L(
            ("narrateur", "La ficelle de laine tient les deux voyageurs."),
            ("maman", "Elle fait quoi, autour d'eux ?"),
        ),
        confirm=L(
            ("enfant-f", "Un nœud."),
            ("papa", "Le nœud tient, sans serrer trop."),
            ("maman", "Tu gardes le sac à l'épaule ?"),
            ("enfant-f", "Oui."),
            ("narrateur", "La laine frotte le poignet, un peu tiède."),
            ("narrateur", "Le quai recule, et la marche s'éloigne."),
        ),
        choice=L(
            ("narrateur", "La ficelle tire un peu, puis se tait."),
            ("narrateur", "Un filet pend au-dessus des sièges."),
            ("narrateur", "La banquette brille, lisse comme une pierre."),
            ("narrateur", "Le passage entre les voitures souffle."),
            ("papa", "On les pose où, pour attendre le tunnel ?"),
        ),
    ),
}

T2_LABS = ("le filet", "la banquette", "le passage")
T3_LABS = {
    1: ("le nid de laine", "la boîte dans le filet", "contre soi"),
    2: ("la vallée du châle", "la maison-boîte", "la ficelle au dossier"),
    3: ("contre la poitrine", "sur la marche", "attendre le calme"),
}


def t2_filet(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Le châle bleu accroche une maille trop lâche."),
            ("enfant-f", "Vous voyez le plafond, tous les deux ?"),
            ("narrateur", "Le hérisson roule vers un trou, lent."),
            ("narrateur", "Le museau du renard glisse entre les fils."),
            ("enfant-f", "Lui il roule, lui il file !"),
            ("narrateur", "Elle ouvre la bouche, puis la referme."),
            ("papa", "On les garde ensemble, sans choisir."),
            ("maman", "Le tunnel n'est pas là."),
            ("narrateur", "Le filet sent le fer froid, trop haut."),
            ("papa", "Tu les gardes comment, dans le filet ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "La boîte penche dans le filet, clic."),
            ("enfant-f", "Votre cabine, trop penchée !"),
            ("narrateur", "Le hérisson glisse au fond, lourd."),
            ("narrateur", "Le renard racle le rebord, mince."),
            ("enfant-f", "Ils ne jouent plus au même endroit."),
            ("narrateur", "Chouchou se dresse sur la pointe, déçue."),
            ("maman", "Le fer ne les tient pas."),
            ("papa", "On les reprend, les deux."),
            ("narrateur", "Une miette tombe à travers une maille."),
            ("papa", "Tu les gardes comment, dans le filet ?"),
        )
    return L(
        ("narrateur", "La ficelle passe entre les mailles, trop vite."),
        ("enfant-f", "Vous pendez, comme du linge !"),
        ("narrateur", "Le hérisson se balance, lourd d'un côté."),
        ("narrateur", "Le renard file vers le vide, léger."),
        ("enfant-f", "Je ne veux pas d'un seul."),
        ("narrateur", "Ses épaules tombent, et le filet grince."),
        ("papa", "Alors on les garde ensemble."),
        ("maman", "Le tunnel attend, plus loin."),
        ("narrateur", "Le nœud frotte le fer, trop lâche."),
        ("papa", "Tu les gardes comment, dans le filet ?"),
    )


def t2_banquette(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Le châle glisse sur le vinyle chaud."),
            ("enfant-f", "C'est trop lisse, ici."),
            ("narrateur", "Le hérisson part vers l'allée, rond."),
            ("narrateur", "Le renard se faufile sous le siège."),
            ("enfant-f", "Le châle ne les tient plus."),
            ("narrateur", "Elle attrape l'un, et l'autre disparaît."),
            ("maman", "Ils ne jouent plus au même endroit."),
            ("papa", "On les reprend, les deux."),
            ("enfant-f", "Je ne veux pas choisir."),
            ("papa", "Tu les poses comment, sur le siège ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "La boîte part vers l'allée, toc."),
            ("enfant-f", "Votre maison roule !"),
            ("narrateur", "Le hérisson bute le couvercle, lourd."),
            ("narrateur", "Le renard glisse sous le dossier, fin."),
            ("enfant-f", "Un dedans, un dessous, ce n'est pas juste."),
            ("narrateur", "Chouchou a les mains trop petites, un instant."),
            ("maman", "Le chauffage les emporte."),
            ("papa", "On les reprend, les deux."),
            ("narrateur", "Le vinyle sent le chaud, trop glissant."),
            ("papa", "Tu les poses comment, sur le siège ?"),
        )
    return L(
        ("narrateur", "La ficelle fuit sous le dossier, vive."),
        ("enfant-f", "Vous vous cachez !"),
        ("narrateur", "Le hérisson reste coincé au bord, rond."),
        ("narrateur", "Le renard tire le nœud vers l'ombre."),
        ("enfant-f", "Je ne chasse pas l'un sans l'autre."),
        ("narrateur", "Elle s'agenouille, le cœur un peu lourd."),
        ("maman", "Le siège les sépare."),
        ("papa", "On les reprend, les deux."),
        ("narrateur", "La laine racle le vinyle, puis se tait."),
        ("papa", "Tu les poses comment, sur le siège ?"),
    )


def t2_passage(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Le châle tremble entre les deux voitures."),
            ("enfant-f", "Ça bouge trop, papa."),
            ("narrateur", "Le hérisson rebondit contre le genou."),
            ("narrateur", "Le renard glisse vers le soufflet noir."),
            ("enfant-f", "Le bleu n'arrête plus rien."),
            ("narrateur", "Le vent froid lui pique les joues."),
            ("maman", "On les tient, on ne les laisse pas."),
            ("papa", "Le tunnel va passer."),
            ("enfant-f", "Ils doivent le voir, tous les deux."),
            ("maman", "Tu les tiens comment, ici ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "La boîte tape le plancher, toc toc."),
            ("enfant-f", "Votre cabine danse !"),
            ("narrateur", "Le hérisson saute au fond, lourd."),
            ("narrateur", "Le renard frappe le rebord, aigu."),
            ("enfant-f", "J'ai peur qu'ils se quittent."),
            ("narrateur", "Chouchou serre les dents, les bras tendus."),
            ("maman", "On les tient, on ne les laisse pas."),
            ("papa", "Le tunnel va passer."),
            ("narrateur", "Le soufflet gémit, noir et froid."),
            ("maman", "Tu les tiens comment, ici ?"),
        )
    return L(
        ("narrateur", "La ficelle saute à chaque joint du plancher."),
        ("enfant-f", "Le nœud fait des bonds !"),
        ("narrateur", "Le hérisson tire d'un côté, lourd."),
        ("narrateur", "Le renard tire de l'autre, léger."),
        ("enfant-f", "Vous n'êtes pas deux équipes."),
        ("narrateur", "Elle retient un mot, et serre le poignet."),
        ("maman", "On les tient, on ne les laisse pas."),
        ("papa", "Le tunnel va passer."),
        ("narrateur", "Le vent sèche la laine, trop vite."),
        ("maman", "Tu les tiens comment, ici ?"),
    )


T2_FN = {1: t2_filet, 2: t2_banquette, 3: t2_passage}
T2_SONS = {1: "filet,fer", 2: "banquette,chauffage", 3: "soufflet,vent"}
T2_EMPH = {1: "filet", 2: "banquette", 3: "passage"}


def t3_choice(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "Le filet attend, trop lâche."),
            ("papa", "Le nid, la boîte, ou contre toi ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "La banquette chauffe, trop lisse."),
            ("maman", "La vallée, la maison, ou la ficelle ?"),
        )
    return L(
        ("narrateur", "Le passage tremble, près des soufflets."),
        ("papa", "La poitrine, la marche, ou le calme ?"),
    )


T3 = {
    (1, 1, 1): L(
        ("enfant-f", "Un nid, pour vous deux."),
        ("narrateur", "Elle pousse le châle en creux, dans les mailles."),
        ("narrateur", "Le hérisson s'enfonce, et le renard le rejoint."),
        ("enfant-f", "Vous vous touchez, là."),
        ("papa", "Ils tiennent, l'un contre l'autre."),
        ("maman", "Le filet devient un hamac, un peu mou."),
        ("narrateur", "Le bleu garde le bord, sans trou."),
        ("enfant-f", "On verra le tunnel, d'en haut."),
        ("narrateur", "Chouchou lève le menton, moins pressée."),
    ),
    (1, 1, 2): L(
        ("enfant-f", "Votre cabine, dans le filet."),
        ("narrateur", "Elle glisse le châle dans la boîte, par-dessus."),
        ("narrateur", "Deux places, une seule boîte, face au trou."),
        ("papa", "Le couvercle fait une petite fenêtre."),
        ("maman", "Ils voyagent ensemble."),
        ("enfant-f", "On verra le tunnel, par le trou."),
        ("narrateur", "La boîte cliquette une fois, puis se tait."),
        ("narrateur", "Chouchou pose un doigt sur le métal, fière."),
    ),
    (1, 1, 3): L(
        ("enfant-f", "Le filet est trop grand."),
        ("narrateur", "Elle ramène le châle contre sa poitrine."),
        ("narrateur", "Le hérisson chauffe la manche, lourd et rond."),
        ("narrateur", "Le renard frotte le bouton du manteau."),
        ("enfant-f", "Vous restez ici, tous les deux."),
        ("papa", "Plus bas, on les voit mieux."),
        ("maman", "Tes bras font le nid, maintenant."),
        ("narrateur", "Le bleu pèse un peu, près du cœur."),
        ("enfant-f", "Le tunnel, on le verra d'ici."),
    ),
    (1, 2, 1): L(
        ("enfant-f", "Une vallée, pour ne plus rouler."),
        ("narrateur", "Elle plie le châle entre deux coussins."),
        ("narrateur", "Le hérisson s'arrête au milieu, enfin."),
        ("narrateur", "Le renard reste sur le pli, droit."),
        ("enfant-f", "Plus de glissade."),
        ("papa", "Ils ont la même pente, maintenant."),
        ("maman", "Le vinyle ne les emporte plus."),
        ("narrateur", "Le bleu tient le creux, face à la vitre."),
        ("enfant-f", "La vitre est à vous, tous les deux."),
    ),
    (1, 2, 2): L(
        ("enfant-f", "Votre maison, sur la banquette."),
        ("narrateur", "Elle tapisse la boîte avec le châle."),
        ("narrateur", "Le hérisson garde le coin gauche."),
        ("narrateur", "Le renard garde le coin droit."),
        ("enfant-f", "Chacun sa fenêtre, dans la même maison."),
        ("papa", "Deux chambres, une seule porte."),
        ("maman", "Ils se parlent, l'un contre l'autre."),
        ("narrateur", "Le beurre et la laine sentent ensemble."),
        ("enfant-f", "Le tunnel va frapper le verre."),
    ),
    (1, 2, 3): L(
        ("enfant-f", "Une ceinture, pour vous deux."),
        ("narrateur", "Elle passe le châle derrière le dossier."),
        ("narrateur", "Le hérisson reste collé au tissu."),
        ("narrateur", "Le renard reste collé à lui."),
        ("enfant-f", "Vous ne partez plus sous le siège."),
        ("papa", "Ils tiennent le dossier, ensemble."),
        ("maman", "Plus de chasse sous la banquette."),
        ("narrateur", "Le bleu serre un peu, puis s'arrête."),
        ("enfant-f", "On attend le noir, sans bouger."),
    ),
    (1, 3, 1): L(
        ("enfant-f", "Contre moi, tous les deux."),
        ("narrateur", "Elle serre le châle contre sa poitrine."),
        ("narrateur", "Le hérisson entend son cœur, près d'elle."),
        ("narrateur", "Le renard sent le bouton, froid."),
        ("enfant-f", "Vous entendez le train, comme moi."),
        ("papa", "Tes bras font le wagon, maintenant."),
        ("maman", "Le soufflet peut gémir, ils restent."),
        ("narrateur", "Le bleu chauffe le manteau, près du col."),
        ("enfant-f", "Le tunnel, on le sentira ici."),
    ),
    (1, 3, 2): L(
        ("enfant-f", "Sur la marche, votre quai."),
        ("narrateur", "Elle s'assoit, le châle sur les genoux."),
        ("narrateur", "Le hérisson regarde le joint noir."),
        ("narrateur", "Le renard regarde le même joint."),
        ("enfant-f", "On est des voyageurs, là."),
        ("papa", "La marche est à toi, un moment."),
        ("maman", "Le plancher tremble moins, d'ici."),
        ("narrateur", "Le bleu tient le poids, sans glisser."),
        ("enfant-f", "Le tunnel va passer sous nous."),
    ),
    (1, 3, 3): L(
        ("enfant-f", "On attend que ça se taise."),
        ("narrateur", "Elle attend, le châle serré, jusqu'au silence."),
        ("narrateur", "Le hérisson ne rebondit plus."),
        ("narrateur", "Le renard ne glisse plus."),
        ("enfant-f", "Maintenant, contre la vitre du passage."),
        ("papa", "Le plancher a dit oui, enfin."),
        ("maman", "Ils peuvent voir, sans danser."),
        ("narrateur", "Le bleu redevient calme, contre le verre."),
        ("enfant-f", "Le tunnel, on l'écoute d'ici."),
    ),
    (2, 1, 1): L(
        ("enfant-f", "Un nid sous la boîte, pour vous."),
        ("narrateur", "Elle pose un coin de châle sous la boîte."),
        ("narrateur", "Le hérisson s'enfonce au fond, chaud."),
        ("narrateur", "Le renard se couche contre lui, droit."),
        ("papa", "Le filet devient un hamac, un peu mou."),
        ("maman", "La boîte ne penche plus."),
        ("enfant-f", "On verra le tunnel, d'en haut."),
        ("narrateur", "Une miette dort au bord du nid."),
        ("narrateur", "Chouchou lâche les épaules, soulagée."),
    ),
    (2, 1, 2): L(
        ("enfant-f", "Votre cabine, dans une maille serrée."),
        ("narrateur", "Elle cale la boîte dans le filet, bien droit."),
        ("narrateur", "Le hérisson prend le fond, le renard le rebord."),
        ("papa", "Deux places, une seule boîte."),
        ("maman", "Ils voyagent ensemble."),
        ("enfant-f", "La fenêtre, c'est le couvercle."),
        ("narrateur", "La boîte cliquette une fois, puis se tait."),
        ("enfant-f", "On verra le tunnel, par le trou."),
        ("narrateur", "Chouchou pose le front contre une maille."),
    ),
    (2, 1, 3): L(
        ("enfant-f", "Le filet est trop grand."),
        ("narrateur", "Elle reprend la boîte, contre elle."),
        ("narrateur", "Le hérisson chauffe le couvercle, lourd."),
        ("narrateur", "Le renard frotte le bord, mince."),
        ("papa", "Plus bas, on les voit mieux."),
        ("maman", "Tes bras font le nid, maintenant."),
        ("enfant-f", "Vous restez ici, tous les deux."),
        ("narrateur", "La boîte pèse un peu, près du cœur."),
        ("enfant-f", "Le tunnel, on le verra d'ici."),
    ),
    (2, 2, 1): L(
        ("enfant-f", "Une vallée, pour la cabine."),
        ("narrateur", "Elle glisse la boîte au fond de deux coussins."),
        ("narrateur", "Le hérisson s'arrête, et le renard aussi."),
        ("papa", "Ils ont la même pente, maintenant."),
        ("maman", "Le vinyle ne les emporte plus."),
        ("enfant-f", "Plus de glissade."),
        ("narrateur", "La boîte tient le creux, face à la vitre."),
        ("enfant-f", "La vitre est à vous, tous les deux."),
        ("narrateur", "Chouchou souffle, et la buée arrive."),
    ),
    (2, 2, 2): L(
        ("enfant-f", "Votre maison, face à la vitre."),
        ("narrateur", "Elle ouvre la boîte, vers le verre froid."),
        ("narrateur", "Le hérisson garde le coin gauche."),
        ("narrateur", "Le renard garde le coin droit."),
        ("enfant-f", "Chacun sa fenêtre, dans la même maison."),
        ("papa", "Deux chambres, une seule porte."),
        ("maman", "Ça sent le beurre, un peu."),
        ("narrateur", "Le couvercle fait deux petites places."),
        ("enfant-f", "Le tunnel va frapper le verre."),
    ),
    (2, 2, 3): L(
        ("enfant-f", "Une ceinture, pour la cabine."),
        ("narrateur", "Elle cale la boîte sous une boucle de laine."),
        ("narrateur", "Le hérisson reste collé, le renard aussi."),
        ("papa", "Ils tiennent le dossier, ensemble."),
        ("maman", "Plus de chasse sous la banquette."),
        ("enfant-f", "Vous ne partez plus sous le siège."),
        ("narrateur", "La boîte serre un peu, puis s'arrête."),
        ("enfant-f", "On attend le noir, sans bouger."),
        ("narrateur", "Chouchou pose la paume sur le couvercle."),
    ),
    (2, 3, 1): L(
        ("enfant-f", "Contre moi, tous les deux."),
        ("narrateur", "Elle plaque la boîte sous le menton."),
        ("narrateur", "Le hérisson entend son cœur, près d'elle."),
        ("narrateur", "Le renard sent le bouton, froid."),
        ("papa", "Tes bras font le wagon, maintenant."),
        ("maman", "Le soufflet peut gémir, ils restent."),
        ("enfant-f", "Vous entendez le train, comme moi."),
        ("narrateur", "La boîte chauffe le manteau, près du col."),
        ("enfant-f", "Le tunnel, on le sentira ici."),
    ),
    (2, 3, 2): L(
        ("enfant-f", "Sur la marche, votre quai."),
        ("narrateur", "Elle pose la boîte sur ses genoux, ouverte."),
        ("narrateur", "Le hérisson regarde le joint noir."),
        ("narrateur", "Le renard regarde le même joint."),
        ("papa", "La marche est à toi, un moment."),
        ("maman", "Le plancher tremble moins, d'ici."),
        ("enfant-f", "On est des voyageurs, là."),
        ("narrateur", "La boîte tient le poids, sans danser."),
        ("enfant-f", "Le tunnel va passer sous nous."),
    ),
    (2, 3, 3): L(
        ("enfant-f", "On attend que ça se taise."),
        ("narrateur", "Elle attend, la boîte fermée, jusqu'au silence."),
        ("narrateur", "Le hérisson ne saute plus."),
        ("narrateur", "Le renard ne frappe plus."),
        ("papa", "Le plancher a dit oui, enfin."),
        ("maman", "Ils peuvent voir, sans danser."),
        ("enfant-f", "Maintenant, contre la vitre du passage."),
        ("narrateur", "La boîte redevient calme, contre le verre."),
        ("enfant-f", "Le tunnel, on l'écoute d'ici."),
    ),
    (3, 1, 1): L(
        ("enfant-f", "Un nid, et le nœud autour."),
        ("narrateur", "Elle noue la ficelle autour du nid de laine."),
        ("narrateur", "Le hérisson s'enfonce, le renard se couche."),
        ("papa", "Ils tiennent, l'un contre l'autre."),
        ("maman", "Le filet devient un hamac, un peu mou."),
        ("enfant-f", "Vous vous touchez, là."),
        ("narrateur", "Le nœud garde le bord, sans trou."),
        ("enfant-f", "On verra le tunnel, d'en haut."),
        ("narrateur", "Chouchou lève le menton, moins pressée."),
    ),
    (3, 1, 2): L(
        ("enfant-f", "Votre cabine, attachée au filet."),
        ("narrateur", "Elle attache la ficelle au bord de la boîte."),
        ("narrateur", "Le hérisson prend le fond, le renard le rebord."),
        ("papa", "Deux places, une seule boîte."),
        ("maman", "Ils voyagent ensemble."),
        ("enfant-f", "La fenêtre, c'est le couvercle."),
        ("narrateur", "Le nœud cliquette une fois, puis se tait."),
        ("enfant-f", "On verra le tunnel, par le trou."),
        ("narrateur", "Chouchou tire un brin, pour vérifier."),
    ),
    (3, 1, 3): L(
        ("enfant-f", "Le filet est trop grand."),
        ("narrateur", "Elle enroule la ficelle autour de son poignet."),
        ("narrateur", "Le hérisson chauffe la manche, lourd."),
        ("narrateur", "Le renard frotte le bouton du manteau."),
        ("papa", "Plus bas, on les voit mieux."),
        ("maman", "Tes bras font le nid, maintenant."),
        ("enfant-f", "Vous restez ici, tous les deux."),
        ("narrateur", "La ficelle pèse un peu, près du pouls."),
        ("enfant-f", "Le tunnel, on le verra d'ici."),
    ),
    (3, 2, 1): L(
        ("enfant-f", "Une vallée, d'un coussin à l'autre."),
        ("narrateur", "Elle tend la ficelle d'un coussin à l'autre."),
        ("narrateur", "Le hérisson s'arrête au milieu, enfin."),
        ("narrateur", "Le renard reste sur le pli, droit."),
        ("papa", "Ils ont la même pente, maintenant."),
        ("maman", "Le vinyle ne les emporte plus."),
        ("enfant-f", "Plus de glissade."),
        ("narrateur", "Le nœud tient le creux, face à la vitre."),
        ("enfant-f", "La vitre est à vous, tous les deux."),
    ),
    (3, 2, 2): L(
        ("enfant-f", "Votre maison, avec une anse."),
        ("narrateur", "Elle noue la ficelle à l'anse de la boîte."),
        ("narrateur", "Le hérisson garde le coin gauche."),
        ("narrateur", "Le renard garde le coin droit."),
        ("enfant-f", "Chacun sa fenêtre, dans la même maison."),
        ("papa", "Deux chambres, une seule porte."),
        ("maman", "Ils se parlent, l'un contre l'autre."),
        ("narrateur", "Le nœud sent le beurre, un peu."),
        ("enfant-f", "Le tunnel va frapper le verre."),
    ),
    (3, 2, 3): L(
        ("enfant-f", "Une ceinture, deux tours."),
        ("narrateur", "Elle noue la ficelle autour du dossier, deux fois."),
        ("narrateur", "Le hérisson reste collé au tissu."),
        ("narrateur", "Le renard reste collé à lui."),
        ("enfant-f", "Vous ne partez plus sous le siège."),
        ("papa", "Ils tiennent le dossier, ensemble."),
        ("maman", "Plus de chasse sous la banquette."),
        ("narrateur", "Le nœud serre un peu, puis s'arrête."),
        ("enfant-f", "On attend le noir, sans bouger."),
    ),
    (3, 3, 1): L(
        ("enfant-f", "Contre moi, tous les deux."),
        ("narrateur", "Elle enroule la ficelle autour de son pouce."),
        ("narrateur", "Le hérisson entend son cœur, près d'elle."),
        ("narrateur", "Le renard sent le bouton, froid."),
        ("papa", "Tes bras font le wagon, maintenant."),
        ("maman", "Le soufflet peut gémir, ils restent."),
        ("enfant-f", "Vous entendez le train, comme moi."),
        ("narrateur", "La ficelle chauffe le pouce, près du col."),
        ("enfant-f", "Le tunnel, on le sentira ici."),
    ),
    (3, 3, 2): L(
        ("enfant-f", "Sur la marche, votre quai."),
        ("narrateur", "Elle attache la ficelle à sa cheville."),
        ("narrateur", "Le hérisson regarde le joint noir."),
        ("narrateur", "Le renard regarde le même joint."),
        ("papa", "La marche est à toi, un moment."),
        ("maman", "Le plancher tremble moins, d'ici."),
        ("enfant-f", "On est des voyageurs, là."),
        ("narrateur", "La ficelle tient le poids, sans sauter."),
        ("enfant-f", "Le tunnel va passer sous nous."),
    ),
    (3, 3, 3): L(
        ("enfant-f", "On attend que ça se taise."),
        ("narrateur", "Elle attend, la ficelle au poignet, jusqu'au silence."),
        ("narrateur", "Le hérisson ne rebondit plus."),
        ("narrateur", "Le renard ne glisse plus."),
        ("papa", "Le plancher a dit oui, enfin."),
        ("maman", "Ils peuvent voir, sans danser."),
        ("enfant-f", "Maintenant, contre la vitre du passage."),
        ("narrateur", "La ficelle redevient calme, contre le verre."),
        ("enfant-f", "Le tunnel, on l'écoute d'ici."),
    ),
}

FIN = {
    (1, 1, 1): L(
        ("narrateur", "Le filet penche vers le noir, très haut."),
        ("enfant-f", "Le tunnel, il arrive."),
        ("papa", "Ils l'ont vu, tous les deux."),
        ("maman", "Deux têtes dans le même nid."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Les lampes du tunnel défilent, orange."),
        ("enfant-f", "Puis c'est blanc."),
        ("narrateur", "La neige colle à une maille, comme la lampe du quai."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Le couvercle tremble, puis s'ouvre un peu."),
        ("enfant-f", "Vous voyez le trou, tous les deux ?"),
        ("papa", "Deux places, une seule cabine."),
        ("maman", "Le filet les a gardés."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le noir entre, puis s'en va."),
        ("enfant-f", "De la neige, sur le métal."),
        ("narrateur", "Un flocon reste au fer, et le cacao sent le sucre."),
    ),
    (1, 1, 3): L(
        ("narrateur", "Ses bras baissent un peu, vers la vitre."),
        ("enfant-f", "Vous êtes plus près, maintenant."),
        ("papa", "Tu les as repris tous les deux."),
        ("maman", "Le filet peut attendre, vide."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le noir frappe le verre, un instant."),
        ("enfant-f", "On l'a vu, ensemble."),
        ("narrateur", "La neige éclaire le manteau, et le sac vide."),
    ),
    (1, 2, 1): L(
        ("narrateur", "La vallée de laine s'arrête, face au verre."),
        ("enfant-f", "Plus personne ne roule."),
        ("papa", "Ils ont la même pente, jusqu'au bout."),
        ("maman", "Le chauffage ronronne, bas."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le souffle de Chouchou dessine le noir."),
        ("enfant-f", "Puis le blanc."),
        ("narrateur", "Deux silhouettes restent dans la buée, rond et fin."),
    ),
    (1, 2, 2): L(
        ("narrateur", "La maison-boîte regarde la vitre, droit."),
        ("enfant-f", "Chacun sa fenêtre, même noir."),
        ("papa", "Deux chambres, un seul tunnel."),
        ("maman", "Ça sent le beurre, un peu."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le verre devient noir, puis blanc."),
        ("enfant-f", "On est arrivés, presque."),
        ("narrateur", "Un flocon se pose au couvercle, près du bleu."),
    ),
    (1, 2, 3): L(
        ("narrateur", "La ceinture de laine tient le dossier."),
        ("enfant-f", "Vous n'êtes plus sous le siège."),
        ("papa", "Ils ont voyagé à la même hauteur."),
        ("maman", "La banquette redevient un lit."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le tunnel avale le wagon, une minute."),
        ("enfant-f", "Je vous ai gardés."),
        ("narrateur", "La neige frappe le vinyle, et la lampe jaune revient."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Son cœur et le train parlent ensemble."),
        ("enfant-f", "Vous l'avez entendu, tous les deux."),
        ("papa", "Tes bras ont fait le wagon."),
        ("maman", "Le soufflet se tait, enfin."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le noir presse un peu les oreilles."),
        ("enfant-f", "Puis la lumière revient."),
        ("narrateur", "La neige entre par la fente, fine comme l'eau du pont."),
    ),
    (1, 3, 2): L(
        ("narrateur", "La marche vibre, puis s'endort."),
        ("enfant-f", "Votre quai a vu le noir."),
        ("papa", "La marche était à toi, un moment."),
        ("maman", "Le joint ne les a pas pris."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le tunnel passe sous leurs pattes."),
        ("enfant-f", "On est des voyageurs, vraiment."),
        ("narrateur", "Un peu de neige reste sur le fer, blanc comme le quai."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Le plancher s'est tu, juste à temps."),
        ("enfant-f", "On a attendu, puis on a vu."),
        ("papa", "Le calme t'a laissé la place."),
        ("maman", "La vitre du passage tient."),
        ("narrateur", "Un brin de laine bleue reste au chaud."),
        ("narrateur", "Le noir arrive sans danser, cette fois."),
        ("enfant-f", "Vous l'avez, tous les deux."),
        ("narrateur", "La neige allume le couloir, comme la lampe du quai."),
    ),
    (2, 1, 1): L(
        ("narrateur", "Le filet penche vers le noir, très haut."),
        ("enfant-f", "Le tunnel, il arrive."),
        ("papa", "Ils l'ont vu, tous les deux."),
        ("maman", "Deux têtes dans le même nid."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Les lampes du tunnel défilent, orange."),
        ("enfant-f", "Puis c'est blanc."),
        ("narrateur", "La neige colle à une maille, sucrée de beurre."),
    ),
    (2, 1, 2): L(
        ("narrateur", "Le couvercle tremble, puis s'ouvre un peu."),
        ("enfant-f", "Vous voyez le trou, tous les deux ?"),
        ("papa", "Deux places, une seule cabine."),
        ("maman", "Le filet les a gardés."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le noir entre, puis s'en va."),
        ("enfant-f", "De la neige, sur le métal."),
        ("narrateur", "Un flocon reste au fer, près du clic."),
    ),
    (2, 1, 3): L(
        ("narrateur", "Ses bras baissent un peu, vers la vitre."),
        ("enfant-f", "Vous êtes plus près, maintenant."),
        ("papa", "Tu les as repris tous les deux."),
        ("maman", "Le filet peut attendre, vide."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le noir frappe le verre, un instant."),
        ("enfant-f", "On l'a vu, ensemble."),
        ("narrateur", "La neige éclaire le manteau, et le couvercle."),
    ),
    (2, 2, 1): L(
        ("narrateur", "La vallée de laine s'arrête, face au verre."),
        ("enfant-f", "Plus personne ne roule."),
        ("papa", "Ils ont la même pente, jusqu'au bout."),
        ("maman", "Le chauffage ronronne, bas."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le souffle de Chouchou dessine le noir."),
        ("enfant-f", "Puis le blanc."),
        ("narrateur", "Deux silhouettes restent dans la buée, dans la cabine."),
    ),
    (2, 2, 2): L(
        ("narrateur", "La maison-boîte regarde la vitre, droit."),
        ("enfant-f", "Chacun sa fenêtre, même noir."),
        ("papa", "Deux chambres, un seul tunnel."),
        ("maman", "Ça sent le beurre, un peu."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le verre devient noir, puis blanc."),
        ("enfant-f", "On est arrivés, presque."),
        ("narrateur", "Un flocon se pose au couvercle, sucré."),
    ),
    (2, 2, 3): L(
        ("narrateur", "La ceinture de laine tient le dossier."),
        ("enfant-f", "Vous n'êtes plus sous le siège."),
        ("papa", "Ils ont voyagé à la même hauteur."),
        ("maman", "La banquette redevient un lit."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le tunnel avale le wagon, une minute."),
        ("enfant-f", "Je vous ai gardés."),
        ("narrateur", "La neige frappe le vinyle, près de la boîte."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Son cœur et le train parlent ensemble."),
        ("enfant-f", "Vous l'avez entendu, tous les deux."),
        ("papa", "Tes bras ont fait le wagon."),
        ("maman", "Le soufflet se tait, enfin."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le noir presse un peu les oreilles."),
        ("enfant-f", "Puis la lumière revient."),
        ("narrateur", "La neige entre par la fente, fine, sur le métal."),
    ),
    (2, 3, 2): L(
        ("narrateur", "La marche vibre, puis s'endort."),
        ("enfant-f", "Votre quai a vu le noir."),
        ("papa", "La marche était à toi, un moment."),
        ("maman", "Le joint ne les a pas pris."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le tunnel passe sous leurs pattes."),
        ("enfant-f", "On est des voyageurs, vraiment."),
        ("narrateur", "Un peu de neige reste sur le fer, et sur le couvercle."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Le plancher s'est tu, juste à temps."),
        ("enfant-f", "On a attendu, puis on a vu."),
        ("papa", "Le calme t'a laissé la place."),
        ("maman", "La vitre du passage tient."),
        ("narrateur", "Une miette de biscuit dort au bord."),
        ("narrateur", "Le noir arrive sans danser, cette fois."),
        ("enfant-f", "Vous l'avez, tous les deux."),
        ("narrateur", "La neige allume le couloir, et le clic se tait."),
    ),
    (3, 1, 1): L(
        ("narrateur", "Le filet penche vers le noir, très haut."),
        ("enfant-f", "Le tunnel, il arrive."),
        ("papa", "Ils l'ont vu, tous les deux."),
        ("maman", "Deux têtes dans le même nid."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Les lampes du tunnel défilent, orange."),
        ("enfant-f", "Puis c'est blanc."),
        ("narrateur", "La neige colle à une maille, près du nœud."),
    ),
    (3, 1, 2): L(
        ("narrateur", "Le couvercle tremble, puis s'ouvre un peu."),
        ("enfant-f", "Vous voyez le trou, tous les deux ?"),
        ("papa", "Deux places, une seule cabine."),
        ("maman", "Le filet les a gardés."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le noir entre, puis s'en va."),
        ("enfant-f", "De la neige, sur le métal."),
        ("narrateur", "Un flocon reste au fer, accroché à la ficelle."),
    ),
    (3, 1, 3): L(
        ("narrateur", "Ses bras baissent un peu, vers la vitre."),
        ("enfant-f", "Vous êtes plus près, maintenant."),
        ("papa", "Tu les as repris tous les deux."),
        ("maman", "Le filet peut attendre, vide."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le noir frappe le verre, un instant."),
        ("enfant-f", "On l'a vu, ensemble."),
        ("narrateur", "La neige éclaire le manteau, et le poignet."),
    ),
    (3, 2, 1): L(
        ("narrateur", "La vallée de laine s'arrête, face au verre."),
        ("enfant-f", "Plus personne ne roule."),
        ("papa", "Ils ont la même pente, jusqu'au bout."),
        ("maman", "Le chauffage ronronne, bas."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le souffle de Chouchou dessine le noir."),
        ("enfant-f", "Puis le blanc."),
        ("narrateur", "Deux silhouettes restent dans la buée, liées."),
    ),
    (3, 2, 2): L(
        ("narrateur", "La maison-boîte regarde la vitre, droit."),
        ("enfant-f", "Chacun sa fenêtre, même noir."),
        ("papa", "Deux chambres, un seul tunnel."),
        ("maman", "Ça sent le beurre, un peu."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le verre devient noir, puis blanc."),
        ("enfant-f", "On est arrivés, presque."),
        ("narrateur", "Un flocon se pose à l'anse, sur le nœud."),
    ),
    (3, 2, 3): L(
        ("narrateur", "La ceinture de laine tient le dossier."),
        ("enfant-f", "Vous n'êtes plus sous le siège."),
        ("papa", "Ils ont voyagé à la même hauteur."),
        ("maman", "La banquette redevient un lit."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le tunnel avale le wagon, une minute."),
        ("enfant-f", "Je vous ai gardés."),
        ("narrateur", "La neige frappe le vinyle, et le double nœud."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Son cœur et le train parlent ensemble."),
        ("enfant-f", "Vous l'avez entendu, tous les deux."),
        ("papa", "Tes bras ont fait le wagon."),
        ("maman", "Le soufflet se tait, enfin."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le noir presse un peu les oreilles."),
        ("enfant-f", "Puis la lumière revient."),
        ("narrateur", "La neige entre par la fente, fine, sur le pouce."),
    ),
    (3, 3, 2): L(
        ("narrateur", "La marche vibre, puis s'endort."),
        ("enfant-f", "Votre quai a vu le noir."),
        ("papa", "La marche était à toi, un moment."),
        ("maman", "Le joint ne les a pas pris."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le tunnel passe sous leurs pattes."),
        ("enfant-f", "On est des voyageurs, vraiment."),
        ("narrateur", "Un peu de neige reste sur le fer, près de la cheville."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Le plancher s'est tu, juste à temps."),
        ("enfant-f", "On a attendu, puis on a vu."),
        ("papa", "Le calme t'a laissé la place."),
        ("maman", "La vitre du passage tient."),
        ("narrateur", "Le nœud de laine reste un peu tiède."),
        ("narrateur", "Le noir arrive sans danser, cette fois."),
        ("enfant-f", "Vous l'avez, tous les deux."),
        ("narrateur", "La neige allume le couloir, et le poignet se tait."),
    ),
}

T3_SONS = {1: "laine,filet", 2: "boite,verre", 3: "soufflet,pas"}
FIN_SONS = {1: "tunnel,neige", 2: "neige,vitre", 3: "neige,fer"}
T3_EMPH = {
    1: {1: "nid", 2: "cabine", 3: "bras"},
    2: {1: "vallée", 3: "ceinture", 2: "maison"},
    3: {1: "cœur", 2: "marche", 3: "silence"},
}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "riviere,gare", "emphasis": "tunnel"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Trois affaires attendent près du sac."),
            ("papa", "Le châle, la boîte, ou la ficelle de laine ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le châle bleu",
            "option_2_label": "la boîte à biscuits",
            "option_3_label": "la ficelle de laine",
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
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], FIN[(a, b, c)], "ending",
                    extra={"sons": FIN_SONS[c], "emphasis": "neige"},
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
        "Le soir, à la gare de colline, Chouchou veut que son hérisson rond "
        "et son renard de bois voient le tunnel ensemble. Elle prend d'abord "
        "le plus facile : le renard tombe dans le sac. Elle reprend les deux, "
        "puis le châle, la boîte ou la ficelle. Au filet trop lâche, sur la "
        "banquette trop lisse, ou dans le passage qui tremble, ils se séparent. "
        "Elle change le geste : nid, cabine, bras ; vallée, maison, ceinture ; "
        "poitrine, marche, ou attendre. Le noir, puis la neige."
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
    if "chouchou" not in blob:
        raise SystemExit("Chouchou absente")
    if "hérisson" not in blob or "renard" not in blob:
        raise SystemExit("voyageurs absents")
    for bad in (
        "escargot", "loupe", "carnet bleu", "pots de menthe", "trace d'argent",
        "lina", "kenzo", "prunier", "carillon", "pain tiède", "la mer",
        "canard", "poupée", "savon", "lavande", "la mare", "capitaine",
        "plic", "volet jaune", "poissons de papier", "nichoir", "citronnade",
        "cerf-volant", "bac à sable", "dinette", "dînette", "les cubes",
    ):
        if bad in whole:
            raise SystemExit(f"calque: {bad}")
    for bad in ("la cuisine", "le jardin", "la chambre"):
        if bad in labels:
            raise SystemExit(f"label calque: {bad}")
    for c in out["chunks"]:
        if not c.get("text_xai_tags") or not c.get("notes") or not c.get("style_energy"):
            raise SystemExit(f"{c['chunk_id']}: TTS incomplet")
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
        "Soir, gare de colline : pont, fer mouillé, lampe jaune, cacao. "
        "Chouchou veut que le hérisson rond et le renard de bois voient le "
        "tunnel ensemble. Première idée : elle prend le plus facile, le "
        "renard tombe dans le sac. Papa remercie qu'elle l'ait repris avec "
        "l'autre. T1 = châle / boîte / ficelle (elle enroule, ferme ou noue "
        "trop vite un seul, puis les deux). T2 = filet trop lâche / banquette "
        "trop lisse / passage qui tremble : ils se séparent, elle retient un "
        "mot sur les corps. T3 change le geste (nid, cabine, bras ; vallée, "
        "maison, ceinture ; poitrine, marche, attendre). Chaque fin paie le "
        "noir du tunnel, puis une neige unique (maille, couvercle, manteau, "
        "buée, vinyle, fente, fer, couloir). La leçon se vit : on les garde "
        "ensemble, sans blague. Autre récit que TREE-DIF-041 (pas mer, pas "
        "pain, pas Nina).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N3 ≤ 16. Troupe D16 : Chouchou, papa, maman.\n"
        "- Slogan « Plus rond ou plus mince » jeté. Première idée échoue "
        "(un seul voyageur, le pli du sac).\n"
        "- 27 fins textuellement distinctes. Un merci vécu (reprendre les deux), "
        "pas un refrain Bravo.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/"
        "resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n"
        "- Tics « tout doux / tout calme / encore / déjà » écartés. "
        "Hérisson lent et lourd, renard vif et glissant : deux rythmes, "
        "même voyage.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
