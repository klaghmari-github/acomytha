#!/usr/bin/env python3
"""TREE-COL-003 — L'arrosoir et le tapis de Raphaël (F-NAR-019). N3, COL.ECO.002.

Jardin, campement du cerisier, arrosoir vert à bec bosselé, tapis rouge.
Leçon vécue : écouter / ne pas couper. Jamais dite.
Indice unique : un grain de cerise (ouverture → climax → 27 fins).
Monde ≠ TREE-COL-008 (Nina, goutte, laitue) ≠ TREE-DIF-006 (trois arrosoirs).
Texte + TTS. Pas apply. Pas audio. Pas git.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-003"
N3 = LIMITS["N3"]
TITLE = "L'arrosoir et le tapis de Raphaël"
FIL = (
    "Au campement du cerisier, papa déroule le tapis rouge : un grain de "
    "cerise glisse d'un pli et se colle au bec de l'arrosoir vert. Raphaël "
    "veut porter l'eau au pied de l'arbre avant que le soleil durcisse la "
    "terre. Mila veut le tapis, tout de suite, pour raconter. Ils parlent "
    "ensemble : personne n'entend. L'arrosoir reste. Sous le cerisier, près "
    "du bec, ou sur le tapis, la première idée rate. Seau, carafe ou coussin "
    "changent la deuxième ruse : Raphaël refuse de foncer. Merle, chat ou "
    "poule rendent le grain. Le grain, le bec et le tapis paient la fin."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de cerise",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=deux_envies_vont_se_couper; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_campement; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=une_oreille_a_manqué; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrete; intensite=1; destinataire=enfant; sous_texte=la_voix_a_une_place; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=la_premiere_idee_rate; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=deux_envies_sur_le_meme_objet; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de cerise",
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=fierte_calme; intensite=2; destinataire=enfant; sous_texte=le_grain_revient_quand_on_ecoute; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de cerise",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_le_bec_et_le_tapis_reviennent; tempo=pose; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in (
            "miel",
            "trois notes",
            "j'ai compris",
            "mission accomplie",
            "aujourd'hui,",
            "il faut attendre",
            "on va apprendre",
            "tout doux",
            "tout calme",
        ):
            if bad in low:
                raise SystemExit(f"interdit « {bad} »: {ph}")
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


def ssml(text: str, m: dict) -> str:
    body = html.escape(text, quote=False)
    emp = m.get("emphasis")
    if emp and emp in text:
        e = html.escape(emp, quote=False)
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
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(nc: dict, profile: str, extra_note: str = "", emphasis: str | None | bool = False) -> None:
    m = dict(PROFILES[profile])
    if emphasis is not False:
        m["emphasis"] = emphasis
    text = nc["text"]
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = 200 if profile in ("choice", "clue") else 0
    nc["pause_after_ms"] = m["pause"]
    nc["pause_sentence_ms"] = m["sentence"]
    nc["style_energy"] = m["energy"]
    nc["style_contour"] = m["contour"]
    nc["noise_scale_piper"] = m["noise"]
    nc["kokoro_speed"] = m["speed"]
    nc["melo_speed"] = m["speed"]
    nc["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    nc["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    nc["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    note = m["note"]
    if extra_note:
        note = note + "; " + extra_note
    nc["notes"] = note
    nc["night_policy"] = nc.get("night_policy") or "play"
    nc["locale"] = nc.get("locale") or "fr-FR"
    nc["voice_id"] = nc.get("voice_id") or "fr_FR-siwis-medium"


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str, ok: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
        "engine_ok_text": ok,
        "engine_near_text": "Tu es proche. Écoute l'indice.",
    }


def profile_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "opening"
    if kind == "transition_question":
        return "choice"
    if kind == "passage_question":
        return "clue"
    if kind == "passage_fin":
        return "ending"
    if cid.endswith("_C0001"):
        return "confirm"
    if "_T0003_P000" in cid and cid[-1] in "123":
        return "resolution"
    if "_T0002_P000" in cid and cid[-1] in "123":
        return "obstacle"
    return "action"


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

DEBUT = L(
    "narrateur|Le tapis rouge, plié en boudin, roule hors des bras de papa.",
    "narrateur|Il s'ouvre, chaud, avec une odeur de foin.",
    "narrateur|Un grain de cerise glisse hors d'un pli.",
    "narrateur|Le grain s'arrête, collé au bec de l'arrosoir.",
    "narrateur|L'arrosoir vert, lourd et bosselé, attend au campement du cerisier.",
    "narrateur|Maman pose la carafe, et un coussin rayé.",
    "papa|Raphaël, l'eau, pour le pied de l'arbre.",
    "maman|Le tapis est prêt, les genoux aussi.",
    "narrateur|En ce moment, Raphaël saisit l'anse, trop vite.",
    "enfant-m|Je veux arroser, maintenant !",
    "narrateur|Mila arrive, les joues chaudes, les mains ouvertes.",
    "enfant-f|Je veux le tapis, pour raconter !",
    "narrateur|Les deux voix partent ensemble, trop fort.",
    "narrateur|Papa tourne la carafe, il n'entend qu'un mélange.",
    "papa|J'ai entendu un mélange.",
    "maman|On n'a rien compris.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|La terre a soif !",
    "narrateur|Mila parle par-dessus, les mots se cognent.",
    "narrateur|Personne ne se tourne.",
    "narrateur|Le grain de cerise reste collé au bec, minuscule.",
)

T1Q = L(
    "narrateur|L'arrosoir vert reste là, lourd, près du tapis.",
    "papa|Raphaël, tu commences où ?",
    "maman|Sous le cerisier, près de l'arrosoir, ou sur le tapis ?",
)

T1 = {
    1: L(
        "narrateur|Raphaël traîne l'arrosoir sous le cerisier, toc.",
        "narrateur|L'ombre ronde refroidit ses genoux.",
        "enfant-m|La terre a soif, papa !",
        "enfant-f|Moi, je raconte, sous l'arbre !",
        "narrateur|Les deux voix se cognent contre le tronc.",
        "narrateur|Papa ne tourne pas la tête.",
        "papa|J'entends l'arbre, pas vos mots.",
        "narrateur|Maman s'accroupit, à la même hauteur.",
        "maman|Je te regarde, Raphaël.",
        "narrateur|Il ouvre la bouche, puis la referme.",
        "narrateur|Mila finit sa phrase, toute seule.",
        "enfant-f|Le tapis, après l'eau.",
        "papa|Je t'entends, maintenant.",
        "enfant-m|L'eau, au pied, s'il te plaît.",
        "maman|Merci, j'ai tes mots.",
        "narrateur|Le grain de cerise tient au bec, collé.",
    ),
    2: L(
        "narrateur|Raphaël reste près de l'arrosoir, l'anse dans la paume.",
        "narrateur|Le bec bosselé luit, un peu froid.",
        "enfant-m|C'est mon arrosoir !",
        "enfant-f|L'eau, pour mon histoire !",
        "narrateur|Deux mains tirent l'anse, l'eau bascule.",
        "narrateur|Une tache froide avance vers le tapis.",
        "maman|Le tapis, les enfants ?",
        "narrateur|Papa s'accroupit, une main sur le bec.",
        "papa|Une main, puis l'autre.",
        "narrateur|Raphaël lâche, les joues chaudes.",
        "narrateur|Mila lâche aussi, un peu plus tard.",
        "enfant-m|Je tiens, tu verses après.",
        "enfant-f|D'accord, toi l'anse.",
        "maman|Je t'entends, Raphaël.",
        "papa|Merci, le bec est resté droit.",
        "narrateur|Le grain de cerise n'a pas bougé.",
    ),
    3: L(
        "narrateur|Raphaël pose un genou sur le tapis rouge.",
        "narrateur|Le tissu chatouille, l'arrosoir reste à côté.",
        "enfant-m|La terre, d'abord !",
        "enfant-f|Mon histoire, d'abord !",
        "narrateur|Les voix se croisent, tout près des oreilles.",
        "narrateur|Papa plie un coin de tapis, sans lever les yeux.",
        "papa|J'entends le tissu, pas vos mots.",
        "narrateur|Maman s'accroupit, pose un doigt sur le grain.",
        "maman|Il est là, sur le bec.",
        "narrateur|Raphaël se tait, le doigt de maman l'arrête.",
        "narrateur|Mila met sa main sur sa bouche.",
        "papa|Je t'entends, maintenant.",
        "enfant-m|Le tapis, après l'arbre.",
        "enfant-f|Oui, après.",
        "maman|Merci, le tapis n'a pas bougé.",
        "narrateur|L'arrosoir vert garde le grain, tout contre le tapis.",
    ),
}

Q1 = {
    1: L(
        "narrateur|Sous l'arbre, les voix se sont cognées.",
        "papa|Après le silence, on a entendu qui ?",
    ),
    2: L(
        "narrateur|Deux mains tiraient l'anse.",
        "maman|Raphaël voulait quoi, près de l'eau ?",
    ),
    3: L(
        "narrateur|Maman a touché un petit grain.",
        "papa|Le grain de cerise est où ?",
    ),
}

C1 = {
    1: L(
        "enfant-m|Moi, Raphaël.",
        "papa|Oui, ta voix, après le silence.",
        "maman|Mila a fini, puis toi.",
        "enfant-f|Le tapis attend, un peu.",
        "narrateur|L'ombre du cerisier reste ronde, fraîche.",
        "papa|L'arrosoir peut avancer, maintenant.",
        "narrateur|Le grain tient au bec, minuscule phare.",
    ),
    2: L(
        "enfant-m|L'arrosoir !",
        "maman|Oui, l'arrosoir vert.",
        "papa|Une main, puis l'autre, ça a tenu.",
        "enfant-f|Moi je verse, après.",
        "narrateur|La tache froide s'arrête avant le tapis.",
        "maman|Le bec est droit, le grain aussi.",
        "narrateur|L'anse pèse, familière, dans la paume.",
    ),
    3: L(
        "enfant-m|Sur le bec !",
        "papa|Oui, collé au bec de l'arrosoir.",
        "maman|On l'a vu, parce que tu t'es tu.",
        "enfant-f|Moi aussi, je l'ai vu.",
        "narrateur|Le tapis rouge garde un pli de genou.",
        "papa|L'eau peut partir, le tapis reste.",
        "narrateur|Le grain brille, tout contre le tissu.",
    ),
}

T2Q = {
    1: L(
        "narrateur|Sous le cerisier, un objet peut aider l'eau.",
        "papa|Le seau, la carafe, ou le coussin ?",
        "maman|Tu prends quoi, Raphaël ?",
    ),
    2: L(
        "narrateur|Près du bec, un objet peut tenir l'eau.",
        "maman|Le seau, la carafe, ou le coussin ?",
        "papa|Tu prends quoi, Raphaël ?",
    ),
    3: L(
        "narrateur|Sur le tapis, un objet peut garder l'eau.",
        "papa|Le seau, la carafe, ou le coussin ?",
        "maman|Tu prends quoi, Raphaël ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Sous le cerisier, Mila tire le seau bleu.",
        "enfant-f|C'est mon puits !",
        "enfant-m|Non, c'est pour remplir l'arrosoir !",
        "narrateur|Leurs mains se cognent sur l'anse du seau.",
        "narrateur|L'eau saute, une tache froide vers les racines.",
        "papa|Le seau, les enfants ?",
        "narrateur|Raphaël ouvre la bouche, puis la referme.",
        "narrateur|Cette fois, il refuse de foncer.",
        "enfant-m|Tu finis, Mila.",
        "enfant-f|Le puits, après l'arbre.",
        "narrateur|Maman s'accroupit, essuie la tache du doigt.",
        "maman|L'arrosoir peut boire au seau, ensuite.",
        "narrateur|Le grain de cerise n'est plus sur le bec.",
        "narrateur|Raphaël cherche, les joues chaudes.",
    ),
    (1, 2): L(
        "narrateur|Mila saisit la carafe, trop vite, sous l'arbre.",
        "enfant-f|J'ai soif !",
        "enfant-m|C'est pour l'arrosoir !",
        "narrateur|La carafe glisse, un cercle d'eau naît.",
        "narrateur|Le grain quitte le bec, colle au verre mouillé.",
        "papa|La carafe, elle veut rester debout ?",
        "narrateur|Dans sa poitrine, l'envie pousse, puis recule.",
        "narrateur|Raphaël refuse de foncer vers le verre.",
        "enfant-m|Bois, puis on verse.",
        "enfant-f|Une gorgée, je te laisse le reste.",
        "narrateur|Maman pose un doigt sur le grain collé.",
        "maman|Il a voyagé, celui-là.",
        "papa|La carafe d'abord, l'arbre ensuite.",
        "narrateur|L'arrosoir attend, bec vide, un peu penché.",
    ),
    (1, 3): L(
        "narrateur|Mila tire le coussin rayé sous le cerisier.",
        "enfant-f|C'est mon trône !",
        "enfant-m|Non, pour caler l'arrosoir !",
        "narrateur|Le coussin glisse, l'arrosoir penche, toc.",
        "narrateur|Le grain roule, disparaît sous une rayure.",
        "maman|Le coussin, il a mangé quelque chose ?",
        "narrateur|Raphaël veut plonger la main, puis s'arrête.",
        "narrateur|Il refuse de foncer sous le tissu.",
        "enfant-m|Soulève, Mila, doucement.",
        "enfant-f|J'écoute, je soulève.",
        "narrateur|Papa s'accroupit, une main sur le bec.",
        "papa|Le trône peut caler, après l'eau.",
        "narrateur|Une rayure cache le grain, tout contre le tissu.",
        "narrateur|L'ombre de l'arbre tremble sur le coussin.",
    ),
    (2, 1): L(
        "narrateur|Près de l'arrosoir, Mila pose le seau trop haut.",
        "enfant-f|Je verse, moi !",
        "enfant-m|C'est mon anse !",
        "narrateur|Le seau déborde, l'eau file vers les chaussures.",
        "papa|Une verse, pas deux, d'accord ?",
        "narrateur|Raphaël sent les mots monter, trop vite.",
        "narrateur|Il les avale, refuse de foncer.",
        "enfant-m|Tu verses, je tiens le bec.",
        "enfant-f|Puis on change.",
        "narrateur|Maman essuie une chaussure, sans gronder.",
        "maman|Le grain, il a sauté où ?",
        "narrateur|Il n'est plus au bec, il sonne au fond du seau.",
        "papa|On le verra, quand l'eau sera calme.",
        "narrateur|L'arrosoir vert attend sa part, la bouche ouverte.",
    ),
    (2, 2): L(
        "narrateur|Près du bec, Mila débouche la carafe d'un coup.",
        "enfant-f|Je bois le froid !",
        "enfant-m|Il reste pour l'arbre !",
        "narrateur|Un filet manque le bec, mouille le bois de l'anse.",
        "maman|La carafe, un peu, pas tout ?",
        "narrateur|Raphaël tend la main, puis la retire.",
        "narrateur|Cette fois, il refuse de foncer.",
        "enfant-m|Une gorgée, puis le bec.",
        "enfant-f|J'ai entendu, une gorgée.",
        "narrateur|Papa tient la carafe, à leur hauteur.",
        "papa|Le grain a voyagé sur le verre, là.",
        "narrateur|Une tache sombre colle au fond, ronde.",
        "maman|On le reprend, après la gorgée.",
        "narrateur|L'arrosoir reste près d'eux, lourd, patient.",
    ),
    (2, 3): L(
        "narrateur|Près de l'arrosoir, Mila glisse le coussin sous le fond.",
        "enfant-f|Il va dormir, l'arrosoir !",
        "enfant-m|Il va tomber !",
        "narrateur|Le tissu cède, le bec tape la terre, toc.",
        "narrateur|Le grain fuit sous le coussin, invisible.",
        "papa|On soulève, ou on écrase ?",
        "narrateur|Raphaël veut arracher le coussin, puis non.",
        "narrateur|Il refuse de foncer, les poings ouverts.",
        "enfant-m|Tu soulèves, je regarde.",
        "enfant-f|J'écoute, je soulève un coin.",
        "narrateur|Maman s'accroupit, souffle sur la rayure.",
        "maman|Il est là, peut-être.",
        "papa|Le coussin cale, si on le pose après.",
        "narrateur|L'arrosoir penche, bec vers la terre sèche.",
    ),
    (3, 1): L(
        "narrateur|Sur le tapis, Mila pose le seau, pile au milieu.",
        "enfant-f|C'est ma table !",
        "enfant-m|Le tapis va boire l'eau !",
        "narrateur|Un cercle sombre naît dans le rouge.",
        "maman|Le seau, à côté, ou dessus ?",
        "narrateur|Raphaël veut crier, les mots lui brûlent.",
        "narrateur|Il les garde, refuse de foncer.",
        "enfant-m|À côté, s'il te plaît.",
        "enfant-f|J'ai entendu, à côté.",
        "narrateur|Papa glisse le seau hors du tissu, tout net.",
        "papa|Le grain, il est tombé dans le bleu ?",
        "narrateur|Au fond du seau, une petite chose ronde attend.",
        "maman|On le prend, quand tu auras fini ta phrase.",
        "narrateur|L'arrosoir veille au bord du tapis, anse vers Raphaël.",
    ),
    (3, 2): L(
        "narrateur|Sur le tapis, Mila plante la carafe entre deux plis.",
        "enfant-f|C'est mon vase !",
        "enfant-m|Elle va tomber, sur le rouge !",
        "narrateur|La carafe penche, un filet froid part.",
        "papa|Le vase, il aime le plat ?",
        "narrateur|Raphaël avance trop vite, puis s'arrête net.",
        "narrateur|Il refuse de foncer vers le verre.",
        "enfant-m|Pose-la, je tiens le pied.",
        "enfant-f|Tu tiens, je pose.",
        "narrateur|Maman glisse une assiette sous la carafe.",
        "maman|Le grain a quitté le bec, il colle au verre.",
        "narrateur|Une perle sombre, au fond, ne bouge plus.",
        "papa|On le reprend, après le vase.",
        "narrateur|L'arrosoir reste hors du tapis, bec vers l'arbre.",
    ),
    (3, 3): L(
        "narrateur|Sur le tapis, Mila et Raphaël tirent le même coussin.",
        "enfant-f|Mon oreiller !",
        "enfant-m|Pour l'arrosoir !",
        "narrateur|Le coussin plie, l'arrosoir toc contre le tissu.",
        "narrateur|Le grain saute, se cache dans une rayure.",
        "maman|Un coussin, deux envies, comment on fait ?",
        "narrateur|Raphaël tire, puis lâche, les yeux chauds.",
        "narrateur|Il refuse de foncer, les doigts ouverts.",
        "enfant-m|Toi tu t'assois, moi je cale le bec.",
        "enfant-f|J'ai entendu, je m'assois ici.",
        "narrateur|Papa cale le bec sur le bord du coussin.",
        "papa|Le grain, il est dans la rayure, je crois.",
        "maman|On le cherche, l'un après l'autre.",
        "narrateur|Le tapis rouge garde une bosse, là, minuscule.",
    ),
}

T3Q = {
    1: L(
        "narrateur|Quelque chose s'approche du seau.",
        "papa|Le merle, le chat, ou la poule ?",
        "maman|Qui écoutes-tu, là ?",
    ),
    2: L(
        "narrateur|Quelque chose s'approche de la carafe.",
        "maman|Le merle, le chat, ou la poule ?",
        "papa|Qui écoutes-tu, là ?",
    ),
    3: L(
        "narrateur|Quelque chose s'approche du coussin.",
        "papa|Le merle, le chat, ou la poule ?",
        "maman|Qui écoutes-tu, là ?",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Un merle saute sur le rebord du seau.",
        "enfant-m|Il picore le grain !",
        "enfant-f|C'est mon merle !",
        "narrateur|Les voix partent ensemble, le merle s'envole.",
        "narrateur|Le grain reste au fond, oublié.",
        "papa|On a parlé trop fort, non ?",
        "narrateur|Raphaël se tait, écoute le seau.",
        "enfant-m|À toi, Mila.",
        "enfant-f|Le merle a laissé le grain.",
        "narrateur|Ils attendent, le merle revient, picore ailleurs.",
        "maman|Vous l'avez laissé finir, lui aussi.",
        "narrateur|Raphaël pince le grain de cerise, mouillé.",
        "narrateur|Il le pose au pied du cerisier, près de l'eau.",
        "papa|L'arrosoir peut verser, maintenant.",
    ),
    (1, 1, 2): L(
        "narrateur|Un chat gris boit au seau, moustaches mouillées.",
        "enfant-f|Il va tout boire !",
        "enfant-m|Le grain, au fond !",
        "narrateur|Le chat lève la tête, fâché du bruit.",
        "maman|Il a des oreilles, lui aussi.",
        "narrateur|Raphaël ferme la bouche, les mains sur les genoux.",
        "enfant-m|Quand il part, on prend le grain.",
        "enfant-f|J'ai entendu, on attend.",
        "narrateur|Le chat s'en va, une moustache laisse un poil.",
        "papa|Le poil, et le grain, deux trésors.",
        "narrateur|Mila sort le grain de cerise, tout rond.",
        "narrateur|Raphaël verse, l'eau rejoint les racines.",
        "maman|Le seau est vide, l'arbre a bu.",
        "narrateur|Le poil gris reste collé au bleu du seau.",
    ),
    (1, 1, 3): L(
        "narrateur|Une poule rousse picore le rebord du seau.",
        "enfant-m|Elle veut le grain !",
        "enfant-f|C'est ma poule !",
        "narrateur|La poule recule, un caquet court.",
        "papa|Elle n'a pas fini, on dirait.",
        "narrateur|Raphaël avale son cri, les joues chaudes.",
        "enfant-m|On la laisse, puis on prend.",
        "enfant-f|D'accord, je me tais.",
        "narrateur|La poule part, une plume reste au seau.",
        "maman|La plume, et le grain, côte à côte.",
        "narrateur|Raphaël sort le grain de cerise, un peu terreux.",
        "narrateur|Il arrose le pied, l'eau fait un cercle sombre.",
        "papa|L'arbre a son cercle, la poule sa plume.",
        "narrateur|Le seau sonne creux, content.",
    ),
    (1, 2, 1): L(
        "narrateur|Le merle se pose près de la carafe mouillée.",
        "enfant-f|Il veut le grain collé !",
        "enfant-m|C'est le nôtre !",
        "narrateur|Le merle s'envole, le verre tinte.",
        "maman|Il a eu peur des deux voix.",
        "narrateur|Raphaël pose un doigt sur ses lèvres.",
        "enfant-m|Toi tu parles, moi j'écoute le merle.",
        "enfant-f|Il est sur la branche, il picore une cerise.",
        "narrateur|Ils attendent la fin du picorement.",
        "papa|Le grain, sur le verre, n'a pas bougé.",
        "narrateur|Mila décolle le grain de cerise, tout brillant.",
        "narrateur|Raphaël verse la carafe dans l'arrosoir, puis au pied.",
        "maman|L'arbre a bu le froid de la carafe.",
        "narrateur|Une cerise trop mûre tache la terre, à côté.",
    ),
    (1, 2, 2): L(
        "narrateur|Le chat se frotte à la carafe, le verre tremble.",
        "enfant-m|Il va la faire tomber !",
        "enfant-f|C'est mon chat !",
        "narrateur|Le chat miaule, trop fort pour les mots.",
        "papa|On a parlé dans son miaulement.",
        "narrateur|Raphaël se tait, une main sur la carafe.",
        "enfant-m|Je tiens, tu dis bonjour.",
        "enfant-f|Bonjour, chat.",
        "narrateur|Le chat s'assoit, un poil reste au verre.",
        "maman|Le grain est là, sous le poil.",
        "narrateur|Raphaël pince le grain de cerise, collé.",
        "narrateur|Il le pose sur le tapis, puis arrose l'arbre.",
        "papa|La carafe est vide, l'arbre non.",
        "narrateur|Le poil gris dessine une virgule sur le verre.",
    ),
    (1, 2, 3): L(
        "narrateur|La poule cogne la carafe du bec, toc.",
        "enfant-f|Elle veut boire !",
        "enfant-m|Le grain !",
        "narrateur|La poule caquette, les voix se perdent.",
        "maman|Elle n'a pas entendu vos mots, elle.",
        "narrateur|Raphaël attend le silence de la poule.",
        "enfant-m|Quand elle part, on décolle le grain.",
        "enfant-f|J'ai entendu, on attend.",
        "narrateur|La poule s'éloigne, une plume colle au verre.",
        "papa|Plume, grain, même voyage.",
        "narrateur|Mila donne le grain de cerise à Raphaël.",
        "narrateur|Il arrose, l'eau sent un peu le verre froid.",
        "maman|L'arbre a eu sa part, la poule la sienne.",
        "narrateur|La carafe sèche, un rond de poussière au pied.",
    ),
    (1, 3, 1): L(
        "narrateur|Le merle saute sur le coussin rayé, sous l'arbre.",
        "enfant-m|Il a le grain !",
        "enfant-f|Il va s'envoler avec !",
        "narrateur|Le merle picore la rayure, puis s'arrête.",
        "papa|Il cherche, comme vous.",
        "narrateur|Raphaël ne crie pas, cette fois.",
        "enfant-m|On le laisse, il n'a pas le grain.",
        "enfant-f|Je vois le grain, là, sous l'aile.",
        "narrateur|Le merle part, le grain de cerise reste.",
        "maman|Vous l'avez vu, parce que vous vous êtes tus.",
        "narrateur|Raphaël glisse la main, sort le grain.",
        "narrateur|Le coussin cale l'arrosoir, l'eau va aux racines.",
        "papa|Le trône a calé, l'arbre a bu.",
        "narrateur|Une plume noire reste dans la rayure.",
    ),
    (1, 3, 2): L(
        "narrateur|Le chat s'allonge sur le coussin, pile sur la rayure.",
        "enfant-f|Il écrase le grain !",
        "enfant-m|Pousse-le !",
        "narrateur|Le chat ronronne, sourd aux deux voix.",
        "maman|Il n'entend que son ronron, là.",
        "narrateur|Raphaël pose la main, sans pousser.",
        "enfant-m|On attend qu'il parte.",
        "enfant-f|Moi je le caresse, toi tu regardes.",
        "narrateur|Le chat s'en va, un poil sur le grain de cerise.",
        "papa|Poil et grain, même coussin.",
        "narrateur|Raphaël prend le grain, le pose près du tronc.",
        "narrateur|Le coussin cale le bec, l'eau part sans toc.",
        "maman|L'arbre a eu l'eau, le chat le soleil.",
        "narrateur|La rayure garde un creux de chat, tiède.",
    ),
    (1, 3, 3): L(
        "narrateur|La poule grimpe sur le coussin, un peu gauche.",
        "enfant-m|Elle va le salir !",
        "enfant-f|C'est ma poule, mon coussin !",
        "narrateur|La poule picore la rayure, trop près du grain.",
        "papa|On la laisse finir son picorement ?",
        "narrateur|Raphaël hoche la tête, la bouche fermée.",
        "enfant-m|Après, on prend le grain.",
        "enfant-f|J'ai entendu, après.",
        "narrateur|La poule descend, une plume rousse reste.",
        "maman|Le grain de cerise est là, à côté.",
        "narrateur|Mila le donne, Raphaël arrose le pied.",
        "narrateur|Le coussin, un peu poussiéreux, cale le bec.",
        "papa|L'eau a trouvé la terre, sans crier.",
        "narrateur|La plume rousse sèche au soleil, sur la rayure.",
    ),
    (2, 1, 1): L(
        "narrateur|Le merle se penche au-dessus du seau, près du bec.",
        "enfant-m|Il va pêcher le grain !",
        "enfant-f|Laisse-le, c'est drôle !",
        "narrateur|Le merle s'envole, l'eau tremble.",
        "maman|Deux voix, un oiseau, trop de bruit.",
        "narrateur|Raphaël écoute le seau, plus l'oiseau.",
        "enfant-m|Il est parti, on peut pêcher.",
        "enfant-f|Moi je tiens le seau, toi tu pinces.",
        "narrateur|Le grain de cerise monte, luisant d'eau.",
        "papa|Vous l'avez pêché, l'un après l'autre.",
        "narrateur|Raphaël le pose sur le bec, comme au début.",
        "narrateur|Puis il verse, du seau à l'arrosoir, au pied.",
        "maman|La chaîne d'eau a tenu, sans crier.",
        "narrateur|Le merle, plus loin, picore autre chose.",
    ),
    (2, 1, 2): L(
        "narrateur|Le chat pose une patte sur l'anse du seau.",
        "enfant-f|Il va le renverser !",
        "enfant-m|Le grain, au fond !",
        "narrateur|Le seau penche, l'eau menace les chaussures.",
        "papa|Une patte, deux enfants, qui lâche ?",
        "narrateur|Raphaël lâche les mots, pas le seau.",
        "enfant-m|Doucement, chat.",
        "enfant-f|J'ai entendu, doucement.",
        "narrateur|Le chat retire la patte, un poil flotte.",
        "maman|Le poil, et le grain, au fond.",
        "narrateur|Ils pêchent le grain de cerise, à deux mains.",
        "narrateur|Raphaël remplit l'arrosoir, verse au pied.",
        "papa|Le seau n'a pas versé sur les chaussures.",
        "narrateur|Le poil gris sèche sur l'anse, minuscule drapeau.",
    ),
    (2, 1, 3): L(
        "narrateur|La poule boit au seau, tout près de l'arrosoir.",
        "enfant-m|Elle va avaler le grain !",
        "enfant-f|Elle a soif, elle !",
        "narrateur|La poule lève le bec, un caquet les coupe.",
        "maman|Elle n'a pas fini de boire.",
        "narrateur|Raphaël attend, les doigts au bord du seau.",
        "enfant-m|Quand elle a fini, on cherche.",
        "enfant-f|D'accord, je me tais.",
        "narrateur|La poule part, une plume flotte, puis le grain.",
        "papa|Plume d'abord, grain ensuite.",
        "narrateur|Raphaël prend le grain de cerise, le sèche au tissu.",
        "narrateur|L'eau du seau rejoint l'arrosoir, puis la terre.",
        "maman|La poule a bu, l'arbre aussi.",
        "narrateur|Le bec bosselé porte une perle d'eau, puis plus.",
    ),
    (2, 2, 1): L(
        "narrateur|Le merle frappe la carafe du bec, un tintement.",
        "enfant-f|Il a vu le grain !",
        "enfant-m|C'est notre grain !",
        "narrateur|Le merle s'envole, le tintement reste.",
        "papa|On a parlé dans le tintement.",
        "narrateur|Raphaël écoute le verre, jusqu'au silence.",
        "enfant-m|Il est parti, tu décolles le grain.",
        "enfant-f|Je décolle, tu tiens la carafe.",
        "narrateur|Le grain de cerise se détache, un peu collant.",
        "maman|Vous l'avez eu, sans chasser l'oiseau.",
        "narrateur|Raphaël verse une gorgée au bec, le reste au pied.",
        "narrateur|L'arrosoir pèse moins, l'arbre plus.",
        "papa|La carafe a fait le pont, jusqu'à la terre.",
        "narrateur|Le tintement s'est tu, le campement aussi.",
    ),
    (2, 2, 2): L(
        "narrateur|Le chat lèche le verre de la carafe, près du grain.",
        "enfant-m|Il va l'avaler !",
        "enfant-f|Il aime le froid !",
        "narrateur|Le chat lève la tête, un miaulement les recouvre.",
        "maman|Il n'a pas fini sa langue.",
        "narrateur|Raphaël attend la fin du miaulement.",
        "enfant-m|À toi de dire, Mila.",
        "enfant-f|Il est parti, le grain est à nous.",
        "narrateur|Un poil reste collé au grain de cerise.",
        "papa|Poil et grain, même verre.",
        "narrateur|Raphaël essuie le grain, le pose sur le bec.",
        "narrateur|Puis il arrose, l'eau sent un peu le chat.",
        "maman|L'arbre n'a pas soif, plus.",
        "narrateur|La carafe vide fait un rond de soleil, au bois.",
    ),
    (2, 2, 3): L(
        "narrateur|La poule contourne la carafe, picore le grain collé.",
        "enfant-f|Non, poule !",
        "enfant-m|Attends, elle n'a pas fini !",
        "narrateur|La poule recule, surprise des deux voix.",
        "papa|Une voix, peut-être, aurait suffi.",
        "narrateur|Raphaël se tait, Mila aussi, un peu après.",
        "enfant-m|Elle picore à côté, plus le grain.",
        "enfant-f|Je le décolle, toi tu tiens.",
        "narrateur|Le grain de cerise vient, une plume avec.",
        "maman|Plume et grain, même voyage.",
        "narrateur|Raphaël pose le grain au bec, verse ensuite.",
        "narrateur|L'eau de la carafe rejoint le pied de l'arbre.",
        "papa|La poule a picoré ailleurs, l'arbre ici.",
        "narrateur|Le verre sèche, une plume rousse au col.",
    ),
    (2, 3, 1): L(
        "narrateur|Le merle saute sur le coussin, près de l'arrosoir.",
        "enfant-m|Il va faire tomber le bec !",
        "enfant-f|Il cherche le grain !",
        "narrateur|Le merle picore, le coussin s'enfonce.",
        "maman|On le laisse chercher, ou on crie ?",
        "narrateur|Raphaël choisit de ne pas crier.",
        "enfant-m|Il n'a pas le grain, il picore une filasse.",
        "enfant-f|Là, sous l'aile, le grain.",
        "narrateur|Le merle part, le grain de cerise reste.",
        "papa|Vous l'avez vu, sans le chasser.",
        "narrateur|Raphaël le reprend, le remet au bec.",
        "narrateur|Le coussin cale, l'eau part vers la terre sèche.",
        "maman|Le toc n'est pas revenu.",
        "narrateur|Une plume noire marque le coin du coussin.",
    ),
    (2, 3, 2): L(
        "narrateur|Le chat s'assoit sur le coussin, l'arrosoir penche.",
        "enfant-f|Il est trop lourd !",
        "enfant-m|Le grain, dessous !",
        "narrateur|Le chat ronronne, l'anse glisse d'un pouce.",
        "papa|On pousse le chat, ou on attend ?",
        "narrateur|Raphaël attend, une main sous le bec.",
        "enfant-m|Quand il part, on cale mieux.",
        "enfant-f|Je le caresse, tu tiens le bec.",
        "narrateur|Le chat s'en va, le grain de cerise apparaît.",
        "maman|Poil, grain, même creux.",
        "narrateur|Raphaël remet le grain au bec, puis verse.",
        "narrateur|Le coussin, plus plat, tient le fond.",
        "papa|L'eau a trouvé le pied, sans toc.",
        "narrateur|Un poil gris reste dans la rayure, tiède.",
    ),
    (2, 3, 3): L(
        "narrateur|La poule s'installe sur le coussin, près du bec.",
        "enfant-m|Elle va tout casser !",
        "enfant-f|C'est sa place, non !",
        "narrateur|La poule picore le tissu, trop près du grain.",
        "maman|Elle n'a pas fini, on dirait.",
        "narrateur|Raphaël se tait, les épaules hautes, puis basses.",
        "enfant-m|Après sa phrase à elle, on prend.",
        "enfant-f|Les poules n'ont pas de phrase, mais d'accord.",
        "narrateur|La poule descend, le grain de cerise est là.",
        "papa|Une plume, pour le chemin.",
        "narrateur|Raphaël pose le grain au bec, cale, verse.",
        "narrateur|L'eau rejoint la terre, sans un cri.",
        "maman|La poule a eu le coussin, l'arbre l'eau.",
        "narrateur|Le tissu rayé sent un peu la poule, puis plus.",
    ),
    (3, 1, 1): L(
        "narrateur|Le merle se pose au bord du tapis, près du seau.",
        "enfant-f|Il va marcher sur le rouge !",
        "enfant-m|Le grain, dans le seau !",
        "narrateur|Le merle saute, le tapis s'enfonce un peu.",
        "papa|Deux envies, un oiseau, on fait quoi ?",
        "narrateur|Raphaël écoute le merle, plus sa propre voix.",
        "enfant-m|Il picore à côté, pas le seau.",
        "enfant-f|Alors on pêche le grain.",
        "narrateur|Mila tient le seau, Raphaël pince le grain de cerise.",
        "maman|Vous l'avez eu, sans chasser l'oiseau.",
        "narrateur|Ils posent le grain sur le tapis, petit trésor.",
        "narrateur|Puis Raphaël arrose, l'arrosoir hors du rouge.",
        "papa|Le tapis est resté presque sec.",
        "narrateur|Le merle picore plus loin, une cerise trop mûre.",
    ),
    (3, 1, 2): L(
        "narrateur|Le chat s'allonge sur le tapis, la queue dans le seau.",
        "enfant-m|Sa queue, le grain !",
        "enfant-f|Il est trop bien, là !",
        "narrateur|Le chat lève la queue, l'eau tremble.",
        "maman|On le dérange, ou on attend ?",
        "narrateur|Raphaël attend, les genoux sur le rouge.",
        "enfant-m|Quand la queue sort, on pêche.",
        "enfant-f|Je le dis, toi tu pêches.",
        "narrateur|Le chat part, un poil flotte, puis le grain.",
        "papa|Poil, grain, même seau.",
        "narrateur|Raphaël sort le grain de cerise, le pose au tapis.",
        "narrateur|L'arrosoir verse au pied, loin du rouge.",
        "maman|Le cercle sombre du tapis sèche, un peu.",
        "narrateur|Le poil gris reste au bord du seau, comme un trait.",
    ),
    (3, 1, 3): L(
        "narrateur|La poule traverse le tapis, vers le seau.",
        "enfant-f|Mes genoux !",
        "enfant-m|Le grain, elle le veut !",
        "narrateur|La poule picore le rouge, trop près des mains.",
        "papa|On crie, ou on ouvre un chemin ?",
        "narrateur|Raphaël ouvre un chemin, sans un mot d'abord.",
        "enfant-m|Par là, poule.",
        "enfant-f|J'ai entendu, par là.",
        "narrateur|La poule part, une plume sur le tapis.",
        "maman|La plume, et le grain, deux souvenirs.",
        "narrateur|Ils pêchent le grain de cerise, le posent au tissu.",
        "narrateur|Raphaël arrose l'arbre, le seau à côté du tapis.",
        "papa|La poule a eu le chemin, l'arbre l'eau.",
        "narrateur|Le rouge du tapis porte une plume, et un grain.",
    ),
    (3, 2, 1): L(
        "narrateur|Le merle se pose sur l'assiette, près de la carafe.",
        "enfant-m|Il va faire tomber le vase !",
        "enfant-f|Il veut le grain du verre !",
        "narrateur|Le merle picore l'assiette, un tintement.",
        "maman|On le laisse, le temps d'un picorement ?",
        "narrateur|Raphaël hoche, la carafe tenue à deux mains.",
        "enfant-m|Toi tu parles, moi je tiens.",
        "enfant-f|Il est parti, le grain est à nous.",
        "narrateur|Mila décolle le grain de cerise du verre.",
        "papa|Vous l'avez eu, le merle a eu l'assiette.",
        "narrateur|Ils posent le grain sur le tapis, près du pli.",
        "narrateur|Raphaël verse, l'arrosoir hors du rouge, vers l'arbre.",
        "maman|Le vase n'est pas tombé.",
        "narrateur|L'assiette garde une fiente minuscule, essuyée.",
    ),
    (3, 2, 2): L(
        "narrateur|Le chat se frotte à la carafe, sur le tapis.",
        "enfant-f|Le vase !",
        "enfant-m|Le grain, au fond !",
        "narrateur|La carafe penche, l'assiette la rattrape.",
        "papa|Le chat, il a fini son frottement ?",
        "narrateur|Raphaël attend, les deux mains au pied du verre.",
        "enfant-m|Quand il part, tu décolles.",
        "enfant-f|Je décolle, tu tiens.",
        "narrateur|Le chat s'en va, un poil sur le grain de cerise.",
        "maman|Poil et grain, même fond.",
        "narrateur|Ils posent le grain au tapis, petit point sombre.",
        "narrateur|Raphaël arrose, loin du rouge, au pied de l'arbre.",
        "papa|La carafe a tenu, le tapis aussi.",
        "narrateur|Un poil gris reste sur l'assiette, comme une virgule.",
    ),
    (3, 2, 3): L(
        "narrateur|La poule cogne la carafe, l'assiette sonne.",
        "enfant-m|Elle va tout casser !",
        "enfant-f|Elle a soif, la poule !",
        "narrateur|La poule picore le col, trop près du grain.",
        "maman|Une voix, peut-être, pas deux.",
        "narrateur|Raphaël laisse Mila parler, lui tient le verre.",
        "enfant-f|Poule, le grain n'est pas pour toi.",
        "enfant-m|J'ai entendu, je tiens.",
        "narrateur|La poule s'éloigne, une plume au col.",
        "papa|Plume, grain, même col.",
        "narrateur|Mila donne le grain de cerise, Raphaël le pose au tapis.",
        "narrateur|Puis il arrose l'arbre, carafe vide, arrosoir allégé.",
        "maman|Le vase a tenu, la poule a picoré ailleurs.",
        "narrateur|L'assiette sèche, une plume rousse au bord.",
    ),
    (3, 3, 1): L(
        "narrateur|Le merle s'installe sur le coussin, au milieu du tapis.",
        "enfant-f|Mon oreiller !",
        "enfant-m|Le grain, dans la rayure !",
        "narrateur|Le merle picore la rayure, trop près du secret.",
        "papa|On le chasse, ou on attend ?",
        "narrateur|Raphaël attend, assis à son bord de coussin.",
        "enfant-m|Il n'a pas le grain, il picore un fil.",
        "enfant-f|Là, le grain, sous sa patte.",
        "narrateur|Le merle part, le grain de cerise est là.",
        "maman|Vous l'avez vu, l'un après l'autre.",
        "narrateur|Raphaël le pose au tapis, puis cale le bec.",
        "narrateur|L'eau part vers l'arbre, l'arrosoir hors du rouge.",
        "papa|Le coussin a calé, le merle a picoré.",
        "narrateur|Une plume noire reste dans la rayure, comme un trait.",
    ),
    (3, 3, 2): L(
        "narrateur|Le chat s'allonge sur le coussin, pile sur le grain.",
        "enfant-m|Il l'écrase !",
        "enfant-f|Il est trop bien, laisse-le !",
        "narrateur|Le chat ronronne, sourd aux deux envies.",
        "maman|On le dérange, ou on caresse ?",
        "narrateur|Raphaël caresse, sans tirer le coussin.",
        "enfant-m|Quand il part, je prends le grain.",
        "enfant-f|Je caresse, toi tu prends.",
        "narrateur|Le chat s'en va, le grain de cerise un peu chaud.",
        "papa|Poil et grain, même creux.",
        "narrateur|Ils posent le grain au tapis, près du genou.",
        "narrateur|Le coussin cale l'arrosoir, l'eau rejoint l'arbre.",
        "maman|Le chat a eu le soleil, l'arbre l'eau.",
        "narrateur|La rayure garde un creux tiède, et un poil.",
    ),
    (3, 3, 3): L(
        "narrateur|La poule s'assoit sur le coussin, au milieu du tapis.",
        "enfant-f|Elle va le salir !",
        "enfant-m|Le grain, dessous !",
        "narrateur|La poule picore, une rayure se lève.",
        "papa|On la pousse, ou on ouvre une place ?",
        "narrateur|Raphaël ouvre une place, sans pousser.",
        "enfant-m|À côté, poule, s'il te plaît.",
        "enfant-f|J'ai entendu, à côté.",
        "narrateur|La poule glisse, le grain de cerise apparaît.",
        "maman|Une plume, pour dire qu'elle est passée.",
        "narrateur|Raphaël pose le grain au tapis, cale, verse.",
        "narrateur|L'eau trouve le pied de l'arbre, loin du rouge.",
        "papa|La poule a eu le bord, l'arbre le centre.",
        "narrateur|Le coussin rayé sent le jardin, et un peu la poule.",
    ),
}

FINS = {
    (1, 1, 1): L(
        "narrateur|Le grain de cerise sèche au pied du cerisier.",
        "enfant-m|Il a voyagé dans le seau.",
        "enfant-f|Le merle l'a laissé.",
        "papa|Vous avez parlé, l'un après l'autre.",
        "maman|L'arrosoir vert a un cercle d'eau, au bec.",
        "narrateur|Le tapis rouge, plus loin, sent le foin.",
        "narrateur|Une plume noire croise le grain, puis plus.",
        "narrateur|L'ombre ronde s'allonge, et s'arrête.",
    ),
    (1, 1, 2): L(
        "narrateur|Le grain de cerise porte un poil gris, minuscule.",
        "enfant-f|Le chat a bu, l'arbre aussi.",
        "enfant-m|Le seau est vide, l'anse sèche.",
        "papa|Deux trésors, un seau.",
        "maman|L'arrosoir reste droit, sous l'arbre.",
        "narrateur|Le tapis n'a pas bu la tache froide.",
        "narrateur|Le poil s'envole, le grain reste.",
        "narrateur|La terre sombre fume un peu, au soleil.",
    ),
    (1, 1, 3): L(
        "narrateur|Le grain de cerise et la plume rousse sèchent ensemble.",
        "enfant-m|La poule a picoré le rebord.",
        "enfant-f|Nous, le fond.",
        "papa|Le seau sonne creux, content.",
        "maman|L'arbre a son cercle sombre.",
        "narrateur|L'arrosoir vert pèse moins, anse tiède.",
        "narrateur|Le tapis garde une odeur de foin, seulement.",
        "narrateur|La plume tremble, puis se tait.",
    ),
    (1, 2, 1): L(
        "narrateur|Le grain de cerise brille, un peu de verre dessus.",
        "enfant-m|Le merle a picoré une cerise, plus haut.",
        "enfant-f|Nous, le grain, plus bas.",
        "papa|La carafe a fait le pont.",
        "maman|L'arbre a bu le froid.",
        "narrateur|L'arrosoir, vide, penche vers le tapis.",
        "narrateur|Une tache de cerise mûre marque la terre.",
        "narrateur|Le campement sent le fruit, et l'eau.",
    ),
    (1, 2, 2): L(
        "narrateur|Le grain de cerise repose sur le tapis, un poil avec.",
        "enfant-f|Le chat a eu le verre.",
        "enfant-m|L'arbre a eu l'eau.",
        "papa|La carafe est vide, ronde.",
        "maman|Le poil dessine une virgule, puis s'en va.",
        "narrateur|L'arrosoir vert a un anneau mouillé, au fond.",
        "narrateur|Le tapis rouge a son petit point sombre.",
        "narrateur|L'ombre du cerisier couvre le grain, un moment.",
    ),
    (1, 2, 3): L(
        "narrateur|Le grain de cerise sèche près d'une plume rousse.",
        "enfant-m|La poule a cogné le verre.",
        "enfant-f|Nous, on a décollé le grain.",
        "papa|La carafe a un rond de poussière, au pied.",
        "maman|L'arbre a eu sa part.",
        "narrateur|L'arrosoir reste sous l'arbre, bec vers la terre.",
        "narrateur|Le tapis n'a pas reçu le filet froid.",
        "narrateur|La plume sèche, légère, sur le bois.",
    ),
    (1, 3, 1): L(
        "narrateur|Le grain de cerise tient près du tronc, une plume à côté.",
        "enfant-m|Le merle a picoré la rayure.",
        "enfant-f|Le trône a calé l'arrosoir.",
        "papa|L'eau a trouvé les racines, sans toc.",
        "maman|Le coussin a une plume noire, souvenir.",
        "narrateur|L'arrosoir vert, calé, ne penche plus.",
        "narrateur|Le tapis, plus loin, attend les genoux.",
        "narrateur|L'ombre tremble, puis s'apaise.",
    ),
    (1, 3, 2): L(
        "narrateur|Le grain de cerise porte un poil, au pied de l'arbre.",
        "enfant-f|Le chat a eu le soleil du coussin.",
        "enfant-m|Moi, le bec calé.",
        "papa|Le toc n'est pas revenu.",
        "maman|La rayure garde un creux tiède.",
        "narrateur|L'arrosoir a versé, l'anse est sèche.",
        "narrateur|Le tapis rouge sent le chat, un peu, puis plus.",
        "narrateur|Le poil s'envole vers le tronc, et s'arrête.",
    ),
    (1, 3, 3): L(
        "narrateur|Le grain de cerise sèche près d'une plume rousse.",
        "enfant-m|La poule a eu le coussin, un moment.",
        "enfant-f|Puis l'eau, à l'arbre.",
        "papa|Le bec a tenu, calé.",
        "maman|La poussière du coussin sent le jardin.",
        "narrateur|L'arrosoir vert a une terre sèche au fond, fine.",
        "narrateur|Le tapis n'a pas bougé, rouge et plat.",
        "narrateur|La plume rousse s'endort au soleil.",
    ),
    (2, 1, 1): L(
        "narrateur|Le grain de cerise est revenu au bec, comme au début.",
        "enfant-m|On l'a pêché, dans le seau.",
        "enfant-f|Le merle a regardé, sans le prendre.",
        "papa|La chaîne d'eau a tenu.",
        "maman|Seau, arrosoir, terre.",
        "narrateur|L'arrosoir vert a un goût de seau, au bec.",
        "narrateur|Le tapis, à l'écart, est resté sec.",
        "narrateur|Le merle picore plus loin, une autre affaire.",
    ),
    (2, 1, 2): L(
        "narrateur|Le grain de cerise sèche sur l'anse, un poil à côté.",
        "enfant-f|Le chat a posé sa patte.",
        "enfant-m|On n'a pas versé sur les chaussures.",
        "papa|Le seau a tenu, l'anse aussi.",
        "maman|L'arbre a bu, le chat s'est retiré.",
        "narrateur|L'arrosoir vert a une perle, puis plus.",
        "narrateur|Le tapis n'a pas vu cette eau-là.",
        "narrateur|Le drapeau de poil sèche, minuscule.",
    ),
    (2, 1, 3): L(
        "narrateur|Le grain de cerise sèche au tissu, près du bec.",
        "enfant-m|La poule a bu, l'arbre aussi.",
        "enfant-f|Une plume a flotté, avant le grain.",
        "papa|Plume d'abord, grain ensuite.",
        "maman|L'arrosoir a reçu le seau, puis la terre.",
        "narrateur|Le bec bosselé n'a plus de perle.",
        "narrateur|Le tapis rouge attend, hors de l'eau.",
        "narrateur|La poule caquette plus loin, sans eux.",
    ),
    (2, 2, 1): L(
        "narrateur|Le grain de cerise, un peu collant, tient au bec.",
        "enfant-m|Le merle a tinté le verre.",
        "enfant-f|Nous, on a décollé le grain.",
        "papa|La carafe a fait le pont, jusqu'à la terre.",
        "maman|Une gorgée, puis le pied de l'arbre.",
        "narrateur|L'arrosoir pèse moins, l'arbre plus.",
        "narrateur|Le tapis n'a pas reçu le filet.",
        "narrateur|Le tintement s'est tu, pour de bon.",
    ),
    (2, 2, 2): L(
        "narrateur|Le grain de cerise porte un poil, collé au bec.",
        "enfant-f|Le chat a léché le froid.",
        "enfant-m|L'arbre a eu le reste.",
        "papa|Poil et grain, même verre, même bec.",
        "maman|La carafe vide fait un rond de soleil.",
        "narrateur|L'arrosoir vert sent un peu le chat, puis l'eau.",
        "narrateur|Le tapis, à l'écart, reste chaud.",
        "narrateur|Le rond de soleil glisse, et s'en va.",
    ),
    (2, 2, 3): L(
        "narrateur|Le grain de cerise sèche au bec, une plume au col.",
        "enfant-m|La poule a picoré à côté.",
        "enfant-f|Nous, le grain, sans crier.",
        "papa|Une voix aurait suffi, deux se sont tues.",
        "maman|L'eau de la carafe a trouvé le pied.",
        "narrateur|L'arrosoir vert a un col de plume, un moment.",
        "narrateur|Le tapis n'a pas tremblé.",
        "narrateur|La plume rousse s'envole, le grain reste.",
    ),
    (2, 3, 1): L(
        "narrateur|Le grain de cerise est revenu au bec, une plume au coin.",
        "enfant-m|Le merle a picoré une filasse.",
        "enfant-f|Nous, le grain, sans le chasser.",
        "papa|Le coussin a calé, le toc n'est pas revenu.",
        "maman|L'eau a trouvé la terre sèche.",
        "narrateur|L'arrosoir vert tient droit, fond sur le tissu.",
        "narrateur|Le tapis, plus loin, n'a pas reçu d'eau.",
        "narrateur|La plume noire marque le coin, comme une flèche.",
    ),
    (2, 3, 2): L(
        "narrateur|Le grain de cerise sèche au bec, un poil dans la rayure.",
        "enfant-f|Le chat a eu le coussin.",
        "enfant-m|Moi, le bec, sans toc.",
        "papa|Le fond a tenu, plus plat.",
        "maman|L'eau a trouvé le pied.",
        "narrateur|L'arrosoir vert a une ombre de chat, au tissu.",
        "narrateur|Le tapis rouge reste hors du jeu, cette fois.",
        "narrateur|Le poil tiède s'en va, le grain non.",
    ),
    (2, 3, 3): L(
        "narrateur|Le grain de cerise tient au bec, une plume sur le tissu.",
        "enfant-m|La poule a eu le coussin, un moment.",
        "enfant-f|Puis l'arbre a eu l'eau.",
        "papa|Sans un cri, le bec a versé.",
        "maman|Le tissu rayé sent le jardin.",
        "narrateur|L'arrosoir vert, calé, ne penche plus.",
        "narrateur|Le tapis attend les genoux, plus tard.",
        "narrateur|La poule, plus loin, picore autre chose.",
    ),
    (3, 1, 1): L(
        "narrateur|Le grain de cerise sèche sur le tapis, petit trésor.",
        "enfant-m|On l'a pêché dans le seau.",
        "enfant-f|Le merle a eu une cerise, plus loin.",
        "papa|Le tapis est resté presque sec.",
        "maman|L'arrosoir a versé hors du rouge.",
        "narrateur|L'arrosoir vert, au bord, a un cercle d'eau.",
        "narrateur|Le seau bleu sèche, à côté.",
        "narrateur|Le merle picore sa cerise, sans eux.",
    ),
    (3, 1, 2): L(
        "narrateur|Le grain de cerise repose au tapis, un poil au seau.",
        "enfant-f|Le chat a mis sa queue dedans.",
        "enfant-m|On a attendu la queue.",
        "papa|Poil, grain, même seau, puis le tapis.",
        "maman|Le cercle sombre sèche, un peu.",
        "narrateur|L'arrosoir vert a versé au pied, loin du rouge.",
        "narrateur|Le tapis garde un trait de poil, minuscule.",
        "narrateur|Le chat, à l'ombre, ferme un œil.",
    ),
    (3, 1, 3): L(
        "narrateur|Le grain de cerise et une plume rousse tiennent au tapis.",
        "enfant-m|La poule a eu le chemin.",
        "enfant-f|L'arbre a eu l'eau.",
        "papa|Le seau, à côté, n'a plus versé.",
        "maman|Deux souvenirs, un tapis.",
        "narrateur|L'arrosoir vert sèche au bord, anse vers Raphaël.",
        "narrateur|Le rouge porte la plume, et le grain.",
        "narrateur|La poule, plus loin, n'a plus besoin d'eux.",
    ),
    (3, 2, 1): L(
        "narrateur|Le grain de cerise sèche près du pli du tapis.",
        "enfant-m|Le merle a eu l'assiette.",
        "enfant-f|Nous, le grain du verre.",
        "papa|Le vase n'est pas tombé.",
        "maman|L'arrosoir a versé hors du rouge.",
        "narrateur|La carafe vide luit, un peu.",
        "narrateur|L'assiette est nette, essuyée.",
        "narrateur|Le campement sent le verre, et le foin.",
    ),
    (3, 2, 2): L(
        "narrateur|Le grain de cerise fait un point sombre, sur le tapis.",
        "enfant-f|Le chat a frotté le vase.",
        "enfant-m|On a tenu le pied.",
        "papa|La carafe a tenu, le tapis aussi.",
        "maman|Un poil sur l'assiette, comme une virgule.",
        "narrateur|L'arrosoir vert, hors du rouge, a fini sa tâche.",
        "narrateur|Le point sombre du grain ne bouge plus.",
        "narrateur|Le chat, au soleil, lèche une patte.",
    ),
    (3, 2, 3): L(
        "narrateur|Le grain de cerise sèche au tapis, une plume à l'assiette.",
        "enfant-m|La poule a cogné le col.",
        "enfant-f|Mila a parlé, moi j'ai tenu.",
        "papa|Le vase a tenu, la poule a picoré ailleurs.",
        "maman|L'arrosoir allégé a rejoint l'arbre.",
        "narrateur|La carafe sèche, un rond de poussière au pied.",
        "narrateur|Le tapis rouge a son grain, son pli.",
        "narrateur|La plume rousse ne vole plus.",
    ),
    (3, 3, 1): L(
        "narrateur|Le grain de cerise sèche au tapis, une plume dans la rayure.",
        "enfant-m|Le merle a picoré un fil.",
        "enfant-f|Nous, le grain, l'un après l'autre.",
        "papa|Le coussin a calé, le merle a picoré.",
        "maman|L'arrosoir a versé hors du rouge.",
        "narrateur|La plume noire fait un trait, sur le tissu.",
        "narrateur|L'arrosoir vert, au bord, ne penche plus.",
        "narrateur|Le campement du cerisier s'assoit, enfin.",
    ),
    (3, 3, 2): L(
        "narrateur|Le grain de cerise, un peu chaud, sèche près du genou.",
        "enfant-f|Le chat a eu le soleil.",
        "enfant-m|Moi, le grain, après la caresse.",
        "papa|Poil et grain, même creux, puis le tapis.",
        "maman|L'arbre a eu l'eau, le chat le coussin.",
        "narrateur|L'arrosoir vert a versé, calé, sans toc.",
        "narrateur|La rayure garde un creux, et un poil.",
        "narrateur|Le tapis rouge sent le chat, puis le foin.",
    ),
    (3, 3, 3): L(
        "narrateur|Le grain de cerise sèche au tapis, une plume au bord.",
        "enfant-m|La poule a eu le bord.",
        "enfant-f|L'arbre, le centre de l'eau.",
        "papa|Sans pousser, une place s'est ouverte.",
        "maman|Le coussin sent le jardin, un peu la poule.",
        "narrateur|L'arrosoir vert, hors du rouge, a fini.",
        "narrateur|Le grain, le bec, le tapis, trois places.",
        "narrateur|Le campement du cerisier se tait, content.",
    ),
}

SONS = {
    "CHK_T0000_P0000": "tapis,arrosoir,jardin",
    "CHK_T0001_P0001": "cerisier,terre",
    "CHK_T0001_P0002": "arrosoir,anse",
    "CHK_T0001_P0003": "tapis,tissu",
}
SONS_T2 = {1: "seau,eau", 2: "carafe,verre", 3: "coussin,tissu"}
SONS_T3 = {1: "oiseau,jardin", 2: "chat,ronron", 3: "poule,plumes"}
SONS_FIN = {1: "cerisier,silence", 2: "tapis,foin", 3: "arrosoir,terre"}

QMETA = {
    1: qf(
        "Raphaël",
        "Raphaël | raphael | lui | sa voix | Raphaël après le silence",
        "Après le silence, on a entendu qui ?",
        "Oui, Raphaël.",
    ),
    2: qf(
        "l'arrosoir",
        "l'arrosoir | arrosoir | l arrosoir | l'anse | l'eau | arroser",
        "Raphaël voulait quoi, près de l'eau ?",
        "Oui, l'arrosoir.",
    ),
    3: qf(
        "bec",
        "bec | au bec | sur le bec | arrosoir | sur l'arrosoir | collé au bec",
        "Le grain de cerise est où ?",
        "Oui, sur le bec.",
    ),
}

EMPH = {
    "CHK_T0000_P0000": "grain de cerise",
    "CHK_T0001_P0001": "cerisier",
    "CHK_T0001_P0002": "arrosoir",
    "CHK_T0001_P0003": "tapis",
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("sous le cerisier", "près de l'arrosoir", "sur le tapis"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("le seau", "la carafe", "le coussin")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[j]
            extras[f"{p2}_T0003_P0000"] = t3("le merle", "le chat", "la poule")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = T3[(i, j, k)]
                sons[p3] = SONS_T3[k]
                s[f"{p3}_F0001"] = FINS[(i, j, k)]
                sons[f"{p3}_F0001"] = SONS_FIN[k]
    return s, sons, extras


def path_words(scripts: dict) -> tuple[int, int, float]:
    lengths = []
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                ids = [
                    "CHK_T0000_P0000",
                    "CHK_T0001_P0000",
                    f"CHK_T0001_P000{i}",
                    f"CHK_T0001_P000{i}_Q0001",
                    f"CHK_T0001_P000{i}_C0001",
                    f"CHK_T0001_P000{i}_T0002_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
                ]
                n = 0
                for cid in ids:
                    for ln in scripts[cid]:
                        n += words(ln.split("|", 1)[1])
                lengths.append(n)
    return min(lengths), max(lengths), sum(lengths) / len(lengths)


def write_tree(scripts: dict, sons: dict, extras: dict) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind in ("passage_question", "transition_question") else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        emp = EMPH.get(cid, False)
        voice(nc, profile_for(cid, kind), extra_note=f"chunk={cid}", emphasis=emp)
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Raphaël, Mila, papa, maman"
    out["setting"] = "jardin, campement du cerisier, arrosoir vert, tapis rouge"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tout doux",
        "tout calme",
        "il faut demander",
        "il faut attendre",
        "on doit demander",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
        "aujourd'hui,",
        "j'ai une idée. écoute",
        "celui où j'ai compris",
        "avec sa couleur, son poids",
        "lumière couleur de miel",
        "trois notes",
        "mission accomplie",
        "j'ai compris",
        "gouttes au bord",
        "laitue",
        "éclat vert",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    if TICS.search(blob):
        raise SystemExit(f"{SID} tic corpus")
    if "en ce moment" not in blob:
        raise SystemExit(f"{SID} manque en ce moment")
    if "grain de cerise" not in blob:
        raise SystemExit(f"{SID} manque grain de cerise")
    fins = [c["text"] for c in out["chunks"] if c.get("kind") == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"{SID} fins distinctes: {len(set(fins))}/{len(fins)}")
    t3s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage" and "_T0003_P000" in c["chunk_id"] and not c["chunk_id"].endswith("_P0000")
    ]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"{SID} T3 distincts: {len(set(t3s))}/{len(t3s)}")
    t2s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage"
        and "_T0002_P000" in c["chunk_id"]
        and "_T0003_" not in c["chunk_id"]
        and not c["chunk_id"].endswith("_P0000")
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"{SID} T2 distincts: {len(set(t2s))}/{len(t2s)}")
    for c in out["chunks"]:
        if c.get("kind") == "passage_fin":
            last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
            last = last_n[-1].split("|", 1)[1].lower()
            if "histoire" in last or "bravo" in last or "bon travail" in last:
                raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
            if "grain de cerise" not in c["text"].lower():
                raise SystemExit(f"{SID} {c['chunk_id']} fin sans grain de cerise")
        if not c.get("text_xai_tags") or not c.get("notes"):
            raise SystemExit(f"{SID} TTS manquant: {c['chunk_id']}")
    lo, hi, avg = path_words(scripts)
    print(f"chemins {lo}–{hi} mots (moyenne {avg:.0f})")
    if lo < 520 or hi > 780:
        raise SystemExit(f"{SID} longueur chemins hors barre: {lo}–{hi}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    s, n, e = build()
    write_tree(s, n, e)
    lo, hi, avg = path_words(s)
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Graphe source conservé "
        "(sous le cerisier / près de l'arrosoir / sur le tapis ; "
        "le seau / la carafe / le coussin ; "
        "le merle / le chat / la poule).\n\n"
        "## Promesse narrative\n\n"
        "Au campement du cerisier, papa déroule le tapis rouge. Un grain de "
        "cerise glisse d'un pli et se colle au bec de l'arrosoir vert. Raphaël "
        "veut porter l'eau au pied de l'arbre avant que le soleil durcisse la "
        "terre. Mila veut le tapis, tout de suite, pour raconter. Ils parlent "
        "ensemble : personne n'entend. L'arrosoir reste. Le premier lieu change "
        "la manière d'échouer, seau / carafe / coussin la deuxième ruse, merle / "
        "chat / poule le retour du grain. Le grain, le bec et le tapis paient la fin.\n\n"
        "## Vécu\n\n"
        "- Désir : arroser le cerisier, maintenant, avec l'arrosoir vert.\n"
        "- Déclencheur : Mila veut le tapis au même moment. Deux voix, un mélange.\n"
        "- Imprévu 1 : parler trop tôt, personne n'entend, sourire disparu, poitrine pleine.\n"
        "- Imprévu 2 : seau-puits, carafe-soif, coussin-trône ; le grain quitte le bec. Raphaël refuse de foncer.\n"
        "- COL.ECO.002 vécu (écouter / ne pas couper) : fermer la bouche, laisser finir, "
        "une voix puis l'autre, plaisir d'être entendu. Jamais dite.\n"
        "- Indice unique : grain de cerise, vu à l'ouverture, payé au climax et aux 27 fins.\n"
        f"- 27 fins distinctes. Chemins {lo}–{hi} mots (moyenne {avg:.0f}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Raphaël, Mila, papa, maman.\n"
        "- 86 nœuds, graphe et libellés d'options conservés.\n"
        "- 27 fins, 27 T3, 9 T2 textuellement distincts.\n"
        "- Premier choix ne retire pas l'arrosoir.\n"
        "- Objet nommé : arrosoir vert à bec bosselé (poids, toc, mission).\n"
        "- Coin inventif : le campement du cerisier (tapis rouge, odeur de foin).\n"
        "- Monde ≠ TREE-COL-008 (Nina, goutte, laitue) ≠ TREE-DIF-006 (trois arrosoirs).\n"
        "- Ouverture inventée (tapis-boudin, grain qui glisse). Pas « encore ».\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N3 ≤ 16 mots/phrase. Un merci vécu. `en ce moment`. Papa/maman + question.\n"
        "- Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Pas merle-trois-notes, miel, gouttes-refrain. Pas apply. Pas audio. Pas git.\n\n"
        "## Direction vocale\n\n"
        "`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        "tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. Tours "
        "de parole : envie de couper, retenue, écoute réelle, plaisir d'être entendu.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
