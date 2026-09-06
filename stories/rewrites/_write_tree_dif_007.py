#!/usr/bin/env python3
"""TREE-DIF-007 — Le rayon sur le casier (F-NAR-019). N2, DIF.BES.001.

Nino veut accrocher sa lentille jaune au bouton du casier avant que
la bande de soleil ne quitte la porte. Aniss, sur le banc, regarde
autrement. Première idée trop vite. Deuxième imprévu plus rusé.
Texte + TTS. Pas apply.
"""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-007"
LIM = 15
TICS = (
    "tout doux",
    "tout calme",
    "on lève la main",
    "puis on parle",
    "c'est du bon travail",
    "l'histoire est finie",
    "on va apprendre",
    "aujourd'hui,",
    "j'ai une idée. écoute",
    "celui où j'ai compris",
    "avec sa couleur, son poids",
    "couleur de miel",
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_rayon_va_quitter_le_casier; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_chasse; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_est_tombé; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_chasse_continue_autrement; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=la_premiere_idee_rate; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=aniss_regarde_autrement; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=une_autre_manière_a_ouvert_le_geste; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_lentille_et_le_rayon_reviennent; tempo=posé; sourire=léger; respiration=ample",
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
    ("narrateur", "Le vestiaire des casiers sent le savon et la banane."),
    ("narrateur", "Une bande de soleil coupe la porte grise de Nino."),
    ("narrateur", "De la poussière tourne dans le rayon, grain par grain."),
    ("narrateur", "Les crochets font clic, un, puis un autre."),
    ("narrateur", "Le carrelage pique un peu, sous les chaussettes."),
    ("papa", "Le soleil glisse, tu le vois sur le métal ?"),
    ("enfant-m", "Ma lentille jaune est là, dans le casier."),
    ("enfant-m", "Je la mets au bouton, pour le cercle d'or."),
    ("maman", "Avant que la bande quitte la porte ?"),
    ("enfant-m", "Oui, la chasse aux reflets."),
    ("narrateur", "En ce moment, Nino tire la poignée, trop fort."),
    ("narrateur", "Des feuilles s'échappent, et tapent le sol."),
    ("narrateur", "Un tic métallique roule, puis se tait."),
    ("narrateur", "Aniss s'assoit sur le banc, les mains à plat."),
    ("narrateur", "Il suit la poussière, sans un mot."),
    ("enfant-m", "Aniss, tu viens attraper le rond ?"),
    ("narrateur", "Aniss ne bouge pas, les épaules basses."),
    ("papa", "Il regarde à sa façon."),
    ("maman", "Par où commences-tu, pour la lentille ?"),
)

T1 = {
    1: dict(
        name="le manteau",
        passage=L(
            ("narrateur", "Nino attrape le manteau, d'un coup."),
            ("narrateur", "Le tissu froid claque contre le crochet."),
            ("enfant-m", "Elle est dans la poche !"),
            ("maman", "Ouvre la poche, sans secouer la manche."),
            ("narrateur", "Il secoue quand même, trop vite."),
            ("narrateur", "Un crayon tombe, tic, sur le carrelage."),
            ("papa", "Le crayon, d'accord."),
            ("papa", "Et la lentille ?"),
            ("enfant-m", "Pas dans la poche."),
            ("narrateur", "La manche balaye le rayon, et le rond saute."),
            ("narrateur", "Aniss cligne, puis recule d'un pouce."),
            ("enfant-m", "Pardon, Aniss."),
            ("narrateur", "Aniss repose ses mains, sans répondre."),
            ("papa", "Le crochet a fait clic, trop fort pour lui."),
            ("enfant-m", "Je voulais aller trop vite."),
            ("maman", "On cherche autrement, alors."),
        ),
        question=L(
            ("narrateur", "La lentille n'est pas dans la poche."),
            ("maman", "Que tombe de la poche ?"),
        ),
        expected="crayon",
        accepted="crayon | un crayon | le crayon | poche | de la poche",
        retry="Un crayon tombe de la poche. Que tombe ?",
        ok="Oui, c'est le crayon.",
        confirm=L(
            ("narrateur", "Le manteau pend au crochet, une manche froide."),
            ("narrateur", "Le crayon reste au sol, inutile."),
            ("enfant-m", "Je la veux, ma lentille."),
            ("papa", "On cherche, sans tout mélanger."),
            ("narrateur", "Nino pose les mains à plat, un moment."),
            ("maman", "Le verre a pu rouler, près du rayon."),
            ("enfant-m", "Je vais la suivre des yeux."),
        ),
        choice=L(
            ("narrateur", "Un éclat jaune a quitté le manteau."),
            ("papa", "Le banc, la vitre, ou les chaussures ?"),
        ),
        sons="manteau,crayon",
        emp="poche",
        lift="le pan du manteau",
    ),
    2: dict(
        name="le cartable",
        passage=L(
            ("narrateur", "Nino pose le cartable, d'un geste large."),
            ("narrateur", "La fermeture résiste, un peu de travers."),
            ("enfant-m", "Elle est coincée."),
            ("papa", "Tire sans forcer, on verra le dessus."),
            ("narrateur", "Il tire trop, et ça fait zzzit, très long."),
            ("narrateur", "Des feuilles s'éventent, une, puis une autre."),
            ("enfant-m", "Ma lentille ?"),
            ("maman", "Regarde le dessus, sans tout vider."),
            ("narrateur", "Un livre pèse au fond, lourd."),
            ("narrateur", "Le verre n'est pas sur le dessus."),
            ("enfant-m", "Elle a glissé."),
            ("narrateur", "Aniss se bouche un peu les oreilles."),
            ("papa", "Le zzzit était trop fort, pour lui."),
            ("enfant-m", "Pardon."),
            ("narrateur", "Nino referme à moitié, les joues chaudes."),
            ("maman", "On suit le tic, maintenant."),
        ),
        question=L(
            ("narrateur", "La lentille n'est pas sur le dessus."),
            ("papa", "Qu'est-ce que Nino a ouvert ?"),
        ),
        expected="cartable",
        accepted="cartable | le cartable | sac | le sac | fermeture",
        retry="Nino a ouvert le cartable. Qu'a-t-il ouvert ?",
        ok="Oui, c'est le cartable.",
        confirm=L(
            ("narrateur", "Le cartable reste ouvert, la fermeture tordue."),
            ("narrateur", "Une feuille d'exercice dépasse, pliée."),
            ("enfant-m", "Je la veux, ma lentille."),
            ("maman", "On cherche, sans tout éventer."),
            ("narrateur", "Nino pose le rabat, tout plat."),
            ("papa", "Le verre a pu filer, près du rayon."),
            ("enfant-m", "Je vais écouter le tic."),
        ),
        choice=L(
            ("narrateur", "Un éclat jaune a quitté le cartable."),
            ("maman", "Le banc, la vitre, ou les chaussures ?"),
        ),
        sons="fermeture,papier",
        emp="dessus",
        lift="le rabat du cartable",
    ),
    3: dict(
        name="la boîte",
        passage=L(
            ("narrateur", "Nino ouvre la boîte, d'un clac sec."),
            ("narrateur", "Le couvercle reste en l'air, surpris."),
            ("enfant-m", "Ça sent la banane."),
            ("maman", "La serviette est collée, au fond."),
            ("narrateur", "Il soulève la serviette, trop vite."),
            ("narrateur", "Une tache ronde brille, un peu collante."),
            ("enfant-m", "Pas la lentille."),
            ("papa", "Elle n'est pas dans la boîte, alors."),
            ("narrateur", "Le couvercle attend, ouvert."),
            ("narrateur", "Aniss pince le nez, puis le relâche."),
            ("enfant-m", "Elle est partie où ?"),
            ("maman", "On suit le verre, sans se presser."),
            ("narrateur", "Nino repose la serviette, à plat."),
            ("papa", "Le clac a fait sursauter le banc."),
            ("enfant-m", "J'ai claqué trop fort."),
            ("maman", "Une autre manière, Nino."),
        ),
        question=L(
            ("narrateur", "La lentille n'est pas sous la serviette."),
            ("maman", "Qu'est-ce que Nino a ouvert ?"),
        ),
        expected="boîte",
        accepted="boîte | boite | la boîte | la boite | serviette",
        retry="Nino a ouvert la boîte. Qu'a-t-il ouvert ?",
        ok="Oui, c'est la boîte.",
        confirm=L(
            ("narrateur", "La boîte reste ouverte, ça sent la banane."),
            ("narrateur", "La serviette a une tache ronde."),
            ("enfant-m", "Je la veux, ma lentille."),
            ("papa", "On cherche, sans tout coller."),
            ("narrateur", "Nino essuie un doigt, sur le tissu."),
            ("maman", "Le verre a pu glisser, près du rayon."),
            ("enfant-m", "Je vais suivre l'odeur, et le tic."),
        ),
        choice=L(
            ("narrateur", "Un éclat jaune a quitté la boîte."),
            ("papa", "Le banc, la vitre, ou les chaussures ?"),
        ),
        sons="boite,couvercle",
        emp="serviette",
        lift="le couvercle de la boîte",
    ),
}


def t2(a: int, b: int) -> list[tuple[str, str]]:
    if a == 1 and b == 1:
        return L(
            ("narrateur", "Le manteau pend, et un éclat jaune file."),
            ("narrateur", "Il glisse sous le banc, près des genoux d'Aniss."),
            ("enfant-m", "Je la prends !"),
            ("narrateur", "Nino rampe trop vite, le carrelage claque."),
            ("narrateur", "Aniss serre les genoux, et la lentille recule."),
            ("enfant-m", "Elle part !"),
            ("maman", "Il a besoin d'air, autour de lui."),
            ("papa", "Regarde comme lui, pas avec les mains d'abord."),
            ("narrateur", "Aniss repose un pied, très lentement."),
            ("narrateur", "Un grain de poussière tombe sur le verre, et brille."),
            ("enfant-m", "Je vois le bord jaune."),
            ("narrateur", "Le manteau, derrière, coupe un peu le rayon."),
            ("maman", "Le tic est là, sous le bois."),
        )
    if a == 1 and b == 2:
        return L(
            ("narrateur", "La porte laisse un filet d'air."),
            ("narrateur", "Le coin jaune vole vers la vitre."),
            ("narrateur", "Le rayon le rattrape, et le tient."),
            ("enfant-m", "Elle est contre le verre !"),
            ("papa", "Regarde, sans courir."),
            ("narrateur", "Nino court quand même, et son ombre avale le rond."),
            ("enfant-m", "Elle a disparu !"),
            ("narrateur", "Aniss lève à peine les yeux, vers la poussière."),
            ("maman", "Recule, le soleil la montrera."),
            ("narrateur", "Nino recule d'un pas, les épaules basses."),
            ("narrateur", "Un fil de lumière redevient mince, sur la vitre."),
            ("enfant-m", "Le bord jaune, je le vois."),
            ("papa", "Le manteau, au crochet, bouge un peu."),
        )
    if a == 1 and b == 3:
        return L(
            ("narrateur", "Une goutte quitte le col du manteau."),
            ("narrateur", "Le verre suit, vers les chaussures."),
            ("narrateur", "Une lacette traîne, un peu humide."),
            ("enfant-m", "Elle est près des souliers !"),
            ("maman", "Baisse-toi, sans tirer."),
            ("narrateur", "Nino tire la lacette, trop fort."),
            ("narrateur", "La lentille skie vers le pied d'Aniss."),
            ("enfant-m", "Oh !"),
            ("narrateur", "Aniss garde le pied, sans bouger."),
            ("papa", "Il laisse le verre, à sa place."),
            ("narrateur", "Une semelle sent le caoutchouc, très bas."),
            ("enfant-m", "Le bord jaune, sous le lacet."),
            ("maman", "Ses pieds parlent, sans un mot."),
        )
    if a == 2 and b == 1:
        return L(
            ("narrateur", "Une feuille quitte le cartable, toute plate."),
            ("narrateur", "Elle glisse jusqu'au banc, le verre dessus."),
            ("narrateur", "Aniss serre un peu les genoux."),
            ("enfant-m", "Ma lentille va sous le banc."),
            ("papa", "On marche lentement, d'accord ?"),
            ("enfant-m", "D'accord."),
            ("narrateur", "Nino froisse le papier, trop vite."),
            ("narrateur", "Aniss se bouche les oreilles, les yeux plissés."),
            ("maman", "Le papier fait trop de bruit, pour lui."),
            ("enfant-m", "Je le laisse."),
            ("narrateur", "Un pied du banc fait un petit toc."),
            ("narrateur", "Le bord jaune apparaît, entre deux lattes."),
            ("papa", "Le rabat, derrière, reste ouvert."),
        )
    if a == 2 and b == 2:
        return L(
            ("narrateur", "Le courant prend une feuille du cartable."),
            ("narrateur", "Elle va se coller contre la vitre, le verre au milieu."),
            ("narrateur", "Le rayon la tient, chaud."),
            ("enfant-m", "C'est elle, sur la vitre !"),
            ("maman", "On y va, sans se bousculer."),
            ("narrateur", "Nino plaque la main, et le verre sonne."),
            ("narrateur", "Aniss sursaute, puis se recroqueville."),
            ("enfant-m", "Pardon, j'ai tapé."),
            ("papa", "Le soleil que tu as dessiné est là, aussi."),
            ("narrateur", "Nino retire sa paume, tout lentement."),
            ("narrateur", "Un fil de lumière redevient net."),
            ("enfant-m", "Je vois le bord jaune, sans la main."),
            ("maman", "Le cartable attend au milieu, ouvert."),
        )
    if a == 2 and b == 3:
        return L(
            ("narrateur", "Une feuille échappe au cartable, vers le bas."),
            ("narrateur", "Elle file vers les chaussures, le verre collé."),
            ("narrateur", "Une lacette traîne, un peu humide."),
            ("enfant-m", "Elle se cache près des souliers."),
            ("papa", "On se baisse, chacun son temps."),
            ("narrateur", "Nino donne un coup de pied, par erreur."),
            ("narrateur", "La feuille part, et Aniss retire un orteil."),
            ("enfant-m", "Je n'ai pas fait exprès !"),
            ("maman", "Regarde son orteil, il a parlé."),
            ("narrateur", "Aniss repose l'orteil, sans un mot."),
            ("narrateur", "Une semelle sent le caoutchouc, très bas."),
            ("enfant-m", "Le bord jaune, près du lacet."),
            ("papa", "Le cartable, derrière, s'est un peu refermé."),
        )
    if a == 3 and b == 1:
        return L(
            ("narrateur", "Un coin de verre quitte la boîte."),
            ("narrateur", "Il glisse sous le banc, un peu collé."),
            ("narrateur", "Ça sent la banane, tout près."),
            ("enfant-m", "Elle est sous le banc."),
            ("maman", "On s'approche, sans claquer."),
            ("narrateur", "Nino attrape trop vite, et le verre colle au doigt."),
            ("narrateur", "Un clac mou, et Aniss pince les lèvres."),
            ("enfant-m", "Elle colle !"),
            ("papa", "La serviette a laissé une tache ronde."),
            ("narrateur", "Nino ouvre la main, et attend."),
            ("narrateur", "Le bois du banc est lisse, un peu froid."),
            ("enfant-m", "Le bord jaune, je le vois."),
            ("maman", "Aniss garde les mains sur les genoux."),
        )
    if a == 3 and b == 2:
        return L(
            ("narrateur", "Le papier s'échappe de la boîte, léger."),
            ("narrateur", "Il va se poser contre la vitre, collant."),
            ("narrateur", "Le rayon le réchauffe, et la tache brille."),
            ("enfant-m", "Elle est à la vitre !"),
            ("papa", "On marche, sans courir."),
            ("narrateur", "Nino décolle trop fort, et ça fait clac."),
            ("narrateur", "Aniss cligne, puis tourne un peu la tête."),
            ("enfant-m", "Elle reste collée."),
            ("maman", "Tu la vois, malgré la tache ?"),
            ("enfant-m", "Oui, le bord jaune est là."),
            ("narrateur", "Un fil de lumière traverse la tache, mince."),
            ("narrateur", "La boîte reste ouverte, au casier."),
            ("papa", "Aniss regarde la lumière, pas le clac."),
        )
    return L(
        ("narrateur", "Le verre quitte la boîte, vers le bas."),
        ("narrateur", "Il s'arrête près des chaussures, sur la serviette."),
        ("narrateur", "Une lacette traîne, un peu humide."),
        ("enfant-m", "Elle est près des souliers."),
        ("maman", "On se baisse, sans se presser."),
        ("narrateur", "Nino saisit la serviette, d'un coup."),
        ("narrateur", "L'odeur de banane monte, et Aniss détourne le nez."),
        ("enfant-m", "Il n'aime pas ça."),
        ("papa", "La boîte reste ouverte, derrière nous."),
        ("narrateur", "Nino repose le tissu, plus loin."),
        ("narrateur", "Une semelle sent le caoutchouc, très bas."),
        ("enfant-m", "Le bord jaune, près du lacet."),
        ("maman", "Aniss n'a pas bougé d'un pied."),
    )


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "La lentille attend sous le banc, près d'Aniss."),
            ("maman", "On attend, on souffle, ou on lève ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "La lentille attend contre la vitre, dans le rayon."),
            ("papa", "On attend, on souffle, ou on lève ?"),
        )
    return L(
        ("narrateur", "La lentille attend près des chaussures, au sol."),
        ("maman", "On attend, on souffle, ou on lève ?"),
    )


def t3(a: int, b: int, c: int) -> list[tuple[str, str]]:
    lift = T1[a]["lift"]
    return {
        (1, 1, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino s'assoit près du banc, pas trop près."),
            ("narrateur", "Il pose les mains à plat, comme Aniss."),
            ("papa", "On laisse le rayon montrer le bord jaune."),
            ("narrateur", "La poussière tourne, puis un tic minuscule."),
            ("narrateur", "La lentille brille sous le bois, un instant."),
            ("enfant-m", "Je la vois."),
            ("maman", "Merci d'avoir attendu avec lui."),
            ("narrateur", "Nino avance deux doigts, sans froisser l'air."),
            ("narrateur", "La lentille est froide, un peu poussiéreuse."),
            ("papa", "Le manteau, au crochet, a cessé de bouger."),
        ),
        (1, 1, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle une longue fois, vers le banc."),
            ("narrateur", "La poussière danse, et le grain d'or cligne."),
            ("papa", "Plus petit, ce souffle."),
            ("narrateur", "Aniss ne se bouche pas les oreilles."),
            ("narrateur", "Le papier du manteau ne bouge plus."),
            ("enfant-m", "Elle avance vers moi."),
            ("maman", "Merci pour ce souffle, si mince."),
            ("narrateur", "Nino prend le verre, à plat."),
            ("narrateur", "Un pied du banc a fait toc, puis s'est tu."),
            ("papa", "La manche froide n'a plus balayé le rond."),
        ),
        (1, 1, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le pan du manteau, c'est ça ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le pan, et le rayon tombe sous le banc."),
            ("narrateur", "La lentille apparaît, entre deux lattes."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir demandé, avant le geste."),
            ("narrateur", "Aniss n'a pas sursauté."),
            ("narrateur", "Le tissu sent le savon, un peu."),
            ("maman", "Le crochet a cliqué, tout bas."),
        ),
        (1, 2, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino recule, et son ombre quitte la vitre."),
            ("narrateur", "Il pose les mains, comme Aniss sur le banc."),
            ("papa", "Le fil de lumière va la montrer."),
            ("narrateur", "La poussière tourne contre le verre, grain par grain."),
            ("narrateur", "Le bord jaune revient, tout seul."),
            ("enfant-m", "Elle est là."),
            ("maman", "Merci d'avoir reculé, pour le soleil."),
            ("narrateur", "Nino glisse deux doigts, le long du fil."),
            ("narrateur", "La lentille est tiède, du rayon."),
            ("papa", "Le manteau, derrière, a cessé de souffler."),
        ),
        (1, 2, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur la vitre, une fois, mince."),
            ("narrateur", "La buée s'ouvre, et le bord jaune cligne."),
            ("papa", "Sans coller la main, cette fois."),
            ("narrateur", "Aniss suit la poussière, les yeux calmes."),
            ("enfant-m", "Elle glisse."),
            ("maman", "Merci pour ce souffle, pas pour la paume."),
            ("narrateur", "Nino cueille le verre, contre le fil de lumière."),
            ("narrateur", "La manche du manteau ne balaye plus."),
            ("papa", "Le rond est à toi, sans l'ombre."),
            ("narrateur", "Un grain d'or reste collé au verre, minuscule."),
        ),
        (1, 2, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le pan du manteau, qui coupe le rayon ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le pan, et le fil frappe la vitre."),
            ("narrateur", "La lentille brille, collée au chaud."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir vu l'ombre, d'abord."),
            ("narrateur", "Aniss cligne, puis regarde le rond, content."),
            ("narrateur", "Le crochet a fait clic, très bas."),
            ("maman", "La porte a cessé de souffler."),
        ),
        (1, 3, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino s'accroupit près des chaussures, sans tirer."),
            ("narrateur", "Il pose les mains à plat, comme Aniss."),
            ("papa", "Le pied d'Aniss a parlé, en restant."),
            ("narrateur", "La poussière tombe sur le lacet, et le bord jaune cligne."),
            ("enfant-m", "Je la vois."),
            ("maman", "Merci d'avoir laissé son pied tranquille."),
            ("narrateur", "Nino glisse deux doigts sous la lacette."),
            ("narrateur", "La lentille est froide, un peu mouillée."),
            ("papa", "La goutte du col a séché, sur le tissu."),
            ("narrateur", "Aniss n'a pas retiré l'orteil."),
        ),
        (1, 3, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur la lacette, une fois, long."),
            ("narrateur", "La poussière part, et le grain d'or cligne."),
            ("papa", "Sans tirer, cette fois."),
            ("narrateur", "Aniss garde le pied, comme une porte ouverte."),
            ("enfant-m", "Elle avance."),
            ("maman", "Merci pour ce souffle, près des souliers."),
            ("narrateur", "Nino prend le verre, à plat, sans le ski."),
            ("narrateur", "La semelle sent le caoutchouc, et le savon."),
            ("papa", "Le col du manteau n'a plus de goutte."),
            ("narrateur", "Un cercle pâle reste un instant, sur le carrelage."),
        ),
        (1, 3, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le pan du manteau, qui cache les souliers ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le pan, et le rayon tombe sur les lacets."),
            ("narrateur", "La lentille apparaît, près du caoutchouc."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir demandé, avant de tirer."),
            ("narrateur", "Aniss n'a pas bougé d'un orteil."),
            ("narrateur", "Le tissu sent le dehors, un peu froid."),
            ("maman", "La goutte du col s'est tue."),
        ),
        (2, 1, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino laisse le papier, et s'assoit un peu plus loin."),
            ("narrateur", "Il pose les mains, comme Aniss."),
            ("papa", "Le toc du banc va la montrer."),
            ("narrateur", "Aniss relâche les oreilles, puis les genoux."),
            ("narrateur", "Le bord jaune apparaît, entre deux lattes."),
            ("enfant-m", "Je la vois."),
            ("maman", "Merci d'avoir laissé le papier se taire."),
            ("narrateur", "Nino avance deux doigts, sans froisser."),
            ("narrateur", "La lentille est froide, sous le bois."),
            ("papa", "Le rabat du cartable a cessé de pendre."),
        ),
        (2, 1, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur la feuille, une fois, mince."),
            ("narrateur", "Le papier glisse, et le verre reste, brillant."),
            ("papa", "Sans le froisser, cette fois."),
            ("narrateur", "Aniss descend les mains, loin des oreilles."),
            ("enfant-m", "Elle est à moi."),
            ("maman", "Merci pour ce souffle, pas pour le zzzit."),
            ("narrateur", "Nino prend le verre, à plat."),
            ("narrateur", "Un pied du banc a fait toc, puis plus rien."),
            ("papa", "La fermeture tordue ne parle plus."),
            ("narrateur", "Une feuille d'exercice dort, pliée, sous le bois."),
        ),
        (2, 1, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le rabat du cartable, c'est ça ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le rabat, et le rayon tombe sous le banc."),
            ("narrateur", "La lentille apparaît, entre les lattes."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir demandé, avant le zzzit."),
            ("narrateur", "Aniss n'a pas bouché les oreilles."),
            ("narrateur", "Le papier sent l'encre, un peu."),
            ("maman", "La fermeture pend, sans bruit."),
        ),
        (2, 2, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino retire sa paume, et attend le fil."),
            ("narrateur", "Il pose les mains, comme Aniss."),
            ("papa", "Le soleil dessiné va la montrer."),
            ("narrateur", "La poussière tourne contre la vitre, grain par grain."),
            ("narrateur", "Le bord jaune revient, sans la main."),
            ("enfant-m", "Elle est là."),
            ("maman", "Merci d'avoir laissé le verre sonner tout seul."),
            ("narrateur", "Nino glisse deux doigts, le long du fil."),
            ("narrateur", "La lentille est tiède, du rayon."),
            ("papa", "Le cartable, au milieu, s'est un peu refermé."),
        ),
        (2, 2, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur la vitre, une fois, mince."),
            ("narrateur", "La feuille se décolle, et le verre reste."),
            ("papa", "Sans plaquer la main, cette fois."),
            ("narrateur", "Aniss se déroule un peu, les épaules moins hautes."),
            ("enfant-m", "Je la prends."),
            ("maman", "Merci pour ce souffle, pas pour le coup."),
            ("narrateur", "Nino cueille le verre, contre le fil."),
            ("narrateur", "Le soleil dessiné regarde, de travers."),
            ("papa", "La fermeture tordue s'est tue."),
            ("narrateur", "Un rectangle de buée s'efface, tout seul."),
        ),
        (2, 2, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le rabat du cartable, qui coupe le fil ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le rabat, et le rayon frappe la vitre."),
            ("narrateur", "La lentille brille, au milieu de la feuille."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir vu le fil, d'abord."),
            ("narrateur", "Aniss cligne, puis regarde le rond."),
            ("narrateur", "Le cartable, au milieu, a cessé de s'éventer."),
            ("maman", "La fermeture pend, tordue, et se tait."),
        ),
        (2, 3, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino s'accroupit, loin de l'orteil d'Aniss."),
            ("narrateur", "Il pose les mains à plat, et compte un souffle."),
            ("papa", "Son orteil a parlé, en se posant."),
            ("narrateur", "La poussière tombe sur le lacet, et le bord jaune cligne."),
            ("enfant-m", "Je la vois."),
            ("maman", "Merci d'avoir laissé son pied rentrer."),
            ("narrateur", "Nino glisse deux doigts, sans donner de coup."),
            ("narrateur", "La lentille est froide, un peu mouillée."),
            ("papa", "Le cartable, derrière, s'est refermé d'un cran."),
            ("narrateur", "Les deux chaussures restent paires, près du rond."),
        ),
        (2, 3, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur la feuille, près des souliers."),
            ("narrateur", "Le papier part, et le verre reste, brillant."),
            ("papa", "Sans le pied, cette fois."),
            ("narrateur", "Aniss repose l'orteil, comme une permission."),
            ("enfant-m", "Elle est à moi."),
            ("maman", "Merci pour ce souffle, pas pour le coup."),
            ("narrateur", "Nino prend le verre, à plat."),
            ("narrateur", "Une lacette a une poussière d'or."),
            ("papa", "La fermeture tordue ne zzzit plus."),
            ("narrateur", "La semelle sent le caoutchouc, et l'encre."),
        ),
        (2, 3, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le rabat du cartable, qui fait de l'ombre ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le rabat, et le rayon tombe sur les lacets."),
            ("narrateur", "La lentille apparaît, près du caoutchouc."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir demandé, avant le pied."),
            ("narrateur", "Aniss n'a pas retiré l'orteil."),
            ("narrateur", "Une feuille d'exercice reste pliée, au sol."),
            ("maman", "Le cartable a cessé de s'éventer."),
        ),
        (3, 1, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino ouvre la main, et laisse le collant se taire."),
            ("narrateur", "Il s'assoit un peu plus loin, les mains à plat."),
            ("papa", "Le bois froid va la montrer."),
            ("narrateur", "Aniss relâche les lèvres, puis les genoux."),
            ("narrateur", "Le bord jaune apparaît, un peu collé."),
            ("enfant-m", "Je la vois."),
            ("maman", "Merci d'avoir attendu que ça décolle."),
            ("narrateur", "Nino avance deux doigts, sans clac."),
            ("narrateur", "La lentille est froide, un peu sucrée."),
            ("papa", "La boîte, derrière, sent la banane, trop."),
        ),
        (3, 1, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur la tache, une fois, mince."),
            ("narrateur", "Le collant lâche, et le grain d'or cligne."),
            ("papa", "Sans le doigt collé, cette fois."),
            ("narrateur", "Aniss descend les épaules, loin du nez pincé."),
            ("enfant-m", "Elle avance."),
            ("maman", "Merci pour ce souffle, pas pour le clac."),
            ("narrateur", "Nino prend le verre, à plat."),
            ("narrateur", "Le bois du banc est lisse, un peu froid."),
            ("papa", "Le couvercle de la boîte reste en l'air."),
            ("narrateur", "Une tache ronde brille au fond, oubliée."),
        ),
        (3, 1, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le couvercle de la boîte, c'est ça ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le couvercle, et le rayon tombe sous le banc."),
            ("narrateur", "La lentille apparaît, un peu collée."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir demandé, avant le clac."),
            ("narrateur", "Aniss n'a pas pincé le nez."),
            ("narrateur", "La boîte sent la banane, près du banc."),
            ("maman", "La serviette a gardé un pli."),
        ),
        (3, 2, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino recule, et laisse la tache sécher un peu."),
            ("narrateur", "Il pose les mains, comme Aniss."),
            ("papa", "Le fil de lumière va la montrer."),
            ("narrateur", "La poussière tourne contre la tache, grain par grain."),
            ("narrateur", "Le bord jaune revient, moins collé."),
            ("enfant-m", "Elle est là."),
            ("maman", "Merci d'avoir laissé le clac se taire."),
            ("narrateur", "Nino glisse deux doigts, le long du fil."),
            ("narrateur", "La lentille est tiède, un peu sucrée."),
            ("papa", "La boîte, au casier, reste ouverte."),
        ),
        (3, 2, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur la tache, une fois, mince."),
            ("narrateur", "Le collant lâche, et le verre glisse d'un poil."),
            ("papa", "Sans décoller trop fort, cette fois."),
            ("narrateur", "Aniss tourne la tête, puis revient vers la lumière."),
            ("enfant-m", "Je la prends."),
            ("maman", "Merci pour ce souffle, pas pour le clac."),
            ("narrateur", "Nino cueille le verre, contre le fil."),
            ("narrateur", "La tache ronde, sur le verre, a pâli."),
            ("papa", "Le couvercle attend, en l'air."),
            ("narrateur", "Le rayon quitte un peu la porte, lentement."),
        ),
        (3, 2, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le couvercle de la boîte, qui fait de l'ombre ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le couvercle, et le rayon frappe la vitre."),
            ("narrateur", "La lentille brille, malgré la tache."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir vu la tache, d'abord."),
            ("narrateur", "Aniss cligne, puis regarde le rond."),
            ("narrateur", "La serviette a gardé un pli collant."),
            ("maman", "La boîte, au casier, s'est tue."),
        ),
        (3, 3, 1): L(
            ("enfant-m", "On attend."),
            ("narrateur", "Nino repose le tissu plus loin, et s'accroupit."),
            ("narrateur", "Il pose les mains à plat, loin du nez d'Aniss."),
            ("papa", "L'odeur va partir, si on laisse l'air."),
            ("narrateur", "Aniss revient vers les souliers, un peu."),
            ("narrateur", "Le bord jaune cligne, près du lacet."),
            ("enfant-m", "Je la vois."),
            ("maman", "Merci d'avoir éloigné la banane."),
            ("narrateur", "Nino glisse deux doigts, sans saisir le tissu."),
            ("narrateur", "La lentille est froide, un peu sucrée."),
            ("papa", "La boîte, derrière, reste ouverte."),
        ),
        (3, 3, 2): L(
            ("enfant-m", "Je souffle."),
            ("narrateur", "Nino souffle sur le lacet, une fois, mince."),
            ("narrateur", "La poussière part, et le grain d'or cligne."),
            ("papa", "Sans l'odeur sous le nez, cette fois."),
            ("narrateur", "Aniss ne détourne plus le visage."),
            ("enfant-m", "Elle avance."),
            ("maman", "Merci pour ce souffle, pas pour la serviette."),
            ("narrateur", "Nino prend le verre, à plat."),
            ("narrateur", "Une semelle sent le caoutchouc, très bas."),
            ("papa", "Le couvercle de la boîte s'est un peu refermé."),
            ("narrateur", "Un cercle pâle reste un instant, sur le carrelage."),
        ),
        (3, 3, 3): L(
            ("enfant-m", "Tu lèves, papa ?"),
            ("papa", "Le couvercle de la boîte, c'est ça ?"),
            ("enfant-m", "Oui, s'il te plaît."),
            ("narrateur", "Papa lève le couvercle, et le rayon tombe sur les lacets."),
            ("narrateur", "La lentille apparaît, près du caoutchouc."),
            ("maman", "Tu la prends, Nino."),
            ("enfant-m", "Merci, papa."),
            ("papa", "Merci d'avoir demandé, avant l'odeur."),
            ("narrateur", "Aniss n'a pas détourné le nez."),
            ("narrateur", "La serviette reste plus loin, pliée."),
            ("maman", "Le bouton du casier attend, tiède."),
        ),
    }[(a, b, c)]


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    return {
        (1, 1, 1): L(
            ("narrateur", "Nino tient la lentille des deux mains."),
            ("enfant-m", "Au bouton, pour le cercle d'or."),
            ("maman", "On la met où le rayon arrive ?"),
            ("enfant-m", "Oui, sur le casier."),
            ("narrateur", "Le verre se cale sous le bouton, tiède."),
            ("narrateur", "Un rond d'or tombe près du banc, et Aniss le suit."),
            ("papa", "Il regarde à sa façon, et le rond tient."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "Le manteau pend, une manche froide."),
            ("narrateur", "Le bouton du casier garde un rond tiède."),
        ),
        (1, 1, 2): L(
            ("narrateur", "Nino pose la lentille sous le bouton."),
            ("enfant-m", "Souffle, et le rond danse."),
            ("papa", "Un grain, rien de plus."),
            ("narrateur", "Le cercle d'or tremble sur le bois du banc."),
            ("narrateur", "Aniss avance un doigt, dans la lumière, puis le retire."),
            ("maman", "Il a touché le rond, à sa manière."),
            ("enfant-m", "Merci, Aniss."),
            ("narrateur", "Le manteau a cessé de claquer."),
            ("papa", "Le tic du verre s'est tu, enfin."),
            ("narrateur", "Un grain de poussière s'endort sur le verre jaune."),
        ),
        (1, 1, 3): L(
            ("narrateur", "Papa lâche le pan, et Nino cale le verre."),
            ("enfant-m", "Le bouton est chaud."),
            ("maman", "Le rayon a payé le geste."),
            ("narrateur", "Un cercle d'or s'assoit sur le carrelage, rond."),
            ("narrateur", "Aniss le regarde, les mains à plat."),
            ("papa", "Le crochet n'a plus cliqué trop fort."),
            ("enfant-m", "On a levé, et le soleil est venu."),
            ("narrateur", "Le crayon, au sol, a une poudre jaune."),
            ("maman", "Tu l'as demandé, avant le tissu."),
            ("narrateur", "Le crochet du manteau s'est tu."),
        ),
        (1, 2, 1): L(
            ("narrateur", "Nino cale la lentille sous le bouton."),
            ("enfant-m", "Sans mon ombre, cette fois."),
            ("papa", "Le fil de la vitre a montré le chemin."),
            ("narrateur", "Un cercle d'or glisse sur la porte, puis tient."),
            ("narrateur", "Aniss lève les yeux, un instant, vers le rond."),
            ("maman", "Il a suivi la poussière, jusqu'ici."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "Le manteau, au crochet, ne coupe plus le soleil."),
            ("papa", "La bande quitte un peu le métal, lentement."),
            ("narrateur", "La vitre tient un carré de soleil, vide."),
        ),
        (1, 2, 2): L(
            ("narrateur", "Nino pose le verre, et souffle un dernier grain."),
            ("enfant-m", "Le rond, sur le casier !"),
            ("maman", "Il danse, sans la paume."),
            ("narrateur", "Un cercle d'or part de la porte, vers Aniss."),
            ("narrateur", "Aniss cligne, puis le laisse passer sur le genou."),
            ("papa", "Tu as soufflé, pas tapé."),
            ("enfant-m", "Le bord jaune est à sa place."),
            ("narrateur", "La manche du manteau ne balaye plus le rayon."),
            ("maman", "Le grain d'or reste collé, minuscule."),
            ("narrateur", "Le fil de lumière a cessé de bouger."),
        ),
        (1, 2, 3): L(
            ("narrateur", "Papa lâche le pan, et le bouton reçoit le verre."),
            ("enfant-m", "Le rayon, pile là."),
            ("maman", "L'ombre du manteau n'est plus sur la chasse."),
            ("narrateur", "Un cercle d'or s'accroche au métal, puis au sol."),
            ("narrateur", "Aniss sourit à peine, sans un mot."),
            ("papa", "Merci d'avoir vu l'ombre, Nino."),
            ("enfant-m", "On a levé, et le fil est venu."),
            ("narrateur", "La porte a cessé de souffler."),
            ("maman", "Le crochet a fait clic, très bas."),
            ("narrateur", "La manche du manteau ne balaye plus le rayon."),
        ),
        (1, 3, 1): L(
            ("narrateur", "Nino cale la lentille, les doigts un peu mouillés."),
            ("enfant-m", "Le lacet a parlé, et j'ai attendu."),
            ("papa", "Le pied d'Aniss a gardé sa place."),
            ("narrateur", "Un cercle d'or tombe près des chaussures, pâle."),
            ("narrateur", "Aniss le regarde, l'orteil tranquille."),
            ("maman", "Tu n'as pas tiré, cette fois."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "La goutte du col a séché, sur le tissu."),
            ("papa", "Le savon du vestiaire tient, dans l'air."),
            ("narrateur", "Une lacette sèche, à côté d'un cercle pâle."),
        ),
        (1, 3, 2): L(
            ("narrateur", "Nino pose le verre sous le bouton, et souffle."),
            ("enfant-m", "Le grain d'or, sur le casier."),
            ("maman", "Sans le ski, cette fois."),
            ("narrateur", "Un cercle d'or glisse du métal vers le caoutchouc."),
            ("narrateur", "Aniss laisse le rond sur la chaussure, un instant."),
            ("papa", "Tu as soufflé, pas tiré."),
            ("enfant-m", "Le bord jaune est chaud."),
            ("narrateur", "Le col du manteau n'a plus de goutte."),
            ("maman", "La semelle sent le savon, un peu."),
            ("narrateur", "La semelle sent le caoutchouc, et le verre, un peu."),
        ),
        (1, 3, 3): L(
            ("narrateur", "Papa lâche le pan, et Nino cale le verre."),
            ("enfant-m", "Les souliers ont de la lumière."),
            ("maman", "Le pan ne cache plus le lacet."),
            ("narrateur", "Un cercle d'or s'assoit sur le carrelage, près des paires."),
            ("narrateur", "Aniss n'a pas bougé d'un orteil."),
            ("papa", "Merci d'avoir demandé, Nino."),
            ("enfant-m", "On a levé, et le rayon est venu."),
            ("narrateur", "Le tissu sent le dehors, un peu froid."),
            ("maman", "Le crochet s'est tu."),
            ("narrateur", "Le col du manteau a perdu sa goutte."),
        ),
        (2, 1, 1): L(
            ("narrateur", "Nino cale la lentille sous le bouton."),
            ("enfant-m", "Sans le papier, cette fois."),
            ("papa", "Le toc du banc a montré le bord."),
            ("narrateur", "Un cercle d'or tombe près d'Aniss, et il le suit."),
            ("narrateur", "Aniss relâche les oreilles, pour de bon."),
            ("maman", "Le zzzit n'est plus là."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "Le rabat du cartable reste ouvert, sans bruit."),
            ("papa", "L'encre de la feuille sent moins fort."),
            ("narrateur", "Le rabat du cartable reste ouvert, sans zzzit."),
        ),
        (2, 1, 2): L(
            ("narrateur", "Nino pose le verre, et souffle un grain vers le bouton."),
            ("enfant-m", "Le rond, pour Aniss."),
            ("maman", "Le papier s'est tu, sous le bois."),
            ("narrateur", "Un cercle d'or tremble sur le banc, puis tient."),
            ("narrateur", "Aniss descend les mains, loin des oreilles."),
            ("papa", "Tu as soufflé, pas froissé."),
            ("enfant-m", "Le bord jaune est à sa place."),
            ("narrateur", "La fermeture tordue ne parle plus."),
            ("maman", "Le tic du verre s'est tu."),
            ("narrateur", "Une feuille d'exercice dort, pliée, sous le banc."),
        ),
        (2, 1, 3): L(
            ("narrateur", "Papa lâche le rabat, et Nino cale le verre."),
            ("enfant-m", "Le bouton est chaud."),
            ("maman", "Le rabat n'a plus coupé le rayon."),
            ("narrateur", "Un cercle d'or s'assoit sur le carrelage, rond."),
            ("narrateur", "Aniss n'a pas bouché les oreilles."),
            ("papa", "Merci d'avoir demandé, avant le zzzit."),
            ("enfant-m", "On a levé, et le soleil est venu."),
            ("narrateur", "Le papier sent l'encre, un peu."),
            ("maman", "La fermeture pend, sans bruit."),
            ("narrateur", "Le bois du banc a un petit toc, puis plus rien."),
        ),
        (2, 2, 1): L(
            ("narrateur", "Nino cale la lentille, loin de sa paume."),
            ("enfant-m", "Sans taper, cette fois."),
            ("papa", "Le soleil dessiné a gardé le fil."),
            ("narrateur", "Un cercle d'or glisse sur la porte, puis tient."),
            ("narrateur", "Aniss lève les yeux, un instant, vers le rond."),
            ("maman", "Il a suivi la poussière, pas le coup."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "Le cartable, au milieu, s'est un peu refermé."),
            ("papa", "La bande quitte le métal, lentement."),
            ("narrateur", "Le soleil dessiné sur une feuille regarde la vitre."),
        ),
        (2, 2, 2): L(
            ("narrateur", "Nino pose le verre, et souffle la buée."),
            ("enfant-m", "Le rond, sur le casier !"),
            ("maman", "La feuille s'est décollée, sans la main."),
            ("narrateur", "Un cercle d'or part vers Aniss, et s'arrête au genou."),
            ("narrateur", "Aniss se déroule, les épaules moins hautes."),
            ("papa", "Tu as soufflé, pas plaqué."),
            ("enfant-m", "Le bord jaune est chaud."),
            ("narrateur", "La fermeture tordue s'est tue."),
            ("maman", "Le vestiaire sent moins le papier froissé."),
            ("narrateur", "Un rectangle de buée s'efface, tout seul."),
        ),
        (2, 2, 3): L(
            ("narrateur", "Papa lâche le rabat, et le bouton reçoit le verre."),
            ("enfant-m", "Le fil, pile là."),
            ("maman", "Le rabat n'a plus coupé la chasse."),
            ("narrateur", "Un cercle d'or s'accroche au métal, puis au sol."),
            ("narrateur", "Aniss cligne, puis regarde le rond."),
            ("papa", "Merci d'avoir vu le fil, Nino."),
            ("enfant-m", "On a levé, et la vitre a parlé."),
            ("narrateur", "Le cartable, au milieu, a cessé de s'éventer."),
            ("maman", "La feuille reste contre le verre, sage."),
            ("narrateur", "La fermeture pend, tordue, et se tait."),
        ),
        (2, 3, 1): L(
            ("narrateur", "Nino cale la lentille, loin de l'orteil."),
            ("enfant-m", "J'ai compté un souffle."),
            ("papa", "Son orteil a gardé la permission."),
            ("narrateur", "Un cercle d'or tombe près des chaussures, pâle."),
            ("narrateur", "Aniss le regarde, l'orteil tranquille."),
            ("maman", "Tu n'as pas donné de coup, cette fois."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "Le cartable, derrière, s'est refermé d'un cran."),
            ("papa", "Le savon du vestiaire tient, dans l'air."),
            ("narrateur", "Les deux chaussures restent paires, près du rond."),
        ),
        (2, 3, 2): L(
            ("narrateur", "Nino pose le verre sous le bouton, et souffle."),
            ("enfant-m", "Le grain d'or, sur le casier."),
            ("maman", "Sans le pied, cette fois."),
            ("narrateur", "Un cercle d'or glisse du métal vers le caoutchouc."),
            ("narrateur", "Aniss laisse le rond sur la chaussure, un instant."),
            ("papa", "Tu as soufflé, pas tapé."),
            ("enfant-m", "Le bord jaune est chaud."),
            ("narrateur", "La fermeture tordue ne zzzit plus."),
            ("maman", "La semelle sent l'encre, un peu."),
            ("narrateur", "Une lacette a une poussière d'or."),
        ),
        (2, 3, 3): L(
            ("narrateur", "Papa lâche le rabat, et Nino cale le verre."),
            ("enfant-m", "Les souliers ont de la lumière."),
            ("maman", "Le rabat ne fait plus d'ombre."),
            ("narrateur", "Un cercle d'or s'assoit près des paires, rond."),
            ("narrateur", "Aniss n'a pas retiré l'orteil."),
            ("papa", "Merci d'avoir demandé, Nino."),
            ("enfant-m", "On a levé, et le rayon est venu."),
            ("narrateur", "Une feuille d'exercice reste pliée, au sol."),
            ("maman", "La fermeture s'est tue."),
            ("narrateur", "Le cartable, au milieu, a cessé de s'éventer."),
        ),
        (3, 1, 1): L(
            ("narrateur", "Nino cale la lentille, un doigt un peu sucré."),
            ("enfant-m", "Sans le clac, cette fois."),
            ("papa", "Le bois froid a montré le bord."),
            ("narrateur", "Un cercle d'or tombe près d'Aniss, et il le suit."),
            ("narrateur", "Aniss relâche les lèvres, pour de bon."),
            ("maman", "L'odeur de banane reste, plus loin."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "La boîte, derrière, sent trop, et s'éloigne."),
            ("papa", "Le collant s'est tu, sous le bois."),
            ("narrateur", "La tache de banane brille au fond, oubliée."),
        ),
        (3, 1, 2): L(
            ("narrateur", "Nino pose le verre, et souffle un grain vers le bouton."),
            ("enfant-m", "Le rond, pour Aniss."),
            ("maman", "Le collant a lâché, sans le doigt."),
            ("narrateur", "Un cercle d'or tremble sur le banc, puis tient."),
            ("narrateur", "Aniss descend les épaules, loin du nez pincé."),
            ("papa", "Tu as soufflé, pas claqué."),
            ("enfant-m", "Le bord jaune est à sa place."),
            ("narrateur", "Le couvercle de la boîte reste en l'air."),
            ("maman", "Le tic du verre s'est tu."),
            ("narrateur", "Le couvercle de la boîte reste en l'air, sage."),
        ),
        (3, 1, 3): L(
            ("narrateur", "Papa lâche le couvercle, et Nino cale le verre."),
            ("enfant-m", "Le bouton est chaud."),
            ("maman", "Le couvercle n'a plus coupé le rayon."),
            ("narrateur", "Un cercle d'or s'assoit sur le carrelage, rond."),
            ("narrateur", "Aniss n'a pas pincé le nez."),
            ("papa", "Merci d'avoir demandé, avant le clac."),
            ("enfant-m", "On a levé, et le soleil est venu."),
            ("narrateur", "La serviette a gardé un pli."),
            ("maman", "La tache ronde, au fond, s'est tue."),
            ("narrateur", "La boîte sent la banane, près du banc."),
        ),
        (3, 2, 1): L(
            ("narrateur", "Nino cale la lentille, loin de la tache sèche."),
            ("enfant-m", "Sans décoller trop fort."),
            ("papa", "Le fil de la vitre a montré le chemin."),
            ("narrateur", "Un cercle d'or glisse sur la porte, puis tient."),
            ("narrateur", "Aniss lève les yeux, un instant, vers le rond."),
            ("maman", "Il a suivi la lumière, pas le clac."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "La boîte, au casier, reste ouverte."),
            ("papa", "La bande quitte un peu le métal, lentement."),
            ("narrateur", "La tache ronde, sur le verre, a séché."),
        ),
        (3, 2, 2): L(
            ("narrateur", "Nino pose le verre, et souffle la tache."),
            ("enfant-m", "Le rond, sur le casier !"),
            ("maman", "Le collant a lâché, d'un poil."),
            ("narrateur", "Un cercle d'or part vers Aniss, et s'arrête au genou."),
            ("narrateur", "Aniss tourne la tête, puis revient vers la lumière."),
            ("papa", "Tu as soufflé, pas claqué."),
            ("enfant-m", "Le bord jaune est chaud."),
            ("narrateur", "Le couvercle attend, en l'air."),
            ("maman", "Le vestiaire sent moins le sucré."),
            ("narrateur", "Le rayon quitte la porte, et le cercle reste un peu."),
        ),
        (3, 2, 3): L(
            ("narrateur", "Papa lâche le couvercle, et le bouton reçoit le verre."),
            ("enfant-m", "Le fil, pile là."),
            ("maman", "Le couvercle n'a plus fait d'ombre."),
            ("narrateur", "Un cercle d'or s'accroche au métal, puis au sol."),
            ("narrateur", "Aniss cligne, puis regarde le rond."),
            ("papa", "Merci d'avoir vu la tache, Nino."),
            ("enfant-m", "On a levé, et la vitre a parlé."),
            ("narrateur", "La boîte, au casier, s'est tue."),
            ("maman", "Le sucré reste, plus loin."),
            ("narrateur", "La serviette a gardé un pli collant."),
        ),
        (3, 3, 1): L(
            ("narrateur", "Nino cale la lentille, loin de l'odeur."),
            ("enfant-m", "J'ai éloigné le tissu."),
            ("papa", "L'air a parlé, et Aniss est revenu."),
            ("narrateur", "Un cercle d'or tombe près des chaussures, pâle."),
            ("narrateur", "Aniss le regarde, le nez tranquille."),
            ("maman", "Tu n'as pas saisi la serviette, cette fois."),
            ("enfant-m", "Ma chasse aux reflets."),
            ("narrateur", "La boîte, derrière, reste ouverte."),
            ("papa", "Le savon du vestiaire tient, dans l'air."),
            ("narrateur", "Un cercle d'or s'éteint sur le caoutchouc."),
        ),
        (3, 3, 2): L(
            ("narrateur", "Nino pose le verre sous le bouton, et souffle."),
            ("enfant-m", "Le grain d'or, sur le casier."),
            ("maman", "Sans l'odeur sous le nez."),
            ("narrateur", "Un cercle d'or glisse du métal vers le caoutchouc."),
            ("narrateur", "Aniss ne détourne plus le visage."),
            ("papa", "Tu as soufflé, pas saisi."),
            ("enfant-m", "Le bord jaune est chaud."),
            ("narrateur", "Le couvercle de la boîte s'est un peu refermé."),
            ("maman", "La semelle sent le savon, un peu."),
            ("narrateur", "La poussière ne danse plus, dans le vestiaire."),
        ),
        (3, 3, 3): L(
            ("narrateur", "Papa lâche le couvercle, et Nino cale le verre."),
            ("enfant-m", "Les souliers ont de la lumière."),
            ("maman", "Le couvercle n'a plus fait d'ombre."),
            ("narrateur", "Un cercle d'or s'assoit près des paires, rond."),
            ("narrateur", "Aniss n'a pas détourné le nez."),
            ("papa", "Merci d'avoir demandé, Nino."),
            ("enfant-m", "On a levé, et le rayon est venu."),
            ("narrateur", "La serviette reste plus loin, pliée."),
            ("maman", "Le vestiaire sent le savon, et le soleil."),
            ("narrateur", "Le bouton du casier cliquette, très bas, puis s'arrête."),
        ),
    }[(a, b, c)]


T2_SONS = {1: "banc", 2: "vitre", 3: "chaussures"}
T3_SONS = {1: "silence", 2: "souffle", 3: "tissu"}
FIN_SONS = {
    1: "casier,banc",
    2: "casier,vitre",
    3: "casier,chaussures",
}


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


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "porte_classe", "emphasis": "lentille jaune"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Le casier reste sombre, derrière la bande de soleil."),
            ("maman", "Le manteau, le cartable, ou la boîte ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le manteau",
            "option_2_label": "le cartable",
            "option_3_label": "la boîte",
        }},
    )

    for a, t1 in T1.items():
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(
            by_old[base], t1["passage"], "action",
            extra={"sons": t1["sons"], "emphasis": t1["name"]},
        )
        by[f"{base}_Q0001"] = voice(
            by_old[f"{base}_Q0001"], t1["question"], "clue",
            extra={"sons": "", "emphasis": t1["emp"], "fields": {
                "expected_answer": t1["expected"],
                "accepted_examples": t1["accepted"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "Tu es tout près. Reprenons la scène.",
            }},
        )
        by[f"{base}_C0001"] = voice(
            by_old[f"{base}_C0001"], t1["confirm"], "confirm",
            extra={"sons": "", "emphasis": "lentille"},
        )
        by[f"{base}_T0002_P0000"] = voice(
            by_old[f"{base}_T0002_P0000"], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "le banc",
                "option_2_label": "la vitre",
                "option_3_label": "les chaussures",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], t2(a, b), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": "bord jaune"},
            )
            t3q = f"{p2}_T0003_P0000"
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": "on attend",
                    "option_2_label": "on souffle",
                    "option_3_label": "on lève",
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], t3(a, b, c), "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": "lentille" if c != 2 else "souffle"},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], ending(a, b, c), "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": "cercle d'or"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")

    last_lines = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        narr = [ln for ln in by[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        last_lines.append(narr[-1])
    if len(set(last_lines)) != 27:
        raise SystemExit(f"dernières images non distinctes: {len(set(last_lines))}/27")

    counts = [sum(words(by[i]["text"]) for i in path_ids(a, b, c))
              for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(counts) < 520:
        raise SystemExit(f"chemin trop court: min={min(counts)} max={max(counts)}")

    tts_ok = all(
        c.get("text_xai_tags") and c.get("notes") and c.get("style_energy")
        for c in by.values()
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = (
        "Dans le vestiaire des casiers, une bande de soleil coupe la porte "
        "de Nino. Il veut accrocher sa lentille jaune au bouton avant que "
        "le rayon ne parte : une chasse aux reflets. Il ouvre trop vite. "
        "Aniss, sur le banc, regarde autrement. Nino cherche dans le manteau, "
        "le cartable ou la boîte, puis au banc, à la vitre ou près des "
        "chaussures. Attendre, souffler ou lever change le geste. La lentille "
        "revient au bouton, avec une trace, et un cercle d'or."
    )
    out["title"] = "Le rayon sur le casier"
    out["characters"] = "Nino, Aniss, papa, maman"
    out["setting"] = "couloir de l'école, casiers, vestiaire des reflets"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    low = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in TICS:
        if tic in low:
            raise SystemExit(f"tic global: {tic}")
    n_enc = len(re.findall(r"\bencore\b", low))
    n_dej = len(re.findall(r"\bdéjà\b", low))
    if n_enc > 2 or n_dej > 2:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-DIF-007 — Le rayon sur le casier\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Graphe source conservé "
        "(manteau / cartable / boîte ; banc / vitre / chaussures ; "
        "on attend / on souffle / on lève).\n\n"
        "## Promesse narrative\n"
        "Dans le vestiaire des casiers, une bande de soleil coupe la porte "
        "grise. Nino veut accrocher sa **lentille jaune** au bouton **maintenant**, "
        "pour un cercle d'or, avant que le rayon ne parte. Première idée : "
        "ouvrir trop vite. Les feuilles glissent, un tic roule. Aniss s'assoit "
        "sur le banc, les mains à plat, et ne vient pas. T1 change l'objet "
        "fouillé et l'échec (manche qui balaye le rayon, zzzit trop fort, "
        "clac de la boîte). T2 change le second imprévu (genoux d'Aniss, "
        "ombre sur la vitre, lacette / orteil / odeur). T3 change le geste "
        "(attendre comme Aniss, souffler un grain, demander à lever). "
        "Chaque fin paie la lentille, le bouton, le rayon, Aniss.\n\n"
        "## Vécu\n"
        "- Désir : porter la lentille jusqu'au bouton, chasse aux reflets.\n"
        "- Imprévu 1 : poignée trop forte, tic qui se tait, Aniss immobile.\n"
        "- Imprévu 2 : ramper / courir / tirer / froisser / plaquer / "
        "saisir — Aniss recule, se bouche les oreilles, cligne, détourne.\n"
        "- DIF.BES.001 vécu, pas dit : Aniss a besoin d'air, de silence, "
        "d'un autre rythme. Nino change de manière (mains à plat, souffle "
        "mince, demander avant de lever). Le silence d'Aniss compte.\n"
        "- Nuances : attendre / souffler / lever ; le camarade n'est pas "
        "corrigé, c'est Nino qui ajuste le regard.\n"
        "- Pas de refrain example3, pas de merle, pas de miel, pas de "
        "« aujourd'hui, », pas de tout doux / tout calme.\n\n"
        "## Vu et corrigé\n"
        f"- Titre noyau conservé. N2 ≤ 15. Troupe D16 : Nino, Aniss, papa, maman.\n"
        f"- 86 nœuds, 27 chemins, 27 fins textuellement distinctes, "
        f"27 dernières images distinctes.\n"
        f"- Mots par chemin : {min(counts)}–{max(counts)}, moyenne {sum(counts)//27}.\n"
        "- Questions : crayon / cartable / boîte, après la scène (rappel).\n"
        "- Un merci adulte vécu dans chaque T3, pas un refrain Bravo.\n"
        "- TTS par chunk (opening/choice/clue/confirm/action/obstacle/"
        "resolution/ending) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration).\n"
        "- `text` / `script` synchronisés. Pas apply.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(
        f"OK {SID} {nwords} mots  fins={len(set(fins))}  "
        f"chemins {min(counts)}-{max(counts)}"
    )


if __name__ == "__main__":
    build()
