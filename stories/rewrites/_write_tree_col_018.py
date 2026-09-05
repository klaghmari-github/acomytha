#!/usr/bin/env python3
"""TREE-COL-018 — Le rond de soleil sur le tapis (F-NAR-019)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-018"
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_papier_va_se_plier; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; destinataire=enfant; sous_texte=la_phrase_a_eu_sa_place; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_papier_plie; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=decouragement; intensite=2; destinataire=enfant; sous_texte=couper_fait_rater; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=fierte_calme; intensite=2; destinataire=enfant; sous_texte=raconter_a_ouvert_le_rond; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=le_rond_a_trouve_le_papier; tempo=pose; sourire=léger; respiration=ample",
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
    ("narrateur", "Le chemin de l'école sent le pain chaud."),
    ("narrateur", "Les tuiles du village brillent, oranges."),
    ("narrateur", "Nina marche entre papa et maman."),
    ("narrateur", "Dans sa poche, un soleil de papier attend."),
    ("narrateur", "Maman l'a collé hier, avec de la farine."),
    ("narrateur", "La colle a séché, un peu rêche."),
    ("enfant-f", "Je le mets dans le vrai rond !"),
    ("maman", "Le vrai rond, c'est celui du tapis ?"),
    ("enfant-f", "Oui, avant qu'il glisse."),
    ("narrateur", "La classe sent le bois des patères."),
    ("narrateur", "Le manteau bleu de Nina reste tiède."),
    ("narrateur", "Sur le tapis, un rond de soleil dort."),
    ("narrateur", "Il est chaud, rond comme une assiette."),
    ("narrateur", "En ce moment, Nina sort le papier jaune."),
    ("enfant-f", "Je le pose là, tout de suite !"),
    ("narrateur", "La maîtresse tapote la table, toc toc."),
    ("maitresse", "On range les manteaux d'abord."),
    ("narrateur", "Les mots de Nina se cognent au toc."),
    ("narrateur", "Un camarade se penche, trop près."),
    ("narrateur", "Le soleil de papier glisse, et se plie."),
    ("enfant-f", "Non !"),
    ("narrateur", "Le rond de lumière a bougé, vers le mur."),
    ("narrateur", "Nina serre le papier, les joues chaudes."),
    ("papa", "On t'écoute ce soir, d'accord ?"),
    ("enfant-f", "D'accord."),
    ("narrateur", "Elle range le soleil plié, sans l'avoir posé."),
)

T1 = {
    1: dict(
        name="le tapis",
        passage=L(
            ("narrateur", "Nina pose un genou sur le tapis rêche."),
            ("narrateur", "Le rond de soleil lui chauffe la laine."),
            ("enfant-f", "Je glisse mon papier, vite."),
            ("narrateur", "La maîtresse parle du jour, près du tableau."),
            ("narrateur", "La phrase de Nina passe sous les mots."),
            ("narrateur", "Un soulier de camarade frôle le rond."),
            ("enfant-f", "Attention, mon soleil !"),
            ("narrateur", "Personne n'entend. Le papier tremble."),
            ("narrateur", "Elle referme la bouche, les épaules hautes."),
            ("narrateur", "Elle attend la fin du toc de la table."),
            ("maman", "J'ai fini de parler avec papa."),
            ("maman", "Je t'écoute."),
            ("enfant-f", "Le rond va partir. Mon papier est plié."),
            ("papa", "On le voit, collé dans ta main."),
            ("narrateur", "La lumière a glissé d'un doigt, vers le mur."),
        ),
        question="Quelle forme a la lumière sur le tapis ?",
        expected="rond",
        accepted="rond | un rond | rond de soleil | un rond de soleil | cercle",
        retry="Regarde la lumière posée sur le tapis.",
        ok="Oui, c'est un rond.",
        confirm=L(
            ("enfant-f", "Un rond !"),
            ("narrateur", "Oui, un rond de soleil."),
            ("maman", "Merci. J'ai entendu toute ta phrase."),
            ("narrateur", "Nina souffle. Le papier reste plié."),
            ("narrateur", "Sur le tapis, la lumière a reculé."),
        ),
        sons="tapis,classe",
        choice=L(
            ("narrateur", "Sur le tapis, trois jeux attendent le rond."),
            ("maman", "L'histoire, le dessin, ou la chanson ?"),
        ),
    ),
    2: dict(
        name="la table",
        passage=L(
            ("narrateur", "Nina grimpe sur la chaise, près de la table."),
            ("narrateur", "Le bois est lisse, un peu froid."),
            ("narrateur", "Son soleil de papier reste loin du tapis."),
            ("enfant-f", "Je descends le poser !"),
            ("narrateur", "La chaise racle. La maîtresse lève les yeux."),
            ("maitresse", "On reste assis, le temps de la phrase."),
            ("narrateur", "Nina se rassoit, le ventre serré."),
            ("narrateur", "Le papier jaune attend sur le bois."),
            ("enfant-f", "Il ne voit pas le vrai rond."),
            ("narrateur", "Elle veut crier. Elle pose les mains à plat."),
            ("papa", "Ta phrase, on la garde pour plus tard ?"),
            ("enfant-f", "Oui. Mais le rond glisse sans moi."),
            ("maman", "On l'a vu, de la porte."),
            ("narrateur", "Un crayon roule, et s'arrête contre le papier."),
        ),
        question="De quelle couleur est le soleil de papier ?",
        expected="jaune",
        accepted="jaune | il est jaune | papier jaune | soleil jaune",
        retry="Regarde le papier posé sur la table.",
        ok="Oui, il est jaune.",
        confirm=L(
            ("enfant-f", "Jaune, comme le vrai !"),
            ("narrateur", "Oui, le papier est jaune."),
            ("papa", "Merci d'être restée sur la chaise."),
            ("narrateur", "Le crayon dort contre le soleil plié."),
        ),
        sons="chaise,crayon",
        choice=L(
            ("narrateur", "À la table, trois jeux peuvent aider le papier."),
            ("papa", "L'histoire, le dessin, ou la chanson ?"),
        ),
    ),
    3: dict(
        name="le préau",
        passage=L(
            ("narrateur", "La classe sort sous le préau de bois."),
            ("narrateur", "L'ombre cache le tapis, et le rond."),
            ("enfant-f", "Il n'est plus là !"),
            ("narrateur", "Une goutte tombe du toit, ploc."),
            ("narrateur", "Nina lève le papier vers le ciel gris."),
            ("narrateur", "Le soleil de papier ne trouve plus sa place."),
            ("maitresse", "On écoute le vent, et les gouttes."),
            ("narrateur", "Nina ouvre la bouche pour crier au rond."),
            ("narrateur", "Le cri reste dedans. Ses poings se serrent."),
            ("maman", "Tu cherches la lumière, ma puce ?"),
            ("enfant-f", "Elle est restée sur le tapis, sans moi."),
            ("papa", "On l'a vue, avant de sortir."),
            ("narrateur", "La goutte dessine un point sur le papier jaune."),
        ),
        question="Qu'est-ce qui tombe du toit du préau ?",
        expected="goutte",
        accepted="goutte | une goutte | l'eau | une goutte d'eau | ploc",
        retry="Écoute le petit bruit sur le toit.",
        ok="Oui, c'est une goutte.",
        confirm=L(
            ("enfant-f", "Une goutte !"),
            ("narrateur", "Oui, une goutte du toit."),
            ("maman", "Merci d'avoir gardé le cri dedans."),
            ("narrateur", "Le point d'eau sèche sur le jaune."),
        ),
        sons="goutte,preau",
        choice=L(
            ("narrateur", "Sous le préau, trois jeux gardent le soleil."),
            ("maman", "L'histoire, le dessin, ou la chanson ?"),
        ),
    ),
}


def t2_histoire(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "La maîtresse ouvre un livre, sur le tapis."),
            ("narrateur", "Une page sent l'encre, un peu sèche."),
            ("narrateur", "Un soleil rond y dort, comme le vrai."),
            ("enfant-f", "C'est le mien !"),
            ("narrateur", "Le mot coupe la phrase du livre."),
            ("narrateur", "La maîtresse s'arrête. La page tremble."),
            ("narrateur", "Nina rentre le mot, les joues brûlantes."),
            ("maitresse", "J'arrive au bout. Ensuite, c'est toi."),
            ("narrateur", "Elle attend. Le renard de l'image s'assoit."),
            ("enfant-f", "Son soleil à lui n'est pas plié."),
            ("narrateur", "Le vrai rond chauffe son genou, un peu moins."),
        )
    if a == 2:
        return L(
            ("narrateur", "À la table, le livre s'ouvre contre le carton."),
            ("narrateur", "Le papier jaune de Nina frôle un soleil dessiné."),
            ("enfant-f", "Ils sont pareils !"),
            ("narrateur", "Sa phrase recouvre le mot de la maîtresse."),
            ("narrateur", "Deux voix se marchent dessus. Le livre se ferme."),
            ("narrateur", "Nina mord sa lèvre, déçue."),
            ("maitresse", "Je recommence la dernière phrase."),
            ("narrateur", "Cette fois, Nina laisse la voix aller au point."),
            ("papa", "Le renard du livre s'assoit dans un rond."),
            ("enfant-f", "Le mien est plié. Le sien est lisse."),
            ("narrateur", "Le crayon, sur la table, ne roule plus."),
        )
    return L(
        ("narrateur", "Sous le préau, la maîtresse tient le livre ouvert."),
        ("narrateur", "Le vent tourne une page, trop vite."),
        ("enfant-f", "Le soleil de l'image, il part !"),
        ("narrateur", "Son cri coupe le mot. Une goutte tombe."),
        ("narrateur", "La page se tache, juste sur le rond dessiné."),
        ("narrateur", "Nina se tait, les épaules basses."),
        ("maitresse", "On écoute la fin, malgré le vent."),
        ("narrateur", "Le renard de papier trouve un coin sec."),
        ("enfant-f", "Lui, il a un abri. Moi, une goutte."),
        ("maman", "Tu as laissé la page aller au bout."),
        ("narrateur", "Le point d'eau sèche au bord du livre."),
    )


def t2_dessin(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Sur le tapis, une feuille arrive, blanche."),
            ("narrateur", "Nina veut le crayon jaune, pour copier le rond."),
            ("narrateur", "Un camarade le prend au même instant."),
            ("enfant-f", "C'est pour mon soleil !"),
            ("narrateur", "Deux mains tirent. Le bois craque, presque."),
            ("narrateur", "Elle lâche, les doigts vides, le ventre dur."),
            ("maitresse", "Un crayon après l'autre. Ensuite, c'est toi."),
            ("narrateur", "Nina attend. Le vrai rond glisse vers le mur."),
            ("enfant-f", "Mon papier à moi est plié. Je dessine ça."),
            ("narrateur", "Quand le jaune revient, elle trace un pli."),
            ("papa", "On voit le pli, et on voit le rond."),
        )
    if a == 2:
        return L(
            ("narrateur", "À la table, Nina pose le papier plié."),
            ("narrateur", "Elle veut le coller sur sa feuille, tout de suite."),
            ("narrateur", "Un pot de colle avance, trop plein."),
            ("enfant-f", "Pas sur mon soleil !"),
            ("narrateur", "Le mot sort pendant la consigne."),
            ("narrateur", "La maîtresse n'entend que le bruit du pot."),
            ("narrateur", "Nina pose les mains à plat, impatiente."),
            ("maitresse", "D'abord la consigne. Après, ta feuille."),
            ("enfant-f", "Je dessine le pli, sans la colle."),
            ("maman", "Tu as gardé le papier au sec."),
            ("narrateur", "Un trait jaune fait le tour du pli."),
        )
    return L(
        ("narrateur", "Sous le préau, le papier claque dans le vent."),
        ("narrateur", "Nina veut tracer le rond perdu du tapis."),
        ("narrateur", "Le crayon jaune roule vers une flaque."),
        ("enfant-f", "Il va se noyer !"),
        ("narrateur", "Cette fois, elle n'attend pas : le crayon glisse."),
        ("narrateur", "Elle le rattrape, le bois froid et mouillé."),
        ("maitresse", "Merci d'avoir parlé, là. Il allait tomber."),
        ("enfant-f", "Je dessine le préau, sans rond."),
        ("papa", "Le toit gris, et le petit point d'eau ?"),
        ("narrateur", "Un trait jaune fait un ploc, sur la feuille."),
        ("narrateur", "Le vrai soleil de papier reste au poing, plié."),
    )


def t2_chanson(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Sur le tapis, la maîtresse tape deux fois."),
            ("narrateur", "Une chanson de soleil commence, toute simple."),
            ("enfant-f", "Moi aussi, je chante le rond !"),
            ("narrateur", "Sa voix part trop tôt, trop fort."),
            ("narrateur", "Les autres se taisent. Le fil de la chanson casse."),
            ("narrateur", "Nina rentre la tête, les joues chaudes."),
            ("maitresse", "On reprend. Toi, tu glisses dans le trou."),
            ("narrateur", "Elle attend la fin de la ligne."),
            ("enfant-f", "Soleil, soleil, sur le tapis."),
            ("papa", "Cette fois, on t'a entendue jusqu'au bout."),
            ("narrateur", "Le vrai rond tremble, comme un refrain."),
        )
    if a == 2:
        return L(
            ("narrateur", "À la table, les mains tapent le bois."),
            ("narrateur", "La chanson de soleil part, un peu serrée."),
            ("narrateur", "Le papier jaune vibre, au rythme."),
            ("enfant-f", "Je veux le couplet du pli !"),
            ("narrateur", "Le mot arrive pendant le refrain des autres."),
            ("narrateur", "Personne ne comprend. Nina serre le papier."),
            ("maitresse", "Un couplet après l'autre. Le tien vient."),
            ("narrateur", "Elle compte les taps, les épaules moins hautes."),
            ("enfant-f", "Mon soleil est plié, et il chante bas."),
            ("maman", "On a laissé ta note à sa place."),
            ("narrateur", "Le crayon, dans la coupelle, ne tinte plus."),
        )
    return L(
        ("narrateur", "Sous le préau, le vent chante avec les gouttes."),
        ("narrateur", "La maîtresse lance une chanson de pluie."),
        ("enfant-f", "Non, une de soleil !"),
        ("narrateur", "Sa voix recouvre le premier mot."),
        ("narrateur", "L'écho du préau mélange tout. Nina se tait."),
        ("maitresse", "La pluie d'abord. Le soleil, dans le trou."),
        ("narrateur", "Nina attend. Une goutte marque le temps."),
        ("enfant-f", "Soleil mouillé, soleil plié."),
        ("papa", "L'écho t'a rendue, cette fois."),
        ("narrateur", "Le papier jaune a un point d'eau, comme une note."),
        ("maman", "Tu as chanté après le vent, pas contre."),
    )


T2_FN = {1: t2_histoire, 2: t2_dessin, 3: t2_chanson}
T2_SONS = {1: "page", 2: "crayon", 3: "chanson"}
T2_NAME = {1: "l'histoire", 2: "le dessin", 3: "la chanson"}
T3_NAME = {1: "maman", 2: "papa", 3: "le doudou"}
T3_SONS = {1: "casserole", 2: "fauteuil", 3: "tissu"}
FIN_SONS = {1: "soupe,tapis", 2: "lampe,fauteuil", 3: "tissu,nuit"}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Le soir, le livre reste dans sa tête."),
            ("maman", "Tu racontes à maman, à papa, ou au doudou ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "Le soir, un peu de jaune reste au doigt."),
            ("papa", "Tu racontes à maman, à papa, ou au doudou ?"),
        )
    return L(
        ("narrateur", "Le soir, la chanson suit Nina jusqu'à la porte."),
        ("maman", "Tu racontes à maman, à papa, ou au doudou ?"),
    )


T3 = {
    (1, 1, 1): L(
        ("narrateur", "Le soir, la cuisine sent la soupe au potiron."),
        ("narrateur", "La louche tape la casserole, toc."),
        ("narrateur", "Nina court, le papier plié au poing."),
        ("enfant-f", "Maman, le rond, le renard, le soulier !"),
        ("narrateur", "Les mots se mélangent."),
        ("narrateur", "La louche s'arrête."),
        ("maman", "Attends. Je pose la casserole."),
        ("maman", "Je t'écoute."),
        ("enfant-f", "Un camarade a parlé trop près."),
        ("enfant-f", "Mon papier s'est plié, sur le tapis."),
        ("narrateur", "Maman lisse le papier avec le dos de la cuillère."),
        ("narrateur", "Il redevient presque rond, un peu tiède."),
        ("enfant-f", "On le met sur notre tapis ?"),
        ("maman", "Oui. Le vrai rond du soir est là."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Le soir, la lampe fait un rond jaune."),
        ("narrateur", "Papa est dans le fauteuil, une phrase au bout."),
        ("enfant-f", "Papa, le renard, mon tapis !"),
        ("narrateur", "Il n'a entendu que le mot tapis."),
        ("narrateur", "Nina serre le papier, impatiente."),
        ("narrateur", "Elle le pose sur son genou, et elle attend."),
        ("papa", "Voilà. Toute la phrase, maintenant."),
        ("enfant-f", "Le livre avait un soleil lisse. Le mien était plié."),
        ("narrateur", "Papa déplie le papier, très lentement."),
        ("narrateur", "La lampe y dessine un petit renard."),
        ("maman", "On t'écoute jusqu'au bout."),
        ("enfant-f", "Le rond du soir, il est à nous."),
    ),
    (1, 1, 3): L(
        ("narrateur", "Le soir, le doudou attend sur le lit, tiède."),
        ("narrateur", "Nina lui parle trop vite, le papier au poing."),
        ("enfant-f", "Renard, tapis, pli, chut !"),
        ("narrateur", "Le doudou ne répond pas. Elle souffle."),
        ("enfant-f", "Toi d'abord, plus lentement."),
        ("narrateur", "Elle raconte le soulier, puis le livre, puis le pli."),
        ("narrateur", "Le doudou penche l'oreille, sage."),
        ("maman", "On a entendu, de la porte."),
        ("papa", "Viens. On a un rond sur le tapis, ici aussi."),
        ("narrateur", "Nina pose le doudou et le papier dans la lumière."),
        ("enfant-f", "Lui, il a tout écouté."),
    ),
    (1, 2, 1): L(
        ("narrateur", "Le soir, un peu de jaune reste au doigt de Nina."),
        ("narrateur", "La soupe fume. Maman essuie la nappe."),
        ("enfant-f", "Maman, le crayon, le pli, le tapis !"),
        ("narrateur", "Le doigt jaune manque de tâcher la nappe."),
        ("maman", "D'abord tes mots. Après, on essuie."),
        ("narrateur", "Nina attend que la phrase de maman finisse."),
        ("enfant-f", "J'ai dessiné le pli, parce que le rond glissait."),
        ("narrateur", "Maman souffle sur le doigt, puis sur le papier."),
        ("narrateur", "Le trait jaune du dessin semble s'y poser."),
        ("papa", "On le met dans notre rond, maintenant ?"),
        ("enfant-f", "Oui. Sans colle, juste la lumière."),
    ),
    (1, 2, 2): L(
        ("narrateur", "Le soir, le crayon de poche dépasse du manteau."),
        ("narrateur", "Papa range les chaussures, le dos tourné."),
        ("enfant-f", "Regarde mon pli !"),
        ("narrateur", "Papa entend le mot pli, pas le reste."),
        ("narrateur", "Nina s'assoit sur le tapis, le crayon en l'air."),
        ("narrateur", "Elle attend qu'il se tourne."),
        ("papa", "Je te vois. Montre-moi."),
        ("enfant-f", "À l'école, j'ai tracé le pli du papier."),
        ("narrateur", "Papa pose le crayon à côté, sans le prendre."),
        ("maman", "Le rond de la lampe est assez grand pour deux."),
        ("narrateur", "Le papier et le crayon dorment dans la lumière."),
    ),
    (1, 2, 3): L(
        ("narrateur", "Le soir, le doudou a un point jaune au museau."),
        ("narrateur", "Nina l'a serré avec le doigt marqué de jaune."),
        ("enfant-f", "Pardon. C'est le dessin du tapis."),
        ("narrateur", "Elle veut tout dire d'un coup. Le doudou roule."),
        ("narrateur", "Elle le rattrape, et elle recommence, plus bas."),
        ("enfant-f", "J'ai attendu le crayon. J'ai dessiné le pli."),
        ("papa", "On t'écoute, nous aussi."),
        ("maman", "Le museau jaune, c'est une trace du jour."),
        ("narrateur", "Nina pose doudou et papier dans le rond du tapis."),
        ("enfant-f", "Toi, tu as le jaune. Moi, le pli."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Le soir, Nina entre en chantant le couplet du rond."),
        ("narrateur", "La louche de maman tape à côté, pas ensemble."),
        ("enfant-f", "C'est ma chanson !"),
        ("maman", "La mienne, c'est la soupe. Une après l'autre."),
        ("narrateur", "Nina se tait, le papier contre la poitrine."),
        ("narrateur", "La louche finit son toc. La cuisine s'ouvre."),
        ("enfant-f", "Sur le tapis, j'ai chanté trop tôt. Après, on m'a entendue."),
        ("maman", "Chante-moi le trou, maintenant."),
        ("narrateur", "Nina pose le papier, et glisse sa note."),
        ("papa", "Le rond du tapis suit le rythme, tout bas."),
        ("narrateur", "La soupe fume, sans recouvrir la chanson."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Le soir, papa chante en rangeant le manteau."),
        ("enfant-f", "Soleil, soleil !"),
        ("narrateur", "Les deux voix se marchent dessus, près du tapis."),
        ("papa", "Laisse-moi finir. Ensuite, ton couplet."),
        ("narrateur", "Nina attend, un pied sur la laine."),
        ("enfant-f", "À l'école, j'ai trop chanté tôt. Le fil a cassé."),
        ("narrateur", "Papa s'arrête pile, et penche l'oreille."),
        ("enfant-f", "Soleil, soleil, sur le tapis."),
        ("maman", "Cette fois, ta note a toute la place."),
        ("narrateur", "Le papier plié vibre, comme un petit tambour."),
        ("papa", "On le pose dans le rond, sur le dernier mot."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Le soir, Nina pose le doudou en public, sur le tapis."),
        ("enfant-f", "Toi, tu écoutes la chanson. Après, les mots."),
        ("narrateur", "Elle commence trop fort. Le doudou bascule."),
        ("narrateur", "Elle le redresse, et reprend plus bas."),
        ("enfant-f", "Soleil mouillé, non. Soleil du tapis."),
        ("maman", "On a le droit d'écouter, nous aussi ?"),
        ("enfant-f", "Oui. Le trou, c'est pour vous."),
        ("papa", "On le prend, ce trou."),
        ("narrateur", "Le doudou balance, puis s'arrête dans la lumière."),
        ("narrateur", "Le papier jaune s'y installe, enfin à plat."),
    ),
    (2, 1, 1): L(
        ("narrateur", "Le soir, l'assiette ronde attend près de la soupe."),
        ("narrateur", "Nina pose le papier contre le bord, trop vite."),
        ("enfant-f", "C'est le soleil du livre, maman !"),
        ("narrateur", "Une goutte de soupe manque le jaune."),
        ("maman", "L'assiette d'abord. Tes mots, juste après."),
        ("narrateur", "Nina recule le papier, les épaules hautes, puis basses."),
        ("enfant-f", "À la table, j'ai coupé l'histoire. Le livre s'est fermé."),
        ("enfant-f", "Après, j'ai attendu le point."),
        ("maman", "Là, j'ai tout. Merci."),
        ("narrateur", "Elle lisse le papier loin de la vapeur."),
        ("papa", "Le tapis de la maison a un rond, pour lui."),
    ),
    (2, 1, 2): L(
        ("narrateur", "Le soir, papa ouvre un vrai livre, dans le fauteuil."),
        ("enfant-f", "Le mien, à la table, s'était fermé !"),
        ("narrateur", "Sa phrase recouvre la sienne. La page claque."),
        ("papa", "Je finis celle-ci. Puis c'est la tienne."),
        ("narrateur", "Nina s'assoit par terre, le papier sur les genoux."),
        ("enfant-f", "Le renard du livre d'école s'assoit dans un rond."),
        ("enfant-f", "Le mien était plié, loin du tapis."),
        ("papa", "Je vois les deux, maintenant."),
        ("maman", "On t'écoute jusqu'à ton point."),
        ("narrateur", "Papa glisse le papier dans le rond de la lampe."),
        ("enfant-f", "Cette page-là, elle reste ouverte."),
    ),
    (2, 1, 3): L(
        ("narrateur", "Le soir, Nina installe le doudou à table, face à l'assiette."),
        ("enfant-f", "Toi, tu es la maîtresse. J'ouvre le livre."),
        ("narrateur", "Elle parle trop vite. Le doudou glisse sur le bois."),
        ("narrateur", "Elle le rattrape, et recommence, un mot après l'autre."),
        ("enfant-f", "J'ai coupé. J'ai attendu. Le renard a eu son rond."),
        ("maman", "La maîtresse en tissu a bien écouté."),
        ("papa", "Nous aussi, on prend notre tour."),
        ("narrateur", "Nina porte doudou et papier jusqu'au tapis."),
        ("narrateur", "La lampe leur fait un petit livre de lumière."),
    ),
    (2, 2, 1): L(
        ("narrateur", "Le soir, de la farine reste sur la table de cuisine."),
        ("narrateur", "Nina y pose le papier, pour coller le pli."),
        ("enfant-f", "Comme à l'école, sans le pot trop plein !"),
        ("narrateur", "La farine saute. Un nuage blanc cache le jaune."),
        ("maman", "On souffle d'abord. Ensuite, tu me racontes."),
        ("narrateur", "Nina attend que le nuage retombe."),
        ("enfant-f", "J'ai gardé le papier au sec, à la table."),
        ("enfant-f", "J'ai dessiné le pli, tout autour."),
        ("maman", "Je vois le trait. Merci d'avoir attendu la farine."),
        ("papa", "Un tapis, un rond, et plus de nuage."),
        ("narrateur", "Le papier retrouve sa couleur, dans la lumière."),
    ),
    (2, 2, 2): L(
        ("narrateur", "Le soir, le bois de la table de cuisine brille."),
        ("narrateur", "Nina y aligne crayon et papier, comme à l'école."),
        ("enfant-f", "Papa, le pot allait sur mon soleil !"),
        ("narrateur", "Papa coupe du pain, et rate la moitié des mots."),
        ("narrateur", "Elle pose le crayon, et attend la fin de la miche."),
        ("papa", "Me voilà. Le pot, le papier, le pli."),
        ("enfant-f", "J'ai tracé le tour du pli, sans colle."),
        ("maman", "Le bois d'ici ressemble à celui de la classe."),
        ("narrateur", "Papa porte le papier jusqu'au tapis, tout droit."),
        ("enfant-f", "Là, le rond peut le voir."),
    ),
    (2, 2, 3): L(
        ("narrateur", "Le soir, le doudou reçoit le crayon, trop gros."),
        ("enfant-f", "Tiens, dessine le pli."),
        ("narrateur", "La patte n'y arrive pas. Nina rit, puis s'arrête."),
        ("enfant-f", "D'accord. Je raconte, tu écoutes."),
        ("narrateur", "Elle dit le pot, la consigne, le trait jaune."),
        ("maman", "Le doudou a l'air de tout garder."),
        ("papa", "Nous, on a gardé une oreille, aussi."),
        ("narrateur", "Nina reprend le crayon, et pose le papier dans le rond."),
        ("enfant-f", "Toi, tu as écouté. Moi, j'ai tracé."),
        ("narrateur", "Un point de farine reste sur l'oreille du doudou."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Le soir, maman tapote la casserole, comme une table."),
        ("enfant-f", "C'est ma chanson de table !"),
        ("narrateur", "Deux rythmes se battent. La soupe tressaute."),
        ("maman", "Un tap, puis l'autre. Le tien après le mien."),
        ("narrateur", "Nina compte, le papier contre le bois de la chaise."),
        ("enfant-f", "À la table, j'ai trop serré le couplet. Après, on m'a mise dans le trou."),
        ("maman", "Voici un trou, dans ma casserole."),
        ("narrateur", "Nina glisse sa note. La vapeur danse."),
        ("papa", "On pose le papier quand la note est finie."),
        ("narrateur", "Le rond du tapis reçoit le jaune, sans bruit."),
    ),
    (2, 3, 2): L(
        ("narrateur", "Le soir, le fauteuil de papa grince en rythme."),
        ("enfant-f", "C'est le bois de la table, papa !"),
        ("narrateur", "Elle chante par-dessus le grincement. Rien n'est clair."),
        ("papa", "Je finis de m'asseoir. Ensuite, ton couplet."),
        ("narrateur", "Nina attend que le fauteuil se taise."),
        ("enfant-f", "Mon soleil est plié, et il chante bas."),
        ("papa", "Je l'entends, cette fois."),
        ("maman", "La note a trouvé sa chaise."),
        ("narrateur", "Papa pose le papier dans le rond, au silence."),
        ("enfant-f", "Le bois ne tinte plus."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Le soir, Nina fait écouter le refrain au doudou, à table."),
        ("enfant-f", "Toi, tu prends le trou."),
        ("narrateur", "Elle commence trop tôt. Le doudou bascule de la chaise."),
        ("narrateur", "Elle le rattrape, et laisse un vrai silence."),
        ("enfant-f", "Maintenant, c'est toi. Puis maman. Puis papa."),
        ("maman", "On prend notre trou, avec plaisir."),
        ("papa", "Le silence du doudou était le plus net."),
        ("narrateur", "Nina pose les trois dans le rond : doudou, papier, crayon."),
        ("enfant-f", "Chacun sa note."),
    ),
    (3, 1, 1): L(
        ("narrateur", "À la maison, une goutte sèche sur le papier."),
        ("narrateur", "Nina la montre à maman, au-dessus de la soupe."),
        ("enfant-f", "Le préau, le livre, la page tachée !"),
        ("narrateur", "La vapeur mouille le point d'eau. Nina recule, trop tard."),
        ("maman", "Loin de la casserole. Je t'écoute ici."),
        ("narrateur", "Nina s'assoit sur le tapis, le papier à l'abri."),
        ("enfant-f", "J'ai crié trop tôt. La page s'est tachée. Après, j'ai attendu la fin."),
        ("maman", "Le renard a trouvé son coin sec. Toi, le nôtre."),
        ("papa", "On souffle sur le point. Il s'en va."),
        ("narrateur", "Le papier, plus sec, entre dans le rond du tapis."),
    ),
    (3, 1, 2): L(
        ("narrateur", "Le soir, papa entend un ploc, dans la voix de Nina."),
        ("enfant-f", "C'est le toit du préau, dans l'histoire !"),
        ("narrateur", "Elle le dit pendant qu'il ferme la porte."),
        ("narrateur", "Le clac recouvre le ploc. Nina pince les lèvres."),
        ("papa", "Recommence. La porte a fini."),
        ("enfant-f", "Le vent a tourné la page. Une goutte est tombée sur le soleil."),
        ("enfant-f", "J'ai laissé la fin, malgré le vent."),
        ("papa", "Je tiens le ploc, maintenant."),
        ("maman", "Le tapis d'ici n'a pas de toit. Juste un rond."),
        ("narrateur", "Nina pose le papier. La lampe sèche le dernier point."),
    ),
    (3, 1, 3): L(
        ("narrateur", "Le soir, le doudou a le nez froid, comme le préau."),
        ("enfant-f", "Toi, tu as eu le vent. Moi, la goutte."),
        ("narrateur", "Elle parle trop vite. Le doudou tombe du lit."),
        ("narrateur", "Elle le réchauffe contre sa joue, puis reprend."),
        ("enfant-f", "Le livre a taché le rond. J'ai attendu la fin, sous le toit."),
        ("maman", "Le nez du doudou se réchauffe. Tes mots aussi."),
        ("papa", "On a de la place, sur le tapis, pour un nez froid."),
        ("narrateur", "Nina les pose tous les deux dans la lumière."),
        ("enfant-f", "Plus de vent. Plus de goutte."),
    ),
    (3, 2, 1): L(
        ("narrateur", "Le soir, le papier de Nina claque, comme au préau."),
        ("narrateur", "Elle le secoue au-dessus de la nappe, trop fort."),
        ("enfant-f", "Le crayon allait dans la flaque !"),
        ("maman", "Ici, pas de flaque. Pose, puis raconte."),
        ("narrateur", "Nina pose. Le papier s'apaise."),
        ("enfant-f", "Je l'ai rattrapé, sans attendre. Après, j'ai dessiné un ploc."),
        ("maman", "Tu as parlé pile pour le crayon. Merci."),
        ("papa", "Le toit gris, on le voit dans le trait ?"),
        ("enfant-f", "Oui. Et le vrai papier, il veut le tapis."),
        ("narrateur", "Maman glisse le jaune dans le rond, loin de toute eau."),
    ),
    (3, 2, 2): L(
        ("narrateur", "Le soir, papa veut voir le dessin du préau."),
        ("enfant-f", "Toit gris, point d'eau, crayon mouillé !"),
        ("narrateur", "Les mots tombent pendant qu'il cherche ses lunettes."),
        ("papa", "Une seconde. Je les ai. Reprends."),
        ("narrateur", "Nina attend, un pied impatient, puis calme."),
        ("enfant-f", "J'ai crié, parce que le crayon glissait. J'ai eu raison."),
        ("enfant-f", "Après, j'ai dessiné le ploc, sans rond."),
        ("papa", "Je vois le toit. Je vois le courage."),
        ("maman", "Le rond d'ici peut accueillir un dessin sans rond."),
        ("narrateur", "Le papier et la feuille se rejoignent, sous la lampe."),
    ),
    (3, 2, 3): L(
        ("narrateur", "Le soir, Nina cache le doudou loin du courant d'air."),
        ("enfant-f", "Pas le vent du préau, pas toi."),
        ("narrateur", "Elle veut tout dire d'un souffle. Le doudou s'échappe."),
        ("narrateur", "Elle le rattrape, et pose le papier d'abord."),
        ("enfant-f", "Le crayon allait se noyer. J'ai parlé. Puis j'ai dessiné."),
        ("maman", "Le doudou est au chaud. Tes mots aussi."),
        ("papa", "On les met dans le rond, loin de toute flaque."),
        ("narrateur", "Le museau du doudou frôle le papier, sans le plier."),
        ("enfant-f", "Toi, tu n'as pas eu le vent."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Le soir, l'écho du préau rentre avec Nina dans la cuisine."),
        ("enfant-f", "Soleil mouillé, soleil plié !"),
        ("narrateur", "Sa chanson recouvre la question de maman."),
        ("maman", "J'ai demandé si tu avais faim. Ensuite, ton couplet."),
        ("narrateur", "Nina hoche la tête, le papier collé au tablier."),
        ("enfant-f", "Un peu faim. Et j'ai chanté après le vent, pas contre."),
        ("maman", "L'écho d'ici, c'est la casserole. Elle te laisse un trou."),
        ("narrateur", "Nina glisse la note. La vapeur répond, puis se tait."),
        ("papa", "Le tapis prend le papier, sur le silence."),
        ("enfant-f", "Plus d'écho. Juste le rond."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Le soir, papa tapote le bois du fauteuil, comme une goutte."),
        ("enfant-f", "C'est le préau !"),
        ("narrateur", "Elle chante par-dessus le tap. Le rythme se casse."),
        ("papa", "Un tap à moi. Un mot à toi."),
        ("narrateur", "Nina attend le tap, puis pose sa note."),
        ("enfant-f", "Soleil mouillé, soleil plié."),
        ("papa", "L'écho m'a rendue ta voix, nette."),
        ("maman", "On a chanté avec la maison, pas contre la goutte."),
        ("narrateur", "Le papier entre dans le rond, au dernier tap."),
        ("enfant-f", "Le toit est loin. Le tapis est là."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Le soir, Nina berce le doudou au rythme des gouttes."),
        ("enfant-f", "Toi, tu es le vent. Moi, le soleil plié."),
        ("narrateur", "Elle commence trop tôt. Le doudou s'endort pile au milieu."),
        ("narrateur", "Elle s'arrête, surprise, puis sourit."),
        ("enfant-f", "D'accord. Ton trou, c'est le sommeil."),
        ("maman", "On chuchote, alors."),
        ("papa", "Le papier, on le pose sans le réveiller."),
        ("narrateur", "Nina glisse le jaune dans le rond, tout bas."),
        ("enfant-f", "Plus de vent. Un doudou qui dort, et un soleil."),
    ),
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    recap = {
        (1, 1, 1): "J'ai lu sur le tapis, et maman a lissé mon papier.",
        (1, 1, 2): "J'ai lu sur le tapis, et papa a vu le renard dans la lampe.",
        (1, 1, 3): "J'ai lu sur le tapis, et le doudou a eu l'oreille.",
        (1, 2, 1): "J'ai dessiné le pli, et maman a soufflé sur mon doigt.",
        (1, 2, 2): "J'ai dessiné le pli, et papa a posé le crayon à côté.",
        (1, 2, 3): "J'ai dessiné le pli, et le doudou a le museau jaune.",
        (1, 3, 1): "J'ai chanté trop tôt, puis maman m'a laissé un trou.",
        (1, 3, 2): "J'ai chanté trop tôt, puis papa a pris mon couplet.",
        (1, 3, 3): "J'ai chanté pour le doudou, et le papier s'est posé.",
        (2, 1, 1): "À la table, j'ai coupé le livre, puis maman m'a entendue.",
        (2, 1, 2): "À la table, le livre s'est fermé, puis papa a ouvert le sien.",
        (2, 1, 3): "À la table, le doudou a joué la maîtresse.",
        (2, 2, 1): "À la table, j'ai gardé le papier au sec, loin de la farine.",
        (2, 2, 2): "À la table, j'ai tracé le pli, et papa a porté le papier.",
        (2, 2, 3): "À la table, le doudou a trop gros crayon, et il a écouté.",
        (2, 3, 1): "À la table, la casserole m'a laissé un trou de chanson.",
        (2, 3, 2): "À la table, le fauteuil a fini de grincer, puis j'ai chanté.",
        (2, 3, 3): "À la table, le doudou a pris le silence du refrain.",
        (3, 1, 1): "Au préau, la page s'est tachée, et maman a séché le point.",
        (3, 1, 2): "Au préau, le ploc était dans ma voix, et papa l'a pris.",
        (3, 1, 3): "Au préau, le doudou avait le nez froid, comme moi.",
        (3, 2, 1): "Au préau, j'ai sauvé le crayon, et maman a mis le papier au sec.",
        (3, 2, 2): "Au préau, j'ai dessiné le toit, et papa a vu le courage.",
        (3, 2, 3): "Au préau, j'ai caché le doudou du vent, puis j'ai raconté.",
        (3, 3, 1): "Au préau, j'ai chanté après le vent, et la casserole m'a répondu.",
        (3, 3, 2): "Au préau, le tap de papa a rendu ma note nette.",
        (3, 3, 3): "Au préau, le doudou s'est endormi dans le trou de la chanson.",
    }
    tails = {
        (1, 1, 1): "Sur le tapis de la maison, le papier lisse dort dans le rond.",
        (1, 1, 2): "La lampe dessine un petit renard autour du papier.",
        (1, 1, 3): "Le doudou garde le papier, l'oreille dans la lumière.",
        (1, 2, 1): "Un trait jaune de craie brille au bord du rond.",
        (1, 2, 2): "Le crayon repose à côté du papier, sous la lampe.",
        (1, 2, 3): "Le point jaune du museau brille dans le rond tiède.",
        (1, 3, 1): "La louche s'est tue. Le papier chante tout bas, dans la laine.",
        (1, 3, 2): "Le dernier mot de papa reste posé sur le jaune.",
        (1, 3, 3): "Le doudou ne bascule plus. Voilà le papier, à plat.",
        (2, 1, 1): "L'assiette ronde garde une miette, comme un soleil.",
        (2, 1, 2): "Le livre de papa reste ouvert, face au papier.",
        (2, 1, 3): "Le doudou est assis à table, face à la lumière du tapis.",
        (2, 2, 1): "La nappe a un petit rond de farine, sous le papier.",
        (2, 2, 2): "Le bois de la cuisine brille, jaune un instant.",
        (2, 2, 3): "Un point de farine reste sur l'oreille du doudou.",
        (2, 3, 1): "La casserole reprend une note, puis s'arrête pour de bon.",
        (2, 3, 2): "Le fauteuil ne grince plus. Voilà le papier, tenu.",
        (2, 3, 3): "Trois silences dorment dans le rond : doudou, papier, crayon.",
        (3, 1, 1): "Une goutte sèche sur le papier, loin de la soupe.",
        (3, 1, 2): "La lampe sèche le dernier point, sans un ploc.",
        (3, 1, 3): "Le nez du doudou, plus chaud, frôle le jaune.",
        (3, 2, 1): "Plus aucun clac. Voilà le papier, au sec.",
        (3, 2, 2): "Le toit gris du dessin veille au bord de la lampe.",
        (3, 2, 3): "Le doudou, loin du vent, touche le papier sans le plier.",
        (3, 3, 1): "L'écho du préau finit dans la cuisine, tout mince.",
        (3, 3, 2): "Le tap du fauteuil s'arrête. Voilà le soleil, gardé.",
        (3, 3, 3): "Le doudou dort. Une goutte imaginaire sèche sur son poil.",
    }
    keepsake = {
        1: "Près de la porte, le manteau bleu sèche, la poche vide.",
        2: "La chaise de la cuisine ne racle plus.",
        3: "Dehors, le préau est noir. Ici, le rond reste.",
    }[a]
    who = {
        1: ("maman", "On a posé ton soleil. Tu veux un peu de soupe ?"),
        2: ("papa", "On a posé ton soleil. La lampe le garde ?"),
        3: ("maman", "On a posé ton soleil. Le doudou le garde ?"),
    }[c]
    return L(
        ("narrateur", keepsake),
        (who[0], who[1]),
        ("enfant-f", recap[(a, b, c)]),
        ("narrateur", "Voilà le rond du soir, autour du papier."),
        ("narrateur", tails[(a, b, c)]),
    )


def path_ids(a: int, b: int, c: int) -> list[str]:
    t1 = f"CHK_T0001_P000{a}"
    t2 = f"{t1}_T0002_P000{b}"
    t3 = f"{t2}_T0003_P000{c}"
    return [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        t1,
        f"{t1}_Q0001",
        f"{t1}_C0001",
        f"{t1}_T0002_P0000",
        t2,
        f"{t2}_T0003_P0000",
        t3,
        f"{t3}_F0001",
    ]


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "porte,pain", "emphasis": "rond de soleil"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Pour garder le rond, trois places attendent."),
            ("maman", "Le tapis, la table, ou le préau ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le tapis",
            "option_2_label": "la table",
            "option_3_label": "le préau",
        }},
    )

    for a, t1 in T1.items():
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(by_old[base], t1["passage"], "action", extra={"sons": t1["sons"], "emphasis": "rond"})
        qid = f"{base}_Q0001"
        by[qid] = voice(
            by_old[qid],
            L(("narrateur", t1["question"])),
            "clue",
            extra={"sons": "", "emphasis": None, "fields": {
                "expected_answer": t1["expected"],
                "accepted_examples": t1["accepted"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "C'est presque ça. Écoute l'indice.",
            }},
        )
        cid = f"{base}_C0001"
        by[cid] = voice(by_old[cid], t1["confirm"], "confirm", extra={"sons": "", "emphasis": "Merci"})
        tid = f"{base}_T0002_P0000"
        by[tid] = voice(
            by_old[tid], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "l'histoire",
                "option_2_label": "le dessin",
                "option_3_label": "la chanson",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], T2_FN[b](a), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": "papier"},
            )
            t3q = f"{p2}_T0003_P0000"
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": "maman",
                    "option_2_label": "papa",
                    "option_3_label": "le doudou",
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": T3_NAME[c]},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], ending(a, b, c), "ending",
                    extra={"sons": FIN_SONS[c], "emphasis": "rond"},
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

    out = dict(src)
    out["fil_rouge"] = (
        "Nina veut poser son soleil de papier dans le rond de lumière du tapis "
        "de classe, avant qu'il glisse au mur. Elle parle trop tôt : les mots "
        "se cognent au toc de la maîtresse, un camarade plie le papier. Tapis, "
        "table ou préau changent l'obstacle. Histoire, dessin ou chanson "
        "changent l'indice. Le soir, maman, papa ou le doudou changent la "
        "manière d'être entendue. Le papier retrouve un rond, à la maison."
    )
    out["title"] = "Le rond de soleil sur le tapis"
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "école, puis la maison le soir"
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

    lengths = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                n = sum(words(by[i]["text"]) for i in path_ids(a, b, c))
                lengths.append(n)
    nwords = sum(words(c["text"]) for c in out["chunks"])

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-COL-018 — Le rond de soleil sur le tapis\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Pas d'apply.\n\n"
        "## Vécu\n"
        "Chemin d'école, pain chaud, tuiles oranges. Nina a un soleil de papier "
        "collé à la farine : elle veut le poser dans le vrai rond de lumière du "
        "tapis de classe, avant qu'il glisse au mur. Première tentative : elle "
        "parle pendant le toc de la maîtresse. Un camarade se penche, le papier "
        "se plie, le rond recule. Joues chaudes, ventre serré.\n\n"
        "Tapis / table / préau changent l'obstacle (soulier sur la laine, chaise "
        "qui racle, goutte sous l'ombre). Histoire / dessin / chanson changent "
        "l'indice (soleil du livre, pli dessiné, couplet trop tôt). Maman / papa / "
        "doudou changent la manière d'être entendue le soir (cuillère tiède, "
        "lampe-renard, oreille de tissu). Nuance : on attend pour parler, sauf "
        "si le crayon glisse vers la flaque. Chaque fin ramène le papier dans un "
        "rond, à la maison.\n\n"
        "Leçon COL.ECO.001 vécue, non dite : à l'école on laisse la phrase aller "
        "au bout ; ce qui serre se raconte le soir, quand les oreilles sont prêtes.\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N2 ≤ 15. Troupe D16 : Nina, papa, maman.\n"
        "- T3 « la sœur » → le doudou (objet neutre, graphe conservé).\n"
        "- Leçon non récitée. Pas « tu écoutes / si malaise tu racontes ».\n"
        "- 27 fins textuellement distinctes (dernière image narrator unique).\n"
        f"- Chemins {min(lengths)}–{max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}.\n"
        "- Un merci vécu (T1), pas un refrain Bravo / bon travail.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}  chemins {min(lengths)}-{max(lengths)}")


if __name__ == "__main__":
    build()
