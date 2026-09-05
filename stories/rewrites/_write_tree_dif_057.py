#!/usr/bin/env python3
"""TREE-DIF-057 — Le carillon de Sarah, au prunier (F-NAR-019, N3, DIF.BES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-057"
LIM = 16
TITLE = "Le carillon de Sarah, au prunier"
CHARS = "Sarah, Nino, papa, maman"
SETTING = "jardin : table, terrasse, prunier, rose, herbe"
TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "inviter sans forcer",
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_jardin_peut_chanter_si_nino_entend; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_a_pris; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
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
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=assembler_le_carillon_avant_le_vent; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=deception_legere; intensite=2; destinataire=enfant; sous_texte=nino_a_autre_chose_en_tete; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=proposer_sans_tirer; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=le_prunier_a_son_toc; tempo=pose; sourire=léger; respiration=ample",
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
    ("narrateur", "Derrière la maison, le prunier penche ses fruits mûrs."),
    ("narrateur", "Une prune tombe, et la terre sent le sucre."),
    ("narrateur", "Le fil à linge claque, bleu et blanc."),
    ("narrateur", "Sarah vit ici avec papa, maman, et Nino."),
    ("narrateur", "Un bocal vide brille près des sandales."),
    ("narrateur", "Un grelot dort dans la coupelle de pierre."),
    ("narrateur", "Un ruban bleu pend trop long, au vent."),
    ("papa", "La nappe est prête, sur la table du jardin."),
    ("maman", "Les pinces, je les range une par une."),
    ("narrateur", "En ce moment, Sarah frotte le verre du bocal."),
    ("enfant-f", "Nino, viens, le jardin va chanter !"),
    ("narrateur", "Sa voix part trop fort, trop vite."),
    ("narrateur", "Nino, plus loin, ne se tourne pas."),
    ("narrateur", "Le bocal glisse, et un toc plat frappe le bois."),
    ("enfant-f", "Il n'a pas entendu."),
    ("narrateur", "Sarah rattrape le verre, les joues chaudes."),
    ("papa", "Merci, tu l'as tenu à deux mains."),
    ("maman", "Le vent du soir va prendre le son."),
    ("enfant-f", "Je veux un carillon, pour lui, maintenant."),
)

T1 = {
    1: dict(
        name="le bocal",
        expected="bocal",
        accepted="bocal | le bocal | le verre | d'abord le bocal",
        retry="Sarah a pris le bocal.",
        ok="Oui, c'est le bocal.",
        sons="verre,table",
        emphasis="bocal",
        passage=L(
            ("narrateur", "Sarah pose le bocal sur la table chaude."),
            ("enfant-f", "Écoute, Nino, le verre chante !"),
            ("narrateur", "Elle tape trop fort : le toc fait peur."),
            ("narrateur", "Nino, vers la terrasse, hausse les épaules."),
            ("enfant-f", "Ce n'est pas le bon son."),
            ("maman", "Tiens-le contre le bois, plus lentement."),
            ("narrateur", "Sarah pose le verre, sans le brusquer."),
            ("narrateur", "Un toc creux répond, comme une petite cloche."),
            ("papa", "Le grelot et le ruban te suivent."),
            ("narrateur", "Elle glisse le grelot dans le col."),
            ("narrateur", "Maman noue le ruban autour du verre."),
            ("enfant-f", "Maintenant, je lui propose."),
            ("papa", "Tu lui proposes, quand tu le trouves ?"),
        ),
        question=L(
            ("narrateur", "Le verre tiède reste dans ses mains."),
            ("maman", "Elle a pris quoi, d'abord ?"),
        ),
        confirm=L(
            ("enfant-f", "Le bocal."),
            ("maman", "Oui, le verre."),
            ("narrateur", "Un toc creux dort contre le bois."),
            ("narrateur", "La table du jardin sent la nappe chaude."),
            ("enfant-f", "Nino est dehors, quelque part."),
            ("papa", "Je l'entends, vers la terrasse."),
            ("maman", "Vous allez le trouver."),
            ("enfant-f", "Je lui propose le carillon."),
        ),
        choice=L(
            ("narrateur", "Le bocal tinte contre la nappe."),
            ("narrateur", "Une craie jaune traîne sur la terrasse."),
            ("narrateur", "Une rose penche, lourde de chaleur."),
            ("narrateur", "Une sandale attend, dans l'herbe."),
            ("papa", "On va vers quoi, Sarah ?"),
        ),
    ),
    2: dict(
        name="le grelot",
        expected="grelot",
        accepted="grelot | le grelot | la clochette | d'abord le grelot",
        retry="Sarah a pris le grelot.",
        ok="Oui, c'est le grelot.",
        sons="grelot,pierre",
        emphasis="grelot",
        passage=L(
            ("narrateur", "Sarah prend le grelot, froid dans la paume."),
            ("enfant-f", "Il va courir jusqu'au prunier !"),
            ("narrateur", "Elle le secoue trop fort, sur la marche."),
            ("narrateur", "Nino se bouche une oreille, loin."),
            ("enfant-f", "Trop fort, pardon."),
            ("papa", "Secoue-le bas, près de la pierre."),
            ("narrateur", "Un tintement mince court sur la marche."),
            ("maman", "Le bocal aussi, près de toi."),
            ("narrateur", "Le ruban s'enroule autour de son poignet."),
            ("narrateur", "Les trois affaires restent ensemble."),
            ("enfant-f", "Nino va suivre le son, s'il veut."),
            ("papa", "Tu lui proposes, sans le tirer ?"),
            ("enfant-f", "Oui, papa."),
        ),
        question=L(
            ("narrateur", "Le petit fer tinte dans sa paume."),
            ("papa", "Elle a pris quoi, d'abord ?"),
        ),
        confirm=L(
            ("enfant-f", "Le grelot."),
            ("papa", "Oui, la petite cloche."),
            ("narrateur", "Le fer dort, froid, contre sa peau."),
            ("narrateur", "La marche garde un tintement mince."),
            ("enfant-f", "Nino est dehors, quelque part."),
            ("maman", "Je l'entends, vers la rose."),
            ("papa", "Le son a couru, pas trop fort."),
            ("enfant-f", "Je lui propose le grelot."),
        ),
        choice=L(
            ("narrateur", "Le grelot dort dans sa paume."),
            ("narrateur", "Une craie jaune traîne sur la terrasse."),
            ("narrateur", "Une rose penche, lourde de chaleur."),
            ("narrateur", "Une sandale attend, dans l'herbe."),
            ("maman", "On va vers quoi, Sarah ?"),
        ),
    ),
    3: dict(
        name="le ruban bleu",
        expected="ruban",
        accepted="ruban | le ruban | le ruban bleu | d'abord le ruban",
        retry="Sarah a pris le ruban.",
        ok="Oui, c'est le ruban.",
        sons="tissu,branche",
        emphasis="ruban",
        passage=L(
            ("narrateur", "Sarah prend le ruban bleu, un peu rêche."),
            ("enfant-f", "Il va tenir le carillon."),
            ("maman", "Noue une boucle, à la branche basse."),
            ("narrateur", "Elle noue trop vite : la boucle reste vide."),
            ("narrateur", "Nino ne lève pas les yeux."),
            ("enfant-f", "Sans son, il ne vient pas."),
            ("papa", "Le prunier penche, près de toi."),
            ("narrateur", "Le bocal et le grelot la rejoignent."),
            ("narrateur", "Rien ne reste près de la porte."),
            ("enfant-f", "Nino va voir ma boucle, s'il veut."),
            ("papa", "Tu lui proposes, sans le tirer ?"),
            ("enfant-f", "Oui."),
        ),
        question=L(
            ("narrateur", "Le bleu tremble entre ses doigts."),
            ("maman", "Elle a noué quoi ?"),
        ),
        confirm=L(
            ("enfant-f", "Le ruban."),
            ("maman", "Oui, la boucle bleue."),
            ("narrateur", "Une boucle pend à la branche basse."),
            ("narrateur", "Le prunier sent les prunes chaudes."),
            ("enfant-f", "Nino est dehors, quelque part."),
            ("papa", "Je l'entends, vers l'herbe."),
            ("maman", "La boucle attend, vide."),
            ("enfant-f", "Je lui propose la branche."),
        ),
        choice=L(
            ("narrateur", "Le ruban pend à la branche."),
            ("narrateur", "Une craie jaune traîne sur la terrasse."),
            ("narrateur", "Une rose penche, lourde de chaleur."),
            ("narrateur", "Une sandale attend, dans l'herbe."),
            ("papa", "On va vers quoi, Sarah ?"),
        ),
    ),
}


def t2_sun(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Sarah quitte la table, le bocal contre elle."),
            ("narrateur", "Nino dessine un soleil, absorbé."),
            ("enfant-f", "Nino, le carillon est prêt !"),
            ("narrateur", "Il ne lève pas le menton."),
            ("narrateur", "Un rayon de craie manque, sur la pierre."),
            ("copain", "Ce soleil, d'abord."),
            ("enfant-f", "Tu viens l'entendre, après ?"),
            ("narrateur", "Nino souffle sur la poussière jaune, sans répondre."),
            ("narrateur", "Sarah sent ses épaules tomber."),
            ("maman", "La craie tient sa poussière, elle."),
            ("papa", "Tu restes près de lui ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Sarah pose le grelot près de la craie."),
            ("narrateur", "Nino penche l'oreille, puis reprend le trait."),
            ("enfant-f", "Nino, ça tinte, minuscule."),
            ("narrateur", "Le dernier rayon n'est pas tiré."),
            ("copain", "Mon soleil n'est pas fini."),
            ("enfant-f", "Tu viens sur la marche ?"),
            ("copain", "Ce soleil, d'abord."),
            ("narrateur", "Sarah serre le fer, déçue un instant."),
            ("papa", "Il suit la poussière jaune, lui."),
            ("maman", "Tu restes près de lui ?"),
        )
    return L(
        ("narrateur", "Le ruban attend à la branche, noué et vide."),
        ("narrateur", "Sarah revient vers la terrasse, les pieds lourds."),
        ("enfant-f", "Nino, ma boucle est bleue."),
        ("narrateur", "Un rayon de craie manque, sur la pierre."),
        ("copain", "Il n'a pas son dernier trait."),
        ("enfant-f", "Tu viens sous le prunier ?"),
        ("copain", "Ce soleil, d'abord."),
        ("narrateur", "Sarah ouvre la bouche, puis la referme."),
        ("maman", "La craie n'a pas dit au revoir."),
        ("papa", "Tu restes près de lui ?"),
    )


def t2_bug(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Sarah laisse le bocal sur la table."),
            ("narrateur", "Nino suit une coccinelle, sur la rose."),
            ("enfant-f", "Nino, le verre va chanter."),
            ("copain", "Elle n'a pas volé."),
            ("enfant-f", "Tu viens au prunier ?"),
            ("copain", "La coccinelle, d'abord."),
            ("narrateur", "Une patte rouge hésite, puis se rassoit."),
            ("narrateur", "Sarah attend un mot, et rien ne vient."),
            ("maman", "Il écoute la rose, lui."),
            ("papa", "Tu fais quoi, alors ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Le grelot se tait dans son poing."),
            ("narrateur", "Nino est collé à la rose, le nez dedans."),
            ("enfant-f", "Nino, tu veux un son minuscule ?"),
            ("copain", "Elle n'a pas volé."),
            ("enfant-f", "On l'écoute, puis on part ?"),
            ("copain", "La coccinelle, d'abord."),
            ("narrateur", "Une aile tremble, puis se rassoit."),
            ("narrateur", "Sarah sent l'impatience lui piquer les doigts."),
            ("papa", "La rose n'a pas fini."),
            ("maman", "Tu fais quoi, alors ?"),
        )
    return L(
        ("narrateur", "Sarah quitte la branche, le ruban en place."),
        ("narrateur", "Nino respire contre la rose, jusqu'aux épaules."),
        ("enfant-f", "Nino, ma boucle t'attend."),
        ("copain", "Elle n'a pas volé."),
        ("enfant-f", "Tu viens sous le prunier ?"),
        ("copain", "La coccinelle, d'abord."),
        ("narrateur", "Une patte rouge reste collée, immobile."),
        ("narrateur", "Sarah baisse les yeux, un peu seule."),
        ("maman", "Il ne veut pas bouger."),
        ("papa", "Tu fais quoi, alors ?"),
    )


def t2_shoe(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Nino s'arrête au bord de l'herbe."),
            ("copain", "J'ai un pied nu, Sarah."),
            ("enfant-f", "Le bocal est sur la table."),
            ("narrateur", "Une sandale manque, sous les tiges."),
            ("enfant-f", "Tu viens au verre, après ?"),
            ("copain", "L'autre sandale, d'abord."),
            ("narrateur", "Il fouille, le front plissé."),
            ("narrateur", "Sarah tape du pied, puis s'arrête."),
            ("papa", "Le second n'est pas là."),
            ("maman", "Tu l'aides, ou tu attends ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Nino quitte la marche, un pied nu."),
            ("copain", "J'ai un pied nu, Sarah."),
            ("enfant-f", "Le grelot peut t'aider à chercher."),
            ("narrateur", "La sandale droite est chaude, seule."),
            ("enfant-f", "Tu reviens au son ?"),
            ("copain", "L'autre sandale, d'abord."),
            ("narrateur", "Il cherche, tendu, dans l'herbe haute."),
            ("narrateur", "Sarah serre le fer, prête à partir."),
            ("maman", "Le second n'est pas là."),
            ("papa", "Tu l'aides, ou tu attends ?"),
        )
    return L(
        ("narrateur", "Nino se tient sous le prunier, un pied nu."),
        ("copain", "J'ai un pied nu, Sarah."),
        ("enfant-f", "Ma boucle est nouée."),
        ("narrateur", "Il serre une sandale, le cuir chaud."),
        ("enfant-f", "Tu regardes la branche ?"),
        ("copain", "L'autre sandale, d'abord."),
        ("narrateur", "Il cherche, près des prunes tombées."),
        ("narrateur", "Sarah croise les bras, puis les desserre."),
        ("papa", "Le second n'est pas là."),
        ("maman", "Tu l'aides, ou tu attends ?"),
    )


T2_FN = {1: t2_sun, 2: t2_bug, 3: t2_shoe}
T2_SONS = {1: "craie", 2: "rose,insecte", 3: "herbe"}
T2_EMPH = {1: "soleil", 2: "coccinelle", 3: "sandale"}
T3_LABS = {
    1: ("attendre le soleil", "parler près de lui", "s'asseoir à côté"),
    2: ("attendre l'envol", "un grelot minuscule", "garder le carillon"),
    3: ("aider un peu", "un petit regard", "proposer plus tard"),
}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Le soleil de craie n'est pas fini."),
            ("papa", "Attendre, parler près, ou s'asseoir ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "La coccinelle n'est pas partie."),
            ("maman", "Attendre l'envol, un grelot, ou garder ?"),
        )
    return L(
        ("narrateur", "Une sandale n'est pas chaussée."),
        ("papa", "Aider, un petit regard, ou plus tard ?"),
    )


T3 = {
    (1, 1, 1): L(
        ("enfant-f", "J'attends le dernier trait."),
        ("copain", "Merci, le verre peut patienter."),
        ("narrateur", "Sarah pose le bocal comme un second soleil."),
        ("narrateur", "Elle compte les rayons sur la buée du verre."),
        ("narrateur", "La craie s'arrête, pile, contre le col."),
        ("copain", "Mon soleil a réveillé le tien."),
        ("enfant-f", "Tu viens, alors ?"),
        ("copain", "Oui, j'apporte la craie."),
        ("papa", "Tu as laissé le soleil finir."),
    ),
    (1, 1, 2): L(
        ("enfant-f", "Nino, le verre a une oreille."),
        ("narrateur", "Elle glisse le bocal contre le rayon manquant."),
        ("narrateur", "Sa voix reste un souffle, collée au bois."),
        ("copain", "Il écoute mon soleil, lui aussi ?"),
        ("enfant-f", "Oui, creux comme un trait."),
        ("copain", "Je viens, alors."),
        ("narrateur", "Il pose la craie dans l'ombre du verre."),
        ("papa", "Tu as parlé contre son dessin."),
        ("maman", "C'est lui qui a dit oui."),
    ),
    (1, 1, 3): L(
        ("enfant-f", "Je m'assois à côté."),
        ("narrateur", "Sarah s'assoit au pied de la table."),
        ("narrateur", "Le bocal tient chaud entre eux, sans bouger."),
        ("copain", "Tu vois le rayon, toi aussi ?"),
        ("enfant-f", "Oui, il pique un peu."),
        ("narrateur", "Un dernier trait les fait souffler ensemble."),
        ("copain", "On accroche, après ça."),
        ("papa", "Tu as écouté son soleil."),
        ("maman", "C'est lui qui a dit après."),
    ),
    (1, 2, 1): L(
        ("enfant-f", "J'attends l'envol."),
        ("copain", "Merci, la rose d'abord."),
        ("narrateur", "Sarah regarde la rose dans le verre du bocal."),
        ("narrateur", "La petite bête y marche, à l'envers."),
        ("narrateur", "Une aile s'ouvre, et l'image s'envole."),
        ("copain", "Elle a volé, là."),
        ("enfant-f", "Tu viens, alors ?"),
        ("copain", "Oui, je laisse la rose."),
        ("papa", "Tu as laissé la rose finir."),
    ),
    (1, 2, 2): L(
        ("enfant-f", "Un toc minuscule, pour elle ?"),
        ("narrateur", "Elle pose le bocal près de la tige, sans frotter."),
        ("copain", "Elle l'entend, la petite ?"),
        ("enfant-f", "Bas, oui."),
        ("narrateur", "Une aile se lève, puis se rassoit sur le col."),
        ("copain", "On va jusqu'au prunier, alors."),
        ("enfant-f", "D'accord."),
        ("papa", "Le son n'a pas chassé la rose."),
        ("maman", "Il a choisi le voyage."),
    ),
    (1, 2, 3): L(
        ("copain", "Pas maintenant, Sarah."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Elle serre le bocal, les épaules basses."),
        ("enfant-f", "J'accroche à la table, alors."),
        ("narrateur", "Un toc part vers la rose, loin, sans elle."),
        ("copain", "Je l'entends, d'ici !"),
        ("enfant-f", "Toi la rose, moi le verre."),
        ("papa", "Tu as gardé ton carillon."),
        ("maman", "La rose est restée à lui."),
    ),
    (1, 3, 1): L(
        ("enfant-f", "J'aide un peu."),
        ("narrateur", "Elle penche le bocal, et le verre éclaire l'ombre."),
        ("narrateur", "Une sandale chaude apparaît, collée au pied de table."),
        ("copain", "Elle s'était cachée sous le bois !"),
        ("enfant-f", "Près du bord, oui."),
        ("narrateur", "Deux pieds, à présent, bien chauds."),
        ("copain", "On peut accrocher, là."),
        ("papa", "Tu as cherché avec lui."),
        ("maman", "Le pied nu n'a plus froid."),
    ),
    (1, 3, 2): L(
        ("enfant-f", "Un petit regard, Nino ?"),
        ("copain", "Le temps d'un toc, alors."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Nino colle l'œil au verre, une seconde."),
        ("narrateur", "Le jardin y tremble, à l'envers."),
        ("copain", "Il chante, presque."),
        ("narrateur", "Il lâche le bocal, et reprend la sandale."),
        ("papa", "Tu as montré juste un peu."),
        ("maman", "Il a vu, puis choisi."),
    ),
    (1, 3, 3): L(
        ("enfant-f", "On accroche plus tard, alors ?"),
        ("copain", "Oui, plus tard, le pied d'abord."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Sarah pose le bocal au milieu de la nappe."),
        ("narrateur", "Nino serre la sandale, concentré."),
        ("copain", "Garde un toc pour moi."),
        ("enfant-f", "Il t'attend sur le bois."),
        ("papa", "Tu as dit une autre heure."),
        ("maman", "Le pied nu cherche, lui."),
    ),
    (2, 1, 1): L(
        ("enfant-f", "J'attends le dernier trait."),
        ("copain", "Merci, le grelot après le trait."),
        ("narrateur", "Sarah tient le fer, le doigt sur la languette."),
        ("narrateur", "Le grelot reste muet, sur la marche froide."),
        ("narrateur", "Nino tire le rayon, sans un tintement."),
        ("copain", "Il est fini, et ton fer n'a pas volé."),
        ("enfant-f", "Tu viens, alors ?"),
        ("copain", "Oui, j'apporte la craie."),
        ("papa", "Tu as gardé le son pour la fin."),
    ),
    (2, 1, 2): L(
        ("enfant-f", "Nino, un tintement pour le rayon ?"),
        ("narrateur", "Elle ouvre le poing, juste au-dessus du jaune."),
        ("narrateur", "Un son mince montre le trait qui manque."),
        ("copain", "Il m'a montré où tirer."),
        ("enfant-f", "Minuscule, comme un rayon."),
        ("copain", "Je viens, alors."),
        ("narrateur", "Il pose la craie contre le petit fer."),
        ("papa", "Le son a aidé le dessin, pas volé."),
        ("maman", "C'est lui qui a dit oui."),
    ),
    (2, 1, 3): L(
        ("enfant-f", "Je m'assois à côté."),
        ("narrateur", "Sarah s'assoit sur la marche de pierre."),
        ("narrateur", "Le grelot dort sur ses genoux, silencieux."),
        ("copain", "Ta cloche a chaud, là ?"),
        ("enfant-f", "Oui, elle attend ton trait."),
        ("narrateur", "Un dernier trait les fait souffler ensemble."),
        ("copain", "On accroche, après ça."),
        ("papa", "Tu as écouté son soleil."),
        ("maman", "C'est lui qui a dit après."),
    ),
    (2, 2, 1): L(
        ("enfant-f", "J'attends l'envol."),
        ("copain", "Merci, pas de son."),
        ("narrateur", "Sarah ferme le poing, le grelot prisonnier."),
        ("narrateur", "La rose n'entend que le souffle de Nino."),
        ("narrateur", "Une aile s'ouvre, et la petite part."),
        ("copain", "Elle a volé, sans peur."),
        ("enfant-f", "Tu viens, alors ?"),
        ("copain", "Oui, je laisse la rose."),
        ("papa", "Tu as laissé la rose finir."),
    ),
    (2, 2, 2): L(
        ("enfant-f", "Nino, un grelot minuscule ?"),
        ("narrateur", "Elle ouvre le poing, un son mince comme un fil."),
        ("copain", "Elle l'entend, la petite ?"),
        ("enfant-f", "Bas, oui."),
        ("narrateur", "Une aile se lève, puis se rassoit sur le fer."),
        ("copain", "On va jusqu'au prunier, alors."),
        ("enfant-f", "D'accord."),
        ("papa", "Le son n'a pas chassé la rose."),
        ("maman", "Il a choisi le voyage."),
    ),
    (2, 2, 3): L(
        ("copain", "Pas maintenant, Sarah."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Elle serre le grelot, les épaules basses."),
        ("enfant-f", "J'accroche à la marche, alors."),
        ("narrateur", "Un tintement part vers la rose, loin."),
        ("copain", "Je l'entends, d'ici !"),
        ("enfant-f", "Toi la rose, moi la pierre."),
        ("papa", "Tu as gardé ton carillon."),
        ("maman", "La rose est restée à lui."),
    ),
    (2, 3, 1): L(
        ("enfant-f", "J'aide un peu."),
        ("narrateur", "Elle fait tinter le grelot, près de l'herbe."),
        ("narrateur", "Le son montre une lanière, collée à la pierre."),
        ("copain", "Elle s'était cachée sous la marche !"),
        ("enfant-f", "Près du bord, oui."),
        ("narrateur", "Deux pieds, à présent, bien chauds."),
        ("copain", "On peut accrocher, là."),
        ("papa", "Tu as cherché avec lui."),
        ("maman", "Le pied nu n'a plus froid."),
    ),
    (2, 3, 2): L(
        ("enfant-f", "Un petit regard, Nino ?"),
        ("copain", "Le temps d'un tintement, alors."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Sarah pose le grelot dans sa paume ouverte."),
        ("narrateur", "Nino le touche du doigt, et le fer dit toc."),
        ("copain", "Assez, je l'ai entendu."),
        ("narrateur", "Il referme la main de Sarah, puis cherche."),
        ("papa", "Tu as montré juste un peu."),
        ("maman", "Il a vu, puis choisi."),
    ),
    (2, 3, 3): L(
        ("enfant-f", "On accroche plus tard, alors ?"),
        ("copain", "Oui, plus tard, le pied d'abord."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Sarah pose le grelot au bord de la marche."),
        ("narrateur", "Nino serre la sandale, concentré."),
        ("copain", "Garde un tintement pour moi."),
        ("enfant-f", "Il t'attend sur la pierre."),
        ("papa", "Tu as dit une autre heure."),
        ("maman", "Le pied nu cherche, lui."),
    ),
    (3, 1, 1): L(
        ("enfant-f", "J'attends le dernier trait."),
        ("copain", "Merci, ta boucle après."),
        ("narrateur", "Sarah enroule le ruban autour d'un doigt."),
        ("narrateur", "Chaque tour compte un rayon, sans tirer Nino."),
        ("narrateur", "La craie s'arrête, et le bleu se desserre."),
        ("copain", "Mon soleil est rond, comme ta boucle."),
        ("enfant-f", "Tu viens, alors ?"),
        ("copain", "Oui, j'apporte la craie."),
        ("papa", "Tu as laissé le soleil finir."),
    ),
    (3, 1, 2): L(
        ("enfant-f", "Nino, la boucle t'écoute, de loin."),
        ("narrateur", "Elle montre le bleu, sans quitter la terrasse."),
        ("narrateur", "Sa voix reste un souffle, collée à la craie."),
        ("copain", "Elle a une oreille, la branche ?"),
        ("enfant-f", "Oui, bleue comme le ciel."),
        ("copain", "Je viens, alors."),
        ("narrateur", "Il pose la craie, et suit le ruban des yeux."),
        ("papa", "Tu as parlé contre son dessin."),
        ("maman", "C'est lui qui a dit oui."),
    ),
    (3, 1, 3): L(
        ("enfant-f", "Je m'assois à côté."),
        ("narrateur", "Sarah s'assoit dans l'herbe, sous la branche."),
        ("narrateur", "Le ruban lui fait un bracelet, un peu rêche."),
        ("copain", "Tu vois le rayon, toi aussi ?"),
        ("enfant-f", "Oui, il pique un peu."),
        ("narrateur", "Un dernier trait les fait souffler ensemble."),
        ("copain", "On accroche, après ça."),
        ("papa", "Tu as écouté son soleil."),
        ("maman", "C'est lui qui a dit après."),
    ),
    (3, 2, 1): L(
        ("enfant-f", "J'attends l'envol."),
        ("copain", "Merci, pas de boucle trop près."),
        ("narrateur", "Sarah laisse le ruban à la branche, loin de la rose."),
        ("narrateur", "La petite bête n'a que le souffle de Nino."),
        ("narrateur", "Une aile s'ouvre, et l'hôte quitte la fleur."),
        ("copain", "Elle a volé, là."),
        ("enfant-f", "Tu viens, alors ?"),
        ("copain", "Oui, je laisse la rose."),
        ("papa", "Tu as laissé la rose finir."),
    ),
    (3, 2, 2): L(
        ("enfant-f", "Nino, un bleu minuscule ?"),
        ("narrateur", "Elle agite le ruban, une seconde seulement."),
        ("copain", "Elle l'entend, la petite ?"),
        ("enfant-f", "Bas, oui."),
        ("narrateur", "Une aile se lève, puis se rassoit sur le bleu."),
        ("copain", "On va jusqu'au prunier, alors."),
        ("enfant-f", "D'accord."),
        ("papa", "Le tissu n'a pas chassé la rose."),
        ("maman", "Il a choisi le voyage."),
    ),
    (3, 2, 3): L(
        ("copain", "Pas maintenant, Sarah."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Elle serre le ruban, les épaules basses."),
        ("enfant-f", "J'accroche à la branche, alors."),
        ("narrateur", "Un battement bleu part vers la rose, loin."),
        ("copain", "Je l'entends, d'ici !"),
        ("enfant-f", "Toi la rose, moi le nœud."),
        ("papa", "Tu as gardé ton carillon."),
        ("maman", "La rose est restée à lui."),
    ),
    (3, 3, 1): L(
        ("enfant-f", "J'aide un peu."),
        ("narrateur", "Elle plante le ruban comme un drapeau, sous les prunes."),
        ("narrateur", "Une sandale chaude apparaît, collée aux fruits."),
        ("copain", "Elle s'était cachée sous le prunier !"),
        ("enfant-f", "Près du bord, oui."),
        ("narrateur", "Deux pieds, à présent, bien chauds."),
        ("copain", "On peut accrocher, là."),
        ("papa", "Tu as cherché avec lui."),
        ("maman", "Le pied nu n'a plus froid."),
    ),
    (3, 3, 2): L(
        ("enfant-f", "Un petit regard, Nino ?"),
        ("copain", "Le temps d'un bleu, alors."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Nino lève les yeux vers la boucle, une seconde."),
        ("narrateur", "Le ruban bat, puis se tait."),
        ("copain", "J'ai vu, je cherche."),
        ("narrateur", "Il baisse la tête, et fouille l'herbe à nouveau."),
        ("papa", "Tu as montré juste un peu."),
        ("maman", "Il a vu, puis choisi."),
    ),
    (3, 3, 3): L(
        ("enfant-f", "On accroche plus tard, alors ?"),
        ("copain", "Oui, plus tard, le pied d'abord."),
        ("enfant-f", "D'accord."),
        ("narrateur", "Sarah laisse la boucle vide, à la branche."),
        ("narrateur", "Nino serre la sandale, concentré."),
        ("copain", "Garde un bleu pour moi."),
        ("enfant-f", "Il t'attend à la branche."),
        ("papa", "Tu as dit une autre heure."),
        ("maman", "Le pied nu cherche, lui."),
    ),
}

FIN = {
    (1, 1, 1): L(
        ("narrateur", "Le soleil de craie chauffe le bois de la table."),
        ("copain", "Il a son dernier trait, Sarah."),
        ("enfant-f", "Oui, bien jaune."),
        ("papa", "La craie a laissé la place."),
        ("maman", "Le prunier fait un petit toc."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino noue le grelot, les doigts tâchés de jaune."),
        ("enfant-f", "Le jardin chante, là."),
        ("narrateur", "La poussière jaune dort sur les genoux de Nino."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Le carillon collé écoute, un peu, près du trait."),
        ("enfant-f", "Il t'a attendu, bas."),
        ("copain", "J'ai dit oui, près de toi."),
        ("papa", "Ta voix n'a pas cassé le trait."),
        ("maman", "Accrochez, à présent, sans le brusquer."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino tient le ruban, et Sarah le verre."),
        ("enfant-f", "On tire ensemble, lentement."),
        ("narrateur", "La craie se cache dans une fente de pierre."),
    ),
    (1, 1, 3): L(
        ("narrateur", "Après le dernier trait, le ruban descend."),
        ("copain", "On a soufflé, d'abord."),
        ("enfant-f", "Puis tu as dit : on accroche."),
        ("maman", "Un trait, puis un toc."),
        ("papa", "Le jardin redevient tiède."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino rit, minuscule, sous les prunes."),
        ("enfant-f", "Le prunier a attendu le soleil."),
        ("narrateur", "Deux ombres tiennent le nœud, sous les prunes."),
    ),
    (1, 2, 1): L(
        ("narrateur", "La rose est vide, et le verre reflète le ciel."),
        ("copain", "Elle a volé, Sarah."),
        ("enfant-f", "Tu as dit oui, après."),
        ("papa", "Les ailes se sont tues."),
        ("maman", "Le grelot glisse vers la branche."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino souffle sur le verre, minuscule."),
        ("enfant-f", "Il chante, dans le bleu."),
        ("narrateur", "Une feuille de rose reste collée au verre."),
    ),
    (1, 2, 2): L(
        ("narrateur", "Le petit son les mène jusqu'au prunier."),
        ("enfant-f", "Le grelot descend, lentement."),
        ("copain", "Il a tenu près de la rose."),
        ("papa", "Vous avez fait un chemin, ensemble."),
        ("maman", "La branche devient une cloche, à présent."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino pousse le verre, une dernière fois."),
        ("enfant-f", "On reste un peu."),
        ("narrateur", "Une aile rouge a laissé sa poussière sur le col."),
    ),
    (1, 2, 3): L(
        ("narrateur", "La rose reste à sa place."),
        ("copain", "Tu n'as pas pris ma rose."),
        ("enfant-f", "Tu avais dit non."),
        ("papa", "Sa rose est restée à lui."),
        ("maman", "Le prunier a eu son toc, malgré ça."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino écoute, puis reprend la rose."),
        ("enfant-f", "Je sonne, tu regardes."),
        ("narrateur", "Le toc du bocal voyage jusqu'à la rose."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Les deux sandales fument un peu, sous la table."),
        ("copain", "Le pied nu n'a plus froid."),
        ("enfant-f", "On peut accrocher, là."),
        ("papa", "Vous avez cherché ensemble."),
        ("maman", "La branche attend, un peu."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino s'assoit, le pied au chaud."),
        ("enfant-f", "Le carillon est prêt, pour deux."),
        ("narrateur", "Les deux sandales fument un peu, au soleil."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Le petit regard est fini."),
        ("copain", "Il chantait, presque."),
        ("enfant-f", "Tu as vu, une seconde."),
        ("papa", "Un œil a suffi, ce soir."),
        ("maman", "La sandale est chaussée, à présent."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Nino s'assoit au bord de l'herbe."),
        ("enfant-f", "On noue, lentement."),
        ("narrateur", "La sandale droite garde une goutte de prune."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Nino enfile, un instant, sans se presser."),
        ("enfant-f", "Plus tard, il a dit."),
        ("enfant-f", "Le son t'attend à la branche."),
        ("papa", "Tu as dit une autre heure."),
        ("maman", "Le pied nu cherche, lui."),
        ("narrateur", "Le bocal garde un toc, tiède contre le bois."),
        ("narrateur", "Sarah laisse un toc à part, pour lui."),
        ("enfant-f", "Le prunier t'attend, Nino."),
        ("narrateur", "Le bocal sonne pour l'heure d'après."),
    ),
    (2, 1, 1): L(
        ("narrateur", "Le soleil de craie borde la marche de pierre."),
        ("copain", "Il a son dernier trait, Sarah."),
        ("enfant-f", "Oui, bien jaune."),
        ("papa", "La craie a laissé la place."),
        ("maman", "Le prunier fait un petit toc."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino noue le ruban, les doigts tâchés de jaune."),
        ("enfant-f", "Le jardin chante, là."),
        ("narrateur", "Le grelot et le soleil de craie se touchent."),
    ),
    (2, 1, 2): L(
        ("narrateur", "Le carillon collé écoute, un peu, près du trait."),
        ("enfant-f", "Il t'a attendu, bas."),
        ("copain", "J'ai dit oui, près de toi."),
        ("papa", "Ta voix n'a pas cassé le trait."),
        ("maman", "Accrochez, à présent, sans le brusquer."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino tient le ruban, et Sarah le fer."),
        ("enfant-f", "On tire ensemble, lentement."),
        ("narrateur", "Un rayon jaune tremble sur le petit fer."),
    ),
    (2, 1, 3): L(
        ("narrateur", "Après le dernier trait, le ruban descend."),
        ("copain", "On a soufflé, d'abord."),
        ("enfant-f", "Puis tu as dit : on accroche."),
        ("maman", "Un trait, puis un toc."),
        ("papa", "Le jardin redevient tiède."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino rit, minuscule, sur la marche."),
        ("enfant-f", "Le prunier a attendu le soleil."),
        ("narrateur", "La marche de pierre garde un tintement mince."),
    ),
    (2, 2, 1): L(
        ("narrateur", "La rose est vide, et le fer reste froid."),
        ("copain", "Elle a volé, Sarah."),
        ("enfant-f", "Tu as dit oui, après."),
        ("papa", "Les ailes se sont tues."),
        ("maman", "Le grelot glisse vers la branche."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino souffle sur le fer, minuscule."),
        ("enfant-f", "Il chante, dans le bleu."),
        ("narrateur", "La rose vide sent le chaud du soir."),
    ),
    (2, 2, 2): L(
        ("narrateur", "Le petit son les mène jusqu'au prunier."),
        ("enfant-f", "Le grelot descend, lentement."),
        ("copain", "Il a tenu près de la rose."),
        ("papa", "Vous avez fait un chemin, ensemble."),
        ("maman", "La branche devient une cloche, à présent."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino pousse le fer, une dernière fois."),
        ("enfant-f", "On reste un peu."),
        ("narrateur", "Le chemin de son va de la rose au prunier."),
    ),
    (2, 2, 3): L(
        ("narrateur", "La rose reste à sa place."),
        ("copain", "Tu n'as pas pris ma rose."),
        ("enfant-f", "Tu avais dit non."),
        ("papa", "Sa rose est restée à lui."),
        ("maman", "Le prunier a eu son toc, malgré ça."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino écoute, puis reprend la rose."),
        ("enfant-f", "Je sonne, tu regardes."),
        ("narrateur", "Nino écoute depuis la rose, sans bouger."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Les deux sandales fument un peu, près de la marche."),
        ("copain", "Le pied nu n'a plus froid."),
        ("enfant-f", "On peut accrocher, là."),
        ("papa", "Vous avez cherché ensemble."),
        ("maman", "La branche attend, un peu."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino s'assoit, le pied au chaud."),
        ("enfant-f", "Le carillon est prêt, pour deux."),
        ("narrateur", "Le grelot a montré l'herbe, puis la branche."),
    ),
    (2, 3, 2): L(
        ("narrateur", "Le petit regard est fini."),
        ("copain", "Il chantait, presque."),
        ("enfant-f", "Tu as vu, une seconde."),
        ("papa", "Un œil a suffi, ce soir."),
        ("maman", "La sandale est chaussée, à présent."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Nino s'assoit au bord de l'herbe."),
        ("enfant-f", "On noue, lentement."),
        ("narrateur", "Un tintement court, puis le pied se chausse."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Nino enfile, un instant, sans se presser."),
        ("enfant-f", "Plus tard, il a dit."),
        ("enfant-f", "Le son t'attend à la branche."),
        ("papa", "Tu as dit une autre heure."),
        ("maman", "Le pied nu cherche, lui."),
        ("narrateur", "Le grelot dort contre le verre, minuscule."),
        ("narrateur", "Sarah laisse un tintement à part, pour lui."),
        ("enfant-f", "Le prunier t'attend, Nino."),
        ("narrateur", "La marche garde le grelot, pour plus tard."),
    ),
    (3, 1, 1): L(
        ("narrateur", "Le soleil de craie regarde la boucle vide."),
        ("copain", "Il a son dernier trait, Sarah."),
        ("enfant-f", "Oui, bien jaune."),
        ("papa", "La craie a laissé la place."),
        ("maman", "Le prunier fait un petit toc."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino glisse le grelot dans la boucle."),
        ("enfant-f", "Le jardin chante, là."),
        ("narrateur", "Nino pose sa craie au pied du prunier."),
    ),
    (3, 1, 2): L(
        ("narrateur", "Le carillon collé écoute, un peu, près du trait."),
        ("enfant-f", "Il t'a attendu, bas."),
        ("copain", "J'ai dit oui, près de toi."),
        ("papa", "Ta voix n'a pas cassé le trait."),
        ("maman", "Accrochez, à présent, sans le brusquer."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino tient le verre, et Sarah la boucle."),
        ("enfant-f", "On tire ensemble, lentement."),
        ("narrateur", "La boucle bleue frôle le dernier trait jaune."),
    ),
    (3, 1, 3): L(
        ("narrateur", "Après le dernier trait, le ruban descend."),
        ("copain", "On a soufflé, d'abord."),
        ("enfant-f", "Puis tu as dit : on accroche."),
        ("maman", "Un trait, puis un toc."),
        ("papa", "Le jardin redevient tiède."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino rit, minuscule, dans l'herbe."),
        ("enfant-f", "Le prunier a attendu le soleil."),
        ("narrateur", "L'herbe tache le ruban, sous la branche."),
    ),
    (3, 2, 1): L(
        ("narrateur", "La rose est vide, et le bleu bat un peu."),
        ("copain", "Elle a volé, Sarah."),
        ("enfant-f", "Tu as dit oui, après."),
        ("papa", "Les ailes se sont tues."),
        ("maman", "Le grelot glisse vers la branche."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino souffle sur la boucle, minuscule."),
        ("enfant-f", "Il chante, dans le bleu."),
        ("narrateur", "Le ruban bat, et la rose n'a plus d'hôte."),
    ),
    (3, 2, 2): L(
        ("narrateur", "Le petit son les mène jusqu'au prunier."),
        ("enfant-f", "Le grelot descend, lentement."),
        ("copain", "Il a tenu près de la rose."),
        ("papa", "Vous avez fait un chemin, ensemble."),
        ("maman", "La branche devient une cloche, à présent."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino pousse la boucle, une dernière fois."),
        ("enfant-f", "On reste un peu."),
        ("narrateur", "Le bleu du ruban n'a pas chassé l'aile."),
    ),
    (3, 2, 3): L(
        ("narrateur", "La rose reste à sa place."),
        ("copain", "Tu n'as pas pris ma rose."),
        ("enfant-f", "Tu avais dit non."),
        ("papa", "Sa rose est restée à lui."),
        ("maman", "Le prunier a eu son toc, malgré ça."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino écoute, puis reprend la rose."),
        ("enfant-f", "Je sonne, tu regardes."),
        ("narrateur", "Deux jeux se parlent, de loin, sans se tirer."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Les deux sandales fument un peu, sous les prunes."),
        ("copain", "Le pied nu n'a plus froid."),
        ("enfant-f", "On peut accrocher, là."),
        ("papa", "Vous avez cherché ensemble."),
        ("maman", "La branche attend, un peu."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino s'assoit, le pied au chaud."),
        ("enfant-f", "Le carillon est prêt, pour deux."),
        ("narrateur", "La sandale était sous les prunes, au frais."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Le petit regard est fini."),
        ("copain", "Il chantait, presque."),
        ("enfant-f", "Tu as vu, une seconde."),
        ("papa", "Un œil a suffi, ce soir."),
        ("maman", "La sandale est chaussée, à présent."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Nino s'assoit au bord de l'herbe."),
        ("enfant-f", "On noue, lentement."),
        ("narrateur", "Un regard bleu, puis le pied retrouve son cuir."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Nino enfile, un instant, sans se presser."),
        ("enfant-f", "Plus tard, il a dit."),
        ("enfant-f", "Le son t'attend à la branche."),
        ("papa", "Tu as dit une autre heure."),
        ("maman", "Le pied nu cherche, lui."),
        ("narrateur", "Le ruban bleu tient un nœud, ferme."),
        ("narrateur", "Sarah laisse un bleu à part, pour lui."),
        ("enfant-f", "Le prunier t'attend, Nino."),
        ("narrateur", "Le ruban fait un pont, et Nino cherche."),
    ),
}

T3_SONS = {1: "carillon,vent", 2: "grelot,rose", 3: "herbe,tissu"}
FIN_SONS = {1: "prunier,verre", 2: "prunier,vent", 3: "prunier,linge"}
T3_EMPH = {
    1: {1: "soleil", 2: "carillon", 3: "côté"},
    2: {1: "envol", 2: "grelot", 3: "carillon"},
    3: {1: "sandale", 2: "regard", 3: "plus tard"},
}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "prune,linge", "emphasis": "carillon"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Le carillon a besoin de trois choses."),
            ("papa", "Le bocal, le grelot, ou le ruban bleu ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le bocal",
            "option_2_label": "le grelot",
            "option_3_label": "le ruban bleu",
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
                "option_1_label": "le soleil de craie",
                "option_2_label": "la coccinelle",
                "option_3_label": "la sandale",
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
                    extra={"sons": FIN_SONS[c], "emphasis": "prunier"},
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
        "Sarah veut accrocher un carillon au prunier, pour que Nino entende "
        "le jardin chanter avec elle, avant le vent du soir. Elle crie trop tôt : "
        "Nino ne se tourne pas, le bocal glisse. Elle reprend par le verre, le grelot "
        "ou le ruban bleu. Nino dessine un soleil, suit une coccinelle, ou cherche "
        "une sandale. Elle attend, parle près, s'assoit ; attend l'envol, offre un son "
        "minuscule, ou garde le carillon ; aide, montre un instant, ou propose plus tard. "
        "Le prunier sonne."
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
    if "sarah" not in blob or "nino" not in blob:
        raise SystemExit("troupe Sarah/Nino absente")
    for bad in (
        "escargot", "loupe", "carnet bleu", "pots de menthe", "trace d'argent",
        "sara ", "kenzo", "coussin", "le fort", "tomate", "figuier",
        "dinette", "dînette", "wagon", "sifflet", "capitaine", "plic",
        "volet jaune", "poissons de papier", "nichoir", "citronnade",
        "cerf-volant", "bac à sable",
    ):
        if bad in whole:
            raise SystemExit(f"calque: {bad}")
    for bad in ("la cuisine", "le jardin", "la chambre"):
        if bad in labels:
            raise SystemExit(f"label calque: {bad}")
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
        "Fin d'après-midi au jardin : prunier mûr, fil à linge, terre sucrée. "
        "Sarah veut un carillon au prunier, pour que Nino entende le jardin chanter "
        "avec elle, avant le vent du soir. Elle crie trop tôt : Nino ne se tourne pas, "
        "le bocal glisse, papa remercie qu'elle l'ait rattrapé. T1 change le premier "
        "geste (verre trop fort à la table / grelot trop fort sur la marche / boucle "
        "vide à la branche). T2 : Nino a autre chose (soleil de craie, coccinelle, "
        "sandale). T3 change l'invitation : attendre, parler près, s'asseoir ; "
        "attendre l'envol, un son minuscule, garder le carillon (le non compte) ; "
        "aider, un petit regard, plus tard. La leçon se vit : elle propose, elle "
        "accepte oui, non, ou une autre heure. Chaque fin paie le toc, le nœud, "
        "le prunier. Autre récit que TREE-COL-015 (pas d'escargot, pas de piste d'argent).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N3 ≤ 16. Troupe D16 : Sarah, Nino, papa, maman.\n"
        "- Sara et le slogan « Inviter sans forcer » jetés. Première idée échoue (cri, toc plat).\n"
        "- 27 fins textuellement distinctes. Un merci vécu (rattraper le bocal), pas un refrain Bravo.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n"
        "- Tics « tout doux / tout calme / encore / déjà » écartés. Silence de Nino = réponse.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
