#!/usr/bin/env python3
"""TREE-COL-001 — Le voyage des pommes de Raphaël (F-NAR-019). N2, COL.POL.001."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-001"
LIM = 15
TICS = (
    "tout doux",
    "tout calme",
    "on lève la main",
    "puis on parle",
    "c'est du bon travail",
    "on va apprendre",
    "si malaise",
    "l'histoire est finie",
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la_feuille_va_tomber; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_voyage; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ou_elle_est_allee; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; destinataire=enfant; sous_texte=le_mot_a_ouvert_la_main; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_la_pomme_bascule; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=decouragement; intensite=2; destinataire=enfant; sous_texte=couper_fait_rater_l_arret; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=fierte_calme; intensite=2; destinataire=enfant; sous_texte=demander_a_ouvert_le_geste; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=la_feuille_et_le_fil_blanc_reviennent; tempo=pose; sourire=léger; respiration=ample",
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
    out: list[tuple[str, str]] = []
    for role, ph in rows:
        parts = re.findall(r".+?[.!?]", ph.strip())
        leftover = ph.strip()
        for p in parts:
            leftover = leftover.replace(p, "", 1)
        if leftover.strip():
            raise SystemExit(f"reste {leftover!r}: {ph}")
        if not parts:
            raise SystemExit(f"sans phrase: {ph}")
        for part in parts:
            out.append((role, part.strip()))
    return out


OPENING = L(
    ("narrateur", "Le couvercle lâche un fil blanc, au-dessus de la casserole."),
    ("narrateur", "Ça sent la pomme, et le panier mouillé."),
    ("narrateur", "Dehors, le marché plie ses dernières caisses."),
    ("narrateur", "Le carrelage fait un quai, entre la table et le feu."),
    ("narrateur", "Un bol jaune attend, collant un peu."),
    ("narrateur", "Les rondelles brillent, comme de petites lunes."),
    ("narrateur", "Une pomme entière porte sa feuille verte."),
    ("narrateur", "Le torchon rayé pend de travers, sur une chaise."),
    ("narrateur", "Près du bol, une cuillère de bois a le manche rouge."),
    ("narrateur", "Elle a une entaille, et elle fait toc, contre le bord."),
    ("narrateur", "Les chaussettes de Raphaël sont humides, du jardin."),
    ("narrateur", "En ce moment, il surveille la feuille qui tremble."),
    ("enfant-m", "Je veux l'offrir à Mila, avant la tarte."),
    ("maman", "Elle arrive, j'entends le gravier."),
    ("narrateur", "Raphaël saisit le bol, et la cuillère-capitaine."),
    ("narrateur", "Le bol est trop lourd, pour lui seul."),
    ("narrateur", "La pomme roule jusqu'au bord, la feuille penche."),
    ("enfant-m", "Elle va tomber !"),
    ("papa", "Tes jouets peuvent porter ça, tu crois ?"),
    ("narrateur", "La feuille penche, comme un petit chapeau."),
    ("narrateur", "Des pas pressés sonnent, sur le gravier."),
    ("enfant-m", "Mila, les pommes, vite !"),
    ("papa", "Regarde-la d'abord, ensuite le bol."),
    ("maman", "Qu'est-ce que tu prends, pour l'emmener ?"),
)

T1 = {
    1: dict(
        name="le train",
        passage=L(
            ("narrateur", "Raphaël saisit le train de bois, près du bol."),
            ("narrateur", "Les roues font clic, sur le carrelage froid."),
            ("narrateur", "La cuillère-capitaine s'assoit dans le premier wagon."),
            ("narrateur", "La porte s'ouvre. Mila entre, les joues roses."),
            ("narrateur", "Ses cheveux sentent la pluie arrêtée."),
            ("narrateur", "Raphaël pousse le train contre ses pieds, sans lever les yeux."),
            ("enfant-m", "C'est le train des pommes !"),
            ("narrateur", "Mila reste plantée, un petit panier contre le ventre."),
            ("enfant-f", "Hein ?"),
            ("narrateur", "Il glisse la pomme entre deux wagons, trop vite."),
            ("narrateur", "La feuille se coinse, puis le fruit bascule."),
            ("enfant-f", "Elle tombe !"),
            ("narrateur", "Raphaël s'arrête, puis lève enfin le visage."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour, Raphaël."),
            ("papa", "Le bol est lourd, allez-y à deux."),
            ("narrateur", "Ils glissent le bol entre les wagons."),
            ("narrateur", "La pomme à feuille n'est plus dedans."),
        ),
        question=L(
            ("narrateur", "La pomme à feuille n'est plus dans le bol."),
            ("maman", "Où est-elle allée ?"),
        ),
        expected="wagons",
        accepted="wagons | entre les wagons | pomme | par terre | le train",
        retry="La pomme à feuille n'est plus dans le bol. Où est-elle ?",
        ok="Oui, entre les wagons.",
        confirm=L(
            ("enfant-m", "Entre les wagons !"),
            ("narrateur", "Oui, elle brille un peu loin, sous le bois."),
            ("papa", "Merci d'avoir levé les yeux, d'abord."),
            ("enfant-f", "On la suit, sans la bousculer."),
            ("narrateur", "Le bol reste sur le train, la cuillère tapote, toc."),
            ("maman", "Le torchon rayé peut aider, tout à l'heure."),
        ),
        sons="train_bois,porte",
        choice=L(
            ("narrateur", "La pomme roule, et le train n'a pas de gare."),
            ("papa", "La table, la fenêtre, ou le tabouret ?"),
        ),
        emp="entre deux wagons",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=sans_bonjour_la_pomme_tombe; tempo=vif; sourire=léger; respiration=courte",
    ),
    2: dict(
        name="le bus",
        passage=L(
            ("narrateur", "Raphaël prend le bus rouge, un peu cabossé."),
            ("narrateur", "Dehors, un vrai bus souffle, très bas."),
            ("narrateur", "Il pose la cuillère-capitaine sur le toit plat."),
            ("narrateur", "Mila pousse la porte, les joues mouillées."),
            ("enfant-m", "Bonjour."),
            ("enfant-f", "Bonjour."),
            ("narrateur", "Une miette colle au rebord du bol jaune."),
            ("narrateur", "Maman essuie la planche, le torchon à la main."),
            ("narrateur", "Raphaël tire le tissu, trop vite."),
            ("narrateur", "La main de maman vient avec, surprise."),
            ("maman", "Hé, j'ai pas fini le bois."),
            ("narrateur", "Le bol bascule. La pomme fuit sous la chaise."),
            ("enfant-m", "Le torchon, s'il te plaît."),
            ("maman", "Le voilà, maintenant."),
            ("narrateur", "Il essuie le rebord, et les sièges peuvent recevoir."),
            ("enfant-f", "Les rondelles montent, une par une."),
            ("narrateur", "La pomme à feuille, elle, n'est plus dans le bus."),
        ),
        question=L(
            ("narrateur", "La pomme à feuille n'est plus dans le bol."),
            ("papa", "Où est-elle allée ?"),
        ),
        expected="chaise",
        accepted="chaise | sous la chaise | pomme | par terre | le bus",
        retry="La pomme à feuille n'est plus dans le bol. Où est-elle ?",
        ok="Oui, sous la chaise.",
        confirm=L(
            ("enfant-m", "Sous la chaise !"),
            ("narrateur", "Oui, elle brille un peu loin, près d'un pied."),
            ("maman", "Merci d'avoir attendu ma main."),
            ("enfant-f", "On la suit, le torchon prêt."),
            ("narrateur", "Le bol reste sur le bus, la cuillère tapote, toc."),
            ("papa", "Doucement, le carrelage est froid."),
        ),
        sons="bus,porte",
        choice=L(
            ("narrateur", "La pomme roule, et le bus n'a pas d'arrêt."),
            ("maman", "La table, la fenêtre, ou le tabouret ?"),
        ),
        emp="sous la chaise",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=sans_demander_le_torchon_part; tempo=vif; sourire=léger; respiration=courte",
    ),
    3: dict(
        name="la voiture",
        passage=L(
            ("narrateur", "Raphaël prend la petite voiture, lisse et froide."),
            ("narrateur", "Il glisse la cuillère-capitaine contre le volant."),
            ("narrateur", "Mila arrive, son manteau sent la pluie."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour."),
            ("enfant-f", "Tu accroches mon manteau ?"),
            ("maman", "Oui, donne."),
            ("narrateur", "Le manteau goutte un peu, près de la chaise."),
            ("papa", "Une rondelle pour la route ?"),
            ("narrateur", "Raphaël attrape le fruit, mais les doigts de papa restent."),
            ("narrateur", "La rondelle ne vient pas."),
            ("enfant-m", "Oui, merci."),
            ("narrateur", "Alors la main s'ouvre, et la rondelle est à lui."),
            ("narrateur", "Il la pose sur le capot, pour de faux."),
            ("narrateur", "Le métal froid la fait glisser tout de suite."),
            ("narrateur", "Le bol penche. La pomme se coince contre le livre."),
            ("enfant-f", "Elle file !"),
        ),
        question=L(
            ("narrateur", "La pomme à feuille n'est plus dans le bol."),
            ("maman", "Où est-elle allée ?"),
        ),
        expected="livre",
        accepted="livre | contre le livre | pomme | par terre | la voiture",
        retry="La pomme à feuille n'est plus dans le bol. Où est-elle ?",
        ok="Oui, contre le livre.",
        confirm=L(
            ("enfant-m", "Contre le livre !"),
            ("narrateur", "Oui, elle brille un peu loin, près des recettes."),
            ("papa", "Merci, j'ai entendu ta voix."),
            ("enfant-f", "On la suit, sans coller le capot."),
            ("narrateur", "Le bol reste sur la voiture, la cuillère tapote, toc."),
            ("maman", "Le livre de tarte peut attendre, une minute."),
        ),
        sons="voiture,manteau",
        choice=L(
            ("narrateur", "La pomme roule, et la voiture n'a pas de garage."),
            ("papa", "La table, la fenêtre, ou le tabouret ?"),
        ),
        emp="contre le livre",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=sans_merci_la_rondelle_reste; tempo=vif; sourire=léger; respiration=courte",
    ),
}


def t2(a: int, b: int) -> list[tuple[str, str]]:
    veh = {1: "Le train", 2: "Le bus", 3: "La voiture"}[a]
    if a == 1 and b == 1:
        return L(
            ("narrateur", "Le train file vers la table, wagon par wagon."),
            ("narrateur", "La pomme à feuille roule sous la nappe."),
            ("narrateur", "Des assiettes occupent toute la place."),
            ("narrateur", "Le bol n'a pas de quai."),
            ("enfant-m", "On pousse les assiettes !"),
            ("narrateur", "Il avance trop vite, et une cuillère tombe."),
            ("enfant-f", "Attends, je demande."),
            ("enfant-f", "Maman, on pose le bol ici ?"),
            ("maman", "Oui, je dégage un coin."),
            ("narrateur", "Maman glisse la planche mouillée vers le bord."),
            ("narrateur", "Un petit quai apparaît, entre deux assiettes."),
            ("enfant-m", "Gare table !"),
            ("narrateur", "La feuille penche vers la cuillère tombée."),
            ("papa", "Vous la prenez comment, cette passagère ?"),
        )
    if a == 1 and b == 2:
        return L(
            ("narrateur", "Le train glisse jusqu'à la fenêtre embuée."),
            ("narrateur", "La pomme à feuille s'arrête contre la vitre."),
            ("narrateur", "Le marché, dehors, n'est plus qu'un flou."),
            ("enfant-f", "Je dessine la gare, dans la buée."),
            ("narrateur", "Mila trace un petit rectangle, avec le doigt."),
            ("enfant-m", "Je veux voir les caisses !"),
            ("narrateur", "Il essuie trop, et le rectangle disparaît."),
            ("enfant-f", "Ma gare !"),
            ("narrateur", "Raphaël baisse la main, les joues chaudes."),
            ("enfant-m", "Redessine, tout petit."),
            ("narrateur", "Elle trace un rond, et le marché apparaît dedans."),
            ("narrateur", "La feuille regarde les caisses, par le rond."),
            ("papa", "Qui pousse jusqu'à ce rond, sans tout effacer ?"),
        )
    if a == 1 and b == 3:
        return L(
            ("narrateur", "Le train arrive au tabouret de bois clair."),
            ("narrateur", "La pomme à feuille se cache sous le siège."),
            ("enfant-f", "C'est la gare haute !"),
            ("narrateur", "Mila s'assoit, et le tabouret bascule un peu."),
            ("enfant-m", "Le bol va là-haut."),
            ("narrateur", "Il pose le bol sur le bois, et ça penche."),
            ("papa", "Le bol va glisser, descends-le."),
            ("narrateur", "Raphaël reprend le bol, les bras tendus."),
            ("enfant-f", "Le train passe en dessous, comme un tunnel."),
            ("narrateur", "Ils baissent le bol au sol, sous le siège."),
            ("narrateur", "Le tabouret fait un toit, et craque."),
            ("maman", "Il tient, si personne ne gigote."),
            ("papa", "Vous la prenez comment, sous le toit ?"),
        )
    if a == 2 and b == 1:
        return L(
            ("narrateur", "Le bus rouge roule vers la table."),
            ("narrateur", "La pomme à feuille file sous une assiette."),
            ("narrateur", "Raphaël veut décharger tout de suite, sur les assiettes."),
            ("narrateur", "Une rondelle tombe dans une cuillère."),
            ("enfant-f", "Elles restent dans le bus, l'arrêt n'est pas prêt !"),
            ("narrateur", "Il s'arrête, déçu, la main au-dessus du bol."),
            ("enfant-m", "On fait un guichet, alors."),
            ("narrateur", "Deux tasses deviennent un petit bureau."),
            ("enfant-f", "Ticket, c'est la miette sur la tasse."),
            ("maman", "Je vous laisse ce coin, près du sel."),
            ("narrateur", "Un quai étroit apparaît, assez pour le bus."),
            ("narrateur", "La feuille attend, collée au rebord d'une assiette."),
            ("papa", "Vous la prenez comment, sans tout verser ?"),
        )
    if a == 2 and b == 2:
        return L(
            ("narrateur", "Le bus s'approche de la vitre floue."),
            ("narrateur", "La pomme à feuille s'arrête contre le verre."),
            ("narrateur", "Dehors, le vrai bus passe, et fait trembler le verre."),
            ("enfant-m", "On part avec lui !"),
            ("narrateur", "Raphaël pousse trop vite, et la buée s'étale."),
            ("narrateur", "L'arrêt dessiné n'est plus qu'une tache."),
            ("enfant-f", "Attends qu'il soit parti, le grand."),
            ("narrateur", "Ils restent, pendant que le vrai bus s'éloigne."),
            ("enfant-f", "Maintenant, j'en dessine un, pour nous."),
            ("narrateur", "Un arrêt simple apparaît, un trait, un point."),
            ("narrateur", "Leur bus rouge se gare dans le trait."),
            ("maman", "Le grand est parti, et le petit a sa place."),
            ("papa", "Vous la prenez comment, sans fondre le trait ?"),
        )
    if a == 2 and b == 3:
        return L(
            ("narrateur", "Le bus vise le tabouret, comme un abri."),
            ("narrateur", "La pomme à feuille roule sous le bois."),
            ("enfant-f", "Je tiens le poteau d'arrêt."),
            ("narrateur", "Mila redresse le tabouret, les bras qui tremblent."),
            ("enfant-m", "Je me gare tout contre."),
            ("narrateur", "Le bois penche sur le toit du bus."),
            ("enfant-f", "Tu es trop près, il va nous tomber dessus !"),
            ("narrateur", "Raphaël recule d'une case de carrelage."),
            ("narrateur", "Le tabouret se cale, et l'abri tient."),
            ("papa", "Un peu d'air, entre le bois et les sièges."),
            ("narrateur", "La feuille a de l'ombre, sans le poids."),
            ("maman", "Vous avez laissé de la place au poteau."),
            ("papa", "Vous la prenez comment, sans serrer ?"),
        )
    if a == 3 and b == 1:
        return L(
            ("narrateur", "La voiture roule vers la table mouillée."),
            ("narrateur", "La pomme à feuille glisse dans une flaque de jus."),
            ("narrateur", "La planche a laissé cette flaque, près du sel."),
            ("enfant-m", "On se gare ici, capot contre le bois."),
            ("narrateur", "La rondelle du capot glisse dans la flaque."),
            ("enfant-f", "Trop mouillé !"),
            ("narrateur", "Raphaël veut la reprendre à toute vitesse."),
            ("enfant-f", "Le torchon, on sèche un carré."),
            ("narrateur", "Maman a fini, et le torchon rayé est libre."),
            ("enfant-m", "Je prends le coin près du sel, il est sec."),
            ("narrateur", "Un petit garage apparaît, mat, sans flaque."),
            ("narrateur", "La feuille attend dans le jus, à deux doigts."),
            ("papa", "Vous la prenez comment, sans la flaque ?"),
        )
    if a == 3 and b == 2:
        return L(
            ("narrateur", "La voiture vise la fenêtre, pour montrer le marché."),
            ("narrateur", "La pomme à feuille s'arrête contre la vitre."),
            ("enfant-m", "Les caisses doivent nous voir !"),
            ("narrateur", "Il plaque le jouet contre le verre."),
            ("narrateur", "La buée prend tout, on ne voit plus rien."),
            ("narrateur", "Une goutte tombe du haut, sur le capot."),
            ("enfant-f", "Ta rondelle est mouillée."),
            ("narrateur", "Raphaël recule, déçu, la voiture collée aux doigts."),
            ("enfant-f", "Le soleil, sur le carrelage, fait un carré."),
            ("narrateur", "Ils posent la voiture dans le carré chaud."),
            ("enfant-m", "Et toi, tu dessines la route, sur la vitre."),
            ("narrateur", "Une route de buée descend jusqu'au carré."),
            ("maman", "Le marché nous voit, par la route."),
            ("papa", "Vous la prenez comment, sans quitter la route ?"),
        )
    _ = veh
    return L(
        ("narrateur", "La voiture arrive au tabouret, pour en faire une rampe."),
        ("narrateur", "La pomme à feuille se cache sous le pied."),
        ("enfant-m", "Je monte, et je descends !"),
        ("narrateur", "Il envoie la voiture trop fort, et elle saute."),
        ("enfant-f", "Je l'ai !"),
        ("narrateur", "Mila rattrape le jouet, tout près du sol."),
        ("papa", "Trop raide, cette montagne."),
        ("enfant-f", "On baisse, avec le livre de recettes."),
        ("narrateur", "Papa glisse le livre sous un pied."),
        ("narrateur", "La rampe devient douce, presque plate."),
        ("narrateur", "La feuille, sous le bois, ne bascule plus."),
        ("maman", "Le tabouret a cessé de danser."),
        ("papa", "Vous la prenez comment, sans faire sauter le capot ?"),
    )


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Le quai est étroit, il reste un dernier geste."),
            ("maman", "On ramasse, on attend, ou on invente ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "La vitre surveille, il reste un dernier geste."),
            ("papa", "On ramasse, on attend, ou on invente ?"),
        )
    return L(
        ("narrateur", "Le bois craque, il reste un dernier geste."),
        ("maman", "On ramasse, on attend, ou on invente ?"),
    )


T3 = {
    (1, 1, 1): L(
        ("enfant-m", "Le torchon, s'il te plaît."),
        ("maman", "Le voilà."),
        ("narrateur", "Mila tient le tissu, Raphaël glisse la main."),
        ("narrateur", "Il touche la pomme, sous la nappe."),
        ("enfant-f", "Je te la passe."),
        ("enfant-m", "Merci."),
        ("narrateur", "Le fruit est un peu froid, la feuille pliée."),
        ("narrateur", "Ils le posent dans le bol, loin de la cuillère tombée."),
        ("papa", "Tu as demandé, et le quai a reçu sa passagère."),
        ("narrateur", "La cuillère-capitaine tapote le bois, toc."),
    ),
    (1, 1, 2): L(
        ("enfant-m", "On attend. Elle tremble."),
        ("narrateur", "La pomme s'arrête sous la nappe, enfin."),
        ("narrateur", "Raphaël compte les carreaux, un par un."),
        ("enfant-f", "Plus lent, le bol penche !"),
        ("narrateur", "Il souffle, et avance deux doigts."),
        ("narrateur", "Mila tient la feuille, à peine."),
        ("enfant-m", "Gare."),
        ("maman", "Vous avez laissé le temps, et l'assiette n'a pas tinté."),
        ("narrateur", "Le fruit roule dans sa paume, puis dans le bol."),
        ("narrateur", "La cuillère tombée reste à sa place."),
    ),
    (1, 1, 3): L(
        ("enfant-m", "C'est l'invitée en retard."),
        ("enfant-f", "Le restaurant ouvre pour elle."),
        ("narrateur", "Ils posent la pomme sous la nappe, comme un siège."),
        ("enfant-m", "S'il te plaît, une rondelle."),
        ("enfant-f", "Voilà, madame Pomme."),
        ("narrateur", "Une table pour trois, alors."),
        ("narrateur", "Mila glisse une rondelle près de la ronde."),
        ("papa", "Vous avez inventé une place, et le bol a suivi."),
        ("narrateur", "Deux traces de jus brillent sur le bois, côte à côte."),
        ("narrateur", "La cuillère-capitaine garde la porte, toc."),
    ),
    (1, 2, 1): L(
        ("enfant-f", "Je ramasse près du rond, et toi tu n'essuies plus."),
        ("narrateur", "Raphaël cache ses mains dans son dos, pour de vrai."),
        ("narrateur", "Mila glisse le torchon sous la pomme, contre la vitre."),
        ("narrateur", "Une goutte de buée glisse vers le rond."),
        ("enfant-m", "Elle va le manger !"),
        ("enfant-f", "On prend le fruit, pas la goutte."),
        ("narrateur", "La goutte passe à côté, et le rond reste."),
        ("maman", "Tu as regardé la vitre, pas seulement le train."),
        ("narrateur", "La pomme rentre dans le bol, la feuille vers le marché."),
        ("narrateur", "Le train attend sous le rebord."),
    ),
    (1, 2, 2): L(
        ("enfant-m", "On attend que le soleil chauffe le verre."),
        ("narrateur", "Le premier wagon arrive dans la lumière."),
        ("narrateur", "La feuille se recroqueville, un peu molle."),
        ("enfant-f", "Elle a trop chaud, je la fais de l'ombre."),
        ("narrateur", "Mila creuse un toit avec sa paume."),
        ("narrateur", "Ils restent, et la pomme cesse de glisser."),
        ("narrateur", "Raphaël avance deux doigts, dans l'ombre de la main."),
        ("papa", "Le rond de buée est resté, grâce à vous."),
        ("narrateur", "Le fruit rejoint le bol, sans frotter la vitre."),
        ("narrateur", "Dehors, une caisse se ferme, sans bruit."),
    ),
    (1, 2, 3): L(
        ("enfant-m", "On invente deux gares, avec nos nez."),
        ("narrateur", "Leurs deux fronts s'approchent de la vitre."),
        ("narrateur", "La buée s'ouvre en deux petits ronds."),
        ("enfant-f", "Deux gares !"),
        ("narrateur", "Ils glissent le train sous les deux ronds."),
        ("narrateur", "La pomme passe d'une gare à l'autre, puis au bol."),
        ("maman", "Vous n'avez rien essuyé, cette fois."),
        ("narrateur", "Le marché apparaît, net, le temps d'un souffle."),
        ("narrateur", "La feuille sèche un peu, sur le rebord."),
        ("narrateur", "La cuillère-capitaine veille entre les deux ronds."),
    ),
    (1, 3, 1): L(
        ("enfant-f", "Je ramasse sous le toit, et toi tu tiens le pied."),
        ("narrateur", "Raphaël s'assoit par terre, une main sur le bois."),
        ("narrateur", "Le tabouret veut danser, et il le retient."),
        ("enfant-m", "J'ai mal au poignet."),
        ("enfant-f", "Une case de plus."),
        ("narrateur", "Elle glisse le torchon, et attrape la pomme."),
        ("narrateur", "Le fruit rentre dans le bol, sous le siège."),
        ("papa", "Le toit n'a pas marché sur les wagons."),
        ("narrateur", "La feuille est à l'ombre, passagère cachée."),
        ("narrateur", "La cuillère-capitaine tapote le wagon de queue."),
    ),
    (1, 3, 2): L(
        ("enfant-m", "On attend que le bois se taise."),
        ("narrateur", "Il veut monter sur le pied, trop haut."),
        ("enfant-f", "Non, en dessous, on avait dit."),
        ("narrateur", "Raphaël recule, contrarié, puis se baisse."),
        ("narrateur", "Ils comptent jusqu'à trois, sans gigoter."),
        ("narrateur", "Mila glisse un livre à plat, pour caler le bol."),
        ("narrateur", "La pomme roule dans sa paume, puis dans le bol."),
        ("maman", "Tu as changé de chemin, et le bol a tenu."),
        ("narrateur", "Un craquement, puis plus rien."),
        ("narrateur", "Le train passe, et le livre fait tampon."),
    ),
    (1, 3, 3): L(
        ("enfant-m", "On invente un pont, tous les deux."),
        ("narrateur", "Ils lèvent le tabouret, comme un pont."),
        ("narrateur", "Le train passe en dessous, sans se frotter."),
        ("enfant-f", "On repose, sur trois."),
        ("enfant-m", "Trois."),
        ("narrateur", "Le bois retrouve le carrelage, sans claquer."),
        ("narrateur", "La pomme, au milieu, entre dans le bol."),
        ("papa", "Le pont s'est refermé pile après le dernier wagon."),
        ("narrateur", "La feuille a traversé l'ombre, intacte."),
        ("narrateur", "La cuillère-capitaine a passé le tunnel, toc."),
    ),
    (2, 1, 1): L(
        ("enfant-f", "Je ramasse près du guichet, et toi tu gardes le ticket."),
        ("narrateur", "Raphaël tient la tasse, trop serrée."),
        ("narrateur", "La miette-ticket saute sur la table."),
        ("enfant-m", "Pardon, je la remets."),
        ("narrateur", "Mila glisse le torchon sous l'assiette."),
        ("narrateur", "La pomme rejoint les sièges du bus, puis le bol."),
        ("enfant-f", "Arrêt guichet."),
        ("maman", "Tu as rendu le ticket, et le bus a pu s'arrêter."),
        ("narrateur", "La feuille descend la première, invitée."),
        ("narrateur", "La cuillère-capitaine poinçonnerait, si elle pouvait."),
    ),
    (2, 1, 2): L(
        ("enfant-m", "On attend. Toutes les pommes descendent !"),
        ("narrateur", "Il bascule le bol, et une rondelle fuit vers le sel."),
        ("enfant-f", "Dans le bus, pas sur la table !"),
        ("narrateur", "Mila rattrape la fuyarde, la remet sur un siège."),
        ("narrateur", "Raphaël pose le bol, les épaules basses."),
        ("enfant-m", "Une par une, alors."),
        ("narrateur", "Ils attendent que la pomme cesse de rouler."),
        ("narrateur", "Deux doigts, et elle rentre dans le bol."),
        ("papa", "Le guichet a attendu que tu finisses."),
        ("narrateur", "La dernière, c'est la feuille, posée sans bruit."),
    ),
    (2, 1, 3): L(
        ("enfant-m", "On invente un poinçon, toi le volant, moi les tasses."),
        ("enfant-f", "Et le ticket, on le pose ensemble."),
        ("narrateur", "Ils avancent le bus d'un côté, les tasses de l'autre."),
        ("narrateur", "Le guichet et l'arrêt se rencontrent, pile au sel."),
        ("enfant-f", "Poinçon !"),
        ("narrateur", "Un doigt de chaque enfant appuie sur la miette."),
        ("narrateur", "La pomme paie sa place, pour de faux, puis rentre."),
        ("maman", "Deux poinçons, un seul ticket."),
        ("narrateur", "La feuille a son siège, près du sel."),
        ("narrateur", "La cuillère-capitaine garde le toit, toc."),
    ),
    (2, 2, 1): L(
        ("enfant-f", "Je ramasse au rythme du grand, dehors."),
        ("narrateur", "Le vrai bus est loin, et Mila va très lentement."),
        ("enfant-m", "Trop lent, on n'arrive jamais !"),
        ("narrateur", "Il veut pousser par-dessus ses mains."),
        ("enfant-f", "Le trait va fondre."),
        ("narrateur", "Il retire ses doigts, et elle glisse le torchon."),
        ("narrateur", "La pomme quitte la vitre, entre dans le bol."),
        ("papa", "Tu as laissé le volant, et l'arrêt est resté net."),
        ("narrateur", "Une virgule de buée tombe, loin du point."),
        ("narrateur", "Le bus rouge dort dans son trait, tout petit."),
    ),
    (2, 2, 2): L(
        ("enfant-m", "Klaxon !"),
        ("narrateur", "Sa voix est trop forte, et la vitre vibre."),
        ("enfant-f", "Chut, le grand va croire qu'on se moque."),
        ("narrateur", "Raphaël se tait, la bouche ronde, un peu honteux."),
        ("narrateur", "Ils attendent que le vrai bus ait tourné la rue."),
        ("narrateur", "Alors seulement, il avance deux doigts, sans bruit."),
        ("narrateur", "La pomme cesse de trembler, et rentre dans le bol."),
        ("maman", "Votre arrêt n'a pas crié plus fort que le village."),
        ("narrateur", "Le bus rouge dort dans son trait, tout petit."),
        ("narrateur", "La feuille sèche, loin de la tache de buée."),
    ),
    (2, 2, 3): L(
        ("enfant-f", "On invente deux tickets, un chacun, dans la buée."),
        ("narrateur", "Ils dessinent deux petits rectangles, côte à côte."),
        ("enfant-m", "Le mien, c'est pour la feuille."),
        ("narrateur", "Ils poussent le bus sous les deux tickets."),
        ("narrateur", "La pomme passe sous les rectangles, puis au bol."),
        ("narrateur", "Les rectangles gouttent, mais restent lisibles."),
        ("papa", "Vous avez chacun votre place, et le même arrêt."),
        ("narrateur", "Dehors, le grand bus n'est plus qu'un point."),
        ("narrateur", "La cuillère-capitaine a son ticket, un toc."),
        ("narrateur", "La feuille paie, pour de faux."),
    ),
    (2, 3, 1): L(
        ("enfant-f", "Je ramasse, et toi tu tiens l'abri."),
        ("narrateur", "Les bras de Raphaël tremblent autour du tabouret."),
        ("enfant-m", "Il est lourd, ce poteau."),
        ("narrateur", "Mila glisse le torchon sous le bois."),
        ("narrateur", "La pomme quitte l'ombre, entre dans le bol."),
        ("narrateur", "Un espace reste, assez pour un doigt."),
        ("papa", "L'abri n'a pas mangé le toit."),
        ("narrateur", "La feuille a de l'ombre, et de l'air."),
        ("enfant-f", "Dépôt tabouret."),
        ("narrateur", "Le bus se gare à côté, sans serrer."),
    ),
    (2, 3, 2): L(
        ("enfant-m", "On attend, je me gare au fond, tout au noir."),
        ("narrateur", "Sous le tabouret, c'est frais, un peu trop sombre."),
        ("enfant-f", "J'ai peur pour la feuille, on ne la voit plus."),
        ("narrateur", "Raphaël s'arrête à mi-chemin, dans une bande claire."),
        ("enfant-m", "Dépôt à l'entrée, alors."),
        ("narrateur", "Ils attendent que leurs yeux s'habituent."),
        ("narrateur", "Deux doigts, et la pomme rentre dans le bol."),
        ("maman", "Tu as entendu qu'elle avait peur, et tu as reculé."),
        ("narrateur", "La feuille reparaît, dans la bande de soleil."),
        ("narrateur", "Le bus rouge reste à l'entrée, pas au fond."),
    ),
    (2, 3, 3): L(
        ("enfant-m", "On invente un abri pour les passagers, pas pour le bois."),
        ("narrateur", "Ils glissent le bol sous le tabouret, ensemble."),
        ("narrateur", "Le bus se gare à côté, comme un chien sage."),
        ("enfant-f", "Toit pour les pommes."),
        ("narrateur", "Personne ne touche les pieds, et le bois reste droit."),
        ("narrateur", "La pomme entre dans le bol, sous le toit."),
        ("papa", "Vous avez logé le fruit, pas coincé le jouet."),
        ("narrateur", "Une miette, dernier passager, attend près d'une roue."),
        ("narrateur", "La cuillère-capitaine a son box, à l'ombre."),
        ("narrateur", "La feuille ne touche plus le carrelage."),
    ),
    (3, 1, 1): L(
        ("enfant-f", "Je ramasse, et toi tu surveilles la flaque."),
        ("narrateur", "Raphaël se met en travers, comme un barrage."),
        ("narrateur", "La voiture arrive, et la rondelle du capot veut fuir."),
        ("enfant-f", "Doigt !"),
        ("narrateur", "Elle freine avec un doigt, sur le métal."),
        ("narrateur", "Mila glisse le torchon sous la pomme, hors du jus."),
        ("narrateur", "Le fruit s'arrête au bord du carré sec, puis au bol."),
        ("papa", "Le barrage a tenu, et le doigt aussi."),
        ("narrateur", "La feuille descend sur une assiette sèche."),
        ("narrateur", "La cuillère-capitaine garde le capot, toc."),
    ),
    (3, 1, 2): L(
        ("enfant-m", "On attend. Je me gare contre la planche."),
        ("narrateur", "Le couteau de papa reste trop près."),
        ("enfant-f", "Papa, tu poses le couteau plus loin ?"),
        ("papa", "Oui, merci de l'avoir vu."),
        ("narrateur", "La lame part, et Raphaël avance, plus sûr."),
        ("narrateur", "Ils attendent que la flaque cesse de bouger."),
        ("narrateur", "Deux doigts, et la pomme quitte le jus."),
        ("narrateur", "Le capot touche le bois, sans la flaque."),
        ("maman", "Vous avez demandé, et la route s'est ouverte."),
        ("narrateur", "La tarte peut attendre, le garage est pris."),
    ),
    (3, 1, 3): L(
        ("enfant-m", "On invente deux serviettes, un vrai garage."),
        ("narrateur", "Ils plient le linge, l'un à gauche, l'autre à droite."),
        ("narrateur", "La voiture entre dans le couloir de tissu."),
        ("enfant-f", "Portes !"),
        ("narrateur", "Les serviettes se referment, tout contre les roues."),
        ("narrateur", "La pomme a son box, près du sel, dans le bol."),
        ("maman", "Un pépin reste au milieu, comme une lampe."),
        ("narrateur", "La feuille a son box, près du sel."),
        ("narrateur", "La cuillère-capitaine disparaît entre les plis, un peu."),
        ("narrateur", "Le jus n'entre plus."),
    ),
    (3, 2, 1): L(
        ("enfant-f", "Je ramasse dans le carré, et le métal chauffe."),
        ("narrateur", "La rondelle du capot se colle, un peu molle."),
        ("enfant-m", "Elle est coincée !"),
        ("enfant-f", "Le torchon, sous la pomme, pas sur le verre."),
        ("narrateur", "Mila glisse le tissu, et le fruit se libère."),
        ("narrateur", "Ils restent, et un fil de jus perle, puis s'arrête."),
        ("narrateur", "La pomme rentre dans le bol, dans le carré chaud."),
        ("papa", "Vous n'avez pas gratté, et le fruit est resté entier."),
        ("narrateur", "Le carré de soleil contient enfin le jouet."),
        ("narrateur", "La cuillère-capitaine brille, moins froide."),
    ),
    (3, 2, 2): L(
        ("enfant-m", "On attend. Je montre le marché, sans coller le verre."),
        ("narrateur", "Il pousse jusqu'au début de la route de buée."),
        ("narrateur", "Ses doigts veulent plaquer, par habitude."),
        ("enfant-f", "La route, pas la vitre."),
        ("narrateur", "Il s'arrête sur le carrelage, dans le carré."),
        ("narrateur", "Ils attendent que la goutte du haut ait fini de tomber."),
        ("narrateur", "Deux doigts, et la pomme quitte la vitre."),
        ("narrateur", "Mila allonge la route d'un trait, jusqu'aux roues."),
        ("maman", "Le marché nous voit, et le verre reste net."),
        ("narrateur", "Une caisse, dehors, claque, loin."),
    ),
    (3, 2, 3): L(
        ("enfant-m", "On invente : toi la route, moi le carré."),
        ("enfant-f", "Et la feuille, au milieu."),
        ("narrateur", "Ils poussent ensemble, et la voiture entre dans le soleil."),
        ("narrateur", "Rien d'autre n'y tient : pas d'assiette, pas de bol."),
        ("narrateur", "Alors ils posent le bol juste à côté, dans l'ombre."),
        ("narrateur", "La pomme passe du verre au bol, ticket de soleil."),
        ("papa", "Le carré du matin a trouvé son auto."),
        ("narrateur", "La feuille pose son chapeau, comme un ticket."),
        ("maman", "Le fil de vapeur, derrière, a cessé de bouger."),
        ("narrateur", "La cuillère-capitaine garde le volant, toc."),
    ),
    (3, 3, 1): L(
        ("enfant-f", "Je ramasse en bas, et toi tu reçois."),
        ("narrateur", "Mila lâche la voiture, très lentement."),
        ("narrateur", "La voiture roule, et Raphaël ouvre les paumes."),
        ("narrateur", "Elle arrive dans ses mains, sans sauter."),
        ("enfant-m", "Arrivée."),
        ("narrateur", "Mila glisse le torchon sous la pomme, près du pied."),
        ("narrateur", "Le fruit rentre dans le bol, au sol."),
        ("papa", "La montagne a cessé d'être un tremplin."),
        ("narrateur", "Le torchon rayé, en bas, garde un pépin."),
        ("enfant-f", "Garage rampe."),
    ),
    (3, 3, 2): L(
        ("enfant-m", "On attend. Je redescends, plus fort, pour rattraper le temps."),
        ("narrateur", "La voiture décolle un peu, et Mila étale le torchon."),
        ("narrateur", "Le tissu rayé fait coussin, et le jouet s'y enfonce."),
        ("enfant-f", "Tu vas trop vite, même avec le livre."),
        ("narrateur", "Ils restent, le temps que le bois se taise."),
        ("narrateur", "Raphaël pose le bol à côté, sans le lancer."),
        ("narrateur", "Deux doigts, et la pomme quitte le pied du tabouret."),
        ("maman", "Le coussin a pris le choc, pas la pomme."),
        ("narrateur", "Le torchon garde la forme du capot, un moment."),
        ("narrateur", "La feuille n'a pas sauté."),
    ),
    (3, 3, 3): L(
        ("enfant-m", "On invente : toi un pied, moi l'autre, pour qu'il ne marche pas."),
        ("narrateur", "Chacun tient un pied du tabouret."),
        ("narrateur", "La voiture descend au milieu, sans que le bois voyage."),
        ("enfant-f", "On lâche ensemble."),
        ("enfant-m", "Un, deux, trois."),
        ("narrateur", "Ils ouvrent les mains, et le tabouret reste."),
        ("narrateur", "La pomme, au milieu, entre dans le bol."),
        ("papa", "Vous avez tenu la montagne, pas la voiture."),
        ("narrateur", "La feuille n'a pas bougé d'un pouce."),
        ("narrateur", "La cuillère-capitaine arrive au milieu, enfin."),
    ),
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    return {
        (1, 1, 1): L(
            ("narrateur", "Mila pose la pomme à feuille dans son assiette."),
            ("narrateur", "La feuille fait un bateau, au milieu d'une rondelle."),
            ("enfant-m", "C'est pour toi, je t'ai vue, d'abord."),
            ("enfant-f", "Merci, elle a voyagé dans le wagon de tête."),
            ("papa", "La tarte peut prendre les autres, plus tard."),
            ("maman", "Le fil de vapeur fait danser la feuille, un peu."),
            ("narrateur", "Le train dort contre le bol jaune, vide."),
            ("narrateur", "La cuillère-capitaine garde l'entaille tournée vers le quai."),
            ("narrateur", "Dehors, le marché a fini de plier ses caisses."),
        ),
        (1, 1, 2): L(
            ("narrateur", "Raphaël coupe la feuille, et la pose près du sel."),
            ("enfant-f", "Elle a tenu, même quand l'assiette a tinté."),
            ("enfant-m", "On croque, ça pique un peu, sucré."),
            ("maman", "Il reste une rondelle au fond, pour demain matin."),
            ("papa", "Merci d'avoir compté les carreaux."),
            ("narrateur", "Un clic lointain reste sous la table, puis plus rien."),
            ("narrateur", "Le bol jaune est chaud, vide, près des assiettes."),
            ("narrateur", "La casserole n'envoie plus qu'un souffle court."),
        ),
        (1, 1, 3): L(
            ("narrateur", "Ils croquent la même rondelle, chacun un bord."),
            ("enfant-f", "Tes mains et mes mains, sur le jus."),
            ("enfant-m", "Deux traces, une pomme."),
            ("papa", "Vous avez poussé au même nombre, jusqu'au bout."),
            ("maman", "Je rince le torchon rayé, il sent le fruit."),
            ("narrateur", "Quatre petites empreintes collent au bois."),
            ("narrateur", "Le train s'est calé entre le sel et le bol."),
            ("narrateur", "Dehors, plus aucune caisse ne parle."),
        ),
        (1, 2, 1): L(
            ("narrateur", "La feuille se colle une seconde à la vitre, puis tombe."),
            ("enfant-f", "Elle a vu le marché, par le rond."),
            ("enfant-m", "Je n'ai plus essuyé, et c'était dur."),
            ("maman", "Le rond est toujours là, un peu plus large."),
            ("papa", "Une dernière caisse se ferme, de l'autre côté."),
            ("narrateur", "Ils mangent près du rebord, sans toucher la buée."),
            ("narrateur", "Le train rentre sous le rebord, à l'ombre."),
            ("narrateur", "Le gravier, dehors, ne sonne plus."),
        ),
        (1, 2, 2): L(
            ("narrateur", "Le train s'endort dans le carré de soleil, sur les carreaux."),
            ("enfant-m", "La feuille a eu trop chaud, puis l'ombre."),
            ("enfant-f", "Ma main sent le wagon, un peu chaude."),
            ("papa", "Le soleil a bougé, et votre gare a suivi."),
            ("maman", "Il reste une rondelle tiède, pour chacun."),
            ("narrateur", "Ils croquent, et le jus court jusqu'au poignet."),
            ("narrateur", "Le rond de buée s'est élargi, comme une fenêtre."),
            ("narrateur", "La casserole, derrière, ne fume plus."),
        ),
        (1, 2, 3): L(
            ("narrateur", "Deux ronds de buée restent, deux nez, côte à côte."),
            ("enfant-m", "On a livré par les deux gares."),
            ("enfant-f", "La feuille sèche sur le rebord, toute plate."),
            ("maman", "Vous n'avez rien frotté, et le marché s'est montré."),
            ("papa", "Une rondelle chacun, et la tarte plus tard."),
            ("narrateur", "Ils mangent le nez contre le verre, sans l'embuer trop."),
            ("narrateur", "Le train dort entre les deux ronds, invisible d'en bas."),
            ("narrateur", "Les chaussettes de Raphaël ont séché, enfin."),
        ),
        (1, 3, 1): L(
            ("narrateur", "Sous le tabouret, le train est une grotte vide."),
            ("enfant-f", "J'étais le toit, tu étais le pied."),
            ("enfant-m", "Mon poignet est content, maintenant."),
            ("papa", "Le bois a gardé un petit anneau mouillé."),
            ("maman", "La pomme à feuille, on la partage ici, au sol."),
            ("narrateur", "Ils s'assoient sous le siège, comme dans une cabane."),
            ("narrateur", "Ça sent le bois clair et le fruit."),
            ("narrateur", "Le couvercle de la casserole ne danse plus."),
        ),
        (1, 3, 2): L(
            ("narrateur", "La feuille oubliée est un chapeau, sur le tabouret."),
            ("enfant-m", "Je voulais la montagne, mais le tunnel était mieux."),
            ("enfant-f", "Le livre a calé, et on croque."),
            ("maman", "Papa reprend le livre, tout collant de jus."),
            ("papa", "Merci, il me servira pour la tarte."),
            ("narrateur", "Un craquement, très petit, puis le silence du bois."),
            ("narrateur", "Le bol jaune reste au sol, près d'une chaussette humide."),
            ("narrateur", "Le marché, dehors, a rangé jusqu'à la dernière caisse."),
        ),
        (1, 3, 3): L(
            ("narrateur", "Ils s'assoient tous les deux sur le tabouret."),
            ("narrateur", "Il tient, et le pont a refermé."),
            ("enfant-f", "On a levé, on a reposé, on mange."),
            ("enfant-m", "La feuille a traversé l'ombre."),
            ("maman", "Une rondelle pour le haut, une pour le bas."),
            ("papa", "Le dernier wagon est passé, et le bois s'est tu."),
            ("narrateur", "Le fil de vapeur n'est plus qu'une odeur."),
            ("narrateur", "Le train, au sol, garde un clic dans une roue."),
        ),
        (2, 1, 1): L(
            ("narrateur", "Mila croque d'abord, invitée du guichet."),
            ("enfant-m", "Le ticket, c'était la miette, il n'y en a plus."),
            ("enfant-f", "Merci pour le siège propre."),
            ("maman", "Le torchon rayé, plié, sent la pomme et la miette."),
            ("papa", "Le bus rouge reste près du sel, portes ouvertes."),
            ("narrateur", "Ils vident le bol, tasse après tasse, pour de faux."),
            ("narrateur", "Une rondelle reste collée au guichet, puis part."),
            ("narrateur", "Dehors, plus aucun vrai bus ne souffle."),
        ),
        (2, 1, 2): L(
            ("narrateur", "Raphaël tend la dernière rondelle, celle de la fuite."),
            ("enfant-f", "Tu l'as remise, on la partage."),
            ("enfant-m", "Une par une, c'était plus long, et mieux."),
            ("papa", "Le sel a gardé une trace de jus, tout étroite."),
            ("maman", "Je lave la cuillère qui avait attrapé le fruit."),
            ("narrateur", "Le bus rouge se gare contre les assiettes, vide."),
            ("narrateur", "La pomme à feuille n'est plus qu'un goût, et une tige."),
            ("narrateur", "Le panier mouillé, près de la porte, a séché."),
        ),
        (2, 1, 3): L(
            ("narrateur", "Deux doigts ont poinçonné, il reste un trou de miette."),
            ("enfant-f", "Mon poinçon, ton poinçon."),
            ("enfant-m", "La feuille a payé, et on croque."),
            ("maman", "Les deux tasses gardent une goutte, chacune."),
            ("papa", "Un seul ticket, deux conducteurs."),
            ("narrateur", "Ils boivent un peu d'eau, comme après un vrai trajet."),
            ("narrateur", "Le bol jaune brille, vide, entre les tasses."),
            ("narrateur", "Le couteau de papa s'est tu, sur le bois."),
        ),
        (2, 2, 1): L(
            ("narrateur", "Le ticket de buée a coulé en virgule, loin du point."),
            ("enfant-f", "J'ai mené au rythme du grand, même parti."),
            ("enfant-m", "J'ai failli pousser par-dessus, alors j'ai retiré."),
            ("papa", "Votre arrêt est resté un trait, pas une tache."),
            ("maman", "Une rondelle chacun, le nez vers le village."),
            ("narrateur", "Ils mangent, et le verre rend le goût un peu froid."),
            ("narrateur", "Le bus rouge dort dans son trait, trop petit pour le vrai."),
            ("narrateur", "Le gravier ne parle plus, sous la fenêtre."),
        ),
        (2, 2, 2): L(
            ("narrateur", "Raphaël a laissé un siège dessiné, sur le verre."),
            ("enfant-m", "Mon klaxon était trop fort, celui-là est silencieux."),
            ("enfant-f", "Le grand a tourné, on peut croquer."),
            ("maman", "Le village n'a pas entendu la honte, seulement le calme."),
            ("papa", "Une rondelle pour le petit bus, une pour vous."),
            ("narrateur", "Le trait de buée s'efface par le bas, lentement."),
            ("narrateur", "Le bus rouge reste, lui, bien réel, près du rebord."),
            ("narrateur", "La vapeur de la casserole a rejoint la buée, puis plus rien."),
        ),
        (2, 2, 3): L(
            ("narrateur", "Deux tickets de buée pâlissent ensemble, rectangle contre rectangle."),
            ("enfant-m", "Le mien était pour la feuille."),
            ("enfant-f", "Le mien pour les rondelles, on a tout livré."),
            ("papa", "Le grand bus n'est plus qu'un point, au bout de la rue."),
            ("maman", "Vous avez chacun votre place, et le même goût."),
            ("narrateur", "Ils croquent, épaule contre épaule, face au verre."),
            ("narrateur", "Les rectangles gouttent, et deviennent deux larmes claires."),
            ("narrateur", "Le torchon rayé, sur la chaise, a cessé de pendre de travers."),
        ),
        (2, 3, 1): L(
            ("narrateur", "Le tabouret penche un peu, fier, comme un poteau d'arrêt."),
            ("enfant-f", "Dépôt, j'ai rangé sans serrer."),
            ("enfant-m", "Mes bras ne tremblent plus."),
            ("papa", "Un doigt d'air est resté, entre le bois et le toit."),
            ("maman", "On partage sous l'abri, assis par terre."),
            ("narrateur", "La pomme à feuille a l'ombre, et ils ont le sucré."),
            ("narrateur", "Le bus rouge garde une miette près d'une roue, oubliée."),
            ("narrateur", "Le fil blanc, au-dessus de la casserole, s'est cassé."),
        ),
        (2, 3, 2): L(
            ("narrateur", "Sous le tabouret, le dépôt reste frais, un peu noir."),
            ("enfant-m", "J'ai reculé, pour que tu voies la feuille."),
            ("enfant-f", "Elle est là, dans la bande de soleil, on la mange."),
            ("maman", "Tu as entendu la peur, et tu as changé de place."),
            ("papa", "Une rondelle dans le clair, une dans l'ombre, pour jouer."),
            ("narrateur", "Ils croquent à la frontière, un pied au soleil."),
            ("narrateur", "Le bus rouge reste à l'entrée, pas au fond."),
            ("narrateur", "Les chaussettes humides ont fait deux taches, qui séchent."),
        ),
        (2, 3, 3): L(
            ("narrateur", "Le bol vide garde l'ombre du tabouret, comme un toit."),
            ("enfant-f", "Abri pour les pommes, le bus à côté, sage."),
            ("enfant-m", "La miette, dernier passager, on la laisse ?"),
            ("papa", "On la met à la terre, demain, près du jardin."),
            ("maman", "Vous croquez le reste, ici, maintenant."),
            ("narrateur", "Ils mangent, et le bois au-dessus sent le clair."),
            ("narrateur", "Personne n'a touché les pieds, et l'abri tient."),
            ("narrateur", "Le panier de Mila, près de la porte, est vide aussi."),
        ),
        (3, 1, 1): L(
            ("narrateur", "Le capot n'est plus froid, un fil de jus y sèche."),
            ("enfant-f", "Mon doigt a freiné, et ta palme a fait barrage."),
            ("enfant-m", "La feuille a eu l'assiette sèche."),
            ("papa", "La flaque est restée de l'autre côté, seule."),
            ("maman", "Une rondelle pour le garage, une pour les conducteurs."),
            ("narrateur", "Ils croquent, ça craque, près du sel."),
            ("narrateur", "La petite voiture brille moins, enfin posée."),
            ("narrateur", "Le torchon rayé, replié, a une tache en forme de capot."),
        ),
        (3, 1, 2): L(
            ("narrateur", "Le couteau de papa dort loin du quai, cette fois."),
            ("enfant-m", "J'ai demandé, et la lame est partie."),
            ("enfant-f", "On peut croquer sans regarder le fer."),
            ("papa", "Merci de l'avoir vue, la lame, la tarte attendra."),
            ("maman", "Le carré sec a gardé deux pépins, comme des phares."),
            ("narrateur", "Ils mangent, et la planche ne suinte plus."),
            ("narrateur", "La voiture reste contre le bois, garage improvisé."),
            ("narrateur", "Le fil de vapeur a cessé d'écrire au plafond."),
        ),
        (3, 1, 3): L(
            ("narrateur", "Les deux serviettes gardent un pépin, lampe du box."),
            ("enfant-m", "Portes fermées, on ouvre pour manger."),
            ("enfant-f", "La feuille a eu son box, près du sel."),
            ("maman", "Je reprendrai le linge, il sent le fruit, maintenant."),
            ("papa", "Un garage de tissu, et une tarte plus tard."),
            ("narrateur", "Ils croquent à même le bol, assis sur les chaises."),
            ("narrateur", "La petite voiture disparaît entre les plis."),
            ("narrateur", "Dehors, le marché n'a plus de voix."),
        ),
        (3, 2, 1): L(
            ("narrateur", "Le métal a pris le soleil, tiède comme une joue."),
            ("enfant-f", "On n'a pas gratté, elle s'est décrochée toute seule."),
            ("enfant-m", "Le carré nous a gardés."),
            ("papa", "Le fruit est entier, et le jus a perlé, puis séché."),
            ("maman", "Une rondelle chacun, dans la lumière du carreau."),
            ("narrateur", "Ils mangent, et le verre leur renvoie les joues roses."),
            ("narrateur", "La voiture tient tout le carré, et rien d'autre."),
            ("narrateur", "Une caisse, au loin, a fini de claquer."),
        ),
        (3, 2, 2): L(
            ("narrateur", "Une route de buée reste, avec une auto dessinée au bout."),
            ("enfant-m", "J'ai voulu coller, puis j'ai posé sur le carreau."),
            ("enfant-f", "Ma route a rejoint tes roues, on croque."),
            ("maman", "Le verre est net, et le marché nous a vus, un peu."),
            ("papa", "Une rondelle pour la route, une pour la maison."),
            ("narrateur", "Ils mangent près du carré, sans remettre le jouet au verre."),
            ("narrateur", "La petite voiture garde une goutte sèche, sur le capot."),
            ("narrateur", "Les chaussettes de Raphaël ne laissent plus de marque."),
        ),
        (3, 2, 3): L(
            ("narrateur", "Le carré de soleil n'a plus que la petite voiture, et l'odeur."),
            ("enfant-m", "Toi la route, moi le carré, la feuille au milieu."),
            ("enfant-f", "Ticket de soleil, on l'a mangé."),
            ("papa", "Le fil de vapeur, derrière, ne bouge plus."),
            ("maman", "Il reste une rondelle froide, pour plus tard, sur le torchon."),
            ("narrateur", "Ils s'allongent un peu, joues au carrelage chaud."),
            ("narrateur", "Le marché, par la vitre, n'est plus qu'une rue vide."),
            ("narrateur", "La feuille, collée au torchon, fait un petit chapeau."),
        ),
        (3, 3, 1): L(
            ("narrateur", "En bas de la rampe, le torchon rayé garde un pépin."),
            ("enfant-f", "Je t'ai envoyé la voiture, et tu l'as reçue."),
            ("enfant-m", "Mes paumes sentent le métal, moins froid."),
            ("papa", "La montagne n'a pas été un tremplin, à la fin."),
            ("maman", "On croque ici, au sol, près du pied de bois."),
            ("narrateur", "Ils mangent, et le livre de recettes a une tache de jus."),
            ("narrateur", "La petite voiture reste dans les plis du torchon."),
            ("narrateur", "Le couvercle, là-haut, ne lâche plus de fil blanc."),
        ),
        (3, 3, 2): L(
            ("narrateur", "Le torchon-coussin garde la forme du capot, un moment."),
            ("enfant-m", "J'allais trop vite, et le tissu a pris le choc."),
            ("enfant-f", "La pomme, elle, n'a pas sauté."),
            ("maman", "Merci d'avoir posé le bol, après, sans le lancer."),
            ("papa", "Une rondelle pour le coussin, une pour les mains."),
            ("narrateur", "Ils croquent, et le rayé sent le fer et le fruit."),
            ("narrateur", "Le tabouret a cessé de danser, le livre sous le pied."),
            ("narrateur", "La tarte, plus tard, aura les rondelles qui restent."),
        ),
        (3, 3, 3): L(
            ("narrateur", "Chacun lâche un pied, et le tabouret ne voyage plus."),
            ("enfant-m", "Un, deux, trois, on a tenu la montagne."),
            ("enfant-f", "La feuille n'a pas bougé d'un pouce."),
            ("papa", "Vous avez gardé le bois, pas le jouet."),
            ("maman", "Une rondelle pour toi, une pour elle, ici, debout."),
            ("narrateur", "Ils mangent, une main près du pied, par habitude."),
            ("narrateur", "La petite voiture est au milieu, enfin arrivée."),
            ("narrateur", "Le gravier, dehors, a oublié les pas de Mila."),
        ),
    }[(a, b, c)]


T2_SONS = {1: "assiette", 2: "vitre", 3: "bois"}
T3_SONS = {1: "torchon", 2: "silence", 3: "mains"}
FIN_SONS = {1: "couverts,casserole", 2: "couverts,vitre", 3: "couverts,bois"}
VEH = {1: "train", 2: "bus", 3: "voiture"}


def path_ids(a: int, b: int, c: int) -> list[str]:
    t1 = f"CHK_T0001_P000{a}"
    t2id = f"{t1}_T0002_P000{b}"
    t3id = f"{t2id}_T0003_P000{c}"
    return [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        t1,
        f"{t1}_Q0001",
        f"{t1}_C0001",
        f"{t1}_T0002_P0000",
        t2id,
        f"{t2id}_T0003_P0000",
        t3id,
        f"{t3id}_F0001",
    ]


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "casserole,marche", "emphasis": "cuillère-capitaine"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Trois jouets attendent près du bol jaune."),
            ("narrateur", "Le train, le bus, ou la voiture."),
            ("maman", "Qu'est-ce que tu prends, Raphaël ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le train",
            "option_2_label": "le bus",
            "option_3_label": "la voiture",
        }},
    )

    for a, t1 in T1.items():
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(
            by_old[base], t1["passage"], "action",
            extra={"sons": t1["sons"], "emphasis": t1["name"], "note": t1["note"]},
        )
        by[f"{base}_Q0001"] = voice(
            by_old[f"{base}_Q0001"], t1["question"], "clue",
            extra={"sons": "", "emphasis": t1["emp"], "fields": {
                "expected_answer": t1["expected"],
                "accepted_examples": t1["accepted"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "C'est presque ça. Écoute l'indice.",
            }},
        )
        by[f"{base}_C0001"] = voice(
            by_old[f"{base}_C0001"], t1["confirm"], "confirm",
            extra={"sons": "", "emphasis": "Merci"},
        )
        by[f"{base}_T0002_P0000"] = voice(
            by_old[f"{base}_T0002_P0000"], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "la table",
                "option_2_label": "la fenêtre",
                "option_3_label": "le tabouret",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], t2(a, b), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": "pomme à feuille"},
            )
            t3q = f"{p2}_T0003_P0000"
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": "on ramasse",
                    "option_2_label": "on attend",
                    "option_3_label": "on invente",
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": "cuillère-capitaine" if c == 3 else "feuille"},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], ending(a, b, c), "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": "feuille"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")
    last_nars = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        nars = [ln.split("|", 1)[1] for ln in by[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        last_nars.append(nars[-1])
    if len(set(last_nars)) != 27:
        raise SystemExit(f"dernières images non distinctes: {len(set(last_nars))}/27")

    counts = [sum(words(by[i]["text"]) for i in path_ids(a, b, c))
              for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(counts) < 550 or max(counts) > 720:
        raise SystemExit(f"chemins hors cible 550-700: min={min(counts)} max={max(counts)}")

    tts_ok = all(
        c.get("text_xai_tags") and c.get("notes") and c.get("style_energy")
        for c in by.values()
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = (
        "Après le marché, Raphaël veut offrir à Mila la pomme à feuille "
        "avant que papa n'en fasse une tarte. La cuillère-capitaine, manche "
        "rouge et entaille, doit escorter le fruit sur le quai des casseroles. "
        "Le bol est trop lourd : la pomme roule. Train, bus ou voiture changent "
        "la première ruse (bonjour, s'il te plaît, merci) et l'endroit de la "
        "chute (wagons, chaise, livre). Table, fenêtre ou tabouret changent "
        "l'arrêt. Ramasser, attendre ou inventer changent le dernier geste. "
        "Chaque fin paie la feuille, le fil blanc, le torchon ou le gravier."
    )
    out["title"] = "Le voyage des pommes de Raphaël"
    out["characters"] = "Raphaël, Mila, papa, maman"
    out["setting"] = "cuisine, après le marché"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    low = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in TICS:
        if tic in low:
            raise SystemExit(f"tic global: {tic}")
    n_enc = len(re.findall(r"\bencore\b", low))
    n_dej = len(re.findall(r"\bdéjà\b", low))
    if n_enc > 0 or n_dej > 0:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-COL-001 — Le voyage des pommes de Raphaël\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / `option_*_next_chunk` inchangés. Pas d'apply.\n\n"
        "## Promesse narrative\n"
        "Après le marché, la casserole lâche un fil blanc. Sur le quai des "
        "casseroles, un bol jaune attend, une pomme porte sa feuille, une "
        "cuillère-capitaine (manche rouge, entaille, toc) doit escorter le "
        "fruit jusqu'à Mila **maintenant**, avant la tarte. Première idée : "
        "soulever le bol seul. Trop lourd, la feuille penche. T1 change le "
        "véhicule et la politesse qui débloque le départ (voir / demander / "
        "remercier) ; la pomme chute entre les wagons, sous la chaise ou "
        "contre le livre. T2 change l'arrêt (quai d'assiettes, gare de buée, "
        "tabouret-tunnel ou rampe). T3 change le dernier geste (ramasser, "
        "attendre, inventer). Chaque fin paie la feuille, la vapeur, le "
        "torchon, le gravier ou le carré de soleil.\n\n"
        "## Vécu\n"
        "- Désir : offrir la pomme à feuille, en voyage, avant la tarte.\n"
        "- Objet nommé : cuillère-capitaine, manche rouge, entaille, toc.\n"
        "- Lieu-coin : le quai des casseroles, entre la table et le feu.\n"
        "- Imprévu 1 : bol trop lourd ; Mila arrive ; la feuille penche.\n"
        "- Imprévu 2 (plus rusé) : assiettes-quai, buée essuyée, tabouret "
        "qui danse, vrai bus, flaque, vitre collée, rampe-tremplin.\n"
        "- COL.POL.001 vécu, pas récité : bonjour qui fait entrer Mila ; "
        "s'il te plaît qui libère le torchon ; merci qui ouvre la main de "
        "papa. Ailleurs, demander est un geste (couteau trop près, laisser "
        "le volant), pas un refrain.\n"
        "- Indice d'ouverture payé : fil blanc, feuille-chapeau, torchon "
        "rayé, gravier, chaussettes humides, toc de la cuillère.\n"
        "- Nuance : on attend pour parler, sauf si le tabouret va tomber "
        "ou si le couteau est trop près.\n\n"
        "## Vu et corrigé\n"
        f"- Titre noyau conservé. N2 ≤ 15. Troupe D16 : Raphaël, Mila, papa, maman.\n"
        f"- 86 nœuds, 27 chemins, 27 fins textuellement distinctes "
        f"(dernière image narrateur unique).\n"
        f"- Mots par chemin : {min(counts)}–{max(counts)}, moyenne {sum(counts)//27}.\n"
        "- Labels T1/T2/T3 source conservés (train/bus/voiture ; "
        "table/fenêtre/tabouret ; ramasse/attend/invente).\n"
        "- Questions concrètes : wagons / chaise / livre.\n"
        "- Un merci adulte vécu (T1), pas un refrain Bravo.\n"
        "- TTS par chunk (opening/choice/clue/confirm/action/obstacle/"
        "resolution/ending) : `text_ssml`, `text_xai_tags`, `notes`.\n"
        "- `text` / `script` synchronisés. Pas apply.\n"
        "- Tics « encore / déjà / tout doux / tout calme » absents.\n\n"
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
