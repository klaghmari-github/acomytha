#!/usr/bin/env python3
"""TREE-DIF-054 — Le loup de carton de Victorina, sur le mur (F-NAR-019, N3, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-054"
LIM = 16
TITLE = "Le loup de carton de Victorina, sur le mur"
CHARS = "Victorina, papa, maman"
SETTING = "la maison, le soir : couloir, buffet, placard sous l'escalier, palier"
TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "il faut attendre",
    "laisser le temps",
    "attendre la fin",
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_loup_veut_le_grand_mur_mais_la_lune_manque; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_mot_de_papa_se_casse; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_decouragement; intensite=2; destinataire=enfant; sous_texte=la_phrase_de_papa_se_coupe; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_lune_arrive_quand_la_bouche_reste_fermee; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=le_loup_marche_sur_le_mur; tempo=pose; sourire=léger; respiration=ample",
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
    ("narrateur", "Sur les carreaux du couloir, une bande jaune s'allonge."),
    ("narrateur", "La lampe du portemanteau tient ce rond tiède."),
    ("narrateur", "Ça sent le savon, près de la salle d'eau."),
    ("narrateur", "Une horloge tape, derrière la porte de la cuisine."),
    ("narrateur", "Victorina vit ici avec papa et maman."),
    ("papa", "Le torchon est plié, près de la marche."),
    ("maman", "Ta serviette reste un peu humide, Victorina."),
    ("narrateur", "Un loup de carton attend, gris, contre le bois."),
    ("enfant-f", "Mon loup va marcher, tout grand, ce soir."),
    ("narrateur", "En ce moment, Victorina pose le carton contre le mur."),
    ("narrateur", "Deux oreilles pointues cherchent la lumière, sans bouger."),
    ("papa", "Tu veux le grand mur, c'est ça ?"),
    ("enfant-f", "Le grand, papa, avec la lune."),
    ("papa", "La lune de papier est dans le."),
    ("narrateur", "Le mot s'arrête, et le carton glisse."),
    ("enfant-f", "Dans le quoi ?"),
    ("narrateur", "Une oreille se plie, molle, contre le carreau."),
    ("enfant-f", "Il ne tient plus."),
    ("maman", "La bande jaune recule un peu, là-bas."),
    ("papa", "Prenez vos affaires, avant que la lumière parte."),
)


T1 = {
    1: dict(
        name="le drap blanc",
        expected="drap",
        accepted="drap | le drap | drap blanc | le drap blanc | le coton",
        retry="Victorina tient le drap. Elle tient quoi ?",
        ok="Oui, c'est le drap.",
        sons="tissu,couloir",
        emphasis="drap blanc",
        passage=L(
            ("narrateur", "Victorina saisit le drap blanc, trop vite."),
            ("enfant-f", "Je le jette, et le loup marche !"),
            ("narrateur", "Le coton tombe sur la bouche de papa."),
            ("papa", "Il est parti sous le linge."),
            ("enfant-f", "Pardon, il m'échappe."),
            ("maman", "Garde-le contre toi, droit."),
            ("narrateur", "Le coton sent le savon de la salle d'eau."),
            ("papa", "Le loup, près de toi, et la lampe."),
            ("narrateur", "Maman glisse la lampe ronde vers l'épaule."),
            ("narrateur", "Les trois affaires avancent avec elle."),
            ("enfant-f", "La lune, papa ?"),
            ("narrateur", "Papa ouvre la bouche, puis la referme."),
            ("papa", "On marche, le mot va venir."),
        ),
        question=L(
            ("narrateur", "Le coton blanc reste contre son bras."),
            ("maman", "Victorina a pris quoi, d'abord ?"),
        ),
        confirm=L(
            ("enfant-f", "Le drap."),
            ("papa", "Oui, le coton."),
            ("narrateur", "Le loup et la lampe voyagent contre le linge."),
            ("maman", "La lune se dira plus loin."),
            ("enfant-f", "Je le tiens droit, cette fois."),
            ("papa", "On marche, alors ?"),
            ("enfant-f", "Oui, papa."),
            ("narrateur", "Le drap penche vers le couloir, patient."),
        ),
        choice=L(
            ("narrateur", "Le drap blanc penche vers le couloir."),
            ("narrateur", "La maison a trois coins, ce soir."),
            ("papa", "Le buffet, le placard, ou l'étagère ?"),
        ),
    ),
    2: dict(
        name="le loup de carton",
        expected="loup",
        accepted="loup | le loup | carton | le carton | loup de carton",
        retry="Victorina tient le loup. Elle tient quoi ?",
        ok="Oui, c'est le loup.",
        sons="carton,colle",
        emphasis="loup de carton",
        passage=L(
            ("narrateur", "Victorina saisit le loup de carton."),
            ("enfant-f", "Il marche sans lune, je parie !"),
            ("narrateur", "Elle le tend vers le mur, trop tôt."),
            ("narrateur", "L'ombre n'est qu'une tache, sans oreilles."),
            ("enfant-f", "C'est moche."),
            ("papa", "Tiens-le contre toi, les oreilles hautes."),
            ("narrateur", "Le carton sent la colle, fine, un peu rêche."),
            ("maman", "Le drap ensuite, autour du bras."),
            ("narrateur", "Papa glisse la lampe ronde dans sa main libre."),
            ("narrateur", "Les trois affaires avancent, pas après pas."),
            ("enfant-f", "Alors dis-moi où."),
            ("narrateur", "Papa inspire, les lèvres rondes, vides."),
            ("maman", "Il cherche la suite."),
            ("enfant-f", "J'écoute."),
        ),
        question=L(
            ("narrateur", "Le carton gris reste contre sa hanche."),
            ("papa", "Victorina a pris quoi, d'abord ?"),
        ),
        confirm=L(
            ("enfant-f", "Le loup."),
            ("maman", "Oui, le carton."),
            ("narrateur", "Le drap penche sous le bras, lourd."),
            ("narrateur", "La lampe dort contre sa hanche, ronde."),
            ("papa", "Le carton a un peu piqué."),
            ("enfant-f", "J'écoute la suite."),
            ("maman", "On reste ensemble."),
            ("enfant-f", "D'accord."),
        ),
        choice=L(
            ("narrateur", "Le loup de carton tape un peu sa hanche."),
            ("narrateur", "La maison a trois coins, ce soir."),
            ("maman", "Le buffet, le placard, ou l'étagère ?"),
        ),
    ),
    3: dict(
        name="la lampe ronde",
        expected="lampe",
        accepted="lampe | la lampe | lampe ronde | la lampe ronde | le rond",
        retry="Victorina tient la lampe. Elle tient quoi ?",
        ok="Oui, c'est la lampe.",
        sons="clic,lampe",
        emphasis="lampe ronde",
        passage=L(
            ("narrateur", "Victorina saisit la lampe ronde."),
            ("enfant-f", "Pour le loup, après."),
            ("papa", "Elle est tiède, dans ta paume."),
            ("narrateur", "Un clic trop fort réveille le plafond."),
            ("enfant-f", "Maintenant, tu dis où."),
            ("narrateur", "Le mot se noie dans le clic."),
            ("papa", "Le mot va arriver."),
            ("maman", "Le drap ensuite, et le loup."),
            ("narrateur", "Papa les pose contre elle, l'un après l'autre."),
            ("enfant-f", "D'accord."),
            ("narrateur", "Près de la marche, plus rien n'attend."),
            ("maman", "On avance, sans courir."),
            ("enfant-f", "J'attends le mot, cette fois."),
        ),
        question=L(
            ("narrateur", "Le rond tiède reste dans sa paume."),
            ("maman", "Victorina a pris quoi, d'abord ?"),
        ),
        confirm=L(
            ("enfant-f", "La lampe."),
            ("papa", "Oui, le rond."),
            ("narrateur", "Le drap et le loup pèsent contre elle, chauds."),
            ("maman", "Le rond va parler, en marchant."),
            ("enfant-f", "J'attends le mot."),
            ("papa", "Il va venir, tout seul."),
            ("maman", "On avance, alors ?"),
            ("enfant-f", "Oui."),
        ),
        choice=L(
            ("narrateur", "La lampe ronde pèse contre sa hanche."),
            ("narrateur", "La maison a trois coins, ce soir."),
            ("papa", "Le buffet, le placard, ou l'étagère ?"),
        ),
    ),
}


def t2_buffet(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Le drap blanc arrive près du buffet."),
            ("narrateur", "Il bute contre une pile d'assiettes, bas."),
            ("narrateur", "Des assiettes s'entrechoquent, mêlées sur le bois."),
            ("enfant-f", "C'est ici ?"),
            ("papa", "C'est la lune, près du."),
            ("narrateur", "Le mot s'arrête au milieu, couvert par le bruit."),
            ("enfant-f", "Près du quoi ?"),
            ("narrateur", "Victorina referme sa bouche, nette."),
            ("maman", "Elles se ressemblent toutes, là-haut."),
            ("papa", "On fait comment, Victorina ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Le loup de carton arrive près du buffet."),
            ("narrateur", "Il s'accroche à une anse, trop tôt."),
            ("narrateur", "Des assiettes s'entrechoquent, mêlées sur le bois."),
            ("enfant-f", "Elle est là, sous une assiette ?"),
            ("papa", "C'est la lune, près du."),
            ("narrateur", "Un tintement mange la fin, sec."),
            ("enfant-f", "Près du quoi ?"),
            ("narrateur", "Victorina pince le carton, puis relâche."),
            ("maman", "Elles parlent trop fort, ces assiettes."),
            ("papa", "On fait comment, Victorina ?"),
        )
    return L(
        ("narrateur", "La lampe ronde arrive près du buffet."),
        ("narrateur", "Elle tape le bois, un petit toc."),
        ("narrateur", "Des assiettes s'entrechoquent, mêlées sur le bois."),
        ("enfant-f", "Le rond va la trouver !"),
        ("papa", "C'est la lune, près du."),
        ("narrateur", "Le toc et les assiettes couvrent la suite."),
        ("enfant-f", "Près du quoi ?"),
        ("narrateur", "Victorina baisse la lampe, les joues chaudes."),
        ("maman", "Elles se ressemblent toutes, là-haut."),
        ("papa", "On fait comment, Victorina ?"),
    )


def t2_placard(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Le drap blanc arrive près du placard, sous l'escalier."),
            ("narrateur", "Il se froisse un peu, au bord sombre."),
            ("enfant-f", "Elle est là, la lune ?"),
            ("maman", "Elle est derrière le."),
            ("narrateur", "L'écho couvre le mot, fort, entre les cartons."),
            ("narrateur", "Un fond de boîte tape, loin."),
            ("enfant-f", "Derrière le bois ?"),
            ("narrateur", "Victorina recule d'un pas, puis attend."),
            ("papa", "On n'entend plus la fin."),
            ("maman", "Tu trouves comment ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Le loup de carton arrive près du placard, sous l'escalier."),
            ("narrateur", "Il rentre de travers, les oreilles pliées."),
            ("enfant-f", "Il va la sentir, lui !"),
            ("maman", "Elle est derrière le."),
            ("narrateur", "L'écho lui renvoie sa propre voix, trop forte."),
            ("enfant-f", "Derrière le bois ?"),
            ("narrateur", "Victorina serre le carton, déçue un instant."),
            ("papa", "On n'entend plus la fin."),
            ("narrateur", "Un fond de boîte tape, loin."),
            ("maman", "Tu trouves comment ?"),
        )
    return L(
        ("narrateur", "La lampe ronde arrive près du placard, sous l'escalier."),
        ("narrateur", "Elle éclaire un coin, trop vite."),
        ("enfant-f", "Je la vois, peut-être !"),
        ("maman", "Elle est derrière le."),
        ("narrateur", "L'écho avale le mot, et le rond saute."),
        ("enfant-f", "Derrière le bois ?"),
        ("narrateur", "Victorina baisse le rond, les épaules tombées."),
        ("papa", "On n'entend plus la fin."),
        ("narrateur", "Un fond de boîte tape, loin."),
        ("maman", "Tu trouves comment ?"),
    )


def t2_etagere(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Le drap blanc arrive sous l'étagère du palier."),
            ("narrateur", "Il reste trop bas, sous le bois."),
            ("enfant-f", "Tout en haut ?"),
            ("papa", "Tout en haut, près du."),
            ("narrateur", "Papa s'arrête, les lèvres rondes, sans la suite."),
            ("enfant-f", "Près du cadre ?"),
            ("narrateur", "Victorina garde sa bouche fermée, après."),
            ("maman", "Le haut est trop loin, pour elle."),
            ("papa", "Un tabouret dort près du mur."),
            ("papa", "Tu fais quoi, alors ?"),
        )
    if a == 2:
        return L(
            ("narrateur", "Le loup de carton arrive sous l'étagère du palier."),
            ("narrateur", "Il pend, trop court, sous la planche."),
            ("enfant-f", "Ses oreilles veulent le haut !"),
            ("papa", "Tout en haut, près du."),
            ("narrateur", "Papa s'arrête, les lèvres rondes, sans la suite."),
            ("enfant-f", "Près du cadre ?"),
            ("narrateur", "Victorina lève le carton, puis le baisse."),
            ("maman", "Le haut est trop loin, pour elle."),
            ("papa", "Un tabouret dort près du mur."),
            ("papa", "Tu fais quoi, alors ?"),
        )
    return L(
        ("narrateur", "La lampe ronde arrive sous l'étagère du palier."),
        ("narrateur", "Elle n'atteint pas le bord, trop haute."),
        ("enfant-f", "Le rond va grimper !"),
        ("papa", "Tout en haut, près du."),
        ("narrateur", "Papa s'arrête, les lèvres rondes, sans la suite."),
        ("enfant-f", "Près du cadre ?"),
        ("narrateur", "Victorina tend le bras, puis le ramène."),
        ("maman", "Le haut est trop loin, pour elle."),
        ("papa", "Un tabouret dort près du mur."),
        ("papa", "Tu fais quoi, alors ?"),
    )


T2_FN = {1: t2_buffet, 2: t2_placard, 3: t2_etagere}
T2_SONS = {1: "assiettes,bois", 2: "echo,carton", 3: "bois,palier"}
T2_EMPH = {1: "assiettes", 2: "placard", 3: "étagère"}
T3_LABS = {
    1: ("le tiroir du bas", "la serviette", "la chaise"),
    2: ("la porte tenue", "le chuchotement", "la marche"),
    3: ("le tabouret", "le regard d'en bas", "les bras de papa"),
}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Sur le buffet, la suite manque."),
            ("papa", "Le tiroir, la serviette, ou la chaise ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "Près du placard, le mot n'est pas fini."),
            ("maman", "La porte, le chuchotement, ou la marche ?"),
        )
    return L(
        ("narrateur", "Sous l'étagère, le haut attend."),
        ("papa", "Le tabouret, le regard, ou mes bras ?"),
    )


COL = {
    1: "Le drap blanc reste contre la jambe, sage.",
    2: "Le loup de carton attend un dernier pas.",
    3: "La lampe ronde dort contre sa paume.",
}


T3 = {
    (1, 1, 1): L(
        ("enfant-f", "On reste."),
        ("narrateur", "Elles s'arrêtent sous les assiettes, sans un cri."),
        ("papa", "Le tiroir."),
        ("enfant-f", "Le tiroir du bas."),
        ("narrateur", "Victorina attend, sans crier, les lèvres fermées."),
        ("narrateur", "Une lune de papier penche, enfin, contre le bois."),
        ("narrateur", COL[1]),
        ("maman", "Elle était là, tout contre."),
        ("papa", "Merci, Victorina."),
    ),
    (1, 1, 2): L(
        ("enfant-f", "La serviette, dessus."),
        ("narrateur", "Les assiettes se taisent un peu, sous le linge."),
        ("papa", "Le."),
        ("narrateur", "Victorina ne dit rien."),
        ("papa", "Le bas, sous le linge."),
        ("enfant-f", "Je la vois, maintenant."),
        ("narrateur", COL[1]),
        ("maman", "Le linge a calmé le bois."),
        ("papa", "Merci d'avoir posé le linge."),
    ),
    (1, 1, 3): L(
        ("enfant-f", "On s'assoit."),
        ("narrateur", "Elles regardent le bois, près du pied."),
        ("papa", "Pas le haut."),
        ("narrateur", "Victorina garde sa bouche fermée."),
        ("papa", "Contre la chaise."),
        ("enfant-f", "Celle-là, tout contre le pied."),
        ("narrateur", COL[1]),
        ("maman", "Le pied de chaise a parlé, lui."),
        ("papa", "La lune est là."),
    ),
    (1, 2, 1): L(
        ("enfant-f", "On tient."),
        ("narrateur", "Les deux retiennent la porte, sans l'écho."),
        ("papa", "Derrière le."),
        ("narrateur", "Victorina attend, les lèvres fermées."),
        ("papa", "Derrière le carton, la lune."),
        ("enfant-f", "Je l'entends, maintenant."),
        ("narrateur", COL[1]),
        ("maman", "La porte s'est tue."),
        ("papa", "Merci d'avoir tenu avec moi."),
    ),
    (1, 2, 2): L(
        ("enfant-f", "Tout bas, ici."),
        ("papa", "Tout près des oreilles."),
        ("narrateur", "L'écho devient un peu plus loin."),
        ("maman", "Derrière."),
        ("narrateur", "Victorina attend, les lèvres fermées."),
        ("maman", "Derrière la boîte."),
        ("narrateur", COL[1]),
        ("papa", "On a chuchoté ensemble."),
        ("maman", "On l'entend, maintenant."),
    ),
    (1, 2, 3): L(
        ("enfant-f", "La marche, là."),
        ("papa", "On s'assoit, sans courir."),
        ("narrateur", "Le bois est froid, sous les chaussettes."),
        ("maman", "La lune."),
        ("narrateur", "Victorina tourne la tête, sans parler."),
        ("enfant-f", "Je la vois, contre le fond."),
        ("narrateur", COL[1]),
        ("papa", "La marche a tenu le mot."),
        ("maman", "On a regardé ensemble."),
    ),
    (1, 3, 1): L(
        ("enfant-f", "Le tabouret, dessous."),
        ("papa", "Je le tiens, à ta hauteur."),
        ("narrateur", "Victorina monte, sans crier."),
        ("papa", "Près du."),
        ("narrateur", "Victorina attend, un pied en l'air."),
        ("papa", "Près du cadre."),
        ("narrateur", COL[1]),
        ("maman", "Le bois a tenu tes pieds."),
        ("papa", "Merci d'être restée un instant."),
    ),
    (1, 3, 2): L(
        ("enfant-f", "Je regarde en bas."),
        ("narrateur", "Victorina baisse les yeux, vers la plinthe."),
        ("papa", "Pas le grand."),
        ("enfant-f", "Le petit, contre le bois."),
        ("narrateur", "Une lune de papier penche, bas, tombée."),
        ("narrateur", "Elle attendait près de la plinthe, sans un bruit."),
        ("narrateur", COL[1]),
        ("maman", "Elle attendait là, tout bas."),
        ("papa", "Merci d'avoir baissé les yeux."),
    ),
    (1, 3, 3): L(
        ("enfant-f", "Tes bras, papa."),
        ("papa", "Viens, tout contre moi."),
        ("narrateur", "Victorina s'élève, le nez au cadre, près des livres."),
        ("papa", "La lune, tout près du bord."),
        ("enfant-f", "Je la vois !"),
        ("narrateur", "Un rond blanc brille entre deux livres, enfin."),
        ("narrateur", COL[1]),
        ("maman", "Elle est entre les livres."),
        ("papa", "Chacun a fait sa part."),
    ),
    (2, 1, 1): L(
        ("enfant-f", "On reste, loup contre moi."),
        ("narrateur", "Le carton se tait sous les assiettes."),
        ("papa", "Le tiroir."),
        ("narrateur", "Victorina pince une oreille, puis relâche."),
        ("narrateur", "Une lune de papier penche, contre le bois."),
        ("enfant-f", "Il ne l'a pas bousculée."),
        ("narrateur", COL[2]),
        ("maman", "Elle était là, tout contre."),
        ("papa", "Merci, Victorina."),
    ),
    (2, 1, 2): L(
        ("enfant-f", "La serviette, et le loup attend."),
        ("narrateur", "Les assiettes se taisent sous le linge."),
        ("papa", "Le."),
        ("narrateur", "Le carton reste collé à sa hanche, muet."),
        ("papa", "Le bas, sous le linge."),
        ("enfant-f", "Je la vois, gris comme lui."),
        ("narrateur", COL[2]),
        ("maman", "Le linge a calmé le bois."),
        ("papa", "Merci d'avoir posé le linge."),
    ),
    (2, 1, 3): L(
        ("enfant-f", "On s'assoit, lui sur les genoux."),
        ("narrateur", "Le carton regarde le pied de chaise."),
        ("papa", "Pas le haut."),
        ("narrateur", "Victorina pose une oreille contre le bois."),
        ("papa", "Contre la chaise."),
        ("enfant-f", "Il l'a sentie, lui."),
        ("narrateur", COL[2]),
        ("maman", "Le pied de chaise a parlé, lui."),
        ("papa", "La lune est là."),
    ),
    (2, 2, 1): L(
        ("enfant-f", "On tient, loup au poing."),
        ("narrateur", "Les deux retiennent la porte, et le carton se tait."),
        ("papa", "Derrière le."),
        ("narrateur", "Victorina attend, une oreille contre le bois."),
        ("papa", "Derrière le carton, la lune."),
        ("enfant-f", "Il l'a entendue, lui aussi."),
        ("narrateur", COL[2]),
        ("maman", "La porte s'est tue."),
        ("papa", "Merci d'avoir tenu avec moi."),
    ),
    (2, 2, 2): L(
        ("enfant-f", "Chut, loup."),
        ("papa", "Tout près des oreilles."),
        ("narrateur", "L'écho recule, et le carton ne gratte plus."),
        ("maman", "Derrière."),
        ("narrateur", "Victorina colle le loup à sa joue, silencieuse."),
        ("maman", "Derrière la boîte."),
        ("narrateur", COL[2]),
        ("papa", "On a chuchoté ensemble."),
        ("maman", "On l'entend, maintenant."),
    ),
    (2, 2, 3): L(
        ("enfant-f", "La marche, loup avec moi."),
        ("papa", "On s'assoit, sans courir."),
        ("narrateur", "Le carton pose son museau sur le bois froid."),
        ("maman", "La lune."),
        ("narrateur", "Victorina tourne la tête, sans parler."),
        ("enfant-f", "Il la montre, contre le fond."),
        ("narrateur", COL[2]),
        ("papa", "La marche a tenu le mot."),
        ("maman", "On a regardé ensemble."),
    ),
    (2, 3, 1): L(
        ("enfant-f", "Le tabouret, et lui avec."),
        ("papa", "Je le tiens, à ta hauteur."),
        ("narrateur", "Victorina monte, le carton contre le ventre."),
        ("papa", "Près du."),
        ("narrateur", "Une oreille tremble, puis se tient."),
        ("papa", "Près du cadre."),
        ("narrateur", COL[2]),
        ("maman", "Le bois a tenu tes pieds."),
        ("papa", "Merci d'être restée un instant."),
    ),
    (2, 3, 2): L(
        ("enfant-f", "Le loup regarde en bas."),
        ("narrateur", "Victorina baisse le carton, vers la plinthe."),
        ("papa", "Pas le grand."),
        ("enfant-f", "Le petit, contre le bois."),
        ("narrateur", "Une lune de papier penche, bas, tombée."),
        ("narrateur", "Le museau la touche, sans la froisser."),
        ("narrateur", COL[2]),
        ("maman", "Elle attendait là, tout bas."),
        ("papa", "Merci d'avoir baissé les yeux."),
    ),
    (2, 3, 3): L(
        ("enfant-f", "Tes bras, et le loup."),
        ("papa", "Viens, tout contre moi."),
        ("narrateur", "Victorina s'élève, le carton entre eux, près des livres."),
        ("papa", "La lune, tout près du bord."),
        ("enfant-f", "Il la voit !"),
        ("narrateur", "Un rond blanc brille entre deux livres, enfin."),
        ("narrateur", COL[2]),
        ("maman", "Elle est entre les livres."),
        ("papa", "Chacun a fait sa part."),
    ),
    (3, 1, 1): L(
        ("enfant-f", "On reste, lampe basse."),
        ("narrateur", "Le rond éclaire le bas du buffet, sans clic."),
        ("papa", "Le tiroir."),
        ("narrateur", "Victorina tient le bouton, sans le tourner."),
        ("narrateur", "Une lune de papier penche, dans le rond."),
        ("enfant-f", "Elle est jaune, comme la bande."),
        ("narrateur", COL[3]),
        ("maman", "Elle était là, tout contre."),
        ("papa", "Merci, Victorina."),
    ),
    (3, 1, 2): L(
        ("enfant-f", "La serviette, et le rond attend."),
        ("narrateur", "Les assiettes se taisent, et le rond se pose."),
        ("papa", "Le."),
        ("narrateur", "Victorina cache le clic sous le linge."),
        ("papa", "Le bas, sous le linge."),
        ("enfant-f", "Je la vois, dans le rond."),
        ("narrateur", COL[3]),
        ("maman", "Le linge a calmé le bois."),
        ("papa", "Merci d'avoir posé le linge."),
    ),
    (3, 1, 3): L(
        ("enfant-f", "On s'assoit, lampe au sol."),
        ("narrateur", "Le rond glisse jusqu'au pied de chaise."),
        ("papa", "Pas le haut."),
        ("narrateur", "Victorina ne clique plus."),
        ("papa", "Contre la chaise."),
        ("enfant-f", "Le rond l'a trouvée."),
        ("narrateur", COL[3]),
        ("maman", "Le pied de chaise a parlé, lui."),
        ("papa", "La lune est là."),
    ),
    (3, 2, 1): L(
        ("enfant-f", "On tient, lampe éteinte."),
        ("narrateur", "Les deux retiennent la porte, et le rond se tait."),
        ("papa", "Derrière le."),
        ("narrateur", "Victorina attend, le pouce loin du bouton."),
        ("papa", "Derrière le carton, la lune."),
        ("enfant-f", "Sans clic, je l'entends."),
        ("narrateur", COL[3]),
        ("maman", "La porte s'est tue."),
        ("papa", "Merci d'avoir tenu avec moi."),
    ),
    (3, 2, 2): L(
        ("enfant-f", "Tout bas, sans le clic."),
        ("papa", "Tout près des oreilles."),
        ("narrateur", "L'écho recule, et le rond reste tiède."),
        ("maman", "Derrière."),
        ("narrateur", "Victorina souffle sur le verre, sans parler."),
        ("maman", "Derrière la boîte."),
        ("narrateur", COL[3]),
        ("papa", "On a chuchoté ensemble."),
        ("maman", "On l'entend, maintenant."),
    ),
    (3, 2, 3): L(
        ("enfant-f", "La marche, lampe posée."),
        ("papa", "On s'assoit, sans courir."),
        ("narrateur", "Le rond éclaire les chaussettes, puis le fond."),
        ("maman", "La lune."),
        ("narrateur", "Victorina tourne la tête, sans parler."),
        ("enfant-f", "Je la vois, dans le rond."),
        ("narrateur", COL[3]),
        ("papa", "La marche a tenu le mot."),
        ("maman", "On a regardé ensemble."),
    ),
    (3, 3, 1): L(
        ("enfant-f", "Le tabouret, lampe avec moi."),
        ("papa", "Je le tiens, à ta hauteur."),
        ("narrateur", "Victorina monte, le rond contre le cadre."),
        ("papa", "Près du."),
        ("narrateur", "Elle n'appuie pas, le pouce en l'air."),
        ("papa", "Près du cadre."),
        ("narrateur", COL[3]),
        ("maman", "Le bois a tenu tes pieds."),
        ("papa", "Merci d'être restée un instant."),
    ),
    (3, 3, 2): L(
        ("enfant-f", "Le rond regarde en bas."),
        ("narrateur", "Victorina baisse la lampe, vers la plinthe."),
        ("papa", "Pas le grand."),
        ("enfant-f", "Le petit, contre le bois."),
        ("narrateur", "Une lune de papier penche, bas, tombée."),
        ("narrateur", "Le rond la réveille, sans un clic."),
        ("narrateur", COL[3]),
        ("maman", "Elle attendait là, tout bas."),
        ("papa", "Merci d'avoir baissé les yeux."),
    ),
    (3, 3, 3): L(
        ("enfant-f", "Tes bras, et la lampe."),
        ("papa", "Viens, tout contre moi."),
        ("narrateur", "Victorina s'élève, le rond entre les livres."),
        ("papa", "La lune, tout près du bord."),
        ("enfant-f", "Le rond l'a eue !"),
        ("narrateur", "Un rond blanc brille entre deux livres, enfin."),
        ("narrateur", COL[3]),
        ("maman", "Elle est entre les livres."),
        ("papa", "Chacun a fait sa part."),
    ),
}


FIN = {
    (1, 1, 1): L(
        ("narrateur", "La lune rentre dans le poing, un petit clic."),
        ("enfant-f", "Il marche !"),
        ("papa", "Sur le mur du buffet, tout droit."),
        ("maman", "Regarde ses oreilles, droites."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Une miette sèche sur le bois."),
        ("narrateur", "Le buffet se tait autour des assiettes."),
        ("narrateur", "Le savon de la cuisine sent, tiède."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Le loup part, gris, entre les ombres des assiettes."),
        ("enfant-f", "J'ai posé la serviette, d'abord."),
        ("papa", "Puis le mot est venu."),
        ("maman", "Venez, le mur est prêt."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Victorina pose le carton contre l'épaule."),
        ("narrateur", "Une assiette tinte, puis se tait."),
        ("narrateur", "Un rai mince coupe le linge, puis s'arrête."),
    ),
    (1, 1, 3): L(
        ("narrateur", "Contre la chaise, le loup tient."),
        ("enfant-f", "On s'est assises, papa."),
        ("papa", "Le haut gardera son ombre."),
        ("maman", "Tiens bien le carton."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Victorina tapote le bois, léger."),
        ("narrateur", "Une poussière s'envole, puis retombe."),
        ("narrateur", "L'horloge tape une fois, le buffet se tait."),
    ),
    (1, 2, 1): L(
        ("narrateur", "Loin de l'écho, la lune était là, contre le carton."),
        ("enfant-f", "Tu as fini, papa."),
        ("papa", "Oui, le mot était long."),
        ("maman", "Tu as tenu la porte."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Une poussière sèche sur le carton."),
        ("narrateur", "Victorina fait marcher le loup, près du bois."),
        ("narrateur", "Le placard redevient un placard, simple."),
    ),
    (1, 2, 2): L(
        ("narrateur", "Dans le chuchotement, le mot a parlé."),
        ("enfant-f", "J'ai écouté, tout contre."),
        ("papa", "Tes oreilles étaient à la bonne place."),
        ("maman", "Le mur t'attend."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Victorina essuie une main sur son pantalon."),
        ("narrateur", "Une ombre de drap reste sur le bois."),
        ("narrateur", "Les oreilles du loup touchent le bois, sans bruit."),
    ),
    (1, 2, 3): L(
        ("narrateur", "Sur la marche, la lune penche."),
        ("enfant-f", "Je l'ai vue, contre le fond."),
        ("papa", "Le bois a gardé l'ombre."),
        ("maman", "Rentre le carton, après le pas."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Victorina souffle un peu sur les oreilles."),
        ("narrateur", "Une poussière s'envole, puis retombe."),
        ("narrateur", "La marche garde une ombre de drap, seule."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Sur le tabouret, Victorina a vu le cadre."),
        ("enfant-f", "Le mot est monté avec moi."),
        ("papa", "Je remporte le tabouret, tout à l'heure."),
        ("maman", "Essuie tes chaussettes, Victorina."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Le loup marche jusqu'au palier."),
        ("narrateur", "Une marche se tait, puis l'autre."),
        ("narrateur", "La planche du palier redevient une planche."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Tout en bas, la lune brille, près de la plinthe."),
        ("enfant-f", "Tu as dit petit, à la fin."),
        ("papa", "Merci d'avoir regardé en bas."),
        ("maman", "Le savon t'attend, près de l'eau."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Victorina pose le carton contre le mur du palier."),
        ("narrateur", "L'étagère reprend sa place, sage."),
        ("narrateur", "Les carreaux du palier reprennent la bande jaune."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Dans les bras de papa, la lune était là."),
        ("enfant-f", "On l'a prise, tout haut."),
        ("papa", "Tes yeux allaient assez loin."),
        ("maman", "Le haut gardera son ombre."),
        ("narrateur", "Le drap blanc tient le carton, droit."),
        ("narrateur", "Victorina pose le carton près des carreaux."),
        ("narrateur", "Les oreilles touchent l'air."),
        ("narrateur", "La bande jaune s'allonge, puis la lampe se tait."),
    ),
    (2, 1, 1): L(
        ("narrateur", "La lune rentre derrière une oreille, un petit clic."),
        ("enfant-f", "Il marche, lui !"),
        ("papa", "Sur le mur du buffet, les oreilles hautes."),
        ("maman", "Regarde, il ne glisse plus."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Une anse d'assiette garde un fil de colle."),
        ("narrateur", "Le buffet se tait autour des assiettes."),
        ("narrateur", "Un fil de colle sèche sur une anse."),
    ),
    (2, 1, 2): L(
        ("narrateur", "Le loup part entre deux ombres d'assiettes."),
        ("enfant-f", "J'ai posé la serviette, lui d'abord."),
        ("papa", "Puis le mot est venu."),
        ("maman", "Venez, le mur est prêt."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Victorina redresse une oreille, du pouce."),
        ("narrateur", "Une assiette tinte, puis se tait."),
        ("narrateur", "Le couloir laisse un rai sur le carton gris."),
    ),
    (2, 1, 3): L(
        ("narrateur", "Contre la chaise, le loup tient, museau bas."),
        ("enfant-f", "On s'est assis, lui sur moi."),
        ("papa", "Le haut gardera son ombre."),
        ("maman", "Tiens bien le carton."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Victorina gratte un peu de colle, du doigt."),
        ("narrateur", "Une poussière s'envole, puis retombe."),
        ("narrateur", "L'horloge tape, et le museau se tient."),
    ),
    (2, 2, 1): L(
        ("narrateur", "Loin de l'écho, la lune était collée au carton."),
        ("enfant-f", "Tu as fini, papa."),
        ("papa", "Oui, le mot était long."),
        ("maman", "Tu as tenu la porte."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Une poussière sèche sur une oreille."),
        ("narrateur", "Victorina fait marcher le loup, près du bois."),
        ("narrateur", "Le placard referme son écho, sans un mot."),
    ),
    (2, 2, 2): L(
        ("narrateur", "Dans le chuchotement, le loup a entendu la fin."),
        ("enfant-f", "J'ai collé mon oreille, tout contre."),
        ("papa", "Tes oreilles étaient à la bonne place."),
        ("maman", "Le mur t'attend."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Victorina essuie la colle sur son pantalon."),
        ("narrateur", "Une ombre d'oreille reste sur le bois."),
        ("narrateur", "Le loup avance, oreilles hautes, pas après pas."),
    ),
    (2, 2, 3): L(
        ("narrateur", "Sur la marche, la lune penche vers le museau."),
        ("enfant-f", "Il l'a vue, contre le fond."),
        ("papa", "Le bois a gardé l'ombre."),
        ("maman", "Rentre le carton, après le pas."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Victorina souffle un peu sur les oreilles."),
        ("narrateur", "Une poussière s'envole, puis retombe."),
        ("narrateur", "La marche garde une ombre de museau, seule."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Sur le tabouret, le loup a vu le cadre."),
        ("enfant-f", "Le mot est monté avec nous."),
        ("papa", "Je remporte le tabouret, tout à l'heure."),
        ("maman", "Essuie tes chaussettes, Victorina."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Le loup marche jusqu'au palier, oreilles hautes."),
        ("narrateur", "Une marche se tait, puis l'autre."),
        ("narrateur", "Deux oreilles passent la planche, puis s'arrêtent."),
    ),
    (2, 3, 2): L(
        ("narrateur", "Tout en bas, la lune brille, près du museau."),
        ("enfant-f", "Tu as dit petit, à la fin."),
        ("papa", "Merci d'avoir regardé en bas."),
        ("maman", "Le savon t'attend, près de l'eau."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Victorina pose le carton contre le mur du palier."),
        ("narrateur", "L'étagère reprend sa place, sage."),
        ("narrateur", "Le haut n'a plus rien à cacher, ce soir."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Dans les bras de papa, le loup a pris la lune."),
        ("enfant-f", "On l'a prise, tout haut."),
        ("papa", "Tes yeux allaient assez loin."),
        ("maman", "Le haut gardera son ombre."),
        ("narrateur", "Le loup de carton serre le bois."),
        ("narrateur", "Victorina pose le carton près des carreaux."),
        ("narrateur", "Les oreilles touchent l'air, près des carreaux."),
        ("narrateur", "La lampe du portemanteau tient un rond, puis s'éteint."),
    ),
    (3, 1, 1): L(
        ("narrateur", "La lune rentre dans le rond, un petit clic."),
        ("enfant-f", "Il marche, dans la lumière !"),
        ("papa", "Sur le mur du buffet, le rond le suit."),
        ("maman", "Le rond le tient, maintenant."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Une miette sèche dans le cercle jaune."),
        ("narrateur", "Le buffet se tait autour des assiettes."),
        ("narrateur", "Le savon sent, et le rond s'éteint."),
    ),
    (3, 1, 2): L(
        ("narrateur", "Le loup part, gris, dans le rond des assiettes."),
        ("enfant-f", "J'ai posé la serviette, sans clic."),
        ("papa", "Puis le mot est venu."),
        ("maman", "Venez, le mur est prêt."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Victorina pose le carton contre l'épaule."),
        ("narrateur", "Une assiette tinte, puis se tait."),
        ("narrateur", "Un rai mince dort dans le verre de la lampe."),
    ),
    (3, 1, 3): L(
        ("narrateur", "Contre la chaise, le loup tient, dans le rond."),
        ("enfant-f", "On s'est assises, lampe au sol."),
        ("papa", "Le haut gardera son ombre."),
        ("maman", "Tiens bien le carton."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Victorina tapote le bois, léger."),
        ("narrateur", "Une poussière s'envole, puis retombe."),
        ("narrateur", "L'horloge tape, le rond se tait."),
    ),
    (3, 2, 1): L(
        ("narrateur", "Loin de l'écho, la lune était là, dans le rond."),
        ("enfant-f", "Tu as fini, papa."),
        ("papa", "Oui, le mot était long."),
        ("maman", "Tu as tenu la porte."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Une poussière sèche sur le verre."),
        ("narrateur", "Victorina fait marcher le loup, près du bois."),
        ("narrateur", "Le verre de la lampe redevient froid."),
    ),
    (3, 2, 2): L(
        ("narrateur", "Dans le chuchotement, le rond a parlé."),
        ("enfant-f", "J'ai écouté, sans le clic."),
        ("papa", "Tes oreilles étaient à la bonne place."),
        ("maman", "Le mur t'attend."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Victorina essuie le verre sur son pantalon."),
        ("narrateur", "Le clic dort dans sa poche, oublié."),
        ("narrateur", "Une ombre ronde reste collée au bois."),
    ),
    (3, 2, 3): L(
        ("narrateur", "Sur la marche, la lune penche dans le rond."),
        ("enfant-f", "Je l'ai vue, contre le fond."),
        ("papa", "Le bois a gardé l'ombre."),
        ("maman", "Rentre le carton, après le pas."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Victorina souffle un peu sur les oreilles."),
        ("narrateur", "Une poussière s'envole, puis retombe."),
        ("narrateur", "La marche garde un rond, puis l'oublie."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Sur le tabouret, le rond a vu le cadre."),
        ("enfant-f", "Le mot est monté avec la lumière."),
        ("papa", "Je remporte le tabouret, tout à l'heure."),
        ("maman", "Essuie tes chaussettes, Victorina."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Le loup marche jusqu'au palier, dans le rond."),
        ("narrateur", "Une marche se tait, puis l'autre."),
        ("narrateur", "Le palier garde un cercle, puis s'éteint."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Tout en bas, la lune brille dans le rond, près de la plinthe."),
        ("enfant-f", "Tu as dit petit, à la fin."),
        ("papa", "Merci d'avoir regardé en bas."),
        ("maman", "Le savon t'attend, près de l'eau."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Victorina pose le carton contre le mur du palier."),
        ("narrateur", "L'étagère reprend sa place, sage."),
        ("narrateur", "La plinthe reprend son ombre, sans secret."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Dans les bras de papa, le rond a pris la lune."),
        ("enfant-f", "On l'a prise, tout haut."),
        ("papa", "Tes yeux allaient assez loin."),
        ("maman", "Le haut gardera son ombre."),
        ("narrateur", "La lampe ronde cliquette une fois, puis se tait."),
        ("narrateur", "Victorina pose le carton près des carreaux."),
        ("narrateur", "Les oreilles touchent l'air."),
        ("narrateur", "La bande jaune s'allonge, et le rond s'éteint."),
    ),
}


T3_SONS = {1: "tiroir,lune", 2: "porte,chuchotement", 3: "bois,tabouret"}
FIN_SONS = {1: "loup,assiettes", 2: "loup,placard", 3: "loup,palier"}
T3_EMPH = {
    1: {1: "tiroir", 2: "serviette", 3: "chaise"},
    2: {1: "porte", 2: "chuchotement", 3: "marche"},
    3: {1: "tabouret", 2: "plinthe", 3: "bras"},
}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "horloge,lampe", "emphasis": "loup de carton"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Trois affaires attendent près de la marche."),
            ("papa", "Le drap, le loup, ou la lampe ronde ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le drap blanc",
            "option_2_label": "le loup de carton",
            "option_3_label": "la lampe ronde",
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
                "option_1_label": "le buffet",
                "option_2_label": "le placard",
                "option_3_label": "l'étagère",
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
                    extra={"sons": FIN_SONS[c], "emphasis": "loup"},
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
        "Le soir, dans la maison, Victorina veut faire marcher son loup de carton "
        "sur le mur, tout grand, avec le drap et la lampe ronde. La lune de papier "
        "manque. Papa sait où, mais le mot s'arrête : elle coupe, le carton glisse, "
        "une oreille se plie. T1 = drap blanc / loup de carton / lampe ronde ; les "
        "trois partent. T2 = buffet (assiettes qui couvrent) / placard sous "
        "l'escalier (écho) / étagère du palier (trop haute). T3 = tiroir, serviette, "
        "chaise ; porte tenue, chuchotement, marche ; tabouret, regard d'en bas, "
        "bras de papa. Elle referme sa bouche. La lune rentre. Le loup marche. "
        "La bande jaune du couloir revient."
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
    if "victorina" not in blob:
        raise SystemExit("Victorina absente")
    for bad in (
        "escargot", "loupe", "carnet bleu", "pots de menthe", "trace d'argent",
        "inès", "ines", "noé", "sami", " toboggan", "balançoire", "bac à sable",
        "capitaine", "plic", "volet jaune", "biscuit", "gâteau", "cheval",
        "moulinet", "marché", "joue au salon", "dans le salon", "nichoir",
        "citronnade", "carillon", "prunier", "album",
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
        "Soir dans la maison : carreaux, bande jaune du portemanteau, savon, "
        "horloge. Victorina veut faire marcher son loup de carton sur le grand mur, "
        "avec le drap et la lampe ronde. La lune de papier manque. Papa commence : "
        "« dans le… » Elle coupe : « Dans le quoi ? » Le carton glisse, une oreille "
        "se plie, la bande recule. T1 change le premier geste (drap trop vite sur "
        "la bouche / loup tendu trop tôt, ombre sans oreilles / clic trop fort). "
        "T2 : buffet (assiettes qui couvrent le mot), placard (écho), étagère "
        "(trop haute). T3 change la manière : tiroir, serviette, chaise ; porte "
        "tenue, chuchotement, marche ; tabouret, regard d'en bas, bras de papa. "
        "Elle referme sa bouche. La lune rentre. Le loup marche. Chaque fin paie "
        "la bande, les oreilles, le savon ou l'horloge. Autre récit que TREE-COL-015 "
        "(pas d'escargot), DIF-070 (pas d'album), DIF-057 (pas de carillon).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N3 ≤ 16. Troupe D16 : Victorina, papa, maman.\n"
        "- Inès, bac-toboggan-balançoires, « On va apprendre » jetés. Première idée "
        "échoue (elle coupe, le loup glisse).\n"
        "- 27 fins textuellement distinctes (27 dernières images uniques). Merci vécu, pas un refrain Bravo.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/"
        "resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n"
        "- Tics « tout doux / tout calme / encore / déjà » écartés. Leçon vécue, "
        "pas dite (pas « laisser le temps »).\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
